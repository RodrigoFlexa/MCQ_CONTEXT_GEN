# Planejamento e controle de planos e ordens de manutenção

## 1. Finalidade e recorte da faceta
Este documento consolida conceitos e práticas de **planejamento e controle da manutenção** aplicáveis à gestão de planos e ordens de manutenção, com foco em **priorização, programação, tratamento de atrasos, backlog e realimentação dos planos**. O material de origem combina estudos acadêmicos e mapeamentos de processo em ambientes industriais e terminais; portanto, deve ser lido como **base técnica de trabalho**, não como requisito normativo nem como modelo certificado para um FPSO específico.

Em contexto de FPSO/FSO, a utilidade principal deste conteúdo está em estruturar o fluxo entre **plano de manutenção**, **ordem de manutenção**, **programação com a operação**, **execução em campo**, **encerramento técnico** e **revisão dos planos com base no histórico**. (Fontes: `regis-7493a0b7af9688fbb59924e0:pNone:1105.0-1326.0`, `regis-712143aa49549e5339b71436:pNone:5624.0-5926.0`, `regis-712143aa49549e5339b71436:pNone:5928.0-6528.0`)

## 2. Conceitos estruturantes

### 2.1 Plano de manutenção, lista de tarefas e ordem de manutenção
Os trechos analisados diferenciam claramente três níveis:

1. **Plano de manutenção**: conjunto de informações necessárias para orientar a atividade de manutenção preventiva. O plano fica associado ao equipamento ou grupo de equipamentos e contém a lógica de execução, periodicidade e demais parâmetros de controle.
2. **Lista de tarefas**: conjunto de tarefas elaborado pelo centro de trabalho responsável, usado para orientar a execução das ordens de manutenção sistemática.
3. **Ordem de manutenção / ordem de serviço**: documento operacional gerado quando o plano atinge o ponto de execução ou quando uma necessidade não sistemática é formalizada e liberada no sistema.

Assim, o plano **não é a execução em si**; ele é o mecanismo que, quando chega a data, condição ou critério de disparo, **gera a ordem** para execução. Esse encadeamento é central para qualquer CMMS/SAP PM bem governado. (Fontes: `regis-7493a0b7af9688fbb59924e0:pNone:1105.0-1326.0`, `regis-7493a0b7af9688fbb59924e0:pNone:4171.0-4401.0`, `regis-7493a0b7af9688fbb59924e0:pNone:4286.0-4549.0`)

### 2.2 Manutenção preventiva sistemática e condicional
O material distingue duas bases importantes para elaboração do plano:

- **Preventiva sistemática/periódica**: executada em intervalos constantes, como horas de funcionamento, produção ou outro contador. É mais coerente quando o mecanismo de falha é tipicamente associado a desgaste e quando a periodicidade representa adequadamente o comportamento do item.
- **Preventiva condicional**: baseada em acompanhamento do estado do equipamento por meios de vigilância sistemáticos, como análise de vibração, termografia, parâmetros de desempenho, inspeção visual e medições ultrassônicas, permitindo intervir antes da falha funcional.

Para planejamento e controle, a diferença é decisiva: a manutenção sistemática tende a gerar ordens por calendário/ciclo; a condicional depende de **critérios de condição e monitoramento**, exigindo integração mais forte entre inspeção, diagnóstico e programação. (Fontes: `regis-7493a0b7af9688fbb59924e0:pNone:1105.0-1326.0`)

### 2.3 PCM como órgão de suporte
Os textos definem o **Planejamento e Controle da Manutenção (PCM)** como função de suporte responsável por automatizar, organizar e controlar o fluxo da manutenção preventiva/preditiva, conectando cadastro, planos, programação e geração de ordens. Em termos práticos, o PCM é o elo entre engenharia, operação, executantes, almoxarifado e gestão. (Fontes: `regis-7493a0b7af9688fbb59924e0:pNone:1105.0-1326.0`)

