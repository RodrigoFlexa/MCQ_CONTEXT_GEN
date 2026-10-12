# Sistema de Fogo e Gás (F&G) — testes, calibração e manutenção

## 1. Finalidade da manutenção no contexto de F&G
Em sistemas de F&G de FPSOs/FSOs, a manutenção não deve ser vista apenas como reparo de detectores avariados, mas como um conjunto de ações para preservar a capacidade de detecção e de atuação das funções associadas ao longo do tempo. Em termos gerais de instrumentação, um programa bem estruturado de manutenção preventiva busca: reduzir falhas imprevistas, manter o desempenho esperado dos sistemas, prolongar a vida útil dos equipamentos e melhorar o aproveitamento da mão de obra. Para F&G, esses objetivos se traduzem em manter a disponibilidade dos detectores e da cadeia funcional de segurança em condições de detectar vazamentos de gás, fogo ou fumaça com confiabilidade e tempo de resposta compatíveis com a filosofia de proteção da instalação.

Em aplicações de segurança, um regime puramente corretivo é inadequado como estratégia dominante: esperar a falha se manifestar para então agir tende a degradar disponibilidade e aumentar exposição ao risco. Por isso, a manutenção preventiva e a verificação sistemática da integridade funcional são centrais para F&G.

**Fontes:** `regis-35ffbc28dda7ff89fe900876:pNone:0.0-33.0`, `regis-a448305960d327e79c9a0631:pNone:218.0-285.0`

## 2. Tipos de intervenção aplicáveis aos detectores e às funções F&G
### 2.1 Manutenção preventiva
A manutenção preventiva tem por objetivo impedir a ocorrência do defeito ou corrigi-lo antes que provoque perturbações evidentes. No contexto de F&G, isso abrange, por exemplo:
- inspeções visuais periódicas;
- limpeza de sensores, ópticas, telas sinterizadas, invólucros e janelas ópticas;
- verificação de integridade mecânica, fixação, vedação, corrosão e entrada de água;
- aferição/calibração com padrões e equipamentos adequados;
- testes funcionais do detector e, quando aplicável, verificação da transmissão do sinal até a lógica e dos alarmes/atuações associados;
- substituição programada de componentes sujeitos a desgaste, contaminação, envelhecimento ou deriva.

Os textos-fonte distinguem com utilidade dois subconjuntos dentro da preventiva:
1. **Aferição preventiva**: comparação quantitativa e qualitativa do desempenho do instrumento com padrões preestabelecidos, usando equipamentos de teste adequados.
2. **Manutenção preventiva propriamente dita**: além da aferição, inclui desmontagem, limpeza, troca de peças danificadas ou gastas, montagem e calibração.

Essa distinção é especialmente relevante em F&G porque, na prática, muitos desvios aparecem primeiro como deriva de calibração, perda de sensibilidade, instabilidade de sinal ou falhas de autodiagnóstico, antes de se configurarem como falha total do detector.

### 2.2 Manutenção preditiva
A manutenção preditiva decorre do acompanhamento de variáveis indicadoras da evolução de defeitos. Aplicada a F&G, ela pode ser entendida como o uso de evidências operacionais para antecipar intervenção, por exemplo:
- tendência de deriva de zero/span;
- frequência anormal de falhas de comunicação ou fault status;
- aumento recorrente de sujidade/obstrução em detectores ópticos;
- repetição de calibrações fora do esperado em uma determinada área;
- degradação mais rápida em zonas com névoa salina, vibração, hidrocarbonetos pesados, H₂S, umidade ou temperatura severa.

A manutenção preditiva não substitui a preventiva básica, mas ajuda a reajustar periodicidades e priorizar intervenções.

### 2.3 Manutenção corretiva
A corretiva é executada quando o defeito se tornou evidente pelas perturbações provocadas no sistema. Em F&G, são exemplos: detector travado em falha, perda de alimentação, resposta incompatível com teste funcional, dano mecânico, corrosão severa, descalibração não recuperável por ajuste simples, ou falha de módulos/placas eletrônicas.

