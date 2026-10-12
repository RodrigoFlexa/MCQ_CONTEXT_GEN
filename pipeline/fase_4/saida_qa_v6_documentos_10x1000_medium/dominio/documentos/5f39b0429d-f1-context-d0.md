# Corrosão e mecanismos de degradação em equipamentos e tubulações

## 1. Premissas técnicas para integridade
Em equipamentos e tubulações de produção e processamento offshore, a degradação por corrosão não depende apenas do material: ela resulta da interação entre **metalurgia**, **meio corrosivo**, **presença de fase aquosa**, **temperatura**, **pressão**, **velocidade de escoamento**, **sólidos**, **micro-organismos** e **estado de tensões** aplicadas ou residuais. Para a gestão de integridade, isso significa que a identificação do mecanismo dominante deve sempre considerar o conjunto **material + fluido + condição operacional + carregamento mecânico**.

Os trechos consultados indicam que, na cadeia de petróleo e gás, são particularmente relevantes como agentes corrosivos o **CO2**, o **H2S**, os **cloretos da água produzida**, os **ácidos orgânicos**, os **polissulfetos** e a presença de **particulados**. Além disso, esforços cíclicos, vibração, ciclos térmicos e tensões residuais de soldagem podem transformar uma corrosão inicialmente controlável em um mecanismo trincante ou acelerado.

**Implicação prática para FPSO/FSO:** a definição de pontos de acompanhamento deve priorizar trechos com água produzida, gases ácidos dissolvidos, sólidos, regiões sujeitas a vibração ou ciclos térmicos, e áreas com tensões residuais significativas, especialmente em juntas soldadas e componentes pressurizados.

*Fontes: [`petroles-4ee4bce16acf674505c8912d:pNone:597640.60-597677.0`, `petroles-4ee4bce16acf674505c8912d:pNone:1128505.0-1128546.0`, `petroles-4ee4bce16acf674505c8912d:pNone:2586128.0-2586171.0`]*

## 2. Formas de ataque relevantes para inspeção e acompanhamento
A classificação morfológica ajuda a reconhecer o dano em campo e a inferir risco:

### 2.1 Corrosão uniforme
É a perda de espessura distribuída ao longo da superfície. Embora seja mais simples de quantificar, continua sendo crítica em tubulações e vasos porque reduz progressivamente a capacidade resistente à pressão.

### 2.2 Corrosão localizada
Inclui formas como:
- **pite**: cavidade com profundidade geralmente maior que o diâmetro;
- **alveolar**: escavações com fundo arredondado e profundidade menor que o diâmetro;
- **por placa**: regiões escavadas mais extensas;
- **em frestas/aeração diferencial**: associada a heterogeneidades de acesso de oxigênio ou eletrólito.

Do ponto de vista de integridade, a corrosão localizada é mais difícil de mensurar e pode causar falhas graves com perda de massa global relativamente pequena. Pites são particularmente perigosos porque funcionam como **concentradores de tensão** e podem nuclear trincas por fadiga.

### 2.3 Corrosão intergranular e transgranular
- **Intergranular**: progride ao longo dos contornos de grão. A quantidade de metal oxidado pode ser pequena, mas as propriedades mecânicas se degradam fortemente e o material pode fissurar em profundidade.
- **Transgranular**: o ataque/trinca atravessa os grãos. Em certos contextos aparece associado à corrosão sob tensão.

### 2.4 Corrosão seletiva
É o ataque preferencial a um dos constituintes da liga, como na **dezincificação** de latões. Em sistemas de troca térmica ou água salgada, a mudança de composição superficial pode comprometer resistência mecânica e vedação.

### 2.5 Corrosão galvânica
Ocorre quando dois metais com potenciais diferentes ficam eletricamente conectados e imersos em eletrólito. O metal menos nobre atua como ânodo e tende a se corroer mais rapidamente. Em arranjos com materiais dissimilares, esse mecanismo deve ser considerado em conexões, reparos, inserções e interfaces metálicas.

