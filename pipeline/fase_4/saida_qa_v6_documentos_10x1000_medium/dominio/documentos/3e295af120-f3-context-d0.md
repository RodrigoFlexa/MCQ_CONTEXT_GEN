# Hidráulica e escoamento no flare

## 1. Delimitação técnica desta faceta

Esta faceta trata da **capacidade hidráulica** e dos **fenômenos de escoamento** que afetam o desempenho de sistemas de alívio, despressurização e flare em FPSOs, com foco nos aspectos que podem ser sustentados pelos trechos fornecidos. O material disponível não traz regras específicas de dimensionamento de flare tip, headers de flare, PSV ou BDV, mas oferece base útil sobre:

- escoamento multifásico e mudança de regime de fluxo;
- perda de carga e contrapressão em escoamentos gás-líquido;
- transientes, acumulação de líquido e slugging;
- escolha entre modelos permanentes, transientes e mecanicistas;
- efeitos de vibração, corrosão e integridade associados ao padrão de escoamento.

Em sistemas de flare, esses temas são relevantes porque a descarga de alívio nem sempre permanece estritamente monofásica ao longo de todo o percurso: variações de pressão, temperatura, composição e geometria podem alterar o regime de escoamento, a perda de carga, a contrapressão percebida a montante e a tendência a arraste ou acúmulo de líquidos.

**Fontes:** `petroles-4ee4bce16acf674505c8912d:pNone:737749.0-737784.0`, `petroles-4ee4bce16acf674505c8912d:pNone:737768.0-737809.0`, `petroles-004c2afadba7ea17c7dd7908:pNone:1917826.0-1917883.0`

## 2. Base fenomenológica: por que o flare pode deixar de ser um problema apenas de gás

Os trechos de referência mostram que, em sistemas de produção de hidrocarbonetos, a redução de pressão e temperatura ao longo do escoamento pode fazer com que um fluido inicialmente tratado de forma simples passe a apresentar **duas fases**. São citados, no contexto de produção, mecanismos como:

- condensação de frações pesadas por resfriamento;
- condensação por queda de pressão;
- condensação de água;
- arraste de água já presente no sistema.

Embora esses exemplos tenham sido descritos para colunas de produção e linhas de produção, o ponto hidráulico mais importante para a faceta de flare é geral: **a mudança das condições termodinâmicas ao longo do escoamento pode alterar a distribuição das fases e transformar um cálculo monofásico em um problema multifásico**.

Para o sistema de alívio e flare, isso significa que a avaliação de capacidade não deve partir automaticamente da hipótese de escoamento seco e estável em toda a rede. Sempre que houver possibilidade de condensação, arraste de líquido ou entrada episódica de líquido na descarga, passam a ser relevantes:

- o regime de escoamento ao longo do header;
- o hold-up líquido local;
- o aumento de perda de carga;
- a oscilação de contrapressão;
- o potencial de slugging e cargas dinâmicas.

Os textos também destacam que, em poços de gás, quando a quantidade de líquido excede a capacidade de arraste da fase gasosa, pode ocorrer **acúmulo de líquido** e aumento de contrapressão, levando a comportamento oscilatório e maior perda de carga. Em um flare header, por analogia fenomenológica, bolsões ou acúmulos de líquido em pontos baixos podem igualmente degradar o desempenho hidráulico e tornar o escoamento transiente mais severo.

**Fontes:** `petroles-4ee4bce16acf674505c8912d:pNone:737749.0-737784.0`, `petroles-4ee4bce16acf674505c8912d:pNone:737768.0-737809.0`

## 3. Padrões de escoamento bifásico relevantes para o flare

Os trechos fornecem uma revisão útil de **padrões de escoamento gás-líquido**, especialmente em linhas verticais e horizontais. Esses padrões são importantes porque a perda de carga, a estabilidade do fluxo, o arraste de líquido e o potencial de vibração dependem do arranjo espacial das fases, e não apenas da vazão total.

### 3.1 Padrões citados no material

