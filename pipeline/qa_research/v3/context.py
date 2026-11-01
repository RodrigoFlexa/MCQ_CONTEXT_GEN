"""Buscar, redigir seções, revisar o conjunto e corrigir uma vez."""
import asyncio
import json
import re
from pathlib import Path

from pipeline.inventario.llm import BudgetExceeded
from pipeline.inventario.textutil import atomic_json
from pipeline.qa_research.corpus import CorpusIndex
from pipeline.qa_research.v2.language import lint_ptbr
from . import contracts as C, prompts as P
from .runtime import digest, CallFailure, Fatal
from .retrieval import prompt_source, research, qa_ready, REVISION


def input_size(payload, prompt):
    return len(json.dumps(payload,ensure_ascii=False))+len(prompt)


def outline(sections):
    return [{k:s[k] for k in ('id','titulo','pontos')} for s in sections]


def fit_write(payload, config):
    """Ajusta a seleção por tamanho serializado, sem cortar passagens ou o escopo."""
    limit=config['max_input_chars'];before=input_size(payload,P.WRITE)
    detail=dict(caracteres_antes=before,limite=limit,fontes_antes=len(payload['fontes']),
        componentes={k:len(json.dumps(v,ensure_ascii=False)) for k,v in payload.items()},excluidas=[])
    if before<=limit:
        return payload,dict(detail,ajustado=False,caracteres_depois=before,fontes_enviadas=len(payload['fontes']))
    compact=dict(payload,sumario=outline(payload['sumario']),
        secao={k:payload['secao'][k] for k in ('id','titulo','pontos')})
    compact['fontes']=[prompt_source(s) for s in payload['fontes']]
    if input_size(compact,P.WRITE)>limit:
        selected=[]
        # Reserva espaço para o texto gerado poder ser auditado junto às evidências.
        target=int(limit*.7)
        for source in compact['fontes']:
            candidate=dict(compact,fontes=selected+[source])
            if input_size(candidate,P.WRITE)<=target:selected.append(source)
            else:detail['excluidas'].append(dict(id=source['id'],motivo='passagem integral não cabe no orçamento da seção',caracteres=len(source['texto'])))
        compact['fontes']=selected
    size=input_size(compact,P.WRITE)
    detail.update(ajustado=True,caracteres_depois=size,fontes_enviadas=len(compact['fontes']))
    if size>limit:
        detail['erro']='Escopo, sumário e orientações excedem o orçamento mesmo sem fontes'
    elif payload['fontes'] and not compact['fontes']:
        detail['erro']='Nenhuma passagem integral cabe no pacote; revise a extração ou o orçamento'
    return compact,detail


def clean_headings(body, section_title, document_title):
    """Hierarquia de apresentação; não modifica o conteúdo técnico."""
    lines=body.strip().splitlines()
    if lines and re.sub(r'^#+\s*','',lines[0]).strip() in (section_title,document_title):lines=lines[1:]
    levels=[len(m[1]) for line in lines if (m:=re.match(r'^(#{1,6})\s+',line))]
    shift=max(0,3-min(levels)) if levels else 0
    return '\n'.join(re.sub(r'^(#{1,6})(?=\s)',lambda m:'#'*min(6,len(m[1])+shift),line) for line in lines).strip()


def editor_issues(section):
    body=section['texto'];issues=lint_ptbr(body)
    if re.search(r'https?://|\bE[a-f0-9]{20}\b|\b(?:o trecho|a fonte afirma|nos ensaios relatados|referências? (?:consultadas?|disponíveis)|(?:as? fontes?|as? referências?) (?:apontam|indicam|afirmam)|conforme a referência)\b',body,re.I):
        issues.append('Referências e relato de fonte devem ficar nos auxiliares; redija conhecimento autônomo')
    return issues


