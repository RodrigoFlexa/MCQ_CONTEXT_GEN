# Capacidade e arranjo de rigging

## 1. Finalidade técnica da verificação de capacidade e arranjo

Na movimentação de cargas em FPSOs/FSOs, a verificação técnica do rigging não se resume a confirmar se o guindaste “levanta o peso”. O arranjo precisa assegurar que **carga, pontos de pega, acessórios, equipamento de içamento, trajetória e área de assentamento** sejam compatíveis entre si e com as condições operacionais. Para movimentações críticas, o material disponível indica a necessidade de um **plano de movimentação de cargas / plano de rigging**, acompanhado de **análise de risco da tarefa**. Esse planejamento deve considerar, no mínimo:

- peso da carga;
- localização e posição da carga;
- capacidade e posição do equipamento de guindar;
- configuração do equipamento dentro da respectiva tabela de carga, incluindo exemplos como **ângulo de inclinação** e **comprimento de lança**;
- necessidade de máquinas de auxílio;
- características do piso;
- peças de auxílio para distribuição de esforços, cabos de aço, cintas sintéticas e acessórios de movimentação;
- área de içamento e de assentamento da carga, incluindo os obstáculos mais proeminentes.

Esse conjunto de verificações define a **viabilidade técnica do arranjo** e evita que a seleção de acessórios e pontos de sustentação seja feita apenas por aproximação visual ou experiência informal.  
**Fontes:** `petroles-004c2afadba7ea17c7dd7908:pNone:1994395.0-1994444.0`

## 2. Elementos mínimos de verificação do load path

Pelos trechos disponíveis, a lógica de verificação deve acompanhar todo o **caminho de carga**: da carga propriamente dita até o equipamento de içamento. Na prática, isso envolve verificar:

1. **A carga**: massa conhecida, posição, estabilidade, ponto de equilíbrio e ausência de materiais soltos sobre ela.
2. **Os pontos de sustentação da carga**: pontos de pega, padeyes, ganchos de fixação, eixos ou demais elementos que recebem corte, flexão ou pressão superficial.
3. **Os acessórios intermediários**: eslingas, cabos de aço, manilhas, patescas/dispositivos distribuidores de esforços, links e outros acessórios aplicáveis.
4. **Os elementos de desvio e transmissão**: polias, tambores, ganchos e seus eixos.
5. **O equipamento principal**: guindaste, guincho, monovia, ponte rolante ou equivalente, sempre conforme sua configuração real de operação e respectiva tabela de carga.

O material também indica que a linha de içamento deve permanecer **na vertical durante a movimentação** e que **não é permitido puxar ou arrastar lateralmente cargas sobre o piso utilizando equipamentos de guindar**. Isso é tecnicamente relevante porque cargas laterais e desalinhamentos alteram a distribuição de esforços no sistema e podem levar a solicitações não previstas em lança, cabo, gancho, moitão, acessórios e pontos de pega.  
**Fontes:** `petroles-004c2afadba7ea17c7dd7908:pNone:1994395.0-1994444.0`

## 3. Verificação da capacidade dos componentes do rigging

### 3.1 Comparação entre cargas da operação e limites admissíveis

Um caso técnico disponível, relativo à instalação de árvore submarina por cabo de guindaste, mostra uma abordagem de verificação aplicável como referência conceitual para operações offshore mais exigentes: foi necessário analisar **padeye, manilha e sling** originalmente projetados para a carga, comparando-os com as **cargas de instalação**. A análise também considerou:

- limites do guindaste;
- capacidade de içamento em determinadas condições oceânicas;
- respostas hidrodinâmicas da embarcação;
- características de RAO da embarcação;
- características de padeyes, slings, wire e posição do guindaste;
- load chart;
- possibilidade de **cargas dinâmicas** e de **snap loads**.

Nesse exemplo, foram analisadas tanto a **entrada do equipamento na água** quanto a fase de descida até o fundo, com o objetivo de assegurar que as cargas de instalação não excedessem os limites admissíveis de cada componente do sistema. Para FPSOs/FSOs, a lição técnica principal é que a verificação de capacidade do rigging deve ser feita para a **condição real de operação**, não apenas para o peso estático nominal da carga.

### 3.2 Implicações para a seleção do arranjo

Assim, a seleção e verificação técnica do arranjo de rigging devem confrontar, para cada componente:

- a carga esperada na operação;
- a configuração geométrica efetiva do içamento;
- a posição/configuração do equipamento de içar no load chart;
- as condições ambientais e dinâmicas relevantes;
- os limites admissíveis do componente analisado.

Em operações offshore, isso é particularmente importante quando a movimentação envolve embarcações, mar agitado, penetração na água, mudanças de empuxo, oscilações da carga ou risco de amplificação dinâmica.  
**Fontes:** `petroles-004c2afadba7ea17c7dd7908:pNone:475500.0-475556.0`, `petroles-004c2afadba7ea17c7dd7908:pNone:1994395.0-1994444.0`

## 4. Arranjo de rigging: compatibilidade entre cabo, polia, ponto de içamento e estrutura

Um trecho de projeto de um sistema estrutural inclinável, embora não descreva uma instalação de FPSO, é útil para ilustrar como a verificação do rigging deve abranger o **conjunto estrutural** e não apenas o equipamento principal.

### 4.1 Exemplo de cadeia de verificação

No exemplo, o sistema de içamento era composto por:

1. cabo de aço;
2. patesca/distribuidor de forças;
3. polia de içamento;
4. eixo do ponto de içamento;
5. guincho;
6. elementos auxiliares de acesso e trava;
7. gancho de fixação.

As dimensões do cabo indicado pelo fabricante do guincho foram verificadas segundo recomendação do fabricante do cabo. Considerando solicitação correspondente à metade da tensão máxima de içamento devido à presença da patesca e adotando **fator de segurança de cinco para o tipo de serviço**, o estudo concluiu que um cabo de aço 6x25 FILLER de 8 mm atendia aos requisitos do sistema. No mesmo exemplo, foram indicadas cargas máximas calculadas de **400 kgf para o cabo** e **800 kgf para a patesca**.

O aspecto mais importante, para fins de rigging, é o método: a verificação não ficou limitada ao cabo, mas se estendeu a todos os elementos que recebem carga.

### 4.2 Verificação localizada de componentes estruturais

No mesmo caso:

- o **eixo do ponto de içamento** foi reconhecido como elemento submetido a **corte direto e flexão**, sendo a flexão o caso mais crítico;
- o **gancho de fixação** foi projetado especificamente para sustentar o cabo que vinha da patesca;
- na **polia de içamento**, o eixo foi escolhido fixo para evitar esforços alternantes;
- o diâmetro da polia foi definido segundo critério vinculado ao diâmetro do cabo: **diâmetro mínimo da polia igual a 26 vezes o diâmetro do cabo**, com **recomendação de 39 vezes** o diâmetro do cabo;
- o cubo da polia foi dimensionado para não exceder **pressão superficial de 40 a 70 kg/cm²**, limite indicado para o material da bucha utilizado no exemplo.

### 4.3 Aplicação prática ao contexto de FPSO/FSO

Como princípio técnico, esse exemplo mostra que a verificação do arranjo de rigging deve incluir:

- compatibilidade entre **cabo e polia**;
- avaliação de **pinos/eixos** quanto a corte e flexão;
- avaliação de **ganchos, padeyes e conexões** como elementos estruturais carregados;
- conferência de dispositivos usados para **distribuição de esforços**;
- coerência entre o arranjo selecionado e o **tipo de serviço**.

Em outras palavras, a seleção do acessório não pode ser dissociada da verificação do ponto onde ele trabalha e do elemento estrutural que o recebe.  
**Fontes:** `regis-254373af6cf879ea64c54a1f:pNone:6600.0-6973.0`, `regis-254373af6cf879ea64c54a1f:pNone:6835.0-7077.0`

## 5. Critérios práticos para seleção de acessórios e pontos de pega

Com base nos trechos fornecidos, a preparação do arranjo deve observar os seguintes critérios operacionais e de integridade:

### 5.1 Posicionamento da pega na carga

A carga deve ser **presa junto ao seu ponto de equilíbrio**. Esse requisito é central para evitar inclinação imprevista, rotação, instabilidade e redistribuição não planejada de esforços no conjunto de rigging. Quando o ponto de pega não coincide adequadamente com o equilíbrio da carga, aumenta a probabilidade de:

- giro não controlado;
- colisão com estruturas, tubulações ou piso;
- necessidade indevida de correção manual durante a movimentação;
- aumento da criticidade do uso de cabo guia.

### 5.2 Controle de materiais soltos e configurações instáveis

