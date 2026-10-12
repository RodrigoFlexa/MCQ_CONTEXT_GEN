# Água do mar e utilidades térmicas

## 1. Escopo técnico e arquitetura típica
Em FPSOs/FSOs e outras UEPs offshore, a utilidade de água do mar costuma exercer dois papéis centrais nesta faceta: **fornecer água bruta para serviços** e **atuar como sumidouro térmico** para sistemas fechados de água de resfriamento. Os trechos também mostram a interface da água do mar com **eletrocloração/hipoclorito** para controle microbiológico e, em outro contexto, com **tratamento de água para injeção**.

Os arranjos descritos não são idênticos entre si, mas convergem para uma filosofia comum:
- captação por **caixas de mar** e **bombas centrífugas verticais**;
- distribuição da água do mar para consumidores utilitários e de processo;
- uso de **trocadores de placas** para remover calor de um **circuito fechado de água doce** de resfriamento;
- segregação de consumidores, em alguns casos, entre **área classificada** e **área não classificada**;
- uso de **vaso/tanque de expansão**, **bombas de circulação**, **filtros** e, quando aplicável, **linha de by-pass**.

Fontes da seção: `petroles-004c2afadba7ea17c7dd7908:pNone:388734.0-388774.0`, `petroles-004c2afadba7ea17c7dd7908:pNone:2160438.0-2160505.0`, `petroles-004c2afadba7ea17c7dd7908:pNone:2160506.0-2160541.0`, `petroles-004c2afadba7ea17c7dd7908:pNone:511961.0-511995.0`

## 2. Captação e distribuição de água do mar
Os materiais mostram arranjos offshore com **múltiplas caixas de mar** e **redundância de bombas**. Em uma descrição, a água do mar é captada em **duas caixas de mar** por **pelo menos cinco bombas**, ficando **uma em reserva**. Em outra, a captação ocorre por **seis caixas de mar** com bombas elétricas verticais, além de bombas de emergência. Isso sugere que a filosofia de redundância é fortemente dependente da instalação e do balanço de consumidores.

A água do mar captada pode alimentar:
- trocadores de placas dos sistemas de água de resfriamento;
- sistema de injeção de água;
- sistema de combate a incêndio;
- utilidades diversas, como postos de limpeza, unidade de eletrocloração, tratamento de esgoto e dessalinização.

Do ponto de vista de projeto e operação, os pontos críticos são:
1. **Disponibilidade hidráulica** para demanda normal e de pico.
2. **Segregação de consumidores críticos**, evitando que uma única perda de capacidade comprometa toda a planta.
3. **Reserva e emergência**, especialmente quando a água do mar atende simultaneamente resfriamento, serviços e outras funções essenciais.
4. **Proteção contra entrada de sólidos e organismos**, porque a água do mar alimenta diretamente equipamentos sujeitos a fouling e biofouling.

Em referência conceitual adicional, um sistema de refrigeração em circuito aberto com água do mar requer infraestrutura de **captação** e **descarga**, e a tomada d’água deve reduzir a passagem de areia grossa e sólidos para o circuito. Embora o trecho seja de instalação costeira em terra, o princípio é útil: a qualidade da água captada influencia diretamente desgaste, incrustação, perda de carga e desempenho térmico.

Fontes da seção: `petroles-004c2afadba7ea17c7dd7908:pNone:388734.0-388774.0`, `petroles-004c2afadba7ea17c7dd7908:pNone:2160438.0-2160505.0`, `regis-d55109174fd64e1fa1a0bdd0:pNone:8715.0-8908.0`

## 3. Sistema de água de resfriamento: circuito fechado com rejeição ao mar
Os trechos descrevem, como solução recorrente offshore, **sistemas fechados de água doce** que removem calor dos consumidores e o rejeitam à água do mar por meio de **trocadores de placas**. Em uma instalação, existem **dois sistemas independentes**, um para área classificada e outro para área não classificada, com a mesma concepção básica.

