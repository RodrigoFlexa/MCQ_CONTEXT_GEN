# Ventilação e proteção pressão-vácuo

## 1. Finalidade dos sistemas de ventilação e proteção P/V em tanques de carga e slop de FPSO

Nos tanques de carga e slop, o sistema de ventilação e os dispositivos de proteção contra sobrepressão e vácuo existem para manter a integridade estrutural do tanque e controlar, de forma segura, a movimentação do espaço de vapor. Em operação, o espaço acima do líquido sofre variações de pressão por pelo menos quatro mecanismos relevantes:

1. **enchimento do tanque**, que desloca vapor/gás e tende a elevar a pressão interna;
2. **esvaziamento/transferência/offloading**, que tende a gerar vácuo se a reposição de gás não acompanhar a retirada de líquido;
3. **variações térmicas**, que expandem ou contraem o vapor do tanque;
4. **operações com gás inerte (IG)**, que mantêm o tanque com pressão positiva e baixo teor de oxigênio, mas também impõem requisitos de controle de pressão, qualidade do gás e confiabilidade da rede.

Em termos de segurança de processo, a função do conjunto ventilação + proteção P/V é dupla:

- **evitar que a pressão interna ultrapasse o limite estrutural do tanque**;
- **evitar vácuo excessivo e ingresso indevido de ar**, o que pode comprometer a integridade do tanque e, em tanques inertados, aumentar o risco de formação de atmosfera inflamável no espaço de vapor.

A descrição clássica de válvula de pressão e vácuo em tanques de estocagem menciona alívio de vapores quando a pressão interna sobe e admissão de ar durante o descarregamento. Para FPSOs, esse princípio físico continua válido, mas deve ser compatibilizado com a filosofia do **sistema de gás inerte**: em tanques de carga inertados, a reposição gasosa desejada é, em regra, gás inerte e não ar atmosférico, justamente para limitar o teor de oxigênio no espaço de vapor.

**Fontes:** `regis-350bcc2de3ebad0b293b5ed6:pNone:0.0-44.0`, `hse-84ee4101a6ca194620d4089b:p108-110:10.0-19.0`

## 2. Dispositivos de proteção: conceitos, tipos e implicações para tanques

### 2.1 Válvula de pressão e vácuo (P/V valve)

A válvula de pressão e vácuo é descrita, na fonte histórica da Petrobras, como um dispositivo com **dois bocais de alívio independentes**, montados de forma inversa:

- um abre quando há **pressão interna** no tanque;
- outro abre quando há **vácuo** no interior do tanque.

A vedação é feita por disco contra sede. Na descrição da fonte, o ponto de abertura do lado de pressão é geralmente regulado por contrapeso; no lado de vácuo, a resistência à abertura decorre do próprio peso do conjunto móvel. Em termos operacionais, o conceito essencial é que o dispositivo deve permitir que o tanque “respire” dentro de uma faixa estreita, sem operar continuamente e sem permitir pressões ou depressões estruturamente perigosas.

Para FPSOs, a válvula P/V costuma integrar o **header de vent dos tanques de carga**. O papel prático não é apenas “aliviar”, mas também sustentar a filosofia de operação do espaço de vapor: pressão levemente positiva, baixa entrada de oxigênio, e rota segura para descarga de vapores.

### 2.2 Diferença entre válvula de alívio, válvula de segurança e válvula de segurança e alívio

A fonte distingue:

- **válvula de alívio (relief valve):** típica para líquidos; abertura gradual;
- **válvula de segurança (safety valve):** típica para gases/vapores/ar; abertura rápida e intermitente;
- **válvula de segurança e alívio (safety relief valve):** aplicável a líquidos e gases.

Essa distinção é útil porque o sistema de ventilação de tanques trabalha principalmente com **vapores/gases**, enquanto redes líquidas associadas podem requerer outra filosofia de proteção. Em tanques de carga, o dispositivo mais característico continua sendo a válvula P/V e, em algumas arquiteturas, dispositivos emergenciais complementares.

### 2.3 Conceitos de set pressure, acumulação, sobrepressão e contrapressão

Os conceitos clássicos apresentados na fonte são relevantes para entender o comportamento da proteção:

- **pressão de ajuste (set pressure):** pressão na qual a válvula é regulada para abrir, sem considerar contrapressão;
- **acumulação:** acréscimo de pressão entre o início da abertura e a abertura plena;
- **sobrepressão (overpressure):** elevação de pressão a montante do dispositivo de segurança, decorrente da acumulação;
- **contrapressão (back pressure):** pressão estática na descarga da válvula, ou pressão gerada por perdas de carga na linha de descarga.

