# Internos e eficiência de separação

## 1. Papel dos internos no separador trifásico
O separador trifásico de produção não depende apenas do volume do vaso; seu desempenho resulta da combinação entre **hidrodinâmica interna**, **tempo de residência**, **controle de pressão e níveis** e **adequação dos internos** à carga de entrada. Em termos práticos, o vaso precisa reduzir a energia do escoamento de entrada, promover a segregação gás-líquido e líquido-líquido e manter, em limites toleráveis, três formas clássicas de desempenho insuficiente:

- **líquido arrastado no gás**;
- **água arrastada no óleo** (BSW);
- **óleo arrastado na água** (TOG).

Os trechos consultados descrevem o separador trifásico com quatro regiões funcionais principais:

1. **seção de separação primária**, na entrada do vaso, onde a maior parte do gás se desprende e gotas/líquido de maior tamanho são removidos;
2. **seção de acúmulo/coleta de líquido**, onde ocorre desgaseificação adicional do líquido e separação óleo-água por gravidade;
3. **seção de separação secundária**, na região gasosa, para remoção de gotas menores arrastadas pelo gás;
4. **seção de aglutinação**, na saída de gás, onde dispositivos como extratores de névoa promovem coalescência das gotas remanescentes.

Nos arranjos trifásicos horizontais com câmara de óleo e vertedouro, as variáveis mais diretamente relacionadas ao inventário e à qualidade da separação são:

- **pressão do gás**;
- **nível total e/ou nível de água na câmara de separação**;
- **nível de óleo na câmara de óleo**;
- **nível da interface óleo-água**.

Assim, os internos não são acessórios secundários: eles definem o padrão de escoamento real dentro do vaso e, portanto, a capacidade de evitar **carryover**, **carryunder** e arraste cruzado entre óleo e água.

**Fontes da seção:** `petroles-004c2afadba7ea17c7dd7908:pNone:215418.0-215453.0`, `petroles-004c2afadba7ea17c7dd7908:pNone:215508.0-215548.0`, `regis-282132e81add5278ef714ccc:pNone:2186.0-2371.0`, `regis-382370e69ec038894a313f3f:pNone:16.120-55.0`

## 2. Mecanismos físicos que os internos exploram
Os internos atuam sobre quatro mecanismos centrais de separação mencionados nas fontes:

- **separação gravitacional por diferença de densidades**;
- **separação inercial**, pela mudança brusca de direção e velocidade do escoamento;
- **coalescência em superfícies ou meios porosos**, aumentando o tamanho efetivo das gotas;
- **efeito centrífugo**, quando um dispositivo realmente estabelece escoamento rotacional interno.

A eficiência desses mecanismos depende fortemente de:

- intensidade de turbulência;
- tamanho inicial de gotas e bolhas;
- viscosidade do óleo;
- diferença de densidade entre óleo, água e gás;
- velocidade superficial do gás;
- tempo de residência disponível na fase líquida e na região gasosa.

As fontes destacam um ponto operacional importante: **quanto menor a turbulência na seção gasosa de separação secundária, melhor a eficiência de remoção de gotas líquidas do gás**. Na seção líquida, a lógica é semelhante: menor agitação e melhores trajetórias de drenagem favorecem a separação óleo-água e a liberação de gás disperso.

Também é enfatizado que gotas maiores se separam mais facilmente; por isso, internos coalescedores e superfícies de contato podem aumentar o desempenho sem necessariamente aumentar o volume do vaso. Essa é a base física do uso de **placas coalescedoras**, **demisters** e outros internos de aglutinação.

**Fontes da seção:** `petroles-004c2afadba7ea17c7dd7908:pNone:790828.0-790865.0`, `petroles-004c2afadba7ea17c7dd7908:pNone:215418.0-215453.0`, `petroles-004c2afadba7ea17c7dd7908:pNone:215456.0-215504.0`, `petroles-4ee4bce16acf674505c8912d:pNone:617338.0-617375.0`

## 3. Dispositivo de entrada: primeiro determinante da eficiência
### 3.1 Função
O dispositivo de entrada é tratado nas fontes como o **interno primário de separação**. Sua missão é receber uma corrente multifásica com alto momento, slugging eventual e forte desequilíbrio local de fases, e transformá-la em um escoamento menos destrutivo para o restante do vaso.

