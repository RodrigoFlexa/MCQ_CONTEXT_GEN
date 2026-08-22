# %% [markdown]
# # Geração de Dataset MCQ a partir do Corpus Petrolês
#
# Pipeline para geração de questões de múltipla escolha (MCQ) em português,
# no domínio de óleo e gás offshore (FPSO, SGSO), usando o corpus Petrolês
# como base documental e o prompt `PORTUGUESE_V13` (`prompt_mcq_generation.py`).
#
# ## Metodologia
#
# **Princípio de desenho**: nenhuma engenharia manual de conhecimento. O único
# insumo de domínio é a **descrição textual de cada assunto** — que integra a
# própria definição da tarefa e é usada *verbatim* nas duas condições
# experimentais, com dois papéis aqui: query de recuperação **e** enquadramento
# do assunto no prompt. Assim as duas condições recebem a mesma descrição e a
# única variável experimental é a presença do trecho recuperado:
#
# | Condição | Bloco `{content}` |
# |---|---|
# | *Instruction-only* | `Assunto:` + descrição |
# | *Context-grounded* | `Assunto:` + descrição, `Trecho de referência:` + trecho |
#
# Todos os componentes de recuperação são métodos padrão da literatura de RI,
# com parâmetros convencionais:
#
# 1. **Chunking** — janelas deslizantes de 12 sentenças com passo 6 (50% de
#    sobreposição), preservando coerência local num corpus sem fronteiras de
#    documento. Filtros de qualidade objetivos: 80–450 palavras e ≤15% de
#    tokens mascarados (`<NUMBER>`).
# 2. **Recuperação esparsa — Okapi BM25** (Robertson & Zaragoza, 2009), com a
#    descrição do assunto como query e parâmetros convencionais k1=1.5, b=0.75.
#    Implementação exata em duas passadas streaming (estatísticas globais →
#    scoring), retendo os top-K candidatos por assunto.
# 3. **Re-ranking denso** — embeddings multilíngues (sentence-transformers;
#    fallback determinístico TF-IDF) medem similaridade de cosseno entre cada
#    candidato e a descrição do assunto.
# 4. **Fusão por Reciprocal Rank Fusion** (Cormack et al., 2009) — combina os
#    rankings esparso e denso usando apenas posições de rank
#    (`RRF(d) = Σ 1/(k + rank_i(d))`, k=60 convencional), eliminando pesos de
#    combinação arbitrários.
# 5. **Seleção com diversidade — MMR** (Carbonell & Goldstein, 1998) — evita
#    trechos redundantes; λ=0.7 (análise de sensibilidade recomendada).
# 6. **Geração via LLM** — cada trecho alimenta o prompt v13 (backend plugável:
#    Anthropic / OpenAI / Ollama / Transformers / mock). Saída JSON validada
#    estruturalmente, com retry.
# 7. **Controle de qualidade** — deduplicação de enunciados, rebalanceamento
#    das posições do gabarito (A–D), estatísticas de dificuldade e de
#    balanceamento de comprimento.
#
# **Saídas:** `dataset_mcq_petroles.jsonl` / `.csv` + `chunks_selecionados.jsonl`
# (rastreabilidade completa: cada questão aponta o trecho-fonte no corpus).

# %%
# ============================== CONFIGURAÇÃO ==============================
import os, re, sys, json, math, heapq, random, hashlib, unicodedata, datetime
from pathlib import Path

import numpy as np
import pandas as pd

# GPU configurável pelo terminal:
#   python geracao_mcq_petroles.py --gpu 3
#   (ou: CUDA_VISIBLE_DEVICES=3 python geracao_mcq_petroles.py)
# Sem --gpu e sem variável exportada, usa todas as GPUs visíveis.
# if "--gpu" in sys.argv:
#     os.environ["CUDA_VISIBLE_DEVICES"] = sys.argv[sys.argv.index("--gpu") + 1]
os.environ.setdefault("CUDA_VISIBLE_DEVICES", "3")
print(f"CUDA_VISIBLE_DEVICES = {os.environ.get('CUDA_VISIBLE_DEVICES', '(todas)')}")

