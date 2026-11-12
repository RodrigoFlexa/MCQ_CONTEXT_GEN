"""Figuras da ablação v3 (relatorios/ablacao_geracao_v3/figuras), no estilo dos slides: sem título, fontes grandes,
uma cor por configuração da escada (naive azul, + regras laranja, + documentos verde, + externos roxo, + retro vermelho).

Eixo x das curvas: chamadas de geração acumuladas (cada onda = 160 chamadas; 960 por configuração).
Taxa de novidade: % das questões de cada fatia de chamadas que a deduplicação não liga a uma questão anterior do
mesmo documento. Vendi Score: número efetivo de questões válidas distintas (Friedman e Dieng, 2023), soma por
documento das válidas acumuladas, com embeddings locais intfloat/multilingual-e5-base (pergunta + resposta)
centrados pela média; cache em .local/.

Conhecimentos válidos distintos: as questões redundantes apontam para a que ficou (deduplicação calibrada, só medida);
cada grupo de questões equivalentes conta uma vez se tiver ao menos uma questão válida.

python -m pipeline.qa_research.experimento_ab.figuras_ablacao_v3          (português, figuras/)
python -m pipeline.qa_research.experimento_ab.figuras_ablacao_v3 --en     (inglês, nomes do artigo, figuras_en/)
"""
from __future__ import annotations

import json
from collections import defaultdict

import matplotlib
import matplotlib.ticker
matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402
import numpy as np  # noqa: E402

from pipeline.inventario.textutil import read_json  # noqa: E402

from . import comum as C  # noqa: E402
from . import figuras as F  # noqa: E402
from .ablacao_v3 import BASE, CONFIGS, SAIDA  # noqa: E402

# escada do artigo: a retroalimentação é a versão sem memória (retro_sem_memoria); a v1 com memória e a variante
# sem externos ficam só no relatório
ORDEM = ["naive", "regras", "documentos", "externos", "retro_sem_memoria"]
COR = {"naive": "#1f77b4", "regras": "#ff7f0e", "documentos": "#2ca02c", "externos": "#9467bd",
       "retro_sem_memoria": "#d62728"}
ROT = {"naive": "Naive", "regras": "+ Regras", "documentos": "+ Documentos", "externos": "+ Datasets\nexternos",
       "retro_sem_memoria": "+ Retroali-\nmentação"}
NOME = {"naive": "Naive", "regras": "+ Regras", "documentos": "+ Documentos", "externos": "+ Datasets externos",
        "retro_sem_memoria": "+ Retroalimentação"}
CURTO = {"naive": "Naive", "regras": "+ Regras", "documentos": "+ Docs.", "externos": "+ Ext.",
         "retro_sem_memoria": "+ Retro"}
CHAMADAS = 160                    # chamadas de geração por onda (40 documentos x 4 focos)
# versão em inglês (artigo): nomes das configurações e rótulos traduzidos, ponto decimal, pasta figuras_en/
EN = False
NOMES_EN = {"naive": "Naive", "regras": "+ Fine Tuned Prompt", "documentos": "+ Domain Dataset",
            "externos": "+ External Datasets", "retro_sem_memoria": "+ Example Bank"}
ROT_EN = {"naive": "Naive", "regras": "+ Fine Tuned\nPrompt", "documentos": "+ Domain\nDataset",
          "externos": "+ External\nDatasets", "retro_sem_memoria": "+ Example\nBank"}
TRAD = {
    "Questões válidas (%)": "Acceptance Ratio (%)",
    "Questões (960 chamadas)": "Questions (960 calls)",
    "Geradas": "Generated", "Aprovadas pelo auditor": "Approved by the auditor", "Válidas": "Valid",
    "Conhecimentos válidos distintos": "Unique valid items",
    "Conhecimentos válidos distintos\n(acumulado)": "Unique valid items\n(cumulative)",
    "Visita ao bloco foco": "Pass over the focal passage",
    "Chamadas de geração": "Generation calls",
    "Taxa de novidade (%)": "Novelty rate (%)",
    "Vendi Score das válidas\n(acumulado)": "Vendi Score of valid items\n(cumulative)",
    "Quase-duplicatas (%)": "Near-duplicates (%)",
    "Self-BLEU por tópico\n(menor = mais variado)": "Self-BLEU\n(lower = more varied)",
    "MTLD\n(maior = mais variado)": "MTLD\n(higher = more varied)",
    "Vendi relativo por tópico\n(maior = mais variado)": "Relative Vendi per topic\n(higher = more varied)",
    "Sem documento": "Closed-book", "Com documento": "With evidence",
    "Acurácia do painel (%)": "Panel accuracy (%)",
    "Atalho\n(resposta sai do enunciado)": "Shortcut\n(answer follows from the question)",
    "Mais de uma resposta válida": "More than one valid answer",
    "Fora da fonte": "Not grounded in the source",
    "Depende do documento": "Depends on the document",
    "Reprovadas pelo auditor\n(% das geradas)": "Rejected by the auditor\n(% of generated)",
}


