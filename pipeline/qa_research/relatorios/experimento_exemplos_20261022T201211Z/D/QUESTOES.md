# Questões geradas

## 01_01 · bloco 000 · Indicadores de monitoramento operacional: detecção de desvios e diagnóstico

Status: `ok`

Exemplos recebidos: PQ-07_01-03 (facil), pira_ptbr:B2008 (facil), arc_challenge:Mercury_7013860 (media), PQ-04_01-07 (dificil), PQ-02_10-05 (media), hotpotqa:5abed6fd5542994516f4544c (dificil)

**1. [facil · recordar]** Em uma unidade de processo de FPSO, qual é o papel de um indicador de desempenho dentro de uma metodologia de monitoramento operacional mais ampla?

Resposta: Detectar desvios, identificar variáveis perturbadas e apoiar o diagnóstico de causas prováveis.

**2. [media · inferir]** Nos topsides de um FPSO, que aspecto da própria operação torna essa lógica de monitoramento especialmente útil?

Resposta: A dependência da interação entre separação, tratamento de óleo, água, gás, utilidades e sistemas de controle.

**3. [facil · comparar]** Se o operador precisa confirmar a grandeza de processo que realmente se alterou, o KPI basta sozinho?

Resposta: Não; o KPI apenas resume o efeito da variável sobre o desempenho e não a substitui.

**4. [media · inferir]** Quando o processo opera com especificações mais restritas e maior exigência de segurança, o que torna as ferramentas online operacionalmente valiosas?

Resposta: Elas permitem avaliar as condições operacionais em tempo próximo do real.

**5. [media · inferir]** Se a equipe quer que o monitoramento ajude a agir antes de um período anormal se instalar, que objetivo está buscando?

Resposta: Antecipar anormalidades.

**6. [media · inferir]** Se um KPI é interpretado sem o contexto do processo, o histórico recente e o conhecimento acumulado da operação, qual erro causal pode entrar no diagnóstico?

Resposta: Tratar o sintoma como se fosse a causa.

**7. [dificil · decidir]** Após uma mudança rápida de carga durante a partida de um trem de processo do FPSO, o KPI piora por curto período e volta ao patamar anterior depois da estabilização. Que conclusão não deve ser tirada apenas desse comportamento?

Resposta: Que houve perda estrutural de desempenho; a variação pode ser transitória pela mudança de carga.

**8. [facil · recordar]** Além de degradação de equipamento e perturbações de alimentação, que tipo de mudança ligada ao controle também pode alterar o comportamento de um KPI?

Resposta: Alterações de estratégia de controle.

## 01_01 · bloco 001 · O que são KPIs e como a finalidade muda sua definição

Status: `ok`

Exemplos recebidos: pira_ptbr:A954 (facil), PQ-03_02-08 (dificil), hotpotqa:5a72fcf65542991f29ee2ced (dificil), PQ-09_01-04 (media), arc_challenge:AIMS_2009_4_11 (media), PQ-04_02-03 (facil)

**1. [facil · recordar]** Em um FPSO, qual é a função básica de um KPI na avaliação de um processo industrial?

Resposta: Avaliar a eficiência e o desempenho do processo.

**2. [facil · recordar]** Ao acompanhar a performance de uma planta de processo em FPSO, com que tipo de referência um KPI pode comparar o resultado real?

Resposta: Com uma referência teórica.

**3. [facil · recordar]** Quais dois consumos são citados como passíveis de expressão por KPI em uma planta de produção?

Resposta: Consumo de energia e de matérias-primas.

**4. [media · decidir]** No mesmo sistema de tratamento de óleo de um FPSO, a operação precisa acompanhamento em tempo real e a gerência quer acompanhamento consolidado. É obrigatório usar um único KPI para os dois usos?

Resposta: Não; o mesmo processo pode exigir indicadores diferentes quando muda a finalidade do acompanhamento.

**5. [facil · recordar]** Em uma planta de produção de FPSO, a que níveis um KPI pode ser aplicado?

Resposta: A equipamentos, a etapas específicas do processo ou à instalação como um todo.

**6. [media · inferir]** Se um KPI de um trem de compressão em FPSO mostrar deficiência de desempenho, que tipo de ação seu uso deve apoiar?

Resposta: Ações para reduzir custos ou elevar a capacidade sem grandes investimentos.

**7. [facil · decidir]** Se a liderança afirma que implantar KPIs por si só garante aumento de capacidade ou redução de custo em qualquer condição operacional do FPSO, essa afirmação é válida?

Resposta: Não; KPIs não garantem esses ganhos em qualquer condição operacional.

**8. [media · decidir]** Ao levar um indicador de desempenho para um painel de controle em tempo real no FPSO, que requisito da métrica precisa ser preservado para sustentar a decisão operacional?

Resposta: A métrica deve permanecer coerente com a decisão que precisa sustentar.

## 01_01 · bloco 002 · Denominador, base de exposição e comparabilidade

Status: `ok`

Exemplos recebidos: PQ-07_04-04 (media), PQ-08_03-02 (facil), arc_challenge:OHAT_2007_5_39 (media), pira_ptbr:A905 (facil), PQ-09_02-09 (dificil), hotpotqa:5a85d2fd5542994c784ddb82 (dificil)

**1. [facil · recordar]** Em um KPI operacional de uma FPSO, qual é a função técnica do denominador?

Resposta: Estabelecer a base de referência do indicador.

**2. [facil · recordar]** Ao calcular a taxa de frequência de acidentes ocupacionais em uma FPSO, qual base deve aparecer no denominador para representar a exposição ao risco no período?

Resposta: As horas-homem de exposição ao risco.

**3. [facil · recordar]** Em uma taxa de frequência de acidentes estruturada por exposição, o que o numerador deve contabilizar?

Resposta: A quantidade de casos enquadrados pela definição adotada.

**4. [facil · comparar]** Duas janelas mensais de uma FPSO serão comparadas por taxa de frequência de acidentes. Além da fórmula, quais três elementos precisam ser compatíveis para a comparação temporal ser consistente?

Resposta: O período, o critério de enquadramento dos casos e a base de horas-homem.

**5. [media · inferir]** Em uma FPSO, o número de acidentes enquadrados ficou igual em dois períodos, mas as horas-homem expostas caíram no segundo. Para a taxa de frequência, qual é a direção esperada da mudança?

Resposta: A taxa aumenta, porque a mesma quantidade de casos passa a ser dividida por uma base menor de exposição.

**6. [media · inferir]** Em um mês, o consumo total de energia da FPSO aumentou junto com o volume processado. Sem normalização, que conclusão sobre o desempenho não pode ser tirada desse valor absoluto?

Resposta: Não se pode concluir que o desempenho intrínseco piorou, porque o aumento pode refletir apenas maior carga ou volume processado.

**7. [media · decidir]** Se a gestão quer acompanhar impacto ambiental de uma FPSO de modo comparável entre períodos com produção diferente, que base de denominador é tecnicamente coerente?

Resposta: Uma base por unidade produzida.

## 01_01 · bloco 004 · Dependabilidade e seus atributos centrais

Status: `ok`

Exemplos recebidos: pira_ptbr:A204 (facil), PQ-10_01-02 (facil), arc_challenge:Mercury_7159758 (media), hotpotqa:5adfb4c8554299603e418382 (dificil), PQ-09_02-06 (media), PQ-03_02-08 (dificil)

**1. [facil · recordar]** Na avaliação de um sistema de processo de um FPSO, o que é dependabilidade?

Resposta: É o conjunto de atributos que sustenta a confiança no serviço prestado pelo sistema.

**2. [facil · recordar]** Um sistema de compressão inicia um teste em operação e deve continuar prestando o serviço correto por 48 horas, sob condições definidas. Qual atributo está sendo avaliado?

Resposta: Confiabilidade.

**3. [media · comparar]** Mantido o mesmo equipamento, qual atributo trata de ele estar apto em um instante e qual trata de recuperá-lo após defeito dentro de um tempo especificado?

Resposta: Disponibilidade no instante; mantenabilidade na restauração após defeito dentro do tempo especificado.

**4. [media · inferir]** Um sistema de proteção de um FPSO é projetado para desligar um equipamento em condição perigosa para evitar dano maior. Qual compromisso técnico esse projeto assume?

Resposta: Aceita reduzir a continuidade operacional para garantir falha em modo seguro.

**5. [media · inferir]** Em um FPSO, falhas param produção, reparos exigem recursos logísticos e proteções podem retirar equipamentos de serviço. O que isso indica sobre disponibilidade, confiabilidade e mantenabilidade na prática?

Resposta: Que esses atributos não são independentes na prática.

**6. [media · inferir]** Se dois sistemas de um FPSO têm o mesmo número de falhas no período, que fator adicional passa a ser decisivo para o desempenho global?

Resposta: A rapidez e as condições do retorno à operação aceitável.

**7. [dificil · diagnosticar]** Dois equipamentos reparáveis de topside têm a mesma frequência de falha e o mesmo tempo de reparo ativo. Ainda assim, um deles permanece indisponível bem mais tempo entre a falha e o retorno seguro à operação. Qual parcela do downtime explica a menor disponibilidade operacional?

Resposta: Tempos logísticos e administrativos maiores.  
_usa apoio_

## 01_01 · bloco 005 · Disponibilidade: o que é e por que depende de falha e reparo

Status: `ok`

Exemplos recebidos: PQ-05_01-07 (dificil), PQ-07_01-03 (facil), pira_ptbr:B2094 (facil), PQ-04_01-06 (media), hotpotqa:5a7b702e55429931da12cab6 (dificil), arc_challenge:Mercury_SC_408550 (media)

**1. [facil · recordar]** Em um KPI de um sistema de processo do FPSO, o que a disponibilidade mede?

Resposta: A capacidade de o sistema estar apto a cumprir a função requerida quando necessário.

**2. [media · decidir]** Antes de comparar a disponibilidade reportada por dois KPIs de equipamentos do FPSO, qual aspecto do critério de cálculo precisa estar explicitado para a comparação ser consistente?

Resposta: Quais indisponibilidades são incluídas no indicador.

**3. [facil · recordar]** Em um equipamento reparável do FPSO, de que comportamento ao longo do tempo resulta a disponibilidade?

Resposta: Da alternância entre períodos operacionais e períodos indisponíveis por falha ou reparo.

**4. [facil · recordar]** Para um KPI em estado estacionário, como a disponibilidade pode ser representada?

Resposta: Pela razão entre uptime e tempo total observado.

**5. [facil · decidir]** Se o histórico do FPSO não traz uptime e downtime diretamente, quais valores médios podem ser usados como aproximação da disponibilidade de um sistema reparável?

Resposta: MTBF e MTTR.

**6. [media · inferir]** Em um sistema reparável do FPSO, se o MTTR permanece constante e o MTBF aumenta, qual tendência se espera para a disponibilidade?

Resposta: Ela tende a aumentar.

**7. [media · comparar]** Na disponibilidade operacional de um equipamento do FPSO, qual é a diferença entre tempo de reparo ativo e downtime total de uma falha?

Resposta: O reparo ativo é só a intervenção; o downtime total inclui também tempos logísticos e administrativos.

## 01_01 · bloco 006 · Redundância, standby e efeitos sobre o comportamento do sistema

