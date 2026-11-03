# Acurácia dos modelos sem contexto

Atualizado em 2026-11-03T20:20:56.288711+00:00. Questões prontas: 107 em 3 tópicos. Juiz: `gpt-5-4-petrobras:medium`. GPT-4.1 Nano/Mini/Full, sem effort; até 100 palavras. Juiz GPT-5.4 medium; braços open/closed-book.
Acurácia = % de respostas corretas; "com parcial" conta a parcial como meio acerto.

## Geral

| Modelo | julgadas | acurácia (%) | com parcial (%) | corretas | parciais |
|---|---|---|---|---|---|
| gpt-5-4 | 107 | **92.5** | 94.4 | 99 | 4 |
| gpt-5-mini | 107 | **86.9** | 90.7 | 93 | 8 |

## Por tipo de questão (acurácia %, julgadas entre parênteses)

| Tipo | questões | gpt-5-mini | gpt-5-4 |
|---|---|---|---|
| conceito | 1 | 100.0 (1) | 100.0 (1) |
| mecanismo | 31 | 93.5 (31) | 93.5 (31) |
| consequencia | 21 | 90.5 (21) | 95.2 (21) |
| diagnostico | 34 | 82.4 (34) | 88.2 (34) |
| decisao | 9 | 77.8 (9) | 100.0 (9) |
| procedimento | 11 | 81.8 (11) | 90.9 (11) |

## Por composição (acurácia %)

| Composição | gpt-5-mini | gpt-5-4 |
|---|---|---|
| simples | 85.9 (92) | 91.3 (92) |
| composta | 93.3 (15) | 100.0 (15) |

## Cobertura

| Modelo | Total | Com nota | Sem nota | Cobertura (%) |
|---|---:|---:|---:|---:|
| gpt-5-mini | 107 | 107 | 0 | 100.0 |
| gpt-5-4 | 107 | 107 | 0 | 100.0 |

Bloqueios terminais sem nota; excluídos da acurácia, reportados na cobertura.

## Por condição

| Condição | Modelo | Com nota | Corretas | Parciais | Incorretas | Sem nota | Acurácia (%) |
|---|---|---:|---:|---:|---:|---:|---:|
| closed_book | gpt-5-mini | 107 | 93 | 8 | 6 | 0 | 86.92 |
| closed_book | gpt-5-4 | 107 | 99 | 4 | 4 | 0 | 92.52 |
