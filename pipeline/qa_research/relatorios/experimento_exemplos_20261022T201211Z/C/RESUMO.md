# Piloto de geração por janela

Condição: C · Modelo: `gpt-5-4-petrobras:high` · mínimo 6 · máximo 8 questões por janela.

| Métrica | Total | 01_01 | 02_02 |
|---|---:|---:|---:|
| Janelas | 40 | 20 | 20 |
| Status ok / parcial / sem | 40 / 0 / 0 | 20 / 0 / 0 | 20 / 0 / 0 |
| Questões | 290 | 149 | 141 |
| Questões por janela | 7.25 | 7.45 | 7.05 |
| Fácil / média / difícil (%) | 41.4 / 55.5 / 3.1 | 43.6 / 55.0 / 1.3 | 39.0 / 56.0 / 5.0 |
| Fundamentos literais (%) | 100.0 | 100.0 | 100.0 |
| Âncora válida em F (%) | 100.0 | 100.0 | 100.0 |
| Usa bloco de apoio (%) | 0.7 | 0.0 | 1.4 |
| Resposta ≤ 50 palavras (%) | 100.0 | 100.0 | 100.0 |
| Palavras: pergunta / resposta | 25.0 / 9.9 | 24.8 / 10.0 | 25.3 / 9.9 |
| Segundos por janela | 65.3 | 59.1 | 71.5 |
| Semelhança com exemplos: média / máx | 0.035 / 0.139 | 0.035 / 0.139 | 0.036 / 0.115 |

Alvo de dificuldade: 50 / 30 / 20. Tipos de demanda (total): recordar 113, inferir 68, diagnosticar 34, comparar 18, decidir 57.
Quase duplicadas (Jaccard ≥ 0.6 no mesmo documento): 0 pares, 0 questões.
Chamadas: 40 ok, 0 tentativas com erro (0 reparos de formato). Tokens: 103355 entrada, 256006 saída.
Janelas com falha pendente: 0.
