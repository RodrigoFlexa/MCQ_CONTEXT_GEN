# SIMOPS em FPSOs: coordenação e comunicação

## 1. Premissas desta faceta
Em operações simultâneas (SIMOPS) em FPSOs, a coordenação e a comunicação funcionam como barreiras organizacionais para evitar que atividades concorrentes degradem a percepção situacional, sobrecarreguem funções críticas, criem lacunas de autorização ou inviabilizem a resposta a desvios e emergências. Neste documento, o foco está na integração entre funções e equipes antes e durante a execução das atividades, com ênfase em CCR/CCRM, OIM, marinha, produção, manutenção, logística/embarque, contratadas e equipes de resposta.

Os trechos utilizados mostram sobretudo: (a) práticas de priorização e planejamento de recursos; (b) achados de auditoria da ANP sobre SGSO/EOR; e (c) lições de um acidente real, que evidenciam falhas de comunicação, passagem de serviço, distribuição de tarefas e comando operacional. Portanto, o conteúdo deve ser lido como base técnica e analítica, não como prescrição normativa fechada.

**Fontes:** `anp-2621377f5c5478141437d2bf:p27-29:8.0-19.0`, `anp-2621377f5c5478141437d2bf:p28-30:17.0-22.0`, `anp-dabfb60617e4f0ede433578e:p21-23:7.0-26.0`, `anp-dabfb60617e4f0ede433578e:p22-25:29.0-14.0`

## 2. Coordenação como barreira organizacional em SIMOPS
A coordenação de SIMOPS não se resume a autorizar trabalhos em paralelo. Ela depende de uma estrutura capaz de:

- saber **quais operações estão em curso** e onde;
- identificar **quem decide, quem executa e quem supervisiona**;
- manter visível o estado de **barreiras, sensores, alarmes, válvulas, permissões e inibições**;
- controlar **sobrecarga humana**, acúmulo de funções e lacunas de competência;
- assegurar que mudanças de escopo, de pessoal ou de condição operacional sejam tratadas por **gestão de mudanças**;
- garantir que uma condição anormal leve rapidamente à revisão das atividades em andamento, podendo resultar em **parada, suspensão ou reorganização**.

Os achados de auditoria citados pela ANP reforçam que falhas recorrentes de segurança operacional incluem: recomendações de análises de risco não implementadas, coordenação inadequada com empresas contratadas em cenários críticos, planos de emergência com composição mínima indefinida, ausência de definição de funções incompatíveis dentro da estrutura de resposta, e problemas documentais que dificultam a passagem de serviço e o acompanhamento de permissões de trabalho e inibições.

Em termos práticos de SIMOPS, isso significa que o controle da interface entre equipes não pode depender apenas de experiência informal ou de arranjos tácitos. A instalação precisa conseguir demonstrar, em cada janela operacional, a coerência entre: pessoas disponíveis, competências, cadeia de comando, estado dos sistemas e documentação operacional vigente.

**Fontes:** `anp-2621377f5c5478141437d2bf:p27-29:8.0-19.0`, `anp-2621377f5c5478141437d2bf:p28-30:17.0-22.0`

## 3. Estrutura de autoridade, papéis e incompatibilidades funcionais
Os materiais apontam que o OIM exerce papel central tanto no comando da instalação quanto na resposta a emergências. Em auditorias da ANP, foi considerada crítica a operação sem OIM a bordo, e também foram identificadas falhas nos PREs por não definirem adequadamente a composição mínima da estrutura organizacional de resposta e as coincidências de funções que **não deveriam ser acumuladas por uma mesma pessoa**.

No caso investigado do FPSO Cidade de São Mateus, durante a emergência a CCR foi o ponto de encontro do OIM/CIO, fiscal da Petrobras, superintendentes de marinha, manutenção e produção, operador de rádio, operadores da sala de controle e time técnico de resposta. Também foi evidenciado que algumas pessoas exerceram funções diferentes das previstas no PRE e que não havia substituto designado para uma função prevista de comando de incidentes. Isso mostra um ponto crítico para SIMOPS: quando há ambiguidade de papéis ou ausência de suplência formal, a coordenação degrada justamente no momento em que a instalação mais precisa de clareza decisória.

Para a coordenação rotineira de SIMOPS, três princípios se destacam a partir das fontes:

1. **Autoridade decisória explícita:** deve estar claro quem prioriza, quem aprova e quem pode suspender atividades.
2. **Incompatibilidades funcionais mapeadas:** certas combinações de funções podem introduzir conflito de atenção, perda de independência ou inviabilidade de resposta.
3. **Suplência e contingência de pessoal:** redução de POB, ausência temporária de supervisão ou troca de equipe precisam ser avaliadas formalmente, e não tratadas como mera adaptação operacional.

