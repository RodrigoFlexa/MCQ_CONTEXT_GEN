"""Similaridade e diversidade por campo (perguntas, respostas, perguntas + respostas) na ablação, no padrão das figuras
anteriores do projeto: histogramas em degrau sobrepostos (pares e questão mais próxima, TF-IDF e E5) e barras de
TTR e MATTR. Também refaz figS1 a figS3 como barras com IC de 95%.

Saída em relatorios/ablacao_geracao_v2/similaridade/ (CSVs) e .../similaridade/figuras/ (figS1 a figS3, figS6 a figS8).

python -m pipeline.qa_research.experimento_ab.campos_ablacao [pasta da ablação]
"""
from __future__ import annotations

import json
import math
import sys
from collections import defaultdict
from pathlib import Path

import matplotlib
import matplotlib.ticker
matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402
import numpy as np  # noqa: E402

from . import figuras as F  # noqa: E402
from .ablacao import SAIDA, mattr, tokens  # noqa: E402
from .similaridade_ablacao import CONJUNTOS, MODELO_E5, _csv, carregar  # noqa: E402

# Figuras: só a escada de componentes, cada configuração somando um componente à anterior (os CSV têm todos os braços).
ESCADA = ["naive", "regras", "documentos_regras", "sem_retro", "completo"]
NOME = {"naive": "Naive", "regras": "+ Regras", "documentos_regras": "+ Documentos (regras + documentos)",
        "sem_retro": "+ Datasets externos", "completo": "+ Retroalimentação (configuração do banco final)"}
CURTO = {"naive": "Naive", "regras": "+ Regras", "documentos_regras": "+ Documentos", "sem_retro": "+ Datasets\nexternos",
         "completo": "+ Retroali-\nmentação"}
COR = {"naive": "#1f77b4", "regras": "#ff7f0e", "documentos_regras": "#2ca02c", "sem_retro": "#9467bd",
       "completo": "#d62728"}

CAMPOS = {"perguntas": "Perguntas", "respostas": "Respostas", "perguntas_respostas": "Perguntas\n+ respostas"}
VIRG = matplotlib.ticker.FuncFormatter(lambda v, _: f"{v:g}".replace(".", ","))


def _texto(q: dict, campo: str) -> str:
    if campo == "perguntas":
        return q["pergunta"]
    if campo == "respostas":
        return q["resposta"]
    return f"{q['pergunta']} {q['resposta']}"


def vetores(qs: list[dict], campo: str, saida: Path) -> dict:
    """TF-IDF de palavras e E5 do campo, ajustados sobre todos os conjuntos juntos (como em similaridade_ablacao)."""
    from sklearn.feature_extraction.text import TfidfVectorizer
    from sklearn.preprocessing import normalize
    tx = [_texto(q, campo) for q in qs]
    V = {"tfidf": normalize(TfidfVectorizer(tokenizer=tokens, lowercase=False, token_pattern=None,
                                            ngram_range=(1, 2), min_df=2, sublinear_tf=True).fit_transform(tx))}
    cache = saida / ("embeddings_e5.npz" if campo == "perguntas" else f"embeddings_e5_{campo}.npz")
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


def _S(V, ks):
    S = V[ks] @ V[ks].T
    return np.asarray(S.todense() if hasattr(S, "todense") else S, dtype=np.float32)


BORDAS = {"tfidf": np.linspace(0, 1, 81), "e5": np.linspace(0.70, 1.0, 121)}            # pares (~500 mil)
BORDAS_NN = {"tfidf": np.linspace(0, 1, 51), "e5": np.linspace(0.84, 1.0, 41)}         # mais próxima (1000)


