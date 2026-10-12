# Suprimento e estoque crítico

## 1. Finalidade da gestão de materiais para continuidade operacional em FPSO

Em logística offshore, a gestão de estoque não deve ser tratada apenas como atividade de almoxarifado. Ela é um mecanismo de proteção da continuidade operacional diante do desencontro entre demanda e suprimento, especialmente quando o ressuprimento depende de cadeias longas, múltiplas etapas de liberação e incertezas logísticas. Em termos de cadeia de suprimentos, o estoque existe porque suprimento e demanda nem sempre estão sincronizados; ele aumenta a capacidade de atendimento, viabiliza economias de escala e melhora a responsividade, mas também eleva custos e riscos de capital imobilizado.

Na indústria do petróleo, o dimensionamento histórico de estoques frequentemente foi expresso em "dias de operação". Embora essa métrica seja útil como referência de cobertura, ela é insuficiente quando usada isoladamente. O dimensionamento precisa considerar fatores logísticos que afetam a reposição, como confiabilidade do abastecimento, tempo de ressuprimento, restrições de transporte, impedimentos operacionais e condições adversas que atrasem entregas.

Em um FPSO, isso é particularmente relevante para sobressalentes críticos, materiais de manutenção, consumíveis operacionais e itens cuja indisponibilidade pode provocar atraso de manutenção, backorder interno, degradação do nível de serviço ou até perda de produção.

*Fontes da seção: `regis-1f62e24eb63478f80ae2cda4:pNone:1917.0-2157.0`, `regis-a084aafb9ae796e02be01ade:pNone:814.0-1019.0`.*

## 2. Conceitos essenciais para planejamento de demanda e reposição

### 2.1 Inventário, estoque e demanda

Os trechos consultados distinguem conceitos úteis para análise profissional:

- **Inventário**: quantitativo de bens mantidos pela empresa para suportar produção, atividades de reparo/manutenção, consumo operacional ou atendimento ao cliente.
- **Estoque (storage)**: produtos ou materiais não transitórios, mantidos para recuperação e uso posterior.
- **Demanda**: quantidade necessária de um produto ou serviço.
- **Lead time ou tempo de ressuprimento/aquisição**: tempo entre a solicitação do item e sua disponibilização para uso.

Para o contexto offshore, o tempo de ressuprimento não termina na emissão do pedido. Ele deve abranger as etapas até a disponibilização efetiva do material: compra ou separação, transferência, recebimento, eventual amostragem/inspeção/certificação e liberação para uso.

### 2.2 Excesso de demanda: backorder e perda

Quando a demanda não pode ser atendida, o sistema pode reagir de duas formas básicas:

- **Backorder/backlog**: o solicitante aceita aguardar o atendimento posterior.
- **Lost sale/perda de demanda**: o atendimento não ocorre no momento e a necessidade não espera.

Em suprimento offshore, essa distinção é relevante porque alguns materiais admitem postergação, enquanto outros podem gerar efeito operacional imediato. Em termos gerenciais, itens associados a perda de demanda, interrupção de tarefa crítica ou indisponibilidade de equipamento tendem a exigir política mais conservadora de reposição.

### 2.3 Tipos de estoque

Os estoques podem ser classificados como:

- **Cíclicos**: atendem a demanda média.
- **De segurança**: absorvem incertezas de demanda e/ou ressuprimento.
- **Sazonais**: absorvem variabilidades previsíveis.

### 2.4 Tempo de revisão do inventário

O acompanhamento do estoque pode ocorrer de duas formas:

- **Revisão contínua**: conhece-se o saldo a qualquer tempo.
- **Revisão periódica**: o saldo é revisto em intervalos predefinidos.

Essa distinção é central para materiais críticos offshore, porque define a velocidade de reação à queda do estoque.

*Fontes da seção: `regis-1f62e24eb63478f80ae2cda4:pNone:1917.0-2157.0`, `regis-661d49649682128ff1d118ca:pNone:1294.0-1470.0`.*

## 3. Trade-off entre nível de serviço, responsividade e custo

A decisão de estoque é um trade-off entre **responsividade** e **eficiência**:

- estoques maiores aumentam a probabilidade de atendimento e tornam a operação mais responsiva;
- estoques maiores também elevam custo de manutenção, capital imobilizado e risco de desperdício.

