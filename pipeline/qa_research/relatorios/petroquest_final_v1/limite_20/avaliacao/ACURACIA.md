# Acurácia dos modelos sem contexto

Atualizado em 2026-11-04T02:20:07.138731+00:00. Questões prontas: 301 em 40 tópicos. Juiz: `gpt-5-4-petrobras:medium`. GPT-4.1 Nano/Mini/Full, sem effort; até 100 palavras. Juiz GPT-5.4 medium; braços open/closed-book.
Acurácia = % de respostas corretas; "com parcial" conta a parcial como meio acerto.

## Geral

| Modelo | julgadas | acurácia (%) | com parcial (%) | corretas | parciais |
|---|---|---|---|---|---|
| gpt-5-4 | 301 | **89.4** | 92.9 | 269 | 21 |
| gpt-5 | 301 | **83.4** | 89.0 | 251 | 34 |
| gpt-5-mini | 301 | **69.8** | 77.2 | 210 | 45 |
| gpt-4-1 | 301 | **65.8** | 76.4 | 198 | 64 |
| gpt-5-nano | 301 | **52.2** | 62.6 | 157 | 63 |
| gpt-4-1-mini | 301 | **51.5** | 64.0 | 155 | 75 |
| gpt-4-1-nano | 301 | **31.9** | 47.3 | 96 | 93 |

## Por tipo de questão (acurácia %, julgadas entre parênteses)

| Tipo | questões | gpt-4-1-nano | gpt-4-1-mini | gpt-4-1 | gpt-5-nano | gpt-5-mini | gpt-5 | gpt-5-4 |
|---|---|---|---|---|---|---|---|---|
| conceito | 47 | 27.7 (47) | 59.6 (47) | 72.3 (47) | 61.7 (47) | 68.1 (47) | 87.2 (47) | 87.2 (47) |
| mecanismo | 83 | 32.5 (83) | 54.2 (83) | 78.3 (83) | 65.1 (83) | 80.7 (83) | 89.2 (83) | 95.2 (83) |
| consequencia | 18 | 33.3 (18) | 55.6 (18) | 72.2 (18) | 66.7 (18) | 77.8 (18) | 100.0 (18) | 100.0 (18) |
| diagnostico | 67 | 34.3 (67) | 47.8 (67) | 64.2 (67) | 46.3 (67) | 73.1 (67) | 80.6 (67) | 91.0 (67) |
| decisao | 48 | 33.3 (48) | 54.2 (48) | 58.3 (48) | 41.7 (48) | 56.2 (48) | 77.1 (48) | 91.7 (48) |
| procedimento | 38 | 28.9 (38) | 36.8 (38) | 39.5 (38) | 28.9 (38) | 55.3 (38) | 71.1 (38) | 68.4 (38) |

## Por composição (acurácia %)

| Composição | gpt-4-1-nano | gpt-4-1-mini | gpt-4-1 | gpt-5-nano | gpt-5-mini | gpt-5 | gpt-5-4 |
|---|---|---|---|---|---|---|---|
| simples | 31.7 (249) | 53.0 (249) | 65.5 (249) | 51.0 (249) | 70.7 (249) | 81.9 (249) | 89.2 (249) |
| composta | 32.7 (52) | 44.2 (52) | 67.3 (52) | 57.7 (52) | 65.4 (52) | 90.4 (52) | 90.4 (52) |

## Cobertura

| Modelo | Total | Com nota | Sem nota | Cobertura (%) |
|---|---:|---:|---:|---:|
| gpt-4-1-nano | 301 | 301 | 0 | 100.0 |
| gpt-4-1-mini | 301 | 301 | 0 | 100.0 |
| gpt-4-1 | 301 | 301 | 0 | 100.0 |
| gpt-5-nano | 301 | 301 | 0 | 100.0 |
| gpt-5-mini | 301 | 301 | 0 | 100.0 |
| gpt-5 | 301 | 301 | 0 | 100.0 |
| gpt-5-4 | 301 | 301 | 0 | 100.0 |

Bloqueios terminais sem nota; excluídos da acurácia, reportados na cobertura.

## Por condição

| Condição | Modelo | Com nota | Corretas | Parciais | Incorretas | Sem nota | Acurácia (%) |
|---|---|---:|---:|---:|---:|---:|---:|
| closed_book | gpt-4-1-nano | 301 | 96 | 93 | 112 | 0 | 31.89 |
| closed_book | gpt-4-1-mini | 301 | 155 | 75 | 71 | 0 | 51.50 |
| closed_book | gpt-4-1 | 301 | 198 | 64 | 39 | 0 | 65.78 |
| closed_book | gpt-5-nano | 301 | 157 | 63 | 81 | 0 | 52.16 |
| closed_book | gpt-5-mini | 301 | 210 | 45 | 46 | 0 | 69.77 |
| closed_book | gpt-5 | 301 | 251 | 34 | 16 | 0 | 83.39 |
| closed_book | gpt-5-4 | 301 | 269 | 21 | 11 | 0 | 89.37 |