A arquitetura funcional é:
- **header de distribuição** para os consumidores;
- **header de retorno** trazendo a água aquecida;
- **vaso de expansão**, cuja função principal é absorver as flutuações volumétricas do circuito;
- **filtro** em derivação ou na circulação, reduzindo sólidos e produtos de corrosão no loop;
- **bombas de circulação** principais e, em alguns casos, bombas de emergência;
- **permutador/trocador de placas**, onde a água doce do circuito fechado troca calor com a água do mar.

O material do aplicativo SAGRES reforça que o dimensionamento começa pela definição do tipo de circuito para áreas classificadas e não classificadas: um deles pode ser **fechado em água doce**, e outro, dependendo da solução adotada, pode ser **aberto em água do mar**. O aplicativo também considera:
- perfil de temperaturas e approach térmico;
- cadastramento detalhado dos consumidores;
- cálculo de perda de carga por trechos e acidentes;
- dimensionamento de linha de by-pass com base nas bombas em operação;
- dimensionamento do vaso de expansão com base no inventário total de água circulante, incluindo volume retido em equipamentos, quando aplicável;
- especificação de bombas normais e de emergência;
- consolidação do balanço global do sistema.

Os consumidores térmicos citados incluem, com destaque, **compressores**, que aparecem como os maiores geradores de carga térmica para o sistema. Também são citados compressor de ar de instrumento, compressor de ar de partida, unidade de glicol, bombas de injeção de água, bombas de água quente, turbinas dos turbogeradores, refrigeração e ar condicionado.

Implicações práticas:
- elevação da temperatura de retorno, com temperatura de suprimento mantida, indica aumento de carga térmica ou queda de vazão;
- aumento de perda de carga no circuito sugere obstrução, fouling, filtro carregado ou problema de alinhamento;
- degradação do trocador de placas reduz a capacidade de rejeição ao mar e tende a elevar a temperatura de todos os consumidores dependentes do loop.

Fontes da seção: `petroles-004c2afadba7ea17c7dd7908:pNone:388734.0-388774.0`, `petroles-004c2afadba7ea17c7dd7908:pNone:2160506.0-2160541.0`, `petroles-004c2afadba7ea17c7dd7908:pNone:511961.0-511995.0`

## 4. Avaliação de capacidade, balanço de consumidores e turndown
A demanda total de água de resfriamento é obtida pela **soma dos consumidores**. O material indica que essa demanda pode ser tratada por **carga térmica**, **vazão volumétrica** ou **vazão mássica**, e que fatores de correção podem ser aplicados por consumidor. Também é possível montar **casos operacionais distintos**, por exemplo cenários de máxima água, máximo gás ou diferentes BSWs.

Isso é relevante para FPSOs porque a carga térmica muda com:
- composição do fluido produzido;
- regime dos compressores;
- número de consumidores em serviço;
- temperatura da água do mar;
- indisponibilidade de bombas ou trocadores.

Boas decisões de projeto e operação incluem:
- separar o cálculo de **caso normal**, **caso de pico** e **caso degradado**;
- definir claramente a filosofia **em operação + reserva**;
- verificar se a linha de by-pass e o controle hidráulico impedem operação fora da faixa das bombas;
- considerar o inventário hidráulico do sistema no comportamento transiente e no vaso de expansão.

Fontes da seção: `petroles-004c2afadba7ea17c7dd7908:pNone:511961.0-511995.0`

## 5. Controle de biofouling e uso de hipoclorito
O material associa o controle microbiológico da água do mar à **geração de hipoclorito por eletrocloração** e à sua injeção logo após a captação ou nas bombas de elevação. No sistema de injeção de água, o hipoclorito é aplicado para evitar o desenvolvimento de microrganismos antes de etapas como filtração, tratamento químico, remoção de sulfato e desaeração. Após a desaeração, o sistema ainda pode receber **sequestrante de oxigênio**, **biodispersante** e **biocida**.

