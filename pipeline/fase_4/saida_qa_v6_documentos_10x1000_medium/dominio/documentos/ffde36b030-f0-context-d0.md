# Filosofia de manutenção e criticidade de ativos em FPSO

## 1. Finalidade e contexto técnico
Em FPSOs, a filosofia de manutenção não deve ser tratada apenas como um conjunto de rotinas periódicas. Ela é uma definição de alto nível sobre **como a organização pretende preservar a função dos ativos** diante de restrições operacionais típicas do ambiente offshore, como:

- distância da costa e dependência logística;
- limitação de mão de obra embarcada;
- limitação física de almoxarifado e sobressalentes a bordo;
- alta complexidade e forte acoplamento entre sistemas;
- requisitos legais, normativos e de segurança operacional;
- impacto potencial de falhas sobre pessoas, meio ambiente, produção e custos.

Nos trechos fornecidos, a proposta metodológica está fundamentada em **Manutenção Centrada em Confiabilidade (MCC/RCM)** e na filosofia de **Operações Integradas**, com a premissa de que a estratégia de manutenção deve maximizar disponibilidade e eficiência, sem dissociar segurança operacional e suporte técnico onshore. Isso é particularmente relevante em novas unidades, mas os próprios trechos indicam que a abordagem também pode ser usada para revisão de estratégias em unidades já em operação.

**Fontes:** `regis-74dd376119cbb653fe9922bc:pNone:1020.0-1313.0`, `regis-74dd376119cbb653fe9922bc:pNone:6210.0-6525.0`

## 2. Filosofia de manutenção: princípios de definição
Pelos excertos, uma filosofia de manutenção tecnicamente consistente para FPSO deve combinar pelo menos quatro princípios.

### 2.1 Manutenção orientada por função, falha e consequência
Os trechos criticam a prática de definir planos a partir da experiência informal de grupos, resultando em excesso de tarefas preventivas sem relação direta com os modos de falha dos equipamentos. Em contrapartida, a filosofia proposta busca definir tarefas e intervalos a partir de:

- funções dos ativos;
- modos de falha relevantes;
- partes afetadas;
- dados de confiabilidade/taxa de falha, quando disponíveis;
- consequência da perda da função.

Isso desloca a manutenção de uma lógica puramente calendárica para uma lógica de **risco, confiabilidade e consequência**.

### 2.2 Priorização da manutenção baseada na condição
A filosofia proposta dá preferência à **manutenção baseada na condição**, com verificações sistemáticas e mais frequentes para identificar defeitos em estágio inicial, antes da falha funcional. Nos trechos, isso aparece como fator de aumento de disponibilidade e confiabilidade, inclusive por reduzir intervenções preventivas desnecessárias e a indisponibilidade induzida por manutenção.

### 2.3 Participação ampliada da operação
Uma diretriz explícita é a **participação ativa dos operadores** em atividades de manutenção autônoma e verificações de campo. O objetivo não é substituir a manutenção especializada, mas deslocar tarefas simples, rotineiras e de observação operacional para a equipe de operação, liberando a equipe de manutenção para problemas de maior complexidade.

### 2.4 Integração offshore-onshore
Na filosofia de Operações Integradas, parte do monitoramento, da análise e do planejamento das intervenções pode ser estruturada com apoio de equipes especializadas em ambiente onshore. Para FPSO, isso é uma resposta organizacional à limitação de recursos embarcados e à necessidade de decisões mais rápidas e tecnicamente qualificadas.

**Síntese prática:** a filosofia de manutenção deixa de ser apenas uma escolha entre corretiva, preventiva ou preditiva e passa a ser um arranjo integrado entre **criticidade, confiabilidade, monitoramento de condição, competências embarcadas e suporte onshore**.

**Fontes:** `regis-74dd376119cbb653fe9922bc:pNone:1020.0-1313.0`, `regis-74dd376119cbb653fe9922bc:pNone:6210.0-6525.0`, `regis-74dd376119cbb653fe9922bc:pNone:33090.0-33377.0`

## 3. Inserção da filosofia de manutenção nas fases do empreendimento
Os trechos indicam que a filosofia de manutenção não deve nascer apenas após o start-up. Ela precisa ser incorporada ainda no ciclo de projeto.

### 3.1 Projeto básico: uso de estudos RAM
Na fase de projeto básico, é apontada a importância de estudos **RAM** (Reliability, Availability and Maintainability) para identificar equipamentos e sistemas críticos e estimar a contribuição de cada um para a disponibilidade final da planta. O raciocínio descrito é:

1. levantar modos de falha, histórico de falhas e tempos de reparo;
2. modelar o sistema por blocos funcionais, em série ou em paralelo conforme a lógica de perda;
3. simular o comportamento do sistema ao longo do tempo;
4. identificar perdas e recomendar melhorias, como redundância ou mudança de estratégia.

Do ponto de vista da filosofia de manutenção, o estudo RAM cumpre duas funções:

- ajuda a identificar **onde a indisponibilidade mais penaliza a planta**;
- fornece insumos para a **priorização técnica** e para decisões de projeto, e não apenas de rotina de manutenção.

### 3.2 Fase de detalhamento: definição estrutural da manutenção
Na fase de detalhamento, os trechos destacam como essenciais:

- atualização do modelo RAM;
- definição preliminar da carga de trabalho de manutenção;
- definição da equipe mínima embarcada;
- seleção do software de manutenção/CMMS, se aplicável;
- definição da estratégia de operação e manutenção;
- definição de contratos de serviços;
- definição de requisitos para gestão de sobressalentes;
- definição de requisitos para Operações Integradas.

Em outras palavras, a filosofia de manutenção deve ser desdobrada em **capacidade organizacional**, **ferramentas**, **recursos humanos**, **sobressalentes** e **processos de trabalho**.

### 3.3 Implantação priorizada
A tese sugere que, ao implantar o planejamento da manutenção, a priorização inicial recaia sobre:

1. sistemas ligados diretamente à segurança operacional, como combate a incêndio, detecção de fogo e gás e geração de emergência;
2. sistemas de medição de fluidos, por atendimento regulatório;
3. sistemas com maior impacto na produção segundo a modelagem RAM;
4. sistemas de impacto irrelevante na produção, em etapa posterior.

Esse encadeamento mostra que a filosofia de manutenção, em FPSO, deve começar pelos ativos cuja indisponibilidade produz **consequências intoleráveis** ou **perdas desproporcionais**.

**Fontes:** `regis-74dd376119cbb653fe9922bc:pNone:5451.0-5740.0`

## 4. Hierarquização dos ativos como base da criticidade
Os trechos tratam a **hierarquização dos ativos** como a primeira etapa da estratégia de manutenção e uma das mais importantes.

### 4.1 O que é a hierarquização
É a subdivisão estruturada da planta em níveis hierárquicos, estabelecendo:

- identificação dos itens manuteníveis;
- relação entre sistemas, subsistemas e componentes;
- função dos blocos dentro do processo produtivo;
- fronteiras técnicas para planejamento e análise.

A construção da árvore de equipamentos deve ser feita a partir de documentos de engenharia, como:

- P&IDs;
- diagramas de blocos;
- diagramas unifilares;
- fluxogramas gerais;
- folhas de dados de equipamentos;
- outros documentos de projeto aplicáveis.

### 4.2 Por que a hierarquização é indispensável
Segundo os trechos, uma boa manutenção começa por um bom cadastro de equipamentos. A hierarquização correta permite:

- planejar intervenções de forma coerente com a função do conjunto;
- agrupar atividades e evitar retirada individual e fragmentada de itens de um mesmo conjunto funcional;
- apoiar estudos de confiabilidade e modelagem por blocos funcionais;
- vincular pacotes de manutenção aos itens corretos;
- associar custos e materiais sobressalentes aos ativos adequados;
- apoiar a gestão de estoque.

Em FPSO, isso é particularmente importante porque a priorização de recursos embarcados depende de saber **qual item pertence a qual função crítica** e **qual indisponibilidade afeta qual sistema**.

### 4.3 Relação entre hierarquia e criticidade
A criticidade não deve ser atribuída de forma descontextualizada ao equipamento isolado. Ela depende da posição do item na hierarquia funcional da planta. Um mesmo tipo de equipamento pode ter criticidades distintas conforme:

- a função que suporta;
- a existência ou não de redundância;
- a consequência da perda de função;
- o tempo tolerável de indisponibilidade;
- a capacidade de reparo ou substituição no ambiente offshore.

**Fontes:** `regis-74dd376119cbb653fe9922bc:pNone:6210.0-6525.0`, `regis-74dd376119cbb653fe9922bc:pNone:33090.0-33377.0`

## 5. Criticidade de ativos para priorização técnica
A criticidade, nos trechos, é o mecanismo de priorização que permite alocar recursos limitados nos equipamentos mais relevantes da planta.

### 5.1 Finalidade da análise de criticidade
A classificação adequada da criticidade permite:

- aumentar a eficácia na escolha do tipo de manutenção;
- otimizar a aplicação de recursos humanos;
- apoiar a gestão de custos;
- definir prioridade de implantação dos planos;
- separar o que deve ser tratado como essencial à segurança do que pode receber tratamento menos intensivo.

