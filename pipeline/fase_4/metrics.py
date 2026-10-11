"""Métricas de diversidade observacionais, independentes dos gates de qualidade."""
import math
import re
import unicodedata
from collections import Counter
import numpy as np

STOPWORDS = set("a o as os de do da dos das em no na nos nas um uma e ou por para com sem que se como qual quais quando onde ao aos sua seu isso este esta esse essa".split())


def tokens(text):
    norm = unicodedata.normalize("NFD", text.casefold())
    norm = "".join(x for x in norm if not unicodedata.combining(x))
    return re.findall(r"[a-z0-9]+", norm)


def canonical_question(text):
    # Sinais, unidades e números podem mudar o problema: não os apague para decidir duplicidade.
    return ' '.join(unicodedata.normalize('NFKC',text).casefold().split())


def entropy(values):
    values = [x for x in values if x]
    counts = Counter(values)
    if len(counts) < 2:
        return 0.0
    return round(-sum((n / len(values)) * math.log2(n / len(values)) for n in counts.values()) / math.log2(len(counts)), 6)


def ngrams(words, n):
    return {tuple(words[i:i+n]) for i in range(max(0, len(words) - n + 1))}


def chargrams(text):
    text = " ".join(tokens(text))
    return {text[i:i+3] for i in range(max(0, len(text) - 2))}


def jaccard(a, b):
    return len(a & b) / max(1, len(a | b))


def lexical_metrics(question, prior_vocab=None):
    words = tokens(question)
    counts = Counter(words)
    content = {w for w in words if len(w) > 2 and w not in STOPWORDS}
    n = len(words)
    return {"token_count": n, "type_token_ratio": round(len(counts) / max(1, n), 6),
            "corrected_type_token_ratio": round(len(counts) / math.sqrt(max(1, 2 * n)), 6),
            "hapax_ratio": round(sum(x == 1 for x in counts.values()) / max(1, n), 6),
            "distinct_bigrams": round(len(ngrams(words, 2)) / max(1, n - 1), 6),
            "distinct_trigrams": round(len(ngrams(words, 3)) / max(1, n - 2), 6),
            "lexical_entropy": entropy(words),
            "content_word_novelty": round(len(content - (prior_vocab or set())) / max(1, len(content)), 6)}


def metric_decisions(similarities, threshold=0.5):
    cosine = similarities.get("cosine")
    lex = similarities.get("lexical_jaccard", 0)
    return {"cosine_050_reject": cosine is not None and cosine >= .50,
            "cosine_070_reject": cosine is not None and cosine >= .70,
            "cosine_085_reject": cosine is not None and cosine >= .85,
            "cosine_095_reject": cosine is not None and cosine >= .95,
            "lexical_jaccard_050_reject": lex >= .50,
            "char_trigram_050_reject": similarities.get("char_trigram_jaccard", 0) >= .50,
            "exact_reject": similarities.get("exact", 0) == 1,
            "configured_cosine_would_reject": cosine is not None and cosine >= threshold,
            "combined_or_070_lex050_reject": (cosine is not None and cosine >= .70) or lex >= .50,
            "combined_and_050_lex050_reject": (cosine is not None and cosine >= .50) and lex >= .50}


