"""Retomada conservadora da versão já executada no servidor."""
from pipeline.inventario.textutil import read_json

from . import contracts as C
from .inputs import digest


# Única implementação anterior auditada para este reparo. Não aceitar qualquer
# alteração de código: tópico, documento, modelos e tokens precisam ser idênticos.
LEGACY_IMPLEMENTATIONS = frozenset({
    "e2b5fea17e61f21e178afeb2ef663f7a342ff112c64ec56da6e4652b393efbe9",
})
TERMINAL = frozenset({"aprovado_modelo", "planejamento_insuficiente",
                      "geracao_insuficiente", "pendente_revisao"})


def compatible(previous, current):
    if previous == current:
        return True
    return (isinstance(previous, dict)
            and previous.get("implementation") in LEGACY_IMPLEMENTATIONS
            and {k: v for k, v in previous.items() if k != "implementation"}
            == {k: v for k, v in current.items() if k != "implementation"})


def checkpoints(output):
    for path in (output / "chamadas").glob("*.json"):
        value = read_json(path)
        if (not isinstance(value, dict) or value.get("key") != path.stem
                or digest(value.get("response")) != value.get("response_sha256")):
            raise ValueError("Checkpoint alterado: " + path.name)


def completed(output, identity, max_refinements):
    summary = read_json(output / "resumo.json")
    if not summary or summary.get("status") not in TERMINAL:
        return None
    for field in ("models", "contexto_sha256"):
        if summary.get(field) != identity[field]:
            raise ValueError("Resumo incompatível com a identidade: " + field)
    if summary.get("item") != identity["topic"]["id"]:
        raise ValueError("Resumo pertence a outro item")
    checkpoints(output)
    status = summary["status"]
    if status == "aprovado_modelo":
        batch = read_json(output / "qa.json")
        C.questions(batch)
        if (batch["status"] != "ok" or summary.get("questoes_publicadas") != 9
                or digest(batch) != summary.get("qa_sha256")):
            raise ValueError("Publicação QA inconsistente")
    elif status == "planejamento_insuficiente":
        if read_json(output / "planejamento.json", {}).get("status") != "insuficiente":
            raise ValueError("Planejamento insuficiente sem resultado correspondente")
    elif status == "geracao_insuficiente":
        if read_json(output / "geracao.json", {}).get("status") != "insuficiente":
            raise ValueError("Geração insuficiente sem resultado correspondente")
    else:
        round_ = summary.get("refinamentos", 0)
        repair = read_json(output / "refinamentos" / f"rodada_{round_:02}.json", {})
        if round_ < max_refinements and repair.get("status") != "insuficiente":
            return None  # Há uma rodada adicional autorizada ainda não executada.
        C.questions(read_json(output / "candidatas.json"))
    return summary
