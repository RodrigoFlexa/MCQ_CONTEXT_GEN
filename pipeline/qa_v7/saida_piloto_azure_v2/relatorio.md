# Piloto QA v7: perguntas a partir do inventário

Gerador gpt-5-4-petrobras:low, juiz gpt-5-4-petrobras:medium. 160 questões geradas, 132 aprovadas (82%). Tempo 9.5 min. Chamadas 249, tokens de entrada 1,160,456, de saída 359,679.

O nível é o tipo pedido ao gerador (sem avaliador de dificuldade no loop).

| Tipo | geradas | aprovadas | corrigidas |
|---|---:|---:|---:|
| facil | 40 | 33 | 2 |
| media | 40 | 36 | 1 |
| dificil_A | 40 | 32 | 0 |
| dificil_B | 40 | 31 | 2 |

Motivos de reprovação: suporte (23), correcao_tecnica (8), sem_generalizacao (5), escopo (3), autonomia (2), tipo_ok (1)
Lotes com falha ou filtro de conteúdo: 0

## Sistemas de Lastro, Estabilidade, Ancoragem e Posicionamento, Offloading e Tanques de Carga

### Operação de Offloading

**facil · REPROVADA: autonomia · corrigida**  
_Nota(s): Falhas de propulsão, energia, controle e apoio que degradam a manobrabilidade do aliviador no offloading_

**P:** Na operação de offloading, a que efeitos operacionais se associam a perda de propulsão do aliviador, a parada do sistema diesel-gerador e um evento de drive-off em embarcação com posicionamento dinâmico?

**R:** Perda de propulsão e parada do sistema diesel-gerador se associam a atraso operacional e à possibilidade de colisão se a operação prosseguir ou o problema persistir. Em evento de drive-off com posicionamento dinâmico, o cenário relevante também é colisão; nessa condição, a pequena distância entre as embarcações limita a velocidade de impacto a até 2 nós.

**media · APROVADA**  
_Nota(s): Falhas de propulsão, energia, controle e apoio que degradam a manobrabilidade do aliviador no offloading_

**P:** Durante o offloading, a equipe enfrenta quatro ocorrências distintas: falha de equipamento genérica; falha no cilindro com sistema de posicionamento dinâmico disponível; problema de thruster; e problema de satélite GPS. Qual deve ser a resposta operacional em cada caso?

**R:** Na falha de equipamento, deve-se desconectar, desamarrar e afastar o aliviador da unidade de produção, com ativação da parada de emergência da transferência; isso aborta a operação. Na falha no cilindro, a desconexão, a desamarração e o afastamento devem ser executados usando o sistema de posicionamento dinâmico. Em problema de thruster, a operação deve ser abortada. Em problema de satélite GPS, a ação indicada é verificar os avisos aos navegantes sobre informações de satélites.

**dificil_A · APROVADA**  
_Nota(s): Perda de posição do navio aliviador e mecanismos de colisão no offloading com FPSO_

**P:** Durante o bombeamento, o navio aliviador começa a sair do envelope seguro. Em um evento, a excursão vem acompanhada de perda de alimentação elétrica para vários sistemas, seguida de parada do motor principal e indisponibilidade de navegação e manobra. Em outro, os sistemas permanecem energizados, mas há perda de propulsão; em um terceiro, a resposta do navio fica inadequada embora energia e propulsão estejam disponíveis. Qual diagnóstico é mais compatível com cada quadro e qual deles tende a evoluir primeiro como atraso operacional antes de aumentar o risco de colisão?

**R:** O primeiro quadro é compatível com blackout em cascata iniciado por falha no motor de combustão auxiliar: a perda elétrica afeta vários sistemas, alcança as bombas de óleo lubrificante do motor principal e leva à parada do motor principal, da navegação e da manobra. O segundo quadro indica perda isolada de propulsão; nessa condição, a consequência inicial tende a ser atraso operacional, passando a elevar o risco de colisão se persistir. O terceiro quadro é mais compatível com erro de programação do sistema automático ou erro de julgamento das condições de manobrabilidade, porque a resposta do navio se torna inadequada mesmo com sistemas energizados. Em qualquer dos três, permanecer fora da posição segura durante o bombeamento não é aceitável, porque o desvio compromete a transferência e aumenta o risco de colisão.

**dificil_B · REPROVADA: correcao_tecnica, suporte**  
_Nota(s): Teste de estanqueidade, pressurização e partida da transferência no offloading; Ensaios e verificações de integridade aplicáveis ao offloading; Integridade mecânica e contenção na interface de offloading: manifold, conexões, mangotes, QRF e linhas_

**P:** Após a conexão do offloading, a equipe executa a sequência de partida: pressuriza a linha para teste, monitora a pressão e depois circula água antes de enviar óleo. No teste, a pressão não se mantém como esperado. Na circulação de água, aparece contrapressão anormal na máxima vazão. Considerando que os pontos mais críticos de perda de contenção estão na interface mecânica, qual diagnóstico deve ser priorizado e como distinguir vedação deficiente, obstrução e falha localizada na interface?

**R:** Não se deve tratar os sinais como um vazamento simples sem separar os mecanismos. Na partida, o primeiro passo é o teste de estanqueidade com pressurização até valor predefinido e monitoramento por um tempo; se a pressão não se mantém, isso aponta para suspeita de perda de contenção no circuito. Já contrapressão anormal durante circulação de água na máxima vazão indica obstrução parcial, porque esse sinal está ligado à restrição de escoamento, não à vedação. Como a perda de contenção tende a surgir nas descontinuidades da interface, a verificação deve priorizar manifold, conexões, QRF, carretel, terminações e mangote, onde conexão incorreta, ruptura ou posicionamento inadequado podem gerar vazamento. Portanto, a combinação dos dois sinais sugere investigar primeiro a possibilidade de restrição e, em paralelo, confirmar se há perda de contenção nos pontos de interface. Se o teste for encerrado, a despressurização deve ser controlada, sem exceder a taxa especificada.

### Operação de tanques de carga, lastro, sistema gás inerte, ventilação e estabilidade

**facil · APROVADA**  
_Nota(s): Uso do sistema de lastro para controlar calado, trim, banda e flutuabilidade_

**P:** Em operação normal de um FPSO monohull, para que o sistema de lastro é usado quando ocorre carregamento ou descarga de óleo cru?

**R:** Para compensar a variação de calado que ocorre à medida que o óleo cru é carregado ou descarregado.

**media · APROVADA**  
_Nota(s): Uso do sistema de lastro para controlar calado, trim, banda e flutuabilidade_

**P:** Durante uma manobra de lastro, a unidade recupera calado, trim e banda desejados. Esse resultado, por si só, basta para considerar a condição aceitável?

**R:** Não. A condição só é aceitável se, além de corrigir calado, trim e banda para uma condição segura e nivelada, a redistribuição de lastro também mantiver shear forces, bending moments e tensões torsionais dentro dos limites permissíveis.

**dificil_A · APROVADA**  
_Nota(s): Barreiras de contenção e intertravamentos de segurança em carga, offloading e gás inerte_

**P:** Durante uma operação de descarga para navio aliviador, a equipe identifica uma anormalidade no arranjo de offloading com potencial de avaria e poluição, antes de confirmar se houve ruptura de mangueira, dano em tubulação ou desconexão por saída de posição. Qual deve ser a resposta operacional inicial e como ela se relaciona à barreira de contenção do sistema?

**R:** A resposta inicial é interromper imediatamente a transferência, antes de qualquer outra providência. Esse é o passo prioritário quando há defeito ou anormalidade com potencial de risco, avaria ou poluição, porque impede a continuidade da condição insegura. Em seguida, a contenção deve ser preservada com os shut-offs compatíveis com o cenário que venha a se confirmar no offloading, como isolamento da linha, fechamento remoto, parada do bombeio e, quando aplicável, desacoplamento projetado para separação. A lógica técnica é não continuar alimentando um possível vazamento enquanto se verifica se a anormalidade evoluiu para ruptura de mangueira, ruptura de tubulação ou desconexão do navio aliviador. Isso protege a barreira de contenção distribuída nas linhas, válvulas e demais pontos do sistema de carga, blanketing e offloading.

**dificil_B · APROVADA**  
_Nota(s): Reconfiguração de drenos e transferências na indisponibilidade de tanques slop; Inventário de tanques por medição remota e conferência independente para estabilidade; Planejamento e verificação da condição de lastro com documentos de bordo e software de estabilidade_

**P:** Com um tanque slop indisponível, a equipe reconfigurou temporariamente drenos e uma transferência com bomba de stripping por linha segregada. Depois da manobra, os níveis remotos e o programa de estabilidade indicam condição aceitável, mas o trim observado e a resposta de alguns tanques não batem com a sequência prevista. Antes de autorizar nova transferência e ajuste de lastro, qual interpretação deve prevalecer e qual decisão técnica é a mais correta?

**R:** Deve prevalecer a hipótese de que a condição representada no programa pode estar errada, não a confiança automática no line-up presumido ou na telemedição. Em contingência de slop, o destino real das correntes pode mudar com a reconfiguração dos drenos e transferências, inclusive para outro tanque de carga, e o caminho hidráulico aberto pode diferir do esperado operacionalmente. Como o programa usa dados de tanques atualizados automaticamente, ele só é confiável quando o conteúdo dos tanques é confirmado por verificação manual regular. Se a condição observada a bordo diverge do que o programa mostra, a próxima transferência ou manobra de lastro não deve prosseguir até reconciliar o inventário real dos tanques com a condição carregada no software e, se necessário, reavaliar e simular a sequência antes da execução.

### Sistema de ancoragem, manutenção e monitoramento da posição

**facil · REPROVADA: autonomia · corrigida**  
_Nota(s): Gestão das cargas de amarração e resposta à falha de linhas em mau tempo_

**P:** Segundo o procedimento operacional apresentado para falha de uma linha de ancoragem, qual deve ser a resposta imediata e de que depende a retomada das operações?

**R:** As operações devem cessar imediatamente. A retomada depende de qual linha falhou, das condições meteorológicas presentes e futuras e da conformidade com os parâmetros de projeto.

**media · APROVADA**  
_Nota(s): Gestão das cargas de amarração e resposta à falha de linhas em mau tempo_

**P:** Uma unidade entra em tempestade com recurso de ajuste de tensões disponível, mas esse ajuste não é usado. Além disso, os limites máximos operacionais dos guinchos não estão prontamente acessíveis na sala de controle. Como essa combinação pode contribuir para exceder tensões operacionais nas amarras?

**R:** Sem ajustar preventivamente as tensões para a condição severa, a unidade deixa de redistribuir as cargas de amarração conforme o procedimento aplicável a mau tempo. Se, ao mesmo tempo, os limites máximos operacionais dos guinchos não estão prontamente disponíveis na sala de controle, a referência para decidir quanto tensionar ou quando restringir a ação fica retardada. Essa combinação favorece decisão tardia ou inadequada durante a tempestade e aumenta a possibilidade de uma ou mais tensões operacionais serem excedidas.

**dificil_A · APROVADA**  
_Nota(s): Critérios de dimensionamento e verificação de linhas e fundações de ancoragem sob cargas estáticas, dinâmicas e de avaria_

**P:** Uma unidade com ancoragem Taut-Leg apresenta linhas muito inclinadas, e a fundação de uma das amarras passa a receber carregamento combinado, com componentes horizontal e vertical. Na revisão de integridade, também deve ser considerada a hipótese de ruptura de uma linha do sistema. Nesse caso, quais verificações são mandatórias, qual mecanismo resistente tende a governar na fundação e por que a análise por elementos finitos se torna necessária?

**R:** Devem ser verificadas as condições estática e dinâmica, tanto com linhas intactas quanto com uma linha rompida. A fundação também deve ser avaliada quanto à resistência a cargas estáticas, cíclicas e transitórias, sem deformações excessivas nem vibrações, porque esses carregamentos afetam o solo de apoio e a resposta estrutural da estaca. Em arranjo Taut-Leg, a grande inclinação da linha aumenta a componente vertical transmitida à fundação; por isso, a resistência ao arrancamento axial tende a governar. A análise por elementos finitos passa a ser necessária porque a solicitação é combinada, com componentes vertical e horizontal, e a capacidade da estaca não depende apenas da magnitude da carga, mas também da sua direção, que altera o mecanismo de falha mobilizado.

**dificil_B · APROVADA**  
_Nota(s): Monitoramento integrado de posição da unidade, resposta estrutural e integridade de risers/linhas; Impacto do offset e dos movimentos da unidade amarrada na integridade de risers; Station keeping: tendências e indicadores além do offset para detectar degradação antes da perda de posição_

**P:** Um FPSO ancorado permanece dentro do limite usual de offset. Porém, em mar com swell e vento, cresce a variação de aproamento e dos movimentos da unidade, enquanto sensores no topo dos risers indicam aumento de inclinação e deformação, com alarmes por faixa-limite em alguns períodos. A equipe pode considerar a condição aceitável apenas porque o offset global ainda está dentro do envelope? Justifique qual lógica de monitoramento deve prevalecer.

**R:** Não. Offset global aceitável não equivale, por si só, a condição aceitável dos risers. Mesmo dentro do envelope de posição, a combinação entre movimentos da unidade e resposta estrutural local pode elevar tensões, flexões e até compressão dinâmica em parte do ciclo, o que aumenta curvatura e dano por fadiga. Por isso, a decisão deve se basear na integração de três grupos de sinais: condições ambientais em tempo real, tendências de movimentos e aproamento da unidade, e resposta dos risers medida por inclinações, deformações e esforços inferidos. Se variáveis estruturais saem de faixa-limite, o problema já não é descrito adequadamente pelo offset isolado. A lógica correta é tratar o station keeping por limites de alarme e análise de tendências, com histórico e correlação entre ambiente, movimento e resposta do riser, porque a degradação pode aparecer antes de uma excedência clara de offset.

## Operações submarinas, poços, risers e equipamentos submarinos

### Operações submarinas, poços, manifolds, PLEM e PLET

**facil · APROVADA**  
_Nota(s): Monitoramento operacional, envelope de segurança e gestão de integridade em sistemas subsea de poços e linhas associadas_

**P:** Em operação subsea, o que significa manter o sistema dentro do envelope de segurança, e qual tratamento operacional é exigido quando ocorre um desvio desse envelope?

**R:** Significa operar o sistema submarino dentro dos limites definidos em projeto para suas condições aceitáveis de operação. Esses limites são a referência para verificar se o sistema permanece em condição prevista de funcionamento. Quando há desvio, a resposta operacional exigida é registrar e investigar a ocorrência e gerar, implementar e documentar medidas para minimizar a recorrência.

**media · APROVADA**  
_Nota(s): Monitoramento operacional, envelope de segurança e gestão de integridade em sistemas subsea de poços e linhas associadas_

**P:** Um operador de poços já acumulou histórico suficiente para identificar tendências de falhas e percebeu que a proporção entre tarefas preventivas e corretivas ficou muito alta em parte dos equipamentos de barreira. Como uma estratégia de manutenção baseada em risco pode usar essas informações para ajustar as frequências de intervenção?

**R:** A estratégia pode definir e documentar as frequências de manutenção com base em uma avaliação de risco, usando matriz apropriada. Com histórico suficiente para mostrar tendências observáveis, essas frequências podem ser ajustadas. A relação entre tarefas preventivas e corretivas serve como critério de revisão: quando essa razão estiver muito alta ou muito baixa, isso indica necessidade de reavaliar a periodicidade para adequá-la ao comportamento real do sistema.

**dificil_A · APROVADA**  
_Nota(s): Uso de VOR/ROV versus mergulho em inspeção e intervenção de linhas submarinas_

**P:** Em uma linha submarina, a equipe precisa avaliar um trecho externo acessível após suspeita de dano. A água está com visibilidade variável por maré e particulados. Há duas demandas possíveis: apenas verificar a condição aparente do trecho, ou executar uma ação física na linha para corrigir, modificar ou ampliar o sistema. Como o escopo deve ser classificado em cada caso e qual recurso é tecnicamente compatível?

**R:** Se a demanda termina em verificar a condição externa na parte aparente e acessível, o escopo é de inspeção ou vistoria, compatível com mergulho, desde que a visibilidade permita a avaliação; com baixa visibilidade, o alcance da inspeção por mergulho fica ainda mais limitado. Se a demanda inclui atuar fisicamente sobre a linha, como corrigir, modificar, expandir ou reparar, o escopo deixa de ser mera vistoria e passa a ser de intervenção, expansão ou reparo, associado a sistemas operados por VOR/ROV. A distinção técnica é definida pelo objetivo da tarefa: observar o estado visível do equipamento ou executar ação sobre a linha.

**dificil_B · APROVADA**  
_Nota(s): Instalação, fabricação e controle operacional do sistema submarino: integridade, rastreabilidade e envelope de segurança; Monitoramento de vazamentos, restrições de fluxo e anomalias de integridade em linhas e equipamentos submarinos; Gestão de integridade, fadiga e resposta a anomalias em risers e sistemas submarinos_

**P:** Próximo da vida de projeto, uma linha com riser ligado a manifold passa a mostrar aumento de queda de pressão até o separador. O fluido também mudou de composição, e a inspeção visual inicial ainda não confirmou vazamento nem restrição. Parte da equipe quer atribuir o desvio ao envelhecimento em operação; outra suspeita de dano introduzido na fabricação ou no lançamento. Qual encaminhamento técnico melhor separa essas hipóteses e define a resposta imediata?

**R:** Primeiro, o desvio deve ser tratado formalmente como anomalia operacional, com registro e investigação, e não como envelhecimento presumido. A leitura hidráulica só é válida se comparada com referência compatível com a vazão, a razão gás-líquido e o water-cut atuais; sem isso, mudança de composição pode simular perda de integridade. Em paralelo, a investigação deve recuperar o as built e os registros de fabricação e instalação para verificar rastreabilidade de materiais, local de aplicação, qualificação de executantes e evidências da instalação, incluindo monitoramento de tensão no lançamento e controle para minimizar dano ao revestimento. A inspeção submarina deve então ser dirigida aos mecanismos plausíveis e ao entorno da linha. Se, mesmo assim, a origem permanecer inconclusiva ou faltarem dados/documentos, a decisão correta é priorizar a anomalia e reduzir a incerteza com inspeções adicionais, eventual reavaliação por modelagem e uso de premissas conservadoras antes de sustentar continuidade operacional.

### Sistema e operação de pull in de risers

**facil · APROVADA**  
_Nota(s): Sequência operacional do pull-in do topo do riser entre PLSV e unidade flutuante_

**P:** Por que é necessária a instalação de uma ferramenta no topo do riser antes da transferência para a unidade flutuante, e qual é o papel dos cabos de aço nessa etapa?

**R:** A ferramenta no topo do riser é necessária porque fornece o meio para viabilizar a manobra de transferência da extremidade superior do riser da embarcação de lançamento para a unidade flutuante. Nessa etapa, os cabos de aço fazem a ligação usada para executar essa transferência, normalmente interligando o riser à embarcação de lançamento durante a passagem do topo até a unidade onde ocorrerá a conexão.

**media · APROVADA**  
_Nota(s): Sequência operacional do pull-in do topo do riser entre PLSV e unidade flutuante_

**P:** Em uma instalação com etapa de transferência do topo do riser entre a embarcação de lançamento e o FPSO, quais pontos do procedimento precisam ser observados para essa fase e como eles delimitam o início da operação?

**R:** Os pontos destacados no procedimento são o posicionamento do PLET e a máxima aproximação do PLSV ao FPSO. A máxima aproximação é a condição que define a aproximação máxima do topo do riser antes de começar sua transferência para o FPSO. Assim, o início do pull-in fica delimitado pelo atendimento dessa condição prevista no procedimento, e o posicionamento do PLET também deve estar conforme o que foi definido para a instalação.

**dificil_A · REPROVADA: escopo, tipo_ok**  
_Nota(s): Posicionamento e controle de heading do FPSO na interface com turret, risers e umbilicais_

**P:** Duas configurações de FPSO estão em análise para operar conectadas ao campo por risers e umbilicais. Na primeira, a unidade tem turret à vante e é deixada girar naturalmente em torno desse ponto. Na segunda, o turret fica mais ao meio do casco e a unidade usa thrusters comandados por Dynamic Positioning (DP) para manter aproamento e posição. Qual é a diferença funcional principal entre essas arquiteturas na forma de controlar a orientação da unidade na interface com o sistema submarino?

**R:** Na arquitetura com turret à vante, a orientação resulta predominantemente do weathervaning: a unidade gira passivamente em torno do ponto de conexão, enquanto o turret preserva a ligação com risers e umbilicais durante essa rotação. Na arquitetura com turret mais ao meio, a orientação não é deixada principalmente ao alinhamento natural da embarcação; heading e posição passam a ser corrigidos ativamente por thrusters. Nesse caso, o DP integra geração de potência, propulsão, sensores e controle para usar as medições e ajustar direção e potência dos thrusters, mantendo a unidade na posição e no aproamento requeridos. Em ambas, o turret continua sendo a interface que permite girar sem perder as conexões submarinas; o que muda é se a orientação decorre sobretudo do giro passivo em torno do turret ou de correções ativas de heading e posição.

**dificil_B · APROVADA**  
_Nota(s): Interfaces críticas entre turret, amarração e risers durante aproximação, pull-in e operação conectada em FPSOs; Perda de posição ou de heading em FPSO com turret: cadeia causal até torção de amarrações, contato com risers e enquadramento como elemento crítico de segurança; Perda de posição, amarração e proteção de risers em operações de pull in sob mau tempo_

**P:** Durante o pull-in de um riser, um FPSO monocaio com turret e thrusters para manter heading sofre perdas de heading que são recuperadas em seguida, enquanto o tempo piora. O arranjo geométrico entre amarrações e risers foi considerado com boa folga, e parte da equipe quer continuar por entender que o controle ainda se recupera. Qual decisão técnica é mais adequada nesse momento e por quê?

**R:** A decisão mais adequada é suspender preventivamente a operação, sem tratar a recuperação momentânea do heading como evidência suficiente de segurança. Perdas recorrentes de heading sob piora ambiental indicam redução de margem operacional. Nesse contexto, o desvio pode evoluir de excursão recuperável para twist do turret; se houver degradação adicional do controle dos thrusters e o turret não girar como necessário, a torção das amarrações pode reduzir as folgas até contato com os risers. A boa geometria entre linhas ajuda em condição normal, mas não elimina o risco em cenário extremo de twist. Se houver rotação anormal do turret, suspeita de contato ou evento severo, o retorno não deve se basear só em sinais de bordo; em arranjos com bóia latched e amarrações sem medição normal de tensão em água, a condição das linhas precisa ser confirmada por inspeção em água antes de retomar.

