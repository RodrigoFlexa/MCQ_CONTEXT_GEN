# Barreiras e elementos críticos

Este texto consolida conceitos e exemplos extraídos dos trechos fornecidos para apoiar avaliação profissional de barreiras preventivas e mitigadoras em FPSO/FSO e produção offshore. O conteúdo **não deve ser tratado como certificação técnica**; há trechos de práticas corporativas, alertas, nota técnica regulatória e estudos de caso usados aqui como base conceitual e ilustrativa.

## 1. Conceitos centrais: barreiras, evento topo e independência

A gestão de risco de processo depende do uso de **múltiplas barreiras de segurança** para prevenir a liberação de substâncias perigosas e limitar suas consequências. Um princípio recorrente nas fontes é que essas barreiras devem operar de forma **independente**, de modo que uma falha comum não comprometa várias salvaguardas ao mesmo tempo. Também aparece o critério de que uma barreira não deve ser removida sem demonstração de que as demais salvaguardas remanescentes continuam **adequadas e suficientes** para manter o risco aceitável. Quando ocorre perda de contenção, devem existir **medidas mitigadoras independentes** para evitar escalada do acidente.

Na lógica do **Bow Tie**:
- **Perigo** é a propriedade ou condição com potencial de causar dano.
- **Ameaças/causas** são os eventos ou condições que podem levar à perda de controle do perigo.
- **Evento topo** ou **evento principal** é a perda de controle sobre o perigo, ponto a partir do qual os impactos podem se materializar.
- **Barreiras preventivas** ficam à esquerda do evento topo e atuam para impedir sua ocorrência, limitar sua proporção ou reduzir sua probabilidade.
- **Barreiras mitigadoras** ficam à direita e atuam para evitar, reduzir ou mitigar as consequências após o evento topo.
- **Fatores de degradação/escalonamento** são condições que deterioram a capacidade da barreira; por isso exigem controles específicos.
- **Consequências** são os danos pessoais, ambientais e patrimoniais decorrentes do evento topo.

As fontes também classificam barreiras por sua natureza funcional:
- **Comportamentais**: dependem diretamente da ação humana.
- **Sócio-técnicas**: dependem da interação homem-máquina.
- **Hardware**: equipamentos, lógica de controle, detecção, alarme, redundância e projeto seguro.

Uma distinção prática importante é entre **barreiras humanas/procedimentais** e **barreiras hardware**. As humanas incluem procedimentos e respostas operacionais; as hardware incluem equipamentos e sistemas essenciais para manter a efetividade da proteção.

**Fontes:** `petroles-4ee4bce16acf674505c8912d:pNone:2091004.0-2091038.0`, `petroles-004c2afadba7ea17c7dd7908:pNone:466560.0-466586.0`, `regis-962e222ee3c37dec82110fd6:pNone:3221.0-3557.0`

## 2. Elementos críticos de segurança operacional

Os trechos associados à ANP definem **Elemento Crítico de Segurança Operacional** como qualquer equipamento ou elemento estrutural da instalação que, em caso de falha, possa causar ou contribuir significativamente para um quase acidente ou acidente operacional. Em termos práticos, são os componentes cuja disponibilidade, funcionalidade e desempenho são decisivos para que as barreiras do cenário acidental funcionem.

Em uma metodologia de diagnóstico citada nas fontes, os cenários escolhidos para monitoramento derivam da **APR** com severidade crítica ou catastrófica nas dimensões pessoas, meio ambiente e patrimônio. Os elementos que compõem as salvaguardas preventivas e mitigadoras desses cenários são tratados como elementos críticos.

Outro conceito relevante é o de **Performance Standard (PS)** para SCE: cada elemento crítico deve ter um resultado esperado de desempenho, contra o qual sua condição é verificada. A integração entre **análise de riscos/safety case**, **Bow Tie** e **programa de integridade de ativos** é apontada como essencial para que os riscos identificados sejam reduzidos de forma sistemática até patamar ALARP.

As fontes regulatórias também sugerem que a gestão de elementos críticos não se limite apenas a equipamentos. Há desvio apontado pela ANP para ausência, na lista de elementos críticos, de **procedimentos críticos** descritos na matriz de treinamento. Isso indica que, dependendo da arquitetura de controle do risco, um procedimento crítico pode precisar receber tratamento equivalente ao de um elemento crítico da barreira.

