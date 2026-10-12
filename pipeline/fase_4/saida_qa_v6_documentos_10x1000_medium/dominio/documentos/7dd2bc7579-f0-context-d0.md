# Coalescência eletrostática em tratadores eletrostáticos

## 1. Contexto do problema: emulsão água-em-óleo e necessidade do campo elétrico
No processamento primário de petróleo, especialmente em correntes de óleo com água produzida, é comum a formação de emulsões do tipo água em óleo (A/O). Essas emulsões podem ser geradas pelo cisalhamento turbulento no escoamento através de dutos, restrições, válvulas, bombas e outros equipamentos, além de movimentos de fluidos no reservatório. Quanto mais intenso o cisalhamento, maior a tendência de fragmentação das gotas de água em diâmetros menores, o que dificulta a separação subsequente.  

A eficiência da separação gravitacional depende fortemente de três variáveis principais: tamanho das gotas, diferença de densidade entre as fases e viscosidade da fase contínua. Em óleo, a separação água-óleo tende a ser lenta porque a diferença de densidade entre as fases é relativamente pequena e a viscosidade da fase contínua pode ser elevada, sobretudo em óleos pesados. Além disso, emulsificantes naturais do cru, sólidos finos e componentes semi-solúveis podem estabilizar a interface água-óleo. Nessa condição, apenas sedimentação gravitacional frequentemente não basta para atingir o teor de água especificado no óleo tratado, o que justifica o uso de tratadores eletrostáticos.  

Em termos de mecanismo global, a quebra de emulsão busca promover **coalescência**: gotas pequenas se unem, formam gotas maiores e, por isso, passam a sedimentar mais rapidamente sob ação da gravidade. Quanto menor o tamanho inicial das gotas, maior tende a ser o tempo de residência necessário no equipamento.  

**Rastreabilidade da seção:** `petroles-004c2afadba7ea17c7dd7908:pNone:1817056.0-1817119.0`, `petroles-004c2afadba7ea17c7dd7908:pNone:4420063.0-4420096.0`

## 2. Princípio físico da coalescência eletrostática
O tratamento eletrostático se aplica à separação de um líquido condutor disperso em outro não condutor. No caso típico da produção de petróleo, a fase dispersa é água salina ou água com sais dissolvidos, eletricamente mais condutiva, e a fase contínua é o óleo, eletricamente menos condutivo.  

Quando a emulsão é submetida a um campo elétrico:

1. **As gotas de água se polarizam** pela reorientação dos dipolos moleculares e pela distribuição de cargas induzidas.
2. **Cada gota deixa de se comportar como esfera ideal** e se alonga na direção do campo, assumindo geometria aproximadamente elíptica.
3. **Formam-se dipolos induzidos** nas gotas; isso cria atração entre extremidades de sinais opostos em gotas vizinhas.
4. **As gotas tendem a se alinhar em cadeias na direção do campo elétrico**.
5. O campo e as interações entre gotas favorecem colisão, drenagem do filme interfacial e, por fim, **coalescência**.
6. As gotas coalescidas passam a ter maior diâmetro e, portanto, maior velocidade de sedimentação.

As fontes também descrevem que esse alinhamento em cadeia pode favorecer descargas elétricas através da cadeia de gotas entre eletrodos. Em termos operacionais, isso ajuda a entender por que o campo elétrico precisa ser forte o suficiente para estimular coalescência, mas não tão agressivo a ponto de provocar instabilidade elétrica persistente ou ruptura excessiva de gotas.  

Segundo outra descrição da mesma base, três fenômenos físicos são especialmente relevantes quando um líquido não condutivo contendo gotículas condutivas é submetido ao campo elétrico:

- **polarização e alinhamento das gotas**, causando coalescência;
- **atração das gotículas pelo eletrodo**;
- **enfraquecimento do filme de emulsificantes na interface da gota**, facilitando a coalescência após colisão.

**Rastreabilidade da seção:** `petroles-004c2afadba7ea17c7dd7908:pNone:1817120.0-1817164.0`, `petroles-004c2afadba7ea17c7dd7908:pNone:4420063.0-4420096.0`

## 3. Mecanismos distintos em campos AC e DC

### 3.1 Campo de corrente contínua (DC)
Em campo DC, além da polarização, as gotas podem migrar em direção aos eletrodos por **eletroforese**. As fontes associam a coalescência em DC a dois mecanismos principais:

