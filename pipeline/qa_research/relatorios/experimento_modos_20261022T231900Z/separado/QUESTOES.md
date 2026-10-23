# Questões geradas

## 01_01 · bloco 000 · Indicadores de monitoramento operacional: detecção de desvios e diagnóstico

Status: `ok`

Exemplos recebidos: PQ-04_01-07 (dificil), PQ-02_10-05 (media), PQ-07_01-03 (facil)

**1. [facil · recordar]** Qual é a relação funcional entre um KPI operacional e a variável de processo associada?

Resposta: O KPI não substitui a variável de processo; ele resume o efeito dela sobre o desempenho.

**2. [media · inferir]** Em um FPSO que passou a operar com especificações mais restritas e maior exigência de segurança, por que ferramentas online de indicadores ganham maior valor operacional?

Resposta: Porque, nessas condições, permitem avaliar as condições operacionais em tempo próximo do real.

**3. [media · inferir]** Após uma mudança recente de carga, um KPI piorou logo em seguida, sem evidência adicional conclusiva de degradação estrutural. O que essa variação permite concluir?

Resposta: A variação pode ser efeito do transiente ou da mudança de carga; sozinha, não comprova perda estrutural de desempenho.

**4. [dificil · decidir]** Em um FPSO, após uma perturbação na alimentação do processo, um KPI saiu da faixa usual. Nas últimas horas, a estratégia de controle também foi alterada, e o histórico recente mostra operação instável desde então. Não há confirmação independente de falha de equipamento. Qual é a decisão diagnóstica correta?

Resposta: Tratar o KPI como sinal de desvio e investigar as variáveis perturbadas no contexto recente; não concluir causa raiz nem degradação de equipamento apenas pelo indicador.

## 01_01 · bloco 001 · O que são KPIs e como a finalidade muda sua definição

Status: `ok`

Exemplos recebidos: PQ-09_01-04 (media), PQ-04_02-03 (facil), PQ-03_02-08 (dificil)

**1. [facil · recordar]** Qual é a função essencial de um KPI em uma planta industrial?

Resposta: É uma métrica usada para avaliar a eficiência e o desempenho de processos industriais.

**2. [media · decidir]** Se o desempenho avaliado é o de uma única bomba da planta, em que nível o KPI deve ser aplicado?

Resposta: Ao equipamento, porque o foco é um ativo específico e não a instalação como um todo.

**3. [media · inferir]** Um KPI do processo já apontou uma deficiência de desempenho, e a equipe propõe uma ação simples para reduzir custo ou elevar capacidade sem grande investimento. O que esse resultado permite concluir?

Resposta: Que o KPI identifica a deficiência e apoia a ação proposta, mas não autoriza garantir redução de custo ou aumento de capacidade em qualquer condição operacional.

**4. [dificil · diagnosticar]** No FPSO, um indicador agregado do tratamento de gás foi definido para acompanhamento gerencial, não para atuação operacional imediata, mas aparece atualizado no painel do CCR. Durante uma instabilidade no mesmo sistema, a equipe quer usá-lo para decidir um ajuste imediato. Qual é o diagnóstico técnico desse uso?

Resposta: Há incoerência entre a métrica e a decisão: um KPI gerencial, mesmo exibido em tempo real, não se torna adequado para ajuste operacional imediato.

## 01_01 · bloco 002 · Denominador, base de exposição e comparabilidade

Status: `ok`

Exemplos recebidos: PQ-07_04-04 (media), PQ-09_02-09 (dificil), PQ-08_03-02 (facil)

**1. [facil · recordar]** Em um KPI, qual é o papel técnico do denominador?

Resposta: Ele define a base de referência do indicador e, portanto, o que está sendo realmente comparado.

**2. [media · comparar]** Em dois períodos de uma FPSO, avaliou-se o mesmo tipo de acidente, mas a taxa de um período foi calculada com uma base de denominador diferente da usada no outro. Essa comparação temporal é direta?

Resposta: Não é comparável diretamente. Para comparação temporal consistente, período, critério de enquadramento e base de horas-homem precisam ser compatíveis.

**3. [media · decidir]** Na FPSO, o consumo total de energia caiu em um mês, mas a carga processada e o volume produzido também caíram. O que isso permite concluir sobre o desempenho intrínseco do processo?

Resposta: Não prova melhora de eficiência. A queda absoluta pode refletir menor carga ou volume processado; o adequado é usar consumo de energia por unidade produzida.

**4. [dificil · diagnosticar]** Em dois semestres de mesma duração numa FPSO e com o mesmo critério de registro, os casos sem afastamento passaram de 4 para 5. No mesmo período, as horas-homem de exposição subiram de 200 mil para 320 mil. Qual é a interpretação técnica correta desse resultado?

Resposta: A piora não é confirmada; com 4 para 5 casos e 200 para 320 mil horas-homem, a taxa de frequência cai. O aumento bruto reflete maior exposição, não pior desempenho intrínseco.

## 01_01 · bloco 004 · Dependabilidade e seus atributos centrais

Status: `ok`

Exemplos recebidos: PQ-09_02-06 (media), PQ-03_02-08 (dificil), PQ-10_01-02 (facil)

**1. [facil · comparar]** Mantidas a mesma função requerida e as mesmas condições de operação, e com início operacional no caso aplicável, o que distingue disponibilidade de confiabilidade?

Resposta: Disponibilidade trata de estar operacional em um instante; confiabilidade, de continuar prestando o serviço correto ao longo de um intervalo, partindo operacional.

**2. [media · inferir]** No FPSO, uma proteção desarma e retira de serviço uma bomba para evitar dano maior ao conjunto. Qual é o efeito técnico dessa atuação sobre o sistema protegido?

Resposta: Preserva segurança e integridade, mas reduz a continuidade operacional do equipamento ou sistema protegido.

**3. [media · inferir]** Dois sistemas do FPSO cumprem a mesma função e falham com a mesma frequência. Um retorna mais rápido à operação aceitável após a falha. Qual tende a apresentar melhor desempenho global?

Resposta: A alternativa que retorna mais rápido e em condições aceitáveis tende a apresentar melhor desempenho global.

**4. [dificil · decidir]** Na mesma janela de observação, dois sistemas do FPSO cumprem a mesma função. O A falha menos, mas cada recuperação até condição aceitável é mais demorada; o B falha mais, porém retorna mais rápido, com os mesmos tempos logísticos e administrativos contabilizados na indisponibilidade. Qual pode ter maior disponibilidade operacional?

Resposta: O sistema que somar menor indisponibilidade total; se o retorno mais rápido compensar as falhas extras, o mais mantenável pode ter maior disponibilidade operacional.  
_usa apoio_

## 01_01 · bloco 005 · Disponibilidade: o que é e por que depende de falha e reparo

Status: `ok`

Exemplos recebidos: PQ-07_01-03 (facil), PQ-04_01-06 (media), PQ-05_01-07 (dificil)

**1. [facil · recordar]** Qual é a definição de disponibilidade de um dispositivo ou sistema?

Resposta: É a capacidade de o dispositivo ou sistema estar apto a cumprir a função requerida quando necessário.

**2. [facil · recordar]** Se uptime e downtime não estão disponíveis diretamente, que tipo de dado pode aproximar a disponibilidade?

Resposta: Podem ser usados valores médios de falha e reparo, como MTBF e MTTR, como aproximação.

**3. [media · comparar]** Duas bombas de injeção são avaliadas pelo mesmo indicador, com as mesmas indisponibilidades incluídas e o mesmo MTTR. Se a bomba A tem MTBF maior que a B, qual tende a ter maior disponibilidade?

Resposta: Mantidos o mesmo MTTR e o mesmo critério de indisponibilidades incluídas, o sistema com maior MTBF tende a ter maior disponibilidade.

**4. [dificil · decidir]** Em dois períodos de operação de um equipamento crítico no FPSO, a frequência de falhas e o tempo de reparo ativo por falha foram iguais, e a disponibilidade operacional foi medida pelo mesmo critério. No período pior, aumentaram tempos de diagnóstico, mobilização, espera por sobressalentes, acesso, liberação e retorno seguro à operação. Que ação deve ser priorizada para elevar a disponibilidade operacional?

