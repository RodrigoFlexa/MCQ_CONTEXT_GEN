# Contingências e integridade operacional no pull-in de risers

Este documento consolida critérios técnicos e de gestão aplicáveis à **resposta a falhas, desvios operacionais e preservação da integridade** em operações de pull-in de risers em FPSOs, com ênfase em risers flexíveis e no contexto regulatório/gerencial do sistema submarino. O material abaixo **não substitui** projeto, análise estrutural, procedimentos aprovados, estudos de risco específicos da instalação ou critérios formais de aceitação do fabricante/operador.

## 1. Enquadramento da integridade no pull-in

Para fins de integridade, o pull-in deve ser tratado como uma **condição transitória do ciclo de vida do sistema submarino**, sujeita a análise de riscos, controle operacional, rastreabilidade de dados e avaliação de integridade. No contexto do SGSS, o operador deve manter um **Programa de Gerenciamento da Integridade (PGI)** cíclico, integrado e contínuo, cobrindo levantamento e integração de dados, análise de riscos, avaliação de integridade, ações corretivas/preventivas e avaliação do próprio programa. Também deve haver gestão de registros e rastreabilidade ao longo de toda a vida útil, inclusive com histórico individualizado de equipamentos, tramos/trechos, ciclos de lançamento e recolhimento e avaliações de integridade, especialmente relevante quando há suspensão, retomada ou reutilização de componentes.  

Em uma operação de pull-in, isso implica que a decisão de iniciar, continuar, suspender ou abortar a atividade não deve ser baseada apenas na execução imediata da manobra, mas na verificação de que:

- a operação está **dentro do envelope de segurança** definido em projeto;
- os **modos de falha aplicáveis** foram identificados e tratados na análise de riscos;
- os **elementos críticos** e barreiras necessárias estão disponíveis ou possuem contingências adequadas;
- a documentação operacional, inspeções e comunicação estão atualizadas para a configuração real da instalação.

_Fontes: `anp-226946a12711e04f54ee4bfb:p61-66:27.0-8.0`, `anp-2e1d17d32fb37a1c34f1eeef:p2-5:22.0-3.0`_

## 2. Modos de falha e ameaças à integridade relevantes ao pull-in

### 2.1 Zonas críticas e mecanismos estruturais

As fontes destacam que, para risers flexíveis, as regiões mais severamente solicitadas tendem a ser:

- **terminação superior / conexão ao FPSO**;
- **pontos de curvatura acentuada**;
- **pontos de contato/interferência**.

Essas regiões são particularmente sensíveis porque concentram esforços dinâmicos e estáticos, e podem se tornar limitantes para a vida em fadiga. O material indica que a **terminação superior** é uma área de maior carregamento e que o uso de **bend stiffener** é uma medida de mitigação típica para essa região. Durante o pull-in, qualquer desvio geométrico, contato indevido, posicionamento incorreto da unidade ou dano em acessórios nessa área deve ser tratado como potencial ameaça de integridade, mesmo que a conexão final ainda não tenha sido concluída.  

Entre os mecanismos de dano destacados nas fontes:

- **fadiga pura** em armaduras metálicas, especialmente sob altos níveis de tração;
- **fadiga de baixo ciclo** associada aos movimentos da plataforma;
- **fadiga de alta frequência** associada a vibrações induzidas por vórtice (VIV), importante em risers em catenária sob correntes marítimas significativas;
- **instabilidade torcional** e torção decorrente de ruptura de arames da armadura de tração, com redistribuição do campo de tensões;
- **fretting** entre arames/camadas internas;
- **corrosão associada à fadiga**, especialmente quando há ingresso de água do mar, CO2, H2S ou oxigênio em regiões anulares ou internas.

Para águas profundas e condições brasileiras citadas no material, a **falha da armadura de tração na conexão** é apontada como modo de falha prioritário a investigar em risers flexíveis sob alta tração. Isso é diretamente relevante ao pull-in, pois essa etapa pode impor carregamentos transitórios importantes na vizinhança da conexão e do sistema de hang-off.  

_Fontes: `petroles-004c2afadba7ea17c7dd7908:pNone:2990169.0-2990204.0`, `petroles-004c2afadba7ea17c7dd7908:pNone:2990188.0-2990221.0`_