## Produção e Processo (Medição Fiscal e Sistema de Alívio)

### Compressão de Gás

**facil · APROVADA**  
_Nota(s): Controle operacional e sensibilidade dos compressores às condições do gás em sistemas offshore_

**P:** Qual é a função do compressor na planta offshore e como esse aumento de pressão e/ou densidade viabiliza os diferentes destinos do gás produzido?

**R:** O compressor transfere energia do acionador para o gás, elevando seu estado de energia por aumento de pressão e/ou densidade. Isso permite que o gás siga adiante no escoamento e no processamento da planta. Em sistemas offshore, essa compressão viabiliza que o gás produzido seja encaminhado, após o tratamento, para diferentes usos operacionais, como gás combustível, gas lift, exportação e, em alguns arranjos, reinjeção. Nessa aplicação, a pressão de sucção é uma variável central de controle, porque sustentar essa condição ajuda a estabilizar a alimentação da compressão e manter as rotas de utilização do gás a jusante.

**media · APROVADA**  
_Nota(s): Controle operacional e sensibilidade dos compressores às condições do gás em sistemas offshore_

**P:** Em um trem de compressão offshore, a pressão de sucção precisa permanecer estável, mas a vazão recebida por cada estágio varia ao longo da operação. Qual é a diferença funcional entre variação de rotação, estrangulamento na sucção e reciclo por estágio, e o que cada uma dessas estratégias corrige?

**R:** A variação de rotação atua na capacidade global da máquina para manter a pressão de sucção estável. O estrangulamento na sucção também é usado para sustentar essa pressão, impondo uma restrição na entrada quando essa é a estratégia adotada. Já o reciclo por estágio não substitui o controle principal de capacidade: ele corrige a vazão efetiva vista por cada estágio, ajustando-a para perto do setpoint da malha de vazão na sucção, que depende da rotação da máquina. Assim, rotação e throttle corrigem principalmente o comportamento da pressão de sucção, enquanto o reciclo corrige o desbalanceamento entre a capacidade efetiva do estágio e a vazão que ele recebe.

**dificil_A · APROVADA**  
_Nota(s): Influência das pressões de sucção e de descarga na aplicação e no controle operacional da compressão de gás_

**P:** Um trem de compressão entra em instabilidade. As leituras mostram sucção dentro do perfil normal, mas pressão de descarga persistentemente alta. Sem evidência adicional de falha mecânica, a ação prioritária deve focar a condição do sistema, a estratégia de controle ou a adequação do tipo de compressor à aplicação? Justifique pela variável afetada.

**R:** A prioridade é tratar a anomalia de descarga como critério primário de diagnóstico e intervenção, concentrando a análise na condição imposta ao compressor e na resposta do controle nesse lado do sistema. Como a pressão anormal está localizada na descarga, o desvio não deve ser interpretado genericamente como perda de desempenho da máquina. No trem de compressão, pressão alta ou baixa na admissão e na descarga são entradas formais para identificação, diagnóstico e procedimentos corretivos; por isso, a decisão correta começa pela variável afetada e pelo lado em que ela aparece. Assim, antes de concluir por inadequação do tipo de compressor, deve-se enquadrar o problema como uma condição operacional de descarga a ser tratada pelo diagnóstico e pelas ações corretivas correspondentes.

**dificil_B · APROVADA**  
_Nota(s): Inspeção em revisões de compressores centrífugos e mitigação de vibração/pulsação em tubulações associadas; Arquiteturas de selagem em compressores multestágio e controle de vazamentos; Vibração e pulsação em compressores e tubulações associadas: mecanismos, danos, fadiga e mitigação_

**P:** Um compressor centrífugo multestágio entrou em revisão após aumento de vazamento e desgaste na selagem, enquanto as linhas conectadas vinham com vibração elevada, pequenos ramais exigindo reforço de suporte e sem viabilidade imediata de reduzir a pulsação nem trocar a tubulação. Na abertura da carcaça ainda há possibilidade de inspecionar internamente antes da retirada do rotor. Qual linha de diagnóstico e mitigação deve ser priorizada para não tratar a selagem como causa primária por engano?

**R:** A prioridade é investigar a vibração do conjunto máquina-linhas como causa antecedente e preservar a evidência interna antes de remover o rotor. Na abertura, devem ser observados estado interno e folgas entre partes fixas e móveis, porque esses indícios perdem valor diagnóstico após a retirada do rotor. O desgaste de labirintos ou selos mecânicos pode resultar de contato mecânico causado por vibração anormal do eixo, então a falha de selagem não deve ser isolada do comportamento rotodinâmico. Em paralelo, a vibração nas linhas e ramais deve ser tratada pela resposta estrutural disponível no caso: suportação mais rígida por abraçadeiras para restringir vibração transversal sem bloquear dilatação axial e, como não é viável reduzir a pulsação nem substituir a linha, aplicação de amortecimento localizado para baixar amplitudes. O diagnóstico correto integra evidências internas do compressor com a resposta vibratória externa do sistema conectado.

### Medição Fiscal de óleo, medição fiscal de gás e transferência de custódia em operações de offloading

**facil · APROVADA**  
_Nota(s): Comunicação de falhas do sistema de medição e efeitos regulatórios sobre não conformidade e recálculo da produção_

**P:** Qual é a função da notificação de falha do sistema de medição na passagem de uma ocorrência técnica para a avaliação da confiabilidade dos dados de produção?

**R:** Ela formaliza a ocorrência de falha como entrada para o processo de fiscalização da medição, permitindo avaliar se a confiabilidade dos dados informados foi comprometida. Se a análise indicar não conformidade dos dados ou dos processos de medição com potencial de gerar resultados incorretos, podem ser instaurados procedimentos de recálculo da produção. Como o controle de não conformidade exige verificar não só o equipamento que falhou, mas todos os procedimentos, equipamentos e processos envolvidos na medição capazes de produzir resultados incorretos, a notificação funciona como elo entre a detecção técnica da falha e a revisão regulatória dos volumes informados.

**media · REPROVADA: correcao_tecnica, suporte**  
_Nota(s): Comunicação de falhas do sistema de medição e efeitos regulatórios sobre não conformidade e recálculo da produção_

**P:** Em uma instalação offshore, foi identificada possível inconsistência na medição fiscal e a equipe precisa saber quais eventos podem abrir processo de recálculo da produção. Quais são os principais gatilhos e qual deles tende a ser o mais frequente?

**R:** Os principais gatilhos são notificação de falha do sistema de medição, inspeções, declarações das concessionárias, denúncias e validação da produção. Entre eles, a notificação de falha do sistema de medição tende a ser o canal mais frequente de abertura desses processos. Isso ocorre porque, quando a falha ou a não conformidade coloca em dúvida a veracidade dos dados informados, a fiscalização da medição pode instaurar recálculo da produção.

**dificil_A · APROVADA**  
_Nota(s): Configuração do sistema de medição para transferência de custódia em offloading de FPSO e variáveis para cálculo do volume compensado_

**P:** Durante o planejamento da medição de custódia no offloading, a equipe avalia duas alternativas: implantar monitoração online contínua de vazão, pressão estática e temperatura, ou limitar a instrumentação à medição direta de pressão estática na parede do duto e temperatura do escoamento. O orçamento é restrito, mas a operação quer manter o cálculo do volume compensado. Qual decisão técnica é mais consistente e qual o impacto dessa escolha sobre a estratégia de medição?

**R:** A decisão técnica depende de compatibilizar rigor metrológico com viabilidade de investimento. Se a monitoração online contínua de vazão, pressão estática e temperatura não se justificar economicamente, é consistente limitar a instrumentação à medição direta de pressão estática na parede do duto e temperatura do escoamento, porque essas duas variáveis devem compor o conjunto mínimo para viabilizar o cálculo do volume compensado. Nessa escolha, a estratégia de medição deixa de depender de uma base online completa em tempo real e passa a concentrar a representatividade do resultado no algoritmo de cálculo aplicado ao volume. Se houver recursos e interesse em maior representatividade operacional do escoamento, a monitoração online completa pode ser adotada, mas ela exige transmissores e sistemas automáticos adicionais. Em qualquer caso, a medição de custódia não se resume ao medidor de vazão; ela envolve o conjunto integrado da estação de medição e seus dispositivos de aquisição e cálculo.

**dificil_B · APROVADA**  
_Nota(s): Projeto, configuração e instalação do sistema de medição fiscal; Calibração, incerteza e rastreabilidade metrológica dos sistemas de medição fiscal de óleo; Requisitos metrológicos e configuração do sistema de medição fiscal e de transferência de custódia_

**P:** Uma linha de medição fiscal de óleo em offloading apresenta desvio recorrente entre o volume operacionalmente esperado e o volume reconhecido pelo sistema. O medidor principal e o computador de vazão permanecem sem alarmes, e existe calibração anterior do medidor. Qual diagnóstico deve ser priorizado para distinguir erro de instalação de calibração insuficientemente representativa, e que evidência técnica aponta para cada origem?

**R:** A prioridade é verificar o sistema completo, não só o medidor. Primeiro, confronte a instalação real com o que foi usado no dimensionamento e na calibração: trechos retos a montante e a jusante, diâmetro, espessura e rugosidade da linha. Se essas condições não forem compatíveis, o indício é de erro hidráulico de instalação, porque o escoamento no medidor mudou em relação à condição considerada. Em paralelo, avalie se a calibração reproduziu condições similares às de operação — vazão, pressão, temperatura, viscosidade e densidade — e se a incerteza foi formalmente estimada, registrada e mantida com rastreabilidade. Se a calibração existir, mas sem essa representatividade metrológica e sem base formal de incerteza, o indício é de fator de calibração inadequado ao uso real. A ausência de alarmes no medidor ou no computador de vazão não elimina nenhuma dessas duas causas.

### Operação de Separadores Trifásicos

**facil · APROVADA**  
_Nota(s): Controle coordenado de nível e interface nas saídas líquidas do separador trifásico_

**P:** Qual é a função da válvula da linha inferior de água livre em um separador trifásico, e como ela se relaciona com o controle da interface água-óleo?

**R:** A válvula da linha inferior regula a vazão de saída da água livre acumulada no fundo do separador. Sua abertura é comandada pelo controle da interface água-óleo, não pelo nível total de líquido. Assim, quando a posição da interface varia, a válvula ajusta a descarga de água para manter a camada aquosa na faixa desejada e preservar a separação entre água e óleo.

**media · APROVADA**  
_Nota(s): Controle coordenado de nível e interface nas saídas líquidas do separador trifásico_

**P:** Em um separador trifásico com pressão controlada pela saída de gás no topo, como a abertura das válvulas de saída de óleo e de água deve regular as vazões de descarga para manter o inventário líquido e a separação estáveis?

**R:** As válvulas das saídas líquidas devem ajustar as vazões de descarga conforme as variáveis de nível medidas no vaso. A saída de óleo responde ao controle de nível do líquido para manter o inventário na faixa desejada. A saída de água, pela linha inferior, responde ao nível de interface água-óleo para regular especificamente a retirada da água livre. Dessa forma, o inventário líquido é controlado sem usar a saída de gás para corrigir níveis, e a posição da interface é mantida pela própria descarga de água, o que favorece a estabilidade da separação.

**dificil_A · APROVADA**  
_Nota(s): Gestão de integridade de vasos em operação no FPSO: corrosão, inspeção, cadastro de ativos e isolamento para intervenção_

**P:** Em um FPSO, um separador trifásico passou a operar por período prolongado com condições reais de processo diferentes das premissas de projeto. O vaso continua com inspeções periódicas programadas, porém parte do histórico de manutenção e inspeção está incompleta no cadastro, e a equipe argumenta que a conformidade com requisitos de classe é suficiente para manter o regime atual. Nesse cenário, essa mudança já justifica revisar o regime de inspeção e reforçar a abordagem baseada em risco?

**R:** Sim. Operar fora do envelope de projeto já é uma condição que eleva o perigo potencial de perda de contenção, portanto aumenta a necessidade de reavaliar se frequência, escopo e prioridade das inspeções continuam adequados. Como o sistema de integridade pode ser estruturado por inspeção prescritiva e/ou baseada em risco, a resposta técnica não é manter o regime por inércia, mas revisar o plano quando a condição real de processo mudou e a incerteza aumentou. A situação fica ainda mais forte porque o histórico incompleto no cadastro reduz a visibilidade sobre inspeções, manutenção e reparos, o que prejudica a avaliação da condição do ativo. Além disso, conformidade com requisitos de classe, isoladamente, não basta quando pode haver lacunas de cobertura no sistema de integridade. Nessa condição, o adequado é reforçar o controle do ativo e revisar o regime com base no risco.

**dificil_B · APROVADA**  
_Nota(s): Formação de espuma, efeitos operacionais e mitigação no separador trifásico; Controle de níveis e da interface óleo-água em separadores trifásicos: como faixa estreita, espuma, nível alto e variações térmicas degradam a separação; Shutdown e intertravamentos na operação de separadores trifásicos_

**P:** Após uma mudança no fluido produzido, um separador trifásico passa a apresentar controle de nível instável, alarmes recorrentes de alto nível e indícios de líquido na linha de gás. Em alguns eventos, o desvio some antes da confirmação em campo, mas a lógica de proteção já foi sensibilizada. Qual encadeamento técnico explica como um problema de separação pode evoluir até alarme/intertravamento/shutdown, e como diferenciar aumento real de inventário líquido de atuação provocada por espuma?

**R:** A hipótese integradora é formação de espuma. Impurezas no líquido e a própria natureza do óleo podem favorecer espuma, que ocupa volume útil, reduz a área de escoamento do gás e aumenta o arraste de líquido na saída de gás. Ao mesmo tempo, a espuma dificulta o controle de nível e pode ser percebida pelos instrumentos como condição de nível alto. Assim, um problema que começa como perda de eficiência de separação pode sensibilizar alarme, intertravamento e shutdown; além disso, o líquido carreamento no gás pode alcançar compressores. Para diferenciar causa e sintoma, é preciso considerar que atuação por nível alto pode vir de dois mecanismos distintos: aumento real do inventário líquido, que também favorece arraste no gás, ou presença de espuma no vaso, que degrada a medição e a condição aparente do nível sem corresponder apenas a líquido claro.

### Operação de Tratadores Eletrostáticos

**facil · REPROVADA: suporte**  
_Nota(s): Acoplamento entre o tratador eletrostático e a carga ao sistema de água produzida_

**P:** Por que o desempenho do tratador eletrostático influencia não só a qualidade do óleo exportado, mas também a carga enviada ao sistema de água produzida?

**R:** Porque a separação no conjunto separador-tratador define para qual corrente a água e o óleo remanescentes vão seguir. Se o tratador remove água da corrente oleosa, ele melhora o enquadramento do óleo. Mas, se a separação se desorganiza, parte do óleo pode sair pela corrente aquosa e aumentar a carga de entrada do sistema de água produzida. Isso é relevante porque esse sistema deve enquadrar a água para descarte, reinjeção ou utilidades e foi projetado para receber, na saída do separador trifásico, água com óleo disperso em torno da faixa prevista de projeto, não cargas de óleo bruto com baixa diluição.

**media · REPROVADA: suporte**  
_Nota(s): Acoplamento entre o tratador eletrostático e a carga ao sistema de água produzida_

**P:** Em uma campanha, a qualidade da água produzida piora progressivamente, mas o óleo exportado ainda atende à especificação de água. Sem evidência de vazamento, o que esse quadro sugere sobre a separação no separador trifásico ou no tratador eletrostático?

**R:** Sugere desvio de separação com perda de óleo para a corrente aquosa. O atendimento da especificação do óleo não garante que a separação global esteja adequada, porque parte do óleo pode estar sendo deslocada para a água produzida. Isso aumenta a carga de entrada do sistema de tratamento de água justamente na corrente que ele precisa enquadrar para descarte, reinjeção ou utilidades. Como esse sistema foi projetado para operar com água contendo óleo disperso na faixa de projeto na saída do separador trifásico, e não com carga de óleo bruto pouco diluída, a piora da água produzida é compatível com sobrecarga por perda de separação a montante.

**dificil_A · APROVADA**  
_Nota(s): Metas de qualidade do óleo tratado: BS&W e salinidade para exportação no contexto do tratador eletrostático_

**P:** Em uma unidade offshore, a separação primária está estável e o óleo sai do separador com boa remoção inicial de água. Ainda assim, a equipe não considera a corrente pronta para exportação e mantém o envio ao tratador eletrostático. Por que essa decisão é tecnicamente correta, considerando a origem do petróleo processado e as metas de qualidade da unidade?

**R:** Porque a corrente exportável é o óleo tratado resultante da mistura dos fluidos produzidos pelos poços interligados à unidade, e a condição de exportação não é definida apenas pela separação primária. O tratamento deve entregar óleo estabilizado e enquadrado simultaneamente em temperatura, salinidade e BS&W. Nesse arranjo de processo, o tratador eletrostático faz parte desse condicionamento final, pois sua função é enquadrar o teor de BS&W do óleo após o separador. Assim, mesmo com boa separação primária, a corrente ainda pode não atender ao conjunto das exigências de exportação; por isso, a etapa eletrostática permanece necessária antes do envio por oleoduto ou navio aliviador.

**dificil_B · APROVADA**  
_Nota(s): Pré-lavagem com água livre separada no condicionamento da emulsão antes do tratador eletrostático; Operação de tratadores eletrostáticos: pré-lavagem, dessalinização e intensificação da coalescência conforme o teor de água; Metas de qualidade do óleo tratado: BS&W e salinidade para exportação no contexto do tratador eletrostático_

**P:** Em um FPSO, o óleo tratado passa a sair com salinidade acima da meta e BSW moderadamente maior. O tratador eletrostático permanece energizado, mas há suspeita de alteração na alimentação ou na hidráulica interna antes da zona de maior campo. Qual diagnóstico deve ser priorizado e por quê?

**R:** Deve-se priorizar o diagnóstico de perda da sequência interna de condicionamento antes da região eletrostática, especialmente da pré-lavagem com água livre previamente separada e da distribuição da mistura no vaso. Essa etapa remove sais e partículas e já promove coalescência de parte da água dispersa. Com isso, a emulsão chega menos estável à região de campo. Além disso, à medida que a quantidade de água dispersa diminui, a mistura fica mais próxima dos eletrodos e o campo entre as interfaces se intensifica, sustentando reduções sucessivas da fase aquosa dispersa. Se essa preparação se deteriora, o campo elétrico passa a atuar sobre uma emulsão pior condicionada, o que reduz a remoção de água e compromete ao mesmo tempo o enquadramento de BSW e de salinidade, ambos exigidos para o óleo de exportação.

### Operação Geral FPSO

**facil · APROVADA**  
_Nota(s): Sistema logístico offshore e flexibilidade do FPSO no escoamento por alívio_

**P:** Qual é a finalidade da logística offshore para a continuidade operacional de uma unidade marítima?

**R:** Garantir o atendimento da unidade marítima com os insumos e equipamentos necessários à operação, por meio de um fluxo integrado de materiais e informações entre fornecedores, armazéns e terminais portuários.

**media · APROVADA**  
_Nota(s): Sistema logístico offshore e flexibilidade do FPSO no escoamento por alívio_

**P:** Em uma locação pioneira, um FPSO opera com armazenamento a bordo e exportação por alívio. Como esse arranjo afeta a necessidade de linhas de exportação, oleodutos e manifolds submarinos?

**R:** Esse arranjo reduz e pode eliminar a necessidade desses elementos de infraestrutura submarina, porque o FPSO armazena o óleo produzido e depois o transfere por alívio para retirada da carga, em vez de depender de uma rota fixa de exportação.

**dificil_A · APROVADA**  
_Nota(s): Tratamento de água produzida como mitigação de perdas operacionais em FPSO_

**P:** Em um FPSO de campo maduro, a produção de água aumentou e, ao mesmo tempo, hidrociclone e flotador ficaram indisponíveis, com queda perceptível da eficiência de separação óleo-água. A equipe tende a tratar o evento apenas como piora da qualidade da água tratada. Por que, tecnicamente, essa indisponibilidade também caracteriza uma restrição operacional da unidade?

**R:** Porque, quando a carga de água produzida é elevada, o tratamento deixa de ser acessório e passa a limitar a operação: a capacidade da estação precisa ser compatível com a demanda corrente de água produzida. Nesse contexto, hidrociclone e flotador não são etapas periféricas; eles atuam de forma complementar na remoção do óleo residual da água. Se ficam indisponíveis, a capacidade de separação de óleo da água cai, e a perda não se restringe à qualidade da corrente tratada: a própria capacidade operacional do sistema de tratamento fica reduzida. Assim, com alta produção de água, a indisponibilidade dessas etapas impõe restrição à unidade porque o tratamento passa a não atender adequadamente a carga recebida, exigindo verificação de capacidade e eventual otimização para sustentar a operação.

**dificil_B · APROVADA**  
_Nota(s): Confiabilidade das medições e aderência dos dados à realidade operacional no monitoramento de FPSO; Confiabilidade das informações operacionais para controle do processo e conformidade em FPSO; Diagnóstico de desvios operacionais e falhas de instrumentação/automação em FPSO_

**P:** Em um FPSO com controle manual, faltam medidores de vazão e a medição online de TOG é pouco confiável. Um tanque registrado como contendo óleo vem recebendo, na prática, água offspec, e a troca de turno não assegura conhecimento uniforme de mudanças e condições operacionais. No supervisório, parte das indicações recorrentes aparece como evento rotineiro. Diante de interpretações divergentes entre turnos, o que deve ser diagnosticado como prioridade para decidir se há perda real de desempenho do processo ou perda de observabilidade da planta?

**R:** A prioridade é diagnosticar perda de observabilidade da planta. Sem vazão confiável e sem TOG online confiável, o acompanhamento do desempenho já fica enfraquecido no controle manual. Se, além disso, o inventário está classificado como óleo quando o recebimento real é água offspec, a interpretação do que o sistema contém e movimenta parte de uma premissa errada. A divergência entre turnos ainda pode ser ampliada quando mudanças e condições operacionais não são transferidas de forma estruturada e quando indicações que não exigem ação são tratadas como se orientassem a resposta operacional. Antes de concluir por perda real de desempenho, é preciso restabelecer a base diagnóstica: validar a classificação pelo recebimento real, separar evento de alarme, e assegurar que limites operacionais seguros e condições de turno sejam conhecidos pela equipe.