*Fontes: [`petroles-4ee4bce16acf674505c8912d:pNone:2324733.0-2324772.0`, `petroles-004c2afadba7ea17c7dd7908:pNone:2731387.0-2731436.0`, `petroles-4ee4bce16acf674505c8912d:pNone:488245.0-488289.0`, `petroles-4ee4bce16acf674505c8912d:pNone:597640.60-597677.0`, `petroles-4ee4bce16acf674505c8912d:pNone:1128505.0-1128546.0`]*

## 3. Mecanismos dominantes em equipamentos e tubulações

### 3.1 Corrosão por CO2
A corrosão por CO2, frequentemente chamada de **sweet corrosion**, é descrita como um dos maiores problemas da indústria do petróleo. Os trechos apontam que ela **só ocorre na presença de uma fase aquosa** em contato com a superfície metálica.

O mecanismo básico envolve:
1. dissolução do CO2 no meio aquoso;
2. hidratação/formação de ácido carbônico;
3. dissociação em bicarbonato e carbonato;
4. reação eletroquímica com o ferro.

Uma reação global simplificada citada é:

- CO2(g) → CO2(aq)
- CO2(aq) + H2O → H2CO3
- H2CO3 ⇌ H+ + HCO3-
- HCO3- ⇌ H+ + CO3^2-
- Fe + CO2 + H2O → FeCO3 + H2

Os fatores destacados como controladores da taxa de corrosão por CO2 em aço carbono incluem:
- química da solução;
- velocidade do fluxo;
- temperatura;
- pressão/pressão parcial de CO2;
- pH.

O produto de corrosão **FeCO3** pode formar película **protetora** ou **não protetora**, dependendo do meio. A formação irregular ou a destruição localizada dessa camada favorece a transição de corrosão mais uniforme para **corrosão localizada**. Portanto, em linhas com água produzida, CO2 dissolvido e variação de regime hidráulico, a simples presença de filme não garante integridade.

**Sinal prático para monitoramento:** trechos com água produzida, variações de temperatura e velocidade, ou tendência à ruptura de filmes de produto de corrosão devem ser acompanhados porque podem migrar rapidamente de perda generalizada para ataque localizado.

*Fontes: [`petroles-004c2afadba7ea17c7dd7908:pNone:2731387.0-2731436.0`, `petroles-4ee4bce16acf674505c8912d:pNone:2586128.0-2586171.0`, `petroles-4ee4bce16acf674505c8912d:pNone:1128505.0-1128546.0`]*

### 3.2 Corrosão por H2S, águas ácidas e danos associados ao hidrogênio
Em meios contendo H2S dissolvido em água, os trechos indicam dissociação em etapas, com geração de espécies contendo hidrogênio e enxofre. A reação do meio sulfídrico com o ferro está associada à formação de sulfetos de ferro na superfície e, principalmente, à geração/absorção de **hidrogênio atômico**, que é crítica para mecanismos fragilizantes.

Aspectos importantes extraídos das fontes:
- a corrosão por H2S em aços carbono pode ser **piteforme**;
- pequenas trincas de fadiga podem existir na base desses pites;
- bactérias redutoras de sulfato podem gerar H2S mesmo em ambiente anaeróbio;
- em ambientes ácidos com H2S, a recombinação do hidrogênio atômico em H2 molecular é retardada, favorecendo a difusão de hidrogênio para o aço.

Os fatores apontados como mais relevantes para danos associados a H2S/ambientes ácidos são:
- pressão parcial ou quantidade dissolvida de H2S;
- pH;
- temperatura;
- contaminantes;
- oxigênio dissolvido, quando aplicável;
- resistência mecânica e microestrutura do material;
- existência de tensões aplicadas ou residuais.

Consequências típicas para integridade:
- pites e perda localizada de espessura;
- **craqueamento induzido por hidrogênio**;
- **trincamento sob tensão por sulfeto**;
- redução de ductilidade e transição para comportamento mais frágil.

**Implicação para FPSO:** equipamentos e tubulações que combinam aço carbono/baixa liga, água, H2S e estado de tensão elevado exigem segregação como regiões de maior criticidade de integridade, sobretudo em juntas soldadas, trechos com histórico de corrosão localizada e componentes submetidos a carregamento mecânico significativo.

