# Experimento de modos: planejamento e redação juntos x separados

Mesmas janelas em todas as variantes.

| Métrica | junto: planejamento e redação no mesmo prompt | separado: planejamento e redação em chamadas separadas |
|---|---:|---:|
| Janelas | 40 | 40 |
| ok / parcial / sem | 40 / 0 / 0 | 40 / 0 / 0 |
| Questões | 160 | 160 |
| Questões por janela | 4.0 | 4.0 |
| Fácil / média / difícil (%) · alvo 50/30/20 | 33.8 / 41.2 / 25.0 | 35.0 / 40.0 / 25.0 |
| Recordar / inferir / diagnosticar / comparar / decidir | 51 / 43 / 22 / 10 / 34 | 49 / 35 / 18 / 19 / 39 |
| Fundamentos literais (%) | 100.0 | 100.0 |
| Âncora válida em F (%) | 100.0 | 100.0 |
| Usa bloco de apoio (%) | 3.1 | 3.1 |
| Resposta ≤ 50 palavras (%) | 100.0 | 100.0 |
| Palavras: pergunta / resposta | 30.8 / 14.9 | 31.1 / 18.3 |
| Semelhança com exemplos: média / máx | 0.038 / 0.128 | 0.038 / 0.097 |
| Semelhança ≥ 0,30 (%) | 0.0 | 0.0 |
| Segundos por janela | 63.0 | 66.7 |
| Janelas com ao menos uma média / uma difícil (%) | 100.0 / 100.0 | 100.0 / 100.0 |
| Palavras da pergunta: fácil / média / difícil | 15.5 / 32.0 / 49.5 | 15.4 / 33.1 / 49.8 |
| Acima do tamanho pedido (%) · 35/60/90 | 0.0 | 0.0 |
| Itens do plano descartados na redação | 0 | 0 |
| Quase duplicadas (pares) | 0 | 0 |
| Tokens entrada / saída | 114235 / 221926 | 214115 / 309893 |
| Falhas pendentes | 0 | 0 |

A semelhança com exemplos é a sobreposição lexical (Jaccard) com os pares recebidos na chamada. Exemplos em inglês (ARC, HotpotQA) quase não se sobrepõem por palavras; para eles, a leitura de `QUESTOES.md` é que mostra se a estrutura foi copiada.
