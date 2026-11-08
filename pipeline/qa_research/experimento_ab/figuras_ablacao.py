"""Figuras do estudo de ablação da geração (relatorios/ablacao_geracao_v1/figuras), no estilo dos slides.

Sem títulos, fontes grandes, PNG 300 dpi e PDF. Lê resultado.json (python -m ...experimento_ab.figuras_ablacao).
"""
from __future__ import annotations

import json

import matplotlib
import matplotlib.ticker  # noqa: F401
matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402
import numpy as np  # noqa: E402

from . import figuras as F  # noqa: E402
from .ablacao import SAIDA as ABL  # noqa: E402

SAIDA = ABL / "figuras"
ORDEM = ["naive", "documento", "sem_retro", "sem_externos", "completo"]
ROTULO = {"naive": "Naive", "documento": "Documento\n+ regras", "sem_retro": "Sem retro-\nalimentação",
          "sem_externos": "Sem datasets\nexternos", "completo": "Pipeline\ncompleto"}
CINZA = "#b9b8b3"


def _salvar(fig, nome):
    SAIDA.mkdir(parents=True, exist_ok=True)
    out = [SAIDA / f"{nome}.png", SAIDA / f"{nome}.pdf"]
    for p in out:
        fig.savefig(p, facecolor="white")
    plt.close(fig)
    return out


def _eixo(ax, ylabel, ymax, yfonte=20):
    ax.set_ylim(0, ymax)
    ax.set_ylabel(ylabel, fontsize=yfonte + 2)
    ax.tick_params(axis="y", labelsize=yfonte)
    ax.tick_params(axis="x", length=0, pad=10)
    ax.yaxis.grid(True)
    ax.set_axisbelow(True)


def taxa_aceite(r):
    """Aceitas por braço, empilhadas por tentativa (1ª, 2ª e 3ª: o ganho da retroalimentação), com IC 95%."""
    fig, ax = plt.subplots(figsize=(14, 7))
    x = np.arange(len(ORDEM))
    cores = {1: F.RAMPA[6], 2: F.RAMPA[4], 3: F.RAMPA[2]}
    base = np.zeros(len(ORDEM))
    for t, nome in ((1, "1ª tentativa"), (2, "2ª tentativa"), (3, "3ª tentativa")):
        v = np.array([r["bracos"][b]["aceitas_por_tentativa"].get(str(t), 0) / 10 for b in ORDEM])
        ax.bar(x, v, 0.62, bottom=base, color=cores[t], label=nome, edgecolor="white", linewidth=1.5, zorder=2)
        base += v
    lo = np.array([r["bracos"][b]["ic95"][0] for b in ORDEM])
    hi = np.array([r["bracos"][b]["ic95"][1] for b in ORDEM])
    ax.errorbar(x, base, yerr=[base - lo, hi - base], fmt="none", ecolor=F.TINTA2, elinewidth=1.6, capsize=6, zorder=3)
    for xi, v, h in zip(x, base, hi):
        ax.text(xi, h + 1.2, f"{v:.1f}%".replace(".", ","), ha="center", va="bottom", fontsize=22,
                fontweight="semibold", color=F.TINTA)
    ax.set_xticks(x, [ROTULO[b] for b in ORDEM], fontsize=20, color=F.TINTA)
    _eixo(ax, "Questões aceitas (% de 1000)", 58)
    ax.legend(loc="upper left", fontsize=19, handlelength=1.2)
    return _salvar(fig, "figA1_taxa_aceite")


def funil(r):
    """Aprovadas pelo auditor, totalmente sustentadas e aceitas (sem redundância), de 1000 pedidas."""
    fig, ax = plt.subplots(figsize=(15, 7))
    x = np.arange(len(ORDEM))
    w = 0.27
    etapas = (("aprovadas_auditor", "Aprovadas pelo auditor", F.RAMPA[2]),
              ("sustentadas", "Sustentadas pelo documento", F.RAMPA[4]),
              ("aceitas", "Aceitas (sem redundância)", F.RAMPA[6]))
    for k, (chave, nome, cor) in enumerate(etapas):
        v = [r["bracos"][b][chave] for b in ORDEM]
        pos = x + (k - 1) * w
        ax.bar(pos, v, w * 0.94, color=cor, label=nome, edgecolor="white", linewidth=1.2, zorder=2)
        for p, n in zip(pos, v):
            ax.text(p, n + 12, str(n), ha="center", va="bottom", fontsize=16, color=F.TINTA)
    ax.set_xticks(x, [ROTULO[b] for b in ORDEM], fontsize=20, color=F.TINTA)
    _eixo(ax, "Questões (de 1000 pedidas)", 880)
    ax.legend(loc="upper left", fontsize=18, ncol=3, bbox_to_anchor=(0, 1.1), handlelength=1.2, columnspacing=1.4)
    return _salvar(fig, "figA2_funil")


