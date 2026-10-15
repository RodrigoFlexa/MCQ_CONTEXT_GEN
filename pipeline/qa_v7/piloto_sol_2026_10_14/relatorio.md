# Piloto QA v7: perguntas a partir do inventário

Modelo gpt-6.1-sol. 160 questões geradas, 155 aprovadas pelo juiz (97%). Tempo 6.7 min. Chamadas 294, tokens entrada 1,195,225, saída 195,647.

| Tipo pedido | geradas | aprovadas | medido fácil | medido média | medido difícil |
|---|---:|---:|---:|---:|---:|
| facil | 40 | 39 | 32 | 7 | 0 |
| media | 40 | 37 | 3 | 31 | 3 |
| dificil_A | 40 | 39 | 0 | 6 | 33 |
| dificil_B | 40 | 40 | 0 | 0 | 40 |

Motivos de reprovação: suporte (3), autonomia (1), correcao_tecnica (1), escopo (1), sem_generalizacao (1), codigo:referencia_alternativas (1)
Corrigidas pelo refinador: 7

## Sistemas de Lastro, Estabilidade, Ancoragem e Posicionamento, Offloading e Tanques de Carga

### Operação de Offloading

**facil · medido fácil · APROVADA**  
_Nota(s): Falhas de propulsão, energia, controle e apoio que degradam a manobrabilidade do aliviador no offloading_

**P:** Quais consequências operacionais estão associadas à perda de propulsão ou à parada do sistema diesel-gerador do aliviador, e qual risco existe em um evento de drive-off durante offloading com posicionamento dinâmico (DP)?

**R:** A perda de propulsão e a parada do sistema diesel-gerador estão associadas a atraso operacional e podem evoluir para colisão se o problema persistir ou a operação prosseguir. Em um evento de drive-off com aliviador DP, também pode ocorrer colisão com o FPSO; na condição de curta separação entre as embarcações, a velocidade máxima de colisão pode ser de 2 nós, pois a distância disponível limita a aceleração.

**media · medido média · APROVADA**  
_Nota(s): Falhas de propulsão, energia, controle e apoio que degradam a manobrabilidade do aliviador no offloading_

**P:** Durante o offloading, considere quatro ocorrências distintas: falha de equipamento que exige desconexão do mangote, falha no cilindro com posicionamento dinâmico (DP) disponível, problema de thruster e problema de satélite do sistema de posicionamento global (GPS). Qual resposta operacional deve ser aplicada a cada ocorrência, distinguindo interrupção da transferência de verificação das informações de posicionamento?

**R:** Na falha de equipamento, abortar o offloading, ativar a parada de emergência da transferência e executar a desconexão, a desamarração e o afastamento do aliviador em relação à unidade de produção. Na falha no cilindro, executar a desconexão, a desamarração e o afastamento utilizando o DP. No problema de thruster, abortar a operação. No problema de satélite GPS, verificar os avisos aos navegantes sobre informações de satélites, sem equiparar automaticamente essa ocorrência às falhas para as quais se indica abortar a operação.

**dificil_A · medido difícil · APROVADA**  
_Nota(s): Perda de posição do navio aliviador e mecanismos de colisão no offloading com FPSO_

**P:** Durante o offloading, um navio aliviador começa a perder posição após a parada do motor auxiliar, seguida de perda de alimentação elétrica em vários sistemas, inclusive nas bombas de óleo lubrificante do motor principal. Em seguida, param o motor principal e os sistemas de navegação e manobra; a equipe atribui a excursão apenas à perda de propulsão. Qual diagnóstico melhor explica essa sequência e quais diferenças nos sintomas sustentariam as hipóteses de perda isolada de propulsão ou erro de programação/julgamento?

**R:** O diagnóstico mais consistente é blackout em cascata decorrente da falha do motor auxiliar: a interrupção da alimentação elétrica afeta vários sistemas, incluindo as bombas de lubrificação do motor principal, e leva à parada deste e dos sistemas de navegação e manobra. Portanto, a perda de propulsão é parte da cadeia, não explica isoladamente o conjunto de sintomas. A hipótese de perda isolada de propulsão seria mais compatível com parada propulsiva sem essa sequência de interrupção elétrica generalizada; pode causar atraso operacional e evoluir para colisão se persistir. Já manobras inadequadas sem a sequência de blackout seriam compatíveis com erro de programação do sistema automático ou julgamento incorreto das condições de manobrabilidade. Esses sintomas permitem diferenciar as hipóteses, mas não identificar, por si só, qual desses dois erros ocorreu.

**dificil_B · medido difícil · APROVADA**  
_Nota(s): Teste de estanqueidade, pressurização e partida da transferência no offloading; Ensaios e verificações de integridade aplicáveis ao offloading; Integridade mecânica e contenção na interface de offloading: manifold, conexões, mangotes, QRF e linhas_

**P:** Após a conexão para offloading, a linha foi pressurizada até o valor previsto e monitorada pelo tempo definido, sem vazamento identificado no teste de estanqueidade. Após despressurização controlada, a circulação de água para o tanque de resíduos do aliviador, na máxima vazão possível, apresentou contrapressão anormal e vazamento visível junto à conexão do mangote com o manifold. A equipe propõe atribuir ambos os sinais à obstrução e iniciar o bombeio de óleo, apoiando-se no resultado inicial do teste. Qual decisão e diagnóstico integrado são tecnicamente consistentes?

**R:** Não liberar o bombeio de óleo: o resultado inicial de estanqueidade não elimina a perda de contenção observada posteriormente. A contrapressão anormal durante a circulação de água na máxima vazão é indício de obstrução parcial, enquanto o vazamento visível evidencia um problema de contenção na interface; não é consistente atribuir os dois sinais apenas à obstrução. A investigação deve contemplar tanto a restrição da linha quanto a conexão e o manifold, pois conexão incorreta e falha do manifold são mecanismos associados a vazamentos. Não se deve presumir que o corpo do mangote seja a única origem possível. A verificação de contenção e a avaliação hidráulica são complementares, não substitutas. No encerramento de novos testes de estanqueidade, despressurizar de forma controlada, respeitando a taxa máxima especificada. A sequência de partida — teste, água para o tanque de resíduos e depois óleo para os tanques de carga — não justifica avançar com anomalias de integridade ainda presentes.

### Operação de tanques de carga, lastro, sistema gás inerte, ventilação e estabilidade

**facil · medido fácil · APROVADA**  
_Nota(s): Uso do sistema de lastro para controlar calado, trim, banda e flutuabilidade_

**P:** Qual é a função do sistema de lastro em relação ao calado durante o carregamento e a descarga de óleo cru em um FPSO monohull?

**R:** O sistema de lastro compensa as variações de calado decorrentes do carregamento e da descarga de óleo cru.

**media · medido média · APROVADA**  
_Nota(s): Uso do sistema de lastro para controlar calado, trim, banda e flutuabilidade_

**P:** Durante a descarga de óleo cru de um FPSO monohull, uma manobra de lastro corrige calado, trim e banda, mas deixa o momento fletor longitudinal acima do limite permissível. Essa condição pode ser aceita apenas porque a atitude da unidade foi corrigida? Justifique o critério técnico.

**R:** Não. A correção da atitude da unidade não é suficiente para aceitar a condição. A movimentação de lastro deve compensar a variação de calado e preservar uma condição segura e nivelada, mantendo simultaneamente forças cortantes, momentos fletores e tensões torsionais dentro dos limites permissíveis. Portanto, a distribuição de lastro precisa ser revista para atender também aos limites estruturais.

**dificil_A · medido média · APROVADA**  
_Nota(s): Barreiras de contenção e intertravamentos de segurança em carga, offloading e gás inerte_

**P:** Durante o offloading de um FPSO, é identificada deformação no mangote com potencial de comprometer sua integridade, mas ainda não há vazamento visível. O navio aliviador também começa a sair de posição, com possibilidade de desconexão da mangueira. A equipe propõe manter o bombeio enquanto verifica o defeito. Qual deve ser a resposta operacional inicial e como as funções de isolamento e parada devem contribuir para preservar a contenção?

**R:** Interromper imediatamente a transferência, antes de investigar o defeito ou adotar outras providências. A ausência de vazamento visível não justifica continuar: a anormalidade apresenta potencial de avaria ou poluição. As funções de isolamento e parada previstas para o sistema devem minimizar a perda de hidrocarbonetos caso ocorra ruptura do mangote ou desconexão pela saída de posição do aliviador. Essas barreiras podem combinar parada das bombas de carga, isolamento manual, válvulas de fechamento remoto e acoplamentos de separação de emergência (breakaway couplings), conforme o arranjo existente. A prioridade é interromper a condição insegura e limitar a perda de contenção, não manter o bombeio para concluir o diagnóstico.

**dificil_B · medido difícil · APROVADA**  
_Nota(s): Reconfiguração de drenos e transferências na indisponibilidade de tanques slop; Inventário de tanques por medição remota e conferência independente para estabilidade; Planejamento e verificação da condição de lastro com documentos de bordo e software de estabilidade_

**P:** Em um FPSO, o slop de bombordo está indisponível e os drenos foram redirecionados ao slop de boreste; o coletor de fundo de bombordo, porém, mantém uma comunicação defeituosa pela qual a carga pode drenar para o slop indisponível. Após uma transferência por esse coletor, o programa de estabilidade, alimentado por níveis remotos ainda não conferidos manualmente, indica condição aceitável, mas o trim observado e a resposta dos tanques divergem do previsto. A equipe propõe corrigir o trim com lastro e continuar as transferências. Qual decisão deve preceder essas manobras e como distinguir erro de indicação de redistribuição real de conteúdo?

**R:** Não se deve aprovar a próxima transferência ou compensar o trim com lastro apenas com base na condição calculada. Primeiro, é necessário confrontar o alinhamento utilizado com o caminho hidráulico disponível e conferir manualmente os conteúdos dos tanques envolvidos, comparando-os com os dados remotos e com a distribuição prevista. A comunicação defeituosa permite que carga entre no slop de bombordo, portanto a divergência não pode ser atribuída automaticamente à instrumentação. Se a conferência confirmar a distribuição prevista, mas divergir das leituras remotas, há inconsistência na indicação; se confirmar conteúdo em destinos não previstos, o inventário real difere do representado. Deve-se evitar esse coletor para transferência de carga enquanto persistir a condição defeituosa. Com o inventário confirmado e corrigido no programa, a sequência revisada de transferência e lastro deve ser simulada, incluindo condições transitórias e esforços estruturais. Uma condição final aparentemente aceitável não valida uma sequência baseada em inventário incorreto.

### Sistema de ancoragem, manutenção e monitoramento da posição

**facil · medido ? · REPROVADA: autonomia**  
_Nota(s): Gestão das cargas de amarração e resposta à falha de linhas em mau tempo_

**P:** Na resposta operacional declarada em um caso analisado pela HSE do Reino Unido, qual conduta estava prevista para a falha de uma linha de ancoragem e quais critérios condicionavam a retomada das operações?

**R:** A conduta declarada era cessar imediatamente as operações. A retomada dependia de qual linha havia falhado, das condições meteorológicas presentes e futuras e da conformidade com os parâmetros de projeto.

**media · medido média · APROVADA**  
_Nota(s): Gestão das cargas de amarração e resposta à falha de linhas em mau tempo_

**P:** Uma unidade enfrenta uma tempestade sem utilizar o recurso disponível de ajuste das tensões de amarração, e os limites máximos operacionais dos guinchos não estão prontamente disponíveis na sala de controle. Como essas duas deficiências contribuem para o risco de exceder as tensões permitidas?

**R:** Não utilizar o ajuste de tensões deixa de aplicar uma medida preventiva prevista para adequar a amarração às condições ambientais severas. A indisponibilidade dos limites na sala de controle retarda a obtenção da referência necessária para verificar e respeitar a tensão máxima operacional dos guinchos. Em conjunto, essas deficiências prejudicam a gestão das tensões durante a tempestade e podem contribuir para exceder os valores permitidos. Qualquer ajuste deve seguir procedimento escrito e não ultrapassar o limite operacional dos guinchos.

**dificil_A · medido difícil · APROVADA**  
_Nota(s): Critérios de dimensionamento e verificação de linhas e fundações de ancoragem sob cargas estáticas, dinâmicas e de avaria_

**P:** Um FPSO utiliza ancoragem Taut-Leg, com linhas bastante inclinadas ligadas a estacas torpedo, transmitindo componentes horizontais e verticais relevantes às fundações. A verificação proposta considera apenas a magnitude da carga máxima estática com todas as linhas intactas, embora exista a possibilidade de ruptura de uma linha. Essa verificação é suficiente para aprovar as fundações? Indique as verificações necessárias, o mecanismo resistente que tende a governar e por que deve ser empregada análise por elementos finitos.

**R:** Não. É necessário avaliar as condições estática e dinâmica, tanto com as linhas intactas quanto com uma linha rompida, aplicando os fatores de segurança correspondentes ao regime e à condição de integridade. Também devem ser verificados os efeitos das cargas cíclicas e transitórias sobre a resistência do solo e a resposta estrutural das estacas, evitando deformações excessivas e vibrações na unidade. Na configuração Taut-Leg descrita, a elevada componente vertical faz com que a capacidade ao arrancamento axial tenda a governar o dimensionamento. A magnitude da resultante, isoladamente, não demonstra a adequação da fundação, pois a direção da carga também influencia o mecanismo de falha. Como as estacas torpedo recebem carregamento combinado horizontal-vertical, sua capacidade deve ser avaliada por elementos finitos, considerando essa combinação de componentes.

**dificil_B · medido difícil · APROVADA**  
_Nota(s): Monitoramento integrado de posição da unidade, resposta estrutural e integridade de risers/linhas; Impacto do offset e dos movimentos da unidade amarrada na integridade de risers; Station keeping: tendências e indicadores além do offset para detectar degradação antes da perda de posição_

**P:** Um FPSO amarrado, com risers rígidos, permanece dentro do limite operacional de offset, isto é, afastamento da posição de referência. Entretanto, sob determinadas combinações de vento e ondas, os movimentos da unidade aumentam e as deformações medidas no topo dos risers indicam esforços oscilatórios fora das faixas-limite. A equipe propõe manter a condição operacional porque o limite de posição não foi ultrapassado. Essa justificativa é suficiente ou a avaliação deve ser ampliada, e quais evidências devem orientar a decisão?

**R:** A justificativa não é suficiente: offset aceitável não assegura integridade dos risers. Os esforços oscilatórios podem produzir compressão localizada acima do admissível durante parte do ciclo, causando flambagem local, grandes curvaturas e cargas flexionais, com possível dano imediato e aceleração da fadiga. Os sinais estruturais fora das faixas-limite devem, portanto, orientar a avaliação da ameaça e das medidas de mitigação, sem esperar uma excedência de posição.

A avaliação deve integrar dados ambientais medidos, movimentos da unidade, inclinações e deformações dos risers, com análise de tendências e limites de alarme. Para avaliar fadiga, é necessário considerar magnitudes e ocorrência dos carregamentos, não apenas máximos de offset. Também não se deve usar a posição aceitável para descartar falha de linha de ancoragem, pois ela pode não produzir alteração imediatamente perceptível na excursão. Assim, é preciso distinguir solicitação estrutural local de possível degradação da ancoragem, apoiando a decisão em indicadores complementares e dados confiáveis.

## Operações submarinas, poços, risers e equipamentos submarinos

### Operações submarinas, poços, manifolds, PLEM e PLET

**facil · medido fácil · APROVADA**  
_Nota(s): Monitoramento operacional, envelope de segurança e gestão de integridade em sistemas subsea de poços e linhas associadas_

**P:** O que significa operar um sistema submarino dentro do envelope de segurança e qual tratamento operacional deve ser dado a um desvio desse envelope?

**R:** Significa manter o sistema submarino dentro dos limites de operação definidos no projeto. Um desvio desses limites deve ser registrado e investigado pelo operador, que deve gerar, implementar e documentar medidas para minimizar sua recorrência.

**media · medido difícil · APROVADA**  
_Nota(s): Monitoramento operacional, envelope de segurança e gestão de integridade em sistemas subsea de poços e linhas associadas_

**P:** O histórico de manutenção das barreiras de um poço permite identificar tendências de falhas e mostra uma relação muito baixa entre tarefas preventivas e corretivas. Como essas informações devem ser utilizadas para revisar as frequências de intervenção em uma estratégia de manutenção baseada em risco?

**R:** O operador deve usar as tendências do histórico e a relação entre tarefas preventivas e corretivas como critérios para reavaliar as frequências e periodicidades de manutenção, podendo empregar uma matriz de avaliação de risco. A relação muito baixa é um sinal para revisão, mas não determina, isoladamente, um novo intervalo: o ajuste deve considerar a avaliação de risco e as tendências observáveis. As frequências e periodicidades resultantes devem ser definidas e documentadas pelo operador.

**dificil_A · medido difícil · APROVADA**  
_Nota(s): Uso de VOR/ROV versus mergulho em inspeção e intervenção de linhas submarinas_

**P:** Uma demanda em linha submarina prevê vistoriar a condição externa de um trecho aparente e acessível e, caso seja necessário, executar seu reparo. Há mergulhadores disponíveis, mas a visibilidade da água varia com a maré e a presença de particulados. A equipe propõe tratar toda a demanda como inspeção por mergulho, aguardando apenas uma melhora da visibilidade. Como deve ser definido o recurso para cada etapa e por que essa proposta é insuficiente?

**R:** O escopo deve ser separado entre vistoria e reparo. O mergulho pode atender à vistoria da condição externa na porção aparente e acessível, condicionado à visibilidade da água; sua disponibilidade não elimina essas limitações de cobertura e execução. Se houver necessidade de reparo, a atividade passa a ser intervenção em linha, associada a sistemas operados por veículo de operação remota (VOR/ROV), assim como expansão e outras intervenções. Portanto, aguardar melhor visibilidade pode favorecer a vistoria por mergulho, mas não justifica enquadrar o reparo como inspeção nem atribuir toda a demanda ao mesmo recurso.

**dificil_B · medido difícil · APROVADA**  
_Nota(s): Instalação, fabricação e controle operacional do sistema submarino: integridade, rastreabilidade e envelope de segurança; Monitoramento de vazamentos, restrições de fluxo e anomalias de integridade em linhas e equipamentos submarinos; Gestão de integridade, fadiga e resposta a anomalias em risers e sistemas submarinos_

**P:** Uma linha entre manifold submarino e separador de um FPSO apresenta aumento de queda de pressão anos após o comissionamento, com mudanças simultâneas na razão gás-líquido e no teor de água. A inspeção identifica dano no revestimento, mas não determina sua origem; os registros de lançamento e a rastreabilidade dos materiais estão incompletos. Próximo ao fim da vida de projeto, a equipe propõe atribuir o dano ao envelhecimento e autorizar a extensão de vida porque não foi confirmado vazamento. Como conduzir o diagnóstico e decidir sobre essa proposta?

**R:** Não autorizar a extensão de vida apenas pela ausência de vazamento confirmado nem atribuir automaticamente o dano ao envelhecimento. Primeiro, comparar a queda de pressão com uma referência compatível com vazão líquida, razão gás-líquido e teor de água, pois essas variáveis influenciam a resposta hidráulica. Confrontar a inspeção atual com documentos as built, isto é, registros do sistema efetivamente construído, rastreabilidade de materiais e registros de tensão no lançamento. Esses elementos ajudam a investigar uma possível origem na instalação; lacunas documentais não comprovam degradação operacional. Direcionar inspeções aos mecanismos pertinentes, revestimento, corrosão, proteção catódica e condições do leito marinho. Para sustentar a extensão de vida, realizar a avaliação formal de integridade e segurança; na insuficiência de dados, empregar inspeções adicionais, modelagem numérica avançada e dados conservadores. Como boa prática de gestão, priorizar a anomalia e definir inspeção intensificada ou reparo até seu encerramento técnico. Manter a operação dentro do envelope de segurança e registrar, investigar e tratar qualquer desvio desses limites.

### Sistema e operação de pull in de risers

**facil · medido fácil · APROVADA**  
_Nota(s): Sequência operacional do pull-in do topo do riser entre PLSV e unidade flutuante_

**P:** Por que se instala uma ferramenta no topo de um riser rígido lançado por Reel-Lay ou J-Lay antes do pull-in, e qual é o papel dos cabos de aço nessa etapa?

**R:** A ferramenta viabiliza a transferência do topo do riser da embarcação de lançamento para a unidade flutuante onde será conectado. A manobra normalmente utiliza cabos de aço que interligam o riser à embarcação de lançamento, permitindo realizar essa transferência.

**media · medido ? · REPROVADA: suporte**  
_Nota(s): Sequência operacional do pull-in do topo do riser entre PLSV e unidade flutuante_

**P:** Na preparação da transferência do topo de um riser para um FPSO, a embarcação de lançamento de linhas (PLSV) ainda não atingiu a condição de máxima aproximação prevista no procedimento. Quais pontos do procedimento devem orientar essa etapa e essa condição permite iniciar a transferência?

**R:** Devem ser observados o posicionamento do PLET, estrutura de terminação da linha submarina, e a máxima aproximação do PLSV ao FPSO. Esta última corresponde à aproximação máxima do topo do riser prevista antes de começar sua transferência. Portanto, a transferência ainda não deve ser iniciada: é necessário atender à condição de aproximação estabelecida no procedimento e observar o posicionamento do PLET previsto para a instalação.

**dificil_A · medido média · APROVADA**  
_Nota(s): Posicionamento e controle de heading do FPSO na interface com turret, risers e umbilicais_

**P:** Dois FPSOs permanecem conectados ao fundo do mar por risers e umbilicais: um possui turret à vante e orientação passiva por weathervaning; o outro possui turret aproximadamente a meio do casco e controle ativo por thrusters. A operação requer correções comandadas de heading (aproamento) e posição, em vez de depender do alinhamento natural da unidade. Um operador propõe tratar as arquiteturas como funcionalmente equivalentes porque ambas permitem giro sem perder as conexões submarinas. Essa equivalência é válida para o requisito operacional e qual arquitetura o atende?

**R:** Não. A função comum do turret é permitir o giro do FPSO mantendo as conexões por risers e umbilicais, mas isso não torna equivalentes os modos de posicionamento. Na arquitetura passiva, a unidade se orienta por weathervaning em torno do turret à vante. Para realizar correções comandadas de aproamento e posição, a arquitetura compatível é a ativa, com thrusters e posicionamento dinâmico (DP). Nesse sistema, o controle utiliza informações dos sensores e ajusta a direção e a potência dos thrusters, integrando geração de potência e propulsão. Portanto, preservar as conexões durante o giro é função do turret; corrigir ativamente aproamento e posição é função do sistema de posicionamento ativo.

**dificil_B · medido difícil · APROVADA**  
_Nota(s): Interfaces críticas entre turret, amarração e risers durante aproximação, pull-in e operação conectada em FPSOs; Perda de posição ou de heading em FPSO com turret: cadeia causal até torção de amarrações, contato com risers e enquadramento como elemento crítico de segurança; Perda de posição, amarração e proteção de risers em operações de pull in sob mau tempo_

**P:** Durante o pull-in de risers em um FPSO com turret e controle de proa por propulsores, ocorrem perdas recorrentes de heading, corrigidas pouco depois, enquanto o vento aumenta. A posição permanece dentro dos limites operacionais, mas o turret não acompanha livremente a reorientação do casco. A equipe propõe continuar porque o espaçamento inicial entre amarrações e risers é amplo, embora a frente de trabalho esteja ficando exposta ao tempo pelo bordo. Qual decisão operacional é mais adequada e como distinguir um desvio recuperável do início de uma ameaça à integridade dos risers?

