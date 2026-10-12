# Hidrociclones de água produzida

## 1. Papel dos hidrociclones no tratamento de água produzida para descarte

Na produção offshore, a água produzida é um efluente volumoso, potencialmente tóxico e ambientalmente sensível. O impacto de seu descarte depende, entre outros fatores, da **composição da água produzida**, do **volume descartado** e da **capacidade de diluição do corpo receptor**. Em FPSOs, o tratamento precisa atender simultaneamente a requisitos ambientais e a restrições severas de **peso, espaço e capacidade de processamento**. Nesse contexto, os hidrociclones são amplamente empregados porque oferecem separação óleo/água com arranjo mais compacto que equipamentos gravitacionais convencionais. Eles também podem aliviar vasos e tanques do processamento primário, preservando volume útil para o óleo e reduzindo a necessidade de expansão da planta por tecnologia puramente gravitacional.

Do ponto de vista de processo, os hidrociclones normalmente tratam uma corrente de água já submetida a uma separação inicial em vasos de produção; o remanescente de óleo disperso, muitas vezes em gotas pequenas e com diferença de densidade relativamente baixa em relação à água, é justamente o caso em que a separação gravitacional se torna difícil e a intensificação centrífuga passa a ser atrativa.

**Fontes:** `petroles-4ee4bce16acf674505c8912d:pNone:615258.0-615294.0`, `petroles-4ee4bce16acf674505c8912d:pNone:615277.0-615309.0`, `petroles-4ee4bce16acf674505c8912d:pNone:615310.0-615348.0`, `regis-5a27e35ea7822cf53d9323c2:pNone:18.120-45.60`

## 2. Princípio físico de separação

O hidrociclone é um separador estático, sem partes móveis, constituído por trechos cilíndricos e cônicos. A alimentação entra tangencialmente, impondo rotação ao escoamento e criando um **campo centrífugo** muito superior ao gravitacional. Em termos físicos, a aceleração centrífuga pode ser representada por:

\[
 a_c = \frac{v_\theta^2}{r}
\]

em que:
- \(a_c\) = aceleração centrífuga;
- \(v_\theta\) = componente azimutal da velocidade;
- \(r\) = distância radial ao eixo.

Como a velocidade de rotação tende a aumentar em regiões mais próximas do eixo, o campo centrífugo promove **segregação radial por densidade**:
- a **fase menos densa** tende a migrar para a região central;
- a **fase mais densa** tende a migrar para a periferia, junto à parede.

Em hidrociclones de água produzida para descarte, isso significa que o **óleo disperso** tende a se concentrar na região central e a sair preferencialmente pelo **overflow**, enquanto a fase aquosa mais densa se concentra na periferia e sai pelo **underflow**.

Outro aspecto essencial é a **reversão de fluxo** no sentido axial: coexistem dois sentidos opostos de escoamento no interior do equipamento devido ao campo de pressões gerado pela rotação. Essa reversão simplifica a obtenção de duas correntes separadas, uma rica na fase leve e outra rica na fase pesada.

**Fontes:** `regis-5a27e35ea7822cf53d9323c2:pNone:0.0-35.0`, `regis-5a27e35ea7822cf53d9323c2:pNone:18.120-45.60`, `petroles-4ee4bce16acf674505c8912d:pNone:615328.0-615371.0`

## 3. Configuração construtiva e implicações para projeto

### 3.1 Componentes básicos

Os trechos fornecidos descrevem como elementos básicos do hidrociclone:
- **seção de entrada da alimentação**;
- **seção cilíndrica**;
- **seção cônica de redemoinho**;
- **tubo de overflow** (frequentemente associado ao *vortex finder*);
- **orifício/tubo de underflow**.

A alimentação tangencial é decisiva para gerar a rotação do fluido. O **overflow** fica próximo à seção de alimentação e remove preferencialmente a corrente enriquecida na fase leve. O **underflow** fica próximo ao vértice do cone e remove preferencialmente a corrente enriquecida na fase pesada.

### 3.2 Papel do vortex finder

O *vortex finder* tem pelo menos duas funções operacionais importantes nos trechos utilizados:
1. **controlar a separação e o início do escoamento interno**;
2. **evitar curto-circuito da alimentação para o overflow**.

Esse segundo ponto é crucial para diagnóstico de falha: se a geometria ou a condição hidráulica favorecer curto-circuito, parte da alimentação pode alcançar o overflow sem a segregação adequada, prejudicando a pureza das correntes e deslocando o ponto de operação esperado.

### 3.3 Geometria como variável de desempenho

