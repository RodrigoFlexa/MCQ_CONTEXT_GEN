"""Dataset de similaridade e diversidade das perguntas da ablação (relatorios/ablacao_geracao_v2/similaridade/).

Conjuntos: as 1000 perguntas geradas por braço (coluna `aceita` marca as aceitas) e as 1000 do banco final nas mesmas
vagas. Três representações, todas com cosseno:
  tfidf  TF-IDF de palavras (uni e bigramas, todas as palavras), ajustado sobre todos os conjuntos juntos;
  char   TF-IDF de n-gramas de caracteres (3 a 5), robusto a flexão e grafia;
  e5     embedding semântico intfloat/multilingual-e5-base (local, prefixo "query: ").

Arquivos (ver LEIAME.md na pasta):
  questoes.csv                 uma linha por pergunta: vizinho mais próximo (no conjunto, no tópico, no banco),
                               similaridade média no tópico, densidade kNN, Self-BLEU da pergunta
  pares_mesmo_topico.csv.gz    todos os pares de perguntas do mesmo tópico dentro de cada conjunto
  pares_amostra.csv.gz         amostra de pares de qualquer tópico dentro de cada conjunto
  pares_distribuicao.csv       quantis e histograma de TODOS os pares de cada conjunto (499.500 por conjunto)
  entre_configuracoes.csv      para cada pergunta de A, a mais parecida em B (mesmo tópico e geral)
  entre_configuracoes_resumo.csv   médias e medianas por par de conjuntos
  diversidade.csv              TTR, MATTR, MTLD, HD-D, Yule K, Distinct-n, entropia, Self-BLEU, Vendi... por conjunto
  diversidade_por_topico.csv   as mesmas métricas por conjunto e tópico
  figuras/                     distribuições (figS1 a figS4)

python -m pipeline.qa_research.experimento_ab.similaridade_ablacao [pasta da ablação]
"""
from __future__ import annotations

import gzip
import json
import math
import random
import sys
import zlib
from collections import Counter, defaultdict
from pathlib import Path

import numpy as np

from . import comum as C
from .ablacao import SAIDA, conteudo, distinct, mattr, mtld, tokens, vendi

CONJUNTOS = ["naive", "documentos", "regras", "documentos_regras", "sem_retro", "sem_externos", "completo", "banco"]
NOME = {"naive": "Naive", "documentos": "Documentos", "regras": "Regras", "documentos_regras": "Documentos + regras",
        "sem_retro": "Sem retroalimentação", "sem_externos": "Sem datasets externos", "completo": "Pipeline completo",
        "banco": "Banco final"}
REPS = ("tfidf", "char", "e5")
MODELO_E5 = "intfloat/multilingual-e5-base"
K_DENS = 10          # densidade: média das K maiores similaridades
SEMENTE = 7


# ----------------------------------------------------------------------------------------------- dados
def carregar(pasta: Path) -> list[dict]:
    qs = []
    for b in CONJUNTOS[:-1]:
        arq = pasta / f"questoes_{b}.jsonl"
        if not arq.exists():
            continue
        for q in C.linhas(arq):
            if q.get("pergunta"):
                qs.append({"conjunto": b, "uid": q["uid"], "item": q["item"], "tipo": q.get("tipo", ""),
                           "aceita": bool(q.get("aceita")), "tentativa": q.get("tentativa"),
                           "pergunta": q["pergunta"], "resposta": q.get("resposta", "")})
    for v in C.linhas(pasta / "vagas.jsonl"):
        qs.append({"conjunto": "banco", "uid": v.get("ref_uid") or v["vaga"], "item": v["item"],
                   "tipo": v.get("tipo", ""), "aceita": True, "tentativa": None, "pergunta": v["ref_pergunta"],
                   "resposta": v.get("ref_resposta", "")})
    return qs


