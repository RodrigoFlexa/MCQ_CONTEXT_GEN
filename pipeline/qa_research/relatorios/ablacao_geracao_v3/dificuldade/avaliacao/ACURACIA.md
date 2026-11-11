# Acurácia dos modelos sem contexto

Atualizado em 2026-11-11T03:29:27.166201+00:00. Questões prontas: 5000 em 40 tópicos. Juiz: `gpt-5-4-petrobras:medium`. GPT-4.1 Nano/Mini/Full, sem effort; até 100 palavras. Juiz GPT-5.4 medium; braços open/closed-book.
Acurácia = % de respostas corretas; "com parcial" conta a parcial como meio acerto.

## Geral

| Modelo | julgadas | acurácia (%) | com parcial (%) | corretas | parciais |
|---|---|---|---|---|---|
| gpt-5 | 4996 | **77.6** | 86.4 | 3876 | 883 |
| gpt-5-mini | 4997 | **67.0** | 78.4 | 3347 | 1146 |
| gpt-4-1 | 4985 | **64.4** | 76.6 | 3208 | 1224 |
| gpt-4-1-mini | 4997 | **56.0** | 69.7 | 2798 | 1366 |

## Por tipo de questão (acurácia %, julgadas entre parênteses)

| Tipo | questões | gpt-4-1-mini | gpt-4-1 | gpt-5-mini | gpt-5 |
|---|---|---|---|---|---|
| conceito | 256 | 50.4 (256) | 59.0 (256) | 61.3 (256) | 68.0 (256) |
| mecanismo | 518 | 69.5 (518) | 75.2 (516) | 80.3 (518) | 89.4 (518) |
| consequencia | 190 | 63.2 (190) | 72.1 (190) | 78.4 (190) | 87.9 (190) |
| diagnostico | 610 | 62.8 (610) | 72.4 (609) | 74.4 (610) | 83.7 (609) |
| decisao | 1760 | 55.9 (1758) | 65.9 (1752) | 70.8 (1758) | 80.8 (1757) |
| procedimento | 1664 | 49.4 (1663) | 56.3 (1660) | 55.6 (1663) | 68.5 (1664) |

## Por composição (acurácia %)

| Composição | gpt-4-1-mini | gpt-4-1 | gpt-5-mini | gpt-5 |
|---|---|---|---|---|
| simples | 56.0 (4997) | 64.4 (4985) | 67.0 (4997) | 77.6 (4996) |
| composta | - (0) | - (0) | - (0) | - (0) |

## Cobertura

| Modelo | Total | Com nota | Sem nota | Cobertura (%) |
|---|---:|---:|---:|---:|
| gpt-4-1-mini | 5000 | 4997 | 3 | 99.9 |
| gpt-4-1 | 5000 | 4985 | 15 | 99.7 |
| gpt-5-mini | 5000 | 4997 | 3 | 99.9 |
| gpt-5 | 5000 | 4996 | 4 | 99.9 |

Bloqueios terminais sem nota; excluídos da acurácia, reportados na cobertura.

## Por condição

| Condição | Modelo | Com nota | Corretas | Parciais | Incorretas | Sem nota | Acurácia (%) |
|---|---|---:|---:|---:|---:|---:|---:|
| closed_book | gpt-4-1-mini | 2498 | 1141 | 787 | 570 | 2 | 45.68 |
| closed_book | gpt-4-1 | 2489 | 1397 | 715 | 377 | 11 | 56.13 |
| closed_book | gpt-5-mini | 2498 | 1526 | 645 | 327 | 2 | 61.09 |
| closed_book | gpt-5 | 2497 | 1805 | 513 | 179 | 3 | 72.29 |
| open_book | gpt-4-1-mini | 2499 | 1657 | 579 | 263 | 1 | 66.31 |
| open_book | gpt-4-1 | 2496 | 1811 | 509 | 176 | 4 | 72.56 |
| open_book | gpt-5-mini | 2499 | 1821 | 501 | 177 | 1 | 72.87 |
| open_book | gpt-5 | 2499 | 2071 | 370 | 58 | 1 | 82.87 |
