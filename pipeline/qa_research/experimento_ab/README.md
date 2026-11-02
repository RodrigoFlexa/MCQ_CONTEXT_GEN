# Experimento A/B da geração de questões

Pergunta: os documentos refinados melhoram as questões? E o contexto de geração deve ser a janela de 3 blocos ou o
capítulo? Cada braço muda um fator só; o gerador é o v21 (`geracao_tipos/rodadas.py`), que produziu as 2.818 questões.

| Braço | Documento | Contexto do bloco foco | Inventário |
|---|---|---|---|
| A | antigo | janela de 3 blocos | novo |
| B | refinado | janela de 3 blocos | novo |
| C | antigo | capítulo inteiro | o de A (mesmo documento) |
| D | refinado | capítulo inteiro | o de B (mesmo documento) |

Documentos: 02_02, 03_03 e 07_01 (snapshot `relatorios/qa_continuo_v2/contextos`). Em todos os braços:
inventário e banco de exemplos começam vazios (nada herdado de rodadas anteriores), as compostas seguem o mesmo método
e a deduplicação é a incremental calibrada. O prompt de capítulo é o v18 com 5 trocas de texto, só na descrição do
contexto (`geracao.TROCAS_CAPITULO`).

## Etapas

0. **Calibração da deduplicação** (`calibracao.py`), com as 2.818 questões existentes: embeddings de pergunta +
   resposta (3-small e 3-large; E5 antigo como base), cosseno centrado, ~170 pares sorteados por faixa + pares que a
   deduplicação antiga já removeu, rótulo de referência (gpt-5.4 high) e juízes candidatos. Saem o embedding (maior
   AUC), o limiar de descarte automático (precisão 100% na amostra), o limiar do juiz (recall >= 95%) e o juiz mais
   barato com concordância >= 90%. Revisão humana opcional: preencha `rotulo_humano` em `pares_rotulados.csv`, salve
   como `rotulos_humanos.csv` e rode `calibrar --recalcular` (sem chamadas).
1. **Preparação** dos documentos na pasta do experimento, com hashes.
2. **Geração** dos quatro braços. Deduplicação incremental (`dedup.py`): cada questão aprovada é comparada com o banco
   do mesmo documento; acima do limiar automático é descartada, na faixa do juiz um modelo decide (e escolhe qual fica),
   abaixo entra. Uma decisão por arquivo.
3. **Avaliação** de cada braço com o protocolo do `benchmark_gap` (GPT-4.1 Nano/Mini/4.1, com e sem contexto, juiz
   gpt-5.4, sustentação por afirmação). O contexto é o mesmo critério em todos os braços: os capítulos inteiros tocados
   pelo contexto de geração. **Comparação** (`COMPARACAO.md`): por braço e efeitos com IC 95% por bootstrap.
4. **Sustentação** (depois de escolher o braço): sobre as mesmas questões do braço, cada gabarito aprovado passa pela
   auditoria de sustentação; se faltar suporte, o reparo recebe as afirmações sem suporte e devolve a resposta mínima
   sustentada (ou descarta só aquela questão). Gera o braço `<X>_sust`, avaliado e comparado com `<X>`.

## Robustez

Toda unidade (bloco, encadeamento, foco, lote de auditoria, questão na deduplicação ou na sustentação, par da
calibração) é salva em arquivo próprio. Uma falha fica registrada em `falhas/` e não afeta as demais; o script tenta
de novo até 3 vezes por etapa, e repetir o comando retoma sem refazer nada.

## Comandos

```bash
bash pipeline/qa_research/rodar_experimento_ab.sh plano          # sem API
bash pipeline/qa_research/rodar_experimento_ab.sh                # etapas 0 a 3
bash pipeline/qa_research/rodar_experimento_ab.sh sustentacao B  # etapa 4 no braço escolhido
```

Testes offline: `python -m pytest pipeline/qa_research/experimento_ab/tests -q`.
