# QRA e ALARP em estudos de segurança

## 1. Finalidade do QRA no estudo de segurança
A Análise Quantitativa de Riscos (QRA/AQR) é a etapa em que os resultados das análises de perigos, consequências e frequências são integrados para estimar o risco imposto por um empreendimento. Nos trechos fornecidos, a lógica geral da AQR é apresentada em cinco macroetapas:

1. caracterização do sistema;
2. identificação de perigos e acidentes;
3. estimativa das consequências dos acidentes;
4. estimativa das frequências dos acidentes;
5. estimativa e avaliação dos riscos.

Para a faceta **QRA e ALARP**, o ponto central é a quinta etapa: converter cenários acidentais em métricas quantitativas de risco e compará-las com critérios de tolerabilidade, distinguindo o que é intolerável, o que é negligenciável e o que permanece na faixa **ALARP**.

Em termos práticos, isso significa que a QRA não é apenas um exercício de cálculo: ela serve para apoiar decisão de projeto, operação, manutenção e mudanças, indicando se o risco residual é compatível com os critérios adotados para o estudo e se ainda existem medidas de redução razoavelmente praticáveis.

*Fontes: ["regis-23f10815ee0a0a8b2ca5ffea:pNone:2973.0-3196.0", "regis-ecacf0f324e4abda266a20de:pNone:3368.0-3627.0"]*

## 2. Encadeamento técnico da quantificação do risco
A quantificação do risco depende de um encadeamento lógico entre:

- **cenário acidental** identificado;
- **frequência** de ocorrência desse cenário;
- **efeitos físicos** esperados;
- **vulnerabilidade** das pessoas expostas;
- **métrica final de risco**.

Os trechos indicam que o risco pode ser interpretado, de forma agregada, como uma relação entre **frequência/probabilidade** e **consequência**. Uma forma resumida apresentada é:

- **R = Σ (f_i x C_i)**

onde `f_i` é a frequência do evento `i` e `C_i` é a consequência associada, normalmente expressa em mortes ou dano grave.

Esse encadeamento é particularmente relevante em estudos de segurança porque evita tratar frequência e consequência de modo isolado. Um evento raro com grande severidade e um evento frequente com severidade moderada podem, dependendo dos valores, gerar riscos comparáveis ou até inverter a priorização.

Para cenários com substâncias inflamáveis, os trechos também mostram que a frequência final de cada efeito físico depende do caminho percorrido no encadeamento acidental, incluindo fatores como:

- evento iniciador;
- direção/frequência do vento, quando aplicável;
- probabilidade de ignição imediata ou tardia.

Logo, a QRA é sensível às hipóteses adotadas na árvore de eventos e aos dados de frequência usados na modelagem.

*Fontes: ["regis-ecacf0f324e4abda266a20de:pNone:3368.0-3627.0", "petroles-4ee4bce16acf674505c8912d:pNone:2230996.0-2231037.0", "petroles-4ee4bce16acf674505c8912d:pNone:2231017.0-2231060.0"]*

## 3. Métricas quantitativas principais

### 3.1. Risco individual
Os trechos definem **risco individual** como a frequência esperada, normalmente em base anual, de um indivíduo situado em determinada posição sofrer um dano, em geral fatalidade, em decorrência de acidentes na instalação.

A formulação apresentada é:

- **RI(x,y) = Σ RI(x,y,i)**
- **RI(x,y,i) = f_i x pf_i(x,y)**

onde:

- `RI(x,y)` = risco individual total de fatalidade no ponto `(x,y)`;
- `RI(x,y,i)` = contribuição do evento `i` para o ponto `(x,y)`;
- `f_i` = frequência do evento `i`;
- `pf_i(x,y)` = probabilidade de o evento `i` resultar em fatalidade nesse ponto, conforme os efeitos físicos e a vulnerabilidade.

Os resultados são usualmente apresentados por **contornos de iso-risco**. Esses contornos conectam pontos com o mesmo valor de risco individual e permitem visualizar a distribuição espacial do risco.

