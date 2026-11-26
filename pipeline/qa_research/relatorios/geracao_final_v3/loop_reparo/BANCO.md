# Geração final v3, loop reparo: banco de questões

Mecanismo: retroalimentação sem memória (melhor configuração da ablação v3), datasets externos e convertidas do dataset de múltipla escolha em metade das chamadas. 40 documentos, 1450 blocos foco, visitados até saturar (teto de 7 visitas), 4291 chamadas do gerador.

Válida = aprovada pelo auditor v23, gabarito de até 20 palavras e totalmente sustentada pelos blocos. Única = uma por grupo de questões equivalentes (deduplicação calibrada entre as válidas).

| Etapa | Questões | % das geradas |
|---|---|---|
| Geradas | 9843 | 100% |
| Aprovadas pelo auditor | 2105 | 21.4% |
| Válidas | 1720 | 17.5% |
| Válidas únicas (banco) | 867 | 8.8% |

## Por visita

| Visita | Geradas | Válidas | Únicas |
|---|---|---|---|
| 1 | 3827 | 702 (18.3%) | 372 |
| 2 | 3210 | 557 (17.4%) | 274 |
| 3 | 1706 | 306 (17.9%) | 145 |
| 4 | 768 | 109 (14.2%) | 60 |
| 5 | 272 | 40 (14.7%) | 13 |
| 6 | 57 | 5 (8.8%) | 3 |
| 7 | 3 | 1 (33.3%) | 0 |

## Com e sem as convertidas do dataset de múltipla escolha

- Com: 885 válidas de 4941 (17.9%).
- Sem: 835 válidas de 4902 (17.0%).

## Tipos (únicas)

- decisao: 309
- procedimento: 302
- diagnostico: 150
- mecanismo: 55
- conceito: 26
- consequencia: 25

## Motivos de reprovação do auditor

- atalho: 7338
- varias_respostas: 745
- nao_unico: 141
- depende_do_documento: 134
- fora_da_fonte: 24
- bloqueio: 1

## Por documento

| Documento | Blocos | Geradas | Válidas | Únicas |
|---|---|---|---|---|
| 01_01 | 33 | 317 | 24 | 15 |
| 02_01 | 35 | 240 | 57 | 26 |
| 02_02 | 46 | 233 | 68 | 29 |
| 02_03 | 32 | 140 | 33 | 15 |
| 02_04 | 37 | 169 | 64 | 24 |
| 02_05 | 38 | 251 | 52 | 21 |
| 02_06 | 48 | 297 | 46 | 32 |
| 02_07 | 35 | 147 | 42 | 18 |
| 02_08 | 36 | 203 | 59 | 23 |
| 02_09 | 26 | 115 | 33 | 17 |
| 02_10 | 31 | 101 | 33 | 20 |
| 02_11 | 49 | 167 | 50 | 19 |
| 02_12 | 36 | 155 | 52 | 24 |
| 03_01 | 34 | 202 | 38 | 19 |
| 03_02 | 35 | 206 | 41 | 23 |
| 03_03 | 34 | 228 | 55 | 26 |
| 04_01 | 31 | 220 | 63 | 22 |
| 04_02 | 38 | 205 | 47 | 24 |
| 05_01 | 53 | 300 | 76 | 32 |
| 05_02 | 37 | 263 | 76 | 32 |
| 06_01 | 34 | 254 | 30 | 20 |
| 06_02 | 37 | 330 | 21 | 17 |
| 06_03 | 30 | 235 | 27 | 17 |
| 06_04 | 34 | 288 | 34 | 20 |
| 06_05 | 34 | 238 | 58 | 27 |
| 06_06 | 29 | 241 | 22 | 12 |
| 06_07 | 39 | 291 | 35 | 19 |
| 07_01 | 37 | 222 | 55 | 23 |
| 07_02 | 30 | 234 | 27 | 10 |
| 07_03 | 40 | 367 | 47 | 27 |
| 07_04 | 34 | 200 | 48 | 26 |
| 07_05 | 33 | 299 | 36 | 21 |
| 08_01 | 35 | 328 | 30 | 21 |
| 08_02 | 44 | 346 | 44 | 29 |
| 08_03 | 41 | 386 | 45 | 22 |
| 08_04 | 36 | 352 | 13 | 12 |
| 08_05 | 34 | 239 | 37 | 22 |
| 09_01 | 34 | 269 | 19 | 13 |
| 09_02 | 35 | 274 | 48 | 28 |
| 10_01 | 36 | 291 | 35 | 20 |
