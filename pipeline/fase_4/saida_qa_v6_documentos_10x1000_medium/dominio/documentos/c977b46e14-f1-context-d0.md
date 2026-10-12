# Desidratação e ponto de orvalho no tratamento do gás produzido em FPSOs

## 1. Finalidade da desidratação do gás
A desidratação do gás natural produzido tem três objetivos operacionais centrais em instalações offshore:

1. **atender à especificação de qualidade do gás** para consumo, exportação ou integração com outras etapas do processo;
2. **reduzir corrosão** em dutos, risers, equipamentos de compressão e vasos;
3. **prevenir formação de hidratos**, que pode bloquear choke lines, kill lines, dutos de transporte e outras linhas de gás.

Em plataformas offshore, o condicionamento do gás deve ser visto como parte de uma cadeia integrada de separação primária, compressão, resfriamento/depuração e desidratação. A remoção de água não é apenas uma exigência comercial; ela condiciona a confiabilidade de todo o sistema de gás, inclusive gás combustível, gas lift, exportação e reinjeção. Há referência de aplicação offshore em que o gás na saída da torre de TEG deve atingir **ponto de orvalho de água de -15 °C**, e também há referência a especificação de **4 lb/MMscf** como limite de água para corrente de gás seco/venda em um caso simulado. Esses valores são exemplos de aplicação e não devem ser tomados como regra universal para qualquer FPSO.

**Fontes:** `petroles-004c2afadba7ea17c7dd7908:pNone:400189.0-400230.0`, `regis-95ab3f5dbd0879a0e75967a9:pNone:236.60-270.120`, `regis-b481bf065addf6ea2a64713f:pNone:2199.0-2302.0`

## 2. Conceitos de teor de água, ponto de orvalho e ponto de hidrato
O desempenho da desidratação pode ser expresso de formas diferentes, conforme a necessidade operacional:

- **teor de água no gás**: usualmente em lb/MMscf ou mg/m³;
- **ponto de orvalho de água (Water Dew Point, WDP)**: temperatura à qual a água começa a condensar para uma dada pressão;
- **ponto de hidrato**: condição em que, na presença de água livre e componentes formadores, pode ocorrer formação de hidratos.

Fontes históricas de Petrolês/REGIS destacam que, para operação e processamento, muitas vezes é mais útil expressar a desidratação em termos de **depressão do ponto de hidrato** do que apenas por teor de vapor d’água. A depressão do ponto de hidrato é a diferença entre a temperatura de formação de hidrato antes e depois do tratamento. Em termos práticos, quanto mais seco o gás, menor a probabilidade de condensação de água e de formação de hidratos nas condições de pressão e temperatura de transporte.

A eficiência de remoção de água depende principalmente de:

- **temperatura e pressão do sistema**;
- **contato gás-líquido** na absorção;
- **concentração do glicol**;
- **taxa de circulação do glicol**;
- **características do desidratante**.

Em soluções higroscópicas, a pressão de vapor da água diminui com:

- **redução da temperatura da solução**;
- **aumento da concentração do desidratante**.

Isso ajuda a explicar por que a qualidade do glicol pobre e a temperatura de contato influenciam diretamente o ponto de orvalho do gás tratado.

**Fontes:** `petroles-004c2afadba7ea17c7dd7908:pNone:902687.0-902750.0`, `regis-b481bf065addf6ea2a64713f:pNone:2199.0-2302.0`, `regis-c432d8f1ec9b5ecdc08954bc:pNone:692.0-853.0`

## 3. Integração da desidratação com separação e compressão
A torre de TEG não deve ser tratada como equipamento isolado. Seu desempenho depende fortemente da **qualidade da separação gás-líquido a montante**.

Separadores bifásicos/trifásicos e eliminadores de névoa têm a função de remover:

- água livre;
- condensado de hidrocarbonetos;
- gotículas arrastadas;
- em alguns casos, sólidos.

Separadores ineficientes ou subdimensionados podem permitir **carryover de líquidos e partículas**, com consequências como:

- dano ou redução de confiabilidade em compressores;
- contaminação do solvente glicol;
- espuma na torre ou no regenerador;
- piora do ponto de orvalho do gás tratado;
- aumento de perdas de glicol por arraste.

Na cadeia de compressão offshore, é comum a sequência **resfria, depura e comprime** entre estágios. O resfriamento condensa parte da água e dos hidrocarbonetos mais pesados; os vasos depuradores/scrubbers removem esse condensado antes do estágio seguinte. Isso reduz carga sobre a unidade de desidratação e melhora estabilidade operacional.

