from __future__ import annotations

from hardaqg.models import Chunk

SYSTEM_PROMPT = """Você é o Agente de Design Pedagógico de um sistema de geração automática de \
questões de múltipla escolha difíceis. Sua função é produzir um PLANO DE GERAÇÃO em linguagem \
natural que servirá de base para os agentes seguintes. Não escreva o enunciado da questão."""


_GROUNDING_INSTRUCTIONS = {
    "restrito": (
        "- A inferência deve ser derivável exclusivamente dos trechos listados acima: não "
        "introduza fatos, dados ou relações que não estejam neles, mesmo que sejam de "
        "conhecimento geral do domínio. Essa restrição é sobre fatos, conceitos e relações do "
        "domínio, não sobre valores numéricos de exemplo: números, nomes e cenários usados para "
        "instanciar um procedimento ensinado no material podem sempre ser inventados livremente, "
        "desde que o procedimento ou conceito aplicado a eles venha do material."
    ),
    "complementar": (
        "- Os trechos são o ponto de partida obrigatório: a inferência precisa nascer deles. A "
        "partir daí, você pode complementar com conhecimento externo sobre o tópico para "
        "enriquecer ou diversificar a questão, desde que o nível de profundidade desse "
        "complemento seja compatível com o nível em que o material já aborda o assunto — não "
        "introduza detalhes muito mais avançados, técnicos ou especializados do que o material "
        "sugere."
    ),
}


def build_prompt(
    *,
    topic: str,
    chunks: list[Chunk],
    bloom_target: str,
    reasoning_steps_target: int,
    min_non_contiguous_chunks: int,
    accepted_questions: list[dict],
    failure_diagnostic: str | None,
    grounding_mode: str = "restrito",
) -> str:
    chunks_block = "\n\n".join(
        f"[{c.id}] (arquivo: {c.source}, posição {c.position})\n{c.text}" for c in chunks
    )
    accepted_block = "\n".join(f"- {q['stem']}" for q in accepted_questions) or "(nenhuma ainda)"

    retry_block = ""
    if failure_diagnostic:
        retry_block = (
            "\n\nDiagnóstico da tentativa anterior desta questão:\nEvite repetir a mesma "
            f"abordagem pedagógica que falhou pelo motivo abaixo.\n{failure_diagnostic}\n"
        )

    grounding_instruction = _GROUNDING_INSTRUCTIONS[grounding_mode]

    return f"""Tópico-alvo: {topic}

Trechos do material-fonte disponíveis:
{chunks_block}

Questões já aceitas neste lote (garanta diversidade temática e cognitiva em relação a elas):
{accepted_block}
{retry_block}
Requisitos do plano de geração:
- Combine no mínimo {min_non_contiguous_chunks} trechos não contíguos entre os disponíveis.
- Descreva explicitamente qual inferência conecta os trechos selecionados.
{grounding_instruction}
- O cenário, exemplo ou atividade usado na questão deve ser original, inventado especificamente \
para esta questão; não reutilize nenhum exemplo, atividade ou caso já apresentado no material, \
mesmo reformulado com palavras diferentes. O material deve fornecer o conceito ou procedimento \
aplicado, não o exemplo específico usado para ensiná-lo.
- Construa uma cadeia de exatamente {reasoning_steps_target} etapas de raciocínio, numeradas, \
em que cada etapa alimenta obrigatoriamente a etapa seguinte.
- Defina se a resposta estará explícita ou implícita no texto (prefira implícita para \
maximizar a dificuldade).
- O nível cognitivo da Taxonomia de Bloom exigido é: {bloom_target}. Justifique por que esse \
nível não pode ser rebaixado dado o conteúdo escolhido.

Antes de finalizar o plano, valide-o internamente com os três testes abaixo. Se o plano falhar \
em algum deles, ajuste-o até passar; não inclua esse processo de ajuste na saída, apenas \
entregue a versão final já validada.
- Teste de irredutibilidade: para cada etapa da cadeia de raciocínio, verifique se a resposta \
correta ainda seria alcançável removendo só aquela etapa. Se ainda for, a cadeia não está pronta: \
refaça-a até que a remoção de qualquer etapa individual torne a resposta correta inalcançável.
- Teste de densidade conceitual: verifique se o racional necessário para resolver a questão \
seria obtido por paráfrase direta do enunciado ou dos trechos-fonte. Se for, o plano não é \
suficientemente denso; introduza uma relação ou distinção adicional entre os trechos que \
precise ser articulada, não apenas localizada.
- Teste de recordação: tente responder à questão que este plano descreve por recordação ou \
localização direta de uma única informação, ignorando a cadeia de raciocínio planejada. Se isso \
bastar para chegar à resposta correta, o plano não atinge o nível cognitivo exigido, \
independentemente do verbo que será usado no enunciado. Refaça o plano até que a resposta só \
seja alcançável decompondo, avaliando ou sintetizando os elementos combinados.

- Liste restrições pedagógicas que o enunciado da questão deve respeitar (ex.: não citar \
trechos literais do texto-fonte, não nomear diretamente os elementos combinados). Ao definir, \
entre essas restrições, como os distratores devem errar, prefira erros que só possam ser \
descartados depois que o estudante resolver a questão combinando os trechos selecionados; \
evite sugerir um erro que contradiga isoladamente um único trecho explícito do material, pois \
esse tipo de erro é descartável sem resolver a questão por completo e compromete a \
plausibilidade dos distratores.

Produza o plano de geração estruturado."""
