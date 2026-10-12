# Gás separado e água produzida em FPSOs

## 1. Papel das correntes separadas no processamento primário

Em um FPSO, o gás separado e a água produzida não são correntes residuais simples: ambas condicionam a capacidade de processamento do óleo e a estabilidade operacional da planta. Após a chegada dos fluidos dos poços, a separação primária distribui o escoamento multifásico em correntes de óleo, gás e água, cada qual com requisitos próprios de tratamento e destinação.

Os vasos separadores podem ser bifásicos ou trifásicos, em série ou em paralelo. Os mecanismos físicos citados para a separação incluem:

- **ação da gravidade e diferença de densidades**, para decantação da fase mais pesada;
- **separação inercial**, por mudança brusca de velocidade e direção do escoamento;
- **aglutinação/coalescência**, favorecendo o crescimento de gotas;
- **força centrífuga**, aproveitando diferenças de densidade.

Em plantas offshore, a grande variação de vazão, pressão e composição gás/óleo/água oriunda dos poços, somada às limitações de volume e peso dos separadores, faz com que a operação das correntes separadas seja particularmente sensível. Variáveis como **tempo de residência, temperatura, dosagem química e pressão** afetam diretamente a qualidade da separação e, portanto, a carga imposta aos sistemas de gás e de água produzida.

Nos separadores, o gás sai pelo topo, tipicamente após seção de remoção de névoa; o líquido segue para acumulação e, conforme o arranjo, para tratamento de óleo e/ou água. Em várias plantas, são usados **múltiplos estágios de separação**, inclusive para lidar com diferentes pressões de fluxo dos poços e maximizar a recuperação de hidrocarbonetos.

**Fontes:** `petroles-4ee4bce16acf674505c8912d:pNone:1075708.60-1075748.0`

## 2. Água produzida: tratamento, recirculações e destinação

### 2.1 Objetivo do tratamento da água produzida

A água produzida é um efluente inevitável da produção de petróleo. Seu tratamento busca dois resultados principais:

1. **recuperar parte do óleo ainda arrastado na corrente aquosa**; e
2. **especificar a água para descarte, reuso ou reinjeção**, conforme requisitos legais e/ou técnicos.

As fontes destacam que a composição da água produzida é variável e pode incluir **sais, compostos orgânicos, metais pesados e gases dissolvidos**, o que explica a necessidade de flexibilidade do tratamento e a dificuldade de padronizar uma única rota universal.

**Fontes:** `petroles-004c2afadba7ea17c7dd7908:pNone:429654.0-429714.0`, `petroles-4ee4bce16acf674505c8912d:pNone:438576.0-438619.0`

### 2.2 Rota típica offshore descrita nas fontes

Nas rotas descritas para FPSO, a corrente aquosa a jusante do separador de água livre ainda contém óleo em teor incompatível com descarte direto no mar. Uma sequência representativa é:

1. **separação primária / separador de água livre**;
2. **hidrociclones**;
3. **flotador**;
4. **medição on-line de TOG**;
5. **descarte**, se dentro da especificação, ou **desvio para tanques de água fora de especificação/slops** quando acima do limite.

Esse arranjo evidencia que o sistema de água produzida não é isolado: ele se conecta ao sistema de separação primária, aos tanques de contingência e, em algumas instalações, ao reprocessamento posterior.

**Fontes:** `regis-2b32d20fca156fd1142e4bec:pNone:3424.0-3600.0`, `petroles-4ee4bce16acf674505c8912d:pNone:1447358.0-1447409.0`

### 2.3 Hidrociclones: função e interface com o processo principal

O primeiro estágio de tratamento da água produzido nas fontes é a bateria de **hidrociclones**. O princípio descrito é o seguinte:

- a água entra sob pressão, de forma tangencial, na região de maior diâmetro;
- o escoamento assume trajetória espiral para as regiões de menor diâmetro;
- o estreitamento aumenta a velocidade e a força centrífuga;
- os componentes mais pesados, principalmente **água e sólidos**, tendem para a parede;
- no centro forma-se um fluxo axial reverso, enriquecido em óleo;
- esse óleo é rejeitado por uma saída específica e **retorna para a entrada do separador gravitacional**.

Essa recirculação é relevante sob o ponto de vista de processo: o hidrociclone não apenas “limpa” a água, mas também **recupera hidrocarbonetos** que retornam ao circuito principal de separação. Logo, ele é um equipamento de tratamento de efluente e, ao mesmo tempo, de recuperação de valor.

**Fontes:** `regis-2b32d20fca156fd1142e4bec:pNone:3424.0-3600.0`

### 2.4 Flotação e decisão de descarte

A etapa final descrita para o tratamento da água produzida é o **vaso flotador**. O mecanismo informado é a injeção de ar em pequenas bolhas, que entram em contato com gotículas remanescentes de óleo em suspensão. As bolhas promovem a ascensão do óleo até a superfície, formando uma camada removível.

Na saída inferior do flotador, a água passa por um **analisador on-line de TOG (teor de óleo e graxa)**. A lógica operacional descrita é binária:

- **TOG dentro da especificação**: a água segue para descarte em alto-mar;
- **TOG acima do limite**: a água é desviada para tanques específicos da plataforma para água fora de especificação, podendo depois ser reprocessada.

Em uma das fontes, o monitoramento contínuo é associado a um **espectrofotômetro on-line**. A ideia de processo é a mesma: o valor medido determina se a corrente vai para descarte ou contenção.

**Fontes:** `regis-2b32d20fca156fd1142e4bec:pNone:3424.0-3600.0`, `petroles-4ee4bce16acf674505c8912d:pNone:1447358.0-1447409.0`

### 2.5 Descarte marítimo e limites legais citados

As fontes indicam que o descarte da água produzida é condicionado por critério legal local. Para o Brasil, uma fonte explicita a **Resolução CONAMA 393/07**, com limite máximo de concentração de óleos e graxas na água descartada ao mar de **29 mg/L**.

As fontes também sugerem que critérios regulatórios podem variar conforme norma aplicável e histórico do projeto, mas o material disponível nesta faceta não permite consolidar, com segurança normativa, todos os cenários possíveis de licenciamento e vigência.

**Fontes:** `regis-2b32d20fca156fd1142e4bec:pNone:3424.0-3600.0`, `petroles-4ee4bce16acf674505c8912d:pNone:1447358.0-1447409.0`

### 2.6 Reinjeção de água produzida: quando existe e o que muda

As fontes deixam claro que **nem toda água produzida tratada é descartada**. Em algumas plataformas, ela pode passar por tratamentos adicionais para permitir **reinjeção no reservatório**, com objetivo de manutenção de pressão e suporte à produção.

Entretanto, também é registrado que, em certas instalações estudadas, a água produzida **não** é reinjetada; nesses casos, a água de injeção vem de um **sistema separado de captação e tratamento de água do mar**.

Quando a destinação é reinjeção, as exigências descritas vão além do TOG:

- remoção de **sólidos em suspensão**, para evitar tamponamento do reservatório;
- remoção de componentes corrosivos dissolvidos, como **CO2** e **H2S**;
- controle microbiológico, especialmente de **bactérias redutoras de sulfato**;
- uso de processos físicos e químicos, como **filtração**, **sequestrantes de oxigênio** (ex.: bissulfito de amônio), **inibidores de corrosão** à base de aminas fílmicas e **inibidores de incrustação**.

Isso mostra que a escolha entre descarte e reinjeção altera profundamente o escopo do tratamento. Um sistema desenhado apenas para descarte pode não ser suficiente para serviço de injeção.

**Fontes:** `regis-2b32d20fca156fd1142e4bec:pNone:3424.0-3600.0`, `petroles-4ee4bce16acf674505c8912d:pNone:438576.0-438619.0`

### 2.7 Limitações tecnológicas relevantes no offshore

