# Filosofia e capacidade de geração elétrica em FPSOs

## 1. Premissas da filosofia de geração em FPSO
Em um FPSO, o sistema elétrico é tipicamente **isolado**, isto é, **não há conexão com um sistema elétrico externo** que possa absorver distúrbios, fornecer potência de reposição ou servir como suporte de contingência. Essa condição muda profundamente os critérios de projeto da geração: a própria unidade precisa carregar internamente sua capacidade de produção, sua margem de contingência e sua filosofia de continuidade operacional.

Na descrição de FPSO apresentada nas fontes, a filosofia típica considera:
- **quatro turbogeradores principais** na geração principal;
- **três geradores suficientes para a operação normal**;
- **um quarto gerador em stand-by**;
- **um gerador auxiliar**;
- **um gerador de emergência**.

Essa arquitetura não é apenas uma escolha de arranjo elétrico; ela reflete a necessidade de combinar:
- atendimento à carga total da planta em regime normal;
- tolerância à indisponibilidade de pelo menos uma unidade geradora principal;
- manutenção da segurança da instalação em shutdowns ou perda da geração principal;
- capacidade de retomada operacional.

A classificação das cargas sustenta a filosofia de capacidade instalada:
- **Cargas normais (não essenciais):** podem ser interrompidas sem comprometer diretamente a segurança. Parte delas é importante para a retomada da produção.
- **Cargas essenciais:** mantêm sistemas relevantes para a continuidade segura da unidade. São alimentadas pelo barramento essencial, que na descrição citada é conectado ao barramento principal por **no mínimo duas conexões**.
- **Cargas de emergência:** suportam funções críticas à salvaguarda da vida, segurança operacional dos poços e de equipamentos críticos de processo. Essas cargas devem permanecer energizadas durante a transição entre a perda da geração principal e a entrada do gerador de emergência, bem como em cenários de falha desse gerador, com suporte de **UPS e sistemas em corrente contínua**.

Exemplos citados de cargas essenciais incluem compressores de ar de serviço e instrumentação, unidades hidráulicas de controle submarino e sistemas de ventilação/refrigeração. Entre as cargas de emergência aparecem, por exemplo, fogo e gás, parada de emergência, iluminação de emergência, telecomunicações, sistemas de controle/intertravamento e painéis associados ao gerador de emergência e à bomba de incêndio.

**Implicação prática para dimensionamento:** a filosofia de geração principal não deve ser confundida com a filosofia de continuidade de todas as cargas. Em caso de perda parcial ou total da geração principal, a continuidade requerida passa a ser definida pela **priorização de cargas**. Assim:
- a **geração principal** é dimensionada para a operação da planta;
- a **geração auxiliar** pode sustentar cargas auxiliares relevantes à retomada da produção em indisponibilidade da geração principal;
- a **geração de emergência + UPS/DC** é voltada à segurança e à preservação de funções críticas, não à manutenção da produção total.

**Fontes da seção:** `regis-74dd376119cbb653fe9922bc:pNone:5742.0-6007.0`, `regis-74dd376119cbb653fe9922bc:pNone:6011.0-6348.0`

## 2. Critério de capacidade instalada: arranjos k-de-n e relação com N+1
As fontes descrevem que um FPSO típico pode ter **potência instalada da ordem de 100 MVA** como exemplo de referência. Para esse tipo de unidade, a redundância da geração principal costuma ser expressa por uma configuração **k-de-n**:
- **n** = número de geradores instalados;
- **k** = número mínimo de geradores necessários para alimentar toda a planta.

Esse formalismo é muito útil porque transforma a redundância em critério explícito de projeto.

### 2.1 Interpretação técnica do k-de-n
Se os geradores forem assumidos como aproximadamente idênticos, e se a planta exigir uma demanda aparente total \(D\), então a potência unitária mínima por gerador, na lógica idealizada do arranjo, é:

- **Potência unitária mínima ≈ D / k**

Logo, a potência instalada total fica:

- **Potência instalada total ≈ n · D / k**

Essa relação reproduz os valores informados na fonte para uma demanda de **100 MVA**:
- **1-de-1 (série):** 100 MVA
- **1-de-2 (paralelo):** 200 MVA
- **1-de-3:** 300 MVA
- **2-de-3:** 150 MVA
- **2-de-4:** 200 MVA
- **3-de-4:** 134 MVA

