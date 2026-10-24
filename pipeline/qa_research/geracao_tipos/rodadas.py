"""Geração por meta (v17): gera e audita em rodadas até cada tópico ter N questões aprovadas.

Por tópico (documento):
  1. inventário: relações por bloco e encadeamentos (reaproveitados de uma rodada anterior, quando houver);
  2. compostas: uma questão por encadeamento (qualquer tipo menos conceito; é onde a decisão é gerada);
  3. rodadas de janela (prompt v16): a 1ª passa por todas as janelas; as seguintes voltam às janelas mais
     produtivas, com as questões já geradas ali em <questoes_existentes>, até atingir a meta;
  4. auditoria depois de cada etapa: só entram as questões com referência válida, sem atalho e sem quase
     duplicata no tópico.

Banco dinâmico: as aprovadas viram exemplos e as reprovadas viram contraexemplos (com a justificativa do
auditor como problema) para as chamadas seguintes de outros tópicos. No fim, `exemplos_proposto.json`
sugere a atualização do banco curado.
"""
from __future__ import annotations

import hashlib
import json
import math
import shutil
import threading
import time
from collections import Counter, defaultdict
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime, timezone
from pathlib import Path

from pipeline.qa_research.inventario_docs import core as inv
from pipeline.qa_research.piloto_janela.core import (QA, ROOT, atomic_json, blocos, carregar_prompt, janela,
                                                     palavras, preencher, read_json, sha, tema, verificar)
from pipeline.qa_research.piloto_janela.core import _tokens
from pipeline.qa_research.tipos import GRUPOS_V16, MAXIMO_V15, TIPOS, problemas_composicao, problemas_tipo

from .core import (CAMPOS, EXEMPLOS, ROTULOS, _texto, carregar_banco, prompt, validar_composta, validar_lote)

PROMPT_JANELA = QA / "prompt_janela_qa_17.md"
TIPOS_JANELA = tuple(t for ts in GRUPOS_V16.values() for t in ts)
# Inventários já extraídos (relações e encadeamentos), na ordem de preferência.
REUSAR = (QA / "relatorios" / "geracao_meta_20261024T000315Z", QA / "relatorios" / "piloto_dificuldade_20261023T053615Z")
# Banco dinâmico herdado: aprovadas e reprovadas de rodadas anteriores continuam valendo como exemplos.
BANCO_INICIAL = (QA / "relatorios" / "geracao_meta_20261024T000315Z" / "banco_dinamico.json",)
MODELOS = {"relacoes": "gpt-5-4-petrobras:low", "combinacoes": "gpt-5-4-petrobras:high",
           "geracao": "gpt-5-4-petrobras:high", "auditoria": "gpt-5-4-petrobras:high"}
LIMIAR_DUPLICATA = 0.6
LIMIAR_RESPOSTA_CURTA = 0.8   # respostas de até 6 termos com a mesma entidade contam como o mesmo conhecimento
CONTRA_FIXOS = 5        # contraexemplos do banco curado em cada chamada
CONTRA_DINAMICOS = 3    # reprovações recentes de outros tópicos


def validar_janela_v16(d: dict) -> None:
    if not isinstance(d, dict) or set(d) != {"status", "motivo", "questoes"}:
        raise ValueError("Use exatamente as chaves status, motivo e questoes.")
    if d["status"] not in ("ok", "parcial", "sem_questoes") or not isinstance(d["questoes"], list) \
            or not isinstance(d["motivo"], str):
        raise ValueError("status deve ser ok, parcial ou sem_questoes; motivo, texto; questoes, lista.")
    problemas = []
    for k, q in enumerate(d["questoes"], 1):
        if not isinstance(q, dict) or set(q) != set(CAMPOS):
            raise ValueError(f"Questão {k}: use exatamente os campos {', '.join(CAMPOS)}.")
        if q["id"] != k:
            raise ValueError(f"Questão {k}: id deve ser {k}.")
        for campo in ("conhecimento", "pergunta", "resposta"):
            if not _texto(q[campo]):
                raise ValueError(f"Questão {k}: {campo} vazio.")
        fs = q["fundamentos"]
        if not isinstance(fs, list) or not fs or any(
                not isinstance(f, dict) or set(f) != {"bloco", "trecho"} or f["bloco"] not in ROTULOS
                or not _texto(f["trecho"]) for f in fs):
            raise ValueError(f'Questão {k}: fundamentos deve ser lista de {{"bloco": A1|F|A2, "trecho": texto}}.')
        problemas += [f"Questão {k} ({q['tipo']}): {m}." for m in
                      problemas_tipo(q["tipo"], q["cenario"], q["pergunta"], q["resposta"])]
    problemas += [m[0].upper() + m[1:] + "." for m in problemas_composicao(
        d["status"], [q["tipo"] for q in d["questoes"]], d["motivo"], maximo=MAXIMO_V15, grupos=GRUPOS_V16)]
    if problemas:
        raise ValueError(" ".join(problemas) + " Corrija ou descarte a questão (use parcial e explique em motivo).")