- **choque entre gotas com cargas de sinais contrários**;
- **migração eletroforética das gotas até superfícies ou regiões favoráveis à coalescência**.

Nesse regime, a força eletrostática associada à eletroforese foi apresentada na fonte como dependente de parâmetros como permissividade do vácuo, raio da gota, fração volumétrica da fase aquosa, constante dielétrica da fase contínua e gradiente de tensão aplicado. A expressão formal aparece corrompida no material, mas a dependência qualitativa é aproveitável.  

### 3.2 Campo de corrente alternada (AC)
Em campo AC, a velocidade líquida de migração da gota em direção aos eletrodos é descrita como praticamente nula. Nessa condição, predomina a ação de **dipolos induzidos** e a deformação periódica das gotas. Os efeitos mais relevantes são:

- polarização repetida da gota;
- distorção cíclica da geometria da gota;
- enfraquecimento do filme interfacial;
- aumento da probabilidade de choque e coalescência entre gotas.

Em outras palavras, o AC atua menos por transporte líquido da gota até o eletrodo e mais por **estimular interação gota-gota** e por fragilizar a barreira interfacial que mantém a emulsão estável.  

### 3.3 Consequência prática
A distinção AC/DC é importante porque a resposta da emulsão depende não só da intensidade do campo, mas também do **modo de aplicação**, da **frequência**, da **forma de onda**, da **condutividade do óleo** e da **estabilidade do filme interfacial**. Isso explica por que diferentes arquiteturas de tratadores eletrostáticos podem responder melhor a diferentes petróleos.  

**Rastreabilidade da seção:** `petroles-004c2afadba7ea17c7dd7908:pNone:1817120.0-1817164.0`, `petroles-004c2afadba7ea17c7dd7908:pNone:1817165.0-1817206.0`

## 4. Forças atuantes nas gotas e variáveis de projeto relevantes
As fontes indicam que, sobre uma gota de água dispersa em óleo e sujeita a campo elétrico, atuam simultaneamente:

- força eletrostática;
- força dipolo-dipolo;
- força gravitacional;
- força viscosa/arraste hidráulico.

### 4.1 Interação dipolo-dipolo
A força de atração dipolo-dipolo foi descrita na fonte como função de:

- raios das gotas (`R1`, `R2`);
- distância entre centros das gotas (`S`);
- constante dielétrica da fase contínua (`K`);
- gradiente de tensão aplicado (`E`);
- ângulo de alinhamento em relação às linhas de campo.

Mesmo com a equação parcialmente ilegível, a interpretação fornecida no texto é clara:

- a interação **aumenta** com o aumento do raio das gotas;
- a interação **aumenta rapidamente** com o aumento do gradiente de tensão;
- a interação **decresce rapidamente** com o aumento da distância entre gotas.

Isso é compatível com a prática: uma vez iniciada a coalescência e aumentados os diâmetros, o próprio processo tende a se autoacelerar localmente, porque gotas maiores interagem mais fortemente e sedimentam mais rápido.  

### 4.2 Gradiente de tensão e intensidade do campo
As fontes registram que o potencial elétrico empregado depende de:

- características dielétricas da fase óleo;
- natureza da película adsorvida na gota;
- distância entre eletrodos.

O potencial é usualmente expresso em **volts por polegada linear**. Entretanto, os valores numéricos da faixa usual foram suprimidos no material de origem, portanto não devem ser reconstruídos.  

### 4.3 Limite superior: gradiente crítico de ruptura
O material também afirma que, embora maior gradiente de tensão acelere a coalescência, existe um **valor crítico** acima do qual a gota pode sofrer deformação excessiva e se romper, gerando gotas menores e mais difíceis de remover. A expressão do gradiente crítico `Ec` foi associada a:

- tensão interfacial óleo-água;
- raio da gota;
- constante dielétrica da fase contínua.

A implicação operacional é decisiva: **nem sempre aumentar a tensão melhora a separação**. Existe uma faixa útil entre energia insuficiente para coalescer e energia excessiva que induz fragmentação.  

### 4.4 Consumo de energia
Uma estimativa de potência mínima requerida para o sistema elétrico foi apresentada como função de:

- gradiente de tensão `E` em **V/cm**;
- condutividade específica `C` em **mho/cm**;
- área de eletrodos `A` em **cm²**;
- distância entre eletrodos `L` em **cm**.

A forma exata da equação está corrompida na fonte, mas a mensagem técnica permanece: o projeto elétrico do tratador e do transformador depende diretamente do campo requerido, da condutividade do meio e da geometria eletrodo-espaçamento.  

