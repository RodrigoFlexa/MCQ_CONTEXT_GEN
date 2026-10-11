AVISO: os trechos disponíveis tratam principalmente de unidades com posicionamento dinâmico e são incompletos para o recorte de FPSO ancorado; não há conteúdo específico útil sobre tensão de linhas de ancoragem, nem detalhamento de limites operacionais, alarmes, tendências ou critérios quantitativos de perda de capacidade de station keeping.

**Arquitetura**

O sistema DP é descrito como responsável por determinar a posição atual da unidade em comparação com um objetivo pré-determinado e gerar sinais de controle para os thrusters propulsores executarem a correção do desvio de posição. Sua arquitetura é dividida em quatro subgrupos: sistemas de referência de posição, responsáveis por determinar a posição da unidade em um dado momento; sistemas de sensores, que auxiliam o posicionamento; controladores/computadores, que recebem os dados dos referenciais e sensores, processam a posição da unidade em relação ao objetivo e enviam comandos aos thrusters; e UPS, responsável por manter alimentação ininterrupta aos equipamentos do sistema por meio de banco de baterias.

A segurança operacional é associada ao critério de redundância. As unidades DP são descritas como possuindo pelo menos dois equipamentos para cada subsistema de sensores, computadores e UPS, além de normalmente três sistemas de referência de posição. Os estados operacionais da unidade expressam o grau de comprometimento da sua capacidade operacional em um determinado instante.

**Referenciais de posição**

Entre os principais referenciais de posição citados estão DGPS, referenciais acústicos e radioposicionamento. O GPS é apresentado como um sistema de posicionamento baseado em satélites, com determinação das variáveis de posição e tempo por triangulação; o uso de mais satélites aumenta a precisão. O DGPS aumenta a precisão do GPS por meio de correções aplicadas ao sinal a partir de estações fixas com coordenadas conhecidas, eliminando erros embutidos por degradação atmosférica. Essas correções são transmitidas à unidade por radiofrequência, com alcance limitado e sujeita à degradação atmosférica, ou por link satelital.

Para compensar o balanço da unidade e a distância entre antenas e a locação real, o sinal DGPS é corrigido com informações de giroscópios e da VRU. Também são citados referenciais acústicos, incluindo HPR/Hipap e arranjos LBL, SBL e SSBL/USBL. Em sistemas combinados, sensores no fundo e na embarcação são operados em conjunto para que um sistema compense desvantagens do outro, melhorando a precisão do posicionamento.

O sinal acústico está sujeito a perdas por espalhamento, absorção, difusão, atenuação, reflexão e refração, com intensificação à medida que aumenta a lâmina d’água de operação. Ainda assim, a precisão típica é indicada como menor que <NUMBER> da LDA. Segundo o material, essa precisão, somada à robustez e à independência de equipamentos externos quando comparado ao DGPS, faz com que o sistema acústico tenha prioridade de escolha pelo controlador, sendo o principal sistema em unidades DP. O radioposicionamento por micro-ondas a partir de estações fixas apresenta limitações de alcance e degradação atmosférica, mas pode atingir precisão de <NUMBER> m.

**Heading, movimentos e vento**

O aproamento da embarcação é medido por giroscópios, enquanto os movimentos de pitch, roll e heave são medidos por sensores de movimento, como MRUs/VRUs. A direção e intensidade do vento são medidas por anemômetros. As informações de aproamento e movimentos da unidade são utilizadas para corrigir os referenciais de posição GPS, DGPS e HPR. Já a velocidade e direção do vento são usadas pelo controlador DP para estimar a força resultante do vento sobre a embarcação.

No arranjo descrito, há giroscópios identificados como Gyro-1, Gyro-2 e Gyro-3, cujos sinais alimentam os controladores DP e também sistemas como DGPS, DARPS e Hipap. Os sistemas Hipap recebem combinações de dois giroscópios, caracterizando dupla redundância. Os sensores de movimento MRU-1, MRU-2 e MRU-3, do tipo Seatex MRU-5, medem roll, pitch e heave da embarcação.

Os giroscópios são apontados como os sensores mais importantes para o posicionamento dinâmico, porque uma falha nesse sistema de referência leva à perda de aproamento da embarcação. Por isso, o arranjo descrito opera com redundância tripla de sensores e dupla redundância de alimentação para o sistema DP.

**Filtragem e continuidade**

O uso de algoritmos de filtragem Kalman é associado a alta precisão, estabilidade e economia no emprego dos thrusters quando comparado a controladores PID. Essa técnica atribui ao controlador um caráter preditivo, denominado dead-reckoning mode, permitindo manter a posição estável por vários minutos mesmo sem sinal proveniente do sistema de referência. No contexto de monitoramento da posição, isso caracteriza uma capacidade temporária de continuidade operacional diante da perda de referenciais.

**Falhas e degradação da capacidade**

Foram identificados <NUMBER> modos de falha para as estações de controle DP, incluindo não aceitar comando do operador, falha de exibição de dados, perda do console, falha de rede e corrupção de software. Em termos de monitoramento da capacidade de station keeping, os trechos disponíveis permitem associar degradação da capacidade operacional à perda ou corrupção de sinais de referência, falhas em giroscópios com consequente perda de aproamento, falhas em consoles e rede, e indisponibilidade de sensores usados para corrigir referenciais e estimar cargas ambientais de vento.

O material disponível não apresenta lógica de alarmes, análise de tendências, limites de offset, limites de heading ou critérios quantitativos para identificação formal de perda de capacidade de station keeping, mas indica que os estados operacionais da unidade são o mecanismo usado para expressar o quanto essa capacidade está comprometida em cada instante.