### 2.2 Degradações observáveis que podem indicar falha ou desvio durante/apos o pull-in

As fontes sobre inspeção e monitoramento de risers flexíveis indicam que inspeções visuais podem detectar, entre outros:

- danos, abrasão, ruptura, vazamento e deformações na capa externa;
- falhas em válvula de alívio da seção de topo;
- falhas na armadura de pressão;
- configuração inadequada de catenária;
- interferência entre risers ou entre riser e embarcação;
- instabilidade torcional;
- ruptura de arames da armadura de tração;
- erro de posicionamento da UEP/FPSO;
- danos na seção de topo;
- danos em equipamento auxiliar;
- falhas na fixação, envelhecimento, degradação ou ruptura de bend stiffener;
- ingresso de água do mar no espaço anular.

Em termos de resposta operacional, esses achados são relevantes porque um pull-in aparentemente concluído pode ainda deixar o riser em **condição geométrica inadequada**, com dano localizado ou com comprometimento de acessórios que serão críticos na vida operacional subsequente. Logo, desvios identificados na operação não devem ser tratados apenas como dificuldade momentânea de instalação, mas como potenciais **precursores de dano cumulativo**, inclusive em fadiga.  

_Fontes: `petroles-004c2afadba7ea17c7dd7908:pNone:2990169.0-2990204.0`, `petroles-004c2afadba7ea17c7dd7908:pNone:2990188.0-2990221.0`_

### 2.3 Modos de falha associados ao anular, ventilação e corrosão

Um alerta de segurança da ANP referente a ruptura de riser destaca lições aprendidas particularmente úteis ao raciocínio de integridade no pull-in/comissionamento:

- a **entrada de oxigênio no anular do riser** deve ser considerada como **modo de falha** no projeto e na análise de riscos;
- deve-se assegurar a **adequação do sistema de ventilação/vent** dos risers conforme o projeto;
- o relatório de comissionamento deve registrar **anormalidades encontradas**;
- o programa de integridade deve contemplar métodos de **análise e avaliação de corrosão interna**;
- o operador deve possuir procedimento para **inspeção do sistema de vent**, quando aplicável.

Para operações de pull-in, isso é importante porque montagem, conexão, passagem de serviço entre projeto/instalação/operação e fechamento de pendências podem introduzir vulnerabilidades que não aparecem apenas como problema mecânico imediato de tração, mas como risco latente de corrosão/degradação do anular. Em outras palavras, a integridade do riser conectado depende não só de “puxar até a posição”, mas de preservar as funções de ventilação, vedação e monitoramento previstas no arranjo final.  

_Fontes: `anp-28ecd3b4b0e4434d9511c613:p2-4:17.0-44.0`_

## 3. Critérios de controle operacional e resposta a desvios no pull-in

### 3.1 Operar dentro do envelope e tratar desvios como evento de integridade

O SGSS exige que o sistema submarino opere dentro dos **limites do envelope de segurança definido no projeto** e que desvios desses limites sejam **registrados, investigados** e tratados com medidas para minimizar recorrência. Também exige monitoramento das variáveis operacionais com limites de alarme e análise de tendências.  

Aplicado ao pull-in, isso significa que variáveis como forças de tração monitoradas, posições, configurações geométricas, interferências e condições da unidade/plataforma não devem ser avaliadas isoladamente; devem ser comparadas ao envelope permitido para aquela etapa. Se houver:

- aumento inesperado da força de tração;
- comportamento geométrico incompatível com a configuração prevista;
- evidência de contato/interferência;
- erro ou incerteza de posicionamento da unidade;
- funcionamento degradado de acessórios críticos;

então a situação deve ser tratada como **desvio operacional com implicação de integridade**, e não apenas como variação aceitável de execução, até que haja verificação técnica suficiente.

O mesmo alerta da ANP sobre perda de estanqueidade em duto flexível reforça que falhas de procedimento podem permitir a continuidade de bombeio ou pressurização sem detecção de anomalias, e que o operador deve rever procedimentos para garantir monitoramento adequado das linhas e evitar ultrapassar o envelope seguro após identificação de anomalia. A lição geral para o pull-in é clara: **procedimentos críticos precisam contemplar a detecção do desvio e a resposta a esse desvio**, não apenas a sequência nominal de execução.  

