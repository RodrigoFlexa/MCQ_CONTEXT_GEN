# Barreiras e resposta a falhas em poços submarinos associados a FPSO

## 1. Escopo técnico desta faceta
Este documento consolida, de forma **conceitual e aplicada**, os fundamentos de **integridade de poço**, **isolamento**, **fechamento de emergência**, **avaliação de vazamentos**, **independência de barreiras** e **resposta a falhas** em poços submarinos com ANM, considerando principalmente a fase de produção/injeção. O material disponível concentra-se em **poço completado, SCPS, BAP, TH, ANM, DSSS e lógica de barreiras**; portanto, PLEM, PLET e manifolds aparecem apenas de forma indireta, pelas interfaces subsea e pela filosofia geral de isolamento e integridade.  
**Fontes:** `petroles-4ee4bce16acf674505c8912d:pNone:1221735.0-1221774.0`, `petroles-4ee4bce16acf674505c8912d:pNone:1222071.0-1222114.0`

## 2. Segurança operacional, integridade de poço e severidade do evento topo
Na engenharia de poços, **segurança operacional** pode ser entendida como o estado em que os riscos para pessoas, instalações, sociedade e meio ambiente são reduzidos e mantidos em nível aceitável. Em operações de poço, é comum o uso do critério de **duas barreiras de segurança independentes** como referência de segurança.

Já **integridade de poço** é a capacidade do sistema de manter controlado o fluxo de fluidos desde o reservatório até a planta de processamento, **prevenindo vazamentos para o meio ambiente**. Em termos práticos, isso exige bloquear todos os caminhos possíveis entre o fluxo do poço e o exterior por meio de barreiras de segurança técnicas, operacionais e organizacionais.

Para completações submarinas, o evento indesejado de maior severidade é o **vazamento descontrolado de hidrocarbonetos**, ou **blowout/erupção**. Nos trechos fornecidos, esse conceito inclui o caso em que, **mesmo após o acionamento das barreiras previamente instaladas, o vazamento continua**. Em poços submarinos, a interpretação adotada foi a de vazamento descontrolado **para o meio externo ao poço**, isto é, tipicamente para o **fundo do mar**. O material também diferencia esse cenário de uma **liberação limitada de hidrocarbonetos (well release)**, em que há vazamento apenas até que uma barreira previamente instalada atue e interrompa o fluxo.

Essa distinção é importante para a resposta operacional: **persistência do fluxo após a demanda das barreiras** caracteriza perda grave de controle; **cessação do fluxo por atuação de barreira pré-instalada** indica evento limitado, ainda crítico, porém de outra categoria funcional.

Em árvores de natal molhadas, os riscos tendem a ser mais fortemente dominados pelo **impacto ambiental**, em razão da distância típica entre os equipamentos submarinos e as pessoas, embora a complexidade de manutenção e controle aumente os requisitos de confiabilidade do sistema.  
**Fontes:** `petroles-004c2afadba7ea17c7dd7908:pNone:2972401.0-2972440.0`, `petroles-4ee4bce16acf674505c8912d:pNone:1221735.0-1221774.0`

## 3. Arquitetura do sistema poço submarino relevante para barreiras
O poço submarino pode ser visto como um sistema composto, ao menos, por três grandes subconjuntos:

1. **Equipamentos estruturais**, como o **SCPS** e os revestimentos.  
2. **Equipamentos de controle de produção/injeção**, como **BAP**, **ANM** e **tree cap**.  
3. **Coluna de completação**, com elementos como tubos de produção, packer, DSSS e acessórios.

### 3.1 Equipamentos estruturais
O **SCPS** realiza a interface entre os revestimentos e os equipamentos de controle da produção/injeção. Falhas críticas nesses elementos estruturais podem levar à **perda do poço**, porque se trata de equipamentos permanentes.

### 3.2 Equipamentos de controle de produção/injeção
Nos sistemas citados como comuns em campos submarinos brasileiros, a configuração inclui **BAP**, **ANM vertical** e **capa da árvore**. A **BAP** faz a interface entre o SCPS, a coluna de completação, a ANM e as linhas de superfície/submarinas. Também é o ponto de passagem de sinais **eletro-hidráulicos** de monitoração e de controle, além do acesso ao anular.

### 3.3 Coluna de completação e equipamentos de segurança
Na completação exemplar mencionada no material, aparecem elementos como:
- tubos de produção;
- mandril de injeção química;
- mandril de gas lift;
- mandril de PDG;
- válvulas de completação inteligente;
- **packer**;
- **DSSS**;
- **tubing hanger (TH)**;
- ANM e seus componentes submarinos associados.

