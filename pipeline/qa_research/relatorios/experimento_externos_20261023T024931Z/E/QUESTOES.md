# Questões geradas

## 01_01 · bloco 000 · Indicadores de monitoramento operacional: detecção de desvios e diagnóstico

Status: `ok`

Exemplos recebidos: pira_ptbr:B1979 (), qasc:351SEKWQS0G5U8EVLNEO79TTRQAMDC (), arc_challenge:Mercury_SC_408447 (), pira_ptbr:B2347 (), mmmlu_ptbr:40 (), mmmlu_ptbr:74 ()

**1. [facil · recordar]** O que um indicador operacional resume nas unidades de processo?

Resposta: O efeito da variável de processo sobre o desempenho.

**2. [media · inferir]** Em um FPSO operando com especificações mais restritas e maior exigência de segurança, por que ferramentas online de indicadores ganham valor operacional?

Resposta: Porque permitem avaliar condições operacionais em tempo próximo do real.

**3. [media · decidir]** Os produtos do FPSO seguem dentro da especificação, mas a equipe usa um KPI para orientar ajustes finos e melhorar o desempenho da planta. Qual objetivo do monitoramento está sendo aplicado?

Resposta: Fornecer referência para otimização.

**4. [dificil · diagnosticar]** Após uma oscilação na alimentação, o KPI global de topsides cai em um FPSO. Separação, tratamento de óleo e utilidades ajustam suas respostas pela malha de controle, e o valor retorna quando o regime estabiliza. A equipe quer atribuir o evento diretamente ao separador. Qual diagnóstico deve prevalecer?

Resposta: O KPI indicou um sintoma transitório; antes de atribuir causa ao separador, é preciso localizar as variáveis perturbadas no contexto do processo e do histórico recente.

## 01_01 · bloco 001 · O que são KPIs e como a finalidade muda sua definição

Status: `ok`

Exemplos recebidos: pira_ptbr:B2550 (), mmmlu_ptbr:43 (), mmmlu_ptbr:3 (), pira_ptbr:A1126 (), qasc:340UGXU9DY0A1XJQLA5445GU6VSUVC (), arc_challenge:AKDE&ED_2012_8_14 ()

**1. [facil · recordar]** Que fator pode levar um mesmo processo a ser acompanhado por KPIs diferentes?

Resposta: A mudança da finalidade da avaliação e do usuário do indicador.

**2. [media · decidir]** Em um FPSO, a diretoria quer acompanhar o desempenho agregado da unidade, sem detalhar por equipamento ou etapa de processo. Em que escopo o KPI deve ser aplicado?

Resposta: Na instalação como um todo.

**3. [media · inferir]** Depois de implantar KPIs, a gestão concluiu que o FPSO reduzirá custos ou elevará capacidade automaticamente em qualquer condição operacional. Essa conclusão procede?

Resposta: Não. KPIs apoiam a identificação de deficiências e ações de melhoria, mas não garantem esses ganhos em qualquer condição operacional.

**4. [dificil · decidir]** Em um FPSO, um KPI de consumo de energia vinha sendo usado pela engenharia para análise de melhoria. A operação quer exibi-lo no painel em tempo real da sala de controle para decidir ajustes imediatos. Mantê-lo sem revisão é adequado?

Resposta: Não. O KPI deve ser redefinido ou substituído para a operação em tempo real, porque a métrica precisa ser coerente com a decisão que vai sustentar.

## 01_01 · bloco 002 · Denominador, base de exposição e comparabilidade

Status: `ok`

Exemplos recebidos: arc_challenge:Mercury_7230545 (), qasc:36U2A8VAG1YD2V9JW7OM5HBQOSEKYC (), mmmlu_ptbr:22 (), pira_ptbr:A732 (), mmmlu_ptbr:42 (), pira_ptbr:A1621 ()

**1. [facil · recordar]** O que o denominador determina em um indicador de desempenho?

Resposta: Ele define o que o indicador realmente compara.

**2. [media · inferir]** Em um FPSO, dois meses tiveram o mesmo número bruto de acidentes sem afastamento, mas horas-homem expostas diferentes. Qual medida compara o desempenho de segurança de forma mais consistente?

Resposta: A taxa de frequência de acidentes normalizada por horas-homem, com critério de enquadramento compatível.

**3. [media · decidir]** Em um mês, um FPSO entregou mais produção e consumiu mais energia. Para verificar se o desempenho energético intrínseco mudou, que base deve compor o indicador?

Resposta: Consumo de energia por unidade produzida.

**4. [dificil · decidir]** Um FPSO reduziu a taxa de acidentes sem afastamento entre dois trimestres. No segundo, passaram a entrar no denominador todas as horas-homem de contratadas embarcadas, mas o numerador continuou contando só casos do quadro próprio, pelo mesmo critério. Essa queda permite concluir melhora real do desempenho de segurança?

Resposta: Não. Numerador e base de exposição ficaram incompatíveis, diluindo a taxa; ela deixou de ser comparável como evidência de melhora real.

## 01_01 · bloco 004 · Dependabilidade e seus atributos centrais

Status: `ok`

Exemplos recebidos: qasc:3PH3VY7DJLW42LD5H7987ZENDA6WZK (), mmmlu_ptbr:91 (), arc_challenge:Mercury_7247975 (), pira_ptbr:A593 (), pira_ptbr:A251 (), mmmlu_ptbr:74 ()

**1. [facil · recordar]** Qual atributo da dependabilidade expressa a probabilidade de o sistema estar operacional em um dado instante?

Resposta: Disponibilidade.

**2. [media · inferir]** Se um sistema inicia a janela de avaliação já fora de serviço, qual atributo da dependabilidade não pode ser aplicado diretamente para medir a continuidade correta ao longo do intervalo?

Resposta: Confiabilidade, porque sua definição assume operação no início do período.

**3. [media · inferir]** Em um FPSO, a lógica de proteção retira um equipamento de serviço ao detectar condição severa, mesmo sem dano ao ativo. Qual efeito imediato isso tende a ter no serviço do sistema?

Resposta: Reduzir ou interromper a continuidade operacional do serviço, preservando segurança e integridade.

**4. [dificil · decidir]** Em um FPSO, um compressor quase não sofre falhas destrutivas, mas a produção cai porque a proteção o retira de serviço em condições anormais e a volta exige longa preparação e checagem antes do retorno seguro. Sem desabilitar a proteção, qual aspecto da dependabilidade deve ser priorizado para recuperar o desempenho global?

Resposta: Mantenabilidade; o limitador principal é o tempo e as condições de restauração após os desligamentos seguros.

## 01_01 · bloco 005 · Disponibilidade: o que é e por que depende de falha e reparo

Status: `ok`

Exemplos recebidos: mmmlu_ptbr:51 (), mmmlu_ptbr:48 (), arc_challenge:Mercury_SC_408447 (), qasc:3Z2R0DQ0JHDKFAO2706OYIXGQXA2EF (), pira_ptbr:B2224 (), pira_ptbr:A1258 ()

**1. [facil · recordar]** Em estado estacionário, que razão pode representar a disponibilidade?

Resposta: Uptime dividido pelo tempo total observado.

**2. [media · comparar]** Duas áreas calculam a disponibilidade do mesmo sistema com critérios de parada diferentes. A comparação direta dos valores é válida?

Resposta: Não; os indicadores usam escopos diferentes de indisponibilidade.

**3. [media · inferir]** Sem registros confiáveis de uptime e downtime, um sistema reparável é avaliado por MTBF e MTTR médios. Se o MTTR aumenta e o MTBF fica constante, qual tendência da disponibilidade aproximada?

Resposta: Tende a diminuir.

**4. [dificil · diagnosticar]** Em um FPSO, a disponibilidade operacional de uma bomba crítica caiu no trimestre. A frequência de falhas e o tempo de intervenção em campo ficaram iguais aos do período anterior, mas aumentaram espera por sobressalente, mobilização de equipe, liberação de acesso e retorno seguro à operação. Qual causa do KPI deve ser priorizada no diagnóstico?

Resposta: O aumento dos tempos logísticos e administrativos do downtime; o reparo ativo não explica a queda.

## 01_01 · bloco 006 · Redundância, standby e efeitos sobre o comportamento do sistema

Status: `ok`

Exemplos recebidos: mmmlu_ptbr:3 (), pira_ptbr:A1539 (), qasc:3VA45EW49NMZ2GJVIA96YBHPWRYO1A (), mmmlu_ptbr:66 (), arc_challenge:AKDE&ED_2012_8_14 (), pira_ptbr:A1070 ()