def similaridades(qs: list[dict], V: dict, campo: str):
    """Por conjunto: histograma (densidade) de todos os pares e similaridade de cada questão com a mais próxima."""
    idx = defaultdict(list)
    for k, q in enumerate(qs):
        idx[q["conjunto"]].append(k)
    hist, vizinho = [], []
    for b in CONJUNTOS:
        ks = np.array(idx[b])
        if not len(ks):
            continue
        for r in ("tfidf", "e5"):
            S = _S(V[r], ks)
            tri = S[np.triu_indices(len(ks), 1)]
            h, _ = np.histogram(np.clip(tri, BORDAS[r][0], BORDAS[r][-1]), BORDAS[r], density=True)
            np.fill_diagonal(S, -np.inf)
            nn = S.max(axis=1)
            hn, _ = np.histogram(np.clip(nn, BORDAS_NN[r][0], BORDAS_NN[r][-1]), BORDAS_NN[r], density=True)
            for tipo, hh, v, bb in (("pares", h, tri, BORDAS[r]), ("mais_proxima", hn, nn, BORDAS_NN[r])):
                hist.append({"campo": campo, "conjunto": b, "representacao": r, "medida": tipo, "n": len(v),
                             "media": float(v.mean()), "mediana": float(np.median(v)), "dp": float(v.std()),
                             "bordas": json.dumps([round(float(x), 4) for x in bb]),
                             "densidade": json.dumps([round(float(x), 5) for x in hh])})
            for k, s in zip(ks, nn):
                vizinho.append({"campo": campo, "conjunto": b, "uid": qs[k]["uid"], "representacao": r,
                                "mais_proxima": round(float(s), 4)})
    return hist, vizinho


def diversidade_campos(qs: list[dict]) -> list[dict]:
    """TTR e MATTR (100 palavras) do corpus de cada conjunto, por campo (em %), como nas figuras anteriores."""
    rng = np.random.default_rng(7)
    out = []
    por = defaultdict(list)
    for q in qs:
        por[q["conjunto"]].append(q)
    for b in CONJUNTOS:
        if b not in por:
            continue
        ordem = rng.permutation(len(por[b]))
        for c in CAMPOS:
            seq = [t for i in ordem for t in tokens(_texto(por[b][i], c))]
            out.append({"conjunto": b, "campo": c, "textos": len(por[b]), "tokens": len(seq), "tipos": len(set(seq)),
                        "ttr_pct": 100 * len(set(seq)) / len(seq), "mattr100_pct": 100 * mattr(seq, 100),
                        "mattr50_pct": 100 * mattr(seq, 50)})
    return out


# ------------------------------------------------------------------------------------------------- figuras
def _salvar(fig, pasta: Path, nome: str) -> list[Path]:
    pasta.mkdir(parents=True, exist_ok=True)
    out = [pasta / f"{nome}.png", pasta / f"{nome}.pdf"]
    for p in out:
        fig.savefig(p, facecolor="white")
    plt.close(fig)
    return out


def _degrau(ax, bordas, dens, cor, lw=2.4, tracejado=False):
    ax.stairs(dens, bordas, color=cor, linewidth=lw, linestyle="--" if tracejado else "-")


def _legenda(fig, conj, y=-0.01, ncol=3, fonte=19):
    alcas = [plt.Rectangle((0, 0), 1, 1, facecolor="white", edgecolor=COR[b], linewidth=2.6,
                           linestyle="--" if b == "banco" else "-") for b in conj]
    fig.legend(alcas, [NOME[b] for b in conj], loc="upper center", bbox_to_anchor=(0.5, y), ncol=ncol,
               fontsize=fonte, frameon=False, handlelength=1.6, columnspacing=1.6)


def _eixo(ax, xlabel, fonte=19):
    ax.set_xlabel(xlabel, fontsize=fonte + 1)
    ax.set_ylabel("Densidade", fontsize=fonte + 1)
    ax.tick_params(labelsize=fonte - 2)
    ax.xaxis.set_major_formatter(VIRG)
    ax.yaxis.grid(True, color=F.GRADE)
    ax.set_axisbelow(True)


def fig_similaridade(hist: list[dict], campo: str, pasta: Path, nome: str):
    """2x2: linhas = pares / questão mais próxima; colunas = TF-IDF (y log nos pares) / E5."""
    H = {(h["conjunto"], h["representacao"], h["medida"]): h for h in hist if h["campo"] == campo}
    conj = [b for b in ESCADA if (b, "e5", "pares") in H]
    fig, axs = plt.subplots(2, 2, figsize=(20, 13))
    for j, r in enumerate(("tfidf", "e5")):
        for i, (med, xl) in enumerate((("pares", "Similaridade entre pares"),
                                       ("mais_proxima", "Similaridade com a questão mais próxima"))):
            ax = axs[i, j]
            for b in conj:
                h = H[(b, r, med)]
                _degrau(ax, np.array(json.loads(h["bordas"])), np.array(json.loads(h["densidade"])), COR[b],
                        tracejado=b == "banco")
            _eixo(ax, xl)
            if r == "tfidf" and med == "pares":
                ax.set_yscale("log")
                ax.yaxis.set_major_formatter(matplotlib.ticker.LogFormatterMathtext())
            if r == "e5":
                ax.set_xlim(0.70 if med == "pares" else 0.84, 1.0)
            if i == 0:
                ax.set_title("TF-IDF" if r == "tfidf" else "E5", fontsize=24, pad=12)
    fig.tight_layout(h_pad=2.5, w_pad=3)
    _legenda(fig, conj)
    return _salvar(fig, pasta, nome)


