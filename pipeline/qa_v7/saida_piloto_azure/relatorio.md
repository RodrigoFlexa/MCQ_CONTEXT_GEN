# Piloto QA v7: perguntas a partir do inventário

Gerador gpt-5-4-petrobras:low, juiz gpt-5-2-petrobras:medium. 160 questões geradas, 97 aprovadas (61%). Tempo 13.5 min. Chamadas 368, tokens de entrada 1,668,794, de saída 382,253.

O nível é o tipo pedido ao gerador (sem avaliador de dificuldade no loop).

| Tipo | geradas | aprovadas | corrigidas |
|---|---:|---:|---:|
| facil | 40 | 27 | 11 |
| media | 40 | 26 | 17 |
| dificil_A | 40 | 25 | 19 |
| dificil_B | 40 | 19 | 18 |

Motivos de reprovação: suporte (56), correcao_tecnica (11), jurisdicao (10), sem_generalizacao (7), codigo:depende_do_material (5), codigo:referencia_alternativas (4), escopo (3)
Lotes com falha ou filtro de conteúdo: 0

## Sistemas de Lastro, Estabilidade, Ancoragem e Posicionamento, Offloading e Tanques de Carga

### Operação de Offloading

**facil · REPROVADA: correcao_tecnica, suporte, escopo**  
_Nota(s): Falhas de propulsão, energia, controle e apoio que degradam a manobrabilidade do aliviador no offloading_

**P:** Na operação de offloading, que quadro de consequências operacionais caracteriza a degradação de propulsão, geração elétrica ou controle automático do navio aliviador?

**R:** Essas degradações são tratadas como precursoras de perda de manobrabilidade e aumento do risco operacional. A perda de propulsão do aliviador tende a causar atraso operacional e pode evoluir para colisão se o problema persistir. A parada do sistema diesel-gerador também foi associada a atraso operacional e à possibilidade de colisão caso a operação prossiga. Já falhas de controle automático, como erro de programação, podem produzir manobras arriscadas durante o offloading, mesmo sem uma quebra mecânica completa.

**media · APROVADA**  
_Nota(s): Falhas de propulsão, energia, controle e apoio que degradam a manobrabilidade do aliviador no offloading_

**P:** Durante o offloading, a equipe identifica quatro anomalias possíveis: falha genérica de equipamento, falha no cilindro do sistema de conexão, problema de thruster e problema de satélite GPS. Qual é a resposta operacional indicada para cada uma?

**R:** Para falha genérica de equipamento, a indicação é desconectar, desamarrar e afastar o aliviador da unidade de produção, com ativação da parada de emergência da transferência; na prática, isso significa abortar o offloading. Para falha no cilindro, a saída indicada é executar desconexão, desamarração e afastamento utilizando o sistema de posicionamento dinâmico. Problema de thruster também requer abortar a operação de offloading. Já diante de problema de satélite GPS, a ação indicada é verificar os avisos aos navegantes sobre informações de satélites.

**dificil_A · APROVADA**  
_Nota(s): Perda de posição do navio aliviador e mecanismos de colisão no offloading com FPSO_

**P:** Durante um offloading, o aliviador sai do envelope seguro em três ocorrências distintas. Na primeira, a excursão vem junto com perda de alimentação para vários sistemas, inclusive bombas de óleo lubrificante do motor principal, seguida de parada do motor principal, navegação e manobra. Na segunda, os sistemas de navegação e controle permanecem energizados, mas há perda de propulsão e o navio passa a responder com atraso. Na terceira, energia e propulsão seguem disponíveis, porém após ajuste no automático ou avaliação inadequada da manobrabilidade o navio corrige na direção errada ou de forma incompatível com a condição. Qual é o diagnóstico mais compatível para cada ocorrência?

**R:** Primeira ocorrência: o diagnóstico mais compatível é blackout em cascata iniciado por falha do motor de combustão auxiliar, porque a assinatura observável é a perda elétrica ampla, atingindo bombas de óleo lubrificante, motor principal, navegação e manobra. Segunda ocorrência: o quadro é mais compatível com perda isolada de propulsão; ela tende a aparecer primeiro como atraso operacional, elevando o risco de colisão se persistir. Terceira ocorrência: o diagnóstico mais provável é erro de programação do sistema automático ou erro de julgamento das condições de manobrabilidade, pois o navio continua energizado e com capacidade propulsiva, mas responde de forma inadequada. Em offloading, distinguir essas assinaturas importa porque o mesmo desvio de posição pode evoluir para cenários de colisão por mecanismos diferentes, mesmo quando o sintoma inicial é apenas a saída do envelope seguro.

**dificil_B · REPROVADA: suporte · corrigida**  
_Nota(s): Teste de estanqueidade, pressurização e partida da transferência no offloading; Ensaios e verificações de integridade aplicáveis ao offloading; Integridade mecânica e contenção na interface de offloading: manifold, conexões, mangotes, QRF e linhas_

**P:** Após a conexão para offloading, a linha passa por teste de estanqueidade antes do bombeio de óleo. O resultado do teste não confirma claramente a integridade e, na etapa seguinte, durante a circulação de água na maior vazão praticável, aparece contrapressão de bombeio anormal. Considerando que a perda de contenção pode estar em manifold, conexões, QRF, carretel e terminações do mangote, qual diagnóstico diferencial deve orientar a decisão operacional imediata?

**R:** A decisão imediata é não iniciar o bombeio de óleo. Após a conexão, a sequência prevista é teste de vazamento na linha de mangueiras, depois circulação de água e só então envio de óleo. Se o teste de estanqueidade não confirma a contenção, permanece suspeita de vazamento na linha ou na interface de transferência, incluindo manifold, conexões, QRF, carretel e terminações do mangote. Já a contrapressão anormal durante a circulação de água na maior vazão praticável é indício de obstrução parcial da linha. Portanto, os sinais devem ser lidos de forma distinta: resultado anômalo no teste aponta para possível perda de contenção; contrapressão anormal na água aponta para restrição de escoamento. O ensaio deve ser encerrado com despressurização controlada, respeitando a taxa máxima especificada.

### Operação de tanques de carga, lastro, sistema gás inerte, ventilação e estabilidade

**facil · REPROVADA: suporte**  
_Nota(s): Uso do sistema de lastro para controlar calado, trim, banda e flutuabilidade_

**P:** Em um FPSO monohull, para que o sistema de lastro é usado durante o carregamento e a descarga de óleo cru em relação ao calado?

**R:** Ele é usado para compensar a variação de calado à medida que o óleo cru é carregado ou descarregado, mantendo a condição operacional da unidade sob controle.

**media · APROVADA**  
_Nota(s): Uso do sistema de lastro para controlar calado, trim, banda e flutuabilidade_

**P:** Durante uma manobra de lastro, a equipe consegue reduzir um trim indesejado e eliminar a banda de um FPSO. Qual critério adicional deve ser atendido para que essa correção seja tecnicamente aceitável?

**R:** A correção só é tecnicamente aceitável se, além de levar a unidade a uma condição segura e nivelada, a redistribuição de água mantiver os carregamentos estruturais dentro dos limites permissíveis, incluindo shear forces, bending moments e tensões torsionais. Ou seja, não basta corrigir a atitude da unidade; é necessário fazê-lo sem comprometer a integridade estrutural.

**dificil_A · APROVADA · corrigida**  
_Nota(s): Barreiras de contenção e intertravamentos de segurança em carga, offloading e gás inerte_

**P:** Durante uma operação de descarga para navio aliviador, a equipe identifica uma anormalidade no sistema de offloading com potencial de risco, avaria ou poluição enquanto a transferência ainda está em andamento. Um grupo quer continuar a operação até entender a origem; outro defende agir de imediato. Qual deve ser a resposta operacional inicial e como ela se relaciona às barreiras e aos shut-offs previstos para o offloading?

**R:** A resposta operacional inicial deve ser interromper imediatamente a transferência, antes de qualquer outra providência. Esse é o critério indicado quando há defeito ou anormalidade com potencial de risco, avaria ou poluição durante recebimento ou descarga. Essa decisão se relaciona à preservação da contenção porque, no offloading, a barreira não está apenas na integridade física de tubulações, válvulas e penetrações associadas aos sistemas de carga, blanketing e offloading, mas também nos shut-offs previstos para minimizar a perda de hidrocarbonetos. Para os cenários de ruptura de mangueira, ruptura de tubulação ou desconexão da mangueira por saída de posição do navio aliviador, esses shut-offs podem incluir isolamento manual, válvulas de fechamento remoto, parada das bombas de carga e breakaway couplings.

**dificil_B · APROVADA**  
_Nota(s): Reconfiguração de drenos e transferências na indisponibilidade de tanques slop; Inventário de tanques por medição remota e conferência independente para estabilidade; Planejamento e verificação da condição de lastro com documentos de bordo e software de estabilidade_

**P:** Com o slop de bombordo indisponível, a equipe reconfigurou temporariamente drenos e transferências. Após a manobra, os níveis remotos dos tanques indicam condição aceitável no programa de estabilidade, mas o trim observado e a resposta de alguns tanques não coincidem com o previsto. Antes de iniciar nova transferência de carga e um ajuste de lastro, qual deve ser a decisão técnica prioritária e por quê?

**R:** A prioridade é interromper a aprovação da próxima manobra com base apenas no software e confirmar independentemente o inventário real dos tanques antes de qualquer nova transferência ou ajuste de lastro. Em line-up contingente, o caminho hidráulico aberto pode não ser o presumido: com slop indisponível, drenos podem ser redirecionados para outro slop ou para o 4C, e certos headers podem até drenar carga para o slop de bombordo se usados inadequadamente. Como o programa recebe dados automáticos dos tanques, mas sua confiabilidade depende de verificação manual regular e de entradas operacionais corretas, uma condição aparentemente aceitável pode estar mascarando migração real de conteúdo. Só depois de reconciliar medições e atualizar a condição no programa é que a nova sequência deve ser simulada e liberada, porque desviar do plano sem reavaliação pode gerar esforços estruturais excessivos.

### Sistema de ancoragem, manutenção e monitoramento da posição

**facil · APROVADA**  
_Nota(s): Gestão das cargas de amarração e resposta à falha de linhas em mau tempo_

**P:** Em uma unidade ancorada, o que a perda de uma única linha de ancoragem exige em termos de continuidade operacional, e de quais fatores depende uma eventual retomada?

**R:** A perda de uma linha de ancoragem deve ser tratada como condição para cessação imediata das operações. A retomada não é automática nem pode ser justificada apenas pela existência de outras linhas remanescentes. Ela deve ser reavaliada conforme a linha que falhou, as condições meteorológicas presentes e previstas e a verificação de conformidade com os parâmetros de projeto da unidade e do sistema de ancoragem.

**media · REPROVADA: correcao_tecnica, suporte · corrigida**  
_Nota(s): Gestão das cargas de amarração e resposta à falha de linhas em mau tempo_

**P:** Durante a aproximação de uma tempestade, a unidade tem recurso para ajustar as tensões de amarração, mas esse ajuste não é usado. Ao mesmo tempo, os limites máximos operacionais dos guinchos não estão prontamente disponíveis na sala de controle. Como essa combinação pode contribuir para a ultrapassagem das tensões operacionais?

**R:** Essa combinação contribui porque reúne duas falhas registradas no caso. Havia procedimento para ajustar as tensões quando era previsto tempo particularmente pesado, mas, no caso citado, esse ajuste nunca era feito. Além disso, os limites máximos operacionais, que não podiam ser excedidos, não estavam disponíveis na sala de controle, o que retardava sua obtenção. No mesmo contexto de tempestade de inverno, acreditava-se que uma ou duas tensões máximas operacionais tinham sido excedidas. Assim, deixar de usar o ajuste previsto para tempo severo e não ter acesso imediato ao limite operacional na sala de controle favorece a ultrapassagem dessas tensões.

**dificil_A · APROVADA**  
_Nota(s): Critérios de dimensionamento e verificação de linhas e fundações de ancoragem sob cargas estáticas, dinâmicas e de avaria_

**P:** Uma unidade com ancoragem Taut-Leg será reavaliada após aumento das cargas ambientais. A fundação prevista é uma estaca torpedo, e a análise preliminar indica solicitação combinada horizontal-vertical nas linhas, com necessidade de verificar também a hipótese de ruptura de uma linha. Nessa condição, quais verificações são mandatórias no dimensionamento, qual mecanismo resistente tende a governar a fundação e por que a análise por elementos finitos passa a ser necessária?

**R:** Devem ser verificadas as condições de carregamento estática e dinâmica, tanto com todas as linhas íntegras quanto na hipótese de uma linha rompida. Além disso, a fundação não deve ser avaliada só pela magnitude da carga, porque o mecanismo de falha também depende da direção de aplicação do esforço, e cargas cíclicas e transitórias precisam ser consideradas para evitar deformações excessivas e vibrações na plataforma. Em Taut-Leg, a grande inclinação da linha transmite componentes verticais relevantes à fundação; por isso, a resistência ao arrancamento axial tende a governar o dimensionamento. A análise por elementos finitos torna-se necessária porque a estaca torpedo está sob carregamento combinado horizontal-vertical, e a capacidade nesse caso precisa ser avaliada considerando explicitamente essa combinação de componentes, não apenas uma resultante escalar.

**dificil_B · APROVADA · corrigida**  
_Nota(s): Monitoramento integrado de posição da unidade, resposta estrutural e integridade de risers/linhas; Impacto do offset e dos movimentos da unidade amarrada na integridade de risers; Station keeping: tendências e indicadores além do offset para detectar degradação antes da perda de posição_

**P:** Um FPSO ancorado permanece dentro do limite operacional de offset. Nas últimas horas, porém, aumentaram a assimetria das excursões, a variação de aproamento, os movimentos do topo e os sinais de inclinação/deformação em trechos de topo de alguns risers, sob estado de mar com swell e vento. A equipe propõe manter a operação porque o critério geométrico principal não foi violado. Qual decisão técnica é mais consistente e por quê?

**R:** A operação não deve ser tratada como automaticamente aceitável apenas porque o offset global segue dentro do limite. A decisão mais consistente é elevar a condição para avaliação integrada e adotar mitigação operacional proativa conforme alarmes e tendências. Isso porque offset seguro da unidade não equivale, por si só, a condição segura dos risers: mesmo dentro desse limite, outros parâmetros precisam ser monitorados, e valores fora das faixas-limite de inclinação, deformação ou esforços inferidos podem indicar ameaça à integridade. Além disso, os movimentos da plataforma contribuem para a fadiga do riser, e esforços dinâmicos oscilatórios podem levar a compressão momentânea acima do admissível. Portanto, a continuidade da operação deve considerar conjuntamente ambiente em tempo real, movimentos da unidade, resposta estrutural dos risers e tendência das variáveis, e não o offset isolado.

## Operações submarinas, poços, risers e equipamentos submarinos

### Operações submarinas, poços, manifolds, PLEM e PLET

**facil · APROVADA**  
_Nota(s): Monitoramento operacional, envelope de segurança e gestão de integridade em sistemas subsea de poços e linhas associadas_

**P:** O que significa operar um sistema submarino dentro do envelope de segurança, e qual deve ser a consequência operacional quando ocorre um desvio desse envelope?

**R:** Significa manter o sistema submarino dentro dos limites operacionais definidos em projeto para sua operação segura. Na prática, isso requer acompanhar as variáveis operacionais com limites de alarme e análise de tendência, de modo a verificar se o sistema permanece nas condições previstas de operação. Quando ocorre um desvio do envelope de segurança, a resposta operacional não é apenas corrigir a condição observada: o desvio deve ser registrado e investigado, e o operador deve gerar, implementar e documentar medidas para minimizar a recorrência. Se alguma variável não puder ser acompanhada pelo sistema supervisório, ainda assim devem existir procedimentos de segurança e mecanismos de controle e monitoramento capazes de identificar anormalidades.

**media · APROVADA · corrigida**  
_Nota(s): Monitoramento operacional, envelope de segurança e gestão de integridade em sistemas subsea de poços e linhas associadas_

**P:** Um operador de poços submarinos dispõe de histórico suficiente para identificar tendências em determinados equipamentos e observa, em alguns deles, uma relação muito alta entre manutenção preventiva e corretiva. Como uma estratégia de manutenção baseada em risco deve usar essas informações para ajustar a frequência das intervenções?

**R:** A estratégia de manutenção baseada em risco deve definir e documentar a frequência e a periodicidade das atividades de manutenção, podendo usar uma matriz de avaliação. Essa frequência pode ser ajustada quando houver histórico suficiente para identificar tendências observáveis. Também pode ser revista quando a razão entre tarefas preventivas e corretivas estiver muito alta ou muito baixa. Portanto, o ajuste da frequência das intervenções deve considerar tanto as tendências identificadas no histórico quanto o comportamento da relação entre manutenção preventiva e corretiva.

**dificil_A · APROVADA · corrigida**  
_Nota(s): Uso de VOR/ROV versus mergulho em inspeção e intervenção de linhas submarinas_

**P:** Uma linha submarina apresentou dúvida sobre sua condição externa após alteração operacional. A equipe só consegue avaliar a parte aparente do trecho, e a visibilidade da água varia com maré e particulados. Há também a possibilidade de a atividade evoluir para intervenção, expansão ou reparo da linha. Como o escopo deve ser classificado para definir entre mergulho e VOR/ROV?

**R:** Se o objetivo da atividade for apenas inspecionar ou vistoriar o estado do equipamento na parte aparente e acessível da linha, o escopo é compatível com mergulho. Nesse caso, a execução da inspeção fica condicionada às condições visuais da água. Se a atividade envolver intervenção, expansão ou reparos de linhas, o escopo deixa de ser apenas de inspeção e se enquadra nas operações associadas a VOR/ROV. Assim, a classificação técnica deve partir do que a tarefa exige: vistoria da parte aparente e acessível caracteriza inspeção por mergulho; atuação na linha para intervenção, expansão ou reparo caracteriza operação por VOR/ROV.

**dificil_B · APROVADA · corrigida**  
_Nota(s): Instalação, fabricação e controle operacional do sistema submarino: integridade, rastreabilidade e envelope de segurança; Monitoramento de vazamentos, restrições de fluxo e anomalias de integridade em linhas e equipamentos submarinos; Gestão de integridade, fadiga e resposta a anomalias em risers e sistemas submarinos_

**P:** Anos após o comissionamento, a linha entre um manifold e o FPSO passa a exigir maior queda de pressão para a mesma vazão aparente. Houve mudança de GLR e water-cut, e parte do histórico de instalação está incompleto, sem evidência direta de vazamento. Como decidir entre possível dano de instalação, degradação em operação ou incerteza de avaliação, e qual deve ser a resposta de integridade se a linha precisar operar além da vida de projeto?

**R:** A decisão não deve partir do indício hidráulico isolado. Primeiro, a queda de pressão deve ser comparada com referência compatível com a condição atual do fluido, porque ela depende de vazão líquida, GLR e water-cut. Depois, o diagnóstico deve ser fechado com inspeção da linha e do entorno, verificando, quando aplicável, enterramento, ancoragem, dispositivos de proteção, vãos livres, corrosão externa, crescimento marinho, revestimento e proteção catódica. Para investigar hipótese de dano de instalação, devem ser recuperados os registros as built e de fabricação/instalação, incluindo rastreabilidade, qualificação dos executantes e dados de lançamento, como tensão monitorada e controle de dano ao revestimento. Se a linha precisar operar além da vida de projeto e faltarem dados para a avaliação, o operador deve adotar inspeções adicionais, modelagem numérica avançada e dados conservadores antes de sustentar a continuidade operacional.

### Sistema e operação de pull in de risers

**facil · APROVADA**  
_Nota(s): Sequência operacional do pull-in do topo do riser entre PLSV e unidade flutuante_

**P:** Por que é necessária a instalação de uma ferramenta no topo do riser antes do pull-in, e qual é o papel dos cabos de aço nessa etapa?

**R:** A ferramenta no topo do riser é necessária porque ela viabiliza a transferência do topo da embarcação de lançamento para a unidade flutuante onde ocorrerá a conexão. Nessa etapa, os cabos de aço fazem a ligação usada para executar a transferência, normalmente interligando o riser à embarcação de lançamento durante a manobra.

**media · REPROVADA: correcao_tecnica, suporte**  
_Nota(s): Sequência operacional do pull-in do topo do riser entre PLSV e unidade flutuante_

**P:** Em um procedimento de instalação com transferência do topo do riser do PLSV para um FPSO, quais pontos devem ser destacados para essa etapa e como eles delimitam o início da operação?

**R:** Os pontos destacados são o posicionamento do PLET e a máxima aproximação do PLSV ao FPSO. Essa máxima aproximação é definida como a aproximação máxima do topo do riser antes de começar a transferência para o FPSO. Portanto, o início do pull-in fica delimitado por essas condições do procedimento: o posicionamento do PLET deve estar conforme previsto e a transferência só deve começar quando a condição de máxima aproximação tiver sido atingida.

**dificil_A · APROVADA · corrigida**  
_Nota(s): Posicionamento e controle de heading do FPSO na interface com turret, risers e umbilicais_

**P:** Durante o planejamento do pull in de risers, a equipe compara duas arquiteturas de FPSO com turret. Na primeira, a unidade gira naturalmente em torno de um turret à vante. Na segunda, o turret fica mais ao meio do casco e a manutenção de aproamento e posição depende de thrusters comandados por Dynamic Positioning (DP). Qual é a diferença funcional mais relevante entre essas arquiteturas na forma de controlar a interface com os risers durante a operação?

**R:** Na arquitetura com turret à vante, a unidade se orienta passivamente por weathervaning ao redor do ponto de conexão. Assim, a rotação do casco em relação ao campo decorre predominantemente do alinhamento natural da embarcação, enquanto o turret mantém a conexão com risers e umbilicais mesmo com o giro do FPSO. Já na arquitetura com turret mais ao meio, heading e posição deixam de resultar principalmente desse alinhamento passivo e passam a ser mantidos ativamente. Nessa condição, o sistema DP usa informações de sensores e comanda direção e potência dos thrusters para corrigir posição e aproamento da unidade. Portanto, a diferença funcional central é que, em um caso, a interface com os risers convive com rotação passiva da unidade em torno do turret; no outro, essa interface é mantida com correções ativas de heading e posição pelo conjunto DP-thrusters, conforme necessário.

**dificil_B · REPROVADA: correcao_tecnica, suporte, sem_generalizacao**  
_Nota(s): Interfaces críticas entre turret, amarração e risers durante aproximação, pull-in e operação conectada em FPSOs; Perda de posição ou de heading em FPSO com turret: cadeia causal até torção de amarrações, contato com risers e enquadramento como elemento crítico de segurança; Perda de posição, amarração e proteção de risers em operações de pull in sob mau tempo_

**P:** Durante o pull-in de um riser em FPSO monocaio com turret e heading assistido por thrusters, ocorrem perdas de heading curtas, sempre recuperadas, enquanto vento e mar aumentam. O espaçamento geométrico entre amarrações e risers é bom em condição normal, mas já houve rotação anormal do conjunto. A operação deve ser tratada como oscilação aceitável ou como início de cenário crítico, e qual decisão operacional é mais adequada?

**R:** Deve ser tratada como degradação de margem, com potencial de evoluir para cenário crítico, não como oscilação automaticamente aceitável. Em FPSO com turret e thrusters, a perda de heading sob carregamento ambiental pode iniciar torção do turret e das amarrações; se o giro relativo esperado não ocorrer, a torção acumulada pode reduzir folgas até contato mooring–riser, mesmo quando o espaçamento geométrico é adequado em condição normal. Perdas de heading recuperadas indicam que a condição extrema ainda foi evitada, mas já sinalizam redução da capacidade de manter heading/posição com segurança. Assim, a decisão correta é suspender preventivamente o pull-in enquanto a unidade ainda estiver dentro dos limites, porque o mau tempo e a recorrência dos desvios reduzem a barreira de integridade e podem ainda aumentar a exposição em weather side working. Se houver saída dos limites operacionais, falha de amarração ou suspeita de contato/dano, a decisão passa a abortar e verificar a integridade antes de retomar.