_Fontes: `anp-2e1d17d32fb37a1c34f1eeef:p2-5:22.0-3.0`, `anp-226946a12711e04f54ee4bfb:p61-66:27.0-8.0`_

### 3.2 Quando a contingência deixa de ser aceitável

O Relatório Anual de Segurança Operacional da ANP destaca situações com **barreiras de segurança degradadas sem medidas de contingenciamento adequadas**, perdas de contenção, equipamentos com inspeção vencida e deficiências em procedimentos de contingência. O relatório também ressalta que a priorização de manutenções e testes de elementos críticos é essencial e que ações mitigadoras devem se refletir nos indicadores de segurança de processo.  

Para o pull-in, a consequência prática é que a existência de:

- barreiras degradadas sem contingência robusta;
- elementos críticos indisponíveis ou sem inspeção/teste válido;
- procedimentos de contingência incompletos;
- comunicação operacional degradada;
- mudanças físicas/operacionais não avaliadas;

**aumenta a complexidade do gerenciamento do risco** e pode invalidar a decisão de seguir com a operação, mesmo que a execução mecânica pareça possível.  

Ainda segundo a ANP, o conceito **ALARP** não pode ser usado de forma inadequada para descartar salvaguardas eficazes e viáveis apenas porque causariam atraso de produção ou postergação logística. Em operações de pull-in, isso afeta decisões como continuar com equipamento degradado, adiar revisão documental, operar com contingência improvisada ou aceitar barreiras temporariamente indisponíveis sem demonstração técnica robusta de aceitabilidade do risco.  

_Fontes: `anp-ac2e4f9942314aa203e5b9b3:p32-34:40.0-40.0`, `anp-b2cfa8a9492ef598716e9685:p52-54:15.0-0.0`_

### 3.3 Resposta a cenários típicos de desvio

Com base nos modos de falha e nas exigências de integridade e controle operacional das fontes, um desvio no pull-in deve ser tratado por critérios como os abaixo:

#### a) Aumento inesperado da força de tração ou comportamento anômalo de carga

Deve motivar verificação imediata de:

- aderência ao envelope de segurança da etapa;
- possibilidade de configuração inadequada do riser;
- interferência com outros risers, casco ou embarcação;
- erro de posicionamento da UEP/FPSO;
- dano ou anomalia em equipamento auxiliar;
- necessidade de inspeção extraordinária antes da retomada.

A base regulatória não fornece valores-limite, mas exige monitoramento, registro, investigação de desvios e manutenção da integridade mecânica.  

#### b) Perda de posicionamento, mudança geométrica ou alteração física não prevista

Mudanças físicas e operacionais requerem **gestão de mudanças** e possível revisão da análise de riscos principal. O relatório da ANP de 2022 mostra que alterações em módulos e no **riser balcony** sem revisão dos estudos de risco foram tratadas como falhas relevantes de gestão. Assim, qualquer mudança de geometria, arranjo de acesso, interferência estrutural ou condição de aproximação do riser à unidade que não esteja coberta pelo cenário original deve ser reavaliada tecnicamente antes da continuação.  

#### c) Falha ou indisponibilidade de elemento crítico / sistema de comunicação

O SGSS requer sistema de comunicação adequado e confiável entre pontos remotos e a sala de controle, com procedimentos e critérios estabelecidos. Também requer procedimentos de SIMOPS com definição de responsabilidades e coordenação entre organizações envolvidas, incluindo resposta à emergência. Se a operação de pull-in depender de comunicação degradada, coordenação precária ou elemento crítico indisponível, o problema deixa de ser local e passa a ser sistêmico, afetando a capacidade de resposta a emergência e de controle coordenado da manobra.  

#### d) Indício de dano em vedação, vent, capa externa ou anular

Esse tipo de achado deve ser encaminhado como questão de integridade, com avaliação específica do mecanismo de falha aplicável: perda de vedação, corrosão, entrada de água do mar, entrada de oxigênio, ruptura/dano de capa externa, condição do bend stiffener e necessidade de monitoramento adicional.  

#### e) Suspensão ou abandono temporário da operação

