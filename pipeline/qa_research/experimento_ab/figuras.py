"""Figuras do banco PetroQuest v1 para apresentação e artigo (PNG 300 dpi e PDF vetorial).

Análise das questões (banco inteiro): funil de construção, composição por tipo e área, divisão em conjuntos.
Desempenho dos modelos (conjunto de TESTE): acurácia sem e com documento com IC 95% (bootstrap), acurácia por tipo,
ganho com o documento por área e métricas lexicais (F1 de tokens e ROUGE-L).
Saída: relatorios/petroquest_banco_v1/figuras/.
"""
from __future__ import annotations

import csv
import json
from collections import Counter
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402
import matplotlib.ticker  # noqa: E402,F401
import numpy as np  # noqa: E402
from matplotlib import font_manager  # noqa: E402

from . import comum as C  # noqa: E402
from . import limite as LI  # noqa: E402
from .banco import SAIDA as BANCO  # noqa: E402
from .completo import SAIDA as FINAL_V2  # noqa: E402

SAIDA = BANCO / "figuras"
# paleta de referência (validada para daltonismo): azul = sem documento, laranja = com documento
AZUL, LARANJA = "#2a78d6", "#eb6834"
RAMPA = ["#cde2fb", "#9ec5f4", "#6da7ec", "#3987e5", "#256abf", "#184f95", "#0d366b"]   # sequencial azul
ORDINAL4 = ["#86b6ef", "#3987e5", "#1c5cab", "#0d366b"]                                 # fácil -> muito difícil
TINTA, TINTA2, TINTA3, GRADE = "#0b0b0b", "#52514e", "#8a8984", "#e6e5e1"
MODELOS = ["gpt-4-1-mini", "gpt-4-1", "gpt-5-mini", "gpt-5", "gpt-5-4"]
NOME = {"gpt-4-1-mini": "GPT-4.1 Mini", "gpt-4-1": "GPT-4.1", "gpt-5-mini": "GPT-5 mini", "gpt-5": "GPT-5",
        "gpt-5-4": "GPT-5.4*"}
TIPOS = ["conceito", "mecanismo", "consequencia", "diagnostico", "decisao", "procedimento"]
NOME_TIPO = {"conceito": "Conceito", "mecanismo": "Mecanismo", "consequencia": "Consequência",
             "diagnostico": "Diagnóstico", "decisao": "Decisão", "procedimento": "Procedimento"}
ESTRATOS = ["facil", "media", "dificil", "muito_dificil"]
NOME_ESTRATO = {"facil": "Fácil", "media": "Média", "dificil": "Difícil", "muito_dificil": "Muito difícil"}
AREA_CURTA = {
    "Produção e Processo (Medição Fiscal e Sistema de Alívio)": "Produção e processo",
    "Segurança Operacional, SGSO, Sistemas de Segurança e Gestão de Riscos": "Segurança operacional e riscos",
    "Manutenção, Inspeção e Integridade de Ativos": "Manutenção e integridade",
    "Segurança Ocupacional, Saúde e Meio Ambiente": "SMS ocupacional e ambiental",
    "Sistemas de Lastro, Estabilidade, Ancoragem e Posicionamento, Offloading e Tanques de Carga":
        "Lastro, ancoragem e offloading",
    "Operações submarinas, poços, risers e equipamentos submarinos": "Submarino, poços e risers",
    "Utilidades, geração de energia e sistemas auxiliares": "Utilidades e energia",
    "Logística, Suprimentos e Movimentação de Cargas": "Logística e cargas",
    "Gestão do Desempenho Empresarial (KPI)": "Gestão do desempenho (KPI)",
    "Descomissionamento e Gestão do Ciclo de Vida da Unidade": "Descomissionamento"}
CONJ = {"treino": "Treino", "validacao": "Validação", "teste": "Teste"}


