"""Dataset final do PetroQuest: uma única coleção de questões válidas, avaliada uma única vez.

Etapas (cada uma retomável; repetir o comando continua de onde parou):
  1. montar: reúne as fontes válidas, na ordem de prioridade
       v23     -> experimento_ab_v1/bracos/B_v23 (se a geração estiver concluída)
       v22     -> experimento_ab_v1/bracos/B_v22
       antigo  -> banco_antigo_filtrado_v1 (geração final v19 com gabarito curto e auditor v23)
     remove as exclusões da revisão manual (exclusoes_revisao.json), sinaliza para o especialista a forma
     "por que X não basta/garante" e deduplica entre fontes, documento por documento, com a deduplicação calibrada do experimento;
  2. avaliar: mesmo protocolo do benchmark_gap (GPT-4.1 Nano/Mini/4.1, com e sem contexto, juiz GPT-5.4,
     sustentação por afirmação); o contexto de cada questão são os blocos que a geraram, no documento de origem;
  3. painel: GPT-5 mini e GPT-5.4 sem contexto (dificuldade empírica);
  4. relatorio: QUALIDADE.md, uma tabela com as métricas do dataset e a direção desejada de cada uma.
"""
from __future__ import annotations

import re
import shutil
import sqlite3
from collections import Counter
from pathlib import Path

import numpy as np

from pipeline.inventario.locking import output_lock
from pipeline.inventario.textutil import atomic_json
from pipeline.inventario.textutil import read_json as ler
from pipeline.qa_research.piloto_janela.core import DOCS, blocos, janela

from . import comum as C
from .dedup import DedupIncremental, carregar_calibracao, centrar
from .metricas import content, grams, rouge, self_bleu4, tokens

SAIDA = C.QA / "relatorios" / "petroquest_final_v1"
ANTIGO = C.QA / "relatorios" / "banco_antigo_filtrado_v1"
AVAL_ANTIGO = C.QA / "relatorios" / "benchmark_gap_antigo_filtrado_v1"
EXCLUSOES = Path(__file__).resolve().parent / "exclusoes_revisao.json"
# "Por que X não basta / não garante / não pode ser avaliado apenas por Y": princípio genérico (revisão manual)
NAO_BASTA = re.compile(r"\bn[aã]o (basta|garante|substitui)\b|\bn[aã]o (pode|deve)m? ser (avaliad|tratad|considerad|"
                       r"definid|presumid)\w* (apenas|s[oó])\b|\bvantagem autom[aá]tica\b", re.I)
CAMPOS = ("item", "tipo", "cenario", "composicao", "pergunta", "resposta", "explicacao", "resposta_padrao", "por_que_nao")


def fontes(exp: Path = C.EXPERIMENTO) -> list[dict]:
    """Fontes na ordem de prioridade (a primeira vence em caso de redundância, salvo substituição pelo juiz)."""
    refinado = C.docs_do_braco(exp, "B")
    return [{"nome": "v23", "pasta": exp / "bracos" / "B_v23", "marcador": "geracao_concluida.json", "docs": refinado,
             "obrigatoria": False},
            {"nome": "v22", "pasta": exp / "bracos" / "B_v22", "marcador": "geracao_concluida.json", "docs": refinado,
             "obrigatoria": True},
            {"nome": "antigo", "pasta": ANTIGO, "marcador": "filtro_concluido.json", "docs": DOCS, "obrigatoria": True}]


def contexto(q: dict, bs: list) -> list:
    if q.get("foco") is not None:
        return [b for _, b in janela(bs, q["foco"])]
    ids = q.get("blocos") or []
    if not ids or any(type(i) is not int or not 0 <= i < len(bs) for i in ids):
        raise ValueError(f"{q['uid']}: questão sem vínculo de contexto válido")
    return [bs[i] for i in ids]


def carregar(fonte: dict) -> list[dict]:
    cache, out = {}, []
    for q in C.linhas(Path(fonte["pasta"]) / "aprovadas.jsonl"):
        if q["item"] not in cache:
            cache[q["item"]] = blocos(q["item"], Path(fonte["docs"]))[1]
        sel = contexto(q, cache[q["item"]])
        out.append({"uid": f"{fonte['nome']}:{q['uid']}", "fonte": fonte["nome"], "uid_origem": q["uid"],
                    **{k: q.get(k) for k in CAMPOS}, "origem": q.get("origem"),
                    # mesmo texto do benchmark_gap: as respostas já cacheadas da avaliação de origem são reaproveitadas
                    "contexto_tecnico": "\n\n".join(f"{b['titulo_capitulo']} / {b['subtitulo']}\n{b['texto']}" for b in sel),
                    "blocos_contexto": [{"id": f"B{k}", "texto": b["texto"], "indice_documento": b["indice"]}
                                        for k, b in enumerate(sel, 1)]})
    return out