Há também referência específica para sistemas de adsorção em peneiras moleculares: antes dos leitos, usam-se **resfriador do gás de entrada**, **vaso depurador vertical** e **filtros coalescedores**, justamente para impedir entrada de condensado e proteger o adsorvente. O mesmo raciocínio de proteção é plenamente aplicável ao circuito de TEG: líquido livre a montante degrada desempenho, aumenta perdas e contamina o solvente.

**Fontes:** `petroles-004c2afadba7ea17c7dd7908:pNone:400189.0-400230.0`, `petroles-004c2afadba7ea17c7dd7908:pNone:1189813.0-1189859.0`, `regis-95ab3f5dbd0879a0e75967a9:pNone:236.60-270.120`, `petroles-004c2afadba7ea17c7dd7908:pNone:3156618.0-3156651.0`

## 4. Desidratação por absorção com glicol
### 4.1. Escolha do glicol
Os glicóis citados para desidratação de gás natural são:

- **MEG (monoetilenoglicol)**;
- **DEG (dietilenoglicol)**;
- **TEG (trietilenoglicol)**.

No contexto de FPSOs e condicionamento de gás por absorção, o **TEG é o solvente mais associado à torre contactora**, por combinar:

- alta afinidade por água;
- baixa volatilidade relativa frente a glicóis mais leves;
- maior facilidade de regeneração a altas concentrações;
- menor perda por vaporização do que solventes mais leves;
- boa aplicabilidade industrial em unidades de absorção.

O **MEG** aparece fortemente associado à **inibição de hidratos em linhas**, pontos frios e correntes submetidas a refrigeração posterior, com recuperação/regeneração em circuito dedicado. Seu uso como desidratante de contato em torre é menos característico do arranjo clássico de desidratação de gás com TEG. Fontes antigas também discutem **EG/DEG** em separação a baixa temperatura, destacando vantagens de custo e viscosidade, mas com maior pressão de vapor e perdas mais elevadas em comparação com glicóis mais pesados.

### 4.2. Mecanismo na torre contactora
Na absorção com TEG, o **gás úmido** entra pela parte inferior/lateral inferior da torre absorvedora (contactora), enquanto o **glicol pobre** entra pela parte superior. O contato ocorre em **contracorrente**. À medida que o gás sobe, o TEG absorve a água do gás; o gás desidratado sai pelo topo e o **TEG rico** em água deixa o fundo da torre para regeneração.

A eficiência do processo depende da capacidade de contato entre gás e solvente. O material fonte enfatiza que a principal resistência à absorção está do lado gasoso, na interface gás-líquido. Em termos operacionais, isso reforça a importância de boa distribuição de líquido, ausência de canalização e manutenção da condição hidráulica adequada do leito/recheio/internos.

### 4.3. Propriedades desejáveis do solvente
As fontes destacam como desejáveis em um absorvente líquido para desidratação:

- alta afinidade pela água;
- baixa pressão de vapor;
- baixa solubilidade em hidrocarbonetos;
- baixa tendência à espuma;
- estabilidade química;
- fácil regeneração;
- viscosidade moderada;
- baixa corrosividade.

**Fontes:** `petroles-004c2afadba7ea17c7dd7908:pNone:400209.0-400256.0`, `petroles-004c2afadba7ea17c7dd7908:pNone:1189813.0-1189859.0`, `petroles-004c2afadba7ea17c7dd7908:pNone:902687.0-902750.0`, `petroles-004c2afadba7ea17c7dd7908:pNone:902751.60-902803.0`, `regis-c432d8f1ec9b5ecdc08954bc:pNone:692.0-853.0`

## 5. Circuito de glicol e regeneração
O circuito de TEG opera em malha fechada: a corrente rica em água é retirada do fundo da absorvedora, pré-aquecida e encaminhada ao sistema de regeneração; depois retorna como **glicol pobre** para a torre.

As fontes descrevem regeneração com:

- **pré-aquecimento** da corrente rica;
- passagem por **coluna de stripping** ou arranjo equivalente;
- **refervedor/reboiler**, cujo vapor promove o arraste da água absorvida;
- retorno do glicol regenerado ao circuito de absorção.

Pontos técnicos relevantes para o circuito:

1. **Concentração do glicol pobre** é variável crítica. Quanto mais concentrado, maior a força motriz para absorção de água; porém concentrações muito elevadas podem exigir maior severidade térmica na regeneração e aumentar perdas e degradação.
2. **Temperatura de regeneração** deve ser suficiente para remover água, mas sem superaquecer o glicol a ponto de aumentar decomposição ou perdas por vaporização.
3. **Eficiência do resfriamento/condensação no topo do regenerador** reduz emissões e perdas de glicol por vapores.
4. **Contaminação do glicol** por hidrocarbonetos, sólidos, gases ácidos ou oxigênio reduz desempenho e aumenta risco de espuma, corrosão e degradação.

Fontes antigas citam ainda que o desempenho da desidratação com glicol depende fundamentalmente de três capacidades: **contato**, **regeneração** e **concentração do glicol na circulação**.

**Fontes:** `petroles-004c2afadba7ea17c7dd7908:pNone:400209.0-400256.0`, `petroles-004c2afadba7ea17c7dd7908:pNone:902687.0-902750.0`, `petroles-004c2afadba7ea17c7dd7908:pNone:902751.60-902803.0`, `petroles-004c2afadba7ea17c7dd7908:pNone:1787661.0-1787701.0`

## 6. Variáveis de controle que governam o ponto de orvalho
Pelo material fornecido, o controle do teor de água no gás tratado e do circuito de glicol gira em torno de algumas variáveis de processo-chave.

### 6.1. Temperatura de contato
A temperatura na absorvedora afeta o equilíbrio água-glicol-gás. Fontes operacionais relatam que o ajuste da **temperatura de entrada do gás** e da **temperatura do glicol na torre** é crítico; também indicam a prática de operar o glicol a temperatura ligeiramente acima da do gás, embora os valores exatos do caso citado não estejam totalmente legíveis.

Em termos físicos:

- contato excessivamente quente tende a prejudicar a capacidade de absorção de água;
- contato excessivamente frio pode aumentar risco de condensação/localização de líquidos e piorar o comportamento hidráulico, dependendo do arranjo.

### 6.2. Pressão do sistema
Pressão afeta equilíbrio de fases, teor de água de saturação e condições de formação de hidratos. Mudanças de pressão ao longo da compressão e do resfriamento alteram a quantidade de água que permanece no gás e a carga sobre a torre.

### 6.3. Vazão de gás
Mudanças de vazão alteram tempo de contato, regime hidráulico e potencial de arraste. Um estudo de simulação dinâmica mostrou que perturbações na vazão de alimentação deslocam a fração molar de água remanescente no gás seco; embora as tendências reportadas nesse caso específico sejam contraintuitivas, o ponto útil para operação é que **transientes de vazão deslocam o ponto de orvalho e exigem monitoramento dinâmico**, não apenas verificação em regime estacionário.

### 6.4. Vazão de glicol
A taxa de circulação deve ser suficiente para remover a água especificada, mas não tão alta a ponto de elevar consumo de bombeamento, arraste, perdas e eventual piora do desempenho global por maior carryover de TEG. Fontes clássicas observam que o ajuste prático pode ser feito acompanhando o ponto de hidrato ou o ponto de orvalho do gás tratado:

- se o gás estiver **mais seco do que o necessário**, pode haver margem para reduzir a circulação;
- se o gás estiver **fora de especificação**, deve-se avaliar primeiro a qualidade da regeneração e depois a taxa de circulação.

### 6.5. Pureza do TEG pobre e do TEG rico
A análise de pureza do TEG é citada como forma de monitoramento do sistema. Mesmo com lacunas numéricas na fonte, a lição operacional é clara: a diferença de composição entre **glicol pobre** e **glicol rico** permite verificar se a absorção e a regeneração estão coerentes com a carga de água e com a condição da unidade.

**Fontes:** `petroles-004c2afadba7ea17c7dd7908:pNone:1787661.0-1787701.0`, `petroles-004c2afadba7ea17c7dd7908:pNone:902687.0-902750.0`, `petroles-004c2afadba7ea17c7dd7908:pNone:902751.60-902803.0`, `regis-b481bf065addf6ea2a64713f:pNone:2199.0-2302.0`, `regis-c432d8f1ec9b5ecdc08954bc:pNone:692.0-853.0`

## 7. Estimativa simplificada da taxa de circulação do glicol
Uma forma simplificada de estimar a circulação de glicol é por **balanço de massa**, assumindo:

- perdas de glicol desprezíveis;
- toda a água removida do gás entrando na corrente rica;
- composição expressa como fração mássica de glicol na solução.

Se:

- \(S\) = vazão mássica da solução de glicol pobre;
- \(W\) = vazão mássica de água absorvida do gás;
- \(x_L\) = fração mássica de glicol na solução pobre;
- \(x_R\) = fração mássica de glicol na solução rica;

então o balanço simplificado de glicol é:

\[
x_L \cdot S = x_R \cdot (S + W)
\]

Logo,

\[
S = \frac{x_R \cdot W}{x_L - x_R}
\]

Essa relação aparece implicitamente nos exemplos comparativos de EG e DEG das fontes históricas. Ela é útil para **primeira estimativa** de circulação, mas não substitui projeto detalhado, porque não considera explicitamente:

- perdas por vaporização/arraste;
- eficiência real de contato na torre;
- espuma e contaminação;
- variações de temperatura e pressão ao longo do circuito;
- limitações de hidráulica e turndown.

A mesma fonte reforça que a quantidade de água a ser removida depende do teor inicial de água do gás e da especificação final requerida. Portanto, o cálculo de circulação sempre deve ser amarrado a uma meta de ponto de orvalho ou teor de água na saída.

**Fontes:** `regis-c432d8f1ec9b5ecdc08954bc:pNone:692.0-853.0`, `petroles-004c2afadba7ea17c7dd7908:pNone:902687.0-902750.0`, `petroles-004c2afadba7ea17c7dd7908:pNone:902751.60-902803.0`

## 8. Perdas de glicol, contaminação e degradação
As fontes destacam que perdas de glicol têm impacto econômico e operacional relevante. As causas principais incluem:

- **vaporização e carreamento no fluxo de gás tratado**;
- **dissolução ou emulsão em hidrocarbonetos líquidos**;
- **decomposição térmica ou química**;
- **vazamentos**;
- **espuma**, muitas vezes associada à contaminação.

### 8.1. Mecanismos operacionais típicos
- **Gás muito carregado de gotículas na saída da absorvedora** pode arrastar TEG.
- **Temperatura inadequada** no regenerador aumenta perdas e degradação.
- **Contaminação por hidrocarbonetos líquidos e sólidos** favorece espuma.
- **Presença de CO2 e H2S**, absorvidos pelo glicol, pode reduzir pH e elevar corrosividade.
- **Contato com oxigênio** e superaquecimento aceleram decomposição.

### 8.2. Medidas corretivas e preventivas
As medidas apontadas pelas fontes incluem:

- manter separação eficiente de líquidos antes da torre;
- usar dispositivos de separação/aglutinação para reduzir carryover;
- controlar adequadamente a regeneração, sem excesso de calor;
- manter bom desempenho do resfriamento/condensação no topo do regenerador;
- filtrar o glicol periodicamente;
- verificar pH periodicamente e mantê-lo em faixa operacional adequada, evitando tanto acidez excessiva quanto excesso de basicidade que favoreça espuma;
- usar antiespumantes/neutralizantes quando tecnicamente justificado.

Como síntese operacional: **gás fora de especificação e perda elevada de TEG frequentemente compartilham causas-raiz comuns**, principalmente falha de separação a montante, regeneração inadequada, circulação mal ajustada e contaminação do solvente.

**Fontes:** `petroles-004c2afadba7ea17c7dd7908:pNone:902751.60-902803.0`, `regis-95ab3f5dbd0879a0e75967a9:pNone:236.60-270.120`, `petroles-004c2afadba7ea17c7dd7908:pNone:1189813.0-1189859.0`

## 9. Monitoramento de desempenho e solução de problemas
Para avaliar o desempenho do circuito de glicol, o material permite organizar um conjunto prático de verificações.

### 9.1. Indicadores primários
- teor de água ou ponto de orvalho do gás seco;
- composição/pureza do TEG pobre e do TEG rico;
- temperatura de entrada do gás e do glicol na absorvedora;
- condição de separadores/scrubbers a montante;
- estabilidade da vazão de gás e da circulação de TEG.

### 9.2. Sinais típicos de problema
**a) Gás tratado fora de especificação de água**
- glicol pobre com baixa concentração;
- regeneração insuficiente;
- circulação inadequada;
- aumento súbito da carga de água por mudança de pressão/temperatura/compressão;
- contaminação do glicol;
- mau contato na torre.

