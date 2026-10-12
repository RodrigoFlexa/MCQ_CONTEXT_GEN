# Modelagem de consequências em estudos de segurança de FPSO/FSO

## 1. Finalidade e posição da modelagem de consequências nos estudos de segurança
A modelagem de consequências é a parte do estudo de segurança que transforma um evento iniciador plausível — por exemplo, perda de contenção de gás ou líquido inflamável — em efeitos físicos mensuráveis sobre pessoas, instalações e, quando aplicável, meio ambiente. Em termos de análise quantitativa de risco, ela compõe a etapa de **análise de risco**, na qual o risco é tratado como combinação de **frequência** e **consequência**.

Uma sequência técnica típica inclui:
1. seleção do incidente ou cenário a ser analisado;
2. definição do **modelo-fonte**, que descreve como o material é descarregado do processo;
3. aplicação de um **modelo de dispersão**, para estimar transporte e diluição da substância liberada;
4. quando o material é inflamável, aplicação de **modelos de incêndio e/ou explosão** para converter a nuvem ou vazamento em grandezas como fluxo térmico e sobrepressão;
5. aplicação de um **modelo de efeitos/vulnerabilidade**, para estimar impactos em pessoas e estruturas;
6. consideração de fatores mitigadores, como sistemas de água, espuma, evacuação e outros recursos de resposta.

Em FPSOs/FSOs, os resultados dessa modelagem servem para apoiar decisões de proteção contra incêndio, plano de contingência, arranjo físico, proteção local, análise de fuga e avaliação da severidade de cenários acidentais relevantes.

*Fontes: `petroles-4ee4bce16acf674505c8912d:pNone:1388630.0-1388671.0`, `petroles-4ee4bce16acf674505c8912d:pNone:2424687.0-2424719.0`, `regis-81b598b3e6bcc2682b8cd61e:pNone:4866.0-5062.0`*

## 2. Dados de entrada e pressupostos mínimos
A qualidade da modelagem depende diretamente da qualidade dos dados de entrada. O material destaca que é necessário dispor de informações **atualizadas** sobre os processos e instalações, incluindo, por exemplo, fluxogramas de processo, detalhes dos equipamentos e identificação dos produtos perigosos presentes.

### 2.1 Informações de processo e inventário
A análise de consequências começa pelo entendimento do sistema real que pode perder contenção. Isso inclui:
- equipamento ou trecho de linha que pode falhar;
- inventário disponível;
- estado físico da substância;
- pressão e temperatura de armazenamento/operação;
- propriedades relevantes da substância.

### 2.2 Dados meteorológicos
Para estudos de dispersão e efeitos atmosféricos, o material indica a adoção de dados meteorológicos reais do local, com base histórica mínima de vários anos, incluindo:
- temperatura ambiente;
- velocidade do vento;
- umidade relativa do ar;
- categoria de estabilidade atmosférica de Pasquill, compatível com as velocidades de vento para períodos diurno e noturno;
- direção do vento em múltiplos setores, com respectivas probabilidades de ocorrência.

Em termos práticos, isso é fundamental para modelar extensão de nuvens inflamáveis/tóxicas, inclinação de chamas e atenuação dos efeitos com a distância.

### 2.3 Topografia e rugosidade
A rugosidade da superfície representa o efeito de obstáculos do entorno — industriais, urbanos ou rurais — sobre o escoamento atmosférico. Em unidades offshore, o análogo técnico mais importante é o grau de **obstrução e congestionamento** local produzido por módulos, equipamentos, pipe-racks e anteparas, porque isso influencia dispersão, ventilação e aceleração de chama.

### 2.4 Duração do vazamento
O tempo de vazamento é determinante para a massa total liberada e, portanto, para a severidade do cenário.

O material diferencia:
- **vazamento instantâneo**: liberação em curto intervalo, típica de ruptura catastrófica, na qual a massa relevante pode ser tratada como descarregada quase de uma vez;
- **vazamento contínuo**: liberação sustentada no tempo, típica de furo, ruptura de linha alimentada ou perda de contenção antes do bloqueio.

