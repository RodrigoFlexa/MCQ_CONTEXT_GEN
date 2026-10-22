# Revisão dos documentos a partir dos pareceres do especialista

Versão derivada de `dez_areas_final_v1`, que permanece intacta. As edições corrigem, nos documentos de contexto, a origem dos problemas apontados pelo especialista nas questões aprovadas com ressalvas e reprovadas do primeiro lote (formulários respondidos em 21/10/2026), para que não se repitam em novas gerações. Os demais documentos são cópias byte a byte da v1.

Totais: 14 documentos editados; 30 trechos alterados; 27 blocos ajustados.

Registro estruturado (antes/depois): [revisao_especialista.json](revisao_especialista.json). Pareceres consolidados: `pipeline/qa_research/revisao_especialista/pareceres.json`.

## 01_01 — [1.1. Gestão do Desempenho Empresarial (KPI)](01_01/documento.md)

**Atribuição de causas: do mecanismo físico à perda observada** · Q003 (aprovada com ressalvas)

Motivo: O enunciado usou 'inibidor' sem a função (incrustação, corrosão etc.), o que o deixou impreciso. O documento passa a nomear o inibidor de incrustação e a explicitar que a função do inibidor precisa ser dita.

- Antes: A inibição química busca prevenir ou retardar nova precipitação; não deve ser confundida com a remoção de uma obstrução já formada.
- Depois: A inibição química de incrustação, feita com inibidor de incrustação, busca prevenir ou retardar nova precipitação; não deve ser confundida com a remoção de uma obstrução já formada. Como há inibidores com funções distintas, como os de incrustação, de corrosão, de hidratos e de parafinas, a função do inibidor precisa ser explicitada ao analisar um caso, porque o efeito esperado de cada um é diferente.

**Disponibilidade: o que é e por que depende de falha e reparo** · Q004 (aprovada com ressalvas)

Motivo: Enunciado pouco claro ou ambíguo. O documento passa a separar explicitamente o tempo de reparo ativo dos tempos logísticos e administrativos que compõem o downtime.

- Antes: Na disponibilidade operacional, a indisponibilidade pode incluir diagnóstico, mobilização de pessoal, espera por sobressalentes, acesso, liberação, reparo e retorno seguro. Esses tempos precisam ser discriminados: o tempo de reparo ativo não deve ser confundido com toda a indisponibilidade logística e administrativa. Por isso, dois equipamentos com a mesma frequência de falha podem apresentar disponibilidades muito diferentes se suas condições de reparo forem distintas.
- Depois: Na disponibilidade operacional, o tempo total de indisponibilidade (downtime) de cada falha soma o tempo de reparo ativo, isto é, a intervenção propriamente dita, a tempos logísticos e administrativos, como diagnóstico, mobilização de pessoal, espera por sobressalentes, acesso, liberação do equipamento e retorno seguro à operação. Esses tempos precisam ser discriminados: o tempo de reparo ativo não deve ser confundido com toda a indisponibilidade. Por isso, dois equipamentos com a mesma frequência de falha e o mesmo tempo de reparo ativo podem apresentar disponibilidades operacionais muito diferentes se seus tempos logísticos e administrativos forem distintos.

## 02_02 — [2.2. Produtos químicos — Produção e Processo](02_02/documento.md)

**Seleção e aplicação de coagulantes e floculantes** · Q007 (aprovada com ressalvas)

Motivo: A resposta não mencionava o impacto no TOG da água produzida, a variável mais importante para avaliar o tratamento. O documento passa a ligar a janela de dosagem ao TOG.

- Antes: subdosagem deixa a emulsão estável; superdosagem pode reestabilizar dispersões, aumentar residual orgânico ou produzir flocos frágeis e pouco capturáveis.
- Depois: subdosagem deixa a emulsão estável; superdosagem pode reestabilizar dispersões, aumentar residual orgânico ou produzir flocos frágeis e pouco capturáveis. Em ambos os casos, o efeito aparece sobretudo no teor de óleos e graxas (TOG) da água produzida tratada, principal variável de avaliação do desempenho do sistema de tratamento e do enquadramento do descarte.

**O que é a URS/SRU e qual problema ela busca evitar** · Q009 (aprovada com ressalvas)

