# Questões geradas

## 01_01 · bloco 000 · Indicadores de monitoramento operacional: detecção de desvios e diagnóstico

Status: `ok`

Exemplos recebidos: PQ-04_01-07 (dificil), PQ-02_10-05 (media), PQ-07_01-03 (facil)

**1. [facil · recordar]** Em topsides de FPSO, o que um indicador de desempenho representa em relação à variável de processo?

Resposta: Ele resume o efeito da variável sobre o desempenho e não substitui a própria variável de processo.

**2. [facil · recordar]** Depois que um KPI aponta um desvio em uma unidade de processo, o que ele ajuda a identificar para orientar o diagnóstico?

Resposta: As variáveis perturbadas.

**3. [media · inferir]** Uma unidade passará a operar com especificações mais restritas e maior exigência de segurança. Ao decidir por uma ferramenta online de KPI, que vantagem operacional se torna decisiva?

Resposta: Avaliar condições operacionais em tempo próximo do real, ajudando a manter especificação, detectar operação anormal e antecipar anormalidades.

**4. [dificil · decidir]** Durante aumento de carga no topsides de um FPSO, um KPI de tratamento piora por alguns minutos. No mesmo intervalo, a variável de especificação do produto segue conforme, houve alteração da estratégia de controle e o histórico recente não mostra deterioração persistente. Qual decisão de diagnóstico é a correta?

Resposta: Tratar o desvio do KPI como sintoma a contextualizar com processo e histórico; ele não basta para concluir nem saída de especificação nem perda estrutural de desempenho.

## 01_01 · bloco 001 · O que são KPIs e como a finalidade muda sua definição

Status: `ok`

Exemplos recebidos: PQ-09_01-04 (media), PQ-04_02-03 (facil), PQ-03_02-08 (dificil)

**1. [facil · recordar]** O que um KPI avalia em um processo industrial?

Resposta: A eficiência e o desempenho do processo, por meio de uma métrica.

**2. [facil · recordar]** Em uma planta de produção, um KPI precisa representar a instalação inteira?

Resposta: Não; ele pode avaliar um equipamento, uma etapa específica ou a instalação como um todo.

**3. [media · inferir]** Após implantar KPIs em um FPSO, a gerência assume que a unidade elevará a capacidade sem grandes investimentos em qualquer condição operacional. Essa conclusão procede?

Resposta: Não; KPIs ajudam a identificar deficiências e apoiar ações para reduzir custos ou elevar capacidade, mas não garantem esses ganhos em qualquer condição operacional.

**4. [dificil · diagnosticar]** Um FPSO passou a mostrar na sala de controle um indicador agregado, criado para revisão gerencial mensal do consumo energético. Durante oscilações de carga, os operadores querem usá-lo para ajustar a operação minuto a minuto sem redefinir a métrica. Qual é o problema técnico principal dessa decisão?

Resposta: A métrica deixa de ser coerente com a decisão operacional em tempo real; ao mudar a finalidade de gerencial para operação imediata, o mesmo processo pode exigir outro KPI.

## 01_01 · bloco 002 · Denominador, base de exposição e comparabilidade

Status: `ok`

Exemplos recebidos: PQ-07_04-04 (media), PQ-09_02-09 (dificil), PQ-08_03-02 (facil)

**1. [facil · recordar]** Numa taxa de frequência de acidentes ocupacionais, o que o numerador representa?

Resposta: A quantidade de casos enquadrados pela definição adotada.

**2. [media · inferir]** Num FPSO, o consumo absoluto de energia subiu após aumento da carga processada no mês. Sem normalização por uma base de referência adequada, o que esse aumento não permite concluir sobre o desempenho da unidade?

Resposta: Não permite concluir piora do desempenho intrínseco; o aumento pode refletir apenas maior carga ou volume processado.

**3. [media · decidir]** Em um FPSO cuja vazão varia bastante entre meses, que tipo de base no denominador torna mais comparável um indicador intensivo de energia entre períodos?

Resposta: Uma base por unidade produzida, isto é, consumo de energia por unidade produzida.

**4. [dificil · comparar]** Em um FPSO, a taxa de frequência de acidentes com afastamento caiu de um trimestre para outro. No segundo, o denominador passou a considerar apenas horas-homem da tripulação própria, excluindo contratados, e um tipo de ocorrência antes excluído passou a entrar na definição do caso. Essa queda sustenta comparação temporal válida do desempenho de segurança?

Resposta: Não. Mudaram a base de horas-homem e o critério de enquadramento; sem compatibilidade entre eles, a comparação da taxa não é consistente.

## 01_01 · bloco 004 · Dependabilidade e seus atributos centrais

Status: `ok`

Exemplos recebidos: PQ-09_02-06 (media), PQ-03_02-08 (dificil), PQ-10_01-02 (facil)

**1. [facil · recordar]** Que conceito reúne os atributos que sustentam a confiança no serviço prestado por um sistema?

Resposta: Dependabilidade.

**2. [facil · comparar]** Mantido o sistema operacional no início do período, qual atributo avalia a continuidade do serviço correto ao longo do tempo, e não apenas em um instante?

Resposta: Confiabilidade.

**3. [media · inferir]** Dois equipamentos críticos têm a mesma frequência de falhas e o mesmo tempo de reparo ativo por evento. Em um deles, mobilização, acesso e liberação para retorno demoram mais. Qual atributo tenderá a ficar pior nesse equipamento?

Resposta: A disponibilidade operacional, porque a indisponibilidade total aumenta com os tempos logísticos e administrativos.  
_usa apoio_

**4. [dificil · diagnosticar]** Em um FPSO, um compressor crítico quase não apresenta falhas funcionais, mas entra repetidamente em parada automática quando a proteção detecta condição de risco. Cada evento exige inspeção e liberação antes do retorno, reduzindo a produção. Sem aumento relevante na contagem de falhas, o que explica tecnicamente a piora do desempenho global?

Resposta: A disponibilidade foi reduzida pelas retiradas de serviço por proteção e pelas condições de retorno; segurança e integridade limitaram a continuidade operacional mesmo sem mais falhas registradas.

## 01_01 · bloco 005 · Disponibilidade: o que é e por que depende de falha e reparo

Status: `ok`

Exemplos recebidos: PQ-07_01-03 (facil), PQ-04_01-06 (media), PQ-05_01-07 (dificil)

**1. [facil · recordar]** Em estado estacionário, que razão representa a disponibilidade?

Resposta: Uptime dividido pelo tempo total observado.

**2. [media · comparar]** No mesmo período e para o mesmo equipamento, um KPI conta só a intervenção técnica; outro soma também diagnóstico, mobilização, espera por sobressalentes, acesso e liberação. Qual KPI tende a resultar em menor disponibilidade?

Resposta: O de disponibilidade operacional, por incorporar toda a indisponibilidade do evento e não só a intervenção técnica.

**3. [media · inferir]** Sem medições diretas de uptime e downtime, um sistema reparável passa a falhar menos, mas o tempo médio de reparo permanece igual. Pela aproximação com médias de falha e reparo, para que lado vai a disponibilidade?

Resposta: Tende a aumentar, porque a menor frequência de falhas eleva o MTBF.

**4. [dificil · decidir]** Um módulo reparável apresenta falhas frequentes. Cada evento tem 2 h de reparo ativo e 14 h de diagnóstico, mobilização, acesso, espera por sobressalente, liberação e retorno seguro. Sem dados diretos de uptime/downtime, a equipe quer elevar a disponibilidade operacional. Qual variável tem maior alavanca: a associada à frequência das falhas ou a ligada apenas à intervenção ativa?

Resposta: A ligada ao MTBF, porque reduzir a frequência das falhas elimina todo o tempo indisponível de cada evento.

## 01_01 · bloco 006 · Redundância, standby e efeitos sobre o comportamento do sistema

