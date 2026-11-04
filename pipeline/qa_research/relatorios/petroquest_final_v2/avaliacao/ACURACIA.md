# Acurácia dos modelos sem contexto

Atualizado em 2026-11-04T19:23:20.565650+00:00. Questões prontas: 3858 em 40 tópicos. Juiz: `gpt-5-4-petrobras:medium`. GPT-4.1 Nano/Mini/Full, sem effort; até 100 palavras. Juiz GPT-5.4 medium; braços open/closed-book.
Acurácia = % de respostas corretas; "com parcial" conta a parcial como meio acerto.

## Geral

| Modelo | julgadas | acurácia (%) | com parcial (%) | corretas | parciais |
|---|---|---|---|---|---|
| gpt-5-4 | 3858 | **90.1** | 93.5 | 3476 | 260 |
| gpt-5 | 3858 | **84.8** | 89.5 | 3270 | 364 |
| gpt-5-mini | 3857 | **74.8** | 82.0 | 2884 | 555 |
| gpt-4-1 | 3858 | **73.0** | 80.9 | 2815 | 616 |
| gpt-4-1-mini | 3858 | **62.9** | 73.0 | 2425 | 779 |
| gpt-5-nano | 3857 | **60.7** | 69.5 | 2342 | 681 |
| gpt-4-1-nano | 3858 | **36.6** | 49.8 | 1412 | 1019 |

## Por tipo de questão (acurácia %, julgadas entre parênteses)

| Tipo | questões | gpt-4-1-nano | gpt-4-1-mini | gpt-4-1 | gpt-5-nano | gpt-5-mini | gpt-5 | gpt-5-4 |
|---|---|---|---|---|---|---|---|---|
| conceito | 398 | 43.7 (398) | 73.1 (398) | 77.6 (398) | 71.9 (398) | 80.4 (398) | 88.9 (398) | 91.5 (398) |
| mecanismo | 702 | 41.3 (702) | 71.1 (702) | 80.8 (702) | 70.2 (702) | 81.8 (702) | 90.2 (702) | 94.0 (702) |
| consequencia | 160 | 40.6 (160) | 70.6 (160) | 76.9 (160) | 67.5 (160) | 85.0 (160) | 86.9 (160) | 91.2 (160) |
| diagnostico | 864 | 32.3 (864) | 62.7 (864) | 74.1 (864) | 56.8 (863) | 76.3 (864) | 85.4 (864) | 92.1 (864) |
| decisao | 1268 | 35.9 (1268) | 58.9 (1268) | 69.2 (1268) | 56.9 (1268) | 71.0 (1267) | 83.0 (1268) | 88.6 (1268) |
| procedimento | 466 | 32.0 (466) | 50.0 (466) | 63.9 (466) | 52.1 (466) | 63.3 (466) | 76.0 (466) | 83.0 (466) |

## Por composição (acurácia %)

| Composição | gpt-4-1-nano | gpt-4-1-mini | gpt-4-1 | gpt-5-nano | gpt-5-mini | gpt-5 | gpt-5-4 |
|---|---|---|---|---|---|---|---|
| simples | 36.9 (3180) | 63.6 (3180) | 73.8 (3180) | 61.3 (3179) | 75.2 (3180) | 85.5 (3180) | 90.1 (3180) |
| composta | 35.1 (678) | 59.6 (678) | 69.0 (678) | 57.8 (678) | 73.0 (677) | 81.4 (678) | 90.0 (678) |

## Cobertura

| Modelo | Total | Com nota | Sem nota | Cobertura (%) |
|---|---:|---:|---:|---:|
| gpt-4-1-nano | 3858 | 3858 | 0 | 100.0 |
| gpt-4-1-mini | 3858 | 3858 | 0 | 100.0 |
| gpt-4-1 | 3858 | 3858 | 0 | 100.0 |
| gpt-5-nano | 3858 | 3857 | 1 | 100.0 |
| gpt-5-mini | 3858 | 3857 | 1 | 100.0 |
| gpt-5 | 3858 | 3858 | 0 | 100.0 |
| gpt-5-4 | 3858 | 3858 | 0 | 100.0 |

Bloqueios terminais sem nota; excluídos da acurácia, reportados na cobertura.

## Por condição

| Condição | Modelo | Com nota | Corretas | Parciais | Incorretas | Sem nota | Acurácia (%) |
|---|---|---:|---:|---:|---:|---:|---:|
| closed_book | gpt-4-1-nano | 1929 | 475 | 549 | 905 | 0 | 24.62 |
| closed_book | gpt-4-1-mini | 1929 | 870 | 547 | 512 | 0 | 45.10 |
| closed_book | gpt-4-1 | 1929 | 1110 | 478 | 341 | 0 | 57.54 |
| closed_book | gpt-5-nano | 1928 | 872 | 458 | 598 | 1 | 45.23 |
| closed_book | gpt-5-mini | 1928 | 1231 | 370 | 327 | 1 | 63.85 |
| closed_book | gpt-5 | 1929 | 1454 | 281 | 194 | 0 | 75.38 |
| closed_book | gpt-5-4 | 1929 | 1606 | 213 | 110 | 0 | 83.26 |
| open_book | gpt-4-1-nano | 1929 | 937 | 470 | 522 | 0 | 48.57 |
| open_book | gpt-4-1-mini | 1929 | 1555 | 232 | 142 | 0 | 80.61 |
| open_book | gpt-4-1 | 1929 | 1705 | 138 | 86 | 0 | 88.39 |
| open_book | gpt-5-nano | 1929 | 1470 | 223 | 236 | 0 | 76.21 |
| open_book | gpt-5-mini | 1929 | 1653 | 185 | 91 | 0 | 85.69 |
| open_book | gpt-5 | 1929 | 1816 | 83 | 30 | 0 | 94.14 |
| open_book | gpt-5-4 | 1929 | 1870 | 47 | 12 | 0 | 96.94 |