Sem essa etapa, o jato de entrada pode:

- ressuspender líquido já separado;
- gerar emulsificação adicional;
- aumentar a carga de gotas para a seção gasosa;
- reduzir o tempo de residência efetivo;
- sobrecarregar o extrator de névoa.

### 3.2 Tipos citados e efeito esperado
As fontes citam três famílias de solução:

- **placa plana**;
- **calota esférica**;
- **defletor centrífugo / entrada tipo ciclone**.

#### Placa plana
Promove mudança brusca de direção e velocidade, mas tende a espalhar mais o líquido. Segundo os trechos, esse espalhamento maior está associado a:

- maior probabilidade de arraste de líquido para a saída de gás;
- maior tendência à formação de emulsões água-em-óleo.

#### Calota esférica
Produz menor perturbação do escoamento do que a placa plana e menor espalhamento do líquido. Consequência esperada:

- menor re-entranhamento;
- menor severidade de emulsificação induzida pela entrada;
- melhor proteção das seções a jusante.

#### Dispositivo centrífugo / ciclone de entrada
Busca usar força centrífuga para promover separação mais eficiente de gás e líquido ainda na região de entrada. Entretanto, as fontes mostram um ponto crucial: **o benefício só existe se a geometria realmente estabelecer o campo rotacional necessário**.

Um estudo numérico citado avaliou um ciclone usado como interno de entrada e concluiu que, no desenho inicialmente proposto, **não se formou o escoamento rotacional interno esperado** por deficiência geométrica do bocal de entrada. O resultado foi eficiência limitada e possibilidade de pequenas gotas seguirem com o gás. Isso é tecnicamente relevante porque mostra que chamar um interno de “ciclone” não garante comportamento ciclônico efetivo.

### 3.3 Critérios práticos de avaliação
Na operação e no troubleshooting, o dispositivo de entrada deve ser suspeito quando houver:

- carryover de líquido no gás logo após aumento de vazão ou redução de pressão;
- formação persistente de emulsão após mudanças de poços ou composição;
- espuma intensa gerada/estabilizada pela energia de entrada;
- elevada sensibilidade da qualidade das correntes de saída a pequenas mudanças de vazão.

**Fontes da seção:** `petroles-004c2afadba7ea17c7dd7908:pNone:215438.0-215481.0`, `petroles-004c2afadba7ea17c7dd7908:pNone:215456.0-215504.0`, `petroles-004c2afadba7ea17c7dd7908:pNone:790828.0-790865.0`, `regis-282132e81add5278ef714ccc:pNone:2186.0-2371.0`

## 4. Internos para reduzir turbulência e estabilizar níveis/interfaces
### 4.1 Placas perfuradas e dispositivos tranquilizadores
As fontes citam **placas perfuradas (perforated plate baffles)** como internos usados especialmente em unidades marítimas para:

- atenuar o movimento do líquido;
- melhorar a distribuição de gás e líquidos;
- reduzir a turbulência;
- evitar zonas mortas e caminhos preferenciais;
- reduzir o impacto do fluido sobre outros internos.

Em um FPSO, isso é particularmente importante porque o separador não sofre apenas perturbações do escoamento do poço/manifold; ele também está sujeito a oscilações operacionais e, em alguns casos, efeitos de movimento da unidade sobre a superfície livre.

### 4.2 Placas quebra-ondas
As placas quebra-ondas são descritas como placas verticais que atravessam o nível de óleo e a interface óleo-água, instaladas perpendicularmente ao fluxo. Seu objetivo é evitar a propagação de ondas geradas por golfadas de líquido. Os efeitos desejados são:

- maior estabilidade do nível de óleo;
- maior estabilidade da interface óleo-água;
- melhor desempenho das malhas de controle de nível;
- menor probabilidade de arraste cruzado por oscilação hidráulica;
- mitigação do efeito do balanço do mar em plataformas flutuantes.

Esse último ponto é diretamente aderente à aplicação em FPSO: mesmo com bom dispositivo de entrada, a oscilação interna da superfície livre pode degradar a separação se o inventário líquido não estiver hidraulicamente “acalmo”.