Status: `ok`

Exemplos recebidos: PQ-07_04-07 (dificil), PQ-06_01-04 (media), PQ-03_01-01 (facil)

**1. [facil · recordar]** Na configuração com reserva fria, o equipamento reserva fica imune a falhas enquanto espera entrar em serviço?

Resposta: Não. A menor carga pode reduzir desgaste, mas continuam possíveis falhas em espera e falhas de partida ou de comutação.

**2. [media · inferir]** Em um arranjo redundante de um FPSO, a unidade reserva está disponível, mas os equipamentos ativos acumulam degradação ao longo de uma campanha longa. Qual é o efeito esperado sobre o ganho de confiabilidade e disponibilidade trazido pela redundância?

Resposta: O ganho tende a diminuir; em tempos mais longos, a degradação dos equipamentos ativos pode deixar de ser compensada pela reserva.

**3. [media · inferir]** Um sistema do FPSO tem dois equipamentos redundantes, mas um deles está isolado para manutenção programada. Durante esse período, o que acontece com a proteção oferecida pela redundância contra perda da função?

Resposta: Ela fica reduzida; a redundância não elimina indisponibilidade causada por manutenção.

**4. [dificil · decidir]** Em um FPSO, dois trens de tratamento foram duplicados e cada um tem seu próprio equipamento principal. Porém ambos descarregam para a mesma linha limitante e dependem do mesmo sistema de controle; quando esse ponto comum satura ou bloqueia, a produção cai mesmo com um trem íntegro. Para avaliar o desempenho, essa duplicação deve ser tratada como redundância plena ou como ganho real limitado?

Resposta: Como ganho real limitado, porque a redundância útil é a que preserva a função de processo relevante; o ponto compartilhado reduz o benefício que uma lógica série-paralelo simplificada sugeriria.

## 01_01 · bloco 007 · Como selecionar, modelar e atualizar análises RAM

Status: `ok`

Exemplos recebidos: PQ-10_01-02 (facil), PQ-04_02-04 (media), PQ-05_02-07 (dificil)

**1. [facil · recordar]** Em etapas preliminares de projeto, para que servem modelos RAM mais simples?

Resposta: Validar o arranjo, a quantidade de equipamentos e as alternativas de redundância.

**2. [media · inferir]** Duas unidades têm a mesma função, mas diferem em arquitetura, acessibilidade e estratégia de manutenção. Se a análise RAM usar os mesmos tempos de reparo e frequências de falha para ambas, qual efeito se espera nas previsões?

Resposta: Resultados imprecisos de disponibilidade e confiabilidade, porque esses parâmetros variam com a arquitetura, a acessibilidade, a manutenção e o contexto operacional de cada unidade.

**3. [dificil · decidir]** No estudo conceitual de um FPSO, um modelo RAM simplificado indicou equivalência entre duas alternativas de compressão. No detalhamento, uma delas passou a incluir dependências entre subsistemas e mais de um modo de operação. Antes de decidir a arquitetura, que tratamento analítico é tecnicamente necessário?

Resposta: Usar um modelo mais completo, que represente explicitamente dependências e modos de operação, para comparar as alternativas e refinar a previsão de disponibilidade e confiabilidade.

**4. [media · diagnosticar]** A equipe reuniu histórico de falhas e tempos de reparo confiáveis, mas o modelo não representa a lógica funcional do sistema. Qual consequência direta isso traz para a análise RAM?

Resposta: A análise passa a representar mal as perdas do sistema, comprometendo as previsões de disponibilidade e confiabilidade.

## 01_01 · bloco 008 · Coleta de dados, indicadores e monitoramento do desempenho real

Status: `ok`

Exemplos recebidos: PQ-06_03-01 (facil), PQ-03_02-08 (dificil), PQ-04_01-06 (media)

**1. [facil · recordar]** Quais dois marcos de tempo permitem calcular MTTR e disponibilidade observada de um item?

Resposta: O tempo de início da falha e o tempo de retorno ao estado operacional.

**2. [media · inferir]** Em um FPSO, falhas e reparos do mesmo sistema são registrados por áreas diferentes com causas genéricas, sem separar mecanismos de falha. Ao definir ações corretivas, o que esse modo de coleta compromete?

Resposta: Compromete a priorização das ações corretivas, porque os registros não permitem identificar com precisão as causas tratáveis.

**3. [media · comparar]** No mesmo período de monitoramento, o Elemento A falhou mais vezes, mas sua parada não afeta a produção por redundância. O Elemento B falhou menos, porém sua indisponibilidade interrompe a exportação. Qual é o limitante mais relevante do desempenho?

Resposta: O Elemento B, porque sua criticidade funcional ao bloquear a exportação pesa mais que a maior frequência de falhas do A.

**4. [dificil · decidir]** Na revisão de desempenho de um FPSO, há um banco setorial consolidado e quatro anos de registros próprios. Os registros da unidade estão em sistemas diferentes, com padronização inconsistente entre áreas, mas o objetivo é representar as condições locais e priorizar correções. Qual deve ser a prioridade analítica?

Resposta: Priorizar os dados da própria unidade, após padronização e gestão eletrônica dos registros; o banco setorial deve ficar como apoio para padronização e comparação.

## 01_01 · bloco 010 · Interações com segurança, manutenção e recursos de suporte

Status: `ok`

Exemplos recebidos: PQ-03_02-08 (dificil), PQ-05_01-02 (facil), PQ-06_01-04 (media)

**1. [facil · recordar]** Que elementos automáticos do sistema podem parar a produção para evitar eventos mais graves?

Resposta: Intertravamentos e funções de proteção.

**2. [media · inferir]** Em um FPSO, pretende-se aumentar a disponibilidade reduzindo intervenções preventivas programadas. Antes de aprovar a mudança, o que precisa ser avaliado?

Resposta: O impacto da redução sobre risco e integridade.

**3. [media · inferir]** Após uma falha, o equipamento aguarda acesso à área, sobressalente crítico e janela logística. A gerência adiciona mais técnicos de manutenção. Qual tende a ser o efeito no retorno operacional?

Resposta: Limitado; o gargalo continua nas esperas por acesso, sobressalente e logística, não na quantidade de técnicos.

**4. [dificil · diagnosticar]** Em uma semana, quatro falhas ocorrem em subsistemas diferentes do FPSO. Há acesso, sobressalentes e liberações disponíveis, mas apenas um time especializado atende essas falhas. O tempo total indisponível cresce embora cada reparo mantenha sua duração usual. Qual mecanismo operacional explica esse aumento?

Resposta: Formação de fila de reparos por limitação do atendimento especializado.

## 01_01 · bloco 011 · Como o processamento primário condiciona a capacidade da unidade

Status: `ok`

Exemplos recebidos: PQ-03_03-04 (media), PQ-07_05-02 (facil), PQ-04_01-07 (dificil)

**1. [facil · recordar]** Para que a água produzida pode ser reinjetada em uma unidade marítima?

Resposta: Para auxiliar a produção de óleo.

**2. [media · inferir]** Um compressor do processamento primário opera abaixo da eficiência esperada e a qualidade do fluido separado começa a cair. Para manter especificações e estabilidade operacional, o que tende a acontecer com a produção?

Resposta: A produção tende a ser reduzida para manter as especificações e a estabilidade operacional.

**3. [media · decidir]** Separação e tratamento ainda têm folga, mas a movimentação de uma das correntes já atingiu o limite. Mantidas as demais condições, a unidade consegue elevar a produção sem criar nova restrição?

Resposta: Não. A capacidade produtiva continua limitada pela capacidade combinada de separação, tratamento e movimentação dos fluxos.

**4. [dificil · decidir]** A vazão de água produzida aumenta, e a malha de água produzida perde capacidade. A reinjeção já está no limite e o tratamento para descarte no mar também, enquanto óleo e gás ainda poderiam ser processados. Para manter descarte aceitável e operação estável, qual decisão operacional passa a ser necessária?

