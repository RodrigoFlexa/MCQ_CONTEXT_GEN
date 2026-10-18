"""Busca complementar limitada nos candidatos originais, sem inventar evidência."""
from .textutil import content_words


def retrieve(gaps, candidates, excluded=(), limit=4):
    """Busca lexical bilíngue por lacuna; uma passagem precisa casar >=2 termos."""
    excluded, found = set(excluded), {}
    for gap in gaps[:2]:
        query = set(content_words(gap.get('consulta_pt', '') + ' ' + gap.get('consulta_en', '')))
        scored = []
        for chunk in candidates:
            if chunk['chunk_id'] in excluded:
                continue
            overlap = len(query & set(content_words(chunk['texto'])))
            if overlap >= 2:
                scored.append((overlap, chunk))
        for score, chunk in sorted(scored, key=lambda x: (-x[0], x[1]['chunk_id']))[:2]:
            found.setdefault(chunk['chunk_id'], {**chunk, 'lacuna': gap['lacuna'], 'score_complemento': score})
    return list(found.values())[:limit]