Para sistemas de vent comuns em FPSOs, a **contrapressão** é um tema particularmente importante. Se vários tanques descarregam para um mesmo header, ou se a linha de vent possui perdas elevadas, a contrapressão pode alterar o ponto efetivo de abertura e a capacidade de alívio do dispositivo. Isso afeta a capacidade de o tanque “respirar” na taxa necessária durante carga, offloading, aquecimento ou evento anormal.

### 2.4 Válvulas convencionais x balanceadas

Na fonte histórica, válvulas do tipo **convencional** têm pressão de alívio afetada pela contrapressão. Já válvulas **balanceadas** são indicadas quando a contrapressão é variável e/ou quando o fluido é corrosivo. Embora a discussão da fonte seja geral e não específica de P/V valves de tanques, o princípio de engenharia permanece útil: **se a descarga do dispositivo estiver sujeita a contrapressão variável, o projetista precisa considerar o efeito dessa contrapressão sobre o ponto de abertura e a capacidade real de alívio**.

### 2.5 Dispositivos complementares

A mesma fonte menciona **disco de ruptura** como dispositivo que, em certos casos, pode substituir ou complementar válvulas de alívio de pressão. Em arranjos de tanques, a lógica correspondente é a existência de **proteção emergencial adicional** quando o dispositivo principal não for suficiente ou falhar. No trecho do HSE, essa filosofia aparece de forma mais diretamente aplicável ao FPSO por meio do **emergency pressure/vacuum breaker**, previsto para atuar se a válvula P/V principal falhar ou não aliviar na taxa apropriada.

**Fontes:** `regis-350bcc2de3ebad0b293b5ed6:pNone:0.0-44.0`, `regis-350bcc2de3ebad0b293b5ed6:pNone:21.0-86.0`, `regis-350bcc2de3ebad0b293b5ed6:pNone:45.0-128.0`, `hse-84ee4101a6ca194620d4089b:p108-110:10.0-19.0`

## 3. Integração entre ventilação de tanques e sistema de gás inerte

O trecho do HSE, ao resumir exigências associadas ao SOLAS para FPSOs/FSUs, mostra que a ventilação de tanques não deve ser tratada isoladamente: ela depende do desempenho do **sistema de gás inerte (IG)**.

### 3.1 Objetivo operacional do IG

O sistema de IG deve:

- manter **pressão positiva** no tanque;
- reduzir o risco de **acúmulo de atmosfera explosiva** no espaço de vapor;
- fornecer vazão suficiente para acompanhar a retirada de líquido e sustentar a filosofia de inertização durante operação normal e perturbações previsíveis.

### 3.2 Requisitos operacionais citados na fonte HSE/SOLAS

Segundo o trecho fornecido, o sistema deve ser capaz de:

- entregar vazão de descarga de **pelo menos 125% v/v da capacidade nominal máxima das bombas de carga**;
- operar com **ao menos dois blowers**;
- manter pressão positiva, sendo citada **pressão normal de descarga de 0,12 barg**;
- fornecer gás com **teor de oxigênio inferior a 5% v/v**;
- possuir **monitoramento e alarme** para teor de oxigênio e demais variáveis críticas.

Esses pontos se conectam diretamente à proteção P/V. Se a vazão de IG for insuficiente durante exportação/offloading ou transferência, o tanque pode migrar rapidamente para condição de vácuo. Se o teor de O2 do IG estiver alto, a pressão positiva deixa de garantir, por si só, ambiente seguro no espaço de vapor.

### 3.3 Barreiras contra retorno de vapores de hidrocarbonetos

A fonte HSE indica a necessidade de **pelo menos dois dispositivos/sistemas de não retorno** para impedir backflow de vapores de hidrocarbonetos para espaços de máquinas no convés. Um deles deve ser **selo d’água**; o outro deve ficar a jusante do selo e pode ser dispositivo mecânico ou válvula manual de isolamento.

Do ponto de vista de segurança, isso evita que a rede de inertização/ventilação se torne caminho de propagação reversa de vapores inflamáveis para áreas não classificadas ou com fontes de ignição.

### 3.4 Alarmes e intertravamentos relevantes

A fonte cita alarmes para:

- **alto teor de oxigênio** no main de IG, normalmente >5% v/v;
- **baixa pressão** no main de IG;
- **baixa pressão de suprimento** ao selo d’água do convés, se existente;
- **baixo nível de água** no deck seal;
- **alta temperatura** do IG no main;
- **baixa pressão de água** para o scrubber do IG.