Resposta: Priorizar a redução dos tempos logísticos e administrativos, porque eles compõem o downtime operacional e explicam a menor disponibilidade quando frequência de falha e reparo ativo são iguais.

## 01_01 · bloco 006 · Redundância, standby e efeitos sobre o comportamento do sistema

Status: `ok`

Exemplos recebidos: PQ-07_04-07 (dificil), PQ-06_01-04 (media), PQ-03_01-01 (facil)

**1. [facil · recordar]** Quando parte do arranjo falha, qual é a finalidade técnica da adoção de redundância?

Resposta: Uso de caminhos, equipamentos ou funções adicionais para manter o serviço quando parte do arranjo falha.

**2. [media · diagnosticar]** Em um arranjo com reserva fria, o ativo falha e o reserva precisa assumir. Sem gargalo comum externo, a produção cai porque o reserva falha em espera ou não entra por falha de partida/comutação. Que limitação isso mostra?

Resposta: A reserva fria reduz exposição a certos desgastes, mas não garante continuidade do serviço: continuam possíveis falhas em espera e na partida ou comutação.

**3. [media · inferir]** Comparando o mesmo arranjo redundante no início da missão e após um período bem mais longo, sem mudar a função requerida do sistema, como tende a evoluir o ganho de confiabilidade e disponibilidade trazido pelo reserva?

Resposta: O ganho tende a se limitar com o tempo; em missões longas, a degradação dos equipamentos ativos pode deixar de ser compensada pelo reserva.

**4. [dificil · decidir]** Em um FPSO, dois trens de compressão de gás são duplicados. O trem A desarma; o B estava disponível, parte com sucesso, mas ambos dependem da mesma água de resfriamento e do mesmo permissivo de intertravamento, indisponíveis após a ocorrência, e a função de compressão segue perdida. Nessa condição, a duplicação preserva a função de processo?

Resposta: Não. Há equipamento duplicado, mas não redundância útil da função de processo, porque a dependência comum de utilidade e intertravamento mantém a indisponibilidade.

## 01_01 · bloco 007 · Como selecionar, modelar e atualizar análises RAM

Status: `ok`

Exemplos recebidos: PQ-10_01-02 (facil), PQ-04_02-04 (media), PQ-05_02-07 (dificil)

**1. [facil · recordar]** Qual conteúdo mínimo o modelo RAM deve representar para avaliar perda de função em um sistema de processo?

Resposta: A lógica funcional do sistema, com dependências e modos de operação, por diagramas de blocos ou método equivalente.

**2. [media · decidir]** Na etapa preliminar de projeto de um FPSO, a análise RAM servirá apenas para checar arranjo, quantidade de equipamentos e opções de redundância. Que nível de complexidade do modelo é suficiente?

Resposta: Modelos mais simples podem servir nessa fase para validar arranjo, quantidade de equipamentos e alternativas de redundância.

**3. [media · inferir]** Uma análise RAM de um FPSO será adaptada para outra unidade com arquitetura, acessibilidade, estratégia de manutenção e contexto operacional diferentes. Os mesmos parâmetros de falha e reparo podem ser reaproveitados sem ajuste?

Resposta: Não. O modelo deve usar dados característicos da unidade, porque tempos de reparo e frequências de falha variam com arquitetura, acessibilidade, manutenção e contexto operacional.

**4. [dificil · decidir]** No desenvolvimento de uma análise RAM para um FPSO novo com módulo protótipo, a equipe criou um modelo muito detalhado, mas usou tempos e taxas genéricos, obtidos de outra realidade operacional, porque ainda não há histórico confiável da unidade. Para melhorar principalmente a confiabilidade da análise, qual deve ser a prioridade?

Resposta: Priorizar a aderência do modelo à unidade: revisar lógica e regime operacional e substituir parâmetros genéricos por dados representativos; sofisticação isolada não evita resultados imprecisos.

## 01_01 · bloco 008 · Coleta de dados, indicadores e monitoramento do desempenho real

Status: `ok`

Exemplos recebidos: PQ-06_03-01 (facil), PQ-03_02-08 (dificil), PQ-04_01-06 (media)

**1. [facil · recordar]** Quais dois marcos temporais devem ser registrados para calcular MTTR e disponibilidade observada?

Resposta: O tempo de início da falha e o tempo de retorno ao estado operacional.

**2. [media · inferir]** Uma unidade acumula registros há muitos anos, mas parte deles mudou de formato ao longo do tempo e parte está fora de gestão eletrônica. Em que condição esse histórico realmente aumenta a confiança analítica?

Resposta: O histórico longo só aumenta a confiança analítica se os registros permanecerem padronizados e eletronicamente gerenciados.

**3. [media · inferir]** Em um FPSO, falhas, mecanismos de falha e manutenção são registrados de forma agregada e não circulam entre áreas. Qual é o efeito disso na escolha das ações corretivas?

Resposta: A priorização de ações corretivas perde qualidade, porque as causas deixam de ser distinguíveis e úteis à decisão.

**4. [dificil · decidir]** No mesmo período e com a mesma base de cálculo, o item A teve mais falhas e piores médias. O item B falhou menos, mas sua indisponibilidade bloqueia produção, segurança de processo ou exportação no FPSO. Qual item deve ser priorizado no plano de ação?

Resposta: Deve ser priorizado o item cuja indisponibilidade bloqueia produção, segurança de processo ou exportação, mesmo com menor taxa de falha; a criticidade funcional prevalece sobre médias isoladas.

## 01_01 · bloco 010 · Interações com segurança, manutenção e recursos de suporte

Status: `ok`

Exemplos recebidos: PQ-03_02-08 (dificil), PQ-05_01-02 (facil), PQ-06_01-04 (media)

**1. [facil · recordar]** Qual é a finalidade operacional de intertravamentos e funções de proteção quando atuam?

Resposta: Evitar estados perigosos, danos ambientais e consequências maiores, mesmo que isso interrompa a produção.

**2. [facil · decidir]** Maior disponibilidade, por si só, autoriza reduzir intervenções preventivas?

Resposta: Não; isso só pode ser considerado após avaliação de risco e integridade.

**3. [media · inferir]** Num FPSO, reforçam-se as equipes de manutenção, mas o retorno operacional depende principalmente de espera por acesso, sobressalente, liberação ou logística. Qual tende a ser o efeito desse reforço?

Resposta: Tende a ser limitado, porque mais equipes não removem a espera dominante por acesso, sobressalente, liberação ou logística.

**4. [dificil · decidir]** Num FPSO, duas falhas surgem ao mesmo tempo em subsistemas diferentes. Há só uma equipe disponível. A falha A compromete uma função mais crítica para a unidade e seu reparo é mais curto que o da falha B. Qual falha deve ser atacada primeiro para acelerar o retorno operacional?

Resposta: A falha A, por combinar maior criticidade funcional com menor tempo de recuperação dentro da restrição compartilhada.

## 01_01 · bloco 011 · Como o processamento primário condiciona a capacidade da unidade

Status: `ok`

Exemplos recebidos: PQ-03_03-04 (media), PQ-07_05-02 (facil), PQ-04_01-07 (dificil)

**1. [facil · recordar]** De que depende a capacidade produtiva da unidade no processamento primário?

Resposta: Da capacidade combinada de separação, tratamento e movimentação dos fluxos de óleo, gás e água.

**2. [facil · recordar]** Que condição na entrada dos fluidos exige avaliar a capacidade do processamento primário de forma conjunta?

Resposta: Os fluidos chegam misturados e podem conter sólidos e outras impurezas.

**3. [media · inferir]** Se um separador, tratador, trocador, bomba, compressor ou sistema auxiliar opera abaixo da eficiência esperada, que consequência operacional pode ser necessária para manter especificações dos fluidos, estabilidade operacional ou descarte aceitável da água?

Resposta: A produção pode precisar ser reduzida para manter especificações dos fluidos, estabilidade operacional ou descarte aceitável da água.

**4. [dificil · diagnosticar]** Em um FPSO, o corte de água aumenta e a unidade já opera no limite para manejar essa fase. A capacidade de separar, tratar, reinjetar ou descartar essa corrente caiu, enquanto os principais equipamentos de óleo e gás não mostram limitação dominante. Para manter especificações, estabilidade operacional e descarte aceitável, a vazão do campo precisa cair. Qual é o sistema limitante?

