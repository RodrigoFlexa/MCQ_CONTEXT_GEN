# Partidas, paradas e upset com atuação do sistema de alívio em FPSOs

## 1. Objetivo técnico da faceta
Em partidas, paradas normais, shutdowns automáticos e condições de upset em um FPSO, a tomada de decisão operacional depende da coordenação entre:
- o sistema básico de controle e supervisão;
- o sistema instrumentado de segurança/intertravamento;
- a detecção de fogo e gás;
- os controles dedicados de máquinas críticas, como compressores;
- o sistema de alívio, blowdown e tocha.

O ponto central não é apenas "parar" ou "partir" equipamentos, mas garantir que a trajetória transitória da planta permaneça controlada, com pressões, vazões e inventário de hidrocarbonetos conduzidos a uma condição segura. Em cenários rápidos, a atuação do sistema de alívio pode deixar de ser um evento secundário e passar a ser parte essencial da própria estratégia de proteção.  

**Fontes:** `petroles-004c2afadba7ea17c7dd7908:pNone:2452703.0-2452728.0`, `petroles-4ee4bce16acf674505c8912d:pNone:1447519.0-1447549.0`, `regis-dce79d82a4a7f1760d88e146:pNone:43.0-68.0`

## 2. Papéis dos sistemas de controle, supervisão e segurança

### 2.1 CLP/controlador versus supervisório
Os controladores programáveis executam lógica sequencial, temporização, contagem e cálculos em ciclos de varredura de milissegundos, lendo entradas, processando a lógica e atualizando saídas. Entradas podem ser analógicas, como pressão, temperatura, vazão e nível, ou digitais, como fim de curso e chaves discretas. Saídas podem modular válvulas de controle, variar rotação de máquinas ou atuar dispositivos binários como solenóides e partidas/paradas de motores.

Já o sistema de supervisão e controle (SSC/SCADA/SDCD, conforme a arquitetura) tem função principal de interface operacional: apresentar valores em tempo real, tendências, alarmes, estados de equipamentos, histórico, eventos e relatórios, além de permitir comandos operacionais autorizados. O material também ressalta que controles com restrição temporal e intertravamentos devem ser implementados diretamente nos controladores, e não no supervisório, por limitações de velocidade, segurança e confiabilidade.

Consequência operacional: em partidas, shutdowns e upset, o operador usa o supervisório para monitorar e comandar dentro dos limites autorizados, mas a proteção de tempo crítico deve estar residente no sistema de controle/intertravamento apropriado.  

**Fontes:** `petroles-004c2afadba7ea17c7dd7908:pNone:2452703.0-2452728.0`

### 2.2 Intertravamentos e funções de segurança
O subsistema de intertravamento é responsável por ações automáticas quando a integridade física do equipamento está em risco, incluindo paradas de emergência. Para compressores centrífugos, os trechos citam como funções típicas de segurança: nível alto em vasos de sucção, sobrevelocidade, temperatura alta de descarga, pressão/temperatura anormal de óleo de lubrificação, pressão baixa de gás de selagem, deslocamento axial alto e vibração alta.

Os textos também indicam práticas de confiabilidade como:
- redundância de iniciadores com votação 2oo2 em várias funções;
- alarme de discrepância entre sensores redundantes;
- degradação para 1oo1 em caso de falha de um sensor;
- sobrevelocidade tratada por sistema eletrônico dedicado;
- sinais de trip comandados por meios físicos hardwired;
- condição segura em falta de energia.

Em termos operacionais, isso significa que permissivas de partida e lógica de shutdown não devem ser avaliadas apenas pela leitura de uma variável no SDCD: é preciso considerar a disponibilidade dos sensores, o estado da votação, falhas degradadas e a cadeia física de atuação do trip.  

**Fontes:** `regis-f8686f0be4025804d5448444:pNone:50.60-89.0`, `petroles-004c2afadba7ea17c7dd7908:pNone:781081.60-781145.0`

## 3. Alarmes como barreira anterior ao ESD

