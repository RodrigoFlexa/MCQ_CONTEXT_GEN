# %% [markdown]
# # Geração MCQ *instruction-only* (baseline) — 5 assuntos
#
# Condição de comparação para a geração fundamentada em contexto
# (`geracao_mcq_petroles.py`). O LLM **não** recebe trechos do corpus: o
# placeholder `{content}` do prompt v13 é preenchido apenas com a **descrição
# do assunto** — a mesma descrição, *verbatim*, usada como query de
# recuperação na condição *context-grounded*. Tudo o mais é idêntico entre
# condições (prompt, modelo, schema, validação, QC), de modo que a única
# variável experimental é o condicionamento:
#
# | Condição | `{content}` | Fonte do conhecimento |
# |---|---|---|
# | *Context-grounded* | trecho recuperado do corpus | documento |
# | *Instruction-only* | descrição do assunto | conhecimento paramétrico |
#
# Gera a **mesma quantidade** da condição com contexto: 10 questões por
# assunto (50 no total). Como não há trecho variando entre chamadas,
# duplicatas entre lotes são esperadas; a taxa de duplicação por assunto é
# registrada como métrica comparativa.

# %%
import os, re, sys, json, random, hashlib, unicodedata, datetime
from pathlib import Path

import numpy as np
import pandas as pd

# GPU configurável pelo terminal:
#   python geracao_mcq_instrucao.py --gpu 3
#   (ou: CUDA_VISIBLE_DEVICES=3 python geracao_mcq_instrucao.py)
# Sem --gpu e sem variável exportada, usa todas as GPUs visíveis.
# if "--gpu" in sys.argv:
#     os.environ["CUDA_VISIBLE_DEVICES"] = sys.argv[sys.argv.index("--gpu") + 1]
os.environ.setdefault("CUDA_VISIBLE_DEVICES", "3")
print(f"CUDA_VISIBLE_DEVICES = {os.environ.get('CUDA_VISIBLE_DEVICES', '(todas)')}")

SEED = 42
random.seed(SEED); np.random.seed(SEED)

BASE_DIR = Path(".")
OUT_DIR = BASE_DIR / "mcq_output"
OUT_DIR.mkdir(exist_ok=True)

# Descrições idênticas às do pipeline context-grounded (insumo único)
TOPICS = {
    "gestao_desempenho": {
        "nome": "Gestão do Desempenho",
        "descricao": (
            "As questões devem abordar aspectos de gestão e desempenho de "
            "FPSOs, incluindo planejamento e controle operacional, gestão de "
            "indicadores e metas, eficiência e disponibilidade dos sistemas, "
            "confiabilidade dos ativos, gestão de riscos, custos, perdas de "
            "produção, desempenho das equipes e processos de melhoria "
            "contínua ao longo do ciclo de vida da unidade."
        ),
    },
    "medicao_fiscal_offloading": {
        "nome": ("Medição Fiscal de óleo, medição fiscal de gás e "
                 "transferência de custódia em operações de offloading"),
        "descricao": (
            "As questões devem abordar a medição fiscal de petróleo e gás "
            "natural e a medição de transferência de custódia nas operações "
            "de offloading de FPSOs, incluindo requisitos de projeto, "
            "instalação, operação, calibração, verificação, manutenção e "
            "controle metrológico dos sistemas de medição, tratamento e "
            "validação dos dados, determinação de volumes e propriedades dos "
            "fluidos, gestão de incertezas, rastreabilidade, registros, "
            "auditorias, comunicação de falhas e atendimento à "
            "regulamentação vigente da ANP."
        ),
    },
    "produtos_quimicos": {
        "nome": "Produtos químicos",
        "descricao": (
            "As questões devem abordar a seleção, aplicação, dosagem, "
            "armazenamento, manuseio, monitoramento de desempenho e "
            "compatibilidade dos produtos químicos utilizados em FPSOs, "
            "incluindo aqueles empregados no processamento do óleo, no "
            "tratamento da água produzida para descarte, no condicionamento "
            "da água do mar para injeção no reservatório — inclusive em "
            "sistemas de remoção de sulfato (SRU) e desaeração —, no "
            "tratamento do gás, como inibidores de corrosão e MEG, e na "
            "prevenção de hidratos, incrustações, corrosão, emulsões, "
            "espuma, depósitos e crescimento microbiológico em sistemas "
            "topside e subsea."
        ),
    },
    "tratamento_agua_produzida": {
        "nome": "Tratamento de água produzida para descarte",
        "descricao": (
            "As questões devem abordar o projeto, a operação, o controle e a "
            "otimização dos sistemas de tratamento de água produzida para "
            "descarte no mar em FPSOs, incluindo separação gravitacional, "
            "hidrociclones, unidades de flotação e skimming vessels, dosagem "
            "de produtos químicos, controle das condições de processo, "
            "tratamento e destinação de correntes oleosas, recirculação ou "
            "desvio da água fora de especificação, monitoramento do teor de "
            "óleos e graxas (TOG), amostragem, análises laboratoriais e "
            "instrumentos on-line, avaliação da eficiência dos equipamentos, "
            "diagnóstico de falhas e atendimento à legislação ambiental "
            "brasileira, às condicionantes do licenciamento e aos requisitos "
            "aplicáveis dos órgãos reguladores e ambientais."
        ),
    },
    "injecao_agua_mar": {
        "nome": ("Sistema de captação e tratamento de água do mar para "
                 "injeção no reservatório"),
        "descricao": (
            "As questões devem abordar o projeto, a operação, o controle e a "
            "otimização dos sistemas de captação, tratamento e injeção de "
            "água do mar em reservatórios a partir de FPSOs, incluindo "
            "caixas de mar, bombas de captação e de injeção, dosagem de "
            "biocidas, sequestrantes de oxigênio, inibidores de corrosão, "
            "incrustação e espuma, etapas de filtração, unidades de remoção "
            "de sulfato (SRU), sistemas de desaeração, controle "
            "microbiológico, monitoramento da qualidade da água, "
            "compatibilidade com a formação, prevenção de souring, "
            "incrustações e corrosão, avaliação do desempenho dos "
            "equipamentos e garantia da vazão, pressão e especificação "
            "requeridas para a injeção."
        ),
    },
}