*Fontes: [`petroles-004c2afadba7ea17c7dd7908:pNone:2731387.0-2731436.0`, `petroles-004c2afadba7ea17c7dd7908:pNone:2731410.0-2731454.0`, `petroles-4ee4bce16acf674505c8912d:pNone:2586128.0-2586171.0`, `petroles-4ee4bce16acf674505c8912d:pNone:1128505.0-1128546.0`]*

### 3.3 Corrosão microbiologicamente induzida (CMI/MIC)
A biocorrosão é apresentada como um processo eletroquímico causado ou acelerado por micro-organismos. As fontes destacam que ela é relevante em oleodutos, separadores, tanques, instalações de armazenamento e outros sistemas com água e tempo de residência elevado.

Pontos técnicos relevantes:
- bactérias, fungos e algas podem participar, embora bactérias sejam predominantes;
- ocorre formação de **biofilme** na interface sólido-líquido;
- a formação de tubérculos e células de aeração diferencial pode acelerar corrosão localizada;
- em ambiente marinho sobre aço carbono, há uma etapa inicial aeróbia controlada pela redução de oxigênio dissolvido e, depois, uma etapa anaeróbia em que a corrosão passa a ser fortemente influenciada microbiologicamente;
- bactérias redutoras de sulfato podem converter sulfato em sulfeto, elevando agressividade do meio e favorecendo formação de sulfetos de ferro.

Condições favoráveis apontadas:
- presença simultânea de água e hidrocarbonetos;
- baixa velocidade ou estagnação;
- alto tempo de residência;
- faixas de temperatura compatíveis com crescimento microbiano.

**Sinais de alerta:** existência de H2S em equipamento onde não se esperaria esse teor, biofilmes, depósitos, tubérculos e corrosão localizada sob depósitos.

*Fontes: [`petroles-004c2afadba7ea17c7dd7908:pNone:2731387.0-2731436.0`, `petroles-4ee4bce16acf674505c8912d:pNone:2324733.0-2324772.0`, `petroles-4ee4bce16acf674505c8912d:pNone:2586128.0-2586171.0`, `petroles-4ee4bce16acf674505c8912d:pNone:488245.0-488289.0`]*

### 3.4 Corrosão-erosão e cavitação
A erosão-corrosão resulta da atuação simultânea de remoção mecânica e ataque eletroquímico/químico. O ponto central é a **remoção da película protetora** ou do próprio material por fluido em movimento e/ou partículas sólidas, expondo metal ativo ao meio.

Morfologias mencionadas nas fontes:
- alvéolos;
- canais;
- vales;
- ondas direcionais;
- sulcos, crateras e furos arredondados.

Fatores de controle destacados:
- velocidade do fluido;
- concentração de particulados;
- natureza dos particulados;
- movimento relativo fluido/material.

Equipamentos tipicamente vulneráveis incluem bombas, válvulas, hélices, agitadores e componentes com escoamento acelerado. As fontes também citam trocadores/permutadores sujeitos a vibração transmitida por bombas, o que pode agravar degradação.

A **cavitação** é tratada separadamente como perda localizada de espessura por colapso de bolhas de vapor em regiões de baixa pressão, sendo favorecida por variações de pressão/temperatura e pela presença de particulados.

**Implicação prática:** onde houver velocidade elevada, mudança brusca de direção, presença de areia ou outros sólidos e histórico de falha de película protetora, deve-se considerar erosão-corrosão como mecanismo dominante, e não apenas corrosão uniforme.

*Fontes: [`petroles-4ee4bce16acf674505c8912d:pNone:2324733.0-2324772.0`, `petroles-4ee4bce16acf674505c8912d:pNone:2586128.0-2586171.0`, `petroles-4ee4bce16acf674505c8912d:pNone:488245.0-488289.0`, `regis-f71d2b01442addcb04ce7364:pNone:2288.0-2516.0`]*