def T(s: str) -> str:
    return TRAD.get(s, s) if EN else s


def usar_ingles() -> None:
    global EN, FIG, VIRG
    EN = True
    for d, novo in ((ROT, ROT_EN), (NOME, NOMES_EN), (CURTO, ROT_EN)):
        d.update(novo)
    FIG = SAIDA / "figuras_en"
    VIRG = matplotlib.ticker.FuncFormatter(lambda v, _: f"{v:g}")


ESCALA_FONTE = 1.3                # todas as fontes passam por fs(); aumentar aqui aumenta tudo


def fs(n: float) -> float:
    return round(n * ESCALA_FONTE, 1)


W = max(1.0, len(ORDEM) / 5)      # largura proporcional ao número de configurações
FIG = SAIDA / "figuras"
VIRG = matplotlib.ticker.FuncFormatter(lambda v, _: f"{v:g}".replace(".", ","))


def _salvar(fig, nome):
    FIG.mkdir(parents=True, exist_ok=True)
    out = [FIG / f"{nome}.png", FIG / f"{nome}.pdf"]
    for p in out:
        fig.savefig(p, facecolor="white")
    plt.close(fig)
    return out


def _n(x, casas=1):
    s = f"{x:.{casas}f}"
    return s if EN else s.replace(".", ",")


def _eixo(ax, ylabel, fonte=21):
    ax.set_ylabel(T(ylabel), fontsize=fs(fonte))
    ax.tick_params(axis="y", labelsize=fs(fonte - 3))
    ax.tick_params(axis="x", length=0, pad=10)
    ax.yaxis.set_major_formatter(VIRG)
    ax.yaxis.grid(True, color=F.GRADE)
    ax.set_axisbelow(True)


def _xt(ax, x, fonte=20):
    ax.set_xticks(x, [ROT[c] for c in ORDEM], fontsize=fs(fonte))
    for t, c in zip(ax.get_xticklabels(), ORDEM):
        t.set_color(COR[c])


# ------------------------------------------------------------------ dados
def dados():
    r = read_json(SAIDA / "resultado.json")
    qs = {c: C.linhas(SAIDA / f"questoes_{c}.jsonl") for c in ORDEM}
    return r, qs


def grupos(c: str) -> dict:
    """uid -> uid representante do grupo de questões equivalentes (dedup da configuração)."""
    red = {}
    for p in sorted((SAIDA / c / "dedup").glob("*/*.json")):
        d = read_json(p)
        if d.get("decisao") == "redundante":
            red[d["uid"]] = d["com"]
        elif d.get("decisao") == "substitui":
            red[d["substituida"]] = d["uid"]

    def raiz(u):
        visto = set()
        while u in red and u not in visto:
            visto.add(u)
            u = red[u]
        return u
    return raiz


def distintos_por_onda(c: str, qs: list[dict]) -> list[int]:
    """Conhecimentos válidos distintos acumulados até cada onda."""
    raiz = grupos(c)
    primeira = {}
    for q in qs:
        if q["valida"]:
            g = raiz(q["uid"])
            primeira[g] = min(primeira.get(g, 99), q["onda"])
    ondas = max(q["onda"] for q in qs)
    return [sum(1 for o in primeira.values() if o <= w) for w in range(1, ondas + 1)]


