# RCM, FMEA e tarefas: seleção de estratégias de manutenção a partir dos modos de falha e suas consequências

## 1. Finalidade técnica do RCM no contexto de ativos offshore
A **manutenção centrada em confiabilidade (RCM)** é uma metodologia sistemática usada para definir atividades de manutenção para itens críticos, com foco em manter o ativo cumprindo suas **funções requeridas no contexto operacional real**. O ponto central não é “devolver o equipamento ao estado perfeito”, mas **preservar um estado funcional aceitável dentro de limites operacionais definidos**.

No uso prático em FPSOs/FSOs, isso significa que a seleção de tarefas de manutenção deve partir de perguntas estruturadas:
- quais funções o sistema deve cumprir;
- como ele pode deixar de cumprir essas funções;
- quais eventos causam essa perda funcional;
- o que acontece quando a falha ocorre;
- quão importante é essa consequência;
- o que pode ser feito para prevenir, detectar ou mitigar a falha;
- o que fazer quando não existe tarefa preventiva aplicável e eficaz.

Um ponto importante do RCM é a distinção entre **confiabilidade inerente** e **desempenho obtido em operação**. Um programa de manutenção preventiva efetivo pode verificar e sustentar a confiabilidade inerente do equipamento, mas **não aumenta essa confiabilidade por si só**; quando a causa do problema está no projeto, na construção ou na adequação do item ao serviço, a melhoria real depende de **redesign ou modificação**.

**Fontes da seção:** `petroles-4ee4bce16acf674505c8912d:pNone:2395829.0-2395881.0`, `petroles-4ee4bce16acf674505c8912d:pNone:2395857.0-2395908.0`

## 2. Conceitos estruturantes para análise de falhas
Para que um plano de manutenção seja consistente, o RCM exige uma terminologia funcional clara.

### 2.1 Sistema e subsistema
- **Sistema**: a planta como um todo ou uma subdivisão relevante para a análise.
- **Subsistema**: conjunto de equipamentos/componentes que desempenham uma ou mais funções e podem ser tratados como unidade funcional separada.

Em uma unidade offshore, isso pode ser aplicado, por exemplo, a um sistema de compressão, geração e distribuição elétrica, utilidades, lubrificação, selagem, proteção ou automação. Esses exemplos são apenas ilustrativos do uso da metodologia.

### 2.2 Função e padrão de desempenho
A análise começa pela definição das **funções requeridas** e dos **padrões de desempenho desejados** no contexto operacional vigente. A qualidade da análise depende fortemente da capacidade de identificar todas as funções relevantes do item.

### 2.3 Falha funcional
A **falha funcional** descreve como o subsistema deixa de cumprir sua função. Pode haver mais de uma falha funcional para uma mesma função.

### 2.4 Modo de falha
O **modo de falha** é a condição específica, associada a um equipamento ou componente, que leva à perda da função do subsistema. No RCM, a identificação do modo de falha deve ir além do sintoma e buscar a **causa específica**, para evitar tratar apenas efeitos superficiais.

### 2.5 Efeito e consequência da falha
- **Efeito da falha**: o que ocorre quando o modo de falha se manifesta.
- **Consequência da falha**: importância desse efeito para segurança, meio ambiente, operação, economia e disponibilidade.

A noção de **item funcionalmente significativo** é central: devem receber atenção prioritária os itens cujos modos de falha tenham significado econômico, de segurança ou impacto relevante sobre a missão/operação do sistema.

**Fontes da seção:** `petroles-4ee4bce16acf674505c8912d:pNone:2395857.0-2395908.0`

## 3. Encadeamento lógico do RCM para chegar às tarefas de manutenção
Uma formulação prática do RCM pode ser resumida nas etapas abaixo.

### 3.1 Definir funções e padrões de desempenho
Primeiro, define-se o que cada ativo físico deve fazer e sob quais limites de desempenho.

### 3.2 Identificar falhas funcionais
Em seguida, identificam-se as formas pelas quais o ativo deixa de atender sua função.

### 3.3 Identificar modos de falha e causas
Para cada falha funcional, levantam-se os eventos causais prováveis. O detalhamento da causa é importante para não desperdiçar esforço em ações que apenas aliviam sintomas.

