"""Dispersão 2D das perguntas da ablação com uma cor por braço (figA7*), para comparar os braços no mesmo mapa.

Tratamento dos dados: todos os conjuntos cobrem os mesmos 40 tópicos, e o tópico domina o vocabulário. Para que o mapa
mostre como cada braço escreve, e não de que tópico fala:
1. cada pergunta vira um vetor TF-IDF de todas as palavras (uni a trigramas, inclui palavras de função, que carregam
   o estilo), reduzido por SVD (100 dim.);
2. desse vetor sai a média do seu tópico (calculada sobre todos os conjuntos): fica o resíduo, normalizado;
3. junta-se um bloco pequeno de traços de forma, padronizados: tamanho (log de palavras), tamanho médio da palavra,
   vírgulas, números, parênteses, siglas/nomes próprios, frases internas e a palavra de abertura (Qual, Como...);
4. UMAP (cosseno) em 2D.
Contornos: região com 50% das perguntas de cada braço (densidade por kernel). Marcadores grandes: centro de cada braço.
figA7c: quão distinguíveis são dois braços (kNN no espaço do passo 3, validação cruzada): 50% = indistinguíveis.

python -m pipeline.qa_research.experimento_ab.dispersao_ablacao [pasta da ablação]   (padrão: v2 se existir, senão v1)
"""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402
import numpy as np  # noqa: E402

from . import comum as C  # noqa: E402
from . import figuras as F  # noqa: E402
from .ablacao import SAIDA, SAIDA_V1  # noqa: E402

ORDEM = ["naive", "documentos", "regras", "documentos_regras", "documento", "sem_retro", "sem_externos", "completo",
         "banco"]
NOME = {"naive": "Naive", "documentos": "Documentos", "regras": "Regras", "documentos_regras": "Documentos + regras",
        "documento": "Documento + regras", "sem_retro": "Sem retroalimentação", "sem_externos": "Sem datasets externos",
        "completo": "Pipeline completo", "banco": "Banco final"}
COR = {"naive": "#1f77b4", "documentos": "#d62728", "regras": "#ff7f0e", "documentos_regras": "#2ca02c",
       "documento": "#2ca02c", "sem_retro": "#9467bd", "sem_externos": "#8c564b", "completo": "#111111",
       "banco": "#9a9994"}


def carregar(pasta: Path) -> dict:
    """{conjunto: [(item, pergunta)]} com as perguntas geradas de cada braço e as do banco nas mesmas vagas."""
    out = {}
    for b in ORDEM:
        arq = pasta / f"questoes_{b}.jsonl"
        if arq.exists():
            out[b] = [(q["item"], q["pergunta"]) for q in C.linhas(arq) if q.get("pergunta")]
    out["banco"] = [(v["item"], v["ref_pergunta"]) for v in C.linhas(pasta / "vagas.jsonl")]
    return out


ABERTURAS = ("qual", "quais", "como", "por que", "o que", "em que", "quando", "quanto", "que", "onde", "durante",
             "considerando", "em uma", "em um", "um", "uma", "ao", "se", "no", "na", "para")
PESO_FORMA = 0.15     # peso do bloco de forma frente ao resíduo lexical (norma 1)


def forma(t: str) -> list:
    """Traços de forma de uma pergunta (independem do tópico)."""
    w = t.split() or [""]
    tl = t.lower()
    return ([np.log(len(w)), np.mean([len(x) for x in w]), t.count(",") / len(w), bool(re.search(r"\d", t)),
             "(" in t, sum(x[:1].isupper() for x in w[1:]) / len(w), len(re.findall(r"[.;:]", t[:-1]))]
            + [tl.startswith(a + " ") for a in ABERTURAS])


def espaco(dados: dict, semente: int = 42) -> np.ndarray:
    """Vetores das perguntas (passos 1 a 3 do tratamento), na ordem de `dados`."""
    from sklearn.decomposition import TruncatedSVD
    from sklearn.feature_extraction.text import TfidfVectorizer
    from sklearn.preprocessing import StandardScaler, normalize
    itens = np.array([i for b in dados for i, _ in dados[b]])
    textos = [t for b in dados for _, t in dados[b]]
    X = TfidfVectorizer(ngram_range=(1, 3), min_df=2, sublinear_tf=True).fit_transform(textos)
    Z = normalize(TruncatedSVD(100, random_state=semente).fit_transform(X))
    for i in np.unique(itens):                       # tira o tópico: resíduo em torno da média do tópico
        m = itens == i
        Z[m] -= Z[m].mean(axis=0)
    S = StandardScaler().fit_transform(np.array([forma(t) for t in textos], dtype=float))
    return np.hstack([normalize(Z), PESO_FORMA * S])