Antes de içar a carga, deve-se verificar se **não há material solto em cima dela** com risco de queda. Além disso, durante içamento ou descarregamento de cargas amarradas, não é permitido tocar o interior de feixes de peças, tubos, perfis, spools, sucatas ou outros materiais com empilhamento instável e risco de aprisionamento ou esmagamento de dedos e mãos.

Esse requisito interfere diretamente na decisão de liberar ou não o içamento, pois uma carga aparentemente “dentro do peso” pode continuar insegura por causa de sua configuração física.

### 5.3 Arestas cortantes e compatibilidade do acessório

Não é permitido movimentar cargas com **arestas cortantes** usando dispositivo de içamento **não metálico**, exceto quando as arestas estiverem protegidas por material resistente. Do ponto de vista de verificação técnica, isso significa que a capacidade nominal do acessório não basta: é necessário avaliar também a **compatibilidade física** entre acessório e geometria da carga.

### 5.4 Recipientes, caixas metálicas e contêineres

O material informa requisitos específicos para recipientes:

- o **peso do recipiente** deve estar indicado em local visível, de forma clara, legível e indelével;
- para **caixas metálicas e contêineres**, devem ser utilizadas eslingas com comprimento mínimo equivalente à maior dimensão da tampa da caixa;
- se a tampa for removível, o **peso da tampa** também deve estar indicado na face superior;
- se a tampa tiver peso superior ao valor-limite indicado no procedimento de origem, sua abertura deve ser feita com uso de equipamento de içar;
- caixas e contêineres com tampa de abertura vertical devem possuir **dispositivos de travamento** da tampa na posição aberta.

Esses pontos mostram que a seleção do rigging precisa considerar não apenas a massa total do item, mas também as **subpartes móveis** e os componentes que podem se tornar cargas independentes durante a operação.  
**Fontes:** `petroles-004c2afadba7ea17c7dd7908:pNone:1994395.0-1994444.0`

## 6. Verificações pré-uso e inspeção de equipamentos e acessórios

### 6.1 Condição de liberação para operação

Os equipamentos de guindar somente devem operar com:

- sistemas de segurança operacionais habilitados;
- plano de manutenção em dia;
- inspeção em dia;
- testes funcionais em dia.

Além disso, o material indica que os equipamentos de guindar devem ser submetidos a **testes de carga periódicos** conforme indicação do fabricante. Antes do início do trabalho, dispositivos de segurança como **fins de curso, travas do gancho e identificadores de peso da carga** devem ser testados.

### 6.2 Inspeção de cabos de aço

No exemplo técnico do sistema de içamento, o cabo de aço é tratado como o elemento mais crítico do sistema, porque se desgasta e gradualmente perde capacidade de trabalho ao longo da vida útil. São recomendados dois tipos de inspeção:

- **inspeção diária/frequente**, feita pelo operador antes de cada jornada, para detectar problemas de ajuste que possam prejudicar a operação;
- **inspeção periódica**, mais detalhada e submetida a procedimentos estritos.

Uma inspeção frequente pode levar o componente à inspeção periódica, dependendo da severidade da avaria encontrada.

A inspeção do cabo deve ser feita **sem carga e em repouso**, concentrando-se nas seções submetidas a esforços repentinos e nos pontos onde a carga inicial de cada levantamento é aplicada. O texto identifica como **zonas críticas**: **polias, ganchos e tambores**.

Os indícios de falha procurados incluem:

- desgaste superficial;
- oxidação;
- corrosão.

O trecho ainda recomenda limpeza prévia com pano limpo, escova de arames e produtos desengraxantes para favorecer a inspeção visual.

### 6.3 Implicação para a seleção técnica

Para fins de seleção e verificação de acessórios, a consequência prática é que um componente não deve ser considerado apto apenas porque “é o modelo correto”; ele precisa estar **em condição operacional compatível** com a manobra planejada.  
**Fontes:** `petroles-004c2afadba7ea17c7dd7908:pNone:1994395.0-1994444.0`, `regis-254373af6cf879ea64c54a1f:pNone:6835.0-7077.0`

## 7. Controles operacionais que afetam diretamente o arranjo de rigging

Embora o foco desta faceta seja capacidade e arranjo, alguns controles de execução são inseparáveis da verificação técnica porque evitam que um arranjo correto seja degradado por uma execução incorreta.

### 7.1 Isolamento e zona de exclusão

A área de movimentação da carga deve ser **isolada**. Não é permitida a permanência de qualquer pessoa:

- **sob a carga suspensa**;
- **dentro do raio de giro** da carga.