Resposta: A malha de água produzida, porque falta capacidade para separar, tratar, reinjetar ou descartar a fase aquosa gerada com os hidrocarbonetos.

## 01_01 · bloco 012 · Seleção e aplicação de medidas para prevenir ou aliviar gargalos

Status: `ok`

Exemplos recebidos: PQ-07_01-03 (facil), PQ-05_01-07 (dificil), PQ-03_03-04 (media)

**1. [facil · recordar]** Ao escolher uma medida para prevenir ou aliviar uma restrição de produção, o que orienta essa decisão?

Resposta: Depende de onde está a limitação e de qual horizonte se deseja atacar.

**2. [media · decidir]** Num novo FPSO, análises do desenvolvimento indicam alto risco de incrustação, embora a capacidade ainda não tenha sido reduzida. Como a intervenção futura será difícil e o objetivo é cortar custos de produção perdida, que diretriz deve entrar na estratégia?

Resposta: Incorporar prevenção já no desenvolvimento, porque o risco de ocorrência e a dificuldade de gerenciamento justificam agir antes da perda para reduzir custos de produção perdida.

**3. [media · comparar]** Em um FPSO, certa rota de controle de incrustação foi adotada com um mecanismo dominante e uma origem de íons. Em outro campo, quer-se repetir a mesma rota, mas o mecanismo dominante, a origem dos íons, a arquitetura de injeção e produção, a acessibilidade para intervenção e a penalidade de parada são diferentes. A comparação direta é válida?

Resposta: Só é válido comparar ou replicar se mecanismo dominante, origem dos íons e condicionantes operacionais relevantes forem equivalentes; a técnica, sozinha, não determina a escolha.

**4. [dificil · decidir]** Após modificar um vaso de processo, a restrição anterior foi aliviada e ele saiu do limite. Mesmo assim, a capacidade total do FPSO continua travada no novo patamar: agora o compressor de gás opera no máximo contínuo, enquanto separadores, aquecedores e sistema de água produzida ainda têm folga. Onde deve ficar o foco do próximo debottlenecking?

Resposta: No compressor de gás, ou na variável que o limita agora; insistir no ponto já aliviado só desloca o gargalo sem aumentar a capacidade.

## 01_01 · bloco 013 · Consequências operacionais e econômicas das restrições em FPSO

Status: `ok`

Exemplos recebidos: PQ-10_01-01 (facil), PQ-09_02-09 (dificil), PQ-04_01-06 (media)

**1. [facil · recordar]** Quando a limitação está em um ponto comum do sistema de um FPSO, que decisão gerencial se torna inevitável?

Resposta: Priorizar entregas e alocar a capacidade disponível.

**2. [media · comparar]** Dois casos de interdição em um FPSO mantêm igual o volume produzido e diferem apenas pela duração da indisponibilidade. Qual deles gera maior perda econômica?

Resposta: A indisponibilidade de maior duração gera maior perda econômica.

**3. [media · comparar]** Em uma falha em riser ou ancoragem, duas FPSOs enfrentam o mesmo evento e a mesma necessidade de parar a produção para intervenção de integridade. Se apenas uma tem projeto que permite separação temporária e posterior restabelecimento das ligações, que diferença operacional adicional pode ocorrer nela?

Resposta: Além da interrupção da produção e da intervenção de integridade, pode ser necessária a desconexão e posterior reconexão.

**4. [dificil · decidir]** Em um FPSO, uma restrição em ponto comum levou a equipe a propor redistribuir vazões e reduzir carga para manter parte da produção. Ao mesmo tempo, o autodiagnóstico falhou, e as ações contingenciais e corretivas não serão implementadas em prazo compatível com o risco. Nessa situação, qual decisão deve prevalecer?

Resposta: Deve prevalecer a interdição da instalação, porque o caso passa a envolver segurança e conformidade, não só alocação de capacidade.

## 01_01 · bloco 015 · Atribuição de causas: do mecanismo físico à perda observada

Status: `ok`

Exemplos recebidos: PQ-04_02-09 (dificil), PQ-07_05-02 (facil), PQ-03_03-04 (media)

**1. [facil · comparar]** Na atribuição de perdas de produção, qual é a diferença entre mecanismo de falha e modo de falha?

Resposta: Mecanismo de falha é o fenômeno ou processo que degrada resistência, funcionalidade ou reserva operacional; modo de falha é a forma como a incapacidade de operar se manifesta.

**2. [facil · inferir]** Com incrustação na coluna de produção, que encadeamento físico explica a queda de vazão bruta?

Resposta: A incrustação obstrui a coluna, aumenta a resistência ao fluxo, pode alterar a pressão observada no poço e se associa à queda de vazão bruta.

**3. [media · decidir]** Um caso de perda de produção foi descrito apenas como queda de vazão ou perda de qualidade. O que precisa ser identificado para o diagnóstico ser robusto?

Resposta: É preciso identificar qual mecanismo passou a limitar a capacidade, em qual ativo, e sob quais condições ele se torna dominante; não basta registrar queda de vazão ou perda de qualidade.

**4. [dificil · decidir]** Em um poço ligado a um FPSO, há obstrução já formada na coluna de produção. O registro informa apenas que foi aplicado "inibidor", sem explicitar a função, e a capacidade não se recuperou. Qual conclusão analítica é correta?

Resposta: Não basta concluir que o tratamento falhou. É preciso explicitar a função do inibidor; se for de incrustação, ele só previne nova precipitação, e a recuperação pode exigir remoção do depósito e avaliação da integridade.

## 01_01 · bloco 016 · Condições que mudam o comportamento do risco no processamento primário

Status: `ok`

Exemplos recebidos: PQ-07_05-06 (media), PQ-04_01-07 (dificil), PQ-06_05-01 (facil)

**1. [facil · recordar]** Qual efeito comum faz medições essenciais ausentes ou pouco confiáveis, separação óleo-água ineficiente, controle manual muito exigente e análise de riscos que omite cenários plausíveis elevarem o risco?

Resposta: Reduzem a observabilidade do processo e a margem para detectar e corrigir desvios.

**2. [media · inferir]** Na revisão de uma FPSO, a análise de riscos omitiu cenários plausíveis no processamento primário e não há medida compensatória prevista. O que acontece com o risco de processo?

Resposta: O risco de processo aumenta, porque a análise passa a cobrir pior desvios plausíveis do processo.

**3. [media · comparar]** Duas unidades recebem a mesma perturbação, com as demais condições iguais. A unidade A tem mais instrumentação, maior capacidade de segregação, mais inventário intermediário e maior flexibilidade operacional que a B. Qual absorve mais a perturbação antes de reduzir carga ou parar?

Resposta: A unidade com mais desses recursos absorve mais a perturbação antes de reduzir carga ou parar.

**4. [dificil · decidir]** Em um estudo de resposta à mesma perturbação, a equipe favorece a Unidade X apenas pela designação da instalação. Porém, com as demais condições iguais, a Unidade Y tem mais instrumentação, maior capacidade de segregação, mais inventário intermediário e maior flexibilidade operacional. Qual critério deve prevalecer para decidir qual responderá melhor?

Resposta: Prevalece o arranjo real: a unidade com recursos reais superiores responderá melhor, mesmo se a designação da outra parecer mais favorável.

## 01_01 · bloco 017 · Estrutura organizacional, gestão de mudanças e autonomia técnica

Status: `ok`

Exemplos recebidos: PQ-07_04-07 (dificil), PQ-04_01-06 (media), PQ-08_03-02 (facil)

**1. [facil · recordar]** Além das técnicas de análise, de que mais depende a gestão de riscos ao longo da vida útil de um FPSO?

Resposta: De uma estrutura organizacional que sustente gestão de mudanças, atualização documental e esclarecimento rápido de parâmetros de projeto e operação.

**2. [media · inferir]** Em um FPSO, um desvio operacional exige decisão e validação de mudança. Se a equipe depende de suporte remoto e a documentação relevante está inacessível, qual tende a ser o efeito sobre a resposta e essa validação?

Resposta: Tende a aumentar o tempo de resposta, atrasar decisões e dificultar a validação das mudanças necessárias.

