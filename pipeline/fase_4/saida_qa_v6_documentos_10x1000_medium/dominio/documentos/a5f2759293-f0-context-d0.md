# Análise de perigos e riscos em FPSOs/FSOs e produção subsea

## 1. Finalidade e enquadramento técnico
A análise de perigos e riscos é a base para reduzir os riscos de uma instalação a níveis toleráveis ao longo de todo o ciclo de vida — projeto, construção, comissionamento, operação, manutenção, modificações e descomissionamento. No contexto de instalações de processo, a segurança de processo tem como foco evitar liberações indesejadas de substâncias ou energia capazes de causar impactos tóxicos, incêndios e explosões; já a segurança ocupacional amplia a proteção dos trabalhadores nas atividades e tarefas executadas na instalação. O material disponível enfatiza que a gestão de segurança de processo deve ser aplicada durante toda a vida útil da planta e depende fortemente de liderança e comprometimento gerencial.  

Em FPSOs/FSOs e sistemas subsea, isso significa tratar tanto os perigos associados ao processo (perda de contenção, sobrepressão, falhas de utilidades, falhas de intertravamentos, incêndio/explosão) quanto perigos associados às operações e tarefas (partidas, paradas, manutenção, limpeza, inspeção, isolamentos, intervenções e respostas a emergências).  

*(Fontes: `regis-161cd3328a094e3a98a6fa18:pNone:2114.0-2317.0`, `regis-151b5a6f2316dd5a5fd5f15d:pNone:0.0-54.0`)*

## 2. Conceitos fundamentais
### 2.1 Perigo
Perigo é a condição, objeto, atividade, característica física ou química com potencial de causar dano. As fontes indicam que o perigo está ligado à potencialidade: materiais perigosos, condições de processo, propriedades dos fluidos, equipamentos, reações, fontes de ignição, falhas de alimentação, perdas de utilidades e falhas humanas/organizacionais podem todos ser fontes de perigo.  

### 2.2 Risco
Risco é a combinação entre a possibilidade/probabilidade/frequência de um evento perigoso e a gravidade de suas consequências. Em linguagem prática de análise, o risco é normalmente tratado como uma função de **frequência/probabilidade × consequência/severidade**, ainda que nem sempre com cálculo matemático explícito.  

### 2.3 Diferença entre perigo e risco
Uma distinção útil trazida pelo material é:
- **perigo**: potencial abstrato de dano;
- **risco**: estimativa concreta desse dano, associando consequências e probabilidades.

Essa distinção evita um erro comum: confundir a existência de um agente perigoso com o nível de risco efetivo. Em um FPSO, hidrocarbonetos inflamáveis são um perigo intrínseco; o risco depende das quantidades, condições operacionais, confinamento, detecção, barreiras, probabilidade de ignição e capacidade de resposta.  

*(Fontes: `regis-161cd3328a094e3a98a6fa18:pNone:2114.0-2317.0`, `regis-474ad04a90c2f8f651b08d76:pNone:7724.0-7944.0`, `petroles-004c2afadba7ea17c7dd7908:pNone:1754353.0-1754396.0`)*

## 3. Processo técnico de identificação, análise, avaliação e tratamento de riscos

### 3.1 Identificação de perigos
A identificação de perigos é a primeira fase da análise de riscos. O material atribui a essa fase o papel de base para as demais atividades de gestão de segurança de processo. Em termos práticos, identificar perigos envolve ao menos duas tarefas:
1. identificar o **evento indesejado**;
2. definir **qual sistema, equipamento, processo ou característica operacional** pode produzi-lo.

Segundo o conteúdo baseado em AIChE/CCPS, métodos usuais de identificação de perigos:
1. analisam as propriedades dos materiais e as condições de processo;
2. consideram a experiência da indústria e de instalações semelhantes;
3. desenvolvem matrizes de interação entre esses elementos e aplicam a técnica de avaliação escolhida.

Para FPSOs/FSOs e subsea, essa identificação deve abranger, entre outros, cenários como:
- perda de contenção de hidrocarbonetos ou químicos;
- sobrepressão e falhas de alívio;
- falhas de instrumentação, alarmes e intertravamentos;
- falhas de alimentação/energia/utilidades;
- falhas em partidas, paradas e transientes;
- introdução de riscos por manutenção, limpeza e intervenções;
- falhas organizacionais e fatores humanos.