Status: `ok`

Exemplos recebidos: hotpotqa:5a7a66755542994f819ef1d3 (dificil), arc_challenge:Mercury_SC_LBS10907 (media), pira_ptbr:B2434 (facil), PQ-06_01-04 (media), PQ-03_01-01 (facil), PQ-07_04-07 (dificil)

**1. [facil · recordar]** Em um sistema redundante de um FPSO, de quais três fatores depende o efeito da redundância sobre o comportamento do sistema?

Resposta: Da lógica funcional do sistema, da forma de acionamento do equipamento reserva e das dependências entre subsistemas.

**2. [facil · recordar]** Em uma configuração com reserva fria, qual exposição tende a diminuir no equipamento reserva por ele não operar sob a mesma carga do ativo?

Resposta: A exposição a certos mecanismos de desgaste.

**3. [media · diagnosticar]** Em um trem redundante de compressão, o ativo falha e, sem perda prévia das utilidades compartilhadas, o equipamento em reserva fria é comandado mas não entra nem assume a função. Que limitação remanescente da reserva explica a perda de serviço?

Resposta: Falha de partida ou de comutação do reserva.

**4. [media · inferir]** Por que a vantagem de confiabilidade e disponibilidade da redundância não cresce indefinidamente ao longo do tempo de missão?

Resposta: Porque a degradação dos equipamentos ativos pode deixar de ser compensada pelo reserva.

**5. [media · decidir]** Em compressão, geração ou tratamento de um FPSO, o que a duplicação precisa manter para que de fato agregue desempenho ao processo?

Resposta: A função de processo relevante, e não só a duplicação física do equipamento.

**6. [media · inferir]** Dois trens de tratamento em um FPSO são duplicados, mas dependem do mesmo gargalo de utilidades e descarga. Como isso afeta o ganho real de desempenho?

Resposta: O ganho real pode ser menor do que o sugerido por uma lógica simplificada série-paralelo.

**7. [media · diagnosticar]** Após um único evento físico, os dois caminhos redundantes de geração perdem a função ao mesmo tempo, embora nenhum dependa do outro para operar. Que limitação da redundância foi caracterizada?

Resposta: Falha de causa comum.

**8. [media · diagnosticar]** Em um arranjo com dois trens duplicados, ambos ficam bloqueados pelo mesmo permissivo de segurança, apesar de os equipamentos estarem aptos. O que isso mostra sobre o efeito da duplicação?

Resposta: Que a lógica de intertravamento ainda pode causar indisponibilidade.

## 01_01 · bloco 007 · Como selecionar, modelar e atualizar análises RAM

Status: `ok`

Exemplos recebidos: PQ-10_01-02 (facil), PQ-05_02-07 (dificil), hotpotqa:5ac2aeee5542996773102603 (dificil), PQ-04_02-04 (media), pira_ptbr:A367 (facil), arc_challenge:ACTAAP_2007_7_4 (media)

**1. [facil · recordar]** Em um FPSO, uma análise RAM pode apoiar decisão em quais frentes do ciclo do ativo?

Resposta: Operação, fabricação, projeto e manutenção.

**2. [facil · recordar]** Antes de modelar a lógica funcional de uma análise RAM de um FPSO, quais levantamentos básicos devem ser feitos?

Resposta: Modos de falha que geram perda ao sistema, histórico de falhas e tempos de reparo.

**3. [facil · recordar]** Ao escolher o método de modelagem RAM para um sistema de processo de FPSO, o que ele precisa representar além dos equipamentos em si?

Resposta: As dependências e os modos de operação da lógica funcional.

**4. [media · decidir]** Na fase preliminar do projeto de um FPSO, a equipe quer apenas validar o arranjo do sistema, a quantidade de equipamentos e alternativas de redundância. Que nível de complexidade de modelo RAM é suficiente nessa etapa?

Resposta: Modelos mais simples.

**5. [media · inferir]** Com o sistema de processo de um FPSO já detalhado, qual resultado de um modelo RAM mais completo ajuda diretamente a priorizar ações de melhoria?

Resposta: Identificar os maiores contribuintes de falha.

**6. [media · inferir]** Por que uma análise RAM de um mesmo sistema não deve manter tempos de reparo e frequências de falha genéricos ao ser aplicada a outro FPSO?

Resposta: Porque esses parâmetros variam com a arquitetura, a acessibilidade, a estratégia de manutenção e o contexto operacional da unidade.

**7. [media · diagnosticar]** Em uma unidade nova com pacote protótipo, a equipe não dispõe de histórico confiável e preenche o modelo RAM com parâmetros emprestados. Qual fragilidade principal isso introduz no resultado?

Resposta: Pode introduzir parâmetros inadequados e gerar resultados imprecisos.

**8. [media · decidir]** Dois estudos de disponibilidade foram feitos para um FPSO. Um usa modelo muito sofisticado, mas com lógica operacional simplificada e dados pouco aderentes à unidade; o outro é menos sofisticado, porém representa corretamente a lógica funcional, o regime operacional e usa dados coerentes com a unidade. Qual tende a ter maior valor para decisão?

Resposta: O menos sofisticado, se estiver aderente à lógica do modelo, ao regime operacional e à qualidade dos dados da unidade.

## 01_01 · bloco 008 · Coleta de dados, indicadores e monitoramento do desempenho real

Status: `ok`

Exemplos recebidos: PQ-03_02-08 (dificil), arc_challenge:NYSEDREGENTS_2009_4_9 (media), PQ-04_01-06 (media), PQ-06_03-01 (facil), hotpotqa:5ab59a2d5542992aa134a373 (dificil), pira_ptbr:A391 (facil)

**1. [facil · recordar]** Na avaliação de disponibilidade e confiabilidade de um FPSO, a qualidade do resultado depende diretamente da qualidade de quais registros operacionais?

Resposta: Dos registros de falha e de retorno à operação.

**2. [facil · recordar]** Ao planejar a coleta de dados de falha em um FPSO, o que deve ser garantido sobre as causas registradas para apoiar a priorização de ações corretivas?

Resposta: Que as causas sejam distinguíveis e úteis à priorização das ações corretivas.

**3. [facil · recordar]** Registros de falha acumulados por anos só tendem a aumentar a confiança analítica sob quais condições de gestão da informação?

Resposta: Quando permanecem padronizados e eletronicamente gerenciados.

**4. [media · decidir]** Uma equipe quer representar as condições locais de um FPSO usando apenas bancos setoriais como OREDA, Well Master ou Subsea Master. Isso substitui os dados da própria unidade?

Resposta: Não; esses bancos apoiam padronização e comparação, mas não substituem dados da unidade para representar condições locais.

**5. [facil · recordar]** No monitoramento operacional de um FPSO, quais dois instantes precisam ser registrados para calcular MTTR e disponibilidade observada?

Resposta: O tempo de início da falha e o tempo de retorno ao estado operacional.

**6. [media · decidir]** Em um FPSO, o Item A falha raramente, mas sua indisponibilidade interrompe a exportação. O Item B falha mais, porém sem bloquear produção, segurança de processo nem exportação. Qual item deve ser tratado como mais relevante para o desempenho da unidade?

Resposta: O Item A, porque sua indisponibilidade bloqueia uma função crítica do sistema.

**7. [media · inferir]** Se o painel de desempenho de um FPSO acompanhar apenas médias de falha e recuperação, sem considerar a função de cada item no sistema, qual efeito analítico pode ocorrer?

Resposta: Os verdadeiros limitantes do desempenho podem ficar mascarados.

## 01_01 · bloco 010 · Interações com segurança, manutenção e recursos de suporte

Status: `ok`

Exemplos recebidos: hotpotqa:5ade294a55429939a52fe847 (dificil), PQ-05_01-02 (facil), pira_ptbr:B2117 (facil), arc_challenge:Mercury_7175718 (media), PQ-03_02-08 (dificil), PQ-06_01-04 (media)

**1. [facil · decidir]** Ao acompanhar o KPI de disponibilidade de um FPSO, é tecnicamente correto desconsiderar as implicações das funções de proteção e analisar apenas o tempo em produção?

Resposta: Não; disponibilidade e segurança devem ser avaliadas conjuntamente.

**2. [media · inferir]** Em um FPSO, um intertravamento de proteção provoca parada automática ao detectar uma condição perigosa. Qual é a justificativa técnica principal dessa interrupção?

Resposta: Evitar estados perigosos, danos ambientais e consequências maiores.

**3. [facil · decidir]** Após melhora do KPI de disponibilidade, propõe-se reduzir intervenções preventivas apenas para ampliar o tempo em produção. Sem outra análise, essa decisão é tecnicamente aceitável?

Resposta: Não; a redução de intervenções preventivas exige avaliar risco e integridade.

**4. [media · inferir]** Um equipamento crítico está parado, mas o atraso dominante para o retorno operacional é aguardar acesso à área, sobressalente e mobilização logística. Se forem adicionadas mais equipes de manutenção, qual tende a ser o efeito?

Resposta: Tende a ser limitado, porque o gargalo está em acesso, sobressalente ou logística, não na quantidade de equipes.

**5. [dificil · diagnosticar]** Em um FPSO, duas falhas ocorrem quase ao mesmo tempo. Há acesso liberado, sobressalentes disponíveis e permissões emitidas, mas uma correção só começa quando uma equipe conclui a outra. Qual é o gargalo que está prolongando a indisponibilidade?

Resposta: A capacidade das equipes de manutenção; as falhas simultâneas formaram fila.

**6. [media · comparar]** Dois subsistemas falham. Mantidos iguais o tempo estimado de recuperação e a disponibilidade de recursos, um compromete uma função essencial da planta e o outro afeta uma função secundária. Qual critério de priorização diferencia esses casos?

Resposta: Criticidade funcional.

**7. [media · comparar]** Em duas intervenções corretivas, mantidos iguais o impacto funcional na planta e a disponibilidade de recursos, uma restabelece a operação em 2 horas e a outra em 18 horas. Qual critério de priorização diferencia esses casos?

Resposta: Duração da recuperação.

**8. [media · comparar]** Entre duas recuperações, mantidos iguais o impacto funcional na planta e o tempo estimado de retorno, uma depende de recurso e liberação exclusivos, e a outra disputa o mesmo recurso e a mesma janela de liberação com outro subsistema. Qual critério de priorização diferencia esses casos?

Resposta: Restrições compartilhadas entre subsistemas.

## 01_01 · bloco 011 · Como o processamento primário condiciona a capacidade da unidade

Status: `ok`

Exemplos recebidos: pira_ptbr:A819 (facil), arc_challenge:Mercury_7236075 (media), hotpotqa:5ae456535542996836b02c80 (dificil), PQ-07_05-02 (facil), PQ-04_01-07 (dificil), PQ-03_03-04 (media)

**1. [facil · recordar]** Em um FPSO, qual é a função do processamento primário sobre os fluidos produzidos?

Resposta: Separar e tratar óleo, gás e água sob condições controladas.

**2. [media · inferir]** Em um FPSO, o fluido chega à planta misturado e com impurezas. Nessa condição, de que conjunto de capacidades passa a depender a capacidade produtiva da unidade?

Resposta: Da capacidade combinada de separação, tratamento e movimentação dos fluxos.

