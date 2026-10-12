# Dilúvio, spray e espuma em FPSOs/FSOs

## 1. Filosofia de proteção e definição de zonas de cobertura
Em unidades offshore, a filosofia de combate a incêndio por água e espuma não deve ser tratada como uma simples distribuição física de bicos ou mangueiras. A locação e o dimensionamento dos recursos de combate devem ser precedidos por avaliação qualitativa e quantitativa de riscos, considerando pelo menos: seleção dos focos de incêndio relevantes, características das chamas, radiação incidente, distribuição de temperatura em estruturas e análise de propagação do incêndio. Em termos práticos, isso significa que a **cobertura** de um sistema distribuído precisa nascer do cenário de fogo e da consequência esperada, e não apenas da geometria do convés ou do módulo.

Para sistemas zonados, os trechos indicam uma filosofia de **independência por zona**: cada área protegida possui seu próprio conjunto de válvula e acionamento. Isso é central para FPSOs/FSOs porque permite aplicar água ou solução de espuma apenas onde necessário, reduzindo consumo indevido de água, preservando disponibilidade hidráulica da rede e limitando impactos operacionais em áreas não afetadas.

Em termos funcionais, a estratégia é dupla:
- **controlar ou extinguir** o incêndio na área atingida;
- **evitar propagação** e **resfriar** ambiente/equipamentos expostos ao calor, reduzindo risco de colapso estrutural ou escalada do evento.

Essa lógica de projeto é especialmente importante para comparar três modos de proteção distribuída:
- **sprinkler**: atuação mais localizada;
- **dilúvio/water spray por bicos abertos**: atuação zonal e simultânea;
- **espuma**: atuação sobre combustível, com formação de manta/extinção superficial e resfriamento.

_Fuentes: `petroles-004c2afadba7ea17c7dd7908:pNone:3060535.0-3060574.0`, `petroles-004c2afadba7ea17c7dd7908:pNone:3060575.0-3060619.0`._

## 2. Diferença funcional entre sprinkler e dilúvio
### 2.1 Sprinkler
O sistema de sprinkler é descrito como contendo **bicos permanentemente fechados**, tipicamente com bulbo/ampola sensível à temperatura, instalados em linhas de água conectadas a uma **VGA (válvula de governo e alarme)**. A válvula permanece fechada até que pelo menos um elemento térmico se rompa, liberando fluxo de água **pontual** na área atingida.

A implicação de cobertura é importante: o sprinkler não descarrega necessariamente toda a zona ao mesmo tempo; ele tende a responder localmente ao aquecimento dos bicos. Nos trechos, esse arranjo é associado a **acomodações e corredores**, onde o objetivo é controlar/extinguir o incêndio, evitar propagação e refrigerar o ambiente para reduzir risco de colapso.

Cada zona protegida por sprinkler possui **VGA independente com sistema de acionamento próprio**. Em termos de engenharia, essa segregação facilita seletividade hidráulica e operacional.

### 2.2 Dilúvio / water spray por bicos abertos
O sistema de dilúvio é descrito com **bicos permanentemente abertos**, conectados a uma **ADV (válvula de dilúvio automática)**. A tubulação associada permanece sem descarga até que a ADV seja acionada, de forma **automática ou manual**, liberando água para todos os bicos daquela zona.

A consequência prática é que o dilúvio representa uma proteção **zonal e simultânea**, adequada quando se busca:
- cobrir integralmente uma área previamente definida;
- resfriar diversos equipamentos ao mesmo tempo;
- impedir propagação do fogo para áreas adjacentes;
- responder a cenários em que a atuação localizada de poucos bicos seria insuficiente.

Nos trechos, cada zona protegida por dilúvio também possui **ADV independente com acionamento próprio**, reforçando a filosofia de seletividade da proteção distribuída.

### 2.3 Leitura comparativa para FPSO/FSO
Sob a ótica de cobertura e acionamento:
- **sprinkler** é mais aderente a proteção localizada por aquecimento individual do bico;
- **dilúvio** é mais aderente a proteção de área/equipamento por descarga coletiva na zona.