Também é citado que a **gas regulating valve** normalmente controla o fluxo de IG para os tanques e deve **fechar** se esses eventos ocorrerem ou se os blowers falharem. Isso evidencia uma filosofia importante de projeto: a rede de vent/IG não é apenas passiva; ela contém funções automáticas de isolamento e resposta a desvios de qualidade e disponibilidade do gás.

**Fontes:** `hse-84ee4101a6ca194620d4089b:p108-110:10.0-19.0`

## 4. Arranjo de ventilação e descarga segura de vapores de hidrocarbonetos

### 4.1 Tipos de vent e critérios geométricos citados na fonte

O trecho do HSE diferencia dois arranjos de descarga de vapores:

1. **free-flowing vents**
   - pelo menos **6 m acima do convés principal**;
   - pelo menos **10 m horizontalmente** de entradas de ar abertas;
   - devem conter **flame arrestors**, para evitar flashback ao tanque.

2. **high-velocity vents**
   - devem se estender a pelo menos **2 m acima do convés dos tanques de carga**;
   - também a pelo menos **10 m** de entradas de ar;
   - **não requerem flame arrestors** quando a velocidade de saída dos gases é **≥30 m/s**, estimada como superior ao dobro da velocidade de frente de chama.

A implicação de projeto é clara: o sistema de ventilação deve descarregar vapores em local e condição que minimizem:

- reentrada em tomadas de ar;
- exposição de pessoal e equipamentos a nuvens inflamáveis;
- risco de propagação de chama para o interior do tanque.

### 4.2 Detecção e supressão associados aos vents

A mesma fonte afirma que os vents devem ter **sistemas associados de detecção de incêndio e snuffing**. Isso reforça que o vent não é apenas uma tubulação de escape, mas um ponto crítico de interface entre o inventário de hidrocarbonetos do tanque e a atmosfera externa.

### 4.3 Faixa de “respiração” do tanque

Segundo o HSE, geralmente um ou dois conjuntos de válvula de pressão/vácuo são conectados ao main crude oil vent header para permitir que os tanques “respirem”, normalmente entre:

- **0,2 kg/cm² acima da pressão atmosférica**; e
- **0,07 kg/cm² abaixo da pressão atmosférica**.

Esses valores devem ser entendidos como valores citados na fonte para determinado contexto de FPSO/FSU, não como setpoints universais. O ponto técnico relevante é a existência de uma **janela operacional estreita**, dentro da qual o tanque pode acomodar variações normais de vapor sem entrar em condição estruturalmente perigosa.

### 4.4 Procedimentos operacionais para venting

O HSE destaca que o operador deve ter **procedimentos de venting de tanques de carga** e orientação sobre em que condições meteorológicas a operação pode ocorrer. O texto informa, como diretriz geral, que o venting deveria ocorrer apenas com **vento ≥2 m/s**.

Na prática, isso vincula a abertura operacional do sistema de vent à capacidade de dispersão atmosférica. Condições de vento muito baixo podem favorecer permanência de nuvem de hidrocarbonetos nas proximidades do convés e de tomadas de ar.

### 4.5 Recuperação de vapores / blanketing por hidrocarboneto

A fonte HSE menciona que, para reduzir emissões de VOC, pode-se empregar **hydrocarbon blanketing and recovery system**. Porém, se esse sistema ficar indisponível, o operador deve ter procedimentos para garantir que o **IG esteja disponível e comutado para o sistema em serviço**. Devem existir ainda medidas secundárias caso a comutação falhe, inclusive parada de planta.

O mesmo trecho alerta para outro ponto de integração: se o arranjo de recuperação/blanketing por HC puder **fechar a rota para flare**, deve existir um método **fail-safe** para restabelecer a rota à flare e evitar sobrepressão. Se a flare não permanecer acesa continuamente, deve haver procedimento para acendê-la em caso de sobrepressão.

Isso mostra que o manejo seguro de vapores não se resume a “ventilar menos”. Reduzir emissões por recuperação de vapores só é aceitável quando a arquitetura de segurança preserva:

- caminho confiável para alívio;
- comutação segura para IG;
- rota disponível para flare, quando requerida pela filosofia da instalação.

**Fontes:** `hse-84ee4101a6ca194620d4089b:p108-110:10.0-19.0`

## 5. Dimensionamento do vent e a necessidade de considerar o caso de fogo

O relatório de investigação da ANP sobre a P-20 fornece uma lição de projeto diretamente aplicável ao tema: **não descartar indevidamente o caso de fogo no dimensionamento do vent**.

