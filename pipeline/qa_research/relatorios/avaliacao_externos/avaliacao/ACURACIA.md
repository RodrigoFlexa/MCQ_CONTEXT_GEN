# Acurácia dos modelos sem contexto

Atualizado em 2026-11-08T23:11:32.417171+00:00. Questões prontas: 7626 em 40 tópicos. Juiz: `gpt-5-4-petrobras:medium`. GPT-4.1 Nano/Mini/Full, sem effort; até 100 palavras. Juiz GPT-5.4 medium; braços open/closed-book.
Acurácia = % de respostas corretas; "com parcial" conta a parcial como meio acerto.

## Geral

| Modelo | julgadas | acurácia (%) | com parcial (%) | corretas | parciais |
|---|---|---|---|---|---|
| llama-3-3-70b | 7622 | **37.6** | 50.0 | 2863 | 1898 |
| llama-3-1-8b | 7626 | **28.6** | 38.8 | 2181 | 1561 |

## Por tipo de questão (acurácia %, julgadas entre parênteses)

| Tipo | questões | llama-3-1-8b | llama-3-3-70b |
|---|---|---|---|
| conceito | 1636 | 35.8 (1636) | 51.9 (1636) |
| mecanismo | 1122 | 33.5 (1122) | 31.1 (1122) |
| consequencia | 324 | 43.5 (324) | 51.5 (324) |
| diagnostico | 1578 | 19.8 (1578) | 30.7 (1578) |
| decisao | 2032 | 25.5 (2032) | 34.4 (2030) |
| procedimento | 934 | 26.7 (934) | 33.9 (932) |

## Por composição (acurácia %)

| Composição | llama-3-1-8b | llama-3-3-70b |
|---|---|---|
| simples | 28.4 (7220) | 37.8 (7216) |
| composta | 32.5 (406) | 33.7 (406) |

## Cobertura

| Modelo | Total | Com nota | Sem nota | Cobertura (%) |
|---|---:|---:|---:|---:|
| llama-3-1-8b | 7626 | 7626 | 0 | 100.0 |
| llama-3-3-70b | 7626 | 7622 | 4 | 99.9 |

Bloqueios terminais sem nota; excluídos da acurácia, reportados na cobertura.

## Por condição

| Condição | Modelo | Com nota | Corretas | Parciais | Incorretas | Sem nota | Acurácia (%) |
|---|---|---:|---:|---:|---:|---:|---:|
| closed_book | llama-3-1-8b | 3813 | 579 | 851 | 2383 | 0 | 15.18 |
| closed_book | llama-3-3-70b | 3813 | 933 | 1016 | 1864 | 0 | 24.47 |
| open_book | llama-3-1-8b | 3813 | 1602 | 710 | 1501 | 0 | 42.01 |
| open_book | llama-3-3-70b | 3809 | 1930 | 882 | 997 | 4 | 50.67 |