As fontes também reforçam que a identificação pode ser feita por análise do passado (acidentes, incidentes, desvios, quase acidentes) e por análise do processo em si. A primeira é mais reativa; a segunda, mais proativa.  

*(Fontes: `regis-161cd3328a094e3a98a6fa18:pNone:2114.0-2317.0`, `regis-474ad04a90c2f8f651b08d76:pNone:7724.0-7944.0`, `petroles-004c2afadba7ea17c7dd7908:pNone:1754353.0-1754396.0`, `regis-18675593ea42a9f6a427733f:pNone:7242.0-7478.0`)*

### 3.2 Análise de riscos
A análise de riscos aprofunda os perigos identificados para compreender:
- causas e fontes de risco;
- consequências possíveis;
- probabilidade/frequência de ocorrência;
- controles existentes e sua eficácia/eficiência;
- interdependências entre riscos e entre suas fontes.

O material associado à ISO 31000 destaca que a análise de riscos pode ser:
- **qualitativa**;
- **semiquantitativa**;
- **quantitativa**;
- ou uma combinação dessas abordagens.

O grau de detalhamento deve depender do risco, da finalidade do estudo e da disponibilidade de dados, recursos e conhecimento do processo. Em aplicações offshore, é comum começar com análise qualitativa ampla e aprofundar cenários críticos por métodos mais formais e, quando necessário, quantitativos.

As consequências e probabilidades podem ser estimadas por:
- modelagem de eventos ou cadeias de eventos;
- extrapolação de dados experimentais;
- dados históricos disponíveis;
- julgamento especializado, quando os dados forem limitados.

Um ponto importante é que um mesmo evento pode produzir várias consequências e afetar objetivos distintos: pessoas, instalações, meio ambiente, produção/continuidade operacional e reputação.  

*(Fontes: `regis-474ad04a90c2f8f651b08d76:pNone:7724.0-7944.0`, `regis-474ad04a90c2f8f651b08d76:pNone:7838.0-8150.0`, `petroles-004c2afadba7ea17c7dd7908:pNone:3234099.60-3234129.0`)*

### 3.3 Avaliação de riscos
Avaliar o risco é comparar o nível encontrado na análise com critérios previamente estabelecidos pela organização. Essa comparação sustenta decisões como:
- tratar imediatamente o risco;
- aprofundar a análise;
- priorizar recursos para cenários mais críticos;
- ou manter controles existentes quando o risco já estiver adequadamente controlado.

A avaliação deve considerar:
- critérios de risco definidos previamente;
- contexto mais amplo do empreendimento;
- requisitos legais, regulatórios e outros aplicáveis;
- tolerância ao risco das partes afetadas;
- efetividade dos controles existentes.

Em resumo:
- **identificação** responde “o que pode dar errado?”;
- **análise** responde “como, por que, com que frequência e com quais consequências?”;
- **avaliação** responde “o risco é aceitável/tolerável ou precisa de tratamento adicional?”.

*(Fontes: `regis-474ad04a90c2f8f651b08d76:pNone:7724.0-7944.0`, `regis-474ad04a90c2f8f651b08d76:pNone:7838.0-8150.0`)*

### 3.4 Tratamento e verificação da eficácia
Os estudos citados convergem para três linhas de ação principais:
- eliminar causas;
- reduzir a probabilidade/frequência do evento;
- reduzir as consequências por medidas preventivas e/ou mitigadoras.

Também há um cuidado explícito: **ao reduzir um risco, não se deve introduzir novos riscos**. Após implementar medidas, sua eficácia precisa ser avaliada, caracterizando um ciclo de melhoria contínua.  

*(Fontes: `petroles-4ee4bce16acf674505c8912d:pNone:2424614.60-2424641.0`, `petroles-004c2afadba7ea17c7dd7908:pNone:1754353.0-1754396.0`)*

## 4. Critérios de classificação e aceitabilidade

### 4.1 Matrizes de risco
Uma forma amplamente usada para classificar riscos é a **matriz de risco**, que cruza:
- **frequência/probabilidade**; e
- **consequência/severidade**.

