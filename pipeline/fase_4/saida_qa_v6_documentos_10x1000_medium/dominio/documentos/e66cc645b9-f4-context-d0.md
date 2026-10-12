# Barreiras e proteção F&G em estudos de segurança de FPSOs

## 1. Finalidade técnica desta faceta
Este documento sintetiza, de forma não certificadora, aspectos relevantes para **definição, avaliação de desempenho e gestão de elementos críticos de segurança, barreiras e requisitos de proteção contra incêndio e explosão** em FPSOs, com ênfase em:

- **PPCI/PFP** como barreira mitigadora passiva;
- **sistemas de detecção de fogo e gás (F&G)** e sua justificativa baseada em risco;
- **implementação das recomendações de estudos de segurança**;
- **contingência, inspeção, teste, manutenção e gestão de degradação**;
- **interfaces com gestão de mudanças, resposta a emergências e revalidação dos estudos**.

Os trechos disponíveis não trazem critérios numéricos completos de projeto, cobertura de detectores, tempos de resposta, espessuras ou curvas de resistência ao fogo; assim, o foco aqui é conceitual e de gestão técnico-operacional.  

**Fontes:** [`anp-35714b541d23cdf8fe609d5b:p1-3:0.0-21.0`, `anp-27516937bf2e1eed76ed6255:p1-3:0.0-16.0`, `anp-21b016bb482410ebc1a9261e:p6-7:125.0-156.0`, `anp-21b016bb482410ebc1a9261e:p15-16:127.0-120.0`]

## 2. Conceitos centrais: barreiras, elementos críticos e Bow-Tie

### 2.1 Barreiras preventivas e mitigadoras
Na lógica de estudos de segurança, um cenário acidental pode ser visto como uma cadeia composta por:

- **ameaças** ou causas iniciadoras;
- **evento topo** (por exemplo, perda de contenção);
- **consequências** (incêndio, explosão, exposição tóxica, danos estruturais, necessidade de evacuação).

O uso de **Bow-Tie** ajuda a explicitar essa lógica, separando:

- no lado esquerdo, as **barreiras preventivas**, que reduzem a probabilidade de o evento topo ocorrer;
- no lado direito, as **barreiras mitigadoras**, que limitam a escalada e as consequências após a liberação.

Em uma fonte setorial secundária, aplicada a instalações marítimas de produção, aparecem como exemplos de grupos de barreiras: contenção primária, controle básico de processo, alarmes críticos com intervenção humana, intertravamentos/sistemas de alívio, sistemas de proteção pós-liberação, resposta à emergência da planta, resposta à emergência da instalação e evacuação/resgate/abandono. Esse arranjo é útil como referência conceitual, mas não deve ser tratado como taxonomia universal obrigatória para todo FPSO.  

**Fontes:** [`petroles-004c2afadba7ea17c7dd7908:pNone:466574.0-466603.0`, `petroles-4ee4bce16acf674505c8912d:pNone:2091004.0-2091038.0`]

### 2.2 Independência de barreiras
Uma boa prática destacada em fonte secundária é o uso de **múltiplas barreiras independentes**, de modo que uma falha comum não comprometa várias salvaguardas simultaneamente. Na prática, isso significa que:

- a mera existência de várias barreiras não basta;
- é necessário avaliar **dependências funcionais, energéticas, lógicas e operacionais**;
- a remoção ou indisponibilidade de uma barreira não deve ser aceita sem demonstração de que as demais são **adequadas e suficientes**.

Essa lógica é particularmente importante em discussões sobre substituição de **PPCI** por **dilúvio**, ou de detecção fixa por procedimentos manuais/portáteis: a função de segurança pode até parecer semelhante, mas o **modo de atuação**, o **tempo de resposta**, a **dependência de intervenção humana** e a **susceptibilidade a falhas comuns** podem ser muito diferentes.  

**Fontes:** [`petroles-4ee4bce16acf674505c8912d:pNone:2091004.0-2091038.0`, `anp-35714b541d23cdf8fe609d5b:p1-3:0.0-21.0`]

### 2.3 Elementos críticos de segurança e padrão de desempenho
Em fonte setorial secundária, elementos críticos de segurança operacional são descritos como equipamentos ou elementos estruturais cuja falha pode causar ou contribuir significativamente para um quase acidente ou acidente operacional. Nos trechos da ANP, essa lógica aparece de modo prático quando a **PPCI** é tratada como elemento crítico e quando falhas em sistemas como ancoragem, combate a incêndio, detecção de chama ou gerador de emergência são tratadas como desvios graves.

