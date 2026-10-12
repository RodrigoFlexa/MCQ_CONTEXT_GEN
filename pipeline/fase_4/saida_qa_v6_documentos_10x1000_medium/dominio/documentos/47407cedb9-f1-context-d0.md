# Manifolds, PLEM e PLET em sistemas submarinos associados a FPSOs

## 1. Papel dos manifolds, PLEM e PLET no arranjo submarino

Em sistemas submarinos de produção ligados a FPSOs ou outras UEPs, o arranjo subsea é formado por equipamentos no leito marinho e por linhas e interfaces que conduzem fluidos entre poços, equipamentos submarinos e a unidade de produção. Nesse contexto:

- **flowlines** são linhas acomodadas no leito marinho para escoamento entre equipamentos submarinos;
- **risers** fazem a ligação dinâmica entre o leito marinho e a unidade flutuante;
- **jumpers** são trechos curtos, rígidos ou flexíveis, usados para interligar equipamentos, por exemplo ANM–manifold, manifold–PLEM/PLET ou manifold–base de riser;
- **umbilicais** fornecem energia, potência hidráulica/elétrica, comunicação, aquisição de dados e, quando aplicável, injeção de químicos para atuação e supervisão subsea.

Nessa arquitetura, **manifolds**, **PLEMs** e **PLETs** são equipamentos de interligação e redistribuição de fluxo. Eles existem para reduzir a quantidade de linhas e risers que chegariam à UEP, organizar a coleta e/ou distribuição de fluidos e viabilizar alinhamentos operacionais mais complexos do que uma ligação direta poço-plataforma.

Em termos funcionais, o fluxo típico pode seguir a sequência:

**poço → cabeça de poço/ANM → jumper/flowline → manifold, PLEM ou PLET → flowline/riser/exportação → UEP/FPSO**.

Essa organização é especialmente relevante em águas profundas, nas quais custo de linhas, carga estrutural na UEP, logística de instalação e intervenção e confiabilidade do sistema tornam-se fatores de decisão importantes.

**Fontes da seção:** `regis-deed1f7cc601072cb57abbfb:pNone:2298.0-2552.0`, `regis-deed1f7cc601072cb57abbfb:pNone:2554.0-2764.0`, `petroles-004c2afadba7ea17c7dd7908:pNone:539578.0-539615.0`

## 2. Definições técnicas e distinções funcionais

### 2.1 Manifold submarino

O **manifold submarino** é um equipamento subsea interligado a múltiplas ANMs/poços, com a finalidade de:

- **agrupar** a produção de vários poços e enviá-la para a UEP por uma linha tronco ou **header coletor**;
- **distribuir** fluidos vindos da UEP para injeção em vários poços por meio de um **header distribuidor**;
- em algumas configurações, **combinar as funções de coleta e distribuição** em uma mesma estrutura.

Os textos consultados convergem ao tratar o manifold como um conjunto de tubulações, válvulas, chokes e instrumentação capaz de **conter pressão**, **direcionar o fluxo**, **controlar vazões** e **coletar dados de escoamento**. Em termos de classificação funcional:

- **MSP / manifold de coleta**: várias entradas convergem para um único duto/header de produção;
- **MSI / manifold de distribuição**: um duto/header de injeção alimenta várias saídas para poços;
- **MSPI / manifold misto**: reúne funções de produção e injeção na mesma instalação.

### 2.2 Header e sua importância operacional

O **header** é o duto tronco associado ao manifold:

- se **recebe** fluxos de várias linhas, atua como **header coletor**;
- se **envia** fluxo para várias linhas, atua como **header distribuidor**.

A avaliação de configuração de válvulas e alinhamentos em manifolds depende diretamente de identificar:

1. qual header está em serviço;
2. quais ramais/poços devem estar comunicados com ele;
3. quais ramais devem permanecer isolados;
4. se existe linha dedicada de teste, exportação ou injeção associada ao arranjo.

### 2.3 PLET

O **PLET (Pipeline End Termination)** é a terminação/interfacing no fim de uma linha, usado como ponto de conexão com outros equipamentos ou com trechos rígidos/flexíveis. As fontes o descrevem como um conector/interface de extremidade de linha, inclusive para ligação entre tubos rígidos e flexíveis e com outros equipamentos submarinos.

