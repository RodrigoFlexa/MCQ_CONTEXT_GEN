# Distribuição e recomposição elétrica

## 1. Premissas e limites de aplicação
Em sistemas elétricos de unidades offshore com geração própria, a arquitetura do switchboard e dos barramentos condiciona diretamente três resultados operacionais: a extensão da perda de carga em caso de falta, a facilidade de transferência entre seções e a velocidade/segurança da recomposição após perda parcial ou total de energia. Os trechos utilizados nesta síntese vêm de literatura de proteção de sistemas de potência e de estudos navais/industriais; portanto, o conteúdo abaixo deve ser lido como base técnica de engenharia e operação, e não como requisito normativo específico de FPSO.

Em termos gerais, quanto maior o número de circuitos conectados a um mesmo barramento, maior a consequência potencial de uma falta de barramento. A literatura usada indica que, quando há mais de seis a oito circuitos envolvidos, é comum dividir o barramento por meio de um disjuntor de interligação (bus tie) ou adotar arranjos que minimizem a quantidade de circuitos que precisam ser abertos para isolar a falta.

**Fontes da seção:** `petroles-004c2afadba7ea17c7dd7908:pNone:2430672.0-2430732.0`, `petroles-004c2afadba7ea17c7dd7908:pNone:2430734.0-2430788.0`

## 2. Arquiteturas de barramentos mais relevantes para transferência e recomposição
### 2.1 Barramento simples com disjuntor simples
É o arranjo mais básico, simples e econômico. Sua principal limitação é a baixa flexibilidade operacional:

- uma falta no barramento exige a abertura de todos os circuitos conectados;
- problema ou manutenção em um disjuntor normalmente retira aquele circuito de serviço;
- a vantagem é a simplicidade de proteção, inclusive com aplicação relativamente direta de proteção diferencial cobrindo todo o barramento.

Esse arranjo pode ser aceitável quando a simplicidade tem prioridade e a indisponibilidade total da seção, em caso de falta de barramento, é tolerável.

### 2.2 Barramentos simples interligados por bus tie
É uma extensão do arranjo anterior e tem relevância direta para FPSO/FSO porque permite seccionar o switchboard e, ao mesmo tempo, manter possibilidade de transferência de carga entre seções. A literatura usada destaca que:

- o arranjo é comum quando existe grande número de circuitos, especialmente em níveis de distribuição/industrial;
- quando cada seção possui sua própria alimentação, o bus tie pode operar aberto ou fechado;
- se uma alimentação for perdida, todos os circuitos podem, em princípio, ser atendidos pela outra alimentação com o fechamento do tie, desde que exista capacidade elétrica e estabilidade suficientes;
- zonas diferenciais separadas por seção permitem que uma falta em uma barra não impeça atendimento pela outra barra.

Do ponto de vista de recomposição, esse é o arranjo mais diretamente associado à ideia de restaurar uma seção desenergizada a partir de uma seção saudável. A contrapartida é que a falha do disjuntor de tie, em certos esquemas, pode exigir desligamento abrangente, inclusive das duas barras.

### 2.3 Barramento principal com barramento de transferência
Esse arranjo aumenta a flexibilidade de manutenção, mas traz exigências importantes de proteção e operação:

- em operação normal, os circuitos são supridos pelo barramento principal;
- o barramento de transferência normalmente não permanece energizado;
- em caso de manutenção ou problema de um disjuntor, o circuito pode ser transferido ao barramento de transferência por manobras de chaves/disjuntor de tie;
- a literatura consultada ressalta que, tipicamente, apenas um circuito por vez fica conectado ao barramento de transferência.

O ponto crítico é a proteção: o disjuntor de tie precisa ter proteção adequada e adaptável ao circuito transferido. Isso pode exigir troca de ajustes ou lógica de proteção, o que aumenta o risco operacional de erro. O uso de relés numéricos com múltiplos grupos de ajustes reduz esse problema, mas não o elimina como preocupação de engenharia e de comissionamento.

### 2.4 Arranjos mais flexíveis: barramento duplo e topologias correlatas
Os trechos usados resumem que arranjos como barramento duplo oferecem flexibilidade operacional superior, porém com maior complexidade de proteção, necessidade de tensões de referência adequadas e maior rigor no gerenciamento de estados de chaveamento. Em recomposição, essa flexibilidade só é benéfica se a lógica de proteção e a disciplina operacional forem robustas.

