# Equipamentos de conexão subsea e readiness aplicáveis ao pull-in/connection

## 1. Delimitação técnica da faceta
*Fontes: `regis-9f26642710f28350a07f0d09:pNone:130.60-154.0`, `regis-9f26642710f28350a07f0d09:pNone:155.60-196.0`, `regis-9f26642710f28350a07f0d09:pNone:197.0-231.0`, `petroles-004c2afadba7ea17c7dd7908:pNone:2663150.0-2663195.0`*

O material disponível não descreve, de forma direta e completa, operações de pull-in de risers em FPSO com guinchos, sheaves, cabeças de pull-in e transferência de carga para hang-off final. Ele trata principalmente de:

- interfaces de conexão submarina em ANMH, tubing hanger e MCVU;
- conectores elétricos e hidráulicos operados ou assistidos por ROV;
- preparação, testes funcionais, qualificação e lições aprendidas de operações subsea de conexão;
- módulos de conexão vertical (MCV) em extremidade de linha/duto, com elementos de alinhamento, soft landing e comando por ROV.

Assim, este documento cobre **aspectos de readiness, capacidade, testes e preparação de equipamentos de conexão/pull-in na etapa final de aproximação e engajamento subsea**, extraindo princípios úteis para avaliação profissional de equipamentos. Não cobre, por insuficiência de fonte, o dimensionamento completo de tração de risers para FPSO.

---

## 2. Filosofia de readiness de equipamentos de pull-in/conexão
*Fontes: `regis-9f26642710f28350a07f0d09:pNone:130.60-154.0`, `regis-9f26642710f28350a07f0d09:pNone:197.0-231.0`, `petroles-004c2afadba7ea17c7dd7908:pNone:2663150.0-2663195.0`*

A prontidão operacional dos equipamentos, à luz dos trechos fornecidos, depende de quatro grupos de verificação:

1. **Compatibilidade geométrica e de interface**  
   O equipamento deve caber no envelope disponível, alinhar-se corretamente ao receptáculo/mandril e manter acesso operacional para ROV, ferramentas de torque, hot stabs, jumpers e conectores. As fontes mostram que restrições de espaço podem se tornar o fator crítico do projeto, como no desenvolvimento de conectores de potência para instalação no topo do tubing hanger.

2. **Capacidade funcional e de vedação**  
   O conjunto precisa suportar a função prevista: travamento mecânico, vedação metal-metal e/ou resiliente, transmissão de sinais, transmissão de potência, acionamento hidráulico, e, quando requerido, vedação a gás.

3. **Operabilidade na instalação**  
   Peso submerso, comprimento, necessidade de orientação, necessidade de soft landing, possibilidade de destravamento secundário e controle por ROV afetam diretamente a executabilidade da operação. Os casos descritos mostram que o simples atendimento da função nominal não basta; o equipamento precisa ser manobrável e conectável em campo.

4. **Testabilidade e monitoramento**  
   Readiness inclui prever meios de teste antes e durante a instalação: pressurização funcional, testes de continuidade, resistência de isolamento, monitoramento de sinais, diagnóstico de falhas e confirmação visual/operacional por ROV.

Em operações de pull-in/conexão, isso significa que a liberação do equipamento não deve se apoiar apenas na capacidade nominal de catálogo, mas na combinação de **capacidade + interface + operabilidade + testabilidade**.

---

## 3. Equipamentos e interfaces relevantes

### 3.1 Capa lógica, MQC e interfaces hidráulicas de teste/acionamento
*Fontes: `regis-9f26642710f28350a07f0d09:pNone:130.60-154.0`*

A capa lógica é descrita como um elemento acoplado ao topo da ANMH, com função de remanejamento de funções hidráulicas atuadas a partir da unidade de produção. Para readiness operacional, destacam-se:

- **flutuador e baixo peso submerso**: a capa tem baixo peso submerso da ordem de 100 kg, o que facilita instalação e recuperação;
- **material não metálico**: contribui para menor peso;
- **sistema anti-back-off**: ajusta-se à posição final do mandril de travamento do suspensor, evitando perda de pré-carga e ajudando a preservar a integridade das vedações metal-metal;
- **destravamento secundário por ferramenta via cabo**: importante como contingência caso o caminho principal falhe;
- **loops hidráulicos com couplings e check valves**: favorecem remanejamento em superfície e reduzem risco de retorno indesejado de fluido;
- **conector mecânico para travamento ao hub**, permitindo **testes até 5.000 psi**;
- **stabs com vedação resiliente** no hub do MCVU;
- uso de **MQC MK-II com painel de ROV**, acoplada ainda na superfície à MQC plate residente na ANMH;
- atuação, via hot stab no painel de ROV, de quatro funções: **lock da ANMH, unlock da ANMH, seal test VGX e teste da bucha**.

Do ponto de vista de readiness, esse arranjo mostra uma boa prática importante: o sistema de conexão deve incorporar recursos específicos para **teste funcional, acionamento remoto e contingência de destravamento**.

### 3.2 Conectores, jumpers e receptáculos de sinal e potência
*Fontes: `regis-9f26642710f28350a07f0d09:pNone:155.60-196.0`*

O sistema elétrico da ANMH é dividido em:

- **sistema de monitoração de sinais**;
- **sistema elétrico de potência**.

Os trechos descrevem vários componentes relevantes para a preparação e testes de conexão subsea:

#### a) Para sinais
- jumpers para ROV entre MCVU e ANMH;
- jumper com long neck ROV plug entre ANMH e tubing hanger;
- jumper elétrico de sinal para teste com ROV durante a instalação;
- receptáculos do tipo seaswitch para conexão, estacionamento e teste;
- dummy plug com resistores para **testes de continuidade**;
- parking receptacle para **testes de resistência de isolamento**;
- conectores associados à ferramenta de instalação do suspensor e da ANMH para leitura dos sinais de PDG durante a descida.

#### b) Para potência
- ROV power electrical jumper entre MCVU e suspensor de coluna, passando pela tree cap;
- jumper elétrico de potência para teste com ROV durante a instalação;
- ROV wet mate receptacle connector ligado ao cross-over de potência do umbilical;
- parking receptacle para ensaio de isolamento;
- test plug connector para ensaio de continuidade;
- tubing hanger wet mate receptacle connector com vedação metal-metal tipo SBMS.

Em termos de readiness, isso evidencia três requisitos:

1. **o projeto do equipamento deve prever pontos dedicados de teste**, e não depender apenas da conexão final;  
2. **os acessórios de instalação são parte do sistema**, não meros itens auxiliares;  
3. **a arquitetura de estacionamento e teste** reduz manuseio indevido e ajuda a preservar conectores enquanto não engajados.

### 3.3 MCV como exemplo de sistema de conexão com alinhamento e redução de dano
*Fontes: `petroles-004c2afadba7ea17c7dd7908:pNone:2663150.0-2663195.0`*

O trecho sobre MCV é particularmente útil para a faceta de equipamentos de pull-in/conexão porque explicita os subconjuntos de um terminal de conexão subsea. O MCV é composto por:

- **pescoço de ganso (gooseneck)**;
- **conector**;
- **sistema de soft landing**;
- **painel de ROV**;
- **sistema de guia**;
- **swivel** na extremidade do flange.

As funções associadas são relevantes:

- o **conector** realiza o travamento entre MCV e mandril e energiza os selos de vedação;
- o **soft landing** suaviza o assentamento final e evita danos aos elementos de vedação;
- o **sistema de guia** aproxima o eixo vertical do MCV ao eixo do mandril, favorecendo o encaixe completo;
- o **painel de ROV** permite comandar as operações subsea;
- o **swivel** permite rotação relativa e ajuda a eliminar efeito de torque residual que dificultaria o alinhamento;
- para **conexão de segunda extremidade**, pode ser necessário um **cabo adicional para suspender o duto próximo à extremidade**, com a finalidade explícita de **reduzir as cargas no conector**.

Mesmo não sendo um sistema de pull-in de riser em FPSO, o MCV mostra um princípio central: **a capacidade do equipamento de conexão não é só resistência estrutural; inclui controle de alinhamento, limitação de momento fletor, redução de torque e proteção de selos no assentamento final**.

---

## 4. Critérios de dimensionamento e qualificação de equipamentos

