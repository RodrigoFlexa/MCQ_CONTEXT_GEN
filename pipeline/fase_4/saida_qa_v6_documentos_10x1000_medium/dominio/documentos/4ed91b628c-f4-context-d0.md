# SIMOPS em FPSOs com interfaces submarinas: monitoramento contínuo e controle de mudanças

## 1. Finalidade do monitoramento durante SIMOPS

Em operações simultâneas (SIMOPS), o ponto central do monitoramento não é apenas acompanhar cada atividade isoladamente, mas verificar continuamente se **as premissas de risco, os limites operacionais, a disponibilidade das barreiras e a coordenação entre organizações** permanecem válidas enquanto várias frentes de trabalho ocorrem ao mesmo tempo.

Nos trechos fornecidos, a base regulatória aplicável ao **Sistema Submarino** exige que o operador:

- especifique as **categorias e os tipos de operações simultâneas** onde existam interfaces operacionais;
- trate com atenção especial SIMOPS que:
  - introduzam **novos perigos** não considerados especificamente na análise de riscos;
  - demandem **logística especial, medidas de apoio ou procedimentos de trabalho seguro** não cobertos por outros procedimentos;
  - possam **comprometer a disponibilidade e a funcionalidade dos Elementos Críticos de Segurança Operacional**;
- estabeleça e documente **procedimentos específicos para gerenciar SIMOPS**.

Para o foco desta faceta, isso significa que o monitoramento contínuo deve responder, durante a execução, a perguntas como:

1. As condições reais ainda estão dentro do **Envelope de Segurança**?
2. Surgiram desvios, anormalidades, interferências ou indisponibilidades de barreiras que mudam o risco combinado?
3. Houve mudança de escopo, condição operacional, pessoal, logística ou configuração que passe a exigir **gestão de mudança formal**?
4. As organizações envolvidas continuam operando com a mesma compreensão das prioridades, restrições e respostas a anormalidades?

**Fontes:** `anp-226946a12711e04f54ee4bfb:p60-64:4.0-18.0`, `anp-226946a12711e04f54ee4bfb:p55-60:22.0-3.0`

## 2. Base técnica do monitoramento contínuo

### 2.1 Limites operacionais, alarmes e tendências

Os trechos da ANP indicam que o operador deve:

- garantir operação dentro dos **limites do Envelope de Segurança** definidos em projeto;
- **registrar e investigar desvios** desses limites;
- monitorar variáveis operacionais com **limites de alarme** estabelecidos;
- **analisar tendências** dessas variáveis;
- adotar, quando não houver acompanhamento em sistema supervisório, **procedimentos de segurança e mecanismos de controle e monitoramento** capazes de identificar anormalidades.

Em termos de SIMOPS, isso significa que o monitoramento não pode ser passivo. Não basta verificar um valor instantâneo; é necessário observar a **tendência** e a **convergência de pequenos desvios** que, somados, podem invalidar a base de segurança da operação combinada. Exemplos típicos de sinais de degradação do controle em SIMOPS, à luz dos trechos, são:

- aproximação repetida aos limites do envelope;
- alarmes inibidos, falsos ou com valor forçado/manual por tempo superior ao estritamente requerido para operação ou manutenção associada;
- perda de visibilidade sobre variáveis não supervisórias;
- anormalidades não comunicadas entre áreas ou empresas envolvidas.

### 2.2 Variáveis centralizadas e não centralizadas

O **Procedimento Mútuo de Operação (PMO)** deve estabelecer:

- critérios para monitoramento das variáveis com **controle centralizado e aquisição de dados**;
- critérios e **intervalos de tempo** para monitoramento das variáveis que **não** estejam cobertas por esse controle centralizado;
- critérios de delegação de responsabilidade e comunicação;
- critérios de reinício de operação após interrupções por anormalidades ou paradas.

Aplicado a SIMOPS, isso implica que o plano de monitoramento deve deixar claro:

