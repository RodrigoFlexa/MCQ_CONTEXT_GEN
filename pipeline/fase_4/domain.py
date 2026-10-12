"""Adapta a recuperação e os codebooks da fase 3 para QA, sem alterar o motor MCQ."""
import hashlib
import json
import sys
from collections import Counter, defaultdict
from pathlib import Path

from .config import ROOT
from .storage import atomic_json, append_jsonl, read_jsonl
from .source_audit import audit_source, audited_document, AUDIT_VERSION, SYSTEM_PROMPT as AUDIT_PROMPT
from .multi_corpus import CONTEXT_VERSION, RETRIEVAL_VERSION
from .facet_scope import VERSION as FACET_VERSION
from .context_recovery import VERSION as RECOVERY_VERSION
from .context_composition import compose_document, material_report, VERSION as COMPOSITION_VERSION, SYSTEM_PROMPT as COMPOSITION_PROMPT

LEGACY_PATH = ROOT / "pipeline/fase_3"
if str(LEGACY_PATH) not in sys.path:
    sys.path.insert(0, str(LEGACY_PATH))
import utils_fase3 as legacy
import seed_fase3 as human_seeds
from pipeline.fase_3.topicos import TOPICOS


def fingerprint(value):
    return hashlib.sha256(json.dumps(value, sort_keys=True, ensure_ascii=False, default=str).encode()).hexdigest()