Como diretriz de modelagem, são citados tempos-padrão associados ao tipo de bloqueio:
- bloqueio automático: cerca de **2 min**;
- bloqueio remoto com validação do operador: cerca de **10 min**;
- bloqueio manual com deslocamento ao local: cerca de **30 min**.

Esses tempos não devem ser tratados como universais; servem como referência de modelagem quando compatíveis com a filosofia de detecção e isolamento adotada.

### 2.5 Distâncias de interesse
As distâncias devem ser referidas ao ponto de liberação. O material indica, de forma geral:
- para incêndios, distâncias associadas a níveis de radiação térmica predefinidos;
- para **flash fire**, a distância associada ao envelope da nuvem na concentração do **Limite Inferior de Inflamabilidade (LII)** no momento da ignição;
- para explosão de nuvem de vapor, distâncias associadas a níveis de sobrepressão predefinidos.

Como os valores numéricos específicos desses limiares não foram preservados integralmente nos trechos recebidos, sua definição deve ser feita com base nos critérios do estudo e do projeto aplicável.

*Fontes: `petroles-4ee4bce16acf674505c8912d:pNone:2424687.0-2424719.0`*

## 3. Seleção de cenários e lógica de evolução do acidente
Após a perda de contenção, o tipo de consequência depende de uma combinação de fatores. O material lista, como fatores decisivos:
- condições iniciais do material inflamável armazenado ou em processo;
- forma de liberação;
- modo de dispersão e mistura com o ar;
- momento e modo de ignição.

Além disso, o **confinamento/congestionamento** do gás liberado é decisivo para diferenciar cenários com baixa sobrepressão daqueles com forte potencial explosivo.

Uma forma útil de organizar esse raciocínio é a **árvore de eventos**. A partir de um modo de falha, como ruptura ou furo, pode-se seguir a sequência:
1. ocorre ou não ignição imediata;
2. se não houver ignição imediata, a nuvem se dispersa, acumula ou encontra atraso de ignição;
3. havendo ignição, o resultado pode ser jet fire, flash fire, fireball/BLEVE ou explosão de nuvem de vapor, conforme mistura, atraso, confinamento e aceleração de chama.

Para FPSOs, isso é particularmente relevante porque a mesma perda de contenção pode produzir resultados muito diferentes entre:
- uma região aberta e ventilada do convés;
- uma área com forte congestionamento por equipamentos e estruturas;
- um módulo parcialmente confinado.

Por isso, o estudo de dispersão não é apenas complementar: ele reduz incertezas sobre **qual tipo de incêndio/explosão é mais plausível** e quais efeitos físicos devem ser priorizados.

*Fontes: `petroles-4ee4bce16acf674505c8912d:pNone:2444947.0-2445001.0`, `petroles-4ee4bce16acf674505c8912d:pNone:2445002.0-2445054.0`, `petroles-4ee4bce16acf674505c8912d:pNone:2448612.0-2448645.0`*

## 4. Modelagem da fonte e da dispersão
### 4.1 Modelo-fonte
O vazamento acidental normalmente se inicia pela perda do inventário contido em um equipamento ou tubulação, por ruptura ou fissura. A causa pode estar associada, entre outras, a corrosão, impacto mecânico ou erro humano. A modelagem da consequência exige descrever matematicamente a **taxa mássica de vazamento** e sua evolução temporal.

Em gases pressurizados, a velocidade de saída influencia fortemente os cenários subsequentes, em especial o jet fire. Para isso, tornam-se relevantes propriedades do material inflamável, como:
- peso molecular;
- razão de calores específicos/constante de Poisson;
- pressão e temperatura de armazenamento.

### 4.2 Dispersão atmosférica
O modelo de dispersão representa o transporte do material liberado e sua mistura com o ar. Para substâncias inflamáveis, o resultado crítico é a identificação das regiões dentro dos limites de inflamabilidade. Para substâncias tóxicas, interessa a evolução das concentrações ao longo do tempo e do espaço.

