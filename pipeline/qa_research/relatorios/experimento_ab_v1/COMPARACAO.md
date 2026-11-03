# Experimento A/B: documento refinado x antigo e capítulo x janela

Mesmo gerador v21, mesmos 3 documentos (02_02, 03_03, 07_01), sem herança de rodadas anteriores, deduplicação incremental calibrada. Avaliação com o mesmo contexto em todos os braços (capítulos tocados pelo contexto de geração).

## Por braço

| Métrica | A (antigo, janela, sust.) | B (refinado, janela, sust.) | C (antigo, capitulo, sust.) | D (refinado, capitulo, sust.) |
|---|---|---|---|---|
| Aprovadas finais | 280 | 342 | 271 | 290 |
| Aprovação do auditor | 47.2% | 52.0% | 46.7% | 49.6% |
| Redundância removida | 38.2% | 32.7% | 39.2% | 42.0% |
| Conhecimentos por 1.000 palavras | 15.38 | 15.59 | 14.88 | 13.22 |
| Blocos com questão | 96.6% | 96.8% | 97.4% | 95.2% |
| Foco coberto: início/meio/fim do capítulo | 97% / 88% / 86% | 98% / 98% / 95% | 97% / 90% / 89% | 95% / 92% / 93% |
| Blocos citados por questão (janela) | 1.09 | 1.12 | 1.18 | 1.16 |
| Palavras na resposta | 16.611 | 16.807 | 16.919 | 16.597 |
| **Gabaritos totalmente sustentados** | 77.1% | 80.7% | 81.2% | 81.4% |
| Afirmações sustentadas | 89.6% | 91.2% | 92.0% | 90.9% |
| gpt-4-1-nano: sem / com contexto (gap) | 50.0% / 74.6% (24.6%) | 52.6% / 72.2% (19.6%) | 46.9% / 73.1% (26.2%) | 50.7% / 73.4% (22.8%) |
| gpt-4-1-mini: sem / com contexto (gap) | 72.9% / 93.9% (21.1%) | 73.4% / 91.2% (17.8%) | 69.4% / 93.4% (24.0%) | 66.6% / 87.9% (21.4%) |
| gpt-4-1: sem / com contexto (gap) | 81.8% / 96.8% (15.0%) | 81.9% / 93.3% (11.4%) | 81.2% / 94.1% (12.9%) | 76.9% / 94.5% (17.6%) |
| Max ROUGE-L pergunta-frase | 0.306 | 0.287 | 0.277 | 0.286 |
| Novel bigramas / trigramas | 53.650 / 72.660 | 54.850 / 75.846 | 56.982 / 76.649 | 55.915 / 76.234 |
| Self-BLEU-4 | 0.217 | 0.214 | 0.197 | 0.211 |
| Vizinho mais próximo (cosseno centrado) | 0.491 | 0.519 | 0.484 | 0.496 |
| Chamadas / tokens (mil) | 3543 / 11857 | 4166 / 13468 | 3340 / 11826 | 3572 / 12935 |

## Efeitos (diferença e IC 95%)

| Efeito | Sustentados | gap 4.1 Nano | gap 4.1 Mini | gap 4.1 | sem contexto 4.1 | Max ROUGE-L | Self-BLEU-4 |
|---|---|---|---|---|---|---|---|
| documento (janela): B-A | +3.6 [-3.3; +9.9] | -5.1 [-14.1; +4.5] | -3.2 [-11.0; +4.5] | -3.6 [-10.3; +3.2] | +0.1 [-5.9; +6.4] | -0.019 [-0.042; +0.006] | -0.003 [-0.023; +0.016] |
| documento (capítulo): D-C | +0.2 [-6.2; +6.6] | -3.4 [-13.3; +7.0] | -2.6 [-10.8; +5.9] | +4.7 [-2.1; +11.5] | -4.3 [-10.9; +2.0] | +0.010 [-0.015; +0.035] | +0.015 [-0.005; +0.033] |
| unidade (antigo): C-A | +4.0 [-2.8; +10.5] | +1.6 [-8.0; +10.9] | +2.9 [-5.1; +10.6] | -2.1 [-8.7; +4.5] | -0.6 [-7.1; +5.8] | -0.029 [-0.053; -0.006] | -0.020 [-0.040; -0.001] |
| unidade (refinado): D-B | +0.7 [-5.1; +6.9] | +3.2 [-6.1; +12.9] | +3.5 [-3.9; +11.0] | +6.2 [-1.1; +12.7] | -5.0 [-11.2; +1.0] | -0.000 [-0.025; +0.023] | -0.003 [-0.022; +0.015] |

Proporções em pontos percentuais. IC 95% por bootstrap de questões; 3 documentos, então efeitos por documento devem ser lidos junto (questões do mesmo documento não são independentes).
