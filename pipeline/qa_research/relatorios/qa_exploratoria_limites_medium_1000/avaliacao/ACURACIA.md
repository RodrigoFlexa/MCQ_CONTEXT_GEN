# Acurácia dos modelos sem contexto

Atualizado em 2026-10-29T08:18:41.666215+00:00. Questões prontas: 6000 em 40 tópicos. Juiz: `gpt-5-4-petrobras:medium`. Respondentes medium; braços 50, 100 e concisa livre; mesmo juiz em todos.
Acurácia = % de respostas corretas; "com parcial" conta a parcial como meio acerto.

## Geral

| Modelo | julgadas | acurácia (%) | com parcial (%) | corretas | parciais |
|---|---|---|---|---|---|
| gpt-5-4 | 5988 | **92.9** | 95.8 | 5561 | 349 |
| gpt-5-4-nano | 5995 | **80.9** | 87.5 | 4850 | 792 |

## Por tipo de questão (acurácia %, julgadas entre parênteses)

| Tipo | questões | gpt-5-4-nano | gpt-5-4 |
|---|---|---|---|
| conceito | 1038 | 79.5 (1038) | 94.2 (1037) |
| mecanismo | 1554 | 93.2 (1550) | 98.4 (1548) |
| consequencia | 558 | 91.4 (558) | 96.1 (558) |
| diagnostico | 1170 | 80.2 (1169) | 93.8 (1168) |
| decisao | 837 | 73.0 (837) | 90.4 (834) |
| procedimento | 843 | 61.8 (843) | 80.2 (843) |

## Por composição (acurácia %)

| Composição | gpt-5-4-nano | gpt-5-4 |
|---|---|---|
| simples | 82.0 (3205) | 93.6 (3203) |
| composta | 79.6 (2790) | 92.1 (2785) |

## Cobertura

| Modelo | Total | Com nota | Sem nota | Cobertura (%) |
|---|---:|---:|---:|---:|
| gpt-5-4-nano | 6000 | 5995 | 5 | 99.9 |
| gpt-5-4 | 6000 | 5988 | 12 | 99.8 |

Bloqueios terminais sem nota; excluídos da acurácia, reportados na cobertura.

## Por condição

| Condição | Modelo | Com nota | Corretas | Parciais | Incorretas | Sem nota | Acurácia (%) |
|---|---|---:|---:|---:|---:|---:|---:|
| default_ampliado / concisa_livre | gpt-5-4-nano | 999 | 793 | 126 | 80 | 1 | 79.38 |
| default_ampliado / concisa_livre | gpt-5-4 | 999 | 913 | 64 | 22 | 1 | 91.39 |
| default_ampliado / p100 | gpt-5-4-nano | 999 | 783 | 132 | 84 | 1 | 78.38 |
| default_ampliado / p100 | gpt-5-4 | 999 | 915 | 63 | 21 | 1 | 91.59 |
| default_ampliado / p50 | gpt-5-4-nano | 999 | 780 | 137 | 82 | 1 | 78.08 |
| default_ampliado / p50 | gpt-5-4 | 995 | 911 | 69 | 15 | 5 | 91.56 |
| sem_contexto / concisa_livre | gpt-5-4-nano | 999 | 852 | 109 | 38 | 1 | 85.29 |
| sem_contexto / concisa_livre | gpt-5-4 | 1000 | 945 | 49 | 6 | 0 | 94.50 |
| sem_contexto / p100 | gpt-5-4-nano | 999 | 825 | 139 | 35 | 1 | 82.58 |
| sem_contexto / p100 | gpt-5-4 | 1000 | 946 | 48 | 6 | 0 | 94.60 |
| sem_contexto / p50 | gpt-5-4-nano | 1000 | 817 | 149 | 34 | 0 | 81.70 |
| sem_contexto / p50 | gpt-5-4 | 995 | 931 | 56 | 8 | 5 | 93.57 |
