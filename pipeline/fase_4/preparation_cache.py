"""Reutiliza índices anteriores verificados, preservando resultados/auditorias."""
import json
import shutil
from pathlib import Path

from .storage import atomic_json


def reuse_preparation(source,target,inputs,signature):
    source=Path(source).resolve()/'dominio';target=Path(target).resolve()
    if source==target:raise ValueError('Reutilização exige uma nova pasta de saída')
    old=json.loads((source/'manifesto_qa.json').read_text(encoding='utf-8'))
    stable=('corpus','scope','embedding','corpora_manifest','multisource_retrieval','context_assembly',
            'lexical_quota_per_collection','clusters','seed','embedding_representation','overlap','retrieval',
            'facet_scope_version','embedding_deployment','embedding_dimensions')
    for key in stable:
        if old['inputs'].get(key)!=inputs.get(key):raise ValueError('Preparação anterior incompatível: '+key)
    if not inputs.get('corpora_manifest'):raise ValueError('Reutilização automática requer manifesto multicorpus')
    candidates=source/'indices/candidatos_multicorpus.jsonl'
    meta=source/'indices/candidatos_multicorpus.meta.json'
    facets=source/'indices/facetas.jsonl';translations=source/'indices/facetas_bilingues.json'
    if not all(p.is_file() for p in (candidates,meta,facets,translations)):
        raise FileNotFoundError('A preparação anterior não concluiu facetas/traduções/varredura')
    # Recalcula a assinatura de busca antiga antes de aceitar o índice pronto.
    from .multi_corpus import bilingual_facets, RETRIEVAL_VERSION
    from .domain import legacy, fingerprint
    facet_rows=[json.loads(line) for line in facets.read_text(encoding='utf-8').splitlines() if line.strip()]
    facet_objects=[legacy.Faceta(**{k:v for k,v in r.items() if k!='subtopico_id'}) for r in facet_rows]
    class NoCalls:
        def complete_json(self,*args,**kwargs):raise ValueError('Traduções anteriores incompletas')
    bilingual=bilingual_facets(facet_objects,NoCalls(),translations,legacy)
    from dataclasses import asdict
    expected=fingerprint({'signature':old['signature'],'facets':[asdict(f) for f in bilingual],
        'version':RETRIEVAL_VERSION,'quota':inputs['lexical_quota_per_collection']})
    if json.loads(meta.read_text(encoding='utf-8')).get('signature')!=expected:
        raise ValueError('Assinatura do índice anterior não confere')
    copies=('indices/facetas.jsonl','indices/facetas_bilingues.json','indices/candidatos_multicorpus.jsonl')
    reused=[]
    for relative in copies:
        original=source/relative;dest=target/relative
        if not original.is_file():continue
        if dest.exists():continue
        dest.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(original,dest);reused.append(relative)
    # O índice depende da recuperação, não do prompt do auditor alterado.
    translated=fingerprint({'signature':signature,'facets':[asdict(f) for f in bilingual],
        'version':RETRIEVAL_VERSION,'quota':inputs['lexical_quota_per_collection']})
    new_meta=json.loads(meta.read_text(encoding='utf-8'));new_meta['signature']=translated
    target_meta=target/'indices/candidatos_multicorpus.meta.json'
    if not target_meta.exists():atomic_json(target_meta,new_meta)
    atomic_json(target/'preparacao_reutilizada.json',{'source':str(source),'files':reused,
        'source_signature':old['signature'],'target_signature':signature,'audits_reused':False})
    print('[corpus] facetas e índice lexical anteriores verificados; varredura reutilizada',flush=True)