def estilo() -> None:
    fam = "Inter" if any("Inter" in f.name for f in font_manager.fontManager.ttflist) else "DejaVu Sans"
    plt.rcParams.update({
        "font.family": fam, "font.size": 11, "axes.titlesize": 12, "axes.titleweight": "semibold",
        "axes.titlelocation": "left", "axes.titlepad": 10, "axes.labelsize": 11, "axes.labelcolor": TINTA2,
        "axes.edgecolor": TINTA3, "axes.linewidth": 0.8, "axes.spines.top": False, "axes.spines.right": False,
        "xtick.color": TINTA2, "ytick.color": TINTA2, "xtick.labelsize": 10, "ytick.labelsize": 10,
        "axes.grid": False, "grid.color": GRADE, "grid.linewidth": 0.8, "legend.frameon": False,
        "legend.fontsize": 10, "figure.dpi": 100, "savefig.dpi": 300, "savefig.bbox": "tight",
        "savefig.pad_inches": 0.08, "text.color": TINTA, "pdf.fonttype": 42})


def salvar(fig, nome: str) -> list[Path]:
    SAIDA.mkdir(parents=True, exist_ok=True)
    out = [SAIDA / f"{nome}.png", SAIDA / f"{nome}.pdf"]
    for p in out:
        fig.savefig(p, facecolor="white")
    plt.close(fig)
    return out


def _bootstrap(x: np.ndarray, n: int = 2000, semente: int = 7) -> tuple[float, float]:
    rng = np.random.default_rng(semente)
    m = rng.choice(x, size=(n, len(x)), replace=True).mean(axis=1)
    return float(np.percentile(m, 2.5)), float(np.percentile(m, 97.5))


def dados():
    banco = C.linhas(BANCO / "banco.jsonl")
    div = json.loads((BANCO / "splits" / "divisao.json").read_text(encoding="utf-8"))
    split = {i: s for s, ids in div["ids"].items() for i in ids}
    for b in banco:
        b["split"] = split[b["id"]]
    respostas: dict = {}
    with (FINAL_V2 / "pares.csv").open(encoding="utf-8-sig") as f:
        for r in csv.DictReader(C.sem_nul(f)):
            respostas.setdefault(r["uid"], {})[r["modelo"]] = (r["resposta_closed_book"], r["resposta_open_book"])
    return banco, div, respostas


# ------------------------------------------------------------------------------ análise das questões
def funil() -> list[Path]:
    rel = C.QA / "relatorios"
    ger = ["geracao_v23_completo", "geracao_conceitos", "geracao_variada", "geracao_tipo_decisao",
           "geracao_tipo_diagnostico", "geracao_tipo_procedimento", "experimento_ab_v1/bracos/B_v23"]
    tot = [json.loads((rel / g / "resultado.json").read_text(encoding="utf-8"))["total"] for g in ger]
    mont = json.loads((FINAL_V2 / "montagem.json").read_text(encoding="utf-8"))
    sust = json.loads((FINAL_V2 / "sustentacao.json").read_text(encoding="utf-8"))
    banco = sum(1 for _ in open(BANCO / "banco.jsonl", encoding="utf-8"))
    etapas = [("Propostas pelos geradores", sum(t["propostas"] for t in tot)),
              ("Aprovadas pelo auditor", sum(t["aprovadas_auditor"] for t in tot)),
              ("Únicas em cada geração¹", sum(f["questoes"] for f in mont["dataset"]["fontes"])),
              ("Únicas entre gerações", mont["dataset"]["n"]),
              ("Gabarito sustentado pelo documento", sust["sustentadas"]),
              ("Banco final (após revisão)", banco)]
    fig, ax = plt.subplots(figsize=(11, 4.6))
    ys = np.arange(len(etapas))[::-1]
    maxv = etapas[0][1]
    cores = [RAMPA[i + 1] for i in range(len(etapas))]
    for y, (nome, v), c in zip(ys, etapas, cores):
        ax.barh(y, v, left=(maxv - v) / 2, height=0.72, color=c, edgecolor="white", linewidth=2)
        ax.text(maxv / 2, y, f"{v:,}".replace(",", "."), ha="center", va="center", fontsize=12,
                fontweight="semibold", color="white" if c in RAMPA[3:] else TINTA)
        ax.text(-maxv * 0.015, y, nome, ha="right", va="center", fontsize=11, color=TINTA)
    antigas = 1019
    for k, ((y0, (_, a)), (_, b)) in enumerate(zip(zip(ys, etapas), etapas[1:])):
        rot = f"↓ {100 * (b - antigas) / a:.0f}%¹" if k == 1 else f"↓ {100 * b / a:.0f}%"
        ax.text(maxv * 1.01, y0 - 0.5, rot, ha="left", va="center", fontsize=9.5, color=TINTA3)
    ax.set_xlim(-maxv * 0.02, maxv * 1.08)
    ax.set_ylim(-0.6, len(etapas) - 0.4)
    ax.axis("off")
    ax.set_title("Construção do banco PetroQuest: da geração ao conjunto final", loc="left", x=-0.33)
    fig.text(0.01, -0.06, "Percentuais: fração retida de uma etapa para a seguinte. ¹ A etapa inclui 1.019 questões de "
             "gerações anteriores (banco antigo filtrado e v22),\nfora do percentual. Revisão final: unicidade do "
             "gabarito, forma, redundância e teto de 150 questões por tópico.", fontsize=8.5, color=TINTA3)
    return salvar(fig, "fig1_funil_construcao")