**Fontes:** `petroles-004c2afadba7ea17c7dd7908:pNone:466574.0-466603.0`, `petroles-4ee4bce16acf674505c8912d:pNone:2091004.0-2091038.0`, `anp-21b016bb482410ebc1a9261e:p7-8:159.0-109.0`

## 3. Definição das barreiras no Bow Tie e exemplos de grupos de barreiras

As fontes apresentam um modelo qualitativo em que o Bow Tie torna visível a relação entre ameaças, evento topo, falhas de barreiras e consequências. Isso é útil não apenas para análise de risco inicial, mas também para diagnóstico operacional, investigação de incidentes e definição de contingências.

Um dos materiais descreve, para instalações marítimas de produção, um **conjunto padrão** de barreiras adotado em determinada metodologia:

### Barreiras preventivas
1. **Contenção primária**
2. **Controle básico do processo**
3. **Alarmes críticos e intervenção humana**
4. **Intertravamentos de segurança**
5. **Sistemas de alívio**

### Barreiras mitigadoras
1. **Sistemas de proteção pós-liberação**
2. **Resposta à emergência da planta**
3. **Resposta à emergência da instalação**
4. **Evacuação, resgate e abandono**

Esse tipo de decomposição é tecnicamente útil porque obriga a avaliar o risco em camadas: prevenção da perda de contenção, detecção/desvio do processo, atuação automática, limitação da liberação e, se o evento topo ocorrer, resposta de emergência e salvamento.

As fontes também reforçam que a análise não deve parar na existência nominal da barreira. Para cada barreira, é necessário identificar:
- sua **função de segurança**;
- os **elementos críticos** que a compõem;
- os **fatores de degradação** que podem torná-la inefetiva;
- os **controles** usados para preservar sua integridade;
- as **condições operacionais** nas quais ela é válida.

**Fontes:** `petroles-004c2afadba7ea17c7dd7908:pNone:466560.0-466586.0`, `regis-962e222ee3c37dec82110fd6:pNone:3221.0-3557.0`

## 4. Verificação de disponibilidade, integridade e efetividade

### 4.1 Disponibilidade e funcionalidade

A expectativa regulatória apresentada é que os operadores garantam a disponibilidade e a funcionalidade dos elementos críticos por meio de **testes e manutenções requeridos**. A continuidade operacional sem testes que demonstrem disponibilidade e confiabilidade é tratada nas fontes como desvio relevante.

As fontes também citam indisponibilidades típicas que precisam de controle formal:
- **by-pass**;
- **override**;
- **inibição**;
- falha na execução de **testes** ou **verificações**;
- indisponibilidade temporária do equipamento ou função.

### 4.2 Integridade da barreira e controles de fatores de degradação

Um dos estudos descreve a avaliação da integridade das barreiras por meio de **controles de fatores de degradação** vinculados a disciplinas de operação, manutenção, inspeção e segurança. Exemplos citados:

- **Operação (OP):** atualização de documentação técnica, treinamento das equipes, desvios de classificação de área, gestão de mudanças, testes funcionais, condição operacional e modo de operação.
- **Manutenção/Inspeção (MAN/INSP):** plano de manutenção, plano de inspeção, calibração, relatórios de tratamento de integridade.
- **Segurança (SEG):** controle de pendências de auditorias, realização de simulados, treinamento das equipes de emergência.

A classificação da integridade da barreira, segundo esse modelo, pode resultar em quatro estados:
- **íntegra**;
- **em degradação**;
- **degradada**;
- **contingenciada**.

Os trechos não fornecem os limiares numéricos da equação de integridade, mas a lógica é clara: a integridade não depende apenas do equipamento existir; depende de gestão ativa dos mecanismos que levam à perda de desempenho.

### 4.3 Efetividade da barreira

As fontes tratam a **efetividade** como ligada à capacidade de a barreira cumprir sua função sob determinadas condições técnicas, operacionais e ambientais, com a **confiabilidade** e o **tempo de resposta** requeridos. Em uma metodologia específica, barreiras que não dependem de ação humana e têm resposta rápida foram consideradas de efetividade mais alta; já alarmes com intervenção humana foram avaliados como menos eficazes, e evacuação/resgate como eficácia intermediária por dependerem de ação humana organizada.