## 3. Estrutura do plano de manutenção e do Plano Mestre

### 3.1 O que o plano precisa conter
O planejamento deve descrever, no mínimo:

- **o que** deve ser feito;
- **quem** deve fazer;
- **quando** deve ser feito;
- **materiais** e **ferramentas** necessários;
- **procedimentos** aplicáveis.

Na prática, isso se desdobra em planos individuais por equipamento ou sistema, com tarefas delegadas, periodicidades e recursos necessários. Sem esse detalhamento, a ordem emitida tende a chegar ao campo incompleta, elevando retrabalho, reprogramação e backlog. (Fontes: `regis-7493a0b7af9688fbb59924e0:pNone:1105.0-1326.0`)

### 3.2 PMMP / plano mestre
O **Plano Mestre de Manutenção Preventiva (PMMP)** é tratado como agregação estruturada das tarefas de manutenção preventiva sistemática, programadas por computador para posterior geração de ordens de serviço. Os textos citam como informações relevantes do PMMP:

- centro técnico responsável;
- descrição do equipamento;
- número do plano de manutenção;
- semana planejada;
- data planejada;
- número da solicitação;
- status da solicitação;
- periodicidade do plano;
- local de instalação.

Para fins de controle em FPSO, essa estrutura é útil porque permite consolidar a visão de longo prazo e desdobrá-la em janelas mensais e semanais, sem perder a rastreabilidade por equipamento e por disciplina. (Fontes: `regis-7493a0b7af9688fbb59924e0:pNone:4171.0-4401.0`, `regis-7493a0b7af9688fbb59924e0:pNone:1105.0-1326.0`)

### 3.3 Relação entre estratégia, rotas e ordens
A implantação do PMMP é descrita em três etapas:

1. definição da estratégia;
2. elaboração dos planos sistemáticos e preditivos, além de rotas como inspeções e lubrificações;
3. elaboração das ordens de serviço.

Essa lógica é relevante porque mostra que a qualidade da ordem depende da qualidade da estratégia e do plano. Uma ordem mal estruturada costuma ser sintoma de falhas anteriores no cadastro, na lista de tarefas, nas rotas ou nos critérios de intervenção. (Fontes: `regis-7493a0b7af9688fbb59924e0:pNone:1105.0-1326.0`)

## 4. Macrofluxo de planejamento e controle no CMMS/SAP

Os trechos mapeiam um fluxo macro consistente para gestão da manutenção. Adaptado ao contexto desta faceta, ele pode ser entendido em oito blocos.

### 4.1 Gestão da manutenção e cadastro
Ponto de partida do processo. Inclui:

- criar/atualizar cadastro dos equipamentos;
- criar/atualizar planos preventiva, preditiva e calibração;
- criar/atualizar planos para testes e inspeções, quando houver interface com inspeção.

A entrada são informações de engenharia, fabricante e histórico; a saída é o cadastro no sistema pronto para emissão das solicitações de serviço. Sem cadastro robusto, o sistema não consegue programar adequadamente nem produzir histórico confiável. (Fontes: `regis-712143aa49549e5339b71436:pNone:5624.0-5926.0`, `regis-712143aa49549e5339b71436:pNone:5928.0-6528.0`)

### 4.2 Emissão das solicitações
Há duas origens principais:

- **programada pelo sistema**, a partir dos planos de manutenção, inspeção, calibração ou recomendações correlatas;
- **não programada**, a partir de solicitação corretiva, melhoria ou necessidade emergente comunicada por operação ou outra parte interessada.

No caso não sistemático, o texto cita a **nota de manutenção** emitida por um notificador para formalizar a necessidade de atendimento. Isso é importante porque separa a identificação da necessidade da posterior análise e liberação da ordem. (Fontes: `regis-712143aa49549e5339b71436:pNone:5624.0-5926.0`, `regis-7493a0b7af9688fbb59924e0:pNone:4286.0-4549.0`)

