# Acurácia dos modelos sem contexto

Atualizado em 2026-11-05T19:46:18.563769+00:00. Questões prontas: 6914 em 40 tópicos. Juiz: `gpt-5-4-petrobras:medium`. GPT-4.1 Nano/Mini/Full, sem effort; até 100 palavras. Juiz GPT-5.4 medium; braços open/closed-book.
Acurácia = % de respostas corretas; "com parcial" conta a parcial como meio acerto.

## Geral

| Modelo | julgadas | acurácia (%) | com parcial (%) | corretas | parciais |
|---|---|---|---|---|---|
| gpt-5-4 | 6913 | **89.5** | 92.9 | 6187 | 471 |
| gpt-5 | 6914 | **85.2** | 89.7 | 5889 | 631 |
| gpt-5-mini | 6912 | **74.8** | 82.0 | 5169 | 1004 |
| gpt-4-1 | 6914 | **72.5** | 80.5 | 5012 | 1101 |
| gpt-4-1-mini | 6914 | **63.8** | 73.4 | 4409 | 1330 |
| gpt-5-nano | 6913 | **61.5** | 70.4 | 4253 | 1223 |
| gpt-4-1-nano | 6914 | **36.9** | 49.6 | 2553 | 1759 |

## Por tipo de questão (acurácia %, julgadas entre parênteses)

| Tipo | questões | gpt-4-1-nano | gpt-4-1-mini | gpt-4-1 | gpt-5-nano | gpt-5-mini | gpt-5 | gpt-5-4 |
|---|---|---|---|---|---|---|---|---|
| conceito | 2090 | 36.9 (2090) | 66.7 (2090) | 74.3 (2090) | 63.4 (2090) | 76.7 (2090) | 87.2 (2090) | 89.7 (2090) |
| mecanismo | 1568 | 39.9 (1568) | 66.9 (1568) | 74.8 (1568) | 66.6 (1568) | 76.5 (1567) | 86.3 (1568) | 90.9 (1567) |
| consequencia | 430 | 41.2 (430) | 70.2 (430) | 73.5 (430) | 66.0 (430) | 80.7 (430) | 86.5 (430) | 89.1 (430) |
| diagnostico | 908 | 32.2 (908) | 61.7 (908) | 73.6 (908) | 55.5 (907) | 76.2 (908) | 85.7 (908) | 92.2 (908) |
| decisao | 1306 | 35.8 (1306) | 59.0 (1306) | 68.8 (1306) | 56.3 (1306) | 70.0 (1305) | 82.4 (1306) | 87.7 (1306) |
| procedimento | 612 | 35.9 (612) | 54.6 (612) | 66.0 (612) | 59.0 (612) | 68.0 (612) | 79.6 (612) | 85.3 (612) |

## Por composição (acurácia %)

| Composição | gpt-4-1-nano | gpt-4-1-mini | gpt-4-1 | gpt-5-nano | gpt-5-mini | gpt-5 | gpt-5-4 |
|---|---|---|---|---|---|---|---|
| simples | 37.0 (6270) | 64.1 (6270) | 72.8 (6270) | 61.9 (6269) | 74.9 (6269) | 85.5 (6270) | 89.4 (6269) |
| composta | 35.7 (644) | 60.4 (644) | 69.4 (644) | 58.2 (644) | 73.3 (643) | 82.3 (644) | 90.7 (644) |

## Cobertura

| Modelo | Total | Com nota | Sem nota | Cobertura (%) |
|---|---:|---:|---:|---:|
| gpt-4-1-nano | 6914 | 6914 | 0 | 100.0 |
| gpt-4-1-mini | 6914 | 6914 | 0 | 100.0 |
| gpt-4-1 | 6914 | 6914 | 0 | 100.0 |
| gpt-5-nano | 6914 | 6913 | 1 | 100.0 |
| gpt-5-mini | 6914 | 6912 | 2 | 100.0 |
| gpt-5 | 6914 | 6914 | 0 | 100.0 |
| gpt-5-4 | 6914 | 6913 | 1 | 100.0 |

Bloqueios terminais sem nota; excluídos da acurácia, reportados na cobertura.

## Por condição

| Condição | Modelo | Com nota | Corretas | Parciais | Incorretas | Sem nota | Acurácia (%) |
|---|---|---:|---:|---:|---:|---:|---:|
| closed_book | gpt-4-1-nano | 3457 | 894 | 942 | 1621 | 0 | 25.86 |
| closed_book | gpt-4-1-mini | 3457 | 1576 | 959 | 922 | 0 | 45.59 |
| closed_book | gpt-4-1 | 3457 | 1949 | 846 | 662 | 0 | 56.38 |
| closed_book | gpt-5-nano | 3456 | 1582 | 831 | 1043 | 1 | 45.78 |
| closed_book | gpt-5-mini | 3455 | 2185 | 685 | 585 | 2 | 63.24 |
| closed_book | gpt-5 | 3457 | 2607 | 503 | 347 | 0 | 75.41 |
| closed_book | gpt-5-4 | 3456 | 2815 | 405 | 236 | 1 | 81.45 |
| open_book | gpt-4-1-nano | 3457 | 1659 | 817 | 981 | 0 | 47.99 |
| open_book | gpt-4-1-mini | 3457 | 2833 | 371 | 253 | 0 | 81.95 |
| open_book | gpt-4-1 | 3457 | 3063 | 255 | 139 | 0 | 88.60 |
| open_book | gpt-5-nano | 3457 | 2671 | 392 | 394 | 0 | 77.26 |
| open_book | gpt-5-mini | 3457 | 2984 | 319 | 154 | 0 | 86.32 |
| open_book | gpt-5 | 3457 | 3282 | 128 | 47 | 0 | 94.94 |
| open_book | gpt-5-4 | 3457 | 3372 | 66 | 19 | 0 | 97.54 |