### 3.4 Levantar efeitos da falha
Descreve-se o que acontece quando o modo de falha ocorre: perda de capacidade, atuação de proteção, degradação de desempenho, indisponibilidade, dano secundário etc.

### 3.5 Analisar consequências
As consequências orientam a decisão. Não basta saber que uma falha acontece; é preciso entender **por que ela importa** e **qual risco ou perda ela produz**.

### 3.6 Selecionar tarefa proativa ou ação default
Se existir uma tarefa tecnicamente aplicável e eficaz para prevenir ou detectar a falha em tempo hábil, ela pode ser incluída no plano. Se não existir, o RCM indica a necessidade de avaliar ações como:
- mudança de estratégia;
- modificação de projeto;
- aceitação controlada de manutenção não programada/corretiva;
- reparo funcional ou outras medidas compensatórias.

A implementação de RCM requer bom conhecimento do processo e dos equipamentos, além do envolvimento de operadores, técnicos e especialistas, porque confiabilidade, segurança e custo dependem de entendimento multidisciplinar.

**Fontes da seção:** `petroles-4ee4bce16acf674505c8912d:pNone:2395857.0-2395908.0`

## 4. FMEA/FMECA como base para a escolha das tarefas
A **FMEA (Failure Modes and Effects Analysis)** é a análise de modos de falha e seus efeitos. A **FMECA** acrescenta a avaliação de criticidade.

### 4.1 Finalidade
Essas ferramentas servem para:
- identificar como um componente pode falhar;
- levantar causas possíveis de cada falha;
- descrever efeitos no sistema e em outros componentes;
- apoiar ações corretivas ou preventivas para evitar recorrência;
- registrar conhecimento sobre mecanismos de falha e consequências.

Na manutenção, a FMEA/FMECA é útil porque transforma experiência dispersa em um registro técnico estruturado, que pode ser atualizado ao longo da vida do ativo. O material consultado destaca que esse registro deve ser tratado como **documento vivo**, atualizado após mudanças de projeto, novos históricos de falha e revisões de estratégia.

### 4.2 Informações mínimas a registrar
Os trechos consultados indicam, no mínimo, os seguintes campos para a análise:
- identificação do sistema;
- participantes da equipe;
- componentes analisados;
- função de cada componente;
- modo potencial de falha;
- efeitos potenciais da falha;
- severidade do efeito;
- causas potenciais da falha;
- ocorrência estimada;
- controles atuais;
- detecção/probabilidade de detecção.

Esse conjunto é suficiente para transformar o raciocínio de confiabilidade em decisões de manutenção rastreáveis.

### 4.3 Número de prioridade de risco
Uma forma difundida de priorização na FMECA é o cálculo do **NPR/RPN**:

**NPR (ou RPN) = Ocorrência × Severidade × Detecção**

ou, em outra formulação equivalente encontrada no material:

**RPN = Probabilidade de Ocorrência × Severidade × Detectabilidade**

O número resultante ajuda a **priorizar ações**, mas não substitui a análise de engenharia. O próprio contexto operacional, a função do item, a consequência real da falha e a aplicabilidade da tarefa precisam ser considerados antes de converter o ranking em plano de manutenção.

**Fontes da seção:** `petroles-4ee4bce16acf674505c8912d:pNone:703696.0-703726.0`, `regis-63a2aa91eb522ba1c06754d8:pNone:3418.0-3740.0`

## 5. Como as consequências determinam a estratégia de manutenção
No material consultado, o processo clássico de RCM trata as consequências das falhas em quatro grupos principais:
- **falhas ocultas**;
- falhas com consequências para **segurança ou meio ambiente**;
- falhas **operacionais**;
- falhas **não operacionais**.

Há também uma formulação adaptada que subdivide as consequências em dimensões humana, ambiental, financeira e operacional. Para seleção de tarefas em manutenção, o ponto técnico essencial é que **a consequência muda a lógica de decisão**.

### 5.1 Falhas ocultas
São especialmente críticas em sistemas de proteção, reservas ou redundâncias, porque podem permanecer sem evidência até que o item seja demandado. Nesses casos, a tarefa típica é **teste de falha oculta** ou **failure-finding**, para verificar se a função estará disponível quando solicitada.