Motivo: A resposta não mencionava que a redução de sulfato também contribui para evitar o souring do reservatório. O documento passa a incluir essa função no bloco que define a URS/SRU.

- Antes: A remoção de sulfato atua, portanto, sobre a causa química da incrustação por sulfatos, reduzindo a carga do ânion que participaria da precipitação.
- Depois: A remoção de sulfato atua, portanto, sobre a causa química da incrustação por sulfatos, reduzindo a carga do ânion que participaria da precipitação. Além disso, a menor disponibilidade de sulfato contribui para mitigar o souring, isto é, o aumento biogênico da produção de sulfeto de hidrogênio (H2S) no reservatório, porque o sulfato é o insumo que as bactérias redutoras de sulfato (BRS) convertem em H2S; essa contribuição reduz a propensão ao souring, mas não elimina de imediato o sulfato já introduzido na formação.

## 03_03 — [3.3. Operação de tanques de carga, lastro, sistema gás inerte, ventilação e estabilidade](03_03/documento.md)

**Por que ocorrem sobrepressão e vácuo** · Q014 (aprovada com ressalvas)

Motivo: Os tanques de carga possuem vent automático e alarme de pressão; para chegar à deformação seria preciso o blank no sistema de alívio e falha do alarme ou da resposta da equipe. O documento passa a exigir essa combinação.

- Antes: Em tanques inertizados, um erro de reinstalação após isolamento também pode causar sobrepressurização: a manutenção indevida de blank pode impedir a rota normal de vent e permitir que o gás inerte eleve a pressão do tanque. A consequência pode ultrapassar o âmbito operacional e atingir a estrutura, com deformação de chapas, anteparas e outras regiões sensíveis à diferença de pressão.
- Depois: Em tanques inertizados, um erro de reinstalação após isolamento também pode contribuir para sobrepressurização: a manutenção indevida de blank pode impedir a rota normal de vent e alívio e permitir que o gás inerte eleve a pressão do tanque. Como os tanques de carga dispõem de vent automático e de monitoramento com alarme de pressão, o bloqueio da rota de vent, sozinho, não leva necessariamente a dano: para que a pressão chegue a deformar a estrutura, é preciso que, além do blank no sistema de alívio, haja falha do alarme de pressão ou da resposta da equipe a ele. Nessa combinação, a consequência pode ultrapassar o âmbito operacional e atingir a estrutura, com deformação de chapas, anteparas e outras regiões sensíveis à diferença de pressão.

**Consequências para integridade, segurança e emissões** · Q014 (aprovada com ressalvas)

Motivo: Coerência com a edição anterior: deformação por isolamento incorreto pressupõe também falha do alarme ou da resposta.

- Antes: pressão excessiva por isolamento incorreto ou reinstalação inadequada pode deformar a estrutura.
- Depois: pressão excessiva por isolamento incorreto ou reinstalação inadequada, sem atuação do alarme de pressão ou sem resposta da equipe a ele, pode deformar a estrutura.

## 04_01 — [4.1. Sistema e operação de pull in de risers](04_01/documento.md)

**Como a transição de rigidez reduz sobrecurvatura e tensões locais** · Q023 (aprovada com ressalvas)

Motivo: O especialista não reconhece a flex-joint como acessório de risers conectados a FPSO, e sim de unidades de perfuração; pediu para eliminá-la do enunciado e da resposta. O documento deixa de apresentá-la como solução de topo de FPSO.

- Antes: O bend stiffener, o stress-joint e a mísula da flex-joint atuam sobre esse problema criando uma variação gradual de rigidez.
- Depois: O bend stiffener, em risers flexíveis, e o stress-joint, em risers rígidos, atuam sobre esse problema criando uma variação gradual de rigidez.

**Como a transição de rigidez reduz sobrecurvatura e tensões locais** · Q023 (aprovada com ressalvas)

Motivo: Idem: flex-joint não é acessório usual de risers conectados a FPSO.

- Antes: Na flex-joint, o elemento flexível acomoda parte dessa rotação enquanto a concha esférica e os componentes estruturais transferem a carga do riser para a plataforma.
- Depois: Em risers flexíveis conectados a FPSO, essa função cabe ao bend stiffener junto à terminação; a flex-joint, que acomoda rotação por meio de um elemento flexível, não é acessório usual de risers conectados a FPSO, sendo mais associada a unidades de perfuração.