Resposta: Reduzir a vazão total do campo, porque falta capacidade para separar, tratar, reinjetar ou descartar a fase aquosa gerada com os hidrocarbonetos.

## 01_01 · bloco 012 · Seleção e aplicação de medidas para prevenir ou aliviar gargalos

Status: `ok`

Exemplos recebidos: PQ-07_01-03 (facil), PQ-05_01-07 (dificil), PQ-03_03-04 (media)

**1. [facil · recordar]** O que determina, em termos gerais, a escolha da ação para tratar uma limitação de capacidade?

Resposta: Ela é determinada por onde está a limitação e pelo horizonte que se deseja atacar.

**2. [facil · comparar]** Qual é a diferença funcional entre medida preventiva e medida corretiva em restrições de capacidade?

Resposta: A preventiva age antes da perda para reduzir a probabilidade do problema; a corretiva atua depois que a restrição já compromete a capacidade.

**3. [media · inferir]** Em um projeto offshore, o risco de incrustação é alto e o gerenciamento previsto é complexo, mas ainda não houve perda de capacidade. Nesse contexto, por que considerar prevenção já no desenvolvimento?

Resposta: Para reduzir os custos associados às perdas de produção, antecipando o problema conforme o risco e a dificuldade de gerenciamento.

**4. [dificil · diagnosticar]** Após um projeto de debottlenecking, a equipe alterou uma condição operacional a montante, mas a vazão total processada não aumentou e a limitação apenas apareceu em outro ponto do processo. Mantidas as demais condições, que falha de abordagem esse resultado indica?

Resposta: Indica que a variável ou o equipamento limitante não foi aliviado precisamente; a mudança apenas deslocou o gargalo para outro ponto.

## 01_01 · bloco 013 · Consequências operacionais e econômicas das restrições em FPSO

Status: `ok`

Exemplos recebidos: PQ-10_01-01 (facil), PQ-09_02-09 (dificil), PQ-04_01-06 (media)

**1. [facil · recordar]** Se a restrição de produção em um FPSO estiver em um ponto comum do sistema, que tipo de decisão gerencial passa a ser inevitável?

Resposta: Priorização de entregas com alocação da capacidade disponível.

**2. [facil · recordar]** Que efeito operacional do projeto de um FPSO é influenciado por localização, meio ambiente, ancoragem, casco, convés e arranjo de produção e armazenagem?

Resposta: A capacidade de minimizar paradas e problemas entre operações de offloading.

**3. [media · comparar]** Duas interdições de FPSO têm a mesma causa técnica. Na unidade X, o volume produzido e a duração da indisponibilidade são maiores que na Y. Como fica a magnitude da perda econômica em X?

Resposta: Maior, porque depende do volume produzido e da duração da indisponibilidade.

**4. [dificil · diagnosticar]** Um FPSO já opera com vazões redistribuídas entre poços por causa de uma limitação em ponto comum. Ao mesmo tempo, o autodiagnóstico apresenta falhas e as ações contingenciais e corretivas não são executadas no prazo compatível com o risco. Qual desfecho operacional passa a prevalecer sobre a tentativa de manter a produção?

Resposta: Interdição da instalação, por falhas de autodiagnóstico sem ações contingenciais e corretivas no prazo compatível com o risco.

## 01_01 · bloco 015 · Atribuição de causas: do mecanismo físico à perda observada

Status: `ok`

Exemplos recebidos: PQ-04_02-09 (dificil), PQ-07_05-02 (facil), PQ-03_03-04 (media)

**1. [facil · recordar]** Na atribuição de perdas, que elemento corresponde à forma de manifestação da incapacidade de operar?

Resposta: O modo de falha.

**2. [media · inferir]** Em um poço, formou-se incrustação na coluna de produção, aumentando a resistência ao fluxo. Mantidas as demais condições, que efeitos operacionais tendem a ser percebidos?

Resposta: Alteração de pressão observada no poço e queda de vazão bruta.

**3. [media · decidir]** Há uma obstrução por incrustação já formada na coluna e a vazão caiu. Aumentar apenas a dosagem de inibidor de incrustação recupera imediatamente a capacidade perdida?

Resposta: Não. Ele previne ou retarda nova precipitação; a recuperação pode exigir remoção do depósito.

**4. [dificil · diagnosticar]** Após perda de produção, um relatório registra "queda de vazão" como causa raiz. Os dados mostram aumento de resistência ao fluxo na coluna, alteração de pressão no poço, depósito já formado e programa químico descrito só como "ajuste de inibidor". Qual formulação de diagnóstico atribui melhor a causa?

Resposta: Obstrução por incrustação na coluna como mecanismo limitante, com a função do inibidor explicitada; queda de vazão é a consequência, e "ajuste de inibidor" sozinho é inespecífico.

## 01_01 · bloco 016 · Condições que mudam o comportamento do risco no processamento primário

Status: `ok`

Exemplos recebidos: PQ-07_05-06 (media), PQ-04_01-07 (dificil), PQ-06_05-01 (facil)

**1. [facil · recordar]** Que efeito o controle manual que exige atenção excessiva tem sobre o risco de processo?

Resposta: Ele aumenta o risco de processo, porque reduz a margem para detectar e corrigir desvios.

**2. [media · inferir]** Duas unidades recebem a mesma perturbação de processo. Uma tem maior capacidade de segregação, mais inventário intermediário e maior flexibilidade operacional. O que muda no comportamento esperado antes de reduzir carga ou parar?

Resposta: Ela tende a absorver mais a perturbação, chegando mais tarde à redução de carga ou à parada.

**3. [facil · recordar]** Quando a análise de riscos omite cenários plausíveis, o que acontece com o risco de processo?

Resposta: O risco de processo aumenta, porque a análise deixa de considerar desvios plausíveis.

**4. [dificil · decidir]** Uma avaliação concluiu que duas unidades reagirão do mesmo modo a uma perturbação porque têm a mesma designação. Na unidade B, porém, há menos instrumentação útil, menor inventário intermediário e menor flexibilidade operacional. Qual conclusão deve ser rejeitada?

Resposta: A equivalência de capacidade de resposta; no arranjo real, a unidade B absorve menos a perturbação antes de reduzir carga ou parar.

## 01_01 · bloco 017 · Estrutura organizacional, gestão de mudanças e autonomia técnica

Status: `ok`

Exemplos recebidos: PQ-07_04-07 (dificil), PQ-04_01-06 (media), PQ-08_03-02 (facil)

**1. [facil · recordar]** Além das técnicas de análise, de que também depende a gestão de riscos ao longo da vida útil da instalação?

Resposta: Depende de uma estrutura organizacional capaz de sustentar identificação de perigos, análise, atualização documental, gestão de mudanças e esclarecimento rápido de parâmetros de projeto e operação.

**2. [media · inferir]** Em um desvio operacional, a equipe embarcada precisa confirmar parâmetros de projeto antes de ajustar a operação. O suporte técnico está remoto e a documentação disponível não é acessível. Qual consequência isso tende a trazer para a resposta e para a validação da mudança?

Resposta: Tende a aumentar o tempo de resposta, atrasar decisões e dificultar a validação da mudança diante do desvio.

**3. [media · comparar]** Dois arranjos mantêm a mesma instrumentação e os mesmos controles. Em um, a equipe local interpreta o problema, autoriza ações e revisa premissas; no outro, essas funções não têm responsável claro. Em qual arranjo os controles tendem a ser mais efetivos?

Resposta: No arranjo em que essas funções estão claramente atribuídas a quem interpreta o problema, autoriza ações e revisa premissas.

