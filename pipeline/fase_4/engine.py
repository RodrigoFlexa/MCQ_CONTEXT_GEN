"""QA v3: auditoria -> exploração -> QA -> qualidade/dificuldade/novidade -> persistência."""
from collections import Counter
import hashlib
from pathlib import Path

from .config import SCHEMA_VERSION
from .domain import DomainResources, TOPICOS, fingerprint
from .examples import ExamplePool, build_seed_bank, load_external, sample_external
from .metrics import MetricsIndex, DiagnosticBaselines, metric_decisions, saturation_signals
from .prompts_qa import SYSTEM_PROMPT, build_prompt
from .scoring import normalize_question,score_qa,refine_question,judge_questions
from .difficulty import evaluate_difficulty
from .redundancy import assess_redundancy,deduplicate_seeds
from .scheduling import CoverageScheduler
from .storage import RunStore,BudgetedClient,CallLimitReached,utc_now,atomic_json,write_jsonl

ROLES=('preparation','source_auditor','generator','refiner','judge','difficulty','redundancy')


def build_clients(cfg,store,backends=None):
    if backends is None:
        from azure_openai_backend import AzureOpenAIBackend
        deployments={r:cfg.preparation_deployment if r in ('preparation','source_auditor') else
                       cfg.judge_deployment if r in ('judge','difficulty','redundancy') else cfg.deployment for r in ROLES}
        backends={r:AzureOpenAIBackend(deployment=d,reasoning_effort=cfg.effort,api_style='reasoning',
                    max_tokens=12000,reasoning_min_tokens=12000,request_timeout=300,cache_enabled=False)
                  for r,d in deployments.items()}
    return {r:BudgetedClient(backends[r],r,store) for r in ROLES}


def payload(row):
    return {k:row[k] for k in ('id','question','answer','concept','target_id','evidence','topic','subtopic')}


def diagnose(question,context,cfg):
    result=score_qa(question,context['chunks'],cfg)
    if question.get('target_id') not in {t['target_id'] for t in context['generation_targets']}:
        result['reasons'].append('invalid_knowledge_target');result['needs_refinement']=True
    return result


def refine(row,diagnostic,stage,context,cfg,clients):
    if len(row['refinements'])>=cfg.max_refinements:return False
    refined,changes=refine_question(clients['refiner'],payload(row),diagnostic,context)
    version={'stage':stage,'attempt':len(row['refinements'])+1,'changes':changes}
    if refined is None:
        row['refinements'].append({**version,'unrepairable':True});return False
    refined['id']=row['id']
    score=diagnose(refined,context,cfg)
    row['refinements'].append({**version,'question':refined,'scorer':score})
    row.update(refined);row['scorer']=score
    return True


