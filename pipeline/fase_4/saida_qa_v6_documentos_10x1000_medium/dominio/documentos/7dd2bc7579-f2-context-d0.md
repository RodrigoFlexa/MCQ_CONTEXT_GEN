# Operação de tratadores eletrostáticos em FPSOs — emulsão e química

## 1. Papel do tratador eletrostático no condicionamento do óleo
Em sistemas marítimos de produção, o tratador eletrostático é empregado como etapa de desidratação e, em alguns arranjos, de dessalinização do petróleo. O princípio citado nas fontes é a aplicação de alta tensão à emulsão água-em-óleo; quando o campo é contínuo, o processo é descrito por eletroforese, e quando o campo é alternado, por efeito de dipolo induzido. Em termos operacionais, o objetivo não é “separar por milagre” uma emulsão muito estável, mas acelerar a aproximação, deformação e coalescência de gotas de água já parcialmente condicionadas por temperatura, química e hidrodinâmica adequadas. As fontes também indicam que, independentemente do tratamento selecionado, tempo de residência adequado, agitação suficiente para contato e uso de desemulsificante são fatores críticos para alcançar a separação desejada.

Para FPSOs, isso significa que o desempenho do tratador eletrostático depende fortemente da qualidade da emulsão que chega ao vaso: uma emulsão excessivamente estável, com gotas muito finas e filme interfacial rígido, exigirá mais condicionamento térmico e químico antes que o campo elétrico produza coalescência útil.

**Fontes da seção:** `petroles-4ee4bce16acf674505c8912d:pNone:1400338.0-1400380.0`, `petroles-4ee4bce16acf674505c8912d:pNone:617216.0-617258.0`

## 2. Como a emulsão água-em-óleo se forma e por que ela persiste
A emulsão de petróleo se forma quando um líquido imiscível é disperso no outro em forma de gotículas sob fornecimento de energia. No petróleo produzido, isso é favorecido por cisalhamento no escoamento, método de elevação, perdas de carga em tubulações, válvulas e outros acidentes, além das etapas de processamento primário. O tipo mais comum no contexto de desidratação do óleo é a emulsão água-em-óleo, em que a água é a fase dispersa e o petróleo a fase contínua.

A estabilidade dessa emulsão aumenta quando:
- as gotas de água são pequenas e com distribuição de tamanho mais estreita;
- há emulsificantes naturais adsorvidos na interface água-óleo;
- a viscosidade do óleo é elevada;
- sólidos finos e contaminantes reforçam a estrutura interfacial.

As fontes descrevem o rompimento da emulsão em três etapas conceituais:
1. **aproximação das gotas**;
2. **drenagem do filme intersticial/interfacial** entre as gotas;
3. **coalescência**, com formação de gotas maiores e posterior segregação gravitacional.

Esse encadeamento é importante para o tratador eletrostático: o campo elétrico atua sobretudo favorecendo encontro e deformação das gotas, mas a coalescência só se completa se a barreira interfacial puder ser drenada. Portanto, química interfacial e propriedades do óleo continuam sendo determinantes mesmo quando há alta tensão aplicada.

**Fontes da seção:** `petroles-4ee4bce16acf674505c8912d:pNone:617216.0-617258.0`, `petroles-004c2afadba7ea17c7dd7908:pNone:3467480.0-3467528.0`, `petroles-4ee4bce16acf674505c8912d:pNone:871422.0-871463.0`

## 3. Emulsificantes naturais: asfaltenos, resinas e sólidos
As fontes convergem em apontar asfaltenos e resinas como os principais emulsificantes naturais associados à estabilidade de emulsões água-em-óleo. Esses compostos são polares, aromáticos e ricos em heteroátomos; concentram-se na interface água-óleo e formam um filme mecanicamente resistente em torno das gotas de água. Esse filme reduz a facilidade de drenagem e, portanto, dificulta a coalescência.

Dois mecanismos qualitativos são destacados para explicar essa estabilidade:
- **repulsão estérica**: partes das moléculas adsorvidas mantêm as interfaces a uma distância suficiente para dificultar o contato efetivo;
- **aumento da viscosidade interfacial/aparente do filme**: a interface torna-se mais rígida e menos drenável.

As resinas podem atuar em associação com os asfaltenos, formando agregados ou micelas solvatadas. Esses agregados adsorvem na interface das gotas de água e contribuem para uma “casca” interfacial rígida. Para a operação do tratador eletrostático, isso significa que nem sempre basta elevar a tensão elétrica: se a água estiver encapsulada por um filme asfaltênico-resinoso muito resistente, a eficiência de coalescência pode permanecer baixa.

As fontes também indicam que sólidos finamente divididos, como carbonato de cálcio, sulfato de cálcio, argilas e areia, podem difundir-se ou acumular-se na interface e criar estruturas estéricas rígidas que impedem a coalescência. Em termos de troubleshooting, a presença de sólidos deve ser considerada quando há emulsão persistente, descarga de água lenta e alto BS&W mesmo com aquecimento e química aparentemente adequados.

