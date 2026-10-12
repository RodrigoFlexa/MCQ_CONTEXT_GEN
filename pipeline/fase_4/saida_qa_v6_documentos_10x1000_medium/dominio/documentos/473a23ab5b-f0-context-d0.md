# Fundamentos e variáveis de separação em separadores trifásicos

## 1. Papel do separador trifásico no processamento primário offshore

Em FPSOs e outras unidades offshore, o separador trifásico é um dos primeiros equipamentos do processamento primário. Sua função é promover a separação das fases gás, óleo e água provenientes dos poços, ao mesmo tempo em que amortece flutuações da corrente de alimentação, inclusive golfadas (*slugs*), entregando correntes mais estáveis aos sistemas a jusante. Na prática, a separação não é perfeita; o objetivo operacional é manter dentro de limites toleráveis:

- líquido arrastado no gás;
- água arrastada no óleo, usualmente acompanhada pelo indicador BS&W;
- óleo arrastado na água, usualmente acompanhado por TOG.

A importância desse desempenho é sistêmica: a qualidade da separação afeta a especificação do óleo exportado, a proteção do sistema de compressão de gás e a carga do tratamento de água produzida. Em plantas mais complexas, o separador interage com aquecimento, injeção química, compressão de gás, tratamento de óleo e tratamento da água produzida. Em função da pressão do sistema e das características do fluido, podem ser empregados vários estágios de separação para maximizar a recuperação de óleo e acomodar poços com diferentes pressões de escoamento.  
**Fontes da seção:** `regis-18b929daeb4c903e869439dc:pNone:2475.0-2526.0`, `petroles-004c2afadba7ea17c7dd7908:pNone:215508.0-215548.0`, `regis-ef7d62eda3748119ba3e9e9e:pNone:976.0-1181.0`, `regis-e2367eb364fd1d2b2ffe0107:pNone:17948.0-18199.0`

## 2. Princípios físicos da separação gás-óleo-água

Os trechos apontam quatro mecanismos principais no interior de vasos separadores gravitacionais:

1. **Ação da gravidade e diferença de densidades**: promovem a decantação da fase mais pesada e a segregação das fases imiscíveis.
2. **Separação inercial**: mudanças bruscas de velocidade e direção, especialmente na entrada, fazem o gás desprender-se do líquido pela diferença de inércia entre as fases.
3. **Aglutinação/coalescência de gotículas**: contato com superfícies ou meios porosos favorece a união de gotículas dispersas em gotas maiores, que se separam mais facilmente.
4. **Força centrífuga**: em dispositivos que impõem movimento giratório, as fases sofrem separação adicional pela diferença de densidade.

Nos separadores trifásicos, a separação líquido-líquido depende fortemente da diferença de densidades entre óleo e água, da viscosidade do óleo, do tamanho das gotas dispersas e do tempo disponível para coalescência e decantação. Os textos também associam a concepção e o dimensionamento desses equipamentos ao princípio de sedimentação/decantação, com referência à Lei de Stokes como base conceitual para o comportamento de partículas ou massas fluidas em meio contínuo.  
**Fontes da seção:** `regis-18b929daeb4c903e869439dc:pNone:2475.0-2526.0`, `regis-282132e81add5278ef714ccc:pNone:2076.0-2284.0`, `regis-ef7d62eda3748119ba3e9e9e:pNone:976.0-1181.0`

## 3. Seções internas e sua relação com o tempo de residência

Os separadores descritos nas fontes podem ser entendidos em quatro seções funcionais:

### 3.1 Seção de separação primária
Na entrada, o fluido choca-se com defletores, difusores ou dispositivos de redirecionamento de escoamento. O objetivo é dissipar o *momentum* da mistura, reduzir turbulência local e remover rapidamente a maior parte do líquido e das gotículas maiores. Essa etapa é crítica em correntes com golfadas, porque a capacidade de amortecimento do separador depende de sua habilidade de receber uma carga variável sem perder a estabilidade das interfaces.  