# Geração — mesma quantidade da condição context-grounded
N_QUESTOES_POR_ASSUNTO = 10
Q_PER_CALL = 10          # questões por chamada (lotes independentes)
N_ALTERNATIVES = 4
MAX_RETRIES = 3
MAX_CALLS_POR_ASSUNTO = 8  # teto de chamadas (folga p/ duplicatas)

# Orçamento de saída generoso: modelos com raciocínio explícito (<think>)
# gastam a maior parte dos tokens antes de emitir o JSON. Aqui cada chamada
# pede Q_PER_CALL questões de uma vez, então a saída é ainda mais longa que
# na condição context-grounded.
MAX_NEW_TOKENS = 16384
TEMPERATURE = 0.7            # 1ª tentativa
RETRY_TEMPERATURE = 0.3      # retentativas: mais determinístico p/ formato
ENABLE_THINKING = False      # desliga <think> quando o chat template suporta

LLM_BACKEND = "transformers"  # "anthropic" | "openai" | "ollama" | "transformers" | "mock"
LLM_MODEL = {
    "anthropic": "claude-sonnet-4-5",
    "openai": "gpt-4o",
    "ollama": "qwen3.6:27b",
    "transformers": "Qwen/Qwen3.6-27B",  # ou "Qwen/Qwen3.6-35B-A3B" (MoE, + rápido)
    "mock": "mock",
}[LLM_BACKEND]

from prompt_mcq_generation import PORTUGUESE_V15, build_content
PROMPT = PORTUGUESE_V15
CONTENT_FORMAT = "assunto"  # registrado em cada questão
print(f"Prompt: {PROMPT.version} | Backend: {LLM_BACKEND} ({LLM_MODEL})")
print(f"Condição: instruction-only | {len(TOPICS)} assuntos × "
      f"{N_QUESTOES_POR_ASSUNTO} questões")

# %% [markdown]
# ## Backends de LLM (idênticos ao pipeline principal)

# %%
def strip_reasoning(text: str) -> str:
    """Remove o traço de raciocínio de modelos que emitem <think>...</think>.

    Trata também o caso em que só o fechamento aparece (alguns templates já
    abrem o bloco no prompt) — daí a busca pelo último `</think>` em vez de
    um par completo, que era o que a versão anterior exigia.
    """
    if "</think>" in text:
        return text.rsplit("</think>", 1)[1]
    return text


class LLMClient:
    def generate(self, system: str, user: str, temperature=None) -> str:
        raise NotImplementedError


