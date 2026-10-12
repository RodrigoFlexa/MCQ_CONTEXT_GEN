# Compatibilidade e autorização em SIMOPS com foco em janelas operacionais, prioridades e restrições compartilhadas

## 1. Delimitação técnica da faceta

Neste recorte, **compatibilidade** entre operações simultâneas pode ser tratada como a condição em que duas ou mais atividades só podem coexistir se o **estado combinado do sistema** permanecer dentro dos seus limites operacionais e de segurança. Para operações de poço, intervenções, gravel pack, perfuração com controle de pressão e sistemas de produção compartilhados, isso significa verificar se as atividades concorrentes preservam:

- a **janela operacional** do poço ou sistema;
- os limites de pressão dinâmica e estática;
- as restrições de vazão e de capacidade de superfície;
- os limites de monitoramento que disparam fechamento, suspensão ou replanejamento.

O material disponível sustenta principalmente uma abordagem de SIMOPS baseada em **restrições técnicas e janelas de execução**, e não um rito formal completo de governança organizacional. Assim, a autorização é tratada aqui como **autorização técnica condicionada**, baseada em limites verificáveis e critérios de continuidade/suspensão.  
**Fontes:** `regis-7a103ff344dd991b5bc1b3f2:pNone:45.0-113.0`, `petroles-690231.0-690276.0`, `regis-f224488b7af99163b6bcec73:pNone:0.0-33.0`

## 2. Janela operacional como critério primário de compatibilidade

### 2.1 Conceito

Os trechos sobre gravel pack, geopressões e MPD convergem para um critério central: a operação só é tecnicamente aceitável quando a **pressão de fundo** ou a **pressão dinâmica equivalente** permanece entre limites inferiores e superiores da janela operacional.

No material, a lógica é descrita assim:

- a pressão dinâmica deve ser **maior que a pressão de poros** para evitar influxo;
- a pressão dinâmica deve ser **menor que a pressão de fratura** para evitar perda para a formação e danos operacionais;
- também devem ser considerados limites associados à **estabilidade do poço**, incluindo colapso inferior e superior;
- em águas profundas e ultraprofundas, a janela tende a ser **mais estreita**, elevando a sensibilidade a pequenas perturbações.

Em termos de SIMOPS, a consequência prática é que a compatibilidade entre atividades não depende apenas de elas serem “permitidas” isoladamente, mas de o **efeito cumulativo** manter o sistema dentro da janela disponível. Se uma atividade consome margem hidráulica, de pressão ou de controle, ela reduz a compatibilidade das demais.

### 2.2 Implicações para autorização

Uma atividade só deve ser tecnicamente autorizada em simultâneo quando houver demonstração de que:

1. o caso-base já opera dentro da janela;
2. a atividade adicional não desloca o sistema para baixo do limite inferior nem acima do superior;
3. os **transientes** de partida, parada, retomada de circulação e perturbações previsíveis também permanecem dentro da janela;
4. o monitoramento em tempo real consegue detectar aproximação dos limites com antecedência útil.

Em outras palavras, a compatibilidade é uma propriedade do **conjunto de condições vigentes**, não apenas da natureza da tarefa.  
**Fontes:** `regis-7a103ff344dd991b5bc1b3f2:pNone:45.0-113.0`, `petroles-690231.0-690276.0`, `regis-12e0c7d952864d9e70c29a29:pNone:358.60-430.0`

## 3. Compatibilidade dinâmica: por que a fase da operação importa

Os textos de gravel pack mostram que a avaliação de compatibilidade deve ser feita **por fase operacional**, e não apenas por atividade genérica. O modelo citado separa, por exemplo:

- etapa de injeção da mistura;
- propagação da onda alfa;
- propagação da onda beta;
- perdas de carga na coluna e no poço aberto;
- pressão hidrostática na coluna.

Isso é relevante para SIMOPS porque uma mesma operação pode ter fases com severidades distintas. A coexistência com outras tarefas pode ser aceitável em uma fase e inaceitável em outra.

### 3.1 Exemplo técnico de incompatibilidade por fase

No deslocamento de gravel, o material destaca o risco de **embuchamento prematuro no rat hole** e de **screen-out**, com elevação instantânea de pressão na sapata. A própria operação pode precisar ser abortada quando a vazão praticada cai abaixo do mínimo necessário para evitar esse mecanismo ou sobe a ponto de ameaçar fraturar a formação.

Convertendo esse raciocínio para SIMOPS:

- fases de maior sensibilidade hidráulica devem ter **janela exclusiva** ou menor carga de interferências externas;
- atividades simultâneas que alterem retorno, contrapressão, densidade, regime de vazão ou capacidade de resposta do sistema tendem a ser **menos compatíveis** com fases críticas;
- a autorização deve ser faseada, com permissões condicionadas à passagem segura entre etapas.

### 3.2 Consequência para sequenciamento

Não basta decidir “executar duas atividades juntas”. É preciso definir:

- **em que fase** a simultaneidade é tolerável;
- em que fase ela deve ser proibida;
- quais variáveis precisam estar estabilizadas antes da próxima etapa.

Isso favorece uma matriz de compatibilidade do tipo:

- compatível sem restrição;
- compatível com condicionantes;
- compatível apenas fora de fase crítica;
- incompatível.

**Fontes:** `regis-7a103ff344dd991b5bc1b3f2:pNone:45.0-113.0`, `regis-7a103ff344dd991b5bc1b3f2:pNone:113.60-151.0`

## 4. Critérios técnicos para definir janelas de execução

Os textos permitem identificar uma lógica robusta para construção de **janelas de execução** em operações simultâneas sensíveis a pressão e hidráulica.

### 4.1 Limites mínimo e máximo

No caso de gravel pack, a janela operacional de vazão é delimitada por:

- **limite mínimo**: menor vazão que evita embuchamento prematuro no rat hole;
- **limite máximo**: maior vazão que não leva à fratura da formação.

A ideia geral aplicável à SIMOPS é que a janela de execução deve ser definida por **restrições concorrentes**, e não por um único parâmetro. Em atividades simultâneas, o limite efetivo é o mais restritivo entre:

- integridade do poço;
- capacidade hidráulica;
- tolerância a picos transitórios;
- disponibilidade de controle e monitoramento;
- capacidade de resposta a desvios.

### 4.2 Janelas estreitas exigem menor simultaneidade

Quando a margem entre limite inferior e superior é pequena, a tolerância a perturbações diminui. Os textos associam isso especialmente a ambientes de águas profundas e ultraprofundas. Para SIMOPS, a conclusão prática é:

- quanto mais estreita a janela, **menor deve ser o número de interferências simultâneas aceitáveis**;
- atividades que adicionam incerteza ou dispersão nas variáveis de processo devem ser removidas ou reprogramadas;
- a autorização deve ser mais conservadora em cenários de alta sensibilidade.

### 4.3 Transientes devem entrar na janela, não só o regime permanente

Os experimentos de controle de pressão e os estudos de gelificação mostram que o problema não está apenas no valor em regime, mas nos **picos transitórios**. Na retomada da circulação após período de estática, a quebra do gel pode gerar pico de ECD/pressão de fundo suficiente para alcançar a pressão de fratura.

Portanto, a janela de execução para SIMOPS precisa incorporar:

- partida e parada;
- retomada após espera;
- mudança de set point;
- variação de densidade, vazão ou retorno;
- perturbações previsíveis do processo.

Uma autorização baseada só em valores médios ou estáveis é insuficiente.  
**Fontes:** `regis-7a103ff344dd991b5bc1b3f2:pNone:45.0-113.0`, `regis-f224488b7af99163b6bcec73:pNone:0.0-33.0`, `regis-12e0c7d952864d9e70c29a29:pNone:358.60-430.0`

## 5. Sequenciamento e escolha entre alternativas operacionais

Os textos sobre ampliação da janela operacional são úteis para construir um critério de **sequenciamento por risco residual**.

### 5.1 Alternativas que ampliam a janela

O material cita, entre outras, as seguintes estratégias:

- operar com o **BOP aberto**, quando possível do ponto de vista da segurança de poço, reduzindo perdas de carga no retorno pelo riser;
- **reduzir o peso do fluido**, com cuidado para não perder overbalance e gerar kick;
- usar ferramentas de **menor perda de carga**;
- usar **redutores de arraste**;
- usar **propantes leves**;
- considerar soluções adicionais como by-pass no rat hole.

### 5.2 Hierarquia técnica implícita

As conclusões do estudo diferenciam alternativas com **baixo nível de risco associado** daquelas com risco mais elevado ou que exigem maior maturidade técnica. O texto trata como alternativas de menor risco relativo, no contexto estudado:

- operar com BOP aberto;
- usar propantes leves;
- usar ferramentas que geram baixas perdas de carga;
- usar redutores de fricção/arraste.

Já a **redução do peso do fluido** e soluções ainda em desenvolvimento são tratadas com maior cautela, por poderem elevar o risco de segurança de poço.

### 5.3 Aplicação à lógica de SIMOPS