- o que é acompanhado continuamente pelo CCR/sala de controle;
- o que depende de verificação local, remota ou periódica por equipes de campo, embarcações ou apoio subsea;
- qual é a frequência mínima dessas verificações;
- quem consolida a informação e toma decisão quando houver conflito entre frentes de trabalho.

### 2.3 Comunicação operacional como condição de controle

A ANP também exige sistema de comunicação **adequado e confiável** entre pontos remotos e a sala de controle responsável pela operação do Sistema Submarino, com procedimentos e critérios estabelecidos. Em SIMOPS, essa exigência é particularmente relevante porque parte do risco surge justamente da **defasagem entre o que mudou no campo e o que a coordenação central acredita que ainda é verdade**.

Portanto, o monitoramento contínuo depende de:

- canais confiáveis entre campo, embarcações, subsea e controle central;
- comunicação tempestiva de **anormalidades e contingências** às demais gerências/empresas envolvidas;
- regras prévias sobre quem declara condição anormal, quem avalia impacto cruzado e quem autoriza continuidade, suspensão ou reinício.

**Fontes:** `anp-226946a12711e04f54ee4bfb:p55-60:22.0-3.0`, `anp-226946a12711e04f54ee4bfb:p60-64:4.0-18.0`

## 3. Interfaces e riscos emergentes durante a execução

A análise de riscos, segundo os trechos regulatórios, deve considerar, entre outros pontos:

- layout, causas externas, áreas adjacentes e interligação com outras instalações;
- procedimentos, situações ou equipamentos que possam aumentar a possibilidade de erros operacionais;
- mudanças ocorridas desde a última análise;
- identificação e adequação das salvaguardas existentes;
- ações necessárias para mitigação e prevenção.

Além disso, a **real condição de integridade** do sistema deve ser considerada na avaliação.

Para o monitoramento em SIMOPS, isso tem uma consequência prática importante: o risco não deve ser visto como fixo. Durante a execução, podem surgir **riscos emergentes** por combinação de fatores que, individualmente, seriam aceitáveis, mas que juntos mudam o cenário. Exemplos de lógica de avaliação compatível com os trechos fornecidos:

- uma atividade que já possuía risco conhecido passa a ter risco maior porque uma salvaguarda relevante ficou indisponível;
- uma interface antes neutra passa a ser crítica porque houve mudança operacional, organizacional ou de pessoal;
- uma atividade permanece formalmente igual, mas sua execução ocorre sob **condição de integridade degradada** do sistema afetado;
- uma alteração temporária introduzida para viabilizar a operação cria novos caminhos de falha ou dificulta resposta a emergência.

A própria revisão da análise de riscos principal deve ser reavaliada quando houver:

- modificações físicas ou operacionais;
- experiência de incidentes relevantes;
- mudanças organizacionais;
- mudanças na base de dados, modelos ou métodos de estimativa de risco;
- alta frequência ou gravidade de incidentes;
- indisponibilidade de salvaguardas contidas em análise anterior.

Isso é diretamente aplicável ao controle de mudanças durante SIMOPS: quando a mudança de condição atinge um desses gatilhos, o monitoramento operacional isolado deixa de ser suficiente e passa a ser necessária uma **reavaliação formal do risco**.

**Fontes:** `anp-226946a12711e04f54ee4bfb:p38-42:28.0-31.0`

## 4. Gestão de mudanças aplicada a SIMOPS

### 4.1 O que deve ser tratado como mudança

Os trechos da ANP determinam procedimento formal para gerenciar mudanças que possam afetar a segurança operacional. Esse processo deve considerar definições do que constitui mudança, abrangendo avaliação de alterações:

- nas **operações**;
- nos **padrões**;
- nos **procedimentos**;
- nas **instalações**;
- no **pessoal**.

Também deve prever situações em que seja necessária **reavaliação e adequação de projeto**, inclusive quando a modificação de uso contrariar premissas do projeto original ou bases de avaliações de integridade anteriores.

