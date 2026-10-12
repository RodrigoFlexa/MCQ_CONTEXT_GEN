# Remoção de sulfato em sistemas de água do mar para injeção em reservatórios a partir de FPSOs

## 1. Finalidade técnica da SRU/URS no sistema de injeção

A unidade de remoção de sulfato (SRU/URS) integra o sistema de tratamento de água do mar para injeção quando se deseja **reduzir a concentração de íons sulfato da água de injeção** antes do contato dessa água com a água de formação. O objetivo operacional principal é permitir a manutenção de pressão do reservatório com menor risco de incompatibilidade química, incrustação e souring, preservando também a injetividade e a confiabilidade dos equipamentos de superfície e subsea.

Em campos offshore, a água do mar é usualmente escolhida pela disponibilidade. Porém, sua injeção sem tratamento pode causar incompatibilidade com a água de formação, especialmente quando esta é rica em **bário, estrôncio e cálcio**, favorecendo a precipitação de sais como **BaSO4, SrSO4 e CaSO4**. Esses sólidos podem se depositar no reservatório, em poços e em equipamentos sujeitos a mistura de águas e queda de pressão, reduzindo permeabilidade, vazão e eficiência operacional. Um benefício adicional da redução de sulfato é a **menor propensão ao souring**, por reduzir a disponibilidade de sulfato para bactérias redutoras de sulfato (BRS), associadas à geração de H2S.

Além do controle de incrustação, a dessulfatação por membranas é usada para manter a água de injeção com salinidade ainda relevante para o reservatório, pois a nanofiltração usada em SRUs tende a permitir a passagem de NaCl em grau maior que a de sulfato. Isso é desejável para evitar efeitos indesejados como inchamento de argilas por água excessivamente dessalinizada.

**Fontes da seção:** `petroles-004c2afadba7ea17c7dd7908:pNone:4363791.0-4363824.0`, `regis-9f1e60c0f9bdef2ea4d052ec:pNone:2242.0-2466.0`, `regis-bf91aa7b5bfc30625dd6306a:pNone:3454.0-3672.0`

## 2. Encadeamento típico do tratamento até a SRU

Uma arquitetura típica, conforme os trechos fornecidos, segue a lógica abaixo:

1. **Captação de água do mar** por bombas centrífugas.
2. **Condicionamento químico inicial**, com adição de agente oxidante/biocida para controle de matéria orgânica e organismos vivos.
3. **Filtração primária**, para reduzir sólidos e proteger as membranas.
4. **Pressurização por bomba booster**, para vencer perdas de carga e fornecer a energia hidráulica do processo de nanofiltração.
5. **Trem de membranas de nanofiltração**, onde ocorre a remoção seletiva do sulfato.
6. **Desaeração** antes ou depois da SRU, conforme arranjo de projeto.
7. **Condicionamento químico final** e envio para bombas de injeção.

O desempenho da SRU depende fortemente da qualidade do pré-tratamento. A membrana de nanofiltração é seletiva, mas é sensível a partículas, incrustação, biofouling e oxidação química. Por isso, a SRU deve ser vista como um sistema integrado, não apenas como o skid de membranas.

**Fontes da seção:** `regis-bf91aa7b5bfc30625dd6306a:pNone:3454.0-3672.0`, `regis-bf91aa7b5bfc30625dd6306a:pNone:3568.0-3779.0`, `regis-bf91aa7b5bfc30625dd6306a:pNone:3781.0-4000.0`, `regis-9f1e60c0f9bdef2ea4d052ec:pNone:2242.0-2466.0`

## 3. Pré-tratamento: papel na proteção da SRU

### 3.1 Filtração grossa e fina

Os trechos descrevem um pré-tratamento em múltiplas barreiras:

- **Filtro grosso / coarse filter**: remove partículas maiores, com faixa reportada de retenção entre aproximadamente **80 e 25 µm**, por ação de filtro rotativo autolimpante com retrolavagem interna.
- **Filtro fino / fine filter de cartucho**: remove partículas finas da ordem de **5 µm**, em vaso de pressão com cartuchos e cestos de suporte, atuando como polimento da água para proteção da membrana de nanofiltração.
- Em alguns arranjos, há ainda um **media filter** intermediário entre o filtro grosso e o fino.

A filosofia de confiabilidade descrita inclui **filtros em standby**, permitindo manutenção ou troca sem parar o tratamento. Para o operador, o indicador mais imediato do estado desses equipamentos é o **diferencial de pressão**, usado tanto para acionar limpeza do filtro grosso como para definir a troca dos elementos do filtro fino quando o limite do fabricante é excedido.

### 3.2 Consequências do pré-tratamento deficiente

Se o pré-tratamento não remove adequadamente sólidos, coloides, material orgânico e organismos vivos, a SRU tende a sofrer:

- **polarização por concentração** na vizinhança da membrana;
- **fouling** após estabilização do fluxo;
- aumento de perda de carga;
- redução do fluxo de permeado;
- maior passagem de íons indesejados;
- menor vida útil de membranas.

Nos processos com membranas, o permeado é a corrente que atravessa a membrana, enquanto o concentrado/rejeito é a corrente enriquecida em solutos rejeitados. Em qualquer SRU, a qualidade do permeado depende da seletividade da membrana, mas também da estabilidade hidrodinâmica e química do lado da alimentação.

**Fontes da seção:** `regis-bf91aa7b5bfc30625dd6306a:pNone:3454.0-3672.0`, `regis-bf91aa7b5bfc30625dd6306a:pNone:3568.0-3779.0`, `regis-6ec5548c441f38209b8b0809:pNone:1811.0-2073.0`

## 4. Princípio de remoção de sulfato por nanofiltração

A remoção de sulfato na SRU é descrita como um processo de **nanofiltração (NF)**, impulsionado por diferença de pressão hidráulica. Em termos gerais, a NF situa-se entre ultrafiltração e osmose inversa quanto ao tamanho de poros e à pressão requerida; o material de referência traz, para NF genérica, faixa de **0,5 a 10 nm** e **5 a 25 atm** como diferença de pressão, embora os valores reais de uma SRU offshore dependam do projeto e do fabricante.

Na aplicação de SRU, as membranas poliméricas compostas foram originalmente derivadas de tecnologias de dessalinização, mas empregadas de forma seletiva para **reter íons multivalentes**, principalmente sulfato, sem remover totalmente NaCl. O mecanismo descrito combina:

- **efeito de tamanho de poro**, com poros da ordem de **10 Å** no estudo citado;
- **efeito eletrostático**, com superfície de membrana negativamente carregada;
- escoamento tangencial que ajuda a reduzir acúmulo local de solutos.

Os trechos informam, como explicação do mecanismo seletivo, que:

- o **cloreto** teria diâmetro aproximado de **1,8 Å** e carga negativa simples, conseguindo atravessar a membrana em alta fração;
- o **sulfato** teria diâmetro aproximado de **2,4 Å** e carga negativa dupla, sofrendo rejeição mais intensa;
- cátions pequenos como **Na+** e **Mg2+** tenderiam a atravessar em grau suficiente para manter neutralidade elétrica.

Assim, a SRU produz uma água dessulfatada que preserva parte relevante da salinidade, o que é tecnicamente útil para injeção em formações sensíveis.

### 4.1 Desempenho típico reportado

Os valores citados nos materiais indicam, como referências históricas de desempenho:

- água do mar com cerca de **2700 mg/L de sulfato**;
- redução inicial para **100 a 150 mg/L**;
- evolução posterior de membranas permitindo cerca de **50 mg/L**;
- rejeição de sulfato de até **99%** em membranas mais evoluídas;
- passagem de cloreto da ordem de **95%**.