def projetar(dados: dict, semente: int = 42) -> tuple:
    import umap
    Z = espaco(dados, semente)
    P = umap.UMAP(n_neighbors=60, min_dist=0.5, metric="cosine", random_state=semente).fit_transform(Z)
    out, k = {}, 0
    for b in dados:
        out[b] = P[k:k + len(dados[b])]
        k += len(dados[b])
    return out, Z


AMOSTRA = 350   # pontos por braço no gráfico único


def _contorno(ax, pts, cor, ext, nivel=0.5, lw=3.0, preencher=False, alfa=0.12):
    """Contorno da região de maior densidade que contém `nivel` dos pontos (KDE gaussiano)."""
    from scipy.stats import gaussian_kde
    kde = gaussian_kde(pts.T, bw_method=0.25)
    xs, ys = np.meshgrid(np.linspace(ext[0], ext[1], 160), np.linspace(ext[2], ext[3], 160))
    dens = kde(np.vstack([xs.ravel(), ys.ravel()])).reshape(xs.shape)
    corte = np.quantile(kde(pts.T), 1 - nivel)            # densidade acima da qual estão `nivel` dos pontos
    if preencher:
        ax.contourf(xs, ys, dens, levels=[corte, dens.max()], colors=[cor], alpha=alfa, zorder=1)
    ax.contour(xs, ys, dens, levels=[corte], colors=[cor], linewidths=lw, zorder=4)


def _limites(P, corte=2.0, margem=0.06):
    todos = np.vstack(list(P.values()))
    lo, hi = np.percentile(todos, corte, axis=0), np.percentile(todos, 100 - corte, axis=0)
    m = (hi - lo) * margem
    return (lo[0] - m[0], hi[0] + m[0], lo[1] - m[1], hi[1] + m[1])


def _limpo(ax, ext):
    ax.set_xlim(ext[0], ext[1])
    ax.set_ylim(ext[2], ext[3])
    ax.set_xticks([])
    ax.set_yticks([])
    ax.set_facecolor("#fbfbfa")
    for lado in ax.spines.values():
        lado.set_color("#b9b8b3")


def unico(P: dict, saida: Path):
    """Todos os braços no mesmo gráfico: pontos coloridos por braço, contornos de 50% e centros.
    Zoom na massa principal (corta as ilhas pequenas da borda; elas aparecem nos painéis)."""
    ext = _limites(P, corte=8.0, margem=0.25)
    fig, ax = plt.subplots(figsize=(15, 12.5))
    rng = np.random.default_rng(0)
    amostra = {b: P[b][rng.permutation(len(P[b]))[:AMOSTRA]] for b in P}   # menos pontos: o contorno fala mais
    pts = np.vstack(list(amostra.values()))
    cs = np.concatenate([[COR[b]] * len(amostra[b]) for b in P])
    o = rng.permutation(len(pts))                     # ordem aleatória: nenhum braço fica sempre por cima
    ax.scatter(pts[o, 0], pts[o, 1], s=14, c=cs[o], alpha=0.45, linewidths=0, zorder=2)
    for b in P:
        _contorno(ax, P[b], COR[b], ext, lw=3.4, preencher=True, alfa=0.07)
        c = np.median(P[b], axis=0)
        ax.scatter(*c, s=420, color=COR[b], edgecolors="white", linewidths=2.5, zorder=6)
    _limpo(ax, ext)
    alcas = [plt.Line2D([], [], marker="o", linestyle="-", markersize=15, linewidth=3, color=COR[b]) for b in P]
    ax.legend(alcas, [NOME[b] for b in P], loc="upper center", bbox_to_anchor=(0.5, -0.01), ncol=4, fontsize=20,
              frameon=False, handlelength=1.8, columnspacing=1.6)
    return _salvar(fig, saida, "figA7_dispersao_bracos")


def paineis(P: dict, saida: Path):
    """Um painel por braço: o braço na sua cor sobre todos os outros em cinza, com o seu contorno de 50%."""
    ext = _limites(P)
    n = len(P)
    cols = 4 if n > 6 else 3
    linhas = int(np.ceil(n / cols))
    fig, axs = plt.subplots(linhas, cols, figsize=(6.4 * cols, 6.2 * linhas))
    fundo = np.vstack(list(P.values()))
    for ax, b in zip(axs.ravel(), P):
        ax.scatter(fundo[:, 0], fundo[:, 1], s=5, color="#e2e1dc", linewidths=0, zorder=1)
        ax.scatter(P[b][:, 0], P[b][:, 1], s=12, color=COR[b], alpha=0.75, linewidths=0, zorder=2)
        _contorno(ax, P[b], COR[b], ext, preencher=True)
        _limpo(ax, ext)
        ax.set_title(NOME[b], fontsize=24, fontweight="semibold", color=COR[b] if b != "banco" else F.TINTA2, pad=10)
    for ax in axs.ravel()[n:]:
        ax.set_visible(False)
    fig.tight_layout(h_pad=2.5, w_pad=1.5)
    return _salvar(fig, saida, "figA7b_dispersao_paineis")