**Fatores que alteram a resposta geométrica e de carga** · Q023 (aprovada com ressalvas)

Motivo: Idem: retirada da flex-joint como recurso de hang-off em FPSO.

- Antes: no trecho superior e flex-joint no hang-off.
- Depois: no trecho superior e elementos de acomodação de rotação e de transição de rigidez no hang-off.

**Aplicação das soluções de topo no pull-in e na conexão** · Q023 (aprovada com ressalvas)

Motivo: Idem: flex-joint separada da solução de topo para FPSO.

- Antes: Para linha rígida, o stress-joint fornece transição progressiva de rigidez, enquanto a flex-joint acrescenta liberdade rotacional controlada na ligação com a unidade.
- Depois: Para linha rígida, o stress-joint fornece transição progressiva de rigidez. A flex-joint, que acrescenta liberdade rotacional controlada na ligação com a unidade, não é acessório usual de risers conectados a FPSO, sendo mais associada a unidades de perfuração.

**O que é pull-in e como ele se distingue da transferência do topo do riser** · Q023 (aprovada com ressalvas)

Motivo: Idem.

- Antes: Em sistemas com riser flexível, flex-joint ou outros acessórios, a função continua
- Depois: Em sistemas com riser flexível e bend stiffener ou com outros acessórios, a função continua

**O que é o pull-in e quais elementos concentram a integridade da conexão** · Q023 (aprovada com ressalvas)

Motivo: Idem: o arranjo de SCR com flex-joint não deve servir de referência para FPSO.

- Antes: Esse encadeamento descreve a sequência típica de SCR com flex-joint; não constitui procedimento completo nem critério universal para outros arranjos de conexão.
- Depois: Esse encadeamento descreve a sequência típica de SCR com flex-joint; não constitui procedimento completo nem critério universal para outros arranjos de conexão. Em FPSOs, a flex-joint não é acessório usual dos risers conectados à unidade, sendo mais associada a unidades de perfuração; por isso, esse arranjo não deve ser tomado como referência para a conexão de risers em FPSO.

## 05_01 — [5.1. Sistema de utilidades](05_01/documento.md)

**Vaso de expansão, headers e estabilidade hidráulico-térmica** · Q030 (aprovada com ressalvas)

Motivo: Parte da resposta ('em aquecimento pressurizado, ajuda a mantê-lo cheio') não vale em todos os arranjos. O documento adota a formulação sugerida pelo especialista.

- Antes: Em sistemas fechados, o vaso de expansão absorve variações volumétricas da água associadas à mudança de temperatura e ajuda a estabilizar a pressão do circuito.
- Depois: Em sistemas fechados, o vaso de expansão acomoda as variações volumétricas do fluido decorrentes das mudanças de temperatura, limitando as oscilações de pressão e contribuindo para manter o circuito adequadamente preenchido e pressurizado.

**Vaso de expansão, headers e estabilidade hidráulico-térmica** · Q030 (aprovada com ressalvas)

Motivo: Idem: retirada a afirmação restrita ao aquecimento pressurizado.

- Antes:  Quando o sistema de aquecimento opera com vaso de expansão pressurizado, essa função também contribui para manter o circuito cheio e reduzir instabilidades de circulação.
- Depois: (trecho removido)

## 05_02 — [5.2. Geração e distribuição de energia elétrica](05_02/documento.md)

**Condições que mudam o comportamento de frequência, tensão e reativos** · Q027 (aprovada com ressalvas)

Motivo: A resposta deveria ser mais abrangente e explicar o uso de 'tendência'. O documento passa a explicar o mecanismo da sobretensão.

- Antes: Próximo à velocidade nominal do motor, a demanda reativa tende a cair, o que pode favorecer sobretensão se a compensação temporária não for retirada.
- Depois: Próximo à velocidade nominal do motor, a demanda reativa cai. Se a compensação temporária de reativos usada para sustentar a tensão durante a partida não for retirada, ela passa a fornecer reativos em excesso em relação à nova demanda, e a tensão do barramento tende a subir, podendo chegar a sobretensão. Por isso, a compensação temporária deve ser retirada ou reduzida ao fim da aceleração.

## 06_05 — [6.5. Sistema de Fogo e Gás (F&G)](06_05/documento.md)

