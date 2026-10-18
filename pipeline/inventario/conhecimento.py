"""Proveniência e limites do conhecimento usado na avaliação profissional.

Contribuições paramétricas enriquecem a explicação, mas não viram evidência por
receber uma citação. Deduções só são avaliáveis quando todas as premissas também
são avaliáveis. A correção semântica continua sendo responsabilidade do revisor.
"""
SCHEMA = 'nota-v5'
ORIGENS = ('fonte', 'deducao', 'parametrico')
NATUREZAS = ('principio', 'requisito', 'procedimento_local', 'estudo', 'incidente', 'checklist')
APLICACOES = ('fpso', 'transferivel', 'restrita')


def texts(value):
    return list(dict.fromkeys(' '.join(x.split()) for x in value if isinstance(x, str) and x.strip())) \
        if isinstance(value, list) else []


def normalize(raw, idmap):
    """Normaliza o contrato novo; nunca promove material legado automaticamente."""
    if raw.get('schema_conhecimento') != SCHEMA:
        return {}, []
    relations, alerts = {}, []
    for r in raw.get('relacoes', []):
        if not isinstance(r, dict):
            raise ValueError('relação deve ser um objeto')
        rid = r.get('id')
        if not isinstance(rid, str) or not rid.strip() or rid in relations:
            raise ValueError('ids de relações devem ser únicos e não vazios')
        if r.get('origem') not in ORIGENS or r.get('natureza') not in NATUREZAS:
            raise ValueError(f'{rid}: origem/natureza inválida')
        if r.get('aplicabilidade') not in APLICACOES:
            raise ValueError(f'{rid}: aplicabilidade inválida')
        statement = ' '.join(str(r.get('afirmacao') or '').split())
        if not statement:
            raise ValueError(f'{rid}: afirmação vazia')
        refs = texts(r.get('fatos'))
        if any(f not in idmap for f in refs):
            raise ValueError(f'{rid}: referência inexistente')
        relations[rid] = {
            'id': rid, 'afirmacao': statement, 'origem': r['origem'], 'natureza': r['natureza'],
            'aplicabilidade': r['aplicabilidade'], 'condicoes': texts(r.get('condicoes')),
            'limites': texts(r.get('limites')), 'premissas': texts(r.get('premissas')),
            'fatos': [idmap[f] for f in refs],
            'justificativa_transferencia': str(r.get('justificativa_transferencia') or '').strip(),
        }
    visiting = set()

    def evaluate(rid):
        if rid not in relations:
            raise ValueError(f'premissa inexistente: {rid}')
        r = relations[rid]
        if 'avaliavel' in r:
            return r['avaliavel']
        if rid in visiting:
            raise ValueError('ciclo entre premissas de relações')
        visiting.add(rid)
        premise_ok = [evaluate(p) for p in r['premissas']]
        for p in r['premissas']:
            r['fatos'] = list(dict.fromkeys(r['fatos'] + relations[p]['fatos']))
            for field in ('condicoes', 'limites'):
                r[field] = list(dict.fromkeys(r[field] + relations[p][field]))
        eligible = r['aplicabilidade'] != 'restrita' and r['natureza'] not in (
            'estudo', 'incidente', 'checklist', 'procedimento_local')
        if r['aplicabilidade'] == 'transferivel' and not r['justificativa_transferencia']:
            eligible = False
        if r['origem'] == 'parametrico':
            eligible = False
        elif r['origem'] == 'fonte':
            eligible = eligible and bool(r['fatos']) and all(premise_ok)
        else:
            eligible = eligible and bool(premise_ok) and all(premise_ok) and bool(r['fatos'])
        r['avaliavel'] = bool(eligible)
        visiting.remove(rid)
        return r['avaliavel']

    for rid in relations:
        evaluate(rid)
    targets, blocked, seen = [], [], set()
    for a in raw.get('alvos', []):
        if not isinstance(a, dict):
            continue
        refs = texts(a.get('relacoes'))
        reasons = []
        if not refs or any(r not in relations or not relations[r]['avaliavel'] for r in refs):
            reasons.append('relacao_sem_suporte_avaliavel')
        answer = str(a.get('resposta') or '').strip()
        criteria = texts(a.get('criterios_correcao'))
        description = str(a.get('descricao') or '').strip()
        if not answer or not criteria or not description or a.get('nivel') not in ('facil', 'media', 'dificil'):
            reasons.append('contrato_incompleto')
        # Mesma relação + mesma habilidade não cria diversidade por trocar palavras/nível.
        skill = str(a.get('habilidade') or 'compreensao').strip()
        key = (tuple(sorted(refs)), skill)
        if key in seen:
            reasons.append('relacao_habilidade_repetida')
        if reasons:
            blocked.append({**a, 'motivos': reasons})
            continue
        seen.add(key)
        targets.append({
            'nivel': a['nivel'], 'descricao': description, 'resposta': answer, 'habilidade': skill,
            'relacoes': refs, 'criterios_correcao': criteria,
            'respostas_aceitaveis': texts(a.get('respostas_aceitaveis')),
            'condicoes_enunciado': list(dict.fromkeys(texts(a.get('condicoes_enunciado')) +
                [condition for rid in refs for condition in relations[rid]['condicoes']])),
            'limites': texts(a.get('limites')) + list(dict.fromkeys(
                limit for rid in refs for limit in relations[rid]['limites'])),
            'fatos': list(dict.fromkeys(f for rid in refs for f in relations[rid]['fatos'])),
        })
    if blocked:
        alerts.append(f'alvos_bloqueados:{len(blocked)}')
    gaps = []
    for gap in raw.get('buscas_complementares', [])[:2]:
        if isinstance(gap, dict) and gap.get('lacuna') and (gap.get('consulta_pt') or gap.get('consulta_en')):
            gaps.append({k: str(gap.get(k) or '').strip() for k in ('lacuna', 'consulta_pt', 'consulta_en')})
    return {'schema_conhecimento': SCHEMA, 'relacoes': list(relations.values()), 'alvos': targets,
            'alvos_bloqueados': blocked, 'buscas_complementares': gaps}, alerts


def payload(note, reverse):
    """Converte referências persistidas de volta para F#/T# sem perder o contrato."""
    if note.get('schema_conhecimento') != SCHEMA:
        return {}
    return {'schema_conhecimento': SCHEMA,
            'relacoes': [{**r, 'fatos': [reverse[f] for f in r['fatos'] if f in reverse]}
                         for r in note['relacoes']],
            'alvos': [{**a, 'fatos': [reverse[f] for f in a['fatos'] if f in reverse]} for a in note['alvos']],
            'buscas_complementares': note.get('buscas_complementares', [])}


def target_contract(target):
    return {k: target[k] for k in ('relacoes', 'fatos', 'habilidade', 'criterios_correcao',
                                  'respostas_aceitaveis', 'condicoes_enunciado', 'limites') if k in target}