Isso leva a um ponto decisivo para FPSO/FSO: ao avaliar uma compensação, não basta perguntar se existe uma barreira; é preciso perguntar **quão autônoma, rápida, confiável e robusta** ela é nas condições reais da operação.

### 4.4 Indicadores e monitoramento

As fontes mencionam o uso de **indicadores proativos e reativos** para medir a frequência de falhas das barreiras e identificar oportunidades de melhoria. Em termos operacionais, isso significa monitorar não apenas acidentes, mas também:
- falhas de teste;
- alarmes inibidos;
- pendências de manutenção de SCE;
- desvios de inspeção;
- indisponibilidade temporária de sistemas críticos;
- falhas recorrentes de execução de procedimentos críticos.

**Fontes:** `petroles-004c2afadba7ea17c7dd7908:pNone:466574.0-466603.0`, `petroles-4ee4bce16acf674505c8912d:pNone:2091004.0-2091038.0`, `anp-21b016bb482410ebc1a9261e:p7-8:159.0-109.0`, `regis-962e222ee3c37dec82110fd6:pNone:3221.0-3557.0`

## 5. Critérios para contingenciamento de elemento crítico degradado

Quando um elemento crítico falha, degrada ou fica indisponível, as fontes convergem em quatro exigências práticas.

### 5.1 A contingência deve existir antes da necessidade

A ANP espera que o operador possua **procedimento prévio** com diretrizes para contingenciamento robusto e adequado de elementos críticos degradados ou fora de serviço. Isso inclui indisponibilidades por by-pass, override, inibição e falha de testes/verificações.

### 5.2 A contingência deve manter o risco aceitável

As contingências propostas devem ser suficientes para manter os riscos em **níveis aceitáveis**, podendo exigir:
- parada de equipamentos;
- parada de sistemas;
- até **parada da planta de processo**.

Logo, contingenciar não significa automaticamente “seguir operando”; significa demonstrar que a combinação de medidas remanescentes e compensatórias ainda controla o risco.

### 5.3 APR/HAZID isolada pode ser insuficiente

A nota técnica alerta que análises preliminares de risco usadas de forma desordenada tendem a ser **insuficientes** para contingenciar degradações relevantes de elementos críticos. O ponto técnico é importante: uma APR pode apoiar entendimento inicial do risco, mas não substitui, por si só, a demonstração de que a barreira compensatória é confiável, disponível e executável no tempo requerido.

### 5.4 Barreiras procedimentais só valem se tratadas com rigor equivalente

Se a contingência recorrer a **ação humana** como barreira procedimental, o procedimento deve ser formalizado e tratado como procedimento crítico específico. As fontes exigem, minimamente:
- evidências de **treinamento prático** dos envolvidos;
- verificação da **quantidade mínima de mão de obra** necessária por **análise temporal**;
- avaliação das **interfaces homem-máquina** quanto à integridade, comissionamento e adequação ao uso;
- uso de ferramentas adequadas, como **Análise de Confiabilidade Humana**.

Em linguagem prática: uma ação manual improvisada não é barreira válida só porque alguém acredita que “daria para fazer”.

### 5.5 Autoridade técnica e gestão de mudanças

Um dos trechos, ao descrever prática corporativa, informa que quando um SCE fica fora dos parâmetros de desempenho, a continuidade operacional somente ocorre com avaliação de um **expert/autoridade técnica**, responsável por definir medidas mitigadoras até o restabelecimento do padrão de desempenho, com registro em **gestão de mudanças**; em alguns casos, atividades são suspensas. Embora seja exemplo de prática empresarial e não regra universal, o princípio é consistente com boa governança de barreiras: degradação de elemento crítico requer **decisão formal, rastreável e tecnicamente competente**.

**Fontes:** `anp-21b016bb482410ebc1a9261e:p7-8:159.0-109.0`, `petroles-4ee4bce16acf674505c8912d:pNone:2091004.0-2091038.0`

## 6. Modos típicos de degradação e falha de barreiras

As fontes fornecem vários mecanismos práticos pelos quais barreiras deixam de ser confiáveis. Eles são úteis para auditoria, preparação de APR/AST, revisão de PT e decisão de contingência.

### 6.1 Falhas técnico-operacionais

