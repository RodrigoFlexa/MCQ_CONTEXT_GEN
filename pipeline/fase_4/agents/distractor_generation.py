from __future__ import annotations

from hardaqg.llm import get_llm
from hardaqg.models import DistractorSet, FullQuestion
from hardaqg.prompts.distractor_generation import SYSTEM_PROMPT, build_prompt
from hardaqg.state import PipelineState


def distractor_generation_agent(state: PipelineState) -> dict:
    config = state["config"]
    llm = get_llm(config, temperature=config.temperature).with_structured_output(DistractorSet)

    prompt = build_prompt(
        stem=state["question_stem"],
        correct_answer=state["correct_answer"],
        correct_rationale=state["correct_rationale"],
        chunks=state["source_chunks"],
        plan=state["generation_plan"],
    )
    result: DistractorSet = llm.invoke([("system", SYSTEM_PROMPT), ("human", prompt)])

    full_question = FullQuestion(
        stem=state["question_stem"],
        correct_answer=state["correct_answer"],
        correct_rationale=state["correct_rationale"],
        distractors=result.distractors,
    )
    return {"distractors": result.distractors, "full_question": full_question}
