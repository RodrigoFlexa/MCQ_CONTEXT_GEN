# Transferência e controle de tanques

## 1. Escopo técnico da faceta

Este documento consolida aspectos de **planejamento, sequência, alinhamento, bombeio, monitoramento e resposta a desvios** em operações de:

- enchimento e esvaziamento de tanques de carga;
- transferências internas entre tanques de carga e slop tanks;
- preparação de tanques para manutenção e retorno ao serviço;
- apoio operacional ao offloading, quando a transferência interna faz parte do preparo da carga.

O foco está em **como controlar a movimentação de fluidos entre tanques com segurança e eficiência**, preservando especificação do produto, evitando contaminação cruzada, sobrepressão, transbordo, migração indevida entre tanques e uso inadequado de linhas/sistemas auxiliares. As informações abaixo combinam conceitos gerais e lições de arranjos específicos de FPSO; portanto, **não devem ser tratadas como prescrição universal de projeto ou operação**.  

**Fontes-base da seção:** `petroles-004c2afadba7ea17c7dd7908:pNone:1901930.0-1901967.0`, `petroles-004c2afadba7ea17c7dd7908:pNone:1901334.0-1901375.0`, `anp-af6fd68d01f2fe2136ef14db:p57-60:27.0-15.0`, `anp-af6fd68d01f2fe2136ef14db:p84-90:14.0-8.0`, `anp-af6fd68d01f2fe2136ef14db:p116-118:10.0-24.0`, `anp-af6fd68d01f2fe2136ef14db:p117-122:16.0-15.0`, `regis-59a7abd3f86de4e909507930:pNone:397.60-432.60`

## 2. Função dos tanques de carga e slop no contexto operacional

Em FPSOs, os **tanques de carga** armazenam temporariamente os fluidos líquidos produzidos e já condicionados para expedição/offloading. No caso relatado para o FPSO CDSM, havia cinco tanques de carga principais para armazenamento do produto líquido destinado à exportação e dois **slop tanks** destinados a armazenar temporariamente misturas oleosas, água oleosa e resíduos associados, antes de tratamento ou destinação compatível com os limites ambientais e operacionais da unidade. O mesmo caso também mostra que a operação real pode desviar da filosofia originalmente preferida de exportação direta por duto, levando ao uso intensivo dos tanques de carga e, portanto, elevando a criticidade do sistema de transferência entre tanques.  

Do ponto de vista de operação, isso implica que:

1. **Tanque de carga não é apenas volume disponível**: ele é parte do controle de qualidade do produto, da logística de offloading e da segurança de processo.
2. **Slop tank não deve ser tratado como “volume livre genérico”**: ele tem papel de segregação operacional. Misturar indiscriminadamente slop, água e produto exportável pode gerar retrabalho, perda de especificação e aumento de risco.
3. **Transferência interna é função crítica**: ela serve para equalizar estoques, esgotar remanescentes, preparar entrada em tanque, concentrar produto para offloading ou remover mistura água/condensado de um tanque antes de manutenção.

**Fontes-base da seção:** `anp-af6fd68d01f2fe2136ef14db:p57-60:27.0-15.0`, `regis-59a7abd3f86de4e909507930:pNone:397.60-432.60`

## 3. Princípios de planejamento da transferência entre tanques

Antes de qualquer enchimento, esvaziamento ou transferência interna, a operação deve ser tratada como uma sequência coordenada entre:

- **tanque origem**;
- **tanque destino**;
- **linha selecionada**;
- **bomba ou modo de transferência**;
- **limites de nível, pressão e qualidade do fluido**;
- **condição de válvulas e estanqueidade**;
- **impacto na campanha seguinte**: manutenção, offloading, drenagem, segregação de slops ou retorno de tanque ao serviço.

A literatura operacional reunida nos trechos de Petrolês destaca dois passos prévios fundamentais:

### 3.1 Planejamento do alinhamento

O alinhamento deve ser planejado de forma explícita, com inspeção do caminho completo do fluido. Isso inclui verificar:

- quais válvulas **serão usadas** e se elas estão operáveis e destravadas;
- quais válvulas **não serão usadas** e se estão totalmente fechadas;
- se existem pontos cegos, raquetes, drenos, derivações, mangotes, linhas temporárias ou bloqueios mecânicos que alterem o trajeto esperado;
- se o sistema de medição do tanque está instalado e funcional;
- se respiradores/alívio de pressão e vácuo do tanque estão em condição de serviço.

### 3.2 Partida conservadora

Na colocação de um tanque em operação, o recebimento deve ser iniciado **lentamente**, com observação constante e verificação de vazamentos em juntas e conexões. Em outras palavras, a partida deve validar o alinhamento real no campo antes de se atingir regime de vazão elevado.

### 3.3 Definição da parada

Quando há meta de volume ou nível final, a parada pode ser planejada a partir da **tabela de arqueação/calibração do tanque** ou de um **fator volumétrico**. Se o fator do tanque for expresso em L/mm, a variação de nível aproximada associada a um volume transferido é:

- **Δh ≈ V / F**

onde:

- **Δh** = variação de nível;
- **V** = volume transferido;
- **F** = fator do tanque.

O tempo aproximado de bombeio pode ser estimado por:

- **t ≈ V / Q**

onde:

- **t** = tempo de bombeio;
- **Q** = vazão.

Essas relações são simples, mas operacionalmente relevantes para definir **nível de parada**, **hora estimada de término**, necessidade de vigilância reforçada perto do fim da operação e prevenção de overfill ou secagem excessiva de sucção.

**Fontes-base da seção:** `petroles-004c2afadba7ea17c7dd7908:pNone:1901930.0-1901967.0`

## 4. Sequência operacional típica para enchimento, esvaziamento e transferência interna

## 4.1 Enchimento de tanque

Uma sequência técnica coerente para enchimento inclui:

1. **Confirmar disponibilidade do tanque destino**
   - volume útil remanescente;
   - compatibilidade do fluido com o histórico do tanque;
   - condição do sistema de medição;
   - condição de ventilação/respiração e proteção P/V.

2. **Confirmar isolamento de rotas não desejadas**
   - fechamento de válvulas de linhas paralelas;
   - verificação de passagens indevidas conhecidas nas válvulas;
   - existência de raquetes ou bloqueios mecânicos em posição correta.

3. **Iniciar recebimento em baixa taxa ou com vigilância intensiva**
   - observar juntas, flanges, mangotes, acoplamentos e comportamento do nível;
   - confirmar se o nível sobe no tanque previsto, e somente nele.

4. **Evoluir para regime normal**
   - após validação de vazão, pressão, tendência de nível e ausência de vazamento.

5. **Aproximar a parada com antecedência**
   - reduzir margem de erro quando o nível estiver próximo do limite operacional;
   - confirmar continuamente a taxa de enchimento e o nível calculado/medido.

## 4.2 Esvaziamento de tanque

Para esvaziamento, a lógica se inverte, mas os riscos mudam:

- queda de pressão ou formação de vácuo se a ventilação/alívio falhar;
- perda de sucção da bomba;
- arraste de água, sedimento ou borra no final do esgotamento;
- maior probabilidade de desvio de fluxo por válvula passing ou alinhamento indevido.

O trecho de Petrolês ressalta que, em tanques com respiração obstruída ou sem proteção adequada, o esvaziamento pode produzir **amassamento/implosão** por vácuo. Logo, o controle de esvaziamento não é apenas hidráulico; ele depende do desempenho do sistema de ventilação e/ou válvulas de pressão e vácuo.

## 4.3 Transferência interna entre tanques de carga e slop

A transferência interna normalmente atende a um ou mais objetivos simultâneos:

- concentrar produto para offloading;
- remover mistura água/óleo ou água/condensado do tanque de carga;
- deslocar remanescente após offloading;
- esgotar tanque para inspeção/manutenção;
- resegregar produto fora de especificação;
- liberar determinado tanque sem interromper totalmente a produção.

Na prática, essa operação exige atenção especial a três pontos:

### a) Qualidade do fluido transferido

Misturas de água e condensado/óleo podem exigir envio para slop, não para tanque de exportação, a depender da especificação do produto e da capacidade posterior de tratamento.

### b) Integridade do trajeto

Se houver histórico de vazamento interno de válvulas ou migração entre tanques, a simples posição “fechada” no painel **não comprova isolamento efetivo**.

