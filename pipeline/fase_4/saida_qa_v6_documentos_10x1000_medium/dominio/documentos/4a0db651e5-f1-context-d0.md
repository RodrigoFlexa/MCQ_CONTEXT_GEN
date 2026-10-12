# Posicionamento e cobertura de detectores em sistemas F&G de FPSO/FSO

## 1. Premissas técnicas da faceta
O posicionamento e a cobertura de detectores de fogo e gás (F&G) devem ser definidos a partir dos cenários de perigo da instalação, e não apenas por aplicação cega de malhas geométricas. O objetivo prático é detectar liberações de gás, fumaça ou fogo cedo o suficiente para permitir resposta operacional e atuação das barreiras associadas. Na prática offshore, isso exige combinar conhecimento de processo, layout, ventilação, dispersão, geometria do módulo/área e limitações reais de cada tecnologia de detecção.

As fontes utilizadas nesta composição mostram que a eficácia do sistema depende fortemente de:
- características do cenário de liberação;
- regime de ventilação natural e/ou mecânica;
- confinamento e congestionamento do módulo;
- tipo de detector e suas interferências ambientais;
- posicionamento relativo a fontes prováveis de vazamento, caminhos preferenciais de dispersão e volumes onde gás pode se acumular.

**Fontes da seção:** `hse-48d901a1fbf08e9f46bb522f:p13-17:15.0-9.0`, `hse-48d901a1fbf08e9f46bb522f:p17-20:10.0-20.0`

## 2. Critérios gerais de projeto para localização e cobertura

### 2.1 Cobertura deve ser específica ao perigo local
As fontes ressaltam que a localização dos cabeçotes detectores deve ser **específica às condições de perigo da área coberta**. Embora a prática frequentemente use malhas regulares, o arranjo final não deve ser decidido somente por espaçamento padrão. A malha é um ponto de partida; a efetividade depende de como os detectores interceptam os cenários plausíveis de formação de nuvem, fogo ou fumaça.

Isso implica que o projeto de cobertura precisa considerar, no mínimo:
- inventário e propriedades dos fluidos processados;
- provável tipo de vazamento: contínuo ou instantâneo, monofásico, bifásico, em jato, em poça etc.;
- taxa de liberação, direção e localização do vazamento;
- efeitos de empuxo, densidade relativa ao ar e resfriamento local da nuvem;
- obstáculos, equipamentos, anteparas e outras obstruções ao escoamento e à linha de visão;
- ventilação externa e interna, incluindo recirculação e zonas mortas.

A literatura utilizada também reforça que a dispersão atmosférica e local depende da massa específica do gás, da velocidade e direção do vento, do tipo de descarga, do relevo/obstruções e do grau de confinamento. Para gases densos, a nuvem tende a se “achatar” e se espalhar lateralmente em baixa altura; para gases leves, o empuxo favorece subida; e para gases aproximadamente neutros, o comportamento pode ser tratado de forma distinta. Esses aspectos afetam diretamente a altura e a distribuição espacial dos detectores.  

**Fontes da seção:** `hse-48d901a1fbf08e9f46bb522f:p13-17:15.0-9.0`, `petroles-4ee4bce16acf674505c8912d:pNone:2655068.0-2655098.0`

### 2.2 Ventilação é variável crítica de desempenho
As fontes HSE são enfáticas ao afirmar que levantamentos de ventilação em tempo real são críticos para o desempenho dos detectores, inclusive para identificar recirculações e zonas mortas. A cobertura por detectores pontuais de gás é especialmente sensível ao regime de ventilação. Portanto, o mesmo arranjo físico pode ter desempenho muito diferente se houver alteração em:
- venezianas, paredes parciais e fechamento de módulos;
- operação de HVAC e exaustão;
- posicionamento de equipamentos que criem sombreamento aerodinâmico;
- direção predominante de vento e sua interação com a geometria da instalação.

