# Aproximação e posicionamento do aliviador

## 1. Contexto operacional e arranjos de offloading
Offloading é a transferência de óleo cru do FPSO/FSO para um navio aliviador, frequentemente em arranjo **tandem** em águas profundas e ultraprofundas. Nessa configuração, manter a **posição relativa segura** entre a unidade de produção e o aliviador é condição central para evitar colisão, interrupção da transferência e eventos com potencial de incêndio e poluição.

Do ponto de vista do aliviador, a literatura utilizada descreve cinco etapas principais da operação: **aproximação, conexão, transferência, desconexão e afastamento**. Para a faceta desta rodada, o foco recai sobre a transição segura entre a chegada à área, o estabelecimento da posição operacional, a permanência em tandem e a saída controlada.

Há diferenças relevantes entre arranjos de ancoragem da unidade de produção:

- **FPSOs spread moored (aproamento fixo)** não se alinham automaticamente às condições ambientais. Isso torna a geometria relativa mais restritiva e eleva a criticidade da perda de posição do aliviador.
- Em material associado a prática da Petrobras, a operação de offloading com **navios convencionais** em FPSOs spread moored foi considerada de risco não tolerável, porque uma mudança súbita do tempo poderia não deixar tempo suficiente para desconectar mangueiras e evitar colisão; por isso, nesse contexto, passou-se a operar com **DP Shuttle Tankers (DPSTs)**.
- **Unidades single point moored / turret** são associadas a aproamento variável e, no glossário disponível, apresentam **uma estação de offloading**; já unidades **spread moored** apresentam **duas estações de offloading**, usualmente uma na proa e outra na popa.
- A noção de **estação preferencial** é importante: é a estação em que as condições ambientais tendem a empurrar o navio aliviador **para longe** do F(P)SO, reduzindo o risco de aproximação indesejada.

Em terminais de aproamento fixo, o uso de duas estações de offloading aumenta a flexibilidade operacional; a indisponibilidade de uma estação, especialmente a de proa em cenários analisados, tende a aumentar o downtime operacional.

**Fontes:** `regis-a895130239a6e9ec62837349:pNone:8812.0-9019.0`, `regis-e8017584b2db5d2b9e42246a:pNone:1317.0-1500.0`, `regis-e8017584b2db5d2b9e42246a:pNone:7251.0-7431.0`, `petroles-004c2afadba7ea17c7dd7908:pNone:3026709.60-3026769.0`

## 2. Meios de manutenção de posição e implicações para a manobra
O posicionamento relativo do aliviador pode ser mantido de duas formas principais:

1. **Navio convencional com apoio de rebocadores**, operando basicamente com motor principal e ação externa de tração para manter a posição relativa ao FPSO.
2. **Navio com sistema de posicionamento dinâmico (DP)**, que usa propulsores controlados por computador com base em sensores de posição e movimento.

O sistema DP é descrito como composto por quatro subsistemas:

- **potência/geração e distribuição**;
- **controle**;
- **propulsão**;
- **sensoriamento/referência de posição**.

Nas fontes utilizadas, o DP é associado a maior segurança e rapidez na aproximação e amarração. Isso é particularmente relevante porque o FPSO concentra hidrocarbonetos e gás; portanto, uma colisão entre o aliviador e a unidade de produção pode ter consequências graves.

As classes de DP diferenciam a tolerância a falhas:

- **Classe 1**: admite perda de posição por falha simples;
- **Classe 2**: não admite perda de posição por falha simples de componente/sistema;
- **Classe 3**: amplia a robustez para cenários incluindo perda de compartimento por incêndio ou alagamento.

Para operações de aproximação e permanência, isso importa porque a filosofia de redundância define quanto o navio pode degradar sem perder a capacidade segura de station keeping.

As fontes também indicam que as falhas mais associadas a perda de posição em navios petroleiros com DP concentram-se em:

- **sensores/referências de posição**;
- **thrusters/propulsores**;
- **sistema de comando do DP**;
- **erro humano**.