### 5.2 Segurança e meio ambiente
Quando a falha pode afetar pessoas ou meio ambiente, a manutenção preventiva só deve ser adotada se for **aplicável** e **eficaz** para manter o risco em nível aceitável. Se não houver tarefa preventiva confiável, o RCM remete à avaliação de ações default, como **modificação de projeto** ou outras barreiras.

### 5.3 Consequências operacionais
Aqui a decisão tende a balancear disponibilidade, custo e perda de produção. Tarefas proativas são justificadas quando evitam indisponibilidade relevante ou reduzem custo total do ciclo de vida.

### 5.4 Consequências não operacionais
Quando o efeito não compromete segurança, meio ambiente nem produção de forma relevante, pode ser tecnicamente aceitável operar com estratégia mais simples, inclusive **corretiva**, desde que o risco permaneça administrável.

### 5.5 Critérios de aplicabilidade e eficácia
Os trechos consultados distinguem dois filtros fundamentais:

**Aplicabilidade**
- a tarefa consegue tecnicamente prevenir, detectar ou reduzir a probabilidade do modo de falha?
- é possível executá-la com a frequência necessária?
- a característica do modo de falha permite monitoramento por condição, restauração planejada ou descarte planejado?

**Eficácia**
- para falhas ocultas: a tarefa reduz a probabilidade de falhas múltiplas ou indisponibilidade não percebida?
- para segurança/meio ambiente: a tarefa mantém o risco em patamar aceitável?
- para operacionais e não operacionais: a tarefa é tecnicamente válida e economicamente justificável?

As atividades proativas citadas no material incluem:
- **restauração planejada**;
- **descarte planejado**;
- **manutenção baseada na condição**.

Quando esses requisitos não são satisfeitos, entram em análise ações default, como:
- **modificação de projeto**;
- **reparo funcional**;
- **manutenção não programada**.

**Fontes da seção:** `petroles-4ee4bce16acf674505c8912d:pNone:2396191.0-2396238.0`

## 6. Seleção entre manutenção baseada em condição, preventiva por tempo e corretiva
Os trechos consultados reforçam que o RCM busca alocar tarefas **preventivas e preditivas eficientes**, e não simplesmente aumentar o volume de intervenções programadas.

### 6.1 Quando faz sentido priorizar manutenção baseada em condição
A manutenção baseada em condição é particularmente adequada quando:
- o modo de falha apresenta **sinais de aviso** antes da falha funcional;
- existe variável observável ou mensurável relacionada à degradação;
- o acompanhamento consegue identificar o defeito em fase inicial;
- a intervenção pode ser planejada antes da perda da função.

Em ambiente offshore, o material consultado indica que estratégias com **verificações sistemáticas e mais frequentes**, inclusive realizadas pela operação e apoiadas por especialistas onshore, podem:
- reduzir o número de intervenções preventivas desnecessárias;
- aumentar a disponibilidade média do sistema;
- aumentar a confiabilidade percebida em operação;
- detectar defeitos ainda em estágio inicial.

### 6.2 Limites do monitoramento humano e instrumental
O material também destaca duas observações importantes:
- inspeções sensoriais realizadas por operadores são de **baixo custo** e úteis para identificação de anormalidades;
- porém, quando a falha iminente é percebida pelos sentidos humanos, muitas vezes a degradação já está em **estágio avançado**, restando pouco tempo para agir.

Por isso, para modos de falha compatíveis, a integração entre sensores, instrumentação e análise de condição tende a oferecer diagnóstico mais rápido e preciso.

### 6.3 Quando a preventiva por tempo pode ser necessária
A estratégia por tempo tende a ser empregada quando o modo de falha admite restauração ou substituição planejada com benefício claro, e quando a evolução da degradação não é bem capturada por condição.

### 6.4 Quando a corretiva pode ser aceitável
A manutenção corretiva planejada ou a aceitação de falha em serviço pode ser racional quando:
- a consequência é baixa;
- não há impacto relevante em segurança, meio ambiente ou operação;
- não existe tarefa preventiva aplicável e eficaz;
- o custo de prevenir supera o custo controlado de corrigir.

**Fontes da seção:** `petroles-4ee4bce16acf674505c8912d:pNone:2395829.0-2395881.0`, `petroles-4ee4bce16acf674505c8912d:pNone:703696.0-703726.0`, `regis-74dd376119cbb653fe9922bc:pNone:33090.0-33377.0`