def composicao(banco: list) -> list[Path]:
    fig, (a, b) = plt.subplots(1, 2, figsize=(12.5, 4.8), gridspec_kw={"width_ratios": [1, 1.25], "wspace": 0.55})
    n = len(banco)
    ct = Counter(x["tipo"] for x in banco)
    tipos = sorted(TIPOS, key=lambda t: ct[t])
    a.barh(range(len(tipos)), [ct[t] for t in tipos], color=AZUL, height=0.62, edgecolor="white", linewidth=2)
    for i, t in enumerate(tipos):
        a.text(ct[t] + n * 0.006, i, f"{ct[t]}  ({100 * ct[t] / n:.1f}%)", va="center", fontsize=10, color=TINTA2)
    a.set_yticks(range(len(tipos)), [NOME_TIPO[t] for t in tipos], color=TINTA)
    a.set_xlim(0, max(ct.values()) * 1.32)
    a.set_title("(a) Tipo de questão")
    a.spines["left"].set_visible(False)
    a.tick_params(axis="y", length=0)
    a.xaxis.grid(True)
    a.set_axisbelow(True)
    a.set_xlabel("Questões")
    ca = Counter(AREA_CURTA.get(x["area"], x["area"]) for x in banco)
    areas = sorted(ca, key=lambda k: ca[k])
    b.barh(range(len(areas)), [ca[k] for k in areas], color=AZUL, height=0.62, edgecolor="white", linewidth=2)
    for i, k in enumerate(areas):
        b.text(ca[k] + n * 0.006, i, f"{ca[k]}", va="center", fontsize=10, color=TINTA2)
    b.set_yticks(range(len(areas)), areas, color=TINTA)
    b.set_xlim(0, max(ca.values()) * 1.15)
    b.set_title(f"(b) Área temática ({len({x['item'] for x in banco})} documentos)")
    b.spines["left"].set_visible(False)
    b.tick_params(axis="y", length=0)
    b.xaxis.grid(True)
    b.set_axisbelow(True)
    b.set_xlabel("Questões")
    return salvar(fig, "fig2_composicao_tipo_area")