**Rastreabilidade da seção:** `petroles-004c2afadba7ea17c7dd7908:pNone:1817120.0-1817164.0`, `petroles-004c2afadba7ea17c7dd7908:pNone:1817165.0-1817206.0`

## 5. Da coalescência à separação gravitacional: por que o aumento do diâmetro importa
O objetivo do campo elétrico não é “separar” diretamente toda a água por si só, mas **transformar uma dispersão de gotas pequenas e estáveis em uma dispersão de gotas maiores**, que então podem ser segregadas por gravidade.  

As fontes associam essa etapa final à lei de Stokes e à velocidade terminal da gota. Em termos qualitativos:

- quanto **maior o diâmetro** da gota, maior a velocidade terminal;
- quanto **maior a diferença de densidade** entre água e óleo, mais fácil a sedimentação;
- quanto **maior a viscosidade do óleo**, mais lenta a separação.

Há um ponto importante: se a gota coalescida não atinge um diâmetro suficientemente grande, a sedimentação continua lenta; em gotas muito pequenas, o movimento browniano pode se tornar relevante e a separação gravitacional fica muito difícil.  

Por isso, uma desidratação eficiente depende de duas etapas encadeadas:

1. **coalescer** gotas pequenas até um tamanho adequado;
2. **dar tempo e condições hidráulicas** para que essas gotas sedimentem sem serem re-dispersas.

Em óleos pesados, a dificuldade aumenta porque:

- a viscosidade é alta;
- a diferença de densidade óleo-água é menor em termos práticos de separação;
- há mais tendência à estabilização interfacial por emulsificantes naturais.

**Rastreabilidade da seção:** `petroles-004c2afadba7ea17c7dd7908:pNone:4420063.0-4420096.0`, `petroles-004c2afadba7ea17c7dd7908:pNone:1817165.0-1817206.0`

## 6. Influência das propriedades do óleo, da água e da interface
A eficiência da coalescência eletrostática não depende apenas do equipamento; depende fortemente da natureza da emulsão.

### 6.1 Viscosidade e densidade
Óleos mais pesados tendem a formar emulsões mais estáveis por três razões destacadas nas fontes:

- **alta viscosidade do óleo**, que reduz a mobilidade das gotas;
- **pequena diferença de densidade em relação à água**, que piora a sedimentação;
- **presença de emulsificantes naturais**, que se acumulam na interface água-óleo.

### 6.2 Tamanho inicial das gotas
O tamanho das gotas na emulsão A/O depende, segundo o material, de fatores como:

- tensão interfacial;
- taxa de cisalhamento;
- natureza dos agentes emulsificantes;
- presença de sólidos;
- propriedades do óleo e da água.

Na prática, condições severas a montante do tratador podem produzir dispersões finas demais para que o campo elétrico, sozinho, compense totalmente o dano gerado.  

### 6.3 Película interfacial e tensoativos
A coalescência só se consolida se o filme interfacial for enfraquecido ou drenado. As fontes atribuem ao campo elétrico, sobretudo em AC, uma contribuição para **distorcer ou enfraquecer o filme**. Além disso, aditivos químicos desemulsificantes e temperatura adequada também reduzem a estabilidade da emulsão, deslocando surfactantes naturais e alterando a tensão interfacial.  

### 6.4 Condutividade do óleo e salmoura dispersa
O material informa que petróleos mais pesados tendem a ser mais condutivos, associando isso principalmente à presença de salmoura e de metais pesados ligados a frações mais pesadas, especialmente asfaltenos e resinas. Em termos práticos:

- maior condutividade favorece maior decaimento de tensão aplicada ao sistema;
- se esse decaimento for grande, o campo efetivo sobre as gotas pode cair abaixo do necessário para coalescência.

### 6.5 Temperatura
A temperatura tem efeito duplo:

**Vantagem:**
- reduz viscosidade e pode facilitar separação e desestabilização da emulsão.

**Desvantagens destacadas nas fontes:**
- aumenta a condutividade do meio, elevando o consumo elétrico e podendo intensificar decaimento de tensão;
- aumenta a solubilidade da água no petróleo, de modo que nem toda a água residual pode ser removida como gotículas livres, porque parte permanece molecularmente dissolvida.

A conclusão prática é que aquecer “além do necessário” não é automaticamente benéfico.  