**Fontes da seção:** `petroles-004c2afadba7ea17c7dd7908:pNone:2430672.0-2430732.0`, `petroles-004c2afadba7ea17c7dd7908:pNone:2430734.0-2430788.0`, `petroles-004c2afadba7ea17c7dd7908:pNone:2430883.0-2430972.0`

## 3. Filosofia de operação com bus tie aberto ou fechado
Nos trechos navais usados, o sistema de distribuição pode ser dividido em duas, três ou quatro seções conectáveis por bus ties, sendo comum distribuir geradores e grandes consumidores de forma equilibrada entre duas seções. Essa lógica é tecnicamente útil para pensar sistemas offshore seccionados.

A decisão entre operar com bus tie aberto ou fechado envolve compromisso entre integridade e flexibilidade:

- **bus tie fechado:** aumenta a flexibilidade de utilização dos geradores, facilita operação com melhor carregamento médio das máquinas e pode melhorar a tolerância do sistema de geração a certos distúrbios da planta elétrica;
- **bus tie aberto:** aumenta a segregação entre seções e limita a propagação de faltas ou instabilidades de uma seção para outra.

Os mesmos trechos alertam, porém, que os benefícios do barramento fechado dependem fortemente da capacidade da proteção e dos controles detectarem e isolarem faltas sem evoluir para blackout. Já a operação com barramento aberto pode preservar a seção não afetada, mas reduz o suporte mútuo entre seções e pode tornar mais crítico o risco de sobrecarga caso uma máquina seja perdida e o sistema de controle/descarte de cargas não responda adequadamente.

Em outras palavras, a decisão de manter o tie aberto ou fechado é uma decisão de filosofia de integridade do sistema, e não apenas de conveniência operacional.

**Fontes da seção:** `regis-7f6b6ce7792501bc7178c146:pNone:2693.0-2804.0`

## 4. Proteção de barramentos e seletividade como base da recomposição
A recomposição segura começa pela isolação correta da falta. Os trechos usados destacam que faltas em barramentos são pouco frequentes, porém severas, porque o nível de curto-circuito disponível costuma ser alto no ponto de barramento e porque vários circuitos alimentando a falta podem precisar ser abertos para isolá-la.

### 4.1 Proteção diferencial de barramento
A proteção diferencial é descrita como proteção sensível e rápida para faltas fase-fase e fase-terra em barramentos, sendo geralmente recomendada para todos os barramentos. Os pontos principais são:

- a zona diferencial define claramente o que pertence ao barramento protegido;
- a retaguarda costuma ser fornecida pelas proteções dos circuitos conectados;
- barramentos muito importantes podem requerer redundância adicional, inclusive um segundo esquema diferencial.

Para arranjos seccionados por bus tie, a separação em zonas diferenciais por barra é especialmente valiosa porque permite perder apenas a seção faltosa, preservando a outra seção para eventual alimentação de cargas remanescentes ou para futura transferência.

### 4.2 Falha do bus tie e limitações do arranjo
Os resumos comparativos usados indicam que, em alguns arranjos, falha do disjuntor de tie pode levar ao desligamento das duas barras. Portanto, o bus tie não deve ser visto apenas como um elemento de flexibilidade, mas também como ponto crítico de integridade da arquitetura.

### 4.3 Proteções de sobrecorrente e lógica com relés numéricos
Para redes radiais de distribuição/industrial, os trechos usados descrevem uma lógica de proteção rápida de barramento por sobrecorrente com bloqueio pelos alimentadores:

- funções instantâneas de sobrecorrente nos alimentadores enviam bloqueio à proteção principal de barramento;
- a proteção de barramento atua com curto atraso, da ordem de seis ciclos, se a falta estiver no barramento e não em um alimentador;
- a aplicabilidade depende da configuração radial.

A literatura também destaca a vantagem dos relés numéricos para:

- múltiplos grupos de ajustes;
- adaptação de ajustes a modos de operação distintos;
- aumento de sensibilidade em carga leve;
- elevação temporária de pick-up após retorno de energia, para acomodar cold-load pickup.

