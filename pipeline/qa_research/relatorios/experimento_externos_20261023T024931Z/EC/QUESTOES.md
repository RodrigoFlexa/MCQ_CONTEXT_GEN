# Questões geradas

## 01_01 · bloco 000 · Indicadores de monitoramento operacional: detecção de desvios e diagnóstico

Status: `ok`

Exemplos recebidos: mmmlu_ptbr:74 (), PQ-04_01-07 (dificil), PQ-02_10-05 (media), arc_challenge:Mercury_SC_408447 (), pira_ptbr:B1979 (), qasc:351SEKWQS0G5U8EVLNEO79TTRQAMDC (), PQ-07_01-03 (facil), pira_ptbr:B2347 (), mmmlu_ptbr:40 ()

**1. [facil · recordar]** Qual é a relação correta entre um KPI operacional e a variável de processo que ele acompanha?

Resposta: O KPI não substitui a variável de processo; ele resume seu efeito sobre o desempenho.

**2. [media · inferir]** Em um FPSO operando com especificações de produto mais restritas e maior exigência de segurança, por que ferramentas online de monitoramento passam a ter mais valor?

Resposta: Porque permitem avaliar as condições operacionais em tempo próximo do real.

**3. [media · inferir]** O óleo ainda atende à especificação, mas o KPI mostra deterioração contínua que sugere desvio futuro. Que objetivo do monitoramento está sendo usado ao investigar isso agora?

Resposta: Antecipar anormalidades.

**4. [dificil · decidir]** Em um FPSO, um KPI de tratamento se afasta da faixa usual logo após perturbação de alimentação e mudança de estratégia de controle feitas para manter o produto em especificação. Minutos depois, as variáveis principais estabilizam e o produto permanece conforme. Qual decisão diagnóstica é correta?

Resposta: Não classificar ainda como perda estrutural; o desvio deve ser interpretado com o contexto do processo e o histórico recente, pois pode ser transitório.

## 01_01 · bloco 001 · O que são KPIs e como a finalidade muda sua definição

Status: `ok`

Exemplos recebidos: qasc:340UGXU9DY0A1XJQLA5445GU6VSUVC (), mmmlu_ptbr:43 (), mmmlu_ptbr:3 (), arc_challenge:AKDE&ED_2012_8_14 (), pira_ptbr:A1126 (), PQ-04_02-03 (facil), pira_ptbr:B2550 (), PQ-09_01-04 (media), PQ-03_02-08 (dificil)

**1. [facil · recordar]** Qual é a função básica de um KPI em processos industriais?

Resposta: Avaliar a eficiência e o desempenho dos processos.

**2. [media · comparar]** No mesmo processo de um FPSO, a sala de controle acompanha a operação em tempo real e a gerência faz revisão mensal de desempenho. O indicador precisa ser o mesmo nas duas análises?

Resposta: Não. O mesmo processo pode usar indicadores diferentes, porque a forma de expressão depende da finalidade da avaliação e do usuário.

**3. [media · inferir]** Após um KPI revelar deficiência de desempenho, a equipe propõe um ajuste operacional para reduzir custos sem grande investimento e trata o ganho esperado como certo. Essa conclusão é tecnicamente válida?

Resposta: Não. O KPI apoia ações para reduzir custos ou elevar capacidade, mas não garante esses ganhos em qualquer condição operacional.

**4. [dificil · decidir]** Em um FPSO, o painel em tempo real mostra melhora de um KPI agregado da instalação após redistribuição de carga. A coordenação quer usar esse mesmo indicador para decidir uma ação de melhoria no sistema de compressão, visando recuperar capacidade sem grande investimento. Qual definição de KPI deve prevalecer para sustentar essa decisão?

Resposta: Deve prevalecer um KPI específico do sistema de compressão ou da etapa afetada, coerente com a decisão local; o agregado da instalação não é o mais adequado para essa escolha.

## 01_01 · bloco 002 · Denominador, base de exposição e comparabilidade

Status: `ok`

Exemplos recebidos: mmmlu_ptbr:42 (), qasc:36U2A8VAG1YD2V9JW7OM5HBQOSEKYC (), pira_ptbr:A732 (), PQ-09_02-09 (dificil), PQ-07_04-04 (media), PQ-08_03-02 (facil), arc_challenge:Mercury_7230545 (), pira_ptbr:A1621 (), mmmlu_ptbr:22 ()

**1. [facil · recordar]** Em um KPI, o que o denominador determina?

Resposta: Ele determina a base de comparação do indicador, ou seja, o que ele realmente compara.

**2. [media · comparar]** Em um FPSO, duas taxas mensais de frequência de acidentes usam a mesma base de horas-homem, mas no segundo mês o critério de enquadramento dos casos foi ampliado. A comparação direta continua consistente?

Resposta: Não. A comparação fica comprometida porque mudou a definição dos casos que entram no numerador.

**3. [media · decidir]** Em um FPSO, o consumo total de energia subiu após aumento do volume processado. Para verificar se houve piora do desempenho energético intrínseco, que forma de indicador deve ser usada?

Resposta: Um indicador intensivo, como consumo de energia por unidade produzida.

**4. [dificil · decidir]** Em dois meses consecutivos de um FPSO, os acidentes com afastamento caíram de 6 para 4. No mesmo intervalo, as horas-homem de exposição ao risco caíram de 200 mil para 80 mil. O critério de enquadramento permaneceu igual. Concluir melhora do desempenho de segurança só pela contagem bruta está correto?

Resposta: Não. A taxa de frequência por horas-homem aumentou, então a queda no número absoluto de casos não indica melhora real.

## 01_01 · bloco 004 · Dependabilidade e seus atributos centrais

Status: `ok`

Exemplos recebidos: mmmlu_ptbr:91 (), pira_ptbr:A251 (), PQ-10_01-02 (facil), PQ-03_02-08 (dificil), PQ-09_02-06 (media), mmmlu_ptbr:74 (), arc_challenge:Mercury_7247975 (), pira_ptbr:A593 (), qasc:3PH3VY7DJLW42LD5H7987ZENDA6WZK ()

**1. [facil · recordar]** Que atributo expressa a chance de restaurar um sistema defeituoso em tempo especificado?

Resposta: Mantenabilidade.

**2. [media · decidir]** Para avaliar se um sistema que começou operando continuará prestando o serviço correto nas próximas 12 horas, sob condições definidas, qual atributo é o adequado?

Resposta: Confiabilidade.

**3. [media · inferir]** Em um FPSO, a lógica de proteção retira um equipamento de serviço ao detectar condição perigosa e evita dano maior. Qual efeito isso pode ter sobre a continuidade operacional?

Resposta: Pode reduzi-la, porque o sistema sai de serviço para preservar segurança e integridade.

**4. [dificil · decidir]** Dois compressores de um FPSO tiveram o mesmo número de falhas no mês. Em ambos, o reparo ativo levou 2 horas, mas no A houve espera logística e, após o retorno, ele operou temporariamente com restrições; no B, o retorno foi imediato e em condição aceitável. Para explicar por que o A perdeu mais produção, o que deve ser priorizado na análise?

Resposta: Deve-se priorizar o tempo e as condições de retorno à operação aceitável; no A, a indisponibilidade logística e o retorno restrito pesam mais que a frequência de falhas.  
_usa apoio_

## 01_01 · bloco 005 · Disponibilidade: o que é e por que depende de falha e reparo

Status: `ok`

Exemplos recebidos: qasc:3Z2R0DQ0JHDKFAO2706OYIXGQXA2EF (), pira_ptbr:A1258 (), PQ-04_01-06 (media), PQ-07_01-03 (facil), PQ-05_01-07 (dificil), arc_challenge:Mercury_SC_408447 (), pira_ptbr:B2224 (), mmmlu_ptbr:48 (), mmmlu_ptbr:51 ()

**1. [facil · recordar]** Em estado estacionário, qual razão pode representar a disponibilidade?

Resposta: Uptime dividido pelo tempo total observado.

**2. [media · inferir]** Dois relatórios usam critérios diferentes para contar indisponibilidades do mesmo sistema. Sem mudança real no equipamento, o que passa a explicar parte da diferença entre os valores de disponibilidade?

Resposta: O escopo do indicador, porque cada relatório inclui downtimes diferentes.

**3. [media · diagnosticar]** Dois compressores falham com a mesma frequência e exigem o mesmo tempo de reparo ativo. Mesmo assim, um deles tem menor disponibilidade operacional. Que diferença explica esse resultado?

Resposta: Tempos logísticos e administrativos maiores em cada falha.

**4. [dificil · diagnosticar]** Sem histórico confiável de uptime e downtime, a equipe estimou a disponibilidade por MTBF e MTTR. Em uma bomba, o MTTR usado cobre só a intervenção ativa, embora cada falha também inclua diagnóstico, mobilização, espera por sobressalente, acesso e liberação antes do retorno seguro. Que viés isso introduz no KPI?

Resposta: O KPI superestima a disponibilidade operacional, porque esse MTTR exclui parte da indisponibilidade da falha.

## 01_01 · bloco 006 · Redundância, standby e efeitos sobre o comportamento do sistema

