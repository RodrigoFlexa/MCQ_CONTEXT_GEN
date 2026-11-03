# Acurácia dos modelos sem contexto

Atualizado em 2026-11-03T03:53:34.158187+00:00. Questões prontas: 214 em 3 tópicos. Juiz: `gpt-5-4-petrobras:medium`. GPT-4.1 Nano/Mini/Full, sem effort; até 100 palavras. Juiz GPT-5.4 medium; braços open/closed-book.
Acurácia = % de respostas corretas; "com parcial" conta a parcial como meio acerto.

## Geral

| Modelo | julgadas | acurácia (%) | com parcial (%) | corretas | parciais |
|---|---|---|---|---|---|
| gpt-4-1 | 214 | **89.3** | 92.3 | 191 | 13 |
| gpt-4-1-mini | 214 | **77.6** | 84.6 | 166 | 30 |
| gpt-4-1-nano | 214 | **55.6** | 64.0 | 119 | 36 |

## Por tipo de questão (acurácia %, julgadas entre parênteses)

| Tipo | questões | gpt-4-1-nano | gpt-4-1-mini | gpt-4-1 |
|---|---|---|---|---|
| conceito | 2 | 50.0 (2) | 100.0 (2) | 100.0 (2) |
| mecanismo | 62 | 67.7 (62) | 79.0 (62) | 91.9 (62) |
| consequencia | 42 | 71.4 (42) | 90.5 (42) | 92.9 (42) |
| diagnostico | 68 | 38.2 (68) | 75.0 (68) | 88.2 (68) |
| decisao | 18 | 50.0 (18) | 66.7 (18) | 77.8 (18) |
| procedimento | 22 | 50.0 (22) | 63.6 (22) | 86.4 (22) |

## Por composição (acurácia %)

| Composição | gpt-4-1-nano | gpt-4-1-mini | gpt-4-1 |
|---|---|---|---|
| simples | 54.9 (184) | 78.8 (184) | 89.7 (184) |
| composta | 60.0 (30) | 70.0 (30) | 86.7 (30) |

## Cobertura

| Modelo | Total | Com nota | Sem nota | Cobertura (%) |
|---|---:|---:|---:|---:|
| gpt-4-1-nano | 214 | 214 | 0 | 100.0 |
| gpt-4-1-mini | 214 | 214 | 0 | 100.0 |
| gpt-4-1 | 214 | 214 | 0 | 100.0 |

Bloqueios terminais sem nota; excluídos da acurácia, reportados na cobertura.

## Por condição

| Condição | Modelo | Com nota | Corretas | Parciais | Incorretas | Sem nota | Acurácia (%) |
|---|---|---:|---:|---:|---:|---:|---:|
| closed_book | gpt-4-1-nano | 107 | 52 | 22 | 33 | 0 | 48.60 |
| closed_book | gpt-4-1-mini | 107 | 73 | 21 | 13 | 0 | 68.22 |
| closed_book | gpt-4-1 | 107 | 92 | 8 | 7 | 0 | 85.98 |
| open_book | gpt-4-1-nano | 107 | 67 | 14 | 26 | 0 | 62.62 |
| open_book | gpt-4-1-mini | 107 | 93 | 9 | 5 | 0 | 86.92 |
| open_book | gpt-4-1 | 107 | 99 | 5 | 3 | 0 | 92.52 |
