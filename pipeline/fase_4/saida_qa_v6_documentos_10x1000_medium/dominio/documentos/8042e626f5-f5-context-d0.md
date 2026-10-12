# Almoxarifado e sobressalentes em FPSO

## 1. Finalidade do almoxarifado de manutenção em um FPSO
Em um FPSO, a gestão de materiais e sobressalentes não é apenas uma função logística: ela interfere diretamente no tempo de restauração da função dos equipamentos, na disponibilidade da produção e no risco operacional. Quando o processo de gestão de materiais é fraco, falhas em equipamentos críticos tendem a gerar compras reativas, fretes urgentes, maior probabilidade de especificação incorreta e aumento do tempo total de manutenção corretiva. Em contrapartida, uma gestão estruturada permite reduzir o tempo de planejamento do trabalho e o tempo de execução da cadeia de suprimentos, principalmente quando os materiais corretos já estão especificados e disponíveis em estoque.

Para itens críticos à produção e à segurança, o almoxarifado deve ser entendido como parte do sistema de integridade do ativo: ele suporta a estratégia de restauração da função após falha, seja por substituição imediata, seja por retirada do item, reparo e retorno ao estoque.

**Fontes:** `petroles-004c2afadba7ea17c7dd7908:pNone:538840.60-538877.0`, `petroles-004c2afadba7ea17c7dd7908:pNone:538859.0-538896.0`

## 2. Base cadastral, BOM e rastreabilidade de sobressalentes
A gestão eficaz de sobressalentes começa na qualidade da base de dados. O processo descrito nas fontes parte da extração de tags do ERP ou ferramenta equivalente para formar uma base de projeto contendo as informações necessárias às decisões de manutenção e estoque. A seleção dos tags pode ser priorizada por criticidade de produção e/ou segurança.

A partir dessa base, define-se para cada tag a estratégia de restauração da função:
- substituir o item por sobressalente;
- reparar o item retirado;
- combinar substituição imediata com reparo offline e reposição posterior.

Em seguida, é estruturada a **Bill of Material (BOM)** de cada tag priorizado. Segundo o material fornecido, a BOM deve conter, no mínimo:
- número/identificação do componente;
- quantidade;
- unidade de medida.

Quando a documentação disponível é insuficiente para identificar corretamente o material ou atender ao padrão de qualidade da BOM, deve-se criar uma **lista de desvios** para registrar lacunas de cadastro e submetê-las a decisão formal das disciplinas responsáveis. O resultado esperado é uma lista de sobressalentes robusta e estruturada, apta a ser carregada no ERP, reduzindo erros de especificação e permitindo requisições proativas.

Do ponto de vista do almoxarifado, isso significa que a rastreabilidade mínima deve ligar:
- o tag do equipamento;
- a estratégia de reparo/substituição;
- o número do material no ERP;
- a BOM do equipamento;
- a situação de estoque do item.

Sem essa rastreabilidade, o estoque físico pode até existir, mas não necessariamente estará disponível de forma confiável para planejamento, reserva, compra e reposição.

**Fontes:** `petroles-004c2afadba7ea17c7dd7908:pNone:538859.0-538896.0`

## 3. Conceitos de inventário aplicáveis ao almoxarifado offshore
As fontes distinguem alguns conceitos úteis para a gestão de sobressalentes:

- **Inventário/estoque:** conjunto de bens mantidos para suportar produção, reparo, manutenção, consumo operacional ou prestação de serviço.
- **Estoque (storage):** materiais não transitórios, protegidos e mantidos para recuperação posterior.
- **Demanda:** quantidade requerida de um produto ou serviço.
- **Backorder/backlog:** demanda não atendida imediatamente, mas aceita pelo cliente/usuário para atendimento posterior.
- **Lost sale:** demanda não atendida e não postergável; no contexto de manutenção, corresponde à indisponibilidade não absorvida pelo sistema de estoques.
- **Lead time / tempo de ressuprimento:** intervalo entre a emissão do pedido e a chegada/disponibilização do item; para itens fabricados internamente, pode incluir o tempo de produção da batelada.
- **Mudança no inventário por deterioração/obsolescência:** redução de utilidade do item por vida útil, deterioração ou ultrapassagem técnica.
- **Review time:** revisão contínua (quantidade conhecida a qualquer momento) ou periódica (quantidade conhecida em épocas definidas).