### 3.1 Conceitos úteis para operação
Os trechos definem alarme como aviso sonoro e/ou visual de mau funcionamento ou condição anormal que requer resposta em tempo restrito. Também são relevantes:
- **alarme incômodo**: anuncia excessivamente, desnecessariamente ou não normaliza após a resposta correta;
- **avalanche de alarmes**: grande quantidade de alarmes em curto período, tornando-os ingerenciáveis;
- **inibição**: desabilitação controlada e temporária do alarme por ação manual;
- **lógica de primeiro trip**: identifica qual inicializador acionou primeiro um cenário com múltiplos sinais;
- **racionalização de alarmes**: análise formal para justificar setpoints, prioridades e resposta esperada.

Em shutdowns e upset, esses conceitos são decisivos: a equipe precisa diferenciar o evento iniciador dos alarmes consequentes e evitar que a sobrecarga de informação atrase ações corretivas.

**Fontes:** `petroles-004c2afadba7ea17c7dd7908:pNone:2452720.0-2452749.0`

### 3.2 Relação entre alarmes e atuação do ESD
O material indica que um bom sistema de alarmes ajuda o operador a identificar situações perigosas antes que o ESD seja forçado a intervir. Isso reduz intervenções desnecessárias do ESD e melhora a segurança operacional. Porém, em perturbações severas, sistemas mal configurados podem gerar volume massivo de alarmes, incluindo chattering e concentração em bad actors, o que compromete a resposta humana.

Portanto, para avaliar uma decisão operacional durante upset, não basta saber que havia alarmes; é preciso verificar se os alarmes eram gerenciáveis, prioritizados e associados a ações claras. Em cenário de alívio iminente, avalanche de alarmes pode mascarar a causa da sobrepressão e atrasar isolamento, redução de carga ou abertura coordenada de rotas seguras.

**Fontes:** `petroles-4ee4bce16acf674505c8912d:pNone:333830.0-333868.0`, `petroles-004c2afadba7ea17c7dd7908:pNone:2452720.0-2452749.0`

## 4. Partidas com foco em proteção contra surge e preparo para alívio

### 4.1 Permissivas e preparação operacional
Em partidas de trens de compressão e sistemas associados, a lógica de partida deve incorporar permissivas, estados local/remoto, disponibilidade de intertravamentos, alarmes e posicionamento de válvulas. O uso de simulação dinâmica é apontado como ferramenta útil para verificar procedimentos de partida, revisar a lógica antes da operação real, reduzir tempo de comissionamento e treinar operadores para reconhecer comportamento transitório.

Uma implicação prática importante é que a decisão de prosseguir com a partida deve considerar não apenas o estado estacionário pretendido, mas também os desvios transitórios previsíveis e a resposta automática da proteção.  

**Fontes:** `petroles-4ee4bce16acf674505c8912d:pNone:1447519.0-1447549.0`, `petroles-004c2afadba7ea17c7dd7908:pNone:2452703.0-2452728.0`

### 4.2 Controle anti-surge na partida e em perturbações rápidas
Os trechos sobre compressores indicam que o controle anti-surge deve ser implementado por estágio quando a máquina tiver mais de um estágio e executado em equipamento digital com algoritmo inferior a 100 ms. Também são citados critérios relevantes:
- levantamento da curva real de surge durante a partida da unidade;
- tempo máximo de resposta de transmissores da ordem de 100 ms;
- linhas de impulso curtas, inferiores a 2 m, para não degradar a dinâmica;
- válvula de reciclo com atuação rápida, com constante de tempo de abertura menor que 2 s;
- possibilidade de operação manual da malha pelo SDCD via sinal físico 4-20 mA, mas com retomada automática da válvula pelo anti-surge se houver ameaça de surge e a válvula não estiver em manutenção.

Decisão operacional importante: se a unidade estiver em partida e a malha anti-surge estiver em manual, isso não elimina a exigência de proteção automática diante de aproximação da linha de surge. O modo manual pode ser aceitável em condição controlada, mas não deve impedir o override protetivo da válvula de reciclo.

