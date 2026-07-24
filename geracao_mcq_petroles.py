# %% [markdown]
# # Geração de Dataset MCQ a partir do Corpus Petrolês
#
# Pipeline para geração de questões de múltipla escolha (MCQ) em português,
# no domínio de óleo e gás offshore (FPSO, SGSO), usando o corpus Petrolês
# como base documental e o prompt `PORTUGUESE_V13` (`prompt_mcq_generation.py`).
#
# ## Metodologia
#
# O pipeline segue 6 etapas, com rastreabilidade completa de cada questão até
# o trecho do corpus que a originou:
#
# 1. **Chunking** — o corpus (1 sentença/linha, sem fronteiras de documento) é
#    segmentado em janelas deslizantes de sentenças consecutivas com sobreposição,
#    preservando coerência local. Filtros de qualidade descartam janelas curtas
#    ou com excesso de tokens mascarados (`<NUMBER>`).
# 2. **Recuperação lexical (estágio 1)** — léxicos ponderados por assunto
#    (termos *fortes*, *médios* e *de apoio*, calibrados por frequência no corpus)
#    pontuam cada janela em uma única passada streaming. Um *gate* exige pelo menos
#    1 termo forte (ou 2 médios) para evitar falsos positivos de termos genéricos.
#    Os top-K candidatos por assunto seguem adiante.
# 3. **Re-ranking semântico (estágio 2)** — embeddings multilíngues
#    (sentence-transformers; fallback TF-IDF) medem similaridade entre cada
#    candidato e uma descrição textual do assunto. Score final = combinação
#    z-normalizada (lexical + semântico).
# 4. **Seleção com diversidade (MMR)** — Maximal Marginal Relevance seleciona
#    trechos relevantes *e* diversos entre si, evitando questões redundantes
#    geradas a partir de trechos quase idênticos.
# 5. **Geração via LLM** — cada trecho selecionado alimenta o prompt v13
#    (backend plugável: Anthropic / OpenAI / Ollama / mock). Saída JSON é
#    validada estruturalmente, com retry.
# 6. **Controle de qualidade** — deduplicação de enunciados, rebalanceamento
#    das posições da resposta correta (A–D), estatísticas de dificuldade e de
#    balanceamento de comprimento das alternativas.
#
# **Saídas:** `dataset_mcq_petroles.jsonl` / `.csv` + `chunks_selecionados.jsonl`
# (rastreabilidade).

# %%
# ============================== CONFIGURAÇÃO ==============================
import os, re, json, math, heapq, random, hashlib, unicodedata, datetime
from pathlib import Path

import numpy as np
import pandas as pd

SEED = 42
random.seed(SEED); np.random.seed(SEED)

BASE_DIR = Path(".")  # pasta do corpus (onde está este notebook)
CORPUS_FILES = [
    BASE_DIR / "corpusPublico(sem IBICT)-SemProcessamento.txt",
    BASE_DIR / "corpusPublicoIBICT-SemProcessamento.txt",
]
OUT_DIR = BASE_DIR / "mcq_output"
OUT_DIR.mkdir(exist_ok=True)

# Chunking
WINDOW = 12          # sentenças por janela
STRIDE = 6           # passo (50% de sobreposição)
MIN_WORDS, MAX_WORDS = 80, 450
MAX_NUMBER_FRAC = 0.15  # fração máxima de tokens '<NUMBER>'

# Recuperação
TOP_K_LEXICAL = 1500     # candidatos por assunto após estágio lexical
N_SELECT = 25            # trechos por assunto após MMR (com folga p/ falhas)
MMR_LAMBDA = 0.7
W_LEX, W_SEM = 0.5, 0.5  # pesos do score combinado

# Geração
N_QUESTOES_POR_ASSUNTO = 30
Q_PER_CHUNK = 2          # questões geradas por trecho
N_ALTERNATIVES = 4
MAX_RETRIES = 2