As fontes também registram que a **posição de estoque** pode ser entendida como a soma do estoque em mãos com os pedidos em aberto, menos os não atendimentos acumulados. Essa visão é importante porque o nível de decisão de reposição não deve considerar apenas o saldo físico local, mas o que já está encomendado e o que já foi comprometido.

No contexto de FPSO, isso é particularmente relevante para itens críticos e de longo prazo de fornecimento, nos quais um saldo aparente no sistema pode não representar disponibilidade efetiva para manutenção.

**Fontes:** `regis-1f62e24eb63478f80ae2cda4:pNone:2009.0-2242.0`, `regis-661d49649682128ff1d118ca:pNone:1294.0-1470.0`

## 4. Parâmetros de decisão: criticidade, lead time, nível de serviço e custo
As fontes indicam que a definição de níveis de estoque deve ser feita por material number, associando o status de estoque aos tags e às estratégias de reparo. Os níveis recomendados de mínimo e máximo devem ser altos o suficiente para cobrir o lead time do fornecedor e a demanda esperada, porém não tão altos a ponto de impor custo excessivo de capital, armazenagem e manutenção de inventário.

Nesse processo, aparecem quatro direcionadores centrais:

### 4.1 Criticidade do item
A priorização pode ser baseada em criticidade de segurança e de produção. Itens safety-critical devem estar disponíveis quando necessários para mitigar consequências de eventos de segurança. Itens production-critical devem minimizar indisponibilidade e perda de produção.

### 4.2 Lead time
O prazo de aquisição ou reparo pesa fortemente na definição do estoque. Itens de longo lead time exigem tratamento diferenciado, porque a falta deles prolonga a indisponibilidade do equipamento e amplia a exposição a compras emergenciais.

### 4.3 Nível de serviço
O material de referência associa o custo de estoque ao **service level target**, entendido como a probabilidade de não ocorrer stock-out durante o próximo ciclo de reposição. Em termos práticos, um nível de serviço mais alto tende a exigir maior proteção por estoque; um nível de serviço mais baixo reduz capital empatado, mas aumenta risco de ruptura.

### 4.4 Custo total
As decisões devem buscar equilíbrio entre:
- custo de aquisição/reposição;
- custo de manutenção do estoque;
- custo de fretes urgentes e compras reativas;
- custo de indisponibilidade do equipamento;
- custo/impacto de perda de produção;
- impacto sobre segurança operacional.

Para FPSOs, esse balanço raramente é puramente contábil. Um item de baixo valor unitário pode justificar estoque alto se sua falta impedir a restauração de um sistema crítico. Em sentido oposto, um item caro e pouco crítico pode ser mantido em quantidade menor, desde que haja estratégia de reparo ou alternativa logística viável.

**Fontes:** `petroles-004c2afadba7ea17c7dd7908:pNone:538859.0-538896.0`, `petroles-004c2afadba7ea17c7dd7908:pNone:468269.0-468309.0`, `regis-1f62e24eb63478f80ae2cda4:pNone:2009.0-2242.0`

## 5. Estoque mínimo, máximo, segurança e ponto de reposição
As fontes permitem consolidar uma lógica de decisão aplicável ao almoxarifado de manutenção:

### 5.1 Estoque de segurança
É o estoque mantido para absorver:
1. variação de demanda acima da prevista; e/ou
2. atraso no recebimento do lote de reposição.

Ou seja, o estoque de segurança protege o FPSO contra a incerteza combinada de consumo e lead time.

### 5.2 Ponto de reposição
O ponto de reposição é o nível de estoque que dispara o pedido de um novo lote. Conceitualmente, ele deve cobrir a demanda esperada até a chegada do próximo lote, acrescida da proteção necessária contra incertezas. Em termos de gestão, a decisão de reposição não depende só do saldo físico, mas da posição de estoque e do tempo de ressuprimento.

### 5.3 Revisão contínua versus revisão periódica
- **Revisão contínua:** adequada quando se deseja conhecer o saldo a qualquer momento e disparar reposição assim que a posição de estoque atingir o ponto de ressuprimento.
- **Revisão periódica:** adequada quando as revisões ocorrem em intervalos definidos e a reposição busca recompor o estoque até um nível máximo.

Para itens críticos de FPSO, a lógica de revisão contínua é, em geral, mais aderente à necessidade de resposta rápida, embora a fonte não estabeleça isso como regra universal.

