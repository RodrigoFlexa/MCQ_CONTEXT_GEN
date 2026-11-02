from .prompts import BASE, JUDGE

GENERATE = BASE + '''
Crie alvos e perguntas abertas juntos a partir do contexto fornecido. Cada pergunta
é uma candidata independente: problemas em outra candidata não autorizam alterar
uma candidata válida. Use o prefixo de IDs recebido (prefixo + Q01, Q02...).
Retorne até limite candidatas; não invente conteúdo para preencher a quantidade.

1. Classes: conceito, mecanismo, consequencia, diagnostico, decisao, procedimento.
   Prioridades orientam variedade, sem cotas obrigatórias. Conceito é simples.
2. Em composicao="simples", ponte="" é permitido. Em composicao="composta",
   ponte NUNCA fica vazia: escreva a inferência concreta que une pelo menos DUAS
   afirmações distintas e necessárias para obter a conclusão. Apenas citar dois
   blocos ou listar dois assuntos não constitui composição. Se uma só relação
   responder à pergunta inteira, classifique-a como simples. Não invente pontes.
3. Selecione afirmações suportadas antes de escrever o enunciado. Evidências
   preferencialmente usam {"passagem":"B001_P001"}, escolhendo um ID de passagens
   fornecidas. O Python recupera exatamente o texto original. Nunca invente IDs.
   O formato legado {"bloco":"B001","trecho":"cópia literal"} também é aceito:
   nesse formato, copie exatamente, sem paráfrase, tradução, elipse ou correção.
4. Enunciado autônomo de até 90 palavras, uma demanda clara; resposta mínima
   suficiente de até 60 palavras. Diagnóstico e decisão exigem cenário com sinais
   discriminantes, sem entregar a resposta. Não inclua premissas de campo ausentes.
5. Cada critério essencial deve ser pedido pela pergunta, constar no mínimo
   suficiente e ter evidência própria. Inferências explicitam premissas e ligação;
   não transformam coocorrência em causa. Preservar condições, negações e limites.
6. memoria contém só perguntas aprovadas. Evite repetir a demanda mudando cenário.
   Exemplos orientam forma, nunca fatos. Não use assuntos declarados pendentes.
7. Interfaces só justificam composição quando a conexão for necessária e suportada.
8. Não forneça classificações de dificuldade nem otimize métricas de comparação.

Retorne somente JSON completo. alvos e questoes têm os mesmos IDs, sem repetições:
{"alvos":[{"id":"prefixoQ01","tipo":"mecanismo","composicao":"simples",
"conhecimento":"relação avaliada com condições","ponte":"",
"afirmacoes":[{"afirmacao":"proposição suportada",
"evidencias":[{"passagem":"B001_P001"}]}]}],
"questoes":[{"id":"prefixoQ01","pergunta":"...?","resposta":"mínimo suficiente",
"cenario":false,"criterios":[{"id":"K1","criterio":"componente essencial",
"evidencias":[{"passagem":"B001_P001"}],"inferencia":"vazio se direto"}],
"equivalentes":[],"erros_materiais":[]}],"impedimentos":[]}.
'''

REPAIR = GENERATE + '''
REPARO INDIVIDUAL DE CONTRATO. Você recebe somente candidatas inválidas, seus
dados anteriores e erros localizados por ID/campo. Retorne alvo e questão completos
APENAS para ids_para_reparar, mantendo esses IDs. Não regenere irmãs aprovadas.
Corrija evidências selecionando passagens reais fornecidas, nunca ajustando o
conteúdo do documento. Para composta sem ponte, só mantenha composta se conseguir
demonstrar a inferência entre duas relações realmente necessárias; caso contrário,
reformule a candidata de modo simples e suportado. Não preencha ponte com texto
genérico para passar na validação. Se não houver solução sustentada, omita a
candidata e explique em impedimentos. Em reparo de refino, mantenha o alvo recebido.
Os IDs de alvos_congelados já possuem alvo válido: conserve integralmente sua
classe, composição, conhecimento, ponte e afirmações; repare apenas a questão.
'''

AUDIT = JUDGE + '''
O inventário contém vizinhos semânticos de todo o banco aprovado. Similaridade
alta, mesmo assunto ou mesma evidência não bastam para descartar: compare demanda,
condições, conclusão e gabaritos. Compare também as candidatas entre si.
Cada parecer é independente; devolva exatamente um por ID recebido. Uma falha
não reprova as outras candidatas. Os contextos_por_alvo indicam IDs de blocos
permitidos no contexto comum; não use blocos externos a essa seleção.
Evidências podem usar {"passagem":"B001_P001"} dos IDs fornecidos. Caso use
bloco/trecho, a citação precisa ser literal. Não invente suporte para admitir.
'''