**3. [media · inferir]** Se um separador ou compressor do processamento primário opera abaixo da eficiência esperada e a unidade precisa preservar especificações e estabilidade operacional, o que tende a acontecer com a taxa de produção?

Resposta: A taxa de produção tende a ser reduzida.

**4. [facil · recordar]** Se um equipamento do processamento primário fica inoperante ou degradado, que combinação de impactos na unidade pode aparecer ao mesmo tempo?

Resposta: Perda de volume e queda de qualidade.

**5. [facil · recordar]** Em uma unidade marítima, quais são os dois destinos operacionais relevantes da água produzida?

Resposta: Reinjeção para auxiliar a produção de óleo ou tratamento para descarte no mar conforme exigências legais.

**6. [media · inferir]** A malha de água produzida perdeu capacidade em um FPSO. Mesmo com potencial dos poços disponível, o que pode acontecer com a vazão total do campo e por qual limitação?

Resposta: Ela pode ter de ser reduzida por falta de capacidade de separar, tratar, reinjetar ou descartar a fase aquosa gerada com os hidrocarbonetos.

## 01_01 · bloco 012 · Seleção e aplicação de medidas para prevenir ou aliviar gargalos

Status: `ok`

Exemplos recebidos: PQ-03_03-04 (media), arc_challenge:Mercury_7187530 (media), PQ-07_01-03 (facil), hotpotqa:5addf72d5542995b365faba2 (dificil), pira_ptbr:A1591 (facil), PQ-05_01-07 (dificil)

**1. [facil · comparar]** Na gestão de gargalos de um FPSO, o que diferencia medidas preventivas de medidas corretivas quanto ao momento de atuação sobre a perda de capacidade?

Resposta: As preventivas atuam antes da perda, reduzindo a probabilidade de formação do problema; as corretivas atuam depois que a restrição já compromete a capacidade.

**2. [media · inferir]** Em um campo offshore com risco de incrustação e gerenciamento difícil, por que a estratégia de desenvolvimento pode incorporar prevenção já nessa fase?

Resposta: Para reduzir custos associados a perdas de produção, considerando o risco de ocorrência e os desafios de gerenciamento.

**3. [facil · decidir]** Num FPSO, squeeze de inibidor e remoção de sulfato são opções possíveis contra incrustação. Qual conjunto de critérios deve sustentar a escolha entre essas rotas?

Resposta: O mecanismo dominante de incrustação, a origem dos íons, a arquitetura de injeção e produção, a acessibilidade para intervenção e as penalidades de parada.

**4. [media · comparar]** Qual é o princípio comum entre selecionar uma rota de controle de incrustação e executar debottlenecking em um processo de FPSO?

Resposta: A ação deve ser escolhida a partir do mecanismo ou da restrição realmente dominante, e não por uma lista genérica de técnicas.

**5. [facil · recordar]** Antes de definir uma mudança para aliviar um gargalo de processo em um FPSO, o que o debottlenecking exige localizar?

Resposta: A variável ou o equipamento limitante.

**6. [media · decidir]** Uma mudança operacional libera a restrição atual de um sistema de processo, mas cria nova limitação em outro ponto da planta. Pelo princípio de debottlenecking, essa solução atende ao objetivo?

Resposta: Não; a mudança deve aliviar precisamente a restrição sem deslocar o problema para outro ponto.

**7. [facil · recordar]** Na seleção de uma ação para prevenir ou aliviar um gargalo em FPSO, quais dois referenciais precisam ser definidos primeiro?

Resposta: Onde está a limitação e qual horizonte se deseja atacar.

## 01_01 · bloco 013 · Consequências operacionais e econômicas das restrições em FPSO

Status: `ok`

Exemplos recebidos: pira_ptbr:A137 (facil), hotpotqa:5ac3e0e25542997ea680c970 (dificil), PQ-04_01-06 (media), arc_challenge:Mercury_412216 (media), PQ-09_02-09 (dificil), PQ-10_01-01 (facil)

**1. [media · inferir]** Se um gargalo atinge um ponto compartilhado por vários fluxos do FPSO e não há expansão imediata da capacidade, que decisão gerencial passa a ser obrigatória para manter a operação?

Resposta: Priorizar entregas e alocar a capacidade disponível.

**2. [media · inferir]** Com a capacidade do FPSO temporariamente limitada em um equipamento comum, mas com vários poços ainda ativos, qual ajuste pode ser feito na participação de cada poço na carga total da unidade?

Resposta: Redistribuir as vazões entre os poços.

**3. [facil · recordar]** Na concepção de um FPSO, quais grupos de características da unidade influenciam a capacidade de reduzir paradas e problemas entre operações de offloading?

Resposta: Localização, meio ambiente, sistema de ancoragem, casco, convés e arranjos de produção e armazenagem.

**4. [media · decidir]** Uma falha confirmada em um riser ou no sistema de ancoragem de um FPSO exige resposta imediata. Qual medida operacional pode se tornar necessária?

Resposta: Interromper a produção para executar intervenções de integridade.

**5. [media · inferir]** Se falham o autodiagnóstico e a implementação de ações contingenciais e corretivas no prazo compatível com o risco, qual consequência pode recair sobre a instalação?

Resposta: Interdição da instalação.

**6. [media · inferir]** Sob os demais fatores constantes, que combinação aumenta a magnitude da perda econômica de uma interdição em FPSO?

Resposta: Maior volume produzido e maior duração da indisponibilidade.

**7. [media · inferir]** Ao longo da vida de um FPSO, perdas recorrentes de produção afetam, além da eficiência, qual classe de decisão empresarial?

Resposta: Decisões de investimento.

## 01_01 · bloco 015 · Atribuição de causas: do mecanismo físico à perda observada

Status: `ok`

Exemplos recebidos: PQ-07_05-02 (facil), PQ-03_03-04 (media), PQ-04_02-09 (dificil), pira_ptbr:A325 (facil), hotpotqa:5a86dd485542996432c571f6 (dificil), arc_challenge:Mercury_7215198 (media)

**1. [media · diagnosticar]** Em um poço, a seção interna da coluna de produção foi sendo reduzida por um depósito aderido. A resistência ao fluxo aumentou, a pressão medida no poço se alterou e a vazão bruta caiu. Qual fenômeno causador deve ser atribuído à perda?

Resposta: Incrustação na coluna de produção.

**2. [facil · recordar]** Em uma investigação, a equipe já registrou o fenômeno físico causador. Agora precisa lançar, em campo próprio, a maneira pela qual a incapacidade de operar apareceu no ativo. Como esse campo deve ser classificado?

Resposta: Modo de falha.

**3. [media · inferir]** Num caso em que a passagem já está restringida por depósito formado, inicia-se somente a dosagem de um produto para evitar novos depósitos. Que efeito não deve ser atribuído a essa dosagem isolada?

Resposta: A desobstrução do trecho já bloqueado.

**4. [media · decidir]** Após retirar o material depositado que limitava a capacidade de escoamento, qual verificação adicional pode ser necessária para concluir a recuperação da capacidade?

Resposta: A avaliação da integridade do equipamento.

**5. [facil · recordar]** Quando diferentes inibidores químicos podem ter sido usados em um caso de perda de produção, que informação sobre o produto precisa ser explicitada para interpretar corretamente o efeito esperado?

Resposta: A função do inibidor utilizado.

**6. [media · inferir]** Se a resistência ao escoamento aumenta por obstrução dentro da coluna de produção, além da vazão bruta, qual variável observada no poço pode refletir esse efeito?

Resposta: A pressão observada no poço.

**7. [dificil · decidir]** Um relatório traz apenas os sintomas finais da perda, como menor vazão e piora de qualidade, mas pretende atribuir causa. O que ainda precisa ser determinado para que o diagnóstico seja robusto?

Resposta: O mecanismo limitante, o ativo afetado e as condições em que esse mecanismo se torna dominante.

## 01_01 · bloco 016 · Condições que mudam o comportamento do risco no processamento primário

Status: `ok`

Exemplos recebidos: hotpotqa:5ae2e10a55429928c4239525 (dificil), pira_ptbr:A1339 (facil), PQ-04_01-07 (dificil), PQ-06_05-01 (facil), PQ-07_05-06 (media), arc_challenge:MDSA_2008_8_26 (media)

**1. [media · inferir]** No processamento primário de um FPSO, variáveis essenciais passam a ficar indisponíveis ou com leituras sem confiança. Sem outras mudanças, o que acontece com o risco de processo?

Resposta: O risco de processo aumenta.

**2. [media · inferir]** A estabilidade do processamento em um FPSO depende de intervenções manuais frequentes e alta carga de atenção do operador para manter as variáveis na faixa. Qual efeito essa condição tem sobre o risco de processo?

Resposta: Essa condição eleva o risco de processo.

**3. [media · decidir]** Em uma revisão de riscos do FPSO, desvios operacionalmente plausíveis ficaram fora do estudo. Essa revisão pode ser tratada como suficiente para manter o mesmo nível de risco?

Resposta: Não; omitir cenários plausíveis aumenta o risco de processo.

**4. [media · inferir]** Em uma unidade com medições críticas falhas, piora na separação óleo-água e forte dependência de intervenção manual, qual efeito comum dessas condições explica a maior vulnerabilidade a desvios?

Resposta: A redução da observabilidade do processo e da margem para detectar e corrigir desvios.

**5. [facil · recordar]** Quais recursos determinam quanto uma unidade consegue absorver uma perturbação antes de reduzir carga ou parar?

Resposta: Instrumentação, capacidade de segregação, inventário intermediário e flexibilidade operacional.

**6. [media · inferir]** Num FPSO com pouca capacidade de segregação, baixo inventário intermediário e flexibilidade operacional limitada, surge uma perturbação no processamento primário. O que tende a ocorrer antes do que em uma unidade mais robusta?

Resposta: Redução de carga ou parada, por menor capacidade de absorver a perturbação.

**7. [media · comparar]** Duas unidades têm a mesma designação de instalação, mas arranjos reais diferentes de instrumentação, segregação e inventário. A designação, sozinha, permite concluir que a capacidade de resposta é igual?

Resposta: Não; a capacidade de resposta deve ser avaliada no arranjo real.

## 01_01 · bloco 017 · Estrutura organizacional, gestão de mudanças e autonomia técnica

Status: `ok`

Exemplos recebidos: PQ-04_01-06 (media), hotpotqa:5abe98605542994516f453d1 (dificil), pira_ptbr:A807 (facil), PQ-07_04-07 (dificil), arc_challenge:NYSEDREGENTS_2004_4_5 (media), PQ-08_03-02 (facil)

**1. [facil · recordar]** Na gestão de riscos de uma FPSO ao longo da vida útil, o que é indispensável além das técnicas de análise?

Resposta: Uma estrutura organizacional capaz de sustentar a gestão de riscos.

**2. [facil · recordar]** Uma modificação operacional precisa ser avaliada, validada e incorporada à rotina com rastreabilidade. Qual prática de gestão deve suportar esse fluxo?

Resposta: Gestão de mudanças.

**3. [media · inferir]** Durante um desvio operacional, a equipe embarcada depende de apoio em terra, os documentos necessários não estão acessíveis e não há responsável técnico claramente definido. Qual efeito conjunto esse arranjo tende a produzir?

