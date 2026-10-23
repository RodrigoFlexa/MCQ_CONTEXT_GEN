# Piloto de geração por janela

Modo: junto · Condição: EC · Modelo: `gpt-5-4-petrobras:high` · mínimo 4 · máximo 4 questões por janela.

| Métrica | Total | 01_01 | 02_02 |
|---|---:|---:|---:|
| Janelas | 40 | 20 | 20 |
| Status ok / parcial / sem | 39 / 1 / 0 | 19 / 1 / 0 | 20 / 0 / 0 |
| Questões | 159 | 79 | 80 |
| Questões por janela | 3.98 | 3.95 | 4.0 |
| Fácil / média / difícil (%) | 25.2 / 50.3 / 24.5 | 25.3 / 50.6 / 24.1 | 25.0 / 50.0 / 25.0 |
| Fundamentos literais (%) | 99.4 | 100.0 | 98.8 |
| Âncora válida em F (%) | 100.0 | 100.0 | 100.0 |
| Usa bloco de apoio (%) | 1.9 | 3.8 | 0.0 |
| Resposta ≤ 50 palavras (%) | 100.0 | 100.0 | 100.0 |
| Palavras: pergunta / resposta | 30.9 / 14.3 | 30.8 / 14.3 | 31.0 / 14.4 |
| Segundos por janela | 58.6 | 59.5 | 57.6 |
| Semelhança com exemplos: média / máx | 0.043 / 0.143 | 0.043 / 0.143 | 0.044 / 0.118 |

Alvo de dificuldade: 50 / 30 / 20. Tipos de demanda (total): recordar 40, inferir 39, diagnosticar 25, comparar 14, decidir 41.
Quase duplicadas (Jaccard ≥ 0.6 no mesmo documento): 0 pares, 0 questões.
Chamadas: 40 ok, 0 tentativas com erro (0 reparos de formato). Tokens: 131391 entrada, 231581 saída.
Janelas com falha pendente: 0.