def _salvar(fig, saida: Path, nome: str):
    saida.mkdir(parents=True, exist_ok=True)
    out = [saida / f"{nome}.png", saida / f"{nome}.pdf"]
    for p in out:
        fig.savefig(p, facecolor="white")
    plt.close(fig)
    return out


def separacao(Z: np.ndarray, dados: dict) -> dict:
    """Acurácia de kNN (k=15, validação cruzada de 5 dobras) separando cada par de conjuntos no espaço do tratamento.
    50% = indistinguíveis; 100% = totalmente separáveis."""
    from sklearn.model_selection import cross_val_score
    from sklearn.neighbors import KNeighborsClassifier
    y = np.concatenate([[b] * len(dados[b]) for b in dados])
    conj = list(dados)
    par = {}
    for i, a in enumerate(conj):
        for b in conj[i + 1:]:
            m = (y == a) | (y == b)
            v = float(cross_val_score(KNeighborsClassifier(15), Z[m], y[m], cv=5).mean())
            par[f"{a}|{b}"] = round(v, 4)
    todos = float(cross_val_score(KNeighborsClassifier(15), Z, y, cv=5).mean())
    return {"conjuntos": conj, "pares": par, "knn_todos": round(todos, 4), "acaso_todos": round(1 / len(conj), 4)}


CURTO = {"naive": "Naive", "documentos": "Docs.", "regras": "Regras", "documentos_regras": "Docs.\n+ regras",
         "documento": "Doc.\n+ regras", "sem_retro": "Sem\nretro", "sem_externos": "Sem\next.",
         "completo": "Comp.", "banco": "Banco"}


def matriz(sep: dict, saida: Path):
    """Mapa de calor: % de acerto de kNN separando cada par de braços (50% = indistinguíveis)."""
    from matplotlib.colors import LinearSegmentedColormap
    conj = sep["conjuntos"]
    n = len(conj)
    M = np.full((n, n), np.nan)
    for i, a in enumerate(conj):
        for j, b in enumerate(conj):
            if i != j:
                M[i, j] = 100 * sep["pares"].get(f"{a}|{b}", sep["pares"].get(f"{b}|{a}"))
    lado = 1.55 * n + 2.2
    fig, ax = plt.subplots(figsize=(lado + 1.6, lado))
    cmap = LinearSegmentedColormap.from_list("sep", ["#f4f3ef", "#9fc1ea", "#2a6cc0", "#0d366b"])
    im = ax.imshow(M, cmap=cmap, vmin=50, vmax=100)
    for i in range(n):
        for j in range(n):
            if i == j:
                ax.add_patch(plt.Rectangle((j - 0.5, i - 0.5), 1, 1, color="white", zorder=2))
                continue
            v = M[i, j]
            ax.text(j, i, f"{v:.0f}", ha="center", va="center", fontsize=24, fontweight="semibold",
                    color="white" if v >= 80 else F.TINTA, zorder=3)
    rot = [CURTO[b] for b in conj]
    ax.set_xticks(range(n), rot, fontsize=21, color=F.TINTA)
    ax.set_yticks(range(n), rot, fontsize=21, color=F.TINTA)
    ax.tick_params(length=0, pad=8)
    for t, b in zip(ax.get_xticklabels(), conj):
        t.set_color(COR[b] if b != "banco" else F.TINTA2)
    for t, b in zip(ax.get_yticklabels(), conj):
        t.set_color(COR[b] if b != "banco" else F.TINTA2)
    for lado_ in ax.spines.values():
        lado_.set_visible(False)
    cb = fig.colorbar(im, ax=ax, fraction=0.045, pad=0.03)
    cb.set_ticks([50, 75, 100], labels=["50%\nindistinguíveis", "75%", "100%\nseparáveis"])
    cb.ax.tick_params(labelsize=19, length=0)
    cb.outline.set_visible(False)
    fig.tight_layout()
    return _salvar(fig, saida, "figA7c_separabilidade")


def gerar(pasta: Path | None = None) -> list:
    pasta = Path(pasta) if pasta else (SAIDA if (SAIDA / "resultado.json").exists() else SAIDA_V1)
    F.estilo()
    dados = carregar(pasta)
    P, Z = projetar(dados)
    saida = pasta / "figuras"
    saida.mkdir(parents=True, exist_ok=True)
    sep = separacao(Z, dados)
    (saida / "dispersao_separacao.json").write_text(json.dumps(sep, indent=1), encoding="utf-8")
    return unico(P, saida) + paineis(P, saida) + matriz(sep, saida)


if __name__ == "__main__":
    for p in gerar(sys.argv[1] if len(sys.argv) > 1 else None):
        print(p)