Resposta: Aumenta o tempo de resposta, atrasa decisões e dificulta validar mudanças.

**4. [media · inferir]** Em um desvio de processo, os procedimentos existem e os documentos estão atualizados. Para que os controles planejados sejam efetivos, que capacidade ainda precisa estar disponível na organização?

Resposta: Capacidade de interpretar o problema, autorizar ações e revisar premissas.

**5. [facil · recordar]** Após várias alterações acumuladas na planta, qual é a função da atualização documental no planejamento operacional?

Resposta: Manter a documentação coerente com a instalação real.

**6. [facil · recordar]** Além da estrutura formal, que elementos interferem na robustez e na resiliência do sistema de gestão de uma FPSO?

Resposta: O contexto organizacional, os fatores humanos e culturais e a comunicação contínua.

**7. [facil · recordar]** Em que condição a influência organizacional e humana se torna especialmente crítica para o sistema de gestão?

Resposta: Quando o risco é dinâmico e as condições mudam ao longo do tempo.

## 01_01 · bloco 018 · Monitoramento, revisão e aprendizagem para próximas intervenções

Status: `ok`

Exemplos recebidos: hotpotqa:5ab69d9f554299710c8d1eec (dificil), pira_ptbr:A1940 (facil), arc_challenge:Mercury_7175718 (media), PQ-02_10-05 (media), PQ-04_02-03 (facil), PQ-10_01-07 (dificil)

**1. [facil · recordar]** Na gestão de paradas de um FPSO, que documento consolida objetivo, escopo, prazos planejados e realizados, linha crítica, efetivo, homens-hora, contratos, custos, acidentes, desvios e lições aprendidas?

Resposta: O relatório final da parada.

**2. [facil · recordar]** Após uma intervenção em um FPSO, quais grupos de informação precisam ser registrados para permitir monitoramento contínuo do risco e revisão das decisões?

Resposta: O que foi planejado, o que ocorreu, os desvios surgidos e as lições que permanecem válidas para futuras intervenções.

**3. [facil · recordar]** Para o planejamento e o custo do ciclo de vida de um FPSO, o que esse registro passa a fornecer ao longo das intervenções?

Resposta: Memória operacional.

**4. [media · inferir]** Numa parada de FPSO, o plano original não previa estrutura complementar, mas a execução exigiu equipes e meios adicionais de retaguarda de forma decisiva. Que informação o registro deve preservar para melhorar futuras intervenções?

Resposta: Quais recursos de suporte foram efetivamente necessários.

**5. [media · decidir]** Ao usar dados consolidados de paradas anteriores para definir que problemas devem receber tratamento primeiro em um FPSO, que processo de gestão está sendo alimentado?

Resposta: A priorização por risco.

**6. [media · decidir]** Se os resultados de várias paradas mostram que a forma escolhida para cuidar dos ativos não evita certos desvios recorrentes, que classe de decisão deve ser revista com base nesse histórico?

Resposta: As estratégias de manutenção.

**7. [media · inferir]** Quando o aprendizado de intervenções é sustentado por cultura de segurança e monitoramento sistemático em um FPSO, qual efeito combinado é esperado sobre a organização?

Resposta: Menor repetição de falhas organizacionais e melhor qualidade da decisão futura.

**8. [media · diagnosticar]** Uma parada foi encerrada com todos os campos do documento preenchidos, mas sem confronto estruturado entre planejado e realizado nem exame das causas dos desvios. O que faltou para que o aprendizado tivesse aplicação prática?

Resposta: Disciplina documental e análise crítica real.

## 01_01 · bloco 019 · Seleção de sistemas críticos e uso de histórico de falhas

Status: `ok`

Exemplos recebidos: arc_challenge:ACTAAP_2008_7_10 (media), PQ-07_04-04 (media), PQ-02_10-07 (dificil), pira_ptbr:A901 (facil), hotpotqa:5a7e798155429934daa2fc2a (dificil), PQ-09_01-02 (facil)

**1. [facil · recordar]** Ao definir quais componentes e sistemas são críticos em um FPSO, que efeito isso deve ter sobre a gestão de risco da unidade?

Resposta: Orientar a implantação e a atualização dos controles de risco, definindo quais funções devem receber tratamento prioritário.

**2. [facil · recordar]** Ao examinar falhas e acidentes anteriores para selecionar sistemas críticos, que três tipos de evidência esse histórico pode fornecer?

Resposta: Mecanismos de processo, tipos de desvio e causas técnicas ou organizacionais já observadas.

**3. [facil · recordar]** Se uma equipe reúne eventos anteriores antes da revisão de criticidade de um FPSO, para que usos esse material serve nessa revisão?

Resposta: Para formular hipóteses de falha, revisar cenários e reconhecer funções sensíveis.

**4. [facil · recordar]** Quais exemplos de funções sensíveis são citados para a seleção de sistemas críticos em um FPSO?

Resposta: Separação de fluidos, medição e tratamento associado ao processo.

**5. [media · decidir]** Uma matriz corporativa classifica equipamentos por eventos passados, e a equipe quer aplicá-la sem ajuste a qualquer FPSO e em qualquer período de operação. Qual limitação técnica invalida essa transposição direta?

Resposta: Ela ignora que a criticidade não é universal: frequência e gravidade variam com configuração, regime operacional, manutenção, barreiras e contexto organizacional.

**6. [media · diagnosticar]** Na revisão de criticidade de uma unidade, a equipe decide classificar os sistemas apenas com base em falhas registradas em outras instalações e não faz verificação específica do ativo atual. Qual erro metodológico está sendo cometido?

Resposta: Usar o histórico como substituto da avaliação da instalação real; ele deve apenas informar a análise da unidade específica.

## 01_01 · bloco 021 · Confiabilidade, disponibilidade e suporte de manutenção

Status: `ok`

Exemplos recebidos: PQ-06_01-04 (media), arc_challenge:Mercury_7102270 (media), PQ-03_01-01 (facil), pira_ptbr:A1392 (facil), PQ-07_04-07 (dificil), hotpotqa:5ae1b75f554299492dc91b7d (dificil)

**1. [facil · recordar]** Em um FPSO, o que caracteriza a confiabilidade de um item?

Resposta: A capacidade de desempenhar a função requerida sob condições especificadas durante um intervalo de tempo.

**2. [facil · recordar]** Se um item de um FPSO precisa estar apto a executar sua função quando requerido e os recursos externos estão assegurados, quais dois fatores entram nessa capacidade além da confiabilidade?

Resposta: Mantenabilidade e suporte de manutenção.

**3. [media · inferir]** Em um FPSO, um equipamento tem bom histórico de falhas e reparo simples, mas depende de recurso externo não garantido para voltar a operar quando solicitado. Qual atributo fica comprometido?

Resposta: A disponibilidade.

**4. [media · decidir]** Dois itens de um FPSO têm a mesma probabilidade de falha. Um pode ter a função restaurada rapidamente com recursos locais; o outro exige vários dias e mobilização específica. Que aspecto deve diferenciar a decisão de adiar a manutenção?

Resposta: O tempo e os meios necessários para restaurar a função.

**5. [media · inferir]** Em uma unidade offshore, a recuperação de um item parado depende de logística complexa, especialista externo, sobressalente não disponível a bordo e condições de mobilização restritas. Qual é o efeito desses fatores?

Resposta: Eles aumentam o impacto da indisponibilidade.

**6. [facil · recordar]** Na engenharia de confiabilidade aplicada a equipamentos de um FPSO, para que servem as ferramentas dessa disciplina no ciclo do item?

Resposta: Para especificar, projetar, testar e demonstrar desempenho.

**7. [facil · recordar]** Para permitir troca de informação entre operador, fabricante e prestador de serviço de um FPSO, como devem ser organizados os dados de confiabilidade e manutenção?

Resposta: Em formato padronizado.

**8. [facil · recordar]** Quais dimensões decisórias a engenharia de confiabilidade ajuda a sustentar melhor em um FPSO?

Resposta: Decisões sobre risco, custo e desempenho operacional.

## 01_01 · bloco 022 · Consequências econômicas de controles insuficientes

Status: `ok`

Exemplos recebidos: PQ-04_01-07 (dificil), pira_ptbr:A1503 (facil), PQ-09_01-02 (facil), arc_challenge:Mercury_7017133 (media), PQ-07_05-06 (media), hotpotqa:5ade816b5542992fa25da7a1 (dificil)

**1. [media · inferir]** Em um FPSO, falhas no autodiagnóstico, nas ações contingenciais e nas medidas corretivas compatíveis com o risco podem levar a que medida extrema sobre a unidade?

Resposta: À interdição da instalação.

**2. [facil · recordar]** Além da segurança e da conformidade operacional, a decisão sobre controle de risco afeta qual dimensão econômica do ativo?

Resposta: O custo ao longo da vida útil do ativo.

**3. [media · inferir]** Mantidos constantes a duração da parada forçada e o escopo corretivo, o que tende a ocorrer com a perda potencial quando a unidade tem maior produção?

Resposta: Tende a crescer, porque a receita diária comprometida durante a parada forçada é maior.

**4. [facil · recordar]** Após uma parada forçada, além do efeito direto sobre a produção, que necessidade excepcional de deslocamento de recursos pode surgir?

Resposta: Mobilização extraordinária.

**5. [facil · comparar]** Na comparação entre gasto preventivo e custo de falha, quais efeitos acumulados precisam entrar na análise além do desembolso imediato?

Resposta: O efeito acumulado de indisponibilidade, correções emergenciais e restrições operacionais.

**6. [facil · decidir]** Um exemplo econômico observado em uma instalação específica pode ser usado como método universal de cálculo para qualquer FPSO?

Resposta: Não; variam duração da parada, capacidade produtiva, escopo corretivo e contexto contratual.

## 01_01 · bloco 023 · Análise de causa: mecanismo de falha, modo de falha e FMEA

Status: `ok`

Exemplos recebidos: PQ-10_01-02 (facil), arc_challenge:Mercury_SC_407137 (media), pira_ptbr:A524 (facil), hotpotqa:5ae48cf55542995ad6573d73 (dificil), PQ-03_01-05 (media), PQ-05_02-07 (dificil)

**1. [media · diagnosticar]** Em uma análise de falhas, a equipe registrou "ataque químico no elastômero" como o processo que levou à perda de vedação. Essa classificação corresponde a quê?

Resposta: Ao mecanismo de falha.

**2. [media · diagnosticar]** Em uma análise de falhas, a equipe registrou "não parte ao comando" para descrever como a perda de função apareceu no equipamento. Essa classificação corresponde a quê?

Resposta: Ao modo de falha.

**3. [facil · recordar]** Numa FMEA, a planilha já lista modos de falha e efeitos. Quais outros dois elementos centrais ainda devem constar nessa avaliação?

Resposta: Causas e controles.

**4. [media · decidir]** Uma FMEA de um sistema de utilidades foi conduzida apenas pela manutenção, sem participação de outras áreas. Que composição de equipe o método requer?

Resposta: Uma equipe multidisciplinar.

**5. [media · diagnosticar]** Na FMEA, o histórico usado pela equipe não permite identificar origem, data nem vínculo com o equipamento avaliado. Qual requisito da aplicação não está atendido?

