# Captação e bombeamento de água do mar para injeção em reservatório

## 1. Função do subsistema e lógica de projeto

Em um sistema offshore de injeção de água do mar, o trecho de **captação e bombeamento** precisa garantir simultaneamente:

1. **vazão** suficiente para alimentar o tratamento e a malha de injeção;
2. **pressão** suficiente para vencer perdas hidráulicas e atender a pressão requerida a jusante;
3. **estabilidade operacional** das bombas, evitando cavitação, entrada de gás/ar e oscilações;
4. **qualidade mínima da água** para não comprometer a formação, a integridade dos equipamentos e a injetividade.

O material disponível mostra um arranjo típico em que a água do mar é captada por bomba, passa por etapas de filtração e condicionamento químico, e depois segue para a bomba de injeção. Embora o foco desta faceta seja o bombeamento, a qualidade da água afeta diretamente a hidráulica do sistema: filtros sujos elevam a perda de carga, sólidos aceleram erosão/corrosão, oxigênio dissolvido e microrganismos afetam integridade, e entrada de ar/gás pode desestabilizar bombas centrífugas.

**Fontes da seção:** `petroles-004c2afadba7ea17c7dd7908:pNone:844668.0-844719.0`, `regis-8b1756079f1d5a9d1fa3f2b0:pNone:620.0-713.0`

## 2. Arranjo de captação, pré-tratamento e sua influência no bombeamento

Um caso descrito no material apresenta dois arranjos de injeção de água do mar:

### 2.1 Sistema antecipado
- captação de água do mar por bomba, em profundidade;
- filtragem grosseira com filtros de tela;
- dosagem química com:
  - eliminador de oxigênio;
  - inibidor de incrustação;
  - biocida orgânico;
- filtragem fina com filtros de cartucho;
- injeção por bomba de alta pressão.

### 2.2 Sistema definitivo
Em relação ao arranjo antecipado, o sistema definitivo passou a incluir:
- **filtros de areia antes dos filtros de cartucho**;
- **torre de desaeração** para remoção do oxigênio dissolvido;
- bomba de injeção com capacidade superior.

### 2.3 Implicações para captação e bombas
Do ponto de vista hidráulico e operacional, esse encadeamento tem consequências claras:

- **filtração grosseira** protege bombas e etapas posteriores contra partículas maiores;
- **filtros de areia** reduzem a carga de sólidos antes dos cartuchos, diminuindo entupimento prematuro e perda de carga excessiva;
- **filtros de cartucho** refinam a qualidade final, mas também podem se tornar limitantes de vazão quando há colmatação;
- **desaeração** reduz o teor de oxigênio dissolvido, importante para corrosão e integridade do sistema;
- **dosagem química** atua preventivamente sobre incrustação, corrosão e atividade microbiológica, preservando linhas, bombas e injetividade;
- **a bomba de injeção** deve ser selecionada não só pela pressão requerida, mas também considerando a perda de carga acumulada em filtros, linhas, válvulas e manifold.

Na prática, o projeto do bombeamento não pode ser separado do pré-tratamento: cada estágio de tratamento melhora a qualidade da água, mas também adiciona perda de carga e exige margem hidráulica apropriada no dimensionamento da bomba.

**Fontes da seção:** `petroles-004c2afadba7ea17c7dd7908:pNone:844668.0-844719.0`

## 3. Compatibilidade da água e consequências para a operação das bombas

O mesmo caso informa que, para dimensionar o sistema de tratamento da água de injeção, foram realizadas análises de:

- distribuição de partículas da água do mar;
- compatibilidade da água do mar com a água da formação;
- sensibilidade da formação à água de injeção.

Os resultados apontaram possibilidade de formação de incrustações como:
- carbonato de cálcio;
- sulfato de bário;
- carbonato ferroso;
- hidróxido férrico;
- sulfato de estrôncio;
- sulfato de cálcio.

Por isso, recomendou-se tratamento com **inibidor de incrustação**. Também foram relatados testes de sensibilidade com redução de permeabilidade atribuída provavelmente à **migração de finos**.

Para o subsistema de captação e bombeamento, isso significa que atender apenas vazão e pressão **não basta**. Se a água injetada não for compatível com a formação, pode ocorrer perda de injetividade mesmo com bombas adequadamente dimensionadas. Além disso:

- precipitados e sólidos podem elevar a perda de carga em filtros e linhas;
- incrustações podem reduzir seção de escoamento e degradar desempenho hidráulico;
- corrosão e biofouling podem comprometer confiabilidade das bombas e das linhas;
- migração de finos no reservatório pode reduzir aceitação de água, elevando a contrapressão vista pela bomba de injeção.

O acompanhamento da qualidade da água foi associado aos seguintes parâmetros:
- teor de sólidos em suspensão;
- fator de filtrabilidade;
- distribuição de partículas.

Essas variáveis são relevantes porque conectam **qualidade da água** com **desempenho hidráulico** e **risco de dano de formação**.

**Fontes da seção:** `petroles-004c2afadba7ea17c7dd7908:pNone:844668.0-844719.0`

## 4. Fundamentos de hidráulica para garantir vazão e pressão

### 4.1 Altura manométrica do sistema
Uma formulação apresentada nas fontes, para sistemas cujo ponto inicial e final estejam sujeitos à pressão atmosférica, é:

**Hm = Hg + ΔHt**

Onde:
- **Hm** = altura manométrica;
- **Hg** = altura geométrica;
- **ΔHt** = perda de carga total na tubulação.

Essa relação é útil para entender que a bomba precisa fornecer energia suficiente para vencer:
- desnível geométrico;
- perdas distribuídas no escoamento;
- perdas localizadas em singularidades.

No serviço real de injeção em unidades offshore, a linha de descarga normalmente opera em sistema pressurizado; portanto, a equação acima representa a parcela geométrica + perdas, devendo-se ter atenção ao fato de que a fonte não desenvolve explicitamente a parcela de pressão de processo a jusante.

### 4.2 Perdas de carga distribuídas e localizadas
A fonte destaca dois caminhos para tratar perdas localizadas:

- uso de **coeficientes K** para singularidades;
- uso de **comprimentos equivalentes**.

São especialmente importantes, no contexto de captação e bombeamento de água do mar:
- entradas de linha;
- curvas e cotovelos;
- tês e derivações;
- válvulas de retenção e de controle;
- crivos/elementos de proteção;
- medidores;
- filtros e internos que adicionem restrição.

Também é apresentada uma expressão de curva do sistema, baseada em Hazen-Williams e perdas localizadas:

**Hm = Hg + (10,64 × Q^1,85 / (C^1,85 × D^4,87)) × L + (8 × K × Q^2 / (g × π^2 × D^4))**

Onde:
- **Q** = vazão;
- **C** = coeficiente de Hazen-Williams;
- **D** = diâmetro do conduto;
- **L** = comprimento;
- **K** = coeficiente de perda localizada;
- **g** = aceleração da gravidade.

O valor prático dessa formulação, para esta faceta, é mostrar que o aumento de vazão eleva rapidamente a perda de carga. Em sistemas com filtros, válvulas, manifolds e linhas longas, a bomba de captação ou de injeção pode sair do ponto de operação esperado se a curva real do sistema se deslocar por sujeira, incrustação ou mudança de configuração.

### 4.3 NPSH e prevenção de cavitação
As fontes trazem a inequação de projeto:

**NPSHd > NPSHr**

e uma forma prática com margem mínima:

**NPSHd - 0,6 m > NPSHr**

com:

**NPSHd = Hatm - ΔHs - Hgs - Hv**

Onde:
- **Hatm** = carga correspondente à pressão atmosférica;
- **ΔHs** = perda de carga na sucção;
- **Hgs** = altura geométrica de sucção;
- **Hv** = carga correspondente à pressão de vapor.

Para bombas de captação de água do mar, isso implica que o projeto de sucção deve limitar perdas em:
- trechos de sucção;
- válvulas e retenções;
- curvas;
- crivos e filtros a montante;
- possíveis restrições por incrustação ou biofouling.

Quanto maior a perda na sucção, menor o NPSHd e maior o risco de cavitação. Isso é crítico na captação porque a degradação do lado de sucção pode não ser imediatamente percebida apenas pela pressão de descarga.

**Fontes da seção:** `regis-8b1756079f1d5a9d1fa3f2b0:pNone:620.0-713.0`

## 5. Seleção e configuração de bombas para água de injeção