class AnthropicClient(LLMClient):
    def __init__(self, model):
        import anthropic
        self.client = anthropic.Anthropic()  # ANTHROPIC_API_KEY no ambiente
        self.model = model
    def generate(self, system, user, temperature=None):
        kw = {} if temperature is None else {"temperature": temperature}
        r = self.client.messages.create(model=self.model,
                                        max_tokens=MAX_NEW_TOKENS,
                                        system=system,
                                        messages=[{"role": "user",
                                                   "content": user}], **kw)
        return r.content[0].text


class OpenAIClient(LLMClient):
    def __init__(self, model):
        from openai import OpenAI
        self.client = OpenAI()  # OPENAI_API_KEY no ambiente
        self.model = model
    def generate(self, system, user, temperature=None):
        kw = {} if temperature is None else {"temperature": temperature}
        r = self.client.chat.completions.create(
            model=self.model,
            messages=[{"role": "system", "content": system},
                      {"role": "user", "content": user}], **kw)
        return r.choices[0].message.content


class OllamaClient(LLMClient):
    def __init__(self, model, host="http://localhost:11434"):
        self.model, self.host = model, host
    def generate(self, system, user, temperature=None):
        import urllib.request
        opts = {"num_predict": MAX_NEW_TOKENS}
        if temperature is not None:
            opts["temperature"] = temperature
        req = urllib.request.Request(
            f"{self.host}/api/chat", method="POST",
            headers={"Content-Type": "application/json"},
            data=json.dumps({"model": self.model, "stream": False,
                             "options": opts,
                             "messages": [
                                 {"role": "system", "content": system},
                                 {"role": "user", "content": user}]}).encode())
        with urllib.request.urlopen(req, timeout=600) as resp:
            return json.loads(resp.read())["message"]["content"]


class TransformersClient(LLMClient):
    """Inferência local via Hugging Face Transformers (ex.: H100)."""
    def __init__(self, model_id, max_new_tokens=MAX_NEW_TOKENS,
                 temperature=TEMPERATURE):
        import torch
        from transformers import AutoTokenizer
        self.max_new_tokens, self.temperature = max_new_tokens, temperature
        self.truncated = 0  # nº de respostas cortadas no limite de tokens
        self.tok = AutoTokenizer.from_pretrained(model_id)
        try:
            from transformers import AutoModelForCausalLM
            self.model = AutoModelForCausalLM.from_pretrained(
                model_id, torch_dtype=torch.bfloat16, device_map="auto")
        except Exception:  # model cards multimodais (Qwen3.6 omni)
            from transformers import AutoModelForMultimodalLM, AutoProcessor
            self.tok = AutoProcessor.from_pretrained(model_id)
            self.model = AutoModelForMultimodalLM.from_pretrained(
                model_id, torch_dtype=torch.bfloat16, device_map="auto")
    def generate(self, system, user, temperature=None):
        messages = [{"role": "system", "content": system},
                    {"role": "user", "content": user}]
        kw = dict(add_generation_prompt=True, tokenize=True,
                  return_dict=True, return_tensors="pt")
        try:  # templates da família Qwen aceitam enable_thinking
            inputs = self.tok.apply_chat_template(
                messages, enable_thinking=ENABLE_THINKING, **kw)
        except TypeError:
            inputs = self.tok.apply_chat_template(messages, **kw)
        inputs = inputs.to(self.model.device)
        t = self.temperature if temperature is None else temperature
        out = self.model.generate(**inputs,
                                  max_new_tokens=self.max_new_tokens,
                                  do_sample=t > 0,
                                  temperature=t if t > 0 else None)
        n_in = inputs["input_ids"].shape[-1]
        if out.shape[-1] - n_in >= self.max_new_tokens:
            self.truncated += 1
        text = self.tok.decode(out[0][n_in:], skip_special_tokens=True)
        return strip_reasoning(text)


