# Histórico: piloto fixo de 60 questões

Esta é a documentação da implementação anterior. O script rodar_piloto_qa.sh
agora executa o fluxo contínuo descrito em README.md. Para reproduzir este piloto
fixo, usar `python -m pipeline.qa_research.piloto_qa` diretamente em vez do script
shell dos exemplos antigos abaixo. Usar saídas distintas para cada mecanismo.

Meta escolhida: **60 questões novas sobre os contextos ajustados, 20 em cada um
dos documentos 02_02, 03_03 e 07_01**. O código está separado dos geradores históricos;
reutiliza transporte, orçamento, cache, avaliação e fórmulas existentes. Não executa
busca de corpus nem baixa ou modifica datasets externos de questões.

## O experimento

| Grupo | Gerador | Documento | Meta |
|---|---|---|---:|
| historico | Questões já aprovadas no banco Default | Contextos originais de geração | 60 selecionadas |
| novo_antigo | Novo gerador | dez_areas_final_v2 | 60 novas |
| novo_refinado | Novo gerador | Terceiro piloto com fechamento editorial explícito | 60 novas |

São **120 questões novas e 60 históricas**, não 180 novas. O histórico é amostrado
deterministicamente por documento e classe. Há entre 70 e 159 questões disponíveis
por documento no banco atual. Não se usa a média global das 2.818 como controle
direto para um piloto de três assuntos. O relatório mantém essa média como contexto
histórico na conversa; a comparação principal recalcula a amostra.

As perguntas dos três grupos são diferentes. Isso permite comparar o novo método
com o banco anterior e comparar o novo gerador sob duas bases. Não é um experimento
fatorial completo: não geramos com o método antigo nos documentos novos. Diferenças
entre grupos não são ganhos pareados por pergunta nem isolam algoritmo, modelo,
comprimento do contexto e seleção de conteúdo como efeitos causais separados.
O conteúdo novo também representa ampliação de base, além de edição.

O que é pareado: **a mesma pergunta respondida com e sem contexto**, por cada modelo.
Uma comparação de acurácia entre bancos diferentes não é o closed-book gap.

## Ajustes documentais

`documents.py` produz uma edição nova em `contextos/refinado/`, sem sobrescrever os
snapshots de experimentos anteriores. Os reparos são explícitos, verificáveis e
registrados em `revisao.json`, com texto anterior/posterior e hashes:

- Químicos: retirar redundância interna de bioincrustação e quatro marcas de relato
  de leitura; recuperar a distinção entre clarificante/floculante/quebrador da
  rodada intermediária; apresentar a definição de MEG antes das aplicações.
- Tanques: recuperar a inclusão anterior de P/V valves, mast risers e flame screens;
  retirar narrativa de investigação e composição particular de vapores sem
  transformar os resultados do caso em regra universal.
- Instrumentação: retirar resultado particular de compensação por pulsos, concentrar
  o exemplo com N2 e remover relato de caso/fechamento desconectado no bloco de bypasses.

As quatro correções protegidas do especialista são verificadas literalmente. Se a
base mudar e uma substituição não corresponder, a preparação para com erro explícito.
Os originais ficam intactos. As pendências reais, como água de lastro, backups e
sobressalentes, permanecem no manifesto. Não são preenchidas com conhecimento do
modelo. O gerador recebe essas pendências e deve avaliar apenas relações sustentadas
pelos blocos fornecidos. Trata-se de **piloto com escopo delimitado**, não de liberação
automática dos 40 documentos nem de certificação de todo o conteúdo.

## Como as questões são geradas

1. Fixar documento, escopo, configuração, exemplos e versões por hash.
2. Planejar até 40 alvos suportados para tentar obter 20 questões por documento.
   Cada alvo já contém afirmações, condições e citações literais dos blocos. Os
   blocos podem ser distantes. Há cotas de referência para as seis classes:
   conceito, mecanismo, consequência, diagnóstico, decisão e procedimento.
3. Redigir em lotes de até quatro. Cada alvo tem seu próprio conjunto de blocos;
   evidências da questão precisam pertencer a esse conjunto. O enunciado tem uma
   demanda e até 90 palavras. O gabarito mínimo tem até 60 palavras, com critérios
   essenciais, formulações equivalentes e erros materiais separados.
4. Resolver sem receber o gabarito. O resolvedor recebe pergunta e contexto, e
   registra ambiguidades. Acerto ou erro dele não determina dificuldade/aceitação.
5. Julgar todas as afirmações da resposta mínima e os critérios essenciais contra
   os blocos, além de autonomia, determinação, pistas, variedade e composição.
   A aprovação inclui evidência literal por critério essencial. Inferências precisam
   declarar sua ligação, preservando premissas e limites.
