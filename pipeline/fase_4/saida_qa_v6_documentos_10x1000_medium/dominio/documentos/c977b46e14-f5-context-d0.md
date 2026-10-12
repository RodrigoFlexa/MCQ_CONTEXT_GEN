# Tratamento do gás produzido em FPSOs — controle, proteção e troubleshooting

## 1. Escopo técnico desta faceta

O material disponível sustenta principalmente princípios de **automação, gerenciamento de alarmes, intertravamentos, controle de estabilidade e proteção de compressores**, com aplicação direta às partes do tratamento do gás onde há maior sensibilidade operacional em FPSOs: vasos/scrubbers de sucção, compressores, sistemas de reciclo/anti-surge, malhas regulatórias associadas à qualidade do gás e integração entre BPCS/SSC/SIS.

Assim, este documento foca em **estabilidade operacional, proteção automática e diagnóstico de falhas** no tratamento do gás, sem pretender cobrir em detalhe químicas e equipamentos específicos de adoçamento, TEG ou membranas quando não sustentados pelos trechos fornecidos.

**Fontes:** `petroles-004c2afadba7ea17c7dd7908:pNone:2452608.0-2452660.0`, `petroles-004c2afadba7ea17c7dd7908:pNone:2452703.0-2452728.0`, `petroles-004c2afadba7ea17c7dd7908:pNone:2452751.0-2452797.0`

## 2. Arquitetura de controle e supervisão aplicável ao tratamento do gás

### 2.1 Papel do CLP/BPCS/SIS versus SSC/SCADA

O controlador lógico programável (CLP) é descrito como um sistema eletrônico digital com memória programável para executar lógica sequencial, temporização, contagem e aritmética, operando em ciclo de **leitura das entradas, execução da lógica e atualização das saídas**. Esse ciclo de scan ocorre tipicamente em milissegundos, o que o torna adequado às funções com restrição temporal.

No contexto do tratamento do gás, isso implica que funções como:

- malhas regulatórias rápidas;
- intertravamentos de processo;
- cálculos com exigência temporal;
- ações automáticas de proteção;
- lógica de parada associada a compressores e equipamentos críticos;

**devem residir no controlador**, e não depender do sistema supervisório para sua execução primária.

O SSC/SCADA, por sua vez, tem como função principal disponibilizar ao operador:

- valores em tempo real de variáveis analógicas;
- tendências de processo;
- anunciação e reconhecimento de alarmes;
- indicação de estado de equipamentos;
- registro de eventos e históricos;
- emissão de relatórios;
- interface para comandos operacionais autorizados.

O próprio material indica que o uso do supervisório como controlador não é o arranjo preferencial em plantas maiores, devido a limitações de **tempo de resposta, segurança e confiabilidade** quando comparado ao controle direto no CLP.

### 2.2 Implicações para sistemas de tratamento do gás

Em trens de tratamento do gás em FPSOs, isso leva a uma separação funcional desejável:

- **BPCS/CLP**: controle regulatório de pressão, vazão, nível, temperatura, reciclo, permissivos de partida/parada e intertravamentos de processo;
- **SIS/ESD**: funções instrumentadas de segurança e paradas automáticas quando a integridade do equipamento ou da instalação estiver ameaçada;
- **SSC/SCADA/IHM**: supervisão, tendências, histórico, alarmes, first-out, apoio à decisão e interface operacional.

Esse arranjo é especialmente relevante quando o gás tratado precisa atender simultaneamente a requisitos de qualidade, continuidade operacional e proteção de máquinas.

**Fontes:** `petroles-004c2afadba7ea17c7dd7908:pNone:2452703.0-2452728.0`, `petroles-004c2afadba7ea17c7dd7908:pNone:2452608.0-2452660.0`

## 3. Gerenciamento de alarmes no tratamento do gás

### 3.1 O que é alarme e o que é evento

O material distingue claramente:

- **Alarme**: aviso sonoro e/ou visual que indica condição anormal que requer resposta do operador em tempo restrito.
- **Evento**: mudança de estado que não demanda ação do operador; deve ser registrada para análise, manutenção ou rastreabilidade, mas não necessariamente anunciada como alarme.

Essa distinção é crítica no tratamento do gás. Se tudo for anunciado como alarme, o operador perde a capacidade de discernir o que realmente requer ação imediata para evitar:

- perda de especificação do gás;
- atuação do SIS/ESD;
- parada de compressores;
- propagação de perturbações para flare, reinjeção, exportação ou gás combustível.

### 3.2 Conceitos relevantes

Os trechos fornecem definições úteis para a filosofia de alarmes:

- **alarme incômodo**: anuncia excessivamente, desnecessariamente, ou não retorna ao normal após a resposta correta;
- **alarme ajustável**: setpoint alterável manual ou automaticamente conforme condição operacional;
- **alarme de sistema**: decorre de falha de hardware, software, transmissores ou comunicação;
- **avalanche de alarmes**: grande quantidade de alarmes em curto intervalo, superando a capacidade de gerenciamento pelo operador;
- **eclipse**: um nível superior substitui um inferior na mesma medição;
- **inibição**: desabilitação manual, controlada e temporária;
- **supressão**: impedimento automático da ativação durante condição pré-estabelecida;
- **prioridade**: nível de relevância/urgência atribuído ao alarme;
- **tempo de resposta**: intervalo entre a anunciação e o início da ação corretiva.

### 3.3 Por que isso é decisivo para estabilidade operacional

Os textos destacam que um sistema de alarmes bem concebido ajuda o operador a restaurar a planta perturbada **antes que o SIS precise atuar**. Em contraste, sistemas com pseudo-alarmes e excesso de anunciadores:

- dificultam a identificação do problema real;
- aumentam o tempo de resposta;
- pioram o desempenho tanto em operação normal quanto em perturbações;
- elevam o risco para pessoas, instalação e meio ambiente;
- aumentam perdas de produção.

Para o tratamento do gás, esse princípio é central: uma perturbação de nível, pressão, temperatura, vazão, vibração ou condição de reciclo pode inicialmente exigir apenas correção operacional; sem boa filosofia de alarmes, a situação evolui para trip desnecessário ou tardio.

### 3.4 Filosofia, racionalização e apresentação

Os trechos associam um sistema robusto de alarmes à existência de:

- **filosofia de alarmes** documentada;
- **racionalização** dos alarmes com base nessa filosofia;
- separação coerente entre alarmes e eventos;
- priorização consistente;
- logs e historiador para análise posterior;
- monitoramento de desempenho do sistema de alarmes.

Também são mencionadas boas práticas de IHM:

- mensagens padronizadas;
- cores por prioridade para as mensagens;
- alteração de cor de objetos de tela para sinalizar anormalidades;
- reconhecimento do alarme pelo operador apenas como confirmação de ciência, não como solução da causa.

Em termos práticos, o reconhecimento do alarme **não elimina o desvio de processo**; ele apenas silencia/confirmar a notificação. Em troubleshooting, isso evita a falsa percepção de normalidade quando a causa raiz permanece ativa.

**Fontes:** `petroles-004c2afadba7ea17c7dd7908:pNone:2452751.0-2452797.0`, `petroles-004c2afadba7ea17c7dd7908:pNone:2452608.0-2452660.0`, `petroles-004c2afadba7ea17c7dd7908:pNone:2452994.0-2453045.0`

## 4. Controle administrativo e operacional de bypass e override

Os trechos atribuem forte criticidade a ações como:

- bypass de pontos de entrada inicializadores de ESD;
- override de pontos de saída, forçando atuadores energizados ou desenergizados;
- mudança de setpoints e parâmetros de controladores;
- mudança de referências usadas em totalização/correção;
- colocação de equipamentos em estado de manutenção.

### 4.1 Princípios operacionais extraídos do material