Os padrões mencionados incluem:

- **bolhas dispersas**: fase gasosa dispersa no líquido;
- **intermitente / slug**: bolhas alongadas ou golfadas de líquido e gás alternadas;
- **churn**: regime vertical não plenamente desenvolvido, tipicamente de transição;
- **anular**: gás dominante no centro do tubo com filme líquido na parede;
- **estratificado liso/ondulado**: típico de escoamentos horizontais em baixas ou moderadas velocidades, com segregação gravitacional das fases.

O material ressalta que a geometria, as propriedades físicas dos fluidos, a proporção entre fases, a velocidade e a inclinação do duto afetam diretamente qual padrão é estabelecido.

### 3.2 Consequências hidráulicas práticas

Para análise de flare, a utilidade desses padrões é direta:

- **o padrão de escoamento altera a perda de carga**;
- **o padrão de escoamento altera o hold-up líquido**;
- **o padrão de escoamento afeta a tendência de formação de golfadas**;
- **o padrão de escoamento modifica a intensidade de flutuações de pressão e de forças dinâmicas**.

Em especial:

- padrões **intermitentes** tendem a gerar maiores oscilações de pressão e vazão local;
- padrões com segregação gravitacional em trechos horizontais ou descendentes favorecem acúmulo de líquido;
- padrões **anulares** podem estar associados a forte cisalhamento interfacial e arraste de gotículas;
- o regime **churn** é particularmente desordenado e pode dificultar previsões simplificadas.

### 3.3 Implicação para headers e linhas de descarga

Em uma rede de flare com trechos horizontais, inclinados e verticais, a mudança de padrão ao longo do percurso pode ser mais importante do que o valor médio de vazão. Assim, a avaliação de capacidade hidráulica deve considerar:

1. onde pode haver segregação gravitacional de fases;
2. onde o gás perde capacidade de carregar o líquido;
3. onde mudanças geométricas ou de inclinação podem iniciar intermitência;
4. onde o aumento de velocidade pode induzir transição para churn ou anular.

**Fontes:** `petroles-4ee4bce16acf674505c8912d:pNone:1341790.0-1341825.0`, `petroles-4ee4bce16acf674505c8912d:pNone:737768.0-737809.0`

## 4. Perda de carga, contrapressão e escolha do modelo hidráulico

### 4.1 Limites de modelos excessivamente simplificados

Os trechos destacam que tratar o escoamento bifásico como se fosse um **fluido homogêneo** pode levar à subestimação relevante da perda de carga. O material também separa as abordagens de cálculo em grupos:

1. **homogêneas**, que desprezam escorregamento entre fases e seus arranjos espaciais;
2. abordagens que consideram **escorregamento** e calculam hold-up por correlações genéricas;
3. abordagens que consideram **escorregamento e padrão de escoamento**;
4. **correlações mecanicistas**, baseadas em modelagem física mais explícita.

A consequência para o flare é clara: quando houver possibilidade razoável de escoamento gás-líquido, o uso de hipóteses homogêneas tende a ser menos robusto para previsão de:

- perda de carga total do sistema;
- contrapressão no coletor de alívio;
- distribuição de fases ao longo da linha;
- pontos de acúmulo de líquido;
- resposta a eventos transientes.

### 4.2 Regime permanente versus transiente

Os textos observam que muitas correlações tradicionais foram consolidadas para **regime permanente**, isto é, para propriedades independentes do tempo. Entretanto, descargas de alívio e despressurização frequentemente envolvem:

- aberturas e fechamentos rápidos de válvulas;
- variações bruscas de restrição ao escoamento;
- mudanças rápidas de pressão;
- formação e deslocamento de frentes gás-líquido.

Nesses casos, o material sugere que ferramentas baseadas em **equações de conservação resolvidas numericamente** são mais adequadas para capturar o fenômeno no espaço e no tempo.

### 4.3 Variáveis hidrodinâmicas explicitamente citadas