## Produção e Processo (Medição Fiscal e Sistema de Alívio)

### Compressão de Gás

**facil · REPROVADA: suporte · corrigida**  
_Nota(s): Controle operacional e sensibilidade dos compressores às condições do gás em sistemas offshore_

**P:** Qual é a função do compressor sobre o gás produzido e por que esse aumento de pressão e/ou densidade é necessário para encaminhá-lo às diferentes rotas de processo de uma planta offshore?

**R:** A função do compressor é transferir ao gás a energia recebida do acionador, como motor ou turbina, elevando seu estado de energia por aumento de pressão e/ou de densidade. Isso torna viável o escoamento do gás e o processamento subsequente. Em uma planta offshore, essa elevação de energia permite que o gás saia de uma condição de sucção e siga para as rotas de utilização e tratamento previstas no processo. Como a aplicação da máquina define a variável principal de controle, o serviço do compressor é ajustado para sustentar a necessidade operacional daquela rota; em compressores de gás úmido, isso é feito com foco na pressão de sucção.

**media · APROVADA · corrigida**  
_Nota(s): Controle operacional e sensibilidade dos compressores às condições do gás em sistemas offshore_

**P:** Em um trem de compressão offshore, a pressão de sucção deve permanecer estável, mas a vazão em cada estágio precisa acompanhar a condição de operação da máquina. Qual é a diferença funcional entre variar a rotação, estrangular a sucção e usar reciclo por estágio nesse controle?

**R:** A variação de rotação é usada para manter a pressão de sucção sem muita oscilação. O estrangulamento na sucção também pode ser empregado com a mesma finalidade, por meio de uma válvula de throttle instalada a jusante do separador de entrada de baixa pressão. Já o reciclo por estágio atua na vazão de sucção de cada estágio: controladores de vazão usam um setpoint variável que depende da rotação da máquina e manipulam válvulas de reciclo para manter a vazão próxima desse valor. Assim, rotação e throttle são estratégias aplicadas à estabilidade da pressão de sucção, enquanto o reciclo por estágio é a estratégia usada para corrigir a vazão vista por cada estágio em torno do setpoint de operação.

**dificil_A · REPROVADA: correcao_tecnica, suporte**  
_Nota(s): Influência das pressões de sucção e de descarga na aplicação e no controle operacional da compressão de gás_

**P:** Após uma alteração na lógica de controle do trem de compressão, a unidade passou a apresentar instabilidade. A pressão de sucção permanece no patamar habitual, mas a pressão de descarga alterna episódios de valor alto e baixo. Sem indício novo de mudança de regime do processo, qual deve ser a ação prioritária: focar a condição do sistema, a estratégia de controle ou a adequação do tipo de compressor à aplicação? Justifique pela variável afetada.

**R:** A prioridade deve ser a estratégia de controle, centrando o diagnóstico na pressão de descarga. Nesse trem, pressões alta e baixa na admissão e na descarga são tratadas como entradas formais de identificação, diagnóstico e procedimentos corretivos; portanto, a primeira decisão correta é usar a variável anormal e o lado afetado como critério primário de intervenção. Como a sucção permanece estável e a anomalia está localizada na descarga, o quadro deve ser lido primeiro como desvio associado à resposta do controle nessa variável, e não como perda genérica de desempenho. Também não é a melhor prioridade concluir, de imediato, por inadequação do tipo de compressor à aplicação, porque o padrão observado ainda está organizado pela variável de descarga dentro do sistema de controle.

**dificil_B · REPROVADA: suporte**  
_Nota(s): Inspeção em revisões de compressores centrífugos e mitigação de vibração/pulsação em tubulações associadas; Arquiteturas de selagem em compressores multestágio e controle de vazamentos; Vibração e pulsação em compressores e tubulações associadas: mecanismos, danos, fadiga e mitigação_

**P:** Um compressor centrífugo multestágio foi retirado para revisão após aumento de vazamento e histórico de vibração elevada nas linhas conectadas. Na abertura da carcaça, antes da remoção do rotor, surgem marcas de contato em regiões de selagem interna, enquanto a tubulação associada já exigia reforço de suportação por resposta vibratória. Qual hipótese causal deve ser priorizada e que evidências técnicas precisam ser preservadas e correlacionadas para não tratar a selagem como causa primária isolada?

**R:** A hipótese prioritária é que a falha de contenção na selagem seja consequência de vibração anormal do eixo e da interação dinâmica entre compressor e tubulações, não necessariamente defeito primário do selo. Danos em selagem labirinto ou mecânica são comumente associados a contato mecânico provocado por vibração anormal do eixo. Por isso, na abertura devem ser preservados e registrados o estado interno do rotor, difusores, planos de junta e as folgas entre partes fixas e móveis antes da retirada do rotor, porque essa evidência se perde depois. Em paralelo, o histórico de vibração das linhas, a necessidade de suportação mais rígida e a possibilidade de fadiga ou afrouxamento em conexões indicam que a investigação deve integrar máquina e tubulação. A priorização técnica é correlacionar indícios internos de contato com o comportamento vibratório externo, antes de concluir por troca de selo como solução suficiente.

### Medição Fiscal de óleo, medição fiscal de gás e transferência de custódia em operações de offloading

**facil · APROVADA**  
_Nota(s): Comunicação de falhas do sistema de medição e efeitos regulatórios sobre não conformidade e recálculo da produção_

**P:** Qual é a função da notificação de falha do sistema de medição na passagem de uma anomalia técnica para a avaliação da confiabilidade dos dados de produção?

**R:** Ela formaliza a ocorrência de falha como evento tratável no sistema de gestão e de fiscalização da medição, ligando a detecção técnica à análise da confiabilidade dos dados informados. Isso é relevante porque a veracidade desses dados é objeto de fiscalização, e, quando a falha ou a não conformidade pode ter afetado os resultados, podem ser instaurados procedimentos de recálculo da produção. A notificação, portanto, não serve apenas para registrar um problema de instrumento; ela funciona como gatilho regulatório para verificar se os volumes declarados permanecem confiáveis.

**media · APROVADA**  
_Nota(s): Comunicação de falhas do sistema de medição e efeitos regulatórios sobre não conformidade e recálculo da produção_

**P:** Após identificar possível inconsistência em volumes já informados, a equipe precisa reconhecer quais eventos podem abrir processo de recálculo da produção e qual deles tende a aparecer com mais frequência. Quais são esses gatilhos?

**R:** Os processos de recálculo podem ser abertos por notificação de falha do sistema de medição, inspeções, declarações das concessionárias, denúncias e validação da produção. Entre esses gatilhos, as notificações de falha do sistema de medição tendem a representar a maior parte dos casos. Na prática, isso torna a comunicação formal de falhas um canal recorrente de entrada para revisão da confiabilidade dos volumes já informados.

**dificil_A · REPROVADA: suporte, codigo:referencia_alternativas · corrigida**  
_Nota(s): Configuração do sistema de medição para transferência de custódia em offloading de FPSO e variáveis para cálculo do volume compensado_

**P:** Durante a revisão da medição de transferência de custódia no offloading de um FPSO, a equipe avalia duas alternativas: implantar monitoração online contínua de vazão, pressão estática e temperatura, ou manter apenas pressão estática medida na parede do duto e temperatura do escoamento por restrição de CAPEX. Qual decisão técnica é mais consistente nesse contexto e em que condição os valores online podem ser usados como representativos da transferência ao longo do tempo?

**R:** A decisão tecnicamente mais consistente é balancear rigor metrológico e viabilidade econômica. Se o investimento em transmissores e sistemas automáticos em tempo real se justificar, a monitoração online contínua de vazão, pressão estática e temperatura melhora o acompanhamento do escoamento. Porém, para que esses valores online sejam representativos da transferência ao longo do tempo, é necessário demonstrar estabilidade operacional, com manutenção de pressão, temperatura e vazão.

Se o CAPEX não se sustenta, limitar a instrumentação à pressão estática na parede do duto e à temperatura do escoamento continua consistente, porque esse é o conjunto mínimo requerido para servir de base ao cálculo do volume compensado. Nessa escolha, a estratégia de medição passa a depender menos de uma representação online completa e mais da correta compensação do volume. Em qualquer caso, a medição de custódia é um sistema integrado, não apenas um medidor de vazão.

**dificil_B · REPROVADA: suporte**  
_Nota(s): Projeto, configuração e instalação do sistema de medição fiscal; Calibração, incerteza e rastreabilidade metrológica dos sistemas de medição fiscal de óleo; Requisitos metrológicos e configuração do sistema de medição fiscal e de transferência de custódia_

**P:** Em uma operação de offloading, a linha de medição fiscal de óleo passou a apresentar desvio recorrente de volume, sem alarme no medidor principal. Houve troca de trecho de tubulação próximo ao medidor, e a equipe dispõe de calibração anterior feita fora das condições usuais de campo. Qual diagnóstico deve ser priorizado para diferenciar causa de instalação de causa de calibração insuficientemente representativa, e por quê?

**R:** Deve-se verificar os dois eixos em sequência técnica, sem aceitar a calibração anterior como prova suficiente. Primeiro, confirmar se a instalação preserva as condições hidráulicas consideradas no dimensionamento e na calibração: trechos retos, diâmetro, espessura e rugosidade influenciam o perfil de escoamento e podem introduzir erro sistemático mesmo sem falha aparente do medidor principal. Depois, avaliar se a calibração representa as condições reais de operação, porque a confiabilidade metrológica exige ensaio em condições muito similares às de campo, com incerteza formalmente estimada e rastreabilidade. Se a calibração foi obtida fora de vazão, pressão, temperatura, viscosidade ou densidade representativas, o fator de calibração pode não sustentar o desempenho em serviço. O ponto central é que o resultado fiscal vem do sistema completo, incluindo instalação, instrumentos auxiliares, cálculo e base metrológica, não do medidor isolado.

### Operação de Separadores Trifásicos

**facil · REPROVADA: suporte, sem_generalizacao**  
_Nota(s): Controle coordenado de nível e interface nas saídas líquidas do separador trifásico_

**P:** Qual é a função da válvula da linha inferior de água livre em um separador trifásico e como ela se relaciona com o controle da interface água-óleo?

**R:** A válvula da linha inferior regula a vazão de saída da água livre pelo fundo do separador. Sua abertura não deve responder ao nível total de líquido, mas ao nível da interface água-óleo, porque a variável crítica nessa descarga é a posição da camada de água no fundo do vaso. Assim, quando o controlador de interface atua sobre essa válvula, ele ajusta a retirada de água para manter a interface na faixa desejada e preservar a separação entre as fases líquidas.

**media · REPROVADA: suporte, sem_generalizacao**  
_Nota(s): Controle coordenado de nível e interface nas saídas líquidas do separador trifásico_

**P:** Em um separador trifásico horizontal, a pressão do vaso permanece controlada pela saída de gás no topo, mas os níveis internos começam a se desviar após variação na formação de óleo e água. Como a abertura das válvulas de saída de óleo e de água deve regular as vazões de descarga para manter o inventário líquido e a separação estáveis?

**R:** As correções devem ser feitas pelas válvulas das correntes líquidas, porque são elas que regulam o inventário no vaso. A válvula de saída de óleo deve responder ao controle de nível do líquido para ajustar a vazão dessa fase, enquanto a válvula da linha inferior de água deve responder ao nível de interface água-óleo para ajustar especificamente a vazão de água livre. Esse arranjo mantém os níveis internos compatíveis com a separação e evita deslocamento indevido da interface. A pressão, por sua vez, continua sendo tratada separadamente pela modulação da saída de gás no topo, sem usar as saídas líquidas para compensar desvio de pressão.

**dificil_A · REPROVADA: suporte, escopo**  
_Nota(s): Gestão de integridade de vasos em operação no FPSO: corrosão, inspeção, cadastro de ativos e isolamento para intervenção_

**P:** Um separador trifásico de um FPSO passou a operar de forma recorrente com condições de processo diferentes das previstas no envelope de projeto. Ao mesmo tempo, há atraso de inspeções, histórico incompleto no cadastro do ativo e indicação de deterioração das barreiras anticorrosivas internas. A equipe discute manter o plano prescritivo original porque o vaso continua disponível e sem vazamento. Nesse cenário, o que justifica revisar o regime de inspeção e reforçar a abordagem baseada em risco no sistema de integridade?

**R:** A revisão se justifica porque a combinação de desvio das condições reais de processo, atraso de inspeções, perda de rastreabilidade e deterioração das barreiras anticorrosivas aumenta a incerteza sobre a condição remanescente do vaso e eleva o risco de perda de contenção. Mudanças do processo em relação ao envelope de projeto são um dos principais perigos potenciais para Loss of Containment em FPSO, podendo evoluir para acidente maior se não houver prevenção, detecção e mitigação. Se o sistema admite inspeção prescritiva e/ou baseada em risco, manter o plano original sem reavaliar frequência, escopo e prioridade deixa de ser tecnicamente robusto quando o serviço mudou e o histórico perdeu confiabilidade. Além disso, a continuidade da proteção anticorrosiva precisa ser mantida ao longo da vida operacional, e o descumprimento do planejamento de inspeções já foi associado a insuficiência dessa proteção sem justificativa técnica formal. O caminho prudente é reforçar o controle do ativo e revisar o plano com base no risco.

**dificil_B · APROVADA**  
_Nota(s): Formação de espuma, efeitos operacionais e mitigação no separador trifásico; Controle de níveis e da interface óleo-água em separadores trifásicos: como faixa estreita, espuma, nível alto e variações térmicas degradam a separação; Shutdown e intertravamentos na operação de separadores trifásicos_

**P:** Após mudança no fluido produzido, um separador trifásico passa a apresentar nível instável, alarmes recorrentes de alto nível e indícios de líquido na linha de gás. Em alguns eventos, o alarme sensibiliza a lógica de trip antes de a equipe confirmar aumento real de inventário líquido. Qual encadeamento técnico explica melhor esse comportamento e qual causa deve ser tratada como primária no diagnóstico para evitar carryover e shutdowns indevidos?

**R:** O encadeamento mais provável é formação de espuma no interior do vaso, favorecida por impurezas no líquido e/ou pela natureza do óleo. A espuma ocupa volume útil, reduz a área livre de escoamento do gás, piora a representatividade da medição de nível e aumenta o arraste de líquido para a saída de gás. Assim, um alarme de nível alto pode refletir a presença de espuma tanto quanto um aumento de líquido claro; se o nível total também estiver alto, o carryover para o gás se agrava. Isso explica por que um problema inicialmente de separação pode evoluir para alarme, intertravamento e trip, além de expor compressores a líquido. No diagnóstico, a causa primária a tratar é a espuma, não assumir automaticamente que todo alarme indica apenas inventário excessivo. A mitigação prioritária é evitar operação em nível muito alto e assegurar quebra de espuma no vaso, complementada por remoção de névoa na descarga de gás.

### Operação de Tratadores Eletrostáticos

**facil · REPROVADA: suporte**  
_Nota(s): Acoplamento entre o tratador eletrostático e a carga ao sistema de água produzida_

**P:** Por que o desempenho do tratador eletrostático influencia não só a qualidade do óleo exportado, mas também a carga enviada ao sistema de água produzida?

**R:** Porque a separação no processamento primário precisa atender dois destinos ao mesmo tempo: o óleo e a água. O tratamento de água produzida tem a função de enquadrar essa corrente para descarte, reinjeção ou utilidades, controlando contaminantes como óleo, sais e metais pesados conforme a destinação. Assim, quando a separação a montante não é adequada, o efeito não fica restrito ao teor de água no óleo exportado; ele também altera a quantidade de óleo que segue com a corrente aquosa. Como o sistema de tratamento de água foi projetado para receber, na saída do separador trifásico, água com cerca de 1000 ppm de óleo disperso, um aumento dessa carga pode tirar a operação da condição de projeto e dificultar o enquadramento final da água.

**media · REPROVADA: suporte**  
_Nota(s): Acoplamento entre o tratador eletrostático e a carga ao sistema de água produzida_

**P:** Em uma unidade, a água produzida piora de qualidade e passa a exigir maior esforço do tratamento, mas o óleo de exportação ainda permanece dentro da especificação. Qual interpretação operacional é mais adequada para esse quadro?

**R:** A interpretação mais adequada é suspeitar de desvio de separação a montante, no separador trifásico e/ou no tratador eletrostático, com aumento da parcela de óleo que está seguindo pela corrente aquosa. O fato de o óleo de exportação ainda atender à especificação não elimina o problema, porque o tratamento de água produzida tem objetivo próprio: enquadrar a água para descarte, reinjeção ou utilidades, controlando contaminantes. Se mais óleo passar para a água, a carga de entrada no sistema de tratamento aumenta. Isso é crítico porque esse sistema foi projetado para operar com água contendo, na saída do separador trifásico, cerca de 1000 ppm de óleo disperso, e não para receber cargas de óleo bruto com baixa diluição na água. Portanto, a piora da água pode aparecer antes de um desvio evidente na exportação do óleo.

**dificil_A · APROVADA**  
_Nota(s): Metas de qualidade do óleo tratado: BS&W e salinidade para exportação no contexto do tratador eletrostático_

**P:** Em um FPSO, a separação primária está operando de forma estável e a equipe entende que isso já deveria bastar para liberar o óleo para exportação. Porém, a corrente exportada ainda precisa passar pelo tratador eletrostático e ser verificada quanto às condições finais da unidade. Por que uma boa separação primária, isoladamente, pode não ser suficiente para considerar o óleo pronto para exportação?

**R:** Porque a condição de exportação não é definida apenas pela separação grosseira das fases na etapa primária. Na unidade offshore, o objetivo do processamento é entregar um óleo tratado e estabilizado que atenda simultaneamente às condições de exportação, incluindo BSW, salinidade e temperatura. Nesse arranjo de processo, o óleo que sai do separador de produção ainda segue para o tratador eletrostático, cuja função é enquadrar o teor de BSW. Portanto, mesmo com boa separação primária, o óleo ainda pode não estar na condição final requerida. Além disso, o produto exportado corresponde ao petróleo tratado da unidade, isto é, ao blend dos fluidos produzidos pelos poços interligados, e essa qualidade final deve ser avaliada no conjunto tratado, não em uma etapa isolada do processo.

**dificil_B · APROVADA**  
_Nota(s): Pré-lavagem com água livre separada no condicionamento da emulsão antes do tratador eletrostático; Operação de tratadores eletrostáticos: pré-lavagem, dessalinização e intensificação da coalescência conforme o teor de água; Metas de qualidade do óleo tratado: BS&W e salinidade para exportação no contexto do tratador eletrostático_

**P:** Em um FPSO, o óleo tratado passa a sair com salinidade acima do esperado e BS&W moderadamente crescente. O tratador eletrostático continua energizado, mas há indício de piora na distribuição de entrada ou na pré-lavagem com água livre previamente separada. Qual degradação deve ser priorizada no diagnóstico e por quê?

**R:** Deve-se priorizar a perda da sequência interna de condicionamento antes da região de maior intensidade de campo, especialmente a pré-lavagem com água livre e a distribuição da alimentação no vaso. Essa etapa remove sais minerais e partículas e já promove coalescência de grande parte da água dispersa; assim, a emulsão chega ao campo elétrico em condição mais favorável à separação. Quando esse condicionamento se deteriora, o campo passa a atuar sobre uma emulsão mais bruta, com pior preparação para as reduções sucessivas da água dispersa ao longo do vaso. Nessa condição, é coerente que BS&W suba e, ao mesmo tempo, a salinidade também piore, porque o tratador integra o atendimento das metas de exportação e não apenas uma desidratação isolada. Portanto, manter o equipamento energizado não basta se a pré-lavagem e a hidráulica interna deixarem de sustentar o mecanismo de separação esperado.

### Operação Geral FPSO

**facil · APROVADA**  
_Nota(s): Sistema logístico offshore e flexibilidade do FPSO no escoamento por alívio_

**P:** Qual é a finalidade da logística offshore para a continuidade operacional de uma unidade marítima?

**R:** Garantir o atendimento da unidade marítima com os insumos e equipamentos necessários à operação contínua. Para isso, a logística offshore organiza um fluxo integrado de materiais e informações entre fornecedores, armazéns, terminais portuários e a própria unidade, de modo que o suporte chegue de forma compatível com a necessidade operacional.

**media · REPROVADA: codigo:depende_do_material · corrigida**  
_Nota(s): Sistema logístico offshore e flexibilidade do FPSO no escoamento por alívio_

**P:** Em uma locação pioneira, foi adotado um FPSO com armazenamento a bordo e exportação por alívio. Como esse arranjo afeta a necessidade de linhas de exportação, oleodutos e manifolds submarinos?

**R:** Nas condições descritas, esse arranjo reduz a necessidade desses elementos de infraestrutura submarina e pode eliminá-los. Segundo o material, a capacidade do FPSO de armazenar e exportar o óleo produzido confere grande flexibilidade e elimina a necessidade de linhas de exportação, oleodutos e manifolds submarinos, sendo uma solução conveniente para locações pioneiras.

**dificil_A · APROVADA**  
_Nota(s): Tratamento de água produzida como mitigação de perdas operacionais em FPSO_

**P:** Em um FPSO de campo maduro, a produção de água aumentou e a estação de tratamento já opera próxima da demanda corrente. Durante a operação, hidrociclone e flotador ficam indisponíveis, e a equipe observa queda na eficiência de separação óleo-água. Por que essa indisponibilidade deve ser tratada como restrição operacional da unidade, e não apenas como perda localizada de qualidade do tratamento?

**R:** Porque, com elevada produção de água, o tratamento deixa de ser periférico e passa a sustentar a capacidade operacional da planta. Nessas condições, a carga de água produzida aumenta a complexidade da operação, e a estação precisa ter capacidade compatível com a demanda corrente. Hidrociclone e flotador atuam de forma complementar em série na remoção do óleo residual: o hidrociclone separa gotículas por diferença de inércia no escoamento em vórtice, e o flotador remove microgotículas remanescentes por borbulhamento e coalescência. Se essas etapas ficam indisponíveis, a capacidade de separação óleo-água cai, não só a “qualidade” de uma corrente isolada. Isso reduz a eficiência global do tratamento justamente quando a carga de água é crítica, tornando o tratamento um limitante da operação da unidade e exigindo verificação ou otimização da capacidade frente à demanda atual.

**dificil_B · APROVADA**  
_Nota(s): Confiabilidade das medições e aderência dos dados à realidade operacional no monitoramento de FPSO; Confiabilidade das informações operacionais para controle do processo e conformidade em FPSO; Diagnóstico de desvios operacionais e falhas de instrumentação/automação em FPSO_

**P:** Em um FPSO com controle manual, uma anomalia persiste por vários turnos. Não há medidores de vazão confiáveis, o TOG online é duvidoso, um tanque usado na prática para água offspec aparece cadastrado como óleo, e a troca de turno não assegurou registro claro de mudanças e isolamentos. No supervisório, parte das mensagens associadas ao desvio não exige ação imediata. Qual diagnóstico deve ser priorizado e que verificações vêm antes de concluir perda real de desempenho do processo?

**R:** Deve-se priorizar o diagnóstico de perda de observabilidade da planta, não assumir de imediato perda real de desempenho. Em controle manual, a falta de vazão confiável e a baixa confiabilidade do TOG já reduzem a capacidade de acompanhar o processo com base objetiva. Se o tanque está documentalmente classificado como óleo, mas recebe água offspec, a interpretação de inventário, risco e comportamento do fluido fica enviesada. A equipe ainda pode estar analisando o desvio com contexto incompleto se a passagem de serviço não transferiu mudanças, isolamentos e condições operacionais. No supervisório, é preciso separar alarme de evento, porque evento não define ação imediata do operador. Antes de concluir por degradação real do processo, devem ser verificados: aderência entre cadastro e recebimento real do tanque, suficiência das medições para controle manual, conhecimento dos limites operacionais seguros pela sala de controle e qualidade do handover.

