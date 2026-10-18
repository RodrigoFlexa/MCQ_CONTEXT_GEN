"""Novidade das perguntas aprovadas, na ordem em que foram planejadas (observacional, não filtra).

Para cada aprovada de um subtópico, compara com as aprovadas ANTERIORES do mesmo subtópico:
cosseno do embedding (pergunta + resposta) e, quando o vizinho mais próximo passa do limiar, um modelo
pequeno confirma se os pares avaliam o mesmo conhecimento. O resultado alimenta o estudo dos critérios
de parada: curva de redundância ao longo da fila.
"""
import json
from concurrent.futures import ThreadPoolExecutor, as_completed

import numpy as np

from pipeline.inventario.llm import CallFailed, ContentFiltered

VERSION = 'novidade-v2-escopo'
JULGAMENTOS = ('redundante', 'sobreposicao', 'distinta')

SYSTEM = """Você compara uma questão NOVA de avaliação técnica (FPSO/FSO) com questões já aprovadas do banco no mesmo domínio. Para cada anterior, classifique:
- redundante: avalia essencialmente o mesmo conhecimento e a resposta essencial é a mesma, mesmo com outra redação ou cenário;
- sobreposicao: compartilha parte do conhecimento, mas a nova exige algo relevante que a anterior não exige;
- distinta: avalia conhecimento diferente.
Julgue o conhecimento exigido, não as palavras. Retorne JSON: {"pares":[{"id":"id da anterior","julgamento":"redundante|sobreposicao|distinta","razao":"curta"}]}"""


def text_of(q):
    return q['pergunta'] + '\n' + q['resposta']


def _pair_check(llm, q, neighbors):
    ids = {n['id'] for n in neighbors}

    def check(data):
        got = {p.get('id') for p in data.get('pares', []) if isinstance(p, dict)}
        if got != ids or any(p.get('julgamento') not in JULGAMENTOS for p in data['pares']):
            raise ValueError('um julgamento válido por id: ' + ', '.join(sorted(ids)))
    user = json.dumps({'nova': {'pergunta': q['pergunta'], 'resposta': q['resposta']},
                       'anteriores': [{'id': n['id'], 'pergunta': n['pergunta'], 'resposta': n['resposta']}
                                      for n in neighbors]}, ensure_ascii=False)
    data = llm.json(SYSTEM, user, tag='qa_novidade', max_tokens=4000, validate=check, item=q['id'])
    return {p['id']: {'julgamento': p['julgamento'], 'razao': p.get('razao', '')} for p in data['pares']}


def measure(rows, embed, llm, limiar=0.70, vizinhos=3, workers=8, scope='subtopico'):
    """Anota q['novidade'] nas aprovadas e devolve a curva por subtópico. embed(textos) -> vetores normalizados."""
    approved = [q for q in rows if q.get('status') == 'aprovada']
    by_sub = {}
    for q in approved:
        key = q['topico'] if scope == 'topico' else q['sub_key']
        by_sub.setdefault(key, []).append(q)
    jobs = []
    for qs in by_sub.values():
        qs.sort(key=lambda q: (q.get('ordem', 0), q['id']))
        vecs = np.asarray(embed([text_of(q) for q in qs]), dtype=np.float32)
        for k, q in enumerate(qs):
            info = {'version': VERSION, 'posicao': k + 1, 'max_cos': None, 'vizinhos': [], 'checado': False,
                    'redundante': False}
            if k:
                sims = vecs[:k] @ vecs[k]
                top = np.argsort(-sims)[:vizinhos]
                info['max_cos'] = round(float(sims[top[0]]), 4)
                info['vizinhos'] = [{'id': qs[i]['id'], 'cos': round(float(sims[i]), 4)} for i in top]
                info['acima_limiar'] = sum(float(sims[i]) >= limiar for i in top)
                close = [qs[i] for i in top]  # Similaridade baixa não prova conhecimento distinto.
                if close:
                    jobs.append((q, close))
            q['novidade'] = info
    with ThreadPoolExecutor(workers) as pool:
        futs = {pool.submit(_pair_check, llm, q, close): q for q, close in jobs}
        for f in as_completed(futs):
            q = futs[f]
            try:
                verdict = f.result()
            except (ContentFiltered, CallFailed) as e:
                q['novidade']['erro'] = str(e)[:200]
                continue
            for n in q['novidade']['vizinhos']:
                n.update(verdict.get(n['id'], {}))
            q['novidade']['checado'] = True
            q['novidade']['redundante'] = any(n.get('julgamento') == 'redundante' for n in q['novidade']['vizinhos'])
    curves = {}
    for key, qs in by_sub.items():
        curves[key] = {'topico': qs[0]['topico'], 'subtopico': qs[0]['topico'] if scope == 'topico' else qs[0]['subtopico'], 'escopo': scope,
                       'sequencia': [{'id': q['id'], 'ordem': q.get('ordem'), 'tipo': q['tipo'],
                                      'max_cos': q['novidade']['max_cos'], 'redundante': q['novidade']['redundante']}
                                     for q in qs]}
    return curves


def windows(seq, size=20):
    """Fração de redundantes por janela consecutiva de aprovadas."""
    out = []
    for i in range(0, len(seq), size):
        part = seq[i:i + size]
        out.append({'de': i + 1, 'ate': i + len(part), 'redundantes': sum(s['redundante'] for s in part),
                    'fracao': round(sum(s['redundante'] for s in part) / len(part), 3)})
    return out