### Produção, processo e processamento do óleo

**facil · REPROVADA: correcao_tecnica, suporte, sem_generalizacao**  
_Nota(s): Inspeção e prontidão operacional de vasos, trocadores, filtros e tubulações_

**P:** Por que a inspeção interna, antes da partida ou do carregamento do leito, deve verificar ao mesmo tempo a integridade dos componentes internos e a presença de umidade, resíduos, depósitos ou produtos de corrosão?

**R:** Porque a liberação para a etapa seguinte depende de confirmar duas condições ao mesmo tempo: que os componentes internos estejam em condição correta para cumprir sua função e que o interior do equipamento não tenha contaminantes incompatíveis com essa função. Em vasos para carregamento de zeólitas, isso inclui verificar descontinuidades no refratário e presença excessiva de umidade ou água acumulada. Em filtros, inclui confirmar montagem correta dos internos e integridade dos elementos. Em trocadores e tubulações, inclui verificar resíduos sólidos, depósitos e resíduos de corrosão. Se qualquer desses desvios existir, a condição interna não corresponde à prevista para entrada em serviço ou para o carregamento do leito.

**media · APROVADA**  
_Nota(s): Inspeção e prontidão operacional de vasos, trocadores, filtros e tubulações_

**P:** Durante a preparação para partida, a inspeção encontra resíduos sólidos e depósitos no feixe de um trocador, além de depósitos no casco e na linha de entrada de utilidade. Como isso pode degradar o desempenho do trocador antes mesmo da operação contínua?

**R:** Esses achados indicam que o trocador já entra em serviço com condição interna diferente da prevista. Resíduos e depósitos no feixe reduzem a efetividade da troca térmica. Depósitos no casco e na linha de entrada de utilidade podem alterar a distribuição do escoamento e restringir passagens internas. Assim, mesmo antes de operação contínua, o equipamento pode partir com menor capacidade de transferência de calor e pior desempenho global, razão pela qual esses pontos devem ser verificados na inspeção de prontidão.

**dificil_A · APROVADA**  
_Nota(s): Separação primária e estabilização do óleo no trem de processo de FPSO_

**P:** Em um FPSO, o óleo na saída do trem segue inadequado para armazenamento. Ao mesmo tempo, a operação registra oscilações de carga na entrada da planta e variação de alimentação nos equipamentos a jusante do primeiro separador. Como diferenciar indícios de estabilização insuficiente daqueles associados a golfadas mal amortecidas no separador de produção, e qual é o efeito típico de cada mecanismo sobre o restante da planta?

**R:** Indícios de estabilização insuficiente apontam para remoção incompleta dos componentes voláteis ainda dissolvidos no óleo. O diagnóstico deve se concentrar nas condições aplicadas aos estágios de estabilização em série e na necessidade de aquecimento para favorecer a vaporização desses componentes. Nesse caso, o problema central é a permanência de gás dissolvido no óleo de saída.

Indícios associados a golfadas mal amortecidas aparecem como flutuações de carga transmitidas adiante do primeiro separador. Como o separador de produção deve atuar também como tanque pulmão, recebendo vazão flutuante e entregando vazão mais regular, a falha nesse amortecimento tende a se manifestar como alimentação instável aos equipamentos a jusante e perda de previsibilidade do desempenho do trem.

Em resumo: estabilização insuficiente afeta diretamente a condição do óleo por retenção de voláteis; golfadas mal amortecidas afetam principalmente a regularidade da alimentação e a estabilidade operacional das etapas seguintes.

**dificil_B · APROVADA**  
_Nota(s): Dessalgação do óleo: mecanismo, integração com a desidratação e impacto na qualidade de exportação; Recirculação de água separada quente dos tratadores eletrostáticos e sua interface com o header de produção; Incrustação mineral por carbonatos no topside: efeito de temperatura, pH, despressurização e suporte à mitigação por modelagem de mistura de águas_

**P:** Uma unidade quer intensificar a redução de sal no óleo aumentando a integração térmica com água separada quente dos tratadores eletrostáticos e mantendo injeção de água de lavagem. Ao mesmo tempo, há preocupação com incrustação carbonática em linhas e equipamentos do topside após aquecimento e despressurização. Qual decisão técnica é mais adequada para conciliar tratamento do óleo e integridade do sistema?

**R:** A decisão mais adequada é manter a dessalgação integrada à desidratação, sem tratar a recirculação quente como benefício automático nem como agravante automático, e reavaliar a mitigação de incrustação pela pior mistura de águas do sistema. A redução de sal depende de água de lavagem aquecida, contato dessa água com o óleo e remoção efetiva da fase aquosa no vaso por coalescência e decantação sob campo elétrico. Porém, no topside, a tendência à incrustação carbonática cresce com temperatura, pH e despressurização com liberação de CO2. Nessa avaliação, a água recirculada quente merece análise, mas seu efeito direto sobre a criticidade tende a ser baixo; a água de diluição usada para reduzir a salinidade do óleo é a variável com maior impacto sobre o potencial de incrustação. Portanto, a priorização correta é revisar a mistura de águas e a dosagem de inibidor com base no cenário mais crítico, não simplesmente maximizar a recirculação.

### Produtos químicos

**facil · APROVADA**  
_Nota(s): Coagulantes, floculantes e condicionamento químico da emulsão óleo-em-água na água produzida para descarte offshore_

**P:** Como os floculantes atuam, em termos básicos, sobre uma emulsão óleo-em-água na água produzida?

**R:** Eles atuam pela adsorção na interface das gotas de óleo dispersas e, a partir dessa interação, promovem neutralização de cargas e/ou formação de pontes inter-particulares. Esse mecanismo desestabiliza a emulsão e favorece a aproximação das gotas e de outros materiais poluentes para formar agregados maiores.

**media · APROVADA**  
_Nota(s): Coagulantes, floculantes e condicionamento químico da emulsão óleo-em-água na água produzida para descarte offshore_

**P:** Após o separador água-óleo, uma corrente de água produzida recebe condicionamento químico e segue para flotação. Se a dosagem formar agregados maiores, como isso afeta a etapa física seguinte e qual é a diferença entre o papel da química e o da flotação?

**R:** A formação de agregados maiores torna a remoção na etapa física seguinte mais favorável, porque esses agregados ficam mais facilmente flotáveis ou decantáveis do que gotas pequenas e estáveis. O papel da química é desestabilizar a emulsão e promover a coagulação/floculação para gerar esses agregados. O papel da flotação ou da decantação é retirar da corrente os agregados já formados; a dosagem química prepara a corrente, mas não substitui a separação física.

**dificil_A · APROVADA**  
_Nota(s): Compatibilidade da água de injeção com a formação e mitigação de incrustações por sulfatos_

**P:** Em um campo com injeção de água do mar, a água produzida de um poço passa a mostrar fração crescente de água injetada. A partir daí surgem perda de desempenho por restrição na coluna de produção e, em seguida, deposição também em linhas e equipamentos de superfície. Antes desse estágio, o poço não apresentava esse padrão. A hipótese de incompatibilidade entre água injetada e água de formação, com precipitação de sulfatos insolúveis, é consistente com esse quadro? Justifique pelo momento e pelos locais dos sintomas.

**R:** Sim. O quadro é consistente porque a severidade da incrustação aumenta quando a água injetada alcança o produtor, isto é, após o breakthrough, momento em que cresce o contato entre a água injetada e a água de formação. Sob condições termodinâmicas adequadas, essa mistura pode gerar depósitos insolúveis, incluindo sulfatos de bário, estrôncio e cálcio. A distribuição dos sintomas também é compatível com essa hipótese, porque esses depósitos podem ocorrer desde regiões associadas ao reservatório e à vizinhança do poço até a coluna de produção, linhas e equipamentos de superfície. O fato de o problema piorar justamente com o aumento da fração de água injetada reforça a suspeita e justifica monitoramento contínuo a partir desse estágio.

**dificil_B · APROVADA**  
_Nota(s): Controle químico de corrosão e de H2S em linhas e equipamentos do processamento de óleo; Compatibilidade entre produtos químicos e efeitos cruzados no desempenho do tratamento em FPSOs; Ensaios e monitoramento de desempenho e compatibilidade de produtos químicos em FPSOs_

**P:** Uma linha de aço-carbono teve queda do problema de H2S após introdução de glioxal, sem formação de sais, mas os indicadores seguintes sugerem meio mais agressivo ao metal. A equipe quer manter o sequestrante e adicionar inibidor de corrosão. Qual critério técnico deve orientar essa decisão para evitar uma solução apenas aparente, e como validar o pacote químico antes e depois da aplicação?

**R:** A decisão deve se basear na corrosividade do meio resultante do tratamento e no desempenho da combinação real de produtos no material exposto, não no benefício isolado do sequestrante nem na eficácia isolada do inibidor. O glioxal pode remover H2S sem incrustação, mas em baixo pH torna o meio corrosivo para aço-carbono; o inibidor pode controlar essa corrosão ao formar e manter barreira adsorvida sobre o filme de óxido, porém combinações químicas podem tanto piorar quanto melhorar a proteção. Portanto, a validação deve incluir ensaio representativo com a combinação prevista de sequestrante e inibidor no meio relevante e com corpo de prova compatível com o sistema, por método de eficiência anticorrosiva. Em operação, é preciso confirmar por monitoramento das taxas de corrosão e investigar os pontos de maior criticidade, sem generalizar resultado favorável obtido em um único ponto monitorado.

### Sistema de Alívio e Flare

**facil · APROVADA**  
_Nota(s): Comissionamento, testes funcionais, handover e capacitação operacional em sistemas de alívio, despressurização e flare_

**P:** Qual é a função do comissionamento na transição entre construção e operação, e por que o uso de checklists é necessário para assegurar aderência ao projeto detalhado?

**R:** O comissionamento faz a transição da montagem física para a prontidão operacional ao verificar, inspecionar e testar os componentes do sistema e, depois, confirmar o funcionamento dos processos antes do início pleno da operação. Isso evita liberar uma planta apenas montada fisicamente, sem evidência de que os equipamentos e processos estejam operando como previsto. Os checklists são usados para garantir cobertura completa dos itens de projeto e da futura operação, verificando se todos os componentes necessários estão contemplados, disponíveis e operacionais conforme o projeto detalhado.

**media · APROVADA**  
_Nota(s): Comissionamento, testes funcionais, handover e capacitação operacional em sistemas de alívio, despressurização e flare_

**P:** Em um vendor package, a equipe de operação só participa após a entrega do equipamento já comissionado pelo fornecedor. Por que essa decisão tende a reduzir a capacidade futura de operação e manutenção da unidade?

**R:** Porque a participação de operadores e técnicos no comissionamento, junto com o pessoal do fornecedor, é o mecanismo que desenvolve familiaridade prática com o equipamento. Sem esse envolvimento, o pacote pode ser entregue com conhecimento operacional e de manutenção insuficiente na equipe que vai recebê-lo. Isso reduz a capacidade futura porque o aprendizado necessário para operar e manter o equipamento de forma competente depende dessa exposição prática, complementada por arranjos adequados de treinamento durante a transição para a operação.

**dificil_A · APROVADA**  
_Nota(s): Radiação térmica, dispersão e ignição segura em sistemas de flare e vent_

**P:** Após uma modificação no topside, uma rota de acesso e um painel crítico ficaram mais expostos à linha de visada da tocha. Além disso, na partida do flare pode haver um intervalo curto entre a abertura do gás e a ignição, e o vento no local varia de direção ao longo do dia. Como o estudo de radiação e dispersão deve ser usado para decidir se o arranjo permanece aceitável e o que o procedimento de partida precisa incorporar?

**R:** O estudo deve verificar, nos pontos reais de interesse da instalação, se a chama impõe radiação incidente admissível para pessoas e equipamentos, considerando os parâmetros de emissão e geometria da chama e a posição relativa desses pontos. Com isso, confirma-se se a rota de acesso, o painel crítico e outras áreas sensíveis permanecem aceitáveis no arranjo atual ou se ficaram expostos demais.

Ao mesmo tempo, a análise de dispersão deve mostrar se, no intervalo sem ignição, o gás não queimado pode atingir regiões vulneráveis, como o deck de processo, em função do vento e das características da liberação. Esses resultados precisam entrar no procedimento de partida: a ignição não pode ser tratada separadamente da abertura do gás, devendo considerar direção e velocidade do vento e os cenários de dispersão já avaliados, além de evitar venting não ignitado por tempo prolongado.

**dificil_B · REPROVADA: suporte**  
_Nota(s): Influência da contrapressão e do arranjo de descarga na seleção da PSV; Capacidade do sistema de flare, blowdown e vent frente a eventos combinados de sobrepressão; Dimensionamento e verificação dinâmica de PSV com interação com o sistema coletor de alívio_

**P:** Uma PSV de um vaso foi mantida após revisão porque, na verificação do cenário de sobrepressão do equipamento, o transiente mostrou pressão aceitável. Meses depois, em um upset com blowdown e alívio simultâneos para o mesmo flare, a pressão a montante de algumas PSVs permanece alta por mais tempo e há suspeita de abertura fora do esperado. Qual é o diagnóstico técnico mais consistente e qual decisão de projeto/operação deve ser priorizada?

**R:** O desvio mais consistente é a interação entre a PSV e o header comum sob evento combinado, não uma falha isolada do dispositivo. Uma PSV pode parecer adequada quando verificada para o equipamento protegido, mas perder desempenho se a descarga simultânea elevar a contrapressão no coletor além do admitido. Nessa condição, a contrapressão pode alterar a abertura de válvulas conectadas ao header e comprometer a proteção. A prioridade é reavaliar o sistema integrado: combinações críveis de alívio e blowdown, capacidade hidráulica do flare/header e adequação do tipo de PSV à contrapressão prevista. Se houver contrapressão relevante no coletor, a seleção de PSV balanceada é tecnicamente mais consistente do que a convencional. Se a capacidade simultânea do sistema receptor for insuficiente, a demanda deve ser compatibilizada com a capacidade disponível, por exemplo com despressurização faseada ou escalonada, em vez de presumir blowdown total simultâneo.

### Sistema de captação e tratamento de água do mar para injeção no reservatório

**facil · APROVADA**  
_Nota(s): Monitoramento microbiológico e indicadores de biofouling, MIC e souring em água do mar para injeção_

**P:** Como a combinação de sulfato, presença de H2S, Eh e pH pode ser usada para identificar atividade de bactérias redutoras de sulfato nas condições em que esses parâmetros servem para esse diagnóstico?

**R:** Essa identificação não deve se basear em um parâmetro isolado. A presença de H2S funciona como sinal de processo associado à geração de sulfeto, e a avaliação conjunta com dosagem de sulfato, Eh e pH permite reconhecer um quadro compatível com atividade de bactérias redutoras de sulfato nas condições em que esses parâmetros são aplicados para esse fim. Portanto, o diagnóstico decorre da convergência desses indicadores químicos para um ambiente e um metabolismo compatíveis com redução de sulfato.

**media · APROVADA**  
_Nota(s): Monitoramento microbiológico e indicadores de biofouling, MIC e souring em água do mar para injeção_

**P:** Em um sistema de água do mar para injeção com oxigênio disponível, como a atividade de bactérias oxidantes de ferro e nitrito pode ao mesmo tempo contribuir para entupimento de dutos e favorecer a criação de condições anaeróbias?

**R:** Essas bactérias podem participar da oxidação de Fe2+ para Fe3+. Esse mecanismo contribui para entupimento de dutos pela formação associada ao ferro oxidado. Ao mesmo tempo, a atividade microbiana consome o oxigênio disponível no sistema. Com esse consumo, o meio tende a perder a condição aerada e passa a favorecer a criação de condições anaeróbias.

**dificil_A · APROVADA**  
_Nota(s): Qualidade da água de injeção, compatibilidade com o reservatório e prevenção de incrustação em sistemas de água do mar de FPSO_

**P:** Após o início da injeção de água em um poço, a vazão de injeção cai e a pressão necessária para manter a operação aumenta. Pouco antes disso, a unidade passou a misturar correntes de água com características diferentes. As análises químicas da água indicam combinação favorável à precipitação após a mistura, e a inspeção encontra depósitos aderentes em componentes de escoamento, com pontos de pitting. Entre incompatibilidade química, deposição de sólidos, atividade bacteriana e corrosividade da água com formação de depósitos, qual é o mecanismo dominante mais provável e por quê?

**R:** O mecanismo dominante mais provável é a incompatibilidade química entre a água injetada e a água presente no sistema associado ao reservatório. A principal evidência é a mistura de águas com características diferentes, seguida por análises que indicam precipitação após a mistura. Esse quadro é compatível com a formação de sais pouco solúveis e incrustações, que podem obstruir componentes de escoamento, reduzir a permeoporosidade e favorecer corrosão localizada por pitting. Portanto, o pitting observado entra como efeito associado ao processo de incrustação por incompatibilidade, não como causa primária independente. Em termos operacionais, o aumento de pressão e a queda de vazão são coerentes com perda de injetividade por deposição de sais decorrente da incompatibilidade da mistura.

**dificil_B · REPROVADA: correcao_tecnica, suporte, sem_generalizacao**  
_Nota(s): Seleção da fonte de captação e projeto físico do sistema de água do mar para injeção em FPSOs; Ciclo operacional da filtração e retrolavagem do leito em sistemas de água do mar para injeção; Garantia hidráulica de vazão e pressão no sistema de água de injeção_

**P:** Uma unidade passou a ter ciclos de filtração mais curtos, mais retrolavagens e maior oscilação de vazão na sucção das bombas de injeção, com dificuldade para sustentar as cotas dos poços. Sem indício inicial de dano nas bombas, qual diagnóstico deve ser priorizado: limitação da filtração, limitação hidráulica de alimentação ou problema na fonte de captação? Justifique pela relação causal entre esses elementos.

**R:** A prioridade é verificar a fonte de captação como causa primária e tratar a filtração e a hidráulica como efeitos encadeados. Se a água captada chega com mais sólidos, turbidez ou maior variabilidade, aumenta a carga sobre o pré-tratamento. Nos filtros, isso encurta o ciclo de serviço, porque o leito retém partículas, se obstrui progressivamente e perde eficiência, exigindo retrolavagens mais frequentes. Essas transições tornam menos estável a disponibilidade de água tratada a montante do bombeio. A oscilação nas bombas passa então a ser manifestação hidráulica de uma perturbação originada antes, não necessariamente falha do bombeamento. Na etapa seguinte, deve-se confirmar se a reservação e o arranjo de estabilização estão conseguindo desacoplar essa variabilidade; se não estiverem, o sintoma hidráulico aparece com mais força, mas a origem continua sendo a piora da água na captação.

### Sistema de drenagem aberta e fechada

**facil · REPROVADA: escopo**  
_Nota(s): Filosofia de alarmes e intertravamentos de proteção em sistemas de drenagem/processo_

**P:** Qual é a diferença funcional entre um alarme operacional e um intertravamento ou sistema instrumentado de proteção em um sistema de drenagem/processo?

**R:** O alarme operacional serve para avisar que uma variável está se aproximando do limite de operação normal, dando ao operador oportunidade de corrigir o desvio antes que a condição de trip seja atingida. Já o intertravamento ou sistema instrumentado de proteção atua como camada de proteção automática quando a condição insegura é alcançada, sem depender de resposta manual do operador para sua operação normal.

**media · REPROVADA: escopo**  
_Nota(s): Filosofia de alarmes e intertravamentos de proteção em sistemas de drenagem/processo_

**P:** Durante a operação, um override de proteção é aplicado em painel remoto ou HMI sem conhecimento da sala de controle e sem autorização ou avaliação prévia. Qual risco operacional isso cria?

**R:** Isso cria risco por degradação não controlada da função de proteção, porque o override pode deixar a proteção indisponível ou alterada sem que a condição seja conhecida e gerida pela sala de controle. Sem conhecimento operacional, autorização e avaliação apropriada, a instalação passa a operar com a barreira comprometida fora de controle e sem critério definido.

**dificil_A · APROVADA**  
_Nota(s): Arranjo do sistema de drenagem aberta e fechada e gestão de integridade de linhas internas a tanques, headers e vasos de drenagem_

**P:** Durante um descomissionamento parcial, um trecho de drenagem aberta e uma linha overboard foram retirados da operação normal, mas a segregação definitiva ainda não foi concluída. A equipe propõe removê-los do plano de inspeção e tratar o isolamento existente como suficiente até a próxima parada. Tecnicamente, por que essa decisão é inadequada?

**R:** Porque, sem segregação definitiva, esses trechos ainda podem permanecer hidraulicamente conectados a tanques, convés ou mar e continuar relevantes para o risco. Nessa condição, a integridade mecânica das linhas internas a tanques e das interligações associadas deve seguir sendo considerada na gestão de mudanças e nas análises de risco, pois uma falha pode criar retorno de gás ao convés, transferência de carga entre tanques ou vazamento de óleo para o mar. Por isso, linhas inoperantes não devem ser tratadas como neutras apenas por estarem fora da operação normal. Elas precisam permanecer sob rotina de inspeções e manutenções, e o descomissionamento deve manter isolamento e bloqueios adequados até a segregação definitiva eliminar essas comunicações indesejadas.

**dificil_B · APROVADA**  
_Nota(s): Planejamento e governança dos testes de comissionamento em sistemas de drenagem aberta e fechada; Limpeza, flushing, drenagem, teste de estanqueidade e preservação de linhas e vasos de drenagem antes da entrada em serviço; Inspeção e limpeza de selos e pontos de bloqueio em sistemas de drenagem aberta e fechada_

**P:** Nos primeiros dias após o start-up de um sistema de drenagem aberta e fechada, surgem escoamento irregular, intervenções locais para desobstrução e suspeita de perda de segregação em dispositivos com selo líquido. O sistema havia sido liberado após flushing com água e ficou alguns dias vazio; além disso, há divergência entre equipes sobre a versão do procedimento usada na liberação. Tecnicamente, qual origem deve ser priorizada no diagnóstico: falha de manutenção rotineira ou desvio de comissionamento/preparação, e por quê?

