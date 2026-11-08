"""Mapa 2D do vocabulário das questões da ablação (relatorios/ablacao_geracao_v1/figuras/figA5*).

Cada ponto é uma pergunta. As 1000 geradas por braço e as 1000 do banco final (as das vagas) entram num único
espaço lexical: TF-IDF das palavras de conteúdo (uni e bigramas), SVD com 100 dimensões e UMAP (cosseno) em 2D.
Pontos próximos usam vocabulário parecido; um braço que espalha pontos pelo mapa usa um vocabulário mais amplo.
Cobertura = fração dos hexágonos do mapa (ocupados por algum conjunto) que o conjunto ocupa; todos os conjuntos têm
1000 perguntas, então a cobertura é comparável.
"""
from __future__ import annotations

import json

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402
import numpy as np  # noqa: E402

from . import comum as C  # noqa: E402
from . import figuras as F  # noqa: E402
from .ablacao import SAIDA as ABL, conteudo  # noqa: E402
from .figuras_ablacao import SAIDA, _salvar  # noqa: E402

CONJ = ["naive", "documento", "sem_retro", "sem_externos", "completo", "banco"]
NOME = {"naive": "Naive", "documento": "Documento + regras", "sem_retro": "Sem retroalimentação",
        "sem_externos": "Sem datasets externos", "completo": "Pipeline completo", "banco": "Banco final"}
COR = {"naive": "#9c3d8f", "documento": "#6da7ec", "sem_retro": "#3987e5", "sem_externos": "#256abf",
       "completo": "#0d366b", "banco": F.LARANJA}


def textos() -> dict:
    out = {b: [q["pergunta"] for q in C.linhas(ABL / f"questoes_{b}.jsonl") if q.get("pergunta")]
           for b in CONJ if b != "banco"}
    out["banco"] = [v["ref_pergunta"] for v in C.linhas(ABL / "vagas.jsonl")]
    return out


def projetar(tx: dict, semente: int = 42) -> dict:
    from sklearn.decomposition import TruncatedSVD
    from sklearn.feature_extraction.text import TfidfVectorizer
    from sklearn.preprocessing import normalize
    import umap
    todos = [t for b in CONJ for t in tx[b]]
    vec = TfidfVectorizer(tokenizer=conteudo, lowercase=False, token_pattern=None, ngram_range=(1, 2), min_df=2,
                          sublinear_tf=True)
    X = vec.fit_transform(todos)
    Z = normalize(TruncatedSVD(100, random_state=semente).fit_transform(X))
    P = umap.UMAP(n_neighbors=30, min_dist=0.12, metric="cosine", random_state=semente).fit_transform(Z)
    out, k = {}, 0
    for b in CONJ:
        out[b] = P[k:k + len(tx[b])]
        k += len(tx[b])
    return out


HEX = 30   # hexágonos na largura do mapa


def _limites(P: dict):
    todos = np.vstack(list(P.values()))
    lo, hi = todos.min(0), todos.max(0)
    m = (hi - lo) * 0.03
    return (lo[0] - m[0], hi[0] + m[0], lo[1] - m[1], hi[1] + m[1])


def _contagens(ax, pts, ext, **kw):
    return ax.hexbin(pts[:, 0], pts[:, 1], gridsize=HEX, extent=ext, mincnt=1, linewidths=0.4, **kw)


def cobertura(P: dict) -> dict:
    """Fração dos hexágonos ocupados por algum conjunto que cada conjunto ocupa (mesma grade dos mapas)."""
    ext = _limites(P)
    fig, ax = plt.subplots()
    todos = _contagens(ax, np.vstack(list(P.values())), ext).get_offsets()
    total = {tuple(np.round(o, 6)) for o in todos}
    out = {}
    for b, pts in P.items():
        occ = {tuple(np.round(o, 6)) for o in _contagens(ax, pts, ext).get_offsets()}
        out[b] = 100 * len(occ & total) / len(total)
    plt.close(fig)
    return out


def _painel(ax, P, b, ext, cob, fonte=26):
    from matplotlib.colors import LinearSegmentedColormap
    from matplotlib.colors import ListedColormap
    # fundo: hexágonos ocupados por algum conjunto, todos no mesmo cinza
    _contagens(ax, np.vstack(list(P.values())), ext, cmap=ListedColormap(["#efeeea"]), edgecolors="white", zorder=1)
    from matplotlib.colors import to_rgb
    claro = tuple(0.68 + 0.32 * c for c in to_rgb(COR[b]))      # 1 pergunta no hexágono: tom claro da cor do conjunto
    cmap = LinearSegmentedColormap.from_list(b, [claro, COR[b]])
    h = _contagens(ax, P[b], ext, C=np.ones(len(P[b])), reduce_C_function=np.sum, cmap=cmap,
                   edgecolors="white", zorder=2)
    h.set_clim(1, 8)        # mesma escala em todos os painéis: 8 ou mais perguntas no hexágono = cor plena
    ax.set_xlim(ext[0], ext[1])
    ax.set_ylim(ext[2], ext[3])
    ax.set_xticks([])
    ax.set_yticks([])
    ax.set_aspect("equal")
    for lado in ax.spines.values():
        lado.set_visible(False)
    ax.text(0.5, 1.03, f"{NOME[b]}  ·  {cob[b]:.0f}%", transform=ax.transAxes, ha="center", va="bottom",
            fontsize=fonte, fontweight="semibold", color=COR[b])


def mapa_paineis(P: dict, cob: dict):
    ext = _limites(P)
    fig, axs = plt.subplots(2, 3, figsize=(21, 15))
    for ax, b in zip(axs.ravel(), CONJ):
        _painel(ax, P, b, ext, cob)
    fig.tight_layout(h_pad=3, w_pad=1.5)
    return _salvar(fig, "figA5_mapa_vocabulario")


def mapa_sobreposto(P: dict, cob: dict):
    """Naive x pipeline completo lado a lado, no mesmo mapa (hexágonos cinza = área ocupada por algum conjunto)."""
    ext = _limites(P)
    fig, axs = plt.subplots(1, 2, figsize=(20, 10.5))
    for ax, b in zip(axs, ("naive", "completo")):
        _painel(ax, P, b, ext, cob, fonte=30)
    fig.tight_layout(w_pad=2)
    return _salvar(fig, "figA5b_mapa_naive_completo")


def gerar() -> list:
    F.estilo()
    tx = textos()
    P = projetar(tx)
    cob = cobertura(P)
    (SAIDA / "mapa_cobertura.json").write_text(json.dumps({"hexagonos_na_largura": HEX, "cobertura_pct": cob,
                                                           "n": {b: len(tx[b]) for b in CONJ}}, indent=1))
    return mapa_paineis(P, cob) + mapa_sobreposto(P, cob)


if __name__ == "__main__":
    for p in gerar():
        print(p)
