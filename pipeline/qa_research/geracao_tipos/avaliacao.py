"""Avaliação dos modelos: respondentes sem contexto + juiz, com tabela de acurácia atualizada durante a execução.

Lê as questões aprovadas de uma rodada de geração. Durante a geração completa, cada tópico fica pronto ao fim da
sua onda (`topicos/<item>/finalizado.json` e `topicos/<item>/aprovadas.jsonl`), e esta avaliação roda em paralelo:
a cada passagem pega os tópicos prontos, responde com cada modelo (esforço low; os gpt-4-1 não têm esforço), julga em
lotes de N respostas do mesmo modelo (o juiz não sabe qual modelo respondeu) e regrava a tabela.

Saídas em `<rodada>/avaliacao/`:
  ACURACIA.md, acuracia.csv   tabela geral, por tipo e por composição (regravadas a cada lote julgado)
  respostas/<modelo>/*.json   uma resposta por questão
  juiz/<modelo>/*.json        vereditos por lote
  avaliacoes.jsonl            questão, resposta e veredito de cada modelo (no fim de cada passagem)
"""
from __future__ import annotations

import csv
import hashlib
import io
import json
import threading
import time
from collections import defaultdict
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime, timezone
from pathlib import Path

from pipeline.qa_research.piloto_janela.core import ROOT, atomic_json, read_json
from pipeline.qa_research.tipos import TIPOS

from .core import prompt
from .rodadas import _filtrado, _nome_arq

# Respondentes: deployment[:esforço]. Os gpt-4-1 não são modelos de raciocínio e não aceitam esforço.
RESPONDENTES = {
    "gpt-5-4-nano": "gpt-5-4-nano-petrobras:low",
    "gpt-5-4": "gpt-5-4-petrobras:low",
    "gpt-5": "gpt-5-petrobras:low",
    "gpt-5-nano": "gpt-5-nano-petrobras:low",
    "gpt-4-1": "gpt-4-1-petrobras",
    "gpt-4-1-nano": "gpt-4-1-nano-petrobras",
}
JUIZ = "gpt-5-4-petrobras:medium"
VEREDITOS = ("correta", "parcial", "incorreta")
ENCERRADA = "geracao_encerrada"   # marcador gravado pelo script quando o processo de geração termina


def validar_resposta(d: dict) -> None:
    if not isinstance(d, dict) or not isinstance(d.get("resposta"), str) or not d["resposta"].strip():
        raise ValueError('Retorne {"resposta": "..."} com a resposta preenchida.')


def validar_juiz(d: dict, ids: list[str]) -> None:
    av = d.get("avaliacoes") if isinstance(d, dict) else None
    if not isinstance(av, list) or [a.get("id") for a in av] != ids:
        raise ValueError("Devolva exatamente um objeto por id recebido, na mesma ordem.")
    for a in av:
        if a.get("veredito") not in VEREDITOS:
            raise ValueError("veredito deve ser correta, parcial ou incorreta.")