O material informa que, no segmento offshore, são comuns matrizes com três a seis categorias por eixo. Cada célula representa uma combinação específica de frequência e consequência. A organização deve definir quais células correspondem a riscos:
- aceitáveis;
- toleráveis sob controle;
- ou não toleráveis, exigindo redução.

Exemplos de categorias de consequência citadas em referências reproduzidas pelo material incluem:
- desprezível;
- marginal;
- crítica;
- catastrófica.

Há também referência a matrizes que discriminam consequências para quatro dimensões:
- pessoas;
- instalações/patrimônio;
- meio ambiente;
- reputação/imagem.

Em FPSOs/FSOs, essa segregação é particularmente útil porque um mesmo cenário pode ter criticidade distinta em cada dimensão. Um vazamento pequeno pode ser marginal para patrimônio, mas crítico para meio ambiente ou ocupacional dependendo da substância e do local.  

*(Fontes: `regis-474ad04a90c2f8f651b08d76:pNone:7838.0-8150.0`, `petroles-004c2afadba7ea17c7dd7908:pNone:3234099.60-3234129.0`)*

### 4.2 Cenários críveis
As fontes ressaltam que a análise deve focar **cenários críveis**, isto é, eventos com possibilidade real de ocorrer. Não se recomenda colocar lado a lado cenários fantasiosos e cenários operacionalmente plausíveis, porque isso distorce priorização e alocação de recursos.

Exemplos de cenários críveis incluem:
- erro humano;
- falha de instrumento;
- problema mecânico;
- corrosão e perda de contenção;
- perda de alimentação relevante;
- falha operacional durante manutenção ou partida/parada.

Já combinações extremamente improváveis de múltiplas falhas independentes simultâneas podem não ser úteis como base principal de priorização, salvo quando houver justificativa técnica específica.  

*(Fontes: `petroles-004c2afadba7ea17c7dd7908:pNone:1754353.0-1754396.0`)*

### 4.3 Princípio ALARP e risco tolerável
O material descreve o princípio **ALARP (As Low As Reasonably Practicable)** como a ideia de reduzir o risco até um nível tão baixo quanto razoavelmente praticável, considerando recursos e viabilidade técnica. Aplicado às instalações offshore, o conceito não significa risco zero; significa demonstrar que:
- riscos não aceitáveis foram reduzidos;
- riscos remanescentes estão controlados;
- a instalação permanece em região tolerável conforme critérios adotados.

Para fins de decisão, ALARP é menos uma fórmula e mais um critério de demonstração de razoabilidade na seleção de medidas de redução.  

*(Fontes: `regis-474ad04a90c2f8f651b08d76:pNone:7838.0-8150.0`, `petroles-004c2afadba7ea17c7dd7908:pNone:466560.0-466586.0`)*

## 5. Técnicas de identificação e análise de perigos/riscos

## 5.1 APR / APP / PHA — Análise Preliminar de Riscos ou de Perigos
A APR é apresentada como técnica qualitativa, preliminar e estruturada para identificar perigos de instalações novas ou existentes. É especialmente útil:
- na fase inicial do projeto;
- no início da concepção;
- em revisões rápidas de segurança de instalações existentes;
- quando há pouca informação disponível para modelagens mais sofisticadas.

### Características principais
- antecipa riscos e orienta o projeto;
- ajuda a direcionar análises posteriores mais detalhadas;
- pode ser aplicada por módulos/sistemas da instalação;
- gera resultados qualitativos e preliminares;
- permite rápida priorização de recursos em prevenção e mitigação.

### Limitações
- tende a ser mais superficial que métodos formais como HAZOP;
- depende fortemente da experiência da equipe;
- é menos indicada, isoladamente, para sistemas já muito conhecidos ou para instalações complexas que exigem maior detalhamento.

### Etapas recorrentes de uma APR
Os materiais citam, com pequenas variações, etapas como:
1. definir objetivos e fronteiras da análise;
2. coletar informações sobre a instalação, a região e os perigos envolvidos;
3. subdividir o processo em módulos ou sistemas;
4. identificar cenários, causas e consequências;
5. atribuir frequência/probabilidade e severidade;
6. classificar o risco;
7. propor medidas preventivas e/ou mitigadoras;
8. consolidar resultados e relatório.