Os materiais citam explicitamente que a eficiência do hidrociclone é sensível à geometria. Entre as variáveis geométricas avaliadas em estudos computacionais estão, por exemplo, diâmetro do corpo, diâmetros de overflow e underflow, altura cilíndrica e outros parâmetros dimensionais. Mesmo sem os valores numéricos completos nos trechos, a mensagem técnica é clara: **não existe desempenho independente de geometria**. O projeto deve ser compatibilizado com:
- características do fluido;
- teor de óleo na alimentação;
- faixa de vazão esperada;
- pressões disponíveis;
- objetivo de separação.

Essa dependência explica o desenvolvimento de famílias distintas de hidrociclones para **altos, médios e baixos teores de óleo** e a possibilidade de uso em série na corrente rica em água, selecionando-se o tipo mais adequado para cada aplicação.

**Fontes:** `petroles-4ee4bce16acf674505c8912d:pNone:615277.0-615309.0`, `petroles-4ee4bce16acf674505c8912d:pNone:615328.0-615371.0`, `regis-5a27e35ea7822cf53d9323c2:pNone:0.0-35.0`

## 4. Variáveis de processo que governam o desempenho

Os trechos disponíveis apontam vários fatores que afetam diretamente a eficiência de separação óleo/água em hidrociclones.

### 4.1 Diferença de densidade entre as fases

A força motriz da segregação radial depende da diferença de massa específica entre fase dispersa e fase contínua. Quanto menor essa diferença, mais difícil tende a ser a separação, especialmente para gotas finas.

### 4.2 Tamanho das gotas de óleo

A remoção de pequenas gotículas dispersas é descrita como particularmente difícil. Quanto menor o diâmetro da gota, menor tende a ser a tendência de migração radial, o que reduz a eficiência do equipamento.

### 4.3 Viscosidade e estabilidade da emulsão

Os textos associam a estabilidade de emulsões a fatores como:
- viscosidade das fases;
- massa específica;
- proporção volumétrica das fases;
- distribuição de diâmetros da fase interna;
- tensão e viscosidade interfaciais;
- envelhecimento do filme interfacial;
- presença de íons;
- presença de agentes emulsificantes naturais do petróleo, como parafinas e asfaltenos.

Esses fatores podem estabilizar gotas menores e dificultar coalescência, tornando o hidrociclone menos efetivo para produzir underflow com baixo TOG.

### 4.4 Teor de óleo na alimentação

Um estudo de CFD citado nos materiais observou que, ao reduzir a concentração de óleo na alimentação, também se reduziu a concentração de óleo medida no underflow. Em termos práticos, isso sugere que o desempenho do hidrociclone depende do **regime de carga oleosa** e que a comparação entre desempenhos deve sempre considerar o teor de óleo de entrada.

### 4.5 Queda de pressão e condições hidráulicas

As quedas de pressão são explicitamente citadas como um dos fatores que afetam o desempenho. Como o hidrociclone usa a própria energia do escoamento para gerar o campo centrífugo, a condição hidráulica disponível influencia fortemente:
- intensidade do redemoinho;
- capacidade de processamento;
- split operacional;
- eficiência de remoção de óleo.

### 4.6 Capacidade de processamento e faixa de vazão

A capacidade de processamento também aparece como fator relevante. Em operação real, isso significa que o hidrociclone não deve ser analisado apenas por TOG na saída; deve-se verificar se ele está processando a vazão para a qual foi projetado e em qual faixa de pressão/vazão sua curva hidrodinâmica continua válida.

**Fontes:** `petroles-004c2afadba7ea17c7dd7908:pNone:478912.0-478959.0`, `petroles-4ee4bce16acf674505c8912d:pNone:615310.0-615348.0`, `petroles-4ee4bce16acf674505c8912d:pNone:615328.0-615371.0`, `petroles-4ee4bce16acf674505c8912d:pNone:615277.0-615309.0`

## 5. Indicadores e curvas para avaliar desempenho

A avaliação profissional de um hidrociclone não deve depender de um único número de TOG. Os materiais destacam uma abordagem mais completa, baseada em comportamento hidrodinâmico e eficiência de separação.

### 5.1 Curva de capacidade

Uma das curvas hidrodinâmicas citadas relaciona a **vazão mássica pelo hidrociclone** com a **perda de pressão entre a alimentação e a corrente rica em água**. Essa curva permite verificar se o equipamento está operando numa região compatível com seu projeto e é útil para distinguir:
- problema de processo a montante;
- desvio hidráulico do próprio hidrociclone;
- incompatibilidade entre vazão real e faixa operacional.

### 5.2 Split

O **split** é definido como a fração da vazão de alimentação que deixa o hidrociclone pelo overflow:

\[
\text{split} = \frac{Q_{to}}{Q_{te}}
\]

em que:
- \(Q_{te}\) = vazão total na entrada;
- \(Q_{to}\) = vazão total que sai pelo overflow.