Embora esse encadeamento seja de água para injeção, ele é tecnicamente útil para a faceta porque mostra a lógica de controle de biofouling em utilidades com água do mar:
- atuar cedo na linha, próximo à captação, reduzindo colonização biológica a jusante;
- combinar desinfecção oxidante com outras barreiras químicas quando o serviço exigir;
- monitorar o desempenho não só pela dosagem, mas pelo efeito sobre crescimento microbiológico e sobre incrustações associadas.

Em referência conceitual complementar, em circuitos de refrigeração com água do mar pode haver injeção esporádica de **hipoclorito de sódio** e **brometo de sódio** na tomada de água, com controle da dosagem para que a concentração descarregada permaneça dentro do limite ambiental aplicável ao contexto do projeto. O trecho também menciona, em outro contexto, controle contínuo de **cloro residual** na purga.

Para operação e troubleshooting, sinais típicos de biofouling incluem:
- elevação progressiva da perda de carga na captação, filtros ou trocadores;
- piora da troca térmica sem aumento proporcional de carga térmica do processo;
- necessidade crescente de dosagem química para manter desempenho;
- formação de biofilme, que pode acelerar corrosão sob depósito e retenção de sólidos.

Fontes da seção: `petroles-004c2afadba7ea17c7dd7908:pNone:388734.0-388774.0`, `petroles-004c2afadba7ea17c7dd7908:pNone:388720.0-388754.0`, `petroles-004c2afadba7ea17c7dd7908:pNone:2160438.0-2160505.0`, `regis-d55109174fd64e1fa1a0bdd0:pNone:8715.0-8908.0`

## 6. Incrustação, fouling e corrosão em sistemas térmicos
Os trechos sobre química de água indicam que o desempenho do sistema de resfriamento depende do controle simultâneo de **incrustação**, **fouling/deposição** e **corrosão**.

### 6.1 Incrustação
A incrustação está ligada à precipitação de sais, especialmente carbonato de cálcio. O material cita o uso de índices como **LSI**, **RSI** e **PSI** para prever tendência à incrustação ou corrosão. Ainda que os valores numéricos tenham sido suprimidos em parte do material, a lógica é clara:
- tendência mais incrustante favorece depósito em trocadores e perda de eficiência térmica;
- tendência mais corrosiva favorece perda de espessura e geração de produtos de corrosão, que por sua vez também podem atuar como depósito.

Medidas mencionadas:
- adição de ácido para reduzir pH e aumentar solubilidade de formadores de incrustação;
- uso de **inibidores químicos**, como fosfonatos, poliacrilatos e copolímeros;
- remoção de cálcio por abrandamento, troca iônica ou membranas.

### 6.2 Fouling
O fouling é descrito como deposição nas superfícies metálicas por sólidos suspensos, areia, poeira, biofilme, flocos de alumínio, óxidos de ferro, produtos de corrosão e até hidrocarbonetos oriundos de vazamentos de processo. Estratégias de controle citadas:
- filtração lateral;
- aumento da velocidade da água quando hidraulicamente adequado;
- adição de dispersantes químicos;
- limpeza de tubos com bolas de borracha, em arranjos compatíveis;
- melhoria da distribuição de fluxo para eliminar áreas de baixo escoamento.

### 6.3 Corrosão
A corrosão compromete espessura, resistência mecânica e transferência térmica. O material destaca a importância da **película superficial** formada por produtos de corrosão: uma película aderente e estável pode reduzir a continuidade do ataque; uma película porosa favorece a progressão corrosiva. Isso conecta diretamente tratamento químico, velocidade de escoamento, oxigênio dissolvido e deposição.

Para monitoramento prático, esta faceta pede atenção a:
- tendência química da água;
- estabilidade do filme protetor;
- acúmulo de produtos de corrosão em filtros e trocadores;
- impacto combinado de biofouling e depósitos sobre corrosão localizada.

Fontes da seção: `petroles-004c2afadba7ea17c7dd7908:pNone:3423731.0-3423771.0`