### 3.5 Corrosão sob fadiga
A corrosão sob fadiga ocorre quando o material está submetido a **esforços cíclicos** em meio corrosivo. As fontes convergem em um ponto central: em ambiente corrosivo ocorre o **desaparecimento do limite de fadiga**, de modo que mesmo tensões baixas podem levar à fratura após certo número de ciclos.

Mecanismos associados descritos nas fontes:
- pites atuando como concentradores de tensão e locais preferenciais de iniciação de trincas;
- dissolução anódica preferencial na ponta da trinca;
- ruptura cíclica de camadas passivas ou filmes de óxido;
- repassivação local seguida de nova ruptura;
- fragilização por hidrogênio.

O processo é mais expressivo em meios aquosos do que gasosos, porque a formação de células eletroquímicas requer eletrólito. Em aços carbono, a trinca frequentemente inicia em pites e costuma ser transgranular, ainda que isso não seja regra absoluta.

Exemplos de condições favoráveis citadas:
- tubulações com ciclos térmicos de expansão e contração;
- trocadores sujeitos a vibração;
- diversos vasos de pressão;
- tubulações com ciclos mecânicos de pressão.

**Decisão de controle importante:** a proteção catódica pode aumentar a resistência à iniciação de trincas de corrosão-fadiga em aços de baixo carbono, mas em aços de alta resistência pode piorar o comportamento por favorecer fragilização por hidrogênio. Portanto, a seleção do método de controle deve considerar a classe do material, e não apenas a taxa de corrosão generalizada.

*Fontes: [`petroles-004c2afadba7ea17c7dd7908:pNone:2731387.0-2731436.0`, `petroles-004c2afadba7ea17c7dd7908:pNone:2731410.0-2731454.0`, `regis-f71d2b01442addcb04ce7364:pNone:2288.0-2516.0`, `petroles-4ee4bce16acf674505c8912d:pNone:1128505.0-1128546.0`]*

### 3.6 Corrosão sob tensão (SCC) e mecanismos correlatos
A corrosão sob tensão é definida nas fontes como deterioração por ação combinada de **tensões estáticas** (aplicadas ou residuais) e **meio corrosivo específico**. Diferencia-se da corrosão sob fadiga porque não depende de carregamento alternado. Um aspecto operacional importante é que pode haver **muito pouca perda de massa visível**: o material pode manter bom aspecto superficial até a fratura.

As fontes mencionam, entre outras, as seguintes variantes:
- **SCC por cloreto**, particularmente relevante para aços inoxidáveis austeníticos, controlada por teor de cloretos, pH, temperatura, oxigênio, tensão e microestrutura;
- **SCC por amina**, em aços carbono e baixa liga, associada a alcanolaminas contaminadas em regiões tensionadas;
- trincamento externo em tubulações de gás, com possibilidade de propagação adicional por fadiga quando existem ciclos de pressão.

**Pontos críticos de acompanhamento:**
- soldas e zonas termicamente afetadas, por tensões residuais;
- áreas com defeitos superficiais, pites ou revestimentos degradados;
- regiões em que o meio contém cloretos, aminas ou H2S.

*Fontes: [`petroles-004c2afadba7ea17c7dd7908:pNone:2731387.0-2731436.0`, `petroles-4ee4bce16acf674505c8912d:pNone:2586128.0-2586171.0`, `petroles-4ee4bce16acf674505c8912d:pNone:488245.0-488289.0`, `petroles-4ee4bce16acf674505c8912d:pNone:1128505.0-1128546.0`]*

### 3.7 Fragilização por hidrogênio e empolamento
A fragilização por hidrogênio é descrita como dano decorrente da incorporação e retenção de hidrogênio acima do nível tolerado, causando tensões internas elevadas e queda acentuada da capacidade de deformação. O hidrogênio atômico pode vir de diferentes fontes, incluindo processos eletroquímicos de corrosão e meios com H2S.

As fontes indicam que o fenômeno pode ser favorecido por:
- fração de hidrogênio atômico disponível;
- alta resistência mecânica do material;
- microestrutura suscetível à transição dúctil-frágil;
- tensões aplicadas ou residuais elevadas.

