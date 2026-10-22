# Experimento de exemplos de forma

Mesmas janelas em todas as condições; só muda o bloco `<exemplos_de_forma>`.

| Métrica | A: sem exemplos | B: 3 externos (Pirá, ARC-Challenge, HotpotQA) | C: 3 aprovadas pelo especialista, de outras áreas | D: B + C (6 exemplos) |
|---|---:|---:|---:|---:|
| Janelas | 40 | 40 | 40 | 40 |
| ok / parcial / sem | 40 / 0 / 0 | 40 / 0 / 0 | 40 / 0 / 0 | 40 / 0 / 0 |
| Questões | 283 | 300 | 290 | 288 |
| Questões por janela | 7.08 | 7.5 | 7.25 | 7.2 |
| Fácil / média / difícil (%) · alvo 50/30/20 | 42.4 / 54.1 / 3.5 | 43.7 / 54.3 / 2.0 | 41.4 / 55.5 / 3.1 | 45.1 / 52.1 / 2.8 |
| Recordar / inferir / diagnosticar / comparar / decidir | 105 / 78 / 34 / 19 / 47 | 112 / 74 / 29 / 23 / 62 | 113 / 68 / 34 / 18 / 57 | 107 / 78 / 27 / 22 / 54 |
| Fundamentos literais (%) | 100.0 | 100.0 | 100.0 | 100.0 |
| Âncora válida em F (%) | 100.0 | 100.0 | 100.0 | 100.0 |
| Usa bloco de apoio (%) | 1.8 | 1.7 | 0.7 | 2.1 |
| Resposta ≤ 50 palavras (%) | 100.0 | 100.0 | 100.0 | 100.0 |
| Palavras: pergunta / resposta | 25.3 / 9.4 | 23.1 / 9.3 | 25.0 / 9.9 | 24.8 / 9.6 |
| Semelhança com exemplos: média / máx | 0.0 / 0.0 | 0.011 / 0.158 | 0.035 / 0.139 | 0.038 / 0.105 |
| Semelhança ≥ 0,30 (%) | 0.0 | 0.0 | 0.0 | 0.0 |
| Segundos por janela | 68.4 | 67.3 | 65.3 | 72.0 |
| Quase duplicadas (pares) | 0 | 0 | 0 | 0 |
| Tokens entrada / saída | 94792 / 259433 | 97972 / 267845 | 103355 / 256006 | 107642 / 283304 |
| Falhas pendentes | 0 | 0 | 0 | 0 |

A semelhança com exemplos é a sobreposição lexical (Jaccard) com os pares recebidos na chamada. Exemplos em inglês (ARC, HotpotQA) quase não se sobrepõem por palavras; para eles, a leitura de `QUESTOES.md` é que mostra se a estrutura foi copiada.