Operacionalmente, o split é um indicador central porque altera quanto da alimentação acompanha a corrente rica em óleo. Mudanças de split afetam simultaneamente a pureza do overflow e do underflow.

### 5.3 DPR (razão de perda de carga)

O **DPR** é definido como a razão entre a perda de carga da alimentação para o overflow e a perda de carga da alimentação para o underflow:

\[
DPR = \frac{P_a - P_o}{P_a - P_u}
\]

em que:
- \(P_a\) = pressão na alimentação;
- \(P_o\) = pressão no overflow;
- \(P_u\) = pressão no underflow.

A curva **split × DPR** foi tratada como uma das principais curvas experimentais de comportamento hidrodinâmico. Em diagnóstico, isso é muito útil: se o TOG do underflow piora ao mesmo tempo em que a relação split–DPR sai da tendência histórica, há forte indício de alteração hidráulica do equipamento ou da malha associada.

### 5.4 Eficiência de remoção de óleo

Um conceito de eficiência explicitamente fornecido é a **eficiência de remoção de óleo**, definida como a razão entre a vazão de óleo que sai pelo overflow e a vazão de óleo que entra no hidrociclone:

\[
\eta_{óleo} = \frac{Q_{oo}}{Q_{oe}}
\]

em que:
- \(Q_{oe}\) = vazão de óleo na entrada;
- \(Q_{oo}\) = vazão de óleo na saída pelo overflow.

Os materiais indicam ainda uma preocupação com a **pureza das duas correntes** (overflow e underflow), o que é coerente com a operação real: não basta remover óleo para o overflow; é preciso garantir que o underflow fique suficientemente limpo para a etapa seguinte ou para descarte.

### 5.5 Eficiência parametrizada pelo teor de óleo de entrada

As curvas de desempenho são descritas como relacionando a eficiência de separação ao split operacional, **parametrizadas em função do teor de óleo na alimentação**. Isso é particularmente importante para FPSOs com produção variável ao longo da vida do campo, pois a degradação aparente do hidrociclone pode, na verdade, ser consequência de mudança de envelope de alimentação.

**Fontes:** `petroles-004c2afadba7ea17c7dd7908:pNone:711937.0-711983.0`, `petroles-004c2afadba7ea17c7dd7908:pNone:478912.0-478959.0`

## 6. Controle operacional e otimização

### 6.1 Variáveis que merecem acompanhamento contínuo

Com base nos trechos, o controle operacional de hidrociclones para água produzida deve priorizar o acompanhamento de:
- pressões na alimentação, overflow e underflow;
- vazões nas correntes principais;
- split e DPR calculados;
- teor de óleo na alimentação e no underflow;
- estabilidade da alimentação, incluindo variações de emulsão e propriedades do fluido.

Embora o material traga um banco de testes, a lógica é transferível para a planta: primeiro identifica-se o **ponto de operação desejado**, depois busca-se sua manutenção estável por meio das variáveis hidráulicas do sistema.

### 6.2 Controle manual e manutenção automática do ponto de operação

No laboratório móvel descrito nas fontes, o operador podia localizar manualmente o ponto de operação e, em seguida, optar por mantê-lo automaticamente. O valor profissional desse conceito é que o hidrociclone não deve ser operado “por hábito” ou apenas por abertura fixa de válvulas; ele deve ser operado em torno de um ponto definido por desempenho esperado.

Em FPSO, isso se traduz em uma disciplina operacional em que a equipe deve correlacionar:
- queda de pressão disponível;
- split observado;
- qualidade do underflow;
- teor de óleo de entrada.

### 6.3 Otimização prática

A otimização de um conjunto de hidrociclones passa por três frentes complementares:
1. **compatibilizar a geometria com a aplicação**;
2. **manter o equipamento dentro da janela hidrodinâmica adequada**;
3. **reavaliar o arranjo conforme mudam as características do fluido ao longo do tempo**.

As fontes citam famílias de hidrociclones para altos, médios e baixos teores de óleo e uma rotina de projeto capaz de selecionar o tipo mais adequado, estimar número de unidades e condições operacionais. Isso reforça um ponto importante: quando o envelope do processo muda, a otimização pode exigir não apenas ajuste operacional, mas também **reconfiguração do arranjo**, uso em série ou revisão do número de hidrociclones em serviço.

**Fontes:** `petroles-004c2afadba7ea17c7dd7908:pNone:711937.0-711983.0`, `regis-5a27e35ea7822cf53d9323c2:pNone:0.0-35.0`

## 7. Falhas, sintomas e diagnóstico de hidrociclones

### 7.1 Sintoma principal: aumento do óleo no underflow