O **empolamento pelo hidrogênio** é citado como situação em que o hidrogênio atômico difunde-se rapidamente, acumula-se em descontinuidades, vazios ou inclusões e se recombina em H2 molecular, gerando pressão interna e bolhas.

**Implicação de integridade:** materiais de maior resistência e regiões soldadas/tensionadas devem receber atenção especial em ambientes sour, porque uma taxa de corrosão aparentemente moderada pode coexistir com mecanismo fragilizante de alta severidade.

*Fontes: [`petroles-004c2afadba7ea17c7dd7908:pNone:2731387.0-2731436.0`, `petroles-004c2afadba7ea17c7dd7908:pNone:2731410.0-2731454.0`, `petroles-4ee4bce16acf674505c8912d:pNone:2586128.0-2586171.0`]*

## 4. Acompanhamento e monitoramento dos mecanismos

### 4.1 Direcionadores para escolha de pontos de monitoramento
A partir dos mecanismos descritos, os pontos de acompanhamento devem ser escolhidos onde haja maior probabilidade de combinação entre eletrólito, espécies agressivas e tensões. Com base nas fontes, merecem priorização:
- trechos com **água produzida** e alta concentração de sais;
- pontos com **CO2** e/ou **H2S** dissolvidos;
- regiões com **areia ou sólidos** em suspensão;
- equipamentos sujeitos a **vibração** e **ciclos térmicos**;
- **soldas** e zonas com tensões residuais;
- áreas com **revestimento** onde a visualização direta é improvável;
- sistemas de baixa velocidade ou maior residência, propensos a **CMI/MIC**.

### 4.2 Métodos de acompanhamento citados nas fontes
As fontes fornecem métodos de monitoramento especialmente voltados à corrosão interna e ao estudo de mecanismos:

#### a) Cupons de perda de massa
Podem ser instalados no interior do duto para informar a taxa de corrosão interna ao longo do tempo. São úteis para tendência global, mas não capturam bem a severidade local de pites isolados.

#### b) Sondas de resistência elétrica
Também podem ser instaladas internamente para acompanhamento da taxa de corrosão. São apropriadas para tendência e resposta mais contínua que cupons em certas aplicações.

#### c) Técnicas eletroquímicas
As fontes destacam grande vantagem dessas técnicas por permitirem avaliação **não destrutiva**, inclusive **in situ**, sem remoção do corpo de prova do meio. Elas permitem estudar a **cinética** do processo corrosivo, e não apenas a perda de massa acumulada.

Métodos explicitamente citados:
- **extrapolação de Tafel** e **resistência de polarização**: estudo de corrosão uniforme;
- **polarização potenciodinâmica cíclica**, **potenciostático/galvanostático** e **ruído eletroquímico**: estudo de corrosão localizada;
- aplicação também a corrosão galvânica, seletiva, corrosão sob tensão e danos induzidos por hidrogênio;
- uso no estudo de passivação, proteção catódica/anódica e desempenho de revestimentos metálicos de sacrifício ou de barreira.

### 4.3 Limitações de detectabilidade
As fontes ressaltam que alguns mecanismos são intrinsecamente difíceis de detectar cedo:
- **corrosão localizada por pites**, pela dificuldade de mensuração representativa;
- **corrosão sob revestimento**, porque a visualização direta é improvável e o dano pode progredir oculto;
- mecanismos trincantes, como SCC e fragilização por hidrogênio, que podem evoluir sem grande perda de massa aparente.

**Conclusão operacional:** monitorar apenas taxa média de corrosão não é suficiente quando o mecanismo provável é localizado ou trincante.

*Fontes: [`petroles-004c2afadba7ea17c7dd7908:pNone:2731410.0-2731454.0`, `petroles-4ee4bce16acf674505c8912d:pNone:1128505.0-1128546.0`, `petroles-4ee4bce16acf674505c8912d:pNone:2324733.0-2324772.0`]*

## 5. Avaliação de criticidade e decisões de controle

### 5.1 Leitura integrada do risco de degradação
A severidade do mecanismo não deve ser inferida apenas pela taxa de perda de espessura. As fontes sugerem pelo menos três classes de risco distintas:
1. **perda generalizada de espessura** — mais fácil de acompanhar por tendência;
2. **ataque localizado** — menor previsibilidade, maior potencial de perfuração ou iniciação de trinca;
3. **mecanismos trincantes/fragilizantes** — podem falhar com pouca perda de massa visível.

