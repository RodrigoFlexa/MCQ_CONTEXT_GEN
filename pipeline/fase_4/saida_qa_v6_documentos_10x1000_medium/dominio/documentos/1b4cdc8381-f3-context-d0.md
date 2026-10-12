# Proteção e aterramento: seletividade das proteções e tratamento de faltas elétricas e à terra em sistemas de geração e distribuição de energia

## 1. Finalidade da proteção elétrica e critério de seletividade
**Fontes-base:** `petroles-004c2afadba7ea17c7dd7908:pNone:2134903.0-2134951.0`, `petroles-004c2afadba7ea17c7dd7908:pNone:2423927.0-2423997.0`

A função central do sistema de proteção é **isolar a menor parte possível do sistema elétrico, no menor tempo possível**, quando ocorre uma condição anormal ou intolerável. O objetivo prático é reduzir o choque elétrico e eletromagnético imposto ao restante da rede, limitar danos a pessoas e equipamentos e diminuir o tempo de indisponibilidade.

Um ponto importante é que **proteção não significa prevenção da falta**. Relés, disjuntores e circuitos de disparo **atuam depois** que a falta ou a condição anormal se manifesta com intensidade suficiente para ser detectada. Portanto, a qualidade do esquema de proteção depende de:

- sensibilidade adequada para detectar a falta no trecho sob responsabilidade;
- seletividade para desligar apenas o elemento necessário;
- rapidez compatível com a suportabilidade térmica, dinâmica e dielétrica dos equipamentos;
- confiabilidade do conjunto relé–TC/TP–lógica–bobina de disparo–disjuntor;
- coordenação com a filosofia de continuidade operacional da planta.

Em um FPSO, esse princípio é particularmente crítico porque uma eliminação indevida de cargas ou barramentos pode evoluir de uma falta local para:

- perda de geração ou separação de barramentos;
- subtensão/subfrequência generalizadas;
- atuação em cascata de proteções;
- perda de utilidades e impacto em sistemas de processo, segurança e marítimos.

Assim, a seletividade não é apenas um requisito elétrico: ela também protege a **continuidade operacional** e a **segurança de processo**.

## 2. Arquitetura típica do sistema de proteção
**Fontes-base:** `petroles-004c2afadba7ea17c7dd7908:pNone:2423927.0-2423997.0`, `petroles-004c2afadba7ea17c7dd7908:pNone:4350201.0-4350228.0`

Os relés de proteção que utilizam grandezas elétricas são conectados ao sistema de potência por meio de **transformadores de corrente (TCs)** e, quando necessário, **transformadores de potencial/tensão (TPs/VTs)**. Esses transformadores de instrumentos cumprem duas funções essenciais:

1. **isolação** entre o sistema de potência e os circuitos de proteção/controle;
2. **redução de magnitude** para níveis secundários adequados aos relés.

A cadeia funcional básica é:

1. a falta altera corrente, tensão, frequência ou relações angulares;
2. TCs/TPs reproduzem essas grandezas em nível secundário;
3. o relé processa a condição e fecha sua saída de trip;
4. a bobina de abertura do disjuntor é energizada por um **sistema de corrente contínua**;
5. o disjuntor abre e isola o circuito faltoso.

As fontes destacam que a **alimentação CC da proteção** é parte vital do sistema, pois abastece bobinas de trip, controle, relés, alarmes e iluminação de emergência. Para aplicações offshore, isso reforça a necessidade de inspeção do banco de baterias, carregadores, fusíveis, supervisão de tensão CC e integridade dos circuitos de disparo.

Outro ponto relevante é o uso crescente de **relés digitais multifunção**, incorporando:

- proteção;
- monitoração;
- controle;
- registro de eventos;
- comunicação;
- aquisição de dados para o sistema supervisório.

Na prática, isso melhora a capacidade de análise pós-falha, de ajuste fino da seletividade e de integração com PMS/EMS, automação elétrica e sistemas de alarme.