LLM_BACKEND = "mock"     # "anthropic" | "openai" | "ollama" | "transformers" | "mock"
LLM_MODEL = {
    "anthropic": "claude-sonnet-4-5",
    "openai": "gpt-4o",
    "ollama": "qwen3.6:27b",
    "transformers": "Qwen/Qwen3.6-27B",  # ou "Qwen/Qwen3.6-35B-A3B" (MoE, + rápido)
    "mock": "mock",
}[LLM_BACKEND]

from prompt_mcq_generation import PORTUGUESE_V13
PROMPT = PORTUGUESE_V13
print(f"Prompt: {PROMPT.version} ({PROMPT.language}) | Backend: {LLM_BACKEND} ({LLM_MODEL})")

# %% [markdown]
# ## Definição dos assuntos
#
# Cada assunto tem: léxico ponderado (calibrado por varredura de frequência no
# corpus real), termos de contexto de domínio (bônus) e uma *query* descritiva
# usada no re-ranking semântico. Termos em forma normalizada (minúsculas, sem
# acentos).

# %%
TOPICS = {
    "producao_processo_medicao_alivio": {
        "nome": "Produção e Processo (Medição Fiscal e Sistema de Alívio)",
        "strong": [  # peso 3 — específicos do assunto
            "medicao fiscal", "transferencia de custodia", "placa de orificio",
            "regulamento tecnico de medicao", "incerteza de medicao",
            "sistema de medicao", "medicao de vazao", "computador de vazao",
            "sistema de alivio", "alivio de pressao", "valvula de seguranca",
            "psv", "flare", "tocha", "blowdown", "despressurizacao",
            "queima de gas", "medidor ultrassonico",
        ],
        "medium": [  # peso 2
            "calibracao", "vazao", "medicao de gas", "medicao de petroleo",
            "queimador", "vaso separador", "pressao de abertura", "gas de queima",
            "seguranca de processo", "sobrepressao",
        ],
        "support": [  # peso 1
            "medicao", "pressao", "valvula", "separador", "gas natural",
        ],
        "query": (
            "Medição fiscal de petróleo e gás natural, transferência de custódia, "
            "incerteza de medição, calibração de medidores de vazão, placa de "
            "orifício, regulamento técnico de medição da ANP; sistemas de alívio "
            "e queima em plataformas: flare, tocha, válvulas de segurança PSV, "
            "despressurização de emergência (blowdown), proteção contra "
            "sobrepressão no processamento primário de petróleo em FPSOs."
        ),
    },
    "gestao_desempenho": {
        "nome": "Gestão do Desempenho",
        "strong": [
            "gestao do desempenho", "gestao de desempenho",
            "indicador de desempenho", "indicadores de desempenho",
            "avaliacao de desempenho", "desempenho operacional",
            "monitoramento do desempenho", "monitoramento de desempenho",
            "metas de desempenho", "kpi",
        ],
        "medium": [
            "melhoria continua", "analise critica", "sgso",
            "seguranca operacional", "auditoria interna", "plano de acao",
            "benchmarking", "eficiencia operacional", "sistema de gestao",
        ],
        "support": [
            "desempenho", "indicador", "meta", "auditoria", "gestao",
        ],
        "query": (
            "Gestão do desempenho em unidades de produção offshore: definição e "
            "monitoramento de indicadores de desempenho (KPIs) operacionais e de "
            "segurança, avaliação de desempenho, metas, análise crítica pela "
            "liderança, melhoria contínua, auditorias e práticas de gestão do "
            "Sistema de Gerenciamento de Segurança Operacional (SGSO) em FPSOs."
        ),
    },
    "manutencao_inspecao_integridade": {
        "nome": "Manutenção, Inspeção e Integridade de Ativos",
        "strong": [
            "integridade mecanica", "gestao de integridade",
            "integridade de ativos", "manutencao preventiva",
            "manutencao preditiva", "manutencao corretiva",
            "ensaios nao destrutivos", "ensaio nao destrutivo",
            "plano de manutencao", "inspecao baseada em risco",
            "manutencao centrada em confiabilidade",
        ],
        "medium": [
            "integridade estrutural", "corrosao", "inspecao", "confiabilidade",
            "vida util", "analise de falha", "taxa de falha", "degradacao",
            "protecao catodica", "monitoramento da corrosao",
        ],
        "support": [
            "manutencao", "falha", "desgaste", "fadiga", "trinca", "reparo",
        ],
        "query": (
            "Manutenção, inspeção e gestão da integridade de ativos em unidades "
            "offshore: estratégias de manutenção preventiva, preditiva e "
            "corretiva, manutenção centrada em confiabilidade, inspeção baseada "
            "em risco, ensaios não destrutivos, mecanismos de degradação como "
            "corrosão e fadiga, integridade mecânica e estrutural de cascos, "
            "tanques, tubulações e equipamentos de FPSOs."
        ),
    },
}