**Testes, manutenção e retorno ao serviço como evidência de funcionalidade** · Q035 (aprovada com ressalvas)

Motivo: Enunciado pouco claro ou ambíguo. O documento passa a definir disponibilidade administrativa e o que comprova a barreira.

- Antes: Disponibilidade administrativa de um detector ou de uma zona não equivale, por si só, a funcionalidade comprovada da barreira.
- Depois: Disponibilidade administrativa de um detector ou de uma zona, isto é, a retirada da inibição ou do bloqueio no sistema, não equivale, por si só, a funcionalidade comprovada da barreira; a comprovação vem do teste funcional da cadeia completa, da detecção à ação prevista na matriz de causa e efeito.

## 06_07 — [6.7. Segurança e Controle de Riscos](06_07/documento.md)

**Mudanças que alteram o comportamento do risco** · Q034 (aprovada com ressalvas)

Motivo: Enunciado pouco claro ou ambíguo. O documento passa a explicar por que a mudança de setpoint ou intertravamento altera o risco e exige gestão de mudanças.

- Antes: Já mudanças de setpoint, lógica de controle ou intertravamentos podem alterar a escalada do desvio e a resposta automática do sistema.
- Depois: Já mudanças de setpoint, lógica de controle ou intertravamentos, mesmo sem alteração de equipamentos ou de inventário, podem alterar a escalada do desvio e a resposta automática do sistema: mudam o ponto e o momento em que a proteção atua e, com isso, a margem disponível até a condição perigosa. Por isso, também são mudanças sujeitas à gestão de mudanças, com revisão da identificação de perigos e da avaliação de riscos da função afetada.

**Comando do incidente e compatibilidade entre estrutura documental e estrutura real** · Q036 (aprovada com ressalvas)

Motivo: Enunciado pouco claro ou ambíguo. O bloco era o relato de um caso específico (PRE, ICT, MECC); passa a ser um princípio geral, em linguagem direta.

- Antes: O PRE distribuía funções e pontos de encontro em diferentes locais da unidade, mas não apresentava quem deveria compor o Incident Command Team (ICT), isto é, o time de comando do incidente. Além disso, para incidentes de maior severidade, o procedimento previa mobilização em um Main Emergency Control Centre (MECC) com lideranças que não correspondiam integralmente à estrutura existente da organização local. Essa incompatibilidade indica desalinhamento entre o arranjo documental e a capacidade organizacional efetivamente disponível. Em termos técnicos, quando a estrutura prevista não coincide com cargos, centros de controle e interfaces realmente existentes, a tomada de decisão tende a depender mais de adaptação situacional do que de papéis previamente definidos.
- Depois: O Plano de Resposta a Emergências (PRE) precisa indicar não só funções e pontos de encontro, mas também quem compõe o time de comando do incidente (ICT, Incident Command Team). Para incidentes de maior severidade, os centros de controle previstos, como um centro principal de controle de emergência (MECC, Main Emergency Control Centre), e as lideranças designadas para eles devem corresponder a cargos e instalações que realmente existem na organização local. Quando o PRE omite a composição do comando ou atribui papéis a cargos, centros de controle e interfaces que não existem na unidade, há desalinhamento entre o arranjo documental e a capacidade organizacional efetivamente disponível. Na emergência, a coordenação e a tomada de decisão passam então a depender de improviso, isto é, de adaptação situacional, em vez de papéis previamente definidos e treinados.

## 07_02 — [7.2. Cibersegurança e Integridade de Sistemas Digitais](07_02/documento.md)

**Consequências práticas das falhas de suporte para a disponibilidade digital** · Q040 (aprovada com ressalvas)

Motivo: Enunciado pouco claro ou ambíguo. O bloco era uma sequência de relatos de incidentes com UPS; passa a explicar o mecanismo (modo de falha comum) e como distinguir falha de energia de comprometimento lógico.