Exemplos citados:
- resposta inadequada à emergência, com falha de ativação manual e automática de **ESD**;
- sistema de **detecção de fogo e gás** com não conformidades de manutenção;
- **alocação inadequada** de detectores de fogo e gás;
- uso de **equipamento inadequado em área classificada**;
- planos de manutenção de equipamentos **ATEX/Ex vencidos**;
- ausência de verificação sistemática de posicionamento de detectores;
- falta de revisão de segurança **pré-partida** para retomadas e partidas.

### 6.2 Falhas de tarefa e de planejamento

Os estudos de caso relatam desvios como:
- **purga incompleta**;
- **despressurização insuficiente** antes de abertura de linha;
- abertura antecipada de sistema contendo inflamável;
- ausência de medição de gás ou falta de monitoramento contínuo com detector;
- detector multigás alarmando e sendo **desligado**;
- ferramenta com potencial de ignição usada sem clareza sobre adequação ao ambiente explosivo;
- falta de discussão prévia entre operação e empreendimento sobre como executar o trabalho real.

Esses exemplos mostram que uma barreira pode falhar por perda de integridade técnica, mas também por **sequenciamento inadequado de atividades** e por decisões de campo que reduzem margens de segurança.

### 6.3 Fatores humanos e organizacionais

As fontes são claras ao associar degradação de barreiras a fatores como:
- confiança excessiva em lideranças experientes substituindo análise técnica do risco;
- terceirização com **baixo treinamento** e alta rotatividade;
- treinamento excessivamente teórico, pouco aderente às variabilidades do trabalho real;
- ausência de qualificação específica para inflamáveis e áreas classificadas;
- pressão de prazo e produção para **“pular etapas”**;
- normalização de desvios porque liberações anteriores deram certo;
- comunicação insuficiente entre contratante, contratadas e equipes de liberação;
- autonomia limitada de contratados para interromper atividade insegura.

Do ponto de vista de barreiras, isso significa que a degradação de um elemento crítico raramente é puramente mecânica; muitas vezes ela vem acompanhada de enfraquecimento de treinamento, supervisão, disciplina operacional e capacidade de resposta humana.

**Fontes:** `anp-ac72dc113a17b403b32f806c:p2-3:19.0-25.0`, `petroles-4ee4bce16acf674505c8912d:pNone:1954078.0-1954117.0`, `petroles-4ee4bce16acf674505c8912d:pNone:1954138.0-1954184.0`, `petroles-4ee4bce16acf674505c8912d:pNone:1954164.0-1954206.0`

## 7. Barreiras mitigadoras: o que verificar quando a prevenção falha

Quando o evento topo já ocorreu ou está em curso, o foco passa da prevenção para a mitigação. As fontes permitem organizar essa verificação em quatro blocos.

### 7.1 Proteção pós-liberação

Inclui sistemas e recursos que reduzem a severidade da liberação e da ignição, como proteção ativa contra fogo, dispersão/queima de gases e posicionamento adequado de detecção. Um caso citado mostra que uma **neblina d'água** com mangueiras contra incêndio estava prevista na análise de risco para controlar possível vazamento de gás, mas não foi implementada na execução.

### 7.2 Resposta de emergência da planta/instalação

Deve existir equipe treinada, simulados, brigada preparada e recursos operacionais efetivamente disponíveis. As fontes destacam a necessidade de treinamento das equipes de emergência e de rotinas de inspeção/posicionamento de detectores. A resposta não pode depender de mobilização desorganizada após o evento.

### 7.3 Evacuação, resgate e abandono

Uma metodologia citada trata evacuação, resgate e abandono como barreira mitigadora específica, com efetividade intermediária por depender de ação humana. O estudo de caso ilustra o problema quando não há **rota de fuga** adequada: trabalhadores precisaram escapar por superfície irregular e salto de altura. Isso evidencia que rota de fuga e ponto de abandono não são detalhes civis; são parte da barreira mitigadora.

### 7.4 Proteção pessoal e atendimento inicial

Embora EPI não substitua prevenção de grandes acidentes, as fontes mostram que sua ausência agrava severidade. Foi citado caso em que apenas empregados próprios usavam roupa especial para contato com chama, enquanto terceiros expostos à mesma tarefa crítica não a utilizavam. Também foi relatada falha no **translado de vítimas**, feito em veículo comum e não em ambulância, apesar da disponibilidade esperada de recursos de emergência.

Em FPSO/FSO, a conclusão prática é direta: após a perda de contenção, a mitigação precisa estar pronta para funcionar sem depender de improviso, e isso inclui proteção ativa, comunicação, abandono, resgate, primeiros socorros e logística médica.