# Termos de contexto de domínio (bônus de 0.5 cada, máx. 2.0)
DOMAIN_TERMS = [
    "fpso", "offshore", "plataforma", "unidade de producao",
    "unidade estacionaria", "anp", "poco", "submarino", "pre-sal",
    "petroleo", "campo de producao",
]

# %% [markdown]
# ## Etapa 1–2 — Chunking + varredura lexical (streaming, uma passada)

# %%
_ACCENT_TABLE = None
def normalize(text: str) -> str:
    """Minúsculas + remoção de acentos (rápido, via tabela de tradução)."""
    global _ACCENT_TABLE
    if _ACCENT_TABLE is None:
        _ACCENT_TABLE = {}
        for cp in range(0x2500):
            ch = chr(cp)
            dec = unicodedata.normalize("NFD", ch.lower())
            _ACCENT_TABLE[cp] = "".join(c for c in dec
                                        if unicodedata.category(c) != "Mn")
    return text.translate(_ACCENT_TABLE)


def compile_topic_patterns(topics):
    """Compila um regex por (assunto, nível) com word boundaries."""
    pats = {}
    for tid, t in topics.items():
        for level in ("strong", "medium", "support"):
            terms = sorted(t[level], key=len, reverse=True)
            pats[(tid, level)] = re.compile(
                r"\b(" + "|".join(re.escape(x) for x in terms) + r")\b")
    return pats

TOPIC_PATTERNS = compile_topic_patterns(TOPICS)
DOMAIN_PATTERN = re.compile(
    r"\b(" + "|".join(re.escape(x) for x in sorted(DOMAIN_TERMS, key=len,
                                                   reverse=True)) + r")\b")
LEVEL_WEIGHTS = {"strong": 3.0, "medium": 2.0, "support": 1.0}
CAP_PER_TERM = 3  # evita que 1 termo repetido domine o score


def chunk_quality_ok(text: str) -> bool:
    words = text.split()
    if not (MIN_WORDS <= len(words) <= MAX_WORDS):
        return False
    n_masked = text.count("<NUMBER>")
    return (n_masked / max(len(words), 1)) <= MAX_NUMBER_FRAC


def score_chunk(norm_text: str, tid: str):
    """Retorna score lexical (ou None se não passar no gate)."""
    strong_hits = TOPIC_PATTERNS[(tid, "strong")].findall(norm_text)
    medium_hits = TOPIC_PATTERNS[(tid, "medium")].findall(norm_text)
    if not strong_hits and len(set(medium_hits)) < 2:
        return None  # gate: exige especificidade mínima
    score = 0.0
    for level, hits in (("strong", strong_hits), ("medium", medium_hits),
                        ("support", TOPIC_PATTERNS[(tid, "support")]
                         .findall(norm_text))):
        counts = {}
        for h in hits:
            counts[h] = counts.get(h, 0) + 1
        score += LEVEL_WEIGHTS[level] * sum(min(c, CAP_PER_TERM)
                                            for c in counts.values())
    score += min(len(set(DOMAIN_PATTERN.findall(norm_text))) * 0.5, 2.0)
    return score