No contexto de um estudo de segurança, isso é útil para:

- comparar alternativas de arranjo físico;
- avaliar exposição em posições específicas;
- verificar se áreas críticas ficam em faixas de risco mais altas;
- acompanhar o efeito de medidas redutoras de frequência ou consequência.

Embora os trechos de referência sejam fortemente orientados a instalações terrestres e vizinhança externa, o conceito permanece válido para estudos offshore: a métrica exige definir claramente **quem está exposto**, **onde está exposto** e **por quanto tempo**.

*Fontes: ["regis-23f10815ee0a0a8b2ca5ffea:pNone:2973.0-3196.0", "regis-6ce306d1aa9065c0dae3e980:pNone:3018.0-3293.0", "petroles-4ee4bce16acf674505c8912d:pNone:2231017.0-2231060.0"]*

### 3.2. Risco social
Os trechos definem **risco social** como o risco para um determinado número ou agrupamento de pessoas expostas aos danos de um ou mais cenários acidentais.

Sua forma clássica de apresentação é a **curva F-N**, que relaciona:

- `N` = número de fatalidades; e
- `F(N)` = frequência acumulada de acidentes com `N` ou mais fatalidades.

A lógica de construção é:

1. definir os eventos iniciais;
2. combinar cada evento com condições relevantes, como vento e ignição, quando aplicável;
3. calcular, para cada combinação, o número esperado de mortes;
4. calcular a frequência dessa combinação;
5. acumular as frequências de todas as combinações com número de fatalidades maior ou igual a `N`.

A forma resumida apresentada nos trechos é:

- **F(N) = soma das frequências dos eventos/composições para os quais N_i >= N**

Os textos também destacam que a estimativa do risco social requer, no mínimo:

- tipo de população exposta;
- variação temporal da exposição, como períodos do dia;
- características das edificações ou condições de abrigo, quando aplicável.

Em termos metodológicos, isso significa que a curva F-N não depende só das consequências físicas; ela também depende da modelagem populacional e de ocupação.

*Fontes: ["regis-23f10815ee0a0a8b2ca5ffea:pNone:2973.0-3196.0", "regis-6ce306d1aa9065c0dae3e980:pNone:3018.0-3293.0", "petroles-4ee4bce16acf674505c8912d:pNone:2231017.0-2231060.0"]*

## 4. De onde vêm as frequências e as probabilidades de fatalidade

### 4.1. Frequências dos cenários
Os trechos indicam que a frequência dos cenários pode ser estimada a partir de:

- dados de falha da própria unidade;
- dados de equipamentos semelhantes em outras unidades;
- bancos de dados de confiabilidade;
- modelagem por árvores de falhas e árvores de eventos, quando a complexidade justificar.

A **árvore de falhas** é descrita como método sistemático para partir de um evento topo indesejado e decompor suas causas com operadores lógicos como `E` e `OU`. O resultado inclui conjuntos mínimos de falha e ajuda a identificar quais combinações de eventos iniciadores levam ao evento principal.

A **árvore de eventos** representa os possíveis desdobramentos a partir de um evento iniciador, incluindo estados alternativos de falha e sucesso ao longo do encadeamento acidental. Em cenários com inflamáveis, as probabilidades de ignição imediata e tardia afetam diretamente a frequência dos efeitos físicos finais.

Assim, a frequência do cenário final não é, em geral, a mesma frequência do evento iniciador; ela é a frequência do iniciador multiplicada pelas probabilidades dos ramos percorridos.

### 4.2. Vulnerabilidade e fatalidade
Os trechos informam que a vulnerabilidade pode ser estimada por **equações do tipo Probit**, de modo a converter intensidade de efeito físico em probabilidade de fatalidade.

Também aparecem exemplos simplificados em que, para certos fenômenos, se adota fatalidade total dentro de determinados envelopes de efeito. Esses exemplos são úteis para entender a lógica do cálculo, mas devem ser tratados como **hipóteses de modelo dependentes do método e do cenário**, e não como regra universal.

