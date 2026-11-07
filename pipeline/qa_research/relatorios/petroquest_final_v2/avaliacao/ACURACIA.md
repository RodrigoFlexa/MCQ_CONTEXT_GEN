# Acurácia dos modelos sem contexto

Atualizado em 2026-11-07T03:16:43.924774+00:00. Questões prontas: 8738 em 40 tópicos. Juiz: `gpt-5-4-petrobras:medium`. GPT-4.1 Nano/Mini/Full, sem effort; até 100 palavras. Juiz GPT-5.4 medium; braços open/closed-book.
Acurácia = % de respostas corretas; "com parcial" conta a parcial como meio acerto.

## Geral

| Modelo | julgadas | acurácia (%) | com parcial (%) | corretas | parciais |
|---|---|---|---|---|---|
| gpt-5-4 | 8737 | **86.3** | 90.6 | 7544 | 750 |
| gpt-5 | 8738 | **81.1** | 86.6 | 7085 | 956 |
| gpt-5-mini | 8736 | **68.2** | 76.2 | 5958 | 1401 |
| gpt-4-1 | 8737 | **66.8** | 75.7 | 5832 | 1570 |
| gpt-4-1-mini | 8738 | **56.9** | 67.4 | 4972 | 1834 |

## Por tipo de questão (acurácia %, julgadas entre parênteses)

| Tipo | questões | gpt-4-1-mini | gpt-4-1 | gpt-5-mini | gpt-5 | gpt-5-4 |
|---|---|---|---|---|---|---|
| conceito | 1816 | 65.0 (1816) | 72.8 (1816) | 75.8 (1816) | 86.5 (1816) | 88.5 (1816) |
| mecanismo | 1292 | 66.3 (1292) | 73.6 (1292) | 76.7 (1291) | 85.8 (1292) | 90.8 (1291) |
| consequencia | 356 | 68.0 (356) | 71.9 (356) | 79.8 (356) | 86.0 (356) | 87.9 (356) |
| diagnostico | 1858 | 51.7 (1858) | 64.3 (1858) | 65.2 (1858) | 79.9 (1858) | 86.4 (1858) |
| decisao | 2332 | 51.8 (2332) | 62.1 (2331) | 61.3 (2331) | 77.9 (2332) | 84.7 (2332) |
| procedimento | 1084 | 48.5 (1084) | 61.1 (1084) | 61.6 (1084) | 73.6 (1084) | 80.4 (1084) |

## Por composição (acurácia %)

| Composição | gpt-4-1-mini | gpt-4-1 | gpt-5-mini | gpt-5 | gpt-5-4 |
|---|---|---|---|---|---|
| simples | 56.7 (8292) | 66.5 (8291) | 68.1 (8291) | 81.1 (8292) | 86.2 (8291) |
| composta | 61.2 (446) | 71.3 (446) | 70.6 (445) | 80.5 (446) | 89.5 (446) |

## Cobertura

| Modelo | Total | Com nota | Sem nota | Cobertura (%) |
|---|---:|---:|---:|---:|
| gpt-4-1-mini | 8738 | 8738 | 0 | 100.0 |
| gpt-4-1 | 8738 | 8737 | 1 | 100.0 |
| gpt-5-mini | 8738 | 8736 | 2 | 100.0 |
| gpt-5 | 8738 | 8738 | 0 | 100.0 |
| gpt-5-4 | 8738 | 8737 | 1 | 100.0 |

Bloqueios terminais sem nota; excluídos da acurácia, reportados na cobertura.

## Por condição

| Condição | Modelo | Com nota | Corretas | Parciais | Incorretas | Sem nota | Acurácia (%) |
|---|---|---:|---:|---:|---:|---:|---:|
| closed_book | gpt-4-1-mini | 4369 | 1748 | 1229 | 1392 | 0 | 40.01 |
| closed_book | gpt-4-1 | 4369 | 2233 | 1120 | 1016 | 0 | 51.11 |
| closed_book | gpt-5-mini | 4367 | 2485 | 871 | 1011 | 2 | 56.90 |
| closed_book | gpt-5 | 4369 | 3073 | 716 | 580 | 0 | 70.34 |
| closed_book | gpt-5-4 | 4368 | 3367 | 614 | 387 | 1 | 77.08 |
| open_book | gpt-4-1-mini | 4369 | 3224 | 605 | 540 | 0 | 73.79 |
| open_book | gpt-4-1 | 4368 | 3599 | 450 | 319 | 1 | 82.39 |
| open_book | gpt-5-mini | 4369 | 3473 | 530 | 366 | 0 | 79.49 |
| open_book | gpt-5 | 4369 | 4012 | 240 | 117 | 0 | 91.83 |
| open_book | gpt-5-4 | 4369 | 4177 | 136 | 56 | 0 | 95.61 |