As fontes destacam que, no ambiente offshore, a maior parte das tecnologias usuais de tratamento da água produzida remove principalmente **óleo disperso**, não necessariamente **óleo solúvel** ou aromáticos solúveis. São citados como exemplos de frações pouco removidas compostos como **BTEX** e compostos aromáticos policíclicos mais leves.

O desempenho do tratamento depende fortemente das variáveis da instalação, como:

- tipo de reservatório;
- temperatura e pressão;
- tipo e viscosidade do óleo;
- estabilidade da emulsão;
- tamanho de gota do óleo;
- salinidade da água;
- velocidade de escoamento.

Tratamentos adicionais/terciários podem existir, mas as fontes apontam restrições frequentes em plataformas relacionadas a **espaço, peso, energia e tempo de residência**. Portanto, a eficiência do sistema de água produzida não deve ser avaliada apenas pela presença nominal de equipamentos, mas pela aderência da solução às características do fluido e às limitações físicas da unidade.

**Fontes:** `petroles-4ee4bce16acf674505c8912d:pNone:438576.0-438619.0`

## 3. Gás separado: rotas, condicionamento e destinos

### 3.1 Origem do gás separado e classificação por pressão

O gás separado em FPSOs pode surgir em diferentes pontos e níveis de pressão ao longo da separação primária e do tratamento do óleo. As fontes mostram pelo menos dois arranjos representativos:

- em uma instalação, o **gás do primeiro estágio de separação** e o do **separador de teste** seguem para a sucção do sistema principal de compressão, enquanto o gás do **segundo estágio** segue para **compressores booster**, que elevam sua pressão antes do envio à compressão principal;
- em outra instalação, as correntes são classificadas como **gás de alta, média e baixa pressão**. O gás de alta vai diretamente ao sistema principal de compressão, enquanto os gases de média e baixa passam por um sistema adicional, identificado como **Unidade de Recuperação de Vapor (URV)**, para elevar a pressão até o nível de sucção dos compressores principais.

Esses exemplos mostram uma regra prática importante: **correntes gasosas de menor pressão normalmente não entram diretamente na compressão principal sem equalização ou reforço de pressão**.

**Fontes:** `petroles-4ee4bce16acf674505c8912d:pNone:2060915.0-2060948.0`, `petroles-4ee4bce16acf674505c8912d:pNone:1447358.0-1447409.0`

### 3.2 Interfaces entre separação, compressão e remoção de líquidos

As fontes descrevem sistemas de compressão em múltiplos estágios, com **coolers** e **scrubbers** após cada estágio. A função operacional é dupla:

- **resfriar o gás** após a compressão;
- **reter líquidos formados ou arrastados**, devolvendo esses líquidos ao processo.

Isso é uma interface importante entre tratamento de gás e recuperação de hidrocarbonetos: os líquidos separados nos scrubbers não são descarte, mas **retorno ao processo**. Em outras palavras, o condicionamento do gás também opera como etapa de retenção de condensados e proteção dos compressores e linhas a jusante.

**Fontes:** `petroles-4ee4bce16acf674505c8912d:pNone:1447358.0-1447409.0`, `petroles-4ee4bce16acf674505c8912d:pNone:1075708.60-1075748.0`

### 3.3 Condicionamento do gás para exportação, consumo interno e gas lift

As destinações citadas para o gás incluem:

- **exportação por gasoduto**;
- **reinjeção no reservatório**;
- **consumo interno como gás combustível**;
- **uso em gas lift**;
- **flare**, como último recurso.

Para exportação, as fontes indicam a necessidade de:

- atender a **teores máximos de água** no gás, para preservar a integridade dos gasodutos;
- reduzir contaminantes;
- garantir **pressão mínima inicial** para escoamento até terra.

Uma das rotas descritas inclui **desidratação com TEG (trietilenoglicol)** após a compressão. O objetivo declarado é adequar a umidade do gás para exportação e gas lift e evitar formação de **hidratos**, especialmente em linhas frias e sob alta pressão. Em uma instalação analisada, é citado como meta um **ponto de orvalho de -15 °C**.