### Produção, processo e processamento do óleo

**facil · APROVADA · corrigida**  
_Nota(s): Inspeção e prontidão operacional de vasos, trocadores, filtros e tubulações_

**P:** Por que a inspeção interna, antes da partida ou do carregamento do leito, deve verificar ao mesmo tempo a integridade dos componentes internos e a presença de contaminantes em vasos, trocadores, filtros e tubulações?

**R:** Porque a liberação para a etapa seguinte exige confirmar, simultaneamente, que a condição interna do equipamento é compatível com sua função e que não há contaminação que comprometa essa condição. Nos vasos para leitos de zeólitas, isso inclui verificar refratário sem fissuras, furos ou rachaduras e ausência de umidade excessiva ou água acumulada. Nos filtros coalescedores e de particulado, inclui montagem correta dos internos e preservação e integridade dos elementos. Nos trocadores, inclui ausência de resíduos sólidos e depósitos no feixe, no casco e nas linhas de entrada de utilidades. Nas tubulações, especialmente de aço-carbono, inclui ausência de sólidos e resíduos de corrosão. Se houver esses desvios, a condição interna não é adequada para entrada em serviço ou carregamento do leito.

**media · APROVADA**  
_Nota(s): Inspeção e prontidão operacional de vasos, trocadores, filtros e tubulações_

**P:** Na preparação de um sistema de desidratação para operação com gás natural, a inspeção encontra resíduos sólidos e depósitos no feixe do trocador, no casco e nas linhas de entrada de utilidades. Como isso pode degradar o desempenho do trocador antes mesmo da operação contínua?

**R:** Esses achados mostram que o trocador já entra em serviço com condição interna diferente da prevista. Resíduos e depósitos no feixe, no casco e nas linhas de utilidades podem reduzir a área livre de passagem, alterar a distribuição do escoamento e prejudicar a troca térmica. Assim, mesmo antes de uma campanha operacional longa, o equipamento pode apresentar menor eficiência porque o fluido de processo e a utilidade deixam de circular nas condições esperadas de projeto. Por isso, a presença desses materiais é um desvio de prontidão operacional e deve ser tratada antes da partida.

**dificil_A · APROVADA**  
_Nota(s): Separação primária e estabilização do óleo no trem de processo de FPSO_

**P:** Em um FPSO, o óleo chega ao fim do trem ainda inadequado para armazenamento. Ao mesmo tempo, operadores observam oscilações importantes na alimentação dos equipamentos após o primeiro separador. Nesse quadro, como diferenciar indícios de estabilização insuficiente daqueles ligados a golfadas mal amortecidas no separador de produção, e qual efeito principal cada mecanismo tende a impor ao restante da planta?

**R:** O diagnóstico deve separar dois mecanismos. Se o problema dominante for estabilização insuficiente, o indício central é que o óleo não passou por remoção suficiente dos componentes voláteis ainda dissolvidos. Nesse caso, a investigação deve se concentrar nas condições dos estágios de separação em série e na necessidade de aquecimento em pontos do trem, porque a estabilização do óleo depende dessa vaporização dos voláteis para atender à condição de armazenamento. Se o problema dominante for golfada mal amortecida, o indício principal é a transmissão de instabilidade de vazão para jusante. O primeiro separador deve atuar como tanque pulmão, absorvendo flutuações de carga e entregando alimentação mais regular aos equipamentos seguintes. Assim, a consequência típica da estabilização insuficiente é óleo ainda instável na saída; a consequência típica de golfadas mal amortecidas é perda de regularidade operacional e menor previsibilidade de desempenho do restante da planta. As duas causas podem coexistir.

**dificil_B · APROVADA · corrigida**  
_Nota(s): Dessalgação do óleo: mecanismo, integração com a desidratação e impacto na qualidade de exportação; Recirculação de água separada quente dos tratadores eletrostáticos e sua interface com o header de produção; Incrustação mineral por carbonatos no topside: efeito de temperatura, pH, despressurização e suporte à mitigação por modelagem de mistura de águas_

**P:** Em uma unidade, pretende-se reforçar o aquecimento da alimentação do header por recirculação de água separada quente dos tratadores eletrostáticos e aumentar a água de diluição/lavagem para reduzir o sal do óleo de exportação. Na avaliação de incrustação do topside dessa unidade, a recirculação mostrou baixo efeito e não elevou a criticidade, enquanto a água de diluição teve maior impacto no potencial de incrustação. Diante disso, qual decisão deve ser priorizada para conciliar tratamento do óleo e integridade?

**R:** Deve-se manter a estratégia de tratamento do óleo necessária para reduzir sal e BS&W e reavaliar a pior mistura de águas para definir a mitigação química, em vez de limitar a recirculação quente por princípio. A dessalgação depende da adição de água quente e da remoção posterior da fase aquosa por coalescência e decantação no vaso; sem essa separação, o sal permanece associado ao óleo e a especificação de exportação pode não ser atendida. Quanto à incrustação carbonática, temperatura, pH e despressurização importam, mas, no cenário informado, a recirculação teve baixo efeito e não aumentou a criticidade. Assim, a água de diluição, por ter maior impacto no potencial de incrustação, deve pesar mais na definição da pior mistura e da dosagem de inibidor.

### Produtos químicos

**facil · APROVADA**  
_Nota(s): Coagulantes, floculantes e condicionamento químico da emulsão óleo-em-água na água produzida para descarte offshore_

**P:** Qual é o mecanismo básico de atuação dos floculantes em uma emulsão óleo-em-água na água produzida?

**R:** Os floculantes atuam primeiro por adsorção na interface das gotas de óleo dispersas na água. A partir dessa interação, podem promover neutralização de cargas e também formação de pontes inter-particulares entre gotas e outros materiais poluentes. O efeito prático desse mecanismo é a aproximação e aglomeração dessas partículas, favorecendo a formação de flocos ou agregados maiores do que as gotas originalmente dispersas.

**media · APROVADA**  
_Nota(s): Coagulantes, floculantes e condicionamento químico da emulsão óleo-em-água na água produzida para descarte offshore_

**P:** Em uma linha de tratamento de água produzida, após o condicionamento químico passam a aparecer agregados maiores na corrente antes da etapa física seguinte. Que efeito isso tende a ter na separação e como se distinguem os papéis da química e da flotação ou decantação?

**R:** A formação de agregados maiores tende a tornar a separação mais eficiente, porque esses flocos ficam mais facilmente flotáveis ou decantáveis do que o óleo finamente disperso. O papel da química é desestabilizar a dispersão e promover a coagulação e a floculação, gerando agregados maiores. Já a etapa física seguinte, como flotação ou decantação, é a que efetivamente remove esses agregados da corrente. Em arranjos de tratamento de água produzida, isso é coerente com a sequência em que a água passa pela separação inicial, recebe tratamento químico em tanques e só depois segue para a flotação.

**dificil_A · APROVADA · corrigida**  
_Nota(s): Compatibilidade da água de injeção com a formação e mitigação de incrustações por sulfatos_

**P:** Em um campo com injeção de água do mar, a água produzida passa a apresentar fração crescente de água injetada. Nesse mesmo período surgem perda de desempenho no poço, aumento de restrições na coluna de produção e deposição em linhas e equipamentos de superfície, sem mudança informada na estratégia de produção. A hipótese de incompatibilidade entre água injetada e água de formação, com precipitação de sulfatos insolúveis, é consistente com esse quadro? Justifique pelo momento e pelos locais afetados.

**R:** Sim, essa hipótese é consistente com o quadro descrito. Se esse avanço da água injetada na produção corresponder ao breakthrough, isto é, à chegada da água de injeção ao poço produtor, os problemas de incrustação tendem a se tornar mais sérios e o poço deve ser monitorado continuamente. A justificativa técnica é que o contato entre água de injeção e água de formação, sob condições termodinâmicas adequadas, pode formar depósitos insolúveis como sulfato de bário, sulfato de estrôncio e sulfato de cálcio. Também é compatível que os efeitos apareçam em diferentes pontos do sistema, porque a precipitação pode causar restrições desde a região do poço e coluna de produção até linhas e equipamentos de superfície. Portanto, o momento e a distribuição dos sintomas são compatíveis com incrustação por mistura de águas.

**dificil_B · APROVADA**  
_Nota(s): Controle químico de corrosão e de H2S em linhas e equipamentos do processamento de óleo; Compatibilidade entre produtos químicos e efeitos cruzados no desempenho do tratamento em FPSOs; Ensaios e monitoramento de desempenho e compatibilidade de produtos químicos em FPSOs_

**P:** Uma linha de aço-carbono reduziu o problema de H2S após injeção de glioxal, sem formação de sais, mas a corrosão aumentou. A equipe propõe apenas adicionar ou elevar o inibidor e seguir operando. Qual decisão técnica é mais adequada para validar esse pacote químico antes de consolidá-lo na rotina do FPSO?

**R:** A decisão mais adequada é manter a análise focada no meio real e validar o pacote combinado, não aprovar o ajuste por analogia. O glioxal pode remover H2S sem incrustação, mas em baixo pH torna o meio corrosivo para aço-carbono; portanto, a piora não deve ser atribuída só ao H2S residual nem descartada pela ausência de depósitos. O inibidor pode viabilizar o uso do glioxal porque atua por adsorção e estabilização do filme de óxido, com barreira difusional adicional, mas sua eficácia depende de conseguir manter essa proteção no meio tratado. Como combinações químicas podem piorar ou melhorar a proteção, é necessário ensaio representativo com o material e a matriz do sistema, seguido de monitoramento das taxas de corrosão e verificação dos pontos mais críticos em operação antes de consolidar dosagem e continuidade do pacote.

### Sistema de Alívio e Flare

**facil · APROVADA**  
_Nota(s): Comissionamento, testes funcionais, handover e capacitação operacional em sistemas de alívio, despressurização e flare_

**P:** Qual é a função do comissionamento na transição entre construção e operação, e por que o uso de checklists é importante para assegurar aderência ao projeto detalhado?

**R:** O comissionamento faz a ponte entre a montagem física e a prontidão operacional. Sua função é verificar, inspecionar e testar os componentes físicos do empreendimento e, depois, confirmar o funcionamento dos processos antes do início pleno da operação, eliminando erros que poderiam ser transferidos para a rotina operacional. Os checklists são importantes porque estruturam o conjunto de testes para garantir cobertura completa dos componentes do projeto e confirmar que os itens necessários à futura operação estejam disponíveis e operando exatamente como previsto no projeto detalhado. Assim, não basta o equipamento estar instalado; ele precisa demonstrar desempenho compatível com o que foi definido em engenharia para que a liberação para operação tenha base técnica.

**media · REPROVADA: jurisdicao · corrigida**  
_Nota(s): Comissionamento, testes funcionais, handover e capacitação operacional em sistemas de alívio, despressurização e flare_

**P:** Em um vendor package do sistema de flare, a equipe pretende receber o pacote após os testes, mas sem participação ativa de operadores e técnicos no comissionamento com o fornecedor. Por que essa decisão tende a reduzir a capacidade futura de operação e manutenção do sistema?

**R:** Porque, em vendor packages, a participação de operadores e técnicos no comissionamento junto com o pessoal do fornecedor aumenta a familiaridade prática com o equipamento. Essa familiaridade ajuda a equipe a operar e manter o pacote depois do handover. Sem esse envolvimento, cresce o risco de o sistema ser entregue com conhecimento prático limitado para operação e manutenção. Além disso, a transição para a operação deve contar com arranjos adequados de treinamento, que podem começar quando o projeto estiver fixado e os procedimentos operacionais estiverem disponíveis. Se houver mudança no modo de operação, também pode ser necessário retreinamento.

**dificil_A · APROVADA · corrigida**  
_Nota(s): Radiação térmica, dispersão e ignição segura em sistemas de flare e vent_

**P:** Em um FPSO, após modificações no topo da planta, a equipe pretende recolocar em serviço o flare e manter um vent atmosférico existente. Na condição de vento prevista para a partida, há possibilidade de abertura de gás antes da chama estabilizar. Como os estudos de radiação térmica e dispersão devem ser usados para verificar o arranjo da instalação, identificar áreas sensíveis expostas e definir restrições do procedimento de partida do flare?

**R:** Os estudos devem ser usados de forma integrada. A avaliação de radiação térmica serve para verificar se a chama do flare pode atingir pessoas, equipamentos e outros pontos da instalação com níveis relevantes de calor, considerando a geometria da chama e a posição dos pontos avaliados. A avaliação de dispersão deve verificar se gás não ignitado pode alcançar áreas sensíveis, como o deck de processo, tanto a partir do flare quanto do vent atmosférico. Esses resultados apoiam a verificação do arranjo físico e a identificação de exposições que exijam mitigação. Na partida, o procedimento de ignição deve considerar os resultados de dispersão e as condições atmosféricas do momento, especialmente velocidade e direção do vento, para evitar venting não ignitado prolongado. Como há vent atmosférico, também deve existir proteção contra flash-back, como flame arrestor ou dispositivo equivalente.

**dificil_B · REPROVADA: codigo:depende_do_material · corrigida**  
_Nota(s): Influência da contrapressão e do arranjo de descarga na seleção da PSV; Capacidade do sistema de flare, blowdown e vent frente a eventos combinados de sobrepressão; Dimensionamento e verificação dinâmica de PSV com interação com o sistema coletor de alívio_

**P:** Uma PSV de um vaso foi verificada por simulação dinâmica e considerada adequada para o equipamento isolado. Meses depois, em um blackout com abertura simultânea de BDVs e outros alívios para o mesmo flare, a pressão a montante de algumas PSVs permanece elevada por mais tempo que o previsto e há suspeita de abertura fora da condição esperada. Qual é o diagnóstico técnico mais consistente e qual deve ser a prioridade da investigação?

**R:** O diagnóstico mais consistente é a interação entre as PSVs e o header/flare em evento combinado, e não a conclusão imediata de falha da PSV isolada. Em coletor comum, descargas simultâneas podem elevar a contrapressão e alterar a abertura ou o desempenho de outras PSVs; por isso, a adequação da válvula depende também do arranjo de descarga, da contrapressão máxima prevista e do tipo de PSV selecionado. A prioridade da investigação deve ser verificar se o cenário combinado foi considerado no estudo do sistema receptor e se a hidráulica do header/flare, com a contrapressão resultante, permanece compatível com as PSVs instaladas. Se houve mudança de condições operacionais ou de demanda do sistema, o projeto deve ser reavaliado antes de atribuir o desvio apenas à válvula.

### Sistema de captação e tratamento de água do mar para injeção no reservatório

**facil · APROVADA · corrigida**  
_Nota(s): Monitoramento microbiológico e indicadores de biofouling, MIC e souring em água do mar para injeção_

**P:** Como sulfato, H2S, Eh e pH são usados para identificar atividade de bactérias redutoras de sulfato nas condições em que esses parâmetros se aplicam a esse diagnóstico?

**R:** Nas condições descritas, esses parâmetros são usados como base do diagnóstico de atividade de bactérias redutoras de sulfato. A identificação foi feita por dosagem de sulfato, teste qualitativo de H2S e medições de Eh e pH. Assim, quando a avaliação utiliza esse conjunto de medições nesse contexto, ele serve para identificar a atividade associada às BRS.

**media · APROVADA**  
_Nota(s): Monitoramento microbiológico e indicadores de biofouling, MIC e souring em água do mar para injeção_

**P:** Em um sistema de água do mar para injeção com oxigênio disponível, observa-se entupimento progressivo de dutos com participação de ferro. Como a atividade de bactérias oxidantes de ferro e de nitrito pode explicar, ao mesmo tempo, esse entupimento e a criação de condições anaeróbias?

**R:** Um mecanismo consistente é a oxidação de Fe2+ para Fe3+ associada à atividade de bactérias oxidantes de ferro e de nitrito. Essa conversão pode contribuir para o entupimento dos dutos quando há participação de ferro no problema observado. Ao mesmo tempo, esses microrganismos consomem oxigênio no sistema. Esse consumo reduz a disponibilidade de oxigênio e favorece a evolução do meio para condições anaeróbias. Assim, o mesmo quadro microbiológico pode explicar simultaneamente o entupimento por processos ligados à oxidação do ferro e a transição do sistema para um ambiente mais favorável a processos anaeróbios.

**dificil_A · APROVADA**  
_Nota(s): Qualidade da água de injeção, compatibilidade com o reservatório e prevenção de incrustação em sistemas de água do mar de FPSO_

**P:** Após o comissionamento da injeção de água do mar em um FPSO, a equipe passou a misturar correntes de água de origens diferentes para manter vazão. Em seguida, houve queda de injetividade, aumento de restrição em válvulas e inspeção com depósitos aderidos; a análise química da mistura indicou tendência à precipitação de sais pouco solúveis quando a água injetada entra em contato com a água de formação. Qual diagnóstico é mais consistente para a perda de desempenho do sistema?

**R:** O diagnóstico mais consistente é incompatibilidade química entre a água de injeção e a água de formação, com formação de incrustações. A mudança para mistura de correntes com características diferentes é um gatilho relevante, porque essa condição pode levar à precipitação de sais e gerar incrustação tanto nas tubulações quanto no reservatório. Esse mecanismo explica a queda de injetividade, a restrição em válvulas e os depósitos observados. Também é compatível com risco de redução da permeoporosidade da formação e favorecimento de corrosão localizada por pitting. Como a escolha da água depende das características do reservatório e da compatibilidade com a formação receptora, o caso aponta mais para scale por mistura incompatível do que para um problema definido primariamente como sólidos externos, atividade bacteriana ou corrosividade isolada. O monitoramento desde o início da injeção é justamente a barreira para detectar essa deterioração cedo e corrigir a operação antes de dano severo.

**dificil_B · REPROVADA: suporte · corrigida**  
_Nota(s): Seleção da fonte de captação e projeto físico do sistema de água do mar para injeção em FPSOs; Ciclo operacional da filtração e retrolavagem do leito em sistemas de água do mar para injeção; Garantia hidráulica de vazão e pressão no sistema de água de injeção_

**P:** Em um FPSO, os filtros do sistema de água do mar passaram a operar com mais episódios de perda de eficiência e retrolavagem, enquanto surgiram oscilações de vazão nas bombas de injeção e irregularidade no atendimento aos poços. Sem parar a injeção, qual diagnóstico deve ser priorizado primeiro e que elemento do arranjo ajuda a separar um problema ligado à captação/filtração de uma limitação hidráulica de alimentação?

**R:** Deve-se priorizar primeiro o ramo captação/filtração. A fonte de captação condiciona o teor de sólidos em suspensão, a turbidez e a estabilidade da água recebida pelo tratamento, e a filtração perde eficiência quando partículas ficam retidas e obstruem o leito, exigindo retrolavagem. Portanto, aumento de eventos de retrolavagem deve ser lido primeiro como sinal a investigar na água captada e no comportamento do filtro. Para separar isso de limitação hidráulica de alimentação, o elemento-chave do arranjo é o vaso de injeção. No fato operacional citado, quando cai a água produzida e entra água salgada no sistema, o vaso mantém pressão constante para as bombas e impede oscilação de fluxo. Assim, filtração/retrolavagem apontam para montante do tratamento; manutenção de pressão constante é função do desacoplamento hidráulico.

### Sistema de drenagem aberta e fechada

**facil · APROVADA**  
_Nota(s): Filosofia de alarmes e intertravamentos de proteção em sistemas de drenagem/processo_

**P:** Qual é a diferença funcional entre um alarme operacional e um intertravamento ou sistema instrumentado de proteção em um sistema de drenagem/processo?

**R:** O alarme operacional serve para avisar que uma variável está se aproximando do limite de operação normal, dando ao operador oportunidade de corrigir o desvio antes que a condição perigosa se estabeleça. Já o intertravamento ou sistema instrumentado de proteção é a camada de proteção que deve atuar automaticamente quando a condição insegura é atingida, sem depender de resposta manual do operador. Por isso, alarme e proteção não são intercambiáveis: o alarme apoia a condução da operação, enquanto a proteção existe para evitar perda de contenção quando a resposta precisa ser automática.

**media · APROVADA**  
_Nota(s): Filosofia de alarmes e intertravamentos de proteção em sistemas de drenagem/processo_

**P:** Durante a operação, um override de proteção foi aplicado em painel remoto ou HMI sem conhecimento da sala de controle e sem autorização nem avaliação formal. Qual risco operacional essa prática introduz?

**R:** Ela introduz risco por degradação não controlada da função de proteção. Quando o override é aplicado sem conhecimento da sala de controle, sem autorização e sem avaliação apropriada, a instalação pode operar com a proteção instrumentada indisponível ou reduzida sem que essa condição seja gerida. Isso aumenta a exposição a perda de contenção, porque a barreira que deveria atuar automaticamente pode estar neutralizada justamente quando uma condição insegura ocorrer. Além disso, essa prática rompe o controle operacional sobre a indisponibilidade temporária da função de proteção.

**dificil_A · REPROVADA: escopo · corrigida**  
_Nota(s): Arranjo do sistema de drenagem aberta e fechada e gestão de integridade de linhas internas a tanques, headers e vasos de drenagem_

**P:** Em um descomissionamento parcial, um trecho de drenagem aberta deixou de operar e a equipe propõe retirá-lo da análise de risco, da gestão de mudanças e da rotina de inspeção, por entendê-lo como “sem relevância” enquanto o projeto não é concluído. Considerando que há linhas no interior de tanques associadas a esse arranjo, por que essa decisão é tecnicamente inadequada?

**R:** A decisão é inadequada porque, em descomissionamento e gestão de mudanças, as condições de integridade das linhas no interior de tanques ainda precisam ser consideradas nas análises de risco. Os riscos relevantes incluem retorno de gás ao convés, transferência de carga entre tanques e vazamento de óleo para o mar. Além disso, deve existir rotina de gestão da integridade, com inspeções e manutenções, para tubulações que passam no interior dos tanques; portanto, o simples fato de o trecho estar fora da operação normal não elimina a necessidade desse controle. Se testes ou manutenções identificarem falhas, elas devem ser tratadas por Ordem de Manutenção corretiva, com planejamento compatível com o risco e a complexidade, e com incentivo a ações preventivas.

**dificil_B · REPROVADA: suporte · corrigida**  
_Nota(s): Planejamento e governança dos testes de comissionamento em sistemas de drenagem aberta e fechada; Limpeza, flushing, drenagem, teste de estanqueidade e preservação de linhas e vasos de drenagem antes da entrada em serviço; Inspeção e limpeza de selos e pontos de bloqueio em sistemas de drenagem aberta e fechada_

**P:** Nos primeiros dias após o start-up de um sistema de drenagem aberta e fechada em um FPSO, surgem escoamento irregular, acúmulo em drenos e suspeita de perda de segregação em seal pots e loops. O sistema foi liberado para operação, mas a equipe precisa decidir se a análise técnica deve começar pela preparação pré-serviço/comissionamento ou pela rotina inicial de inspeção e manutenção. Qual linha de investigação é mais consistente com os indícios do cenário e como ela deve ser justificada?

**R:** A linha mais consistente é começar verificando se houve desvio de preparação pré-serviço ou erro não eliminado no comissionamento, sem excluir a inspeção inicial. Como as anomalias surgiram nos primeiros dias, isso é compatível com a necessidade de confirmar se os testes cobriram os componentes e processos previstos e se a operação assistida tratou rapidamente os desvios iniciais. Também convém verificar a preparação física: limpeza/flushing para remoção de detritos e, se houve uso de água, drenagem dos pontos baixos, remoção da água residual com ar seco e preservação com ar seco ou nitrogênio quando o sistema ficou vazio por alguns dias. A rotina de inspeção continua necessária porque deve checar integridade dos selos e ausência de detritos em drenos e headers, mas, nesse cenário, ela pode estar revelando anomalias introduzidas antes da entrada em serviço.

