"""
Portuguese prompt templates version 1.0 for question generation.
"""

from typing import NamedTuple


class PromptTemplate(NamedTuple):
    """Container for system message and question template pair."""
    system_message: str #  basically the instructions the model should follow   
    question_template: str # the template for the question generation prompt, with placeholders for content and parameters

    #  (not used in the prompt itself, but useful for documentation)
    version: str # version of the prompt template 
    language: str # language of the prompt template 
    description: str # brief description of the prompt template 


def build_content(descricao: str, trecho: str = None) -> str:
    """Monta o bloco `{content}` do prompt para as duas condições.

    As duas condições experimentais compartilham esta função para que o
    enquadramento do assunto seja idêntico e a única variável entre elas
    seja a presença do trecho recuperado do corpus:

        instruction-only ... build_content(descricao)
        context-grounded ... build_content(descricao, trecho)
    """
    blocos = [f"Assunto:\n{descricao.strip()}"]
    if trecho:
        blocos.append(f"Trecho de referência:\n{trecho.strip()}")
    return "\n\n".join(blocos)


PORTUGUESE_V13 = PromptTemplate(
    system_message="""
Você cria questões de múltipla escolha de alta qualidade em português brasileiro com
gabarito, indicação do grau de dificuldade e justificativa da resposta correta.
 
CRITÉRIOS DE QUALIDADE (toda questão deve atender):
1. Testa RACIOCÍNIO sobre o conteúdo, não localização de fatos. Se a resposta pode
   ser obtida com Ctrl+F, REFAZER.
2. O enunciado apresenta um CONTEXTO (cenário, caso, afirmação para avaliar,
   comparação a fazer).
3. Cada distrator captura um ERRO DE RACIOCÍNIO específico que profissionais da
   indústria do petróleo cometem.
4. A posição da resposta correta deve variar entre A, B, C e D dentro do questionário.
5. Apenas conteúdo técnico e boas práticas de engenharia relacionado a indústria
   de óleo e gás, em específico para projeto, operação, manutenção, gestão,
   conformidade, logística e descomissionamento de unidades de produção
   offshore, em especial de unidades do tipo FPSO — nada sobre professor,
   instituição, empresas, fabricantes ou formato.
6. O comprimento das alternativas deve ser equilibrado entre TODAS elas (correta e
   distratores), de modo que o tamanho da alternativa não sirva de pista para a
   resposta. Não faça a correta sistematicamente mais longa nem sistematicamente
   mais curta que as demais.
7. A sobreposição de palavras-chave com o enunciado deve estar distribuída entre
   correta e distratores: a alternativa correta não deve se destacar por repetir
   termos do enunciado. Termos técnicos que precisam aparecer tanto no enunciado
   quanto nas alternativas são aceitáveis; o que se evita é que essa repetição
   entregue qual é a correta.
8. A resposta correta deve vir acompanhada de uma justificativa curta, registrada
   no campo "correct_reason" do JSON.
 
DISTRIBUIÇÃO ALVO no questionário:
- ~30% questões mais fáceis (compreensão profunda, NÃO memorização)
- ~40% questões médias (aplicação, conexão entre conceitos)
- ~30% questões difíceis (análise crítica, avaliação, síntese)
 
Confie no seu julgamento sobre como atingir esses critérios — não há um processo
rígido a seguir.
""",
    question_template="""
Gere {n_questions} questões de múltipla escolha com {n_alternatives} alternativas
cada, atendendo aos critérios de qualidade.
 
Para cada questão, indique também o grau de dificuldade ("facil", "media" ou
"dificil") e uma justificativa curta da resposta correta.
 
Conteúdo:
```
{content}
```
 
Retorne apenas o JSON:
```json
[
    {{
        "stem": "O texto da pergunta",
        "alternatives": ["Opção A", "Opção B", "Opção C", "Opção D"],
        "correct_answer_index": 2,
        "difficulty": "media",
        "correct_reason": "Justificativa curta de por que a alternativa correta está certa"
    }},
    {{
        "stem": "O texto da segunda pergunta",
        "alternatives": ["Opção A", "Opção B", "Opção C", "Opção D"],
        "correct_answer_index": 0,
        "difficulty": "dificil",
        "correct_reason": "Justificativa curta de por que a alternativa correta está certa"
    }}
]
```
""",
    version="v13.0",
    language="pt-BR",
    description=(
        "Reasoning-model criteria prompt, especializado em óleo e gás offshore/FPSO; "
        "critérios 6 e 7 reformulados para balanceamento (não banimento); "
        "schema com difficulty e correct_reason"
    ),
)