**4. [dificil · diagnosticar]** Num FPSO, as condições operacionais mudam ao longo da campanha e exigem reavaliações frequentes. Os procedimentos existem, mas áreas operam com pouca troca de informação, surgem interpretações diferentes sobre parâmetros de operação e a atualização documental atrasa. Qual fragilidade organizacional melhor explica a perda de robustez do sistema de gestão nesse contexto?

Resposta: Comunicação contínua insuficiente, associada a fatores humanos e culturais, reduz a robustez e a resiliência do sistema de gestão quando o risco é dinâmico.

## 01_01 · bloco 018 · Monitoramento, revisão e aprendizagem para próximas intervenções

Status: `ok`

Exemplos recebidos: PQ-04_02-03 (facil), PQ-02_10-05 (media), PQ-10_01-07 (dificil)

**1. [facil · recordar]** Na gestão de paradas de um FPSO, qual documento consolida objetivo, escopo, prazos planejados e realizados, custos, desvios e lições aprendidas?

Resposta: O relatório final da parada.

**2. [media · inferir]** Depois de uma parada, o registro mostrou que o plano subestimou a complexidade e que foram necessários suportes não previstos. No próximo orçamento do ciclo de vida, que ajuste deve ser feito?

Resposta: As estimativas devem incorporar a complexidade real e os recursos de suporte efetivamente necessários.

**3. [media · decidir]** Em uma intervenção, o histórico consolidado mostrou quais atividades concentraram maior exposição a desvios relevantes. Para a próxima parada, qual critério de ordenação das ações deve ser revisto com base nesse aprendizado?

Resposta: A priorização por risco.

**4. [dificil · diagnosticar]** Uma unidade mantém cultura de segurança e monitoramento sistemático entre paradas. Mesmo assim, repetiu na última intervenção a mesma falha organizacional já vista antes. Os registros anteriores foram preenchidos e arquivados, mas não geraram revisão das decisões nem uso das lições no planejamento seguinte. O que explica essa repetição?

Resposta: Faltou transformar o registro em aprendizado efetivo, com disciplina documental e análise crítica real; o preenchimento formal sozinho não evita repetir falhas organizacionais.

## 01_01 · bloco 019 · Seleção de sistemas críticos e uso de histórico de falhas

Status: `ok`

Exemplos recebidos: PQ-07_04-04 (media), PQ-02_10-07 (dificil), PQ-09_01-02 (facil)

**1. [facil · recordar]** Qual é a função da identificação de componentes e sistemas críticos na gestão de risco da unidade?

Resposta: Orientar a implantação e a atualização dos controles de risco, priorizando as funções que merecem tratamento.

**2. [facil · recordar]** Na seleção de sistemas críticos, para que o histórico de falhas pode ser usado na análise?

Resposta: Para formular hipóteses de falha.

**3. [media · inferir]** Duas FPSOs compartilham acidentes passados semelhantes, mas têm configuração, regime operacional, manutenção e barreiras diferentes. Ao priorizar sistemas críticos da segunda unidade, o histórico da primeira pode virar ranking pronto?

Resposta: Não. A criticidade depende dessas condições da unidade; o histórico apenas informa a análise da instalação real.

**4. [dificil · decidir]** Após revisar eventos de outras unidades, a equipe quer encerrar a seleção de sistemas críticos copiando apenas o que mais falhou. Na FPSO atual, porém, separação, medição e tratamento têm funções sensíveis pelo arranjo da unidade. Qual decisão é tecnicamente correta para fechar a priorização?

Resposta: Combinar o aprendizado do histórico com exame específico das funções e vulnerabilidades da FPSO; o que mais falhou em outras unidades não substitui a avaliação local.

## 01_01 · bloco 021 · Confiabilidade, disponibilidade e suporte de manutenção

Status: `ok`

Exemplos recebidos: PQ-03_01-01 (facil), PQ-07_04-07 (dificil), PQ-06_01-04 (media)

**1. [facil · recordar]** Qual propriedade expressa a capacidade de um item cumprir a função requerida, sob condições especificadas, durante um intervalo de tempo?

Resposta: Confiabilidade.

**2. [media · inferir]** Um equipamento tem boa confiabilidade e é reparável rapidamente, mas o sobressalente crítico e o apoio externo não estão assegurados. Quando ele for requerido, que atributo tende a ficar comprometido?

Resposta: A disponibilidade, porque ela também depende do suporte de manutenção e dos recursos externos necessários estarem assegurados.

**3. [dificil · decidir]** Em um FPSO, duas intervenções podem ser adiadas. Os dois itens têm probabilidade de falha semelhante, mas um deles, se perder a função, só pode ser restaurado com especialista mobilizado de terra, peça não embarcada e janela logística restrita. Para esse item, qual decisão é tecnicamente mais prudente?

Resposta: Priorizar a intervenção, porque o tempo e os meios para restaurar a função elevam o impacto da indisponibilidade.

**4. [media · diagnosticar]** O operador recebe históricos de falha e manutenção em formatos incompatíveis de fabricantes e prestadores. Que entrega da engenharia de confiabilidade está faltando para melhorar essa troca de informação?

Resposta: A organização dos dados de confiabilidade e manutenção em formato padronizado para troca entre as partes.

## 01_01 · bloco 022 · Consequências econômicas de controles insuficientes

Status: `ok`

Exemplos recebidos: PQ-07_05-06 (media), PQ-04_01-07 (dificil), PQ-09_01-02 (facil)

**1. [facil · recordar]** Além da segurança e da conformidade, qual dimensão do negócio também é afetada pela decisão de controlar riscos?

Resposta: O custo ao longo da vida útil do ativo.

**2. [media · inferir]** Em um FPSO, um sistema não detecta sua própria falha, a resposta contingencial não funciona e a correção aplicada fica aquém do risco. Qual consequência operacional-econômica pode resultar?

Resposta: Interdição da instalação, com perda relevante de receita.

**3. [facil · recordar]** Após uma parada forçada, qual impacto indireto pode exigir reorganizar transporte, suprimento e apoio à unidade?

Resposta: Replanejamento logístico.

**4. [dificil · decidir]** Uma equipe quer adiar um controle preventivo usando apenas o custo observado numa falha passada de outro FPSO. A unidade atual tem duração provável de parada, capacidade produtiva, escopo corretivo e contexto contratual diferentes. Como essa decisão deve ser tratada economicamente?

Resposta: Não basta usar esse exemplo; a avaliação deve considerar os parâmetros da unidade e o efeito acumulado de indisponibilidade, correções emergenciais e restrições operacionais.

## 01_01 · bloco 023 · Análise de causa: mecanismo de falha, modo de falha e FMEA

Status: `ok`

Exemplos recebidos: PQ-10_01-02 (facil), PQ-05_02-07 (dificil), PQ-03_01-05 (media)

**1. [facil · recordar]** Em abordagens que usam o NPR, como esse índice é calculado?

Resposta: Pelo produto das classificações de severidade, ocorrência e detecção.

**2. [media · comparar]** Na análise de uma perda de função, a equipe registra “corrosão interna” e “vazamento externo”. Qual deles é o mecanismo e qual é o modo de falha?

Resposta: Corrosão interna é o mecanismo; vazamento externo é o modo de falha.

**3. [media · decidir]** Uma equipe inicia a FMEA, mas cada disciplina usa critérios próprios, os dados históricos não têm origem verificável e não há alinhamento sobre a função do sistema. O que precisa ser estabelecido antes de prosseguir?

Resposta: Critérios definidos, dados rastreáveis e entendimento comum das funções analisadas.

**4. [dificil · decidir]** Dois modos de falha receberam o mesmo NPR. No primeiro, a consequência potencial é crítica, embora a ocorrência seja baixa; no segundo, a severidade é menor, mas ocorrência e detecção levaram ao mesmo produto. Ao priorizar ações, qual decisão analítica é correta?

Resposta: Usar o NPR apenas para triagem e analisar separadamente a consequência crítica do primeiro caso, porque combinações diferentes podem gerar o mesmo NPR.