def _paineis(r, metr, nome_arq):
    """Dois painéis lado a lado sobre as 1000 questões geradas por braço; linha tracejada = banco final."""
    fig, axs = plt.subplots(1, 2, figsize=(16, 7.2))
    x = np.arange(len(ORDEM))
    for ax, (chave, nome, casas) in zip(axs, metr):
        v = [r["bracos"][b]["vocabulario_geradas"][chave] for b in ORDEM]
        cores = [CINZA] + [F.AZUL] * (len(ORDEM) - 2) + [F.RAMPA[6]]
        ax.bar(x, v, 0.7, color=cores, zorder=2)
        ref = r["referencia_banco"]["vocabulario"][chave]
        ax.axhline(ref, color=F.LARANJA, linestyle="--", linewidth=2.5, zorder=3)
        topo = max(max(v), ref) * 1.25
        for xi, n, cor in zip(x, v, cores):
            txt = f"{n:.{casas}f}".replace(".", ",")
            if abs(n + topo * 0.04 - ref) < topo * 0.06:      # rótulo cairia sobre a linha do banco: vai para dentro
                ax.text(xi, n - topo * 0.015, txt, ha="center", va="top", fontsize=19, fontweight="semibold",
                        color="white" if cor != CINZA else F.TINTA)
            else:
                ax.text(xi, n + topo * 0.012, txt, ha="center", va="bottom", fontsize=19, fontweight="semibold",
                        color=F.TINTA)
        ax.set_xticks(x, ["Naive", "Doc.", "Sem\nretro", "Sem\next.", "Comp."], fontsize=20, color=F.TINTA)
        ax.set_ylim(0, topo)
        ax.yaxis.set_major_formatter(matplotlib.ticker.FuncFormatter(
            lambda y, _, c=casas: f"{y:.{max(c - 1, 0)}f}".replace(".", ",")))
        ax.tick_params(axis="y", labelsize=18)
        ax.tick_params(axis="x", length=0, pad=8)
        ax.yaxis.grid(True)
        ax.set_axisbelow(True)
        ax.set_xlabel(nome, fontsize=22, labelpad=14, color=F.TINTA)
    axs[0].plot([], [], color=F.LARANJA, linestyle="--", linewidth=2.5, label="Banco final (referência)")
    axs[0].legend(loc="upper left", fontsize=18, handlelength=1.8)
    fig.tight_layout(w_pad=3)
    return _salvar(fig, nome_arq)


def vocabulario(r):
    """Riqueza de vocabulário e diversidade das 1000 questões geradas por braço (mesmo tamanho de conjunto)."""
    return (_paineis(r, (("vocabulario_conteudo", "Vocabulário (palavras de conteúdo)", 0),
                         ("termos_especializados", "Termos especializados", 0)), "figA3_vocabulario")
            + _paineis(r, (("mtld", "MTLD (diversidade lexical)", 0),
                           ("self_bleu_por_topico", "Self-BLEU por tópico (menor = mais variado)", 3)),
                       "figA3b_diversidade"))


def motivos(r):
    """Questões recusadas pelo auditor por motivo, por braço."""
    grupos = (("atalho", "Atalho (resposta sai do enunciado)", F.RAMPA[6]),
              ("varias_respostas", "Mais de uma resposta válida", F.RAMPA[4]),
              ("outros", "Fora da fonte, depende do documento ou não única", F.RAMPA[2]))
    fig, ax = plt.subplots(figsize=(14, 7))
    x = np.arange(len(ORDEM))
    base = np.zeros(len(ORDEM))
    for chave, nome, cor in grupos:
        v = []
        for b in ORDEM:
            m = r["bracos"][b]["motivos_auditor"]
            v.append(sum(n for k, n in m.items() if k not in ("atalho", "varias_respostas")) if chave == "outros"
                     else m.get(chave, 0))
        v = np.array(v, dtype=float)
        ax.bar(x, v, 0.62, bottom=base, color=cor, label=nome, edgecolor="white", linewidth=1.5, zorder=2)
        base += v
    for xi, n in zip(x, base):
        ax.text(xi, n + 10, f"{n:.0f}", ha="center", va="bottom", fontsize=21, fontweight="semibold", color=F.TINTA)
    ax.set_xticks(x, [ROTULO[b] for b in ORDEM], fontsize=20, color=F.TINTA)
    _eixo(ax, "Recusadas pelo auditor", 1150)
    ax.legend(loc="upper right", fontsize=17, handlelength=1.2)
    return _salvar(fig, "figA4_motivos_recusa")


def gerar() -> list:
    F.estilo()
    r = json.loads((ABL / "resultado.json").read_text(encoding="utf-8"))
    return taxa_aceite(r) + funil(r) + vocabulario(r) + motivos(r)


if __name__ == "__main__":
    for p in gerar():
        print(p)
