from __future__ import annotations

from hardaqg.models import Chunk, GenerationPlan

SYSTEM_PROMPT = """Você é o Agente de Geração de Questão de um sistema de geração automática de \
questões de múltipla escolha difíceis. Sua função é escrever o enunciado, a resposta correta e \
o racional que fundamenta essa resposta, com base no plano de geração fornecido, sem produzir \
as alternativas incorretas. A resposta correta é o texto que o estudante verá como alternativa; \
o racional é de uso interno do pipeline e nunca é exibido ao estudante."""

FORBIDDEN_VERBS = "listar, definir, identificar, nomear, reconhecer, descrever, resumir"


def build_prompt(*, chunks: list[Chunk], plan: GenerationPlan, accepted_questions: list[dict]) -> str:
    chunks_block = "\n\n".join(f"[{c.id}] (arquivo: {c.source})\n{c.text}" for c in chunks)
    accepted_block = "\n".join(f"- {q['stem']}" for q in accepted_questions) or "(nenhuma ainda)"
    steps_block = "\n".join(f"  {i + 1}. {step}" for i, step in enumerate(plan.reasoning_steps))

    return f"""Trechos do material-fonte:
{chunks_block}

Plano de geração:
- Trechos combinados: {', '.join(plan.chunk_ids_used)}
- Inferência que os conecta: {plan.connecting_inference}
- Cadeia de raciocínio exigida:
{steps_block}
- Explicitação da resposta: {plan.answer_explicitness}
- Nível cognitivo (Bloom): {plan.bloom_level} — {plan.bloom_rationale}
- Restrições pedagógicas: {', '.join(plan.constraints) or '(nenhuma adicional)'}

Questões já aceitas neste lote (não se aproxime delas):
{accepted_block}

Escreva o enunciado da questão, a resposta correta e o racional da resposta correta. Regras \
obrigatórias:
- Não reproduza nenhuma sentença ou expressão literal dos trechos selecionados.
- Não copie nenhum exemplo, atividade, cenário ou caso apresentado no material, mesmo \
reformulado com palavras ou dados diferentes; o cenário e os dados da questão devem ser \
inventados especificamente para ela. Isso vale em particular para dados numéricos: invente um \
conjunto de valores novo, diferente de qualquer exemplo, tabela ou lista presente nos trechos. \
O que deve vir do material é o procedimento ou conceito a ser aplicado, não o exemplo específico \
usado para ensiná-lo.
- Não explicite no enunciado nenhuma das etapas intermediárias da cadeia de raciocínio.
- É proibido usar no enunciado os seguintes verbos, ou operações mentais associadas a eles: \
{FORBIDDEN_VERBS}.
- O enunciado deve exigir exclusivamente a operação cognitiva definida no plano \
({plan.bloom_level}).
- Trocar um verbo proibido por um sinônimo sofisticado não satisfaz esse requisito: o que \
importa é a operação mental que o estudante precisa executar para responder, não a \
formulação da pergunta. Um enunciado com vocabulário elaborado que ainda assim seja \
respondível por recordação direta continua sendo uma violação desta regra.
- A resposta correta é a conclusão do plano aplicada a este cenário, expressa da forma mais \
direta possível: sem citar os trechos do material-fonte e sem narrar os cálculos, passos ou o \
encadeamento que levam a ela. Quando essa conclusão for, ela própria, uma avaliação sobre a \
validade, a equivalência ou a estrutura de um argumento ou relação lógica, inclua nela o dado \
que a torna essa avaliação específica (a condição avaliada, o resultado obtido, a expressão \
final), sem narrar por que esse dado a comprova.
- Apesar de curta, a resposta correta permanece amarrada aos elementos específicos do cenário \
do enunciado (os dados, entidades, valores ou condições nele introduzidos): ela não pode ficar \
intercambiável com a resposta de uma questão genérica sobre o mesmo tópico.
- Não use nela termos absolutos ("sempre", "nunca", "todos", "nenhum", "totalmente", \
"completamente" ou equivalentes).
- Não use sintaxe LaTeX ou marcações de fórmula (ex.: \\text{{}}, \\subseteq, \\mathcal{{}}, \\qquad, \\frac{{}}{{}}). \
Escreva números, operadores e símbolos matemáticos diretamente como caracteres comuns (ex.: \
3+4, x², ⊆, ∈, ∪, ∩, ≤, ≥).

Além do enunciado e da resposta correta, produza o racional da resposta correta: a \
argumentação que liga o enunciado à conclusão, incluindo a referência aos trechos combinados e \
os valores e passos intermediários de qualquer cálculo ou derivação. A resposta correta e o \
racional compartilham a mesma conclusão; o que não se repete entre os dois é a citação dos \
trechos-fonte e a narração dos cálculos, passos ou do encadeamento que levam a ela.

Produza o enunciado, a resposta correta e o racional da resposta correta como campos \
separados."""