### 4.1 Capacidade elétrica, vedação e restrição geométrica
*Fontes: `regis-9f26642710f28350a07f0d09:pNone:130.60-154.0`, `regis-9f26642710f28350a07f0d09:pNone:155.60-196.0`*

Os conectores elétricos previamente utilizados em projetos submarinos da Petrobras eram projetados para cerca de **5 kV e 150 A**, possibilitando uso de BCS até **1.000 HP**. Para o caso citado, houve necessidade de desenvolver conectores de **8 kV x 200 A** para um sistema de BCSS de **1.200 HP**.

Os critérios de readiness extraíveis desse caso são:

- **capacidade nominal deve ser confrontada com a demanda real do sistema**;
- **restrição geométrica** pode dominar o projeto: o conector deveria ser instalado no topo do TH em espaço restrito, com diâmetro disponível de **4,17 pol**;
- **isolação elétrica** deve atender às tensões de teste exigidas para qualificação;
- **falha para terra (Uo)** é um requisito explícito de qualificação;
- quando houver possibilidade de **gas lift de reserva**, o conector também precisa de **vedação a gás**;
- conectores de sinal associados ao PDG também podem exigir **qualificação com vedação a gás**.

Portanto, para equipamentos de pull-in/conexão, o dimensionamento adequado é multidisciplinar: **capacidade funcional + envelope geométrico + requisito de vedação + compatibilidade com cenários operacionais futuros**.

### 4.2 Critérios normativos e ensaios citados
*Fontes: `regis-9f26642710f28350a07f0d09:pNone:130.60-154.0`*

Para as válvulas esferas do suspensor de coluna, o texto informa:

- **testes de aceitação** conforme **API 6A PSL-3**;
- **atuador** conforme **API 17D**;
- **teste de qualificação** conforme **API 6A, Apêndice F, PR-2 (500 ciclos)**.

Embora essas referências se apliquem ao contexto específico das válvulas/atuadores do suspensor e não a todos os itens de pull-in, elas ilustram um ponto essencial de readiness: **o equipamento crítico deve ter trilha de aceitação e qualificação claramente definida, com critérios de ciclo e desempenho apropriados à função**.

### 4.3 Vedação e barreiras de segurança
*Fontes: `regis-9f26642710f28350a07f0d09:pNone:130.60-154.0`*

O suspensor de coluna descrito possui:

- metalurgia compatível com **H2S e CO2**;
- duas válvulas esfera acionadas simultaneamente;
- requisito de vedação a gás importante para evitar hidratos;
- saída lateral com vedação primária metal-metal tipo **SBMS-II** e secundária elastomérica tipo **S-seal**;
- selo externo projetado para vedação com **gás (N2) a 3.000 psi** e com **água a 5.000 psi** como segunda barreira.

Isso reforça que readiness de conexão não se restringe a “conseguir engatar”: é preciso demonstrar que, após a conexão, a integridade de vedação e a função de barreira permanecem válidas nas condições previstas.

---

## 5. Preparação, testes funcionais e verificação pré-operação

### 5.1 Testes funcionais hidráulicos durante a instalação
*Fontes: `regis-9f26642710f28350a07f0d09:pNone:130.60-154.0`*

Para permitir instalação a cabo da ANMH, a capa de teste do hub do MCVU é dotada de jumpers que permitem teste funcional da árvore. O ROV, por meio desses jumpers, consegue:

- pressurizar linhas de controle dos atuadores;
- observar no painel da ANMH a abertura completa dos atuadores.

Esse arranjo é representativo de um requisito robusto de readiness: **validar funcionalmente o equipamento no ambiente de instalação, antes da consolidação final da conexão**.

### 5.2 Testes de continuidade e resistência de isolamento
*Fontes: `regis-9f26642710f28350a07f0d09:pNone:155.60-196.0`, `regis-9f26642710f28350a07f0d09:pNone:197.0-231.0`*

As fontes citam, de forma explícita, meios dedicados para ensaios elétricos subsea:

- **parking receptacle** para testes de resistência de isolamento;
- **dummy ROV plug with resistors** e **test plug connector/test receptacle** para testes de continuidade;
- monitoramento de sinais do PDG, PT e TPT durante descida e instalação;
- uso de cabos do umbilical de controle ou do umbilical de ROV para monitorar o isolamento dos cabos.