As fontes também registram que, em certos casos, poços de gás com pressão suficientemente alta podem seguir diretamente para desidratação, sem passar pela compressão principal; em outros cenários, a pressão é reduzida até a sucção do sistema principal e o gás passa então pela rota completa de compressão.

**Fontes:** `regis-2b32d20fca156fd1142e4bec:pNone:3424.0-3600.0`, `petroles-4ee4bce16acf674505c8912d:pNone:1447358.0-1447409.0`

### 3.4 Gás para reinjeção

Quando a destinação é reinjeção, as fontes informam dois critérios essenciais:

- o gás deve atender a **baixos teores de água**;
- sua pressão deve ser elevada a valor **acima da pressão do reservatório** onde será reinjetado.

Uma fonte associa esse requisito à realidade do pré-sal, citando reservatórios com pressão da ordem de **550 bar**. Isso evidencia que a reinjeção de gás pode impor requisitos de compressão mais severos que a exportação, dependendo do ativo.

As fontes também observam que o volume reinjetado pode depender da demanda de exportação, ou seja, a reinjeção pode funcionar como destino do gás não absorvido pelo mercado consumidor.

**Fontes:** `regis-2b32d20fca156fd1142e4bec:pNone:3424.0-3600.0`

### 3.5 Flare como contingência e impacto na produção de óleo

O flare é descrito como **último recurso** para destinação do gás. O uso prolongado é indesejável tanto por razões ambientais quanto por limitações regulatórias de queima.

As fontes são particularmente enfáticas quanto ao impacto da indisponibilidade do tratamento de gás em campos com **alta RGO**. Se o sistema de tratamento/compressão ficar indisponível e impedir exportação ou reinjeção, o gás não tratado tende a ser desviado imediatamente para flare. Caso o restabelecimento não ocorra em poucas horas, torna-se necessária a **restrição da produção de óleo**, com possível fechamento de poços.

Isso reforça um ponto operacional central da faceta: em muitos FPSOs, **o sistema de gás é gargalo direto da produção de óleo**.

**Fontes:** `regis-2b32d20fca156fd1142e4bec:pNone:3424.0-3600.0`, `petroles-4ee4bce16acf674505c8912d:pNone:2060915.0-2060948.0`

## 4. Interfaces e recirculações críticas do processo

As principais interfaces e recirculações identificadas nas fontes são:

### 4.1 Na água produzida

- **óleo rejeitado pelos hidrociclones** retorna à entrada do separador gravitacional;
- **água fora de especificação** é desviada para tanques dedicados/slops, em vez de ser descartada;
- em instalações com reprocessamento, o conteúdo desses tanques pode retornar posteriormente ao circuito de tratamento.

### 4.2 No gás separado

- gás de **média/baixa pressão** pode seguir para **URV** antes da compressão principal;
- gás de estágios intermediários pode seguir para **boosters**, elevando a pressão até a sucção do trem principal;
- líquidos removidos em **scrubbers** retornam ao processo;
- após tratamento, o gás pode ser repartido entre **combustível, gas lift, exportação e reinjeção**.

### 4.3 Na decisão operacional integrada

A destinação das correntes depende do atendimento simultâneo a critérios de **qualidade** e **capacidade de recebimento**:

- água com TOG adequado pode ser descartada; fora da especificação, deve ser contida/reprocessada;
- gás com pressão e qualidade adequadas pode ir para exportação, uso interno ou reinjeção;
- na indisponibilidade desses destinos, o flare absorve apenas de forma contingencial e limitada;
- se a capacidade de flare ou o tempo permissível de contingência forem excedidos, a consequência pode ser **redução de throughput de óleo**.

