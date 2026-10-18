"""Plano de geração: fila ordenada de alvos por subtópico e cota por tópico.

Cada alvo de uma nota vira no máximo UMA pergunta. A fila reveza níveis (padrão 3 fácil : 4 média :
2 difícil A : 1 difícil B), assuntos e notas: uma nota só recebe a segunda pergunta depois que todas
as notas com alvo disponível naquele nível receberam a primeira. As combinações de notas viram difícil B.
Quando um nível se esgota, a fila usa o que restar, até acabar (modo profundo).
"""
import random
from collections import Counter
from pipeline.inventario.conhecimento import target_contract

PADRAO = ('facil', 'media', 'dificil_A', 'media', 'facil', 'dificil_B', 'media', 'dificil_A', 'facil', 'media')
NIVEL_DO_TIPO = {'facil': 'facil', 'media': 'media', 'dificil_A': 'dificil', 'dificil_B': 'dificil'}
RESERVA = {'facil': ('media', 'dificil_A', 'dificil_B'), 'media': ('facil', 'dificil_A', 'dificil_B'),
           'dificil_A': ('dificil_B', 'media', 'facil'), 'dificil_B': ('dificil_A', 'media', 'facil')}


def combo_alvo(c):
    return (f"{c['titulo']}. Ligação: {c['ligacao']} Raciocínio exigido: {c['raciocinio']} "
            f"Esboço de cenário: {c['cenario']}")


def build_queue(sub, seed):
    """Fila completa e determinística de lotes de UM alvo para o subtópico."""
    rng = random.Random(f'{seed}:{sub["key"]}:fila')
    by_nid = {n['nid']: n for n in sub['notas']}
    order = {n['nid']: i for i, n in enumerate(rng.sample(sub['notas'], len(sub['notas'])))}
    pools = {lvl: {} for lvl in ('facil', 'media', 'dificil')}
    for n in sub['notas']:
        for i, a in enumerate(n['alvos']):
            if a.get('nivel') in pools:
                pools[a['nivel']].setdefault(n['nid'], []).append(i)
    for lvl in pools:
        for idx in pools[lvl].values():
            rng.shuffle(idx)
    combos = [c for c in sub['combinacoes'] if all(nid in by_nid for nid in c['notas'])]
    rng.shuffle(combos)
    uses_note, uses_assunto = Counter(), Counter()
    last_assunto, queue, step = None, [], 0

    def available(tipo):
        if tipo == 'dificil_B':
            return bool(combos)
        return any(pools[NIVEL_DO_TIPO[tipo]].values())

    while any(available(t) for t in ('facil', 'media', 'dificil_A', 'dificil_B')):
        want = PADRAO[step % len(PADRAO)]
        step += 1
        tipo = want if available(want) else next(t for t in RESERVA[want] if available(t))
        if tipo == 'dificil_B':
            c = combos.pop(0)
            notes = [by_nid[nid] for nid in c['notas']]
            alvo = {'tipo': 'dificil_B', 'descricao': combo_alvo(c)}
            if c.get('criterios_correcao'):
                needed = {k['nid']: set(k.get('relacoes', [])) for k in c['conhecimentos']}
                alvo['resposta_esperada'] = c['resposta']
                alvo['contrato'] = {k: c[k] for k in ('criterios_correcao', 'condicoes_enunciado', 'limites')}
                alvo['contrato'].update(habilidade='integracao',
                    fatos=list(dict.fromkeys(f for n in notes for r in n['relacoes']
                                             if r['id'] in needed.get(n['nid'], set()) for f in r['fatos'])),
                    relacoes=[n['nid'] + ':' + rid for n in notes for rid in sorted(needed.get(n['nid'], []))])
            batch = {'notas': notes, 'combinacao': c, 'alvos': [alvo], 'alvo_ref': c['cid']}
        else:
            lvl = NIVEL_DO_TIPO[tipo]
            cands = [nid for nid, idx in pools[lvl].items() if idx]

            def key(nid):
                a = by_nid[nid]['assuntos'][0] if by_nid[nid]['assuntos'] else ''
                return uses_note[nid], uses_assunto[a], a == last_assunto, order[nid]
            nid = min(cands, key=key)
            i = pools[lvl][nid].pop(0)
            n = by_nid[nid]
            alvo = {'tipo': tipo, 'descricao': n['alvos'][i]['descricao'],
                    'contrato': target_contract(n['alvos'][i]),
                    **({'resposta_esperada': n['alvos'][i]['resposta']} if n['alvos'][i].get('resposta') else {})}
            batch = {'notas': [n], 'alvos': [alvo], 'alvo_ref': f'{nid}#alvo{i}'}
        for n in batch['notas']:
            uses_note[n['nid']] += 1
            if n['assuntos']:
                uses_assunto[n['assuntos'][0]] += 1
        last_assunto = batch['notas'][0]['assuntos'][0] if batch['notas'][0]['assuntos'] else None
        batch['ordem'] = len(queue)
        batch['id'] = f"{sub['key']}-s{batch['ordem']:04d}"
        batch['alvos'] = [{'aid': 'A1', **batch['alvos'][0]}]
        queue.append(batch)
    return queue


def allocate(subs, por_topico, minimo):
    """Cota de perguntas por subtópico: proporcional às notas aprovadas, com piso, somando por_topico."""
    by_topic = {}
    for s in subs:
        by_topic.setdefault(s['topico'], []).append(s)
    quota = {}
    for topic, ss in by_topic.items():
        base = {s['key']: min(minimo, por_topico // len(ss)) for s in ss}
        rest = por_topico - sum(base.values())
        weights = {s['key']: len(s['notas']) for s in ss}
        total = sum(weights.values()) or 1
        raw = {k: rest * w / total for k, w in weights.items()}
        extra = {k: int(v) for k, v in raw.items()}
        left = rest - sum(extra.values())
        for k in sorted(raw, key=lambda k: raw[k] - extra[k], reverse=True)[:left]:
            extra[k] += 1
        for k in base:
            quota[k] = base[k] + extra[k]
    return quota