def vetores(qs: list[dict], saida: Path) -> dict:
    from sklearn.feature_extraction.text import TfidfVectorizer
    from sklearn.preprocessing import normalize
    tx = [q["pergunta"] for q in qs]
    V = {"tfidf": normalize(TfidfVectorizer(tokenizer=tokens, lowercase=False, token_pattern=None,
                                            ngram_range=(1, 2), min_df=2, sublinear_tf=True).fit_transform(tx)),
         "char": normalize(TfidfVectorizer(analyzer="char_wb", ngram_range=(3, 5), min_df=2,
                                           sublinear_tf=True).fit_transform(tx))}
    cache = saida / "embeddings_e5.npz"
    chave = np.array([q["conjunto"] + "|" + q["uid"] for q in qs])
    E = None
    if cache.exists():
        z = np.load(cache)
        if len(z["chave"]) == len(chave) and (z["chave"] == chave).all():
            E = z["E"].astype(np.float32)
    if E is None:
        from sentence_transformers import SentenceTransformer
        m = SentenceTransformer(MODELO_E5, device="cpu")
        E = m.encode(["query: " + t for t in tx], batch_size=64, normalize_embeddings=True,
                     show_progress_bar=True).astype(np.float32)
        np.savez_compressed(cache, E=E.astype(np.float16), chave=chave, modelo=MODELO_E5)
    V["e5"] = E / np.linalg.norm(E, axis=1, keepdims=True)
    return V


def _sim(V, a, b=None):
    A = V[a]
    B = A if b is None else V[b]
    S = A @ B.T
    return np.asarray(S.todense() if hasattr(S, "todense") else S, dtype=np.float32)


# ----------------------------------------------------------------------------------------------- BLEU
def _bleu(hip: list[str], refs: list[list[str]]) -> float:
    from nltk.translate.bleu_score import SmoothingFunction, sentence_bleu
    if not refs or not hip:
        return float("nan")
    return float(sentence_bleu(refs, hip, smoothing_function=SmoothingFunction().method1))


