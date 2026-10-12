# Garantia de escoamento em linhas submarinas

## 1. Contexto técnico e escopo operacional
*Fontes: `regis-675f59687b517be845d5bb41:pNone:934.0-1197.0`, `petroles-004c2afadba7ea17c7dd7908:pNone:2015282.0-2015327.60`*

Em sistemas submarinos associados à produção offshore, o escoamento dos fluidos ocorre ao longo de poços, árvores de natal molhadas, linhas submarinas, manifolds, risers e interfaces com a unidade de produção. Do ponto de vista de garantia de escoamento, o problema central é manter a capacidade de transporte do sistema sem perda relevante de vazão, sem bloqueios e sem submeter linhas e equipamentos a condições operacionais inadequadas.

As fontes destacam que flowlines conectam equipamentos submarinos e que umbilicais integram o sistema de controle e de injeção química, transmitindo potência/sinais e levando fluidos para injeção química nos poços e equipamentos submarinos. Isso é relevante porque a prevenção e a mitigação de deposições e plugs dependem não apenas da geometria hidráulica da linha, mas também da disponibilidade de medição, comando e injeção química subsea.

Em desenvolvimentos tipo **tie-back**, especialmente de longas distâncias e em águas profundas, a garantia de escoamento torna-se mais crítica por dois motivos principais:

- a pressão disponível do reservatório e do sistema deve sustentar a produção por longos trechos;
- a perda térmica ao ambiente marinho favorece a aproximação da temperatura do fluido à temperatura do fundo do mar, elevando o risco de hidratos, parafinas e asfaltenos.

Embora parte do material mencione arranjos subsea-to-shore, os mecanismos físicos e as decisões operacionais descritos são aplicáveis, em termos conceituais, a linhas submarinas conectadas a FPSOs, desde que se respeitem as diferenças de fluido, distância, profundidade, isolamento térmico e filosofia operacional.

## 2. Conceito de garantia de escoamento e classes de problemas
*Fontes: `regis-dde44a51a227cfcb99b72f1a:pNone:1728.0-1986.0`, `regis-675f59687b517be845d5bb41:pNone:1201.0-1412.0`, `petroles-004c2afadba7ea17c7dd7908:pNone:2015282.0-2015327.60`*

As fontes convergem ao definir **garantia de escoamento** como o conjunto de atividades e estratégias de **previsão, prevenção, mitigação e remoção** de depósitos e de outros fenômenos que reduzam ou interrompam a capacidade de escoamento de um sistema de produção de óleo e gás.

Os principais mecanismos citados são:

- **deposições orgânicas**: hidratos, parafinas e asfaltenos;
- **deposições inorgânicas**: incrustações minerais, como sulfatos e carbonatos;
- **outros degradadores do escoamento/integridade**: corrosão, erosão por areia, baixa fluidez do óleo, emulsões e intermitência severa.

As consequências técnicas incluem:

- aumento de perda de carga;
- redução de vazão;
- aumento da potência requerida para escoar ou bombear;
- restrições operacionais em partida, parada e retomada;
- obstrução parcial ou total da linha;
- necessidade de intervenção, limpeza ou remediação corretiva.

O material também ressalta que a garantia de escoamento precisa ser tratada **desde o projeto até a fase produtiva**. Não basta dimensionar a linha apenas pela diferença de pressão; é necessário incorporar aspectos operacionais e transientes, como abertura/fechamento de poços, bloqueio de válvulas, shut-downs e retomada da produção.

## 3. Dependência do problema com o fluido e com o trajeto P-T
*Fontes: `regis-675f59687b517be845d5bb41:pNone:1201.0-1412.0`, `regis-dde44a51a227cfcb99b72f1a:pNone:1728.0-1986.0`*

Um ponto importante das fontes é que o risco de deposição não depende apenas da geometria da linha, mas do **tipo de fluido** e do **trajeto de pressão e temperatura** desde o reservatório até a planta de processamento.

Aspectos relevantes:

- óleos com °API semelhantes podem apresentar comportamentos diferentes de garantia de escoamento, devido à composição, complexidade das cadeias de hidrocarbonetos e impurezas;
- asfaltenos e parafinas tendem a ser mais frequentes em certos sistemas com óleos mais leves, mas isso não elimina a necessidade de ensaios específicos por fluido;
- a produção em águas profundas expõe a linha a **altas pressões e baixas temperaturas**, combinação particularmente desfavorável para hidratos e outros sólidos.

Por isso, as fontes recomendam explicitamente o uso de **análises laboratoriais em amostras representativas** e de **simulação térmica/hidráulica**, para selecionar soluções técnica e economicamente viáveis. Em termos práticos, isso significa que frequências de pigagem, necessidade de inibidor, nível de isolamento térmico e procedimentos de parada/retomada não devem ser fixados por analogia simples entre ativos.

## 4. Hidratos: mecanismo, critérios de risco e implicações operacionais
*Fontes: `regis-675f59687b517be845d5bb41:pNone:1201.0-1412.0`, `regis-dde44a51a227cfcb99b72f1a:pNone:1728.0-1986.0`, `regis-dde44a51a227cfcb99b72f1a:pNone:1860.0-2091.0`, `petroles-004c2afadba7ea17c7dd7908:pNone:2015282.0-2015327.60`*

### 4.1 Definição e condições de formação
Os hidratos são descritos como sólidos cristalinos semelhantes a gelo, formados por água e componentes gasosos de baixa massa molecular. Em sistemas submarinos, sua formação é favorecida por quatro condições simultâneas:

1. alta pressão;
2. baixa temperatura;
3. presença de água;
4. presença de gás.

A eliminação de pelo menos uma dessas condições reduz ou impede a formação.

As fontes enfatizam que, em sistemas produtores de gás, um dos maiores riscos de garantia de escoamento é o **plugue de hidrato**, capaz de bloquear a linha de produção.

### 4.2 Envelope de hidrato e sub-resfriamento
A avaliação do risco pode ser feita por meio da **curva de dissociação/formação de hidrato** em um gráfico de pressão versus temperatura. Segundo a fonte, a região de formação fica **acima/à esquerda da curva**; fora dessa região, o risco termodinâmico é reduzido.

Um conceito operacional útil é o **sub-resfriamento**:

**ΔTsub = Tequilíbrio − Toperação**

onde:

- **Tequilíbrio** = temperatura sobre a curva de formação/dissociação para a pressão considerada;
- **Toperação** = temperatura real de operação dentro do envelope.

Quanto maior o ΔTsub, mais rápida tende a ser a formação dos cristais. Portanto, duas linhas podem estar ambas em região de risco, mas a mais profundamente inserida no envelope terá maior severidade de formação.

### 4.3 Consequências práticas
As consequências operacionais descritas incluem:

- aderência/aglomeração nas paredes internas da tubulação;
- formação de bloqueio parcial ou total;
- dificuldade de dissociação, porque a remoção demanda aporte de calor e o ambiente de águas profundas é frio;
- necessidade de procedimentos corretivos potencialmente longos e de alto impacto na produção.

### 4.4 Prevenção e mitigação
As fontes citam as seguintes abordagens:

- **injeção de inibidores químicos**, como álcool, glicol, MEG e metanol, para alterar as condições de formação;
- **redução da perda de calor**, por isolamento térmico e soluções construtivas adequadas;
- **remoção de parte da água** do sistema, quando aplicável;
- uso de **modelagem térmica/hidráulica e termodinâmica integrada**, inclusive para cenários transientes.

Um ponto relevante é que a preocupação operacional não é apenas prever a nucleação, mas impedir que o sólido formado se aglomere e adira à superfície interna a ponto de comprometer o escoamento.

### 4.5 Remediação
Como medida corretiva, a fonte cita a **despressurização da linha** para alterar as condições de estabilidade do hidrato. Entretanto, isso deve ser feito com cautela, pois uma redução inadequada de pressão pode favorecer a formação de plugs/pistões de hidrato durante a manobra. Em outras palavras, a despressurização pode ser remédio ou agravante, dependendo do procedimento adotado.