**R:** Suspender preventivamente o pull-in para avaliar a resposta integrada do controle de proa, do turret e das amarrações, além de controlar a exposição do trabalho pelo bordo ao tempo. A recuperação momentânea da heading e a posição dentro dos limites não bastam para justificar continuidade: é necessário verificar se a reorientação ocorre sem acumular torção e sem comprometer a separação entre amarrações e risers. Um desvio recuperável não implica automaticamente contato. Entretanto, vento crescente e ausência de livre giro do turret indicam possibilidade de evolução para torção das amarrações; em condição extrema, sem liberação do giro do turret, elas podem alcançar os risers. O espaçamento inicial reduz a probabilidade de contato, mas não exclui esse mecanismo extremo. Se houver perda de posição fora dos limites operacionais, considerar o abortamento, e não tratar o evento como simples oscilação de controle.

## Produção e Processo (Medição Fiscal e Sistema de Alívio)

### Compressão de Gás

**facil · medido fácil · APROVADA**  
_Nota(s): Controle operacional e sensibilidade dos compressores às condições do gás em sistemas offshore_

**P:** Qual é a função do compressor no condicionamento do gás destinado a gás combustível, gas lift, exportação ou reinjeção em uma planta offshore?

**R:** O compressor transfere ao gás a energia recebida de um acionador, como motor ou turbina, elevando sua pressão e/ou densidade. Assim, aumenta a energia do escoamento para encaminhar o gás aos destinos previstos na planta.

**media · medido média · APROVADA**  
_Nota(s): Controle operacional e sensibilidade dos compressores às condições do gás em sistemas offshore_

**P:** Em um trem de compressão offshore, a pressão de sucção oscila e a vazão de sucção de um estágio se afasta do setpoint correspondente à rotação da máquina. Como a variação de rotação, o estrangulamento na sucção e o reciclo por estágio diferem na correção dessas condições?

**R:** A variação de rotação atua para manter a pressão de sucção sem grandes oscilações. O estrangulamento na sucção é uma estratégia alternativa de manutenção dessa pressão, impondo uma restrição por válvula; no arranjo considerado, ela fica a jusante do separador de entrada de baixa pressão. Já o reciclo por estágio ajusta a vazão de sucção para aproximá-la do setpoint, que depende da rotação da máquina. Portanto, rotação e estrangulamento atuam no controle da pressão de sucção, enquanto o reciclo corrige o desvio de vazão de cada estágio em relação à referência associada à rotação.

**dificil_A · medido média · APROVADA**  
_Nota(s): Influência das pressões de sucção e de descarga na aplicação e no controle operacional da compressão de gás_

**P:** Um trem de compressão de gás apresenta instabilidade, com pressão baixa na sucção e pressão de descarga dentro da condição operacional esperada. A equipe considera investigar a condição do sistema, alterar a estratégia de controle ou substituir o compressor por outro tipo. Qual deve ser a prioridade e o que essas observações permitem concluir sobre a causa?

**R:** Priorizar a investigação da condição operacional na sucção, utilizando a pressão baixa como entrada para identificação, diagnóstico e definição da ação corretiva no controle do trem. O desvio está localizado na admissão, e não na descarga; portanto, a instabilidade não deve ser tratada apenas como um sintoma genérico. Essas observações identificam a variável anormal, mas não demonstram, por si só, falha da estratégia de controle ou inadequação do tipo de compressor. Alterar o controle ou substituir a máquina não deve anteceder o diagnóstico orientado pelo desvio de pressão.

**dificil_B · medido difícil · APROVADA**  
_Nota(s): Inspeção em revisões de compressores centrífugos e mitigação de vibração/pulsação em tubulações associadas; Arquiteturas de selagem em compressores multestágio e controle de vazamentos; Vibração e pulsação em compressores e tubulações associadas: mecanismos, danos, fadiga e mitigação_

**P:** Um compressor centrífugo multistágio de um FPSO entra em revisão após aumento de vazamento pela selagem e histórico de vibração elevada nas linhas conectadas, com afrouxamento de conexões. Na abertura da carcaça, aparecem marcas de contato nos labirintos, enquanto a tubulação apresentava vibração transversal e radial da parede. A equipe propõe retirar imediatamente o rotor, substituir os selos danificados e reforçar os suportes das linhas. Qual linha de diagnóstico deve ser priorizada antes dessas intervenções, e por que a proposta pode ser insuficiente?

**R:** Priorizar a investigação da vibração como possível causa do dano de selagem, sem assumir que os selos sejam a origem do problema. Antes de remover o rotor, observar o estado do rotor, dos difusores e dos planos de junta e medir as folgas entre partes fixas e móveis, preservando evidências que se perdem com a desmontagem. Interpretar essas evidências junto ao comportamento vibratório: vibração anormal do eixo pode provocar contato e danificar labirintos; nas linhas, a resposta lateral e a vibração radial da parede envolvem comportamentos distintos, e o afrouxamento pode contribuir para liberação de gás. Investigar fonte, transmissão e resposta estrutural, distinguindo causas mecânicas de excitação por pulsação ou acústica. Substituir selos e reforçar suportes pode tratar consequências sem controlar a excitação dominante. A suportação deve restringir vibração transversal sem impedir dilatação térmica axial, mas não substitui a investigação da causa.

### Medição Fiscal de óleo, medição fiscal de gás e transferência de custódia em operações de offloading

**facil · medido fácil · APROVADA**  
_Nota(s): Comunicação de falhas do sistema de medição e efeitos regulatórios sobre não conformidade e recálculo da produção_

**P:** Qual é a função da notificação de falha do sistema de medição na avaliação regulatória da confiabilidade dos dados de produção de petróleo e gás?

**R:** A notificação formaliza a ocorrência técnica como um gatilho para a avaliação regulatória dos dados de produção informados pelo concessionário. Ela pode dar origem a um processo de recálculo da produção, conectando a falha do sistema à fiscalização da veracidade dos volumes declarados. Quando se constata não conformidade dos dados, são instaurados procedimentos de recálculo.

**media · medido média · APROVADA**  
_Nota(s): Comunicação de falhas do sistema de medição e efeitos regulatórios sobre não conformidade e recálculo da produção_

**P:** Uma concessionária não registrou notificações de falha do sistema de medição, mas uma inspeção identificou não conformidade nos dados de produção. A ausência de notificação impede a abertura de um processo de recálculo? Justifique indicando os principais gatilhos desses processos.

**R:** Não. A inspeção também pode originar um processo de recálculo, e a constatação de não conformidade dos dados leva à instauração dos procedimentos correspondentes. Os principais gatilhos são notificações de falha do sistema de medição, inspeções, declarações das concessionárias, denúncias e validação da produção. Portanto, a notificação de falha não é condição necessária para a abertura desses processos.

**dificil_A · medido difícil · APROVADA**  
_Nota(s): Configuração do sistema de medição para transferência de custódia em offloading de FPSO e variáveis para cálculo do volume compensado_

**P:** No planejamento da medição de transferência de custódia de um FPSO, a monitoração online completa de vazão, pressão e temperatura exige investimento que a equipe considera economicamente injustificado. Propõe-se manter a medição de vazão existente e limitar a instrumentação adicional à pressão estática na parede do duto e à temperatura do escoamento. Outra equipe defende que somente a monitoração online completa permitiria calcular o volume compensado. Qual decisão é tecnicamente defensável e quais consequências ela traz para a estratégia de medição?

**R:** É defensável limitar a instrumentação adicional à medição direta de pressão estática e temperatura quando o investimento em monitoração online completa não se justifica. Essas duas medições devem permanecer na estação, pois integram o conjunto requerido como base do cálculo do volume compensado; portanto, não cabe tratar a monitoração online completa como requisito indispensável em todos os casos. A economia de investimento, porém, implica limitar a monitoração automática em tempo real das três variáveis. A estratégia deve reconhecer essa limitação, sem equiparar a configuração reduzida à monitoração online completa. A decisão econômica não autoriza eliminar pressão estática ou temperatura necessárias ao cálculo compensado.

**dificil_B · medido difícil · APROVADA**  
_Nota(s): Projeto, configuração e instalação do sistema de medição fiscal; Calibração, incerteza e rastreabilidade metrológica dos sistemas de medição fiscal de óleo; Requisitos metrológicos e configuração do sistema de medição fiscal e de transferência de custódia_

**P:** Uma linha de medição fiscal de óleo de um FPSO apresenta desvio persistente em relação ao volume esperado pela operação, sem indicação de falha no medidor principal. Após uma alteração na tubulação, não foi demonstrada a preservação das condições geométricas consideradas na calibração; o certificado disponível apresenta fator de calibração rastreável, mas os ensaios utilizaram óleo com viscosidade e densidade diferentes das atuais. Uma equipe propõe corrigir apenas a instalação, enquanto outra considera o certificado suficiente para aceitar os volumes. Que diagnóstico e critérios de aceitação devem orientar a decisão, distinguindo a contribuição da instalação daquela da calibração?

**R:** Nenhuma das propostas, isoladamente, sustenta a aceitação dos volumes. O diagnóstico deve avaliar duas contribuições que podem coexistir:

• Instalação: confrontar trechos retos, diâmetro, espessura e rugosidade com as exigências aplicáveis e as condições consideradas no dimensionamento e na calibração. A alteração pode comprometer o resultado mesmo sem indicação de falha do medidor.

• Calibração: verificar a similaridade entre ensaio e operação quanto a vazão, pressão, temperatura, viscosidade e densidade. Um fator rastreável não demonstra, sozinho, desempenho nas condições atuais; a rastreabilidade estabelece a cadeia de comparações, não substitui a representatividade do ensaio.

A aceitação exige demonstrar a adequação da instalação e da calibração ao uso, com incerteza do processo estimada e registrada antes da comprovação metrológica e aprovação. Se a representatividade não estiver demonstrada, será necessária calibração em condições muito similares às de campo. Corrigir apenas a tubulação não resolve essa lacuna, assim como recalibrar não dispensa verificar a instalação.

### Operação de Separadores Trifásicos

**facil · medido fácil · APROVADA**  
_Nota(s): Controle coordenado de nível e interface nas saídas líquidas do separador trifásico_

**P:** Qual é a função da válvula instalada na linha inferior de água livre de um separador trifásico e qual variável comanda sua abertura?

**R:** A válvula regula a vazão de descarga da água livre pelo fundo do separador. Sua abertura é comandada pelo controle do nível de interface água-óleo, relacionando a retirada de água à posição dessa interface, e não apenas ao nível total de líquido.

**media · medido média · APROVADA**  
_Nota(s): Controle coordenado de nível e interface nas saídas líquidas do separador trifásico_

**P:** Em um separador trifásico horizontal, a pressão permanece controlada, mas o nível de óleo e a interface água-óleo se afastam dos respectivos valores de controle. Como as válvulas de saída de óleo e água devem atuar para regular as descargas e manter os níveis necessários à separação?

**R:** A válvula de saída de óleo deve ter sua abertura ajustada pelo controlador de nível de óleo, enquanto a válvula inferior de água deve responder ao controlador de interface água-óleo. Essas atuações regulam as vazões de descarga correspondentes para manter o inventário líquido e a posição da interface nos valores de controle. A saída de água não deve ser comandada apenas pelo nível total de líquido. A pressão continua sendo regulada separadamente pela saída de gás no topo.

**dificil_A · medido difícil · APROVADA**  
_Nota(s): Gestão de integridade de vasos em operação no FPSO: corrosão, inspeção, cadastro de ativos e isolamento para intervenção_

**P:** Um separador trifásico de um FPSO passou a operar em condições de processo fora do envelope de projeto. As inspeções periódicas estão em dia e não há vazamento identificado, mas o plano de inspeção permanece baseado nas condições anteriores. A equipe propõe manter o plano até surgir evidência de dano. Qual decisão sobre o regime de inspeção é tecnicamente mais adequada e por que os argumentos apresentados não bastam para manter o plano?

**R:** Revisar o regime de inspeção diante do desvio do envelope de projeto e reforçar a avaliação baseada em risco, sem necessariamente abandonar as inspeções periódicas. Mudanças nas condições reais de processo constituem perigo potencial de perda de contenção e podem gerar cenários que exigem prevenção, detecção e mitigação. Portanto, inspeções em dia e ausência de vazamento não demonstram que o plano concebido para as condições anteriores continua adequado. O sistema de integridade pode combinar inspeção prescritiva e inspeção baseada em risco; a revisão deve avaliar os cenários associados às novas condições e adequar o regime de inspeção ao risco identificado, em vez de aguardar manifestação de dano.

**dificil_B · medido difícil · APROVADA**  
_Nota(s): Formação de espuma, efeitos operacionais e mitigação no separador trifásico; Controle de níveis e da interface óleo-água em separadores trifásicos: como faixa estreita, espuma, nível alto e variações térmicas degradam a separação; Shutdown e intertravamentos na operação de separadores trifásicos_

**P:** Após uma mudança no fluido produzido, um separador trifásico apresenta controle de nível instável, alarmes de nível alto e indícios de líquido na saída de gás para os compressores. Alguns alarmes desaparecem antes da confirmação do inventário líquido, e a equipe propõe classificá-los como falha de instrumentação para evitar shutdowns. Qual diagnóstico e prioridade operacional são mais consistentes, considerando a relação entre separação, controle de nível e proteção?

**R:** Não é consistente concluir que os alarmes sejam falha de instrumentação apenas porque desaparecem. A espuma é uma causa provável: impurezas ou características do óleo podem favorecer sua formação; ela ocupa volume útil, dificulta o controle de nível, reduz a área de escoamento do gás e aumenta o arraste de líquido. Além disso, pode acionar chaves de alarme e parada mesmo sem aumento equivalente do inventário de líquido claro. Deve-se distinguir essa condição de nível líquido efetivamente muito alto, que também favorece arraste; os mecanismos podem coexistir. A prioridade é tratar o risco de líquido alcançar os compressores e considerar os alarmes como possível manifestação real do processo, não como evidência suficiente de defeito. A cadeia de proteção deve contemplar alarme antes da parada de emergência. Para enfrentar a causa, quando a formação de espuma for previsível, o separador deve possuir interno de remoção com tempo e superfície coalescedora suficientes; corrigir apenas a indicação de nível não elimina a perda de volume útil nem o arraste.

### Operação de Tratadores Eletrostáticos

**facil · medido média · APROVADA**  
_Nota(s): Acoplamento entre o tratador eletrostático e a carga ao sistema de água produzida_

**P:** Por que a avaliação do desempenho do tratador eletrostático deve considerar também a carga de óleo enviada ao tratamento de água produzida, e não apenas a qualidade do óleo exportado?

**R:** Porque o óleo que segue pela corrente aquosa constitui carga para o tratamento de água produzida. Esse sistema precisa enquadrar a água para sua destinação e tem uma condição de projeto para a concentração de óleo na entrada. Assim, atender à especificação do óleo exportado não basta se a corrente aquosa receber cargas de óleo bruto com baixa diluição, incompatíveis com o projeto do tratamento de água.

**media · medido média · APROVADA**  
_Nota(s): Acoplamento entre o tratador eletrostático e a carga ao sistema de água produzida_

**P:** O óleo exportado permanece dentro da especificação, mas há indícios de desvio de separação no conjunto separador trifásico–tratador eletrostático e chegada de óleo bruto com baixa diluição ao tratamento de água produzida. Sabendo que esse sistema foi projetado para receber cerca de 1000 ppm de óleo disperso na saída do separador, como interpretar a piora da qualidade da água?

**R:** A piora deve ser relacionada à mudança da carga recebida pelo tratamento de água: óleo bruto com baixa diluição não corresponde à condição de projeto de cerca de 1000 ppm de óleo disperso. Portanto, a conformidade do óleo exportado não elimina o problema na corrente aquosa. Os indícios apresentados apontam para uma carga de entrada incompatível com o projeto, que compromete o enquadramento da água para sua destinação, e não apenas para uma questão de qualidade do óleo exportado.

**dificil_A · medido média · APROVADA**  
_Nota(s): Metas de qualidade do óleo tratado: BS&W e salinidade para exportação no contexto do tratador eletrostático_

**P:** Em um FPSO, os fluidos de vários poços são misturados antes do processamento, e o separador de produção apresenta boa separação primária. O óleo segue para um tratador eletrostático, mas ainda não foi confirmado o atendimento simultâneo às especificações de temperatura, salinidade e BS&W (teor de água e sedimentos). A equipe propõe considerar o óleo pronto para exportação com base no desempenho do separador. Essa decisão é tecnicamente justificável?

**R:** Não. A boa separação primária não comprova, por si só, que o blend produzido esteja estabilizado e enquadrado para exportação. Nesse arranjo, o tratamento prossegue no tratador eletrostático, cuja função é enquadrar o BS&W. Além disso, o enquadramento desse parâmetro não basta para demonstrar o atendimento das demais condições de exportação: temperatura e salinidade também precisam estar dentro das especificações aplicáveis. Portanto, a decisão deve se apoiar na qualidade final do blend tratado e no atendimento simultâneo dessas condições, e não apenas no desempenho do separador ou na qualidade de uma corrente isolada.

**dificil_B · medido difícil · APROVADA**  
_Nota(s): Pré-lavagem com água livre separada no condicionamento da emulsão antes do tratador eletrostático; Operação de tratadores eletrostáticos: pré-lavagem, dessalinização e intensificação da coalescência conforme o teor de água; Metas de qualidade do óleo tratado: BS&W e salinidade para exportação no contexto do tratador eletrostático_

**P:** Em um FPSO, a salinidade do óleo tratado deixa de atender à especificação de exportação, enquanto o BS&W (teor de água e sedimentos) aumenta moderadamente. O tratador permanece energizado e possui entrada inferior distribuída, pré-lavagem com água livre separada e uma região posterior de campo mais intenso. Há suspeita de alteração da distribuição interna, mas a equipe propõe concentrar a investigação apenas na etapa elétrica. Qual deve ser a prioridade do diagnóstico para recuperar o atendimento conjunto de BS&W e salinidade, e por que a energização não basta para descartar uma falha de condicionamento?

**R:** Priorizar a verificação da distribuição da alimentação e do contato efetivo com a água livre de pré-lavagem, preservando a sequência entre condicionamento inicial e tratamento eletrostático. A pré-lavagem remove sais e partículas e promove a coalescência de parte das gotas dispersas; sua deterioração pode comprometer simultaneamente a remoção de contaminantes e a redução inicial da água dispersa. Nessa configuração, a redução progressiva da água aproxima a mistura dos eletrodos, intensificando o campo entre as interfaces e favorecendo separações adicionais. Portanto, manter o equipamento energizado não demonstra que essa sequência esteja funcionando adequadamente, nem justifica restringir o diagnóstico à etapa elétrica. A recuperação deve ser avaliada pelo atendimento simultâneo de BS&W e salinidade, sem considerar a corrente enquadrada apenas pela melhora de um desses parâmetros; a temperatura também integra as condições de exportação.

### Operação Geral FPSO

**facil · medido fácil · APROVADA**  
_Nota(s): Sistema logístico offshore e flexibilidade do FPSO no escoamento por alívio_

**P:** Qual é a finalidade da logística de apoio offshore para a continuidade operacional de uma unidade marítima?

**R:** Atender a unidade marítima com os insumos e equipamentos necessários à continuidade operacional, integrando o fluxo de materiais e informações entre fornecedores nacionais e internacionais, armazéns e terminais portuários.

**media · medido média · APROVADA**  
_Nota(s): Sistema logístico offshore e flexibilidade do FPSO no escoamento por alívio_

**P:** Em uma locação pioneira, prevê-se operar um FPSO com armazenamento de óleo a bordo e exportação por alívio, evitando infraestrutura submarina dedicada ao escoamento. Como esse arranjo altera a necessidade de linhas de exportação, oleodutos e manifolds submarinos?

**R:** Nesse arranjo, a capacidade de armazenar o óleo a bordo e exportá-lo por alívio permite dispensar linhas de exportação, oleodutos e manifolds submarinos destinados a esse escoamento. Essa flexibilidade torna a solução conveniente para a locação pioneira nas condições apresentadas.

**dificil_A · medido difícil · APROVADA**  
_Nota(s): Tratamento de água produzida como mitigação de perdas operacionais em FPSO_

**P:** Um FPSO opera em um campo maduro com elevada produção de água. O hidrociclone e o flotador ficam inoperantes, e a eficiência de separação óleo-água diminui. A equipe propõe manter a operação sem reavaliar a capacidade de tratamento, por considerar que o problema se limita à qualidade da separação. Essa decisão é tecnicamente justificável? Explique por que essa condição pode impor uma restrição operacional à unidade.

**R:** Não é justificável manter a operação sem reavaliar a capacidade de tratamento frente à demanda atual. A inoperância do hidrociclone e do flotador reduz a capacidade de separação óleo-água: o primeiro separa gotículas por diferença de inércia no escoamento em vórtice, enquanto o segundo remove microgotículas residuais por borbulhamento de gás e coalescência. Portanto, a queda de eficiência não é um problema isolado de qualidade, mas evidencia perda de capacidade funcional da linha de tratamento. Com elevada produção de água, essa capacidade reduzida pode ser incompatível com a demanda corrente e tornar o tratamento uma restrição à operação. É necessário verificar essa compatibilidade e avaliar a recuperação ou otimização das etapas, em vez de presumir que a unidade pode manter o mesmo desempenho operacional.

**dificil_B · medido difícil · APROVADA**  
_Nota(s): Confiabilidade das medições e aderência dos dados à realidade operacional no monitoramento de FPSO; Confiabilidade das informações operacionais para controle do processo e conformidade em FPSO; Diagnóstico de desvios operacionais e falhas de instrumentação/automação em FPSO_

**P:** Em um FPSO sob controle manual, uma anomalia persiste entre turnos, sem medição de vazão e com indicação online de teor de óleos e graxas (TOG) não confiável. O cadastro identifica um tanque como contendo óleo, mas os registros de recebimento mostram água com alto TOG. A passagem de serviço omite mudanças operacionais, os operadores não sabem localizar os limites seguros e mensagens que exigem ação em tempo restrito são tratadas como eventos rotineiros. Antes de atribuir a anomalia à perda de desempenho do processo, qual diagnóstico deve orientar a investigação e quais verificações devem ser priorizadas?

**R:** Deve-se reconhecer primeiro a perda de observabilidade da planta, sem concluir que ela exclui um desvio real de processo. A ausência de vazão e a baixa confiabilidade do TOG impedem acompanhar adequadamente o desempenho; o cadastro incorreto induz a interpretar o inventário como um fluido diferente do recebido. A passagem de serviço incompleta perpetua premissas divergentes entre equipes, enquanto o desconhecimento dos limites seguros compromete o julgamento da condição operacional. Na supervisão, tratar como evento uma indicação que exige ação em tempo restrito mascara sua urgência. Priorizar a obtenção de medições confiáveis, confrontar o cadastro com os registros de recebimento e transferência e assegurar passagem de serviço escrita com mudanças e condições operacionais. Identificar e disponibilizar os limites seguros aos operadores e revisar a classificação das mensagens: alarmes exigem ação em tempo restrito; eventos apenas registram mudanças sem exigir ação. Essas verificações fornecem a base para distinguir desvio real de interpretação enganosa.

### Produção, processo e processamento do óleo

**facil · medido média · APROVADA**  
_Nota(s): Inspeção e prontidão operacional de vasos, trocadores, filtros e tubulações_

**P:** Por que a inspeção interna de vasos, trocadores, filtros e tubulações deve verificar tanto a integridade dos componentes quanto a presença de contaminantes antes da entrada em serviço ou do carregamento do leito?

**R:** Porque são verificações complementares: a condição dos componentes não substitui a avaliação da contaminação interna. Nos vasos destinados a leitos de zeólitas, devem ser verificadas descontinuidades do refratário que possam comprometer o isolamento térmico ou criar caminhos preferenciais para o gás, além de umidade excessiva e água líquida. Nos filtros, devem ser verificadas a montagem dos internos conforme projeto e a preservação e integridade dos elementos. Nos trocadores e nas linhas de utilidades, devem ser procurados sólidos e depósitos; nas tubulações, também resíduos de corrosão. Assim, a inspeção abrange tanto a condição dos componentes quanto a presença de materiais indesejados no sistema.