## 3. Estudos necessários para seletividade e tratamento de faltas
**Fontes-base:** `petroles-004c2afadba7ea17c7dd7908:pNone:2134903.0-2134951.0`, `petroles-004c2afadba7ea17c7dd7908:pNone:2136329.60-2136387.0`, `petroles-004c2afadba7ea17c7dd7908:pNone:2137034.0-2137099.0`, `petroles-004c2afadba7ea17c7dd7908:pNone:4350201.0-4350228.0`

A avaliação de seletividade e de faltas à terra não pode ser feita apenas por regra prática. As fontes convergem para a necessidade de estudos específicos, entre eles:

### 3.1 Estudo de curto-circuito
Baseia o dimensionamento de disjuntores, a verificação de suportabilidade e os ajustes de proteção. Conceitos citados nas fontes:

- uso de **equivalente de Thévenin** para calcular a contribuição de falta vista a partir do ponto de interesse;
- representação de **geradores** por tensão atrás da reatância subtransitória ou transitória, conforme o objetivo do estudo;
- representação de **transformadores** por sua impedância de curto-circuito;
- necessidade de considerar **impedâncias de sequência positiva e zero**;
- consideração da **relação X/R**, importante para assimetria e esforços sobre equipamentos;
- inclusão da contribuição de **motores de indução** e de **geração local** na corrente de falta.

### 3.2 Componentes simétricas e faltas desequilibradas
Quando a falta quebra o equilíbrio trifásico, o circuito equivalente monofásico deixa de ser suficiente. Nesse caso, o método das **componentes simétricas** permite tratar faltas monofásicas, bifásicas e bifásicas-terra por meio das redes de sequência.

Para faltas à terra, a disponibilidade de caminho de **sequência zero** é decisiva para:

- magnitude da corrente de falta;
- sensibilidade do relé de terra;
- escolha entre proteção por corrente residual/neutro e proteção por sobretensão residual.

### 3.3 Estudo de estabilidade transitória
Embora seja usualmente associado à geração, ele também influencia a filosofia de proteção. As fontes indicam que programas de estabilidade devem simular:

- curtos-circuitos trifásicos em pontos críticos;
- tempo de eliminação da falta pela abertura de disjuntores;
- chaveamento de linhas e geradores;
- partida de motores.

Saídas típicas desses estudos incluem:

- ângulo e velocidade dos rotores das máquinas síncronas;
- potência ativa e reativa no sistema;
- tensões nas barras;
- frequência do sistema;
- comportamento dos motores de indução.

Um resultado particularmente importante é o **tempo crítico de abertura**: tempo máximo admissível para que uma falta permaneça no sistema sem que uma máquina síncrona perca estabilidade. Em redes isoladas ou fracamente interligadas, como é comum em unidades offshore, esse tempo crítico é um limitador direto do atraso permissível na proteção de retaguarda.

### 3.4 Estudos de transitórios e qualidade de energia
As fontes apontam que também devem ser analisados:

- operação de disjuntores;
- chaveamento de bancos de capacitores;
- tensão de restabelecimento transitória (TRV);
- inclusão de cargas não lineares, como conversores de frequência;
- níveis de harmônicos de tensão e corrente.

Esses fenômenos podem provocar aquecimento, interferência em controle, falha de capacitores e, em alguns casos, atuação indevida ou não seletiva das proteções.

## 4. Tipos de falta, frequência de ocorrência e severidade
**Fontes-base:** `petroles-004c2afadba7ea17c7dd7908:pNone:2137034.0-2137099.0`, `petroles-004c2afadba7ea17c7dd7908:pNone:2136329.60-2136387.0`

As fontes destacam dois fatos importantes:

- **curtos monofásicos** tendem a ser os mais frequentes;
- **curtos trifásicos** tendem a ser os menos frequentes, porém são usualmente tratados como os mais severos para estudos de estabilidade e dimensionamento crítico.

Isso leva a uma consequência prática de engenharia:

- a coordenação de proteção precisa ser sensível e seletiva para as faltas mais prováveis, sobretudo **faltas à terra** e desequilíbrios;
- ao mesmo tempo, o sistema deve ser verificado contra o cenário mais severo, frequentemente representado pelo **curto trifásico** em pontos críticos.

