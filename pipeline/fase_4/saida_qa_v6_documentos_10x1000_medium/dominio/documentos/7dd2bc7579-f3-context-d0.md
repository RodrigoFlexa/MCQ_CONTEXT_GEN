# Qualidade do óleo tratado em tratadores eletrostáticos

## 1. Função do tratador eletrostático no enquadramento do óleo

Em um arranjo típico de processamento de óleo em plataforma, os separadores gravitacionais removem principalmente gás, água livre e parte das gotas maiores de água. O tratador eletrostático entra como etapa de **ajuste fino** da qualidade do óleo, promovendo a remoção de gotículas de água dispersa e, por consequência, reduzindo também o teor de sal associado a essa fase aquosa. Nos trechos fornecidos, o óleo tratado após essa etapa segue para medição e armazenamento, já enquadrado quanto a **BS&W** e **salinidade** para exportação.

O **BS&W (Basic Sediment and Water)** é descrito como uma medida obtida a partir de amostra líquida da corrente produzida, expressa como porcentagem volumétrica e incluindo **água livre e sedimentos**. Para a qualidade do óleo exportado, tanto o BSW quanto o teor de sal são relevantes: a água residual aumenta custo de movimentação, pode elevar a viscosidade aparente da mistura e carrega sais corrosivos.

Um ponto importante para operação é que, **em geral**, ao reduzir significativamente o BSW também se reduz a salinidade do óleo, porque a maior parte do sal está dissolvida na água produzida. Contudo, isso **não é uma equivalência absoluta**: sais cristalinos e deficiências de lavagem/contato com água de diluição podem fazer com que o controle de salinidade exija atenção específica além do simples atendimento do BSW.

**Fontes:** `petroles-4ee4bce16acf674505c8912d:pNone:1447333.0-1447384.0`, `petroles-004c2afadba7ea17c7dd7908:pNone:1787561.0-1787598.0`, `petroles-004c2afadba7ea17c7dd7908:pNone:3131726.0-3131776.0`

## 2. Mecanismo de remoção de água e sal

### 2.1 Separação prévia e papel do campo elétrico

Nas unidades de produção, parte da água salina dispersa é retirada antes do tratador por separadores trifásicos de grande volume, que removem gotas maiores e bolsões de água livre. O tratador eletrostático atua sobre a fração mais difícil: gotas menores dispersas no óleo, que têm baixa tendência natural à sedimentação, sobretudo quando estão muito afastadas entre si.

No interior do tratador, placas ou eletrodos energizados promovem **eletrocoalescência**. O efeito principal citado nas fontes para campos alternados é a **atração entre dipolos induzidos**, dependente da intensidade do campo elétrico, do tamanho das gotas e da constante dielétrica do meio contínuo. À medida que as gotas crescem por coalescência, sua velocidade de sedimentação aumenta, facilitando a separação gravitacional e a migração para a interface óleo-água.

### 2.2 Relação entre desidratação e dessalgamento

Como os sais estão normalmente dissolvidos na fase aquosa, o decréscimo da salinidade do óleo está fortemente ligado à eficiência de desidratação. Em termos práticos:

- **menos água dispersa residual** tende a significar **menos sal residual** no óleo;
- porém, para remover sais dissolvidos de forma mais eficiente, pode ser necessário **lavar** o óleo com água de baixo teor salino;
- partículas cristalinas de sal ou contaminantes molháveis pela água só são removidos da fase oleosa se houver **bom contato com a água de lavagem**.

Isso explica por que um tratador pode apresentar BSW reduzido e, ainda assim, não atingir o melhor desempenho de dessalgamento se a etapa de contato água/óleo for inadequada.

### 2.3 Mistura e múltiplos ciclos de contato

Nos trechos sobre tecnologias avançadas, a eficiência do processo não depende apenas da válvula misturadora. Há indicação de que uma parte importante do contato entre salmoura residual e água de diluição ocorre durante os próprios ciclos de **dispersão, mistura, coalescência e separação** dentro do campo elétrico. Em outras palavras, a mistura eletrostática pode contribuir materialmente para a eficiência de remoção de sal.