# ----------------------------------------------------------------------------------------------- por pergunta e pares
def por_pergunta_e_pares(qs: list[dict], V: dict, saida: Path):
    rng = np.random.default_rng(SEMENTE)
    idx = defaultdict(list)
    for k, q in enumerate(qs):
        idx[q["conjunto"]].append(k)
    banco = np.array(idx["banco"])
    linhas, pares, amostra, dist = [], [], [], []
    bordas = np.linspace(-0.2, 1.0, 121)
    toks = [tokens(q["pergunta"]) for q in qs]
    cont = [set(conteudo(q["pergunta"])) for q in qs]
    for b in CONJUNTOS:
        ks = np.array(idx[b])
        if not len(ks):
            continue
        itens = np.array([qs[k]["item"] for k in ks])
        S = {r: _sim(V[r], ks) for r in REPS}
        SB = {r: _sim(V[r], ks, banco) for r in REPS} if b != "banco" else None
        for r in REPS:
            np.fill_diagonal(S[r], -np.inf)
            tri = S[r][np.triu_indices(len(ks), 1)]
            q_ = np.quantile(tri, [0.01, 0.05, 0.25, 0.5, 0.75, 0.95, 0.99])
            h, _ = np.histogram(tri, bordas)
            dist.append({"conjunto": b, "representacao": r, "pares": len(tri), "media": float(tri.mean()),
                         "dp": float(tri.std()), **{f"q{int(p * 100):02d}": float(v) for p, v in
                                                     zip((0.01, 0.05, 0.25, 0.5, 0.75, 0.95, 0.99), q_)},
                         "histograma_bordas": json.dumps([round(float(x), 3) for x in bordas]),
                         "histograma_contagens": json.dumps(h.tolist())})
        # amostra de pares de qualquer tópico (5000 por conjunto)
        i_ = rng.integers(0, len(ks), 7000)
        j_ = rng.integers(0, len(ks), 7000)
        ok = i_ != j_
        for i, j in list(zip(i_[ok], j_[ok]))[:5000]:
            amostra.append({"conjunto": b, "uid_a": qs[ks[i]]["uid"], "uid_b": qs[ks[j]]["uid"],
                            "mesmo_topico": itens[i] == itens[j], **{f"cos_{r}": round(float(S[r][i, j]), 4)
                                                                    for r in REPS}})
        for a in range(len(ks)):
            q = qs[ks[a]]
            mt = np.where(itens == itens[a])[0]
            mt = mt[mt != a]
            lin = {k: q[k] for k in ("conjunto", "uid", "item", "tipo", "aceita", "tentativa")}
            lin["palavras"] = len(toks[ks[a]])
            for r in REPS:
                s = S[r][a]
                j = int(np.argmax(s))
                lin[f"nn_{r}_conjunto"] = round(float(s[j]), 4)
                lin[f"dens{K_DENS}_{r}_conjunto"] = round(float(np.sort(s)[-K_DENS:].mean()), 4)
                if r in ("tfidf", "e5"):
                    lin[f"nn_{r}_uid"] = qs[ks[j]]["uid"]
                if len(mt):
                    st = s[mt]
                    jt = int(np.argmax(st))
                    lin[f"nn_{r}_topico"] = round(float(st[jt]), 4)
                    lin[f"media_{r}_topico"] = round(float(st.mean()), 4)
                    if r == "e5":
                        lin["nn_e5_topico_uid"] = qs[ks[mt[jt]]]["uid"]
                        lin["nn_e5_topico_pergunta"] = qs[ks[mt[jt]]]["pergunta"]
                if SB is not None:
                    lin[f"nn_{r}_banco"] = round(float(SB[r][a].max()), 4)
            lin["self_bleu_topico"] = round(_bleu(toks[ks[a]], [toks[ks[m]] for m in mt]), 4) if len(mt) else None
            lin["pergunta"] = q["pergunta"]
            linhas.append(lin)
        # todos os pares do mesmo tópico
        for it in np.unique(itens):
            pos = np.where(itens == it)[0]
            for x in range(len(pos)):
                for y in range(x + 1, len(pos)):
                    i, j = pos[x], pos[y]
                    ta, tb = toks[ks[i]], toks[ks[j]]
                    ca, cb = cont[ks[i]], cont[ks[j]]
                    pares.append({"conjunto": b, "item": it, "uid_a": qs[ks[i]]["uid"], "uid_b": qs[ks[j]]["uid"],
                                  "aceitas_ambas": qs[ks[i]]["aceita"] and qs[ks[j]]["aceita"],
                                  **{f"cos_{r}": round(float(S[r][i, j]), 4) for r in REPS},
                                  "jaccard_conteudo": round(len(ca & cb) / len(ca | cb), 4) if ca | cb else None,
                                  "bleu4": round((_bleu(ta, [tb]) + _bleu(tb, [ta])) / 2, 4)})
        print(f"  {b}: {len(ks)} perguntas", flush=True)
    return linhas, pares, amostra, dist


def entre_configuracoes(qs: list[dict], V: dict):
    idx = defaultdict(list)
    for k, q in enumerate(qs):
        idx[q["conjunto"]].append(k)
    longo, resumo = [], []
    presentes = [b for b in CONJUNTOS if idx[b]]
    for a in presentes:
        ka = np.array(idx[a])
        ia = np.array([qs[k]["item"] for k in ka])
        for b in presentes:
            if a == b:
                continue
            kb = np.array(idx[b])
            ib = np.array([qs[k]["item"] for k in kb])
            reg = {}
            for r in REPS:
                S = _sim(V[r], ka, kb)
                geral = S.max(axis=1)
                mesmo = np.full(len(ka), np.nan, dtype=np.float32)
                for it in np.unique(ia):
                    m = ib == it
                    if m.any():
                        mesmo[ia == it] = S[np.ix_(ia == it, m)].max(axis=1)
                reg[r] = (geral, mesmo)
                ca = V[r][ka].mean(axis=0)
                cb = V[r][kb].mean(axis=0)
                ca, cb = np.asarray(ca).ravel(), np.asarray(cb).ravel()
                resumo.append({"conjunto_a": a, "conjunto_b": b, "representacao": r,
                               "nn_media_topico": float(np.nanmean(mesmo)), "nn_mediana_topico": float(np.nanmedian(mesmo)),
                               "nn_media_geral": float(geral.mean()), "cos_media_pares_topico": float(np.mean(
                                   [S[np.ix_(ia == it, ib == it)].mean() for it in np.unique(ia) if (ib == it).any()])),
                               "cos_centroides": float(ca @ cb / (np.linalg.norm(ca) * np.linalg.norm(cb)))})
            for n, k in enumerate(ka):
                longo.append({"conjunto_a": a, "conjunto_b": b, "uid": qs[k]["uid"], "item": qs[k]["item"],
                              **{f"nn_{r}_topico": round(float(reg[r][1][n]), 4) for r in REPS},
                              **{f"nn_{r}_geral": round(float(reg[r][0][n]), 4) for r in REPS}})
    return longo, resumo