## 5. Asfaltenos, parafinas, incrustações e restrições associadas
*Fontes: `regis-dde44a51a227cfcb99b72f1a:pNone:1860.0-2091.0`, `regis-dde44a51a227cfcb99b72f1a:pNone:1728.0-1986.0`, `petroles-004c2afadba7ea17c7dd7908:pNone:2089667.0-2089711.0`*

### 5.1 Asfaltenos
As fontes descrevem os asfaltenos como frações de elevada massa molar que podem se depositar nas paredes dos dutos. A tendência de deposição aumenta quando a mistura atinge o **ponto de bolha** e há liberação de fase gasosa, alterando a composição do fluido.

Implicações:

- aumento de rugosidade e perda de carga;
- redução de área útil de escoamento;
- possibilidade de deposição também em regiões porosas próximas ao poço, em função da queda de pressão.

Estratégias citadas:

- **prevenção** por injeção de inibidores em região do poço onde a pressão esteja acima do ponto de bolha, mantendo os asfaltenos em solução;
- **remoção** por passagem de **PIGs** nas linhas de produção.

A fonte ainda registra estudo segundo o qual aumento da velocidade do fluido e redução da temperatura superficial da coluna diminuíram a taxa de deposição em um caso avaliado. Isso é útil como insight, mas não deve ser generalizado sem validação específica do fluido e do regime de escoamento.

### 5.2 Parafinas e gelificação de óleo
As fontes tratam a precipitação/cristalização de parafinas e a gelificação como riscos de grande relevância, sobretudo em baixas temperaturas. Consequências possíveis:

- aumento de viscosidade;
- aumento de tensão limite de escoamento;
- dificuldade de reinício após parada;
- necessidade de pressões elevadas para retomar a fluidez;
- maior demanda por limpeza mecânica e estratégias térmicas.

Medidas mitigatórias citadas:

- **substituição/deslocamento do fluido por diesel** em certas paradas, por ser menos suscetível à estrutura gelificada;
- **aquecimento** do duto, por aquecimento elétrico ou por circulação de fluido quente;
- **aumento do isolamento térmico**;
- **injeção contínua de produtos químicos**;
- uso de **pigagem** para limpeza.

As próprias fontes observam que essas medidas podem introduzir novos custos, restrições ou riscos secundários. Portanto, a escolha da estratégia é de otimização técnico-econômica, não de aplicação universal.

### 5.3 Incrustações, corrosão e erosão
As incrustações minerais de sulfatos e carbonatos são listadas como restrições inorgânicas relevantes. O material também associa:

- altos teores de **H2S** e **CO2** à corrosão;
- elevada produção de areia à **erosão**.

Esses fenômenos nem sempre se manifestam como “plug” súbito, mas podem reduzir área efetiva, alterar o regime de escoamento, degradar a integridade e impor intervenção ou troca prematura de componentes.

## 6. Monitoramento e controle operacional para prevenção de restrições
*Fontes: `petroles-004c2afadba7ea17c7dd7908:pNone:1997369.60-1997401.0`, `petroles-004c2afadba7ea17c7dd7908:pNone:2015282.0-2015327.60`, `regis-675f59687b517be845d5bb41:pNone:934.0-1197.0`*

As fontes apontam que a prevenção de plugs e restrições depende de monitoramento contínuo e de procedimentos operacionais coerentes com os estudos de escoamento permanente e transiente.

### 6.1 Variáveis de monitoramento mencionadas
- pressão e temperatura ao longo do sistema;
- **BSW** (teor de água produzida);
- **RGO/RGL** (relação gás-óleo / relação gás-líquido, conforme contexto do documento);
- presença/potencial de parafinas;
- potencial de incrustação;
- volume de líquido acumulado em linhas;
- pressões nas linhas de serviço e coleta durante pigagem/manobras.

### 6.2 Abertura de poços e manuseio de choke
Na elaboração de procedimentos de abertura/manobra, as simulações devem determinar taxas de abertura dos chokes que permitam simultaneamente:

1. não enviar ao separador mais líquido e gás do que sua capacidade de gerenciamento;
2. não atingir a pressão de atuação do sistema de proteção dos equipamentos;
3. não submeter as linhas a temperaturas inferiores às especificadas;
4. preservar os requisitos de garantia de escoamento.

Isso mostra que **choke management** não é apenas controle de produção; é também ferramenta de prevenção de risco térmico, hidráulico e de plugs em linhas submarinas.

### 6.3 Papel dos umbilicais e da injeção química
Como os umbilicais transportam sinais, potência e fluidos de injeção química para equipamentos submarinos, a disponibilidade desses sistemas influencia diretamente a capacidade de:

- injetar inibidores de hidrato;
- suportar estratégias preventivas em ANM/equipamentos subsea;
- diagnosticar desvios de processo a partir de medições e comandos remotos.

## 7. Pigabilidade e pigagem como ferramenta de mitigação e remediação
*Fontes: `petroles-004c2afadba7ea17c7dd7908:pNone:1997369.60-1997401.0`, `regis-dde44a51a227cfcb99b72f1a:pNone:1860.0-2091.0`*

A pigagem aparece nas fontes como meio importante de **remoção de depósitos** e de **excesso de líquido acumulado**.

### 7.1 Requisitos de projeto para pigabilidade
A pigabilidade deve ser prevista desde a fase de projeto. As fontes citam como obstáculos à passagem de PIG:

- mudanças simultâneas de direção de fluxo e diâmetro;
- configurações ou instalações que criem descontinuidades impeditivas;
- diferenças elevadas de diâmetro entre trechos, podendo restringir a operação a PIGs de espuma de baixa densidade.

Portanto, a decisão de “ter ou não pigagem” não é meramente operacional; ela decorre do arranjo físico do sistema submarino.

### 7.2 Pigagem mecânica
Finalidades citadas:

- remover depósitos;
- deslocar excesso de líquido acumulado na linha de coleta;
- veicular colchão de inibidor de corrosão entre PIGs, para proteção de partes da linha.

A frequência de pigagem para remoção de depósitos deve ser baseada na **taxa de deposição calculada**, usando como insumos os estudos de fluido e as amostras do reservatório.

### 7.3 Pigagem dinâmica
A pigagem dinâmica é descrita como aumento gradual ou brusco da vazão de gás para carrear o líquido acumulado. O procedimento deve considerar:

- quantidade de líquido acumulado;
- vazão de gás necessária;
- capacidade do vaso separador para receber esse líquido sem “atolar”.

### 7.4 Limites e cuidados operacionais
As manobras de pigagem devem ser conduzidas com monitoramento rigoroso, porque o pistão de líquido à frente do PIG pode elevar significativamente a pressão nas linhas submarinas. As fontes recomendam considerar:

- velocidade máxima do PIG informada pelo fabricante;
- classe de pressão das linhas de serviço e de produção;
- efeito da pressão hidrostática e/ou gasostática somado à pressão lida em superfície.

Se o sistema não suportar a pressão associada à pigagem na condição corrente, pode ser necessário reduzir a vazão de produção antes da operação, com impacto produtivo.

## 8. Paradas, shutdowns e retorno à produção
*Fontes: `petroles-004c2afadba7ea17c7dd7908:pNone:2015282.0-2015327.60`, `petroles-004c2afadba7ea17c7dd7908:pNone:2089667.0-2089711.0`*

As fontes tratam as paradas de produção como eventos críticos para garantia de escoamento. Situações de abertura/fechamento de poços, bloqueio de válvulas e shutdowns são cenários tipicamente **transientes** e devem ser simulados.

Pontos de decisão relevantes:

- a condição remanescente na linha após a parada depende do grau de atuação permitido aos operadores durante o fechamento;
- em shut-downs por intertravamento, a atuação é mais restrita e a linha pode permanecer em condição menos favorável ao retorno;
- quando o fechamento é coordenado, podem ser tomadas ações para deixar o sistema mais apto à reabertura.

