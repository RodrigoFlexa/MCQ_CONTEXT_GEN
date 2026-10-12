# Perigos, riscos e gerenciamento de mudanças no SGSO de FPSOs

## 1. Função desses temas dentro do SGSO

No contexto do Sistema de Gerenciamento da Segurança Operacional (SGSO), a identificação de perigos, a análise de riscos e o gerenciamento de mudanças formam um encadeamento lógico de controle:

1. **identificar o que pode dar errado**;
2. **entender causas, consequências e barreiras**;
3. **avaliar se o risco é tolerável/aceitável ou requer redução adicional**; e
4. **assegurar que qualquer mudança ao longo da vida da unidade não degrade o nível de segurança originalmente concebido**.

As fontes consultadas convergem em um ponto central: o gerenciamento de riscos é elemento-chave do sistema de gestão de segurança operacional e visa orientar a alocação equilibrada de recursos para controle e mitigação dos riscos viáveis. Nessa lógica, as barreiras de segurança são tratadas como camadas de proteção; quando essas camadas falham ou apresentam fragilidades simultâneas, aumenta a probabilidade de materialização de eventos de maior gravidade.

A representação por **Bow-tie** ajuda a visualizar essa lógica: à esquerda ficam as ameaças/causas que podem levar ao evento principal; no centro, o evento perigoso; à direita, as consequências; e entre esses elementos, as barreiras preventivas e mitigadoras. Em paralelo, a chamada **teoria do queijo suíço** descreve que acidentes organizacionais tendem a ocorrer quando fragilidades de múltiplas barreiras se alinham, incluindo falhas ativas e condições latentes.

**Conceitos úteis**:
- **Perigo**: fonte, condição ou situação com potencial de causar dano.
- **Risco**: combinação de probabilidade e consequência da consumação do perigo.
- **Barreira de segurança**: medida física, administrativa, humana ou organizacional voltada a prevenir, controlar ou mitigar um evento indesejado.

*Fontes da seção: `regis-161cd3328a094e3a98a6fa18:pNone:2319.0-2527.0`, `regis-962e222ee3c37dec82110fd6:pNone:3831.0-4085.0`*

## 2. Processo de avaliação de riscos aplicável ao ciclo de vida

As fontes descrevem a avaliação de riscos como um processo estruturado para apoiar decisões e manter riscos em níveis toleráveis. Uma sequência técnica coerente para FPSOs, compatível com os trechos fornecidos, inclui:

### 2.1 Etapas principais

- **Definição da metodologia de análise de riscos**.
- **Identificação de perigos e classificação dos riscos**.
- **Identificação dos grandes eventos acidentais** e análise das barreiras associadas.
- **Quantificação dos riscos** relacionados aos grandes eventos acidentais, quando cabível.
- **Avaliação de aceitabilidade** dos riscos e definição de medidas adicionais.

### 2.2 Escolha do nível metodológico

As fontes distinguem três níveis de abordagem:

- **Qualitativa (Q)**: frequência e severidade definidas qualitativamente, com base na experiência da equipe.
- **Semi-quantitativa (SQ)**: frequência e severidade aproximadas dentro de faixas numéricas.
- **Quantitativa (QRA)**: quantificação explícita de frequências e consequências, especialmente para grandes eventos acidentais.

O princípio decisório explicitado é que **o grau de complexidade da metodologia deve ser proporcional à magnitude do risco e à complexidade da atividade**. Em termos práticos para FPSOs:

- mudanças simples e de baixo impacto podem admitir avaliação qualitativa bem estruturada;
- mudanças com potencial de afetar inventário de hidrocarbonetos, layout, segregação, detecção, alívio, desligamento, evacuação ou integridade de barreiras demandam aprofundamento;
- cenários de grandes acidentes tipicamente requerem estudos mais robustos, podendo chegar a QRA.

### 2.3 Aplicação ao ciclo de vida da unidade

Os trechos da ANP sobre o **Safety Case** do FPSO Cidade de São Mateus mostram que os estudos de segurança não são restritos à operação. O manual citado no relatório indica aplicabilidade a:

- **novos projetos**,
- **conversões**,
- **modificações ou aprimoramentos**, e
- **embarcações existentes**.

Isso é consistente com a ideia de SGSO ao longo de todo o ciclo de vida: projeto, construção, instalação, comissionamento, operação, modificações e, por extensão lógica de gestão, fases de encerramento/desativação também exigem reavaliação dos perigos e das barreiras pertinentes.