Assim, a segurança da manobra não depende apenas da potência instalada, mas da **confiabilidade integrada** dos sensores, do controle, da geração elétrica e da atuação humana.

**Fontes:** `regis-a895130239a6e9ec62837349:pNone:8812.0-9019.0`, `regis-a895130239a6e9ec62837349:pNone:8900.0-9280.0`, `regis-e8017584b2db5d2b9e42246a:pNone:1317.0-1500.0`

## 3. Planejamento pré-aproximação
Antes de o aliviador entrar na área de operação, os elementos decisórios mais importantes, com base no material fornecido, são:

### 3.1 Seleção da estação de offloading
A escolha entre estação de proa ou popa, quando houver duas estações, deve considerar:

- aproamento fixo ou variável da unidade;
- direção e intensidade esperadas de **vento, ondas e corrente**;
- lado dos **risers/linhas de produção** e restrições setoriais;
- capacidade do aliviador de manter posição dentro dos limites operacionais.

O conceito de **estação preferencial** busca garantir que os agentes ambientais afastem o aliviador da unidade, e não o contrário.

### 3.2 Avaliação meteorológica e oceanográfica
Mudança das condições ambientais é tratada nas fontes como um **evento crítico** da operação de offloading. Pode decorrer de:

- erro de previsão meteorológica;
- mudança inesperada de vento e ondas.

Por isso, recomenda-se verificação detalhada da previsão do tempo **antes de o aliviador adentrar a área operacional**. Em instalações de aproamento fixo, essa análise é ainda mais sensível, porque a unidade não se realinha livremente ao ambiente.

### 3.3 Estado de degradação e capacidade de manobra do DP
O posicionamento ótimo do aliviador não depende apenas do alvo geométrico; depende também de:

- potência disponível;
- estado de degradação do DP;
- capacidade dos propulsores;
- direção resultante das forças ambientais.

As fontes destacam que conhecer os estados de degradação e a capacidade de manobra é vital para definir a melhor orientação do aliviador frente a vento, ondas e corrente.

### 3.4 Uso de rebocador de apoio
Em certas condições, especialmente fora do envelope mais favorável, pode ser necessário programar **rebocador dedicado** para apoio ao navio aliviador com DP. A decisão deve considerar magnitude e direção dos agentes ambientais. O material também registra uma orientação prática relevante: **não empregar dois rebocadores simultaneamente** no apoio ao aliviador; se a condição ambiental exigir suporte dessa ordem, a indicação é **suspender temporariamente a operação** até melhora das condições.

**Fontes:** `regis-a895130239a6e9ec62837349:pNone:10144.0-10384.0`, `regis-e8017584b2db5d2b9e42246a:pNone:7251.0-7431.0`, `petroles-004c2afadba7ea17c7dd7908:pNone:3026150.0-3026183.0`

## 4. Aproximação do aliviador
A aproximação é a fase em que o risco de colisão cresce rapidamente se houver falha de propulsão, sensoriamento, julgamento ou mudança ambiental.

### 4.1 Marco de início da fase
As fontes convergem em tratar a aproximação a partir de cerca de **1500 m** do FPSO. Nesse ponto, o aliviador passa ao regime de controle mais estrito da manobra, com forte participação do DP no caso de navios DP.

### 4.2 Velocidade e rumo de aproximação
Há divergência entre as fontes quanto à velocidade característica nesse trecho:

- uma fonte menciona aproximação a 1500 m com **velocidade máxima de 1,5 nós**;
- outra registra que, ao ligar o DP por volta de 1500 m, a velocidade é reduzida progressivamente de cerca de **3 nós** até parada completa.

Mais importante que o valor absoluto é o princípio operacional comum: a aproximação deve ocorrer com **redução progressiva e controlada da velocidade**, compatível com o envelope da instalação e do navio específico.

Outro critério explícito é que o aliviador deve se aproximar **na direção oposta à resultante das forças ambientais**, para minimizar o risco de colisão com o FPSO em caso de blackout ou perda súbita de capacidade propulsiva.

