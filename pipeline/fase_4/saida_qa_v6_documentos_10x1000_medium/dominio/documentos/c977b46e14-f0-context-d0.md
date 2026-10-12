# Separação de arrastes no gás

## 1. Papel da separação de líquidos e sólidos no tratamento do gás produzido
O gás que sai da separação primária em uma unidade de produção não deve ser entendido como uma fase perfeitamente limpa. Mesmo após o primeiro vaso separador, ainda pode haver arraste de gotículas de hidrocarbonetos, água e, em alguns serviços, sólidos. Por isso, a remoção desses arrastes é uma etapa crítica antes de compressão e do condicionamento subsequente do gás.

Nas fontes, o condicionamento do gás é apresentado como o conjunto de processos destinados a reduzir contaminantes para atender requisitos de transporte, uso e comercialização. Dentro desse contexto, a remoção de água é destacada por reduzir corrosão, diminuir a possibilidade de formação de hidratos e viabilizar a compressão do gás em condições mais seguras. Em paralelo, quando existe estação de compressão, é considerado imprescindível haver, a montante, equipamentos de depuração do gás para remover arraste de líquidos e sólidos. Fontes: `regis-6afa562b7a4623c44e6a8025:pNone:1715.0-1957.0`, `regis-ef7d62eda3748119ba3e9e9e:pNone:976.0-1181.0`, `regis-6afa562b7a4623c44e6a8025:pNone:1829.0-2073.0`.

## 2. Mecanismos físicos que removem arrastes no separador de produção
A remoção de arrastes no gás produzido depende principalmente de mecanismos físicos aplicados no interior do vaso separador. As fontes convergem para quatro mecanismos centrais:

1. **Separação inercial na entrada**: o fluido choca-se com defletores ou sofre brusca mudança de direção e velocidade. O líquido, por sua maior inércia, tende a se desprender do gás.
2. **Ação centrífuga em alguns arranjos de entrada**: quando um difusor ou arranjo interno impõe rotação ao escoamento, as fases se separam pela diferença de densidade e pela ação da força centrífuga.
3. **Decantação gravitacional**: gotas líquidas arrastadas pela corrente gasosa sedimentam quando a turbulência é suficientemente baixa.
4. **Aglutinação/coalescência em meios porosos**: gotículas finas remanescentes são capturadas por extratores de névoa, onde se unem em gotas maiores e podem drenar por gravidade.

Didaticamente, isso se organiza em quatro seções do separador:

- **Seção de separação primária**: localizada na entrada do vaso; remove a maior parte do líquido por impacto, desaceleração e/ou rotação do escoamento.
- **Seção de acumulação/coleta de líquido**: localizada no fundo; o tempo de residência do líquido é determinante para liberar gás remanescente e, em separadores trifásicos, favorecer também a separação de água.
- **Seção de separação secundária**: localizada na região superior; reduz o teor de líquido carreado pelo gás por decantação, sendo favorecida por baixa turbulência.
- **Seção de aglutinação**: próxima à saída de gás; utiliza demister ou outros meios porosos para remover gotículas finas que escaparam das etapas anteriores.

Uma referência cita, para um separador típico, tempo de retenção de aproximadamente 3 a 4 minutos na seção de acumulação como suficiente para a liberação do gás remanescente e, em alguns casos, de grande parte da água. Esse valor deve ser entendido como indicativo do caso citado, e não como regra universal de dimensionamento. Fontes: `regis-ef7d62eda3748119ba3e9e9e:pNone:1079.0-1270.0`, `regis-6afa562b7a4623c44e6a8025:pNone:1715.0-1957.0`, `regis-6afa562b7a4623c44e6a8025:pNone:1829.0-2073.0`.

## 3. Equipamentos principais para reter arrastes no gás

### 3.1 Separadores de produção
A primeira barreira relevante contra carryover é o separador de produção, que pode ser bifásico ou trifásico, horizontal ou vertical, em série ou em paralelo. Um separador típico incorpora dispositivos internos como defletores de entrada, quebradores de espuma, quebradores de ondas e vórtice, além de extrator de névoa.

Do ponto de vista operacional, as fontes destacam que:

- a **pressão do separador** é mantida por controlador que regula a saída de gás;
- o **líquido separado** deixa o vaso por válvula comandada por controlador de nível;
- a eficiência de separação no topo depende fortemente de não haver turbulência excessiva.

Isso mostra que carryover não é apenas um problema mecânico de internals; ele também é um problema de controle de processo. Se pressão, nível e regime de escoamento se afastam do ponto de projeto, a eficiência de retenção de gotículas cai. Fontes: `regis-ef7d62eda3748119ba3e9e9e:pNone:1079.0-1270.0`, `regis-ef7d62eda3748119ba3e9e9e:pNone:976.0-1181.0`.

