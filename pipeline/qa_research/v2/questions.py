"""QA guiada por unidades/alvos, resolução cega, auditoria e refino encaminhado."""
import csv
import json
from pathlib import Path

from pipeline.inventario.textutil import atomic_json
from pipeline.qa_research.tipos import problemas_tipo
from pipeline.inventario.llm import ContentFiltered, CallFailed
from .common import TYPES, require, text, unique, ids, exact_rows, approved, digest, jaccard
from .context import flatten
from . import prompts as P

UNIT_CRITERIA=('fiel','atomica','condicoes_preservadas','alvos_sustentados')
QA_CRITERIA=('sustentada','correta','determinada','autonoma','sem_pistas','alvo_preservado','classe_confere','composicao_confere')
ROUTES=('aprovar','reescrever','replanejar','lacuna_documental','descartar')


def validate_units(data,blocks,maximum):
    rows=data.get('unidades');unique(rows);require(len(rows)<=maximum,'Excesso de unidades por lote')
    for u in rows:
        require(text(u.get('conhecimento')) and isinstance(u.get('condicoes'),list),'Unidade incompleta')
        require(isinstance(u.get('evidencias'),list) and bool(u['evidencias']),'Unidade sem evidência')
        for e in u['evidencias']:
            require(e.get('bloco') in blocks and text(e.get('trecho')) and
                e['trecho'] in blocks[e['bloco']]['texto'],'Fundamento não é passagem literal do bloco')
        require(isinstance(u.get('alvos'),list) and bool(u['alvos']),'Unidade sem alvo avaliável')
        require(len({a.get('tipo') for a in u['alvos']})==len(u['alvos']),'Classes repetidas na unidade')
        for a in u['alvos']: require(a.get('tipo') in TYPES and text(a.get('alvo')),'Alvo inválido')


def validate_unit_audit(data,units,previous):
    rows=data.get('avaliacoes');exact_rows(rows,[u['id'] for u in units])
    known={u['id'] for u in units+previous}
    edges={}
    for r in rows:
        require(all(type(r.get(k)) is bool for k in ('aprovada',*UNIT_CRITERIA)) and text(r.get('motivo')),'Auditoria de unidade inválida')
        duplicate=r.get('duplicada_de')
        require(duplicate is None or duplicate in known-{r['id']},'Duplicata inexistente')
        require(not r['aprovada'] or all(r[c] for c in UNIT_CRITERIA),'Aprovação contradiz critérios')
        if duplicate: edges[r['id']]=duplicate
    for start in edges:
        seen=set();current=start
        while current in edges:
            require(current not in seen,'Ciclo de duplicatas');seen.add(current);current=edges[current]


def inventory(blocks,output,config,calls):
    admitted,all_units=[],[]
    for start in range(0,len(blocks),config['unit_batch_blocks']):
        batch=blocks[start:start+config['unit_batch_blocks']];byid={b['id']:b for b in batch}
        d=calls.call('units',P.EXTRACT,dict(blocos=batch,max_unidades=config['max_units_per_batch']),
            lambda d:validate_units(d,byid,config['max_units_per_batch']))
        units=[{**u,'id':f'L{start:04}_'+u['id']} for u in d['unidades']]
        if not units: continue
        audit=calls.call('unit_audit',P.AUDIT_UNITS,dict(unidades=units,blocos=batch,unidades_anteriores=admitted),
            lambda d:validate_unit_audit(d,units,admitted))
        for u,r in zip(units,sorted(audit['avaliacoes'],key=lambda r:[u['id'] for u in units].index(r['id']))):
            row={**u,'auditoria':r,'elegivel':approved(r,UNIT_CRITERIA) and r.get('duplicada_de') is None}
            all_units.append(row)
            if row['elegivel']: admitted.append(row)
    atomic_json(Path(output)/'unidades.json',all_units)
    return admitted,all_units


