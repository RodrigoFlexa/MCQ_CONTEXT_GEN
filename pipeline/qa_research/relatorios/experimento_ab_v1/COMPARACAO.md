# Experimento A/B: documento refinado x antigo e capítulo x janela

Braços A a D com o gerador v21 (derivados: _v22, _v23, _sat, _sust), mesmos 3 documentos (02_02, 03_03, 07_01), sem herança de rodadas anteriores, deduplicação incremental calibrada. Avaliação com o mesmo contexto em todos os braços (capítulos tocados pelo contexto de geração).

## Por braço

| Métrica | A (antigo, janela) | B (refinado, janela) | C (antigo, capitulo) | D (refinado, capitulo) | B_v22 (refinado, janela, sat.) | B_v23 (refinado, janela, sat.) |
|---|---|---|---|---|---|---|
| Aprovadas finais | 280 | 342 | 271 | 290 | 107 | 301 |
| Aprovação do auditor | 47.2% | 52.0% | 46.7% | 49.6% | 13.0% | 31.3% |
| Redundância removida | 38.2% | 32.7% | 39.2% | 42.0% | 17.7% | 14.7% |
| Conhecimentos por 1.000 palavras | 15.38 | 15.59 | 14.88 | 13.22 | 4.88 | 13.72 |
| Conhecimentos novos por rodada (saturação) | - | - | - | - | 45 / 25 / 13 / 4 / 0 | 109 / 69 / 43 / 18 / 11 |
| Blocos com questão | 96.6% | 96.8% | 97.4% | 95.2% | 53.2% | 84.9% |
| Foco coberto: início/meio/fim do capítulo | 97% / 88% / 86% | 98% / 98% / 95% | 97% / 90% / 89% | 95% / 92% / 93% | 53% / 42% / 37% | 72% / 75% / 79% |
| Blocos citados por questão (janela) | 1.09 | 1.12 | 1.18 | 1.16 | 1.53 | 1.53 |
| Palavras na resposta | 16.611 | 16.807 | 16.919 | 16.597 | 7.607 | 6.319 |
| **Gabaritos totalmente sustentados** | 77.1% | 80.7% | 81.2% | 81.4% | 81.3% | 75.7% |
| Afirmações sustentadas | 89.6% | 91.2% | 92.0% | 90.9% | 85.2% | 82.3% |
| Sustentados nas rodadas extras | - | - | - | - | 73.3% | 75.3% |
| gpt-4-1-nano: sem / com contexto (gap) | 50.0% / 74.6% (24.6%) | 52.6% / 72.2% (19.6%) | 46.9% / 73.1% (26.2%) | 50.7% / 73.4% (22.8%) | 48.6% / 62.6% (14.0%) | 31.6% / 48.8% (17.3%) |
| gpt-4-1-mini: sem / com contexto (gap) | 72.9% / 93.9% (21.1%) | 73.4% / 91.2% (17.8%) | 69.4% / 93.4% (24.0%) | 66.6% / 87.9% (21.4%) | 68.2% / 86.9% (18.7%) | 55.5% / 82.1% (26.6%) |
| gpt-4-1: sem / com contexto (gap) | 81.8% / 96.8% (15.0%) | 81.9% / 93.3% (11.4%) | 81.2% / 94.1% (12.9%) | 76.9% / 94.5% (17.6%) | 86.0% / 92.5% (6.5%) | 71.4% / 86.4% (15.0%) |
| Sem contexto, parcial = 0,5 (Nano / Mini / 4.1) | 64.8% / 80.7% / 89.3% | 66.7% / 82.7% / 88.6% | 63.7% / 80.3% / 88.6% | 64.0% / 76.9% / 85.5% | 58.9% / 78.0% / 89.7% | 44.7% / 66.6% / 78.9% |
| Painel sem contexto: GPT-5 mini / GPT-5.4 | - | 85.6% / 94.4% | - | - | 86.9% / 92.5% | 80.6% / 91.3% |
| Difícil para o GPT-5.4 / nenhum modelo acerta | - | 5.5% / 2.3% | - | - | 7.4% / 0.9% | 8.7% / 5.0% |
| Decisão + procedimento | 19.3% | 18.4% | 15.9% | 16.9% | 18.7% | 45.5% |
| Max ROUGE-L pergunta-frase | 0.306 | 0.287 | 0.277 | 0.286 | 0.224 | 0.191 |
| Novel bigramas / trigramas | 53.650 / 72.660 | 54.850 / 75.846 | 56.982 / 76.649 | 55.915 / 76.234 | 48.275 / 69.668 | 46.243 / 70.066 |
| Self-BLEU-4 | 0.217 | 0.214 | 0.197 | 0.211 | 0.157 | 0.216 |
| Vizinho mais próximo (cosseno centrado) | 0.491 | 0.519 | 0.484 | 0.496 | 0.508 | 0.539 |
| Chamadas / tokens (mil) | 3543 / 11857 | 4938 / 14173 | 3340 / 11826 | 3572 / 12935 | 2793 / 10964 | 5175 / 18183 |