SEED = 42
random.seed(SEED); np.random.seed(SEED)

BASE_DIR = Path(".")  # pasta do notebook
CORPUS_DIR = BASE_DIR / "corpus"
CORPUS_FILES = [
    CORPUS_DIR / "corpusPublico(sem IBICT)-SemProcessamento.txt",
    CORPUS_DIR / "corpusPublicoIBICT-SemProcessamento.txt",
]
OUT_DIR = BASE_DIR / "mcq_output"
OUT_DIR.mkdir(exist_ok=True)

# Chunking
WINDOW = 12          # sentenças por janela
STRIDE = 6           # passo (50% de sobreposição)
MIN_WORDS, MAX_WORDS = 80, 450
MAX_NUMBER_FRAC = 0.15  # fração máxima de tokens '<NUMBER>'

# Recuperação (parâmetros convencionais da literatura)
BM25_K1, BM25_B = 1.5, 0.75   # Robertson & Zaragoza (2009)
RRF_K = 60                    # Cormack et al. (2009)
TOP_K_BM25 = 2000             # candidatos por assunto após estágio esparso
N_SELECT = 25                 # trechos por assunto após MMR
MMR_LAMBDA = 0.7              # Carbonell & Goldstein (1998)

# Geração
N_QUESTOES_POR_ASSUNTO = 10
Q_PER_CHUNK = 2          # questões geradas por trecho
N_ALTERNATIVES = 4
MAX_RETRIES = 3

# Orçamento de saída generoso: modelos com raciocínio explícito (<think>)
# gastam a maior parte dos tokens antes de emitir o JSON. Com 4096 o corte
# ocorria no meio do raciocínio e a resposta saía sem nenhum array JSON.
MAX_NEW_TOKENS = 16384
TEMPERATURE = 0.7            # 1ª tentativa
RETRY_TEMPERATURE = 0.3      # retentativas: mais determinístico p/ formato
ENABLE_THINKING = False      # desliga <think> quando o chat template suporta

LLM_BACKEND = "transformers"     # "anthropic" | "openai" | "ollama" | "transformers" | "mock"
LLM_MODEL = {
    "anthropic": "claude-sonnet-4-5",
    "openai": "gpt-4o",
    "ollama": "qwen3.6:27b",
    "transformers": "Qwen/Qwen3.6-27B",  # ou "Qwen/Qwen3.6-35B-A3B" (MoE, + rápido)
    "mock": "mock",
}[LLM_BACKEND]

from prompt_mcq_generation import PORTUGUESE_V15, build_content
PROMPT = PORTUGUESE_V15
CONTENT_FORMAT = "assunto+trecho"  # registrado em cada questão
print(f"Prompt: {PROMPT.version} ({PROMPT.language}) | Backend: {LLM_BACKEND} ({LLM_MODEL})")

# %% [markdown]
# ## Definição dos assuntos
#
# Cada assunto é definido **apenas** por sua descrição em linguagem natural.
# Esta descrição é o único insumo de domínio do pipeline e deve ser idêntica
# ao `content` usado na condição *instruction-only* do estudo comparativo.

# %%
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

# %% [markdown]
# ## Etapa 1–2 — Chunking + Okapi BM25 (duas passadas streaming)
#
# Pré-processamento padrão: minúsculas, remoção de acentos, tokens alfabéticos
# com ≥3 caracteres, remoção de stopwords do português (lista padrão). A query
# de cada assunto é o conjunto de tokens de sua descrição — sem qualquer
# seleção ou ponderação manual de termos: a discriminatividade de cada termo é
# dada pelo IDF, estimado do próprio corpus.

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