Assim, em uma análise profissional, a principal pergunta de projeto não é apenas “qual sistema usar”, mas sim **se o cenário pede atuação local progressiva ou descarga total imediata na zona**.

_Fuentes: `petroles-004c2afadba7ea17c7dd7908:pNone:3060535.0-3060574.0`, `petroles-004c2afadba7ea17c7dd7908:pNone:3060560.0-3060599.0`._

## 3. Sistema de espuma: arquitetura, mecanismo e aplicação distribuída
O sistema de espuma é apresentado como destinado a **extinguir o incêndio**, **evitar sua propagação** e **refrigerar o combustível aquecido**. A arquitetura básica descrita inclui:
- fonte de água;
- reservatório de **LGE (líquido gerador de espuma)**, em tanque ou bombona;
- válvulas de bloqueio;
- proporcionador de linha;
- tubulação rígida ou flexível;
- esguicho de espuma ou bicos de descarga.

O mecanismo operacional descrito é o seguinte:
1. a água é liberada pelas válvulas de bloqueio;
2. passa pelo proporcionador de linha;
3. o proporcionador realiza o **arraste do LGE**;
4. forma-se a solução água + LGE;
5. a solução é **aerada** no esguicho ou nos bicos;
6. a espuma é lançada sobre o incêndio.

Quando aplicada sobre a superfície do combustível, a espuma forma uma **camada que isola o combustível do comburente**, promovendo extinção. Os trechos indicam uso normal para incêndios de **Classe A e B**; para a lógica de FPSO/FSO, o ponto mais relevante é a proteção de **combustíveis líquidos expostos**, onde a manta de espuma atua na supressão superficial e na limitação de reignição/propagação.

A descarga pode ocorrer por dois meios citados:
- **sprinkler/bicos**;
- **esguicho**.

Do ponto de vista da proteção distribuída, isso permite duas estratégias complementares:
- **espuma fixa distribuída**, por bicos em área definida;
- **espuma móvel/manual**, por esguicho, para ataque orientado pela equipe.

Em avaliação de cobertura, a decisão entre água pura e espuma depende fundamentalmente da natureza do combustível e do objetivo predominante da resposta:
- **resfriar estruturas/equipamentos expostos** → água/dilúvio tende a ser a lógica principal;
- **abafar superfície de combustível líquido** → espuma ganha relevância.

_Fuentes: `petroles-004c2afadba7ea17c7dd7908:pNone:3060575.0-3060619.0`, `petroles-004c2afadba7ea17c7dd7908:pNone:3060560.0-3060599.0`._

## 4. Cobertura e desempenho: o que os bicos e a hidráulica realmente mudam
Os trechos sobre aspersores e água nebulizada mostram que a eficácia de cobertura não depende apenas de “ter bicos instalados”, mas da combinação entre **geometria do bico, pressão, tamanho de gota, vazão, ângulo de cone, impulso do jato, ventilação e confinamento**.

### 4.1 Geometria do bico e distribuição
Nos bicos com defletor, a forma do defletor e a velocidade do jato determinam:
- tamanho das gotas;
- distribuição das gotas;
- ângulo do cone de aspersão.

Nos bicos com bulbo/ampola, a ruptura do elemento térmico libera água que colide com o defletor e é aspergida como chuva ou névoa. O texto também alerta que, em alguns arranjos, o próprio defletor e seus braços podem reduzir o momento axial da névoa e causar **distribuição irregular do fluxo**. Isso é tecnicamente relevante porque uma mesma vazão total não garante a mesma qualidade de cobertura sobre o alvo.

### 4.2 Pressão e tipo de aplicação
Os trechos classificam sistemas de água nebulizada em baixa, média e alta pressão, mas diversos valores numéricos estão suprimidos. Ainda assim, a relação qualitativa é clara:
- pressão mais elevada favorece atomização em gotas menores;
- gotas menores aumentam área de contato, absorção de calor e geração de vapor;
- isso pode reduzir consumo de água e danos por encharcamento em comparação com sprinkler/dilúvio convencionais.