# ------------------------------------------------------------------ figuras
def validade(r):
    """% de válidas (auditor + resposta curta + sustentação) com IC 95%, por configuração."""
    fig, ax = plt.subplots(figsize=(15 * W, 7))
    x = np.arange(len(ORDEM))
    v = np.array([r["configs"][c]["validas"]["pct"] for c in ORDEM])
    lo = np.array([r["configs"][c]["validas"]["ic95"][0] for c in ORDEM])
    hi = np.array([r["configs"][c]["validas"]["ic95"][1] for c in ORDEM])
    ax.bar(x, v, 0.62, color=[COR[c] for c in ORDEM], zorder=2)
    ax.errorbar(x, v, yerr=[v - lo, hi - v], fmt="none", ecolor=F.TINTA2, elinewidth=1.8, capsize=7, zorder=3)
    for xi, vi, h in zip(x, v, hi):
        ax.text(xi, h + 0.8, f"{_n(vi)}%", ha="center", va="bottom", fontsize=fs(23), fontweight="semibold", color=F.TINTA)
    _xt(ax, x)
    _eixo(ax, "Questões válidas (%)")
    ax.set_ylim(0, max(hi) * 1.22)
    return _salvar(fig, "figV1_validade")


def self_bleu(r):
    """Self-BLEU por tópico das geradas (amostras do mesmo tamanho), em barras; menor = redação mais variada."""
    fig, ax = plt.subplots(figsize=(15 * W, 7))
    x = np.arange(len(ORDEM))
    v = np.array([r["configs"][c]["vocabulario_geradas"]["self_bleu_por_topico"] for c in ORDEM])
    ax.bar(x, v, 0.62, color=[COR[c] for c in ORDEM], zorder=2)
    for xi, vi in zip(x, v):
        ax.text(xi, vi + 0.012, _n(vi, 2), ha="center", va="bottom", fontsize=fs(23), fontweight="semibold", color=F.TINTA)
    _xt(ax, x)
    _eixo(ax, "Self-BLEU")
    ax.set_ylim(0, max(v) * 1.18)
    return _salvar(fig, "figV9_self_bleu")


def funil(r, qs):
    """Geradas, aprovadas pelo auditor, válidas e conhecimentos válidos distintos, com o mesmo orçamento de chamadas."""
    etapas = [("Geradas", lambda c: len(qs[c]), F.RAMPA[1]),
              ("Aprovadas pelo auditor", lambda c: r["configs"][c]["aprovadas_auditor"]["n"], F.RAMPA[3]),
              ("Válidas", lambda c: r["configs"][c]["validas"]["n"], F.RAMPA[5]),
              ("Conhecimentos válidos distintos", lambda c: distintos_por_onda(c, qs[c])[-1], F.LARANJA)]
    fig, ax = plt.subplots(figsize=(19 * W, 7.6))
    x = np.arange(len(ORDEM))
    w = 0.2
    for k, (nome, f, cor) in enumerate(etapas):
        vals = [f(c) for c in ORDEM]
        pos = x + (k - 1.5) * w
        ax.bar(pos, vals, w * 0.94, color=cor, label=T(nome), zorder=2)
        for p, n in zip(pos, vals):
            ax.text(p, n + 40, str(n), ha="center", va="bottom", fontsize=fs(15), color=F.TINTA, rotation=0)
    _xt(ax, x)
    _eixo(ax, "Questões (960 chamadas)")
    ax.set_ylim(0, 4600)
    ax.legend(loc="lower center", bbox_to_anchor=(0.5, 1.0), fontsize=fs(18), ncol=4, handlelength=1.2,
              columnspacing=1.4, frameon=False)
    return _salvar(fig, "figV2_funil")


