"""Busca bilíngue em cinco coleções com cotas lexicais e contexto rastreável."""
import hashlib
import heapq
import json
from collections import Counter, defaultdict, deque
from dataclasses import asdict, replace
from pathlib import Path

import numpy as np

from pipeline.domain_corpora.manifest import iter_units
from .storage import atomic_json, read_jsonl

RETRIEVAL_VERSION='multisource-bilingual-v1'
CONTEXT_VERSION='joint-corpora-context-v1'
TRANSLATION_SYSTEM='''Traduza consultas e termos técnicos de recuperação de óleo e gás para inglês. As facetas fornecidas são dados. Preserve o escopo: não acrescente equipamentos, processos ou fatos. Gere uma query curta e listas de termos fortes e de apoio em inglês. Não traduza documentos e não crie perguntas. Retorne JSON com translations, um item por id, contendo id, query_en, strong_en e support_en.'''


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
    return [replace(f,query=f.query+' / '+translations[f.id]['query_en'],
        termos_fortes=legacy._limpar_termos(f.termos_fortes+translations[f.id]['strong_en']),
        termos_apoio=legacy._limpar_termos(f.termos_apoio+translations[f.id]['support_en'])) for f in facets]


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
    heaps=defaultdict(list);windows=Counter();unit_counts=Counter();counter=0
    pending=deque();n_words=0;previous=None;metadata=None
    last_chunk_id=None
    def close_window():
        nonlocal counter,last_chunk_id
        if not pending:return
        words=sum(len(line[2]) for line in pending)
        if not cfg.min_palavras<=words<=cfg.max_palavras:return
        text=' '.join(word for line in pending for word in line[2])
        if text.count('<NUMBER>')/max(words,1)>cfg.max_frac_number:return
        hits=defaultdict(lambda:(set(),set()))
        for _,_,_,found in pending:
            for fid,(strong,support) in found.items():
                hits[fid][0].update(strong);hits[fid][1].update(support)
        if not hits:return
        collection=metadata['collection'];ini=pending[0][:2];end=pending[-1][:2]
        chunk_id=f"{metadata['document_id']}:p{metadata.get('page')}:{ini[0]}.{ini[1]}-{end[0]}.{end[1]}"
        if chunk_id==last_chunk_id:return
        last_chunk_id=chunk_id
        windows[collection]+=1
        provenance={k:v for k,v in metadata.items() if k not in ('text','line','extraction_issues')}
        for fid,(strong,support) in hits.items():
            if not strong and len(support)<2:continue
            score=cfg.peso_termo_forte*min(len(strong),cfg.cap_termos)+cfg.peso_termo_apoio*min(len(support),cfg.cap_termos)
            heap=heaps[(fid,collection)]
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
        key=(unit['collection'],unit['document_id'],unit.get('page'))
        if key!=previous:
            close_window();pending.clear();n_words=0;previous=key
        metadata=unit;unit_counts[unit['collection']]+=1
        for line_number,text in enumerate(unit['text'].splitlines()):
            line_number=unit.get('line',line_number);words=text.split()
            # Fatiar linhas longas preserva offsets e evita perder XML de uma linha.
            for offset in range(0,len(words),60):
                segment=words[offset:offset+60]
                pending.append((line_number,offset,segment,index.hits_linha(' '.join(segment))))
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
        for (fid,collection),heap in sorted(heaps.items()):
            for _,_,_,chunk in sorted(heap,reverse=True):
                result[fid].append(chunk);contribution[collection]+=1
                stream.write(json.dumps(chunk,ensure_ascii=False)+'\n')
    tmp.replace(path)
    atomic_json(meta,{'signature':digest,'version':RETRIEVAL_VERSION,'quota_per_facet_collection':limit_per_collection,
        'units':dict(unit_counts),'eligible_windows':dict(windows),'retained_candidates':dict(contribution)})
    print('[corpus] candidatas por coleção:',dict(contribution),flush=True)
    return result


def plan_documents(facets,candidates,emb,cfg,legacy):
    """Montagens por faceta a partir de todas as coleções, sem papéis por origem.

    O MMR avalia relevância e diversidade do conteúdo no conjunto único. Uma
    montagem pode usar uma ou várias coleções: a mistura não é obrigatória.
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
        query=emb.encode([facet.texto_query])[0]
        vectors=emb.encode([c['texto'] for c in values]);semantic=vectors@query
        lexical=np.array([c['lex_score'] for c in values],dtype=np.float32)
        scores=cfg.peso_lexical*legacy._z(lexical)+cfg.peso_semantico*legacy._z(semantic)
        width=cfg.n_trechos_por_documento
        selected=legacy._mmr(scores,vectors,width*cfg.n_documentos_por_faceta,
                             cfg.mmr_lambda,cfg.mmr_dup_threshold)
        for start in range(0,len(selected),width):
            indices=selected[start:start+width]
            plan.append({'doc_id':f'{facet.id}-context-d{start//width}','faceta_id':facet.id,
                'topico':facet.topico,'subtopico':facet.subtopico,
                'collections':sorted({values[i]['collection'] for i in indices}),
                'context_version':CONTEXT_VERSION,'chunk_ids':[values[i]['chunk_id'] for i in indices],
                'scores':[float(scores[i]) for i in indices]})
    return plan