No caso **3-de-4**, o valor publicado de **134 MVA** é compatível com arredondamento de \(4 × 100/3 ≈ 133,3\) MVA.

### 2.2 Relação entre k-de-n e N+1
A lógica **N+1** aparece como um caso particular de k-de-n quando a planta precisa de **N unidades em operação** e existe **1 unidade adicional de reserva instalada**. Assim:
- **2-de-3** é um caso típico de **N+1**;
- **3-de-4** também é **N+1**;
- **2-de-4** já representa redundância mais ampla que N+1 sob o ponto de vista de quantidade instalada.

### 2.3 Consequência econômica e operacional
O requisito de redundância impacta diretamente o capital investido. Quanto maior a redundância:
- maior a capacidade instalada total;
- maior o investimento inicial em máquinas, transformadores, switchgear, proteção e auxiliares associados;
- porém, em princípio, maior a tolerância a falhas e a janelas de manutenção.

A fonte destaca explicitamente o trade-off entre **CAPEX** e **disponibilidade**. Projetos com CAPEX menor tendem a ter menos redundância, menos instrumentação para manutenção baseada em condição e, potencialmente, menor confiabilidade/eficiência operacional. Em FPSO, esse trade-off é especialmente sensível porque a perda de geração pode significar perda relevante de produção, além de impactos em segurança e retomada operacional.

### 2.4 Leitura correta do número de MVA instalado
A potência instalada total por si só não é o único indicador de robustez. Dois arranjos diferentes podem ter a mesma potência instalada, mas comportamentos distintos frente a falhas e manutenção. Exemplo dado pelas fontes:
- **2-de-4 = 200 MVA**
- **1-de-2 = 200 MVA**

Apesar do mesmo total instalado, o comportamento operacional não é equivalente: o primeiro admite a perda de até duas máquinas sem necessariamente inviabilizar a filosofia de contingência da mesma forma que o segundo.

**Fontes da seção:** `regis-74dd376119cbb653fe9922bc:pNone:6011.0-6348.0`, `regis-74dd376119cbb653fe9922bc:pNone:5742.0-6007.0`

## 3. Reserva girante, stand-by e reserva de rápido acionamento no contexto de FPSO
As fontes genéricas sobre sistemas elétricos definem:
- **reserva girante (spinning reserve):** capacidade ociosa de unidades já em operação, disponível para assumir carga rapidamente;
- **reserva de rápido acionamento (quick start reserve):** capacidade de unidades capazes de entrar em operação rapidamente após uma contingência.

Embora essas definições tenham sido apresentadas em contexto mais amplo de sistemas elétricos, elas são úteis para interpretar a filosofia de FPSO:
- quando três geradores principais estão online e um está desligado em stand-by, a unidade pode combinar **reserva girante** nas máquinas carregadas abaixo do máximo com **reserva de rápido acionamento** na máquina parada, desde que o tempo de partida seja compatível com a filosofia operacional;
- em sistemas isolados offshore, essa reserva é ainda mais crítica porque **não existe suporte externo de rede**.

Do ponto de vista de projeto, isso significa que o dimensionamento não deve considerar apenas a carga média ou a carga máxima estática. Também devem ser avaliados:
- margem para absorver variações de carga;
- capacidade de atravessar a perda de uma unidade geradora principal;
- tempo necessário para colocar uma unidade stand-by em carga;
- efeito de partidas de grandes consumidores sobre frequência e tensão.

Em termos conceituais, um arranjo **3-de-4** com três máquinas em operação e uma em stand-by expressa bem essa combinação entre produção normal e contingência. Já um arranjo **2-de-3** pode ser adequado quando duas unidades cobrem a planta e a terceira cumpre o papel de contingência/stand-by.

**Fontes da seção:** `petroles-004c2afadba7ea17c7dd7908:pNone:420532.0-420567.0`, `regis-74dd376119cbb653fe9922bc:pNone:5742.0-6007.0`, `regis-74dd376119cbb653fe9922bc:pNone:6011.0-6348.0`