**Fontes:** `petroles-004c2afadba7ea17c7dd7908:pNone:3131726.0-3131776.0`, `petroles-004c2afadba7ea17c7dd7908:pNone:3132101.0-3132157.0`, `petroles-004c2afadba7ea17c7dd7908:pNone:3132137.0-3132180.0`

## 3. Variáveis operacionais que controlam BSW e salinidade

## 3.1 Temperatura

A temperatura é uma variável central do desempenho do tratador:

- aumenta a temperatura -> reduz a viscosidade do óleo e da emulsão;
- menor viscosidade -> aumenta a mobilidade das gotas, a frequência de colisão e a taxa de coalescência;
- maior temperatura também favorece a sedimentação ao facilitar o escoamento da fase contínua.

Por isso, aquecimento a montante é prática usual para melhorar a separação. Entretanto, as fontes também registram **efeitos adversos** do aumento de temperatura:

- aumento da **solubilidade da água no petróleo**, o que pode elevar o teor de água residual no óleo tratado, especialmente em petróleos pesados;
- aumento da **condutividade elétrica**, com possível redução da eficiência de dessalgamento em certas condições.

Logo, não existe regra operacional de “quanto mais quente, melhor”. O ajuste de temperatura deve buscar o melhor compromisso entre redução de viscosidade, estabilidade da emulsão, condutividade elétrica e especificação de saída.

## 3.2 Vazão, capacidade e tempo de residência

A elevação da vazão de carga reduz o tempo de residência efetivo disponível para crescimento e sedimentação das gotas. Em offshore isso é particularmente crítico, porque o espaço e o volume disponível no convés são limitados. As fontes destacam que a indisponibilidade de grandes tempos de residência é um desafio característico das unidades marítimas, e que a combinação de calor, produtos químicos e campo elétrico é justamente a forma de compensar essa limitação.

Do ponto de vista de qualidade do óleo, aumentar throughput sem perder especificação requer verificar se o tratador continua fornecendo tempo suficiente para:

1. contato entre água de lavagem e salmoura residual;
2. crescimento das gotas por eletrocoalescência;
3. decantação até a interface.

## 3.3 Campo elétrico, tensão e frequência

Os trechos fornecidos indicam que a eficiência da eletrocoalescência depende do **gradiente de tensão entre eletrodos**, conceitualmente associado à razão entre a tensão aplicada e o espaçamento entre eletrodos. Além da amplitude do campo, tecnologias mais recentes utilizam:

- **frequência base**;
- **frequência modulada**;
- **forma de onda**;
- tensão mínima e máxima controladas;
- sistemas eletrônicos de controle do transformador, como o **Load Responsive Controller (LRC)**.

Segundo os textos, tecnologias convencionais em 50/60 Hz podem sofrer queda rápida de tensão ou formação de arcos, reduzindo a eficiência da desidratação. Já sistemas com modulação de frequência e controle da carga elétrica do vaso reduzem essa queda de tensão e podem operar com menor BSW de saída ou maior vazão para o mesmo BSW.

Para controle da qualidade do óleo, isso significa que o operador deve enxergar o sistema elétrico não apenas como “ligado/desligado”, mas como uma variável de processo que afeta diretamente a distribuição de tamanho de gotas e, portanto, a qualidade final do óleo.

## 3.4 Água de diluição/lavagem

A água adicionada ao processo tem papel duplo: diluir a salmoura residual e facilitar a remoção de sais por contato. As fontes apontam que essa água deve ter **baixo teor de sais** para ser efetiva. Também alertam que, em alguns contextos industriais, a chamada água “fresca” pode vir contaminada com hidróxido de sódio ou amônio, elevando o pH.

Esse ponto é particularmente relevante para óleos ricos em ácidos naftênicos: água de lavagem com pH elevado pode **estabilizar emulsões** e piorar o desempenho do tratador, comprometendo BSW e salinidade.

## 3.5 Desemulsificante

O uso de desemulsificantes é descrito como habitual. Esses produtos:

- migram para a interface água-óleo;
- rompem ou enfraquecem o filme interfacial;
- aumentam a taxa de coalescência das gotas.

A dosagem e o ponto de injeção dependem da solubilidade e da função ativa do produto. Para o foco de qualidade do óleo, a consequência prática é direta: uma dosagem inadequada pode resultar em água residual elevada, salinidade fora de meta e maior sensibilidade do processo a mudanças de vazão, temperatura ou composição do cru.

