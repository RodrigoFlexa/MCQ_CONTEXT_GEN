# %% [markdown]
# # Análise dos resultados e seleção estratificada de questões
#
# Este notebook: (1) calcula métricas comparativas entre as condições
# *context-grounded* e *instruction-only*; (2) seleciona uma amostra
# estratificada de N questões por **assunto × condição**, variando a
# dificuldade (amostragem round-robin fácil→média→difícil, determinística);
# (3) exporta a seleção em JSONL/CSV e em HTML lado a lado (ex.: para envio a
# especialistas ou inclusão no artigo).
#
# Entradas (em `mcq_output/`): `dataset_mcq_petroles.jsonl` (com contexto),
# `dataset_mcq_instrucao.jsonl` (sem contexto), `chunks_selecionados.jsonl`
# (rastreabilidade dos trechos-fonte).

# %%
import json, re, html, random, unicodedata
from pathlib import Path

import numpy as np
import pandas as pd

SEED = 42
random.seed(SEED); np.random.seed(SEED)

OUT_DIR = Path("mcq_output")
N_POR_GRUPO = 5          # questões por assunto × condição (3–5)
DIFF_ORDER = ["facil", "media", "dificil"]

def load_jsonl(p):
    return pd.DataFrame([json.loads(l) for l in open(p, encoding="utf-8")])

df_ctx = load_jsonl(OUT_DIR / "dataset_mcq_petroles.jsonl")
df_ins = load_jsonl(OUT_DIR / "dataset_mcq_instrucao.jsonl")
df_ctx["condition"] = "context-grounded"
df_ins["condition"] = "instruction-only"
chunks = {json.loads(l)["chunk_id"]: json.loads(l)["text"]
          for l in open(OUT_DIR / "chunks_selecionados.jsonl",
                        encoding="utf-8")}

TOPIC_NAMES = dict(df_ctx.groupby("topic")["topic_name"].first())
print(f"Com contexto: {len(df_ctx)} questões | Sem contexto: {len(df_ins)}")
print(f"Assuntos: {list(TOPIC_NAMES)}")

# %% [markdown]
# ## 1. Métricas comparativas

# %%
def norm(s):
    d = unicodedata.normalize("NFD", str(s).lower())
    return "".join(c for c in d if unicodedata.category(c) != "Mn")

STOP = set("que nao com para por uma dos das mais como ser sao esta deve "
           "devem qual quais sobre entre".split())

def content_toks(s):
    return set(re.findall(r"[a-z]{3,}", norm(s))) - STOP

def length_balance(q):
    lens = [len(a) for a in q.alternatives]
    lc = lens[q.correct_answer_index]
    others = [l for i, l in enumerate(lens) if i != q.correct_answer_index]
    return lc / (np.mean(others) + 1e-9)

def metric_rows(df):
    rows = []
    for (tid, cond), d in df.groupby(["topic", "condition"]):
        all_t = [t for s in d.stem for t in re.findall(r"[a-z]{3,}", norm(s))]
        rows.append({
            "assunto": tid, "condição": cond, "n": len(d),
            "fácil": (d.difficulty == "facil").sum(),
            "média": (d.difficulty == "media").sum(),
            "difícil": (d.difficulty == "dificil").sum(),
            "TTR": round(len(set(all_t)) / max(len(all_t), 1), 3),
            "palavras/enunciado": round(
                d.stem.str.split().str.len().mean(), 1),
            "palavras/alternativa": round(d.alternatives.apply(
                lambda a: np.mean([len(x.split()) for x in a])).mean(), 1),
            "razão_compr": round(d.apply(length_balance, axis=1).mean(), 2),
            "%cita_norma": round(d.stem.str.contains(
                "ANP|ISO|API|NR-|Portaria|Resolução|RTM").mean() * 100),
        })
    return pd.DataFrame(rows)

df_all = pd.concat([df_ctx, df_ins], ignore_index=True)
df_metrics = metric_rows(df_all).sort_values(["assunto", "condição"])
print(df_metrics.to_string(index=False))

