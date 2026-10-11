AVISO: os trechos trazem informação direta limitada sobre a sequência operacional de offloading e sobre a gestão detalhada de lastro do FPSO; a consolidação abaixo reúne apenas os elementos técnicos explicitamente presentes e pertinentes ao tema.

**Estabilidade e condição de carregamento**

O FPSO é uma unidade flutuante estacionária que produz, armazena petróleo e escoa a produção para um navio aliviador. Sua ancoragem pode ser feita por linhas em catenária ou em taut-leg. Um aspecto operacional relevante é que o FPSO é muito sensível a carregamentos perpendiculares ao eixo proa-popa. Por isso, pode empregar sistema de posicionamento do tipo turret, com rolamentos que permitem ao navio se realinhar de acordo com as condições ambientais.

Para os cálculos de estabilidade em cada condição de carregamento, deve ser considerado o efeito de superfície livre dos tanques de líquidos consumíveis. Essa exigência vincula diretamente o controle de níveis dos tanques à avaliação contínua da estabilidade. Quando houver adoção de lastros sólidos, sua distribuição também afeta a estabilidade da embarcação e deve ser feita nos locais mais favoráveis para evitar problemas de trim.

No caso do navio aliviador, a condição considerada no estudo citado foi a de carregado, com calado máximo, tanques cheios e carregamento equilibrado, sem trim e sem banda. Essa condição define uma referência de estabilidade e equilíbrio longitudinal e transversal para análise de comportamento durante a operação.

**Controle de níveis dos tanques**

Os trechos não apresentam uma lógica operacional completa de enchimento e esvaziamento de tanques, mas deixam claro que o nível de enchimento altera a condição hidrodinâmica da unidade. Em modelos de offloading lado a lado, foram consideradas condições com tanques de armazenamento carregados a <NUMBER> da capacidade e, em outra condição, a <NUMBER> da capacidade total. A própria necessidade de modelar separadamente essas condições mostra que o estado de enchimento dos tanques não é neutro do ponto de vista dinâmico.

Também foi apresentada a comparação entre modelos hidrodinâmicos com e sem a representação dos tanques de carga. Nos resultados, a inclusão dos tanques altera funções de transferência de roll e massas adicionais associadas, especialmente em sway e roll, tanto para a unidade produtora quanto para o navio aliviador. Assim, o controle de nível dos tanques está associado não apenas ao atendimento da estabilidade estática, mas também à resposta dinâmica do conjunto durante o offloading.

**Sequência de transferência**

Não há, nos trechos, uma sequência explícita de transferência entre tanques do FPSO e do navio aliviador. O ponto tecnicamente suportado é que cada condição de carregamento deve ser tratada como uma condição distinta de estabilidade e de resposta hidrodinâmica. Em consequência, a sequência de transferência, quando analisada, não pode ser dissociada do acompanhamento do estado de enchimento dos tanques e dos efeitos de superfície livre na condição correspondente.

No caso do navio aliviador, a condição equilibrada sem trim e banda foi tomada como referência. Isso reforça que, ao longo da transferência, a manutenção do equilíbrio de carregamento é um parâmetro central para não degradar a condição inicial adotada.

**Interação entre movimentação de carga, movimentos e ancoragem**

A ligação mais clara entre movimentação de carga e esforços globais aparece nos resultados hidrodinâmicos de offloading lado a lado. Foram apresentados modelos completos da simulação, funções de transferência de roll para casos com e sem incorporação dos tanques de carga, massas adicionais de sway e de roll do navio aliviador, além de funções de transferência da elevação da superfície livre na região entre as unidades para diferentes incidências de onda e níveis de amortecimento. Também foram apresentadas funções de transferência de força de excitação da unidade produtora e do navio aliviador para incidência de zero grau e diferentes níveis de amortecimento nessa região.

Esses resultados associam o estado dos tanques e a representação hidrodinâmica da carga às respostas de movimento e às forças de excitação atuantes durante o offloading. Para um FPSO ancorado por catenária ou taut-leg, e sensível a carregamentos transversais, essa associação é relevante porque a alteração dos movimentos no plano horizontal e em roll interfere no quadro de ações que a unidade transmite ao seu sistema de ancoragem. O turret, quando existente, atua justamente para permitir o realinhamento da unidade frente às condições ambientais, reduzindo a exposição a carregamentos desfavoráveis perpendiculares ao eixo proa-popa.

**Posicionamento do navio aliviador**

No estudo citado, o navio aliviador dispõe de um propulsor principal na popa, dois propulsores do tipo túnel, um na proa e outro na popa, e dois propulsores do tipo azimutal, um na proa e outro na popa. Seu sistema DP é composto por controladores PID para cada grau de liberdade no plano horizontal. Ainda que os detalhes de ajuste tenham sido omitidos, a configuração indica que o controle de posição do aliviador integra a gestão da operação lado a lado, em paralelo às restrições de estabilidade e às variações de resposta hidrodinâmica causadas pelo estado de enchimento dos tanques.