O material conceitual de Petrolês reforça essa lógica ao mencionar que instalações de processamento estão sujeitas a modificações contínuas para aumentar eficiência, desempenho e segurança, e que **reparos temporários, interconexões, bypasses e outros arranjos operacionais** podem introduzir novos riscos ou comprometer salvaguardas existentes. O mesmo material lista como exemplos de mudança:

- alterações relevantes em pressões, temperaturas, vazões e condições operacionais frente ao projeto original;
- modificações em sistemas de instrumentação e controle;
- bypasses e intertravamentos associados;
- operações a carga reduzida ou fora dos limites operacionais;
- tubulações, conexões ou mangueiras temporárias;
- equipamentos e conexões elétricas provisórias;
- substituição de equipamentos por outros diferentes dos originais;
- mudanças na força de trabalho, passagem de turno, substituições e uso de pessoal sem treinamento adequado.

Esses exemplos são úteis em SIMOPS porque muitas mudanças críticas surgem como “arranjos temporários” para viabilizar a coexistência de atividades. Em termos de controle, o caráter temporário **não reduz** a necessidade de avaliação; frequentemente a aumenta.

### 4.2 Conteúdo mínimo do processo de mudança

Segundo a ANP, o processo de gestão de mudanças deve incluir, entre outros elementos disponíveis no trecho:

- responsabilidades para aprovação compatíveis com o potencial de risco da mudança;
- descrição da mudança proposta e sua justificativa;
- classificação quanto a ser **temporária ou permanente**;
- previsão de duração para mudanças temporárias;
- previsão de **revisões e nova autorização** se a duração precisar ser ampliada, com justificativa;
- avaliação dos perigos e do **impacto global nas atividades** antes da implementação.

O relatório da ANP de 2022 reforça, como lição aprendida, que mudanças devem ser geridas por **processo formal**, com:

- avaliação dos perigos e do impacto global nas atividades;
- atualização de procedimentos impactados;
- treinamento e comunicação ao pessoal afetado;
- revisão e nova autorização para mudanças temporárias cuja duração precise ser estendida.

### 4.3 Relação entre mudança e disciplina operacional

Os procedimentos operacionais, de acordo com a ANP, devem ser:

- claros e concisos;
- revisados periodicamente quando necessário para refletir condições reais ou mudanças realizadas;
- elaborados com consideração adequada de **fatores humanos**;
- avaliados quanto à sua adequabilidade e ao risco de desvio ou de não cumprimento de etapas;
- acompanhados de treinamento adequado nas revisões.

Em SIMOPS, isso é crucial: mudança sem atualização procedural e sem comunicação estruturada tende a gerar **desalinhamento entre equipes, turnos, contratadas e controle central**, aumentando probabilidade de erro humano exatamente nas interfaces mais sensíveis.

**Fontes:** `anp-226946a12711e04f54ee4bfb:p38-42:28.0-31.0`, `petroles-004c2afadba7ea17c7dd7908:pNone:3234240.0-3234268.0`, `anp-b2cfa8a9492ef598716e9685:p61-63:30.0-27.0`, `anp-226946a12711e04f54ee4bfb:p60-64:4.0-18.0`

## 5. Barreiras, elementos críticos e mudanças de condição

Uma das razões para classificar e controlar SIMOPS é evitar que a combinação de atividades **comprometa a disponibilidade e a funcionalidade dos Elementos Críticos de Segurança Operacional**.

Os relatórios anuais da ANP mostram achados recorrentes relevantes para esse tema, entre eles:

- falha de contingenciamento adequado quando há degradação de elemento crítico;
- ausência de testes de desempenho de barreiras;
- subdimensionamento de sistemas críticos;
- falhas relacionadas a SDVs, sistemas de dilúvio, drenagem e detecção;
- ausência de gestão de mudanças quando alterações de projeto são implementadas;
- não implementação de recomendações de análises de risco associadas a mudanças;
- ausência de procedimento de gerenciamento de alarmes;
- falha no monitoramento e análise de tendências de variáveis operacionais;
- falha na definição do envelope de segurança.