Status: `ok`

Exemplos recebidos: mmmlu_ptbr:3 (), mmmlu_ptbr:66 (), arc_challenge:AKDE&ED_2012_8_14 (), pira_ptbr:A1539 (), PQ-03_01-01 (facil), pira_ptbr:A1070 (), qasc:3VA45EW49NMZ2GJVIA96YBHPWRYO1A (), PQ-06_01-04 (media), PQ-07_04-07 (dificil)

**1. [facil · recordar]** Em compressão, geração e tratamento em FPSO, o que caracteriza uma redundância útil?

Resposta: Preservar a função de processo relevante, não apenas duplicar equipamento.

**2. [media · diagnosticar]** Num arranjo com reserva fria em um FPSO, o equipamento reserva não trabalha sob a mesma carga do ativo. Se ele permanece íntegro em espera, mas a função não retorna quando é solicitado, qual falha explica a perda do serviço?

Resposta: Falha de partida ou de comutação do equipamento reserva.

**3. [media · inferir]** Em um FPSO, dois geradores redundantes podem ser bloqueados pela mesma lógica automática de proteção. Se esse bloqueio atuar, qual efeito a redundância terá sobre a indisponibilidade desse evento?

Resposta: Nenhum; uma lógica de intertravamento comum continua tornando os dois indisponíveis.

**4. [dificil · diagnosticar]** Em um FPSO, um compressor opera continuamente e o reserva fica em reserva fria. No início da campanha, a redundância elevou a disponibilidade. Após longo período, o ativo degradou e, numa troca por falha, o reserva não partiu, sem ocorrências de utilidades compartilhadas, manutenção ou intertravamentos comuns. Que limitação do arranjo explica a perda do ganho esperado?

Resposta: O ganho da redundância se limita em missões longas: a degradação do ativo pode deixar de ser compensada, e o equipamento reserva ainda pode falhar ao assumir a função.

## 01_01 · bloco 007 · Como selecionar, modelar e atualizar análises RAM

Status: `ok`

Exemplos recebidos: mmmlu_ptbr:112 (), PQ-04_02-04 (media), qasc:3KB8R4ZV1E6CN1KPWOPNZELWULQBGW (), PQ-10_01-02 (facil), pira_ptbr:B2268 (), pira_ptbr:A1863 (), PQ-05_02-07 (dificil), mmmlu_ptbr:2 (), arc_challenge:Mercury_7268013 ()

**1. [facil · recordar]** Além de confiabilidade, disponibilidade e manutenibilidade, que dimensão o RAMS acrescenta à análise?

Resposta: Segurança.

**2. [media · decidir]** Na fase preliminar de projeto de um FPSO, a equipe quer validar arranjo, quantidade de equipamentos e alternativas de redundância. Que nível de modelagem RAM é adequado nessa etapa?

Resposta: Modelos mais simples, suficientes para essa validação preliminar.

**3. [media · inferir]** Após o detalhamento do sistema, a equipe manteve um modelo RAM preliminar e quer priorizar melhorias comparando modos operacionais. Que limitação esse modelo tende a ter?

Resposta: Tende a não identificar adequadamente os maiores contribuintes de falha nem a refinar as previsões de disponibilidade e confiabilidade.

**4. [dificil · decidir]** Para um FPSO, a equipe tem duas análises RAM para decidir uma modificação. Uma é muito detalhada, mas usa tempos de reparo e frequências de falha de outra unidade; a outra representa corretamente a lógica funcional e o regime operacional locais, com menor sofisticação. Qual análise merece maior confiança?

Resposta: A que representa a lógica funcional e o regime operacional locais com dados aderentes à unidade; sofisticação isolada com parâmetros externos não garante precisão.

## 01_01 · bloco 008 · Coleta de dados, indicadores e monitoramento do desempenho real

Status: `ok`

Exemplos recebidos: pira_ptbr:A1196 (), arc_challenge:AIMS_2009_8_9 (), mmmlu_ptbr:53 (), PQ-06_03-01 (facil), PQ-04_01-06 (media), pira_ptbr:A658 (), qasc:333U7HK6I9EFT08AIQ1WRH1CPUIJD6 (), mmmlu_ptbr:43 (), PQ-03_02-08 (dificil)

**1. [facil · recordar]** Qual indicador de reparo é calculado com o início da falha e o retorno à operação?

Resposta: MTTR.

**2. [media · inferir]** Em um FPSO, as ordens de manutenção registram várias paradas sob uma categoria genérica, sem distinguir mecanismos de falha. Qual consequência isso traz para priorizar ações corretivas?

Resposta: As causas deixam de ser distinguíveis, reduzindo a utilidade dos dados para priorizar ações corretivas.

**3. [media · inferir]** Para representar o desempenho local de um FPSO, a equipe usa só dados do OREDA e ignora os registros da própria unidade. Qual limitação principal surge?

Resposta: A avaliação pode não representar as condições locais da unidade, porque o banco setorial não substitui dados próprios.

**4. [dificil · decidir]** No painel de KPI de um FPSO, um skid auxiliar falha várias vezes no mês, mas sem perda de produção porque há redundância. Já uma válvula da linha de exportação falha uma vez e interrompe a exportação por horas. Se o acompanhamento usa apenas médias de falha por item, qual elemento deve ser priorizado como limitante do desempenho real?

Resposta: A válvula da linha de exportação, porque sua indisponibilidade bloqueia a exportação e sua criticidade funcional supera a maior frequência de falhas do skid redundante.

## 01_01 · bloco 010 · Interações com segurança, manutenção e recursos de suporte

Status: `ok`

Exemplos recebidos: qasc:3I7DHKZYGNZ4KL7LKUSSE7LSLO85FO (), PQ-06_01-04 (media), arc_challenge:Mercury_SC_LBS10039 (), mmmlu_ptbr:148 (), mmmlu_ptbr:40 (), pira_ptbr:A489 (), pira_ptbr:B2460 (), PQ-05_01-02 (facil), PQ-03_02-08 (dificil)

**1. [facil · recordar]** Que finalidade operacional justifica a parada por função de proteção?

Resposta: Evitar estados perigosos, danos ambientais e consequências maiores.

**2. [media · inferir]** Um FPSO ampliou a equipe de manutenção, mas o retorno ao serviço continua atrasado porque os reparos aguardam sobressalente, liberação e logística. Qual efeito essa ampliação tende a ter na disponibilidade?

Resposta: Tende a gerar ganho limitado, porque o gargalo do retorno operacional não está na capacidade das equipes.

**3. [media · decidir]** Para elevar o KPI de disponibilidade, a gerência propõe diminuir preventivas sem qualquer avaliação prévia. Essa decisão é tecnicamente suportada?

Resposta: Não; reduzir intervenções preventivas exige avaliar risco e integridade antes.

**4. [dificil · decidir]** Num FPSO, três falhas simultâneas disputam a única equipe especializada. Duas exigem a mesma liberação de área, disponível por apenas 1 hora: uma recoloca a produção em 40 minutos; outra recupera uma função secundária em 3 horas. A terceira não compartilha essa restrição, mas não remove a limitação principal. Qual prioridade técnica deve vir primeiro?

Resposta: A intervenção funcionalmente crítica que cabe na janela de liberação comum, porque combina maior criticidade, menor recuperação e a restrição compartilhada.

## 01_01 · bloco 011 · Como o processamento primário condiciona a capacidade da unidade

Status: `ok`

Exemplos recebidos: pira_ptbr:A349 (), PQ-04_01-07 (dificil), PQ-07_05-02 (facil), qasc:3WS1NTTKEYB5PELKNOMGXCP10ZPF03 (), mmmlu_ptbr:82 (), mmmlu_ptbr:134 (), PQ-03_03-04 (media), arc_challenge:Mercury_7142713 (), pira_ptbr:A905 ()

**1. [facil · recordar]** Qual é a função do processamento primário nas facilidades de produção marítimas?

Resposta: Separar e tratar óleo, gás e água sob condições controladas.

**2. [media · inferir]** Os fluidos chegam misturados e com impurezas. Mesmo com a separação estável, a movimentação dos fluxos virou o limitante. O que explica a perda de capacidade da unidade?

Resposta: Porque a capacidade produtiva depende da capacidade combinada de separação, tratamento e movimentação; se a movimentação limita, a unidade perde capacidade.

**3. [media · decidir]** Um tratador passou a operar abaixo da eficiência esperada e a qualidade das correntes separadas caiu. Para manter especificações e estabilidade operacional, que ajuste pode ser necessário?

Resposta: Reduzir a produção.

**4. [dificil · diagnosticar]** Após aumento do corte de água, um separador passou a operar abaixo da eficiência esperada. A qualidade da fase aquosa piorou, a reinjeção disponível está saturada e o tratamento para descarte no mar já opera no limite aceitável; compressão de gás e exportação de óleo permanecem normais. Qual mecanismo explica a necessidade de reduzir a vazão total do campo?

Resposta: A perda de eficiência do separador agravou o gargalo da malha de água produzida; sem capacidade de tratar, reinjetar ou descartar a fase aquosa com qualidade aceitável, a vazão total precisa cair.

