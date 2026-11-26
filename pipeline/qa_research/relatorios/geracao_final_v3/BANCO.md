# Geração final v3: banco de questões

Mecanismo: retroalimentação sem memória (melhor configuração da ablação v3), datasets externos e convertidas do dataset de múltipla escolha em metade das chamadas. 40 documentos, 1450 blocos foco, visitados até saturar (teto de 10 visitas), 9981 chamadas do gerador.

Válida = aprovada pelo auditor v23, gabarito de até 20 palavras e totalmente sustentada pelos blocos. Única = uma por grupo de questões equivalentes (deduplicação calibrada entre as válidas).

| Etapa | Questões | % das geradas |
|---|---|---|
| Geradas | 35634 | 100% |
| Aprovadas pelo auditor | 17075 | 47.9% |
| Válidas | 15185 | 42.6% |
| Válidas únicas (banco) | 4129 | 11.6% |

## Por visita

| Visita | Geradas | Válidas | Únicas |
|---|---|---|---|
| 1 | 5221 | 1980 (37.9%) | 972 |
| 2 | 5154 | 2071 (40.2%) | 689 |
| 3 | 5132 | 2041 (39.8%) | 573 |
| 4 | 4552 | 1904 (41.8%) | 438 |
| 5 | 3890 | 1746 (44.9%) | 409 |
| 6 | 3297 | 1488 (45.1%) | 320 |
| 7 | 2731 | 1278 (46.8%) | 270 |
| 8 | 2295 | 1070 (46.6%) | 202 |
| 9 | 1876 | 872 (46.5%) | 138 |
| 10 | 1486 | 735 (49.5%) | 118 |

## Com e sem as convertidas do dataset de múltipla escolha

- Com: 7541 válidas de 17859 (42.2%).
- Sem: 7644 válidas de 17775 (43.0%).

## Tipos (únicas)

- procedimento: 1488
- decisao: 1351
- diagnostico: 552
- mecanismo: 389
- consequencia: 189
- conceito: 160

## Motivos de reprovação do auditor

- atalho: 16516
- varias_respostas: 2756
- depende_do_documento: 595
- nao_unico: 227
- fora_da_fonte: 79
- bloqueio: 4

## Por documento

| Documento | Blocos | Geradas | Válidas | Únicas |
|---|---|---|---|---|
| 01_01 | 33 | 547 | 80 | 36 |
| 02_01 | 35 | 1037 | 441 | 132 |
| 02_02 | 46 | 1234 | 666 | 148 |
| 02_03 | 32 | 867 | 471 | 108 |
| 02_04 | 37 | 970 | 571 | 130 |
| 02_05 | 38 | 950 | 457 | 105 |
| 02_06 | 48 | 1069 | 460 | 138 |
| 02_07 | 35 | 955 | 535 | 127 |
| 02_08 | 36 | 956 | 460 | 125 |
| 02_09 | 26 | 784 | 391 | 102 |
| 02_10 | 31 | 891 | 532 | 131 |
| 02_11 | 49 | 1366 | 855 | 184 |
| 02_12 | 36 | 1038 | 601 | 149 |
| 03_01 | 34 | 936 | 454 | 109 |
| 03_02 | 35 | 900 | 452 | 112 |
| 03_03 | 34 | 891 | 396 | 125 |
| 04_01 | 31 | 908 | 413 | 101 |
| 04_02 | 38 | 1092 | 516 | 138 |
| 05_01 | 53 | 1394 | 676 | 175 |
| 05_02 | 37 | 1046 | 502 | 132 |
| 06_01 | 34 | 873 | 361 | 89 |
| 06_02 | 37 | 788 | 202 | 73 |
| 06_03 | 30 | 740 | 183 | 75 |
| 06_04 | 34 | 852 | 267 | 89 |
| 06_05 | 34 | 765 | 322 | 66 |
| 06_06 | 29 | 593 | 167 | 64 |
| 06_07 | 39 | 827 | 258 | 78 |
| 07_01 | 37 | 939 | 443 | 111 |
| 07_02 | 30 | 668 | 214 | 66 |
| 07_03 | 40 | 878 | 276 | 88 |
| 07_04 | 34 | 792 | 405 | 107 |
| 07_05 | 33 | 626 | 173 | 52 |
| 08_01 | 35 | 717 | 194 | 61 |
| 08_02 | 44 | 1082 | 417 | 117 |
| 08_03 | 41 | 926 | 241 | 100 |
| 08_04 | 36 | 655 | 79 | 39 |
| 08_05 | 34 | 746 | 260 | 84 |
| 09_01 | 34 | 677 | 220 | 70 |
| 09_02 | 35 | 809 | 294 | 87 |
| 10_01 | 36 | 850 | 280 | 106 |