### 4.3 Vertedouro e câmara de óleo
Nos separadores trifásicos horizontais citados, o **vertedouro** separa a câmara de acúmulo de líquido da câmara de óleo. O óleo verte por cima, acumula-se em uma câmara dedicada e sua vazão de saída é manipulada pela válvula de controle de nível de óleo; a água livre sai pelo fundo com controle do nível de interface.

Esse arranjo ajuda a:

- criar zonas líquidas mais definidas;
- reduzir curto-circuito hidráulico entre água e óleo;
- dar previsibilidade ao controle da interface;
- reduzir a chance de que água livre siga com o óleo por simples flutuação transiente.

**Fontes da seção:** `petroles-4ee4bce16acf674505c8912d:pNone:617338.0-617375.0`, `petroles-004c2afadba7ea17c7dd7908:pNone:215438.0-215481.0`, `petroles-004c2afadba7ea17c7dd7908:pNone:215418.0-215453.0`

## 5. Internos para separação óleo-água e prevenção de arraste cruzado
### 5.1 Placas coalescedoras / plate pack
As placas coalescedoras são apontadas nas fontes como um dos principais recursos para melhorar a separação líquido-líquido. Elas podem ser usadas tanto para:

- aumentar a aglutinação de gotas de óleo presentes na água;
- quanto para aumentar a aglutinação de gotas de água presentes no óleo.

O princípio é simples: ao atravessar ou escoar sobre as placas, as gotas encontram superfícies de contato e se unem em gotas maiores. Gotas maiores se separam mais facilmente por gravidade. As fontes também observam que as placas são normalmente dimensionadas para favorecer **escoamento laminar** através delas, condição importante para coalescência e drenagem.

### 5.2 Efeito sobre capacidade e retrofit
Um ponto operacional importante é que a instalação de pratos/placas coalescedoras pode:

- **aumentar a capacidade de separação de vasos existentes**;
- ou permitir **redução de tamanho** em projetos novos, quando adequadamente concebidos.

Em retrofit de FPSO, isso é particularmente relevante porque o aumento de produção de água ao longo da vida do campo costuma pressionar a capacidade do separador sem permitir expansão física simples do vaso.

### 5.3 Limitações práticas
O ganho de eficiência das placas coalescedoras depende de não haver degradação do escoamento por:

- turbulência excessiva na entrada;
- emulsão estável na interface;
- incrustação/parafina nas superfícies;
- sólidos e areia obstruindo passagens;
- má distribuição do fluxo, com bypass ou caminhos preferenciais.

Por isso, a simples presença do coalescedor não garante desempenho; ele precisa estar inserido em uma hidrodinâmica compatível.

**Fontes da seção:** `petroles-004c2afadba7ea17c7dd7908:pNone:215456.0-215504.0`, `petroles-4ee4bce16acf674505c8912d:pNone:617338.0-617375.0`, `petroles-004c2afadba7ea17c7dd7908:pNone:215508.0-215548.0`

## 6. Internos da seção gasosa: prevenção de carryover de líquido para o gás
### 6.1 Separação secundária e seção de aglutinação
Depois da separação primária, o gás ainda carrega gotas líquidas. As fontes tratam isso em duas etapas complementares:

- uma **seção de separação secundária**, fortemente afetada pela turbulência do gás;
- uma **seção de aglutinação** na saída de gás, com uso de extratores de névoa.

### 6.2 Extrator de névoa (demister)
O demister é descrito como um meio poroso ou estruturado que faz as gotas colidirem com uma superfície, coalescerem e drenarem por gravidade de volta ao fundo do vaso.

Tipos citados:

- **almofadas de tela metálica (wire-mesh)**;
- **tipo aletas / vane**;
- **placas cilíndricas**.

### 6.3 Efeito da velocidade do gás
A eficiência do demister depende criticamente da velocidade do gás:

- **velocidade muito baixa:** o gás atravessa o meio sem promover colisão/coalescência suficientes;
- **velocidade muito alta:** gotas já coalescidas podem ser re-arrastadas.

Isso torna o demister um interno com janela operacional relativamente estreita. Portanto, seu desempenho real depende da interação entre:

- área disponível na seção gasosa;
- pressão e temperatura de separação;
- vazão de gás libertado no vaso;
- qualidade da separação primária;
- carga de espuma/neblina que chega ao topo.

