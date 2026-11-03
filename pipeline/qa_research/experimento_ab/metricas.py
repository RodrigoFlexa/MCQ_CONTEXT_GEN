"""Métricas por braço e comparação 2x2 (documento x unidade). Offline, exceto embeddings não cacheados.

Efeitos reportados com IC de 95% por bootstrap (reamostragem de questões em cada braço):
  documento refinado - antigo: B-A (janela) e D-C (capítulo)
  capítulo - janela:            C-A (antigo) e D-B (refinado)
"""
from __future__ import annotations

import csv
import json
import math
import re
from collections import Counter, defaultdict
from pathlib import Path

import numpy as np

from pipeline.qa_research.piloto_janela.core import atomic_json, blocos, read_json

from . import comum as C

try:
    from spacy.lang.pt.stop_words import STOP_WORDS
except Exception:  # noqa: BLE001 - mesma família de métricas sem spaCy, registrada no resultado
    STOP_WORDS = set("a ao aos as até com como da das de do dos e é ela elas ele eles em entre era essa esse esta este "
                     "eu foi há isso isto já la lhe mais mas me mesmo muito na nas nem no nos o os ou para pela pelas "
                     "pelo pelos por qual quando que se sem ser seu seus sua suas só também te tem um uma umas uns".split())

EFEITOS = {"documento (janela): B-A": ("B", "A"), "documento (capítulo): D-C": ("D", "C"),
           "unidade (antigo): C-A": ("C", "A"), "unidade (refinado): D-B": ("D", "B")}
MODELOS = ("gpt-4-1-nano", "gpt-4-1-mini", "gpt-4-1")
B = 2000


# ------------------------------------------------------------------ texto
def tokens(s):
    return re.findall(r"[^\W\d_]+(?:[-’'][^\W\d_]+)*", s.lower(), re.UNICODE)


def content(s):
    return [t for t in tokens(s) if t not in STOP_WORDS]


def grams(t, n):
    return set(zip(*(t[i:] for i in range(n))))


def lcs(a, b):
    masks = {}
    for i, t in enumerate(a):
        masks[t] = masks.get(t, 0) | (1 << i)
    s = 0
    for t in b:
        x = masks.get(t, 0) | s
        s = x & ~(x - ((s << 1) | 1))
    return bin(s).count("1")


def rouge(a, b):
    return 2 * lcs(a, b) / (len(a) + len(b)) if a and b else 0.0


def self_bleu4(perguntas: list[str]) -> list[float]:
    """Sentence BLEU-4 de cada pergunta contra todas as outras do braço (mesma definição de calcular.py)."""
    qs = [tokens(q) for q in perguntas]
    if len(qs) < 2:
        return [float("nan")] * len(qs)
    tops, counts = [{} for _ in range(4)], []
    for ts in qs:
        cs = [Counter(zip(*(ts[i:] for i in range(n)))) for n in range(1, 5)]
        counts.append(cs)
        for n, c in enumerate(cs):
            for g, v in c.items():
                a, b, k = tops[n].get(g, (0, 0, 0))
                if v > a:
                    tops[n][g] = (v, a, 1)
                elif v == a:
                    tops[n][g] = (a, b, k + 1)
                elif v > b:
                    tops[n][g] = (a, v, k)
    lengths = Counter(map(len, qs))
    out = []
    for ts, cs in zip(qs, counts):
        length = max(1, len(ts))
        closest = min((n for n, k in lengths.items() if k - (n == len(ts)) > 0), key=lambda n: (abs(n - len(ts)), n))
        prec = []
        for i, c in enumerate(cs):
            num = 0
            for g, v in c.items():
                a, b, k = tops[i][g]
                num += min(v, b if v == a and k == 1 else a)
            prec.append((num if num else .1) / max(1, length - i))
        bp = 1 if length > closest else math.exp(1 - closest / length)
        out.append(bp * math.exp(sum(math.log(v) for v in prec) / 4))
    return out


# ------------------------------------------------------------------ estatística
def media(x):
    x = [v for v in x if v is not None and not (isinstance(v, float) and math.isnan(v))]
    return float(np.mean(x)) if x else None


def boot_diff(a, b, seed=0):
    """Diferença de médias (a - b) com IC 95% por bootstrap independente nos dois braços."""
    a = np.asarray([v for v in a if v is not None], float)
    b = np.asarray([v for v in b if v is not None], float)
    if not len(a) or not len(b):
        return None
    rng = np.random.default_rng(seed)
    d = rng.choice(a, (B, len(a))).mean(1) - rng.choice(b, (B, len(b))).mean(1)
    return {"diferenca": float(a.mean() - b.mean()), "ic95": [float(np.quantile(d, .025)), float(np.quantile(d, .975))]}


