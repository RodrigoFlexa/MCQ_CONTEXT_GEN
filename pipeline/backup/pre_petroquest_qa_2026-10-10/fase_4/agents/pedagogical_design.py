from __future__ import annotations

from hardaqg.llm import get_llm
from hardaqg.models import GenerationPlan
from hardaqg.prompts.pedagogical_design import SYSTEM_PROMPT, build_prompt
from hardaqg.state import PipelineState


def pedagogical_design_agent(state: PipelineState) -> dict:
    config = state["config"]
    llm = get_llm(config, temperature=config.temperature).with_structured_output(GenerationPlan)

    prompt = build_prompt(
        topic=config.topic,
        chunks=state["source_chunks"],
        bloom_target=config.bloom_target,
        reasoning_steps_target=config.reasoning_steps_target,
        min_non_contiguous_chunks=config.min_non_contiguous_chunks,
        accepted_questions=state["accepted_questions"],
        failure_diagnostic=state.get("failure_diagnostic"),
        grounding_mode=config.grounding_mode,
    )
    plan: GenerationPlan = llm.invoke([("system", SYSTEM_PROMPT), ("human", prompt)])

    return {"generation_plan": plan}