Os textos também descrevem tratamento de falhas de instrumentação:
- falha de transmissor de pressão usado nos cálculos: o controle passa a usar valor de projeto do sinal afetado;
- falha de sinal de vazão: a válvula de reciclo vai para posição predeterminada, o controle vai para manual e alarme é gerado.

Operacionalmente, isso significa que a partida com instrumentação degradada pode até ter estratégia definida, mas passa a ocorrer com proteção reduzida e maior dependência de avaliação de risco e do procedimento específico da unidade.

**Fontes:** `regis-f8686f0be4025804d5448444:pNone:50.60-89.0`

## 5. Paradas, trips e shutdowns: critérios práticos de atuação

### 5.1 Trip deve ser inteligível e fisicamente executável
Os trechos sobre automação de grandes máquinas registram que toda parada de emergência deve ser precedida por alarme, que sinais de trip devem ser hardwired e que, na falta de energia, o subsistema deve levar a máquina a condição segura. Também mencionam atrasos configurados em alguns casos específicos, por exemplo:
- atraso de 1 s em paradas por anormalidades no subsistema de óleo;
- atraso de 1 a 3 s para nível alto em vaso de sucção.

Isso não deve ser interpretado como regra universal para qualquer FPSO, mas ilustra um princípio: atrasos de trip só são aceitáveis quando fazem parte da filosofia de proteção do equipamento e quando o atraso não compromete a integridade.

Na avaliação operacional, algumas perguntas técnicas úteis são:
1. o alarme antecedente existiu e era visível ao operador?
2. o caminho de atuação do trip era independente do supervisório?
3. havia atraso configurado? Se sim, por justificativa técnica documentada?
4. a condição segura de perda de energia foi considerada?

**Fontes:** `petroles-004c2afadba7ea17c7dd7908:pNone:781081.60-781145.0`

### 5.2 Isolamento automático de fontes em detecção de gás
O relatório da ANP destaca que intertravamentos são forma primária de proteção contra sobrepressão segundo API RP 14C e que, em detecção de gás, boas práticas recomendam alarmes audíveis/visuais e atuação automática em fontes de gás. O trecho cita valores de referência de API para alarme até 25% do LIE e ações corretivas automáticas até 60% do LIE, mas mostra que em um projeto específico havia critérios mais conservadores na sala de bombas: alarme a 10% do LIE e shutdown a 30% do LIE.

O ponto mais importante do caso não é o número em si, mas a completude da matriz de causa e efeito. Na unidade investigada, o shutdown por gás na sala de bombas interrompia bombas de carga, porém não contemplava a bomba de stripping, que também movimentava hidrocarboneto. Assim, a fonte potencial de gás não era totalmente isolada.

Lição operacional para shutdowns e upset com atuação do alívio: a decisão correta não é "desligar algum equipamento", e sim isolar todas as fontes relevantes de inventário ou energia conforme a filosofia de segurança e a matriz causa-efeito da unidade. Se uma fonte permanece ativa, o cenário de perda de contenção pode continuar evoluindo mesmo com parte do sistema em shutdown.

**Fontes:** `anp-dabfb60617e4f0ede433578e:p218-220:9.0-25.0`

### 5.3 Alarme operacional explícito versus mera indicação em tela
No mesmo caso, a ANP relata ausência de alarme de alta pressão na descarga da bomba de stripping. Havia apenas indicação em pop-up, com escala inadequada e sem explicitação do valor máximo admissível. Sem alarme formal e sem limite operacional documentado no procedimento, a identificação da condição insegura tornava-se incerta.

Para avaliação de decisões em partida, parada ou upset, isso mostra que a simples disponibilidade de uma variável na IHM não equivale a uma barreira efetiva. Quando o parâmetro é crítico para evitar sobrepressão ou perda de contenção, é necessário que o operador receba alerta inequívoco e em tempo hábil.

**Fontes:** `anp-dabfb60617e4f0ede433578e:p218-220:9.0-25.0`

## 6. Interface entre shutdown/blowdown e sistema de alívio/tocha

