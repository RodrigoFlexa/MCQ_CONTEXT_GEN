# Planejamento e riscos combinados em SIMOPS no FPSO

## 1. Conceito operacional de SIMOPS e implicações para o planejamento
SIMOPS (Simultaneous Operations, operações simultâneas) pode ser entendido, com base nos trechos fornecidos, como a condução de operações independentes cujos eventos de uma podem impactar a segurança pessoal, a integridade de equipamentos ou o meio ambiente da outra. Embora o exemplo mais citado nas fontes seja a combinação entre produção, perfuração e atividades de projeto, o conceito é mais amplo: qualquer combinação de operações que crie interferência relevante de risco deve ser tratada como SIMOPS.

Para fins de planejamento em FPSO, o ponto central não é apenas a simultaneidade temporal, mas a **interdependência de risco** entre atividades. Duas tarefas executadas ao mesmo tempo só se tornam um caso de SIMOPS relevante quando houver possibilidade de uma afetar:

- as barreiras preventivas ou mitigadoras da outra;
- a resposta a emergências;
- a disponibilidade de equipamentos críticos;
- a ocupação segura de áreas e rotas;
- a exposição de pessoas, ativos e meio ambiente a consequências combinadas.

Assim, o planejamento de SIMOPS deve partir da pergunta: **quais atividades são independentes na execução, mas dependentes em risco?**

**Fontes utilizadas:** `regis-962e222ee3c37dec82110fd6:pNone:3995.0-4281.0`

## 2. Base de identificação de conflitos: avaliar interfaces, não apenas tarefas isoladas
As fontes indicam um cuidado metodológico importante: a análise não deve se concentrar apenas no sistema usado para executar o trabalho; também deve considerar o sistema que está sendo construído, modificado, testado ou colocado em risco. O exemplo fornecido é claro: na perfuração de um poço, tanto a sonda quanto o próprio poço precisam ser analisados.

Transpondo esse princípio para SIMOPS em FPSOs, o planejamento deve identificar conflitos em pelo menos dois níveis:

### 2.1. Sistema executor
É o conjunto de recursos que realiza a tarefa, por exemplo:
- guindaste e acessórios de içamento;
- sistema de offloading e seus mangotes/terminações;
- unidade ou spread de intervenção em poço;
- embarcação de apoio associada à atividade;
- equipe, procedimento, permissões, supervisão e meios de comunicação.

### 2.2. Sistema afetado ou exposto
É o sistema cujo estado pode mudar ou ser degradado em função da atividade simultânea, por exemplo:
- poço em perfuração, completação, restauração ou abandono;
- sistema de processo em produção;
- arranjo de exportação/offloading;
- barreiras instrumentadas ou mecânicas temporariamente indisponíveis;
- áreas classificadas e zonas de acesso restrito.

Esse raciocínio é particularmente relevante quando há interface entre FPSO, poços e sistemas submarinos: uma mesma atividade pode parecer local, mas alterar o estado global de risco da instalação.

**Fontes utilizadas:** `regis-15cf521b35d1f84d2c0bf17e:pNone:9965.0-10298.0`

## 3. Dependência da fase operacional e do ciclo de vida
As fontes mostram que os perigos não são uniformes ao longo do ciclo de vida do poço. O método descrito confronta perigos com fases operacionais e mostra que certos perigos aparecem apenas em fases específicas. No estudo citado, "operações simultâneas nas atividades da plataforma fixa" apareceram como perigo mapeado em determinadas fases do ciclo de vida do poço, e não em todas.

O ensinamento aplicável ao planejamento de SIMOPS em FPSOs é que a compatibilidade entre atividades deve ser analisada **por fase operacional**, e não apenas por tipo genérico de tarefa. Uma intervenção que seria tolerável em determinada condição pode ser incompatível em outra porque mudam:

- as energias presentes;
- a condição de pressão/fluxo do poço ou do processo;
- o inventário de hidrocarbonetos exposto;
- a necessidade de detecção, monitoramento e resposta;
- a criticidade das barreiras necessárias.

As fontes também descrevem fases típicas do ciclo de vida de poços marítimos, incluindo perfuração, completação, operação (produção/injeção), restauração e abandono. Em SIMOPS envolvendo FPSO e poços, essa segmentação é útil porque o conflito de risco entre atividades deve ser verificado **fase a fase**.

Exemplo prático: a coexistência entre produção estável e uma intervenção em poço tende a exigir avaliação diferente da coexistência entre offloading e uma atividade de acesso ao reservatório, pois os cenários acidentais, as energias em jogo e as barreiras requeridas não são os mesmos.

**Fontes utilizadas:** `regis-15cf521b35d1f84d2c0bf17e:pNone:9965.0-10298.0`, `regis-15cf521b35d1f84d2c0bf17e:pNone:10132.0-10448.0`