def fig_perguntas_vs_pr(hist: list[dict], pasta: Path):
    """Questão mais próxima (E5): perguntas x perguntas + respostas."""
    fig, axs = plt.subplots(1, 2, figsize=(20, 7.5), sharey=False)
    conj = None
    for ax, campo, tit in zip(axs, ("perguntas", "perguntas_respostas"), ("Perguntas", "Perguntas + respostas")):
        H = {h["conjunto"]: h for h in hist if h["campo"] == campo and h["representacao"] == "e5"
             and h["medida"] == "mais_proxima"}
        conj = [b for b in ESCADA if b in H]
        for b in conj:
            _degrau(ax, np.array(json.loads(H[b]["bordas"])), np.array(json.loads(H[b]["densidade"])), COR[b],
                    tracejado=b == "banco")
        _eixo(ax, "Similaridade com a questão mais próxima")
        ax.set_xlim(0.84, 1.0)
        ax.set_title(tit, fontsize=24, pad=12)
    fig.tight_layout(w_pad=3)
    _legenda(fig, conj, y=0.0)
    return _salvar(fig, pasta, "figS7_mais_proxima_perguntas_vs_respostas")


def fig_ttr_mattr(div: list[dict], pasta: Path):
    D = {(d["conjunto"], d["campo"]): d for d in div}
    conj = [b for b in ESCADA if (b, "perguntas") in D]
    fig, axs = plt.subplots(1, 2, figsize=(24, 8.2))
    w = 0.8 / len(conj)
    x = np.arange(len(CAMPOS))
    for ax, chave, ylabel, tit in ((axs[0], "ttr_pct", "Diversidade lexical (%)", "TTR"),
                                   (axs[1], "mattr100_pct", "Diversidade lexical (%)", "MATTR · 100 palavras")):
        topo = 0
        for k, b in enumerate(conj):
            v = [D[(b, c)][chave] for c in CAMPOS]
            pos = x - 0.4 + w / 2 + k * w
            ax.bar(pos, v, w * 0.92, color=COR[b], zorder=2, hatch="//" if b == "banco" else None,
                   edgecolor="white" if b != "banco" else "#6b6a66", linewidth=0.6)
            topo = max(topo, max(v))
            for p, n in zip(pos, v):
                ax.text(p, n + topo * 0.012, f"{n:.1f}".replace(".", ","), ha="center", va="bottom", fontsize=15,
                        color=F.TINTA)
        ax.set_xticks(x, list(CAMPOS.values()), fontsize=20)
        ax.set_ylabel(ylabel, fontsize=20)
        ax.set_ylim(0, topo * 1.18)
        ax.tick_params(axis="y", labelsize=17)
        ax.tick_params(axis="x", length=0, pad=10)
        ax.yaxis.grid(True, color=F.GRADE)
        ax.set_axisbelow(True)
        ax.set_title(tit, fontsize=24, pad=12)
    fig.tight_layout(w_pad=3)
    alcas = [plt.Rectangle((0, 0), 1, 1, facecolor=COR[b], hatch="//" if b == "banco" else None,
                           edgecolor="white" if b != "banco" else "#6b6a66") for b in conj]
    fig.legend(alcas, [NOME[b] for b in conj], loc="upper center", bbox_to_anchor=(0.5, 0.0), ncol=3, fontsize=19,
               frameon=False, handlelength=1.4, columnspacing=1.6)
    return _salvar(fig, pasta, "figS8_ttr_mattr")


def _ic(v):
    v = np.asarray([x for x in v if x is not None and not (isinstance(x, float) and math.isnan(x))], dtype=float)
    m = v.mean()
    return m, 1.96 * v.std(ddof=1) / math.sqrt(len(v)), len(v)