### Conteúdo típico da planilha de APR
Uma planilha típica pode conter:
- cenário;
- perigo/risco identificado;
- causas;
- salvaguardas/barreiras existentes;
- consequências;
- severidade;
- frequência/probabilidade;
- classificação/ranking do risco;
- recomendações.

### Tipos de danos usualmente contemplados
Os efeitos e danos esperados citados nas fontes incluem:
- incêndios;
- explosões;
- danos a corpos d’água por vazamentos;
- lesões a operadores;
- lesões ao público externo;
- danos a propriedades e instalações;
- perda de equipamentos;
- perda de produção e de continuidade operacional.

Em FPSOs/FSOs, a APR é útil para triagem inicial de cenários como perda de contenção em módulos de separação, compressão ou tratamento, falhas de utilidades, falhas de alívio, riscos em partidas e paradas e falhas com potencial de escalada para incêndio/explosão.  

*(Fontes: `regis-161cd3328a094e3a98a6fa18:pNone:2114.0-2317.0`, `regis-151b5a6f2316dd5a5fd5f15d:pNone:0.0-54.0`, `petroles-4ee4bce16acf674505c8912d:pNone:2424614.60-2424641.0`, `petroles-004c2afadba7ea17c7dd7908:pNone:1754353.0-1754396.0`, `petroles-004c2afadba7ea17c7dd7908:pNone:3234099.60-3234129.0`, `regis-18675593ea42a9f6a427733f:pNone:7242.0-7478.0`)*

## 5.2 HAZOP, What-If, checklist, brainstorm e revisões de segurança
As fontes citam técnicas menos ou mais estruturadas, úteis conforme complexidade do sistema:
- **HAZOP**: abordagem sistemática orientada por parâmetros críticos de processo (ex.: vazão, temperatura, pressão) e palavras-guia, aplicada a nós do processo para revelar desvios, perigos e problemas de operabilidade;
- **What-If**: revisão por perguntas do tipo “e se?”;
- **checklists** e **brainstorm**: úteis como apoio em avaliações iniciais ou complementares;
- **WIC / What-If Checklist**: combinação de perguntas estruturadas com documentação do processo.

Para revisões tipo What-If/Checklist, o material lista como insumos relevantes:
- instruções de operação;
- memória de cálculo de instalações e equipamentos;
- relação de alarmes e intertravamentos;
- relatórios de incidentes;
- padrões técnicos de processo;
- diagramas elétricos, lógicos e de instrumentação.

Exemplos de perguntas tecnicamente relevantes nessas revisões:
- materiais foram classificados quanto à perigosidade?
- há risco de decomposição/reação descontrolada?
- que misturas inflamáveis podem ocorrer no equipamento?
- a instalação permanece segura em falha simultânea de instrumentação/alimentações?
- quais riscos são introduzidos pela manutenção de rotina?
- quais exigências de limpeza existem antes de partidas?
- válvulas e botões de emergência são acessíveis?
- houve previsão para testar e manter alarmes/intertravamentos?

Esse tipo de abordagem é particularmente valioso para fases de comissionamento, partida, parada, manutenção e mudanças operacionais.  

*(Fontes: `regis-474ad04a90c2f8f651b08d76:pNone:7724.0-7944.0`, `petroles-004c2afadba7ea17c7dd7908:pNone:1754353.0-1754396.0`, `petroles-004c2afadba7ea17c7dd7908:pNone:3234099.60-3234129.0`, `regis-18675593ea42a9f6a427733f:pNone:7242.0-7478.0`)*

## 5.3 FMEA / AMFE
A Análise de Modos de Falha e Efeitos é apresentada como técnica voltada à detecção de falhas antes da construção e ao exame de modos de falha e seus efeitos sobre o sistema. O material a descreve como útil para:
- detectar falhas potenciais em fase de projeto;
- propor melhorias para eliminação, mitigação ou controle;
- estimar taxas de falha e melhorar confiabilidade;
- apoiar prevenção com menor custo que correções tardias.

As fontes também registram uma limitação importante: a técnica não seria a mais recomendada para sistemas muito complexos, sendo mais apropriada a sistemas com falhas recorrentes ou mais facilmente decomponíveis.  

