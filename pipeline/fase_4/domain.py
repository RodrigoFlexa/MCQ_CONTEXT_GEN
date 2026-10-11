"""Adapta a recuperação e os codebooks da fase 3 para QA, sem alterar o motor MCQ."""
import hashlib
import json
import sys
from collections import Counter, defaultdict
from pathlib import Path

from .config import ROOT
from .storage import atomic_json, append_jsonl, read_jsonl
from .source_audit import audit_source, audited_document, AUDIT_VERSION, SYSTEM_PROMPT as AUDIT_PROMPT

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
        self.legacy_cfg = legacy.Config(
            raiz=ROOT, out_dir=Path(cfg.output) / "dominio",
            corpus_dir=None if (cfg.corpus_txt or cfg.corpus_zip or cfg.corpus_manifest) else cfg.corpus_dir,
            corpus_txt=cfg.corpus_txt, corpus_zip=cfg.corpus_zip,
            modelo_embedding=cfg.embedding_model, seed=cfg.seed,
            n_clusters_codebook=cfg.clusters)
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
                  "multisource_retrieval":"multisource-bilingual-v1" if collections else None,
                  "lexical_quota_per_collection":self.cfg.lexical_candidates_per_collection,
                  "clusters": self.cfg.clusters, "seed": self.cfg.seed,
                  "audit_version": AUDIT_VERSION, "audit_prompt": fingerprint(AUDIT_PROMPT),
                  "embedding_representation": "full_text_windows_v1", "overlap":self.cfg.embedding_overlap_tokens,
                  "retrieval": {"window_words": self.legacy_cfg.alvo_palavras_trecho,
                                "lexical_top_k": self.legacy_cfg.top_k_lexical,
                                "mmr_lambda": self.legacy_cfg.mmr_lambda,
                                "chunks_per_document": self.legacy_cfg.n_trechos_por_documento}}
        signature = fingerprint(inputs)
        manifest = self.legacy_cfg.out_dir / "manifesto_qa.json"
        if manifest.exists() and json.loads(manifest.read_text(encoding="utf-8"))["signature"] != signature:
            raise ValueError("Corpus, tópicos ou modelo mudaram. Use outro --output para preservar índices e curvas anteriores.")
        atomic_json(manifest, {"signature": signature, "inputs": inputs})
        self.signature = signature
        from .embedding import FullTextEmbedder
        self.emb = FullTextEmbedder(self.legacy_cfg,self.cfg.embedding_overlap_tokens)
        # Reutiliza os passos já existentes: extração de facetas -> busca lexical
        # streaming em todos os tópicos -> rerank semântico + MMR.
        facets = legacy.extrair_facetas(self.client, TOPICOS, self.legacy_cfg,
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
                self.chunk_lookup[chunk["chunk_id"]] = chunk
        coverage = []
        audit_journal=Path(self.cfg.output)/'auditorias_contexto.jsonl'
        journaled={r['doc_id'] for r in read_jsonl(audit_journal)}
        for topic in selected_topics:
            topic_texts = {}
            for subtopic in TOPICOS[topic]:
                pair_facets = grouped.get((topic, subtopic), [])
                plan = (plan_documents(pair_facets,candidates,self.emb,self.legacy_cfg,legacy) if collections else
                        legacy.plano_de_documentos(pair_facets, candidates, self.emb, self.legacy_cfg))
                valid_plan=[]
                facets_by_id={f.id:f for f in pair_facets}
                for doc in plan:
                    facet=facets_by_id[doc['faceta_id']]
                    chunks=[self.chunk_lookup[cid] for cid in doc['chunk_ids']]
                    context={'topic':topic,'subtopic':subtopic,'scope':TOPICOS[topic][subtopic],
                        'focus':facet.foco,'facet_id':facet.id,'facet_title':facet.titulo,
                        'doc_id':doc['doc_id'],'chunks':chunks}
                    audit=audit_source(self.audit_client,context,self.legacy_cfg.out_dir,signature)
                    if doc['doc_id'] not in journaled:
                        append_jsonl(audit_journal,{'doc_id':doc['doc_id'],'topic':topic,'subtopic':subtopic,
                            'approved':audit['approved'],'audit':audit})
                        journaled.add(doc['doc_id'])
                    print(f"[auditoria] {subtopic}: {doc['doc_id']} -> {'aprovado' if audit['approved'] else 'bloqueado'}",flush=True)
                    if not audit['approved']:continue
                    allowed=set(audit['allowed_chunk_ids'])
                    context['chunks']=[dict(c) for c in chunks if c['chunk_id'] in allowed]
                    context['collections']=sorted({c.get('collection','petroles') for c in context['chunks']})
                    context.update(document=audited_document(audit),source_audit=audit,corpus_signature=signature,
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
                                 "blocked_documents":len(plan)-len(valid_plan),
                                 "valid_facets":len({d['faceta_id'] for d in valid_plan}),
                                 "codebook_clusters": codebook.k if codebook else 0,
                                 "documents_by_collection":dict(Counter(
                                     c for doc in valid_plan for c in self.doc_contexts[doc['doc_id']]['collections']))})
            if topic_texts:
                self.topic_codebooks[topic] = self.make_codebook(list(topic_texts.values()), f"topic::{topic}")
        atomic_json(Path(self.cfg.output) / "cobertura_dominio.json", coverage)
        self.emb.salvar_cache()
        return self

    def make_codebook(self, texts, name):
        # O codebook é fixo e treinado sobre dados do domínio, nunca sobre tags
        # livres geradas pelo próprio modelo nem reagrupado a cada rodada.
        name = f"qa-v3::{self.signature}::{fingerprint(texts)}::{name}"
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