## 02_02 · bloco 000 · Como selecionar e aplicar: bottle test como triagem empírica

Status: `ok`

Exemplos recebidos: PQ-05_01-02 (facil), PQ-07_04-07 (dificil), PQ-04_02-04 (media)

**1. [facil · recordar]** No bottle test, qual é a função técnica da amostra sem aditivo?

Resposta: Servir de referência para a separação natural da emulsão, permitindo comparar o efeito dos produtos testados.

**2. [media · inferir]** Em uma triagem, duas garrafas receberam produtos diferentes, mas uma foi testada em temperatura mais alta e com mistura mais intensa. O que fica comprometido nessa comparação?

Resposta: Fica comprometida a atribuição da diferença de desempenho ao produto ou à dosagem, porque temperatura e mistura deveriam estar controladas.

**3. [media · comparar]** Mantidas iguais a temperatura, a mistura, a concentração do produto e o tempo de observação, o que muda no critério de avaliação entre emulsões água-em-óleo e óleo-em-água?

Resposta: Em água-em-óleo, avalia-se a liberação da água dispersa do petróleo; em óleo-em-água, a clarificação da fase aquosa.

**4. [dificil · diagnosticar]** Um desemulsificante foi selecionado em bottle test porque liberou água rapidamente em bancada. No FPSO, a injeção ocorre antes de bombas e válvulas, o tempo de residência é menor que no ensaio e a composição do fluido varia; no teste operacional, o ganho não se confirma. Qual diagnóstico técnico explica melhor a divergência?

Resposta: O ensaio de bancada não representou adequadamente as condições relevantes do processo; cisalhamento, residência e composição real alteraram o desempenho, por isso a seleção exige validação operacional.  
_usa apoio_

## 02_02 · bloco 003 · Por que pH, salmoura, petróleo e asfaltenos mudam o desempenho

Status: `ok`

Exemplos recebidos: PQ-06_01-04 (media), PQ-01_01-03 (facil), PQ-07_04-07 (dificil)

**1. [facil · recordar]** Que efeito de asfaltenos e sólidos ao redor das gotas tende a impedir a coalescência?

Resposta: A formação de filmes interfaciais resistentes em torno das gotas.

**2. [media · inferir]** Em um teste representativo do FPSO, as gotas entram em contato, mas a drenagem entre elas é lenta e a coalescência quase não avança. Que ação do aditivo pode destravar a separação?

Resposta: Modificar a organização do filme interfacial para facilitar a drenagem entre gotas em contato.

**3. [media · inferir]** Ao levar um desemulsificante para outro fluido, os novos testes usam pH mais baixo e salinidade maior. Que conclusão sobre a separação não pode ser assumida só por essas mudanças?

Resposta: Que a separação necessariamente melhorará; esse efeito depende da formulação e do fluido.

**4. [dificil · decidir]** Num FPSO, um fornecedor quer selecionar o produto pelo melhor resultado obtido em ensaio com salmoura e pH diferentes dos do processo. O petróleo real do campo também tem composição distinta da amostra do laboratório. Qual critério deve prevalecer antes da escolha final?

Resposta: Comparar os candidatos nas condições representativas do sistema, porque a resposta depende da formulação e do fluido.

## 02_02 · bloco 006 · Como o antiespumante atua na quebra da espuma

Status: `ok`

Exemplos recebidos: PQ-09_01-04 (media), PQ-04_01-07 (dificil), PQ-06_03-01 (facil)

**1. [facil · recordar]** Qual efeito direto no filme da bolha o antiespumante deve promover para reduzir a espuma?

Resposta: Ruptura ou drenagem do filme que estabiliza a bolha.

**2. [media · comparar]** Dois antiespumantes são aplicados na mesma interface gás-líquido e na mesma dose, mas um quebra a espuma mais rápido. Que relação técnica explica essa diferença?

Resposta: A formulação altera espalhamento, penetração e dispersão do produto, mudando sua capacidade de alcançar o filme estabilizante.

**3. [media · inferir]** Após aumento de tensoativos e sólidos no fluido de entrada do separador, a espuma passa a persistir sem mudança de temperatura ou regime. Além da própria estabilidade da espuma, o que essa mudança pode dificultar na ação do antiespumante?

Resposta: Pode dificultar o contato do antiespumante com o filme, prejudicando seu espalhamento, penetração e dispersão na interface.

**4. [dificil · decidir]** Em um separador de produção, a dose de antiespumante foi elevada em etapas após aumento de tensoativos no fluido. Houve melhora inicial, depois nenhum ganho adicional, e existe preocupação com impacto em etapas posteriores do processo. Qual decisão técnica é mais consistente a partir desse comportamento?

Resposta: Reavaliar a formulação frente às propriedades da interface antes de aumentar mais a dose, porque após certa faixa o ganho adicional não é garantido e pode haver efeito no restante do processo.

## 02_02 · bloco 009 · Interações e efeitos colaterais relevantes no processamento

Status: `ok`

Exemplos recebidos: PQ-05_02-07 (dificil), PQ-01_01-03 (facil), PQ-07_05-06 (media)

**1. [facil · recordar]** Em separadores, que efeito a melhora da quebra de espuma tende a causar na saída de gás?

Resposta: Redução do arraste de líquido na corrente de gás.

**2. [media · diagnosticar]** Um antiespumante controlou a espuma em um vaso, mas surgiram problemas de interface em equipamentos seguintes. Que critério de seleção faltou considerar?

Resposta: A avaliação do antiespumante em conjunto com o restante do processamento, porque ele pode alterar interfaces em outros equipamentos.

**3. [media · decidir]** No mesmo FPSO, a formulação inicial funcionava bem, mas ao longo do campo aumentaram corte de água, sólidos e salinidade. Qual decisão sobre o programa químico é a correta?

Resposta: Revisar o programa químico; não se deve assumir que o desempenho inicial permanecerá estável indefinidamente.

**4. [dificil · diagnosticar]** A mesma formulação e a mesma dose continuam em uso, sem mudança relevante de corte de água, sólidos, salinidade ou temperatura. Após uma alteração de arranjo, a resposta ao antiespumante ficou irregular: em alguns períodos a espuma quebra, em outros não, e o arraste de líquido no gás oscila. Que mecanismo explica melhor essa inconsistência?

Resposta: Aplicação inadequada do antiespumante, com mistura insuficiente ou sem atingir a interface crítica.

## 02_02 · bloco 012 · Por que esses químicos funcionam na água produzida

Status: `ok`

Exemplos recebidos: PQ-05_02-07 (dificil), PQ-08_02-04 (media), PQ-09_01-02 (facil)

**1. [facil · recordar]** Além de aumentar o tamanho, que propriedade do floco um floculante polimérico eleva?

Resposta: A resistência mecânica dos flocos.

**2. [media · inferir]** Num teste de tratamento, o coagulante comprimiu a dupla camada elétrica das gotas de óleo. Antes da flotação, que mudança imediata se espera na interação entre gotas e sólidos?

Resposta: Menor repulsão elétrica, favorecendo a aproximação e a agregação entre gotas e sólidos.

**3. [media · decidir]** Um fornecedor propõe trocar um coagulante sintético por um natural, ambos com o mesmo mecanismo declarado. Qual condição técnica falta para aceitar a substituição na unidade?

Resposta: Demonstrar desempenho equivalente na água produzida específica da unidade.

**4. [dificil · diagnosticar]** Após ajuste químico, a água produzida passa a mostrar agregados maiores, mas a flotação por ar dissolvido não melhora. Ao mesmo tempo, vazão e carga de óleo aumentaram, sem ajuste na geração de bolhas, mistura ou tempo de contato. Qual limitação deve ser diagnosticada primeiro?

Resposta: Limitação hidrodinâmica e de captura na flotação, porque as condições de colisão e adesão às microbolhas não acompanharam a nova carga.  
_usa apoio_