### 4.3 Passagem do mensageiro e conexão inicial
Em um cenário de DP shuttle tanker com **Bow Loading System (BLS)**:

- quando o navio está a cerca de **80 m** do FPSO, a **mensageira** pode ser passada da plataforma para o aliviador com auxílio de pistola de ar;
- o aliviador recolhe a mensageira do **hawser** e da **linha de mangotes**, efetuando a conexão ao **chain stopper** e ao **BLS**, respectivamente.

Esse arranjo reduz a exposição direta de pessoal ao manuseio da linha de mangotes, melhorando a segurança ocupacional.

### 4.4 Duração e estabilização pós-conexão
Uma das fontes informa que a fase de conexão pode durar cerca de **6 horas**. Após a conexão, o aliviador reposiciona-se para continuar a operação a uma distância da ordem de **120 a 155 m** do FPSO, antes do teste de estanqueidade e da transferência efetiva de carga.

Esses valores devem ser entendidos como **referências de casos descritos**, não como parâmetros universais.

**Fontes:** `regis-a895130239a6e9ec62837349:pNone:8900.0-9280.0`, `regis-e8017584b2db5d2b9e42246a:pNone:1317.0-1500.0`, `regis-e8017584b2db5d2b9e42246a:pNone:7251.0-7431.0`

## 5. Posicionamento e permanência em tandem
Depois da amarração, o aliviador permanece submetido à ação combinada de vento, corrente e ondas. Como consequência, ele pode se mover dentro do **raio de amarração**, exigindo monitoramento contínuo da posição relativa e da orientação.

### 5.1 Setores operacionais
O material consultado descreve três setores operacionais para o aliviador em relação ao FPSO:

- **setor verde**: operação normal; o aliviador pode mover-se livremente dentro do envelope admitido;
- **setor amarelo**: condição degradada temporária; a embarcação pode permanecer somente o tempo necessário para tentar retornar ao setor verde;
- **setor vermelho**: permanência não permitida.

Uma fonte brasileira cita, para operação normal, limites de **45/60 graus de aproamento relativo da linha de centro**. Já outras fontes descrevem setores assimétricos, especialmente em FPSOs de aproamento fixo com lado de risers mais restritivo. Portanto, o valor angular exato é **instalação-específico**.

### 5.2 Relação entre setor e bombeio
Um ponto operacional importante é que, em alguns procedimentos descritos para NADPs em FPSOs de aproamento fixo, se o navio ultrapassa os limites e entra no **setor amarelo**, o **bombeio deve ser interrompido** até retorno integral à condição normal, mesmo que parte da geometria ainda pareça aceitável.

A sequência de resposta descrita é:

1. atingir limiar do amarelo → **contatar o FPSO** e solicitar interrupção imediata do bombeio;
2. iniciar **OESD1** (primeiro estágio de parada de emergência do descarregamento);
3. se a perda de posição piorar → preparar e executar **OESD2**, com desconexão de emergência no BLS e desconexão do sistema de amarração;
4. ao atingir setor vermelho → **OESD2 imediato**.

### 5.3 Conflito entre menor demanda de potência e setor seguro
As fontes ressaltam uma contradição relevante em FPSOs de aproamento fixo: a posição/orientação do aliviador que **minimiza a potência demandada pelo DP** pode colocá-lo **fora dos limites do setor operacional recomendado** para offloading.

Profissionalmente, isso significa que a decisão não pode ser baseada apenas em eficiência do DP. É necessário conciliar:

- capacidade de manutenção da posição;
- limites setoriais da instalação;
- geometria relativa ao lado dos risers;
- continuidade segura do bombeio;
- possibilidade de desconexão de emergência.

### 5.4 Influência da transferência de carga
As operações de alívio envolvem **grandes variações de calado** nas embarcações. Isso altera a resposta hidrodinâmica e pode mudar o agente ambiental predominante sobre o sistema, afetando a dinâmica relativa durante a permanência. Em outras palavras, a condição de station keeping não deve ser avaliada como fixa do início ao fim da operação; ela evolui com o carregamento do aliviador e com o estado da unidade de produção.