Do ponto de vista operacional, o PLET é menos um barramento de múltiplos poços e mais um **ponto estruturado de conexão, terminação e tie-in**.

### 2.4 PLEM

O **PLEM (Pipeline End Manifold)** aparece nas fontes como um equipamento de interligação no fim de uma linha e, em formulações mais detalhadas, como um **manifold de pequeno porte** ou uma extremidade de linha que pode **suportar válvulas e conexões adicionais**, servindo como ponto de junção entre linhas e outros equipamentos submarinos.

Na prática conceitual, o PLEM tende a ter função mais ativa de **manobra/distribuição/integração** do que um PLET simples, embora a nomenclatura exata e o escopo funcional dependam do projeto.

### 2.5 Interface com ANM e poço

A **ANM** é instalada na cabeça do poço e controla o fluxo de produção ou injeção. As fontes citam válvulas típicas como:

- válvula mestra de produção;
- válvula lateral de produção;
- válvula mestra do anular;
- válvula lateral do anular;
- crossover;
- válvulas de swab/pistoneio.

Na interface com manifolds, PLEM e PLET, a ANM fornece o ponto de origem ou destino do escoamento do poço, enquanto o restante do arranjo subsea define se esse fluxo será coletado, distribuído, testado, exportado ou isolado.

**Fontes da seção:** `petroles-004c2afadba7ea17c7dd7908:pNone:1185009.0-1185049.0`, `petroles-004c2afadba7ea17c7dd7908:pNone:1185029.0-1185070.0`, `regis-deed1f7cc601072cb57abbfb:pNone:2554.0-2764.0`, `petroles-004c2afadba7ea17c7dd7908:pNone:539578.0-539615.0`

## 3. Componentes relevantes para configuração de válvulas, headers e alinhamentos

Os manifolds mais completos, conforme os trechos utilizados, podem incluir:

- **sub-base**, que suporta a instalação no leito marinho e compensa irregularidades/inclinação do fundo;
- **estrutura principal**, sobre a qual ficam montadas tubulações e válvulas residentes;
- **tubulação e válvulas residentes**, associadas ao isolamento dos headers e dos módulos;
- **módulos de válvulas e/ou chokes**, removíveis para manutenção/reparo em superfície;
- **módulos de controle subsea**, correspondentes à parte submarina do sistema de controle;
- **módulos de conexão** para dutos, jumpers e umbilicais.

Também são citados:

- **SCMs/Subsea Control Modules** e monitoramento/controle subsea;
- **válvulas de bloqueio**, para isolamento de linhas, headers ou módulos;
- **válvulas de controle / chokes**, para estrangulamento e controle de escoamento;
- **transdutores de pressão e temperatura**, indicadores de posição de haste de choke e, em alguns projetos, **medidores de vazão**, inclusive multifásicos.

### Funções operacionais dos principais elementos

#### a) Válvulas de bloqueio
Usadas para:

- isolar poços, ramais, módulos ou headers;
- definir o caminho ativo do fluido;
- permitir manutenção ou retirada de módulos com menor escopo de indisponibilidade.

#### b) Chokes e válvulas de controle
Usados para:

- ajustar vazão de produção ou de injeção;
- balancear contribuição entre poços/ramais;
- controlar queda de pressão e regime de escoamento de forma compatível com os objetivos de produção e drenagem.

#### c) Headers
São o eixo do alinhamento hidráulico. A abertura/fechamento correta das derivações para o header determina se o sistema está em:

- coleta de produção;
- distribuição de água/gás de injeção;
- teste de poço;
- condição parcial de isolamento/intervenção.

#### d) Jumpers, flowlines e PLET/PLEM
São as conexões físicas que materializam o alinhamento. A lógica operacional do manifold só se realiza se essas conexões existirem e estiverem integradas ao sistema de controle.

**Fontes da seção:** `petroles-004c2afadba7ea17c7dd7908:pNone:1185029.0-1185070.0`, `petroles-004c2afadba7ea17c7dd7908:pNone:1185051.0-1185089.0`, `regis-deed1f7cc601072cb57abbfb:pNone:2298.0-2552.0`, `regis-deed1f7cc601072cb57abbfb:pNone:2554.0-2764.0`

## 4. Lógica de alinhamento operacional