Resposta: Dados rastreáveis.

**6. [media · diagnosticar]** Durante a FMEA, operação e manutenção descrevem funções diferentes para o mesmo sistema e, por isso, avaliam as falhas de forma incompatível. Que condição necessária está faltando?

Resposta: Entendimento comum das funções analisadas.

**7. [media · inferir]** Em uma abordagem que usa NPR, um modo de falha recebeu severidade 7, ocorrência 3 e detecção 2. Qual é o NPR?

Resposta: 42.

**8. [dificil · decidir]** Dois modos de falha receberam NPR 60 por combinações diferentes de severidade, ocorrência e detecção. A equipe quer tratá-los como equivalentes e encerrar a análise sem revisar individualmente as consequências críticas. Isso é suficiente?

Resposta: Não. O NPR só apoia a triagem; combinações distintas podem gerar o mesmo valor e não substituem a análise individual de consequências críticas.

## 02_02 · bloco 000 · Como selecionar e aplicar: bottle test como triagem empírica

Status: `ok`

Exemplos recebidos: PQ-05_01-02 (facil), hotpotqa:5ab9b8c8554299743d22ebc8 (dificil), PQ-07_04-07 (dificil), PQ-04_02-04 (media), pira_ptbr:B2085 (facil), arc_challenge:LEAP__5_10318 (media)

**1. [facil · recordar]** Qual é a função do bottle test na seleção inicial de desemulsificantes?

Resposta: Comparar, como triagem empírica, a resposta da emulsão a diferentes produtos e dosagens em condições controladas.

**2. [facil · recordar]** Em uma bateria de bottle tests, por que deve existir uma amostra sem aditivo?

Resposta: Para avaliar a separação natural da emulsão e servir de referência para as amostras tratadas.

**3. [facil · recordar]** Nas amostras tratadas do bottle test, quais quatro condições precisam ser controladas para comparar os resultados?

Resposta: Temperatura, mistura, concentração do produto e tempo de observação.

**4. [facil · recordar]** Além do volume de água separada, quais dois aspectos visuais devem ser registrados no bottle test?

Resposta: O aspecto das fases e a qualidade da interface.

**5. [media · comparar]** Mantidos produto, dose e condições de ensaio, o que se avalia em uma emulsão água-em-óleo e o que se avalia em uma óleo-em-água?

Resposta: Na água-em-óleo, avalia-se a liberação da água dispersa do petróleo; na óleo-em-água, a clarificação da fase aquosa.  
_usa apoio_

**6. [facil · recordar]** Ao montar o bottle test para selecionar um produto, o que o ensaio deve reproduzir, na medida do possível?

Resposta: O fluido e as condições relevantes do processo.

**7. [media · inferir]** Um desemulsificante foi escolhido em bancada, mas o desempenho mudou no FPSO. Que etapa ainda era necessária antes da adoção definitiva e por qual motivo técnico?

Resposta: Validação operacional, porque cisalhamento, tempo de residência e composição real podem alterar o desempenho do produto.  
_usa apoio_

## 02_02 · bloco 003 · Por que pH, salmoura, petróleo e asfaltenos mudam o desempenho

Status: `ok`

Exemplos recebidos: pira_ptbr:A1288 (facil), PQ-06_01-04 (media), hotpotqa:5ab1f75d554299340b525443 (dificil), PQ-07_04-07 (dificil), arc_challenge:CSZ30771 (media), PQ-01_01-03 (facil)

**1. [facil · recordar]** De quais elementos depende a estabilidade de uma emulsão nesse contexto de processamento?

Resposta: Da composição do petróleo, da salmoura e do filme interfacial.

**2. [media · inferir]** Em testes com o mesmo petróleo e o mesmo produto químico, apenas o pH e a salinidade da água mudaram e a resposta de separação também mudou. Que conjunto de propriedades na interface foi afetado?

Resposta: Carga elétrica, solvatação e adsorção de espécies na interface.

**3. [media · diagnosticar]** No trem de tratamento de um FPSO, a emulsão permanece muito estável e as gotas não coalescem; a análise do fluido mostra alto teor de asfaltenos e sólidos. Qual barreira física explica essa resistência?

Resposta: Filmes resistentes em torno das gotas, formados por asfaltenos e sólidos.

**4. [media · inferir]** Se um químico reorganiza a camada ao redor das gotas, qual etapa imediata da separação ele favorece?

Resposta: A drenagem entre gotas em contato.

**5. [media · comparar]** Mantidos o mesmo equipamento, a mesma temperatura e a mesma dosagem, compare as afirmações: "reduzir o pH sempre melhora a separação" e "aumentar a salinidade sempre melhora a separação".

Resposta: Nenhuma é universal; o efeito depende da formulação e do fluido.

**6. [media · decidir]** Para escolher entre dois desemulsificantes para um FPSO, os ensaios foram feitos com fluido e água que não representam a operação real. Que condição essencial faltou para sustentar a escolha?

Resposta: Comparar os produtos nas condições representativas do sistema.

## 02_02 · bloco 006 · Como o antiespumante atua na quebra da espuma

Status: `ok`

Exemplos recebidos: PQ-06_03-01 (facil), pira_ptbr:A1070 (facil), hotpotqa:5adcf0955542992c1e3a24c7 (dificil), PQ-09_01-04 (media), arc_challenge:Mercury_SC_400338 (media), PQ-04_01-07 (dificil)

**1. [facil · recordar]** Para atuar na quebra da espuma em um separador, a que estrutura da bolha o antiespumante precisa chegar?

Resposta: Ao filme que estabiliza a bolha.

**2. [facil · recordar]** Quais três comportamentos do antiespumante governam sua atuação efetiva sobre a espuma?

Resposta: Espalhamento, penetração e dispersão.

**3. [media · inferir]** Mantida a mesma dose, um antiespumante perde eficiência após mudança na composição do fluido do separador. Além da formulação do produto, que característica do sistema pode explicar a mudança de desempenho?

Resposta: As propriedades da interface gás-líquido.

**4. [media · diagnosticar]** Se o fluido passa a conter mais tensoativos, sais ou sólidos, quais dois aspectos decisivos para o controle químico da espuma podem ser alterados diretamente?

Resposta: A estabilidade da espuma e a facilidade de contato do antiespumante com o filme.

**5. [facil · decidir]** Uma faixa de dosagem validada para um fluido pode ser adotada automaticamente em outro sistema apenas porque o produto é o mesmo?

Resposta: Não. A resposta à dose do antiespumante não é universal.

**6. [media · inferir]** Em um teste operacional, elevar a concentração melhorou o controle de espuma até certo ponto. O que não pode ser concluído sobre aumentos adicionais de concentração?

Resposta: Que continuarão aumentando o desempenho.

**7. [media · decidir]** Ao propor nova elevação de dose para reduzir espuma remanescente, qual suposição sobre o restante do processo é tecnicamente indevida?

Resposta: Supor que não haverá efeitos no restante do processo.

**8. [media · decidir]** Após aumento de salinidade e de teor de sólidos, a faixa de dose antes usada deixou de controlar a espuma de forma consistente. Qual ajuste no produto passa a ser tecnicamente justificável antes de insistir apenas em mais dose?

Resposta: Revisar a formulação do antiespumante.  
_usa apoio_

## 02_02 · bloco 009 · Interações e efeitos colaterais relevantes no processamento

Status: `ok`

Exemplos recebidos: PQ-07_05-06 (media), PQ-01_01-03 (facil), arc_challenge:Mercury_7085908 (media), hotpotqa:5adf03f35542995ec70e8f55 (dificil), pira_ptbr:A877 (facil), PQ-05_02-07 (dificil)

**1. [facil · recordar]** Na escolha de um antiespumante para o processamento em um FPSO, quais componentes da corrente produzida devem ser considerados por poderem mudar o desempenho do produto?

Resposta: Tensoativos naturais do óleo, sólidos produzidos e sais dissolvidos.

**2. [media · inferir]** Em um separador de produção de FPSO, a quebra de espuma melhora sem outras alterações relevantes. Qual efeito tende a ocorrer na corrente de gás de saída?

Resposta: Redução do arraste de líquido na saída de gás.

**3. [media · diagnosticar]** Após a injeção do antiespumante ser transferida para um ramal de baixo escoamento antes do separador, a mesma dose passa a dar resultado irregular, sem mudança do fluido ou da formulação. Que mecanismo explica essa instabilidade?

Resposta: Distribuição insuficiente do produto por falta de mistura adequada antes do vaso.

**4. [media · diagnosticar]** Em outro caso, a dispersão a montante está adequada, mas o ponto de injeção foi movido para muito depois da região em que a espuma se forma no processo. A dose e a formulação não mudaram. Qual causa explica a perda de consistência do controle?

Resposta: O antiespumante deixou de alcançar a interface crítica onde precisa atuar.

**5. [media · comparar]** Dois antiespumantes controlam igualmente a espuma no primeiro separador de um FPSO. Mantido igual esse resultado local, um contém fase oleosa e emulsificantes e o outro não. Qual deles exige maior atenção no restante do processamento?

Resposta: O que contém fase oleosa e emulsificantes, pelo maior potencial de alterar o comportamento de interfaces em outros equipamentos.

**6. [media · inferir]** Sem trocar equipamentos nem formulação, a composição do fluido produzido de um FPSO muda ao longo da vida do campo. Qual consequência isso pode trazer para o comportamento da espuma?

Resposta: Pode deslocar o equilíbrio entre formação e quebra de espuma.

**7. [dificil · decidir]** Um antiespumante funcionou bem no início da campanha. Meses depois mudam corte de água, produção de sólidos, salinidade, temperatura e regime operacional, sem falha na injeção química. Qual decisão é tecnicamente correta?

Resposta: Rever o programa químico, sem assumir que o desempenho inicial continuará estável.

## 02_02 · bloco 012 · Por que esses químicos funcionam na água produzida

Status: `ok`

Exemplos recebidos: arc_challenge:Mercury_7056613 (media), pira_ptbr:A1600 (facil), hotpotqa:5a8cab59554299653c1aa0e4 (dificil), PQ-08_02-04 (media), PQ-09_01-02 (facil), PQ-05_02-07 (dificil)

**1. [facil · recordar]** Na água produzida de um FPSO, que fatores costumam manter estáveis gotas finas de óleo e matéria coloidal antes do condicionamento químico?

Resposta: Repulsão elétrica, filmes interfaciais resistentes e baixa frequência de colisão efetiva.

**2. [media · inferir]** Em um FPSO, a água produzida apresenta gotas finas de óleo cuja estabilidade é dominada por repulsão elétrica. Que ação do coagulante atua diretamente sobre essa barreira?

Resposta: Neutralizar cargas ou comprimir a dupla camada elétrica.

**3. [media · comparar]** Mantidas a mesma água produzida e a mesma etapa posterior de separação, qual é a diferença funcional entre um coagulante e um floculante polimérico?

Resposta: O coagulante desestabiliza a dispersão; o floculante conecta entidades desestabilizadas para formar flocos.

**4. [facil · recordar]** Após a aplicação de um floculante polimérico em água produzida já condicionada, que propriedades dos flocos tendem a aumentar?

