# Acurácia dos modelos sem contexto

Atualizado em 2026-10-28T01:58:23.907683+00:00. Questões prontas: 798 em 40 tópicos. Juiz: `gpt-5-4-petrobras:medium`. Respondentes com esforço low (os gpt-4-1 não têm esforço).
Acurácia = % de respostas corretas; "com parcial" conta a parcial como meio acerto.

## Geral

| Modelo | julgadas | acurácia (%) | com parcial (%) | corretas | parciais |
|---|---|---|---|---|---|
| gpt-5-4 | 798 | **89.8** | 94.2 | 717 | 69 |
| gpt-5-4-nano | 798 | **73.4** | 82.5 | 586 | 144 |

## Por tipo de questão (acurácia %, julgadas entre parênteses)

| Tipo | questões | gpt-5-4-nano | gpt-5-4 |
|---|---|---|---|
| conceito | 476 | 77.3 (476) | 93.7 (476) |
| mecanismo | 49 | 85.7 (49) | 95.9 (49) |
| consequencia | 35 | 88.6 (35) | 100.0 (35) |
| diagnostico | 14 | 85.7 (14) | 78.6 (14) |
| decisao | 147 | 57.1 (147) | 78.9 (147) |
| procedimento | 77 | 63.6 (77) | 80.5 (77) |

## Por composição (acurácia %)

| Composição | gpt-5-4-nano | gpt-5-4 |
|---|---|---|
| simples | 76.9 (640) | 93.0 (640) |
| composta | 59.5 (158) | 77.2 (158) |

## Por conjunto de origem

| Conjunto | Modelo | Julgadas | Acurácia (%) | Com parcial (%) |
|---|---|---:|---:|---:|
| MCQs autorais do especialista | gpt-5-4-nano | 623 | 77.0 | 84.3 |
| MCQs autorais do especialista | gpt-5-4 | 623 | 92.6 | 95.5 |
| MCQs revisadas e aprovadas pelo especialista | gpt-5-4-nano | 175 | 60.6 | 76.0 |
| MCQs revisadas e aprovadas pelo especialista | gpt-5-4 | 175 | 80.0 | 89.4 |

## Cobertura da avaliação

Bloqueios são resultados terminais sem nota técnica; ficam fora do denominador da acurácia e são mostrados na cobertura.

| Modelo | Total | Processadas | Julgadas | Bloqueio respondente | Bloqueio juiz | Cobertura (%) |
|---|---:|---:|---:|---:|---:|---:|
| gpt-5-4-nano | 798 | 798 | 798 | 0 | 0 | 100.0 |
| gpt-5-4 | 798 | 798 | 798 | 0 | 0 | 100.0 |