1. **Bypass e override são excepcionais**.
2. Devem seguir **procedimentos específicos de segurança operacional**.
3. Devem ser **documentados**.
4. Exigem **análise de risco**.
5. Dependem de **autorização por níveis hierárquicos superiores**, conforme criticidade.
6. O sistema deve ter **categorias de acesso** distintas por perfil de usuário.

### 4.2 Aplicação ao tratamento do gás

Em tratamento do gás, isso é particularmente sensível porque bypass indevido pode mascarar ou neutralizar proteção contra cenários como:

- nível alto em vaso/scrubber de sucção;
- falhas críticas de lubrificação ou gás de selagem em compressores;
- alta temperatura de descarga;
- vibração elevada;
- falhas de sensores usados em lógica anti-surge;
- permissivos de partida que evitam energização em condição insegura.

Para troubleshooting, um dos primeiros passos em anomalias persistentes deve ser verificar se há **pontos inibidos, suprimidos, em bypass, em override ou equipamentos em manutenção lógica**.

**Fontes:** `petroles-004c2afadba7ea17c7dd7908:pNone:2452703.0-2452728.0`, `petroles-004c2afadba7ea17c7dd7908:pNone:2452720.0-2452749.0`

## 5. Proteção automática e intertravamentos de equipamentos críticos do gás

### 5.1 Relação entre BPCS, SIS e sistema de alarmes

O material informa que o sistema de alarmes engloba tanto o **BPCS** quanto o **SIS**, ambos utilizando variáveis medidas por sensores para executar lógicas e gerar alarmes. Isso reforça que, no tratamento do gás, alarme e proteção são camadas relacionadas, mas com funções distintas:

- o **alarme** busca dar ao operador tempo para agir;
- o **SIS/intertravamento** atua automaticamente quando o risco à integridade exige ação independente da intervenção humana.

### 5.2 Funções típicas de segurança em compressores de gás

Os trechos sobre automação de grandes máquinas listam funções típicas de segurança para compressor centrífugo, incluindo:

- nível alto em vaso de sucção;
- sobrevelocidade;
- alta temperatura na descarga;
- baixa pressão de óleo de lubrificação de mancais;
- alta temperatura do óleo de lubrificação;
- baixa pressão de gás de selagem;
- alto deslocamento axial;
- alta vibração;
- alta pressão/temperatura de exausto.

No tratamento do gás, essa lista é relevante porque o compressor frequentemente está logo a jusante de etapas que precisam impedir **arraste de líquido** e estabilizar condições de sucção.

### 5.3 Integridade funcional e redundância

Os trechos destacam que:

- a classificação **SIL** se aplica às **malhas de segurança**, não isoladamente a cada componente;
- sensores e atuadores devem ser especificados para atender ao nível de integridade requerido pela malha;
- no exemplo apresentado para compressores, a maior parte dos iniciadores de segurança deve ter **redundância com votação** e alarme de discrepância;
- a detecção de sobrevelocidade deve ser feita por **sistema eletrônico dedicado**.

Como regra de leitura técnica deste material, o ponto principal é que funções de proteção críticas não devem depender de um único elemento sem avaliação de integridade, e que a arquitetura de votação/discrepância é parte do projeto de proteção.

### 5.4 Regras operacionais citadas para trips

O trecho também traz orientações objetivas para paradas de emergência em compressores:

- **toda parada de emergência deve ser precedida por um alarme**;
- sinais que comandem parada de emergência devem ser **físicos (hardwired)**;
- paradas por anormalidades no subsistema de óleo podem ter **atraso de 1 s**;
- paradas por **nível alto no vaso de sucção** podem ter atraso de **1 a 3 s**;
- na falta de energia, o subsistema deve levar a máquina a **condição segura**.

Essas orientações revelam um equilíbrio de projeto importante:

- atrasos muito curtos podem causar trips espúrios por ruído/transiente;
- atrasos muito longos expõem a máquina e a instalação;
- o valor admissível deve refletir a física do processo, a dinâmica do equipamento e a filosofia de risco da instalação.