**1. [facil · recordar]** Qual é a finalidade da redundância em um sistema?

Resposta: Manter o serviço quando ocorre falha em parte do arranjo.

**2. [media · diagnosticar]** Em um FPSO, um gerador em reserva fria permaneceu meses parado e não assumiu a carga quando a troca automática foi comandada. Que limitação da reserva fria esse evento mostra?

Resposta: Que ela não elimina falhas de partida ou de comutação.

**3. [media · inferir]** Uma configuração redundante elevou a disponibilidade no início da missão, mas o ganho diminuiu em horizonte mais longo, sem mudança de operação do reserva. Qual explicação do texto se aplica?

Resposta: Em tempos mais longos, a degradação dos equipamentos ativos pode deixar de ser compensada pelo reserva.

**4. [dificil · decidir]** Num FPSO, dois trens de tratamento têm equipamentos duplicados, mas compartilham a mesma utilidade elétrica e a mesma lógica de intertravamento de descarga. Um estudo simplificado os tratou como paralelo puro e estimou grande ganho de desempenho. Após perda dessa utilidade, ambos perdem a função. Esse arranjo representa redundância útil para a função de processo?

Resposta: Não. O ganho real é menor que o sugerido pelo paralelo puro, porque as dependências compartilhadas impedem preservar a função de processo relevante.

## 01_01 · bloco 007 · Como selecionar, modelar e atualizar análises RAM

Status: `ok`

Exemplos recebidos: qasc:3KB8R4ZV1E6CN1KPWOPNZELWULQBGW (), arc_challenge:Mercury_7268013 (), mmmlu_ptbr:2 (), mmmlu_ptbr:112 (), pira_ptbr:A1863 (), pira_ptbr:B2268 ()

**1. [facil · recordar]** Além de confiabilidade, disponibilidade e manutenibilidade, que dimensão o RAMS incorpora?

Resposta: Segurança.

**2. [media · decidir]** Num FPSO com o sistema já detalhado, a equipe precisa localizar os maiores contribuintes de falha, comparar modos operacionais e melhorar a previsão de disponibilidade. Que tipo de modelo RAM deve usar?

Resposta: Um modelo mais completo.

**3. [media · inferir]** Após um retrofit, a arquitetura, a acessibilidade para reparo e a estratégia de manutenção de um FPSO mudaram. Se a análise RAM mantiver os parâmetros antigos, como tendem a ficar as previsões?

Resposta: Tendem a ficar imprecisas, porque tempos de reparo e frequências de falha variam com as condições da unidade.

**4. [dificil · decidir]** Na fase preliminar de um FPSO novo, a equipe precisa escolher entre arranjos de compressão e alternativas de redundância. Um dos pacotes é protótipo e não há histórico confiável de falhas nem de reparo. Mesmo assim, propõem um modelo RAM muito detalhado, alimentado por parâmetros genéricos de mercado, para fechar a decisão. Qual abordagem deve ser priorizada?

Resposta: Priorizar um modelo mais simples e aderente ao regime operacional para validar arranjos e redundância; com dados genéricos em unidade nova, o detalhamento tende a gerar resultados imprecisos.

## 01_01 · bloco 008 · Coleta de dados, indicadores e monitoramento do desempenho real

Status: `ok`

Exemplos recebidos: qasc:333U7HK6I9EFT08AIQ1WRH1CPUIJD6 (), mmmlu_ptbr:53 (), arc_challenge:AIMS_2009_8_9 (), mmmlu_ptbr:43 (), pira_ptbr:A658 (), pira_ptbr:A1196 ()

**1. [facil · recordar]** Quais dois tempos devem ser registrados para calcular MTTR e disponibilidade observada?

Resposta: O tempo de início da falha e o tempo de retorno ao estado operacional.

**2. [media · inferir]** Falhas e manutenções são registradas, mas os dados não circulam entre as áreas e as causas não são separadas. O que isso tende a prejudicar?

Resposta: A priorização de ações corretivas, porque as causas deixam de ser distinguíveis de forma útil.

**3. [media · inferir]** Uma unidade possui anos de registros de falha, porém em formatos diferentes e sem gestão eletrônica. O que isso implica para a confiança analítica desses dados?

Resposta: Ela não aumenta como esperado; sem padronização e gestão eletrônica, o histórico perde valor analítico.

**4. [dificil · decidir]** Na revisão de KPIs de um FPSO, a equipe usa médias de bancos setoriais para priorizar itens. O item A aparece pior nessas médias, mas na unidade tem redundância e sua parada não afeta produção. O item B tem poucas falhas nos registros locais, porém cada indisponibilidade bloqueia a exportação. Para identificar o limitante real do desempenho local, qual item deve ser priorizado?

Resposta: O item B, porque a criticidade funcional local e os dados da unidade pesam mais que a taxa de falha genérica.

## 01_01 · bloco 010 · Interações com segurança, manutenção e recursos de suporte

Status: `ok`

Exemplos recebidos: qasc:3I7DHKZYGNZ4KL7LKUSSE7LSLO85FO (), arc_challenge:Mercury_SC_LBS10039 (), mmmlu_ptbr:40 (), pira_ptbr:A489 (), mmmlu_ptbr:148 (), pira_ptbr:B2460 ()

**1. [facil · recordar]** Em que situação mais equipes de manutenção têm efeito limitado no retorno operacional de um FPSO?

Resposta: Quando a espera dominante é por acesso, sobressalente, liberação ou logística, e não pela capacidade das equipes.

**2. [media · inferir]** Num FPSO, duas falhas corretivas ocorrem quase ao mesmo tempo e a capacidade das equipes já é o gargalo. Qual efeito isso tende a causar na indisponibilidade?

Resposta: Tende a criar fila de atendimento e prolongar a indisponibilidade.

**3. [media · decidir]** Para recuperar a disponibilidade mensal, a gestão quer cortar preventivas programadas sem nenhuma análise adicional. Isso é compatível com o critério técnico do sistema?

Resposta: Não. Aumentar a disponibilidade não autoriza reduzir intervenções preventivas sem avaliar risco e integridade.

**4. [dificil · decidir]** Após uma parada, há uma única equipe e uma única liberação de acesso para dois subsistemas. O A restabelece uma função necessária ao retorno de produção em 2 horas. O B afeta apenas otimização e levaria 8 horas, usando a mesma liberação. Qual intervenção deve ser executada primeiro?

Resposta: A do subsistema A, por maior criticidade funcional, menor duração de recuperação e pela restrição compartilhada.

## 01_01 · bloco 011 · Como o processamento primário condiciona a capacidade da unidade

Status: `ok`

Exemplos recebidos: arc_challenge:Mercury_7142713 (), mmmlu_ptbr:82 (), qasc:3WS1NTTKEYB5PELKNOMGXCP10ZPF03 (), pira_ptbr:A905 (), mmmlu_ptbr:134 (), pira_ptbr:A349 ()

**1. [facil · recordar]** Qual é a finalidade operacional da reinjeção da água produzida?

Resposta: Auxiliar a produção de óleo.

**2. [media · inferir]** Se um separador passa a operar abaixo da eficiência esperada, o que pode ocorrer com a qualidade dos fluidos separados e que ajuste pode ser necessário para manter especificações?

Resposta: A qualidade pode cair, e a produção pode ter de ser reduzida.

**3. [media · inferir]** A malha de água produzida perde capacidade, mas a exportação de óleo e a compressão de gás permanecem disponíveis. Qual efeito isso pode impor sobre a vazão total do campo?

Resposta: Pode impor redução da vazão total do campo por falta de capacidade para lidar com a fase aquosa gerada.

**4. [dificil · decidir]** Em um FPSO, a quantidade de água produzida sobe e um tratador passa a operar abaixo da eficiência esperada. A água tratada se aproxima do limite para descarte no mar, a reinjeção já está no máximo e bombas de óleo e compressores seguem normais. Para manter especificações e estabilidade operacional, qual decisão deve ser tomada sobre a vazão da unidade?

Resposta: Reduzir a produção total até recuperar a capacidade de separação e tratamento da fase aquosa, pois esse gargalo passou a limitar a unidade.

## 01_01 · bloco 012 · Seleção e aplicação de medidas para prevenir ou aliviar gargalos

Status: `ok`

Exemplos recebidos: pira_ptbr:A365 (), pira_ptbr:A1439 (), arc_challenge:MEA_2010_8_20-v1 (), mmmlu_ptbr:84 (), qasc:3B3WTRP3DB13KEXLZPQ264W5XZ992N (), mmmlu_ptbr:102 ()

