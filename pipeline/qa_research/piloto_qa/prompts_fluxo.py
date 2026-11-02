from .prompts import BASE,AUTHOR,JUDGE

GENERATE=AUTHOR+'''
Nesta chamada os alvos ainda não foram planejados: crie-os junto com as questões,
a partir do contexto entregue. Retorne alvos e questoes no mesmo JSON, com IDs iguais.
Use o prefixo recebido nos IDs (prefixo + Q01, Q02...). Para cada alvo declare
tipo, composicao, conhecimento, ponte e afirmacoes com evidencias literais.
Exemplo de alvo: {"id":"prefixoQ01","tipo":"mecanismo","composicao":"simples",
"conhecimento":"relação avaliada","ponte":"","afirmacoes":[{"afirmacao":"...",
"evidencias":[{"bloco":"B001","trecho":"literal"}]}]}.
Prioridades de tipos orientam variedade; não são cotas obrigatórias. Retorne até
limite questões, podendo retornar nenhuma com impedimentos, sem inventar para completar.
memoria contém somente enunciados já aprovados. Evite repetir a demanda avaliada,
mesmo trocando cenário. Exemplos de forma não são evidência. Não use assuntos pendentes.
Em contexto de interface, priorize conexões necessárias entre sistemas, quando sustentadas.
Inferências não podem introduzir condições de campo ausentes. Diagnóstico e decisão
exigem sinais discriminantes sem palavras que entreguem o fenômeno.
JSON final: {"alvos":[...],"questoes":[...],"impedimentos":[]}.
'''

AUDIT=JUDGE+'''
O inventário recebido contém vizinhos recuperados por similaridade semântica em
todo o banco aprovado. Similaridade alta, mesmo assunto ou mesma evidência não
bastam para descartar: compare a demanda, condições e conclusão, usando também
os gabaritos. Considere todas as candidatas deste lote entre si.
'''
