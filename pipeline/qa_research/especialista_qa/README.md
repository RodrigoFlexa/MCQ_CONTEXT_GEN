# Questões do especialista em QA aberto

Para a seleção ampliada de MCQs sem reprovação explícita, usando comentários
do especialista e refatoração limitada, veja [a versão v3](README_V3.md).
As instruções abaixo descrevem o experimento histórico v2.

Converte os MCQs do documento fornecido em QAs abertas, valida a conversão e
classifica cada questão nos seis tipos e nos 40 subtópicos do programa.
O agrupamento original do DOCX é preservado separadamente da classificação.

A entrada padrão reúne **2.992 MCQs candidatas** de duas origens:

| Origem | Candidatas | Identificador |
|---|---:|---|
| Documento autoral do especialista | 2.546 | autoral_especialista |
| Questoes_100_por_topico_revisadas.docx | 446 de 1.000 | mcq_revisada_aprovada |

Todas as candidatas têm alternativas e um único gabarito explícito. Isso
verifica a estrutura de entrada, **não significa aprovação do QA convertido**.
O manifesto entrada/fontes.json referencia os dois JSONLs sem duplicar o
primeiro banco. Nenhum DOCX ou biblioteca do Word é necessário no servidor.

No DOCX revisado entram somente pareceres cujo conteúdo completo é
"aprovada", "aprovado" ou "aprovar", admitindo pontuação e espaços. Aprovações
com qualquer observação adicional, ressalvas, descartes e pareceres
indeterminados ficam fora. É uma seleção conservadora: uma observação pode
ser apenas descritiva, mas não se presume uma aprovação sem ressalvas.
Não há comparação de similaridade nesta seleção.

Foram selecionadas 446; excluídas 554: 277 descartadas/reprovadas, 272 com
observações/ressalvas e 5 pareceres indeterminados. Quatro aprovações foram
recuperadas reconhecendo grafias incorretas do rótulo "Comentário"; o texto
do parecer não foi corrigido. entrada/revisadas/curadoria.csv permite conferir
as 1.000 decisões; curadoria_todas.jsonl preserva também as MCQs completas.
Os hashes dos DOCXs e os parágrafos de origem acompanham os registros.

## Executar no servidor

### Finalizar a execução especialista_qa_v2 já publicada

    git pull --ff-only origin codex/qa-evidencias-verificadas && \
    bash pipeline/qa_research/rodar_especialista_qa.sh \
      --saida pipeline/qa_research/relatorios/especialista_qa_v2

Este comando retoma a mesma pasta: preserva as 798 QAs aprovadas e as 2.991
decisões já concluídas. A única falha ContentFiltered conhecida vira uma
exclusão documentada em bloqueadas/, sem reenviar a questão ao provedor.
Depois monta os três bancos e executa os dois respondentes em paralelo,
seguindo até o julgamento das respostas. Não use uma pasta nova para esta
retomada nem --so-avaliacao antes de concluir a conversão.

A compatibilidade é restrita ao hash da implementação que produziu esta
run. Entrada, catálogo, modelos, prompts, regras de aprovação e baselines
precisam permanecer idênticos. config.json original é preservado e
compatibilidade_retomada.json documenta o código usado na retomada.

### Nova execução

As duas entradas estruturadas já estão versionadas, incluindo alternativas,
gabarito, justificativa quando existe, agrupamento original e proveniência.
O subtópico original do DOCX revisado também é preservado quando presente;
KPI não possui subtítulo próprio no corpo do documento e mantém esse campo
vazio, enquanto a classificação nos 40 itens é feita pelo modelo.

    cd /home/gbs2/MCQ_CONTEXT_GEN
    git pull --ff-only origin codex/qa-evidencias-verificadas
    bash pipeline/qa_research/rodar_especialista_qa.sh \
      --saida pipeline/qa_research/relatorios/especialista_qa_v2

Esse comando executa:

1. Conversão e classificação por gpt-5-4-petrobras:high.
2. Validação separada por gpt-5-4-petrobras:high, recebendo original e QA candidata.
3. Exportação somente dos QAs válidos, preservando o identificador de origem
   e o parecer humano da MCQ em campos separados da validação automática.
4. Montagem dos três conjuntos para a comparação posterior.
5. Respostas sem contexto por gpt-5-4-nano-petrobras:low e
   gpt-5-4-petrobras:low no mesmo grupo, em paralelo; juiz
   gpt-5-4-petrobras:medium avalia as respostas em lotes.

Usa o ambiente .venv-documento, depois venv, ou python3. DOCUMENT_PYTHON permite
especificar outro executável. As credenciais Azure e requirements-server.txt são
as mesmas do pipeline existente. Nenhuma nova biblioteca é necessária para
conversão ou avaliação; os gráficos locais têm dependências adicionais.

Para deixar em segundo plano:

    nohup bash pipeline/qa_research/rodar_especialista_qa.sh \
      --saida pipeline/qa_research/relatorios/especialista_qa_v2 \
      > pipeline/qa_research/relatorios/especialista_qa_v2.console.log 2>&1 &
    tail -F pipeline/qa_research/relatorios/especialista_qa_v2.console.log

Ctrl+C encerra apenas o acompanhamento do log quando iniciado por nohup.

## Conferir ou fazer piloto

Planejamento, sem API e sem criar a saída:

    bash pipeline/qa_research/rodar_especialista_qa.sh --plano

Piloto com as primeiras 10 questões, incluindo avaliação pelos dois modelos:

    bash pipeline/qa_research/rodar_especialista_qa.sh \
      --saida pipeline/qa_research/relatorios/especialista_qa_piloto \
      --limite 10

Use outra saída para a execução completa. A retomada sem --limite preserva a
seleção inicial do piloto. --sem-avaliacao executa somente conversão e junção;
--so-avaliacao retoma apenas as respostas e o julgamento.

Para testar especificamente a nova origem, use uma saída própria:

    bash pipeline/qa_research/rodar_especialista_qa.sh \
      --entrada pipeline/qa_research/especialista_qa/entrada/revisadas/aprovadas_mcq.jsonl \
      --saida pipeline/qa_research/relatorios/especialista_revisada_piloto \
      --limite 10

Use a saída especialista_qa_v2 para o conjunto completo. Entradas e regras
mudaram: pastas de execuções v1 não podem ser usadas para retomar esta versão.

## Regras da conversão e validação

- Cada MCQ gera no máximo uma QA candidata; não são criadas novas questões
  sobre o assunto. O alvo, o gabarito e as condições necessárias são preservados.
- Distratores são contexto para entender a tarefa; não são incorporados como
  fatos na resposta. Não há outros bancos, exemplos ou documentos no prompt.
- Dados do DOCX são tratados como conteúdo, nunca como instruções do sistema.
- O conversor pode descartar quando uma QA autônoma e unívoca exigiria inventar
  premissas ou mudar o gabarito. A existência de um gabarito do especialista
  não obriga o validador a aceitar uma afirmação tecnicamente duvidosa.
- A validação verifica fidelidade, autonomia, ausência de resposta entregue pelo
  enunciado, univocidade, correção técnica, escopo, pergunta aberta e ausência
  de informações inventadas. Todos os critérios devem ser aprovados.
- O auditor pode corrigir tipo, cenário, composição e subtópico; não modifica
  pergunta nem resposta. As classificações originais também são registradas.
- Há checagens adicionais em código: forma aberta, pergunta até 90 palavras,
  resposta até 40, gabarito literal na pergunta, referências às alternativas,
  diagnóstico/decisão sem cenário e números novos sem sustentação no
  enunciado, na alternativa correta ou na justificativa.
