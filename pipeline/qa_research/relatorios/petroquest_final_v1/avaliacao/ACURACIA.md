# Acurácia dos modelos sem contexto

Atualizado em 2026-11-04T00:43:45.438680+00:00. Questões prontas: 2152 em 40 tópicos. Juiz: `gpt-5-4-petrobras:medium`. GPT-4.1 Nano/Mini/Full, sem effort; até 100 palavras. Juiz GPT-5.4 medium; braços open/closed-book.
Acurácia = % de respostas corretas; "com parcial" conta a parcial como meio acerto.

## Geral

| Modelo | julgadas | acurácia (%) | com parcial (%) | corretas | parciais |
|---|---|---|---|---|---|
| gpt-4-1 | 2152 | **83.7** | 88.9 | 1802 | 221 |
| gpt-4-1-mini | 2148 | **74.4** | 82.2 | 1598 | 335 |
| gpt-4-1-nano | 2152 | **53.0** | 65.3 | 1140 | 531 |

## Por tipo de questão (acurácia %, julgadas entre parênteses)

| Tipo | questões | gpt-4-1-nano | gpt-4-1-mini | gpt-4-1 |
|---|---|---|---|---|
| conceito | 344 | 59.0 (344) | 74.0 (342) | 82.8 (344) |
| mecanismo | 590 | 65.1 (590) | 82.5 (589) | 89.5 (590) |
| consequencia | 130 | 61.5 (130) | 86.2 (130) | 91.5 (130) |
| diagnostico | 474 | 41.1 (474) | 70.3 (474) | 85.7 (474) |
| decisao | 344 | 44.8 (344) | 70.1 (344) | 77.3 (344) |
| procedimento | 270 | 45.9 (270) | 64.3 (269) | 73.3 (270) |

## Por composição (acurácia %)

| Composição | gpt-4-1-nano | gpt-4-1-mini | gpt-4-1 |
|---|---|---|---|
| simples | 53.3 (1776) | 74.0 (1772) | 83.6 (1776) |
| composta | 51.6 (376) | 76.3 (376) | 84.6 (376) |

## Cobertura

| Modelo | Total | Com nota | Sem nota | Cobertura (%) |
|---|---:|---:|---:|---:|
| gpt-4-1-nano | 2152 | 2152 | 0 | 100.0 |
| gpt-4-1-mini | 2152 | 2148 | 4 | 99.8 |
| gpt-4-1 | 2152 | 2152 | 0 | 100.0 |

Bloqueios terminais sem nota; excluídos da acurácia, reportados na cobertura.

## Por condição

| Condição | Modelo | Com nota | Corretas | Parciais | Incorretas | Sem nota | Acurácia (%) |
|---|---|---:|---:|---:|---:|---:|---:|
| closed_book | gpt-4-1-nano | 1076 | 385 | 340 | 351 | 0 | 35.78 |
| closed_book | gpt-4-1-mini | 1072 | 628 | 259 | 185 | 4 | 58.58 |
| closed_book | gpt-4-1 | 1076 | 781 | 185 | 110 | 0 | 72.58 |
| open_book | gpt-4-1-nano | 1076 | 755 | 191 | 130 | 0 | 70.17 |
| open_book | gpt-4-1-mini | 1076 | 970 | 76 | 30 | 0 | 90.15 |
| open_book | gpt-4-1 | 1076 | 1021 | 36 | 19 | 0 | 94.89 |
