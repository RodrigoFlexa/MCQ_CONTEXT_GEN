# Geração final v3: loops

Cada loop roda sobre os mesmos contextos e entra na mesma deduplicação da geração principal; "únicas" são as válidas que não são equivalentes a nenhuma válida anterior do documento, de qualquer origem.

| Loop | Chamadas | Geradas | Válidas | % válidas | Únicas |
|---|---|---|---|---|---|
| retro_sem_memoria | 9981 | 35634 | 15185 | 42.6% | 4129 |
| loop_reparo | 4291 | 9843 | 1720 | 17.5% | 867 |

Únicas no total: 4996.

Tipos (únicas, todas as origens): procedimento 1790, decisao 1660, diagnostico 702, mecanismo 444, consequencia 214, conceito 186.