class MockClient(LLMClient):
    """Dry-run p/ validar o pipeline sem custo de API."""
    _themes = ["indicadores de disponibilidade", "metas de eficiência",
               "confiabilidade de ativos", "gestão de riscos",
               "custos de manutenção", "perdas de produção",
               "medição fiscal", "calibração de medidores", "flare e tocha",
               "despressurização", "inspeção baseada em risco", "corrosão"]
    _stems = [
        "Em um FPSO, considere um cenário de {th} com restrições de {x}: qual conduta prioriza o desempenho global da unidade?",
        "Durante a análise crítica mensal, a equipe identifica desvio em {th} associado a {x}: qual deve ser a primeira ação?",
        "Um gestor precisa decidir entre investir em {th} ou mitigar {x}: qual critério de decisão é tecnicamente mais adequado?",
        "Ao estruturar o plano anual da unidade, como o aspecto de {th} deve ser integrado ao tratamento de {x}?",
        "Após um período de queda de desempenho atribuída a {th}, que relação causal com {x} deve ser investigada primeiro?",
    ]
    _stress = ["orçamento e prazo", "janela de parada programada",
               "indisponibilidade de sobressalentes", "metas regulatórias",
               "turnos reduzidos de equipe", "contratos de afretamento"]
    def generate(self, system, user, temperature=None):
        qs = []
        for i in range(Q_PER_CALL):
            th = random.choice(self._themes)
            nonce = hashlib.md5(f"{random.random()}".encode()).hexdigest()[:6]
            qs.append({
                "stem": "[MOCK " + nonce + "] " +
                        random.choice(self._stems).format(
                            th=th, x=random.choice(self._stress)),
                "alternatives": [f"Alternativa {c} ({nonce})" for c in "ABCD"],
                "correct_answer_index": random.randrange(4),
                "difficulty": random.choice(["facil", "media", "dificil"]),
                "correct_reason": "Justificativa simulada.",
            })
        return "```json\n" + json.dumps(qs, ensure_ascii=False) + "\n```"


def make_client(backend, model):
    return {"anthropic": AnthropicClient, "openai": OpenAIClient,
            "ollama": OllamaClient, "transformers": TransformersClient,
            "mock": lambda m: MockClient()}[backend](model)


client = make_client(LLM_BACKEND, LLM_MODEL)

# %% [markdown]
# ## Parsing e validação estrutural (idênticos ao pipeline principal)

# %%
FENCE_RE = re.compile(r"```(?:json)?\s*(.*?)```", re.DOTALL)
TRAILING_COMMA_RE = re.compile(r",\s*([\]}])")

def normalize(text: str) -> str:
    dec = unicodedata.normalize("NFD", text.lower())
    return "".join(c for c in dec if unicodedata.category(c) != "Mn")


def extract_json_array(raw: str):
    """Extrai o primeiro array JSON válido da resposta do LLM (robusto a
    texto extra, blocos cercados e vírgulas finais)."""
    dec = json.JSONDecoder()
    variants = [raw, TRAILING_COMMA_RE.sub(r"\1", raw)]
    for text in variants:
        for m in FENCE_RE.finditer(text):
            try:
                data = json.loads(m.group(1).strip())
                if isinstance(data, list) and data \
                        and all(isinstance(x, dict) for x in data):
                    return data
            except Exception:
                pass
        for i, ch in enumerate(text):
            if ch == "[":
                try:
                    data, _ = dec.raw_decode(text[i:])
                    if isinstance(data, list) and data \
                            and all(isinstance(x, dict) for x in data):
                        return data
                except Exception:
                    continue
    raise ValueError("Nenhum array JSON válido na resposta")


# Detector de vício "test-wiseness": distratores com linguagem absolutista
# concentrada (e correta sem) permitem eliminar alternativas sem conhecimento.
ABSOLUTIST_MARKERS = re.compile("|".join([
    r"\bapenas\b", r"\bsomente\b", r"\bexclusivamente\b", r"\bunicamente\b",
    r"\bnunca\b", r"\bjamais\b", r"\btodos os\b", r"\btodas as\b",
    r"elimina(ndo)? a necessidade", r"\bdispensa(ndo)?\b",
    r"sem necessidade de", r"sem considerar", r"\bindependentemente\b",
    r"\bisolad[oa]\b", r"substituir todos"]))

def has_absolutist_cue(q):
    """True se ≥2 distratores têm marcador absolutista e a correta nenhum."""
    c = q["correct_answer_index"]
    d_marks = sum(bool(ABSOLUTIST_MARKERS.search(normalize(a)))
                  for i, a in enumerate(q["alternatives"]) if i != c)
    c_mark = bool(ABSOLUTIST_MARKERS.search(normalize(q["alternatives"][c])))
    return d_marks >= 2 and not c_mark

CUE_REJECTED = {"n": 0}  # contador global p/ relatório

