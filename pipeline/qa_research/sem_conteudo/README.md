# Geração bruta sem conteúdo externo

Para completar o baseline até **4.111 questões** e avaliar sua dificuldade,
use [README_FULL.md](README_FULL.md). O fluxo abaixo documenta a geração inicial.

Gera **2.818 questões nos mesmos 40 subtópicos** da run
geracao_final_20261024T204734Z, com a mesma quantidade final por subtópico:
62 em Gestão do Desempenho, 159 em Produtos químicos, 70 em Offloading etc.

**A meta conta questões geradas, não aprovadas ou únicas.** Todas as questões com
estrutura utilizável são preservadas, inclusive repetidas, semelhantes ou fracas.
Não há auditoria, refinamento, filtro de qualidade ou deduplicação durante a geração.
A única checagem é estrutural: JSON, campos preenchidos, classificações e quantidade
solicitada. Não há revisão dos tipos declarados, estilo, correção técnica ou novidade.

O servidor lê somente o manifesto congelado de metas, com rótulos, frases originais
do especialista e contagens. Não lê questões ou documentos da run anterior.
Documentos, blocos, inventários, encadeamentos, pesquisas, exemplos e bancos herdados
não são carregados. Nenhum dataset externo de QA é usado.

## Executar no servidor

Use uma **saída nova**, distinta da versão anterior que filtrava questões:

    cd /home/gbs2/MCQ_CONTEXT_GEN
    git pull --ff-only origin codex/qa-evidencias-verificadas
    bash pipeline/qa_research/rodar_sem_conteudo.sh \
      --saida pipeline/qa_research/relatorios/sem_conteudo_bruto_v1

O padrão é **somente gerar**. O script utiliza o Python de .venv-documento,
depois venv, ou python3. DOCUMENT_PYTHON pode indicar outro executável.
As credenciais Azure e as dependências são as mesmas da instalação anterior.
Não é preciso instalar bibliotecas adicionais.

Para rodar em segundo plano e acompanhar:

    nohup bash pipeline/qa_research/rodar_sem_conteudo.sh \
      --saida pipeline/qa_research/relatorios/sem_conteudo_bruto_v1 \
      > pipeline/qa_research/relatorios/sem_conteudo_bruto_v1.console.log 2>&1 &
    tail -F pipeline/qa_research/relatorios/sem_conteudo_bruto_v1.console.log

Ctrl+C encerra o acompanhamento; a execução iniciada por nohup continua.
Repita o comando com a mesma saída para retomar.

## Método

- Um único papel de modelo: gerador gpt-5-4-petrobras:high.
- Lotes de até 5 questões, reduzindo o último lote para fechar a meta exata.
- Entrada: tópico, subtópico, frase do especialista e últimas 20 questões geradas
  no mesmo subtópico desta run. A memória só incentiva variedade; novidade não é
  condição para completar a quantidade.
- Os seis tipos continuam: conceito, mecanismo, consequencia, diagnostico, decisao,
  procedimento. O gerador também declara cenário e composição simples/composta,
  sem cotas e sem correção posterior das classificações.
- Repetições não são excluídas nem repostas; contam para a meta. A geração encerra
  assim que cada subtópico atinge sua quantidade, sem aguardar diversidade.
- Cada lote é gravado em checkpoint atômico. O cache permite recuperar uma resposta
  após interrupção anterior à gravação do checkpoint.
- Limites cumulativos: 100 lotes por subtópico e 30.000 tentativas de API para toda
  a geração, incluindo retentativas e reparos estruturais de JSON. Esses reparos
  são feitos pelo cliente de API e não são uma etapa de refinamento da qualidade.
- Falha de API ou limite atingido resulta em código 2 e progresso salvo. Não há
  tentativas extras para obter questões diferentes.
- O banco é chamado questoes.jsonl; não é exportado como aprovadas.jsonl.
  Todas as questões ficam com avaliacao_qualidade igual a nao_realizada.

Sem falhas, a quantidade de chamadas de geração é a soma de teto(meta/5) pelos
subtópicos, e não depende da taxa de duplicatas. Qualidade, variedade e redundância
são resultados a medir depois; não controlam a parada.

## Planejamento e avaliação posterior

Para listar as metas sem consumir API ou criar a saída:

    bash pipeline/qa_research/rodar_sem_conteudo.sh --plano

Para gerar um único subtópico com sua meta real:

    bash pipeline/qa_research/rodar_sem_conteudo.sh \
      --saida pipeline/qa_research/relatorios/sem_conteudo_bruto_piloto_kpi \
      --itens 01_01

A avaliação pelos mesmos seis respondentes e juiz é opcional, separada da geração.
Ela lê todas as questões geradas, inclusive repetidas ou fracas, sem alterar o banco.
Para executá-la depois da geração:

    bash pipeline/qa_research/rodar_sem_conteudo.sh \
      --saida pipeline/qa_research/relatorios/sem_conteudo_bruto_v1 \
      --so-avaliacao

Também é possível acrescentar --avaliar ao comando de geração. --sem-avaliacao
continua aceito, embora agora seja o padrão. A tabela fica em avaliacao/ACURACIA.md.
A avaliação de respostas não é um filtro e não verifica documentalmente a resposta
de referência produzida pelo gerador. Correção técnica e semelhança devem ser
analisadas posteriormente, sem remover questões desta condição experimental.

## Retomada e arquivos

Repita o comando com a mesma saída. Tópicos concluídos não chamam o modelo novamente.
O código bloqueia mistura com checkpoints da versão antiga filtrada. Mudanças em
metas, escopos, modelo, memória, lote, prompt ou código exigem outra pasta.
A seleção inicial de --itens é recuperada na retomada; outras opções não padrão,
como --lote, devem ser repetidas. Os limites podem ser aumentados sem zerar contagens:

    bash pipeline/qa_research/rodar_sem_conteudo.sh \
      --saida pipeline/qa_research/relatorios/sem_conteudo_bruto_v1 \
      --max-lotes 150 --max-chamadas 45000

Arquivos principais:

- questoes.jsonl: todas as questões, com classificações originais.
- resultado.json e RELATORIO.md: metas, quantidades geradas, classificações e falhas.
- topicos/<id>/estado.json: checkpoint e memória recente.
- topicos/<id>/finalizado.json: indica quantidade gerada igual à meta.
- geracao_concluida.json: indica que todos os subtópicos selecionados chegaram à meta.
- config.json, metas.json, limites_execucao.json, orcamento.json e chamadas/:
  protocolo, contagens e uso de API. O cache em .local/ permanece fora do Git.

O script mostra, ao terminar, a mensagem de conclusão e os comandos de coleta:

    git add -- pipeline/qa_research/relatorios/sem_conteudo_bruto_v1
    git commit -m "Resultados: sem_conteudo_bruto_v1"
    git push origin codex/qa-evidencias-verificadas

Na máquina local: git pull --ff-only origin codex/qa-evidencias-verificadas.

O manifesto foi preparado uma única vez pela ferramenta preparar_metas, que contou
as aprovadas da run de referência. A geração não importa nem executa essa ferramenta.