def validate_targets(data,units,limit):
    rows=data.get('alvos');unique(rows);require(len(rows)<=limit,'Excesso de alvos')
    for t in rows:
        require(t.get('tipo') in TYPES and t.get('composicao') in ('simples','composta'),'Classificação inválida')
        ids(t.get('unidades'),units)
        n=len(t['unidades'])
        require((n==1 and t['composicao']=='simples') or
            (2<=n<=3 and t['composicao']=='composta' and t['tipo']!='conceito' and text(t.get('ponte'))),'Composição não corresponde às unidades')
        require(text(t.get('alvo')) and text(t.get('resposta_esperada')),'Alvo sem demanda ou resposta')
        if n==1:
            allowed={a['tipo'] for a in units[t['unidades'][0]]['alvos']}
            require(t['tipo'] in allowed,'Classe não sustentada na unidade auditada')
    require(isinstance(data.get('impedimentos'),list),'Impedimentos devem ser lista')
    for r in data['impedimentos']:
        ids(r.get('unidades'),units);require(text(r.get('motivo')),'Impedimento sem motivo')


def validate_candidate(d,target,refine=False):
    statuses=('ok','insuficiente','replanejar','lacuna_documental','descartar') if refine else ('ok','insuficiente')
    require(d.get('status') in statuses and isinstance(d.get('motivo'),str),'Status de candidata inválido')
    require(d.get('tipo')==target['tipo'] and d.get('composicao')==target['composicao'],'Mudança de alvo/classe exige replanejamento explícito')
    if d['status']!='ok': require(text(d['motivo']),'Saída não aprovada precisa de motivo');return
    require(text(d.get('pergunta')) and text(d.get('resposta')) and type(d.get('cenario')) is bool,'Candidata incompleta')
    require(len(d['pergunta'].split())<=90 and len(d['resposta'].split())<=50,'Enunciado/gabarito excede limite')
    # Mesmo filtro de forma já utilizado no projeto; gabarito atual limitado a 30 palavras.
    issues=problemas_tipo(d['tipo'],d['cenario'],d['pergunta'],d['resposta'])
    require(not issues,'; '.join(issues))


def validate_solution(d):
    require(text(d.get('resposta')),'Resolução vazia')
    for k in ('ambiguidades','concorrentes'):
        require(isinstance(d.get(k),list) and all(text(v) for v in d[k]),'Resolução sem listas de ambiguidades/concorrentes')


def validate_qa_audit(d):
    require(all(type(d.get(k)) is bool for k in ('aprovada',*QA_CRITERIA)),'Critérios booleanos ausentes')
    require(text(d.get('motivo')) and d.get('encaminhamento') in ROUTES,'Encaminhamento inválido')
    require(d['aprovada']==(all(d[k] for k in QA_CRITERIA) and d['encaminhamento']=='aprovar'),
            'Aprovação contradiz critérios/encaminhamento')
    require(d['aprovada'] or d['encaminhamento']!='aprovar','Reprovada com encaminhamento aprovar')


def support(target,units,blocks):
    used={e['bloco'] for u in target['unidades'] for e in units[u]['evidencias']}
    return [blocks[k] for k in sorted(used)]


def validate_dedup(d,existing):
    require('duplicada_de' in d and (d['duplicada_de'] is None or d['duplicada_de'] in {q['id'] for q in existing})
            and text(d.get('motivo')),'Deduplicação inválida')


