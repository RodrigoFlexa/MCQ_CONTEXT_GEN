# Falhas na arquitetura de automação

## 1. Visão técnica da arquitetura e dos domínios de falha

Para diagnóstico e correção de falhas em automação de FPSO/FSO, é útil tratar a arquitetura como uma cadeia de camadas, desde a geração do sinal no campo até a supervisão. Nos trechos utilizados, a arquitetura é descrita, de forma genérica, pelas seguintes camadas:

1. instrumento/transmissor;
2. conversão analógico-digital;
3. controle local por CLP/PLC;
4. supervisão local, quando existente, por SDCD/DCS;
5. sistema de comunicação;
6. supervisão central ou SCADA.

Cada salto entre camadas pode introduzir **incerteza, atraso, perda de informação ou falhas de comunicação**. Para manutenção e troubleshooting, isso é importante porque o sintoma visto no supervisório nem sempre nasce no supervisório: ele pode ter origem no transmissor, na alimentação da malha, no cartão de entrada, na CPU, na E/S remota, na rede ou no servidor de supervisão.

Na instrumentação industrial, o sensor ou elemento primário entra em contato direto com a variável medida; o transmissor converte essa grandeza em um sinal transmissível. A transmissão pode ser analógica ou digital. Entre as soluções analógicas, destaca-se a malha de corrente `4-20 mA`, valorizada por robustez, baixo custo relativo e boa imunidade a ruído em ambientes industriais. Entre as soluções digitais, o material destaca o **Modbus**, em variantes seriais e em TCP/IP.

Implicação prática para diagnóstico: a investigação deve começar pela **delimitação do domínio de falha**. Em termos operacionais, convém responder, nesta ordem:

- a variável está errada já no campo ou apenas no sistema de controle?
- o problema afeta um único ponto, um cartão, um rack, uma CPU, uma rede, ou só a camada supervisória?
- a falha é de medição, de conversão, de lógica, de comunicação ou de alimentação?

**Fontes:** `petroles-4ee4bce16acf674505c8912d:pNone:490527.0-490575.0`, `petroles-004c2afadba7ea17c7dd7908:pNone:4159910.0-4159955.0`, `petroles-004c2afadba7ea17c7dd7908:pNone:4159935.0-4159977.0`

## 2. Arquitetura do CLP, E/S e supervisão: onde as falhas aparecem

Um CLP é apresentado nas fontes como um equipamento microprocessado, tipicamente modular, formado por:

- fonte de alimentação;
- CPU;
- memória;
- cartões de entrada e saída;
- módulos de comunicação;
- rack/chassi e backplane.

Em arquiteturas mais extensas, podem existir **racks remotos de E/S**, conectados por adaptadores remotos em cadeia ou por rede. Isso cria domínios claros de falha:

- **falha de fonte do rack**: pode derrubar vários cartões ao mesmo tempo;
- **falha de backplane/rack**: pode afetar um conjunto inteiro de módulos;
- **falha de adaptador remoto ou elo serial de alta velocidade**: pode isolar uma estação remota de E/S;
- **falha de cartão de entrada/saída**: costuma afetar grupos específicos de sinais;
- **falha de CPU ou de sincronismo em arquitetura redundante**: pode afetar a lógica inteira ou a comutação entre controladores.

No nível de supervisão, o SCADA/HMI concentra tags, alarmes, históricos e comandos de operador. Portanto, um sintoma como “valor congelado na tela” não comprova, por si só, defeito do transmissor: também pode ser falha de atualização de tag, perda de comunicação com o CLP ou latência na rede.

**Critério prático de segmentação da falha:**

- se **apenas um instrumento** falha, suspeitar primeiro de sensor/transmissor, malha, canal de entrada ou parametrização do ponto;
- se **vários sinais do mesmo cartão** falham, suspeitar do cartão, alimentação comum ou rack;
- se **vários racks remotos** a jusante perdem comunicação, suspeitar do adaptador remoto ou do elo daisy chain;
- se **o controle local continua, mas o SCADA não atualiza**, suspeitar da camada de comunicação, servidores ou estação de supervisão;
- se **há trips ou perda geral de saídas**, considerar falha de CPU, fonte, backplane ou arquitetura fail-safe.

**Fontes:** `petroles-4ee4bce16acf674505c8912d:pNone:490527.0-490575.0`, `petroles-004c2afadba7ea17c7dd7908:pNone:839932.0-839979.0`, `petroles-004c2afadba7ea17c7dd7908:pNone:4159910.0-4159955.0`