**3. [media · comparar]** Dois FPSOs têm o mesmo desvio operacional e os mesmos controles técnicos disponíveis. A única diferença é a autonomia técnica e a capacidade da equipe para manter bases de projeto e operação alinhadas à planta. Em qual arranjo os controles tendem a ser mais efetivos no planejamento operacional?

Resposta: No arranjo em que a equipe consegue interpretar o problema, autorizar ações, revisar premissas e manter a documentação coerente com a instalação real.

**4. [dificil · decidir]** Em um FPSO, as análises de risco existem e são usadas, mas as condições operacionais mudam ao longo do tempo. Nos desvios, parâmetros de projeto só são esclarecidos por suporte remoto; a documentação acessível não reflete bem a planta; e a responsabilidade técnica entre áreas é difusa. Qual fragilidade deve ser priorizada para recuperar robustez e resiliência?

Resposta: A fragilidade organizacional e de gestão de mudanças/documentação, com clarificação da responsabilidade técnica; ela reduz robustez e resiliência mesmo com técnicas de análise disponíveis.

## 01_01 · bloco 018 · Monitoramento, revisão e aprendizagem para próximas intervenções

Status: `ok`

Exemplos recebidos: PQ-04_02-03 (facil), PQ-02_10-05 (media), PQ-10_01-07 (dificil)

**1. [facil · recordar]** Que base informacional sustenta o monitoramento contínuo do risco e a revisão de decisões?

Resposta: Do registro do planejado, do realizado, dos desvios e das lições válidas para futuras intervenções.

**2. [media · inferir]** Numa parada de FPSO, o escopo executado superou o previsto e foi preciso mobilizar mais recursos de suporte que o planejado. Ao usar esse histórico no planejamento e no custo do ciclo de vida da próxima intervenção, o que ele indica?

Resposta: Que o plano subestimou a complexidade; o próximo planejamento e custo devem revisar premissas e recursos de suporte.

**3. [media · diagnosticar]** Na gestão de paradas de um FPSO, os relatórios finais são emitidos formalmente, mas desvios recorrentes reaparecem e as decisões futuras não mudam. Qual falha principal isso evidencia?

Resposta: Falta análise crítica real do relatório; preenchimento formal, sozinho, não transforma o registro em melhoria de decisão.

**4. [dificil · decidir]** Em uma parada anterior de FPSO, houve acréscimo de escopo e desvio na linha crítica, sem acidentes, e a execução exigiu mais recursos de suporte que o planejado. Para a próxima intervenção, a proposta é apenas aumentar o orçamento. Além do custo, que preparação também deve ser revista?

Resposta: Também deve revisar a preparação de contingências, porque os desvios indicam complexidade e suporte subestimados, não só custo maior.

## 01_01 · bloco 019 · Seleção de sistemas críticos e uso de histórico de falhas

Status: `ok`

Exemplos recebidos: PQ-07_04-04 (media), PQ-02_10-07 (dificil), PQ-09_01-02 (facil)

**1. [facil · recordar]** Na gestão de risco de um FPSO, qual é o papel da identificação de componentes e sistemas críticos?

Resposta: Definir quais funções merecem tratamento prioritário e orientar a implantação e a atualização dos controles de risco.

**2. [media · inferir]** Na seleção de criticidade de um FPSO, a função de medição apresenta desvios recorrentes já observados em falhas anteriores da unidade, com o mesmo mecanismo de processo. Como esse histórico deve entrar na análise atual?

Resposta: Como base para formular hipóteses de falha da função analisada na seleção de criticidade atual.

**3. [facil · recordar]** Que conteúdo do histórico de falhas o torna útil na seleção de sistemas críticos?

Resposta: A revelação de mecanismos de processo, tipos de desvio e causas técnicas ou organizacionais já ocorridos.

**4. [dificil · decidir]** Na revisão de criticidade de um FPSO, a equipe quer adotar, sem ajustes, a mesma sequência de sistemas apontada por estatísticas de falhas de outras unidades e de períodos anteriores. A unidade em análise opera com configuração de processo, regime operacional, manutenção, barreiras e contexto organizacional próprios. Qual decisão é correta?

Resposta: Não usar esse histórico como ranking final; ele apenas informa a análise, e a criticidade deve ser definida pelo exame das funções e vulnerabilidades da unidade.

## 01_01 · bloco 021 · Confiabilidade, disponibilidade e suporte de manutenção

Status: `ok`

Exemplos recebidos: PQ-03_01-01 (facil), PQ-07_04-07 (dificil), PQ-06_01-04 (media)

**1. [facil · recordar]** Qual é a definição de confiabilidade de um item?

Resposta: Capacidade de um item desempenhar a função requerida sob condições especificadas durante um intervalo de tempo.

**2. [facil · recordar]** Qual é a finalidade de usar formato padronizado para dados de confiabilidade e manutenção?

Resposta: Viabilizar a troca padronizada de informações de confiabilidade e manutenção entre as partes envolvidas.

**3. [media · decidir]** Em um FPSO, a probabilidade de falha de um equipamento permanece igual, mas o retorno da função ficou mais demorado e exige mais recursos. Ao escolher entre intervir, adiar manutenção ou aceitar operação degradada, como isso afeta o adiamento?

Resposta: A decisão fica menos favorável ao adiamento; é preciso pesar o maior tempo e a maior dificuldade para restaurar a função, não só a probabilidade de falha.

**4. [dificil · diagnosticar]** Em um FPSO, um item mantém a mesma probabilidade de falha, porém o retorno ao serviço ficou mais lento por restrições de logística, sobressalentes e mobilização de especialistas. Qual atributo do item é o mais afetado nesse caso?

Resposta: A disponibilidade, não a confiabilidade, porque a aptidão para operar quando requerida cai com suporte pior e restauração mais lenta.

## 01_01 · bloco 022 · Consequências econômicas de controles insuficientes

Status: `ok`

Exemplos recebidos: PQ-07_05-06 (media), PQ-04_01-07 (dificil), PQ-09_01-02 (facil)

**1. [facil · recordar]** Que consequência pode resultar de falhas em autodiagnóstico, ações contingenciais e medidas corretivas compatíveis com o risco?

Resposta: Podem levar à interdição da instalação e a perdas relevantes de receita.

**2. [media · comparar]** Duas FPSOs terão a mesma duração de parada forçada, com escopo corretivo e contexto contratual equivalentes. Se apenas a capacidade produtiva diferir, qual tende a ter maior perda potencial e por quê?

Resposta: A unidade de maior produção tende a ter maior perda potencial, porque a receita diária comprometida durante a parada forçada é maior.

**3. [facil · recordar]** O que impede que um exemplo econômico de uma instalação específica seja usado, sem ajuste, em qualquer outra FPSO?

Resposta: Eles não são universais, porque variam entre instalações a duração da parada, a capacidade produtiva, o escopo corretivo e o contexto contratual.

**4. [dificil · decidir]** Em uma FPSO de alta produção, foram identificadas falhas em autodiagnóstico e nas ações contingenciais previstas para um desvio crítico, com possibilidade de parada forçada ou interdição se o evento evoluir. Um gestor propõe adiar o controle de risco porque o gasto preventivo imediato supera o desembolso corretivo imediato, embora o cenário possa exigir mobilização extraordinária, replanejamento logístico e maior pressão sobre equipes e contratos. Que critério econômico deve orientar a decisão?

Resposta: A decisão não deve usar só o menor desembolso imediato; deve considerar o custo ao longo da vida útil, somando perda de receita, indisponibilidade, correções emergenciais e impactos indiretos.

## 01_01 · bloco 023 · Análise de causa: mecanismo de falha, modo de falha e FMEA

Status: `ok`

Exemplos recebidos: PQ-10_01-02 (facil), PQ-05_02-07 (dificil), PQ-03_01-05 (media)

**1. [facil · comparar]** Na análise de falhas, o que distingue o processo que leva à perda de função da forma como essa perda aparece?

Resposta: Mecanismo de falha é o processo físico, químico ou organizacional que leva à perda de função; modo de falha é a forma como essa perda se manifesta.

**2. [media · diagnosticar]** Em uma FMEA de um sistema do FPSO, operação, manutenção e automação descrevem de forma divergente a função do item analisado. Que condição indispensável ainda não foi atendida para aplicar a análise adequadamente?