A partir das definições das fontes, a análise profissional de alinhamento deve ser feita em termos de **trajetória hidráulica pretendida** e **isolamentos requeridos**. A seguir, apresenta-se uma lógica conceitual, não um procedimento universal de operação.

### 4.1 Coleta de produção em manifold de produção

Em um **manifold de coleta (MSP)**, o objetivo é encaminhar a produção de vários poços para um único header coletor e daí para a UEP.

Conceitualmente, o alinhamento exige:

- **abertura** do caminho entre cada poço selecionado e o header coletor;
- **abertura** da saída do header para a linha de exportação/produção rumo à UEP;
- **fechamento** dos ramais de poços fora de serviço ou isolados;
- **fechamento** de linhas de injeção ou teste que não devam participar da operação.

Pontos de verificação técnica:

- se todas as entradas do header estão realmente correspondendo aos poços desejados;
- se não há caminho inadvertido para uma linha de teste ou de injeção;
- se os chokes estão ajustados para evitar desequilíbrio excessivo entre poços;
- se a contrapressão no header e na linha tronco é compatível com o desempenho dos poços.

### 4.2 Distribuição de água ou gás em manifold de injeção

Em um **manifold de distribuição (MSI)**, um header distribuidor recebe fluido da UEP e o envia a múltiplos poços injetores.

Conceitualmente, o alinhamento exige:

- **abertura** da entrada de injeção no manifold/header distribuidor;
- **abertura** apenas dos ramais destinados aos poços que devem receber injeção;
- **fechamento** dos demais ramais e de linhas de produção/teste não associadas à manobra;
- ajuste dos **chokes/válvulas de controle** para repartir vazão/pressão conforme a estratégia de injeção.

Esse raciocínio vale tanto para água quanto para gás de injeção, inclusive quando o manifold é usado para compartilhar sistemas de injeção ou de gas lift entre vários poços.

### 4.3 Operação em manifold misto

No **MSPI**, produção e injeção coexistem na mesma instalação. Isso aumenta a flexibilidade, mas também eleva a criticidade do arranjo de válvulas.

A avaliação do alinhamento deve confirmar que:

- os caminhos de produção e injeção estão **segregados conforme o projeto**;
- o header coletor não está comunicado indevidamente com o header distribuidor;
- isolamentos necessários para um serviço não prejudiquem o outro além do previsto;
- a instrumentação usada para monitoramento reflete o header e o ramal efetivamente em operação.

### 4.4 Alinhamento para teste de poço

As fontes indicam a existência de **linhas de teste** e a prática de alinhar um poço ao separador de testes para determinar suas vazões por medidores monofásicos na saída do separador.

Conceitualmente, isso implica:

- selecionar **um poço** para a rota de teste;
- abrir o caminho desse poço até a **linha de teste**;
- manter os demais poços na rota normal de produção, quando o arranjo permitir;
- confirmar que o poço em teste não permaneça simultaneamente comunicado com a rota principal de produção, salvo lógica projetada específica.

As limitações operacionais apontadas pelas fontes incluem:

- baixa frequência de teste quando há muitos poços e alto tempo de estabilização;
- resultado do teste como uma fotografia momentânea, não necessariamente representativa do mês inteiro;
- possibilidade de a condição hidráulica no teste diferir da condição normal de produção;
- o separador de testes mascarar flutuações rápidas por se comportar como vaso com controle de pressão e nível;
- em alguns casos, o alinhamento para teste provocar perda de produção.

### 4.5 Alinhamento para intervenção e manutenção

Quando há **módulos removíveis** e **válvulas residentes atuadas por ROV**, a lógica operacional tende a ser:

1. isolar hidraulicamente o módulo ou trecho a ser intervencionado;
2. manter, quando possível, os headers ou demais ramais em condição segura e segregada;
3. confirmar ausência de comunicação indesejada entre produção, injeção e trecho em intervenção;
4. então proceder à retirada do módulo para manutenção em superfície.

As fontes ressaltam que a retirada de um manifold ou a indisponibilidade do equipamento pode interromper a produção de vários poços, de modo que o planejamento do alinhamento e do isolamento tem forte impacto na disponibilidade do sistema.

