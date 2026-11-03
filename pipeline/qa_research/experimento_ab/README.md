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

5. **Saturação por foco** (depois de escolher o braço, desligada por padrão): o braço `<X>_sat` copia a 1ª rodada
   de `<X>` e volta a cada foco enquanto ele trouxer conhecimento novo. Em cada rodada extra, o gerador recebe as
   questões já geradas naquele foco; as novas passam por auditoria, refino e deduplicação incremental contra o banco
   do documento inteiro. Um foco fecha quando uma rodada não traz nenhuma questão aprovada e não redundante
   (`--paciencia`, padrão 1) ou ao atingir `--max-rodadas` visitas (padrão 5, incluindo a 1ª). Substituições na
   deduplicação não contam como conhecimento novo. `saturacao.json` traz a curva de conhecimentos novos por rodada
   e as visitas de cada foco; a comparação `<X>_sat` x `<X>` mostra o que as rodadas extras acrescentam e a
   sustentação das questões das rodadas extras.

## Gerador v22 (`v22.py`)

Refatoração feita a partir da revisão manual das questões do braço B. O fluxo é gerador → régua → auditor →
deduplicação, em rodadas por foco até saturar:

| Mudança | Defeito observado no B |
|---|---|
| O gerador entrega de 0 a 4 questões por foco, sem cota por tipo; zero é resposta válida | 126 de 126 chamadas devolveram exatamente 4 questões, inclusive quando o bloco não sustentava |
| O gerador vê os conhecimentos já aceitos no documento (focos em ondas de `--onda` focos distantes entre si) | 33% das aprovadas eram redundantes |
| Exclusões explícitas: nomes comerciais, nomenclatura de projeto, itens de lista, "por que X não garante Y" | Turbiscan, "dirty inert gas header", princípios tautológicos de gestão |
| Gabarito curto (até 15 palavras) e `explicacao` separada, fora da avaliação | Gabaritos compostos, "causa mais provável" sem suporte, acerto parcial |
| Auditor por questão, com o texto-fonte e 5 verificações binárias (sem documento, alternativa excluída, atalho, sustentação, elemento único) | Várias respostas plausíveis, atalhos aprovados, auditor sem acesso à fonte |
| Sem refinador: a correção é do próprio gerador, que recebe a questão recusada e o motivo, e a nova versão passa de novo por régua, auditor e deduplicação | O refinador descartava 1,2% e reescrevia o resto; 44% do banco final eram reescritas, avaliadas pelo mesmo auditor sem fonte |

Um foco fecha quando o gerador devolve zero questões, quando a visita não traz conhecimento novo aceito
(`--paciencia`) ou ao atingir `--max-rodadas` visitas. Exceção (segunda chance, uma vez por foco): uma visita sem
conhecimento novo, mas com questões recusadas pela régua ou pelo auditor, dá ao foco mais uma visita, em que o
gerador vê as recusas e os motivos. Uma composta recusada por qualidade ganha uma única segunda tentativa, com a
questão anterior e o motivo. Redundância e bloqueio de conteúdo não dão segunda chance. `resultado.json` traz
quanto a segunda chance rendeu (`segunda_chance`). Uma questão inválida nunca afeta as outras: régua e auditor
decidem questão por questão, e um foco com falha pendente só volta a abrir depois da retomada.

```bash
bash pipeline/qa_research/rodar_experimento_ab.sh v22 B    # cria B_v22, avalia e compara com B
```

O juiz da avaliação é o mesmo dos braços A a D, para que a comparação meça a geração. A comparação passa a
mostrar também a acurácia com parcial valendo 0,5.

## Robustez

Toda unidade (bloco, encadeamento, foco, lote de auditoria, questão na deduplicação ou na sustentação, par da
calibração) é salva em arquivo próprio. Uma falha fica registrada em `falhas/` e não afeta as demais; o script tenta
de novo até 3 vezes por etapa, e repetir o comando retoma sem refazer nada.

## Comandos

```bash
bash pipeline/qa_research/rodar_experimento_ab.sh plano          # sem API
bash pipeline/qa_research/rodar_experimento_ab.sh                # etapas 0 a 3
bash pipeline/qa_research/rodar_experimento_ab.sh sustentacao B  # etapa 4 no braço escolhido
bash pipeline/qa_research/rodar_experimento_ab.sh saturacao D    # saturação por foco no braço escolhido
```

Testes offline: `python -m pytest pipeline/qa_research/experimento_ab/tests -q`.