Também aparece, em prática corporativa citada em fonte secundária, a associação entre cada elemento crítico e um **Performance Standard (PS)**, entendido como o resultado esperado de desempenho. Para fins desta faceta, esse conceito é útil para organizar a avaliação de barreiras em termos de:

- **funcionalidade**: a barreira cumpre a função pretendida?
- **disponibilidade**: está presente e apta para atuar quando demandada?
- **integridade**: mantém as características de projeto?
- **confiabilidade**: sua probabilidade de falha é aceitável para o papel no cenário?
- **sobrevivência ao acidente**: continua capaz de atuar no ambiente de incêndio/explosão para o qual foi requerida?

Os trechos não trazem um formato padronizado de PS, mas apontam claramente para a necessidade de que o desempenho esperado seja **definido, monitorado e restaurado** quando degradado.  

**Fontes:** [`petroles-4ee4bce16acf674505c8912d:pNone:2091004.0-2091038.0`, `anp-27516937bf2e1eed76ed6255:p1-3:0.0-16.0`, `anp-2d117d40b4b79e409c88509a:p46-48:11.0-18.0`]

## 3. PPCI/PFP como barreira mitigadora crítica

### 3.1 Definição e função
A **proteção passiva contra incêndio (PPCI/PFP)** é definida, com base na API RP 2218 citada pela ANP, como barreira, revestimento ou outra salvaguarda que oferece proteção contra aquecimento por fogo **sem necessidade de intervenção adicional**. Seu objetivo é melhorar a capacidade de manter a **integridade estrutural** de equipamentos e de suas estruturas de suporte durante um cenário de incêndio.

A diferença essencial para a proteção ativa é que a proteção ativa depende de detecção/acionamento/intervenção, enquanto a PPCI atua desde o início da exposição térmica. A ANP destaca que seu valor é particularmente relevante nos **estágios iniciais do incêndio**, quando a prioridade operacional está em:

- parar a unidade;
- isolar fluxos de inflamáveis;
- acionar sistemas fixos de combate a incêndio.

Sem PPCI adequada, suportes de tubulações, equipamentos e estruturas podem perder resistência, colapsar e **escalar o cenário acidental**, gerando novas perdas de contenção e ampliando danos humanos, ambientais e patrimoniais.  

**Fontes:** [`anp-35714b541d23cdf8fe609d5b:p1-3:0.0-21.0`, `anp-27516937bf2e1eed76ed6255:p1-3:0.0-16.0`]

### 3.2 PPCI não é requisito genérico cego; depende do estudo da unidade
A ISO 13702:2015, conforme resumida pela ANP, fornece diretrizes e aplicações típicas de PPCI em áreas críticas de instalações offshore, mas ressalta a necessidade de **avaliação específica para cada instalação**, considerando:

- os **estudos de incêndio e explosão**;
- os **estudos de consequência**;
- a **estratégia de resposta à emergência** adotada.

Portanto, a PPCI não deve ser instalada nem retirada apenas por repetição de arranjos de outras unidades. A decisão precisa refletir os cenários relevantes da instalação em questão.  

**Fontes:** [`anp-35714b541d23cdf8fe609d5b:p1-3:0.0-21.0`, `anp-27516937bf2e1eed76ed6255:p1-3:0.0-16.0`]

### 3.3 Consequências da ausência, degradação ou instalação fora de especificação
Os trechos da ANP associam a ausência, degradação ou não conformidade da PPCI a:

- maior probabilidade de **escalonamento do incêndio**;
- falha de elementos críticos por aquecimento;
- redução do **tempo disponível para evacuação segura**;
- piora das condições para **controle da emergência**;
- aumento do potencial de impacto a pessoas, meio ambiente e ativos.

Em termos de segurança de processo, a degradação da PPCI transforma um cenário inicialmente controlável em um evento com maior probabilidade de colapso estrutural, ruptura secundária e propagação térmica.  

**Fontes:** [`anp-35714b541d23cdf8fe609d5b:p1-3:0.0-21.0`, `anp-27516937bf2e1eed76ed6255:p1-3:0.0-16.0`]

## 4. Onde os estudos e auditorias têm mostrado criticidade para PPCI e F&G
Os trechos não apresentam uma lista normativa exaustiva de locais obrigatórios, mas evidenciam regiões e itens frequentemente sensíveis em FPSOs e instalações offshore de produção. Exemplos citados pela ANP incluem:

- conexões de **risers** de produção e exportação;
- **riser balcony / riser porch**;
- tubulações de poços e trechos entre flanges;
- flanges a montante de **SDVs**;
- válvulas **ESD** e de blowdown/despressurização quando recomendadas por estudo quantitativo;
- estruturas inferiores de torres e suportes;
- **bandejamento de cabos**;
- áreas de lançadores/recebedores de pig;
- **slug catcher**;
- exportação de gás;
- colunas de pipe rack e colunas próximas a bombas de transferência de óleo;
- reparos compósitos em tubulações e equipamentos de fluido perigoso e da rede de combate a incêndio.

A recorrência dessas áreas nos desvios inspecionados indica que a definição de barreiras deve dialogar com os cenários de perda de contenção, ignição, propagação de fogo/explosão e manutenção da integridade estrutural.  

**Fontes:** [`anp-35714b541d23cdf8fe609d5b:p1-3:0.0-21.0`, `anp-27516937bf2e1eed76ed6255:p1-3:0.0-16.0`, `anp-21b016bb482410ebc1a9261e:p15-16:127.0-120.0`]

## 5. Substituição, equivalência e demonstração técnica
Um ponto crítico recorrente nas auditorias da ANP é a adoção de soluções alternativas **sem demonstração técnica suficiente**. Entre os exemplos citados:

- substituir PPCI classe **J-60** no piso do deck ao longo do riser porch por encapsulamento de flanges, sem avaliar tecnicamente o grau de proteção da solução alternativa nos cenários identificados;
- substituir **PPCI** por **dilúvio** sem avaliação técnica do nível de proteção efetivamente assegurado;
- deixar de instalar PPCI recomendada por estudo quantitativo em partes críticas, assumindo que outras medidas seriam suficientes, **sem verificação quantitativa**.

A implicação prática é clara: **barreiras com princípios de funcionamento diferentes não são automaticamente equivalentes**. Uma medida ativa pode reduzir consequência, mas não necessariamente substitui uma medida passiva que protege a integridade estrutural desde o início do evento. Da mesma forma, encapsulamento local de flanges não demonstra, por si só, desempenho equivalente ao de uma proteção projetada para cenários de fogo e explosão da área.

Quando houver proposta de substituição, dispensa ou implementação parcial de uma barreira recomendada por estudo, a decisão deve ser tecnicamente sustentada e documentada, preferencialmente com base no mesmo nível de rigor analítico que gerou a recomendação original.  

**Fontes:** [`anp-35714b541d23cdf8fe609d5b:p1-3:0.0-21.0`, `anp-27516937bf2e1eed76ed6255:p1-3:0.0-16.0`]

## 6. Sistemas de detecção de fogo e gás: papel, justificativa e limites

### 6.1 Detecção fixa de gás como barreira primária quando o risco a exige
A Nota Técnica da ANP afirma que, independentemente da filosofia de projeto da época de construção, **não é aceitável expor a força de trabalho a nuvens de gás inflamável, tóxico ou asfixiante** para executar atividades ou para verificar vazamentos após indicação em painel. Por isso, o operador deve prover solução de engenharia para detecção de vazamentos que não dependa dessa exposição.

A consequência prática é:

- **detectores fixos** devem ser tratados como a **primeira forma de detecção** quando o risco assim o exigir;
- **sensores portáteis** devem ser entendidos como **segunda forma de detecção**, para falha da primeira barreira, e não como substituto rotineiro da detecção fixa.

Isso desloca a discussão de “ter ou não ter detector” para “qual demonstração baseada em risco justifica a arquitetura de detecção adotada”.  

**Fontes:** [`anp-21b016bb482410ebc1a9261e:p6-7:125.0-156.0`]

### 6.2 Ausência de sistema de detecção de gás: só com demonstração baseada em risco
A mesma Nota Técnica deixa explícito que isso **não significa** exigir sistema de detecção de gases em todo tipo de instalação. Contudo, quando ele não existir, o operador deve apresentar **demonstração baseada em risco**, amparada por melhores práticas de engenharia e estudos adequados, para justificar a ausência.

O nível de robustez esperado dessa justificativa depende do contexto. A ANP sugere que instalações mais simples e isoladas possam admitir justificativas mais simples, enquanto instalações **habitadas** ou próximas a comunidades exigem demonstração mais robusta. Em um FPSO habitado, a tendência é de expectativa por uma justificativa mais forte para eventual ausência ou limitação de detecção fixa.  

