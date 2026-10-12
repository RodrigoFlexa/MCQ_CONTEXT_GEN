"""Recompõe contextos rejeitados selecionando somente trechos reais e reaudita."""
import hashlib
import json
from pathlib import Path

import numpy as np

from .storage import atomic_json, append_jsonl, read_jsonl, utc_now

VERSION='context-recovery-v1'
SYSTEM_PROMPT='''Você refina a seleção de evidências de um contexto para QA de FPSO/FSO. Use o diagnóstico do auditor para selecionar um novo conjunto coerente de trechos reais, mantendo a faceta e o escopo. Pode excluir trechos, aproveitar trechos compatíveis já utilizados e selecionar substitutos de qualquer coleção, sem funções fixas por corpus. Não reescreva fontes, não complete fatos, não invente IDs, não suavize critérios de qualidade. Não suponha mesma instalação ou condições pela proximidade temática. Selecionar poucas evidências úteis é permitido. Retorne JSON com selected_chunk_ids, reason e unrepairable (booleano). Se não há suporte apropriado, selected_chunk_ids=[] e unrepairable=true. A nova seleção ainda será auditada independentemente.'''


def digest(value):
    return hashlib.sha256(json.dumps(value,sort_keys=True,ensure_ascii=False,default=str).encode()).hexdigest()


def alternative_pool(context,audit,candidates,emb,cfg,legacy,limit,excluded):
    """Mantém evidências úteis e busca alternativas relevantes/diversas no índice."""
    for review in audit.get('chunk_reviews',[]) or []:
        if isinstance(review,dict) and (review.get('compatible') is False or review.get('useful') is False):
            excluded.add(review.get('chunk_id'))
    unique={}
    for candidate in candidates:
        if candidate['chunk_id'] in excluded:continue
        key=' '.join(candidate['texto'].casefold().split())
        if key not in unique or candidate.get('lex_score',0)>unique[key].get('lex_score',0):unique[key]=candidate
    values=list(unique.values())
    if not values:return []
    vectors=emb.encode([c['texto'] for c in values])
    from .multi_corpus import source_scores
    scores=source_scores(values,vectors,context['facet_title']+'. '+context['focus'],emb,legacy)
    # Um trecho da tentativa anterior que seja útil ainda pode ser preservado.
    current={c['chunk_id'] for c in context['chunks']}
    kept=[i for i,c in enumerate(values) if c['chunk_id'] in current][:min(len(current),limit)]
    selected=legacy._mmr(scores,vectors,limit,cfg.mmr_lambda,cfg.mmr_dup_threshold)
    indices=list(dict.fromkeys(kept+selected))[:limit]
    return [values[i] for i in indices]


def validate_plan(raw,pool,previous_sets,width):
    if not isinstance(raw,dict) or type(raw.get('unrepairable')) is not bool:
        raise ValueError('Estrutura inválida do refinador de contexto')
    ids=raw.get('selected_chunk_ids');reason=raw.get('reason')
    if not isinstance(ids,list) or not isinstance(reason,str) or not reason.strip():
        raise ValueError('Seleção/justificativa inválida do refinador de contexto')
    lookup={c['chunk_id']:c for c in pool}
    if any(not isinstance(cid,str) or cid not in lookup for cid in ids):raise ValueError('Refinador inventou ID ou usou trecho excluído')
    if len(ids)>width or len(ids)!=len(set(ids)):raise ValueError('Seleção excede limite ou repete IDs')
    if raw['unrepairable']:
        if ids:raise ValueError('Seleção inconsistente com unrepairable=true')
    elif not ids or frozenset(ids) in previous_sets:
        raise ValueError('Refinador não apresentou uma nova seleção utilizável')
    return {'selected_chunk_ids':ids,'reason':reason.strip(),'unrepairable':raw['unrepairable']}


