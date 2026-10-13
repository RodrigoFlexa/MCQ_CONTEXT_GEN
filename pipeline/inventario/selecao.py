"""Etapa 3: escolha dos trechos de cada assunto.

candidatos lexicais -> similaridade densa com DUAS consultas (pt e en; vale a maior,
para não penalizar HSE/BSEE em inglês) -> reranker cross-encoder opcional ->
piso de relevância (absoluto e relativo ao melhor) -> cota mínima por coleção ->
MMR (diversidade) com teto por documento.
"""
from collections import Counter

import numpy as np

from .textutil import squash, sha

VERSION = 'selecao-v3-bilingue-cotas'

# Pisos por modo de pontuação, calibrados com text-embedding-3-large em trechos reais de
# Produção (2026-10-13): relevantes 0,60-0,74; trechos de outro subtópico do mesmo domínio
# até ~0,69 (p90 ~0,50). O cosseno só separa o grosseiro; a pertinência fina fica com o LLM.
DEFAULT_FLOOR = {'cosine': 0.45, 'cross_encoder': 0.10, 'hash': 0.0}
DEFAULT_REL = {'cosine': 0.82, 'cross_encoder': 0.30, 'hash': 0.0}


def assunto_queries(a):
    pt = f"{a['texto']}. {a['consulta_pt']}"
    en = a['consulta_en'] + (('. ' + ', '.join(a.get('termos_en', [])[:6])) if a.get('termos_en') else '')
    return pt, en


def score_mode(embedder, reranker):
    if reranker is not None and getattr(reranker, 'name', None) not in (None, 'hash', 'cosine'):
        return 'cross_encoder'
    return 'hash' if getattr(embedder, 'name', '') == 'hash' else 'cosine'


def select_for_assunto(a, candidates, emb_cache, embedder, reranker=None, dense_top=60, k=12, min_score=None,
                       rel_score=None, min_por_colecao=2, max_por_documento=3, mmr_lambda=0.75, dup=0.95,
                       batch=32, rerank_batch=32):
    uniq = {}
    for c in sorted(candidates, key=lambda c: (-c['lex_score'], c['chunk_id'])):
        uniq.setdefault(sha(squash(c['texto'][:2000]), 20), c)
    pool = list(uniq.values())
    mode = score_mode(embedder, reranker)
    floor = DEFAULT_FLOOR[mode] if min_score is None else min_score
    rel = DEFAULT_REL[mode] if rel_score is None else rel_score
    info = {'candidatos': len(candidates), 'unicos': len(pool), 'elegiveis': 0, 'selecionados': 0,
            'modo': mode, 'piso': floor, 'candidatos_por_colecao': dict(Counter(c['collection'] for c in pool))}
    if not pool:
        info['colecoes'] = {}
        return [], info
    q_pt, q_en = assunto_queries(a)
    qv = embedder.encode([q_pt, q_en])
    vecs = emb_cache.encode(embedder, [c['texto'] for c in pool], batch_size=batch)
    dense = np.maximum(vecs @ qv[0], vecs @ qv[1])
    order = np.argsort(-dense, kind='stable')[:dense_top]
    shortlist = [pool[i] for i in order]
    svecs = vecs[order]
    if mode == 'cross_encoder':
        scores = np.asarray(reranker.score(q_pt, [c['texto'] for c in shortlist], batch_size=rerank_batch),
                            dtype=np.float32)
    else:
        scores = dense[order].astype(np.float32)
    if len(scores) != len(shortlist) or not np.isfinite(scores).all():
        raise ValueError('Scores de seleção incompletos ou inválidos')
    best = float(scores.max())
    cut = max(floor, rel * best)
    eligible = [i for i in range(len(shortlist)) if scores[i] >= cut]
    info.update(elegiveis=len(eligible), score_max=round(best, 4), corte=round(cut, 4))

    chosen, per_doc = [], Counter()

    def admissible(i):
        c = shortlist[i]
        if c['collection'] != 'petroles' and per_doc[c['document_id']] >= max_por_documento:
            return False
        return all(float(svecs[i] @ svecs[j]) < dup for j in chosen)

    def take(i):
        chosen.append(i)
        per_doc[shortlist[i]['document_id']] += 1

    # 1) cota mínima por coleção (as mais bem pontuadas de cada uma, se elegíveis)
    by_coll = {}
    for i in sorted(eligible, key=lambda i: -scores[i]):
        by_coll.setdefault(shortlist[i]['collection'], []).append(i)
    for coll in sorted(by_coll, key=lambda c: -scores[by_coll[c][0]]):
        taken = 0
        for i in by_coll[coll]:
            if len(chosen) >= k or taken >= min_por_colecao:
                break
            if admissible(i):
                take(i)
                taken += 1
    # 2) restante por MMR
    rest = [i for i in eligible if i not in chosen]
    while rest and len(chosen) < k:
        best_i, best_val = None, -1e9
        for i in rest:
            if not admissible(i):
                continue
            sim = max((float(svecs[i] @ svecs[j]) for j in chosen), default=0.0)
            val = mmr_lambda * float(scores[i]) - (1 - mmr_lambda) * sim
            if val > best_val:
                best_i, best_val = i, val
        if best_i is None:
            break
        take(best_i)
        rest.remove(best_i)
    chosen.sort(key=lambda i: -scores[i])
    out = []
    for rank, i in enumerate(chosen):
        c = dict(shortlist[i])
        c['dense'] = round(float(dense[order[i]]), 4)
        c['score'] = round(float(scores[i]), 4)
        c['rank'] = rank
        out.append(c)
    info['selecionados'] = len(out)
    info['colecoes'] = dict(Counter(c['collection'] for c in out))
    return out, info