**Rastreabilidade da seção:** `petroles-004c2afadba7ea17c7dd7908:pNone:1817056.0-1817119.0`, `petroles-004c2afadba7ea17c7dd7908:pNone:1817235.0-1817274.0`, `petroles-004c2afadba7ea17c7dd7908:pNone:4420063.0-4420096.0`

## 7. Frequência, tensão mínima, tensão máxima e forma de onda
As fontes destacam que a resposta da emulsão ao campo elétrico não depende apenas do valor instantâneo de tensão, mas da forma como essa energia é entregue ao sistema.

### 7.1 Tensão mínima (threshold voltage)
A chamada **tensão mínima** ou *threshold voltage* é apresentada como o patamar mínimo necessário para iniciar coalescência efetiva. A interpretação experimental descrita é:

- abaixo desse patamar, a energia eletrostática não é suficiente para carregar/energizar adequadamente as gotas de água;
- acima desse patamar, há indício de que as gotas passam a responder eletricamente, ocorrendo crescimento e coalescência.

A fonte também observa que operar apenas pouco acima da tensão mínima pode favorecer crescimento de gotas já mobilizadas, mas não necessariamente trata de forma eficiente as gotas menores mais difíceis de coalescer.  

### 7.2 Tensão máxima
A **tensão máxima** tem papel de atingir e energizar as menores gotas, ampliando a fração de água efetivamente afetada pelo campo. Contudo, existe limite superior prático: se a tensão se aproxima ou supera o nível crítico de ruptura, gotas que já atingiram diâmetro favorável à sedimentação podem voltar a se fragmentar.  

### 7.3 Frequência
Segundo a fonte, em óleos de alta condutividade a frequência primária pode ser aumentada para reduzir o decaimento de tensão e elevar a energia efetivamente entregue ao processo. Ou seja:

- **maior condutividade do óleo** → maior tendência a decaimento de tensão;
- **frequência mais alta** pode mitigar esse decaimento.

Por outro lado, a mesma fonte afirma que a frequência deve ser mantida **abaixo da frequência natural das gotículas**, para evitar destruição das gotas e perda de eficiência de coalescência. Isso sugere um problema de otimização com dois limites:

- limite inferior: evitar decaimento excessivo da tensão efetiva;
- limite superior: evitar excitação desfavorável e ruptura das gotas.

### 7.4 Forma de onda
Na descrição do tratador Dual Frequency, o campo pode ser ajustado quanto a:

- tensão máxima;
- tensão mínima;
- frequência;
- padrão cíclico/forma de onda.

A ideia técnica é adaptar o campo às propriedades do petróleo para maximizar a coalescência sem induzir instabilidade elétrica ou quebra de gotas. Ainda que a fonte cite formas de onda específicas em equipamento proprietário, o conceito geral aplicável é que **o condicionamento temporal do campo importa** para o desempenho da desidratação.  

**Rastreabilidade da seção:** `petroles-004c2afadba7ea17c7dd7908:pNone:1817208.0-1817254.0`, `petroles-004c2afadba7ea17c7dd7908:pNone:1817235.0-1817274.0`

## 8. Relação entre configuração do tratador e os mecanismos de coalescência
Embora o foco aqui seja o mecanismo, a configuração hidráulica do tratador altera o modo como as gotas encontram o campo e o risco de instabilidade elétrica.

### 8.1 Tratadores convencionais de baixa velocidade
Nos tratadores de baixa velocidade descritos na fonte, a carga entra abaixo da região de eletrodos, próxima da interface água-óleo. Nessa configuração:

- parte das gotas maiores coalesce em região de campo mais fraco, antes de alcançar a zona principal entre eletrodos;
- apenas gotas menores seguem para a região de campo mais intenso;
- o arranjo tende a tolerar melhor variações no teor de água de entrada.

Isso é coerente com operação offshore variável, em que mudanças de vazão e BS&W podem ocorrer.  

### 8.2 Tratadores convencionais de alta velocidade
Neles, a carga entra diretamente na região entre eletrodos. Isso favorece coalescência rápida porque aumenta a população de gotas sob campo intenso, mas também torna o sistema mais sensível a:

- teor máximo de água na carga;
- presença de água livre;
- tamanho das gotas;
- desestabilização elétrica e risco de curto-circuito.

### 8.3 Dual Polarity e Dual Frequency
As fontes descrevem o **Dual Polarity** como combinação de campo AC em uma região e DC em outra, explorando simultaneamente mecanismos de polarização/distorção e eletroforese. Já o **Dual Frequency** é apresentado como evolução com controle de amplitude, frequência e forma de onda, permitindo otimização para cada petróleo.  