Essa arquitetura é relevante porque a integridade do poço não depende de um único componente, e sim da **continuidade funcional do envelope de contenção** ao longo das interfaces mecânicas, hidráulicas e de controle.  
**Fontes:** `petroles-4ee4bce16acf674505c8912d:pNone:1221735.0-1221774.0`, `petroles-4ee4bce16acf674505c8912d:pNone:1222049.0-1222091.0`, `petroles-4ee4bce16acf674505c8912d:pNone:1222071.0-1222114.0`

## 4. Conceito de barreira: elemento isolado versus envelope contínuo
Os trechos fornecidos mostram duas leituras conceituais importantes:

### 4.1 Leitura regulatória brasileira (barreira como separação física)
A formulação atribuída à ANP trata **barreira** como uma **separação física** apta a conter ou isolar fluidos entre intervalos permeáveis. Essa barreira pode ser líquida, sólida consolidada ou sólida mecânica.

### 4.2 Leitura NORSOK (barreira de poço como envelope de elementos)
Na formulação associada à **NORSOK D-010**, a **barreira de poço** é um **envelope** formado por um ou mais elementos de barreira dependentes entre si, cuja função conjunta é impedir fluxo não intencional desde a formação para outra formação ou para a superfície.

### 4.3 Consequência prática da diferença conceitual
A diferença não é apenas terminológica. Se a análise tratar cada equipamento isoladamente, pode-se perder de vista a necessidade de **continuidade da contenção** ao longo de todo o caminho de vazamento. Por isso, o material destaca a utilidade de enxergar a integridade do poço como um **invólucro contínuo** envolvendo o reservatório e os caminhos potenciais de migração de fluido.

Na fase de produção, o exemplo baseado na NORSOK descreve, para um cenário produtor, uma **barreira primária** composta por elementos como **packer de produção, coluna de produção e DSSS**, e uma **barreira secundária** composta por **cimentação do revestimento, revestimento, cabeça do poço, suspensor de coluna, linha de acesso ao anular com válvulas e árvore de natal**.

Essa forma de representação é particularmente útil quando o objetivo é avaliar **falhas de barreiras**, **isolamento** e **resposta a vazamentos**.  
**Fontes:** `petroles-4ee4bce16acf674505c8912d:pNone:1221936.0-1221985.0`, `regis-a8155330e2120dca899050ba:pNone:3217.0-3531.0`

## 5. Caminhos de vazamento, cavidades pressurizáveis e risco de sobrepressão local
Um dos pontos centrais para avaliar perda de integridade é identificar os **caminhos possíveis entre o reservatório e o meio ambiente**. O material resume quatro caminhos principais:
- **coluna**;
- **poço** (incluindo o anular entre coluna e último revestimento);
- **anular externo**;
- **rocha**.

### 5.1 Caminhos de vazamento
- **Coluna:** todo caminho pelo interior de uma coluna instalada no poço.
- **Poço:** interior do último revestimento assentado e cimentado; se houver coluna, inclui o anular entre essa coluna e o revestimento.
- **Anular externo:** espaço anular externo ao último revestimento assentado e cimentado.
- **Rocha:** caminho pela formação geológica entre reservatório e meio ambiente.

O documento-fonte chama atenção para um limite importante da prática simplificada de exigir “duas barreiras por caminho”: isso pode ser insuficiente se houver **atalhos** ou **comunicação entre caminhos**. Em outras palavras, um vazamento por conexão de tubos, por um stab de produção da ANM ou por outro ponto de interligação pode **contornar barreiras aparentemente suficientes** quando a análise não considera o poço como sistema integrado.

### 5.2 Cavidades onde a pressão pode ficar trapeada
A metodologia citada também exige mapear as **cavidades do poço onde a pressão pode ser trapeada** entre reservatório e meio ambiente. Qualquer espaço em que uma falha ou vazamento de um ou mais equipamentos possa causar **acúmulo de pressão** deve ser considerado.

Esse mapeamento é essencial para entender:
- onde pode surgir **sobrepressão local** após falha de contenção;
- que barreiras limitam cada cavidade;
- como um vazamento entre cavidades pode **pressurizar sucessivamente** outras regiões do sistema;
- quais sequências de falhas podem levar ao meio ambiente.

O material não traz o detalhamento de dispositivos específicos de alívio de sobrepressão; porém, conceitualmente, ele estabelece que a gestão de sobrepressão depende primeiro de **identificar as cavidades**, os **modos de falha** e as **barreiras que as separam**.  
**Fontes:** `petroles-4ee4bce16acf674505c8912d:pNone:1221986.0-1222029.0`, `petroles-4ee4bce16acf674505c8912d:pNone:1222010.0-1222047.0`, `petroles-4ee4bce16acf674505c8912d:pNone:1222071.0-1222114.0`