**Fontes:** `petroles-4ee4bce16acf674505c8912d:pNone:1447333.0-1447384.0`, `petroles-004c2afadba7ea17c7dd7908:pNone:1787561.0-1787598.0`, `petroles-004c2afadba7ea17c7dd7908:pNone:3131793.0-3131846.0`, `petroles-004c2afadba7ea17c7dd7908:pNone:3132101.0-3132157.0`, `petroles-004c2afadba7ea17c7dd7908:pNone:3132137.0-3132180.0`

## 4. Influência das propriedades do óleo e da emulsão

A dificuldade de atingir especificação de exportação cresce quando o óleo ou a emulsão apresentam características desfavoráveis à separação.

### 4.1 Petróleos pesados

As fontes apontam três causas principais para a maior dificuldade de desidratação de óleos pesados:

1. **alta viscosidade**, que reduz a velocidade de separação gravitacional e dificulta o transporte do desemulsificante até a interface;
2. **pequena diferença de densidade** entre óleo e salmoura, reduzindo a velocidade de sedimentação;
3. **maior concentração de agentes surfactantes**, favorecendo emulsões estáveis.

Em tais casos, mesmo com aquecimento, o óleo dessalgado/desidratado pode apresentar teor de água residual mais alto que o observado em petróleos leves.

### 4.2 Compostos naturais estabilizantes

A estabilidade das emulsões é influenciada por:

- **ácidos naftênicos**;
- **resinas**;
- **asfaltenos** e seus agregados;
- filmes interfaciais contendo espécies polares;
- sólidos finamente divididos orgânicos e inorgânicos.

Esses componentes podem formar ou reforçar filmes interfaciais rígidos, reduzindo a coalescência das gotas. Em consequência, aumenta a probabilidade de BSW elevado no óleo tratado e de retenção de sal na fase oleosa por permanência de salmoura fina dispersa.

### 4.3 Sólidos e sedimentos

Os sedimentos e sólidos finos têm efeito duplo:

- aparecem como parte do próprio BS&W;
- podem estabilizar a emulsão, dependendo do tamanho de partícula, da molhabilidade e da interação com compostos orgânicos pesados.

As fontes citam areia, lodo, argilas, silicatos, gipsita, sulfato de bário, óxidos e sulfetos de ferro como contaminantes possíveis. Quando esses sólidos se posicionam na interface e são molhados por óleo e água, podem dificultar bastante a quebra da emulsão.

### 4.4 pH da água

O pH da água influencia fortemente a estabilidade da emulsão porque altera a ionização de espécies presentes no filme interfacial. As fontes relatam que baixos valores de pH tendem a favorecer emulsões água-em-óleo, enquanto pH alto pode alterar o tipo e a estabilidade da emulsão. Em crus ácidos, pH elevado da água de diluição pode agravar a estabilidade da emulsão e piorar a qualidade do óleo de saída.

**Fontes:** `petroles-004c2afadba7ea17c7dd7908:pNone:3131726.0-3131776.0`, `petroles-004c2afadba7ea17c7dd7908:pNone:3131793.0-3131846.0`

## 5. Relação entre BSW, salinidade e risco de corrosão

Os sais mais frequentemente encontrados na água de formação são de sódio, cálcio e magnésio, sobretudo na forma de cloretos. A salinidade costuma ser reportada com base em cloreto de sódio, mas os cloretos de magnésio e cálcio têm relevância especial por sua associação com mecanismos corrosivos em altas temperaturas. Os textos indicam que a hidrólise desses sais pode gerar cloreto de hidrogênio, agravando a corrosão dos sistemas a jusante.

Do ponto de vista operacional no FPSO/FSO, a importância desse tema é que o controle de salinidade do óleo tratado não é apenas requisito comercial: ele também reduz o potencial de corrosão e de problemas posteriores em transferência, estocagem e processamento.

Consequência prática:

- **BSW fora de especificação** normalmente implica também maior transporte de sais;
- **salinidade alta**, mesmo com BSW aparentemente aceitável, pode indicar água residual muito salina, lavagem ineficiente ou presença de cristais/sólidos salinos não adequadamente removidos.