**Fontes:** `petroles-004c2afadba7ea17c7dd7908:pNone:466560.0-466586.0`, `petroles-4ee4bce16acf674505c8912d:pNone:1954164.0-1954206.0`, `anp-ac72dc113a17b403b32f806c:p2-3:19.0-25.0`

## 8. Critérios práticos de avaliação em FPSO/FSO

Com base nos trechos, a avaliação profissional de barreiras e elementos críticos pode ser estruturada nas perguntas técnicas abaixo.

### 8.1 O cenário está bem definido?
- Qual é o **perigo**?
- Qual é o **evento topo**?
- Quais ameaças levam à perda de contenção ou perda de controle?
- Quais consequências relevantes existem para pessoas, meio ambiente, patrimônio e continuidade operacional?

### 8.2 As barreiras são realmente independentes?
- Há falhas de causa comum capazes de derrubar mais de uma barreira?
- Alguma barreira compensatória depende da mesma fonte de energia, mesmo instrumento, mesma lógica ou mesma ação humana da barreira degradada?

### 8.3 Os elementos críticos e procedimentos críticos estão identificados?
- Os componentes essenciais da barreira estão listados?
- Existem **procedimentos críticos** associados que também precisam ser tratados como elementos críticos do controle do risco?
- Há padrão de desempenho esperado para cada elemento?

### 8.4 A integridade foi demonstrada?
- Testes, inspeções, calibrações e manutenção estão em dia?
- Há inibições, bypasses, overrides ou falhas de teste pendentes?
- Os fatores de degradação estão controlados por operação, manutenção, inspeção e segurança?

### 8.5 A contingência é tecnicamente válida?
- Mantém o risco em nível aceitável?
- Está formalizada?
- Se depender de ação humana, há treinamento prático, efetivo de pessoal suficiente, interface homem-máquina adequada e análise de confiabilidade humana?
- Se a compensação não for robusta, a decisão correta pode ser **reduzir escopo, suspender a atividade ou parar o sistema/planta**.

### 8.6 Há sinais de degradação organizacional das barreiras?
- Pressão por prazo ou produção?
- Tolerância a desvios porque “sempre foi assim”?
- Treinamento superficial?
- Falhas de comunicação entre operação, manutenção, contratadas e projeto?
- Falta de autonomia para interromper trabalho inseguro?

### 8.7 A mitigação está pronta para o pior caso plausível?
- Detecção e alarme funcionam?
- Proteção pós-liberação está disponível?
- Rotas de fuga e abandono estão desobstruídas e praticáveis?
- Equipes de resposta e recursos médicos estão posicionados e treinados?

**Fontes:** `petroles-4ee4bce16acf674505c8912d:pNone:2091004.0-2091038.0`, `petroles-004c2afadba7ea17c7dd7908:pNone:466560.0-466586.0`, `petroles-004c2afadba7ea17c7dd7908:pNone:466574.0-466603.0`, `anp-21b016bb482410ebc1a9261e:p7-8:159.0-109.0`, `anp-ac72dc113a17b403b32f806c:p2-3:19.0-25.0`, `petroles-4ee4bce16acf674505c8912d:pNone:1954078.0-1954117.0`, `petroles-4ee4bce16acf674505c8912d:pNone:1954138.0-1954184.0`, `petroles-4ee4bce16acf674505c8912d:pNone:1954164.0-1954206.0`, `regis-962e222ee3c37dec82110fd6:pNone:3221.0-3557.0`

## 9. Síntese final

A mensagem técnica central dos trechos é que **barreira eficaz não é apenas barreira existente**. Para que uma barreira preventiva ou mitigadora seja válida no gerenciamento de risco de um FPSO/FSO, ela precisa:
- ter **função claramente definida** no cenário;
- possuir **elementos críticos identificados**;
- ter **desempenho esperado** conhecido;
- manter **integridade e disponibilidade demonstradas**;
- ser protegida contra **fatores de degradação**;
- ter **compensação formal, robusta e verificável** quando degradada;
- e, se necessário, levar à **restrição operacional ou parada** quando o risco não puder ser mantido em patamar aceitável.

Em termos de disciplina operacional, a decisão madura não é “como seguir operando a qualquer custo”, e sim “sob quais condições a operação ainda permanece segura, e quando deve ser interrompida”.