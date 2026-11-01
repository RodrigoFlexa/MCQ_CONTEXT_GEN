"""Buscar, redigir seções, revisar o conjunto e corrigir uma vez."""
import asyncio
import json
from pathlib import Path

from pipeline.inventario.llm import BudgetExceeded
from pipeline.inventario.textutil import atomic_json
from pipeline.qa_research.corpus import CorpusIndex
from . import contracts as C, prompts as P
from .runtime import digest, CallFailure, Fatal
from .retrieval import prompt_source, research, qa_ready, REVISION
from .review import review_all, input_size, outline, clean_headings, editor_issues


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


async def generate(entrada, manifest, config, calls, root, corpus_identity):
    semantic={k:config[k] for k in ('sections','sources_per_section','max_per_document','retrieval_candidates','selection_candidates','max_support_sources','section_words')}
    version=digest([entrada,corpus_identity,semantic,{k:config['models'][k] for k in ('plan','write','review')},
        P.PLAN,P.SELECT,P.WRITE,P.REVIEW,C.VERSION,REVISION,Path(__file__).with_name('retrieval.py').read_text(encoding='utf-8'),Path(__file__).with_name('review.py').read_text(encoding='utf-8'),Path(__file__).read_text(encoding='utf-8')])[:20]
    work=Path(root)/'versoes'/version
    plan=await calls.call('plan','plano',dict(entrada=entrada,quantidade_secoes=config['sections']),lambda d:C.plan(d,entrada))
    atomic_json(work/'plano.json',plan)
    index=CorpusIndex(calls.output/'.local'/'corpus',manifest=manifest)
    print('[busca] verificando e construindo o índice local',flush=True)
    info=await asyncio.to_thread(index.build)
    pools={};traces=[];selections={};errors=[]

    async def search_section(section, pairs=None, suffix='inicial'):
        sid=section['id']
        seen={s['id'] for key,detail in selections.items() if key.startswith(sid+'_')
            for s in detail['candidatas']}
        sources,detail=await research(index,section,entrada,plan['pontos'],config,calls,
            pairs=pairs,exclude=seen,suffix=suffix)
        selections[sid+'_'+suffix]=detail
        traces.extend(dict(secao=sid,etapa=suffix,**t) for t in detail['consultas'])
        atomic_json(work/'buscas.json',traces)
        atomic_json(work/'selecao.json',selections)
        return sources

    async def write_one(section, previous=None, report=None):
        sid=section['id']
        try:
            sources=pools.get(sid,[])
            if previous is None:
                sources=await search_section(section)
            elif report:
                essential=report.get('lacunas_essenciais',[])
                new=[]
                if essential and report['consultas']:
                    focus=dict(section,pontos=sorted({g['ponto'] for g in essential}))
                    try:
                        new=await search_section(focus,report['consultas'],'complementar')
                    except (Fatal,BudgetExceeded):raise
                    except (CallFailure,ValueError) as exc:
                        errors.append(dict(secao=sid,etapa='pesquisa_complementar',erro=str(exc)))
                useful=[r for r in new if r['pertinencia']=='direta']
                if report['decisao']=='liberar' and not useful:
                    print(f'[contexto:{sid}] conteúdo preservado; pesquisa não trouxe evidência direta nova',flush=True)
                    return previous
                if useful:
                    # Mantém as evidências do texto correto e acrescenta as novas.
                    known={r['id'] for r in sources}
                    sources=sources+[r for r in new if r['id'] not in known]
                    report=dict(report,correcao='; '.join(filter(None,[report['correcao'],
                        'Completar somente as lacunas essenciais com as novas evidências: '+
                        '; '.join(g['descricao'] for g in essential)])))
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

    async def audit(current,suffix):
        if not current:
            return dict(secoes=[],cobertura=[dict(id=p['id'],estado='ausente',secoes=[],
                motivo='Sem evidência pertinente ou redação concluída') for p in plan['pontos']],omissoes_escopo=[])
        return await review_all(current,suffix,entrada=entrada,plan=plan,pools=pools,
            config=config,calls=calls,errors=errors,work=work)

    current=await write_many(plan['secoes'])
    drafts=dict(current)
    review=await audit(current,'inicial')
    repairs={r['id']:r for r in review['secoes'] if not r.get('operacional') and
        (r['decisao']=='corrigir' or (r['lacunas_essenciais'] and r['consultas']))}
    if repairs:
        fixed=await write_many([s for s in plan['secoes'] if s['id'] in repairs],current,repairs)
        changed=any(digest(result)!=digest(current[sid]) for sid,result in fixed.items())
        # Falha em melhorar cobertura preserva conteúdo aprovado. Erro conhecido
        # continua impedindo liberação quando a correção falha.
        bad={sid for sid,r in repairs.items() if r['decisao']=='corrigir'}
        current={sid:r for sid,r in current.items() if sid not in bad or sid in fixed}
        current.update(fixed);drafts.update(fixed)
        if changed:review=await audit(current,'final')
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
        cobertura=coverage,cobertura_revisada=review['cobertura'],prioritarios_pendentes=missing,omissoes_escopo=review['omissoes_escopo'],erros=errors,
        criterio_qualidade=REVISION,corpus=info,corpus_manifest=corpus_identity,entrada=digest(entrada),
        documento_sha256=digest(doc),aprovacao='revisão automática; validação pelo especialista pendente')
    report['pendencias']=[dict(secao=r['id'],qualidade=r['decisao'],motivo=r['motivo'],
        lacunas_essenciais=r.get('lacunas_essenciais',[]),limites=r.get('limites',[])) for r in review['secoes']]
    report['secoes_para_revisao']=len(drafts)
    report['motivo_parada']=('escopo_atendido' if report['status']=='concluido' else
        'correcao_pendente' if any(r['decisao']=='corrigir' for r in review['secoes']) else
        'falha_operacional' if errors else 'evidencias_insuficientes')
    report['qa_elegivel']=qa_ready(report)
    metadata={sid:[{k:v for k,v in s.items() if k!='texto'} for s in pool] for sid,pool in pools.items()}
    atomic_json(calls.output/'.local'/'evidencias'/(version+'.json'),pools)
    atomic_json(work/'rastreabilidade.json',dict(secoes=sections,fontes=metadata))
    atomic_json(work/'cobertura.json',report);atomic_json(Path(root)/'cobertura.json',report)
    atomic_json(Path(root)/'documento.json',doc)
    for name,rows in (('documento.md',sections),('rascunho_para_revisao.md',
            [drafts[s['id']] for s in plan['secoes'] if s['id'] in drafts])):
        lines=['# '+doc['titulo']]
        for section in rows:lines+=['','## '+section['titulo'],'',section['texto']]
        (Path(root)/name).write_text('\n'.join(lines)+'\n',encoding='utf-8')
    return sections,report
