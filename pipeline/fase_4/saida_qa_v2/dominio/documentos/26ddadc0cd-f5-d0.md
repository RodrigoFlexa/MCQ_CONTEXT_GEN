AVISO: os trechos são parciais e concentram-se em SIS/ESD e transferência de GNL em píer, com cobertura insuficiente para detalhar SIMOPS, inspeção/manutenção e fatores humanos além das referências pontuais abaixo.

**Análise de risco e integridade funcional**

A definição do sistema de intertravamento de segurança SIS, também referido como sistema de parada de emergência ESD, é vinculada ao processo de análise preliminar de perigos APP e à classificação SIL. A recomendação normativa destacada é a ligação entre os resultados da APP e o SIL requerido. No caso citado, se a severidade da consequência for moderada, a probabilidade de ocorrência dos eventos iniciadores for moderada e a eficácia das barreiras de proteção estiver entre moderada e baixa, a recomendação é a utilização de um SIS com SIL <NUMBER>. Para a plataforma de PARGO, o estudo mencionado adota SIL <NUMBER>. Entre as partes principais do sistema de segurança aparecem a estação central de operação e supervisão ECOS, o sistema de controle de processo e o SIS/ESD, com arranjos físicos do logic solver dimensionados para atender aos SILs requeridos.

**Critérios de projeto e confiabilidade**

Na avaliação de alternativas de projeto para sistemas de segurança, a combinação entre análise de confiabilidade e custo do ciclo de vida CCV é tratada como critério decisório, com prioridade para a performance do sistema de segurança sobre a performance econômica. Para o sistema de segurança em questão, a modelagem markoviana foi escolhida como abordagem de confiabilidade. O uso de controladores lógicos programáveis CLPs em SIS cresceu significativamente a partir da década de <NUMBER>, mas o material registra que houve resistência de órgãos regulamentadores e seguradoras ao emprego de CLPs em substituição aos sistemas tradicionais a relés. Ainda assim, os CLPs aparecem como base da supervisão e da lógica de operação remota dos sistemas descritos.

**Parada e desconexão de emergência**

Os conectores de emergência integram o ESD e podem ser desconectados manualmente ou automaticamente. O sistema é acionado quando há vazamento ou quando o navio se movimenta além dos limites do envelope de operação dos braços, com o objetivo de minimizar derramamento. Os braços associados à transferência também dispõem de sistema QCDC com a finalidade de minimizar vazamentos. Essa lógica mostra que a parada de emergência e a desconexão são tratadas como medidas de contenção imediata frente a perda de contenção ou desvio de posicionamento do navio em relação aos limites operacionais.

A sala de controle utiliza PLCs com Scada para realizar e supervisionar remotamente as operações do píer. Os sistemas de emergência dos navios são conectados ao sistema supervisório por uma interface navio-píer ship-to-shore link, provida de alarmes que alertam os operadores quanto à necessidade de acionamento do ESD. Essa mesma interface também é usada como transmissor de dados ship-to-shore data communication link ou SSL.

**Resposta a falhas e desvios operacionais**

A resposta a condições anormais inclui o monitoramento de acúmulo de água em bacia por sensor de nível, com descarte por bombas. O procedimento deve ser observado porque a presença de água durante a transferência de GNL pode ocasionar rápida vaporização do produto, fenômeno identificado como Rapid Phase Transition RPT. A purga das linhas de GNL e de retorno de vapor é direcionada a um vaso de purga knockout drum KOD. Encerrada a transferência, ou quando for atingido determinado volume de líquido no vaso, o produto é descarregado para o navio. Se a pressão de vapor atingir o valor máximo aceitável, a válvula de segurança do vaso abre e envia gás ao vent. Essas funções evidenciam resposta automática ou procedural a desvios de inventário e pressão.

**Integridade de linhas e equipamentos**

As linhas de transferência que interligam os braços têm diâmetro externo de <NUMBER> e foram fabricadas em aço inoxidável adequado às baixas temperaturas envolvidas. O isolamento térmico foi feito com espuma de vidro ou poliuretano expandido, conforme a localização, e protegido por placas de alumínio contra danos mecânicos e intempéries. As unidades hidráulicas e acumuladores são responsáveis pelo acionamento dos braços de carregamento e descarregamento, compondo um subsistema crítico para disponibilidade da transferência e para a execução das manobras exigidas pelo ESD.

**Prevenção de atmosfera explosiva, poluição e incêndio**

O vent possui duas linhas, uma de alta pressão proveniente do sistema de gás natural gerado na regaseificação do GNL e outra de baixa pressão proveniente do KOD. Ambas possuem injeção de nitrogênio na extremidade superior para evitar formação de atmosfera explosiva e válvulas de retenção para impedir penetração de ar. Na prevenção de derramamentos, a lógica central é minimizar vazamentos por meio do ESD, da desconexão manual ou automática e do QCDC nos braços.

Na resposta a incêndio, ambos os píeres utilizam água do mar e cada área é coberta por dois canhões monitores instalados em torres, com uso de pó químico para combate a incêndios em poças e jatos de GNL. A integração entre detecção, alarmes, atuação dos operadores e sistemas automáticos aparece como elemento essencial da resposta a emergências durante a transferência.