6. Reparar apenas candidatas recuperáveis, uma vez, e resolver/julgar novamente.
   Falha no reparo não apaga questões já admitidas. IDs, alvo e classe permanecem
   fixos; sem suporte, a candidata fica como lacuna documental ou é descartada.
7. Comparar com as admitidas por conhecimento, demanda, condições e conclusão.
   Duplicatas exatas são barradas localmente; duplicação semântica é julgada com
   inventário de questões. Uma troca de cenário não basta para indicar novidade.
8. Encerrar na meta, no esgotamento de alvos, após três lotes sem ganho, após 15
   lotes ou no orçamento de 150 tentativas por grupo/documento. Sem forçar a meta.

Conceito continua simples; diagnóstico e decisão exigem cenário. A composta exige
duas relações e uma ponte necessária. O revisor confere se uma única evidência já
resolveria a demanda. **Não há teste automático de ablação A/B nesta versão**: a
classificação de integração ainda é um julgamento e deve ser analisada no piloto.

Os exemplos padrão são seis questões próprias de outros subtópicos, uma de cada
classe, excluindo todos os três assuntos do experimento. Servem somente como forma.
`--examples caminho.jsonl` permite ler explicitamente exemplos já existentes,
inclusive externos. Nada é baixado. O histórico selecionado para comparação não é
fornecido ao redator como exemplo nem é usado para completar suporte factual.