# %%
# Grounding (só condição com contexto): fração dos termos de conteúdo da
# questão (enunciado + alternativas) presentes no trecho-fonte.
def grounding(q):
    src = content_toks(chunks.get(q.source_chunk_id, ""))
    qt = content_toks(q.stem + " " + " ".join(q.alternatives))
    return len(qt & src) / max(len(qt), 1)

df_ctx["grounding"] = df_ctx.apply(grounding, axis=1)
print("Grounding (context-grounded), por assunto:")
print(df_ctx.groupby("topic")["grounding"]
      .agg(["mean", "min", "max"]).round(2))

# %%
# Posições do gabarito e verificação de quase-duplicatas internas
print("Posição da resposta correta (por condição):")
print(df_all.groupby(["condition", "correct_answer_index"]).size()
      .unstack(fill_value=0))

import itertools
for cond, d in df_all.groupby("condition"):
    ts = [content_toks(s) for s in d.stem]
    nd = sum(1 for i, j in itertools.combinations(range(len(ts)), 2)
             if len(ts[i] & ts[j]) / max(len(ts[i] | ts[j]), 1) >= 0.6)
    print(f"{cond}: {nd} pares de enunciados com Jaccard ≥ 0.6")

# %% [markdown]
# ## 2. Seleção estratificada (N por assunto × condição, variando dificuldade)
#
# Round-robin sobre dificuldades (fácil → média → difícil): garante variedade
# quando disponível; se um estrato não tem questões suficientes, os demais
# compensam. Determinístico (SEED fixa). Para a condição com contexto, a
# seleção também evita repetir trecho-fonte.

# %%
def stratified_select(d, n, avoid_same_source=False):
    pools = {k: g.sample(frac=1, random_state=SEED).to_dict("records")
             for k, g in d.groupby("difficulty")}
    order = [k for k in DIFF_ORDER if k in pools]
    chosen, used_sources = [], set()
    while len(chosen) < n and any(pools.get(k) for k in order):
        for k in order:
            if len(chosen) >= n:
                break
            while pools.get(k):
                q = pools[k].pop(0)
                src = q.get("source_chunk_id")
                if avoid_same_source and src in used_sources and \
                        sum(len(p) for p in pools.values()) >= n - len(chosen):
                    continue  # tenta variar a fonte se houver folga
                chosen.append(q)
                used_sources.add(src)
                break
    return chosen

selection = []
for tid in TOPIC_NAMES:
    for cond, d in [("context-grounded", df_ctx), ("instruction-only", df_ins)]:
        sel = stratified_select(d[d.topic == tid], N_POR_GRUPO,
                                avoid_same_source=(cond == "context-grounded"))
        selection.extend(sel)
        diffs = pd.Series([q["difficulty"] for q in sel]).value_counts().to_dict()
        print(f"{tid} | {cond}: {len(sel)} questões {diffs}")

df_sel = pd.DataFrame(selection)
print(f"\nTotal selecionado: {len(df_sel)}")

# %% [markdown]
# ## 3. Exportação da seleção

# %%
sel_jsonl = OUT_DIR / "selecao_questoes.jsonl"
sel_csv = OUT_DIR / "selecao_questoes.csv"
with open(sel_jsonl, "w", encoding="utf-8") as f:
    for q in selection:
        f.write(json.dumps(
            {k: v for k, v in q.items() if k != "grounding"},
            ensure_ascii=False, default=str) + "\n")

flat = df_sel.copy()
for i in range(4):
    flat[f"alternativa_{chr(65+i)}"] = flat["alternatives"].str[i]
flat["gabarito"] = flat["correct_answer_index"].map(lambda i: chr(65 + i))
flat.drop(columns=["alternatives"]).to_csv(sel_csv, index=False,
                                           encoding="utf-8-sig")
print(f"Salvos:\n  {sel_jsonl}\n  {sel_csv}")

