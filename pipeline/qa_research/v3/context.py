"""Buscar, redigir seções, revisar o conjunto e corrigir uma vez."""
import asyncio
import json
import re
from pathlib import Path

from pipeline.inventario.llm import BudgetExceeded
from pipeline.inventario.textutil import atomic_json
from pipeline.qa_research.corpus import CorpusIndex
from pipeline.qa_research.v2.language import bilingual_search, lint_ptbr
from . import contracts as C, prompts as P
from .runtime import digest, CallFailure, Fatal


def retrieve(index, pairs, config, retained=()):
    hits,traces=bilingual_search(index,pairs,config['retrieval_candidates'])
    selected=list(retained); counts={}
    for row in selected:counts[row.get('document_id')]=counts.get(row.get('document_id'),0)+1
    for row in hits:
        sid='E'+digest([row['chunk_id'],row['content_hash']])[:20]
        if any(s['id']==sid for s in selected):continue
        document=row.get('document_id')
        if counts.get(document,0)>=config['max_per_document']:continue
        if len(selected)>=config['sources_per_section']:break
        selected.append(dict(id=sid,texto=row['texto'],collection=row.get('collection'),
            document_id=document,chunk_id=row['chunk_id'],language=row.get('language'),
            title=row.get('title'),url=row.get('url'),page_ini=row.get('page_ini'),
            page_fim=row.get('page_fim'),source_boundary=row.get('source_boundary')))
        counts[document]=counts.get(document,0)+1
    return selected,traces


def editor_issues(section):
    body=section['texto'];issues=lint_ptbr(body)
    if re.search(r'https?://|\bE[a-f0-9]{20}\b|\b(?:o trecho|a fonte afirma|nos ensaios relatados)\b',body,re.I):
        issues.append('Referências e relato de fonte devem ficar nos auxiliares; redija conhecimento autônomo')
    return issues


