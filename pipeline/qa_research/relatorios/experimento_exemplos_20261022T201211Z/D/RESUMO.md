# Piloto de geração por janela

Condição: D · Modelo: `gpt-5-4-petrobras:high` · mínimo 6 · máximo 8 questões por janela.

| Métrica | Total | 01_01 | 02_02 |
|---|---:|---:|---:|
| Janelas | 40 | 20 | 20 |
| Status ok / parcial / sem | 40 / 0 / 0 | 20 / 0 / 0 | 20 / 0 / 0 |
| Questões | 288 | 145 | 143 |
| Questões por janela | 7.2 | 7.25 | 7.15 |
| Fácil / média / difícil (%) | 45.1 / 52.1 / 2.8 | 42.8 / 53.8 / 3.4 | 47.6 / 50.3 / 2.1 |
| Fundamentos literais (%) | 100.0 | 100.0 | 100.0 |
| Âncora válida em F (%) | 100.0 | 100.0 | 100.0 |
| Usa bloco de apoio (%) | 2.1 | 0.7 | 3.5 |
| Resposta ≤ 50 palavras (%) | 100.0 | 100.0 | 100.0 |
| Palavras: pergunta / resposta | 24.8 / 9.6 | 25.6 / 9.7 | 23.9 / 9.6 |
| Segundos por janela | 72.0 | 74.5 | 69.5 |
| Semelhança com exemplos: média / máx | 0.038 / 0.105 | 0.038 / 0.105 | 0.037 / 0.102 |

Alvo de dificuldade: 50 / 30 / 20. Tipos de demanda (total): recordar 107, inferir 78, diagnosticar 27, comparar 22, decidir 54.
Quase duplicadas (Jaccard ≥ 0.6 no mesmo documento): 0 pares, 0 questões.
Chamadas: 40 ok, 0 tentativas com erro (0 reparos de formato). Tokens: 107642 entrada, 283304 saída.
Janelas com falha pendente: 0.