As lições aprendidas da ANP de 2022 acrescentam que o operador deve:

- conhecer todos os elementos críticos contingenciados;
- realizar análise crítica desses contingenciamentos;
- restaurar a condição original de projeto do elemento crítico sempre que possível;
- quando essa restauração não for imediata, garantir que as medidas de controle de risco permaneçam adequadas até o restabelecimento completo.

Para SIMOPS, a consequência é direta: **mudança de condição de barreira é também mudança de base de autorização da operação**. Se uma atividade foi aprovada assumindo determinada barreira disponível, a indisponibilidade, degradação, bypass ou contingenciamento dessa barreira exige reavaliação do arranjo operacional e pode demandar suspensão, replanejamento ou nova autorização.

**Fontes:** `anp-226946a12711e04f54ee4bfb:p60-64:4.0-18.0`, `anp-53df4afc22d11e83207417ba:p29-32:48.0-33.0`, `anp-53df4afc22d11e83207417ba:p31-33:23.0-37.0`, `anp-b2cfa8a9492ef598716e9685:p61-63:30.0-27.0`

## 6. Monitoramento de anormalidades, interrupção e reinício

Os trechos fornecidos não trazem uma matriz completa de cancelamento de SIMOPS para FPSO, mas permitem extrair uma lógica mínima de decisão.

### 6.1 Situações que tipicamente exigem reavaliação imediata

À luz dos requisitos e achados apresentados, devem ser tratadas como condições de reavaliação imediata, e potencialmente de interrupção controlada da atividade afetada, situações como:

- desvio dos limites do **Envelope de Segurança**;
- surgimento de novos perigos não contemplados na análise de risco usada para autorização da SIMOPS;
- perda, degradação, contingenciamento ou indisisponibilidade de salvaguarda/barreira relevante;
- alteração operacional, física, organizacional ou de pessoal com impacto no risco;
- falha ou insuficiência dos meios de comunicação entre ponto remoto e sala de controle;
- impossibilidade de monitorar adequadamente variáveis críticas, inclusive as não cobertas por supervisório;
- necessidade de estender uma modificação temporária sem revisão e nova autorização.

### 6.2 Reinício após anormalidade ou parada

O PMO deve estabelecer critérios para o **reinício da operação** após interrupções motivadas por anormalidades operacionais ou paradas. Em complemento, para partes do sistema que tenham permanecido fora de operação, a ANP exige procedimento de retorno operacional com revisão de histórico operacional, inspeção, manutenção, monitoramento/corrosão e avaliação de integridade.

Assim, o reinício em contexto de SIMOPS deve estar condicionado, no mínimo, a que:

- a causa da interrupção seja compreendida e comunicada;
- as condições relevantes de integridade e monitoramento tenham sido reavaliadas;
- os critérios de monitoramento e comunicação tenham sido restabelecidos;
- as licenças e autorizações necessárias estejam emitidas;
- a base documental de risco, procedimento ou mudança tenha sido atualizada quando aplicável.

### 6.3 Condição segura de equipamentos ou trechos temporariamente fora de operação

A ANP determina que dutos, componentes ou complementos fora de operação, em manutenção ou temporariamente desativados sejam mantidos em **condições seguras**, com planos de inspeção, manutenção, monitoramento e controle de corrosão apropriados durante todo o período. Em SIMOPS com interfaces submarinas, isso é importante porque a simples retirada temporária de serviço de um trecho, equipamento ou função não elimina o risco; ela pode apenas **transferi-lo** para outra barreira, outro modo de falha ou outra interface operacional.

**Fontes:** `anp-226946a12711e04f54ee4bfb:p55-60:22.0-3.0`, `anp-226946a12711e04f54ee4bfb:p60-64:4.0-18.0`, `anp-226946a12711e04f54ee4bfb:p61-66:27.0-8.0`

## 7. Registros, rastreabilidade e aprendizado operacional

O controle de mudanças e o monitoramento em SIMOPS só são auditáveis e reproduzíveis se houver boa gestão de registros.