### 4.3 Análise das solicitações
Nesta etapa, avalia-se se a demanda realmente deve ser executada e sob que forma. O material aponta análise de:

- necessidade real do serviço;
- custo aproximado;
- criticidade para o processo;
- executante responsável;
- necessidade de apoio externo, administrativo ou de outro setor.

Para a faceta de priorização, essa é a etapa em que uma solicitação deixa de ser apenas um pedido e passa a ser um item classificado e preparado para planejamento. (Fontes: `regis-712143aa49549e5339b71436:pNone:5624.0-5926.0`)

### 4.4 Planejamento do serviço
O planejamento do serviço é detalhado com um conjunto de entregáveis práticos:

- sequência das tarefas;
- recursos humanos: executante, quantidade de pessoas e duração de cada tarefa;
- materiais e sobressalentes;
- padrão de execução;
- ferramentas e dispositivos;
- prazo e custo total da intervenção;
- medidas para restabelecimento de limpeza e organização;
- planejamento operacional, incluindo matriz de isolamento, análises de risco e formulários específicos.

Este é um ponto crítico para FPSO: ordens atrasadas ou reprogramadas frequentemente decorrem de planejamento incompleto, especialmente em materiais, ferramentas, isolamentos, PT e interfaces operacionais. (Fontes: `regis-712143aa49549e5339b71436:pNone:5624.0-5926.0`, `regis-712143aa49549e5339b71436:pNone:5780.0-6189.0`)

### 4.5 Programação do serviço
A programação é a negociação com a operação sobre **quando** o serviço planejado poderá ser executado. Os textos indicam que essa etapa:

- verifica a prioridade dos serviços;
- nivela a carteira para que os de maior prioridade sejam executados na semana seguinte;
- refina a programação com partes interessadas, tipicamente em reunião semanal;
- confirma data de liberação, PT e retorno do equipamento à operação.

Também é atribuição do programador:

- desdobrar o plano em programação mensal e semanal;
- validar a programação com as partes interessadas;
- avaliar backlog e estratégias para reduzi-lo;
- confirmar disponibilidade da produção/linha para intervenção;
- verificar mão de obra disponível;
- confirmar disponibilidade de material.

Essa etapa é o centro do **controle de atrasos**, porque é onde a carteira planejada é transformada em compromisso executável. (Fontes: `regis-7493a0b7af9688fbb59924e0:pNone:4171.0-4401.0`, `regis-7493a0b7af9688fbb59924e0:pNone:4286.0-4549.0`, `regis-712143aa49549e5339b71436:pNone:5624.0-5926.0`, `regis-712143aa49549e5339b71436:pNone:5928.0-6528.0`)

### 4.6 Emissão e distribuição das ordens
Após programação definida, o PCM emite as ordens no SAP/CMMS e distribui aos centros técnicos responsáveis. Para ordens sistemáticas, o programador verifica antecipadamente as datas e gera ordens no horizonte definido, frequentemente semanal. Para ordens não sistemáticas, o programador acompanha as notas pendentes, libera, emite e distribui as ordens correspondentes. (Fontes: `regis-7493a0b7af9688fbb59924e0:pNone:4171.0-4401.0`, `regis-7493a0b7af9688fbb59924e0:pNone:4286.0-4549.0`)

### 4.7 Execução, testes e entrega
Na execução, os textos destacam:

- execução conforme planejado e programado;
- registro das informações técnicas na ordem;
- realização de testes operacionais para devolução do equipamento;
- emissão de relatórios de execução e de testes;
- encerramento da PT.

Do ponto de vista de controle, isso significa que uma ordem só deve ser considerada tecnicamente concluída quando houver evidência registrada de execução e, quando aplicável, de testes pós-manutenção e entrega para operação. (Fontes: `regis-712143aa49549e5339b71436:pNone:5928.0-6528.0`)