def _colunas(ax, rotulos: list, valores: list, n: int, cores, titulo: str, base: dict | None = None,
             xfonte: float = 22, rot: float = 0) -> None:
    """Colunas para slide (número de questões no eixo y), com fontes grandes. `base` = {rótulo: (valor, cor)}
    desenha um segmento inferior destacado dentro da coluna (ex.: questões que nenhum modelo acerta)."""
    x = np.arange(len(rotulos))
    ax.bar(x, valores, color=cores, width=0.66, edgecolor="white", linewidth=2, zorder=2)
    topo = max(valores)
    for xi, r, v in zip(x, rotulos, valores):
        ax.text(xi, v + topo * 0.025, f"{v:,}".replace(",", "."), ha="center", va="bottom", fontsize=26,
                fontweight="bold", color=TINTA)
        ax.text(xi, v + topo * 0.15, f"{100 * v / n:.1f}%".replace(".", ","), ha="center", va="bottom",
                fontsize=21, color=TINTA2)
        if base and r in base:
            bv, bc = base[r]
            ax.bar(xi, bv, color=bc, width=0.66, edgecolor="white", linewidth=2, zorder=3)
            ax.text(xi, bv / 2, f"{bv}", ha="center", va="center", fontsize=22, fontweight="bold", color="white",
                    zorder=4)
    ax.set_xticks(x, rotulos, fontsize=xfonte, color=TINTA, rotation=rot, ha="right" if rot else "center",
                  rotation_mode="anchor" if rot else "default")
    ax.set_ylim(0, topo * 1.34)
    ax.tick_params(axis="y", labelsize=19)
    ax.tick_params(axis="x", length=0, pad=10)
    if titulo:
        ax.set_title(titulo, fontsize=27, pad=16)
    ax.yaxis.grid(True)
    ax.set_axisbelow(True)
    ax.set_ylabel("Questões", fontsize=21)
    ax.yaxis.set_major_locator(matplotlib.ticker.MaxNLocator(5))


def tipo_e_dificuldade(banco: list) -> list[Path]:
    """Tipo de questão e dificuldade empírica (colunas, fontes de slide); combinado e cada painel separado."""
    n = len(banco)
    ct = Counter(x["tipo"] for x in banco)
    tipos = sorted(TIPOS, key=lambda t: -ct[t])
    ce = Counter(x["dificuldade"]["estrato"] for x in banco)
    niveis = [("Fácil", ce["facil"]), ("Média", ce["media"]), ("Difícil", ce["dificil"] + ce["muito_dificil"])]
    base = None
    nota = ("Fácil = os 4 modelos independentes acertam sem o documento; difícil = o GPT-5 não acerta; "
            "média = o restante.")
    cores_dif = [ORDINAL4[0], ORDINAL4[1], ORDINAL4[2]]
    paineis = [("tipo", [NOME_TIPO[t] for t in tipos], [ct[t] for t in tipos], AZUL, "", None),
               ("dificuldade", [r for r, _ in niveis], [v for _, v in niveis], cores_dif, "", base)]
    arqs = []
    fig, axs = plt.subplots(1, 2, figsize=(14, 6.6), gridspec_kw={"width_ratios": [2.1, 1.15], "wspace": 0.3})
    for ax, (nome, rot, val, cor, tit, b) in zip(axs, paineis):
        _colunas(ax, rot, val, n, cor, tit, b, xfonte=19 if nome == "tipo" else 22, rot=30 if nome == "tipo" else 0)
    axs[1].set_ylabel("")
    fig.text(0.01, -0.2, nota, fontsize=13, color=TINTA3)
    arqs += salvar(fig, "fig2b_tipo_e_dificuldade")
    for nome, rot, val, cor, tit, b in paineis:
        fig, ax = plt.subplots(figsize=(11.5, 6.4) if nome == "tipo" else (6.8, 6.4))
        _colunas(ax, rot, val, n, cor, tit, b, xfonte=19 if nome == "tipo" else 22, rot=25 if nome == "tipo" else 0)
        arqs += salvar(fig, f"fig2{'c' if nome == 'tipo' else 'd'}_{nome}")
    return arqs


