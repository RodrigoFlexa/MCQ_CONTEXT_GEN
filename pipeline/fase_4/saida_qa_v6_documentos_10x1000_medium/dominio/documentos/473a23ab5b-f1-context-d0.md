# Controle de níveis e pressão em separadores trifásicos

## 1. Papel das malhas de nível e pressão no separador trifásico
O separador trifásico de produção recebe uma corrente multifásica e promove a separação inicial entre gás, óleo e água. Em arranjos típicos citados nas fontes, o vaso possui uma câmara de separação e uma câmara de óleo, com uma entrada e três saídas: gás, óleo e água. As variáveis de controle mais diretamente ligadas ao inventário e à qualidade da separação são:

- **pressão do gás no vaso**;
- **nível da interface água-óleo** na região de acumulação/separação líquida;
- **nível de óleo** na câmara de óleo, ou nível líquido correspondente à fase oleosa acumulada.

Essas malhas não existem apenas para manter indicadores estáveis. Elas definem o inventário do vaso, amortecem perturbações vindas dos poços e condicionam a qualidade das correntes de saída. A separação não é completa; o objetivo prático é manter dentro de limites aceitáveis, entre outros efeitos:

- líquido arrastado no gás;
- água arrastada no óleo, usualmente expressa como **BSW**;
- óleo arrastado na água, usualmente expresso como **TOG**.

Em unidades offshore compactas, a restrição de peso e espaço tende a reduzir a capacidade de absorver oscilações de carga. Isso aumenta a importância do desenho da malha e da filosofia operacional, especialmente quando há aumento de produção de água, uso de gás-lift e ocorrência de golfadas.

**Fontes:** `petroles-004c2afadba7ea17c7dd7908:pNone:215533.0-215571.0`, `petroles-004c2afadba7ea17c7dd7908:pNone:2016490.0-2016516.0`, `regis-cbfdf414fa0dd7c3c5945bb5:pNone:0.0-27.0`

## 2. Estrutura básica das malhas e objetivo operacional
As fontes descrevem uma arquitetura clássica de controle por realimentação, em que a variável de processo medida é comparada ao setpoint e o controlador ajusta uma variável manipulada para reduzir o erro. Em separadores de produção, isso se traduz, de forma simplificada, em:

- **controle de pressão**: manipula a **vazão de saída de gás**;
- **controle da interface água-óleo**: manipula a **vazão de saída de água produzida**;
- **controle do nível de óleo**: manipula a **vazão de saída de óleo**.

A função do controle automático é simultaneamente:

- adaptar o processo a perturbações externas;
- respeitar restrições dos equipamentos;
- elevar a estabilidade operacional;
- apoiar atendimento às especificações do produto;
- reduzir risco operacional e impacto ambiental.

Na prática offshore, essas malhas são muito exigidas porque a vazão de chegada ao separador é a soma dos poços alinhados ao header de produção e pode variar fortemente por causa de golfadas, mudanças de choke, composição do fluido, gás-lift e condições de escoamento do sistema poço-linha-planta.

**Fontes:** `petroles-004c2afadba7ea17c7dd7908:pNone:215533.0-215571.0`, `petroles-004c2afadba7ea17c7dd7908:pNone:2016490.0-2016516.0`

## 3. Controle de pressão do separador
### 3.1 Objetivo do controle de pressão
Um dos objetivos do processo de separação é maximizar a recuperação de hidrocarbonetos líquidos. As fontes citam a ideia de uma **pressão ótima de separação**, oriunda de considerações termodinâmicas, na qual a produção de líquido é maximizada. Também indicam que o aumento do número de estágios pode elevar a recuperação de líquido, embora isso traga penalidades de custo, peso e espaço. Portanto, a pressão do vaso não é apenas uma variável de segurança; ela também afeta desempenho de separação e integração com o restante da planta.

### 3.2 Variável manipulada e lógica de ação
Na configuração clássica, a malha de pressão atua sobre a **válvula da linha de gás** na saída do separador em direção ao sistema de compressão. Se a pressão medida subir acima do valor desejado, a válvula abre mais e descarrega mais gás; se a pressão cair, a válvula fecha. Em um exemplo de separador de teste, a válvula de controle de gás é descrita como **normalmente aberta ou fail safe open**, de modo que a perda do suprimento pneumático não leve à sobrepressurização do vaso.

