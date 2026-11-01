"""BM25/RRF existente, leitura de pertinência e uma busca complementar delimitada."""
import json

from pipeline.qa_research.v2.language import bilingual_search
from pipeline.qa_research.v2.navigation import navigation_reason
from . import contracts as C, prompts as P
from .runtime import digest

REVISION='focused-research-2'


def prompt_source(source):
    row={k:source[k] for k in ('id','texto','collection','language','jurisdiction','year',
        'document_type','page_ini','page_fim','aplicabilidade','pertinencia','pontos') if k in source}
    title=source.get('title')
    if isinstance(title,str) and len(title)<=1000:row['title']=title
    elif title:row['title_omitted_chars']=len(str(title))
    return row


def candidates(index,pairs,config,exclude=()):
    hits,traces=bilingual_search(index,pairs,config['retrieval_candidates'])
    excluded_ids=set(exclude)
    clean=[];excluded=[]
    for row in hits:
        reason=navigation_reason(row)
        if reason:
            excluded.append(dict(chunk_id=row['chunk_id'],motivo=reason));continue
        sid='E'+digest([row['chunk_id'],row['content_hash']])[:20]
        if sid in excluded_ids:continue
        clean.append(dict(id=sid,texto=row['texto'],
            **{k:row.get(k) for k in ('collection','document_id','chunk_id','language','title','url',
                'page_ini','page_fim','source_boundary','jurisdiction','document_type','year')}))
    # Um candidato de cada coleção primeiro; o restante conserva a ordem RRF.
    first=[];seen=set()
    for row in clean:
        if row['collection'] not in seen:first.append(row);seen.add(row['collection'])
    selected=[];ids=set();counts={}
    for row in first+clean:
        if navigation_reason(row) or row['id'] in ids:continue
        doc=row['document_id']
        if counts.get(doc,0)>=config['max_per_document']:continue
        if len(selected)>=min(config['selection_candidates'],config['retrieval_candidates']):break
        selected.append(row);ids.add(row['id']);counts[doc]=counts.get(doc,0)+1
    return selected,traces,excluded


def validate_selection(data,sources,points,limit,max_support):
    selected=C.rows(data.get('selecionadas'),'selecionadas')
    C.require(len(selected)<=limit,'selecionadas: limite excedido')
    for row in selected:
        C.require(row['id'] in sources and row.get('pertinencia') in ('direta','apoio'),
            row['id']+': passagem desconhecida ou pertinência inválida')
        C.require(C.text(row.get('aplicabilidade')),row['id']+': informe aplicabilidade e limites')
        C.refs(row.get('pontos'),points,row['id']+'.pontos')
    C.require(sum(r['pertinencia']=='apoio' for r in selected)<=max_support,'Excesso de apoio genérico')
    C.refs(data.get('lacunas'),points,'lacunas',empty=True)


async def research(index,section,entrada,points,config,calls,pairs=None,exclude=(),suffix='inicial'):
    """Uma seleção por pesquisa; a revisão decide a única complementação possível."""
    sources,traces,excluded=candidates(index,pairs or section['consultas'],config,exclude)
    payload=dict(entrada=entrada,secao={k:section[k] for k in ('id','titulo','pontos')},
        pontos=[p for p in points if p['id'] in section['pontos']],candidatas=[],
        limite=config['sources_per_section'],max_apoio=config['max_support_sources'])
    packed=[]
    for row in sources:
        test=dict(payload,candidatas=payload['candidatas']+[prompt_source(row)])
        if len(json.dumps(test,ensure_ascii=False))+len(P.SELECT)<=config['max_input_chars']:
            payload=test;packed.append(row)
        else:excluded.append(dict(id=row['id'],motivo='passagem integral não cabe na seleção'))
    detail=dict(consultas=traces,excluidas=excluded,rodadas=[],selecionadas=[],
        candidatas=[{k:v for k,v in s.items() if k!='texto'} for s in sources],
        lacunas=list(section['pontos']))
    if not packed:
        return [],dict(detail,motivo='Nenhuma passagem nova utilizável')
    print(f'[busca:{section["id"]}] selecionando evidências para {suffix}',flush=True)
    result=await calls.call('write',section['id']+'_selecao_'+suffix,payload,
        lambda d:validate_selection(d,{s['id'] for s in packed},section['pontos'],
            config['sources_per_section'],config['max_support_sources']),system=P.SELECT)
    mapping={s['id']:s for s in packed}
    selected=[dict(mapping[r['id']],**{k:r[k] for k in ('pertinencia','aplicabilidade','pontos')})
        for r in result['selecionadas']]
    selected.sort(key=lambda s:s['pertinencia']!='direta')
    if not any(s['pertinencia']=='direta' for s in selected):selected=[]
    detail.update(rodadas=[result],selecionadas=[s['id'] for s in selected],lacunas=result['lacunas'])
    return selected,detail


def qa_ready(report):
    return bool(report and report.get('criterio_qualidade')==REVISION
        and report.get('status')=='concluido' and report.get('secoes_liberadas',0)>0
        and report['secoes_liberadas']==report.get('secoes_planejadas')
        and report.get('cobertura') and report.get('pontos')
        and {p['id'] for p in report['cobertura']}=={p['id'] for p in report['pontos']}
        and all(p['estado']=='atendido' for p in report['cobertura'])
        and not any(r.get('lacunas_essenciais') or r.get('qualidade')=='corrigir' for r in report.get('pendencias',[]))
        and not report.get('omissoes_escopo') and not report.get('prioritarios_pendentes'))
