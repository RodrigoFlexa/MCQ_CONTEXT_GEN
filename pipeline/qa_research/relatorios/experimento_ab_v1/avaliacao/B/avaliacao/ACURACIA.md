# Acurácia dos modelos sem contexto

Atualizado em 2026-11-02T22:25:57.261294+00:00. Questões prontas: 684 em 3 tópicos. Juiz: `gpt-5-4-petrobras:medium`. GPT-4.1 Nano/Mini/Full, sem effort; até 100 palavras. Juiz GPT-5.4 medium; braços open/closed-book.
Acurácia = % de respostas corretas; "com parcial" conta a parcial como meio acerto.

## Geral

| Modelo | julgadas | acurácia (%) | com parcial (%) | corretas | parciais |
|---|---|---|---|---|---|
| gpt-4-1 | 684 | **87.6** | 92.2 | 599 | 63 |
| gpt-4-1-mini | 684 | **82.3** | 88.7 | 563 | 87 |
| gpt-4-1-nano | 684 | **62.4** | 73.9 | 427 | 157 |

## Por tipo de questão (acurácia %, julgadas entre parênteses)

| Tipo | questões | gpt-4-1-nano | gpt-4-1-mini | gpt-4-1 |
|---|---|---|---|---|
| conceito | 96 | 70.8 (96) | 83.3 (96) | 89.6 (96) |
| mecanismo | 242 | 74.0 (242) | 88.4 (242) | 92.1 (242) |
| consequencia | 42 | 73.8 (42) | 85.7 (42) | 88.1 (42) |
| diagnostico | 178 | 46.1 (178) | 75.8 (178) | 86.0 (178) |
| decisao | 24 | 58.3 (24) | 75.0 (24) | 70.8 (24) |
| procedimento | 102 | 52.0 (102) | 78.4 (102) | 81.4 (102) |

## Por composição (acurácia %)

| Composição | gpt-4-1-nano | gpt-4-1-mini | gpt-4-1 |
|---|---|---|---|
| simples | 62.2 (590) | 82.2 (590) | 87.3 (590) |
| composta | 63.8 (94) | 83.0 (94) | 89.4 (94) |

## Cobertura

| Modelo | Total | Com nota | Sem nota | Cobertura (%) |
|---|---:|---:|---:|---:|
| gpt-4-1-nano | 684 | 684 | 0 | 100.0 |
| gpt-4-1-mini | 684 | 684 | 0 | 100.0 |
| gpt-4-1 | 684 | 684 | 0 | 100.0 |

Bloqueios terminais sem nota; excluídos da acurácia, reportados na cobertura.

## Por condição

| Condição | Modelo | Com nota | Corretas | Parciais | Incorretas | Sem nota | Acurácia (%) |
|---|---|---:|---:|---:|---:|---:|---:|
| closed_book | gpt-4-1-nano | 342 | 180 | 96 | 66 | 0 | 52.63 |
| closed_book | gpt-4-1-mini | 342 | 251 | 64 | 27 | 0 | 73.39 |
| closed_book | gpt-4-1 | 342 | 280 | 46 | 16 | 0 | 81.87 |
| open_book | gpt-4-1-nano | 342 | 247 | 61 | 34 | 0 | 72.22 |
| open_book | gpt-4-1-mini | 342 | 312 | 23 | 7 | 0 | 91.23 |
| open_book | gpt-4-1 | 342 | 319 | 17 | 6 | 0 | 93.27 |