### 3.3 Integração com o sistema de compressão
As fontes mostram que, em arquiteturas mais modernas, o controle de pressão do separador pode deixar de ser uma malha PIC simples e passar a fazer parte de uma **estrutura multivariável** associada ao compressor. Nesse caso, a válvula de gás do separador é manipulada junto com outras variáveis relevantes da máquina, tais como:

- pressão de sucção;
- pressão de descarga de estágios;
- fluxo de ar da turbina;
- fluxo de gás combustível;
- fluxo de gás comprimido.

A prioridade operacional descrita é evitar **surge** em compressor centrífugo, entendido nas fontes como regime de escoamento instável, podendo chegar a reversão de fluxo, associado ao aumento da relação entre pressão de descarga e pressão de sucção em condição de vazão reduzida. Nessa filosofia, a pressão do separador pode variar mais do que em uma malha clássica, porque a proteção e a estabilidade do compressor têm prioridade.

### 3.4 Instrumentação de pressão
As fontes citam como tecnologias usuais:

- sensores mecânicos por deformação elástica;
- sensores elétricos tipo **strain gauge**;
- sensores **piezoelétricos**.

Os sensores eletrônicos são preferidos nas descrições apresentadas por sua precisão e facilidade de integração com sinais padrão. Também é mencionado o uso de **selo de pressão** para proteger o transmissor contra fluidos agressivos, por exemplo presença de H2S, usando um diafragma e um fluido de enchimento para transmitir a pressão ao sensor.

### 3.5 Pontos de atenção operacional
Alguns diagnósticos práticos descritos nas fontes:

- oscilações excessivas de pressão podem refletir sintonia inadequada do controlador, perturbações severas na entrada ou restrições do sistema de gás/compressão;
- ausência de histórico ou da variável manipulada dificulta diagnóstico fino da malha;
- em sistemas acoplados à compressão, avaliar o controle isoladamente pode levar a conclusões erradas, porque a malha de pressão está subordinada a restrições da máquina.

**Fontes:** `petroles-004c2afadba7ea17c7dd7908:pNone:2016518.0-2016553.0`, `regis-864b525b79e3c20e7da3415d:pNone:426.0-463.0`, `petroles-004c2afadba7ea17c7dd7908:pNone:2016635.0-2016662.60`, `petroles-004c2afadba7ea17c7dd7908:pNone:2016703.0-2016737.0`, `petroles-004c2afadba7ea17c7dd7908:pNone:2016683.0-2016720.0`

## 4. Controle da interface água-óleo
### 4.1 Relação entre interface e tempo de residência
As fontes tratam o controle da interface água-óleo como uma das questões mais delicadas da separação gravitacional. O motivo é que o **nível da interface define o tempo de residência efetivo** das fases líquidas dentro do vaso. Esse tempo de residência determina quanto tempo as gotas dispersas têm para migrar para a região de acumulação da sua fase predominante.

Em termos operacionais:

- **aumentar o nível da interface** tende a aumentar o tempo de residência da água, favorecendo menor TOG na água de saída, mas reduz o tempo de residência do óleo e pode elevar o BSW do óleo;
- **reduzir o nível da interface** tende a favorecer a qualidade do óleo na saída do separador, mas pode piorar a qualidade da água produzida.

Portanto, o setpoint da interface é um **compromisso entre BSW do óleo e TOG da água**, além de afetar a carga imposta aos equipamentos a jusante, como hidrociclones, tratadores eletrostáticos e demais etapas de tratamento.

### 4.2 Variável manipulada
A malha de interface atua sobre a **vazão de saída de água produzida**. Uma configuração citada nas fontes posiciona a válvula de controle preferencialmente **a jusante da bateria de hidrociclones**, o que mostra que, em alguns arranjos, a filosofia de controle considera a interação do separador com o sistema de tratamento de água e não apenas o vaso isolado.