## 3. Falhas de sinal, alimentação e conversão A/D

### 3.1 Assinaturas típicas de falha no sinal de processo

Os trechos usados descrevem quatro padrões úteis de diagnóstico na origem do dado:

- **dado congelado**: o instrumento repete o mesmo valor por várias varreduras;
- **dado fora de faixa**: valor impossível ou incompatível com limites físicos/operacionais;
- **dado fora da incerteza esperada**: erro aleatório maior que o informado pelo fabricante;
- **dado incoerente com a dinâmica do processo**: por exemplo, tendência temporal incompatível com o comportamento esperado.

Essas assinaturas ajudam a distinguir defeito real de processo de problema instrumental. Um valor incoerente não implica, automaticamente, defeito do sensor; ele também pode resultar de erro de conversão, amostragem inadequada, atraso de atualização ou falha de comunicação.

### 3.2 Malha `4-20 mA` e alimentação

Na malha de corrente, o transmissor, a fonte CC e o dispositivo de aquisição ficam em série. A consequência diagnóstica é direta: qualquer interrupção relevante na cadeia elétrica pode impedir a representação correta da variável no cartão analógico. Também é possível que alguns sistemas de aquisição alimentem o transdutor, enquanto outros dependam de fonte externa.

Em manutenção, isso leva a verificações objetivas:

- presença da alimentação da malha;
- continuidade do circuito em série;
- compatibilidade entre o tipo de sinal do transmissor e o tipo configurado no canal de entrada;
- capacidade da fonte da unidade básica ou necessidade de fonte externa adicional;
- coerência entre o sinal medido e o valor bruto lido no cartão.

### 3.3 Conversão analógico-digital

A conversão A/D pode introduzir incerteza adicional e precisa respeitar a limitação temporal do elemento primário. Amostrar muito mais rápido do que a capacidade física do sensor não cria informação nova; apenas multiplica leituras do mesmo conteúdo útil ou de ruído/conversão.

Do ponto de vista de troubleshooting, isso significa que uma anomalia percebida no CLP pode nascer de:

- resolução insuficiente da conversão;
- parametrização errada do canal analógico;
- limitação do tempo de amostragem;
- erro do cartão A/D, e não do transmissor;
- alimentação insuficiente para módulos de expansão.

Um dos trechos traz um exemplo de CLP com módulos analógicos configuráveis por hardware e software, em que o tipo de sinal precisa ser ajustado no módulo e nos registradores do controlador, e em que a impedância de entrada e a disponibilidade de potência da fonte influenciam a medição. Embora o exemplo seja de equipamento específico, ele ilustra uma boa prática geral: **confirmar configuração física e lógica do canal antes de condenar o instrumento de campo**.

### 3.4 Correlação sintoma-causa em sinais analógicos

Exemplos úteis:

- **Uma única variável analógica zerada ou fora de escala**: investigar transmissor, alimentação da malha, abertura da série, defeito de canal ou configuração errada do tipo de entrada.
- **Todas as variáveis de um mesmo módulo analógico falham juntas**: mais provável problema comum de módulo, expansão ou alimentação, e menos provável falha simultânea de vários transmissores.
- **Leitura presente, porém errática ou incompatível com a dinâmica do processo**: verificar se o problema nasce no sensor, no A/D ou na varredura/configuração de aquisição.

**Fontes:** `petroles-004c2afadba7ea17c7dd7908:pNone:4159910.0-4159955.0`, `petroles-4ee4bce16acf674505c8912d:pNone:490527.0-490575.0`, `petroles-4ee4bce16acf674505c8912d:pNone:563858.0-563911.0`

## 4. Falhas em CPU, lógica de controle e tempo de varredura

O CLP opera por ciclo de varredura. Nas fontes, esse ciclo inclui, em essência:

1. leitura das entradas;
2. execução do programa de aplicação;
3. atualização das saídas;
4. funções auxiliares, como comunicação e verificações internas.

Esse comportamento é central para entender sintomas de automação que parecem falhas de hardware, mas podem ser falhas de desempenho temporal.

### 4.1 Efeitos do tempo de varredura

O tempo de varredura depende, entre outros fatores, de:

- velocidade e características do processador;
- tamanho do programa;
- quantidade e tipo de pontos de E/S;
- carga de comunicação;
- janelas reservadas para programação, comunicação com dispositivos inteligentes e verificações internas.

Consequências práticas:

- **entradas muito rápidas** podem não ser percebidas se a duração do evento for menor que o tempo efetivo de resposta do ciclo;
- **comandos e feedbacks podem parecer atrasados** sem existir falha física na rede;
- **timeouts de comunicação** podem resultar de fila ou janela de comunicação do CLP, não apenas de defeito do meio físico;
- **dados “velhos” no supervisório** podem ser reflexo de atraso no scan ou na janela de comunicação.

Os trechos mencionam que, em situações críticas, o PLC pode precisar interromper o ciclo normal para atender eventos prioritários. Também indicam que certos pedidos de comunicação só são processados em uma janela específica da varredura; assim, no pior caso, a comunicação pode aguardar um ciclo inteiro antes de ser tratada.

### 4.2 Diagnósticos internos, watchdog e capacidade do controlador

As fontes associam à CPU funções de verificação de erros por diagnósticos internos e por **watchdog timer**. Isso é relevante para manutenção porque parte das falhas em controladores não se manifesta como queima total do CLP, mas como:

- watchdog acionando por travamento ou sobrecarga;
- perda de sincronismo em arquitetura com backup;
- esgotamento prático de memória/recursos;
- saturação de processamento com reflexo no scan e na comunicação.

### 4.3 Indícios de que a falha está no controlador e não no campo

Há maior probabilidade de domínio do controlador quando se observam, por exemplo:

- múltiplos sinais corretos no campo, porém incorretos na lógica ou na supervisão;
- aumento do tempo de resposta em vários pontos sem causa comum no processo;
- alarmes de diagnóstico interno, watchdog ou estado anormal da CPU;
- falha correlacionada à carga de comunicação ou à troca de programa/configuração.

**Fontes:** `petroles-4ee4bce16acf674505c8912d:pNone:217169.0-217204.0`, `petroles-004c2afadba7ea17c7dd7908:pNone:3795043.0-3795103.0`, `petroles-004c2afadba7ea17c7dd7908:pNone:839932.0-839979.0`

## 5. Falhas em E/S remotas, racks e interfaces de expansão

Em sistemas distribuídos, a separação física entre CPU e cartões de E/S amplia a capacidade da arquitetura, mas cria novos pontos de falha. As fontes citam:

- racks separados com fontes próprias;
- adaptadores de E/S remota ligados em série;
- comunicação serial de alta velocidade para interligação de partes do sistema;
- módulos de expansão para sinais analógicos e digitais.

### 5.1 Padrões de falha típicos

- **perda total de um rack remoto**: suspeitar de fonte do rack, adaptador remoto, cabo de interligação ou falha do rack/backplane;
- **perda somente dos pontos de um cartão**: suspeitar do próprio cartão ou do grupo de terminais/sinal associado;
- **perda de vários racks a jusante em topologia em série**: suspeitar do primeiro adaptador/canal comum afetado;
- **instabilidade após expansão do sistema**: verificar capacidade de alimentação, configuração de quantidade de módulos e endereçamento lógico.

### 5.2 Exemplo de raciocínio diagnóstico

Se oito sinais analógicos de um módulo desaparecem simultaneamente, é tecnicamente mais consistente investigar primeiro:

1. a alimentação do módulo e da expansão;
2. a presença/configuração do módulo no CLP;
3. o rack/backplane;
4. a interface remota, se aplicável;
5. só depois a hipótese improvável de oito falhas independentes de transmissor.

Esse raciocínio reduz trocas desnecessárias e encurta o tempo de restauração.

**Fontes:** `petroles-004c2afadba7ea17c7dd7908:pNone:839932.0-839979.0`, `regis-7364e31ba7e905489a4aa55e:pNone:30.0-76.0`, `petroles-4ee4bce16acf674505c8912d:pNone:563858.0-563911.0`

## 6. Falhas em redes industriais e comunicação

### 6.1 Protocolos e camadas relevantes para o diagnóstico

As fontes destacam que a automação industrial combina meios físicos e lógicos distintos. Exemplos citados:

- serial `RS-232` e `RS-485`;
- Ethernet/TCP-IP;
- Modbus serial e Modbus TCP/IP;
- enlaces por fibra, rádio e outros meios, em arquiteturas distribuídas.

Também é ressaltado que a comunicação entre transmissor analógico e cartão A/D não é um protocolo digital, mas uma convenção elétrica; já acima do CLP há predominância crescente de protocolos digitais, com forte presença de TCP/IP em arquiteturas mais modernas.

No caso do Modbus, a compatibilidade depende de implementação coerente de endereçamento, mapeamento de registradores e função de leitura/escrita. Logo, uma falha de comunicação pode ser elétrica, lógica ou de configuração.

### 6.2 Sintomas típicos de falha de rede/comunicação

