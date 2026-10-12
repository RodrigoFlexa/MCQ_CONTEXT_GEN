# Monitoramento de posição

## 1. Aplicabilidade e limite do material disponível *(Fontes: `petroles-004c2afadba7ea17c7dd7908:pNone:1917328.0-1917363.0`, `petroles-004c2afadba7ea17c7dd7908:pNone:1317003.0-1317042.0`)*

Os trechos fornecidos tratam predominantemente de **sondas com posicionamento dinâmico (DP)** e de operações com **riser/BOP**, não de FPSOs/FSOs permanentemente ancorados. Ainda assim, parte importante do conteúdo é aproveitável para a faceta **monitoramento de posição**, porque a lógica de detecção de perda de capacidade de *station keeping* é comum a várias unidades flutuantes:

- existe uma **posição-alvo** ou uma **região admissível** em torno dela;
- a posição medida é comparada continuamente com o alvo;
- além da posição, é necessário monitorar **aproamento**, **movimentos do casco**, **forças ambientais**, **qualidade dos sistemas de referência** e **perda de redundância**;
- a resposta operacional depende de **limites pré-definidos**, **alarmes** e **evolução temporal das variáveis**.

Nos trechos de DP, a correção do desvio é feita por controladores e *thrusters*. Em um FPSO/FSO ancorado, a restauração de posição decorre principalmente do **sistema de ancoragem** e, quando aplicável, de recursos auxiliares de propulsão/assistência. Portanto, o valor transferível aqui está menos no mecanismo de correção e mais na **arquitetura de monitoramento**, nos **critérios de alarme** e no **uso de tendências para reconhecer degradação antes da perda efetiva de posição**.

## 2. Grandezas fundamentais para detectar perda de capacidade de manutenção de posição *(Fontes: `petroles-004c2afadba7ea17c7dd7908:pNone:1917328.0-1917363.0`, `petroles-004c2afadba7ea17c7dd7908:pNone:1917386.0-1917418.0`, `petroles-4ee4bce16acf674505c8912d:pNone:1995038.0-1995093.0`)*

### 2.1 Posição e offset
A variável principal é a **posição corrente** da unidade em relação a uma **posição pré-fixada** ou a um **referencial fixo**. O desvio entre posição medida e posição desejada constitui o **offset**. Nos trechos, o sistema de controle compara continuamente a posição atual com a posição-alvo e avalia se a unidade permanece dentro de um **raio de tolerância**.

Para fins de monitoramento, o offset não deve ser tratado apenas como um valor instantâneo. A detecção de perda de capacidade de *station keeping* exige observar:

- **magnitude do offset**;
- **direção do offset** em relação a vento, corrente, ondas, obstáculos e ativos conectados;
- **taxa de crescimento do offset**;
- **persistência de viés** para um lado, mesmo antes de atingir o limite.

Em linguagem prática, uma unidade pode ainda estar “dentro do círculo” e, mesmo assim, já apresentar sinais de incapacidade crescente de se manter posicionada.

### 2.2 Aproamento (*heading*)
Os trechos destacam que, além da posição, pode ser necessário manter **aproamento fixo**. O *heading* é variável crítica porque altera:

- a decomposição das cargas ambientais sobre o casco;
- a transformação de coordenadas dos sistemas de referência;
- a relação entre posição do casco, pontos de conexão e envoltórias operacionais.

Oscilações excessivas de *heading*, perda de controle direcional ou divergência entre sensores de aproamento são indícios relevantes de degradação da capacidade de manutenção de posição.

### 2.3 Movimentos do casco
Os sensores de movimento fornecem **roll**, **pitch** e **heave**. Nos trechos, essas medições não são o alvo principal do controle DP, mas são essenciais para **corrigir** os sistemas de referência de posição, principalmente DGPS e acústico. Logo, para monitoramento confiável da posição, não basta medir X-Y; também é necessário medir e compensar os movimentos que contaminam a estimativa de posição.

### 2.4 Forças ambientais e sua evolução
As forças ambientais citadas são **vento**, **ondas** e **correnteza**. O material destaca os graus de liberdade horizontais mais diretamente associados à manutenção de posição: **surge**, **sway** e **yaw**. Na prática operacional, a perda de capacidade de *station keeping* costuma ser precedida por uma combinação entre:

- aumento de intensidade ambiental;
- mudança de direção das ações ambientais;
- resposta menos eficiente da unidade para contrariar a resultante dessas forças.