*Fontes da seção: `regis-962e222ee3c37dec82110fd6:pNone:1327.0-1567.0`, `anp-dabfb60617e4f0ede433578e:p69-72:23.0-19.0`*

## 3. Técnicas de identificação de perigos e análise de riscos

## 3.1 HAZID

O **HAZID (Hazard Identification)** é descrito como técnica qualitativa voltada a:

- identificar perigos;
- levantar causas e consequências;
- classificar riscos associados; e
- identificar medidas de controle/barreiras preventivas e corretivas.

Seu papel é particularmente importante nas fases iniciais ou em revisões amplas da instalação, pois gera base para estudos posteriores. Os resultados do HAZID subsidiam a delimitação de ações necessárias para manter os riscos sob controle.

Para FPSOs, o HAZID tende a ser útil em temas como:
- inventários e liberação de hidrocarbonetos;
- gases tóxicos, como H2S, quando aplicável ao fluido/processo;
- colisão, queda de carga, incêndio/explosão, falha de utilidades e perda de contenção;
- interfaces marítimas, processo, acomodações, evacuação e resposta a emergências;
- mudanças operacionais, organizacionais e de escopo.

## 3.2 HAZOP

O **HAZOP (Hazard and Operability Study)** é apresentado como técnica qualitativa e multidisciplinar focada em **desvios de variáveis de processo**, como:

- pressão,
- temperatura,
- vazão/fluxo,
- nível.

Cada desvio é analisado quanto a **causas e consequências**. Pelas fontes, o HAZOP é particularmente apropriado para:
- a **fase de projeto**, e
- **alterações em processos existentes**.

Em FPSOs, isso o torna especialmente pertinente para topsides de processo, utilidades, flare/vent, sistemas de exportação e interfaces onde mudanças operacionais ou físicas possam introduzir novos desvios relevantes.

## 3.3 QRA e estudos complementares

O relatório da ANP sobre o FPSO Cidade de São Mateus cita um conjunto de estudos formais usados como base do Safety Case, incluindo:

- **HAZID**;
- **HAZOP** de sistemas marítimos e de processo;
- **QRA (Quantified Risk Assessment)**;
- estudos de dispersão de gases;
- **FEA (Fire and Explosion Assessment)**;
- **ETRERA** para escape, refúgio temporário, evacuação e resgate;
- **ESSA** para sobrevivência de sistemas de emergência.

Esse conjunto evidencia que, para unidades complexas como FPSOs, a análise de riscos é normalmente **multitécnica**, não se esgotando em uma única ferramenta.

## 3.4 Criticidade e aprofundamento analítico

Uma das fontes acadêmicas indica critérios gerais para escolher técnicas de identificação de perigos: **fase do projeto, nível de detalhamento desejado, tempo e recursos disponíveis**. A mesma fonte mostra que, quando certos desvios são classificados como mais críticos, pode haver aprofundamento por:

- **árvores de falhas**;
- **diagramas de sequência de eventos**;
- ou quantificação probabilística adicional.

Também apresenta, em contexto de priorização técnica, o uso de um **número de priorização de risco (RPN)**:

**RPN = O x G x D**

onde:
- **O** = probabilidade/ocorrência,
- **G** = gravidade,
- **D** = potencial de detecção.

Essa formulação é útil como exemplo de priorização, mas não aparece nas fontes como requisito específico do SGSO/ANP para FPSOs.

*Fontes da seção: `regis-962e222ee3c37dec82110fd6:pNone:1327.0-1567.0`, `regis-161cd3328a094e3a98a6fa18:pNone:2319.0-2527.0`, `anp-dabfb60617e4f0ede433578e:p69-72:23.0-19.0`, `regis-2bc1d7ed973c40eb10c4dfe8:pNone:56.0-106.0`*

## 4. Grandes eventos acidentais, barreiras e aceitabilidade do risco

Os trechos fornecidos permitem estruturar a gestão dos grandes eventos acidentais em torno de três perguntas:

### 4.1 Quais eventos merecem atenção especial?

Eventos com potencial de impacto severo à vida humana, ao meio ambiente, aos equipamentos e ao negócio devem receber tratamento diferenciado. Uma fonte utiliza a ideia de área de atenção para **Major Accident Hazard Identification** e destaca que tais cenários exigem gerenciamento específico.