## 4. Análise de riscos combinados: abordagem qualitativa, dinâmica e orientada a barreiras

### 4.1. Ferramentas e definições úteis
Os trechos fornecem definições úteis para estruturar a análise:

- **Risco**: combinação de probabilidade e consequência de um perigo se consumar.
- **HAZID/APR**: ferramenta qualitativa para identificar perigos e suas consequências indesejáveis, incluindo avaliação de severidade e probabilidade.
- **Bow-Tie**: representação gráfica de causas/ameaças, evento principal e barreiras preventivas/mitigadoras.
- **Função da barreira de segurança**: função planejada para prevenir, controlar ou mitigar evento indesejável.
- **SOOB**: estrutura de limites operacionais para apoiar líderes na decisão sobre continuar ou não uma atividade quando a efetividade de certas barreiras pode estar comprometida.

Para SIMOPS, essas definições permitem organizar o planejamento de forma coerente:
1. identificar as atividades simultâneas e os cenários de interferência;
2. descrever ameaças cruzadas entre elas;
3. definir quais barreiras previnem a escalada do evento;
4. verificar se essas barreiras continuam disponíveis e efetivas durante a simultaneidade;
5. estabelecer limites para continuidade, restrição ou suspensão.

### 4.2. Por que o risco combinado não pode ser tratado como soma simples de APRs isoladas
Os trechos sobre engenharia de poços destacam que atividades de construção e reparo ocorrem em regime transiente: uma operação pode alterar o estado do poço rapidamente, tornando-o inseguro de uma hora para outra. Por isso, a análise de risco precisa incorporar mudanças das condições ao longo das atividades.

Essa observação é diretamente útil ao planejamento de SIMOPS em FPSOs quando houver interface com poços/subsea: não basta aprovar duas APRs separadas. É necessário avaliar o **efeito combinado e evolutivo** da simultaneidade, por exemplo:

- uma operação altera o estado do poço ou do sistema de processo enquanto outra depende daquele estado para permanecer segura;
- uma mudança operacional reduz a confiabilidade de detecção, isolamento ou resposta;
- uma atividade consome recursos críticos de supervisão, monitoramento ou evacuação necessários à outra.

Portanto, em SIMOPS de maior criticidade, a análise precisa ser revista sempre que houver alteração de estado relevante, e não apenas no início da janela de trabalho.

### 4.3. Critério de aceitação e decisão
As fontes classificam riscos como:
- **aceitáveis**;
- **ALARP** (As Low As Reasonably Practicable/Possible, conforme grafado na fonte), situação em que o risco deve ser mitigado até nível mínimo razoável;
- **inaceitáveis**.

A lógica decisória extraível para o planejamento é:
- se o risco combinado for aceitável, a simultaneidade pode ser planejada com os controles previstos;
- se estiver em zona ALARP, devem ser adotadas medidas mitigadoras adicionais antes da execução;
- se for inaceitável, o arranjo simultâneo não deve prosseguir na forma proposta.

Esse critério é particularmente importante quando a simultaneidade afeta barreiras de alto valor preventivo, como controle de poço, detecção de gás, bloqueio automático, sistemas de combate a incêndio ou meios de monitoramento contínuo.

**Fontes utilizadas:** `regis-962e222ee3c37dec82110fd6:pNone:3995.0-4281.0`, `regis-15cf521b35d1f84d2c0bf17e:pNone:4233.0-4433.0`, `regis-15cf521b35d1f84d2c0bf17e:pNone:10132.0-10448.0`

## 5. Identificação prática de conflitos em SIMOPS
Com base nos cenários e controles listados nas planilhas HAZID fornecidas, alguns grupos de conflito são particularmente relevantes para o planejamento.

### 5.1. Movimentação de cargas e operações de içamento
As fontes associam operações de içamento a riscos como colisão de equipamentos, ruptura de cabos, queda de ferramentas e múltiplas fatalidades, com controles como:
- checklist pré-içamento;
- inspeção e manutenção prévia;
- inventário de acessórios;
- plano de içamento;
- sinaleiro;
- restrição de acesso à área;
- teste de segurança no sistema de içamento;
- supervisão;
- treinamento e competência;
- uso de **SOOB** para restrições operacionais.

Em planejamento de SIMOPS, esse conjunto indica que atividades de içamento não devem ser avaliadas isoladamente. Devem ser verificadas as interferências com:
- ocupação de áreas adjacentes;
- rotas de fuga e zonas de exclusão;
- operações que dependam de permanência de pessoas em área potencial de queda de carga;
- necessidade de manter barreiras livres e acessíveis.