# Stopwords padrão do português (subconjunto da lista NLTK)
STOPWORDS_PT = set("""
a o e de da do das dos em no na nos nas um uma uns umas para por com sem sob
sobre entre ate apos que se nao mais menos muito pouco como quando onde qual
quais cujo cuja ser estar ter haver fazer pode podem deve devem foi sao era
seu sua seus suas este esta estes estas esse essa esses essas aquele aquela
isto isso aquilo tambem ja ainda so apenas ou mas porem contudo entao assim
pois porque portanto alem cada todo toda todos todas outro outra outros outras
mesmo mesma ao aos das dos pelo pela pelos pelas nos nas num numa dele dela
deles delas lhe lhes eles elas nós vos os as
""".split())

TOKEN_RE = re.compile(r"[a-z]{3,}")

def tokenize(text: str):
    return [t for t in TOKEN_RE.findall(normalize(text))
            if t not in STOPWORDS_PT]


TOPIC_QUERY_TOKENS = {tid: sorted(set(tokenize(t["descricao"])))
                      for tid, t in TOPICS.items()}
for tid, toks in TOPIC_QUERY_TOKENS.items():
    print(f"{tid}: {len(toks)} termos de query")


def chunk_quality_ok(text: str) -> bool:
    words = text.split()
    if not (MIN_WORDS <= len(words) <= MAX_WORDS):
        return False
    n_masked = text.count("<NUMBER>")
    return (n_masked / max(len(words), 1)) <= MAX_NUMBER_FRAC


def iter_chunks(files):
    """Gera janelas deslizantes (determinístico entre passadas)."""
    for fpath in files:
        fname = fpath.name
        buf, buf_start = [], 1
        with open(fpath, encoding="utf-8", errors="replace") as f:
            lineno = 0
            for line in f:
                lineno += 1
                buf.append(line.strip())
                if len(buf) == WINDOW:
                    yield fname, buf_start, lineno, " ".join(buf)
                    buf = buf[STRIDE:]
                    buf_start += STRIDE


def bm25_pass1(files, query_tokens_by_topic, cache_path):
    """Passada 1: N, comprimento médio e DF dos termos de query."""
    if cache_path.exists():
        return json.loads(cache_path.read_text(encoding="utf-8"))
    all_query_terms = set().union(*query_tokens_by_topic.values())
    N, sum_len = 0, 0
    df = {t: 0 for t in all_query_terms}
    for fname, ls, le, text in iter_chunks(files):
        if not chunk_quality_ok(text):
            continue
        toks = set(tokenize(text))
        N += 1
        sum_len += len(text.split())
        for t in all_query_terms & toks:
            df[t] += 1
    stats = {"N": N, "avgdl": sum_len / max(N, 1), "df": df}
    cache_path.write_text(json.dumps(stats), encoding="utf-8")
    return stats


def bm25_pass2(files, query_tokens_by_topic, stats, cache_path):
    """Passada 2: score BM25 de cada janela; top-K por assunto via heap."""
    if cache_path.exists():
        return [json.loads(l) for l in open(cache_path, encoding="utf-8")]
    N, avgdl, df = stats["N"], stats["avgdl"], stats["df"]
    idf = {t: math.log((N - d + 0.5) / (d + 0.5) + 1.0)
           for t, d in df.items()}
    heaps = {tid: [] for tid in query_tokens_by_topic}
    uid = 0
    for fname, ls, le, text in iter_chunks(files):
        if not chunk_quality_ok(text):
            continue
        toks = tokenize(text)
        dl = len(text.split())
        tf = {}
        for t in toks:
            tf[t] = tf.get(t, 0) + 1
        norm_len = BM25_K1 * (1 - BM25_B + BM25_B * dl / avgdl)
        for tid, qterms in query_tokens_by_topic.items():
            s = 0.0
            for t in qterms:
                f = tf.get(t)
                if f:
                    s += idf[t] * f * (BM25_K1 + 1) / (f + norm_len)
            if s <= 0:
                continue
            uid += 1
            item = (s, uid, {
                "chunk_id": f"{fname}:{ls}-{le}",
                "file": fname, "line_start": ls, "line_end": le,
                "topic": tid, "bm25_score": round(s, 3), "text": text})
            h = heaps[tid]
            if len(h) < TOP_K_BM25:
                heapq.heappush(h, item)
            elif s > h[0][0]:
                heapq.heapreplace(h, item)
    cands = [it[2] for tid in query_tokens_by_topic
             for it in sorted(heaps[tid], key=lambda x: -x[0])]
    with open(cache_path, "w", encoding="utf-8") as f:
        for c in cands:
            f.write(json.dumps(c, ensure_ascii=False) + "\n")
    return cands


