# Piloto de geração por janela

Modo: junto · Condição: EC · Modelo: `gpt-5-4-petrobras:high` · mínimo 4 · máximo 4 questões por janela.

| Métrica | Total | 01_01 | 02_02 |
|---|---:|---:|---:|
| Janelas | 60 | 24 | 36 |
| Status ok / parcial / sem | 60 / 0 / 0 | 24 / 0 / 0 | 36 / 0 / 0 |
| Questões | 240 | 96 | 144 |
| Questões por janela | 4.0 | 4.0 | 4.0 |
| Fácil / média / difícil (%) | 25.0 / 50.0 / 25.0 | 25.0 / 50.0 / 25.0 | 25.0 / 50.0 / 25.0 |
| Fundamentos literais (%) | 99.6 | 99.0 | 100.0 |
| Âncora válida em F (%) | 100.0 | 100.0 | 100.0 |
| Usa bloco de apoio (%) | 3.8 | 1.0 | 5.6 |
| Resposta ≤ 50 palavras (%) | 100.0 | 100.0 | 100.0 |
| Palavras: pergunta / resposta | 33.5 / 10.4 | 34.2 / 9.5 | 33.1 / 11.0 |
| Segundos por janela | 74.0 | 74.7 | 73.5 |
| Semelhança com exemplos: média / máx | 0.039 / 0.154 | 0.037 / 0.088 | 0.04 / 0.154 |

Alvo de dificuldade: 50 / 30 / 20. Tipos de demanda (total): recordar 60, inferir 80, diagnosticar 51, comparar 21, decidir 28.
Quase duplicadas (Jaccard ≥ 0.6 no mesmo documento): 0 pares, 0 questões.
Chamadas: 60 ok, 0 tentativas com erro (0 reparos de formato). Tokens: 225060 entrada, 456550 saída.
Janelas com falha pendente: 0.