## 4. Escolha da máquina motriz e efeito na filosofia de capacidade
As fontes associadas a geração termelétrica e cogeração destacam características relevantes de turbinas a gás e de tecnologias de rápida resposta.

### 4.1 Turbogeradores principais
Na descrição do FPSO, os geradores principais são turbogeradores que podem usar **gás natural da própria produção** ou **óleo diesel**. Isso é coerente com a necessidade de autonomia e flexibilidade de combustível em ambiente offshore.

Para turbinas a gás simples, a literatura citada aponta como características importantes:
- **expansão modular**;
- **simplicidade de implantação dos módulos**;
- **menor tempo de comissionamento**;
- **investimento reduzido** quando comparado a arranjos caldeira + turbina a vapor;
- **alto fator de disponibilidade**.

Esses atributos favorecem sua aplicação em sistemas nos quais compactação, modularidade e prazo de implantação são relevantes, como em unidades offshore.

### 4.2 Reserva rápida e partida
Em texto de contexto mais amplo, as tecnologias termelétricas são comparadas quanto ao tempo de partida e rampa de carga:
- **motores de combustão interna** (tipicamente diesel/óleo combustível): resposta mais rápida;
- **turbinas a gás aeroderivadas:** segunda faixa de resposta, com partida relativamente rápida;
- **turbinas a gás industriais:** mais robustas e com maior tempo para atingir carga máxima.

Transpondo esse raciocínio para FPSOs, sem transformá-lo em regra universal:
- motores a combustão podem ser muito atrativos para **geração de emergência** ou **reserva de rápido acionamento**;
- turbinas aeroderivadas podem ser interessantes quando se deseja **boa resposta dinâmica** com elevada disponibilidade operacional;
- turbinas industriais tendem a ser mais compatíveis com geração principal contínua, desde que a filosofia de contingência absorva seu tempo de partida/carga.

### 4.3 Disponibilidade e mantenabilidade
A fonte também atribui às unidades aeroderivadas características de **alta confiabilidade**, **tempo reduzido de manutenção** e **elevado rendimento**, indicando potencial contribuição para a disponibilidade da instalação.

Na prática de FPSO, a decisão entre turbina a gás, motor diesel ou combinação entre ambos precisa considerar simultaneamente:
- combustível disponível a bordo;
- resposta requerida para contingência;
- espaço/peso;
- filosofia de operação contínua ou stand-by;
- manutenção e sobressalentes;
- meta de disponibilidade do sistema isolado.

**Fontes da seção:** `regis-74dd376119cbb653fe9922bc:pNone:5742.0-6007.0`, `regis-810b669184c0f77601c59a87:pNone:13321.0-13552.0`, `petroles-004c2afadba7ea17c7dd7908:pNone:420532.0-420567.0`

## 5. Disponibilidade: efeito da redundância e da estratégia de manutenção
As fontes da tese destacam dois pontos importantes para a filosofia de geração:
1. a redundância influencia a **criticidade funcional** dos equipamentos;
2. a estratégia de manutenção influencia diretamente a **disponibilidade média do sistema**.

Além disso, o contexto de FPSO impõe restrições reais:
- grande quantidade de equipamentos instalados;
- limitação de mão de obra a bordo;
- necessidade de priorização de recursos de manutenção.

### 5.1 Sem redundância: criticidade alta
No caso simulado de **configuração radial com um gerador de 100 MVA** (explicitamente descrita como não usual em offshore, usada para validação metodológica), qualquer falha no conjunto **gerador + relé + disjuntor** implica falha do sistema principal. Por isso, a criticidade desses itens foi tratada como alta.

Para um horizonte de 5 anos, a disponibilidade média simulada foi:
- **96,07%** com método tradicional de manutenção;
- **98,63%** com método proposto na tese.

O resultado mostra que, em arquitetura sem redundância, pequenas diferenças de indisponibilidade de equipamentos têm grande impacto sistêmico.

### 5.2 Com redundância 3-de-4: criticidade individual menor, disponibilidade sistêmica maior
No caso **k=3 e n=4**, com quatro geradores de **33,5 MVA** cada, totalizando **134 MVA**, a fonte classifica o arranjo como **usual em sistemas elétricos offshore**. Nesse caso, a falha de um conjunto gerador-relé-disjuntor **não provoca imediatamente a falha do sistema principal**, pois ainda restam três conjuntos capazes de sustentar a planta.

