"""BM25/RRF existente, leitura de pertinência e uma busca complementar delimitada."""
import json

from pipeline.qa_research.v2.language import bilingual_search
from pipeline.qa_research.v2.navigation import navigation_reason
from . import contracts as C, prompts as P
from .runtime import digest

REVISION='relevance-selection-1'


def prompt_source(source):
    row={k:source[k] for k in ('id','texto','collection','language','jurisdiction','year',
        'document_type','page_ini','page_fim','aplicabilidade','pertinencia') if k in source}
    title=source.get('title')
    if isinstance(title,str) and len(title)<=1000:row['title']=title
    elif title:row['title_omitted_chars']=len(str(title))
    return row


def candidates(index,pairs,config,retained=()):
    hits,traces=bilingual_search(index,pairs,config['retrieval_candidates'])
    clean=[];excluded=[]
    for row in hits:
        reason=navigation_reason(row)
        if reason:
            excluded.append(dict(chunk_id=row['chunk_id'],motivo=reason));continue
        clean.append(dict(id='E'+digest([row['chunk_id'],row['content_hash']])[:20],texto=row['texto'],
            **{k:row.get(k) for k in ('collection','document_id','chunk_id','language','title','url',
                'page_ini','page_fim','source_boundary','jurisdiction','document_type','year')}))
    # Um candidato de cada coleção primeiro; o restante conserva a ordem RRF.
    first=[];seen=set()
    for row in clean:
        if row['collection'] not in seen:first.append(row);seen.add(row['collection'])
    selected=[];ids=set();counts={}
    for row in list(retained)+first+clean:
        if navigation_reason(row) or row['id'] in ids:continue
        doc=row['document_id']
        if counts.get(doc,0)>=config['max_per_document']:continue
        if len(selected)>=min(24,config['retrieval_candidates']):break
        selected.append(row);ids.add(row['id']);counts[doc]=counts.get(doc,0)+1
    return selected,traces,excluded


def validate_selection(data,sources,points):
    C.exact(data.get('avaliacoes'),sources,'avaliacoes')
    for row in data['avaliacoes']:
        C.require(row.get('pertinencia') in ('direta','apoio','descartar') and C.text(row.get('motivo')),
            row['id']+': pertinência e motivo obrigatórios')
        C.require(C.text(row.get('aplicabilidade')),row['id']+': explicite o equipamento/processo e limites de aplicação')
    C.refs(data.get('lacunas'),points,'lacunas',empty=True)
    C.pairs(data.get('consultas'), 'consultas',empty=True)
    C.require(len(data['consultas'])<=3,'No máximo três pares de consultas complementares')


async def research(index,section,entrada,points,config,calls,retained=(),pairs=None,complement=True):
    """No máximo duas seleções iniciais; correção usa somente uma seleção."""
    sources,traces,excluded=candidates(index,pairs or section['consultas'],config,retained)
    reports=[];metadata={}
    for turn in range(2 if complement else 1):
        metadata.update((s['id'],{k:v for k,v in s.items() if k!='texto'}) for s in sources)
        payload=dict(entrada=entrada,secao={k:section[k] for k in ('id','titulo','pontos')},
            pontos=[p for p in points if p['id'] in section['pontos']],candidatas=[])
        packed=[]
        for row in sources:
            test=dict(payload,candidatas=payload['candidatas']+[prompt_source(row)])
            if len(json.dumps(test,ensure_ascii=False))+len(P.SELECT)<=config['max_input_chars']:
                payload=test;packed.append(row)
            else:excluded.append(dict(id=row['id'],motivo='passagem integral não cabe na seleção'))
        if not packed:
            return [],dict(consultas=traces,excluidas=excluded,rodadas=reports,candidatas=list(metadata.values()),motivo='Nenhuma passagem utilizável')
        label=section['id']+('_selecao' if complement else '_selecao_correcao')+str(turn+1)
        print(f'[busca:{section["id"]}] selecionando passagens pertinentes',flush=True)
        result=await calls.call('write',label,payload,
            lambda d:validate_selection(d,{s['id'] for s in packed},section['pontos']),system=P.SELECT)
        reports.append(result)
        judged={r['id']:r for r in result['avaliacoes']}
        useful=[dict(row,pertinencia=judged[row['id']]['pertinencia'],
            aplicabilidade=judged[row['id']]['aplicabilidade']) for row in packed
            if judged[row['id']]['pertinencia']!='descartar']
        useful.sort(key=lambda s:s['pertinencia']!='direta')
        selected=useful[:config['sources_per_section']]
        if turn==0 and complement and result['lacunas'] and result['consultas']:
            additional,new_traces,new_excluded=candidates(index,result['consultas'],config,selected)
            traces.extend(new_traces);excluded.extend(new_excluded)
            if {s['id'] for s in additional}-{s['id'] for s in packed}:
                sources=additional;continue
        # Apoio genérico sozinho não justifica uma seção profissional.
        if not any(s['pertinencia']=='direta' for s in selected):selected=[]
        return selected,dict(consultas=traces,excluidas=excluded,rodadas=reports,candidatas=list(metadata.values()),
            selecionadas=[s['id'] for s in selected],lacunas=result['lacunas'])


def qa_ready(report):
    return bool(report and report.get('criterio_qualidade')==REVISION
        and report.get('status')=='concluido' and report.get('secoes_liberadas',0)>0
        and report['secoes_liberadas']==report.get('secoes_planejadas')
        and report.get('cobertura') and report.get('pontos')
        and {p['id'] for p in report['cobertura']}=={p['id'] for p in report['pontos']}
        and all(p['estado']=='atendido' for p in report['cobertura'])
        and not report.get('omissoes_escopo') and not report.get('prioritarios_pendentes'))