### 4.2 Quais barreiras previnem ou mitigam esses eventos?

A análise de riscos deve ir além da listagem de perigos e identificar:
- barreiras **preventivas** que reduzem a chance do evento topo;
- barreiras **mitigadoras** que reduzem as consequências após a ocorrência.

A visualização Bow-tie é útil para isso, pois conecta ameaças, evento principal, consequências e barreiras, facilitando entendimento e comunicação.

### 4.3 O risco foi reduzido o suficiente?

No caso citado pela ANP, o Safety Case buscava demonstrar que:
- todos os perigos relevantes foram identificados;
- os riscos foram avaliados; e
- as medidas de controle adotadas reduziram o risco a nível **ALARP** (*as low as reasonably practicable*), isto é, tão baixo quanto razoavelmente praticável.

Para uso técnico-profissional, o conceito importante não é transformar ALARP em obrigação geral brasileira por analogia automática, mas reconhecer o princípio de que a redução adicional de risco precisa ser analisada à luz de benefício de segurança, viabilidade e consistência com o arranjo regulatório aplicável.

*Fontes da seção: `anp-dabfb60617e4f0ede433578e:p69-72:23.0-19.0`, `regis-161cd3328a094e3a98a6fa18:pNone:2319.0-2527.0`, `regis-962e222ee3c37dec82110fd6:pNone:3831.0-4085.0`*

## 5. Gerenciamento de Mudanças (MOC) no SGSO

## 5.1 Finalidade

As fontes definem o **Gerenciamento de Mudanças (Management of Change - MOC)** como um conjunto de princípios, diretrizes e prática formal escrita destinado a garantir que mudanças não reduzam a segurança prevista na condição original de projeto/operação. É descrito como processo contínuo ao longo de toda a vida da instalação.

Em termos técnicos, o MOC serve para impedir que alterações aparentemente localizadas introduzam:
- novos perigos;
- aumento de frequência de cenários acidentais;
- aumento de severidade de consequências;
- degradação ou ineficácia de barreiras existentes;
- incompatibilidades documentais, operacionais ou organizacionais.

## 5.2 Que tipos de mudança merecem tratamento formal?

Os trechos usados apontam que instalações de processamento estão sujeitas a modificações contínuas para desempenho, eficiência, segurança e incorporação de novas tecnologias. Como exemplos de gatilhos de MOC aparecem:

### a) Mudanças tecnológicas e de processo
- alteração de condições operacionais, como **pressões, temperaturas e vazões**;
- mudanças em sistemas de instrumentação e controle;
- alterações em materiais de construção;
- inclusão de novos produtos químicos;
- modificação com impacto em sistemas de alívio e despressurização;
- mudança de procedimentos de partida, parada, emergência ou operação fora dos limites usuais.

### b) Mudanças físicas na planta/unidade
- substituição de equipamentos por itens diferentes dos originais;
- interligações provisórias;
- **bypasses**;
- conexões, tubulações, mangueiras ou instalações temporárias;
- reparos temporários ou improvisados.

### c) Mudanças na força de trabalho e organização
- troca de operador da instalação ou do contrato;
- alterações em passagem de turno, substituições e composição das equipes;
- uso de pessoal novo sem treinamento adequado;
- arranjos organizacionais que acumulem funções críticas.

Essa última categoria é particularmente relevante no SGSO, porque mudanças organizacionais podem modificar autoridade decisória, competência disponível, fluxo de informações e capacidade de resposta a emergências, mesmo sem qualquer alteração física no FPSO.

## 5.3 Conteúdo mínimo de uma avaliação de mudança

A fonte técnica secundária usada sobre gerenciamento de modificações, em linha com exemplos observados pela ANP, indica que o processo formal deve considerar, no mínimo:

- bases de projeto e premissas do processo/mecânica afetadas;
- implicações de segurança, saúde e meio ambiente da mudança proposta;
- impacto da mudança a montante e a jusante do sistema alterado;
- necessidade de alterar procedimentos operacionais;
- divulgação da mudança e de suas implicações ao pessoal envolvido;
- geração/atualização da documentação técnica antes da implementação;
- duração da mudança, especialmente se for temporária;
- obtenção das autorizações gerenciais e, quando aplicável, externas.

## 5.4 Por que o MOC é crítico em FPSOs?

