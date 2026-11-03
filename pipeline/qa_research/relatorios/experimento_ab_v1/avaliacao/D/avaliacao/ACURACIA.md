# Acurácia dos modelos sem contexto

Atualizado em 2026-11-02T23:26:22.243297+00:00. Questões prontas: 580 em 3 tópicos. Juiz: `gpt-5-4-petrobras:medium`. GPT-4.1 Nano/Mini/Full, sem effort; até 100 palavras. Juiz GPT-5.4 medium; braços open/closed-book.
Acurácia = % de respostas corretas; "com parcial" conta a parcial como meio acerto.

## Geral

| Modelo | julgadas | acurácia (%) | com parcial (%) | corretas | parciais |
|---|---|---|---|---|---|
| gpt-4-1 | 580 | **85.7** | 90.9 | 497 | 60 |
| gpt-4-1-mini | 580 | **77.2** | 84.6 | 448 | 85 |
| gpt-4-1-nano | 580 | **62.1** | 71.8 | 360 | 113 |

## Por tipo de questão (acurácia %, julgadas entre parênteses)

| Tipo | questões | gpt-4-1-nano | gpt-4-1-mini | gpt-4-1 |
|---|---|---|---|---|
| conceito | 100 | 60.0 (100) | 73.0 (100) | 87.0 (100) |
| mecanismo | 200 | 77.0 (200) | 85.5 (200) | 92.0 (200) |
| consequencia | 46 | 63.0 (46) | 87.0 (46) | 80.4 (46) |
| diagnostico | 136 | 44.1 (136) | 66.9 (136) | 82.4 (136) |
| decisao | 26 | 57.7 (26) | 84.6 (26) | 88.5 (26) |
| procedimento | 72 | 58.3 (72) | 70.8 (72) | 75.0 (72) |

## Por composição (acurácia %)

| Composição | gpt-4-1-nano | gpt-4-1-mini | gpt-4-1 |
|---|---|---|---|
| simples | 62.9 (498) | 76.9 (498) | 86.3 (498) |
| composta | 57.3 (82) | 79.3 (82) | 81.7 (82) |

## Cobertura

| Modelo | Total | Com nota | Sem nota | Cobertura (%) |
|---|---:|---:|---:|---:|
| gpt-4-1-nano | 580 | 580 | 0 | 100.0 |
| gpt-4-1-mini | 580 | 580 | 0 | 100.0 |
| gpt-4-1 | 580 | 580 | 0 | 100.0 |

Bloqueios terminais sem nota; excluídos da acurácia, reportados na cobertura.

## Por condição

| Condição | Modelo | Com nota | Corretas | Parciais | Incorretas | Sem nota | Acurácia (%) |
|---|---|---:|---:|---:|---:|---:|---:|
| closed_book | gpt-4-1-nano | 290 | 147 | 77 | 66 | 0 | 50.69 |
| closed_book | gpt-4-1-mini | 290 | 193 | 60 | 37 | 0 | 66.55 |
| closed_book | gpt-4-1 | 290 | 223 | 50 | 17 | 0 | 76.90 |
| open_book | gpt-4-1-nano | 290 | 213 | 36 | 41 | 0 | 73.45 |
| open_book | gpt-4-1-mini | 290 | 255 | 25 | 10 | 0 | 87.93 |
| open_book | gpt-4-1 | 290 | 274 | 10 | 6 | 0 | 94.48 |