**media · medido ? · REPROVADA: correcao_tecnica, suporte, escopo**  
_Nota(s): Inspeção e prontidão operacional de vasos, trocadores, filtros e tubulações_

**P:** Antes da partida de um sistema de desidratação de gás natural, são encontrados resíduos sólidos e depósitos no feixe, no casco e nas linhas de entrada de utilidades de um trocador de calor. Como esses achados devem ser considerados na avaliação da prontidão e do desempenho do equipamento, mesmo sem histórico de operação contínua?

**R:** Esses achados são relevantes já na preparação para operação: a inspeção deve verificar resíduos sólidos e depósitos no feixe, no casco e nas linhas de entrada de utilidades, sem depender de um histórico de operação contínua. Portanto, a avaliação não deve se limitar ao feixe nem desconsiderar a contaminação das demais regiões. Entretanto, a identificação de resíduos e depósitos, isoladamente, não permite determinar o mecanismo nem quantificar uma eventual perda de desempenho térmico; ela estabelece a condição de contaminação interna que precisa ser considerada na avaliação de prontidão.

**dificil_A · medido difícil · APROVADA**  
_Nota(s): Separação primária e estabilização do óleo no trem de processo de FPSO_

**P:** Em um FPSO, o óleo permanece instável na saída do trem de processamento. Durante períodos de golfadas, a vazão enviada pelo primeiro separador aos estágios seguintes oscila; porém, mesmo nos períodos de alimentação regular, o óleo continua fora da condição de estabilização requerida. Como diferenciar os dois mecanismos e direcionar a avaliação, considerando seus efeitos sobre o restante da planta?

**R:** A oscilação transmitida aos estágios seguintes durante as golfadas indica amortecimento insuficiente no primeiro separador: sua função de tanque pulmão é receber vazão flutuante e regularizar a alimentação a jusante. Deve-se avaliar essa função, pois sua deficiência mantém os próximos equipamentos sujeitos às flutuações de carga. Já a persistência de óleo instável com alimentação regular indica que as golfadas não explicam sozinhas o problema. É necessário avaliar a remoção dos componentes voláteis nos separadores em série e a necessidade de adição de calor nos pontos apropriados do trem. Esse mecanismo afeta diretamente o condicionamento do óleo para seu destino, enquanto o amortecimento insuficiente afeta a regularidade da alimentação dos estágios posteriores. Portanto, a avaliação deve abranger ambos: regularizar a vazão não substitui a estabilização, e remover voláteis não substitui a função de tanque pulmão.

**dificil_B · medido difícil · APROVADA**  
_Nota(s): Dessalgação do óleo: mecanismo, integração com a desidratação e impacto na qualidade de exportação; Recirculação de água separada quente dos tratadores eletrostáticos e sua interface com o header de produção; Incrustação mineral por carbonatos no topside: efeito de temperatura, pH, despressurização e suporte à mitigação por modelagem de mistura de águas_

**P:** Em um FPSO, o óleo tratado mantém salinidade elevada, e a operação propõe aumentar a recirculação de água separada quente dos tratadores eletrostáticos para aquecer a alimentação do coletor de produção. O sistema utiliza água de lavagem na dessalgação e apresenta aquecimento, aumento de pH e despressurização no processamento primário. A equipe de integridade teme incrustação carbonática, enquanto a operação considera o reforço térmico suficiente para corrigir a qualidade do óleo. Que decisão técnica deve orientar essa alteração, conciliando remoção de sais e controle de incrustação?

**R:** A alteração deve ser condicionada à avaliação conjunta da dessalgação/desidratação e da mistura de águas no topside, não aprovada apenas pelo benefício térmico nem rejeitada automaticamente pelo risco de incrustação. Para reduzir o sal, é necessário verificar o contato da água de lavagem com o óleo e a efetiva coalescência, decantação e remoção da fase aquosa contaminada; aumentar o aquecimento não substitui essa remoção. Em paralelo, temperatura e pH elevados reduzem a solubilidade dos carbonatos, e a despressurização com liberação de CO₂ integra as condições do mecanismo de incrustação. Deve-se avaliar a mistura de águas mais crítica nas condições propostas para apoiar a seleção e a dosagem do inibidor. A recirculação pode ter baixo efeito sobre a criticidade, enquanto a água de diluição pode reduzir a severidade de forma predominante; esses resultados precisam ser verificados para o novo cenário, sem generalização.

### Produtos químicos

**facil · medido fácil · APROVADA**  
_Nota(s): Coagulantes, floculantes e condicionamento químico da emulsão óleo-em-água na água produzida para descarte offshore_

**P:** Como os floculantes atuam sobre as gotas de óleo em uma emulsão óleo-em-água na água produzida?

**R:** Os floculantes adsorvem na interface das gotas de óleo e podem atuar por neutralização de cargas e/ou formação de pontes inter-particulares. Esses mecanismos favorecem a agregação das gotas e de matéria poluente em flocos maiores.

**media · medido média · APROVADA**  
_Nota(s): Coagulantes, floculantes e condicionamento químico da emulsão óleo-em-água na água produzida para descarte offshore_

**P:** Após o condicionamento químico da água produzida, observa-se a formação de agregados maiores antes da flotação. Por que essa mudança favorece a separação subsequente e qual é a diferença entre o papel do produto químico e o da flotação ou decantação?

**R:** A formação de agregados maiores favorece a separação porque eles são mais facilmente flotáveis ou decantáveis. O produto químico promove a agregação por mecanismos como neutralização de cargas e/ou formação de pontes inter-particulares, preparando a corrente para a separação. A flotação ou decantação realiza a remoção física dos agregados; portanto, o condicionamento químico facilita, mas não substitui, essa etapa.

**dificil_A · medido difícil · APROVADA**  
_Nota(s): Compatibilidade da água de injeção com a formação e mitigação de incrustações por sulfatos_

**P:** Em um campo offshore com injeção de água do mar, a água produzida passa a apresentar fração crescente de água injetada. Nesse período, surgem restrições de escoamento na coluna de produção e nas linhas de superfície. A equipe propõe descartar a incompatibilidade entre águas porque os sintomas não estão limitados ao reservatório. Essa avaliação é tecnicamente adequada, considerando o momento e os locais de aparecimento das restrições?

**R:** Não. A hipótese de incompatibilidade entre águas com formação de sulfatos é consistente tanto com o momento quanto com os locais dos sintomas. A chegada da água injetada ao produtor caracteriza o breakthrough, a partir do qual os problemas de incrustação se tornam mais sérios. Sob condições termodinâmicas adequadas, o contato entre água de formação e água de injeção pode formar sulfatos insolúveis de bário, estrôncio e cálcio. A precipitação de sais inorgânicos pode afetar a coluna de produção e as linhas e equipamentos de superfície, portanto sua ocorrência fora do reservatório não exclui essa hipótese. Entretanto, a coincidência temporal e espacial não confirma, por si só, que as restrições sejam depósitos de sulfatos: a interpretação depende da composição das águas e das condições de contato. O poço deve ser monitorado continuamente após o breakthrough.

**dificil_B · medido difícil · APROVADA**  
_Nota(s): Controle químico de corrosão e de H2S em linhas e equipamentos do processamento de óleo; Compatibilidade entre produtos químicos e efeitos cruzados no desempenho do tratamento em FPSOs; Ensaios e monitoramento de desempenho e compatibilidade de produtos químicos em FPSOs_

**P:** Em um FPSO, uma linha de aço carbono AISI 1020 apresenta redução de H2S após a introdução de glioxal em baixo pH, sem depósitos salinos, mas os indicadores de corrosão pioram. A equipe propõe manter o sequestrante e adicionar um inibidor de poliol fosfato, apoiando-se em resultados favoráveis do inibidor sem os demais aditivos utilizados na linha. Como decidir se essa proposta oferece proteção efetiva, distinguindo a corrosividade introduzida pelo tratamento de uma possível perda de desempenho da combinação química?

**R:** Não aprovar o pacote apenas pela redução de H2S, ausência de depósitos ou desempenho individual do inibidor. O glioxal em baixo pH pode tornar o meio corrosivo ao AISI 1020; portanto, o próprio tratamento é uma hipótese para a piora. O poliol fosfato pode proteger por adsorção e estabilização do filme de óxido, além de dificultar o acesso de espécies agressivas, mas sua eficácia não deve ser presumida para qualquer combinação. Comparar, em ensaios representativos do meio e do material da linha, o tratamento com sequestrante, o inibidor e o pacote completo com os demais aditivos, avaliando a corrosão e possíveis efeitos antagônicos. Resultados favoráveis em outro aço ou matriz não validam automaticamente essa aplicação. Condicionar a continuidade do pacote à demonstração de proteção na combinação real e à confirmação por monitoramento das taxas de corrosão nos trechos críticos, sem generalizar uma indicação favorável obtida em apenas um ponto.

### Sistema de Alívio e Flare

**facil · medido fácil · APROVADA**  
_Nota(s): Comissionamento, testes funcionais, handover e capacitação operacional em sistemas de alívio, despressurização e flare_

**P:** Qual é a função do comissionamento na transição entre construção e operação de sistemas de alívio e flare, e por que são utilizados checklists nessa etapa?

**R:** O comissionamento verifica, inspeciona e testa os componentes físicos e, em seguida, confirma o funcionamento dos processos antes do início pleno da operação, permitindo identificar e eliminar erros de implantação. Os checklists asseguram que todos os componentes previstos no projeto sejam contemplados nos testes e que estejam disponíveis e operacionais conforme o projeto detalhado para a futura operação.

**media · medido média · APROVADA**  
_Nota(s): Comissionamento, testes funcionais, handover e capacitação operacional em sistemas de alívio, despressurização e flare_

**P:** Um pacote fornecido por fabricante para o sistema de flare está em comissionamento, mas os operadores e técnicos que assumirão sua operação e manutenção não participam das atividades. Por que envolvê-los diretamente nos trabalhos junto ao fornecedor melhora a preparação para receber esse pacote?

**R:** A participação ativa no comissionamento junto ao pessoal do fornecedor permite que operadores e técnicos adquiram familiaridade e conhecimento prático sobre o equipamento. Isso melhora sua preparação para operá-lo e mantê-lo após a entrega, reduzindo o risco de receberem o pacote com conhecimento prático limitado, mesmo que os testes de vazamento e de funcionamento tenham sido realizados.

**dificil_A · medido difícil · APROVADA**  
_Nota(s): Radiação térmica, dispersão e ignição segura em sistemas de flare e vent_

**P:** Em uma plataforma offshore, a avaliação do flare identifica radiação térmica não admissível em uma área com equipamentos e circulação de pessoas, além de possibilidade de gás não ignitado alcançar o convés de processo sob determinadas direções de vento. A equipe propõe manter o arranjo e liberar gás durante a partida até conseguir o acendimento, argumentando que a capacidade de alívio está adequada. Como esses resultados devem orientar a decisão sobre o arranjo e o procedimento de partida?

**R:** A capacidade de alívio adequada não resolve os riscos identificados. A verificação do arranjo deve considerar a área exposta à radiação não admissível e o convés de processo vulnerável à nuvem de gás. Para avaliar a exposição térmica, devem ser considerados os parâmetros de emissão e geometria da chama e a posição dos pontos de interesse, usando os resultados para orientar a revisão do arranjo. O procedimento de partida deve incorporar os cenários de dispersão e considerar a velocidade e a direção do vento durante a ignição. Não deve prever liberação prolongada de gás não queimado enquanto se tenta obter o acendimento. Assim, a decisão deve tratar tanto a exposição com a tocha acesa quanto o risco de dispersão antes da ignição, sem considerar a capacidade de alívio como critério suficiente.

**dificil_B · medido difícil · APROVADA**  
_Nota(s): Influência da contrapressão e do arranjo de descarga na seleção da PSV; Capacidade do sistema de flare, blowdown e vent frente a eventos combinados de sobrepressão; Dimensionamento e verificação dinâmica de PSV com interação com o sistema coletor de alívio_

**P:** Em um FPSO, uma válvula de segurança e alívio de pressão (PSV) convencional foi aprovada por simulação dinâmica de um evento isolado, com contrapressão fixa na descarga. Durante um evento combinado de alívio e despressurização, várias válvulas descarregam no mesmo coletor do flare, a contrapressão aumenta e a pressão dos equipamentos permanece elevada além do previsto. A equipe propõe aumentar o orifício da PSV ou substituí-la por uma balanceada, mantendo o sistema receptor inalterado. Qual diagnóstico deve orientar a revisão e por que essas soluções não podem ser aprovadas apenas com a verificação isolada da válvula?

**R:** O diagnóstico prioritário é a interação entre as descargas simultâneas e a contrapressão do coletor, sem concluir de imediato que o orifício é insuficiente. A descarga de uma válvula pode elevar a contrapressão e alterar a pressão de abertura das demais; portanto, a aprovação com contrapressão fixa não demonstra adequação ao evento combinado. É necessário avaliar a capacidade do coletor e do flare para combinações críveis e verificar dinamicamente a PSV sob as condições de descarga correspondentes. O critério é que, após a abertura, a pressão se estabeleça abaixo ou igual à pressão de projeto, adotando o cenário que exigir maior área. A válvula balanceada reduz a influência da contrapressão sobre seu funcionamento, mas isso não comprova capacidade suficiente do sistema receptor. Aumentar o orifício só se justifica se a avaliação integrada demonstrar área insuficiente; superdimensionamento pode provocar chatter, isto é, oscilação rápida da válvula, e danos. A solução deve preservar simultaneamente o desempenho das válvulas e a capacidade da rota de descarte.

### Sistema de captação e tratamento de água do mar para injeção no reservatório

**facil · medido fácil · APROVADA**  
_Nota(s): Monitoramento microbiológico e indicadores de biofouling, MIC e souring em água do mar para injeção_

**P:** Como a dosagem de sulfato, a presença de H₂S, o potencial de oxirredução (Eh) e o pH são utilizados na identificação da atividade de bactérias redutoras de sulfato (BRS) em ensaios laboratoriais de biorredução de sulfato?

**R:** A dosagem de sulfato, o teste qualitativo de H₂S e as medidas de Eh e pH são utilizados em conjunto para identificar a atividade associada às BRS e confirmar sua presença nas condições desses ensaios.

**media · medido média · APROVADA**  
_Nota(s): Monitoramento microbiológico e indicadores de biofouling, MIC e souring em água do mar para injeção_

**P:** Em um duto de água do mar para injeção, há íons ferrosos (Fe²⁺), oxigênio disponível e bactérias oxidantes de ferro e de nitrito. Como a atividade dessas bactérias pode contribuir simultaneamente para o entupimento do duto e para a formação de condições anaeróbias?

**R:** A atividade dessas bactérias está associada à oxidação de Fe²⁺ a Fe³⁺, processo que pode causar entupimento do duto. Simultaneamente, o consumo do oxigênio disponível pelos microrganismos favorece o estabelecimento de condições anaeróbias. Assim, a atividade microbiana pode contribuir tanto para a obstrução quanto para a mudança das condições de oxigenação do sistema.

**dificil_A · medido difícil · APROVADA**  
_Nota(s): Qualidade da água de injeção, compatibilidade com o reservatório e prevenção de incrustação em sistemas de água do mar de FPSO_

**P:** Em um FPSO, a injetividade diminui após uma mudança na composição da água de injeção, e a inspeção identifica depósitos salinos e corrosão localizada por pitting. As análises da água não mostram aumento de sólidos suspensos, população bacteriana ou corrosividade em relação à condição anterior. A avaliação da mistura com a água de formação, baseada nas composições químicas e no equilíbrio termodinâmico, indica precipitação de sais pouco solúveis. Qual mecanismo deve ser priorizado no diagnóstico, frente às hipóteses de deposição de sólidos, atividade bacteriana e corrosividade da água, e como orientar a seleção do tratamento?

**R:** Priorizar a incompatibilidade química entre a água de injeção e a água de formação, com precipitação de sais e formação de incrustações. A previsão de precipitação e os depósitos salinos sustentam esse diagnóstico: as incrustações podem reduzir a permeoporosidade e favorecer pitting, portanto a corrosão observada não exige que a corrosividade da água seja a causa principal. Nas condições apresentadas, não há evidência de aumento dos outros fatores que justifique priorizá-los sobre a incompatibilidade. Orientar o tratamento pela avaliação da compatibilidade com a formação e pela previsão de incrustações, utilizando as composições químicas e o equilíbrio termodinâmico para apoiar a seleção do tipo e da quantidade de inibidores. Manter o monitoramento para detectar deterioração da qualidade e permitir correções antes de danos severos.

**dificil_B · medido difícil · APROVADA**  
_Nota(s): Seleção da fonte de captação e projeto físico do sistema de água do mar para injeção em FPSOs; Ciclo operacional da filtração e retrolavagem do leito em sistemas de água do mar para injeção; Garantia hidráulica de vazão e pressão no sistema de água de injeção_

**P:** Em um FPSO, a água captada apresenta aumento de sólidos e turbidez durante movimentos de embarcações, acompanhado de ciclos mais curtos de filtração. Nas retrolavagens, a oferta de água salgada tratada diminui e a vazão para as bombas de injeção oscila, especialmente quando também cai a disponibilidade de água produzida. A equipe propõe atuar apenas no vaso de injeção para estabilizar a pressão. Qual diagnóstico e prioridade de intervenção distinguem a causa primária da limitação hidráulica e permitem sustentar a alimentação da injeção?

**R:** Priorizar a avaliação da captação e da recuperação dos filtros, sem limitar a intervenção ao vaso. A seleção da captação deve considerar sólidos, turbidez causada por embarcações e estabilidade da qualidade; a deterioração observada aponta para uma contribuição da origem da água. A retenção de partículas obstrui progressivamente o leito e reduz sua eficiência, justificando a retrolavagem com água filtrada em sentido inverso e o encaminhamento do efluente concentrado ao tratamento de despejos industriais. No cenário, as oscilações coincidentes com a menor oferta de água tratada indicam também uma limitação de alimentação, e não demonstram, isoladamente, falha das bombas. Avaliar conjuntamente a reposição por água salgada tratada quando cai a água produzida e a capacidade do vaso de manter pressão constante para as bombas. Estabilizar a pressão trata a manifestação hidráulica, mas não remove os sólidos acumulados nem corrige a qualidade da captação.

### Sistema de drenagem aberta e fechada

**facil · medido fácil · APROVADA**  
_Nota(s): Filosofia de alarmes e intertravamentos de proteção em sistemas de drenagem/processo_

**P:** Qual é a diferença entre a função de um alarme operacional e a de um intertravamento instrumentado de proteção em um sistema de drenagem ou processo offshore?

**R:** O alarme operacional alerta que uma variável atingiu os limites de operação normal, dando ao operador oportunidade de corrigir o desvio antes do nível de disparo da proteção. O intertravamento instrumentado executa a ação protetiva automaticamente, sem depender de resposta manual do operador. Portanto, o alarme complementa a proteção, mas não substitui sua atuação automática.

**media · medido média · APROVADA**  
_Nota(s): Filosofia de alarmes e intertravamentos de proteção em sistemas de drenagem/processo_

**P:** Durante a operação de um sistema de drenagem offshore, um técnico aplica um override, isto é, uma inibição da função de proteção, por uma interface homem-máquina remota, sem conhecimento da sala de controle, autorização ou avaliação apropriada. Por que essa condição representa risco operacional e qual controle deve ser exigido?

**R:** A inibição pode deixar a função de proteção indisponível sem que a sala de controle conheça ou tenha avaliado essa condição. Isso caracteriza aplicação fora de controle, comprometendo a gestão da proteção. O override deve ser submetido a um processo controlado, com conhecimento do operador da sala de controle, autorização e avaliação apropriadas da indisponibilidade temporária da função.

**dificil_A · medido difícil · APROVADA**  
_Nota(s): Arranjo do sistema de drenagem aberta e fechada e gestão de integridade de linhas internas a tanques, headers e vasos de drenagem_

**P:** Durante o descomissionamento de um FPSO, um trecho de drenagem que atravessa tanques e se conecta à descarga para o mar (overboard) deixou de receber efluentes, mas ainda não foi segregado das demais linhas. A equipe propõe retirá-lo do plano de inspeção por estar inoperante e adiar seu isolamento. Essa decisão é tecnicamente justificável? Explique quais condições devem orientar a gestão da mudança.

**R:** Não. A ausência de recebimento de efluentes não elimina os riscos associados à integridade das linhas internas aos tanques enquanto permanecem interligadas. Devem ser considerados retorno de gás ao convés, transferência de carga entre tanques e vazamento de óleo para o mar. A gestão da mudança deve avaliar essas interligações e as condições de integridade para definir a mitigação, incluindo o isolamento necessário à segregação do trecho. Até que essa segregação seja efetivada, não se justifica excluir as tubulações internas dos tanques da rotina de inspeção e manutenção apenas por estarem inoperantes. Se testes ou manutenções identificarem falhas, devem ser abertas ordens corretivas, com planejamento e execução compatíveis com o risco e a complexidade.

**dificil_B · medido difícil · APROVADA**  
_Nota(s): Planejamento e governança dos testes de comissionamento em sistemas de drenagem aberta e fechada; Limpeza, flushing, drenagem, teste de estanqueidade e preservação de linhas e vasos de drenagem antes da entrada em serviço; Inspeção e limpeza de selos e pontos de bloqueio em sistemas de drenagem aberta e fechada_

**P:** Nos primeiros dias após a partida de um FPSO, o sistema de drenagem apresenta escoamento irregular e suspeita de perda de segregação nos selos líquidos. A inspeção encontra escória em um coletor e um selo sem integridade, embora o sistema tenha sido formalmente liberado. O dossiê registra testes físicos, mas não comprova flushing, drenagem dos pontos baixos nem teste funcional do processo; após a preparação, o sistema permaneceu vazio por duas semanas, sem registro de preservação. A equipe propõe apenas desobstruir o coletor e tratar o selo como manutenção rotineira. Qual deve ser a prioridade técnica para corrigir o desvio e avaliar sua origem?

**R:** Priorizar a recuperação do escoamento e da integridade do selo, mas não encerrar o evento como simples manutenção rotineira. A obstrução compromete a drenagem; o selo não íntegro compromete a segregação e a barreira contra migração de gás. Em paralelo, investigar a preparação e a liberação: verificar evidências de limpeza/flushing, drenagem dos pontos baixos, remoção de água residual e preservação com ar seco ou nitrogênio durante a espera. A escória é compatível com detritos que deveriam ter sido removidos antes da entrada em serviço, enquanto a ausência de registros não comprova, isoladamente, que essas etapas foram omitidas. Revisar a cobertura dos checklists e os procedimentos aprovados e atualizados, além de verificar o funcionamento do processo após as correções. A liberação baseada em testes físicos não substitui essa verificação funcional. Acompanhar os desvios na operação assistida, distinguindo pendências introduzidas no comissionamento de problemas efetivamente surgidos na rotina operacional.

### Tratamento de água produzida para descarte

**facil · medido fácil · APROVADA**  
_Nota(s): Separação primária gravitacional e condicionamento inicial da água produzida em FPSO_

**P:** Qual é a função dos tanques de slop no tratamento da água de produção em um FPSO?

**R:** Os tanques de slop recebem a água de produção para tratamento e posterior descarte. Em FPSO, um ou dois tanques originais do navio podem ser dedicados a essa finalidade, integrando o sistema de tratamento da água.

**media · medido média · APROVADA**  
_Nota(s): Separação primária gravitacional e condicionamento inicial da água produzida em FPSO_

**P:** Em um FPSO, a água produzida passa a ser tratada em tanques de decantação de maiores dimensões e com maior tempo de repouso. Qual tendência se espera para a eficiência da separação gravitacional e essa mudança, por si só, garante água apta ao descarte?

