"""Piloto de dificuldade v2: inventário (relações e encadeamentos) x janela EC v13, com avaliação cega.

Rubrica: pipeline/qa_research/DIFICULDADE_V2.md. Etapas, todas retomáveis (cada unidade vira um arquivo):
  1. relações por bloco (reaproveitadas de uma rodada anterior com --reusar);
  2. encadeamentos por documento (base das difíceis B);
  3. alvos com reservas: fáceis, médias, difíceis A (diagnóstico com resposta atraente) e B (encadeamento);
  4. questões: uma chamada por alvo; reservas só entram para cobrir alvos insuficientes;
  5. EC v13: geração por janela com a mesma rubrica e amostra na mesma composição;
  6. avaliação cega: dois respondentes sem contexto e um juiz forte (veredito, referência válida, atalho genérico);
  7. relatório por método e dificuldade, com o histórico da v1 e um filtro adversarial simulado.
"""
from __future__ import annotations

import csv
import hashlib
import json
import math
import random
import re
import shutil
import threading
import time
from collections import defaultdict
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime, timezone
from pathlib import Path

from pipeline.qa_research.dificuldade import CAMPOS_DESENHO, problemas_desenho, problemas_forma
from pipeline.qa_research.piloto_janela.core import (QA, ROOT, atomic_json, blocos, normalizar, palavras,
                                                     read_json, selecionar_focos, tema)

AQUI = Path(__file__).resolve().parent
PROMPTS = AQUI / "prompts"
ITENS = ("01_01", "02_02")
MODELOS = {
    "relacoes": "gpt-5-4-petrobras:low",
    "combinacoes": "gpt-5-4-petrobras:high",
    "questao": "gpt-5-4-petrobras:high",
    "juiz": "gpt-5-4-petrobras:high",
}
RESPONDENTES = ("gpt-4-1-nano-petrobras", "gpt-5-4-nano-petrobras:low")
TIPOS = ("facil", "media", "dificil_A", "dificil_B")
NIVEIS = ("facil", "media", "dificil")
TIPOS_REL = ("definicao", "mecanismo", "causa_efeito", "condicao", "criterio", "comparacao", "aplicacao")
NIVEIS_REL = ("facil", "media", "dificil_A")
# A difícil A precisa de mecanismo; critérios e definições tendem a respostas de prudência genérica.
PREFERENCIA_A = {"mecanismo": 0, "causa_efeito": 0, "condicao": 1, "aplicacao": 2, "comparacao": 2,
                 "criterio": 3, "definicao": 4}
VEREDITOS = {"correta": 1.0, "parcial": 0.5, "incorreta": 0.0}
CAMPOS_REL = ("afirmacao", "tipo", "condicoes", "limites", "trecho", "niveis", "explicacao_concorrente",
              "condicao_que_distingue")
CAMPOS_COMB = ("relacoes", "tipo", "titulo", "ponte", "cadeia", "cenario", "resposta", "resposta_atraente",
               "sinal_que_descarta", "condicoes_enunciado", "limites")
TETO_RESPOSTA = 30


def prompt(nome: str, **valores) -> str:
    texto = (PROMPTS / f"{nome}.md").read_text(encoding="utf-8").strip()
    for k, v in valores.items():
        texto = texto.replace("{{" + k + "}}", str(v))
    if "{{" in texto:
        raise ValueError(f"Marcador não preenchido em {nome}.md")
    return texto


def _lista_textos(v) -> bool:
    return isinstance(v, list) and all(isinstance(x, str) for x in v)


def _texto(v) -> bool:
    return isinstance(v, str) and bool(v.strip())


def _rng(*partes) -> random.Random:
    return random.Random(int(hashlib.sha256("|".join(map(str, partes)).encode()).hexdigest()[:16], 16))


def _absoluto(p) -> Path | None:
    return None if not p else (Path(p) if Path(p).is_absolute() else ROOT / p)


def _relativo(p: Path | None) -> str | None:
    if p is None:
        return None
    r = Path(p).resolve()
    return r.relative_to(ROOT).as_posix() if r.is_relative_to(ROOT) else r.as_posix()


def _nome(i: str) -> str:
    return re.sub(r"[^A-Za-z0-9_.-]", "_", i)


def nivel_agregado(tipo: str) -> str:
    return "dificil" if tipo.startswith("dificil") else tipo


# ---------------------------------------------------------------- validações (formato e ancoragem)
def validar_relacoes(d: dict, texto_bloco: str) -> None:
    if not isinstance(d, dict) or set(d) != {"status", "motivo", "relacoes"}:
        raise ValueError("Use exatamente as chaves status, motivo e relacoes.")
    if d["status"] not in ("ok", "sem_relacoes") or not isinstance(d["relacoes"], list):
        raise ValueError("status deve ser ok ou sem_relacoes; relacoes, uma lista.")
    if d["status"] == "sem_relacoes" and (d["relacoes"] or not _texto(d["motivo"])):
        raise ValueError("sem_relacoes exige lista vazia e motivo.")
    if d["status"] == "ok" and not 1 <= len(d["relacoes"]) <= 8:
        raise ValueError("status ok exige de 1 a 8 relações.")
    bloco = normalizar(texto_bloco).lower()
    for k, r in enumerate(d["relacoes"], 1):
        if not isinstance(r, dict) or set(r) != set(CAMPOS_REL):
            raise ValueError(f"Relação {k}: use exatamente os campos {', '.join(CAMPOS_REL)}.")
        if not _texto(r["afirmacao"]) or r["tipo"] not in TIPOS_REL:
            raise ValueError(f"Relação {k}: afirmacao vazia ou tipo inválido.")
        if not (_lista_textos(r["condicoes"]) and _lista_textos(r["limites"])):
            raise ValueError(f"Relação {k}: condicoes e limites devem ser listas de textos.")
        if not r["niveis"] or not isinstance(r["niveis"], list) or not set(r["niveis"]) <= set(NIVEIS_REL):
            raise ValueError(f"Relação {k}: niveis deve conter facil, media e/ou dificil_A.")
        if "dificil_A" in r["niveis"] and not (_texto(r["explicacao_concorrente"])
                                               and _texto(r["condicao_que_distingue"])):
            raise ValueError(f"Relação {k}: dificil_A exige explicacao_concorrente e condicao_que_distingue.")
        if not _texto(r["trecho"]) or normalizar(r["trecho"]).lower().strip(" .;:\"'") not in bloco:
            raise ValueError(f"Relação {k}: trecho deve ser cópia literal do bloco.")