# ----------------------------------------------------------------------------------------------- diversidade
def _hdd(toks: list[str], amostra: int = 42) -> float:
    """HD-D (McCarthy e Jarvis): soma, por tipo, da probabilidade de aparecer numa amostra de 42 tokens."""
    from scipy.stats import hypergeom
    n = len(toks)
    if n < amostra:
        return float("nan")
    return float(sum(1 - hypergeom.pmf(0, n, c, amostra) for c in Counter(toks).values()) / amostra)


def _yule_k(toks: list[str]) -> float:
    n = len(toks)
    if not n:
        return float("nan")
    vm = Counter(Counter(toks).values())
    return float(1e4 * (sum(m * m * v for m, v in vm.items()) - n) / (n * n))


def _entropia(toks: list[str]) -> float:
    c = np.array(list(Counter(toks).values()), dtype=float)
    p = c / c.sum()
    return float(-(p * np.log2(p)).sum())


def _self_bleu(listas: list[list[str]], max_n: int = 300, semente: int = SEMENTE) -> float:
    if len(listas) < 2:
        return float("nan")
    rng = random.Random(semente)
    alvo = range(len(listas)) if len(listas) <= max_n else rng.sample(range(len(listas)), max_n)
    return float(np.mean([_bleu(listas[i], listas[:i] + listas[i + 1:]) for i in alvo]))