### 3.2 Scrubbers ou vasos depuradores a montante da compressão
Quando há compressão de gás, as fontes indicam como imprescindível a instalação de scrubbers a montante da unidade de compressão para remover arraste de líquidos e sólidos do escoamento gasoso. O scrubber não substitui o separador preliminar: ele é projetado para **cargas líquidas leves**, funcionando como polimento e proteção do compressor, não como equipamento principal de separação de grandes volumes de líquido.

O funcionamento descrito nas fontes é consistente com um depurador de gás clássico:

- o gás encontra inicialmente uma placa defletora;
- a corrente sofre desaceleração, o que favorece a separação;
- um extrator de névoa de alta eficiência captura partículas líquidas remanescentes;
- o líquido acumulado é drenado pelo fundo, manual ou automaticamente;
- o gás segue pela parte superior.

Em termos práticos, o scrubber é a última proteção importante contra carryover antes de equipamentos sensíveis, especialmente compressores. Fontes: `regis-6afa562b7a4623c44e6a8025:pNone:1715.0-1957.0`, `regis-6afa562b7a4623c44e6a8025:pNone:1829.0-2073.0`.

## 4. Causas principais de carryover de líquido no gás
O arraste de líquido na saída de gás, referido nas fontes como **LCO (Liquid Carry Over)**, pode ocorrer por diferentes mecanismos operacionais e de projeto.

### 4.1 Formação de espuma
A presença de impurezas no líquido pode favorecer a formação de espuma no interior do vaso. A espuma tem grande volume específico, reduz a área livre para escoamento do gás e aumenta o arraste de gotas na saída de gás. Esse é um dos mecanismos mais claramente associados a carryover nas fontes.

Além do aumento direto do LCO, a espuma pode prejudicar a confiabilidade dos instrumentos de nível, dificultando a manutenção do inventário líquido em faixa segura. Fontes: `regis-ef7d62eda3748119ba3e9e9e:pNone:1079.0-1270.0`.

### 4.2 Turbulência excessiva na zona de gás
Na seção secundária, a separação depende da decantação gravitacional de gotículas arrastadas. As fontes são explícitas: **quanto menor a turbulência do gás, melhor a eficiência de separação**. Logo, qualquer condição que aumente a turbulência na região superior do vaso tende a piorar a remoção de gotículas finas e elevar carryover. Fontes: `regis-ef7d62eda3748119ba3e9e9e:pNone:1079.0-1270.0`, `regis-6afa562b7a4623c44e6a8025:pNone:1715.0-1957.0`.

### 4.3 Sobrecarga hidráulica, gasosa ou por golfadas
A eficiência do separador depende de tempo de residência e de regime de escoamento compatíveis com o projeto. As fontes observam que separadores horizontais, embora normalmente mais eficientes na separação gás/líquido e adequados a sistemas com espuma e alta razão gás/óleo, têm **menor capacidade de absorver grandes variações de fluxo ou golfadas**. Em transientes severos, a seção primária pode ser sobrecarregada, o inventário líquido pode oscilar e o polimento do gás se torna menos eficaz. Fontes: `regis-ef7d62eda3748119ba3e9e9e:pNone:1079.0-1270.0`.

### 4.4 Controle deficiente de nível e pressão
As fontes associam diretamente o comportamento do separador ao controlador de pressão na saída de gás e ao controlador de nível na descarga de líquido. Isso implica que falhas de instrumentação, sintonia inadequada ou operação fora da faixa do controlador podem contribuir para carryover, por exemplo ao elevar o nível líquido indevidamente ou ao perturbar o regime de escoamento no topo do vaso. Fontes: `regis-ef7d62eda3748119ba3e9e9e:pNone:1079.0-1270.0`.

### 4.5 Uso indevido do scrubber como separador principal
As fontes alertam que scrubber é projetado para **baixa carga líquida**. Portanto, quando ele recebe líquido em quantidade incompatível com sua função — por deficiência do separador preliminar, transientes ou arraste anormal a montante — cresce a probabilidade de carryover para jusante. Em projeto e troubleshooting, esse ponto é decisivo: nem todo problema de líquido no compressor se resolve aumentando a capacidade do scrubber; frequentemente é necessário atuar na separação principal. Fontes: `regis-6afa562b7a4623c44e6a8025:pNone:1715.0-1957.0`, `regis-6afa562b7a4623c44e6a8025:pNone:1829.0-2073.0`.

## 5. Sólidos arrastados no gás e implicações para o arranjo do separador
Além de líquido, o gás pode carregar sólidos. As fontes mencionam scrubbers como equipamentos capazes de remover arraste de líquidos e sólidos antes da compressão e registram que separadores de teste podem evidenciar consequências indesejáveis como presença de areia ou lama.