## 01_01 · bloco 012 · Seleção e aplicação de medidas para prevenir ou aliviar gargalos

Status: `ok`

Exemplos recebidos: arc_challenge:MEA_2010_8_20-v1 (), PQ-07_01-03 (facil), mmmlu_ptbr:84 (), pira_ptbr:A1439 (), qasc:3B3WTRP3DB13KEXLZPQ264W5XZ992N (), pira_ptbr:A365 (), PQ-05_01-07 (dificil), PQ-03_03-04 (media), mmmlu_ptbr:102 ()

**1. [facil · recordar]** Quando uma medida corretiva se aplica a uma restrição de produção?

Resposta: Quando a restrição já compromete a capacidade.

**2. [media · decidir]** Em um novo campo offshore com alto risco de incrustação e gerenciamento difícil, a meta é reduzir custos com perdas de produção. Deve-se priorizar prevenção ou correção?

Resposta: Prevenção, incorporada à estratégia de desenvolvimento offshore.

**3. [media · decidir]** Em um gargalo de processo, a limitação foi identificada como condição operacional, não como equipamento. Que tipo de mudança o debottlenecking deve priorizar?

Resposta: Uma mudança de condição operacional que alivie precisamente essa restrição.

**4. [dificil · diagnosticar]** Um FPSO ampliou a capacidade de um equipamento para aliviar uma restrição, mas a vazão total não aumentou; a limitação só mudou de lugar na planta. Não houve alteração de fluido nem falha nova. Que diagnóstico esse padrão sustenta?

Resposta: Que o debottlenecking não localizou a variável ou o equipamento realmente limitante; a ação apenas deslocou o gargalo para outro ponto.

## 01_01 · bloco 013 · Consequências operacionais e econômicas das restrições em FPSO

Status: `ok`

Exemplos recebidos: arc_challenge:AKDE&ED_2012_8_42 (), mmmlu_ptbr:51 (), PQ-04_01-06 (media), PQ-09_02-09 (dificil), pira_ptbr:A260 (), qasc:3A4TN5196KH9X276UU30VY3FSDCCHR (), pira_ptbr:B2513 (), PQ-10_01-01 (facil), mmmlu_ptbr:71 ()

**1. [facil · recordar]** Quando a restrição está em um ponto comum do sistema do FPSO, qual decisão gerencial se torna inevitável?

Resposta: Priorizar entregas e alocar a capacidade disponível.

**2. [media · comparar]** Dois FPSOs têm a mesma demanda de produção. Um deles foi concebido considerando localização, meio ambiente, ancoragem, casco, convés e arranjo de produção e armazenagem para reduzir impactos operacionais. O que se espera dessa unidade entre operações de offloading?

Resposta: Maior capacidade de minimizar paradas e problemas entre offloadings.

**3. [media · comparar]** Duas interdições decorrem da mesma falha operacional. Uma unidade produz mais e fica indisponível por mais tempo que a outra. Em qual delas a perda econômica tende a ser maior?

Resposta: Na unidade com maior volume produzido e maior duração da indisponibilidade.

**4. [dificil · decidir]** Num FPSO de campo maduro, a produção total começa a cair mesmo com folga no processamento de hidrocarbonetos. O limite passou a ser a rota de tratamento e descarte da água produzida, enquanto a outra rota de manejo dessa fase ainda tem capacidade. Como a restrição está em um ponto comum do sistema, qual decisão operacional é mais consistente para reduzir a perda de produção?

Resposta: Redirecionar parte da água produzida para reinjeção, realocando a capacidade disponível.  
_usa apoio_

## 01_01 · bloco 015 · Atribuição de causas: do mecanismo físico à perda observada

Status: `ok`

Exemplos recebidos: mmmlu_ptbr:91 (), pira_ptbr:B2326 (), PQ-03_03-04 (media), PQ-07_05-02 (facil), pira_ptbr:A1340 (), mmmlu_ptbr:60 (), PQ-04_02-09 (dificil), arc_challenge:MSA_2013_5_33 (), qasc:3R0T90IZ1SBVX6CVAOLIAYREEH4GCA ()

**1. [facil · recordar]** Qual é a função do inibidor de incrustação?

Resposta: Prevenir ou retardar nova precipitação de incrustação.

**2. [media · inferir]** Se a incrustação na coluna de produção restringe a passagem do fluido, o que tende a acontecer com a resistência ao fluxo, a pressão observada no poço e a vazão bruta?

Resposta: A resistência ao fluxo aumenta, a pressão observada no poço tende a se alterar e a vazão bruta cai.

**3. [media · decidir]** Uma obstrução por incrustação já formada na coluna passou a limitar a capacidade. Para recuperar produção, que intervenção pode se tornar necessária?

Resposta: Remoção do depósito e avaliação da integridade do equipamento.

**4. [dificil · diagnosticar]** Em um FPSO, um relatório de perdas encerra o caso como queda de vazão do poço após alteração de pressão. Nenhuma ação específica no sistema foi definida porque o registro ficou no efeito observado. Para que a atribuição da perda seja útil à operação, o que ainda precisa ser determinado?

Resposta: O mecanismo que limita a capacidade, o ativo afetado e as condições em que esse mecanismo se tornou dominante; a queda de vazão é só o efeito observado.

## 01_01 · bloco 016 · Condições que mudam o comportamento do risco no processamento primário

Status: `parcial` · O bloco [F] sustenta 3 questões fortes, mas não traz critérios de priorização, limites ou combinações operacionais suficientes para formular uma questão difícil inequívoca sem recorrer a conhecimento externo ou a um cenário artificial.

Exemplos recebidos: arc_challenge:Mercury_407675 (), PQ-06_05-01 (facil), PQ-04_01-07 (dificil), qasc:3AMW0RGHOD1K1N2L2XKJKIZID83PNU (), PQ-07_05-06 (media), pira_ptbr:A1725 (), pira_ptbr:A1021 (), mmmlu_ptbr:50 (), mmmlu_ptbr:102 ()

**1. [facil · recordar]** Qual condição de monitoramento eleva o risco de processo no processamento primário?

Resposta: Ausência de medições essenciais ou medições pouco confiáveis.

**2. [media · inferir]** Durante operação estável, a separação óleo-água perde eficiência. Qual é a consequência esperada para a detecção e correção de desvios?

Resposta: A observabilidade do processo e a margem para detectar e corrigir desvios diminuem, elevando o risco.

**3. [media · comparar]** Duas unidades têm a mesma designação. Na X, instrumentação, capacidade de segregação, inventário intermediário e flexibilidade operacional são maiores que na Y. Mantida a mesma perturbação, qual tende a postergar mais a redução de carga ou a parada?

Resposta: A X, porque esses recursos determinam quanto a unidade absorve a perturbação antes de reduzir carga ou parar.

## 01_01 · bloco 017 · Estrutura organizacional, gestão de mudanças e autonomia técnica

Status: `ok`

Exemplos recebidos: PQ-08_03-02 (facil), mmmlu_ptbr:101 (), arc_challenge:Mercury_7126683 (), qasc:3DY46V3X3PHCIOEWEIFJSVUFXGE55Y (), pira_ptbr:A1310 (), PQ-07_04-07 (dificil), PQ-04_01-06 (media), pira_ptbr:B2393 (), mmmlu_ptbr:77 ()

**1. [facil · recordar]** Além das técnicas de análise, que capacidade organizacional sustenta a gestão de riscos ao longo da vida útil da instalação?

Resposta: Uma estrutura organizacional capaz de sustentar identificação de perigos, análise, atualização documental, gestão de mudanças e esclarecimento rápido de parâmetros de projeto e operação.

**2. [media · inferir]** Durante um desvio operacional, a equipe depende de suporte remoto, não acessa a documentação atualizada e não sabe quem detém a responsabilidade técnica. Que efeito isso tende a produzir sobre a resposta e a validação de mudanças?

Resposta: Aumenta o tempo de resposta, atrasa decisões e dificulta validar mudanças diante do desvio.

**3. [media · comparar]** Dois períodos operacionais têm o mesmo risco técnico inicial. Em um, há comunicação contínua entre áreas; no outro, ela se rompe e fatores culturais inibem o reporte de desvios enquanto as condições mudam rapidamente. O que tende a diferir no sistema de gestão?

Resposta: No segundo, a robustez e a resiliência do sistema de gestão tendem a ser menores.

**4. [dificil · decidir]** Durante um transitório de processo, a equipe identifica um ajuste temporário que pode estabilizar a operação sem parar a planta. As barreiras técnicas estão disponíveis, mas a bordo faltam as premissas de projeto atualizadas, o suporte remoto não responde no tempo requerido e ninguém tem responsabilidade técnica claramente definida para autorizar a mudança. O que deve ser priorizado para viabilizar um controle efetivo?

Resposta: Priorizar responsabilidade técnica clara a bordo, com acesso à documentação atualizada para revisar premissas e validar a mudança.

## 01_01 · bloco 018 · Monitoramento, revisão e aprendizagem para próximas intervenções

Status: `ok`

