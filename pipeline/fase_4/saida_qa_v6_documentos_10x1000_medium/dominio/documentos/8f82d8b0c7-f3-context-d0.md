# Integridade de lógica e dados em sistemas digitais de FPSO

## 1. Enquadramento técnico da faceta
A integridade de lógica e de dados, no contexto de sistemas digitais de FPSO, pode ser analisada por duas perspectivas complementares:

1. **Integridade da lógica de controle, intertravamento e segurança**: preservação da especificação, implementação, validação e operação correta das lógicas executadas em CLPs, PES, DCS e subsistemas dedicados.
2. **Integridade, autenticidade operacional e disponibilidade dos dados**: confiabilidade dos valores, estados, alarmes, eventos, históricos e parâmetros usados para operar, supervisionar e manter a planta.

Com base nos trechos fornecidos, esta faceta é tratada principalmente sob o ângulo de **automação industrial, SIS, supervisão, gestão de alarmes, especificação de lógica e governança operacional de alterações**. Os materiais não trazem, de forma explícita, controles típicos de cibersegurança de rede como criptografia, IDS/IPS, DMZ, gestão de certificados ou arquitetura IT/OT detalhada; portanto, o documento foca os mecanismos tecnicamente sustentados pelas fontes para evitar, detectar e limitar alterações indevidas ou mal controladas em lógica e dados.  
**Fontes:** `petroles-004c2afadba7ea17c7dd7908:pNone:2452720.0-2452749.0`, `regis-2d3da060a3a288efef9b844c:pNone:216.0-494.0`, `regis-301d1c700775a964110d0bb7:pNone:2859.0-3135.0`

## 2. Criticidade operacional da lógica e dos dados
A ANP é citada no material como definindo sistemas críticos de segurança operacional como sistemas de controle de engenharia projetados para manter a instalação dentro dos limites operacionais de segurança, parar total ou parcialmente a instalação ou processo em caso de falha de segurança operacional, ou reduzir a exposição humana às consequências de falhas. Na mesma linha, elementos críticos de segurança operacional são equipamentos ou elementos estruturais cuja falha pode causar ou contribuir significativamente para um quase acidente ou acidente operacional. Esses equipamentos/instrumentos são identificados por TAGs restritos e registrados em sistemas de gerenciamento de manutenção e inspeção.

Isso é relevante para a integridade de lógica e dados porque, nesses sistemas, alterações indevidas podem afetar diretamente:

- a manutenção da planta em limites seguros;
- o disparo correto de ESD/SIS;
- a atuação de barreiras preventivas e mitigadoras;
- a interpretação do estado real dos ativos e salvaguardas;
- a continuidade da produção e a resposta a emergências.

Na abordagem Bow Tie citada, o **controle básico do processo**, os **alarmes críticos com intervenção humana**, o **intertravamento de segurança** e a **proteção física** aparecem como camadas preventivas distintas. Portanto, a perda de integridade de lógica ou de dados em qualquer dessas camadas pode reduzir a efetividade global de proteção.  
**Fontes:** `regis-301d1c700775a964110d0bb7:pNone:2859.0-3135.0`, `petroles-004c2afadba7ea17c7dd7908:pNone:2475592.0-2475621.0`

## 3. Onde a lógica deve residir e por que isso importa para a integridade
Os trechos diferenciam claramente o papel do sistema de supervisão e controle (SSC/SCADA) do papel dos controladores:

- O SSC pode apresentar variáveis analógicas em tempo real, tendências, alarmes, estados, eventos, históricos, relatórios e permitir diversos comandos operacionais.
- Contudo, segundo o trecho citado de especificação técnica da Petrobras, **controles, intertravamentos e cálculos com restrição temporal devem ser executados diretamente no controlador/CLP**, e não no sistema supervisório, devido a limitações de velocidade, segurança e confiabilidade do DDC no supervisório.

Essa separação é central para a integridade de lógica:

- **Lógica crítica e temporizada** deve estar em ambiente de execução determinístico, mais previsível e mais adequado a funções de segurança e controle em tempo real.
- **Supervisão, visualização e comando** devem permanecer como camada de operação, não como executor primário de funções que dependem de resposta temporal rigorosa.

Em arquitetura de automação de grandes máquinas, o material também descreve o uso de subsistemas dedicados:

- subsistema de intertravamento com equipamento programável certificado SIL mínimo;
- subsistema de controle redundante para automação de partida, controle de rotação e anti-surge;
- detecção de sobrevelocidade em sistema eletrônico dedicado;
- integração por sinais hardwired, Modbus e 4-20 mA conforme a função.