Resposta: O tamanho e a resistência mecânica dos flocos.

**5. [media · inferir]** Em um trem de tratamento de água produzida que segue para flotação por ar dissolvido, qual efeito do condicionamento químico bem-sucedido é esperado na interação com as microbolhas?

Resposta: Captura mais fácil dos agregados, com subida mais rápida da fase oleosa.

**6. [media · decidir]** No tratamento de água produzida com desestabilização química seguida de flotação, aumentar apenas a vazão garante maior remoção de óleo se a dose e as condições de geração de bolhas permanecerem inalteradas?

Resposta: Não; a remoção depende da otimização conjunta de dose, carga de óleo, vazão e condições de geração de bolhas.  
_usa apoio_

**7. [media · decidir]** Um fornecedor propõe trocar um coagulante sintético por um natural porque ambos atuam por neutralização de carga e agregação. O que ainda precisa ser demonstrado antes de adotar a troca na água produzida da unidade?

Resposta: A equivalência de desempenho na água produzida de interesse.

## 02_02 · bloco 015 · Consequências e interações relevantes para o descarte

Status: `ok`

Exemplos recebidos: arc_challenge:Mercury_SC_401002 (media), pira_ptbr:B2458 (facil), PQ-07_05-06 (media), PQ-03_02-08 (dificil), hotpotqa:5a7f21185542993067513651 (dificil), PQ-09_01-02 (facil)

**1. [facil · recordar]** No tratamento da água produzida para descarte, além da remoção de óleo, o que a escolha e a dosagem do programa químico modificam de forma abrangente?

Resposta: O perfil do efluente tratado.

**2. [facil · recordar]** Quais duas características do efluente tratado podem ser alteradas por coagulantes e floculantes, além da remoção de óleo?

Resposta: Carbono orgânico residual e sólidos suspensos remanescentes.

**3. [facil · recordar]** Que aspecto operacional do lodo pode mudar com o uso de coagulantes e floculantes no tratamento da água produzida?

Resposta: A facilidade de desaguamento do lodo.

**4. [media · inferir]** Um mesmo agente melhora a quebra de emulsão em uma água produzida, mas em outra passa a piorar a separação. Qual mudança interfacial oposta explica esse resultado?

Resposta: Ele pode estabilizar a interface nessa outra água.

**5. [media · decidir]** Em um FPSO, mudou o programa químico de produção e, sem alteração mecânica na flotação, o tratamento da água produzida perdeu desempenho. Qual variável do tratamento deve ser revista primeiro?

Resposta: A dosagem ótima do programa químico do tratamento da água produzida.

**6. [media · inferir]** Resíduos de químicos de produção passaram a reduzir a captura de gotas pela flotação, sem mudança de hardware. Qual mecanismo interfacial citado pode ter sido afetado diretamente?

Resposta: A aderência das gotas às bolhas.

**7. [facil · decidir]** Em operação offshore, quando o desempenho do tratamento da água produzida para descarte deve ser reavaliado?

Resposta: Sempre que houver alteração relevante de fluido, de regime de escoamento ou de configuração da flotação.

## 02_02 · bloco 018 · Papel dos inibidores de incrustação e limites de aplicação em sistemas com URS

Status: `ok`

Exemplos recebidos: pira_ptbr:A230 (facil), arc_challenge:Mercury_417139 (media), PQ-03_01-05 (media), PQ-05_01-07 (dificil), hotpotqa:5ade2ee75542997c77adeda2 (dificil), PQ-04_02-03 (facil)

**1. [facil · recordar]** No controle de depósitos minerais em processo, em que estágio do fenômeno os inibidores de incrustação são destinados a atuar prioritariamente?

Resposta: Antes de a incrustação se estabelecer; atuam de forma essencialmente preventiva.

**2. [media · inferir]** Se já houver cristais presentes no sistema, que efeito do inibidor é descrito sobre eles?

Resposta: Efeitos de distorção e dispersão dos cristais.

**3. [facil · recordar]** Quais fatores são citados como condicionantes da eficiência de um inibidor de incrustação?

Resposta: pH, compatibilidade com cálcio, presença de quelantes, massa molecular e estabilidade química e térmica.

**4. [media · inferir]** Uma FPSO possui URS, mas a planta de processo continua sujeita a um depósito que a remoção de sulfato não elimina. Qual função cabe ao inibidor nesse caso?

Resposta: Compensar incrustações não resolvidas pela remoção de sulfato, como CaCO3 na planta de processo.

**5. [media · inferir]** Em uma URS, qual corrente deve receber atenção por concentrar espécies incrustantes e poder precipitar um sal de cálcio pouco solúvel?

Resposta: A corrente concentrada rica em sulfato, com potencial de precipitação de CaSO4.

**6. [media · inferir]** Um inibidor é dosado somente na água de injeção para proteger o processo de produção. Qual limitação pode impedir que ele cumpra esse objetivo?

Resposta: Ele pode adsorver na rocha ao redor do poço injetor e não alcançar o poço produtor.

**7. [facil · recordar]** Sem unidade de dessulfatação, além dos pontos de mistura de águas incompatíveis, quais equipamentos são citados como necessitando proteção por inibidor?

Resposta: Trocadores de calor e bombas.

## 02_02 · bloco 021 · Sequestrante químico: bissulfito de sódio, mecanismo e limitações

Status: `ok`

Exemplos recebidos: pira_ptbr:A1214 (facil), PQ-05_01-07 (dificil), PQ-07_01-03 (facil), hotpotqa:5ae3ef1e5542995dadf2425f (dificil), arc_challenge:VASoL_2007_5_28 (media), PQ-01_01-05 (media)

**1. [facil · recordar]** No condicionamento de água, qual espécie dissolvida é consumida pelo bissulfito de sódio?

Resposta: Oxigênio dissolvido.

**2. [media · inferir]** Duas correntes serão tratadas com bissulfito sob a mesma meta de desoxigenação. Se uma delas chega com maior teor do componente consumido pelo reagente, como muda a dosagem requerida nessa corrente?

Resposta: Ela aumenta, porque a necessidade de bissulfito cresce com a carga de oxigênio a remover.

**3. [media · inferir]** Em uma unidade de tratamento de água, a injeção de bissulfito fica abaixo da demanda calculada para a corrente. Qual resultado tende a permanecer após o tratamento?

Resposta: Residual de oxigênio no sistema.

**4. [media · inferir]** Um lote de bissulfito preparado para dosagem permanece armazenado por longo período com contato frequente com a atmosfera. Sem mudar a receita de preparo, qual propriedade do lote pode deixar de se manter?

Resposta: A concentração ativa.

**5. [facil · recordar]** Qual característica da solução diluída de bissulfito explica sua tendência corrosiva para muitos materiais?

Resposta: O baixo pH.

**6. [facil · recordar]** Ao aplicar bissulfito em um arranjo de processo, quais aspectos devem ser avaliados em conjunto além da remoção química?

Resposta: Eficiência de desoxigenação, efeito sobre pH, compatibilidade metalúrgica e controle de residual.

## 02_02 · bloco 024 · Condições que mudam o comportamento: cloro residual, CO2 e disponibilidade de gás

Status: `ok`

Exemplos recebidos: arc_challenge:VASoL_2007_5_28 (media), PQ-05_01-06 (media), PQ-04_01-07 (dificil), pira_ptbr:A934 (facil), PQ-10_01-02 (facil), hotpotqa:5a8efecc5542997ba9cb3177 (dificil)

**1. [facil · recordar]** Na escolha e no desempenho de um processo de desoxigenação de água em um FPSO, quais dois grupos de fatores são determinantes gerais?

Resposta: A química da água e as utilidades disponíveis.

**2. [media · inferir]** Em um sistema que usa bissulfito ou sulfito como sequestrante, a dosagem foi mantida, mas a água passou a chegar com cloro residual em excesso. O que acontece com a parcela do reagente que ainda resta para remover oxigênio dissolvido?

Resposta: Ela diminui, porque parte do bissulfito ou sulfito reage com o cloro residual.

**3. [media · inferir]** Em água do mar tratada por desaeração a vácuo, qual efeito secundário teórico pode aparecer quando as condições favorecem a remoção de CO2 dissolvido?

Resposta: Precipitação de carbonato de cálcio.

**4. [facil · recordar]** Ao avaliar o uso de stripping a gás para desoxigenação em um FPSO, quais três itens da corrente gasosa precisam ser verificados?

Resposta: Disponibilidade, composição e destino seguro da corrente gasosa.

**5. [media · decidir]** Mantida a mesma meta de desoxigenação, qual rota passa a ser alternativa se não houver gás de arraste disponível ou adequado?

Resposta: A rota a vácuo.

**6. [media · decidir]** Em um projeto de FPSO, quando pode fazer sentido adotar um sistema combinado de desoxigenação em vez de uma única rota?

Resposta: Quando o projeto precisa conciliar o balanço de remoção com as restrições de espaço, peso e utilidades.

## 02_02 · bloco 027 · Função do controle microbiológico na água de injeção

Status: `ok`

Exemplos recebidos: PQ-09_02-09 (dificil), PQ-10_01-02 (facil), pira_ptbr:A942 (facil), hotpotqa:5a8a27df55429930ff3c0cc4 (dificil), PQ-03_01-05 (media), arc_challenge:Mercury_7143045 (media)

**1. [facil · recordar]** Qual é a função técnica do controle microbiológico na água de injeção?

Resposta: Limitar a contaminação, o crescimento e a atividade de microrganismos no sistema.

**2. [facil · recordar]** Além de favorecer biofilme e corrosão microbiologicamente influenciada, que efeito operacional o controle microbiológico na água de injeção busca limitar?

Resposta: Souring.

**3. [facil · recordar]** Qual grupo microbiano é particularmente relevante na água de injeção por converter sulfato em sulfeto?

Resposta: As bactérias redutoras de sulfato, BRS.

**4. [facil · recordar]** Além das células dispersas na fase aquosa, em que regiões do sistema a contaminação microbiológica também pode se estabelecer?

Resposta: Em superfícies internas de linhas, tanques, filtros, tubulações e poços.

**5. [media · comparar]** Mantidos o mesmo biocida, a mesma dosagem e a mesma carga microbiana, a migração da população da fase aquosa para superfícies internas tende a facilitar ou dificultar o tratamento químico?

Resposta: Dificultar, porque a biomassa aderida em biofilme fica menos acessível ao tratamento.

**6. [media · inferir]** Se microrganismos aderidos se concentram em nichos protegidos do escoamento, o que tende a ocorrer mesmo com aplicação de biocida?

Resposta: Eles podem persistir, por ficarem protegidos do escoamento e da ação do biocida.

**7. [media · inferir]** Sem trocar o produto químico, um sistema de água de injeção passa a ter mais depósito e incrustação interna. Como tende a variar o desempenho do programa microbiológico?

Resposta: Tende a piorar, porque o desempenho também depende da quantidade de depósito ou incrustação no sistema.

**8. [dificil · diagnosticar]** Em uma linha de aço de água de injeção, a contagem de células planctônicas cai após o tratamento, mas a corrosão interna persiste; há depósitos e trechos de baixo escoamento. Que condição microbiológica explica melhor esse quadro?

