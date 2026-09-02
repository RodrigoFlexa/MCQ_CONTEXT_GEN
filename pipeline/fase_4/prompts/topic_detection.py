from __future__ import annotations

from hardaqg.models import Chunk

SYSTEM_PROMPT = """Você é responsável por detectar, em um material educacional, os assuntos \
pedagogicamente relevantes sobre os quais questões de múltipla escolha podem ser geradas.

Exclua explicitamente do conjunto de assuntos pertinentes qualquer conteúdo que não seja \
conteúdo pedagógico em si: avisos administrativos (datas de prova, prazos de entrega, \
compromissos), observações corriqueiras do professor sem relação com a matéria, conversas \
cotidianas, cumprimentos, e qualquer outro trecho que não ensine um conceito, fato ou \
habilidade avaliável. Registre esses trechos separadamente como excluídos, com uma breve \
justificativa de por que não são pertinentes.

Se o material não contiver nenhum conteúdo pedagogicamente relevante (por exemplo, uma aula \
inteiramente dedicada a apresentações e regras da disciplina), retorne a lista de assuntos \
incluídos vazia — isso é um resultado válido, não um erro."""


def build_prompt(chunks: list[Chunk]) -> str:
    chunks_block = "\n\n".join(f"[{c.id}] (arquivo: {c.source})\n{c.text}" for c in chunks)

    return f"""Material-fonte, já segmentado em trechos:

{chunks_block}

Identifique os assuntos pedagogicamente relevantes presentes neste material. Para cada um, \
dê um nome curto e uma descrição do que ele cobre. Não há número mínimo ou máximo de assuntos \
— use seu julgamento sobre a real diversidade de conteúdo presente, podendo ser inclusive \
zero se o material não tiver conteúdo pedagógico substantivo.

Separe também os trechos que identificar como não pertinentes (ruído administrativo, conversa \
cotidiana, etc.), com uma breve justificativa para cada exclusão."""