Os trechos mencionam, como variáveis úteis na modelagem de escoamentos bifásicos:

- **velocidade superficial** (`J`);
- **fração de vazio homogênea**;
- **velocidade da mistura**;
- **velocidade de atrito**;
- **fator de atrito bifásico**;
- **hold-up líquido**;
- pressões características, como **contrapressão**.

As equações explícitas dessas grandezas não aparecem integralmente nos excertos fornecidos, mas o material deixa claro que elas são essenciais para previsão de regime, perda de carga e estabilidade.

### 4.4 Consequência prática para sistemas de alívio e flare

Na prática, a análise de capacidade hidráulica do flare deve distinguir pelo menos três níveis de modelagem:

- **triagem simplificada**: útil quando a descarga é seguramente gasosa e a possibilidade de liquefação/arraste é desprezível;
- **modelo bifásico em regime permanente**: útil para comparar trechos, quedas de pressão médias e sensibilidades de layout;
- **modelo transiente/mecanicista**: necessário quando há blowdown, cenários de ESD, risco de slugging, bolsões de líquido, forte variação temporal de vazão ou necessidade de avaliar contrapressão dinâmica.

**Fontes:** `petroles-004c2afadba7ea17c7dd7908:pNone:1917826.0-1917883.0`, `petroles-4ee4bce16acf674505c8912d:pNone:737768.0-737809.0`, `petroles-004c2afadba7ea17c7dd7908:pNone:3001770.0-3001811.0`

## 5. Slugging, intermitência severa e comportamento oscilatório

### 5.1 Mecanismo físico descrito nos trechos

O material descreve a **intermitência severa (severe slugging)** como um ciclo associado a baixas vazões de gás e líquido e a uma geometria com trecho descendente seguido de trecho ascendente. O ciclo é resumido em etapas:

1. **acúmulo de líquido** na transição geométrica, bloqueando a passagem do gás;
2. **compressão da fase gasosa** a montante;
3. quando a coluna líquida atinge condição crítica, o gás penetra no trecho ascendente e ocorre **blowout** com alta velocidade;
4. após a descarga, o líquido residual retorna por ação hidrostática (**fallback**), reiniciando o ciclo.

Esse mecanismo produz oscilações fortes de pressão, vazão e hold-up.

### 5.2 Aplicação conceitual à hidráulica do flare

Os trechos são de dutos e risers de produção, não de flare. Ainda assim, a fenomenologia é útil para a faceta de flare porque qualquer rede com:

- trechos descendentes e ascendentes;
- pontos baixos onde líquido possa se acumular;
- escoamento gás-líquido com baixa capacidade de arraste;
- grande sensibilidade a contrapressão;

pode apresentar comportamento oscilatório análogo.

Em sistemas de flare, tal comportamento é indesejável porque pode ampliar:

- picos transitórios de contrapressão no header;
- chegada intermitente de golfadas líquidas a equipamentos de separação ou drenagem;
- carregamentos dinâmicos em suportes e estruturas;
- incertezas na capacidade efetiva da rede durante eventos reais de alívio.

### 5.3 Contrapressão como variável de estabilidade

Os materiais de apoio indicam que, em sistemas pipeline-riser, o **estrangulamento no topo** pode reduzir ou eliminar severe slugging via aumento de **backpressure**, funcionando também como resistência ao fluxo proporcional à velocidade da mistura. O mesmo conjunto de textos mostra que a contrapressão é uma variável crítica na delimitação de regiões estáveis e instáveis.

Para sistemas de flare, a leitura profissional correta é mais cautelosa: a contrapressão continua sendo uma variável hidráulica central, mas seu aumento não pode ser tratado genericamente como solução, pois a rede de alívio precisa ser avaliada em conjunto com o comportamento dos dispositivos de proteção a montante. Os trechos fornecidos sustentam a importância da contrapressão na estabilidade do escoamento, mas **não fornecem critérios específicos de aceitabilidade para PSV/BDV ou flare**.