**Fontes da seção:** `petroles-004c2afadba7ea17c7dd7908:pNone:1185009.0-1185049.0`, `petroles-004c2afadba7ea17c7dd7908:pNone:1185029.0-1185070.0`, `petroles-004c2afadba7ea17c7dd7908:pNone:1185051.0-1185089.0`

## 5. Tipos de manifold e implicações para configuração e intervenção

As fontes citam três arranjos típicos de manifold:

- **tipo Cluster**: módulo independente ao qual os poços se conectam por jumpers; pode ser instalado antes ou durante a perfuração;
- **tipo Modular**: semelhante ao cluster, porém com maior flexibilidade e partes removíveis/trocáveis ao longo da vida útil;
- **tipo Template**: os poços podem ser conectados diretamente à estrutura do manifold.

### Implicações práticas

#### Cluster
- favorece conexão de poços satélites por jumpers;
- tende a concentrar a lógica de alinhamento no próprio manifold e em suas interfaces externas.

#### Modular
- favorece manutenção por substituição de módulos;
- torna especialmente importante a existência de válvulas residentes para isolar módulos sem retirar toda a estrutura.

#### Template
- aumenta a integração física entre poços e estrutura;
- pode alterar a estratégia de intervenção e o impacto operacional de indisponibilidades locais.

Além do tipo de manifold, as fontes distinguem arquiteturas de arranjo submarino:

1. **poços satélites com tie-back individual**;
2. **arranjo com manifold**;
3. **anel coletor/daisy chain**.

O arranjo com manifold é apontado como muito usado em águas profundas por reduzir o número de risers para a UEP, embora com eficiência operacional potencialmente inferior ao tie-back individual. Isso é relevante para avaliação de alinhamentos porque maior concentração de fluxos num único equipamento normalmente significa maior sensibilidade a falhas, manutenção e decisões de manobra.

**Fontes da seção:** `regis-deed1f7cc601072cb57abbfb:pNone:2554.0-2764.0`, `petroles-004c2afadba7ea17c7dd7908:pNone:1185029.0-1185070.0`

## 6. Monitoramento, controle e diagnóstico operacional

O manifold não é apenas um barramento hidráulico; ele também é um nó de **monitoramento e controle**. As fontes associam ao equipamento:

- monitoramento de **pressão** e **temperatura**;
- indicação de posição de **chokes**;
- medição de vazão, inclusive por **medidores multifásicos** em alguns arranjos;
- controle subsea por módulos de controle e interconexão com a UEP, usualmente por sistemas elétricos/hidráulicos via umbilical.

### Variáveis que suportam a decisão de alinhamento

Para avaliar se um alinhamento de válvulas e headers está correto, são particularmente úteis:

- pressão a montante e a jusante do header;
- temperatura do escoamento em pontos-chave;
- posição comandada e posição indicada de válvulas e chokes;
- coerência entre vazão esperada e vazão medida/estimada;
- comportamento da contrapressão imposta ao poço e ao sistema.

### Modelagem do manifold como nó hidráulico

Uma fonte técnica destaca que o sistema de produção pode ser representado em simuladores por tabelas de **Fluxo Vertical Multifásico (FVM)**, relacionando pressão de fundo do poço a vazão de líquido, RGO, corte de água e pressão no nó a jusante, que pode ser a pressão na cabeça do poço, no manifold submarino ou no header na plataforma.

No exemplo citado, três poços produzem para um manifold e deste para um separador/UEP, o que é representado por quatro relações FVM: três do poço ao manifold e uma do manifold ao separador. O ponto essencial para a operação é que o manifold/header impõe **contrapressão** aos poços; portanto, mudanças de alinhamento, abertura de poços adicionais ou alteração de choke podem modificar o desempenho de todo o conjunto.

Essa abordagem de modelagem é útil para:

- prever impacto de diferentes combinações de poços abertos no mesmo header;
- identificar gargalos hidráulicos no manifold ou na linha tronco;
- avaliar benefício de alterar o caminho do fluido ou redistribuir vazões;
- integrar produção, reservatório e processamento em estudos de tomada de decisão.

**Fontes da seção:** `petroles-004c2afadba7ea17c7dd7908:pNone:1185009.0-1185049.0`, `regis-deed1f7cc601072cb57abbfb:pNone:2298.0-2552.0`, `regis-55ed1aa71679e71313f60cf6:pNone:908.0-1185.0`