As próprias referências citadas apontam incertezas importantes sobre critérios de ventilação em normas, incluindo inconsistências entre taxa de renovação de ar e taxa de ventilação como medidas de adequação. Em termos de projeto de F&G, a consequência é clara: **cobertura não deve ser validada apenas por um número global de trocas de ar por hora**; é necessário entender a distribuição do fluxo de ar e os bolsões de acúmulo.

**Fontes da seção:** `hse-48d901a1fbf08e9f46bb522f:p13-17:15.0-9.0`, `hse-48d901a1fbf08e9f46bb522f:p18-22:22.0-12.0`

## 3. Detectores de gás inflamável: posicionamento e mapeamento de cobertura

### 3.1 Variáveis dominantes para espaçamento
Segundo as fontes HSE, o espaçamento entre cabeçotes de detecção de gás é governado por:
- tamanho e geometria da área;
- grau de confinamento e congestionamento;
- ventilação;
- natureza da liberação.

Em áreas congestionadas, é citado como valor típico um **espaçamento mínimo em torno de 5 m** para detectores pontuais. Esse valor não deve ser interpretado como universal; ele reflete uma regra prática utilizada em módulos offshore congestionados e foi sustentado por estudos experimentais em que uma malha de 5 m teve bom resultado para detectar liberações que efetivamente formavam nuvens dentro do módulo.

**Fontes da seção:** `hse-48d901a1fbf08e9f46bb522f:p17-20:10.0-20.0`, `hse-48d901a1fbf08e9f46bb522f:p18-22:22.0-12.0`

### 3.2 Limitações de uma malha uniforme
Os mesmos estudos mostram que, quando a nuvem formada é pequena ou cresce lentamente, os tempos de detecção aumentam e, em alguns casos, a liberação pode não ser detectada. Também foi observado que:
- reduzir pela metade o espaçamento traz apenas redução modesta do tempo de detecção, mas com grande aumento do número de detectores;
- dobrar o espaçamento provoca grande aumento do tempo de detecção.

O aprendizado prático é que a cobertura não deve ser julgada apenas por “densidade de detectores”. O ganho real vem do **bom posicionamento** em função da dispersão esperada, do processo executado no módulo e do layout. Detectores bem posicionados podem superar, em desempenho, arranjos mais densos porém mal localizados.

**Fontes da seção:** `hse-48d901a1fbf08e9f46bb522f:p17-20:10.0-20.0`, `hse-48d901a1fbf08e9f46bb522f:p18-22:22.0-12.0`

### 3.3 Posicionamento tridimensional e gases densos/frio-resfriados
As fontes destacam que, após liberação de gás liquefeito, a nuvem pode ficar localmente fria e relativamente densa, tendendo a “afundar” em áreas com baixo movimento de ar. Nessas condições, recomenda-se que os detectores sejam distribuídos em **padrão tridimensional**, com alguns cabeçotes em nível baixo nos módulos sujeitos a esse comportamento.

Esse critério é especialmente relevante quando houver:
- risco de gases ou vapores mais densos que o ar;
- possibilidade de resfriamento por expansão;
- volumes aprisionados ou com ventilação deficiente;
- pisos, valas, depressões ou obstáculos que favoreçam acúmulo em baixa altura.

O critério geral é alinhar a altura do detector ao caminho mais provável da nuvem, em vez de posicionar todos os pontos numa única elevação.

**Fontes da seção:** `hse-48d901a1fbf08e9f46bb522f:p17-20:10.0-20.0`, `petroles-4ee4bce16acf674505c8912d:pNone:2655068.0-2655098.0`

### 3.4 Detectores pontuais, por caminho aberto e acústicos
As fontes consultadas distinguem três contribuições relevantes para cobertura de gás:

- **Detectores pontuais de concentração**: sensíveis ao regime de ventilação e à trajetória local da nuvem; podem impor maior carga de manutenção.
- **Detectores por caminho aberto / line-of-sight / feixe IR**: fornecem cobertura mais ampla e, em dutos, tendem a cobrir melhor a seção atravessada.
- **Detectores acústicos de vazamento ultrassônico**: são posicionados a partir da identificação das fontes potenciais de fuga, especialmente junções em sistemas de gás de alta pressão; exigem conhecimento do ruído de fundo e cuidado com reflexões acústicas que possam gerar alarmes espúrios.

A estratégia técnica sugerida nas fontes é usar **combinação de sensores**, de modo que detectores acústicos possam fornecer indicação muito precoce de vazamento, enquanto detectores IR por ponto ou por feixe identificam acúmulo efetivo de nuvem inflamável.

Para detectores acústicos, o mapeamento da cobertura deve partir de uma **carta de ruído ultrassônico de fundo**, utilizada para definição do nível de alarme e da localização ótima. Já para detectores por feixe, é essencial verificar desobstrução do caminho óptico e a correspondência entre o feixe e os caminhos prováveis de passagem da nuvem.

**Fontes da seção:** `hse-48d901a1fbf08e9f46bb522f:p13-17:15.0-9.0`, `hse-48d901a1fbf08e9f46bb522f:p17-20:10.0-20.0`

### 3.5 Escolha tecnológica e efeito na cobertura
Nos resultados experimentais citados, os detectores IR pontuais tiveram melhor desempenho do que detectores catalíticos tanto no número de liberações detectadas quanto no tempo de detecção. Detectores por feixe IR também apresentaram bom desempenho quando comparados a fileiras de detectores pontuais IR.

Isso não significa que uma tecnologia substitui automaticamente a outra, mas indica um critério de projeto: a seleção e o posicionamento devem levar em conta a **capacidade de detecção dentro do cenário específico**, e não só o tipo de sensor adotado por tradição. Em áreas extensas, com geometrias que dificultam cobertura pontual, detectores por feixe podem ser fortes candidatos. Em áreas de fontes específicas e caminhos de passagem mais previsíveis, detectores pontuais podem ser adequados, desde que bem localizados.

**Fontes da seção:** `hse-48d901a1fbf08e9f46bb522f:p18-22:22.0-12.0`

## 4. Mapeamento por cenários de vazamento e por layout do FPSO/FSO

### 4.1 Partir de fontes prováveis de liberação
O posicionamento de detectores deve começar pelo mapeamento dos pontos de vazamento mais críticos. O exemplo de estudo de dispersão em planta de teste de poço em unidade marítima descreve que os pontos principais foram definidos nos pisos/áreas de trabalho e na entrada e saída dos equipamentos principais, e a malha de detectores foi construída para cobrir esse layout.

Na prática de FPSO/FSO, isso direciona a priorização de cobertura em regiões como:
- manifolds e conexões;
- linhas e válvulas de alta pressão;
- sucções e descargas de compressores;
- vasos separadores, aquecedores, trocadores e suas interligações;
- interfaces de transferência e trechos com maior inventário ou energia de vazamento.

**Fontes da seção:** `petroles-004c2afadba7ea17c7dd7908:pNone:474078.0-474135.0`, `hse-48d901a1fbf08e9f46bb522f:p17-20:10.0-20.0`

### 4.2 Considerar a lógica do arranjo físico do FPSO
O arranjo físico do convés influencia diretamente a filosofia de cobertura. Em FPSOs, o convés tende a permitir separação progressiva entre áreas seguras/ocupadas e áreas de maior risco de hidrocarbonetos. O texto de apoio destaca, por exemplo:
- manutenção de áreas seguras, como casario, afastadas dos sistemas mais perigosos;
- posicionamento do flare no extremo oposto à acomodação;
- necessidade de considerar ventos predominantes para evitar que a chama do flare atue como fonte de ignição de vazamentos na planta;
- recomendação de dispor equipamentos de processo em conveses expostos ou áreas abertas com ventilação natural, evitando confinamento de hidrocarbonetos em salas.