**Fontes:** `petroles-004c2afadba7ea17c7dd7908:pNone:3131793.0-3131846.0`, `petroles-004c2afadba7ea17c7dd7908:pNone:1787561.0-1787598.0`, `petroles-004c2afadba7ea17c7dd7908:pNone:3131726.0-3131776.0`

## 6. Estratégia prática de controle para atendimento da especificação de exportação

Com base nos mecanismos e causas descritos nas fontes, uma lógica técnica de ajuste do tratador para controlar BSW e salinidade pode ser estruturada da seguinte forma.

### 6.1 Quando o BSW de saída sobe

Verificar, em sequência:

1. **mudança de carga**: aumento de viscosidade, queda de API, aumento do teor de água, entrada de óleo mais ácido ou com mais sólidos;
2. **temperatura de alimentação**: confirmar se houve queda de aquecimento ou operação em faixa abaixo da necessária para reduzir a viscosidade;
3. **vazão de carga**: confirmar se a unidade está acima da condição em que mantém tempo de residência suficiente;
4. **desemulsificante**: revisar dosagem, ponto de injeção e compatibilidade com o cru atual;
5. **desempenho elétrico**: investigar queda de tensão, arco, instabilidade do campo ou necessidade de ajuste de frequência/modulação, quando disponível;
6. **qualidade da água de lavagem**: checar salinidade e pH.

### 6.2 Quando a salinidade do óleo permanece alta

Mesmo que o BSW tenha melhorado, investigar:

1. **água de diluição insuficiente** ou mal distribuída;
2. **mistura ineficiente** entre água fresca e salmoura residual;
3. **água de lavagem com salinidade elevada**, reduzindo o efeito de diluição;
4. **pH inadequado** da água em cru ácido/naftênico, estabilizando emulsão fina;
5. **presença de sais cristalinos ou sólidos molháveis pela água**, cuja remoção exige melhor contato com água de lavagem;
6. **limitação de residência/campo elétrico**, que permita a saída de gotas finas ainda salinas.

### 6.3 Quando o aumento de temperatura não melhora a qualidade

As fontes sugerem atenção para dois cenários:

- a temperatura pode já ter ultrapassado a faixa em que a redução de viscosidade compensa os efeitos adversos de maior solubilidade da água no óleo e de maior condutividade elétrica;
- emulsões envelhecidas ou estabilizadas por filmes interfaciais robustos podem responder pouco ao calor isoladamente.

Nesses casos, o ganho operacional pode depender mais de ajuste químico, qualidade da água de lavagem e parâmetros elétricos do que de mais aquecimento.

### 6.4 Quando a unidade está no limite de capacidade

Resultados comparativos citados nas fontes para tecnologias avançadas indicam que, para um mesmo fluxo, pode-se obter menor BSW de saída, ou, alternativamente, para um mesmo BSW, pode-se processar maior vazão. Isso reforça um critério operacional importante:

- se o ativo opera próximo do limite de capacidade, a solução não é apenas elevar carga; pode ser necessário reotimizar campo elétrico, frequência, mistura e química, ou reconhecer que a unidade entrou em região de desempenho degradado.

**Fontes:** `petroles-004c2afadba7ea17c7dd7908:pNone:1817276.0-1817339.0`, `petroles-004c2afadba7ea17c7dd7908:pNone:1787561.0-1787598.0`, `petroles-004c2afadba7ea17c7dd7908:pNone:3131726.0-3131776.0`, `petroles-004c2afadba7ea17c7dd7908:pNone:3131793.0-3131846.0`, `petroles-004c2afadba7ea17c7dd7908:pNone:3132101.0-3132157.0`, `petroles-004c2afadba7ea17c7dd7908:pNone:3132137.0-3132180.0`

## 7. Avaliação de desempenho e limitações de modelagem

As fontes mencionam que a literatura aberta ainda oferece poucos modelos fenomenológicos rigorosos para tratamento eletrostático de petróleo. Em geral, modelos empíricos ou semiempíricos relacionam o desempenho com variáveis como:

- propriedades físicas do óleo e da fase aquosa;
- vazão de carga;
- temperatura;
- gradiente de tensão;
- distribuição de tamanho de gotas.