**Fontes:** `regis-a895130239a6e9ec62837349:pNone:10144.0-10384.0`, `petroles-004c2afadba7ea17c7dd7908:pNone:3026150.0-3026183.0`, `petroles-004c2afadba7ea17c7dd7908:pNone:2461046.0-2461107.0`

## 6. Desconexão segura e critérios de abortamento
A desconexão segura pode ser **planejada** ao término da transferência ou **emergencial** por degradação da condição operacional.

### 6.1 Situações que podem exigir abortamento
As fontes destacam como eventos críticos:

- **falha do motor de combustão auxiliar (MCA)**, com perda de alimentação elétrica de sistemas importantes e possível parada do MCP e dos sistemas de navegação/manobra;
- **falha do DP**, por problema na geração de energia, thrusters, navegação ou controle;
- **falha do motor de combustão principal (MCP)**;
- **mudança abrupta das condições ambientais**;
- **execução de manobras arriscadas**, seja por erro de programação do sistema automático, seja por julgamento inadequado sobre manobrabilidade.

### 6.2 Resposta operacional
As ações de contingência descritas são, em essência:

- **abortar a operação** quando a condição segura não puder ser mantida;
- executar o **afastamento do aliviador** por procedimento de emergência;
- em falha do DP, usar o **MCP** para afastamento, quando disponível;
- em problemas de posicionamento ou manobra, solicitar **auxílio de rebocador**;
- adotar manutenção preventiva rigorosa para reduzir frequência de falhas críticas.

### 6.3 Papel do BLS e do Emergency Release
O **BLS** contribui para a segurança porque automatiza a conexão da linha de mangotes ao manifold de proa e reduz o contato direto dos trabalhadores com o sistema. As fontes também apontam a existência de **quick release/emergency release**, importante para permitir desconexão rápida e reduzir o potencial de poluição em eventos indesejados.

### 6.4 Riscos humanos na desconexão
Na fase de desconexão/desamarração, erros humanos na liberação do **cabo mensageiro** do mangote e do sistema de amarração podem causar:

- queda de elementos ao mar;
- necessidade de embarcação de apoio para recolhimento;
- ferimentos por chicoteamento e tensionamento de cabos.

Isso reforça que a desconexão segura não é apenas uma função do equipamento: depende de coordenação, disciplina operacional e barreiras físicas adequadas.

**Fontes:** `regis-a895130239a6e9ec62837349:pNone:10144.0-10384.0`, `regis-e8017584b2db5d2b9e42246a:pNone:1317.0-1500.0`

## 7. Síntese prática para avaliação profissional
Na aproximação e posicionamento do aliviador, a decisão segura combina quatro eixos:

1. **Compatibilidade entre arranjo da unidade e tipo de aliviador**  
   FPSOs spread moored/fixed heading impõem maior restrição geométrica e maior dependência de capacidade de posicionamento ativa do aliviador.

2. **Controle da posição relativa dentro do setor permitido**  
   Não basta manter distância média adequada; é necessário permanecer no setor admissível e respeitar os gatilhos de interrupção do bombeio e de OESD.

3. **Preparação para falhas e piora ambiental**  
   Sensores, thrusters, geração de energia e erros humanos estão entre os principais gatilhos de perda de posição; o plano de contingência deve ser claro antes da aproximação.

4. **Critério conservador para continuidade**  
   Se a manutenção da posição exigir manobra excessivamente agressiva, potência incompatível, suporte externo além do previsto ou resultar em ingresso no setor amarelo/vermelho, a resposta correta tende a ser **suspender, abortar ou desconectar de forma controlada**, e não insistir no bombeio.

**Fontes:** `regis-a895130239a6e9ec62837349:pNone:8900.0-9280.0`, `regis-a895130239a6e9ec62837349:pNone:10144.0-10384.0`, `regis-e8017584b2db5d2b9e42246a:pNone:1317.0-1500.0`, `petroles-004c2afadba7ea17c7dd7908:pNone:3026150.0-3026183.0`