## 6. Independência de barreiras, redundância e Conjuntos Solidários de Barreiras (CSB)
Um ponto decisivo para avaliar isolamento e resposta a falhas é distinguir **redundância** de **independência**.

### 6.1 Independência de barreiras
O material define que **duas ou mais barreiras são independentes quando o funcionamento de cada uma não depende de componentes em comum**. Isso é mais rigoroso do que simplesmente ter duas válvulas em série.

### 6.2 Exemplo importante: válvulas da ANM
Durante a produção, o fluxo pode ser interrompido na ANM por válvulas como **M1** e **W1**. Entretanto, essas válvulas **não são necessariamente barreiras independentes**, porque a atuação de ambas pode depender de componentes comuns, como:
- bloco da ANM;
- stab de produção;
- sistema de controle das válvulas;
- interfaces mecânicas da própria árvore.

Logo, a ANM pode conter **barreiras redundantes**, mas ainda assim atuar como **uma única barreira independente** do ponto de vista sistêmico.

### 6.3 Conjunto Solidário de Barreiras (CSB)
Para resolver esse problema de continuidade e atalhos entre caminhos, o material apresenta o conceito de **Conjunto Solidário de Barreiras (CSB)**: um conjunto de uma ou mais barreiras apto a impedir o fluxo não intencional dos fluidos do intervalo permeável **considerando todos os caminhos possíveis**.

A lógica do CSB é:
- garantir que haja barreira em cada caminho relevante;
- verificar se as barreiras estão **interligadas de modo contínuo**;
- evitar comunicações ou atalhos que permitam ao fluido contornar a contenção;
- avaliar se existem **dois CSB independentes** entre si.

O próprio material propõe como critério de avaliação que uma operação seja considerada favorável do ponto de vista de segurança/integridade quando houver **dois CSB independentes e testados**.  
**Fontes:** `petroles-4ee4bce16acf674505c8912d:pNone:1222010.0-1222047.0`, `regis-a8155330e2120dca899050ba:pNone:3217.0-3531.0`

## 7. Funções de isolamento e fechamento de emergência
Na fase de produção, o material distingue duas funções principais:

### 7.1 Função de fechamento de emergência
É a capacidade dos equipamentos instalados no poço — especialmente **DSSS** e **válvulas da ANM** — de **interromper o fluxo** a partir de:
- uma solicitação/comando; ou
- uma falha que leve à **perda de potência hidráulica** nas linhas de controle.

Essa formulação é importante porque associa a filosofia de fail-safe não apenas a um comando ativo, mas também à resposta esperada diante de perda de utilidades de controle.

### 7.2 Função integridade de poço
É a capacidade de **prevenir vazamentos para o meio ambiente** tanto durante a produção como enquanto o poço estiver fechado.

### 7.3 Implicações operacionais
Em termos de resposta a falhas, isso significa que a avaliação não deve parar em “a válvula fechou” ou “o DSSS foi demandado”. É preciso verificar:
- se a barreira demandada realmente vedou o caminho de fluxo;
- se permanece pelo menos um segundo conjunto independente disponível;
- se a falha observada é de **fechamento**, **vedação** ou **vazamento externo**;
- se a perda de potência hidráulica afetou **mais de uma barreira por causa comum**.

Como as barreiras na produção são tratadas como uma composição **mais estática** do que na perfuração, sua funcionalidade precisa ser verificada por **monitoramento de parâmetros** e por **testes periódicos**, especialmente em funções standby que só revelam seu estado real quando demandadas.  
**Fontes:** `petroles-004c2afadba7ea17c7dd7908:pNone:2972401.0-2972440.0`, `petroles-4ee4bce16acf674505c8912d:pNone:1222049.0-1222091.0`, `petroles-4ee4bce16acf674505c8912d:pNone:1222071.0-1222114.0`

## 8. Modos de falha relevantes para perda de integridade
A metodologia reproduzida no material trabalha explicitamente com os seguintes **modos de falha** dos elementos/barreiras:
- **FNF**: falha no fechamento;
- **VPF**: vazamento na posição fechada;
- **VE**: vazamento externo;
- **VI**: vazamento interno;
- **VCA**: vazamento da coluna para o anular.

Esses modos de falha são relevantes porque não basta perguntar se o equipamento “falhou”; é preciso saber **como** falhou, pois cada modo produz caminhos de vazamento distintos e pressuriza cavidades diferentes.