## 02_02 · bloco 015 · Consequências e interações relevantes para o descarte

Status: `ok`

Exemplos recebidos: PQ-09_01-02 (facil), PQ-03_02-08 (dificil), PQ-07_05-06 (media)

**1. [facil · recordar]** Que característica do lodo pode ser alterada pelo uso de coagulantes e floculantes no tratamento da água produzida?

Resposta: A facilidade de desaguamento do lodo.

**2. [media · inferir]** Mantidos vazão e equipamento, um agente antes usado para quebrar emulsão passa a deixar a interface mais estável após mudança do fluido tratado. O que isso indica sobre a aplicação desse agente?

Resposta: Que sua ação depende da água; um agente que quebra emulsão em uma água pode estabilizar a interface em outra.

**3. [media · inferir]** Em um FPSO, resíduos de químicos de produção passaram a consumir parte do coagulante no tratamento da água produzida. Sem mudar o hardware, que efeito isso tende a ter no ajuste químico dessa etapa?

Resposta: Pode deslocar a dosagem ótima do tratamento, exigindo reajuste do programa químico.

**4. [dificil · decidir]** Após alteração relevante no regime de escoamento e na configuração da flotação, a remoção de óleo permaneceu semelhante, mas aumentaram o carbono orgânico residual e os sólidos suspensos do efluente. O programa químico foi mantido sem revisão. Qual ação deve ser priorizada para sustentar o descarte?

Resposta: Reavaliar o desempenho e redeterminar a dosagem do programa químico do tratamento da água produzida.

## 02_02 · bloco 018 · Papel dos inibidores de incrustação e limites de aplicação em sistemas com URS

Status: `ok`

Exemplos recebidos: PQ-03_01-05 (media), PQ-04_02-03 (facil), PQ-05_01-07 (dificil)

**1. [facil · recordar]** Além da adsorção, que mecanismo do inibidor dificulta o crescimento dos cristais?

Resposta: O aumento da barreira energética ao crescimento cristalino.

**2. [media · inferir]** Em um sistema com URS, pretende-se dosar inibidor apenas na água de injeção para proteger o processo de produção. Se o produto adsorve na rocha ao redor do poço injetor, qual é a consequência para essa proteção?

Resposta: Ela não fica garantida, porque o inibidor pode não alcançar o poço produtor.

**3. [dificil · decidir]** Uma FPSO possui URS operando adequadamente e o permeado segue para injeção. Ainda assim, surgem sinais de incrustação em um trecho interno associado à corrente concentrada da unidade, sem indício de falha na remoção de sulfato do permeado. Qual aplicação do inibidor deve ser priorizada?

Resposta: A proteção desse ponto interno da URS, especialmente da corrente concentrada rica em sulfato, onde há potencial de precipitação de CaSO4.  
_usa apoio_

**4. [media · inferir]** Em uma unidade com URS, a remoção de sulfato reduziu o risco ligado a sulfatos na injeção, mas a planta de processo mantém tendência de incrustação por CaCO3. Qual papel do inibidor permanece aplicável?

Resposta: Compensar incrustações que a remoção de sulfato não resolve, como CaCO3 na planta de processo.

## 02_02 · bloco 021 · Sequestrante químico: bissulfito de sódio, mecanismo e limitações

Status: `ok`

Exemplos recebidos: PQ-07_01-03 (facil), PQ-05_01-07 (dificil), PQ-01_01-05 (media)

**1. [facil · recordar]** Qual é a função do bissulfito de sódio no condicionamento de água?

Resposta: Reagir quimicamente com o oxigênio dissolvido, atuando como sequestrante.

**2. [media · inferir]** Em um sistema de água de injeção, a etapa mecânica passa a deixar mais oxigênio residual, mas a dosagem de bissulfito de sódio permanece inalterada. Qual efeito se espera a jusante?

Resposta: A demanda do sequestrante aumenta e, sem ajuste de dose, tende a permanecer residual de oxigênio no sistema.  
_usa apoio_

**3. [facil · recordar]** Que característica da solução diluída explica seu potencial corrosivo para muitos materiais?

Resposta: O baixo pH da solução diluída.

**4. [dificil · diagnosticar]** Em um FPSO, o oxigênio dissolvido antes do ponto de injeção permanece estável e a vazão indicada da bomba de bissulfito não mudou. Mesmo assim, o residual de oxigênio a jusante começou a subir após vários dias usando solução mantida em tanque com respiro para atmosfera; ao trocar por solução nova, o residual voltou ao normal. Qual diagnóstico esse padrão sustenta?

Resposta: Perda de concentração ativa da solução estocada, por conservação inadequada em contato com o ar, reduzindo a dosagem efetiva.

## 02_02 · bloco 024 · Condições que mudam o comportamento: cloro residual, CO2 e disponibilidade de gás

Status: `ok`

Exemplos recebidos: PQ-04_01-07 (dificil), PQ-05_01-06 (media), PQ-10_01-02 (facil)

**1. [facil · recordar]** Que arranjo de processo pode ser adotado quando balanço de remoção, espaço, peso e utilidades precisam ser conciliados?

Resposta: Sistemas combinados de desoxigenação.

**2. [media · inferir]** Água do mar clorada recebe bissulfito, mas o cloro residual sobe acima do normal e a dosagem permanece igual. Qual efeito direto se espera sobre o oxigênio dissolvido remanescente?

Resposta: Ele tende a aumentar, porque parte do bissulfito é consumida pelo cloro residual e sobra menos para remover oxigênio.

**3. [media · inferir]** Durante a desaeração a vácuo de água do mar, observa-se forte remoção de CO2 dissolvido. Que tendência inorgânica isso pode teoricamente favorecer?

Resposta: Precipitação de carbonato de cálcio.

**4. [dificil · decidir]** Uma unidade de água do mar compara stripping a gás com desaeração a vácuo. Testes mostram que o vácuo pode aumentar a tendência de CaCO3 por remoção de CO2. Há gás disponível, porém sua composição é inadequada para arraste e a corrente gasosa não tem destinação segura. Entre essas duas rotas isoladas, qual deve ser escolhida?

Resposta: A desaeração a vácuo, porque o stripping a gás fica inadequado sem gás compatível e sem destinação segura da corrente.

## 02_02 · bloco 027 · Função do controle microbiológico na água de injeção

Status: `ok`

Exemplos recebidos: PQ-03_01-05 (media), PQ-09_02-09 (dificil), PQ-10_01-02 (facil)

**1. [facil · recordar]** Qual é a função do controle microbiológico na água de injeção?

Resposta: Limitar a contaminação, o crescimento e a atividade microbiana que favorecem biofilme, souring e corrosão microbiologicamente influenciada.

**2. [facil · recordar]** Que grupo microbiano é particularmente relevante por sua associação com biocorrosão em ferro e aço?

Resposta: As bactérias redutoras de sulfato.

**3. [media · inferir]** Uma amostra da fase aquosa da água de injeção mostra baixa contagem microbiana, mas persistem sinais de colonização interna em linhas e filtros. Que limitação dessa avaliação impede concluir controle microbiológico do sistema?

Resposta: Ela representa células planctônicas da fase aquosa, mas não descarta microrganismos aderidos e biofilme em superfícies internas.

**4. [dificil · decidir]** Após substituir o biocida por outro de melhor desempenho em teste de bancada, a contagem na água de injeção cai, mas corrosão localizada e souring persistem em trechos com baixo escoamento e muita incrustação. Sem evidência de erro de dosagem, o foco técnico deve ser revisar novamente o produto ou a acessibilidade do tratamento às regiões contaminadas?

Resposta: A acessibilidade do tratamento, porque baixo escoamento e incrustação favorecem biofilme em nichos protegidos, menos alcançados pelo biocida.