Também é reportada redução de pressão operacional de cerca de **400 psi para 250 psi** com evolução tecnológica de membranas, além de aumento de área superficial por elemento de **320 ft² para 400 ft²**, reduzindo a quantidade de vasos necessária para uma dada capacidade.

Esses números são úteis como referência de ordem de grandeza e de tendência tecnológica, não como especificações universais.

**Fontes da seção:** `regis-bf91aa7b5bfc30625dd6306a:pNone:3568.0-3779.0`, `regis-6ec5548c441f38209b8b0809:pNone:1811.0-2073.0`, `regis-9f1e60c0f9bdef2ea4d052ec:pNone:2242.0-2466.0`

## 5. Arranjo hidráulico e configuração dos módulos

A SRU depende de fornecimento adequado de energia hidráulica. Os trechos descrevem:

- **bombas de captação** de água do mar, tipicamente centrífugas, com arranjo vertical e pressão de trabalho da ordem de **4 a 6 atm**;
- **bombas booster**, destinadas a superar perdas de carga e fornecer a pressão para a nanofiltração;
- **bombas de injeção**, posteriormente, para elevar a água tratada à pressão de injeção do poço.

Para a etapa de NF, as membranas são descritas em configuração **espiralada**, favorecendo alta área por volume instalado. Os módulos são inseridos em vasos e organizados em estágios; um arranjo citado é o de **dois vasos para um** entre estágios, em que o rejeito do primeiro conjunto segue para o segundo. Essa organização busca manter vazão tangencial suficiente para um efeito de **auto-limpeza hidrodinâmica**, reduzindo a deposição de sais e sólidos na superfície da membrana.

Na prática operacional, isso significa que o desempenho da SRU não deve ser avaliado apenas pela concentração de sulfato na água tratada. É igualmente crítico observar se o arranjo está mantendo:

- vazão de alimentação adequada em cada trem;
- distribuição homogênea entre vasos;
- rejeito suficiente para varredura da superfície da membrana;
- pressão compatível com a recuperação desejada sem acelerar fouling e scaling.

**Fontes da seção:** `regis-bf91aa7b5bfc30625dd6306a:pNone:3568.0-3779.0`, `regis-bf91aa7b5bfc30625dd6306a:pNone:3781.0-4000.0`

## 6. Indicadores de desempenho da SRU para operação e otimização

Com base nos materiais fornecidos, a avaliação do desempenho da SRU deve considerar simultaneamente qualidade da água, integridade das membranas e estabilidade operacional.

### 6.1 Indicadores de qualidade da água tratada

Os principais indicadores inferidos para a SRU são:

- **concentração de sulfato no permeado/água tratada**;
- **preservação de salinidade adequada**, especialmente pela passagem de NaCl;
- teor de sólidos após pré-filtragem, para proteção do sistema;
- **teor de oxigênio dissolvido** quando a desaeração integra o mesmo sistema de tratamento.

No contexto do reservatório, a qualidade da água tratada deve ser compatível com a formação para minimizar:

- precipitação de sulfatos de bário, estrôncio e cálcio;
- redução de permeabilidade e injetividade;
- souring associado a BRS;
- corrosão induzida por oxigênio e atividade microbiológica.

### 6.2 Indicadores de desempenho do processo de membranas

Os sinais operacionais mais relevantes são:

- **queda de fluxo de permeado**;
- aumento do **diferencial de pressão** em filtros e trens;
- necessidade crescente de pressão para manter produção de água tratada;
- aumento da passagem de íons que deveriam ser rejeitados;
- frequência crescente de limpeza química.

Os materiais diferenciam dois mecanismos importantes:

- **polarização**: concentração de soluto junto à membrana diferente da concentração no seio do fluido, com redução do fluxo de permeado;
- **fouling**: diminuição de fluxo persistente após estabilização, associada a deposição/aderência na membrana.

### 6.3 Compromisso operacional entre recuperação e incrustação

