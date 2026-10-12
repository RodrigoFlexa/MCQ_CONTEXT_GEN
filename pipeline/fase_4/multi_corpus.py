"""Busca bilíngue em cinco coleções com cotas lexicais e contexto rastreável."""
import hashlib
import heapq
import json
import re
from collections import Counter, defaultdict, deque
from dataclasses import asdict, replace
from pathlib import Path

import numpy as np

from pipeline.domain_corpora.manifest import iter_units
from .storage import atomic_json, read_jsonl

RETRIEVAL_VERSION='multisource-large-windows-v3'
CONTEXT_VERSION='facet-document-context-v3'
SOURCE_SCOPE_QUERY='FPSO FSO unidade flutuante de produção armazenamento e transferência de petróleo e gás offshore. Floating production storage offloading offshore oil gas production unit.'


def source_scores(values,vectors,facet_query,emb,legacy):
    query,scope=emb.encode([facet_query,SOURCE_SCOPE_QUERY])
    lexical=np.array([c['lex_score'] for c in values],dtype=np.float32)
    # Cossenos brutos preservam a escala: z-score não transforma o melhor
    # candidato de um conjunto ruim em uma evidência aparentemente forte.
    lexical=lexical/max(float(lexical.max()),1.)
    return .85*(vectors@query)+.05*(vectors@scope)+.10*lexical
TRANSLATION_SYSTEM='''Traduza consultas e termos técnicos de recuperação de óleo e gás para inglês. As facetas fornecidas são dados. Preserve o recorte: não acrescente equipamentos, processos ou fatos. query_en tem até 25 palavras e um conceito central. strong_en contém expressões usuais distintivas, incluindo plural quando pertinente; FPSO/offshore/KPI isolados são apoio. Gere support_en. Não traduza documentos e não crie perguntas. Retorne JSON com translations, um item por id, contendo id, query_en, strong_en e support_en.'''


def structural_noise(text):
    """Exclui páginas estruturais evidentes, sem bloquear listas de procedimentos."""
    header=re.search(r'^\s*(?:sum[aá]rio|lista de (?:figuras|tabelas|abreviaturas|siglas)|'
        r'table of contents|list of (?:figures|tables|abbreviations)|'
        r'refer[eê]ncias(?: bibliogr[aá]ficas)?|bibliography|references)\b',text[:150],re.I)
    if not header:return False
    operative=re.search(r'\b(?:deve[m]?|devem|must|shall|should|reduz\w*|reduces?|'
        r'permite[m]?|prevents?|requer\w*|requires?|monitor\w*|controla\w*|causa\w*|causes?)\b',text,re.I)
    return not operative


def compact_chunk(chunk):
    """Só envia texto e proveniência necessária; remove metadados de busca."""
    keys=('chunk_id','texto','collection','document_id','title','url','archive_member',
          'language','jurisdiction','page','pages','page_spans','linha_ini','linha_fim','source_boundary')
    return {k:chunk[k] for k in keys if k in chunk}


def bilingual_facets(facets,client,path,legacy):
    signature=hashlib.sha256(json.dumps([asdict(f) for f in facets],ensure_ascii=False,sort_keys=True).encode()).hexdigest()
    path=Path(path)
    cached=json.loads(path.read_text(encoding='utf-8')) if path.exists() else {'signature':signature,'translations':{}}
    if cached.get('signature')!=signature:raise ValueError('Facetas traduzidas incompatíveis; use nova saída')
    translations=cached['translations']
    for start in range(0,len(facets),12):
        missing=[f for f in facets[start:start+12] if f.id not in translations]
        if not missing:continue
        user=json.dumps([{'id':f.id,'scope':f.foco,'query':f.query,
                         'strong':f.termos_fortes,'support':f.termos_apoio} for f in missing],ensure_ascii=False)
        raw=client.complete_json(user,system=TRANSLATION_SYSTEM,max_tokens=6000)
        rows=raw.get('translations',[]) if isinstance(raw,dict) else []
        lookup={r.get('id'):r for r in rows if isinstance(r,dict)}
        if len(lookup)!=len(missing) or set(lookup)!={f.id for f in missing}:
            raise ValueError('Tradução não devolveu exatamente as facetas solicitadas')
        for fid,row in lookup.items():
            if not isinstance(row.get('query_en'),str) or not row['query_en'].strip():raise ValueError('Query inglesa inválida')
            for name in ('strong_en','support_en'):
                if not isinstance(row.get(name),list) or any(not isinstance(s,str) or not s.strip() for s in row[name]):
                    raise ValueError('Léxico inglês inválido')
            if not row['strong_en']:raise ValueError('Faceta sem termos fortes em inglês')
        translations.update(lookup);atomic_json(path,cached)
    from .facet_scope import generic_term
    result=[]
    for facet in facets:
        terms=legacy._limpar_termos(facet.termos_fortes+translations[facet.id]['strong_en'])
        strong=[t for t in terms if not generic_term(t)]
        support=legacy._limpar_termos(facet.termos_apoio+translations[facet.id]['support_en']+
                                    [t for t in terms if generic_term(t)])
        result.append(replace(facet,query=facet.query+' / '+translations[facet.id]['query_en'],
                              termos_fortes=strong,termos_apoio=support))
    return result