### c) Final da drenagem/stripping

O fim da transferência é o trecho mais sensível para:

- redução drástica de eficiência de bombeio;
- entrada de gás na sucção;
- aumento de incerteza sobre o que ainda resta no tanque;
- tentação operacional de improvisar novos caminhos para “tirar o resto”.

O caso do FPSO CDSM mostra precisamente esse cenário: uma operação de stripping do tanque 6C para slop tank ocorreu de forma satisfatória por dias, mas perdeu fortemente eficiência quando se aproximou do esgotamento. A partir daí, foram buscadas alternativas de alinhamento para retirar o remanescente.  

**Fontes-base da seção:** `petroles-004c2afadba7ea17c7dd7908:pNone:1901930.0-1901967.0`, `petroles-004c2afadba7ea17c7dd7908:pNone:1901334.0-1901375.0`, `regis-59a7abd3f86de4e909507930:pNone:397.60-432.60`

## 5. Controle de níveis, vazão e tempo de bombeio

A operação segura depende de combinar **medição real** com **previsão operacional**.

### 5.1 Nível

O nível deve ser acompanhado para:

- prevenir transbordo no tanque destino;
- evitar sucção de gás/ar no tanque origem;
- identificar comportamento anômalo, como subida em tanque não selecionado;
- inferir se a vazão efetiva é compatível com a esperada;
- detectar contaminação cruzada ou passagem por válvula supostamente fechada.

### 5.2 Vazão e tempo

A comparação entre vazão nominal da bomba e volume realmente transferido é um bom teste de plausibilidade. O caso resumido por REGIS é ilustrativo: foi observada forte perda de eficiência quando, em 7 horas, a transferência foi da ordem de 31 m³, apesar de a bomba de stripping ter capacidade muito superior em condições nominais. Para a operação, um desvio dessa magnitude sugere necessidade de investigar:

- baixa disponibilidade de líquido na sucção;
- entrada de gás;
- obstrução parcial;
- vazamento interno por válvulas;
- caminho hidráulico inadequado;
- recirculação ou retorno indesejado.

### 5.3 Consistência entre medições e balanço

Em qualquer transferência entre tanques, diferenças relevantes entre:

- volume bombeado;
- variação de nível do tanque origem;
- variação de nível do tanque destino;
- tendência observada em tanques vizinhos;

podem indicar:

- estanqueidade insuficiente em válvulas;
- comunicação entre tanques por headers;
- erro de alinhamento;
- migração por diferenciais de pressão;
- medição defeituosa;
- vazamento externo.

**Fontes-base da seção:** `petroles-004c2afadba7ea17c7dd7908:pNone:1901930.0-1901967.0`, `regis-59a7abd3f86de4e909507930:pNone:397.60-432.60`

## 6. Válvulas, headers, isolamento e risco de migração entre tanques

Um dos pontos mais críticos desta faceta é reconhecer que **a segurança da transferência depende tanto da condição real das válvulas quanto da lógica operacional**.

No relatório da ANP sobre o FPSO CDSM, foi identificado que algumas válvulas do sistema permitiam **passagem de fluido mesmo fechadas**, causando migração de conteúdo entre slop tanks e tanques de carga. As consequências operacionais incluíram:

- contaminação do produto armazenado com água;
- perda de especificação do condensado;
- necessidade de novas medidas para restaurar a condição do produto;
- criação de mudanças temporárias no sistema para manter a produção e permitir manutenção em tanques.

### 6.1 Implicações práticas

Quando há suspeita ou evidência de válvula “passing”, o operador não pode assumir que o inventário ficará segregado apenas pela posição da válvula. Nesses casos, tornam-se relevantes:

- bloqueios adicionais;
- válvulas manuais suplementares;
- check valves, quando aplicáveis ao sentido de fluxo pretendido;
- raqueteamento ou isolamento mecânico positivo;
- eliminação de rotas alternativas via headers comuns;
- replanejamento da transferência para minimizar diferencial de pressão favorável à migração.

### 6.2 Headers de fundo e rotas comuns

O arranjo com headers comuns no fundo dos tanques facilita a flexibilidade operacional, mas também aumenta o potencial de:

- transferência não intencional entre tanques;
- contaminação cruzada;
- retorno de produto a tanques já drenados ou em manutenção;
- falsa percepção de isolamento.

### 6.3 Gestão de mudança

Quando o sistema original deixa de atender devido a defeitos de válvula ou acoplamentos, a mudança de alinhamento, instalação de linhas temporárias, uso de mangotes, bombas submersíveis, válvulas manuais extras ou check valves deve ser tratada sob **gestão formal de mudança (MOC)**. O caso CDSM mostra que esse tipo de adaptação foi necessário para permitir entrada em tanques e continuidade de operação, mas também evidencia que arranjos temporários alteram profundamente os perigos do sistema.

**Fontes-base da seção:** `anp-af6fd68d01f2fe2136ef14db:p116-118:10.0-24.0`, `anp-af6fd68d01f2fe2136ef14db:p117-122:16.0-15.0`

## 7. Uso de bombas de carga, ballast e stripping: limites operacionais relevantes

No arranjo relatado pela ANP, a pump room reunia bombas de carga, bombas de água produzida, bombas de lastro e bomba de stripping. Isso mostra que a transferência entre tanques não ocorre isoladamente; ela convive com outros serviços marítimos e de processo, o que aumenta a necessidade de coordenação operacional.

### 7.1 Função da bomba de stripping

A bomba de stripping é vocacionada para:

- drenagem final;
- remoção de remanescentes dos tanques;
- transferência de pequenos volumes ou fases residuais.

No caso analisado, a bomba de stripping possuía válvula de alívio de pressão fornecida pelo fabricante, conectada para descarregar de volta à sucção da própria bomba. Esse detalhe é relevante porque indica que a bomba tinha proteção contra determinadas sobrepressões internas do conjunto, mas isso **não significa** que qualquer condição de bloqueio na linha, qualquer arranjo temporário ou qualquer componente associado estivesse automaticamente protegido.

### 7.2 Riscos de operar perto do esgotamento

Ao aproximar-se do fundo do tanque:

- a sucção pode perder estabilidade;
- a bomba pode operar com baixa eficiência;
- a pressão de descarga pode oscilar;
- o operador pode ser levado a alterar trim ou alinhamento para “buscar o resto” do conteúdo.

No evento descrito por REGIS, houve inclusive tentativa de alterar o trim para facilitar o bombeio do fluido remanescente no tanque 6C. Essa é uma interação importante entre operação de tanques e condição marítima da unidade: o ajuste do trim pode ajudar a posicionar o líquido remanescente, mas não elimina defeitos de válvula, limitações da linha ou inadequação do caminho de bombeio.

### 7.3 Bloqueio de descarga e sobrepressão

No acidente resumido por REGIS, durante a mudança de alinhamento, a válvula de descarga da bomba de stripping foi fechada mantendo-se a bomba em operação, elevando a pressão na linha de descarga. Ainda que a pressão tenha sido descrita como abaixo da pressão máxima de projeto da linha principal, houve vazamento em um flange próximo a uma raquete de baixa pressão fora de especificação para aquele serviço.

A lição operacional é clara: **a integridade do sistema é limitada pelo elo mais fraco do trecho efetivamente montado**, não pelo componente nominalmente mais robusto.

**Fontes-base da seção:** `anp-af6fd68d01f2fe2136ef14db:p84-90:14.0-8.0`, `regis-59a7abd3f86de4e909507930:pNone:397.60-432.60`

## 8. Linhas de gás inerte e outras linhas auxiliares: uso permitido versus uso desviado

Uma lição crítica dos materiais é a distinção entre:

- **linha projetada para determinada função**, e
- **linha improvisada ou temporariamente usada para outra função hidráulica**.

No caso CDSM, uma linha de secagem/purga associada ao sistema de gás inerte foi considerada em mudanças temporárias para transferência de conteúdo entre tanques, em conjunto com bombas submersíveis, mangotes e válvulas adicionais. O resumo de REGIS explicita que a linha de gás inerte **não havia sido projetada para ser usada com a bomba de stripping** no novo alinhamento proposto no dia do acidente.

### 8.1 Implicações de projeto e operação

Usar uma linha auxiliar para transferir líquido pode alterar:

- pressão admissível do trecho;
- compatibilidade de juntas, flanges e raquetes;
- drenabilidade e pontos de acúmulo de líquido;
- capacidade de bloqueio contra refluxo;
- filosofia de detecção de vazamento;
- classificação de risco do arranjo resultante.

### 8.2 Critério prático

Antes de usar uma linha originalmente associada a purga, secagem, inertização ou serviço auxiliar para movimentação de líquido, deve-se verificar pelo menos:

1. se a linha foi **projetada mecanicamente** para pressão, fluido, pulsação e regime de bombeio envolvidos;
2. se os componentes instalados no trecho têm a mesma **classe de pressão** requerida;
3. se há risco de **refluxo** para outros tanques ou sistemas;
4. se o novo arranjo compromete a função original do sistema de gás inerte;
5. se a mudança passou por **MOC**, análise de risco e atualização de documentação.

**Fontes-base da seção:** `anp-af6fd68d01f2fe2136ef14db:p116-118:10.0-24.0`, `anp-af6fd68d01f2fe2136ef14db:p117-122:16.0-15.0`, `regis-59a7abd3f86de4e909507930:pNone:397.60-432.60`

## 9. Pressão, vácuo e ventilação durante enchimento e esvaziamento

Embora esta faceta esteja centrada em transferência entre tanques, o controle do fluxo líquido é inseparável do controle da atmosfera do tanque.

Os trechos de Petrolês destacam que tanques de teto fixo e outros arranjos precisam de:

- **respiração desobstruída**; e/ou
- **válvulas de pressão e vácuo (P/V)**.

### 9.1 Durante o enchimento

Se o tanque recebe líquido, a fase gasosa precisa sair com segurança. Falhas nesse alívio podem produzir sobrepressão. Em tanques com vapores inflamáveis, os gases liberados podem requerer retenção/isolamento de chama por dispositivos tipo corta-chama/flame screen.

### 9.2 Durante o esvaziamento

Se o líquido sai e não há reposição adequada de fase gasosa, forma-se vácuo. A obstrução da respiração pode levar ao amassamento do tanque por implosão.

### 9.3 Durante drenagem de água ou preparação para manutenção

Ao drenar água de um tanque cheio para inertização/deslocamento, ou ao esvaziá-lo para manutenção, pode ser necessário abrir suspiros ou bocas de visita de forma controlada para evitar vácuo, conforme o texto de Petrolês descreve para esferas e tanques cilíndricos de GLP.

Mesmo que os exemplos originais envolvam outros tipos de tanque, o princípio de engenharia permanece: **o balanço gasoso do espaço de vapor deve acompanhar o balanço volumétrico do líquido**.

**Fontes-base da seção:** `petroles-004c2afadba7ea17c7dd7908:pNone:1901334.0-1901375.0`, `petroles-004c2afadba7ea17c7dd7908:pNone:1901930.0-1901967.0`

## 10. Preparação de tanques para manutenção e retorno ao serviço

Os trechos de Petrolês descrevem uma lógica de preparação de tanques que, adaptada ao contexto marítimo, permanece útil como referência conceitual.

## 10.1 Retirada de operação / liberação para manutenção

A sequência típica inclui:

1. **retirar o máximo de produto pelos meios normais**;
2. quando aplicável, usar água para elevar/deslocar o remanescente, desde que a separação posterior seja viável para o tipo de produto;
3. **raquetear/isolar** linhas de entrada e saída entre válvulas e tanque, reduzindo necessidade de reabrir linhas de processo depois;
4. instalar **exaustão/ventilação** conforme necessário;
5. em tanques específicos, posicionar componentes móveis em condição de manutenção;
6. somente após esvaziamento, drenagem, ventilação e isolamento adequados, liberar para manutenção.

### 10.1.1 Observação sobre uso de água

O texto menciona elevação com água para remoção de produto remanescente, especialmente em produtos claros. Em FPSOs, esse tipo de decisão deve considerar rigorosamente:

- compatibilidade com a especificação do produto;
- capacidade de tratar a mistura gerada;
- segregação em slop;
- risco de ampliar emulsão ou contaminantes;
- impacto na campanha seguinte.

## 10.2 Colocação do tanque novamente em operação

