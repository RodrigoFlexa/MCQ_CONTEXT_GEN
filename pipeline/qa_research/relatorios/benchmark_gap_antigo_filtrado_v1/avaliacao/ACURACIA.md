# Acurácia dos modelos sem contexto

Atualizado em 2026-11-03T18:59:15.253894+00:00. Questões prontas: 1824 em 40 tópicos. Juiz: `gpt-5-4-petrobras:medium`. GPT-4.1 Nano/Mini/Full, sem effort; até 100 palavras. Juiz GPT-5.4 medium; braços open/closed-book.
Acurácia = % de respostas corretas; "com parcial" conta a parcial como meio acerto.

## Geral

| Modelo | julgadas | acurácia (%) | com parcial (%) | corretas | parciais |
|---|---|---|---|---|---|
| gpt-4-1 | 1824 | **85.2** | 90.0 | 1554 | 174 |
| gpt-4-1-mini | 1820 | **76.6** | 84.0 | 1394 | 269 |
| gpt-4-1-nano | 1824 | **57.8** | 69.9 | 1054 | 441 |

## Por tipo de questão (acurácia %, julgadas entre parênteses)

| Tipo | questões | gpt-4-1-nano | gpt-4-1-mini | gpt-4-1 |
|---|---|---|---|---|
| conceito | 378 | 59.3 (378) | 75.3 (377) | 83.3 (378) |
| mecanismo | 576 | 69.6 (576) | 84.0 (574) | 90.1 (576) |
| consequencia | 136 | 60.3 (136) | 83.1 (136) | 88.2 (136) |
| diagnostico | 326 | 43.9 (326) | 71.5 (326) | 85.3 (326) |
| decisao | 202 | 49.5 (202) | 67.8 (202) | 78.2 (202) |
| procedimento | 206 | 50.5 (206) | 70.7 (205) | 79.6 (206) |

## Por composição (acurácia %)

| Composição | gpt-4-1-nano | gpt-4-1-mini | gpt-4-1 |
|---|---|---|---|
| simples | 58.8 (1476) | 76.6 (1472) | 85.0 (1476) |
| composta | 53.4 (348) | 76.7 (348) | 86.2 (348) |

## Cobertura

| Modelo | Total | Com nota | Sem nota | Cobertura (%) |
|---|---:|---:|---:|---:|
| gpt-4-1-nano | 1824 | 1824 | 0 | 100.0 |
| gpt-4-1-mini | 1824 | 1820 | 4 | 99.8 |
| gpt-4-1 | 1824 | 1824 | 0 | 100.0 |

Bloqueios terminais sem nota; excluídos da acurácia, reportados na cobertura.

## Por condição

| Condição | Modelo | Com nota | Corretas | Parciais | Incorretas | Sem nota | Acurácia (%) |
|---|---|---:|---:|---:|---:|---:|---:|
| closed_book | gpt-4-1-nano | 912 | 347 | 298 | 267 | 0 | 38.05 |
| closed_book | gpt-4-1-mini | 912 | 548 | 221 | 143 | 0 | 60.09 |
| closed_book | gpt-4-1 | 912 | 668 | 154 | 90 | 0 | 73.25 |
| open_book | gpt-4-1-nano | 912 | 707 | 143 | 62 | 0 | 77.52 |
| open_book | gpt-4-1-mini | 908 | 846 | 48 | 14 | 4 | 93.17 |
| open_book | gpt-4-1 | 912 | 886 | 20 | 6 | 0 | 97.15 |
