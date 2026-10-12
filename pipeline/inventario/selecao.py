"""Etapa 3: ordenação fina dos candidatos de cada assunto (GPU).

candidatos lexicais -> similaridade densa (bge-m3) -> top N -> reranker
cross-encoder -> limiar mínimo -> MMR (diversidade) com teto por documento.
"""
import numpy as np

from .textutil import squash, sha

VERSION = 'selecao-v2'


def assunto_query(a):
    return f"{a['texto']}. {a['consulta_pt']} / {a['consulta_en']}"


def select_for_assunto(a, candidates, emb_cache, embedder, reranker, dense_top=60, k=12,
                       min_rerank=0.10, mmr_lambda=0.75, dup=0.95, max_per_doc=4, batch=32, rerank_batch=32):
    uniq = {}
    for c in sorted(candidates, key=lambda c: (-c['lex_score'], c['chunk_id'])):
        uniq.setdefault(sha(squash(c['texto'][:2000]), 20), c)
    pool = list(uniq.values())
    info = {'candidatos': len(candidates), 'unicos': len(pool), 'acima_limiar': 0, 'selecionados': 0}
    info['score_mode'] = 'cosine' if getattr(reranker, 'name', None) in ('hash', 'cosine') else 'cross_encoder'
    if not pool:
        return [], info
    q = assunto_query(a)
    qv = embedder.encode([q])[0]
    vecs = emb_cache.encode(embedder, [c['texto'] for c in pool], batch_size=batch)
    dense = vecs @ qv
    order = np.argsort(-dense)[:dense_top]
    shortlist = [pool[i] for i in order]
    svecs = vecs[order]
    rr = reranker.score(q, [c['texto'] for c in shortlist], batch_size=rerank_batch)
    if len(rr) != len(shortlist) or not np.isfinite(rr).all():
        raise ValueError('Scores de seleção incompletos ou inválidos')
    keep = [i for i in range(len(shortlist)) if rr[i] >= min_rerank]
    info['acima_limiar'] = len(keep)
    chosen, per_doc = [], {}
    while keep and len(chosen) < k:
        best, best_val = None, -1e9
        for i in keep:
            sim = max((float(svecs[i] @ svecs[j]) for j in chosen), default=0.0)
            if sim >= dup:
                continue
            doc = shortlist[i]['document_id']
            if shortlist[i]['collection'] != 'petroles' and per_doc.get(doc, 0) >= max_per_doc:
                continue
            val = mmr_lambda * float(rr[i]) - (1 - mmr_lambda) * sim
            if val > best_val:
                best, best_val = i, val
        if best is None:
            break
        chosen.append(best)
        keep.remove(best)
        doc = shortlist[best]['document_id']
        per_doc[doc] = per_doc.get(doc, 0) + 1
    out = []
    for rank, i in enumerate(chosen):
        c = dict(shortlist[i])
        c['dense'] = round(float(dense[order[i]]), 4)
        c['rerank'] = round(float(rr[i]), 4)
        c['rank'] = rank
        out.append(c)
    info['selecionados'] = len(out)
    info['rerank_max'] = round(float(rr.max()), 4) if len(rr) else None
    info['colecoes'] = sorted({c['collection'] for c in out})
    return out, info