A volta ao serviço requer:

- inspeção interna final;
- confirmação de fechamento de aberturas e drenos;
- restabelecimento do sistema de medição;
- verificação completa do alinhamento;
- início do recebimento de forma lenta e observada;
- validação do funcionamento dos respiros/alívio.

Em termos práticos, a liberação do tanque não se encerra com a manutenção concluída: ela só se consolida quando a sequência de retorno comprova que o sistema voltou a operar sem vazamentos, sem bloqueios indevidos e com instrumentação disponível.

**Fontes-base da seção:** `petroles-004c2afadba7ea17c7dd7908:pNone:1901930.0-1901967.0`

## 11. Resposta a condições anormais durante a transferência

A documentação utilizada permite destacar um conjunto de sinais precoces que devem interromper ou reavaliar a operação:

### 11.1 Perda anormal de eficiência de bombeio

Exemplos:

- vazão real muito abaixo da nominal;
- aumento de tempo de transferência sem redução correspondente do inventário;
- necessidade crescente de manobras para manter sucção.

Possíveis causas:

- baixo nível na sucção;
- gás na linha;
- obstrução;
- recirculação;
- alinhamento incorreto;
- válvula passing;
- diferença de cota/trim insuficiente.

### 11.2 Pressão de descarga subindo rapidamente

Especialmente crítica quando combinada com:

- válvula de descarga fechada ou parcialmente bloqueada;
- alteração de alinhamento com a bomba em operação;
- presença de componentes temporários ou de menor classe de pressão.

### 11.3 Vazamento em flange, junta, raquete ou mangote

Deve ser tratado como evidência de perda de integridade do arranjo real. Não importa se parte do sistema principal suportaria maior pressão: o que falhou foi o conjunto montado para a operação.

### 11.4 Alarme de gás em pump room ou áreas adjacentes

No caso analisado, após o vazamento, detectores de gás foram acionados na casa de bombas. Como pump rooms são áreas classificadas e comunicam-se com fontes de vapor inflamável, a resposta deve ser imediata e compatível com a matriz de causa e efeito da unidade, inclusive isolamento, parada de equipamentos e gestão da ventilação/exaustão conforme a filosofia de segurança instalada.

**Fontes-base da seção:** `anp-af6fd68d01f2fe2136ef14db:p84-90:14.0-8.0`, `regis-59a7abd3f86de4e909507930:pNone:397.60-432.60`

## 12. Boas práticas consolidadas para transferência e controle de tanques

Com base no conjunto de fontes, as boas práticas mais robustas para esta faceta são:

1. **Planejar a operação pelo caminho completo do fluido**, não apenas pelo par origem-destino.
2. **Confirmar segregação real**, especialmente quando houver histórico de válvula passing.
3. **Usar medição de nível e balanço de volumes como verificação cruzada** do alinhamento.
4. **Iniciar e terminar a operação com vigilância reforçada**, pois partida e final de drenagem são fases críticas.
5. **Evitar improvisação hidráulica no fim do stripping** sem MOC e verificação mecânica completa.
6. **Não usar linha de sistema auxiliar para bombeio de líquido** sem validação de projeto, pressão, refluxo e integridade.
7. **Tratar slop como serviço de segregação**, não como destino universal para qualquer desvio operacional.
8. **Garantir ventilação/respiração/P-V adequados** durante enchimento e esvaziamento.
9. **Preparar manutenção com isolamento positivo e inspeção rigorosa** antes do retorno ao serviço.
10. **Reconhecer que a integridade do arranjo temporário é decisiva**: mangotes, raquetes, check valves e conexões temporárias podem se tornar o ponto limitante da operação.

**Fontes-base da seção:** `petroles-004c2afadba7ea17c7dd7908:pNone:1901930.0-1901967.0`, `petroles-004c2afadba7ea17c7dd7908:pNone:1901334.0-1901375.0`, `anp-af6fd68d01f2fe2136ef14db:p116-118:10.0-24.0`, `anp-af6fd68d01f2fe2136ef14db:p117-122:16.0-15.0`, `anp-af6fd68d01f2fe2136ef14db:p84-90:14.0-8.0`, `regis-59a7abd3f86de4e909507930:pNone:397.60-432.60`