class MetricsIndex:
    """Índice explícito de referência, sem auto-comparação."""
    def __init__(self, embedder, rows=()):
        self.emb = embedder
        self.rows, self.word_sets, self.char_sets, self.normalized = [], [], [], []
        self.q_vectors = np.empty((0, embedder.dim), dtype=np.float32)
        self.qa_vectors = np.empty((0, embedder.dim), dtype=np.float32)
        self.answer_vectors = np.empty((0, embedder.dim), dtype=np.float32)
        self.ids, self.vocab = set(), set()
        self.add_many(rows)

    def add_many(self, rows):
        pending, seen = [], set(self.ids)
        for row in rows:
            if row.get("id") in seen or not row.get("question") or not row.get("answer"):
                continue
            pending.append(row)
            seen.add(row["id"])
        if not pending:
            return
        q_vecs = self.emb.encode([r["question"] for r in pending])
        qa_vecs = self.emb.encode([r["question"] + "\n" + r["answer"] for r in pending])
        self.q_vectors = np.vstack([self.q_vectors, q_vecs])
        self.qa_vectors = np.vstack([self.qa_vectors, qa_vecs])
        self.answer_vectors = np.vstack([self.answer_vectors,self.emb.encode([r['answer'] for r in pending])])
        for row in pending:
            self.rows.append(row)
            self.ids.add(row["id"])
            words = tokens(row["question"])
            self.word_sets.append(set(words))
            self.char_sets.append(chargrams(row["question"]))
            self.normalized.append(" ".join(words))
            self.vocab.update(words)

    def measure(self, row):
        indices = [i for i, r in enumerate(self.rows) if r["id"] != row.get("id")]
        values = lexical_metrics(row["question"], self.vocab)
        values.update(cosine=None, cosine_question_answer=None, lexical_jaccard=0.0,
                      char_trigram_jaccard=0.0, exact=0.0, baseline_size=len(indices),
                      cosine_max_generated=None, cosine_max_seeds=None)
        if not indices:
            return values
        qvec = self.emb.encode([row["question"]])[0]
        qavec = self.emb.encode([row["question"] + "\n" + row["answer"]])[0]
        qs = self.q_vectors[indices] @ qvec
        qas = self.qa_vectors[indices] @ qavec
        ans = self.answer_vectors[indices] @ self.emb.encode([row['answer']])[0]
        words, chars = set(tokens(row["question"])), chargrams(row["question"])
        lex = [jaccard(words, self.word_sets[i]) for i in indices]
        char_scores = [jaccard(chars, self.char_sets[i]) for i in indices]
        for name, scores in (("cosine", qs), ("cosine_question_answer", qas),
                             ('cosine_answer',ans),
                             ("lexical_jaccard", lex), ("char_trigram_jaccard", char_scores)):
            pos = int(np.argmax(scores))
            ref = self.rows[indices[pos]]
            values[name] = round(float(scores[pos]), 6)
            values[f"nearest_{name}_id"] = ref["id"]
            values[f"nearest_{name}_origin"] = ref.get("origin", "generated_qa_v2")
        norm = " ".join(tokens(row["question"]))
        values["exact"] = float(any(self.normalized[i] == norm for i in indices))
        for category in ("generated", "seeds"):
            scores = [float(qs[j]) for j, i in enumerate(indices)
                      if self.rows[i].get('origin','').startswith('generated_qa') == (category == "generated")]
            values[f"cosine_max_{category}"] = round(max(scores), 6) if scores else None
        return values

    def neighbors(self,row,threshold=.85,limit=8):
        if not self.rows:return []
        scores=self.q_vectors @ self.emb.encode([row['question']])[0]
        answer_scores=self.answer_vectors @ self.emb.encode([row['answer']])[0]
        order=np.argsort(-scores)
        return [{'reference':self.rows[i],'cosine_question':float(scores[i]),'cosine_answer':float(answer_scores[i]),
                 'word_jaccard':jaccard(set(tokens(row['question'])),self.word_sets[i])}
                for i in order if self.rows[i]['id']!=row.get('id') and scores[i]>=threshold][:limit]


class DiagnosticBaselines:
    """Bases separadas para estudo; nunca entram na aprovação ou na parada."""
    def __init__(self,embedder,seeds,records):
        self.indices={'seeds':MetricsIndex(embedder,seeds),
                      'accepted':MetricsIndex(embedder,[r for r in records if r.get('accepted')]),
                      'rejected':MetricsIndex(embedder,[r for r in records if not r.get('accepted')])}

    def measure(self,row):
        return {name:index.measure(row) for name,index in self.indices.items()}

    def add(self,row):
        self.indices['accepted' if row['accepted'] else 'rejected'].add_many([row])


def saturation_signals(history, current, cfg):
    last = (history + [current])[-cfg.entropy_patience:]
    warm = current.get("entropy_reliable", False) and current["accepted_total"] >= cfg.entropy_warmup
    enough = warm and len(last) == cfg.entropy_patience
    signals = {}
    for cutoff in (.005, .010, .020, cfg.entropy_gain_threshold):
        signals[f"entropy_gain_below_{cutoff:.3f}"] = bool(enough and all(
            r.get("entropy_gain") is not None and r["entropy_gain"] < cutoff for r in last))
    signals["low_acceptance"] = bool(enough and all(r["acceptance_rate"] <= .10 for r in last))
    signals["no_new_clusters"] = bool(enough and all(r.get("new_clusters") == 0 for r in last))
    signals["high_mean_cosine_085"] = bool(enough and all(
        r.get("mean_cosine") is not None and r["mean_cosine"] >= .85 for r in last))
    signals["configured_saturation_would_stop"] = signals[f"entropy_gain_below_{cfg.entropy_gain_threshold:.3f}"]
    return signals