Para serviços com sólidos, a geometria do vaso influencia a operação. Segundo as fontes, separadores horizontais costumam ter melhor eficiência gás/líquido, mas apresentam maior dificuldade de remoção dos sólidos produzidos. Já os verticais favorecem deposição localizada no fundo e tendem a facilitar a remoção. Portanto, em poços ou sistemas com expectativa de produção de sólidos, a decisão horizontal versus vertical não deve ser feita apenas pela eficiência de separação de gotas, mas também pela mantenabilidade do sistema. Fontes: `regis-ef7d62eda3748119ba3e9e9e:pNone:976.0-1181.0`, `regis-ef7d62eda3748119ba3e9e9e:pNone:1079.0-1270.0`, `regis-6afa562b7a4623c44e6a8025:pNone:1715.0-1957.0`.

## 6. Consequências operacionais do carryover
A consequência mais crítica explicitamente citada nas fontes é o risco de dano aos compressores. O carreamento de líquido para a sucção pode atingir equipamentos de alto custo e comprometer disponibilidade da planta.

Além disso, como o gás segue depois para condicionamento, desidratação e eventual uso como gás combustível, exportação ou reinjeção, a permanência de água e condensados a jusante contraria o objetivo básico do tratamento do gás: reduzir riscos de corrosão, formação de hidratos e problemas de movimentação/compressão. Em termos de segurança e confiabilidade, a remoção de arrastes é, portanto, uma etapa de proteção de equipamentos e também de qualidade do gás tratado. Fontes: `regis-ef7d62eda3748119ba3e9e9e:pNone:1079.0-1270.0`, `regis-ef7d62eda3748119ba3e9e9e:pNone:976.0-1181.0`, `regis-6afa562b7a4623c44e6a8025:pNone:1715.0-1957.0`.

## 7. Critérios práticos de projeto, operação e troubleshooting
Com base nas fontes, alguns critérios práticos podem ser consolidados.

### 7.1 Em projeto
- prever **separação preliminar efetiva** antes do scrubber;
- selecionar o tipo de vaso considerando não apenas eficiência gás/líquido, mas também tendência a espuma, razão gás/óleo, produção de sólidos e ocorrência de golfadas;
- assegurar internals adequados: defletores/difusores de entrada, regiões de baixa turbulência, seção de acumulação compatível com o tempo de retenção requerido e extrator de névoa na saída de gás;
- não atribuir ao scrubber a função de remover grandes quantidades de líquido.

### 7.2 Em comissionamento e partida
- verificar instalação e integridade dos internals de separação e do extrator de névoa;
- confirmar atuação dos controles de pressão e nível;
- testar drenagem de líquido no fundo de scrubbers/vasos depuradores;
- acompanhar com atenção condições transitórias e golfadas, pois essas condições podem sobrecarregar a separação.

### 7.3 Em operação e solução de problemas
Diante de suspeita de carryover, a análise deve priorizar:

1. presença de espuma no vaso;
2. aumento de turbulência ou regime fora do envelope de projeto;
3. elevação indevida de nível líquido;
4. perda de efetividade da separação primária ou do demister;
5. sobrecarga do scrubber por líquido vindo a montante;
6. acúmulo/produção de sólidos incompatível com o arranjo do vaso.

Essa lógica evita tratar o sintoma apenas no fim da linha. Em muitos casos, o carryover observado no compressor é consequência de mau desempenho do separador principal, e não apenas do scrubber. Fontes: `regis-ef7d62eda3748119ba3e9e9e:pNone:1079.0-1270.0`, `regis-6afa562b7a4623c44e6a8025:pNone:1715.0-1957.0`, `regis-6afa562b7a4623c44e6a8025:pNone:1829.0-2073.0`.

## 8. Síntese técnica
Para fins de avaliação profissional, a ideia central é que a separação de arrastes no gás produzido em FPSOs depende da combinação entre:

- mecanismo físico adequado de separação;
- tempo de residência e baixa turbulência;
- seleção correta entre separador de produção e scrubber;
- instrumentação de pressão e nível funcionando corretamente;
- compatibilização do equipamento com espuma, sólidos e golfadas.

Quando esses elementos falham, cresce a probabilidade de carryover. Quando são bem integrados, o gás segue para compressão e condicionamento com menor risco operacional e maior aderência aos objetivos de qualidade do tratamento. Fontes: `regis-6afa562b7a4623c44e6a8025:pNone:1715.0-1957.0`, `regis-ef7d62eda3748119ba3e9e9e:pNone:976.0-1181.0`, `regis-ef7d62eda3748119ba3e9e9e:pNone:1079.0-1270.0`, `regis-6afa562b7a4623c44e6a8025:pNone:1829.0-2073.0`.