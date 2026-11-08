# Ablação da geração de questões

1000 vagas (documento, bloco foco, tipo) sorteadas do banco final v1; cada braço gera uma questão por vaga (o naive, o mesmo número por tópico). Aceita = auditor v23 + resposta de até 20 palavras + sustentação total + não redundante dentro do braço.

## Taxa de aceite

| Braço | Geradas | Auditor | Sustentadas | Aceitas | Taxa (IC 95%) |
|---|---|---|---|---|---|
| Naive (só o tópico) | 1000 | 102 | 23 | 23 | 2,3% (1,5–3,4) |
| Documento + regras | 1000 | 482 | 350 | 296 | 29,6% (26,9–32,5) |
| Sem datasets externos | 1000 | 722 | 502 | 439 | 43,9% (40,9–47,0) |
| Sem retroalimentação | 1000 | 464 | 344 | 287 | 28,7% (26,0–31,6) |
| Pipeline completo | 1000 | 726 | 516 | 445 | 44,5% (41,4–47,6) |

Naive sem exigir a fonte (auditor sem a verificação de sustentação): 162 válidas.

Aceitas por tentativa (ganho da retroalimentação nas mesmas vagas):

- Naive (só o tópico): {1: 23}
- Documento + regras: {1: 296}
- Sem datasets externos: {1: 279, 2: 102, 3: 58}
- Sem retroalimentação: {1: 287}
- Pipeline completo: {1: 269, 2: 116, 3: 60}

| Comparação pareada (McNemar exato) | Só o 1º aceita | Só o 2º aceita | p |
|---|---|---|---|
| Pipeline completo x Sem retroalimentação | 168 | 10 | 3.77e-38 |
| Sem datasets externos x Documento + regras | 157 | 14 | 8.89e-32 |
| Pipeline completo x Sem datasets externos | 179 | 173 | 0.79 |
| Sem retroalimentação x Documento + regras | 145 | 154 | 0.644 |

Motivos de recusa do auditor:

- Naive (só o tópico): {'atalho': 361, 'varias_respostas': 234, 'fora_da_fonte': 175, 'depende_do_documento': 27, 'nao_unico': 101}
- Documento + regras: {'atalho': 408, 'fora_da_fonte': 7, 'varias_respostas': 68, 'depende_do_documento': 35}
- Sem datasets externos: {'atalho': 239, 'varias_respostas': 22, 'depende_do_documento': 14, 'fora_da_fonte': 3}
- Sem retroalimentação: {'atalho': 405, 'varias_respostas': 91, 'fora_da_fonte': 12, 'depende_do_documento': 27, 'nao_unico': 1}
- Pipeline completo: {'atalho': 219, 'varias_respostas': 35, 'fora_da_fonte': 8, 'depende_do_documento': 12}

## Vocabulário e diversidade: aceitas

Distinct, vocabulário, termos especializados e aberturas: rarefeitos ao mesmo número de questões (média de 30 sorteios). Termos especializados: palavras de conteúdo que aparecem em até 1/4 dos 40 documentos.

