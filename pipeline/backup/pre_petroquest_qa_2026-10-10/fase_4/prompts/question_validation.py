from __future__ import annotations

from hardaqg.models import FullQuestion

SYSTEM_PROMPT = """Você é o Agente de Validação de Questão. Avalie a questão quanto a critérios \
de conformidade (binários) e de qualidade (escala de 1 a 3).

Para cada critério de qualidade, aplique o teste operacional descrito antes de atribuir uma \
pontuação. Não se deixe enganar por características superficiais (vocabulário sofisticado, \
enunciado longo, alternativas bem escritas): julgue pelo que a questão efetivamente exige do \
estudante, não pela aparência dela."""


def build_prompt(*, full_question: FullQuestion, accepted_questions: list[dict]) -> str:
    alt_block = "\n".join(
        f"  - {d.text} (difere por: {d.difference_description})" for d in full_question.distractors
    )
    accepted_block = "\n".join(f"- {q['stem']}" for q in accepted_questions) or "(nenhuma ainda)"

    return f"""Enunciado: {full_question.stem}

Resposta correta: {full_question.correct_answer}

Distratores:
{alt_block}

Questões já aceitas no lote (verifique sobreposição de conteúdo ou formulação):
{accepted_block}

Avalie os critérios abaixo.

## 1. Critérios de conformidade (binários; reprovação imediata se algum for falso)

- **single_correct_answer**: exatamente uma alternativa está correta (não zero, não mais de uma).
- **no_inappropriate_content**: sem conteúdo ofensivo, perigoso ou impróprio para uso educacional.
- **no_implausible_distractor**: nenhum distrator é eliminável sem conhecimento do domínio (ex.: \
absurdo de contexto, categoria completamente diferente da resposta correta).
- **no_grammatical_clue**: nenhuma alternativa é entregue por concordância gramatical com o \
enunciado (ex.: singular/plural, artigo, tempo verbal que só combina com a correta).
- **no_absolute_terms**: nenhuma alternativa usa termos absolutos ("sempre", "nunca", "todos", \
"nenhum") que a tornem suspeita de estar errada só pela linguagem, independente do conteúdo.
- **no_length_imbalance**: as alternativas têm comprimento e nível de detalhe comparáveis; a \
correta não se destaca por ser sistematicamente mais longa ou mais específica.
- **no_combination_alternatives**: nenhuma alternativa é do tipo combinação (ex.: "todas as \
anteriores", "A e C estão corretas").

## 2. Critérios de qualidade (escala de 1 a 3 cada)

**clarity** — clareza do enunciado e das alternativas:
  1 = ambígua: mais de uma interpretação possível, erro que afeta o sentido, ou informação \
essencial faltando.
  2 = clara: sentido único, gramática correta, sem ambiguidade que afete a interpretação.
  3 = exemplar: precisão máxima em enunciado e alternativas, linguagem adequada ao nível, nada \
faltando.

**educational_relevance** — relevância educacional do conteúdo avaliado:
  1 = irrelevante: testa detalhe administrativo ou contextual (nome, data, formato, opinião \
pessoal do professor), não testa conteúdo.
  2 = parcialmente relevante: toca um assunto real, mas de forma genérica ou superficial, sem \
exigir compreensão de um conceito-chave.
  3 = relevante: avalia compreensão de um conceito central, relação ou aplicação de um assunto \
substantivo.
  Teste: esta questão poderia aparecer em qualquer aula, de qualquer assunto? Se sim, pontuação \
baixa, independente do quão bem escrita esteja.

**distractor_quality** — qualidade dos distratores:
  1 = dois ou mais distratores são fracos, elimináveis sem qualquer conhecimento do domínio.
  2 = exatamente um distrator é fraco; ou nenhum é fraco, mas nem todos capturam um erro de \
raciocínio específico e diferente dos demais.
  3 = nenhum distrator é fraco, e cada um captura um erro de raciocínio específico e diferente \
dos demais, informativo sobre qual tipo de equívoco o estudante cometeu.
  Teste: avalie cada um dos quatro distratores individualmente quanto à eliminabilidade sem \
conhecimento de domínio. Conte quantos são fracos: dois ou mais define pontuação 1; exatamente \
um define pontuação 2. Se nenhum for fraco, verifique se os quatro, comparados entre si, \
capturam erros de raciocínio distintos e diagnosticáveis: se sim, pontue 3; se não, pontue 2.

**semantic_diversity** — diversidade CONCEITUAL entre as alternativas (não diversidade textual):
  1 = duas ou mais alternativas representam essencialmente a mesma ideia ou o mesmo erro \
conceitual, mudando apenas a redação — quem entende o conceito não consegue diferenciá-las \
pelo conteúdo, só pela forma como foram escritas.
  2 = as alternativas cobrem posições conceituais diferentes, mas alguma se sobrepõe \
parcialmente a outra em significado.
  3 = cada alternativa representa uma posição conceitual distinta e mutuamente exclusiva — um \
erro de raciocínio específico e diferente por alternativa.
  Atenção: semelhança textual entre as alternativas (mesma estrutura gramatical, mesmo domínio, \
diferindo por um único elemento) NÃO deve ser penalizada aqui: ela é uma forma legítima de \
impedir que a questão seja respondida por pista de superfície em vez de conteúdo. Julgue \
exclusivamente se o significado de cada alternativa é distinto, não se a redação parece parecida.

Se qualquer critério de conformidade falhar, marque a questão como reprovada (passed=false) e \
explique no diagnóstico qual critério falhou e por quê."""