## 7. Falhas ocultas, redundância e testes funcionais
Um exemplo relevante do material é o de um sistema de lubrificação de compressor com bomba reserva. Após a parada da turbina auxiliar, a bomba reserva entrou em operação, porém uma **válvula de retenção emperrada** permitiu o esvaziamento dos acumuladores, causando queda de pressão e desarme do conjunto. A falha básica inicial existia, mas a severidade operacional foi ampliada pela **indisponibilidade oculta** do caminho redundante.

O ensinamento técnico é direto: em componentes redundantes, de reserva ou de proteção, é insuficiente presumir disponibilidade apenas porque o item está instalado. É necessário executar **testes funcionais periódicos** capazes de revelar falhas ocultas.

Do ponto de vista do plano de manutenção, isso leva a uma regra prática:
- se o modo de falha só aparece quando o item é demandado, a tarefa dominante tende a ser **teste funcional/failure-finding**;
- se o modo de falha apresenta tendência mensurável, a tarefa dominante tende a ser **monitoramento por condição**;
- se o item sofre envelhecimento previsível e restaurável, pode-se considerar **restauração/substituição planejada**;
- se nenhuma dessas opções é tecnicamente válida, avalia-se **mudança de projeto** ou **aceitação controlada de corretiva**.

**Fontes da seção:** `petroles-4ee4bce16acf674505c8912d:pNone:703696.0-703726.0`, `petroles-4ee4bce16acf674505c8912d:pNone:2396191.0-2396238.0`

## 8. Exemplo de raciocínio aplicado a modos de falha típicos de equipamentos rotativos
Os exemplos abaixo não pretendem fixar periodicidades universais; servem apenas para mostrar como o raciocínio RCM/FMEA pode ser estruturado.

### 8.1 Desalinhamento com dano em mancais
Modo de falha citado no material: **elevado desalinhamento entre eixos**, levando a danos nos mancais e, por consequência, ao conjunto rotativo.

**Seleção provável de tarefas**
- monitoramento de vibração e comportamento operacional;
- verificações de alinhamento após intervenções ou eventos que possam alterar geometria;
- inspeções dirigidas quando houver sintomas de aumento de temperatura, ruído ou vibração.

**Lógica de seleção**
- se o desalinhamento produz sintomas detectáveis antes da falha funcional, a estratégia favorece **manutenção baseada em condição**;
- se a consequência operacional é alta, a tarefa ganha prioridade;
- se houver risco de dano secundário extenso, pode ser necessária combinação de inspeção e ação corretiva planejada.

### 8.2 Depósitos em difusores ou impelidores
Modo de falha citado: **depósitos de sujeira** associados à presença de líquidos condensáveis no gás.

**Seleção provável de tarefas**
- acompanhamento de desempenho do equipamento;
- inspeções internas em campanhas/paradas compatíveis;
- ações de controle de processo/contaminação quando aplicáveis.

**Lógica de seleção**
- a falha tende a degradar performance antes de causar perda total da função;
- portanto, costuma ser compatível com **monitoramento por condição e desempenho**.

### 8.3 Desgaste de selos labirinto e pistão de balanceamento
Modo de falha citado: desgaste por sucção de partículas, com **redução de performance** e **sobrecarga do mancal de escora**.

**Seleção provável de tarefas**
- monitoramento de performance e condição do equipamento;
- inspeções em parada programada;
- reforço de controles para evitar ingresso de partículas, quando aplicável.

**Lógica de seleção**
- a tarefa deve bloquear o mecanismo causal ou detectar precocemente sua progressão;
- quando o defeito for progressivo e observável, a manutenção baseada em condição tende a ser preferível à troca por calendário puro.

**Fontes da seção:** `petroles-4ee4bce16acf674505c8912d:pNone:703696.0-703726.0`

## 9. Ajuste de intervalos e priorização
Os materiais consultados indicam que a seleção da técnica e do intervalo não deve ser arbitrária. A decisão pode incorporar:
- análise dos **modos de falha e partes afetadas**;
- criticidade do equipamento;
- **taxa de falha** e histórico operacional, quando disponíveis;
- impacto da intervenção na disponibilidade;
- capacidade de a operação executar verificações sistemáticas;
- suporte de equipes especializadas onshore em operações integradas.