def parse_questions(raw: str):
    data = extract_json_array(raw)
    valid = []
    for q in data:
        if not all(k in q for k in ("stem", "alternatives",
                                    "correct_answer_index", "difficulty",
                                    "correct_reason")):
            continue
        if (len(q["alternatives"]) != N_ALTERNATIVES
                or not isinstance(q["correct_answer_index"], int)
                or not 0 <= q["correct_answer_index"] < N_ALTERNATIVES
                or q["difficulty"] not in ("facil", "media", "dificil")
                or len(str(q["stem"]).split()) < 8):
            continue
        if has_absolutist_cue(q):
            CUE_REJECTED["n"] += 1
            continue  # rejeita: lotes seguintes compensam
        valid.append(q)
    return valid


def is_duplicate(stem, seen_token_sets, threshold=0.75):
    toks = set(normalize(stem).split())
    return any(len(toks & s) / max(len(toks | s), 1) >= threshold
               for s in seen_token_sets)

# %% [markdown]
# ## Geração — lotes independentes por assunto
#
# Cada chamada é independente (mesmo prompt, sem histórico). Duplicatas entre
# lotes são removidas on-line e contabilizadas por assunto.

# %%
# Salvamento incremental: cada questão aceita é gravada imediatamente aqui.
# Acompanhe em outro terminal com:  tail -f mcq_output/dataset_mcq_instrucao_parcial.jsonl
PARTIAL_PATH = OUT_DIR / "dataset_mcq_instrucao_parcial.jsonl"
if PARTIAL_PATH.exists() and PARTIAL_PATH.stat().st_size:
    # preserva o parcial da execução anterior antes de zerar
    ts = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    PARTIAL_PATH.rename(OUT_DIR / f"dataset_mcq_instrucao_parcial_{ts}.jsonl")
PARTIAL_PATH.write_text("", encoding="utf-8")

def save_partial(q):
    with open(PARTIAL_PATH, "a", encoding="utf-8") as f:
        f.write(json.dumps(q, ensure_ascii=False) + "\n")


all_questions = []
dup_stats = {}

for tid, t in TOPICS.items():
    print(f"\nGerando: {t['nome']}")
    user_prompt = PROMPT.question_template.format(
        n_questions=Q_PER_CALL, n_alternatives=N_ALTERNATIVES,
        content=build_content(t["descricao"]))
    questions, seen = [], []
    n_calls = n_gen_total = n_dup = 0
    while len(questions) < N_QUESTOES_POR_ASSUNTO \
            and n_calls < MAX_CALLS_POR_ASSUNTO:
        n_calls += 1
        qs = []
        for attempt in range(MAX_RETRIES + 1):
            try:
                # Nas retentativas, reforça o formato e reduz a temperatura:
                # a 1ª falha é quase sempre de formatação, não de conteúdo.
                prompt = user_prompt if attempt == 0 else (
                    user_prompt + "\n\nResponda APENAS com o array JSON, sem "
                    "texto antes ou depois e sem comentários.")
                raw = client.generate(PROMPT.system_message, prompt,
                                      temperature=None if attempt == 0
                                      else RETRY_TEMPERATURE)
                qs = parse_questions(raw)
                if not qs:
                    raise ValueError("Nenhuma questão válida no lote")
                break
            except Exception as e:
                if attempt == MAX_RETRIES:
                    print(f"  Lote {n_calls} falhou: {e}")
                    qs = []
        n_gen_total += len(qs)
        for q in qs:
            if len(questions) >= N_QUESTOES_POR_ASSUNTO:
                break
            if is_duplicate(q["stem"], seen):
                n_dup += 1
                continue
            seen.append(set(normalize(q["stem"]).split()))
            q.update({
                "topic": tid,
                "topic_name": t["nome"],
                "generation_mode": "instruction_only",
                "content_format": CONTENT_FORMAT,
                "source_chunk_id": None,
                "source_file": None,
                "prompt_version": PROMPT.version,
                "model": f"{LLM_BACKEND}/{LLM_MODEL}",
                "batch": n_calls,
                "generated_at": datetime.datetime.now()
                                .isoformat(timespec="seconds"),
            })
            questions.append(q)
            save_partial(q)
        print(f"  Lote {n_calls}: geradas {len(qs)}, "
              f"acumuladas {len(questions)}, duplicatas {n_dup}")
    dup_stats[tid] = {"chamadas": n_calls, "geradas_total": n_gen_total,
                      "duplicatas": n_dup,
                      "taxa_dup": round(n_dup / max(n_gen_total, 1), 3)}
    all_questions.extend(questions)

print("\nTaxa de duplicação por assunto:")
print(pd.DataFrame(dup_stats).T)

# %% [markdown]
# ## Controle de qualidade e estatísticas (idênticos ao pipeline principal)

