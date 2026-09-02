from __future__ import annotations

from hardaqg.config import QualityThresholds
from hardaqg.llm import get_llm
from hardaqg.models import ValidationResult
from hardaqg.prompts.question_validation import SYSTEM_PROMPT, build_prompt
from hardaqg.state import PipelineState

_QUALITY_LABELS = {
    "clarity": "clareza",
    "educational_relevance": "relevância educacional",
    "distractor_quality": "qualidade dos distratores",
    "semantic_diversity": "diversidade semântica",
}


def question_validation_agent(state: PipelineState) -> dict:
    config = state["config"]
    llm = get_llm(config, temperature=0.2).with_structured_output(ValidationResult)

    prompt = build_prompt(
        full_question=state["full_question"],
        accepted_questions=state["accepted_questions"],
    )
    result: ValidationResult = llm.invoke([("system", SYSTEM_PROMPT), ("human", prompt)])

    thresholds = config.quality_thresholds
    quality_ok = (
        result.quality.clarity >= thresholds.clarity_min
        and result.quality.educational_relevance >= thresholds.educational_relevance_min
        and result.quality.distractor_quality >= thresholds.distractor_quality_min
        and result.quality.semantic_diversity >= thresholds.semantic_diversity_min
    )
    # Todos os campos booleanos de ConformityCheck (exceto 'notes') precisam ser verdadeiros;
    # iterar em vez de nomear cada campo evita esquecer um se o schema crescer no futuro.
    conformity_ok = all(result.conformity.model_dump(exclude={"notes"}).values())
    passed = conformity_ok and quality_ok

    if not passed:
        diagnostic = _build_failure_diagnostic(result, thresholds)
        return {"validated_question": None, "quality_scores": result.quality, "failure_diagnostic": diagnostic}

    return {
        "validated_question": state["full_question"],
        "quality_scores": result.quality,
        "failure_diagnostic": None,
    }


def _build_failure_diagnostic(result: ValidationResult, thresholds: QualityThresholds) -> str:
    """Constrói o diagnóstico a partir dos critérios que o próprio sistema reprovou, em vez
    de usar diretamente o texto livre do LLM: esse texto costuma resumir a impressão geral do
    avaliador (podendo até dizer 'aprovada'), sem saber quais são os limiares numéricos
    configurados — quem decide aprovação é o código, comparando as notas contra esses limiares."""
    reasons: list[str] = []

    for field_name, passed_field in result.conformity.model_dump(exclude={"notes"}).items():
        if not passed_field:
            reasons.append(f"critério de conformidade '{field_name}' não atendido")

    quality_values = {
        "clarity": (result.quality.clarity, thresholds.clarity_min),
        "educational_relevance": (result.quality.educational_relevance, thresholds.educational_relevance_min),
        "distractor_quality": (result.quality.distractor_quality, thresholds.distractor_quality_min),
        "semantic_diversity": (result.quality.semantic_diversity, thresholds.semantic_diversity_min),
    }
    for field_name, (score, minimum) in quality_values.items():
        if score < minimum:
            label = _QUALITY_LABELS[field_name]
            reasons.append(f"{label} pontuou {score}, abaixo do mínimo exigido ({minimum})")

    reason_text = "; ".join(reasons) if reasons else "critério não identificado pelo sistema"
    diagnostic = f"Questão reprovada: {reason_text}."

    notes = result.conformity.notes or result.diagnostic
    if notes:
        diagnostic += f" Observações do avaliador: {notes}"

    return diagnostic