### Tratamento de água produzida para descarte

**facil · APROVADA**  
_Nota(s): Separação primária gravitacional e condicionamento inicial da água produzida em FPSO_

**P:** Qual é o papel dos tanques de slop no tratamento da água produzida em um FPSO antes do descarte?

**R:** Nos FPSOs, os tanques de slop recebem a água de produção para tratamento e posterior descarte, atuando como parte do sistema de tratamento e não apenas como armazenamento. Nesse arranjo, um ou dois tanques originais do navio podem ser dedicados a essa função, integrando a etapa inicial de separação gravitacional da água produzida.

**media · APROVADA · corrigida**  
_Nota(s): Separação primária gravitacional e condicionamento inicial da água produzida em FPSO_

**P:** Em um FPSO, a equipe pretende aumentar o volume útil de um tanque de decantação e o tempo de repouso da água produzida na etapa inicial por gravidade. Qual efeito essa mudança tende a ter sobre a eficiência da separação gravitacional?

**R:** Essa mudança tende a aumentar a eficiência da separação gravitacional na etapa inicial. Porém, mesmo com tanque de maiores dimensões e maior tempo de repouso, a água produzida ainda pode sair com elevada concentração de hidrocarbonetos, exigindo etapa adicional antes do descarte.

**dificil_A · REPROVADA: codigo:depende_do_material · corrigida**  
_Nota(s): Hidrociclones no tratamento de água produzida para intensificação da separação óleo-água_

**P:** Em um FPSO, a água produzida saiu pior da bateria de hidrociclones. No mesmo período, a corrente de água que deixa os separadores e alimenta esse tratamento passou a apresentar óleo disperso acima de 1000 mg/L, valor de referência desse estágio, após instabilidade no separador e no tratador eletrostático. Sem evidência de perda de pressão na alimentação dos hidrociclones, qual causa é mais provável para a piora: sobrecarga por arraste de óleo a montante ou perda de condição de separação no próprio hidrociclone?

**R:** A causa mais provável é sobrecarga por arraste de óleo a montante. Pelo F1, a corrente de água que deixa os separadores deve chegar a esse tratamento com concentração de óleo disperso não superior a 1000 mg/L; se esse valor foi ultrapassado após instabilidade no separador e no tratador eletrostático, o indício principal é excesso de óleo sendo carregado para os hidrociclones. Pelo F2, o hidrociclone depende de alimentação tangencial sob pressão para gerar a força centrífuga que promove a separação. Como o cenário informa que não há evidência de perda de pressão de alimentação, fica menos provável atribuir a piora, em primeiro lugar, a perda da condição hidráulica do próprio equipamento.

**dificil_B · REPROVADA: correcao_tecnica, suporte, sem_generalizacao**  
_Nota(s): HAZOP como estrutura de diagnóstico de falhas no tratamento de água produzida; Falhas de medição e controle da interface óleo/água e seu efeito no arraste de óleo para a água produzida; Diagnóstico de ineficiência em equipamentos de tratamento da água produzida_

**P:** Uma unidade de tratamento de água produzida passa a exigir múltiplas passagens para enquadrar TOG e, em alguns períodos, a operação recorre a by-pass manual. Ao mesmo tempo, há suspeita de medição lenta ou descalibrada da interface óleo/água no separador e no tratador eletrostático. Como estruturar o diagnóstico para distinguir perda de controle na separação primária de limitação do mecanismo dos equipamentos de tratamento, e qual frente deve ser verificada primeiro?

**R:** Estruture por HAZOP em nós separados: separação primária e tratamento. Em cada nó, defina o comportamento esperado, escolha parâmetros e aplique palavras-guia para gerar desvios, causas, consequências, ação e meios de detecção/atuação. No nó da separação primária, investigue “interface mais/menos” e “medição lenta/incorreta”, porque o controle da interface evita envio de óleo para a corrente de água produzida; se o sensor de interface tem deriva, erro ou atraso, ele degrada simultaneamente o controle e o próprio diagnóstico. No nó do tratamento, investigue se a carga recebida contém gotas finas ou óleo emulsionado, situação compatível com necessidade de múltiplas passagens, ou se há perda de capacidade por bloqueio de poros com retrolavagem. A prioridade é verificar primeiro a confiabilidade da medição e o controle de interface a montante, porque arraste de óleo da separação primária pode sobrecarregar o tratamento e mascarar uma limitação tecnológica real.

### Tratamento do Gás produzido

**facil · APROVADA**  
_Nota(s): Desidratação do gás por glicóis e condicionamento para evitar hidratos, condensação e danos a jusante_

**P:** Qual é a função da desidratação do gás produzido e por que a remoção de água protege linhas e equipamentos a jusante contra condensação e danos?

**R:** A desidratação remove a água da corrente de gás sob pressão para reduzir a formação de fase aquosa e de hidratos ao longo do escoamento e do tratamento. Ao retirar essa água, diminui-se a chance de condensação líquida nas linhas e equipamentos a jusante, o que ajuda a evitar sua deterioração. Em arranjos usuais, o gás que permanece na fase gasosa após compressão e resfriamento segue para a unidade de secagem antes de tratamentos posteriores e da exportação. Essa etapa trata especificamente o teor de água do gás; ela não substitui o ajuste do ponto de orvalho de hidrocarbonetos, que é uma etapa distinta para controlar a condensação de componentes pesados do próprio gás.

**media · REPROVADA: codigo:referencia_alternativas · corrigida**  
_Nota(s): Desidratação do gás por glicóis e condicionamento para evitar hidratos, condensação e danos a jusante_

**P:** Em uma unidade offshore de tratamento de gás, a equipe avalia manter a desidratação por absorção com glicol ou adotar outra tecnologia de remoção de umidade. Compare essas alternativas e indique por que a absorção líquida é frequente offshore e em que condição de processo a especificação de umidade pode levar a outra escolha.

**R:** A absorção com glicol é frequente offshore porque a absorção com líquidos facilita a logística de manuseio nesse ambiente e, por isso, é a solução mais comum. Nessa rota, o glicol remove água do gás e depois é regenerado para reuso. Em comparação, peneiras moleculares podem ser escolhidas quando se deseja teor de umidade mais baixo, porque o TEG normalmente deixa no gás uma umidade maior do que a obtida com peneiras moleculares. A escolha também depende das condições de pressão e temperatura a que o gás será submetido depois do tratamento: conforme esse regime, pode-se adotar especificação de umidade menos restritiva e até tecnologias diferentes das peneiras moleculares.

**dificil_A · APROVADA**  
_Nota(s): Modos operacionais A, B e C de plataformas com membranas de remoção de CO₂ e seus efeitos sobre exportação, injeção e gás combustível_

**P:** Uma plataforma com remoção de CO₂ por membranas alterna entre três condições ao longo do dia: indisponibilidade total por restrição operacional, operação parcial e operação plena. A equipe precisa definir, em cada condição, como fica o balanço entre exportação e injeção do gás produzido e qual conclusão pode ser afirmada sobre o gás combustível das turbinas quando as membranas ficam totalmente fora de serviço. Qual é a avaliação correta?

**R:** Com indisponibilidade total das membranas, a unidade opera no arranjo em que todo o gás contorna a remoção de CO₂; nessa condição, a exportação fica impedida e todo o volume deve ser direcionado para injeção no reservatório. Com operação plena das membranas, a plataforma cria a condição para exportação máxima de gás. Com operação parcial, o resultado é intermediário: parte do gás é tratada, permitindo exportação parcial, e a parcela restante segue para injeção parcial. Para o gás combustível, a conclusão sustentada para a condição de indisponibilidade total é que o gás enviado às turbinas terá teor de CO₂ igual ao do fluido produzido nos poços, porque não existe parcela tratada pelas membranas antes desse uso.

**dificil_B · REPROVADA: suporte**  
_Nota(s): Desidratação e condicionamento do gás produzido para exportação ou reinjeção em FPSOs; Remoção de condensados no gás comprimido e proteção do sistema de compressão; Controle de líquido no gás a montante de peneiras moleculares: proteção do leito, desempenho de desidratação e confiabilidade da regeneração_

**P:** Após aumento de carga no trem de compressão com resfriamento entre estágios, uma unidade de desidratação por peneiras moleculares passou a entregar gás mais úmido, e a regeneração seguinte não recuperou o desempenho. Houve indícios de líquido a montante do adsorvedor. Qual mecanismo deve ser priorizado no diagnóstico e que barreira de processo precisa ser verificada primeiro para evitar recorrência?

**R:** O diagnóstico deve priorizar entrada de líquido no leito, e não apenas saturação normal da peneira ou falha isolada de regeneração. No trem de compressão, o resfriamento entre estágios reduz a temperatura do gás e promove condensação de frações mais pesadas, exigindo remoção do líquido formado em scrubbers ou separadores antes que o gás siga adiante. Se essa retenção falha, gotículas ou condensado podem alcançar o adsorvedor. Em peneiras moleculares, água líquida no leito pode solubilizar o ligante, formar cakes durante a regeneração, reduzir a área superficial e piorar a distribuição do fluxo, com caminhos preferenciais; por isso a regeneração deixa de restaurar o desempenho como faria em um leito apenas carregado de água adsorvida. A primeira barreira a verificar é a separação mecânica de líquidos a montante do adsorvedor, especialmente nos pontos a jusante dos resfriadores, onde o condensado volta a se formar.

## Segurança Operacional, SGSO, Sistemas de Segurança e Gestão de Riscos

### Estudos de Segurança

**facil · APROVADA**  
_Nota(s): Bow-Tie e premissas para classificar risco e avaliar a efetividade de barreiras em estudos de segurança_

**P:** No diagrama Bow-Tie, o que representa o lado esquerdo e o que representa o lado direito, em relação à árvore de falhas e à árvore de eventos?

**R:** O lado esquerdo representa a lógica de árvore de falhas: organiza as causas e como elas podem levar ao evento principal. O lado direito representa a lógica de árvore de eventos: mostra como as consequências podem se desdobrar a partir do evento principal. Assim, o Bow-Tie conecta causas, evento principal e consequências em uma única estrutura de análise de barreiras.

**media · APROVADA**  
_Nota(s): Bow-Tie e premissas para classificar risco e avaliar a efetividade de barreiras em estudos de segurança_

**P:** Em um estudo de segurança, um cenário foi classificado pela pior consequência que pode ocorrer imediatamente após a liberação do perigo, e sua frequência foi calculada assumindo barreiras disponíveis e operando conforme esperado. Como essa classificação deve ser interpretada?

**R:** Ela deve ser entendida como o risco do cenário sob hipóteses explícitas de desempenho das barreiras. A severidade usada na classificação corresponde à pior consequência imediata após a liberação do perigo, não a escalonamentos posteriores. Já a frequência estimada pressupõe que as barreiras de segurança estão disponíveis e atuam no nível de performance esperado. Portanto, o resultado não representa automaticamente o risco real em qualquer condição operacional: ele vale dentro dessas premissas sobre disponibilidade, adequação e desempenho das barreiras creditadas.

**dificil_A · REPROVADA: correcao_tecnica, suporte, sem_generalizacao · corrigida**  
_Nota(s): Revisão periódica, atualização e validade dos estudos de segurança de FPSOs ao longo do ciclo de vida_

**P:** Um FPSO entrou em late life, e a equipe de integridade identificou indícios de fadiga e corrosão no casco e no topside, com possível impacto na vida remanescente. Ao mesmo tempo, houve modificações registradas no gerenciamento de mudanças. Para decidir se a revisão do safety case deve ser acionada, que verificações e estudos devem subsidiar essa decisão, e como ela deve ser formalizada no sistema de gestão?

**R:** A decisão deve partir de duas verificações principais: se o envelhecimento em late life, incluindo fadiga e corrosão no casco e no topside, alterou premissas técnicas antes aceitas, e se as modificações registradas no gerenciamento de mudanças geraram impacto relevante sobre os estudos de risco. Como esse tipo de condição pode exigir revisão do safety case, a avaliação deve confirmar se as premissas dos estudos permanecem válidas e se o safety case continua representando a unidade. Quando houver impacto, o sistema deve acionar a Safety Case Review e, se necessário, revisão adicional da análise de risco do processo, como HAZOP. A revisão também não pode ter escopo incompleto: devem ser incluídos os estudos complementares cujas premissas sustentam a avaliação. No sistema de gestão, a decisão deve ser identificada, registrada, comunicada e evidenciada, mantendo alinhamento com o programa de integridade de ativos para sustentar o risco residual em ALARP.

**dificil_B · REPROVADA: suporte, jurisdicao · corrigida**  
_Nota(s): Identificação e seleção de perigos e cenários acidentais com HAZID, HAZOP, What-if e FMEA/FMECA; Construção de cenários acidentais para liberações inflamáveis em estudos de segurança offshore; QRA/FERA: estrutura do estudo, escopo e critérios para seleção metodológica_

**P:** Durante a atualização dos estudos de uma unidade offshore, a equipe quer manter apenas HAZID e What-if antigos para concluir que os cenários de incêndio e explosão por liberações inflamáveis já estão cobertos. Porém, a decisão em aberto é se o estudo atual sustenta a escolha de medidas adicionais de redução de risco em área congestionada. Qual encaminhamento metodológico é mais consistente nesse caso?

**R:** O encaminhamento mais consistente é não tratar HAZID e What-if antigos como base suficiente por si só. Eles servem para identificar perigos, mas, para liberações inflamáveis, os cenários precisam ser consolidados em hipóteses acidentais estruturadas por árvore de eventos, encadeando liberação, dispersão, ignição e consequências. A escolha metodológica também precisa ser justificada conforme o tipo de perigo e a profundidade necessária para a decisão. Se for necessário estimar com mais realismo frequências e consequências para apoiar a definição de medidas de redução de risco, cabe aprofundamento semiquantitativo ou quantitativo. Isso evita distorções porque, em áreas congestionadas, o desfecho depende de variáveis como tipo e condição do vazamento, tempo de ignição, confinamento e dispersão do gás, além do potencial de escalonamento.

### Operações simultâneas – SIMOPS

**facil · APROVADA**  
_Nota(s): Governança de SIMOPS: papéis, cadeia de comando, reuniões e comunicação entre frentes_

**P:** Por que crews contratadas ou de construção precisam ser alertadas, por meio de seus supervisores, sobre operações de produção, perfuração ou workover com as quais possam interagir inadvertidamente?

**R:** Porque essas equipes podem não ter familiaridade suficiente com as operações offshore em curso e, sem esse alerta, aumentam as chances de interferir sem intenção em uma atividade de óleo e gás que esteja ocorrendo ao mesmo tempo. O objetivo do alerta, feito via supervisão, é tornar explícita qual operação pode ser afetada e quais consequências essa interação pode gerar. Em SIMOPS, não basta cada equipe conhecer apenas o próprio serviço; ela também precisa estar ciente das interações com outros trabalhos, pois a falta dessa percepção é uma lacuna de controle que compromete o planejamento, as barreiras e a adequação do trabalho autorizado.

**media · APROVADA**  
_Nota(s): Governança de SIMOPS: papéis, cadeia de comando, reuniões e comunicação entre frentes_

**P:** Em um projeto offshore com trabalho de contratada executado simultaneamente à produção, a troca de turno ocorre junto com substituição parcial da crew. Como essas mudanças podem degradar a coordenação de SIMOPS e por que a comunicação entre a supervisão do operador e a da contratada deve ser mantida durante todo o projeto?

**R:** Mudanças de turno e de crew são pontos típicos de perda de continuidade da informação. Nelas, detalhes sobre quais atividades coexistem, onde há interação entre frentes e quem responde por cada interface podem se distorcer ou deixar de ser repassados, reduzindo a capacidade de perceber conflitos a tempo. Por isso, a comunicação entre a supervisão do operador e a da contratada deve permanecer clara e contínua ao longo de todo o projeto, e não só no início, para preservar o mesmo entendimento operacional apesar das trocas de pessoas. Em atividades cobertas por Permit, essa continuidade também deve aparecer em rotinas formais como discussão do trabalho, reunião de Permit e passagem de turno, nas quais os Permits e suas interações são revisitados para manter a coordenação entre as frentes.

**dificil_A · APROVADA**  
_Nota(s): Condições anormais dinâmicas em SIMOPS: perda de posicionamento, perda de geração e transição para estado seguro_

**P:** Durante SIMOPS, uma unidade entra em condição anormal dinâmica por dois caminhos possíveis. No primeiro, o posicionamento dinâmico passa a operar com carga crescente nos propulsores, desvio de rumo e deriva sob piora ambiental. No segundo, ocorre falha de energia principal. Comparando os dois casos, quais funções essenciais devem ser preservadas primeiro em cada um para conduzir a unidade a um estado seguro, e qual decisão operacional tende a prevalecer em cada cenário?

**R:** Se a condição predominante for perda de posicionamento, a função essencial a preservar primeiro é a capacidade de evitar interação danosa com a infraestrutura submarina. Carga crescente nos propulsores, desvio de rumo e deriva sob agravamento ambiental caracterizam degradação da capacidade de manter posição; quando o DP já não sustenta rumo e posição, a decisão que tende a prevalecer é a desconexão de emergência para evitar danos potenciais à infraestrutura submarina. Se a condição predominante for falha de energia principal, a função essencial a preservar primeiro é a estabilidade da unidade por meio da operabilidade do lastro. Nesse caso, a transição segura depende de conseguir levar o vaso a trim seguro e nivelado, mantendo uma ou mais bombas de lastro e o sistema completo de lastro operáveis a partir do quadro de emergência alimentado pelo gerador de emergência. Portanto, no primeiro caso prevalece desconectar; no segundo, preservar lastro e estabilidade.

**dificil_B · REPROVADA: suporte, codigo:depende_do_material · corrigida**  
_Nota(s): Matriz operações versus barreiras como base para compatibilidade e restrições operacionais em SIMOPS; SIMOPS: como bypasses, intertravamentos e lógicas automáticas podem degradar simultaneamente disponibilidade e independência das barreiras; Impacto de alarmes, detecção de gás, intertravamentos e ESD na continuidade de SIMOPS_

**P:** Duas frentes em SIMOPS foram liberadas como compatíveis pela matriz vigente. Durante a execução, há detecção de gás na pumps room, e a lógica automática muda a ventilação, aquecendo painéis do e-house. Ao mesmo tempo, verifica-se que, para viabilizar outra frente, foi aplicado maintenance bypass em um transmissor que executa PSH e PSL. Qual deve ser a decisão inicial da coordenação sobre a continuidade das frentes e por quê?

**R:** A decisão inicial deve ser reavaliar imediatamente a compatibilidade real das frentes e, até essa verificação, restringir ou suspender as atividades afetadas. A razão é que a compatibilidade em SIMOPS depende do estado efetivo das barreiras, não apenas da matriz nominal. Uma operação pode afetar várias barreiras, e a lista só sustenta a decisão se estiver convergente com a condição em campo (F1, F2). Neste caso, o maintenance bypass no transmissor não retirou só a função pretendida: ele desabilitou simultaneamente PSH e PSL (F4). Além disso, o alarme de gás teve efeito operacional relevante, pois a lógica automática alterou a ventilação e aqueceu painéis do e-house, podendo levar ao desligamento de produção e geração (F7). Portanto, a premissa de compatibilidade deve ser revista com base nas barreiras que ainda permanecem disponíveis.

### Segurança e Controle de Riscos

**facil · APROVADA**  
_Nota(s): Controle de fontes de ignição e proteção de equipamentos em áreas classificadas_

**P:** Por que equipamentos elétricos e eletrônicos podem atuar como fontes de ignição em atmosferas explosivas?

**R:** Porque, em áreas com gases ou vapores inflamáveis, esses equipamentos podem fornecer a energia ou a temperatura necessárias para inflamar a mistura. Isso pode ocorrer por arcos e faíscas, pelo centelhamento normal na abertura e fechamento de contatos, e por superfícies aquecidas, tanto em operação normal quanto em condição de falha. Também podem contribuir fenômenos associados ao uso desses equipamentos, como eletricidade estática e descargas atmosféricas. Como a energia mínima de ignição de certas misturas pode ser muito baixa, equipamentos não adequados para a área classificada podem deixar de ser barreira e passar a atuar como iniciadores de incêndio ou explosão.

**media · APROVADA**  
_Nota(s): Controle de fontes de ignição e proteção de equipamentos em áreas classificadas_

**P:** Em uma instalação elétrica localizada em área classificada, como dispositivos de alarme e seccionamento automático reduzem o risco de ignição quando surgem sobretensão, sobrecorrente, falha de isolamento ou aquecimento anormal?

**R:** Esses dispositivos reduzem o risco ao identificar condições elétricas anormais antes que elas evoluam para uma fonte de ignição e, então, sinalizar a anomalia e interromper automaticamente a energia do circuito afetado. Com isso, diminuem a probabilidade de formação de arcos, faíscas ou superfícies aquecidas capazes de inflamar gases ou vapores presentes na área classificada. Sua função é atuar como barreira complementar contra anormalidades como sobretensão, sobrecorrente, falha de isolamento e aquecimento excessivo, limitando a progressão da falha para um evento de incêndio ou explosão.

**dificil_A · REPROVADA: suporte**  
_Nota(s): Investigação de incidentes com identificação de causas imediatas, básicas e sistêmicas_

**P:** Em uma atividade de manutenção repetitiva em unidade offshore, ocorreu um quase acidente na recolocação em serviço após isolamento. A investigação mostrou um desvio na execução, mas também encontrou auditorias com não conformidades recorrentes no isolamento, ausência de sistema para revisar válvulas travadas abertas ou fechadas, supervisão fraca e avaliação de riscos/método de trabalho alterados apenas depois de questionamento. Quais ações corretivas e preventivas são mais coerentes com esse diagnóstico?

**R:** As ações devem atacar a cadeia causal completa, não apenas o erro de execução. É tecnicamente mais coerente restaurar a eficácia das barreiras de isolamento, implantando controle e revisão sistemática das válvulas travadas abertas ou fechadas e corrigindo as fragilidades práticas do arranjo de isolamento evidenciadas por auditorias e recorrência. Em paralelo, a organização deve revisar a avaliação de riscos e o método de trabalho, porque a mudança só após questionamento indica falha prévia nessas etapas. Também é necessário fortalecer como o trabalho é controlado e supervisionado, com monitoramento de conformidade mais eficaz, revisão dos controles procedimentais e das deficiências de gestão que permitiram a permanência do problema. Medidas apenas disciplinares, de requalificação isolada ou de produção documental são insuficientes, porque não removem as falhas de barreira, supervisão e gestão que sustentam a repetição do evento.

**dificil_B · APROVADA**  
_Nota(s): Lacunas de identificação de perigos por mudanças operacionais, interpretações locais e cenários não previstos; Gestão de mudanças, HRA e revisão de análises para condições não rotineiras; Avaliação de riscos em modos operacionais, transientes e condições anormais_

**P:** Após manutenção, uma unidade entra em retorno ao serviço. Durante a tarefa liberada por PT, a equipe identifica no campo um perigo relevante de liberação de substância perigosa que não constava da análise usada para autorizar o trabalho. A supervisão deve tratar isso como falha pontual de execução ou como evidência de lacuna no processo de gestão de riscos? Qual decisão técnica é mais adequada?

**R:** Deve tratar como evidência de lacuna sistêmica de identificação e reavaliação de perigos, não apenas como falha local da equipe. Quando um perigo relevante só é reconhecido durante a execução, isso indica que a análise não representou a condição operacional real; esse sinal já foi observado em desconexão com H2S aprisionado não previsto no HAZID. Retorno ao serviço após manutenção é condição diferente da rotina, com perigos próprios, e pode exigir gestão de mudanças, procedimento específico de partida/retorno, atualização das informações de pré-operação e controles efetivos de PTW e isolamento. Como o processo estava em transiente, a análise deveria cobrir essa etapa e seus limites operacionais. Se a tarefa ou procedimento for crítico para a segurança, a revisão deve incluir HRA. Se a metodologia permitiu essa omissão, o procedimento de gestão de riscos deve ser revisto com ferramenta reconhecida e rastreabilidade documental.