### 6.4 Sensibilidade a sujeira e seleção prática
As fontes indicam que o tipo **wire-mesh** é mais suscetível à obstrução do que outros. Em cenários com potencial de parafina, esse aspecto torna-se crítico. Também se destacam extratores alternativos e previsão de acesso/limpeza quando parafina for problema real ou potencial.

Em termos de prevenção de carryover, o demister é a última barreira mecânica antes da linha de gás. Se ele estiver saturado, mal selecionado, obstruído ou operando fora da faixa de velocidade, a separação global do vaso se deteriora rapidamente.

**Fontes da seção:** `petroles-004c2afadba7ea17c7dd7908:pNone:215418.0-215453.0`, `petroles-004c2afadba7ea17c7dd7908:pNone:215456.0-215504.0`, `regis-282132e81add5278ef714ccc:pNone:2186.0-2371.0`

## 7. Internos para evitar carryunder de gás nas saídas líquidas
### 7.1 Quebra-vórtice
O quebra-vórtice é instalado no bocal de saída de líquido no fundo do vaso para interromper a formação de redemoinho quando a válvula de controle abre e o líquido escoa. As fontes destacam dois riscos diretos do vórtice:

- **sucção de gás para a corrente líquida**;
- **arraste de óleo para a saída de água**.

Portanto, esse interno atua simultaneamente em dois problemas:

- **carryunder de gás nas correntes líquidas**;
- **degradação da separação óleo-água por sucção local seletiva**.

Tipos citados incluem tubo perfurado, plataforma e cruzeta.

### 7.2 Relação com controle de nível
O risco de vórtice aumenta quando há combinação de:

- vazão de saída elevada na fase líquida;
- baixo selo líquido local;
- oscilação do nível/interface;
- abertura agressiva da válvula de controle.

Assim, quebra-vórtice e estabilidade de nível não devem ser tratados separadamente. Em comissionamento e troubleshooting, a presença do interno deve ser verificada fisicamente, porque sua ausência ou dano pode imitar falha de controle de interface.

**Fontes da seção:** `petroles-004c2afadba7ea17c7dd7908:pNone:215438.0-215481.0`, `petroles-004c2afadba7ea17c7dd7908:pNone:215456.0-215504.0`, `petroles-4ee4bce16acf674505c8912d:pNone:617338.0-617375.0`

## 8. Espuma, emulsão, parafina e sólidos: como degradam os internos
### 8.1 Espuma
A formação de espuma pode decorrer das propriedades físico-químicas do óleo, impurezas e queda de pressão no escoamento/entrada do separador. Quando presente, a espuma:

- ocupa volume útil do vaso;
- dificulta o controle de nível;
- pode ser arrastada com o gás;
- pode contaminar o óleo desgaseificado.

As fontes recomendam, quando a tendência à espuma for previsível, o uso de **dispositivos internos específicos para removê-la** e superfície/tempo de coalescência suficientes para sua quebra. Um exemplo citado é o **prato quebra-espuma** com placas paralelas inclinadas, que promove ruptura das bolhas e coalescência do líquido retido.

### 8.2 Emulsões na interface óleo-água
O acúmulo de emulsão na interface:

- reduz o tempo de retenção efetivo;
- ocupa volume que deveria estar disponível para separação clara das fases;
- dificulta a medição e o controle da interface;
- aumenta o risco de água no óleo e óleo na água.

As fontes observam que calor e químicos podem minimizar emulsões, embora esses recursos sejam frequentemente mais associados ao tratamento posterior do óleo. Ainda assim, do ponto de vista do separador, o projeto deve prever espaço e hidrodinâmica compatíveis com a presença de banda de emulsão.

### 8.3 Parafina
Parafina pode obstruir exatamente os internos mais sensíveis à eficiência:

- **placas coalescedoras** na seção líquida;
- **extratores de névoa** na seção gasosa.

Por isso, quando o problema for real ou potencial, as fontes recomendam considerar extratores alternativos e prover **bocas de visita/orifícios/bocais para limpeza com solvente ou vapor**.

### 8.4 Areia e sedimentos
Areia e sedimentos causam:

- erosão de válvulas;
- obstrução de internos;
- redução do tempo de residência pelo acúmulo no fundo;
- perda de volume útil do vaso.