Do ponto de vista da integridade, essa distribuição reduz a chance de que uma falha ou alteração em um nível inadequado comprometa funções que exigem maior robustez.  
**Fontes:** `petroles-004c2afadba7ea17c7dd7908:pNone:2452720.0-2452749.0`, `petroles-004c2afadba7ea17c7dd7908:pNone:781081.60-781145.0`

## 4. Principais pontos de alteração sensível de lógica e parâmetros
Os materiais listam várias funções operacionais do SSC que, se alteradas sem autorização ou sem controle adequado, têm potencial direto de degradar a segurança, a confiabilidade operacional ou a fidelidade dos dados:

- acionamento e desligamento de equipamentos;
- abertura/fechamento de válvulas on-off;
- modulação de válvulas de controle;
- alteração de parâmetros de operação manual/automático;
- abertura/fechamento de dispositivos elétricos;
- bypass de pontos de entrada inicializadores de ESD;
- override de pontos de saída, forçando atuadores energizados ou desenergizados;
- alteração de parametrização de controladores, como setpoint e ganhos;
- mudança de parâmetros usados em totalizadores e correções de volume;
- alteração online de dados de equipamentos.

Do ponto de vista desta faceta, esses pontos representam superfícies críticas de alteração de lógica e dados porque podem modificar:

- a resposta da malha de controle;
- o estado lógico percebido pelo operador;
- a atuação de intertravamentos;
- os critérios de alarme;
- os cálculos operacionais e históricos;
- a consistência entre estado físico e representação digital.

Em aplicações de controle avançado, o material informa que algoritmos podem atuar em tempo real sobre **setpoints** e **sintonia de controladores PID**, inclusive com interfaces para que operadores liguem/desliguem a aplicação e definam limites de operação e desempenho desejado. Isso amplia os benefícios operacionais, mas também evidencia a necessidade de governança robusta sobre quem altera limites, sintonias e condições de habilitação.  
**Fontes:** `petroles-004c2afadba7ea17c7dd7908:pNone:2452720.0-2452749.0`, `petroles-004c2afadba7ea17c7dd7908:pNone:476933.0-476971.0`

## 5. Controle de acesso e autorização operacional como primeira barreira de integridade
O material destaca explicitamente que, para garantir a segurança das instalações, existem **categorias de usuários** no acesso ao SSC e que cada categoria possui nível de acesso específico. O princípio implícito é compatível com o **menor privilégio funcional**:

- o técnico de operação deve ter acesso apenas às funções necessárias ao seu trabalho;
- supervisor, coordenador e gerente possuem níveis diferentes;
- bypass e override só devem ser realizados com autorização hierárquica superior e após análise de risco;
- alguns bypass exigem autorização do gerente do ativo ou do gerente geral.

Embora o texto trate isso sob a ótica operacional, esse mecanismo é diretamente aplicável à proteção contra alterações não autorizadas:

- restringe quem pode alterar lógica efetiva ou comportamento do processo;
- reduz a exposição de funções críticas a uso indevido;
- cria uma cadeia de responsabilização para mudanças de maior impacto;
- associa alteração a análise de risco formal, especialmente em ESD/SIS.

Para esta faceta, isso vale não só para bypass/override, mas por analogia técnica também para mudanças de setpoint, ganho, parâmetros de alarme, condições de manutenção, modos manual/automático e habilitação de aplicações avançadas.  
**Fontes:** `petroles-004c2afadba7ea17c7dd7908:pNone:2452720.0-2452749.0`

## 6. Integridade de especificação: matriz Causa e Efeito como base da lógica de segurança
Um dos riscos mais relevantes para a integridade da lógica não está apenas na operação online, mas na **fase de especificação**. O material da REGIS descreve que diferenças no preenchimento da matriz de Causa e Efeito (C&E) reduziam significativamente a confiabilidade do sistema, porque as especificações contidas nessa matriz eram usadas para:

- implementação dos programas de CLP do sistema de segurança;
- validação desses programas.

A ferramenta descrita no estudo foi concebida justamente para padronizar a edição da matriz em formato uniforme, com interface simples e geração estruturada de documentos. Do ponto de vista da integridade de lógica, isso é importante porque:

- reduz ambiguidades na tradução de requisitos para lógica programável;
- melhora a rastreabilidade entre requisito, implementação e teste;
- apoia manutenção futura sem depender de interpretação informal;
- reduz divergência entre o comportamento especificado e o comportamento executado.

Em sistemas instrumentados de segurança, uma especificação inconsistente pode resultar em lógica correta do ponto de vista do programador, mas incorreta do ponto de vista do processo. Assim, a integridade da lógica começa antes do código: começa na qualidade, padronização e verificabilidade da especificação.  
**Fontes:** `regis-2d3da060a3a288efef9b844c:pNone:216.0-494.0`

## 7. Alterações frequentes e perda de independência funcional
Um trecho sobre barreiras de proteção observa que a barreira de “controles básicos, alarmes de processo e supervisão do operador” não é, na prática, tratada como barreira de proteção independente devido às **modificações constantes que ocorrem ao longo da vida da planta sem a devida validação da integridade funcional de segurança**.

Mesmo com limitações de legibilidade no excerto, a ideia técnica é importante para esta faceta:

- mudanças acumuladas em lógica básica, alarmes ou parametrizações podem degradar a confiança na camada;
- alterações não revalidadas podem eliminar a independência esperada entre camadas de proteção;
- a simples existência de uma função digital não garante que ela continue apta como salvaguarda ao longo do tempo.

Consequentemente, mudanças em BPCS, alarmes, intertravamentos permissivos e lógicas auxiliares devem ser tratadas com disciplina de validação, e não como ajustes rotineiros sem impacto na segurança.  
**Fontes:** `petroles-004c2afadba7ea17c7dd7908:pNone:2475592.0-2475621.0`

## 8. Medidas de robustez lógica e disponibilidade em subsistemas críticos
Os trechos de automação de compressores apresentam várias medidas que, embora não sejam descritas como “cibersegurança”, fortalecem a integridade e a disponibilidade funcional da lógica:

### 8.1 Redundância e votação
Para funções de segurança de compressores centrífugos, os iniciadores devem ter redundância com esquemas de votação, tipicamente **2-de-2**, com **alarme de discrepância**; em caso de falha de um sensor, a lógica pode passar para **1-de-1**. Sensores de vibração e sobrevelocidade recebem tratamentos específicos.

Isso reduz a probabilidade de decisão incorreta por falha isolada de entrada e melhora a detectabilidade de inconsistências.

### 8.2 Equipamentos dedicados para funções críticas
A detecção de sobrevelocidade deve ser feita por sistema eletrônico dedicado. O intertravamento pode ser executado em PES com nível mínimo de integridade especificado. Essa separação reduz acoplamentos indevidos e limita a propagação de falhas entre funções.

### 8.3 Trips por sinais físicos hardwired
O texto afirma que sinais que comandem paradas de emergência devem ser **físicos (hardwired)** e que sinais digitais não são aceitos para esse fim. Para a integridade da lógica, isso reforça que a cadeia final de atuação de emergência deve minimizar dependências de comunicação lógica mais sujeita a latência, falhas de protocolo ou ambiguidades de integração.

### 8.4 Alarme antes do trip
Toda parada de emergência deve ser precedida por alarme. Isso é relevante para rastreabilidade operacional e diagnóstico, pois ajuda a distinguir degradação detectada, resposta do sistema e confirmação do mecanismo que antecedeu a atuação automática.

### 8.5 Comportamento definido para falhas de sinal
No controle anti-surge, em caso de falha de transmissor de pressão participante dos cálculos, o controle opera com valor de projeto do sinal afetado; em falha de vazão, a válvula de reciclo vai automaticamente para posição predeterminada, o controle é colocado em manual e um alarme deve ser gerado. Isso ilustra um princípio importante: **falhas de dados devem induzir comportamento previsível, alarmado e seguro**, e não operação silenciosa com dado inválido.

### 8.6 Padronização em unidades de engenharia
Todos os parâmetros utilizados no controle devem estar indicados em unidades de engenharia. Isso reduz erros de interpretação, parametrização e manutenção, preservando a integridade semântica dos dados configurados.  
**Fontes:** `petroles-004c2afadba7ea17c7dd7908:pNone:781060.0-781099.0`, `petroles-004c2afadba7ea17c7dd7908:pNone:781081.60-781145.0`

## 9. Integridade e confiabilidade dos dados operacionais
Os sistemas de supervisão descritos no material concentram um conjunto amplo de dados críticos:

- valores numéricos de variáveis analógicas em tempo real;
- gráficos de tendência;
- alarmes com mensagens, cor e som;
- reconhecimento de alarmes;
- estado operacional de equipamentos;
- registro de eventos;
- histórico de variáveis, alarmes e eventos;
- horímetros de operação, falha e manutenção;
- relatórios.

Esses dados têm papéis operacionais distintos:

- **tempo real** para tomada de decisão imediata;
- **eventos e alarmes** para diagnóstico e resposta;
- **históricos** para análise de falhas, performance e integridade;
- **horímetros e estados** para manutenção e indisponibilidade.

Logo, proteger a integridade dos dados operacionais significa preservar, no mínimo:

- a correspondência entre dado e estado real do processo;
- a consistência temporal dos eventos;
- a rastreabilidade de alarmes, mudanças de estado e comandos;
- a não adulteração de parâmetros de cálculo e referência.

O trecho sobre aquisição de dados mostra ainda que parte das informações é obtida automaticamente de sistemas como PI, APLAT e SAP, enquanto outra parte é inserida manualmente. Entre os dados automáticos citados estão:

- condição automático/manual de equipamentos;
- condição de inibição de intertravamentos e salvaguardas;
- dados de manutenção e inspeção.

Isso implica que a interpretação segura dos dados depende também de conhecer sua **origem**, **modo de aquisição** e **contexto operacional**. Por exemplo, um equipamento em manual ou um intertravamento inibido pode alterar completamente o significado de tendências e alarmes.  
**Fontes:** `petroles-004c2afadba7ea17c7dd7908:pNone:2452720.0-2452749.0`, `regis-301d1c700775a964110d0bb7:pNone:2859.0-3135.0`

## 10. Alarmes, pseudoalarmes e qualidade da informação
Um dos trechos destaca que grande quantidade de pseudoalarmes durante a operação industrial dificulta a identificação de problemas, aumenta o tempo de resposta a anormalidades e eleva riscos à segurança pessoal, instalações, meio ambiente e produção. A solução apresentada no estudo é uma filosofia de configuração do sistema de supervisão e controle voltada a reduzir pseudoalarmes e aumentar a confiabilidade da informação fornecida pelo sistema.

Isso é altamente pertinente para integridade de dados operacionais, porque um sistema pode estar “disponível”, mas ainda assim ser operacionalmente pouco confiável se:

- anuncia alarmes excessivos, desnecessários ou persistentes;
- não permite distinguir anormalidades reais de ruído operacional;
- apresenta avalanche de alarmes além da capacidade de gestão do operador.

As definições citadas no material reforçam esse ponto:

- **alarme incômodo**: anuncia excessivamente, desnecessariamente ou não retorna ao normal após a resposta correta;
- **avalanche de alarmes**: grande quantidade em curto período, inviabilizando gerenciamento pelo operador;
- **filosofia de alarmes**: documentação base para projetar, implementar e manter o sistema de alarmes;
- **racionalização de alarmes**: análise fundamentada na filosofia para concepção e documentação dos alarmes;
- **inibição** e **desabilitação**: formas de impedir anunciação, exigindo controle rigoroso.

Para esta faceta, alarmes mal configurados degradam a integridade operacional da informação, porque o sistema passa a comunicar um retrato distorcido da prioridade e do risco reais.  
**Fontes:** `petroles-004c2afadba7ea17c7dd7908:pNone:2452550.0-2452645.0`, `petroles-004c2afadba7ea17c7dd7908:pNone:2452720.0-2452749.0`

## 11. Monitoramento analítico e limiares de detecção
O trecho sobre análise estatística indica que a definição de limites de violação é crucial para equilibrar:

- **erro do Tipo I**: falso alarme, quando a falha é detectada sem realmente existir;
- **erro do Tipo II**: detecção perdida, quando a falha ocorre e não é detectada.

A fonte observa que ampliar a região considerada normal reduz falsos alarmes, mas aumenta detecções perdidas. Para reduzir simultaneamente esses erros, são citadas duas direções:

- aumentar o tamanho da amostra de dados de treinamento usada para obter limiares de detecção;
- melhorar a exatidão dos sensores instalados na planta.

Para integridade e disponibilidade dos dados operacionais, essa discussão tem duas implicações práticas:

1. **Integridade de dados não é apenas impedir adulteração**; é também manter qualidade metrológica e limiares adequados para que o sistema reconheça corretamente desvios reais.
2. **Monitoramento analítico ruim pode ser tão danoso quanto dado corrompido**, porque leva a ações indevidas ou omissões perigosas.