### 4.3 Estratégias de controle: PID versus controle por bandas
Modelos dinâmicos e implementações citados nas fontes compararam duas estratégias para o controle da interface:

- **PID convencional**;
- **controle por bandas**.

A filosofia do controle por bandas, segundo a fonte, é **manter a vazão de descarte estável e permitir que o nível flutue dentro da faixa disponível**. Nos casos modelados e relatados, essa estratégia foi considerada mais eficiente na estabilização das vazões e na melhoria da qualidade da água descartada do que o controle PID estrito em torno de um setpoint fixo.

Essa conclusão é coerente com uma limitação prática do ambiente offshore: vasos compactos têm menos capacidade para absorver perturbações, e variações excessivas da válvula de saída de água podem propagar instabilidades para os hidrociclones e o sistema de descarte.

### 4.4 Instrumentação de interface
As fontes citam diferentes tecnologias de medição aplicadas a nível/interface:

- **deslocador/empuxo**;
- **radar**;
- **perfilagem nucleônica por atenuação de raios gama**, capaz de indicar perfil de preenchimento do vaso e identificar gás, espuma, óleo, emulsão, água e areia;
- em aplicações mais simples, **chaves de nível tipo bóia** e observação local por sight glass.

Para controles mais críticos e vasos compactos, a capacidade de identificar não apenas um nível simples, mas também perfis de espuma e emulsão, pode ser operacionalmente relevante.

### 4.5 Critérios práticos de ajuste
As fontes sugerem alguns critérios práticos:

- não buscar necessariamente um nível rigidamente fixo se isso exigir modulação excessiva da válvula;
- usar a capacidade volumétrica do vaso como amortecimento de perturbações, desde que haja margem operacional suficiente;
- validar tempos de ação, retardo instrumental e comunicação, especialmente em transientes e em sistemas compactos.

**Fontes:** `petroles-004c2afadba7ea17c7dd7908:pNone:2016518.0-2016553.0`, `regis-cbfdf414fa0dd7c3c5945bb5:pNone:0.0-27.0`, `regis-c09531a21d9ac256b681a236:pNone:267.0-292.0`, `petroles-004c2afadba7ea17c7dd7908:pNone:2016635.0-2016662.60`, `regis-864b525b79e3c20e7da3415d:pNone:426.0-463.0`

## 5. Controle do nível de óleo e coordenação entre as saídas líquidas
A fase oleosa verte para a câmara de óleo, onde o nível é controlado manipulando-se a vazão de saída de óleo. Essa malha precisa ser coordenada com a malha da interface água-óleo, porque ambas repartem o inventário líquido do vaso e influenciam a separação gás-líquido e líquido-líquido.

Alguns efeitos operacionais descritos nas fontes:

- **nível líquido alto demais** favorece arraste de líquido para a corrente de gás;
- **nível líquido baixo demais** pode indicar ou provocar arraste de gás para as correntes líquidas;
- **setpoint excessivamente alto** reduz a margem de manobra da malha diante de perturbações e pode aproximar o processo de alarmes e intertravamentos;
- **modulação intensa da válvula de óleo** reduz sua vida útil e transfere perturbações para as etapas seguintes, desperdiçando a capacidade amortecedora do separador.

As fontes trazem exemplos de tendência nos quais o nível de óleo era mantido com setpoint alto ou com atividade muito intensa de válvula. O diagnóstico proposto nesses casos foi:

- verificar se a válvula realiza o curso completo;
- investigar deposição de borra, incrustação ou redução de capacidade de vazão;
- revisar sintonia PID excessivamente agressiva;
- questionar se a malha está tentando controlar rigidamente uma variável que poderia oscilar dentro de banda aceitável.

**Fontes:** `petroles-004c2afadba7ea17c7dd7908:pNone:215533.0-215571.0`, `petroles-004c2afadba7ea17c7dd7908:pNone:2016635.0-2016662.60`, `petroles-004c2afadba7ea17c7dd7908:pNone:2016703.0-2016737.0`, `petroles-004c2afadba7ea17c7dd7908:pNone:2016683.0-2016720.0`