Exemplos recebidos: arc_challenge:Mercury_SC_408759 (), mmmlu_ptbr:60 (), PQ-10_01-07 (dificil), pira_ptbr:A1751 (), pira_ptbr:A666 (), PQ-02_10-05 (media), PQ-04_02-03 (facil), qasc:3H0W84IWBK11JU5NMQLPZQ5O0H3REE (), mmmlu_ptbr:121 ()

**1. [facil · recordar]** Que documento de uma parada reúne prazos planejados e realizados, linha crítica, custos, acidentes, desvios e lições aprendidas?

Resposta: O relatório final da parada.

**2. [media · decidir]** Uma parada anterior mostrou, no registro pós-intervenção, que a complexidade foi subestimada e que suporte extra acabou sendo necessário. Para a próxima intervenção semelhante, que aspecto do preparo deve ser reforçado?

Resposta: A preparação de contingências, com base no suporte efetivamente necessário e no risco.

**3. [media · decidir]** Em várias paradas do mesmo sistema, o histórico mostra acréscimo recorrente de escopo no mesmo pacote e recursos de suporte maiores que o previsto. Além de explicar custos passados, que decisão sobre esse pacote esse histórico pode embasar?

Resposta: A revisão da estratégia de manutenção desse pacote.

**4. [dificil · diagnosticar]** A unidade mantém monitoramento sistemático de risco e emite relatórios ao fim de cada parada. Mesmo assim, duas intervenções semelhantes repetem atraso na linha crítica, aumento de escopo e falta de suporte; as lições foram copiadas entre relatórios, sem verificar se ainda valiam. Qual falha de gestão explica melhor a repetição?

Resposta: Preenchimento formal sem análise crítica real do histórico, impedindo que o aprendizado retroalimente o planejamento.

## 01_01 · bloco 019 · Seleção de sistemas críticos e uso de histórico de falhas

Status: `ok`

Exemplos recebidos: PQ-07_04-04 (media), qasc:3ON104KXQKVOZOPGWEJID31EEEQ4W3 (), pira_ptbr:B2376 (), mmmlu_ptbr:66 (), arc_challenge:MDSA_2007_8_47 (), PQ-09_01-02 (facil), mmmlu_ptbr:1 (), pira_ptbr:A839 (), PQ-02_10-07 (dificil)

**1. [facil · recordar]** Para que serve identificar componentes e sistemas críticos em um FPSO?

Resposta: Para orientar a implantação e a atualização dos controles de risco, priorizando as funções que merecem tratamento.

**2. [media · inferir]** Na revisão de risco, eventos anteriores mostram repetidamente desvios em separação de fluidos e medição. Como isso deve influenciar a seleção de sistemas críticos?

Resposta: Essas funções devem ser tratadas como sensíveis, servindo para formular hipóteses de falha e revisar cenários na priorização dos controles.

**3. [media · decidir]** Uma equipe quer priorizar sistemas críticos de um FPSO usando apenas a frequência de acidentes de outra unidade, sem avaliar configuração, regime operacional e barreiras locais. Essa abordagem é válida?

Resposta: Não. Dados históricos não formam ranking universal; a priorização deve considerar as funções e vulnerabilidades da instalação real.

**4. [dificil · decidir]** No histórico da frota, medição concentrou mais eventos que separação. No FPSO em análise, porém, a função de separação opera com barreira degradada e manutenção atrasada, enquanto a medição mantém desempenho previsto. Na atualização dos controles de risco, qual função deve receber prioridade na seleção de sistemas críticos?

Resposta: A separação, porque a seleção deve refletir a vulnerabilidade real da unidade; o histórico apenas informa a análise.  
_usa apoio_

## 01_01 · bloco 021 · Confiabilidade, disponibilidade e suporte de manutenção

Status: `ok`

Exemplos recebidos: arc_challenge:Mercury_7142713 (), PQ-03_01-01 (facil), mmmlu_ptbr:48 (), PQ-06_01-04 (media), PQ-07_04-07 (dificil), qasc:3KYQYYSHYV6TUBZ7Y3T1ZDIY26YODE (), pira_ptbr:A357 (), pira_ptbr:A1278 (), mmmlu_ptbr:37 ()

**1. [facil · recordar]** O que a confiabilidade de um item mede ao longo do tempo?

Resposta: A capacidade de cumprir a função requerida, sob condições especificadas, durante um intervalo de tempo.

**2. [media · inferir]** Uma unidade sofre paradas não programadas recorrentes e decisões frágeis sobre risco e custo. Que efeito se espera da engenharia de confiabilidade sobre esse quadro?

Resposta: Reduzir paradas não programadas e melhorar a base para decisões sobre risco, custo e desempenho operacional.

**3. [media · comparar]** Dois equipamentos têm a mesma confiabilidade e a mesma mantenabilidade. Em um deles, sobressalentes e mobilização externa não estão assegurados. Qual tende a ter menor disponibilidade quando requisitado?

Resposta: O que não tem sobressalentes e mobilização externa assegurados, porque sua disponibilidade depende do suporte de manutenção e dos recursos externos.

**4. [dificil · decidir]** Um equipamento crítico de FPSO opera degradado, mas sua probabilidade histórica de falha é baixa. Não há sobressalente a bordo, a mobilização depende de janela logística e o especialista só chega dias depois. Na decisão entre intervir agora ou adiar, qual aspecto deve orientar a escolha?

Resposta: O tempo e os meios para restaurar a função, porque a disponibilidade fica limitada pelo suporte de manutenção e pelos recursos externos.

## 01_01 · bloco 022 · Consequências econômicas de controles insuficientes

Status: `ok`

Exemplos recebidos: mmmlu_ptbr:18 (), PQ-04_01-07 (dificil), pira_ptbr:A1229 (), PQ-07_05-06 (media), arc_challenge:NCEOGA_2013_5_25 (), PQ-09_01-02 (facil), pira_ptbr:A345 (), qasc:3T111IHZ5EPKOYE6EF537C4D8OX9R3 (), mmmlu_ptbr:144 ()

**1. [facil · recordar]** Que efeito operacional pode resultar de falhas em autodiagnóstico, ações contingenciais e medidas corretivas compatíveis com o risco?

Resposta: Interdição da instalação.

**2. [media · comparar]** Duas FPSOs enfrentam a mesma parada forçada, com igual duração e mesmo escopo corretivo. Se uma delas produz mais por dia, como fica sua perda potencial de receita?

Resposta: Tende a ser maior, porque a receita diária comprometida durante a parada forçada é mais alta.

**3. [media · decidir]** Um gestor compara a intervenção preventiva apenas com o custo imediato do reparo após a falha. Esse recorte é economicamente suficiente para decidir o controle de risco?

Resposta: Não. A análise deve incluir o efeito acumulado da indisponibilidade, das correções emergenciais e das restrições operacionais.

**4. [dificil · decidir]** Uma análise econômica em uma FPSO indicou que adiar um controle de risco foi aceitável porque o reparo posterior seria simples. O gerente quer repetir essa decisão em outra unidade, onde a mesma falha pode causar parada mais longa, mobilização extraordinária e restrições operacionais, sob contrato diferente. Essa transferência direta é válida?

Resposta: Não. O caso anterior não é universal; a outra unidade exige avaliação própria do efeito acumulado da indisponibilidade, do escopo corretivo e do contexto contratual.

## 01_01 · bloco 023 · Análise de causa: mecanismo de falha, modo de falha e FMEA

Status: `ok`

Exemplos recebidos: PQ-10_01-02 (facil), mmmlu_ptbr:19 (), mmmlu_ptbr:29 (), qasc:3QAVNHZ3EM3NQJTY11M7HV6Y8OIAL5 (), arc_challenge:MCAS_2004_9_15 (), PQ-03_01-05 (media), pira_ptbr:A1639 (), pira_ptbr:B1980 (), PQ-05_02-07 (dificil)

**1. [facil · recordar]** Na análise de falhas, qual é a função técnica da FMEA?

Resposta: Estruturar a avaliação dos modos de falha e de seus efeitos, causas e controles.

**2. [media · comparar]** Em um trocador do FPSO, ataque químico progressivo reduz a espessura até surgir vazamento. Na análise de falhas, como se classificam o ataque químico e o vazamento?

Resposta: O ataque químico é o mecanismo de falha; o vazamento é o modo de falha.

**3. [media · diagnosticar]** Em um FPSO, a FMEA de um sistema foi elaborada só pela manutenção, embora incluísse efeitos, causas e controles operacionais. Que requisito do método ficou sem atendimento?

Resposta: A condução por equipe multidisciplinar.

**4. [dificil · decidir]** Na priorização de ações da FMEA de um FPSO, duas falhas receberam o mesmo NPR. Uma pode gerar consequência crítica, embora tenha baixa ocorrência; a outra é mais frequente e mais fácil de detectar, mas causa apenas perda operacional limitada. Se só uma puder ser tratada primeiro, qual deve ser priorizada?

Resposta: A que pode gerar consequência crítica, porque o NPR só apoia a triagem e não substitui a análise individual.