**1. [facil · recordar]** Qual objetivo econômico da prevenção de incrustações na estratégia offshore?

Resposta: Reduzir custos associados a perdas de produção.

**2. [media · decidir]** Em uma FPSO, a restrição por incrustação já reduziu a capacidade de processamento. Pelo horizonte de atuação, a medida adequada é preventiva ou corretiva?

Resposta: Corretiva, porque a restrição já comprometeu a capacidade.

**3. [media · comparar]** Mantendo iguais o mecanismo dominante e a origem dos íons, duas rotas de controle de incrustação diferem só pela facilidade de intervenção e pelo impacto da parada. Que critérios decidem a seleção?

Resposta: A acessibilidade para intervenção e as penalidades de parada.

**4. [dificil · decidir]** Em uma FPSO, a equipe propõe ampliar um equipamento que opera perto do limite. Testes mostram, porém, que a capacidade só aumenta quando se muda uma condição operacional específica, e uma ampliação anterior apenas transferiu a restrição para outra etapa. Qual deve ser a abordagem correta?

Resposta: Atuar na condição operacional limitante, não ampliar o equipamento; o debottlenecking deve aliviar a restrição real sem deslocar o gargalo.

## 01_01 · bloco 013 · Consequências operacionais e econômicas das restrições em FPSO

Status: `ok`

Exemplos recebidos: mmmlu_ptbr:51 (), arc_challenge:AKDE&ED_2012_8_42 (), pira_ptbr:B2513 (), pira_ptbr:A260 (), qasc:3A4TN5196KH9X276UU30VY3FSDCCHR (), mmmlu_ptbr:71 ()

**1. [facil · recordar]** A perda de produção em FPSO é apenas tema de eficiência?

Resposta: Não; ela também interage com integridade, conformidade, segurança e decisões de investimento.

**2. [media · decidir]** Um gargalo surgiu em um ponto comum do sistema do FPSO e não será removido no curto prazo. Que classe de decisão operacional passa a ser inevitável para operar dentro da capacidade disponível?

Resposta: Priorizar entregas e alocar a capacidade do sistema, por exemplo redistribuindo vazões ou reduzindo a carga de processamento.

**3. [media · comparar]** Dois FPSOs têm a mesma frequência de offloading. Em um, localização, ancoragem, casco, convés e arranjo de produção/armazenagem estão mais aderentes às condições do campo. Qual tende a ter menos paradas entre offloadings?

Resposta: O FPSO mais aderente às condições locais, porque esses fatores de projeto influenciam a minimização de paradas entre offloadings.

**4. [dificil · diagnosticar]** Em um FPSO de alta produção, um problema relevante não é detectado pelo autodiagnóstico e as ações contingenciais e corretivas não entram em vigor no prazo compatível com o risco. A recomposição das barreiras levará vários dias. Qual desfecho operacional e econômico deve ser assumido?

Resposta: Interdição da instalação, com perdas econômicas elevadas pela combinação de alto volume produzido e longa indisponibilidade.

## 01_01 · bloco 015 · Atribuição de causas: do mecanismo físico à perda observada

Status: `ok`

Exemplos recebidos: pira_ptbr:A1340 (), mmmlu_ptbr:91 (), qasc:3R0T90IZ1SBVX6CVAOLIAYREEH4GCA (), pira_ptbr:B2326 (), mmmlu_ptbr:60 (), arc_challenge:MSA_2013_5_33 ()

**1. [facil · recordar]** Na análise de perdas, que conceito descreve a forma como a incapacidade de operar se manifesta?

Resposta: Modo de falha.

**2. [media · diagnosticar]** Em um poço ligado ao FPSO, há aumento da resistência ao fluxo na coluna e mudança de pressão observada. Qual restrição física explica também a queda de vazão bruta?

Resposta: Incrustação na coluna de produção.

**3. [media · inferir]** Após uma perda de capacidade, o registro informa apenas que foi aplicado inibidor. Que dado falta para prever corretamente o efeito esperado dessa ação?

Resposta: Falta explicitar para qual mecanismo o inibidor foi escolhido, porque cada tipo tem efeito esperado diferente.

**4. [dificil · decidir]** Em um poço de FPSO, a vazão bruta caiu e a qualidade do produto piorou. A pressão no poço mudou após aumento da resistência ao fluxo, e inspeção confirmou depósito aderido na coluna; a equipe quer lançar a causa apenas como 'baixa produção' e manter somente dosagem preventiva. Para o KPI e a recuperação de capacidade, qual decisão é correta?

Resposta: Registrar restrição por incrustação na coluna, não o sintoma final; recuperar capacidade requer remover o depósito e avaliar a integridade do equipamento.

## 01_01 · bloco 016 · Condições que mudam o comportamento do risco no processamento primário

Status: `ok`

Exemplos recebidos: pira_ptbr:A1725 (), qasc:3AMW0RGHOD1K1N2L2XKJKIZID83PNU (), mmmlu_ptbr:50 (), mmmlu_ptbr:102 (), pira_ptbr:A1021 (), arc_challenge:Mercury_407675 ()

**1. [facil · recordar]** Qual condição de medição eleva o risco de processo no processamento primário?

Resposta: A ausência ou baixa confiabilidade de medições essenciais.

**2. [media · inferir]** Em uma perturbação operacional, a separação óleo-água perde eficiência e o processo fica em controle manual com alta demanda de atenção. Qual efeito isso tem na capacidade de detectar e corrigir desvios?

Resposta: Ela diminui, porque a observabilidade do processo e a margem para correção ficam reduzidas, aumentando o risco.

**3. [media · comparar]** Duas unidades recebem a mesma perturbação e têm a mesma instrumentação e flexibilidade operacional. A primeira dispõe de maior capacidade de segregação e maior inventário intermediário. Qual absorve melhor o desvio antes de reduzir carga ou parar?

Resposta: A primeira, porque maior capacidade de segregação e inventário intermediário ampliam a absorção da perturbação.

**4. [dificil · decidir]** Dois FPSOs com a mesma designação enfrentam o mesmo distúrbio de processo. Na Unidade A, as medições essenciais são confiáveis e há boa capacidade de segregação, inventário intermediário e flexibilidade operacional. Na Unidade B, faltam medições críticas, a separação óleo-água está ineficiente e a flexibilidade é limitada. Qual unidade tende a reduzir carga ou parar primeiro?

Resposta: A Unidade B, porque o arranjo real combina menor observabilidade e menor capacidade de absorver a perturbação; a designação isoladamente não determina a resposta.

## 01_01 · bloco 017 · Estrutura organizacional, gestão de mudanças e autonomia técnica

Status: `ok`

Exemplos recebidos: mmmlu_ptbr:101 (), mmmlu_ptbr:77 (), qasc:3DY46V3X3PHCIOEWEIFJSVUFXGE55Y (), arc_challenge:Mercury_7126683 (), pira_ptbr:B2393 (), pira_ptbr:A1310 ()

**1. [facil · recordar]** Que atividade documental a estrutura organizacional deve sustentar na gestão de riscos?

Resposta: Atualização documental.

**2. [media · comparar]** Duas unidades usam a mesma técnica de análise. Na A, a documentação é acessível e a responsabilidade técnica é clara; na B, há dependência de suporte remoto e documentos difíceis de obter. Em um desvio operacional, qual tende a validar mais rápido uma mudança?

Resposta: A unidade A, porque consegue decidir com documentação acessível e responsabilidade técnica definida.

**3. [media · inferir]** Num FPSO com risco dinâmico e condições mudando ao longo do tempo, falhas contínuas de comunicação e fatores humanos não tratados tendem a reduzir o quê no sistema de gestão?

Resposta: A robustez e a resiliência do sistema de gestão.

**4. [dificil · decidir]** Um ajuste temporário foi incorporado à rotina do FPSO. Desde então, cada novo desvio exige consultas em cadeia, as premissas usadas nas decisões anteriores não são recuperadas com rapidez e os documentos de bordo não confirmam a configuração vigente. Sem falha física dos controles, o que deve ser priorizado para restaurar sua efetividade?

Resposta: Fortalecer a gestão de mudanças, definindo quem interpreta o problema e autoriza ações e mantendo a documentação coerente com a instalação real.

## 01_01 · bloco 018 · Monitoramento, revisão e aprendizagem para próximas intervenções

Status: `ok`