### 5.2. Operações de perfilagem/canhoneio com explosivos
Para transporte, manuseio e uso de explosivos, as fontes associam o cenário a fatalidades ou múltiplas fatalidades e indicam controles como:
- APR;
- notificação prévia;
- SIMOPS;
- permissão de trabalho;
- procedimento específico de canhoneio;
- restrição de acesso à área;
- sistema de comunicação;
- sistema de detecção e combate a incêndio;
- treinamento e competência.

A implicação para o planejamento é clara: quando há explosivos ou fontes especiais na instalação, a simultaneidade exige coordenação reforçada, segregação de áreas e revisão das demais atividades em curso, especialmente aquelas que poderiam dificultar isolamento, monitoramento ou resposta.

### 5.3. Acesso ao reservatório e cenários de perda de controle de poço
As fontes apresentam, para hidrocarbonetos sob pressão e liberação indesejada de gás natural, controles como:
- análise de risco específica para o poço;
- BOP;
- detector de gás;
- gestão de mudanças (MOC);
- monitoramento de parâmetros do poço e mud logging;
- mapa de áreas classificadas;
- medidor de H2S;
- simulados de kick e de controle de poço;
- plano de emergência individual e plano de resposta à emergência;
- restrição de acesso;
- supervisão.

Para SIMOPS, isso mostra que intervenções ligadas à integridade do poço e ao acesso ao reservatório não podem ser tratadas apenas como mais uma tarefa dentro da carteira do dia. Elas mudam substancialmente o perfil de risco da instalação e podem impor restrições a outras atividades simultâneas, principalmente se estas dependerem de disponibilidade plena de áreas, equipes de resposta, comunicação, detecção ou isolamento.

**Fontes utilizadas:** `regis-962e222ee3c37dec82110fd6:pNone:5930.0-6566.0`

## 6. Controles de planejamento que precisam ser integrados entre as atividades simultâneas
Os trechos fornecem um conjunto consistente de controles que, embora apareçam em cenários diferentes, podem ser organizados como requisitos integradores do planejamento de SIMOPS:

### 6.1. Identificação formal de perigos e pré-planejamento multidisciplinar
- HAZID/APR para identificar ameaças e consequências;
- planejamento de poço (DWOP) com participação das partes interessadas;
- análise de risco específica para o poço quando a atividade alterar seu estado;
- uso de brainstorming/multidisciplinaridade como suporte à identificação de interfaces e cenários.

### 6.2. Controle operacional e autorização
- permissão de trabalho;
- checklist pré-atividade;
- procedimentos operacionais específicos e claros;
- restrição de acesso a áreas afetadas;
- notificação prévia para atividades críticas;
- definição de limites operacionais/restrições por SOOB.

### 6.3. Barreira técnica e disponibilidade de salvaguardas
- sistemas de detecção e combate a incêndio;
- detectores de gás e medidores específicos, como H2S;
- barreiras de controle de poço, como BOP;
- monitoramento contínuo de parâmetros operacionais;
- bloqueios automáticos e intertravamentos, quando aplicáveis.

### 6.4. Pessoas, comunicação e resposta
- sistema de comunicação confiável;
- supervisão;
- treinamento e competência;
- simulados e preparo para resposta a emergências;
- definição de responsabilidades sobre manutenção, operação e vigilância dos sistemas envolvidos.

Esses controles não devem ser apenas listados em documentos separados. O planejamento de SIMOPS deve verificar se eles permanecem **compatíveis entre si** quando duas ou mais atividades ocorrem ao mesmo tempo. O simples fato de cada atividade possuir seu próprio procedimento não garante que o conjunto seja seguro.

**Fontes utilizadas:** `regis-962e222ee3c37dec82110fd6:pNone:3995.0-4281.0`, `regis-962e222ee3c37dec82110fd6:pNone:5930.0-6566.0`

## 7. Gestão de mudanças como elemento crítico do planejamento de SIMOPS
O alerta da ANP sobre vazamento durante offloading mostra um ponto decisivo para planejamento de operações simultâneas: alterações de configuração, de procedimento ou de forma de execução podem criar risco novo ou degradar salvaguardas existentes.

No caso relatado, foram identificadas, entre outras, as seguintes causas:
- falta de gestão de mudança para avaliar a execução do pull-in dos mangotes com instruções diferentes do manual do fornecedor;
- ausência de atualização do HAZOP após alteração que removeu uma salvaguarda de bloqueio por baixa pressão;
- indefinição de responsabilidade de manutenção do sistema;
- falhas documentais do fornecedor;
- ausência de monitoramento/vigilância conforme previsto em padrão corporativo;
- falhas de treinamento e de verificação de conformidade com procedimento.

Para o planejamento de SIMOPS em FPSO, isso leva a conclusões práticas importantes:

1. **Mudança de procedimento é mudança de risco**, mesmo que a tarefa pareça rotineira.
2. **Retirada ou degradação de uma salvaguarda** exige reavaliação formal da compatibilidade entre operações simultâneas.
3. **Documentação incoerente** entre instalação, fornecedor e padrão corporativo pode gerar conflito operacional durante a execução.
4. **Monitoramento dedicado** faz parte da barreira; sua ausência não é detalhe administrativo.
5. Em operações de offloading, a interface entre FPSO, sistema de transferência e navio aliviador precisa ser tratada como sistema integrado para fins de risco.

Esse caso reforça que, no planejamento de SIMOPS, a pergunta não deve ser apenas "as atividades podem ocorrer juntas?", mas também "houve alguma mudança de configuração, manual, responsabilidade, treinamento ou vigilância que altere a resposta?".

**Fontes utilizadas:** `anp-13a33bb67429b09d3272c53e:p1-4:0.0-0.0`

## 8. Critérios práticos para decidir se uma simultaneidade é compatível
Com base nas fontes, uma decisão técnica de permitir SIMOPS deve ser sustentada, no mínimo, pelos seguintes elementos:

### 8.1. Condições favoráveis para prosseguir
A simultaneidade tende a ser mais defensável quando:
- os perigos e interferências cruzadas foram identificados por análise específica;
- a fase operacional e o estado do sistema foram explicitamente considerados;
- as barreiras preventivas e mitigadoras requeridas estão disponíveis e verificadas;
- eventuais limites operacionais foram definidos e comunicados;
- procedimentos, permissões, responsabilidades e comunicações são coerentes entre todas as partes;
- monitoramento e vigilância estão adequadamente definidos;
- não há mudança não tratada de configuração, manual, salvaguarda ou responsabilidade.

### 8.2. Sinais de que a simultaneidade deve ser restringida, replanejada ou recusada
A simultaneidade torna-se tecnicamente frágil quando houver, por exemplo:
- condição transiente do poço ou do processo sem análise dinâmica adequada;
- remoção, bypass, indisponibilidade ou dúvida sobre a efetividade de salvaguardas;
- conflito documental entre procedimento local e orientação do fabricante;
- indefinição de responsabilidade por inspeção, manutenção ou operação do equipamento envolvido;
- monitoramento insuficiente ou inexistente em ponto crítico da operação;
- treinamento ou competência inadequados da força de trabalho ou contratada;
- necessidade de resposta emergencial que possa ser prejudicada pela outra atividade simultânea.

### 8.3. Uso do histórico de incidentes e do julgamento técnico
As fontes lembram que falha de equipamento e erro humano aparecem como causas frequentes de incidentes, e também alertam que ferramentas quantitativas não devem substituir o julgamento pessoal. Em SIMOPS, isso significa que números, matrizes e planilhas são apoio à decisão, mas não dispensam avaliação técnica qualificada sobre a combinação real de atividades e barreiras.

**Fontes utilizadas:** `regis-15cf521b35d1f84d2c0bf17e:pNone:4233.0-4433.0`, `regis-15cf521b35d1f84d2c0bf17e:pNone:10132.0-10448.0`, `anp-13a33bb67429b09d3272c53e:p1-4:0.0-0.0`

## 9. Síntese aplicável ao foco da faceta: planejamento e riscos combinados
Para o foco desta faceta, o ensinamento principal dos materiais é que o planejamento de SIMOPS em FPSO deve ser estruturado como **análise de interfaces e de riscos combinados**, e não como simples coexistência administrativa de atividades. Em termos práticos:

- identificar a simultaneidade relevante a partir da interdependência de risco;
- analisar tanto o sistema executor quanto o sistema afetado;
- considerar a fase operacional/ciclo de vida, especialmente quando houver poços e atividades submarinas envolvidas;
- usar HAZID/APR, Bow-Tie e critérios de aceitação de risco para organizar a decisão;
- tratar estados transitórios e mudanças de configuração por análise dinâmica e MOC;
- confirmar disponibilidade real de barreiras, monitoramento, comunicação, competência e resposta a emergência;
- impor restrições operacionais ou cancelar a simultaneidade quando o risco combinado ultrapassar o aceitável ou permanecer sem mitigação suficiente.

Essa abordagem não elimina a necessidade de procedimentos locais, mas fornece uma base técnica para avaliar conflitos e tomar decisões de compatibilidade entre operações simultâneas.

**Fontes utilizadas:** `regis-962e222ee3c37dec82110fd6:pNone:3995.0-4281.0`, `regis-15cf521b35d1f84d2c0bf17e:pNone:4233.0-4433.0`, `regis-15cf521b35d1f84d2c0bf17e:pNone:9965.0-10298.0`, `regis-15cf521b35d1f84d2c0bf17e:pNone:10132.0-10448.0`, `regis-962e222ee3c37dec82110fd6:pNone:5930.0-6566.0`, `anp-13a33bb67429b09d3272c53e:p1-4:0.0-0.0`