def metricas(grupo: list[int], qs: list[dict], V: dict, toks: list, m_tokens: int | None, reps: int = 20) -> dict:
    if not grupo:
        return {"n": 0}
    rng = random.Random(SEMENTE)
    tx = [qs[k]["pergunta"] for k in grupo]
    ordem = rng.sample(grupo, len(grupo))
    seq = [t for k in ordem for t in toks[k]]
    out = {"n": len(grupo), "tokens": len(seq), "tipos": len(set(seq)), "ttr": len(set(seq)) / len(seq),
           "root_ttr_guiraud": len(set(seq)) / math.sqrt(len(seq)), "log_ttr_herdan": math.log(len(set(seq))) /
           math.log(len(seq)), "mattr_50": mattr(seq, 50), "mattr_100": mattr(seq, 100), "mtld": mtld(seq),
           "hdd": _hdd(seq), "yule_k": _yule_k(seq), "entropia_unigramas_bits": _entropia(seq),
           "distinct_1": distinct(tx, 1), "distinct_2": distinct(tx, 2), "distinct_3": distinct(tx, 3),
           "vocabulario_conteudo": len({t for k in grupo for t in conteudo(qs[k]["pergunta"])}),
           "palavras_media": float(np.mean([len(toks[k]) for k in grupo])),
           "compressao_gzip": len(zlib.compress("\n".join(tx).encode("utf-8"), 9)) / len("\n".join(tx).encode("utf-8"))}
    if m_tokens and len(seq) >= m_tokens:
        tt = []
        for _ in range(reps):
            i0 = rng.randrange(0, len(seq) - m_tokens + 1)
            tt.append(len(set(seq[i0:i0 + m_tokens])) / m_tokens)
        out[f"ttr_rarefeito_{m_tokens}_tokens"] = float(np.mean(tt))
    por_item = defaultdict(list)
    for k in grupo:
        por_item[qs[k]["item"]].append(k)
    out["self_bleu_conjunto"] = _self_bleu([toks[k] for k in grupo])
    sb = [_self_bleu([toks[k] for k in v]) for v in por_item.values() if len(v) >= 2]
    out["self_bleu_topico"] = float(np.nanmean(sb)) if sb else float("nan")
    for r in REPS:
        g = np.array(grupo)
        S = _sim(V[r], g)
        np.fill_diagonal(S, np.nan)
        out[f"cos_medio_{r}_conjunto"] = float(np.nanmean(S))
        out[f"nn_medio_{r}_conjunto"] = float(np.nanmax(S, axis=1).mean()) if len(g) > 1 else float("nan")
        cos_t, nn_t, ven = [], [], []
        for v in por_item.values():
            if len(v) >= 2:
                St = _sim(V[r], np.array(v))
                np.fill_diagonal(St, np.nan)
                cos_t.append(np.nanmean(St))
                nn_t.append(np.nanmax(St, axis=1).mean())
                if r == "e5":
                    ven.append(vendi(V[r][v]) / len(v))
        out[f"cos_medio_{r}_topico"] = float(np.mean(cos_t)) if cos_t else float("nan")
        out[f"nn_medio_{r}_topico"] = float(np.mean(nn_t)) if nn_t else float("nan")
        if r == "e5":
            out["vendi_e5_relativo_topico"] = float(np.mean(ven)) if ven else float("nan")
            out["vendi_e5_conjunto"] = vendi(V[r][g])
    return out


def diversidade(qs: list[dict], V: dict):
    toks = [tokens(q["pergunta"]) for q in qs]
    grupos = defaultdict(list)
    for k, q in enumerate(qs):
        grupos[(q["conjunto"], "geradas")].append(k)
        if q["aceita"]:
            grupos[(q["conjunto"], "aceitas")].append(k)
    m_ger = min(sum(len(toks[k]) for k in v) for (b, s), v in grupos.items() if s == "geradas")
    m_ace = min(sum(len(toks[k]) for k in v) for (b, s), v in grupos.items() if s == "aceitas")
    geral, topico = [], []
    for b in CONJUNTOS:
        for s, m in (("geradas", m_ger), ("aceitas", m_ace)):
            g = grupos.get((b, s), [])
            if b == "banco" and s == "aceitas":
                continue
            geral.append({"conjunto": b, "subconjunto": s if b != "banco" else "banco", **metricas(g, qs, V, toks, m)})
            if s == "geradas":
                por_item = defaultdict(list)
                for k in g:
                    por_item[qs[k]["item"]].append(k)
                for it, ks in sorted(por_item.items()):
                    topico.append({"conjunto": b, "item": it, **metricas(ks, qs, V, toks, None, reps=1)})
        print(f"  diversidade {b}", flush=True)
    return geral, topico


# ----------------------------------------------------------------------------------------------- figuras
COR = {"naive": "#1f77b4", "documentos": "#d62728", "regras": "#ff7f0e", "documentos_regras": "#2ca02c",
       "sem_retro": "#9467bd", "sem_externos": "#8c564b", "completo": "#111111", "banco": "#9a9994"}
CURTO = {"naive": "Naive", "documentos": "Docs.", "regras": "Regras", "documentos_regras": "Docs.\n+ regras",
         "sem_retro": "Sem\nretro", "sem_externos": "Sem\next.", "completo": "Comp.", "banco": "Banco"}