### 3.2 Seção de acumulação/coleta de líquido
Depois da separação primária, o líquido permanece retido por um período suficiente para liberação de bolhas de gás e para a formação/estabilização das camadas líquidas. As fontes citam valores típicos de retenção de aproximadamente **3 a 4 minutos** e, em outro trecho, **cerca de 5 minutos**, indicando que o valor é contextual e depende do serviço e do fluido. Em separadores trifásicos, essa retenção também suporta a decantação de água livre e a evolução da interface óleo-água.

### 3.3 Seção de separação secundária
Nessa região, gotículas menores ainda arrastadas pelo gás são separadas, principalmente por gravidade. A eficiência é fortemente degradada por alta turbulência no espaço gasoso.

### 3.4 Seção aglutinadora / extrator de névoa
O gás passa por meios porosos, almofadas de tela, aletas metálicas, placas pouco espaçadas ou outro extrator de névoa (*demister*), que promovem coalescência e remoção das gotas residuais. Se o gás sair dessa seção com velocidade excessiva ou se o interno estiver obstruído, aumenta o risco de arraste de líquido.

### 3.5 Particularidades da separação trifásica
Os trechos citam, para configuração trifásica horizontal, a existência de duas câmaras principais separadas por barragem: uma câmara de separação e uma câmara de óleo. Também são mencionados elementos como condutor de líquido, chaminé/condutor de gás para equalização de pressão e espalhador abaixo da interface óleo-água, de modo a reduzir perturbações na interface e permitir escoamento em contracorrente entre água descendente e óleo ascendente. Esses internos existem justamente para transformar volume geométrico em **tempo de residência efetivo**, e não apenas em inventário bruto.  
**Fontes da seção:** `regis-18b929daeb4c903e869439dc:pNone:2475.0-2526.0`, `regis-e2367eb364fd1d2b2ffe0107:pNone:17948.0-18199.0`, `regis-f96d8b534287b9dfd7921821:pNone:4242.0-4444.0`, `regis-282132e81add5278ef714ccc:pNone:2076.0-2284.0`

## 4. Variáveis de processo que mais afetam a separação

As fontes convergem em quatro variáveis centrais para a qualidade da separação: **tempo de residência, pressão, temperatura e dosagem de produtos químicos**. Em ambiente offshore, essas variáveis são continuamente perturbadas por oscilações de vazão e de composição da mistura produzida.  
**Fontes da seção:** `regis-18b929daeb4c903e869439dc:pNone:2475.0-2526.0`, `petroles-004c2afadba7ea17c7dd7908:pNone:215508.0-215548.0`

### 4.1 Vazão de alimentação, flutuações e golfadas
A grande variação de vazão, pressão e razão gás/óleo/água é destacada como característica dinâmica essencial de plantas offshore. Quando a alimentação oscila:

- o inventário do vaso varia rapidamente;
- o tempo de residência efetivo muda;
- a pressão interna tende a oscilar;
- a interface óleo-água pode se deslocar e perder estabilidade;
- a qualidade do gás, do óleo e da água se deteriora.

Por isso, o separador trifásico também cumpre papel de **tanque pulmão** (*surge tank*), recebendo uma vazão flutuante e entregando correntes mais estáveis. Se a vazão instantânea supera a capacidade de dissipação de energia e retenção do vaso, cresce o risco de:

- **carryover** de líquido para a saída de gás;
- gás remanescente nas fases líquidas;
- arraste cruzado entre óleo e água;
- perda de desempenho das malhas de controle de nível e pressão.

### 4.2 Pressão de separação
A pressão de operação é uma das variáveis mais importantes. Os trechos indicam que:

- existe uma **pressão ótima de separação**, dependente do sistema e do óleo processado;
- **redução da pressão** aumenta o volume de gás liberado do óleo;
- com mais gás ocupando o mesmo espaço do vaso, aumenta a velocidade do gás no interior do separador;
- esse aumento de velocidade favorece o arraste de gotículas de óleo na corrente de gás;
- para evitar esse efeito, pode ser necessário reduzir a vazão de entrada, o que diminui a capacidade efetiva do separador;
- no sentido oposto, **aumento da pressão** permite maior capacidade do separador, embora reduza o volume de gás liberado do óleo naquela etapa.

Do ponto de vista prático, a pressão afeta simultaneamente: liberação de gás dissolvido, carga volumétrica da seção gasosa, desempenho do *demister* e carga imposta ao sistema de compressão de gás. Assim, operar em pressão mais baixa não é automaticamente melhor para separar; pode melhorar a liberação de gás do óleo, mas piorar o arraste de líquido no gás e reduzir capacidade.

### 4.3 Temperatura de separação
A temperatura ótima depende das características do óleo. As fontes associam temperaturas maiores a:

- redução da viscosidade do óleo, favorecendo escoamento e decantação;
- redução da densidade do óleo e, em geral, aumento da diferença em relação à água, facilitando sedimentação/separação líquido-líquido;
- mitigação da formação de espuma na separação gás-óleo;
- facilitação da quebra de emulsões em conjunto com outros métodos.

Entretanto, os mesmos trechos alertam que o aumento de temperatura pode produzir, sobre a vazão/carga de gás, efeito semelhante ao da redução da pressão de separação. Em termos operacionais, isso significa que aquecer pode ajudar a coalescência e a separação óleo-água, mas também aumentar a carga de gás no espaço superior e exigir mais cuidado com velocidade de gás, *carryover* e capacidade do vaso.

### 4.4 Composição dos fluidos e proporções das fases
A escolha de arranjo, etapas de separação e condições operacionais depende de:

- composição dos hidrocarbonetos;
- proporções de óleo, gás e água produzidos;
- razão gás/óleo;
- presença de água livre e de água emulsionada;
- tendência a espuma, parafina, areia e sedimentos.

Fluidos com alta viscosidade, maior teor de emulsão ou elevada razão gás/óleo impõem necessidades diferentes de temperatura, internos e estabilidade operacional.

### 4.5 Produtos químicos
Os trechos mencionam injeção de desemulsificantes, antiespumantes, inibidores de incrustação, inibidores de corrosão e outros químicos. No contexto da separação trifásica, esses produtos podem:

- acelerar coalescência;
- ajudar a romper emulsões;
- reduzir espuma;
- proteger integridade dos internos e da tubulação.

A dosagem, porém, é tratada como variável de qualidade: oscilações de vazão e composição podem tornar a dosagem efetiva inadequada, mesmo se a vazão nominal de químico não mudar.  
**Fontes da subseção 4:** `regis-18b929daeb4c903e869439dc:pNone:2475.0-2526.0`, `petroles-004c2afadba7ea17c7dd7908:pNone:215508.0-215548.0`, `regis-282132e81add5278ef714ccc:pNone:2076.0-2284.0`, `regis-e2367eb364fd1d2b2ffe0107:pNone:17948.0-18199.0`, `regis-ef7d62eda3748119ba3e9e9e:pNone:976.0-1181.0`

## 5. Tempo de residência: conceito operacional e perda de efetividade

Nos trechos fornecidos, o tempo de residência aparece como variável-chave da qualidade de separação. Na prática, o que importa não é apenas o volume nominal do separador, mas o **tempo de residência efetivo** disponível para:

- desprendimento de gás do líquido;
- coalescência de gotas de água no óleo e de óleo na água;
- sedimentação/decantação;
- estabilização das interfaces.

Esse tempo efetivo diminui quando há:

- aumento de vazão líquida;
- slugs que ocupam rapidamente a seção de separação;
- espuma ocupando parte do volume útil;
- acúmulo de emulsão na interface óleo-água;
- areia e sedimentos depositados no fundo;
- parafina/incrustações obstruindo internos e alterando o escoamento.