### 5.1 O erro de premissa identificado no caso investigado

No caso analisado, as vazões usadas para cálculo de perda de carga do sistema de vent foram derivadas das **máximas vazões em condição normal** de aspiração/expiração, convertidas para vazão mássica com densidade do ar de 1,29 kg/m³. O relatório conclui que o **caso de fogo foi desconsiderado** no dimensionamento.

A memória de cálculo assumia que, em caso de fogo, o sistema de dilúvio protegeria o tanque a ponto de o fluido não atingir a ebulição. A ANP registra que essa premissa está **em desacordo com a API STD 2000**, a qual define a **exposição ao fogo como circunstância de sobrepressão** a ser considerada.

### 5.2 Ligação fraca teto-costado e capacidade adicional de venting

O relatório resume que, conforme a API 2000 citada no caso:

- o **tipo construtivo do tanque** influencia a necessidade de capacidade adicional de venting em incêndio;
- se o tanque possuir **ligação fraca entre teto e costado**, essa ligação pode romper preferencialmente e aliviar a sobrepressão;
- se o tanque **não** possuir essa ligação fraca, devem ser aplicados os requisitos correspondentes de capacidade de venting adicional.

No evento analisado, o tanque não possuía a ligação fraca e, portanto, o dimensionamento deveria ter seguido as equações aplicáveis da API 2000 para esse caso.

### 5.3 Dilúvio não é justificativa automática para reduzir a carga de fogo do vent

A ANP destaca que, mesmo para tanques com aplicação de água, o **fator ambiental F** citado pela API 2000 pode permanecer em **1,0**, porque a confiabilidade da água aplicada depende de múltiplos fatores: vento forte, obstruções, suprimento de água, cobertura não uniforme da superfície etc. Em outras palavras, a mera existência de dilúvio/névoa não autoriza, por si só, reduzir o caso de fogo no cálculo do vent.

Essa conclusão é decisiva para FPSOs:

- o vent deve ser verificado não só para “respiração normal” do tanque, mas também para **sobrepressão de emergência**;
- sistemas auxiliares, como dilúvio, **não devem ser tratados como premissa automática de descarte** do cenário de fogo, salvo respaldo claro na norma aplicável e na confiabilidade efetivamente demonstrada do sistema.

### 5.4 Consequência prática observada no caso

Segundo o relatório, a adoção dessa premissa levou à manutenção de vents preexistentes de **2"**, que não seriam suficientes para o alívio na condição considerada pela investigação. O detalhe dimensional pertence ao caso específico e não deve ser generalizado; a lição geral é que **o diâmetro do vent não pode ser validado apenas com base em vazões normais se houver cenários de fogo aplicáveis**.

### 5.5 Relação com operação de FPSO

Em FPSOs, a avaliação de capacidade do vent deve cobrir pelo menos:

- enchimento e exportação na taxa máxima prevista;
- variações térmicas plausíveis do inventário e do espaço de vapor;
- perda ou degradação do suprimento de IG quando isso puder conduzir a vácuo;
- eventos de sobrepressão por fogo, quando aplicáveis à configuração do tanque e da norma usada no projeto.

As equações 1A/1B da API 2000 são mencionadas no relatório da ANP, mas **não foram reproduzidas integralmente nos trechos fornecidos**; portanto, este documento preserva apenas o critério técnico evidenciado pelo caso, sem reconstituir fórmulas não disponíveis.

**Fontes:** `anp-668be0de2e3714c6db785a31:p30-35:12.0-3.0`

## 6. Operação, monitoramento e resposta a condições anormais

### 6.1 Variáveis que precisam ser monitoradas

Com base nos trechos fornecidos, o monitoramento mínimo relevante para ventilação segura de tanques inclui:

- **pressão do tank vent / espaço de vapor**;
- **pressão do main de IG**;
- **teor de O2 no IG**;
- **temperatura do IG**;
- **pressão e nível de água do deck seal**;
- condições que possam comprometer o **dreno do vent header** e de vasos associados.

### 6.2 Situações anormais críticas

As situações anormais mais claramente suportadas pelas fontes são:

- **alto O2 no IG**: aumenta o risco de perda de inertização adequada;
- **baixa pressão no IG main**: pode levar o tanque a vácuo durante retirada de líquido;
- **falha dos blowers do IG**: reduz ou elimina reposição de gás inerte;
- **falha da válvula P/V principal**: requer rota alternativa de alívio e atuação do emergency P/V breaker;
- **problemas no selo d’água**: perda de barreira contra retorno de vapores;
- **condições ambientais extremas que prejudiquem drenagem do vent header**: podem alterar o comportamento do sistema de ventilação;
- **vento muito baixo durante venting**: reduz dispersão atmosférica de vapores;
- **indisponibilidade do sistema de recuperação/blanketing por HC** sem comutação segura para IG.

### 6.3 Resposta operacional esperada

Dos trechos do HSE decorre a necessidade de procedimentos claros para:

- resposta do operador a **alto teor de oxigênio** no fluxo de IG;
- venting em **baixa velocidade de vento**;
- atuação em **condições ambientais severas** que comprometam drenagem ou funcionamento do header de vent;
- falha da válvula P/V e uso da proteção emergencial;
- indisponibilidade do sistema de recuperação de vapores, com **comutação para IG**;
- abertura de **rota fail-safe para flare**, quando a filosofia da instalação depender disso para evitar sobrepressão.

### 6.4 Elementos de manutenção e inspeção

O HSE trata o **pressure/vacuum breaker** como **safety critical element**, devendo ter padrão de desempenho e ser submetido a **testes e manutenção rotineiros**. Também recomenda verificar:

- se existem procedimentos de venting e política para baixo vento;
- qual seria a ação da operação sob condições extremas que afetem drenagem do sistema;
- se o IG atende à capacidade mínima requerida;
- se há monitoramento do O2 e alarmes ajustados apropriadamente.

Da fonte histórica da Petrobras, acrescenta-se o conceito de que a contrapressão na descarga pode alterar a pressão de abertura; logo, inspeção e análise de integridade devem abranger não apenas o dispositivo isolado, mas também o **header, as perdas de carga e a contrapressão real de descarga**.

**Fontes:** `hse-84ee4101a6ca194620d4089b:p108-110:10.0-19.0`, `regis-350bcc2de3ebad0b293b5ed6:pNone:21.0-86.0`, `regis-350bcc2de3ebad0b293b5ed6:pNone:45.0-128.0`

## 7. Critérios práticos de decisão para engenharia e operação

### 7.1 Quando a análise de contrapressão ganha importância

A contrapressão merece avaliação cuidadosa quando:

- vários tanques compartilham um **vent header comum**;
- a descarga do dispositivo percorre linhas longas ou com acessórios que elevem a perda de carga;
- a contrapressão puder variar com o modo operacional;
- a filosofia de proteção depender de abertura dentro de janela estreita de pressão.

Nessas situações, o princípio apresentado nas fontes gerais sobre válvulas é que **o dispositivo selecionado não pode ter sua pressão efetiva de abertura indevidamente deslocada pela contrapressão do sistema**.

### 7.2 Quando o caso de fogo não deve ser descartado

O caso de fogo não deve ser descartado apenas porque:

- existe sistema de dilúvio/água aplicada; ou
- as vazões normais de inspiração/expiração foram aparentemente atendidas.

O relatório da ANP mostra que a avaliação deve considerar o tipo construtivo do tanque e os critérios da API 2000 aplicáveis ao cenário de incêndio.

### 7.3 Quando o manejo de vapores exige integração com outros sistemas

O manejo seguro de vapores exige análise integrada quando houver:

- sistema de **recuperação de VOC/blanketing por HC**;
- necessidade de manter **rota disponível para flare**;
- dependência de **IG como sistema de contingência**;
- operação de venting sujeita a **restrições meteorológicas**.

### 7.4 O que caracteriza um arranjo robusto

Com base no conjunto das fontes, um arranjo robusto de ventilação e proteção P/V em FPSO tende a apresentar:

- manutenção de **pressão positiva controlada** no espaço de vapor;
- **O2 do IG controlado** e alarmado;
- dispositivos de **não retorno** entre tanques e espaços de máquinas;
- válvula(s) P/V principal(is) e **emergency P/V breaker** adequadamente dimensionados;
- vents localizados para **dispersão segura** e prevenção de flashback;
- procedimentos operacionais para **venting, baixo vento, falhas e comutação** de sistemas;
- verificação explícita do cenário de **fogo** no dimensionamento.

**Fontes:** `regis-350bcc2de3ebad0b293b5ed6:pNone:21.0-86.0`, `regis-350bcc2de3ebad0b293b5ed6:pNone:45.0-128.0`, `hse-84ee4101a6ca194620d4089b:p108-110:10.0-19.0`, `anp-668be0de2e3714c6db785a31:p30-35:12.0-3.0`