# %% [markdown]
# ## 4. Visualização lado a lado (HTML)
#
# Por assunto: coluna esquerda = context-grounded (azul), direita =
# instruction-only (laranja), pareadas por ordem de seleção. Alternativa
# correta destacada; trecho-fonte identificado quando existe.

# %%
def q_card(q, extra=""):
    cls = "ctx" if q["condition"] == "context-grounded" else "ins"
    alts = "".join(
        f'<li class="{"ok" if i == q["correct_answer_index"] else ""}">'
        f'<b>{chr(65+i)})</b> {html.escape(a)}</li>'
        for i, a in enumerate(q["alternatives"]))
    return (f'<div class="card {cls}"><div class="cond">'
            f'{q["condition"]} · {q["difficulty"]}{extra}</div>'
            f'<p class="stem">{html.escape(q["stem"])}</p>'
            f'<ul class="alts">{alts}</ul>'
            f'<p class="just"><b>Justificativa:</b> '
            f'{html.escape(q["correct_reason"])}</p></div>')

body = ""
for tid, tname in TOPIC_NAMES.items():
    body += f"<h2>{html.escape(tname)}</h2>"
    sc = [q for q in selection
          if q["topic"] == tid and q["condition"] == "context-grounded"]
    si = [q for q in selection
          if q["topic"] == tid and q["condition"] == "instruction-only"]
    for k in range(max(len(sc), len(si))):
        left = q_card(sc[k], f'<br><span class="src">fonte: '
                      f'{html.escape(str(sc[k]["source_chunk_id"]))}</span>') \
               if k < len(sc) else '<div class="card"></div>'
        right = q_card(si[k]) if k < len(si) else '<div class="card"></div>'
        body += f'<div class="pair">{left}{right}</div>'

CSS = """body{font-family:Georgia,serif;max-width:1150px;margin:24px auto;
padding:0 16px;color:#1a1a1a;line-height:1.45}
h1{font-size:1.4em} h2{margin-top:1.6em;border-bottom:2px solid #24567a;
padding-bottom:4px}
.pair{display:flex;gap:14px;margin:14px 0}
.card{flex:1;border:1px solid #ccc;border-radius:8px;padding:12px 14px;
font-size:.86em}
.card.ctx{border-left:5px solid #24567a}
.card.ins{border-left:5px solid #b3702d}
.cond{font-weight:bold;font-size:.9em;color:#555;margin-bottom:6px}
.src{font-weight:normal;color:#888;font-size:.9em}
.stem{font-weight:600} .alts{list-style:none;padding-left:0}
.alts li{margin:4px 0;padding:4px 8px;border-radius:4px;background:#f5f5f5}
.alts li.ok{background:#e3efe3;border:1px solid #7aa87a}
.just{color:#444;font-size:.95em}"""

html_doc = (f'<!DOCTYPE html><html lang="pt-BR"><head><meta charset="utf-8">'
            f'<title>Seleção de questões — lado a lado</title>'
            f'<style>{CSS}</style></head><body>'
            f'<h1>Seleção estratificada — {N_POR_GRUPO} questões por assunto '
            f'× condição</h1>'
            f'<p>Azul = context-grounded · Laranja = instruction-only · '
            f'correta destacada em verde.</p>{body}</body></html>')
sel_html = OUT_DIR / "selecao_questoes_lado_a_lado.html"
sel_html.write_text(html_doc, encoding="utf-8")
print(f"Salvo: {sel_html}")

# %% [markdown]
# ## Notas
#
# - A seleção é **determinística** (SEED=42): re-executar reproduz a mesma
#   amostra — importante para rastreabilidade no artigo.
# - Para avaliação humana **cega**, use `selecao_questoes.csv` removendo as
#   colunas `condition`, `source_chunk_id`, `source_file` e `generation_mode`
#   e embaralhando as linhas antes de enviar aos especialistas.
# - `N_POR_GRUPO` pode ser ajustado (3–5) na célula de configuração.
