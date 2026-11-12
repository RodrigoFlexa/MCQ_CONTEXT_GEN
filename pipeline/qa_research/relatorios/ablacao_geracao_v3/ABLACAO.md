# Ablação da geração v3 (escada cumulativa, sem poda)

960 chamadas por configuração (focos x visitas), de 0 a 4 questões por chamada. Toda questão gerada é avaliada. Válida = aprovada pelo auditor v23 + resposta de até 20 palavras + gabarito totalmente sustentado. IC 95% por reamostragem de tópicos.

| Configuração | Geradas | Por chamada | Aprovadas pelo auditor | Válida intrínseca | Válidas | Válidas por chamada | Quase-duplicatas | Tokens por válida |
|---|---|---|---|---|---|---|---|---|
| Naive | 3838 | 4,00 | 10,0% (7,3–12,9) | 3,5% (2,4–4,7) | 0,5% (0,2–0,9) | 0,02 | 83,1% | 65316 |
| + Regras | 3825 | 3,98 | 26,8% (22,9–31,0) | 59,5% (54,9–63,7) | 7,9% (6,3–9,5) | 0,31 | 67,9% | 24274 |
| + Documentos | 3443 | 3,59 | 34,4% (29,2–39,4) | 35,0% (29,8–40,2) | 26,9% (22,6–31,1) | 0,97 | 55,3% | 10105 |
| + Datasets externos | 3463 | 3,61 | 35,6% (30,6–40,4) | 36,1% (31,2–41,0) | 29,4% (25,2–33,4) | 1,06 | 54,4% | 9811 |
| + Retroalimentação | 2637 | 2,75 | 31,1% (26,0–36,0) | 32,3% (27,1–37,3) | 22,9% (18,8–27,1) | 0,63 | 14,0% | 25102 |
| + Retroalimentação sem memória | 2960 | 3,08 | 44,8% (39,1–50,4) | 44,9% (39,2–50,5) | 40,0% (34,8–45,2) | 1,23 | 52,0% | 13474 |
| + Retroalimentação sem memória e sem externos | 2778 | 2,89 | 45,6% (39,5–51,7) | 45,8% (39,7–51,8) | 39,8% (34,5–45,2) | 1,15 | 50,8% | 14042 |

| Comparação (degrau) | Válidas: diferença (pp, IC 95%, p) | Aprovadas pelo auditor |
|---|---|---|
| Naive → + Regras | 7,3 (5,8–9,0), p=0 | 16,8 (12,7–21,1), p=0 |
| + Regras → + Documentos | 19,1 (14,5–23,4), p=0 | 7,6 (2,3–12,5), p=0.002 |
| + Documentos → + Datasets externos | 2,4 (0,8–4,2), p=0 | 1,2 (-0,4–2,9), p=0.154 |
| + Datasets externos → + Retroalimentação | -6,5 (-8,8–-4,2), p=0 | -4,5 (-6,3–-2,5), p=0 |
| + Datasets externos → + Retroalimentação sem memória | 10,7 (8,3–13,0), p=0 | 9,3 (6,9–11,5), p=0 |
| + Retroalimentação → + Retroalimentação sem memória | 17,2 (14,2–19,9), p=0 | 13,7 (11,1–16,3), p=0 |
| + Documentos → + Retroalimentação sem memória e sem externos | 12,9 (10,6–15,2), p=0 | 11,2 (9,1–13,3), p=0 |
| + Retroalimentação sem memória → + Retroalimentação sem memória e sem externos | -0,3 (-2,3–1,9), p=0.808 | 0,8 (-1,6–3,2), p=0.519 |

## Diversidade (geradas, amostras do mesmo tamanho)

m = 2637 questões por amostra.

| Configuração | Self-BLEU por tópico | Distinct-2 | MATTR | MTLD | Vocabulário | Cosseno médio no tópico | Vendi relativo |
|---|---|---|---|---|---|---|---|
| Naive | 0,718 | 0,228 | 0,784 | 71,5 | 2379 | 0,616 | 0,066 |
| + Regras | 0,349 | 0,435 | 0,853 | 149,4 | 5917 | 0,561 | 0,103 |
| + Documentos | 0,229 | 0,506 | 0,865 | 171,3 | 6282 | 0,509 | 0,149 |
| + Datasets externos | 0,224 | 0,507 | 0,866 | 172,7 | 6361 | 0,509 | 0,149 |
| + Retroalimentação | 0,116 | 0,532 | 0,867 | 179,8 | 7012 | 0,507 | 0,189 |
| + Retroalimentação sem memória | 0,189 | 0,513 | 0,864 | 172,6 | 6784 | 0,512 | 0,165 |
| + Retroalimentação sem memória e sem externos | 0,191 | 0,507 | 0,864 | 172,9 | 6832 | 0,515 | 0,169 |

## Dificuldade (amostra, painel sem e com contexto)

| Configuração | Amostra | Acerto sem contexto (todas / válidas / inválidas) | Com contexto (todas) | Nenhum modelo acerta (válidas) |
|---|---|---|---|---|
| Naive | 500 | 38,4 / 100,0 / 38,2 | 39,6 | 0,0 |
| + Regras | 500 | 61,7 / 57,8 / 61,9 | 63,8 | 10,3 |
| + Documentos | 500 | 62,1 / 61,1 / 62,4 | 89,3 | 15,6 |
| + Datasets externos | 500 | 61,0 / 56,0 / 63,2 | 89,7 | 17,7 |
| + Retroalimentação | 500 | 70,4 / 66,4 / 71,5 | 85,6 | 6,5 |
| + Retroalimentação sem memória | 500 | 63,0 / 59,9 / 65,4 | 91,3 | 13,6 |
| + Retroalimentação sem memória e sem externos | 500 | 65,1 / 61,4 / 67,6 | 89,2 | 12,9 |

Motivos de reprovação do auditor:

- Naive: {'atalho': 1341, 'fora_da_fonte': 887, 'varias_respostas': 1248, 'nao_unico': 2938, 'depende_do_documento': 26, 'bloqueio': 2}
- + Regras: {'fora_da_fonte': 1942, 'atalho': 1077, 'varias_respostas': 558, 'depende_do_documento': 27, 'bloqueio': 10, 'nao_unico': 6}
- + Documentos: {'atalho': 1953, 'varias_respostas': 461, 'fora_da_fonte': 42, 'depende_do_documento': 129, 'nao_unico': 32, 'bloqueio': 1}
- + Datasets externos: {'atalho': 1925, 'varias_respostas': 495, 'nao_unico': 24, 'depende_do_documento': 130, 'fora_da_fonte': 35, 'bloqueio': 2}
- + Retroalimentação: {'atalho': 1613, 'varias_respostas': 329, 'fora_da_fonte': 57, 'depende_do_documento': 74, 'nao_unico': 9, 'bloqueio': 1}
- + Retroalimentação sem memória: {'atalho': 1473, 'depende_do_documento': 80, 'varias_respostas': 255, 'fora_da_fonte': 3, 'nao_unico': 16}
- + Retroalimentação sem memória e sem externos: {'atalho': 1340, 'varias_respostas': 234, 'nao_unico': 12, 'depende_do_documento': 90, 'bloqueio': 1, 'fora_da_fonte': 4}