**R:** A eficiência da separação gravitacional tende a aumentar com as maiores dimensões dos tanques e o maior tempo de repouso. Entretanto, essa melhoria não garante, por si só, água apta ao descarte: a corrente ainda pode apresentar elevada concentração de hidrocarbonetos e exigir uma etapa adicional de tratamento.

**dificil_A · medido difícil · APROVADA**  
_Nota(s): Hidrociclones no tratamento de água produzida para intensificação da separação óleo-água_

**P:** Em um trem de tratamento de água produzida, o limite operacional de óleo disperso na alimentação dos hidrociclones é 1000 mg/L. Após uma piora da qualidade da água na saída desse estágio, a concentração na entrada passou a superar esse limite, enquanto a alimentação tangencial pressurizada permaneceu nas mesmas condições anteriores. Qual hipótese deve orientar a investigação inicial: arraste de óleo a montante ou perda das condições hidráulicas nos hidrociclones, e por quê?

**R:** A investigação inicial deve priorizar o arraste de óleo a montante, com possível sobrecarga dos hidrociclones. A concentração de entrada ultrapassou a condição prevista para esse trem, e deficiências na separação a montante podem comprometer o tratamento subsequente. Já a manutenção das condições de alimentação tangencial pressurizada não indica, por si, perda do mecanismo hidráulico que gera o campo centrífugo de separação. Portanto, a piora na saída não deve ser atribuída automaticamente a uma falha dos hidrociclones: deve-se investigar primeiro a qualidade da corrente entregue pelos separadores, sem considerar definitivamente excluída uma deficiência no próprio estágio.

**dificil_B · medido difícil · APROVADA**  
_Nota(s): HAZOP como estrutura de diagnóstico de falhas no tratamento de água produzida; Falhas de medição e controle da interface óleo/água e seu efeito no arraste de óleo para a água produzida; Diagnóstico de ineficiência em equipamentos de tratamento da água produzida_

**P:** Em um FPSO, a água produzida apresenta teor de óleos e graxas (TOG) elevado e só se enquadra após múltiplas passagens pelo tratamento. A interface do tratador permanece indicada na faixa operacional de 60–70%, mas seu medidor por empuxo, instalado em tubo externo (standpipe), apresenta resposta lenta e histórico de descalibração; o tratamento subsequente tem desempenho limitado para gotas pequenas e óleo emulsionado. A equipe propõe aumentar a recirculação por considerar a indicação de interface normal. Como estruturar um HAZOP (análise de perigos e operabilidade) para decidir se essa proposta trata a causa ou apenas compensa o sintoma, e qual verificação priorizar?

**R:** Priorizar a verificação da confiabilidade da medição de interface: uma indicação dentro da faixa não demonstra controle adequado quando o instrumento apresenta descalibração e atraso. Sem sinais confiáveis, tanto o controle quanto o diagnóstico ficam comprometidos.

Usando o diagrama de fluxo, separar os nós de separação primária e tratamento subsequente, definir seus comportamentos esperados e aplicar palavras-guia aos parâmetros. No primeiro nó, investigar desvios de interface, distinguindo erro ou atraso de medição de descontrole real; relacionar causas ao possível arraste de óleo, ao sensor e aos atuadores associados ao controle. No segundo, investigar o desvio de TOG elevado, confrontando a forma do óleo recebido com as limitações para gotas pequenas e emulsões.

Se houver descontrole de interface, a ação deve tratar sua causa, não apenas aumentar as passagens. Se a interface estiver efetivamente controlada e a carga apresentar características incompatíveis com o desempenho da tecnologia, múltiplas passagens são compatíveis com essa limitação. Definir ações conforme consequências e severidade; o sintoma final, isoladamente, não distingue as hipóteses.

### Tratamento do Gás produzido

**facil · medido fácil · APROVADA**  
_Nota(s): Desidratação do gás por glicóis e condicionamento para evitar hidratos, condensação e danos a jusante_

**P:** Qual é a função da desidratação do gás produzido e como a remoção de água protege as linhas e os equipamentos a jusante?

**R:** A desidratação retira água da corrente de gás pressurizada. Essa remoção evita a formação de hidratos e reduz a água disponível para condensação, protegendo as linhas e os equipamentos a jusante contra a deterioração associada à presença de condensado aquoso.

**media · medido difícil · APROVADA**  
_Nota(s): Desidratação do gás por glicóis e condicionamento para evitar hidratos, condensação e danos a jusante_

**P:** Uma unidade offshore utiliza absorção com trietilenoglicol (TEG), mas uma alteração nas condições de pressão e temperatura a jusante exige menor teor residual de água no gás. Como comparar a manutenção da absorção com glicol com a adoção de peneiras moleculares, considerando a logística offshore e a nova especificação?

**R:** A absorção com glicol é frequente offshore porque o uso de absorventes líquidos facilita a logística de manuseio. Entretanto, essa vantagem não substitui o atendimento à especificação de umidade. As peneiras moleculares permitem teor residual de água menor que o obtido com TEG e devem ser consideradas quando a exigência de secagem se torna mais severa. A escolha deve levar em conta a especificação requerida e as condições de pressão e temperatura às quais o gás será submetido; a manutenção do glicol depende de sua capacidade de atender a essa exigência.

**dificil_A · medido difícil · APROVADA**  
_Nota(s): Modos operacionais A, B e C de plataformas com membranas de remoção de CO₂ e seus efeitos sobre exportação, injeção e gás combustível_

**P:** Uma plataforma opera com plena disponibilidade das membranas de remoção de CO₂, mas uma restrição operacional reduz o tratamento a apenas parte do gás produzido. A equipe propõe manter a exportação máxima e, caso o tratamento fique totalmente indisponível, considera que o gás combustível das turbinas continuará com teor de CO₂ reduzido. Como corrigir esse planejamento, relacionando cada condição de disponibilidade ao modo operacional, ao balanço entre exportação e injeção e à conclusão sustentada sobre o gás combustível sem tratamento?

**R:** Com disponibilidade plena, a plataforma opera no modo B, utilizando integralmente a remoção de CO₂ e permitindo exportação máxima. Com tratamento apenas parcial, deve operar no modo C, combinando exportação parcial e injeção parcial; portanto, não cabe manter a premissa de exportação máxima. Se as membranas ficarem totalmente indisponíveis, a configuração passa ao modo A: todo o gás contorna a remoção de CO₂, a exportação fica impedida e o volume deve ser encaminhado à injeção no reservatório. Quanto ao gás combustível, a conclusão explicitamente sustentada para o modo A é que, sem parcela tratada pelas membranas, o gás encaminhado às turbinas apresenta teor de CO₂ igual ao do petróleo oriundo dos poços, e não um teor reduzido pelo tratamento.

**dificil_B · medido difícil · APROVADA**  
_Nota(s): Desidratação e condicionamento do gás produzido para exportação ou reinjeção em FPSOs; Remoção de condensados no gás comprimido e proteção do sistema de compressão; Controle de líquido no gás a montante de peneiras moleculares: proteção do leito, desempenho de desidratação e confiabilidade da regeneração_

**P:** Em um FPSO, a desidratação por peneiras moleculares perde desempenho após um período de maior carga na compressão, com recuperação insuficiente após regeneração e indícios de má distribuição do gás no leito. Há líquido contendo água a jusante dos resfriadores, embora o vaso de segurança da sucção inicial esteja funcionando normalmente. A equipe propõe atuar apenas na regeneração, atribuindo a falha à saturação do adsorvente. Qual diagnóstico deve orientar a intervenção e qual barreira deve ser priorizada?

**R:** Deve-se investigar arraste de líquidos formados após o resfriamento e possível dano físico ao leito, em vez de assumir apenas saturação normal. O resfriamento entre estágios promove condensação; portanto, o vaso de segurança na sucção inicial não substitui a separação dos líquidos gerados posteriormente. A prioridade é verificar e restabelecer a retenção eficaz nos scrubbers e separadores após os resfriadores, antes que o líquido alcance a peneira, protegendo também os estágios seguintes de compressão. A água líquida pode solubilizar o ligante e formar aglomerados durante a regeneração, reduzindo a área superficial e criando caminhos preferenciais. Esse mecanismo explica conjuntamente a secagem deficiente, a má distribuição e a recuperação insuficiente após regeneração. Assim, atuar somente na regeneração não resolve a origem do arraste nem demonstra que a integridade do adsorvente foi preservada.

## Segurança Operacional, SGSO, Sistemas de Segurança e Gestão de Riscos

### Estudos de Segurança

**facil · medido fácil · APROVADA**  
_Nota(s): Bow-Tie e premissas para classificar risco e avaliar a efetividade de barreiras em estudos de segurança_

**P:** Como os lados esquerdo e direito de um diagrama Bow-Tie se relacionam com a árvore de falhas e a árvore de eventos?

**R:** O lado esquerdo corresponde à árvore de falhas e organiza as causas que podem levar ao evento principal. O lado direito corresponde à árvore de eventos e representa os possíveis desdobramentos e consequências a partir desse evento.

**media · medido média · APROVADA**  
_Nota(s): Bow-Tie e premissas para classificar risco e avaliar a efetividade de barreiras em estudos de segurança_

**P:** Em um FPSO, um cenário foi classificado pela pior consequência possível imediatamente após a liberação do perigo, com frequência calculada supondo barreiras disponíveis e operando conforme esperado. Se uma dessas barreiras ficar indisponível, como deve ser interpretada a classificação original e qual avaliação é necessária?

**R:** A classificação original representa o risco sob a premissa de disponibilidade e desempenho esperado das barreiras, considerando a pior consequência imediata após a liberação do perigo, e não os escalonamentos posteriores. Com a indisponibilidade de uma barreira, essa premissa deixa de ser atendida; portanto, a classificação não deve ser considerada automaticamente válida para a condição atual. É necessário reavaliar o cenário afetado e a frequência estimada, levando em conta a barreira indisponível, sem presumir que o risco permaneça igual.

**dificil_A · medido difícil · APROVADA**  
_Nota(s): Revisão periódica, atualização e validade dos estudos de segurança de FPSOs ao longo do ciclo de vida_

**P:** Um FPSO ainda está dentro do prazo de revisão periódica do safety case, mas recebeu uma mudança de processo com impacto identificado e apresenta indícios de fadiga e corrosão no casco e no topside. A equipe propõe aguardar a revisão programada porque ainda não demonstrou alteração da vida útil. Como decidir sobre a revisão, quais verificações e estudos adicionais devem subsidiá-la e como registrar o encaminhamento no sistema de gestão?

**R:** Não se deve aguardar apenas o prazo periódico: a mudança com impacto deve ser identificada e comunicada pelo sistema de gestão ou pelo gerenciamento de mudanças, acionando a revisão do safety case e estudos adicionais. Deve-se verificar se a configuração alterada e as condições de integridade preservam as premissas dos estudos, avaliando especialmente os efeitos da fadiga e da corrosão sobre a vida útil do casco e do topside. O programa de integridade deve permanecer alinhado ao safety case. Os estudos adicionais devem ser definidos conforme as premissas afetadas; se a alteração alcançar hipóteses de dispersão de gás e localização de detectores, propagação de incêndio ou proteção estrutural, os respectivos estudos devem integrar o escopo. Registrar a mudança, os impactos identificados, as premissas verificadas, o escopo dos estudos adicionais e a justificativa técnica do encaminhamento permite evidenciar a decisão e manter o controle da validade dos estudos.

**dificil_B · medido difícil · APROVADA**  
_Nota(s): Identificação e seleção de perigos e cenários acidentais com HAZID, HAZOP, What-if e FMEA/FMECA; Construção de cenários acidentais para liberações inflamáveis em estudos de segurança offshore; QRA/FERA: estrutura do estudo, escopo e critérios para seleção metodológica_

**P:** Na atualização dos estudos de um FPSO, a equipe propõe manter apenas o HAZID (identificação de perigos) e o What-if anteriores, pois ambos registram os principais perigos de liberação inflamável. Entretanto, o arranjo alterado inclui regiões parcialmente confinadas, e há incerteza sobre dispersão e ignição imediata ou retardada. A decisão envolve comparar medidas adicionais de redução de risco, considerando frequências e consequências, mas há pressão para limitar o esforço analítico. Qual encaminhamento metodológico permite sustentar essa decisão sem confundir cobertura dos perigos com suficiência dos cenários?

**R:** Não considerar o registro dos perigos suficiente para decidir sobre as medidas. Reavaliar a cobertura das áreas alteradas e selecionar técnicas complementares conforme o caso, com equipe multidisciplinar, aproveitando os estudos anteriores como base. Para as liberações inflamáveis, construir árvores de eventos antes de estimar efeitos físicos, diferenciando condições de vazamento, dispersão, tempo de ignição e confinamento; realizar estudo de dispersão para reduzir a incerteza sobre os desfechos plausíveis. Explicitar e justificar o nível qualitativo, semiquantitativo ou quantitativo pela profundidade necessária à decisão, e não apenas pelo esforço disponível. Como a comparação proposta depende de frequências e consequências e requer maior realismo dos incêndios, aprofundar quantitativamente esses cenários e integrar os resultados na avaliação de risco. A identificação qualitativa continua útil, mas não substitui esse aprofundamento. Assim, a comparação das medidas se apoia em cenários fisicamente fundamentados, em vez de hipóteses simplificadas que podem distorcer a decisão.

### Operações simultâneas – SIMOPS

**facil · medido fácil · APROVADA**  
_Nota(s): Governança de SIMOPS: papéis, cadeia de comando, reuniões e comunicação entre frentes_

**P:** Por que equipes contratadas de construção offshore precisam ser alertadas, por meio de seus supervisores, sobre operações simultâneas de produção, perfuração ou intervenção em poços (workover) com as quais possam interagir?

**R:** Porque essas equipes podem não estar familiarizadas com as operações de óleo e gás executadas simultaneamente à construção. O alerta identifica a operação específica com a qual o serviço pode interferir inadvertidamente e busca evitar consequências graves dessa interação não intencional.

**media · medido média · APROVADA**  
_Nota(s): Governança de SIMOPS: papéis, cadeia de comando, reuniões e comunicação entre frentes_

**P:** Durante uma construção offshore simultânea à produção, ocorre troca de turno do operador e substituição da equipe contratada; as atividades continuam podendo interferir entre si. Como essas mudanças podem degradar a coordenação das operações simultâneas (SIMOPS) e por que a comunicação entre as supervisões não deve se limitar ao início do projeto?

**R:** As trocas de turno e de equipe podem causar falhas de comunicação entre as supervisões, comprometendo a continuidade do entendimento sobre as interações entre construção e produção. Se a equipe deixar de conhecer essas interações, surge uma lacuna de controle que pode afetar o planejamento e as barreiras. Por isso, as linhas de comunicação entre a supervisão do operador e a da contratada devem permanecer claras durante todo o projeto, com atenção especial às trocas de turno e de equipe, e não apenas na mobilização inicial.

**dificil_A · medido difícil · APROVADA**  
_Nota(s): Condições anormais dinâmicas em SIMOPS: perda de posicionamento, perda de geração e transição para estado seguro_

**P:** Durante operações simultâneas em um navio, avaliam-se duas condições de emergência distintas. Na primeira, o agravamento ambiental aumenta a carga dos propulsores, e o sistema de posicionamento dinâmico (DP) deixa de manter rumo e posição, com deriva que ameaça a infraestrutura submarina conectada. Na segunda, ocorre perda da energia principal, sendo necessário recuperar um trim seguro e nivelado. Qual deve ser a prioridade operacional em cada condição, e por que uma mesma resposta não atende às duas?

**R:** Na perda de posicionamento, o aumento da carga dos propulsores associado à deriva e ao desvio de rumo caracteriza incapacidade de manter posição, justificando escalar o alerta de amarelo para vermelho. Com ameaça à infraestrutura submarina, a prioridade é iniciar a desconexão de emergência (EDS) para evitar danos potenciais, em vez de depender de um DP que já não mantém rumo e posição. Na perda de energia principal, a prioridade é preservar a capacidade de operar o lastro para conduzir o navio a um trim seguro e nivelado: uma ou mais bombas e o sistema completo de lastro devem permanecer operáveis pelo quadro de emergência alimentado pelo gerador de emergência. As respostas diferem porque a primeira enfrenta a perda de controle de posição e o risco à infraestrutura conectada; a segunda exige disponibilidade de energia de emergência para recuperar a condição segura pelo lastro.

**dificil_B · medido difícil · APROVADA**  
_Nota(s): Matriz operações versus barreiras como base para compatibilidade e restrições operacionais em SIMOPS; SIMOPS: como bypasses, intertravamentos e lógicas automáticas podem degradar simultaneamente disponibilidade e independência das barreiras; Impacto de alarmes, detecção de gás, intertravamentos e ESD na continuidade de SIMOPS_

**P:** Em um FPSO, uma partida e uma transferência foram liberadas como operações simultâneas (SIMOPS) pela matriz operações versus barreiras. Durante a partida, um bypass de manutenção, registrado como retirada apenas da proteção de baixa pressão (PSL), também desabilitou a proteção de alta pressão (PSH) do mesmo transmissor, sem atualização da matriz. Surge detecção de gás na sala de bombas, e a lógica automática coloca a ventilação do ambiente dos painéis elétricos em recirculação, elevando sua temperatura e ameaçando a geração que atende às duas frentes. A coordenação propõe desfazer essa ação para manter as atividades: qual decisão é tecnicamente justificável e quais premissas da liberação precisam ser revistas?

**R:** Não é justificável manter as duas frentes apenas pela compatibilidade registrada ou desfazer a ação automática apenas para preservar a geração. Deve-se suspender a combinação liberada e reavaliar sua continuidade com base nas barreiras efetivamente disponíveis e na resposta ao gás. O bypass retirou duas funções por uma única ação: não há apenas indisponibilidade de PSL, mas perda simultânea de proteções vinculadas ao mesmo instrumento. É necessário verificar o bypass mínimo necessário à partida e preservar PSH quando sua retirada for desnecessária. A detecção de gás deve orientar a resposta coordenada; o aquecimento dos painéis é um efeito secundário da lógica, não evidência de que o perigo inicial deixou de existir. Antes de reconfigurar a ventilação ou retomar as frentes, devem ser avaliados esses impactos cruzados e atualizada a matriz operações versus barreiras. Deixaram de valer as premissas de PSH disponível, de retirada limitada a PSL e de continuidade da utilidade compartilhada sob atuação automática.

### Segurança e Controle de Riscos

**facil · medido fácil · APROVADA**  
_Nota(s): Controle de fontes de ignição e proteção de equipamentos em áreas classificadas_

**P:** Por que equipamentos elétricos e eletrônicos podem atuar como fontes de ignição em atmosferas explosivas, tanto em operação normal quanto em falha?

**R:** Porque podem produzir arcos, faíscas e superfícies aquecidas capazes de inflamar gases ou vapores presentes. Essas fontes podem surgir no funcionamento normal, como no centelhamento durante a abertura e o fechamento de contatos, ou em condições de falha, com elevação de temperatura. Assim, o risco de ignição não se limita a equipamentos defeituosos.

**media · medido média · APROVADA**  
_Nota(s): Controle de fontes de ignição e proteção de equipamentos em áreas classificadas_

**P:** Em uma instalação elétrica de área classificada com possibilidade de atmosfera inflamável, a proteção contra sobretensão, sobrecorrente, falha de isolamento e aquecimento anormal apenas emite alarme, mantendo o circuito afetado energizado. Por que somente alarmar é insuficiente e como o seccionamento automático complementaria essa proteção?

**R:** Somente alarmar é insuficiente porque sinaliza a condição anormal, mas mantém a alimentação do circuito afetado, permitindo que a condição elétrica perigosa persista. Sobretensão, sobrecorrente, falha de isolamento e aquecimento anormal podem favorecer arcos, faíscas ou superfícies aquecidas capazes de inflamar a atmosfera presente. O seccionamento automático complementa o alarme ao interromper a alimentação do circuito afetado, reduzindo a possibilidade de essas condições evoluírem para uma fonte de ignição. Assim, sinalização e interrupção desempenham funções complementares na redução do risco.

**dificil_A · medido difícil · APROVADA**  
_Nota(s): Investigação de incidentes com identificação de causas imediatas, básicas e sistêmicas_

**P:** Em um FPSO, a investigação de um quase acidente durante manutenção identificou falha de isolamento, ausência de revisão das válvulas travadas abertas ou fechadas e não conformidades recorrentes em auditorias. Também constatou supervisão insuficiente e avaliação de riscos que não contemplava essas deficiências. A proposta inicial é advertir o executante e atualizar o registro da ocorrência. Que conjunto de ações corretivas e preventivas deve substituir essa proposta para tratar a cadeia causal e reduzir a recorrência?

**R:** O plano deve corrigir as deficiências das barreiras de isolamento e instituir a revisão das válvulas travadas abertas ou fechadas, em vez de tratar apenas a atuação do executante. Deve também rever a avaliação de riscos, o controle e a supervisão do trabalho, além do desenho das medidas de controle. O acompanhamento deve incluir monitoramento, revisão e auditoria dessas medidas, verificando se as não conformidades persistem e se os controles são eficazes na prática. As ações precisam estar vinculadas às causas imediatas, subjacentes e organizacionais identificadas. Advertência e atualização documental, isoladamente, não tratam as falhas de barreiras e de gestão que permitiram o quase acidente.

**dificil_B · medido difícil · APROVADA**  
_Nota(s): Lacunas de identificação de perigos por mudanças operacionais, interpretações locais e cenários não previstos; Gestão de mudanças, HRA e revisão de análises para condições não rotineiras; Avaliação de riscos em modos operacionais, transientes e condições anormais_

**P:** Durante o retorno ao serviço de um FPSO após manutenção, uma tarefa de desconexão revela sulfeto de hidrogênio (H₂S) aprisionado em um riser, perigo ausente da análise usada para liberar o trabalho. A equipe cumpriu a sequência prevista, mas a análise contemplava apenas a operação normal, e a configuração temporária não passou por gestão de mudanças. A supervisão propõe apenas reforçar as orientações à equipe e continuar. Qual diagnóstico e condição para continuidade são tecnicamente mais defensáveis?

**R:** O diagnóstico mais defensável é uma falha sistêmica de cobertura das análises, não um desvio de execução demonstrado: o perigo estava ausente da avaliação, embora a equipe tivesse seguido o procedimento. A identificação de H₂S aprisionado evidencia a lacuna, enquanto o uso de uma análise restrita à operação normal deixa o retorno ao serviço e a configuração temporária sem avaliação compatível. Antes de continuar, é necessário avaliar essa condição por gestão de mudanças, descrevendo e justificando a alteração, e revisar a identificação de perigos e a análise de riscos para o transiente, considerando os limites operacionais aplicáveis. Os procedimentos críticos envolvidos devem ser contemplados por análise de confiabilidade humana (HRA), mediante método consolidado. Reforçar orientações à equipe não substitui essa reavaliação nem demonstra que os riscos da condição real foram tratados.

### SGSO

**facil · medido fácil · APROVADA**  
_Nota(s): Planejamento do Plano de Emergência integrado à gestão de riscos e aos cenários acidentais_

**P:** Quais elementos mínimos o Plano de Emergência de um FPSO/FSO deve contemplar para estruturar a resposta aos cenários acidentais?

**R:** Deve contemplar identificação da instalação e do responsável legal; descrição dos acessos; cenários acidentais; sistemas de alerta; comunicação do acidente; estrutura organizacional de resposta; procedimentos de resposta; equipamentos e materiais de resposta; e procedimento para acionamento de recursos e estruturas de resposta complementares, quando aplicável.

**media · medido média · APROVADA**  
_Nota(s): Planejamento do Plano de Emergência integrado à gestão de riscos e aos cenários acidentais_

