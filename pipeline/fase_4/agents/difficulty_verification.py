from __future__ import annotations

import random

from hardaqg.llm import get_llm
from hardaqg.models import AcceptedQuestion, AttributeScores, DifficultyResult
from hardaqg.prompts.difficulty_verification import SYSTEM_PROMPT, build_prompt
from hardaqg.scoring import composite_score, is_hard_enough
from hardaqg.state import PipelineState

LETTERS = ["A", "B", "C", "D", "E"]


def difficulty_verification_agent(state: PipelineState) -> dict:
    config = state["config"]
    llm = get_llm(config, temperature=0.2).with_structured_output(DifficultyResult)

    prompt = build_prompt(
        full_question=state["validated_question"],
        chunks=state["source_chunks"],
        plan=state["generation_plan"],
    )
    result: DifficultyResult = llm.invoke([("system", SYSTEM_PROMPT), ("human", prompt)])

    d_score = composite_score(result.scores, config.weights)

    if not is_hard_enough(d_score, config.tau):
        reasons = " | ".join(
            f"{attr}: {reason}" for attr, reason in result.rationale_per_attribute.model_dump().items()
        )
        diagnostic = (
            f"Pontuação composta D={d_score:.2f} não ultrapassou o limiar τ={config.tau}. {reasons}"
        )
        return {
            "attribute_scores": result.scores,
            "composite_score": d_score,
            "failure_diagnostic": diagnostic,
            "status": "in_progress",
        }

    accepted_dict = _to_accepted_dict(state, result.scores, d_score)
    return {
        "attribute_scores": result.scores,
        "composite_score": d_score,
        "failure_diagnostic": None,
        "status": "accepted",
        "accepted_questions": state["accepted_questions"] + [accepted_dict],
    }


def _to_accepted_dict(state: PipelineState, scores: AttributeScores, d_score: float) -> dict:
    question = state["validated_question"]
    # (texto, racional, é a correta) — embaralhados como uma única unidade, para que o racional
    # de cada alternativa nunca se desalinhe do texto correspondente após a rotulação A-E.
    items = [(question.correct_answer, question.correct_rationale, True)] + [
        (d.text, d.rationale, False) for d in question.distractors
    ]
    random.shuffle(items)
    labeled = list(zip(LETTERS, items))
    correct_label = next(letter for letter, (_, _, is_correct) in labeled if is_correct)

    accepted = AcceptedQuestion(
        topic=state["config"].topic,
        stem=question.stem,
        alternatives={letter: text for letter, (text, _, _) in labeled},
        rationales={letter: rationale for letter, (_, rationale, _) in labeled},
        correct_label=correct_label,
        attribute_scores=scores,
        composite_score=round(d_score, 3),
        quality_scores=state["quality_scores"],
        attempts_used=state["attempt_count"] + 1,
        failed_criteria_history=state.get("failure_history", []),
    )
    return accepted.model_dump()