Os textos destacam que planejar estoques é balancear:

- **custos de manutenção do estoque**;
- **custos ou riscos da falta de estoque**;
- **custos de aquisição/ressuprimento**.

Portanto, para continuidade operacional em FPSO, o objetivo não é maximizar estoque, e sim atingir o nível de serviço desejado com custo total aceitável. Estoque de segurança insuficiente compromete atendimento; estoque excessivo indica possível desperdício de recursos.

### 3.1 Indicadores de serviço aplicáveis

Dois indicadores aparecem com destaque:

1. **Nível de serviço do ciclo (NSC / Cycle Service Level)**: probabilidade de não ocorrer falta durante o ciclo de ressuprimento.
2. **Disponibilidade / percentual de atendimento da demanda (Fill Rate)**: fração da demanda atendida diretamente pelo estoque disponível.

Esses indicadores não são equivalentes. Um item pode ter bom atendimento percentual e ainda apresentar faltas ocasionais em ciclos críticos. Para materiais de alto impacto operacional, a escolha do indicador-meta deve refletir a consequência da ruptura.

*Fontes da seção: `regis-1f62e24eb63478f80ae2cda4:pNone:1917.0-2157.0`, `regis-a084aafb9ae796e02be01ade:pNone:814.0-1019.0`, `regis-350f415ac736e1cd2ce4c178:pNone:4911.0-5147.0`.*

## 4. Políticas de estoque e reposição

Os trechos descrevem políticas de estoques puxados e dois modos clássicos de controle.

### 4.1 Estratégias de estoque puxado

Na lógica **pull**, a demanda orienta a reposição. Quatro abordagens são citadas:

1. **Estoque para a demanda**: mantém-se apenas o necessário para a demanda daquele ponto.
2. **Ponto de ressuprimento**: quando o saldo cai abaixo de um nível predeterminado, dispara-se um pedido.
3. **Quantidade variável / reposição periódica**: em datas fixas, calcula-se o pedido como a diferença entre um nível máximo e o estoque disponível.
4. **Just-in-time (JIT)**: aplicável quando a demanda é conhecida com elevada certeza, o tempo de ressuprimento é curto e previsível e não há vantagem em suprir quantidades maiores que as requeridas.

Os próprios textos recomendam composições entre métodos, em vez de adoção rígida de um único arranjo.

### 4.2 Revisão contínua versus revisão periódica

Segundo as fontes:

- **Quantidade fixa / revisão contínua** é mais favorável para itens caros e para componentes críticos de reposição ou reparo, pois permite resposta mais rápida à queda do estoque.
- **Período fixo / revisão periódica** tende a exigir estoques maiores, mas pode ser vantajoso quando há compras de muitos itens do mesmo fornecedor, aproveitando escala e simplificação administrativa.
- Sistemas mistos são possíveis e compatíveis com a prática logística real.

### 4.3 Implicação prática para FPSO

Sem extrapolar além das fontes, a consequência lógica para suprimento offshore é:

- materiais **críticos para continuidade operacional** tendem a requerer monitoramento mais próximo e política mais responsiva;
- materiais **menos críticos**, comprados em conjunto ou de consumo mais estável, podem admitir revisão periódica;
- **JIT puro** deve ser usado com cautela quando o lead time não é curto nem confiável.

*Fontes da seção: `regis-661d49649682128ff1d118ca:pNone:1294.0-1470.0`, `regis-350f415ac736e1cd2ce4c178:pNone:6429.0-6699.0`.*

## 5. Estoque de segurança, ponto de ressuprimento e tempo de ressuprimento

### 5.1 Estoque de segurança

O **estoque de segurança (ES)** é o estoque mantido para absorver:

1. variações de demanda acima do previsto; e/ou
2. atraso no recebimento de novo lote.

Sua função é proteger o atendimento durante o período em que a organização fica exposta às incertezas do ressuprimento. Quanto maior o estoque de segurança, maior tende a ser o nível de serviço; porém também aumentam os custos de manutenção.

### 5.2 Ponto de ressuprimento

O **ponto de ressuprimento (PR)** é o nível de estoque que dispara o pedido de um novo lote.

Em condição determinística, a fonte apresenta o conceito de que o ponto de reposição resulta da demanda média durante o lead time:

- **PR = Dm × L**

onde:

- **Dm** = demanda média no período adotado;
- **L** = lead time de pedido/ressuprimento, na mesma base temporal.

Em condição de incerteza, o ponto de reposição incorpora proteção adicional:

- **PR = Dm × L + ES**

onde **ES** é o estoque de segurança.

A coerência de unidades é obrigatória: se a demanda estiver em unidades por dia, o lead time deve estar em dias.

### 5.3 Tempo de ressuprimento

O **tempo de ressuprimento (TR ou lead time)** é o intervalo entre a solicitação do novo lote e sua disponibilização para entrega/uso. As fontes deixam claro que esse período pode incluir envio, recebimento, amostragem, certificação e liberação.

Esse conceito é decisivo em offshore porque, durante o lead time, a empresa fica exposta à incerteza da demanda. Se o estoque disponível no PR não cobrir a demanda até a chegada do lote, ocorre ruptura.

### 5.4 Inventário médio

Em um sistema com estoque de segurança, o inventário médio pode ser representado como:

- **Inventário médio = Q/2 + ES**

onde:

- **Q** = quantidade do pedido ou lote de reposição;
- **ES** = estoque de segurança.

Essa relação mostra que o estoque médio depende tanto do tamanho do lote quanto da proteção contra incerteza.

*Fontes da seção: `regis-661d49649682128ff1d118ca:pNone:1294.0-1470.0`, `regis-350f415ac736e1cd2ce4c178:pNone:4911.0-5147.0`, `regis-350f415ac736e1cd2ce4c178:pNone:6429.0-6699.0`.*

## 6. Limites dos modelos determinísticos e implicações para item crítico

Os textos alertam que o modelo de ponto de ressuprimento com lote econômico exige pressupostos fortes, como:

- demanda constante;
- capacidade de estimar custos unitários com qualidade;
- comportamento relativamente estável do ressuprimento.

Se a demanda não for constante, o lote calculado deixa de ser economicamente ótimo. Em materiais de demanda intermitente, comum em sobressalentes de manutenção, a aplicação mecânica do lote econômico pode produzir resultados insatisfatórios.

As fontes também observam que organizações frequentemente erram ao adotar regras generalistas de estoque de segurança iguais para todos os SKUs. Um mesmo número de dias de cobertura para todos os itens pode superdimensionar alguns e subdimensionar outros.

Logo, para estoque crítico em FPSO, a parametrização deve ser por item ou por famílias tecnicamente homogêneas, considerando ao menos:

- variabilidade da demanda;
- duração e confiabilidade do lead time;
- consequência da falta;
- nível de serviço desejado;
- valor do item e custo de manutenção;
- possibilidade de revisão contínua ou apenas periódica.

*Fontes da seção: `regis-661d49649682128ff1d118ca:pNone:1294.0-1470.0`, `regis-350f415ac736e1cd2ce4c178:pNone:6429.0-6699.0`, `regis-a084aafb9ae796e02be01ade:pNone:814.0-1019.0`.*

## 7. Critérios práticos de priorização de materiais para continuidade operacional

Com base nas relações explicitadas pelas fontes, a priorização profissional de materiais deve ser estruturada por consequência e por dificuldade de reposição, e não somente por valor financeiro.

### 7.1 Critérios técnicos recomendáveis

1. **Impacto da falta**
   - item cuja falta gera apenas espera administrável pode aceitar backorder;
   - item cuja falta interrompe atividade relevante ou compromete atendimento requer proteção maior.

2. **Lead time e sua confiabilidade**
   - quanto maior e menos confiável o lead time, maior tende a ser a necessidade de proteção por estoque ou maior antecedência de pedido.

3. **Variabilidade da demanda**
   - demanda estável favorece planejamento simples;
   - demanda incerta exige maior atenção ao ES e ao modo de revisão.

4. **Valor do item e custo de estocagem**
   - itens de alto valor pedem maior rigor no dimensionamento;
   - isso não significa necessariamente estoque baixo se o custo da falta for muito alto.

5. **Modelo de aquisição**
   - compras agrupadas do mesmo fornecedor podem justificar revisão periódica;
   - itens críticos de reparo/reposição favorecem revisão contínua.

### 7.2 Regra decisória coerente com as fontes

Uma regra prática consistente com os trechos é:

- **alto impacto da falta + lead time longo/incerto** → elevar prioridade, revisar continuamente, calcular PR com ES e perseguir alto nível de serviço;
- **baixo impacto da falta + fornecimento frequente/agrupável** → admitir revisão periódica e estoques menos conservadores;
- **item caro + demanda previsível + lead time curto e confiável** → considerar política mais enxuta e menor cobertura.

*Fontes da seção: `regis-1f62e24eb63478f80ae2cda4:pNone:1917.0-2157.0`, `regis-661d49649682128ff1d118ca:pNone:1294.0-1470.0`, `regis-350f415ac736e1cd2ce4c178:pNone:6429.0-6699.0`.*

## 8. Aplicação ao planejamento de demanda e reposição offshore

Para uso profissional na logística de FPSO, o encadeamento decisório pode ser resumido assim:

1. **Caracterizar o item**: consumo, função operacional, criticidade e consequência da falta.
2. **Definir o regime de controle**: revisão contínua, periódica ou mista.
3. **Medir o lead time real**: da solicitação até a liberação para uso, e não apenas até o embarque.
4. **Estimar demanda durante o lead time**.
5. **Definir o estoque de segurança** em função das incertezas e do nível de serviço desejado.
6. **Calcular o ponto de ressuprimento**.
7. **Revisar o lote de pedido** à luz do trade-off entre custo de manutenção e custo do pedido, sem presumir que o lote econômico teórico seja sempre o melhor para demanda variável.
8. **Acompanhar indicadores de serviço**: ao menos ausência de ruptura no ciclo e atendimento da demanda pelo estoque.
9. **Reparametrizar periodicamente**: mudanças de lead time, consumo, confiabilidade de fornecedor ou restrições logísticas alteram a política ótima.

### Exemplo ilustrativo 1: sobressalente crítico de manutenção

Se um sobressalente tem demanda pouco frequente, porém a falta pode impedir reparo importante e o ressuprimento é demorado, a política coerente é:

- revisão contínua;
- PR com ES;
- meta de serviço elevada;
- menor tolerância a backorder.

### Exemplo ilustrativo 2: consumível recorrente comprado em conjunto

Se vários consumíveis são adquiridos do mesmo fornecedor e a demanda é relativamente estável, pode ser mais adequado:

- revisão periódica;
- nível máximo de reposição;
- consolidação de pedidos para ganho de escala.

### Exemplo ilustrativo 3: item caro com fornecimento previsível

Quando o item é de alto valor unitário, a demanda é conhecida e o tempo de ressuprimento é curto e confiável, a empresa pode operar com estoque menor e controle mais rigoroso, aproximando-se de lógica JIT.

Esses exemplos são ilustrativos; não substituem parametrização por dados reais.

*Fontes da seção: `regis-661d49649682128ff1d118ca:pNone:1294.0-1470.0`, `regis-350f415ac736e1cd2ce4c178:pNone:4911.0-5147.0`, `regis-350f415ac736e1cd2ce4c178:pNone:6429.0-6699.0`, `regis-a084aafb9ae796e02be01ade:pNone:814.0-1019.0`.*

## 9. Síntese executiva

Para continuidade operacional offshore, a gestão de estoque crítico deve ser tratada como decisão de risco logístico. O eixo central é simples:

- a demanda durante o lead time precisa estar coberta;
- o ponto de ressuprimento deve disparar antes da ruptura;
- o estoque de segurança deve refletir incerteza e criticidade;
- revisão contínua tende a ser superior para itens críticos de reparo/reposição;
- revisão periódica pode ser eficiente para itens agrupáveis e menos críticos;
- nível de serviço maior exige mais estoque ou maior confiabilidade do ressuprimento;
- usar apenas "dias de operação" ou regras uniformes para todos os itens é tecnicamente frágil.

Em consequência, o planejamento de demanda, reposição e priorização de materiais em FPSO deve ser item a item, orientado por impacto operacional, variabilidade e lead time real de reabastecimento.

*Fontes da seção: `regis-1f62e24eb63478f80ae2cda4:pNone:1917.0-2157.0`, `regis-661d49649682128ff1d118ca:pNone:1294.0-1470.0`, `regis-a084aafb9ae796e02be01ade:pNone:814.0-1019.0`, `regis-350f415ac736e1cd2ce4c178:pNone:4911.0-5147.0`, `regis-350f415ac736e1cd2ce4c178:pNone:6429.0-6699.0`.*