Portanto, dois vasos com o mesmo volume geométrico podem apresentar desempenho muito diferente se um deles estiver com espuma persistente, camada de emulsão espessa, acúmulo de sólidos ou internos degradados. Essa distinção é central em diagnóstico operacional.  
**Fontes da seção:** `regis-18b929daeb4c903e869439dc:pNone:2475.0-2526.0`, `petroles-004c2afadba7ea17c7dd7908:pNone:215508.0-215548.0`, `regis-282132e81add5278ef714ccc:pNone:2186.0-2371.0`

## 6. Níveis, interface óleo-água e pressão: por que o controle afeta a separação

As principais variáveis controladas associadas ao inventário do separador trifásico são:

- pressão do gás;
- nível total e/ou nível de água na câmara de separação;
- nível de óleo na câmara de óleo.

As fontes descrevem o seguinte arranjo funcional:

- o **controle de pressão** atua sobre a vazão de saída de gás;
- o **controle de nível de óleo** atua sobre a vazão de saída de óleo;
- o **controle de nível de água** atua sobre a vazão de saída de água;
- quando a alimentação é regular, é possível manter mais estáveis os níveis e a velocidade de circulação de gás, favorecendo maior eficiência de separação.

O impacto operacional é direto. Segundo os trechos, elevação de nível pode:

- pressurizar o sistema;
- aumentar o risco de arraste de óleo para a linha de gás;
- causar passagem de água para a linha de óleo;
- aproximar o vaso de seus limites mecânicos.

Em separadores trifásicos, controlar apenas nível total não é suficiente; a **interface óleo-água** precisa permanecer em posição compatível com os internos e com os bocais de retirada. Interface instável ou mal controlada tende a aumentar o arraste cruzado entre fases líquidas. As malhas de controle, portanto, não são apenas instrumentos de inventário: elas são parte do desempenho de separação. Seu objetivo maior, conforme os textos, é reduzir a propagação de oscilações ao longo da planta e limitar o impacto dessas oscilações sobre as variáveis de qualidade.  
**Fontes da seção:** `petroles-004c2afadba7ea17c7dd7908:pNone:215508.0-215548.0`, `regis-e2367eb364fd1d2b2ffe0107:pNone:17948.0-18199.0`, `regis-18b929daeb4c903e869439dc:pNone:2475.0-2526.0`

## 7. Efeito dos internos no desempenho frente às variáveis de processo

O desempenho do separador depende dos seus internos e de como eles respondem às perturbações do processo.

### 7.1 Dispositivos de entrada
Cabeças de serviço, defletores, difusores e separadores envolventes dissipam a energia de entrada e controlam o *momentum* da mistura. Se a alimentação chega com energia excessiva ou se esses dispositivos estão danificados/obstruídos, aumenta a turbulência e cai a eficiência das etapas seguintes.

### 7.2 Barragens, condutores e espalhadores
Na separação trifásica, barragem, condutor de líquido, chaminé/condutor de gás e espalhador abaixo da interface servem para não perturbar a interface óleo-água, equalizar pressões entre regiões do vaso e criar um padrão de escoamento mais favorável à decantação.

### 7.3 Placas coalescedoras e região de coalescência
Esses elementos ampliam área de contato e promovem união de gotas dispersas. Seu benefício é particularmente importante quando o fluido tem tendência à emulsão ou quando o tamanho inicial das gotas é pequeno.

### 7.4 Extrator de névoa (*demister*)
É o último recurso contra o arraste de líquido no gás. Se a vazão de gás cresce por queda de pressão, aumento de temperatura ou slugging, o *demister* pode ser sobrecarregado. Além disso, parafina e sólidos podem obstruí-lo e reduzir sua eficiência.