| Métrica | Naive (só o tópico) | Documento + regras | Sem datasets externos | Sem retroalimentação | Pipeline completo | Banco |
|---|---|---|---|---|---|---|
| Questões no conjunto | 23 | 296 | 439 | 287 | 445 | 1000 |
| Rarefeito a | 23 | 287 | 287 | 287 | 287 | 287 |
| Distinct-1 | 0,534 | 0,217 | 0,222 | 0,218 | 0,225 | 0,276 |
| Distinct-2 | 0,882 | 0,723 | 0,736 | 0,723 | 0,737 | 0,791 |
| Vocabulário (palavras de conteúdo) | 104 | 2481 | 2535 | 2422 | 2497 | 2221 |
| Termos especializados | 44 | 1374 | 1390 | 1365 | 1370 | 1166 |
| Fração de tokens especializados | 0,402 | 0,371 | 0,367 | 0,368 | 0,359 | 0,366 |
| MATTR (50) | 0,755 | 0,851 | 0,855 | 0,848 | 0,853 | 0,860 |
| MTLD | 61,3 | 149,1 | 153,6 | 143,6 | 149,0 | 168,7 |
| Self-BLEU por tópico (menor = mais variado) | 0,020 | 0,044 | 0,055 | 0,041 | 0,048 | 0,060 |
| Cosseno médio por tópico (menor = mais variado) | 0,479 | 0,539 | 0,525 | 0,529 | 0,528 | 0,471 |
| Vendi relativo por tópico | 0,839 | 0,584 | 0,491 | 0,578 | 0,496 | 0,383 |
| Aberturas distintas | 0,522 | 0,677 | 0,698 | 0,676 | 0,700 | 0,773 |
| Abertura "Em um/Num/Após..." | 0,000 | 0,294 | 0,246 | 0,282 | 0,243 | 0,113 |
| Trigramas copiados do documento | 0,000 | 0,039 | 0,035 | 0,042 | 0,038 | 0,031 |
| Palavras na pergunta | 10,9 | 41,8 | 41,7 | 40,6 | 40,7 | 29,5 |
| Palavras na resposta | 9,8 | 7,6 | 7,2 | 7,2 | 7,1 | 5,8 |

## Vocabulário e diversidade: todas as geradas

Distinct, vocabulário, termos especializados e aberturas: rarefeitos ao mesmo número de questões (média de 30 sorteios). Termos especializados: palavras de conteúdo que aparecem em até 1/4 dos 40 documentos.

| Métrica | Naive (só o tópico) | Documento + regras | Sem datasets externos | Sem retroalimentação | Pipeline completo | Banco |
|---|---|---|---|---|---|---|
| Questões no conjunto | 1000 | 1000 | 1000 | 1000 | 1000 | 1000 |
| Rarefeito a | 1000 | 1000 | 1000 | 1000 | 1000 | 1000 |
| Distinct-1 | 0,178 | 0,119 | 0,121 | 0,120 | 0,125 | 0,157 |
| Distinct-2 | 0,554 | 0,585 | 0,598 | 0,590 | 0,603 | 0,661 |
| Vocabulário (palavras de conteúdo) | 1838 | 4920 | 4943 | 4923 | 5057 | 4493 |
| Termos especializados | 971 | 2891 | 2835 | 2863 | 2928 | 2599 |
| Fração de tokens especializados | 0,354 | 0,361 | 0,360 | 0,357 | 0,359 | 0,366 |
| MATTR (50) | 0,795 | 0,853 | 0,852 | 0,852 | 0,854 | 0,860 |
| MTLD | 81,1 | 153,4 | 154,2 | 148,7 | 154,5 | 165,0 |
| Self-BLEU por tópico (menor = mais variado) | 0,129 | 0,115 | 0,100 | 0,108 | 0,096 | 0,060 |
| Cosseno médio por tópico (menor = mais variado) | 0,459 | 0,534 | 0,524 | 0,533 | 0,522 | 0,471 |
| Vendi relativo por tópico | 0,390 | 0,307 | 0,320 | 0,309 | 0,323 | 0,383 |
| Aberturas distintas | 0,226 | 0,515 | 0,546 | 0,527 | 0,550 | 0,667 |
| Abertura "Em um/Num/Após..." | 0,004 | 0,250 | 0,212 | 0,260 | 0,240 | 0,113 |
| Trigramas copiados do documento | 0,009 | 0,043 | 0,031 | 0,042 | 0,033 | 0,031 |
| Palavras na pergunta | 10,7 | 42,7 | 42,2 | 42,2 | 41,6 | 29,5 |
| Palavras na resposta | 9,4 | 7,5 | 7,2 | 7,4 | 7,2 | 5,8 |

## Observacional: banco final v1

2037 questões do banco vieram de revisitas do foco e 50 da 2ª tentativa de compostas: 54,7% das 3813 (a revisita também troca os exemplos de forma, então mede retroalimentação e exemplos juntos).