- tags intermitentes apenas na supervisão, com controle local preservado;
- múltiplos dispositivos inacessíveis no mesmo segmento;
- leituras ou comandos errados por conflito de endereçamento ou mapeamento incorreto;
- latência elevada sem perda total de comunicação;
- falhas concentradas em equipamentos ligados a um mesmo comutador, porta ou caminho de comunicação.

### 6.3 Comutadores Ethernet, duplex e priorização

Um dos trechos utilizados descreve comportamento de comutadores com filas de prioridade por porta de saída e distingue operação **half-duplex** e **full-duplex**. A consequência prática é que o desempenho da rede não depende apenas de “ter link”, mas também de como a infraestrutura encaminha e arbitra o tráfego:

- em **half-duplex**, transmissão e recepção compartilham o canal e podem limitar o desempenho;
- em **full-duplex**, transmissão e recepção ocorrem simultaneamente, reduzindo colisões nessa arquitetura descrita;
- filas e prioridade podem alterar latência percebida por tráfegos diferentes.

Para troubleshooting, isso significa que “rede com ping” ou “porta ativa” não basta. É preciso considerar se a rede está impondo atraso excessivo ao tráfego de automação, especialmente quando o CLP também só processa pedidos de comunicação em janelas específicas do scan.

### 6.4 Itens mínimos a verificar em falhas de comunicação

- endereçamento configurado dos dispositivos;
- coerência entre protocolo usado no equipamento e no sistema mestre;
- estado do elo físico entre camadas;
- correlação do problema com um segmento de rede, porta, rack remoto ou adaptador;
- efeitos de latência, fila ou janela de comunicação do controlador.

**Fontes:** `petroles-4ee4bce16acf674505c8912d:pNone:490527.0-490575.0`, `petroles-004c2afadba7ea17c7dd7908:pNone:4159935.0-4159977.0`, `petroles-4ee4bce16acf674505c8912d:pNone:563858.0-563911.0`, `petroles-004c2afadba7ea17c7dd7908:pNone:3795043.0-3795103.0`

## 7. Redundância, fail-safe e diferença entre falha crítica e falha espúria

Para sistemas de intertravamento e proteção, as fontes destacam que a arquitetura do CLP influencia não só a disponibilidade, mas também o perfil de risco operacional. São citadas configurações como:

- simplex;
- dual-simplex;
- dual-dual;
- 2-de-3.

### 7.1 Conceito de fail-safe

Um dos trechos adota a hipótese de saídas normalmente energizadas, em que a desenergização provoca o desligamento da planta. Em termos práticos, isso representa uma filosofia **fail-safe**: perda de energia ou de comando tende a levar o sistema para uma condição segura de parada, e não para continuidade cega da operação.

Diagnóstico importante: em arquiteturas desse tipo, um trip pode ter sido causado por **perda de energia, falha de CPU, falha de interface ou falha de módulo**, mesmo sem existir anomalia real de processo.

### 7.2 Falha crítica versus falha espúria

Os materiais distinguem dois efeitos diferentes:

- **falha crítica**: perda da função de proteção ou estado perigoso não detectado;
- **falha espúria**: desligamento indevido da planta.

Essa distinção é essencial para análise de automação em FPSO, porque uma alteração que reduz desligamentos indevidos nem sempre melhora a capacidade de proteção frente a falhas perigosas.

### 7.3 Redundância com CPU ativa e backup

Na configuração dual-simplex descrita, uma CPU fica ativa e outra em backup. Um módulo de backup gerencia a conexão com as E/S e um canal serial de alta velocidade mantém monitoramento e atualização de contexto da unidade reserva. Em caso de falha do sistema primário, entradas e saídas são transferidas ao secundário.

Do ponto de vista de manutenção, isso cria pontos adicionais de verificação:

- status primário/secundário;
- integridade do módulo de backup;
- integridade do canal de sincronismo/monitoramento;
- efeito da comutação sobre as E/S e sobre a continuidade de controle.

### 7.4 Resultado de confiabilidade que não deve ser universalizado

Um estudo citado nas fontes indica que, para as configurações analisadas naquele contexto, a arquitetura dual-simplex **não trouxe vantagem sobre simplex em falha crítica**, embora tenha sido melhor contra desligamentos espúrios; já a configuração `2-de-3` apresentou vantagem significativa no caso estudado. Isso é útil como raciocínio de engenharia: **redundância não pode ser avaliada só pelo número de CPUs**, mas pela arquitetura completa e pelos modos de falha.

