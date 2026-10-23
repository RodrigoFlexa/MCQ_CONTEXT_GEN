# Piloto de geração por janela

Modo: junto · Condição: E · Modelo: `gpt-5-4-petrobras:high` · mínimo 4 · máximo 4 questões por janela.

| Métrica | Total | 01_01 | 02_02 |
|---|---:|---:|---:|
| Janelas | 40 | 20 | 20 |
| Status ok / parcial / sem | 40 / 0 / 0 | 20 / 0 / 0 | 20 / 0 / 0 |
| Questões | 160 | 80 | 80 |
| Questões por janela | 4.0 | 4.0 | 4.0 |
| Fácil / média / difícil (%) | 25.0 / 50.0 / 25.0 | 25.0 / 50.0 / 25.0 | 25.0 / 50.0 / 25.0 |
| Fundamentos literais (%) | 100.0 | 100.0 | 100.0 |
| Âncora válida em F (%) | 100.0 | 100.0 | 100.0 |
| Usa bloco de apoio (%) | 1.2 | 0.0 | 2.5 |
| Resposta ≤ 50 palavras (%) | 100.0 | 100.0 | 100.0 |
| Palavras: pergunta / resposta | 31.0 / 14.0 | 30.5 / 13.4 | 31.5 / 14.5 |
| Segundos por janela | 56.9 | 56.9 | 57.0 |
| Semelhança com exemplos: média / máx | 0.028 / 0.111 | 0.029 / 0.083 | 0.028 / 0.111 |

Alvo de dificuldade: 50 / 30 / 20. Tipos de demanda (total): recordar 40, inferir 38, diagnosticar 19, comparar 15, decidir 48.
Quase duplicadas (Jaccard ≥ 0.6 no mesmo documento): 0 pares, 0 questões.
Chamadas: 40 ok, 0 tentativas com erro (0 reparos de formato). Tokens: 118361 entrada, 227928 saída.
Janelas com falha pendente: 0.