def _filtrado(exc: Exception) -> bool:
    """Bloqueio do filtro de conteúdo do Azure: tentar de novo não adianta."""
    return type(exc).__name__ == "ContentFiltered"


def _resposta_curta(resposta: str) -> frozenset:
    t = _tokens(resposta.split(";")[0].split(",")[0])
    return frozenset(t) if 0 < len(t) <= 6 else frozenset()


def _h(*partes) -> int:
    return int(hashlib.sha256("|".join(map(str, partes)).encode()).hexdigest()[:12], 16)


class GeracaoMeta:
    def __init__(self, saida: Path, itens: list[str], *, meta: int = 100, max_rodadas: int = 4,
                 max_passagens: int = 3, modelos: dict | None = None, reusar=REUSAR, banco_inicial=BANCO_INICIAL,
                 exemplos: Path = EXEMPLOS, combinacoes_por_doc: int = 25, workers: int = 8, lote: int = 10,
                 clientes: dict | None = None, progress=print):
        self.saida, self.itens, self.meta = Path(saida), list(itens), meta
        self.max_rodadas, self.max_passagens = max_rodadas, max_passagens
        self.modelos = {**MODELOS, **(modelos or {})}
        self.reusar = [Path(r) for r in ((reusar,) if isinstance(reusar, (str, Path)) else (reusar or ()))]
        self.banco_inicial = {"aprovadas": [], "reprovadas": []}
        for arq in ((banco_inicial,) if isinstance(banco_inicial, (str, Path)) else (banco_inicial or ())):
            if Path(arq).exists():
                d = read_json(arq)
                self.banco_inicial["aprovadas"] += d["aprovadas"]
                self.banco_inicial["reprovadas"] += d["reprovadas"]
        self.n_banco_inicial = {k: len(v) for k, v in self.banco_inicial.items()}
        self.caminho_exemplos, self.base = Path(exemplos), carregar_banco(exemplos)
        self.combinacoes_por_doc, self.workers, self.lote = combinacoes_por_doc, workers, lote
        self.clientes, self.progress = dict(clientes or {}), progress
        self.lock = threading.Lock()
        self.temas = {i: tema(i) for i in self.itens}
        self.docs = {i: blocos(i)[1] for i in self.itens}

    # ---------------------------------------------------------------- infraestrutura
    def cliente(self, papel: str):
        with self.lock:
            if papel not in self.clientes:
                from pipeline.inventario.llm import LLMClient, load_dotenv
                load_dotenv(ROOT)
                model, effort = (self.modelos[papel].rsplit(":", 1) if ":" in self.modelos[papel]
                                 else (self.modelos[papel], ""))
                self.clientes[papel] = LLMClient(
                    model, effort, self.saida / ".local" / f"{papel}.sqlite3", self.saida / "chamadas" / f"{papel}.jsonl",
                    provider="azure", max_attempts=3, timeout=600, max_tokens_cap=32000, max_calls=200000,
                    response_dir=self.saida / ".local" / "respostas" / papel)
            return self.clientes[papel]

    def _paralelo(self, tarefas, funcao, rotulo: str) -> int:
        if not tarefas:
            return 0
        feitos, falhas, inicio = 0, 0, time.time()
        with ThreadPoolExecutor(max_workers=max(1, self.workers)) as pool:
            for ok in pool.map(funcao, tarefas):
                feitos += 1
                falhas += 0 if ok else 1
                if feitos % 20 == 0 or feitos == len(tarefas):
                    eta = (time.time() - inicio) / feitos * (len(tarefas) - feitos)
                    self.progress(f"  {rotulo}: {feitos}/{len(tarefas)} | falhas {falhas} | restam ~{eta / 60:.1f} min",
                                  flush=True)
        return falhas

    def _falha(self, nome: str, exc: Exception) -> None:
        atomic_json(self.saida / "falhas" / f"{nome}.json",
                    {"erro": type(exc).__name__, "mensagem": str(exc)[:2000], "em": datetime.now(timezone.utc).isoformat()})

    def _ok(self, nome: str) -> None:
        f = self.saida / "falhas" / f"{nome}.json"
        if f.exists():
            f.unlink()

    def config(self) -> None:
        cfg = {"schema": "geracao-meta-v17", "meta": self.meta, "max_rodadas": self.max_rodadas,
               "max_passagens": self.max_passagens, "modelos": self.modelos,
               "prompt_janela_sha256": sha(PROMPT_JANELA.read_text(encoding="utf-8")),
               "prompt_composta_sha256": sha(prompt("composta")),
               "exemplos_sha256": sha(self.caminho_exemplos.read_text(encoding="utf-8")),
               "combinacoes_por_doc": self.combinacoes_por_doc, "banco_inicial": self.n_banco_inicial}
        path = self.saida / "config.json"
        if path.exists():
            antigo = read_json(path)
            fixos = {k: v for k, v in antigo.items() if k not in ("itens", "criado_em")}
            if fixos != cfg:
                diff = sorted(k for k in set(fixos) | set(cfg) if fixos.get(k) != cfg.get(k))
                raise ValueError(f"Configuração diferente da pasta existente ({', '.join(diff)}); use outra --saida")
            cfg["itens"] = sorted(set(antigo["itens"]) | set(self.itens))
            cfg["criado_em"] = antigo["criado_em"]
        else:
            cfg["itens"], cfg["criado_em"] = sorted(self.itens), datetime.now(timezone.utc).isoformat()
        atomic_json(path, cfg)

    # ---------------------------------------------------------------- 1. inventário
    def _dir(self, item: str) -> Path:
        return self.saida / "topicos" / item

    def inventario(self) -> int:
        for item in self.itens:   # reaproveita relações e encadeamentos já extraídos (dois formatos de pasta)
            d = self._dir(item)
            for r in self.reusar:
                if (d / "combinacoes.json").exists():
                    break
                for rel, comb in ((r / "topicos" / item / "relacoes", r / "topicos" / item / "combinacoes.json"),
                                  (r / "relacoes" / item, r / "combinacoes" / f"{item}.json")):
                    if comb.exists():
                        (d / "relacoes").mkdir(parents=True, exist_ok=True)
                        for p in rel.glob("*.json"):
                            shutil.copy2(p, d / "relacoes" / p.name)
                        shutil.copy2(comb, d / "combinacoes.json")
                        break
            # relações já extraídas sem encadeamento (ex.: encadeamento truncado) também são aproveitadas
            for r in self.reusar:
                origem = r / "topicos" / item / "relacoes"
                if not (d / "combinacoes.json").exists() and origem.exists():
                    (d / "relacoes").mkdir(parents=True, exist_ok=True)
                    for p in origem.glob("*.json"):
                        if not (d / "relacoes" / p.name).exists():
                            shutil.copy2(p, d / "relacoes" / p.name)
        system = inv.prompt("relacoes")
        tarefas = [(i, b) for i in self.itens for b in self.docs[i]
                   if not (self._dir(i) / "combinacoes.json").exists()
                   and not (self._dir(i) / "relacoes" / f"{b['indice']:03d}.json").exists()]
        self.progress(f"1a. relações: {len(tarefas)} blocos", flush=True)

        def rel(t):
            item, b = t
            t_ = self.temas[item]
            user = (f"<tema>\nÁrea: {t_['area']}\nTema: {t_['tema']}\n</tema>\n\n<documento>{t_['titulo']}</documento>\n\n"
                    f"<bloco>\n{b['titulo_capitulo']} / {b['subtitulo']}\n{b['texto']}\n</bloco>")
            nome = f"relacoes_{item}_{b['indice']:03d}"
            try:
                d = self.cliente("relacoes").json(system, user, tag="meta_relacoes", max_tokens=8000, item=item,
                                                  validate=lambda d: inv.validar_relacoes(d, b["texto"]))
            except Exception as exc:  # noqa: BLE001
                if not _filtrado(exc):
                    self._falha(nome, exc)
                    return False
                d = {"status": "sem_relacoes", "motivo": "bloqueado pelo filtro de conteúdo", "relacoes": []}
            rels = [{**r, "id": f"B{b['indice']:03d}.R{k}", "bloco": b["indice"]} for k, r in enumerate(d["relacoes"], 1)]
            atomic_json(self._dir(item) / "relacoes" / f"{b['indice']:03d}.json",
                        {"item": item, "bloco": b["indice"], "status": d["status"], "motivo": d["motivo"], "relacoes": rels})
            self._ok(nome)
            return True

        falhas = self._paralelo(tarefas, rel, "relações")
        pend = [i for i in self.itens if not (self._dir(i) / "combinacoes.json").exists()
                and len(list((self._dir(i) / "relacoes").glob("*.json"))) == len(self.docs[i])]
        self.progress(f"1b. encadeamentos: {len(pend)} tópicos", flush=True)

        def comb(item):
            rels = [r for p in sorted((self._dir(item) / "relacoes").glob("*.json")) for r in read_json(p)["relacoes"]]
            subt = {b["indice"]: b["subtitulo"] for b in self.docs[item]}
            linhas = [f"{r['id']} | bloco {r['bloco']:03d} ({subt[r['bloco']]}) | {r['tipo']} | {r['afirmacao']} | "
                      f"condições: {'; '.join(r['condicoes']) or '-'} | limites: {'; '.join(r['limites']) or '-'}" for r in rels]
            t_ = self.temas[item]
            user = (f"<tema>\nÁrea: {t_['area']}\nTema: {t_['tema']}\n</tema>\n\n<documento>{t_['titulo']}</documento>\n\n"
                    "<relacoes>\n" + "\n".join(linhas) + "\n</relacoes>")
            bloco_da = {r["id"]: r["bloco"] for r in rels}
            try:
                d = self.cliente("combinacoes").json(
                    inv.prompt("combinacoes", QUANTIDADE=self.combinacoes_por_doc), user, tag="meta_combinacoes",
                    max_tokens=32000, item=item,
                    validate=lambda d: inv.validar_combinacoes(d, bloco_da, self.combinacoes_por_doc))
            except Exception as exc:  # noqa: BLE001
                self._falha(f"combinacoes_{item}", exc)
                return False
            atomic_json(self._dir(item) / "combinacoes.json",
                        {"item": item, "observacao": d["observacao"],
                         "combinacoes": [{**c, "id": f"C{k}"} for k, c in enumerate(d["combinacoes"], 1)]})
            self._ok(f"combinacoes_{item}")
            return True

        return falhas + self._paralelo(pend, comb, "encadeamentos")

    # ---------------------------------------------------------------- banco dinâmico de exemplos
    def _dinamico(self) -> dict:
        arq = self.saida / "banco_dinamico.json"
        atual = read_json(arq) if arq.exists() else {"aprovadas": [], "reprovadas": []}
        return {k: self.banco_inicial[k] + atual[k] for k in ("aprovadas", "reprovadas")}

    def atualizar_banco(self) -> None:
        aprovadas, reprovadas = [], []
        for item in self.itens:
            for q in self.questoes(item):
                a = q.get("auditoria")
                if not a:
                    continue
                reg = {"id": q["uid"], "item": item, "tipo": a["tipo_sugerido"], "composicao": q["composicao"],
                       "pergunta": q["pergunta"], "resposta": q["resposta"]}
                if q.get("aprovada"):
                    aprovadas.append({**reg, "por_que": "aprovada pelo auditor: " + a["justificativa"]})
                elif not q.get("duplicada"):
                    reprovadas.append({**reg, "problema": a["justificativa"]})
        atomic_json(self.saida / "banco_dinamico.json", {"aprovadas": aprovadas, "reprovadas": reprovadas})

    def render_exemplos(self, item: str, composicao: str, semente: str) -> str:
        din = self._dinamico()
        if composicao == "simples":
            escolhidos = []
            for t in TIPOS_JANELA:
                pool = [e for e in self.base["exemplos"] + din["aprovadas"]
                        if e["tipo"] == t and e["item"] != item and e["composicao"] == "simples"]
                pool = pool or [e for e in self.base["exemplos"] if e["tipo"] == t]
                if pool:
                    escolhidos.append(pool[_h(semente, t) % len(pool)])
            fixos = self.base["contraexemplos"]
        else:
            pool = [e for e in self.base["exemplos"] + din["aprovadas"] if e["composicao"] == "composta" and e["item"] != item]
            pool = pool or [e for e in self.base["exemplos"] if e["composicao"] == "composta"]
            escolhidos = sorted(pool, key=lambda e: _h(semente, e["id"]))[:3]
            fixos = [c for c in self.base["contraexemplos"] if c["tipo"] != "conceito"]
        fixos = sorted(fixos, key=lambda c: _h(semente, c["id"]))[:CONTRA_FIXOS]
        dinamicos = sorted((c for c in din["reprovadas"] if c["item"] != item),
                           key=lambda c: _h(semente, c["id"]))[:CONTRA_DINAMICOS]
        bons = "\n\n".join(f"[{e['tipo']}] Pergunta: {e['pergunta']}\nResposta: {e['resposta']}\nPor que é boa: {e['por_que']}"
                           for e in escolhidos)
        ruins = "\n\n".join(f"[{c['tipo']}] Pergunta: {c['pergunta']}\nResposta: {c['resposta']}\nProblema: {c['problema']}"
                            for c in fixos + dinamicos)
        return (f"<exemplos_por_tipo>\n{bons}\n</exemplos_por_tipo>\n\n"
                f"<contraexemplos>\nNão gere questões como estas.\n\n{ruins}\n</contraexemplos>")

    # ---------------------------------------------------------------- 2. compostas
    def compostas(self) -> int:
        system, tarefas = prompt("composta"), []
        for item in self.itens:
            arq = self._dir(item) / "combinacoes.json"
            if not arq.exists():
                continue
            rels = {r["id"]: r for p in sorted((self._dir(item) / "relacoes").glob("*.json")) for r in read_json(p)["relacoes"]}
            for c in read_json(arq)["combinacoes"]:
                if not (self._dir(item) / "compostas" / f"{c['id']}.json").exists():
                    tarefas.append((item, c, [rels[i] for i in c["relacoes"] if i in rels]))
        self.progress(f"2. compostas: {len(tarefas)} encadeamentos", flush=True)

        def um(t):
            item, c, rels = t
            bs = {b["indice"]: b for b in self.docs[item]}
            usados = sorted({r["bloco"] for r in rels})
            enc = {k: c[k] for k in ("tipo", "titulo", "ponte", "cadeia", "cenario", "resposta", "resposta_atraente",
                                     "sinal_que_descarta", "condicoes_enunciado", "limites")}
            enc["relacoes"] = [{k: r[k] for k in ("id", "afirmacao", "condicoes", "limites")} for r in rels]
            t_ = self.temas[item]
            user = "\n\n".join((
                f"<tema>\nÁrea: {t_['area']}\nTema: {t_['tema']}\n</tema>",
                f"<encadeamento>\n{json.dumps(enc, ensure_ascii=False, indent=2)}\n</encadeamento>",
                self.render_exemplos(item, "composta", f"{item}:{c['id']}"),
                "<blocos>\n" + "\n\n".join(f"[bloco {i:03d}] {bs[i]['titulo_capitulo']} / {bs[i]['subtitulo']}\n"
                                           f"{bs[i]['texto']}" for i in usados) + "\n</blocos>"))
            try:
                d = self.cliente("geracao").json(system, user, tag="meta_composta", max_tokens=12000, item=item,
                                                 validate=validar_composta)
            except Exception as exc:  # noqa: BLE001
                if not _filtrado(exc):
                    self._falha(f"composta_{item}_{c['id']}", exc)
                    return False
                d = {"status": "insuficiente", "motivo": "bloqueado pelo filtro de conteúdo", "tipo": "", "cenario": False,
                     "pergunta": "", "resposta": ""}
            atomic_json(self._dir(item) / "compostas" / f"{c['id']}.json",
                        {"id": c["id"], "item": item, "blocos": usados, "relacoes": [r["id"] for r in rels], **d})
            self._ok(f"composta_{item}_{c['id']}")
            return True

        return self._paralelo(tarefas, um, "compostas")

    # ---------------------------------------------------------------- 3. janelas por rodada
    def _passagens(self, item: str) -> dict[int, list[dict]]:
        out = defaultdict(list)
        for p in sorted((self._dir(item) / "janelas").glob("r*/*.json")):
            out[int(p.stem)].append(read_json(p))
        return out

    def escolher_janelas(self, item: str, rodada: int) -> list[int]:
        focos = list(range(len(self.docs[item])))
        if rodada == 1:
            return focos
        falta = self.meta - self.validas(item)
        if falta <= 0:
            return []
        passagens = self._passagens(item)
        aprov = Counter(q["foco"] for q in self.questoes(item) if q["origem"] == "janela" and q.get("aprovada"))
        n_pass = sum(len(v) for v in passagens.values())
        taxa = max(0.5, sum(aprov.values()) / n_pass) if n_pass else 1.0
        cands = [f for f in focos if len(passagens.get(f, [])) < self.max_passagens]
        cands.sort(key=lambda f: (-aprov.get(f, 0) / max(1, len(passagens.get(f, []))), f))
        return cands[: math.ceil(falta / taxa)]

    def janelas(self, rodada: int) -> int:
        system, modelo_usuario, _ = carregar_prompt(4, 4, PROMPT_JANELA)
        tarefas = [(i, f) for i in self.itens
                   if rodada == 1 or self.validas(i) < self.meta
                   for f in self.escolher_janelas(i, rodada)
                   if not (self._dir(i) / "janelas" / f"r{rodada}" / f"{f:03d}.json").exists()]
        self.progress(f"3. janelas, rodada {rodada}: {len(tarefas)}", flush=True)
        anteriores = {i: self._passagens(i) for i in self.itens}

        def um(t):
            item, foco = t
            jan = janela(self.docs[item], foco)
            existentes = [f"- [{q['tipo']}] {q['pergunta']} → {q['resposta']}" for j in anteriores[item].get(foco, [])
                          for q in j["questoes"]]
            user = preencher(modelo_usuario, self.temas[item], "", "\n".join(existentes) or "Nenhuma.", jan,
                             self.render_exemplos(item, "simples", f"{item}:{foco}:r{rodada}"))
            nome = f"janela_{item}_r{rodada}_{foco:03d}"
            try:
                d = self.cliente("geracao").json(system, user, tag="meta_janela", max_tokens=16000, item=item,
                                                 validate=validar_janela_v16)
            except Exception as exc:  # noqa: BLE001
                if not _filtrado(exc):
                    self._falha(nome, exc)
                    return False
                d = {"status": "sem_questoes", "motivo": "bloqueado pelo filtro de conteúdo", "questoes": []}
            textos = {r: b["texto"] for r, b in jan}
            atomic_json(self._dir(item) / "janelas" / f"r{rodada}" / f"{foco:03d}.json", {
                "item": item, "foco": foco, "rodada": rodada, "status": d["status"], "motivo": d["motivo"],
                "questoes": [{**q, "verificacoes": verificar(q, textos)} for q in d["questoes"]]})
            self._ok(nome)
            return True

        return self._paralelo(tarefas, um, f"janelas r{rodada}")

    # ---------------------------------------------------------------- banco de questões e auditoria
    def questoes(self, item: str) -> list[dict]:
        aud = {a["uid"]: a for p in (self._dir(item) / "auditoria").glob("*.json") for a in read_json(p)["avaliacoes"]}
        out = []
        for p in sorted((self._dir(item) / "compostas").glob("*.json")):
            c = read_json(p)
            if c["status"] == "ok":
                out.append({"uid": f"{item}:c:{c['id']}", "origem": "composta", "item": item, "rodada": 0,
                            "tipo": c["tipo"], "cenario": c["cenario"], "composicao": "composta",
                            "pergunta": c["pergunta"], "resposta": c["resposta"], "blocos": c["blocos"]})
        for p in sorted((self._dir(item) / "janelas").glob("r*/*.json"), key=lambda p: (int(p.parent.name[1:]), p.stem)):
            j = read_json(p)
            for q in j["questoes"]:
                out.append({"uid": f"{item}:j:r{j['rodada']}:{j['foco']:03d}:{q['id']}", "origem": "janela", "item": item,
                            "rodada": j["rodada"], "foco": j["foco"], "tipo": q["tipo"], "cenario": q["cenario"],
                            "composicao": "simples", "conhecimento": q["conhecimento"], "pergunta": q["pergunta"],
                            "resposta": q["resposta"], "fundamentos": q["fundamentos"], "verificacoes": q["verificacoes"]})
        aceitos, curtas = [], []
        for q in out:   # ordem de geração: a primeira versão de um conhecimento fica, as quase duplicatas saem
            if q["uid"] not in aud:
                continue
            q["auditoria"] = {k: aud[q["uid"]][k] for k in ("tipo_confere", "tipo_sugerido", "referencia_valida",
                                                             "atalho", "justificativa")}
            if q["auditoria"]["referencia_valida"] and not q["auditoria"]["atalho"]:
                t = _tokens(q["pergunta"] + " " + q["resposta"])
                c = _resposta_curta(q["resposta"])
                if any(t and a and len(t & a) / len(t | a) >= LIMIAR_DUPLICATA for a in aceitos) or \
                        (c and any(len(c & b) / len(c | b) >= LIMIAR_RESPOSTA_CURTA for b in curtas)):
                    q["duplicada"] = True
                else:
                    q["aprovada"] = True
                    aceitos.append(t)
                    if c:
                        curtas.append(c)
        return out

    def validas(self, item: str) -> int:
        return sum(1 for q in self.questoes(item) if q.get("aprovada"))

    def auditar(self) -> int:
        pend = []
        for item in self.itens:
            pend += [q for q in self.questoes(item) if "auditoria" not in q]
        pend.sort(key=lambda q: (q["item"], _h("aud", q["uid"])))
        lotes = [pend[i:i + self.lote] for i in range(0, len(pend), self.lote)]
        self.progress(f"   auditoria: {len(pend)} questões em {len(lotes)} lotes", flush=True)
        system = prompt("auditoria")

        def um(lote):
            ids = [f"Q{k}" for k in range(1, len(lote) + 1)]
            itens = [{"id": i, "tipo_declarado": q["tipo"], "pergunta": q["pergunta"], "resposta_referencia": q["resposta"]}
                     for i, q in zip(ids, lote)]
            nome = hashlib.sha256("|".join(q["uid"] for q in lote).encode()).hexdigest()[:16]
            try:
                d = self.cliente("auditoria").json(
                    system, json.dumps(itens, ensure_ascii=False), tag="meta_auditoria", max_tokens=12000,
                    validate=lambda d: validar_lote(d, ids, "avaliacoes", ("tipo_confere", "referencia_valida", "atalho"),
                                                    "tipo_sugerido"))
            except Exception as exc:  # noqa: BLE001
                self._falha(f"auditoria_{nome}", exc)
                return False
            por_item = defaultdict(list)
            for a, q in zip(d["avaliacoes"], lote):
                por_item[q["item"]].append({**a, "uid": q["uid"]})
            for item, avs in por_item.items():
                atomic_json(self._dir(item) / "auditoria" / f"{nome}.json", {"avaliacoes": avs})
            self._ok(f"auditoria_{nome}")
            return True

        falhas = self._paralelo(lotes, um, "auditoria")
        self.atualizar_banco()
        return falhas

    # ---------------------------------------------------------------- execução
    def run(self) -> int:
        self.config()
        falhas = self.inventario()
        falhas += self.compostas()
        falhas += self.auditar()
        for rodada in range(1, self.max_rodadas + 1):
            antes = {i: self.validas(i) for i in self.itens}
            if rodada > 1 and all(v >= self.meta for v in antes.values()):
                break
            falhas += self.janelas(rodada)
            falhas += self.auditar()
            ganho = {i: self.validas(i) - antes[i] for i in self.itens}
            self.progress("   válidas por tópico: " + ", ".join(f"{i} {self.validas(i)} (+{ganho[i]})" for i in self.itens),
                          flush=True)
            if rodada > 1 and not any(ganho.values()):
                break
        self.relatorio()
        return falhas

    # ---------------------------------------------------------------- relatório
    def relatorio(self) -> dict:
        todas = [q for item in self.itens for q in self.questoes(item)]
        aprovadas = [{**q, "tipo_declarado": q["tipo"], "tipo": q["auditoria"]["tipo_sugerido"]} for q in todas if q.get("aprovada")]
        for nome, qs in (("questoes.jsonl", todas), ("aprovadas.jsonl", aprovadas)):
            with (self.saida / nome).open("w", encoding="utf-8", newline="\n") as f:
                for q in qs:
                    f.write(json.dumps(q, ensure_ascii=False) + "\n")

        def taxa(qs):
            aud = [q for q in qs if "auditoria" in q]
            return {"geradas": len(qs), "auditadas": len(aud), "aprovadas": sum(bool(q.get("aprovada")) for q in qs),
                    "duplicadas": sum(bool(q.get("duplicada")) for q in qs),
                    "ref_invalida": sum(not q["auditoria"]["referencia_valida"] for q in aud),
                    "atalho": sum(q["auditoria"]["atalho"] for q in aud)}

        res = {"meta": self.meta, "modelos": self.modelos, "topicos": {}, "por_tipo": {}, "por_rodada": {}}
        for item in self.itens:
            qs = [q for q in todas if q["item"] == item]
            passagens = self._passagens(item)
            res["topicos"][item] = {
                "tema": self.temas[item]["tema"], "blocos": len(self.docs[item]),
                "relacoes": sum(len(read_json(p)["relacoes"]) for p in (self._dir(item) / "relacoes").glob("*.json")),
                "encadeamentos": len(read_json(self._dir(item) / "combinacoes.json")["combinacoes"])
                if (self._dir(item) / "combinacoes.json").exists() else 0,
                "passagens_janela": sum(len(v) for v in passagens.values()),
                "rodadas": max((j["rodada"] for v in passagens.values() for j in v), default=0),
                "validas": sum(bool(q.get("aprovada")) for q in qs), "atingiu_meta": sum(bool(q.get("aprovada")) for q in qs) >= self.meta,
                "compostas": taxa([q for q in qs if q["origem"] == "composta"]),
                "janela": taxa([q for q in qs if q["origem"] == "janela"]),
                "aprovadas_por_tipo": dict(Counter(q["tipo"] for q in aprovadas if q["item"] == item))}
        for t in TIPOS:
            res["por_tipo"][t] = {o: taxa([q for q in todas if q["tipo"] == t and q["origem"] == o]) for o in ("janela", "composta")}
        for r in sorted({q["rodada"] for q in todas}):
            res["por_rodada"][r] = taxa([q for q in todas if q["rodada"] == r])
        din = self._dinamico()
        res["banco_dinamico"] = {"aprovadas": len(din["aprovadas"]), "reprovadas": len(din["reprovadas"]),
                                 "herdadas": self.n_banco_inicial}
        res["falhas_pendentes"] = sorted(p.stem for p in (self.saida / "falhas").glob("*.json"))
        atomic_json(self.saida / "resultado.json", res)
        self._proposta(aprovadas, todas)
        self._markdown(res, aprovadas)
        return res

    def _proposta(self, aprovadas: list[dict], todas: list[dict]) -> None:
        """Sugestão de banco curado: até 3 aprovadas por tipo, de tópicos diferentes, e reprovadas típicas."""
        exemplos = list(self.base["exemplos"])
        for t in TIPOS:
            vistos = {e["item"] for e in exemplos if e["tipo"] == t}
            for q in sorted((q for q in aprovadas if q["tipo"] == t), key=lambda q: _h("prop", q["uid"])):
                if q["item"] not in vistos and sum(e["tipo"] == t for e in exemplos) < 5:
                    exemplos.append({"id": q["uid"], "item": q["item"], "tipo": t, "composicao": q["composicao"],
                                     "pergunta": q["pergunta"], "resposta": q["resposta"],
                                     "por_que": "aprovada pelo auditor: " + q["auditoria"]["justificativa"]})
                    vistos.add(q["item"])
        contra = list(self.base["contraexemplos"])
        reprov = [q for q in todas if "auditoria" in q and not q.get("aprovada") and not q.get("duplicada")]
        for t in TIPOS:
            for q in sorted((q for q in reprov if q["auditoria"]["tipo_sugerido"] == t), key=lambda q: _h("c", q["uid"]))[:2]:
                contra.append({"id": q["uid"], "item": q["item"], "tipo": t, "pergunta": q["pergunta"],
                               "resposta": q["resposta"], "problema": q["auditoria"]["justificativa"]})
        atomic_json(self.saida / "exemplos_proposto.json",
                    {"descricao": "Proposta de atualização de geracao_tipos/exemplos.json; revisar antes de promover.",
                     "exemplos": exemplos, "contraexemplos": contra})

    def _markdown(self, res: dict, aprovadas: list[dict]) -> None:
        total = sum(t["validas"] for t in res["topicos"].values())
        l = [f"# Geração por meta (v17): {res['meta']} questões válidas por tópico", "",
             "Janela com o prompt v17 (sem decisão), compostas a partir dos encadeamentos, auditoria como filtro e "
             "banco dinâmico de exemplos e contraexemplos (herdado das rodadas anteriores).", "",
             f"**Total: {total} questões válidas em {len(res['topicos'])} tópicos; "
             f"{sum(t['atingiu_meta'] for t in res['topicos'].values())} atingiram a meta.**", "",
             "| Tópico | Tema | blocos | encadeamentos | passagens de janela | rodadas | válidas | meta | janela aprov. | compostas aprov. |",
             "|---|---|---|---|---|---|---|---|---|---|"]
        for i, t in res["topicos"].items():
            l.append(f"| {i} | {t['tema'][:45]} | {t['blocos']} | {t['encadeamentos']} | {t['passagens_janela']} | {t['rodadas']} | "
                     f"**{t['validas']}** | {'✓' if t['atingiu_meta'] else '✗'} | {t['janela']['aprovadas']}/{t['janela']['geradas']} | "
                     f"{t['compostas']['aprovadas']}/{t['compostas']['geradas']} |")
        l += ["", "| Tipo | janela (aprov./geradas) | compostas (aprov./geradas) |", "|---|---|---|"]
        for t, b in res["por_tipo"].items():
            l.append(f"| {t} | {b['janela']['aprovadas']}/{b['janela']['geradas']} | {b['composta']['aprovadas']}/{b['composta']['geradas']} |")
        l += ["", "Por rodada (0 = compostas): " + "; ".join(
            f"r{r}: {b['aprovadas']}/{b['geradas']} (dup. {b['duplicadas']})" for r, b in res["por_rodada"].items()) + ".",
              f"Banco dinâmico: {res['banco_dinamico']}. Falhas pendentes: {len(res['falhas_pendentes'])}.", "",
              "## Amostra de aprovadas por tópico", ""]
        for i in res["topicos"]:
            l.append(f"### {i}")
            l.append("")
            for q in sorted((q for q in aprovadas if q["item"] == i), key=lambda q: _h("md", q["uid"]))[:4]:
                l += [f"**[{q['tipo']} · {q['composicao']}]** {q['pergunta']}", "", f"- Resposta: {q['resposta']}", ""]
        (self.saida / "RELATORIO.md").write_text("\n".join(l), encoding="utf-8")