## 02_02 · bloco 000 · Como selecionar e aplicar: bottle test como triagem empírica

Status: `ok`

Exemplos recebidos: mmmlu_ptbr:102 (), PQ-04_02-04 (media), PQ-07_04-07 (dificil), pira_ptbr:A1658 (), mmmlu_ptbr:84 (), qasc:3VBEN272MKYB4N1R7ABIP3VW36GGS5 (), PQ-05_01-02 (facil), pira_ptbr:B2040 (), arc_challenge:MEA_2014_5_13 ()

**1. [facil · recordar]** Qual amostra serve de referência para avaliar a separação natural no bottle test?

Resposta: A amostra sem aditivo.

**2. [media · comparar]** Dois frascos receberam o mesmo desemulsificante e a mesma dosagem, mas um foi submetido a mistura mais intensa. A diferença observada pode ser usada como comparação válida do tratamento?

Resposta: Não. O bottle test exige condições controladas; mistura, temperatura, concentração do produto e tempo de observação precisam ser comparáveis.

**3. [media · decidir]** Um produto foi o melhor na bancada, porém o ensaio não representou bem o fluido nem as condições relevantes do processo. Antes de adotá-lo no FPSO, o que deve ser feito?

Resposta: Validação operacional, porque cisalhamento, residência e composição real podem alterar o desempenho visto em bancada.

**4. [dificil · diagnosticar]** Uma equipe avaliou um produto para uma emulsão óleo-em-água. No bottle test, escolheu o candidato que mais aumentou a liberação de água do petróleo e ignorou o comportamento da fase aquosa. Qual foi o erro técnico na seleção?

Resposta: Usou o critério de água-em-óleo; em emulsão óleo-em-água, o indicador relevante é a clarificação da fase aquosa.

## 02_02 · bloco 003 · Por que pH, salmoura, petróleo e asfaltenos mudam o desempenho

Status: `ok`

Exemplos recebidos: pira_ptbr:A1483 (), PQ-07_04-07 (dificil), arc_challenge:Mercury_7043995 (), pira_ptbr:A406 (), PQ-01_01-03 (facil), qasc:3IHR8NYAM70YFFSFKS5NL9TIN4D4PA (), PQ-06_01-04 (media), mmmlu_ptbr:41 (), mmmlu_ptbr:79 ()

**1. [facil · recordar]** Que componentes podem formar filmes resistentes ao redor das gotas e dificultar a coalescência?

Resposta: Asfaltenos e sólidos.

**2. [media · inferir]** Uma emulsão segue estável por causa de um filme interfacial resistente. Se o aditivo desorganiza esse filme, qual mecanismo de separação passa a ser favorecido quando as gotas se tocam?

Resposta: A drenagem do filme líquido entre as gotas, favorecendo a coalescência.

**3. [media · diagnosticar]** Dois testes usam o mesmo clarificante e o mesmo petróleo, mas pequenas mudanças apenas no pH e na salinidade alteram o resultado. Que propriedades interfaciais provavelmente foram modificadas?

Resposta: Carga elétrica, solvatação e adsorção de espécies na interface.

**4. [dificil · decidir]** Após mudar o blend de produção, a emulsão passou a separar mal. As análises mostram mais asfaltenos e sólidos, e uma tentativa de aumentar a salinidade não trouxe melhora. Sem outras anomalias de processo, qual decisão técnica deve ter prioridade antes de novos ajustes de pH ou salinidade?

Resposta: Reavaliar e comparar os produtos nas condições representativas do novo sistema, porque filmes de asfaltenos e sólidos podem exigir outra formulação e maior salinidade não garante melhor separação.

## 02_02 · bloco 006 · Como o antiespumante atua na quebra da espuma

Status: `ok`

Exemplos recebidos: PQ-04_01-07 (dificil), arc_challenge:Mercury_SC_400696 (), mmmlu_ptbr:44 (), PQ-06_03-01 (facil), PQ-09_01-04 (media), pira_ptbr:A1591 (), pira_ptbr:A950 (), qasc:3ND9UOO81K1KXWW126IZZK3P06SWL7 (), mmmlu_ptbr:75 ()

**1. [facil · recordar]** Para romper a espuma, que região da bolha o antiespumante precisa alcançar?

Resposta: O filme que estabiliza a bolha, para favorecer sua ruptura ou drenagem.

**2. [media · inferir]** No mesmo separador, elevar a concentração do antiespumante melhora a quebra da espuma até certa faixa; acima disso, o desempenho deixa de crescer. O que isso indica sobre a relação dose-resposta?

Resposta: Que ela não é universal; acima de uma faixa útil, mais concentração não garante melhor desempenho.

**3. [media · comparar]** Duas formulações antiespumantes são aplicadas no mesmo fluido e na mesma dose, mas uma controla melhor a espuma. Mantidas as demais condições, o que explica essa diferença?

Resposta: Diferenças de formulação alteram o espalhamento, a penetração e a dispersão do produto na interface gás-líquido.

**4. [dificil · diagnosticar]** Após mudança na composição do fluido de entrada, mantendo o mesmo separador, a mesma formulação e as demais condições de processo, a espuma passou a persistir. Aumentos sucessivos na concentração deram ganho inicial, mas doses maiores não trouxeram melhora adicional. Qual diagnóstico explica o comportamento?

Resposta: A mudança de composição alterou a estabilidade da espuma e dificultou o contato efetivo do antiespumante com a interface; não é apenas falta de dose.

## 02_02 · bloco 009 · Interações e efeitos colaterais relevantes no processamento

Status: `ok`

Exemplos recebidos: pira_ptbr:B2096 (), PQ-01_01-03 (facil), PQ-05_02-07 (dificil), arc_challenge:Mercury_7170433 (), mmmlu_ptbr:67 (), PQ-07_05-06 (media), mmmlu_ptbr:37 (), qasc:3U4J9857OEATU89O3LLTT183THRB79 (), pira_ptbr:A286 ()

**1. [facil · recordar]** Qual efeito a melhora da quebra de espuma tende a ter na saída de gás de um separador?

Resposta: Redução do arraste de líquido na saída de gás.

**2. [media · inferir]** Um antiespumante controla a espuma no primeiro vaso, mas sua formulação inclui fase oleosa e emulsificantes. Mantidas as demais condições do trem de processo, que efeito colateral precisa ser avaliado nos equipamentos seguintes?

Resposta: Possível alteração do comportamento das interfaces em outros equipamentos.

**3. [media · diagnosticar]** Em um separador, a mesma formulação apresenta desempenho irregular. Se a dose não mudou e não houve mudança do fluido, que tipo de falha de aplicação explica essa resposta inconsistente?

Resposta: Mistura insuficiente ou falha em fazer o produto alcançar a interface crítica.

**4. [dificil · decidir]** Num FPSO, um antiespumante reduziu o arraste de líquido no gás no início da produção. Meses depois, a espuma reaparece e o arraste volta, embora vazão de injeção, equipamento e arranjo de aplicação permaneçam inalterados. No mesmo período aumentaram corte de água, sólidos produzidos e salinidade. Entre manter o programa químico como está e revê-lo, qual decisão é correta?

Resposta: Rever o programa químico e reavaliar o antiespumante, porque a mudança do fluido deslocou o equilíbrio entre formação e quebra de espuma.

## 02_02 · bloco 012 · Por que esses químicos funcionam na água produzida

Status: `ok`

Exemplos recebidos: PQ-09_01-02 (facil), pira_ptbr:A1424 (), arc_challenge:Mercury_7142695 (), mmmlu_ptbr:22 (), mmmlu_ptbr:126 (), PQ-05_02-07 (dificil), pira_ptbr:B2571 (), PQ-08_02-04 (media), qasc:31LM9EDVOLROFCZN7KFZNMD65HEJNM ()

**1. [facil · recordar]** Antes de considerar equivalentes um coagulante natural e um sintético, o que deve ser comprovado?

Resposta: A equivalência de desempenho na água produzida de interesse.

**2. [media · inferir]** Uma água produzida mantém gotas finas dispersas principalmente por repulsão elétrica. Que ação do coagulante tende a aumentar a aproximação entre gotas e sólidos?

Resposta: Neutralização de cargas e/ou compressão da dupla camada elétrica, aproximando gotas e sólidos.

**3. [media · inferir]** Após o condicionamento químico, a corrente segue para flotação por ar dissolvido. Se os agregados ficam maiores e as interfaces menos estáveis, que efeito se espera na remoção do óleo?

Resposta: A captura por microbolhas tende a ficar mais fácil, acelerando a subida da fase oleosa.

**4. [dificil · diagnosticar]** Em uma unidade com flotação por ar dissolvido, a geração de microbolhas está normal. A dosagem de coagulante já reduziu a repulsão elétrica, mas os agregados observados seguem pequenos e se rompem na circulação, mantendo baixa remoção de óleo. Qual função química está faltando no condicionamento?

Resposta: Falta a ação de ponte de um floculante polimérico, para gerar flocos maiores e mais resistentes, mais capturáveis por microbolhas.

## 02_02 · bloco 015 · Consequências e interações relevantes para o descarte

Status: `ok`