Para tratamento de água produzida visando descarte, o sintoma operacional mais crítico é o aumento do teor de óleo no underflow. À luz dos materiais, esse desvio pode estar associado a:
- gotas excessivamente pequenas;
- redução da diferença de densidade entre as fases;
- aumento de viscosidade ou estabilização de emulsão;
- queda de pressão inadequada;
- split fora da faixa esperada;
- geometria inadequada para o teor de óleo real da alimentação;
- curto-circuito para o overflow por desenho/condição inadequada do vortex finder.

### 7.2 Quando o problema é do fluido, e não do equipamento

Os trechos sobre emulsão deixam claro que parte das perdas de desempenho não é “falha mecânica” do hidrociclone, mas consequência de mudança nas propriedades do sistema óleo/água. Exemplos:
- maior ação de agentes emulsificantes naturais do petróleo;
- alteração de temperatura com efeito sobre viscosidade e estabilidade;
- mudança de proporção volumétrica entre fases;
- distribuição mais fina do diâmetro de gotas.

Nesses casos, insistir apenas em ajustes hidráulicos pode não resolver o desvio; o problema pode exigir atuação a montante sobre condicionamento de processo ou química.

### 7.3 Diagnóstico por correlação entre variáveis

Uma forma robusta de diagnóstico é correlacionar simultaneamente:
- TOG/óleo no underflow;
- pressões \(P_a\), \(P_o\), \(P_u\);
- split;
- DPR;
- teor de óleo na alimentação.

Exemplos de leitura técnica possíveis:
- **TOG no underflow piora e DPR/split também se deslocam:** forte suspeita de desvio hidráulico, obstrução parcial, alteração de backpressure ou operação fora da janela.
- **TOG piora, mas hidráulica permanece semelhante:** suspeita mais forte sobre mudança das propriedades do fluido, estabilidade de emulsão ou redução do tamanho de gotas.
- **Desempenho ruim crônico desde a partida:** suspeita de incompatibilidade entre geometria selecionada e o teor de óleo/condições reais da aplicação.

### 7.4 Limites do diagnóstico puramente empírico

Os materiais também sugerem cautela: estudos de CFD, ensaios de campo e curvas experimentais são essenciais porque o comportamento do hidrociclone é fortemente dependente da aplicação. Portanto, diagnósticos baseados apenas em “regras de bolso” têm risco alto de erro quando mudam óleo, água, vazão ou faixa de pressão.

**Fontes:** `petroles-004c2afadba7ea17c7dd7908:pNone:478912.0-478959.0`, `petroles-4ee4bce16acf674505c8912d:pNone:615310.0-615348.0`, `petroles-4ee4bce16acf674505c8912d:pNone:615328.0-615371.0`, `petroles-004c2afadba7ea17c7dd7908:pNone:711937.0-711983.0`

## 8. Arranjos de processo e aplicação em série

Os materiais mostram que hidrociclones podem ser empregados como parte de **sistemas compactos de separação**, inclusive com famílias diferentes para teores altos, médios e baixos de óleo, posicionadas em série na corrente rica em água. O raciocínio de engenharia por trás disso é importante para FPSOs:
- uma única etapa pode não ser a melhor solução para toda a faixa de operação;
- o teor de óleo de entrada muda ao longo do sistema e ao longo da vida do campo;
- a seleção do hidrociclone deve partir das **características reais dos fluidos** e não apenas do valor nominal de vazão.

Esse entendimento é útil tanto para projeto inicial quanto para revamps de sistemas de tratamento de águas oleosas.

**Fontes:** `regis-5a27e35ea7822cf53d9323c2:pNone:0.0-35.0`, `regis-5a27e35ea7822cf53d9323c2:pNone:18.120-45.60`

## 9. Considerações ambientais e conformidade

Os trechos citam que, no Brasil, o descarte de água produzida deve obedecer a limites regulatórios de **óleos e graxas**, mencionando média aritmética simples mensal e valor máximo diário segundo referência ao CONAMA. Contudo, os valores numéricos aparecem redigidos como `<NUMBER>` nos materiais fornecidos, de modo que este documento não reproduz números que não estão legíveis na fonte.

Ainda assim, para avaliação profissional, ficam estabelecidos três pontos:
1. o hidrociclone deve ser avaliado em função da **qualidade do underflow para descarte**;
2. o desempenho não pode ser separado da **variabilidade do fluido e das condições hidráulicas**;
3. a conformidade ambiental depende não só do equipamento em si, mas do conjunto separador primário + hidrociclone + controle operacional + monitoramento analítico.

**Fontes:** `petroles-4ee4bce16acf674505c8912d:pNone:615258.0-615294.0`, `petroles-4ee4bce16acf674505c8912d:pNone:615310.0-615348.0`, `petroles-004c2afadba7ea17c7dd7908:pNone:478912.0-478959.0`