A etapa de diagnóstico de falhas citada no material também depende da contribuição das variáveis do processo e de padrões de falha, o que exige consistência histórica e coerência entre medições, modelos e contexto operacional.  
**Fontes:** `petroles-4ee4bce16acf674505c8912d:pNone:2066950.0-2066988.0`

## 12. Ciclo de vida, monitoramento e manutenção de aplicações de controle avançado
As aplicações de controle avançado citadas no material atuam sobre setpoints, sintonias e condições operacionais para reduzir trips, estabilizar o processo e melhorar qualidade de produtos. O texto destaca fatores críticos para sucesso e manutenção da integridade dessas aplicações:

- participação das equipes de operação desde o início do projeto;
- comissionamento e sintonia adequados;
- monitoração contínua das aplicações em uso;
- evolução com feedback dos operadores;
- alteração controlada de parâmetros de sintonia;
- treinamento de operadores, automação e engenharia;
- repetição de treinamento quando houver renovação de equipes;
- uso de plataforma de gestão de ativos para monitorar desempenho.

Esses pontos mostram que a integridade de lógica não se esgota na implantação inicial. Ela depende de um ciclo contínuo de:

- entendimento do objetivo da aplicação;
- supervisão do efeito de suas ações sobre a planta;
- disciplina de ajuste e revalidação;
- retenção de conhecimento operacional.

Sem isso, mesmo lógicas inicialmente corretas podem se tornar inadequadas, mal compreendidas ou operacionalmente arriscadas.  
**Fontes:** `petroles-004c2afadba7ea17c7dd7908:pNone:476933.0-476971.0`

## 13. Consequências típicas da perda de integridade de lógica e dados
A partir dos materiais, as consequências técnicas mais plausíveis incluem:

- acionamento indevido ou tardio de alarmes e trips;
- degradação do comportamento dinâmico da planta;
- maior variabilidade em torno dos setpoints;
- aumento de paradas não programadas;
- desgaste de atuadores por controle inadequado;
- aumento de risco em equipamentos como separadores e compressores;
- perda de confiabilidade da supervisão por pseudoalarmes;
- implementação incorreta de lógica de segurança por especificação ambígua;
- redução da efetividade ou independência das camadas de proteção;
- diagnóstico equivocado por inconsistência de dados ou limiares inadequados.

Nos exemplos de controle avançado, os textos associam diretamente a melhoria de controle a redução de trips de compressores, menor risco de paradas não programadas e operação mais aberta de poços com segurança. Por simetria técnica, alteração indevida de setpoints, ganhos, lógicas ou condições de habilitação nesses sistemas pode reverter esses ganhos e aumentar a exposição operacional.  
**Fontes:** `petroles-004c2afadba7ea17c7dd7908:pNone:476914.0-476952.0`, `petroles-004c2afadba7ea17c7dd7908:pNone:476933.0-476971.0`, `petroles-004c2afadba7ea17c7dd7908:pNone:2452550.0-2452645.0`

## 14. Síntese prática para avaliação profissional
Com base nos trechos, a proteção contra alterações indevidas em lógica e a preservação da integridade dos dados operacionais em FPSO dependem, no mínimo, de:

1. **Separar execução crítica de supervisão**: lógica temporizada e de segurança no controlador/subsistema dedicado.
2. **Restringir permissões por perfil**: acesso conforme função, com autorização escalonada para bypass, override e outras alterações de alto impacto.
3. **Padronizar especificações**: matriz C&E consistente e rastreável para implementação e validação da lógica.
4. **Definir comportamento seguro para falhas de sinal**: fallback conhecido, alarmado e operacionalmente tratável.
5. **Usar arquiteturas robustas**: redundância, votação, discrepância, sistemas dedicados e sinais hardwired para trips.
6. **Preservar qualidade dos dados e dos alarmes**: racionalização, filosofia de alarmes, histórico consistente e redução de pseudoalarmes.
7. **Controlar mudanças ao longo do ciclo de vida**: comissionamento, revalidação, monitoramento de desempenho e treinamento recorrente.
8. **Contextualizar o dado operacional**: distinguir modo automático/manual, intertravamentos inibidos e origem manual/automática das informações.

Essa síntese não substitui requisitos formais de cibersegurança, mas representa um conjunto de fundamentos de automação e integridade funcional diretamente relacionados à proteção da lógica e da informação operacional.  
**Fontes:** todos os IDs listados em `used_chunk_ids`.