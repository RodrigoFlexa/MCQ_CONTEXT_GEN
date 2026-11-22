# Calibração do atalho do auditor

Amostra estratificada por tipo: 299 reprovadas só por atalho (de 5204) e 300 válidas (de 5452), respondidas sem contexto, resposta de até 20 palavras, juiz padrão.

| Modelo | Acerto nas reprovadas por atalho | Acerto nas válidas | Diferença (pontos) |
|---|---|---|---|
| gpt-4-1-mini | 56.2% (IC 50.5 a 61.7) | 38.7% (IC 33.3 a 44.3) | 17.5 |
| gpt-5-mini | 71.6% (IC 66.2 a 76.4) | 65.0% (IC 59.4 a 70.2) | 6.6 |

Leitura: O atalho apontado pelo auditor separa pouco: as reprovadas por ele não são muito mais fáceis que as válidas para os modelos menores; boa parte é ruído de julgamento e merece conserto ou reavaliação, não descarte.

## Por tipo (acerto, %)

- gpt-4-1-mini: atalho {'conceito': 100.0, 'consequencia': 71.4, 'decisao': 50.9, 'diagnostico': 55.6, 'mecanismo': 69.2, 'procedimento': 57.1}; válidas {'conceito': 45.5, 'consequencia': 58.3, 'decisao': 37.2, 'diagnostico': 45.9, 'mecanismo': 48.3, 'procedimento': 31.6}
- gpt-5-mini: atalho {'conceito': 100.0, 'consequencia': 85.7, 'decisao': 73.7, 'diagnostico': 74.1, 'mecanismo': 100.0, 'procedimento': 64.7}; válidas {'conceito': 72.7, 'consequencia': 75.0, 'decisao': 62.8, 'diagnostico': 70.3, 'mecanismo': 72.4, 'procedimento': 61.2}