### 7.5 Quebradores de espuma, ondas e vórtice
Os trechos citam quebradores de espuma, ondas e vórtice como internos típicos de separadores de produção. Eles ajudam a preservar a estabilidade do escoamento e da interface, reduzindo re-entrainment e perdas de volume útil por espuma.  
**Fontes da seção:** `regis-e2367eb364fd1d2b2ffe0107:pNone:17948.0-18199.0`, `regis-f96d8b534287b9dfd7921821:pNone:4242.0-4444.0`, `regis-ef7d62eda3748119ba3e9e9e:pNone:976.0-1181.0`, `regis-282132e81add5278ef714ccc:pNone:2076.0-2284.0`

## 8. Principais degradações de desempenho e sua relação com as variáveis operacionais

### 8.1 Formação de espuma
A espuma é associada às características físico-químicas do óleo, às impurezas e à queda de pressão imposta à mistura. Seus efeitos incluem:

- ocupação de volume que deveria estar disponível para retenção de líquido;
- dificuldade de medição/controle de nível;
- aumento do arraste para a saída de gás ou para o óleo desgaseificado;
- redução da área livre de escoamento do gás.

Os trechos indicam como medidas de mitigação: dispositivo interno para remoção/quebra de espuma, superfície/tempo de coalescência adequados, uso de antiespumante e, em alguns casos, aquecimento.

### 8.2 Emulsões na interface óleo-água
A emulsão acumulada na interface reduz o espaço útil do vaso e o tempo de retenção efetivo. Também desorganiza o controle de nível/interface. Quando a emulsão é persistente, a separação líquido-líquido exige mais tempo, calor e/ou química. Se esse tempo não está disponível, aumenta o teor de água no óleo e o teor de óleo na água.

### 8.3 Areia e sedimentos
Areia e sedimentos causam erosão de válvulas, obstrução de internos e perda de volume útil no fundo do vaso. O acúmulo reduz o tempo de residência do líquido. Se o separador não possuir remoção adequada por drenos ou outro arranjo, pode ser necessário interromper a produção para limpeza.

### 8.4 Parafinas e depósitos
Placas coalescedoras e extratores de névoa são particularmente suscetíveis a obstrução por parafina. Os trechos citam a conveniência de prever acessos e bocais para limpeza com solvente ou vapor. Baixa temperatura em relação à tendência de cristalização agrava o problema.

### 8.5 Arraste de óleo pelo gás e outros arrastes cruzados
As fontes associam o arraste de óleo pelo gás a condições como:

- nível de líquido elevado;
- formação de espuma;
- saída de líquido obstruída por areia ou parafina;
- subdimensionamento do separador para a vazão de entrada;
- aumento da velocidade do gás por redução de pressão ou aumento de temperatura.

De forma análoga, água no óleo e óleo na água tendem a crescer quando a interface está instável, o tempo de residência é insuficiente ou a emulsão ocupa volume excessivo.  
**Fontes da seção:** `petroles-004c2afadba7ea17c7dd7908:pNone:215508.0-215548.0`, `regis-282132e81add5278ef714ccc:pNone:2186.0-2371.0`, `regis-f96d8b534287b9dfd7921821:pNone:4242.0-4444.0`

## 9. Configuração horizontal ou vertical: implicações para a separação

As fontes indicam que separadores horizontais são amplamente usados offshore e, em geral, oferecem maior área interfacial, o que favorece separação gás-líquido e líquido-líquido, especialmente em serviços com espumas, emulsões e altas razões gás/óleo. Já os verticais facilitam deposição localizada de sólidos no fundo, o que simplifica a remoção de areia e sedimentos, além de ocuparem menor área de planta.

Para o foco desta faceta, a consequência mais importante é que a geometria altera:

- a área interfacial disponível;
- a sensibilidade à turbulência e ao *momentum* de entrada;
- a facilidade de remoção de sólidos;
- a forma como o inventário líquido se distribui e, portanto, o tempo de residência efetivo.