## 7. Sistema de água quente / heating medium
Os trechos descrevem um **sistema fechado de água doce** usado como fonte de calor para o processo, com **injeção periódica de inibidor de corrosão** e **vaso de expansão pressurizado**. O aquecimento ocorre por aproveitamento do calor residual dos gases de exaustão das turbinas em uma **WHRU/recuperador de calor**.

Aplicações citadas:
- aquecer a corrente de óleo e facilitar a separação das fases;
- aquecer a corrente de gás combustível para obtenção de ponto de orvalho adequado;
- atender consumidores de utilidades térmicas por meio de bombas de circulação dedicadas.

Pontos de projeto e operação:
- o sistema é fechado, logo o controle de inventário, expansão térmica e reposição de volume perdido é essencial;
- a indisponibilidade do recuperador de calor reduz a capacidade de aquecimento e pode afetar separação de óleo e condicionamento do gás combustível;
- a circulação por múltiplas bombas em paralelo exige atenção ao balanceamento hidráulico e à filosofia operação/reserva.

Fontes da seção: `petroles-004c2afadba7ea17c7dd7908:pNone:388734.0-388774.0`, `petroles-004c2afadba7ea17c7dd7908:pNone:2160506.0-2160541.0`

## 8. Comissionamento, monitoramento e solução de problemas
Com base nos arranjos descritos, o comissionamento e a operação assistida devem verificar, no mínimo:
- alinhamento hidráulico de captação, headers, trocadores, vasos e by-pass;
- condição dos filtros e limpeza dos circuitos;
- funcionamento de bombas principais, de reserva e de emergência quando existentes;
- comportamento do vaso de expansão frente à variação de temperatura e inventário;
- temperaturas de ida e retorno dos circuitos frios e quentes;
- integridade térmica dos trocadores de placas;
- dosagem química e evidências de biofouling, incrustação ou corrosão.

Em troubleshooting, algumas relações causais são particularmente importantes:
- **queda da capacidade de resfriamento** pode resultar de perda de vazão de água do mar, fouling no lado marinho, obstrução de filtros, degradação do trocador ou aumento da carga térmica dos compressores;
- **temperatura alta generalizada no circuito fechado** tende a apontar problema na rejeição de calor ao mar, não apenas em um consumidor individual;
- **aumento de perda de carga** com piora térmica reforça hipótese de depósito ou biofouling;
- **corrosão recorrente** sugere problema de tratamento químico, estabilidade do filme protetor ou combinação de oxigênio, depósitos e velocidade inadequada.

Fontes da seção: `petroles-004c2afadba7ea17c7dd7908:pNone:511961.0-511995.0`, `petroles-004c2afadba7ea17c7dd7908:pNone:3423731.0-3423771.0`, `petroles-004c2afadba7ea17c7dd7908:pNone:2160506.0-2160541.0`

## 9. Impacto de falhas de utilidades
A perda parcial ou total da utilidade de água do mar pode produzir efeitos em cascata:
- perda da capacidade de rejeição térmica dos circuitos fechados de água doce;
- aquecimento progressivo de compressores e demais consumidores críticos;
- redução da margem operacional de sistemas classificados e não classificados, se houver dependência comum da captação;
- comprometimento de outras funções alimentadas pela água do mar, como eletrocloração, dessalinização e, conforme a instalação, combate a incêndio ou água para injeção.

A segregação em dois sistemas de resfriamento, classificado e não classificado, reduz a probabilidade de uma única falha derrubar toda a planta, mas não elimina vulnerabilidades de causa comum na captação de água do mar ou na química de tratamento.

Fontes da seção: `petroles-004c2afadba7ea17c7dd7908:pNone:388734.0-388774.0`, `petroles-004c2afadba7ea17c7dd7908:pNone:2160438.0-2160505.0`, `petroles-004c2afadba7ea17c7dd7908:pNone:2160506.0-2160541.0`