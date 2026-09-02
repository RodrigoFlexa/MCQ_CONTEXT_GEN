from __future__ import annotations

from hardaqg.llm import get_llm
from hardaqg.models import QuestionDraft
from hardaqg.prompts.question_generation import SYSTEM_PROMPT, build_prompt
from hardaqg.state import PipelineState


def question_generation_agent(state: PipelineState) -> dict:
    config = state["config"]
    llm = get_llm(config, temperature=config.temperature).with_structured_output(QuestionDraft)

    prompt = build_prompt(
        chunks=state["source_chunks"],
        plan=state["generation_plan"],
        accepted_questions=state["accepted_questions"],
    )
    draft: QuestionDraft = llm.invoke([("system", SYSTEM_PROMPT), ("human", prompt)])

    return {
        "question_stem": draft.stem,
        "correct_answer": draft.correct_answer,
        "correct_rationale": draft.correct_rationale,
    }
