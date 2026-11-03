# Acurácia dos modelos sem contexto

Atualizado em 2026-11-03T20:30:37.433925+00:00. Questões prontas: 301 em 3 tópicos. Juiz: `gpt-5-4-petrobras:medium`. GPT-4.1 Nano/Mini/Full, sem effort; até 100 palavras. Juiz GPT-5.4 medium; braços open/closed-book.
Acurácia = % de respostas corretas; "com parcial" conta a parcial como meio acerto.

## Geral

| Modelo | julgadas | acurácia (%) | com parcial (%) | corretas | parciais |
|---|---|---|---|---|---|
| gpt-5-4 | 301 | **91.4** | 94.2 | 275 | 17 |
| gpt-5-mini | 299 | **80.6** | 85.5 | 241 | 29 |

## Por tipo de questão (acurácia %, julgadas entre parênteses)

| Tipo | questões | gpt-5-mini | gpt-5-4 |
|---|---|---|---|
| conceito | 12 | 91.7 (12) | 100.0 (12) |
| mecanismo | 49 | 79.6 (49) | 91.8 (49) |
| consequencia | 8 | 100.0 (8) | 100.0 (8) |
| diagnostico | 95 | 85.3 (95) | 94.7 (95) |
| decisao | 96 | 80.9 (94) | 91.7 (96) |
| procedimento | 41 | 63.4 (41) | 78.0 (41) |

## Por composição (acurácia %)

| Composição | gpt-5-mini | gpt-5-4 |
|---|---|---|
| simples | 80.9 (267) | 91.4 (269) |
| composta | 78.1 (32) | 90.6 (32) |

## Cobertura

| Modelo | Total | Com nota | Sem nota | Cobertura (%) |
|---|---:|---:|---:|---:|
| gpt-5-mini | 301 | 299 | 2 | 99.3 |
| gpt-5-4 | 301 | 301 | 0 | 100.0 |

Bloqueios terminais sem nota; excluídos da acurácia, reportados na cobertura.

## Por condição

| Condição | Modelo | Com nota | Corretas | Parciais | Incorretas | Sem nota | Acurácia (%) |
|---|---|---:|---:|---:|---:|---:|---:|
| closed_book | gpt-5-mini | 299 | 241 | 29 | 29 | 2 | 80.60 |
| closed_book | gpt-5-4 | 301 | 275 | 17 | 9 | 0 | 91.36 |