**Fontes:** `regis-a448305960d327e79c9a0631:pNone:218.0-285.0`, `regis-35ffbc28dda7ff89fe900876:pNone:0.0-33.0`, `regis-35ffbc28dda7ff89fe900876:pNone:14.0-54.0`

## 3. Critérios para programar inspeções, testes e calibrações
### 3.1 Controle por TAG, detector, malha e zona
Os textos indicam que a programação preventiva deve ser feita por TAG, local de aplicação ou malha, com controle individualizado por instrumento e recorrência para análise por TAG. Para F&G, isso é diretamente aproveitável: o plano deve permitir rastrear cada detector, transmissor, controlador, I/O, voting group ou função associada por identificação única, localização e zona de fogo/gás.

Isso evita tratar o sistema como massa homogênea. Em F&G, dois detectores do mesmo modelo podem exigir tratamento distinto por estarem em ambientes diferentes.

### 3.2 Agrupamento por severidade operacional
Uma contribuição importante das fontes é dividir equipamentos em grupos conforme a rigorosidade operacional. Adaptado a F&G offshore, esse critério pode considerar, conforme o caso:
- salinidade e névoa marinha;
- temperatura e insolação;
- vibração estrutural;
- umidade/condensação;
- agressividade química da atmosfera;
- proximidade de fontes de liberação de hidrocarbonetos ou gases tóxicos;
- acessibilidade e dificuldade de inspeção;
- criticidade da área protegida e ocupação humana.

Assim, detectores idênticos podem ter períodos de manutenção distintos conforme o local de instalação. Esse ponto é coerente com a realidade de F&G: detectores em áreas abertas, expostas ao mar, tendem a sofrer mecanismos de degradação diferentes dos instalados em módulos abrigados.

### 3.3 Período de manutenção
Período é o intervalo entre duas manutenções preventivas consecutivas. As fontes históricas o expressam normalmente em semanas, mas o conceito mais importante é outro: o intervalo deve ser definido com base em características do instrumento, experiência anterior, condições de trabalho e histórico de manutenção.

Para F&G, a consequência prática é que a periodicidade de inspeção, teste funcional rápido, calibração e prova funcional mais abrangente não deve ser arbitrária nem uniforme por conveniência administrativa. Ela deve ser ajustada progressivamente a partir de:
- estado real encontrado nas intervenções;
- ocorrência de corretivas entre preventivas;
- histórico de deriva/calibração;
- recorrência de indisponibilidades;
- severidade ambiental da localização.

Quando há corretivas repetidas entre preventivas, isso é indício de período inadequado, instalação deficiente ou mecanismo de degradação não controlado.

### 3.4 Ciclo de manutenção
As fontes apresentam o conceito de ciclo como a sequência de tipos de manutenção aplicados ao instrumento, por exemplo A-A-B. Para F&G, esse raciocínio é útil para diferenciar profundidades de intervenção:
- **Tipo A**: intervenção leve, normalmente em campo, como inspeção visual, limpeza, verificação de condição externa, checagens simples, confirmação de indicação/diagnóstico e pequenos ajustes;
- **Tipo B**: intervenção parcial, com verificação mais completa, possível retirada para oficina, limpeza aprofundada, substituição de peças danificadas, montagem e calibração;
- **Tipo C**: intervenção total/de oficina, incluindo revisão abrangente e eventual substituição sistemática de componentes críticos.

O conteúdo exato de A, B e C deve ser definido por tecnologia e modelo de detector. Em F&G, uma boa prática é não confundir um teste rápido de resposta com uma calibração completa, nem uma calibração com uma prova funcional da cadeia completa de segurança.

**Fontes:** `regis-a448305960d327e79c9a0631:pNone:218.0-285.0`, `regis-35ffbc28dda7ff89fe900876:pNone:14.0-54.0`, `regis-35ffbc28dda7ff89fe900876:pNone:0.0-33.0`