# Cache automaticamente invalidado se assuntos/parâmetros mudarem
CFG_HASH = hashlib.md5((json.dumps(
    {t: TOPICS[t]["descricao"] for t in TOPICS}, sort_keys=True,
    ensure_ascii=False) +
    f"|{WINDOW}|{STRIDE}|{MIN_WORDS}|{MAX_WORDS}|{MAX_NUMBER_FRAC}|"
    f"{TOP_K_BM25}").encode()).hexdigest()[:8]
print(f"Hash da configuração de recuperação: {CFG_HASH}")

stats = bm25_pass1(CORPUS_FILES, TOPIC_QUERY_TOKENS,
                   OUT_DIR / f"bm25_stats_{CFG_HASH}.json")
print(f"Chunks válidos: {stats['N']:,} | comprimento médio: "
      f"{stats['avgdl']:.0f} palavras")
candidates = bm25_pass2(CORPUS_FILES, TOPIC_QUERY_TOKENS, stats,
                        OUT_DIR / f"candidatos_bm25_{CFG_HASH}.jsonl")
df_cand = pd.DataFrame(candidates)
print(df_cand.groupby("topic").agg(n=("chunk_id", "count"),
                                   bm25_max=("bm25_score", "max"),
                                   bm25_min=("bm25_score", "min")))

# %% [markdown]
# ## Etapa 3 — Re-ranking denso
#
# `sentence-transformers` (modelo multilíngue) se disponível; caso contrário,
# TF-IDF como fallback determinístico. A query é a própria descrição do
# assunto — a mesma da etapa BM25.

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
        print(f"sentence-transformers indisponível ({type(e).__name__}); "
              f"usando fallback TF-IDF")
        return None, "tfidf"


def semantic_scores(df, topics):
    """Adiciona coluna sem_score e retorna embeddings por assunto (p/ MMR)."""
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
            q = embed([t["descricao"]])[0]
        else:
            from sklearn.feature_extraction.text import TfidfVectorizer
            from sklearn.preprocessing import normalize as sk_normalize
            vec = TfidfVectorizer(ngram_range=(1, 2), max_features=50000,
                                  sublinear_tf=True)
            M = sk_normalize(vec.fit_transform(
                [normalize(x) for x in texts] + [normalize(t["descricao"])]))
            E, q = M[:-1], M[-1]  # esparsos
        sims = ((E @ q.T).toarray().ravel() if kind == "tfidf" else E @ q)
        df.loc[mask, "sem_score"] = sims
        embs[tid] = (df.index[mask].to_numpy(), E)
    return df, embs


df_cand, topic_embs = semantic_scores(df_cand, TOPICS)

# %% [markdown]
# ## Etapa 4 — Fusão RRF + seleção com diversidade (MMR)
#
# RRF combina os dois rankings usando apenas posições:
# `RRF(d) = Σ_i 1/(k + rank_i(d))`, k=60. Nenhum peso de combinação manual.

# %%
def rrf_fusion(df, k=RRF_K):
    df = df.copy()
    df["rrf"] = 0.0
    for tid in df["topic"].unique():
        m = df["topic"] == tid
        r_bm25 = (-df.loc[m, "bm25_score"]).rank(method="first")
        r_sem = (-df.loc[m, "sem_score"]).rank(method="first")
        df.loc[m, "rrf"] = 1.0 / (k + r_bm25) + 1.0 / (k + r_sem)
    return df