As fontes mencionam o uso de **jatos espalhadores de areia (sander jet)** e coletores para evitar obstrução de drenos e reduzir a frequência de parada para limpeza. Em separadores sem recurso de remoção de sólidos, a limpeza pode exigir interrupção da produção.

**Fontes da seção:** `petroles-004c2afadba7ea17c7dd7908:pNone:215508.0-215548.0`, `regis-282132e81add5278ef714ccc:pNone:2186.0-2371.0`, `petroles-004c2afadba7ea17c7dd7908:pNone:215438.0-215481.0`, `petroles-004c2afadba7ea17c7dd7908:pNone:215456.0-215504.0`

## 9. Efeito de pressão, temperatura e carga sobre o desempenho dos internos
### 9.1 Pressão
As fontes indicam que, ao reduzir a pressão de separação, aumenta o volume de gás liberado do óleo. Isso eleva a ocupação volumétrica do gás no vaso e tende a aumentar sua velocidade interna. Consequências:

- maior tendência de arraste de gotículas de óleo pela corrente gasosa;
- maior exigência sobre a seção gasosa e o demister;
- possível necessidade de reduzir vazão de entrada para evitar carryover;
- redução da capacidade efetiva do separador naquela condição.

Ou seja, um conjunto de internos que funciona bem em pressão mais alta pode tornar-se insuficiente quando a operação passa a liberar muito mais gás dentro do mesmo volume geométrico.

### 9.2 Temperatura
O aumento da temperatura tende a reduzir a densidade/viscosidade do óleo e aumentar a diferença relativa em relação à água, favorecendo sedimentação e separação líquido-líquido. Também pode reduzir espuma. Contudo, as fontes observam que elevar a temperatura pode produzir, na vazão de gás, efeito semelhante ao da redução da pressão: mais gás liberado e maior solicitação da seção gasosa.

Em uma referência metodológica citada, a temperatura de operação foi definida para manter a viscosidade cinemática do petróleo entre **10 cSt e 25 cSt**, condição que em muitos casos se associou a boa eficiência com **5 a 10 min** de residência líquida. Isso deve ser entendido como referência de metodologia específica, não como regra universal.

### 9.3 Regularidade da carga
Quando o separador recebe fluxo regular, as fontes indicam que é possível manter estáveis o nível de óleo e a velocidade de circulação do gás, obtendo maior eficiência. Em contraste, golfadas, mudanças de produção e instabilidade do manifold tendem a degradar o desempenho dos internos por:

- sobrecarga temporária do dispositivo de entrada;
- oscilação de níveis e interface;
- propagação de ondas no líquido;
- aumento de carryover/carryunder transiente.

**Fontes da seção:** `petroles-004c2afadba7ea17c7dd7908:pNone:215508.0-215548.0`, `regis-382370e69ec038894a313f3f:pNone:16.120-55.0`

## 10. Diagnóstico de baixo desempenho focado em internos
### 10.1 Líquido na saída de gás
Causas prováveis relacionadas a internos:

- dispositivo de entrada gerando espalhamento excessivo;
- ciclone de entrada sem campo rotacional efetivo;
- turbulência elevada na seção gasosa;
- demister obstruído, danificado ou operando fora da faixa de velocidade;
- espuma ocupando espaço na região gás-líquido;
- parafina bloqueando extrator de névoa.

### 10.2 Gás nas saídas líquidas
Causas prováveis:

- vórtice na saída líquida por ausência/falha do quebra-vórtice;
- oscilação severa do nível ou da interface;
- baixo tempo de residência no líquido;
- degaseificação insuficiente na seção de coleta.

### 10.3 Água no óleo e óleo na água
Causas prováveis:

- coalescedor inexistente, mal distribuído ou obstruído;
- alta turbulência por entrada agressiva ou slugs;
- banda de emulsão ocupando volume excessivo;
- vertedouro/câmara de óleo sem comportamento hidráulico adequado;
- erro de controle ou leitura da interface;
- vórtice sugando óleo para a saída de água.

### 10.4 Instabilidade persistente dos níveis
Causas prováveis:

- ausência/ineficiência de quebra-ondas;
- excesso de agitação por carga irregular;
- espuma mascarando nível real;
- acúmulo de sólidos reduzindo volume útil;
- caminhos preferenciais por distribuição inadequada do fluxo.