Há indicação de que, em campos alternados, variáveis fundamentais incluem intensidade do campo elétrico, tamanho das gotas e constante dielétrica do meio contínuo. Também é registrado que alguns modelos assumem que a remoção de sal acompanha a desidratação porque o sal está essencialmente na fase aquosa. Essa hipótese é útil, mas não resolve todas as situações reais, especialmente para petróleos ultra-pesados, sistemas com forte efeito de emulsificantes/sólidos e cenários em que a etapa de lavagem é determinante.

Os trechos informam ainda que a modelagem do processo de dessalgação é dificultada por dois obstáculos práticos:

1. descrever adequadamente os fenômenos acoplados de quebra/coalescência e transferência de massa nas etapas de mistura;
2. obter determinação confiável do teor de sal no petróleo.

Portanto, para operação em FPSO, o controle de qualidade do óleo tratado deve combinar **medição de BSW e sal**, observação do comportamento elétrico do vaso e interpretação das condições da carga, em vez de confiar exclusivamente em um modelo simplificado.

**Fontes:** `petroles-004c2afadba7ea17c7dd7908:pNone:3132137.0-3132180.0`, `petroles-004c2afadba7ea17c7dd7908:pNone:3132746.0-3132821.0`

## 8. Medição e acompanhamento da qualidade

Os trechos citam métodos ASTM para determinação laboratorial de água e sedimentos no petróleo e de sal no cru, indicando a necessidade de monitoramento analítico específico para acompanhar desempenho do tratador. Mesmo sem transformar essas referências em obrigação normativa, elas mostram que o controle da qualidade do óleo tratado depende de duas medições distintas:

- **BS&W**: indicador de água e sedimentos residuais;
- **salinidade do óleo**: indicador direto da remoção de sais dissolvidos/carreados.

Operacionalmente, isso evita erro comum de inferir desempenho apenas por uma variável. Um tratador pode melhorar BSW sem maximizar dessalgamento, ou vice-versa, dependendo da qualidade da água de lavagem, da intensidade de mistura e da natureza da emulsão.

**Fontes:** `petroles-4ee4bce16acf674505c8912d:pNone:1447333.0-1447384.0`, `petroles-004c2afadba7ea17c7dd7908:pNone:3131726.0-3131776.0`, `petroles-004c2afadba7ea17c7dd7908:pNone:3132746.0-3132821.0`

## 9. Síntese operacional

Para enquadrar o óleo de exportação em BSW e salinidade, o tratador eletrostático deve ser entendido como a combinação de quatro funções integradas:

1. **quebra da emulsão** por calor, química e campo elétrico;
2. **crescimento das gotas** por eletrocoalescência;
3. **decantação gravitacional** até a interface óleo-água;
4. **lavagem/diluição da salmoura residual** para remover sal de forma efetiva.

O melhor resultado de qualidade não decorre de maximizar isoladamente uma variável, e sim de balancear:

- temperatura suficiente para reduzir viscosidade, sem piorar excessivamente condutividade e solubilidade de água;
- vazão compatível com tempo de residência disponível;
- campo elétrico estável, sem queda de tensão ou arcos recorrentes;
- desemulsificante compatível com o cru e bem dosado;
- água de lavagem adequada em qualidade, salinidade e pH;
- atenção especial a petróleos pesados, ácidos e com sólidos finos.

Essa visão é a base técnica para analisar por que um tratador atende ou não as especificações de exportação de óleo em FPSOs/FSOs.

**Fontes:** `petroles-4ee4bce16acf674505c8912d:pNone:1447333.0-1447384.0`, `petroles-004c2afadba7ea17c7dd7908:pNone:1787561.0-1787598.0`, `petroles-004c2afadba7ea17c7dd7908:pNone:3131726.0-3131776.0`, `petroles-004c2afadba7ea17c7dd7908:pNone:3131793.0-3131846.0`, `petroles-004c2afadba7ea17c7dd7908:pNone:3132101.0-3132157.0`, `petroles-004c2afadba7ea17c7dd7908:pNone:3132137.0-3132180.0`, `petroles-004c2afadba7ea17c7dd7908:pNone:3132746.0-3132821.0`, `petroles-004c2afadba7ea17c7dd7908:pNone:1817276.0-1817339.0`