class AvaliacaoModelos:
    def __init__(self, rodada: Path, *, respondentes: dict | None = None, juiz: str = JUIZ, lote_juiz: int = 8,
                 workers: int = 8, intervalo: int = 120, clientes: dict | None = None, progress=print):
        self.rodada = Path(rodada)
        self.saida = self.rodada / "avaliacao"
        self.respondentes = dict(respondentes or RESPONDENTES)
        self.juiz, self.lote_juiz = juiz, max(1, lote_juiz)
        self.workers, self.intervalo = workers, intervalo
        self.clientes, self.progress = dict(clientes or {}), progress
        self.lock = threading.Lock()
        self.vereditos: dict[str, dict[str, str]] = defaultdict(dict)   # modelo -> uid -> veredito
        self.questoes: dict[str, dict] = {}

    # ---------------------------------------------------------------- infraestrutura
    def cliente(self, papel: str, modelo: str):
        with self.lock:
            if papel not in self.clientes:
                from pipeline.inventario.llm import LLMClient, load_dotenv
                load_dotenv(ROOT)
                model, effort = modelo.rsplit(":", 1) if ":" in modelo else (modelo, "")
                self.clientes[papel] = LLMClient(
                    model, effort, self.saida / ".local" / f"{papel}.sqlite3", self.saida / "chamadas" / f"{papel}.jsonl",
                    provider="azure", max_attempts=3, timeout=600, max_tokens_cap=16000, max_calls=500000,
                    response_dir=self.saida / ".local" / "respostas" / papel)
            return self.clientes[papel]

    def _falha(self, nome: str, exc: Exception) -> None:
        atomic_json(self.saida / "falhas" / f"{nome}.json", {"erro": type(exc).__name__, "mensagem": str(exc)[:2000]})

    def _ok(self, nome: str) -> None:
        f = self.saida / "falhas" / f"{nome}.json"
        if f.exists():
            f.unlink()

    # ---------------------------------------------------------------- dados
    def carregar_questoes(self) -> dict[str, dict]:
        """Tópicos prontos (finalizado.json); sem marcadores, o aprovadas.jsonl da rodada (rodada antiga)."""
        out = {}
        prontos = sorted((self.rodada / "topicos").glob("*/finalizado.json")) if (self.rodada / "topicos").exists() else []
        arquivos = [p.parent / "aprovadas.jsonl" for p in prontos]
        if not prontos and (self.rodada / "aprovadas.jsonl").exists():
            arquivos = [self.rodada / "aprovadas.jsonl"]
        for arq in arquivos:
            if arq.exists():
                for linha in arq.read_text(encoding="utf-8").splitlines():
                    if linha.strip():
                        q = json.loads(linha)
                        out[q["uid"]] = q
        return out

    def _arq_resposta(self, modelo: str, uid: str) -> Path:
        return self.saida / "respostas" / modelo / f"{_nome_arq(uid)}.json"

    def _carregar_vereditos(self) -> None:
        for modelo in self.respondentes:
            for p in (self.saida / "juiz" / modelo).glob("*.json"):
                for a in read_json(p)["avaliacoes"]:
                    self.vereditos[modelo][a["uid"]] = a["veredito"]

    # ---------------------------------------------------------------- etapas
    def checar_modelos(self) -> None:
        """Uma chamada de teste por respondente: deployment inexistente sai da avaliação com aviso, sem travar os outros."""
        fora = {}
        for m, modelo in list(self.respondentes.items()):
            try:
                self.cliente(f"resp_{m}", modelo).json(prompt("respondente"), "Qual é a função de um separador trifásico?",
                                                      tag=f"teste_{m}", max_tokens=2000, validate=validar_resposta)
            except Exception as exc:  # noqa: BLE001
                if _filtrado(exc):
                    continue
                fora[m] = f"{type(exc).__name__}: {str(exc)[:300]}"
                del self.respondentes[m]
                self.progress(f"[avaliação] AVISO: {m} ({modelo}) indisponível e fora da avaliação: {fora[m]}", flush=True)
        if fora:
            atomic_json(self.saida / "modelos_indisponiveis.json", fora)

    def responder(self) -> int:
        tarefas = [(m, q) for m in self.respondentes for q in self.questoes.values()
                   if not self._arq_resposta(m, q["uid"]).exists()]
        if not tarefas:
            return 0
        self.progress(f"  respostas pendentes: {len(tarefas)} ({len(self.questoes)} questões x {len(self.respondentes)} modelos)",
                      flush=True)
        system = prompt("respondente")

        def um(t):
            m, q = t
            nome = f"resposta_{m}_{_nome_arq(q['uid'])}"
            try:
                d = self.cliente(f"resp_{m}", self.respondentes[m]).json(
                    system, q["pergunta"], tag=f"resposta_{m}", max_tokens=4000, item=q["item"], validate=validar_resposta)
                resposta = d["resposta"]
            except Exception as exc:  # noqa: BLE001
                if not _filtrado(exc):
                    self._falha(nome, exc)
                    return False
                resposta = "(sem resposta: bloqueada pelo filtro de conteúdo)"
            atomic_json(self._arq_resposta(m, q["uid"]), {"uid": q["uid"], "modelo": m, "resposta": resposta})
            self._ok(nome)
            return True

        return self._paralelo(tarefas, um, "respostas")

    def julgar(self, final: bool) -> int:
        """Lotes de `lote_juiz` respostas do mesmo modelo; o resto incompleto só é julgado na passagem final."""
        system, lotes = prompt("juiz_respostas"), []
        for m in self.respondentes:
            prontas = sorted((q for q in self.questoes.values()
                              if q["uid"] not in self.vereditos[m] and self._arq_resposta(m, q["uid"]).exists()),
                             key=lambda q: hashlib.sha256(f"{m}|{q['uid']}".encode()).hexdigest())
            for i in range(0, len(prontas), self.lote_juiz):
                lote = prontas[i:i + self.lote_juiz]
                if len(lote) == self.lote_juiz or final:
                    lotes.append((m, lote))
        if not lotes:
            return 0
        self.progress(f"  juiz ({self.juiz}): {len(lotes)} lotes de até {self.lote_juiz} respostas", flush=True)

        def um(t):
            m, lote = t
            ids = [f"Q{k}" for k in range(1, len(lote) + 1)]
            itens = [{"id": i, "pergunta": q["pergunta"], "resposta_referencia": q["resposta"],
                      "resposta_candidato": read_json(self._arq_resposta(m, q["uid"]))["resposta"]}
                     for i, q in zip(ids, lote)]
            nome = hashlib.sha256((m + "|" + "|".join(q["uid"] for q in lote)).encode()).hexdigest()[:16]
            try:
                d = self.cliente("juiz", self.juiz).json(system, json.dumps(itens, ensure_ascii=False), tag="juiz_respostas",
                                                         max_tokens=8000, validate=lambda d: validar_juiz(d, ids))
            except Exception as exc:  # noqa: BLE001
                self._falha(f"juiz_{m}_{nome}", exc)
                return False
            avs = [{"uid": q["uid"], "veredito": a["veredito"], "justificativa": a.get("justificativa", "")}
                   for a, q in zip(d["avaliacoes"], lote)]
            atomic_json(self.saida / "juiz" / m / f"{nome}.json", {"modelo": m, "avaliacoes": avs})
            with self.lock:
                for a in avs:
                    self.vereditos[m][a["uid"]] = a["veredito"]
                self.tabela()
            self._ok(f"juiz_{m}_{nome}")
            return True

        return self._paralelo(lotes, um, "juiz")

    def _paralelo(self, tarefas, funcao, rotulo: str) -> int:
        falhas, inicio = 0, time.time()
        with ThreadPoolExecutor(max_workers=max(1, self.workers)) as pool:
            for k, ok in enumerate(pool.map(funcao, tarefas), 1):
                falhas += 0 if ok else 1
                if k % 50 == 0 or k == len(tarefas):
                    eta = (time.time() - inicio) / k * (len(tarefas) - k)
                    self.progress(f"  {rotulo}: {k}/{len(tarefas)} | falhas {falhas} | restam ~{eta / 60:.1f} min", flush=True)
        return falhas

    # ---------------------------------------------------------------- tabela
    def tabela(self) -> dict:
        """Acurácia = % de corretas; 'com parcial' conta parcial como meio acerto. Só questões atuais da rodada."""
        def agrega(filtro):
            out = {}
            for m in self.respondentes:
                vs = [v for u, v in self.vereditos[m].items() if u in self.questoes and filtro(self.questoes[u])]
                n = len(vs)
                c, p = vs.count("correta"), vs.count("parcial")
                out[m] = {"n": n, "acuracia": round(100 * c / n, 1) if n else None,
                          "com_parcial": round(100 * (c + 0.5 * p) / n, 1) if n else None,
                          "corretas": c, "parciais": p}
            return out

        res = {"atualizado": datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC"), "questoes": len(self.questoes),
               "topicos": len({q["item"] for q in self.questoes.values()}), "juiz": self.juiz,
               "respondentes": self.respondentes, "geral": agrega(lambda q: True),
               "por_tipo": {t: agrega(lambda q, t=t: q["tipo"] == t) for t in TIPOS},
               "por_composicao": {c: agrega(lambda q, c=c: q.get("composicao") == c) for c in ("simples", "composta")}}
        atomic_json(self.saida / "acuracia.json", res)
        self._markdown(res)
        self._csv(res)
        return res

    def _markdown(self, res: dict) -> None:
        ms = list(self.respondentes)
        fmt = lambda d: "-" if d["acuracia"] is None else f"{d['acuracia']:.1f}"
        n_tipo = {t: sum(1 for q in self.questoes.values() if q["tipo"] == t) for t in TIPOS}
        L = ["# Acurácia dos modelos sem contexto", "",
             f"Atualizado em {res['atualizado']}. Questões prontas: {res['questoes']} em {res['topicos']} tópicos. "
             f"Juiz: `{res['juiz']}`. Respondentes com esforço low (os gpt-4-1 não têm esforço).",
             "Acurácia = % de respostas corretas; \"com parcial\" conta a parcial como meio acerto.", "",
             "## Geral", "", "| Modelo | julgadas | acurácia (%) | com parcial (%) | corretas | parciais |", "|---|---|---|---|---|---|"]
        for m in sorted(ms, key=lambda m: -(res["geral"][m]["acuracia"] or 0)):
            d = res["geral"][m]
            L.append(f"| {m} | {d['n']} | **{fmt(d)}** | {'-' if d['com_parcial'] is None else d['com_parcial']} "
                     f"| {d['corretas']} | {d['parciais']} |")
        L += ["", "## Por tipo de questão (acurácia %, julgadas entre parênteses)", "",
              "| Tipo | questões | " + " | ".join(ms) + " |", "|---|---|" + "---|" * len(ms)]
        for t in TIPOS:
            L.append(f"| {t} | {n_tipo[t]} | " + " | ".join(f"{fmt(res['por_tipo'][t][m])} ({res['por_tipo'][t][m]['n']})"
                                                         for m in ms) + " |")
        L += ["", "## Por composição (acurácia %)", "", "| Composição | " + " | ".join(ms) + " |", "|---|" + "---|" * len(ms)]
        for c, dd in res["por_composicao"].items():
            L.append(f"| {c} | " + " | ".join(f"{fmt(dd[m])} ({dd[m]['n']})" for m in ms) + " |")
        (self.saida / "ACURACIA.md").write_text("\n".join(L) + "\n", encoding="utf-8")

    def _csv(self, res: dict) -> None:
        buf = io.StringIO()
        w = csv.writer(buf)
        w.writerow(["recorte", "valor", "modelo", "julgadas", "acuracia", "com_parcial", "corretas", "parciais"])
        for m, d in res["geral"].items():
            w.writerow(["geral", "", m, d["n"], d["acuracia"], d["com_parcial"], d["corretas"], d["parciais"]])
        for chave in ("por_tipo", "por_composicao"):
            for valor, dd in res[chave].items():
                for m, d in dd.items():
                    w.writerow([chave, valor, m, d["n"], d["acuracia"], d["com_parcial"], d["corretas"], d["parciais"]])
        (self.saida / "acuracia.csv").write_text(buf.getvalue(), encoding="utf-8")

    def exportar(self) -> None:
        juiz = {}
        for m in self.respondentes:
            for p in (self.saida / "juiz" / m).glob("*.json"):
                for a in read_json(p)["avaliacoes"]:
                    juiz[(m, a["uid"])] = a
        with (self.saida / "avaliacoes.jsonl").open("w", encoding="utf-8", newline="\n") as f:
            for q in self.questoes.values():
                linha = {k: q.get(k) for k in ("uid", "item", "tipo", "composicao", "origem", "pergunta", "resposta")}
                for m in self.respondentes:
                    r = self._arq_resposta(m, q["uid"])
                    linha[f"resposta_{m}"] = read_json(r)["resposta"] if r.exists() else None
                    linha[f"veredito_{m}"] = juiz.get((m, q["uid"]), {}).get("veredito")
                f.write(json.dumps(linha, ensure_ascii=False) + "\n")

    # ---------------------------------------------------------------- execução
    def passagem(self, final: bool) -> int:
        with self.lock:
            self.questoes = self.carregar_questoes()
        falhas = self.responder() + self.julgar(final)
        with self.lock:
            self.tabela()
        self.exportar()
        return falhas

    def run(self, esperar: bool = False) -> int:
        """esperar: repete as passagens enquanto a geração não termina (marcador `geracao_encerrada`)."""
        self.saida.mkdir(parents=True, exist_ok=True)
        atomic_json(self.saida / "config.json", {"respondentes": self.respondentes, "juiz": self.juiz,
                                                 "lote_juiz": self.lote_juiz})
        self.checar_modelos()
        self._carregar_vereditos()
        while esperar and not (self.rodada / ENCERRADA).exists():
            self.passagem(final=False)
            self.progress(f"[avaliação] {len(self.questoes)} questões prontas; próxima verificação em {self.intervalo}s",
                          flush=True)
            for _ in range(self.intervalo):
                if (self.rodada / ENCERRADA).exists():
                    break
                time.sleep(1)
        falhas = self.passagem(final=True)
        self.progress(f"[avaliação] concluída: {len(self.questoes)} questões; tabela em {self.saida / 'ACURACIA.md'}", flush=True)
        return falhas
