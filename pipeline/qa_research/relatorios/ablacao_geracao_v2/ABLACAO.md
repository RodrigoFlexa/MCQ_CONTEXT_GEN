# Ablação da geração de questões

1000 vagas (documento, bloco foco, tipo) sorteadas do banco final v1; cada braço gera uma questão por vaga (os braços sem documento, o mesmo número por tópico). Aceita = auditor v23 + resposta de até 20 palavras + sustentação total + não redundante dentro do braço.

## Taxa de aceite

| Braço | Geradas | Auditor | Sustentadas | Aceitas | Taxa (IC 95%) |
|---|---|---|---|---|---|
| Naive (só o tópico) | 1000 | 102 | 23 | 23 | 2,3% (1,5–3,4) |
| Documentos | 1000 | 353 | 280 | 213 | 21,3% (18,9–23,9) |
| Regras (sem documento) | 1000 | 123 | 31 | 31 | 3,1% (2,2–4,4) |
| Documentos + regras | 1000 | 440 | 323 | 271 | 27,1% (24,4–29,9) |
| Sem retroalimentação | 999 | 450 | 345 | 294 | 29,4% (26,7–32,3) |
| Sem datasets externos | 1000 | 707 | 494 | 454 | 45,4% (42,3–48,5) |
| Pipeline completo | 1000 | 715 | 489 | 454 | 45,4% (42,3–48,5) |

Naive (só o tópico) sem exigir a fonte (auditor sem a verificação de sustentação): 162 válidas.

Regras (sem documento) sem exigir a fonte (auditor sem a verificação de sustentação): 406 válidas.

Aceitas por tentativa (retroalimentação: novas tentativas nas mesmas vagas):

- Naive (só o tópico): {1: 23}
- Documentos: {1: 213}
- Regras (sem documento): {1: 31}
- Documentos + regras: {1: 271}
- Sem retroalimentação: {1: 294}
- Sem datasets externos: {1: 268, 2: 122, 3: 64}
- Pipeline completo: {1: 281, 2: 107, 3: 66}

| Comparação pareada (McNemar exato) | Só o 1º aceita | Só o 2º aceita | p |
|---|---|---|---|
| Documentos + regras x Documentos | 210 | 152 | 0.00269 |
| Sem retroalimentação x Documentos + regras | 160 | 137 | 0.202 |
| Sem datasets externos x Documentos + regras | 291 | 108 | 1.69e-20 |
| Pipeline completo x Sem retroalimentação | 275 | 115 | 3.13e-16 |
| Pipeline completo x Sem datasets externos | 195 | 195 | 1 |

Motivos de recusa do auditor:

- Naive (só o tópico): {'atalho': 361, 'varias_respostas': 234, 'fora_da_fonte': 175, 'depende_do_documento': 27, 'nao_unico': 101}
- Documentos: {'atalho': 351, 'nao_unico': 134, 'varias_respostas': 119, 'depende_do_documento': 43}
- Regras (sem documento): {'fora_da_fonte': 286, 'varias_respostas': 150, 'atalho': 428, 'depende_do_documento': 9, 'bloqueio': 2, 'nao_unico': 2}
- Documentos + regras: {'atalho': 427, 'varias_respostas': 90, 'depende_do_documento': 34, 'bloqueio': 2, 'fora_da_fonte': 5, 'nao_unico': 2}
- Sem retroalimentação: {'atalho': 426, 'varias_respostas': 91, 'nao_unico': 4, 'depende_do_documento': 21, 'fora_da_fonte': 7}
- Sem datasets externos: {'atalho': 230, 'varias_respostas': 39, 'depende_do_documento': 18, 'fora_da_fonte': 5, 'bloqueio': 1}
- Pipeline completo: {'atalho': 241, 'varias_respostas': 19, 'bloqueio': 2, 'fora_da_fonte': 12, 'depende_do_documento': 9, 'nao_unico': 2}

## Vocabulário e diversidade: aceitas

Distinct, vocabulário, termos especializados e aberturas: rarefeitos ao mesmo número de questões (média de 30 sorteios). Termos especializados: palavras de conteúdo que aparecem em até 1/4 dos 40 documentos.

