# Experimento de exemplos externos (modo junto, composição exata)

Mesmas janelas em todas as variantes.

| Métrica | E: 6 exemplos externos | EC: 6 exemplos externos + 3 questões já geradas (especialista) |
|---|---:|---:|
| Janelas | 40 | 40 |
| ok / parcial / sem | 40 / 0 / 0 | 39 / 1 / 0 |
| Questões | 160 | 159 |
| Questões por janela | 4.0 | 3.98 |
| Fácil / média / difícil (%) · alvo 50/30/20 | 25.0 / 50.0 / 25.0 | 25.2 / 50.3 / 24.5 |
| Recordar / inferir / diagnosticar / comparar / decidir | 40 / 38 / 19 / 15 / 48 | 40 / 39 / 25 / 14 / 41 |
| Fundamentos literais (%) | 100.0 | 99.4 |
| Âncora válida em F (%) | 100.0 | 100.0 |
| Usa bloco de apoio (%) | 1.2 | 1.9 |
| Resposta ≤ 50 palavras (%) | 100.0 | 100.0 |
| Palavras: pergunta / resposta | 31.0 / 14.0 | 30.9 / 14.3 |
| Semelhança com exemplos: média / máx | 0.028 / 0.111 | 0.043 / 0.143 |
| Semelhança ≥ 0,30 (%) | 0.0 | 0.0 |
| Segundos por janela | 56.9 | 58.6 |
| Janelas com ao menos uma média / uma difícil (%) | 100.0 / 100.0 | 100.0 / 97.5 |
| Palavras da pergunta: fácil / média / difícil | 13.0 / 29.1 / 52.7 | 13.3 / 29.3 / 52.1 |
| Acima do tamanho pedido (%) · 35/60/90 | 0.0 | 0.0 |
| Itens do plano descartados na redação | 0 | 0 |
| Janelas com a composição exata (%) | 100.0 | 97.5 |
| Inícios de pergunta distintos (2 primeiras palavras) | 92 | 110 |
| Início mais comum | em um (18.1%) | em um (17.0%) |
| Quase duplicadas (pares) | 0 | 0 |
| Tokens entrada / saída | 118361 / 227928 | 131391 / 231581 |
| Falhas pendentes | 0 | 0 |

A semelhança com exemplos é a sobreposição lexical (Jaccard) com os pares recebidos na chamada. Exemplos em inglês (ARC, HotpotQA) quase não se sobrepõem por palavras; para eles, a leitura de `QUESTOES.md` é que mostra se a estrutura foi copiada.
