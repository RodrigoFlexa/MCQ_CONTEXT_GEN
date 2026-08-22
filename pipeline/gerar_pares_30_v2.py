# Monta a avaliação comparativa pareada a partir dos datasets das duas
# condições: sorteia N_POR_TOPICO questões de cada condição em cada assunto,
# pareia-as e embaralha qual das duas ocupa a posição "A" no formulário.
#
# O balanceamento é feito DENTRO de cada assunto (metade dos pares com
# context-grounded em A), e não só no total: sorteio global poderia deixar um
# assunto com quase todos os context-grounded do mesmo lado, o que vira um
# confundidor entre assunto e posição na hora de analisar as respostas.
#
# Saídas em mcq_output/:
#   criar_form_avaliacao_comparativa_v2.gs  -> colar no script.google.com
#   mapa_avaliacao_comparativa_v2.csv       -> chave A/B (NAO enviar aos avaliadores)
#   pares_questoes_30_v2.jsonl              -> pares completos, rastreáveis
#   pares_questoes_30_v2_lado_a_lado.html   -> conferência visual sua
import csv
import html
import json
import random
from collections import Counter
from pathlib import Path

SEED = 42
N_POR_TOPICO = 6          # questões sorteadas por assunto em CADA condição
OUT_DIR = Path("mcq_output")


def load_jsonl(p):
    return [json.loads(l) for l in open(p, encoding="utf-8") if l.strip()]


ctx = load_jsonl(OUT_DIR / "dataset_mcq_petroles.jsonl")
ins = load_jsonl(OUT_DIR / "dataset_mcq_instrucao.jsonl")
for q in ctx:
    q["condition"] = "context-grounded"
for q in ins:
    q["condition"] = "instruction-only"

topics = sorted(set(q["topic"] for q in ctx) & set(q["topic"] for q in ins))
topic_names = {q["topic"]: q["topic_name"] for q in ctx + ins}