### 5.4 Faixas mínimo–máximo
As fontes do projeto de material management indicam que, para cada número de material, os níveis recomendados de mínimo e máximo devem ser definidos em workshops com as disciplinas responsáveis e depois carregados no ERP. Essas faixas precisam refletir:
- lead time do fornecedor;
- demanda/consumo esperado;
- criticidade do tag;
- política de reparo/substituição;
- objetivo de nível de serviço;
- custo de inventário.

### 5.5 Papel da variabilidade e da obsolescência
A política de estoques existe, entre outras razões, para lidar com economia de escala, variabilidade previsível ou imprevisível e conflitos entre objetivos. Porém os parâmetros não são permanentes: consumo histórico, confiabilidade, contratos, especificações e obsolescência mudam com o tempo. Por isso, níveis mínimo/máximo e estoques de segurança devem ser periodicamente revistos.

**Fontes:** `regis-661d49649682128ff1d118ca:pNone:1294.0-1470.0`, `regis-1f62e24eb63478f80ae2cda4:pNone:2009.0-2242.0`, `petroles-004c2afadba7ea17c7dd7908:pNone:538859.0-538896.0`

## 6. Tratamento de reparáveis: retirar, reparar, testar e retornar ao estoque
Um ponto central para FPSO é distinguir o que deve ser estocado como sobressalente novo e o que pode operar em regime de **reparável**.

As fontes descrevem que a restauração da função após falha pode ser feita por substituição ou reparo, e que a escolha depende de fatores como:
- preço do equipamento;
- acessibilidade para manutenção;
- especialização da equipe de manutenção;
- localização/área perigosa;
- política de inventário aplicável.

Também aparece um macrofluxo típico para equipamentos e materiais: fornecedor → estoque/centro de distribuição → unidade offshore → uso → retorno de excedentes ou usados → manutenção → retorno ao estoque; podendo haver alienação quando aplicável.

Para equipamentos submarinos e módulos recuperáveis, o material destaca uma prática de **replace on failure wherever possible and repair offline**, isto é:
1. substituir o item em campo para restabelecer rapidamente a função;
2. remover o item falhado;
3. encaminhá-lo para oficina onshore ou fabricante para reparo/refurbishment;
4. repor o estoque a um nível aceitável após o consumo do sobressalente.

Essa lógica é muito relevante para um almoxarifado de FPSO porque desloca parte do desempenho da manutenção para a gestão do ciclo do reparável. Um item reparável mal rastreado pode desaparecer do ciclo e provocar falsa sensação de cobertura de estoque.

Boas decisões sobre reparáveis exigem, no mínimo:
- identificação do item como reparável ou não reparável;
- vínculo do reparável ao tag/equipamento de origem;
- registro de retirada, envio, reparo e retorno;
- definição do nível aceitável de reposição após consumo;
- alinhamento entre bordo, oficina em terra e ERP.

**Fontes:** `petroles-004c2afadba7ea17c7dd7908:pNone:538840.60-538877.0`, `regis-1f62e24eb63478f80ae2cda4:pNone:2009.0-2242.0`, `petroles-004c2afadba7ea17c7dd7908:pNone:468269.0-468309.0`

## 7. Preservação e obsolescência de sobressalentes
O material fornecido não detalha condições ambientais específicas de preservação offshore, mas traz princípios úteis:

- estoque é um conjunto de itens **protegidos e mantidos** para recuperação posterior;
- sobressalentes e pacotes devem ter definida não apenas a quantidade, mas também **onde serão armazenados e como serão mantidos**;
- materiais podem perder adequação por **deterioração**, **vida útil** ou **obsolescência técnica**;
- especificações, histórico de consumo e contratos mudam com o tempo, exigindo atualização contínua da gestão de materiais.

Assim, mesmo sem detalhamento de temperatura, umidade ou requisitos por família de materiais, a implicação prática para o almoxarifado é que preservar não significa apenas "guardar": significa manter a condição de uso e a validade técnica do item até sua aplicação, evitando tanto deterioração física quanto obsolescência documental/cadastral.

Em termos de governança, a preservação deve ser acompanhada por revisão contínua dos cadastros e das estratégias, porque um item corretamente armazenado, mas com especificação desatualizada ou contrato de reparo encerrado, continua sendo um risco de indisponibilidade.

