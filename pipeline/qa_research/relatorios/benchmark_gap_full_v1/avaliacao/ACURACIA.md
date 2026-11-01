# Acurácia dos modelos sem contexto

Atualizado em 2026-11-01T07:04:06.448608+00:00. Questões prontas: 5636 em 40 tópicos. Juiz: `gpt-5-4-petrobras:medium`. GPT-4.1 Nano/Mini/Full, sem effort; até 100 palavras. Juiz GPT-5.4 medium; braços open/closed-book.
Acurácia = % de respostas corretas; "com parcial" conta a parcial como meio acerto.

## Geral

| Modelo | julgadas | acurácia (%) | com parcial (%) | corretas | parciais |
|---|---|---|---|---|---|
| gpt-4-1 | 5636 | **87.2** | 92.0 | 4916 | 541 |
| gpt-4-1-mini | 5636 | **81.0** | 87.7 | 4564 | 760 |
| gpt-4-1-nano | 5635 | **63.3** | 75.1 | 3566 | 1329 |

## Por tipo de questão (acurácia %, julgadas entre parênteses)

| Tipo | questões | gpt-4-1-nano | gpt-4-1-mini | gpt-4-1 |
|---|---|---|---|---|
| conceito | 902 | 61.5 (902) | 77.9 (902) | 84.4 (902) |
| mecanismo | 1914 | 77.1 (1914) | 88.7 (1914) | 93.8 (1914) |
| consequencia | 414 | 62.1 (414) | 83.6 (414) | 87.0 (414) |
| diagnostico | 1176 | 53.4 (1176) | 78.1 (1176) | 86.6 (1176) |
| decisao | 482 | 59.1 (482) | 79.3 (482) | 85.9 (482) |
| procedimento | 748 | 49.0 (747) | 69.1 (748) | 75.8 (748) |

## Por composição (acurácia %)

| Composição | gpt-4-1-nano | gpt-4-1-mini | gpt-4-1 |
|---|---|---|---|
| simples | 63.8 (4479) | 81.0 (4480) | 87.3 (4480) |
| composta | 61.3 (1156) | 80.9 (1156) | 86.9 (1156) |

## Cobertura

| Modelo | Total | Com nota | Sem nota | Cobertura (%) |
|---|---:|---:|---:|---:|
| gpt-4-1-nano | 5636 | 5635 | 1 | 100.0 |
| gpt-4-1-mini | 5636 | 5636 | 0 | 100.0 |
| gpt-4-1 | 5636 | 5636 | 0 | 100.0 |

Bloqueios terminais sem nota; excluídos da acurácia, reportados na cobertura.

## Por condição

| Condição | Modelo | Com nota | Corretas | Parciais | Incorretas | Sem nota | Acurácia (%) |
|---|---|---:|---:|---:|---:|---:|---:|
| closed_book | gpt-4-1-nano | 2817 | 1408 | 848 | 561 | 1 | 49.98 |
| closed_book | gpt-4-1-mini | 2818 | 1917 | 621 | 280 | 0 | 68.03 |
| closed_book | gpt-4-1 | 2818 | 2218 | 444 | 156 | 0 | 78.71 |
| open_book | gpt-4-1-nano | 2818 | 2158 | 481 | 179 | 0 | 76.58 |
| open_book | gpt-4-1-mini | 2818 | 2647 | 139 | 32 | 0 | 93.93 |
| open_book | gpt-4-1 | 2818 | 2698 | 97 | 23 | 0 | 95.74 |