Por outro lado, os próprios textos indicam que sistemas de alta pressão podem implicar **maior custo e maior exigência de tubulações/bombas especiais**, o que afeta decisões de retrofit e manutenção ao longo da vida do FPSO.

### 4.3 Tamanho de gota e tipo de incêndio
Os trechos afirmam que, para água nebulizada:
- gotas menores são especialmente importantes para extinção de incêndios **Classe B**;
- gotas maiores tendem a ser mais eficazes em incêndios **Classe A**.

Isso reforça um ponto de projeto: **não existe “spray universal”**. A cobertura requerida depende do combustível, do confinamento e do mecanismo dominante de extinção desejado.

### 4.4 Confinamento e ventilação
O desempenho da água nebulizada é fortemente afetado por:
- efeito do confinamento;
- dinâmica da mistura;
- ventilação/trocas de ar do ambiente.

Os trechos mencionam testes em que sistemas com dois fluidos foram mais sensíveis à ventilação do que sistemas com um fluido. Em ambientes confinados, como espaços de máquinas ou enclausuramentos, o efeito térmico e a expansão de vapor tendem a favorecer a atuação do sistema. Já em ambientes com ventilação relevante ou perda de contenção da névoa, a eficácia pode cair.

### 4.5 Água nebulizada como alternativa em certos cenários
Os textos colocam a água nebulizada como alternativa aos agentes gasosos em alguns contextos, destacando:
- uso limitado de água;
- grande área de atuação por vaporização das gotas;
- menor dano por água em comparação com sistemas tradicionais de maior descarga;
- melhor adequação a áreas ocupadas em relação a certos agentes gasosos.

Para fins desta faceta, o ponto central é que a **cobertura por spray** não pode ser avaliada apenas por área geométrica: é preciso considerar como o spray chega ao fogo, como interage com o ambiente e se o mecanismo predominante é resfriamento, deslocamento local de oxigênio por vapor ou isolamento do combustível.

_Fuentes: `petroles-004c2afadba7ea17c7dd7908:pNone:3060875.0-3060910.0`, `petroles-004c2afadba7ea17c7dd7908:pNone:3060860.0-3060891.0`, `petroles-004c2afadba7ea17c7dd7908:pNone:3060575.0-3060619.0`, `petroles-004c2afadba7ea17c7dd7908:pNone:3060153.0-3060207.0`._

## 5. Sistemas de um fluido e dois fluidos: implicações para cobertura, acionamento e manutenção
Os trechos sobre água nebulizada descrevem duas arquiteturas principais.

### 5.1 Sistema com um fluido
No arranjo com um fluido, usa-se água como agente extintor principal, podendo haver gás apenas como meio de pressurização/acionamento em sistemas pré-engenheirados. O texto descreve exemplos em que:
- um comando abre a válvula do cilindro de gás;
- o gás pilota a válvula de descarga de água;
- o tanque ou cilindros de água são pressurizados;
- a água segue para os bicos do ambiente protegido.

Há ainda indicação de:
- pressostatos para confirmar êxito do acionamento e passagem do gás piloto;
- válvula de alívio/disco de ruptura contra sobrepressão;
- possibilidade de **acionamento manual** em caso de falta de energia;
- reposição de água e substituição do cilindro de gás após disparo.

Essa arquitetura mostra que, mesmo em sistemas distribuídos, o desempenho não depende só dos bicos: depende também da **integridade da cadeia de acionamento**.

### 5.2 Sistema com dois fluidos
Nos sistemas com dois fluidos, água e ar comprimido/nitrogênio são misturados no interior do bico, e a quebra do jato produz as gotas. Os textos destacam como possíveis vantagens:
- maior controle sobre distribuição do tamanho de gota, ângulo de cone, impulso da névoa e taxa de descarga;
- menor probabilidade de entupimento, por conta de orifícios maiores;
- manutenção facilitada por operar em baixa pressão.