## 02_02 · bloco 029 · Por que biofilme, incrustação e depósitos reduzem a eficácia

Status: `ok`

Exemplos recebidos: PQ-01_01-02 (facil), PQ-07_04-07 (dificil), PQ-03_01-05 (media)

**1. [facil · recordar]** Em sistemas sob escoamento, que característica da superfície também influencia a formação de biofilme?

Resposta: A rugosidade da superfície.

**2. [media · inferir]** Um mesmo biocida controla células livres em uma linha limpa. Em outro trecho, há biofilme recoberto por incrustação mineral e sulfeto de ferro. Mantido o produto, o que tende a ocorrer com a dosagem necessária nesse segundo trecho?

Resposta: Tende a ser maior que a usada para células livres, porque o recobrimento dificulta o contato e a penetração do produto.

**3. [media · inferir]** Em um sistema de injeção com materiais aderidos que criam locais inacessíveis ao biocida, o mesmo tratamento é mantido por longo período. Que consequência microbiológica tende a ser favorecida nesses locais?

Resposta: Proliferação bacteriana com aquisição de resistência ao tratamento usado.

**4. [dificil · diagnosticar]** Em uma linha de água de injeção, detectam-se bactérias na amostra e surge ataque localizado no material. O trecho também apresenta depósitos aderidos, química da água capaz de agravar o processo e material reconhecidamente suscetível. Qual conclusão sobre a causa do ataque é tecnicamente defensável?

Resposta: Não é defensável atribuí-lo apenas às bactérias; a causa deve ser avaliada combinando atividade microbiana, depósitos, química da água e suscetibilidade do material.

## 02_02 · bloco 032 · Como a inibição funciona e quais limites mecanísticos importam

Status: `ok`

Exemplos recebidos: PQ-10_01-02 (facil), PQ-08_02-04 (media), PQ-05_02-07 (dificil)

**1. [facil · recordar]** Qual é a função termodinâmica do MEG na fase aquosa para prevenir hidratos?

Resposta: Reduzir a atividade da água e deslocar o equilíbrio de formação de hidratos para condições mais severas.

**2. [media · inferir]** Mantendo pressão e composição do gás constantes, a concentração efetiva de MEG na água livre foi aumentada. O que acontece com a temperatura mínima de operação antes de atingir o equilíbrio de hidrato?

Resposta: A operação pode ocorrer em temperaturas mais baixas antes de alcançar o equilíbrio de hidrato.

**3. [media · decidir]** Uma equipe alega que o histórico térmico será favorável e o transporte de massa limitará o crescimento do hidrato, então não precisa verificar a margem operacional. O que deve prevalecer na avaliação?

Resposta: Deve prevalecer a avaliação do equilíbrio e da margem operacional; histórico térmico e transporte de massa não a substituem.

**4. [dificil · diagnosticar]** Em um sistema subsea, a vazão nominal de injeção de MEG permaneceu estável. Após aumento de água produzida, apenas um ramal, na mesma faixa de pressão, composição do gás e temperatura dos demais, passou a apresentar restrições intermitentes. Qual mecanismo explica melhor essa perda localizada de proteção?

Resposta: Concentração efetiva insuficiente de MEG na água livre desse ramal, por diluição e distribuição desigual, apesar da vazão nominal estável.

## 02_02 · bloco 035 · Seleção, monitoramento e alternativas de regeneração

Status: `ok`

Exemplos recebidos: PQ-01_01-02 (facil), PQ-04_02-09 (dificil), PQ-07_05-06 (media)

**1. [facil · recordar]** Qual é a função da regeneração no circuito de MEG?

Resposta: Remover água para permitir o reúso do glicol.

**2. [media · diagnosticar]** Num circuito de MEG, a concentração de glicol e o teor de sais estão adequados, mas a recuperação perde capacidade por limitação de escoamento. Qual aspecto monitorado aponta diretamente essa causa?

Resposta: Restrições hidráulicas no circuito.

**3. [media · inferir]** Em um FPSO, a regeneração do MEG opera estavelmente, mas o teor de sais na recuperação continua alto. Qual conclusão se aplica ao tratamento necessário?

Resposta: A remoção de sais deve ser avaliada separadamente; regeneração estável não garante seu controle.

**4. [dificil · decidir]** Duas alternativas de regeneração foram estudadas para um FPSO. A primeira mostrou baixo consumo de energia em ensaio com MEG e água limpos. A segunda foi avaliada com a carga real do circuito, contendo sais, sólidos e hidrocarbonetos. Para a escolha industrial, qual alternativa deve prevalecer?

Resposta: A segunda, porque a seleção deve considerar o circuito real; desempenho de mistura simplificada de laboratório não deve ser extrapolado para o arranjo industrial.

## 02_02 · bloco 038 · Função dos químicos no tratamento do gás

Status: `ok`

Exemplos recebidos: PQ-07_04-07 (dificil), PQ-03_03-04 (media), PQ-04_02-03 (facil)

**1. [facil · recordar]** Qual é o efeito buscado pelo inibidor de corrosão de gás sobre o material metálico?

Resposta: Reduzir a velocidade de ataque ao material metálico.

**2. [facil · recordar]** Por que os químicos do tratamento do gás são distribuídos por correntes e subsistemas específicos?

Resposta: Porque cada produto atua, por mecanismo próprio, sobre um problema distinto do processo.

**3. [media · inferir]** Em um trecho do tratamento do gás, a espécie sulfídrica passa a ser a ameaça dominante, enquanto espuma e risco de hidrato seguem inalterados. Que tipo de produto deve ser escolhido para esse trecho?

Resposta: Sequestrante de H2S, para consumir ou imobilizar a espécie sulfídrica.

**4. [dificil · decidir]** Em um FPSO, o gás entra em uma seção fria com risco de hidrato e depois segue para remoção de CO2. Alegando que os químicos coexistem no mesmo sistema, um operador propõe dosar apenas MEG em um único ponto para atender ambas as ameaças. Qual decisão técnica é correta?

Resposta: A proposta deve ser rejeitada: MEG trata hidratos; a remoção de CO2 requer solvente de absorção, como alcanolamina, e não obriga mesma corrente, concentração ou ponto de injeção.

## 02_02 · bloco 041 · Compatibilidade química: por que a combinação pode melhorar ou piorar a proteção

Status: `ok`

Exemplos recebidos: PQ-10_01-07 (dificil), PQ-07_01-03 (facil), PQ-09_02-06 (media)

**1. [facil · recordar]** A compatibilidade entre dois químicos de processo pode ser assumida apenas pela função declarada de cada produto?

Resposta: Não; a função declarada não garante a interação nem a proteção resultante.

**2. [facil · recordar]** Qual mecanismo de interação descreve a disputa de dois produtos pela mesma cobertura de superfície?

Resposta: Competição de adsorção.

**3. [media · inferir]** Em um sistema, a função nominal dos produtos não mudou, porém a formulação do pacote e o meio de serviço foram alterados. A proteção anticorrosiva deve ser tratada como invariável? Diga a consequência possível.

Resposta: Não. Ela pode melhorar, ser preservada ou reduzir, conforme a formulação e o meio.

**4. [dificil · decidir]** Um pacote com inibidor de corrosão e sequestrante de H2S preservou a proteção em bancada, mas o ensaio usou solução apenas com NaCl e corpo de prova de material diferente do equipamento real. Como o efeito da combinação depende do meio, qual decisão técnica deve anteceder a liberação para o serviço?

Resposta: Repetir o teste de compatibilidade com concentrações, materiais e fluido representativos do serviço; solução só com NaCl não valida esse desempenho.

## 02_02 · bloco 044 · Alternativas ao squeeze para controle de incrustação

Status: `ok`

Exemplos recebidos: PQ-08_02-04 (media), PQ-04_02-09 (dificil), PQ-05_01-02 (facil)