## Efeitos (diferença e IC 95%)

| Efeito | Sustentados | gap 4.1 Nano | gap 4.1 Mini | gap 4.1 | sem contexto 4.1 | sem contexto 5.4 | difícil (5.4) | Max ROUGE-L | Self-BLEU-4 |
|---|---|---|---|---|---|---|---|---|---|
| documento (janela): B-A | +3.6 [-3.3; +9.9] | -5.1 [-14.1; +4.5] | -3.2 [-11.0; +4.5] | -3.6 [-10.3; +3.2] | +0.1 [-5.9; +6.4] | - | - | -0.019 [-0.042; +0.006] | -0.003 [-0.023; +0.016] |
| documento (capítulo): D-C | +0.2 [-6.2; +6.6] | -3.4 [-13.3; +7.0] | -2.6 [-10.8; +5.9] | +4.7 [-2.1; +11.5] | -4.3 [-10.9; +2.0] | - | - | +0.010 [-0.015; +0.035] | +0.015 [-0.005; +0.033] |
| unidade (antigo): C-A | +4.0 [-2.8; +10.5] | +1.6 [-8.0; +10.9] | +2.9 [-5.1; +10.6] | -2.1 [-8.7; +4.5] | -0.6 [-7.1; +5.8] | - | - | -0.029 [-0.053; -0.006] | -0.020 [-0.040; -0.001] |
| unidade (refinado): D-B | +0.7 [-5.1; +6.9] | +3.2 [-6.1; +12.9] | +3.5 [-3.9; +11.0] | +6.2 [-1.1; +12.7] | -5.0 [-11.2; +1.0] | - | - | -0.000 [-0.025; +0.023] | -0.003 [-0.022; +0.015] |
| gerador v22: B_v22-B | +0.6 [-8.3; +8.8] | -5.6 [-17.4; +7.5] | +0.9 [-10.9; +12.3] | -4.9 [-13.7; +5.0] | +4.1 [-4.1; +11.8] | -1.9 [-7.8; +3.1] | +1.9 [-3.3; +7.5] | -0.063 [-0.086; -0.040] | -0.057 [-0.082; -0.033] |
| gerador v23: B_v23-B | -5.0 [-11.5; +1.7] | -2.3 [-11.2; +6.9] | +8.7 [+1.1; +16.9] | +3.5 [-3.6; +11.0] | -10.4 [-17.2; -3.9] | -3.1 [-6.8; +0.9] | +3.1 [-0.8; +7.1] | -0.096 [-0.113; -0.078] | +0.001 [-0.016; +0.019] |
| v23 x v22: B_v23-B_v22 | -5.6 [-14.2; +3.5] | +3.3 [-10.2; +16.5] | +7.9 [-3.8; +19.4] | +8.4 [-2.2; +18.8] | -14.6 [-23.0; -5.8] | -1.2 [-6.9; +5.1] | +1.2 [-4.6; +7.0] | -0.033 [-0.053; -0.014] | +0.058 [+0.036; +0.081] |

Proporções em pontos percentuais. IC 95% por bootstrap de questões; 3 documentos, então efeitos por documento devem ser lidos junto (questões do mesmo documento não são independentes).