def process_batch(raw_items,context,difficulty,batch_id,quality_examples,external_examples,
                  cfg,store,clients,metrics,requested,diagnostic_baselines=None):
    processed=[];used_targets=set()
    for position,raw in enumerate(raw_items[:requested]):
        normalized=normalize_question(raw)
        row={'schema_version':SCHEMA_VERSION,'id':f'{batch_id}-q{position}','origin':'generated_qa_v3',
            'topic':context['topic'],'subtopic':context['subtopic'],'requested_difficulty':difficulty,
            'batch_id':batch_id,'doc_id':context['doc_id'],'facet_id':context['facet_id'],
            'facet_title':context['facet_title'],'focus':context['focus'],'source_chunks':context['chunks'],
            'source_audit':context['source_audit'],'document':context['document'],
            'source_embedding_diagnostics':context.get('embedding_diagnostics',{}),
            'corpus_signature':context['corpus_signature'],
            'quality_example_ids':[q['id'] for q in quality_examples],
            'format_example_ids':[q.get('id') for q in external_examples],
            'created_at':utc_now(),'original':raw,'refinements':[],'judge_history':[],
            'accepted':False,'quality_approved':False,'useful_novel':False,'novelty_measurable':False,
            'cosine_filter_enabled':cfg.enable_cosine_filter,'redundancy_filter_enabled':cfg.filter_redundancy}
        if normalized is None:
            row.update(question='',answer='',rejection_reason='invalid_qa_format',scorer=None,judge=None)
            processed.append(row);continue
        row.update(normalized)
        row_context={**context,'generation_targets':[t for t in context['generation_targets'] if t['target_id'] not in used_targets]}
        row['metrics_original']=metrics.measure(row)
        row['scorer']=row['scorer_original']=diagnose(row,row_context,cfg)
        while row['scorer']['needs_refinement'] and len(row['refinements'])<cfg.max_refinements:
            if not refine(row,row['scorer'],'scorer',row_context,cfg,clients):break
        if row['scorer']['needs_refinement']:
            row['rejection_reason']='unresolved_scorer:'+';'.join(row['scorer']['reasons'])
        else:used_targets.add(row['target_id'])
        processed.append(row)
    ready=[payload(r) for r in processed if r.get('scorer') and not r['scorer']['needs_refinement']]
    verdicts=judge_questions(clients['judge'],ready,context,cfg)
    for row in processed:
        verdict=verdicts.get(row['id'])
        if verdict:
            row['judge_history'].append(verdict)
            while verdict.get('repairable') and len(row['refinements'])<cfg.max_refinements:
                repair_context={**context,'generation_targets':[t for t in context['generation_targets'] if t['target_id']==row['target_id']]}
                if not refine(row,verdict,'judge',repair_context,cfg,clients):break
                if row['scorer']['needs_refinement']:break
                verdict=judge_questions(clients['judge'],[payload(row)],context,cfg)[row['id']]
                row['judge_history'].append(verdict)
        row['judge']=verdict
        row['refined']=bool(row['refinements'])
        if verdict:
            row['nota']=verdict.get('nota')
            row['quality_approved']=bool(verdict['approved'] and not row['scorer']['needs_refinement'])
            row['rejection_reason']=verdict['reason'] if not row['scorer']['needs_refinement'] else 'unresolved_scorer'
    evaluated=evaluate_difficulty(clients['difficulty'],[payload(r) for r in processed if r['quality_approved']])
    for row in processed:
        if not row['question']:
            store.commit(row);continue
        row['metrics']=metrics.measure(row)
        row['metrics_by_baseline']=diagnostic_baselines.measure(row) if diagnostic_baselines else {}
        row['counterfactual_decisions']=metric_decisions(row['metrics'],cfg.similarity_threshold)
        row['embedding_diagnostics']={k:metrics.emb.diagnostics(row['question'] if k=='question' else
                                         row['answer'] if k=='answer' else row['question']+'\n'+row['answer'])
                                      for k in ('question','answer','qa')}
        level=evaluated.get(row['id']);row['difficulty_evaluation']=level
        row['difficulty']=level.get('difficulty') if level else None
        approved=row['quality_approved']
        if approved and (not level or not level.get('valid')):
            approved=False;row['rejection_reason']='invalid_difficulty_evaluation'
        decision=assess_redundancy(clients['redundancy'],row,metrics,cfg) if approved else None
        row['redundancy']=decision
        if decision and not decision['valid']:
            approved=False;row['rejection_reason']='invalid_redundancy_evaluation'
        if decision and decision['redundant'] and cfg.filter_redundancy:
            approved=False;row['rejection_reason']='confirmed_redundancy'
        if approved and cfg.enable_cosine_filter and row['counterfactual_decisions']['configured_cosine_would_reject']:
            approved=False;row['rejection_reason']='cosine_filter_explicitly_enabled'
        row['useful_novel']=bool(approved and row['quality_approved'] and level and level.get('valid') and decision and
                                  decision['valid'] and decision.get('novelty_resolved',True) and not decision['redundant'])
        row['novelty_measurable']=bool(not row['scorer']['needs_refinement'] and row.get('judge') and row['judge'].get('valid') and
            (not row['quality_approved'] or (level and level.get('valid') and decision and decision['valid'] and
                                            decision.get('novelty_resolved',True))))
        row['accepted']=approved
        store.commit(row)
        if diagnostic_baselines:diagnostic_baselines.add(row)
        if approved and row['useful_novel']:metrics.add_many([row])
    return processed


def record_round(store,cfg,domain,topic,subtopic,number,requested,difficulty,batch_id,rows,before,
                 selection=None,error=None):
    current=domain.entropy(store.accepted,topic)
    previous=[r for r in store.rounds if r['topic']==topic]
    scores=[r['metrics']['cosine'] for r in rows if r.get('metrics') and r['metrics']['cosine'] is not None]
    row={'topic':topic,'subtopic':subtopic,'round':number,'batch_id':batch_id,'requested_difficulty':difficulty,
        'requested':requested,'generated':len(rows),'accepted_this_round':sum(r['accepted'] for r in rows),
        'accepted_total':sum(r['topic']==topic for r in store.accepted),
        'acceptance_rate':sum(r['accepted'] for r in rows)/max(1,len(rows)),
        'useful_novel_this_round':sum(r.get('useful_novel',False) for r in rows),
        'entropy':current,'entropy_subtopic':domain.entropy(store.accepted,topic,subtopic),
        'entropy_useful_novel':domain.entropy([r for r in store.records if r.get('useful_novel')],topic),
        'entropy_gain':round(current['value']-before['value'],6) if current['value'] is not None and before['value'] is not None else None,
        'new_clusters':current['clusters_visited']-before['clusters_visited'],'entropy_reliable':current['reliable'],
        'mean_cosine':sum(scores)/len(scores) if scores else None,'selection':selection,
        'doc_id':selection.get('doc_id') if selection else None,'facet_id':selection.get('facet_id') if selection else None,
        'error':error,'at':utc_now(),'cosine_filter_enabled':cfg.enable_cosine_filter,
        'saturation_stop_enabled':cfg.enable_saturation_stop}
    row['entropy_diagnostics_legacy']=saturation_signals(previous,row,cfg)
    row['stopping']=CoverageScheduler(cfg,domain,store).refresh(topic)
    row['saturation_diagnostics']={**row['entropy_diagnostics_legacy'],
                                 'configured_saturation_would_stop':row['stopping']['would_stop']}
    store.log_round(row)
    return row