# ------------------------------------------------------------------ por braço
def _custo(pastas):
    out = defaultdict(lambda: {"chamadas": 0, "prompt_tokens": 0, "completion_tokens": 0})
    for pasta in pastas:
        for arq in Path(pasta).glob("**/chamadas/*.jsonl"):
            for l in arq.read_text(encoding="utf-8").splitlines():
                try:
                    r = json.loads(l)
                except ValueError:
                    continue
                if r.get("prompt_tokens") is None and r.get("completion_tokens") is None:
                    continue
                c = out[arq.stem]
                c["chamadas"] += 1
                c["prompt_tokens"] += r.get("prompt_tokens") or 0
                c["completion_tokens"] += r.get("completion_tokens") or 0
    tot = {k: sum(v[k] for v in out.values()) for k in ("chamadas", "prompt_tokens", "completion_tokens")}
    return {"total": tot, "por_papel": dict(out)}


def _posicao(bs):
    """Terço do bloco dentro do capítulo: inicio, meio ou fim (capítulo de 1 bloco: meio)."""
    por_cap = defaultdict(list)
    for b in bs:
        por_cap[b["capitulo"]].append(b["indice"])
    out = {}
    for idx in por_cap.values():
        for k, i in enumerate(idx):
            r = k / (len(idx) - 1) if len(idx) > 1 else .5
            out[i] = "inicio" if r < 1 / 3 else "fim" if r > 2 / 3 else "meio"
    return out