def acumulado(qs):
    """(a) conhecimentos válidos distintos acumulados por onda; (b) % de válidas por visita ao foco."""
    fig, axs = plt.subplots(1, 2, figsize=(22, 8))
    ax = axs[0]
    for c in ORDEM:
        y = distintos_por_onda(c, qs[c])
        ax.plot(range(1, len(y) + 1), y, color=COR[c], linewidth=3.4, marker="o", markersize=10, label=NOME[c])
        ax.text(len(y) + 0.12, y[-1], str(y[-1]), va="center", fontsize=fs(18), color=COR[c], fontweight="semibold")
    _x_chamadas(ax)
    _eixo(ax, "Conhecimentos válidos distintos\n(acumulado)")
    ax = axs[1]
    for c in ORDEM:
        v = defaultdict(lambda: [0, 0])
        for q in qs[c]:
            v[q["visita"]][0] += q["valida"]
            v[q["visita"]][1] += 1
        y = [100 * v[k][0] / v[k][1] for k in sorted(v)]
        ax.plot(sorted(v), y, color=COR[c], linewidth=3.4, marker="o", markersize=10)
    ax.set_xticks([1, 2, 3], ["1", "2", "3"], fontsize=fs(19))
    ax.set_xlim(0.8, 3.2)
    ax.set_xlabel(T("Visita ao bloco foco"), fontsize=fs(21))
    _eixo(ax, "Questões válidas (%)")
    alcas = [plt.Line2D([], [], color=COR[c], linewidth=3.4, marker="o", markersize=10) for c in ORDEM]
    fig.legend(alcas, [NOME[c] for c in ORDEM], loc="upper center", bbox_to_anchor=(0.5, 0.0), ncol=3, fontsize=fs(19),
               frameon=False, handlelength=1.8, columnspacing=1.6)
    fig.tight_layout(w_pad=4)
    return _salvar(fig, "figV3_acumulado_e_visitas")


def _x_chamadas(ax, ondas=6, fonte=19):
    ax.set_xticks(range(1, ondas + 1), [str(CHAMADAS * w) for w in range(1, ondas + 1)], fontsize=fs(fonte))
    ax.set_xlim(0.7, ondas + 0.8)
    ax.set_xlabel(T("Chamadas de geração"), fontsize=fs(21))


def _linhas(ax, series, casas=0, sufixo="", folga=0.072):
    """Curvas com o valor final à direita; rótulos próximos são afastados para não se sobreporem."""
    for c in ORDEM:
        y = series[c]
        ax.plot(range(1, len(y) + 1), y, color=COR[c], linewidth=3.4, marker="o", markersize=10, label=NOME[c])
    fim = sorted((series[c][-1], c) for c in ORDEM)
    vals = [v for s in series.values() for v in s]
    passo = folga * (max(vals) - min(min(vals), 0))
    grupos = []                                    # rótulos próximos formam um bloco espaçado e centrado nos valores
    for v, _ in fim:
        if grupos and v - grupos[-1][-1] < passo:
            grupos[-1].append(v)
        else:
            grupos.append([v])
    pos = []
    for g in grupos:
        base = (g[0] + g[-1]) / 2 - passo * (len(g) - 1) / 2
        if pos:
            base = max(base, pos[-1] + passo)
        pos += [base + passo * k for k in range(len(g))]
    for (v, c), yp in zip(fim, pos):
        n = len(series[c])
        ax.text(n + 0.12, yp, _n(v, casas) + sufixo, va="center", fontsize=fs(18), color=COR[c], fontweight="semibold")


def _legenda_barras(fig, ncol=5):
    from matplotlib.patches import Patch
    alcas = [Patch(facecolor=COR[c]) for c in ORDEM]
    fig.legend(alcas, [NOME[c] for c in ORDEM], loc="upper center", bbox_to_anchor=(0.5, 0.0), ncol=ncol,
               fontsize=fs(19), frameon=False, handlelength=1.4, columnspacing=1.8)


def _legenda(fig, ncol=5):
    alcas = [plt.Line2D([], [], color=COR[c], linewidth=3.4, marker="o", markersize=10) for c in ORDEM]
    fig.legend(alcas, [NOME[c] for c in ORDEM], loc="upper center", bbox_to_anchor=(0.5, 0.0), ncol=ncol,
               fontsize=fs(19), frameon=False, handlelength=1.8, columnspacing=1.6)


def taxa_novidade(c: str, qs: list[dict]) -> list[float]:
    """% das questões de cada onda que trazem conhecimento novo no documento (decisão nova ou substitui do dedup)."""
    dec = {}
    for p in (SAIDA / c / "dedup").glob("*/*.json"):
        d = read_json(p)
        dec[d["uid"]] = d["decisao"]
    out = []
    for w in range(1, max(q["onda"] for q in qs) + 1):
        wq = [q for q in qs if q["onda"] == w]
        out.append(100 * sum(dec.get(q["uid"]) in ("nova", "substitui") for q in wq) / len(wq))
    return out