**P:** Na elaboração do Plano de Emergência de um FPSO, foram identificados cenários de incêndio e de vazamento de óleo. Existe um plano específico para vazamento de óleo definido pelo regulamento aplicável: quais desses cenários devem constar no Plano de Emergência da instalação e quais podem ser tratados somente no plano específico?

**R:** Os cenários de incêndio devem constar no Plano de Emergência da instalação, que deve contemplar os cenários acidentais e os elementos necessários à resposta. Os cenários decorrentes da hipótese de vazamento de óleo podem ser tratados somente no plano específico definido pelo regulamento aplicável. Essa possibilidade é específica para a hipótese de vazamento de óleo e não justifica retirar os cenários de incêndio do Plano de Emergência da instalação.

**dificil_A · medido difícil · APROVADA**  
_Nota(s): Identificação, classificação e governança dos Elementos Críticos de Segurança Operacional no SGSO_

**P:** Em um FPSO, auditorias sucessivas do Sistema de Gerenciamento da Segurança Operacional (SGSO) encontram novamente salvaguardas essenciais à prevenção de acidentes que não foram identificadas como Elementos Críticos de Segurança Operacional (ECSO). As equipes corrigiram as omissões apontadas anteriormente, mas novas verificações revelam o mesmo problema em outros sistemas. A gestão atribui os resultados a falhas isoladas de execução local. Qual diagnóstico é mais consistente com essas evidências e que direcionamento deve ser dado ao tratamento dos desvios?

**R:** As evidências indicam possível falha sistêmica na identificação dos ECSO, e não apenas erros locais: salvaguardas essenciais à prevenção de acidentes atendem ao critério de criticidade, mas continuam sendo omitidas em diferentes sistemas. A repetição após correções anteriores indica que o tratamento não teve abrangência eficaz. O direcionamento deve ser avaliar a consistência dos critérios de identificação e classificação no sistema de gestão, abrangendo equipamentos, sistemas e procedimentos críticos, em vez de apenas corrigir cada omissão encontrada. A disponibilidade e a integridade das salvaguardas devem alimentar monitoramento contínuo em nível gerencial adequado, com informações dos responsáveis. Se constatada falha recorrente do operador no gerenciamento dos elementos críticos, deve ser solicitado atestado de verificação de barreiras por organismo de terceira parte.

**dificil_B · medido difícil · APROVADA**  
_Nota(s): Capacitação, mudanças organizacionais e gestão de contratadas no SGSO em FPSOs; Gestão de mudanças de pessoas e capacitação para mudanças operacionais no SGSO; SGSO: efetividade de procedimentos operacionais depende de controle documental, recursos, treinamento e garantia da qualidade na execução_

**P:** Após reorganização de equipes em um FPSO, alguns operadores passaram a acumular funções temporariamente. Os procedimentos continuam atualizados e disponíveis, e os registros mostram treinamentos anteriores, mas verificações de campo revelam interpretações diferentes da mesma rotina e dúvidas sobre etapas críticas. A gestão propõe manter o arranjo porque não houve alteração do procedimento. No âmbito do Sistema de Gerenciamento da Segurança Operacional (SGSO), essa justificativa é suficiente? Qual diagnóstico e quais controles devem orientar a decisão?

**R:** Não. A conformidade documental não demonstra, sozinha, capacidade de execução segura. O acúmulo de funções deve ser tratado pelo gerenciamento de mudanças de pessoas, mesmo sem alteração do procedimento. As diferenças de execução e as dúvidas indicam que os registros anteriores não bastam para demonstrar capacitação adequada às funções atuais: a fragilidade está na ligação entre mudança de pessoas, competência e execução, não necessariamente na versão documental. A decisão deve considerar requisitos objetivos de capacitação por cargo, avaliação teórica e prática e reciclagem aplicável. É necessário verificar o entendimento das implicações da mudança e assegurar treinamento contínuo nos procedimentos, com reciclagem diferenciada para os críticos. A revisão da mudança com operação e manutenção para verificar esse entendimento é uma referência técnica de inspeção do HSE britânico, não uma exigência brasileira por essa origem. Por fim, devem ser aplicados requisitos de garantia da qualidade na execução, confirmando na prática que o procedimento é cumprido, em vez de aceitar apenas documentos vigentes e registros de treinamento.

### Sistema de Combate a Incêndio

**facil · medido fácil · APROVADA**  
_Nota(s): Barreiras passivas, divisórias e compartimentação corta-fogo_

**P:** Na proteção passiva contra incêndio de uma unidade offshore, como paredes e divisórias se comparam quanto ao nível relativo de proteção?

**R:** Paredes fornecem maior proteção contra incêndio do que divisórias.

**media · medido fácil · APROVADA**  
_Nota(s): Barreiras passivas, divisórias e compartimentação corta-fogo_

**P:** Em um FPSO, uma área será ampliada e terá sua configuração alterada, passando a abrigar uma ocupação diferente e um cenário de incêndio mais severo. Quais variáveis devem orientar a revisão do tipo, da localização e do projeto da barreira de proteção contra fogo?

**R:** A revisão deve considerar o tipo e a severidade do incêndio, o tamanho e a configuração da área protegida, além dos tipos de ocupação e dos níveis de perigo envolvidos. Assim, a ampliação e a mudança de configuração devem ser avaliadas juntamente com a nova ocupação e a maior severidade do incêndio para definir o tipo, a localização e o projeto da barreira.

**dificil_A · medido difícil · APROVADA**  
_Nota(s): Gestão de inspeção, manutenção e tratamento de desvios em sistemas de combate a incêndio no SGSO_

**P:** Em um FPSO, um elemento crítico do sistema de combate a incêndio apresentou desempenho inferior ao critério de aceitação em teste e permanece degradado. Foi aberta uma ordem de manutenção corretiva, mas sua prioridade não considera a criticidade do elemento. A equipe propõe aguardar o reparo usando uma medida temporária ainda sem aprovação ou controle formal. Quais decisões devem ser tomadas no Sistema de Gerenciamento da Segurança Operacional (SGSO) para tratar essa situação, e por que a ordem de manutenção não basta para controlar o risco residual?

**R:** O operador deve avaliar o resultado do teste e registrar uma conclusão sobre a condição do elemento com base no critério de aceitação. A ordem de manutenção corretiva deve ser priorizada considerando o desvio identificado e a criticidade do elemento degradado. Enquanto persistir a degradação, devem ser acionados procedimentos de contingência com aprovação e controle, incluindo medidas temporárias equivalentes quando aplicável. A medida proposta não pode ser considerada contingência adequadamente controlada enquanto não passar por esse processo. A ordem de manutenção trata a correção do desvio, mas não assegura, por si só, o controle da condição durante a espera pelo reparo: a permanência do sistema degradado sem contingência adequada compromete a resposta a incêndio. Portanto, é necessário tratar simultaneamente a recuperação do elemento e o controle do risco residual durante sua degradação.

**dificil_B · medido difícil · APROVADA**  
_Nota(s): Integração entre detecção de fogo e gás, SIS/ESD, supressão e HVAC nas ações automáticas de emergência; Disponibilidade real do sistema de combate a incêndio e robustez das funções de emergência associadas; Resiliência do sistema de combate a incêndio quando o próprio evento degrada o sistema_

**P:** Durante um incêndio em um FPSO, os registros confirmam que os comandos automáticos de supressão, parada de emergência e controle de ventilação correspondem à matriz de causa e efeito, mas as bombas elétricas não partem e a capacidade de combate fica reduzida. Há danos pelo fogo nos cabos de alimentação e barramentos; uma bomba elétrica temporária compartilha essa infraestrutura, enquanto bombas a diesel permanecem disponíveis para partida manual. A equipe propõe revisar primeiro a lógica automática, pois os comandos não produziram a mitigação esperada. Qual diagnóstico e prioridade de resposta são mais adequados, e por que a bomba temporária não comprova redundância efetiva?

**R:** O diagnóstico prioritário é perda de disponibilidade da infraestrutura acionada por dano do próprio incêndio, não erro de lógica: os comandos correspondem à matriz, mas isso não comprova que os equipamentos consigam executar a função. O dano aos cabos e barramentos explica a indisponibilidade das bombas elétricas. A prioridade é recorrer à contingência disponível, com partida manual das bombas a diesel para sustentar o combate, e verificar funcionalmente a cadeia entre demanda e atuação, incluindo a resposta aos diferentes iniciadores. A bomba temporária não demonstra redundância efetiva porque compartilha a infraestrutura elétrica danificada e, portanto, o mesmo mecanismo de falha. A avaliação da contingência deve considerar segregação, diversidade de energia, perigos e consequências da perda do sistema principal, inclusive durante manutenção. Revisar apenas a lógica não resolve a perda física de alimentação.

### Sistema de Fogo e Gás (F&G)

**facil · medido média · APROVADA**  
_Nota(s): Proof tests, testes parciais e inspeções associadas às SIF/F&G_

**P:** Como deve ser definida a frequência de proof test de uma função instrumentada de segurança associada ao sistema de fogo e gás, e por que ela não deve depender apenas da conveniência operacional?

**R:** A frequência deve atender à especificação de requisitos de segurança (SRS) e ser coerente com o cálculo de verificação do nível de integridade de segurança (SIL). As frequências de cada componente devem estar definidas na SRS e servir de base para esse cálculo. As restrições operacionais devem ser consideradas para tornar o planejamento apropriado e executável, mas a conveniência operacional, isoladamente, não demonstra atendimento aos requisitos da SRS nem coerência com a verificação de SIL.

**media · medido média · APROVADA**  
_Nota(s): Proof tests, testes parciais e inspeções associadas às SIF/F&G_

**P:** Durante um proof test parcial de uma função instrumentada de segurança associada ao sistema de fogo e gás, os instrumentos respondem ao teste, mas há suspeita de substituições não autorizadas e deterioração dos equipamentos associados. Quais verificações de configuração e integridade física devem acompanhar o teste para avaliar essas condições?

**R:** A inspeção deve identificar e abranger os instrumentos e os equipamentos associados, incluindo tubulações de instrumentação, caixas de junção e sistemas de aquecimento por traço. Deve verificar a ausência de modificações não autorizadas, inclusive pela conferência dos números de série, e procurar sinais de deterioração, como parafusos ou tampas faltantes, suportes enferrujados e danos em cabos. Essas verificações devem confirmar que o equipamento instalado não foi alterado nem se deteriorou a ponto de deixar de funcionar conforme a especificação de requisitos de segurança (SRS). A resposta dos instrumentos ao teste não substitui essa avaliação de configuração e condição física.

**dificil_A · medido difícil · APROVADA**  
_Nota(s): Estratégias combinadas de manutenção, calibração e verificação de desempenho em sistemas F&G_

**P:** Em um FPSO sob jurisdição britânica, um elemento crítico do sistema de fogo e gás ficou indisponível. A avaliação de risco admite operação temporária com produção limitada, desde que seja possível creditar o fechamento dos elementos finais de proteção remanescentes. Entretanto, as inspeções desses elementos estão pendentes, e a equipe propõe manter a produção limitada até o reparo, apoiando-se apenas nos registros de atuação anteriores. Qual decisão técnica deve ser tomada para controlar o risco durante a indisponibilidade?

**R:** Não autorizar a continuidade com base apenas na limitação de produção e nos registros de atuação anteriores. Na condição apresentada, a medida temporária depende do crédito pelos elementos finais remanescentes; sob o referencial britânico, esse crédito durante uma indisponibilidade não planejada deve ser acompanhado do atendimento aos requisitos de inspeção. Portanto, é necessário satisfazer esses requisitos antes de aceitar a operação temporária nas condições avaliadas. A inspeção deve verificar também os equipamentos associados, a deterioração e possíveis modificações não autorizadas. Em paralelo, deve-se aplicar manutenção corretiva para restaurar rapidamente a função indisponível. A limitação de produção não substitui a verificação da barreira da qual depende sua aceitação.

**dificil_B · medido difícil · APROVADA**  
_Nota(s): Sistema F&G: desempenho intrínseco do sensor, calibração e influência ambiental na detecção de gás inflamável; Interferência de umidade, vapor d’água, névoa/óleo e gases atmosféricos na resposta e na calibração de detectores de F&G; Calibração, aferição, ajuste, deriva e monitoramento de condição em detectores e instrumentos de F&G_

**P:** Em um FPSO, um detector de gás inflamável de estado sólido apresenta leituras flutuantes durante mudanças de umidade e temperatura, inclusive em períodos com névoa de óleo. O histórico contém verificações com o mesmo gás de referência, mas ainda não foi analisado em tendência; também não está demonstrado que a concentração real de gás permaneceu constante. A manutenção propõe recalibrar ou substituir imediatamente o sensor. Qual investigação deve ser priorizada para distinguir variação real do gás, interferência ambiental e deriva, e como seus resultados devem orientar a intervenção?

**R:** Priorizar a comparação do desempenho com padrão e a análise conjunta do histórico metrológico e das condições ambientais, sem concluir imediatamente por defeito. No sensor de estado sólido, umidade e temperatura alteram a adsorção superficial: flutuação de leitura não demonstra, sozinha, mudança da concentração real. Comparar respostas ao mesmo gás de referência no início e no fim do intervalo de ajuste permite investigar deriva sem mudar deliberadamente o estímulo. Se a resposta ao padrão variar com o ambiente, investigar essa dependência antes de ajustar; se houver afastamento persistente do padrão em condições comparáveis, avaliar ajuste. Desvio anormal pode indicar defeito que exija reparo, mas não o comprova automaticamente. Para episódios com névoa de óleo, não presumir desempenho nominal: a sensibilidade a essas liberações é variável e a calibração apresenta grandes incertezas. A hipótese de variação real do gás deve permanecer aberta, pois estabilidade metrológica não demonstra concentração constante em campo. A decisão deve combinar essas evidências e o acompanhamento em tendência.

### Sistemas e equipamentos de salvatagem

**facil · medido fácil · APROVADA**  
_Nota(s): Pontos de reunião e interfaces com o refúgio temporário na resposta a emergências_

**P:** O que significa estruturar a resposta a emergências de um FPSO com pontos de encontro distribuídos por função e localização?

**R:** Significa definir locais de apresentação distintos para as funções previstas na resposta, em vez de adotar um único ponto genérico para todos. Essa organização pode incluir a central de controle, a enfermaria, a sala de controle da praça de máquinas, o bote de resgate rápido, locais com equipamentos de brigada e o refúgio temporário, integrando esses locais à estrutura de resposta.

**media · medido média · APROVADA**  
_Nota(s): Pontos de reunião e interfaces com o refúgio temporário na resposta a emergências_

**P:** Em um FPSO, o plano de emergência define locais distintos de apresentação para comando, assistência a feridos, resposta técnica e pessoal destinado ao refúgio temporário. Como essa distribuição deve orientar a organização inicial das equipes e a conferência da apresentação do pessoal, em vez de concentrar todos em um único local?

**R:** A apresentação inicial deve seguir a correspondência entre função e ponto de encontro: cada grupo se apresenta no local previsto para sua atuação, e o pessoal destinado ao refúgio temporário se reúne nesse ambiente. Assim, a organização mantém a distribuição funcional das equipes, em vez de concentrá-las indistintamente. Para conferir a apresentação do pessoal, a referência é o local previsto para cada grupo; a simples reunião de pessoas em um único local não verifica o cumprimento dessa distribuição.

**dificil_A · medido difícil · APROVADA**  
_Nota(s): Condições de acesso, descida ao mar e lançamento seguro de life rafts_

**P:** Em uma instalação offshore no Reino Unido, uma balsa salva-vidas de lançamento manual está disponível, e uma escada fixa permite descer ao nível do mar por uma rota protegida. Entretanto, não há acesso à painter line (cabo de ligação à balsa) na chegada, e alcançar a balsa exige entrar na água. O ponto alternativo de embarque só pode ser alcançado por uma passagem cuja exposição à radiação térmica e à fumaça impede seu uso durante o período requerido de abandono. Esse arranjo pode ser considerado uma cadeia de abandono viável e quais falhas precisam ser corrigidas?

**R:** Não. A escada fixa oferece descida controlada, mas isso não garante a continuidade até a balsa: falta acesso à painter line no ponto de chegada ao nível do mar, tornando a entrada na água necessária, embora ela deva ser considerada último recurso. A alternativa também não resolve o problema, pois sua rota não permanece utilizável pelo período requerido. É necessário assegurar acesso funcional à painter line após a descida e proteção suficiente das rotas contra radiação térmica e fumaça para manter sua disponibilidade. Os pontos de lançamento e embarque também devem ser protegidos contra radiação térmica tanto quanto razoavelmente praticável. A existência da balsa e da rota física, isoladamente, não demonstra viabilidade do abandono.

**dificil_B · medido difícil · APROVADA**  
_Nota(s): Redundância e disponibilidade de rotas para escape-to-sea; Dependência do refúgio temporário quando o abandono é degradado; Proteção e disponibilidade de rotas de fuga, pontos de embarque e Temporary Refuge em cenários de incêndio, fumaça e explosão_

**P:** Em um FPSO, a indisponibilidade de um meio de evacuação reduz a capacidade imediata de abandono e prolonga a permanência prevista no refúgio temporário (TR). A rota alternativa está desobstruída, mas sua proteção contra calor e fumaça foi demonstrada apenas para um período inferior ao agora necessário. O TR apresenta condições atmosféricas aceitáveis no momento, porém os testes de seus sistemas de detecção mostram tendência de aproximação dos critérios de não conformidade. A equipe propõe aceitar o arranjo porque ainda existe uma saída e o TR está habitável. Qual decisão técnica deve orientar essa avaliação?

**R:** Não aceitar o arranjo apenas pela existência de uma saída e pela habitabilidade atual do TR. A capacidade remanescente deve ser avaliada como uma cadeia de proteção e deslocamento durante todo o período agora necessário: as rotas precisam continuar seguras e disponíveis, com proteção contra calor e fumaça compatível com esse período. A demonstração para um intervalo menor não sustenta essa disponibilidade prolongada. Em paralelo, a avaliação do TR deve considerar as condições atmosféricas que comprometeriam sua efetividade durante a permanência, e não apenas a condição instantânea. A tendência dos testes de detecção deve orientar intervenção preventiva antes da não conformidade, em vez de aguardar falha. A aceitação exige demonstrar conjuntamente a permanência protegida no TR e a continuidade do acesso seguro ao abandono pelo tempo requerido; uma dessas condições não substitui a outra.

## Utilidades, geração de energia e sistemas auxiliares

### Geração e distribuição de energia elétrica

**facil · medido fácil · APROVADA**  
_Nota(s): PMS/EMS como supervisão integrada da geração, sincronismo e partilha de carga_

**P:** Qual é a função do sistema de gerenciamento de energia (PMS) em uma rede elétrica offshore com múltiplos geradores conectados ao mesmo barramento?

**R:** O PMS integra a supervisão contínua da rede elétrica à coordenação da geração. Comanda a partida e a conexão de geradores ao barramento, realiza a partilha de carga e controla ou monitora frequência e sincronismo. Ao acompanhar as condições elétricas e detectar antecipadamente anormalidades em grandes consumidores, permite prevenir sobrecargas, manter a estabilidade e sustentar a continuidade do fornecimento.

**media · medido média · APROVADA**  
_Nota(s): PMS/EMS como supervisão integrada da geração, sincronismo e partilha de carga_

**P:** Em uma instalação offshore, a entrada de grandes consumidores aumenta a demanda elétrica, e o sistema de gerenciamento de energia (PMS) acompanha continuamente tensões, correntes e fator de potência. Como essas informações devem apoiar a conexão de outro gerador ao barramento e a partilha de carga?

**R:** As medições permitem acompanhar o estado elétrico da rede e identificar tendências de sobrecarga ou condições anormais durante o aumento da demanda. Essa visibilidade apoia a decisão de colocar geração adicional em serviço. O PMS coordena a partida e a conexão do gerador ao barramento, com controle ou monitoramento de frequência e sincronismo, e realiza a partilha de carga entre as unidades conectadas. Assim, a aquisição contínua de dados fundamenta a atuação sobre a geração para prevenir sobrecargas e manter a estabilidade.

**dificil_A · medido média · APROVADA**  
_Nota(s): Arranjos de partida de unidades geradoras e automação da lógica de partida_

**P:** Em um sistema com múltiplos geradores, uma unidade automática já coordena as partidas, mas o bloco de partida axial apresenta problemas operacionais frequentes que comprometem a confiabilidade das unidades. A equipe considera manter esse bloco por já existir controle automático ou substituí-lo por um Conversor Estático de Frequência (SFC), automatizando integralmente o processo de partida. Qual decisão é tecnicamente justificável e por que a automação existente não elimina a necessidade dessa mudança?

**R:** É justificável substituir o bloco de partida axial pelo SFC, pois a recorrência dos problemas no próprio arranjo de partida compromete a confiabilidade das unidades. A existência de uma unidade automática que coordena as partidas dos geradores não equivale à automatização integral do processo executado pelo equipamento de partida, nem elimina os problemas operacionais do bloco axial. A substituição atua sobre o arranjo associado a esses problemas e torna o processo de partida totalmente automatizado. Portanto, a justificativa combina o comprometimento recorrente da confiabilidade com a automatização do processo, e não apenas a presença ou ausência de controle automático do conjunto de geradores.

**dificil_B · medido difícil · APROVADA**  
_Nota(s): Filosofia de geração principal, emergência e realimentação do quadro principal; Continuidade de alimentação de cargas essenciais e reconfiguração em contingências elétricas; Redundância e reconfiguração da distribuição para sustentar consumidores essenciais e de controle_

**P:** Após perda de toda a geração principal de um FPSO, a geração de emergência realimenta parte do painel principal, com os disjuntores dos geradores principais abertos e a seletora das cargas essenciais em realimentação. Simultaneamente, o conjunto A de 24 Vcc falha; o conjunto B permanece disponível, mas o disjuntor de interligação TIE está aberto. O controlador lógico programável (CLP) e os painéis de controle alimentados por A ficam sem energia, enquanto os consumidores de B permanecem operáveis. Qual reconfiguração deve ser priorizada para recuperar o controle, e por que a realimentação já estabelecida não garante, sozinha, a recomposição das cargas prioritárias?

**R:** Deve-se estabelecer a transferência dos consumidores de A para o conjunto B pelo disjuntor TIE. Cada conjunto de 24 Vcc tem capacidade para atender sozinho 100% da demanda do quadro de corrente contínua; portanto, a falha de A não exige perda desses consumidores quando B está disponível e a interligação é estabelecida. O diagnóstico é de indisponibilidade do caminho de alimentação auxiliar, não de falta de capacidade do conjunto remanescente. O back feeding atende sistemas ligados ao painel principal, mas não substitui a transferência dos circuitos de controle em 24 Vcc. Da mesma forma, recuperar CLP e painéis de controle por B não realimenta, por si só, os consumidores do painel principal. A continuidade requer os dois caminhos corretamente configurados: transferência em corrente contínua e realimentação pela emergência, esta condicionada à indisponibilidade dos geradores principais, aos disjuntores abertos ou em teste e à seletora em realimentação.

### Sistema de utilidades

**facil · medido fácil · APROVADA**  
_Nota(s): Gestão energética e hídrica baseada em M&V e indicadores em sistemas de utilidades_

**P:** Por que inspeções e calibrações periódicas dos instrumentos são necessárias à confiabilidade dos dados de medição e como essa confiabilidade afeta a avaliação do desempenho energético?

**R:** Inspeções e calibrações periódicas são necessárias para assegurar a confiabilidade dos dados fornecidos pelos equipamentos de medição. Sem essa confiabilidade, fica condicionado o uso dos dados para gerir o consumo e avaliar o desempenho energético. Portanto, a avaliação rigorosa depende de práticas de medição e verificação apoiadas em dados confiáveis.

**media · medido média · APROVADA**  
_Nota(s): Gestão energética e hídrica baseada em M&V e indicadores em sistemas de utilidades_