Resposta: Falta entendimento comum das funções analisadas; sem isso, a aplicação da FMEA fica comprometida.

**3. [media · inferir]** Em uma FMEA que usa número de prioridade de risco, um modo de falha recebeu severidade 9, ocorrência 2 e detecção 5. Qual é o NPR?

Resposta: 90.

**4. [dificil · decidir]** Em uma FMEA de um FPSO, dois modos de falha tiveram NPR 60: um com severidade 10, ocorrência 2 e detecção 3, com consequência crítica, e outro com severidade 5, ocorrência 4 e detecção 3. A equipe quer tratá-los como equivalentes só porque o NPR é igual. Isso procede?

Resposta: Não. O NPR serve para triagem; o modo com consequência crítica exige análise individual, mesmo com o mesmo NPR.

## 02_02 · bloco 000 · Como selecionar e aplicar: bottle test como triagem empírica

Status: `ok`

Exemplos recebidos: PQ-05_01-02 (facil), PQ-07_04-07 (dificil), PQ-04_02-04 (media)

**1. [facil · recordar]** No bottle test, para que se usa a amostra sem aditivo?

Resposta: Ela mostra a separação natural da emulsão e serve de referência para comparar o efeito dos aditivos.

**2. [media · comparar]** Em bottle tests sob a mesma temperatura, mistura, concentração e tempo, uma amostra é água-em-óleo e outra é óleo-em-água. Em cada caso, que resultado indica bom desempenho do tratamento?

Resposta: Na emulsão água-em-óleo, a liberação da água dispersa do petróleo; na óleo-em-água, a clarificação da fase aquosa.

**3. [media · inferir]** Em um bottle test para comparar produtos ou dosagens, algumas garrafas ficaram com temperatura diferente e receberam mistura mais intensa que outras. O que isso implica para a conclusão do ensaio?

Resposta: A comparação perde validade; a diferença observada não pode ser atribuída com confiança só ao produto ou à dosagem.

**4. [dificil · diagnosticar]** Um desemulsificante foi escolhido por bottle test e aplicado no FPSO na mesma dosagem, mas a separação piorou após aumento do cisalhamento em válvulas e bombas, menor tempo de residência e mudança na composição do fluido. Qual diagnóstico explica essa divergência?

Resposta: O bottle test não bastou para representar a operação; o produto precisa de validação operacional, porque cisalhamento, tempo de residência e composição real podem alterar o desempenho.  
_usa apoio_

## 02_02 · bloco 003 · Por que pH, salmoura, petróleo e asfaltenos mudam o desempenho

Status: `ok`

Exemplos recebidos: PQ-06_01-04 (media), PQ-01_01-03 (facil), PQ-07_04-07 (dificil)

**1. [facil · recordar]** Qual efeito de asfaltenos e sólidos na estabilidade de uma emulsão?

Resposta: Podem formar filmes resistentes em torno das gotas e dificultar a coalescência.

**2. [facil · recordar]** Como um aditivo pode atuar na interface para favorecer a separação de uma emulsão estável?

Resposta: Pode modificar a organização dos filmes interfaciais e facilitar a drenagem entre gotas em contato.

**3. [media · inferir]** Com o mesmo clarificante, mesma dosagem e demais condições principais iguais, a separação mudou após variar a salinidade da água produzida. Que mecanismo explica essa mudança?

Resposta: A mudança de salinidade altera propriedades interfaciais — carga elétrica, solvatação e adsorção — e, assim, modifica a resposta ao aditivo.

**4. [dificil · decidir]** Em um FPSO, o desemulsificante foi escolhido quando cru e salmoura tinham outra composição. Após entrada de novos poços, o petróleo e a água produzida mudaram; a salinidade aumentou e o pH caiu. A equipe quer manter o produto apenas pelo histórico. Qual decisão técnica é correta?

Resposta: Reavaliá-lo, comparando produtos nas condições representativas do sistema atual; o efeito líquido depende da formulação e do fluido.

## 02_02 · bloco 006 · Como o antiespumante atua na quebra da espuma

Status: `ok`

Exemplos recebidos: PQ-09_01-04 (media), PQ-04_01-07 (dificil), PQ-06_03-01 (facil)

**1. [facil · recordar]** Que condição o antiespumante precisa cumprir para efetivamente quebrar a espuma?

Resposta: Ele deve alcançar o filme que estabiliza a bolha e favorecer sua ruptura ou drenagem.

**2. [facil · recordar]** De que dependem o espalhamento, a penetração e a dispersão do antiespumante?

Resposta: Dependem da formulação do produto e das propriedades da interface gás-líquido.

**3. [media · inferir]** Após baixo desempenho inicial no separador, a única ação foi aumentar a concentração do mesmo antiespumante; a formulação e a composição do fluido não mudaram. O que essa mudança permite inferir?

Resposta: Aumentar a concentração pode melhorar o contato até certa faixa, mas não garante desempenho crescente nem ausência de efeitos no restante do processo.

**4. [dificil · diagnosticar]** Em um separador de FPSO, o fluido passou a ter mais tensoativos e sais; pressão, temperatura, regime e internos permaneceram sem mudança relevante. Manteve-se o mesmo antiespumante, a dose foi aumentada e a espuma continuou. Qual diagnóstico explica melhor essa limitação?

Resposta: A mudança de tensoativos e sais provavelmente alterou a estabilidade da espuma e o contato do antiespumante com o filme; por isso, mais dose não garante ganho adicional.

## 02_02 · bloco 009 · Interações e efeitos colaterais relevantes no processamento

Status: `ok`

Exemplos recebidos: PQ-05_02-07 (dificil), PQ-01_01-03 (facil), PQ-07_05-06 (media)

**1. [facil · recordar]** Em um separador, que efeito a melhora da quebra de espuma tende a ter sobre o líquido na corrente de gás de saída?

Resposta: Tende a reduzir o arraste de líquido na saída de gás.

**2. [media · inferir]** Usando o mesmo produto, o controle de espuma passou a responder de forma inconsistente. Verificou-se mistura insuficiente na injeção e parte do químico não alcança a interface crítica. Qual é a causa mais provável?

Resposta: Aplicação inadequada: mistura insuficiente e/ou o produto não está alcançando a interface crítica.

**3. [media · decidir]** O antiespumante teve bom desempenho no início da campanha, mas depois houve aumento do corte de água, da produção de sólidos e mudança do regime operacional. Que ação passa a ser necessária no programa químico?

Resposta: Rever o programa químico; não assumir que o desempenho inicial permanecerá estável indefinidamente.

**4. [dificil · diagnosticar]** Após trocar o antiespumante por uma formulação com fase oleosa e emulsificantes, a espuma no separador de aplicação caiu como esperado e a injeção foi confirmada com mistura e alcance adequados. Na semana seguinte, sem mudança relevante de fluido ou de regime, o tratador a jusante passou a mostrar pior definição de interface. Qual diagnóstico técnico melhor explica o quadro?

Resposta: O mais consistente é efeito colateral da formulação sobre interfaces em outros equipamentos; a formulação deve ser reavaliada pela compatibilidade com o processamento como um todo.

## 02_02 · bloco 012 · Por que esses químicos funcionam na água produzida

Status: `ok`

Exemplos recebidos: PQ-05_02-07 (dificil), PQ-08_02-04 (media), PQ-09_01-02 (facil)

**1. [facil · recordar]** Que efeito a introdução de espécies catiônicas por um coagulante produz na interação entre gotas e sólidos?

Resposta: Favorece a aproximação entre gotas e sólidos, reduzindo a estabilidade da dispersão.

**2. [media · comparar]** Em duas correntes na mesma etapa de flotação por ar dissolvido, sob as mesmas condições, uma chega com agregados maiores e interfaces menos estáveis que a outra. Qual tende a ser removida com mais facilidade?

Resposta: A corrente com agregados maiores e interfaces menos estáveis, porque tende a ser capturada mais facilmente por microbolhas e subir mais rápido.

**3. [media · decidir]** Pretende-se substituir um coagulante sintético por um natural na água produzida porque ambos atuam por neutralização de carga e agregação. Qual critério confirma desempenho equivalente?

