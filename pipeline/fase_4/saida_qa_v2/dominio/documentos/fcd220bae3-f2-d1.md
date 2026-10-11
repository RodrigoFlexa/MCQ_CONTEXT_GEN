AVISO: os trechos são predominantemente sobre unidades com posicionamento dinâmico, não sobre FPSO ancorado, e não trazem conteúdo útil sobre tensão de linhas de ancoragem; consolida-se abaixo apenas o que é aplicável a referência, monitoramento de posição e identificação de perda de capacidade de station keeping.

**Referências de posição**

O sistema de posicionamento reúne sistemas de referência de posição, sensores auxiliares, controladores e propulsão. Entre as referências citadas estão DGPS, sistemas acústicos, sensores de inclinação e direção, além de instrumentos de heading, como bússolas e giroscópios. Há menção a DGPS com link rádio e com link satélite.

Nos sistemas acústicos, os arranjos LBL, SBL e SSBL/USBL aparecem como meios aplicáveis. No arranjo com triangulação acústica, o uso de transponders fornece posição ao processador com elevada precisão, estabilidade e repetitibilidade, embora com custo elevado. No SBL, há um beacon ou transponder em operação, com unidade stand-by no mud line e três ou quatro transdutores no casco; é um esquema simples e de baixo custo, porém suscetível a ruídos e a variações de roll e pitch. No SSBL/USBL, grupos de transdutores muito próximos entre si determinam a posição pelo tempo e pela fase do sinal de resposta de um ou mais transponders; a precisão aumenta com a quantidade de unidades acompanhadas e com a qualidade dos sensores. Sistemas combinados, com sensores no fundo e na embarcação, são usados para que um arranjo compense as desvantagens do outro.

Os trechos registram que a precisão típica de um sistema acústico é da ordem de menos que <NUMBER> da lâmina d’água, embora o sinal esteja sujeito a perdas por espalhamento, absorção, difusão, atenuação, reflexão e refração, efeitos que se intensificam com o aumento da lâmina d’água. Também se registra que, pela robustez e independência de equipamentos externos, o sistema acústico pode ser priorizado pelo controlador; em outro trecho, o sistema DP é descrito como inicialmente priorizando o DGPS. Em ambos os casos, a referência prioritária não é aceita de forma cega: ela é testada quanto à consistência.

**Monitoramento da posição**

O monitoramento operacional é centrado na comparação contínua entre a posição atual e a posição de referência, ou set point. A tela principal apresenta o afastamento entre a posição atual e o set point, o passeio da unidade em torno desse ponto e a qualidade das informações dos sistemas de referência usados para manter a posição. Isso atende diretamente ao acompanhamento de offset e da estabilidade da posição ao longo do tempo.

As telas secundárias complementam o diagnóstico com a planta de geradores e thrusters, energia disponível versus consumo, thrusters em uso e performance atual, bússolas, VRS/VRU, vento a partir de <NUMBER> fontes independentes e correnteza. Com isso, o heading é acompanhado por bússolas e sensores de direção, enquanto os movimentos do casco são observados por referência vertical e pelas próprias limitações dos sistemas sensíveis a roll e pitch. Para as condições meteoceanográficas, os trechos citam explicitamente vento e correnteza.

No sistema hidroacústico, há telas específicas para visualizar todos os transponders emissores e receptores em uso no fundo do mar e a qualidade do sinal e da posição associada. Há ainda duas telas de DGPS indicando respostas e qualidade dos sinais de posição. Os alarmes do sistema são registrados em tela e em impressora, além de alarmes gerados na OCC.

**Validação, redundância e ponderação**

A arquitetura descrita procura evitar que a falha de um único sistema de referência provoque perda imediata da capacidade de manter posição. Os sistemas de referência já possuem redundância, e o sistema DP executa testes de consistência em todos os sensores, inclusive no prioritário. Quando um sensor apresenta incoerência, seus dados são ignorados para avaliação da posição efetiva.

Além disso, o sistema calcula a variância de cada referência a partir da diferença entre o dado medido e o valor estimado por um modelo matemático. Essa variância é comparada com a menor variância entre os sensores e com limites de tolerância. O resultado é a atribuição de pesos inversamente proporcionais às variâncias, definindo o grau de importância de cada sistema de referência no cálculo da posição. Nos sistemas mais antigos, essa lógica automática é menos sofisticada, com referências distribuídas em entradas específicas do controlador e seleção operacional do DGPS e de referências relativas em paralelo.

**Limites, alarmes e perda de station keeping**

Os trechos não fornecem limites operacionais numéricos, mas a lógica de limite é clara: posição versus set point, passeio em torno do ponto de referência, qualidade dos sinais, consistência entre sensores, variância admissível, desempenho dos thrusters e relação entre energia disponível e consumo. O acompanhamento dessas variáveis, junto com o registro de alarmes, permite identificar tendência de degradação antes da perda completa da capacidade de station keeping.

Os principais indícios de perda de capacidade são aumento do offset e do passeio em torno do set point, piora da qualidade dos sinais DGPS ou acústicos, descarte frequente de sensores por incoerência, aumento relativo da variância das referências, queda de performance dos thrusters, redução da folga entre energia disponível e consumo e agravamento das ações ambientais monitoradas, especialmente vento e correnteza. Em sistemas sensíveis a movimentos do casco, variações de roll e pitch também degradam a qualidade da referência.

**Impactos associados**

A perda de posicionamento pode levar a ruptura e queda de risers de perfuração ou completação, danos em poços, manifolds e outros equipamentos submarinos, danos pessoais e ambientais e colisão com obstáculos de superfície ou subsuperfície nas proximidades da unidade.