**Fontes:** `petroles-4ee4bce16acf674505c8912d:pNone:1341771.0-1341808.0`, `petroles-4ee4bce16acf674505c8912d:pNone:1341790.0-1341825.0`, `regis-5c1c7e6bbabc1a899b957acd:pNone:610.0-710.0`, `petroles-004c2afadba7ea17c7dd7908:pNone:762165.0-762203.0`

## 6. Transientes de válvulas, blowdown e necessidade de simulação dinâmica

Os textos citam explicitamente a utilidade de simuladores transientes para estudar:

- abertura e fechamento de válvulas;
- mudanças bruscas de restrição ao fluxo;
- shut-in ou fechamento completo;
- propagação e convecção de frentes de gás;
- possibilidade de formação de hidratos durante transientes em outros contextos.

Também é citado que o simulador OLGA é amplamente usado para fluxo transiente em tubulações com suporte a escoamento bifásico e trifásico, e que modelos de deslizamento, híbridos Eulerianos-Lagrangeanos e outras formulações podem ser mais adequados para fenômenos convectivos de longa escala temporal.

Na faceta de flare, isso sustenta uma distinção prática:

- para eventos lentos e relativamente estáveis, modelos permanentes podem ser suficientes para uma primeira estimativa;
- para blowdown, ESD, descargas simultâneas, mudança abrupta de regime ou avaliação de slugging, a **simulação transiente** é mais indicada.

Isso é especialmente importante quando a pergunta profissional envolve não apenas “qual a perda de carga média”, mas sim:

- qual o pico de contrapressão;
- em que instante chega uma frente líquida;
- se haverá oscilação de pressão;
- se a capacidade hidráulica é mantida durante todo o evento, e não apenas em um estado médio.

**Fontes:** `petroles-004c2afadba7ea17c7dd7908:pNone:1917826.0-1917883.0`, `petroles-004c2afadba7ea17c7dd7908:pNone:3001770.0-3001811.0`, `petroles-004c2afadba7ea17c7dd7908:pNone:762165.0-762203.0`

## 7. Vibração induzida por escoamento e efeitos estruturais

Um dos trechos trata de **vibração induzida por escoamento bifásico** em tubo, mostrando que a resposta estrutural pode ser relacionada a parâmetros de escoamento, como fração de vazio homogênea e velocidade de atrito, por meio de frequência de pico e desvio padrão de aceleração. O material registra ainda observações de:

- ressonância por turbulência;
- influência da intermitência do escoamento;
- melhor desempenho do método proposto para certos padrões de fluxo e altas frações de vazio.

Para linhas de flare, a conclusão de engenharia é que a avaliação hidráulica não deve se limitar ao balanço de massa e energia. Regimes intermitentes, alta turbulência e presença de duas fases podem gerar:

- excitação dinâmica da tubulação;
- amplificação de vibração;
- esforços cíclicos em suportes e conexões;
- sensibilidade maior durante eventos transientes.

Assim, a análise de capacidade do flare e a análise mecânica/estrutural precisam ser coerentes entre si, sobretudo quando há previsão de escoamento oscilatório ou slugging.

**Fontes:** `petroles-4ee4bce16acf674505c8912d:pNone:1661398.0-1661462.0`

## 8. Corrosão, velocidade e padrão de escoamento

Os trechos sobre integridade indicam que a corrosão pode se intensificar com aumento de:

- temperatura;
- pressão;
- velocidade de escoamento.

Também é explicitado que o **padrão de escoamento** influencia o dano: escoamentos mais turbulentos e intermitentes tendem a remover ou afinar filmes protetores e incrustações, elevando o potencial corrosivo. O texto chega a comparar o padrão intermitente como potencialmente mais danoso que o estratificado.

Em termos de flare, isso reforça que a hidráulica e a integridade são inseparáveis. Uma configuração que “passa na capacidade” pode continuar problemática se produzir:

- altas velocidades locais persistentes;
- flutuações severas de cisalhamento;
- zonas de molhamento intermitente;
- retenção de condensado ou água em bolsões.