**P:** Em um FPSO, a equipe pretende otimizar o uso de água e energia nas utilidades, mas conhece apenas os consumos totais, sem identificar as demandas de cada aplicação nem os pontos de geração de efluentes. Que levantamento deve orientar a identificação de oportunidades e a escolha das medidas de otimização?

**R:** A equipe deve conhecer as atividades atendidas pelas utilidades e identificar os principais pontos de consumo, a forma e a quantidade de água e energia utilizadas, os requisitos de quantidade e qualidade de cada aplicação e os pontos de geração de efluentes. Esse levantamento permite identificar oportunidades de adequação do uso dos recursos às necessidades das aplicações. As medidas devem ser selecionadas conforme o perfil de operação dos equipamentos, buscando reduzir consumos, custos e descargas de águas residuais industriais.

**dificil_A · medido difícil · APROVADA**  
_Nota(s): Falhas em utilidades térmicas e de resfriamento: segregação de circuitos e consequências da perda de circulação_

**P:** Durante a retomada operacional de uma plataforma offshore, as bombas de circulação de um sistema de transferência de calor em fase líquida permanecem paradas, mas o queimador principal está em operação. A pressão do circuito começa a subir rapidamente, embora ainda não haja vazamento visível. A equipe propõe manter o queimador ligado enquanto tenta restabelecer o bombeio. Essa proposta é tecnicamente aceitável? Justifique relacionando a condição operacional à possível evolução do evento.

**R:** Não. A combinação de bombas paradas e queimador em operação deve ser tratada como condição perigosa, e não apenas como indisponibilidade de bombeio. O aporte de calor sem circulação pode superaquecer o fluido, provocar sua expansão e elevar rapidamente a pressão. Se a pressão exceder a resistência do tanque de expansão, pode ocorrer ruptura, com extravasamento do fluido aquecido sobre o aquecedor e o convés, seguido de ignição. Portanto, manter o queimador operando enquanto se tenta recuperar a circulação permite a continuidade desse encadeamento. A ausência de vazamento visível não afasta o risco: a perda de contenção é uma consequência posterior ao superaquecimento e à sobrepressão.

**dificil_B · medido difícil · APROVADA**  
_Nota(s): Segurança operacional em sistemas de heating medium em fase líquida: superaquecimento por perda de circulação, sobrepressão e salvaguardas; Intertravamentos e sistemas de proteção para desligamento seguro em turbinas, compressores e utilidades; Falhas em utilidades térmicas e de resfriamento: segregação de circuitos e consequências da perda de circulação_

**P:** Durante a retomada de um FPSO, o desligamento manual de segurança interrompe todas as bombas e sistemas de processo, mas a válvula de combustível do queimador do heating medium líquido permanece aberta. Com as bombas de circulação paradas, a temperatura após a câmara de combustão e a pressão começam a subir. A equipe considera o desligamento suficiente e propõe aguardar, confiando no alívio do tanque de expansão. Que ação deve ser priorizada e por que o alcance do desligamento e as demais barreiras não garantem um estado seguro nessa condição?

**R:** Priorizar o bloqueio do combustível do queimador: o desligamento das bombas e dos sistemas de processo não garante segurança se o aporte térmico permanece ativo. A parada das bombas elimina a circulação que remove calor da região aquecida; mantendo-se a combustão, podem ocorrer superaquecimento, expansão, sobrepressão, ruptura do tanque e extravasamento com posterior ignição. Portanto, a atuação do desligamento manual não comprova que a proteção entre equipamentos tenha cumprido sua função: o bloqueio deve impedir a operação da válvula de combustível quando as bombas não operam. É necessário avaliar conjuntamente o alcance do desligamento e esse bloqueio antes da retomada, e não apenas confirmar que as bombas pararam. O monitoramento contínuo de temperatura após a câmara de combustão detecta a anomalia; resistência mecânica e alívio limitam consequências, mas não substituem a prevenção. Para sistemas desse tipo, a fonte BSEE recomenda testar operacionalmente o alívio secundário mensalmente e antes de cada partida; isso não estabelece, por si só, obrigação geral para FPSOs brasileiros.

## Descomissionamento e Gestão do Ciclo de Vida da Unidade

### Geral

**facil · medido média · APROVADA**  
_Nota(s): Estratégia de ciclo de vida, extensão de vida e preparação para descomissionamento em unidades flutuantes_

**P:** Por que a gestão do ciclo de vida de um FPSO deve começar na fase de projeto, e não apenas durante a operação ou próximo ao descomissionamento?

**R:** Porque o projeto permite antecipar riscos, identificar possíveis desvios, condições inseguras e falhas combinadas das camadas de proteção antes da entrada em operação. Também permite incorporar medidas que reduzam impactos ambientais, sociais e de saúde e segurança do futuro descomissionamento, com menor custo, como a localização adequada de componentes, a prevenção de interferências com áreas sensíveis e o estabelecimento de garantias financeiras. O gerenciamento de riscos deve continuar ao longo do ciclo de vida, até a desativação, incluindo planejamento, execução de ações, controle e análise crítica.

**media · medido difícil · APROVADA**  
_Nota(s): Estratégia de ciclo de vida, extensão de vida e preparação para descomissionamento em unidades flutuantes_

**P:** Um FPSO ainda está distante do fim da vida de projeto, mas apresenta mudanças na condição operacional e nos fatores que influenciam a degradação. Por que a preparação para extensão de vida deve ocorrer desde já e quais elementos técnicos devem sustentar a futura decisão?

**R:** A preparação deve ser contínua porque o envelhecimento não é definido apenas pela idade: depende da condição operacional conhecida e dos fatores que influenciam a degradação. Portanto, a distância até o fim da vida de projeto não justifica adiar essa preparação. A futura decisão deve ser sustentada por uma metodologia de extensão de vida que inclua avaliação completa da unidade, demonstrando integridade estrutural e mecânica suficiente para operar com segurança além da vida de projeto. Também são necessárias avaliações técnicas formais e estruturadas que demonstrem a adequação das barreiras de segurança; constatações pontuais de auditoria sobre envelhecimento não substituem essa avaliação.

**dificil_A · medido difícil · APROVADA**  
_Nota(s): Controle do retorno ao serviço após lay-up ou intervenção_

**P:** Após um período ocioso de um FPSO, a manutenção de um sistema de processo foi encerrada, mas os isolamentos temporários permanecem instalados e a necessidade de inertização não foi avaliada. A equipe propõe retirar todos os isolamentos e introduzir fluido imediatamente, deixando a reinstalação dos tampões roscados dos drenos para depois do retorno. Como tratar essa partida como gestão de mudanças orienta a decisão e a sequência de retorno ao serviço?

**R:** Não se deve autorizar a introdução imediata de fluido apenas porque a manutenção terminou. A reintrodução de fluidos após manutenção ou período ocioso gera perigos próprios e deve ser controlada como uma mudança de condição operacional. A sequência deve seguir os procedimentos específicos da instalação, com aplicação efetiva da permissão de trabalho (PTW) e dos certificados de isolamento, em vez de uma retirada indiscriminada dos isolamentos. É necessário avaliar a necessidade de inertização e, se requerida, incorporá-la à sequência prevista antes da introdução do fluido de processo. A recomposição e a retirada dos isolamentos devem ser coordenadas por esses controles. Após o retorno, devem ser reinstalados os tampões roscados nas extremidades dos drenos. Portanto, essa reinstalação posterior não justifica antecipar a partida sem avaliar a inertização e controlar os isolamentos.

**dificil_B · medido difícil · APROVADA**  
_Nota(s): Avaliação inicial da unidade para definir remoção, reboque e local de desmontagem; Riscos e restrições para retirada da FPSO da locação e reboque até estaleiro; Condição de limpeza, drenagem e isolamento da planta para transporte ou reboque_

**P:** Uma equipe propõe rebocar um FPSO para desmontagem em estaleiro, visando reduzir a exposição das pessoas às atividades offshore. A avaliação inicial indica integridade e navegabilidade preliminarmente favoráveis e sistemas disponíveis para limpeza e desconexão, mas ainda há hidrocarbonetos e materiais radioativos naturais tecnologicamente concentrados (TENORM) a remover. Foram confirmadas espécies exóticas invasoras no casco, e uma perda de posição durante a retirada pode causar colisão com uma instalação adjacente. Como decidir entre manter a proposta de reboque e aprofundar a alternativa de desmontagem offshore, considerando também o condicionamento da planta?

**R:** Não aprovar o reboque apenas pela condição técnica preliminar ou pela expectativa de menor exposição offshore; aprofundar a alternativa de desmontagem na locação, sem considerá-la automaticamente segura. A avaliação de navegabilidade, integridade e disponibilidade dos sistemas fundamenta o planejamento, mas não elimina os demais condicionantes. A presença de espécies exóticas invasoras torna o método de reflutuação e reboque não recomendado pelo risco de disseminação. Além disso, a possível perda de posição com colisão representa perigo de acidente maior e deve integrar a avaliação de segurança; no contexto regulatório britânico, essa avaliação é exigida no safety case. Para eventual navegação ou reboque, ainda é necessário executar drenagem, ventilação, purga e lavagem, remover hidrocarbonetos, outras substâncias e TENORM e isolar os sistemas contra recontaminação, atendendo à condição determinada pela classificadora. Com planta e tanques limpos, realizam-se os reforços e ajustes estruturais necessários. Essa preparação não elimina a restrição ambiental nem o perigo de perda de posição.

## Gestão do Desempenho Empresarial (KPI)

### Gestão do Desempenho Empresarial (KPI)

**facil · medido fácil · APROVADA**  
_Nota(s): KPIs para segurança de processo e gestão dinâmica de risco operacional_

**P:** Por que indicadores de input, como horas dedicadas à saúde, segurança e meio ambiente (HSE) e número de inspeções, não bastam isoladamente para medir o desempenho em segurança de processo?

**R:** Porque medem o esforço aplicado, mas não demonstram necessariamente o impacto do trabalho realizado. Mais horas ou inspeções não comprovam, por si só, redução do risco ou recuperação de funções de segurança degradadas. Esses indicadores devem ser complementados por resultados qualitativos que forneçam evidências do efeito das atividades sobre a segurança.

**media · medido média · APROVADA**  
_Nota(s): KPIs para segurança de processo e gestão dinâmica de risco operacional_

**P:** Em um FPSO sob o regime regulatório do Reino Unido, um elemento crítico de segurança (SCE) está degradado, e a equipe pretende avaliar a continuidade operacional. Quais elementos de governança devem sustentar essa avaliação e a decisão de continuar operando?

**R:** Deve existir um procedimento formal e robusto que defina o processo de avaliação de risco, os níveis de autoridade para a decisão, a expertise técnica envolvida e os requisitos de revisão. A avaliação deve considerar o papel do SCE como barreira contra perigos de acidentes maiores e fundamentar as medidas de mitigação e/ou barreiras adicionais. As avaliações devem ser registradas e auditadas regularmente. Se houver outras degradações, avaliações individuais adequadas não bastam: o risco combinado deve ser examinado em revisões gerais periódicas, com expertise apropriada e sem depender exclusivamente da gestão offshore.

**dificil_A · medido média · APROVADA**  
_Nota(s): Qualidade dos dados e trending como base de KPIs preditivos de confiabilidade dos ativos_

**P:** Em um FPSO, o indicador de confiabilidade de uma bomba mantém uma tendência aparentemente contínua, embora a condição observada após sua substituição não corresponda ao histórico apresentado. A conferência não encontrou erros de registro nem divergências entre as ferramentas utilizadas, e não houve mudança identificada nas propriedades dos fluidos. O sistema identifica o conjunto pela localização funcional, e a bomba nova recebeu o mesmo tag da anterior. Qual causa deve ser priorizada na investigação e como tratar o histórico antes de utilizá-lo para decisões de manutenção?

**R:** Deve-se priorizar a perda de rastreabilidade do item físico: a identificação pela localização funcional e a reutilização do tag podem ter misturado os históricos da bomba retirada e da nova, produzindo uma continuidade que não representa o mesmo equipamento. Antes de utilizar a tendência, é necessário distinguir os registros de cada bomba e restabelecer a vinculação dos dados ao item correspondente. Os indícios apresentados tornam erro de registro e divergência entre ferramentas menos prováveis; também não sustentam atribuir a inconsistência à mudança das propriedades dos fluidos. A tendência com rastreabilidade restabelecida deve servir de base para prever ameaças e apoiar manutenção proativa, em vez de orientar decisões a partir do histórico misturado.

**dificil_B · medido difícil · APROVADA**  
_Nota(s): Sistema de KPIs alinhado à estratégia e à criação de valor; KPIs econômicos e operacionais para sustentabilidade do negócio em FPSOs; Risco de processo, degradação de barreiras e impacto no desempenho empresarial_

**P:** Em um FPSO sob pressão de preços do petróleo, a gestão reforça metas de redução de despesas operacionais (OPEX) e manutenção da produção. O painel mostra menor gasto e produção preservada, mas surgem desvios operacionais e adiamentos de manutenção que degradam funções de segurança. A diretoria pretende manter essas metas por considerar o resultado favorável. Como revisar o sistema de indicadores-chave de desempenho (KPIs) e orientar essa decisão para distinguir criação de valor de melhoria econômica aparente?

**R:** A melhoria de gasto e produção não basta para validar a manutenção das metas. O painel deve explicitar o encadeamento entre metas, decisões operacionais e de manutenção, degradação das funções de segurança, alteração do risco de processo e resultado empresarial. Para isso, deve relacionar custos e produção a variáveis que monitorem os desvios, as funções de segurança afetadas e seus efeitos sobre a frequência ou a severidade dos cenários de risco, conectando essas informações à rentabilidade e ao retorno dos ativos. A redução de custo deve ser avaliada pelo equilíbrio dos efeitos da manutenção, não pelo gasto isolado. Como acidentes de processo comprometem fortemente a sustentabilidade do negócio, a diretoria deve reavaliar as metas e decisões que favorecem a degradação identificada, em vez de premiar automaticamente a economia registrada. A revisão deve tornar visíveis essas relações causais para que o desempenho local não seja confundido com criação de valor.

## Logística, Suprimentos e Movimentação de Cargas

### Logística e Suprimento Offshore

**facil · medido média · APROVADA**  
_Nota(s): Operações submarinas e recursos de apoio: como a seleção de meios e sistemas muda a logística e as interfaces com a unidade_

**P:** Por que a eliminação do umbilical em operações de inspeção com veículo submarino autônomo (AUV) reduz as exigências sobre os sistemas de lançamento e a embarcação de apoio, especialmente em maiores profundidades?

**R:** Sem umbilical, o AUV reduz a necessidade de recursos de lançamento mais robustos, como guincho e pórtico com compensação dos movimentos verticais da embarcação. Isso diminui os requisitos de equipamentos de lançamento que a embarcação de apoio precisa atender. O impacto dessa redução cresce proporcionalmente à profundidade, tornando o benefício logístico mais relevante em águas mais profundas.

**media · medido ? · REPROVADA: suporte, sem_generalizacao**  
_Nota(s): Operações submarinas e recursos de apoio: como a seleção de meios e sistemas muda a logística e as interfaces com a unidade_

**P:** Uma campanha submarina inicialmente limitada à inspeção passa a incluir abertura e fechamento de válvulas e cortes em componentes. Como essa mudança de escopo deve orientar a escolha entre um veículo submarino autônomo (AUV) e um veículo operado remotamente (ROV), considerando também os recursos de apoio?

**R:** Para o escopo de inspeção, o AUV é favorecido pela ausência de umbilical e pela menor exigência de recursos robustos de lançamento. Com a inclusão de abertura e fechamento de válvulas e cortes, a escolha deve priorizar um ROV dotado dos manipuladores necessários à intervenção, e não apenas a simplicidade logística do lançamento. A mobilização deve considerar os recursos associados ao ROV: sala de controle, supervisor e piloto durante os mergulhos, além de outro piloto ou mecânico para operar o guincho de descida e subida do veículo.

**dificil_A · medido difícil · APROVADA**  
_Nota(s): Gestão de estoques e sobressalentes no suprimento offshore: criticidade, risco, custo total e nível de serviço_

**P:** Um FPSO mantém um sobressalente de componente submarino crítico cuja indisponibilidade prolonga a parada de produção. O item tem baixo giro e elevado valor imobilizado, mas o mercado fornecedor é complexo e o nível de serviço requerido é alto. Uma proposta prevê eliminar o estoque para reduzir custos; outra propõe uma parceria com fornecedor, ainda sem demonstrar capacidade de manter o atendimento necessário. Qual decisão deve ser tomada sobre o estoque e a parceria, considerando o custo total e o risco da indisponibilidade?

**R:** Manter o sobressalente enquanto a alternativa de fornecimento não demonstrar capacidade de preservar o nível de serviço requerido e limitar o tempo de restauração da função. O baixo giro e o valor imobilizado, isoladamente, não justificam retirar um item crítico de produção: sua disponibilidade deve minimizar a indisponibilidade operacional. A parceria pode ser desenvolvida como meio de melhorar o atendimento e reduzir custos, mas não deve ser tratada como substituição automática do estoque. Sua avaliação deve considerar criticidade, complexidade do mercado fornecedor, potencial de economia e dificuldade de implantação. Uma eventual redução de estoque deve ser sustentada por uma análise de confiabilidade e risco e pela redução do custo total do suprimento, com manutenção ou melhoria do nível de serviço, e não apenas pela diminuição do capital imobilizado.

**dificil_B · medido difícil · APROVADA**  
_Nota(s): Embarcações de apoio offshore e configuração das cargas de suprimento, com foco no PSV; Planejamento logístico de suprimentos com PSV sob restrições de arrumação no convés; Priorização logística offshore sob restrições de armazenamento, POB e transporte_

**P:** Um FPSO solicita consumíveis cuja falta interromperia a operação, contêineres para manutenção adiável e equipamentos volumosos para uma atividade posterior, todos na mesma janela de suprimento. Embora a massa total seja compatível com o PSV (Platform Supply Vessel, embarcação de suprimento), os volumes não cabem no convés nas orientações permitidas, sem empilhamento. A unidade exige embarque integral devido à baixa capacidade de armazenagem e às atividades programadas. Como decidir a composição da viagem e justificar a postergação de parte da carga?

**R:** O gargalo é a área e a geometria de arrumação do convés, não a tonelagem: a compatibilidade da massa total não garante que os volumes caibam, pois não se admite empilhamento nem rotação. Deve-se refazer o arranjo com as dimensões e orientações permitidas, priorizando os consumíveis cuja ausência interromperia a operação. Os materiais de manutenção adiável e os equipamentos destinados à atividade posterior devem ser comparados pelas consequências de sua postergação e pelo espaço que ocupam, embarcando apenas o conjunto fisicamente viável. A parcela que não couber deve ter o atendimento reprogramado, considerando o impacto sobre a execução da manutenção. A baixa armazenagem justifica o suprimento periódico e reforça a necessidade de priorização, mas não elimina a restrição física do PSV nem torna todas as demandas igualmente críticas.

### Movimentação de Cargas

**facil · medido fácil · APROVADA**  
_Nota(s): Controle contínuo da operação de içamento por planejamento, supervisão e handover_

**P:** Qual é a função do lifting plan (plano de içamento) na orientação da operação e na definição do equipamento a ser utilizado?

**R:** O plano de içamento orienta a execução da operação por meio de instruções passo a passo e especifica os detalhes do equipamento a ser utilizado, vinculando a sequência de trabalho aos recursos previstos para realizá-la.

**media · medido média · APROVADA**  
_Nota(s): Controle contínuo da operação de içamento por planejamento, supervisão e handover_

**P:** Durante um içamento offshore, o supervisor precisa se afastar, e a equipe executante não dispõe do plano de içamento no local. Que medidas de supervisão e organização são necessárias para manter a aderência entre o plano e a execução em campo?

**R:** A organização deve assegurar que o plano esteja disponível à equipe e que seu conteúdo seja comunicado aos participantes. O afastamento do supervisor deve ser acompanhado de uma passagem de responsabilidade estruturada, registrada, comunicada e supervisionada, preservando a supervisão e o monitoramento do trabalho. A supervisão deve acompanhar essa transferência, enquanto a organização deve verificar a efetividade de seus procedimentos de supervisão e identificar fatores que a prejudiquem, como restrições de tempo ou de treinamento. Prosseguir sem supervisão e sem o plano disponível compromete o controle operacional e pode contribuir para danos a equipamentos e consequências graves.

**dificil_A · medido difícil · APROVADA**  
_Nota(s): Limites ambientais e classificação dinâmica em içamentos entre unidade e embarcação_

**P:** Durante a transferência de uma carga de um FPSO para uma embarcação de apoio, o peso suspenso permanece abaixo da capacidade nominal estática do guindaste. O movimento relativo aumenta, o operador passa a ter dificuldade para estimar o pouso no convés e a tag line (cabo-guia) apresenta folga variável junto à equipe. O operador propõe continuar porque o peso não mudou e o guindaste possui funções de segurança. Qual decisão deve ser tomada e como justificá-la tecnicamente?

**R:** Interromper a operação, pois o peso abaixo da capacidade estática não comprova segurança em uma transferência dinâmica. O movimento relativo pode elevar transitoriamente o momento aplicado ao guindaste; para o mesmo modelo e ângulo de lança, a capacidade dinâmica admissível é inferior à estática. A avaliação deve considerar essa capacidade e as limitações das funções de segurança, cuja presença não autoriza operar fora das capacidades do equipamento. A dificuldade de estimar o pouso evidencia comprometimento do controle da transferência, enquanto a folga variável do cabo-guia aumenta o risco de emaranhamento e reduz a consciência situacional da equipe. Antes de considerar a retomada, é necessário reavaliar os movimentos, a altura do convés, o comportamento do cabo-guia e o posicionamento dos trabalhadores, em conjunto com as restrições do guindaste.

**dificil_B · medido difícil · APROVADA**  
_Nota(s): Supervisão, monitoramento em tempo real e verificação de conformidade em operações de içamento offshore; Trajetória, altura livre e controle de interferências na movimentação de cargas; Interferências mecânicas, tração anômala e movimentos relativos na avaliação da capacidade de içamento_

**P:** Durante a descida de uma carga junto a estruturas de um FPSO, o guincho desenrola cabo, a indicação de peso diminui, mas o observador não confirma deslocamento; o operador não vê parte da trajetória. Para manter o rigger afastado, a equipe adotou um cabo guia mais longo que o discutido no toolbox talk, agora próximo de uma saliência. Parte da equipe propõe continuar baixando, alegando simples resistência no apoio, inspeções pré-uso concluídas e plano aprovado. Como o supervisor deve decidir sobre a continuidade e estabelecer condições para retomar, considerando tanto os sinais da manobra quanto a alteração do cabo guia?

**R:** Deve interromper e investigar possível enrosco, sem concluir que a carga apenas resiste no apoio. Desenrolamento sem deslocamento confirmado, associado à redução da indicação de peso, pode significar transferência de sustentação para uma estrutura, não margem segura para continuar. É necessário confrontar movimento da carga, comportamento da linha e indicação de peso, verificando os pontos de contato da trajetória. O cabo guia também deve ser inspecionado: seu maior comprimento afasta o rigger, mas pode criar uma interferência na saliência; não se deve presumir que seja a causa. Plano aprovado e inspeções pré-uso não comprovam conformidade da execução: a alteração frente ao procedimento discutido deve ser verificada e justificada. Para retomar, é preciso esclarecer a ausência de movimento, tratar as interferências identificadas e adequar o cabo guia para manter afastamento seguro sem favorecer enrosco. A comunicação deve confirmar deslocamentos reais, direcionais e incrementais. Insistir no desenrolamento pode permitir liberação súbita de um enrosco.

## Manutenção, Inspeção e Integridade de Ativos

### Apoio Técnico e Manutenção em um FPSO (Laboratório, Oficinas, Pipe Shop)

