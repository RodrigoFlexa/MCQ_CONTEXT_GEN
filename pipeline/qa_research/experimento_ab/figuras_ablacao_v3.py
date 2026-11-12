"""Figuras da ablação v3 (relatorios/ablacao_geracao_v3/figuras), no estilo dos slides: sem título, fontes grandes,
uma cor por configuração da escada (naive azul, + regras laranja, + documentos verde, + externos roxo, + retro vermelho).

Conhecimentos válidos distintos: as questões redundantes apontam para a que ficou (deduplicação calibrada, só medida);
cada grupo de questões equivalentes conta uma vez se tiver ao menos uma questão válida.

python -m pipeline.qa_research.experimento_ab.figuras_ablacao_v3
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
    return f"{x:.{casas}f}".replace(".", ",")


def _eixo(ax, ylabel, fonte=21):
    ax.set_ylabel(ylabel, fontsize=fonte)
    ax.tick_params(axis="y", labelsize=fonte - 3)
    ax.tick_params(axis="x", length=0, pad=10)
    ax.yaxis.set_major_formatter(VIRG)
    ax.yaxis.grid(True, color=F.GRADE)
    ax.set_axisbelow(True)


def _xt(ax, x, fonte=20):
    ax.set_xticks(x, [ROT[c] for c in ORDEM], fontsize=fonte)
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
        ax.text(xi, h + 0.8, f"{_n(vi)}%", ha="center", va="bottom", fontsize=23, fontweight="semibold", color=F.TINTA)
    _xt(ax, x)
    _eixo(ax, "Questões válidas (%)")
    ax.set_ylim(0, max(hi) * 1.22)
    return _salvar(fig, "figV1_validade")


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
        ax.bar(pos, vals, w * 0.94, color=cor, label=nome, zorder=2)
        for p, n in zip(pos, vals):
            ax.text(p, n + 40, str(n), ha="center", va="bottom", fontsize=15, color=F.TINTA, rotation=0)
    _xt(ax, x)
    _eixo(ax, "Questões (960 chamadas)")
    ax.set_ylim(0, 4600)
    ax.legend(loc="upper right", fontsize=18, ncol=2, handlelength=1.2, columnspacing=1.4)
    return _salvar(fig, "figV2_funil")


def acumulado(qs):
    """(a) conhecimentos válidos distintos acumulados por onda; (b) % de válidas por visita ao foco."""
    fig, axs = plt.subplots(1, 2, figsize=(22, 8))
    ax = axs[0]
    for c in ORDEM:
        y = distintos_por_onda(c, qs[c])
        ax.plot(range(1, len(y) + 1), y, color=COR[c], linewidth=3.4, marker="o", markersize=10, label=NOME[c])
        ax.text(len(y) + 0.12, y[-1], str(y[-1]), va="center", fontsize=18, color=COR[c], fontweight="semibold")
    ax.set_xticks(range(1, 7), [str(i) for i in range(1, 7)], fontsize=19)
    ax.set_xlim(0.7, 6.8)
    ax.set_xlabel("Onda de geração", fontsize=21)
    _eixo(ax, "Conhecimentos válidos distintos\n(acumulado)")
    ax = axs[1]
    for c in ORDEM:
        v = defaultdict(lambda: [0, 0])
        for q in qs[c]:
            v[q["visita"]][0] += q["valida"]
            v[q["visita"]][1] += 1
        y = [100 * v[k][0] / v[k][1] for k in sorted(v)]
        ax.plot(sorted(v), y, color=COR[c], linewidth=3.4, marker="o", markersize=10)
    ax.set_xticks([1, 2, 3], ["1", "2", "3"], fontsize=19)
    ax.set_xlim(0.8, 3.2)
    ax.set_xlabel("Visita ao bloco foco", fontsize=21)
    _eixo(ax, "Questões válidas (%)")
    alcas = [plt.Line2D([], [], color=COR[c], linewidth=3.4, marker="o", markersize=10) for c in ORDEM]
    fig.legend(alcas, [NOME[c] for c in ORDEM], loc="upper center", bbox_to_anchor=(0.5, 0.0), ncol=min(len(ORDEM), 4), fontsize=19,
               frameon=False, handlelength=1.8, columnspacing=1.6)
    fig.tight_layout(w_pad=4)
    return _salvar(fig, "figV3_acumulado_e_visitas")


def diversidade(r):
    """Quase-duplicatas, Self-BLEU por tópico, MTLD e Vendi relativo (geradas, amostras do mesmo tamanho)."""
    metr = (("quase_duplicatas", None, "Quase-duplicatas (%)", 0),
            ("self_bleu_por_topico", "vocabulario_geradas", "Self-BLEU por tópico\n(menor = mais variado)", 2),
            ("mtld", "vocabulario_geradas", "MTLD\n(maior = mais variado)", 0),
            ("vendi_relativo_por_topico", "vocabulario_geradas", "Vendi relativo por tópico\n(maior = mais variado)", 2))
    fig, axs = plt.subplots(1, 4, figsize=(28 * W, 7.4))
    x = np.arange(len(ORDEM))
    for ax, (k, bloco, ylabel, casas) in zip(axs, metr):
        v = [(r["configs"][c][bloco][k] if bloco else r["configs"][c][k]) for c in ORDEM]
        ax.bar(x, v, 0.68, color=[COR[c] for c in ORDEM], zorder=2)
        topo = max(v)
        for xi, n in zip(x, v):
            ax.text(xi, n + topo * 0.015, _n(n, casas), ha="center", va="bottom", fontsize=17, fontweight="semibold",
                    color=F.TINTA)
        ax.set_xticks(x, [CURTO[c] for c in ORDEM], fontsize=17, rotation=0)
        for t, c in zip(ax.get_xticklabels(), ORDEM):
            t.set_color(COR[c])
        _eixo(ax, ylabel, fonte=19)
        ax.set_ylim(0, topo * 1.16)
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
        ax.bar(pos, v, w * 0.94, color=cor, label=nome, zorder=2)
        for p, n in zip(pos, v):
            ax.text(p, n + 1.2, _n(n, 0), ha="center", va="bottom", fontsize=20, fontweight="semibold", color=F.TINTA)
    _xt(ax, x)
    _eixo(ax, "Acurácia do painel (%)")
    ax.set_ylim(0, 108)
    ax.legend(loc="upper left", fontsize=19, ncol=2, handlelength=1.2)
    return _salvar(fig, "figV5_dificuldade")


def motivos(r, qs):
    """Reprovações do auditor por motivo, em % das geradas (uma questão pode ter mais de um motivo)."""
    grupos_ = (("atalho", ("atalho",), F.RAMPA[6], "Atalho (resposta sai do enunciado)"),
               ("varias", ("varias_respostas", "nao_unico"), F.RAMPA[4], "Mais de uma resposta válida"),
               ("fonte", ("fora_da_fonte",), F.RAMPA[2], "Fora da fonte"),
               ("doc", ("depende_do_documento",), "#c9c8c3", "Depende do documento"))
    fig, axs = plt.subplots(1, 4, figsize=(28 * W, 7.4), sharey=True)
    x = np.arange(len(ORDEM))
    for ax, (_, ks, cor, nome) in zip(axs, grupos_):
        v = [100 * sum(any(f in ks for f in q["auditoria"].get("falhas", [])) for q in qs[c]) / len(qs[c]) for c in ORDEM]
        ax.bar(x, v, 0.68, color=[COR[c] for c in ORDEM], zorder=2)
        for xi, n in zip(x, v):
            ax.text(xi, n + 1.2, _n(n, 0), ha="center", va="bottom", fontsize=18, fontweight="semibold", color=F.TINTA)
        ax.set_xticks(x, [CURTO[c] for c in ORDEM], fontsize=17)
        for t, c in zip(ax.get_xticklabels(), ORDEM):
            t.set_color(COR[c])
        ax.set_xlabel(nome, fontsize=20, labelpad=12)
        _eixo(ax, "Reprovadas pelo auditor (% das geradas)" if ax is axs[0] else "", fonte=19)
    axs[0].set_ylim(0, 100)
    fig.tight_layout(w_pad=2)
    return _salvar(fig, "figV6_motivos")


def gerar() -> list:
    F.estilo()
    r, qs = dados()
    resumo = {c: {"conhecimentos_validos_distintos_por_onda": distintos_por_onda(c, qs[c])} for c in ORDEM}
    FIG.mkdir(parents=True, exist_ok=True)
    (FIG / "distintos.json").write_text(json.dumps(resumo, indent=1), encoding="utf-8")
    return (validade(r) + funil(r, qs) + acumulado(qs) + diversidade(r) + dificuldade(r) + motivos(r, qs))


if __name__ == "__main__":
    for p in gerar():
        print(p)