Medidas mitigatórias citadas para facilitar o retorno:

- deslocamento por diesel, quando operacionalmente viável;
- manutenção ou recuperação de temperatura por aquecimento/isolamento;
- aplicação de produtos químicos;
- avaliação prévia da pressão necessária de reinício, especialmente em fluidos com tendência à gelificação.

As fontes também registram que soluções como aquecimento por **Pipe-in-Pipe (PIP)** com fluido quente podem ser eficazes para reduzir cristalização, auxiliar dissociação de hidratos e parafinas e diminuir necessidade de limpeza, mas trazem aumento de custo e preocupações adicionais, como risco de corrosão em anular e dependência de compatibilidade com o sistema de superfície.

## 9. Critérios de decisão técnica
*Fontes: `regis-675f59687b517be845d5bb41:pNone:1201.0-1412.0`, `petroles-004c2afadba7ea17c7dd7908:pNone:1997369.60-1997401.0`, `petroles-004c2afadba7ea17c7dd7908:pNone:2089667.0-2089711.0`, `regis-675f59687b517be845d5bb41:pNone:934.0-1197.0`*

A partir das fontes, a seleção entre prevenção, monitoramento, mitigação e remediação pode ser estruturada pelos seguintes critérios:

1. **Risco termodinâmico do fluido**
   - posição da operação em relação ao envelope de hidrato;
   - severidade do sub-resfriamento;
   - tendência a precipitação orgânica/inorgânica.

2. **Características do arranjo submarino**
   - extensão do tie-back;
   - exposição térmica ao fundo do mar;
   - possibilidade de pigagem;
   - disponibilidade de injeção química via umbilical.

3. **Capacidade operacional do sistema topside**
   - capacidade do separador para receber líquido deslocado em pigagem ou abertura;
   - limites de pressão dos sistemas e das linhas;
   - flexibilidade para aquecimento, recirculação ou manobras de vazão.

4. **Condição de integridade e retorno à produção**
   - risco de corrosão/erosão;
   - pressão requerida para reinício após gelificação;
   - possibilidade de despressurização segura;
   - impacto da frequência de intervenções na disponibilidade do ativo.

5. **Critério econômico-operacional**
   - as fontes observam que elevar o nível de “garantia” implica crescimento de CAPEX/OPEX;
   - por isso, a solução ótima costuma ser a que controla o risco a um nível aceitável com base em estudos do fluido, simulações e limites operacionais, e não a eliminação absoluta de toda incerteza.

## 10. Síntese aplicada à operação submarina
*Fontes: `regis-dde44a51a227cfcb99b72f1a:pNone:1728.0-1986.0`, `regis-dde44a51a227cfcb99b72f1a:pNone:1860.0-2091.0`, `petroles-004c2afadba7ea17c7dd7908:pNone:1997369.60-1997401.0`, `petroles-004c2afadba7ea17c7dd7908:pNone:2015282.0-2015327.60`, `petroles-004c2afadba7ea17c7dd7908:pNone:2089667.0-2089711.0`*

Para linhas submarinas associadas a FPSOs, a boa prática derivada das fontes pode ser resumida assim:

- **prever** o comportamento do fluido com dados representativos e simulações permanentes/transientes;
- **projetar** linhas, acessórios e interfaces de modo compatível com isolamento térmico, pigabilidade, injeção química e limites de pressão;
- **monitorar** continuamente P, T, água produzida, relação gás-líquido/óleo, potencial de depósito e volumes acumulados;
- **operar** aberturas, fechamentos, pigagens e shutdowns com procedimentos que respeitem limites de processo e de garantia de escoamento;
- **mitigar** com inibidores, isolamento, aquecimento, pigagem e controle de manobras;
- **remediar** com cautela, reconhecendo que despressurização, limpeza ou aquecimento podem exigir condições bem controladas para não agravar o bloqueio.

Em essência, plugs e restrições em sistemas submarinos não são apenas problema de duto; são problema integrado de **fluido + temperatura + pressão + geometria + operação + capacidade de resposta do sistema subsea e topside**.