**facil · medido fácil · APROVADA**  
_Nota(s): Boas práticas de qualidade em ensaios laboratoriais que suportam decisões de integridade_

**P:** Qual é a finalidade da limpeza prévia dos equipamentos de amostragem e de ensaio antes de testes laboratoriais de corrosão?

**R:** Evitar que resíduos presentes nos equipamentos contaminem a amostra e falseiem o resultado do teste de corrosão. A limpeza deve abranger os equipamentos de amostragem e de ensaio, conforme os métodos estabelecidos, antes da execução do teste.

**media · medido média · APROVADA**  
_Nota(s): Boas práticas de qualidade em ensaios laboratoriais que suportam decisões de integridade_

**P:** Uma amostra de gás liquefeito de petróleo (GLP) foi coletada para avaliar a corrosividade do produto armazenado em um FPSO, mas sua representatividade não foi assegurada e a limpeza prévia dos equipamentos de coleta e ensaio não foi confirmada. Como essas condições afetam a confiabilidade do resultado para controle da qualidade e decisões de integridade?

**R:** O resultado não oferece uma base confiável para concluir sobre a condição real do produto armazenado. A falta de representatividade pode fazer o ensaio avaliar uma condição diferente daquela que se pretende verificar; a ausência de confirmação da limpeza deixa aberta a possibilidade de contaminação que falseie o resultado. Para sustentar a conclusão técnica, é necessário assegurar uma amostra representativa do produto armazenado e a limpeza prévia de todo o equipamento de amostragem e ensaio conforme os métodos estabelecidos.

**dificil_A · medido difícil · APROVADA**  
_Nota(s): Sistema metrológico do laboratório e rastreabilidade aos padrões_

**P:** O laboratório de instrumentação de um FPSO propõe acrescentar dois níveis intermediários à sua hierarquia de calibração, mantendo a referência nacional utilizada. A equipe considera que o maior número de calibrações tornará o resultado final mais robusto, mas ainda não documentou a incerteza e os procedimentos dos novos níveis. Essa alteração pode ser aceita como melhoria da confiabilidade metrológica? Justifique considerando o efeito das etapas adicionais e as condições de rastreabilidade.

**R:** Não pode ser aceita como melhoria apenas por acrescentar calibrações. Ao longo da hierarquia, cada etapa depende da anterior e acrescenta contribuição à incerteza, que aumenta até o resultado final. Portanto, mais níveis não significam, por si só, maior robustez metrológica. Manter a referência nacional também não basta: a rastreabilidade exige uma cadeia ininterrupta, com incertezas e procedimentos documentados e competência técnica reconhecida. Antes de aceitar a alteração, é necessário completar esses elementos nos novos níveis e considerar a incerteza acumulada no resultado final. Uma cadeia mais longa pode manter rastreabilidade válida, mas não elimina o aumento de incerteza decorrente das etapas adicionais.

**dificil_B · medido difícil · APROVADA**  
_Nota(s): Planejamento de inspeção, monitoramento de integridade e gestão de recomendações em FPSO; Registros, rastreabilidade e controle documental de serviços, inspeções e materiais em apoio técnico e manutenção de FPSO; Priorização de correções e resposta a não conformidades para evitar interdição de FPSO_

**P:** Em uma auditoria interna de um FPSO, recomendações antigas de inspeção de equipamentos críticos apresentam status divergentes entre os sistemas de integridade e manutenção. A oficina informa que executou reparos, mas os registros não vinculam cada intervenção ao achado original nem apresentam resultados dos testes de aceitação. A operação propõe encerrar as pendências para reduzir o backlog, enquanto a integridade alerta para o risco de interdição. Qual decisão deve ser tomada e por que a execução física dos reparos não demonstra, sozinha, controle do risco?

**R:** Não encerrar as recomendações apenas pela informação de que os reparos foram executados. Deve-se reconciliar os registros por equipamento, vinculando achado, recomendação, classificação, prazo, intervenção e evidências de inspeções, testes ou ensaios que permitam aprovar o serviço, com acompanhamento até o fechamento. Quando essas evidências forem insuficientes, a condição atual deve ser reavaliada para orientar o tratamento da pendência. A prioridade deve considerar a criticidade, as condições de serviço e as consequências da falha, e não a conveniência de reduzir o backlog. Ações contingenciais e corretivas devem ser implementadas em prazo compatível com o risco. Sem esse encadeamento, um serviço executado pode mascarar uma recomendação ainda não atendida ou um reparo sem eficácia demonstrada; portanto, o status administrativo não comprova integridade. A exposição técnica permanece sem controle demonstrável, e falhas no autodiagnóstico e na implementação tempestiva de contingências e correções podem levar à interdição do FPSO.

### Cibersegurança e Integridade de Sistemas Digitais

**facil · medido fácil · APROVADA**  
_Nota(s): Autenticação robusta e gestão segura de credenciais em sistemas digitais que suportam funções essenciais_

**P:** Em sistemas digitais que sustentam funções essenciais de um FPSO, qual é a lógica do princípio do menor privilégio e como ele limita o impacto de uma credencial comprometida?

**R:** O princípio do menor privilégio consiste em conceder ao usuário somente os acessos necessários à sua função. Se uma credencial for comprometida, essa restrição limita o alcance do uso indevido às permissões concedidas à conta, reduzindo o impacto potencial sobre os sistemas essenciais. Ela não impede, por si só, o comprometimento da credencial.

**media · medido média · APROVADA**  
_Nota(s): Autenticação robusta e gestão segura de credenciais em sistemas digitais que suportam funções essenciais_

**P:** O sistema de acesso a funções essenciais de um FPSO identifica individualmente os usuários, mas permite cadastrar senhas sem qualidade aceitável. Que mudança deve ser feita no cadastro e como ela contribui para a confiabilidade da autenticação e a prevenção do uso indevido de contas?

**R:** O sistema deve recusar o cadastramento de senhas sem qualidade aceitável. Identificar individualmente o usuário não substitui a necessidade de autenticação robusta: aceitar credenciais fracas compromete a proteção da conta. A validação da qualidade da senha reforça essa proteção e reduz o risco de uso indevido, contribuindo para que o acesso autenticado corresponda ao usuário autorizado.

**dificil_A · medido difícil · APROVADA**  
_Nota(s): Contenção, erradicação e recuperação de incidentes cibernéticos na automação industrial_

**P:** Em um FPSO, a rede de automação industrial perde comunicação enquanto recebe grande volume de requisições dirigidas a um host, sem evidência inicial de infecção nesse ativo. Há suspeita de ataque distribuído com falsificação dos endereços IP de origem (IP spoofing), e a equipe propõe aguardar a identificação do atacante antes de agir. Durante o diagnóstico, um segundo ativo apresenta infecção por vírus confirmada. Como priorizar e diferenciar a resposta técnica nesses dois ativos?

**R:** No primeiro ativo, priorizar a resposta à degradação da conectividade com a engenharia de telecomunicações ou redes: o acúmulo de requisições e a inundação de pacotes podem explicar a perda de comunicação, sem que isso comprove infecção local. Não condicionar essa atuação à identificação do atacante, pois um ataque distribuído associado a IP spoofing pode tornar a origem virtualmente impossível de identificar. No segundo ativo, a infecção confirmada exige atuação voltada à remoção do vírus, por deleção do arquivo associado à sua eliminação ou por reinstalação do sistema operacional. Assim, a falha de comunicação direciona a resposta à infraestrutura de rede, enquanto a evidência de infecção fundamenta a erradicação no sistema afetado; uma medida não substitui a outra.

**dificil_B · medido difícil · APROVADA**  
_Nota(s): Arquitetura integrada de redes e acesso remoto em sistemas digitais de FPSO; Gestão de alarmes como suporte à decisão para prevenir trips e shutdowns; Integridade operacional por alarmes, IHMs e diagnósticos de automação em ambientes IT/OT_

**P:** Após ampliar a integração entre redes operacionais e corporativas de um FPSO, o suporte em terra relata indisponibilidade de informações, enquanto a operação embarcada recebe muitos alarmes e não consegue identificar a origem dos desvios. O excesso de alarmes já existia em regime normal antes da ampliação, e os controladores lógicos programáveis (CLPs) antigos não disponibilizam diagnósticos nas interfaces homem-máquina (IHMs). Durante uma perturbação, a equipe propõe corrigir apenas a conectividade para recuperar o apoio operacional. Essa prioridade é suficiente? Como distinguir as causas e orientar a recuperação do suporte à decisão?

**R:** Não. A indisponibilidade em terra exige avaliar a coleta e a disponibilização remota das informações na arquitetura integrada, mas não explica, por si só, o excesso de alarmes preexistente nem a ausência de diagnósticos a bordo. A integração favorece a identificação de causas-raiz; não substitui uma configuração adequada de alarmes e diagnósticos. Deve-se confrontar as informações de gerenciamento da rede com os logs de alarmes e o conteúdo apresentado nas IHMs. Os logs permitem analisar a carga de alarmes em operação normal e perturbada; os diagnósticos dos CLPs e dos componentes de rede apoiam a identificação de problemas de automação. A recuperação deve combinar a correção das deficiências de acesso identificadas com a revisão da configuração e padronização dos alarmes e a disponibilização dos diagnósticos em bancos de dados e telas. Recuperar somente a conectividade deixaria o operador com excesso de sinais e lacunas diagnósticas, comprometendo sua capacidade de estabilizar a planta antes da intervenção do sistema instrumentado de segurança (SIS).

### Inspeção e Integridade

**facil · medido fácil · APROVADA**  
_Nota(s): Inspeção Baseada em Risco e efetividade do plano de inspeção na gestão da integridade de FPSOs_

**P:** O que é Inspeção Baseada em Risco (IBR/RBI) e como ela utiliza a probabilidade e a consequência de falha para priorizar a inspeção e a manutenção de equipamentos em uma unidade de processo?

**R:** A IBR/RBI é uma metodologia que utiliza o risco como critério para orientar decisões de inspeção e manutenção. Ela combina avaliações qualitativas e quantitativas da probabilidade e da consequência de falha para determinar quais equipamentos devem receber atenção prioritária, em vez de distribuir os recursos uniformemente. Os planos devem ser coerentes com os mecanismos de dano de cada equipamento, incorporando o histórico operacional para atualizar a avaliação de risco.

**media · medido média · APROVADA**  
_Nota(s): Inspeção Baseada em Risco e efetividade do plano de inspeção na gestão da integridade de FPSOs_

**P:** Em uma unidade de processo de um FPSO, novas inspeções revelam uma evolução do dano diferente da considerada no planejamento, e o histórico registra mudanças nas condições de operação. Por que o plano de inspeção deve ser reavaliado e quais aspectos devem orientar essa revisão?

**R:** Os novos resultados e as mudanças operacionais devem ser incorporados ao histórico do equipamento para atualizar a avaliação de risco. Como o plano precisa ser coerente com os mecanismos de dano atuantes, manter o planejamento anterior sem reavaliação pode deixar a inspeção inadequada ao dano esperado. A revisão deve verificar a compatibilidade dos métodos com esses mecanismos, a capacidade de detectar e dimensionar o dano, a probabilidade de detecção e o nível de amostragem. Com base no risco atualizado, devem ser reavaliadas a prioridade do equipamento e a combinação de métodos e frequências, considerando a efetividade na redução da probabilidade de falha e o custo da inspeção.

**dificil_A · medido difícil · APROVADA**  
_Nota(s): Inspeção estrutural do casco e do envelope externo com foco em estanqueidade, corrosão e perda de seção_

**P:** Um FPSO operando no Reino Unido planeja uma inspeção subaquática em substituição à docagem (UWILD), mas o escopo proposto limita-se ao exame visual externo do casco. Há indícios de corrosão em compartimentos internos e nas interfaces entre costado, suportes e topo do tanque no espaço de máquinas; as válvulas de casco e suas tubulações associadas ficaram fora do programa. Esse escopo permite demonstrar a preservação do envelope do casco? Justifique a decisão e indique como integrar as verificações necessárias ao planejamento da UWILD.

**R:** Não. O exame visual externo isolado não demonstra simultaneamente a integridade estrutural e a estanqueidade do envelope. Para a UWILD planejada, deve ser desenvolvido e implementado um plano formal de inspeção de integridade do envelope externo. A verificação estrutural deve abranger os compartimentos internos pertinentes, com atenção especial à chapa do costado junto aos suportes que conectam as estruturas laterais ao topo do tanque e às anteparas do espaço de máquinas junto ao topo do tanque e aos poços de bilge. O exame deve identificar corrosão substancial, deformações significativas, fraturas e outros danos, sendo complementado por medições de espessura e testes conforme necessário. Em paralelo, arranjos adequados de inspeção devem cobrir todas as conexões laterais do casco, incluindo válvulas e tubulações associadas, para manter a estanqueidade. Assim, a UWILD integra o plano do envelope externo sem substituir as verificações necessárias da estrutura interna e das conexões com o mar.

**dificil_B · medido difícil · APROVADA**  
_Nota(s): Monitoramento do desempenho da proteção catódica e critérios de intervenção; Inspeção e manutenção da integridade de revestimentos em tanques e no envelope externo do casco; Avaliação de integridade de tanques por espessura, revestimento e proteção catódica_

**P:** Em um FPSO de casco simples, um tanque que armazenou água produzida apresenta perda localizada de espessura, embora as medições ainda superem a espessura mínima estrutural calculada. Nessas regiões, o revestimento compósito apresenta falhas de adesão; os ânodos de sacrifício estão desgastados e a eficácia da proteção catódica não foi comprovada por medições recentes. A equipe propõe apenas acompanhar a espessura, alegando que o mínimo estrutural não foi atingido. Qual deve ser a prioridade técnica e o escopo da avaliação antes de aceitar essa proposta?

**R:** Deve-se priorizar uma avaliação integrada, sem aceitar o simples acompanhamento apenas porque a espessura supera o mínimo estrutural. É necessário comparar a espessura remanescente com a espessura mínima acrescida da sobreespessura prevista para corrosão, verificando a margem disponível. As falhas de adesão podem romper o revestimento e acelerar a corrosão; o desgaste dos ânodos exige verificar se a proteção catódica permanece eficaz. Portanto, o dano medido não deve ser tratado como estabilizado enquanto houver dúvida sobre ambas as barreiras. A avaliação deve abranger a integridade estrutural, a extensão dos defeitos do revestimento e a funcionalidade da proteção catódica, mediante inspeção do potencial, da corrente e da condição física dos ânodos. A decisão entre acompanhamento e reparo deve considerar conjuntamente a margem estrutural e o controle da corrosão. Confirmada despolarização, é necessária ação corretiva, não apenas monitoramento da espessura.

### Instrumentação, Controle e Automação

**facil · medido média · APROVADA**  
_Nota(s): Integridade metrológica e manutenção de instrumentos por condição_

**P:** Por que a calibração periódica manual de instrumentos pode reduzir a disponibilidade do processo e nem sempre ser a melhor estratégia de manutenção?

**R:** Porque frequentemente exige parada do processo ou retirada dos instrumentos de operação. Além disso, a intervenção manual pode afetar adversamente a confiabilidade do instrumento, mesmo quando a calibração não é necessária. Por isso, validar as leituras e determinar o estado de funcionamento dos sensores é importante para avaliar a necessidade de intervenção, em vez de depender apenas da periodicidade fixa.

**media · medido fácil · APROVADA**  
_Nota(s): Integridade metrológica e manutenção de instrumentos por condição_

**P:** Sob condições de medição constantes, um instrumento apresenta elevada dispersão entre leituras sucessivas, sem deslocamento progressivo; outro mantém baixa dispersão no curto prazo, mas suas leituras se deslocam lentamente ao longo do tempo. Qual padrão indica problema de repetibilidade e qual indica deriva?

**R:** A elevada dispersão entre leituras sucessivas indica problema de repetibilidade, que corresponde à estabilidade no curto prazo. O deslocamento lento das leituras do segundo instrumento, apesar da baixa dispersão no curto prazo, é compatível com deriva: uma variação lenta das características metrológicas, associada à estabilidade de longo prazo. Portanto, boa repetibilidade não exclui deriva.

**dificil_A · medido difícil · APROVADA**  
_Nota(s): Integração de sinais de campo para redes digitais e supervisão Web_

**P:** Em uma unidade offshore, um transmissor HART sobre 4–20 mA foi integrado à rede FOUNDATION Fieldbus por um conversor de corrente, e sua variável já está disponível na automação. Entretanto, ela não aparece no cliente Web, cuja base é um servidor OPC-DA (servidor de acesso a dados de processo). A equipe propõe substituir o conversor para resolver a ausência na supervisão. Qual etapa deve ser priorizada no diagnóstico e por que a conexão à rede digital não garante a disponibilização fim a fim?

**R:** Deve-se priorizar a verificação do mapeamento, do endereçamento padronizado e do armazenamento da variável no servidor OPC-DA, além de sua disponibilização pela aplicação cliente Web. A presença da variável na automação indica que a conversão de corrente para FOUNDATION Fieldbus já cumpre sua função de interligar o instrumento ao barramento digital; portanto, a ausência apenas na supervisão não justifica, por si só, substituir o conversor. As duas camadas resolvem necessidades distintas: a primeira torna o sinal disponível à rede de automação; a segunda organiza e disponibiliza os dados para consumo pela aplicação supervisória. A disponibilização fim a fim depende de ambas, e o sucesso da conversão não substitui o tratamento dos dados no servidor e sua publicação Web.

**dificil_B · medido difícil · APROVADA**  
_Nota(s): Medição de nível por radar de onda guiada e medição de interface por densidade com medidores nucleônicos; Desempenho metrológico e resposta dinâmica de instrumentos de processo; Seleção e aplicação de instrumentação e elementos finais de controle no processo_

**P:** Em um separador trifásico de FPSO, mudanças de composição enfraquecem o eco do radar de onda guiada, enquanto a interface água–óleo varia rapidamente. Um medidor nucleônico próximo à saída de água fornece a interface ao controlador e ao desarme por interface extremamente baixa, mas sua indicação apresenta atraso durante os transientes. Para reduzir as oscilações, propõe-se aumentar a filtragem desse sinal e substituir a válvula modulante por uma liga-desliga. Essa proposta é tecnicamente coerente ou deve ser revista, considerando conjuntamente a medição, o controle e a proteção?

**R:** A proposta deve ser revista. O radar depende do contraste dielétrico para produzir um eco adequado; portanto, sua indicação de nível não deve ser tomada automaticamente como representação confiável da interface nas condições descritas. A medição nucleônica por densidade atende ao fenômeno de interface e, nessa configuração, alimenta tanto o controle quanto o desarme, mas a adequação física não elimina a necessidade de resposta dinâmica compatível.

O atraso observado exige avaliar a dinâmica do sistema de medição e as influências da instalação. Aumentar a filtragem sem essa avaliação pode suprimir variações relevantes, em vez de apenas ruído, comprometendo a informação usada pelo controlador e pela proteção.

A válvula liga-desliga também não é adequada ao objetivo de controle proporcional. Deve-se avaliar a cadeia completa: confiabilidade da interface medida, resposta temporal para os transientes e para a condição crítica, e capacidade da válvula modulante de responder ao comando e suportar o serviço. Uma leitura mais suave, isoladamente, não demonstra controle adequado nem proteção confiável.

### Manutenção e Plano de Manutenção

**facil · medido fácil · APROVADA**  
_Nota(s): FMEA/FMECA como base para definir estratégia e plano de manutenção de ativos críticos_

**P:** O que a análise de modos, efeitos e criticidade de falhas (FMEA/FMECA) identifica em equipamentos críticos e por que deve partir da função e das falhas funcionais até examinar modos, efeitos e consequências?

**R:** A análise identifica modos de falha e de deterioração dos equipamentos críticos. O encadeamento começa pela função e pelo padrão de desempenho esperado, identifica as falhas funcionais, detalha os modos de falha e suas causas, descreve os efeitos e analisa as consequências. Isso permite compreender como ocorre a perda de função e quais consequências ela produz. Detalhar as causas evita que as ações tratem apenas os sintomas. Para equipamentos de maior criticidade, a análise dos modos de falha, combinada com dados de confiabilidade, subsidia a escolha da técnica de manutenção.

**media · medido fácil · APROVADA**  
_Nota(s): FMEA/FMECA como base para definir estratégia e plano de manutenção de ativos críticos_

**P:** Em um FPSO, a revisão do histórico de serviços e dos indicadores do sistema de gestão da manutenção, apoiada por resultados de FMEA, identificou tarefas de um plano existente que precisam de ajuste, necessidades de manutenção ainda não cobertas por planos e sobressalentes necessários que não constam do estoque. Que recomendações a engenharia deve encaminhar à gestão de manutenção para atender a esses achados?

**R:** A engenharia deve recomendar a melhoria do plano existente para ajustar as tarefas identificadas, a criação de novos planos para as necessidades de manutenção ainda não cobertas e a inclusão em estoque dos sobressalentes apontados como necessários. Cada recomendação deve ser fundamentada nos achados da análise do histórico e dos indicadores do sistema, apoiados pelos resultados da FMEA, vinculando as alterações propostas às necessidades identificadas.

**dificil_A · medido difícil · APROVADA**  
_Nota(s): Verificação operacional de barreiras e retorno seguro após manutenção_

**P:** Após manutenção no sistema de armazenamento de um FPSO, o supervisório indica barreiras disponíveis, mas a inspeção física identifica uma válvula crítica fora da posição normal e um isolamento temporário ainda instalado. A comparação com o projeto confirma que o arranjo dos tanques de carga e de armazenamento de água não foi restabelecido. A equipe propõe retomar a operação com uma contingência cuja suficiência diante dessas indisponibilidades ainda não foi avaliada. Qual decisão deve ser tomada e quais condições precisam ser atendidas para justificar o retorno ao serviço?

**R:** Não liberar o retorno ao serviço nas condições apresentadas. A indicação no supervisório não confirma a disponibilidade das barreiras quando a inspeção física revela desalinhamentos e a comparação com o projeto aponta que o arranjo não foi restabelecido. É necessário recompor e verificar a configuração, incluindo a remoção do isolamento temporário e o retorno da válvula crítica à posição normal. Se permanecerem degradações ou indisponibilidades de elementos críticos, a continuidade dependerá de demonstrar que as contingências mantêm os riscos em níveis aceitáveis, considerando essas limitações. Se forem insuficientes, deve-se prever a parada do equipamento, do sistema ou, conforme necessário, da planta de processo.

**dificil_B · medido difícil · APROVADA**  
_Nota(s): Dimensionamento e priorização de sobressalentes críticos por risco, falha e lead time; Integração do plano de manutenção com materiais, suprimentos, custos e conformidade em CMMS/SAP PM; Planejamento de manutenção e provisão de recursos para reduzir indisponibilidades_

**P:** Em um FPSO, a falha de um componente associado a uma barreira operacional exigiu reparo simples, mas a restauração demorou principalmente pela espera de material comprado somente após a falha. O componente tem baixo consumo histórico e longo prazo de aquisição e disponibilização a bordo; compras emergenciais semelhantes são recorrentes, embora as ordens sejam emitidas regularmente no sistema informatizado de gestão da manutenção (CMMS). A gerência propõe priorizar a redução do tempo de reparo em campo e manter o estoque baseado no consumo passado. Qual diagnóstico e mudança de prioridade são mais adequados para reduzir a indisponibilidade?

**R:** O quadro aponta principalmente para deficiência de prontidão logística e integração do planejamento com suprimentos, não para demora do reparo físico. A emissão regular de ordens não assegura disponibilidade de materiais; compras decididas após a falha prolongam a espera e podem introduzir erros de especificação e de requisitos de qualidade. A prioridade deve ser revisar a criticidade e o dimensionamento dos sobressalentes considerando risco do cenário associado à barreira, taxa de falha, população instalada, consequência da falha e prazo de aquisição e disponibilização a bordo. Baixo consumo histórico, isoladamente, não justifica baixa prontidão para um item de longo prazo de reposição. Essa análise deve alimentar o ressuprimento informatizado e a preparação das ordens, integrando planejamento e materiais para antecipar aquisições e assegurar os itens necessários à programação. Assim, atua-se sobre a espera que domina a indisponibilidade, sem comprometer a segurança; acelerar apenas o reparo não elimina a falta de peças.