Como limitações, os trechos indicam:
- necessidade de duas linhas/suprimentos;
- maior custo do sistema;
- impulso menor da névoa devido à baixa pressão de descarga;
- maior sensibilidade às condições de ventilação em alguns testes comparativos.

Para avaliação profissional, isso significa que a decisão entre um e dois fluidos precisa considerar **não apenas extinção nominal**, mas também disponibilidade de utilidades, robustez frente à ventilação do compartimento, manutenção e risco de obstrução.

_Fuentes: `petroles-004c2afadba7ea17c7dd7908:pNone:3060875.0-3060910.0`, `petroles-004c2afadba7ea17c7dd7908:pNone:3060927.0-3060964.0`, `petroles-004c2afadba7ea17c7dd7908:pNone:3060946.0-3060985.0`._

## 6. Acionamento zonal e coordenação operacional com a emergência
Nos sistemas descritos, o **acionamento por zona** é o elemento central da proteção distribuída:
- sprinkler: cada zona com VGA própria;
- dilúvio: cada zona com ADV própria;
- água nebulizada pré-engenheirada: válvulas direcionais/de seção e lógica de comando por compartimento.

Os trechos também trazem um exemplo útil para análise operacional em ambientes com predominância de equipamentos elétricos. Nesse caso, são descritas tubulações secas pressurizadas com ar; o rompimento do bulbo gera alarme de baixa pressão na sala de controle; o operador avalia a situação por CCTV e decide sobre envio de equipe, uso de extintores portáteis ou acionamento do sistema fixo. No exemplo, antes da liberação de água, realiza-se o **desligamento do barramento afetado**, depois a partida da bomba e a abertura da válvula de seção do compartimento.

Tecnicamente, esse exemplo ilustra quatro princípios relevantes para FPSO/FSO:
1. **seletividade de descarga**: água somente na área afetada;
2. **coordenação com isolamento elétrico/processo** antes da aplicação, quando aplicável;
3. **preservação da disponibilidade hidráulica** para a resposta real;
4. **prevenção de disparo indevido em área energizada**, em certos arranjos.

Embora o foco desta faceta não seja detecção, a mensagem operacional é clara: o sistema distribuído de água/espuma precisa estar coerente com a lógica de emergência da unidade, incluindo isolamento de energia ou de seção protegida quando isso fizer parte do arranjo aprovado.

_Fuentes: `petroles-004c2afadba7ea17c7dd7908:pNone:3060535.0-3060574.0`, `petroles-004c2afadba7ea17c7dd7908:pNone:3060927.0-3060964.0`, `petroles-004c2afadba7ea17c7dd7908:pNone:3060946.0-3060985.0`._

## 7. Comissionamento, testes, inspeção e integridade: o que os trechos permitem afirmar
Os trechos não fornecem rotinas completas nem periodicidades de inspeção, mas permitem identificar pontos críticos de integridade para sistemas distribuídos de água e espuma.

### 7.1 Itens críticos de prontidão
Da arquitetura descrita, dependem diretamente da prontidão operacional:
- independência funcional das válvulas de zona (VGA/ADV);
- integridade de linhas piloto, pressostatos e comandos manuais;
- disponibilidade do meio pressurizante, quando aplicável;
- condição dos bicos, defletores e elementos térmicos;
- qualidade da água de suprimento;
- condição de filtros e passagens internas dos bicos, especialmente em sistemas de orifício reduzido.

### 7.2 Qualidade da água e risco de obstrução
No arranjo de ensaio descrito, foi instalado **filtro na linha de suprimento** para garantir a qualidade da água. Isso é particularmente relevante em sistemas de névoa/aspersão fina, nos quais pequenos orifícios são mais sensíveis a obstrução. Os próprios trechos destacam que sistemas de dois fluidos tendem a ser menos propensos a entupimento por possuírem orifícios maiores.

### 7.3 Restauração após disparo
Nos exemplos com tanque/cilindros e gás piloto, após o acionamento é necessário:
- desenergizar/segregar o sistema conforme o arranjo;
- repor a água até o nível inicial;
- substituir cilindros de gás utilizados;
- restaurar as condições de prontidão.

