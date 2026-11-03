# Acurácia dos modelos sem contexto

Atualizado em 2026-11-03T19:56:12.551149+00:00. Questões prontas: 912 em 40 tópicos. Juiz: `gpt-5-4-petrobras:medium`. GPT-4.1 Nano/Mini/Full, sem effort; até 100 palavras. Juiz GPT-5.4 medium; braços open/closed-book.
Acurácia = % de respostas corretas; "com parcial" conta a parcial como meio acerto.

## Geral

| Modelo | julgadas | acurácia (%) | com parcial (%) | corretas | parciais |
|---|---|---|---|---|---|
| gpt-5-4 | 903 | **92.4** | 95.1 | 834 | 49 |
| gpt-5-mini | 912 | **79.1** | 85.6 | 721 | 120 |

## Por tipo de questão (acurácia %, julgadas entre parênteses)

| Tipo | questões | gpt-5-mini | gpt-5-4 |
|---|---|---|---|
| conceito | 189 | 73.5 (189) | 90.9 (187) |
| mecanismo | 288 | 88.9 (288) | 96.1 (285) |
| consequencia | 68 | 83.8 (68) | 95.6 (68) |
| diagnostico | 163 | 72.4 (163) | 94.5 (163) |
| decisao | 101 | 72.3 (101) | 86.7 (98) |
| procedimento | 103 | 75.7 (103) | 84.3 (102) |

## Por composição (acurácia %)

| Composição | gpt-5-mini | gpt-5-4 |
|---|---|---|
| simples | 79.0 (738) | 92.6 (730) |
| composta | 79.3 (174) | 91.3 (173) |

## Cobertura

| Modelo | Total | Com nota | Sem nota | Cobertura (%) |
|---|---:|---:|---:|---:|
| gpt-5-mini | 912 | 912 | 0 | 100.0 |
| gpt-5-4 | 912 | 903 | 9 | 99.0 |

Bloqueios terminais sem nota; excluídos da acurácia, reportados na cobertura.

## Por condição

| Condição | Modelo | Com nota | Corretas | Parciais | Incorretas | Sem nota | Acurácia (%) |
|---|---|---:|---:|---:|---:|---:|---:|
| closed_book | gpt-5-mini | 912 | 721 | 120 | 71 | 0 | 79.06 |
| closed_book | gpt-5-4 | 903 | 834 | 49 | 20 | 9 | 92.36 |
