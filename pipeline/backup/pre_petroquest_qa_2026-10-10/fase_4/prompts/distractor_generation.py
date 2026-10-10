from __future__ import annotations

from hardaqg.models import Chunk, GenerationPlan

SYSTEM_PROMPT = """Você é o Agente de Geração de Distratores. Sua função é produzir quatro \
alternativas incorretas, porém plausíveis, para a questão fornecida, e o racional que \
fundamenta cada uma. As alternativas são o texto que o estudante verá; os racionais são de uso \
interno do pipeline e nunca são exibidos ao estudante."""


def build_prompt(
    *,
    stem: str,
    correct_answer: str,
    correct_rationale: str,
    chunks: list[Chunk],
    plan: GenerationPlan,
) -> str:
    chunks_block = "\n\n".join(f"[{c.id}] (arquivo: {c.source})\n{c.text}" for c in chunks)

    return f"""Enunciado da questão:
{stem}

Resposta correta:
{correct_answer}

Racional da resposta correta:
{correct_rationale}

Trechos do material-fonte:
{chunks_block}

Plano de geração (referência de contexto e nível de dificuldade):
- Inferência: {plan.connecting_inference}
- Nível cognitivo: {plan.bloom_level}
- Restrições pedagógicas definidas para esta questão: {', '.join(plan.constraints) or '(nenhuma adicional)'}

Produza exatamente quatro distratores e o racional de cada um. Regras obrigatórias:
- Cada distrator, no texto que o estudante verá, declara a conclusão incorreta correspondente \
da forma mais direta possível: sem citar os trechos do material-fonte e sem narrar os cálculos, \
passos ou o encadeamento que levariam a ela. Quando a conclusão correta for, ela própria, uma \
avaliação sobre a validade, a equivalência ou a estrutura de um argumento ou relação lógica, o \
distrator inclui o dado que a torna essa avaliação específica (a condição avaliada, o resultado \
obtido, a expressão final), sem narrar por que esse dado a comprovaria.
- Cada distrator deve diferir da resposta correta em exatamente um elemento (factual, \
inferencial ou causal). Declare esse elemento e o erro de raciocínio que o gera no racional do \
distrator, nunca no texto da alternativa.
- Cada distrator deve corresponder a um erro de raciocínio plausível e distinto dos demais: \
o tipo de engano que alguém cometeria por uma confusão específica (ex.: trocar causa por \
consequência, aplicar a inferência a um trecho errado, generalizar além do que o texto \
sustenta). Os quatro distratores não podem representar a mesma categoria de erro.
- Se a resposta correta depende de uma sequência de etapas de cálculo ou derivação (não de um \
único passo), distribua os erros dos quatro distratores entre etapas diferentes dessa \
sequência, não apenas no resultado final. Pelo menos um distrator deve resultar de um erro \
introduzido em uma etapa intermediária dessa sequência, usando o racional da resposta correta \
para identificar quais etapas existem, de modo que o valor final do distrator só possa ser \
descartado refazendo a sequência inteira, não por inspeção isolada do resultado. Declare no \
racional de cada distrator em qual etapa o erro foi introduzido e como ele se propaga até o \
resultado final; o texto da alternativa contém apenas o resultado, não esse percurso.
- Cada distrator deve compartilhar com a resposta correta o mesmo domínio conceitual, a mesma \
estrutura gramatical, o mesmo nível de especificidade e um comprimento comparável. Nenhum \
distrator pode se destacar por ser sistematicamente mais curto, mais longo ou mais genérico do \
que a resposta correta.
- Nenhum distrator pode ser eliminado por incompatibilidade evidente com o enunciado ou por \
absurdo contextual: a eliminação deve exigir resolver a questão por completo.
- Nenhum distrator pode, na prática, também ser uma resposta correta ou parcialmente aceitável \
para a questão — deve haver exatamente uma alternativa correta entre a resposta fornecida e os \
quatro distratores.
- Nenhum distrator pode conter termos absolutos ("sempre", "nunca", "todos", "nenhum", \
"totalmente", "completamente" ou equivalentes) que o tornem suspeito de estar errado só pela \
linguagem usada, independentemente do conteúdo.
- Nenhum distrator pode ser do tipo combinação (ex.: "todas as anteriores", "nenhuma das \
anteriores", "A e C estão corretas").
- Nenhum distrator pode ser identificável pela concordância gramatical com o enunciado (tempo \
verbal, número singular/plural, artigo) de um jeito que só combine com a resposta correta.
- Não use sintaxe LaTeX ou marcações de fórmula (ex.: \\text{{}}, \\subseteq, \\mathcal{{}}, \\qquad, \\frac{{}}{{}}). \
Escreva números, operadores e símbolos matemáticos diretamente como caracteres comuns (ex.: \
3+4, x², ⊆, ∈, ∪, ∩, ≤, ≥), seguindo o mesmo padrão de notação já usado na resposta correta.

Antes de finalizar os quatro distratores, teste cada um internamente considerando apenas o \
texto da alternativa, como o estudante vai lê-lo, sem o racional: tente descartá-lo sem \
resolver a questão por completo. Revise qualquer distrator que passar nesse teste, isto é, que \
seja descartável cedo, até que nenhum permaneça descartável antes da resolução completa.

Produza os quatro distratores e o racional de cada um como campos separados."""