**1. [facil · recordar]** Na remoção seletiva de sulfato da água de injeção, por qual recurso essa separação é realizada?

Resposta: Por membranas adequadas ao serviço.

**2. [media · inferir]** Uma água de injeção com alto teor de sulfato alimenta um sistema com potencial de formar BaSO4 e SrSO4. Se esse teor for reduzido antes da injeção, o que acontece com a condição para essa incrustação?

Resposta: Ela diminui e pode até ser eliminada, porque a precipitação de BaSO4 e SrSO4 perde a condição necessária.

**3. [media · decidir]** Em um campo de longa vida, a equipe compara instalar URS com manter um programa de inibição. A URS tem investimento inicial e custos de operação e manutenção; a inibição traz custos recorrentes e perdas em paradas. Que base deve orientar a escolha?

Resposta: Um estudo de viabilidade técnico-econômica, comparando CAPEX e O&M da URS com os custos recorrentes de inibição e as perdas associadas à parada de produção.

**4. [dificil · decidir]** Uma equipe quer substituir a remoção de sulfato por uma tecnologia de transporte e retenção de inibidor no reservatório. Os testes ainda não demonstraram distribuição do produto, sua liberação ao longo do tempo nem compatibilidade com o meio. Na avaliação do projeto, essa opção pode ser tratada como equivalente à remoção de sulfato?

Resposta: Não. Sem validar distribuição, liberação e compatibilidade, ela não deve ser tratada como substituta equivalente da remoção de sulfato.

## 02_02 · bloco 047 · Segregação e compatibilidade entre produtos químicos

Status: `ok`

Exemplos recebidos: PQ-04_02-03 (facil), PQ-05_01-07 (dificil), PQ-08_02-04 (media)

**1. [facil · recordar]** Qual é a finalidade da segregação entre produtos químicos em uma instalação offshore?

Resposta: Evitar contato não intencional entre produtos incompatíveis e perda de desempenho por reação paralela.

**2. [media · decidir]** Em um skid de injeção de FPSO, pretende-se usar a mesma linha e a mesma mangueira para dois químicos em sequência, com possibilidade de resíduo entre bateladas. Que verificação deve ser feita antes da operação?

Resposta: Deve ser avaliada a compatibilidade entre os químicos no uso conjunto ou sequencial, incluindo a mistura residual na linha, na mangueira e no recipiente.

**3. [media · inferir]** No tratamento de água, passou a haver cloro residual alcançando o ponto de bissulfito por contaminação cruzada. As bombas e vazões de dosagem não mudaram. Qual efeito essa interação tende a causar no consumo químico e na avaliação do tratamento?

Resposta: O cloro residual consome o bissulfito antes da função principal, elevando a demanda química e podendo mascarar falhas de tratamento.

**4. [dificil · diagnosticar]** Durante uma campanha de limpeza no FPSO, a equipe reaproveita para limpador ácido uma mangueira que retornou do circuito de alvejante clorado. A identificação da linha estava inadequada, não havia prevenção de retorno e o flushing compatível não foi feito. Ao iniciar a transferência, surge uma nuvem gasosa na área. Qual diagnóstico explica o evento?

Resposta: Houve mistura residual de limpador ácido com alvejante clorado na mangueira/linha, gerando nuvem gasosa tóxica.

## 02_02 · bloco 050 · Monitoramento do armazenamento e consequências operacionais

Status: `ok`

Exemplos recebidos: PQ-03_01-05 (media), PQ-07_05-02 (facil), PQ-09_02-09 (dificil)

**1. [facil · inferir]** Se água produzida acumulada puder ter atividade microbiológica, que facilidades passam a ser relevantes?

Resposta: Facilidades para monitorar H2S e para aplicar biocidas.

**2. [media · decidir]** Em um sistema de injeção sujeito à corrosão, a vazão varia ao longo do dia e a equipe precisa acompanhar mudanças de corrosividade nesse regime. Que técnicas são adequadas?

Resposta: Técnicas eletroquímicas como par galvânico e resistência à polarização.

**3. [facil · recordar]** Se houver falhas de segregação, superdosagem, subdosagem ou degradação do químico, que aspecto físico da planta pode ser comprometido?

Resposta: A integridade de linhas e vasos.

**4. [dificil · diagnosticar]** Num FPSO, oscilações de vazão, pressão e composição são usuais. Mesmo dentro desse padrão, aparecem consumo anormal de químico, alteração de cor do produto, espuma inesperada e perda de eficiência de separação, enquanto a dosagem planejada permanece a mesma. Qual diagnóstico deve ser priorizado?

Resposta: Problema de estocagem ou manuseio do químico, especialmente degradação, falha de segregação ou dosagem inadequada, porque isso pode aparecer como instabilidade a jusante.

## 02_02 · bloco 053 · Seleção do ponto de medição, automação e confiabilidade dos dados

Status: `ok`

Exemplos recebidos: PQ-09_01-04 (media), PQ-04_02-09 (dificil), PQ-01_01-02 (facil)

**1. [facil · recordar]** Na dosagem automatizada de químicos, que salvaguarda continua necessária para confirmar a confiabilidade da medição?

Resposta: Validação periódica da medição, com manutenção do sensor e reconciliação com análises laboratoriais.

**2. [facil · recordar]** Que ponto de medição tende a representar melhor a condição realmente recebida pelo equipamento após a injeção do químico?

Resposta: Um sensor a jusante do misturador ou do ponto de injeção, após a mistura do químico.

**3. [media · decidir]** Em um FPSO, um químico protege um ativo crítico e há possibilidade de água livre. Se um falso negativo reduz a dosagem e expõe o ativo, enquanto um falso positivo só eleva consumo, que erro a lógica de controle deve priorizar evitar?

Resposta: O falso negativo, porque nesse cenário ele compromete a proteção do ativo crítico.

**4. [dificil · diagnosticar]** Num FPSO, a vazão de injeção de um químico é alterada e o controlador on-line passa a corrigir em excesso. O sensor está sem incrustação nem deriva aparente, e a comparação com laboratório só coincide quando os dados são deslocados no tempo de trânsito da linha. Qual fator deve entrar na lógica de controle para evitar esse comportamento?

Resposta: O atraso entre injeção e medição, incluindo tempo de mistura e tempo de resposta do sensor.

## 02_02 · bloco 056 · Leitura temporal, pH e resposta corrosiva

Status: `ok`

Exemplos recebidos: PQ-03_02-08 (dificil), PQ-01_01-02 (facil), PQ-06_01-04 (media)

**1. [facil · recordar]** Além das reações eletroquímicas, que aspecto da superfície metálica a acidificação pode desestabilizar e assim favorecer maior corrosão?

Resposta: A estabilidade dos filmes superficiais.

**2. [media · inferir]** Em um meio aquoso suscetível à corrosão ácida, o pH cai durante a operação. Mantidos metalurgia, temperatura e escoamento, para que lado tende a mudar a taxa de perda metálica?

Resposta: Tende a aumentar.

**3. [dificil · diagnosticar]** Em uma linha com fase aquosa, o pH sofre uma queda curta e depois retorna. A sonda RE mostra mudança na inclinação da perda metálica, mas a curva acumulada de perda de espessura não desenha o mesmo vale do pH no mesmo instante. Esse desencontro, por si só, sustenta falha de medição ou resposta esperada do sistema?

Resposta: Resposta esperada do sistema; a perda metálica é cumulativa, então a curva de dano não replica instantaneamente a curva de pH.

**4. [media · decidir]** Duas linhas apresentam a mesma queda transitória de pH, mas diferem em metalurgia, presença de fase aquosa, composição do fluido e regime de escoamento. A correlação pH-corrosão medida na primeira pode ser usada como regra na segunda?

Resposta: Não; a sensibilidade da resposta corrosiva depende dessas condições, então a correlação observada não é universal.