**R:** Deve-se priorizar desvio de comissionamento/preparação. O problema apareceu nos primeiros dias de operação, fase em que ainda se confirmam processo e transição para o serviço; nesse contexto, falhas de cobertura dos testes ou de transição são causa provável. A divergência entre equipes sobre a versão do procedimento reforça deficiência de controle documental, compatível com liberação inadequada. Como houve flushing com água e o sistema ficou vazio por alguns dias, o diagnóstico deve verificar se a água foi drenada pelos pontos baixos, se houve remoção de residual com ar seco e se foi feita preservação com ar seco ou nitrogênio. Em paralelo, é necessário inspecionar integridade dos selos líquidos e presença de detritos em drenos, valas e headers. Esses achados podem parecer falha rotineira, mas também podem ter sido introduzidos pela preparação física incompleta antes da entrada em serviço.

### Tratamento de água produzida para descarte

**facil · APROVADA**  
_Nota(s): Separação primária gravitacional e condicionamento inicial da água produzida em FPSO_

**P:** Qual é o papel dos tanques de slop no tratamento da água de produção em um FPSO?

**R:** Receber a água de produção como parte do sistema de tratamento, funcionando como etapa inicial para seu condicionamento antes do descarte. Em FPSO, um ou dois tanques originais do navio podem ser dedicados a essa função.

**media · APROVADA**  
_Nota(s): Separação primária gravitacional e condicionamento inicial da água produzida em FPSO_

**P:** Em um FPSO, a equipe avalia aumentar o volume efetivo de decantação e o tempo de repouso da água produzida nos tanques. Que efeito isso tende a ter sobre a separação gravitacional inicial e qual limite operacional permanece?

**R:** Tende a aumentar a eficiência da separação gravitacional inicial, porque maiores dimensões de tanque e maior tempo de repouso favorecem a decantação. Ainda assim, a água ao final dessa etapa pode permanecer com elevada concentração de hidrocarbonetos, o que mantém a necessidade de tratamento adicional antes do descarte.

**dificil_A · APROVADA**  
_Nota(s): Hidrociclones no tratamento de água produzida para intensificação da separação óleo-água_

**P:** A água descartada após os hidrociclones piorou. Ao mesmo tempo, a água que sai dos separadores passou a chegar a esse estágio com teor de óleo disperso acima de 1000 mg/L, enquanto a alimentação dos hidrociclones permaneceu tangencial e pressurizada, sem indício de perda desse padrão. Pela lógica do trem de tratamento, qual é a causa mais provável: sobrecarga por arraste de óleo a montante ou perda das condições de separação no próprio hidrociclone?

**R:** A causa mais provável é sobrecarga por arraste de óleo a montante. Nesse trem, a corrente que sai dos separadores deve chegar ao estágio de hidrociclones e flotação com no máximo 1000 mg/L de óleo disperso. Se esse valor é ultrapassado, a interpretação correta é que houve deficiência anterior no trem, com mais óleo sendo arrastado para o tratamento de água. Como os hidrociclones ainda estão recebendo a corrente de forma tangencial e sob pressão, o mecanismo básico de separação centrífuga continua disponível: a fase aquosa mais densa tende a ir para a periferia e a fase oleosa para a região interna, saindo por vias distintas. Nessas condições, a piora da água tratada aponta mais para excesso de carga de óleo recebido do que para perda intrínseca do princípio de separação no equipamento.

**dificil_B · REPROVADA: suporte**  
_Nota(s): HAZOP como estrutura de diagnóstico de falhas no tratamento de água produzida; Falhas de medição e controle da interface óleo/água e seu efeito no arraste de óleo para a água produzida; Diagnóstico de ineficiência em equipamentos de tratamento da água produzida_

**P:** Uma planta de água produzida passou a exigir múltiplas passagens para enquadrar TOG e, em alguns períodos, a operação recorre a by-pass manual. Ao mesmo tempo, a interface óleo/água na separação primária é controlada por medidor em standpipe com resposta lenta e histórico de falta de manutenção. Como estruturar um HAZOP para diferenciar se a causa dominante é descontrole da interface a montante ou limitação do mecanismo dos equipamentos de tratamento a jusante, e qual hipótese deve ser verificada primeiro?

**R:** Divida a análise em dois nós: separação primária e tratamento da água produzida. Em cada nó, defina o comportamento esperado e aplique palavras-guia ao parâmetro relevante. Na separação primária, use a interface óleo/água e desvios como “mais”, “menos” ou “retardo”, ligando-os a arraste de óleo para a linha de água, aos sensores de interface e aos atuadores de controle. Como medição lenta, descalibrada e sem manutenção degrada simultaneamente o controle e o diagnóstico, essa hipótese deve ser verificada primeiro. No tratamento a jusante, analise desvios de desempenho como necessidade de múltiplas passagens, bloqueio com retrolavagem e by-pass manual, relacionando-os à forma do óleo no efluente e à limitação do mecanismo de separação. Se a carga de entrada já estiver deteriorada por arraste a montante, o sintoma a jusante pode ser efeito secundário, não causa primária.

### Tratamento do Gás produzido

**facil · APROVADA**  
_Nota(s): Desidratação do gás por glicóis e condicionamento para evitar hidratos, condensação e danos a jusante_

**P:** Qual é a função da desidratação do gás produzido e por que a remoção de água protege linhas e equipamentos a jusante contra condensação e danos?

**R:** A desidratação retira água da corrente de gás sob pressão para reduzir a formação de hidratos e evitar que a água condense em fase líquida ao longo do sistema. Essa remoção protege linhas e equipamentos a jusante porque a presença de água favorece condensação aquosa e deterioração dos equipamentos e tubulações. Em arranjos usuais, o gás que permanece na fase gasosa após compressão e resfriamento segue para secagem por glicol antes das etapas posteriores de tratamento.

**media · APROVADA**  
_Nota(s): Desidratação do gás por glicóis e condicionamento para evitar hidratos, condensação e danos a jusante_

**P:** Em uma instalação offshore, o gás será tratado para exportação sob condições posteriores de pressão e temperatura potencialmente severas. Como comparar a absorção com glicóis com outras tecnologias de desidratação, e em que situação a escolha tende a sair da absorção líquida mais comum?

**R:** Em sistemas offshore, a absorção com glicóis é frequente porque o uso de absorventes líquidos facilita a logística de manuseio. Ela é adequada para remover água do gás e controlar risco de hidratos, mas deixa teor de umidade maior do que tecnologias mais severas, como peneiras moleculares. A escolha tende a sair da absorção líquida mais comum quando as condições posteriores de pressão e temperatura exigem especificação de umidade mais restritiva, porque a seleção da tecnologia depende justamente do regime de pressão e temperatura a que o gás será submetido. Em condições menos severas, pode-se admitir especificação menos restritiva e manter alternativas diferentes das peneiras moleculares.

**dificil_A · APROVADA**  
_Nota(s): Modos operacionais A, B e C de plataformas com membranas de remoção de CO₂ e seus efeitos sobre exportação, injeção e gás combustível_

**P:** Em uma plataforma com remoção de CO₂ por membranas, a equipe enfrenta três condições ao longo da campanha: indisponibilidade total das membranas, operação plena e operação parcial. Para cada condição, como deve ficar o balanço entre exportação e injeção de gás? Na condição de indisponibilidade total, qual é a conclusão explicitamente sustentada sobre o gás enviado às turbinas?

**R:** Com indisponibilidade total das membranas, a unidade opera em modo A: a exportação fica impedida e todo o gás deve ser direcionado para injeção. Com operação plena, opera em modo B: a remoção de CO₂ permite exportação máxima de gás. Com operação parcial, opera em modo C: a plataforma combina exportação parcial com injeção parcial. No modo A, como não existe parcela de gás tratada pelas membranas, o gás encaminhado às turbinas apresenta teor de CO₂ igual ao do fluido produzido nos poços.

**dificil_B · REPROVADA: suporte**  
_Nota(s): Desidratação e condicionamento do gás produzido para exportação ou reinjeção em FPSOs; Remoção de condensados no gás comprimido e proteção do sistema de compressão; Controle de líquido no gás a montante de peneiras moleculares: proteção do leito, desempenho de desidratação e confiabilidade da regeneração_

**P:** Após aumento de carga no trem de compressão, uma unidade de desidratação por peneiras moleculares passou a entregar gás mais úmido de forma abrupta. Há indicação de líquido a montante do adsorvedor, e a regeneração posterior não recupera o desempenho anterior. Qual diagnóstico é mais consistente e qual deve ser a prioridade técnica na investigação?

**R:** O diagnóstico mais consistente é entrada de condensado ou névoa líquida formada no próprio circuito de compressão com resfriamento entre estágios, atravessando a separação mecânica a montante do adsorvedor. O resfriamento entre estágios forma líquido que precisa ser removido antes que o gás siga adiante; esse fenômeno pode se repetir após cada resfriador, não apenas na sucção inicial. Se água líquida alcança a peneira molecular, o problema deixa de ser simples saturação normal do leito: pode ocorrer solubilização do ligante, formação de aglomerados na regeneração, perda de área superficial e má distribuição do fluxo. Por isso, a prioridade é verificar e restabelecer a retenção de líquidos antes do leito, especialmente nos pontos a jusante dos resfriadores e nos dispositivos de separação/coalescência a montante do adsorvedor, em vez de tratar o caso apenas como ajuste de regeneração.

## Segurança Operacional, SGSO, Sistemas de Segurança e Gestão de Riscos

### Estudos de Segurança

**facil · APROVADA**  
_Nota(s): Bow-Tie e premissas para classificar risco e avaliar a efetividade de barreiras em estudos de segurança_

**P:** No Bow-Tie, o que representa o lado esquerdo e o que representa o lado direito do diagrama em relação à árvore de falhas e à árvore de eventos?

**R:** O lado esquerdo corresponde à lógica da árvore de falhas, organizando como causas podem levar ao evento principal. O lado direito corresponde à lógica da árvore de eventos, mostrando como as consequências se desdobram a partir do evento principal.

**media · APROVADA**  
_Nota(s): Bow-Tie e premissas para classificar risco e avaliar a efetividade de barreiras em estudos de segurança_

**P:** Em um estudo, um cenário foi classificado pela pior consequência que pode ocorrer imediatamente após a liberação do perigo, e a frequência foi estimada assumindo barreiras disponíveis e operando como esperado. Como essa classificação deve ser interpretada se depois surgir evidência de deficiência em uma barreira creditada?

**R:** Essa classificação representa o risco do cenário sob a premissa de que as barreiras estavam disponíveis, adequadas e com o desempenho esperado. Se surge evidência de deficiência em uma barreira creditada, essa condição de base deixa de valer para o cenário afetado. Portanto, a classificação original não deve ser tomada como automaticamente válida para a condição real; o cenário precisa ser reavaliado com foco na barreira comprometida e no efeito dessa degradação sobre o risco.

**dificil_A · REPROVADA: correcao_tecnica, suporte, sem_generalizacao**  
_Nota(s): Revisão periódica, atualização e validade dos estudos de segurança de FPSOs ao longo do ciclo de vida_

**P:** Em um FPSO em operação, o gerenciamento de mudanças registrou uma alteração com impacto na planta de processo. Em paralelo, inspeções e dados de integridade indicam redução da vida remanescente por fadiga e corrosão em casco e topside. Antes de decidir se a Safety Case Review será aberta, que verificações e estudos adicionais devem ser feitos, e como essa decisão deve ser registrada no sistema de gestão?

**R:** A decisão deve ser subsidiada por duas frentes. Primeiro, verificar se as bases técnicas do safety case e dos demais estudos de risco ainda representam a configuração real, os equipamentos, os processos e as condições operacionais da unidade, incluindo se as premissas permanecem válidas e se o programa de integridade de ativos continua alinhado ao safety case. Segundo, avaliar o efeito da mudança e do envelhecimento sobre os perigos maiores, especialmente quando fadiga e corrosão alteram a vida remanescente de casco e topside. Se houver impacto, o sistema de gestão deve identificar, registrar e comunicar a mudança, acionar formalmente a Safety Case Review e, quando necessário, estudos adicionais como HAZID e HAZOP. A documentação deve evidenciar o critério usado para decidir, as premissas verificadas, os impactos identificados, os estudos complementares requeridos e o vínculo com a implementação das ações resultantes.

**dificil_B · APROVADA**  
_Nota(s): Identificação e seleção de perigos e cenários acidentais com HAZID, HAZOP, What-if e FMEA/FMECA; Construção de cenários acidentais para liberações inflamáveis em estudos de segurança offshore; QRA/FERA: estrutura do estudo, escopo e critérios para seleção metodológica_

**P:** Na atualização dos estudos de uma unidade offshore, a equipe decide manter apenas HAZID e What-if antigos porque os perigos principais já estavam listados. Agora, porém, precisa decidir se cenários de liberação inflamável em área congestionada justificam medidas adicionais de redução de risco. Esse conjunto é suficiente para sustentar a decisão? O que deve ser acrescentado para que a seleção dos cenários e a decisão sobre barreiras não fiquem distorcidas?

**R:** Não. HAZID e What-if podem sustentar a identificação inicial de perigos, mas, para decidir sobre cenários de liberação inflamável e medidas adicionais, a metodologia precisa ser explicitada conforme o tipo de perigo e a profundidade exigida pela decisão. Nesse caso, os cenários devem ser consolidados como hipóteses acidentais por árvores de eventos, encadeando liberação, dispersão, ignição e consequências. A plausibilidade do evento depende do tipo e das condições do vazamento, do tempo de ignição e do grau de confinamento; por isso, o estudo de dispersão é necessário para reduzir incertezas sobre o cenário mais provável. Se a decisão envolve comparar barreiras ou representar com maior realismo incêndio, explosão e possível escalonamento em área congestionada, a análise deve avançar para abordagem ao menos semiquantitativa e, quando se busca maior completude do comportamento do incêndio, quantitativa.

### Operações simultâneas – SIMOPS

**facil · APROVADA**  
_Nota(s): Governança de SIMOPS: papéis, cadeia de comando, reuniões e comunicação entre frentes_

**P:** Por que crews contratadas ou de construção devem ser alertadas, por meio de seus supervisores, sobre operações de produção, perfuração ou workover com as quais possam interagir inadvertidamente?

**R:** Porque essas crews podem não ter familiaridade suficiente com as operações offshore em curso e, sem esse alerta, podem interferir de forma não intencional em atividades de produção, perfuração ou workover. O alerta via supervisão serve para tornar visível qual operação pode ser afetada e quais interações precisam ser evitadas, reduzindo o risco de consequências graves decorrentes dessa interação inadvertida.

**media · APROVADA**  
_Nota(s): Governança de SIMOPS: papéis, cadeia de comando, reuniões e comunicação entre frentes_

**P:** Em um projeto com SIMOPS, a contratada troca parte da crew no fim do turno enquanto a operação principal continua sem mudança relevante. Como essas trocas podem degradar a coordenação, e por que a comunicação entre a supervisão do operador e da contratada deve ser mantida durante todo o projeto?

**R:** Mudanças de turno e de crew são pontos em que a informação sobre interações entre frentes pode se perder, ser transmitida de forma incompleta ou chegar distorcida. Isso degrada a continuidade do entendimento sobre quais atividades coexistem, com quais operações a contratada pode interagir e quem deve acionar ou ajustar o trabalho quando o contexto muda. Por isso, a comunicação entre a supervisão do operador e a da contratada deve permanecer clara e contínua durante todo o projeto, não só no início, para preservar esse entendimento ao longo das passagens de turno e reduzir a chance de que interações críticas deixem de ser percebidas a tempo.

**dificil_A · REPROVADA: suporte**  
_Nota(s): Condições anormais dinâmicas em SIMOPS: perda de posicionamento, perda de geração e transição para estado seguro_

**P:** Em uma SIMOPS com unidade conectada a infraestrutura submarina, duas condições anormais dinâmicas são discutidas no plano de resposta: no primeiro caso, forças ambientais em rápida piora elevam a carga dos propulsores, surgem deriva e desvio de rumo; no segundo, ocorre falha de energia principal. Em cada caso, qual função essencial deve ser preservada primeiro para levar a unidade a estado seguro, e qual ação operacional decorre dessa prioridade?

**R:** Se os sinais mostram aumento de carga nos propulsores, deriva e desvio de rumo, a função crítica em perda é a manutenção de posição. Nessa condição, a prioridade passa a ser evitar dano à infraestrutura submarina e à unidade, o que pode exigir iniciar a desconexão de emergência quando o posicionamento já não é mantido.

Se ocorre falha de energia principal, a função essencial a preservar primeiro é a estabilidade da unidade por meio da operabilidade do lastro. Para levar a unidade a estado seguro, devem permanecer disponíveis, a partir do quadro de emergência alimentado pelo gerador de emergência, uma ou mais bombas de lastro e o sistema completo de lastro, de modo a recuperar trim seguro e nivelado.

**dificil_B · APROVADA**  
_Nota(s): Matriz operações versus barreiras como base para compatibilidade e restrições operacionais em SIMOPS; SIMOPS: como bypasses, intertravamentos e lógicas automáticas podem degradar simultaneamente disponibilidade e independência das barreiras; Impacto de alarmes, detecção de gás, intertravamentos e ESD na continuidade de SIMOPS_

**P:** Duas frentes em SIMOPS foram liberadas como compatíveis pela matriz vigente. Durante a execução, ocorre alarme de gás na área, com atuação automática que altera a ventilação e começa a afetar painéis elétricos; ao mesmo tempo, descobre-se que um maintenance bypass aplicado para viabilizar startup atuava sobre um transmissor que executa PSH e PSL, desabilitando ambas as funções. A coordenação deve manter, restringir ou interromper as frentes? Justifique pelo efeito combinado sobre a compatibilidade.

**R:** Deve interromper ou, no mínimo, suspender as frentes até reavaliar a compatibilidade com a arquitetura real de barreiras. A matriz só sustenta a compatibilidade se estiver convergente com o estado efetivo das barreiras e atualizada para mudanças operacionais. Aqui, a premissa deixou de valer por dois motivos combinados: o bypass não retirou apenas a função de partida, mas também a proteção primária de pressão do mesmo transmissor, reduzindo disponibilidade e independência das proteções; e o alarme não foi só indicação, pois a lógica automática alterou a ventilação e passou a impactar painéis elétricos e sistemas dependentes. Assim, o evento ocorreu com menos camadas de defesa do que a matriz nominal presumiu. Antes de retomar SIMOPS, é preciso restabelecer ou controlar formalmente as barreiras degradadas e atualizar a base de compatibilidade para refletir o novo arranjo.

### Segurança e Controle de Riscos

**facil · APROVADA**  
_Nota(s): Controle de fontes de ignição e proteção de equipamentos em áreas classificadas_

**P:** Por que equipamentos elétricos e eletrônicos podem atuar como fontes de ignição em atmosferas explosivas em áreas classificadas?

**R:** Porque podem fornecer energia ou temperatura suficientes para inflamar gases ou vapores inflamáveis presentes. Isso ocorre por arcos e faíscas gerados no centelhamento de contatos, por superfícies aquecidas, e tanto em operação normal quanto em condição de falha. Em áreas classificadas, esses mecanismos tornam o equipamento uma fonte relevante de ignição se a atmosfera explosiva estiver presente.

**media · APROVADA**  
_Nota(s): Controle de fontes de ignição e proteção de equipamentos em áreas classificadas_

**P:** Em uma instalação elétrica localizada em área classificada, como dispositivos de alarme e seccionamento automático reduzem o risco de ignição quando surgem sobretensão, sobrecorrente, falha de isolamento ou aquecimento anormal?

**R:** Eles reduzem o risco ao detectar condições anormais de operação e atuar antes que essas condições evoluam para arco, faísca ou aquecimento capaz de inflamar a atmosfera. O alarme sinaliza a anomalia para intervenção, e o seccionamento automático interrompe a energia do circuito ou equipamento afetado. Assim, limitam a permanência de sobretensão, sobrecorrente, falha de isolamento e aquecimento anormal em equipamentos instalados em área classificada.

**dificil_A · REPROVADA: correcao_tecnica, suporte**  
_Nota(s): Investigação de incidentes com identificação de causas imediatas, básicas e sistêmicas_

**P:** Em uma manutenção com isolamento de linha em unidade offshore, ocorreu um quase acidente após liberação inesperada de fluido. A investigação encontrou não conformidades recorrentes nas auditorias de isolamento, ausência de revisão das válvulas travadas abertas/fechadas, supervisão deficiente em campo e avaliação de riscos que não refletia a prática real. A gerência pretende encerrar o caso com advertência ao executor, reciclagem rápida e reforço de assinaturas em formulários. Que ações corretivas e preventivas são mais coerentes com esse diagnóstico?

**R:** A resposta coerente é tratar a falha como problema de barreiras e de gestão, não só de execução individual. Devem ser corrigidas as disposições de isolamento para recuperar sua eficácia prática, incluindo um sistema de revisão das válvulas travadas abertas/fechadas e tratamento das não conformidades recorrentes. Também é necessário refazer a avaliação de riscos e o método de trabalho conforme a condição real de execução, porque a mudança do método após questionamento indica falha prévia de avaliação e de monitoramento. Além disso, a organização deve fortalecer como o trabalho é supervisionado e controlado em campo, verificando competência, planejamento e os controles usados na tarefa. Medidas apenas disciplinares ou documentais são insuficientes quando a investigação identificou causas imediatas, subjacentes e de gestão; as ações devem revisar o sistema, restaurar barreiras e melhorar monitoramento e conformidade operacional.

**dificil_B · APROVADA**  
_Nota(s): Lacunas de identificação de perigos por mudanças operacionais, interpretações locais e cenários não previstos; Gestão de mudanças, HRA e revisão de análises para condições não rotineiras; Avaliação de riscos em modos operacionais, transientes e condições anormais_

**P:** Após manutenção, um sistema retorna ao serviço em configuração temporária diferente da rotina. Durante a tarefa, a equipe identifica no campo um perigo relevante que não constava da análise usada para liberar o trabalho. A supervisão deve tratar isso principalmente como falha pontual de execução ou como evidência de falha mais ampla no processo de gestão de riscos, e qual providência técnica deve priorizar antes de continuar?

**R:** Deve tratar principalmente como evidência de falha mais ampla no processo de gestão de riscos. Quando um perigo relevante só é reconhecido durante a execução, isso indica que a identificação de perigos não representou a condição real da operação. Em retorno ao serviço e outras transições, a planta sai da base rotineira; essa condição pode alterar barreiras, ações humanas críticas e limites operacionais, exigindo gestão de mudanças e reavaliação das análises aplicáveis antes da continuidade. A prioridade é interromper a continuidade baseada na análise insuficiente e revisar formalmente a condição operacional: descrever e justificar a mudança, reavaliar os perigos da transição, verificar se a atividade é crítica a ponto de exigir HRA e restabelecer os controles de retorno ao serviço compatíveis com a condição real, como PTW e certificados de isolamento.