Resposta: A equivalência de desempenho precisa ser demonstrada na água produzida de interesse; mecanismo semelhante, sozinho, não basta.

**4. [dificil · decidir]** Na água produzida de um FPSO, a coagulação já reduziu a repulsão elétrica antes da flotação por ar dissolvido. Mesmo sem mudança relevante na geração de microbolhas, mistura ou vazão, a unidade ainda recebe agregados pequenos e frágeis, com baixa captura. Que produto deve ser acrescentado?

Resposta: Um floculante polimérico; ele faz pontes entre entidades já desestabilizadas, gerando flocos maiores e mais resistentes, mais facilmente capturados por microbolhas.

## 02_02 · bloco 015 · Consequências e interações relevantes para o descarte

Status: `ok`

Exemplos recebidos: PQ-09_01-02 (facil), PQ-03_02-08 (dificil), PQ-07_05-06 (media)

**1. [facil · recordar]** Além da remoção de óleo, que propriedade operacional do lodo gerado pode mudar com coagulantes e floculantes na água produzida?

Resposta: Podem alterar a facilidade de desaguamento do lodo.

**2. [facil · recordar]** Na flotação da água produzida, que efeito resíduos de químicos de produção podem causar na interação entre óleo disperso e gás?

Resposta: Podem mudar a aderência das gotas às bolhas, interferindo na flotação.

**3. [media · comparar]** O mesmo agente químico é aplicado com a mesma finalidade de promover separação água-óleo, mas em duas águas produzidas diferentes. É válido assumir o mesmo efeito nas duas?

Resposta: Não. Em outra água, o mesmo agente pode estabilizar a interface em vez de quebrar a emulsão.

**4. [dificil · diagnosticar]** Após entrada de poços de outra origem e ajuste no programa químico de produção, o TOG da água tratada sobe no FPSO. A dosagem do tratamento foi mantida, sem mudança relevante no regime de escoamento nem na configuração da flotação. Qual é a interpretação técnica mais provável e a ação correspondente?

Resposta: O mais provável é deslocamento da dosagem ótima por mudança de fluido/químicos; reavaliar o desempenho e o programa de tratamento.

## 02_02 · bloco 018 · Papel dos inibidores de incrustação e limites de aplicação em sistemas com URS

Status: `ok`

Exemplos recebidos: PQ-03_01-05 (media), PQ-04_02-03 (facil), PQ-05_01-07 (dificil)

**1. [facil · recordar]** Como os inibidores de incrustação atuam predominantemente sobre o crescimento cristalino?

Resposta: Atuam essencialmente de forma preventiva, por adsorção do inibidor e aumento da barreira energética ao crescimento cristalino.

**2. [media · inferir]** Num FPSO com URS operando, a dessulfatação está normal, mas persiste incrustação por CaCO3 na planta de processo. Qual deve ser a função do inibidor nessa situação?

Resposta: O inibidor deve ser usado para compensar incrustações que a remoção de sulfato não resolve, como CaCO3 na planta de processo.

**3. [media · inferir]** Num FPSO com URS em operação, o concentrado da unidade sai rico em sulfato e há risco de precipitação de CaSO4 em trechos internos. Qual deve ser a função do inibidor nesse caso?

Resposta: O inibidor deve proteger a corrente concentrada e pontos internos da URS em que a concentração favorece precipitação, especialmente de CaSO4.

**4. [dificil · diagnosticar]** Num FPSO com URS estável e sem perda evidente de proteção no lado de injeção, o inibidor é dosado apenas na água de injeção. Mesmo assim, continuam sinais de incrustação no poço produtor e na planta de produção. Que limitação essa estratégia revela?

Resposta: A estratégia falha por alcance: o inibidor pode adsorver na rocha ao redor do poço injetor e não chegar ao poço produtor; por isso, essa dosagem isolada não garante proteção ao processo de produção.

## 02_02 · bloco 021 · Sequestrante químico: bissulfito de sódio, mecanismo e limitações

Status: `ok`

Exemplos recebidos: PQ-07_01-03 (facil), PQ-05_01-07 (dificil), PQ-01_01-05 (media)

**1. [facil · recordar]** Qual é o mecanismo funcional do bissulfito de sódio no condicionamento da água?

Resposta: Reagir quimicamente com o oxigênio dissolvido, sequestrando-o no condicionamento da água.

**2. [media · inferir]** Se o teor de oxigênio dissolvido aumenta, a concentração ativa da solução permanece a mesma e a dosagem de bissulfito não é ajustada, qual consequência ocorre no sistema?

Resposta: A dosagem fica estequiometricamente insuficiente e tende a permanecer oxigênio residual no sistema.

**3. [dificil · diagnosticar]** Na água de injeção, o teor de oxigênio na entrada permanece estável. A bomba mantém a mesma vazão volumétrica de solução, não houve outra mudança relevante no processo, mas o lote atual ficou dias em recipiente parcialmente aberto e o residual de oxigênio começou a subir. Qual a causa mais provável?

Resposta: Perda de concentração ativa da solução por armazenamento inadequado com contato com ar; a mesma vazão volumétrica já não fornece bissulfito ativo suficiente.

**4. [media · decidir]** Mantida a mesma meta de oxigênio residual, com a mesma solução diluída e o mesmo arranjo metalúrgico sensível a baixo pH, qual critério deve orientar a decisão de elevar a dosagem de bissulfito?

Resposta: Não se deve assumir benefício automático. A solução diluída pode elevar a corrosividade por baixo pH; a dose deve considerar pH, compatibilidade metalúrgica e controle de residual.

## 02_02 · bloco 024 · Condições que mudam o comportamento: cloro residual, CO2 e disponibilidade de gás

Status: `ok`

Exemplos recebidos: PQ-04_01-07 (dificil), PQ-05_01-06 (media), PQ-10_01-02 (facil)

**1. [facil · decidir]** A mera disponibilidade de gás basta para viabilizar stripping a gás?

Resposta: Não. Além da disponibilidade, é preciso avaliar a composição do gás e o destino seguro da corrente gasosa.

**2. [facil · recordar]** Quando o gás de arraste está indisponível ou inadequado, qual rota pode ser usada para desoxigenação?

Resposta: A rota de desaeração a vácuo.

**3. [media · inferir]** Em água do mar submetida à desaeração a vácuo, com remoção de CO2 dissolvido em condições em que o equilíbrio CO2/carbonato/bicarbonato seja relevante, qual efeito teórico se espera sobre a tendência de precipitação mineral?

Resposta: Há aumento da tendência teórica de precipitação de carbonato de cálcio, por desequilíbrio do sistema CO2/carbonato/bicarbonato.

**4. [dificil · diagnosticar]** Em um sistema de água de injeção que usa bissulfito ou sulfito como sequestrante, o oxigênio residual na saída piora após aumento do cloro residual a montante. Não há evidência de maior carga de oxigênio dissolvido na água de entrada. Qual é a causa mais provável dessa piora?

Resposta: Parte do bissulfito ou sulfito está reagindo com o cloro residual; sobra menos sequestrante para consumir o oxigênio dissolvido.

## 02_02 · bloco 027 · Função do controle microbiológico na água de injeção

Status: `ok`

Exemplos recebidos: PQ-03_01-05 (media), PQ-09_02-09 (dificil), PQ-10_01-02 (facil)

**1. [facil · recordar]** Qual é o objetivo operacional do controle microbiológico na água de injeção?

Resposta: Limitar a contaminação, o crescimento e a atividade de microrganismos que favorecem biofilme, souring e corrosão microbiologicamente influenciada.

**2. [media · inferir]** Em um sistema de água de injeção com sulfato disponível, há preocupação com formação de sulfeto e corrosão em ferro e aço. Que grupo microbiano é mais relevante e por quê?

Resposta: As BRS são as mais relevantes, porque reduzem sulfato a sulfeto e estão associadas à biocorrosão em ferro e aço.

**3. [facil · comparar]** Na água de injeção, qual fase abriga as células planctônicas e onde ficam os microrganismos não dispersos?

Resposta: As planctônicas ficam dispersas na fase aquosa; os aderidos ficam fixos nas superfícies internas do sistema.