Exemplos recebidos: PQ-07_05-06 (media), pira_ptbr:A750 (), pira_ptbr:A894 (), PQ-03_02-08 (dificil), qasc:3OJSZ2ATDSVR5SSF2BUGQF8BQBO75A (), mmmlu_ptbr:3 (), mmmlu_ptbr:79 (), PQ-09_01-02 (facil), arc_challenge:NYSEDREGENTS_2009_8_7 ()

**1. [facil · recordar]** Que propriedade das gotas pode ser alterada por resíduos de químicos de produção?

Resposta: A molhabilidade das gotas.

**2. [media · inferir]** Em um FPSO, o corte de água aumentou e parte da produção passou a vir de outros poços, sem mudança no equipamento. O que isso implica para a dosagem ótima do tratamento da água produzida?

Resposta: Ela pode mudar; o desempenho do tratamento deve ser reavaliado e a dosagem redeterminada.

**3. [media · inferir]** Após ajustar coagulante e floculante, a remoção de óleo continuou adequada, mas subiram os sólidos suspensos do efluente e o lodo passou a desaguar pior. Que conclusão isso impõe sobre a avaliação do programa químico?

Resposta: Ela não pode se limitar ao óleo removido; o programa também está afetando o perfil do efluente e o desaguamento do lodo.

**4. [dificil · diagnosticar]** Um FPSO trocou o desemulsificante da produção. Dias depois, a água produzida tratada passou a sair com mais óleo e a flotação perdeu estabilidade, embora a configuração do equipamento e o regime de escoamento não tenham mudado. Ensaios indicam maior consumo de coagulante e menor captura das gotas pelas bolhas. Qual diagnóstico explica melhor o quadro?

Resposta: Há interferência do novo químico de produção no tratamento da água produzida, consumindo coagulante e prejudicando a aderência das gotas às bolhas.

## 02_02 · bloco 018 · Papel dos inibidores de incrustação e limites de aplicação em sistemas com URS

Status: `ok`

Exemplos recebidos: PQ-03_01-05 (media), pira_ptbr:A1258 (), PQ-04_02-03 (facil), qasc:3P59JYT76LJM4T6ZXVVJX4XHPQHT2E (), mmmlu_ptbr:152 (), pira_ptbr:A934 (), PQ-05_01-07 (dificil), mmmlu_ptbr:18 (), arc_challenge:Mercury_7282118 ()

**1. [facil · recordar]** Se cristais de incrustação já estão presentes, que efeito o inibidor ainda pode exercer sobre eles?

Resposta: Pode provocar distorção e dispersão dos cristais.

**2. [media · inferir]** Uma FPSO usa URS para reduzir sulfato na água de injeção, mas persiste tendência de depósito por carbonato de cálcio na planta de processo. Nesse quadro, qual papel cabe ao anti-incrustante?

Resposta: Compensar uma incrustação que a remoção de sulfato não resolve, protegendo a planta de processo.

**3. [media · inferir]** O mesmo anti-incrustante vinha performando bem, mas a água passou a operar com outro pH e recebeu um quelante. Sem mudar a meta de controle, o que deve ser reavaliado no produto?

Resposta: Sua eficiência no sistema, porque ela depende do pH e da presença de quelantes.

**4. [dificil · decidir]** Uma FPSO opera com URS. A saída mais carregada da unidade passou a ter risco local de depósito, enquanto a equipe tenta proteger os poços produtores aumentando a dosagem apenas na água de injeção. Qual aplicação do anti-incrustante deve ser priorizada?

Resposta: A proteção dos pontos da URS onde as espécies incrustantes se concentram; dosar só a água de injeção não assegura proteção aos produtores, porque o produto pode adsorver na rocha junto ao injetor.

## 02_02 · bloco 021 · Sequestrante químico: bissulfito de sódio, mecanismo e limitações

Status: `ok`

Exemplos recebidos: PQ-05_01-07 (dificil), arc_challenge:Mercury_7027038 (), mmmlu_ptbr:144 (), pira_ptbr:A1189 (), PQ-07_01-03 (facil), mmmlu_ptbr:68 (), qasc:3HL8HNGX450NL89XNK59QNQU4L99F0 (), pira_ptbr:A943 (), PQ-01_01-05 (media)

**1. [facil · recordar]** Qual é a função do bissulfito de sódio no condicionamento da água?

Resposta: Reagir quimicamente com o oxigênio dissolvido para removê-lo.

**2. [media · inferir]** Se o teor de oxigênio dissolvido da água aumenta e a dosagem de bissulfito permanece inalterada, qual tendência operacional deve ser esperada?

Resposta: A demanda química cresce; a dosagem pode ficar insuficiente e deixar oxigênio residual no sistema.

**3. [media · inferir]** Após substituir o produto por uma solução mais diluída de bissulfito, um circuito passa a exigir verificação extra de materiais, sem mudança de serviço. Qual aspecto justifica essa checagem?

Resposta: O baixo pH da solução diluída pode torná-la corrosiva para muitos materiais.

**4. [dificil · diagnosticar]** Em uma unidade de água de injeção, o teor de oxigênio na água de entrada e a vazão da bomba dosadora permaneceram estáveis. Mesmo assim, a remoção piorou logo após começar o uso de uma solução preparada dias antes e mantida em tanque parcialmente cheio e ventilado. Qual diagnóstico melhor explica o desvio?

Resposta: A solução perdeu concentração ativa no armazenamento com contato com ar, e a mesma vazão volumétrica deixou de atender à demanda estequiométrica.

## 02_02 · bloco 024 · Condições que mudam o comportamento: cloro residual, CO2 e disponibilidade de gás

Status: `ok`

Exemplos recebidos: mmmlu_ptbr:66 (), PQ-04_01-07 (dificil), pira_ptbr:A1727 (), qasc:38F71OA9GTV2SSSRCT9EV9WE9NLMFS (), PQ-05_01-06 (media), mmmlu_ptbr:31 (), pira_ptbr:A1022 (), PQ-10_01-02 (facil), arc_challenge:Mercury_180163 ()

**1. [facil · recordar]** Qual rota de desoxigenação é alternativa quando o gás de arraste está indisponível ou inadequado?

Resposta: A desaeração a vácuo.

**2. [media · decidir]** Na seleção da desoxigenação por stripping a gás em um FPSO, há gás disponível, mas sua composição é variável e a corrente gasosa de saída não tem destino seguro definido. Qual decisão técnica decorre disso?

Resposta: A rota por stripping a gás não deve ser escolhida sem confirmar disponibilidade, composição adequada e destino seguro da corrente gasosa.

**3. [media · decidir]** A remoção exigida de oxigênio não é atendida com folga por uma única rota, e o projeto continua limitado por espaço, peso e utilidades. Que arranjo de processo pode ser adotado?

Resposta: Sistemas combinados de desoxigenação, ajustados ao balanço de remoção e às restrições do projeto.

**4. [dificil · diagnosticar]** Após iniciar desaeração a vácuo em água do mar, aumenta a tendência de depósito carbonático e o bissulfito passa a render menos na remoção de oxigênio dissolvido. Análises mostram cloro residual elevado na alimentação. Qual combinação de mecanismos explica esses dois efeitos?

Resposta: O cloro residual compete com o oxigênio e consome parte do bissulfito; ao mesmo tempo, a remoção de CO2 no vácuo pode favorecer a precipitação de carbonato de cálcio.

## 02_02 · bloco 027 · Função do controle microbiológico na água de injeção

Status: `ok`

Exemplos recebidos: PQ-09_02-09 (dificil), mmmlu_ptbr:37 (), qasc:3E337GFOL97EOA9MZEUWQ9LQFP0GNK (), pira_ptbr:B2393 (), mmmlu_ptbr:178 (), arc_challenge:Mercury_7172795 (), pira_ptbr:B2040 (), PQ-03_01-05 (media), PQ-10_01-02 (facil)

**1. [facil · recordar]** Qual é a função do controle microbiológico na água de injeção?

Resposta: Limitar a contaminação, o crescimento e a atividade de microrganismos que favorecem biofilme, souring e corrosão microbiologicamente influenciada.

**2. [media · diagnosticar]** Em água de injeção com sulfato disponível, começa a surgir sulfeto e há ataque em componentes de ferro e aço. Que grupo microbiano se torna especialmente relevante nesse quadro?

Resposta: As bactérias redutoras de sulfato, porque reduzem sulfato a sulfeto e estão associadas à biocorrosão.

**3. [media · inferir]** No circuito de água de injeção, por que avaliar só microrganismos na fase aquosa pode subestimar o problema operacional?

Resposta: Porque o problema também inclui microrganismos aderidos às superfícies internas de linhas, tanques, filtros, tubulações e poços.

**4. [dificil · diagnosticar]** Num FPSO, o biocida do programa é aplicado e as amostras da fase aquosa melhoram, mas a contaminação retorna sempre no mesmo trecho da água de injeção. Inspeção mostra incrustação interna e regiões de baixo escoamento. Qual mecanismo explica melhor a recorrência?