Resposta: Microrganismos aderidos em biofilme, incluindo BRS, persistindo em nichos protegidos e menos acessíveis ao biocida.

## 02_02 · bloco 029 · Por que biofilme, incrustação e depósitos reduzem a eficácia

Status: `ok`

Exemplos recebidos: pira_ptbr:B2569 (facil), PQ-01_01-02 (facil), hotpotqa:5ac2a1a7554299657fa28ff1 (dificil), arc_challenge:Mercury_7085243 (media), PQ-07_04-07 (dificil), PQ-03_01-05 (media)

**1. [media · diagnosticar]** Em um trecho de água de injeção, a dosagem aplicada está dentro do planejado, mas permanecem depósitos aderidos às superfícies internas e a população microbiana se mantém nesses pontos. Que mecanismo explica essa persistência?

Resposta: Os depósitos criam regiões inacessíveis onde o biocida não chega adequadamente.

**2. [media · decidir]** Em um circuito de injeção tratado por longo período com o mesmo produto, que condição do sistema ajuda a evitar nichos em que bactérias proliferem e ganhem resistência?

Resposta: Manter o sistema de injeção limpo, sem locais inacessíveis e depósitos.

**3. [media · comparar]** Sem alterar o produto, compare o controle esperado sobre células livres na água e sobre uma comunidade microbiana aderida à parede interna. Em qual condição o desempenho tende a ser insuficiente?

Resposta: Na comunidade aderida como biofilme, porque ela dificulta a penetração do produto.

**4. [media · comparar]** Se a comunidade microbiana aderida ainda estiver coberta por incrustação mineral e sulfeto de ferro, como a dosagem necessária se compara à usada para células livres?

Resposta: Tende a ser maior do que a usada para células livres.

**5. [facil · recordar]** Além da concentração, qual parâmetro de aplicação citado afeta diretamente o desempenho do tratamento químico?

Resposta: O tempo de contato.

**6. [media · comparar]** Duas linhas de água de injeção operam sob escoamento, com a mesma água e o mesmo tratamento; uma apresenta superfície interna mais rugosa. Em qual delas a formação de biofilme tende a ser mais favorecida?

Resposta: Na linha de superfície interna mais rugosa.

**7. [media · decidir]** Em um ponto corroído do sistema, foram detectadas bactérias, mas não houve avaliação integrada do depósito presente, da química da água nem da suscetibilidade do material. Isso basta para atribuir a causa do ataque às bactérias?

Resposta: Não. A presença isolada de bactérias não demonstra a causa do ataque corrosivo.

## 02_02 · bloco 032 · Como a inibição funciona e quais limites mecanísticos importam

Status: `ok`

Exemplos recebidos: arc_challenge:Mercury_7122570 (media), pira_ptbr:A1471 (facil), PQ-08_02-04 (media), hotpotqa:5a8c72815542995e66a475f4 (dificil), PQ-05_02-07 (dificil), PQ-10_01-02 (facil)

**1. [facil · recordar]** Na prevenção de hidratos em sistemas topside e subsea de um FPSO, como o MEG é classificado quanto ao tipo de inibição?

Resposta: Como inibidor termodinâmico.

**2. [facil · recordar]** Qual é o mecanismo técnico pelo qual o MEG dificulta a formação de hidratos?

Resposta: Reduz a atividade da água e desloca o equilíbrio de formação de hidratos para condições mais severas.

**3. [media · inferir]** Mantidas a mesma pressão e a mesma composição do gás, o que uma concentração adequada de MEG permite quanto à temperatura de operação antes da condição de equilíbrio do hidrato ser atingida?

Resposta: Permite operar em temperaturas mais baixas antes de atingir a condição de equilíbrio do hidrato.

**4. [facil · comparar]** Para avaliar a proteção contra hidratos, o que é mais determinante: a vazão nominal de injeção de MEG ou sua concentração efetiva na água livre?

Resposta: A concentração efetiva do MEG na água livre.

**5. [media · inferir]** Em uma linha subsea, a vazão nominal de injeção de MEG e a distribuição do produto permanecem inalteradas, mas a quantidade de água produzida aumenta. Sem reajuste de dosagem, o que acontece com a proteção contra hidratos?

Resposta: A proteção diminui, porque o aumento de água produzida dilui o MEG na água livre e reduz sua concentração efetiva.

**6. [media · diagnosticar]** Em um conjunto com vários ramos, a vazão nominal total de MEG está correta e a quantidade de água livre não mudou, mas apenas um ramo apresenta hidrato. Que falha do uso do MEG explica essa proteção desigual?

Resposta: Distribuição não uniforme do MEG, por mistura insuficiente ou falha de distribuição, deixando esse ramo sem proteção efetiva.

**7. [media · decidir]** Mesmo quando o histórico térmico do escoamento e o transporte de massa indiquem menor propensão imediata à nucleação, qual avaliação continua obrigatória para definir a proteção contra hidratos?

Resposta: A avaliação do equilíbrio de formação de hidratos e da margem operacional.

## 02_02 · bloco 035 · Seleção, monitoramento e alternativas de regeneração

Status: `ok`

Exemplos recebidos: PQ-01_01-02 (facil), PQ-04_02-09 (dificil), arc_challenge:NYSEDREGENTS_2004_4_9 (media), pira_ptbr:A765 (facil), PQ-07_05-06 (media), hotpotqa:5a8b879355429949d91db5cd (dificil)

**1. [facil · recordar]** Num FPSO, o programa de MEG não pode ser ajustado apenas para evitar hidratos. Que segundo objetivo precisa ser conciliado com essa proteção?

Resposta: O controle de sais na recuperação do MEG.

**2. [media · inferir]** A concentração de glicol medida na fase aquosa caiu. Qual variável também monitorada ajuda a verificar se a mudança está ligada à água no circuito?

Resposta: O balanço de água.

**3. [media · diagnosticar]** Em um circuito de MEG, um trecho passou a limitar vazão e um trocador deixou de entregar o desempenho esperado. Quais frentes do monitoramento foram afetadas?

Resposta: Restrições hidráulicas e troca térmica.

**4. [facil · recordar]** Qual é a finalidade operacional da regeneração no circuito de MEG?

Resposta: Remover água para permitir o reúso do glicol.

**5. [media · decidir]** Uma unidade já entrega glicol apto ao reúso após a etapa de regeneração, mas isso não encerra outra decisão de tratamento na recuperação. Qual decisão ainda precisa ser avaliada separadamente?

Resposta: Se há necessidade de remoção de sais.

**6. [facil · recordar]** Mantido o mesmo circuito, quais variáveis operacionais influenciam simultaneamente a separação e o consumo de energia?

Resposta: Temperatura, pressão e carga.

**7. [media · inferir]** Na seleção de uma alternativa de regeneração, por que não se deve prometer para o arranjo industrial o mesmo desempenho obtido com uma mistura simplificada de laboratório?

Resposta: Porque a seleção deve considerar o circuito real, incluindo sais, sólidos e hidrocarbonetos, que pode ter desempenho diferente.

## 02_02 · bloco 038 · Função dos químicos no tratamento do gás

Status: `ok`

Exemplos recebidos: PQ-07_04-07 (dificil), pira_ptbr:B2507 (facil), PQ-04_02-03 (facil), hotpotqa:5a77e77d5542992a6e59dfec (dificil), PQ-03_03-04 (media), arc_challenge:VASoL_2009_3_10 (media)

**1. [facil · recordar]** Por que os produtos químicos usados no tratamento do gás não devem ser tratados como intercambiáveis entre todos os serviços?

Resposta: Porque o mecanismo de cada produto atua sobre um problema distinto.

**2. [media · decidir]** Em um trecho do sistema de gás onde a fase aquosa está acelerando o ataque ao material metálico, qual classe de químico deve ser priorizada?

Resposta: Inibidor de corrosão de gás.

**3. [media · decidir]** Se a ameaça dominante em uma corrente de gás é a presença de sulfeto de hidrogênio, qual produto deve ser aplicado?

Resposta: Sequestrante de H2S.

**4. [facil · recordar]** Quando o objetivo principal é remover CO2 da corrente e também contribuir para o adoçamento do gás, que tipo de químico é empregado?

Resposta: Solvente de absorção, como alcanolaminas.

**5. [media · inferir]** Dois produtos químicos diferentes estão em uso no mesmo sistema de processo de gás. Quais aspectos de aplicação não precisam coincidir entre eles?

Resposta: Corrente, concentração e ponto de injeção.

**6. [facil · decidir]** Ao definir um produto para um trecho específico do sistema de gás, qual critério técnico deve prevalecer?

Resposta: A ameaça dominante naquele trecho.

**7. [media · inferir]** Qual ameaça dominante torna relevante o uso de antiespumante em um trecho do tratamento do gás?

Resposta: Tendência a espuma.

**8. [media · inferir]** Qual ameaça dominante torna relevante o uso de MEG em um trecho do tratamento do gás?

Resposta: Risco de hidrato.

## 02_02 · bloco 041 · Compatibilidade química: por que a combinação pode melhorar ou piorar a proteção

Status: `ok`

Exemplos recebidos: PQ-09_02-06 (media), hotpotqa:5adf60735542993344016c64 (dificil), arc_challenge:Mercury_SC_401254 (media), PQ-07_01-03 (facil), pira_ptbr:B2331 (facil), PQ-10_01-07 (dificil)

**1. [facil · decidir]** Ao selecionar dois produtos para uso conjunto no tratamento do gás de um FPSO, basta a função declarada de cada um para concluir que eles se comportarão de forma compatível?

Resposta: Não; a função declarada de cada produto não basta para concluir compatibilidade.

**2. [facil · recordar]** Quais mecanismos de interação entre químicos são citados como capazes de alterar a proteção anticorrosiva?

Resposta: Competição de adsorção, alteração de pH, precipitação e modificação da estabilidade do filme protetor.

**3. [facil · decidir]** Quando dois químicos são usados juntos, a proteção anticorrosiva combinada necessariamente se reduz?

Resposta: Não; ela pode melhorar, preservar ou reduzir a proteção anticorrosiva.

**4. [media · inferir]** Se a mesma combinação química apresenta resultados anticorrosivos diferentes em dois ensaios, a que essa variação pode ser atribuída segundo o texto?

Resposta: À formulação e ao meio.

**5. [facil · comparar]** Em um teste de compatibilidade para uso em serviço, quais três elementos do ensaio devem representar o sistema real?

Resposta: As concentrações, os materiais e o fluido.

**6. [facil · decidir]** Uma salmoura preparada somente com NaCl reproduz integralmente a água do mar e uma água produzida multissalina para avaliar compatibilidade?

Resposta: Não; ela não reproduz integralmente nenhum dos dois meios.

**7. [facil · recordar]** Quais classes de produtos o texto cita explicitamente como passíveis de interação em compatibilidade química?

Resposta: Inibidores de corrosão, inibidores de incrustação e sequestrantes de H2S.

## 02_02 · bloco 044 · Alternativas ao squeeze para controle de incrustação

Status: `ok`

Exemplos recebidos: arc_challenge:Mercury_7071838 (media), PQ-08_02-04 (media), hotpotqa:5a75ebe6554299109176e5d2 (dificil), pira_ptbr:A664 (facil), PQ-05_01-02 (facil), PQ-04_02-09 (dificil)

