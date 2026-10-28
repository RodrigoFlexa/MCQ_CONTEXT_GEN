# Acurácia dos modelos sem contexto

Atualizado em 2026-10-28T04:49:14.378860+00:00. Questões prontas: 670 em 40 tópicos. Juiz: `gpt-5-4-petrobras:medium`. Respondentes com esforço low (os gpt-4-1 não têm esforço).
Acurácia = % de respostas corretas; "com parcial" conta a parcial como meio acerto.

## Geral

| Modelo | julgadas | acurácia (%) | com parcial (%) | corretas | parciais |
|---|---|---|---|---|---|
| gpt-5-4 | 670 | **73.4** | 84.6 | 492 | 150 |
| gpt-5-4-nano | 669 | **54.0** | 71.6 | 361 | 236 |

## Por tipo de questão (acurácia %, julgadas entre parênteses)

| Tipo | questões | gpt-5-4-nano | gpt-5-4 |
|---|---|---|---|
| conceito | 54 | 55.6 (54) | 72.2 (54) |
| mecanismo | 90 | 71.1 (90) | 84.4 (90) |
| consequencia | 23 | 91.3 (23) | 95.7 (23) |
| diagnostico | 26 | 76.9 (26) | 80.8 (26) |
| decisao | 300 | 50.5 (299) | 74.3 (300) |
| procedimento | 177 | 42.4 (177) | 62.7 (177) |

## Por composição (acurácia %)

| Composição | gpt-5-4-nano | gpt-5-4 |
|---|---|---|
| simples | 64.1 (304) | 81.6 (304) |
| composta | 45.5 (365) | 66.7 (366) |

## Por conjunto de origem

| Conjunto | Modelo | Julgadas | Acurácia (%) | Com parcial (%) |
|---|---|---:|---:|---:|
| MCQs revisadas sem reprovação explícita | gpt-5-4-nano | 494 | 51.6 | 70.0 |
| MCQs revisadas sem reprovação explícita | gpt-5-4 | 495 | 71.1 | 82.9 |
| MCQs revisadas e aprovadas pelo especialista | gpt-5-4-nano | 175 | 60.6 | 76.0 |
| MCQs revisadas e aprovadas pelo especialista | gpt-5-4 | 175 | 80.0 | 89.4 |

## Por faixa do parecer humano

| Parecer da MCQ | Modelo | Julgadas | Acurácia (%) | Com parcial (%) |
|---|---|---:|---:|---:|
| Aprovação simples | gpt-5-4-nano | 419 | 56.8 | 73.3 |
| Aprovação simples | gpt-5-4 | 419 | 75.7 | 85.7 |
| Aprovação com observações | gpt-5-4-nano | 247 | 49.4 | 69.2 |
| Aprovação com observações | gpt-5-4 | 248 | 70.2 | 83.1 |
| Sem aprovação explícita | gpt-5-4-nano | 3 | 33.3 | 33.3 |
| Sem aprovação explícita | gpt-5-4 | 3 | 33.3 | 66.7 |

## Cobertura da avaliação

Bloqueios são resultados terminais sem nota técnica; ficam fora do denominador da acurácia e são mostrados na cobertura.

| Modelo | Total | Processadas | Julgadas | Bloqueio respondente | Bloqueio juiz | Cobertura (%) |
|---|---:|---:|---:|---:|---:|---:|
| gpt-5-4-nano | 670 | 670 | 669 | 1 | 0 | 99.9 |
| gpt-5-4 | 670 | 670 | 670 | 0 | 0 | 100.0 |