PORTUGUESE_V14 = PromptTemplate(
    system_message=PORTUGUESE_V13.system_message.replace(
        """8. A resposta correta deve vir acompanhada de uma justificativa curta, registrada
   no campo "correct_reason" do JSON.""",
        """8. A resposta correta deve vir acompanhada de uma justificativa curta, registrada
   no campo "correct_reason" do JSON.
9. NÃO concentre linguagem absolutista nos distratores. Termos como "apenas",
   "somente", "exclusivamente", "nunca", "sempre", "todos", "eliminando a
   necessidade", "dispensando", "sem considerar", "independentemente" tornam o
   distrator obviamente errado e entregam o gabarito por eliminação. Os
   distratores devem ser posições tecnicamente plausíveis e matizadas, erradas
   pelo CONTEÚDO (o erro de raciocínio que capturam), não pela forma extrema da
   redação. O padrão de linguagem (tom, hedging, quantificadores) deve ser
   indistinguível entre a alternativa correta e os distratores."""),
    question_template=PORTUGUESE_V13.question_template,
    version="v14.0",
    language="pt-BR",
    description=(
        "v13 + critério 9: proíbe concentração de marcadores absolutistas nos "
        "distratores (test-wiseness cue), exigindo paridade de linguagem entre "
        "correta e distratores"
    ),
)


PORTUGUESE_V15 = PromptTemplate(
    system_message="""
Você cria questões de múltipla escolha de alta qualidade em português brasileiro com
gabarito, indicação do grau de dificuldade e justificativa da resposta correta.

CRITÉRIOS DE QUALIDADE (toda questão deve atender):
1. Testa RACIOCÍNIO sobre o conteúdo, não localização de fatos. Se a resposta pode
   ser obtida com Ctrl+F, REFAZER.
2. O enunciado apresenta um CONTEXTO (cenário, caso, afirmação para avaliar,
   comparação a fazer).
3. Cada distrator é uma POSIÇÃO ALTERNATIVA PLAUSÍVEL — outro mecanismo, outro
   componente, outra prioridade ou outra interpretação técnica que um
   profissional da indústria do petróleo poderia defender à primeira vista —
   e captura um erro de raciocínio específico. O distrator NUNCA deve ser uma
   versão exagerada, extremada ou caricata da alternativa correta: ele erra
   pelo CONTEÚDO, não pela forma da redação.
4. PARIDADE DE LINGUAGEM entre todas as alternativas: tom, nível de nuance e
   quantificadores devem ser indistinguíveis entre a correta e os distratores.
   Termos absolutistas ("apenas", "somente", "exclusivamente", "nunca",
   "sempre", "todos", "eliminando a necessidade", "dispensando",
   "sem considerar", "independentemente") não podem se concentrar nos
   distratores. Um leitor atento NÃO deve conseguir eliminar alternativas
   apenas pelo estilo da escrita.
5. A posição da resposta correta deve variar entre A, B, C e D dentro do questionário.
6. Apenas conteúdo técnico e boas práticas de engenharia relacionado a indústria
   de óleo e gás, em específico para projeto, operação, manutenção, gestão,
   conformidade, logística e descomissionamento de unidades de produção
   offshore, em especial de unidades do tipo FPSO — nada sobre professor,
   instituição, empresas, fabricantes ou formato.
7. Comprimento das alternativas: variação natural é aceitável; o que não pode
   existir é padrão sistemático (a correta consistentemente mais longa ou mais
   curta que os distratores). NÃO alongue distratores artificialmente para
   igualar tamanhos — prefira reformular a correta ou aceitar variação.
8. A sobreposição de palavras-chave com o enunciado deve estar distribuída entre
   correta e distratores: a alternativa correta não deve se destacar por repetir
   termos do enunciado.
9. A resposta correta deve vir acompanhada de uma justificativa curta, registrada
   no campo "correct_reason" do JSON.

DISTRIBUIÇÃO ALVO no questionário:
- ~30% questões mais fáceis (compreensão profunda, NÃO memorização)
- ~40% questões médias (aplicação, conexão entre conceitos)
- ~30% questões difíceis (análise crítica, avaliação, síntese)

Confie no seu julgamento sobre como atingir esses critérios — não há um processo
rígido a seguir.
""",
    question_template=PORTUGUESE_V13.question_template,
    version="v15.0",
    language="pt-BR",
    description=(
        "Consolidação empírica: distratores como posições alternativas "
        "plausíveis (não distorções da correta), paridade de linguagem "
        "anti-absolutismo, critério de comprimento afrouxado para variação "
        "natural (sem enchimento artificial)"
    ),
)