Nos trechos da ANP, o operador deve:

- levantar, integrar, organizar e revisar dados operacionais, de integridade, indicadores de desempenho, alterações identificadas pelo sistema de gestão de mudanças e análises de riscos;
- manter sistemática de **gestão de registros, controle e rastreabilidade** das informações de gerenciamento da integridade e de monitoramento/controle operacional;
- documentar as principais informações e decisões tomadas na identificação e análise de riscos, com base explícita para essas decisões;
- implementar recomendações de análise de riscos e acompanhar seu progresso;
- justificar e documentar modificações ou não implementação de recomendações por meio de parecer técnico compatível com os riscos envolvidos;
- manter análises de risco disponíveis à força de trabalho pertinente;
- divulgar riscos identificados e recomendações implementadas.

Os relatórios anuais da ANP mostram, como falhas recorrentes observadas em auditorias, precisamente a **ausência de registro e implementação de ações**, atrasos na implementação de recomendações, falhas em procedimentos de alarmes e falhas em monitoramento de tendências. Para fins de SIMOPS, isso indica que o registro não é burocracia acessória; ele é parte do próprio controle do risco combinado.

Também há exigência de definição e monitoramento de **indicadores de desempenho** associados ao cumprimento de planos, monitoramento e ações corretivas/preventivas. Embora os trechos não apresentem uma lista fechada de indicadores de SIMOPS, a lógica regulatória sugere que indicadores úteis devam evidenciar se o sistema está detectando desvios, reavaliando mudanças e fechando ações dentro do prazo compatível com o risco.

**Fontes:** `anp-226946a12711e04f54ee4bfb:p60-64:4.0-18.0`, `anp-226946a12711e04f54ee4bfb:p61-66:27.0-8.0`, `anp-226946a12711e04f54ee4bfb:p38-42:28.0-31.0`, `anp-53df4afc22d11e83207417ba:p29-32:48.0-33.0`

## 8. Síntese prática para avaliação profissional

Com base exclusivamente nos materiais fornecidos, uma avaliação técnica de monitoramento e mudanças em SIMOPS deve verificar se o arranjo operacional consegue demonstrar, de forma consistente, os seguintes pontos:

1. **Classificação adequada da SIMOPS** e reconhecimento das interfaces que introduzem novos perigos ou afetam elementos críticos.
2. **Monitoramento contínuo** das variáveis relevantes, com limites, tendências e tratamento claro das variáveis não supervisórias.
3. **Comunicação confiável** entre ponto remoto e sala de controle, além de comunicação estruturada entre empresas/gerências envolvidas.
4. **Critérios formais de mudança**, incluindo definição do que constitui mudança, avaliação de perigos, impacto global, temporalidade, duração, revisão e nova autorização.
5. **Avaliação da disponibilidade das salvaguardas**, com especial atenção a contingenciamentos, bypasses, degradações e alarmes inibidos/forçados.
6. **Critérios de interrupção e reinício** após anormalidades, compatíveis com a condição de integridade e com a necessidade de nova autorização.
7. **Rastreabilidade documental**, implementação de recomendações e aprendizado a partir de desvios, auditorias e incidentes.

Não há fórmulas quantitativas nos trechos disponibilizados para esta faceta; o material é predominantemente de natureza procedimental, organizacional e de governança do risco.

**Fontes:** `anp-226946a12711e04f54ee4bfb:p55-60:22.0-3.0`, `anp-226946a12711e04f54ee4bfb:p60-64:4.0-18.0`, `anp-226946a12711e04f54ee4bfb:p61-66:27.0-8.0`, `anp-226946a12711e04f54ee4bfb:p38-42:28.0-31.0`, `anp-53df4afc22d11e83207417ba:p29-32:48.0-33.0`, `anp-53df4afc22d11e83207417ba:p31-33:23.0-37.0`, `anp-b2cfa8a9492ef598716e9685:p61-63:30.0-27.0`, `petroles-004c2afadba7ea17c7dd7908:pNone:3234240.0-3234268.0`