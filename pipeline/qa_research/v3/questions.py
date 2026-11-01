"""Lotes de autoria, resolução sem gabarito e revisão com refino seletivo."""
import csv
import io
import re
from collections import Counter
from pathlib import Path

from pipeline.inventario.textutil import atomic_json, read_json
from pipeline.qa_research.v2.language import lint_ptbr
from . import contracts as C, prompts as P
from .runtime import digest


def normalized(s):return ' '.join(s.split())


def compact(q):
    return {k:q[k] for k in ('id','tipo','composicao','pergunta','resposta','conhecimento','pontos')}


def form_issues(q):
    issues=lint_ptbr(q['pergunta']+' '+q['resposta'])
    if len(q['pergunta'].split())>90 or len(q['resposta'].split())>30:issues.append('Enunciado até 90 palavras; resposta até 30')
    if q['tipo'] in ('diagnostico','decisao') and not q['cenario']:issues.append('Diagnóstico e decisão exigem cenário')
    if q['tipo']=='conceito' and (q['cenario'] or q['composicao']=='composta'):issues.append('Conceito deve ser direto e simples')
    if re.search(r'\b(segundo o texto|no documento|nos blocos|o trecho)\b',q['pergunta']+' '+q['resposta'],re.I):issues.append('Questão precisa ser autônoma, sem referência ao documento')
    return issues


def save_results(root, records, report):
    root=Path(root);root.mkdir(parents=True,exist_ok=True)
    admitted=[r['questao'] for r in records if r['decisao']=='admitir']
    atomic_json(root/'admitidas.json',admitted)
    atomic_json(root/'decisoes.json',records)
    atomic_json(root/'cobertura.json',report)
    stream=io.StringIO(newline='');writer=csv.DictWriter(stream,fieldnames=['id','tipo','composicao','pergunta','resposta'])
    writer.writeheader();writer.writerows({k:q[k] for k in writer.fieldnames} for q in admitted)
    temp=root/'qa.csv.tmp';temp.write_text(stream.getvalue(),encoding='utf-8-sig');temp.replace(root/'qa.csv')


def stats(records, points):
    admitted=[r['questao'] for r in records if r['decisao']=='admitir']
    covered={p for q in admitted for p in q['pontos']}
    return dict(admitidas=len(admitted),avaliadas=len(records),por_classe={t:sum(q['tipo']==t for q in admitted) for t in C.TYPES},
        por_composicao={t:sum(q['composicao']==t for q in admitted) for t in ('simples','composta')},
        pontos_com_questao=sorted(covered),pontos_sem_questao=sorted(set(points)-covered))


async def evaluate(questions, sections, admitted, calls, tag, points, entrada, originals=None):
    known={q['id']:q for q in questions}
    used={e['secao'] for q in questions for e in q['fundamentos']}
    context=[sections[s] for s in sections if s in used]
    solutions=await calls.call('solve',tag,dict(questoes=[dict(id=q['id'],pergunta=q['pergunta']) for q in questions],contexto=context),
        lambda d:C.solutions(d,known))
    review=await calls.call('judge',tag,dict(candidatas=questions,resolucoes=solutions['resolucoes'],contexto=context,entrada=entrada,pontos=points,
        admitidas=[compact(q) for q in admitted],originais=originals or {}),
        lambda d:C.judged(d,known,{q['id'] for q in admitted}))
    resolutions={r['id']:r for r in solutions['resolucoes']}
    result=[]
    for r in review['avaliacoes']:
        q=known[r['id']];issues=form_issues(q)
        if issues and r['decisao']=='admitir':r=dict(r,decisao='corrigir',motivo='; '.join(issues))
        result.append(dict(id=q['id'],questao=q,decisao=r['decisao'],parecer=r,resolucao=resolutions[q['id']]))
    # Se uma referência de duplicata perdeu a admissão pela checagem local, preserve a candidata para correção.
    decisions={r['id']:r['decisao'] for r in result}
    for r in result:
        target=r['parecer'].get('duplicada_de')
        if target in decisions and decisions[target]!='admitir':
            r.update(decisao='corrigir',parecer=dict(r['parecer'],decisao='corrigir',motivo='Reavaliar duplicação: a referência não foi admitida'))
    return result