### SGSO

**facil · APROVADA**  
_Nota(s): Planejamento do Plano de Emergência integrado à gestão de riscos e aos cenários acidentais_

**P:** Quais elementos mínimos o Plano de Emergência da instalação deve contemplar para estruturar a resposta a cenários acidentais?

**R:** Deve contemplar: identificação da instalação e do responsável legal; descrição dos acessos; cenários acidentais; sistemas de alerta; comunicação do acidente; estrutura organizacional de resposta; procedimentos de resposta; equipamentos e materiais de resposta; e procedimento para acionamento de recursos e estruturas de resposta complementares, quando aplicável.

**media · APROVADA**  
_Nota(s): Planejamento do Plano de Emergência integrado à gestão de riscos e aos cenários acidentais_

**P:** Na elaboração do Plano de Emergência de uma unidade, a equipe discute dois cenários: liberação de material perigoso com necessidade de isolamento e controle de vazamento, e vazamento de óleo. Qual deles deve permanecer tratado no Plano de Emergência da instalação e qual pode ser tratado somente em plano específico?

**R:** O cenário de liberação de material perigoso com necessidade de isolamento e controle de vazamento deve permanecer tratado no Plano de Emergência da instalação, com ações específicas para esse tipo de resposta. Já o cenário de vazamento de óleo pode ser tratado somente em plano de emergência específico aplicável, em vez de permanecer no plano geral da instalação.

**dificil_A · APROVADA**  
_Nota(s): Identificação, classificação e governança dos Elementos Críticos de Segurança Operacional no SGSO_

**P:** Em um FPSO, auditorias sucessivas de SGSO voltam a registrar desvios ligados a elementos críticos, mesmo após correções locais apontadas como concluídas pelas áreas operacionais. Parte dos desvios envolve salvaguardas que não estavam claramente tratadas como críticas no sistema de gestão. Por que esse quadro pode caracterizar falha sistêmica na identificação ou no tratamento dos ECSO, e não apenas falhas isoladas de execução local?

**R:** Porque a repetição de desvios após ações corretivas indica que o tratamento anterior não eliminou a causa de gestão, apenas corrigiu manifestações locais. Quando isso ocorre em elementos críticos, o problema deixa de ser pontual e passa a sugerir insuficiência de abrangência no tratamento dado pelo operador. Se, além disso, há salvaguardas relevantes sem identificação ou classificação consistente como ECSO, a organização tende a monitorar e gerir apenas parte das barreiras críticas. Isso compromete a visão sobre disponibilidade e integridade dessas salvaguardas e revela inconsistência estrutural na definição do que é barreira crítica no SGSO. Nessa condição, a recorrência não é explicada apenas por execução local deficiente, mas por falha sistêmica na identificação dos elementos críticos e/ou na eficácia do tratamento gerencial dos desvios.

**dificil_B · APROVADA**  
_Nota(s): Capacitação, mudanças organizacionais e gestão de contratadas no SGSO em FPSOs; Gestão de mudanças de pessoas e capacitação para mudanças operacionais no SGSO; SGSO: efetividade de procedimentos operacionais depende de controle documental, recursos, treinamento e garantia da qualidade na execução_

**P:** Após uma reorganização com entrada de pessoal, acúmulo temporário de funções e uso de contratadas em manutenção, os procedimentos da área seguem atuais e acessíveis no sistema. Em campo, ocupantes do mesmo cargo executam a rotina com diferenças em etapas críticas, e os registros mostram apenas treinamentos anteriores, sem evidência específica da transição. Qual é o diagnóstico técnico mais consistente e qual controle deve ser priorizado para restabelecer a efetividade da barreira procedimental?

**R:** O diagnóstico mais consistente é barreira procedimental formalmente disponível, porém degradada por falha de gestão de mudanças de pessoas e de capacitação por função. A mudança de pessoas e o acúmulo de funções alteram a competência disponível e exigem tratamento formal, inclusive para entradas de pessoal. Se a transição não foi acompanhada por capacitação teórica e prática, reciclagem, tutoria prévia para novos integrantes e verificação de entendimento das implicações operacionais, o procedimento pode permanecer vigente no sistema sem ser executado de forma uniforme. A prioridade é aplicar o gerenciamento de mudanças de pessoas à reorganização e reconverter a execução do procedimento em requisito controlado: requisitos mínimos por cargo com avaliação teórica e prática, treinamento nos procedimentos aplicáveis à nova condição, revisão com as equipes de operação e manutenção sobre as implicações da mudança e, para contratadas, evidência de treinamento adequado e acompanhamento por indicadores.

### Sistema de Combate a Incêndio

**facil · APROVADA**  
_Nota(s): Barreiras passivas, divisórias e compartimentação corta-fogo_

**P:** Em proteção passiva contra incêndio por barreiras, qual solução oferece maior nível relativo de proteção: parede ou divisória?

**R:** A parede oferece maior nível relativo de proteção contra incêndio do que a divisória.

**media · APROVADA**  
_Nota(s): Barreiras passivas, divisórias e compartimentação corta-fogo_

**P:** Ao definir o tipo, a localização e o projeto de uma barreira resistente ao fogo entre áreas com ocupações e perigos distintos, quais variáveis do cenário e da geometria da área protegida devem ser consideradas?

**R:** Devem ser considerados o tipo e a severidade do incêndio, além do tamanho e da configuração da área a ser protegida. Esses fatores condicionam a escolha do tipo de barreira, sua localização e seu projeto.

**dificil_A · APROVADA**  
_Nota(s): Gestão de inspeção, manutenção e tratamento de desvios em sistemas de combate a incêndio no SGSO_

**P:** Em uma unidade offshore, uma bomba do sistema de combate a incêndio, classificada como elemento crítico, não atende aos critérios de vazão e pressão em teste periódico. A operação pretende mantê-la nessa condição até a próxima janela de manutenção, alegando que o sistema continua parcialmente disponível. No SGSO, quais decisões de controle precisam existir para essa permanência ser tecnicamente controlada, e o que caracteriza falha de gestão do risco residual nesse caso?

**R:** O resultado do teste deve ser tratado como desvio conclusivo de desempenho, com emissão de ordem de manutenção corretiva priorizada conforme a gravidade do desvio e a criticidade do elemento degradado. Se a operação for mantida antes do reparo, isso não pode ficar apenas como pendência de manutenção: devem existir procedimentos de contingência formalmente estabelecidos, com aprovação e controle, incluindo medidas temporárias equivalentes quando aplicável. A decisão de permanência em serviço depende, portanto, de duas frentes simultâneas: correção priorizada do elemento que falhou no teste e contingência aprovada para controlar a perda parcial da função. Há falha de gestão do risco residual quando o sistema permanece indisponível ou degradado sem contingência adequada e controlada, porque nessa condição a capacidade de resposta a incêndio fica comprometida.

**dificil_B · APROVADA**  
_Nota(s): Integração entre detecção de fogo e gás, SIS/ESD, supressão e HVAC nas ações automáticas de emergência; Disponibilidade real do sistema de combate a incêndio e robustez das funções de emergência associadas; Resiliência do sistema de combate a incêndio quando o próprio evento degrada o sistema_

**P:** Durante um incêndio, os alarmes e as ações automáticas previstas ocorrem: shutdown de emergência, isolamento de processo e comando de supressão/ventilação. Mesmo assim, a mitigação fica abaixo do esperado, com baixa efetividade do combate e parte da resposta física não se sustentando. Qual diagnóstico deve ser priorizado: erro da lógica de emergência ou perda de disponibilidade/resiliência da infraestrutura acionada? Justifique pelo encadeamento técnico mais provável.

**R:** Deve-se priorizar a hipótese de perda de disponibilidade/resiliência da infraestrutura acionada. Se a detecção disparou as ações automáticas coerentes com a matriz de causa e efeito, isso indica que a cadeia sensor–lógica–atuadores de comando foi ao menos iniciada corretamente. A degradação restante pode estar na parte que materializa a resposta: partida de bombas, alimentação elétrica, caminhos hidráulicos e contingências. Em emergência, o sistema pode ficar parcial ou totalmente ineficaz por dano inicial do próprio evento ou por defeitos latentes. Um incêndio pode inutilizar seletivamente meios elétricos de combate, exigindo uso de alternativas com diversidade de energia e até acionamento manual. Também é preciso verificar se as bombas respondem aos diferentes iniciadores previstos, porque a perda de função integrada pode estar na interface entre demanda e partida, não na lógica principal de ESD/supressão.

### Sistema de Fogo e Gás (F&G)

**facil · APROVADA**  
_Nota(s): Proof tests, testes parciais e inspeções associadas às SIF/F&G_

**P:** Por que a frequência de proof test de uma SIF não deve ser definida apenas por conveniência operacional?

**R:** Porque a periodicidade precisa ser a definida no SRS e usada na verificação de SIL, além de ser exequível nas restrições operacionais vigentes. Se a frequência for escolhida só por conveniência de manutenção, ela pode deixar de representar a base considerada para demonstrar a integridade da função. Em funções com componentes testados em momentos diferentes, as frequências de cada parte também precisam estar definidas no SRS e sustentar o cálculo de verificação de SIL.

**media · APROVADA**  
_Nota(s): Proof tests, testes parciais e inspeções associadas às SIF/F&G_

**P:** Em uma SIF cujo proof test completo foi dividido entre operação normal e shutdown planejado, quais verificações de inspeção devem acompanhar o proof test ou partial proof test para identificar modificação não autorizada e deterioração do equipamento instalado?

**R:** A inspeção deve confirmar que o equipamento instalado continua conforme o SRS, sem modificações não autorizadas e sem deterioração que comprometa sua função. Para isso, o procedimento deve identificar os instrumentos e os equipamentos associados a inspecionar, incluindo tubing de instrumentação, caixas de junção e trace heating. Também deve verificar a configuração instalada, como confirmação de números de série, e sinais de deterioração física, como ausência de parafusos ou tampas, suportes com corrosão e danos em cabos.

**dificil_A · REPROVADA: correcao_tecnica, suporte, sem_generalizacao**  
_Nota(s): Estratégias combinadas de manutenção, calibração e verificação de desempenho em sistemas F&G_

**P:** Durante a operação, um elemento crítico do sistema F&G fica degradado e parte da sua função de proteção deixa de estar disponível. A equipe pretende manter a unidade operando com crédito nas barreiras remanescentes até o reparo. Qual decisão técnica é a mais robusta para manter o risco controlado nessa condição?

**R:** Manter a operação só é tecnicamente defensável se o crédito nas barreiras remanescentes vier acompanhado da verificação de que os requisitos de inspeção continuam atendidos e da adoção de medidas temporárias compatíveis com o risco da perda parcial da função. Isso exige tratar o item como Elemento Crítico de Segurança Operacional dentro de um programa diferenciado de inspeção, manutenção e calibração, registrar e acompanhar o desempenho em tendência para não migrar para gestão reativa da falha e usar as informações dos estudos de segurança no sistema de gerenciamento para definir as compensações aplicáveis. Se essas condições não puderem ser asseguradas, o controle do risco passa por restringir a operação, isolar a condição ou parar a atividade afetada.

**dificil_B · REPROVADA: suporte, sem_generalizacao**  
_Nota(s): Sistema F&G: desempenho intrínseco do sensor, calibração e influência ambiental na detecção de gás inflamável; Interferência de umidade, vapor d’água, névoa/óleo e gases atmosféricos na resposta e na calibração de detectores de F&G; Calibração, aferição, ajuste, deriva e monitoramento de condição em detectores e instrumentos de F&G_

**P:** Em uma área com potencial de acúmulo de gás inflamável, um detector de estado sólido passou a oscilar e a aparentar perda de sensibilidade em dias com alta umidade, variação térmica e presença intermitente de névoa. A equipe discute trocar o sensor, recalibrar imediatamente ou manter observação. Qual deve ser a prioridade diagnóstica e como distinguir interferência ambiental de deriva real do detector antes de decidir ajuste ou substituição?

**R:** A prioridade é investigar primeiro a correlação da instabilidade com o ambiente e confrontá-la com o histórico metrológico do detector, antes de ajustar ou substituir. Em sensores de estado sólido, umidade e temperatura alteram a adsorção na superfície sensível e podem mudar a resposta para a mesma concentração. Em presença de névoa, a sensibilidade pode variar e a calibração associada tem alta incerteza, reduzindo a confiança em interpretar a oscilação como defeito. Para separar isso de deriva real, a verificação deve comparar o desempenho com padrão usando o mesmo gás de referência no início e no fim do intervalo de ajuste e registrar a tendência ao longo do tempo. Se a variação acompanhar as condições ambientais, sem tendência consistente contra o padrão, não há base para concluir defeito eletrônico nem para recalibração imediata. Se houver desvio recorrente ou anormal frente ao padrão, aí cabe ajuste e, se o comportamento fugir do esperado, investigação de reparo.

### Sistemas e equipamentos de salvatagem

**facil · APROVADA**  
_Nota(s): Pontos de reunião e interfaces com o refúgio temporário na resposta a emergências_

**P:** O que significa estruturar a resposta a emergências com pontos de encontro distribuídos por função e localização na unidade?

**R:** Significa que a apresentação inicial do pessoal não é concentrada em um único local genérico. A resposta é organizada com pontos de encontro previamente definidos para funções diferentes, em locais distintos da unidade, como comando, atendimento, áreas técnicas, recursos de resposta e refúgio temporário. Assim, cada grupo se dirige ao ponto correspondente à sua função e posição prevista na estrutura de emergência.

**media · APROVADA**  
_Nota(s): Pontos de reunião e interfaces com o refúgio temporário na resposta a emergências_

**P:** Em uma emergência, a unidade já possui locais de apresentação previamente definidos para cada função em diferentes áreas, em vez de reunir todos no mesmo ponto. Como essa definição tende a influenciar a organização inicial da resposta, a concentração de equipes e a contabilização de pessoal?

**R:** Ela tende a organizar a resposta desde o início, porque cada função já tem um local esperado de apresentação. Isso evita reunir todo o pessoal em um único ponto, distribuindo as equipes conforme sua função e sua posição na estrutura de emergência. Também favorece a contabilização por grupos e locais previamente definidos, porque a verificação passa a ser feita onde cada função deve se apresentar.

**dificil_A · REPROVADA: suporte**  
_Nota(s): Condições de acesso, descida ao mar e lançamento seguro de life rafts_

**P:** Em um abandono noturno, a rota até a estação de life raft permanece fisicamente desobstruída e a balsa throw-over está a bordo. Porém, o único meio de descer ao nível do mar é uma rede de escalada, o acesso à painter line só seria possível já dentro d’água, e o ponto de lançamento fica sujeito a radiação térmica e fumaça sem proteção dedicada. A estação tem iluminação de emergência, mas o trecho final da rota pode perder visibilidade se a iluminação normal falhar. Esse arranjo torna a cadeia acesso–descida–alcance da balsa–embarque realmente viável?

**R:** Não. A cadeia falha em mais de uma etapa crítica. A rede de escalada não caracteriza meio controlado de descida, porque depende de força e destreza sob emergência. Além disso, se a pessoa só consegue alcançar a painter line após entrar na água, o arranjo passa a depender da entrada física no mar como etapa prática do acesso à balsa, e isso deve ser tratado como último recurso, não como solução normal de abandono. O ponto de lançamento e embarque também não atende ao critério de viabilidade se permanece exposto à radiação térmica, e a rota final não pode ser considerada disponível se pode perder condições de uso por fumaça ou falha de iluminação sem proteção ou iluminação adequada. Ter rota física e balsa disponível não basta; o abandono só é executável quando acesso, descida, conexão com a balsa e lançamento/embarque permanecem utilizáveis nas condições do cenário.

**dificil_B · REPROVADA: suporte**  
_Nota(s): Redundância e disponibilidade de rotas para escape-to-sea; Dependência do refúgio temporário quando o abandono é degradado; Proteção e disponibilidade de rotas de fuga, pontos de embarque e Temporary Refuge em cenários de incêndio, fumaça e explosão_

**P:** Após a indisponibilidade de um meio de evacuação, uma área da unidade passa a depender de rota alternativa até o escape-to-sea. Essa rota cruza zona com potencial de fumaça e radiação térmica, e o abandono pode atrasar, aumentando o tempo de permanência no Temporary Refuge (TR). Qual critério técnico deve orientar a decisão sobre a aceitabilidade dessa condição degradada?

**R:** A condição só é aceitável se a degradação não romper a cadeia completa de abandono. Isso exige verificar, primeiro, se ainda existe rota segura e efetivamente disponível até o escape-to-sea, sem dependência de um único percurso vulnerável; segundo, se a rota remanescente e os pontos de embarque permanecem utilizáveis pelo tempo requerido sob fumaça e radiação térmica; e, terceiro, se o TR suporta a maior permanência com habitabilidade preservada. Nessa verificação, o TR não pode ser tratado apenas como compartimento existente: sua proteção contra sobrepressão, suas condições atmosféricas internas admissíveis e a confiabilidade de detecção de fumaça, gás e funções de desligamento precisam sustentar permanência segura. Se a perda do meio de evacuação transfere a proteção para um TR degradado ou para rota que não sobreviva ao cenário, a condição não é aceitável.

## Utilidades, geração de energia e sistemas auxiliares

### Geração e distribuição de energia elétrica

**facil · APROVADA**  
_Nota(s): PMS/EMS como supervisão integrada da geração, sincronismo e partilha de carga_

**P:** Qual é a função do PMS em uma rede elétrica com múltiplos geradores conectados a um mesmo barramento?

**R:** O PMS supervisiona em tempo real o estado da rede elétrica e coordena a operação da geração. Para isso, acompanha variáveis como tensão, corrente e fator de potência, recebe informações de medição, proteção e controle, comanda a partida e a conexão de geradores ao barramento, realiza a partilha de carga entre as unidades e controla ou monitora frequência e sincronismo. Essa integração permite atuar sobre a geração para prevenir sobrecargas e sustentar a continuidade do fornecimento.

**media · APROVADA**  
_Nota(s): PMS/EMS como supervisão integrada da geração, sincronismo e partilha de carga_

**P:** Em uma instalação offshore com vários geradores no mesmo barramento, por que a aquisição contínua de tensões, correntes e fator de potência é importante para decidir a conexão de outro gerador e ajustar a partilha de carga?

**R:** Porque essas variáveis mostram, em tempo real, a condição elétrica da rede e a evolução da demanda. Com essa visibilidade contínua, o PMS identifica aproximação de sobrecarga ou mudanças de carga, especialmente em regimes com demanda variável, e pode comandar a partida e a conexão de outro gerador ao barramento sob supervisão de frequência e sincronismo. Depois disso, usa o mesmo acompanhamento para redistribuir a carga entre as unidades em operação. Sem essa aquisição contínua, a decisão de acrescentar geração e ajustar a partilha perde base operacional.

**dificil_A · APROVADA**  
_Nota(s): Arranjos de partida de unidades geradoras e automação da lógica de partida_

**P:** Em uma unidade com múltiplos geradores, um dos arranjos de partida permite tanto partir apenas o gerador para operar como compensador síncrono quanto partir a unidade completa para gerar potência ativa. Esse arranjo passou a apresentar problemas operacionais frequentes, reduzindo a confiabilidade das unidades. A equipe propõe substituí-lo por um Conversor Estático de Frequência (SFC) e integrar a partida à lógica automática do sistema. Por que essa substituição é tecnicamente justificável nesse contexto?

**R:** Porque o arranjo com falhas recorrentes compromete a confiabilidade justamente em uma função crítica: colocar o gerador ou a unidade completa em serviço no modo requerido. Quando o mesmo meio de partida atende mais de uma necessidade operacional, seus problemas afetam a disponibilidade da unidade em diferentes condições de operação. A substituição por um SFC é justificável porque ela elimina o arranjo que vinha apresentando recorrência de problemas e, ao mesmo tempo, transforma a partida em um processo totalmente automatizado. Com isso, a sequência de partida deixa de depender do desempenho do arranjo problemático e passa a ser executada de forma automática, coerente com a existência de uma unidade de controle automática para comandar a partida de todos os geradores.

**dificil_B · APROVADA**  
_Nota(s): Filosofia de geração principal, emergência e realimentação do quadro principal; Continuidade de alimentação de cargas essenciais e reconfiguração em contingências elétricas; Redundância e reconfiguração da distribuição para sustentar consumidores essenciais e de controle_

**P:** Após perda da geração principal, a geração de emergência está disponível e as permissivas para back feeding foram atendidas, energizando parte do painel principal. Ao mesmo tempo, um dos dois sistemas de 24 Vcc que alimentam CLP e painéis de controle falhou, e o TIE ainda não foi fechado. Há barramento em CA disponível, mas parte das funções de controle prioritárias continua indisponível. Qual reconfiguração deve ser priorizada para restabelecer essas funções, e por que o back feeding, isoladamente, não resolve o problema?

**R:** Deve-se priorizar a transferência dos consumidores de 24 Vcc para o conjunto remanescente pelo disjuntor TIE. O back feeding recompõe alimentação em CA para sistemas ligados ao painel principal, mas não substitui a alimentação dos circuitos de controle em corrente contínua. CLP e painéis de controle dos geradores dependem dos sistemas independentes de 24 Vcc, e cada conjunto tem capacidade para suprir sozinho 100% da demanda desse quadro. Portanto, se um trem de 24 Vcc falha, a continuidade dessas cargas prioritárias depende da interligação ao trem remanescente. O back feeding só atende a parcela do sistema ligada ao painel principal e, mesmo quando válido, não restabelece por si só consumidores cujo caminho funcional de alimentação é o sistema auxiliar em 24 Vcc.

### Sistema de utilidades

**facil · APROVADA**  
_Nota(s): Gestão energética e hídrica baseada em M&V e indicadores em sistemas de utilidades_

**P:** Por que a confiabilidade dos dados de medição em um sistema de utilidades depende de inspeção e calibração periódica, e como isso afeta a avaliação de desempenho?

**R:** Porque a confiabilidade dos dados só é assegurada quando os equipamentos de medição passam por inspeções e calibrações periódicas. Sem essa manutenção metrológica, o uso dos dados fica condicionado, e a avaliação do desempenho energético deixa de ter base confiável. Como a caracterização rigorosa do desempenho depende de medição e verificação, dados não confiáveis comprometem a gestão, o monitoramento e o reporte do consumo.

