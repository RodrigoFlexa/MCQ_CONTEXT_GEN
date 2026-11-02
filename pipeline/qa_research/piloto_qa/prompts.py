from pipeline.qa_research.v3.prompts import BASE

PLAN = BASE + '''Planeje alvos de avaliação para o escopo e documento recebidos.
Uma questão avalia uma relação ou uma combinação necessária de relações. Preserve
as seis classes: conceito, mecanismo, consequencia, diagnostico, decisao, procedimento.
Proponha até limite alvos diversos e distribuídos pelos capítulos. Use as cotas de
classe como prioridade, sem inventar conhecimento para cumpri-las. Conceito é simples;
diagnóstico e decisão exigem condições discriminantes. Em composta, cada evidência
deve contribuir para a conclusão, não apenas repetir ou ilustrar a outra.
Primeiro selecione afirmações do documento, depois defina o alvo. Em evidencias,
registre bloco e trecho literalmente presente. Não use conhecimento externo.
Não inclua assunto declarado pendente. Histórico/exemplos orientam variedade e
forma, nunca fundamentação. Não copie questões históricas. Evite listas abertas,
atalhos de prudência e reformulações da mesma competência. Não otimize ROUGE ou gap.
JSON {"alvos":[{"id":"T01","tipo":"mecanismo","composicao":"simples",
"conhecimento":"relação avaliada com condições","ponte":"vazio se simples",
"afirmacoes":[{"afirmacao":"proposição suportada com condições",
"evidencias":[{"bloco":"B001","trecho":"passagem literal"}]}]}],"impedimentos":[]}.
'''

AUTHOR = BASE + '''Redija uma pergunta aberta por alvo recebido, até limite.
Não copie exemplos; eles não são suporte factual. Não altere alvo, classe ou composição.
Enunciado autônomo de até 90 palavras, com uma demanda clara. Diagnóstico e decisão
precisam de cenário com sinais suficientes; não entregue a resposta no cenário.
Resposta mínima suficiente até 60 palavras. Explicações opcionais ficam fora dela.
Cada critério essencial deve ser pedido pela pergunta, constar na resposta mínima
e ser fundamentado em trecho literal do documento ou em inferência explícita entre
os trechos. Não acrescente premissas de campo, números, normas ou exceções ausentes.
Rubrica aceita formulações tecnicamente equivalentes, não uma lista arbitrária.
Não confunda ausência de detalhe opcional com erro. Uma inferência deve declarar
suas premissas em fundamento e a ligação em inferencia. Não trate coocorrência como causa.
JSON {"questoes":[{"id":"T01","pergunta":"...?","resposta":"mínimo suficiente",
"cenario":false,"criterios":[{"id":"K1","criterio":"componente essencial",
"evidencias":[{"bloco":"B001","trecho":"literal"}],"inferencia":"vazio se direto"}],
"equivalentes":["formulação aceitável"],"erros_materiais":["contradição relevante"]}],
"impedimentos":[]}.
Em reparo, devolva somente as questões solicitadas, completas, ou deixe-as ausentes
e explique em impedimentos. Corrija a pergunta e o mínimo suficiente sem mudar o alvo.
'''

SOLVE = BASE + '''Resolva as perguntas com o contexto recebido, sem gabaritos.
Responda aos componentes pedidos com até 100 palavras. Registre ambiguidade ou
premissa faltante. Não invente medições nem condições. Não use ferramentas.
JSON {"resolucoes":[{"id":"T01","resposta":"...","ambiguidades":[]}]}.
'''

JUDGE = BASE + '''Julgue cada candidata independentemente contra o documento e seu alvo.
Para cada critério essencial e para TODAS as afirmações da resposta mínima, confira
suporte e condições. Uma inferência válida explicita premissas; plausibilidade externa
não é suporte documental. Se o mínimo contém extrapolação, peça sua remoção/reparo.
Confira correção, autonomia, resposta determinada, ausência de pistas, PT-BR, classe,
composição e variedade. Cite no parecer as evidências literais que sustentam sua decisão.
A resolução independente serve para detectar ambiguidade, não para rejeitar automaticamente
uma candidata acertada ou errada pelo resolvedor. Não selecione pela dificuldade para ele.
Compare com as candidatas do lote e com o inventário admitido: trocar o cenário sem
mudar relação, condições, conclusão e demanda não cria nova competência. Mesmo assunto
sozinho não prova duplicação. duplicada_de deve apontar a uma admitida anterior ou
anterior na ordem deste lote que você admita, sem ciclos.
Em composta, verifique se a ligação exige as duas relações: caso uma só resolva toda
a demanda, indique reparar composição/pergunta. Não presuma integração por ter dois IDs.
Decisões: admitir, corrigir, descartar, lacuna_documental. Não preencher quantidade à força.
Todos os sete critérios precisam ser verdadeiros para admitir. Uma falha recuperável
recebe reparo concreto. Sem evidência para o alvo, lacuna_documental.
JSON {"avaliacoes":[{"id":"T01","decisao":"admitir","motivo":"...",
"correcao":"","duplicada_de":null,"criterios":{"suporte":true,"correta":true,
"autonoma":true,"determinada":true,"sem_pistas":true,"distinta":true,"composicao":true},
"checagem_essenciais":[{"id":"K1","sustentado":true,
"evidencias":[{"bloco":"B001","trecho":"literal"}],"justificativa":"..."}]}]}.
'''
