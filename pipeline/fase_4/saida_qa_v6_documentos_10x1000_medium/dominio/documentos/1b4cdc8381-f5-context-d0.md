# Cargas essenciais e integridade elétrica

## 1. Visão geral da continuidade de alimentação em FPSOs

Em um FPSO, o sistema elétrico é tipicamente **isolado**, isto é, sem conexão a outro sistema elétrico de potência. Por isso, a continuidade das cargas críticas depende de uma arquitetura em camadas, normalmente composta por:

1. **geração principal**;
2. **distribuição principal**;
3. **barramento essencial**;
4. **geração de emergência**;
5. **sistemas de corrente contínua e UPS** para ponte de energia sem interrupção.

A literatura reunida descreve FPSOs nos quais a planta é normalmente suprida por **quatro turbogeradores principais**, sendo comum que **três atendam à demanda normal** e o quarto permaneça em *stand-by*. Além disso, pode existir **gerador auxiliar** e **gerador de emergência** para suportar cargas auxiliares, essenciais e emergenciais. Em um exemplo de caso investigado pela ANP, a geração principal era composta por **3 moto-geradores de 1.600 kVA, 480 Vca**, e a geração de emergência por **2 moto-geradores de 500 kVA, 480 Vca**.

Do ponto de vista funcional, a continuidade das cargas críticas não se resume a manter a produção: ela precisa preservar, mesmo sob perda de geração principal, os sistemas necessários à **segurança de processo**, **intertravamentos**, **supervisão**, **telecomunicações** e, quando aplicável, aos sistemas de apoio marítimo e automação.

**Fontes da seção:** `regis-74dd376119cbb653fe9922bc:pNone:5876.0-6208.0`, `anp-80a4074406f1461613df01eb:p6-8:34.0-52.0`

## 2. Classificação das cargas e implicações para a arquitetura elétrica

A classificação das cargas é central para o projeto e para a operação segura do sistema elétrico do FPSO. Os trechos utilizados distinguem três grupos:

### 2.1 Cargas normais
São cargas cuja interrupção pode ser tolerada sem risco imediato à segurança. Incluem processos e utilidades passíveis de parada controlada. Parte dessas cargas auxiliares pode ser retomada por **gerador auxiliar** em caso de indisponibilidade da geração principal.

### 2.2 Cargas essenciais
São cargas associadas a sistemas cuja continuidade é importante para a segurança e a manutenção da unidade em condição operacional segura. Segundo a literatura usada, essas cargas são alimentadas por **barramento essencial**, que por sua vez é conectado ao barramento principal por **no mínimo duas conexões**. Em perda da geração principal ou em *shutdown* da unidade, essas cargas devem continuar alimentadas pelo **gerador de emergência**.

Exemplos citados para cargas essenciais:
- compressores de ar de serviço e instrumentação;
- unidades hidráulicas de controle do sistema de produção submarino;
- exaustores, ventiladores e sistemas de refrigeração de ar.

### 2.3 Cargas de emergência
São as cargas mais críticas para a salvaguarda da vida, segurança operacional dos poços e manutenção dos sistemas críticos da unidade. Essas cargas são alimentadas pelo **barramento essencial** e também por **UPS e sistemas em corrente contínua**. O objetivo é mantê-las energizadas:
- no intervalo entre a perda da geração principal e a entrada do gerador de emergência; e
- mesmo em falha do próprio gerador de emergência, dentro da autonomia disponível do sistema ininterrupto.

Exemplos citados para cargas de emergência:
- detecção de fogo e gás;
- combate a incêndio;
- parada de emergência;
- iluminação de emergência;
- luzes de navegação e de obstáculo aéreo;
- telecomunicações e intercomunicadores;
- painéis de controle do gerador de emergência e da bomba de incêndio;
- equipamentos de controle, intertravamento e supervisão.

**Implicação prática:** a criticidade da carga define **o nível de redundância**, **o barramento de alimentação**, **a necessidade de UPS/DC**, e o grau de restrição aceitável a testes, manobras e manutenção.