Para 5 anos, a disponibilidade média simulada foi:
- **98,64%** com método tradicional;
- **99,76%** com método proposto.

A principal leitura para projeto é que a redundância:
- reduz a probabilidade de perda total do suprimento principal por falha única;
- diminui a criticidade individual funcional de cada conjunto gerador/proteção/manobra;
- cria margem para manutenção sem interromper a produção total, desde que a gestão de cargas e a contingência sejam compatíveis.

### 5.3 O que esses resultados significam para dimensionamento
Esses números não devem ser usados como garantia universal de desempenho, mas ajudam a mostrar a direção do efeito:
- **mais redundância tende a aumentar disponibilidade**, desde que a filosofia de manutenção seja coerente;
- a disponibilidade não depende só do número de geradores, mas também do conjunto **gerador + disjuntor + proteção + manutenção**;
- em sistema isolado, indisponibilidade elétrica tem impacto direto em produção.

Isso reforça que a decisão de capacidade instalada não é apenas um problema de somatório de MVA. É também uma decisão de **confiabilidade funcional**, **janela de manutenção** e **tolerância a falhas**.

**Fontes da seção:** `regis-74dd376119cbb653fe9922bc:pNone:6011.0-6348.0`, `regis-74dd376119cbb653fe9922bc:pNone:31177.0-31621.0`, `regis-74dd376119cbb653fe9922bc:pNone:32627.0-33086.0`, `regis-74dd376119cbb653fe9922bc:pNone:5742.0-6007.0`

## 6. Papel do gerador auxiliar, do gerador de emergência e do UPS no critério de capacidade
Uma filosofia de geração robusta em FPSO não se encerra nos geradores principais.

### 6.1 Gerador auxiliar
As cargas normais incluem cargas auxiliares importantes para a retomada da produção. A fonte indica que essas cargas **podem ser alimentadas pelo gerador auxiliar** quando houver indisponibilidade do sistema de geração principal.

Portanto, o gerador auxiliar não substitui integralmente a geração principal; seu papel é mais seletivo e funcional:
- sustentar serviços auxiliares necessários à retomada operacional;
- reduzir o tempo de recuperação após contingência;
- prover flexibilidade operacional em indisponibilidades da geração principal.

### 6.2 Gerador de emergência
O gerador de emergência é associado às cargas essenciais e de emergência. Sua função é garantir energia para sistemas ligados à segurança da unidade e à salvaguarda da vida. Isso implica que seu dimensionamento segue a **lista de cargas emergenciais/essenciais** e não a carga total da produção.

### 6.3 UPS e sistemas em corrente contínua
As cargas de emergência devem permanecer energizadas:
- no intervalo entre a perda da geração principal e a entrada do gerador de emergência;
- e também em falha do próprio gerador de emergência, conforme a filosofia adotada.

Daí o papel do **UPS** e dos sistemas **220 Vac / 12, 24, 48 e 125 Vcc** citados na fonte. Em termos de filosofia de capacidade, eles compõem a camada de continuidade de curtíssimo prazo e de maior criticidade funcional.

**Conclusão de projeto:** a capacidade de geração de um FPSO é multicamadas:
1. **capacidade de produção** na geração principal;
2. **capacidade de suporte/restart** na geração auxiliar;
3. **capacidade de segurança** na geração de emergência;
4. **capacidade de transição e retenção de funções críticas** em UPS/DC.

**Fontes da seção:** `regis-74dd376119cbb653fe9922bc:pNone:5742.0-6007.0`, `regis-74dd376119cbb653fe9922bc:pNone:6011.0-6348.0`

## 7. Sincronismo e controle: implicações para filosofia de múltiplos geradores
Quando a instalação utiliza **geradores síncronos** em corrente alternada, a operação em paralelo exige **arranjos específicos de controle e proteção** para sincronismo com o sistema. A fonte destaca que geradores síncronos:
- devem operar precisamente em sincronia com a frequência do sistema;
- requerem controle e proteção apropriados para o sincronismo;
- podem operar com fator de potência unitário ou adiantado;
- podem contribuir para o controle do fator de potência da instalação.