| Métrica | Naive (só o tópico) | Documentos | Regras (sem documento) | Documentos + regras | Sem retroalimentação | Sem datasets externos | Pipeline completo | Banco |
|---|---|---|---|---|---|---|---|---|
| Questões no conjunto | 23 | 213 | 31 | 271 | 294 | 454 | 454 | 1000 |
| Rarefeito a | 23 | 213 | 31 | 213 | 213 | 213 | 213 | 213 |
| Distinct-1 | 0,534 | 0,319 | 0,529 | 0,251 | 0,251 | 0,248 | 0,258 | 0,309 |
| Distinct-2 | 0,882 | 0,749 | 0,922 | 0,755 | 0,749 | 0,760 | 0,767 | 0,816 |
| Vocabulário (palavras de conteúdo) | 104 | 956 | 327 | 2046 | 2063 | 2049 | 2102 | 1836 |
| Termos especializados | 44 | 486 | 130 | 1136 | 1103 | 1087 | 1130 | 938 |
| Fração de tokens especializados | 0,402 | 0,384 | 0,368 | 0,380 | 0,360 | 0,365 | 0,364 | 0,366 |
| MATTR (50) | 0,755 | 0,809 | 0,847 | 0,849 | 0,848 | 0,853 | 0,853 | 0,860 |
| MTLD | 61,3 | 86,0 | 131,0 | 135,8 | 140,7 | 154,2 | 155,2 | 167,8 |
| Self-BLEU por tópico (menor = mais variado) | 0,020 | 0,052 | 0,013 | 0,049 | 0,047 | 0,058 | 0,059 | 0,060 |
| Cosseno médio por tópico (menor = mais variado) | 0,479 | 0,474 | 0,535 | 0,527 | 0,518 | 0,520 | 0,515 | 0,471 |
| Vendi relativo por tópico | 0,839 | 0,687 | 0,819 | 0,584 | 0,573 | 0,500 | 0,490 | 0,383 |
| Aberturas distintas | 0,522 | 0,300 | 0,742 | 0,663 | 0,643 | 0,730 | 0,731 | 0,804 |
| Abertura "Em um/Num/Após..." | 0,000 | 0,052 | 0,032 | 0,292 | 0,303 | 0,264 | 0,244 | 0,113 |
| Trigramas copiados do documento | 0,000 | 0,142 | 0,016 | 0,053 | 0,050 | 0,035 | 0,038 | 0,031 |
| Palavras na pergunta | 10,9 | 14,9 | 23,0 | 40,3 | 40,5 | 41,1 | 40,2 | 29,5 |
| Palavras na resposta | 9,8 | 11,9 | 4,1 | 7,4 | 7,4 | 7,3 | 7,1 | 5,8 |

## Vocabulário e diversidade: todas as geradas

Distinct, vocabulário, termos especializados e aberturas: rarefeitos ao mesmo número de questões (média de 30 sorteios). Termos especializados: palavras de conteúdo que aparecem em até 1/4 dos 40 documentos.

| Métrica | Naive (só o tópico) | Documentos | Regras (sem documento) | Documentos + regras | Sem retroalimentação | Sem datasets externos | Pipeline completo | Banco |
|---|---|---|---|---|---|---|---|---|
| Questões no conjunto | 1000 | 1000 | 1000 | 1000 | 999 | 1000 | 1000 | 1000 |
| Rarefeito a | 999 | 999 | 999 | 999 | 999 | 999 | 999 | 999 |
| Distinct-1 | 0,179 | 0,160 | 0,144 | 0,119 | 0,119 | 0,122 | 0,122 | 0,157 |
| Distinct-2 | 0,554 | 0,534 | 0,603 | 0,576 | 0,581 | 0,601 | 0,598 | 0,662 |
| Vocabulário (palavras de conteúdo) | 1837 | 2325 | 3810 | 4836 | 4797 | 5001 | 5014 | 4491 |
| Termos especializados | 970 | 1359 | 1943 | 2926 | 2860 | 2890 | 2885 | 2598 |
| Fração de tokens especializados | 0,354 | 0,341 | 0,362 | 0,358 | 0,360 | 0,360 | 0,362 | 0,366 |
| MATTR (50) | 0,797 | 0,811 | 0,855 | 0,851 | 0,850 | 0,857 | 0,854 | 0,859 |
| MTLD | 84,5 | 91,0 | 149,0 | 146,7 | 147,4 | 155,3 | 154,4 | 163,0 |
| Self-BLEU por tópico (menor = mais variado) | 0,129 | 0,294 | 0,134 | 0,128 | 0,129 | 0,103 | 0,105 | 0,060 |
| Cosseno médio por tópico (menor = mais variado) | 0,459 | 0,490 | 0,477 | 0,535 | 0,534 | 0,520 | 0,523 | 0,471 |
| Vendi relativo por tópico | 0,390 | 0,326 | 0,367 | 0,306 | 0,307 | 0,326 | 0,322 | 0,383 |
| Aberturas distintas | 0,226 | 0,222 | 0,501 | 0,507 | 0,489 | 0,581 | 0,541 | 0,667 |
| Abertura "Em um/Num/Após..." | 0,004 | 0,055 | 0,103 | 0,264 | 0,283 | 0,242 | 0,255 | 0,113 |
| Trigramas copiados do documento | 0,009 | 0,137 | 0,002 | 0,047 | 0,049 | 0,029 | 0,028 | 0,031 |
| Palavras na pergunta | 10,7 | 15,1 | 27,4 | 42,0 | 41,8 | 42,4 | 42,3 | 29,5 |
| Palavras na resposta | 9,4 | 11,7 | 4,9 | 7,7 | 7,6 | 7,3 | 7,5 | 5,8 |

## Observacional: banco final v1

2037 questões do banco vieram de revisitas do foco e 50 da 2ª tentativa de compostas: 54,7% das 3813 (a revisita também troca os exemplos de forma, então mede retroalimentação e exemplos juntos).