O material também registra, em modelagem de Markov, a frequência de desligamentos espúrios em regime estacionário pela relação `θe = λe · P1(est)`, em que `λe` é a taxa de transição para falha espúria a partir do estado bom e `P1(est)` é a probabilidade estacionária do estado normal. Essa relação é conceitualmente útil para análise de confiabilidade, mas depende do modelo adotado.

**Fontes:** `petroles-004c2afadba7ea17c7dd7908:pNone:839932.0-839979.0`, `regis-7364e31ba7e905489a4aa55e:pNone:30.0-76.0`

## 8. Sequência recomendada de diagnóstico e correção

Com base nas relações técnicas descritas nas fontes, uma sequência de diagnóstico coerente para falhas em controladores, E/S, redes, alimentação e comunicação é:

1. **Delimitar o escopo da falha**
   - ponto único, cartão, rack, CPU, rede, ou supervisório.

2. **Comparar o valor em diferentes camadas**
   - indicação de campo ou valor bruto;
   - leitura no cartão/CLP;
   - variável usada na lógica;
   - tag apresentada no SCADA.

3. **Verificar alimentação e infraestrutura comum**
   - fonte da malha analógica;
   - fonte do rack local;
   - fonte do rack remoto;
   - necessidade de fonte externa para expansões.

4. **Confirmar configuração antes de substituir hardware**
   - tipo de sinal do canal;
   - quantidade de módulos configurados;
   - endereços de rede;
   - mapeamento de registradores/variáveis.

5. **Avaliar desempenho temporal do CLP**
   - tempo de varredura;
   - janelas de comunicação;
   - diagnósticos internos e watchdog.

6. **Separar falha de rede de falha de aplicação**
   - rede física/porta/comutador;
   - protocolo e endereçamento;
   - atraso imposto por scan ou fila do controlador.

7. **Em arquiteturas redundantes, verificar o mecanismo de comutação**
   - estado do primário e do secundário;
   - sincronismo;
   - impacto da troca na disponibilidade e em trips espúrios.

### Exemplos sintéticos

- **Exemplo 1:** a válvula continua respondendo ao CLP local, mas o SCADA não atualiza. Tendência diagnóstica: falha acima do controle local, na comunicação ou supervisão, não no elemento final.
- **Exemplo 2:** vários sinais analógicos de um mesmo módulo ficam inválidos ao mesmo tempo. Tendência diagnóstica: alimentação do módulo, expansão ou cartão A/D, antes de suspeitar dos transmissores.
- **Exemplo 3:** ocorre trip sem evidência de desvio de processo, e a arquitetura é fail-safe com saídas energizadas. Tendência diagnóstica: perda de energia, CPU, módulo de backup ou interface de E/S pode ter causado desligamento seguro.

**Fontes:** `petroles-004c2afadba7ea17c7dd7908:pNone:4159910.0-4159955.0`, `petroles-004c2afadba7ea17c7dd7908:pNone:4159935.0-4159977.0`, `petroles-4ee4bce16acf674505c8912d:pNone:217169.0-217204.0`, `petroles-004c2afadba7ea17c7dd7908:pNone:839932.0-839979.0`, `petroles-4ee4bce16acf674505c8912d:pNone:563858.0-563911.0`, `regis-7364e31ba7e905489a4aa55e:pNone:30.0-76.0`

## 9. Síntese técnica

Na arquitetura de automação, a correção eficiente de falhas depende menos de “trocar o componente suspeito” e mais de **localizar corretamente a camada defeituosa**. As fontes indicam que problemas de medição, scan, endereçamento, janelas de comunicação, módulos remotos, alimentação comum e redundância mal compreendida podem produzir sintomas semelhantes no supervisório.

Assim, para fins profissionais, o raciocínio mais robusto é:

- identificar a camada em que o erro nasce;
- distinguir falha pontual de falha comum de arquitetura;
- separar indisponibilidade de medição, indisponibilidade de controle e indisponibilidade de supervisão;
- entender que redundância melhora alguns atributos, mas não elimina a necessidade de diagnóstico de fonte, CPU, interface, I/O e comunicação.

**Fontes:** `petroles-4ee4bce16acf674505c8912d:pNone:490527.0-490575.0`, `petroles-004c2afadba7ea17c7dd7908:pNone:4159910.0-4159955.0`, `petroles-004c2afadba7ea17c7dd7908:pNone:839932.0-839979.0`, `petroles-004c2afadba7ea17c7dd7908:pNone:3795043.0-3795103.0`, `regis-7364e31ba7e905489a4aa55e:pNone:30.0-76.0`