Se a operação precisar ser interrompida e o sistema ficar temporariamente fora de operação, o SGSS exige que componentes/dutos/sistemas nessa condição permaneçam em **condições seguras**, com planos apropriados de inspeção, manutenção, monitoramento e controle de corrosão para o período correspondente.  

_Fontes: `anp-226946a12711e04f54ee4bfb:p61-66:27.0-8.0`, `anp-2e1d17d32fb37a1c34f1eeef:p2-5:22.0-3.0`, `anp-b2cfa8a9492ef598716e9685:p52-54:15.0-0.0`, `petroles-004c2afadba7ea17c7dd7908:pNone:2990169.0-2990204.0`_

## 4. Monitoramento, inspeção e aceitação de integridade

### 4.1 Monitoramento durante a execução

As fontes regulatórias exigem que a **tensão aplicada seja monitorada e registrada durante todo o lançamento, ainda que indiretamente**. Embora o trecho citado trate genericamente do lançamento, o princípio é aplicável às etapas de pull-in como parte da movimentação/instalação do sistema submarino.  

Além disso, o sistema deve monitorar variáveis operacionais com alarmes e tendências, e manter rastreabilidade das informações de controle operacional e integridade. Isso permite:

- reconstruir a história da manobra após um desvio;
- demonstrar aderência ou não ao envelope de segurança;
- fundamentar a avaliação de integridade pós-evento;
- decidir se a continuidade da operação é admissível.

_Fontes: `anp-2e1d17d32fb37a1c34f1eeef:p2-5:22.0-3.0`, `anp-226946a12711e04f54ee4bfb:p61-66:27.0-8.0`_

### 4.2 Inspeções iniciais, extraordinárias e foco em trechos críticos

O SGSS exige que a metodologia de inspeções, testes e ensaios contemple no mínimo:

- inspeções **iniciais, periódicas e extraordinárias**;
- justificativa do método de inspeção e critérios de aceitação;
- avaliação de processos corrosivos ou outros mecanismos de falha;
- mapeamento de pontos de medição e descontinuidades, quando aplicável;
- imagens, filmagens ou esquemas dos principais pontos de inspeção/descontinuidades;
- definição dos recursos necessários à inspeção.

Também exige **programa diferenciado de avaliação de integridade para trechos críticos**. Para o pull-in, isso orienta que, após desvio operacional, sejam priorizados os locais reconhecidamente mais vulneráveis nas fontes:

- conexão/terminação superior;
- zonas de curvatura acentuada;
- regiões de contato/interferência;
- bend stiffener e sua fixação;
- capa externa e indícios de alagamento do anular;
- sistema de vent e sinais de corrosão/ingresso indevido de gases.

Se a operação envolver conector emerso em riser flexível que conduz hidrocarboneto, as fontes recomendam sistema de **monitoramento de gás percolado**.  

_Fontes: `anp-226946a12711e04f54ee4bfb:p61-66:27.0-8.0`, `petroles-004c2afadba7ea17c7dd7908:pNone:2990188.0-2990221.0`, `petroles-004c2afadba7ea17c7dd7908:pNone:2990169.0-2990204.0`, `anp-28ecd3b4b0e4434d9511c613:p2-4:17.0-44.0`_

### 4.3 O que deve alimentar a decisão de aceitação pós-pull-in

Antes de aceitar a conclusão do pull-in, as fontes apontam para a necessidade de integrar:

- histórico operacional da etapa;
- registros de monitoramento de cargas/variáveis;
- resultados de inspeção visual/submarina e, quando aplicável, filmagens;
- avaliação dos mecanismos de falha pertinentes;
- verificação de anormalidades de comissionamento;
- atualização de desenhos, coordenadas e documentação do sistema, quando houver alteração ou desvio;
- registro formal das ações corretivas e preventivas.

A aceitação não deve se limitar a “conectou/não conectou”; deve demonstrar **adequação ao uso** do sistema submarino após a manobra e coerência com a integridade mecânica requerida pelo PGI.  

_Fontes: `anp-226946a12711e04f54ee4bfb:p61-66:27.0-8.0`, `anp-28ecd3b4b0e4434d9511c613:p2-4:17.0-44.0`_

## 5. SIMOPS, comunicação, treinamento e governança de contingências

