# Calibração do atalho do auditor

Amostra estratificada por tipo: 299 reprovadas só por atalho (de 5204) e 300 válidas (de 5452), respondidas sem contexto, resposta de até 20 palavras, juiz padrão.

| Modelo | Acerto nas reprovadas por atalho | Acerto nas válidas | Diferença (pontos) | p |
|---|---|---|---|---|
| gpt-4-1-mini | 56.2% (IC 50.5 a 61.7) | 38.7% (IC 33.3 a 44.3) | 17.5 | 0.000 |
| gpt-5-mini | 71.6% (IC 66.2 a 76.4) | 65.0% (IC 59.4 a 70.2) | 6.6 | 0.083 |

Leitura: O atalho é real só em parte (gpt-4-1-mini: +17.5 pontos (p = 0.000), erra 44% das reprovadas por atalho; gpt-5-mini: +6.6 pontos (p = 0.083), erra 28% das reprovadas por atalho). As reprovadas por ele são mais fáceis para o modelo mais fraco, mas pouco ou nada para o mais forte, e uma fração grande delas não é trivial na prática. Elas têm conhecimento aproveitável: conserto, não descarte.

## Por tipo (acerto, %)

- gpt-4-1-mini: atalho {'conceito': 100.0, 'consequencia': 71.4, 'decisao': 50.9, 'diagnostico': 55.6, 'mecanismo': 69.2, 'procedimento': 57.1}; válidas {'conceito': 45.5, 'consequencia': 58.3, 'decisao': 37.2, 'diagnostico': 45.9, 'mecanismo': 48.3, 'procedimento': 31.6}
- gpt-5-mini: atalho {'conceito': 100.0, 'consequencia': 85.7, 'decisao': 73.7, 'diagnostico': 74.1, 'mecanismo': 100.0, 'procedimento': 64.7}; válidas {'conceito': 72.7, 'consequencia': 75.0, 'decisao': 62.8, 'diagnostico': 70.3, 'mecanismo': 72.4, 'procedimento': 61.2}