*(Fontes: `regis-161cd3328a094e3a98a6fa18:pNone:2114.0-2317.0`, `regis-474ad04a90c2f8f651b08d76:pNone:7724.0-7944.0`)*

## 5.4 Árvore de Falhas (FTA / AAF)
A Árvore de Falhas é descrita como método dedutivo que parte de um **evento topo** previamente definido e reconstrói, por relações lógicas, as falhas causadoras do evento. É útil quando o interesse está em entender como combinações de falhas podem levar a um acidente relevante, apoiar o aumento da confiabilidade e complementar análises qualitativas.  

*(Fontes: `regis-161cd3328a094e3a98a6fa18:pNone:2114.0-2317.0`, `petroles-004c2afadba7ea17c7dd7908:pNone:1754353.0-1754396.0`)*

## 5.5 Análise Quantitativa de Riscos (AQR/QRA)
Quando a decisão exige maior profundidade, o material aponta a progressão para análises quantitativas. Uma estrutura citada para AQR inclui:
1. caracterização do empreendimento e da região;
2. identificação de perigos e consolidação dos cenários acidentais;
3. estimativa dos efeitos físicos e análise de vulnerabilidade;
4. estimativa de frequências;
5. estimativa e avaliação de riscos.

Isso reforça um encadeamento importante: a análise preliminar não substitui necessariamente estudos mais detalhados; ela frequentemente os antecede e os orienta.  

*(Fontes: `petroles-4ee4bce16acf674505c8912d:pNone:2424614.60-2424641.0`, `petroles-004c2afadba7ea17c7dd7908:pNone:3234099.60-3234129.0`)*

## 5.6 Bow Tie e análise de barreiras
O material menciona o uso de **Bow Tie** para representar logicamente um cenário acidental, conectando:
- **ameaças** ao
- **evento topo**, e deste às
- **consequências**,
com as respectivas **barreiras preventivas** e **barreiras mitigadoras**.

### Conceitos centrais
- **Ameaça**: ação ou fato capaz de liberar o perigo e produzir o evento topo;
- **Evento topo**: primeiro evento de uma cadeia que leva a consequências indesejáveis;
- **Barreiras preventivas**: atuam antes do evento topo, reduzindo a probabilidade de sua ocorrência;
- **Barreiras mitigadoras**: atuam após o evento topo, reduzindo a severidade das consequências;
- **Controles de fatores de degradação**: ações para manter a integridade das barreiras.

Um arranjo exemplificativo citado para instalações de produção inclui, no lado preventivo:
- contenção primária;
- controle básico do processo;
- alarmes críticos e intervenção humana;
- intertravamentos de segurança;
- sistemas de alívio.

E, no lado mitigador:
- sistemas de proteção pós-liberação;
- resposta à emergência da planta;
- resposta à emergência da instalação;
- evacuação, resgate e abandono.

Essa abordagem é especialmente útil para FPSOs porque conecta a análise de risco à integridade operacional das barreiras e ajuda a tratar desvios como inibições, modo manual, indisponibilidade temporária de salvaguardas e degradação de funções de segurança.  

*(Fontes: `petroles-004c2afadba7ea17c7dd7908:pNone:466560.0-466586.0`)*

## 6. Aplicação ao ciclo de vida de FPSOs/FSOs e sistemas subsea

### 6.1 Projeto e concepção
Na fase de projeto, a prioridade é antecipar perigos com informação ainda incompleta. A APR aparece como ferramenta de escolha para esse estágio, apoiando decisões de concepção e evitando retrabalho caro no detalhamento ou após a partida. O material também ressalta que experiências passadas nem sempre bastam para novas concepções; por isso, análises estruturadas devem considerar materiais, condições de processo, filosofia de segurança, intertravamentos e utilidades.  

*(Fontes: `regis-151b5a6f2316dd5a5fd5f15d:pNone:0.0-54.0`, `regis-161cd3328a094e3a98a6fa18:pNone:2114.0-2317.0`)*

### 6.2 Construção, comissionamento e partida
Nessas fases, a revisão de segurança por perguntas estruturadas ganha relevância, pois emergem riscos ligados a:
- limpeza e preparação antes da partida;
- acessibilidade de dispositivos de emergência;
- testes de alarmes e intertravamentos;
- riscos introduzidos pela manutenção e montagem;
- falhas combinadas de alimentação, instrumentação e utilidades.