**Fontes:** `petroles-004c2afadba7ea17c7dd7908:pNone:2452751.0-2452797.0`, `petroles-004c2afadba7ea17c7dd7908:pNone:781060.0-781099.0`, `petroles-004c2afadba7ea17c7dd7908:pNone:781081.60-781145.0`

## 6. Controle de estabilidade operacional: anti-surge e controle avançado

### 6.1 Relevância para o tratamento do gás

A estabilidade operacional do tratamento do gás depende não apenas da qualidade dos equipamentos, mas da qualidade das malhas de controle. Os textos fornecidos mostram dois eixos fundamentais:

1. **controle anti-surge** em compressores;
2. **controle avançado/estabilização** para reduzir variabilidade, evitar trips e melhorar qualidade.

### 6.2 Requisitos extraídos para controle anti-surge

O material descreve requisitos práticos de projeto e operação do controle anti-surge:

- a válvula de reciclo deve ter tempo de abertura com constante de tempo **inferior a 2 s**;
- se houver possibilidade de condensado na linha, a válvula de reciclo deve ficar em altura que evite **acúmulo de líquido** na linha de reciclo, pois isso prejudica a dinâmica do controle;
- a vazão de cada estágio e a vazão de reciclo devem ser medidas;
- o diferencial de pressão nos medidores da linha de reciclo deve ser o mais baixo possível para não degradar o desempenho;
- quando a vazão é medida na saída do estágio, ela deve ser convertida para as condições de sucção da máquina;
- medições sensíveis à vibração, como Coriolis e vórtices, são desaconselhadas nesse serviço; o texto prefere tecnologias por diferencial de pressão, com recomendação de Venturi quando a perda de carga disponível na sucção for pequena.

### 6.3 Respostas automáticas a falhas de instrumentação

Dois comportamentos automáticos são explicitados:

- falha de transmissor de pressão usado nos cálculos: o controle anti-surge passa a operar com o **valor de projeto** do sinal afetado;
- falha do sinal de vazão: a válvula de reciclo vai automaticamente para uma **posição predeterminada**, o controle entra em **manual** e um **alarme** deve ser gerado.

Esses mecanismos são valiosos em troubleshooting porque permitem diferenciar:

- degradação do desempenho por perda de qualidade de medição;
- proteção funcional preservada por fallback automático;
- falha grave em que o controle perde capacidade de manter estabilidade.

### 6.4 Controle avançado de estabilização e qualidade

Os textos também relatam que controles avançados podem:

- reduzir trips de compressores em cenários de instabilidade;
- mitigar efeitos de golfadas/slugging no escoamento;
- permitir operação mais aberta com segurança em poços/processos limitados por eventos de alta pressão;
- melhorar a qualidade do gás;
- reduzir variabilidade das malhas e desgaste de válvulas.

A lógica física por trás disso é clara no material: controladores PID lineares, quando sintonizados de forma fixa para diferentes pontos de operação, podem apresentar desempenho ruim, ampliando perturbações, aumentando a oscilação das variáveis e elevando a chance de alarme e atuação de sistemas de segurança. O controle avançado ajusta parâmetros/sintonia conforme a condição operacional, aproximando a planta de um comportamento mais estável.

Para tratamento do gás, a consequência operacional é relevante: menor variabilidade facilita manter condições requeridas para compressão, exportação, reinjeção ou gás combustível, além de reduzir o acionamento de proteções.

**Fontes:** `petroles-004c2afadba7ea17c7dd7908:pNone:781060.0-781099.0`, `petroles-004c2afadba7ea17c7dd7908:pNone:476933.0-476971.0`

## 7. First-out, causalidade e diagnóstico de falhas

### 7.1 Lógica de primeiro trip

O material apresenta a lógica de **primeiro trip/first-out** como método para identificar qual inicializador acionou primeiro o SIS em cenário com múltiplos alarmes. Essa lógica grava o primeiro evento em buffer e bloqueia a gravação posterior dos demais como causa primária.

Isso é particularmente importante no tratamento do gás porque uma única perturbação pode gerar rapidamente:

- alarmes de processo;
- desvios em equipamentos a jusante;
- paradas encadeadas;
- alarmes consequentes que não representam a causa raiz.

### 7.2 Importância de modelar interações entre equipamentos

O texto traz um exemplo genérico de duas bombas em série: a parada da primeira causa perda de sucção na segunda, que também para. Sem uma lógica causal adequada, ambas poderiam registrar a mesma variável secundária como motivo da parada, mascarando a origem.

A aplicação ao tratamento do gás é direta. Em um arranjo com scrubber/vaso de sucção, compressor, reciclo e sistemas a jusante, o troubleshooting precisa distinguir:

- **causa primária**;
- **efeitos propagados**;
- **alarmes consequentes**.

Assim, a lógica de trip e as telas de first-out devem contemplar não só instrumentos de proteção locais, mas também **interações entre equipamentos do mesmo sistema**.

### 7.3 Uso combinado de first-out, tendências e logs

Os trechos também sustentam o uso de:

- histórico de variáveis de processo;
- log de alarmes;
- registro de eventos;
- tendências;
- horímetros/estados de operação/falha/manutenção.

Em troubleshooting, isso permite reconstruir a sequência:

1. perturbação inicial;
2. primeira variável a sair da faixa;
3. alarmes anunciados;
4. atuação do operador;
5. atuação do BPCS/SIS;
6. estado final de trip ou estabilização.

Esse encadeamento é mais confiável do que avaliar apenas a condição final da planta após a parada.

**Fontes:** `petroles-004c2afadba7ea17c7dd7908:pNone:2452994.0-2453045.0`, `petroles-004c2afadba7ea17c7dd7908:pNone:2452703.0-2452728.0`, `petroles-004c2afadba7ea17c7dd7908:pNone:2452751.0-2452797.0`

## 8. Troubleshooting estruturado para anomalias no tratamento do gás

Com base nos mecanismos descritos nas fontes, um troubleshooting eficaz deve verificar pelo menos os seguintes grupos de causa.

### 8.1 Excesso de alarmes e pseudo-alarmes

Sintomas típicos:

- muitas mensagens em curto intervalo;
- dificuldade do operador em identificar a anormalidade principal;
- alarmes que persistem após a ação correta;
- perda de credibilidade do sistema.

Hipóteses técnicas:

- configuração inadequada de alarmes/eventos;
- prioridades mal definidas;
- ausência de supressão/eclipsamento apropriado;
- malhas instáveis gerando alarmes repetitivos;
- falta de racionalização e tratamento de bad actors.

### 8.2 Trips espúrios ou frequentes em compressores

Sintomas típicos:

- aumento de paradas sem falha mecânica evidente;
- trips precedidos por oscilação de variáveis;
- disparos em alta frequência durante perturbações normais de processo.

Hipóteses técnicas sustentadas pelos trechos:

- sintonia inadequada de malhas PID em diferentes pontos de operação;
- projeto insuficiente do controle anti-surge;
- atraso inadequado em intertravamentos;
- falhas de medição de pressão/vazão usadas na proteção/controle;
- acúmulo de condensado na linha de reciclo prejudicando a dinâmica;
- ausência de causalidade adequada na lógica de primeiro trip.

### 8.3 Indícios de separação insuficiente de líquido a montante

O fato de o material citar **nível alto no vaso de sucção** como função típica de segurança mostra que o controle de arraste de líquido é crítico para a estabilidade da compressão. Assim, alarmes/trips dessa natureza devem levar à verificação de:

- desempenho do vaso/scrubber de sucção;
- coerência da medição de nível;
- transientes de vazão/pressão que favoreçam arraste;
- resposta do sistema de drenagem/remoção de líquido;
- efeito da condição a montante sobre vibração, temperatura e estabilidade do compressor.

### 8.4 Falhas de instrumentação e de comunicação

Os textos descrevem explicitamente alarmes de sistema e casos de falha de transmissor/sinal. Em troubleshooting, devem ser verificados:

- qualidade e disponibilidade dos sinais analógicos e digitais;
- confirmação de comando enviado versus comando executado;
- falhas de comunicação entre campo, controlador e supervisório;
- discrepância entre sensores redundantes;
- fallback automático do controle para valor de projeto ou modo manual.

### 8.5 Interferência humana e condições administrativas do sistema

Também devem ser checados:

- pontos em bypass;
- saídas em override;
- equipamentos em estado de manutenção lógica;
- alterações recentes de setpoint/ganho;
- mudanças de acesso e permissivos;
- se o operador apenas reconheceu o alarme sem tratar a causa.

**Fontes:** `petroles-004c2afadba7ea17c7dd7908:pNone:2452751.0-2452797.0`, `petroles-004c2afadba7ea17c7dd7908:pNone:2452703.0-2452728.0`, `petroles-004c2afadba7ea17c7dd7908:pNone:781060.0-781099.0`, `petroles-004c2afadba7ea17c7dd7908:pNone:476933.0-476971.0`

## 9. Comissionamento, operação assistida e manutenção da performance

Os trechos sobre controle avançado ressaltam que o sucesso da implantação depende de:

- participação da operação desde o início;
- comissionamento cuidadoso e sintonia de parâmetros;
- monitoração contínua do desempenho das aplicações;
- feedback dos operadores;
- atualização de parâmetros quando necessário;
- treinamento inicial e reciclagem quando houver renovação das equipes.

Transpondo isso para tratamento do gás, o comissionamento e a manutenção da performance devem incluir ao menos:

- teste funcional das lógicas de alarme e trip;
- validação de first-out;
- conferência da apresentação correta na IHM;
- verificação de permissivos de partida/parada;
- teste de falha de instrumentos relevantes ao controle anti-surge;
- revisão de sintonia e comportamento das malhas nos diferentes pontos de operação.

A monitoração de KPIs de alarme, tendências de trips e recorrência de bad actors é consistente com a ideia, presente no material, de usar o sistema de alarmes não só como anunciador, mas também como **fonte estruturada para melhoria contínua da estabilidade operacional**.

**Fontes:** `petroles-004c2afadba7ea17c7dd7908:pNone:476933.0-476971.0`, `petroles-004c2afadba7ea17c7dd7908:pNone:2452608.0-2452660.0`, `petroles-004c2afadba7ea17c7dd7908:pNone:2452751.0-2452797.0`

## 10. Síntese técnica

Para esta faceta, o tratamento do gás em FPSOs deve ser entendido como um sistema em que **qualidade de controle, filosofia de alarmes e arquitetura de proteção** determinam a capacidade de manter operação estável e evitar paradas.

Os pontos mais consistentes nas fontes são:

- o **CLP/BPCS/SIS** deve executar controle e proteção com restrição temporal;
- o **SSC/SCADA** deve apoiar operação, diagnóstico e rastreabilidade, sem substituir a camada de proteção rápida;
- um sistema de alarmes eficaz diferencia alarme de evento, evita pseudo-alarmes e reduz a demanda de atuação do ESD;
- compressores exigem proteção dedicada, lógica de trip robusta, instrumentação apropriada e anti-surge bem projetado;
- first-out, tendências e logs são essenciais para causa raiz em paradas encadeadas;
- controle avançado e reavaliação contínua de sintonia podem reduzir trips, melhorar estabilidade e sustentar a qualidade do gás.

**Fontes:** `petroles-004c2afadba7ea17c7dd7908:pNone:2452703.0-2452728.0`, `petroles-004c2afadba7ea17c7dd7908:pNone:2452751.0-2452797.0`, `petroles-004c2afadba7ea17c7dd7908:pNone:2452994.0-2453045.0`, `petroles-004c2afadba7ea17c7dd7908:pNone:781060.0-781099.0`, `petroles-004c2afadba7ea17c7dd7908:pNone:781081.60-781145.0`, `petroles-004c2afadba7ea17c7dd7908:pNone:476933.0-476971.0`