Mesmo quando não há ignição, a dispersão pode produzir consequências relevantes:
- intoxicação por inalação, se houver componentes tóxicos;
- exposição a gás quente em alta velocidade;
- lesões por fragmentos associados à ruptura do sistema.

No caso de gás natural, um dos trechos sugere que, em cenários abertos, sua menor densidade relativa ao ar pode reduzir a tendência de acúmulo ao nível da superfície. Isso pode simplificar alguns estudos específicos, mas **não deve ser generalizado** para todas as situações offshore, pois composição, temperatura, ventilação local, jato, geometrias confinadas e obstáculos podem alterar o comportamento da nuvem.

*Fontes: `petroles-4ee4bce16acf674505c8912d:pNone:2424687.0-2424719.0`, `petroles-4ee4bce16acf674505c8912d:pNone:2424871.0-2424913.0`, `petroles-4ee4bce16acf674505c8912d:pNone:2448612.0-2448645.0`*

## 5. Modelagem dos principais cenários de incêndio
## 5.1 Pool fire
O **incêndio em poça** ocorre quando um vazamento de líquido forma uma poça e esta sofre ignição. Sua severidade depende de vários parâmetros, incluindo:
- composição do hidrocarboneto;
- tamanho, forma e duração do incêndio;
- distância entre incêndio e alvo;
- características do alvo exposto.

A caracterização do cenário envolve a geometria da chama — altura, diâmetro e inclinação — e a taxa de propagação da chama sobre o líquido. Para poças maiores, a transferência de calor por radiação tende a se tornar dominante.

Aplicação prática em FPSO: cenários de pool fire são relevantes em áreas onde vazamentos líquidos podem se acumular sobre deck, bacias, pisos ou contenções locais.

## 5.2 Jet fire
O **jet fire** é típico de liberações contínuas de gases ou líquidos pressurizados que sofrem ignição. O material destaca que:
- atinge intensidade máxima quase instantaneamente;
- é afetado pela direção e velocidade do vento;
- pode ser desviado por estruturas e equipamentos próximos;
- pode impor efeitos severos por **radiação térmica** e **convecção** a estruturas vizinhas.

A velocidade do jato é parâmetro-chave para estimativa das dimensões da chama. O texto também menciona o fenômeno de **lift-off**, entendido como a separação entre o ponto de liberação e o início visível da chama, causado pela velocidade e concentração do gás próximos à origem. Em grandes liberações, pode haver uma fase transitória de fireball seguida pelo estabelecimento de um jet fire quase estacionário.

Em FPSOs, o jet fire é um dos cenários mais críticos para integridade local de equipamentos, tubulações, suportes estruturais e rotas de fuga próximas ao vazamento.

## 5.3 Flash fire
O **flash fire** é a queima de uma nuvem inflamável com **sobrepressão desprezível ou não significativa**, usualmente em região não confinada ou pouco obstruída. Seus perigos principais são:
- contato direto com a chama;
- efeitos térmicos da combustão sobre pessoas inseridas na nuvem.

A área relevante do fenômeno é a porção da nuvem dentro dos limites de inflamabilidade; por isso, a modelagem de dispersão e o contorno em **LII** são centrais. Em geral, flash fire tende a causar menos dano estrutural que uma explosão, mas pode ser severo para pessoas expostas diretamente.

## 5.4 BLEVE e fireball
O **BLEVE** (Boiling Liquid Expanding Vapor Explosion) está associado à falha catastrófica de um vaso contendo líquido superaquecido ou liquefeito inflamável sob pressão. O fenômeno pode decorrer de:
- aquecimento externo por incêndio e consequente perda de resistência da parede do vaso;
- elevação de temperatura/pressão interna, mesmo com atuação de alívio;
- falha estrutural por degradação, como corrosão.

As consequências principais mencionadas são:
- **sobrepressão** pela expansão rápida;
- **radiação térmica intensa** da fireball;
- **fragmentos do recipiente** projetados a distância.