Para fins de compatibilidade e autorização, isso sustenta um princípio de decisão:

1. primeiro, buscar medidas que **ampliem a janela** sem degradar significativamente as barreiras;
2. depois, avaliar se ainda é necessário manter atividades simultâneas em fases críticas;
3. reservar alternativas de maior risco ou menor maturidade para situações em que opções mais seguras não sejam suficientes.

Assim, o sequenciamento de SIMOPS deve preferir combinações que preservem margem operacional e evitar simultaneidade justamente quando a janela depende de medidas mais frágeis ou sensíveis.  
**Fontes:** `regis-7a103ff344dd991b5bc1b3f2:pNone:113.60-151.0`, `regis-7a103ff344dd991b5bc1b3f2:pNone:190.0-218.0`

## 6. Priorização sob restrições compartilhadas

Há um trecho sobre alocação de vazões em sistemas de produção compartilhados que, embora não trate diretamente de SIMOPS, traz uma contribuição metodológica útil: quando existe uma restrição global, pode-se optar por:

- distribuir a capacidade de forma uniforme entre todos os elementos; ou
- usar um **ranking de prioridades** e abrir/atender os elementos na ordem de prioridade até atingir a restrição.

O texto distingue uma abordagem simples, em que todos os poços produzem a mesma fração de suas vazões máximas, de uma abordagem `PRIOR`, em que existe um **ranking explícito**, e de uma abordagem `INGUIDE`, em que a repartição é guiada por pesos de prioridade, sem eliminar totalmente os de menor prioridade.

### 6.1 Tradução metodológica para SIMOPS

Para autorização de atividades simultâneas em FPSO/sistemas subsea, isso sugere que a priorização não deve ser implícita nem ad hoc. Uma matriz de decisão pode distinguir, por exemplo:

- atividades mandatórias para segurança/integridade;
- atividades críticas para continuidade operacional;
- atividades recuperáveis/postergáveis;
- atividades complementares.

Em caso de restrição compartilhada de capacidade, janela operacional ou supervisão, a autorização simultânea tende a ser mais robusta quando existe:

- um **critério de ranking** previamente definido;
- uma regra de desempate;
- um critério claro para escolher qual atividade é mantida, limitada, sequenciada ou suspensa.

### 6.2 Ganho prático

Essa abordagem evita duas falhas comuns:

- tratar todas as atividades como equivalentes, mesmo quando o risco e o valor operacional são diferentes;
- improvisar prioridades no momento do conflito, sem base formal.

No contexto de SIMOPS, a principal utilidade desse material é reforçar que a priorização deve ser **explícita, parametrizada e rastreável**.  
**Fontes:** `petroles-4ee4bce16acf674505c8912d:pNone:1253907.0-1253951.0`

## 7. Restrições operacionais e de monitoramento como gatilhos de autorização/suspensão

Outro trecho útil descreve que poços produtores podem operar sujeitos a restrições de superfície e de monitoramento, incluindo:

- vazão máxima de óleo;
- vazão máxima de líquido;
- pressão mínima de fundo (BHP);
- razão gás-óleo máxima (RGO);
- corte de água máximo (WCUT).

Quando certos limites são atingidos, o poço é fechado por alta RGO ou alto WCUT.

### 7.1 Aplicação à autorização de SIMOPS

Isso permite estruturar a autorização de operações simultâneas em três camadas:

1. **pré-condições de autorização**: limites devem estar dentro do envelope antes do início;
2. **condições de continuidade**: variáveis devem permanecer dentro das faixas aprovadas;
3. **gatilhos de suspensão/cancelamento**: ao atingir limite de monitoramento, a atividade é interrompida ou revertida.

### 7.2 Implicação para compatibilidade

Duas atividades podem parecer compatíveis em projeto, mas tornar-se incompatíveis se a combinação delas empurra o sistema para perto de:

- BHP mínimo;
- restrição máxima de vazão;
- limites de qualidade/monitoramento que levem a fechamento automático ou operacional.

Logo, a matriz de compatibilidade deve incluir não só conflitos espaciais ou energéticos, mas também **conflitos por consumo de margem operacional e de capacidade de superfície**.  
**Fontes:** `petroles-004c2afadba7ea17c7dd7908:pNone:2056745.0-2056797.0`

## 8. Autoridade técnica para aprovar, suspender ou cancelar

Os textos não nomeiam a autoridade organizacional de SIMOPS, mas permitem definir o que essa autoridade precisa assegurar tecnicamente.

### 8.1 Requisitos mínimos da autoridade de aprovação

A aprovação técnica de atividades simultâneas sensíveis deve recair sobre quem possa verificar, de forma integrada:

- a janela operacional aplicável;
- as fases críticas da operação;
- as restrições compartilhadas de processo e superfície;
- os efeitos transitórios previsíveis;
- a disponibilidade de monitoramento e de capacidade de intervenção;
- os gatilhos objetivos de suspensão.

### 8.2 Critério de suspensão ou cancelamento

Pelos materiais, a suspensão/cancelamento é tecnicamente justificável quando ocorre qualquer uma destas situações:

- aproximação ou violação do limite inferior/superior da janela operacional;
- ocorrência de mecanismo de falha conhecido, como embuchamento/screen-out;
- pico transitório de pressão na retomada de circulação capaz de atingir o gradiente de fratura;
- necessidade de recorrer a alternativa de maior risco sem reanálise prévia;
- atingimento de restrições de monitoramento que exijam fechamento ou limitação.

### 8.3 Retomada

A retomada segura pressupõe, no mínimo:

- confirmação de retorno ao envelope operacional;
- reavaliação das causas do desvio;
- revisão do sequenciamento e das restrições, se necessário;
- verificação de que o transiente de recomeço é aceitável, principalmente após período de estática.

**Fontes:** `regis-f224488b7af99163b6bcec73:pNone:0.0-33.0`, `regis-12e0c7d952864d9e70c29a29:pNone:358.60-430.0`, `regis-7a103ff344dd991b5bc1b3f2:pNone:45.0-113.0`

## 9. Síntese aplicável à matriz de compatibilidade e autorização

Com base nos materiais, uma matriz técnica de compatibilidade para SIMOPS envolvendo produção, poços e operações submarinas sensíveis deveria, no mínimo, testar:

1. **Envelope de pressão**  
   - permanece acima da pressão de poros/limites de estabilidade?  
   - permanece abaixo da pressão de fratura?

2. **Envelope hidráulico**  
   - a vazão mínima evita mecanismos de falha como screen-out/embuchamento?  
   - a vazão máxima permanece abaixo do limite de fratura?

3. **Transientes operacionais**  
   - partida, parada e retomada após estática foram avaliadas?  
   - picos de pressão cabem na janela?

4. **Capacidade compartilhada**  
   - há restrição de superfície, vazão, retorno, controle ou monitoramento?  
   - a combinação das atividades consome margem excessiva?

5. **Prioridade e sequenciamento**  
   - existe ranking explícito de prioridade?  
   - a fase crítica foi isolada ou protegida?

6. **Gatilhos de suspensão**  
   - os limites que exigem parar estão claros e monitoráveis?  
   - há critério de retomada definido?

Essa abordagem é compatível com uma autorização de SIMOPS baseada em **margem operacional disponível**, **priorização formal** e **continuidade condicionada ao monitoramento**.  
**Fontes:** `regis-7a103ff344dd991b5bc1b3f2:pNone:45.0-113.0`, `regis-7a103ff344dd991b5bc1b3f2:pNone:113.60-151.0`, `regis-7a103ff344dd991b5bc1b3f2:pNone:190.0-218.0`, `regis-f224488b7af99163b6bcec73:pNone:0.0-33.0`, `regis-12e0c7d952864d9e70c29a29:pNone:358.60-430.0`, `petroles-4ee4bce16acf674505c8912d:pNone:1253907.0-1253951.0`, `petroles-004c2afadba7ea17c7dd7908:pNone:2056745.0-2056797.0`

## 10. Conclusão técnica

Para esta faceta, o principal ensinamento extraível do material é que a compatibilidade em SIMOPS não deve ser tratada como mera coexistência administrativa de tarefas. Ela deve ser demonstrada pela permanência do sistema dentro de uma **janela operacional dinâmica**, sujeita a restrições hidráulicas, de pressão, de monitoramento e de capacidade compartilhada.

A autorização técnica, por sua vez, é mais robusta quando:

- as janelas de execução são definidas por fase;
- os conflitos são avaliados pelo consumo de margem operacional;
- a priorização entre atividades é explícita e rastreável;
- existem gatilhos objetivos para suspender, cancelar e retomar.

Esse conjunto é particularmente relevante para SIMOPS que envolvam poços, intervenções, gravel pack, perfuração/MPD e sistemas de produção com restrições compartilhadas em FPSOs e arranjos subsea.  
**Fontes:** `regis-7a103ff344dd991b5bc1b3f2:pNone:190.0-218.0`, `regis-f224488b7af99163b6bcec73:pNone:0.0-33.0`, `regis-12e0c7d952864d9e70c29a29:pNone:358.60-430.0`