## 6. Efeitos de espuma, emulsão, areia, parafina e incrustação sobre as malhas
As malhas de nível e pressão só funcionam bem se a hidrodinâmica do separador e seus internos estiverem saudáveis. As fontes apontam os seguintes mecanismos de degradação operacional:

### 6.1 Espuma
A formação de espuma pode decorrer das características físico-químicas do óleo, impurezas presentes e da queda de pressão na entrada do separador. A espuma ocupa volume útil do vaso, dificulta a leitura e o controle de nível e pode ser arrastada tanto pelo gás quanto pelo óleo desgaseificado.

### 6.2 Emulsão
Emulsões na interface água-óleo reduzem o tempo de retenção efetivo e prejudicam o controle da interface. A presença de uma camada emulsificada torna a posição da interface menos nítida e reduz a eficiência da separação. As fontes mencionam calor e químicos como meios de mitigação, embora frequentemente aplicados em etapas de tratamento posteriores.

### 6.3 Areia e sedimentos
Areia causa erosão em válvulas, obstrução de internos e redução do volume útil do vaso por acúmulo no fundo. Nas fontes aparecem dois efeitos particularmente relevantes para controle:

- erosão de sede e plug das válvulas de nível, tornando a curva de vazão errática;
- obstrução parcial da válvula ou das linhas, levando operadores a recorrer a by-pass manual, o que degrada a ação automática.

### 6.4 Parafina, borra e incrustação
Parafina pode obstruir placas coalescedoras e extratores de névoa. Incrustação salina e borras reduzem a eficiência de trocadores de calor, diminuindo a temperatura de separação e agravando espuma, emulsionamento e viscosidade. Também podem comprometer a capacidade efetiva de vazão das válvulas de controle.

Esses mecanismos são importantes porque uma malha aparentemente mal sintonizada pode, na verdade, estar reagindo a um problema mecânico ou de processo.

**Fontes:** `petroles-004c2afadba7ea17c7dd7908:pNone:215533.0-215571.0`, `petroles-004c2afadba7ea17c7dd7908:pNone:2016490.0-2016516.0`, `petroles-004c2afadba7ea17c7dd7908:pNone:2016683.0-2016720.0`

## 7. Comissionamento, transientes e validação do controle
As fontes ressaltam que a robustez das malhas deve ser verificada não só em regime permanente, mas também em condições transitórias. Em um programa de qualificação citado, foram avaliados, entre outros, os seguintes cenários:

- parada da alimentação;
- bloqueio de saídas;
- variações em degrau na entrada;
- oscilações de vazão, pressão e composição;
- partidas, paradas e flushing.

Os objetivos desse tipo de ensaio são confirmar que:

- a instrumentação e a malha de controle mantêm a interface dentro da faixa requerida;
- a capacidade volumétrica do vaso é suficiente para a filosofia de controle adotada;
- transientes rápidos não induzem mistura excessiva e perda de eficiência;
- tempos de resposta e retardos instrumentais/comunicação são compatíveis com a dinâmica real do processo.

Para o ambiente de produção offshore, essa visão é importante porque a sintonia que parece boa em operação estável pode falhar diante de golfadas ou mudanças bruscas no regime de produção dos poços.

**Fontes:** `regis-c09531a21d9ac256b681a236:pNone:267.0-292.0`, `regis-cbfdf414fa0dd7c3c5945bb5:pNone:0.0-27.0`, `petroles-004c2afadba7ea17c7dd7908:pNone:2016490.0-2016516.0`

## 8. Diagnóstico prático de baixo desempenho das malhas
A partir dos exemplos e conceitos das fontes, alguns sintomas e interpretações úteis são:

- **pressão instável**: pode indicar perturbação severa na alimentação, sintonia inadequada, restrição no sistema de gás ou atuação subordinada às restrições do compressor;
- **interface com oscilação persistente mas baixa amplitude**: requer acompanhamento; dependendo da sintonia, a malha pode passar a amplificar essa oscilação;
- **setpoint de nível muito alto**: aumenta tempo de residência, mas reduz margem de controle para upset e pode aproximar a operação de intertravamentos;
- **válvula muito ativa para manter nível aparentemente normal**: sugere sintonia agressiva, válvula sobredimensionada em ganho, ou degradação mecânica/hidráulica;
- **nível saturado com válvula em manual/by-pass**: indica perda de controle automático e tende a sobrecarregar as etapas de tratamento a jusante;
- **presença de by-pass manual parcialmente aberto para compensar válvula degradada**: sintoma de restrição de capacidade, erosão ou obstrução na válvula principal;
- **alto nível com arraste de líquido no gás**: pode resultar de espuma, dano em internos, obstrução da saída líquida, projeto impróprio ou operação acima da capacidade;
- **arraste de gás pelo líquido**: pode indicar nível muito baixo ou falha no sistema de controle de nível.

Uma boa prática extraída das fontes é não separar diagnóstico de controle de diagnóstico mecânico. Antes de retunear agressivamente uma malha, deve-se verificar condição de válvula, internas, incrustação, areia, capacidade disponível e coerência do setpoint com os objetivos de qualidade do óleo e da água.

**Fontes:** `petroles-004c2afadba7ea17c7dd7908:pNone:215533.0-215571.0`, `petroles-004c2afadba7ea17c7dd7908:pNone:2016635.0-2016662.60`, `petroles-004c2afadba7ea17c7dd7908:pNone:2016683.0-2016720.0`, `petroles-004c2afadba7ea17c7dd7908:pNone:2016703.0-2016737.0`

## 9. Implicações para segurança de processo e operação integrada
As fontes tratam a instrumentação do separador como o primeiro meio para garantir operação eficiente e segura do equipamento. No recorte disponível, as contribuições mais claras para segurança de processo são:

- manutenção do inventário e da pressão dentro de faixas operáveis;
- escolha de posição de falha adequada da válvula de gás, com exemplo de fail safe open;
- preservação de margem operacional para evitar chegada a alarmes e intertravamentos por setpoints excessivamente altos;
- redução de perturbações impostas ao sistema de compressão e ao tratamento de água/óleo a jusante.

Entretanto, os detalhes de PSV, setpoints de alívio, lógica completa de shutdown e camadas independentes de proteção não estão explicitados no material fornecido. Assim, o controle regulatório aqui descrito deve ser entendido como complementar, e não substituto, das proteções dedicadas do vaso e da planta.

**Fontes:** `petroles-004c2afadba7ea17c7dd7908:pNone:2016490.0-2016516.0`, `regis-864b525b79e3c20e7da3415d:pNone:426.0-463.0`, `petroles-004c2afadba7ea17c7dd7908:pNone:2016635.0-2016662.60`

## 10. Síntese operacional
Para operar bem um separador trifásico offshore, o controle de níveis e pressão deve ser visto como um problema integrado de **inventário, qualidade de separação e estabilidade da planta**. Em termos práticos, a síntese das fontes aponta que:

1. a **pressão** deve ser mantida em faixa que preserve a separação e respeite as restrições da compressão;
2. a **interface água-óleo** deve ser ajustada como compromisso entre **TOG na água** e **BSW no óleo**;
3. o **nível de óleo** não deve consumir desnecessariamente a margem operacional do vaso;
4. o melhor controle nem sempre é o que mantém o nível mais fixo, mas o que produz **saídas mais estáveis** e menor perturbação a jusante;
5. problemas de válvula, areia, incrustação, espuma e emulsão podem se manifestar primeiro como aparente problema de controle;
6. a validação da filosofia de controle em transientes e golfadas é parte do desempenho real do sistema, não um detalhe de laboratório.

**Fontes:** `petroles-004c2afadba7ea17c7dd7908:pNone:2016518.0-2016553.0`, `petroles-004c2afadba7ea17c7dd7908:pNone:215533.0-215571.0`, `regis-cbfdf414fa0dd7c3c5945bb5:pNone:0.0-27.0`, `regis-c09531a21d9ac256b681a236:pNone:267.0-292.0`, `petroles-004c2afadba7ea17c7dd7908:pNone:2016703.0-2016737.0`