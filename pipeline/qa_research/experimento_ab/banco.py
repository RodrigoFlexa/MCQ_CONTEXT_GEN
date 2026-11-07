"""Banco final PetroQuest: poda do dataset final v2 e montagem do arquivo que será publicado.

Parte do dataset final v2 (todas as fontes, só gabaritos totalmente sustentados, avaliado com resposta de até 20
palavras e classificado pela rubrica do especialista) e aplica, em ordem:

1. Regras determinísticas (sem API):
   (R1) suspeita                nem o GPT-5 nem o GPT-5.4 chegam ao gabarito COM o documento. Pode ser a pegadinha
                                do enunciado funcionando (o modelo cai na resposta padrão mesmo lendo o texto) ou um
                                gabarito vago ou não único: a questão vai para a revisão (passo 2), que também vê as
                                respostas com documento. Sem revisão concluída, fica fora (R1);
   R2 resposta_no_enunciado     80% ou mais das palavras de conteúdo do gabarito já estão na pergunta (escolha entre
                                opções dadas ou atalho);
   R3 forma_por_que_nao_basta   "Por que X não basta/garante...": a forma que o projeto decidiu evitar;
   R4 mesmo_conhecimento        par do mesmo tópico com gabarito e pergunta muito parecidos (TF-IDF): fica o da
                                fonte de maior prioridade.
2. Revisão de unicidade (API, nas questões que o GPT-5 não acerta sem contexto e nas suspeitas R1): um juiz
   especialista vê a pergunta, o gabarito, a resposta padrão (a pegadinha prevista), o documento e as respostas sem
   contexto de GPT-5, GPT-5 mini e GPT-4.1 (nas suspeitas, também as de GPT-5 e GPT-5.4 com documento), e diz se
   cada resposta é equivalente, alternativa válida ou incorreta; se o gabarito é específico, único e se depende do
   documento. Resposta que cai na pegadinha é incorreta: a questão fica, difícil. Saem:
   R5 gabarito_nao_unico        alguma resposta é alternativa válida, ou o gabarito não é único;
   R6 gabarito_vago             o gabarito não nomeia um elemento técnico concreto;
   R7 depende_documento         a resposta exige algo próprio do documento.
   Resposta "equivalente" que o juiz original não aceitou vira acerto (veredito corrigido) e a questão continua.
3. R8 excedente_topico: tópicos acima de TETO_TOPICO perdem as questões mais redundantes dentro do tópico (maior
   similaridade com outra questão do tópico), sem tocar no tipo minoritário (consequência).

Saída em relatorios/petroquest_banco_v1: banco.jsonl (ids PQ-0001...), poda.jsonl (cada questão removida e a regra),
unicidade/ (uma revisão por questão), resumo.json e BANCO.md. Sem a revisão de unicidade concluída, o banco sai
marcado como provisório.
"""
from __future__ import annotations

import csv
import json
import re
from collections import Counter
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

import numpy as np

from pipeline.inventario.locking import output_lock
from pipeline.inventario.textutil import atomic_json, read_json
from pipeline.qa_research import benchmark_gap as G
from pipeline.qa_research.geracao_tipos.rodadas import _filtrado, _nome_arq

from . import comum as C
from .completo import SAIDA as ORIGEM
from .painel import ESTRATOS, estrato

SAIDA = C.QA / "relatorios" / "petroquest_banco_v1"
INDEPENDENTES = ("gpt-4-1-mini", "gpt-4-1", "gpt-5-mini", "gpt-5")
REVISADOS = ("gpt-5", "gpt-5-mini", "gpt-4-1")          # respostas mostradas ao juiz de unicidade (R1, R2, R3)
FORTES_COM_CONTEXTO = ("gpt-5", "gpt-5-4")
JUIZ = G.Q.JUIZ
TETO_TOPICO = 150
PROTEGIDOS = ("consequencia",)
PRIORIDADE = ("v23", "v23c", "v22", "antigo", "conceitos", "variada", "tipo_decisao", "tipo_diagnostico",
              "tipo_procedimento")