Na filosofia de múltiplas unidades geradoras de FPSO, isso tem implicações diretas:
- o aumento de n no arranjo k-de-n melhora a redundância, mas aumenta a necessidade de coordenação operacional entre unidades;
- a repartição de potência ativa entre máquinas precisa ser compatível com a filosofia de despacho;
- a repartição de potência reativa e o controle de tensão/fator de potência passam a ser parte do critério de operação segura e estável.

Logo, a decisão sobre quantidade e porte de geradores não é apenas mecânica ou econômica; ela também afeta a complexidade de sincronismo, proteção e controle do sistema isolado.

**Fontes da seção:** `regis-810b669184c0f77601c59a87:pNone:13321.0-13552.0`, `regis-74dd376119cbb653fe9922bc:pNone:5742.0-6007.0`

## 8. Critérios práticos de decisão para dimensionar a filosofia de geração
Com base nas fontes, os critérios profissionais mais relevantes para escolher a filosofia e a capacidade de geração de um FPSO são:

### 8.1 Determinar a demanda que precisa ser efetivamente sustentada
Separar claramente:
- carga total de produção em regime normal;
- carga mínima para continuidade operacional segura;
- carga necessária para retomada da produção;
- carga de emergência e segurança.

### 8.2 Escolher o nível de redundância
Aplicar conscientemente a lógica **k-de-n/N+1**, observando que:
- menor redundância reduz investimento inicial;
- maior redundância melhora tolerância a falhas e manutenção;
- a melhor escolha depende do custo da perda de produção e da criticidade do processo.

### 8.3 Verificar a filosofia de reserva
Definir qual parcela da contingência será atendida por:
- **reserva girante** nas máquinas online;
- **unidade stand-by** de rápido acionamento;
- **load shedding/priorização de carga**, quando necessário.

### 8.4 Compatibilizar máquina motriz e missão operacional
Selecionar entre turbina a gás, motor diesel ou combinação, considerando:
- combustível disponível;
- rapidez de partida e rampa de carga;
- disponibilidade esperada;
- facilidade de manutenção e comissionamento.

### 8.5 Incorporar disponibilidade ao projeto desde o início
Não tratar manutenção como tema apenas da operação. As fontes mostram que:
- a falta de redundância e de instrumentação pode degradar a disponibilidade ao longo do ciclo de vida;
- manutenção baseada em condição e priorização por criticidade tendem a melhorar disponibilidade;
- em FPSO, a limitação de recursos humanos a bordo exige escolhas de arquitetura que facilitem a manutenção.

**Fontes da seção:** `regis-74dd376119cbb653fe9922bc:pNone:5742.0-6007.0`, `regis-74dd376119cbb653fe9922bc:pNone:6011.0-6348.0`, `regis-74dd376119cbb653fe9922bc:pNone:31177.0-31621.0`, `regis-74dd376119cbb653fe9922bc:pNone:32627.0-33086.0`, `regis-810b669184c0f77601c59a87:pNone:13321.0-13552.0`, `petroles-004c2afadba7ea17c7dd7908:pNone:420532.0-420567.0`

## 9. Síntese técnica
Para FPSOs, a filosofia de geração elétrica deve ser entendida como uma composição entre **capacidade**, **redundância**, **tempo de resposta** e **segurança funcional**. Em termos práticos:
- o sistema é isolado e precisa ser autossuficiente em contingência;
- a classificação de cargas define qual capacidade deve ser sustentada em cada modo operacional;
- arranjos **k-de-n** permitem traduzir tolerância a falhas em potência instalada;
- a redundância aumenta CAPEX, mas tende a elevar disponibilidade e flexibilidade de manutenção;
- a máquina motriz influencia não apenas eficiência, mas também rapidez de partida e filosofia de reserva;
- gerador auxiliar, gerador de emergência e UPS/DC não são acessórios: são partes estruturais da filosofia de continuidade;
- em múltiplos geradores, sincronismo, proteção e controle de potência/fator de potência tornam-se parte do critério de projeto.

Em resumo, **dimensionar a geração de um FPSO não é somente “somar MVA”**; é definir qual combinação de máquinas, reservas e camadas de suprimento permite manter produção, segurança e recuperação operacional com o nível de disponibilidade desejado.