### SGSO

**facil · APROVADA**  
_Nota(s): Planejamento do Plano de Emergência integrado à gestão de riscos e aos cenários acidentais_

**P:** Quais elementos mínimos o Plano de Emergência da instalação deve contemplar para estruturar a resposta a cenários acidentais?

**R:** Deve contemplar, no mínimo: identificação da instalação e do responsável legal; descrição dos acessos; cenários acidentais previstos; sistemas de alerta; comunicação do acidente; estrutura organizacional de resposta; procedimentos de resposta; equipamentos e materiais de resposta; e procedimento para acionamento de recursos e estruturas complementares, quando aplicável. Para cenários com materiais perigosos, o planejamento deve incluir ações específicas para isolamento e controle de vazamentos, porque essa definição é parte relevante da capacidade de resposta.

**media · APROVADA · corrigida**  
_Nota(s): Planejamento do Plano de Emergência integrado à gestão de riscos e aos cenários acidentais_

**P:** Na revisão do Plano de Emergência de um FPSO, a equipe discute se determinados cenários devem permanecer no plano da instalação ou ser tratados em plano específico. Qual é o critério para essa decisão no caso de vazamento de óleo, e o que deve continuar previsto para os demais cenários perigosos?

**R:** Se a hipótese acidental for vazamento de óleo, esses cenários podem ser tratados somente em plano de emergência específico, como o SOPEP ou outro plano de emergência definido por regulamento específico. Para os demais cenários acidentais da instalação, o Plano de Emergência deve continuar contemplando os cenários previstos e a estrutura de resposta correspondente, incluindo comunicação do acidente, organização da resposta, procedimentos, equipamentos e materiais. Quando houver materiais perigosos, também devem estar previstas ações específicas para isolamento e controle de vazamentos.

**dificil_A · APROVADA**  
_Nota(s): Identificação, classificação e governança dos Elementos Críticos de Segurança Operacional no SGSO_

**P:** Em um FPSO, auditorias sucessivas voltam a registrar desvios ligados a salvaguardas classificadas como críticas. As correções locais foram encerradas a cada ciclo, mas os mesmos tipos de problema reaparecem em áreas diferentes e a gerência não consegue demonstrar, por indicadores, visão estável da disponibilidade e integridade dessas barreiras. Por que esse quadro sugere falha sistêmica na identificação ou no tratamento dos Elementos Críticos de Segurança Operacional, e não apenas falhas isoladas de execução?

**R:** Porque a recorrência, após ações corretivas anteriores, indica que o tratamento não foi suficientemente abrangente para eliminar a causa de gestão, apenas manifestações locais do desvio. Quando isso ocorre no universo de salvaguardas críticas, o problema deixa de ser pontual e passa a sugerir inconsistência estrutural em como o sistema identifica quais elementos realmente são barreiras críticas e como os gerencia. No SGSO, são críticos não só equipamentos, mas também sistemas e procedimentos cuja função é prevenir ou mitigar acidentes, ou cuja falha pode provocá-los; se a identificação for incompleta ou inconsistente, parte dessas barreiras fica fora do controle gerencial. Além disso, a disponibilidade e a integridade devem ser monitoradas continuamente em nível gerencial, com apoio de indicadores por unidade offshore. Se a gerência não consegue evidenciar essa visão e os desvios se repetem, há forte sinal de falha sistêmica; em recorrência no gerenciamento dos elementos críticos, pode ser requerida verificação de barreiras por terceira parte.

**dificil_B · APROVADA**  
_Nota(s): Capacitação, mudanças organizacionais e gestão de contratadas no SGSO em FPSOs; Gestão de mudanças de pessoas e capacitação para mudanças operacionais no SGSO; SGSO: efetividade de procedimentos operacionais depende de controle documental, recursos, treinamento e garantia da qualidade na execução_

**P:** Após reorganização de equipes com acúmulo temporário de funções e entrada de novos operadores, os procedimentos críticos permanecem atualizados e acessíveis no sistema documental. Em campo, porém, ocupantes do mesmo cargo executam a mesma rotina com interpretações diferentes e dúvidas sobre etapas críticas; há registros de treinamentos passados, mas não de tutoria prévia nem de revisão da mudança com operação e manutenção. Qual é o diagnóstico técnico prioritário e a ação de gestão mais consistente?

**R:** O problema prioritário é barreira humana degradada por mudança de pessoas não absorvida, e não falha principal de controle documental. Mesmo com procedimento vigente e acessível, sua efetividade depende de capacitação por função, treinamento contínuo e verificação da execução com qualidade; sem isso, o procedimento perde autoridade operacional na prática. Como houve acúmulo de funções e entrada de pessoal, a situação deveria ter passado pelo gerenciamento de mudanças de pessoas, com tratamento formal dessas alterações, capacitação teórica e prática, reciclagem e tutoria antes da efetivação. A heterogeneidade de execução indica que a equipe não converteu a mudança em entendimento uniforme do procedimento. A ação mais consistente é reabrir a mudança como mudança de pessoas, revisar suas implicações com operação e manutenção, aplicar tutoria e treinamento específico por função e restabelecer a verificação da qualidade da execução no campo.

### Sistema de Combate a Incêndio

**facil · APROVADA**  
_Nota(s): Barreiras passivas, divisórias e compartimentação corta-fogo_

**P:** Entre uma parede corta-fogo e uma divisória resistente ao fogo, qual oferece maior nível relativo de proteção contra incêndio?

**R:** A parede corta-fogo oferece maior proteção relativa contra incêndio. Na estratégia passiva de proteção e contenção, tanto paredes quanto divisórias podem atuar como barreiras, mas a parede fornece proteção superior à divisória.

**media · APROVADA**  
_Nota(s): Barreiras passivas, divisórias e compartimentação corta-fogo_

**P:** Na definição de uma barreira resistente ao fogo para separar áreas com ocupações e níveis de perigo distintos em uma unidade offshore, quais variáveis do cenário e da área protegida devem orientar a escolha do tipo, da localização e do projeto da barreira?

**R:** Devem ser considerados o tipo e a severidade do incêndio esperado, além do tamanho e da configuração da área a ser protegida. A escolha também precisa refletir as características de ocupação e o nível de perigo das áreas separadas, porque a aplicação de barreiras resistentes ao fogo depende do cenário de risco e das características do espaço protegido.

**dificil_A · APROVADA · corrigida**  
_Nota(s): Gestão de inspeção, manutenção e tratamento de desvios em sistemas de combate a incêndio no SGSO_

**P:** Em um FPSO, uma bomba principal de água de incêndio falhou no teste de desempenho e não atingiu os requisitos de vazão e pressão definidos. O equipamento é crítico para a resposta a incêndio, e a unidade pretende mantê-lo nessa condição até a próxima parada, sem contingência formalmente aprovada. No SGSO, quais decisões de controle são indispensáveis nessa situação?

**R:** O resultado do teste deve ser tratado como desvio conclusivo de desempenho, porque houve não atendimento aos requisitos definidos para o elemento testado. Nessa condição, deve ser emitida ordem de manutenção corretiva, com priorização compatível com a gravidade do desvio e com a criticidade da bomba. Além disso, o operador deve monitorar e avaliar formalmente o resultado do teste. Como se trata de elemento crítico degradado para a função de combate a incêndio, a situação não pode permanecer apenas como pendência de manutenção: devem ser acionados procedimentos de contingência com sistema de aprovação e controle, incluindo medidas temporárias equivalentes, quando aplicável. Se a bomba permanecer degradada sem contingência adequada, a resposta a incêndio fica comprometida.

**dificil_B · APROVADA**  
_Nota(s): Integração entre detecção de fogo e gás, SIS/ESD, supressão e HVAC nas ações automáticas de emergência; Disponibilidade real do sistema de combate a incêndio e robustez das funções de emergência associadas; Resiliência do sistema de combate a incêndio quando o próprio evento degrada o sistema_

**P:** Durante um incêndio, os alarmes e a sequência automática prevista ocorrem: ESD atua, isolamento de processo é iniciado, ventilação do compartimento afetado é comandada e a demanda de combate é registrada. Mesmo assim, a mitigação fica abaixo do esperado: a pressão de firewater cai, parte das bombas não parte e a resposta melhora apenas após acionamento manual de bombas a diesel. Qual hipótese técnica deve ser priorizada no diagnóstico: erro na lógica integrada de emergência ou perda de disponibilidade/resiliência da infraestrutura demandada?

**R:** A hipótese principal é perda de disponibilidade/resiliência da infraestrutura de combate e suporte, não erro primário da lógica integrada. Se a detecção e a sequência automática coerente com a matriz de causa e efeito ocorreram, houve conversão do sinal em comandos de ESD, isolamento, supressão e ventilação conforme a arquitetura SIS/ESD prevê. O problema passa a ser a cadeia física demandada não entregar a função: bombas, energia e caminhos hidráulicos precisam permanecer aptos quando acionados. Queda de pressão com não partida de parte das bombas, seguida de recuperação parcial por bombas diesel em manual, é compatível com degradação do sistema pelo próprio evento ou por vulnerabilidades comuns, inclusive dano à alimentação/distribuição elétrica. O diagnóstico deve priorizar energia de emergência, interfaces de partida por diferentes iniciadores, segregação/diversidade das bombas e contingências realmente utilizáveis sob dano do acidente.

### Sistema de Fogo e Gás (F&G)

**facil · APROVADA**  
_Nota(s): Proof tests, testes parciais e inspeções associadas às SIF/F&G_

**P:** Por que a frequência de proof test de uma função instrumentada de segurança não deve ser definida apenas por conveniência operacional?

**R:** Porque a periodicidade do proof test precisa demonstrar a integridade requerida da função, e por isso deve estar alinhada ao SRS e ao cálculo de verificação de SIL, além de ser exequível nas restrições operacionais vigentes. A definição pode até considerar limitações da operação, mas não pode ser guiada só pela facilidade de programar manutenção. Quando houver decomposição por componentes, as frequências de sensor, solver lógico e elemento final devem estar definidas no SRS e servir de base para a verificação de SIL. Se o teste completo de ponta a ponta não for viável, a solução aceitável é estruturar proof tests parciais de forma compatível com essa verificação, e não simplesmente adiar ou testar “quando der”.

**media · APROVADA · corrigida**  
_Nota(s): Proof tests, testes parciais e inspeções associadas às SIF/F&G_

**P:** Em uma SIF, um partial proof test confirmou a atuação do instrumento, mas há preocupação com possível modificação de campo e deterioração do arranjo instalado. Quais verificações de inspeção devem acompanhar esse teste para identificar esses problemas?

**R:** Devem ser feitas inspeções para assegurar que o equipamento instalado não foi modificado e que sua condição não se deteriorou a ponto de não funcionar conforme o SRS. O procedimento deve identificar os itens a inspecionar, incluindo os instrumentos e equipamentos associados, como tubing de instrumentação, caixas de junção e trace heating. A inspeção deve verificar ausência de modificações não autorizadas, por exemplo pela conferência de números de série, e sinais de deterioração física, como parafusos ou tampas faltantes, suportes com ferrugem e danos em cabos. Essas inspeções são normalmente realizadas durante o proof test ou partial proof test, com requisitos incluídos no procedimento.

**dificil_A · REPROVADA: suporte, jurisdicao · corrigida**  
_Nota(s): Estratégias combinadas de manutenção, calibração e verificação de desempenho em sistemas F&G_

**P:** Em um FPSO, um detector de gás classificado como Elemento Crítico de Segurança Operacional fica fora de operação por falha inesperada, e a equipe considera manter produção apoiando-se em barreiras remanescentes até o reparo. Qual decisão técnica é a mais adequada para manter o risco controlado nessa condição degradada?

**R:** A decisão mais robusta é só manter a operação se a condição degradada for tratada formalmente como temporária e com compensações compatíveis com o risco. Antes de dar crédito às barreiras remanescentes, é necessário assegurar que os requisitos de inspeção aplicáveis a essas barreiras continuem atendidos; não basta presumir proteção porque o equipamento ainda está instalado ou porque existem outros elementos disponíveis. Como se trata de Elemento Crítico de Segurança Operacional, a situação deve entrar no programa diferenciado de inspeção, manutenção e calibração, sustentado pelas informações de criticidade oriundas dos estudos de segurança no sistema de gerenciamento. As medidas temporárias podem incluir controles alternativos equivalentes, limitação de produção, isolamento da condição perigosa ou parada, conforme o risco da exposição durante a indisponibilidade. A degradação e seu desempenho associado também devem ser registrados e acompanhados para evitar gestão reativa por falha consumada.

**dificil_B · APROVADA**  
_Nota(s): Sistema F&G: desempenho intrínseco do sensor, calibração e influência ambiental na detecção de gás inflamável; Interferência de umidade, vapor d’água, névoa/óleo e gases atmosféricos na resposta e na calibração de detectores de F&G; Calibração, aferição, ajuste, deriva e monitoramento de condição em detectores e instrumentos de F&G_

**P:** Em uma área de processo offshore com forte variação de umidade e temperatura, um detector de gás inflamável passou a oscilar a leitura e a aparentar perda de sensibilidade. Em alguns períodos também há vapor d’água e névoa. A equipe discute trocar o sensor, recalibrar imediatamente ou manter em operação. Qual deve ser a prioridade diagnóstica para distinguir interferência ambiental, deriva e defeito do instrumento?

**R:** A prioridade é correlacionar a instabilidade com as condições ambientais e verificar a deriva com método metrológico antes de concluir por defeito ou fazer ajuste imediato. Em sensores de estado sólido, umidade da amostra e temperatura alteram a adsorção na superfície e podem mudar a resposta sem indicar falha eletrônica. Se a tecnologia aplicada também for sensível a vapor d’água ou a névoa, a leitura pode incorporar interferência do meio e não apenas variação real de gás. Em seguida, a aferição deve comparar o desempenho com padrão e a deriva deve ser verificada usando o mesmo gás de referência no início e no fim do intervalo, para separar desvio de calibração de mudança causada pelo ambiente. Como desvios de calibração são mais frequentes que defeitos, substituição imediata não é a primeira conclusão; se houver desvio anormal ou dúvida sobre falha oculta, cabem investigação específica e ações detectivas.

### Sistemas e equipamentos de salvatagem

**facil · APROVADA · corrigida**  
_Nota(s): Pontos de reunião e interfaces com o refúgio temporário na resposta a emergências_

**P:** O que significa estruturar a resposta a emergências com pontos de encontro distribuídos por função e localização em uma unidade offshore?

**R:** Significa que a resposta a emergências não é organizada em um único ponto de encontro genérico para todos. Ela é estruturada com funções e respectivos pontos de encontro definidos em diferentes locais da unidade. No FPSO, essa estrutura incluía locais como a CCR, a enfermaria, a sala de controle da praça de máquinas, o bote de resgate rápido, locais com equipamentos de brigada e o refeitório, usado como refúgio temporário.

**media · REPROVADA: suporte**  
_Nota(s): Pontos de reunião e interfaces com o refúgio temporário na resposta a emergências_

**P:** Em uma unidade offshore, os locais de apresentação do pessoal já estão definidos por função em diferentes pontos da instalação. Como essa definição prévia influencia a organização inicial da resposta, a concentração de equipes e a contabilização de pessoal?

**R:** Ela tende a tornar a resposta inicial mais organizada, porque cada função se apresenta no local previamente previsto para seu grupo, em vez de convergir para um único ponto genérico. Como os pontos de encontro são distribuídos por função e localização na unidade, a concentração de equipes em um só local é reduzida e a alocação inicial do pessoal fica mais estruturada. Além disso, quando existe um local esperado para cada função, a conferência de presença e a identificação de ausências ou desvios ficam mais objetivas na fase inicial da emergência.

**dificil_A · APROVADA**  
_Nota(s): Condições de acesso, descida ao mar e lançamento seguro de life rafts_

**P:** Em um abandono, a tripulação consegue chegar a uma estação de life raft throw-over por uma rota física existente. Porém, no ponto de lançamento há exposição relevante a radiação térmica e fumaça, e o único modo prático de alcançar a balsa já implantada é descer por corda com nós e nadar alguns metros até a painter line. A balsa está disponível e pode ser lançada. Esse arranjo torna o abandono realmente viável?

**R:** Não. A cadeia acesso–descida–alcance da balsa–embarque não é executável com segurança apenas porque existe rota física e a balsa está a bordo. Neste cenário, o arranjo falha em dois pontos críticos. Primeiro, a entrada física no mar aparece como etapa necessária para conectar-se à balsa, quando deveria ser último recurso. Além disso, corda com nós não é meio controlado de descida, porque depende de força e destreza sob emergência. Segundo, o ponto de lançamento/embarque e, quando necessário, a rota de acesso precisam permanecer disponíveis sob os efeitos do cenário, com proteção suficiente contra radiação térmica e fumaça; se o ponto relevante está exposto, a disponibilidade operacional da estação fica comprometida. Portanto, a presença da balsa não basta: sem descida controlada, acesso funcional à painter line e proteção adequada da rota e do ponto de embarque, o abandono não é considerado viável.

**dificil_B · REPROVADA: suporte, jurisdicao, codigo:referencia_alternativas · corrigida**  
_Nota(s): Redundância e disponibilidade de rotas para escape-to-sea; Dependência do refúgio temporário quando o abandono é degradado; Proteção e disponibilidade de rotas de fuga, pontos de embarque e Temporary Refuge em cenários de incêndio, fumaça e explosão_

**P:** Em um FPSO, uma estação de abandono fica indisponível após falha mecânica. O plano passa a concentrar o pessoal no Temporary Refuge (TR) até usar rotas remanescentes para outro ponto de embarque com baleeira throw-over. Ao mesmo tempo, há tendência de piora na detecção de gás associada ao TR, e a rota alternativa pode ficar exposta a fumaça e radiação térmica. Com base no material, qual critério técnico deve orientar a decisão sobre continuar operando nessa condição degradada?

**R:** Pelo critério técnico do material, a decisão deve se basear na cadeia remanescente completa de proteção e abandono, e não apenas na existência de outro meio final. Deve-se verificar se ainda há rotas seguras até o escape-to-sea, mantidas e disponíveis, e se a rota remanescente e o ponto de embarque com throw-over permanecem utilizáveis pelo tempo requerido, com proteção contra fumaça e radiação térmica e iluminação de emergência. Como a perda de um meio de abandono aumenta a dependência do TR, também pesa a capacidade de o TR manter muster e habitabilidade, com limites atmosféricos definidos. A tendência de piora na detecção de gás e em sistemas associados ao TR é sinal de risco crescente e deve ser tratada por gestão preventiva baseada em desempenho, não por correção apenas após falha. Em cenários com potencial de explosão, entra também a proteção do TR contra sobrepressão.

## Utilidades, geração de energia e sistemas auxiliares

### Geração e distribuição de energia elétrica

**facil · APROVADA**  
_Nota(s): PMS/EMS como supervisão integrada da geração, sincronismo e partilha de carga_

**P:** Qual é a função do PMS em uma rede elétrica offshore com múltiplos geradores conectados a um mesmo barramento?

**R:** O PMS faz a supervisão integrada da rede elétrica e da geração. Ele monitora continuamente variáveis como tensão, corrente e fator de potência, além de receber sinais de medição, proteção, controle de motores e acionamentos. Com essa visão do estado elétrico, comanda a partida e a conexão de geradores ao barramento, realiza a partilha de carga entre as unidades e controla ou monitora frequência e sincronismo. Sua função prática é transformar a percepção em tempo real da rede em ação coordenada sobre a geração, para prevenir sobrecargas, preservar a integridade dos equipamentos e manter o fornecimento das cargas essenciais.

**media · APROVADA · corrigida**  
_Nota(s): PMS/EMS como supervisão integrada da geração, sincronismo e partilha de carga_

**P:** Em uma unidade offshore com variação relevante de demanda, por que a aquisição contínua de tensões, correntes e fator de potência é importante para decidir a conexão de outro gerador ao barramento e a partilha de carga?

**R:** Porque essas variáveis mostram, em tempo real, a condição elétrica do barramento e a evolução da carga. Ao integrar esses dados com sinais de proteção, controle de motores e acionamentos, o sistema ganha visibilidade para reconhecer aumento de demanda, aproximação de sobrecarga ou comportamento anormal de grandes consumidores. Com base nisso, o PMS pode decidir a partida e a conexão de outro gerador ao barramento sob supervisão de frequência e sincronismo e, depois, redistribuir a carga entre as máquinas em operação. Essa lógica ajuda a prevenir sobrecargas e manter a estabilidade, especialmente quando diferentes modos operacionais provocam mudanças significativas de demanda.

**dificil_A · REPROVADA: suporte**  
_Nota(s): Arranjos de partida de unidades geradoras e automação da lógica de partida_

**P:** Uma FPSO possui vários geradores e a partida de um deles vinha sendo feita por bloco de partida axial. Esse arranjo apresenta falhas operacionais recorrentes, com impacto na disponibilidade da unidade, e a equipe avalia migrar para um Conversor Estático de Frequência (SFC) com sequência de partida automática integrada ao controle dos geradores. Tecnicamente, por que essa substituição é justificável?

**R:** A substituição é justificável porque o problema deixou de ser apenas “conseguir partir” a máquina e passou a ser garantir partida confiável. O bloco de partida axial atendia funcionalmente tanto à partida apenas do gerador, inclusive para operação como compensador síncrono, quanto à partida da unidade completa para geração de potência ativa. Porém, como esse arranjo apresentava problemas operacionais frequentes, ele comprometia a confiabilidade das unidades. Nessa condição, trocar o bloco por um SFC é coerente com o objetivo de reduzir a recorrência das falhas no processo de partida e tornar a colocação da unidade em serviço mais confiável. Além disso, o SFC tornou o processo de partida totalmente automatizado, e o sistema já dispõe de uma unidade de controle automática para comandar a partida de todos os geradores. Assim, a solução melhora simultaneamente a confiabilidade da partida e sua coordenação automática no conjunto gerador.

**dificil_B · APROVADA · corrigida**  
_Nota(s): Filosofia de geração principal, emergência e realimentação do quadro principal; Continuidade de alimentação de cargas essenciais e reconfiguração em contingências elétricas; Redundância e reconfiguração da distribuição para sustentar consumidores essenciais e de controle_

**P:** Após perda total da geração principal, a geração de emergência está disponível e as permissivas de back feeding foram atendidas, energizando sistemas/equipamentos ligados ao painel principal. Ao mesmo tempo, um dos conjuntos de 24 Vcc que alimenta CLP e painéis de controle falhou, e o TIE ainda não foi fechado. Há tensão em barramentos, mas algumas funções de controle seguem indisponíveis. Que diagnóstico explica esse quadro e, para restabelecer essas funções de controle afetadas, qual reconfiguração deve ser feita?

**R:** O quadro indica que a realimentação em CA por back feeding e a alimentação auxiliar em 24 Vcc são camadas distintas. O back feeding pode energizar sistemas/equipamentos ligados ao painel principal, mas isso não transfere automaticamente os consumidores de CLP e painéis de controle do conjunto de 24 Vcc que falhou. Por isso, pode existir tensão em barramentos e ainda assim permanecer indisponibilidade de funções de controle. Para restabelecer essas funções afetadas no cenário dado, deve-se reconfigurar o sistema de 24 Vcc, fechando o TIE para que o conjunto remanescente alimente também os consumidores do ramo falhado. Isso é viável porque cada conjunto de 24 Vcc tem capacidade para suprir 100% da demanda do quadro correspondente.

### Sistema de utilidades

**facil · REPROVADA: suporte**  
_Nota(s): Gestão energética e hídrica baseada em M&V e indicadores em sistemas de utilidades_