def choose_plan(client,context,audit,pool,previous_sets,width,path,signature):
    request={'facet_id':context['facet_id'],'focus':context['focus'],'scope':context['scope'],
        'previous_chunk_sets':[sorted(s) for s in previous_sets],
        'diagnostic':{k:audit.get(k) for k in ('reason','issues','validation_errors','chunk_reviews','recovery_advice')},
        'candidate_chunks':pool,'maximum_chunks':width}
    request_hash=digest(request)
    if path.exists():
        saved=json.loads(path.read_text(encoding='utf-8'))
        if saved.get('signature')!=signature or saved.get('request_hash')!=request_hash or saved.get('version')!=VERSION:
            raise ValueError('Plano de recuperação em cache incompatível; use nova saída')
        return validate_plan(saved['plan'],pool,previous_sets,width)
    user=json.dumps(request,ensure_ascii=False)
    for attempt in range(2):
        raw=client.complete_json(user,system=SYSTEM_PROMPT,max_tokens=4000)
        try:plan=validate_plan(raw,pool,previous_sets,width);break
        except ValueError as error:
            if attempt:raise ValueError('Refinador de contexto inválido duas vezes: '+str(error)) from error
            user+='\nCorrija a resposta anterior: '+str(error)
    path.parent.mkdir(parents=True,exist_ok=True)
    atomic_json(path,{'version':VERSION,'signature':signature,'request_hash':request_hash,'plan':plan,'created_at':utc_now()})
    return plan


def recover_context(context,audit,candidates,emb,legacy_cfg,qa_cfg,refiner,auditor,root,signature,legacy,audit_fn,on_audit):
    base_id=context['doc_id'];root=Path(root)
    attempts=[];previous_sets=[frozenset(c['chunk_id'] for c in context['chunks'])];excluded=set()
    current=dict(context)
    journal=root.parent/'recuperacoes_contexto.jsonl'
    recorded={(r['base_doc_id'],r['attempt']) for r in read_jsonl(journal)}
    for number in range(1,qa_cfg.max_context_refinements+1):
        pool=alternative_pool(current,audit,candidates,emb,legacy_cfg,legacy,qa_cfg.context_recovery_pool,excluded)
        path=root/'recuperacoes'/base_id/f'plano-r{number}.json'
        event={'base_doc_id':base_id,'attempt':number,'facet_id':context['facet_id'],
               'topic':context['topic'],'subtopic':context['subtopic'],'previous_doc_id':current['doc_id']}
        if not pool:
            event.update(status='no_eligible_candidates',reason='Não há candidatos elegíveis restantes')
        else:
            plan=choose_plan(refiner,current,audit,pool,previous_sets,legacy_cfg.n_trechos_por_documento,path,signature)
            if plan['unrepairable']:event.update(status='unrepairable',reason=plan['reason'])
            else:
                lookup={c['chunk_id']:c for c in pool}
                chunks=[dict(lookup[cid]) for cid in plan['selected_chunk_ids']]
                previous_sets.append(frozenset(plan['selected_chunk_ids']))
                current={**context,'doc_id':f'{base_id}-r{number}','original_doc_id':base_id,'chunks':chunks,
                    'collections':sorted({c.get('collection','petroles') for c in chunks})}
                audit=audit_fn(auditor,current,root,signature)
                on_audit(current,audit)
                event.update(doc_id=current['doc_id'],selected_chunk_ids=plan['selected_chunk_ids'],
                    collections=current['collections'],status='recovered' if audit['approved'] else 'blocked',
                    reason=plan['reason'],audit_reason=audit.get('reason'),validation_errors=audit.get('validation_errors',[]))
        attempts.append(event)
        if (base_id,number) not in recorded:
            append_jsonl(journal,{**event,'at':utc_now()});recorded.add((base_id,number))
        print(f"[recuperação] {base_id}: tentativa {number}/{qa_cfg.max_context_refinements} -> {event['status']}",flush=True)
        if event['status'] in ('recovered','unrepairable','no_eligible_candidates'):break
    current['context_recovery']={'version':VERSION,'base_doc_id':base_id,'attempts':attempts,'recovered':bool(audit['approved'])}
    return current,audit