- Tipos: conceito, mecanismo, consequencia, diagnostico, decisao, procedimento.
  QA aberto não obriga tipo conceito nem composição simples; essa classificação
  descreve as relações necessárias para responder. Não há cotas por tipo.
- Não há deduplicação de QAs válidas. Questões parecidas continuam no conjunto
  para que a redundância possa ser medida depois, sem alterar o baseline bruto.

A aprovação do QA convertido é automática, pelo modelo e pelas regras, sem
comprovação documental. A aprovação humana já existente refere-se à MCQ
original e não garante aprovação da conversão. O código não certifica normas,
dosagens ou limites do MCQ.
Detalhes, originais e justificativas ficam nos arquivos auxiliares de auditoria,
fora do texto da pergunta e da resposta usados pelos respondentes.

## Respostas em paralelo

Os respondentes recebem **somente a pergunta convertida**: não recebem
alternativas, gabarito, resposta de referência ou justificativa do especialista.
O juiz recebe a resposta de referência e a resposta candidata, sem o nome do
respondente no conteúdo julgado. A tabela é atualizada por blocos:

    cat pipeline/qa_research/relatorios/especialista_qa_v2/avaliacao/ACURACIA.md

A etapa avalia as QAs aprovadas do especialista, não refaz automaticamente as
respostas dos bancos anteriores. Os dois deployments são obrigatórios: falha
ou indisponibilidade de um deles resulta em execução incompleta, em vez de
sucesso silencioso com apenas um modelo.

Além do resultado geral, avaliacao/acuracia.json contém
por_conjunto_especialista. ACURACIA.md e acuracia_por_conjunto.csv separam os
denominadores e as acurácias das duas origens para cada respondente.
avaliacoes.jsonl inclui a origem, o subtópico original e o parecer humano
para análises posteriores; esses metadados não são enviados aos respondentes.

Filtros de conteúdo são resultados terminais em qualquer etapa: nunca são
contornados por reformulação, divisão de lote ou novas tentativas. Na
conversão/validação, a questão fica excluída do banco aprovado. Nos respondentes
ou no juiz, o bloqueio é registrado por questão/modelo com veredito null;
não é transformado em acerto nem erro técnico. A acurácia usa apenas respostas
julgadas; total, processadas, não avaliadas e cobertura são apresentados
separadamente, inclusive por origem. Um bloqueio do juiz abrange todo o lote
enviado e preserva as respostas existentes.

avaliacao_concluida.json só é criado quando ambos os modelos têm uma resposta
ou bloqueio registrado para cada QA e cada caso tem julgamento ou bloqueio
terminal. O status indica concluida ou concluida_com_bloqueios. Falhas de
autenticação, rede ou formato não viram exclusões: mantêm a execução incompleta
e podem ser retomadas pelo mesmo comando. Respostas e julgamentos salvos não
são refeitos.

## Retomada e limites

Repita o mesmo comando com a mesma --saida. Conversões, validações e decisões
são salvas separadamente por questão; uma falha na validação não refaz uma
conversão já concluída. Questões reprovadas são decisões finais desta run e
não ficam sendo reescritas até passar. Reparos estruturais de JSON e retentativas
de API continuam limitados a três tentativas por chamada no cliente existente.

Padrões: oito trabalhadores e orçamento de 20.000 tentativas cumulativas de
API para conversão/validação, incluindo reparos. --max-chamadas pode aumentar
o limite sem zerar o uso. A avaliação de respostas usa o orçamento do avaliador
existente. Não há chamada paga na extração, planejamento ou testes offline.

Alterar entrada, catálogo, código, prompts ou bancos de referência exige nova
saída. Um bloqueio impede processos simultâneos na mesma pasta. Falhas retornam
código 2 e preservam progresso. A avaliação só começa com conversão concluída.

A única exceção para mudança de código é a retomada compatível descrita acima:
ela aceita a implementação original conhecida da run v2, mantendo o restante
do protocolo e todas as decisões já concluídas.