**Fontes:** [`anp-21b016bb482410ebc1a9261e:p6-7:125.0-156.0`]

### 6.3 Requisitos associados ao estudo de F&G
Os trechos da ANP vinculam a avaliação de F&G a vários pontos de projeto e segurança:

- necessidade de avaliar a aderência do sistema de F&G à **Filosofia de Segurança do Operador**;
- verificação da necessidade de **estudos complementares**, como estudo de dispersão e QRA;
- verificação da necessidade de instalar **sensores/detectores de gás**;
- desvio crítico quando há **ausência de intertravamento** em caso de gás confirmado;
- desvios quando inexistem sistemas de detecção de gás ou de chama em áreas relevantes.

Isso mostra que o estudo de F&G não é apenas um exercício de posicionamento de detectores: ele se conecta a filosofia de segurança, estudos de risco, lógica de shutdown/intertravamento e estratégia de proteção da força de trabalho.  

**Fontes:** [`anp-21b016bb482410ebc1a9261e:p6-7:125.0-156.0`, `anp-2d117d40b4b79e409c88509a:p46-48:11.0-18.0`]

### 6.4 Evidências de falha de implementação
A ANP relata casos em que:

- havia **ausência de sistema de detecção de chama** no main deck;
- as recomendações de um estudo de detecção de chama para alocação de **43 detectores** não estavam implementadas, mesmo após quase 3 anos da conclusão do estudo.

Esses exemplos reforçam que a qualidade do estudo, por si só, não é suficiente. O risco persiste quando suas recomendações não são efetivamente implantadas, rastreadas e encerradas.  

**Fontes:** [`anp-2d117d40b4b79e409c88509a:p46-48:11.0-18.0`]

## 7. Critérios de desempenho e verificação de disponibilidade das barreiras

### 7.1 Obrigações de gestão destacadas pela ANP/SGSO
No alerta da ANP, aparecem como obrigações de gestão relacionadas ao SGSO:

- planejar e prover recursos necessários para implementação e operação do sistema;
- cumprir critérios de projeto, padrões da indústria e boas práticas de engenharia no projeto, construção, instalação e desativação;
- estabelecer **procedimentos de contingência** para equipamentos e sistemas críticos degradados ou fora de operação;
- estabelecer medidas temporárias para compensar ausência, falha, degradação ou desativação, incluindo, quando aplicável:
  - controles alternativos equivalentes;
  - redução/limitação de produção;
  - isolamento e parada de equipamentos, sistemas e unidades;
- implementar e documentar ações corretivas relativas a recomendações de análises de risco, e justificar modificações ou rejeições;
- estabelecer planos e procedimentos de **inspeção, teste e manutenção** voltados à integridade mecânica e assegurar cobertura integral dos equipamentos/sistemas críticos.

Esses pontos traduzem o princípio de que barreira de segurança só conta como tal se seu desempenho for efetivamente gerido ao longo do ciclo de vida.  

**Fontes:** [`anp-27516937bf2e1eed76ed6255:p1-3:0.0-16.0`]

### 7.2 O que verificar, na prática, em barreiras de PPCI, F&G e proteção de emergência
A Nota Técnica nº 06/2023 detalha verificações úteis para avaliar a efetividade real de barreiras:

- existência de **Planos de Inspeção, Teste e Manutenção Preventiva (ITMP)** cadastrados no sistema de gestão;
- suficiência das tarefas em relação a normas, padrões, manuais e função da barreira;
- conformidade das frequências planejadas com normas, padrões, manuais, boas práticas e premissas de estudos de risco, como **SIL** e **QRA**;
- execução das tarefas dentro da frequência prevista;
- mecanismos de verificação da correta execução, com aprovação técnica adequada;
- documentação da execução;
- abertura e gestão de ordens de manutenção corretiva para falhas identificadas;
- compatibilidade do prazo de tratamento com o **risco** e a **complexidade**;
- ferramentas para atacar problemas recorrentes com soluções preventivas ou definitivas;
- verificação física da **disponibilidade aparente** da barreira;
- gestão de sobressalentes considerando risco do cenário, tempo de reposição, taxa de falha e quantidade em operação.

Para barreiras de F&G e PPCI, isso implica que não basta registrar a barreira como instalada: é preciso demonstrar que ela está coberta pelo sistema de integridade, com periodicidades e critérios coerentes com sua função de segurança.  