Os trechos fornecidos não são plenamente consistentes quanto à comparação entre horizontal e vertical para absorção de golfadas, então essa comparação deve ser tratada com cautela.  
**Fontes da seção:** `regis-18b929daeb4c903e869439dc:pNone:2475.0-2526.0`, `regis-282132e81add5278ef714ccc:pNone:2076.0-2284.0`, `regis-f96d8b534287b9dfd7921821:pNone:4242.0-4444.0`

## 10. Consequências a jusante e leitura operacional de desempenho

O desempenho do separador trifásico deve ser interpretado pela qualidade das três correntes de saída e pelo impacto a jusante:

- **Gás**: arraste de líquido prejudica compressores, linhas e sistemas de condicionamento;
- **Óleo**: aumento de BS&W e sais desloca carga para tratadores, aquecimento e desidratação;
- **Água produzida**: aumento de óleo disperso eleva a carga sobre skimmers, hidrociclones e flotadores.

Os trechos citam especificações históricas de referência, como limites de BS&W no óleo e TOG na água produzida, mas o ponto essencial aqui é conceitual: baixa eficiência de separação primária transfere instabilidade e sobrecarga para os sistemas subsequentes.

Do ponto de vista de diagnóstico, alguns padrões úteis são:

- **gás úmido ou com líquido**: verificar pressão muito baixa, temperatura elevada, slugging, nível alto, espuma, *demister* obstruído ou interno de entrada degradado;
- **óleo com excesso de água**: verificar tempo de residência insuficiente, emulsão acumulada, temperatura inadequada, química insuficiente e interface instável;
- **água com excesso de óleo**: verificar arraste cruzado por turbulência, emulsão persistente, controle deficiente da interface e queda do tempo de residência efetivo;
- **oscilação generalizada de níveis e pressão**: verificar variabilidade da alimentação, sintonia das malhas e capacidade de amortecimento do vaso.

Esses diagnósticos não substituem balanço de processo e inspeção, mas organizam a relação causal entre variável de processo, mecanismo físico e desvio de qualidade.  
**Fontes da seção:** `petroles-004c2afadba7ea17c7dd7908:pNone:215508.0-215548.0`, `regis-ef7d62eda3748119ba3e9e9e:pNone:976.0-1181.0`, `regis-18b929daeb4c903e869439dc:pNone:2475.0-2526.0`

## 11. Síntese técnica

Para avaliar como variáveis de processo afetam a separação gás-óleo-água em separadores trifásicos, o raciocínio central é:

1. **A separação depende de mecanismos gravitacionais, inerciais, centrífugos e de coalescência.**
2. **O vaso só performa bem se houver tempo de residência efetivo suficiente e baixa turbulência nas regiões críticas.**
3. **Pressão e temperatura alteram simultaneamente a liberação de gás, a viscosidade do óleo, a tendência à espuma e a capacidade do vaso.**
4. **Vazão, slugging e composição do fluido perturbam níveis, interfaces e carga volumétrica de gás.**
5. **Internos e malhas de controle convertem o volume disponível em desempenho real de separação.**
6. **Espuma, emulsão, areia e parafina reduzem esse desempenho mesmo sem mudança aparente de volume geométrico.**
7. **A eficiência do separador deve ser julgada pelas especificações das três correntes e pelo efeito nos sistemas a jusante.**

Em termos profissionais, isso significa que a operação de um separador trifásico não pode ser analisada apenas por um valor de nível ou pressão isolado; é necessário interpretar o conjunto formado por vazão, P/T, composição, estabilidade do escoamento, condição dos internos e resposta das malhas de controle.  
**Fontes da seção:** `regis-18b929daeb4c903e869439dc:pNone:2475.0-2526.0`, `petroles-004c2afadba7ea17c7dd7908:pNone:215508.0-215548.0`, `regis-e2367eb364fd1d2b2ffe0107:pNone:17948.0-18199.0`, `regis-282132e81add5278ef714ccc:pNone:2186.0-2371.0`