def generate_one(target,units,blocks,existing,examples,config,calls):
    context=support(target,units,blocks)
    ex=[e for e in examples if e['tipo'] in (target['tipo'],None)][:config['examples_per_call']]
    author_input=dict(alvo=target,unidades=[units[u] for u in target['unidades']],blocos=context,
        exemplos=ex,ja_cobertas=[dict(id=q['id'],pergunta=q['pergunta'],resposta=q['resposta']) for q in existing])
    candidate=calls.call('qa_author',P.AUTHOR,author_input,lambda d:validate_candidate(d,target))
    history=[]
    for attempt in range(config['refine_attempts']+1):
        if candidate['status']!='ok':
            return dict(alvo=target,status=candidate['status'],historico=history,candidata=candidate)
        # Nunca enviar alvo, gabarito, exemplos ou histórico ao resolvedor.
        solution=calls.call('qa_solver',P.SOLVE,dict(pergunta=candidate['pergunta'],blocos=context),validate_solution)
        review=calls.call('qa_audit',P.AUDIT_QA,dict(alvo=target,candidata=candidate,resolucao=solution,
            blocos=context,ja_cobertas=author_input['ja_cobertas']),validate_qa_audit)
        history.append(dict(tentativa=attempt,candidata=candidate,resolucao=solution,auditoria=review))
        if approved(review,QA_CRITERIA):
            duplicate=None
            # Todos os aprovados são comparados em lotes; nenhuma decisão depende de cosine universal.
            for start in range(0,len(existing),config['dedup_batch']):
                group=existing[start:start+config['dedup_batch']]
                d=calls.call('dedup',P.DEDUP,dict(candidata=candidate,alvo=target,
                    aprovadas=[dict(id=q['id'],alvo=q['alvo'],pergunta=q['pergunta'],resposta=q['resposta']) for q in group]),
                    lambda d:validate_dedup(d,group))
                if d['duplicada_de']: duplicate=d;break
            if duplicate:
                return dict(alvo=target,status='redundante',historico=history,deduplicacao=duplicate)
            return dict(id=target['id'],alvo=target,status='aprovada_modelo',historico=history,
                **{k:candidate[k] for k in ('tipo','composicao','cenario','pergunta','resposta')})
        route=review['encaminhamento']
        if route!='reescrever' or attempt==config['refine_attempts']:
            return dict(alvo=target,status=route if route!='reescrever' else 'tentativas_esgotadas',historico=history)
        revised=calls.call('qa_refine',P.REFINE,dict(**author_input,original=candidate,parecer=review,historico=history),
                           lambda d:validate_candidate(d,target,refine=True))
        if revised['status']=='ok' and jaccard(candidate['pergunta'],revised['pergunta'])>=.95 and candidate['resposta']==revised['resposta']:
            return dict(alvo=target,status='mudanca_cosmetica',historico=history,candidata=revised)
        candidate=revised


def statistics(units,records):
    approved_q=[q for q in records if q['status']=='aprovada_modelo']
    covered={u for q in approved_q for u in q['alvo']['unidades']}
    demands={(u,q['tipo']) for q in approved_q for u in q['alvo']['unidades']}
    eligible={(u['id'],a['tipo']) for u in units for a in u['alvos']}
    return dict(unidades_elegiveis=len(units),unidades_cobertas=len(covered),
        cobertura_unidades=len(covered)/max(1,len(units)),
        demandas_elegiveis=len(eligible),demandas_cobertas=len(demands&eligible),
        cobertura_demandas=len(demands&eligible)/max(1,len(eligible)),
        por_tipo={t:sum(q['tipo']==t for q in approved_q) for t in TYPES},
        por_composicao={c:sum(q['composicao']==c for q in approved_q) for c in ('simples','composta')},
        aprovadas=len(approved_q),avaliadas=len(records),
        uncovered=[dict(unidade=u,tipo=t) for u,t in sorted(eligible-demands)])


def write_results(output,records,report):
    output=Path(output);output.mkdir(parents=True,exist_ok=True)
    good=[q for q in records if q['status']=='aprovada_modelo']
    for filename,rows in (('aprovadas.jsonl',good),('nao_aprovadas.jsonl',[q for q in records if q not in good])):
        path=output/filename
        tmp=path.with_suffix('.tmp');tmp.write_text(''.join(json.dumps(q,ensure_ascii=False)+'\n' for q in rows),encoding='utf-8');tmp.replace(path)
    with (output/'qa.csv').open('w',encoding='utf-8-sig',newline='') as out:
        w=csv.DictWriter(out,fieldnames=['id','tipo','composicao','pergunta','resposta']);w.writeheader()
        w.writerows({k:q[k] for k in w.fieldnames} for q in good)
    atomic_json(output/'cobertura.json',report)