- Antes: Há relato de série de falhas em UPS industriais associadas à falta de manutenção, com perda significativa de energia para sistemas de controle industrial, sistemas de shutdown de emergência e sistemas de mitigação de emergência. Em um incidente, falha de componentes do UPS levou a shutdown da instalação, acionamento do gerador de emergência, disparo de disjuntor de shunt e ocorrência de fumaça e arco elétrico na seção inversora, exigindo isolamento e bloqueio das fontes antes da colocação em bypass seguro. Em outro, durante teste, a ativação de sistema de segurança de emergência provocou perda de geração e shutdown; nesse cenário, o gerador de emergência falhou em partir e o UPS não forneceu a alimentação de backup esperada. Esses casos não definem frequência universal, mas mostram que
- Depois: A falta de manutenção em UPS pode levar à perda simultânea de energia para sistemas de controle industrial, de shutdown de emergência e de mitigação de emergência, porque esses sistemas podem depender da mesma alimentação ininterrupta; a UPS torna-se, assim, um modo de falha comum para barreiras distintas. Uma falha de componentes da UPS pode levar a shutdown da instalação, acionamento do gerador de emergência e disparo de proteções elétricas, e pode se manifestar com fumaça e arco elétrico na seção inversora; nesse caso, a resposta passa por isolar e bloquear as fontes antes de colocar as cargas críticas em bypass seguro. A UPS também precisa ser vista como parte da cadeia de emergência: se a geração principal for perdida e o gerador de emergência não partir, ela é o meio que resta para manter alimentadas as funções críticas. Sinais físicos locais, como fumaça, arco elétrico e atuação de proteções, associados à perda simultânea de sistemas que compartilham a mesma alimentação, apontam para falha da infraestrutura de energia; alteração de lógica, de setpoints ou comandos não autorizados é que caracterizaria comprometimento do controle. Esses mecanismos mostram que

**Relação entre incidente digital e emergência operacional** · Q040 (aprovada com ressalvas)

Motivo: Idem: relato de caso convertido em mecanismo.

- Antes: Há situações em que a resposta operacional assume prioridade imediata: diante de fumaça e arco elétrico em UPS, o isolamento seguro das partes com falha e o uso de bypass seguro permitiram manter alimentação de equipamentos críticos enquanto se inspecionava o dano. Em outro caso, durante teste, a ativação de sistema de segurança levou à perda de geração e shutdown, com deluge total, alarme de abandono, falha de partida do gerador de emergência e falha da UPS em fornecer potência de backup. Esses exemplos mostram que eventos elétricos, de automação e de segurança podem se encadear rapidamente.
- Depois: Há situações em que a resposta operacional assume prioridade imediata: diante de fumaça e arco elétrico em UPS, o isolamento seguro das partes com falha e a transferência para bypass seguro permitem manter a alimentação de equipamentos críticos enquanto o dano é inspecionado. Eventos elétricos, de automação e de segurança podem se encadear rapidamente: a perda da geração principal, somada à falha de partida do gerador de emergência e à indisponibilidade da UPS, pode deixar sem energia as funções de segurança justamente durante a emergência.

## 08_01 — [8.1. Saúde Ocupacional](08_01/documento.md)

**Como a avaliação quantitativa pode ser estruturada** · Q045 (reprovada)

Motivo: Questão reprovada por enunciado pouco claro ou ambíguo. O bloco misturava o relato de um estudo específico com o princípio; o relato sai e o papel de cada estratégia amostral fica explícito.

- Antes: Em um estudo com benzeno em plataformas de produção da Bacia de Campos, essa combinação foi usada com tratamento estatístico dos resultados para decisão sobre a exposição na jornada, e houve medição simultânea de teores de benzeno nas linhas de processo.
- Depois: Essa combinação pode ser apoiada por tratamento estatístico dos resultados para decisão sobre a exposição na jornada e, quando pertinente, por medição dos teores do agente nas correntes de processo.

**Como a avaliação quantitativa pode ser estruturada** · Q045 (reprovada)

Motivo: Idem: distinção explícita entre ponto fixo, amostragem pessoal e amostra de curta duração.

- Antes: Em FPSO, pontos fixos ajudam a vigiar áreas de presença frequente, enquanto a amostragem pessoal é mais representativa quando o trabalhador se desloca entre fontes, microambientes e tarefas.
- Depois: Em FPSO, pontos fixos ajudam a vigiar a concentração ambiental em áreas de presença frequente, mas não medem a exposição individual. A amostragem pessoal, com o amostrador junto à zona respiratória do trabalhador, é mais representativa quando ele se desloca entre fontes, microambientes e tarefas, e as amostras de curta duração captam picos de tarefas breves que a média da jornada ou a leitura de um ponto fixo podem diluir. Assim, um resultado baixo em ponto fixo não descarta exposição relevante de quem executa intervenções curtas junto às fontes.