### 6.1 Problema operacional clássico: a perturbação é mais rápida que a sequência de abertura
O estudo sobre sistema de tocha descreve problemas de arranjos por estágios em que a abertura de um estágio dependia da abertura completa do estágio anterior, por sinal de fim de curso. Em elevações bruscas de pressão, mesmo atingindo os setpoints dos pressostatos, a abertura dos estágios seguintes ficava inibida até a abertura total do anterior, frequentemente resultando em rompimento de discos de ruptura em paralelo às válvulas de controle de cada estágio.

Mesmo após remover o intertravamento entre estágios, o problema podia persistir por tempo morto entre detecção da elevação brusca de pressão e abertura efetiva da válvula. Esse ponto é central para shutdowns com atuação do alívio: sequências lógicas excessivamente encadeadas podem ser lentas demais para o distúrbio real.

**Fontes:** `regis-dce79d82a4a7f1760d88e146:pNone:43.0-68.0`

### 6.2 Estratégia de antecipação para despressurização e blowdown
Para mitigar esse problema, o trecho descreve um controle de turn-down da tocha que antecipa eventos, principalmente parada total ou parcial da plataforma com despressurização do processo. A lógica proposta inclui:
- medição de vazão no header de distribuição de gás aos estágios da tocha, ou medição por estágio com soma no CLP;
- correção da vazão com pressão e temperatura;
- tabela no controlador associando faixas de vazão à combinação adequada de estágios abertos;
- carregamento de um registro com o valor equivalente à vazão máxima da tabela sempre que é gerado comando de despressurização;
- decréscimo progressivo desse registro a uma velocidade dependente do processo da plataforma;
- comparação usando sempre o maior entre a vazão medida e o valor predito/forçado pelo registro, para selecionar previamente a combinação de estágios apropriada.

Em termos operacionais, isso quer dizer que, ao iniciar um blowdown, a tocha não deve esperar apenas a vazão real chegar. A lógica pode preparar a capacidade de queima antes da chegada do pico, compensando o tempo morto das BDVs e a inércia dos atuadores. Essa antecipação reduz risco de sobrepressão local, rompimento de discos e funcionamento inadequado da tocha.

**Fontes:** `regis-dce79d82a4a7f1760d88e146:pNone:43.0-68.0`

### 6.3 Benefícios operacionais adicionais do controle de turn-down
O texto aponta ainda três benefícios complementares:
- totalização do volume de gás queimado;
- indicação ao operador da posição de cada estágio da tocha;
- manutenção da radiação incidente em níveis permitidos em ampla faixa de vazão, inclusive em vazões baixas, evitando combinações de estágios que elevem demasiadamente a emissividade da chama.

Assim, o sistema de alívio não deve ser tratado apenas como rota passiva de emergência. Ele pode exigir lógica ativa de preparação, monitoramento e confirmação de posição para operar adequadamente tanto em despressurizações totais quanto parciais.

**Fontes:** `regis-dce79d82a4a7f1760d88e146:pNone:43.0-68.0`

## 7. Bypass, override, inibição e autoridade operacional
O supervisório pode permitir comandos como partida/parada de equipamentos, abertura/fechamento de válvulas, alteração manual/automático, mudança de setpoint, bypass de inicializadores de ESD e override de saídas. Contudo, os trechos são explícitos em afirmar que bypass e override devem ocorrer apenas em situações excepcionais, com procedimento específico, documentação, análise de risco e autorização de níveis hierárquicos superiores.

Para a operação de partidas e paradas, isso impõe critérios claros:
- não normalizar partida com proteção bypassada como prática de rotina;
- tratar override de saída como condição extraordinária, não como substituto de reparo;
- registrar quem autorizou, por quanto tempo e com quais compensações operacionais;
- diferenciar bypass de função de segurança, override de atuador e inibição de alarme, pois as consequências são diferentes.

Em upset com atuação do alívio, um bypass indevido pode retirar a barreira que isolaria a fonte, enquanto uma inibição de alarme mal controlada pode atrasar a percepção do evento iniciador.

