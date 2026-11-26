# Acurácia dos modelos sem contexto

Atualizado em 2026-11-25T21:14:37.737711+00:00. Questões prontas: 8918 em 40 tópicos. Juiz: `gpt-5-4-petrobras:medium`. GPT-4.1 Nano/Mini/Full, sem effort; até 100 palavras. Juiz GPT-5.4 medium; braços open/closed-book.
Acurácia = % de respostas corretas; "com parcial" conta a parcial como meio acerto.

## Geral

| Modelo | julgadas | acurácia (%) | com parcial (%) | corretas | parciais |
|---|---|---|---|---|---|
| gpt-5-4 | 8912 | **90.7** | 93.4 | 8086 | 481 |
| gpt-5 | 8914 | **87.8** | 90.9 | 7830 | 551 |
| gpt-5-mini | 8917 | **75.3** | 80.7 | 6717 | 952 |
| gpt-4-1 | 8917 | **73.6** | 80.0 | 6564 | 1135 |
| gpt-4-1-mini | 8917 | **62.0** | 70.0 | 5530 | 1418 |

## Por tipo de questão (acurácia %, julgadas entre parênteses)

| Tipo | questões | gpt-4-1-mini | gpt-4-1 | gpt-5-mini | gpt-5 | gpt-5-4 |
|---|---|---|---|---|---|---|
| conceito | 354 | 68.4 (354) | 81.1 (354) | 82.8 (354) | 91.0 (354) | 91.0 (354) |
| mecanismo | 784 | 69.8 (784) | 80.6 (784) | 82.0 (784) | 92.2 (784) | 93.8 (784) |
| consequencia | 380 | 61.1 (380) | 71.6 (380) | 79.2 (380) | 88.2 (380) | 92.4 (380) |
| diagnostico | 1214 | 66.8 (1214) | 79.2 (1214) | 81.9 (1214) | 92.5 (1214) | 96.2 (1213) |
| decisao | 2956 | 61.6 (2955) | 74.7 (2955) | 75.8 (2955) | 88.8 (2952) | 91.6 (2954) |
| procedimento | 3230 | 58.1 (3230) | 68.2 (3230) | 69.6 (3230) | 83.7 (3230) | 86.9 (3227) |

## Por composição (acurácia %)

| Composição | gpt-4-1-mini | gpt-4-1 | gpt-5-mini | gpt-5 | gpt-5-4 |
|---|---|---|---|---|---|
| simples | 62.0 (8917) | 73.6 (8917) | 75.3 (8917) | 87.8 (8914) | 90.7 (8912) |
| composta | - (0) | - (0) | - (0) | - (0) | - (0) |

## Cobertura

| Modelo | Total | Com nota | Sem nota | Cobertura (%) |
|---|---:|---:|---:|---:|
| gpt-4-1-mini | 8918 | 8917 | 1 | 100.0 |
| gpt-4-1 | 8918 | 8917 | 1 | 100.0 |
| gpt-5-mini | 8918 | 8917 | 1 | 100.0 |
| gpt-5 | 8918 | 8914 | 4 | 100.0 |
| gpt-5-4 | 8918 | 8912 | 6 | 99.9 |

Bloqueios terminais sem nota; excluídos da acurácia, reportados na cobertura.

## Por condição

| Condição | Modelo | Com nota | Corretas | Parciais | Incorretas | Sem nota | Acurácia (%) |
|---|---|---:|---:|---:|---:|---:|---:|
| closed_book | gpt-4-1-mini | 4458 | 1839 | 1082 | 1537 | 1 | 41.25 |
| closed_book | gpt-4-1 | 4458 | 2526 | 890 | 1042 | 1 | 56.66 |
| closed_book | gpt-5-mini | 4458 | 2766 | 685 | 1007 | 1 | 62.05 |
| closed_book | gpt-5 | 4456 | 3475 | 478 | 503 | 3 | 77.98 |
| closed_book | gpt-5-4 | 4453 | 3665 | 450 | 338 | 6 | 82.30 |
| open_book | gpt-4-1-mini | 4459 | 3691 | 336 | 432 | 0 | 82.78 |
| open_book | gpt-4-1 | 4459 | 4038 | 245 | 176 | 0 | 90.56 |
| open_book | gpt-5-mini | 4459 | 3951 | 267 | 241 | 0 | 88.61 |
| open_book | gpt-5 | 4458 | 4355 | 73 | 30 | 1 | 97.69 |
| open_book | gpt-5-4 | 4459 | 4421 | 31 | 7 | 0 | 99.15 |