Portanto, avaliar seletividade em um FPSO exige olhar simultaneamente para:

1. a **frequência de ocorrência** da falta;
2. a **corrente de curto-circuito** disponível naquele barramento;
3. o **efeito sistêmico** da falta sobre geração, tensão e frequência;
4. o **tempo de eliminação** necessário para manter estabilidade e continuidade.

## 5. Seletividade entre dispositivos e coordenação de tempos
**Fontes-base:** `petroles-004c2afadba7ea17c7dd7908:pNone:2134903.0-2134951.0`, `petroles-004c2afadba7ea17c7dd7908:pNone:4350201.0-4350228.0`, `petroles-004c2afadba7ea17c7dd7908:pNone:2429140.0-2429182.0`

A coordenação da proteção seleciona e ajusta, quando aplicável, os dispositivos envolvidos no sistema, como **fusíveis, disjuntores e relés**. O princípio prático é estabelecer uma hierarquia entre proteção principal e proteção de retaguarda.

### 5.1 Critérios de coordenação
Do material fornecido, decorrem os seguintes critérios:

- a unidade temporizada deve ter **sensibilidade suficiente**, considerando contribuições de outras fontes de corrente de falta;
- a proteção deve detectar faltas em toda a extensão do circuito para a qual se exige isolamento do equipamento gerador ou do alimentador;
- quando houver benefício de ajuste, funções **direcionais** podem ser usadas para melhorar seletividade;
- a proteção do sistema da unidade geradora não deve provocar, indevidamente, a abertura de dispositivos externos além do ponto necessário de interligação/isolação.

Em termos funcionais, isso significa coordenar:

- sobrecorrente instantânea para faltas próximas e severas;
- sobrecorrente temporizada para retaguarda e gradiente de seletividade;
- proteção de terra por corrente residual/neutro quando existe caminho de sequência zero;
- proteção de sobretensão residual quando a corrente de terra é limitada ou inexistente pela conexão do sistema.

### 5.2 Situações que degradam a seletividade
As fontes chamam atenção para vários mecanismos que podem causar erro de coordenação ou contagem indevida em esquemas automáticos:

- **contribuição de retorno de motores de indução** durante curto-circuito;
- contribuição de **geração local** para a falta;
- **correntes de partida** de motores durante religamento;
- **corrente de magnetização de transformadores**;
- efeitos das **capacitâncias das linhas/cabos**;
- chaveamento de **bancos de capacitores**.

Em sistemas com muitos motores e geração embarcada, esses efeitos podem fazer com que um dispositivo “a montante” enxergue uma condição mais severa do que a efetivamente existente no trecho faltoso, comprometendo a seletividade.

### 5.3 Cuidado com o uso de fusíveis em circuitos com motores
O material usado menciona que o uso de chaves-fusíveis para determinados alimentadores/transformadores é desaconselhável quando houver risco de **perda de fase**, pois isso pode levar ao bloqueio do rotor de motores de indução. A lição geral aplicável é que, em sistemas com alta participação de motores, a proteção deve evitar criar uma condição de monofasamento não detectada.

## 6. Tratamento de faltas à terra: influência do aterramento e das conexões dos transformadores
**Fontes-base:** `petroles-004c2afadba7ea17c7dd7908:pNone:2429140.0-2429182.0`, `petroles-004c2afadba7ea17c7dd7908:pNone:2136329.60-2136387.0`, `petroles-004c2afadba7ea17c7dd7908:pNone:4350217.0-4350251.0`

O comportamento da falta à terra depende menos da carga e mais de três fatores estruturais:

1. **método de aterramento da fonte**;
2. **capacitâncias do sistema para a terra**;
3. **conexão dos transformadores**, que pode permitir ou bloquear a circulação de sequência zero.

### 6.1 Quando existe caminho de sequência zero
Se a conexão do transformador permite circulação de corrente de sequência zero do lado protegido, a falta à terra pode ser detectada por:

- relé de sobrecorrente de terra ligado ao neutro;
- medição residual nos TCs;
- eventualmente proteção direcional de terra, se isso trouxer vantagem de coordenação;
- suplementação por unidade instantânea de terra para acelerar a eliminação de faltas próximas.

