"""Geração contínua: contexto, candidatos, vizinhos, auditoria e memória."""
from collections import Counter
from pathlib import Path
from pipeline.inventario.textutil import atomic_json,read_json
from pipeline.inventario.llm import BudgetExceeded
from pipeline.qa_research.v3.runtime import Calls,digest,topic
from . import contracts as C,prompts as P,prompts_fluxo as F
from .contextos import packages
from .generate import jsonl,key,validate_solutions


def memory(bank,package,similarity,limit):
    recent=[q for q in bank if q.get('pacote')==package['id'] and q.get('item')==package.get('item')][-min(5,limit):]
    nearest=similarity.nearest(package['nome'],bank,limit)
    result=[];seen=set()
    for q in recent+nearest:
        if q['id'] not in seen:result.append(q['pergunta']);seen.add(q['id'])
        if len(result)>=limit:break
    return result


def priorities(bank,item,round_number):
    counts=Counter(q['tipo'] for q in bank if q.get('item')==item and q.get('nova'))
    rotation=list(C.TYPES);offset=(round_number-1)%len(rotation)
    rotation=rotation[offset:]+rotation[:offset]
    return sorted(rotation,key=lambda t:counts[t])


async def generate(document,item,group,config,output,bank,similarity,examples=(),pending=(),transport=None):
    output=Path(output);output.mkdir(parents=True,exist_ok=True)
    contexts=[dict(p,item=item) for p in packages(document,config['context_chars'])]
    identity=dict(schema='qa-continuo-1',documento=digest(document),banco=digest(bank),
        config={k:v for k,v in config.items() if k not in ('max_calls','heartbeat','workers')},
        item=item,grupo=group,exemplos=list(examples),pendencias=list(pending),semantica=similarity.protocol,
        prompts={k:digest(v) for k,v in dict(gerar=F.GENERATE,auditar=F.AUDIT,refinar=P.AUTHOR,resolver=P.SOLVE).items()},
        codigo={p.name:digest(p.read_text(encoding='utf-8')) for p in Path(__file__).parent.glob('*.py')})
    old=read_json(output/'identidade.json');C.require(old is None or old==identity,'Fluxo/entradas mudaram; use nova saída')
    atomic_json(output/'identidade.json',identity);atomic_json(output/'contextos.json',contexts)
    state=read_json(output/'estado.json') or dict(rodada=0,proximo=0,vazias={p['id']:0 for p in contexts},records=[],historico=[])
    calls=Calls(output,config,transport=transport);unfinished=[];reason='em_andamento';error=None

    def accepted():return [r['questao'] for r in state['records'] if r['decisao']=='admitir']
    def save():
        admitted=accepted()+[r['questao'] for r in unfinished if r['decisao']=='admitir']
        jsonl(output/'aprovadas.jsonl',admitted)
        atomic_json(output/'decisoes.json',state['records']+unfinished)
        report=dict(schema='qa-continuo-1',item=item,grupo=group,status='concluido' if reason=='contextos_sem_ganho' else 'parcial',
            motivo_parada=reason,erro=error,admitidas=len(admitted),candidatas=len(state['records'])+len(unfinished),
            por_classe=dict(Counter(q['tipo'] for q in admitted)),tentativas=calls.budget.used,
            contextos=[dict(id=p['id'],nome=p['nome'],tipo=p['tipo'],rodadas_sem_ganho=state['vazias'][p['id']]) for p in contexts],
            historico=state['historico'],nota='Baixa produtividade observada; não certifica esgotamento conceitual.')
        atomic_json(output/'resumo.json',report);return report

    async def review(qs,targets,source,inventory,tag):
        if not qs:return []
        solutions=await calls.call('solve',tag,dict(questoes=[dict(id=q['id'],pergunta=q['pergunta'],contexto=source) for q in qs]),
            lambda d:validate_solutions(d,{q['id'] for q in qs}),system=P.SOLVE)
        neighbors={}
        for q in qs:
            for n in similarity.nearest(q['pergunta'],inventory,config['neighbors']):neighbors[n['id']]=n
        small=[{k:q[k] for k in ('id','pergunta','resposta','conhecimento','tipo','composicao') if k in q} for q in neighbors.values()]
        mapping={q['id']:q for q in qs};blocks={b['id']:b for b in source}
        judged=await calls.call('judge',tag,dict(candidatas=[compact(q) for q in qs],alvos=[targets[q['id']] for q in qs],
            contextos_por_alvo={q['id']:source for q in qs},resolucoes=solutions['resolucoes'],inventario_admitido=small),
            lambda d:C.judged(d,mapping,blocks,set(neighbors)),system=F.AUDIT)
        solved={r['id']:r for r in solutions['resolucoes']}
        return [dict(id=r['id'],decisao=r['decisao'],parecer=r,questao=mapping[r['id']],resolucao=solved[r['id']],
            vizinhos=[dict(id=n['id'],similaridade=n['similaridade']) for n in similarity.nearest(mapping[r['id']]['pergunta'],inventory,config['neighbors'])])
            for r in judged['avaliacoes']]

    def compact(q):
        return {k:v for k,v in q.items() if k not in ('blocos_contexto','contexto_tecnico')}

    try:
        while True:
            active=[i for i,p in enumerate(contexts) if state['vazias'][p['id']]<config['patience']]
            if not active:reason='contextos_sem_ganho';break
            i=next((j for j in active if j>=state['proximo']),active[0]);package=contexts[i];source=package['blocos']
            number=state['rodada']+1;prefix=f'{item}_{number:06}_';tag=f'{package["id"]}_rodada_{number}'
            blocks={b['id']:b for b in source};inventory=bank+accepted()
            path=output/'rodadas'/f'{number:06}_inicial.json';initial=read_json(path)
            print(f'[contexto {package["id"]}] {package["nome"]} | rodada {number} | aprovadas {len(accepted())}',flush=True)
            def check(data):
                C.planned(data,blocks,config['batch_size']);targets={t['id']:t for t in data['alvos']}
                C.authored(data,targets,blocks,config['batch_size'])
                C.require(set(targets)=={q['id'] for q in data['questoes']},'Cada candidata exige um alvo correspondente')
                C.require(all(qid.startswith(prefix) for qid in targets),'Use prefixo de IDs recebido')
            def enrich(q,targets):
                t=targets[q['id']]
                return dict(q,uid=f'{group}:{item}:{q["id"]}',item=item,grupo=group,origem=group,nova=True,
                    tipo=t['tipo'],composicao=t['composicao'],conhecimento=t['conhecimento'],ponte=t['ponte'],
                    afirmacoes_alvo=t['afirmacoes'],documento_sha256=digest(document),pacote=package['id'],
                    blocos_contexto=source,contexto_tecnico='\n\n'.join(f"{b['capitulo']} / {b['subtitulo']}\n{b['texto']}" for b in source))
            if initial is None:
                payload=dict(entrada=topic(item),contexto=package,rodada=number,prefixo=prefix,limite=config['batch_size'],
                    prioridades_tipos=priorities(inventory,item,number),memoria=memory(inventory,package,similarity,config['memory_limit']),
                    exemplos_de_forma=list(examples),pendencias=list(pending))
                data=await calls.call('author',tag,payload,check,system=F.GENERATE)
                targets={t['id']:t for t in data['alvos']};qs=[enrich(q,targets) for q in data['questoes']]
                exact={key(q['pergunta']) for q in inventory};unique=[];records=[]
                for q in qs:
                    value=key(q['pergunta'])
                    if value in exact:records.append(dict(id=q['id'],decisao='descartar',questao=q,motivo='Duplicata exata normalizada'))
                    else:unique.append(q);exact.add(value)
                records+=await review(unique,targets,source,inventory,tag)
                initial=dict(records=records,alvos=targets,impedimentos=data['impedimentos'])
                atomic_json(path,initial)
            unfinished=initial['records'];targets=initial['alvos'];save()
            repair={r['id']:r for r in unfinished if r['decisao']=='corrigir'}
            if repair:
                def fixed_check(data):C.authored(data,{k:targets[k] for k in repair},blocks,len(repair))
                fixed=await calls.call('refine',tag,dict(alvos=[targets[k] for k in repair],
                    contextos_por_alvo={k:source for k in repair},
                    corrigir=[dict(r,questao=compact(r['questao'])) for r in repair.values()],limite=len(repair)),fixed_check,system=P.AUTHOR)
                stable=inventory+[r['questao'] for r in unfinished if r['decisao']=='admitir']
                revised=await review([enrich(q,targets) for q in fixed['questoes']],targets,source,stable,tag+'_reparo')
                updates={r['id']:dict(r,historico=[repair[r['id']]],decisao='refino_esgotado' if r['decisao']=='corrigir' else r['decisao']) for r in revised}
                unfinished=[updates.get(r['id'],dict(r,decisao='refino_esgotado') if r['id'] in repair else r) for r in unfinished]
            exact={key(q['pergunta']) for q in inventory}
            for r in unfinished:
                if r['decisao']=='admitir':
                    value=key(r['questao']['pergunta'])
                    if value in exact:r.update(decisao='descartar',motivo='Duplicata exata após refino')
                    else:exact.add(value)
            gain=sum(r['decisao']=='admitir' for r in unfinished)
            state['records']+=unfinished;unfinished=[];state['rodada']=number;state['proximo']=(i+1)%len(contexts)
            state['vazias'][package['id']]=0 if gain else state['vazias'][package['id']]+1
            state['historico'].append(dict(rodada=number,contexto=package['id'],ganho=gain,impedimentos=initial['impedimentos']))
            atomic_json(output/'estado.json',state);save()
    except BudgetExceeded as exc:reason='suspenso_orcamento';error=str(exc)
    except Exception as exc:reason='falha_retomavel';error=type(exc).__name__+': '+str(exc)
    finally:
        result=save();await calls.close()
    return result
