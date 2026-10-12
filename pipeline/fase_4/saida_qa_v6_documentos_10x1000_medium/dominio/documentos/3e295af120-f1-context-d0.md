# Seleção e dimensionamento de PSV e BDV

## 1. Escopo efetivamente coberto pelos trechos
Os trechos fornecidos sustentam principalmente critérios de **seleção e dimensionamento de PSV (Pressure Safety Valve)** e a forma como a **contrapressão**, o **tipo de fluido** e o **cenário de sobrepressão** afetam esse dimensionamento. Há também conteúdo útil sobre **fenômenos operacionais** decorrentes de especificação inadequada e sobre o uso de **simulação dinâmica** como apoio à análise.

Para **BDV (blowdown valve)**, os trechos não trazem critérios próprios de seleção, capacidade, tempo de despressurização, Cv, filosofia de falha, lógica ESD/SIS ou equações de dimensionamento. Portanto, este documento trata BDV apenas como lacuna explícita do material fornecido, sem completar com inferências externas.

**Fontes:** `petroles-004c2afadba7ea17c7dd7908:pNone:4274145.0-4274176.0`, `petroles-004c2afadba7ea17c7dd7908:pNone:4274177.0-4274225.0`, `petroles-004c2afadba7ea17c7dd7908:pNone:4274127.0-4274164.0`

## 2. Papel da PSV na proteção contra sobrepressão
A PSV é apresentada como a **última camada de proteção** do processo quando as demais camadas — projeto adequado, controle, alarmes e intertravamentos — não conseguem manter a instalação em condição segura. Seu papel é abrir quando a pressão do sistema protegido excede a condição admissível de projeto em margem predeterminada, reduzindo automaticamente o risco associado ao excesso de pressão, desde que tenha sido **especificada, dimensionada e instalada corretamente**.

Um ponto importante dos trechos é que o dimensionamento não deve ser visto apenas como exercício conservativo. O material ressalta que o conceito de que “PSV superdimensionada não é problema” pode ser incorreto, porque o excesso de capacidade pode induzir comportamento instável da válvula e comprometer sua função protetiva.

**Fontes:** `petroles-004c2afadba7ea17c7dd7908:pNone:4273983.0-4274025.0`, `petroles-004c2afadba7ea17c7dd7908:pNone:4274145.0-4274176.0`

## 3. Terminologia essencial para seleção e cálculo
Os trechos trazem a terminologia básica necessária para leitura de folhas de dados, memória de cálculo e avaliação de desempenho de PSVs:

- **Pressão de ajuste (set pressure):** pressão manométrica na qual a PSV é ajustada para abrir em condições anormais de operação.
- **Sobrepressão (overpressure):** aumento de pressão acima da pressão de ajuste alcançado durante a descarga da PSV, normalmente expresso como percentual da pressão de ajuste.
- **Pressão de alívio (relieving pressure):** soma da pressão de ajuste com a sobrepressão; representa a pressão máxima a que o equipamento estará sujeito durante o alívio.
- **Blowdown:** diferença entre a pressão de ajuste e a pressão de fechamento da válvula, usualmente expressa como percentual da pressão de ajuste.
- **Contrapressão superimposta (superimposed back-pressure):** pressão estática existente na saída da PSV imediatamente antes de sua abertura, oriunda do sistema de descarga.
- **Contrapressão desenvolvida (built-up backpressure):** aumento de pressão na saída da PSV que se desenvolve em consequência do escoamento após a abertura.
- **Contrapressão total (backpressure):** soma da contrapressão superimposta com a contrapressão desenvolvida.

Esses termos são centrais porque a seleção do tipo de PSV e os fatores de correção aplicados no cálculo dependem diretamente deles.

**Fontes:** `petroles-004c2afadba7ea17c7dd7908:pNone:4274145.0-4274176.0`

## 4. Seleção do tipo de PSV conforme fluido e contrapressão

### 4.1 Segurança versus alívio
Os trechos distinguem:

- **Válvulas de segurança:** aplicadas a **fluidos compressíveis** (gases e vapores), com alívio rápido e praticamente instantâneo.
- **Válvulas de alívio:** aplicadas principalmente a **fluidos incompressíveis** (líquidos), com abertura proporcional ao aumento da pressão acima da pressão de abertura.

Na prática documental apresentada, ambas aparecem sob a designação ampla **PSV**.

### 4.2 Tipos construtivos segundo efeito da contrapressão
A contrapressão participa do balanço de forças atuantes na válvula. Por isso, os trechos classificam as PSVs em três grupos:

- **Convencional:** desempenho afetado diretamente pela aplicação e/ou variação da contrapressão.
- **Balanceada:** incorpora meios de minimizar o efeito da contrapressão durante a descarga, por exemplo por **fole** ou **pistão**. O texto destaca a equalização de áreas para anular ou reduzir o efeito da contrapressão.
- **Piloto-operada:** composta por válvula principal e válvula piloto, em que a abertura da principal ocorre quando a piloto altera o balanço de pressão no pistão superior.

### 4.3 Critério prático de seleção indicado pelos trechos
Com base exclusivamente no material fornecido, a lógica de seleção é:

1. identificar se o fluido aliviado é predominantemente **gás/vapor** ou **líquido**;
2. avaliar se a **contrapressão** do sistema de descarga pode afetar o desempenho;
3. optar por **válvula convencional** quando esse efeito for aceitável;
4. optar por **balanceada** quando se queira reduzir a sensibilidade à contrapressão;
5. considerar **piloto-operada** quando a filosofia de operação exigir esse arranjo e o comportamento descrito for compatível com a aplicação.

Os trechos também citam que **disco de ruptura** pode ser combinado à PSV quando o fluido de processo for **corrosivo** ou contiver **sólidos em suspensão**.

**Fontes:** `petroles-004c2afadba7ea17c7dd7908:pNone:4274145.0-4274176.0`, `petroles-004c2afadba7ea17c7dd7908:pNone:4274177.0-4274225.0`

## 5. Roteiro de dimensionamento de PSV
Os trechos permitem reconstruir um roteiro técnico de dimensionamento em nível conceitual:

1. **Definir a pressão de ajuste da PSV.** Em geral, ela equivale à **pressão de projeto** do equipamento protegido e pode coincidir com a **PMTA**.
2. **Identificar todos os cenários de sobrepressão** plausíveis para o equipamento ou sistema onde a PSV está instalada.
3. **Calcular, para cada cenário, a vazão de alívio requerida e as propriedades do fluido nas condições de alívio.**
4. **Aplicar as equações de dimensionamento** apropriadas ao tipo de fluido e regime de escoamento.
5. **Obter a área requerida** para cada cenário.
6. **Escolher o caso dimensionante**, isto é, o cenário que produzir a **maior área requerida**.
7. **Selecionar o orifício padronizado** cuja área selecionada seja compatível com a área requerida do caso dimensionante.

O texto enfatiza que o orifício escolhido deve resultar de comparação entre a **área requerida calculada** e a **área padronizada disponível**, e não apenas de regra conservativa genérica.

**Fontes:** `petroles-004c2afadba7ea17c7dd7908:pNone:4274177.0-4274225.0`, `petroles-004c2afadba7ea17c7dd7908:pNone:4273983.0-4274025.0`

## 6. Critérios de dimensionamento para gás e vapor
Para alívio de **gás ou vapor**, os trechos informam que o dimensionamento se divide em dois grupos, conforme o regime de fluxo no orifício:

### 6.1 Fluxo crítico
O fluxo crítico ocorre quando a velocidade no orifício atinge a velocidade do som. Nessa condição, a pressão a jusante é menor ou igual à **pressão de fluxo crítico**.

### 6.2 Fluxo subcrítico
Se a pressão a jusante do orifício for maior que a pressão de fluxo crítico, o escoamento será subcrítico.

### 6.3 Consequência para a seleção do método de cálculo
Os trechos indicam que:

- para **válvulas convencionais** e **piloto-operadas**, usam-se conjuntos distintos de equações conforme o fluxo seja crítico ou subcrítico;
- para **válvulas balanceadas**, o cálculo pode continuar referenciado às equações de fluxo crítico, sendo que o parâmetro **Kb** passa a refletir a condição de escoamento e a influência da contrapressão.

### 6.4 Parâmetros de cálculo explicitamente citados
Os trechos não reproduzem as fórmulas completas, mas informam os principais parâmetros envolvidos:

- **A**: área requerida da PSV;
- **W**: vazão de alívio requerida que escoa pelo orifício;
- **P1g**: pressão de alívio para gás/vapor;
- **P2g**: contrapressão no alívio de gás/vapor;
- **PFC**: pressão de fluxo crítico;
- **k**: relação de calores específicos;
- **C**: função de *k*;
- **M**: peso molecular do gás ou vapor;
- **T**: temperatura de alívio;
- **Z**: fator de compressibilidade;
- **Kb**: fator de correção devido à contrapressão em alívio de gás/vapor;
- **Kd**: coeficiente de descarga;
- **Kc**: fator de correção para instalação de disco de ruptura combinado com PSV.

O material também informa que, para válvulas balanceadas, os valores de **Kb** podem ser obtidos por gráfico do API quando o fabricante não é conhecido; se o fabricante for conhecido, o valor recomendado é usar o dado do próprio fabricante.