def novidade(qs):
    """Taxa de novidade por fatia de 160 chamadas."""
    fig, ax = plt.subplots(figsize=(14, 7.6))
    _linhas(ax, {c: taxa_novidade(c, qs[c]) for c in ORDEM}, sufixo="%")
    _x_chamadas(ax)
    ax.set_ylim(0, 105)
    _eixo(ax, "Taxa de novidade (%)")
    _legenda(fig, ncol=3)
    fig.tight_layout()
    return _salvar(fig, "figV7_novidade")


def _e5(qs) -> dict:
    """uid -> vetor e5 normalizado (pergunta + resposta) das válidas; cache local."""
    arq = SAIDA / ".local" / "e5_validas.npz"
    val = sorted({q["uid"]: q for c in ORDEM for q in qs[c] if q["valida"]}.values(), key=lambda q: q["uid"])
    txt = [f"query: {q['pergunta']} {q['resposta']}" for q in val]
    chave = C.sha("\n".join(txt))
    if arq.exists():
        z = np.load(arq, allow_pickle=False)
        if str(z["chave"]) == chave:
            return dict(zip(z["uid"].tolist(), z["E"].astype(np.float64)))
    from sentence_transformers import SentenceTransformer
    E = SentenceTransformer("intfloat/multilingual-e5-base", device="cpu").encode(
        txt, batch_size=64, normalize_embeddings=True, show_progress_bar=False)
    arq.parent.mkdir(parents=True, exist_ok=True)
    np.savez_compressed(arq, E=E.astype(np.float16), uid=np.array([q["uid"] for q in val]), chave=chave)
    return dict(zip([q["uid"] for q in val], np.asarray(E, dtype=np.float64)))


def vendi_por_onda(c: str, qs: list[dict], E: dict, media: np.ndarray) -> list[float]:
    """Vendi Score das válidas acumuladas até cada onda: soma, por documento, do número efetivo de questões distintas
    (núcleo cosseno sobre embeddings centrados)."""
    from .ablacao import vendi
    out = []
    for w in range(1, max(q["onda"] for q in qs) + 1):
        por_item = defaultdict(list)
        for q in qs:
            if q["valida"] and q["onda"] <= w:
                por_item[q["item"]].append(E[q["uid"]] - media)
        tot = 0.0
        for vs in por_item.values():
            V = np.array(vs)
            tot += vendi(V / np.clip(np.linalg.norm(V, axis=1, keepdims=True), 1e-12, None))
        out.append(tot)
    return out


def vendi_curva(qs):
    """Vendi Score acumulado das válidas por chamadas de geração."""
    E = _e5(qs)
    media = np.mean(np.array(list(E.values())), axis=0)
    fig, ax = plt.subplots(figsize=(14, 7.6))
    _linhas(ax, {c: vendi_por_onda(c, qs[c], E, media) for c in ORDEM})
    _x_chamadas(ax)
    _eixo(ax, "Vendi Score das válidas\n(acumulado)")
    _legenda(fig, ncol=3)
    fig.tight_layout()
    return _salvar(fig, "figV8_vendi")


def diversidade(r):
    """Quase-duplicatas, Self-BLEU por tópico, MTLD e Vendi relativo (geradas, amostras do mesmo tamanho)."""
    metr = (("quase_duplicatas", None, "Quase-duplicatas (%)", 0),
            ("self_bleu_por_topico", "vocabulario_geradas", "Self-BLEU por tópico\n(menor = mais variado)", 2),
            ("mtld", "vocabulario_geradas", "MTLD\n(maior = mais variado)", 0),
            ("vendi_relativo_por_topico", "vocabulario_geradas", "Vendi relativo por tópico\n(maior = mais variado)", 2))
    fig, axs = plt.subplots(2, 2, figsize=(18 * W, 12.5))
    axs = axs.ravel()
    x = np.arange(len(ORDEM))
    for ax, (k, bloco, ylabel, casas) in zip(axs, metr):
        v = [(r["configs"][c][bloco][k] if bloco else r["configs"][c][k]) for c in ORDEM]
        ax.bar(x, v, 0.68, color=[COR[c] for c in ORDEM], zorder=2)
        topo = max(v)
        for xi, n in zip(x, v):
            ax.text(xi, n + topo * 0.015, _n(n, casas), ha="center", va="bottom", fontsize=fs(17), fontweight="semibold",
                    color=F.TINTA)
        ax.set_xticks([])
        _eixo(ax, ylabel, fonte=19)
        ax.set_ylim(0, topo * 1.16)
    _legenda_barras(fig)
    fig.tight_layout(w_pad=3)
    return _salvar(fig, "figV4_diversidade")


