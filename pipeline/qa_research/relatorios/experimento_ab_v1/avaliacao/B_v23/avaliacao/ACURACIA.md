# Acurácia dos modelos sem contexto

Atualizado em 2026-11-03T20:05:55.383781+00:00. Questões prontas: 602 em 3 tópicos. Juiz: `gpt-5-4-petrobras:medium`. GPT-4.1 Nano/Mini/Full, sem effort; até 100 palavras. Juiz GPT-5.4 medium; braços open/closed-book.
Acurácia = % de respostas corretas; "com parcial" conta a parcial como meio acerto.

## Geral

| Modelo | julgadas | acurácia (%) | com parcial (%) | corretas | parciais |
|---|---|---|---|---|---|
| gpt-4-1 | 602 | **78.9** | 84.7 | 475 | 70 |
| gpt-4-1-mini | 602 | **68.8** | 76.9 | 414 | 98 |
| gpt-4-1-nano | 602 | **40.2** | 51.9 | 242 | 141 |

## Por tipo de questão (acurácia %, julgadas entre parênteses)

| Tipo | questões | gpt-4-1-nano | gpt-4-1-mini | gpt-4-1 |
|---|---|---|---|---|
| conceito | 24 | 50.0 (24) | 75.0 (24) | 95.8 (24) |
| mecanismo | 98 | 48.0 (98) | 76.5 (98) | 81.6 (98) |
| consequencia | 16 | 50.0 (16) | 93.8 (16) | 93.8 (16) |
| diagnostico | 190 | 33.7 (190) | 67.4 (190) | 82.1 (190) |
| decisao | 192 | 42.2 (192) | 70.8 (192) | 77.1 (192) |
| procedimento | 82 | 36.6 (82) | 51.2 (82) | 64.6 (82) |

## Por composição (acurácia %)

| Composição | gpt-4-1-nano | gpt-4-1-mini | gpt-4-1 |
|---|---|---|---|
| simples | 40.0 (538) | 68.8 (538) | 78.6 (538) |
| composta | 42.2 (64) | 68.8 (64) | 81.2 (64) |

## Cobertura

| Modelo | Total | Com nota | Sem nota | Cobertura (%) |
|---|---:|---:|---:|---:|
| gpt-4-1-nano | 602 | 602 | 0 | 100.0 |
| gpt-4-1-mini | 602 | 602 | 0 | 100.0 |
| gpt-4-1 | 602 | 602 | 0 | 100.0 |

Bloqueios terminais sem nota; excluídos da acurácia, reportados na cobertura.

## Por condição

| Condição | Modelo | Com nota | Corretas | Parciais | Incorretas | Sem nota | Acurácia (%) |
|---|---|---:|---:|---:|---:|---:|---:|
| closed_book | gpt-4-1-nano | 301 | 95 | 79 | 127 | 0 | 31.56 |
| closed_book | gpt-4-1-mini | 301 | 167 | 67 | 67 | 0 | 55.48 |
| closed_book | gpt-4-1 | 301 | 215 | 45 | 41 | 0 | 71.43 |
| open_book | gpt-4-1-nano | 301 | 147 | 62 | 92 | 0 | 48.84 |
| open_book | gpt-4-1-mini | 301 | 247 | 31 | 23 | 0 | 82.06 |
| open_book | gpt-4-1 | 301 | 260 | 25 | 16 | 0 | 86.38 |