### 4.8 Encerramento técnico e histórico
Após a execução, devem ser lançadas no sistema as informações do serviço executado, incluindo horas gastas, dados de execução e histórico do equipamento. O encerramento técnico atualiza o CMMS/SAP e alimenta o banco de dados para indicadores e análises futuras.

Sem esse fechamento disciplinado, não há base confiável para medir aderência do plano, tempo de reparo, reincidência, custos ou revisão de periodicidades. (Fontes: `regis-7493a0b7af9688fbb59924e0:pNone:4286.0-4549.0`, `regis-712143aa49549e5339b71436:pNone:5624.0-5926.0`, `regis-712143aa49549e5339b71436:pNone:5928.0-6528.0`)

## 5. Priorização de serviços e hierarquização da carteira

### 5.1 Critérios de priorização
O material aponta dois níveis complementares de priorização.

**No curto prazo**, a programação semanal nivela a carteira para executar primeiro os itens de maior prioridade, considerando restrições operacionais e de recursos. (Fontes: `regis-712143aa49549e5339b71436:pNone:5624.0-5926.0`, `regis-7493a0b7af9688fbb59924e0:pNone:4286.0-4549.0`)

**Na implantação e estruturação dos planos**, um estudo propõe classificar sistemas pela consequência em três dimensões:

- saúde, segurança e meio ambiente;
- produção;
- custo.

Além das classes alta, média e baixa, o autor propõe uma classe **altíssima** para equipamentos críticos de segurança operacional, salvaguardas de estudos de risco e sistemas críticos de segurança. Em sua sugestão de implantação, devem ser priorizados primeiro:

1. sistemas ligados diretamente à segurança operacional;
2. sistemas de medição de fluidos associados a atendimento legal aplicável no caso estudado;
3. sistemas com maiores perdas de produção em caso de indisponibilidade, identificáveis por modelagem RAM;
4. sistemas com impacto irrelevante por último.

Para FPSO, isso fornece um critério útil de ordenação da carteira e do rollout do plano, sem substituir a matriz de criticidade própria da empresa. (Fontes: `regis-74dd376119cbb653fe9922bc:pNone:5451.0-5740.0`)

### 5.2 Integração manutenção-produção
Um dos trechos ressalta que muitos trabalhos tratam manutenção olhando apenas variáveis da própria manutenção, sem integrar adequadamente o plano de produção. Outro estudo de caso mostra que a falta de integração entre o plano mestre de produção e o plano mestre de manutenção desloca a gestão para o curtíssimo prazo, aumentando dependência de reprogramações.

Para planejamento e controle, isso significa que a priorização não deve ser feita apenas por urgência percebida ou por data original do plano. Ela precisa considerar o efeito da indisponibilidade sobre o modo de operação do sistema produtivo, inclusive quando a parada de um item altera a operação de outros subsistemas. (Fontes: `regis-0e3ade70c2795843d646ab84:pNone:197.0-238.0`, `regis-7493a0b7af9688fbb59924e0:pNone:4171.0-4401.0`)

## 6. Controle da programação, backlog e tratamento de atrasos

### 6.1 O que controlar
Os textos indicam alguns controles essenciais para o PCM:

- aderência entre manutenção preventiva/corretiva programada e executada;
- backlog de manutenção;
- disponibilidade de material;
- disponibilidade de mão de obra;
- disponibilidade da instalação/linha/equipamento para intervenção;
- pendências de notas de manutenção;
- encerramento tempestivo das ordens.

Em ambiente offshore, isso equivale a controlar não apenas a existência da ordem, mas sua **executabilidade real** dentro da janela operacional e logística disponível. (Fontes: `regis-7493a0b7af9688fbb59924e0:pNone:4171.0-4401.0`, `regis-7493a0b7af9688fbb59924e0:pNone:4286.0-4549.0`)

### 6.2 Causas recorrentes de atraso observadas no material
Os estudos apontam fatores que tendem a empurrar ordens para atraso ou backlog:

- falta de integração entre manutenção e produção;
- foco excessivo na programação de curto prazo;
- indisponibilidade ou atraso de materiais e contratações;
- ausência de desdobramento consistente entre custos reais das ordens e planejamento orçamentário;
- necessidade de refinamento semanal com múltiplas partes interessadas;
- equipe potencialmente subdimensionada em relação à carga de trabalho;
- planejamento incompleto do serviço.

Esses fatores não são exclusivos de plantas em terra e podem ser ainda mais sensíveis em FPSO, onde mobilização, janelas operacionais e sobressalentes críticos aumentam a consequência do atraso. (Fontes: `regis-7493a0b7af9688fbb59924e0:pNone:4171.0-4401.0`, `regis-7493a0b7af9688fbb59924e0:pNone:3734.0-3956.0`, `regis-7493a0b7af9688fbb59924e0:pNone:4286.0-4549.0`, `regis-712143aa49549e5339b71436:pNone:5624.0-5926.0`)

### 6.3 Tratamento técnico de ordens atrasadas
Com base no material, o tratamento de ordens atrasadas ou não executadas no período programado deve passar, no mínimo, por nova verificação de:

- prioridade e criticidade do serviço;
- pertinência da execução;
- disponibilidade de material e sobressalentes;
- disponibilidade de mão de obra e de apoio externo;
- liberação operacional e janela de parada/intervenção;
- requisitos de isolamento, risco, PT e demais preparativos;
- impacto sobre backlog e carteira da semana seguinte.

Em outras palavras, a reprogramação não deve ser apenas mudança de data. Ela exige revalidação das premissas de execução. (Fontes: `regis-712143aa49549e5339b71436:pNone:5624.0-5926.0`, `regis-7493a0b7af9688fbb59924e0:pNone:4286.0-4549.0`)

### 6.4 Reprogramação e governança
Um estudo de caso informa que a ordem de manutenção sistemática possui período de execução que pode ser reprogramado apenas uma vez, enquanto ordens não sistemáticas não possuem período de execução definido da mesma forma. Para uso profissional, o ponto técnico mais importante não é universalizar essa regra, e sim reconhecer que o processo local deve definir:

- quais ordens podem ser reprogramadas;
- quantas vezes;
- sob qual aprovação;
- como o atraso impacta prioridade, risco e histórico.

A governança da reprogramação é parte do controle do plano. Sem ela, o plano perde capacidade de distinguir o que está em conformidade do que está vencido, postergado ou cronicamente adiado. (Fontes: `regis-7493a0b7af9688fbb59924e0:pNone:4286.0-4549.0`)

## 7. Preparação da ordem para execução

Uma ordem de manutenção com boa qualidade de planejamento deve chegar ao executante com requisitos já verificados. O material lista explicitamente itens a serem tratados antes da programação/execução:

- recursos humanos e quantidade de pessoas;
- materiais e sobressalentes;
- ferramentas e dispositivos;
- procedimentos e padrão de execução;
- prazo e custo estimado;
- matriz de isolamento atualizada;
- análises de risco;
- formulários de planejamento;
- articulação com operação para liberação do equipamento e retorno ao serviço;
- PT e registros associados;
- contratação externa quando necessária.

Na prática, a ordem é o instrumento de coordenação entre operação, manutenção, inspeção, fiscalização de contratos e apoio administrativo. Quanto mais incompleta a ordem, maior a chance de interrupção, atraso ou retorno sem conclusão. (Fontes: `regis-712143aa49549e5339b71436:pNone:5624.0-5926.0`, `regis-712143aa49549e5339b71436:pNone:5928.0-6528.0`)

## 8. Indicadores e realimentação dos planos

### 8.1 Indicadores citados no material
Os textos apontam a extração, a partir do sistema de gerenciamento da manutenção, de dados para análise como:

- **MTTR**;
- **MTBF**;
- **disponibilidade de equipamentos**;
- **custos** de manutenção preventiva, preditiva, corretiva e calibração;
- **quantidade de manutenção executada** no período.

Também se menciona emissão mensal de relatório de indicadores no processo de encerramento técnico. (Fontes: `regis-712143aa49549e5339b71436:pNone:5780.0-6189.0`, `regis-712143aa49549e5339b71436:pNone:5928.0-6528.0`)

### 8.2 Uso dos indicadores
Segundo o fluxo descrito, esses dados devem gerar saídas concretas para a engenharia/gestão da manutenção, como:

- recomendações de melhoria nos planos de manutenção;
- criação de novos planos;
- inclusão de itens em estoque;
- estudos e análises de FMEA;
- aplicação de MCC/RCM.

Portanto, o fechamento do ciclo não é apenas medir. É **usar o histórico para revisar plano, estoque e estratégia**. Isso é especialmente importante quando há backlog recorrente, reincidência de falhas ou baixa aderência entre programado e executado. (Fontes: `regis-712143aa49549e5339b71436:pNone:5780.0-6189.0`, `regis-712143aa49549e5339b71436:pNone:5928.0-6528.0`)

## 9. Planejamento da manutenção já na fase de projeto e implantação

Embora esta faceta foque a fase operacional, um dos trechos mostra que o planejamento e controle da manutenção começa antes da operação. Na fase de projeto detalhado e preparação operacional, o estudo destaca:

- atualização do modelo RAM;
- definição preliminar da carga de trabalho de manutenção;
- seleção do software de manutenção/CMMS;
- definição da estratégia de operação e manutenção;
- definição dos contratos de manutenção;
- definição dos requisitos de sobressalentes;
- definição dos requisitos para operações integradas.

Para novas unidades ou grandes modificações em FPSO, isso é relevante porque a futura qualidade do plano e da programação depende da qualidade dessas definições iniciais. (Fontes: `regis-74dd376119cbb653fe9922bc:pNone:5451.0-5740.0`)

## 10. Síntese aplicada à faceta “planejamento e controle”

Para elaborar e controlar planos e ordens de manutenção com boa priorização e tratamento de atrasos, o conjunto de fontes sustenta a seguinte lógica técnica:

1. **Cadastrar corretamente os ativos e planos** no CMMS/SAP.
2. **Estruturar planos com tarefas, periodicidades, recursos e critérios claros**.
3. **Emitir solicitações de forma disciplinada**, separando programadas de não programadas.
4. **Analisar criticidade, pertinência, custo e executante** antes de planejar.
5. **Planejar o serviço em detalhe**, incluindo materiais, ferramentas, pessoal, isolamentos, risco e documentação.
6. **Programar em conjunto com a operação**, priorizando a carteira e validando janelas executáveis.
7. **Emitir, distribuir, executar e testar** as ordens com registro técnico adequado.
8. **Encerrar corretamente no sistema**, preservando histórico e rastreabilidade.
9. **Monitorar backlog, aderência e indicadores de confiabilidade/manutenção**.
10. **Revisar planos, estoques e estratégias** a partir do histórico, FMEA/MCC/RCM e das falhas de execução observadas.

Essa sequência transforma o plano de manutenção em um sistema vivo de decisão, e não apenas em calendário de ordens. (Fontes: `regis-7493a0b7af9688fbb59924e0:pNone:1105.0-1326.0`, `regis-7493a0b7af9688fbb59924e0:pNone:4171.0-4401.0`, `regis-7493a0b7af9688fbb59924e0:pNone:4286.0-4549.0`, `regis-712143aa49549e5339b71436:pNone:5624.0-5926.0`, `regis-712143aa49549e5339b71436:pNone:5928.0-6528.0`, `regis-74dd376119cbb653fe9922bc:pNone:5451.0-5740.0`, `regis-0e3ade70c2795843d646ab84:pNone:197.0-238.0`)