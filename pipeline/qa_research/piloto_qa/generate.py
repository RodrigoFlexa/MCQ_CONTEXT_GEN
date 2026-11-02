"""Evidência antes da pergunta; um reparo; inventário por competência."""
import json
import asyncio
from collections import Counter
from pathlib import Path
from pipeline.inventario.textutil import atomic_json, read_json
from pipeline.inventario.llm import BudgetExceeded
from pipeline.qa_research.v3.runtime import Calls, digest, topic, CallFailure, Fatal
from . import VERSION, contracts as C, prompts as P
from .documents import flatten
from .validation import question_key as key


def selected(target, blocks):
    ids = {e['bloco'] for a in target['afirmacoes'] for e in a['evidencias']}
    return [b for bid, b in blocks.items() if bid in ids]


def jsonl(path, rows):
    path = Path(path); path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_suffix('.tmp')
    temporary.write_text(''.join(json.dumps(q, ensure_ascii=False) + '\n' for q in rows), encoding='utf-8')
    temporary.replace(path)


async def generate(document, item, group, config, output, examples=(), pending=(), transport=None):
    """Compatibilidade do piloto fixo com a mesma unidade de decisão individual."""
    from .rounds import CandidateRound
    from .validation import indexed, resolve_evidence, source_with_passages
    output = Path(output); output.mkdir(parents=True, exist_ok=True)
    blocks = {b['id']: b for b in flatten(document)}
    identity = dict(schema=VERSION, documento=digest(document), item=item, grupo=group,
        config={k:v for k,v in config.items() if k not in ('workers','max_calls','heartbeat','verbose')},
        exemplos=list(examples), pendencias=list(pending),
        prompts={name:digest(getattr(P,name)) for name in ('PLAN','AUTHOR','SOLVE','JUDGE')},
        codigo={p.name:digest(p.read_text(encoding='utf-8')) for p in Path(__file__).parent.glob('*.py')})
    old = read_json(output/'identidade.json')
    C.require(old is None or old == identity, 'Documento/gerador/protocolo mudou; use nova saída')
    atomic_json(output/'identidade.json',identity)
    calls = Calls(output,config,transport=transport)
    records, active, history, failures = [], [], [], []
    quota = {t:config['questions_per_item']//6+(i<config['questions_per_item']%6) for i,t in enumerate(C.TYPES)}
    reason = 'alvos_esgotados'
    def save():
        all_records=records+active
        admitted=[r['questao'] for r in all_records if r['decisao']=='admitir']
        jsonl(output/'aprovadas.jsonl',admitted);atomic_json(output/'decisoes.json',all_records)
        result=dict(schema=VERSION,item=item,grupo=group,documento_sha256=digest(document),meta=config['questions_per_item'],
            admitidas=len(admitted),candidatas=len(all_records),por_classe=dict(Counter(q['tipo'] for q in admitted)),
            cotas_planejadas=quota,motivo_parada=reason,status='concluido' if len(admitted)>=config['questions_per_item'] else 'parcial',
            tentativas=calls.budget.used,historico=history,erros=failures,
            invalidas_contrato=sum(r['decisao']=='invalida_contrato' for r in all_records))
        atomic_json(output/'resumo.json',result);return result
    def progress(data):
        nonlocal active
        active=data['records'];save()
    def enrich(q,targets):
        target=targets[q['id']];context=selected(target,blocks)
        return dict(q,uid=f'{group}:{item}:{q["id"]}',item=item,grupo=group,origem=group,
            tipo=target['tipo'],composicao=target['composicao'],conhecimento=target['conhecimento'],ponte=target['ponte'],
            afirmacoes_alvo=target['afirmacoes'],documento_sha256=digest(document),blocos_contexto=context,
            contexto_tecnico='\n\n'.join(f"{b['capitulo']} / {b['subtitulo']}\n{b['texto']}" for b in context))
    try:
        raw=await calls.call('plan','alvos',dict(entrada=topic(item),documento=source_with_passages(list(blocks.values())),
            limite=min(80,2*config['questions_per_item']),cotas=quota,pendencias=list(pending)),C.envelope,system=P.PLAN)
        byid,errors=indexed(raw,'alvos');failures.extend(errors);targets=[]
        for qid,t in byid.items():
            try:
                C.require(isinstance(t,dict),'Alvo ausente ou duplicado')
                t=resolve_evidence(t,blocks);C.target(t,blocks)
            except (ValueError,KeyError,TypeError,AttributeError) as exc:
                failures.append(dict(id=qid,etapa='planejamento',erro=str(exc)))
            else: targets.append(t)
        plan=dict(alvos=targets,impedimentos=raw.get('impedimentos',[]))
        atomic_json(output/'plano.json',plan)
        remaining,number,stale=list(targets),0,0
        while remaining and number<config['max_batches']:
            admitted=[r['questao'] for r in records if r['decisao']=='admitir']
            if len(admitted)>=config['questions_per_item']:reason='meta';break
            counts=Counter(q['tipo'] for q in admitted)
            remaining.sort(key=lambda t:(counts[t['tipo']]/max(1,quota[t['tipo']]),t['id']))
            size=min(config['batch_size'],config['questions_per_item']-len(admitted))
            chosen,remaining=remaining[:size],remaining[size:];number+=1
            mapping={t['id']:t for t in chosen};contexts={t['id']:selected(t,blocks) for t in chosen}
            used={b['id'] for ctx in contexts.values() for b in ctx}
            source=[b for bid,b in blocks.items() if bid in used]
            processor=CandidateRound(calls,output/'lotes'/f'{number:03}.json',source,admitted,None,config,enrich,
                on_save=progress,contexts=lambda t:selected(t,blocks))
            progress(processor.data)
            payload=dict(alvos=chosen,contextos_por_alvo={qid:source_with_passages(ctx) for qid,ctx in contexts.items()},
                limite=len(chosen),inventario=[dict(conhecimento=q['conhecimento'],pergunta=q['pergunta'],tipo=q['tipo']) for q in admitted],
                exemplos_de_forma=list(examples)[:6])
            result=await processor.process(payload,f'lote_{number}',targets=mapping,system=P.AUTHOR)
            records.extend(result['records']);active=[]
            gain=sum(r['decisao']=='admitir' for r in result['records'])
            valid=any(r['decisao']!='invalida_contrato' for r in result['records'])
            history.append(dict(lote=number,ganho=gain,alvos=list(mapping),impedimentos=result['impedimentos'],rodada_valida=valid))
            stale=stale+1 if gain==0 and valid else 0
            save()
            if stale>=config['patience']:reason='baixa_produtividade';break
        if sum(r['decisao']=='admitir' for r in records)>=config['questions_per_item']:reason='meta'
        elif number>=config['max_batches']:reason='limite_lotes'
    except BudgetExceeded as exc:
        reason='suspenso_orcamento';failures.append(dict(erro=str(exc)))
    except (asyncio.CancelledError,KeyboardInterrupt) as exc:
        reason='interrompido';failures.append(dict(erro=type(exc).__name__+': checkpoints individuais preservados'))
        raise
    except CallFailure as exc:
        reason='interrompido' if isinstance(exc,Fatal) else 'falha_retomavel'
        failures.append(dict(erro=type(exc).__name__+': '+str(exc)))
    except Exception as exc:
        reason='interrompido';failures.append(dict(erro=type(exc).__name__+': '+str(exc)))
    finally:
        try:result=save()
        finally:await calls.close()
    return result


def validate_solutions(data, ids):
    C.exact(data.get('resolucoes'),ids,'resolucoes')
    for r in data['resolucoes']:
        C.require(C.text(r.get('resposta')), 'Resposta independente obrigatória')
        C.strings(r.get('ambiguidades'),'ambiguidades')