def metricas_braco(exp: Path, braco: str, embedder=None, media_vec=None) -> tuple[dict, list[dict]]:
    gdir, adir = Path(exp) / "bracos" / braco, Path(exp) / "avaliacao" / braco
    gcfg = read_json(gdir / "config.json")
    docs, unidade = C.resolver(gcfg["docs"]), gcfg["unidade"]
    todas = C.linhas(gdir / "questoes.jsonl")
    aprov = C.linhas(gdir / "aprovadas.jsonl")
    bs = {i: blocos(i, docs)[1] for i in gcfg["itens"]}
    res = {"braco": braco, "docs": C.BRACOS[braco.split("_")[0]]["docs"], "unidade": unidade,
           "gate_sustentacao": bool(gcfg.get("sustentacao")), "saturacao": bool(gcfg.get("saturacao"))}

    # geração
    aud = [q for q in todas if q.get("auditoria")]
    ok_aud = [q for q in aud if q["auditoria"]["referencia_valida"] and not q["auditoria"]["atalho"]]
    red = [q for q in todas if q.get("redundante")]
    dup = [q for q in todas if q.get("duplicada")]
    palavras = sum(C.palavras_documento(v) for v in bs.values())
    res["geracao"] = {
        "geradas": len(todas), "auditadas": len(aud), "aprovadas_auditor": len(ok_aud),
        "taxa_aprovacao_auditor": len(ok_aud) / max(1, len(aud)),
        "redundantes_semanticas": len(red), "duplicadas_lexicais": len(dup),
        "taxa_redundancia": (len(red) + len(dup)) / max(1, len(aprov) + len(red) + len(dup)),
        "aprovadas_finais": len(aprov), "palavras_documentos": palavras,
        "conhecimentos_por_1000_palavras": 1000 * len(aprov) / max(1, palavras),
        "por_origem": dict(Counter(q["origem"] for q in aprov)),
        "palavras_resposta_media": media([len(q["resposta"].split()) for q in aprov])}

    # cobertura
    cobertos, focos = set(), set()
    for q in aprov:
        if q.get("foco") is not None:
            cobertos.add((q["item"], q["foco"]))
            focos.add((q["item"], q["foco"]))
        for i in q.get("blocos") or []:
            cobertos.add((q["item"], i))
    total = [(i, b["indice"]) for i, v in bs.items() for b in v]
    pos = {(i, k): p for i, v in bs.items() for k, p in _posicao(v).items()}
    res["cobertura"] = {
        "blocos": len(total), "blocos_com_questao": sum(t in cobertos for t in total) / len(total),
        "blocos_foco_com_questao": sum(t in focos for t in total) / len(total),
        "foco_por_posicao_no_capitulo": {p: sum(t in focos for t in total if pos[t] == p) /
                                         max(1, sum(pos[t] == p for t in total)) for p in ("inicio", "meio", "fim")}}

    # integração (questões de foco com fundamentos)
    fund = [q for q in aprov if q.get("fundamentos")]
    res["integracao"] = {"questoes_com_fundamentos": len(fund),
                         "blocos_citados_media": media([len({f["bloco"] for f in q["fundamentos"]}) for q in fund]),
                         "usa_apoio": media([any(f["bloco"] != "F" for f in q["fundamentos"]) for q in fund])}

    por_q = {q["uid"]: {"braco": braco, "uid": q["uid"], "item": q["item"], "origem": q["origem"], "tipo": q["tipo"],
                        "rodada": q.get("rodada", 1),
                        "pergunta": q["pergunta"], "resposta": q["resposta"]} for q in aprov}

    # avaliação: sustentação e gap
    if (adir / "faithfulness.jsonl").exists():
        fs = {r["uid"]: r for r in C.linhas(adir / "faithfulness.jsonl")}
        for u, r in fs.items():
            if u in por_q and r.get("status") not in ("bloqueio_provedor", "inconclusivo"):
                por_q[u]["sustentado"] = float(r["status"] == "totalmente_sustentado")
                por_q[u]["fracao_afirmacoes_sustentadas"] = r.get("fracao_sustentada")
        res["sustentacao"] = {"status": dict(Counter(r.get("status") for r in fs.values())),
                              "taxa_totalmente_sustentadas": media([v.get("sustentado") for v in por_q.values()]),
                              "fracao_afirmacoes_sustentadas": media([v.get("fracao_afirmacoes_sustentadas") for v in por_q.values()]),
                              "por_origem": {o: media([v.get("sustentado") for v in por_q.values() if v["origem"] == o])
                                             for o in ("janela", "composta", "refinada")},
                              "rodadas_extras": media([v.get("sustentado") for v in por_q.values() if (v["rodada"] or 0) > 1])}
    if (adir / "pares.csv").exists():
        with (adir / "pares.csv").open(encoding="utf-8-sig") as f:
            for r in csv.DictReader(f):
                if r["uid"] in por_q and r["veredito_closed_book"] and r["veredito_open_book"]:
                    por_q[r["uid"]][f"closed_{r['modelo']}"] = float(r["veredito_closed_book"] == "correta")
                    por_q[r["uid"]][f"open_{r['modelo']}"] = float(r["veredito_open_book"] == "correta")
                    por_q[r["uid"]][f"gap_{r['modelo']}"] = (por_q[r["uid"]][f"open_{r['modelo']}"]
                                                            - por_q[r["uid"]][f"closed_{r['modelo']}"])
        res["acuracia"] = {m: {k: media([v.get(f"{k}_{m}") for v in por_q.values()]) for k in ("closed", "open", "gap")}
                           for m in MODELOS}

    # lexical (contra o contexto de avaliação: capítulos)
    if (adir / "contextos.jsonl").exists():
        ctx = {q["uid"]: q for q in C.linhas(adir / "contextos.jsonl")}
        for u, v in por_q.items():
            c = ctx.get(u)
            if not c:
                continue
            frases = [s for b in c["blocos_contexto"] for s in re.split(r"(?<=[.!?;])\s+|\n+", b["texto"]) if s.strip()]
            qt, at = content(v["pergunta"]), tokens(v["resposta"])
            v["max_rougeL"] = max((rouge(qt, content(s)) for s in frases), default=0.0)
            cts = [tokens(b["texto"]) for b in c["blocos_contexto"]]
            for n in (2, 3):
                ag = grams(at, n)
                cg = set().union(*(grams(t, n) for t in cts)) if cts else set()
                v[f"novel_{n}gram"] = 100 * len(ag - cg) / len(ag) if ag else None
    sb = self_bleu4([v["pergunta"] for v in por_q.values()])
    for v, s in zip(por_q.values(), sb):
        v["self_bleu4"] = s
    res["lexical"] = {k: media([v.get(k) for v in por_q.values()]) for k in ("max_rougeL", "novel_2gram", "novel_3gram", "self_bleu4")}

    # redundância semântica residual: vizinho mais próximo (cosseno centrado) no mesmo documento, após a deduplicação
    if embedder is not None and media_vec is not None and por_q:
        from .dedup import centrar
        lst = list(por_q.values())
        try:
            V = centrar(embedder.encode([C.texto_questao(v) for v in lst]), media_vec)
        except Exception as exc:  # noqa: BLE001 - sem API (ex.: máquina local): métrica fica ausente
            res["semantica"] = {"vizinho_cosseno_centrado_medio": None, "erro": f"{type(exc).__name__}: {exc}"[:300]}
        else:
            for k, v in enumerate(lst):
                mesmos = [j for j, w in enumerate(lst) if w["item"] == v["item"] and j != k]
                v["vizinho_cosseno_centrado"] = float(max(V[mesmos] @ V[k])) if mesmos else None
            res["semantica"] = {"vizinho_cosseno_centrado_medio": media([v.get("vizinho_cosseno_centrado") for v in lst])}

    resultado = read_json(gdir / "resultado.json") if (gdir / "resultado.json").exists() else {}
    res["dedup_incremental"] = resultado.get("dedup_incremental")
    res["checagem_sustentacao"] = resultado.get("sustentacao")
    if resultado.get("saturacao"):
        s = resultado["saturacao"]
        res["saturacao_resumo"] = {k: s[k] for k in ("conhecimentos_novos_por_rodada", "focos_por_numero_de_visitas")}
    res["custo"] = _custo([gdir, adir])
    res["stopwords"] = "spacy" if len(STOP_WORDS) > 200 else "lista_interna"
    return res, list(por_q.values())