## Três conjuntos preparados

O manifesto bancos/manifesto.json aponta para:

| Conjunto | Conteúdo |
|---|---|
| Sem contexto | As mesmas 2.818 questões de sem_conteudo_bruto_v1 |
| Com contexto sem questões do especialista | As mesmas 2.818 aprovadas de geracao_final_20261024T204734Z |
| Com contexto com questões do especialista | As 2.818 anteriores + somente as QAs aprovadas do especialista |

O novo conjunto é um arquivo separado; os dois bancos anteriores não são
modificados. IDs e hashes permitem conferir a integridade e a proveniência.
A quantidade de QAs aprovada em cada origem será conhecida após a execução
real. Ambos os grupos de especialistas entram no conjunto ampliado; os três
conjuntos da comparação anterior continuam sendo os mesmos.

## Gráficos depois de coletar os resultados

Depois do commit/push no servidor e pull local, em um Python com NumPy,
scikit-learn, Matplotlib, PyTorch, Transformers e o mesmo E5 local já usado:

    python -m pipeline.qa_research.especialista_qa graficos \
      --saida pipeline/qa_research/relatorios/especialista_qa_v2

Gera PNG/SVG de similaridade lexical/semântica e vocabulário dos três bancos,
com TTR, MATTR, comprimentos e contagens. Usa a mesma tokenização e a lista
congelada de stopwords da análise anterior; E5 multilíngue na mesma revisão.
O IDF é comum aos três bancos, contando cada UID uma vez na união para não
duplicar artificialmente o peso do banco base incluído no conjunto ampliado.

O conjunto ampliado terá mais questões e palavras: TTR bruto é sensível ao
tamanho, então MATTR e contagens também são apresentados. Cosseno E5 não é
porcentagem de igualdade. As diferenças de origem, composição, filtros e
volume não permitem atribuir causalidade apenas ao acréscimo do especialista.
Não há download automático de modelo nem uso de API para esses gráficos.

## Saídas e coleta

- aprovadas.jsonl: QAs válidas do especialista, com agrupamento original e item classificado.
- decisoes.jsonl, reprovadas.jsonl e revisao_conversoes.csv: resultados e motivos por questão.
- conversoes/ e validacoes/: saídas originais dos dois estágios.
- bancos/com_contexto_com_especialista.jsonl e bancos/manifesto.json: junção e três conjuntos.
- resultado.json e RELATORIO.md: contagens, tipos e resumo.
- por_conjunto_especialista nos resumos: seleção e aprovação separadas por origem.
- avaliacao/: respostas dos dois modelos, vereditos do juiz e tabela de acurácia.
- .local/ contém caches e respostas brutas de API, ignorados pelo Git.

Ao terminar, o script mostra a mensagem de conclusão e os comandos de coleta:

    git add -- pipeline/qa_research/relatorios/especialista_qa_v2
    git commit -m "Resultados: especialista_qa_v2"
    git push origin codex/qa-evidencias-verificadas

Na máquina local:

    git pull --ff-only origin codex/qa-evidencias-verificadas

Para repetir a extração de outro DOCX com o mesmo formato, sem API:

    python -m pipeline.qa_research.especialista_qa extrair --docx CAMINHO.docx --saida NOVA_ENTRADA

Gabaritos ausentes/conflitantes e estruturas não reconhecidas ficam em pendencias.jsonl;
não são adivinhados. A extração também registra divergências de contagem por agrupamento.

Para reproduzir a curadoria do segundo documento, sem API:

    python -m pipeline.qa_research.especialista_qa extrair-revisadas \
      --docx "Comentários especialista/Questoes_100_por_topico_revisadas.docx"

O servidor lê somente as 446 selecionadas. Os 1.000 registros de curadoria
são auxiliares e não são enviados ao conversor. O leitor verifica novamente
o parecer humano antes de qualquer chamada, mesmo em uma entrada JSONL avulsa.