### 4.4 Detecção de condições anormais que afetam a restauração
Outra contribuição importante dos relés numéricos é detectar condições de subtensão/desbalanceamento que representem anormalidades como fusível aberto no lado de alta de transformador, condição que pode danificar motores se a instalação permanecer ligada com tensões desequilibradas e reduzidas. Em recomposição, isso importa porque o restabelecimento de carga não deve ocorrer sobre uma condição de tensão já degradada.

### 4.5 Desempenho da proteção e análise pós-evento
Os trechos também classificam o desempenho da proteção em operação correta, incorreta ou inconclusiva. Operações incorretas podem resultar de erro de aplicação, erro de ajuste, erro humano ou falhas de relés, disjuntores, TCs, TPs, baterias e fiação. Relés microprocessados com registros e oscilografia ajudam a identificar a causa do evento e são recurso importante antes de autorizar reenergização ou nova transferência de carga.

**Fontes da seção:** `petroles-004c2afadba7ea17c7dd7908:pNone:2430672.0-2430732.0`, `petroles-004c2afadba7ea17c7dd7908:pNone:2430883.0-2430972.0`, `petroles-004c2afadba7ea17c7dd7908:pNone:2434752.0-2434797.0`, `petroles-004c2afadba7ea17c7dd7908:pNone:2424130.0-2424186.0`

## 5. Transferência de cargas entre barras e recomposição após perda de energia
Com base nos trechos disponíveis, a transferência e a recomposição não devem ser tratadas como simples manobras topológicas; elas dependem de proteção, margem de geração e estabilidade transitória.

### 5.1 Perda de uma alimentação em barramento seccionado
Nos barramentos simples conectados por bus tie, a filosofia descrita é clara: se uma alimentação é perdida, os circuitos podem ser supridos pela outra com o fechamento do tie, desde que a outra fonte consiga sustentar a carga. Para que essa manobra seja aceitável, é necessário pelo menos verificar:

- se a falta foi isolada na zona correta;
- se a barra saudável mantém tensão e frequência adequadas;
- se a geração remanescente suporta a nova carga sem violar estabilidade ou proteção;
- se a carga a ser retomada não excede a capacidade transitória do sistema.

### 5.2 Transferência via barramento de transferência
Quando existe barramento de transferência, a recomposição ou continuidade por manutenção deve considerar que:

- o tie assume papel funcional de alimentação do circuito transferido;
- sua proteção deve ser compatível com o circuito que passa a atender;
- a mudança de ajustes/proteção é um ponto sensível de erro;
- a prática mais segura depende de lógica previamente validada e controle rigoroso de configuração.

### 5.3 Estudos de estabilidade e transientes como base da sequência de restauração
Os trechos sobre estabilidade transitória em sistemas industriais mostram que a recomposição deve ser suportada por estudos computacionais capazes de representar:

- máquinas síncronas com regimes transitórios e subtransitórios;
- sistemas de excitação dos geradores;
- reguladores de velocidade;
- motores de indução e suas cargas;
- transformadores, linhas, cabos, reatores e cargas estáticas.

As perturbações a simular incluem, entre outras:

- curtos-circuitos trifásicos em pontos críticos;
- tempo de eliminação da falta por abertura de disjuntores;
- chaveamento de geradores e linhas;
- partida de motores.

As saídas relevantes para definir uma estratégia de recomposição incluem tensões nas barras, frequência, fluxos de potência ativa e reativa, ângulo/velocidade de rotores de máquinas síncronas e escorregamento de motores de indução.

### 5.4 Critérios práticos derivados dos estudos
Os trechos usados apontam como resultados típicos desses estudos:

- **tempo crítico de abertura**, isto é, tempo máximo de permanência de uma falta sem perda de estabilidade de máquina síncrona;
- **impacto de carga**, como aumento súbito de carga sobre gerador local;
- **perda de carga** e seus efeitos em estabilidade e tensão;
- **perda de gerador**;
- necessidade de **descarte de cargas** para manter operação estável e contínua após separação ou perda de geração.

Assim, a recomposição após perda de energia deve ser sequenciada conforme a capacidade dinâmica do sistema, e não apenas pela potência nominal permanente dos geradores.