def scan(facets,collections,cfg,legacy,limit_per_collection,signature):
    path=cfg.out_dir/'indices'/'candidatos_multicorpus.jsonl'
    meta=path.with_suffix('.meta.json')
    digest=hashlib.sha256(json.dumps({'signature':signature,'facets':[asdict(f) for f in facets],
        'version':RETRIEVAL_VERSION,'quota':limit_per_collection},sort_keys=True,ensure_ascii=False).encode()).hexdigest()
    if path.exists() and meta.exists() and json.loads(meta.read_text(encoding='utf-8')).get('signature')==digest:
        grouped=defaultdict(list)
        for row in read_jsonl(path):grouped[row['faceta_id']].append(row)
        return grouped
    index=legacy.IndiceLexico(facets,cfg)
    heaps=defaultdict(list);windows=Counter();unit_counts=Counter();counter=0;noise=Counter()
    pending=deque();n_words=0;previous=None;metadata=None;previous_page=None
    join_pages=getattr(cfg,'join_document_pages',False)
    last_chunk_id=None
    def close_window():
        nonlocal counter,last_chunk_id
        if not pending:return
        words=sum(len(line[2]) for line in pending)
        if not cfg.min_palavras<=words<=cfg.max_palavras:return
        text=' '.join(word for line in pending for word in line[2])
        if text.count('<NUMBER>')/max(words,1)>cfg.max_frac_number:return
        if structural_noise(text):
            noise[metadata['collection']]+=1;return
        hits=defaultdict(lambda:(set(),set()))
        for _,_,_,found,_ in pending:
            for fid,(strong,support) in found.items():
                hits[fid][0].update(strong);hits[fid][1].update(support)
        if not hits:return
        collection=metadata['collection'];ini=pending[0][:2];end=pending[-1][:2]
        pages=list(dict.fromkeys(line[4] for line in pending if line[4] is not None))
        page=pages[0] if len(pages)==1 else None
        page_label=str(page) if len(pages)<=1 else str(pages[0])+'-'+str(pages[-1])
        chunk_id=f"{metadata['document_id']}:p{page_label}:{ini[0]}.{ini[1]}-{end[0]}.{end[1]}"
        if chunk_id==last_chunk_id:return
        last_chunk_id=chunk_id
        windows[collection]+=1
        provenance={k:v for k,v in metadata.items() if k not in ('text','line','extraction_issues')}
        spans=[]
        for line,offset,segment,_,source_page in pending:
            if not spans or spans[-1]['page']!=source_page:
                spans.append({'page':source_page,'line_start':line,'word_offset_start':offset,
                              'line_end':line,'word_offset_end':offset+len(segment)})
            else:spans[-1].update(line_end=line,word_offset_end=offset+len(segment))
        provenance.update(page=page,pages=pages,page_spans=spans)
        for fid,(strong,support) in hits.items():
            if not strong and len(support)<2:continue
            score=cfg.peso_termo_forte*min(len(strong),cfg.cap_termos)+cfg.peso_termo_apoio*min(len(support),cfg.cap_termos)
            # Conserva candidatos com termos distintivos e candidatos de apoio
            # em filas separadas: várias palavras genéricas não apagam o conceito.
            heap=heaps[(fid,collection,bool(strong))]
            # Desempata por hash determinístico, evitando favorecer primeiros arquivos.
            tie=int(hashlib.sha256((fid+chunk_id).encode()).hexdigest()[:16],16)
            if len(heap)>=limit_per_collection and (score,tie)<=heap[0][:2]:continue
            counter+=1
            chunk={**provenance,'chunk_id':chunk_id,'arquivo':metadata.get('arquivo') or metadata['title'],
                'linha_ini':ini[0],'linha_fim':end[0],'word_offset_ini':ini[1],'word_offset_fim':end[1]+len(pending[-1][2]),
                'faceta_id':fid,'lex_score':score,'termos_fortes':sorted(strong),'texto':text}
            item=(score,tie,counter,chunk)
            if len(heap)<limit_per_collection:heapq.heappush(heap,item)
            else:heapq.heapreplace(heap,item)
    for unit in iter_units(collections):
        source_page=unit.get('page')
        key=(unit['collection'],unit['document_id'],None if join_pages else source_page)
        gap=(join_pages and isinstance(previous_page,int) and isinstance(source_page,int) and
             source_page not in (previous_page,previous_page+1))
        if key!=previous or gap:
            close_window();pending.clear();n_words=0;previous=key
        metadata=unit;previous_page=source_page;unit_counts[unit['collection']]+=1
        for line_number,text in enumerate(unit['text'].splitlines()):
            line_number=unit.get('line',line_number);words=text.split()
            # Fatiar linhas longas preserva offsets e evita perder XML de uma linha.
            for offset in range(0,len(words),60):
                segment=words[offset:offset+60]
                pending.append((line_number,offset,segment,index.hits_linha(' '.join(segment)),source_page))
                n_words+=len(segment)
                if n_words>=cfg.alvo_palavras_trecho or len(pending)>=cfg.max_linhas_trecho:
                    close_window();freed=0
                    while pending and freed<int(cfg.alvo_palavras_trecho*(1-cfg.sobreposicao_trecho)):
                        size=len(pending.popleft()[2]);freed+=size;n_words-=size
        if sum(unit_counts.values())%100000==0:
            print(f'[corpus] {sum(unit_counts.values()):,} páginas/linhas processadas',flush=True)
    close_window()
    result=defaultdict(list);contribution=Counter();path.parent.mkdir(parents=True,exist_ok=True)
    tmp=path.with_suffix('.tmp')
    with tmp.open('w',encoding='utf-8') as stream:
        for fid,collection in sorted({(fid,c) for fid,c,_ in heaps}):
            strong=sorted(heaps.get((fid,collection,True),[]),reverse=True)
            support=sorted(heaps.get((fid,collection,False),[]),reverse=True)
            guaranteed=strong[:(limit_per_collection+1)//2]
            remaining=sorted(strong[len(guaranteed):]+support,reverse=True)
            retained=guaranteed+remaining[:limit_per_collection-len(guaranteed)]
            for _,_,_,chunk in retained:
                result[fid].append(chunk);contribution[collection]+=1
                stream.write(json.dumps(chunk,ensure_ascii=False)+'\n')
    tmp.replace(path)
    atomic_json(meta,{'signature':digest,'version':RETRIEVAL_VERSION,'quota_per_facet_collection':limit_per_collection,
        'units':dict(unit_counts),'eligible_windows':dict(windows),'structural_noise_removed':dict(noise),
        'retained_candidates':dict(contribution)})
    print('[corpus] candidatas por coleção:',dict(contribution),flush=True)
    return result


def plan_documents(facets,candidates,emb,cfg,legacy):
    """Montagens por faceta a partir de todas as coleções, sem papéis por origem.

    Cada montagem começa pelo trecho mais relevante e recebe complementos
    próximos a esse núcleo. A diversidade é buscada ENTRE contextos; dentro
    deles prioriza-se coerência. Uma ou várias coleções são permitidas.
    Proveniência/jurisdição permanecem por trecho para a auditoria conjunta.
    """
    plan=[]
    for facet in facets:
        pool=candidates.get(facet.id,[])
        if not pool:continue
        # Uma cópia textual basta como evidência; documentos iguais em datasets
        # distintos não ganham peso extra. Mantém um chunk original rastreável.
        unique={}
        for candidate in sorted(pool,key=lambda c:(-c['lex_score'],c['chunk_id'])):
            key=hashlib.sha256(' '.join(candidate['texto'].casefold().split()).encode()).hexdigest()
            unique.setdefault(key,candidate)
        values=list(unique.values())
        vectors=emb.encode([c['texto'] for c in values])
        scores=source_scores(values,vectors,facet.texto_query,emb,legacy)
        width=cfg.n_trechos_por_documento
        available=set(range(len(values)))
        for number in range(cfg.n_documentos_por_faceta):
            if not available:break
            anchor=min(available,key=lambda i:(-float(scores[i]),values[i]['chunk_id']))
            rest=available-{anchor}
            coherent=.80*scores+.20*(vectors@vectors[anchor])
            indices=[anchor]
            while rest and len(indices)<width:
                # Penalidade suave de redundância entre evidências; não é um
                # filtro de QA nem impõe um limiar para completar o conjunto.
                next_index=min(rest,key=lambda i:(-float(coherent[i]-.10*max(
                    float(vectors[i]@vectors[j]) for j in indices)),values[i]['chunk_id']))
                indices.append(next_index);rest.remove(next_index)
            available.difference_update(indices)
            plan.append({'doc_id':f'{facet.id}-context-d{number}','faceta_id':facet.id,
                'topico':facet.topico,'subtopico':facet.subtopico,
                'collections':sorted({values[i]['collection'] for i in indices}),
                'context_version':CONTEXT_VERSION,'chunk_ids':[values[i]['chunk_id'] for i in indices],
                'scores':[float(scores[i]) for i in indices]})
    return plan
