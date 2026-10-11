"""Configuração do fluxo QA completo. Métricas de diversidade são observacionais."""
from dataclasses import asdict, dataclass, field
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
SCHEMA_VERSION = "petroquest-qa-v3"
DIFFICULTIES = ("facil", "media", "dificil")


def default_corpus():
    for name in ("corpus-SemProcessamento-publico-PetrolesCompleto",
                 "corpus-SemProcessamento-publico-PetrolesHibrido"):
        path = ROOT / "dataset" / name
        if path.is_dir():
            return path
    return ROOT / "dataset/corpus-SemProcessamento-publico-PetrolesCompleto"


@dataclass
class QAConfig:
    output: Path = ROOT / "pipeline/fase_4/saida_qa_v3_medium"
    corpus_dir: Path | None = field(default_factory=default_corpus)
    corpus_txt: list[Path] = field(default_factory=list)
    corpus_zip: Path | None = None
    external_examples: Path = ROOT / "pipeline/qa_references/data/qa_examples.jsonl"
    reviewed_seeds: Path = ROOT / "pipeline/qa_references/review/sementes_qa_candidatas.jsonl"
    human_ratings: Path = ROOT / "pipeline/fase_2/questionarios/respostas_questionario"
    deployment: str = "gpt-5-4-petrobras"
    preparation_deployment: str = "gpt-5-4-petrobras"
    judge_deployment: str = "gpt-5-4-petrobras"
    effort: str = "medium"
    embedding_model: str = "sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2"
    limit_per_topic: int = 100
    batch_size: int = 2
    max_attempts_per_topic: int = 1000
    max_calls: int = 5000
    max_consecutive_api_failures: int = 3
    max_refinements: int = 2
    format_examples: int = 8
    cross_topic_examples: int = 4
    min_human_preference: float = 0.5
    minimum_quality: float = 0.85
    minimum_technical: float = 0.90
    minimum_domain: float = 0.85
    minimum_fewshot_quality: float = 0.85
    max_question_words: int = 140
    max_answer_words: int = 250
    # Similaridade das candidatas não descarta nem refina no modo observacional.
    enable_cosine_filter: bool = False
    enable_saturation_stop: bool = False
    similarity_threshold: float = 0.85
    redundancy_neighbors: int = 8
    redundancy_confidence: float = 0.90
    filter_redundancy: bool = False
    embedding_overlap_tokens: int = 16
    coverage_fraction: float = 0.50
    minimum_subtopic_candidates: int = 12
    novelty_window: int = 30
    novelty_patience: int = 2
    minimum_novelty_yield: float = 0.10
    recovery_candidates: int = 12
    entropy_gain_threshold: float = 0.005
    entropy_patience: int = 6
    entropy_warmup: int = 12
    clusters: int = 24
    seed: int = 42
    resume: bool = False
    prepare_only: bool = False
    topics: list[str] | None = None

    def validate(self):
        import math
        for name,value in self.serializable().items():
            if isinstance(value,float) and not math.isfinite(value):
                raise ValueError(f'O parâmetro {name} precisa ser finito')
        if self.effort not in ('low','medium','high'):
            raise ValueError('Effort suportado nesta rodada: low, medium ou high')
        if min(self.limit_per_topic, self.batch_size, self.max_attempts_per_topic, self.max_calls) < 1:
            raise ValueError("Metas, tamanho de lote e limites técnicos devem ser positivos")
        if self.max_refinements < 0 or self.format_examples < 1 or self.cross_topic_examples < 1:
            raise ValueError("Exemplos devem ser positivos; refinamentos não podem ser negativos")
        if min(self.entropy_patience, self.entropy_warmup, self.max_consecutive_api_failures) < 1 or self.clusters < 2:
            raise ValueError("Aquecimento, paciência e limite de falhas devem ser positivos; clusters >= 2")
        if not 0 <= self.similarity_threshold <= 1:
            raise ValueError("O limiar de cosine deve estar entre 0 e 1")
        if not 0 <= self.minimum_quality <= self.minimum_fewshot_quality <= 1:
            raise ValueError("Notas de aprovação e few-shot devem estar em [0, 1]")
        if min(self.redundancy_neighbors, self.minimum_subtopic_candidates, self.novelty_window,
               self.novelty_patience, self.recovery_candidates) < 1:
            raise ValueError("Janelas, vizinhos e exploração mínima devem ser positivos")
        for value in (self.coverage_fraction, self.minimum_novelty_yield, self.redundancy_confidence,
                      self.minimum_technical, self.minimum_domain):
            if not 0 <= value <= 1:
                raise ValueError("Frações e notas precisam estar em [0, 1]")
        if self.embedding_overlap_tokens < 0:
            raise ValueError("Sobreposição de embeddings não pode ser negativa")
        if self.entropy_gain_threshold < 0 or min(self.max_question_words,self.max_answer_words)<1:
            raise ValueError('Ganho de entropia não pode ser negativo; limites de texto devem ser positivos')

    def serializable(self):
        return {k: str(v) if isinstance(v, Path) else
                [str(x) for x in v] if k == "corpus_txt" else v
                for k, v in asdict(self).items()}