O texto cita como exemplos de conexões que **permitem** tal circulação configurações aterradas em estrela-estrela e certos arranjos com estrela aterrada e delta, nos quais o transformador oferece caminho ou fonte efetiva de sequência zero para determinadas faltas.

### 6.2 Quando a conexão bloqueia corrente de terra
Se o lado do sistema onde se quer detectar a falta estiver **não aterrado do ponto de vista da sequência zero** por causa da conexão do transformador, a instalação pode **não fornecer corrente significativa de falta à terra**. Nessa condição:

- a corrente pode ser baixa demais para uma proteção de sobrecorrente de terra convencional;
- a fase faltosa pode cair para potencial de terra;
- as fases sãs podem elevar sua tensão fase-terra para valores próximos da tensão fase-fase.

A consequência prática é risco de:

- solicitação excessiva de para-raios/supressores;
- estresse dielétrico da isolação de equipamentos;
- dano rápido, se a isolação fase-terra não for compatível com essa elevação.

### 6.3 Proteção por sobretensão residual (deslocamento do neutro)
Nessas situações, a fonte recomenda detectar a condição por:

- relé trifásico de sobretensão; ou
- relé de tensão conectado para medir a **tensão residual** (associada a 3V0).

A conexão típica em delta aberto/broken-delta no circuito de TP mede a soma fasorial das tensões de fase e, em regime equilibrado, o valor residual é próximo de zero. Assim, o surgimento de tensão residual é um indicador forte de falta à terra em sistema sem corrente de terra suficientemente elevada.

A mesma fonte recomenda **eliminação em alta velocidade** quando a instalação não é isolada para suportar elevação fase-terra até próximo da tensão fase-fase. Quando a isolação é compatível, pode-se admitir retardo intencional para aumentar a segurança contra atuações espúrias, desde que isso seja verificado por estudo.

### 6.4 Aterramento por resistência e limitação da corrente de falta
Os exemplos do material também mostram o uso de:

- resistor no neutro do gerador; ou
- transformador de aterramento com resistor;

para **limitar a corrente de falta monofásica**. Essa filosofia reduz danos térmicos e eletrodinâmicos, mas traz implicações importantes:

- a corrente de falta pode ficar relativamente baixa;
- a proteção precisa ser mais sensível;
- as **capacitâncias do sistema para a terra** passam a ter papel relevante na corrente total de falta;
- a integridade do resistor e do circuito de aterramento torna-se crítica para a confiabilidade da proteção.

Em outras palavras, limitar corrente de terra melhora a agressão física da falta, mas aumenta a importância da engenharia de detecção.

## 7. Modelagem elétrica relevante para proteção e aterramento
**Fontes-base:** `petroles-004c2afadba7ea17c7dd7908:pNone:4350217.0-4350251.0`, `petroles-004c2afadba7ea17c7dd7908:pNone:2134903.0-2134951.0`, `petroles-004c2afadba7ea17c7dd7908:pNone:2136329.60-2136387.0`

As fontes destacam parâmetros que influenciam diretamente cálculos de falta e ajustes de proteção:

### 7.1 Geradores
No estudo de curto-circuito, o gerador é representado pela tensão pré-falta atrás da reatância adequada ao intervalo de interesse:

- **subtransitória**, para os primeiros instantes e maiores correntes iniciais;
- **transitória**, quando se busca comportamento em intervalo mais longo.

A potência reativa e a tensão de excitação influenciam o comportamento da barra geradora e, consequentemente, a forma como as proteções de tensão e estabilidade devem ser avaliadas.

### 7.2 Linhas e cabos
A impedância de sequência zero depende de fatores como:

- geometria do circuito;
- espaçamento entre condutores;
- altura ou arranjo físico em relação ao meio de retorno;
- frequência;
- resistividade do meio de retorno.

Para faltas à terra, isso é decisivo porque a sequência zero governa a corrente residual e a sensibilidade da proteção.