**Fontes:** `petroles-004c2afadba7ea17c7dd7908:pNone:2452703.0-2452728.0`, `petroles-004c2afadba7ea17c7dd7908:pNone:2452720.0-2452749.0`

## 8. Critérios de decisão operacional para partidas, paradas e upset com alívio
A partir dos materiais fornecidos, decisões operacionais tecnicamente mais robustas tendem a seguir os critérios abaixo:

1. **Priorizar proteção automática de tempo crítico no controlador/intertravamento**, não no supervisório.  
2. **Exigir permissivas completas para partida**, incluindo sensores, válvulas críticas, lógica de intertravamento, estados local/remoto e disponibilidade da proteção anti-surge quando aplicável.  
3. **Não depender apenas de indicação de tela para variáveis críticas**; parâmetros associados a sobrepressão e perda de contenção devem ter alarme formal e resposta definida.  
4. **Usar a lógica de primeiro trip e o agrupamento/racionalização de alarmes** para distinguir causa iniciadora de consequências durante shutdown ou upset.  
5. **Em detecção de gás, isolar todas as fontes relevantes**, não apenas parte dos equipamentos da área.  
6. **Evitar encadeamentos lógicos lentos no sistema de alívio**, especialmente quando a perturbação cresce mais rápido que a abertura sequencial de válvulas.  
7. **Antecipar a preparação da tocha/blowdown** em despressurizações planejadas ou automáticas, considerando tempo morto de válvulas e capacidade necessária por estágio.  
8. **Tratar bypass/override como exceção controlada**, com análise de risco e autoridade formal.  
9. **Empregar simulação dinâmica** para validar procedimentos de partida, shutdown e ESD, além de treinar operadores para cenários fora da rotina.  
10. **Considerar degradação de sensores e malhas de votação** na decisão de continuar operando ou iniciar parada controlada.

**Fontes:** `petroles-004c2afadba7ea17c7dd7908:pNone:2452703.0-2452728.0`, `petroles-004c2afadba7ea17c7dd7908:pNone:2452720.0-2452749.0`, `regis-f8686f0be4025804d5448444:pNone:50.60-89.0`, `petroles-004c2afadba7ea17c7dd7908:pNone:781081.60-781145.0`, `anp-dabfb60617e4f0ede433578e:p218-220:9.0-25.0`, `petroles-4ee4bce16acf674505c8912d:pNone:1447519.0-1447549.0`, `regis-dce79d82a4a7f1760d88e146:pNone:43.0-68.0`, `petroles-4ee4bce16acf674505c8912d:pNone:333830.0-333868.0`

## 9. Exemplos de aplicação

### Exemplo 1: partida de compressor com reciclo em manual
Se o reciclo estiver em manual pelo SDCD, mas a válvula estiver disponível e a máquina se aproximar do surge, a estratégia correta, segundo o material, é permitir que o controle anti-surge assuma automaticamente a posição da válvula. Prosseguir com a partida sem essa proteção automática eleva o risco de surge durante aceleração e estabilização de carga.  

### Exemplo 2: shutdown por gás em área de bombas
Se houver detecção de gás e a matriz causa-efeito desligar apenas parte dos equipamentos que movimentam hidrocarboneto, a resposta é tecnicamente incompleta. A decisão correta é revisar o isolamento das fontes da área, pois manter uma bomba relevante em operação pode perpetuar a liberação.  

### Exemplo 3: despressurização parcial com atuação de blowdown
Se a planta executar blowdown e o sistema de tocha abrir estágios apenas em cascata após confirmação integral do estágio anterior, pode haver atraso incompatível com a velocidade do evento. A estratégia mais robusta é preparar antecipadamente a combinação de estágios requerida pela vazão esperada da despressurização.  

**Fontes:** `regis-f8686f0be4025804d5448444:pNone:50.60-89.0`, `anp-dabfb60617e4f0ede433578e:p218-220:9.0-25.0`, `regis-dce79d82a4a7f1760d88e146:pNone:43.0-68.0`