Porque o FPSO reúne sistemas altamente integrados: processo, utilidades, casco/sistemas marítimos, geração de energia, detecção e combate a incêndio, telecomunicações, acomodação, evacuação, interfaces submarinas e, frequentemente, contratadas múltiplas. Pequenas mudanças podem gerar efeitos cruzados não triviais.

Exemplos típicos de encadeamentos perigosos:
- mudança em setpoint, lógica ou bypass de instrumentação -> alteração da resposta de proteção -> aumento da probabilidade de perda de contenção;
- interligação temporária -> nova rota de fluxo ou acúmulo de inventário -> cenário não previsto no HAZOP original;
- troca de operador/procedimento -> perda de aderência entre prática real, documentos e treinamentos -> falhas humanas e organizacionais;
- mudança na equipe mínima ou acumulação de funções -> redução da capacidade de supervisão e resposta.

*Fontes da seção: `regis-161cd3328a094e3a98a6fa18:pNone:2319.0-2527.0`, `regis-962e222ee3c37dec82110fd6:pNone:1327.0-1567.0`, `petroles-004c2afadba7ea17c7dd7908:pNone:3234240.0-3234268.0`, `anp-2621377f5c5478141437d2bf:p28-30:17.0-22.0`*

## 6. Mudanças organizacionais e troca de operador como mudanças de segurança operacional

Um ponto forte dos trechos da ANP é mostrar que **mudança de operador** não é mero evento contratual/administrativo; trata-se de mudança com potencial direto sobre o SGSO.

A ANP registrou não conformidades com potencial de afetar a segurança operacional durante processos de alteração de operadores, incluindo:

- falta de entendimento de que alterações no SGSO decorrentes de aquisições, trocas e fusões devem passar por **gerenciamento de mudanças**;
- falhas na transferência de informações essenciais entre operadores;
- passivos de manutenção em **Sistemas/Elementos Críticos de Segurança Operacional**;
- ausência de validação formal, pelo novo operador, das análises de risco e estudos de segurança do operador anterior;
- falhas de treinamento/reciclagem do pessoal nos novos procedimentos;
- falhas na disponibilização dos procedimentos operacionais aplicáveis;
- problemas de registros e controle documental de permissões de trabalho, inibições de sensores e gestão de mudança.

Do ponto de vista técnico, isso significa que uma mudança organizacional pode invalidar pressupostos de risco anteriormente aceitos, por exemplo:
- a equipe pode deixar de conhecer corretamente as barreiras e seus limites;
- procedimentos vigentes podem não corresponder à prática operacional real;
- pendências documentais podem ocultar condições degradadas;
- históricos de incidentes e de desvios podem se perder na transição.

A mesma lógica aparece no relatório de investigação do FPSO Cidade de São Mateus, que apontou dependência técnica excessiva da equipe local em relação ao exterior para temas como:
- gerenciamento de mudanças,
- controle de documentação,
- atualização de desenhos,
- traduções de documentos,
- investigação de acidentes.

Isso evidencia que **estrutura organizacional, autonomia técnica local e suporte de engenharia/segurança** também são componentes de controle de risco.

*Fontes da seção: `anp-2621377f5c5478141437d2bf:p28-30:17.0-22.0`, `anp-dabfb60617e4f0ede433578e:p69-72:23.0-19.0`*

## 7. Revalidação de perigos e riscos após mudanças ou aprendizado operacional

Os materiais indicam claramente que estudos iniciais de projeto não bastam por si só. Eles precisam ser **revistos, validados ou complementados** quando surgem novas condições operacionais, novas informações ou novas interfaces.

Um exemplo relevante citado pela ANP foi a **detecção de H2S aprisionado em riser de produção de 6"**, cenário que **não havia sido considerado no HAZID de projeto** da unidade. A lição técnica é direta:

- a identificação de perigos pode ficar incompleta;
- o aprendizado operacional revela cenários não previstos;
- mudanças de fluido, escoamento, condição operacional ou configuração podem exigir revisão dos estudos;
- a ausência dessa revisão pode deixar barreiras inadequadas, mal especificadas ou inexistentes.

Assim, a gestão eficaz no SGSO requer um ciclo de retroalimentação:

1. resultados de operação, incidentes, inspeções e auditorias;
2. revisão de perigos, cenários e barreiras;
3. implementação de recomendações e ações corretivas/preventivas;
4. atualização documental e treinamento;
5. monitoramento da eficácia.

