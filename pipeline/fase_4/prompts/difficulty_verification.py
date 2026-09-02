from __future__ import annotations

from hardaqg.models import Chunk, FullQuestion, GenerationPlan

SYSTEM_PROMPT = """Você é o Agente de Verificação de Dificuldade. Avalie a questão fornecida em \
cinco atributos de dificuldade, cada um em escala de 1 a 3, seguindo rigorosamente os critérios \
abaixo. Para cada atributo, simule ativamente a tentativa de responder pelos atalhos descritos \
antes de atribuir a pontuação — não infira a pontuação apenas pela aparência da questão."""


def build_prompt(*, full_question: FullQuestion, chunks: list[Chunk], plan: GenerationPlan) -> str:
    chunks_block = "\n\n".join(f"[{c.id}] (arquivo: {c.source})\n{c.text}" for c in chunks)
    alt_block = "\n".join(f"  - {d.text}" for d in full_question.distractors)
    distractor_rationales_block = "\n".join(f"  - {d.rationale}" for d in full_question.distractors)

    return f"""Enunciado: {full_question.stem}

Resposta correta: {full_question.correct_answer}

Distratores:
{alt_block}

Trechos do material-fonte:
{chunks_block}

Plano de geração original e racionais registrados durante a geração (referência; não devem ser \
revelados nem assumidos como garantidos — reavalie a questão como ela está, não como foi \
planejada ou registrada):
- Cadeia de raciocínio pretendida: {'; '.join(plan.reasoning_steps)}
- Nível cognitivo pretendido: {plan.bloom_level}
- Racional registrado da resposta correta: {full_question.correct_rationale}
- Racionais registrados dos distratores:
{distractor_rationales_block}

Avalie cada atributo em escala de 1 a 3 e justifique:

L — Localização e acessibilidade da informação:
  1 = resposta obtida de um único trecho, explicitamente declarada.
  2 = requer inferência simples a partir de um único trecho, ou está distribuída de forma \
parcialmente explícita.
  3 = a resposta só é construída combinando múltiplos trechos não contíguos mediante inferência.
  Teste: tente responder usando cada trecho individualmente antes de julgar.

R — Profundidade dos passos de raciocínio:
  1 = resposta alcançável em uma única etapa inferencial.
  2 = etapas encadeadas, mas alguma pode ser pulada sem comprometer o resultado.
  3 = a resposta só é obtida percorrendo todas as etapas da cadeia, na ordem, sem pular nenhuma.
  Teste: tente responder pulando etapas da cadeia pretendida antes de julgar.

C — Complexidade do processo de resolução:
  1 = o racional é obtível por paráfrase direta do enunciado ou do texto-fonte.
  2 = o racional introduz algum conceito externo ao enunciado, mas permanece curto.
  3 = o racional é extenso e denso em conceitos não presentes no enunciado.
  Teste: gere internamente o racional necessário para resolver a questão e avalie sua extensão \
e densidade conceitual em relação ao enunciado.

G — Demanda cognitiva:
  1 = a resposta é obtida por recordação ou localização direta de informação.
  2 = a resposta exige compreensão ou aplicação, sem operações de ordem superior.
  3 = a resposta só é obtida mediante análise, avaliação ou síntese.
  Teste: tente responder por recordação pura antes de julgar; o verbo usado no enunciado não \
determina a pontuação por si só.

P — Plausibilidade dos distratores:
  1 = dois ou mais distratores são elimináveis antes da resolução completa da questão.
  2 = no máximo um distrator é eliminável antes da resolução completa da questão; os demais só \
são descartáveis resolvendo o problema inteiro.
  3 = nenhum distrator é eliminável antes da resolução completa da questão.
  Teste: avalie cada um dos quatro distratores individualmente, verificando se pode ser \
descartado sem resolver a questão por completo. Conte quantos distratores se enquadram nisso e \
pontue pela contagem: nenhum = 3, um = 2, dois ou mais = 1.

Retorne a pontuação de cada atributo (1 a 3) e a justificativa correspondente para cada um dos \
cinco atributos: L, R, C, G, P."""