STOP = set("a o as os um uma uns umas de do da dos das em no na nos nas por pelo pela pelos pelas para com e ou que "
           "se ao aos à às é".split())
REGRAS = {
    "R1": "sem_alcance_com_contexto", "R2": "resposta_no_enunciado", "R3": "forma_por_que_nao_basta",
    "R4": "mesmo_conhecimento", "R5": "gabarito_nao_unico", "R6": "gabarito_vago", "R7": "depende_documento",
    "R8": "excedente_topico"}
DESCRICAO = {
    "R1": "GPT-5 e GPT-5.4 erram com o documento e a revisão não foi concluída",
    "R2": "o gabarito já está no enunciado (escolha entre opções dadas ou atalho)",
    "R3": "forma \"por que X não basta/garante\"",
    "R4": "mesmo conhecimento de outra questão do tópico",
    "R5": "revisão: outra resposta também é correta",
    "R6": "revisão: gabarito vago",
    "R7": "revisão: depende do documento",
    "R8": "tópico acima do teto: questão mais redundante do tópico"}


def conteudo(s: str) -> list[str]:
    return [t for t in re.findall(r"\w+", s.lower()) if t not in STOP and len(t) > 2]


def sobreposicao(q: dict) -> float:
    g = set(conteudo(q["resposta"]))
    return len(g & set(conteudo(q["pergunta"]))) / len(g) if g else 0.0


def _tfidf(textos: list[str]):
    from sklearn.feature_extraction.text import TfidfVectorizer
    return TfidfVectorizer(ngram_range=(1, 2), sublinear_tf=True).fit_transform(textos)


def validar_unicidade(d: dict, ids: list[str]) -> None:
    chaves = {"respostas", "gabarito_especifico", "gabarito_unico", "depende_documento", "justificativa"}
    if not isinstance(d, dict) or set(d) != chaves:
        raise ValueError(f"use exatamente as chaves {sorted(chaves)}")
    if not isinstance(d["respostas"], list) or sorted(r.get("id") for r in d["respostas"] if isinstance(r, dict)) != \
            sorted(ids) or any(r.get("avaliacao") not in ("equivalente", "alternativa_valida", "incorreta")
                               for r in d["respostas"]):
        raise ValueError(f"respostas deve avaliar {ids} como equivalente, alternativa_valida ou incorreta")
    for k in ("gabarito_especifico", "gabarito_unico", "depende_documento"):
        if not isinstance(d[k], bool):
            raise ValueError(f"{k} deve ser true ou false")
    if not isinstance(d["justificativa"], str) or not d["justificativa"].strip():
        raise ValueError("justificativa deve ser um texto")