def figuras(linhas: list[dict], pares: list[dict], resumo: list[dict], saida: Path) -> list[Path]:
    import matplotlib
    import matplotlib.ticker
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    from . import figuras as F
    F.estilo()
    pasta = saida / "figuras"
    pasta.mkdir(parents=True, exist_ok=True)
    arqs = []

    def salvar(fig, nome):
        for ext in ("png", "pdf"):
            fig.savefig(pasta / f"{nome}.{ext}", facecolor="white")
            arqs.append(pasta / f"{nome}.{ext}")
        plt.close(fig)

    def violino(valores: dict, ylabel: str, nome: str, ylim=None):
        conj = [b for b in CONJUNTOS if len(valores.get(b, []))]
        fig, ax = plt.subplots(figsize=(17, 7))
        x = np.arange(len(conj))
        partes = ax.violinplot([valores[b] for b in conj], x, widths=0.8, showextrema=False)
        for pc, b in zip(partes["bodies"], conj):
            pc.set_facecolor(COR[b])
            pc.set_edgecolor(COR[b])
            pc.set_alpha(0.35)
        for xi, b in zip(x, conj):
            v = np.asarray(valores[b])
            q1, md, q3 = np.percentile(v, [25, 50, 75])
            ax.plot([xi, xi], [q1, q3], color=COR[b], linewidth=7, solid_capstyle="butt", zorder=3)
            ax.scatter([xi], [md], s=90, color="white", edgecolors=COR[b], linewidths=2.5, zorder=4)
            ax.text(xi + 0.12, md, f"{md:.2f}".replace(".", ","), va="center", fontsize=17, color=F.TINTA,
                    fontweight="semibold", zorder=5)
        ax.set_xticks(x, [CURTO[b] for b in conj], fontsize=20)
        for t, b in zip(ax.get_xticklabels(), conj):
            t.set_color(COR[b] if b != "banco" else F.TINTA2)
        ax.set_ylabel(ylabel, fontsize=21)
        ax.tick_params(axis="y", labelsize=18)
        ax.tick_params(axis="x", length=0, pad=10)
        if ylim:
            ax.set_ylim(*ylim)
        ax.yaxis.set_major_formatter(matplotlib.ticker.FuncFormatter(lambda y, _: f"{y:.2f}".replace(".", ",")))
        ax.yaxis.grid(True)
        ax.set_axisbelow(True)
        salvar(fig, nome)

    por = defaultdict(lambda: defaultdict(list))
    for l in linhas:
        for c in ("nn_e5_topico", "nn_tfidf_topico", "self_bleu_topico", "dens10_e5_conjunto"):
            if l.get(c) is not None and not (isinstance(l[c], float) and math.isnan(l[c])):
                por[c][l["conjunto"]].append(l[c])
    violino(por["nn_e5_topico"], "Similaridade com a mais parecida\ndo mesmo tópico (E5, cosseno)",
            "figS1_vizinho_mais_proximo_e5")
    violino(por["nn_tfidf_topico"], "Similaridade com a mais parecida\ndo mesmo tópico (TF-IDF, cosseno)",
            "figS1b_vizinho_mais_proximo_tfidf", (0, 1))
    pp = defaultdict(list)
    for p in pares:
        pp[p["conjunto"]].append(p["cos_e5"])
    violino(pp, "Similaridade entre pares\ndo mesmo tópico (E5, cosseno)", "figS2_pares_mesmo_topico_e5")
    violino(por["self_bleu_topico"], "Self-BLEU da pergunta\n(contra o mesmo tópico)", "figS3_self_bleu", (0, 1))
    # matriz entre configurações (E5, vizinho mais próximo no mesmo tópico, média)
    conj = [b for b in CONJUNTOS if any(r["conjunto_a"] == b for r in resumo)]
    M = np.full((len(conj), len(conj)), np.nan)
    for r in resumo:
        if r["representacao"] == "e5":
            M[conj.index(r["conjunto_a"]), conj.index(r["conjunto_b"])] = r["nn_media_topico"]
    fig, ax = plt.subplots(figsize=(15, 12.5))
    lo, hi = np.nanmin(M), np.nanmax(M)
    im = ax.imshow(M, cmap="Blues", vmin=lo - 0.02, vmax=hi)
    for i in range(len(conj)):
        for j in range(len(conj)):
            if i != j:
                ax.text(j, i, f"{M[i, j]:.2f}".replace(".", ","), ha="center", va="center", fontsize=19,
                        fontweight="semibold", color="white" if M[i, j] > (lo + hi) / 2 else F.TINTA)
            else:
                ax.add_patch(plt.Rectangle((j - 0.5, i - 0.5), 1, 1, color="white"))
    ax.set_xticks(range(len(conj)), [CURTO[b] for b in conj], fontsize=19)
    ax.set_yticks(range(len(conj)), [CURTO[b] for b in conj], fontsize=19)
    ax.set_xlabel("Conjunto onde se busca a mais parecida", fontsize=20, labelpad=12)
    ax.set_ylabel("Pergunta de origem", fontsize=20, labelpad=12)
    ax.tick_params(length=0)
    for s in ax.spines.values():
        s.set_visible(False)
    cb = fig.colorbar(im, ax=ax, fraction=0.045, pad=0.03)
    cb.ax.tick_params(labelsize=17)
    cb.ax.yaxis.set_major_formatter(matplotlib.ticker.FuncFormatter(lambda y, _: f"{y:.2f}".replace(".", ",")))
    cb.outline.set_visible(False)
    salvar(fig, "figS4_entre_configuracoes_e5")
    return arqs


