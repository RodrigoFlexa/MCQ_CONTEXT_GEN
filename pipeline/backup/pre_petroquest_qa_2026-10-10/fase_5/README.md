# Fase 5 — filtragem do dataset pela aderência ao texto do especialista

As questões da fase 3 nasceram das instruções longas de `pipeline/fase_3/topicos.py`.
Depois da revisão, o especialista reescreveu essas instruções em versões curtas
(*Versão resumida* e *Versão compacta*) no docx **SUGESTÃO DE FRASES PARA COMPOR
PROMPT MÚLTIPLA ESCOLHA V14 (09/09/26)**. Esta fase mede o quanto cada questão se
parece com a referência do próprio subtópico e corta o dataset por limiar de
similaridade.

## Como está montado

| arquivo | papel |
|---|---|
| `extrair_referencias.py` | lê o docx e grava `referencias_especialista.json` |
| `filtragem_fase5.py` | motor: embeddings, similaridade, varredura de limiares, exportação |
| `filtragem_fase5.ipynb` | notebook com a análise passo a passo e os gráficos |
| `_montar_notebook.py` | só regenera o `.ipynb` quando o roteiro dele muda |
| `saida_fase5/` | resultados (ver abaixo) |

Decisões (combinadas em set/2026):

* **referência** = `Versão compacta` > `Versão resumida` > descrição longa;
* **texto da questão** = enunciado + todas as alternativas, para capturar também o
  vocabulário dos distratores;
* **comparação** = cada questão só contra a referência do subtópico em que foi
  gerada (mede aderência, não reclassifica);
* **dificuldade** = campo `difficulty` da geração (juiz da fase 3), não a
  reavaliação da fase 4;
* **embeddings** = `paraphrase-multilingual-MiniLM-L12-v2`, o mesmo do resto do
  projeto, via `utils_fase3.Embedder` com cache próprio em `saida_fase5/embeddings/`.

## Como rodar

```bash
# 1) referências, a partir do docx (refazer quando vier docx novo)
python pipeline/fase_5/extrair_referencias.py

# 2) similaridade + varredura (a 1ª vez leva ~10 min de embeddings em CPU)
python pipeline/fase_5/filtragem_fase5.py

# 3) exportar o dataset cortado, reaproveitando as similaridades já calculadas
python pipeline/fase_5/filtragem_fase5.py \
    --similaridades pipeline/fase_5/saida_fase5/similaridades.csv \
    --exportar 0.55 --respeitar-piso
```

O notebook `filtragem_fase5.ipynb` faz o mesmo com gráficos e tabelas
intermediárias.

## Resultado da primeira rodada (19/09/2026, 15.602 questões)

Similaridade: mínimo 0,190 · p25 0,452 · **mediana 0,513** · p75 0,577 · máximo 0,824.

| limiar | questões | % do total | fácil | média | difícil |
|---|---|---|---|---|---|
| 0,30 | 15.503 | 99,4% | 2.366 | 12.189 | 948 |
| 0,40 | 14.078 | 90,2% | 2.141 | 11.086 | 851 |
| **0,45** | **11.822** | **75,8%** | 1.754 | 9.362 | 706 |
| 0,50 | 8.633 | 55,3% | 1.285 | 6.858 | 490 |
| 0,55 | 5.375 | 34,5% | 799 | 4.291 | 285 |
| 0,60 | 2.832 | 18,2% | 431 | 2.253 | 148 |

Três leituras:

1. **O corte é praticamente neutro em dificuldade.** A composição fica em
   ~15% fácil / ~79% média / ~6% difícil de 0,0 até 0,65 — filtrar por
   semelhança com o texto do especialista não desequilibra o dataset. O que o
   número expõe é outra coisa: o dataset já é dominado por questões médias.
2. **0,45 é o limiar máximo utilizável** se os números do docx forem tratados
   como piso por tópico. Em 0,46 o tópico *Gestão do Desempenho Empresarial
   (KPI)* cai para 195 questões, abaixo do piso de 200.
3. **O gargalo é o tópico 1.** Ele tem 281 questões no total (foi regenerado por
   último) contra um piso de 200, então é ele que trava o limiar. Gerar mais
   questões de KPI libera limiares mais altos para o dataset inteiro.

Achado colateral, registrado em `referencias_especialista.json`: no docx V14, as
versões resumida e compacta de *Operação de Separadores Trifásicos* trazem o
texto de tratadores eletrostáticos, e as de *Compressão de Gás* trazem o de
tratamento do gás produzido (copiar/colar do vizinho). O extrator detecta isso
comparando cada variante com a descrição longa do próprio subtópico e cai para a
longa, que está correta. Vale confirmar com o especialista.

