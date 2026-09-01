from __future__ import annotations

from hardaqg.llm import get_llm
from hardaqg.models import Chunk, ChunkSelection
from hardaqg.prompts.retrieval import SYSTEM_PROMPT, build_prompt
from hardaqg.state import PipelineState


def _has_non_contiguous_spread(positions: list[int]) -> bool:
    """Verifica se as posições não formam um único bloco sequencial (proxy para
    'trechos não contíguos' no modo manual, sem busca vetorial)."""
    if len(positions) < 2:
        return False
    ordered = sorted(positions)
    return any(b - a > 1 for a, b in zip(ordered, ordered[1:]))


def retrieval_agent(state: PipelineState) -> dict:
    config = state["config"]
    all_chunks = config.chunks

    if len(all_chunks) < config.min_non_contiguous_chunks:
        return {
            "source_chunks": all_chunks,
            "failure_diagnostic": (
                "O material-fonte processado não contém trechos suficientes "
                f"({len(all_chunks)} disponíveis, mínimo {config.min_non_contiguous_chunks} exigido)."
            ),
        }

    used_chunk_ids = state.get("used_chunk_ids", [])

    llm = get_llm(config, temperature=0.3).with_structured_output(ChunkSelection)
    prompt = build_prompt(
        topic=config.topic,
        chunks=all_chunks,
        min_non_contiguous_chunks=config.min_non_contiguous_chunks,
        failure_diagnostic=state.get("failure_diagnostic"),
        used_chunk_ids=used_chunk_ids,
    )
    selection: ChunkSelection = llm.invoke([("system", SYSTEM_PROMPT), ("human", prompt)])

    by_id = {c.id: c for c in all_chunks}
    selected = [by_id[cid] for cid in selection.chunk_ids if cid in by_id]

    if not _is_sufficient(selected, config.min_non_contiguous_chunks):
        # Modo manual não tem reformulação de consulta por similaridade; a "segunda busca"
        # equivale a considerar todo o material disponível como conjunto candidato.
        selected = all_chunks

    updated_used_ids = list(dict.fromkeys(used_chunk_ids + [c.id for c in selected]))

    if not _is_sufficient(selected, config.min_non_contiguous_chunks):
        return {
            "source_chunks": selected,
            "used_chunk_ids": updated_used_ids,
            "failure_diagnostic": (
                "Não foi possível reunir um conjunto suficientemente rico e não contíguo de "
                "trechos para o tópico-alvo, mesmo utilizando todo o material disponível."
            ),
        }

    return {"source_chunks": selected, "used_chunk_ids": updated_used_ids, "failure_diagnostic": None}


def _is_sufficient(selected: list[Chunk], minimum: int) -> bool:
    positions = [c.position for c in selected]
    return len(selected) >= minimum and _has_non_contiguous_spread(positions)