def scan_corpus(files, topics, cache_path):
    """Passada única: gera janelas e mantém top-K por assunto (heap)."""
    if cache_path.exists():
        print(f"Cache encontrado: {cache_path}")
        cands = [json.loads(l) for l in open(cache_path, encoding="utf-8")]
        return cands
    heaps = {tid: [] for tid in topics}  # (score, uid, chunk_dict)
    uid = 0
    for fpath in files:
        fname = fpath.name
        buf, buf_start = [], 1
        with open(fpath, encoding="utf-8", errors="replace") as f:
            for lineno, line in enumerate(f, 1):
                buf.append(line.strip())
                if len(buf) == WINDOW:
                    text = " ".join(buf)
                    if chunk_quality_ok(text):
                        ntext = normalize(text)
                        for tid in topics:
                            s = score_chunk(ntext, tid)
                            if s is not None:
                                uid += 1
                                item = (s, uid, {
                                    "chunk_id": f"{fname}:{buf_start}-{lineno}",
                                    "file": fname,
                                    "line_start": buf_start,
                                    "line_end": lineno,
                                    "topic": tid,
                                    "lex_score": round(s, 2),
                                    "text": text,
                                })
                                h = heaps[tid]
                                if len(h) < TOP_K_LEXICAL:
                                    heapq.heappush(h, item)
                                elif s > h[0][0]:
                                    heapq.heapreplace(h, item)
                    buf = buf[STRIDE:]
                    buf_start += STRIDE
                if lineno % 1_000_000 == 0:
                    print(f"  {fname}: {lineno:,} linhas...")
        print(f"Concluído: {fname}")
    cands = [it[2] for tid in topics for it in
             sorted(heaps[tid], key=lambda x: -x[0])]
    with open(cache_path, "w", encoding="utf-8") as f:
        for c in cands:
            f.write(json.dumps(c, ensure_ascii=False) + "\n")
    return cands


candidates = scan_corpus(CORPUS_FILES, TOPICS,
                         OUT_DIR / "candidatos_lexicais.jsonl")
df_cand = pd.DataFrame(candidates)
print(df_cand.groupby("topic").agg(n=("chunk_id", "count"),
                                   score_max=("lex_score", "max"),
                                   score_min=("lex_score", "min")))

# %% [markdown]
# ## Etapa 3 — Re-ranking semântico
#
# Usa `sentence-transformers` (modelo multilíngue) se disponível; caso
# contrário, TF-IDF (n-gramas de palavras) como fallback determinístico.

# %%
def build_embedder():
    try:
        from sentence_transformers import SentenceTransformer
        model = SentenceTransformer("paraphrase-multilingual-MiniLM-L12-v2")
        print("Embedder: sentence-transformers (multilíngue)")
        def embed(texts):
            return np.asarray(model.encode(texts, batch_size=64,
                                           normalize_embeddings=True,
                                           show_progress_bar=False))
        return embed, "sbert"
    except Exception as e:
        from sklearn.feature_extraction.text import TfidfVectorizer
        print(f"sentence-transformers indisponível ({type(e).__name__}); "
              f"usando fallback TF-IDF")
        return None, "tfidf"


def semantic_scores(df, topics):
    """Adiciona colunas sem_score e embedding (p/ MMR)."""
    embed, kind = build_embedder()
    df = df.copy()
    df["sem_score"] = 0.0
    embs = {}
    for tid, t in topics.items():
        mask = df["topic"] == tid
        texts = df.loc[mask, "text"].tolist()
        if not texts:
            continue
        if kind == "sbert":
            E = embed(texts)
            q = embed([t["query"]])[0]
        else:
            from sklearn.feature_extraction.text import TfidfVectorizer
            from sklearn.preprocessing import normalize as sk_normalize
            vec = TfidfVectorizer(ngram_range=(1, 2), max_features=50000,
                                  sublinear_tf=True)
            M = sk_normalize(vec.fit_transform(
                [normalize(x) for x in texts] + [normalize(t["query"])]))
            E, q = M[:-1], M[-1]  # esparsos
        sims = ((E @ q.T).toarray().ravel() if kind == "tfidf" else E @ q)
        df.loc[mask, "sem_score"] = sims
        embs[tid] = (df.index[mask].to_numpy(), E)
    return df, embs