Os materiais de dessalinização por membranas mostram um trade-off útil para SRUs: **quanto maior a recuperação de água, menor o volume de concentrado, porém maior a concentração iônica no rejeito**, elevando o risco de ultrapassar limites metaestáveis e formar incrustações. Isso afeta recuperação, membranas, bombas e tubulações.

Para fins de otimização, portanto, a SRU deve operar em um ponto em que a redução de sulfato seja alcançada sem elevar excessivamente a tendência à incrustação no lado concentrado nem comprometer a autolimpeza dos módulos.

**Fontes da seção:** `regis-bf91aa7b5bfc30625dd6306a:pNone:3454.0-3672.0`, `regis-bf91aa7b5bfc30625dd6306a:pNone:3568.0-3779.0`, `petroles-004c2afadba7ea17c7dd7908:pNone:4363791.0-4363824.0`, `regis-607ef7883aeb407548bf695c:pNone:3501.0-3695.0`, `regis-9f1e60c0f9bdef2ea4d052ec:pNone:2242.0-2466.0`

## 7. Químicos associados à operação da SRU

Os trechos indicam que a SRU não opera isoladamente das rotinas de dosagem química. São mencionadas três finalidades principais:

1. **Biocidas**, para prevenção e remoção de proliferação biológica.
2. **Inibidores de incrustação**, para reduzir a formação de sais insolúveis sobre membranas e no sistema.
3. **Sequestrante de cloro**, para evitar oxidação da superfície das membranas pelo cloro livre.

Há também referência à adição inicial de **hipoclorito de sódio** para eliminação de matéria orgânica e organismos vivos na água captada. Isso reforça a necessidade de controle rigoroso da química ao longo do sistema: produtos úteis a montante podem ser danosos às membranas se não houver neutralização adequada antes da NF.

A configuração usual citada para o skid químico inclui tanques, instrumentos e bombas dosadoras, com materiais compatíveis com cada produto. A dosagem é operacionalmente relevante para o desempenho da SRU porque influencia diretamente:

- controle microbiológico;
- integridade química da membrana;
- taxa de incrustação;
- frequência de limpeza;
- estabilidade da rejeição de sulfato.

Em campos com alto potencial de precipitação de sulfatos, a literatura citada também posiciona a URS como alternativa ou complemento ao uso intensivo de inibidores químicos, sobretudo quando a prevenção apenas por químicos se torna complexa ou onerosa.

**Fontes da seção:** `regis-bf91aa7b5bfc30625dd6306a:pNone:3454.0-3672.0`, `regis-bf91aa7b5bfc30625dd6306a:pNone:3781.0-4000.0`, `petroles-004c2afadba7ea17c7dd7908:pNone:1063945.0-1063980.0`

## 8. Integração com desaeração e controle de oxigênio

A presença de oxigênio dissolvido na água de injeção é descrita como indesejável por favorecer:

- **corrosão**;
- atividade de bactérias e microrganismos relacionados ao sistema de injeção;
- geração de H2S em condições associadas a microrganismos redutores de sulfato.

A coluna desaeradora pode ser instalada **antes da pré-filtragem ou após a remoção de sulfato**, conforme o arranjo. O princípio descrito envolve distribuição da água pelo topo do vaso e uso de vácuo para reduzir a pressão parcial de oxigênio, transferindo-o da água para a fase gasosa. Os trechos indicam que as desaeradoras usualmente reduzem o oxigênio para **menos de 10 a 50 ppb**, havendo também referência a água pronta para injeção com **menos de 10 ppb**.

Do ponto de vista da SRU, a posição relativa entre desaerador e membranas afeta o projeto. Há menção de que, se a URS estiver **a montante da desaeradora**, deve ser projetada para trabalhar com aproximadamente **8 ppm de oxigênio** presente. Isso implica exigências de materiais e de controle químico mais severas.

Em termos de avaliação operacional, a decisão de posicionamento influencia:

- seleção de materiais construtivos;
- risco corrosivo no skid de membranas;
- estratégia de dosagem química;
- pressão de trabalho dos equipamentos.

**Fontes da seção:** `regis-bf91aa7b5bfc30625dd6306a:pNone:3781.0-4000.0`, `regis-9f1e60c0f9bdef2ea4d052ec:pNone:2242.0-2466.0`, `petroles-004c2afadba7ea17c7dd7908:pNone:4363791.0-4363824.0`

## 9. Degradação de desempenho: polarização, fouling e incrustação

### 9.1 Polarização e fouling

Os materiais destacam polarização e fouling como desvantagens importantes dos processos com membranas.

- **Polarização por concentração**: ocorre quando a concentração de soluto na vizinhança da membrana se torna diferente da concentração no volume principal do fluido, reduzindo o fluxo de permeado.
- **Fouling**: é a perda adicional de desempenho associada a deposição após a estabilização inicial.

Esses fenômenos elevam o consumo energético, reduzem a produção de água tratada e podem aumentar a passagem de solutos, degradando o desempenho da SRU.

### 9.2 Incrustação inorgânica

No contexto da SRU e do reservatório, a incrustação tem dois planos distintos:

1. **no reservatório e sistema de produção/injeção**, pela mistura entre águas incompatíveis;
2. **na própria unidade de membranas**, quando a concentração no concentrado e junto à superfície da membrana cresce a ponto de favorecer precipitação.

Os materiais indicam que incrustações em sistemas de membranas reduzem fluxo, aumentam passagem de íons, prejudicam vida útil e podem danificar bombas e tubulações. A tendência aumenta com maior recuperação e maior concentração do rejeito. Em reservatórios e linhas, a incrustação pode provocar obstrução parcial ou total, além de colaborar com corrosão ao aprisionar bactérias na superfície metálica.

### 9.3 O que observar na operação

Sinais típicos de piora do desempenho da SRU incluem:

- necessidade de maior pressão para mesma produção de permeado;
- redução progressiva de vazão tratada;
- piora da qualidade do permeado quanto a sulfato;
- aumento de perda de carga em filtros e trens;
- encurtamento do intervalo entre limpezas.

**Fontes da seção:** `regis-bf91aa7b5bfc30625dd6306a:pNone:3454.0-3672.0`, `petroles-004c2afadba7ea17c7dd7908:pNone:4363791.0-4363824.0`, `regis-607ef7883aeb407548bf695c:pNone:3501.0-3695.0`, `regis-9f1e60c0f9bdef2ea4d052ec:pNone:2242.0-2466.0`

## 10. Limpeza, manutenção e continuidade operacional

Os materiais descrevem um **sistema integrado de limpeza das membranas**, destinado a prolongar a vida útil, reportada no trecho como podendo chegar a **cerca de 3 anos**. Esse sistema inclui:

- tanque de preparo/armazenamento da solução de limpeza;
- bomba centrífuga;
- filtro cartucho de limpeza;
- recirculação da solução pelo trem de membranas.

A limpeza é normalmente feita **por trens de membranas**, e não em toda a unidade simultaneamente, para que a remoção de sulfato da água do mar não seja totalmente interrompida. Esse aspecto é importante para FPSOs, em que a disponibilidade do sistema de injeção é diretamente ligada à estratégia de manutenção de pressão do reservatório.

O filtro do sistema de limpeza é descrito como semelhante ao fine filter e remove partículas maiores que **5 µm**. A solução retorna ao tanque para nova interação com água e produtos químicos de limpeza, enquanto o rejeito segue para header apropriado.

Do ponto de vista de avaliação de desempenho, uma frequência anormal de limpeza ou recuperação insuficiente de desempenho após limpeza sugere problemas mais profundos, como:

- inadequação do pré-tratamento;
- dosagem química insuficiente ou excessiva;
- regime hidráulico inadequado de escoamento tangencial;
- dano químico irreversível à membrana.

