# Acurácia dos modelos sem contexto

Atualizado em 2026-11-02T23:02:21.133195+00:00. Questões prontas: 542 em 3 tópicos. Juiz: `gpt-5-4-petrobras:medium`. GPT-4.1 Nano/Mini/Full, sem effort; até 100 palavras. Juiz GPT-5.4 medium; braços open/closed-book.
Acurácia = % de respostas corretas; "com parcial" conta a parcial como meio acerto.

## Geral

| Modelo | julgadas | acurácia (%) | com parcial (%) | corretas | parciais |
|---|---|---|---|---|---|
| gpt-4-1 | 542 | **87.6** | 92.3 | 475 | 51 |
| gpt-4-1-mini | 542 | **81.4** | 87.7 | 441 | 69 |
| gpt-4-1-nano | 542 | **60.0** | 72.2 | 325 | 133 |

## Por tipo de questão (acurácia %, julgadas entre parênteses)

| Tipo | questões | gpt-4-1-nano | gpt-4-1-mini | gpt-4-1 |
|---|---|---|---|---|
| conceito | 92 | 57.6 (92) | 77.2 (92) | 84.8 (92) |
| mecanismo | 194 | 77.3 (194) | 90.2 (194) | 94.8 (194) |
| consequencia | 44 | 59.1 (44) | 77.3 (44) | 90.9 (44) |
| diagnostico | 126 | 42.1 (126) | 77.8 (126) | 87.3 (126) |
| decisao | 22 | 45.5 (22) | 77.3 (22) | 86.4 (22) |
| procedimento | 64 | 51.6 (64) | 71.9 (64) | 68.8 (64) |

## Por composição (acurácia %)

| Composição | gpt-4-1-nano | gpt-4-1-mini | gpt-4-1 |
|---|---|---|---|
| simples | 60.9 (460) | 80.9 (460) | 87.2 (460) |
| composta | 54.9 (82) | 84.1 (82) | 90.2 (82) |

## Cobertura

| Modelo | Total | Com nota | Sem nota | Cobertura (%) |
|---|---:|---:|---:|---:|
| gpt-4-1-nano | 542 | 542 | 0 | 100.0 |
| gpt-4-1-mini | 542 | 542 | 0 | 100.0 |
| gpt-4-1 | 542 | 542 | 0 | 100.0 |

Bloqueios terminais sem nota; excluídos da acurácia, reportados na cobertura.

## Por condição

| Condição | Modelo | Com nota | Corretas | Parciais | Incorretas | Sem nota | Acurácia (%) |
|---|---|---:|---:|---:|---:|---:|---:|
| closed_book | gpt-4-1-nano | 271 | 127 | 91 | 53 | 0 | 46.86 |
| closed_book | gpt-4-1-mini | 271 | 188 | 59 | 24 | 0 | 69.37 |
| closed_book | gpt-4-1 | 271 | 220 | 40 | 11 | 0 | 81.18 |
| open_book | gpt-4-1-nano | 271 | 198 | 42 | 31 | 0 | 73.06 |
| open_book | gpt-4-1-mini | 271 | 253 | 10 | 8 | 0 | 93.36 |
| open_book | gpt-4-1 | 271 | 255 | 11 | 5 | 0 | 94.10 |
