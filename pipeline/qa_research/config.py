"""Configuração explícita, sem bancos de questões ou exemplos de QA."""
from dataclasses import asdict, dataclass, field
from pathlib import Path


DEFAULT_ORIGINS = ["pipeline/inventario/" + name for name in (
    "saida_sistemas_de_lastro_v4_notas", "saida_mais_4_topicos_v4_nano_low",
    "saida_ultimos_5_topicos_v4_nano_low")]

ROLES = ("planejador", "pesquisador", "redator", "auditor", "extrator",
         "autor_qa", "respondente", "adversario", "novidade")


@dataclass
class Config:
    topic: dict
    output: str
    origins: list = field(default_factory=lambda: list(DEFAULT_ORIGINS))
    manifest: str | None = None
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

    def validate(self):
        if not isinstance(self.topic, dict):
            raise ValueError("topic deve ser um objeto")
        for key in ("titulo", "escopo"):
            if not isinstance(self.topic.get(key), str) or not self.topic[key].strip():
                raise ValueError(f"topic.{key} deve ser texto não vazio")
        for key in ("initial_facets", "max_facets", "research_rounds", "queries_per_round",
                    "chunks_per_query", "max_evidence", "max_atoms_per_facet", "max_candidates",
                    "target_qa", "answer_words", "workers", "max_calls", "max_attempts", "timeout"):
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
        for path in protected:
            if output == path or output in path.parents or path in output.parents:
                raise ValueError(f"output deve ficar separado das entradas e do índice: {path}")
        if not self.origins and not self.manifest:
            raise ValueError("Informe origins ou manifest")
        return self

    def identity(self):
        # Aumentar apenas o orçamento/concorrência não muda o experimento retomado.
        return {k: v for k, v in asdict(self).items()
                if k not in ("max_calls", "workers", "timeout", "output")}