def validar_combinacoes(d: dict, bloco_da_relacao: dict, maximo: int) -> None:
    if not isinstance(d, dict) or set(d) != {"combinacoes", "observacao"}:
        raise ValueError("Use exatamente as chaves combinacoes e observacao.")
    if not isinstance(d["combinacoes"], list) or len(d["combinacoes"]) > maximo:
        raise ValueError(f"combinacoes deve ser lista com no máximo {maximo} itens.")
    for k, c in enumerate(d["combinacoes"], 1):
        if not isinstance(c, dict) or set(c) != set(CAMPOS_COMB):
            raise ValueError(f"Combinação {k}: use exatamente os campos {', '.join(CAMPOS_COMB)}.")
        ids = c["relacoes"]
        if not isinstance(ids, list) or not 2 <= len(ids) <= 3 or any(i not in bloco_da_relacao for i in ids):
            raise ValueError(f"Combinação {k}: informe 2 ou 3 ids de relações existentes.")
        if len({bloco_da_relacao[i] for i in ids}) < 2:
            raise ValueError(f"Combinação {k}: as relações devem vir de blocos diferentes.")
        if c["tipo"] not in ("encadeamento", "mascaramento"):
            raise ValueError(f"Combinação {k}: tipo deve ser encadeamento ou mascaramento.")
        for campo in ("titulo", "ponte", "cadeia", "cenario", "resposta", "resposta_atraente", "sinal_que_descarta"):
            if not _texto(c[campo]):
                raise ValueError(f"Combinação {k}: {campo} vazio.")
        if palavras(c["resposta"]) > TETO_RESPOSTA:
            raise ValueError(f"Combinação {k}: resposta com mais de {TETO_RESPOSTA} palavras.")
        if not all(_lista_textos(c[x]) for x in ("condicoes_enunciado", "limites")):
            raise ValueError(f"Combinação {k}: condicoes_enunciado e limites devem ser listas de textos.")


def validar_questao(d: dict, tipo: str) -> None:
    if not isinstance(d, dict) or set(d) != {"status", "motivo", "pergunta", "resposta", "desenho"}:
        raise ValueError("Use exatamente as chaves status, motivo, pergunta, resposta e desenho.")
    if d["status"] == "insuficiente":
        if not _texto(d["motivo"]):
            raise ValueError("insuficiente exige motivo.")
        return
    if d["status"] != "ok":
        raise ValueError("status deve ser ok ou insuficiente.")
    if not (_texto(d["pergunta"]) and _texto(d["resposta"])):
        raise ValueError("status ok exige pergunta e resposta.")
    problemas = problemas_forma(d["pergunta"], d["resposta"], TETO_RESPOSTA) \
        + problemas_desenho(d["desenho"], tipo, d["resposta"])
    if problemas:
        raise ValueError("Corrija: " + "; ".join(problemas) + ". Se não for possível no tipo pedido, use insuficiente.")


def validar_resposta(d: dict) -> None:
    if not isinstance(d, dict) or not isinstance(d.get("resposta"), str):
        raise ValueError('Retorne {"resposta": "..."}.')


def validar_juiz(d: dict, ids: list[str], candidatos: list[str]) -> None:
    av = d.get("avaliacoes") if isinstance(d, dict) else None
    if not isinstance(av, list) or [a.get("id") for a in av] != ids:
        raise ValueError("Devolva exatamente um objeto por id recebido, na mesma ordem.")
    for a in av:
        v = a.get("vereditos")
        if not isinstance(v, dict) or set(v) != set(candidatos) or any(x not in VEREDITOS for x in v.values()):
            raise ValueError(f"vereditos deve ter {', '.join(candidatos)}, cada um correta, parcial ou incorreta.")
        if not isinstance(a.get("referencia_valida"), bool) or not isinstance(a.get("atalho_generico"), bool):
            raise ValueError("referencia_valida e atalho_generico devem ser booleanos.")