def divisao(banco: list) -> list[Path]:
    fig, ax = plt.subplots(figsize=(11, 3.6))
    conj = list(CONJ)
    for i, s in enumerate(conj):
        bs = [x for x in banco if x["split"] == s]
        c = Counter(x["dificuldade"]["estrato"] for x in bs)
        esq = 0.0
        for e, cor in zip(ESTRATOS, ORDINAL4):
            p = 100 * c[e] / len(bs)
            ax.barh(i, p, left=esq, color=cor, height=0.6, edgecolor="white", linewidth=2,
                    label=NOME_ESTRATO[e] if i == 0 else None)
            if p >= 6:
                ax.text(esq + p / 2, i, f"{p:.0f}%", ha="center", va="center", fontsize=10,
                        color="white" if cor != ORDINAL4[0] else TINTA)
            esq += p
        ax.text(101.5, i, f"n = {len(bs)}", va="center", fontsize=10, color=TINTA2)
    ax.set_yticks(range(len(conj)), [CONJ[s] for s in conj], color=TINTA, fontsize=11)
    ax.invert_yaxis()
    ax.set_xlim(0, 100)
    ax.set_xlabel("Questões (%)")
    ax.spines["left"].set_visible(False)
    ax.tick_params(axis="y", length=0)
    ax.legend(ncol=4, loc="upper left", bbox_to_anchor=(0, 1.2), handlelength=1.2, columnspacing=1.6)
    ax.set_title("Divisão 70/10/20 estratificada por dificuldade empírica, tipo, tópico e fonte", pad=34)
    return salvar(fig, "fig3_divisao_dificuldade")


# ------------------------------------------------------------------------------ desempenho dos modelos (teste)
def acuracia(teste: list) -> tuple[list[Path], dict]:
    res = {}
    fig, ax = plt.subplots(figsize=(11, 4.8))
    x = np.arange(len(MODELOS))
    w = 0.36
    for k, (cond, cor, rot) in enumerate((("sem_contexto", AZUL, "Sem documento"),
                                          ("com_contexto", LARANJA, "Com documento"))):
        vals, lo, hi = [], [], []
        for m in MODELOS:
            v = np.array([x["dificuldade"][cond][m] == "correta" for x in teste], dtype=float)
            a, b = _bootstrap(v)
            vals.append(100 * v.mean())
            lo.append(100 * (v.mean() - a))
            hi.append(100 * (b - v.mean()))
            res.setdefault(m, {})[cond] = (100 * v.mean(), 100 * a, 100 * b)
        pos = x + (k - 0.5) * w
        bars = ax.bar(pos, vals, w * 0.92, color=cor, label=rot, edgecolor="white", linewidth=1.5, zorder=2)
        bars[-1].set_hatch("////")
        bars[-1].set_edgecolor("white")
        ax.errorbar(pos, vals, yerr=[lo, hi], fmt="none", ecolor=TINTA2, elinewidth=1, capsize=3, zorder=3)
        for p, v, h in zip(pos, vals, hi):
            ax.text(p, v + h + 1.2, f"{v:.1f}", ha="center", va="bottom", fontsize=9.5, color=TINTA)
    ax.set_xticks(x, [NOME[m] for m in MODELOS], color=TINTA, fontsize=11)
    ax.set_ylim(0, 108)
    ax.set_yticks(range(0, 101, 20))
    ax.set_ylabel("Acurácia (%)")
    ax.yaxis.grid(True)
    ax.set_axisbelow(True)
    ax.tick_params(axis="x", length=0)
    ax.legend(loc="upper left", ncol=2, bbox_to_anchor=(0, 1.12))
    ax.set_title(f"Acurácia no conjunto de teste (n = {len(teste)}), resposta de até 20 palavras", pad=30)
    fig.text(0.01, -0.03, "Barras de erro: IC 95% por bootstrap. *GPT-5.4 gerou e auditou as questões: apenas "
             "referência (hachurado). Veredito do juiz GPT-5.4 contra o gabarito.", fontsize=8.5, color=TINTA3)
    return salvar(fig, "fig4_acuracia_modelos"), res