Exemplos recebidos: mmmlu_ptbr:60 (), qasc:3H0W84IWBK11JU5NMQLPZQ5O0H3REE (), mmmlu_ptbr:121 (), arc_challenge:Mercury_SC_408759 (), pira_ptbr:A666 (), pira_ptbr:A1751 ()

**1. [facil · recordar]** Na gestão de paradas, que instrumento consolida objetivo, escopo, prazos e lições da intervenção?

Resposta: O relatório final da parada.

**2. [media · inferir]** Após uma parada, o registro mostrou subestimação da complexidade, acréscimo de escopo e suporte extra não previsto. No planejamento de custo do ciclo de vida, qual ajuste esse histórico deve provocar?

Resposta: Revisar estimativas e recursos futuros conforme a complexidade real e o suporte efetivamente necessário.

**3. [media · decidir]** Com objetivo e escopo mantidos, o histórico mostra que um pacote concentrou os principais desvios da parada anterior. Se a equipe precisa definir qual pacote receberá atenção preventiva primeiro, para que esse registro deve ser usado?

Resposta: Para retroalimentar a priorização por risco.

**4. [dificil · decidir]** Em três paradas consecutivas de um FPSO, o mesmo pacote atrasou a linha crítica, consumiu mais homens-hora e exigiu suporte contratual acima do previsto. Os relatórios foram encerrados com campos preenchidos, porém sem comparar planejado e realizado nem transformar desvios em lições utilizadas depois. Para a próxima intervenção, qual mudança de gestão deve vir primeiro?

Resposta: Implantar análise crítica disciplinada do relatório final, registrando planejado, ocorrido, desvios e lições válidas; o preenchimento formal sozinho não retroalimenta a decisão.

## 01_01 · bloco 019 · Seleção de sistemas críticos e uso de histórico de falhas

Status: `ok`

Exemplos recebidos: qasc:3ON104KXQKVOZOPGWEJID31EEEQ4W3 (), mmmlu_ptbr:1 (), pira_ptbr:A839 (), arc_challenge:MDSA_2007_8_47 (), pira_ptbr:B2376 (), mmmlu_ptbr:66 ()

**1. [facil · recordar]** Qual efeito da identificação de sistemas críticos sobre os controles de risco?

Resposta: Ela orienta a implantação e a atualização dos controles ao definir quais funções recebem tratamento prioritário.

**2. [media · comparar]** Dois FPSOs têm histórico corporativo semelhante, mas um opera com configuração, manutenção e barreiras diferentes. É correto aplicar o mesmo ranking fixo de criticidade aos dois?

Resposta: Não. Frequência e gravidade mudam com essas condições; o histórico não é um ranking universal aplicável a qualquer FPSO.

**3. [media · decidir]** Após analisar acidentes anteriores de instalações industriais e marítimas, para que a equipe deve usar esse histórico na revisão da criticidade?

Resposta: Para formular hipóteses de falha, revisar cenários e reconhecer funções sensíveis do processo.

**4. [dificil · decidir]** Na revisão de criticidade, o histórico corporativo aponta mais ocorrências em um sistema de outra configuração de FPSO. Na unidade avaliada, porém, os maiores desvios potenciais estão nas funções de separação e medição, sob regime operacional distinto. A equipe deve seguir o ranking histórico ou priorizar outra base de decisão?

Resposta: Deve priorizar o exame específico das funções e vulnerabilidades da unidade, usando o histórico apenas para informar a análise.

## 01_01 · bloco 021 · Confiabilidade, disponibilidade e suporte de manutenção

Status: `ok`

Exemplos recebidos: arc_challenge:Mercury_7142713 (), mmmlu_ptbr:37 (), mmmlu_ptbr:48 (), pira_ptbr:A357 (), qasc:3KYQYYSHYV6TUBZ7Y3T1ZDIY26YODE (), pira_ptbr:A1278 ()

**1. [facil · recordar]** Além da confiabilidade, que capacidades compõem a disponibilidade de um item?

Resposta: Mantenabilidade e suporte de manutenção, com os recursos externos necessários assegurados.

**2. [media · comparar]** Dois itens operam nas mesmas condições e têm igual confiabilidade e suporte de manutenção. Um é restaurado mais rapidamente após falha. Qual tende a apresentar maior disponibilidade?

Resposta: O item restaurado mais rapidamente, porque a disponibilidade combina também a mantenabilidade.

**3. [media · inferir]** Um operador quer que fabricante e prestador de serviço usem registros compatíveis de falhas e manutenção para avaliar desempenho do ativo. Que contribuição da engenharia de confiabilidade atende essa necessidade?

Resposta: Organizar dados de confiabilidade e manutenção em formato padronizado para troca de informação entre as partes.

**4. [dificil · decidir]** Em um FPSO, um item crítico pode seguir operando degradado, e a equipe pensa em adiar a manutenção porque a probabilidade de falha no curto prazo é baixa. Não há sobressalente a bordo, o especialista depende de mobilização externa e o acesso pode atrasar por condições operacionais. A baixa probabilidade de falha basta para sustentar o adiamento?

Resposta: Não. A decisão também deve considerar o tempo e os meios para restaurar a função; com suporte de manutenção restrito, a disponibilidade fica comprometida.

## 01_01 · bloco 022 · Consequências econômicas de controles insuficientes

Status: `ok`

Exemplos recebidos: arc_challenge:NCEOGA_2013_5_25 (), qasc:3T111IHZ5EPKOYE6EF537C4D8OX9R3 (), pira_ptbr:A1229 (), mmmlu_ptbr:18 (), mmmlu_ptbr:144 (), pira_ptbr:A345 ()

**1. [facil · recordar]** Além de segurança e conformidade operacional, que dimensão a decisão sobre controle de risco também afeta?

Resposta: O custo ao longo da vida útil do ativo.

**2. [media · comparar]** Dois FPSOs teriam a mesma parada forçada de 24 horas. Mantidas iguais as demais condições, em qual deles a perda potencial de receita tende a ser maior?

Resposta: No de maior produção, porque a receita diária comprometida durante a parada forçada é maior.

**3. [media · inferir]** Um gestor compara gasto preventivo e custo de falha olhando apenas o desembolso imediato. Nesse raciocínio, que efeito econômico relevante fica de fora?

Resposta: O efeito acumulado de indisponibilidade, correções emergenciais e restrições operacionais.

**4. [dificil · decidir]** Dois FPSOs podem ser interditados por controles insuficientes. O FPSO A produz mais por dia, mas a correção prevista é pontual e a parada estimada é curta. O FPSO B produz menos, porém exigiria correção emergencial extensa, parada muito mais longa e contrato mais restritivo. Qual deve ter prioridade no gasto preventivo por consequência econômica esperada?

Resposta: O FPSO B, porque a decisão não deve olhar só a produção diária; duração da parada, escopo corretivo e contexto contratual podem elevar mais o custo de falha.

## 01_01 · bloco 023 · Análise de causa: mecanismo de falha, modo de falha e FMEA

Status: `ok`

Exemplos recebidos: pira_ptbr:A1639 (), qasc:3QAVNHZ3EM3NQJTY11M7HV6Y8OIAL5 (), pira_ptbr:B1980 (), arc_challenge:MCAS_2004_9_15 (), mmmlu_ptbr:29 (), mmmlu_ptbr:19 ()

**1. [facil · recordar]** Em FMEA que usa NPR, por qual operação se obtém esse índice a partir de severidade, ocorrência e detecção?

Resposta: Pela multiplicação das três classificações.

**2. [media · diagnosticar]** Em um trocador, ataque químico progressivo levou à perda de função. Nessa análise, esse ataque deve ser tratado como mecanismo ou como modo de falha?

Resposta: Como mecanismo de falha, por ser o processo químico que levou à perda de função.

**3. [media · inferir]** Na preparação de uma FMEA, operação, manutenção e engenharia descrevem de formas diferentes a função do mesmo equipamento. Qual requisito da aplicação fica comprometido?

Resposta: O entendimento comum das funções analisadas.

**4. [dificil · decidir]** Dois modos de falha de um sistema de utilidades receberam NPR 96. Um combina severidade alta e baixa ocorrência; o outro, severidade menor e detecção pior. A equipe quer tratá-los como equivalentes porque o índice empatou. Qual decisão técnica deve ser tomada?

Resposta: Não tratá-los como equivalentes só pelo NPR; é preciso analisar individualmente as consequências críticas de cada modo antes de priorizar.

## 02_02 · bloco 000 · Como selecionar e aplicar: bottle test como triagem empírica

Status: `ok`