**Fontes da seção:** `petroles-004c2afadba7ea17c7dd7908:pNone:2430734.0-2430788.0`, `petroles-004c2afadba7ea17c7dd7908:pNone:2137034.0-2137099.0`, `petroles-004c2afadba7ea17c7dd7908:pNone:2434752.0-2434797.0`

## 6. Grandes cargas dinâmicas, tensão/frequência e qualidade de energia durante a recomposição
Em sistemas marítimos, os degraus de carga podem alcançar alguns megawatts. Por isso, a recomposição de cargas de grande porte deve considerar não só potência ativa, mas também potência reativa, fator de potência e limites admissíveis de qualidade de energia.

Os trechos navais reproduzem limites de uma norma citada para instalações elétricas em navios, com os seguintes valores de referência:

- desvio permanente de tensão: +6% / -10%;
- desvio permanente de frequência: ±5%;
- assimetria de tensão: 3%;
- THD: até 5%;
- harmônico individual: até 3%.

Esses valores são úteis como referência de projeto/estudo para entender que a transferência entre barras e a retomada de carga precisam preservar uma faixa aceitável de tensão e frequência.

Os mesmos trechos indicam problemas recorrentes em sistemas marítimos quando os controles não são adequadamente coordenados:

- falta de comunicação entre diferentes sistemas de controle;
- dificuldade de controle da potência reativa;
- ausência de monitoramento do fator de potência;
- risco de instabilidade de tensão quando se inserem cargas reativas ou quando há perda de filtros.

Como exemplo ilustrativo de carga dinâmica, um estudo modelado de propulsores de 800 kW, 910 kW e 2 MW mostrou que o torque varia ao longo da aceleração até atingir a potência nominal, que a maior variação de fluxo ocorreu nos primeiros segundos e que a potência reativa acompanhou as variações de torque, com fator de potência em torno de 0,84. Ainda que esse caso seja específico de propulsão naval, ele ilustra um princípio útil para FPSO/FSO: grandes motores ou acionamentos eletrônicos não devem ser religados em massa após um evento, porque sua retomada afeta simultaneamente tensão, frequência e demanda reativa.

**Fontes da seção:** `regis-7f6b6ce7792501bc7178c146:pNone:2693.0-2804.0`, `regis-7f6b6ce7792501bc7178c146:pNone:2516.0-2756.0`

## 7. Síntese aplicada à engenharia de FPSO/FSO
A partir dos trechos analisados, algumas conclusões técnicas úteis para a faceta de distribuição e recomposição elétrica são:

1. **Barramento simples** é simples, mas tem baixa tolerância a falta de barramento.
2. **Barramento seccionado com bus tie** oferece a melhor ponte entre segregação e recomposição, desde que a proteção por zona e a capacidade remanescente de geração sejam verificadas.
3. **Barramento principal com transferência** é útil para manutenção, porém exige disciplina de proteção e controle de configuração mais rigorosa.
4. **Operação do tie aberto ou fechado** é decisão de integridade do sistema: tie fechado aumenta flexibilidade e compartilhamento, tie aberto reduz propagação de falhas.
5. **A recomposição deve ser validada por estudos dinâmicos**, especialmente quando há grandes motores, acionamentos eletrônicos ou cargas com variação rápida de torque/potência reativa.
6. **Relés numéricos e registros de evento** são parte central da restauração segura, tanto para seletividade quanto para análise pós-falta e liberação de reenergização.

**Fontes da seção:** `petroles-004c2afadba7ea17c7dd7908:pNone:2430672.0-2430732.0`, `petroles-004c2afadba7ea17c7dd7908:pNone:2430734.0-2430788.0`, `petroles-004c2afadba7ea17c7dd7908:pNone:2430883.0-2430972.0`, `petroles-004c2afadba7ea17c7dd7908:pNone:2434752.0-2434797.0`, `petroles-004c2afadba7ea17c7dd7908:pNone:2424130.0-2424186.0`, `petroles-004c2afadba7ea17c7dd7908:pNone:2137034.0-2137099.0`, `regis-7f6b6ce7792501bc7178c146:pNone:2693.0-2804.0`, `regis-7f6b6ce7792501bc7178c146:pNone:2516.0-2756.0`