**P:** Por que a confiabilidade dos dados de medição em um sistema de utilidades depende de inspeção e calibração periódica, e como isso afeta a avaliação de desempenho energético?

**R:** Porque os dados só são confiáveis para gestão e avaliação de desempenho quando os equipamentos de medição mantêm sua condição metrológica assegurada por inspeções e calibrações periódicas. Sem essa confiabilidade, o uso dos dados fica condicionado e a caracterização rigorosa do desempenho energético perde sustentação. Na prática, isso compromete a medição e verificação do consumo, enfraquece o monitoramento contínuo e reduz a capacidade de gerir, monitorar e reportar o uso de energia de forma consistente. Como consequência, a unidade passa a ter menor base técnica para avaliar o desempenho real e para sustentar ações de eficiência energética ao longo da operação.

**media · APROVADA · corrigida**  
_Nota(s): Gestão energética e hídrica baseada em M&V e indicadores em sistemas de utilidades_

**P:** Uma unidade offshore quer reduzir o consumo de energia e água nas utilidades, mas ainda não mapeou claramente os principais pontos de consumo, as quantidades e qualidades requeridas em cada aplicação nem os pontos de geração de efluentes. Como essa lacuna afeta a identificação de oportunidades de otimização?

**R:** Essa lacuna dificulta a identificação de oportunidades de otimização porque o conhecimento das atividades industriais é fundamental para reconhecer os principais pontos de consumo, as quantidades e qualidades exigidas em cada aplicação e os pontos de geração de efluentes. Sem essa base, fica prejudicada a identificação de oportunidades de adequação do uso de energia e da água em cada unidade. Também fica comprometida a definição de uma estratégia aderente ao perfil de operação dos equipamentos, que é a condição para implementar medidas de eficientização voltadas à redução de consumos, custos econômicos e descargas de águas residuais industriais.

**dificil_A · APROVADA · corrigida**  
_Nota(s): Falhas em utilidades térmicas e de resfriamento: segregação de circuitos e consequências da perda de circulação_

**P:** Durante a partida de um sistema de transferência de calor em fase líquida, o queimador principal permanece admitindo combustível, mas as bombas de circulação não entram em operação. Pouco depois, a temperatura do fluido na saída da câmara de combustão sobe rapidamente. Se essa condição for mantida, qual é o encadeamento de falha mais provável e por que ela deve ser tratada como condição de emergência, e não apenas como perda de bombeio?

**R:** O encadeamento mais provável é superaquecimento do fluido na região aquecida porque o queimador continua fornecendo calor sem circulação efetiva. Com isso, o fluido se expande e a pressão no circuito aumenta rapidamente. Se essa pressão exceder a resistência do tanque de expansão, pode ocorrer ruptura mecânica, com extravasamento do fluido aquecido sobre o aquecedor e para a área do convés. Essa perda de contenção pode ser seguida de ignição. Por isso, a situação deve ser tratada como emergência: não é apenas indisponibilidade de bombeio, mas uma condição que pode evoluir para sobrepressão, falha mecânica e incêndio. Nesse tipo de sistema, recomenda-se monitoramento contínuo da temperatura imediatamente a jusante da câmara de combustão.

**dificil_B · APROVADA**  
_Nota(s): Segurança operacional em sistemas de heating medium em fase líquida: superaquecimento por perda de circulação, sobrepressão e salvaguardas; Intertravamentos e sistemas de proteção para desligamento seguro em turbinas, compressores e utilidades; Falhas em utilidades térmicas e de resfriamento: segregação de circuitos e consequências da perda de circulação_

**P:** Na retomada de operação de um FPSO, perde-se um circuito de água de resfriamento que atende apenas cargas de área não classificada, enquanto o queimador principal do heating medium é liberado sem confirmação clara de circulação. Em seguida, a temperatura a jusante da câmara de combustão sobe e a pressão do circuito aumenta rapidamente. Qual condição deve ser tratada como ameaça imediata à integridade e ao incêndio, e que barreira de proteção deveria ter impedido a energização térmica?

**R:** A ameaça imediata é o heating medium com fonte térmica ativa sem circulação comprovada. Em circuito líquido, a perda de circulação remove a via de retirada de calor da região aquecida; se o queimador permanece habilitado, o fluido superaquece, expande-se, a pressão sobe rapidamente e pode romper o tanque de expansão, com extravasamento sobre superfícies quentes e ignição. Já a perda de apenas um circuito segregado de água de resfriamento tem alcance funcional limitado aos consumidores daquele circuito, não equivalendo por si só à perda total da utilidade. A barreira que deveria ter atuado antes da admissão de combustível é o intertravamento permissivo que bloqueia a válvula de combustível do queimador principal quando as bombas de circulação não estiverem operando. Como camadas complementares, cabem monitoramento contínuo de temperatura a jusante da câmara de combustão e contenção/alívio adequados no tanque de expansão.

## Descomissionamento e Gestão do Ciclo de Vida da Unidade

### Geral

**facil · REPROVADA: suporte**  
_Nota(s): Estratégia de ciclo de vida, extensão de vida e preparação para descomissionamento em unidades flutuantes_

**P:** Por que a gestão do ciclo de vida de uma unidade flutuante deve começar na fase de projeto, e não apenas durante a operação ou perto do descomissionamento?

**R:** Porque decisões tomadas no projeto já permitem reduzir, com menor custo, impactos ambientais, sociais e de saúde e segurança do descomissionamento, por meio de medidas preventivas como melhor arranjo de componentes, afastamento de áreas sensíveis e provisão de garantias financeiras. Além disso, o gerenciamento de riscos precisa nascer nessa fase, com antecipação de desvios, condições inseguras e falhas de camadas de proteção, e seguir até a desativação. Quando a gestão começa cedo, inspeção e manutenção passam a ser controladas ao longo de todo o ciclo de vida, formando a base histórica necessária para decisões futuras de extensão de vida ou descomissionamento. Se isso é deixado para o fim, a unidade tende a chegar à etapa final com integridade menos conhecida e decisões mais reativas.

**media · REPROVADA: suporte**  
_Nota(s): Estratégia de ciclo de vida, extensão de vida e preparação para descomissionamento em unidades flutuantes_

**P:** Uma unidade flutuante se aproxima do fim da vida de projeto, mas o operador dispõe de registros de condição, inspeção e manutenção acumulados ao longo dos anos. Por que a extensão de vida deve ser tratada como processo contínuo de preparação, e o que precisa sustentá-la tecnicamente?

**R:** Ela deve ser contínua porque envelhecimento não se define pela idade cronológica, mas pelo conhecimento da condição real do ativo e dos fatores que influenciaram sua degradação ao longo da operação. Por isso, preparar a extensão de vida apenas no fim da vida de projeto é inadequado. Tecnicamente, a decisão precisa ser sustentada por uma metodologia de life extension com avaliação completa da unidade para verificar se a integridade estrutural e mecânica permanece suficiente para operar com segurança além da vida de projeto. Isso não deve se basear apenas em achados dispersos de auditoria ou correções pontuais, mas em avaliações técnicas formais e estruturadas voltadas a demonstrar a adequação das barreiras de segurança. O histórico controlado de inspeção e manutenção é parte essencial dessa base técnica.

**dificil_A · REPROVADA: correcao_tecnica, suporte**  
_Nota(s): Controle do retorno ao serviço após lay-up ou intervenção_

**P:** Após 18 dias em lay-up, um circuito de processo de um FPSO será devolvido à operação depois de intervenção. A manutenção foi encerrada, mas ainda há isolamentos temporários sob controle documental e existe dúvida se o volume interno deve ser inertizado antes da partida. Qual sequência de decisão e execução é tecnicamente mais adequada para o retorno ao serviço, e por que essa etapa deve ser tratada como gestão de mudanças, e não como simples continuação da manutenção?

**R:** A sequência adequada é conduzir o retorno ao serviço por procedimento específico da instalação, sob PTW (permissão de trabalho) e certificados de isolamento, tratando a reintrodução de fluido como etapa própria; avaliar então a necessidade de inertização; somente depois retirar os isolamentos de forma controlada e confirmar a recomposição final necessária para operar, incluindo a reinstalação do tampão cap roscado nos drenos; por fim, introduzir os fluidos. Essa lógica é necessária porque o risco relevante surge justamente quando o sistema volta a receber inventário, pressão e temperatura: a introdução de fluidos em sistema recém-mantido ou que esteve ocioso tem perigos próprios e pode ser tratada como gestão de mudanças. Assim, a decisão não pode se limitar ao encerramento da manutenção, mas deve assegurar que a configuração liberada para trabalho foi realmente recomposta para operação segura antes da partida.

**dificil_B · APROVADA · corrigida**  
_Nota(s): Avaliação inicial da unidade para definir remoção, reboque e local de desmontagem; Riscos e restrições para retirada da FPSO da locação e reboque até estaleiro; Condição de limpeza, drenagem e isolamento da planta para transporte ou reboque_

**P:** Uma FPSO em fim de vida teve avaliação inicial favorável de integridade, navegabilidade e de parte dos sistemas ainda utilizáveis na desativação. A equipe propõe rebocá-la a estaleiro para reduzir exposição offshore, mas a unidade ainda não foi colocada na condição de limpeza e isolamento para reboque, há espécies exóticas invasoras no casco e a retirada da locação ocorreria próxima a instalação adjacente com risers/poços. Qual estratégia é tecnicamente mais defensável e por quê?

**R:** A desmontagem offshore é a estratégia mais defensável nesse cenário. A avaliação inicial favorável não basta para aceitar o tow-out, porque o reboque só pode ser considerado depois de a unidade atingir a condição requerida para navegação ou reboque, com limpeza da planta e tanques, drenagem, ventilação, purga, lavagem, remoção de TENORM e isolamento contra recontaminação; depois disso ainda podem ser necessários reforços e ajustes estruturais. Além disso, a presença de espécies exóticas invasoras torna o método de reflutuação e reboque não recomendado, pelo risco de disseminação. E, se ocorrer perda de posição durante a retirada próxima a instalação adjacente com risers/poços, as consequências podem incluir colisão ou liberação de hidrocarbonetos. Assim, o reboque fica tecnicamente desfavorecido.

## Gestão do Desempenho Empresarial (KPI)

### Gestão do Desempenho Empresarial (KPI)

**facil · APROVADA**  
_Nota(s): KPIs para segurança de processo e gestão dinâmica de risco operacional_

**P:** Por que indicadores de input, como horas dedicadas a HSE e número de inspeções, não bastam isoladamente para medir o desempenho em segurança de processo?

**R:** Porque eles mostram esforço aplicado, mas não demonstram, por si só, se houve redução real do risco nem recuperação da função de segurança. Em operação, desvios de processo e de manutenção podem degradar ou inibir temporariamente barreiras, e essa mudança nem sempre é capturada de imediato pelas análises de risco usuais. Assim, uma instalação pode apresentar muita atividade de HSE e ainda manter exposição elevada. Para medir desempenho de forma útil, os indicadores precisam evidenciar o efeito sobre a condição das barreiras e ser complementados por resultados qualitativos que mostrem o impacto das ações executadas.

**media · APROVADA**  
_Nota(s): KPIs para segurança de processo e gestão dinâmica de risco operacional_

**P:** Um elemento crítico de segurança (SCE) foi identificado como degradado e a unidade pretende avaliar se pode continuar operando. Quais elementos de governança devem existir nessa avaliação de risco?

**R:** Devem existir, no mínimo, um procedimento formal e robusto que defina como a avaliação de risco será feita, quais são os níveis de autoridade para decidir, qual expertise técnica deve participar e quais revisões são exigidas. A avaliação deve considerar o papel do SCE como barreira contra major accident hazards, para sustentar medidas mitigatórias e, se necessário, barreiras adicionais. Também deve haver registro das avaliações e auditoria regular desses registros. Como o risco combinado pode ser elevado mesmo quando avaliações individuais parecem adequadas, o processo deve prever revisões gerais periódicas com expertise apropriada, sem depender apenas da gestão offshore. Além disso, dados de desempenho, KPIs e achados de auditoria devem ser reportados ao nível sênior, com ações decorrentes.

**dificil_A · REPROVADA: suporte · corrigida**  
_Nota(s): Qualidade dos dados e trending como base de KPIs preditivos de confiabilidade dos ativos_

**P:** Em um conjunto motobomba, o KPI preditivo de confiabilidade ficou inconsistente com a condição observada após a troca do motor. No sistema, a identificação do conjunto é feita pela localização funcional, e o motor substituído permaneceu com o mesmo tag ID do anterior. Qual é a causa mais provável dessa inconsistência no KPI?

**R:** A causa mais provável é a perda de rastreabilidade do item físico monitorado. Quando o sistema identifica o equipamento pela localização funcional, um componente novo pode herdar o mesmo tag ID do componente substituído. Nesse caso, o histórico de desempenho pode deixar de representar claramente qual item físico gerou cada dado. Isso distorce a base usada no KPI preditivo, porque o indicador passa a combinar registros de equipamentos diferentes sob a mesma identificação. Assim, a inconsistência do KPI decorre principalmente da confusão entre o histórico do motor antigo e o do motor novo.

**dificil_B · REPROVADA: suporte**  
_Nota(s): Sistema de KPIs alinhado à estratégia e à criação de valor; KPIs econômicos e operacionais para sustentabilidade do negócio em FPSOs; Risco de processo, degradação de barreiras e impacto no desempenho empresarial_

**P:** Em um FPSO sob preço de petróleo pressionado, a gestão reforçou metas de redução de OPEX e manutenção da produção. Nas semanas seguintes, margem e volume melhoraram, mas cresceram adiamentos de manutenção e desvios operacionais com potencial de reduzir a efetividade de funções de segurança. Ao revisar o painel estratégico, qual mudança de desenho é mais adequada para decidir se o ativo está realmente criando valor, e não apenas antecipando ganho econômico à custa de risco futuro?

**R:** A revisão deve substituir um painel centrado em volume e custo por um sistema de KPIs que explicite a cadeia causal entre estratégia, decisões operacionais, manutenção, resultado econômico e risco de processo. Em ambiente mutável, o sistema de indicadores deve apoiar a gestão estratégica e o entendimento da criação de valor, por meio de um mapa sistêmico com inter-relações entre variáveis-chave e associação de eventos relevantes às variáveis usadas para monitorar seus efeitos nos resultados. Sob pressão de margem, os KPIs precisam mostrar simultaneamente efeitos sobre CAPEX/OPEX e sobre a capacidade de sustentar receita, evitando premiar eficiência local sem consequência econômica real. Como desvios de produção e manutenção podem degradar funções de segurança e aumentar frequência e/ou severidade de cenários de risco, o painel deve incorporar indicadores que revelem esses desvios e seus impactos sobre continuidade operacional e sustentabilidade do negócio, não apenas ganho financeiro imediato.

## Logística, Suprimentos e Movimentação de Cargas

### Logística e Suprimento Offshore

**facil · APROVADA · corrigida**  
_Nota(s): Operações submarinas e recursos de apoio: como a seleção de meios e sistemas muda a logística e as interfaces com a unidade_

**P:** Por que a eliminação do umbilical em operações com AUV reduz a exigência sobre o sistema de lançamento e sobre a embarcação de apoio, especialmente com o aumento da profundidade?

**R:** Porque o AUV, ao dispensar o umbilical, também dispensa a necessidade de recursos de lançamento mais robustos ligados a esse tipo de operação, como guincho e pórtico de lançamento com compensador de heave. Isso simplifica o lançamento e reduz a exigência de recursos sobre a embarcação de apoio. Esse efeito tende a aumentar com a profundidade porque, segundo o fato apresentado, o impacto dessas reduções é diretamente proporcional à profundidade.

**media · APROVADA**  
_Nota(s): Operações submarinas e recursos de apoio: como a seleção de meios e sistemas muda a logística e as interfaces com a unidade_

**P:** Uma campanha submarina inicialmente prevista para inspeção de rotina passou a incluir abertura de válvulas e cortes localizados no fundo do mar. Como essa mudança afeta a escolha entre AUV e ROV?

**R:** A escolha passa a favorecer o ROV. Para inspeção, o AUV reduz requisitos de lançamento e de embarcação por não usar umbilical, o que simplifica a logística. Porém, quando o escopo inclui intervenção física, como abertura e fechamento de válvulas, cortes e hidrojateamento, o requisito principal deixa de ser apenas cobertura de inspeção e passa a ser capacidade operacional de atuar sobre os componentes submarinos. O ROV atende esse tipo de tarefa porque dispõe de manipuladores e sistemas de operação remota para executar intervenções, embora isso exija sala de controle dedicada, equipe mínima específica e operação de guincho na borda da unidade, aumentando as interfaces logísticas e operacionais.

**dificil_A · REPROVADA: suporte · corrigida**  
_Nota(s): Gestão de estoques e sobressalentes no suprimento offshore: criticidade, risco, custo total e nível de serviço_

**P:** Uma operadora offshore avalia cortar o estoque de um componente cuja falha afeta uma função crítica de segurança e também pode prolongar a perda de produção até a restauração da função. O mercado fornecedor é complexo, e a área usuária exige alto nível de serviço. Nessa condição, qual decisão deve ser priorizada: reduzir estoque, manter o sobressalente disponível ou concentrar o esforço em parceria com fornecedor?

**R:** Deve-se priorizar manter o sobressalente disponível. Como o item é crítico, a decisão deve ser guiada por criticidade, risco da falha e necessidade de reduzir o tempo de restauração da função. Se o item faltar quando requerido, ficam comprometidas tanto a mitigação de consequências de segurança quanto a redução do downtime de produção. Além disso, alto nível de serviço não pode ser avaliado só pelo custo interno do estoque, porque serviço, custo e desempenho do suprimento estão diretamente relacionados. A complexidade do mercado fornecedor pesa na estratégia de compras e sourcing, e parcerias podem apoiar redução de custo total e melhora do atendimento, mas, neste caso, não substituem a necessidade de disponibilidade do item crítico quando exigido.

**dificil_B · REPROVADA: suporte · corrigida**  
_Nota(s): Embarcações de apoio offshore e configuração das cargas de suprimento, com foco no PSV; Planejamento logístico de suprimentos com PSV sob restrições de arrumação no convés; Priorização logística offshore sob restrições de armazenamento, POB e transporte_

**P:** Um FPSO com baixa armazenagem pede, na mesma viagem de PSV, contêineres de materiais de manutenção, consumíveis operacionais e volumes longos de geometria desfavorável. Pela lista de pesos, tudo caberia, mas o plano real não fecha no convés. Como decidir o que embarca nesta viagem e por que seria tecnicamente errado usar só a tonelagem total como critério?

**R:** A decisão deve partir do limitante físico real da viagem: a área de convés e a geometria de arrumação. No PSV, a carga de convés fica no nível do convés, sem empilhamento, e não pode ser rotacionada livremente; assim, uma carteira aparentemente viável em peso pode falhar no carregamento real. Nessa situação, devem ser priorizados os itens cuja falta mais afeta a continuidade do trabalho na unidade, deixando para viagem posterior os itens de menor criticidade entre os que disputam a área de convés disponível. O erro técnico de usar apenas a tonelagem é supor que capacidade útil equivale a peso total, quando o gargalo da viagem está no deck cargo, governado por área e ajuste geométrico dos volumes.

### Movimentação de Cargas

**facil · REPROVADA: jurisdicao, sem_generalizacao · corrigida**  
_Nota(s): Controle contínuo da operação de içamento por planejamento, supervisão e handover_

**P:** Qual é a função do lifting plan em uma operação de içamento em relação à execução da tarefa e à escolha do equipamento?

**R:** O lifting plan tem a função de descrever a operação de içamento em instruções passo a passo para a execução da tarefa e de informar os detalhes do equipamento a ser usado. Assim, ele define como o içamento deve ser realizado e qual equipamento será utilizado na atividade. Além disso, o lifting plan deve ser produzido por uma Pessoa Competente ou, no mínimo, autorizado por uma Pessoa Competente.

**media · APROVADA**  
_Nota(s): Controle contínuo da operação de içamento por planejamento, supervisão e handover_

**P:** Em um içamento, o plano foi emitido, mas o supervisor se afasta da área e a equipe continua o trabalho com pouco monitoramento em campo. Qual é o papel técnico do supervisor de içamento e da organização para manter a aderência entre o plano, a execução e o monitoramento do trabalho?

**R:** O supervisor deve manter acompanhamento em campo para que a execução permaneça aderente ao método autorizado, assegurando continuidade entre plano, trabalho real e monitoramento da atividade. A organização, por sua vez, deve ter procedimentos efetivos de supervisão e monitoramento, verificar se esses procedimentos funcionam na prática e identificar fatores que prejudiquem a supervisão efetiva, como falta de tempo ou treinamento insuficiente do supervisor. Isso é relevante porque supervisão inadequada aparece como causa subjacente importante de acidentes, e a continuidade do trabalho sem supervisão adequada favorece desvio entre o que foi planejado e o que é executado.

**dificil_A · APROVADA**  
_Nota(s): Limites ambientais e classificação dinâmica em içamentos entre unidade e embarcação_

**P:** Durante a transferência de uma carga entre uma unidade offshore e uma embarcação de apoio, o peso suspenso permanece dentro da capacidade nominal estática do guindaste. Porém, o movimento relativo entre os cascos aumentou, a equipe passou a ter dificuldade para estimar o pouso no convés e a tag line começou a alternar entre folga excessiva e trancos. Qual decisão é tecnicamente correta e como justificá-la?

**R:** A decisão correta é interromper a manobra até que a condição volte a ser compatível com o regime dinâmico aplicável. Nessa situação, o critério não é o peso estático da carga, porque a transferência entre unidade e embarcação é um içamento dinâmico, no qual o movimento relativo pode elevar transitoriamente o esforço e o momento no guindaste acima do correspondente ao peso real; por isso, a referência deve ser o load chart dinâmico, mais restritivo. A dificuldade de estimar o pouso indica perda de controle da condição operacional, e a tag line com folga variável e trancos mostra efeito do movimento da embarcação sobre o comprimento efetivo e a trajetória do cabo, aumentando risco de perda de consciência situacional e emaranhamento. Além disso, as funções de segurança do guindaste não devem ser tratadas como autorização para operar fora das limitações do equipamento. Com essa degradação, a exposição da equipe na zona de manobra deixa de ser aceitável.

**dificil_B · REPROVADA: suporte**  
_Nota(s): Supervisão, monitoramento em tempo real e verificação de conformidade em operações de içamento offshore; Trajetória, altura livre e controle de interferências na movimentação de cargas; Interferências mecânicas, tração anômala e movimentos relativos na avaliação da capacidade de içamento_

**P:** Em um içamento próximo a estruturas, o operador confirma resposta ao comando de descida, mas o rigger não observa avanço coerente da carga no trajeto. O indicador de peso não sugere sobrecarga, a visibilidade do operador é limitada e parte da equipe interpreta a situação como simples resistência da carga no apoio. Como o supervisor deve diagnosticar a condição e qual decisão operacional deve priorizar?

**R:** O quadro deve ser tratado primeiro como possível interferência mecânica na trajetória ou na linha, e não como mera resistência da carga. A combinação de comando executado, ausência de movimento coerente da carga e indicação de peso aparentemente normal é compatível com snag, em que parte da sustentação migra para a estrutura e o indicador deixa de representar corretamente a carga no guincho. Com visibilidade limitada, o diagnóstico deve cruzar comportamento real da carga, trajetória da linha e pontos potenciais de contato previamente mapeados, com comunicação explícita de verificação incremental do movimento. A decisão prioritária é interromper a manobra, confirmar caminho livre da linha e da carga e investigar interferências antes de prosseguir, porque insistir pode acumular folga/energia e levar à liberação súbita do ponto preso.

## Manutenção, Inspeção e Integridade de Ativos

### Apoio Técnico e Manutenção em um FPSO (Laboratório, Oficinas, Pipe Shop)

**facil · APROVADA · corrigida**  
_Nota(s): Boas práticas de qualidade em ensaios laboratoriais que suportam decisões de integridade_

