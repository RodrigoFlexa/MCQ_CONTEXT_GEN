from __future__ import annotations

from hardaqg.models import Chunk

SYSTEM_PROMPT = """Você é o Agente de Recuperação de um sistema de geração automática de \
questões difíceis. Sua função é selecionar, dentre os trechos do material-fonte fornecido, \
o subconjunto mais rico para sustentar uma questão difícil sobre o tópico-alvo."""


def build_prompt(
    *,
    topic: str,
    chunks: list[Chunk],
    min_non_contiguous_chunks: int,
    failure_diagnostic: str | None,
    used_chunk_ids: list[str],
) -> str:
    chunks_block = "\n\n".join(
        f"[{c.id}] (arquivo: {c.source}, posição {c.position})\n{c.text}" for c in chunks
    )

    retry_block = ""
    if failure_diagnostic:
        retry_block = (
            "\n\nA tentativa anterior falhou pelo seguinte motivo. Amplie ou redirecione a "
            f"seleção de trechos em relação à tentativa anterior:\n{failure_diagnostic}\n"
        )

    used_block = ""
    if used_chunk_ids:
        used_block = (
            "\n\nTrechos já usados em tentativas anteriores desta mesma questão: "
            f"{', '.join(used_chunk_ids)}. Prefira um subconjunto diferente sempre que o material \
disponível permitir, mesmo que o motivo da falha anterior não tenha sido a seleção de trechos.\n"
        )

    return f"""Tópico-alvo: {topic}

Trechos disponíveis no material-fonte:
{chunks_block}
{retry_block}{used_block}
Selecione no mínimo {min_non_contiguous_chunks} trechos não contíguos (isto é, cujas posições \
não formem um único bloco sequencial) sobre o tópico-alvo. "Suficientemente ricos" significa \
concretamente: nenhum trecho isolado, sozinho, contém a resposta de forma explícita — a resposta \
só emerge de uma inferência que combina informação de mais de um trecho selecionado. Teste antes \
de decidir: se um único trecho já responderia a uma pergunta óbvia sobre o tópico, o conjunto não \
está rico o suficiente; amplie a seleção. Retorne os IDs selecionados e uma justificativa."""