Uma contribuição importante do material offshore consultado é a ideia de que a priorização de manutenção baseada em condição, com verificações de campo e suporte analítico remoto, pode **reduzir intervenções preventivas excessivas** e melhorar a disponibilidade do sistema.

Também é destacado que uma boa análise depende de **estruturação hierárquica adequada dos equipamentos e instalações**, porque isso melhora:
- o planejamento das intervenções;
- o agrupamento funcional de itens manuteníveis;
- os estudos de confiabilidade;
- a gestão de sobressalentes e materiais.

Assim, a priorização de tarefas deve ser entendida como resultado de uma combinação entre:
1. função do item;
2. modo de falha;
3. consequência;
4. criticidade;
5. detectabilidade;
6. possibilidade de intervenção eficaz;
7. impacto da própria manutenção na indisponibilidade do sistema.

**Fontes da seção:** `regis-74dd376119cbb653fe9922bc:pNone:33090.0-33377.0`, `petroles-4ee4bce16acf674505c8912d:pNone:2396191.0-2396238.0`

## 10. Regras práticas para converter análise de falhas em lista de tarefas
Uma forma disciplinada de sair da FMEA/FMECA e chegar ao plano de manutenção é organizar cada item funcional com a seguinte cadeia lógica:

1. **Função requerida** do sistema/subsistema.
2. **Falha funcional** associada à perda dessa função.
3. **Modo de falha** e causa provável.
4. **Efeito observável** e impacto no sistema.
5. **Consequência** classificada por criticidade.
6. **Controles atuais** e capacidade de detecção.
7. **Tarefa selecionada**, por exemplo:
   - inspeção sensorial/operacional;
   - monitoramento por condição;
   - teste funcional para falha oculta;
   - restauração planejada;
   - descarte/substituição planejada;
   - corretiva controlada;
   - recomendação de modificação de projeto.
8. **Critério de execução/intervenção**, compatível com o padrão de desempenho e com o método escolhido.
9. **Periodicidade ou frequência de verificação**, ajustada por histórico, detectabilidade e consequência.
10. **Revisão da estratégia**, caso o histórico mostre falha recorrente, baixa eficácia da tarefa ou necessidade de redesign.

Esse encadeamento evita dois erros frequentes:
- escolher tarefa pelo hábito, sem vínculo com o modo de falha;
- usar um ranking numérico isolado, sem analisar a natureza da consequência.

**Fontes da seção:** `petroles-4ee4bce16acf674505c8912d:pNone:2395857.0-2395908.0`, `petroles-4ee4bce16acf674505c8912d:pNone:2396191.0-2396238.0`, `regis-63a2aa91eb522ba1c06754d8:pNone:3418.0-3740.0`, `regis-74dd376119cbb653fe9922bc:pNone:33090.0-33377.0`

## 11. Síntese executiva
Para selecionar corretamente estratégias e tarefas de manutenção em um FPSO/FSO a partir de modos de falha e consequências, o raciocínio técnico essencial é:
- começar pela **função** e não pela tarefa pronta;
- descrever a **falha funcional**, o **modo de falha**, a **causa**, o **efeito** e a **consequência**;
- usar **FMEA/FMECA** para estruturar e priorizar a análise;
- distinguir entre falhas **ocultas**, de **segurança/meio ambiente**, **operacionais** e **não operacionais**;
- aplicar tarefas proativas apenas quando forem **tecnicamente aplicáveis e eficazes**;
- priorizar **manutenção baseada em condição** quando o modo de falha apresentar sinais detectáveis em tempo útil;
- exigir **testes funcionais** para redundâncias e reservas sujeitas a falhas ocultas;
- reconhecer que certos problemas exigem **modificação de projeto**, e não apenas mais manutenção.

**Fontes da seção:** `petroles-4ee4bce16acf674505c8912d:pNone:2395829.0-2395881.0`, `petroles-4ee4bce16acf674505c8912d:pNone:2395857.0-2395908.0`, `petroles-4ee4bce16acf674505c8912d:pNone:2396191.0-2396238.0`, `petroles-4ee4bce16acf674505c8912d:pNone:703696.0-703726.0`, `regis-63a2aa91eb522ba1c06754d8:pNone:3418.0-3740.0`, `regis-74dd376119cbb653fe9922bc:pNone:33090.0-33377.0`