### 5.2 Critérios de consequência
O trecho baseado na NORSOK Z-008 apresenta três eixos principais de consequência:

- **saúde, segurança e meio ambiente (SSMA/HSE)**;
- **produção**;
- **custo**, inclusive perda de produção.

A classificação geral é apresentada em três níveis de consequência:

- **Alta**: potencial para lesões sérias, indisponibilidade de sistemas críticos de segurança, potencial para incêndio em área classificada, ampla poluição ambiental, ou parada/perda significativa de produção e custo significativo;
- **Média**: potencial para lesões com tratamento médico, efeito limitado em sistemas de segurança, poluição moderada, breve parada/redução de produção e custo moderado;
- **Baixa**: sem potencial para lesões, sem efeito em sistemas de segurança, sem potencial para incêndio ou poluição, sem efeito na produção e custo insignificante.

Os próprios limites de tempo e custo são deixados para definição da empresa, o que mostra que a criticidade deve ser calibrada ao contexto do ativo e da organização.

### 5.3 Inclusão do nível altíssima
Além da referência com três classes de consequência, a tese propõe um **quarto nível de criticidade: altíssima**. O objetivo é destacar equipamentos críticos de segurança operacional, incluindo aqueles:

- definidos como salvaguardas em estudos de risco; ou
- pertencentes a sistemas críticos de segurança operacional.

Na prática, esse nível separa o que não é apenas importante, mas **intolerante a falhas sem tratamento prioritário**, por sua função de barreira, proteção ou resposta a emergências.

### 5.4 Metodologia de ranqueamento
Os trechos informam que a metodologia da tese considera diversos fatores relevantes para manutenção, fundamenta-se em normas técnicas da NORSOK e utiliza o **critério de Mudge** como ferramenta de apoio para definição quantitativa da criticidade. Contudo, os excertos não trazem o algoritmo completo, a matriz nem a fórmula de cálculo. Portanto, o ponto tecnicamente seguro é:

- a criticidade pode ser tratada de forma **qualitativa ou semi-quantitativa**;
- o ranqueamento deve comparar a importância relativa dos critérios;
- a saída da análise deve apoiar decisões de priorização e não ser um fim em si.

**Fontes:** `regis-74dd376119cbb653fe9922bc:pNone:5451.0-5740.0`, `regis-74dd376119cbb653fe9922bc:pNone:33090.0-33377.0`

## 6. Como a criticidade altera a estratégia de manutenção
A criticidade não serve apenas para montar listas de prioridade. Nos trechos, ela altera diretamente a estratégia de manutenção aplicável.

### 6.1 Equipamentos de baixa criticidade
Para equipamentos de **baixa criticidade**, a proposta recomenda **manutenção corretiva planejada**. Isso decorre da restrição de mão de obra a bordo e da necessidade de concentrar esforço nos ativos mais relevantes.

Essa escolha só é tecnicamente defensável se houver, no mínimo:

- gestão adequada de materiais sobressalentes;
- capacidade de recompor a função após falha em prazo aceitável;
- confirmação de que a falha não produz consequência relevante em segurança, meio ambiente ou produção.

### 6.2 Equipamentos de maior criticidade
Para ativos de criticidade mais alta, a estratégia deve envolver:

- análise dos modos de falha;
- uso de dados de confiabilidade/taxa de falha, quando disponíveis;
- escolha da técnica de manutenção mais adequada para bloquear ou detectar o modo de falha;
- definição da periodicidade com base em criticidade e comportamento de falha.

Nos trechos, a manutenção baseada na condição é priorizada para esses casos, com apoio de verificações mais frequentes e monitoramento estruturado.

### 6.3 Otimização da preventiva
Uma conclusão importante da tese é que a metodologia proposta aumentou a disponibilidade média dos sistemas analisados ao **reduzir o número de intervenções preventivas** e, consequentemente, a indisponibilidade associada à própria manutenção. Isso reforça um ponto central da filosofia:

- mais manutenção não implica necessariamente mais confiabilidade;
- preventiva mal selecionada pode degradar disponibilidade;
- a estratégia deve ser justificada por criticidade, modo de falha e condição do ativo.

### 6.4 Papel da operação e do suporte onshore
A priorização da manutenção baseada na condição é viabilizada, nos trechos, por:

- verificações sistemáticas feitas pela operação em campo;
- estruturação de grupo onshore para avaliar dados e planejar intervenções;
- racionalização dos recursos embarcados.

Esse arranjo organiza a criticidade em dois planos:

1. **prioridade do ativo** para receber atenção;
2. **modelo operacional** de quem detecta, quem analisa e quem executa.

**Fontes:** `regis-74dd376119cbb653fe9922bc:pNone:6210.0-6525.0`, `regis-74dd376119cbb653fe9922bc:pNone:33090.0-33377.0`