**Fontes:** [`anp-21b016bb482410ebc1a9261e:p15-16:127.0-120.0`]

### 7.3 Efetividade relativa de barreiras automáticas e humanas
Em fonte secundária, algumas barreiras automáticas e de resposta rápida são tratadas como de maior efetividade que barreiras dependentes de ação humana, enquanto evacuação/resgate/abandono é vista como mitigação importante, porém com dependência operacional humana.

Sem transformar isso em regra universal, há uma lição útil para estudos de segurança: ao comparar alternativas, deve-se considerar que barreiras dependentes de:

- percepção humana;
- interpretação de alarmes;
- deslocamento até campo;
- execução manual sob estresse;

costumam ter vulnerabilidades diferentes das barreiras automáticas/passivas. Isso é particularmente relevante quando se tenta substituir detecção fixa por portátil, ou PPCI por respostas ativas.  

**Fontes:** [`petroles-004c2afadba7ea17c7dd7908:pNone:466574.0-466603.0`, `petroles-4ee4bce16acf674505c8912d:pNone:2091004.0-2091038.0`]

## 8. Falhas recorrentes observadas em auditorias e interdições
A recorrência dos desvios relatados pela ANP é um dado importante para avaliação profissional, porque mostra onde a gestão de barreiras costuma falhar na prática.

### 8.1 Falhas típicas em PPCI
Exemplos observados:

- planos de inspeção/manutenção incompletos;
- ausência de verificação de toda a PPCI instalada;
- PPCI degradada sem medidas contingenciais;
- remoção de PPCI sem controles alternativos equivalentes;
- instalação parcial, deixando elementos críticos sem proteção;
- recomposição com cronograma que não prioriza áreas de maior risco;
- ausência de PPCI em reparos compósitos de linhas/equipamentos de fluido perigoso;
- falta de implementação de recomendações de estudo de incêndio quanto à aplicação de PPCI.

### 8.2 Falhas típicas em F&G e sistemas associados
Exemplos observados:

- ausência de sistema de detecção de chama em área relevante;
- não implementação de recomendações de estudo de alocação de detectores;
- inexistência de intertravamento por gás confirmado;
- baixa confiabilidade do sistema de combate a incêndio;
- ausência de dilúvio em módulo específico;
- degradação de camadas de proteção independentes (IPLs) comprometendo o atendimento ao SIL requerido.

### 8.3 Consequência de gestão deficiente
Os relatos da ANP mostram que a falha não está apenas no equipamento, mas no **sistema de gestão da barreira**:

- desvios conhecidos permanecem abertos por anos;
- há degradação mapeada sem contingência adequada;
- recomendações de estudo ficam sem implementação;
- decisões não são priorizadas pelo risco;
- mudanças permanecem abertas sem solução definitiva.

Em termos profissionais, isso evidencia que disponibilidade de barreiras é um problema tanto de engenharia quanto de governança operacional.  

**Fontes:** [`anp-35714b541d23cdf8fe609d5b:p1-3:0.0-21.0`, `anp-2d117d40b4b79e409c88509a:p45-47:6.0-15.0`, `anp-2d117d40b4b79e409c88509a:p46-48:11.0-18.0`, `anp-21b016bb482410ebc1a9261e:p15-16:127.0-120.0`]

## 9. Contingência operacional quando a barreira está degradada ou indisponível
Os trechos da ANP deixam claro que a degradação ou indisponibilidade de elemento crítico não pode ser simplesmente tolerada até a próxima parada. Devem existir **procedimentos de contingência** e **medidas temporárias** compatíveis com o risco, incluindo:

- implementação de controles alternativos equivalentes, quando demonstráveis;
- redução ou limitação da produção;
- isolamento e parada de equipamentos, sistemas ou da unidade;
- recomposição da proteção para retorno às condições de projeto.

No caso de PPCI e F&G, isso implica que, na ausência de demonstração técnica robusta de equivalência, a tendência correta é **reduzir a exposição ao risco**, e não apenas manter a operação por conveniência produtiva.  

**Fontes:** [`anp-27516937bf2e1eed76ed6255:p1-3:0.0-16.0`, `anp-27516937bf2e1eed76ed6255:p2-3:20.0-37.0`, `anp-35714b541d23cdf8fe609d5b:p1-3:0.0-21.0`]

## 10. Interfaces com gestão de mudanças, estudos complementares e resposta à emergência

### 10.1 Gestão de mudanças (MoC)
A documentação da ANP mostra que mudanças de projeto, arranjo ou condição operacional podem criar riscos não tratados quando não passam por gestão formal de mudança. Exemplos relatados incluem:

- ausência de gestão de mudança para paiol de inflamáveis;
- processo de adequação de sistema crítico aberto por anos, sem solução definitiva;
- falha no gerenciamento de mudanças como desvio crítico recorrente.

Para barreiras F&G e PPCI, a MoC é especialmente importante quando houver:

- remoção, substituição ou desativação de barreiras;
- mudança de filosofia de detecção/combate;
- reforma de módulos e arranjos com impacto em ventilação, dispersão, ignição, rotas de fuga ou acessibilidade;
- reparos temporários com comportamento térmico diferente do original.

**Fontes:** [`anp-2d117d40b4b79e409c88509a:p45-47:6.0-15.0`, `petroles-4ee4bce16acf674505c8912d:pNone:2091004.0-2091038.0`]

### 10.2 Integração com estudos complementares
A Nota Técnica nº 06/2023 relaciona a definição do sistema de F&G à eventual necessidade de:

- **estudos de dispersão**;
- **QRA**;
- verificação da aderência à Filosofia de Segurança do Operador.

Além disso, os casos auditados mostram que estudos de incêndio e explosão podem ter escopo insuficiente, deixando riscos desconhecidos e não tratados. Logo, a interface entre HAZID/HAZOP, estudos de incêndio/explosão, F&G, SIL/LOPA/QRA e resposta à emergência precisa ser fechada de forma rastreável.  

**Fontes:** [`anp-21b016bb482410ebc1a9261e:p6-7:125.0-156.0`, `anp-2d117d40b4b79e409c88509a:p45-47:6.0-15.0`]

### 10.3 Interface com PRE, escape e sistemas de emergência
A Nota Técnica também conecta análise de riscos e barreiras a:

- PRE específico por instalação;
- disponibilidade do **Sistema Fixo de Combate a Incêndio (SFCI)**;
- eficácia dos simulados de emergência;
- eficácia dos sistemas de parada de emergência;
- inclusão, no PRE, de todos os cenários de grandes emergências;
- adequação e disponibilidade dos recursos de resposta;
- avaliação da necessidade de mais de uma rota de fuga e mais de um ponto de encontro com base em risco.

Isso é coerente com a ideia de que barreiras F&G/PPCI não são fim em si mesmas: elas precisam sustentar a sobrevivência da instalação e das pessoas tempo suficiente para **detecção, isolamento, combate, refúgio e evacuação**.  

**Fontes:** [`anp-21b016bb482410ebc1a9261e:p15-16:127.0-120.0`, `anp-21b016bb482410ebc1a9261e:p6-7:125.0-156.0`]

## 11. Síntese prática para avaliação profissional
Com base nos trechos disponíveis, uma avaliação tecnicamente consistente de **barreiras e proteção F&G** em FPSOs deve verificar, no mínimo, se:

1. **As barreiras foram derivadas de estudos adequados e específicos da unidade**, e não apenas copiadas de referenciais genéricos.
2. **PPCI/PFP** foi definida para elementos/áreas críticos conforme os cenários de incêndio e explosão relevantes.
3. A ausência, retirada, degradação ou substituição de PPCI foi tratada com **demonstração técnica** e, quando necessário, **verificação quantitativa**.
4. O sistema de **detecção fixa de gases** é adotado como barreira primária quando o risco assim exige, sem expor pessoas a atmosferas perigosas.
5. A eventual ausência de detecção fixa possui **justificativa robusta baseada em risco**.
6. O estudo de F&G está integrado à **filosofia de segurança**, aos estudos de dispersão/QRA e à lógica de intertravamento.
7. Há **implementação, rastreamento e encerramento** das recomendações dos estudos de segurança.
8. Os elementos críticos possuem **critérios de desempenho verificáveis** e cobertura integral por inspeção, teste e manutenção.
9. A priorização de recomposição e correção considera **nível de risco**, e não conveniência operacional.
10. Existem **contingências formais** para degradação ou indisponibilidade de barreiras, com redução da exposição ao risco até restabelecimento das condições de projeto.
11. Mudanças de projeto/operação com impacto em fogo, explosão, detecção, combate, escape ou sobrevivência passam por **gestão de mudanças**.
12. Os resultados das análises são efetivamente usados em **PRE, simulados, rotas de fuga, recursos de emergência e tomada de decisão operacional**.

**Fontes:** todos os trechos usados neste documento.