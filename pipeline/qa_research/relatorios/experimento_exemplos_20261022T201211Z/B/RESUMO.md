# Piloto de geração por janela

Condição: B · Modelo: `gpt-5-4-petrobras:high` · mínimo 6 · máximo 8 questões por janela.

| Métrica | Total | 01_01 | 02_02 |
|---|---:|---:|---:|
| Janelas | 40 | 20 | 20 |
| Status ok / parcial / sem | 40 / 0 / 0 | 20 / 0 / 0 | 20 / 0 / 0 |
| Questões | 300 | 150 | 150 |
| Questões por janela | 7.5 | 7.5 | 7.5 |
| Fácil / média / difícil (%) | 43.7 / 54.3 / 2.0 | 44.0 / 55.3 / 0.7 | 43.3 / 53.3 / 3.3 |
| Fundamentos literais (%) | 100.0 | 100.0 | 100.0 |
| Âncora válida em F (%) | 100.0 | 100.0 | 100.0 |
| Usa bloco de apoio (%) | 1.7 | 0.7 | 2.7 |
| Resposta ≤ 50 palavras (%) | 100.0 | 100.0 | 100.0 |
| Palavras: pergunta / resposta | 23.1 / 9.3 | 23.1 / 9.5 | 23.1 / 9.2 |
| Segundos por janela | 67.3 | 67.4 | 67.1 |
| Semelhança com exemplos: média / máx | 0.011 / 0.158 | 0.01 / 0.158 | 0.011 / 0.103 |

Alvo de dificuldade: 50 / 30 / 20. Tipos de demanda (total): recordar 112, inferir 74, diagnosticar 29, comparar 23, decidir 62.
Quase duplicadas (Jaccard ≥ 0.6 no mesmo documento): 0 pares, 0 questões.
Chamadas: 40 ok, 0 tentativas com erro (0 reparos de formato). Tokens: 97972 entrada, 267845 saída.
Janelas com falha pendente: 0.