### 7.2 Continuidade do ciclo de içamento

Uma vez içada a carga, o ciclo deve ser **completado**, não a deixando suspensa. Essa orientação reduz exposição prolongada a falhas de retenção, mudança de vento, perda de controle ou interferência operacional.

### 7.3 Estabilização e uso de cabo guia

Não é permitido utilizar qualquer parte do corpo para estabilizar cargas suspensas. Cordas não podem ser usadas para içar ou puxar cargas; seu uso deve ficar restrito a **cabo guia**. Quando houver possibilidade de colisão ou giro da carga durante a movimentação, o uso do cabo guia é **obrigatório**.

Na movimentação em convés de embarcações, a dispensa do uso do cabo guia deve estar baseada em **análise de risco**, permanecendo obrigatória a fixação do cabo na carga a ser movimentada. O texto ainda estabelece que:

- não é permitida a fixação do cabo guia com a carga suspensa;
- deve ser utilizado dispositivo adequado para permitir o alcance do cabo guia fora da área de giro da carga suspensa;
- o comprimento do cabo guia deve manter o auxiliar em distância segura do raio de movimentação;
- o cabo guia deve possuir diâmetro tal que, se ficar preso acidentalmente em obstáculo, **se rompa sem ocasionar sobrecarga no sistema de içamento**.

### 7.4 Visibilidade limitada

Ao executar manobras que não permitam a visualização de obstáculos, é obrigatória a presença de **sinalizador**. Em termos de rigging, isso significa que a aprovação do arranjo depende também da capacidade de controlar a trajetória prevista sem introduzir esforços, choques ou correções improvisadas.  
**Fontes:** `petroles-004c2afadba7ea17c7dd7908:pNone:1994395.0-1994444.0`

## 8. Decisões de liberação, suspensão ou reprovação do arranjo

Com base nos materiais disponíveis, o arranjo de rigging não deve ser liberado quando houver uma ou mais das seguintes condições:

- peso, localização ou posição da carga não suficientemente definidos no plano;
- incompatibilidade entre a configuração real do equipamento e sua tabela de carga;
- necessidade de máquinas auxiliares ou peças de distribuição de esforços não contemplada no planejamento;
- características de piso, área de içamento ou área de assentamento não avaliadas;
- obstáculos proeminentes sem trajetória previamente definida;
- sistemas de segurança, inspeções, manutenção ou testes funcionais fora de conformidade;
- necessidade de puxar lateralmente a carga ou de operar com linha de içamento fora da vertical;
- uso de acessório não metálico em aresta cortante sem proteção adequada;
- presença de material solto sobre a carga;
- impossibilidade de controle seguro da carga girante/colidente;
- incerteza quanto à capacidade admissível de padeye, manilha, sling, wire, polia, eixo ou guindaste diante das cargas estáticas e dinâmicas da operação.

Em operações offshore mais sensíveis, o arranjo também deve ser reavaliado quando as condições ambientais ou dinâmicas indicarem potencial de aumento de carga, inclusive em fases como entrada na água e descida subsea.  
**Fontes:** `petroles-004c2afadba7ea17c7dd7908:pNone:1994395.0-1994444.0`, `petroles-004c2afadba7ea17c7dd7908:pNone:475500.0-475556.0`, `regis-254373af6cf879ea64c54a1f:pNone:6835.0-7077.0`

## 9. Síntese técnica

A faceta de **capacidade e arranjo de rigging** pode ser resumida em quatro verificações integradas:

1. **A carga é conhecida, estável e pegada no ponto de equilíbrio?**
2. **Cada componente do caminho de carga suporta a solicitação real da operação, inclusive efeitos dinâmicos relevantes?**
3. **A geometria do arranjo é compatível com cabo, polia, pontos de sustentação, área e trajetória?**
4. **Equipamentos e acessórios estão inspecionados, testados e operando com dispositivos de segurança habilitados?**

Quando uma dessas respostas é negativa, a falha não é apenas operacional: ela compromete a integridade do próprio arranjo de rigging.  
**Fontes:** `petroles-004c2afadba7ea17c7dd7908:pNone:1994395.0-1994444.0`, `petroles-004c2afadba7ea17c7dd7908:pNone:475500.0-475556.0`, `regis-254373af6cf879ea64c54a1f:pNone:6600.0-6973.0`, `regis-254373af6cf879ea64c54a1f:pNone:6835.0-7077.0`