**Fontes da seção:** `petroles-004c2afadba7ea17c7dd7908:pNone:215438.0-215481.0`, `petroles-004c2afadba7ea17c7dd7908:pNone:215456.0-215504.0`, `petroles-004c2afadba7ea17c7dd7908:pNone:215508.0-215548.0`, `petroles-004c2afadba7ea17c7dd7908:pNone:790828.0-790865.0`, `petroles-4ee4bce16acf674505c8912d:pNone:617338.0-617375.0`, `regis-282132e81add5278ef714ccc:pNone:2186.0-2371.0`

## 11. Comissionamento, inspeção e manutenção dos internos
Na fase de comissionamento e nas inspeções de integridade, o foco deve ser confirmar não apenas a presença dos internos, mas sua **função hidrodinâmica real**. Com base nas fontes, os pontos críticos incluem:

- posicionamento e integridade do **defletor/dispositivo de entrada**;
- existência de rotas de drenagem adequadas para líquidos separados no topo/gás;
- instalação correta de **demister** e ausência de obstrução por parafina;
- estado de limpeza e fixação de **placas coalescedoras**;
- presença e integridade de **quebra-vórtice** nas saídas líquidas;
- condição de **placas perfuradas/quebra-ondas** em vasos sujeitos a slugs e movimento;
- funcionamento de drenos, coletores e sistemas de remoção de areia.

Quando o problema for recorrente, a manutenção não deve tratar apenas válvulas de controle e instrumentos; deve-se verificar se houve:

- deformação mecânica de internos;
- bypass de fluxo ao redor de coalescedores/demisters;
- entupimento parcial por sólidos/parafina;
- perda de área útil de separação por acúmulo no fundo;
- alteração da carga de entrada para condição fora da janela de projeto.

**Fontes da seção:** `petroles-004c2afadba7ea17c7dd7908:pNone:215456.0-215504.0`, `petroles-004c2afadba7ea17c7dd7908:pNone:215508.0-215548.0`, `petroles-4ee4bce16acf674505c8912d:pNone:617338.0-617375.0`, `petroles-004c2afadba7ea17c7dd7908:pNone:790828.0-790865.0`

## 12. Síntese para decisão de engenharia
Para avaliar o efeito dos internos no desempenho do separador trifásico, uma leitura útil é a seguinte:

- **internos de entrada** controlam a agressividade da carga e condicionam toda a separação subsequente;
- **internos tranquilizadores e quebra-ondas** estabilizam níveis, interface e comportamento do vaso frente a slugs e movimento offshore;
- **coalescedores** elevam a eficiência líquido-líquido por aumento do tamanho efetivo das gotas e redução de caminhos de sedimentação;
- **demisters** são a barreira final contra carryover de líquido para o gás, mas só funcionam bem dentro de sua janela de velocidade e limpeza;
- **quebra-vórtice** é decisivo para evitar gás na saída líquida e óleo na linha de água;
- **sistemas para sólidos e acesso para limpeza** são parte da eficiência de separação, porque preservam volume útil e evitam perda de função dos demais internos.

Em resumo, a eficiência de um separador trifásico em FPSO não deve ser julgada apenas por seu volume, pressão ou tempo de residência nominal. O desempenho real depende de como os internos reduzem turbulência, promovem coalescência, drenam corretamente as fases separadas e resistem às perturbações de vazão, espuma, emulsão, parafina, areia e movimento da unidade.

**Fontes da seção:** `petroles-004c2afadba7ea17c7dd7908:pNone:215418.0-215453.0`, `petroles-004c2afadba7ea17c7dd7908:pNone:215438.0-215481.0`, `petroles-004c2afadba7ea17c7dd7908:pNone:215456.0-215504.0`, `petroles-004c2afadba7ea17c7dd7908:pNone:215508.0-215548.0`, `petroles-004c2afadba7ea17c7dd7908:pNone:790828.0-790865.0`, `petroles-4ee4bce16acf674505c8912d:pNone:617338.0-617375.0`, `regis-282132e81add5278ef714ccc:pNone:2186.0-2371.0`, `regis-382370e69ec038894a313f3f:pNone:16.120-55.0`