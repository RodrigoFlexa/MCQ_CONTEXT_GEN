"""Configuração explícita, sem bancos de questões ou exemplos de QA."""
from dataclasses import asdict, dataclass, field
from pathlib import Path


DEFAULT_ORIGINS = ["pipeline/inventario/" + name for name in (
    "saida_sistemas_de_lastro_v4_notas", "saida_mais_4_topicos_v4_nano_low",
    "saida_ultimos_5_topicos_v4_nano_low")]

ROLES = ("planejador", "pesquisador", "redator", "auditor", "extrator",
         "autor_qa", "respondente", "adversario", "novidade", "reranqueador")


@dataclass
class Config:
    topic: dict
    output: str
    origins: list = field(default_factory=lambda: list(DEFAULT_ORIGINS))
    manifest: str | None = None
    prepared_pack: str | None = None
    index_dir: str = "pipeline/qa_research/.local/index"
    provider: str = "azure"
    models: dict = field(default_factory=lambda: {
        role: "gpt-5-4-petrobras:low" for role in ROLES})
    initial_facets: int = 6
    max_facets: int = 12
    research_rounds: int = 3
    queries_per_round: int = 3
    chunks_per_query: int = 5
    max_evidence: int = 30
    max_repairs: int = 1
    max_atoms_per_facet: int = 12
    max_candidates: int = 40
    target_qa: int = 15
    answer_words: int = 24
    workers: int = 3
    max_calls: int = 400
    max_attempts: int = 3
    timeout: int = 180
    retrieval_mode: str = "hybrid"
    embedding_model: str = "text-embedding-3-large"
    embedding_deployment: str = "embedding-3-large-global"
    embedding_dimensions: int = 3072
    embedding_model_version: str = "1"
    embedding_batch_size: int = 64
    embedding_batch_tokens: int = 60000
    embedding_window_tokens: int = 8191
    embedding_overlap_tokens: int = 128
    embedding_max_calls: int = 50000
    lexical_candidates: int = 80
    dense_candidates: int = 80
    rerank_candidates: int = 50
    rrf_constant: int = 60
    max_chunks_per_document: int = 3
    vector_flat_threshold: int = 20000
    vector_train_size: int = 50000
    vector_nprobe: int = 32
    vector_threads: int = 4

    def validate(self):
        if not isinstance(self.topic, dict):
            raise ValueError("topic deve ser um objeto")
        for key in ("titulo", "escopo"):
            if not isinstance(self.topic.get(key), str) or not self.topic[key].strip():
                raise ValueError(f"topic.{key} deve ser texto não vazio")
        for key in ("initial_facets", "max_facets", "research_rounds", "queries_per_round",
                    "chunks_per_query", "max_evidence", "max_atoms_per_facet", "max_candidates",
                    "target_qa", "answer_words", "workers", "max_calls", "max_attempts", "timeout",
                    "embedding_dimensions", "embedding_batch_size", "embedding_batch_tokens",
                    "embedding_window_tokens", "embedding_max_calls", "lexical_candidates",
                    "dense_candidates", "rerank_candidates", "rrf_constant", "max_chunks_per_document",
                    "vector_flat_threshold", "vector_train_size", "vector_nprobe", "vector_threads"):
            if type(getattr(self, key)) is not int or getattr(self, key) < 1:
                raise ValueError(f"{key} deve ser inteiro positivo")
        if type(self.max_repairs) is not int or self.max_repairs < 0:
            raise ValueError("max_repairs deve ser inteiro não negativo")
        if self.initial_facets > self.max_facets:
            raise ValueError("initial_facets não pode exceder max_facets")
        if self.target_qa > self.max_candidates:
            raise ValueError("target_qa não pode exceder max_candidates")
        if self.provider not in ("azure", "openai"):
            raise ValueError("provider deve ser azure ou openai")
        if self.retrieval_mode not in ("hybrid", "bm25"):
            raise ValueError("retrieval_mode deve ser hybrid ou bm25")
        if self.embedding_model != "text-embedding-3-large" or self.embedding_dimensions != 3072:
            raise ValueError("Este protocolo usa text-embedding-3-large com 3072 dimensões")
        if not self.embedding_deployment.strip() or not self.embedding_model_version.strip():
            raise ValueError("Informe deployment e versão declarada dos embeddings")
        if (type(self.embedding_overlap_tokens) is not int or
                not 0 <= self.embedding_overlap_tokens < self.embedding_window_tokens <= 8191):
            raise ValueError("Janela/sobreposição dos embeddings inválidas")
        if self.embedding_batch_size > 64 or not self.embedding_window_tokens <= self.embedding_batch_tokens <= 100000:
            raise ValueError("Lotes de embeddings: até 64 entradas e 100000 tokens; devem comportar uma janela")
        if self.rerank_candidates > self.lexical_candidates + self.dense_candidates:
            raise ValueError("rerank_candidates excede candidatos possíveis")
        if self.vector_train_size < 10000:
            raise ValueError("vector_train_size deve ser >= 10000 para treinamento IVF-PQ")
        if set(self.models) != set(ROLES):
            raise ValueError(f"models deve configurar exatamente os papéis {ROLES}")
        for role, spec in self.models.items():
            parts = spec.rsplit(":", 1) if isinstance(spec, str) else []
            if len(parts) != 2 or not parts[0] or parts[1] not in ("none", "low", "medium", "high"):
                raise ValueError(f"models.{role}: use deployment:none|low|medium|high")
        output = Path(self.output).resolve()
        protected = [Path(p).resolve() for p in [*self.origins, self.index_dir]]
        if self.manifest:
            protected.append(Path(self.manifest).resolve().parent)
        if self.prepared_pack:
            protected.append(Path(self.prepared_pack).resolve())
        for path in protected:
            if output == path or output in path.parents or path in output.parents:
                raise ValueError(f"output deve ficar separado das entradas e do índice: {path}")
        if not self.origins and not self.manifest and not self.prepared_pack:
            raise ValueError("Informe origins, manifest ou prepared_pack")
        return self

    def identity(self):
        # Aumentar apenas o orçamento/concorrência não muda o experimento retomado.
        result = {k: v for k, v in asdict(self).items()
                  if k not in ("max_calls", "embedding_max_calls", "workers", "timeout", "output")}
        if self.prepared_pack:
            # A identidade do pacote entra pela assinatura verificada, não pelo
            # caminho Windows/Linux nem por entradas que não serão consultadas.
            for key in ("origins", "manifest", "index_dir", "prepared_pack"):
                result.pop(key, None)
            result["prepared_pack"] = True
        return result