Para o projeto de F&G, esses aspectos significam que a cobertura deve ser analisada por **macrozonas de risco** e interfaces entre elas, considerando:
- transição entre processo e áreas ocupadas;
- possíveis trajetórias de dispersão rumo a áreas seguras;
- interferência de flare, estruturas, passarelas e módulos na ventilação e na linha de visão.

**Fontes da seção:** `petroles-004c2afadba7ea17c7dd7908:pNone:1185920.0-1185961.0`

### 4.3 Uso de CFD e outras ferramentas de estudo de cobertura
As fontes indicam o uso de ferramentas computacionais para otimização de cobertura:
- **CAD** para otimizar cones de visão de detectores de chama;
- **CFD** para estudar dispersão de gás ao redor de equipamentos e estruturas e, a partir daí, definir número e localização de detectores;
- medições de ventilação e estudos experimentais para validar hipóteses de dispersão.

O exemplo do estudo de CO2 em unidade de teste descreve exatamente esse fluxo: modelagem CFD com a geometria dos equipamentos e estruturas, definição de cenários de vazamento e posicionamento dos detectores para identificação de pequenos vazamentos. Embora o caso seja de CO2 e não de gás inflamável, o valor metodológico para cobertura de F&G é claro: **localização de detectores deve ser demonstrada por cenários e geometria reais**.

As fontes HSE também observam que modelos de dispersão têm incertezas, sobretudo em módulos congestionados e confinados, e que modelos mais antigos precisam de validação contra dados experimentais mais recentes. Assim, CFD e modelagem são ferramentas úteis, mas não dispensam julgamento de engenharia, inspeção de campo e revisão quando houver mudanças de layout ou ventilação.

**Fontes da seção:** `petroles-004c2afadba7ea17c7dd7908:pNone:474078.0-474135.0`, `hse-48d901a1fbf08e9f46bb522f:p18-22:22.0-12.0`, `hse-48d901a1fbf08e9f46bb522f:p13-17:15.0-9.0`

## 5. Posicionamento e cobertura de detectores de chama, calor e fumaça

### 5.1 Detectores de chama
Os detectores de chama devem ser posicionados para que o **cone de visão** cubra as áreas onde o fogo pode ocorrer. Para detectores IR de chama, as fontes citam cerca de **15 m** como alcance razoável, devido à obscurecimento por fumaça e à menor sensibilidade na periferia do campo de visão. Em módulos ou áreas, eles são usualmente posicionados nos cantos, e ferramentas CAD podem ser empregadas para otimizar cobertura e minimizar zonas cegas.

Outro ponto relevante é que sistemas IR de três bandas são mencionados como menos suscetíveis a falsos alarmes. Para posicionamento, isso significa que o campo visual deve ser verificado não só em condição “limpa”, mas considerando possíveis bloqueios por estruturas, fumaça e reflexos.

**Fontes da seção:** `hse-48d901a1fbf08e9f46bb522f:p13-17:15.0-9.0`

### 5.2 Detectores de calor
As fontes apresentam regras práticas de cobertura para detectores pontuais de calor:
- em áreas abertas e naturalmente ventiladas: aproximadamente **1 detector por 25 m²**, com espaçamento de **7 m** e distância máxima até anteparas de **3,5 m**;
- em módulos fechados com ventilação mecânica: aproximadamente **1 detector por 37 m²**, com espaçamento de **9 m** e distância máxima até anteparas de **4,5 m**.

Também é indicado que detectores pontuais de calor **não são adequados para tetos altos acima de 8 m**, devido à piora de sensibilidade com a altura.

Esses critérios servem como heurística de projeto, mas devem ser ajustados ao volume, à estratificação térmica, aos fluxos de ar e ao cenário de incêndio esperado.

**Fontes da seção:** `hse-48d901a1fbf08e9f46bb522f:p13-17:15.0-9.0`