Em estudos de segurança, BLEVE exige atenção especial a recipientes pressurizados, inventário líquido sob pressão, exposição externa ao fogo e potencial de efeito dominó.

*Fontes: `petroles-4ee4bce16acf674505c8912d:pNone:2424871.0-2424913.0`, `petroles-4ee4bce16acf674505c8912d:pNone:2445002.0-2445054.0`, `petroles-4ee4bce16acf674505c8912d:pNone:2448612.0-2448645.0`*

## 6. Modelagem de explosões de nuvem de vapor
A explosão de nuvem de vapor é descrita como a ignição de uma nuvem combustível pré-misturada com ar, capaz de gerar rápido aumento de pressão. A distinção essencial entre **flash fire** e **VCE/CVCE** é a magnitude da sobrepressão produzida.

Condições necessárias destacadas no material:
- o material liberado deve ser inflamável e estar em condições adequadas;
- a nuvem deve atingir dimensão suficiente antes da ignição retardada;
- parcela relevante da nuvem deve estar dentro da região de inflamabilidade;
- confinamento, congestionamento, turbulência e proximidade da estequiometria favorecem aceleração da chama e aumento da sobrepressão.

### 6.1 Deflagração e detonação
Os trechos diferenciam:
- **deflagração**: propagação subsônica da chama, com aumento de pressão moderado;
- **detonação**: propagação supersônica com forte onda de choque.

Em misturas gasosas em espaços confinados, o termo **CVCE** é citado para explosão em nuvem de vapor confinado, na qual deflagração acelerada ou detonação podem ocorrer conforme as condições.

### 6.2 Relação com confinamento e obstrução
O material enfatiza que ambientes parcial ou fortemente confinados/obstruídos oferecem condições apropriadas para combustão explosiva. Isso é diretamente aplicável a módulos de processo em FPSO, nos quais o arranjo de equipamentos influencia fortemente a severidade da explosão.

### 6.3 Métodos semiquantitativos
Um dos trechos menciona o **método Multi-Energia**, assumindo mistura estequiométrica no volume livre relevante. A utilidade prática desse tipo de método é estimar distâncias de dano por sobrepressão em cenários com nuvens inflamáveis confinadas ou parcialmente confinadas. O uso, porém, depende da consistência entre a hipótese do método e a geometria/ventilação reais da instalação.

*Fontes: `petroles-4ee4bce16acf674505c8912d:pNone:1388630.0-1388671.0`, `petroles-4ee4bce16acf674505c8912d:pNone:2445002.0-2445054.0`, `petroles-4ee4bce16acf674505c8912d:pNone:2448612.0-2448645.0`, `petroles-4ee4bce16acf674505c8912d:pNone:727215.0-727266.0`*

## 7. Efeitos físicos: radiação térmica, sobrepressão e vulnerabilidade
A estimativa de consequências não se encerra no tamanho da nuvem ou no tipo de evento; ela precisa traduzir o fenômeno físico em dano potencial.

### 7.1 Radiação térmica
Os trechos fornecem a estrutura conceitual de cálculo baseada em **Surface Emissive Power (SEP)** da chama.

De forma conceitual:
- o **SEP máximo** depende da energia liberada na combustão por unidade de tempo, da área superficial da chama e da fração radiada;
- o **SEP atual** considera o efeito de fuligem/fumaça cobrindo parte da superfície da chama;
- o **fluxo de calor incidente** em um receptor depende do SEP atual, do **fator de vista** e da **transmissividade atmosférica**.

Em termos operacionais, isso significa que a severidade térmica sobre uma pessoa, parede, vaso, tubulação ou suporte estrutural não depende apenas da potência do incêndio, mas também de:
- geometria relativa entre chama e alvo;
- distância;
- orientação;
- atenuação atmosférica;
- obscurecimento por fuligem.

### 7.2 Sobrepressão
Na explosão de nuvem de vapor, o parâmetro dominante é a **sobrepressão**. Ela é usada para estimar:
- danos estruturais;
- lesões em pessoas;
- alcance de zonas de efeito.