### 7.3 Transformadores
A conexão dos enrolamentos define o caminho de sequência zero e, portanto, a forma de detecção da falta à terra. Além disso, em transformadores menores, a resistência pode ser mais significativa em relação à reatância, tornando a relação **X/R** relevante para a assimetria da corrente e para a capacidade de interrupção.

### 7.4 Contribuições de outras fontes
O uso da superposição e do equivalente de Thévenin é especialmente útil para separar a contribuição de:

- geradores locais;
- motores de indução;
- alimentações externas/interligadas.

Isso é importante para verificar se um relé temporizado manterá sensibilidade adequada nas condições de geração mínima, máxima, barramento seccionado ou operação degradada.

## 8. Relação entre proteção, estabilidade e descarte de cargas
**Fontes-base:** `petroles-004c2afadba7ea17c7dd7908:pNone:2137034.0-2137099.0`

Faltas mal coordenadas não afetam apenas o trecho defeituoso; elas podem alterar o equilíbrio entre geração e carga. As fontes citam situações relevantes:

- grande aumento súbito de carga sobre gerador local;
- perda brusca de carga;
- perda de gerador;
- separação de sistema interligado;
- necessidade de **descarte de cargas** para manter operação estável e contínua.

Aplicando isso ao contexto de FPSO, a seletividade deve ser avaliada não só pela lógica “quem abre primeiro”, mas também pelo efeito dinâmico da abertura sobre:

- margem de estabilidade dos geradores remanescentes;
- queda de frequência e subtensão;
- acionamento de load shedding;
- possibilidade de manter cargas essenciais energizadas.

Uma proteção excessivamente lenta pode perder estabilidade; uma proteção excessivamente agressiva pode induzir shedding desnecessário ou blackout parcial. O ajuste correto resulta do compromisso entre **rapidez, seletividade e estabilidade global**.

## 9. Transitórios, harmônicos e efeitos sobre a atuação das proteções
**Fontes-base:** `petroles-004c2afadba7ea17c7dd7908:pNone:2134903.0-2134951.0`, `petroles-004c2afadba7ea17c7dd7908:pNone:4350201.0-4350228.0`

As fontes registram que cargas não lineares típicas da indústria do petróleo, como **conversores de frequência**, podem introduzir harmônicos de tensão e corrente com consequências como:

- interferência em sistemas de controle;
- aquecimento de máquinas rotativas;
- falhas de capacitores;
- interferência em sistemas de comunicação.

Do ponto de vista de proteção, isso importa porque:

- altera grandezas medidas por TCs/TPs e relés;
- pode distorcer formas de onda e dificultar medições por valor eficaz/fasorial;
- afeta bancos de capacitores e esquemas de compensação reativa;
- pode induzir operações indevidas em esquemas sensíveis.

Além disso, a operação de disjuntores, o chaveamento de capacitores e a TRV são fenômenos que devem ser analisados por ferramentas de transitórios eletromagnéticos quando a complexidade do sistema justificar.

## 10. Diretrizes práticas de decisão para avaliação de seletividade e faltas à terra
**Fontes-base:** `petroles-004c2afadba7ea17c7dd7908:pNone:2134903.0-2134951.0`, `petroles-004c2afadba7ea17c7dd7908:pNone:2136329.60-2136387.0`, `petroles-004c2afadba7ea17c7dd7908:pNone:2137034.0-2137099.0`, `petroles-004c2afadba7ea17c7dd7908:pNone:2423927.0-2423997.0`, `petroles-004c2afadba7ea17c7dd7908:pNone:2429140.0-2429182.0`, `petroles-004c2afadba7ea17c7dd7908:pNone:4350201.0-4350228.0`

Ao avaliar um esquema de proteção e aterramento em geração/distribuição de energia, é tecnicamente útil seguir a sequência abaixo:

1. **Definir o modo de aterramento e as conexões dos transformadores** para saber se a falta à terra produzirá corrente elevada, corrente limitada ou principalmente deslocamento de tensão.
2. **Calcular as correntes de curto-circuito** para os principais pontos do sistema, incluindo contribuições de geradores e motores.
3. **Verificar a disponibilidade do caminho de sequência zero** em cada cenário operacional.
4. **Escolher a variável de detecção predominante**:
   - corrente de fase, para faltas francas com contribuição robusta;
   - corrente residual/neutro, quando há caminho de terra suficiente;
   - tensão residual, quando a corrente de terra é limitada ou bloqueada.