**Fontes da seção:** `regis-74dd376119cbb653fe9922bc:pNone:5876.0-6208.0`, `anp-80a4074406f1461613df01eb:p7-10:54.0-14.0`

## 3. Redundância, capacidade instalada e continuidade das cargas críticas

Os exemplos reunidos mostram que a confiabilidade global do FPSO começa na filosofia de geração. Para uma planta com demanda de ordem elevada, a redundância da geração principal é tratada por arranjos **k-de-n**, nos quais existem `n` geradores instalados e `k` é o número mínimo necessário para alimentar a planta.

Para uma demanda de referência de **100 MVA**, a literatura citada apresenta os seguintes exemplos de capacidade instalada:
- série: **100 MVA**;
- paralelo: **200 MVA**;
- `k=1, n=3`: **300 MVA**;
- `k=2, n=3`: **150 MVA**;
- `k=2, n=4`: **200 MVA**;
- `k=3, n=4`: **134 MVA**.

O ponto importante para a faceta desta rodada é que **maior redundância na geração principal não elimina a necessidade de UPS, bancos de baterias e barramentos essenciais**. Esses subsistemas continuam sendo necessários porque:
- a transferência entre fontes não é instantânea por si só;
- certos consumidores não admitem qualquer interrupção;
- falhas locais podem atingir controles e painéis mesmo com geração ainda disponível;
- a segregação de cargas evita que distúrbios ou falhas em consumidores não essenciais comprometam funções de segurança.

Em um caso real descrito pela ANP, a geração de emergência podia inclusive realizar **realimentação (*back feeding*)** de sistemas ligados ao painel principal, mas somente sob condições restritivas: geradores principais inoperantes, disjuntores principais abertos ou em teste, e chave seletora posicionada para “realimentação”. Isso ilustra que a continuidade operacional pode exigir caminhos alternativos de alimentação, porém com **permissivas claras** para evitar paralelismo indevido, energização insegura de barramentos ou perda de seletividade operacional.

**Fontes da seção:** `regis-74dd376119cbb653fe9922bc:pNone:5876.0-6208.0`, `anp-80a4074406f1461613df01eb:p6-8:34.0-52.0`

## 4. Arranjos A/B de 24 Vcc e UPS para cargas críticas

## 4.1 Sistemas de 24 Vcc
Em um exemplo de FPSO reportado pela ANP, havia vários sistemas independentes de **24 Vcc**. Dois deles alimentavam o **CLP** e os **painéis de controle dos geradores principais e de emergência**. Cada sistema era composto por:
- **2 retificadores/carregadores**;
- **2 bancos de baterias**;
- um **quadro elétrico de distribuição em corrente contínua**.

Cada conjunto “A” ou “B” possuía capacidade de suprir **100% da demanda** do respectivo quadro. Em falha de um conjunto, os consumidores podiam ser alimentados pelo outro por meio de um **disjuntor de interligação (TIE)**.

Esse arranjo tem implicações importantes para a continuidade de cargas críticas:
- elimina dependência de uma única fonte DC para controle e partida lógica dos sistemas de geração;
- permite recomposição por interligação controlada;
- cria uma base de redundância para automação, proteção e supervisão.

## 4.2 UPS em corrente alternada
Os trechos utilizados descrevem UPS industriais com função explícita de alimentar cargas críticas com energia de alta qualidade. No caso Transpetro, as UPS-CA são descritas como **dupla conversão on-line**: a energia CA de entrada é retificada em CC, que carrega o banco de baterias e alimenta um inversor; este reconstrói a saída CA dentro das especificações de desempenho. Isso reduz a exposição das cargas críticas a perturbações do suprimento principal.

No caso P-34, o sistema UPS era composto por:
- um ramo com **transformador/abaixador/estabilizador**;
- outro ramo com **carregador de baterias + baterias + inversor**.

Em condição normal, o sistema operava pelo ramo com baterias, garantindo **120 Vca** para equipamentos vitais, como o sistema **ECOS**. Havia **duas UPS**, cada uma dimensionada para suprir **100% das cargas de 120 Vca** do sistema, com distribuição em quadro CA contendo barramento “A”, barramento “B” e um disjuntor de interligação entre eles.