class DatasetFinal:
    def __init__(self, saida: Path = SAIDA, exp: Path = C.EXPERIMENTO, fontes_: list | None = None,
                 calibracao: Path | None = None, exclusoes: Path = EXCLUSOES, embedder=None, juiz=None,
                 progress=print):
        self.saida, self.exp = Path(saida), Path(exp)
        self.fontes = fontes_ if fontes_ is not None else fontes(self.exp)
        self.cal_arq = Path(calibracao or self.exp / "calibracao" / "calibracao.json")
        self.exclusoes = ler(Path(exclusoes))["exclusoes"]
        self._embedder, self._juiz, self.progress = embedder, juiz, progress

    # ---------------------------------------------------------------- 1. montar
    def _dedup(self) -> DedupIncremental:
        cal = carregar_calibracao(self.cal_arq)
        media = np.asarray(ler(self.cal_arq.parent / cal["media"]), dtype=float)
        emb = self._embedder or C.embedder(cal["embedding"], self.saida)
        juiz = self._juiz or C.cliente_llm(cal["juiz"], self.saida, "dedup_juiz")
        self._embedder = emb
        return DedupIncremental(self.saida / "dedup", emb, media, cal["limiar_auto"], cal["limiar_juiz"], juiz,
                                progress=self.progress)

    def montar(self) -> int:
        usadas, todas = [], []
        for f in self.fontes:
            pronta = (Path(f["pasta"]) / f["marcador"]).exists()
            if not pronta:
                if f["obrigatoria"]:
                    raise ValueError(f"Fonte {f['nome']} ainda não concluída: {C.relativo(Path(f['pasta']))}")
                self.progress(f"[final] fonte {f['nome']} ausente ou incompleta; segue sem ela", flush=True)
                continue
            qs = carregar(f)
            usadas.append({"nome": f["nome"], "pasta": C.relativo(Path(f["pasta"])), "questoes": len(qs)})
            todas += qs
        if len({q["uid"] for q in todas}) != len(todas):
            raise ValueError("UIDs repetidos entre fontes")
        excl = {q["uid"]: "revisão manual: " + self.exclusoes[q["uid"]] for q in todas if q["uid"] in self.exclusoes}
        for q in todas:
            # o padrão pega princípios genéricos, mas também questões técnicas boas ("por que mais MEG não basta"):
            # sinaliza para a revisão do especialista em vez de excluir
            q["sinalizar"] = "forma 'por que X não basta/garante'" if NAO_BASTA.search(q["pergunta"]) else None
        cands = [q for q in todas if q["uid"] not in excl]
        dd = self._dedup()
        from concurrent.futures import ThreadPoolExecutor
        with ThreadPoolExecutor(max_workers=8) as pool:      # tópicos são independentes
            falhas = sum(pool.map(lambda item: dd.processar(
                item, [q for q in cands if q["item"] == item],
                falha=lambda n, e: self.progress(f"[final] falha {n}: {e}", flush=True)),
                sorted({q["item"] for q in cands})))
        if falhas:
            self.progress(f"[final] {falhas} decisões de deduplicação falharam; repita o comando", flush=True)
            return falhas
        removidas = {}
        for item in {q["item"] for q in cands}:
            removidas.update(dd.redundantes(item))
        final = [q for q in cands if q["uid"] not in removidas]
        cfg_dataset = {"fontes": usadas, "n": len(final), "sha256": C.sha(final)}
        atual = ler(self.saida / "montagem.json")
        if atual and atual["dataset"]["sha256"] != cfg_dataset["sha256"] and (self.saida / "avaliacao").exists():
            raise ValueError("O dataset mudou desde a última avaliação (nova fonte, exclusão ou decisão). Apague "
                             f"{C.relativo(self.saida / 'avaliacao')} e {C.relativo(self.saida / 'painel')} para "
                             "reavaliar (as respostas já pagas continuam no cache copiado das fontes)")
        C.gravar_jsonl(self.saida / "dataset.jsonl", final)
        res = {"dataset": cfg_dataset,
               "por_fonte": {f["nome"]: {"reunidas": f["questoes"],
                                         "excluidas": sum(u.startswith(f["nome"] + ":") for u in excl),
                                         "redundantes": sum(u.startswith(f["nome"] + ":") for u in removidas),
                                         "finais": sum(q["fonte"] == f["nome"] for q in final)} for f in usadas},
               "exclusoes": excl, "redundantes": removidas,
               "sinalizadas_para_revisao": [q["uid"] for q in final if q["sinalizar"]]}
        atomic_json(self.saida / "montagem.json", res)
        self.progress(f"[final] dataset: {len(final)} questões | " + " | ".join(
            f"{k}: {v['finais']}/{v['reunidas']}" for k, v in res["por_fonte"].items()), flush=True)
        return 0

    # ---------------------------------------------------------------- 2. avaliar
    def _mesclar_cache(self, destino: Path, origens: list[Path]) -> None:
        """Junta os caches sqlite das avaliações de origem (mesma pergunta e contexto = mesma chamada, já paga)."""
        destino.mkdir(parents=True, exist_ok=True)
        for o in origens:
            for arq in sorted(Path(o).glob("*.sqlite3")) if Path(o).exists() else []:
                alvo = destino / arq.name
                if not alvo.exists():
                    shutil.copy2(arq, alvo)
                    continue
                with sqlite3.connect(alvo) as db:
                    db.execute("ATTACH DATABASE ? AS o", (str(arq),))
                    db.execute("INSERT OR IGNORE INTO cache SELECT * FROM o.cache")
                    db.commit()
                    db.execute("DETACH DATABASE o")

    def _origens_cache(self, sub: str) -> list[Path]:
        aval = {"v23": self.exp / "avaliacao" / "B_v23", "v22": self.exp / "avaliacao" / "B_v22", "antigo": AVAL_ANTIGO}
        return [aval[f["nome"]] / sub / ".local" for f in self.fontes if f["nome"] in aval]

    def avaliar(self, workers=8, judge_workers=2, mini="gpt-4-1-mini-petrobras", clientes=None) -> int:
        from pipeline.qa_research import benchmark_gap as G
        original = C.linhas(self.saida / "dataset.jsonl")
        rows = [{**q, "uid_original": q["uid"], "uid": arm + ":" + q["uid"], "condicao": arm,
                 "contexto_tecnico": q["contexto_tecnico"] if arm == "open_book" else None}
                for q in original for arm in G.ARMS]
        models = {**G.MODELS, "gpt-4-1-mini": mini}
        cfg = dict(schema="petroquest-final-avaliacao-v1", n=len(original), dados_sha256=C.sha(original),
                   questoes_sha256=C.sha(rows), modelos=models, juiz=G.Q.JUIZ, limite_palavras=100, lote_juiz=8,
                   contexto="blocos que geraram a questão, no documento de origem",
                   prompts={n: C.sha(G.prompt(n)) for n in ("respondente", "juiz", "faithfulness")})
        with output_lock(self.saida / "avaliacao"):
            old = ler(self.saida / "config.json")
            if old is not None and old != cfg:
                raise ValueError("Protocolo ou dataset mudou em relação à avaliação existente")
            if not (self.saida / "avaliacao" / ".local").exists() and clientes is None:
                self._mesclar_cache(self.saida / "avaliacao" / ".local", self._origens_cache("avaliacao"))
            atomic_json(self.saida / "config.json", cfg)
            G.Q.C.GeracaoSemConteudo.jsonl(self.saida / "questoes.jsonl", rows)
            G.Q.C.GeracaoSemConteudo.jsonl(self.saida / "contextos.jsonl", original)
            d = self.saida / "avaliacao"
            for m in models:
                for sub in ("respostas", "juiz"):
                    (d / sub / m).mkdir(parents=True, exist_ok=True)
            (d / "falhas").mkdir(exist_ok=True)
            marcador = self.saida / "rodada_concluida.json"
            marcador.unlink(missing_ok=True)
            e = G.AvaliacaoGap(self.saida, respondentes=models, juiz=G.Q.JUIZ, grupos=[tuple(models)], workers=workers,
                               judge_workers=judge_workers, lote_juiz=8, clientes=clientes, progress=self.progress)
            try:
                e.run()
                G.exportar_gap(self.saida, models)
                ok = all(len(e.vereditos[m]) == len(rows) for m in models) and G.faithfulness(e, original)
            finally:
                for c in e.clientes.values():
                    if hasattr(c, "close"):
                        c.close()
            if ok:
                atomic_json(marcador, {"status": "concluida", "questoes": len(original)})
            return 0 if ok else 2

    def painel(self, workers=8, judge_workers=2, clientes=None) -> int:
        from .painel import executar
        if not (self.saida / "painel" / "avaliacao" / ".local").exists() and clientes is None:
            self._mesclar_cache(self.saida / "painel" / "avaliacao" / ".local", self._origens_cache("painel/avaliacao"))
        return executar(self.saida, workers=workers, judge_workers=judge_workers, clientes=clientes,
                        progress=self.progress)

    # ---------------------------------------------------------------- 4. relatório
    def relatorio(self) -> dict:
        import csv
        qs = {q["uid"]: q for q in C.linhas(self.saida / "dataset.jsonl")}
        n = len(qs)
        media = lambda xs: float(np.mean([x for x in xs if x is not None])) if any(x is not None for x in xs) else None  # noqa: E731
        res: dict = {"n": n, "topicos": len({q["item"] for q in qs.values()}),
                     "por_fonte": dict(Counter(q["fonte"] for q in qs.values())),
                     "por_tipo": dict(Counter(q["tipo"] for q in qs.values())),
                     "por_topico": dict(sorted(Counter(q["item"] for q in qs.values()).items()))}
        fs = {r["uid"]: r for r in C.linhas(self.saida / "faithfulness.jsonl")} if (self.saida / "faithfulness.jsonl").exists() else {}
        res["sustentados"] = media([float(r.get("status") == "totalmente_sustentado") for r in fs.values()]) if fs else None
        res["afirmacoes_sustentadas"] = media([r.get("fracao_sustentada") for r in fs.values()]) if fs else None
        acc: dict = {}
        if (self.saida / "pares.csv").exists():
            with (self.saida / "pares.csv").open(encoding="utf-8-sig") as f:
                for r in csv.DictReader(f):
                    a = acc.setdefault(r["modelo"], {"closed": [], "closedp": [], "open": []})
                    a["closed"].append(float(r["veredito_closed_book"] == "correta"))
                    a["closedp"].append({"correta": 1.0, "parcial": .5}.get(r["veredito_closed_book"], 0.0))
                    a["open"].append(float(r["veredito_open_book"] == "correta"))
        res["acuracia"] = {m: {k: media(v) for k, v in a.items()} for m, a in acc.items()}
        res["painel"] = ler(self.saida / "painel" / "resumo.json")
        # não trivialidade e diversidade
        mr, n2, n3 = [], [], []
        for q in qs.values():
            frases = [s for b in q["blocos_contexto"] for s in re.split(r"(?<=[.!?;])\s+|\n+", b["texto"]) if s.strip()]
            qt = content(q["pergunta"])
            mr.append(max((rouge(qt, content(s)) for s in frases), default=0.0))
            at, cts = tokens(q["resposta"]), [tokens(b["texto"]) for b in q["blocos_contexto"]]
            for k, lst in ((2, n2), (3, n3)):
                ag, cg = grams(at, k), set().union(*(grams(t, k) for t in cts))
                if ag:
                    lst.append(100 * len(ag - cg) / len(ag))
        lst = list(qs.values())
        sb = []
        for item in {q["item"] for q in lst}:   # repetição dentro do mesmo tópico (independe do tamanho do dataset)
            grupo = [q["pergunta"] for q in lst if q["item"] == item]
            if len(grupo) > 1:
                sb += list(self_bleu4(grupo))
        res["lexical"] = {"max_rougeL": media(mr), "novel_2gram": media(n2), "novel_3gram": media(n3),
                          "self_bleu4_por_topico": media(sb),
                          "palavras_resposta": media([len(q["resposta"].split()) for q in lst])}
        try:
            cal = carregar_calibracao(self.cal_arq)
            emb = self._embedder or C.embedder(cal["embedding"], self.saida)
            V = centrar(emb.encode([C.texto_questao(q) for q in lst]), np.asarray(ler(self.cal_arq.parent / cal["media"])))
            viz = []
            for k, q in enumerate(lst):
                mesmos = [j for j, w in enumerate(lst) if w["item"] == q["item"] and j != k]
                if mesmos:
                    viz.append(float(max(V[mesmos] @ V[k])))
            res["vizinho_cosseno_centrado"] = media(viz)
        except Exception as exc:  # noqa: BLE001 - sem API: a métrica fica ausente
            res["vizinho_cosseno_centrado"] = None
            res["erro_embeddings"] = f"{type(exc).__name__}: {exc}"[:200]
        atomic_json(self.saida / "qualidade.json", res)
        (self.saida / "QUALIDADE.md").write_text(_markdown(res), encoding="utf-8")
        return res