**4. [dificil · diagnosticar]** Mantendo o mesmo produto de tratamento na água de injeção, a contagem microbiana cai na fase aquosa. Mesmo assim, a contaminação persiste ou recorre em superfícies internas de trechos com baixo escoamento e com depósitos ou incrustação. Que mecanismo está limitando o programa?

Resposta: Biofilme aderido em nichos protegidos por baixo escoamento e depósitos ou incrustação, deixando a massa microbiana menos acessível ao biocida.

## 02_02 · bloco 029 · Por que biofilme, incrustação e depósitos reduzem a eficácia

Status: `ok`

Exemplos recebidos: PQ-01_01-02 (facil), PQ-07_04-07 (dificil), PQ-03_01-05 (media)

**1. [facil · recordar]** Que condição é indispensável para um biocida atuar sobre um microrganismo?

Resposta: Que o biocida entre em contato com o microrganismo.

**2. [media · decidir]** Em um circuito de água de injeção, há ataque corrosivo observado e o único indício microbiológico é a presença de bactérias. Sem avaliar depósitos, química da água e suscetibilidade do material, isso basta para atribuir a causa à atividade microbiana?

Resposta: Não. A presença de bactérias, isoladamente, não comprova a causa; a avaliação deve incluir depósitos, química da água e suscetibilidade do material.

**3. [media · inferir]** Se depósitos, biofilmes ou materiais aderidos criam regiões inacessíveis no sistema de injeção e o mesmo tratamento é mantido por longo período, o que pode ocorrer nesses pontos?

Resposta: Nesses locais, bactérias podem proliferar e adquirir resistência ao tratamento.

**4. [dificil · diagnosticar]** Num FPSO, a dosagem de biocida reduz as contagens no volume de água, mas inspeções ainda mostram camada aderida persistente recoberta por incrustação mineral e sulfeto de ferro. A dosagem aplicada é a usual para células livres. Qual é o limitante do tratamento?

Resposta: A persistência é compatível com biofilme recoberto por incrustação/sulfeto de ferro, que impede contato e penetração do biocida; a dose usada para células livres pode ser insuficiente.

## 02_02 · bloco 032 · Como a inibição funciona e quais limites mecanísticos importam

Status: `ok`

Exemplos recebidos: PQ-10_01-02 (facil), PQ-08_02-04 (media), PQ-05_02-07 (dificil)

**1. [facil · recordar]** Qual é a classificação do MEG quanto ao mecanismo de prevenção de hidratos?

Resposta: Inibidor termodinâmico.

**2. [media · comparar]** Mantendo a mesma pressão e a mesma composição do gás, duas correntes diferem apenas pela concentração de MEG na fase aquosa. Na de maior concentração adequada, como muda o limite inferior de temperatura de operação sem entrar na condição de formação de hidratos?

Resposta: Permite operar a temperaturas mais baixas antes de atingir a condição de equilíbrio do hidrato.

**3. [media · inferir]** A vazão nominal de injeção de MEG foi mantida, mas aumentou a água produzida, sem evidência de ajuste compensatório na concentração efetiva na água livre. Qual é a consequência para a proteção contra hidratos?

Resposta: A concentração efetiva do MEG na água livre cai e a proteção diminui; podem surgir regiões sem proteção mesmo com a mesma vazão nominal.

**4. [dificil · decidir]** Após uma parada curta, a linha retorna ainda quente. A vazão nominal de MEG segue o procedimento, mas houve aumento de água produzida e há indícios de mistura insuficiente ou falha de distribuição. Antes de concluir que a linha está segura contra hidratos, qual checagem deve ter prioridade?

Resposta: Verificar primeiro a concentração efetiva de MEG na água livre e sua distribuição local; o histórico térmico favorável não garante proteção e pode haver subinibição regional.

## 02_02 · bloco 035 · Seleção, monitoramento e alternativas de regeneração

Status: `ok`

Exemplos recebidos: PQ-01_01-02 (facil), PQ-04_02-09 (dificil), PQ-07_05-06 (media)

**1. [facil · recordar]** Qual é a função imediata da regeneração no circuito de MEG?

Resposta: Remover água para permitir o reúso do glicol.

**2. [media · inferir]** Se a concentração de MEG na fase aquosa cair, com a mesma composição do fluido, as mesmas condições de pressão e temperatura, e a mesma condição de água livre e tempo de residência, o que ocorre com a proteção contra hidratos?

Resposta: A proteção contra hidratos diminui; a tendência de formação de hidratos aumenta.  
_usa apoio_

**3. [media · inferir]** Em uma recuperação de MEG com teor de sais elevado no circuito, a remoção de água é intensificada para concentrar o glicol. Que risco adicional surge e qual a implicação para o tratamento de sais?

Resposta: Pode ocorrer supersaturação e precipitação de sais; por isso, a remoção de sais deve ser avaliada separadamente da regeneração.  
_usa apoio_

**4. [dificil · decidir]** Em bancada, uma alternativa de regeneração teve bom desempenho com uma mistura simplificada. No FPSO, o circuito real contém sais, sólidos e hidrocarbonetos, e opera com temperatura, pressão e carga diferentes ou variáveis. Qual critério deve orientar a seleção dessa alternativa?

Resposta: Não extrapolar diretamente o resultado do ensaio; a seleção deve considerar o circuito real e condições representativas, porque contaminantes e T/P/carga alteram a separação e o consumo de energia.

## 02_02 · bloco 038 · Função dos químicos no tratamento do gás

Status: `ok`

Exemplos recebidos: PQ-07_04-07 (dificil), PQ-03_03-04 (media), PQ-04_02-03 (facil)

**1. [facil · recordar]** Qual é a função do sequestrante de H2S no tratamento do gás offshore?

Resposta: Consumir ou imobilizar a espécie sulfídrica, o H2S.

**2. [media · comparar]** No tratamento do gás offshore, que função o MEG exerce e que função as alcanolaminas exercem, considerando apenas a ação química?

Resposta: O MEG atua contra hidratos; as alcanolaminas removem CO2 e podem também participar do adoçamento do gás.

**3. [media · inferir]** Em um trecho do tratamento de gás offshore, há gases ácidos e risco de hidrato no sistema, mas ali a ameaça dominante é a corrosão por fase aquosa. Qual serviço químico deve ser priorizado?

Resposta: Priorizar o inibidor de corrosão naquele trecho.

**4. [dificil · decidir]** No tratamento de gás de um FPSO, um subsistema apresenta tendência a espuma e outro, mais frio, apresenta risco de hidrato. Para simplificar a operação, propõem usar um único produto, na mesma concentração e no mesmo ponto de injeção, para ambos. Essa simplificação é tecnicamente adequada?

Resposta: Não. Devem ser tratados como serviços separados, com produto, corrente, concentração e ponto de injeção definidos pelo risco dominante de cada trecho.

## 02_02 · bloco 041 · Compatibilidade química: por que a combinação pode melhorar ou piorar a proteção

Status: `ok`

Exemplos recebidos: PQ-10_01-07 (dificil), PQ-07_01-03 (facil), PQ-09_02-06 (media)

**1. [facil · recordar]** Ao comparar dois químicos de processo, o que é inválido concluir apenas pela função declarada de cada um?

Resposta: Não se pode presumir a compatibilidade pela função de cada químico.

**2. [facil · recordar]** Além de alteração de pH, precipitação e mudança da estabilidade do filme, que mecanismo de interação pode afetar a proteção anticorrosiva quando químicos são combinados?

Resposta: Competição de adsorção.

**3. [media · comparar]** Duas combinações usam os mesmos tipos nominais de químicos e são julgadas pelo mesmo critério de proteção anticorrosiva. Se a formulação e/ou o meio mudam entre os casos, o resultado de uma pode ser transferido para a outra?

Resposta: Não. A combinação pode melhorar, preservar ou reduzir a proteção anticorrosiva conforme a formulação e o meio.

**4. [dificil · decidir]** Em uma avaliação de químicos para um sistema de gás de FPSO, a mesma combinação preserva a proteção anticorrosiva em bancada com solução só de NaCl, mas a reduz em ensaio com as concentrações, os materiais e o fluido do serviço. Qual resultado deve orientar a decisão de compatibilidade?

Resposta: Deve prevalecer o ensaio com concentrações, materiais e fluido do serviço; teste só com NaCl não basta, porque a compatibilidade depende do meio e esse fluido não reproduz a água real.