### 5.1 Operações simultâneas e coordenação entre organizações

O SGSS determina que o operador estabeleça procedimentos para gerenciar **operações simultâneas (SIMOPS)**, abordando:

- identificação de novos perigos introduzidos pelas atividades simultâneas;
- verificação de medidas de prevenção/mitigação adequadas;
- definição de responsabilidades;
- coordenação entre todas as organizações envolvidas, incluindo a resposta à emergência.

Para o pull-in em FPSO, isso é especialmente relevante quando coexistem atividades submarinas, marine, topside, içamento, embarcações de apoio, ROV e condicionantes de posicionamento da unidade. Uma falha de coordenação pode transformar um desvio mecânico localizado em evento com múltiplas interfaces e resposta tardia.  

_Fontes: `anp-226946a12711e04f54ee4bfb:p61-66:27.0-8.0`_

### 5.2 Comunicação operacional

A exigência de sistema de comunicação adequado e confiável entre pontos remotos e sala de controle aplica-se diretamente a operações de pull-in, em que a resposta a aumento de carga, alteração de geometria, perda de visibilidade subsea ou necessidade de interrupção depende de comando e confirmação rápidos. Se o sistema de comunicação for degradado, a operação perde capacidade de coordenação e de resposta a contingência.  

O relatório da ANP de 2022 ilustra, de forma mais ampla, como falhas em sistemas críticos de comunicação e alarme podem ser tratadas como desvios graves.  

_Fontes: `anp-226946a12711e04f54ee4bfb:p61-66:27.0-8.0`, `anp-b2cfa8a9492ef598716e9685:p52-54:15.0-0.0`_

### 5.3 Competência, familiarização e procedimentos críticos

A ANP ressalta que equipes de contingência devem:

- estar **familiarizadas com a instalação**;
- realizar **treinamento antes** de assumir suas funções;
- conhecer especificidades de cada unidade, incluindo **gestões de mudança, inibições e contingências** em vigor.

Outro alerta da ANP recomenda classificar **procedimentos operacionais críticos** e exigir APR específica, com participação de especialistas de SMS, antes da sua realização. Também reforça a necessidade de revisão controlada de procedimentos e documentos.  

Para o pull-in, isso significa que a resposta a falhas não pode depender de improvisação por equipe pouco familiarizada com o arranjo específico do FPSO, do riser ou das interfaces de instalação.  

_Fontes: `anp-ac2e4f9942314aa203e5b9b3:p32-34:40.0-40.0`, `anp-2e1d17d32fb37a1c34f1eeef:p2-5:22.0-3.0`_

## 6. Síntese prática para tomada de decisão em contingência

À luz das fontes, uma resposta tecnicamente defensável a falhas ou desvios no pull-in deve, no mínimo, verificar se há simultaneamente:

1. **Integridade estrutural preservada** nas regiões críticas do riser e acessórios associados;  
2. **Operação dentro do envelope de segurança** ou, se houve desvio, registro e investigação formal antes de prosseguir;  
3. **Barreiras e elementos críticos disponíveis**, ou contingência adequadamente demonstrada;  
4. **Comunicação e coordenação eficazes** entre sala de controle, ponto remoto, equipes subsea/topside/marine e organizações contratadas;  
5. **Gestão de mudanças atualizada** para qualquer alteração física, operacional ou documental relevante;  
6. **Inspeção extraordinária e avaliação de integridade** quando o evento puder ter causado dano localizado, corrosão, perda de vedação, interferência ou mudança de geometria;  
7. **Rastreabilidade completa** dos dados operacionais, inspeções, anormalidades e ações corretivas/preventivas.

Quando um ou mais desses elementos estiverem comprometidos, a tendência das fontes é tratar a situação como incompatível com a condução segura da operação até reavaliação técnica adequada.  

_Fontes: `anp-226946a12711e04f54ee4bfb:p61-66:27.0-8.0`, `anp-ac2e4f9942314aa203e5b9b3:p32-34:40.0-40.0`, `anp-b2cfa8a9492ef598716e9685:p52-54:15.0-0.0`, `petroles-004c2afadba7ea17c7dd7908:pNone:2990169.0-2990204.0`, `anp-28ecd3b4b0e4434d9511c613:p2-4:17.0-44.0`_