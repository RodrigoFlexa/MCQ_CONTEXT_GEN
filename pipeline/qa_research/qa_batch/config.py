"""Configuração independente da pesquisa documental em andamento."""
from dataclasses import dataclass
from pathlib import Path

from pipeline.inventario.textutil import read_json
from ..document.common import absolute

DEFAULT_CONFIG = "pipeline/qa_research/configs/qa_lote_9.json"
ROLES = ("planejamento", "geracao", "verificacao", "refinamento")


@dataclass
class Config:
    data: dict
    item: str
    document: Path
    output: Path

    @property
    def models(self):
        return self.data["models"]

    @classmethod
    def load(cls, path=DEFAULT_CONFIG, *, item=None, document=None, output=None):
        data = read_json(absolute(path))
        if not isinstance(data, dict) or data.get("schema") != "qa-batch-v1":
            raise ValueError("Configuração de lote QA ausente ou incompatível")
        if set(data.get("models", {})) != set(ROLES):
            raise ValueError("Configure os quatro modelos/efforts do lote")
        for role, spec in data["models"].items():
            if not isinstance(spec, str) or ":" not in spec:
                raise ValueError("Use deployment:effort em " + role)
            model, effort = spec.rsplit(":", 1)
            if not model or effort not in {"low", "medium", "high"}:
                raise ValueError("Deployment/effort inválido em " + role)
        for field in ("max_calls", "max_attempts", "timeout"):
            if type(data.get(field)) is not int or data[field] < 1:
                raise ValueError("Inteiro positivo esperado: " + field)
        if type(data.get("max_refinements")) is not int or not 0 <= data["max_refinements"] <= 3:
            raise ValueError("max_refinements deve estar entre zero e três")
        if set(data.get("tokens", {})) != set(ROLES):
            raise ValueError("Configure o orçamento de tokens das quatro etapas")
        for value in data["tokens"].values():
            if type(value) is not int or not 1000 <= value <= 32000:
                raise ValueError("Tokens por etapa devem estar entre 1000 e 32000")
        item = item or data["item"]
        # O ID também compõe caminhos de saída. Não aceite separadores ou '..'.
        import re
        if not isinstance(item, str) or not re.fullmatch(r"\d{2}_\d{2}", item):
            raise ValueError("Item esperado no formato 02_02")
        return cls(data, item,
                   absolute(document) if document else absolute(data["documents_root"]) / item / "documento.json",
                   absolute(output) if output else absolute(data["output_root"]) / item)