Também é citado o uso de **TDR (Time Domain Reflectometery)** para localizar a origem de baixo isolamento, distinguindo defeito no umbilical de controle de defeito nos cabos de BCS/PDG. Isso mostra que a readiness adequada inclui não apenas ensaiar, mas **ter capacidade diagnóstica para localizar a falha e evitar ações corretivas equivocadas**.

### 5.3 Simulação e testes físicos de manuseio por ROV
*Fontes: `regis-9f26642710f28350a07f0d09:pNone:197.0-231.0`*

A conexão dos conectores elétricos com auxílio de ROV foi tratada como aspecto crítico do projeto. Foram empregados dois níveis de preparação:

1. **simulação computadorizada das principais operações com ROV**;  
2. **testes em tanque**, realizados para reproduzir melhor o comportamento das operações.

Há uma lição relevante de readiness: a simulação computacional planejada **não conseguiu reproduzir adequadamente as operações**, por limitações do software, mas ainda assim ajudou no planejamento com os operadores. Já os testes em tanque permitiram **modificações importantes no projeto dos conectores elétricos**.

Conclusão operacional: para equipamentos de conexão/pull-in com interação fina de ROV, **simulação digital é útil, mas não substitui ensaio físico quando a sensibilidade geométrica e de manuseio é alta**.

---

## 6. Capacidade operacional, manuseio e efeitos de carga/alinhamento
*Fontes: `regis-9f26642710f28350a07f0d09:pNone:197.0-231.0`, `petroles-004c2afadba7ea17c7dd7908:pNone:2663150.0-2663195.0`*

As fontes não fornecem fórmulas de pull-in nem curvas de carga, mas fornecem indícios claros dos fatores de capacidade e operabilidade.

### 6.1 Peso, comprimento e acessibilidade
A tree cap instalada por ROV exigiu conectores elétricos muito longos, de cerca de **1,40 m**, e o conector de potência tinha cerca de **40 kg**. Esses valores são relevantes porque mostram que a viabilidade da conexão depende de:

- capacidade de manipulação pelo ROV;
- controle de inércia e desalinhamento do conector;
- folgas geométricas disponíveis na interface;
- compatibilidade do envelope do conector com o acesso real em campo.

### 6.2 Redução de momento e torque residual
No sistema com MCV, a evolução do projeto descrita mostra duas preocupações mecânicas clássicas de operações de conexão:

- o duto/linha pode impor **momento fletor** ao conector, prejudicando verticalidade;
- pode haver **torque residual**, dificultando o alinhamento final.

A introdução do **swivel** e, em certas condições, de **cabo adicional para aliviar a extremidade da linha**, revela um princípio prático importante: **o equipamento de conexão deve ser avaliado não só pela carga axial, mas pelos efeitos de momento e torque transmitidos pela linha durante a aproximação e o assentamento**.

### 6.3 Soft landing e proteção de vedação
O sistema de **soft landing** do MCV é descrito como meio de suavizar o assentamento final para evitar danos aos elementos de vedação. Em operações de pull-in/conexão, essa função equivale a controlar a energia de contato no instante final de engajamento, reduzindo risco de:

- dano aos selos;
- assentamento enviesado;
- necessidade de retrabalho;
- comprometimento da estanqueidade logo após a conexão.

---

## 7. Lições aprendidas e implicações para decisão operacional
*Fontes: `regis-9f26642710f28350a07f0d09:pNone:197.0-231.0`, `regis-9f26642710f28350a07f0d09:pNone:155.60-196.0`*

### 7.1 Não confundir adequação funcional pontual com qualificação completa
O caso citado informa que os conectores instalados na ANMH eram de **8 kV x 200 A**, porém com qualificação de **falha para terra de 4,6 kV**, abaixo do requerido de projeto, embora considerados suficientes para o motor efetivamente instalado (**5 kV x 180 A**, 1.200 HP).

A lição para readiness é clara:

- um equipamento pode ser **funcionalmente utilizável** em um caso específico;
- isso **não equivale** a dizer que o requisito de projeto foi integralmente atendido;
- qualquer aceitação dessa natureza requer análise formal de risco, limites de uso e consciência de que a margem futura pode ficar reduzida.