def zscore(x):
    x = np.asarray(x, dtype=float)
    return (x - x.mean()) / (x.std() + 1e-9)


df_cand, topic_embs = semantic_scores(df_cand, TOPICS)
for tid in TOPICS:
    m = df_cand["topic"] == tid
    df_cand.loc[m, "combined"] = (W_LEX * zscore(df_cand.loc[m, "lex_score"])
                                  + W_SEM * zscore(df_cand.loc[m, "sem_score"]))
print(df_cand.groupby("topic")[["lex_score", "sem_score", "combined"]].mean())

# %% [markdown]
# ## Etapa 4 — Seleção final com diversidade (MMR)
#
# `MMR = λ·relevância − (1−λ)·max(similaridade com já selecionados)`.
# Também remove quase-duplicatas (similaridade > 0.92).

# %%
def row_sim(E, i, j):
    """Cosseno entre linhas i e j (suporta numpy denso e scipy esparso)."""
    if hasattr(E, "toarray"):  # esparso
        return float((E[i] @ E[j].T).toarray().ravel()[0])
    return float(E[i] @ E[j])


def mmr_select(idx_array, E, relevance, n_select, lam=MMR_LAMBDA,
               dup_threshold=0.92):
    order = np.argsort(-relevance)[:max(n_select * 12, 300)]  # pool p/ eficiência
    selected = []
    for _ in range(min(n_select, len(order))):
        best, best_val = None, -np.inf
        for j in order:
            if j in selected:
                continue
            sim_max = max((row_sim(E, j, s) for s in selected), default=0.0)
            if sim_max > dup_threshold:
                continue
            val = lam * relevance[j] - (1 - lam) * sim_max
            if val > best_val:
                best, best_val = j, val
        if best is None:
            break
        selected.append(best)
    return [idx_array[j] for j in selected]


selected_rows = []
for tid in TOPICS:
    idx_array, E = topic_embs[tid]
    rel = df_cand.loc[idx_array, "combined"].to_numpy()
    rel = (rel - rel.min()) / (rel.max() - rel.min() + 1e-9)
    chosen = mmr_select(idx_array, E, rel, N_SELECT)
    selected_rows.extend(chosen)
    print(f"{tid}: {len(chosen)} trechos selecionados")

df_sel = df_cand.loc[selected_rows].reset_index(drop=True)
with open(OUT_DIR / "chunks_selecionados.jsonl", "w", encoding="utf-8") as f:
    for _, r in df_sel.iterrows():
        f.write(json.dumps({k: r[k] for k in
                            ["chunk_id", "file", "line_start", "line_end",
                             "topic", "lex_score", "sem_score", "combined",
                             "text"]}, ensure_ascii=False, default=float) + "\n")

# Inspeção manual recomendada de uma amostra:
for tid in TOPICS:
    ex = df_sel[df_sel.topic == tid].iloc[0]
    print(f"\n=== {tid} | {ex.chunk_id} ===\n{ex.text[:400]}...")

# %% [markdown]
# ## Etapa 5 — Geração via LLM (backend plugável)

# %%
class LLMClient:
    def generate(self, system: str, user: str) -> str:
        raise NotImplementedError


class AnthropicClient(LLMClient):
    def __init__(self, model):
        import anthropic
        self.client = anthropic.Anthropic()  # ANTHROPIC_API_KEY no ambiente
        self.model = model
    def generate(self, system, user):
        r = self.client.messages.create(model=self.model, max_tokens=4096,
                                        system=system,
                                        messages=[{"role": "user",
                                                   "content": user}])
        return r.content[0].text


class OpenAIClient(LLMClient):
    def __init__(self, model):
        from openai import OpenAI
        self.client = OpenAI()  # OPENAI_API_KEY no ambiente
        self.model = model
    def generate(self, system, user):
        r = self.client.chat.completions.create(
            model=self.model,
            messages=[{"role": "system", "content": system},
                      {"role": "user", "content": user}])
        return r.choices[0].message.content