## 08_02 — [8.2. Segurança Ocupacional](08_02/documento.md)

**Ventilação, purga, lavagem e monitoramento da atmosfera** · Q047 (aprovada com ressalvas)

Motivo: Enunciado pouco claro ou ambíguo. O documento passa a dizer de forma direta onde e quando medir a atmosfera em espaço confinado.

- Antes: Por isso, a condição atmosférica pode precisar de acompanhamento durante a execução, e não apenas de verificação inicial.
- Depois: Por isso, a medição precisa abranger os diferentes pontos e níveis do espaço, inclusive a zona onde o trabalho será executado, e não apenas a região próxima ao acesso; e, quando a atividade pode liberar contaminantes, como na remoção de resíduos ou borras, a atmosfera precisa ser monitorada continuamente durante a execução, e não apenas verificada no início.

## 08_03 — [8.3. Meio Ambiente, Gestão Ambiental e Sustentabilidade](08_03/documento.md)

**O que é água produzida e por que ela exige gestão própria** · Q044 (aprovada com ressalvas)

Motivo: Pedido para eliminar 'e do volume a tratar' da resposta (redundante com carga hidráulica) e observação de que a questão não é de SMS. O documento retira a redundância e acrescenta o enfoque ambiental.

- Antes: o aumento da produção de água eleva carga hidráulica, volume a tratar, exposição de equipamentos a incrustação e corrosão, consumo de insumos e potencial de impacto ambiental. Por isso, água produzida deve ser tratada como uma corrente de processo com requisitos de caracterização, controle e destinação, e não como um resíduo aquoso genérico.
- Depois: o aumento da produção de água eleva a carga hidráulica do tratamento, a exposição de equipamentos a incrustação e corrosão, o consumo de insumos e o potencial de impacto ambiental. Por isso, água produzida deve ser tratada como uma corrente com requisitos de caracterização, controle e destinação, e não como um resíduo aquoso genérico. Sob a ótica de meio ambiente, o foco recai sobre a qualidade do efluente descartado, o monitoramento dos parâmetros de enquadramento e a escolha entre descarte e reinjeção.

## 09_01 — [9.1. Logística e Suprimento Offshore](09_01/documento.md)

**Função logística das embarcações no atendimento offshore** · Q050 (aprovada com ressalvas)

Motivo: Resposta incompleta: descrevia o PSV como 'a embarcação mais recorrente' em vez de dizer sua função. O documento adota a definição funcional sugerida pelo especialista.

- Antes: O Platform Supply Vessel (PSV) é o meio mais recorrente para suprimento de plataformas e unidades de produção, porque combina área de convés para carga seca com tanques para granéis líquidos e outros insumos operacionais.
- Depois: O Platform Supply Vessel (PSV) tem como função realizar o transporte e a entrega de suprimentos às unidades offshore, incluindo cargas de convés, granéis líquidos e sólidos, equipamentos e materiais operacionais, além de permitir o retorno de cargas às bases de apoio em terra. É o meio mais recorrente para suprimento de plataformas e unidades de produção, porque combina área de convés para carga seca com tanques para granéis líquidos e sólidos e outros insumos operacionais.

**Operações noturnas, CFIT/W e wrong deck landing** · Q052 (reprovada)

Motivo: Questão reprovada por erro técnico: tripulação não familiarizada com o local não condiz com a realidade da segurança de voo, ainda mais à noite. O documento deixa de tratar essa condição como cenário operacional.

- Antes: Esse risco aumenta com visibilidade limitada, excesso de instalações semelhantes e baixa familiaridade da tripulação com a área.
- Depois: Esse risco aumenta com visibilidade limitada e com a presença de várias instalações semelhantes próximas. A familiarização da tripulação com a área e com as unidades atendidas faz parte da qualificação exigida pela segurança de voo offshore, sobretudo para operações noturnas; tripulação não familiarizada com o local não corresponde a uma condição normal de operação.

## 10_01 — [10.1. Descomissionamento e Gestão do Ciclo de Vida da Unidade](10_01/documento.md)