Assim, o monitoramento de posição precisa ser integrado ao acompanhamento meteoceanográfico, especialmente quando a unidade se aproxima de limites operacionais.

## 3. Sistemas de medição e referência aplicáveis ao monitoramento de posição *(Fontes: `petroles-004c2afadba7ea17c7dd7908:pNone:1917365.0-1917400.0`, `petroles-004c2afadba7ea17c7dd7908:pNone:1917386.0-1917418.0`, `petroles-4ee4bce16acf674505c8912d:pNone:1995038.0-1995093.0`)*

### 3.1 DGPS
O **DGPS** é apresentado como evolução do GPS, com correção diferencial para reduzir erros de posição. O material ressalta alguns pontos técnicos importantes para fins de monitoramento:

- o posicionamento resulta da triangulação com satélites;
- a qualidade melhora com maior disponibilidade/qualidade do sinal;
- o sinal precisa ser corrigido para efeitos de movimentação da unidade por informações de **giroscópios** e **VRU**;
- o sistema pode sofrer degradação por efeitos atmosféricos, em especial **cintilação ionosférica**.

Portanto, não basta “ter DGPS disponível”; é necessário monitorar sua **qualidade**, **estabilidade** e **confiabilidade temporal**.

### 3.2 Referência hidroacústica
O sistema **hidroacústico** é descrito como referência baseada em *beacons/transponders* no fundo e receptores/transdutores no casco. Seu desempenho depende do arranjo adotado, como **LBL**, **SBL** e **SSBL/USBL**.

Aspectos relevantes para monitoramento:

- alta robustez relativa, especialmente em águas profundas;
- necessidade de correção por **roll** e **pitch** com dados da VRU;
- suscetibilidade a perdas de sinal por fenômenos de propagação acústica, que tendem a se intensificar com o aumento da lâmina d’água;
- possibilidade de interferência acústica em áreas congestionadas.

Em um sistema de monitoramento de posição, a referência hidroacústica é valiosa porque fornece um **modo físico diferente** do DGPS, reduzindo vulnerabilidade a falhas comuns.

### 3.3 Radioposicionamento
Os trechos citam sistemas de **radioposicionamento** por micro-ondas entre estações fixas e receptores móveis, com uso prático em operações de proximidade. Para a faceta de monitoramento, o ponto principal é que esse recurso pode servir como **fonte adicional e independente** de referência, útil onde haja necessidade de ajuste fino ou diversificação de princípios de medição.

### 3.4 Sensores auxiliares essenciais
Os sensores auxiliares destacados são:

- **Giroscópios/Gyrocompass**: medem aproamento e são vitais para transformação de coordenadas e correção de referências.
- **VRU (Vertical Reference Unit)**: mede **roll**, **pitch** e **heave**, permitindo compensar os efeitos do movimento da unidade sobre os sistemas de posicionamento.
- **Anemômetros**: medem direção e velocidade do vento, variável ambiental de variação rápida e relevante para antecipar degradação da manutenção de posição.

Esses sensores não substituem a medição de posição, mas sem eles a avaliação da posição tende a ficar menos confiável ou menos interpretável.

### 3.5 Indicadores indiretos de degradação geométrica
Nos trechos de perfuração aparecem os sistemas **ERA** e **ARA**, que medem ângulo do riser ou da conexão inferior. Eles são específicos do contexto de sonda/riser, mas ilustram um princípio transferível: a perda de capacidade de *station keeping* pode ser percebida também por **variáveis acopladas**, não apenas pela posição do casco. Em FPSOs, a ideia equivalente é monitorar grandezas acopladas às interfaces críticas da unidade, desde que o sistema aplicável exista e esteja devidamente validado para aquela instalação.

## 4. Qualidade do dado e redundância: o monitoramento não é só medir, é saber se a medição continua confiável *(Fontes: `petroles-004c2afadba7ea17c7dd7908:pNone:1917365.0-1917400.0`, `petroles-004c2afadba7ea17c7dd7908:pNone:1917419.0-1917452.0`, `petroles-004c2afadba7ea17c7dd7908:pNone:1317003.0-1317042.0`, `petroles-4ee4bce16acf674505c8912d:pNone:1995038.0-1995093.0`)*

O material enfatiza que a avaliação de posição não depende de uma única leitura, mas de um **conjunto redundante de sensores, referências e alimentação elétrica**.

### 4.1 Combinação e validação de referências
Um dos trechos descreve o uso de filtragem que pondera diferentes sistemas de referência conforme:

- **qualidade**;
- **precisão**;
- **estabilidade**;
- **repetibilidade**;
- **variância dos dados**.

Esse conceito é particularmente importante para detecção de degradação: quando um sistema começa a divergir, oscilar ou apresentar aumento de variância, ele pode deixar de ser confiável antes mesmo de “falhar” completamente.

### 4.2 Redundância e modos de falha distintos
Os trechos de DP mencionam, para operações críticas, a necessidade de múltiplos sistemas de referência trabalhando continuamente e baseados em **princípios físicos distintos**, justamente para evitar falha simultânea por causa comum. Embora a formulação venha de contexto DP, o princípio é diretamente útil para monitoramento de posição em geral:

- referência única aumenta o risco de erro não detectado;
- referências de mesma natureza podem degradar pelo mesmo mecanismo;
- perda de uma referência pode não causar perda imediata de posição, mas já representa **perda de margem**.

### 4.3 Alimentação elétrica, comunicação e consoles
Os trechos também mostram que falhas em **UPS**, **rede de comunicação**, **controladores** ou **estações de operação** podem degradar o monitoramento, ainda que a unidade não tenha perdido posição naquele instante. Isso é crucial: a perda de capacidade de *station keeping* pode ser detectada não apenas por excursão do casco, mas também por **perda de confiabilidade do sistema que a vigia**.

Exemplos de sintomas precursores mencionados no material:

- perda de uma UPS e, com isso, da redundância do sistema;
- falha de uma rede redundante, com alarme de perda de redundância;
- retirada automática de um controlador em falha;
- perda de alimentação de sensores ou de referência.

## 5. Limites operacionais e filosofia de alarme *(Fontes: `petroles-004c2afadba7ea17c7dd7908:pNone:1917328.0-1917363.0`, `petroles-004c2afadba7ea17c7dd7908:pNone:1917419.0-1917452.0`, `petroles-004c2afadba7ea17c7dd7908:pNone:1317022.0-1317064.0`, `petroles-004c2afadba7ea17c7dd7908:pNone:3313127.0-3313153.0`)*

### 5.1 Conceito de raio de tolerância
Os trechos definem que tanto unidades com DP quanto unidades com ligação física ao solo marinho operam com um **raio de tolerância do alvo**, que fornece o **offset limite de operação**. Esse limite depende de vários fatores, entre eles:

- operação em curso;
- equipamentos envolvidos;
- obstáculos marinhos ou de superfície;
- lâmina d’água;
- condições oceano-meteorológicas.

Ou seja, o limite de posição não é apenas geométrico; ele é **operacional** e **contextual**.

### 5.2 Estados operacionais como ferramenta de decisão
O material descreve uma hierarquia de estados operacionais útil para a lógica de monitoramento:

- **Estado normal**: não há indicativos de anormalidade e as redundâncias mínimas estão preservadas.
- **Estado degradado**: há perda de redundância mínima ou aproximação/ultrapassagem de limites ambientais do estado normal; requer análise da criticidade da operação.
- **Alarme amarelo**: perda de redundância abaixo do mínimo requerido, ou condições ambientais/offset já fora da faixa segura; operações devem ser interrompidas e a equipe deve preparar contingências.
- **Alarme vermelho**: perda de capacidade operacional ou extrapolação de limites máximos seguros; a perda de posicionamento é iminente.
- **Alarme vermelho direto**: evento catastrófico ou degradação súbita que exige resposta imediata, mesmo sem trajetória gradual pelos estados anteriores.

Esse arranjo mostra que o sistema de monitoramento não deve disparar alarmes somente por **offset absoluto**. Ele também deve reagir a **perda de redundância**, **falhas catastróficas** e **degradação funcional**.

### 5.3 Um ponto importante: o alarme pode vir antes da excursão
Os trechos são explícitos ao dizer que, dependendo da gravidade, um alarme pode ser acionado **mesmo sem perda de posição**. Isso é central para a faceta “medição, limites e tendências”:

- falha simultânea de meios de atuação ou controle pode reduzir drasticamente a capacidade de resistir ao próximo aumento ambiental;
- perda de referência ou de energia pode não mover imediatamente a unidade, mas reduz a capacidade de detectar ou corrigir desvios;
- logo, monitoramento efetivo é **preventivo**, não apenas reativo.