class DomainResources:
    def __init__(self, cfg, client, audit_client=None):
        self.cfg, self.client = cfg, client
        self.audit_client = audit_client or client
        self.recovery_client=client
        self.composition_client=client
        self.embedding_store=None
        self.legacy_cfg = legacy.Config(
            raiz=ROOT, out_dir=Path(cfg.output) / "dominio",
            corpus_dir=None if (cfg.corpus_txt or cfg.corpus_zip or cfg.corpus_manifest) else cfg.corpus_dir,
            corpus_txt=cfg.corpus_txt, corpus_zip=cfg.corpus_zip,
            modelo_embedding=cfg.embedding_model, seed=cfg.seed,
            alvo_palavras_trecho=cfg.chunk_words,
            min_palavras=80,max_palavras=cfg.chunk_words+max(60,cfg.chunk_words//5),
            max_linhas_trecho=max(120,cfg.chunk_words),
            n_trechos_por_documento=cfg.chunks_per_facet,
            n_documentos_por_faceta=1 if cfg.context_mode=='composed' else 2,
            n_clusters_codebook=cfg.clusters)
        self.legacy_cfg.join_document_pages=cfg.chunk_words>450
        self.pairs = {}
        self.topic_codebooks = {}
        self.chunk_lookup = {}
        self.doc_contexts = {}

    def prepare(self, selected_topics):
        # Verificação de fonte antes de carregar embeddings ou gastar chamadas de LLM.
        corpus_manifest=None;collections=None
        if self.cfg.corpus_manifest:
            from pipeline.domain_corpora.manifest import load_manifest
            corpus_manifest,collections=load_manifest(self.cfg.corpus_manifest,self.cfg.allow_sample_corpus)
            if corpus_manifest.get('partial'):
                print('[corpus] instalação parcial autorizada no instalador; confira install_report.json',flush=True)
            files=[Path(self.cfg.corpus_manifest)]
            for collection in collections:
                if collection['format']=='pages_jsonl':files.append(collection['resolved_path'])
                else:files.extend(f['resolved_path'] for f in collection['files'])
        else:files = legacy.arquivos_do_corpus(self.legacy_cfg)
        if not files and not self.cfg.corpus_zip:
            raise FileNotFoundError("Corpus Petrolês não encontrado. Configure --corpus-dir, --corpus-txt ou --corpus-zip.")
        if self.cfg.corpus_zip:
            files = [Path(self.cfg.corpus_zip)]
        if any(not f.is_file() for f in files):
            raise FileNotFoundError("Um arquivo configurado do corpus não existe")
        digests={}
        if collections:
            digests[str(Path(self.cfg.corpus_manifest).resolve())]=fingerprint(corpus_manifest)
            for collection in collections:
                if collection['format']=='pages_jsonl':digests[str(collection['resolved_path'])]=collection['sha256']
                else:digests.update({str(f['resolved_path']):f['sha256'] for f in collection['files']})
        inputs = {"corpus": [{"path": str(f.resolve()), "bytes": f.stat().st_size,
                              **({'sha256':digests[str(f.resolve())]} if collections else
                                 {'mtime_ns':f.stat().st_mtime_ns})} for f in files],
                  "scope": TOPICOS, "embedding": self.cfg.embedding_model,
                  "corpora_manifest":corpus_manifest,
                  "multisource_retrieval":RETRIEVAL_VERSION if collections else None,
                  "context_assembly":CONTEXT_VERSION if collections else None,
                  "lexical_quota_per_collection":self.cfg.lexical_candidates_per_collection,
                  "clusters": self.cfg.clusters, "seed": self.cfg.seed,
                  "context_mode":self.cfg.context_mode,
                  "composition":{"version":COMPOSITION_VERSION,"prompt":fingerprint(COMPOSITION_PROMPT),
                                 "max_tokens":self.cfg.composition_max_tokens},
                  "audit_version": AUDIT_VERSION, "audit_prompt": fingerprint(AUDIT_PROMPT),
                  "context_recovery":{"version":RECOVERY_VERSION,"attempts":self.cfg.max_context_refinements,
                                      "pool":self.cfg.context_recovery_pool},
                  "embedding_deployment":self.cfg.embedding_deployment,
                  "embedding_dimensions":self.cfg.embedding_dimensions,
                  "facet_scope_version":FACET_VERSION,"source_rerank_version":"raw-cosine-focused-v2",
                  "embedding_representation": "full_text_windows_v1", "overlap":self.cfg.embedding_overlap_tokens,
                  "retrieval": {"window_words": self.legacy_cfg.alvo_palavras_trecho,
                                "minimum_words":self.legacy_cfg.min_palavras,"maximum_words":self.legacy_cfg.max_palavras,
                                "join_document_pages":self.legacy_cfg.join_document_pages,
                                "lexical_top_k": self.legacy_cfg.top_k_lexical,
                                "mmr_lambda": self.legacy_cfg.mmr_lambda,
                                "chunks_per_document": self.legacy_cfg.n_trechos_por_documento,
                                "documents_per_facet":self.legacy_cfg.n_documentos_por_faceta}}
        signature = fingerprint(inputs)
        manifest = self.legacy_cfg.out_dir / "manifesto_qa.json"
        if manifest.exists() and json.loads(manifest.read_text(encoding="utf-8"))["signature"] != signature:
            raise ValueError("Corpus, tópicos ou modelo mudaram. Use outro --output para preservar índices e curvas anteriores.")
        atomic_json(manifest, {"signature": signature, "inputs": inputs})
        self.signature = signature
        if self.cfg.reuse_preparation_from:
            from .preparation_cache import reuse_preparation
            reuse_preparation(self.cfg.reuse_preparation_from,self.legacy_cfg.out_dir,inputs,signature)
        from .azure_embeddings import AzureFullTextEmbedder
        self.emb = AzureFullTextEmbedder(self.cfg,store=self.embedding_store)
        # Reutiliza os passos já existentes: extração de facetas -> busca lexical
        # streaming em todos os tópicos -> rerank semântico + MMR.
        from .facet_scope import ScopedFacetClient
        facets = legacy.extrair_facetas(ScopedFacetClient(self.client), TOPICOS, self.legacy_cfg,
            subtopicos_alvo=[(t,s) for t in selected_topics for s in TOPICOS[t]])
        if collections:
            from .multi_corpus import bilingual_facets, scan, plan_documents
            facets=bilingual_facets(facets,self.client,self.legacy_cfg.out_dir/'indices/facetas_bilingues.json',legacy)
            candidates=scan(facets,collections,self.legacy_cfg,legacy,self.cfg.lexical_candidates_per_collection,signature)
            atomic_json(Path(self.cfg.output)/'corpora_utilizados.json',corpus_manifest)
        else:
            legacy.descrever_corpus(self.legacy_cfg)
            legacy.varrer_corpus(facets, self.legacy_cfg)
            candidates = legacy.carregar_candidatos(self.legacy_cfg)
        grouped = defaultdict(list)
        for facet in facets:
            grouped[(facet.topico, facet.subtopico)].append(facet)
        for values in candidates.values():
            for chunk in values:
                # A mesma fonte pode aparecer em várias buscas. A faceta/score
                # de uma busca não pode sobrescrever a identidade de outra.
                self.chunk_lookup[chunk["chunk_id"]] = {k:v for k,v in chunk.items()
                    if k not in ('faceta_id','lex_score','termos_fortes')}
        coverage = []
        progress={'stage':'composing' if self.cfg.context_mode=='composed' else 'auditing',
                  'composed':0,'no_material':0,'audits':0,'approved':0,'rejected_content':0,'invalid_response':0,
                  'consecutive_invalid_responses':0,'invalid_recovery_plans':0,
                  'consecutive_invalid_recovery_plans':0}
        progress_path=Path(self.cfg.output)/'preparacao_status.json'
        audit_journal=Path(self.cfg.output)/'auditorias_contexto.jsonl'
        composition_journal=Path(self.cfg.output)/'composicoes_contexto.jsonl'
        composed_ids={r['doc_id'] for r in read_jsonl(composition_journal)}
        journaled={r['doc_id'] for r in read_jsonl(audit_journal)}
        def log_audit(context,audit):
            chunks=context['chunks'];doc_id=context['doc_id']
            status=audit.get('audit_status') or ('approved' if audit['approved'] else 'rejected_content')
            progress['audits']+=1;progress[status]+=1
            progress['consecutive_invalid_responses']=progress['consecutive_invalid_responses']+1 if status=='invalid_response' else 0
            progress.update(last_doc_id=doc_id,topic=context['topic'],subtopic=context['subtopic'])
            atomic_json(progress_path,progress)
            if doc_id not in journaled:
                append_jsonl(audit_journal,{'doc_id':doc_id,'topic':context['topic'],'subtopic':context['subtopic'],
                    'collections':context['collections'],'approved_collections':sorted({c.get('collection','petroles')
                    for c in chunks if audit['approved'] and c['chunk_id'] in audit.get('allowed_chunk_ids',[])}),
                    'approved':audit['approved'],'audit_status':status,'audit':audit})
                journaled.add(doc_id)
            reason=' '.join(str(audit.get('reason','')).split())[:300]
            label='resposta inválida' if status=='invalid_response' else 'aprovado' if audit['approved'] else 'bloqueado'
            print(f"[auditoria] {context['subtopic']}: {doc_id} -> {label} | {reason}",flush=True)
            if progress['consecutive_invalid_responses']>=self.cfg.max_consecutive_api_failures:
                raise RuntimeError('Falhas consecutivas de resposta do auditor; confira dominio/auditorias_respostas e preparacao_status.json. Não é saturação nem falta de conteúdo.')
        for topic in selected_topics:
            topic_texts = {}
            for subtopic in TOPICOS[topic]:
                pair_facets = grouped.get((topic, subtopic), [])
                plan = (plan_documents(pair_facets,candidates,self.emb,self.legacy_cfg,legacy) if collections else
                        legacy.plano_de_documentos(pair_facets, candidates, self.emb, self.legacy_cfg))
                plan_dir=self.legacy_cfg.out_dir/'planos';plan_dir.mkdir(parents=True,exist_ok=True)
                atomic_json(plan_dir/f'{fingerprint([topic,subtopic])[:16]}.json',plan)
                valid_plan=[]
                approved_sets=set();duplicate_contexts=0;content_blocked=0;invalid_audits=0
                facets_by_id={f.id:f for f in pair_facets}
                for doc in plan:
                    facet=facets_by_id[doc['faceta_id']]
                    chunks=[self.chunk_lookup[cid] for cid in doc['chunk_ids']]
                    context={'topic':topic,'subtopic':subtopic,'scope':TOPICOS[topic][subtopic],
                        'focus':facet.foco,'facet_id':facet.id,'facet_title':facet.titulo,
                        'doc_id':doc['doc_id'],'chunks':chunks,
                        'collections':sorted({c.get('collection','petroles') for c in chunks})}
                    context['context_mode']=self.cfg.context_mode
                    if self.cfg.context_mode=='composed':
                        composition=compose_document(self.composition_client,context,self.legacy_cfg.out_dir,
                                                     signature,self.cfg.composition_max_tokens)
                        status=composition['status']
                        progress['composed' if status=='ready' else status]+=1
                        progress['consecutive_invalid_responses']=progress['consecutive_invalid_responses']+1 if status=='invalid_response' else 0
                        progress.update(last_doc_id=context['doc_id'],topic=topic,subtopic=subtopic)
                        atomic_json(progress_path,progress)
                        if context['doc_id'] not in composed_ids:
                            append_jsonl(composition_journal,{'doc_id':context['doc_id'],'facet_id':facet.id,
                                'topic':topic,'subtopic':subtopic,'collections':context['collections'],
                                'status':status,'retrieved_chunks':composition['retrieved_chunks'],
                                'retrieved_words':composition['retrieved_words'],'document_words':composition['document_words'],
                                'used_chunk_ids':composition['used_chunk_ids'],'targets':composition['targets'],
                                'warnings':composition['warnings'],'factually_audited':False})
                            composed_ids.add(context['doc_id'])
                        print(f"[composição] {subtopic}: {context['doc_id']} -> {status}; "
                              f"{composition['retrieved_chunks']}/{self.cfg.chunks_per_facet} trechos, "
                              f"{composition['retrieved_words']} palavras -> documento {composition['document_words']} palavras; "
                              f"{len(composition['targets'])} alvos",flush=True)
                        for warning in composition['warnings']:print('[composição] aviso: '+warning[:350],flush=True)
                        if progress['consecutive_invalid_responses']>=self.cfg.max_consecutive_api_failures:
                            raise RuntimeError('Falhas consecutivas do compositor; confira dominio/composicoes/*.respostas.jsonl')
                        if status!='ready':
                            if status=='invalid_response':invalid_audits+=1
                            else:content_blocked+=1
                            continue
                        audit=material_report(composition)
                        context.update(document=composition['document'],context_composition=composition)
                    else:
                        audit=audit_source(self.audit_client,context,self.legacy_cfg.out_dir,signature)
                        log_audit(context,audit)
                    if self.cfg.context_mode=='audited' and not audit['approved'] and audit.get('audit_status')!='invalid_response' and self.cfg.max_context_refinements:
                        from .context_recovery import recover_context
                        context,audit=recover_context(context,audit,candidates.get(facet.id,[]),self.emb,self.legacy_cfg,
                            self.cfg,self.recovery_client,self.audit_client,self.legacy_cfg.out_dir,signature,legacy,audit_source,log_audit)
                        events=context.get('context_recovery',{}).get('attempts',[])
                        bad_plan=bool(events and events[-1]['status']=='invalid_response' and
                                      audit.get('audit_status')!='invalid_response')
                        progress['invalid_recovery_plans']+=int(bad_plan)
                        progress['consecutive_invalid_recovery_plans']=progress['consecutive_invalid_recovery_plans']+1 if bad_plan else 0
                        atomic_json(progress_path,progress)
                        if progress['consecutive_invalid_recovery_plans']>=self.cfg.max_consecutive_api_failures:
                            raise RuntimeError('Falhas consecutivas do refinador de contexto; confira dominio/recuperacoes/*/*.respostas.jsonl. Não é falta de evidência.')
                    if self.cfg.context_mode=='audited' and not audit['approved']:
                        if audit.get('audit_status')=='invalid_response':invalid_audits+=1
                        else:content_blocked+=1
                        continue
                    chunks=context['chunks']
                    doc={**doc,'doc_id':context['doc_id'],'chunk_ids':[c['chunk_id'] for c in chunks]}
                    allowed=set(audit['allowed_chunk_ids'])
                    context['chunks']=[dict(c) for c in chunks if c['chunk_id'] in allowed]
                    evidence_set=(facet.id,frozenset(c['chunk_id'] for c in context['chunks']))
                    if evidence_set in approved_sets:
                        duplicate_contexts+=1
                        print(f"[contexto] {context['doc_id']}: seleção aprovada já presente; duplicata retirada do plano",flush=True)
                        continue
                    approved_sets.add(evidence_set)
                    context['collections']=sorted({c.get('collection','petroles') for c in context['chunks']})
                    # O gerador recebe o recorte aprovado, não a obrigação de
                    # preencher todos os assuntos enumerados no foco solicitado.
                    context['requested_focus']=context['focus']
                    context['focus']=audit.get('supported_focus') or '; '.join(audit['targets'])
                    context.update(document=context['document'] if self.cfg.context_mode=='composed' else audited_document(audit),
                        source_audit=audit,corpus_signature=signature,
                        embedding_diagnostics={c['chunk_id']:self.emb.diagnostics(c['texto']) for c in context['chunks']})
                    self.doc_contexts[doc['doc_id']]=context
                    (self.legacy_cfg.out_dir/'documentos').mkdir(parents=True,exist_ok=True)
                    (self.legacy_cfg.out_dir/'documentos'/f"{doc['doc_id']}.md").write_text(context['document'],encoding='utf-8')
                    valid_plan.append(doc)
                unique={c['chunk_id']:c['texto'] for doc in valid_plan for c in self.doc_contexts[doc['doc_id']]['chunks']}
                topic_texts.update(unique)
                codebook = self.make_codebook(list(unique.values()), f"sub::{topic}::{subtopic}") if unique else None
                self.pairs[(topic, subtopic)] = {
                    "plan": valid_plan, "codebook": codebook, "facets": facets_by_id}
                coverage.append({"topic": topic, "subtopic": subtopic, "chunks": len(unique),
                                 "documents": len(valid_plan), "planned_documents":len(plan),
                                 "blocked_documents":content_blocked,
                                 "invalid_audits":invalid_audits,
                                 "context_mode":self.cfg.context_mode,
                                 "factually_audited":self.cfg.context_mode=='audited',
                                 "composed_documents":len(valid_plan) if self.cfg.context_mode=='composed' else 0,
                                 "documents_with_fewer_than_requested_chunks":sum(
                                     self.doc_contexts[d['doc_id']].get('context_composition',{}).get('retrieved_chunks',self.cfg.chunks_per_facet)<self.cfg.chunks_per_facet
                                     for d in valid_plan),
                                 "partially_supported_documents":sum(self.doc_contexts[d['doc_id']]['source_audit'].get(
                                     'coverage')=='partial' for d in valid_plan),
                                 "valid_facets":len({d['faceta_id'] for d in valid_plan}),
                                 "codebook_clusters": codebook.k if codebook else 0,
                                 "documents_by_collection":dict(Counter(
                                     c for doc in valid_plan for c in self.doc_contexts[doc['doc_id']]['collections'])),
                                 "documents_with_multiple_collections":sum(
                                     len(self.doc_contexts[doc['doc_id']]['collections'])>1 for doc in valid_plan),
                                 "recovered_documents":sum(bool(self.doc_contexts[doc['doc_id']].get(
                                     'context_recovery',{}).get('recovered')) for doc in valid_plan),
                                 "duplicate_contexts_removed":duplicate_contexts})
                atomic_json(Path(self.cfg.output)/'cobertura_dominio.json',coverage)
            if topic_texts:
                self.topic_codebooks[topic] = self.make_codebook(list(topic_texts.values()), f"topic::{topic}")
        atomic_json(Path(self.cfg.output) / "cobertura_dominio.json", coverage)
        progress.update(stage='prepared',ready_documents=len(self.doc_contexts),
                        approved_documents=len(self.doc_contexts) if self.cfg.context_mode=='audited' else 0,
                        covered_subtopics=sum(bool(r['documents']) for r in coverage))
        atomic_json(progress_path,progress)
        self.emb.salvar_cache()
        return self

    def make_codebook(self, texts, name):
        # O codebook é fixo e treinado sobre dados do domínio, nunca sobre tags
        # livres geradas pelo próprio modelo nem reagrupado a cada rodada.
        name = f"qa-v6::{self.signature}::{fingerprint(texts)}::{name}"
        if len(texts) >= 8:
            return legacy.treinar_codebook(texts, self.emb, self.legacy_cfg, nome=name)
        centers = self.emb.encode(texts)
        return legacy.Codebook(centers, {"nome": name, "n_treino": len(texts),
                                       "fonte": "chunks", "small_sample": True})

    def covered_subtopics(self, topic):
        return [s for s in TOPICOS[topic] if self.pairs[(topic, s)]["plan"]]

    def materialize(self, topic, subtopic, cursor=0, doc_id=None):
        resources = self.pairs[(topic, subtopic)]
        plan = resources["plan"]
        if not plan:
            raise ValueError(f"Nenhum documento recuperado para {topic} / {subtopic}")
        doc = next((d for d in plan if d['doc_id']==doc_id),None) if doc_id else plan[cursor % len(plan)]
        if doc is None:raise ValueError('Documento não pertence ao plano auditado')
        return dict(self.doc_contexts[doc['doc_id']])

    def documents(self,topic,subtopic):
        return [self.doc_contexts[d['doc_id']] for d in self.pairs[(topic,subtopic)]['plan']]

    def entropy(self, rows, topic, subtopic=None):
        cb = self.pairs[(topic, subtopic)]["codebook"] if subtopic else self.topic_codebooks.get(topic)
        if cb is None:
            return {"value": None, "clusters_visited": 0, "clusters_total": 0, "reliable": False}
        values = [r for r in rows if r.get("topic") == topic and
                  (subtopic is None or r.get("subtopic") == subtopic)]
        vectors = self.emb.encode([r["question"] + "\n" + r["answer"] for r in values])
        labels = cb.atribuir(vectors)
        return {"value": round(legacy.entropia_normalizada(labels, cb.k), 6),
                "clusters_visited": len(set(int(x) for x in labels)), "clusters_total": cb.k,
                "n_questions": len(values), "reliable": cb.k > 1 and not cb.meta.get("small_sample", False)}