# ----------------------------------------------------------------------------------------------- saída
def _csv(caminho: Path, linhas: list[dict]) -> None:
    import csv
    campos = list(dict.fromkeys(k for l in linhas for k in l))
    abrir = gzip.open if caminho.suffix == ".gz" else open
    with abrir(caminho, "wt", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, campos)
        w.writeheader()
        for l in linhas:
            w.writerow({k: (round(v, 6) if isinstance(v, float) else v) for k, v in l.items()})


LEIAME = """# Similaridade e diversidade das perguntas da ablação

Gerado por `python -m pipeline.qa_research.experimento_ab.similaridade_ablacao`.

Conjuntos: as 1000 perguntas geradas de cada braço (coluna `aceita` = passou no auditor, na resposta de até 20 palavras,
na sustentação e no dedup) e as 1000 do banco final nas mesmas vagas (`banco`). Só a pergunta entra nas similaridades.

Representações (cosseno): `tfidf` = TF-IDF de palavras, uni e bigramas, todas as palavras, ajustado em todos os
conjuntos juntos; `char` = TF-IDF de n-gramas de caracteres 3 a 5; `e5` = embedding `{modelo}` (local, prefixo
"query: "; vetores em `embeddings_e5.npz`, float16). Os embeddings 3-large do dedup não estão no repositório.

## Arquivos

- `questoes.csv`: uma linha por pergunta.
  - `nn_<rep>_conjunto`: similaridade com a pergunta mais parecida do mesmo conjunto (qualquer tópico);
    `nn_<rep>_uid` diz qual é.
  - `nn_<rep>_topico` / `media_<rep>_topico`: a mais parecida e a média, só entre as do mesmo tópico.
    `nn_e5_topico_pergunta` traz o texto da mais parecida.
  - `dens10_<rep>_conjunto`: densidade local = média das 10 maiores similaridades no conjunto.
  - `nn_<rep>_banco`: a mais parecida entre as 1000 do banco (vazia para o próprio banco).
  - `self_bleu_topico`: BLEU-4 (suavizado) da pergunta contra as outras do mesmo conjunto e tópico.
- `pares_mesmo_topico.csv.gz`: todos os pares do mesmo tópico dentro de cada conjunto: cossenos nas três
  representações, Jaccard das palavras de conteúdo e BLEU-4 simétrico (média dos dois sentidos).
- `pares_amostra.csv.gz`: 5000 pares sorteados por conjunto, de qualquer tópico (`mesmo_topico` marca).
- `pares_distribuicao.csv`: TODOS os 499.500 pares de cada conjunto: média, desvio, quantis e histograma
  (bordas de -0,2 a 1,0 em passos de 0,01, em JSON).
- `entre_configuracoes.csv`: para cada pergunta do conjunto A, a similaridade com a mais parecida do conjunto B
  no mesmo tópico (`nn_<rep>_topico`) e em qualquer tópico (`nn_<rep>_geral`).
- `entre_configuracoes_resumo.csv`: por par (A, B) e representação: média e mediana do vizinho no tópico, média do
  vizinho geral, cosseno médio dos pares do mesmo tópico e cosseno entre os centroides.
- `diversidade.csv`: por conjunto, para as geradas e as aceitas: TTR, TTR rarefeito (mesmo número de tokens para
  todos: o menor conjunto), Guiraud, Herdan, MATTR (janelas 50 e 100), MTLD, HD-D, Yule K, entropia de unigramas,
  Distinct-1/2/3, vocabulário de conteúdo, taxa de compressão gzip, Self-BLEU (conjunto, até 300 perguntas
  sorteadas, e por tópico), cosseno médio e vizinho mais próximo médio (conjunto e tópico) e Vendi (E5).
- `diversidade_por_topico.csv`: as mesmas métricas por conjunto e tópico (geradas).
- `figuras/`: figS1 (vizinho mais próximo no tópico, E5 e TF-IDF), figS2 (pares do mesmo tópico, E5),
  figS3 (Self-BLEU), figS4 (matriz entre configurações, E5).

## Leitura

Similaridade maior = perguntas mais parecidas = menos diversidade. Self-BLEU, cosseno médio, vizinho mais próximo,
Yule K e compressão: menor = mais variado. TTR, MATTR, MTLD, HD-D, entropia, Distinct e Vendi: maior = mais variado.
TTR bruto depende do tamanho do texto: compare o rarefeito, MATTR, MTLD ou HD-D. Naive e regras têm poucas aceitas
(23 e 31): as métricas das aceitas desses braços são frágeis.
"""