### 5.3 Detectores de fumaça
Detectores pontuais de fumaça dependem do transporte convectivo de particulados e gases de combustão até o detector. As fontes indicam espaçamento máximo corrente em torno de **7,5 m** e apontam que eles **não são apropriados para tetos altos acima de 10,5 m**. Embora o aumento da altura possa permitir distribuição mais uniforme dos produtos de combustão, a concentração na altura do detector tende a diminuir, exigindo sensibilidade adequada.

Como consequência, a cobertura de fumaça precisa verificar:
- caminhos de convecção e retorno de ar;
- influência do HVAC;
- altura livre e barreiras arquitetônicas;
- tempo de transporte do fumo até o detector.

**Fontes da seção:** `hse-48d901a1fbf08e9f46bb522f:p13-17:15.0-9.0`, `hse-48d901a1fbf08e9f46bb522f:p17-20:10.0-20.0`

## 6. Efeitos ambientais e interferências que alteram a cobertura real
A cobertura geométrica raramente coincide com a cobertura efetiva em campo. As fontes citam diversos fatores que podem degradar desempenho ou gerar falsos alarmes:
- luz solar rasante;
- neblina, condensação e reflexos em alguns detectores de gás;
- obscurecimento por fumaça em detectores IR de chama;
- forte dependência do regime de ventilação para detectores pontuais de gás;
- reflexões acústicas em detectores ultrassônicos;
- maior carga de manutenção em detectores pontuais comparados a detectores line-of-sight;
- baixa capacidade dos detectores de gás em detectar névoas de óleo; para esse fenômeno, detectores ópticos por feixe são mais mencionados.

Do ponto de vista de cobertura, esses fatores exigem que a localização prevista em desenho seja verificada quanto a:
- exposição a contaminação, condensação e spray marinho;
- incidência solar/reflexos nos ângulos reais de instalação;
- obstrução progressiva por equipamentos, suportes e modificações de campo;
- acessibilidade para manutenção, sem a qual a cobertura nominal se deteriora.

**Fontes da seção:** `hse-48d901a1fbf08e9f46bb522f:p13-17:15.0-9.0`, `hse-48d901a1fbf08e9f46bb522f:p17-20:10.0-20.0`

## 7. Incertezas relevantes para avaliação de cobertura
As fontes consultadas registram incertezas importantes que precisam ser reconhecidas no projeto e na revisão de cobertura:

1. Faltam diretrizes suficientemente detalhadas para a combinação ótima entre detectores pontuais, por feixe e acústicos.  
2. A melhor localização para diferentes fluidos inflamáveis — por exemplo, metano, propano e condensados C5-C8 — não está plenamente definida.  
3. Há pouca informação sobre a efetividade na detecção de vazamentos de baixa taxa, menores que **1,0 kg/s**, que podem se tornar perigosos ao longo do tempo.  
4. A resposta de sensores calibrados em metano para hidrocarbonetos mais pesados não é bem definida.  
5. A relação entre grandezas medidas por feixe (**%LEL·m**) ou por acústica (**dB**) e o perigo inflamável real ainda não é bem entendida.  
6. A literatura citada reporta uma taxa efetiva global de detecção de cerca de **60%** em análise histórica de liberações de hidrocarbonetos, o que evidencia que cobertura nominal não garante detecção efetiva em todos os cenários.

Essas incertezas reforçam a necessidade de usar estudos de dispersão, revisão periódica e análise de desempenho observado em serviço, em vez de depender exclusivamente de regras fixas.

**Fontes da seção:** `hse-48d901a1fbf08e9f46bb522f:p13-17:15.0-9.0`, `hse-48d901a1fbf08e9f46bb522f:p17-20:10.0-20.0`

## 8. Diretrizes práticas para mapeamento de detectores
Com base no material fornecido, um processo técnico coerente para mapeamento de detectores em FPSO/FSO pode ser resumido assim:

1. **Definir cenários de perigo por área/módulo**  
   Identificar fluidos, pressões, fases, inventário, modos de falha e fontes prováveis de vazamento.

2. **Ler o layout como campo de dispersão**  
   Considerar obstruções, congestão, confinamento, volumes aprisionados, alturas, interfaces com áreas ocupadas e efeito do arranjo do convés.

3. **Caracterizar ventilação real**  
   Avaliar ventilação natural e mecânica, direções predominantes do vento, recirculação e zonas mortas.

4. **Selecionar tecnologias por mecanismo de detecção**  
   - pontual para interceptar concentrações locais;  
   - por feixe para cobertura mais ampla e caminhos de passagem;  
   - acústica para identificação muito precoce de vazamentos de alta pressão;  
   - chama, calor e fumaça conforme o cenário de incêndio e geometrias do ambiente.

5. **Distribuir detectores segundo a física do cenário**  
   Usar padrões tridimensionais quando houver risco de afundamento da nuvem; posicionar detectores de chama pelos cones de visão e evitar zonas cegas; ajustar alturas e alcances à estratificação e à ventilação.

6. **Validar cobertura por estudo**  
   Empregar CAD, CFD, testes ou avaliação experimental compatível com o risco e a complexidade do arranjo.

7. **Revisar cobertura quando houver mudança**  
   Qualquer alteração de layout, anteparas, equipamentos, ventilação ou processo pode invalidar a cobertura originalmente demonstrada.

**Fontes da seção:** `hse-48d901a1fbf08e9f46bb522f:p13-17:15.0-9.0`, `hse-48d901a1fbf08e9f46bb522f:p17-20:10.0-20.0`, `hse-48d901a1fbf08e9f46bb522f:p18-22:22.0-12.0`, `petroles-004c2afadba7ea17c7dd7908:pNone:474078.0-474135.0`, `petroles-004c2afadba7ea17c7dd7908:pNone:1185920.0-1185961.0`

## 9. Exemplos técnicos sintéticos

### Exemplo 1 — Módulo congestionado com gás inflamável
Se o módulo é congestionado, naturalmente ventilado, com múltiplas junções e risco de formação de nuvens no interior, uma malha de detectores pontuais com ordem de grandeza de **5 m** pode ser um ponto de partida. Porém, se houver locais de baixa movimentação de ar e possibilidade de gás frio/denso, parte dos detectores deve ser instalada em níveis baixos e em padrão tridimensional. A distribuição final deve ser revista à luz do layout e dos resultados de dispersão.

### Exemplo 2 — Área com necessidade de ampla cobertura transversal
Quando há corredores de passagem da nuvem, dutos ou áreas onde a cobertura pontual deixaria grandes lacunas, detectores por feixe IR podem ampliar a cobertura efetiva. A instalação deve garantir que o caminho óptico permaneça desobstruído e represente o trajeto provável da nuvem.

### Exemplo 3 — Cobertura de fogo em módulo de processo
Detectores IR de chama podem ser instalados nos cantos para sobrepor campos de visão sobre áreas prováveis de incêndio, adotando cerca de **15 m** como alcance razoável de projeto inicial. CAD pode ser usado para checar intervisibilidade, pontos cegos e sombreamento por estruturas.

### Exemplo 4 — Revisão de cobertura após modificação de layout
A inclusão de skids, paredes parciais, exaustores ou novos equipamentos pode alterar drasticamente dispersão e linha de visão. Nesses casos, a cobertura originalmente aceitável pode deixar de sê-lo, mesmo sem mover nenhum detector. A revisão deve reavaliar ventilação, zonas mortas e cenários de vazamento.

**Fontes da seção:** `hse-48d901a1fbf08e9f46bb522f:p13-17:15.0-9.0`, `hse-48d901a1fbf08e9f46bb522f:p17-20:10.0-20.0`, `hse-48d901a1fbf08e9f46bb522f:p18-22:22.0-12.0`