### 5.1 Princípio da bomba centrífuga multiestágio
Uma das fontes descreve a bomba centrífuga de múltiplos estágios como um conjunto em que cada estágio possui **impelidor e difusor** operando em série. O impelidor transmite energia ao fluido; o difusor direciona o escoamento ao estágio seguinte. Em termos práticos, a associação em série de estágios eleva a capacidade de geração de pressão.

Outra fonte resume a relação operacional da seguinte forma:
- **o aumento do número de estágios não altera a vazão da bomba de forma primária**;
- **a rotação está associada à vazão**;
- **o número de estágios está associado ao limite de pressão/altura desenvolvida**.

Para esta faceta, isso dá um critério de decisão importante:

- se o problema principal é **atingir maior pressão de injeção**, o recurso típico é selecionar uma bomba com maior capacidade de altura, frequentemente por mais estágios;
- se o problema principal é **ajustar vazão**, a análise passa pela rotação e pela interseção entre curva da bomba e curva do sistema;
- em qualquer caso, o ponto de operação real depende das perdas do sistema e não apenas da bomba isolada.

### 5.2 Escolha entre bomba de captação e bomba de injeção
Ainda que as fontes não tragam um procedimento completo de seleção para FPSO, os princípios aplicáveis são:

- **bomba de captação**: prioriza robustez de sucção, tolerância à operação contínua e atendimento da vazão para alimentação do tratamento;
- **bomba de injeção**: prioriza geração de alta pressão com estabilidade e margem para variação de perda de carga na malha;
- ambas exigem alimentação elétrica confiável e operação dentro da faixa recomendada do fabricante.

### 5.3 Sensibilidade a sólidos e gás/ar
As fontes sobre bombas centrífugas submersas relatam que o desempenho é degradado por:
- presença de gás na sucção, com risco de cavitação e bloqueio de passagem do líquido;
- areia/sólidos abrasivos, com corrosão abrasiva e redução de eficiência.

Embora essas referências sejam de BCS, o mecanismo físico é útil para interpretar sistemas centrífugos de captação/injeção: sucção com ar/gás e fluido com sólidos tende a comprometer estabilidade, desgaste e capacidade hidráulica.

**Fontes da seção:** `petroles-4ee4bce16acf674505c8912d:pNone:511875.0-511914.0`, `petroles-4ee4bce16acf674505c8912d:pNone:334707.0-334749.0`

## 6. Instabilidade operacional: cavitação, entrada de gás/ar e espuma

Uma fonte experimental sobre linha com bomba centrífuga mostra um ponto importante para diagnóstico: houve vibração, barulho e comportamento anômalo da linha em rotações mais altas. O cálculo indicava **NPSHd superior ao NPSHr**, isto é, a desigualdade de cavitação estava satisfeita; ainda assim, a instabilidade persistia. A hipótese levantada foi a **sucção de espuma** formada no tanque de retorno.

Essa observação é valiosa para sistemas de água do mar:

- atender ao critério de NPSH é **necessário**, mas pode não ser **suficiente** para garantir estabilidade;
- entrada de ar, gás ou espuma na sucção pode produzir vibração, ruído, oscilação de vazão e degradação do desempenho;
- portanto, problemas de sucção devem ser investigados não só como cavitação clássica, mas também como **ingestão de fase gasosa** ou formação de espuma.

Outra fonte, em contexto de BCS, descreve fenômenos associados à presença de gás:
- **surging**: oscilações abruptas da capacidade de elevação e da pressão de descarga, mais pronunciadas em menor vazão de líquido;
- **gas-locking**: bloqueio da passagem do fluido pela presença de gás, com intermitência de vazão e faixas de produção nula.

Para bombas de água de injeção, esses fenômenos não devem ser transpostos de forma literal, mas servem como analogia útil para o diagnóstico de:
- entrada de ar na captação;
- desaeração deficiente;
- bolsões de gás em linhas;
- sucção de espuma;
- perda de escorva ou instabilidade da sucção.

Sinais operacionais coerentes com esse tipo de problema incluem:
- oscilações da pressão de descarga;
- intermitência de vazão;
- ruído e vibração anormais;
- perda de capacidade sem aumento equivalente de contrapressão do sistema.

**Fontes da seção:** `regis-72a4fd7832bb5654a2905a6a:pNone:732.60-774.60`, `petroles-4ee4bce16acf674505c8912d:pNone:1345070.0-1345116.0`