**Fontes:** `regis-2b32d20fca156fd1142e4bec:pNone:3424.0-3600.0`, `petroles-4ee4bce16acf674505c8912d:pNone:2060915.0-2060948.0`, `petroles-4ee4bce16acf674505c8912d:pNone:1447358.0-1447409.0`

## 5. Condições anormais, gargalos e lições operacionais

As fontes trazem exemplos úteis de condições anormais que ajudam a entender a importância das interfaces entre sistemas.

### 5.1 Ausência ou indisponibilidade de equipamentos de água produzida

Em um estudo de caso, a ausência de **flotador** em uma unidade fazia com que o tratamento dependesse apenas do hidrociclone. Nessas condições, era comum haver momentos em que o TOG da água não atendia às especificações ambientais para descarte no mar. A resposta operacional incluía:

- armazenamento da água oleosa em tanque específico;
- em casos críticos, contratação de navio para remoção do inventário e tratamento em outra instalação ou em terminal terrestre.

A lição prática é clara: o desempenho do sistema de água produzida não deve ser avaliado apenas pela presença do primeiro estágio de separação. A ausência do estágio complementar pode transferir o problema para tancagem, logística e custo operacional.

**Fontes:** `petroles-004c2afadba7ea17c7dd7908:pNone:1390398.0-1390484.0`

### 5.2 Incompatibilidade de produtos químicos e efeito nas correntes tratadas

No mesmo conjunto de observações de campo, há relato de **iridescência/mancha na água** atribuída à mistura de produtos químicos usados em pontos distintos do processo, como desemulsificante, sequestrante de H2S e antiespumante. O texto associa o problema à falta de projeto integrado entre unidades que operavam em série.

Mesmo sem caracterizar, por si só, não conformidade de TOG, esse exemplo mostra que interfaces químicas mal geridas podem:

- prejudicar a aparência da descarga;
- dificultar diagnóstico operacional;
- mascarar ou agravar problemas de separação óleo/água.

Portanto, além de pressão, vazão e qualidade analítica, a gestão das correntes separadas também depende de **compatibilidade química entre sistemas e entre unidades interligadas**.

**Fontes:** `petroles-004c2afadba7ea17c7dd7908:pNone:1390398.0-1390484.0`

## 6. Síntese técnica para tomada de decisão

Com base nas fontes, o manejo profissional de gás separado e água produzida em FPSOs pode ser sintetizado pelos seguintes critérios:

1. **Tratar a água produzida não é apenas adequar um efluente**; é também recuperar óleo e proteger descarte ou reinjeção.
2. **Hidrociclone e flotador cumprem funções complementares**: o primeiro promove separação centrífuga e recircula óleo ao processo; o segundo remove óleo remanescente por flotação.
3. **TOG on-line governa a decisão imediata de descarte ou contenção**.
4. **Reinjeção de água e descarte são destinos com requisitos distintos**; reinjeção exige controle adicional de sólidos, corrosivos dissolvidos e microbiologia.
5. **O gás separado nasce em diferentes níveis de pressão**, exigindo integração entre separação, URV/boosters, compressão principal, resfriamento, scrubbers e desidratação.
6. **Exportação, combustível, gas lift, reinjeção e flare competem pela mesma corrente tratada**, de modo que indisponibilidade de uma rota pode sobrecarregar as demais.
7. **O flare não é solução de regime normal**; em sistemas de alta RGO, sua utilização prolongada pode forçar restrição da produção de óleo.
8. **A eficiência real do tratamento depende das características do fluido e da integração de equipamentos e químicos**, não apenas do fluxograma nominal.

**Fontes:** `regis-2b32d20fca156fd1142e4bec:pNone:3424.0-3600.0`, `petroles-4ee4bce16acf674505c8912d:pNone:2060915.0-2060948.0`, `petroles-4ee4bce16acf674505c8912d:pNone:1447358.0-1447409.0`, `petroles-4ee4bce16acf674505c8912d:pNone:438576.0-438619.0`, `petroles-004c2afadba7ea17c7dd7908:pNone:1390398.0-1390484.0`