Exemplos recebidos: mmmlu_ptbr:102 (), arc_challenge:MEA_2014_5_13 (), pira_ptbr:B2040 (), mmmlu_ptbr:84 (), pira_ptbr:A1658 (), qasc:3VBEN272MKYB4N1R7ABIP3VW36GGS5 ()

**1. [facil · recordar]** Qual é o papel do frasco sem produto no bottle test?

Resposta: Medir a separação natural da emulsão e servir como referência de comparação.

**2. [media · inferir]** Em um bottle test de emulsão óleo-em-água, dois produtos geram volumes semelhantes de fase separada. Qual observação adicional decide qual teve melhor desempenho?

Resposta: A clarificação da fase aquosa.

**3. [media · comparar]** Dois frascos tratados receberam produtos diferentes, porém um foi testado com temperatura maior e menor tempo de observação. Qual conclusão fica inválida?

Resposta: A de que um produto é superior ao outro, porque a diferença pode vir das condições de teste, não da química.

**4. [dificil · decidir]** Na bancada, um desemulsificante foi escolhido pelo maior volume de água separado após mistura branda. No FPSO, porém, a limitação operacional não é esse volume, e a separação final entre as fases continua ruim; além disso, o escoamento real tem maior cisalhamento e menor tempo de residência que o ensaio. Antes de trocar de química, qual revisão da avaliação deve ser priorizada?

Resposta: Repetir e validar o bottle test com fluido e condições representativas do processo, adotando a qualidade da interface como critério principal.  
_usa apoio_

## 02_02 · bloco 003 · Por que pH, salmoura, petróleo e asfaltenos mudam o desempenho

Status: `ok`

Exemplos recebidos: pira_ptbr:A406 (), pira_ptbr:A1483 (), arc_challenge:Mercury_7043995 (), qasc:3IHR8NYAM70YFFSFKS5NL9TIN4D4PA (), mmmlu_ptbr:79 (), mmmlu_ptbr:41 ()

**1. [facil · recordar]** De quais elementos do sistema depende a estabilidade de uma emulsão?

Resposta: Da composição do petróleo, da salmoura e do filme interfacial.

**2. [media · inferir]** Em um FPSO, a mistura de entrada passa a conter mais asfaltenos e sólidos, mantidas as demais condições semelhantes. Qual efeito tende a aparecer na separação por coalescência?

Resposta: Maior dificuldade de coalescência, porque asfaltenos e sólidos podem formar filmes resistentes em torno das gotas.

**3. [media · diagnosticar]** Em testes com a mesma emulsão, as gotas chegam a tocar umas nas outras, mas a separação continua lenta. Que ação do aditivo passa a ser decisiva?

Resposta: Modificar a organização do filme interfacial e facilitar a drenagem entre gotas em contato.

**4. [dificil · decidir]** Em bancada, um desemulsificante foi escolhido usando uma única salmoura sintética. No FPSO, o pH e a salinidade da água produzida variam entre poços e ao longo da campanha. A equipe quer manter a escolha com base só nesse ensaio inicial. Qual decisão técnica é correta?

Resposta: Não manter a escolha por esse ensaio isolado; os produtos devem ser comparados em condições representativas do sistema, porque o efeito de pH e salinidade depende da formulação e do fluido.

## 02_02 · bloco 006 · Como o antiespumante atua na quebra da espuma

Status: `ok`

Exemplos recebidos: arc_challenge:Mercury_SC_400696 (), pira_ptbr:A950 (), mmmlu_ptbr:44 (), mmmlu_ptbr:75 (), qasc:3ND9UOO81K1KXWW126IZZK3P06SWL7 (), pira_ptbr:A1591 ()

**1. [facil · recordar]** Ao atuar corretamente, que efeito o antiespumante deve promover no filme que estabiliza a bolha?

Resposta: Favorecer a ruptura ou a drenagem do filme líquido.

**2. [media · inferir]** Em um teste de processo, apenas as propriedades da interface gás-líquido mudam; a formulação do antiespumante é mantida. O que tende a ser diretamente afetado em sua atuação?

Resposta: Seu espalhamento, penetração e dispersão na interface.

**3. [media · diagnosticar]** Dois poços alimentam o mesmo separador com a mesma dose de antiespumante. Um dos fluidos passa a trazer mais tensoativos e sólidos. Sem alterar a injeção do produto, que mudança de resposta é esperada?

Resposta: A espuma pode ficar mais estável e o contato do antiespumante com o filme mais difícil, reduzindo a resposta.

**4. [dificil · decidir]** Após mudança na composição do fluido de um separador, a espuma persiste. A dose do antiespumante foi aumentada em etapas; houve melhora inicial, mas acima de certa faixa o desempenho parou de crescer, embora a dispersão do produto continue adequada. Qual decisão técnica sobre o ajuste deve ser tomada?

Resposta: Interromper a escalada de dose como única ação; o limite útil foi atingido e mais concentração não garante melhor desempenho.

## 02_02 · bloco 009 · Interações e efeitos colaterais relevantes no processamento

Status: `ok`

Exemplos recebidos: mmmlu_ptbr:37 (), mmmlu_ptbr:67 (), pira_ptbr:B2096 (), pira_ptbr:A286 (), qasc:3U4J9857OEATU89O3LLTT183THRB79 (), arc_challenge:Mercury_7170433 ()

**1. [facil · recordar]** Em separadores, que efeito a melhora da quebra de espuma tende a causar na saída de gás?

Resposta: Tende a reduzir o arraste de líquido na saída de gás.

**2. [media · comparar]** Duas formulações quebram a espuma no mesmo ponto do processo com eficácia semelhante. Se a estabilidade de interfaces a jusante é crítica, qual delas oferece maior risco operacional?

Resposta: A formulação que contém fases oleosas, sólidos ou emulsificantes.

**3. [media · diagnosticar]** A dose foi mantida e não há evidência de mudança do fluido, mas o efeito do antiespumante oscila entre campanhas. Se a mistura na aplicação é insuficiente, o que explica essa inconsistência?

Resposta: O produto não alcança de modo consistente a interface crítica, gerando contato inefetivo.

**4. [dificil · decidir]** Após meses de operação estável, o FPSO passa a produzir com maior corte de água e salinidade. A mesma formulação ainda derruba a espuma no separador, porém a resposta fica irregular e interfaces em equipamentos a jusante se tornam sensíveis. Qual decisão técnica deve ser priorizada?

Resposta: Revisar o programa químico e a seleção da formulação, pois a mudança do fluido pode deslocar o equilíbrio entre formação e quebra de espuma e agravar interações de interface a jusante.

## 02_02 · bloco 012 · Por que esses químicos funcionam na água produzida

Status: `ok`

Exemplos recebidos: pira_ptbr:A1424 (), pira_ptbr:B2571 (), qasc:31LM9EDVOLROFCZN7KFZNMD65HEJNM (), arc_challenge:Mercury_7142695 (), mmmlu_ptbr:126 (), mmmlu_ptbr:22 ()

**1. [facil · recordar]** Além das forças elétricas, que fator de interface também ajuda a manter estáveis gotas finas de óleo na água produzida?

Resposta: Filmes interfaciais resistentes.

**2. [media · inferir]** Em uma água produzida, a estabilidade vem principalmente das forças elétricas entre gotas de óleo e matéria coloidal. Qual efeito do coagulante favorece o encontro entre essas entidades?

Resposta: Neutralizar cargas, reduzindo a repulsão elétrica e permitindo maior aproximação entre gotas e sólidos.

**3. [media · decidir]** Em um FPSO, pretende-se trocar um coagulante sintético por um natural mantendo a mesma água produzida e o mesmo sistema de descarte. Qual condição técnica deve ser comprovada antes da troca?

Resposta: A equivalência de desempenho do coagulante natural nessa água produzida.

**4. [dificil · diagnosticar]** Na água produzida de um FPSO, um coagulante já reduziu a repulsão entre gotas e sólidos, mas a flotação por ar dissolvido continua ineficiente. As microbolhas estão normais; ainda assim, os agregados observados são pequenos e se rompem facilmente. Qual deficiência química explica melhor o quadro?

Resposta: Insuficiência de floculante polimérico; faltam pontes entre entidades desestabilizadas para aumentar o tamanho e a resistência mecânica dos flocos.

## 02_02 · bloco 015 · Consequências e interações relevantes para o descarte

Status: `ok`

Exemplos recebidos: pira_ptbr:A894 (), arc_challenge:NYSEDREGENTS_2009_8_7 (), mmmlu_ptbr:3 (), qasc:3OJSZ2ATDSVR5SSF2BUGQF8BQBO75A (), pira_ptbr:A750 (), mmmlu_ptbr:79 ()

