# Acurácia dos modelos sem contexto

Atualizado em 2026-10-29T00:47:58.786434+00:00. Questões prontas: 2000 em 40 tópicos. Juiz: `gpt-5-4-petrobras:medium`. Respondentes com esforço medium e limite solicitado de 100 palavras.
Acurácia = % de respostas corretas; "com parcial" conta a parcial como meio acerto.

## Geral

| Modelo | julgadas | acurácia (%) | com parcial (%) | corretas | parciais |
|---|---|---|---|---|---|
| gpt-5-4 | 1999 | **93.1** | 95.9 | 1861 | 111 |
| gpt-5-4-nano | 1998 | **80.5** | 87.3 | 1608 | 271 |

## Por tipo de questão (acurácia %, julgadas entre parênteses)

| Tipo | questões | gpt-5-4-nano | gpt-5-4 |
|---|---|---|---|
| conceito | 346 | 77.7 (346) | 94.8 (346) |
| mecanismo | 518 | 93.6 (516) | 97.9 (517) |
| consequencia | 186 | 92.5 (186) | 95.7 (186) |
| diagnostico | 390 | 80.5 (390) | 94.6 (390) |
| decisao | 279 | 73.8 (279) | 90.3 (279) |
| procedimento | 281 | 58.4 (281) | 81.1 (281) |

## Por composição (acurácia %)

| Composição | gpt-5-4-nano | gpt-5-4 |
|---|---|---|
| simples | 82.4 (1068) | 93.9 (1069) |
| composta | 78.3 (930) | 92.2 (930) |

## Cobertura

| Modelo | Total | Com nota | Sem nota | Cobertura (%) |
|---|---:|---:|---:|---:|
| gpt-5-4-nano | 2000 | 1998 | 2 | 99.9 |
| gpt-5-4 | 2000 | 1999 | 1 | 100.0 |

Bloqueios terminais sem nota; excluídos da acurácia, reportados na cobertura.

## Por condição

| Condição | Modelo | Com nota | Corretas | Parciais | Incorretas | Sem nota | Acurácia (%) |
|---|---|---:|---:|---:|---:|---:|---:|
| default_ampliado | gpt-5-4-nano | 999 | 783 | 132 | 84 | 1 | 78.38 |
| default_ampliado | gpt-5-4 | 999 | 915 | 63 | 21 | 1 | 91.59 |
| sem_contexto | gpt-5-4-nano | 999 | 825 | 139 | 35 | 1 | 82.58 |
| sem_contexto | gpt-5-4 | 1000 | 946 | 48 | 6 | 0 | 94.60 |