## 4.3 Segregação de cargas e prevenção de falhas comuns
O projeto citado indicava que as duas estações *master* do ECOS deveriam ser alimentadas por **UPS diferentes**. O valor técnico dessa segregação é direto: se uma UPS falhar, preserva-se a operacionalidade do sistema de supervisão por meio da outra. Em aplicações de FPSO, essa lógica vale também para CLPs, servidores, redes de automação, F&G e telecomunicações: **a redundância só se converte em disponibilidade real quando os canais são segregados de fato**.

## 4.4 Papel dos TIEs e interligações
Os TIEs entre barramentos ou entre conjuntos de retificação/baterias são recursos importantes para recuperação após falha, mas devem ser usados com disciplina operacional. Eles podem restaurar a alimentação de consumidores críticos, porém também reduzem a segregação quando mantidos fechados sem necessidade. A arquitetura usada nas fontes indica que o TIE é um recurso de contingência, não um substituto automático para separação funcional permanente.

**Fontes da seção:** `anp-80a4074406f1461613df01eb:p6-8:34.0-52.0`, `anp-80a4074406f1461613df01eb:p7-10:54.0-14.0`, `petroles-004c2afadba7ea17c7dd7908:pNone:488832.0-488860.0`

## 5. Vulnerabilidades relevantes para a continuidade das cargas essenciais

## 5.1 Bancos de baterias como ponto crítico de indisponibilidade
Nos trechos de Petrolês referentes a dutos e terminais, os bancos de baterias aparecem como parcela dominante das ordens de manutenção corretiva em sistemas de energia ininterrupta. Embora esse caso não seja de FPSO, o princípio é altamente transferível: **a UPS só é tão confiável quanto seu banco de baterias, carregadores, conexões e regime de manutenção**.

Foram identificadas três causas básicas de falhas nesses bancos:
- **especificações inadequadas**;
- **ineficiência dos testes funcionais vigentes**;
- **dificuldade de gestão do parque instalado** devido à elevada diversidade de materiais.

Para FPSOs, isso se traduz em risco direto sobre cargas como:
- CLPs e intertravamentos;
- supervisão e historiadores;
- telecomunicações;
- painéis de controle de geração e emergência;
- sistemas de segurança dependentes de alimentação contínua.

## 5.2 Ensaios invasivos podem aumentar o risco operacional
Os trechos usados relatam dificuldade prática com o **ensaio de capacidade** anual de baterias quando o sistema UPS não é redundante. O problema é relevante para unidades offshore: retirar o banco de operação ou transferir carga para uma condição degradada pode expor cargas críticas justamente durante o teste.

Além disso, foram observadas limitações de testes simplificados de descarga:
- um banco superdimensionado e submetido a baixa corrente pode aparentar autonomia suficiente em teste simplificado;
- o mesmo banco pode falhar numa falta real de energia;
- portanto, o resultado do teste simplificado pode **não representar corretamente o estado de saúde**.

O ensinamento prático é que a integridade elétrica das cargas essenciais não depende só do arranjo de projeto; depende também de **como se testa** sem degradar a própria barreira de continuidade.

## 5.3 Falhas catastróficas em ativos de média tensão e potência
Outro trecho aplicado como referência de disponibilidade offshore descreve que, embora raras, podem ocorrer falhas catastróficas em componentes internos de média tensão, como:
- transformador principal;
- terminais e barramentos de média tensão de entrada;
- filtro senoidal;
- terminais de saída.

Nesses casos, a indisponibilidade pode ser muito superior à de falhas modulares simples. Para FPSOs, isso reforça que a continuidade das cargas críticas não pode ser tratada apenas como um problema de geração disponível: a **integridade dos ativos elétricos de potência** também é determinante.

**Fontes da seção:** `petroles-004c2afadba7ea17c7dd7908:pNone:488850.60-488876.0`, `regis-cf9083b7fb6d77ade93a9431:pNone:622.0-651.0`

## 6. Integridade elétrica: manutenção, preditiva e gestão de ativos