**Fontes da seção:** `petroles-4ee4bce16acf674505c8912d:pNone:871422.0-871463.0`, `petroles-004c2afadba7ea17c7dd7908:pNone:3467480.0-3467528.0`

## 4. Influência das propriedades do óleo e da emulsão no desempenho eletrostático

### 4.1 Viscosidade e temperatura
A temperatura afeta diretamente as propriedades do óleo, da água e do filme interfacial. As fontes afirmam que o aumento de temperatura reduz abruptamente a viscosidade do óleo, o que facilita a aproximação das gotas de água e acelera a coalescência. Em consequência, o aquecimento prévio melhora a resposta do tratador eletrostático porque reduz a resistência ao movimento das gotas e ajuda a drenagem do filme entre elas.

Na prática, óleos mais viscosos tendem a exigir maior condicionamento térmico e/ou químico. Sem isso, o campo elétrico encontra gotas menos móveis, com menor frequência de colisão efetiva e maior dificuldade de sedimentação após a coalescência.

### 4.2 Tamanho de gota e distribuição de tamanhos
As fontes indicam que gotas menores tornam a emulsão mais estável; distribuições monodispersas de gotas finas tendem a aumentar a persistência da emulsão, enquanto distribuições mais amplas podem favorecer o crescimento de gotas maiores pela aproximação entre gotas pequenas e grandes. Também é mencionado que maior intensidade e maior tempo de agitação reduzem o tamanho de gota até um limite assintótico.

Isso é particularmente relevante para FPSOs: excesso de cisalhamento a montante do tratador — em bombas, válvulas de controle, chokes, misturadores ou recirculações — pode produzir uma emulsão demasiadamente fina para o estágio eletrostático disponível. O resultado esperado é piora da desidratação, aumento do teor de água remanescente no óleo e maior dependência de química.

### 4.3 Teor de água e salinidade
A água de formação co-produzida com o petróleo costuma apresentar alta concentração de sais dissolvidos. As fontes relacionam a permanência de água e sal no óleo a problemas de corrosão, hidratos, incrustações, maior viscosidade aparente e aumento do custo energético e de transporte. Portanto, a meta operacional não é apenas “tirar água visível”, mas reduzir água e sal remanescentes a níveis compatíveis com exportação, transporte e processamento subsequente.

Os resultados experimentais reportados em bancada mostram que a eficiência de remoção de água e sal depende diretamente das características físicas e químicas do petróleo, do uso de desemulsificante, do processo de lavagem e do tempo disponível para separação gravitacional. Isso reforça que o desempenho do tratador eletrostático não deve ser interpretado isoladamente: qualidade da lavagem, mistura com água de lavagem e tempo de queda da água continuam sendo partes do problema.

**Fontes da seção:** `petroles-4ee4bce16acf674505c8912d:pNone:871422.0-871463.0`, `petroles-4ee4bce16acf674505c8912d:pNone:1400338.0-1400380.0`, `regis-82e39b1ebb0d9ac30fe84073:pNone:214.0-232.0`

## 5. Desemulsificantes: mecanismo de ação e seleção
As fontes descrevem os desemulsificantes como surfactantes poliméricos, em geral não iônicos, contendo partes lipofílica e hidrofílica. São citados, entre os comerciais, copolímeros à base de poli(óxido de etileno) e poli(óxido de propileno), além de formulações com resinas alquilfenol-formaldeído.

O mecanismo simplificado apresentado é:
1. o desemulsificante migra até a interface água-óleo;
2. desloca o filme rígido formado pelos emulsificantes naturais do petróleo;
3. substitui essa camada por um filme mais fino e mais fácil de drenar;
4. as gotas coalescem e, em seguida, sedimentam por gravidade.

No contexto do tratador eletrostático, isso é decisivo: o campo elétrico pode aproximar e polarizar gotas, mas a química precisa tornar a interface “quebrável”. Sem essa substituição ou enfraquecimento do filme natural, a gota pode até colidir e deformar, mas não necessariamente coalescer de forma eficiente.

### 5.1 Seleção de produto
As fontes mostram que a eficiência do desemulsificante depende de vários fatores:
- composição química do petróleo;
- concentração do produto;
- balanço hidrofílico-lipofílico da molécula;
- massa molar/cadeia polimérica;
- teor de água da emulsão;
- tempo de atuação antes e durante a separação.

Também há forte indicação de que **não existe produto universal**. Um estudo de bancada observou que a adição de um desemulsificante reduziu significativamente os teores remanescentes de água e sal, mas registrou explicitamente que a seleção de um produto específico para cada petróleo tenderia a levar a resultados ainda melhores.