## 7. Exemplo de aplicação conceitual em FPSO
Sem extrapolar os trechos para números não fornecidos, uma lógica coerente de aplicação seria:

### 7.1 Primeiro nível: ativos de segurança operacional
Entram no topo da priorização sistemas como:

- combate a incêndio;
- detecção de fogo e gás;
- geração de emergência;
- salvaguardas identificadas em estudos de risco.

Esses ativos tendem a receber classificação **altíssima** ou equivalente, com exigência de estratégia robusta e baixa tolerância a indisponibilidade.

### 7.2 Segundo nível: ativos de impacto regulatório ou de medição essencial
Sistemas de medição de fluidos aparecem como prioritários nos trechos por necessidade de atendimento regulatório e operacional.

### 7.3 Terceiro nível: ativos com maior penalização de produção
A modelagem RAM pode indicar quais sistemas mais degradam a disponibilidade ou a produção da planta. Esses ativos devem receber criticidade elevada mesmo quando não são barreiras de segurança, pois afetam diretamente o desempenho do FPSO.

### 7.4 Quarto nível: ativos sem efeito relevante na segurança ou produção
Quando não há consequência relevante, a estratégia pode migrar para corretiva planejada, desde que o estoque, a logística e o tempo de recomposição sejam compatíveis com o risco aceito.

**Fontes:** `regis-74dd376119cbb653fe9922bc:pNone:5451.0-5740.0`, `regis-74dd376119cbb653fe9922bc:pNone:6210.0-6525.0`

## 8. Critérios de decisão que emergem dos trechos
A partir do material fornecido, alguns critérios de decisão são particularmente úteis para avaliação profissional.

### 8.1 Quando a filosofia deve privilegiar manutenção baseada na condição
Privilegiar quando houver:

- modo de falha detectável antes da falha funcional;
- consequência relevante de indisponibilidade;
- possibilidade de monitoramento sistemático por operação e/ou suporte onshore;
- ganho de disponibilidade por redução de paradas preventivas desnecessárias.

### 8.2 Quando a corretiva planejada é aceitável
Aceitável quando houver simultaneamente:

- baixa criticidade;
- ausência de impacto relevante em segurança, meio ambiente e produção;
- recomposição viável após falha;
- suporte logístico e sobressalentes adequados.

### 8.3 Quando a análise de criticidade deve prevalecer sobre a tradição
Se a planta possui muitos ativos e recursos embarcados limitados, a definição de planos apenas por tradição ou experiência tende a gerar sobrecarga de preventiva. Nesses casos, os trechos sustentam priorização formal baseada em criticidade, modos de falha e dados de confiabilidade.

### 8.4 Quando a manutenção deve entrar no projeto
Os trechos sustentam inserção desde o projeto básico e detalhado, para que a manutenção influencie:

- redundância;
- capacidade de equipe;
- CMMS;
- contratos;
- sobressalentes;
- implantação de Operações Integradas.

**Fontes:** `regis-74dd376119cbb653fe9922bc:pNone:5451.0-5740.0`, `regis-74dd376119cbb653fe9922bc:pNone:6210.0-6525.0`, `regis-74dd376119cbb653fe9922bc:pNone:33090.0-33377.0`

## 9. Conclusão técnica
Para a faceta de **filosofia e criticidade**, os trechos sustentam que a gestão da manutenção em FPSO deve ser construída a partir de uma sequência lógica:

1. incorporar a manutenção desde o projeto;
2. estruturar corretamente a hierarquia de ativos;
3. avaliar criticidade por consequência em segurança, meio ambiente, produção e custo;
4. destacar separadamente os elementos críticos de segurança;
5. ligar a criticidade à escolha da estratégia de manutenção;
6. priorizar manutenção baseada na condição onde ela efetivamente aumenta disponibilidade e confiabilidade;
7. reservar a corretiva planejada para ativos de baixa criticidade, com suporte de sobressalentes e logística;
8. usar operação e suporte onshore como parte da solução organizacional de manutenção.

O ponto central é que, em FPSO, **filosofia de manutenção e criticidade não são temas separados**: a criticidade organiza a prioridade técnica, e a filosofia define como a organização responderá a essa prioridade com recursos limitados e alta exigência de segurança.

**Fontes:** `regis-74dd376119cbb653fe9922bc:pNone:1020.0-1313.0`, `regis-74dd376119cbb653fe9922bc:pNone:5451.0-5740.0`, `regis-74dd376119cbb653fe9922bc:pNone:6210.0-6525.0`, `regis-74dd376119cbb653fe9922bc:pNone:33090.0-33377.0`