class OllamaClient(LLMClient):
    def __init__(self, model, host="http://localhost:11434"):
        self.model, self.host = model, host
    def generate(self, system, user):
        import urllib.request
        req = urllib.request.Request(
            f"{self.host}/api/chat", method="POST",
            headers={"Content-Type": "application/json"},
            data=json.dumps({"model": self.model, "stream": False,
                             "messages": [
                                 {"role": "system", "content": system},
                                 {"role": "user", "content": user}]}).encode())
        with urllib.request.urlopen(req, timeout=600) as resp:
            return json.loads(resp.read())["message"]["content"]


class TransformersClient(LLMClient):
    """Inferência local via Hugging Face Transformers (ex.: H100).

    Carrega o modelo uma única vez em bfloat16. Uso apenas texto (system +
    user); exemplos multimodais do model card (imagem) não se aplicam aqui.
    """
    def __init__(self, model_id, max_new_tokens=4096, temperature=0.7):
        import torch
        from transformers import AutoTokenizer
        self.max_new_tokens, self.temperature = max_new_tokens, temperature
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
    def generate(self, system, user):
        messages = [{"role": "system", "content": system},
                    {"role": "user", "content": user}]
        inputs = self.tok.apply_chat_template(
            messages, add_generation_prompt=True, tokenize=True,
            return_dict=True, return_tensors="pt").to(self.model.device)
        out = self.model.generate(**inputs,
                                  max_new_tokens=self.max_new_tokens,
                                  do_sample=True,
                                  temperature=self.temperature)
        n_in = inputs["input_ids"].shape[-1]
        text = self.tok.decode(out[0][n_in:], skip_special_tokens=True)
        # remove eventual traço de raciocínio (<think>...</think>)
        return re.sub(r"<think>.*?</think>", "", text, flags=re.DOTALL)