Exemplos de implicação:
- **FNF** compromete a função de isolamento por comando ou fail-safe;
- **VPF** invalida a confiança na barreira mesmo após fechamento aparente;
- **VE** pode criar comunicação direta para o exterior ou entre volumes não previstos;
- **VI** pode transferir pressão entre cavidades internas;
- **VCA** pode deslocar o problema do caminho coluna para o caminho poço/anular.

Esse detalhamento é essencial para diagnósticos de campo, porque a resposta adequada depende de identificar se o evento é de **não atuação**, **não vedação**, **vazamento para cavidade interna** ou **vazamento para o exterior**.  
**Fontes:** `petroles-4ee4bce16acf674505c8912d:pNone:1222071.0-1222114.0`, `petroles-4ee4bce16acf674505c8912d:pNone:1222010.0-1222047.0`

## 9. Avaliação quantitativa da perda de integridade e da probabilidade de vazamento
Os trechos fornecidos apontam uma abordagem quantitativa baseada em **confiabilidade** e **Árvore de Falhas (AdF)** para apoiar decisões de integridade.

### 9.1 Finalidade da modelagem
A modelagem é proposta para avaliar o impacto de degradações ao longo da vida operacional do poço e quantificar a influência de:
- perda de funcionalidade de componentes específicos;
- alteração do intervalo entre testes de funções standby;
- histórico operacional e histórico de falhas;
- combinação de falhas até o evento topo de vazamento.

Com base em dados reais, pode-se estimar uma **função taxa de falha** para cada modo de falha e componente e, incorporando isso ao modelo, estimar a probabilidade de ocorrência do evento topo em determinado período.

### 9.2 Passos metodológicos destacados
A metodologia citada para a função integridade de poço inclui, em síntese:
1. definir o escopo da completação analisada;
2. definir o evento topo indesejado;
3. definir as cavidades onde a pressão pode ficar trapeada;
4. identificar modos de falha e caminhos de vazamento;
5. identificar a tolerância à falha do sistema;
6. identificar vetores de barreiras;
7. identificar **cortes mínimos**;
8. calcular a probabilidade de vazamento.

### 9.3 Cortes mínimos
Em uma AdF, **corte** é um conjunto de eventos cuja ocorrência implica o evento topo. **Corte mínimo** é o conjunto irredutível: se qualquer evento for removido, ele deixa de causar necessariamente o evento topo.

Na prática, os cortes mínimos ajudam a identificar:
- quais combinações de falhas realmente governam a perda de integridade;
- onde estão os pontos de maior sensibilidade da arquitetura de barreiras;
- quais falhas múltiplas merecem priorização em testes, inspeções e intervenção.

### 9.4 Combinação de probabilidades e equipamento contingencial
O exemplo fornecido mostra a lógica de uma função de segurança exercida por um **dispositivo primário** e por um **equipamento de segurança contingencial (ESC)**. Quando a AdF usa uma porta lógica do tipo **E** para representar que a função só se perde se **ambos falharem**, e assumindo **independência** entre eles, a probabilidade de perda da função é o **produto** das probabilidades de falha individuais:

\[
P(\text{perda da função}) = P(\text{falha do dispositivo primário}) \times P(\text{falha do contingencial})
\]

Esse raciocínio é valioso para decisão operacional: um equipamento contingencial independente pode reduzir significativamente a probabilidade de perda da função de fechamento, mas essa redução só é válida se a hipótese de independência for tecnicamente defensável.  
**Fontes:** `petroles-004c2afadba7ea17c7dd7908:pNone:2972401.0-2972440.0`, `petroles-4ee4bce16acf674505c8912d:pNone:1222049.0-1222091.0`, `petroles-4ee4bce16acf674505c8912d:pNone:1222071.0-1222114.0`, `regis-a8155330e2120dca899050ba:pNone:3217.0-3531.0`

## 10. Resposta operacional a vazamentos, falhas de barreiras e perda de controle do poço
Com base nos conceitos dos trechos fornecidos, a resposta operacional a eventos de integridade deve se orientar pelos seguintes princípios técnicos.

### 10.1 Identificar a natureza do evento
Primeiro, é necessário distinguir entre:
- **degradação de barreira sem vazamento externo confirmado**;
- **liberação limitada** cessada por barreira pré-instalada;
- **vazamento descontrolado para o ambiente externo**;
- **perda da função de fechamento de emergência**.

Essa classificação altera o entendimento do risco e a urgência da resposta.

### 10.2 Verificar quais barreiras/CSB permanecem válidos
Após a falha, deve-se avaliar quais barreiras continuam **disponíveis** e se permanecem **independentes**. Não basta contar válvulas fechadas; é necessário verificar se elas compartilham componentes comuns ou se um mesmo mecanismo de falha compromete várias barreiras ao mesmo tempo.