### 5.2 Variáveis de decisão para controle
Os trechos indicam como variáveis decisórias principais:
- composição do meio: água, cloretos, CO2, H2S, ácidos orgânicos, oxigênio;
- hidráulica: velocidade do fluido e teor de sólidos;
- mecânica: ciclos de carga, vibração, pressão, tensões residuais;
- metalurgia: composição, dureza, microestrutura, nível de resistência;
- presença e estabilidade de película de produto de corrosão ou revestimento.

### 5.3 Medidas de controle mencionadas nas fontes
As fontes citam, em termos gerais, as seguintes abordagens de mitigação:
- **revestimentos**;
- **proteção catódica**;
- **inibidores**;
- **novas técnicas metalúrgicas** e seleção de materiais;
- **materiais não metálicos**, quando aplicáveis;
- controle de **velocidade** e de **particulados** em erosão-corrosão.

Entretanto, a escolha deve respeitar o mecanismo predominante. Exemplo importante: proteção catódica pode ser benéfica para corrosão-fadiga em aço de baixo carbono, mas contraproducente em aço de alta resistência pela elevação do risco de fragilização por hidrogênio.

### 5.4 Tubulações com defeitos de corrosão
Para tubulações com perda de seção, as fontes mencionam uso de métodos **determinísticos** e **probabilísticos** de avaliação de confiabilidade/resistência remanescente. O método B31G é citado como amplamente empregado, mas com desempenho mais satisfatório para defeitos de corrosão pequenos do que para defeitos longos em espiral. Isso reforça que a qualidade da caracterização geométrica do defeito é decisiva para a avaliação de integridade.

*Fontes: [`petroles-4ee4bce16acf674505c8912d:pNone:597640.60-597677.0`, `petroles-4ee4bce16acf674505c8912d:pNone:1128505.0-1128546.0`, `petroles-4ee4bce16acf674505c8912d:pNone:2586128.0-2586171.0`, `regis-f71d2b01442addcb04ce7364:pNone:2288.0-2516.0`]*

## 6. Síntese aplicada para equipamentos e tubulações de FPSO
Para avaliação profissional da integridade por corrosão em ativos de processo, uma síntese útil é:

- **CO2 + água**: esperar corrosão interna de aço carbono, inicialmente generalizada, podendo localizar se a camada de FeCO3 for instável.
- **H2S + água + aço suscetível**: além de corrosão, considerar fortemente mecanismos por hidrogênio e trincamento assistido pelo meio.
- **água + hidrocarboneto + baixa velocidade/estagnação**: incluir MIC/CMI no diagnóstico diferencial.
- **alta velocidade + sólidos**: priorizar erosão-corrosão e cavitação em componentes de escoamento.
- **pites + ciclos de pressão/vibração/temperatura**: elevar suspeita de corrosão sob fadiga.
- **tensão residual/aplicada + meio específico (cloretos, aminas, H2S)**: investigar SCC, mesmo sem perda de massa expressiva.
- **revestimento aparentemente íntegro** não elimina risco: corrosão sob revestimento pode permanecer oculta até estágio avançado.

Essa lógica ajuda a definir prioridades de inspeção, técnicas de monitoramento, criticidade de anomalias e medidas compensatórias enquanto a condição real do ativo é melhor caracterizada.

*Fontes: [`petroles-004c2afadba7ea17c7dd7908:pNone:2731387.0-2731436.0`, `petroles-004c2afadba7ea17c7dd7908:pNone:2731410.0-2731454.0`, `petroles-4ee4bce16acf674505c8912d:pNone:2324733.0-2324772.0`, `petroles-4ee4bce16acf674505c8912d:pNone:2586128.0-2586171.0`, `petroles-4ee4bce16acf674505c8912d:pNone:1128505.0-1128546.0`, `regis-f71d2b01442addcb04ce7364:pNone:2288.0-2516.0`]*