## Saídas em `saida_fase5/`

| arquivo | conteúdo |
|---|---|
| `similaridades.csv` | uma linha por questão: id, tópico, subtópico, dificuldade, similaridade |
| `varredura_limiares.csv` | quanto sobra em cada limiar, por dificuldade |
| `varredura_por_subtopico.csv` | o mesmo corte, subtópico a subtópico |
| `varredura_limiares.png` | gráfico da varredura |
| `questoes_filtradas_0.45.jsonl` | dataset cortado, com `similaridade_especialista` em cada questão |

## Corte adotado: 0,55 como teto de poda, piso do docx como trava

Regra combinada em set/2026: **0,55 é o corte mais rigoroso que se admite** —
nenhum tópico é podado além dele. O piso do docx tem prioridade: quando um
tópico não tem questões parecidas o bastante para chegar ao seu mínimo, ele para
de ser podado antes e fica com as N mais parecidas, o que equivale a um limiar
efetivo mais baixo só ali. É o que `filtrar_com_piso` faz (`--respeitar-piso` na
linha de comando).

Resultado: **5.645 questões** (36,2% das 15.602).

| tópico | total | mantidas | piso docx | limiar efetivo | critério | fácil | média | difícil |
|---|---|---|---|---|---|---|---|---|
| Produção e Processo (Medição Fiscal e Alívio) | 7.055 | 2.735 | 600 | 0,550 | limiar | 381 | 2.165 | 189 |
| Segurança Operacional, SGSO e Riscos | 1.954 | 787 | 350 | 0,550 | limiar | 133 | 631 | 23 |
| Manutenção, Inspeção e Integridade | 1.418 | 451 | 400 | 0,550 | limiar | 58 | 371 | 22 |
| Lastro, Ancoragem, Offloading e Tanques | 1.136 | 389 | 200 | 0,550 | limiar | 42 | 331 | 16 |
| Segurança Ocupacional, Saúde e Meio Ambiente | 1.354 | 300 | 300 | **0,531** | piso | 67 | 225 | 8 |
| Utilidades e geração de energia | 853 | 250 | 250 | 0,551 | limiar | 59 | 182 | 9 |
| Operações submarinas, poços e risers | 740 | 233 | 150 | 0,551 | limiar | 30 | 196 | 7 |
| Gestão do Desempenho Empresarial (KPI) | 281 | 200 | 200 | **0,454** | piso | 33 | 160 | 7 |
| Descomissionamento e Ciclo de Vida | 350 | 150 | 150 | **0,512** | piso | 27 | 119 | 4 |
| Logística, Suprimentos e Movimentação | 461 | 150 | 150 | **0,526** | piso | 17 | 125 | 8 |

Quatro tópicos travaram no piso. O relatório fica em `saida_fase5/piso_0.55.csv`
e a coluna `criterio` diz qual regra mandou em cada um.

Dois desses casos são volume: KPI (281 questões no total) e Descomissionamento
(350) não têm de onde tirar 200 e 150 depois de um corte de dois terços. Gerar
mais questões nesses tópicos na fase 3 sobe o limiar efetivo deles.

*Segurança Ocupacional, Saúde e Meio Ambiente* é diferente: tem 1.354 questões e
mesmo assim só 226 passam de 0,55 (16,7%, contra ~31% dos demais). O déficit se
concentra em dois subtópicos — *Saúde Ocupacional* cai de 260 para 17 e
*Segurança Ocupacional* de 264 para 32. Ou as questões derivaram do assunto, ou
a versão compacta desses dois subtópicos ficou estreita demais frente ao que foi
gerado. Vale ler uma amostra das descartadas antes de fechar.

## Método adotado: piso de relevância + cota por cluster (set/2026)

O corte por limiar puro ordena por similaridade e corta, o que concentra a
seleção em volta do centroide da referência. Medindo com o codebook da fase 3
(k=24 por subtópico) e a entropia normalizada, o custo aparece:

| seleção (mesmo tamanho) | entropia | similaridade média | clusters cobertos (de 24) |
|---|---|---|---|
| dataset completo | 0,953 | — | 24,0 |
| limiar 0,55 + piso do docx | 0,793 | 0,604 | 17,6 |
| amostra aleatória | 0,920 | — | — |
| MMR λ=0,7 | 0,815 | 0,603 | 18,9 |
| MMR λ=0,5 | 0,858 | 0,590 | 21,0 |
| **piso 0,45 + cota por cluster** | **0,925** | 0,588 | **22,4** |

