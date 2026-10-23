# Piloto de geração por janela

Modo: junto · Condição: C · Modelo: `gpt-5-4-petrobras:high` · mínimo 4 · máximo 4 questões por janela.

| Métrica | Total | 01_01 | 02_02 |
|---|---:|---:|---:|
| Janelas | 40 | 20 | 20 |
| Status ok / parcial / sem | 40 / 0 / 0 | 20 / 0 / 0 | 20 / 0 / 0 |
| Questões | 160 | 80 | 80 |
| Questões por janela | 4.0 | 4.0 | 4.0 |
| Fácil / média / difícil (%) | 33.8 / 41.2 / 25.0 | 35.0 / 40.0 / 25.0 | 32.5 / 42.5 / 25.0 |
| Fundamentos literais (%) | 100.0 | 100.0 | 100.0 |
| Âncora válida em F (%) | 100.0 | 100.0 | 100.0 |
| Usa bloco de apoio (%) | 3.1 | 1.2 | 5.0 |
| Resposta ≤ 50 palavras (%) | 100.0 | 100.0 | 100.0 |
| Palavras: pergunta / resposta | 30.8 / 14.9 | 30.5 / 15.4 | 31.0 / 14.4 |
| Segundos por janela | 63.0 | 58.5 | 67.5 |
| Semelhança com exemplos: média / máx | 0.038 / 0.128 | 0.036 / 0.102 | 0.039 / 0.128 |

Alvo de dificuldade: 50 / 30 / 20. Tipos de demanda (total): recordar 51, inferir 43, diagnosticar 22, comparar 10, decidir 34.
Quase duplicadas (Jaccard ≥ 0.6 no mesmo documento): 0 pares, 0 questões.
Chamadas: 40 ok, 0 tentativas com erro (0 reparos de formato). Tokens: 114235 entrada, 221926 saída.
Janelas com falha pendente: 0.