**1. [facil · recordar]** Além da remoção de óleo, o que a escolha e a dosagem do programa químico também afetam no tratamento da água produzida?

Resposta: O perfil do efluente tratado.

**2. [media · inferir]** Um agente que quebrava a emulsão de uma água produzida foi aplicado em outra corrente e passou a estabilizar a interface. O que esse resultado indica sobre a interação química do sistema?

Resposta: Que a resposta depende da composição da água e das interações com surfactantes e outros aditivos; o mesmo agente pode ter efeito oposto em outra água.

**3. [media · decidir]** Em um FPSO, a água produzida permanece a mesma, mas o regime de escoamento foi alterado e a configuração da flotação mudou após uma intervenção. O que deve ser feito no tratamento para descarte?

Resposta: Reavaliar o desempenho do tratamento, porque essas mudanças podem deslocar a condição ótima.

**4. [dificil · diagnosticar]** Após incluir poços de outra origem e mudar o programa químico de produção, a água tratada passou a sair com mais sólidos suspensos e pior resposta na flotação, embora o teor de óleo de entrada e o hardware da flotação tenham permanecido estáveis. Qual diagnóstico deve orientar a ação imediata no tratamento para descarte?

Resposta: Que a nova composição do fluido e resíduos dos químicos de produção alteraram a resposta da flotação e deslocaram a dosagem ótima; o programa químico precisa ser reavaliado.

## 02_02 · bloco 018 · Papel dos inibidores de incrustação e limites de aplicação em sistemas com URS

Status: `ok`

Exemplos recebidos: pira_ptbr:A1258 (), arc_challenge:Mercury_7282118 (), pira_ptbr:A934 (), mmmlu_ptbr:152 (), qasc:3P59JYT76LJM4T6ZXVVJX4XHPQHT2E (), mmmlu_ptbr:18 ()

**1. [facil · recordar]** Que efeito o inibidor pode exercer quando cristais já existem?

Resposta: Distorção e dispersão dos cristais.

**2. [media · comparar]** Dois inibidores serão usados no mesmo ponto, com igual pH, cálcio, quelantes e massa molecular. Um mantém suas propriedades nas condições de operação do FPSO; o outro se decompõe com a temperatura. Qual tende a ser mais eficiente?

Resposta: O que permanece estável química e termicamente.

**3. [media · inferir]** Em uma unidade sem dessulfatação, duas correntes de águas incompatíveis passam a se misturar antes de trocadores e bombas. Que tratamento químico pode ser requerido nesse trecho?

Resposta: Inibidor de incrustação para proteger trocadores, bombas e o ponto de mistura.

**4. [dificil · decidir]** Um FPSO com URS quer reduzir consumo químico mantendo inibidor apenas na água de injeção. A justificativa é que a dessulfatação já reduz o risco principal. Porém a planta de processo ainda tende a formar CaCO3, e a URS gera uma corrente concentrada rica em sulfato. Essa mudança é tecnicamente adequada?

Resposta: Não. Dosar só na água de injeção não garante proteção à produção, porque o produto pode adsorver na rocha próxima ao injetor; além disso, seguem requerendo inibidor o CaCO3 na planta e o concentrado da URS com risco de CaSO4.

## 02_02 · bloco 021 · Sequestrante químico: bissulfito de sódio, mecanismo e limitações

Status: `ok`

Exemplos recebidos: mmmlu_ptbr:68 (), arc_challenge:Mercury_7027038 (), mmmlu_ptbr:144 (), pira_ptbr:A1189 (), pira_ptbr:A943 (), qasc:3HL8HNGX450NL89XNK59QNQU4L99F0 ()

**1. [facil · recordar]** Que função o bissulfito de sódio exerce no condicionamento de água?

Resposta: Reagir com o oxigênio dissolvido para removê-lo da água.

**2. [media · inferir]** Num sistema de água de injeção, a dosagem aplicada ficou abaixo da necessária para a carga de oxigênio presente. Qual efeito deve aparecer no sistema?

Resposta: Deve permanecer oxigênio residual, porque a dosagem foi insuficiente para consumi-lo.

**3. [media · inferir]** Se a solução de bissulfito for armazenada com maior exposição ao ar, o que tende a acontecer com sua concentração ativa disponível para dosagem?

Resposta: Ela tende a ser pior conservada e a perder concentração ativa.

**4. [dificil · diagnosticar]** Em um skid de água de injeção de um FPSO, aumentou-se a dosagem de solução diluída de bissulfito para reduzir o residual de oxigênio. O residual caiu, mas surgiram sinais de ataque em materiais sensíveis à acidez, sem mudança em outros químicos ou materiais. Qual mecanismo explica melhor o novo problema?

Resposta: Corrosão favorecida pelo baixo pH da solução diluída de bissulfito, agravada pela maior dosagem.

## 02_02 · bloco 024 · Condições que mudam o comportamento: cloro residual, CO2 e disponibilidade de gás

Status: `ok`

Exemplos recebidos: pira_ptbr:A1727 (), arc_challenge:Mercury_180163 (), pira_ptbr:A1022 (), mmmlu_ptbr:66 (), mmmlu_ptbr:31 (), qasc:38F71OA9GTV2SSSRCT9EV9WE9NLMFS ()

**1. [facil · recordar]** Que tipo de arranjo pode ser usado conforme o balanço de remoção, o espaço, o peso e as utilidades do projeto?

Resposta: Sistemas combinados.

**2. [media · diagnosticar]** Após cloração, há cloro residual em excesso. O consumo de bissulfito subiu e o oxigênio dissolvido a jusante permaneceu alto. Que mecanismo explica esse comportamento?

Resposta: O cloro residual está reagindo com o bissulfito, deixando menos sequestrante disponível para consumir o oxigênio dissolvido.

**3. [media · comparar]** Duas correntes de água do mar têm a mesma composição e temperatura; apenas uma passa por desaeração a vácuo com remoção de CO2 dissolvido. Em qual delas a tendência teórica à formação de carbonato de cálcio é maior?

Resposta: Na corrente que passou por desaeração a vácuo, pela remoção de CO2 que desequilibra o sistema carbonato/bicarbonato.

**4. [dificil · decidir]** Em um FPSO, a água do mar chega com cloro residual alto; o consumo de bissulfito cresce, mas o oxigênio dissolvido não cai na mesma proporção. O gás disponível para stripping é inadequado e não há destino seguro para a corrente gasosa. Que rota de desoxigenação deve ser priorizada?

Resposta: Priorizar a rota a vácuo, porque o cloro consome parte do sequestrante e o stripping não é adequado sem gás apropriado e sem destino seguro.

## 02_02 · bloco 027 · Função do controle microbiológico na água de injeção

Status: `ok`

Exemplos recebidos: mmmlu_ptbr:178 (), qasc:3E337GFOL97EOA9MZEUWQ9LQFP0GNK (), arc_challenge:Mercury_7172795 (), pira_ptbr:B2040 (), pira_ptbr:B2393 (), mmmlu_ptbr:37 ()

**1. [facil · recordar]** Qual é a função do controle microbiológico na água de injeção?

Resposta: Limitar a contaminação, o crescimento e a atividade de microrganismos que favorecem biofilme, souring e corrosão microbiologicamente influenciada.

**2. [media · inferir]** Em água de injeção com sulfato disponível, a atividade de BRS aumenta. Que transformação química explica o maior risco para equipamentos de ferro e aço?

Resposta: A redução de sulfato a sulfeto, associada ao desenvolvimento de biocorrosão em ferro e aço.

**3. [media · comparar]** Mantidos produto e dosagem, um trecho passa a ter mais depósito interno e pior escoamento que outro limpo. Como tende a mudar a eficácia do programa microbiológico nesse trecho?

Resposta: A eficácia tende a diminuir, porque depósito e pior escoamento dificultam o alcance do tratamento aos microrganismos.

**4. [dificil · diagnosticar]** Após um choque de biocida na água de injeção, as contagens na fase aquosa caem. Mesmo assim, persistem corrosão localizada e contaminação em pontos com incrustação e baixo escoamento, onde linhas e filtros já tinham superfícies internas colonizadas. Qual fonte de contaminação explica essa persistência?

Resposta: A comunidade aderida em biofilme nas superfícies internas, protegida por incrustação e pouco alcançada pelo biocida.

## 02_02 · bloco 029 · Por que biofilme, incrustação e depósitos reduzem a eficácia

Status: `ok`