class Banco:
    def __init__(self, origem: Path = ORIGEM, saida: Path = SAIDA, *, juiz: str = JUIZ, teto: int = TETO_TOPICO,
                 workers: int = 8, cliente=None, embedder=None, exp: Path = C.EXPERIMENTO, progress=print):
        self._embedder, self.cal_arq = embedder, Path(exp) / "calibracao" / "calibracao.json"
        self.similaridade_teto = None
        self.origem, self.saida = Path(origem), Path(saida)
        self.juiz, self.teto, self.workers, self.progress = juiz, int(teto), max(1, int(workers)), progress
        self._cliente = cliente
        self.qs = {q["uid"]: q for q in C.linhas(self.origem / "dataset.jsonl")}
        self.vs: dict = {}
        with (self.origem / "pares.csv").open(encoding="utf-8-sig") as f:
            for r in csv.DictReader(C.sem_nul(f)):
                if r["uid"] in self.qs:
                    self.vs.setdefault(r["uid"], {})[r["modelo"]] = r
        self.rub = {r["uid"]: r for r in C.linhas(self.origem / "rubrica" / "rubrica.jsonl")} \
            if (self.origem / "rubrica" / "rubrica.jsonl").exists() else {}

    # ---------------------------------------------------------------- 1. regras determinísticas
    def regras_locais(self) -> dict:
        poda: dict = {}
        self.suspeitas = {u for u in self.qs if all(self.vs.get(u, {}).get(m, {}).get("veredito_open_book") != "correta"
                                                    for m in FORTES_COM_CONTEXTO)}
        for u, q in self.qs.items():
            if sobreposicao(q) >= 0.8:
                poda[u] = ("R2", f"sobreposição {sobreposicao(q):.2f}")
            elif q.get("sinalizar") and re.match(r"\s*por que\b", q["pergunta"], re.I):
                poda[u] = ("R3", q["sinalizar"])
        restantes = [q for u, q in self.qs.items() if u not in poda]
        por_item: dict = {}
        for q in restantes:
            por_item.setdefault(q["item"], []).append(q)
        prio = lambda q: (PRIORIDADE.index(q["fonte"]) if q["fonte"] in PRIORIDADE else 99, q["uid"])  # noqa: E731
        for item, qs in sorted(por_item.items()):
            if len(qs) < 2:
                continue
            from sklearn.feature_extraction.text import TfidfVectorizer
            vr = TfidfVectorizer(sublinear_tf=True).fit([q["resposta"] + " " + q["pergunta"] for q in qs])
            R, Q = vr.transform([q["resposta"] for q in qs]), vr.transform([q["pergunta"] for q in qs])
            SR, SQ = (R @ R.T).toarray(), (Q @ Q.T).toarray()
            for i in range(len(qs)):
                for j in range(i + 1, len(qs)):
                    if SR[i, j] >= 0.6 and SQ[i, j] >= 0.25:
                        a, b = sorted((qs[i], qs[j]), key=prio)
                        if a["uid"] not in poda and b["uid"] not in poda:
                            poda[b["uid"]] = ("R4", f"mesmo conhecimento de {a['uid']} (gabarito {SR[i, j]:.2f})")
        return poda

    # ---------------------------------------------------------------- 2. revisão de unicidade
    def alvos_unicidade(self, poda: dict) -> list[str]:
        return [u for u in self.qs if u not in poda and (
            u in self.suspeitas or self.vs[u].get("gpt-5", {}).get("veredito_closed_book") != "correta")]

    def _arq_u(self, uid: str) -> Path:
        return self.saida / "unicidade" / f"{_nome_arq(uid)}.json"

    def cliente(self):
        if self._cliente is None:
            self._cliente = C.cliente_llm(self.juiz, self.saida, "unicidade")
        return self._cliente

    def entrada_unicidade(self, u: str) -> tuple[str, dict]:
        """-> payload e {id: [modelo, condição]} das respostas mostradas."""
        q, v = self.qs[u], self.vs[u]
        mostrar = [(m, "closed_book") for m in REVISADOS]
        if u in self.suspeitas:
            mostrar += [(m, "open_book") for m in FORTES_COM_CONTEXTO]
        resp, ids = [], {}
        for m, cond in mostrar:
            texto = v.get(m, {}).get(f"resposta_{cond}")
            if texto:
                i = f"R{len(resp) + 1}"
                resp.append({"id": i, "com_documento": cond == "open_book", "resposta": texto})
                ids[i] = [m, cond]
        payload = {"pergunta": q["pergunta"], "gabarito": q["resposta"], "explicacao": q.get("explicacao"),
                   "resposta_padrao": q.get("resposta_padrao"), "por_que_nao": q.get("por_que_nao"),
                   "documento": q["contexto_tecnico"], "respostas": resp}
        return json.dumps({k: x for k, x in payload.items() if x is not None}, ensure_ascii=False), ids

    def unicidade(self, poda: dict) -> int:
        alvos = self.alvos_unicidade(poda)
        cfg = {"schema": "petroquest-unicidade-v1", "juiz": self.juiz, "prompt_sha256": C.sha(C.prompt("unicidade")),
               "revisados": list(REVISADOS)}
        with output_lock(self.saida / "unicidade"):
            old = read_json(self.saida / "unicidade" / "config.json")
            if old is not None and old != cfg:
                raise ValueError(f"Revisão de unicidade com outro juiz ou prompt em {C.relativo(self.saida)}; "
                                 "apague a pasta unicidade/")
            atomic_json(self.saida / "unicidade" / "config.json", cfg)
            (self.saida / "unicidade" / "falhas").mkdir(parents=True, exist_ok=True)
            faltam = [u for u in alvos if not self._arq_u(u).exists()]
            self.progress(f"[banco] unicidade: {len(alvos) - len(faltam)}/{len(alvos)} revisadas; {len(faltam)} a "
                          "revisar", flush=True)
            sistema = C.prompt("unicidade")

            def um(u: str) -> bool:
                user, ids = self.entrada_unicidade(u)
                try:
                    d = self.cliente().json(sistema, user, tag="unicidade", max_tokens=6000, item=self.qs[u]["item"],
                                            validate=lambda d: validar_unicidade(d, list(ids)))
                    rec = {"uid": u, "status": "revisada", "ids": ids, **d}
                except Exception as exc:  # noqa: BLE001
                    if not _filtrado(exc):
                        atomic_json(self.saida / "unicidade" / "falhas" / self._arq_u(u).name,
                                    {"uid": u, "erro": f"{type(exc).__name__}: {exc}"[:1500]})
                        return False
                    rec = {"uid": u, "status": "bloqueio_provedor"}
                atomic_json(self._arq_u(u), rec)
                return True

            ok = 0
            with ThreadPoolExecutor(max_workers=self.workers) as pool:
                for r in pool.map(um, faltam):
                    ok += r
                    if ok and ok % 200 == 0:
                        self.progress(f"[banco] unicidade {ok}/{len(faltam)}", flush=True)
            return len(faltam) - ok

    def aplicar_unicidade(self, poda: dict) -> tuple[dict, dict, int]:
        """-> poda ampliada, vereditos corrigidos {uid: {condição: {modelo: 'correta'}}}, revisões pendentes."""
        poda, corr, pend = dict(poda), {}, 0
        self.suspeitas_mantidas = 0
        for u in self.alvos_unicidade(poda):
            r = read_json(self._arq_u(u))
            if r is None or r.get("status") != "revisada":
                pend += r is None
                if u in self.suspeitas:
                    v = self.vs[u]
                    poda[u] = ("R1", "com documento: " + ", ".join(
                        f"{m} {v.get(m, {}).get('veredito_open_book')}" for m in FORTES_COM_CONTEXTO))
                continue
            aval = {tuple(r["ids"][x["id"]]): x["avaliacao"] for x in r["respostas"]}
            if any(a == "alternativa_valida" for a in aval.values()) or not r["gabarito_unico"]:
                poda[u] = ("R5", r["justificativa"])
            elif not r["gabarito_especifico"]:
                poda[u] = ("R6", r["justificativa"])
            elif r["depende_documento"]:
                poda[u] = ("R7", r["justificativa"])
            else:
                self.suspeitas_mantidas += u in self.suspeitas
                eq: dict = {}
                for (m, cond), a in aval.items():
                    if a == "equivalente" and self.vs[u][m][f"veredito_{cond}"] != "correta":
                        eq.setdefault(cond, {})[m] = "correta"
                if eq:
                    corr[u] = eq
        return poda, corr, pend

    # ---------------------------------------------------------------- 3. teto por tópico
    def teto_topico(self, poda: dict) -> dict:
        poda = dict(poda)
        por_item: dict = {}
        for u, q in self.qs.items():
            if u not in poda:
                por_item.setdefault(q["item"], []).append(q)
        for item, qs in sorted(por_item.items()):
            if len(qs) <= self.teto:
                continue
            S = self._similaridade(qs)
            np.fill_diagonal(S, 0)
            vivos = set(range(len(qs)))
            while len(vivos) > self.teto:
                cand = [i for i in vivos if qs[i]["tipo"] not in PROTEGIDOS]
                if not cand:
                    break
                idx = sorted(vivos)
                i = max(cand, key=lambda i: (max(S[i, j] for j in idx if j != i), qs[i]["uid"]))
                j = max((j for j in idx if j != i), key=lambda j: S[i, j])
                poda[qs[i]["uid"]] = ("R8", f"similaridade {S[i, j]:.2f} com {qs[j]['uid']}")
                vivos.discard(i)
        return poda

    def _similaridade(self, qs: list) -> np.ndarray:
        """Cosseno centrado dos embeddings da deduplicação (cache do dataset final v2); sem API, TF-IDF."""
        try:
            from .dedup import carregar_calibracao, centrar
            cal = carregar_calibracao(self.cal_arq)
            emb = self._embedder or C.embedder(cal["embedding"], self.origem)
            V = centrar(emb.encode([C.texto_questao(q) for q in qs]),
                        np.asarray(read_json(self.cal_arq.parent / cal["media"])))
            self.similaridade_teto = "embeddings (cosseno centrado)"
            return V @ V.T
        except Exception as exc:  # noqa: BLE001
            self.progress(f"[banco] sem embeddings ({type(exc).__name__}); teto por tópico com TF-IDF", flush=True)
            self.similaridade_teto = "TF-IDF"
            V = _tfidf([q["pergunta"] + " " + q["resposta"] for q in qs])
            return (V @ V.T).toarray()

    # ---------------------------------------------------------------- montagem e relatório
    def executar(self, revisar: bool = True) -> int:
        self.saida.mkdir(parents=True, exist_ok=True)
        poda = self.regras_locais()
        self._alvos = self.alvos_unicidade(poda)
        falhas = self.unicidade(poda) if revisar else 0
        poda, corr, pend = self.aplicar_unicidade(poda)
        poda = self.teto_topico(poda)
        self.gravar(poda, corr, pend)
        return 2 if falhas or (revisar and pend) else 0

    def _vereditos(self, u: str, corr: dict, cond: str) -> dict:
        v = {m: r[f"veredito_{cond}"] for m, r in self.vs[u].items()}
        return {**v, **corr.get(u, {}).get(cond, {})}

    def gravar(self, poda: dict, corr: dict, pend: int) -> dict:
        from pipeline.qa_research.piloto_janela.core import tema
        temas = {i: tema(i) for i in sorted({q["item"] for q in self.qs.values()})}
        ficam = sorted((q for u, q in self.qs.items() if u not in poda), key=lambda q: (q["item"], q["tipo"], q["uid"]))
        banco = []
        for k, q in enumerate(ficam, 1):
            u, r = q["uid"], self.rub.get(q["uid"], {})
            fech, aberto = self._vereditos(u, corr, "closed_book"), self._vereditos(u, corr, "open_book")
            banco.append({
                "id": f"PQ-{k:04d}", "uid": u, "item": q["item"], "area": temas[q["item"]]["area"],
                "tema": temas[q["item"]]["tema"], "tipo": q["tipo"], "cenario": q["cenario"],
                "pergunta": q["pergunta"], "resposta": q["resposta"], "explicacao": q.get("explicacao"),
                "resposta_padrao": q.get("resposta_padrao"), "por_que_nao": q.get("por_que_nao"),
                "contexto": q["contexto_tecnico"], "fonte": q["fonte"],
                "dificuldade": {"estrato": estrato({m: fech.get(m) for m in INDEPENDENTES}),
                                "rubrica": r.get("nivel"), "criterios_rubrica": r.get("criterios", []),
                                "sem_contexto": fech, "com_contexto": aberto,
                                "veredito_corrigido": {c: sorted(ms) for c, ms in corr.get(u, {}).items()}}})
        C.gravar_jsonl(self.saida / "banco.jsonl", banco)
        C.gravar_jsonl(self.saida / "poda.jsonl", [
            {"uid": u, "regra": k, "nome": REGRAS[k], "detalhe": d, "fonte": self.qs[u]["fonte"],
             "item": self.qs[u]["item"], "tipo": self.qs[u]["tipo"], "pergunta": self.qs[u]["pergunta"],
             "resposta": self.qs[u]["resposta"]} for u, (k, d) in sorted(poda.items(), key=lambda x: (x[1][0], x[0]))])
        res = self.resumo(banco, poda, corr, pend)
        atomic_json(self.saida / "resumo.json", res)
        (self.saida / "BANCO.md").write_text(_markdown(res), encoding="utf-8")
        self.progress(f"[banco] {res['n']} questões ({'provisório' if res['provisorio'] else 'final'}): "
                      f"{C.relativo(self.saida / 'BANCO.md')}", flush=True)
        return res

    def resumo(self, banco: list, poda: dict, corr: dict, pend: int) -> dict:
        n = len(banco)
        pct = lambda c, t: round(100 * c / t, 1) if t else None  # noqa: E731
        modelos = [m for m in ("gpt-4-1-mini", "gpt-4-1", "gpt-5-mini", "gpt-5", "gpt-5-4")
                   if all(m in b["dificuldade"]["sem_contexto"] for b in banco)]
        acc = {m: {c: pct(sum(b["dificuldade"][c][m] == "correta" for b in banco), n)
                   for c in ("sem_contexto", "com_contexto")} for m in modelos}
        est = Counter(b["dificuldade"]["estrato"] for b in banco)
        rub = Counter(b["dificuldade"]["rubrica"] for b in banco)
        por_topico = Counter(b["item"] for b in banco)
        alvos = getattr(self, "_alvos", None) or self.alvos_unicidade(self.regras_locais())
        revisadas = sum(1 for u in alvos if self._arq_u(u).exists())
        try:
            from .completo import DatasetCompleto
            div = DatasetCompleto(saida=self.origem, progress=lambda *a, **k: None).diversidade(
                [{**self.qs[b["uid"]]} for b in banco])
        except Exception as exc:  # noqa: BLE001
            div = {"erro": f"{type(exc).__name__}: {exc}"[:200]}
        return {
            "n": n, "de": len(self.qs), "provisorio": bool(pend) or revisadas == 0, "unicidade_pendente": pend,
            "unicidade_revisadas": revisadas, "vereditos_corrigidos": len(corr), "teto_topico": self.teto,
            "suspeitas_r1": len(self.suspeitas), "suspeitas_mantidas": getattr(self, "suspeitas_mantidas", 0),
            "similaridade_teto": self.similaridade_teto,
            "poda": {k: sum(1 for r, _ in poda.values() if r == k) for k in REGRAS},
            "poda_por_fonte": {f: dict(Counter(r for u, (r, _) in poda.items() if self.qs[u]["fonte"] == f))
                               for f in sorted({q["fonte"] for q in self.qs.values()})},
            "por_fonte": dict(Counter(b["fonte"] for b in banco).most_common()),
            "por_tipo": dict(Counter(b["tipo"] for b in banco).most_common()),
            "por_area": dict(Counter(b["area"] for b in banco).most_common()),
            "topicos": len(por_topico), "por_topico": dict(sorted(por_topico.items())),
            "topico_min_max": [min(por_topico.values()), max(por_topico.values())] if por_topico else None,
            "acuracia": acc, "estratos_pct": {e: pct(est.get(e, 0), n) for e in ESTRATOS},
            "rubrica_pct": {k: pct(rub.get(k, 0), n) for k in ("facil", "media", "dificil")},
            "dificil_por_tipo": {t: pct(sum(b["dificuldade"]["estrato"] in ("dificil", "muito_dificil") for b in bs),
                                        len(bs))
                                 for t in sorted({b["tipo"] for b in banco})
                                 for bs in [[b for b in banco if b["tipo"] == t]]},
            "palavras_pergunta": float(np.mean([len(b["pergunta"].split()) for b in banco])) if banco else None,
            "abertura_em_um_pct": pct(sum(bool(re.match(r"(em uma?|num|numa)\b", b["pergunta"], re.I))
                                          for b in banco), n),
            "com_cenario_pct": pct(sum(bool(b["cenario"]) for b in banco), n),
            **div}