Portanto, trechos sujeitos a alternância gás-líquido, recirculação local ou repetidas golfadas devem receber atenção especial em inspeção e estratégia de integridade.

**Fontes:** `petroles-4ee4bce16acf674505c8912d:pNone:1341771.0-1341808.0`

## 9. Critérios práticos de avaliação hidráulica para o flare, sustentados pelo material

Sem extrapolar para regras normativas não fornecidas, os trechos permitem estruturar uma análise profissional do flare em torno das seguintes perguntas técnicas:

### 9.1 Há possibilidade real de escoamento multifásico?

Indícios relevantes:

- queda de pressão e temperatura ao longo da linha;
- presença potencial de condensáveis e água;
- histórico de arraste de líquido;
- transientes de blowdown ou alívio com forte variação termodinâmica.

### 9.2 O padrão de escoamento foi identificado de forma compatível com geometria e inclinação?

A avaliação deve reconhecer que trechos horizontais, inclinados e verticais podem operar em padrões distintos, com diferenças marcantes de hold-up, perda de carga e estabilidade.

### 9.3 O modelo hidráulico é compatível com o problema?

- modelo homogêneo: apenas quando a simplificação for defensável;
- correlações com escorregamento e/ou regime: quando houver duas fases e necessidade de maior realismo;
- simulação transiente/mecanicista: quando houver slugging, acúmulo de líquido, blowdown, ESD, válvulas atuando rapidamente ou necessidade de prever contrapressão dinâmica.

### 9.4 Existem condições para acúmulo de líquido e oscilação?

Geometrias com pontos baixos, mudanças de inclinação e trechos descendente-ascendente devem ser examinadas porque podem iniciar ciclos de bloqueio por líquido, compressão de gás, blowout e fallback.

### 9.5 A análise considerou os efeitos colaterais mecânicos e de integridade?

Alta turbulência, intermitência e escoamento bifásico podem impor simultaneamente:

- perda de carga elevada;
- vibração induzida por escoamento;
- corrosão acelerada;
- maior incerteza operacional em eventos reais.

**Fontes:** `petroles-4ee4bce16acf674505c8912d:pNone:737768.0-737809.0`, `petroles-4ee4bce16acf674505c8912d:pNone:1341790.0-1341825.0`, `petroles-004c2afadba7ea17c7dd7908:pNone:1917826.0-1917883.0`, `petroles-004c2afadba7ea17c7dd7908:pNone:3001770.0-3001811.0`, `petroles-4ee4bce16acf674505c8912d:pNone:1661398.0-1661462.0`, `petroles-4ee4bce16acf674505c8912d:pNone:1341771.0-1341808.0`

## 10. Síntese

Os trechos fornecidos sustentam uma mensagem central para a faceta **Hidráulica e escoamento no flare**: a capacidade de um sistema de alívio não deve ser analisada apenas como problema de vazão de gás em regime permanente. Sempre que houver possibilidade de mudança de fase, arraste ou acúmulo de líquido, tornam-se determinantes:

- o padrão de escoamento;
- o hold-up e a segregação de fases;
- a perda de carga bifásica;
- a contrapressão dinâmica;
- a propensão a slugging e oscilações;
- os efeitos de vibração e corrosão associados.

A seleção do método de cálculo deve acompanhar a complexidade do fenômeno: correlações simplificadas podem ser úteis em triagens, mas transientes relevantes de blowdown/alívio, escoamento oscilatório e presença de duas fases justificam modelos mecanicistas e simulação dinâmica.

**Fontes:** `petroles-4ee4bce16acf674505c8912d:pNone:737768.0-737809.0`, `petroles-004c2afadba7ea17c7dd7908:pNone:1917826.0-1917883.0`, `petroles-004c2afadba7ea17c7dd7908:pNone:3001770.0-3001811.0`, `petroles-4ee4bce16acf674505c8912d:pNone:1341790.0-1341825.0`