Resposta: Persistência de microrganismos aderidos em biofilme, protegidos por depósitos e pelo baixo escoamento, o que reduz o alcance efetivo do biocida.

## 02_02 · bloco 029 · Por que biofilme, incrustação e depósitos reduzem a eficácia

Status: `ok`

Exemplos recebidos: PQ-07_04-07 (dificil), arc_challenge:MSA_2012_5_14 (), pira_ptbr:A1285 (), mmmlu_ptbr:144 (), qasc:3VA45EW49NMZ2GJVIA96YBHPDTA1OK (), mmmlu_ptbr:74 (), PQ-03_01-05 (media), PQ-01_01-02 (facil), pira_ptbr:B2325 ()

**1. [facil · recordar]** Além da concentração, qual parâmetro do tratamento também afeta o desempenho químico contra microrganismos?

Resposta: O tempo de contato.

**2. [media · inferir]** Em um sistema de água de injeção, um biocida teve bom resultado contra células planctônicas em teste, mas a colonização no equipamento ocorre como biofilme aderido. Sem mudar o produto, que comportamento é mais esperado no campo?

Resposta: Desempenho insuficiente contra o biofilme, porque ele dificulta o contato e a penetração do produto.

**3. [media · comparar]** Dois trechos de uma linha de água de injeção têm a mesma água, o mesmo material e a mesma vazão. O trecho B possui superfície interna mais rugosa. Em qual trecho a formação de biofilme tende a ser maior?

Resposta: No trecho B, porque a rugosidade da superfície favorece a formação de biofilme em escoamento.

**4. [dificil · diagnosticar]** Em um sistema de água de injeção sob tratamento prolongado, a amostragem do fluido mostra baixa contagem de bactérias livres. Na inspeção de um trecho rugoso aparecem depósitos aderidos, biofilme recoberto por incrustação mineral e ataque localizado. Qual interpretação técnica do caso é mais consistente?

Resposta: Há regiões inacessíveis sob depósitos, onde o biocida não penetra adequadamente; o ataque não deve ser atribuído diretamente às bactérias sem avaliar também depósitos, química da água e suscetibilidade do material.

## 02_02 · bloco 032 · Como a inibição funciona e quais limites mecanísticos importam

Status: `ok`

Exemplos recebidos: qasc:3Z9WI9EOZZNRG0JUM7KYJHGNAJXKHV (), pira_ptbr:A143 (), mmmlu_ptbr:152 (), pira_ptbr:A251 (), arc_challenge:Mercury_7033863 (), PQ-05_02-07 (dificil), PQ-10_01-02 (facil), PQ-08_02-04 (media), mmmlu_ptbr:18 ()

**1. [facil · recordar]** Que tipo de inibidor é o MEG na prevenção de hidratos?

Resposta: Um inibidor termodinâmico.

**2. [media · inferir]** Mantidas a pressão e a composição do gás, a concentração de MEG foi elevada ao valor adequado. O que acontece com a temperatura em que o sistema passa a atingir a condição de hidrato?

Resposta: Ela diminui; o sistema pode operar a temperaturas mais baixas antes de alcançar o equilíbrio de hidrato.

**3. [media · diagnosticar]** A vazão nominal de injeção de MEG permaneceu igual, mas a água produzida aumentou e houve mistura insuficiente em parte da linha. Qual falha de proteção deve ser esperada nesse trecho?

Resposta: Queda da concentração efetiva de MEG na água livre, deixando regiões da linha sem proteção contra hidratos.

**4. [dificil · decidir]** Durante uma campanha no FPSO, um escoamento subsea completou um resfriamento gradual sem indícios de hidrato. Na condição seguinte, a pressão e a composição do gás permanecem iguais, mas a temperatura prevista será mais baixa e a água produzida aumentou, enquanto a vazão nominal de MEG continua na meta. Para decidir se a operação segue protegida, em que critério técnico a decisão deve se basear?

Resposta: Na margem ao equilíbrio de hidrato calculada pela concentração efetiva de MEG na água livre; o histórico sem nucleação não substitui essa verificação.

## 02_02 · bloco 035 · Seleção, monitoramento e alternativas de regeneração

Status: `ok`

Exemplos recebidos: qasc:3OS4RQUCR9E691OUL4J5HTLKSLABFA (), mmmlu_ptbr:201 (), pira_ptbr:A1082 (), PQ-01_01-02 (facil), PQ-07_05-06 (media), arc_challenge:ACTAAP_2007_7_24 (), mmmlu_ptbr:48 (), pira_ptbr:A380 (), PQ-04_02-09 (dificil)

**1. [facil · recordar]** Qual parâmetro de composição o monitoramento do programa de MEG acompanha na fase aquosa?

Resposta: A concentração de glicol na fase aquosa.

**2. [media · inferir]** Após a regeneração remover água e devolver ao MEG a concentração requerida para reúso, o teor de sais ainda ameaça a recuperação. Qual conclusão técnica se aplica?

Resposta: A necessidade de remoção de sais deve ser avaliada separadamente; remover água para regenerar o MEG não resolve isso por si só.

**3. [media · inferir]** Em uma unidade de regeneração de MEG, a carga de processamento aumenta e as condições de temperatura e pressão mudam. Que dois aspectos devem ser reavaliados porque essa mudança os afeta diretamente?

Resposta: A separação e o consumo de energia.

**4. [dificil · decidir]** Uma alternativa de regeneração apresentou bom desempenho e baixo consumo em teste de laboratório com mistura simplificada. No FPSO, o circuito real contém sais, sólidos e hidrocarbonetos e opera com variações de temperatura, pressão e carga. Antes da seleção, qual decisão técnica é correta?

Resposta: Validá-la no circuito real; o desempenho observado na mistura simplificada não deve ser extrapolado ao arranjo industrial.

## 02_02 · bloco 038 · Função dos químicos no tratamento do gás

Status: `ok`

Exemplos recebidos: PQ-03_03-04 (media), pira_ptbr:A727 (), qasc:3G5F9DBFOPW5WBD6LBY5LQR498FHVQ (), mmmlu_ptbr:74 (), mmmlu_ptbr:54 (), PQ-04_02-03 (facil), pira_ptbr:A1551 (), arc_challenge:MDSA_2007_5_9 (), PQ-07_04-07 (dificil)

**1. [facil · recordar]** Que função tem o sequestrante de H2S no tratamento do gás?

Resposta: Consumir ou imobilizar a espécie sulfídrica.

**2. [media · inferir]** Em um trecho do tratamento de gás há fase aquosa e aumento da taxa de ataque ao aço, sem risco dominante de hidrato, espuma ou gases ácidos. Qual serviço químico deve ser priorizado nesse trecho?

Resposta: Inibidor de corrosão de gás, para reduzir a velocidade de ataque ao material metálico.

**3. [media · inferir]** O gás precisa reduzir CO2 em um subsistema de adoçamento, e o risco dominante não é hidrato, espuma nem corrosão por fase aquosa. Que classe de produto atende esse objetivo?

Resposta: Solvente de absorção, como alcanolamina.

**4. [dificil · decidir]** Em um FPSO, o mesmo sistema de tratamento de gás inclui um trecho frio com risco de hidrato, um vaso com tendência à espuma e outro trecho onde a fase aquosa acelera o ataque ao aço. A equipe propõe usar um único químico em uma única corrente e no mesmo ponto de injeção para simplificar a operação. Qual decisão técnica é correta?

Resposta: Rejeitar a simplificação: os químicos devem ser selecionados pela ameaça dominante em cada trecho e não necessariamente na mesma corrente, concentração ou ponto de injeção.

## 02_02 · bloco 041 · Compatibilidade química: por que a combinação pode melhorar ou piorar a proteção

Status: `ok`

Exemplos recebidos: PQ-10_01-07 (dificil), mmmlu_ptbr:95 (), pira_ptbr:A1617 (), qasc:3UJ1CZ6IZHODOQC7QESRL647MJV5SM (), mmmlu_ptbr:44 (), arc_challenge:Mercury_SC_415079 (), PQ-09_02-06 (media), PQ-07_01-03 (facil), pira_ptbr:A1081 ()

**1. [facil · recordar]** Que aspecto impede prever o efeito de dois químicos apenas pela função declarada de cada um?

Resposta: As interações entre os produtos no meio de serviço.

**2. [media · inferir]** Num circuito de gás úmido do FPSO, a mistura de dois químicos gera precipitação e perde a estabilidade do filme protetor. Qual tendência esperar para a proteção anticorrosiva?

Resposta: Tendência de redução da proteção anticorrosiva.

**3. [media · decidir]** Um teste de compatibilidade usa as dosagens corretas, mas cupom de material e fluido diferentes do sistema real do FPSO. Ele basta para validar a mistura no serviço?

Resposta: Não; materiais e fluido também precisam ser representativos do serviço.

**4. [dificil · diagnosticar]** Em um FPSO, escolheu-se combinar um inibidor de corrosão com um sequestrante de H2S porque cada um atendia sua própria função. A mistura foi aprovada em laboratório apenas em solução com NaCl, mas falha no serviço com água produzida multissalina e materiais específicos. Qual falha de avaliação explica esse falso sinal de compatibilidade?