def barras_ic(valores: dict, ylabel: str, pasta: Path, nome: str, ymin: float = 0.0, casas: int = 2):
    """Média com IC de 95% (média ± 1,96·dp/√n) por conjunto; ymin > 0 corta o eixo (dito no rótulo)."""
    conj = [b for b in ESCADA if len(valores.get(b, []))]
    est = {b: _ic(valores[b]) for b in conj}
    fig, ax = plt.subplots(figsize=(17, 7))
    x = np.arange(len(conj))
    m = np.array([est[b][0] for b in conj])
    e = np.array([est[b][1] for b in conj])
    ax.bar(x, m - ymin, 0.66, bottom=ymin, color=[COR[b] for b in conj], zorder=2,
           hatch=["//" if b == "banco" else None for b in conj],
           edgecolor=["#6b6a66" if b == "banco" else "white" for b in conj], linewidth=0.6)
    ax.errorbar(x, m, yerr=e, fmt="none", ecolor=F.TINTA2, elinewidth=1.8, capsize=7, zorder=3)
    topo = (m + e).max()
    alcance = topo - ymin
    for xi, mi, ei in zip(x, m, e):
        ax.text(xi, mi + ei + alcance * 0.02, f"{mi:.{casas}f}".replace(".", ","), ha="center", va="bottom",
                fontsize=19, fontweight="semibold", color=F.TINTA)
    ax.set_xticks(x, [CURTO[b] for b in conj], fontsize=20)
    for t, b in zip(ax.get_xticklabels(), conj):
        t.set_color(COR[b] if b != "banco" else F.TINTA2)
    ax.set_ylim(ymin, topo + alcance * 0.16)
    ax.set_ylabel(ylabel, fontsize=21)
    ax.yaxis.set_major_formatter(matplotlib.ticker.FuncFormatter(lambda v, _: f"{v:.{casas}f}".replace(".", ",")))
    ax.tick_params(axis="y", labelsize=18)
    ax.tick_params(axis="x", length=0, pad=10)
    ax.yaxis.grid(True, color=F.GRADE)
    ax.set_axisbelow(True)
    return _salvar(fig, pasta, nome)


def barras_antigas(saida: Path):
    """figS1, figS1b, figS2 e figS3 como barras com IC de 95% (substituem os boxplots)."""
    import pandas as pd
    q = pd.read_csv(saida / "questoes.csv")
    p = pd.read_csv(saida / "pares_mesmo_topico.csv.gz")
    pasta = saida / "figuras"
    g = lambda df, c: {b: df.loc[df.conjunto == b, c].dropna().tolist() for b in ESCADA}  # noqa: E731
    out = barras_ic(g(q, "nn_e5_topico"), "Similaridade com a mais parecida\ndo mesmo tópico (E5, cosseno)",
                    pasta, "figS1_vizinho_mais_proximo_e5", ymin=0.85, casas=3)
    out += barras_ic(g(q, "nn_tfidf_topico"), "Similaridade com a mais parecida\ndo mesmo tópico (TF-IDF, cosseno)",
                     pasta, "figS1b_vizinho_mais_proximo_tfidf")
    out += barras_ic(g(p, "cos_e5"), "Similaridade entre pares\ndo mesmo tópico (E5, cosseno)", pasta,
                     "figS2_pares_mesmo_topico_e5", ymin=0.80, casas=3)
    out += barras_ic(g(q, "self_bleu_topico"), "Self-BLEU da pergunta\n(contra o mesmo tópico)", pasta,
                     "figS3_self_bleu", casas=3)
    return out


def gerar(pasta: Path | None = None) -> Path:
    pasta = Path(pasta) if pasta else SAIDA
    saida = pasta / "similaridade"
    F.estilo()
    qs = carregar(pasta)
    hist, viz = [], []
    for campo in ("perguntas", "perguntas_respostas"):
        V = vetores(qs, campo, saida)
        h, v = similaridades(qs, V, campo)
        hist += h
        viz += v
        print(f"  {campo}", flush=True)
    div = diversidade_campos(qs)
    _csv(saida / "distribuicoes_por_campo.csv", hist)
    _csv(saida / "mais_proxima_por_campo.csv.gz", viz)
    _csv(saida / "diversidade_por_campo.csv", div)
    fig = saida / "figuras"
    fig_similaridade(hist, "perguntas", fig, "figS6_similaridade_perguntas")
    fig_similaridade(hist, "perguntas_respostas", fig, "figS6b_similaridade_perguntas_respostas")
    fig_perguntas_vs_pr(hist, fig)
    fig_ttr_mattr(div, fig)
    barras_antigas(saida)
    return saida


if __name__ == "__main__":
    print(gerar(sys.argv[1] if len(sys.argv) > 1 else None))
