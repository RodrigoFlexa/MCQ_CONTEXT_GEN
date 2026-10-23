# Piloto de geração por janela

Modo: separado · Condição: C · Modelo: `gpt-5-4-petrobras:high` · mínimo 4 · máximo 4 questões por janela.

| Métrica | Total | 01_01 | 02_02 |
|---|---:|---:|---:|
| Janelas | 40 | 20 | 20 |
| Status ok / parcial / sem | 40 / 0 / 0 | 20 / 0 / 0 | 20 / 0 / 0 |
| Questões | 160 | 80 | 80 |
| Questões por janela | 4.0 | 4.0 | 4.0 |
| Fácil / média / difícil (%) | 35.0 / 40.0 / 25.0 | 33.8 / 41.2 / 25.0 | 36.2 / 38.8 / 25.0 |
| Fundamentos literais (%) | 100.0 | 100.0 | 100.0 |
| Âncora válida em F (%) | 100.0 | 100.0 | 100.0 |
| Usa bloco de apoio (%) | 3.1 | 1.2 | 5.0 |
| Resposta ≤ 50 palavras (%) | 100.0 | 100.0 | 100.0 |
| Palavras: pergunta / resposta | 31.1 / 18.3 | 32.1 / 19.4 | 30.1 / 17.1 |
| Segundos por janela | 66.7 | 66.6 | 66.8 |
| Semelhança com exemplos: média / máx | 0.038 / 0.097 | 0.036 / 0.083 | 0.039 / 0.097 |

Alvo de dificuldade: 50 / 30 / 20. Tipos de demanda (total): recordar 49, inferir 35, diagnosticar 18, comparar 19, decidir 39.
Quase duplicadas (Jaccard ≥ 0.6 no mesmo documento): 0 pares, 0 questões.
Chamadas: 80 ok, 0 tentativas com erro (0 reparos de formato). Tokens: 214115 entrada, 309893 saída.
Janelas com falha pendente: 0.
