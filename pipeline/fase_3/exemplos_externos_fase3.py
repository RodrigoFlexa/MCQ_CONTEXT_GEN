"""
exemplos_externos_fase3.py — banco pequeno e curado de exemplos de OUTRO
domínio, usados no prompt do gerador só para calibrar a LÓGICA de construção
de distratores (nunca o assunto).

Origem: AI2 Reasoning Challenge (ARC), subconjunto "Challenge" — questões de
ciências (nível fundamental/médio, EUA) selecionadas por retrieval e
co-ocorrência de palavras NÃO bastarem para resolvê-las, ou seja, os
distratores foram desenhados pra serem difíceis de eliminar por atalho
superficial. Dataset: https://huggingface.co/datasets/allenai/ai2_arc
(config "ARC-Challenge"), licença CC BY-SA 4.0 — ao redistribuir ou publicar
este arquivo fora do repositório, mantenha a atribuição e a mesma licença
para o que for derivado destas 5 questões.

Por que ARC e não mais exemplos do próprio domínio: o banco seed (fase 2) e o
repositório aprovado (fase 3) têm os PRÓPRIOS vícios de construção — é onde
achamos o vício `similaridade` e o vício `racionalizacao` (ver
utils_fase3.py). Calibrar o gerador só com exemplos que compartilham a mesma
origem tende a reproduzir os mesmos vícios. O ARC Challenge foi selecionado
como um segundo padrão de referência justamente por ser adversarial por
construção: bom pra ilustrar "distrator plausível" que não é a mesma coisa
que "distrator aleatoriamente errado".

Cada item abaixo é uma TRADUÇÃO fiel do original (mesmo raciocínio, mesma
lógica de cada distrator — nada foi facilitado nem dificultado), com o
`fonte_id` do item original em inglês para rastreabilidade.

Por que só 5, por enquanto: pedido explícito do usuário, para testar o
mecanismo antes de considerar outros datasets ou um pool maior.
"""

from __future__ import annotations

EXEMPLOS_ARC: list[dict] = [
    {
        "id": "arc-challenge-Mercury_7141558",
        "fonte": "ARC-Challenge (traduzido)",
        "fonte_id": "Mercury_7141558",
        "stem": (
            "Um engenheiro precisa calcular a energia potencial de um "
            "carrinho de montanha-russa no topo de uma rampa. Qual "
            "informação ajudaria melhor o engenheiro a determinar a "
            "energia potencial do carrinho?"
        ),
        "alternatives": [
            "A distância que o carrinho precisa percorrer.",
            "A massa do carrinho com capacidade máxima de passageiros.",
            "O peso médio do carrinho vazio.",
            "A direção em que o carrinho está se movendo.",
        ],
        "correct_answer_index": 1,
        # por que é um bom exemplo: os 4 distratores "tocam" no assunto
        # certo (massa/energia potencial), mas C erra por um detalhe
        # preciso — massa do carrinho VAZIO, não em operação real — em vez
        # de ser uma opção genericamente errada.
    },
    {
        "id": "arc-challenge-Mercury_7270305",
        "fonte": "ARC-Challenge (traduzido)",
        "fonte_id": "Mercury_7270305",
        "stem": (
            "Muitos cavalos desenvolvem uma pelagem espessa no outono e a "
            "trocam na primavera. Os cientistas não tinham certeza se a "
            "temperatura ou a quantidade de luz solar por dia (chamada "
            "fotoperíodo) causava essa mudança. Por isso, realizaram um "
            "experimento e concluíram que a mudança no fotoperíodo era "
            "responsável pelas alterações biológicas. A troca de pelagem "
            "causada por qual conjunto de condições teria permitido chegar "
            "a essa conclusão?"
        ),
        "alternatives": [
            "Fotoperíodo constante, mas temperaturas variadas.",
            "Fotoperíodo variado e temperaturas variadas.",
            "Fotoperíodo constante e temperatura constante.",
            "Fotoperíodo variado, mas temperatura constante.",
        ],
        "correct_answer_index": 3,
        # por que é um bom exemplo: testa controle de variável (isolar UMA
        # causa exige variar só ela e manter o resto constante) — as 4
        # opções são as 4 combinações lógicas possíveis, então não dá pra
        # acertar por eliminação superficial, só entendendo o motivo.
    },
    {
        "id": "arc-challenge-Mercury_7027038",
        "fonte": "ARC-Challenge (traduzido)",
        "fonte_id": "Mercury_7027038",
        "stem": (
            "Um estudante conclui que uma reação química realizada em uma "
            "investigação de sala de aula foi exotérmica. Para comunicar a "
            "validade dessa conclusão, qual seria a melhor evidência "
            "visual em uma apresentação?"
        ),
        "alternatives": [
            "Fotografias dos reagentes e dos produtos.",
            "Lista das massas dos reagentes e dos produtos.",
            "Lista do tempo do início ao fim da reação.",
            "Fotografia de uma chama produzida quando as substâncias reagiram.",
        ],
        "correct_answer_index": 3,
        # por que é um bom exemplo: cada distrator é evidência LEGÍTIMA
        # para OUTRA conclusão (massas -> conservação de massa; tempo ->
        # cinética; fotos antes/depois -> que houve reação) — nenhum é
        # bobo, mas só um evidencia especificamente liberação de calor.
    },
    {
        "id": "arc-challenge-Mercury_7174195",
        "fonte": "ARC-Challenge (traduzido)",
        "fonte_id": "Mercury_7174195",
        "stem": (
            "Uma máquina de movimento perpétuo é um dispositivo teórico "
            "que, uma vez acionado, continua funcionando sem nenhuma "
            "entrada adicional de energia. Qual afirmação explica por que "
            "é impossível projetar uma máquina de movimento perpétuo?"
        ),
        "alternatives": [
            "Energia pode ser convertida em massa.",
            "O atrito reduz a eficiência de um sistema.",
            "A quantidade de energia em um sistema permanece constante.",
            "Energia potencial pode ser convertida em energia cinética.",
        ],
        "correct_answer_index": 1,
        # por que é um bom exemplo: C e D são afirmações VERDADEIRAS, só
        # que não respondem à pergunta feita (por que é IMPOSSÍVEL) — o
        # oposto do vício "racionalizacao" que reprovamos no scorer: aqui o
        # distrator não se justifica de forma frágil, ele é uma verdade
        # real que simplesmente erra o alvo da pergunta.
    },
    {
        "id": "arc-challenge-MCAS_2015_8_7",
        "fonte": "ARC-Challenge (traduzido)",
        "fonte_id": "MCAS_2015_8_7",
        "stem": (
            "Um estudante aquece duas panelas de água no fogão, usando a "
            "potência máxima. Uma panela contém 1 L de água e a outra "
            "contém 3 L de água. O estudante aquece cada panela até a água "
            "ferver. Qual das afirmações a seguir descreve melhor o que "
            "acontece com a água nas panelas?"
        ),
        "alternatives": [
            "A água das duas panelas ferve ao mesmo tempo.",
            "A água das duas panelas ferve na mesma temperatura.",
            "Os 3 L de água ficam mais quentes que o 1 L de água antes de ferver.",
            "Os 3 L de água absorvem calor mais rápido que o 1 L de água.",
        ],
        "correct_answer_index": 1,
        # por que é um bom exemplo: distrator C explora uma confusão comum
        # e intuitiva (mais água = "mais quente") — um distrator que
        # captura um erro de raciocínio real, não um chute qualquer.
    },
]

__all__ = ["EXEMPLOS_ARC"]