## 6.1 Substituição de testes periódicos invasivos por monitoramento preditivo
Os trechos usados relatam uma mudança de paradigma: substituir testes de descarga periódicos por uma sistemática de **manutenção preditiva minimamente invasiva**, com uso de **medição de condutância** nos bancos de baterias. A justificativa técnica apresentada é que a condutância, como método ôhmico, possui correlação com a capacidade da bateria e permite acompanhar o estado de saúde com menor impacto operacional.

Vantagens destacadas:
- menor risco de interrupção da alimentação durante a avaliação;
- avaliação individual de elementos/monoblocos;
- priorização de troca de bancos e remanejamento de elementos;
- aumento de produtividade da manutenção;
- criação de base de dados para gestão do parque instalado.

Nos trechos utilizados, o ensaio de capacidade passa a ser aplicado **apenas em casos selecionados**, e não como prática indiscriminada anual para todos os bancos.

## 6.2 Padronização do parque instalado
A padronização de especificações foi tratada como medida de integridade e disponibilidade, não apenas de suprimentos. Reduzir a diversidade de modelos de baterias facilita:
- dimensionamento consistente por grupos de aplicação;
- reposição e intercâmbio seguro entre bancos, quando aplicável;
- treinamento da equipe;
- manutenção e estocagem de sobressalentes;
- comparação de desempenho entre modelos e condições operacionais.

## 6.3 Qualidade e classificação dos acumuladores
Os trechos apontam a adoção de acumuladores enquadrados como de **alta integridade**, além de requisitos de certificação/homologação citados no material de origem. Mesmo sem reproduzir a numeração normativa completa, o princípio útil para FPSOs é claro: para cargas críticas, a especificação do banco de baterias deve refletir a severidade e a criticidade do serviço, não apenas a capacidade nominal em Ah.

## 6.4 Base de dados de manutenção e análise holística
A gestão centralizada dos relatórios de preditiva foi apontada como ferramenta para:
- acompanhar tendências de degradação;
- comparar desempenho por modelo de bateria;
- correlacionar falhas com clima e condições operacionais;
- priorizar substituições antes da falha em demanda.

Em unidades offshore, essa abordagem é particularmente valiosa porque o custo de falha em carga crítica é desproporcional ao custo de monitoramento.

**Fontes da seção:** `petroles-004c2afadba7ea17c7dd7908:pNone:488850.60-488876.0`, `petroles-004c2afadba7ea17c7dd7908:pNone:488879.0-488921.0`

## 7. Disponibilidade, tempo de reparo e sobressalentes a bordo

Para ativos elétricos offshore em local remoto, um trecho utilizado de REGIS decompõe o tempo total de reparo como:

**T_reparo = T_if + T_ect + T_ls + T_rp**

Onde:
- **T_if**: tempo de identificação da falha;
- **T_ect**: tempo de execução do conserto e testes;
- **T_ls**: tempo para liberação do serviço;
- **T_rp**: tempo de preparação para retorno da produção.

Mesmo sendo apresentado no contexto de conversores de frequência para BCSS, o raciocínio é útil para a integridade elétrica de FPSOs. Em particular:
- a modularidade reduz o tempo de reparo de alguns equipamentos;
- a dificuldade de diagnóstico pode elevar muito `T_if`;
- a falta de peças a bordo eleva `T_ect` de forma crítica;
- rotinas formais de liberação de serviço e retorno tendem a ser relativamente constantes.

O material destaca a importância de manter a bordo sobressalentes como células, placas, ventiladores, sensores e periféricos, com preservação adequada. Em sistemas críticos, essa lógica pode ser estendida ao planejamento de sobressalentes para UPS, retificadores, cartões eletrônicos, módulos de potência e componentes auxiliares. A indisponibilidade de peças em ambiente offshore pode transformar uma falha reparável localmente em evento de longa duração.

O mesmo trecho também menciona que a alimentação externa dos circuitos de controle e ventilação é crucial para a disponibilidade de certos equipamentos, e que uma forma de aumentá-la é alimentar tais circuitos por **UPS**; como alternativa adicional, cita a possibilidade de usar tensões de controle em **corrente contínua diretamente dos bancos de baterias** da plataforma, quando o projeto do equipamento permitir.