Em resumo, a componente `pf_i(x,y)` do risco individual, e a estimativa de fatalidades usada no risco social, dependem de dois grupos de insumos:

- **intensidade do fenômeno físico** no local de interesse;
- **modelo de vulnerabilidade** adotado.

*Fontes: ["regis-ecacf0f324e4abda266a20de:pNone:3267.0-3513.0", "petroles-4ee4bce16acf674505c8912d:pNone:2230996.0-2231037.0", "petroles-4ee4bce16acf674505c8912d:pNone:2231017.0-2231060.0"]*

## 5. Critérios de aceitabilidade, tolerabilidade e ALARP
Os trechos deixam claro que a avaliação quantitativa do risco só se completa quando os resultados são comparados com **critérios previamente definidos**.

Dois pontos conceituais são importantes:

1. **tolerável** não é sinônimo de **aceitável**;
2. risco em faixa tolerável/ALARP não pode ser simplesmente ignorado.

Segundo o material citado, o conceito de **Tolerability of Risk (TOR)** serve para apoiar a decisão sobre se um risco é:

- inaceitável;
- tolerável sob controle e revisão contínua;
- amplamente aceitável/negligenciável.

Na formulação resumida trazida nos trechos, há três regiões:

- **região intolerável**: acima do limite superior;
- **região negligenciável ou amplamente aceitável**: abaixo do limite inferior;
- **região ALARP**: faixa intermediária em que o risco deve ser reduzido tanto quanto razoavelmente praticável.

Para a referência histórica citada da CETESB para atividades industriais terrestres, os limites de **risco individual** mencionados são:

- **risco máximo tolerável: 1 x 10^-5 por ano**;
- **risco negligenciável: menor que 1 x 10^-6 por ano**.

Os trechos também registram que **dutos** foram tratados como caso particular, com outros valores, o que reforça que os critérios dependem do contexto do empreendimento e não devem ser transplantados automaticamente.

Para **risco social**, a comparação é feita pela posição da curva F-N em relação às curvas-limite de tolerabilidade. Os trechos não trazem a parametrização numérica completa dessas curvas, mas deixam claro que a interpretação também segue a lógica de três regiões: intolerável, ALARP e negligenciável.

Uma consequência prática importante é a seguinte:

- estar **abaixo do limite de intolerabilidade** não encerra a discussão;
- se o resultado permanece na região **ALARP**, ainda é necessário justificar se medidas adicionais de redução são ou não razoavelmente praticáveis.

*Fontes: ["regis-6ce306d1aa9065c0dae3e980:pNone:3018.0-3293.0", "regis-ecacf0f324e4abda266a20de:pNone:3368.0-3627.0"]*

## 6. O que significa demonstrar ALARP na prática
Com base nos trechos, a demonstração de ALARP pode ser estruturada como uma sequência lógica de engenharia e gestão:

### 6.1. Estimar o risco de base
Primeiro calcula-se o risco com o conjunto de cenários, frequências, consequências e vulnerabilidades adotado no estudo. O resultado deve ser apresentado, no mínimo, nas métricas aplicáveis:

- risco individual por localização/contorno;
- risco social por curva F-N.

### 6.2. Comparar com os critérios definidos
O risco calculado deve ser comparado com os critérios adotados para o estudo, identificando se está:

- acima do limite de intolerabilidade;
- entre os limites, na faixa ALARP;
- abaixo do limite inferior.

### 6.3. Identificar medidas adicionais de redução
Os trechos citam, como exemplos de medidas de prevenção e proteção a serem consideradas em programas de gerenciamento de riscos:

- melhoria da qualidade da instalação;
- aumento da confiabilidade dos sistemas de controle e segurança;
- programas de inspeção e manutenção;
- programas de treinamento e capacitação;
- ações de redução dos impactos de acidentes;
- sistemas de contenção de vazamentos;
- redução de inventário de substâncias perigosas;
- sistemas de abatimento de vapores tóxicos ou inflamáveis;
- reforço estrutural para absorção de impactos de explosões;
- plano de ação de emergência;
- comunicação de riscos.

