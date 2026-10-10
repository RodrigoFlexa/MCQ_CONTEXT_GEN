"""Journal de candidatas, saída aceita derivada e checkpoint atômico."""
import json
import os
from datetime import datetime, timezone
from pathlib import Path

from .config import SCHEMA_VERSION


def utc_now():
    return datetime.now(timezone.utc).isoformat()


def read_jsonl(path):
    if not Path(path).exists():
        return []
    rows = []
    lines = Path(path).read_text(encoding="utf-8").splitlines()
    for index, line in enumerate(lines):
        if not line.strip():
            continue
        try:
            rows.append(json.loads(line))
        except json.JSONDecodeError:
            # Uma última linha truncada por interrupção é recuperável.
            if index != len(lines) - 1:
                raise
            raise ValueError(f"Journal truncado em {path}. Preserve-o e repare a última linha antes de retomar.")
    return rows


def append_jsonl(path, row):
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("a", encoding="utf-8") as stream:
        stream.write(json.dumps(row, ensure_ascii=False, allow_nan=False) + "\n")
        stream.flush()
        os.fsync(stream.fileno())


def atomic_json(path, value):
    path = Path(path)
    tmp = path.with_suffix(path.suffix + ".tmp")
    tmp.write_text(json.dumps(value, ensure_ascii=False, indent=2, allow_nan=False), encoding="utf-8")
    os.replace(tmp, path)


def write_jsonl(path, rows):
    path = Path(path)
    tmp = path.with_suffix(path.suffix + ".tmp")
    with tmp.open("w", encoding="utf-8") as stream:
        for row in rows:
            stream.write(json.dumps(row, ensure_ascii=False, allow_nan=False) + "\n")
    os.replace(tmp, path)


class RunStore:
    def __init__(self, cfg):
        self.cfg = cfg
        self.root = Path(cfg.output)
        self.root.mkdir(parents=True, exist_ok=True)
        self.config_path = self.root / "run_config.json"
        if self.config_path.exists():
            previous = json.loads(self.config_path.read_text(encoding="utf-8"))
            if previous.get("schema_version") != SCHEMA_VERSION:
                raise ValueError("Saída incompatível com QA v2. Use outra pasta; os resultados antigos permanecem preservados.")
            if not cfg.resume:
                raise ValueError("A pasta já contém uma execução. Use --resume ou escolha outro --output.")
            for key in ("deployment", "preparation_deployment", "judge_deployment", "effort", "embedding_model", "seed",
                        "minimum_quality", "minimum_fewshot_quality", "max_refinements",
                        "enable_cosine_filter", "enable_saturation_stop", "similarity_threshold",
                        "batch_size", "format_examples", "cross_topic_examples", "min_human_preference",
                        "max_question_words", "max_answer_words", "entropy_gain_threshold",
                        "entropy_patience", "entropy_warmup", "clusters"):
                if previous["config"].get(key) != cfg.serializable().get(key):
                    raise ValueError(f"O parâmetro {key} mudou. Compare políticas em uma nova pasta.")
            self.meta = previous
        else:
            if any((self.root / name).exists() for name in ("questoes_qa.jsonl", "candidatas_metricas.jsonl")):
                raise ValueError("Saída sem configuração de origem. Use outra pasta para preservar esses arquivos.")
            self.meta = {"schema_version": SCHEMA_VERSION, "started_at": utc_now(),
                         "config": cfg.serializable(), "status": "preparing"}
        self.meta["config"] = cfg.serializable()
        atomic_json(self.config_path, self.meta)
        state_path = self.root / "state.json"
        self.state = json.loads(state_path.read_text(encoding="utf-8")) if state_path.exists() else {
            "api_calls": 0, "calls_by_role": {}, "topics": {}}
        self.records = read_jsonl(self.root / "candidatas_metricas.jsonl")
        ids = [r["id"] for r in self.records]
        if len(ids) != len(set(ids)):
            raise ValueError("Há ids duplicados no journal de candidatas")
        self.accepted = [r for r in self.records if r.get("accepted")]
        self.rounds = read_jsonl(self.root / "metricas_por_rodada.jsonl")
        # Reconstrói a exportação se a execução parou entre journal e exportação.
        write_jsonl(self.root / "questoes_qa.jsonl", self.accepted)

    def save_state(self):
        atomic_json(self.root / "state.json", self.state)

    def reserve_round(self, topic, requested):
        state = self.state["topics"].setdefault(topic, {"rounds": 0, "requested_candidates": 0})
        state["rounds"] += 1
        state["requested_candidates"] += requested
        self.save_state()
        return state["rounds"]

    def commit(self, row):
        if any(r["id"] == row["id"] for r in self.records):
            raise ValueError(f"Id repetido no journal: {row['id']}")
        append_jsonl(self.root / "candidatas_metricas.jsonl", row)
        self.records.append(row)
        if row["accepted"]:
            self.accepted.append(row)
            append_jsonl(self.root / "questoes_qa.jsonl", row)

    def log_round(self, row):
        append_jsonl(self.root / "metricas_por_rodada.jsonl", row)
        self.rounds.append(row)

    def event(self, stage, payload):
        append_jsonl(self.root / "eventos.jsonl", {"at": utc_now(), "stage": stage, **payload})

    def status(self, status):
        self.meta.update(status=status, updated_at=utc_now(), api_calls=self.state["api_calls"],
                         calls_by_role=self.state["calls_by_role"])
        atomic_json(self.config_path, self.meta)


class CallLimitReached(RuntimeError):
    pass


class BudgetedClient:
    """Conta pedidos lógicos de todos os papéis, inclusive preparação e refino."""
    def __init__(self, backend, role, store):
        self.backend, self.role, self.store = backend, role, store

    def reserve(self):
        state = self.store.state
        if state["api_calls"] >= self.store.cfg.max_calls:
            raise CallLimitReached("Limite de chamadas atingido")
        state["api_calls"] += 1
        role_calls = state["calls_by_role"]
        role_calls[self.role] = role_calls.get(self.role, 0) + 1
        self.store.save_state()

    def complete(self, *args, **kwargs):
        self.reserve()
        result = self.backend.complete(*args, **kwargs)
        self.check_effort()
        return result

    def complete_json(self, *args, **kwargs):
        self.reserve()
        result = self.backend.complete_json(*args, **kwargs)
        self.check_effort()
        return result

    def check_effort(self):
        if "reasoning_effort" in getattr(self.backend, "_unsupported", set()):
            raise RuntimeError("O endpoint recusou reasoning_effort; a execução não continuará com esforço removido silenciosamente")