A amostra aleatória é a linha que diagnostica: reduzir o dataset para esse
tamanho quase não custa entropia (0,920). Quem derruba para 0,793 é a ordenação
por similaridade, não o tamanho.

**Cota por cluster sozinha não serve**, e é importante registrar por quê: ela
pegaria as mais parecidas de cada cluster inclusive de clusters inteiramente
fora do assunto, que é exatamente o que o texto revisado do especialista veio
excluir. Por isso o método é em dois estágios, nesta ordem:

1. **Piso de relevância (0,45), filtro duro.** Nada abaixo dele entra, nem para
   preencher cota. Um cluster cujas questões estão todas abaixo do piso
   desaparece inteiro, e esse é o efeito pretendido.
2. **Cota por cluster entre os sobreviventes.** k-means sobre os embeddings das
   próprias questões do subtópico, cota igual por cluster, ordenando por
   similaridade dentro de cada um, até o alvo. O alvo por subtópico é o que o
   corte em 0,55 com piso do docx daria, para o tamanho ficar comparável.

```bash
python pipeline/fase_5/filtragem_fase5.py \
    --similaridades pipeline/fase_5/saida_fase5/similaridades.csv \
    --exportar 0.55 --cota-cluster --piso 0.45
```

### Resultado

**5.645 questões** (36,2% de 15.602): 873 fáceis (15,5%), 4.453 médias (78,9%),
319 difíceis (5,7%).

| tópico | mantidas | mínimo docx | sim. média | fácil | média | difícil |
|---|---|---|---|---|---|---|
| Produção e Processo (Medição Fiscal e Alívio) | 2.735 | 600 | 0,599 | 384 | 2.148 | 203 |
| Seg. Operacional, SGSO e Riscos | 787 | 350 | 0,595 | 135 | 634 | 18 |
| Manutenção, Inspeção e Integridade | 451 | 400 | 0,589 | 70 | 355 | 26 |
| Lastro, Ancoragem, Offloading e Tanques | 389 | 200 | 0,595 | 51 | 318 | 20 |
| Seg. Ocupacional, Saúde e Meio Ambiente | 300 | 300 | 0,563 | 61 | 230 | 9 |
| Utilidades e geração de energia | 250 | 250 | 0,576 | 57 | 184 | 9 |
| Operações submarinas, poços e risers | 233 | 150 | 0,587 | 36 | 182 | 15 |
| Gestão do Desempenho Empresarial (KPI) | 200 | 200 | 0,548 | 32 | 161 | 7 |
| Descomissionamento e Ciclo de Vida | 150 | 150 | 0,571 | 28 | 117 | 5 |
| Logística, Suprimentos e Movimentação | 150 | 150 | 0,574 | 19 | 124 | 7 |

Todos os tópicos atendem o mínimo do docx. Contra o corte por limiar puro do
mesmo tamanho, a composição melhora um pouco nas pontas: +26 fáceis e +26
difíceis, −52 médias.

### Clusters eliminados pelo piso

58 clusters (média de 1,5 por subtópico) ficaram inteiramente abaixo de 0,45 e
saíram. Estão listados em `saida_fase5/cota_cluster_clusters_eliminados.csv`
com tamanho, similaridade média e o id de uma questão de exemplo — é a evidência
auditável de o que o texto revisado excluiu. Lendo os maiores, o padrão é deriva
de assunto e não erro do filtro:

* *Saúde Ocupacional*, cluster de 23 questões (sim. média 0,37): qualidade da
  água potável e surto de gastroenterite, assunto de utilidades/meio ambiente;
* *Operação de Offloading*, 13 questões (0,37): by-pass de aquecedor a montante
  do separador, assunto de processo;
* *Sistema de utilidades*, 12 questões (0,32): controle de pressão em vaso
  separador, idem;
* *Gestão de Pessoas e Treinamento*, 11 questões (0,37): limpeza de costa após
  derramamento, assunto ambiental.

*Saúde Ocupacional* perde 9 dos 24 clusters, o que confirma a suspeita anterior:
ali havia deriva de assunto de verdade, não referência estreita demais.

## Alternativa ao limiar único

Subtópicos com referência mais longa e genérica pontuam mais alto, então um
limiar absoluto corta mais de uns do que de outros. O notebook tem a variante por
quantil (manter as X% mais parecidas **dentro de cada subtópico**), que preserva
a cobertura temática. A tabela de medianas por subtópico, na seção 3 do notebook,
é o que decide se vale trocar.