**b) Perdas elevadas de TEG**
- arraste no topo da absorvedora;
- espuma;
- temperatura de regeneração excessiva;
- condensação ineficiente de vapores do regenerador;
- presença de hidrocarbonetos líquidos no circuito.

**c) Aumento de corrosão no circuito**
- absorção de gases ácidos no glicol;
- pH inadequado;
- água residual excessiva no gás ou no solvente;
- degradação/oxidação do glicol.

**d) Formação de hidratos a jusante mesmo com TEG em operação**
- desidratação insuficiente para a condição real de pressão e temperatura;
- mudança de envelope operacional após compressão/resfriamento;
- necessidade de complementar com inibidor químico em trechos frios ou críticos;
- necessidade de tecnologia mais severa de secagem.

### 9.3. Papel de simulação dinâmica e treinamento
Uma fonte destaca o uso de **modelo dinâmico online** para previsão de eventos, treinamento de operadores e suporte à decisão sobre controle avançado. Para desidratação, isso é particularmente útil em partidas, paradas e perturbações de vazão/composição, quando o comportamento do sistema não é instantâneo e o ponto de orvalho pode sair temporariamente da meta.

**Fontes:** `petroles-004c2afadba7ea17c7dd7908:pNone:1787661.0-1787701.0`, `regis-b481bf065addf6ea2a64713f:pNone:2199.0-2302.0`, `regis-95ab3f5dbd0879a0e75967a9:pNone:236.60-270.120`, `petroles-004c2afadba7ea17c7dd7908:pNone:902751.60-902803.0`

## 10. Quando TEG pode ser insuficiente: peneiras moleculares
Embora o foco desta faceta seja o circuito de glicol, as fontes registram que **peneiras moleculares** ganharam relevância em cenários que exigem **ponto de orvalho de água muito baixo**, incluindo aplicações associadas a membranas e a exportação de gás em condições severas.

Pontos principais do material:

- peneiras moleculares são adsorventes físicos com alta capacidade e seletividade para água;
- o sistema requer pelo menos dois leitos, para alternar **adsorção** e **regeneração**;
- a regeneração usa fração do próprio gás seco aquecida, seguida de resfriamento e separação da água condensada;
- para FPSOs é citada a configuração **2:1** como usual em algumas aplicações offshore: dois leitos adsorvendo e um regenerando, favorecendo continuidade operacional e modularização;
- é essencial proteger os leitos com **depuradores e filtros coalescedores** contra arraste de líquidos.

Em termos de decisão de processo, o TEG atende uma grande faixa de aplicações, mas pode ser insuficiente quando a especificação de água é extremamente severa ou quando as condições de pressão/temperatura do escoamento tornam necessário um gás mais seco do que o alcançável economicamente com glicol.

**Fontes:** `petroles-004c2afadba7ea17c7dd7908:pNone:400209.0-400256.0`, `petroles-004c2afadba7ea17c7dd7908:pNone:3156618.0-3156651.0`

## 11. Síntese para operação de FPSO
Para manter o gás dentro de especificação de água e preservar o desempenho do circuito de TEG, a lógica operacional consolidada pelo material é:

1. **separar bem os líquidos e sólidos a montante**;
2. **estabilizar pressão, temperatura e vazão** dentro da faixa de projeto;
3. **assegurar boa qualidade do glicol pobre** por regeneração eficaz, sem superaquecer;
4. **ajustar circulação de glicol** de acordo com a carga real de água e com a meta de ponto de orvalho;
5. **minimizar perdas e contaminação** do solvente;
6. **monitorar continuamente o gás seco e o estado do circuito** por análises, temperaturas e tendências dinâmicas;
7. **reavaliar a tecnologia** quando o alvo de ponto de orvalho estiver além da capacidade prática do TEG.

Essa síntese é compatível com o uso do TEG como tecnologia-base de desidratação em FPSOs, sem excluir a necessidade de integração com compressão, inibição química em trechos críticos e, em casos de especificação severa, adsorção em peneiras moleculares.

**Fontes:** `petroles-004c2afadba7ea17c7dd7908:pNone:400189.0-400230.0`, `petroles-004c2afadba7ea17c7dd7908:pNone:1189813.0-1189859.0`, `petroles-004c2afadba7ea17c7dd7908:pNone:902687.0-902750.0`, `petroles-004c2afadba7ea17c7dd7908:pNone:902751.60-902803.0`, `regis-95ab3f5dbd0879a0e75967a9:pNone:236.60-270.120`