Também é fase crítica para verificar se a instalação permanece em estado seguro diante de falhas de instrumentos, perda de alimentações e desvios de processo.  

*(Fontes: `regis-18675593ea42a9f6a427733f:pNone:7242.0-7478.0`)*

### 6.3 Operação e manutenção
Na operação, a análise de risco deve deixar de ser exercício estático. O material destaca que desvios de operação e manutenção podem degradar ou inibir temporariamente funções de segurança, levando à perda de integridade de barreiras. Isso é particularmente relevante em instalações marítimas, onde a indisponibilidade temporária de uma salvaguarda pode coexistir com transientes operacionais, condições meteorológicas e restrições logísticas.

Também se reforça a necessidade de revisões periódicas de segurança para instalações existentes, principalmente quando houver:
- repetitividade de incidentes e desvios;
- introdução de procedimentos especiais;
- potencial de consequências catastróficas;
- operações que modifiquem as condições originais de segurança.  

*(Fontes: `petroles-004c2afadba7ea17c7dd7908:pNone:466560.0-466586.0`, `regis-151b5a6f2316dd5a5fd5f15d:pNone:0.0-54.0`)*

### 6.4 Modificações e descomissionamento
Embora o material fornecido não trate detalhadamente de descomissionamento, ele deixa claro que as análises devem ser realizadas em qualquer momento do ciclo de vida. Logo, mudanças permanentes ou temporárias, reconfigurações operacionais, retirada de equipamentos de serviço, modificações em salvaguardas e atividades não rotineiras exigem reavaliação proporcional ao risco.  

*(Fontes: `regis-161cd3328a094e3a98a6fa18:pNone:2114.0-2317.0`)*

## 7. Fatores humanos e organizacionais
As fontes indicam que a segurança não depende apenas de tecnologia. Mesmo com automação crescente, o operador continua decisivo para a operação segura e econômica do processo. O material cita fatores como:
- fadiga;
- sonolência;
- diminuição da atenção;
- monotonia em tarefas repetitivas;
- falhas organizacionais;
- estilos de liderança inadequados;
- perda de habilidades de campo;
- comunicação e relações sociais de trabalho.

Há duas implicações práticas para análise de perigos e riscos:
1. cenários com erro humano e degradação organizacional devem ser considerados como cenários críveis;
2. a identificação de perigos é mais efetiva quando envolve trabalhadores da linha de frente e equipe multidisciplinar, e não apenas análise documental.

Isso é coerente com a recomendação de comitês de revisão envolvendo operação, projeto, processo e segurança, além do reconhecimento de que os profissionais da linha de frente identificam perigos reais do trabalho cotidiano com maior fidelidade.  

*(Fontes: `petroles-4ee4bce16acf674505c8912d:pNone:2215055.0-2215090.0`, `petroles-004c2afadba7ea17c7dd7908:pNone:1754353.0-1754396.0`, `regis-18675593ea42a9f6a427733f:pNone:7242.0-7478.0`)*

## 8. Barreiras, salvaguardas e elementos críticos
A análise de riscos não deve listar apenas causas e consequências; deve explicitar as **salvaguardas** e sua condição real. Nos materiais, as salvaguardas aparecem como camadas de proteção que dificultam que um evento inicial se propague para um acidente de maiores proporções.

Dentro dessa lógica, os chamados **elementos críticos de segurança operacional** são descritos, em referência indireta à ANP reproduzida pelo material, como equipamentos ou elementos estruturais cuja falha poderia causar ou contribuir significativamente para um quase-acidente ou acidente operacional.

Na prática analítica, isso exige:
- identificar quais barreiras são preventivas e quais são mitigadoras;
- verificar se estão disponíveis, testadas e adequadas;
- considerar degradação, inibição ou indisponibilidade temporária;
- priorizar cenários em que a consequência é crítica/catastrófica e a barreira esteja enfraquecida.

*(Fontes: `petroles-004c2afadba7ea17c7dd7908:pNone:1754353.0-1754396.0`, `petroles-004c2afadba7ea17c7dd7908:pNone:466560.0-466586.0`)*

