# Acurácia dos modelos sem contexto

Atualizado em 2026-11-12T03:59:26.622732+00:00. Questões prontas: 7000 em 40 tópicos. Juiz: `gpt-5-4-petrobras:medium`. GPT-4.1 Nano/Mini/Full, sem effort; até 100 palavras. Juiz GPT-5.4 medium; braços open/closed-book.
Acurácia = % de respostas corretas; "com parcial" conta a parcial como meio acerto.

## Geral

| Modelo | julgadas | acurácia (%) | com parcial (%) | corretas | parciais |
|---|---|---|---|---|---|
| gpt-5 | 6996 | **80.4** | 87.7 | 5622 | 1030 |
| gpt-5-mini | 6997 | **69.8** | 79.7 | 4885 | 1388 |
| gpt-4-1 | 6985 | **67.8** | 78.4 | 4733 | 1480 |
| gpt-4-1-mini | 6997 | **59.5** | 71.5 | 4162 | 1686 |

## Por tipo de questão (acurácia %, julgadas entre parênteses)

| Tipo | questões | gpt-4-1-mini | gpt-4-1 | gpt-5-mini | gpt-5 |
|---|---|---|---|---|---|
| conceito | 346 | 55.8 (346) | 64.7 (346) | 66.5 (346) | 73.7 (346) |
| mecanismo | 732 | 69.4 (732) | 76.3 (730) | 80.3 (732) | 89.6 (732) |
| consequencia | 288 | 67.0 (288) | 74.0 (288) | 79.9 (288) | 87.2 (288) |
| diagnostico | 832 | 64.3 (832) | 74.0 (831) | 76.1 (832) | 85.2 (831) |
| decisao | 2494 | 60.0 (2492) | 69.3 (2486) | 73.5 (2492) | 83.2 (2491) |
| procedimento | 2306 | 53.7 (2305) | 60.8 (2302) | 59.5 (2305) | 72.8 (2306) |

## Por composição (acurácia %)

| Composição | gpt-4-1-mini | gpt-4-1 | gpt-5-mini | gpt-5 |
|---|---|---|---|---|
| simples | 59.5 (6997) | 67.8 (6985) | 69.8 (6997) | 80.4 (6996) |
| composta | - (0) | - (0) | - (0) | - (0) |

## Cobertura

| Modelo | Total | Com nota | Sem nota | Cobertura (%) |
|---|---:|---:|---:|---:|
| gpt-4-1-mini | 7000 | 6997 | 3 | 100.0 |
| gpt-4-1 | 7000 | 6985 | 15 | 99.8 |
| gpt-5-mini | 7000 | 6997 | 3 | 100.0 |
| gpt-5 | 7000 | 6996 | 4 | 99.9 |

Bloqueios terminais sem nota; excluídos da acurácia, reportados na cobertura.

## Por condição

| Condição | Modelo | Com nota | Corretas | Parciais | Incorretas | Sem nota | Acurácia (%) |
|---|---|---:|---:|---:|---:|---:|---:|
| closed_book | gpt-4-1-mini | 3498 | 1636 | 1033 | 829 | 2 | 46.77 |
| closed_book | gpt-4-1 | 3489 | 2014 | 916 | 559 | 11 | 57.72 |
| closed_book | gpt-5-mini | 3498 | 2192 | 811 | 495 | 2 | 62.66 |
| closed_book | gpt-5 | 3497 | 2590 | 629 | 278 | 3 | 74.06 |
| open_book | gpt-4-1-mini | 3499 | 2526 | 653 | 320 | 1 | 72.19 |
| open_book | gpt-4-1 | 3496 | 2719 | 564 | 213 | 4 | 77.77 |
| open_book | gpt-5-mini | 3499 | 2693 | 577 | 229 | 1 | 76.96 |
| open_book | gpt-5 | 3499 | 3032 | 401 | 66 | 1 | 86.65 |
