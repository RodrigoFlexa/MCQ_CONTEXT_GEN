"""Redundância semântica com embeddings Azure (opcional).

A medida lexical (TF-IDF) só vê repetição quase literal. A repetição que o especialista
apontou é de conceito, com outras palavras; por isso o relatório também mede, quando
configurado, a fração de sentenças com uma paráfrase em outro bloco (cosseno de
embeddings ≥ limiar). Cache por conteúdo em .local; sem numpy.
"""
import hashlib
import json
import math
from pathlib import Path

from pipeline.inventario.textutil import atomic_json, read_json
from . import textos as T


def _key(text, spec):
    return hashlib.sha256(json.dumps([spec, text], ensure_ascii=False).encode()).hexdigest()


async def embed(calls, texts, spec, cache_path):
    cache = read_json(cache_path) or {}
    missing = [t for t in dict.fromkeys(texts) if _key(t, spec) not in cache]
    if missing:
        if calls.client is None:
            calls.make_client()
        for start in range(0, len(missing), 256):
            batch = missing[start:start + 256]
            response = await calls.client.embeddings.create(model=spec['deployment'], input=batch,
                                                            dimensions=spec['dimensions'])
            for text, item in zip(batch, response.data):
                vector = item.embedding
                size = math.sqrt(sum(v * v for v in vector)) or 1.0
                cache[_key(text, spec)] = [round(v / size, 6) for v in vector]
        atomic_json(cache_path, cache)
    return [cache[_key(t, spec)] for t in texts]


def _dot(a, b):
    return sum(x * y for x, y in zip(a, b))


async def redundancy(calls, document, spec, cache_path):
    rows = [(bid, s) for bid, _, text in T.blocks_of(document) for s in T.sentences(text)]
    if len(rows) < 2:
        return dict(taxa_redundancia_semantica=0.0, similaridade_maxima_media_semantica=0.0, limiar=spec['threshold'])
    vectors = await embed(calls, [s for _, s in rows], spec, cache_path)
    best = [0.0] * len(rows)
    for i in range(len(rows)):
        for j in range(i + 1, len(rows)):
            if rows[i][0] == rows[j][0]:
                continue
            sim = _dot(vectors[i], vectors[j])
            if sim > best[i]:
                best[i] = sim
            if sim > best[j]:
                best[j] = sim
    flagged = sum(1 for b in best if b >= spec['threshold'])
    return dict(taxa_redundancia_semantica=round(flagged / len(rows), 4),
                similaridade_maxima_media_semantica=round(sum(best) / len(best), 4), limiar=spec['threshold'])


def cross(vectors_by_doc, threshold):
    """Fração de sentenças com paráfrase em outro documento; usa numpy se disponível."""
    try:
        import numpy as np
    except ImportError:
        return None
    ids = [d for d, v in vectors_by_doc.items() if v]
    if len(ids) < 2:
        return None
    mats = {d: np.asarray(vectors_by_doc[d], dtype=np.float32) for d in ids}
    out = {}
    for d in ids:
        others = np.concatenate([mats[o] for o in ids if o != d])
        sims = mats[d] @ others.T
        out[d] = round(float((sims.max(axis=1) >= threshold).mean()), 4)
    return out


def load_vectors(folder, spec, name):
    """Vetores das sentenças de um documento já medido (para a medida entre documentos)."""
    cache = read_json(Path(folder) / '.local' / 'embeddings.json') or {}
    doc = read_json(Path(folder) / name)
    if not doc:
        return []
    texts = [s for _, _, t in T.blocks_of(doc) for s in T.sentences(t)]
    return [cache[_key(t, spec)] for t in texts if _key(t, spec) in cache]