**Fontes da seção:** `regis-cf9083b7fb6d77ade93a9431:pNone:622.0-651.0`

## 8. Implicações para projeto, comissionamento e operação

Com base nos trechos selecionados, as seguintes verificações são particularmente relevantes para a continuidade das cargas críticas e para a integridade elétrica dos ativos:

### 8.1 Projeto
- separar claramente cargas normais, essenciais e de emergência;
- garantir que cargas críticas de controle, supervisão e segurança tenham caminho por **UPS/DC**;
- prever **redundância A/B** com capacidade de 100% quando essa for a filosofia adotada;
- evitar pontos únicos de falha, inclusive por distribuição inadequada de estações *master* ou controladores na mesma UPS;
- avaliar se existe necessidade de recursos especiais de recomposição, como *back feeding*, com permissivas explícitas.

### 8.2 Comissionamento
- confirmar a capacidade real de cada canal A/B suprir a demanda prevista;
- testar a transferência por **TIE** e a recomposição após perda de um conjunto;
- verificar que cargas críticas foram segregadas conforme projeto;
- comprovar a alimentação do painel/retificadores/UPS por fontes compatíveis com os cenários de perda de geração principal e atuação do gerador de emergência.

### 8.3 Operação e manutenção
- tratar bancos de baterias como ativos críticos de continuidade, e não como acessórios da UPS;
- evitar ensaios invasivos que exponham cargas essenciais, exceto quando tecnicamente justificados e controlados;
- adotar monitoramento preditivo escalável e base de dados para priorização de trocas;
- manter disciplina de manobra em TIEs e barramentos interligados;
- gerir sobressalentes a bordo considerando o impacto de logística offshore no tempo de reparo.

**Fontes da seção:** `anp-80a4074406f1461613df01eb:p6-8:34.0-52.0`, `anp-80a4074406f1461613df01eb:p7-10:54.0-14.0`, `petroles-004c2afadba7ea17c7dd7908:pNone:488850.60-488876.0`, `petroles-004c2afadba7ea17c7dd7908:pNone:488879.0-488921.0`, `regis-cf9083b7fb6d77ade93a9431:pNone:622.0-651.0`, `regis-74dd376119cbb653fe9922bc:pNone:5876.0-6208.0`

## 9. Síntese técnica

A continuidade das cargas essenciais em FPSOs depende de uma cadeia de proteção em níveis:
- **geração principal redundante**, para sustentar a planta em regime normal;
- **barramento essencial**, para segregar consumidores críticos;
- **geração de emergência**, para sustentar a unidade em perda da geração principal;
- **24 Vcc e UPS**, para garantir ausência de interrupção em controles, intertravamentos, supervisão e outras cargas de segurança;
- **integridade dos ativos elétricos**, especialmente bancos de baterias, retificadores, UPS, painéis e componentes de potência;
- **gestão de manutenção e sobressalentes**, para que a redundância de projeto se converta em disponibilidade operacional real.

Em termos práticos, a lição comum das fontes é que a continuidade das cargas críticas não é obtida apenas pelo número de geradores instalados. Ela resulta da combinação entre **classificação correta das cargas**, **segregação elétrica coerente**, **redundância bem distribuída**, **testes que não destruam a própria disponibilidade** e **gestão disciplinada da integridade dos ativos elétricos**.

**Fontes da seção:** `anp-80a4074406f1461613df01eb:p6-8:34.0-52.0`, `anp-80a4074406f1461613df01eb:p7-10:54.0-14.0`, `petroles-004c2afadba7ea17c7dd7908:pNone:488832.0-488860.0`, `petroles-004c2afadba7ea17c7dd7908:pNone:488850.60-488876.0`, `petroles-004c2afadba7ea17c7dd7908:pNone:488879.0-488921.0`, `regis-cf9083b7fb6d77ade93a9431:pNone:622.0-651.0`, `regis-74dd376119cbb653fe9922bc:pNone:5876.0-6208.0`