# ---------------------------------------------------------------- seleção
def cotas_item(n_blocos: int, faceis: int, medias: int, dificeis: int | None, ec_janelas: int) -> dict:
    """As difíceis acompanham o número de janelas EC do item (uma difícil por janela)."""
    d = dificeis if dificeis is not None else len(selecionar_focos(n_blocos, ec_janelas))
    return {"facil": faceis, "media": medias, "dificil_A": math.ceil(d / 2), "dificil_B": d // 2}


def selecionar_alvos(item: str, relacoes: list[dict], combinacoes: list[dict], cota: dict,
                     reserva: float) -> tuple[list, dict]:
    """Rodízio pelos blocos, sem repetir relação; difícil A prefere relações de mecanismo.
    Cada célula recebe a cota mais `reserva` de alvos extras, usados só se faltarem questões."""
    rng = _rng("alvos", item)
    por_bloco = defaultdict(list)
    for r in relacoes:
        por_bloco[r["bloco"]].append(r)
    ordem_blocos = sorted(por_bloco)
    rng.shuffle(ordem_blocos)
    fila = []
    for k in range(max((len(v) for v in por_bloco.values()), default=0)):
        fila += [por_bloco[b][k] for b in ordem_blocos if k < len(por_bloco[b])]
    usadas, alvos, faltas = set(), [], {}

    def total(t):
        return cota.get(t, 0) + math.ceil(cota.get(t, 0) * reserva)

    for nivel in ("dificil_A", "media", "facil"):   # os níveis mais escassos escolhem primeiro
        cand = [r for r in fila if nivel in r["niveis"] and r["id"] not in usadas]
        if nivel == "dificil_A":
            cand.sort(key=lambda r: PREFERENCIA_A.get(r["tipo"], 5))   # sort estável preserva o rodízio
        escolhidas = cand[: total(nivel)]
        usadas |= {r["id"] for r in escolhidas}
        alvos += [{"id": f"{item}:{nivel}:{r['id']}", "item": item, "tipo": nivel, "ordem": k,
                   "reserva": k >= cota.get(nivel, 0), "relacoes": [r]} for k, r in enumerate(escolhidas)]
        if len(escolhidas) < cota.get(nivel, 0):
            faltas[nivel] = cota[nivel] - len(escolhidas)
    combos = list(combinacoes)
    rng.shuffle(combos)
    escolhidos = combos[: total("dificil_B")]
    por_id = {r["id"]: r for r in relacoes}
    alvos += [{"id": f"{item}:dificil_B:{c['id']}", "item": item, "tipo": "dificil_B", "ordem": k,
               "reserva": k >= cota.get("dificil_B", 0), "combinacao": c,
               "relacoes": [por_id[i] for i in c["relacoes"]]} for k, c in enumerate(escolhidos)]
    if len(escolhidos) < cota.get("dificil_B", 0):
        faltas["dificil_B"] = cota["dificil_B"] - len(escolhidos)
    return alvos, faltas


# ---------------------------------------------------------------- execução
class Piloto:
    def __init__(self, saida: Path, *, itens=ITENS, faceis: int = 10, medias: int = 10, dificeis: int | None = None,
                 ec_janelas: int = 36, reserva: float = 1.0, modelos: dict | None = None,
                 respondentes=RESPONDENTES, combinacoes_por_doc: int = 40, reusar: Path | None = None,
                 historico: Path | None = None, workers: int = 6, clientes: dict | None = None,
                 sem_exemplos: bool = False, limpos: Path | None = None, limite_blocos: int | None = None,
                 lote_juiz: int = 8, progress=print):
        self.saida, self.itens = Path(saida), list(itens)
        self.faceis, self.medias, self.dificeis, self.ec_janelas, self.reserva = faceis, medias, dificeis, ec_janelas, reserva
        self.modelos = {**MODELOS, **(modelos or {})}
        self.respondentes = list(respondentes)
        self.candidatos = [f"R{k}" for k in range(1, len(self.respondentes) + 1)]
        self.combinacoes_por_doc, self.workers, self.lote_juiz = combinacoes_por_doc, workers, lote_juiz
        self.reusar, self.historico = _absoluto(reusar), _absoluto(historico)
        self.clientes, self.sem_exemplos, self.limpos, self.progress = dict(clientes or {}), sem_exemplos, limpos, progress
        self.limite_blocos = limite_blocos
        self.lock = threading.Lock()
        self.temas = {i: tema(i) for i in self.itens}
        self.docs, self.n_blocos = {}, {}
        for i in self.itens:
            doc, bs = blocos(i)
            if doc["titulo"] != self.temas[i]["titulo"]:
                raise ValueError(f"{i}: documento não corresponde ao tópico do programa")
            self.n_blocos[i] = len(bs)
            self.docs[i] = bs[:limite_blocos] if limite_blocos else bs
        self.cotas = {i: cotas_item(self.n_blocos[i], faceis, medias, dificeis, ec_janelas) for i in self.itens}

    # -- infraestrutura
    def cliente(self, papel: str):
        with self.lock:
            if papel not in self.clientes:
                from pipeline.inventario.llm import LLMClient, load_dotenv
                load_dotenv(ROOT)
                nome = (self.respondentes[int(papel[1:]) - 1] if re.fullmatch(r"R\d+", papel)
                        else self.modelos[papel])
                model, effort = nome.rsplit(":", 1) if ":" in nome else (nome, "")
                self.clientes[papel] = LLMClient(
                    model, effort, self.saida / ".local" / f"{papel}.sqlite3",
                    self.saida / "chamadas" / f"{papel}.jsonl", provider="azure", max_attempts=3, timeout=600,
                    max_tokens_cap=32000, max_calls=100000, response_dir=self.saida / ".local" / "respostas" / papel)
            return self.clientes[papel]

    def _paralelo(self, tarefas, funcao, rotulo: str) -> int:
        feitos, falhas, inicio = 0, 0, time.time()
        if not tarefas:
            return 0
        with ThreadPoolExecutor(max_workers=max(1, self.workers)) as pool:
            for ok in pool.map(funcao, tarefas):
                feitos += 1
                falhas += 0 if ok else 1
                if feitos % 10 == 0 or feitos == len(tarefas):
                    eta = (time.time() - inicio) / feitos * (len(tarefas) - feitos)
                    self.progress(f"  {rotulo}: {feitos}/{len(tarefas)} | falhas {falhas} | restam ~{eta / 60:.1f} min",
                                  flush=True)
        return falhas

    def _falha(self, pasta: str, nome: str, exc: Exception) -> None:
        atomic_json(self.saida / "falhas" / pasta / f"{nome}.json",
                    {"erro": type(exc).__name__, "mensagem": str(exc)[:2000],
                     "em": datetime.now(timezone.utc).isoformat()})

    def _ok(self, pasta: str, nome: str) -> None:
        f = self.saida / "falhas" / pasta / f"{nome}.json"
        if f.exists():
            f.unlink()

    def config(self) -> None:
        cfg = {"schema": "piloto-dificuldade-v2", "itens": self.itens, "cotas": self.cotas, "reserva": self.reserva,
               "ec_janelas": self.ec_janelas, "modelos": self.modelos, "respondentes": self.respondentes,
               "combinacoes_por_doc": self.combinacoes_por_doc, "sem_exemplos": self.sem_exemplos,
               "limite_blocos": self.limite_blocos,
               "reusar": _relativo(self.reusar), "historico": _relativo(self.historico)}
        path = self.saida / "config.json"
        if path.exists():
            antigo = {k: v for k, v in read_json(path).items() if k != "criado_em"}
            if antigo != cfg:
                diff = sorted(k for k in set(antigo) | set(cfg) if antigo.get(k) != cfg.get(k))
                raise ValueError(f"Configuração diferente da pasta existente ({', '.join(diff)}); use outra --saida")
            return
        atomic_json(path, {**cfg, "criado_em": datetime.now(timezone.utc).isoformat()})

    # -- 1. relações
    def relacoes(self) -> int:
        if self.reusar:
            for i in self.itens:
                origem, destino = self.reusar / "relacoes" / i, self.saida / "relacoes" / i
                if origem.exists() and not destino.exists():
                    destino.mkdir(parents=True)
                    for p in sorted(origem.glob("*.json")):
                        if int(p.stem) < len(self.docs[i]):
                            shutil.copy2(p, destino / p.name)
        system = prompt("relacoes")
        tarefas = [(i, b) for i in self.itens for b in self.docs[i]
                   if not (self.saida / "relacoes" / i / f"{b['indice']:03d}.json").exists()]
        self.progress(f"1. relações: {len(tarefas)} blocos a processar", flush=True)

        def um(t):
            item, b = t
            t_ = self.temas[item]
            user = (f"<tema>\nÁrea: {t_['area']}\nTema: {t_['tema']}\n</tema>\n\n<documento>{t_['titulo']}</documento>\n\n"
                    f"<bloco>\n{b['titulo_capitulo']} / {b['subtitulo']}\n{b['texto']}\n</bloco>")
            try:
                d = self.cliente("relacoes").json(system, user, tag="inv_relacoes", max_tokens=8000, item=item,
                                                  validate=lambda d: validar_relacoes(d, b["texto"]))
            except Exception as exc:  # noqa: BLE001
                self._falha("relacoes", f"{item}_{b['indice']:03d}", exc)
                return False
            rels = [{**r, "id": f"B{b['indice']:03d}.R{k}", "bloco": b["indice"]} for k, r in enumerate(d["relacoes"], 1)]
            atomic_json(self.saida / "relacoes" / item / f"{b['indice']:03d}.json",
                        {"item": item, "bloco": b["indice"], "subtitulo": b["subtitulo"], "status": d["status"],
                         "motivo": d["motivo"], "relacoes": rels})
            self._ok("relacoes", f"{item}_{b['indice']:03d}")
            return True

        return self._paralelo(tarefas, um, "relações")

    def todas_relacoes(self, item: str) -> list[dict]:
        return [r for p in sorted((self.saida / "relacoes" / item).glob("*.json")) for r in read_json(p)["relacoes"]]

    # -- 2. encadeamentos
    def combinacoes(self) -> int:
        falhas = 0
        for item in self.itens:
            destino = self.saida / "combinacoes" / f"{item}.json"
            if destino.exists():
                continue
            if len(list((self.saida / "relacoes" / item).glob("*.json"))) < len(self.docs[item]):
                self.progress(f"2. encadeamentos {item}: relações incompletas; rode de novo para concluir", flush=True)
                falhas += 1
                continue
            rels = self.todas_relacoes(item)
            subt = {b["indice"]: b["subtitulo"] for b in self.docs[item]}
            linhas = [f"{r['id']} | bloco {r['bloco']:03d} ({subt[r['bloco']]}) | {r['tipo']} | {r['afirmacao']} | "
                      f"condições: {'; '.join(r['condicoes']) or '-'} | limites: {'; '.join(r['limites']) or '-'}"
                      for r in rels]
            t_ = self.temas[item]
            user = (f"<tema>\nÁrea: {t_['area']}\nTema: {t_['tema']}\n</tema>\n\n<documento>{t_['titulo']}</documento>\n\n"
                    "<relacoes>\n" + "\n".join(linhas) + "\n</relacoes>")
            bloco_da = {r["id"]: r["bloco"] for r in rels}
            self.progress(f"2. encadeamentos {item}: {len(rels)} relações", flush=True)
            try:
                d = self.cliente("combinacoes").json(
                    prompt("combinacoes", QUANTIDADE=self.combinacoes_por_doc), user, tag="inv_combinacoes",
                    max_tokens=32000, item=item,
                    validate=lambda d: validar_combinacoes(d, bloco_da, self.combinacoes_por_doc))
            except Exception as exc:  # noqa: BLE001
                self._falha("combinacoes", item, exc)
                falhas += 1
                continue
            atomic_json(destino, {"item": item, "observacao": d["observacao"],
                                  "combinacoes": [{**c, "id": f"C{k}"} for k, c in enumerate(d["combinacoes"], 1)]})
            self._ok("combinacoes", item)
        return falhas

    # -- 3. alvos
    def alvos(self) -> list[dict]:
        destino = self.saida / "alvos.json"
        if destino.exists():
            return read_json(destino)["alvos"]
        alvos, faltas = [], {}
        for item in self.itens:
            combos = read_json(self.saida / "combinacoes" / f"{item}.json")["combinacoes"]
            a, f = selecionar_alvos(item, self.todas_relacoes(item), combos, self.cotas[item], self.reserva)
            alvos += a
            faltas.update({f"{item}:{k}": v for k, v in f.items()})
        atomic_json(destino, {"cotas": self.cotas, "reserva": self.reserva, "faltas_no_inventario": faltas,
                              "alvos": alvos})
        if faltas:
            self.progress(f"3. alvos: o inventário não sustentou a cota em {faltas}", flush=True)
        return alvos

    # -- 4. questões
    def _exemplos(self, alvo) -> str:
        if self.sem_exemplos:
            return ""
        from pipeline.qa_research.piloto_janela import exemplos as ex
        with self.lock:
            if not hasattr(self, "_pools"):
                self._pools = ex.carregar_limpos(self.limpos)[0]
                self._banco = ex.carregar_especialista()
        k = int(hashlib.sha256(alvo["id"].encode()).hexdigest()[:8], 16) % 100000
        return ex.render(ex.exemplos_da_janela("EC", alvo["item"], k, self._pools, self._banco))

    def _arquivo_questao(self, alvo) -> Path:
        return self.saida / "questoes" / f"{_nome(alvo['id'])}.json"

    def _gerar_questao(self, alvo) -> bool:
        bs = {b["indice"]: b for b in self.docs[alvo["item"]]}
        usados = sorted({r["bloco"] for r in alvo["relacoes"]})
        blocos_txt = "\n\n".join(f"[bloco {i:03d}] {bs[i]['titulo_capitulo']} / {bs[i]['subtitulo']}\n{bs[i]['texto']}"
                                 for i in usados)
        conteudo = {"tipo": alvo["tipo"]}
        if alvo["tipo"] == "dificil_B":
            c = alvo["combinacao"]
            conteudo["encadeamento"] = {k: c[k] for k in CAMPOS_COMB if k != "relacoes"}
            conteudo["relacoes"] = [{k: r[k] for k in ("id", "afirmacao", "condicoes", "limites")} for r in alvo["relacoes"]]
        else:
            r = alvo["relacoes"][0]
            conteudo["relacao"] = {k: r[k] for k in ("id", "afirmacao", "condicoes", "limites")}
            if alvo["tipo"] == "dificil_A":
                conteudo["relacao"] |= {"explicacao_concorrente (resposta atraente)": r["explicacao_concorrente"],
                                        "condicao_que_distingue": r["condicao_que_distingue"]}
        t_ = self.temas[alvo["item"]]
        user = "\n\n".join(x for x in (
            f"<tema>\nÁrea: {t_['area']}\nTema: {t_['tema']}\n</tema>",
            f"<alvo>\n{json.dumps(conteudo, ensure_ascii=False, indent=2)}\n</alvo>",
            self._exemplos(alvo),
            f"<blocos>\n{blocos_txt}\n</blocos>") if x)
        try:
            d = self.cliente("questao").json(prompt("questao"), user, tag="inv_questao", max_tokens=12000,
                                             item=alvo["item"], validate=lambda d: validar_questao(d, alvo["tipo"]))
        except Exception as exc:  # noqa: BLE001
            self._falha("questoes", _nome(alvo["id"]), exc)
            return False
        atomic_json(self._arquivo_questao(alvo),
                    {"id": f"inv:{alvo['id']}", "metodo": "inventario", "item": alvo["item"], "tipo": alvo["tipo"],
                     "nivel": nivel_agregado(alvo["tipo"]), "ordem": alvo["ordem"], "reserva": alvo["reserva"],
                     "status": d["status"], "motivo": d["motivo"], "pergunta": d["pergunta"], "resposta": d["resposta"],
                     "desenho": d["desenho"], "relacoes": [r["id"] for r in alvo["relacoes"]],
                     "combinacao": alvo.get("combinacao", {}).get("id")})
        self._ok("questoes", _nome(alvo["id"]))
        return True

    def _celulas(self, alvos) -> dict:
        cel = defaultdict(list)
        for a in sorted(alvos, key=lambda a: a["ordem"]):
            cel[(a["item"], a["tipo"])].append(a)
        return cel

    def questoes(self) -> int:
        """Gera a cota de cada célula; reservas entram, em ordem, só para cobrir insuficientes."""
        cel, tentadas, falhas = self._celulas(self.alvos()), set(), 0
        rodada = 0
        while True:
            lote = []
            for (item, tipo), lista in cel.items():
                feitas = [a for a in lista if self._arquivo_questao(a).exists()]
                ok = sum(read_json(self._arquivo_questao(a))["status"] == "ok" for a in feitas)
                falta = self.cotas[item][tipo] - ok
                livres = [a for a in lista if not self._arquivo_questao(a).exists() and a["id"] not in tentadas]
                lote += livres[: max(0, falta)]
            if not lote:
                break
            rodada += 1
            tentadas |= {a["id"] for a in lote}
            self.progress(f"4. questões, rodada {rodada}: {len(lote)} alvos", flush=True)
            falhas += self._paralelo(lote, self._gerar_questao, "questões")
        return falhas

    def selecionadas(self) -> tuple[list[dict], dict]:
        out, faltas = [], {}
        for (item, tipo), lista in self._celulas(self.alvos()).items():
            ok = [read_json(self._arquivo_questao(a)) for a in lista if self._arquivo_questao(a).exists()]
            ok = [q for q in ok if q["status"] == "ok"][: self.cotas[item][tipo]]
            out += ok
            if len(ok) < self.cotas[item][tipo]:
                faltas[f"{item}:{tipo}"] = self.cotas[item][tipo] - len(ok)
        return out, faltas

    # -- 5. EC v13
    def ec(self) -> int:
        from pipeline.qa_research.piloto_janela.core import COMPOSICAO_PADRAO, PROMPT_DIFICULDADE
        from pipeline.qa_research.piloto_janela.core import Piloto as PilotoJanela
        self.progress(f"5. EC v13: janelas de {', '.join(self.itens)} (até {self.ec_janelas} por documento)", flush=True)
        pj = PilotoJanela(self.saida / "ec", self.itens, self.modelos["questao"], minimo=4, maximo=4,
                          max_tokens=16000, workers=self.workers, condicao="EC", janelas_por_item=self.ec_janelas,
                          composicao=COMPOSICAO_PADRAO, prompt=PROMPT_DIFICULDADE, client=self.clientes.get("ec"),
                          limpos=self.limpos, progress=self.progress)
        pj.run()
        return len(list((self.saida / "ec").glob("*/falhas/*.json")))

    def amostra_ec(self) -> tuple[list[dict], dict]:
        """Determinística (semente fixa): refeita a cada chamada, para incluir janelas concluídas depois."""
        destino = self.saida / "amostra_ec.json"
        arq = self.saida / "ec" / "questoes.jsonl"
        linhas = [json.loads(l) for l in arq.read_text(encoding="utf-8").splitlines() if l.strip()] if arq.exists() else []
        linhas = [q for q in linhas if q["verificacoes"]["fundamentos_literais"] and q["verificacoes"]["ancora_em_F"]]
        rng = random.Random(20261023)
        out, faltas = [], {}
        for item in self.itens:
            c = self.cotas[item]
            alvo = {"facil": c["facil"], "media": c["media"], "dificil": c["dificil_A"] + c["dificil_B"]}
            for nivel, n in alvo.items():
                pool = sorted((q for q in linhas if q["item"] == item and q["dificuldade"] == nivel), key=lambda q: q["uid"])
                escolha = rng.sample(pool, min(n, len(pool)))
                if len(escolha) < n:
                    faltas[f"{item}:{nivel}"] = n - len(escolha)
                out += [{"id": f"ec:{q['uid']}", "metodo": "ec", "item": item, "tipo": nivel, "nivel": nivel,
                         "pergunta": q["pergunta"], "resposta": q["resposta"], "desenho": q.get("desenho"),
                         "origem": q["uid"]} for q in escolha]
        atomic_json(destino, {"origem": arq.as_posix(), "faltas": faltas, "questoes": out})
        return out, faltas

    def banco_avaliado(self) -> list[dict]:
        return self.selecionadas()[0] + self.amostra_ec()[0]

    # -- 6. avaliação cega
    def _arq_resposta(self, cand: str, q) -> Path:
        return self.saida / "avaliacao" / "respostas" / cand / f"{_nome(q['id'])}.json"

    def avaliar(self) -> int:
        banco = self.banco_avaliado()
        sys_r, sys_j = prompt("respondente"), prompt("juiz")
        falhas = 0
        for cand, modelo in zip(self.candidatos, self.respondentes):
            pend = [q for q in banco if not self._arq_resposta(cand, q).exists()]
            self.progress(f"6a. respondente {cand} ({modelo}): {len(pend)} perguntas", flush=True)

            def responder(q, cand=cand):
                try:
                    d = self.cliente(cand).json(sys_r, q["pergunta"], tag=f"inv_respondente_{cand}", max_tokens=4000,
                                                item=q["item"], validate=validar_resposta)
                except Exception as exc:  # noqa: BLE001
                    self._falha(f"respostas_{cand}", _nome(q["id"]), exc)
                    return False
                atomic_json(self._arq_resposta(cand, q), {"id": q["id"], "resposta_candidato": d["resposta"]})
                self._ok(f"respostas_{cand}", _nome(q["id"]))
                return True

            falhas += self._paralelo(pend, responder, f"respostas {cand}")
        prontas = [q for q in banco if all(self._arq_resposta(c, q).exists() for c in self.candidatos)]
        ordem = sorted(prontas, key=lambda q: hashlib.sha256(("juiz" + q["id"]).encode()).hexdigest())
        julgados = {a["id"] for p in (self.saida / "avaliacao" / "juiz").glob("*.json") for a in read_json(p)["avaliacoes"]}
        ordem = [q for q in ordem if q["id"] not in julgados]
        lotes = [ordem[i:i + self.lote_juiz] for i in range(0, len(ordem), self.lote_juiz)]
        self.progress(f"6b. juiz ({self.modelos['juiz']}): {len(lotes)} lotes", flush=True)

        def julgar(lote):
            ids = [f"Q{k}" for k in range(1, len(lote) + 1)]   # o juiz não vê método, nível nem modelo
            itens = [{"id": i, "pergunta": q["pergunta"], "resposta_referencia": q["resposta"],
                      "respostas_candidatos": {c: read_json(self._arq_resposta(c, q))["resposta_candidato"]
                                               for c in self.candidatos}}
                     for i, q in zip(ids, lote)]
            nome = hashlib.sha256("|".join(q["id"] for q in lote).encode()).hexdigest()[:16]
            try:
                d = self.cliente("juiz").json(sys_j, json.dumps(itens, ensure_ascii=False), tag="inv_juiz",
                                              max_tokens=12000, validate=lambda d: validar_juiz(d, ids, self.candidatos))
            except Exception as exc:  # noqa: BLE001
                self._falha("juiz", nome, exc)
                return False
            atomic_json(self.saida / "avaliacao" / "juiz" / f"{nome}.json",
                        {"avaliacoes": [{**a, "id": q["id"]} for a, q in zip(d["avaliacoes"], lote)]})
            self._ok("juiz", nome)
            return True

        return falhas + self._paralelo(lotes, julgar, "juiz")

    # -- 7. relatório
    def relatorio(self) -> dict:
        banco = {q["id"]: q for q in self.banco_avaliado()}
        juiz = {a["id"]: a for p in (self.saida / "avaliacao" / "juiz").glob("*.json") for a in read_json(p)["avaliacoes"]}
        linhas = []
        for i, q in banco.items():
            l = dict(q)
            for c in self.candidatos:
                arq = self._arq_resposta(c, q)
                l[f"resposta_{c}"] = read_json(arq)["resposta_candidato"] if arq.exists() else ""
            if i in juiz:
                l.update({f"veredito_{c}": juiz[i]["vereditos"][c] for c in self.candidatos})
                l.update({k: juiz[i][k] for k in ("referencia_valida", "atalho_generico", "justificativa")})
            l["problemas_forma"] = problemas_forma(q["pergunta"], q["resposta"], TETO_RESPOSTA)
            linhas.append(l)
        avaliadas = [l for l in linhas if "referencia_valida" in l]

        def bloco(ls):
            n = len(ls)
            if not n:
                return {"n": 0}
            b = {"n": n,
                 "atalho_generico": sum(l["atalho_generico"] for l in ls),
                 "referencia_invalida": sum(not l["referencia_valida"] for l in ls),
                 "problemas_forma": sum(bool(l["problemas_forma"]) for l in ls),
                 "palavras_pergunta": round(sum(palavras(l["pergunta"]) for l in ls) / n, 1),
                 "palavras_resposta": round(sum(palavras(l["resposta"]) for l in ls) / n, 1)}
            for c in self.candidatos:
                v = [l[f"veredito_{c}"] for l in ls]
                b[c] = {"acuracia": round(sum(VEREDITOS[x] for x in v) / n, 3),
                        "estrita": round(sum(x == "correta" for x in v) / n, 3),
                        "corretas": v.count("correta"), "parciais": v.count("parcial"), "incorretas": v.count("incorreta")}
                validas = [l for l in ls if l["referencia_valida"] and not l["atalho_generico"]]
                b[c]["acuracia_limpa"] = (round(sum(VEREDITOS[l[f"veredito_{c}"]] for l in validas) / len(validas), 3)
                                          if validas else None)
            if len(self.candidatos) > 1:
                # Filtro adversarial simulado: questões que o último respondente errou.
                ult, pri = self.candidatos[-1], self.candidatos[0]
                filtradas = [l for l in ls if l[f"veredito_{ult}"] == "incorreta"]
                b["filtro"] = {"n": len(filtradas), "base": ult, "avaliado": pri,
                               "acuracia": round(sum(VEREDITOS[l[f"veredito_{pri}"]] for l in filtradas) / len(filtradas), 3)
                               if filtradas else None}
            return b

        res = {"modelos": self.modelos, "respondentes": dict(zip(self.candidatos, self.respondentes)), "metodos": {}}
        for m in ("inventario", "ec"):
            lm = [l for l in avaliadas if l["metodo"] == m]
            res["metodos"][m] = {"total": bloco(lm), "por_nivel": {n: bloco([l for l in lm if l["nivel"] == n])
                                                                   for n in NIVEIS}}
            if m == "inventario":
                res["metodos"][m]["por_tipo"] = {t: bloco([l for l in lm if l["tipo"] == t]) for t in ("dificil_A", "dificil_B")}
        geradas = [read_json(p) for p in (self.saida / "questoes").glob("*.json")]
        alvos = read_json(self.saida / "alvos.json") if (self.saida / "alvos.json").exists() else {}
        res["inventario_geracao"] = {
            "geradas": len(geradas), "ok": sum(q["status"] == "ok" for q in geradas),
            "insuficiente": sum(q["status"] == "insuficiente" for q in geradas),
            "insuficiente_por_tipo": {t: sum(q["status"] == "insuficiente" and q["tipo"] == t for q in geradas) for t in TIPOS},
            "faltas_no_inventario": alvos.get("faltas_no_inventario", {}),
            "faltas_finais": self.selecionadas()[1] if alvos else {}}
        res["ec_geracao"] = {"faltas_amostra": self.amostra_ec()[1],
                             "falhas_janelas": len(list((self.saida / "ec").glob("*/falhas/*.json")))}
        res["relacoes"] = {i: len(self.todas_relacoes(i)) for i in self.itens}
        res["combinacoes"] = {i: len(read_json(self.saida / "combinacoes" / f"{i}.json")["combinacoes"])
                              for i in self.itens if (self.saida / "combinacoes" / f"{i}.json").exists()}
        res["falhas_pendentes"] = sorted(p.relative_to(self.saida).as_posix() for p in (self.saida / "falhas").rglob("*.json"))
        if self.historico and (self.historico / "resultado.json").exists():
            h = read_json(self.historico / "resultado.json")["metodos"]
            res["historico_v1"] = {m: {n: h[m]["por_nivel"][n].get("acuracia") for n in NIVEIS} for m in h}
        atomic_json(self.saida / "resultado.json", res)

        campos = (["id", "metodo", "item", "tipo", "nivel", "pergunta", "resposta"]
                  + [f"resposta_{c}" for c in self.candidatos] + [f"veredito_{c}" for c in self.candidatos]
                  + ["referencia_valida", "atalho_generico", "justificativa"]
                  + [f"desenho_{k}" for k in CAMPOS_DESENHO])
        with (self.saida / "questoes_avaliadas.csv").open("w", encoding="utf-8-sig", newline="") as f:
            w = csv.DictWriter(f, fieldnames=campos, extrasaction="ignore")
            w.writeheader()
            for l in sorted(linhas, key=lambda l: (l["metodo"], l["nivel"], l["id"])):
                des = l.get("desenho") or {}
                w.writerow({**{k: l.get(k, "") for k in campos}, **{f"desenho_{k}": des.get(k, "") for k in CAMPOS_DESENHO}})
        self._markdown(res, avaliadas)
        return res

    def _markdown(self, res: dict, avaliadas: list[dict]) -> None:
        cands = self.candidatos

        def cel(b, c):
            if not b or not b.get("n"):
                return "–"
            x = b[c]
            return f"{x['acuracia']:.2f} ({x['estrita']:.2f})"

        def extra(b):
            if not b or not b.get("n"):
                return "–"
            f = b.get("filtro") or {}
            filtro = f"{f['acuracia']:.2f} (n={f['n']})" if f.get("acuracia") is not None else "–"
            return f"{b['n']} | {b['atalho_generico']} | {b['referencia_invalida']} | {filtro}"

        inv, ec = res["metodos"]["inventario"], res["metodos"]["ec"]
        rot = " | ".join(f"{c} {res['respondentes'][c]}" for c in cands)
        l = ["# Piloto de dificuldade v2: inventário x EC v13", "",
             f"Rubrica: `pipeline/qa_research/DIFICULDADE_V2.md`. Respondentes sem contexto: {rot}. "
             f"Juiz: `{res['modelos']['juiz']}`.", "",
             "Acurácia com correta = 1 e parcial = 0,5; entre parênteses, só as corretas. Se a dificuldade for real, "
             "a acurácia cai de fácil para difícil.", "",
             "| Método | Nível | " + " | ".join(cands) + " | n | atalho genérico | ref. inválida | filtro simulado |",
             "|---|---|" + "---|" * len(cands) + "---|---|---|---|"]
        for nome, m in (("inventário", inv), ("EC v13", ec)):
            linhas = [(n, m["por_nivel"][n]) for n in NIVEIS]
            if "por_tipo" in m:
                linhas += [(f"↳ {t}", m["por_tipo"][t]) for t in ("dificil_A", "dificil_B")]
            linhas.append(("**total**", m["total"]))
            for n, b in linhas:
                l.append(f"| {nome} | {n} | " + " | ".join(cel(b, c) for c in cands) + f" | {extra(b)} |")
        l += ["", "Filtro simulado: acurácia de R1 nas questões que o último respondente errou (ideia de filtro "
              "adversarial, como em Humanity's Last Exam).", ""]
        if "historico_v1" in res:
            h = res["historico_v1"]
            l += ["Histórico v1 (R1 = gpt-4-1-nano): " + "; ".join(
                f"{m} " + ", ".join(f"{n} {v:.2f}" for n, v in d.items() if v is not None) for m, d in h.items()) + ".", ""]
        l += ["Acurácia limpa de R1 (sem referências inválidas e sem atalho genérico): " + "; ".join(
            f"{nm} {n}: {m['por_nivel'][n].get('R1', {}).get('acuracia_limpa')}" for nm, m in (("inv", inv), ("ec", ec))
            for n in NIVEIS) + ".", "",
              f"Inventário: relações {res['relacoes']}, encadeamentos {res['combinacoes']}, "
              f"geração {res['inventario_geracao']}.", f"EC: {res['ec_geracao']}.",
              f"Falhas pendentes: {len(res['falhas_pendentes'])}.", "", "## Questões avaliadas", ""]
        for a in sorted(avaliadas, key=lambda a: (a["metodo"], a["nivel"], a["id"])):
            vs = " · ".join(f"{c} {a[f'veredito_{c}']}" for c in cands)
            marcas = ("" if a["referencia_valida"] else " · ref. inválida") + (" · atalho" if a["atalho_generico"] else "")
            l += [f"**{a['metodo']} · {a['tipo']} · {vs}{marcas}** {a['pergunta']}", "", f"- Referência: {a['resposta']}"]
            l += [f"- {c}: {a[f'resposta_{c}']}" for c in cands]
            des = a.get("desenho") or {}
            if des.get("resposta_atraente"):
                l.append(f"- Desenho: atraente = {des['resposta_atraente']} | descarta = {des['sinal_que_descarta']} | "
                         f"passo oculto = {des['passo_oculto']}")
            l += [f"- Juiz: {a.get('justificativa', '')}", ""]
        (self.saida / "RELATORIO.md").write_text("\n".join(l), encoding="utf-8")

    def run(self, etapas=("relacoes", "combinacoes", "questoes", "ec", "avaliar", "relatorio")) -> int:
        self.config()
        falhas = 0
        if "relacoes" in etapas:
            falhas += self.relacoes()
        if "combinacoes" in etapas:
            falhas += self.combinacoes()
        if "questoes" in etapas:
            if all((self.saida / "combinacoes" / f"{i}.json").exists() for i in self.itens):
                falhas += self.questoes()
            else:
                self.progress("4. questões: aguardando relações e encadeamentos completos", flush=True)
                falhas += 1
        if "ec" in etapas:
            falhas += self.ec()
        if "avaliar" in etapas:
            if (self.saida / "alvos.json").exists():
                falhas += self.avaliar()
            else:
                falhas += 1
        if "relatorio" in etapas and (self.saida / "alvos.json").exists():
            self.relatorio()
        return falhas

