"""Adapta a recuperação e os codebooks da fase 3 para QA, sem alterar o motor MCQ."""
import hashlib
import json
import sys
from collections import defaultdict
from pathlib import Path

from .config import ROOT
from .storage import atomic_json

LEGACY_PATH = ROOT / "pipeline/fase_3"
if str(LEGACY_PATH) not in sys.path:
    sys.path.insert(0, str(LEGACY_PATH))
import utils_fase3 as legacy
import seed_fase3 as human_seeds
from pipeline.fase_3.topicos import TOPICOS


def fingerprint(value):
    return hashlib.sha256(json.dumps(value, sort_keys=True, ensure_ascii=False, default=str).encode()).hexdigest()


class DomainResources:
    def __init__(self, cfg, client):
        self.cfg, self.client = cfg, client
        self.legacy_cfg = legacy.Config(
            raiz=ROOT, out_dir=Path(cfg.output) / "dominio",
            corpus_dir=None if (cfg.corpus_txt or cfg.corpus_zip) else cfg.corpus_dir,
            corpus_txt=cfg.corpus_txt, corpus_zip=cfg.corpus_zip,
            modelo_embedding=cfg.embedding_model, seed=cfg.seed,
            n_clusters_codebook=cfg.clusters)
        self.pairs = {}
        self.topic_codebooks = {}
        self.chunk_lookup = {}

    def prepare(self, selected_topics):
        # Verificação de fonte antes de carregar embeddings ou gastar chamadas de LLM.
        files = legacy.arquivos_do_corpus(self.legacy_cfg)
        if not files and not self.cfg.corpus_zip:
            raise FileNotFoundError("Corpus Petrolês não encontrado. Configure --corpus-dir, --corpus-txt ou --corpus-zip.")
        if self.cfg.corpus_zip:
            files = [Path(self.cfg.corpus_zip)]
        if any(not f.is_file() for f in files):
            raise FileNotFoundError("Um arquivo configurado do corpus não existe")
        inputs = {"corpus": [{"path": str(f.resolve()), "bytes": f.stat().st_size,
                              "mtime_ns": f.stat().st_mtime_ns} for f in files],
                  "scope": TOPICOS, "embedding": self.cfg.embedding_model,
                  "clusters": self.cfg.clusters, "seed": self.cfg.seed,
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
        self.emb = legacy.Embedder(self.legacy_cfg)
        # Reutiliza os passos já existentes: extração de facetas -> busca lexical
        # streaming em todos os tópicos -> rerank semântico + MMR.
        facets = legacy.extrair_facetas(self.client, TOPICOS, self.legacy_cfg)
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
        for topic in selected_topics:
            topic_texts = {}
            for subtopic in TOPICOS[topic]:
                pair_facets = grouped.get((topic, subtopic), [])
                plan = legacy.plano_de_documentos(pair_facets, candidates, self.emb, self.legacy_cfg)
                unique = {c["chunk_id"]: c["texto"] for f in pair_facets for c in candidates.get(f.id, [])}
                topic_texts.update(unique)
                codebook = self.make_codebook(list(unique.values()), f"sub::{topic}::{subtopic}") if unique else None
                self.pairs[(topic, subtopic)] = {
                    "plan": plan, "codebook": codebook, "facets": {f.id: f for f in pair_facets}}
                coverage.append({"topic": topic, "subtopic": subtopic, "chunks": len(unique),
                                 "documents": len(plan), "codebook_clusters": codebook.k if codebook else 0})
            if topic_texts:
                self.topic_codebooks[topic] = self.make_codebook(list(topic_texts.values()), f"topic::{topic}")
        atomic_json(Path(self.cfg.output) / "cobertura_dominio.json", coverage)
        self.emb.salvar_cache()
        return self

    def make_codebook(self, texts, name):
        # O codebook é fixo e treinado sobre dados do domínio, nunca sobre tags
        # livres geradas pelo próprio modelo nem reagrupado a cada rodada.
        name = f"qa-v2::{self.signature}::{name}"
        if len(texts) >= 8:
            return legacy.treinar_codebook(texts, self.emb, self.legacy_cfg, nome=name)
        centers = self.emb.encode(texts)
        return legacy.Codebook(centers, {"nome": name, "n_treino": len(texts),
                                       "fonte": "chunks", "small_sample": True})

    def covered_subtopics(self, topic):
        return [s for s in TOPICOS[topic] if self.pairs[(topic, s)]["plan"]]

    def materialize(self, topic, subtopic, cursor):
        resources = self.pairs[(topic, subtopic)]
        plan = resources["plan"]
        if not plan:
            raise ValueError(f"Nenhum documento recuperado para {topic} / {subtopic}")
        doc = plan[cursor % len(plan)]
        facet = resources["facets"][doc["faceta_id"]]
        consolidated = legacy.consolidar_documento(self.client, doc, facet, self.legacy_cfg)
        if not consolidated.strip():
            raise ValueError("Consolidação vazia: geração sem evidência bloqueada")
        chunks = [{k: self.chunk_lookup[cid][k] for k in
                   ("chunk_id", "arquivo", "linha_ini", "linha_fim", "texto")}
                  for cid in doc["chunk_ids"]]
        return {"topic": topic, "subtopic": subtopic, "scope": TOPICOS[topic][subtopic],
                "focus": facet.foco, "document": consolidated, "chunks": chunks,
                "doc_id": doc["doc_id"], "facet_id": facet.id, "facet_title": facet.titulo,
                "corpus_signature": self.signature}

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