### 5.2 Nem todo aumento de cinética de quebra significa boa resolução final
As fontes trazem um exemplo operacional importante: diferentes bases químicas podem acelerar a quebra em graus distintos, e um surfactante pode até aumentar a cinética inicial sem produzir boa resolução final das fases. Em um caso, formulações comerciais baseadas em resina fenólica/polipropilenoglicol ou em polipropilenoglicol foram eficazes para quebra de emulsões altamente estáveis, enquanto um nonilfenol etoxilado de baixo grau de etoxilação aumentou a cinética, mas não apresentou resolução efetiva das fases.

Para o tratador eletrostático, isso significa que a avaliação da química não deve se limitar a observar “água aparecendo mais rápido”. É necessário confirmar:
- teor final de água no óleo;
- sal remanescente;
- clareza da água separada;
- estabilidade do interfaceamento e do downstream.

### 5.3 Tempo de atuação e cinética
Os dados de bancada também sugerem que o desemulsificante pode ter uma cinética própria de atuação na interface. Em ensaios com produto químico, o diâmetro médio de gota decresceu apenas nas primeiras horas, comportamento associado à atuação do produto sobre a interface e à facilitação posterior da coalescência. Em outras palavras, a resposta não precisa ser instantânea; o produto pode demandar tempo de contato para expressar plenamente seu desempenho.

Isso reforça a importância de ponto de injeção, mistura inicial suficiente sem sobrecisalhamento e tempo de residência total até o tratador eletrostático.

**Fontes da seção:** `petroles-4ee4bce16acf674505c8912d:pNone:871422.0-871463.0`, `petroles-4ee4bce16acf674505c8912d:pNone:617216.0-617258.0`, `petroles-4ee4bce16acf674505c8912d:pNone:1401188.0-1401246.0`, `regis-82e39b1ebb0d9ac30fe84073:pNone:214.0-232.0`

## 6. Leitura operacional do baixo desempenho em tratadores eletrostáticos
Com base nas relações descritas nas fontes, um tratador eletrostático tende a apresentar baixo desempenho químico-operacional quando se observam um ou mais dos seguintes quadros:
- óleo tratado com alto teor de água e/ou sal remanescente;
- emulsão persistente mesmo com aplicação de campo elétrico;
- necessidade crescente de temperatura ou de química para manter especificação;
- queda de eficiência após mudanças de petróleo, teor de água, regime de produção ou campanha de poços;
- piora após aumento de cisalhamento a montante.

As causas mais prováveis, no recorte “emulsão e química”, são:
1. **filme interfacial muito rígido**, associado a asfaltenos, resinas e eventualmente sólidos finos;
2. **viscosidade elevada**, com baixa mobilidade das gotas;
3. **gotas muito pequenas**, formadas por cisalhamento excessivo;
4. **desemulsificante inadequado** para aquele petróleo ou dosagem insuficiente/excessiva;
5. **tempo de residência insuficiente** para atuação química e segregação gravitacional;
6. **condicionamento térmico insuficiente**.

O diagnóstico correto deve correlacionar mudança de desempenho com mudança de petróleo, água produzida, sólidos, química, temperatura e hidrodinâmica a montante, e não apenas com a tensão elétrica aplicada.

**Fontes da seção:** `petroles-4ee4bce16acf674505c8912d:pNone:871422.0-871463.0`, `petroles-4ee4bce16acf674505c8912d:pNone:1400338.0-1400380.0`, `petroles-004c2afadba7ea17c7dd7908:pNone:3467480.0-3467528.0`, `regis-82e39b1ebb0d9ac30fe84073:pNone:214.0-232.0`

## 7. Diretrizes práticas de otimização dentro do recorte desta faceta
Sem extrapolar para parâmetros numéricos não presentes nos trechos, as fontes sustentam as seguintes diretrizes qualitativas:
- **Ajustar a temperatura** para reduzir viscosidade e favorecer mobilidade/coalescência das gotas.
- **Controlar o cisalhamento a montante**, evitando produção contínua de gotas ultrafinas.
- **Selecionar o desemulsificante por petróleo e por objetivo** (desidratação, dessalinização ou ambos), e não apenas por histórico genérico.
- **Garantir tempo de contato do químico** antes e durante a etapa eletrostática.
- **Verificar presença de sólidos** quando houver emulsão persistente e baixa resposta à química.
- **Usar a análise de água e sal remanescentes**, e não apenas a observação visual, para decidir ajuste de processo.
- **Tratar o sistema de forma integrada**: separação gravitacional, aquecimento, lavagem, química e campo elétrico são complementares.

Em síntese, o tratador eletrostático funciona melhor quando recebe uma emulsão já “preparada para coalescer”: viscosidade reduzida, gotas com mobilidade suficiente, filme interfacial enfraquecido por química apropriada e tempo de residência compatível com a cinética de separação.

**Fontes da seção:** `petroles-4ee4bce16acf674505c8912d:pNone:1400338.0-1400380.0`, `petroles-4ee4bce16acf674505c8912d:pNone:871422.0-871463.0`, `regis-82e39b1ebb0d9ac30fe84073:pNone:214.0-232.0`, `petroles-4ee4bce16acf674505c8912d:pNone:1401188.0-1401246.0`