# %%
def rebalance_positions(questions):
    by_topic = {}
    for q in questions:
        by_topic.setdefault(q["topic"], []).append(q)
    for qs in by_topic.values():
        for i, q in enumerate(qs):
            target = i % N_ALTERNATIVES
            alts = q["alternatives"][:]
            correct = alts.pop(q["correct_answer_index"])
            random.shuffle(alts)
            q["alternatives"] = alts[:target] + [correct] + alts[target:]
            q["correct_answer_index"] = target
    return questions


all_questions = rebalance_positions(all_questions)
df_q = pd.DataFrame(all_questions)

print("Questões por assunto:")
print(df_q.groupby("topic").size())
print("\nDistribuição de dificuldade (alvo ~30/40/30):")
print(df_q.groupby(["topic", "difficulty"]).size().unstack(fill_value=0))
print("\nPosição da resposta correta:")
print(df_q.groupby(["topic", "correct_answer_index"]).size()
      .unstack(fill_value=0))

def length_balance(q):
    lens = [len(a) for a in q["alternatives"]]
    lc = lens[q["correct_answer_index"]]
    others = [l for i, l in enumerate(lens) if i != q["correct_answer_index"]]
    return lc / (sum(others) / len(others) + 1e-9)

ratios = df_q.apply(length_balance, axis=1)
print(f"\nRazão de comprimento correta/distratores: média={ratios.mean():.2f}, "
      f"desvio={ratios.std():.2f}")

if getattr(client, "truncated", 0):
    print(f"\nRespostas cortadas no limite de {MAX_NEW_TOKENS} tokens: "
          f"{client.truncated} — se for alto, aumente MAX_NEW_TOKENS")

print(f"\nQuestões rejeitadas pelo detector de linguagem absolutista: "
      f"{CUE_REJECTED['n']}")
remaining = int(df_q.apply(lambda q: has_absolutist_cue(q), axis=1).sum())
print(f"Questões no dataset final ainda com padrão absolutista: {remaining} "
      f"(esperado: 0)")

# %% [markdown]
# ## Exportação

# %%
jsonl_path = OUT_DIR / "dataset_mcq_instrucao.jsonl"
csv_path = OUT_DIR / "dataset_mcq_instrucao.csv"
with open(jsonl_path, "w", encoding="utf-8") as f:
    for q in all_questions:
        f.write(json.dumps(q, ensure_ascii=False) + "\n")

flat = df_q.copy()
for i in range(N_ALTERNATIVES):
    flat[f"alternativa_{chr(65+i)}"] = flat["alternatives"].str[i]
flat["gabarito"] = flat["correct_answer_index"].map(lambda i: chr(65 + i))
flat.drop(columns=["alternatives"]).to_csv(csv_path, index=False,
                                           encoding="utf-8-sig")
print(f"Salvos:\n  {jsonl_path}\n  {csv_path}")

# %% [markdown]
# ## Comparação com a condição *context-grounded*
#
# Métricas automáticas por assunto. A comparação decisiva para o artigo é a
# avaliação humana cega (especialistas julgam questões das duas condições sem
# saber a origem).

# %%
ctx_path = OUT_DIR / "dataset_mcq_petroles.jsonl"
if ctx_path.exists():
    df_ctx = pd.DataFrame([json.loads(l) for l in
                           open(ctx_path, encoding="utf-8")])
    def stats_row(df, cond, tid):
        d = df[df.topic == tid]
        if not len(d):
            return None
        toks = [t for s in d["stem"] for t in normalize(s).split()]
        return {
            "assunto": tid, "condição": cond, "n": len(d),
            "ttr": round(len(set(toks)) / max(len(toks), 1), 3),
            "palavras/enunciado": round(
                d["stem"].str.split().str.len().mean(), 1),
            "%fácil": round((d.difficulty == "facil").mean() * 100),
            "%média": round((d.difficulty == "media").mean() * 100),
            "%difícil": round((d.difficulty == "dificil").mean() * 100),
        }
    rows = []
    for tid in TOPICS:
        for cond, d in [("instruction-only", df_q),
                        ("context-grounded", df_ctx)]:
            r = stats_row(d, cond, tid)
            if r:
                rows.append(r)
    print(pd.DataFrame(rows).to_string(index=False))
else:
    print("dataset_mcq_petroles.jsonl não encontrado — rode antes o "
          "geracao_mcq_petroles.py para habilitar a comparação.")