**Fontes:** `regis-1f62e24eb63478f80ae2cda4:pNone:2009.0-2242.0`, `petroles-004c2afadba7ea17c7dd7908:pNone:468269.0-468309.0`, `petroles-004c2afadba7ea17c7dd7908:pNone:538859.0-538896.0`

## 8. Acuracidade: física, cadastral e decisória
Embora os trechos fornecidos não tragam procedimentos detalhados de inventário físico/cíclico, eles sustentam fortemente a necessidade de **acuracidade cadastral e sistêmica**. Essa acuracidade depende de:
- extração correta dos tags e materiais do ERP;
- associação consistente entre tag, BOM, estratégia de reparo e estoque;
- tratamento formal de informações faltantes por lista de desvios;
- atualização contínua dos parâmetros quando houver obsolescência, mudança de consumo, alteração contratual ou revisão de especificação.

Em termos práticos, a acuracidade do almoxarifado pode ser decomposta em três níveis:

1. **Acuracidade cadastral** – o material correto está cadastrado com identificação, unidade e aplicação corretas.
2. **Acuracidade sistêmica** – o ERP reflete a situação real de estoque, pedidos e estratégia de reparo.
3. **Acuracidade decisória** – os parâmetros usados para mínimo, máximo e reposição continuam válidos para a realidade operacional atual.

As fontes deixam claro que a gestão de materiais deve operar em ciclo de melhoria contínua. Logo, a acuracidade não é um estado fixo, mas uma disciplina de revisão e correção permanente.

**Fontes:** `petroles-004c2afadba7ea17c7dd7908:pNone:538859.0-538896.0`, `regis-1f62e24eb63478f80ae2cda4:pNone:2009.0-2242.0`

## 9. Uso de ferramentas analíticas para definir quantidades de sobressalentes
Um dos estudos citados descreve uma ferramenta de análise de sobressalentes para equipamentos submarinos baseada em:
- distribuição de probabilidades de Poisson;
- análise de custo-benefício;
- custo do item;
- exigências de manutenção;
- lead time;
- impacto na produção;
- taxa de falha.

A lógica principal é que a quantidade ótima de sobressalentes não deve ser estática. Ela pode mudar com:
- preço do petróleo;
- perfil de produção do campo;
- novas informações de confiabilidade;
- variações nas taxas de falha ao longo do tempo.

Mesmo sendo um exemplo subsea e específico de projeto, esse raciocínio é transferível ao almoxarifado de FPSO: a definição de quantidade de sobressalentes críticos deve ser **baseada em risco e confiabilidade**, e não apenas em prática histórica ou percepção subjetiva. Em especial, as fontes alertam que dados genéricos da indústria podem não representar adequadamente as condições reais de operação do ativo.

**Fontes:** `petroles-004c2afadba7ea17c7dd7908:pNone:468269.0-468309.0`

## 10. Implicações práticas para a gestão de almoxarifado e sobressalentes em FPSO
Com base nos trechos fornecidos, uma gestão tecnicamente consistente deve assegurar, no mínimo:

- priorização de itens por criticidade de segurança e produção;
- definição formal da estratégia por tag: reparar, substituir ou combinar ambas;
- estruturação de BOM e lista de sobressalentes por equipamento;
- saneamento de desvios cadastrais antes de confiar no estoque sistêmico;
- parametrização de mínimo, máximo e reposição no ERP;
- revisão periódica dos níveis em função de lead time, demanda, falha, contratos e obsolescência;
- rastreabilidade do ciclo dos reparáveis;
- integração entre manutenção, engenharia, suprimentos e logística;
- redução de compras emergenciais como indicador de maturidade da gestão.

Em síntese, o almoxarifado de um FPSO não deve ser gerido como depósito passivo. Ele deve funcionar como um sistema ativo de suporte à manutenção e à integridade, no qual cadastro, rastreabilidade, estoque e tratamento de reparáveis formam uma única cadeia decisória.

**Fontes:** `petroles-004c2afadba7ea17c7dd7908:pNone:538840.60-538877.0`, `petroles-004c2afadba7ea17c7dd7908:pNone:538859.0-538896.0`, `regis-1f62e24eb63478f80ae2cda4:pNone:2009.0-2242.0`, `petroles-004c2afadba7ea17c7dd7908:pNone:468269.0-468309.0`, `regis-661d49649682128ff1d118ca:pNone:1294.0-1470.0`