async def batch(entrada, selected, points, admitted, previous, examples, config, calls, number, limit):
    bysection={s['id']:s for s in selected}
    payload=dict(entrada=entrada,contexto=selected,pontos=points,admitidas=[compact(q) for q in admitted],
        tentativas_anteriores=previous,exemplos=examples[:6],limite=limit)
    authored=await calls.call('author',f'lote_{number:02}',payload,
        lambda d:C.authored(d,bysection,{p['id'] for p in points},limit))
    qs=[dict(q,id=f'L{number:02}_Q{i:03}') for i,q in enumerate(authored['questoes'],1)]
    exact={normalized(q['pergunta']):q['id'] for q in admitted};unique=[];records=[]
    for q in qs:
        key=normalized(q['pergunta'])
        if key in exact:
            records.append(dict(id=q['id'],questao=q,decisao='descartar',motivo='Pergunta textualmente duplicada',duplicada_de=exact[key]))
        else:unique.append(q);exact[key]=q['id']
    if not unique:return records,authored['impedimentos']
    records.extend(await evaluate(unique,bysection,admitted,calls,f'lote_{number:02}',points,entrada))
    recoverable={r['id']:r for r in records if r['decisao']=='corrigir'}
    if recoverable:
        originals={k:v['questao'] for k,v in recoverable.items()}
        result=await calls.call('refine',f'lote_{number:02}',dict(contexto=selected,
            corrigir=list(recoverable.values()),admitidas=[compact(q) for q in admitted]+[compact(r['questao']) for r in records if r['decisao']=='admitir']),
            lambda d:C.refined(d,originals,bysection,{p['id'] for p in points}))
        fixed=[];replacement={}
        for item in result['itens']:
            if item['decisao']=='corrigida':fixed.append(item['questao'])
            else:replacement[item['id']]=dict(recoverable[item['id']],decisao=item['decisao'],refino=item,historico=[recoverable[item['id']]])
        if fixed:
            stable=admitted+[r['questao'] for r in records if r['decisao']=='admitir']
            reviewed=await evaluate(fixed,bysection,stable,calls,f'lote_{number:02}_refino',points,entrada,originals)
            for r in reviewed:
                if r['decisao']=='corrigir':r['decisao']='refino_esgotado'
                replacement[r['id']]=dict(r,historico=[recoverable[r['id']]])
        records=[replacement.get(r['id'],r) for r in records]
    return records,authored['impedimentos']


async def generate(entrada, sections, doc_report, examples, config, calls, root):
    semantic={k:config[k] for k in ('batch_size','max_batches','min_questions','patience')}
    version=digest([sections,doc_report['pontos'],doc_report['cobertura'],examples,semantic,{k:config['models'][k] for k in ('author','solve','judge','refine')},
        P.AUTHOR,P.SOLVE,P.JUDGE,P.REFINE,C.VERSION,Path(__file__).read_text(encoding='utf-8')])[:20]
    work=Path(root)/'versoes'/version
    visits=Counter();records=[];history=[];stale=0;reason='limite_lotes'
    eligible={p['id'] for p in doc_report['cobertura'] if p['estado'] in ('atendido','parcial')}
    points=[p for p in doc_report['pontos'] if p['id'] in eligible]
    C.require(points,'Nenhum ponto do escopo coberto por seção liberada')
    checkpoint=read_json(Path(root)/'cobertura.json') or {}
    if checkpoint.get('versao')!=version:
        save_results(root,[],dict(stats([],eligible),status='em_andamento',versao=version,
            documento_sha256=doc_report['documento_sha256'],historico=[]))
    priorities={p['id'] for p in points if p['prioritario']}
    # Ordenação estável e rodízio garantem que todas as seções recebam oportunidade.
    for number in range(1,config['max_batches']+1):
        admitted=[r['questao'] for r in records if r['decisao']=='admitir']
        covered={p for q in admitted for p in q['pontos']}
        mapping={s['id']:set() for s in sections}
        for p in doc_report['cobertura']:
            for sid in p['secoes']:
                if sid in mapping:mapping[sid].add(p['id'])
        chosen=sorted(sections,key=lambda s:(visits[s['id']],-len(mapping[s['id']]&priorities-covered),s['id']))[:2]
        previous=[dict(conhecimento=r['questao']['conhecimento'],tipo=r['questao']['tipo'],decisao=r['decisao']) for r in records]
        path=work/f'lote_{number:02}.json'
        saved=read_json(path)
        if saved is None:
            limit=config['batch_size']
            # Reduz o lote se a entrada já estiver próxima do teto; nunca trunca contexto/inventário.
            base=dict(entrada=entrada,contexto=chosen,pontos=points,admitidas=[compact(q) for q in admitted],tentativas_anteriores=previous,exemplos=examples[:6],limite=limit)
            import json
            if len(json.dumps(base,ensure_ascii=False))>config['max_input_chars']*.8:limit=max(1,limit//2)
            items,impediments=await batch(entrada,chosen,points,admitted,previous,examples,config,calls,number,limit)
            saved=dict(records=items,impedimentos=impediments,secoes=[s['id'] for s in chosen])
            atomic_json(path,saved)
        records.extend(saved['records']);visits.update(saved['secoes'])
        after=stats(records,eligible);gain=after['admitidas']-len(admitted)
        stale=stale+1 if gain==0 else 0
        history.append(dict(lote=number,ganho=gain,secoes=saved['secoes'],impedimentos=saved['impedimentos']))
        report=dict(after,status='em_andamento',historico=history,versao=version,documento_sha256=doc_report['documento_sha256'])
        save_results(root,records,report)
        print(f'[questoes] lote {number}/{config["max_batches"]} | {after["admitidas"]} admitidas | ganho {gain}',flush=True)
        if after['admitidas']>=config['min_questions'] and priorities<=set(after['pontos_com_questao']):
            reason='meta_e_cobertura';break
        if len(visits)==len(sections) and stale>=config['patience']:
            reason='saturacao';break
    report=dict(stats(records,eligible),status='concluido' if reason=='meta_e_cobertura' else 'parcial',
        motivo_parada=reason,historico=history,versao=version,meta=config['min_questions'],documento_sha256=doc_report['documento_sha256'],
        pontos_prioritarios_sem_questao=sorted(priorities-set(stats(records,eligible)['pontos_com_questao'])),
        nota='Aprovação automática; revisão pelo especialista pendente. Cobertura relativa aos pontos liberados.')
    save_results(root,records,report);atomic_json(work/'cobertura.json',report)
    return report
