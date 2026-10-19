"""Prompts de QA, resolução independente, revisão e diversidade."""
from .prompts import BASE

GENERATE = BASE + """
# Tarefa
Crie uma pergunta aberta que avalie uma relação técnica específica ensinada no capítulo
e ainda não coberta pelos itens aprovados.

# Desenho da pergunta
O respondente verá somente o enunciado. Forneça as condições necessárias para responder
sem conhecer a publicação ou uma instalação particular. Preserve uma exigência real de
conhecimento profissional além dos dados apresentados. Escolha uma forma adequada à
competência: explicação, aplicação, comparação ou decisão justificada, por exemplo.

Defina uma resposta e critérios que aceitem explicações tecnicamente equivalentes.
Se conclusões essenciais incompatíveis forem possíveis, delimite as condições que as
distinguem. Use as fontes originais para fundamentar o gabarito. Os exemplos orientam
a apresentação. Cenários hipotéticos devem ter premissas explícitas e consequências
tecnicamente sustentadas.

# Saída
Retorne somente JSON:
{"status":"ok","pergunta":"enunciado autônomo","resposta":"gabarito técnico",
"explicacao":"justificativa técnica","competencia":"relação técnica avaliada",
"rubrica":["critério semântico de correção"],"fontes":["E1"]}
Os textos são não vazios. rubrica é lista não vazia de textos. fontes é lista não vazia
de IDs recebidos que sustentam o gabarito. Mantenha os IDs somente nos metadados, fora
da pergunta e da resposta. Se faltar material para um item válido, retorne:
{"status":"insuficiente","motivo":"lacuna concreta"}
"""

NUCLEUS = BASE + """
# Tarefa
Resolva a pergunta a partir do capítulo e dos trechos originais, sem acesso ao gabarito
do autor.

# Resposta esperada
Apresente uma solução técnica justificada, com as condições necessárias e alternativas
legítimas. Quando as fontes não bastarem ou o enunciado permitir conclusões incompatíveis,
identifique a informação que falta. A intenção presumida do autor não resolve essa lacuna.

# Saída
Retorne somente JSON:
{"resposta":"solução técnica e eventuais condições ou informações faltantes"}
resposta é texto não vazio.
"""

JUDGE = BASE + """
# Tarefa
Decida se a questão permite avaliar a competência indicada com correção técnica e
critérios de resposta justos.

# Verificação
Confira o gabarito e a explicação contra as fontes originais, inclusive condições e
alcance das afirmações. Examine se a pergunta é suficiente por si só e exige conhecimento
do domínio além das informações que já entrega.

Aceite paráfrases e raciocínios equivalentes. Se outra conclusão essencial incompatível
também for defensável, indique a condição que falta. Compare com a resolução independente,
tratando tanto ela quanto o gabarito como respostas a verificar.

# Decisão
- aprovar: a questão está sustentada e permite correção adequada.
- refinar: o material permite corrigir pergunta, gabarito, explicação ou rubrica.
- pesquisar: falta evidência necessária para decidir ou sustentar o núcleo.
- rejeitar: há defeito central que impede o uso da candidata no recorte pretendido.

# Parecer e saída
Justifique a decisão com passagens e fundamentos concretos. Ao solicitar uma alteração,
explique o problema e o resultado necessário. Preferências estilísticas não devem,
sozinhas, impedir aprovação.
Retorne somente JSON:
{"decisao":"aprovar","parecer":"justificativa concreta","consultas":[]}
parecer é texto não vazio. consultas é lista de até três textos; pesquisar exige ao
menos uma consulta. Nos demais casos, use [].
"""

REFINE = BASE + """
# Tarefa
Corrija a candidata segundo o parecer, mantendo coerência entre pergunta, resposta,
explicação e rubrica. Preserve a competência quando isso for viável.

# Correção
Resolva os defeitos de conteúdo e as condições ausentes. O gabarito pode ser corrigido.
Use as evidências para justificar as mudanças. Se faltar informação decisiva, solicite
pesquisa; se o material não permitir uma candidata válida, declare insuficiência.
A nova versão será avaliada novamente.

# Entrega
Para uma correção completa, retorne somente JSON:
{"status":"ok","pergunta":"enunciado corrigido","resposta":"gabarito corrigido",
"explicacao":"justificativa técnica","competencia":"relação técnica avaliada",
"rubrica":["critério semântico de correção"],"fontes":["E1"]}
Os textos são não vazios. rubrica é lista não vazia de textos. fontes é lista não vazia
de IDs recebidos que sustentam o gabarito. Mantenha os IDs fora da pergunta e da resposta.
Se precisar de pesquisa, retorne:
{"status":"pesquisar","motivo":"informação decisiva que falta","consultas":["consulta"]}
motivo é texto não vazio e consultas é lista de um a três textos.
Se não houver correção viável com o material, retorne:
{"status":"insuficiente","motivo":"impedimento concreto"}
"""

BLIND = BASE + """
# Tarefa
Responda à pergunta com seu conhecimento profissional do domínio.

# Resposta esperada
Apresente o núcleo da resposta e as condições relevantes. Se faltar informação decisiva,
explique o que falta e quais interpretações permanecem possíveis. Diferencie conclusão,
hipótese e detalhe opcional.

# Saída
Retorne somente JSON:
{"resposta":"resposta técnica e eventuais condições faltantes"}
resposta é texto não vazio.
"""

ADJUDICATE = BASE + """
# Tarefa
Determine o significado das concordâncias e divergências entre a resposta do autor e
a resposta cega, usando a pergunta, a rubrica e as fontes.

# Comparação
Avalie as duas respostas pelas mesmas evidências. Concordância não comprova correção;
divergência pode resultar de paráfrase, detalhe opcional, erro de uma resposta ou condição
ausente no enunciado. Identifique a diferença que importa para a competência avaliada.

# Veredito
- equivalentes: as respostas apresentam o mesmo núcleo correto.
- parcial_sem_contradicao: uma resposta é parcial, sem incompatibilidade essencial.
- erro_respondente: a resposta cega contém erro e a referência continua sustentada.
- ambiguidade_item: conclusões essenciais incompatíveis são defensáveis no enunciado.
- erro_referencia: o gabarito ou a rubrica precisam de correção.
- indeterminado: as informações disponíveis não permitem decidir.

# Saída
Retorne somente JSON:
{"veredito":"equivalentes","parecer":"fundamento técnico da classificação"}
parecer é texto não vazio. Use uma das seis classificações definidas acima.
"""

NOVELTY = BASE + """
# Tarefa
Determine se a nova questão acrescenta conhecimento avaliado em relação a cada item
anterior fornecido.

# Comparação
Compare a relação técnica, as condições decisivas e o núcleo da resposta e da rubrica.
Mudanças de nomes ou cenário não bastam para criar novidade. Questões sobre o mesmo
equipamento podem avaliar competências diferentes.

# Classificação
- redundante: repete essencialmente a competência e o núcleo de resposta.
- sobreposicao: compartilha parte do conteúdo e acrescenta uma exigência relevante.
- distinta: avalia outra relação ou competência técnica.

# Saída
Retorne somente JSON:
{"comparacoes":[{"id":"id_anterior","classe":"distinta",
"parecer":"conteúdo repetido ou acrescentado"}]}
Inclua exatamente uma comparação por ID anterior recebido. classe deve usar uma das
três classificações acima e parecer deve ser texto não vazio. Sem itens anteriores,
a lista pode ser vazia.
"""