async def generate(entrada, manifest, config, calls, root, corpus_identity):
    semantic={k:config[k] for k in ('sections','sources_per_section','max_per_document','retrieval_candidates','section_words')}
    version=digest([entrada,corpus_identity,semantic,{k:config['models'][k] for k in ('plan','write','review')},
        P.PLAN,P.WRITE,P.REVIEW,C.VERSION,Path(__file__).read_text(encoding='utf-8')])[:20]
    work=Path(root)/'versoes'/version
    plan=await calls.call('plan','plano',dict(entrada=entrada,quantidade_secoes=config['sections']),lambda d:C.plan(d,entrada))
    atomic_json(work/'plano.json',plan)
    index=CorpusIndex(calls.output/'.local'/'corpus',manifest=manifest)
    print('[busca] verificando e construindo o índice local',flush=True)
    info=await asyncio.to_thread(index.build)
    pools={};traces=[]
    for section in plan['secoes']:
        sources,queries=retrieve(index,section['consultas'],config)
        pools[section['id']]=sources;traces.extend(dict(secao=section['id'],**t) for t in queries)
    C.require(any(pools.values()),'Nenhuma passagem recuperada; confira o corpus e as consultas antes de redigir')
    atomic_json(work/'buscas.json',traces)
    atomic_json(calls.output/'.local'/'evidencias'/(version+'.json'),pools)
    errors=[]

    async def write_one(section, previous=None, report=None):
        sid=section['id'];sources=pools[sid]
        if report and report['consultas']:
            used={s for s in previous['fontes']}
            sources,_=retrieve(index,report['consultas'],config,retained=[s for s in sources if s['id'] in used])
            pools[sid]=sources
        payload=dict(entrada=entrada,sumario=plan['secoes'],secao=section,fontes=sources,
            palavras_alvo=config['section_words'])
        if previous:payload.update(anterior=previous,parecer=report)
        try:
            result=await calls.call('write',sid+('_correcao' if previous else ''),payload,
                lambda d:C.section(d,{s['id'] for s in sources}))
            result=dict(id=sid,**{k:result[k] for k in ('titulo','texto','fontes','complementos')})
            atomic_json(work/'secoes'/(sid+('_corrigida' if previous else '_inicial')+'.json'),result)
            return result
        except (Fatal,BudgetExceeded):raise
        except (CallFailure,ValueError) as exc:
            errors.append(dict(secao=sid,etapa='correcao' if previous else 'redacao',erro=str(exc)))
            print(f'[contexto:{sid}] pendente: {exc}',flush=True)
            return None

    async def write_many(sections, previous=None, reviews=None):
        tasks=[asyncio.create_task(write_one(s,(previous or {}).get(s['id']),(reviews or {}).get(s['id']))) for s in sections]
        try:
            values=await asyncio.gather(*tasks,return_exceptions=True)
            for value in values:
                if isinstance(value,BaseException):raise value
            return {r['id']:r for r in values if r is not None}
        finally:
            for task in tasks:
                if not task.done():task.cancel()
            await asyncio.gather(*tasks,return_exceptions=True)

    def review_payload(sections, coherence=False):
        source_map={s['id']:s for sources in pools.values() for s in sources}
        used={f for s in sections for f in s['fontes']}
        return dict(entrada=entrada,checklist=plan['pontos'],sumario=plan['secoes'],
            secoes_enviadas=sections,fontes=[] if coherence else [source_map[k] for k in sorted(used)],
            modo='coerencia_final' if coherence else 'tecnica_completa')

    async def review_all(current, suffix):
        groups=[]
        def divide(sections):
            payload=review_payload(sections)
            if len(json.dumps(payload,ensure_ascii=False))+len(P.REVIEW)<=config['max_input_chars']:
                groups.append(sections)
            elif len(sections)>1:
                middle=len(sections)//2;divide(sections[:middle]);divide(sections[middle:])
            else:groups.append(sections)  # O limite é diagnosticado pela chamada, sem cortar fontes.
        divide(list(current.values()))
        reports=[];decisions={};coverage={p['id']:dict(id=p['id'],estado='ausente',secoes=[],motivo='Sem revisão concluída') for p in plan['pontos']}
        omissions=[]
        async def one(sections, name, coherence=False):
            expected=[s['id'] for s in sections]
            try:
                result=await calls.call('review',name,review_payload(sections,coherence),lambda d:C.review(d,expected,coverage))
                reports.append(result)
                return result
            except (Fatal,BudgetExceeded):raise
            except (CallFailure,ValueError) as exc:
                errors.append(dict(etapa='revisao',secoes=expected,erro=str(exc)))
                return dict(secoes=[dict(id=s,decisao='corrigir',motivo='Revisão não concluída',correcao='Retomar revisão',consultas=[],operacional=True) for s in expected],cobertura=[],omissoes_escopo=[])
        for gi,group in enumerate(groups,1):
            result=await one(group,f'revisao_{suffix}_{gi}')
            decisions.update((r['id'],r) for r in result['secoes'])
            omissions.extend(result['omissoes_escopo'])
            order={'ausente':0,'parcial':1,'atendido':2}
            for p in result['cobertura']:
                old=coverage[p['id']]
                if order[p['estado']]>order[old['estado']]:coverage[p['id']]=p
                elif p['estado']==old['estado']:
                    old['secoes']=sorted(set(old['secoes'])|set(p['secoes']))
        if len(groups)>1:
            coherent=await one(list(current.values()),'coerencia_'+suffix,True)
            for r in coherent['secoes']:
                if r['decisao']=='corrigir':decisions[r['id']]=r
            coverage.update((p['id'],p) for p in coherent['cobertura'])
            omissions.extend(coherent['omissoes_escopo'])
        for sid,s in current.items():
            issues=editor_issues(s)
            if issues and not decisions[sid].get('operacional'):
                decisions[sid]=dict(id=sid,decisao='corrigir',motivo='Revisão editorial local',
                    correcao='; '.join(issues),consultas=[])
        result=dict(secoes=list(decisions.values()),cobertura=list(coverage.values()),omissoes_escopo=sorted(set(omissions)))
        atomic_json(work/('revisao_'+suffix+'.json'),result)
        return result

    current=await write_many(plan['secoes'])
    C.require(current,'Nenhuma seção redigida; consulte chamadas_llm.jsonl e retome')
    review=await review_all(current,'inicial')
    needed={r['id']:r for r in review['secoes'] if r['decisao']=='corrigir' and not r.get('operacional')}
    if needed:
        fixed=await write_many([s for s in plan['secoes'] if s['id'] in needed],current,needed)
        # Uma correção que falha não deixa o rascunho conhecido como problemático ser liberado.
        current={k:v for k,v in current.items() if k not in needed};current.update(fixed)
        if current:review=await review_all(current,'final')
    released={r['id'] for r in review['secoes'] if r['decisao']=='liberar'} & set(current)
    sections=[current[s['id']] for s in plan['secoes'] if s['id'] in released]
    coverage=[]
    for p in review['cobertura']:
        kept=[s for s in p['secoes'] if s in released]
        coverage.append(dict(p,secoes=kept,estado=p['estado'] if kept==p['secoes'] and kept else 'parcial' if kept else 'ausente'))
    missing=[p['id'] for p in plan['pontos'] if p['prioritario'] and not any(c['id']==p['id'] and c['estado']=='atendido' for c in coverage)]
    doc=dict(titulo=entrada['titulo'],secoes=[dict(titulo=s['titulo'],texto=s['texto']) for s in sections])
    report=dict(status='concluido' if not missing and not review['omissoes_escopo'] and len(sections)==len(plan['secoes']) else 'parcial',
        versao=version,secoes_liberadas=len(sections),secoes_planejadas=len(plan['secoes']),pontos=plan['pontos'],
        cobertura=coverage,prioritarios_pendentes=missing,omissoes_escopo=review['omissoes_escopo'],erros=errors,
        qa_elegivel=bool(sections),corpus=info,corpus_manifest=corpus_identity,entrada=digest(entrada),
        documento_sha256=digest(doc),aprovacao='revisão automática; validação pelo especialista pendente')
    metadata={sid:[{k:v for k,v in s.items() if k!='texto'} for s in pool] for sid,pool in pools.items()}
    atomic_json(calls.output/'.local'/'evidencias'/(version+'.json'),pools)
    atomic_json(work/'rastreabilidade.json',dict(secoes=sections,fontes=metadata))
    atomic_json(work/'cobertura.json',report);atomic_json(Path(root)/'cobertura.json',report)
    atomic_json(Path(root)/'documento.json',doc)
    lines=['# '+doc['titulo']]
    for s in doc['secoes']:lines+=['','## '+s['titulo'],'',s['texto']]
    (Path(root)/'documento.md').write_text('\n'.join(lines)+'\n',encoding='utf-8')
    return sections,report