class MockClient(LLMClient):
    """Dry-run: valida o pipeline de ponta a ponta sem custo de API."""
    def generate(self, system, user):
        # usa palavras reais do trecho p/ enunciados distintos entre si
        words = [w for w in user.split() if len(w) > 5][:40]
        qs = []
        for i in range(Q_PER_CHUNK):
            sample = " ".join(random.sample(words, min(8, len(words))))
            qs.append({
                "stem": f"[MOCK Q{i+1}] Considere o cenário envolvendo "
                        f"{sample}: qual a conduta adequada?",
                "alternatives": [f"Alternativa {c}" for c in "ABCD"],
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

# %%
JSON_RE = re.compile(r"\[.*\]", re.DOTALL)

def parse_questions(raw: str):
    m = JSON_RE.search(raw)
    if not m:
        raise ValueError("Nenhum JSON encontrado na resposta")
    data = json.loads(m.group(0))
    if not isinstance(data, list):
        raise ValueError("JSON não é uma lista")
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
        valid.append(q)
    return valid


def generate_for_topic(tid, df_sel, client, quota):
    rows = df_sel[df_sel.topic == tid]
    questions = []
    for _, chunk in rows.iterrows():
        if len(questions) >= quota:
            break
        user_prompt = PROMPT.question_template.format(
            n_questions=Q_PER_CHUNK, n_alternatives=N_ALTERNATIVES,
            content=chunk.text)
        for attempt in range(MAX_RETRIES + 1):
            try:
                raw = client.generate(PROMPT.system_message, user_prompt)
                qs = parse_questions(raw)
                if not qs:
                    raise ValueError("Nenhuma questão válida")
                for q in qs:
                    q.update({
                        "topic": tid,
                        "topic_name": TOPICS[tid]["nome"],
                        "source_chunk_id": chunk.chunk_id,
                        "source_file": chunk.file,
                        "prompt_version": PROMPT.version,
                        "model": f"{LLM_BACKEND}/{LLM_MODEL}",
                        "generated_at": datetime.datetime.now()
                                        .isoformat(timespec="seconds"),
                    })
                questions.extend(qs)
                break
            except Exception as e:
                if attempt == MAX_RETRIES:
                    print(f"  Falha em {chunk.chunk_id}: {e}")
    return questions[:quota + Q_PER_CHUNK - 1]


all_questions = []
for tid in TOPICS:
    print(f"Gerando: {TOPICS[tid]['nome']}")
    qs = generate_for_topic(tid, df_sel, client, N_QUESTOES_POR_ASSUNTO)
    print(f"  {len(qs)} questões geradas")
    all_questions.extend(qs)

# %% [markdown]
# ## Etapa 6 — Controle de qualidade
#
# 1. Deduplicação de enunciados (Jaccard de tokens ≥ 0.75);
# 2. Rebalanceamento das posições da resposta correta (ciclo A→B→C→D);
# 3. Estatísticas: dificuldade, posição da correta, balanceamento de comprimento.

# %%
def dedupe(questions, threshold=0.75):
    kept, seen = [], []
    for q in questions:
        toks = set(normalize(q["stem"]).split())
        if any(len(toks & s) / max(len(toks | s), 1) >= threshold
               for s in seen):
            continue
        seen.append(toks)
        kept.append(q)
    return kept


def rebalance_positions(questions):
    """Reposiciona a alternativa correta ciclando A→B→C→D por assunto."""
    by_topic = {}
    for q in questions:
        by_topic.setdefault(q["topic"], []).append(q)
    for qs in by_topic.values():
        for i, q in enumerate(qs):
            target = i % N_ALTERNATIVES
            alts = q["alternatives"][:]
            correct = alts.pop(q["correct_answer_index"])
            rest = alts[:]
            random.shuffle(rest)
            new_alts = rest[:target] + [correct] + rest[target:]
            q["alternatives"] = new_alts
            q["correct_answer_index"] = target
    return questions


n0 = len(all_questions)
all_questions = dedupe(all_questions)
print(f"Deduplicação: {n0} → {len(all_questions)}")
all_questions = rebalance_positions(all_questions)

df_q = pd.DataFrame(all_questions)
print("\nQuestões por assunto:")
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
print(f"\nRazão de comprimento correta/distratores: média={ratios.mean():.2f} "
      f"(ideal ≈ 1.0), desvio={ratios.std():.2f}")

# %% [markdown]
# ## Etapa 7 — Exportação

# %%
jsonl_path = OUT_DIR / "dataset_mcq_petroles.jsonl"
csv_path = OUT_DIR / "dataset_mcq_petroles.csv"
with open(jsonl_path, "w", encoding="utf-8") as f:
    for q in all_questions:
        f.write(json.dumps(q, ensure_ascii=False) + "\n")

flat = df_q.copy()
for i in range(N_ALTERNATIVES):
    flat[f"alternativa_{chr(65+i)}"] = flat["alternatives"].str[i]
flat["gabarito"] = flat["correct_answer_index"].map(
    lambda i: chr(65 + i))
flat.drop(columns=["alternatives"]).to_csv(csv_path, index=False,
                                           encoding="utf-8-sig")
print(f"Salvos:\n  {jsonl_path}\n  {csv_path}\n  "
      f"{OUT_DIR / 'chunks_selecionados.jsonl'}")

# %% [markdown]
# ## Limitações e validação humana recomendada
#
# - **Fronteiras de documento**: o corpus não delimita documentos; janelas
#   deslizantes podem raramente misturar fins/inícios de documentos distintos.
#   A inspeção da Etapa 4 mitiga isso.
# - **Números mascarados** (`<NUMBER>`): trechos com muitos valores numéricos
#   são filtrados, mas questões quantitativas não devem depender de valores do
#   texto.
# - **Validação humana**: recomenda-se que 1–2 especialistas do domínio revisem
#   100% das questões (ou uma amostra estratificada por assunto × dificuldade),
#   avaliando: correção técnica do gabarito, plausibilidade dos distratores,
#   ausência de ambiguidade e aderência ao assunto. Registrar taxa de aprovação
#   por assunto como métrica de qualidade do pipeline.
# - **Reprodutibilidade**: SEED fixa; versão do prompt, modelo e trecho-fonte
#   registrados em cada questão.