**1. [facil · recordar]** Em um FPSO, a previsão de incrustação está ligada ao sulfato presente na água que será injetada no reservatório. Que alternativa preventiva de processo atua diretamente nessa causa do risco?

Resposta: Uma Unidade de Remoção de Sulfato (URS).

**2. [media · inferir]** Se o teor de sulfato da água de injeção for reduzido antes da injeção, qual é o efeito esperado sobre a formação de BaSO4 e SrSO4?

Resposta: Diminui, podendo até eliminar, a condição necessária para a precipitação desses sais.

**3. [facil · recordar]** Qual elemento de separação realiza a remoção seletiva de sulfato nessa alternativa preventiva?

Resposta: Membranas adequadas ao serviço.

**4. [facil · decidir]** Ao comparar, ao longo da vida do campo, a instalação de remoção de sulfato com programas de inibição, que base de decisão deve orientar a escolha?

Resposta: Um estudo de viabilidade técnico-econômica.

**5. [facil · comparar]** Nesse confronto econômico, quais grupos de custo e impacto devem ser comparados entre as opções?

Resposta: Investimento inicial e custos de operação e manutenção, frente aos custos recorrentes de inibição e às perdas por parada de produção.

**6. [facil · recordar]** Em uma completação com frac-pack, como o inibidor pode ser aplicado na alternativa citada?

Resposta: Por injeção conjunta com propante.

**7. [facil · recordar]** Quais duas alternativas citadas mudam a origem ou o reaproveitamento da água usada, em vez de aplicar inibidor?

Resposta: Re-injeção de água produzida e uso de água de aquífero.

**8. [facil · recordar]** Uma tecnologia pretende transportar e reter inibidor no reservatório para ocupar o papel da remoção de sulfato. O que precisa estar validado antes de tratá-la como substituta equivalente?

Resposta: Distribuição no reservatório, liberação do inibidor e compatibilidade.

## 02_02 · bloco 047 · Segregação e compatibilidade entre produtos químicos

Status: `ok`

Exemplos recebidos: PQ-05_01-07 (dificil), hotpotqa:5ac028cf5542992a796decb1 (dificil), PQ-04_02-03 (facil), PQ-08_02-04 (media), pira_ptbr:A1415 (facil), arc_challenge:Mercury_7267925 (media)

**1. [facil · recordar]** Qual é a finalidade técnica da segregação de produtos químicos em uma instalação offshore?

Resposta: Impedir contato não intencional entre produtos incompatíveis e evitar perda de desempenho por reação paralela.

**2. [facil · decidir]** Dois produtos serão aplicados no mesmo sistema de injeção, um após o outro, sem coincidência temporal. O que precisa ser verificado antes dessa operação?

Resposta: A compatibilidade entre os químicos, porque ela deve ser avaliada também no uso sequencial.

**3. [media · inferir]** Após a transferência de um produto, a mangueira é drenada de volta para o recipiente de outro produto. Que risco de processo essa prática introduz?

Resposta: Introduz contaminação cruzada por mistura residual, podendo causar reação indesejada e perda de desempenho.

**4. [media · diagnosticar]** Um equipamento recebeu alvejante clorado e, em seguida, sem descontaminação, seria tratado com limpador ácido. Qual perigo específico essa sequência pode gerar?

Resposta: Pode gerar uma nuvem gasosa tóxica.

**5. [dificil · diagnosticar]** Em um tratamento de água, cloro residual atinge indevidamente o ponto onde se adiciona bissulfito. A dosagem aparente aumenta e o desempenho do tratamento fica difícil de interpretar. Que mecanismo explica esse comportamento?

Resposta: O cloro residual consome o bissulfito antes da função principal, alterando a demanda química e mascarando falhas de tratamento.

**6. [facil · recordar]** Na armazenagem de químicos incompatíveis, qual arranjo físico é citado como parte da segregação prática?

Resposta: Tanques dedicados.

**7. [facil · recordar]** Na segregação prática, entre quais classes de produtos as interfaces devem ser controladas?

Resposta: Entre oxidantes, redutores, ácidos, bases e formulações orgânicas sensíveis.

## 02_02 · bloco 050 · Monitoramento do armazenamento e consequências operacionais

Status: `ok`

Exemplos recebidos: PQ-09_02-09 (dificil), PQ-07_05-02 (facil), PQ-03_01-05 (media), pira_ptbr:B2355 (facil), hotpotqa:5a74deda55429974ef308c83 (dificil), arc_challenge:Mercury_7228043 (media)

**1. [facil · inferir]** Em uma FPSO, um operador acompanha apenas o inventário dos tanques de químicos. Que aspecto técnico essencial ainda fica sem verificação?

Resposta: As condições que antecedem falhas de segurança, corrosão ou perda de desempenho.

**2. [facil · recordar]** Em água produzida acumulada com possibilidade de atividade microbiológica, quais duas facilidades se tornam relevantes no sistema?

Resposta: Facilidades para monitorar H2S e para aplicar biocidas.

**3. [facil · decidir]** Um sistema de injeção sujeito a corrosão opera em regime dinâmico e precisa acompanhar mudanças de corrosividade durante a operação. Que abordagem de monitoramento foi considerada adequada nesse contexto?

Resposta: Técnicas eletroquímicas, como par galvânico e resistência à polarização.

**4. [facil · recordar]** Mantido o nível do tanque sob controle, quais dois comportamentos do processo podem funcionar como sinais indiretos de problema químico?

Resposta: Perda de eficiência de separação e espuma inesperada.

**5. [media · inferir]** Numa FPSO com oscilações de vazão, pressão e composição, uma instabilidade aparece apenas a jusante. Que origem a montante deve permanecer na investigação?

Resposta: Problemas de estocagem ou manuseio de químicos.

**6. [facil · recordar]** Quais falhas de armazenamento e manuseio são citadas como interagindo com separação, tratamento de água, controle microbiológico e integridade de linhas e vasos?

Resposta: Falhas de segregação, superdosagem, subdosagem e degradação do produto.

**7. [facil · recordar]** Sem tratar de consumo de químico ou aparência do fluido, que evidência de dano metálico não uniforme é listada como sinal indireto?

Resposta: Corrosão localizada.

## 02_02 · bloco 053 · Seleção do ponto de medição, automação e confiabilidade dos dados

Status: `ok`

Exemplos recebidos: PQ-01_01-02 (facil), PQ-09_01-04 (media), hotpotqa:5ade98d35542997c77adee7e (dificil), PQ-04_02-09 (dificil), pira_ptbr:A1037 (facil), arc_challenge:Mercury_7014193 (media)

**1. [facil · recordar]** Em uma linha com ponto de injeção de químico e misturador, em que posição o sensor tende a representar melhor a condição que realmente chega ao equipamento?

Resposta: A jusante do misturador ou do ponto de injeção, após a mistura do químico.

**2. [media · diagnosticar]** Em uma linha com dosagem de químico, a leitura do indicador permanece aceitável, mas há bolsões com pouca renovação de fluido. Se o ponto de medição era pouco representativo, que condição ele estava mascarando?

Resposta: Zonas mortas.

**3. [facil · recordar]** Além dos controles automáticos ligados à dosagem de químicos e descargas, que dois fenômenos do sistema podem ser monitorados on-line?

Resposta: Corrosão e depósitos.

**4. [media · decidir]** Ao automatizar a dosagem de um químico em um FPSO, o que continua necessário para sustentar a confiança no dado, mesmo com menor variabilidade humana?

Resposta: Validação periódica, manutenção do sensor e reconciliação com análises laboratoriais.

**5. [media · diagnosticar]** Após cada mudança na vazão de injeção, a leitura do analisador só se altera vários minutos depois, sempre com a mesma defasagem, embora calibração e limpeza estejam em dia. Que aspecto da confiabilidade metrológica explica esse comportamento?

Resposta: Atraso entre injeção e medição.

**6. [media · diagnosticar]** Em um skid de dosagem, a leitura do sensor apresenta picos quando motores próximos entram em operação, sem mudança real de processo e com o elemento sensor limpo. Que causas metrológicas devem ser verificadas primeiro?

Resposta: Falhas de aterramento e ruído elétrico.

**7. [facil · recordar]** Quais condições típicas de FPSOs e sistemas submarinos podem agravar problemas de confiabilidade dos dados de sensores?

Resposta: Vibração, acesso limitado e segregação de fases.

**8. [media · decidir]** Na lógica de ajuste automático de dosagem para proteger um ativo crítico em escoamento com água livre intermitente, quais fatores além do valor lido devem ser considerados para que o ajuste seja confiável?

Resposta: Tempo de mistura, regime de escoamento, possibilidade de água livre e a consequência de falso positivo ou falso negativo.

## 02_02 · bloco 056 · Leitura temporal, pH e resposta corrosiva

Status: `ok`

Exemplos recebidos: hotpotqa:5a7b651455429931da12ca84 (dificil), PQ-01_01-02 (facil), PQ-03_02-08 (dificil), PQ-06_01-04 (media), pira_ptbr:A427 (facil), arc_challenge:Mercury_SC_406048 (media)

**1. [facil · recordar]** Em um sistema de processo de um FPSO com condições variáveis ao longo da operação, qual é a principal vantagem da leitura temporal no monitoramento de corrosão?

Resposta: Permitir correlacionar a corrosão com variáveis operacionais que mudam durante a operação.

**2. [facil · recordar]** Em um circuito aquoso de um FPSO, qual instrumento permite acompanhar a perda metálica ao longo do tempo e compará-la com registros de pH?

Resposta: Sonda de resistência elétrica.

**3. [facil · recordar]** Qual fenômeno medido por uma sonda RE permite inferir a perda metálica ao longo do tempo?

Resposta: A alteração da resistência elétrica do elemento sensor à medida que sua seção metálica efetiva diminui.  
_usa apoio_

**4. [media · inferir]** Em um meio aquoso de um FPSO suscetível à corrosão ácida, se o pH cair durante a operação, qual tendência é esperada na taxa de perda metálica?

Resposta: A taxa de perda metálica tende a aumentar.

**5. [media · inferir]** Em muitos meios aquosos, que mecanismo torna fisicamente plausível o aumento da corrosão quando ocorre acidificação?

Resposta: A acidificação pode alterar as reações eletroquímicas e a estabilidade de filmes superficiais, favorecendo maior taxa corrosiva.

**6. [media · diagnosticar]** Em um circuito aquoso de um FPSO, o pH sofre quedas rápidas e depois retorna ao patamar anterior, enquanto a sonda RE mostra aumento de perda de espessura sem repetir cada oscilação do pH no mesmo instante. Qual característica do dano metálico explica esse comportamento?

Resposta: O dano metálico é cumulativo.

**7. [media · decidir]** Uma correlação entre queda de pH e maior perda metálica observada em um sistema de um FPSO pode ser aplicada como regra universal a qualquer outro sistema aquoso?

Resposta: Não; a correlação observada em um sistema não deve ser tratada como regra universal.

**8. [facil · recordar]** Quais características do sistema condicionam a sensibilidade da resposta corrosiva às variações de pH?

Resposta: Metalurgia, presença de fase aquosa, composição do fluido, temperatura e regime de escoamento.
