# Acurácia dos modelos sem contexto

Atualizado em 2026-11-02T22:16:02.159510+00:00. Questões prontas: 560 em 3 tópicos. Juiz: `gpt-5-4-petrobras:medium`. GPT-4.1 Nano/Mini/Full, sem effort; até 100 palavras. Juiz GPT-5.4 medium; braços open/closed-book.
Acurácia = % de respostas corretas; "com parcial" conta a parcial como meio acerto.

## Geral

| Modelo | julgadas | acurácia (%) | com parcial (%) | corretas | parciais |
|---|---|---|---|---|---|
| gpt-4-1 | 560 | **89.3** | 93.7 | 500 | 49 |
| gpt-4-1-mini | 560 | **83.4** | 88.4 | 467 | 56 |
| gpt-4-1-nano | 560 | **62.3** | 73.8 | 349 | 129 |

## Por tipo de questão (acurácia %, julgadas entre parênteses)

| Tipo | questões | gpt-4-1-nano | gpt-4-1-mini | gpt-4-1 |
|---|---|---|---|---|
| conceito | 88 | 60.2 (88) | 72.7 (88) | 89.8 (88) |
| mecanismo | 214 | 77.6 (214) | 91.6 (214) | 94.4 (214) |
| consequencia | 28 | 82.1 (28) | 92.9 (28) | 96.4 (28) |
| diagnostico | 122 | 40.2 (122) | 79.5 (122) | 89.3 (122) |
| decisao | 32 | 53.1 (32) | 81.2 (32) | 78.1 (32) |
| procedimento | 76 | 53.9 (76) | 76.3 (76) | 76.3 (76) |

## Por composição (acurácia %)

| Composição | gpt-4-1-nano | gpt-4-1-mini | gpt-4-1 |
|---|---|---|---|
| simples | 63.9 (474) | 83.8 (474) | 89.9 (474) |
| composta | 53.5 (86) | 81.4 (86) | 86.0 (86) |

## Cobertura

| Modelo | Total | Com nota | Sem nota | Cobertura (%) |
|---|---:|---:|---:|---:|
| gpt-4-1-nano | 560 | 560 | 0 | 100.0 |
| gpt-4-1-mini | 560 | 560 | 0 | 100.0 |
| gpt-4-1 | 560 | 560 | 0 | 100.0 |

Bloqueios terminais sem nota; excluídos da acurácia, reportados na cobertura.

## Por condição

| Condição | Modelo | Com nota | Corretas | Parciais | Incorretas | Sem nota | Acurácia (%) |
|---|---|---:|---:|---:|---:|---:|---:|
| closed_book | gpt-4-1-nano | 280 | 140 | 83 | 57 | 0 | 50.00 |
| closed_book | gpt-4-1-mini | 280 | 204 | 44 | 32 | 0 | 72.86 |
| closed_book | gpt-4-1 | 280 | 229 | 42 | 9 | 0 | 81.79 |
| open_book | gpt-4-1-nano | 280 | 209 | 46 | 25 | 0 | 74.64 |
| open_book | gpt-4-1-mini | 280 | 263 | 12 | 5 | 0 | 93.93 |
| open_book | gpt-4-1 | 280 | 271 | 7 | 2 | 0 | 96.79 |