# ------------------------------------------------------------------ comparação
def comparar(exp: Path, bracos=None, embedder=None, media_vec=None) -> dict:
    exp = Path(exp)
    res, por_q = {}, {}
    if bracos is None:   # A-D e, quando existirem, os braços derivados (X_sat, X_sust, X_sat_sust)
        bracos = list(C.BRACOS) + sorted(p.name for p in (exp / "bracos").glob("*_*") if p.is_dir())
    for b in bracos:
        if (exp / "bracos" / b / "aprovadas.jsonl").exists():
            res[b], por_q[b] = metricas_braco(exp, b, embedder, media_vec)
    variaveis = ["sustentado", "max_rougeL", "novel_2gram", "self_bleu4"] + \
                [f"{k}_{m}" for m in MODELOS for k in ("closed", "open", "gap")]
    efeitos = {}
    pares_efeito = dict(EFEITOS)
    for b in por_q:
        if "_" in b and b.rsplit("_", 1)[0] in por_q:
            origem, suf = b.rsplit("_", 1)
            nome = {"sust": "sustentação", "sat": "saturação"}[suf]
            pares_efeito[f"{nome}: {b}-{origem}"] = (b, origem)
    for nome, (x, y) in pares_efeito.items():
        if x in por_q and y in por_q:
            efeitos[nome] = {v: boot_diff([q.get(v) for q in por_q[x]], [q.get(v) for q in por_q[y]],
                                          seed=int(C.sha(nome + v)[:8], 16)) for v in variaveis}
    out = {"bracos": res, "efeitos": efeitos,
           "observacao": "IC 95% por bootstrap de questões; 3 documentos, então efeitos por documento devem ser lidos "
                         "junto (questões do mesmo documento não são independentes)."}
    atomic_json(exp / "comparacao.json", out)
    linhas = [r for b in por_q.values() for r in b]
    if linhas:
        campos = sorted({k for r in linhas for k in r}, key=lambda k: (k not in ("braco", "uid", "item", "origem"), k))
        with (exp / "por_questao.csv").open("w", encoding="utf-8-sig", newline="") as f:
            w = csv.DictWriter(f, fieldnames=campos, quoting=csv.QUOTE_ALL)
            w.writeheader()
            w.writerows(linhas)
    _markdown(exp, out)
    return out


def _f(v, pct=False, casas=1):
    if v is None:
        return "-"
    return f"{100 * v:.{casas}f}%" if pct else f"{v:.{casas if casas > 1 else 3}f}"