## 4. Procedimentos padronizados, qualidade de execução e supervisão
As fontes enfatizam que a qualidade dos serviços é decisiva: um programa bem elaborado perde valor se a execução for inconsistente. Portanto, detectores F&G devem ter procedimentos padronizados por tecnologia/modelo e por tipo de intervenção.

Esses procedimentos devem estabelecer claramente, no mínimo:
- sequência de execução;
- ferramentas, padrões e dispositivos de teste aplicáveis;
- critérios de aceitação e rejeição;
- registros “como encontrado” e “como deixado”, quando houver calibração/ajuste;
- necessidade de restauração de parâmetros, alarmes, lógicas e estados de inibição após o serviço;
- encaminhamento para reparo, oficina ou substituição quando o desvio não puder ser corrigido em campo.

As fontes também destacam a necessidade de supervisão e coordenação entre campo e oficina. Para F&G, isso é importante porque uma intervenção frequentemente afeta não só o detector, mas permissivos, telas de operação, alarmes, histórico de eventos, lógica de votação e funções acopladas a ESD, HVAC, dampers, dilúvio ou shutdowns. Mesmo quando o serviço é local, o controle da função associada é sistêmico.

Também é conveniente manter sobressalentes quando couber, para permitir retirada e substituição controlada sem alongar indevidamente a indisponibilidade de proteção.

**Fontes:** `regis-35ffbc28dda7ff89fe900876:pNone:14.0-54.0`, `regis-a448305960d327e79c9a0631:pNone:119.0-151.0`

## 5. Manutenibilidade desde o projeto e o comissionamento
Os textos ressaltam que a necessidade de manutenção deve ser considerada desde a fase de projeto. Para F&G isso é crítico: se não houver meios de liberar temporariamente um detector, uma malha ou um segmento do sistema de forma controlada, a manutenção preventiva pode se tornar difícil, insegura ou inviável.

Em termos de projeto e comissionamento, isso implica considerar:
- acessibilidade física para inspeção e teste;
- possibilidade de substituição controlada por sobressalente;
- recursos para intervenção local sem degradação excessiva da cobertura de proteção;
- filosofia clara para inibições, bypasses e retorno ao estado normal;
- análise criteriosa de redundâncias nos pontos críticos.

As fontes mencionam, por analogia com instrumentação de processo, que a ausência de recursos para liberação individual e temporária pode levar a situação operacional desfavorável. Em F&G, isso se traduz na necessidade de gestão formal de indisponibilidades e de medidas compensatórias definidas pela instalação, sem tratar a inibição como prática rotineira ou banal.

**Fontes:** `regis-35ffbc28dda7ff89fe900876:pNone:0.0-33.0`, `regis-a448305960d327e79c9a0631:pNone:119.0-151.0`

## 6. Registros, histórico e rastreabilidade
O histórico de manutenção é descrito nas fontes como um dos elementos mais difíceis de implantar e manter, mas também dos mais críticos. A fase mais sensível é a coleta de informações em cada intervenção. Para F&G, isso tem implicações diretas de integridade: sem dados confiáveis, perde-se a capacidade de justificar periodicidades, entender recorrências e comprovar condição do sistema.

Boas diretrizes extraídas das fontes:
- o registro deve ser feito por ocasião de cada intervenção;
- o formulário deve ser rápido, simples e pouco sujeito a interpretações subjetivas;
- é necessária supervisão constante para reduzir lapsos, omissões e erros de transcrição;
- devem ser registrados dados úteis, e não massa de informações sem propósito definido;
- sistemas informatizados são desejáveis quando a quantidade de equipamentos e históricos justifica.

Para F&G, o histórico deve permitir ao menos correlacionar detector, localização, tecnologia, tipo de intervenção, condição encontrada, resultado do teste/calibração, falhas recorrentes, peças substituídas, tempo de indisponibilidade e causa provável do desvio.