def gerar(pasta: Path | None = None) -> Path:
    pasta = Path(pasta) if pasta else SAIDA
    saida = pasta / "similaridade"
    saida.mkdir(parents=True, exist_ok=True)
    qs = carregar(pasta)
    print(f"{len(qs)} perguntas", flush=True)
    V = vetores(qs, saida)
    linhas, pares, amostra, dist = por_pergunta_e_pares(qs, V, saida)
    _csv(saida / "questoes.csv", linhas)
    _csv(saida / "pares_mesmo_topico.csv.gz", pares)
    _csv(saida / "pares_amostra.csv.gz", amostra)
    _csv(saida / "pares_distribuicao.csv", dist)
    longo, resumo = entre_configuracoes(qs, V)
    _csv(saida / "entre_configuracoes.csv", longo)
    _csv(saida / "entre_configuracoes_resumo.csv", resumo)
    geral, topico = diversidade(qs, V)
    _csv(saida / "diversidade.csv", geral)
    _csv(saida / "diversidade_por_topico.csv", topico)
    figuras(linhas, pares, resumo, saida)
    (saida / "LEIAME.md").write_text(LEIAME.replace("{modelo}", MODELO_E5), encoding="utf-8")
    return saida


def so_figuras(pasta: Path | None = None) -> list[Path]:
    """Refaz as figuras a partir dos CSV já gerados."""
    import pandas as pd
    saida = (Path(pasta) if pasta else SAIDA) / "similaridade"
    linhas = pd.read_csv(saida / "questoes.csv").to_dict("records")
    pares = pd.read_csv(saida / "pares_mesmo_topico.csv.gz").to_dict("records")
    resumo = pd.read_csv(saida / "entre_configuracoes_resumo.csv").to_dict("records")
    return figuras(linhas, pares, resumo, saida)


if __name__ == "__main__":
    if "--figuras" in sys.argv:
        so_figuras(next((a for a in sys.argv[1:] if not a.startswith("--")), None))
    else:
        print(gerar(sys.argv[1] if len(sys.argv) > 1 else None))