## 7. Monitoramento, instrumentação e controle operacional

As fontes indicam uma lógica de monitoramento baseada em:
- medição de pressão em pontos distintos da linha;
- medição de diferencial de pressão;
- medição de temperatura;
- medição de vazão;
- aquisição e processamento dos dados com instrumentos calibrados;
- uso de sistema supervisório/SCADA para centralizar informação e apoiar decisões operacionais.

Para o subsistema de captação e bombeamento, isso permite estruturar uma supervisão mínima orientada a desempenho:

### 7.1 Variáveis de processo prioritárias
- pressão de sucção da bomba de captação;
- pressão de descarga da bomba de captação;
- pressão de sucção da bomba de injeção;
- pressão de descarga da bomba de injeção;
- diferencial de pressão em filtros e trechos críticos;
- vazão de água tratada/injetada;
- temperatura, quando relevante ao desempenho do sistema e dos instrumentos;
- parâmetros de qualidade da água: sólidos em suspensão, fator de filtrabilidade e distribuição de partículas.

### 7.2 Uso prático do SCADA
Segundo a fonte, sistemas SCADA coletam dados de processo, compilam, formatam e apresentam as informações ao operador em tempo real para intervenção e tomada de decisão. Aplicado a este contexto, isso viabiliza:
- detecção precoce de aumento de perda de carga em filtros;
- comparação entre rotação/comando da bomba e vazão efetiva;
- identificação de instabilidade por oscilações de pressão;
- acompanhamento contínuo da qualidade da água de injeção;
- diagnóstico diferenciado entre problema de bomba, restrição hidráulica e deterioração da água.

### 7.3 Relação entre medição e garantia de desempenho
Se a vazão cai, por exemplo, o conjunto de medições ajuda a separar cenários:
- **queda de vazão + aumento de ΔP em filtro**: provável colmatação/restrição a montante;
- **queda de vazão + oscilação de pressão**: possível entrada de ar/gás/espuma;
- **pressão alta requerida com vazão ainda insuficiente**: curva do sistema deslocada ou bomba inadequada ao serviço;
- **vazão e pressão atendidas, mas piora de injetividade**: problema de qualidade/compatibilidade da água e não apenas de bombeamento.

**Fontes da seção:** `regis-72a4fd7832bb5654a2905a6a:pNone:732.60-774.60`, `petroles-4ee4bce16acf674505c8912d:pNone:334707.0-334749.0`, `petroles-004c2afadba7ea17c7dd7908:pNone:844668.0-844719.0`

## 8. Critérios operacionais de otimização focados em captação e bombas

Com base nos materiais fornecidos, a otimização do subsistema de captação e bombeamento deve perseguir os seguintes objetivos práticos:

1. **manter baixa perda de carga na sucção**, preservando NPSHd;
2. **controlar o estado dos filtros**, evitando deslocamento excessivo da curva do sistema;
3. **garantir estabilidade de sucção**, minimizando entrada de ar/gás/espuma;
4. **selecionar corretamente número de estágios e rotação**, conforme a necessidade dominante de pressão ou vazão;
5. **integrar tratamento químico e hidráulica**, porque água fora de especificação compromete tanto a formação quanto o desempenho mecânico/hidráulico do sistema;
6. **usar supervisão em tempo real** para agir antes da perda de desempenho se converter em queda de injeção ou dano ao ativo.

Em síntese, garantir vazão e pressão de injeção em água do mar não é apenas um problema de “bomba maior”. É uma combinação entre:
- projeto de sucção;
- curva hidráulica do sistema;
- configuração da bomba;
- estado dos filtros;
- qualidade da água;
- estabilidade operacional e monitoramento contínuo.

**Fontes da seção:** `petroles-004c2afadba7ea17c7dd7908:pNone:844668.0-844719.0`, `regis-8b1756079f1d5a9d1fa3f2b0:pNone:620.0-713.0`, `petroles-4ee4bce16acf674505c8912d:pNone:511875.0-511914.0`, `petroles-4ee4bce16acf674505c8912d:pNone:334707.0-334749.0`, `regis-72a4fd7832bb5654a2905a6a:pNone:732.60-774.60`, `petroles-4ee4bce16acf674505c8912d:pNone:1345070.0-1345116.0`