Exemplos recebidos: pira_ptbr:B2325 (), arc_challenge:MSA_2012_5_14 (), mmmlu_ptbr:144 (), qasc:3VA45EW49NMZ2GJVIA96YBHPDTA1OK (), mmmlu_ptbr:74 (), pira_ptbr:A1285 ()

**1. [facil · recordar]** Em sistemas sob escoamento, que característica da superfície influencia a formação de biofilme?

Resposta: A rugosidade da superfície.

**2. [media · inferir]** Em uma linha de água de injeção, o mesmo biocida que controla células livres passa a atuar sobre biofilme recoberto por incrustação mineral e sulfeto de ferro. Como tende a mudar a dosagem necessária?

Resposta: Tende a ser maior do que a usada para células livres.

**3. [media · decidir]** Na investigação de corrosão em um sistema de água de injeção, foram detectadas bactérias na água. Isso basta para definir a causa do ataque?

Resposta: Não; a causa deve ser avaliada em conjunto com depósitos, química da água e suscetibilidade do material.

**4. [dificil · decidir]** Em um circuito de água de injeção, a concentração ativa do biocida no fluxo principal atende à meta e o programa alterna entre dosagem contínua e intermitente, mas a atividade microbiológica persiste. Inspeções mostram biofilme espesso e depósitos aderidos nas regiões contaminadas. Qual decisão técnica deve ser priorizada para recuperar a eficácia do tratamento?

Resposta: Priorizar a remoção de biofilmes e depósitos, quando tecnicamente viável; revisar o regime sozinho não basta.  
_usa apoio_

## 02_02 · bloco 032 · Como a inibição funciona e quais limites mecanísticos importam

Status: `ok`

Exemplos recebidos: pira_ptbr:A251 (), arc_challenge:Mercury_7033863 (), pira_ptbr:A143 (), mmmlu_ptbr:152 (), qasc:3Z9WI9EOZZNRG0JUM7KYJHGNAJXKHV (), mmmlu_ptbr:18 ()

**1. [facil · recordar]** Como o MEG dificulta termodinamicamente a formação de hidratos?

Resposta: Ele reduz a atividade da água e desloca o equilíbrio de formação de hidratos para condições mais severas.

**2. [media · comparar]** Duas correntes têm a mesma pressão e a mesma composição de gás. Se uma delas tiver maior concentração efetiva de MEG na água livre, como muda a temperatura mínima de operação antes do equilíbrio de hidrato?

Resposta: Ela pode operar a temperatura mais baixa antes de atingir a condição de equilíbrio do hidrato.

**3. [media · inferir]** A vazão nominal de MEG foi mantida, mas a água produzida aumentou e a mistura ficou deficiente após o ponto de injeção. Qual consequência local é esperada para a proteção contra hidratos?

Resposta: A concentração efetiva de MEG na água livre cai em parte do sistema, podendo deixar regiões sem proteção.

**4. [dificil · decidir]** Após uma partida a frio, surgem indícios de hidrato em um trecho com água livre. A vazão nominal de MEG não mudou, mas houve aumento de água produzida e suspeita de má distribuição após a injeção. A equipe atribui o risco apenas ao histórico térmico da linha. O que deve ser priorizado para decidir se a proteção é suficiente?

Resposta: Reavaliar a concentração efetiva de MEG na água livre e a margem ao equilíbrio de hidrato; o histórico térmico influencia, mas não substitui essa verificação.

## 02_02 · bloco 035 · Seleção, monitoramento e alternativas de regeneração

Status: `ok`

Exemplos recebidos: arc_challenge:ACTAAP_2007_7_24 (), mmmlu_ptbr:48 (), pira_ptbr:A380 (), pira_ptbr:A1082 (), mmmlu_ptbr:201 (), qasc:3OS4RQUCR9E691OUL4J5HTLKSLABFA ()

**1. [facil · recordar]** Qual é a finalidade da regeneração no programa de MEG?

Resposta: Remover água para permitir o reúso do glicol.

**2. [media · inferir]** Após uma mudança de operação, a concentração de glicol na fase aquosa permaneceu na meta, mas entrou mais água no circuito. Qual parâmetro de monitoramento mostra se o programa de MEG continua sob controle?

Resposta: O balanço de água.

**3. [media · inferir]** Um sistema de regeneração entrega MEG com a concentração necessária para reúso, porém o teor de sais no circuito segue alto. O que isso indica sobre o tratamento requerido?

Resposta: Que remover água não basta; a necessidade de remoção de sais deve ser avaliada separadamente.

**4. [dificil · decidir]** Após aumento de carga e ajustes de temperatura e pressão na regeneração, a separação piorou e o consumo de energia subiu. O arranjo havia sido escolhido por ensaios que não representavam a presença de sais, sólidos e hidrocarbonetos do circuito do FPSO. Quanto ao critério de seleção do arranjo, qual decisão técnica é a correta?

Resposta: Reavaliar a alternativa no circuito real; temperatura, pressão e carga afetam separação e energia, e o desempenho de ensaio simplificado não deve ser extrapolado ao arranjo industrial.

## 02_02 · bloco 038 · Função dos químicos no tratamento do gás

Status: `ok`

Exemplos recebidos: arc_challenge:MDSA_2007_5_9 (), mmmlu_ptbr:54 (), pira_ptbr:A1551 (), pira_ptbr:A727 (), mmmlu_ptbr:74 (), qasc:3G5F9DBFOPW5WBD6LBY5LQR498FHVQ ()

**1. [facil · recordar]** Qual é a função do sequestrante de H2S no tratamento do gás?

Resposta: Consumir ou imobilizar a espécie sulfídrica.

**2. [media · comparar]** Mantendo a mesma corrente e os mesmos equipamentos, a ameaça dominante muda de gases ácidos para corrosão por fase aquosa. Qual serviço químico passa a ser prioritário?

Resposta: Inibidor de corrosão.

**3. [media · decidir]** Em uma corrente de gás, o requisito principal é reduzir CO2 antes da exportação, sem hidrato como ameaça dominante. Que classe de produto deve ser selecionada?

Resposta: Solvente de absorção, como alcanolamina.

**4. [dificil · decidir]** Em um FPSO, o gás úmido entra em um trecho frio com risco de hidrato. Mais adiante, outro subsistema apresenta tendência persistente a espuma. Para simplificar a operação, sugerem usar um único químico na mesma corrente, na mesma concentração e no mesmo ponto de injeção para os dois problemas. Qual decisão técnica é coerente?

Resposta: Não. O tratamento deve ser segregado por ameaça dominante: MEG no trecho com risco de hidrato e antiespumante onde há espuma, sem exigir mesma corrente, concentração ou ponto de injeção.

## 02_02 · bloco 041 · Compatibilidade química: por que a combinação pode melhorar ou piorar a proteção

Status: `ok`

Exemplos recebidos: arc_challenge:Mercury_SC_415079 (), mmmlu_ptbr:44 (), mmmlu_ptbr:95 (), pira_ptbr:A1081 (), qasc:3UJ1CZ6IZHODOQC7QESRL647MJV5SM (), pira_ptbr:A1617 ()

**1. [facil · recordar]** De que depende o efeito da combinação de químicos sobre a proteção anticorrosiva?

Resposta: Da formulação e do meio em que os produtos atuam.

**2. [media · diagnosticar]** Em um cupom de aço carbono, a cobertura superficial do inibidor de corrosão cai após adicionar um inibidor de incrustação; pH e fluido permanecem estáveis, e não há sólidos. Que interação explica a perda de proteção?

Resposta: Competição de adsorção entre os produtos na superfície.

**3. [media · decidir]** Para qualificar a mistura de dois químicos para um vaso do FPSO, o laboratório pretende usar as doses de campo, porém com material metálico diferente e um fluido simplificado. Esse ensaio atende ao critério de aplicabilidade ao serviço?

Resposta: Não; precisa usar concentrações, materiais e fluido representativos do serviço.

**4. [dificil · decidir]** Um fornecedor afirma que um inibidor de corrosão e um sequestrante de H2S podem ser dosados juntos porque cada produto já funciona bem isoladamente. Para liberar a aplicação, a equipe planeja apenas um ensaio em aço carbono usando solução de NaCl, embora o serviço real envolva água produzida multissalina e materiais específicos do sistema. Qual decisão técnica é correta?

Resposta: Não liberar; a compatibilidade não pode ser presumida pela função dos produtos e deve ser testada com concentrações, materiais e fluido representativos, pois NaCl sozinho não reproduz a água produzida multissalina.

## 02_02 · bloco 044 · Alternativas ao squeeze para controle de incrustação