def mmr_select(idx_array, E, relevance, n_select, lam=MMR_LAMBDA,
               dup_threshold=0.92):
    """MMR sobre um pool dos mais relevantes, com matriz de similaridade
    pré-computada (eficiente p/ embeddings densos e esparsos)."""
    order = np.argsort(-relevance)[:max(n_select * 12, 300)]  # pool
    Ep = E[order]
    if hasattr(Ep, "toarray"):  # esparso -> denso só no pool
        Ep = Ep.toarray().astype(np.float32)
    S = Ep @ Ep.T  # similaridades cosseno do pool (linhas normalizadas)
    rel = relevance[order]
    selected = []
    for _ in range(min(n_select, len(order))):
        best, best_val = None, -np.inf
        for j in range(len(order)):
            if j in selected:
                continue
            sim_max = float(S[j, selected].max()) if selected else 0.0
            if sim_max > dup_threshold:
                continue
            val = lam * rel[j] - (1 - lam) * sim_max
            if val > best_val:
                best, best_val = j, val
        if best is None:
            break
        selected.append(best)
    return [idx_array[order[j]] for j in selected]


df_cand = rrf_fusion(df_cand)

selected_rows = []
for tid in TOPICS:
    idx_array, E = topic_embs[tid]
    pos = {ix: p for p, ix in enumerate(idx_array)}
    rel = df_cand.loc[idx_array, "rrf"].to_numpy()
    rel = (rel - rel.min()) / (rel.max() - rel.min() + 1e-9)
    chosen = mmr_select(idx_array, E, rel, N_SELECT)
    selected_rows.extend(chosen)
    print(f"{tid}: {len(chosen)} trechos selecionados")

df_sel = df_cand.loc[selected_rows].reset_index(drop=True)
with open(OUT_DIR / "chunks_selecionados.jsonl", "w", encoding="utf-8") as f:
    for _, r in df_sel.iterrows():
        f.write(json.dumps({k: r[k] for k in
                            ["chunk_id", "file", "line_start", "line_end",
                             "topic", "bm25_score", "sem_score", "rrf",
                             "text"]}, ensure_ascii=False, default=float) + "\n")

# Inspeção manual recomendada de uma amostra:
for tid in TOPICS:
    ex = df_sel[df_sel.topic == tid].iloc[0]
    print(f"\n=== {tid} | {ex.chunk_id} ===\n{ex.text[:400]}...")

# %% [markdown]
# ## Etapa 5 — Geração via LLM (backend plugável)

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
    """Inferência local via Hugging Face Transformers (ex.: H100).

    Carrega o modelo uma única vez em bfloat16. Uso apenas texto (system +
    user); exemplos multimodais do model card (imagem) não se aplicam aqui.
    """
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
        n_out = out.shape[-1] - n_in
        if n_out >= self.max_new_tokens:
            self.truncated += 1
        text = self.tok.decode(out[0][n_in:], skip_special_tokens=True)
        return strip_reasoning(text)


class MockClient(LLMClient):
    """Dry-run: valida o pipeline de ponta a ponta sem custo de API."""
    def generate(self, system, user, temperature=None):
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
FENCE_RE = re.compile(r"```(?:json)?\s*(.*?)```", re.DOTALL)
TRAILING_COMMA_RE = re.compile(r",\s*([\]}])")

def extract_json_array(raw: str):
    """Extrai o primeiro array JSON válido da resposta do LLM.

    Estratégia robusta: (1) tenta blocos cercados ```json ... ```;
    (2) varre cada '[' e usa raw_decode, que para exatamente no fim do
    JSON válido (imune a texto extra depois do array); (3) repete com
    reparo de vírgulas finais (erro comum de LLMs).
    """
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
            continue  # rejeita: o retry regenera o lote
        valid.append(q)
    return valid


# Salvamento incremental: cada questão aceita é gravada imediatamente aqui.
# Acompanhe em outro terminal com:  tail -f mcq_output/dataset_mcq_petroles_parcial.jsonl
PARTIAL_PATH = OUT_DIR / "dataset_mcq_petroles_parcial.jsonl"
if PARTIAL_PATH.exists() and PARTIAL_PATH.stat().st_size:
    # preserva o parcial da execução anterior antes de zerar
    ts = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    PARTIAL_PATH.rename(OUT_DIR / f"dataset_mcq_petroles_parcial_{ts}.jsonl")