# ---------------------------------------------------------------- seleção ---
rng = random.Random(SEED)
pairs = []
for tid in topics:
    pool_c = [q for q in ctx if q["topic"] == tid]
    pool_i = [q for q in ins if q["topic"] == tid]
    n = min(N_POR_TOPICO, len(pool_c), len(pool_i))
    if n < N_POR_TOPICO:
        print(f"AVISO: {tid} permite só {n} pares "
              f"(ctx={len(pool_c)}, ins={len(pool_i)})")
    sel_c = rng.sample(pool_c, n)
    sel_i = rng.sample(pool_i, n)

    # metade dos pares deste assunto com context-grounded em A
    ctx_em_a = [True] * (n // 2) + [False] * (n - n // 2)
    rng.shuffle(ctx_em_a)

    for k in range(n):
        pairs.append({"pair_id": len(pairs) + 1, "topic": tid,
                      "topic_name": topic_names[tid],
                      "context_grounded": sel_c[k],
                      "instruction_only": sel_i[k],
                      "ctx_em_a": ctx_em_a[k]})

print(f"Pares gerados: {len(pairs)}")
print("Por assunto:", dict(Counter(p["topic"] for p in pairs)))

# ------------------------------------------------------ montagem do .gs ---
def js_escape(s):
    """Escapa para template literal JS (crase)."""
    return (str(s).replace("\\", "\\\\")
                  .replace("`", "\\`")
                  .replace("${", "\\${"))


def format_questao(q):
    corpo = q["stem"].strip() + "\n"
    for letra, alt in zip("ABCD", q["alternatives"]):
        corpo += f"\n{letra}) {alt}"
    return corpo


pares_js, mapa_rows = [], []
for p in pairs:
    c, i = p["context_grounded"], p["instruction_only"]
    if p["ctx_em_a"]:
        qa, qb = c, i
        cond_a, cond_b = "context-grounded", "instruction-only"
    else:
        qa, qb = i, c
        cond_a, cond_b = "instruction-only", "context-grounded"

    pares_js.append(
        "  {\n"
        f"    assunto: `{js_escape(p['topic_name'])}`,\n"
        f"    textoA: `{js_escape(format_questao(qa))}`,\n"
        f"    textoB: `{js_escape(format_questao(qb))}`\n"
        "  }")

    mapa_rows.append({
        "pair_id": p["pair_id"],
        "topic": p["topic"],
        "topic_name": p["topic_name"],
        "opcao_A_condition": cond_a,
        "opcao_A_gabarito": "ABCD"[qa["correct_answer_index"]],
        "opcao_A_difficulty": qa["difficulty"],
        "opcao_A_source_chunk_id": qa.get("source_chunk_id") or "",
        "opcao_A_stem_preview": qa["stem"][:80],
        "opcao_B_condition": cond_b,
        "opcao_B_gabarito": "ABCD"[qb["correct_answer_index"]],
        "opcao_B_difficulty": qb["difficulty"],
        "opcao_B_source_chunk_id": qb.get("source_chunk_id") or "",
        "opcao_B_stem_preview": qb["stem"][:80],
    })

pares_array = "var PARES = [\n" + ",\n".join(pares_js) + "\n];"

GS_TEMPLATE = '''/**
 * Cria o Google Forms de avaliação COMPARATIVA (pareada) das questões MCQ.
 * Cada par mostra uma questão do mesmo assunto gerada por dois processos
 * diferentes (context-grounded x instruction-only), com a posição A/B
 * embaralhada por par (avaliação cega). O balanceamento é feito dentro de
 * cada assunto: 3 pares com context-grounded em A e 3 com instruction-only
 * em A, totalizando 15/15. O mapeamento real A/B e os gabaritos estão em
 * mcq_output/mapa_avaliacao_comparativa_v2.csv (NAO enviar aos avaliadores).
 *
 * Fonte: dataset_mcq_petroles.jsonl x dataset_mcq_instrucao.jsonl
 * Gerado por gerar_pares_30_v2.py (SEED=42). Nao editar a mao.
 *
 * COMO USAR:
 * 1. Acesse script.google.com > Novo projeto, apague o conteudo e cole este arquivo.
 * 2. Execute a funcao buildForm e autorize as permissoes.
 * 3. Veja no log (Ctrl+Enter) os links do formulario (edicao e resposta).
 */

{PARES_ARRAY}

function buildForm() {
  var form = FormApp.create("Avaliação Comparativa de Questões");

  form.setDescription(
    "Nesta avaliação você verá " + PARES.length + " pares de questões de múltipla escolha. " +
    "As duas questões de cada par tratam do mesmo assunto, mas foram elaboradas por " +
    "processos de elaboração diferentes.\\n\\n" +
    "Sua tarefa NÃO é responder às questões nem demonstrar conhecimento do domínio. " +
    "Sua tarefa é julgar, em cada par, QUAL DAS DUAS ESTÁ MELHOR ELABORADA, considerando " +
    "clareza do enunciado, plausibilidade das alternativas, relevância prática e " +
    "correção técnica.\\n\\n" +
    "Atenção: \\"Opção A\\" e \\"Opção B\\" identificam as DUAS QUESTÕES do par. Não confundir " +
    "com as alternativas A), B), C) e D) que aparecem dentro de cada questão. Note também " +
    "que as questões estão embaralhadas, então a \\"Opção A\\" pode representar ora um tipo " +
    "de geração ora outro.\\n\\n" +
    "Tempo estimado: 40 a 50 minutos. Você pode salvar e retomar depois.\\n\\n" +
    "NOTA: RESPONDA INDIVIDUALMENTE.");

  form.setCollectEmail(true);   // remova esta linha para respostas anônimas
  form.setProgressBar(true);
  form.setShuffleQuestions(false);

  // ---------- identificação do avaliador ----------
  form.addTextItem().setTitle("Nome do avaliador").setRequired(true);
  form.addTextItem()
      .setTitle("Anos de experiência na indústria de óleo e gás")
      .setRequired(false);
  form.addTextItem()
      .setTitle("Área de atuação principal")
      .setHelpText("Ex.: processo, manutenção, integridade, metrologia, operação.")
      .setRequired(false);

  // ---------- um bloco por par ----------
  for (var i = 0; i < PARES.length; i++) {
    var p = PARES[i];
    var k = i + 1;

    form.addPageBreakItem()
        .setTitle("Par " + k + " de " + PARES.length)
        .setHelpText("Assunto: " + p.assunto);

    form.addSectionHeaderItem()
        .setTitle("OPÇÃO A")
        .setHelpText(p.textoA);

    form.addSectionHeaderItem()
        .setTitle("OPÇÃO B")
        .setHelpText(p.textoB);

    form.addMultipleChoiceItem()
        .setTitle(k + ".1 Qual opção foi melhor elaborada?")
        .setChoiceValues([
          "Opção A",
          "Opção B",
          "Não existe distinção, ambas possuem qualidades semelhantes"
        ])
        .setRequired(true);

    form.addCheckboxItem()
        .setTitle(k + ".2 Justifique sua escolha")
        .setHelpText("O que pesou na sua decisão?")
        .setChoiceValues([
          "Clareza do enunciado",
          "Qualidade das alternativas de resposta",
          "Relevância para a operação de FPSOs",
          "Correção técnica",
          "São semelhantes e não vejo como diferenciá-las"
        ])
        .showOtherOption(true)
        .setRequired(true);
  }

  // ---------- encerramento ----------
  form.addPageBreakItem().setTitle("Encerramento");
  form.addParagraphTextItem()
      .setTitle("Comentários gerais sobre o conjunto de questões (OPCIONAL)")
      .setRequired(false);

  Logger.log("Formulário criado com " + PARES.length + " pares.");
  Logger.log("Editar:    " + form.getEditUrl());
  Logger.log("Responder: " + form.getPublishedUrl());
}
'''

gs_path = OUT_DIR / "criar_form_avaliacao_comparativa_v2.gs"
gs_path.write_text(GS_TEMPLATE.replace("{PARES_ARRAY}", pares_array),
                   encoding="utf-8")

mapa_path = OUT_DIR / "mapa_avaliacao_comparativa_v2.csv"
with open(mapa_path, "w", newline="", encoding="utf-8-sig") as f:
    w = csv.DictWriter(f, fieldnames=list(mapa_rows[0].keys()))
    w.writeheader()
    w.writerows(mapa_rows)

jsonl_path = OUT_DIR / "pares_questoes_30_v2.jsonl"
with open(jsonl_path, "w", encoding="utf-8") as f:
    for p in pairs:
        f.write(json.dumps(p, ensure_ascii=False, default=str) + "\n")

# ------------------------------------------- conferência visual (HTML) ---
def q_card(q, lado):
    alts = "".join(
        f'<li class="{"ok" if idx == q["correct_answer_index"] else ""}">'
        f'<b>{chr(65+idx)})</b> {html.escape(a)}</li>'
        for idx, a in enumerate(q["alternatives"]))
    cls = "ctx" if q["condition"] == "context-grounded" else "ins"
    return (f'<div class="card {cls}"><div class="cond">OPÇÃO {lado} · '
            f'{q["condition"]} · {q["difficulty"]}</div>'
            f'<p class="stem">{html.escape(q["stem"])}</p>'
            f'<ul class="alts">{alts}</ul></div>')


body, atual = "", None
for p in pairs:
    if p["topic"] != atual:
        atual = p["topic"]
        body += f'<h2>{html.escape(p["topic_name"])}</h2>'
    c, i = p["context_grounded"], p["instruction_only"]
    qa, qb = (c, i) if p["ctx_em_a"] else (i, c)
    body += (f'<h3 class="pairnum">Par {p["pair_id"]}</h3>'
             f'<div class="pair">{q_card(qa, "A")}{q_card(qb, "B")}</div>')

CSS = """body{font-family:Georgia,serif;max-width:1150px;margin:24px auto;
padding:0 16px;color:#1a1a1a;line-height:1.45}
h1{font-size:1.4em} h2{margin-top:1.6em;border-bottom:2px solid #24567a;
padding-bottom:4px}
.pairnum{margin:10px 0 2px;font-size:.85em;color:#888}
.pair{display:flex;gap:14px;margin:0 0 14px}
.card{flex:1;border:1px solid #ccc;border-radius:8px;padding:12px 14px;
font-size:.86em}
.card.ctx{border-left:5px solid #24567a}
.card.ins{border-left:5px solid #b3702d}
.cond{font-weight:bold;font-size:.9em;color:#555;margin-bottom:6px}
.stem{font-weight:600} .alts{list-style:none;padding-left:0}
.alts li{margin:4px 0;padding:4px 8px;border-radius:4px;background:#f5f5f5}
.alts li.ok{background:#e3efe3;border:1px solid #7aa87a}"""

html_path = OUT_DIR / "pares_questoes_30_v2_lado_a_lado.html"
html_path.write_text(
    f'<!DOCTYPE html><html lang="pt-BR"><head><meta charset="utf-8">'
    f'<title>{len(pairs)} pares — conferência</title><style>{CSS}</style>'
    f'</head><body><h1>{len(pairs)} pares ({N_POR_TOPICO} por assunto) — '
    f'context-grounded × instruction-only</h1>'
    f'<p>Azul = context-grounded · Laranja = instruction-only · correta em '
    f'verde. <b>Uso interno</b>: revela as condições, não enviar aos '
    f'avaliadores.</p>{body}</body></html>', encoding="utf-8")

# ------------------------------------------------------------ validação ---
stems_c = [p["context_grounded"]["stem"] for p in pairs]
stems_i = [p["instruction_only"]["stem"] for p in pairs]
assert len(set(stems_c)) == len(stems_c), "questão context-grounded repetida"
assert len(set(stems_i)) == len(stems_i), "questão instruction-only repetida"
for p in pairs:
    assert p["context_grounded"]["topic"] == p["instruction_only"]["topic"], \
        f"par {p['pair_id']} mistura assuntos"

print("\nCondição na Opção A (total):",
      dict(Counter(r["opcao_A_condition"] for r in mapa_rows)))
print("Por assunto:")
for tid in topics:
    c = Counter(r["opcao_A_condition"] for r in mapa_rows if r["topic"] == tid)
    print(f"   {tid:<28} ctx_em_A={c['context-grounded']} "
          f"ins_em_A={c['instruction-only']}")

seq = [r["opcao_A_condition"] for r in mapa_rows]
streak = cur = 1
for a, b in zip(seq, seq[1:]):
    cur = cur + 1 if a == b else 1
    streak = max(streak, cur)
print(f"Maior sequência do mesmo tipo em A: {streak}")

print(f"\nSalvos:\n  {gs_path}\n  {mapa_path}\n  {jsonl_path}\n  {html_path}")