**media · APROVADA**  
_Nota(s): Gestão energética e hídrica baseada em M&V e indicadores em sistemas de utilidades_

**P:** Uma unidade de utilidades quer reduzir consumo de água e energia, mas ainda não mapeou claramente seus principais consumidores, as quantidades e qualidades requeridas em cada aplicação nem os pontos de geração de efluentes. Como essa lacuna afeta a identificação de oportunidades de otimização?

**R:** Essa lacuna dificulta identificar oportunidades de adequação do uso de água e energia, porque o conhecimento das atividades industriais é o que permite localizar os principais pontos de consumo, entender a quantidade e a qualidade exigidas em cada aplicação e reconhecer onde os efluentes são gerados. Sem essa visão, fica prejudicada a escolha de estratégias aderentes ao perfil de operação dos equipamentos e, portanto, a implementação de medidas de eficientização em utilidades.

**dificil_A · APROVADA**  
_Nota(s): Falhas em utilidades térmicas e de resfriamento: segregação de circuitos e consequências da perda de circulação_

**P:** Durante o retorno de um sistema de transferência de calor em fase líquida, a válvula do queimador principal permanece aberta enquanto as bombas de circulação não entram em operação. Ao mesmo tempo, a temperatura medida imediatamente a jusante da câmara de combustão começa a subir rapidamente. Qual condição perigosa deve ser diagnosticada nessa situação e qual é o encadeamento físico mais provável até um evento de fogo?

**R:** Deve ser diagnosticada a operação do queimador sem circulação efetiva do fluido. Nessa condição, o calor continua sendo imposto ao fluido na região aquecida, mas não é removido pelo escoamento. O resultado provável é superaquecimento local do fluido, seguido de expansão térmica e aumento rápido de pressão no circuito. Se essa pressão exceder a capacidade mecânica do tanque de expansão, pode ocorrer ruptura, com perda de contenção do fluido aquecido. Uma vez extravasado sobre o aquecedor e áreas adjacentes, o fluido pode inflamar pouco depois. A elevação rápida de temperatura logo após a câmara de combustão é um sinal compatível com essa evolução anormal e precisa ser acompanhada continuamente nessa posição.

**dificil_B · APROVADA · corrigida**  
_Nota(s): Segurança operacional em sistemas de heating medium em fase líquida: superaquecimento por perda de circulação, sobrepressão e salvaguardas; Intertravamentos e sistemas de proteção para desligamento seguro em turbinas, compressores e utilidades; Falhas em utilidades térmicas e de resfriamento: segregação de circuitos e consequências da perda de circulação_

**P:** Na partida de um sistema de heating medium em fase líquida, o queimador principal recebe combustível enquanto as bombas de circulação não estão operando. A equipe trata isso como perda parcial de utilidade, mas a temperatura a jusante da câmara de combustão e a pressão sobem rapidamente. Qual é o diagnóstico correto sobre a natureza da falha e quais barreiras deveriam atuar, em sequência, para evitar perda de contenção e incêndio?

**R:** O diagnóstico correto é que não se trata apenas de indisponibilidade de utilidade: a perda de circulação com fonte térmica ativa transforma a falha em evento de integridade mecânica e incêndio. Isso indica falha da camada de proteção/intertravamento, cuja função é preservar a integridade mesmo quando a anomalia venha de outro subsistema. A primeira barreira deveria impedir a operação da válvula de combustível do queimador quando as bombas de circulação não estivessem operando. Se essa prevenção falhar, a segunda barreira é o monitoramento contínuo da temperatura imediatamente a jusante da câmara de combustão. A terceira é a limitação das consequências por tanque de expansão com classificação de pressão adequada e válvula de alívio secundária de grande capacidade. Sem isso, ocorre superaquecimento, sobrepressão, ruptura e possível ignição.

## Descomissionamento e Gestão do Ciclo de Vida da Unidade

### Geral

**facil · APROVADA**  
_Nota(s): Estratégia de ciclo de vida, extensão de vida e preparação para descomissionamento em unidades flutuantes_

**P:** Por que a gestão do ciclo de vida de uma unidade flutuante deve começar na fase de projeto, e não apenas na operação ou perto do descomissionamento?

**R:** Porque decisões tomadas no projeto já podem reduzir impactos ambientais, sociais e de saúde e segurança do descomissionamento, além de fazê-lo com menor custo, por meio de medidas preventivas como melhor posicionamento de componentes, prevenção de interferência com áreas sensíveis e provisão de garantias financeiras. Além disso, o gerenciamento de riscos deve começar no projeto, com antecipação e identificação de desvios, condições inseguras e falhas combinadas de camadas de proteção, seguindo depois por planejamento, execução, controle e análise crítica até a desativação. Tratar o ciclo de vida desde o nascimento do ativo evita que descomissionamento e demais decisões finais sejam conduzidos de forma reativa e sem preparação prévia.

**media · APROVADA**  
_Nota(s): Estratégia de ciclo de vida, extensão de vida e preparação para descomissionamento em unidades flutuantes_

**P:** Uma unidade flutuante se aproxima da vida de projeto, mas a organização só então inicia discussões sobre extensão de vida com base em achados dispersos de auditoria e correções pontuais de envelhecimento. Por que essa abordagem é inadequada e o que deve sustentar tecnicamente a decisão?

**R:** Essa abordagem é inadequada porque extensão de vida não deve começar apenas quando a vida de projeto se aproxima do limite; ela deve ser preparada continuamente ao longo do ciclo de vida. O fundamento não é a idade cronológica nem achados isolados, mas o conhecimento da condição operacional real e dos fatores que influenciam a degradação. Para sustentar a decisão, são necessárias avaliações técnicas formais e estruturadas, capazes de demonstrar a adequação das barreiras de segurança. Em unidades flutuantes, isso requer uma metodologia de life extension com avaliação completa da unidade para verificar se a integridade estrutural e mecânica permanece suficiente para operação segura além da vida de projeto, apoiada por controle adequado de inspeção e manutenção.

**dificil_A · APROVADA**  
_Nota(s): Controle do retorno ao serviço após lay-up ou intervenção_

**P:** Um sistema de processo ficou em lay-up, passou por intervenção e agora será recolocado em operação. A equipe encerrou a manutenção, mas ainda existem isolamentos temporários sob controle documental e o sistema pode exigir inertização antes de receber fluido. Como tratar esse retorno ao serviço para decidir a sequência entre retirada de isolamentos, inertização, recomposição final e introdução de fluidos?

**R:** O retorno deve ser tratado como uma etapa própria, equivalente a uma gestão de mudanças, e não como continuação automática da manutenção. A decisão começa pelos procedimentos operacionais da instalação e pelo controle efetivo por PTW e certificados de isolamento, porque a introdução de fluidos em sistema recém-intervindo ou ocioso cria perigos próprios. Antes de admitir fluido, deve-se avaliar se o sistema precisa ser inertizado e confirmar a recomposição para a condição segura de operação. A retirada de isolamentos temporários deve ocorrer de forma controlada dentro desse arranjo, alinhada à configuração necessária para a partida. A introdução de fluidos só deve ocorrer depois dessa verificação. Concluído o retorno, o arranjo final deve ser restaurado, incluindo a reinstalação do tampão cap roscado nas extremidades de drenos.

**dificil_B · APROVADA**  
_Nota(s): Avaliação inicial da unidade para definir remoção, reboque e local de desmontagem; Riscos e restrições para retirada da FPSO da locação e reboque até estaleiro; Condição de limpeza, drenagem e isolamento da planta para transporte ou reboque_

**P:** Uma equipe propõe rebocar um FPSO para desmontagem em estaleiro para reduzir atividades offshore. A avaliação inicial indica integridade e alguns sistemas ainda operáveis para limpeza e desconexão, mas a unidade ainda não foi colocada na condição de navegação/reboque, há presença confirmada de espécie exótica invasora no casco e a perda de posição durante a retirada poderia interagir com instalação adjacente e risers. Nessa condição, qual estratégia é tecnicamente mais defensável e por quê?

**R:** A desmontagem offshore é a estratégia mais defensável. A avaliação inicial de integridade, navegabilidade e estado dos sistemas remanescentes serve para verificar se a retirada pode ser planejada, mas não basta, por si só, para justificar o reboque. Para navegação ou reboque, a unidade primeiro precisa passar por limpeza com drenagem, ventilação, purga, lavagem, remoção de TENORM e isolamento dos sistemas; só depois dessa condição são feitos os ajustes estruturais para a etapa marítima. Além disso, o reboque se torna tecnicamente desfavorável quando o deslocamento amplia riscos que superam a vantagem logística do estaleiro. A presença de espécie exótica invasora torna reflutuação e reboque não recomendados pelo risco de disseminação. E, se a perda de posição puder interagir com instalação adjacente e risers, o deslocamento passa a carregar potencial de colisão ou liberação de hidrocarbonetos. Com esses condicionantes, retirar a unidade da locação deixa de ser a opção mais aceitável.

## Gestão do Desempenho Empresarial (KPI)

### Gestão do Desempenho Empresarial (KPI)

**facil · APROVADA**  
_Nota(s): KPIs para segurança de processo e gestão dinâmica de risco operacional_

**P:** Por que indicadores de input, como horas dedicadas a HSE e número de inspeções, não bastam isoladamente para medir o desempenho em segurança de processo?

**R:** Porque eles medem esforço executado, não o efeito real sobre o risco. Em operação, desvios de produção e manutenção podem degradar ou inibir temporariamente funções de segurança, e essa mudança no estado das barreiras pode não ser captada de imediato por análises de risco menos dinâmicas. Assim, um volume alto de atividade pode coexistir com perda de integridade de barreiras e risco operacional ainda elevado. Para medir desempenho de forma útil, os indicadores precisam mostrar a condição real das barreiras e ser complementados por evidências qualitativas de impacto das atividades.

**media · APROVADA · corrigida**  
_Nota(s): KPIs para segurança de processo e gestão dinâmica de risco operacional_

**P:** Em um referencial de gestão de segurança aplicável à jurisdição UK, um SCE degradado está sendo avaliado para continuidade operacional com mitigação temporária. Quais elementos de governança essa avaliação de risco deve incluir para sustentar a decisão?

**R:** Deve haver procedimento formal e robusto definindo o processo de avaliação de risco, níveis de autoridade, expertise técnica envolvida e requisitos de revisão. A avaliação deve considerar o papel do SCE como barreira contra major accident hazards para decidir mitigação temporária e, se preciso, barreiras adicionais. As avaliações devem ser registradas e auditadas regularmente. Também devem existir revisões gerais periódicas com expertise apropriada, sem depender apenas da gestão offshore, porque o risco combinado pode ser excessivo mesmo com avaliações individuais adequadas. Quando necessário, a contribuição do SCE falho como barreira deve ser referenciada na safety case. Achados de auditoria, dados de KPI e outras informações de desempenho devem ser reportados ao nível sênior com ações decorrentes.

**dificil_A · APROVADA**  
_Nota(s): Qualidade dos dados e trending como base de KPIs preditivos de confiabilidade dos ativos_

**P:** Um KPI preditivo de confiabilidade de um conjunto motobomba mostra tendência estável, mas a equipe de campo relata piora recente do desempenho. As medições de inspeção estão consistentes, a análise usa a base corporativa única e não houve mudança relevante nas condições do fluido. Na investigação, descobre-se que o motor anterior foi substituído, porém o sistema manteve o mesmo tag funcional para o novo item. Qual é a causa mais provável da inconsistência do KPI?

**R:** A causa mais provável é a perda de rastreabilidade do item físico monitorado. Quando um componente substituído permanece sob o mesmo tag funcional, o histórico do item antigo pode ser fundido ao do novo, preservando uma falsa continuidade da série. Isso distorce o trending e pode produzir uma tendência suave ou contraditória com a condição observada em campo. Nesse cenário, erro de dado fica menos provável porque as medições estão consistentes; fragmentação entre ferramentas também perde força porque a análise usa uma base única; e mudança real do regime de processo não é a melhor explicação porque não houve alteração relevante das condições do fluido. O problema central é que a série histórica deixou de representar o mesmo equipamento ao longo do tempo.

**dificil_B · APROVADA**  
_Nota(s): Sistema de KPIs alinhado à estratégia e à criação de valor; KPIs econômicos e operacionais para sustentabilidade do negócio em FPSOs; Risco de processo, degradação de barreiras e impacto no desempenho empresarial_

**P:** Em um FPSO sob preço de petróleo pressionado, a gestão reforça metas de reduzir OPEX e manter produção. Nas semanas seguintes, margem e volume melhoram, mas há adiamento de intervenções e desvios operacionais que afetam funções de segurança. Ao revisar o painel estratégico, qual mudança de desenho é prioritária para decidir se o ativo está realmente criando valor, e por quê?

**R:** A revisão prioritária é deixar de avaliar custo e produção como resultados isolados e passar a conectá-los, no mesmo encadeamento causal, às variáveis que mostram o efeito dos desvios de operação e manutenção sobre funções de segurança e sobre o resultado econômico. O painel deve traduzir a estratégia por variáveis-chave inter-relacionadas e selecionar indicadores capazes de monitorar o impacto desses eventos nos resultados. Isso é necessário porque, sob pressão de margem, reduzir gasto ou adiar intervenção pode aparentar ganho local, mas também degradar ou inibir funções de segurança, elevando a frequência ou a severidade de cenários de risco. Como acidentes de processo afetam fortemente a sustentabilidade do negócio, melhora de margem sem essa leitura integrada pode apenas deslocar perda futura para a frente. A revisão deve, portanto, impedir que produção e OPEX premiem decisões que destruam rentabilidade do ativo quando considerado o risco total.

## Logística, Suprimentos e Movimentação de Cargas

### Logística e Suprimento Offshore

**facil · APROVADA**  
_Nota(s): Operações submarinas e recursos de apoio: como a seleção de meios e sistemas muda a logística e as interfaces com a unidade_

**P:** Por que a eliminação do umbilical em operações com AUV reduz a exigência sobre o sistema de lançamento e sobre a embarcação de apoio, especialmente em maiores profundidades?

**R:** Porque, sem umbilical, a operação deixa de depender de recursos de lançamento mais robustos associados ao manejo contínuo do veículo pela superfície, como guincho e pórtico com compensação de heave. Isso simplifica o lançamento e reduz a carga operacional e estrutural imposta à embarcação de apoio. Esse efeito aumenta com a profundidade, pois a redução de exigências ligadas ao lançamento e à recuperação se torna mais relevante à medida que a operação ocorre em lâminas d’água maiores.

**media · APROVADA**  
_Nota(s): Operações submarinas e recursos de apoio: como a seleção de meios e sistemas muda a logística e as interfaces com a unidade_

**P:** Uma campanha submarina foi inicialmente definida para inspeção, mas depois passou a incluir abertura de válvulas e cortes em componentes no fundo do mar. Mantidas as demais condições, a escolha entre AUV e ROV deve mudar?

**R:** Sim. Para uma campanha restrita à inspeção, o AUV tende a ser mais adequado porque dispensa umbilical e reduz a exigência de lançamento e de embarcação de apoio. Quando o escopo passa a incluir intervenção física, como abertura de válvulas e cortes, o critério principal deixa de ser a simplicidade logística e passa a ser a capacidade operacional de atuar mecanicamente sobre os componentes submarinos, o que favorece o ROV. Essa mudança também implica maior suporte operacional, com sala de controle, pessoal dedicado e operação de descida e recolhimento do veículo.

**dificil_A · APROVADA**  
_Nota(s): Gestão de estoques e sobressalentes no suprimento offshore: criticidade, risco, custo total e nível de serviço_

**P:** Um sistema offshore depende de um componente cuja falha interrompe a função e pode afetar segurança e produção. O mercado fornecedor desse item é complexo, a reposição não é trivial e a operação exige alto nível de atendimento. A área de compras propõe reduzir o estoque local para baixar capital imobilizado e compensar com negociação comercial mais agressiva com fornecedores. Qual decisão é tecnicamente mais adequada entre reduzir estoque, manter o sobressalente ou priorizar parceria com fornecedor?

**R:** A decisão mais adequada é manter o sobressalente. Para item com alta criticidade, a prioridade deve ser a disponibilidade necessária para mitigar consequências de segurança e minimizar indisponibilidade de produção, reduzindo também o tempo de restauração da função quando ocorrer falha. Em condição de mercado complexo e exigência de alto nível de serviço, reduzir estoque para capturar ganho apenas de custo imediato é frágil, porque o custo total do suprimento deve ser avaliado junto com o atendimento. Níveis mais altos de serviço dependem do desempenho da cadeia e tendem a exigir maior custo logístico. Parceria com fornecedor pode apoiar redução de custo total e melhoria de atendimento, mas, nesse caso, não substitui a necessidade de disponibilidade imediata do item crítico. Logo, o critério dominante é risco da indisponibilidade combinado com criticidade e nível de serviço requerido, não apenas redução do inventário aparente ou do preço de compra.

**dificil_B · APROVADA**  
_Nota(s): Embarcações de apoio offshore e configuração das cargas de suprimento, com foco no PSV; Planejamento logístico de suprimentos com PSV sob restrições de arrumação no convés; Priorização logística offshore sob restrições de armazenamento, POB e transporte_

**P:** Um FPSO, com pouco espaço para armazenagem, pede na mesma viagem de PSV contêineres de materiais para uma manutenção programada, consumíveis necessários à operação corrente e alguns volumes longos que não podem ser girados. Pela lista de pesos, tudo caberia; no arranjo real, sem empilhamento, o convés não fecha. A manutenção pode ser reprogramada sem parada imediata, mas a falta dos consumíveis afeta a continuidade operacional. Como o embarque deve ser reordenado e qual é o limitante técnico que governa essa decisão?

**R:** O embarque deve ser reordenado pelo impacto da postergação, não pela tonelagem total. Como o PSV é limitado no convés por área útil e geometria de arrumação, sem empilhamento e sem rotação, o gargalo real é a carga de convés. Portanto, devem entrar primeiro os consumíveis cuja falta compromete a continuidade operacional da unidade, e devem ser postergados ou fracionados os materiais de manutenção reprogramável e os volumes de geometria desfavorável que consumam área crítica no convés. O fato de a lista de pesos parecer compatível não resolve a viagem se os itens não puderem ser acomodados na orientação permitida. Em unidade com pouca armazenagem, a prioridade prática é selecionar o conjunto de cargas que caiba fisicamente no convés e reduza o risco de interrupção do trabalho a bordo.

### Movimentação de Cargas

**facil · APROVADA**  
_Nota(s): Controle contínuo da operação de içamento por planejamento, supervisão e handover_

**P:** Qual é a função do lifting plan na operação de içamento e como ele se relaciona com a definição do equipamento a ser utilizado?

**R:** O lifting plan funciona como a instrução operacional da atividade: ele descreve a execução em passos e define o equipamento que deve ser usado no içamento. Por isso, ele vincula a equipe a um método previamente validado para aquela operação, em vez de deixar a escolha do modo de executar e dos recursos ao ajuste informal em campo.

**media · APROVADA**  
_Nota(s): Controle contínuo da operação de içamento por planejamento, supervisão e handover_

**P:** Em um içamento offshore, o método foi autorizado, mas o supervisor precisa se ausentar e a equipe tende a continuar o trabalho sem o plano disponível no local. Qual é o papel do supervisor de içamento e da organização para manter a aderência entre o plano, a execução em campo e o monitoramento do trabalho?

**R:** O supervisor deve manter a supervisão da execução e o monitoramento do trabalho de modo que a atividade siga o método autorizado em campo. A organização deve assegurar que o plano permaneça disponível para a equipe durante a execução, que seu conteúdo tenha sido efetivamente comunicado aos participantes e que os procedimentos de supervisão e monitoramento sejam capazes de sustentar esse controle na prática. Se houver passagem de responsabilidade, ela deve ser estruturada, registrada, comunicada e supervisionada, para que o task takeover ocorra sem perda de controle. Prosseguir sem supervisão adequada e sem o plano disponível rompe a aderência entre o que foi autorizado e o que está sendo executado.

**dificil_A · APROVADA**  
_Nota(s): Limites ambientais e classificação dinâmica em içamentos entre unidade e embarcação_

**P:** Durante a transferência de uma carga entre uma unidade offshore e uma embarcação, o peso suspenso permanece dentro da capacidade nominal estática do guindaste. Na aproximação final ao convés, o movimento relativo entre os cascos aumenta, a equipe passa a ter dificuldade para estimar o momento de pouso e a tag line começa a alternar entre folga excessiva e trancos. Qual é a decisão tecnicamente correta e como justificá-la?

**R:** A decisão correta é interromper ou abortar a manobra até restabelecer condições compatíveis com o regime dinâmico. Nessa situação, o critério não é o peso estático da carga, porque a transferência entre unidade e embarcação caracteriza içamento dinâmico, no qual o movimento relativo pode elevar transitoriamente o esforço no guindaste acima do correspondente ao peso real suspenso. Por isso, a verificação aplicável é a do load chart dinâmico, não a capacidade estática mais permissiva. A dificuldade de estimar o pouso indica perda de controle da condição dinâmica, e a tag line com folga variável e trancos mostra efeito do movimento da embarcação sobre o comprimento efetivo e a folga, aumentando risco de perda de controle e emaranhamento. Como a operação também exige considerar limitações e funções de segurança do guindaste, não é tecnicamente defensável continuar apenas porque o peso nominal ainda parece aceitável.

**dificil_B · APROVADA**  
_Nota(s): Supervisão, monitoramento em tempo real e verificação de conformidade em operações de içamento offshore; Trajetória, altura livre e controle de interferências na movimentação de cargas; Interferências mecânicas, tração anômala e movimentos relativos na avaliação da capacidade de içamento_

**P:** Durante um içamento próximo a estruturas, o operador confirma comando de descida, o indicador de peso não sugere sobrecarga e a equipe de campo pede para insistir porque a carga parece apenas apoiada. Porém, a posição da carga não muda de forma coerente com o comando, e a visibilidade do operador sobre a linha é limitada. Como o supervisor deve interpretar essa condição e qual decisão técnica deve tomar?

**R:** Deve tratar a condição como provável interferência mecânica na trajetória da carga ou da linha, e não como simples resistência da carga. A combinação de comando executado, indicação aparentemente normal e ausência de movimento coerente da carga é sinal de perda de correspondência entre leitura do equipamento, caminho real da linha e comportamento físico do içamento. Em proximidade com estruturas, um ponto de contato ou enrosco pode transferir sustentação para a própria estrutura e mascarar o esforço percebido no guindaste. Com visibilidade limitada, a leitura instrumental isolada não basta. A decisão correta é interromper a manobra, confirmar o movimento real da carga por comunicação dirigida, verificar pontos potenciais de contato e snag ao longo da trajetória e só prosseguir após restabelecer evidência coerente entre comando, linha, carga e percurso livre.