O desenho de integração tem relação com a preocupação de evitar atalhos de uma
única evidência discutida no [MuSiQue](https://aclanthology.org/2022.tacl-1.31/).
Não reivindicamos reproduzir o protocolo desse benchmark.

## Modelos

| Papel | Deployment e esforço |
|---|---|
| Planejamento | gpt-5-4-petrobras medium |
| Autoria e um refino | gpt-5-4-petrobras medium |
| Resolução sem gabarito na geração | gpt-5-petrobras medium |
| Juízo de admissão | gpt-5-4-petrobras high |
| Respostas na avaliação congelada | GPT-4.1 Nano, Mini e GPT-4.1, sem effort |
| Juízo de respostas e auditoria adicional | gpt-5-4-petrobras medium |

Os prompts novos estão em `prompts.py`. A avaliação reutiliza literalmente os
prompts de `../benchmark_gap_prompts/`. Os respondentes têm o mesmo limite solicitado
de 100 palavras nos dois braços. O novo esquema de rubrica é usado na geração;
o juiz comparativo continua congelado para manter o protocolo histórico.

## Métricas e comparação

- Overlap Q C sem stopwords, Max ROUGE-L F1 por frase com/sem stopwords e Jaccard.
- Novel bigramas/trigramas da resposta mínima; não cria n-gramas entre blocos.
  Respostas curtas demais ficam ausentes, com denominador registrado.
- Self-BLEU-4 com smoothing método 1; duplicatas normalizadas.
- Cosseno médio, distância, vizinho e Vendi com E5 local opcional, mesma revisão,
  prefixo query e normalização L2. Sensibilidade centrada é reportada separadamente.
- Acurácia estrita e gap pareado com IC 95 por bootstrap. Parciais contam como zero;
  bloqueios/falhas ficam sem nota e aparecem na cobertura, nunca como erro fictício.
- Auditoria **adicional à admissão** dos gabaritos por afirmação, com o mesmo
  protocolo anterior. Não se reporta a própria aprovação do gerador como faithfulness.
  Há sensibilidade dos gaps restrita aos gabaritos sustentados.

As métricas lexicais foram trazidas para funções reutilizáveis com as mesmas
definições do cálculo anterior. Não importamos o script histórico `calcular.py`,
pois ele executa toda a análise e grava arquivos ao ser importado. Não há lematização
simulada. As amostras comparáveis usam o mínimo disponível por documento/classe em
todos os grupos, com seleção por seed; o relatório também preserva resultados integrais.

ROUGE baixo e novidade alta não provam raciocínio nem verdade. Não se usam os
limiares sugeridos na conversa como filtros de aprovação. Self-BLEU e Vendi dependem
de N e composição da amostra. O [Vendi original](https://arxiv.org/abs/2210.02410)
define o escore a partir de um kernel de similaridade; preservamos o kernel e
reportamos a geometria, sem interpretar o número como contagem literal de perguntas.

São candidatos a revisão humana: baixa sustentação, contradições, questões compostas
e respostas divergentes. O juiz automático continua sujeito a erro. Medimos também
taxa de admissão e consumo por grupo; uma métrica melhor após forte descarte não
deve esconder produtividade baixa. Esta versão não seleciona questões por erro
dos GPT-4.1 nem otimiza diretamente o tamanho do gap.

## Executar no servidor

Na raiz do repositório, com o Python correto:

```bash
git pull --ff-only origin codex/qa-evidencias-verificadas
export DOCUMENT_PYTHON="$PWD/.venv-documento/bin/python"
"$DOCUMENT_PYTHON" -m pip install -r pipeline/qa_research/piloto_qa/requirements.txt

# Confere ajustes e mostra volumes, sem API e sem escrever saída.
bash pipeline/qa_research/rodar_piloto_qa.sh --plan

# Ajusta os contextos e gera os dois grupos novos; histórico é apenas amostrado.
nohup bash pipeline/qa_research/rodar_piloto_qa.sh --stage generate \
  > piloto_qa_60_geracao.log 2>&1 &
tail -F piloto_qa_60_geracao.log
```

`DOCUMENT_PYTHON` pode apontar ao venv existente que já tenha as dependências.
Não instalar os pacotes num Python diferente do usado pelo script.

Depois que a geração terminar, medir e avaliar na mesma saída:

```bash
# Local, sem chamadas pagas; não modifica as questões.
bash pipeline/qa_research/rodar_piloto_qa.sh --stage metrics

# Usa modelos pagos, com e sem contexto, e auditoria adicional dos gabaritos.
nohup bash pipeline/qa_research/rodar_piloto_qa.sh --stage evaluate \
  > piloto_qa_60_avaliacao.log 2>&1 &
tail -F piloto_qa_60_avaliacao.log
```

Se as metas forem atingidas, a avaliação terá **1.080 casos de resposta**
(180 questões × dois braços × três modelos), mais julgamentos e até 180 auditorias.
São limites de volume de casos, não previsão de número de requisições/tokens.
`--mini-deployment nome` adapta apenas o alias do Mini. Mudança invalida a retomada
da avaliação e exige nova saída para não misturar modelos.

As métricas semânticas exigem um ambiente com PyTorch, sentence-transformers e
o snapshot E5 já local. A instalação padrão não baixa esses pesos. É possível
calculá-las aqui depois de coletar, ou no venv do servidor que já tenha o modelo:

```bash
bash pipeline/qa_research/rodar_piloto_qa.sh --stage metrics --embeddings
```

Ausência de pesos falha explicitamente; nenhum número é preenchido artificialmente.
Não é necessário executar essa opção para gerar ou avaliar as perguntas.

## Saídas e coleta

Saída padrão `pipeline/qa_research/saida_piloto_qa/piloto_60_v1`:

- `contextos/`: documentos antigos/refinados, ajustes, hashes e pendências.
- `historico.jsonl`, `protocolo.json`: controle e identidade congelados.
- `geracao/<grupo>/<item>/`: plano evidencial, perguntas admitidas, decisões,
  resolução independente, reparos, contagens e consumo. Brutas/cache ficam em `.local`.
- `metricas/RESULTADOS.md`, `metricas.json`, `por_questao.jsonl`: análise lexical e
  semântica opcional; resultados integrais e amostras equilibradas.
- `avaliacao_comparavel/RESULTADOS.md`, `comparacao.json`, `pares.csv` e `faithfulness.jsonl`:
  resultados dos três grupos, pares por questão e evidências da auditoria.

Para continuar uma interrupção, repetir o comando. Chamadas válidas são reutilizadas.
Alterar documento, prompt, modelo ou configuração de conteúdo exige nova saída.
Geração parcial não é fabricada como 60 questões; contagens reais e impedimentos
ficam no resumo. Retorno 2 indica parcial e permite coleta para análise.

Coletar somente depois das etapas desejadas, para destino novo:

```bash
"$DOCUMENT_PYTHON" -m pipeline.qa_research.piloto_qa \
  --collect pipeline/qa_research/relatorios/piloto_qa_60_v1
git add -- pipeline/qa_research/relatorios/piloto_qa_60_v1
git commit -m "Resultados do piloto comparavel de QA"
git push origin codex/qa-evidencias-verificadas
```

Se esse destino já existir, usar outro nome. A coleta exclui arquivos privados e
cache e inclui hashes. Não altera nenhum resultado histórico. A futura decisão
de ampliar N ou liberar produção deve vir da leitura deste piloto, não da simples
aprovação automática do gerador.

## Verificação offline

```bash
python -m unittest discover -s pipeline/qa_research/piloto_qa/tests -v
```

Fixtures usam modelos simulados e cobrem preparação real dos três documentos,
proteções, citação literal, duplicatas, orçamento, retomada, falha de reparo,
denominadores, Vendi com geometria conhecida e integração com o benchmark original.

Na validação local desta implementação passaram 20 testes do piloto, 10 do
benchmark reutilizado e 46 dos componentes v3. As métricas lexicais de 60 questões
históricas também reproduziram os resultados já calculados, sem diferenças acima
de 1e-10. Não foram feitas chamadas pagas nem produzidos resultados de qualidade
para as questões novas nesta máquina; isso depende da execução no servidor.