Essas medidas são candidatas típicas a alterar a QRA por uma ou ambas as vias:

- **redução de frequência** do cenário;
- **redução de consequência/vulnerabilidade**.

### 6.4. Requantificar o risco residual
Após propor medidas, a lógica correta é recalcular o risco. Isso permite mostrar, de forma tecnicamente rastreável, quais mudanças realmente deslocam:

- contornos de risco individual;
- curva F-N;
- posição do estudo em relação aos limites de tolerabilidade.

### 6.5. Justificar a suficiência da redução
Nos trechos, o ALARP é descrito como a região em que as medidas devem ser implementadas quando seus custos **não forem excessivamente altos** ou quando forem **tecnicamente viáveis** em comparação com o benefício de segurança obtido.

Portanto, uma demonstração de ALARP não deveria se limitar a afirmar que o risco residual ficou “abaixo do intolerável”. Ela deve mostrar, de forma estruturada:

- quais medidas adicionais foram consideradas;
- qual efeito quantitativo ou qualitativo cada medida teria;
- quais medidas foram implementadas;
- por que medidas remanescentes não foram adotadas, se for o caso;
- por que o risco residual pode ser entendido como tão baixo quanto razoavelmente praticável.

### 6.6. Manter revisão contínua
Os trechos sobre tolerabilidade enfatizam que tolerar um risco significa conviver com ele sob **controle** e **revisão constante**, e não tratá-lo como resolvido em definitivo. Assim, a condição ALARP depende de pressupostos de projeto, operação e desempenho das salvaguardas; se esses pressupostos mudarem, a demonstração deve ser reavaliada.

*Fontes: ["regis-6ce306d1aa9065c0dae3e980:pNone:3018.0-3293.0", "regis-ecacf0f324e4abda266a20de:pNone:3368.0-3627.0"]*

## 7. Implicações para tomada de decisão em estudos de segurança
A partir dos trechos, alguns critérios de decisão se destacam:

- **Resultado acima do limite intolerável**: o estudo aponta necessidade inequívoca de redução de risco antes de se considerar o arranjo ou condição como aceitável.
- **Resultado na faixa ALARP**: exige análise de opções adicionais e justificativa da suficiência do risco residual.
- **Resultado abaixo do limite negligenciável**: indica situação comparativamente mais favorável, sem eliminar a necessidade de manter controles proporcionais e revisão dos pressupostos.

Além disso, a utilidade prática da QRA aumenta quando seus resultados são conectados ao gerenciamento de riscos, pois as recomendações do estudo alimentam medidas de prevenção, proteção e emergência.

*Fontes: ["regis-ecacf0f324e4abda266a20de:pNone:3368.0-3627.0", "regis-6ce306d1aa9065c0dae3e980:pNone:3018.0-3293.0"]*

## 8. Limites de extrapolação para FPSO
Os trechos fornecidos oferecem boa base conceitual para **quantificação de risco, critérios de aceitabilidade e lógica ALARP**, mas grande parte do material está formulada para:

- instalações industriais terrestres;
- população externa ao empreendimento;
- critérios de órgãos e referências usados em contextos específicos.

Assim, para uso em FPSOs, a principal leitura correta é metodológica:

- calcular frequência e consequência dos cenários;
- converter em risco individual e social/grupal conforme a população modelada;
- comparar com critérios explicitamente escolhidos para o estudo;
- demonstrar redução de risco residual até nível ALARP por meio de medidas tecnicamente justificadas e reavaliação quantitativa.

O documento técnico aqui composto, portanto, é mais confiável como base para entender **o raciocínio de QRA e ALARP** do que como fonte autônoma de critérios normativos offshore aplicáveis sem adaptação.

*Fontes: ["regis-23f10815ee0a0a8b2ca5ffea:pNone:2973.0-3196.0", "regis-6ce306d1aa9065c0dae3e980:pNone:3018.0-3293.0", "regis-ecacf0f324e4abda266a20de:pNone:3368.0-3627.0"]*