**Sequência de módulos, distribuição de pesos e resistência estrutural** · Q057 (aprovada com ressalvas), Q059 (reprovada)

Motivo: Q057 com enunciado e resposta pouco claros; Q059 reprovada com o comentário de que a retirada de módulos segue plano detalhado considerando o peso de cada item e a estabilidade. O documento passa a apresentar a sequência como plano prévio e a explicar 'sensibilidade estrutural'.

- Antes: Por isso, a sequência não deve ser pensada apenas pela facilidade de acesso, mas pela combinação entre acessibilidade, manutenção das funções essenciais, capacidade de içamento disponível e comportamento estrutural da unidade a cada etapa. Em geral, remoções assimétricas, retirada prematura de elementos que contribuem para rigidez global, concentração de cargas temporárias em áreas degradadas ou permanência prolongada em configuração parcialmente desmantelada tendem a aumentar a sensibilidade estrutural.
- Depois: Por isso, a desmontagem segue um plano detalhado, no qual a sequência de retirada de módulos e equipamentos é definida previamente considerando o peso de cada item, a estabilidade e a resistência estrutural da unidade a cada etapa, além da acessibilidade, da manutenção das funções essenciais e da capacidade de içamento disponível. O plano busca evitar configurações que reduzam a margem de estabilidade ou de resistência nos estados intermediários, como remoções assimétricas, retirada prematura de elementos que contribuem para a rigidez global, concentração de cargas temporárias em áreas degradadas ou permanência prolongada em configuração parcialmente desmantelada.

**Levantamentos e controle de integridade para decidir e monitorar** · Q059 (reprovada)

Motivo: Questão reprovada por erro técnico: o cenário de incerteza relevante em massa, distribuição de peso e centro de gravidade na preparação para reboque não guarda semelhança com a realidade, porque o descomissionamento segue plano detalhado com controle de pesos. O documento retira o contrafactual e descreve o controle.

- Antes: Na aplicação ao transporte, esses levantamentos precisam ser convertidos em premissas de engenharia, como massa total, distribuição de peso, posição do centro de gravidade e disponibilidade operacional de compartimentos de lastro. Quando essas entradas são incertas, a confiabilidade das análises hidrostáticas, estruturais e do arranjo de reboque também se reduz.
- Depois: Na aplicação ao transporte, esses levantamentos são convertidos, no plano de descomissionamento, em premissas de engenharia como massa total, distribuição de peso, posição do centro de gravidade e disponibilidade operacional de compartimentos de lastro. Essas premissas são controladas ao longo do plano, com acompanhamento do peso de cada item removido ou acrescentado, e alimentam as análises hidrostáticas, estruturais e do arranjo de reboque.

**Sistemas essenciais, redução progressiva da planta e mudança de barreiras** · Q058 (reprovada)

Motivo: Questão reprovada por enunciado e resposta pouco claros: misturava a redução progressiva da planta com SIMOPS segregadas. O documento separa os dois mecanismos.

- Antes: Tecnicamente, essa redução progressiva muda as barreiras de prevenção, controle e mitigação porque sistemas antes permanentes podem ser retirados, isolados ou substituídos por arranjos remanescentes ou temporários.
- Depois: Tecnicamente, essa redução progressiva é, por si só, um mecanismo de aumento de risco, independente da segregação das operações simultâneas: sistemas antes permanentes são retirados, isolados ou substituídos por arranjos remanescentes ou temporários, e isso muda as barreiras de prevenção, controle e mitigação.

**Içamentos pesados, SIMOPS e seleção da estratégia operacional** · Q058 (reprovada)

Motivo: Idem: SIMOPS sem segregação apresentado como mecanismo distinto.

- Antes: O risco cresce quando corte, içamento, transferência de carga, apoio marítimo, manutenção temporária de sistemas essenciais e atividades em áreas distintas ocorrem ao mesmo tempo sem segregação suficiente.
- Depois: O risco cresce quando corte, içamento, transferência de carga, apoio marítimo, manutenção temporária de sistemas essenciais e atividades em áreas distintas ocorrem ao mesmo tempo sem segregação suficiente. Esse é um mecanismo distinto da redução progressiva da planta: a segregação das SIMOPS controla a interferência entre atividades, mas não restitui as redundâncias e barreiras perdidas com a retirada de sistemas.