### 7.4 Ensaios e validação
Os textos citam ensaios de campo e protocolos de teste para water mist, além de um arranjo experimental com bicos instalados no teto para proteção localizada de painel elétrico. Para comissionamento e testes funcionais, os trechos sustentam a importância de verificar pelo menos:
- abertura correta da válvula da zona/compartimento;
- partida da bomba/unidade de pressurização;
- chegada do agente aos bicos previstos;
- seletividade do disparo apenas na área pretendida;
- coerência entre comando, isolamento operacional e aplicação do agente.

_Fuentes: `petroles-004c2afadba7ea17c7dd7908:pNone:3060875.0-3060910.0`, `petroles-004c2afadba7ea17c7dd7908:pNone:3060927.0-3060964.0`, `petroles-004c2afadba7ea17c7dd7908:pNone:3060946.0-3060985.0`._

## 8. Critérios práticos de decisão para água, dilúvio/spray e espuma
Com base nos trechos, uma leitura profissional coerente para FPSO/FSO é:

### 8.1 Quando a lógica favorece dilúvio/spray de água
Favorece-se dilúvio/spray quando o objetivo principal é:
- resfriar equipamentos ou estruturas expostas ao calor;
- reduzir propagação do incêndio para áreas vizinhas;
- cobrir simultaneamente toda uma zona definida.

### 8.2 Quando a lógica favorece espuma
Favorece-se espuma quando o foco é:
- atuar sobre a superfície de combustível;
- formar manta de isolamento entre combustível e comburente;
- extinguir/incapacitar incêndios superficiais em combustíveis líquidos.

### 8.3 Quando a lógica favorece aspersão fina/água nebulizada
Favorece-se aspersão fina/água nebulizada quando se busca, conforme o cenário validado:
- alta área de contato térmico com menor consumo de água;
- menor dano por água do que sistemas convencionais de maior descarga;
- proteção de compartimentos onde confinamento e dinâmica térmica favoreçam o mecanismo de supressão.

### 8.4 O critério transversal
Independentemente do agente, o critério transversal mais importante é: **a cobertura deve ser compatível com o cenário de incêndio, o combustível, o confinamento, a ventilação e a lógica de acionamento da zona**.

_Fuentes: `petroles-004c2afadba7ea17c7dd7908:pNone:3060535.0-3060574.0`, `petroles-004c2afadba7ea17c7dd7908:pNone:3060575.0-3060619.0`, `petroles-004c2afadba7ea17c7dd7908:pNone:3060153.0-3060207.0`, `petroles-004c2afadba7ea17c7dd7908:pNone:3060946.0-3060985.0`._

## 9. Síntese técnica
Para esta faceta, os trechos sustentam uma visão clara:
- **dilúvio** é proteção distribuída por zona com bicos abertos e descarga simultânea;
- **sprinkler** é proteção localizada com bicos fechados e atuação térmica individual;
- **espuma** combina água + LGE + aeração para formar manta extintora e refrigerante sobre o combustível;
- a **cobertura efetiva** depende de cenário, zona, bicos, pressão, ventilação, confinamento e seletividade de acionamento;
- em ambientes sensíveis, especialmente elétricos, a estratégia de aplicação do agente precisa ser coordenada com o isolamento operacional;
- integridade de válvulas de zona, linhas piloto, filtros, bicos e meios de pressurização é parte essencial da confiabilidade do sistema ao longo da vida operacional.

_Fuentes: `petroles-004c2afadba7ea17c7dd7908:pNone:3060535.0-3060574.0`, `petroles-004c2afadba7ea17c7dd7908:pNone:3060575.0-3060619.0`, `petroles-004c2afadba7ea17c7dd7908:pNone:3060875.0-3060910.0`, `petroles-004c2afadba7ea17c7dd7908:pNone:3060927.0-3060964.0`, `petroles-004c2afadba7ea17c7dd7908:pNone:3060946.0-3060985.0`._