## Segurança Ocupacional, Saúde e Meio Ambiente

### Condições Ambientais e Impactos Operacionais

**facil · medido fácil · APROVADA**  
_Nota(s): Falha de risers: escalonamento do dano, perda de contenção e avaliação de consequências ambientais_

**P:** Por que a falha de um riser que transporta petróleo pode caracterizar perda de contenção com potencial de liberação de hidrocarbonetos ao ambiente marinho?

**R:** Porque a falha pode permitir que os produtos transportados escapem do riser e sejam liberados no ambiente marinho. Quando há esse escape, ocorre perda de contenção: o petróleo deixa de permanecer confinado na linha e pode contaminar o meio receptor.

**media · medido média · APROVADA**  
_Nota(s): Falha de risers: escalonamento do dano, perda de contenção e avaliação de consequências ambientais_

**P:** Um riser flexível sofre ruptura total no trecho submerso, com possibilidade de atingir estruturas e risers de produção adjacentes. Como essa condição pode transformar a falha inicial em um acidente de maior abrangência?

**R:** A ruptura inicial pode causar danos às estruturas e aos risers adjacentes, provocando novos rompimentos e consequente liberação de óleo para o mar. Assim, o evento deixa de se limitar ao riser inicialmente rompido e passa a envolver comprometimento de estruturas, perda de contenção em outras linhas e potencial ampliação da liberação de óleo.

**dificil_A · medido difícil · APROVADA**  
_Nota(s): Temperatura ambiente na adequação de sistemas de monitoramento de gases_

**P:** Em uma sala de um FPSO próxima à exaustão, a carga do processo e a temperatura local variam ao longo do dia. A ventilação e a composição do fundo gasoso também mudam entre os regimes, e o sensor, antes exposto apenas esporadicamente, passa a acompanhar toda a operação. A equipe propõe manter o sistema porque sua faixa atende às medições feitas com baixa carga e à temperatura externa de projeto. Esse critério é suficiente ou a adequação deve ser reavaliada, e quais condições devem orientar a decisão?

**R:** O critério é insuficiente: atender às medições em baixa carga e à temperatura externa não demonstra adequação às condições locais de toda a operação. Deve-se reavaliar o processo monitorado e seus regimes, considerando a temperatura efetiva na sala próxima à exaustão, as variações diurnas e sazonais e os valores de medição em condições diferentes das normais. As condições de ventilação, composição do fundo gasoso e exposição descritas devem integrar a caracterização desses regimes, sem presumir que a condição de baixa carga represente as demais. A decisão de manter o sistema deve depender da compatibilidade de sua faixa e de seu fundo de escala com as condições efetivas avaliadas, e não apenas com o ponto operacional inicialmente medido.

**dificil_B · medido difícil · APROVADA**  
_Nota(s): Dispersão ambiental, monitoramento e modelagem de consequências em FPSOs: efeito de vento, geometria, temperatura e composição do meio; Temperatura ambiente na adequação de sistemas de monitoramento de gases; Detecção, lógica de automação e shutdown sob interferência, fogo, fumaça e necessidade de resposta de emergência_

**P:** Em um módulo de processo de FPSO, alarmes intermitentes de gás coincidem com mudanças de regime, aquecimento local e alterações da direção do vento entre equipamentos. Verificações posteriores não confirmam concentração persistente, e uma simulação reproduz a velocidade média, mas não as concentrações locais. A recorrência reduz a confiança dos operadores, que propõem reclassificar os alarmes como eventos sem atuação automática. Que diagnóstico integrado deve orientar a decisão sobre essa proposta e a cadeia de resposta?

**R:** A proposta não deve ser aceita apenas pela ausência de concentração persistente nas verificações posteriores: permanecem duas hipóteses, dispersão local variável e inadequação da medição. É necessário avaliar vento e geometria, pois estruturas vorticais podem alterar o transporte e a concentração; reproduzir velocidade média não valida a previsão de concentração. Se esta for decisiva, a simulação de grandes escalas (LES) tem melhor suporte que a abordagem RANS nas comparações apresentadas. Em paralelo, deve-se verificar a temperatura efetiva no ponto monitorado, o regime operacional e a compatibilidade do fundo de escala, além das espécies gasosas capazes de causar interferência. Essas avaliações devem orientar a revisão da configuração de alarmes e eventos e da matriz causa-efeito: pseudoalarmes atrasam o reconhecimento, mas erros de medição também comprometem a entrada da lógica. A atuação da parada de emergência não demonstra, sozinha, a completude da resposta; é preciso verificar o alarme geral e os comandos de ventilação que previnem propagação para áreas ocupadas.

### Gestão de Pessoas e Treinamento

**facil · medido fácil · APROVADA**  
_Nota(s): Governança do programa de treinamento como base para avaliar eficácia, retenção e conformidade_

**P:** Qual é a diferença entre a matriz de treinamentos mandatórios gerais e a matriz de treinamentos em procedimentos operacionais por função em um FPSO, e o que cada uma permite comprovar?

**R:** A matriz de treinamentos mandatórios gerais controla a cobertura dos cursos obrigatórios da força de trabalho, mas não comprova treinamento nos procedimentos operacionais específicos de cada função. A matriz de procedimentos operacionais controla essa capacitação específica. Para comprovar o treinamento efetivamente realizado, ambas precisam estar implementadas e apoiadas por registros: a existência da matriz, isoladamente, não demonstra que o trabalhador recebeu treinamento adequado às suas funções. Assim, registros de cursos gerais não substituem as evidências de treinamento nos procedimentos executados a bordo.

**media · medido média · APROVADA**  
_Nota(s): Governança do programa de treinamento como base para avaliar eficácia, retenção e conformidade_

**P:** Em uma instalação offshore permanentemente ancorada no setor britânico do Mar do Norte, a matriz de competências marítimas não acompanha a situação atual da equipe, mas continua sendo usada para escalar pessoal e apresentar evidências em auditorias. Como essa desatualização afeta essas decisões e a demonstração de conformidade?

**R:** A matriz deve refletir o status real das competências marítimas para permitir verificar se os requisitos continuam atendidos. Quando desatualizada, deixa de oferecer uma base confiável para essa verificação: a escalação pode ser feita sem confirmação de que as competências requeridas estão atendidas, e a auditoria não consegue usar a matriz como evidência confiável da situação atual. Portanto, ela não sustenta, por si só, a demonstração de conformidade. É necessário atualizá-la para representar as competências reais antes de utilizá-la como fundamento dessas decisões. No contexto britânico apresentado, esse critério corresponde à orientação do HSE, órgão de saúde e segurança do Reino Unido.

**dificil_A · medido difícil · APROVADA**  
_Nota(s): Gestão de competências, critérios por função e treinamento em instalações offshore_

**P:** Em um FPSO, operadores acumulam funções de tratamento de gás, óleo e utilidades, mas as descrições de cargo exigem apenas “experiência operacional”, sem requisitos por função ou matriz específica. Supervisores são escolhidos pela capacidade de coordenação, sem critérios formais de competência para o papel. Há documentos de treinamento desatualizados, embora existam efetivo e tempo disponíveis para qualificação. Qual deficiência deve ser priorizada no diagnóstico, em vez de atribuir o problema imediatamente à falta de recursos ou à avaliação dos trabalhadores?

**R:** Deve ser priorizada a definição insuficiente dos padrões de competência por função. A exigência genérica de experiência não explicita formação, treinamento, experiência, habilidades e conhecimentos necessários a cada papel; além disso, o acúmulo de funções exige matriz específica. A seleção de supervisores pela coordenação, sem critérios formais, reforça essa lacuna. A disponibilidade de efetivo e tempo torna a insuficiência desses recursos menos consistente como causa predominante nas condições apresentadas. Antes de concluir que os trabalhadores são inadequadamente qualificados ou avaliados, é necessário estabelecer os requisitos contra os quais sua competência será verificada. A prioridade é explicitar requisitos por função, contemplar as funções acumuladas na matriz e definir padrões e arranjos de atendimento para posições-chave sem requisitos formalmente especificados.

**dificil_B · medido difícil · APROVADA**  
_Nota(s): Avaliação de competência e assurance baseados em evidências; Métodos de avaliação e fechamento de lacunas de competência; Critérios objetivos para demonstrar eficácia de treinamento e retenção de competência_

**P:** Em um FPSO, a equipe concluiu a reciclagem periódica, mantém certificados válidos e foi aprovada em testes gerais. Entretanto, observações práticas e exercícios de mesa mostram erros recorrentes em etapas específicas de procedimentos críticos, embora as demais etapas sejam executadas corretamente. A gestão propõe manter a liberação integral e repetir o curso completo na próxima reciclagem. Que decisão e revisão do processo de avaliação permitiriam demonstrar a eficácia real do treinamento sem repetir indiscriminadamente o conteúdo já dominado?

**R:** Não manter a liberação integral apenas com base em certificados e aprovação geral: as falhas observadas impedem considerar demonstrada a competência nas etapas afetadas. A decisão sobre o escopo de atuação deve se apoiar em evidências de atendimento aos padrões da função. Identificar e registrar as lacunas por etapa ou área, combinando perguntas e testes específicos, observação prática e cenários que explorem as condições em que os erros ocorrem. O método e a documentação devem ser proporcionais à criticidade. Comunicar as áreas deficientes ao trabalhador e ao empregador, realizar treinamento adicional direcionado e reavaliar as partes deficientes antes de considerá-las atendidas, sem exigir automaticamente a repetição das áreas já demonstradas. Para comprovar manutenção da competência, monitorar o desempenho posterior e reavaliar áreas-chave, com reciclagem diferenciada para procedimentos críticos. Certificados comprovam qualificação formal, mas não substituem essa demonstração; resultados globais não localizam suficientemente as lacunas que exigem correção.

### Meio Ambiente, Gestão Ambiental e Sustentabilidade

**facil · medido fácil · APROVADA**  
_Nota(s): Gestão ambiental operacional e prontidão para prevenção e resposta a impactos marinhos_

**P:** Qual é a função de sistemas rigorosos de gestão de saúde, segurança, social e ambiental na redução dos riscos e impactos das operações offshore sobre o ambiente marinho?

**R:** Esses sistemas fornecem capacidade para avaliar e minimizar os riscos das operações offshore e desenvolver processos que reduzam os impactos negativos sobre o ambiente marinho.

**media · medido média · APROVADA**  
_Nota(s): Gestão ambiental operacional e prontidão para prevenção e resposta a impactos marinhos_

**P:** Em um FPSO, há procedimento documentado de resposta a uma emergência ambiental, mas um equipamento de controle da poluição previsto nesse procedimento está indisponível. A existência do procedimento é suficiente para considerar a resposta operacionalmente pronta? Justifique o critério de avaliação.

**R:** Não. A adequação documental exige avaliar a eficácia das normas, dos procedimentos e dos registros de operação e manutenção para a tomada de decisão. A prontidão operacional exige também considerar as condições reais de operação e manutenção dos equipamentos envolvidos. Como o equipamento previsto está indisponível, o procedimento, sozinho, não demonstra capacidade efetiva de resposta; a decisão deve considerar essa limitação operacional.

**dificil_A · medido ? · REPROVADA: codigo:referencia_alternativas**  
_Nota(s): Integração do SGA/SMS à governança de projetos de E&P/FPSO no ciclo de vida de projeto_

**P:** Em um projeto de FPSO, duas opções apresentam desempenho econômico inicial semelhante. A opção A tem menor impacto ambiental na fabricação, mas consome mais recursos e utiliza processos de maior impacto na operação, com maior exposição a emissões e preços de carbono. A opção B tem maior impacto na fabricação, mas reduz o consumo de recursos e emprega processos de menor impacto na operação, com menor exposição ao risco de carbono. Qual critério deve orientar a escolha e em que condição a opção B deve ser priorizada?

**R:** A escolha deve considerar a carga ambiental do ciclo de vida, e não apenas o impacto da fabricação ou o desempenho econômico inicial. A opção B deve ser priorizada se a avaliação das diferentes fases demonstrar que a redução do consumo de recursos e o uso de processos de menor impacto compensam seu maior impacto na fabricação, reduzindo a carga ambiental do ciclo de vida. A decisão também deve incorporar o risco de carbono, considerando emissões, efeitos dos preços de carbono e mudanças climáticas. Assim, a menor exposição operacional de B favorece sua escolha, mas não dispensa a comparação integrada dos impactos ao longo do ciclo de vida.

**dificil_B · medido difícil · APROVADA**  
_Nota(s): Conformidade legal, licenciamento ambiental e tratamento de não conformidades em FPSO/FSO; Monitoramento ambiental de emissões atmosféricas, efluentes e indicadores de sustentabilidade; Indicadores de água produzida e efluentes oleosos: monitoramento em linha, seleção de medidores, validação do tratamento e reuso_

**P:** Um FPSO possui licença ambiental válida cuja condicionante exige comprovar a qualidade da água produzida descartada por análise gravimétrica de óleo e graxas. O teor de óleos e graxas (TOG) em linha permanece estável, orienta os ajustes do tratamento e é usado como única evidência nos relatórios de conformidade. Uma auditoria identifica que a compatibilidade do medidor com o óleo e a faixa de concentração da unidade não foi demonstrada. Que diagnóstico e prioridade de ação devem orientar o operador antes de considerar o descarte conforme ou atribuir o problema ao tratamento?

**R:** O diagnóstico é de conformidade não demonstrada, e não necessariamente de falha do tratamento: licença válida e sinal estável não comprovam o cumprimento da condicionante. A prioridade é verificar as exigências do licenciamento e alinhar a comprovação ao parâmetro e ao método gravimétrico exigidos, sem substituir essa evidência pelo indicador em linha. Em paralelo, deve-se caracterizar o óleo e a água oleosa, estabelecer a faixa de concentração e verificar a compatibilidade da técnica do medidor. O TOG em linha pode apoiar o controle operacional, mas sua estabilidade não resolve essas lacunas. Somente com evidência analítica adequada será possível distinguir deficiência de monitoramento de desempenho insuficiente do tratamento. O operador deve formalizar o tratamento da não conformidade em plano com responsáveis, prazos e ações proporcionais ao risco e ao impacto ambiental. Alterações decorrentes devem ser registradas e atender às exigências legais, com revisão de procedimentos e capacitação quando necessárias.

### Saúde Ocupacional

**facil · medido média · APROVADA**  
_Nota(s): Vigilância médica ocupacional em cenários de surtos e pandemias offshore_

**P:** Qual é a função de um programa de vigilância médica ocupacional offshore além do acompanhamento clínico individual, e como ela se relaciona com a continuidade operacional?

**R:** Sua função é transformar informações sobre agravos à saúde em investigação, ações corretivas para prevenir recorrência e acompanhamento da eficácia das medidas adotadas. Além de proteger os trabalhadores, o programa apoia a continuidade operacional ao orientar medidas para lidar com a indisponibilidade de profissionais-chave, como lideranças de bordo, médicos, enfermeiros e técnicos de segurança. Assim, conecta o acompanhamento da saúde à resposta organizacional necessária para sustentar a operação.

**media · medido média · APROVADA**  
_Nota(s): Vigilância médica ocupacional em cenários de surtos e pandemias offshore_

**P:** Em um FPSO, agravos à saúde foram notificados e medidas corretivas foram propostas, mas não há registros de execução nem avaliação dos resultados. Como deve ser completado o encadeamento da vigilância médica para que essas notificações resultem em controle efetivo?

**R:** As notificações devem levar à investigação efetiva dos agravos, verificando se as medidas propostas são pertinentes às causas identificadas e à prevenção de recorrência. Em seguida, as ações corretivas devem ser rastreadas e executadas, com rotinas e registros que permitam comprovar sua implementação. Depois, é necessário acompanhar periodicamente os resultados para verificar a eficácia das medidas e decidir se controles adicionais são necessários. A simples proposta de ações não comprova execução, e a execução, isoladamente, não substitui a avaliação de eficácia.

**dificil_A · medido difícil · APROVADA**  
_Nota(s): Gestão de casos de doença, restrições e retorno seguro ao trabalho offshore_

**P:** Em um FPSO, um trabalhador com suspeita de doença infecciosa foi afastado, mas continua circulando pelas áreas comuns. Outro trabalhador foi afastado por executar atividades em ambiente comprovadamente em desconformidade com os padrões operacionais, sem suspeita de infecção. A coordenação propõe tratar ambos apenas pelo mesmo fluxo administrativo de afastamento e retorno. Que prioridade técnica deve orientar cada caso e por que essa proposta é insuficiente?

**R:** No primeiro caso, a prioridade é controlar o possível caso infeccioso: conectar o monitoramento de saúde ao isolamento e ao impedimento de circulação, com comunicação clara ao pessoal de bordo, sanitização, manejo do caso e protocolo de retorno ao trabalho. O afastamento, sozinho, não resolve a circulação de uma pessoa potencialmente infectada. No segundo caso, a prioridade deve recair sobre a condição operacional em desconformidade associada ao afastamento, e não sobre medidas de controle de infecção sem suspeita correspondente. Esse afastamento representa uma consequência de falha do contexto operacional. O fluxo administrativo comum é insuficiente porque não trata os fatores distintos que sustentam cada caso: possível infecção e circulação no primeiro; ambiente operacional fora de padrão no segundo.

**dificil_B · medido difícil · APROVADA**  
_Nota(s): Água potável offshore em FPSO/FSO: disponibilidade, controle sanitário e contingência operacional; Prevenção de surtos a bordo por controle de agentes biológicos, água potável, alimentos e interfaces de abastecimento; Planejamento para surtos e contingências sanitárias coletivas em instalações offshore_

**P:** Em um FPSO no Brasil, 8% do efetivo apresenta sintomas gastrointestinais após compartilhar refeições e água, e as ausências comprometem a normalidade operacional. Houve falha de refrigeração e abastecimento recente de água com mangueiras sem desinfecção; entretanto, duas amostras diárias da água de acomodação indicaram residual de biocida de 0,5 ppm. A equipe propõe investigar apenas os alimentos e aguardar 10% de trabalhadores afetados para comunicar o incidente. Qual deve ser a prioridade integrada de investigação e contingência, e essa proposta é adequada?

**R:** A proposta não é adequada. Devem ser investigadas simultaneamente as rotas de água e alimentos: a falha de refrigeração sustenta a suspeita sobre os alimentos, enquanto a ausência de desinfecção das mangueiras mantém relevante a hipótese de contaminação no abastecimento. O residual de 0,5 ppm atende à faixa de referência do HSE britânico, mas não demonstra, isoladamente, que todas as barreiras sanitárias funcionaram nem permite excluir a água como fonte. A resposta deve articular as contingências para refrigeração, surto alimentar e suspeita de contaminação da água, preservando o abastecimento adequado ao consumo e verificando a higiene das mangueiras e dos pontos de uso. Essas referências britânicas não constituem automaticamente exigências brasileiras. No Brasil, a comunicação à ANP não deve aguardar 10%: o comprometimento da normalidade operacional já é critério de enquadramento do surto.

### Segurança Ocupacional

**facil · medido fácil · APROVADA**  
_Nota(s): Trabalhos a quente: fontes de dano, avaliação prévia da área e proteção do trabalhador_

**P:** Quais são os principais perigos associados à solda, ao corte e a outros trabalhos a quente em uma plataforma offshore?

**R:** Os principais perigos são queimaduras por exposição térmica; ignição na presença de vapores inflamáveis; inalação de fumos, gases e vapores, especialmente em ambientes fechados; choque elétrico; exposição à luminosidade excessiva da solda elétrica; e projeção de fagulhas e partículas provenientes do corte.

**media · medido média · APROVADA**  
_Nota(s): Trabalhos a quente: fontes de dano, avaliação prévia da área e proteção do trabalhador_

**P:** Uma soldagem será executada em altura, com exposição à luminosidade do arco e risco de fogo súbito (flash fire). Como relacionar roupa resistente ao fogo, capacete de soldagem com tonalidade adequada e proteção contra quedas aos mecanismos de dano presentes?

**R:** A roupa resistente ao fogo corresponde à proteção contra os efeitos térmicos e à mitigação dos impactos de um fogo súbito. O capacete de soldagem com tonalidade adequada corresponde à proteção contra a luminosidade intensa da solda elétrica. A proteção contra quedas atende ao risco adicional da execução em altura. Os três equipamentos de proteção individual são complementares, pois atendem a mecanismos de dano diferentes presentes na mesma tarefa.

**dificil_A · medido difícil · APROVADA**  
_Nota(s): Diálogos de segurança e governança do PTW/CoW_

**P:** Durante uma intervenção em um FPSO, a equipe altera o método previsto na Permissão para Trabalho (PT), sem analisar os novos perigos nem comunicar a mudança aos demais envolvidos. Um profissional não listado na PT assume a autorização da área, sem comprovação de designação e treinamento para essa função. A supervisão propõe continuar porque a PT está assinada, mas um executante considera a condição insegura. Qual decisão deve ser tomada e quais condições precisam ser restabelecidas antes de prosseguir?

**R:** A decisão é interromper a execução; o executante não deve prosseguir enquanto o desvio inseguro permanecer sem resolução. A PT assinada não demonstra que os perigos e controles continuam adequados após a mudança. Antes de retomar, é necessário avaliar os novos perigos, verificar a adequação da PT e dos controles à condição real e discutir os documentos atualizados com os executantes, comunicando os perigos e as medidas de mitigação aos envolvidos. Também é preciso conferir a correspondência entre as pessoas presentes e as listadas na PT e assegurar que a autorização da área seja exercida por pessoa formalmente designada e treinada para suas responsabilidades. O conjunto indica falha de governança e comunicação do trabalho, não apenas uma irregularidade documental. No contexto brasileiro, a recusa diante de condição insegura deve ser devidamente justificada, mesmo havendo PT e anexos.

**dificil_B · medido difícil · APROVADA**  
_Nota(s): Condição operacional do guindaste e controles prévios ao uso em içamento offshore; Prevenção de contato, enroscamento e queda de objetos na movimentação de cargas; Protocolos de comunicação e coordenação em tarefas críticas de movimentação e içamento_

**P:** Durante um içamento no convés de um FPSO, a carga se aproxima de uma estrutura em um trecho de folga reduzida enquanto o turntable (mesa giratória) gira. A inspeção pré-uso e a certificação foram verificadas, mas o operador, sem visão completa do trecho, percebe resposta diferente da esperada; pelo rádio, observadores divergem entre continuar e corrigir o movimento, sem identificar claramente quem transmite e quem recebe. Qual decisão operacional deve ser tomada e como distinguir as possíveis causas antes de retomar a manobra?

**R:** Não prosseguir enquanto a trajetória e os comandos permanecerem indefinidos; retirar pessoas da linha de fogo e restabelecer os controles antes da retomada. A inspeção e a certificação verificadas não encerram o diagnóstico: avaliar o tipo, a regularidade e a qualidade da manutenção e considerar a mudança do centro de gravidade durante o giro, que pode alterar as condições da operação. Em paralelo, revisar o percurso passo a passo, identificando interferências e folgas críticas, posicionar observadores adicionais nos pontos potenciais de contato ou enroscamento e definir zonas de queda e zonas seguras. Esclarecer os papéis, identificar emissor e destinatário no rádio, alinhar o protocolo de falha de comunicação e usar comandos inequívocos com verificação do deslocamento durante todo o içamento. A aproximação da estrutura não permite atribuir isoladamente a causa ao guindaste: comportamento da carga, planejamento da trajetória e coordenação devem ser avaliados conjuntamente.
