# Acurácia dos modelos sem contexto

Atualizado em 2026-11-04T01:22:40.987622+00:00. Questões prontas: 1076 em 40 tópicos. Juiz: `gpt-5-4-petrobras:medium`. GPT-4.1 Nano/Mini/Full, sem effort; até 100 palavras. Juiz GPT-5.4 medium; braços open/closed-book.
Acurácia = % de respostas corretas; "com parcial" conta a parcial como meio acerto.

## Geral

| Modelo | julgadas | acurácia (%) | com parcial (%) | corretas | parciais |
|---|---|---|---|---|---|
| gpt-5-4 | 1076 | **91.6** | 94.8 | 986 | 69 |
| gpt-5 | 1076 | **91.4** | 94.4 | 984 | 63 |
| gpt-5-mini | 1076 | **80.4** | 86.5 | 865 | 131 |
| gpt-5-nano | 1076 | **65.2** | 75.4 | 702 | 218 |

## Por tipo de questão (acurácia %, julgadas entre parênteses)

| Tipo | questões | gpt-5-nano | gpt-5-mini | gpt-5 | gpt-5-4 |
|---|---|---|---|---|---|
| conceito | 172 | 66.3 (172) | 79.7 (172) | 90.7 (172) | 91.9 (172) |
| mecanismo | 295 | 78.3 (295) | 87.1 (295) | 96.3 (295) | 95.6 (295) |
| consequencia | 65 | 84.6 (65) | 90.8 (65) | 100.0 (65) | 98.5 (65) |
| diagnostico | 237 | 57.0 (237) | 76.8 (237) | 89.9 (237) | 94.9 (237) |
| decisao | 172 | 54.7 (172) | 77.9 (172) | 88.4 (172) | 87.2 (172) |
| procedimento | 135 | 54.1 (135) | 71.1 (135) | 84.4 (135) | 79.3 (135) |

## Por composição (acurácia %)

| Composição | gpt-5-nano | gpt-5-mini | gpt-5 | gpt-5-4 |
|---|---|---|---|---|
| simples | 65.9 (888) | 80.4 (888) | 91.3 (888) | 91.7 (888) |
| composta | 62.2 (188) | 80.3 (188) | 92.0 (188) | 91.5 (188) |

## Cobertura

| Modelo | Total | Com nota | Sem nota | Cobertura (%) |
|---|---:|---:|---:|---:|
| gpt-5-nano | 1076 | 1076 | 0 | 100.0 |
| gpt-5-mini | 1076 | 1076 | 0 | 100.0 |
| gpt-5 | 1076 | 1076 | 0 | 100.0 |
| gpt-5-4 | 1076 | 1076 | 0 | 100.0 |

Bloqueios terminais sem nota; excluídos da acurácia, reportados na cobertura.

## Por condição

| Condição | Modelo | Com nota | Corretas | Parciais | Incorretas | Sem nota | Acurácia (%) |
|---|---|---:|---:|---:|---:|---:|---:|
| closed_book | gpt-5-nano | 1076 | 702 | 218 | 156 | 0 | 65.24 |
| closed_book | gpt-5-mini | 1076 | 865 | 131 | 80 | 0 | 80.39 |
| closed_book | gpt-5 | 1076 | 984 | 63 | 29 | 0 | 91.45 |
| closed_book | gpt-5-4 | 1076 | 986 | 69 | 21 | 0 | 91.64 |