### 7.2 Interface tardia é fonte de risco operacional
Foi identificado problema de interface da ANMH com o BOP de perfuração, exigindo adaptador. Mais tarde, verificou-se também proximidade ao limite aceitável na interface com a junta de riser cisalhável.

Isso mostra que a readiness dos equipamentos de conexão deve incluir, antes da campanha:

- verificação de interfaces entre todos os equipamentos temporários e permanentes;
- checagem de envelopes de altura e posição relativa;
- confirmação de compatibilidade com dispositivos de corte, vedação e manobra.

### 7.3 Dificuldade de montagem em campo pode indicar estratégia de pré-montagem
A montagem do conector elétrico de potência no suspensor foi descrita como complicada devido ao comprimento e diâmetro. O texto sugere, para futuras instalações, avaliar a possibilidade de **pré-montar o conector no suspensor** e fazer um **splice** no cabo elétrico do BCS.

Como princípio geral, quando o campo evidencia montagem difícil ou suscetível a erro, vale considerar:

- pré-montagem em ambiente controlado;
- redução do número de operações finas subsea;
- revisão da sequência de instalação para deslocar complexidade para a superfície.

### 7.4 Limites operacionais devem ser respeitados e registrados
Durante o teste do suspensor, houve grande dificuldade para fechar uma válvula x-over da ANMH, sendo necessário aplicar **600 lb·ft**, acima do torque máximo de trabalho de **300 lb·ft**.

Esse dado reforça que readiness não é apenas ter a ferramenta disponível; é ter confirmação de que:

- a função será executada **dentro do envelope de torque/força admissível**;
- desvios sejam tratados como indício de anomalia mecânica, ajuste incorreto, travamento ou condição fora do projeto.

---

## 8. Síntese prática para avaliação profissional de equipamentos de pull-in/readiness
*Fontes: `regis-9f26642710f28350a07f0d09:pNone:130.60-154.0`, `regis-9f26642710f28350a07f0d09:pNone:155.60-196.0`, `regis-9f26642710f28350a07f0d09:pNone:197.0-231.0`, `petroles-004c2afadba7ea17c7dd7908:pNone:2663150.0-2663195.0`*

Com base nos trechos fornecidos, a avaliação de readiness de equipamentos de conexão/pull-in deve verificar, no mínimo:

1. **Capacidade nominal versus demanda real**  
   Tensão, corrente, pressão, vedação, compatibilidade química e capacidade funcional devem ser consistentes com o serviço.

2. **Envelope geométrico e interfaces**  
   Espaço disponível, diâmetro, comprimento do conector, acessibilidade do ROV, alinhamento com receptáculos/mandris e interferências com equipamentos adjacentes precisam ser verificados antecipadamente.

3. **Recursos de conexão assistida**  
   Painéis de ROV, hot stabs, sistemas de guia, soft landing, swivels, travamento mecânico, destravamento secundário e acessórios de estacionamento/teste são parte crítica do sistema.

4. **Testabilidade antes e durante a instalação**  
   O equipamento deve prever meios dedicados para teste funcional, continuidade, isolamento e diagnóstico de falhas.

5. **Operabilidade real em campo**  
   Peso submerso, comprimento, manobrabilidade e comportamento dinâmico durante a aproximação final precisam ser validados, preferencialmente com testes físicos quando a operação for sensível.

6. **Gestão de contingências**  
   Baixo isolamento, incompatibilidade de interface, torque acima do limite, dificuldade de alinhamento ou impossibilidade de simulação fiel devem gerar revisão de procedimento, mitigação adicional ou redefinição da estratégia de instalação.

7. **Aceitação técnica não é sinônimo de conformidade plena**  
   Uso de componente fora da qualificação original, ainda que operacionalmente justificável num caso particular, deve ser tratado como exceção com limites explícitos.

Em resumo, os trechos sugerem uma abordagem robusta de readiness: **um equipamento de pull-in/conexão está realmente pronto quando é qualificado para a função, compatível com as interfaces, testável em campo, operável pelo sistema de instalação e capaz de preservar a integridade de vedação e alinhamento durante o engajamento final**.