## 02_02 · bloco 044 · Alternativas ao squeeze para controle de incrustação

Status: `ok`

Exemplos recebidos: PQ-08_02-04 (media), PQ-04_02-09 (dificil), PQ-05_01-02 (facil)

**1. [facil · recordar]** Qual efeito a redução de sulfato da água de injeção, por URS, tem sobre a formação de BaSO4 e SrSO4?

Resposta: Diminui ou pode eliminar a condição necessária para a precipitação de BaSO4 e SrSO4.

**2. [facil · recordar]** Que meio físico a URS emprega para remover sulfato seletivamente?

Resposta: Membranas adequadas ao serviço.

**3. [media · comparar]** Para a mesma vida de campo, compare duas alternativas de controle de incrustação: instalar URS, com CAPEX e O&M conhecidos, ou manter programa de inibição, com custos recorrentes e perdas por paradas também conhecidos. Qual critério deve orientar a escolha?

Resposta: Um estudo de viabilidade técnico-econômica, comparando CAPEX e O&M da URS com os custos recorrentes de inibição e as perdas por parada de produção.

**4. [dificil · decidir]** Em um FPSO, o risco de incrustação decorre da presença de sulfato na água de injeção. Propõe-se retirar a URS do conceito e adotar tecnologia de transporte e retenção de inibidor no reservatório, mas ainda não há demonstração de distribuição, liberação nem compatibilidade. Essa tecnologia pode ser tratada como substituta equivalente?

Resposta: Não. Sem validação de distribuição, liberação e compatibilidade, ela não deve ser tratada como substituta equivalente da remoção de sulfato.

## 02_02 · bloco 047 · Segregação e compatibilidade entre produtos químicos

Status: `ok`

Exemplos recebidos: PQ-04_02-03 (facil), PQ-05_01-07 (dificil), PQ-08_02-04 (media)

**1. [facil · recordar]** Qual é a finalidade técnica da segregação de produtos químicos no armazenamento e manuseio offshore?

Resposta: Impedir contato não intencional entre produtos incompatíveis e evitar perda de desempenho por reação paralela.

**2. [media · decidir]** Dois químicos serão usados juntos ou em sequência no mesmo sistema de injeção, com possibilidade de residual em linhas, mangueiras, drenagem, retorno ou recipientes. Ainda não houve avaliação prévia entre eles. Que condição deve ser atendida para liberar o mesmo arranjo?

Resposta: A compatibilidade entre os químicos deve ser avaliada e comprovada antes; sem isso, não se deve usar o mesmo arranjo de forma conjunta ou sequencial.

**3. [facil · recordar]** Que perigo pode surgir da mistura sucessiva de limpador ácido com alvejante clorado?

Resposta: Pode gerar nuvem gasosa tóxica.

**4. [dificil · diagnosticar]** Em um tratamento de água no FPSO, cloro e bissulfito atuam em etapas distintas. Sem mudança relevante de carga/processo e sem falha evidente de bomba ou instrumentação, a demanda de bissulfito sobe de forma anormal e o desempenho fica irregular; há compartilhamento de linha, retorno de mangueira ou recipiente com possibilidade de residual. Qual causa esse padrão indica?

Resposta: Contaminação cruzada por segregação inadequada ou residual em retorno; o cloro residual consome o bissulfito antes da função principal.

## 02_02 · bloco 050 · Monitoramento do armazenamento e consequências operacionais

Status: `ok`

Exemplos recebidos: PQ-03_01-05 (media), PQ-07_05-02 (facil), PQ-09_02-09 (dificil)

**1. [facil · recordar]** Além da medição de nível, que aspecto o monitoramento do armazenamento e manuseio de químicos deve verificar?

Resposta: Verificar condições que antecedem falhas de segurança, corrosão ou perda de desempenho, e não só o nível do tanque.

**2. [media · inferir]** Em um tanque fechado com água produzida acumulada e tempo de residência elevado, condição que pode sustentar atividade microbiológica, que facilidades passam a ser relevantes?

Resposta: Em água produzida acumulada com possibilidade de atividade microbiológica, tornam-se relevantes facilidades para monitorar H2S e aplicar biocidas.  
_usa apoio_

**3. [facil · recordar]** Quais técnicas eletroquímicas são adequadas para acompanhar variações de corrosividade em sistemas de injeção sob regime dinâmico?

Resposta: Par galvânico e resistência à polarização.

**4. [dificil · decidir]** Em um FPSO com oscilações normais de vazão, pressão e composição, aparece instabilidade a jusante junto com consumo anormal de químico, desvio entre dosagem planejada e resposta do processo, espuma inesperada, perda de eficiência de separação e corrosão localizada, sem evidência dominante de falha mecânica isolada a jusante. Que investigação priorizar?

Resposta: Priorizar a investigação do armazenamento/manuseio do químico; os sinais são compatíveis com segregação, superdosagem, subdosagem ou degradação causando a instabilidade a jusante.

## 02_02 · bloco 053 · Seleção do ponto de medição, automação e confiabilidade dos dados

Status: `ok`

Exemplos recebidos: PQ-09_01-04 (media), PQ-04_02-09 (dificil), PQ-01_01-02 (facil)

**1. [facil · recordar]** Qual posição do sensor tende a representar melhor a condição química realmente imposta ao equipamento?

Resposta: A jusante do misturador ou do ponto de injeção, após a mistura do químico.

**2. [media · diagnosticar]** Na mesma corrente, comparando medição on-line e laboratório com base analítica compatível, o desvio cresce gradualmente sem mudança relevante de processo, em serviço severo para a superfície molhada do instrumento. Qual causa do afastamento é mais consistente?

Resposta: Deriva por incrustação ou sujidade do sensor.

**3. [media · inferir]** A dosagem foi aumentada há pouco, e há atraso perceptível entre o ponto de injeção e o de medição. A leitura on-line ainda está baixa. Como interpretar esse valor?

Resposta: Pode ser apenas defasagem de resposta e tempo de mistura; não se deve aumentar de novo a dosagem antes de o ajuste chegar à medição.

**4. [dificil · decidir]** Em um FPSO, a dosagem automática de um químico de proteção depende de um único sensor on-line. O ativo protegido é crítico, as leituras altas são intermitentes e o laboratório da mesma corrente não as confirma. Com vibração e acesso limitado ao instrumento, qual decisão de ajuste deve ser tomada?

Resposta: Não reduzir a dosagem só por esse sinal; primeiro validar e manter o sensor e reconciliar com o laboratório, pois o risco de ajuste errado no ativo crítico é alto.

## 02_02 · bloco 056 · Leitura temporal, pH e resposta corrosiva

Status: `ok`

Exemplos recebidos: PQ-03_02-08 (dificil), PQ-01_01-02 (facil), PQ-06_01-04 (media)

**1. [facil · recordar]** Em monitoramento de corrosão com registros de pH, qual é a função da sonda de resistência elétrica?

Resposta: Permitir acompanhar a perda metálica ao longo do tempo e compará-la com os registros de pH.

**2. [media · inferir]** Em uma linha com fase aquosa suscetível à corrosão ácida, o pH caiu durante a operação. Qual efeito isso tende a ter sobre a taxa de perda metálica?

Resposta: A taxa de perda metálica tende a aumentar.

**3. [media · inferir]** No mesmo sistema, o pH oscilou e depois se recuperou, enquanto a perda de espessura vem sendo medida continuamente. A curva de perda de espessura deve reproduzir o pH instante a instante?

Resposta: Não. Ela refletirá o dano acumulado ao longo do tempo, não o pH instantâneo.

**4. [dificil · decidir]** No Sistema 1 do FPSO, a sonda RE mostrou maior perda metálica nos períodos de queda de pH, e um ajuste químico reduziu a progressão do dano. No Sistema 2, querem repetir o mesmo ajuste só porque o pH oscila de forma parecida, embora ali a fase aquosa e a temperatura sejam diferentes. Essa replicação é tecnicamente válida?

Resposta: Não. O ajuste não deve ser copiado automaticamente; no Sistema 2 é preciso confirmar qual variável governa o dano, porque a sensibilidade à resposta depende das condições locais, como fase aquosa e temperatura.