## Manutenção, Inspeção e Integridade de Ativos

### Apoio Técnico e Manutenção em um FPSO (Laboratório, Oficinas, Pipe Shop)

**facil · APROVADA**  
_Nota(s): Boas práticas de qualidade em ensaios laboratoriais que suportam decisões de integridade_

**P:** Qual é a finalidade da limpeza prévia do equipamento de amostragem e de ensaio antes de testes laboratoriais de corrosão?

**R:** Evitar que resíduos presentes no sistema de amostragem ou no aparato de ensaio contaminem a amostra e falseiem o resultado do teste de corrosão. Essa limpeza é uma condição para que o resultado reflita a condição avaliada, e não interferências introduzidas pelo próprio equipamento.

**media · APROVADA**  
_Nota(s): Boas práticas de qualidade em ensaios laboratoriais que suportam decisões de integridade_

**P:** Em um FPSO, um resultado laboratorial será usado para aceitar um material e apoiar uma decisão de integridade. Como a qualidade da coleta e da preparação da amostra afeta a confiabilidade dessa conclusão?

**R:** A conclusão só é confiável quando a amostra representa a condição real da corrente de produto ou do local avaliado e quando o circuito de amostragem e ensaio foi limpo para não introduzir contaminação. Se a amostra não for representativa, o resultado pode não corresponder às condições reais do sistema. Se houver resíduos no equipamento de coleta ou de ensaio, o teste pode ser falseado. Em ambos os casos, o valor medido pode parecer válido, mas deixa de sustentar com confiança a decisão de qualidade ou integridade.

**dificil_A · APROVADA**  
_Nota(s): Sistema metrológico do laboratório e rastreabilidade aos padrões_

**P:** Um laboratório de instrumentação em FPSO precisa calibrar um transmissor de processo e avalia duas cadeias possíveis. A primeira usa poucos níveis entre o instrumento e o padrão de referência; a segunda inclui etapas intermediárias adicionais, todas formalmente previstas. Considerando apenas o efeito da hierarquia de calibração, como o aumento do número de etapas afeta a incerteza do resultado final e a robustez metrológica do resultado obtido?

**R:** Quanto maior o número de etapas na hierarquia de calibração, maior será a incerteza do resultado final, porque cada calibração depende da anterior e acrescenta sua própria contribuição à incerteza. Assim, uma cadeia mais longa tende a produzir um resultado metrologicamente menos robusto que uma cadeia mais curta, se ambas buscam a mesma finalidade. Além disso, a robustez não depende só do padrão de referência: cada elo intermediário precisa manter cadeia ininterrupta até padrão nacional ou internacional, com incerteza documentada, procedimento documentado e competência técnica reconhecida. Se qualquer etapa adicional não atender a esses elementos, o resultado deixa de estar sustentado por rastreabilidade metrológica válida.

**dificil_B · REPROVADA: suporte**  
_Nota(s): Planejamento de inspeção, monitoramento de integridade e gestão de recomendações em FPSO; Registros, rastreabilidade e controle documental de serviços, inspeções e materiais em apoio técnico e manutenção de FPSO; Priorização de correções e resposta a não conformidades para evitar interdição de FPSO_

**P:** Em uma auditoria interna de um FPSO, há recomendações antigas de inspeção para equipamentos críticos com status divergente entre sistemas. Parte dos reparos foi executada, mas os registros não ligam claramente achado, recomendação, prazo, testes/ensaios de aceitação e aprovação técnica para retorno ao serviço. A operação afirma que os itens foram tratados. Qual deve ser o diagnóstico prioritário e por que esse quadro pode sustentar risco de interdição mesmo com manutenção já realizada?

**R:** O diagnóstico prioritário é deficiência de gestão da integridade com perda de rastreabilidade do ciclo achado-recomendação-ação-verificação-fechamento, e não simples comprovação de atraso ou de reparo físico isolado. Em equipamentos críticos, a recomendação só reduz risco quando entra em sistemática formal com classificação, prazo compatível com o risco, controle de qualidade por inspeções, testes e ensaios e acompanhamento até fechamento. Se os registros não conectam a condição observada à intervenção executada, nem mostram a justificativa técnica para retorno ao serviço, não há evidência verificável de que o dano relevante foi tratado nem de que o item pode continuar operando com segurança. Essa lacuna mascara falsa sensação de controle, impede priorização por risco e fragiliza o autodiagnóstico e a demonstração de contingência e correção em tempo adequado, condição que pode evoluir para interdição.

### Cibersegurança e Integridade de Sistemas Digitais

**facil · APROVADA**  
_Nota(s): Autenticação robusta e gestão segura de credenciais em sistemas digitais que suportam funções essenciais_

**P:** Qual é a lógica do princípio do menor privilégio em sistemas que suportam funções essenciais e como ele reduz o impacto de uma credencial comprometida?

**R:** É autorizar cada usuário apenas no nível mínimo necessário para executar sua função. Assim, mesmo que uma credencial seja comprometida, o alcance do uso indevido fica restrito ao conjunto limitado de acessos já concedidos, em vez de se estender a recursos, alterações ou administrações que não eram necessários para aquela função.

**media · APROVADA**  
_Nota(s): Autenticação robusta e gestão segura de credenciais em sistemas digitais que suportam funções essenciais_

**P:** Em um sistema que suporta função essencial, a equipe pretende aceitar qualquer senha no cadastro e tratar o risco apenas com monitoramento posterior. Como a exigência de qualidade de senha se relaciona com a confiabilidade da autenticação e com a prevenção de uso indevido de contas?

**R:** Ela atua na base da autenticação: o sistema deve recusar o cadastramento de senhas sem qualidade, em vez de aceitar credenciais inadequadas. Como o acesso a esses sistemas precisa ser autenticado de forma robusta, permitir senhas de baixa qualidade enfraquece essa etapa desde a criação da credencial. Exigir qualidade de senha aumenta a confiabilidade da autenticação e reduz o risco de uso indevido de contas.

**dificil_A · APROVADA**  
_Nota(s): Contenção, erradicação e recuperação de incidentes cibernéticos na automação industrial_

**P:** Em uma planta offshore, vários ativos da rede de automação industrial perdem comunicação quase ao mesmo tempo, com forte degradação do tráfego e dificuldade de identificar a origem dos pacotes recebidos. Em paralelo, uma estação específica apresenta evidência de infecção por vírus. Nessa situação, quando a prioridade deve recair sobre a infraestrutura de conectividade com suporte de redes, e quando deve ser adotada erradicação no ativo afetado?

**R:** A prioridade inicial recai sobre a infraestrutura de conectividade quando o quadro dominante é indisponibilidade ou defeito de comunicação na rede de automação industrial, especialmente com degradação do tráfego compatível com acúmulo de requisições ou inundação de pacotes dirigida ao alvo. Nesse caso, a atuação adequada é da engenharia de telecomunicações ou redes, e a dificuldade de rastrear a origem dos pacotes não muda essa prioridade. 

A erradicação no ativo afetado deve ser adotada quando houver evidência de comprometimento local por vírus naquele sistema, porque aí o problema principal já não é apenas a conectividade da rede, mas a remoção da causa técnica da infecção. As medidas citadas para isso são a deleção do arquivo associado ao vírus ou a reinstalação do sistema operacional.

**dificil_B · APROVADA**  
_Nota(s): Arquitetura integrada de redes e acesso remoto em sistemas digitais de FPSO; Gestão de alarmes como suporte à decisão para prevenir trips e shutdowns; Integridade operacional por alarmes, IHMs e diagnósticos de automação em ambientes IT/OT_

**P:** Após ampliar a integração entre OT e camadas superiores de um FPSO, a sala de controle passou a perceber IHMs mais lentas, eventos inconsistentes e dificuldade para entender desvios. Em uma perturbação, surgiu grande volume de mensagens e a equipe não conseguiu decidir se a limitação principal estava na arquitetura de conectividade/acesso remoto ou na configuração de alarmes e diagnósticos. Qual diagnóstico deve ser priorizado para separar essas causas?

**R:** A separação deve começar por três sinais. Se a perda de apoio aparece como degradação ampla de acesso, visualização e monitoramento entre camadas, o foco inicial é a arquitetura de conectividade, porque a rede integrada é a base que torna informações e suporte remoto disponíveis de forma coordenada. Se o sintoma dominante é excesso de alarmes já em estado normal, com piora do tempo de resposta, o problema principal é a gestão de alarmes; se, durante a atuação do SIS, ocorre avalanche de alarmes, isso caracteriza configuração deficiente. Se os alarmes existem, mas a equipe continua sem distinguir falha de processo, de PLC, de rede ou condição transitória de instrumento, a prioridade passa a ser a camada de diagnósticos e IHM: gerar diagnósticos nos controladores e carregá-los de forma coerente em banco de dados, supervisório e painel.

### Inspeção e Integridade

**facil · APROVADA**  
_Nota(s): Inspeção Baseada em Risco e efetividade do plano de inspeção na gestão da integridade de FPSOs_

**P:** O que é Inspeção Baseada em Risco e como a combinação de probabilidade e consequência de falha é usada para priorizar inspeção e manutenção em equipamentos de processo?

**R:** Inspeção Baseada em Risco é uma metodologia em que o risco orienta as decisões de inspeção e manutenção, em vez de distribuir recursos de forma uniforme. Para isso, o plano deve ser coerente com os mecanismos de dano de cada equipamento e usar o histórico operacional para atualizar o risco. A priorização resulta da combinação, por meios qualitativos e quantitativos, da probabilidade de falha com a consequência de falha. Com essa combinação, os equipamentos de maior risco relativo são identificados para receber inspeção e manutenção antes dos demais.

**media · APROVADA**  
_Nota(s): Inspeção Baseada em Risco e efetividade do plano de inspeção na gestão da integridade de FPSOs_

**P:** Um equipamento operou por longo período com mudança nas condições de processo e, na última campanha, a inspeção indicou degradação diferente da prevista. Por que o plano de inspeção deve ser revisto nesse caso?

**R:** Porque, na IBR, o plano de inspeção deve refletir os mecanismos de dano atuantes e o histórico operacional usado para atualizar o risco. Se as condições de operação mudam ou a inspeção revela degradação diferente da prevista, muda também a base para estimar a probabilidade de falha e, portanto, a priorização. Além disso, a efetividade do plano depende de sua capacidade real de detectar e dimensionar o dano; por isso, novos dados podem exigir revisão de método, frequência e escopo para manter aderência ao mecanismo de dano e à redução de risco pretendida.

**dificil_A · REPROVADA: suporte**  
_Nota(s): Inspeção estrutural do casco e do envelope externo com foco em estanqueidade, corrosão e perda de seção_

**P:** Uma unidade pretende usar inspeção subaquática em substituição à docagem. Na revisão do programa, a equipe propõe concentrar o exame no costado externo e tratar separadamente os compartimentos internos, enquanto no espaço de máquinas há pontos sensíveis junto ao topo do tanque, brackets, anteparas e poços de bilge, além de conexões laterais do casco com válvulas e tubulações associadas. Que lógica de inspeção deve prevalecer para preservar o envelope do casco?

**R:** Deve prevalecer uma lógica única de integridade do envelope, não uma separação entre costado externo, compartimentos internos e conexões laterais. O plano formal precisa cobrir o envelope externo para suportar a UWILD e, ao mesmo tempo, incluir os compartimentos e arranjos estruturais cujo estado confirma se a resistência e a estanqueidade permanecem eficazes. No espaço de máquinas, as regiões da chapa do costado junto aos brackets, as anteparas na zona do topo do tanque e os poços de bilge merecem atenção específica, porque são interfaces críticas de dano estrutural. As conexões laterais do casco, com válvulas e tubulações associadas, entram na mesma lógica porque podem comprometer diretamente a estanqueidade. O exame visual deve ser complementado por medições de espessura e testes sempre que necessário para identificar corrosão substancial, deformações, fraturas, danos e outras deteriorações antes de decidir reparo ou renovação.

**dificil_B · APROVADA**  
_Nota(s): Monitoramento do desempenho da proteção catódica e critérios de intervenção; Inspeção e manutenção da integridade de revestimentos em tanques e no envelope externo do casco; Avaliação de integridade de tanques por espessura, revestimento e proteção catódica_

**P:** Em um tanque de FPSO de casco simples que armazenou água produzida, a inspeção mostra perda de espessura em áreas com revestimento em condição ruim. Ao mesmo tempo, a funcionalidade da proteção catódica não está comprovada, porque o desempenho elétrico e o estado dos ânodos ainda não foram confirmados. Tecnicamente, isso pode ser tratado apenas como anomalia localizada com acompanhamento simples, ou deve receber priorização maior? Justifique o critério de decisão.

**R:** Deve receber priorização maior. A perda de espessura reduz a margem estrutural que precisa ser verificada contra a espessura mínima exigida acrescida da sobreespessura para corrosão. Ao mesmo tempo, revestimento em condição ruim indica perda de barreira contra o meio corrosivo, e proteção catódica não comprovada impede assumir que a corrosão esteja controlada. Nessa combinação, não há só dano já ocorrido: há também possibilidade de continuidade do mecanismo corrosivo. Por isso, o caso não deve ser tratado como simples acompanhamento de anomalia localizada. A decisão técnica é reavaliar a espessura remanescente no critério estrutural e confirmar a eficácia da proteção catódica por inspeção de potencial eletroquímico, corrente e condição física dos ânodos, além de tratar a degradação do revestimento como fator de integridade.

### Instrumentação, Controle e Automação

**facil · APROVADA**  
_Nota(s): Integridade metrológica e manutenção de instrumentos por condição_

**P:** Por que a calibração periódica manual pode reduzir a disponibilidade do processo e nem sempre ser a melhor estratégia de manutenção de instrumentos?

**R:** Porque a calibração manual periódica frequentemente exige retirar o instrumento de operação e, em muitos casos, parar o processo. Isso reduz a disponibilidade. Além disso, intervir por calendário não garante necessidade técnica: uma parcela pequena das calibrações manuais tende a ser realmente necessária, e a própria intervenção manual pode afetar negativamente a confiabilidade do instrumento. Por isso, quando as leituras podem ser validadas em operação e o comportamento permanece estável, faz mais sentido condicionar a intervenção à evidência de degradação metrológica do que executar recalibrações físicas de rotina.

**media · APROVADA**  
_Nota(s): Integridade metrológica e manutenção de instrumentos por condição_

**P:** Um transmissor apresenta leituras com maior dispersão entre medições sucessivas sob as mesmas condições, mas sem deslocamento progressivo do valor ao longo das semanas. Em outro caso, a dispersão de curto prazo permanece baixa, porém a indicação se desloca lentamente ao longo do tempo. Como distinguir os dois problemas?

**R:** No primeiro caso, o padrão é mais compatível com perda de repetibilidade: a variação aparece no curto prazo como dispersão entre medições sucessivas, sem tendência persistente. No segundo, o padrão é compatível com deriva: a repetibilidade de curto prazo permanece boa, mas há deslocamento lento das características metrológicas ao longo do tempo. A distinção vem do padrão temporal das leituras: dispersão curta sem tendência aponta para repetibilidade limitada; deslocamento progressivo e persistente aponta para estabilidade de longo prazo degradada, manifestada como deriva.

**dificil_A · APROVADA**  
_Nota(s): Integração de sinais de campo para redes digitais e supervisão Web_

**P:** Em uma unidade offshore, um transmissor de pressão envia HART sobre 4–20 mA, enquanto a automação usa FOUNDATION Fieldbus e a supervisão remota usa servidor OPC-DA com cliente Web. A medição existe em campo, mas a equipe quer garantir que ela chegue até a visualização remota. Por que essa arquitetura precisa tratar a integração em duas camadas distintas, e o que cada camada deve cumprir para que a variável fique disponível de ponta a ponta?

**R:** Porque há dois problemas técnicos diferentes na cadeia. Primeiro, a variável precisa sair do domínio elétrico/comunicacional do instrumento e entrar no barramento digital da automação. Quando o instrumento fornece 4–20 mA, 0–20 mA ou HART sobre 4–20 mA e a rede é FOUNDATION Fieldbus, isso exige um conversor intermediário; sem essa interface, a variável não chega ao sistema fieldbus. Segundo, depois de recebida na automação, a variável ainda precisa ser organizada para consumo supervisório. Para isso, os dados são mapeados, recebem endereçamento padronizado e são armazenados no servidor OPC-DA; é essa base que o cliente Web usa para publicar a informação. Assim, a primeira camada condiciona a entrada da variável na rede de automação, e a segunda condiciona sua disponibilização na supervisão remota.

**dificil_B · APROVADA**  
_Nota(s): Medição de nível por radar de onda guiada e medição de interface por densidade com medidores nucleônicos; Desempenho metrológico e resposta dinâmica de instrumentos de processo; Seleção e aplicação de instrumentação e elementos finais de controle no processo_

**P:** Em um separador trifásico, a malha que tenta manter a interface estável passa a oscilar quando a composição interna varia, e a mesma variável também é cogitada para gerar desarme por interface de água criticamente baixa. A unidade dispõe de radar de onda guiada e de medição nucleônica de densidade em pontos distintos do vaso. Qual escolha de medição e de atuação é mais coerente para controle contínuo e proteção, e por quê?

**R:** A escolha mais coerente é usar, para a malha de interface e para a proteção por interface criticamente baixa, a medição de densidade aplicada ao ponto do vaso onde essa interface é operacionalmente relevante, com elemento final de controle de posicionamento contínuo. A interface entre fases pode ser inferida por densidade e esse tipo de medição pode alimentar o controlador e também a lógica de desarme. Já o radar de onda guiada mede pela reflexão na descontinuidade dielétrica; quando a composição muda, a qualidade do eco depende do contraste de constante dielétrica entre os meios, o que pode tornar o sinal menos robusto para a finalidade de controle. Além disso, mesmo uma medição fisicamente correta degrada a malha se sua resposta dinâmica ou as condições de instalação atrasarem ou deformarem as variações relevantes, porque o controlador passa a atuar sobre um sinal inadequado. Para controle proporcional, a atuação não deve ser liga-desliga.

### Manutenção e Plano de Manutenção

**facil · APROVADA**  
_Nota(s): FMEA/FMECA como base para definir estratégia e plano de manutenção de ativos críticos_

**P:** O que a FMEA/FMECA deve identificar em equipamentos críticos e por que a análise precisa avançar da função e da falha funcional até modos, efeitos e consequências?

**R:** Ela deve identificar os modos de falha e de deterioração que podem comprometer a função do equipamento crítico. A análise precisa partir da função e do desempenho esperado, passar pelas falhas funcionais, detalhar os modos de falha e suas causas, e então levantar efeitos e consequências, porque isso mostra como a perda de função ocorre e evita tratar apenas o sintoma observado. Com esse encadeamento, a manutenção pode ser definida com base no mecanismo de falha relevante e nas consequências associadas, e não apenas no registro de que o item falhou.

**media · APROVADA**  
_Nota(s): FMEA/FMECA como base para definir estratégia e plano de manutenção de ativos críticos_

**P:** Após o encerramento técnico dos serviços, a engenharia de manutenção consolida indicadores e histórico no sistema e percebe recorrência de intervenções e lacunas de reposição. Como esse histórico pode gerar recomendações sobre planos de manutenção e sobressalentes?

**R:** O histórico e os indicadores extraídos do sistema permitem analisar o comportamento das falhas e das intervenções já executadas. A partir dessa análise, a engenharia pode encaminhar para a gestão recomendações de melhoria em planos existentes, criação de novos planos e inclusão de itens em estoque. Quando associados aos resultados de estudos de FMEA, esses dados ajudam a revisar o plano conforme a necessidade observada no histórico, em vez de manter tarefas e reposições sem base nos registros consolidados.

**dificil_A · APROVADA**  
_Nota(s): Verificação operacional de barreiras e retorno seguro após manutenção_

**P:** Após manutenção em um sistema de armazenamento com tanques de carga e de armazenamento de água, o supervisório mostra barreiras e intertravamentos como disponíveis. Na inspeção de campo, a equipe encontra uma válvula crítica fora da posição normal, um vent sem recomposição correta e dúvida sobre a remoção de um isolamento temporário. A produção pode ser mantida com contingência provisória, mas sem evidência de que o arranjo real voltou à condição de projeto. O retorno ao serviço é tecnicamente defensável?

**R:** Não. A disponibilidade aparente no supervisório, sozinha, não confirma a barreira. Após manutenção, é necessário verificar em campo se o equipamento foi recomposto conforme o projeto, com remoção de isolamentos temporários, retorno de válvulas críticas à posição normal, posicionamento correto de vents e alinhamento dos dispositivos protetivos. Em sistema de armazenamento, também é preciso confirmar aderência entre a condição operacional observada e a condição de projeto. Como há incoerências de campo e não se comprovou o arranjo pretendido, a barreira está apenas nominalmente disponível. Nesse quadro, a continuidade só seria defensável se a contingência residual mantivesse o risco em nível aceitável; se isso não puder ser demonstrado, deve-se restringir a operação ou parar o equipamento, o sistema associado ou a planta, conforme necessário.

**dificil_B · APROVADA**  
_Nota(s): Dimensionamento e priorização de sobressalentes críticos por risco, falha e lead time; Integração do plano de manutenção com materiais, suprimentos, custos e conformidade em CMMS/SAP PM; Planejamento de manutenção e provisão de recursos para reduzir indisponibilidades_

**P:** Em um FPSO, a falha de um componente importante para continuidade operacional exigiu reparo físico simples, mas a parada durou muito mais que o previsto porque a peça não estava disponível, a compra só começou após a falha e houve recorrência de fretes emergenciais e ordens emitidas sem material assegurado. Qual diagnóstico estrutural melhor explica a indisponibilidade prolongada e qual priorização de gestão tende a reduzir esse padrão?