*Fontes da seção: `anp-2621377f5c5478141437d2bf:p28-30:17.0-22.0`, `regis-962e222ee3c37dec82110fd6:pNone:1327.0-1567.0`*

## 8. Relação entre análise de riscos, integridade e prontidão operacional

As fontes também mostram que perigo, risco e mudança não podem ser tratados isoladamente da integridade operacional. Foram citados pela ANP casos de:

- plano de manutenção, teste e inspeção de equipamento crítico não cumprido conforme recomendação do fabricante;
- corrosão acentuada em equipamentos;
- sistema de combate a incêndio inoperante;
- falta de sobressalentes para manter disponibilidade de equipamentos críticos;
- operação com deficiência em meios de abandono/resposta;
- problemas na estrutura organizacional de resposta a emergências.

Sob a ótica de gestão de risco, isso significa que a análise só é efetiva quando se conecta à **manutenção da performance das barreiras**. Uma barreira identificada no estudo perde valor prático se estiver indisponível, degradada, vencida para manutenção, sem sobressalente ou sem equipe treinada para acioná-la.

Em FPSOs, esse vínculo é essencial para:
- detecção de gás e fogo;
- isolamento e desligamento de emergência;
- despressurização e flare/vent;
- combate a incêndio;
- evacuação, refúgio temporário e resgate;
- integridade de contenção e dos sistemas de processo.

*Fontes da seção: `anp-2621377f5c5478141437d2bf:p28-30:17.0-22.0`, `regis-962e222ee3c37dec82110fd6:pNone:1327.0-1567.0`*

## 9. Critérios práticos para avaliar maturidade do tema no SGSO

Com base na síntese dos trechos, um processo maduro de perigos, riscos e gerenciamento de mudanças em FPSO tende a apresentar evidências de que:

### 9.1 Identificação de perigos
- cobre projeto, operação, transientes e modificações;
- inclui cenários de grandes acidentes e interfaces relevantes;
- é revisada quando surgem novas informações operacionais.

### 9.2 Análise e aceitação de risco
- utiliza técnica compatível com a magnitude do risco;
- identifica claramente causas, consequências e barreiras;
- aprofunda cenários críticos com métodos mais detalhados, quando necessário;
- mantém rastreabilidade das recomendações e da base de decisão sobre aceitabilidade.

### 9.3 Gerenciamento de mudanças
- possui procedimento formal escrito;
- abrange mudanças permanentes e temporárias, físicas, tecnológicas e organizacionais;
- exige avaliação prévia de risco antes da implementação;
- atualiza documentos, desenhos e procedimentos;
- assegura comunicação, treinamento e autorização adequados;
- verifica impactos em integridade, manutenção, emergência e interfaces externas.

### 9.4 Aprendizado e revalidação
- incorpora achados de auditoria, incidentes e operação real;
- evita dependência excessiva de suporte externo para decisões críticas de segurança;
- revalida estudos e premissas quando há troca de operador, alterações de equipe ou novos cenários de processo.

*Fontes da seção: `regis-161cd3328a094e3a98a6fa18:pNone:2319.0-2527.0`, `regis-962e222ee3c37dec82110fd6:pNone:1327.0-1567.0`, `anp-dabfb60617e4f0ede433578e:p69-72:23.0-19.0`, `anp-2621377f5c5478141437d2bf:p28-30:17.0-22.0`, `petroles-004c2afadba7ea17c7dd7908:pNone:3234240.0-3234268.0`*

## 10. Síntese final

Para esta faceta do SGSO, a mensagem técnica central é:

- **identificação de perigos** é o ponto de partida, mas não o ponto final;
- **análise de riscos** deve ser proporcional à complexidade e à severidade potencial dos cenários;
- **barreiras** precisam ser explicitadas, mantidas e verificadas em serviço;
- **mudanças** físicas, processuais, temporárias, organizacionais ou contratuais podem criar riscos equivalentes aos de uma modificação de engenharia;
- em FPSOs, o controle eficaz depende de integração entre estudos de segurança, documentação, treinamento, integridade, emergência e governança técnica local.

Quando essa integração falha, surgem lacunas típicas: cenários não previstos nos estudos, procedimentos desatualizados, perda de rastreabilidade, treinamentos insuficientes, barreiras indisponíveis e decisões operacionais sem suporte técnico adequado.