**P:** Qual é a finalidade da limpeza prévia do equipamento de amostragem e de ensaio antes de testes laboratoriais de corrosão?

**R:** A limpeza prévia tem a finalidade de evitar contaminações no equipamento de amostragem e de ensaio que possam falsear os resultados do teste de corrosão. Ela deve ser realizada antes do ensaio, conforme os métodos estabelecidos, para reduzir a influência de resíduos do próprio sistema sobre o resultado obtido.

**media · APROVADA · corrigida**  
_Nota(s): Boas práticas de qualidade em ensaios laboratoriais que suportam decisões de integridade_

**P:** Em um FPSO, um resultado laboratorial será usado no controle de qualidade. A coleta foi feita em um ponto que pode não representar a corrente real, e há dúvida se o circuito de amostragem e ensaio estava limpo. Como essas duas condições afetam a confiabilidade da conclusão técnica?

**R:** A confiabilidade da conclusão técnica fica comprometida por dois mecanismos. Se a amostra não for representativa da corrente de produto ou do local de armazenamento avaliado, o resultado do ensaio pode não corresponder às condições reais do sistema, reduzindo a confiabilidade do controle de qualidade. Se o equipamento de amostragem e de ensaio não tiver sido limpo conforme método estabelecido antes do teste de corrosão, resíduos podem contaminar o ensaio e falsear o resultado. Assim, a confiança no dado depende de a amostra representar a condição real e de o sistema de amostragem e ensaio estar previamente limpo.

**dificil_A · APROVADA**  
_Nota(s): Sistema metrológico do laboratório e rastreabilidade aos padrões_

**P:** Em um FPSO, o laboratório precisa calibrar um transmissor e há duas rotas possíveis para chegar ao padrão de referência. A primeira usa menos transferências de calibração; a segunda adiciona elos intermediários, mas mantém certificados dos padrões envolvidos. Se ambas forem formalmente documentadas, qual rota tende a produzir o resultado final metrologicamente mais robusto e por quê?

**R:** A rota com menos transferências tende a ser mais robusta. Em uma hierarquia de calibração, cada etapa depende da anterior e acrescenta sua contribuição à incerteza; por isso, a incerteza de medição aumenta ao longo da sequência de calibrações. Assim, ao adicionar elos intermediários, o resultado final tende a carregar maior incerteza. Os certificados, por si só, não eliminam esse efeito: a rastreabilidade metrológica só se caracteriza por uma cadeia ininterrupta vinculada a padrão nacional ou internacional, com incerteza documentada, procedimento documentado e competência técnica reconhecida. Portanto, entre duas cadeias válidas, a menos extensa tende a sustentar melhor a confiabilidade do resultado, desde que preserve a rastreabilidade metrológica requerida.

**dificil_B · REPROVADA: suporte · corrigida**  
_Nota(s): Planejamento de inspeção, monitoramento de integridade e gestão de recomendações em FPSO; Registros, rastreabilidade e controle documental de serviços, inspeções e materiais em apoio técnico e manutenção de FPSO; Priorização de correções e resposta a não conformidades para evitar interdição de FPSO_

**P:** Em uma auditoria interna no FPSO, recomendações antigas de inspeção em equipamentos críticos aparecem com status divergente entre sistemas. Há ordens de serviço encerradas, mas os registros não ligam claramente cada achado à intervenção executada nem mostram inspeções, testes ou ensaios que aprovem o serviço. A operação afirma que os itens já foram tratados. Qual é o diagnóstico prioritário e qual decisão gerencial imediata reduz o risco de interdição?

**R:** O diagnóstico prioritário é falha de rastreabilidade e de fechamento técnico das recomendações de inspeção, e não mero problema administrativo. Em equipamentos críticos, o plano deve definir mecanismos de dano, periodicidades, recursos, prazos e a sistemática de registros. Além disso, a recomendação só reduz risco quando entra em uma sistemática formal com classificação, prazo compatível com o risco, acompanhamento e controle de qualidade mínimo por inspeções, testes ou ensaios que aprovem o serviço executado. Se os registros não conectam achado, ação corretiva e evidência de aprovação, a afirmação de que o item foi tratado não demonstra controle da integridade. A decisão imediata é reavaliar as pendências por criticidade, reconstituir a rastreabilidade, exigir evidência técnica de aprovação do serviço e, se necessário, adotar contingências ou restrições operacionais até o fechamento compatível com o risco.

### Cibersegurança e Integridade de Sistemas Digitais

**facil · REPROVADA: suporte, jurisdicao**  
_Nota(s): Autenticação robusta e gestão segura de credenciais em sistemas digitais que suportam funções essenciais_

**P:** Qual é a lógica do princípio do menor privilégio em sistemas digitais que suportam funções essenciais, e como ele reduz o impacto de uma credencial comprometida?

**R:** O princípio do menor privilégio consiste em limitar o acesso de cada usuário ao mínimo necessário para sua função. A lógica é separar a possibilidade de entrar no sistema da permissão para operar, alterar ou administrar recursos sensíveis, reduzindo o alcance de cada conta. Se uma credencial for comprometida, o dano potencial tende a ser menor porque o invasor herda apenas as permissões estritamente necessárias daquela conta, e não acessos amplos ou administrativos. Em sistemas sensíveis de OT, essa limitação deve ser combinada com autenticação adicional para acessos privilegiados, elevando a confiança sobre quem usa a conta e restringindo ainda mais o risco de uso indevido com alto impacto operacional.

**media · REPROVADA: suporte, jurisdicao**  
_Nota(s): Autenticação robusta e gestão segura de credenciais em sistemas digitais que suportam funções essenciais_

**P:** Em um sistema usado para funções essenciais, o cadastro aceita senhas fracas e depois ocorrem logins válidos associados a ações indevidas em contas de usuário. Como a exigência de qualidade de senha se relaciona com a confiabilidade da autenticação e com a prevenção desse tipo de uso indevido?

**R:** Se o sistema aceita senhas sem qualidade adequada, a autenticação perde confiabilidade porque um login válido deixa de representar, com segurança suficiente, que a conta está sendo usada pelo agente autorizado. Nesse caso, a entrada no sistema pode ocorrer por apropriação indevida da credencial, mesmo sem falha aparente no registro de login. Exigir qualidade de senha atua na origem do problema, fortalecendo a credencial antes do primeiro uso e reduzindo a chance de uso indevido da conta. Em sistemas que sustentam funções essenciais, isso é relevante porque o acesso deve ser autenticado de forma robusta e a proteção da credencial integra a defesa da integridade operacional.

**dificil_A · APROVADA**  
_Nota(s): Contenção, erradicação e recuperação de incidentes cibernéticos na automação industrial_

**P:** Durante uma perda de comunicação na rede de automação industrial, vários hosts deixam de trocar dados e o tráfego está degradado por grande volume de requisições dirigidas a um servidor. Ao mesmo tempo, uma estação apresenta indício de vírus, mas a origem do evento na rede não pode ser atribuída com confiança porque há sinais compatíveis com IP spoofing. Nessa condição, o que deve ser priorizado primeiro e em que momento cabe erradicação no ativo suspeito?

**R:** A prioridade inicial é tratar a indisponibilidade de comunicação como problema da infraestrutura de conectividade e acionar a engenharia de telecomunicações ou redes, porque falhas na RAI e defeitos de comunicação pertencem a essa camada técnica. O quadro descrito é compatível com DoS: acúmulo de requisições e inundação de pacotes degradam o tráfego até afetar o host alvo. Como a combinação com IP spoofing torna a origem virtualmente impossível de identificar no contexto, a decisão operacional não deve depender de atribuição imediata do atacante. A erradicação no ativo local passa a ser a ação prioritária quando houver evidência de que a estação está infectada, e então a remoção pode ser feita por deleção do arquivo associado ao vírus ou por reinstalação do sistema operacional.

**dificil_B · REPROVADA: correcao_tecnica, suporte**  
_Nota(s): Arquitetura integrada de redes e acesso remoto em sistemas digitais de FPSO; Gestão de alarmes como suporte à decisão para prevenir trips e shutdowns; Integridade operacional por alarmes, IHMs e diagnósticos de automação em ambientes IT/OT_

**P:** Após a ampliação da integração entre OT e camadas superiores de um FPSO, a sala de controle passou a relatar IHMs lentas, eventos inconsistentes e dificuldade para entender desvios. Em uma perturbação, houve grande volume de mensagens e a equipe não conseguiu separar falha de processo de falha digital. Qual diagnóstico deve ser priorizado para distinguir degradação da arquitetura integrada de problema de gestão de alarmes e de diagnósticos, e qual evidência aponta para cada origem principal?

**R:** A prioridade é separar integridade do fluxo de informação de qualidade do conteúdo mostrado ao operador. Como logs de alarmes alimentam tanto o sistema de alarme quanto o de gerenciamento, eles são a base para verificar se o problema nasce no transporte/disponibilização ou na configuração dos alarmes. Se os sintomas dominantes forem lentidão, inconsistência entre pontos de visualização e limitação de acesso/intervenção remota, a suspeita principal recai sobre a infraestrutura integrada e suas restrições de acesso. Se já houver excesso de alarmes em estado normal e, na perturbação, avalanche de alarmes, o indício principal é gestão de alarmes mal configurada. Se faltarem diagnósticos claros de PLCs, redes e dispositivos nas telas e bases usadas a bordo, a origem principal tende a ser deficiência na camada diagnóstica e na sua padronização/carregamento. Só depois disso faz sentido atribuir o quadro ao processo.

### Inspeção e Integridade

**facil · APROVADA · corrigida**  
_Nota(s): Inspeção Baseada em Risco e efetividade do plano de inspeção na gestão da integridade de FPSOs_

**P:** O que é Inspeção Baseada em Risco (IBR/RBI) e como a combinação de probabilidade e consequência de falha é usada para priorizar inspeção e manutenção de equipamentos em uma unidade de processo?

**R:** IBR/RBI é uma metodologia em que o risco orienta as decisões de inspeção e manutenção. Nessa abordagem, o risco é avaliado pela combinação entre probabilidade de falha e consequência de falha de cada equipamento. Para isso, o plano de inspeção deve ser coerente com os mecanismos de dano atuantes, e o histórico operacional é usado para atualizar o risco ao longo do tempo. Com essa combinação, torna-se possível determinar quais equipamentos devem receber inspeção e manutenção prioritariamente em uma unidade de processo.

**media · REPROVADA: suporte · corrigida**  
_Nota(s): Inspeção Baseada em Risco e efetividade do plano de inspeção na gestão da integridade de FPSOs_

**P:** Após uma inspeção, um vaso em um FPSO passa a apresentar indícios de um mecanismo de dano diferente do previsto, e as condições de operação da unidade também mudaram desde a última análise. Por que, em IBR/RBI, o plano de inspeção deve ser revisto nesse caso?

**R:** Porque, na IBR/RBI, o risco usado para orientar inspeção e manutenção é atualizado com base no histórico operacional e nas informações mais recentes do equipamento. Se a inspeção aponta indícios de um mecanismo de dano diferente do previsto, e a operação mudou, a avaliação anterior de risco pode deixar de representar a condição real do vaso. Isso pode alterar a probabilidade de falha e a priorização do equipamento. Além disso, diferentes planos de inspeção não têm a mesma capacidade de detectar e dimensionar dano, e sua confiabilidade depende da probabilidade de detecção das técnicas empregadas e do nível de amostragem. Por isso, o plano deve ser revisto para manter aderência ao risco atualizado e à efetividade esperada da inspeção.

**dificil_A · APROVADA · corrigida**  
_Nota(s): Inspeção estrutural do casco e do envelope externo com foco em estanqueidade, corrosão e perda de seção_

**P:** Em um FPSO no contexto de gestão de integridade sob referencial HSE/UK, pretende-se executar UWILD em vez de docagem. Na preparação, a equipe quer limitar o exame ao costado externo e tratar separadamente os compartimentos internos, embora no espaço de máquinas haja indícios de deterioração junto aos brackets na ligação com o topo do tanque, anteparas próximas aos poços de bilge e conexões laterais do casco. Qual lógica de inspeção e decisão preserva melhor o envelope do casco nesse caso?

**R:** A lógica correta é tratar o envelope do casco como uma barreira única de integridade. No contexto HSE/UK, se houver planejamento de UWILD, o envelope externo precisa estar coberto por um plano de inspeção de integridade desenvolvido e implementado. Esse plano não deve se limitar ao costado externo: deve integrar os compartimentos e áreas do escopo estrutural com atenção especial, no espaço de máquinas, à chapa do costado na região dos brackets ligados ao topo do tanque e às anteparas na região do topo do tanque e dos poços de bilge. Também deve abranger as conexões laterais do casco, incluindo ship side valves e tubulações associadas, porque afetam diretamente a estanqueidade. O exame deve ser complementado por medições de espessura e testes, conforme necessário, para identificar corrosão substancial, deformação significativa, fraturas, danos e outras deteriorações.

**dificil_B · REPROVADA: suporte**  
_Nota(s): Monitoramento do desempenho da proteção catódica e critérios de intervenção; Inspeção e manutenção da integridade de revestimentos em tanques e no envelope externo do casco; Avaliação de integridade de tanques por espessura, revestimento e proteção catódica_

**P:** Em um FPSO de casco simples, um tanque que armazenou água produzida apresenta perda de espessura em regiões com revestimento em condição ruim. Na mesma campanha, a eficácia da proteção catódica não pôde ser confirmada porque há indícios de queda de potencial e ânodos desgastados. Tecnicamente, isso pode ser tratado como anomalia localizada com simples acompanhamento, ou deve receber prioridade maior? Justifique a decisão pelo mecanismo de dano e pelo escopo mínimo de reavaliação.

**R:** Deve receber prioridade maior. A perda de espessura não deve ser lida isoladamente: ela precisa ser comparada com a espessura mínima estrutural acrescida da sobreespessura para corrosão, porque a redução de seção afeta a capacidade resistente da chapa. Ao mesmo tempo, o revestimento em condição ruim remove uma barreira anticorrosiva e está associado ao aumento da corrosão e à própria redução de espessura. Se a proteção catódica também está duvidosa, a combinação de queda de potencial e desgaste dos ânodos indica perda de desempenho por despolarização, situação que requer ação corretiva. Portanto, não é caso de simples acompanhamento local: a reavaliação deve integrar espessura remanescente, condição do revestimento e funcionalidade da proteção catódica, incluindo verificação por potencial, corrente e condição física dos ânodos, para decidir reparo, restauração das barreiras e prioridade de inspeção.

### Instrumentação, Controle e Automação

**facil · REPROVADA: suporte · corrigida**  
_Nota(s): Integridade metrológica e manutenção de instrumentos por condição_

**P:** Por que a calibração periódica manual pode reduzir a disponibilidade do processo e nem sempre ser a melhor estratégia de manutenção de instrumentos?

**R:** Porque a calibração periódica manual frequentemente exige retirar o instrumento de operação e, em muitos casos, parar o processo, o que reduz a disponibilidade. Além disso, estudos indicaram que menos de 5% das calibrações manuais realizadas eram realmente necessárias, mostrando que a rotina por periodicidade fixa pode gerar muitas intervenções sem necessidade. Há também o risco de a própria intervenção manual afetar negativamente a confiabilidade do instrumento. Assim, ela nem sempre é a melhor estratégia, especialmente quando provoca paradas ou retiradas de serviço sem benefício proporcional.

**media · APROVADA · corrigida**  
_Nota(s): Integridade metrológica e manutenção de instrumentos por condição_

**P:** Em um transmissor, a alteração observada aparece em medições feitas em curto intervalo de tempo sob as mesmas condições. Em outro, a mudança é lenta e se acumula ao longo de um período mais longo. Como esses dois comportamentos devem ser classificados do ponto de vista metrológico?

**R:** O comportamento observado em curto intervalo de tempo sob as mesmas condições deve ser analisado como repetibilidade, porque a repetibilidade corresponde à estabilidade em curto prazo. Já a mudança lenta que se acumula ao longo de um período mais longo deve ser classificada como deriva, pois a deriva é a variação lenta das características metrológicas e integra a estabilidade de longo prazo. Assim, a distinção técnica é feita pelo horizonte temporal do comportamento observado: curto prazo remete à repetibilidade; longo prazo com variação lenta remete à deriva.

**dificil_A · APROVADA · corrigida**  
_Nota(s): Integração de sinais de campo para redes digitais e supervisão Web_

**P:** Em uma unidade offshore, a integração adotada usa um conversor de corrente para levar sinais 4–20 mA/HART à rede FOUNDATION Fieldbus e, depois, mapeia as variáveis com endereçamento padronizado em servidor OPC-DA, usado por uma aplicação cliente Web. Um transmissor de nível com HART sobre 4–20 mA foi ligado ao sistema, e uma variável de pressão que já estava na automação deixou de aparecer na supervisão Web após alteração de configuração. Por que a integração precisa ser tratada em duas camadas e que verificação técnica cabe em cada uma?

**R:** A integração é tratada em duas camadas porque cada uma resolve uma etapa diferente da disponibilização fim a fim. A primeira camada é a compatibilização do sinal de campo com a rede de automação: no arranjo dado, um instrumento com saída 4–20 mA, 0–20 mA ou HART sobre 4–20 mA precisa de conversão para FOUNDATION Fieldbus. Sem isso, a variável não chega ao sistema de automação. A segunda camada é a disponibilização supervisória: depois de chegar à automação, a variável precisa ser mapeada, receber endereçamento padronizado e ser armazenada no servidor OPC-DA, porque a aplicação cliente Web usa essa base para publicá-la. Assim, para o transmissor de nível, deve-se verificar a conversão para FOUNDATION Fieldbus; para a pressão que sumiu da Web, deve-se verificar mapeamento, endereçamento e armazenamento no OPC-DA.

**dificil_B · APROVADA · corrigida**  
_Nota(s): Medição de nível por radar de onda guiada e medição de interface por densidade com medidores nucleônicos; Desempenho metrológico e resposta dinâmica de instrumentos de processo; Seleção e aplicação de instrumentação e elementos finais de controle no processo_

**P:** Em um separador trifásico de FPSO, a malha perde qualidade quando as condições do conteúdo mudam. A equipe quer usar a mesma medição para controle contínuo e também para proteção por interface crítica. Qual escolha de medição e de atuação é mais coerente para a interface próxima à saída de água, e por que essa decisão deve considerar também a dinâmica e as condições de instalação da medição?

**R:** A escolha mais coerente é usar, para a interface próxima à saída de água, a medição nucleônica por densidade, porque esse sinal pode alimentar o controlador de nível e também acionar desarme quando a interface de água fica extremamente baixa. Já o radar de onda guiada determina nível pelo tempo de reflexão na sonda, e a qualidade desse eco depende da constante dielétrica do processo. Além do princípio físico, a medição só será adequada ao controle se seu tempo de resposta e sua resposta em frequência forem compatíveis com a dinâmica da variável, e se a instalação não introduzir influência externa relevante. Na atuação, deve-se evitar elemento final em modo liga-desliga, pois ele não é ideal para controle proporcional.

### Manutenção e Plano de Manutenção

**facil · REPROVADA: suporte · corrigida**  
_Nota(s): FMEA/FMECA como base para definir estratégia e plano de manutenção de ativos críticos_

**P:** Em equipamentos críticos, o que a FMEA/FMECA procura identificar e por que a análise avança da função e da falha funcional até os modos, efeitos e consequências da falha?

**R:** Em equipamentos críticos, a FMEA/FMECA é usada para identificar modos de falha e de deterioração. A análise parte da função e do padrão de desempenho esperado, passa pelas falhas funcionais, detalha os modos de falha e suas causas, lista os efeitos e analisa as consequências. Esse encadeamento mostra como a perda de função ocorre e qual impacto ela produz no contexto operacional. Ao detalhar a causa de cada modo de falha, evita-se tratar apenas sintomas. Ao avançar até efeitos e consequências, a análise fornece base técnica para decisões de manutenção coerentes com a função do equipamento e com as consequências da falha.

**media · APROVADA**  
_Nota(s): FMEA/FMECA como base para definir estratégia e plano de manutenção de ativos críticos_

**P:** Após o encerramento técnico de várias ordens de serviço, a engenharia consolida indicadores e histórico do sistema de gestão da manutenção e observa recorrência de intervenções em certos ativos. Como esse histórico deve ser usado para ajustar o plano de manutenção?

**R:** Esse histórico deve ser analisado para transformar os dados do sistema em recomendações formais à gestão de manutenção. A partir dos indicadores e registros consolidados, a engenharia pode propor melhoria de planos de manutenção existentes, criação de novos planos de manutenção e inclusão de itens em estoque. Quando disponível, resultados de estudos e análises de FMEA também servem de base para essas recomendações. Assim, o histórico não fica restrito ao registro das intervenções executadas; ele alimenta a revisão estruturada do plano e dos sobressalentes conforme a evidência extraída do sistema.

**dificil_A · APROVADA · corrigida**  
_Nota(s): Verificação operacional de barreiras e retorno seguro após manutenção_

**P:** Após manutenção em um sistema de armazenamento, o supervisório indica barreiras aparentemente disponíveis e operação normal. Na inspeção de campo, a equipe encontra uma válvula crítica fora da posição normal, um ponto de sangria sem tampa e incerteza se o arranjo dos tanques corresponde à condição de projeto. Nessa situação, o retorno ao serviço pode ocorrer com contingências temporárias ou a operação deve ser restringida? Justifique com base na verificação das barreiras e no risco residual.

**R:** A decisão não é automática. Primeiro, é necessário confirmar a disponibilidade aparente das barreiras por verificação física e/ou no supervisório e, no sistema de armazenamento, comparar a condição operacional com a condição de projeto. Como há indícios de desalinhamento pós-manutenção, aplicam-se as checagens visuais do retorno ao serviço como critério técnico: conferir recolocação conforme o projeto, retorno de válvulas críticas, condição de vents/drains, tampas em pontos de sangria e alinhamento de dispositivos protetivos. Se, após essa verificação, as contingências propostas forem suficientes para manter o risco em nível aceitável, a continuidade pode ser considerada. Se não forem suficientes, a medida correta é restringir a operação, podendo chegar à parada do equipamento, do sistema ou da planta.

**dificil_B · APROVADA**  
_Nota(s): Dimensionamento e priorização de sobressalentes críticos por risco, falha e lead time; Integração do plano de manutenção com materiais, suprimentos, custos e conformidade em CMMS/SAP PM; Planejamento de manutenção e provisão de recursos para reduzir indisponibilidades_

**P:** Em um FPSO, a troca física de um componente ligado à continuidade operacional é simples, mas a parada total se alonga repetidamente porque a peça não está disponível, a compra só começa após a falha e surgem fretes urgentes e dúvidas de especificação. A unidade também observa que itens relevantes para barreiras e produção entram em aquisição emergencial com frequência. Qual diagnóstico estrutural é mais consistente e qual prioridade de gestão reduz melhor a indisponibilidade futura?

**R:** O problema principal é de prontidão logística e de integração do planejamento, não de execução de campo. A indisponibilidade total após a falha depende também da disponibilidade de sobressalentes e da prontidão da resposta, além da complexidade do reparo; por isso, uma troca simples pode gerar parada longa quando material e compra não foram preparados antes da falha. A correção prioritária é tratar sobressalentes críticos dentro da estratégia de confiabilidade, dimensionando-os por risco do cenário, taxa de falha, quantidade instalada e lead time, em vez de reagir ao consumo. Em paralelo, o plano de manutenção no CMMS/SAP PM deve nascer vinculado à verificação de material, reserva de estoque ou ressuprimento/compra antecipada e acompanhamento da aquisição. A recorrência de compras reativas indica processo de manutenção e materiais mal estruturado, com risco adicional de erro de especificação, falha de qualidade e não conformidade.

## Segurança Ocupacional, Saúde e Meio Ambiente

### Condições Ambientais e Impactos Operacionais