5. **Coordenar tempos e sensibilidades** entre proteção principal e retaguarda, verificando seletividade para o pior caso de contribuição mínima e máxima.
6. **Checar a dinâmica do sistema**: tempo crítico de abertura, perda de geração, separação de barramentos e necessidade de descarte de cargas.
7. **Avaliar transitórios e religamentos**, especialmente quando houver motores de grande porte, transformadores e bancos de capacitores.
8. **Garantir confiabilidade do circuito de trip em CC**, pois sem ele o relé detecta, mas a falta pode não ser eliminada.
9. **Usar registros de eventos e oscilografias** para revisar ajustes após ocorrências reais ou testes de comissionamento.

## 11. Exemplos de análise de falha e troubleshooting
**Fontes-base:** `petroles-004c2afadba7ea17c7dd7908:pNone:2134903.0-2134951.0`, `petroles-004c2afadba7ea17c7dd7908:pNone:2423927.0-2423997.0`, `petroles-004c2afadba7ea17c7dd7908:pNone:2429140.0-2429182.0`, `petroles-004c2afadba7ea17c7dd7908:pNone:4350201.0-4350228.0`

### 11.1 Relé de terra não detecta a falta
Possíveis causas, com base nos conceitos das fontes:

- conexão do transformador bloqueia sequência zero para o lado monitorado;
- sistema opera com aterramento por alta resistência e o relé de corrente não tem sensibilidade suficiente;
- corrente capacitiva do sistema altera a assinatura da falta;
- TCs/residual mal aplicados ou mal polarizados.

Tratamento técnico:

- revisar a topologia de aterramento e sequência zero;
- verificar se a proteção apropriada deveria ser por **tensão residual** em vez de apenas corrente de terra;
- conferir ajustes, polaridades e integridade do circuito secundário.

### 11.2 Dispositivo a montante atua antes do dispositivo do alimentador
Possíveis causas:

- falta de coordenação temporal;
- contribuição de motores ou geração local elevando a corrente percebida a montante;
- inrush de transformador ou religamento interferindo na lógica;
- ajustes insuficientemente seletivos entre instantâneo e temporizado.

Tratamento técnico:

- recalcular correntes de falta com todas as contribuições relevantes;
- revisar margens de seletividade;
- usar função direcional quando aplicável;
- validar com estudos de transitórios/religamento, se necessário.

### 11.3 Faltas à terra causam sobretensão nas fases sãs
Possíveis causas:

- rede efetivamente não aterrada do ponto de vista da sequência zero;
- proteção baseada apenas em sobrecorrente de terra, sem sensibilidade para o caso.

Tratamento técnico:

- aplicar detecção por sobretensão residual/deslocamento do neutro;
- garantir atuação rápida se a isolação fase-terra não suportar a elevação de tensão.

## 12. Síntese técnica
**Fontes-base:** todos os `used_chunk_ids`

Para a faceta de **proteção e aterramento** em geração e distribuição elétrica, a análise profissional deve partir de uma ideia central: **a seletividade correta depende da interação entre curto-circuito, aterramento, caminho de sequência zero, comportamento dinâmico da geração, contribuição de motores e confiabilidade do circuito de disparo**.

Em particular, o tratamento de faltas à terra exige distinguir claramente três cenários:

- sistema com caminho robusto de sequência zero, em que a proteção por corrente de terra/neutro é naturalmente eficaz;
- sistema com corrente de terra limitada por resistência, em que a sensibilidade precisa ser cuidadosamente verificada;
- sistema em que a conexão do transformador bloqueia a corrente de terra, exigindo proteção por deslocamento de tensão/sobretensão residual.

A coordenação seletiva, por sua vez, só é tecnicamente consistente quando validada por estudos que incluam os casos mais prováveis e os mais severos, além dos cenários operacionais relevantes para a planta.