def _p(v, pct=True, casas=1):
    return "-" if v is None else (f"{100 * v:.{casas}f}%" if pct else f"{v:.{casas}f}")


def _markdown(r: dict) -> str:
    a, p, lx = r.get("acuracia", {}), r.get("painel") or {}, r["lexical"]
    acc = lambda m, k: _p(a.get(m, {}).get(k))  # noqa: E731
    est = p.get("estratos_pct") or {}
    linhas = [
        ("Validade", "Gabaritos totalmente sustentados pelo contexto", "↑", "> 90%", _p(r["sustentados"])),
        ("Validade", "Afirmações do gabarito sustentadas", "↑", "> 95%", _p(r["afirmacoes_sustentadas"])),
        ("Dificuldade", "GPT-4.1 Nano sem contexto", "↓", "30–50%", acc("gpt-4-1-nano", "closed")),
        ("Dificuldade", "GPT-4.1 Mini sem contexto", "↓", "45–70%", acc("gpt-4-1-mini", "closed")),
        ("Dificuldade", "GPT-4.1 sem contexto", "↓", "50–75%", acc("gpt-4-1", "closed")),
        ("Dificuldade", "GPT-4.1 sem contexto, parcial = 0,5", "↓", "60–80%", acc("gpt-4-1", "closedp")),
        ("Dificuldade", "GPT-5 mini sem contexto", "↓", "< 80%",
         "-" if not p else f"{p['acuracia'].get('gpt-5-mini', 0):.1f}%"),
        ("Dificuldade", "GPT-5.4 sem contexto", "↓", "< 85%",
         "-" if not p else f"{p['acuracia'].get('gpt-5-4', 0):.1f}%"),
        ("Dificuldade", "Difícil para o GPT-5.4 (inclui muito difícil)", "↑", "> 15%",
         "-" if not est else f"{est['dificil'] + est['muito_dificil']:.1f}%"),
        ("Dificuldade", "Nenhum modelo acerta", "↑ (com questões boas)", "5–15%",
         "-" if not est else f"{est['muito_dificil']:.1f}%"),
        ("Contexto", "GPT-4.1 com contexto", "↑", "> 90%", acc("gpt-4-1", "open")),
        ("Contexto", "Gap do GPT-4.1 (com − sem contexto)", "↔ moderado", "5–20 pontos",
         "-" if "gpt-4-1" not in a else f"{100 * (a['gpt-4-1']['open'] - a['gpt-4-1']['closed']):.1f} pontos"),
        ("Não trivialidade", "Max ROUGE-L pergunta ↔ frase do contexto", "↓", "0,15–0,40", _p(lx["max_rougeL"], False, 3)),
        ("Não trivialidade", "Bigramas novos no gabarito", "↑", "> 30%",
         "-" if lx["novel_2gram"] is None else f"{lx['novel_2gram']:.1f}%"),
        ("Não trivialidade", "Trigramas novos no gabarito", "↑", "> 50%",
         "-" if lx["novel_3gram"] is None else f"{lx['novel_3gram']:.1f}%"),
        ("Diversidade", "Self-BLEU-4 entre perguntas do mesmo tópico", "↓", "< 0,25", _p(lx["self_bleu4_por_topico"], False, 3)),
        ("Diversidade", "Vizinho mais próximo no tópico (cosseno centrado)", "↓", "< 0,50",
         _p(r.get("vizinho_cosseno_centrado"), False, 3)),
        ("Forma", "Palavras no gabarito", "↓", "3–15", _p(lx["palavras_resposta"], False, 1)),
    ]
    tipos = r["por_tipo"]
    dp = (tipos.get("decisao", 0) + tipos.get("procedimento", 0)) / r["n"] if r["n"] else None
    linhas.append(("Cobertura", "Decisão + procedimento", "↑", "> 30%", _p(dp)))
    out = ["# PetroQuest: qualidade do dataset final", "",
           f"{r['n']} questões em {r['topicos']} tópicos. Por fonte: {r['por_fonte']}. Por tipo: {r['por_tipo']}.", "",
           "| Dimensão | Métrica | Melhor | Faixa de referência | Valor |", "|---|---|---|---|---|"]
    out += [f"| {d} | {m} | {s} | {f} | {v} |" for d, m, s, f, v in linhas]
    out += ["", "As faixas são referências de trabalho do projeto, não padrões da literatura. Acurácia baixa só é virtude "
            "quando a questão é válida: leia as linhas de dificuldade junto com a revisão manual.", "",
            f"Questões por tópico: {r['por_topico']}."]
    return "\n".join(out) + "\n"


def executar(exp: Path = C.EXPERIMENTO, workers=8, judge_workers=2, mini="gpt-4-1-mini-petrobras", progress=print) -> int:
    d = DatasetFinal(exp=exp, progress=progress)
    for etapa in (d.montar, lambda: d.avaliar(workers, judge_workers, mini), lambda: d.painel(workers, judge_workers)):
        st = etapa()
        if st:
            return 2
    d.relatorio()
    return 0