### 10.3 Considerar a continuidade do envelope de contenção
A análise deve abranger os caminhos **coluna, poço, anular externo e rocha**, além das interfaces entre eles. Isso é particularmente importante quando há sinais de comunicação entre cavidades, migração de pressão ou vazamento em conexões e stabs.

### 10.4 Apoiar a decisão com monitoramento e testes
Na fase de produção, como a composição das barreiras é mais estática, a confiabilidade do sistema depende de:
- monitoramento de parâmetros;
- testes periódicos das funções standby;
- avaliação do histórico de falhas;
- reavaliação do intervalo entre testes quando houver degradação observada.

### 10.5 Critério conceitual para retorno à condição operacional
O retorno à produção, do ponto de vista conceitual extraído do material, deve estar condicionado à restauração de uma condição em que a integridade do poço volte a ser sustentada por **barreiras/CSB independentes e validados**, e não apenas pela percepção de que o fluxo foi restabelecido.

### 10.6 Quando o evento caracteriza perda de controle de poço
Se, após demanda das barreiras previamente instaladas, o fluxo para o meio externo continuar, o evento se enquadra na definição apresentada de **erupção/blowout**. Nesse caso, a situação excede o escopo de simples falha local de válvula e passa a representar perda do controle funcional do poço.  
**Fontes:** `petroles-004c2afadba7ea17c7dd7908:pNone:2972401.0-2972440.0`, `petroles-4ee4bce16acf674505c8912d:pNone:1222010.0-1222047.0`, `petroles-4ee4bce16acf674505c8912d:pNone:1222049.0-1222091.0`, `petroles-4ee4bce16acf674505c8912d:pNone:1222071.0-1222114.0`

## 11. Pontos críticos de decisão para engenharia e operações subsea
A partir do conjunto de fontes, os principais critérios de decisão técnica para esta faceta são:

- **Não confundir redundância com independência** de barreiras.
- **Não assumir integridade do poço** apenas porque há duas barreiras em um caminho isolado; é preciso considerar atalhos entre caminhos.
- **Mapear cavidades pressurizáveis** antes de concluir sobre isolamento e sobrepressão local.
- **Classificar o modo de falha** (FNF, VPF, VE, VI, VCA), e não apenas o componente afetado.
- **Usar testes e monitoramento** para funções standby, pois sua indisponibilidade pode permanecer oculta até a demanda real.
- **Priorizar análise de confiabilidade** quando houver degradação observada, envelhecimento ou mudança no intervalo de testes.
- **Tratar persistência de vazamento após atuação de barreiras** como critério funcional de perda grave de controle.

Esses princípios são compatíveis com a necessidade de operação segura e contínua de sistemas submarinos conectados a FPSO, ainda que o material fornecido esteja centrado principalmente no sistema poço-completado e na ANM.  
**Fontes:** `petroles-004c2afadba7ea17c7dd7908:pNone:2972401.0-2972440.0`, `petroles-4ee4bce16acf674505c8912d:pNone:1221936.0-1221985.0`, `petroles-4ee4bce16acf674505c8912d:pNone:1222010.0-1222047.0`, `regis-a8155330e2120dca899050ba:pNone:3217.0-3531.0`

## 12. Síntese final
A base técnica fornecida sustenta uma visão de que a resposta a falhas em poços submarinos não deve ser centrada apenas em um componente isolado, mas na **arquitetura de barreiras como sistema**. Em produção, o foco passa por:
- garantir fechamento de emergência por DSSS e válvulas da ANM;
- verificar vedação efetiva, não apenas comando de fechamento;
- manter **dois conjuntos independentes** de contenção quando aplicável ao critério adotado;
- reconhecer atalhos e cavidades pressurizáveis;
- usar monitoramento, testes e modelagem de confiabilidade para decidir sobre continuidade operacional, intervenção ou resposta ampliada a vazamentos.

Nesse enquadramento, **isolamento**, **proteção contra falha progressiva**, **detecção de perda de vedação** e **avaliação de independência real das barreiras** são os eixos centrais da integridade de poço submarino.  
**Fontes:** `petroles-004c2afadba7ea17c7dd7908:pNone:2972401.0-2972440.0`, `petroles-4ee4bce16acf674505c8912d:pNone:1221735.0-1221774.0`, `petroles-4ee4bce16acf674505c8912d:pNone:1222010.0-1222047.0`, `petroles-4ee4bce16acf674505c8912d:pNone:1222071.0-1222114.0`