def _markdown(exp: Path, out: dict) -> None:
    r = out["bracos"]
    bs = list(r)
    cab = "| Métrica | " + " | ".join(f"{b} ({r[b]['docs']}, {r[b]['unidade']}{', sat.' if r[b].get('saturacao') else ''}"
                                     f"{', sust.' if r[b].get('gate_sustentacao') else ''})" for b in bs) + " |"
    sep = "|---|" + "---|" * len(bs)

    def linha(nome, fn):
        vals = []
        for b in bs:
            try:
                vals.append(fn(r[b]))
            except (KeyError, TypeError):
                vals.append("-")
        return f"| {nome} | " + " | ".join(vals) + " |"

    l = ["# Experimento A/B: documento refinado x antigo e capítulo x janela", "",
         "Mesmo gerador v21, mesmos 3 documentos (02_02, 03_03, 07_01), sem herança de rodadas anteriores, "
         "deduplicação incremental calibrada. Avaliação com o mesmo contexto em todos os braços (capítulos tocados "
         "pelo contexto de geração).", "", "## Por braço", "", cab, sep,
         linha("Aprovadas finais", lambda x: str(x["geracao"]["aprovadas_finais"])),
         linha("Aprovação do auditor", lambda x: _f(x["geracao"]["taxa_aprovacao_auditor"], True)),
         linha("Redundância removida", lambda x: _f(x["geracao"]["taxa_redundancia"], True)),
         linha("Conhecimentos por 1.000 palavras", lambda x: f"{x['geracao']['conhecimentos_por_1000_palavras']:.2f}"),
         linha("Conhecimentos novos por rodada (saturação)", lambda x: " / ".join(
             str(v) for v in x["saturacao_resumo"]["conhecimentos_novos_por_rodada"].values())),
         linha("Blocos com questão", lambda x: _f(x["cobertura"]["blocos_com_questao"], True)),
         linha("Foco coberto: início/meio/fim do capítulo", lambda x: " / ".join(
             _f(x["cobertura"]["foco_por_posicao_no_capitulo"][p], True, 0) for p in ("inicio", "meio", "fim"))),
         linha("Blocos citados por questão (janela)", lambda x: _f(x["integracao"]["blocos_citados_media"], casas=2)),
         linha("Palavras na resposta", lambda x: _f(x["geracao"]["palavras_resposta_media"], casas=1)),
         linha("**Gabaritos totalmente sustentados**", lambda x: _f(x["sustentacao"]["taxa_totalmente_sustentadas"], True)),
         linha("Afirmações sustentadas", lambda x: _f(x["sustentacao"]["fracao_afirmacoes_sustentadas"], True)),
         linha("Sustentados nas rodadas extras", lambda x: _f(x["sustentacao"]["rodadas_extras"], True))]
    for m in MODELOS:
        l.append(linha(f"{m}: sem / com contexto (gap)", lambda x, m=m: (
            f"{_f(x['acuracia'][m]['closed'], True)} / {_f(x['acuracia'][m]['open'], True)} "
            f"({_f(x['acuracia'][m]['gap'], True)})")))
    l += [linha("Max ROUGE-L pergunta-frase", lambda x: _f(x["lexical"]["max_rougeL"])),
          linha("Novel bigramas / trigramas", lambda x: f"{_f(x['lexical']['novel_2gram'], casas=1)} / "
                                                      f"{_f(x['lexical']['novel_3gram'], casas=1)}"),
          linha("Self-BLEU-4", lambda x: _f(x["lexical"]["self_bleu4"])),
          linha("Vizinho mais próximo (cosseno centrado)", lambda x: _f(x["semantica"]["vizinho_cosseno_centrado_medio"])),
          linha("Chamadas / tokens (mil)", lambda x: f"{x['custo']['total']['chamadas']} / "
                                                   f"{(x['custo']['total']['prompt_tokens'] + x['custo']['total']['completion_tokens']) / 1000:.0f}"),
          "", "## Efeitos (diferença e IC 95%)", "",
          "| Efeito | Sustentados | gap 4.1 Nano | gap 4.1 Mini | gap 4.1 | sem contexto 4.1 | Max ROUGE-L | Self-BLEU-4 |",
          "|---|---|---|---|---|---|---|---|"]

    def ef(d, pct=True):
        if not d:
            return "-"
        k = 100 if pct else 1
        return f"{k * d['diferenca']:+.1f} [{k * d['ic95'][0]:+.1f}; {k * d['ic95'][1]:+.1f}]" if pct else \
            f"{d['diferenca']:+.3f} [{d['ic95'][0]:+.3f}; {d['ic95'][1]:+.3f}]"

    for nome, e in out["efeitos"].items():
        l.append(f"| {nome} | {ef(e['sustentado'])} | {ef(e['gap_gpt-4-1-nano'])} | {ef(e['gap_gpt-4-1-mini'])} | "
                 f"{ef(e['gap_gpt-4-1'])} | {ef(e['closed_gpt-4-1'])} | {ef(e['max_rougeL'], False)} | "
                 f"{ef(e['self_bleu4'], False)} |")
    l += ["", "Proporções em pontos percentuais. " + out["observacao"]]
    (exp / "COMPARACAO.md").write_text("\n".join(l) + "\n", encoding="utf-8")