NOMES = {"gpt-4-1-mini": "GPT-4.1 Mini", "gpt-4-1": "GPT-4.1", "gpt-5-mini": "GPT-5 mini", "gpt-5": "GPT-5",
         "gpt-5-4": "GPT-5.4 (referência)"}


def _markdown(r: dict) -> str:
    f = lambda v, c=1: "-" if v is None else f"{v:.{c}f}"  # noqa: E731
    out = [f"# Banco PetroQuest v1{' (PROVISÓRIO: revisão de unicidade pendente)' if r['provisorio'] else ''}", "",
           f"{r['n']} questões em {r['topicos']} tópicos, selecionadas de {r['de']} questões do dataset final v2 "
           f"(todas com gabarito totalmente sustentado pelo documento). Revisão de unicidade: {r['unicidade_revisadas']} "
           f"questões revisadas, {r['vereditos_corrigidos']} com veredito corrigido, {r['unicidade_pendente']} pendentes. "
           f"Das {r['suspeitas_r1']} que GPT-5 e GPT-5.4 erram mesmo com o documento, {r['suspeitas_mantidas']} ficaram "
           "(a pegadinha funcionou e o gabarito é único).",
           "", "## Poda", "", "| Regra | Motivo | Removidas |", "|---|---|---|"]
    out += [f"| {k} | {DESCRICAO[k]} | {v} |" for k, v in r["poda"].items()]
    out += ["", "## Composição", "", f"Por tipo: {r['por_tipo']}.", "", f"Por área: {r['por_area']}.", "",
            f"Por fonte: {r['por_fonte']}.", "",
            f"Questões por tópico: de {r['topico_min_max'][0]} a {r['topico_min_max'][1]} (teto {r['teto_topico']}; "
            f"redundância medida por {r.get('similaridade_teto') or '-'}).",
            "", "## Modelos (resposta de até 20 palavras)", "",
            "| Modelo | Sem contexto | Com contexto | Ganho com contexto |", "|---|---|---|---|"]
    for m, a in r["acuracia"].items():
        out.append(f"| {NOMES.get(m, m)} | {f(a['sem_contexto'])}% | {f(a['com_contexto'])}% | "
                   f"{f(a['com_contexto'] - a['sem_contexto'])} |")
    e, lx = r["estratos_pct"], r.get("lexical", {})
    out += ["", "## Dificuldade e forma", "", "| Métrica | Melhor | Referência | Valor |", "|---|---|---|---|",
            f"| Difícil para o GPT-5 (inclui muito difícil) | ↑ | > 15% | {f(e['dificil'] + e['muito_dificil'])}% |",
            f"| Nenhum modelo independente acerta | ↑ (se forem boas) | 5–15% | {f(e['muito_dificil'])}% |",
            f"| Fácil (todos os independentes acertam) | ↓ | < 40% | {f(e['facil'])}% |",
            f"| Rubrica do especialista: fácil / média / difícil | - | - | {f(r['rubrica_pct']['facil'])}% / "
            f"{f(r['rubrica_pct']['media'])}% / {f(r['rubrica_pct']['dificil'])}% |",
            f"| Max ROUGE-L pergunta ↔ frase do documento | ↓ | 0,15–0,40 | {f(lx.get('max_rougeL'), 3)} |",
            f"| Bigramas novos no gabarito | ↑ | > 30% | {f(lx.get('novel_2gram'))}% |",
            f"| Self-BLEU-4 no tópico | ↓ | < 0,25 | {f(lx.get('self_bleu4_por_topico'), 3)} |",
            f"| Vizinho mais próximo no tópico (cosseno centrado) | ↓ | < 0,50 | {f(r.get('vizinho_cosseno_centrado'), 3)} |",
            f"| Palavras no gabarito | ↓ | 3–15 | {f(lx.get('palavras_resposta'))} |",
            f"| Palavras na pergunta | - | - | {f(r['palavras_pergunta'])} |",
            f"| Perguntas que abrem com \"Em um/Num\" | ↓ | - | {f(r['abertura_em_um_pct'])}% |",
            f"| Perguntas com cenário | - | - | {f(r['com_cenario_pct'])}% |",
            "", f"Difícil para o GPT-5 por tipo: {r['dificil_por_tipo']}.", "",
            f"Por tópico: {r['por_topico']}.", "",
            "Estratos com os 4 modelos independentes (GPT-4.1 Mini, GPT-4.1, GPT-5 mini, GPT-5); o GPT-5.4 gerou as "
            "questões e é só referência. As faixas são referências de trabalho do projeto."]
    return "\n".join(out) + "\n"


def executar(revisar: bool = True, workers: int = 8, progress=print) -> int:
    return Banco(workers=workers, progress=progress).executar(revisar=revisar)
