# Piloto de geração por janela

Condição: A · Modelo: `gpt-5-4-petrobras:high` · mínimo 6 · máximo 8 questões por janela.

| Métrica | Total | 01_01 | 02_02 |
|---|---:|---:|---:|
| Janelas | 40 | 20 | 20 |
| Status ok / parcial / sem | 40 / 0 / 0 | 20 / 0 / 0 | 20 / 0 / 0 |
| Questões | 283 | 144 | 139 |
| Questões por janela | 7.08 | 7.2 | 6.95 |
| Fácil / média / difícil (%) | 42.4 / 54.1 / 3.5 | 41.7 / 56.2 / 2.1 | 43.2 / 51.8 / 5.0 |
| Fundamentos literais (%) | 100.0 | 100.0 | 100.0 |
| Âncora válida em F (%) | 100.0 | 100.0 | 100.0 |
| Usa bloco de apoio (%) | 1.8 | 0.0 | 3.6 |
| Resposta ≤ 50 palavras (%) | 100.0 | 100.0 | 100.0 |
| Palavras: pergunta / resposta | 25.3 / 9.4 | 24.5 / 9.7 | 26.1 / 9.2 |
| Segundos por janela | 68.4 | 68.0 | 68.8 |
| Semelhança com exemplos: média / máx | 0.0 / 0.0 | 0.0 / 0.0 | 0.0 / 0.0 |

Alvo de dificuldade: 50 / 30 / 20. Tipos de demanda (total): recordar 105, inferir 78, diagnosticar 34, comparar 19, decidir 47.
Quase duplicadas (Jaccard ≥ 0.6 no mesmo documento): 0 pares, 0 questões.
Chamadas: 40 ok, 1 tentativas com erro (1 reparos de formato). Tokens: 94792 entrada, 259433 saída.
Janelas com falha pendente: 0.
