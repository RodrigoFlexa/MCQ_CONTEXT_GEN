# Geração final v3: banco de questões

Mecanismo: retroalimentação sem memória (melhor configuração da ablação v3), datasets externos e convertidas do dataset de múltipla escolha em metade das chamadas. 40 documentos, 1450 blocos foco, visitados até saturar (teto de 8 visitas), 3455 chamadas do gerador.

Válida = aprovada pelo auditor v23, gabarito de até 20 palavras e totalmente sustentada pelos blocos. Única = uma por grupo de questões equivalentes (deduplicação calibrada entre as válidas).

| Etapa | Questões | % das geradas |
|---|---|---|
| Geradas | 12454 | 100% |
| Aprovadas pelo auditor | 6092 | 48.9% |
| Válidas | 5452 | 43.8% |
| Válidas únicas (banco) | 2449 | 19.7% |

## Por visita

| Visita | Geradas | Válidas | Únicas |
|---|---|---|---|
| 1 | 5221 | 1980 (37.9%) | 1267 |
| 2 | 3584 | 1654 (46.1%) | 630 |
| 3 | 1968 | 981 (49.8%) | 312 |
| 4 | 953 | 480 (50.4%) | 131 |
| 5 | 409 | 199 (48.7%) | 56 |
| 6 | 181 | 92 (50.8%) | 30 |
| 7 | 85 | 44 (51.8%) | 16 |
| 8 | 53 | 22 (41.5%) | 7 |

## Com e sem as convertidas do dataset de múltipla escolha

- Com: 2705 válidas de 6283 (43.1%).
- Sem: 2747 válidas de 6171 (44.5%).

## Tipos (únicas)

- decisao: 860
- procedimento: 845
- diagnostico: 314
- mecanismo: 223
- consequencia: 108
- conceito: 99

## Motivos de reprovação do auditor

- atalho: 5643
- varias_respostas: 990
- depende_do_documento: 176
- nao_unico: 75
- fora_da_fonte: 30
- bloqueio: 1

## Por documento

| Documento | Blocos | Geradas | Válidas | Únicas |
|---|---|---|---|---|
| 01_01 | 33 | 150 | 18 | 11 |
| 02_01 | 35 | 396 | 173 | 77 |
| 02_02 | 46 | 417 | 221 | 85 |
| 02_03 | 32 | 303 | 163 | 68 |
| 02_04 | 37 | 414 | 244 | 93 |
| 02_05 | 38 | 362 | 180 | 72 |
| 02_06 | 48 | 379 | 164 | 82 |
| 02_07 | 35 | 377 | 223 | 88 |
| 02_08 | 36 | 354 | 179 | 80 |
| 02_09 | 26 | 250 | 118 | 56 |
| 02_10 | 31 | 306 | 173 | 79 |
| 02_11 | 49 | 504 | 315 | 120 |
| 02_12 | 36 | 416 | 246 | 95 |
| 03_01 | 34 | 260 | 124 | 55 |
| 03_02 | 35 | 317 | 168 | 65 |
| 03_03 | 34 | 306 | 134 | 67 |
| 04_01 | 31 | 256 | 116 | 50 |
| 04_02 | 38 | 391 | 186 | 83 |
| 05_01 | 53 | 472 | 233 | 101 |
| 05_02 | 37 | 404 | 204 | 79 |
| 06_01 | 34 | 321 | 130 | 58 |
| 06_02 | 37 | 269 | 68 | 39 |
| 06_03 | 30 | 236 | 60 | 36 |
| 06_04 | 34 | 293 | 105 | 56 |
| 06_05 | 34 | 302 | 123 | 47 |
| 06_06 | 29 | 181 | 55 | 31 |
| 06_07 | 39 | 247 | 81 | 40 |
| 07_01 | 37 | 307 | 124 | 66 |
| 07_02 | 30 | 234 | 73 | 35 |
| 07_03 | 40 | 347 | 128 | 59 |
| 07_04 | 34 | 298 | 148 | 70 |
| 07_05 | 33 | 216 | 56 | 30 |
| 08_01 | 35 | 270 | 85 | 42 |
| 08_02 | 44 | 391 | 155 | 69 |
| 08_03 | 41 | 254 | 67 | 42 |
| 08_04 | 36 | 169 | 14 | 10 |
| 08_05 | 34 | 287 | 113 | 57 |
| 09_01 | 34 | 265 | 95 | 49 |
| 09_02 | 35 | 260 | 94 | 49 |
| 10_01 | 36 | 273 | 96 | 58 |