def por_tipo(teste: list) -> list[Path]:
    M = np.array([[100 * np.mean([x["dificuldade"]["sem_contexto"][m] == "correta" for x in teste if x["tipo"] == t])
                   for t in TIPOS] for m in MODELOS])
    nt = Counter(x["tipo"] for x in teste)
    fig, ax = plt.subplots(figsize=(11, 4.4))
    from matplotlib.colors import LinearSegmentedColormap
    cmap = LinearSegmentedColormap.from_list("azul", RAMPA)
    im = ax.imshow(M, cmap=cmap, vmin=20, vmax=100, aspect="auto")
    for i in range(M.shape[0]):
        for j in range(M.shape[1]):
            ax.text(j, i, f"{M[i, j]:.0f}", ha="center", va="center", fontsize=11,
                    color="white" if M[i, j] >= 62 else TINTA, fontweight="medium")
    ax.set_xticks(range(len(TIPOS)), [f"{NOME_TIPO[t]}\n(n = {nt[t]})" for t in TIPOS], fontsize=10, color=TINTA)
    ax.set_yticks(range(len(MODELOS)), [NOME[m] for m in MODELOS], fontsize=11, color=TINTA)
    ax.tick_params(length=0)
    for s in ax.spines.values():
        s.set_visible(False)
    ax.set_xticks(np.arange(-.5, len(TIPOS), 1), minor=True)
    ax.set_yticks(np.arange(-.5, len(MODELOS), 1), minor=True)
    ax.grid(which="minor", color="white", linewidth=2.5)
    ax.tick_params(which="minor", length=0)
    cb = fig.colorbar(im, ax=ax, fraction=0.025, pad=0.02)
    cb.outline.set_visible(False)
    cb.set_label("Acurácia sem documento (%)", color=TINTA2)
    ax.set_title("Acurácia sem documento por tipo de questão (teste)")
    return salvar(fig, "fig5_acuracia_por_tipo")


def por_area(teste: list) -> list[Path]:
    indep = ["gpt-4-1-mini", "gpt-4-1", "gpt-5-mini", "gpt-5"]
    areas = sorted({AREA_CURTA.get(x["area"], x["area"]) for x in teste})
    linhas = []
    for a in areas:
        xs = [x for x in teste if AREA_CURTA.get(x["area"], x["area"]) == a]
        sem = 100 * np.mean([x["dificuldade"]["sem_contexto"][m] == "correta" for x in xs for m in indep])
        com = 100 * np.mean([x["dificuldade"]["com_contexto"][m] == "correta" for x in xs for m in indep])
        linhas.append((a, sem, com, len(xs)))
    linhas.sort(key=lambda r: r[1])
    fig, ax = plt.subplots(figsize=(11, 4.9))
    for i, (a, sem, com, n) in enumerate(linhas):
        ax.plot([sem, com], [i, i], color=GRADE, linewidth=3, zorder=1, solid_capstyle="round")
        ax.scatter([sem], [i], s=70, color=AZUL, zorder=3, edgecolor="white", linewidth=1.5,
                   label="Sem documento" if i == 0 else None)
        ax.scatter([com], [i], s=70, color=LARANJA, zorder=3, edgecolor="white", linewidth=1.5,
                   label="Com documento" if i == 0 else None)
        ax.text(com + 1.2, i, f"+{com - sem:.0f}", va="center", fontsize=9.5, color=TINTA2)
    ax.set_yticks(range(len(linhas)), [f"{a}  (n = {n})" for a, _, _, n in linhas], color=TINTA, fontsize=10)
    ax.set_xlim(30, 100)
    ax.set_xlabel("Acurácia média dos 4 modelos independentes (%)")
    ax.xaxis.grid(True)
    ax.set_axisbelow(True)
    ax.spines["left"].set_visible(False)
    ax.tick_params(axis="y", length=0)
    ax.legend(loc="upper left", ncol=2, bbox_to_anchor=(0, 1.1))
    ax.set_title("Ganho com o documento por área temática (teste)", pad=30)
    return salvar(fig, "fig6_ganho_por_area")