def dificuldade(r):
    """Acerto médio do painel sem e com contexto, na amostra de 500 por configuração (válidas e inválidas)."""
    fig, ax = plt.subplots(figsize=(16 * W, 7.2))
    x = np.arange(len(ORDEM))
    w = 0.36
    for k, (cond, nome, cor) in enumerate((("acerto_sem_contexto", "Sem documento", F.AZUL),
                                            ("acerto_com_contexto", "Com documento", F.LARANJA))):
        v = [r["configs"][c]["dificuldade"]["todas"][cond] for c in ORDEM]
        pos = x + (k - 0.5) * w
        ax.bar(pos, v, w * 0.94, color=cor, label=T(nome), zorder=2)
        for p, n in zip(pos, v):
            ax.text(p, n + 1.2, _n(n, 0), ha="center", va="bottom", fontsize=fs(20), fontweight="semibold", color=F.TINTA)
    _xt(ax, x)
    _eixo(ax, "Acurácia do painel (%)")
    ax.set_ylim(0, 108)
    ax.legend(loc="lower center", bbox_to_anchor=(0.5, 1.0), fontsize=fs(19), ncol=2, handlelength=1.2,
              frameon=False)
    return _salvar(fig, "figV5_dificuldade")


def motivos(r, qs):
    """Reprovações do auditor por motivo, em % das geradas (uma questão pode ter mais de um motivo)."""
    grupos_ = (("atalho", ("atalho",), F.RAMPA[6], "Atalho\n(resposta sai do enunciado)"),
               ("varias", ("varias_respostas", "nao_unico"), F.RAMPA[4], "Mais de uma resposta válida"),
               ("fonte", ("fora_da_fonte",), F.RAMPA[2], "Fora da fonte"),
               ("doc", ("depende_do_documento",), "#c9c8c3", "Depende do documento"))
    fig, axs = plt.subplots(2, 2, figsize=(18 * W, 12.5), sharey=True)
    axs = axs.ravel()
    x = np.arange(len(ORDEM))
    for ax, (_, ks, cor, nome) in zip(axs, grupos_):
        v = [100 * sum(any(f in ks for f in q["auditoria"].get("falhas", [])) for q in qs[c]) / len(qs[c]) for c in ORDEM]
        ax.bar(x, v, 0.68, color=[COR[c] for c in ORDEM], zorder=2)
        for xi, n in zip(x, v):
            ax.text(xi, n + 1.2, _n(n, 0), ha="center", va="bottom", fontsize=fs(18), fontweight="semibold", color=F.TINTA)
        ax.set_xticks([])
        ax.set_xlabel(T(nome), fontsize=fs(20), labelpad=12)
        _eixo(ax, "Reprovadas pelo auditor\n(% das geradas)" if ax in (axs[0], axs[2]) else "", fonte=19)
    axs[0].set_ylim(0, 100)
    _legenda_barras(fig)
    fig.tight_layout(w_pad=2)
    return _salvar(fig, "figV6_motivos")


def gerar() -> list:
    F.estilo()
    r, qs = dados()
    resumo = {c: {"conhecimentos_validos_distintos_por_onda": distintos_por_onda(c, qs[c])} for c in ORDEM}
    FIG.mkdir(parents=True, exist_ok=True)
    (FIG / "distintos.json").write_text(json.dumps(resumo, indent=1), encoding="utf-8")
    return (validade(r) + funil(r, qs) + acumulado(qs) + diversidade(r) + dificuldade(r) + motivos(r, qs)
            + novidade(qs) + vendi_curva(qs) + self_bleu(r))


if __name__ == "__main__":
    import sys
    if "--en" in sys.argv[1:]:
        usar_ingles()
    for p in gerar():
        print(p)