**facil · APROVADA**  
_Nota(s): Falha de risers: escalonamento do dano, perda de contenção e avaliação de consequências ambientais_

**P:** Por que a falha de um riser caracteriza uma perda de contenção com potencial de liberação de hidrocarbonetos ao ambiente marinho?

**R:** Porque o riser transporta hidrocarbonetos e, quando falha, perde a capacidade de manter esse inventário confinado, permitindo a descarga do produto no mar. Esse potencial de liberação é especialmente relevante quando o escoamento inclui, além do petróleo, gases residuais e compostos corrosivos associados ao fluido produzido, pois a falha passa a ter consequência direta de contaminação ambiental pela saída do conteúdo transportado para o ambiente marinho.

**media · APROVADA**  
_Nota(s): Falha de risers: escalonamento do dano, perda de contenção e avaliação de consequências ambientais_

**P:** Em uma ruptura total de riser flexível no trecho submerso, como o evento pode evoluir de dano localizado para um cenário de maior severidade operacional e ambiental?

**R:** A ruptura pode deixar de ser um dano restrito ao próprio riser quando o evento passa a ameaçar estruturas e risers adjacentes, provocando novos rompimentos e ampliando a liberação de óleo para o mar. Nessa condição, a severidade aumenta porque o acidente combina perda de contenção inicial, propagação do dano físico na instalação e maior volume potencial de hidrocarbonetos no ambiente. O impacto também deixa de ser apenas local quando a pluma pode se dispersar para áreas ambientalmente sensíveis, como praias e manguezais, exigindo avaliar ao mesmo tempo o escalonamento mecânico da falha e a dispersão do poluente.

**dificil_A · REPROVADA: suporte**  
_Nota(s): Temperatura ambiente na adequação de sistemas de monitoramento de gases_

**P:** Em um compartimento interno de uma unidade offshore, um detector de gás será instalado próximo à exaustão. A carga do processo varia ao longo do dia, alterando o aquecimento local, e a equipe quer validar se um instrumento selecionado pela condição climática externa continua adequado. Como deve ser feita essa avaliação de adequação, considerando temperatura local, composição do fundo gasoso, ventilação e regime de exposição do sensor?

**R:** A adequação não deve ser julgada pela temperatura externa, mas pela condição real do ponto monitorado, por ser um ambiente interno e influenciado pela exaustão. A avaliação deve considerar o processo monitorado e o regime operacional efetivo, incluindo variações térmicas ao longo do dia e entre condições sazonais, porque essas mudanças podem deslocar a faixa de valores observada e afetar o fundo de escala requerido. Portanto, o critério correto é verificar se o sistema permanece compatível com as condições locais mais severas e fora do regime normal, no ponto onde o sensor ficará exposto. Como a atmosfera real do local é a referência de projeto, a composição do fundo gasoso e a ventilação do ponto não podem ser tratadas por aproximação climática geral; elas precisam ser caracterizadas no próprio ambiente de instalação antes de confirmar a adequação do sistema.

**dificil_B · APROVADA**  
_Nota(s): Dispersão ambiental, monitoramento e modelagem de consequências em FPSOs: efeito de vento, geometria, temperatura e composição do meio; Temperatura ambiente na adequação de sistemas de monitoramento de gases; Detecção, lógica de automação e shutdown sob interferência, fogo, fumaça e necessidade de resposta de emergência_

**P:** Em um módulo de processo de FPSO, alarmes intermitentes de gás surgem principalmente durante mudanças de regime e aumento de temperatura local. As rondas não confirmam atmosfera perigosa persistente, mas há obstáculos e zonas pouco ventiladas; a equipe começa a tratar os alarmes como espúrios. Qual diagnóstico técnico integrado deve orientar a decisão operacional sobre esses alarmes?

**R:** A interpretação mais robusta é que os alarmes não devem ser classificados de imediato nem como pseudoalarmes puros nem como vazamento confirmado uniforme. Eles podem resultar de acúmulo real e transitório da pluma em zonas de recirculação criadas por geometria e vento, onde concentração local depende de mistura turbulenta e transporte vertical, ou de inadequação do monitoramento sob a temperatura efetiva, umidade e composição gasosa reais do ponto medido, incluindo interferência por gases espúrios. Como essas causas produzem aparência semelhante de perda de prontidão, a decisão correta é manter a credibilidade da barreira e separar as hipóteses verificando conjuntamente dispersão local, temperatura/composição do ambiente monitorado e regime de exposição do sensor. Também é necessário revisar a configuração de alarmes e a resposta automática associada, porque pseudoalarmes e atrasos na atuação de ventilação/shutdown podem aumentar o tempo de resposta e favorecer propagação para áreas ocupadas.

### Gestão de Pessoas e Treinamento

**facil · REPROVADA: suporte**  
_Nota(s): Governança do programa de treinamento como base para avaliar eficácia, retenção e conformidade_

**P:** Qual é a diferença entre uma matriz de treinamentos mandatórios gerais e uma matriz de treinamentos em procedimentos operacionais por função, e o que cada uma comprova ou não comprova?

**R:** A matriz de treinamentos mandatórios gerais comprova a cobertura de cursos obrigatórios formais e documentados aplicáveis à força de trabalho, com evidência rastreável do que foi realizado. Isso ajuda a demonstrar atendimento a exigências gerais de treinamento, mas não comprova, por si só, que cada trabalhador foi treinado nos procedimentos operacionais específicos da atividade que executa. Já a matriz de treinamentos em procedimentos operacionais por função relaciona as necessidades de capacitação ao cargo e à execução real das tarefas, permitindo demonstrar treinamento adequado ao exercício da função. Sem essa matriz específica e sem registros correspondentes, a organização não consegue provar competência operacional por função nem distinguir adequadamente lacunas entre ocupantes do mesmo cargo.

**media · REPROVADA: suporte, codigo:depende_do_material · corrigida**  
_Nota(s): Governança do programa de treinamento como base para avaliar eficácia, retenção e conformidade_

**P:** Em uma unidade offshore, a matriz de treinamento existe, mas está desatualizada e não reflete o status real das competências da equipe. Como isso compromete a verificação das competências, a designação de pessoas para funções e a demonstração de conformidade do treinamento?

**R:** Nas fontes citadas, a matriz atualizada é o meio de refletir o status real das competências e sustentar a verificação de que os requisitos de cada função continuam atendidos. Se ela estiver desatualizada, a organização perde uma referência confiável para confirmar quem mantém as competências requeridas no momento de designar pessoas para determinadas funções. Além disso, fica prejudicada a demonstração de que a força de trabalho recebeu treinamento adequado ao exercício de suas atividades e de que existe verificação periódica desse atendimento. Em termos de conformidade, a matriz deixa de funcionar como evidência rastreável do quadro real de competências, reduzindo a capacidade de comprovar cobertura e aderência do treinamento às funções exercidas.

**dificil_A · REPROVADA: correcao_tecnica, suporte · corrigida**  
_Nota(s): Gestão de competências, critérios por função e treinamento em instalações offshore_

**P:** Em um FPSO, um mesmo cargo acumula operação de utilidades e apoio ao tratamento de gás. As descrições de função são genéricas, os registros de treinamento estão válidos, não há evidência de redução de efetivo, parte da equipe usa procedimentos desatualizados e a empresa não adota critérios formais para designar supervisores de turno com responsabilidade de liderança. Nesse quadro, qual causa predominante deve ser diagnosticada: definição insuficiente do padrão da função, qualificação inadequada para o papel, suficiência de recursos ou avaliação de competência?

**R:** A causa predominante é a qualificação inadequada para o papel, especialmente no exercício da supervisão com liderança. O indício mais direto é a ausência de critérios formais para designar supervisores, sintoma explicitamente associado a fragilidade na seleção/habilitação para esse papel. Os registros de treinamento válidos afastam, em primeiro plano, falha de avaliação da competência, e a ausência de evidência de redução de efetivo afasta insuficiência de recursos. As descrições genéricas e o acúmulo de funções sem tratamento específico por função mostram deficiência de base no sistema, mas, neste caso, o desvio mais imediatamente diagnosticável é que a organização não assegura requisitos claros de formação, experiência, habilidade e conhecimentos para a função de supervisão. O uso de procedimentos desatualizados agrava o quadro, sem mudar essa predominância.

**dificil_B · REPROVADA: suporte, jurisdicao · corrigida**  
_Nota(s): Avaliação de competência e assurance baseados em evidências; Métodos de avaliação e fechamento de lacunas de competência; Critérios objetivos para demonstrar eficácia de treinamento e retenção de competência_

**P:** Em um FPSO, equipe própria e contratada está com certificados e reciclagens em dia, e a maioria foi aprovada em avaliações gerais. Mesmo assim, exercícios de mesa, observações de campo e tarefas pouco frequentes revelam erros repetidos em partes específicas de procedimentos críticos. Que revisão do sistema de treinamento e avaliação melhor demonstra a eficácia real do treinamento e evita liberar pessoal apenas com base em evidências documentais ou resultados agregados?

**R:** A revisão deve usar assurance por função, com padrões objetivos e evidências múltiplas proporcionais à criticidade. Certificados, reciclagem concluída e resultados agregados não bastam para demonstrar competência mantida. Para procedimentos críticos, a avaliação deve combinar testes de conhecimento, observação prática e cenários/exercícios de mesa, registrando evidências. Como os erros aparecem em partes específicas, a lacuna deve ser identificada por área ou seção, e não só por resultado geral; depois disso, aplica-se treinamento adicional direcionado e reavaliação restrita ao trecho deficiente. Em tarefas pouco frequentes, a reciclagem deve ser mais frequente ou pré-tarefa. Para contratados, a avaliação deve ocorrer antes da contratação, no início do contrato e durante a operação. O sistema também deve monitorar desempenho e reavaliar áreas-chave continuamente para sustentar a liberação para a função.

### Meio Ambiente, Gestão Ambiental e Sustentabilidade

**facil · APROVADA · corrigida**  
_Nota(s): Gestão ambiental operacional e prontidão para prevenção e resposta a impactos marinhos_

**P:** Qual é a função de sistemas rigorosos de gestão de saúde, segurança, social e ambiental na operação offshore com potencial de impacto ao ambiente marinho?

**R:** Esses sistemas fornecem capacidade para avaliar e minimizar os riscos das operações offshore. Também permitem desenvolver processos voltados à redução dos impactos negativos ao meio ambiente marinho. Assim, sua função é apoiar a gestão dos riscos operacionais e a redução dos impactos ambientais associados à atividade offshore.

**media · REPROVADA: suporte · corrigida**  
_Nota(s): Gestão ambiental operacional e prontidão para prevenção e resposta a impactos marinhos_

**P:** Em uma emergência ambiental offshore, a unidade tem procedimento documentado e registros de manutenção atualizados, mas um equipamento de controle da poluição está indisponível. Por que essa documentação, isoladamente, não comprova capacidade real de resposta?

**R:** Porque, em situação emergencial, a tomada de decisão deve avaliar não apenas a eficácia de normas, procedimentos documentados e registros de operação e manutenção, mas também as condições reais de operação e manutenção das unidades e equipamentos de controle da poluição, de prevenção de acidentes e relacionados aos aspectos ambientais. Se um equipamento de controle da poluição está indisponível, a resposta fica limitada pela condição operacional existente. Assim, a existência de procedimento e de registros atualizados, por si só, não demonstra capacidade efetiva de resposta, pois a decisão deve considerar também a disponibilidade real dos equipamentos que precisam atuar no evento.

**dificil_A · REPROVADA: suporte, codigo:referencia_alternativas · corrigida**  
_Nota(s): Integração do SGA/SMS à governança de projetos de E&P/FPSO no ciclo de vida de projeto_

**P:** Em um projeto de FPSO, duas alternativas de sistema têm desempenho econômico inicial semelhante. A alternativa X usa mais material e energia na implantação, mas atende à função requerida. A alternativa Y reduz o consumo de recursos, adota processo e fonte energética de menor impacto e apresenta menor exposição futura a emissões e a preços de carbono. Qual alternativa deve ser priorizada e por quê?

**R:** A alternativa Y deve ser priorizada. Pela abordagem de ciclo de vida apoiada pela LCD, um resultado bom de projeto não se limita a atender à função: ele também envolve minimizar o uso de recursos e escolher processos e fontes energéticas de menor impacto ambiental. Além disso, as diretrizes e os processos corporativos de decisão devem considerar o risco de carbono, incluindo emissões, preços de carbono e mudanças climáticas. Assim, entre alternativas com desempenho econômico inicial semelhante, a opção que reduz consumo de recursos, adota processos e energia de menor impacto e tem menor exposição ao risco de carbono é a mais consistente com esses critérios de projeto.

**dificil_B · APROVADA · corrigida**  
_Nota(s): Conformidade legal, licenciamento ambiental e tratamento de não conformidades em FPSO/FSO; Monitoramento ambiental de emissões atmosféricas, efluentes e indicadores de sustentabilidade; Indicadores de água produzida e efluentes oleosos: monitoramento em linha, seleção de medidores, validação do tratamento e reuso_

**P:** Em uma auditoria interna de um FPSO, a operação sustenta que o descarte de água produzida está sob controle porque o TOG em linha permanece estável e é usado para ajustar o tratamento. Porém, a revisão do licenciamento e dos relatórios enviados ao órgão ambiental indica possível desalinhamento entre a condicionante de descarte e o parâmetro ou método analítico informado. Qual é o diagnóstico técnico mais provável e qual deve ser a prioridade de ação?

**R:** O diagnóstico mais provável é de falsa conformidade. O TOG em linha é útil para controle operacional e acompanhamento da água descartada, mas não comprova sozinho o atendimento da condicionante ambiental se o parâmetro ou o método exigido no licenciamento for diferente. No Brasil, para descarte de água produzida ao meio ambiente, o material cita óleo e graxas por método gravimétrico; em outras condições, como águas internacionais ou certos sistemas conectados ao riser, o critério citado é TOG. A prioridade é tratar o caso como não conformidade de gestão e evidência regulatória: verificar os requisitos e restrições aplicáveis do licenciamento, confirmar a coerência entre jurisdição, parâmetro e método usado nos relatórios, e abrir plano de ação com responsáveis e prazos compatíveis com o risco. O TOG em linha deve permanecer como apoio operacional.

### Saúde Ocupacional

**facil · REPROVADA: suporte**  
_Nota(s): Vigilância médica ocupacional em cenários de surtos e pandemias offshore_

**P:** Qual é a função de um programa de vigilância médica ocupacional em ambiente offshore além do acompanhamento clínico individual?

**R:** É transformar sinais de adoecimento em controle efetivo do risco para as pessoas e para a operação. Isso exige que preocupações com doença sejam reportadas e investigadas, com definição de ação corretiva para prevenir recorrência, em vez de apenas registrar casos. Em surtos ou pandemias, o programa também precisa sustentar decisões operacionais com base em informações como POB (pessoas a bordo), casos suspeitos, contactantes e óbitos, além de prever medidas para a ausência de profissionais-chave. Por isso, a vigilância médica offshore conecta monitoramento de saúde, gestão de casos, medidas de contenção e continuidade operacional segura, especialmente quando a indisponibilidade de lideranças, equipe médica ou técnicos de segurança pode degradar a capacidade de resposta da instalação.

**media · REPROVADA: suporte · corrigida**  
_Nota(s): Vigilância médica ocupacional em cenários de surtos e pandemias offshore_

**P:** Em uma unidade offshore, foi reportado um trabalhador com suspeita de doença infecciosa. Qual é o encadeamento de gestão que a vigilância médica deve seguir para transformar esse registro em controle efetivo do risco à saúde?

**R:** O encadeamento começa com o reporte do agravo ou suspeita e a investigação efetiva do caso. A partir dessa apuração, devem ser definidas ações corretivas para prevenir recorrência. No contexto de doença infecciosa, orientações de referência para instalações offshore incluem medidas de manejo como monitoramento de saúde, isolamento, restrição de circulação de pessoas doentes ou potencialmente infectadas, comunicação clara, sanitização e protocolo de retorno ao trabalho. Depois, as ações decorrentes da avaliação de risco à saúde e do plano de melhoria precisam ser rastreadas e executadas com registros de gestão. Por fim, a organização deve verificar periodicamente a eficácia das medidas implantadas e avaliar se são necessários controles adicionais. Sem essa sequência, há registro do caso, mas não evidência de controle efetivo.

**dificil_A · APROVADA**  
_Nota(s): Gestão de casos de doença, restrições e retorno seguro ao trabalho offshore_

**P:** Em uma unidade offshore, dois trabalhadores foram afastados no mesmo turno. Um apresentou febre e tosse após conviver com a equipe em área comum; o outro foi retirado da atividade porque a tarefa estava sendo executada em condição operacional insegura e em ambiente fora do padrão operacional. Se a equipe de gestão precisar definir a prioridade técnica de tratamento de cada afastamento, qual deve ser o foco principal em cada caso?

**R:** No caso com febre e tosse, a prioridade deve recair no controle do caso infeccioso. Isso exige tratar o evento como processo operacional controlado, com monitoramento de saúde, isolamento, impedimento de circulação do trabalhador suspeito ou potencialmente infectado, comunicação clara ao pessoal, sanitização, manejo do caso e retorno ao trabalho. Já no afastamento ligado à condição operacional insegura e ao ambiente em desconformidade, a prioridade é corrigir a condição operacional que sustenta o afastamento, porque esse tipo de ocorrência aparece como consequência de falhas do contexto operacional. Tratar ambos os afastamentos da mesma forma reduz a efetividade da resposta: no primeiro, o risco central é propagação e convivência a bordo; no segundo, o problema central é a condição de operação e de conformidade do ambiente de trabalho.

**dificil_B · REPROVADA: correcao_tecnica, suporte, jurisdicao, sem_generalizacao**  
_Nota(s): Água potável offshore em FPSO/FSO: disponibilidade, controle sanitário e contingência operacional; Prevenção de surtos a bordo por controle de agentes biológicos, água potável, alimentos e interfaces de abastecimento; Planejamento para surtos e contingências sanitárias coletivas em instalações offshore_

**P:** Após bunkering recente de água, 12% do efetivo de um FPSO apresenta sintomas gastrointestinais em poucas horas. Os casos estão em setores diferentes; parte não consumiu a mesma refeição, mas todos usaram água das áreas de vivência. No mesmo período houve falha temporária de refrigeração na cozinha. Qual trilha de investigação e contenção deve ser priorizada para decidir a resposta inicial sem perder a segurança operacional?

**R:** Trate o evento como emergência sanitária coletiva por fonte comum potencial. Como os casos não se concentram em uma única refeição e todos compartilharam a água de vivência, a água potável deve entrar como hipótese prioritária, sem descartar alimento: verifique imediatamente a integridade do abastecimento recente, incluindo higiene sanitária de mangueiras e conexões de bunkering, além de acionar a contingência para suspeita de falta ou contaminação da água. Em paralelo, acione a contingência de falha de refrigeração e de surto transmitido por alimentos, porque a conservação inadequada também pode ter sido vetor. A resposta inicial deve combinar contenção clínica e epidemiológica com isolamento dos casos, rastreamento de contatos, tratamento sintomático e, se necessário, evacuação. Como 12% do efetivo foi atingido, reavalie a normalidade operacional e o efetivo mínimo para operar com segurança, além de comunicar o evento conforme o gatilho aplicável no Brasil.

### Segurança Ocupacional

**facil · APROVADA**  
_Nota(s): Trabalhos a quente: fontes de dano, avaliação prévia da área e proteção do trabalhador_

**P:** Quais são os principais perigos que devem ser considerados em solda, corte e outros trabalhos a quente em ambiente industrial ou offshore?

**R:** Os principais perigos incluem queimaduras por exposição térmica direta, ignição quando há vapores inflamáveis na área, inalação de gases, fumos e vapores, choque elétrico, luminosidade excessiva do arco de solda e projeção de fagulhas ou partículas/projéteis oriundos do corte. Em alguns contextos, também pode haver risco de explosão de cilindros de oxigênio. Esses mecanismos podem ocorrer simultaneamente, por isso a atividade não deve ser tratada como risco único.

**media · APROVADA**  
_Nota(s): Trabalhos a quente: fontes de dano, avaliação prévia da área e proteção do trabalhador_

**P:** Em um serviço de solda executado em plataforma, com possibilidade de flash fire, exposição ao arco elétrico e trabalho em desnível, como cada EPI deve ser relacionado ao mecanismo de dano que controla?

**R:** A roupa resistente ao fogo é indicada para reduzir a severidade do dano térmico e os efeitos de um possível flash fire. O capacete de soldagem com tonalidade adequada serve para atenuar a luminosidade excessiva associada à solda elétrica. A proteção contra quedas controla o risco adicional de trabalho em desnível, especialmente se um evento térmico súbito provocar reação intempestiva ou perda de equilíbrio. A escolha do EPI, portanto, deve cobrir simultaneamente risco térmico, ocular e de queda.

**dificil_A · APROVADA**  
_Nota(s): Diálogos de segurança e governança do PTW/CoW_

**P:** Durante uma intervenção sob PTW em área operacional, a equipe de campo identifica que uma etapa não prevista será necessária para concluir o serviço. Há trabalhadores no local que não constam no permit, a mudança não passou por análise prévia de perigos, a interface com outros trabalhos não foi comunicada e o responsável que está conduzindo a liberação não tem competência formal claramente demonstrada para a função. Nessa condição, qual deve ser a decisão correta sobre a continuidade do trabalho e por quê?

**R:** A decisão correta é interromper ou recusar o trabalho até restabelecer a aderência entre campo e permit. O motivo é que houve mudança de condição e de escopo sem nova verificação da adequação do PTW, o que pode tornar inválidos os perigos e controles originalmente registrados. A presença de pessoas não listadas no permit e a falta de comunicação sobre interfaces indicam perda de coordenação do CoW, especialmente porque mudanças e interações com outros trabalhos precisam ser verificadas no local com os documentos associados. Além disso, a ausência de análise prévia para os novos perigos e a competência não demonstrada de quem conduz a liberação fragilizam a governança e a clareza de responsabilidades. Nessas condições, o permit deixa de ser controle confiável; o trabalho só pode prosseguir após reavaliação, discussão em campo com a equipe, confirmação dos controles e atuação por responsável formalmente competente. Se a condição insegura persistir, cabe recusa justificada.

**dificil_B · REPROVADA: suporte, jurisdicao · corrigida**  
_Nota(s): Condição operacional do guindaste e controles prévios ao uso em içamento offshore; Prevenção de contato, enroscamento e queda de objetos na movimentação de cargas; Protocolos de comunicação e coordenação em tarefas críticas de movimentação e içamento_

**P:** Em um içamento em área congestionada do convés, a carga passa por um trecho de folga reduzida e, durante o giro do turntable, começa a se aproximar de uma estrutura lateral. O operador percebe resposta diferente da esperada, enquanto a equipe de campo diverge por rádio sobre o próximo movimento e sobre a necessidade de reposicionar observadores. Nesse cenário, qual diagnóstico integrado é mais adequado e quais controles devem ser priorizados para recuperar a previsibilidade da manobra?

**R:** O diagnóstico mais adequado integra três frentes. Primeiro, o comportamento da carga pode ter mudado com o giro do turntable, porque isso pode deslocar o centro de gravidade e alterar as condições de operação. Segundo, a trajetória em folga reduzida exige revisar o movimento passo a passo para localizar pontos potenciais de contato ou enroscamento e, se houver esses pontos, posicionar spotters adicionais. Terceiro, a divergência por rádio indica necessidade de restabelecer papéis, comunicações claras e verificação incremental do deslocamento da carga, especialmente se houver visibilidade limitada. Como controle prioritário, a equipe deve manter pessoas fora da line of fire, confirmar zonas de risco e usar comunicações inequívocas com identificação no rádio. A condição operacional documentada do guindaste também deve ser confirmada por inspeção pré-uso e certificação/documentação aplicável.