Status: `ok`

Exemplos recebidos: mmmlu_ptbr:90 (), arc_challenge:Mercury_406916 (), qasc:3B4YI393V9VEUSAI2A5ZEHEZNKNSSG (), mmmlu_ptbr:97 (), pira_ptbr:B2047 (), pira_ptbr:A1032 ()

**1. [facil · recordar]** Como é feita a remoção seletiva na alternativa preventiva contra BaSO4 e SrSO4?

Resposta: Por membranas adequadas ao serviço.

**2. [media · inferir]** Em um sistema no qual a precipitação de BaSO4 e SrSO4 depende do sulfato trazido pela água injetada, o que se espera se essa espécie for reduzida antes da injeção?

Resposta: A tendência de incrustação diminui e pode até ser eliminada, porque a condição necessária para a precipitação é reduzida.

**3. [media · decidir]** Um campo terá custos recorrentes de inibição e histórico de paradas por incrustação. Ao comparar essa estratégia com a retirada de sulfato para toda a vida do campo, que critério deve orientar a escolha?

Resposta: Um estudo de viabilidade técnico-econômica, comparando investimento inicial e O&M com custos recorrentes de inibição e perdas por parada de produção.

**4. [dificil · decidir]** Num campo em que a incrustação vem do sulfato da água de injeção, a análise preliminar indica menor investimento inicial se a retirada de sulfato for trocada por inibidor levado ao reservatório com propante em frac-pack. Os testes só confirmaram chegada do produto, sem demonstrar distribuição, liberação ao longo do tempo nem compatibilidade. Na seleção da estratégia, qual decisão técnica deve prevalecer?

Resposta: Não considerar essa opção substituta equivalente da retirada de sulfato até validar distribuição, liberação e compatibilidade.

## 02_02 · bloco 047 · Segregação e compatibilidade entre produtos químicos

Status: `ok`

Exemplos recebidos: pira_ptbr:B2402 (), arc_challenge:ACTAAP_2010_7_1 (), mmmlu_ptbr:48 (), pira_ptbr:A1620 (), qasc:3EKVH9QMEY3FN4A2B5V4S0FVP3OD2B (), mmmlu_ptbr:3 ()

**1. [facil · recordar]** Qual é a finalidade da segregação entre produtos químicos incompatíveis?

Resposta: Impedir contato não intencional e evitar perda de desempenho por reação paralela.

**2. [media · inferir]** Em um sistema de tratamento de água, cloro residual chega ao ponto de dosagem de bissulfito por contaminação cruzada. Qual efeito operacional isso tende a causar?

Resposta: O cloro residual consome o bissulfito antes da função principal, elevando a demanda química e podendo mascarar falhas de tratamento.

**3. [media · decidir]** Um novo químico será aplicado na mesma linha de injeção logo após outro produto já em uso. Antes de liberar a sequência, o que deve ser verificado?

Resposta: A compatibilidade entre os químicos para uso conjunto ou sequencial na linha.

**4. [dificil · diagnosticar]** Após uma limpeza com alvejante clorado, a mangueira é retornada ao serviço sem flushing e depois conectada a um circuito com limpador ácido. Minutos após o início, surge liberação gasosa na área. Qual diagnóstico explica o evento e que falha de segregação o permitiu?

Resposta: Mistura residual de alvejante clorado com limpador ácido, gerando nuvem gasosa tóxica; faltou flushing compatível na troca entre produtos incompatíveis.

## 02_02 · bloco 050 · Monitoramento do armazenamento e consequências operacionais

Status: `ok`

Exemplos recebidos: arc_challenge:Mercury_7145495 (), mmmlu_ptbr:64 (), mmmlu_ptbr:24 (), pira_ptbr:A249 (), pira_ptbr:B2479 (), qasc:3MX2NQ3YC9TLK7Y6KOYEKELZO5E5XC ()

**1. [facil · recordar]** Além do volume no tanque, que tipo de condição o monitoramento do armazenamento deve verificar?

Resposta: Condições que antecedem falhas de segurança, corrosão ou perda de desempenho.

**2. [media · inferir]** Um tanque de água produzida permanece acumulando fluido e há possibilidade de atividade microbiológica. Que combinação de recursos se torna relevante no armazenamento e manuseio?

Resposta: Facilidades para monitorar H2S e para aplicar biocidas.

**3. [media · decidir]** Num sistema de injeção com corrosividade variando ao longo da operação, qual abordagem de monitoramento é adequada para acompanhar essas mudanças?

Resposta: Técnicas eletroquímicas, como par galvânico e resistência à polarização.

**4. [dificil · diagnosticar]** Em uma FPSO, as oscilações usuais de vazão, pressão e composição continuam dentro do padrão. Ainda assim, a separação a jusante perde eficiência e surge espuma inesperada. No sistema de químicos, o consumo segue a dosagem planejada, porém o produto estocado mudou de cor e a resposta do processo piorou. Qual problema no químico é o diagnóstico mais consistente?

Resposta: Degradação do produto armazenado, pela alteração de cor com perda de resposta apesar da mesma dosagem.

## 02_02 · bloco 053 · Seleção do ponto de medição, automação e confiabilidade dos dados

Status: `ok`

Exemplos recebidos: arc_challenge:Mercury_SC_408415 (), pira_ptbr:A1854 (), pira_ptbr:A1196 (), mmmlu_ptbr:73 (), mmmlu_ptbr:134 (), qasc:3U4J9857OEATU89O3LLTT183VOT7BN ()

**1. [facil · recordar]** No ajuste automático de dosagem, o que tende a diminuir em relação à operação manual?

Resposta: A variabilidade humana.

**2. [media · inferir]** Em um FPSO, a dosagem automática de dispersante reduziu a diferença entre turnos. A equipe quer abolir calibração do sensor e checagens de laboratório. O que ainda deve ser mantido para confiar no ajuste?

Resposta: Validação periódica, manutenção do sensor e reconciliação com análises laboratoriais.

**3. [media · diagnosticar]** A vazão do processo e a taxa de injeção ficaram estáveis, mas o sinal on-line passou a oscilar após intervenção elétrica no skid. Que causa metrológica deve ser investigada primeiro?

Resposta: Falha de aterramento e ruído elétrico no sinal do sensor.

**4. [dificil · diagnosticar]** Na água produzida de um FPSO, o controle automático de hipoclorito usa sensor logo após a injeção. O sinal entra em picos e vales rápidos, mas amostras mais adiante mostram residual estável e a bomba dosadora está normal. Com mistura incompleta e água livre intermitente, qual é a causa mais provável desse ciclo de correções?

Resposta: Medição não representativa no ponto escolhido: mistura incompleta, atraso entre injeção e leitura e segregação de fases/água livre geram falsos desvios.

## 02_02 · bloco 056 · Leitura temporal, pH e resposta corrosiva

Status: `ok`

Exemplos recebidos: pira_ptbr:A1743 (), mmmlu_ptbr:127 (), pira_ptbr:A143 (), qasc:3KB8R4ZV1E6CN1KPWOPNZELWW6TBG7 (), mmmlu_ptbr:74 (), arc_challenge:Mercury_402569 ()

**1. [facil · recordar]** Qual é a principal vantagem da leitura temporal no acompanhamento da corrosão?

Resposta: Permitir correlacionar a corrosão com variáveis operacionais que mudam durante a operação.

**2. [media · inferir]** Em um meio aquoso suscetível à corrosão ácida, o pH cai durante uma perturbação operacional, sem outras mudanças relevantes. Que efeito se espera na taxa de perda metálica ao longo do tempo?

Resposta: Ela tende a aumentar, porque a acidificação pode favorecer maior taxa corrosiva.

**3. [media · decidir]** Uma correlação entre queda de pH e aumento de perda metálica foi observada em um sistema. Em outro, mudam a metalurgia e o regime de escoamento. Essa correlação pode ser aplicada diretamente como regra?

Resposta: Não. A sensibilidade da resposta depende dessas condições, então a correlação de um sistema não é universal.

**4. [dificil · decidir]** Em uma linha com fase aquosa, temperatura, composição do fluido e regime de escoamento estáveis, surgem quedas curtas de pH durante partidas. A sonda RE mostra aumento sustentado da inclinação da perda de espessura após essas quedas, mas a curva acumulada não repete cada vale de pH ponto a ponto. Qual variável deve ser priorizada no ajuste para conter o dano?

Resposta: O pH, ou a causa da acidificação; a curva da sonda RE é cumulativa e por isso não replica instantaneamente a curva de pH.