Do ponto de vista dos mecanismos, essas tecnologias procuram ajustar melhor:

- a energização das gotas menores;
- o crescimento sustentado das gotas já ativadas;
- a minimização de ruptura e de instabilidade do campo;
- a adaptação a óleos com diferentes condutividades e comportamentos interfaciais.

**Rastreabilidade da seção:** `petroles-004c2afadba7ea17c7dd7908:pNone:1817165.0-1817206.0`, `petroles-004c2afadba7ea17c7dd7908:pNone:1817208.0-1817254.0`

## 9. Leitura operacional e diagnóstico de baixo desempenho
Com base nas relações descritas nas fontes, alguns mecanismos de perda de eficiência podem ser interpretados assim:

### 9.1 Gotas continuam pequenas e não sedimentam
Causas prováveis:

- campo abaixo da tensão mínima efetiva;
- excesso de cisalhamento a montante, formando gotas muito finas;
- emulsão muito estável por emulsificantes naturais, sólidos ou propriedades do cru;
- tempo de residência insuficiente para coalescência e sedimentação.

### 9.2 Coalescência ocorre, mas o desempenho final ainda é ruim
Causas prováveis:

- gotas crescem, mas não atingem diâmetro suficiente para sedimentação efetiva;
- viscosidade ainda elevada;
- diferença de densidade insuficiente em óleo pesado;
- re-dispersão hidráulica interna ou em válvulas/etapas subsequentes.

### 9.3 Corrente elétrica se eleva e o campo fica instável
Causas prováveis segundo a lógica das fontes:

- presença elevada de água dispersa ou água livre na zona de eletrodos;
- condutividade elevada do sistema, com forte decaimento de tensão;
- configuração de alta velocidade operando fora da faixa tolerável;
- risco de curto-circuito por desestabilização do sistema elétrico.

### 9.4 Aumento de tensão piora o resultado
Possível explicação:

- o sistema ultrapassou a faixa ótima e se aproximou da condição de ruptura de gotas, produzindo gotas menores e mais difíceis de remover.

### 9.5 Aumento de temperatura não melhora proporcionalmente a desidratação
Possível explicação:

- embora a viscosidade caia, a condutividade aumenta, o consumo elétrico cresce e parte da água permanece dissolvida no petróleo; portanto, aquecimento excessivo pode ter retorno marginal ou até desfavorável.  

**Rastreabilidade da seção:** `petroles-004c2afadba7ea17c7dd7908:pNone:1817165.0-1817206.0`, `petroles-004c2afadba7ea17c7dd7908:pNone:1817208.0-1817254.0`, `petroles-004c2afadba7ea17c7dd7908:pNone:1817235.0-1817274.0`, `petroles-004c2afadba7ea17c7dd7908:pNone:4420063.0-4420096.0`

## 10. Síntese técnica
A coalescência eletrostática em tratadores de óleo pode ser resumida como a combinação de três etapas físicas principais:

1. **polarizar e deformar gotas de água dispersas em óleo**;
2. **promover aproximação, choque, drenagem do filme interfacial e coalescência**;
3. **produzir gotas grandes o suficiente para sedimentar por gravidade**.

O sucesso do processo depende do equilíbrio entre:

- intensidade do campo elétrico;
- frequência e forma de onda;
- geometria/região de aplicação do campo;
- condutividade do meio;
- viscosidade do óleo;
- estabilidade interfacial da emulsão;
- condições hidráulicas e de residência.

Portanto, o tratador eletrostático não deve ser entendido como um equipamento de “alta tensão” isoladamente, mas como um sistema eletro-hidráulico de coalescência cuja eficiência resulta do ajuste fino entre fenômenos elétricos, interfaciais e gravitacionais.  

**Rastreabilidade da seção:** `petroles-004c2afadba7ea17c7dd7908:pNone:1817056.0-1817119.0`, `petroles-004c2afadba7ea17c7dd7908:pNone:1817120.0-1817164.0`, `petroles-004c2afadba7ea17c7dd7908:pNone:1817165.0-1817206.0`, `petroles-004c2afadba7ea17c7dd7908:pNone:1817208.0-1817254.0`, `petroles-004c2afadba7ea17c7dd7908:pNone:1817235.0-1817274.0`, `petroles-004c2afadba7ea17c7dd7908:pNone:4420063.0-4420096.0`