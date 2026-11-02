"""Evidência antes da pergunta; um reparo; inventário por competência."""
import json
import re
from collections import Counter
from pathlib import Path
from pipeline.inventario.textutil import atomic_json, read_json
from pipeline.qa_research.v3.runtime import Calls, digest, topic, CallFailure, Fatal
from . import VERSION, contracts as C, prompts as P
from .documents import flatten


def key(text):
    return ' '.join(re.findall(r'\w+', text.casefold()))


def selected(target, blocks):
    ids = {e['bloco'] for a in target['afirmacoes'] for e in a['evidencias']}
    return [b for bid, b in blocks.items() if bid in ids]


def jsonl(path, rows):
    path = Path(path); path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_suffix('.tmp')
    temporary.write_text(''.join(json.dumps(q, ensure_ascii=False) + '\n' for q in rows), encoding='utf-8')
    temporary.replace(path)


async def generate(document, item, group, config, output, examples=(), pending=(), transport=None):
    output = Path(output); output.mkdir(parents=True, exist_ok=True)
    blocks = {b['id']: b for b in flatten(document)}
    identity = dict(schema=VERSION, documento=digest(document), item=item, grupo=group,
        config={k:v for k,v in config.items() if k not in ('workers', 'max_calls', 'heartbeat', 'verbose')},
        exemplos=list(examples), pendencias=list(pending),
        prompts={name:digest(getattr(P,name)) for name in ('PLAN','AUTHOR','SOLVE','JUDGE')},
        codigo={p.name:digest(p.read_text(encoding='utf-8')) for p in Path(__file__).parent.glob('*.py')})
    old = read_json(output / 'identidade.json')
    C.require(old is None or old == identity, 'Documento/gerador/protocolo mudou; use nova saída')
    atomic_json(output / 'identidade.json', identity)
    calls = Calls(output, config, transport=transport)
    records, history, failures = [], [], []
    quota = {t: config['questions_per_item']//6 + (i < config['questions_per_item'] % 6) for i,t in enumerate(C.TYPES)}

    def save(reason='em_andamento'):
        accepted = [r['questao'] for r in records if r['decisao']=='admitir']
        jsonl(output / 'aprovadas.jsonl', accepted)
        atomic_json(output / 'decisoes.json', records)
        counts = Counter(q['tipo'] for q in accepted)
        result = dict(schema=VERSION, item=item, grupo=group, documento_sha256=digest(document),
            meta=config['questions_per_item'], admitidas=len(accepted), candidatas=len(records),
            por_classe=dict(counts), cotas_planejadas=quota, motivo_parada=reason,
            status='concluido' if len(accepted)>=config['questions_per_item'] else 'em_andamento' if reason=='em_andamento' else 'parcial',
            tentativas=calls.budget.used, historico=history, erros=failures)
        atomic_json(output / 'resumo.json', result)
        return result

    async def evaluate(qs, targets, admitted, tag):
        if not qs: return []
        contexts = {q['id']: selected(targets[q['id']], blocks) for q in qs}
        solutions = await calls.call('solve', tag, dict(questoes=[dict(id=q['id'], pergunta=q['pergunta'], contexto=contexts[q['id']]) for q in qs]),
            lambda d: validate_solutions(d, {q['id'] for q in qs}), system=P.SOLVE)
        byid = {q['id']: q for q in qs}
        def check(data):
            C.judged(data, byid, blocks, {q['id'] for q in admitted})
            for row in data['avaliacoes']:
                allowed = {b['id'] for b in contexts[row['id']]}
                C.require(all(e['bloco'] in allowed for c in row['checagem_essenciais'] for e in c.get('evidencias',[])), 'Parecer deve citar o contexto desta pergunta')
        result = await calls.call('judge', tag, dict(candidatas=qs, alvos=[targets[q['id']] for q in qs],
            contextos_por_alvo=contexts, resolucoes=solutions['resolucoes'],
            inventario_admitido=[{k:q[k] for k in ('id','pergunta','resposta','conhecimento','tipo','composicao')} for q in admitted]),
            check, system=P.JUDGE)
        resolved = {r['id']:r for r in solutions['resolucoes']}
        return [dict(id=r['id'], decisao=r['decisao'], parecer=r, questao=byid[r['id']], resolucao=resolved[r['id']]) for r in result['avaliacoes']]

    def validate_authored(data, targets):
        C.authored(data, targets, blocks, len(targets))
        for q in data['questoes']:
            allowed = {b['id'] for b in selected(targets[q['id']], blocks)}
            C.require(all(e['bloco'] in allowed for c in q['criterios'] for e in c['evidencias']), 'Use somente o contexto deste alvo')

    def enrich(q, targets):
        target = targets[q['id']]
        context = selected(target, blocks)
        return dict(q, uid=f'{group}:{item}:{q["id"]}', item=item, grupo=group, origem=group,
            tipo=target['tipo'], composicao=target['composicao'], conhecimento=target['conhecimento'], ponte=target['ponte'],
            afirmacoes_alvo=target['afirmacoes'], documento_sha256=digest(document),
            blocos_contexto=context, contexto_tecnico='\n\n'.join(f"{b['capitulo']} / {b['subtitulo']}\n{b['texto']}" for b in context))

    reason = 'alvos_esgotados'
    try:
        plan = await calls.call('plan', 'alvos', dict(entrada=topic(item), documento=list(blocks.values()),
            limite=min(80, 2*config['questions_per_item']), cotas=quota, pendencias=list(pending)),
            lambda d: C.planned(d, blocks, min(80, 2*config['questions_per_item'])), system=P.PLAN)
        atomic_json(output / 'plano.json', plan)
        targets = plan['alvos']; stale = 0; remaining = list(targets); number = 0
        # Rodízio por classe; só se força a quantidade quando há alvo suportado.
        while remaining and number < config['max_batches']:
            admitted = [r['questao'] for r in records if r['decisao']=='admitir']
            if len(admitted)>=config['questions_per_item']: reason='meta'; break
            counts = Counter(q['tipo'] for q in admitted)
            remaining.sort(key=lambda t: (counts[t['tipo']]/max(1,quota[t['tipo']]), t['id']))
            size = min(config['batch_size'], config['questions_per_item']-len(admitted))
            chosen, remaining = remaining[:size], remaining[size:]; mapping = {t['id']:t for t in chosen}; number += 1
            path = output / 'lotes' / f'{number:03}.json'
            saved = read_json(path)
            if saved is None:
                decisions = []
                try:
                    contexts = {t['id']:selected(t, blocks) for t in chosen}
                    payload = dict(alvos=chosen, contextos_por_alvo=contexts, limite=len(chosen),
                        inventario=[dict(conhecimento=q['conhecimento'],pergunta=q['pergunta'],tipo=q['tipo']) for q in admitted],
                        exemplos_de_forma=list(examples)[:6])
                    authored = await calls.call('author', f'lote_{number}', payload,
                        lambda d:validate_authored(d,mapping), system=P.AUTHOR)
                    qs = [enrich(q,mapping) for q in authored['questoes']]
                    exact = {key(q['pergunta']) for q in admitted}; competence = {key(q['conhecimento'])+'|'+q['tipo'] for q in admitted}
                    unique, decisions = [], []
                    for q in qs:
                        qkey, ckey = key(q['pergunta']), key(q['conhecimento'])+'|'+q['tipo']
                        if qkey in exact or ckey in competence:
                            decisions.append(dict(id=q['id'],decisao='descartar',questao=q,motivo='Pergunta ou alvo normalizado repetido'))
                        else: unique.append(q); exact.add(qkey); competence.add(ckey)
                    decisions += await evaluate(unique,mapping,admitted,f'lote_{number}')
                    repair = {r['id']:r for r in decisions if r['decisao']=='corrigir'}
                    if repair:
                        fixed = await calls.call('refine', f'reparo_{number}', dict(alvos=[mapping[k] for k in repair],
                            contextos_por_alvo={k:contexts[k] for k in repair}, corrigir=list(repair.values()), limite=len(repair)),
                            lambda d:validate_authored(d,{k:mapping[k] for k in repair}), system=P.AUTHOR)
                        stable = admitted+[r['questao'] for r in decisions if r['decisao']=='admitir']
                        reviewed = await evaluate([enrich(q,mapping) for q in fixed['questoes']],mapping,stable,f'reparo_{number}')
                        updates = {r['id']:dict(r, historico=[repair[r['id']]], decisao='refino_esgotado' if r['decisao']=='corrigir' else r['decisao']) for r in reviewed}
                        for qid, r in repair.items():
                            if qid not in updates:updates[qid]=dict(r,decisao='refino_esgotado')
                        decisions = [updates.get(r['id'],r) for r in decisions]
                    saved = dict(records=decisions,impedimentos=authored['impedimentos'],alvos=list(mapping))
                except BaseException as exc:
                    # Uma falha no reparo não apaga candidatas já admitidas.
                    saved = dict(records=[dict(r,decisao='pendente') if r['decisao']=='corrigir' else r for r in decisions],
                        impedimentos=[str(exc)], alvos=list(mapping), falha=True)
                    if not isinstance(exc,CallFailure) or isinstance(exc,Fatal):
                        records.extend(saved['records']);reason='interrompido'
                        raise
                    failures.append(dict(lote=number,erro=str(exc)))
                if not saved.get('falha'):atomic_json(path,saved)
            admitted_keys = {key(r['questao']['pergunta']) for r in records if r['decisao']=='admitir'}
            for record in saved['records']:
                if record['decisao']=='admitir':
                    value=key(record['questao']['pergunta'])
                    if value in admitted_keys:record.update(decisao='descartar',motivo='Duplicata exata após refino')
                    else:admitted_keys.add(value)
            records.extend(saved['records'])
            gain = sum(r['decisao']=='admitir' for r in saved['records'])
            history.append(dict(lote=number,ganho=gain,alvos=saved['alvos'],impedimentos=saved['impedimentos']))
            stale = stale+1 if gain==0 else 0
            save()
            if saved.get('falha'):reason='falha_retomavel';break
            if stale>=config['patience']:reason='baixa_produtividade'; break
        if sum(r['decisao']=='admitir' for r in records)>=config['questions_per_item']: reason='meta'
        elif number>=config['max_batches']:reason='limite_lotes'
    except Exception as exc:
        reason='interrompido';failures.append(dict(erro=type(exc).__name__+': '+str(exc)))
    finally:
        result = save(reason)
        await calls.close()
    return result


def validate_solutions(data, ids):
    C.exact(data.get('resolucoes'),ids,'resolucoes')
    for r in data['resolucoes']:
        C.require(C.text(r.get('resposta')), 'Resposta independente obrigatória')
        C.strings(r.get('ambiguidades'),'ambiguidades')