Um dos trechos cita, em contexto de estudo de caso, danos como colapso estrutural, hemorragia pulmonar e ruptura de tímpanos como estados de dano avaliados em função da distância ao centro da explosão.

### 7.3 Contato com chama, fumaça, toxicidade e fragmentos
Além da radiação e da sobrepressão, os materiais citam:
- contato direto com chama, especialmente relevante em flash fire;
- fumaça e produtos de combustão, apontados como tema que pode precisar ser incluído explicitamente em análises futuras;
- fragmentos de vasos ou componentes rompidos, relevantes em BLEVEs e falhas catastróficas.

### 7.4 Vulnerabilidade de receptores
Após obter os campos físicos de efeito, a análise deve avaliar a vulnerabilidade de receptores humanos, equipamentos, estruturas e, quando pertinente, meio ambiente, com base em **limites de tolerância ou critérios de dano predefinidos**. O material recebido não preserva todos os limiares numéricos, mas deixa claro que essa conversão é parte obrigatória da análise de consequências.

*Fontes: `petroles-4ee4bce16acf674505c8912d:pNone:2424687.0-2424719.0`, `petroles-4ee4bce16acf674505c8912d:pNone:2424871.0-2424913.0`, `petroles-4ee4bce16acf674505c8912d:pNone:727215.0-727266.0`, `regis-81b598b3e6bcc2682b8cd61e:pNone:4866.0-5062.0`*

## 8. Efeitos sobre pessoas e instalações em FPSO/FSO
Em unidades offshore, a modelagem de consequências deve ser lida à luz de dois objetivos simultâneos:
1. proteger pessoas contra exposição letal ou incapacitante;
2. preservar a integridade da instalação e evitar escalonamento do acidente.

O material menciona como fontes de perigo importantes em plataformas offshore, entre outras:
- dutos de óleo;
- dutos de gás;
- separadores;
- unidades de bombeamento;
- flash drum;
- unidades de compressão.

A severidade resultante de incêndio e explosão pode ser usada para:
- identificar unidades prioritárias para redução de risco;
- comparar projetos de melhoria;
- justificar rearranjo de layout;
- reforçar proteção contra incêndios;
- revisar planos de contingência;
- reavaliar rotas de fuga e saídas de emergência.

Um estudo citado no material, focado em **jet fire**, concluiu que, em certos casos, o tempo disponível para fuga era muito baixo, indicando necessidade de reconsiderar saídas de emergência e proteções locais. Essa é uma aplicação típica da modelagem de consequências em FPSO: não apenas quantificar dano, mas converter o resultado em decisão de engenharia e de resposta a emergências.

*Fontes: `petroles-4ee4bce16acf674505c8912d:pNone:2394582.0-2394628.0`, `regis-81b598b3e6bcc2682b8cd61e:pNone:4866.0-5062.0`, `petroles-4ee4bce16acf674505c8912d:pNone:1388630.0-1388671.0`*

## 9. Limitações práticas e cuidados de interpretação
Os próprios trechos indicam limitações relevantes da modelagem de consequências:
- modelos simplificados podem tratar apenas um tipo de incêndio, deixando de fora outros cenários relevantes;
- a análise pode focar apenas em pessoas, sem quantificar impactos térmicos sobre equipamentos e estruturas;
- fumaça e produtos de combustão podem estar subrepresentados;
- validação experimental e análise de incertezas são desejáveis;
- cenários e resultados dependem fortemente das hipóteses adotadas.

Portanto, em estudos de segurança de FPSO/FSO, a modelagem de consequências deve ser entendida como ferramenta de decisão técnica, não como valor absoluto independente do contexto. Sua credibilidade depende de hipóteses rastreáveis, seleção coerente de cenários, dados de entrada representativos e integração com o restante do estudo de risco.

*Fontes: `regis-81b598b3e6bcc2682b8cd61e:pNone:4866.0-5062.0`, `petroles-4ee4bce16acf674505c8912d:pNone:1388630.0-1388671.0`*