PARTIAL_PATH.write_text("", encoding="utf-8")

def save_partial(q):
    with open(PARTIAL_PATH, "a", encoding="utf-8") as f:
        f.write(json.dumps(q, ensure_ascii=False) + "\n")


def generate_for_topic(tid, df_sel, client, quota):
    rows = df_sel[df_sel.topic == tid]
    questions = []
    for _, chunk in rows.iterrows():
        if len(questions) >= quota:
            break
        user_prompt = PROMPT.question_template.format(
            n_questions=Q_PER_CHUNK, n_alternatives=N_ALTERNATIVES,
            content=build_content(TOPICS[tid]["descricao"], chunk.text))
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
                    raise ValueError("Nenhuma questão válida")
                for q in qs:
                    q.update({
                        "topic": tid,
                        "topic_name": TOPICS[tid]["nome"],
                        "generation_mode": "context_grounded",
                        "content_format": CONTENT_FORMAT,
                        "source_chunk_id": chunk.chunk_id,
                        "source_file": chunk.file,
                        "prompt_version": PROMPT.version,
                        "model": f"{LLM_BACKEND}/{LLM_MODEL}",
                        "generated_at": datetime.datetime.now()
                                        .isoformat(timespec="seconds"),
                    })
                questions.extend(qs)
                for q in qs:
                    save_partial(q)
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

if getattr(client, "truncated", 0):
    print(f"\nRespostas cortadas no limite de {MAX_NEW_TOKENS} tokens: "
          f"{client.truncated} — se for alto, aumente MAX_NEW_TOKENS")

print(f"\nQuestões rejeitadas pelo detector de linguagem absolutista "
      f"(regeneradas): {CUE_REJECTED['n']}")
remaining = int(df_q.apply(lambda q: has_absolutist_cue(q), axis=1).sum())
print(f"Questões no dataset final ainda com padrão absolutista: {remaining} "
      f"(esperado: 0)")

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
# ## Limitações, decisões de projeto e validação humana
#
# - **Sem engenharia manual de conhecimento**: a recuperação usa apenas a
#   descrição do assunto como query; termos são ponderados por IDF estimado do
#   corpus (BM25), rankings são combinados por RRF (rank-based) e a diversidade
#   por MMR. Os únicos hiperparâmetros são convenções da literatura
#   (k1=1.5, b=0.75, k_RRF=60, λ=0.7) — recomenda-se análise de sensibilidade
#   para λ e para o tamanho da janela.
# - **Fronteiras de documento**: o corpus não delimita documentos; janelas
#   deslizantes podem raramente misturar fins/inícios de documentos distintos.
#   A inspeção da Etapa 4 mitiga isso.
# - **Números mascarados** (`<NUMBER>`): trechos com muitos valores numéricos
#   são filtrados; questões quantitativas não devem depender de valores do
#   texto.
# - **Validação humana**: recomenda-se que 1–2 especialistas revisem 100% das
#   questões (ou amostra estratificada por assunto × dificuldade), avaliando
#   correção do gabarito, plausibilidade dos distratores, ambiguidade e
#   aderência ao assunto, com acordo inter-anotador (ex.: Cohen's κ). Nota: a
#   revisão humana do *produto* é controle de qualidade padrão em construção de
#   datasets — distinta da dependência de especialista no *método*.
# - **Reprodutibilidade**: SEED fixa; versão do prompt, modelo, modo de geração
#   e trecho-fonte registrados em cada questão.
#
# **Referências**: Robertson & Zaragoza (2009), *The Probabilistic Relevance
# Framework: BM25 and Beyond*; Cormack, Clarke & Buettcher (2009), *Reciprocal
# Rank Fusion outperforms Condorcet and individual rank learning methods*;
# Carbonell & Goldstein (1998), *The use of MMR, diversity-based reranking for
# reordering documents and producing summaries*.