**Fontes da seção:** `regis-bf91aa7b5bfc30625dd6306a:pNone:3781.0-4000.0`, `regis-bf91aa7b5bfc30625dd6306a:pNone:3568.0-3779.0`

## 11. Critérios práticos para avaliar operação e otimizar a SRU

Com base nos trechos disponíveis, a avaliação profissional da SRU pode ser estruturada pelos seguintes critérios:

### 11.1 Critérios de qualidade da água para mitigação de risco no reservatório

A SRU está desempenhando sua função quando a água tratada apresenta teor de sulfato suficientemente baixo para reduzir o risco de precipitação com cátions da água de formação e, ao mesmo tempo, preserva salinidade compatível com o reservatório.

### 11.2 Critérios de integridade do processo

A operação é estável quando:

- o pré-tratamento mantém partículas fora da faixa crítica para membranas;
- o diferencial de pressão dos filtros permanece sob controle;
- a pressão requerida pela NF não cresce continuamente;
- a vazão tangencial e a varredura do rejeito são suficientes para reduzir deposição;
- a frequência de limpeza é compatível com o histórico e com o projeto.

### 11.3 Critérios de decisão entre tratamento químico e dessulfatação

Os materiais indicam que a URS tende a ser mais justificável quando há:

- alto potencial de precipitação de sulfatos no reservatório;
- presença relevante de bário/estrôncio/cálcio na água de formação;
- preocupação com souring;
- cenários offshore profundos/subsea em que controle por inibidores pode ser caro ou logisticamente complexo;
- necessidade de reduzir dependência de altas doses de químicos.

### 11.4 Limitações de projeto que afetam a decisão

Nem todas as plataformas possuem SRU, principalmente por **restrições de espaço, peso e planejamento de projeto**. Portanto, a decisão de incluir ou ampliar uma SRU depende não só do risco geoquímico, mas também da capacidade topside de acomodar filtros, bombas, vasos de membranas, sistema de limpeza e utilidades associadas.

**Fontes da seção:** `regis-9f1e60c0f9bdef2ea4d052ec:pNone:2242.0-2466.0`, `petroles-004c2afadba7ea17c7dd7908:pNone:1063945.0-1063980.0`, `regis-bf91aa7b5bfc30625dd6306a:pNone:3568.0-3779.0`, `regis-bf91aa7b5bfc30625dd6306a:pNone:3781.0-4000.0`

## 12. Síntese operacional

Em FPSOs, a SRU deve ser entendida como uma **barreira de compatibilidade geoquímica** entre a água do mar e o reservatório. Seu sucesso não depende apenas da membrana, mas da combinação entre:

- pré-filtragem robusta;
- pressurização adequada;
- membranas seletivas e bem distribuídas em trens/vasos;
- controle de oxigênio e de microbiologia;
- dosagem química coerente com a sensibilidade das membranas;
- limpeza por condição e manutenção da disponibilidade.

Quando bem operada, a SRU reduz sulfato a níveis muito inferiores aos da água do mar, preserva a salinidade útil da água de injeção e mitiga riscos de **incrustação, souring, corrosão indireta e perda de injetividade**. Quando mal operada, os sintomas mais prováveis são queda de fluxo, aumento de pressão, maior passagem de sulfato, maior necessidade de limpeza e redução de confiabilidade do sistema de injeção.

**Fontes da seção:** `regis-bf91aa7b5bfc30625dd6306a:pNone:3454.0-3672.0`, `regis-bf91aa7b5bfc30625dd6306a:pNone:3568.0-3779.0`, `regis-bf91aa7b5bfc30625dd6306a:pNone:3781.0-4000.0`, `regis-9f1e60c0f9bdef2ea4d052ec:pNone:2242.0-2466.0`, `petroles-004c2afadba7ea17c7dd7908:pNone:4363791.0-4363824.0`