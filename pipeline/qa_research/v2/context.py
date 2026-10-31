"""Planejamento pelo escopo, pesquisa direcionada e revisão global com retorno."""
import json
import math
from pathlib import Path

from pipeline.inventario.textutil import atomic_json, read_json
from pipeline.qa_research.corpus import CorpusIndex
from pipeline.qa_research.document.common import Packet, citations_for, source_record, file_hash
from pipeline.qa_research.document.runner import Runner
from .common import digest, require, text, unique, ids, exact_rows
from . import prompts as P
from .language import POLICY, QUERIES, validate_pairs, bilingual_search, audit_blocks, language_counts


def validate_plan(data, selected, maximum):
    rows=data.get('recortes');unique(rows)
    require(1<=len(rows)<=maximum,'Quantidade inválida de recortes')
    for r in rows:
        require(all(text(r.get(k)) for k in ('titulo','foco','ancora')),'Recorte incompleto')
        require(r['ancora'] in selected['frase_especialista'],'Âncora não pertence à frase do especialista')
        require(type(r.get('essencial')) is bool,'essencial deve ser booleano')
        for key in ('consultas','termos'):
            require(isinstance(r.get(key),list) and 1<=len(r[key])<=6 and all(text(s) for s in r[key]),'Consultas/termos inválidos')


def flatten(document):
    result=[]
    for ci,c in enumerate(document['capitulos']):
        for bi,b in enumerate(c['blocos']):
            result.append(dict(id=f'B{ci+1:03}_{bi+1:03}',capitulo=c['titulo'],**b))
    return result


def validate_review(data, facets, blocks):
    rows=data.get('cobertura');exact_rows(rows,[f['id'] for f in facets])
    for r in rows:
        require(type(r.get('coberto')) is bool and text(r.get('justificativa')),'Parecer incompleto')
        ids(r.get('blocos'),blocks,nonempty=r['coberto'])
        for key in ('lacunas','proximas_consultas'):
            require(isinstance(r.get(key),list) and all(text(s) for s in r[key]),'Lacunas/consultas inválidas')
    require(isinstance(data.get('correcoes'),list) and isinstance(data.get('repeticoes'),list),'Revisão global inválida')
    for c in data['correcoes']:
        ids(c.get('blocos'),blocks);require(text(c.get('problema')),'Correção sem motivo')
    for d in data['repeticoes']:
        require(d.get('manter') in blocks,'Bloco a manter inexistente')
        ids(d.get('remover'),set(blocks)-{d['manter']})
        require(text(d.get('justificativa')),'Deduplicação sem justificativa')
    require(isinstance(data.get('novas_relacoes'),list),'Novas relações devem ser explícitas')
    for r in data['novas_relacoes']:
        ids(r.get('blocos'),blocks);require(text(r.get('conhecimento')),'Relação sem conhecimento')


def packet(path, selected, facets, evidence, config):
    """Converte recuperação em pacote verificado compatível com o auditor existente."""
    path=Path(path);path.mkdir(parents=True,exist_ok=True)
    sources={r['id']:r for rows in evidence.values() for r in rows}
    runtime=dict(model=config['models']['doc_write'],workers=config['workers'],max_calls=2500,
        max_attempts=3,timeout=300,research_rounds=max(1,math.ceil(config['sources_per_facet']/6)),batch_sources=6,writer_sources=18,
        max_blocks=8,max_block_words=220,audit_repairs=1,facet_retry_passes=1)
    profile=dict(schema='document-profile-v2',topic=dict(titulo=selected['titulo'],escopo=selected['frase_especialista']),
        runtime=runtime,facets=[dict(id=f['id'],titulo=f['titulo'],grupo=selected['subtopico'],foco=f['foco'],
             consultas=f['consultas'],termos=f['termos']) for f in facets])
    atomic_json(path/'profile.json',profile)
    atomic_json(path/'facets.json',[dict(f,fontes=[r['id'] for r in evidence[f['id']]]) for f in profile['facets']])
    atomic_json(path/'preparation.json',dict(input_mode='busca_bm25_por_cobertura',partial=True,
        limitations=['Recuperação limitada ao manifesto instalado; sem afirmação de exaustividade']))
    for name,rows in (('sources.jsonl',sources.values()),('citations.jsonl',[c for s in sources.values() for c in citations_for(s)])):
        (path/name).write_text(''.join(json.dumps(r,ensure_ascii=False)+'\n' for r in rows),encoding='utf-8')
    atomic_json(path/'manifest.json',dict(schema='document-packet-v2',files={n:file_hash(path/n)
        for n in ('profile.json','sources.jsonl','citations.jsonl','facets.json','preparation.json')}))
    return Packet(path)