**Fontes:** `petroles-004c2afadba7ea17c7dd7908:pNone:4274177.0-4274225.0`, `petroles-004c2afadba7ea17c7dd7908:pNone:4273951.0-4274006.0`, `petroles-004c2afadba7ea17c7dd7908:pNone:4274911.0-4275015.0`

## 7. Critérios de dimensionamento para líquido
Para **alívio de líquido**, os trechos indicam um conjunto próprio de equações e fatores de correção. Embora as fórmulas numéricas não estejam legíveis no material, os seguintes parâmetros aparecem como relevantes:

- **A**: área requerida;
- **Q**: fluxo volumétrico;
- **P1l**: pressão de alívio para líquido;
- **P2l**: contrapressão no alívio de líquido;
- **Gl**: densidade do líquido;
- **Kw**: fator de correção devido à contrapressão para líquido;
- **Kv**: fator de correção devido à viscosidade;
- **Re**: número de Reynolds;
- **Kd**: coeficiente de descarga;
- **Kc**: fator de correção associado ao uso de disco de ruptura.

Os trechos afirmam que **Kw** vale para contrapressão atmosférica e, no caso de válvulas balanceadas, o valor pode ser obtido em gráfico do API. Novamente, as notas reproduzidas indicam que, quando houver fabricante definido, o valor recomendado é o informado por esse fabricante.

**Fontes:** `petroles-004c2afadba7ea17c7dd7908:pNone:4274177.0-4274225.0`, `petroles-004c2afadba7ea17c7dd7908:pNone:4273951.0-4274006.0`, `petroles-004c2afadba7ea17c7dd7908:pNone:4274911.0-4275015.0`

## 8. Contrapressão como critério decisório de seleção e capacidade
A contrapressão é um dos elementos mais importantes do material fornecido porque afeta simultaneamente:

- o **desempenho mecânico/funcional** da PSV;
- a **classificação** entre válvula convencional, balanceada e piloto-operada;
- os **fatores de correção** de capacidade (**Kb** para gás/vapor e **Kw** para líquido);
- a própria distinção entre **fluxo crítico** e **subcrítico** em serviços compressíveis.

Do ponto de vista de engenharia, os trechos sustentam a seguinte interpretação prática:

- se a descarga impõe contrapressão relevante ou variável, a escolha de uma PSV **convencional** pode ser inadequada;
- a PSV **balanceada** é justamente descrita como opção para minimizar esse efeito;
- em cálculos de capacidade, a contrapressão não deve ser tratada apenas como dado da linha de flare/vent, mas como variável que interfere no **orifício requerido** e na **estabilidade operacional**.

**Fontes:** `petroles-004c2afadba7ea17c7dd7908:pNone:4274145.0-4274176.0`, `petroles-004c2afadba7ea17c7dd7908:pNone:4274177.0-4274225.0`, `petroles-004c2afadba7ea17c7dd7908:pNone:4274911.0-4275015.0`

## 9. Superdimensionamento e fenômenos operacionais
Os trechos são particularmente úteis ao mostrar que a seleção do orifício não pode ser feita por excesso “para garantir”. O material lista três fenômenos operacionais relevantes:

- **Chatter:** abertura e fechamento total rápidos e sucessivos, com contato do disco com o bocal, podendo danificar a válvula;
- **Flutter:** flutuação semelhante ao chatter, porém menos severa, sem contato do disco com o bocal;
- **Simmer:** escape audível ou visível em válvulas com fluidos compressíveis, ocorrendo próximo da pressão de ajuste.

O **chatter** é destacado como o fenômeno mais crítico por poder danificar a PSV a ponto de torná-la inoperante. As causas citadas nos trechos incluem:

- perda de carga excessiva na **entrada** da PSV;
- tubulações de entrada com **comprimento elevado**;
- **superdimensionamento** da PSV;
- **instalação imprópria**.

Isso leva a uma conclusão importante para avaliações profissionais: **um cálculo mais conservativo nem sempre é o cálculo mais seguro**. Em outras palavras, selecionar uma PSV demasiadamente grande pode reduzir a robustez operacional em vez de aumentá-la.

**Fontes:** `petroles-004c2afadba7ea17c7dd7908:pNone:4273983.0-4274025.0`, `petroles-004c2afadba7ea17c7dd7908:pNone:4274177.0-4274225.0`

## 10. Simulação dinâmica como apoio à definição das cargas de alívio
Os trechos mostram que a simulação dinâmica vem sendo usada como ferramenta de apoio em análise de risco e em estudos de PSV, especialmente para:

- complemento de **HAZOP**;
- análise de partidas e sintonia de controladores;
- avaliação de **PSVs existentes**;
- estudos de **revamp**;
- avaliação de **sistema de flare** em cenários de aumento de capacidade.

O texto informa que, na literatura revisada pelo autor, muitos trabalhos usam simulação dinâmica para estimar cargas de alívio e comparar com métodos convencionais, frequentemente encontrando vazões de alívio menores que as estimadas por métodos estáticos. Ao mesmo tempo, o próprio material afirma que não foi identificado, nessa revisão, trabalho que estabelecesse a simulação dinâmica como método de dimensionamento de PSV na etapa de projeto básico de forma consolidada.

Assim, o uso de simulação dinâmica aparece como **ferramenta complementar**, útil para refinar cenários e verificar conservadorismos, mas não como autorização automática para substituir procedimentos consagrados sem validação adicional.

**Fontes:** `petroles-004c2afadba7ea17c7dd7908:pNone:4274127.0-4274164.0`, `petroles-004c2afadba7ea17c7dd7908:pNone:4273983.0-4274025.0`

## 11. Exemplo de premissas de estudo e seus limites
Um dos trechos descreve um estudo em simulador no qual, para as válvulas de segurança analisadas, foram fornecidos apenas o **tamanho do orifício** e a **pressão de ajuste**, com a observação de que o **blowdown não foi considerado**. Nesse estudo, as pressões de ajuste e fechamento foram tratadas como iguais, e a pressão de abertura total foi considerada a pressão de alívio.

Também se informa que o estudo adotou diferentes margens de sobrepressão para cenários de **fogo**, **não-fogo** e **múltiplas PSVs**, mas os valores numéricos foram suprimidos nos trechos disponibilizados.

Essas premissas são importantes para análise crítica porque mostram que resultados de simulação dependem fortemente das simplificações adotadas. Em contexto profissional, isso significa que comparar cálculo estático, simulação dinâmica e desempenho real da válvula exige atenção às hipóteses do modelo.

**Fontes:** `petroles-004c2afadba7ea17c7dd7908:pNone:4274443.0-4274485.0`

## 12. O que os trechos permitem afirmar sobre BDV
Os trechos **não trazem base suficiente** para descrever, de forma tecnicamente rastreável, critérios de:

- seleção de **BDV** por função de despressurização;
- cálculo de tempo de blowdown;
- filosofia de falha aberta/fechada;
- escolha entre orifício, Cv ou característica intrínseca;
- integração de BDV com ESD, flare header, blowdown header e limitações térmicas de despressurização.

Portanto, para esta faceta, o material permite apenas registrar que o tema de BDV pertence ao escopo maior de sistemas de alívio e flare, porém **não é coberto por conteúdo técnico suficiente** nos trechos fornecidos.

**Fontes:** `petroles-004c2afadba7ea17c7dd7908:pNone:4274127.0-4274164.0`, `petroles-004c2afadba7ea17c7dd7908:pNone:4274443.0-4274485.0`

## 13. Síntese profissional aplicável
Com base apenas nos trechos, os critérios centrais para seleção e dimensionamento de PSV podem ser resumidos assim:

1. **Partir da pressão admissível do equipamento** para definir a pressão de ajuste.
2. **Levantar todos os cenários de sobrepressão** e calcular a carga de alívio de cada um.
3. **Distinguir corretamente o tipo de fluido**: compressível ou líquido.
4. **Verificar se a contrapressão afeta a escolha do tipo de válvula** e os fatores de correção.
5. **Aplicar o regime de escoamento apropriado** para gás/vapor: crítico ou subcrítico.
6. **Selecionar o menor orifício padronizado que atenda ao caso dimensionante**, evitando superdimensionamento desnecessário.
7. **Checar riscos operacionais** como chatter, flutter e simmer, principalmente quando houver grande conservadorismo, perda de carga elevada na entrada ou instalação inadequada.
8. **Usar simulação dinâmica como ferramenta de apoio**, não como substituição automática de critérios estabelecidos, salvo validação específica do caso.

**Fontes:** `petroles-004c2afadba7ea17c7dd7908:pNone:4273983.0-4274025.0`, `petroles-004c2afadba7ea17c7dd7908:pNone:4274145.0-4274176.0`, `petroles-004c2afadba7ea17c7dd7908:pNone:4274177.0-4274225.0`, `petroles-004c2afadba7ea17c7dd7908:pNone:4274127.0-4274164.0`, `petroles-004c2afadba7ea17c7dd7908:pNone:4274443.0-4274485.0`, `petroles-004c2afadba7ea17c7dd7908:pNone:4274911.0-4275015.0`, `petroles-004c2afadba7ea17c7dd7908:pNone:4273951.0-4274006.0`