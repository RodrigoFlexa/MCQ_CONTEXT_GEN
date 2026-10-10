"""Prompt curto e flexível para gerar uma questão QA de FPSO."""

SYSTEM_PROMPT = """Você é especialista em operações offshore de óleo e gás, com experiência em FPSOs e sistemas submarinos. Escreva em português brasileiro claro, com terminologia usada na indústria. Gere uma questão tecnicamente correta e uma resposta objetiva. Não invente normas, limites operacionais ou dados que não foram fornecidos. Use siglas somente quando forem conhecidas no setor ou explicadas."""

QA_PROMPT = """Crie {count} questão(ões) inédita(s) de pergunta e resposta sobre o tópico abaixo.

Tópico: {topic}
Subtópico: {subtopic}
Dificuldade solicitada: {difficulty}

Defina internamente um foco técnico específico e evite repetir os focos das questões anteriores. Faça perguntas naturais e úteis para profissionais de FPSO e sistemas submarinos. Uma pergunta direta é suficiente; inclua um contexto operacional somente quando ele ajudar a avaliar o conhecimento. Não force um cenário fictício, não exagere no tamanho e não introduza nomes, valores ou falhas sem necessidade.

Nível de dificuldade:
- fácil: conceito ou procedimento essencial, resposta direta;
- média: aplicação ou interpretação de um conceito em situação comum;
- difícil: análise de interação entre sistemas, consequências ou decisão técnica, sem depender de informação obscura.

Use os exemplos apenas como referência de formato e estilo. Eles não são fontes de fatos técnicos. Exemplos de outros tópicos servem para variar a forma, não para importar seu conteúdo. As questões anteriores servem apenas para evitar repetição. Não copie frases nem troque apenas alguns substantivos.

Exemplos de formato (podem estar em outro domínio):
{format_examples}

Exemplos de QA PetroQuest de outros tópicos:
{cross_topic_examples}

Focos já usados neste lote/tópico — faça algo diferente:
{used_concepts}

Perguntas PetroQuest já geradas neste tópico — não repita o conceito central nem o cenário:
{prior_questions}

Responda somente com JSON válido no formato:
{{"items":[{{"question":"...","answer":"...","concept":"foco técnico em poucas palavras"}}]}}

Regras: cada item deve conter uma pergunta respondível sem alternativas ou texto externo e uma resposta autossuficiente. Não cite alternativas, opções, letras de gabarito, “texto acima”, “passagem”, nem peça para selecionar uma opção. Não produza múltipla escolha, distratores, explicação do processo de geração ou comentários sobre a tarefa."""


def build_prompt(*, topic, subtopic, difficulty, format_examples, cross_topic_examples, used_concepts, prior_questions=None, count=1):
    def render(rows):
        if not rows:
            return "(sem exemplos disponíveis)"
        return "\n".join(f"Pergunta: {r['question']}\nResposta: {r['answer']}" for r in rows)

    return QA_PROMPT.format(
        count=count,
        topic=topic,
        subtopic=subtopic,
        difficulty=difficulty,
        format_examples=render(format_examples),
        cross_topic_examples=render(cross_topic_examples),
        used_concepts="; ".join(used_concepts[-40:]) or "(nenhum ainda)",
        prior_questions="\n".join(f"- {q}" for q in (prior_questions or [])[-20:]) or "(nenhuma ainda)",
    )