## 6. Tendências operacionais que ajudam a detectar perda de station keeping antes do limite final *(Fontes: `petroles-004c2afadba7ea17c7dd7908:pNone:1917365.0-1917400.0`, `petroles-004c2afadba7ea17c7dd7908:pNone:1917419.0-1917452.0`, `petroles-004c2afadba7ea17c7dd7908:pNone:3313127.0-3313153.0`, `petroles-4ee4bce16acf674505c8912d:pNone:1995038.0-1995093.0`)*

Com base nos trechos, as tendências mais úteis para reconhecer perda de capacidade de manutenção de posição são as seguintes.

### 6.1 Crescimento persistente do offset
Mesmo dentro do limite, um **offset que cresce continuamente** ou que exige correções cada vez maiores indica redução de margem operacional.

### 6.2 Oscilação anormal ou perda de estabilidade do aproamento
Aumento de oscilação de *heading*, divergência entre giroscópios ou incapacidade de manter o aproamento desejado pode anteceder excursão de posição, especialmente quando as cargas ambientais mudam de direção.

### 6.3 Piora na qualidade estatística das referências
O material menciona ponderação por **variância**, **estabilidade** e **repetibilidade**. Assim, sinais típicos de degradação incluem:

- aumento da dispersão de uma referência;
- divergência entre referências diferentes;
- intermitência ou perda temporária de sinal;
- necessidade frequente de rebaixar a confiança em determinado sensor.

### 6.4 Aproximação simultânea de limites ambientais e funcionais
O risco cresce quando há combinação de:

- aumento de vento/corrente/ondas;
- perda de redundância em sensores, energia ou comunicação;
- piora das variáveis de posição e aproamento.

Nenhuma dessas tendências deve ser lida isoladamente. A interpretação correta é integrada.

### 6.5 Permanecer dentro do offset seguro não basta
Um trecho ressalta que, **mesmo mantendo-se dentro dos limites de offset considerados seguros, outros parâmetros devem ser monitorados** para garantir risco mínimo e esforços aceitáveis nos pontos mais solicitados do sistema conectado. O princípio geral é importante para FPSOs: posição “ainda aceitável” não significa necessariamente **capacidade de station keeping preservada**.

## 7. Uso prático do monitoramento para resposta operacional *(Fontes: `petroles-004c2afadba7ea17c7dd7908:pNone:1317003.0-1317042.0`, `petroles-004c2afadba7ea17c7dd7908:pNone:1317022.0-1317064.0`, `petroles-004c2afadba7ea17c7dd7908:pNone:1917419.0-1917452.0`)*

Os trechos associam diretamente o monitoramento de posição à decisão operacional. Em termos práticos, o sistema de monitoramento deve alimentar pelo menos quatro níveis de ação:

1. **continuidade normal da operação**, quando posição, aproamento, ambiente e redundância estão dentro da condição esperada;
2. **restrição ou revisão da operação**, quando há estado degradado, mesmo sem excursão relevante;
3. **preparação de contingência**, quando surgem condições de alarme amarelo;
4. **resposta imediata de emergência**, quando a perda de posicionamento é iminente ou já existe falha grave incompatível com continuidade segura.

Embora os exemplos dos trechos sejam de desconexão de emergência em sondas, a lição transferível para FPSOs/FSOs é clara: o monitoramento de posição precisa ser estruturado para **reconhecer perda de margem antes da perda de controle**, com critérios objetivos de escalonamento.

## 8. Síntese técnica para a faceta “monitoramento de posição” *(Fontes: combinação dos trechos citados acima)*

Para detectar perda de capacidade de manutenção de posição, o monitoramento eficaz deve combinar:

- **medição contínua de posição e offset** em relação ao alvo;
- **monitoramento de aproamento**;
- **compensação e leitura dos movimentos do casco** por VRU;
- **acompanhamento das condições ambientais**, especialmente vento;
- **uso de múltiplos sistemas de referência**, preferencialmente com princípios físicos distintos;
- **verificação da qualidade dos dados** por estabilidade, repetibilidade e variância;
- **vigilância da redundância** de sensores, comunicação, energia e processamento;
- **definição de limites e estados operacionais** que não dependam somente do offset final;
- **observação de tendências**, e não apenas de cruzamento pontual de limiares.

Em resumo, a perda de *station keeping* raramente aparece como evento totalmente súbito sem sinais prévios. Os sinais precursores mais úteis são a combinação de **offset em crescimento**, **degradação do aproamento**, **piora da qualidade das referências**, **perda de redundância** e **aproximação dos limites ambientais/operacionais**.