Resposta: O ensaio foi não representativo do serviço: inferiu compatibilidade pela função e usou só NaCl, que não reproduz a água produzida multissalina.

## 02_02 · bloco 044 · Alternativas ao squeeze para controle de incrustação

Status: `ok`

Exemplos recebidos: mmmlu_ptbr:97 (), PQ-08_02-04 (media), PQ-05_01-02 (facil), pira_ptbr:B2047 (), PQ-04_02-09 (dificil), mmmlu_ptbr:90 (), arc_challenge:Mercury_406916 (), pira_ptbr:A1032 (), qasc:3B4YI393V9VEUSAI2A5ZEHEZNKNSSG ()

**1. [facil · recordar]** Como a URS faz a remoção seletiva de sulfato?

Resposta: Por membranas adequadas ao serviço.

**2. [media · inferir]** Num sistema com água de injeção sulfatada e potencial de BaSO4 e SrSO4, a URS entra em operação. Que efeito se espera sobre a tendência de precipitação desses sais?

Resposta: Ela diminui e pode até ser eliminada, pela redução do sulfato na água injetada.

**3. [media · comparar]** Duas estratégias mantêm a mesma meta de controlar incrustação ao longo da vida do campo: instalar URS ou seguir com inibição. Com diferenças de investimento inicial, operação, manutenção e impacto de paradas, em que comparação a escolha deve se basear?

Resposta: Em estudo de viabilidade técnico-econômica, comparando investimento inicial e custos de operação e manutenção com custos recorrentes de inibição e perdas por parada de produção.

**4. [dificil · decidir]** Em um campo com risco de incrustação por sulfato, uma tecnologia de transporte e retenção de inibidor no reservatório projeta custo menor que a URS. Porém, ainda não comprovou distribuição do inibidor, sua liberação nem compatibilidade. Na priorização da decisão, o menor custo basta para colocá-la no mesmo nível da remoção de sulfato, ou é necessária outra condição antes disso?

Resposta: Não; antes, é necessária a validação de distribuição, liberação e compatibilidade.

## 02_02 · bloco 047 · Segregação e compatibilidade entre produtos químicos

Status: `ok`

Exemplos recebidos: arc_challenge:ACTAAP_2010_7_1 (), PQ-05_01-07 (dificil), pira_ptbr:A1620 (), PQ-08_02-04 (media), pira_ptbr:B2402 (), qasc:3EKVH9QMEY3FN4A2B5V4S0FVP3OD2B (), PQ-04_02-03 (facil), mmmlu_ptbr:48 (), mmmlu_ptbr:3 ()

**1. [facil · recordar]** Qual é a função da segregação entre produtos químicos em uma instalação offshore?

Resposta: Impedir contato não intencional entre incompatíveis e evitar perda de desempenho por reação paralela.

**2. [media · decidir]** Um produto passará a usar a mesma linha de injeção de outro, sem troca de mangueira ou dreno entre campanhas. O que deve ser verificado antes de autorizar a sequência?

Resposta: A compatibilidade entre os químicos, inclusive com a mistura residual na linha, na mangueira ou no recipiente.

**3. [media · inferir]** Após drenagem, um recipiente com resíduo de alvejante clorado recebe limpador ácido. Qual perigo imediato essa sequência cria?

Resposta: Pode gerar uma nuvem gasosa tóxica.

**4. [dificil · diagnosticar]** Depois de uma alteração temporária nas transferências químicas, a demanda de bissulfito aumentou e o tratamento de água passou a apresentar falhas intermitentes difíceis de confirmar. Bombas, analisadores e qualidade da água de entrada foram verificados. No mesmo período, a mesma linha passou a alternar oxidante e redutor, com retorno de mangueira ao tanque e sem flushing validado. Qual causa deve ser priorizada na investigação?

Resposta: Falha de segregação com contaminação cruzada entre oxidante e redutor, consumindo reagente antes da função principal.

## 02_02 · bloco 050 · Monitoramento do armazenamento e consequências operacionais

Status: `ok`

Exemplos recebidos: PQ-07_05-02 (facil), mmmlu_ptbr:24 (), mmmlu_ptbr:64 (), qasc:3MX2NQ3YC9TLK7Y6KOYEKELZO5E5XC (), pira_ptbr:B2479 (), pira_ptbr:A249 (), arc_challenge:Mercury_7145495 (), PQ-03_01-05 (media), PQ-09_02-09 (dificil)

**1. [facil · recordar]** Além do nível do tanque, que condições o monitoramento do armazenamento e manuseio deve verificar?

Resposta: Condições que antecedem falhas de segurança, corrosão ou perda de desempenho.

**2. [media · decidir]** Há água produzida acumulada e existe possibilidade de atividade microbiológica. Que facilidades passam a ser relevantes nesse armazenamento/manuseio?

Resposta: Facilidades para monitorar H2S e para aplicar biocidas.

**3. [media · decidir]** Em um sistema de injeção sujeito à corrosão e com regime dinâmico, que técnicas foram consideradas adequadas para acompanhar variações de corrosividade?

Resposta: Par galvânico e resistência à polarização.

**4. [dificil · diagnosticar]** Em um FPSO com oscilações usuais de vazão, pressão e composição, surge instabilidade a jusante: espuma inesperada e queda da eficiência de separação. A dosagem comandada e o consumo medido de um químico permanecem coerentes, não houve mistura com outros produtos, e o conteúdo do tanque de serviço mudou de cor após estocagem. Qual diagnóstico deve ser priorizado?

Resposta: Degradação do produto armazenado, pois a alteração de cor e a perda de resposta com dosagem coerente apontam para isso.

## 02_02 · bloco 053 · Seleção do ponto de medição, automação e confiabilidade dos dados

Status: `ok`

Exemplos recebidos: pira_ptbr:A1196 (), PQ-04_02-09 (dificil), mmmlu_ptbr:73 (), pira_ptbr:A1854 (), mmmlu_ptbr:134 (), arc_challenge:Mercury_SC_408415 (), qasc:3U4J9857OEATU89O3LLTT183VOT7BN (), PQ-01_01-02 (facil), PQ-09_01-04 (media)

**1. [facil · recordar]** Mesmo com controle automático de químico, o que continua necessário para confiar na medição?

Resposta: Validação periódica da medição, com manutenção do sensor e reconciliação com análises laboratoriais.

**2. [media · inferir]** Em uma malha automática, a condição do processo muda rápido, mas o sensor responde devagar e mede após o tempo de mistura. Que consequência isso traz ao ajuste da dosagem?

Resposta: A malha passa a seguir a condição passada do processo e pode não capturar os transientes.

**3. [media · comparar]** Mantidos o mesmo indicador e o mesmo processo, em qual caso a lógica de controle deve ser mais conservadora contra falso negativo: ativo pouco crítico ou ativo crítico?

Resposta: No ativo crítico, porque a consequência do falso negativo pesa mais na seleção do indicador e da lógica de controle.

**4. [dificil · decidir]** Em um FPSO, a dosagem automática usa um sensor on-line instalado em trecho com segregação de fases. O sinal fica estável, mas análises laboratoriais coletadas a jusante do misturador mostram oscilações relevantes; o sensor ainda opera sob vibração elevada e recebe pouca manutenção por acesso difícil. Antes de aumentar a dosagem, o que deve ser priorizado?

Resposta: Priorizar a validação da medição on-line e a revisão do ponto de instalação; o dado atual pode não representar a condição real e estar metrologicamente degradado.

## 02_02 · bloco 056 · Leitura temporal, pH e resposta corrosiva

Status: `ok`

Exemplos recebidos: arc_challenge:Mercury_402569 (), qasc:3KB8R4ZV1E6CN1KPWOPNZELWW6TBG7 (), mmmlu_ptbr:74 (), PQ-01_01-02 (facil), PQ-06_01-04 (media), pira_ptbr:A1743 (), pira_ptbr:A143 (), PQ-03_02-08 (dificil), mmmlu_ptbr:127 ()

**1. [facil · recordar]** Que instrumento permite acompanhar a perda metálica ao longo do tempo e compará-la com registros de pH?

Resposta: Sonda de resistência elétrica.

**2. [media · inferir]** Em um meio aquoso do FPSO suscetível à corrosão ácida, o pH cai durante a operação. Que tendência de mudança na perda metálica é esperada?

Resposta: Tendência de aumento da taxa de perda metálica.

**3. [media · diagnosticar]** Durante um transiente, a curva de perda de espessura não acompanha instantaneamente as oscilações de pH. Qual característica do dano metálico explica essa defasagem?

Resposta: O dano metálico é cumulativo.

**4. [dificil · decidir]** Em dois circuitos aquosos do FPSO, a leitura temporal mostrou correlação entre corrosão e pH no circuito A. A equipe quer usar no circuito B o mesmo critério de ajuste baseado nessa correlação, embora ele tenha metalurgia, composição do fluido e regime de escoamento diferentes. Qual decisão técnica é correta?

Resposta: Validar a correlação no circuito B antes de usá-la; a resposta corrosiva ao pH depende dessas condições e não é universal.
