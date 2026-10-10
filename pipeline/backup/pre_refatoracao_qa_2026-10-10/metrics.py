"""Métricas observacionais e regras configuráveis para a geração QA."""
from __future__ import annotations

import math
import re
import unicodedata
from collections import Counter

TOKEN_RE = re.compile(r"[\wÀ-ÿ]+", re.UNICODE)


def tokens(text: str) -> list[str]:
    return [t.casefold() for t in TOKEN_RE.findall(unicodedata.normalize("NFKC", text or ""))]


def lexical_metrics(question: str, prior_questions: list[str]) -> dict:
    words = tokens(question)
    unique = set(words)
    grams = {" ".join(words[i:i + 3]) for i in range(max(0, len(words) - 2))}
    prior_tokens = set(tokens(" ".join(prior_questions)))
    content = [w for w in words if len(w) > 3]
    content_unique = set(content)
    return {
        "token_count": len(words),
        "type_token_ratio": round(len(unique) / max(1, len(words)), 4),
        "trigram_count": len(grams),
        "content_word_novelty": round(len(content_unique - prior_tokens) / max(1, len(content_unique)), 4),
    }


def exact_similarity(a: str, b: str) -> float:
    aa, bb = " ".join(tokens(a)), " ".join(tokens(b))
    return 1.0 if aa and aa == bb else 0.0


def lexical_jaccard(a: str, b: str) -> float:
    aa, bb = set(tokens(a)), set(tokens(b))
    return len(aa & bb) / max(1, len(aa | bb))


def char_ngram_similarity(a: str, b: str, n: int = 3) -> float:
    def grams(s):
        compact = " ".join(tokens(s))
        return {compact[i:i+n] for i in range(max(1, len(compact)-n+1))}
    aa, bb = grams(a), grams(b)
    return len(aa & bb) / max(1, len(aa | bb))


def entropy(values: list[str]) -> float:
    vals = [v for v in values if v]
    if not vals:
        return 0.0
    counts = Counter(vals)
    h = -sum((n / len(vals)) * math.log2(n / len(vals)) for n in counts.values())
    return round(h / math.log2(len(counts)), 4) if len(counts) > 1 else 0.0


class SimilarityModel:
    def __init__(self, model_name="sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2"):
        from sentence_transformers import SentenceTransformer
        self.model_name = model_name
        self.model = SentenceTransformer(model_name)
        self._vectors = {}

    def matrix(self, texts: list[str]):
        return self.model.encode(texts, normalize_embeddings=True, show_progress_bar=False)

    def score(self, question: str, candidates: list[str]) -> float | None:
        if not candidates:
            return None
        import numpy as np
        missing = list(dict.fromkeys(t for t in [question, *candidates] if t not in self._vectors))
        if missing:
            encoded = self.matrix(missing)
            self._vectors.update({text: vec for text, vec in zip(missing, encoded)})
        qvec = self._vectors[question]
        refs = np.stack([self._vectors[t] for t in candidates])
        return float(np.max(refs @ qvec))


def all_similarities(question: str, prior: list[str], model: SimilarityModel | None) -> dict:
    if not prior:
        return {"cosine": None, "lexical_jaccard": 0.0, "char_trigram_jaccard": 0.0, "exact": 0.0}
    return {
        "cosine": round(model.score(question, prior), 4) if model else None,
        "lexical_jaccard": round(max(lexical_jaccard(question, p) for p in prior), 4),
        "char_trigram_jaccard": round(max(char_ngram_similarity(question, p) for p in prior), 4),
        "exact": max(exact_similarity(question, p) for p in prior),
    }


def metric_decisions(similarities: dict, threshold: float = 0.50) -> dict:
    cosine = similarities.get("cosine")
    return {
        "cosine_050_reject": cosine is not None and cosine >= 0.50,
        "cosine_070_reject": cosine is not None and cosine >= 0.70,
        "cosine_085_reject": cosine is not None and cosine >= 0.85,
        "lexical_jaccard_050_reject": similarities["lexical_jaccard"] >= 0.50,
        "char_trigram_050_reject": similarities["char_trigram_jaccard"] >= 0.50,
        "exact_reject": similarities["exact"] >= 1.0,
        "active_cosine_reject": cosine is not None and cosine >= threshold,
        "combined_or_070_lex050_reject": (cosine is not None and cosine >= 0.70) or similarities["lexical_jaccard"] >= 0.50,
        "combined_and_050_lex050_reject": (cosine is not None and cosine >= 0.50) and similarities["lexical_jaccard"] >= 0.50,
    }