**R:** O quadro indica que a indisponibilidade foi ampliada mais pela prontidão logística do que pela complexidade técnica do reparo. A causa estrutural mais consistente é a combinação de gestão fraca de sobressalentes críticos com integração insuficiente entre plano de manutenção, materiais e compras. Itens relevantes devem ser priorizados pelo impacto da falha, risco associado, taxa de falha, quantidade instalada e lead time, e não só por consumo histórico ou custo da peça. Se a ordem é emitida sem verificação, reserva ou ressuprimento antecipado, a restauração passa a depender de compra reativa, aumentando atraso, erro de especificação e risco de desvio de qualidade. A prioridade é integrar o CMMS ao microplanejamento de materiais e ao ressuprimento, dimensionando sobressalentes críticos por risco e lead time para que a programação já nasça executável.

## Segurança Ocupacional, Saúde e Meio Ambiente

### Condições Ambientais e Impactos Operacionais

**facil · APROVADA**  
_Nota(s): Falha de risers: escalonamento do dano, perda de contenção e avaliação de consequências ambientais_

**P:** Por que a falha de um riser caracteriza perda de contenção com potencial de liberação de hidrocarbonetos ao ambiente marinho?

**R:** Porque o riser transporta os fluidos produzidos e, quando falha, esses produtos podem escapar do sistema e ser descarregados no mar. Se o fluido inclui hidrocarbonetos, a falha passa a representar liberação desses contaminantes ao ambiente marinho, e não apenas um problema de integridade da linha.

**media · REPROVADA: suporte**  
_Nota(s): Falha de risers: escalonamento do dano, perda de contenção e avaliação de consequências ambientais_

**P:** Em uma ruptura total de riser flexível no trecho submerso, como o evento pode evoluir de um dano localizado para um cenário de maior severidade operacional e ambiental?

**R:** A ruptura pode deixar de afetar apenas o riser inicialmente danificado quando o movimento ou a interação da falha passa a atingir estruturas e risers adjacentes, provocando novos rompimentos. Com isso, o cenário evolui de uma perda de contenção isolada para um encadeamento com dano físico adicional na instalação e aumento da liberação de óleo ao mar. A severidade cresce porque se combinam o escalonamento mecânico da falha e a ampliação do impacto ambiental pela maior descarga de hidrocarbonetos.

**dificil_A · APROVADA**  
_Nota(s): Temperatura ambiente na adequação de sistemas de monitoramento de gases_

**P:** Em uma área interna próxima à exaustão de gases e produtos de combustão, o monitor de gases foi especificado com base na temperatura externa média. Ao longo do dia, a carga do processo varia, o local aquece em alguns turnos e há períodos de pouca ventilação. Que avaliação técnica deve ser feita para decidir se o sistema de medição continua adequado nessa condição?

**R:** A decisão deve ser baseada na temperatura do ponto realmente monitorado, não na condição externa. É preciso verificar se as variações térmicas ao longo do dia, somadas ao regime operacional, deslocam a faixa de valores esperada a ponto de comprometer o fundo de escala e a adequação da medição. Também é necessário caracterizar a composição do fundo gasoso no local, porque gases presentes fora da espécie de interesse podem introduzir leituras equivocadas. Como há pouca ventilação em certos períodos, a análise deve incluir a possibilidade de condensação e seu efeito sobre a viabilidade da medição. Por fim, o regime de exposição do sensor ao ambiente real deve entrar no critério, porque a adequação depende das condições efetivas de operação e não apenas da condição nominal escolhida para operação normal.

**dificil_B · APROVADA**  
_Nota(s): Dispersão ambiental, monitoramento e modelagem de consequências em FPSOs: efeito de vento, geometria, temperatura e composição do meio; Temperatura ambiente na adequação de sistemas de monitoramento de gases; Detecção, lógica de automação e shutdown sob interferência, fogo, fumaça e necessidade de resposta de emergência_

**P:** Em um módulo offshore, alarmes intermitentes de gás surgem quando a carga do processo aumenta e a área fica mais quente. As inspeções não confirmam atmosfera perigosa persistente, mas o arranjo tem obstáculos e zonas de baixa ventilação onde pode haver recirculação. A repetição já reduz a confiança dos operadores nos alarmes automáticos. Qual diagnóstico inicial deve ser priorizado para decidir se o problema é pluma real mal representada pelo monitoramento ou inadequação do próprio sistema de detecção, e que implicação isso traz para a lógica de resposta automática?

**R:** Deve-se priorizar um diagnóstico em duas frentes, sem assumir que o alarme decorre só de instrumentação ou só de dispersão real. Primeiro, verificar se a geometria, a direção do vento e possíveis zonas de vórtice/recirculação podem gerar acúmulos locais e concentrações transitórias que não aparecem como atmosfera persistente; nessas condições, velocidade média aceitável não garante boa predição de concentração. Segundo, checar se o sistema de detecção continua adequado à temperatura real do ponto monitorado, às variações térmicas do regime, à presença de gases espúrios e ao modo de exposição do sensor, porque isso pode deslocar faixa útil, introduzir interferência e degradar a confiabilidade da leitura. A implicação é que a resposta automática não deve ser julgada apenas pela existência de alarmes ou shutdown: erro de medição, pseudoalarmes ou lacunas de lógica podem retardar o reconhecimento do evento real e deixar a cadeia alarme-shutdown-HVAC incompleta para proteger áreas ocupadas.

### Gestão de Pessoas e Treinamento

**facil · REPROVADA: correcao_tecnica, suporte**  
_Nota(s): Governança do programa de treinamento como base para avaliar eficácia, retenção e conformidade_

**P:** Qual a diferença entre uma matriz de treinamentos mandatórios gerais e uma matriz de treinamentos em procedimentos operacionais por função, e o que cada uma comprova ou não comprova?

**R:** A matriz de treinamentos mandatórios gerais comprova a cobertura de cursos obrigatórios aplicáveis à força de trabalho, com evidência formal e documentada do que foi realizado. Ela não comprova, por si só, que a pessoa foi treinada nos procedimentos operacionais específicos que executa na função nem que diferenças de competência entre ocupantes do mesmo cargo foram controladas. Já a matriz de treinamentos em procedimentos operacionais por função vincula a necessidade de capacitação ao cargo e às atividades efetivamente executadas, permitindo demonstrar aderência do treinamento à função e evidência de competência para operar conforme os procedimentos aplicáveis.

**media · APROVADA**  
_Nota(s): Governança do programa de treinamento como base para avaliar eficácia, retenção e conformidade_

**P:** Uma unidade mantém matriz de treinamento, mas ela não acompanha mudanças de pessoal, lacunas de competência e treinamentos já vencidos. Qual é a função de uma matriz atualizada nesse contexto e por que sua desatualização compromete auditorias, escalação de pessoal e demonstração de conformidade?

**R:** A função da matriz atualizada é refletir o status real das competências requeridas e realizadas, permitindo verificar se a força de trabalho continua atendendo ao que cada função exige e se o cumprimento do treinamento pode ser periodicamente confirmado. Quando a matriz não retrata a situação real, ela deixa de servir como controle das competências e passa a mascarar lacunas. Com isso, a organização perde rastreabilidade para auditoria, reduz a confiabilidade da escalação de pessoal porque não consegue confirmar quem está efetivamente apto, e enfraquece a demonstração de conformidade, já que a evidência disponível não corresponde ao estado real das competências.

**dificil_A · APROVADA**  
_Nota(s): Gestão de competências, critérios por função e treinamento em instalações offshore_

**P:** Em uma unidade offshore, supervisores são escolhidos sem critério formal de liderança; as descrições de função trazem requisitos vagos; um mesmo cargo acumula funções operacionais distintas sem matriz específica; e parte da equipe executa procedimentos com documentos desatualizados. Embora existam treinamentos registrados, há dúvidas recorrentes sobre o escopo de cada papel. Qual é a causa predominante a diagnosticar primeiro: definição insuficiente do padrão da função, qualificação inadequada para o papel, insuficiência de recursos ou falha na avaliação de competência?

**R:** A causa predominante a diagnosticar primeiro é a definição insuficiente do padrão da função. Os sinais centrais são requisitos vagos nas descrições de função, ausência de critérios formais para supervisão com responsabilidade de liderança e acúmulo de funções sem matriz específica por função. Isso indica que responsabilidades, tarefas, procedimentos e tarefas críticas de segurança não foram desdobrados em requisitos claros por papel, inclusive quando um mesmo cargo exerce funções distintas. Nessa condição, a qualificação para o papel e o treinamento registrado podem existir, mas ficam apoiados em um padrão mal definido. Documentos desatualizados agravam a execução, porém não explicam sozinhos a indefinição de escopo e de critérios do papel. Insuficiência de recursos e falha de avaliação podem coexistir, mas, pelos sintomas dados, aparecem mais como fatores secundários ou consequências de um padrão de função mal especificado.

**dificil_B · APROVADA**  
_Nota(s): Avaliação de competência e assurance baseados em evidências; Métodos de avaliação e fechamento de lacunas de competência; Critérios objetivos para demonstrar eficácia de treinamento e retenção de competência_

**P:** Após reciclagem periódica, a maior parte da equipe de uma unidade offshore está com certificados válidos e aprovação em avaliações gerais. Mesmo assim, exercícios de cenário e observações em campo mostram erros repetidos em etapas específicas de um procedimento crítico e pouco frequente. Qual mudança deve ser priorizada no assurance de competência para demonstrar eficácia real do treinamento e decidir entre reciclagem, restrição de escopo ou retreinamento?

**R:** Priorizar uma avaliação por função, baseada em evidências múltiplas e com foco na parte da tarefa onde o erro aparece. Certificado e aprovação global não bastam para provar competência mantida. Para procedimento crítico e pouco frequente, a avaliação deve combinar verificação de conhecimento, observação prática e exercício de cenário, com exigência e registro proporcionais ao risco. O diagnóstico precisa apontar a área ou seção específica com deficiência, porque a ação corretiva deve ser dirigida ao mesmo escopo. Se a insuficiência estiver localizada, aplica-se treinamento adicional específico e reavaliação restrita à parte deficiente; se a tarefa for rara, a reciclagem deve ser mais frequente ou até pré-tarefa. Depois, é necessário manter monitoramento do desempenho e reavaliações em áreas-chave para confirmar retenção e uso correto no trabalho real.

### Meio Ambiente, Gestão Ambiental e Sustentabilidade

**facil · REPROVADA: suporte**  
_Nota(s): Gestão ambiental operacional e prontidão para prevenção e resposta a impactos marinhos_

**P:** Qual é a função de sistemas rigorosos de gestão de saúde, segurança, social e ambiental na avaliação e minimização de riscos em operações offshore com potencial de impacto ao ambiente marinho?

**R:** Fornecer à operação capacidade estruturada para avaliar e minimizar riscos e para desenvolver processos que reduzam impactos negativos ao ambiente marinho. Na prática, esses sistemas organizam a prevenção, o controle e a resposta de modo que a proteção ambiental seja tratada como parte da gestão dos riscos operacionais.

**media · APROVADA**  
_Nota(s): Gestão ambiental operacional e prontidão para prevenção e resposta a impactos marinhos_

**P:** Em uma emergência ambiental offshore, a unidade possui procedimentos e registros formalmente adequados, mas parte dos equipamentos de controle da poluição está com manutenção deficiente e condição operacional incerta. Por que a existência desse procedimento não garante, sozinha, capacidade real de resposta?

**R:** Porque a decisão não deve se basear apenas na adequação documental. Também é necessário avaliar a eficácia de normas, procedimentos e registros para a decisão emergencial e considerar as condições reais de operação e manutenção dos equipamentos de controle da poluição e de prevenção de acidentes. Se a condição desses equipamentos é deficiente ou incerta, a capacidade de resposta fica limitada pela prontidão operacional real das barreiras, não pelo que o procedimento presume.

**dificil_A · REPROVADA: suporte**  
_Nota(s): Integração do SGA/SMS à governança de projetos de E&P/FPSO no ciclo de vida de projeto_

**P:** Em um projeto de FPSO, duas alternativas de utilidades têm desempenho econômico inicial semelhante. A alternativa 1 usa materiais e processos mais intensivos em recursos e energia, mas atende ao requisito funcional. A alternativa 2 reduz consumo de recursos, adota processos e fontes energéticas de menor impacto e apresenta menor exposição futura a emissões e a preços de carbono. Qual alternativa deve ser escolhida e por quê?

**R:** A alternativa 2. Com desempenho econômico inicial semelhante, a decisão deve usar abordagem de ciclo de vida, não apenas impacto imediato. Nessa lógica, a comparação inclui minimização de recursos consumidos e seleção de materiais, processos e fontes energéticas de menor impacto ao longo das fases do empreendimento. Além disso, a decisão deve considerar o risco de carbono, que abrange a exposição futura a emissões, preços de carbono e efeitos associados às mudanças climáticas e à transição energética. Portanto, a alternativa 2 é a mais consistente porque combina menor carga ambiental no ciclo de vida com menor exposição econômica e estratégica ao risco de carbono.

**dificil_B · APROVADA**  
_Nota(s): Conformidade legal, licenciamento ambiental e tratamento de não conformidades em FPSO/FSO; Monitoramento ambiental de emissões atmosféricas, efluentes e indicadores de sustentabilidade; Indicadores de água produzida e efluentes oleosos: monitoramento em linha, seleção de medidores, validação do tratamento e reuso_

**P:** Em auditoria interna de um FPSO no Brasil, a equipe sustenta que o descarte de água produzida está sob controle porque o TOG em linha permanece estável e é usado para ajustar o tratamento em tempo real. Na revisão do licenciamento e dos relatórios enviados, aparece que a condicionante de descarte foi demonstrada por critério analítico diferente do indicador operacional. Qual é o diagnóstico mais provável e qual deve ser a prioridade técnica imediata?

**R:** O quadro mais provável é de falsa conformidade: há controle operacional do processo, mas a evidência usada para demonstrar atendimento ambiental pode estar desalinhada com o parâmetro, o método analítico e as condições exigidas pelo licenciamento. Monitoramento em linha de TOG é útil para resposta rápida e ajuste do tratamento, porém a demonstração formal de conformidade precisa seguir o critério aplicável ao descarte, inclusive parâmetro e método de medição. A prioridade imediata é verificar a coerência entre condicionante, jurisdição, método analítico, relatórios emitidos e indicador em linha; se houver desvio, tratar como não conformidade, com ação corretiva rastreável e proporcional ao risco. Só depois disso faz sentido concluir se o problema está na medição operacional, na validação do tratamento ou no controle documental da conformidade.

### Saúde Ocupacional

**facil · APROVADA**  
_Nota(s): Vigilância médica ocupacional em cenários de surtos e pandemias offshore_

**P:** Qual é a função de um programa de vigilância médica ocupacional em uma instalação offshore além do acompanhamento clínico individual?

**R:** É transformar sinais de agravo à saúde em gestão ativa do risco: receber notificações, consolidar informações de saúde, investigar casos, definir medidas de controle e acompanhar sua eficácia. Em cenário infeccioso, isso inclui usar dados como POB, casos suspeitos e contactantes para orientar isolamento, restrição de circulação, manejo de casos e retorno ao trabalho. O programa também apoia decisões de continuidade operacional quando a doença pode afastar profissionais-chave necessários para operar e responder a emergências com segurança.

**media · APROVADA**  
_Nota(s): Vigilância médica ocupacional em cenários de surtos e pandemias offshore_

**P:** Em uma unidade offshore, surgem relatos recorrentes de adoecimento, mas a equipe só registra os casos em planilhas. Qual encadeamento deve existir para que a vigilância médica realmente reduza a recorrência e permita avaliar se a resposta funcionou?

**R:** O encadeamento deve começar pela notificação formal do agravo, seguida de investigação efetiva do caso ou da preocupação de saúde. Dessa investigação devem sair ações corretivas pertinentes para prevenir recorrência. Depois, essas ações precisam ser rastreadas e executadas com registros de gestão que permitam comprovar a implementação. Por fim, a organização deve verificar periodicamente a eficácia do que foi adotado e decidir se são necessários controles adicionais. Sem essa sequência, há registro de ocorrência, mas não evidência de tratamento da causa nem de efetividade da resposta.

**dificil_A · APROVADA**  
_Nota(s): Gestão de casos de doença, restrições e retorno seguro ao trabalho offshore_

**P:** Em uma unidade offshore, um trabalhador foi afastado após apresentar sintomas compatíveis com doença infecciosa durante o turno e ter circulado por áreas comuns antes da avaliação. Ao mesmo tempo, a supervisão informa que há outros afastamentos recentes ligados a trabalho em área com condição operacional insegura e ambiente fora do padrão. Qual deve ser a prioridade imediata de gestão para esse caso específico e por quê?

**R:** A prioridade imediata deve recair no controle do caso infeccioso. Como há suspeita de doença infecciosa com circulação prévia pela instalação, o manejo precisa acionar o encadeamento de monitoramento de saúde, isolamento, impedimento de circulação, comunicação clara ao pessoal, sanitização, manejo do caso e retorno ao trabalho. Os afastamentos por condição operacional insegura e por ambiente em desconformidade exigem correção do contexto operacional, mas isso responde a outra natureza de problema. Quando o afastamento decorre de suspeita infecciosa, tratar o caso como mera questão de condição operacional reduz a efetividade da resposta, porque deixa de atacar os mecanismos centrais de contenção do risco de transmissão a bordo.

**dificil_B · APROVADA · corrigida**  
_Nota(s): Água potável offshore em FPSO/FSO: disponibilidade, controle sanitário e contingência operacional; Prevenção de surtos a bordo por controle de agentes biológicos, água potável, alimentos e interfaces de abastecimento; Planejamento para surtos e contingências sanitárias coletivas em instalações offshore_

**P:** Após uma refeição, vários trabalhadores de setores diferentes apresentam sintomas gastrointestinais em poucas horas. No mesmo período, houve abastecimento recente de água por bunkering e falha de refrigeração na área de alimentos. Nas primeiras decisões, qual linha de investigação e contenção deve ser priorizada para preservar a operação segura?

**R:** A prioridade é tratar o evento como exposição coletiva por fonte comum e investigar, em paralelo, água potável e alimentos. Na água, verificar suspeita de contaminação ou perda de potabilidade ligada ao bunkering, incluindo condição sanitária das mangueiras e a identificação correta dos pontos potáveis. Nos alimentos, verificar se a falha de refrigeração comprometeu a conservação e se houve falha de higiene na manipulação. Devem ser acionados os planos de contingência para contaminação ou falta de água potável e para falha de refrigeração ou surto alimentar. Em paralelo, aplicar medidas de contenção da ocorrência e reavaliar se o número de afetados ou o impacto no efetivo já compromete a normalidade operacional, para adaptar a operação sem descuidar do gerenciamento de riscos.

### Segurança Ocupacional

**facil · APROVADA**  
_Nota(s): Trabalhos a quente: fontes de dano, avaliação prévia da área e proteção do trabalhador_

**P:** Quais são os principais perigos de solda, corte e outros trabalhos a quente que devem ser considerados antes da liberação da atividade?

**R:** Devem ser considerados, no mínimo, os seguintes perigos: queimaduras por exposição térmica; ignição quando houver vapores inflamáveis; inalação de gases, fumos e vapores, especialmente em ambiente fechado; choque elétrico; luminosidade excessiva do arco de solda; e projeção de fagulhas e partículas, incluindo projéteis oriundos de corte. Em alguns contextos, também há risco de explosão de cilindros de oxigênio.

**media · APROVADA**  
_Nota(s): Trabalhos a quente: fontes de dano, avaliação prévia da área e proteção do trabalhador_

**P:** Em um trabalho a quente executado em altura com solda elétrica, há possibilidade de flash fire e exposição intensa ao arco. Como relacionar cada EPI citado ao mecanismo de dano que ele deve mitigar?

**R:** A roupa resistente ao fogo deve ser associada ao risco térmico e ao possível flash fire, reduzindo a severidade da exposição ao calor. O capacete de soldagem com tonalidade adequada deve ser associado à luminosidade excessiva da solda elétrica, atenuando a agressão ocular causada pelo arco. A proteção contra quedas deve ser associada ao risco adicional do trabalho em desnível, para mitigar as consequências de perda de equilíbrio ou queda durante a atividade.

**dificil_A · APROVADA**  
_Nota(s): Diálogos de segurança e governança do PTW/CoW_

**P:** Uma equipe inicia uma intervenção coberta por PTW. No campo, o arranjo real difere do planejado, entra pessoal não listado, surge uma nova etapa não prevista e a coordenação passa a ser conduzida por quem não está formalmente designado nem treinado para aquela responsabilidade. A mudança não foi submetida a nova análise de perigos, e os envolvidos não alinharam os novos controles com as demais frentes. Nessa condição, qual é a decisão correta sobre a continuidade do trabalho?

**R:** O trabalho não deve continuar. A condição correta é interromper a atividade e revalidar o PTW antes de prosseguir, porque houve mudança de condição, de pessoal, de escopo e de interfaces, o que pode tornar inadequados os perigos e controles originalmente registrados. A equipe deve reconfirmar no local os perigos presentes, os controles efetivamente implementados e as interações com outros trabalhos. A coordenação também precisa voltar a um responsável formalmente designado e competente para essa função. Se a nova etapa introduziu perigos não avaliados ou o desvio não for corrigido de imediato, o executante deve recusar a continuidade até que a análise prévia e os controles sejam restabelecidos e comunicados à equipe.

**dificil_B · REPROVADA: suporte**  
_Nota(s): Condição operacional do guindaste e controles prévios ao uso em içamento offshore; Prevenção de contato, enroscamento e queda de objetos na movimentação de cargas; Protocolos de comunicação e coordenação em tarefas críticas de movimentação e içamento_

**P:** Em um içamento blind lift em área congestionada, a carga passa por trecho com folga reduzida junto a estruturas. Ao girar o turntable, a carga começa a derivar lateralmente mais do que o previsto, e a equipe em campo diverge por rádio sobre corrigir o movimento ou seguir. Qual diagnóstico e prioridade de ação melhor tratam a perda de previsibilidade da manobra?

**R:** O quadro deve ser tratado como combinação potencial de três causas, não como desvio único: mudança das condições da carga durante o giro, ponto crítico de trajetória insuficientemente controlado e coordenação/comunicação inadequadas. A prioridade é interromper a progressão da manobra e restabelecer controle antes de qualquer correção. Em seguida, deve-se verificar se o giro alterou o centro de gravidade e, com isso, a resposta esperada da carga; reavaliar passo a passo o trecho de folga reduzida para confirmar pontos de contato ou enroscamento e posicionar spotters nos pontos críticos; e restabelecer comando único com comunicação de movimento clara, verificável e sem ambiguidade, mantendo pessoas fora da line of fire. Se essas barreiras não estiverem asseguradas, a manobra não deve prosseguir.
