"""QA sobre capítulos revisados, com critérios pedagógicos em prosa e saídas pequenas."""
from .prompts import BASE

QUALITY = """
Avalie conhecimento profissional do domínio de óleo e gás, no recorte indicado.
A pessoa verá SOMENTE a pergunta. O capítulo e as fontes são material do autor/revisor.
Não exija conhecer documento, arranjo local, etiquetas de equipamento ou lista de autor.
Se fornecer dados de cenário, ainda deve ser necessário conhecimento técnico além deles.
Evite finalidade vaga, opinião como fato, várias tarefas desconexas ou conclusão já dada
no enunciado. Delimite a relação técnica sem tornar a pergunta artificial ou repetitiva.
Muitas redações e raciocínios equivalentes são aceitáveis. Conclusões essenciais incompatíveis
exigem condições para distinguir qual vale; não escolha arbitrariamente uma resposta.
Diagnóstico único precisa de sinais discriminantes; decisão precisa de critério e condições.
Não force integração nem níveis de dificuldade sem material. Conhecimento condicional é válido.
Não promova recomendação a obrigação nem inclua norma/valor sem referência aplicável.
O capítulo revisado ainda pode conter erro: confira as fontes originais. A fonte do exemplo
de estilo não sustenta fatos do novo item. Concordância entre modelos não prova correção.
"""

QUESTION_SCHEMA = """
Retorne somente o objeto JSON completo:
{"status":"ok","pergunta":"pergunta autônoma","resposta":"gabarito técnico",
"explicacao":"justificativa técnica","competencia":"relação técnica específica avaliada",
"rubrica":["critério semântico de correção"],"fontes":["E1"]}
Todos os textos são não vazios; rubrica é lista não vazia de textos. fontes é lista não
vazia dos IDs recebidos que realmente sustentam o gabarito. Não inclua IDs na pergunta
ou resposta. Respostas equivalentes são aceitas; a rubrica não é lista incidental do autor.
Se falta material para um item válido, retorne {"status":"insuficiente","motivo":"lacuna concreta"}.
Não inclua metadados de execução, julgamentos ou afirmação de aprovação.
"""

GENERATE = BASE + QUALITY + """
Crie UMA questão aberta a partir do capítulo técnico revisado e das fontes.
Escolha uma competência ainda não coberta pelos itens anteriores, com núcleo corrigível.
Use exemplos próprios/externos apenas para qualidade de apresentação. Não copie fatos,
cenário ou gabarito. Pode usar cenário hipotético explicitado, com consequências sustentadas.
""" + QUESTION_SCHEMA

NUCLEUS = BASE + QUALITY + """
Você não recebe o gabarito do autor. Resolva a pergunta com o capítulo e os trechos originais.
Explique o núcleo esperado, condições faltantes, alternativas legítimas e limites de suporte.
Se não há evidência suficiente, explicite a lacuna. Não tente adivinhar a intenção do autor.
Retorne somente JSON {"resposta":"resolução técnica independente com ressalvas necessárias"}.
"""

JUDGE = BASE + QUALITY + """
Você é o juiz técnico e pedagógico. Examine pergunta, resposta, rubrica e explicação contra
as fontes originais, não só contra o capítulo ou a lista de referências escolhida pelo autor.
Examine também a resolução feita sem acesso ao gabarito; ela pode conter erro.
Seu parecer deve sustentar a decisão com defeitos concretos ou justificativa concreta de
validade. Confira cobertura das afirmações substantivas, correção técnica, autonomia,
conhecimento exigido além da premissa e condições de uma correção justa. Não use nota global.
Falta de apoio para o núcleo exige pesquisar ou rejeitar; problemas de redação/gabarito
corrigíveis exigem refinar. Não aprove afirmação duvidosa só porque o autor a escreveu.
Retorne somente JSON completo:
{"decisao":"aprovar","parecer":"justificativa concreta da decisão","consultas":[]}
decisao aceita aprovar, refinar, pesquisar ou rejeitar. parecer é texto não vazio;
consultas é lista de até 3 textos; pesquisar exige ao menos uma consulta. Nos demais, use [].
"""

REFINE = BASE + QUALITY + """
Corrija pergunta, resposta, explicação e rubrica de forma coerente segundo o parecer.
Pode corrigir o gabarito. Não altere condições para esconder um erro nem acrescente regra
técnica sem apoio. Preserve a competência quando viável. Se o problema central é
irremediável com o material, retorne insuficiente. Toda revisão será julgada novamente.
""" + QUESTION_SCHEMA + """
Se uma busca complementar puder resolver a lacuna, pode retornar em vez da questão:
{"status":"pesquisar","motivo":"informação técnica que falta","consultas":["consulta"]}.
motivo é texto não vazio; consultas é lista de 1 a 3 textos. Não inclua pergunta/gabarito
nesse objeto de pedido. Haverá no máximo uma busca complementar por candidata.
"""

BLIND = BASE + """
Você recebe exclusivamente a pergunta. Responda com conhecimento profissional, sem adivinhar
o autor. Se falta condição decisiva, explique e apresente interpretações plausíveis.
Separe núcleo, hipótese e detalhe opcional. Não invente referência ou precisão.
Retorne somente JSON {"resposta":"resposta técnica e eventuais condições faltantes"}.
"""

ADJUDICATE = BASE + QUALITY + """
Adjudique a resposta do autor e a resposta cega contra a pergunta, rubrica e fontes.
Nem concordância prova validade nem divergência prova defeito. Paráfrase, detalhe opcional
e alternativa equivalente não são ambiguidade. Identifique núcleo incompatível igualmente
defensável, erro de referência ou erro do respondente. Não favoreça o autor.
Retorne somente JSON completo:
{"veredito":"equivalentes","parecer":"justificativa com fundamento técnico"}
veredito aceita equivalentes, parcial_sem_contradicao, erro_respondente, ambiguidade_item,
erro_referencia ou indeterminado. parecer é texto não vazio. Indeterminado não aprova.
"""

NOVELTY = BASE + """
Compare a questão nova com TODOS os itens anteriores fornecidos. Compare competência,
condições decisivas, relação técnica e núcleo da resposta/rubrica. Trocar nomes/cenário
não cria novidade; mesmo equipamento pode sustentar competências distintas.
Retorne somente JSON {"comparacoes":[{"id":"ID recebido","classe":"distinta",
"parecer":"o que se repete ou acrescenta"}]}.
Inclua exatamente uma linha por ID anterior. classe aceita redundante, sobreposicao ou
distinta. parecer é texto não vazio. Sobreposição parcial não exige descarte automático.
"""