def lexicais(teste: list, respostas: dict) -> tuple[list[Path], dict]:
    res = {}
    for m in MODELOS:
        for k, cond in enumerate(("sem", "com")):
            pares = [(respostas[x["uid"]][m][k], x["resposta"]) for x in teste
                     if m in respostas.get(x["uid"], {}) and respostas[x["uid"]][m][k]]
            res.setdefault(m, {})[cond] = {"f1": 100 * np.mean([LI.f1(a, g)[0] for a, g in pares]),
                                           "rouge_l": 100 * np.mean([LI.rouge_l(a, g) for a, g in pares]),
                                           "bleu": LI.bleu([a for a, _ in pares], [g for _, g in pares])}
    fig, axs = plt.subplots(1, 2, figsize=(12, 4.2), sharey=True, gridspec_kw={"wspace": 0.12})
    x = np.arange(len(MODELOS))
    w = 0.36
    for ax, (met, rot) in zip(axs, (("f1", "(a) F1 de tokens"), ("rouge_l", "(b) ROUGE-L"))):
        for k, (cond, cor, nome) in enumerate((("sem", AZUL, "Sem documento"), ("com", LARANJA, "Com documento"))):
            vals = [res[m][cond][met] for m in MODELOS]
            bars = ax.bar(x + (k - 0.5) * w, vals, w * 0.92, color=cor, label=nome, edgecolor="white", linewidth=1.5)
            bars[-1].set_hatch("////")
            for p, v in zip(x + (k - 0.5) * w, vals):
                ax.text(p, v + 0.6, f"{v:.0f}", ha="center", va="bottom", fontsize=9, color=TINTA)
        ax.set_xticks(x, [NOME[m] for m in MODELOS], fontsize=10, color=TINTA)
        ax.tick_params(axis="x", length=0)
        ax.yaxis.grid(True)
        ax.set_axisbelow(True)
        ax.set_title(rot)
    axs[0].set_ylabel("Pontuação (0–100)")
    axs[0].set_ylim(0, 60)
    fig.legend(*axs[0].get_legend_handles_labels(), loc="upper left", ncol=2, bbox_to_anchor=(0.06, 1.06))
    for ax in axs:
        ax.title.set_position((0, 1.02))
    fig.text(0.01, -0.04, "Sobreposição lexical entre a resposta do modelo e o gabarito (teste). Complementar ao juiz: "
             "respostas corretas com outras palavras pontuam pouco.", fontsize=8.5, color=TINTA3)
    return salvar(fig, "fig7_metricas_lexicais"), res


def gerar() -> dict:
    estilo()
    banco, div, respostas = dados()
    teste = [x for x in banco if x["split"] == "teste"]
    arqs = funil() + composicao(banco) + tipo_e_dificuldade(banco) + divisao(banco)
    a, acc = acuracia(teste)
    arqs += a + por_tipo(teste) + por_area(teste)
    b, lex = lexicais(teste, respostas)
    arqs += b
    resumo = {"teste_n": len(teste), "acuracia_teste": acc, "lexicais_teste": lex,
              "arquivos": [C.relativo(p) for p in arqs]}
    (SAIDA / "numeros.json").write_text(json.dumps(resumo, ensure_ascii=False, indent=1), encoding="utf-8")
    return resumo


if __name__ == "__main__":
    print(json.dumps(gerar(), ensure_ascii=False, indent=1)[:3000])