def generate(document,output,config,calls,examples=()):
    output=Path(output);output.mkdir(parents=True,exist_ok=True)
    blocks=flatten(document);byblock={b['id']:b for b in blocks}
    units,all_units=inventory(blocks,output,config,calls);byunit={u['id']:u for u in units}
    records,planned,history,impediments=[],[],[],[];stale=0;reason='limite_rodadas'
    report=statistics(units,records)
    if not units:
        reason='sem_unidades_elegiveis'
    else:
        for round_no in range(1,config['qa_rounds']+1):
            before=statistics(units,records);existing=[q for q in records if q['status']=='aprovada_modelo']
            left=config['max_targets']-len(planned)
            if left<=0: reason='limite_alvos';break
            payload=dict(unidades=units,blocos=blocks,planejados=planned,
                resultados=[dict(alvo=q['alvo'],status=q['status'],parecer=q.get('historico',[])[-1:] ) for q in records],
                cobertura=before,impedimentos_anteriores=impediments,limite=min(config['targets_per_round'],left))
            d=calls.call('qa_plan',P.TARGETS,payload,lambda d:validate_targets(d,byunit,payload['limite']))
            atomic_json(output/f'planejamento_{round_no:02}.json',d)
            impediments.extend(d['impedimentos'])
            new=[]
            for target in d['alvos']:
                if any(target['tipo']==t['tipo'] and set(target['unidades'])==set(t['unidades']) and
                       jaccard(target['alvo'],t['alvo'])>=.8 for t in planned): continue
                target={**target,'id':f'R{round_no:02}_'+target['id']}
                planned.append(target);new.append(target)
            for target in new:
                try:
                    q=generate_one(target,byunit,byblock,existing,examples,config,calls)
                except ContentFiltered:
                    q=dict(alvo=target,status='filtro_conteudo',historico=[])
                except CallFailed as exc:
                    q=dict(alvo=target,status='falha_execucao',historico=[],erro=str(exc)[:600])
                records.append(q)
                if q['status']=='aprovada_modelo':existing.append(q)
                atomic_json(output/'alvos'/(target['id']+'.json'),q)
                write_results(output,records,dict(statistics(units,records),status='em_andamento'))
                print(f'[QA] {len(records)} alvos | {len(existing)} aprovadas',flush=True)
            after=statistics(units,records);gain=after['aprovadas']-before['aprovadas']
            stale=stale+1 if gain<config['min_new_questions'] else 0
            history.append(dict(rodada=round_no,novos_alvos=len(new),ganho=gain,**after))
            report=after
            # Cobertura de unidades sozinha não encerra a geração; exige demandas/classes.
            if (after['cobertura_unidades']>=config['unit_coverage'] and
                after['cobertura_demandas']>=config['demand_coverage'] and
                after['aprovadas']>=config['min_questions']): reason='cobertura_suficiente';break
            if not new: reason='sem_novos_alvos_sustentados';break
            if stale>=config['qa_patience']: reason='ganho_marginal_insuficiente';break
    pending=[q['alvo']['id'] for q in records if q['status']=='falha_execucao']
    report=dict(report,motivo_parada=reason,historico=history,unidades_extraidas=len(all_units),
        pendencias_execucao=pending,
        metas_experimentais=True,status='concluido' if reason=='cobertura_suficiente' and not pending else 'parcial',
        nota='Aprovação automática; cobertura relativa ao inventário extraído, não ao domínio inteiro')
    write_results(output,records,report)
    atomic_json(output/'lacunas_documentais.json',[q for q in records if q['status']=='lacuna_documental'])
    return report