async def generate(entrada, manifest, config, calls, root, corpus_identity):
    semantic={k:config[k] for k in ('sections','sources_per_section','max_per_document','retrieval_candidates','section_words')}
    version=digest([entrada,corpus_identity,semantic,{k:config['models'][k] for k in ('plan','write','review')},
        P.PLAN,P.SELECT,P.WRITE,P.REVIEW,C.VERSION,REVISION,Path(__file__).with_name('retrieval.py').read_text(encoding='utf-8'),Path(__file__).read_text(encoding='utf-8')])[:20]
    work=Path(root)/'versoes'/version
    plan=await calls.call('plan','plano',dict(entrada=entrada,quantidade_secoes=config['sections']),lambda d:C.plan(d,entrada))
    atomic_json(work/'plano.json',plan)
    index=CorpusIndex(calls.output/'.local'/'corpus',manifest=manifest)
    print('[busca] verificando e construindo o índice local',flush=True)
    info=await asyncio.to_thread(index.build)
    pools={};traces=[];selections={};errors=[]

    async def search_section(section, previous=(), pairs=None, complement=True):
        sid=section['id']
        sources,detail=await research(index,section,entrada,plan['pontos'],config,calls,
            retained=previous,pairs=pairs,complement=complement)
        selections[sid+('' if complement else '_correcao')]=detail
        traces.extend(dict(secao=sid,etapa='inicial' if complement else 'correcao',**t) for t in detail['consultas'])
        atomic_json(work/'buscas.json',traces)
        atomic_json(work/'selecao.json',selections)
        return sources

    async def write_one(section, previous=None, report=None):
        sid=section['id']
        try:
            sources=pools.get(sid,[])
            if previous is None:
                sources=await search_section(section)
            elif report and report['consultas']:
                used=set(previous['fontes'])
                sources=await search_section(section,[s for s in sources if s['id'] in used],report['consultas'],False)
            pools[sid]=sources
            C.require(sources,sid+': nenhuma evidência diretamente pertinente; seção pendente de pesquisa')
            payload=dict(entrada=entrada,sumario=plan['secoes'],secao=section,fontes=sources,
                palavras_alvo=config['section_words'])
            if previous:payload.update(anterior=previous,parecer=report)
            payload,sizing=fit_write(payload,config)
            atomic_json(work/'entradas'/(sid+('_correcao' if previous else '')+'.json'),sizing)
            C.require(not sizing.get('erro'),sid+': '+sizing.get('erro',''))
            if sizing['ajustado']:
                print(f'[contexto:{sid}] pacote ajustado: {sizing["fontes_enviadas"]} passagens integrais para redação; detalhes no relatório de entrada',flush=True)
            direct={s['id'] for s in payload['fontes'] if s.get('pertinencia')=='direta'}
            C.require(direct,sid+': nenhuma evidência direta coube no pacote de redação')
            def validate_written(data):
                C.section(data,{s['id'] for s in payload['fontes']})
                C.require(direct.intersection(data['fontes']),sid+': a seção precisa usar evidência direta, não somente apoio genérico')
            result=await calls.call('write',sid+('_correcao' if previous else ''),payload,
                validate_written)
            result=dict(id=sid,titulo=section['titulo'],**{k:result[k] for k in ('texto','fontes','complementos','lacunas')})
            result['texto']=clean_headings(result['texto'],section['titulo'],entrada['titulo'])
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
        payload=dict(entrada=entrada,checklist=plan['pontos'],sumario=plan['secoes'],
            secoes_enviadas=sections,fontes=[] if coherence else [source_map[k] for k in sorted(used)],
            modo='coerencia_final' if coherence else 'tecnica_completa')
        if input_size(payload,P.REVIEW)>config['max_input_chars']:
            payload.update(sumario=outline(plan['secoes']),fontes=[prompt_source(s) for s in payload['fontes']])
        return payload

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
            issues=editor_issues(s)+['Lacuna técnica declarada: '+gap for gap in s.get('lacunas',[])]
            if issues and not decisions[sid].get('operacional'):
                old=decisions[sid]
                decisions[sid]=dict(old,decisao='corrigir',motivo=old['motivo']+'; pendências locais',
                    correcao='; '.join(filter(None,[old['correcao'],*issues])))
        result=dict(secoes=list(decisions.values()),cobertura=list(coverage.values()),omissoes_escopo=sorted(set(omissions)))
        atomic_json(work/('revisao_'+suffix+'.json'),result)
        return result

    current=await write_many(plan['secoes'])
    review=await review_all(current,'inicial') if current else dict(secoes=[],cobertura=[dict(id=p['id'],estado='ausente',secoes=[],motivo='Sem evidência pertinente ou redação concluída') for p in plan['pontos']],omissoes_escopo=[])
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
        state=p['estado'] if kept==p['secoes'] and kept else 'parcial' if kept else 'ausente'
        coverage.append(dict(p,secoes=kept,estado=state,motivo=p['motivo'] if state==p['estado'] else
            'Cobertura reduzida: seção de suporte não foi liberada. Parecer anterior: '+p['motivo']))
    missing=[p['id'] for p in plan['pontos'] if p['prioritario'] and not any(c['id']==p['id'] and c['estado']=='atendido' for c in coverage)]
    doc=dict(titulo=entrada['titulo'],secoes=[dict(titulo=s['titulo'],texto=s['texto']) for s in sections])
    report=dict(status='concluido' if all(p['estado']=='atendido' for p in coverage) and not review['omissoes_escopo'] and len(sections)==len(plan['secoes']) else 'parcial',
        versao=version,secoes_liberadas=len(sections),secoes_planejadas=len(plan['secoes']),pontos=plan['pontos'],
        cobertura=coverage,prioritarios_pendentes=missing,omissoes_escopo=review['omissoes_escopo'],erros=errors,
        criterio_qualidade=REVISION,corpus=info,corpus_manifest=corpus_identity,entrada=digest(entrada),
        documento_sha256=digest(doc),aprovacao='revisão automática; validação pelo especialista pendente')
    report['qa_elegivel']=qa_ready(report)
    metadata={sid:[{k:v for k,v in s.items() if k!='texto'} for s in pool] for sid,pool in pools.items()}
    atomic_json(calls.output/'.local'/'evidencias'/(version+'.json'),pools)
    atomic_json(work/'rastreabilidade.json',dict(secoes=sections,fontes=metadata))
    atomic_json(work/'cobertura.json',report);atomic_json(Path(root)/'cobertura.json',report)
    atomic_json(Path(root)/'documento.json',doc)
    lines=['# '+doc['titulo']]
    for s in doc['secoes']:lines+=['','## '+s['titulo'],'',s['texto']]
    (Path(root)/'documento.md').write_text('\n'.join(lines)+'\n',encoding='utf-8')
    return sections,report