## 9. Exemplo de raciocínio aplicado
### Exemplo 1 — perda de contenção em módulo de processo
Em uma análise preliminar de um módulo de separação/compressão de um FPSO, um cenário pode ser descrito assim:
- **evento indesejado**: vazamento de hidrocarboneto inflamável;
- **causas**: corrosão, falha de vedação, erro operacional, falha de instrumento, sobrepressão;
- **salvaguardas**: contenção primária, controle básico do processo, alarmes críticos com intervenção humana, intertravamentos de segurança, sistema de alívio;
- **consequências**: incêndio, explosão, lesões aos operadores, danos a equipamentos, perda de produção, dano ambiental;
- **classificação**: via severidade × frequência, considerando a eficácia real das barreiras.

Se uma das barreiras estiver inibida, em manual ou degradada, o nível de risco do cenário pode deixar de ser tolerável e exigir ação imediata ou análise mais detalhada.  

### Exemplo 2 — partida após manutenção
Numa revisão What-If/Checklist antes de partida, perguntas críticas seriam:
- a limpeza pré-partida foi verificada?
- alarmes e intertravamentos foram testados?
- existe risco de falha simultânea de alimentações relevantes?
- a instalação permanece fail-safe se instrumentos críticos falharem?
- a manutenção introduziu novos perigos ou removeu temporariamente salvaguardas?

Esse tipo de raciocínio mostra como a análise de perigos e riscos deve ser aplicada não só ao projeto, mas também às atividades operacionais e de manutenção.  

*(Fontes: `regis-18675593ea42a9f6a427733f:pNone:7242.0-7478.0`, `petroles-004c2afadba7ea17c7dd7908:pNone:1754353.0-1754396.0`, `petroles-004c2afadba7ea17c7dd7908:pNone:466560.0-466586.0`)*

## 10. Limitações e cuidados metodológicos
As fontes fornecidas apontam limites importantes que precisam ser explicitados em qualquer uso profissional do documento:
- análises de riscos dependem da qualidade das informações sobre processo e instalação;
- documentos desatualizados ou que não reflitam a operação real comprometem os resultados;
- há forte componente de julgamento subjetivo e experiência da equipe;
- equipes diferentes podem chegar a resultados diferentes para o mesmo processo;
- análises de risco de qualidade não garantem ausência de acidentes;
- benefícios relevantes exigem investimento contínuo em informação, equipe, treinamento e sustentação do programa ao longo da vida da instalação.

Também é necessário selecionar a técnica proporcionalmente à complexidade do problema. Aplicar um método excessivamente simples a um processo complexo pode deixar lacunas; aplicar um método excessivamente pesado a um problema simples pode desperdiçar recursos sem ganho proporcional de conhecimento.  

*(Fontes: `petroles-004c2afadba7ea17c7dd7908:pNone:3234099.60-3234129.0`, `petroles-004c2afadba7ea17c7dd7908:pNone:1754353.0-1754396.0`)*

## 11. Síntese operacional
Para fins profissionais, a lógica de análise de perigos e riscos em FPSOs/FSOs e produção subsea pode ser resumida assim:
1. **identificar perigos reais e cenários críveis** ao longo de todo o ciclo de vida;
2. **analisar causas, consequências, probabilidades e barreiras existentes**;
3. **classificar os riscos** por critérios consistentes, usualmente com matriz de risco;
4. **comparar com critérios de aceitabilidade/tolerabilidade**;
5. **tratar os riscos** por eliminação, prevenção, mitigação e reforço de barreiras;
6. **verificar eficácia e evitar criação de novos riscos**;
7. **reavaliar continuamente** quando houver desvios, mudanças, degradação de barreiras, novos dados ou incidentes.

Essa sequência é a essência técnica para demonstrar que os riscos foram identificados, compreendidos, priorizados e reduzidos a níveis toleráveis de forma rastreável e defensável.  

*(Fontes: `regis-161cd3328a094e3a98a6fa18:pNone:2114.0-2317.0`, `regis-474ad04a90c2f8f651b08d76:pNone:7724.0-7944.0`, `regis-474ad04a90c2f8f651b08d76:pNone:7838.0-8150.0`, `petroles-004c2afadba7ea17c7dd7908:pNone:1754353.0-1754396.0`, `petroles-004c2afadba7ea17c7dd7908:pNone:466560.0-466586.0`)