## 7. Efeitos de projeto e operação sobre escoamento, disponibilidade e integridade operacional

As fontes apontam vantagens recorrentes do uso de manifolds:

- redução do comprimento total de linhas;
- redução do número de risers conectados à UEP;
- redução de carga e espaço necessários na unidade;
- potencial de otimização do arranjo submarino e da antecipação de produção.

Também apontam desvantagens e trade-offs relevantes:

- atraso potencial associado a licitação, fabricação e instalação do manifold;
- risco de impacto coletivo: indisponibilidade do manifold pode afetar vários poços;
- maior exigência quanto à confiabilidade de componentes e facilidade de manutenção;
- possível deficiência na coleta individual de dados dos poços quando a produção é agrupada.

### Influência no escoamento e na garantia operacional

Uma observação importante das fontes é que a concentração da produção em uma única tubulação pode elevar a conservação de calor do escoamento, o que pode levar a:

- menores viscosidades e menores perdas por fricção;
- menor tendência à parafinação das linhas;
- menor risco de formação de hidratos em paradas, em razão de maiores tempos de resfriamento.

Esses efeitos são relevantes para a avaliação de alinhamentos, porque a abertura ou fechamento de rotas pode alterar não só vazão e pressão, mas também o regime térmico e o comportamento de escoamento no conjunto manifold–flowline–riser.

Por outro lado, as fontes lembram que a modelagem simplificada em simuladores de reservatório não substitui estudos dedicados aos fenômenos de escoamento em dutos, gradientes de pressão/temperatura, hidratos, parafina e gargalos. Assim, decisões operacionais de alinhamento devem ser compatíveis com análises específicas de garantia de escoamento quando a criticidade justificar.

**Fontes da seção:** `petroles-004c2afadba7ea17c7dd7908:pNone:1185029.0-1185070.0`, `petroles-004c2afadba7ea17c7dd7908:pNone:1185051.0-1185089.0`, `regis-55ed1aa71679e71313f60cf6:pNone:908.0-1185.0`

## 8. Síntese prática para avaliação profissional de configuração de válvulas, headers e alinhamentos

Sem transformar um arranjo particular em regra universal, a análise técnica de um manifold, PLEM ou PLET deve responder, no mínimo, às seguintes perguntas:

1. **Qual é a função ativa da instalação neste momento?**
   - coleta de produção;
   - distribuição de injeção;
   - operação mista;
   - teste de poço;
   - isolamento para intervenção.

2. **Qual header está em serviço?**
   - coletor, distribuidor ou ambos em serviços segregados.

3. **Quais ramais devem estar comunicados com o header ativo?**
   - somente os poços/linhas previstos para aquela operação.

4. **Quais válvulas devem estar fechadas para impedir comunicação indevida?**
   - ramais fora de serviço;
   - rotas de teste não selecionadas;
   - rotas de injeção durante produção, e vice-versa, salvo arranjo projetado específico.

5. **Os instrumentos confirmam o alinhamento hidráulico esperado?**
   - pressões coerentes;
   - temperaturas coerentes;
   - posição de válvulas/chokes consistente com o comando;
   - vazões compatíveis com o estado declarado do sistema.

6. **Há impacto sistêmico aceitável?**
   - contrapressão nos poços;
   - carga térmica e risco de escoamento;
   - disponibilidade do conjunto em caso de manutenção;
   - consequência operacional de falha em módulo, choke, válvula residente ou linha tronco.

Em suma, **manifolds** são nós de coleta/distribuição e controle; **PLETs** são interfaces de terminação/conexão de linha; **PLEMs** são extremidades de linha com função ampliada de interligação/manobra, podendo assumir caráter de pequeno manifold. A correta configuração de válvulas e headers é o que transforma essa arquitetura física em um sistema seguro e funcional para produção, injeção, teste e intervenção.

**Fontes da seção:** `petroles-004c2afadba7ea17c7dd7908:pNone:1185009.0-1185049.0`, `petroles-004c2afadba7ea17c7dd7908:pNone:1185029.0-1185070.0`, `petroles-004c2afadba7ea17c7dd7908:pNone:1185051.0-1185089.0`, `regis-deed1f7cc601072cb57abbfb:pNone:2554.0-2764.0`, `regis-55ed1aa71679e71313f60cf6:pNone:908.0-1185.0`