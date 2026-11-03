# Acurácia dos modelos sem contexto

Atualizado em 2026-11-03T20:17:15.655943+00:00. Questões prontas: 342 em 3 tópicos. Juiz: `gpt-5-4-petrobras:medium`. GPT-4.1 Nano/Mini/Full, sem effort; até 100 palavras. Juiz GPT-5.4 medium; braços open/closed-book.
Acurácia = % de respostas corretas; "com parcial" conta a parcial como meio acerto.

## Geral

| Modelo | julgadas | acurácia (%) | com parcial (%) | corretas | parciais |
|---|---|---|---|---|---|
| gpt-5-4 | 342 | **94.4** | 96.8 | 323 | 16 |
| gpt-5-mini | 341 | **85.6** | 90.8 | 292 | 35 |

## Por tipo de questão (acurácia %, julgadas entre parênteses)

| Tipo | questões | gpt-5-mini | gpt-5-4 |
|---|---|---|---|
| conceito | 48 | 77.1 (48) | 97.9 (48) |
| mecanismo | 121 | 94.2 (121) | 99.2 (121) |
| consequencia | 21 | 90.5 (21) | 85.7 (21) |
| diagnostico | 89 | 86.5 (89) | 93.3 (89) |
| decisao | 12 | 83.3 (12) | 83.3 (12) |
| procedimento | 51 | 70.0 (50) | 88.2 (51) |

## Por composição (acurácia %)

| Composição | gpt-5-mini | gpt-5-4 |
|---|---|---|
| simples | 84.4 (294) | 94.9 (295) |
| composta | 93.6 (47) | 91.5 (47) |

## Cobertura

| Modelo | Total | Com nota | Sem nota | Cobertura (%) |
|---|---:|---:|---:|---:|
| gpt-5-mini | 342 | 341 | 1 | 99.7 |
| gpt-5-4 | 342 | 342 | 0 | 100.0 |

Bloqueios terminais sem nota; excluídos da acurácia, reportados na cobertura.

## Por condição

| Condição | Modelo | Com nota | Corretas | Parciais | Incorretas | Sem nota | Acurácia (%) |
|---|---|---:|---:|---:|---:|---:|---:|
| closed_book | gpt-5-mini | 341 | 292 | 35 | 14 | 1 | 85.63 |
| closed_book | gpt-5-4 | 342 | 323 | 16 | 3 | 0 | 94.44 |