class Router:
    def __init__(self,calls,feedback): self.calls,self.feedback=calls,feedback

    def json(self,system,user,tag='',item=None,max_tokens=9000,validate=None,**kwargs):
        stage=tag.removeprefix('document_')
        role={'research':'doc_research','write':'doc_write','audit':'doc_audit',
              'dedup':'dedup','gaps':'coverage','discover':'doc_research'}[stage]
        payload=json.loads(user)
        system+='\n'+POLICY
        if stage=='write':
            payload['orientacoes_revisao_global']=self.feedback
            system+='\nAtenda as orientacoes_revisao_global sem trocar o escopo nem inventar fundamento.'
        return self.calls.call(role,system,payload,validate,max_tokens)


def review_document(selected,plan,facets,blocks,knowledge,calls,work):
    linguistic=audit_blocks(blocks,calls)
    atomic_json(work/'revisao_ptbr.json',linguistic)
    byid={b['id']:b for b in blocks}
    review=calls.call('coverage',P.COVERAGE,dict(entrada=selected,plano=plan,blocos=blocks,conhecimentos_anteriores=knowledge),
        lambda d:validate_review(d,facets,byid))
    return {**review,'correcoes':review['correcoes']+linguistic['correcoes']}


def generate(selected,manifest,output,config,calls):
    output=Path(output);output.mkdir(parents=True,exist_ok=True)
    plan=calls.call('plan',P.PLAN,dict(entrada=selected,max_facets=config['max_facets']),
        lambda d:validate_plan(d,selected,config['max_facets']))
    atomic_json(output/'plano.json',plan);facets=plan['recortes']
    index=CorpusIndex(calls.output/'.local'/'corpus',manifest=manifest);info=index.build()
    evidence={f['id']:[] for f in facets};seen_chunks={f['id']:set() for f in facets}
    feedback={};history=[];no_gain=0;knowledge=[]
    final,review,reason=None,None,'limite_rodadas'
    for round_no in range(1,config['document_rounds']+1):
        print(f'[contexto] rodada {round_no}/{config["document_rounds"]}',flush=True)
        new_count=0;traces=[]
        for f in facets:
            old=evidence[f['id']];fresh=[]
            queries=list(f['consultas'])
            if review:
                r=next(r for r in review['cobertura'] if r['id']==f['id'])
                queries=r['proximas_consultas']+queries
            bilingual=calls.call('queries',QUERIES,dict(entrada=selected,recorte=f,consultas_e_lacunas=queries,
                limite=config['queries_per_facet']),lambda d:validate_pairs(d,config['queries_per_facet']))
            rows,query_traces=bilingual_search(index,bilingual['pares'],config['retrieval_candidates'],seen_chunks[f['id']])
            traces.extend({**t,'recorte':f['id']} for t in query_traces)
            for row in rows:
                s=source_record(row)
                if s['id'] not in {v['id'] for v in fresh}: fresh.append(s)
            # O teto limita o pacote ativo, não impede investigar uma lacuna nova.
            # Prioriza as fontes recém-recuperadas; as rodadas anteriores continuam auditáveis.
            selected_sources=[];counts={}
            for s in fresh+old:
                doc=s.get('document_id')
                if counts.get(doc,0)>=config['max_per_document']: continue
                if len(selected_sources)>=config['sources_per_facet']: break
                selected_sources.append(s);counts[doc]=counts.get(doc,0)+1
            accepted_new=[s for s in selected_sources if s['chunk_id'] not in seen_chunks[f['id']]]
            seen_chunks[f['id']].update(s['chunk_id'] for s in selected_sources)
            evidence[f['id']]=selected_sources
            new_count+=len(accepted_new)
        work=output/f'rodada_{round_no:02}'
        require(any(evidence.values()),'Nenhuma passagem recuperada; amplie o corpus ou as consultas antes de redigir')
        atomic_json(work/'recuperacoes.json',traces)
        atomic_json(work/'idiomas_busca.json',dict(consultas_por_idioma={lang:sum(t['query_language']==lang for t in traces) for lang in ('pt','en')},
            passagens_selecionadas_por_idioma=language_counts([r for rows in evidence.values() for r in rows]),
            nota='Identificação de idioma é estatística; não exclui fontes. Originais não são traduzidos nem alterados.'))
        p=packet(work/'pacote',selected,facets,evidence,config)
        summary=Runner(p,work/'documental',client=Router(calls,feedback),budget=calls.budget).run()
        require(summary['status']=='concluido','Documento com processamento pendente: '+summary['status'])
        final=read_json(work/'documental'/'documento.json')
        blocks=flatten(final);byid={b['id']:b for b in blocks}
        review=review_document(selected,plan,facets,blocks,knowledge,calls,work)
        atomic_json(work/'revisao_global.json',review)
        missing=[r['id'] for r in review['cobertura'] if not r['coberto'] and
                 next(f for f in facets if f['id']==r['id'])['essencial']]
        defects=bool(review['correcoes'] or review['repeticoes'])
        new_knowledge=[r['conhecimento'] for r in review['novas_relacoes'] if r['conhecimento'] not in knowledge]
        knowledge.extend(new_knowledge)
        no_gain=no_gain+1 if not new_knowledge else 0
        history.append(dict(rodada=round_no,novas_evidencias=new_count,essenciais_pendentes=missing,
                            problemas_globais=defects,blocos=len(blocks),novas_relacoes_auditadas=len(new_knowledge)))
        feedback=review
        if not missing and not defects: reason='cobertura_suficiente';break
        if no_gain>=config['document_patience']: reason='pesquisa_estabilizada_com_pendencias';break
    # Conflitos globais conhecidos não podem entrar silenciosamente no contexto QA.
    excluded={b for c in review['correcoes'] for b in c['blocos']}
    excluded.update(b for d in review['repeticoes'] for b in d['remover'])
    if excluded:
        for ci,c in enumerate(final['capitulos']):
            c['blocos']=[b for bi,b in enumerate(c['blocos']) if f'B{ci+1:03}_{bi+1:03}' not in excluded]
        final['capitulos']=[c for c in final['capitulos'] if c['blocos']]
        blocks=flatten(final);byid={b['id']:b for b in blocks}
        review=review_document(selected,plan,facets,blocks,knowledge,calls,work)
        reason='revisao_final_apos_exclusoes'
    atomic_json(output/'documento.json',final)
    md=['# '+final['titulo']]
    for c in final['capitulos']:
        md+=['','## '+c['titulo']]
        for b in c['blocos']: md+=['','### '+b['subtitulo'],'',b['texto']]
    (output/'documento.md').write_text('\n'.join(md)+'\n',encoding='utf-8')
    report=dict(status='concluido' if reason=='cobertura_suficiente' else 'parcial',motivo_parada=reason,
        historico=history,revisao=review,corpus=info,documento_sha256=digest(final),
        blocos_excluidos=sorted(excluded),qa_elegivel=bool(flatten(final)) and not review['correcoes'] and not review['repeticoes'],
        ptbr_revisado=True,
        aprovacao='auditado_modelo; revisão humana pendente')
    atomic_json(output/'cobertura.json',report)
    return final,report