Esses elementos são especialmente relevantes em SIMOPS porque a mesma pessoa pode ser simultaneamente demandada por produção, manutenção, marinha, PT, resposta a alarmes e interface com contratadas. Se a organização não definir limites, a capacidade de monitoramento e decisão se deteriora.

**Fontes:** `anp-2621377f5c5478141437d2bf:p27-29:8.0-19.0`, `anp-dabfb60617e4f0ede433578e:p21-23:7.0-26.0`, `anp-dabfb60617e4f0ede433578e:p187-190:21.0-9.0`

## 4. Rotinas de coordenação antes da execução
Os trechos do REGIS mostram um encadeamento útil para a fase pré-execução: necessidade identificada em notificação, priorização em reunião multidisciplinar, eventual geração de ordem de serviço e posterior planejamento de embarque dos recursos necessários. Embora o caso descrito trate de manutenção/corrosão, a lógica é aplicável à preparação de atividades simultâneas em geral.

### 4.1 Registro e priorização multidisciplinar
As notificações M2 são usadas para registrar defeitos/não funcionamento e demandar manutenção. A priorização ocorre em **reuniões diárias** com participação de operações, modificações, perfurações e contratadas. Dessa priorização pode resultar ou não uma ordem de serviço. Quando gerada, a ordem de serviço passa a integrar planejamento e cronograma, aumentando a visibilidade interdepartamental.

Para SIMOPS, o valor técnico dessa rotina é que ela cria um fórum para:

- comparar urgência versus impacto operacional;
- identificar interfaces entre atividades de áreas distintas;
- antecipar conflitos por recursos, pessoal ou janela operacional;
- decidir se uma demanda entra na carteira executável ou permanece pendente.

### 4.2 Planejamento de embarque e capacidade de POB
Os mesmos trechos destacam que as plataformas têm limitação de capacidade para receber e acomodar pessoas, e que isso restringe novos projetos e operações rotineiras. O planejamento de embarque é tratado em reuniões semanais para curto prazo, mensais para médio prazo e semestrais para longo prazo. O **OIM prioriza, consolida e aceita** o plano de embarque da plataforma.

Em SIMOPS, esse ponto é decisivo: não basta que duas atividades sejam tecnicamente compatíveis; elas também precisam ser compatíveis com a capacidade de POB, alojamento, supervisão, resposta a emergências e suporte logístico. A limitação de vagas embarcadas afeta diretamente:

- disponibilidade de supervisão dedicada;
- presença de especialistas e contratadas críticas;
- robustez da EOR em caso de contingência;
- qualidade da execução simultânea sem sobrecarga de funções.

### 4.3 Conteúdo mínimo útil de coordenação prévia
Com base na combinação das fontes, a comunicação anterior ao início de SIMOPS deve consolidar, pelo menos:

- atividades ativas e planejadas por área/sistema;
- responsáveis operacionais e autoridade de aprovação;
- restrições de POB, embarque e competências disponíveis;
- PTs relevantes e interfaces entre trabalhos;
- estado de sensores, inibições e indisponibilidades conhecidas;
- mudanças recentes de pessoal, operador ou procedimento que afetem a execução.

**Fontes:** `regis-d076397a916231f2219e023e:pNone:2334.0-2612.0`, `anp-2621377f5c5478141437d2bf:p27-29:8.0-19.0`, `anp-2621377f5c5478141437d2bf:p28-30:17.0-22.0`

## 5. Comunicação durante a execução: CCR/CCRM, campo e equipes locais
Os trechos sobre o sistema de transferência de carga do FPSO CDSM mostram uma interface típica de SIMOPS em FPSO: parte da operação é comandada na CCRM pelo operador de marinha, mas algumas válvulas são operadas localmente no convés superior e na casa de bombas pelo bombeador, sob ordem específica. Além disso, nem todas as válvulas enviavam automaticamente à CCR a confirmação de posição; em certos casos, o operador precisava **inserir manualmente** na IHM a informação de estado.

Essa arquitetura tem implicações operacionais importantes:

- a situação real de campo pode não estar integralmente refletida na tela, dependendo de confirmação humana;
- a sequência de manobra exige comunicação confiável entre CCR/CCRM e executante local;
- o risco de erro aumenta quando a mesma equipe acumula operação, controle de PTs e acompanhamento de outras atividades no convés.

Do ponto de vista de coordenação e comunicação, a operação simultânea de sistemas com comando distribuído exige, no mínimo, disciplina em três níveis:

1. **Comando:** quem dá a ordem e com base em qual condição operacional.
2. **Confirmação:** quem confirma a execução local e como essa informação retorna ao centro de controle.
3. **Registro situacional:** como a equipe assegura que a posição exibida, a posição real e o entendimento compartilhado sejam consistentes.

Quando há atividades paralelas na mesma área ou sistema, essa interface tende a se tornar mais crítica. Uma equipe pode interpretar que um sistema está isolado, parado ou seguro com base em informação de tela, enquanto outra ainda atua localmente. Por isso, o simples fato de existir supervisório não elimina a necessidade de comunicação fechada, confirmação de campo e alinhamento de turno.

**Fontes:** `anp-dabfb60617e4f0ede433578e:p92-97:10.0-21.0`, `anp-dabfb60617e4f0ede433578e:p194-196:12.0-37.0`

## 6. Distribuição de tarefas, sobrecarga e passagem de serviço
Os trechos da ANP mostram que pessoas com o mesmo cargo podem, na prática, desempenhar funções muito diferentes. No caso analisado, operadores de marinha expatriados e brasileiros tinham o mesmo título, mas os expatriados concentravam atividades operacionais: acompanhamento do supervisório, alinhamentos entre tanques, leitura de P&ID, partida/parada de bombas e comunicação operacional com o bombeador. Já os brasileiros ficavam mais ligados a documentação, registros e emissão de PTs, especialmente em movimentações de guindaste e serviços de convés.

Essa assimetria produziu efeitos relevantes para SIMOPS:

- **sobrecarga do operador mais experiente**, que acumulava operação do sistema, controle de manutenção em curso, planejamento e, em certos períodos, funções de superintendência;
- **baixa redundância cognitiva**, pois o conhecimento operacional ficava concentrado em poucos indivíduos;
- **passagem de serviço deficiente**, inclusive por falta de tempo para transmitir o andamento das operações;
- **desbalanceamento entre quem conhece o sistema e quem controla a documentação**, o que pode gerar lacunas entre a condição real da planta e o que está formalmente autorizado.

Os materiais também indicam que a fluência em inglês e a experiência offshore influenciavam a distribuição real de funções. Em ambiente de SIMOPS, isso é crítico, porque diferenças de idioma, experiência ou familiaridade com a unidade podem afetar a qualidade do entendimento compartilhado entre OIM, supervisores, CCR, contratadas e equipes locais.

Além disso, a investigação identificou ausência de aplicação adequada de gestão de mudanças para alterações de pessoal, bem como falta de tutoria efetiva e handover insuficiente para novo superintendente de marinha. A combinação de troca de pessoas, baixa familiarização com a unidade e necessidade de decidir sobre operações em curso reduziu a robustez da coordenação.

Em síntese, para SIMOPS, a passagem de serviço não é mera formalidade administrativa; ela é mecanismo de transferência de risco operacional. Ela precisa preservar, de forma inteligível para a equipe seguinte:

- atividades simultâneas em aberto;
- restrições e desvios temporários;
- PTs relevantes e suas interfaces;
- inibições/bypasses existentes;
- limitações de pessoal, treinamento e supervisão.

**Fontes:** `anp-dabfb60617e4f0ede433578e:p187-190:21.0-9.0`, `anp-dabfb60617e4f0ede433578e:p194-196:12.0-37.0`, `anp-2621377f5c5478141437d2bf:p28-30:17.0-22.0`

## 7. Comunicação sob condição anormal ou emergência durante SIMOPS
Os trechos sobre a emergência no FPSO Cidade de São Mateus mostram como a coordenação precisa migrar rapidamente do modo rotineiro para o modo de contingência.

Quando soou o alarme de gás, o OIM dirigiu-se à CCR, foi informado da detecção na casa de bombas, fez anúncio público em inglês e depois em português, requisitou informações sobre as operações em curso e, ao saber da transferência de carga entre tanques, ordenou a parada do bombeio e o fechamento das válvulas do sistema. Em seguida, convocou uma **reunião de situação (time out meeting)** para atualizar a equipe da CCR sobre operações em curso, condições da emergência e status de reunião de pessoas a bordo.

Esse trecho evidencia um ponto essencial para SIMOPS: diante de desvio relevante, a primeira necessidade de coordenação é reconstruir rapidamente a **imagem operacional comum**, respondendo a perguntas como:

- o que estava acontecendo no momento do alarme;
- quais operações de processo/marinha/manutenção estavam em andamento;
- quem estava em cada área;
- quais sistemas precisavam ser parados ou isolados;
- qual o estado das equipes de resposta e dos pontos de encontro.

Ao mesmo tempo, o caso mostra vulnerabilidades graves de comunicação:

- a equipe da CCR não soube precisar a substância nem a quantidade vazada;
- detectores e alarmes foram inibidos, o que impediu a atuação automática prevista pela matriz de causa e efeito;
- uma equipe foi autorizada a entrar em área com presença confirmada de gás inflamável;
- houve falha de entendimento entre brigadista e comandante em cena devido à dificuldade de fala com equipamento autônomo de respiração, agravada pela transmissão verbal da informação;
- a comunicação ocorreu em mais de um idioma, o que aumenta a necessidade de padronização das mensagens críticas.

Para coordenação de SIMOPS, a lição técnica é clara: em condição anormal, a comunicação deve privilegiar mensagens curtas, inequívocas, confirmadas e rastreáveis, especialmente sobre:

- atmosfera perigosa e leitura de detectores portáteis/fixos;
- autorização de entrada em áreas afetadas;
- suspensão ou continuidade de trabalhos simultâneos;
- inibição de alarmes/sensores e suas consequências operacionais;
- localização e prontidão das equipes.

Também fica evidente que a reunião de situação só é efetiva se incluir os atores necessários ou, no mínimo, se houver fluxo confiável entre o centro de comando e os líderes de campo. A ausência desses elos fragiliza tanto a decisão quanto a execução.

**Fontes:** `anp-dabfb60617e4f0ede433578e:p21-23:7.0-26.0`, `anp-dabfb60617e4f0ede433578e:p22-25:29.0-14.0`

## 8. Controle documental e continuidade operacional
Os achados da ANP sobre mudança de operador e auditorias SGSO ressaltam que problemas de registros e de controle documental relacionados a **permissões de trabalho, inibições de sensores e gestão de mudança** dificultam a passagem de serviço. Em SIMOPS, esse ponto é estrutural: comunicação verbal sem suporte documental atualizado não sustenta controle seguro de interfaces.

A documentação operacional relevante para coordenação não é apenas evidência administrativa; ela é parte do mecanismo de alinhamento entre equipes. Quando PTs, inibições, treinamentos, análises de risco ou procedimentos não estão formalmente validados, disponibilizados e entendidos pela força de trabalho, a tendência é que diferentes grupos atuem com premissas distintas sobre a mesma instalação.

Isso é ainda mais sensível em contextos de troca de operador, entrada de contratadas, mudança de efetivo ou adoção de novos procedimentos. Nesses cenários, a coordenação eficiente depende de que a informação crítica esteja ao mesmo tempo:

- formalmente controlada;
- acessível à força de trabalho;
- coerente com a condição real da unidade;
- transferida adequadamente na passagem de turno e de gestão.

**Fontes:** `anp-2621377f5c5478141437d2bf:p28-30:17.0-22.0`, `anp-dabfb60617e4f0ede433578e:p194-196:12.0-37.0`

## 9. Síntese técnica para avaliação profissional
A partir das fontes, a coordenação e a comunicação em SIMOPS de FPSOs podem ser avaliadas por alguns eixos técnicos principais:

- **clareza de papéis e autoridade:** OIM, CCR/CCRM, supervisões, líderes de campo e contratadas sabem quem aprova, coordena e suspende;
- **qualidade das rotinas prévias:** há reuniões de priorização, planejamento de embarque/POB e consolidação das atividades concorrentes;
- **robustez da interface centro de controle-campo:** manobras remotas e locais têm confirmação confiável e entendimento comum do estado do sistema;
- **qualidade do handover:** a equipe seguinte recebe o quadro real das atividades simultâneas, desvios, limitações e barreiras degradadas;
- **tratamento formal de mudanças:** alterações de pessoal, função, operador ou procedimento passam por gestão de mudanças;
- **disciplina comunicacional em anormalidades:** alarmes, atmosfera perigosa, suspensão de atividades e autorização de acesso são tratados com mensagens inequívocas e rastreáveis.

A falha em qualquer um desses eixos tende a amplificar os riscos combinados típicos de SIMOPS, porque a instalação deixa de operar com uma visão integrada das interfaces entre pessoas, sistemas, áreas e barreiras.

**Fontes:** `regis-d076397a916231f2219e023e:pNone:2334.0-2612.0`, `anp-2621377f5c5478141437d2bf:p27-29:8.0-19.0`, `anp-2621377f5c5478141437d2bf:p28-30:17.0-22.0`, `anp-dabfb60617e4f0ede433578e:p21-23:7.0-26.0`, `anp-dabfb60617e4f0ede433578e:p22-25:29.0-14.0`, `anp-dabfb60617e4f0ede433578e:p92-97:10.0-21.0`, `anp-dabfb60617e4f0ede433578e:p187-190:21.0-9.0`, `anp-dabfb60617e4f0ede433578e:p194-196:12.0-37.0`