**Fontes:** `regis-a448305960d327e79c9a0631:pNone:218.0-285.0`

## 7. Uso do histórico para integridade e solução de problemas
As fontes indicam que o período de manutenção deve ser reajustado gradualmente com base no estado encontrado e na ocorrência de corretivas entre preventivas. Aplicado a F&G, esse princípio ajuda a diferenciar problemas de natureza distinta:

- **Deriva de calibração repetitiva**: pode indicar envelhecimento do elemento sensor, contaminação, envenenamento, sujidade óptica, instabilidade eletrônica ou instalação inadequada.
- **Falhas corretivas recorrentes em área específica**: podem apontar problema ambiental/local, e não defeito intrínseco do modelo.
- **Custos ou esforço anormalmente altos por grupo de detectores**: podem sugerir obsolescência, erro de especificação, necessidade de modificação física ou revisão do plano preventivo.
- **Desempenho desigual entre detectores análogos em unidades/zonas distintas**: pode evidenciar diferenças de instalação, ventilação, exposição ou agressividade atmosférica.

As fontes também propõem analisar custos por grupos de instrumentos e separar preventiva de corretiva. Embora custo não deva prevalecer sobre segurança em F&G, essa análise é útil para identificar onde a preventiva está insuficiente, excessiva ou mal direcionada.

**Fontes:** `regis-35ffbc28dda7ff89fe900876:pNone:0.0-33.0`, `regis-a448305960d327e79c9a0631:pNone:152.60-176.0`

## 8. Recursos auxiliares e arranjo de execução
As fontes observam que transporte e manuseio podem introduzir problemas de calibração em instrumentos sensíveis e defendem a combinação entre oficina central e recursos localizados próximos às áreas operacionais. Para F&G, isso sugere uma estratégia prática:
- executar em campo tudo o que for tecnicamente confiável e seguro, especialmente inspeções, limpezas, verificações rápidas e parte dos testes funcionais;
- reservar oficina ou laboratório para revisão mais profunda, reparos eletrônicos, análise de falha e calibrações que exijam ambiente mais controlado;
- minimizar deslocamentos desnecessários de detectores sensíveis quando o próprio transporte puder alterar sua condição ou ampliar o tempo de indisponibilidade.

Essa separação entre serviço leve de campo e serviço aprofundado de oficina também favorece padronização, produtividade e melhor uso de sobressalentes.

**Fontes:** `regis-a448305960d327e79c9a0631:pNone:152.60-176.0`, `regis-a448305960d327e79c9a0631:pNone:119.0-151.0`

## 9. Síntese prática para F&G
Com base nas fontes e sua adaptação ao contexto de F&G, um plano tecnicamente consistente tende a incluir:
1. cadastro completo por TAG/localização/zona/função;
2. classificação dos detectores por severidade ambiental e criticidade;
3. definição de períodos e ciclos de intervenção por tecnologia e local de aplicação;
4. procedimentos padronizados para inspeção, teste funcional, aferição/calibração, reparo e retorno à operação;
5. gestão formal de indisponibilidades temporárias, com rastreabilidade e controle;
6. supervisão ativa da qualidade de execução e dos registros;
7. uso sistemático do histórico para reajustar intervalos, identificar causas recorrentes e sustentar decisões de substituição, melhoria ou revisão de cobertura.

O ponto central é que a integridade do F&G não depende apenas da existência física dos detectores, mas da disciplina de teste, calibração, manutenção e aprendizado a partir do histórico de desempenho.

**Fontes:** `regis-35ffbc28dda7ff89fe900876:pNone:0.0-33.0`, `regis-35ffbc28dda7ff89fe900876:pNone:14.0-54.0`, `regis-a448305960d327e79c9a0631:pNone:218.0-285.0`, `regis-a448305960d327e79c9a0631:pNone:119.0-151.0`, `regis-a448305960d327e79c9a0631:pNone:152.60-176.0`