def execute(cfg,*,backends=None,domain=None,seeds=None,external=None):
    cfg.validate();selected=cfg.topics or list(TOPICOS)
    if set(selected)-set(TOPICOS):raise ValueError('Tópicos desconhecidos')
    store=RunStore(cfg);summaries={}
    try:
        names=('prompts_qa','source_audit','difficulty','scoring','redundancy','embedding','scheduling','stopping','engine','examples','metrics','domain','config','storage','multi_corpus')
        files=[Path(__file__).with_name(n+'.py') for n in names]
        files += [Path(__file__).parents[1]/'fase_3'/name for name in ('utils_fase3.py','prompts_fase3.py','topicos.py','seed_fase3.py')]
        files += [Path(__file__).parents[1]/'qa_references/download_qa_examples.py']
        files += sorted((Path(__file__).parents[1]/'domain_corpora').glob('*.py'))
        signature=fingerprint({str(p.relative_to(Path(__file__).parents[2])):hashlib.sha256(p.read_bytes()).hexdigest() for p in files})
        if store.meta.get('prompt_signature') and store.meta['prompt_signature']!=signature:
            raise ValueError('Implementação/prompts mudaram; use nova saída')
        store.meta['prompt_signature']=signature
        if not cfg.prepare_only:
            external=load_external(cfg.external_examples) if external is None else external
            seeds=build_seed_bank(cfg) if seeds is None else seeds
            signatures={'seeds':fingerprint(seeds),'external':fingerprint(external)}
            if store.meta.get('example_signatures') and store.meta['example_signatures']!=signatures:
                raise ValueError('Bancos de exemplos mudaram; use nova saída')
            store.meta['example_signatures']=signatures
            write_jsonl(store.root/'external_examples_used.jsonl',external)
        store.status('preparing')
        clients=build_clients(cfg,store,backends)
        domain=DomainResources(cfg,clients['preparation'],clients['source_auditor']).prepare(selected) if domain is None else domain
        store.meta.update(corpus_signature=domain.signature,domain_required=True,quality_roles=list(ROLES),
                          embedding_protocol=getattr(domain.emb,'protocol',{}))
        if cfg.prepare_only:store.status('prepared');return store
        if not seeds or not external:raise ValueError('Exemplos humanos e externos QA são obrigatórios')
        seeds=deduplicate_seeds(seeds,clients['redundancy'],domain.emb,cfg,store)
        write_jsonl(store.root/'banco_seed_qa.jsonl',seeds)
        metrics=MetricsIndex(domain.emb,[*seeds,*[r for r in store.accepted if r.get('useful_novel')]])
        diagnostic_baselines=DiagnosticBaselines(domain.emb,seeds,store.records)
        pool=ExamplePool(cfg,seeds,store.accepted);scheduler=CoverageScheduler(cfg,domain,store)
        store.status('generating');errors=0
        for topic in selected:
            covered=domain.covered_subtopics(topic)
            if not covered:
                summaries[topic]={'topic':topic,'accepted':0,'stop_reason':'no_audited_domain_evidence'}
                atomic_json(store.root/'resumo_topicos.json',list(summaries.values()));continue
            reason=None
            while sum(r['topic']==topic for r in store.accepted)<cfg.limit_per_topic:
                state=store.state['topics'].get(topic,{'rounds':0,'requested_candidates':0})
                attempts=cfg.max_attempts_per_topic-state['requested_candidates']
                if attempts<=0:reason='max_attempts';break
                if store.state['api_calls']>=cfg.max_calls:reason='max_calls';break
                context,difficulty,selection,status=scheduler.choose(topic)
                if cfg.enable_saturation_stop and status['would_stop']:reason=status['reason'];break
                remaining=cfg.limit_per_topic-sum(r['topic']==topic for r in store.accepted)
                quota_remaining=selection['subtopic_quota']-selection['subtopic_accepted']
                requested=min(cfg.batch_size,remaining,attempts,len(context['generation_targets']),max(1,quota_remaining))
                number=store.reserve_round(topic,requested)
                batch_id=f"qa-v3-{hashlib.sha256(topic.encode()).hexdigest()[:12]}-r{number}"
                subtopic=context['subtopic'];before=domain.entropy(store.accepted,topic)
                store.event('selection',{'batch_id':batch_id,**selection})
                try:
                    examples=pool.sample_quality(topic,number)
                    formats=sample_external(external,cfg.format_examples,f'{cfg.seed}:{batch_id}')
                    prior=[r for r in store.accepted if r['topic']==topic]
                    prompt=build_prompt(topic=topic,subtopic=subtopic,scope=context['scope'],focus=context['focus'],
                        document=context['document'],chunks=context['chunks'],difficulty=difficulty,
                        quality_examples=examples,format_examples=formats,previous_questions=[r['question'] for r in prior],
                        used_concepts=[r.get('concept','') for r in prior],count=requested,batch_id=batch_id,
                        source_audit=context['source_audit'],generation_targets=context['generation_targets'])
                    result=clients['generator'].complete_json(prompt,system=SYSTEM_PROMPT,max_tokens=12000)
                    items=result.get('items') if isinstance(result,dict) else None
                    if not isinstance(items,list):raise ValueError('O gerador não retornou items')
                    store.event('generated_batch',{'batch_id':batch_id,'doc_id':context['doc_id'],'raw_items':items,'requested':requested})
                    rows=process_batch(items,context,difficulty,batch_id,examples,formats,cfg,store,clients,metrics,requested,diagnostic_baselines)
                    report=record_round(store,cfg,domain,topic,subtopic,number,requested,difficulty,batch_id,rows,before,selection)
                    errors=0;domain.emb.salvar_cache();store.status('generating')
                    print(f"[{subtopic}] rodada={number} aprovadas={report['accepted_total']}/{cfg.limit_per_topic} "
                          f"novas={report['useful_novel_this_round']} H={report['entropy']['value']}",flush=True)
                except CallLimitReached:
                    partial=[r for r in store.records if r['batch_id']==batch_id]
                    record_round(store,cfg,domain,topic,subtopic,number,requested,difficulty,batch_id,partial,before,selection,'CallLimitReached')
                    reason='max_calls';break
                except Exception as exc:
                    errors+=1
                    store.event('round_error',{'topic':topic,'batch_id':batch_id,'error_type':type(exc).__name__,'error':str(exc)[:500]})
                    partial=[r for r in store.records if r['batch_id']==batch_id]
                    record_round(store,cfg,domain,topic,subtopic,number,requested,difficulty,batch_id,partial,before,selection,type(exc).__name__)
                    if errors>=cfg.max_consecutive_api_failures:raise RuntimeError('Limite de falhas consecutivas; checkpoint preservado') from exc
            accepted=[r for r in store.accepted if r['topic']==topic]
            summaries[topic]={'topic':topic,'accepted':len(accepted),'useful_novel':sum(r.get('useful_novel',False) for r in accepted),
                'stop_reason':reason or 'max_accepted','entropy':domain.entropy(store.accepted,topic),
                'by_subtopic':dict(Counter(r['subtopic'] for r in accepted)),
                'difficulty_inferred':dict(Counter(r['difficulty'] for r in accepted)),
                'difficulty_requested':dict(Counter(r['requested_difficulty'] for r in accepted)),
                'difficulty_by_subtopic':{s:dict(Counter(r['difficulty'] for r in accepted if r['subtopic']==s)) for s in covered},
                'stopping':scheduler.refresh(topic),'uncovered_subtopics':[s for s in TOPICOS[topic] if s not in covered],
                'requested_candidates':store.state['topics'].get(topic,{}).get('requested_candidates',0)}
            atomic_json(store.root/'resumo_topicos.json',list(summaries.values()))
            if reason=='max_calls':break
        write_jsonl(store.root/'resumo_topicos.jsonl',list(summaries.values()))
        write_jsonl(store.root/'pares_qa.jsonl',[{'question':r['question'],'answer':r['answer']} for r in store.accepted])
        write_jsonl(store.root/'seeds_especialista_e_geradas.jsonl',[*seeds,*store.accepted])
        domain.emb.salvar_cache()
        store.status('completed' if len(summaries)==len(selected) and all(r['accepted']>=cfg.limit_per_topic for r in summaries.values()) else 'finished_with_limits')
        return store
    except CallLimitReached:
        store.status('finished_with_limits');store.event('api_budget',{'stage_detail':'preparation_or_audit'});return store
    except BaseException:
        store.status('interrupted');raise
