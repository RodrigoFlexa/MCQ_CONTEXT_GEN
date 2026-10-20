# 2.3. Tratamento de água produzida para descarte

## Tratamento de água produzida para descarte

### Caracterização e separação gravitacional

#### Como aplicar e monitorar a separação gravitacional em FPSOs

Em FPSOs, a separação gravitacional pode utilizar vasos dedicados e, quando previstos para essa função, tanques de slop ou de segregação. O uso de um tanque depende de sua adequação ao fluido e à filosofia da unidade. Essa escolha é coerente com restrições típicas offshore de espaço, peso e capacidade por área instalada. O objetivo operacional é dar tempo para segregação das fases e retirar a fração separada de forma controlada, reduzindo o TOG antes de etapas complementares ou do descarte.

Na seleção e no acompanhamento, alguns sinais são mais úteis do que uma descrição genérica do equipamento: tendência do TOG, estabilidade da interface óleo-água, presença de sólidos e incrustação, sensibilidade do sistema a variações de vazão e ocorrência de perturbações a montante que aumentem a dispersão. A qualidade da água produzida para descarte é descrita como normalmente monitorada por análise diária de óleo e graxa, e sistemas on-line de óleo em água podem ser escolhidos buscando simplicidade, facilidade de condicionamento de amostra e baixa sensibilidade a variações causadas pela mistura de óleos processados.

#### O que é a água produzida e por que sua caracterização importa

Água produzida é a fração aquosa gerada junto com a produção de óleo e gás. Em instalações de produção, ela é tipicamente uma mistura de água de formação com água de injeção, podendo também receber contribuição de água conata. Após a separação primária, essa corrente ainda pode conter óleo, sais, compostos químicos, sólidos, metais, gás carbônico, sulfídrico e produtos associados a corrosão e incrustação. Sua composição varia entre campos e depende das características e da profundidade do campo produtor.

A caracterização é decisiva porque diferentes contaminantes respondem a mecanismos de remoção distintos. Salinidade, dureza e teor de óleos e graxas (TOG) são parâmetros relevantes, e o TOG é destacado como principal parâmetro de controle para descarte no mar nas regras brasileiras citadas. Óleo livre e parte do óleo disperso tendem a responder à separação gravitacional; já compostos dissolvidos normalmente exigem outras rotas de tratamento.

#### Interações relevantes, limitações e consequências operacionais

A separação gravitacional normalmente integra um trem de tratamento, e não uma solução única. Processos são aplicados de forma conjugada porque a água produzida contém constituintes com comportamentos distintos. Quando a gravidade reduz a carga de óleo livre e de parte do óleo disperso, pode melhorar o desempenho de etapas subsequentes. Essa contribuição, porém, cai quando a corrente chega muito emulsificada, com gotas pequenas ou com excesso de sólidos.

Em FPSOs, tempos de residência elevados em grandes tanques gravitacionais, quando coexistem altas concentrações de sulfato e condição anaeróbia, estão associados a maior risco de crescimento de bactérias redutoras de sulfato e geração de sulfeto de hidrogênio (H2S). Além disso, cátions e ânions presentes na água produzida estão associados ao potencial de incrustação. Para reinjeção, o tratamento adicional não se justifica apenas pelo TOG: ele também busca reduzir a possibilidade de dano ao reservatório e de perda de produção.

### Hidrociclones

#### Função do hidrociclone na bateria de tratamento

O hidrociclone é um separador estático usado para remover óleo disperso da água produzida por ação centrífuga. Em arranjos de processamento primário offshore, ele normalmente aparece a jusante de separação trifásica prévia e pode operar em conjunto com flotadores, formando uma bateria compacta de tratamento de água produzida. Essa combinação é frequente quando a instalação precisa conciliar alta capacidade com espaço e peso limitados. Em algumas configurações, a água após tratadores já pode sair suficientemente limpa; em outras, a passagem por bateria de hidrociclones é parte relevante do enquadramento do efluente. Quando a qualidade obtida ainda não é adequada, correntes oleosas separadas ou água fora da condição desejada podem ser encaminhadas para reprocessamento, em vez de descarte direto. Em módulos de processamento primário, vários hidrociclones costumam operar em paralelo para repartir a vazão de alimentação entre liners com cargas aproximadamente equivalentes.

#### Mecanismo de separação e papel da perda de carga

No interior do hidrociclone, a alimentação entra de forma a gerar escoamento circular em alta velocidade. Esse movimento cria forte campo centrífugo: a fase aquosa, mais densa, tende a ocupar a periferia, enquanto a fase oleosa, menos densa, se concentra mais perto do núcleo central. A separação depende da conversão da energia de pressão disponível no processo em energia cinética de rotação; por isso, a perda de carga no equipamento não é apenas uma penalidade hidráulica, mas parte funcional do mecanismo separador. Como o tempo de residência é muito curto, o campo centrífugo precisa ser suficientemente intenso para que as gotas de óleo migrem radialmente antes de sair do equipamento. Se essa conversão de energia for insuficiente, a separação se degrada. A descarga de água também sofre influência da pressão traseira: ela participa da definição do padrão interno de escoamento e ajuda a forçar a corrente rica em óleo a sair pelo overflow, enquanto a água tratada segue pelo underflow.

#### DPR, split e influência da geometria de overflow

DPR é a razão entre diferenciais de pressão usada no controle hidráulico do hidrociclone. O split caracteriza a divisão da vazão entre a corrente rejeitada, rica em óleo, e a corrente tratada; sua convenção precisa ser declarada, pois pode ser expresso como vazão de rejeito dividida pela alimentação ou por outra razão definida no sistema. Geometria do overflow, vazões e pressões nas saídas influenciam esses parâmetros de forma acoplada. A operação fora da faixa validada pode comprometer o campo centrífugo e aumentar óleo residual na água. O ajuste deve seguir a curva e os limites do equipamento, evitando atribuir um valor universal de DPR ou split a qualquer liner.

#### Fatores que alteram o desempenho e o turndown efetivo

O desempenho do hidrociclone não depende apenas de pressão. Geometria, capacidade de processamento, diferença de densidade entre fases, queda de pressão e tamanho das gotas de óleo afetam a eficiência de separação. Há resultados experimentais indicando que, em determinadas condições estudadas, maior fração volumétrica de água na alimentação esteve associada a maior eficiência de remoção da fase oleosa e a menor concentração de óleo no underflow; esse comportamento, porém, é contextual e não deve ser universalizado para qualquer fluido, geometria ou regime. Na prática, o turndown efetivo do hidrociclone tende a ser limitado porque mudanças de vazão alteram simultaneamente velocidade tangencial, tempo de residência, split e distribuição interna do escoamento. Por isso, operar muito abaixo ou muito acima da condição para a qual a geometria foi selecionada pode degradar a separação, mesmo sem mudança de hardware. Modelos fenomenológicos e correlações empíricas podem ajudar a prever tendências entre eficiência, vazão e split, mas sua aplicação direta exige cuidado quando houver coalescência, quebra de gotas, escoamento viscoso relevante ou altas concentrações de óleo.

#### Limitações mecânicas, erosão, incrustação e interações com o sistema

Entre as vantagens do hidrociclone estão compacidade, grande capacidade por área instalada, baixa manutenção e baixo consumo de energia. As limitações relevantes incluem susceptibilidade a incrustação e erosão por areia e, em alguns casos, necessidade de mais de uma passagem para atingir a qualidade desejada da água. A erosão tende a ser crítica quando a corrente contém sólidos abrasivos e altas velocidades locais, porque o próprio mecanismo que favorece a separação também impõe forte solicitação hidráulica às paredes e aos orifícios. A incrustação pode alterar a área efetiva das passagens, modificar o split e deslocar o ponto operacional. Em FPSOs, o uso de tanques slop como grandes separadores gravitacionais de apoio pode ajudar no enquadramento em alguns casos, mas tempos elevados de residência, sulfato e anaerobiose podem aumentar o risco de bactérias redutoras de sulfato e geração de H2S. Tecnologias alternativas, como adsorção e bio-oxidação, podem reduzir mais o teor de óleo em certas aplicações, porém sua adoção offshore pode ser limitada por peso, dimensões, dificuldades construtivas, economia e curto tempo de residência disponível na plataforma.

#### Seleção e aplicação em FPSO

A seleção do tratamento da água produzida em instalações offshore depende do espaço disponível, da aplicação, da disponibilidade de produtos químicos e das características do efluente. Nesse contexto, a associação de hidrociclones com flotadores é frequente porque combina equipamentos compactos e alta capacidade por área instalada, após separação trifásica prévia no processamento primário. Para o hidrociclone, variáveis de seleção e ajuste operacional descritas para sistemas compactos incluem o teor de óleo na alimentação, o DPR disponível, o split, o diâmetro do orifício de overflow e o número de liners em paralelo. Em desenvolvimentos de famílias ATO, MTO e BTO, o overflow aparece como variável geométrica relevante de projeto e de ajuste. Em aplicações com pouco espaço e produção com alto BS&W, isto é, alto teor de água e sedimentos no fluido produzido, sistemas ciclônicos compactos podem ser empregados para desengargalar a planta. Produtos como desemulsificantes, antiespumantes, inibidores de incrustação, inibidores de corrosão e polieletrólitos podem coexistir com esse processamento; seu efeito sobre a separação pode variar porque esses químicos podem alterar propriedades interfaciais, estabilidade da dispersão e tamanho de gotas, sem garantir melhoria em qualquer condição.

#### Monitoramento, controle e diagnóstico de perda de eficiência

Em arranjos acoplados separador-hidrociclone, uma estratégia de controle descrita atua na interface água-óleo do separador por meio da vazão de underflow do hidrociclone, enquanto o controle de Differential Pressure Ratio (DPR) atua no overflow com a intenção de manter o split constante. Em simulações, split quase constante apareceu como condição desejável para o bom funcionamento e esteve associado à estabilização da concentração de óleo na água descartada. Em sistemas sujeitos a golfadas, atuação muito rápida do controle de interface pode induzir grandes oscilações nos hidrociclones e prejudicar a eficiência; nessas situações simuladas, atuação mais lenta, como controle por bandas, reduziu instabilidades e melhorou o controle do teor de óleo e graxas de descarte. Uma camada de emulsão espessa altera o acoplamento entre separador e hidrociclone e exige revisar o ajuste das malhas e as condições de alimentação. Como diagnóstico operacional, aumento do óleo na corrente aquosa de saída é compatível com perda de desempenho separativo. Já o envio de água oleosa ou material removido para reprocessamento deve ser entendido como arranjo de recirculação de correntes fora da condição desejada, não como sintoma universal de falha do hidrociclone.

### Flotação e produtos químicos

#### Como a flotação separa óleo: colisão, adesão e ascensão

Na flotação, bolhas de gás são dispersas na água oleosa para colidir com gotículas de óleo. A separação útil depende de formar agregados bolha-gota suficientemente estáveis para que a força de empuxo do conjunto supere a tendência de permanência da gota no escoamento líquido, promovendo sua ascensão até a região de coleta.

A eficiência não depende apenas de haver bolhas. Ela depende de três etapas encadeadas: aproximação entre bolha e gota, adesão após a colisão e sobrevivência do agregado em meio ao escoamento. Se a colisão não ocorrer, se a interface estiver pouco favorável à adesão ou se a turbulência romper o agregado, a remoção cai. Por isso, a simples injeção de gás não garante desempenho.

Entre os fatores apontados como relevantes para a formação de agregados estáveis estão a razão entre tamanhos de bolha e gota, a concentração numérica dessas fases, a salinidade, a viscosidade do óleo, a velocidade do fluido e a turbulência. Entre esses grupos de fatores, os parâmetros de dispersão gasosa são destacados como especialmente importantes para a separação óleo-água.

#### Nanobolhas, microbolhas e limites de aplicação dos resultados experimentais

Na flotação, a redução do tamanho das bolhas aumenta a área interfacial disponível, mas também altera a velocidade de ascensão e a interação com gotas e flocos. O desempenho depende da distribuição de tamanhos, da estabilidade da dispersão, da carga de óleo e da hidrodinâmica. O emprego de microbolhas ou nanobolhas deve ser avaliado no equipamento e no fluido de interesse; uma melhora em água preparada de laboratório não garante o mesmo ganho em água produzida real. Em instalações com hidrocarbonetos, o gás de flotação e seu circuito devem ser compatíveis com a segurança do processo; um ensaio com ar não define a escolha do gás da unidade.

#### Seleção e aplicação em FPSO: interação entre estágios e restrições de plataforma

A seleção da tecnologia de tratamento depende de espaço disponível, aplicação, disponibilidade de produtos químicos e características do efluente. Em plataformas, limitações de espaço, peso, tempo de residência e dificuldade de intervenções favorecem soluções compactas. Nesse contexto, a combinação hidrociclone-flotador é recorrente porque usa a capacidade do primeiro para remoção inicial de óleo disperso e a do segundo para reduzir o teor remanescente.

A interação entre estágios é decisiva. Se o hidrociclone entrega à flotação uma corrente com gotas muito finas, emulsão estável ou grande oscilação de vazão, a etapa seguinte tende a exigir melhor controle da dispersão gasosa e do condicionamento químico. Se a separação a montante já reduz adequadamente o óleo livre, a flotação pode operar mais como polimento. Em alguns casos, apenas a bateria de hidrociclones pode ser suficiente para enquadramento, o que mostra que a necessidade da flotação depende do conjunto de desempenho do sistema, e não de uma regra fixa.

Em FPSO, a flotação integra uma malha de tratamento e não deve ser analisada isoladamente.

#### Água produzida, variabilidade do efluente e função da flotação

Água produzida é a fração aquosa gerada simultaneamente à produção de óleo e gás. Essa corrente pode incluir água conata e água de formação, o que ajuda a entender por que sua composição não é fixa ao longo da vida do campo. Além da origem geológica, a própria evolução da produção altera o contexto de tratamento, porque o volume de água produzida tende a crescer com o tempo em associação ao aumento da proporção água/óleo.

Em unidades offshore, a flotação aparece como uma das etapas usadas para reduzir o teor remanescente de óleo na água, frequentemente em arranjos que também incluem hidrociclones e, conforme a instalação, vaso degaseificador ou volumes adicionais de separação gravitacional. Esse encadeamento é funcional: a etapa anterior reduz parte da carga oleosa dispersa, e a flotação trata a parcela que permanece difícil de separar apenas por gravidade ou por ação centrífuga.

A necessidade e o papel exato da flotação dependem do desempenho global do sistema. Em alguns casos, a bateria de hidrociclones pode ser suficiente para enquadrar o efluente; em outros, a etapa subsequente de flotação torna-se necessária para complementar a remoção.

#### Como propriedades do fluido e hidrodinâmica alteram a adesão bolha-gota

A eficiência da flotação muda quando mudam as propriedades do óleo, da água e do escoamento. Entre os fatores relevantes para formar agregados bolha-gota estáveis estão a razão entre tamanhos de bolha e gota, a concentração numérica dessas fases, a salinidade, a viscosidade do óleo, a velocidade do fluido e a turbulência. Nesse conjunto, os parâmetros de dispersão gasosa recebem destaque porque controlam quantas bolhas estão disponíveis, como elas se distribuem no líquido e com que frequência encontram as gotículas de óleo.

O efeito dessas variáveis não é isolado. Maior turbulência, por exemplo, pode aumentar encontros entre bolhas e gotas, mas também pode elevar os esforços hidrodinâmicos que rompem agregados já formados. De modo semelhante, alterações no tamanho e na quantidade de bolhas mudam a área interfacial gás-líquido disponível e a probabilidade de colisão eficaz.

Em plataformas, o comportamento observado em uma unidade depende ainda das variáveis próprias da instalação, como temperatura, pressão, tipo e viscosidade do óleo, estabilidade da emulsão, tamanho de gota, salinidade e velocidade de fluxo. Por isso, uma condição favorável em um sistema específico não define desempenho universal para qualquer FPSO.

#### Condicionamento químico: quebra de emulsão, floculação e efeito do pH

No tratamento de água oleosa, é comum usar produtos químicos, como polieletrólitos, para atuar na quebra de emulsões. Quando a água contém óleo disperso fino ou emulsões estáveis, o condicionamento químico pode tornar a flotação mais favorável ao reduzir barreiras à aproximação entre gotículas e partículas e ao promover agregação em estruturas mais facilmente removíveis.

Em sistemas com coagulação ou floculação, a função do reagente é modificar o estado interfacial e a estabilidade do sistema disperso. Dependendo do fluido e da química aplicada, isso pode favorecer a formação de flocos ou agregados com maior chance de captura pelas bolhas. Em coluna de flotação avaliada experimentalmente, a operação com coagulantes esteve associada a maior eficiência do que a operação sem coagulantes, mas esse resultado permanece condicionado ao sistema estudado.

O ajuste de pH pode integrar esse condicionamento porque afeta a ionização de espécies, a ação de coagulantes e a estabilidade de emulsões. A seleção do reagente e da estratégia de dosagem depende das características do efluente e da compatibilidade com as etapas posteriores de separação, manejo de correntes oleosas e descarte.

### Controle, desvios e correntes oleosas

#### Função do controle no tratamento e no destino da água produzida

A água produzida é o principal efluente gerado pela separação de óleo, gás e água em instalações de produção e pode conter óleo, sais, compostos químicos, sólidos e metais. No processamento primário, o tratamento dessa corrente não é um fim isolado: ele condiciona a água para um destino operacionalmente e ambientalmente aceitável, como descarte no mar, reinjeção ou reprocessamento, conforme o arranjo da unidade. Quando a qualidade da água tratada se deteriora, o problema não se limita ao efluente; ele também pode indicar sobrecarga, perda de eficiência de separação ou desbalanceamento entre estágios da planta. Em campos em desenvolvimento, o aumento do volume de água produzida tende a ampliar essa pressão sobre os equipamentos de condicionamento, o que pode reduzir a qualidade da corrente final se a capacidade efetiva do sistema ou sua faixa operacional forem excedidas.

#### Correntes oleosas residuais, slop e retorno ao processo

O tratamento da água produzida gera correntes secundárias mais oleosas que não devem ser confundidas com a água tratada. Em sistemas descritos para FPSOs, o óleo recuperado no tratamento pode ser encaminhado para tanques de slop e, a partir daí, retornar à linha de produção. No FPSO Frade, a água oleosa proveniente dos hidrociclones e o material coletado na célula de flotação eram encaminhados por sistema de drenagem isolado para reprocessamento no separador de produção. A função do slop e das drenagens segregadas é reter e concentrar frações oleosas recuperáveis ou misturas instáveis, evitando que elas retornem inadvertidamente ao sistema de água tratada. Isso reduz recirculação desordenada de óleo e permite reintegração controlada ao processo. A segregação física dessas correntes é relevante porque sua composição, teor de gás, tendência à emulsão e carga de sólidos podem ser diferentes da corrente principal; misturá-las sem controle pode elevar a carga do tratamento, perturbar separadores e mascarar o diagnóstico da origem da contaminação.

#### Desvio de água fora de especificação para tanque off-spec e reprocessamento

Em um arranjo com segregação de água fora de especificação, a corrente de hidrociclones e flotação pode ser desviada para tanque off-spec e posteriormente reprocessada, conforme as rotas previstas no projeto. Nessa configuração, o desvio interrompe o envio da corrente inadequada ao destino principal daquele período e cria uma rota de contenção para nova separação. O reprocessamento pode recuperar parte da qualidade quando a causa da não conformidade é removível por nova passagem no separador, mas sua utilidade prática depende de haver capacidade de inventário no tanque, estabilidade operacional durante a recirculação e compatibilidade hidráulica do retorno com o separador. Se a causa raiz persistir, o desvio contém a corrente inadequada, porém não restabelece sozinho o desempenho do sistema.

#### Segregação de correntes oleosas residuais e retorno controlado ao processo

Correntes removidas no tratamento da água produzida não devem ser tratadas como equivalentes à água já condicionada. No FPSO Frade, a água oleosa proveniente dos hidrociclones e o material coletado na célula de flotação eram direcionados por sistema de drenagem isolado para reprocessamento no separador de produção. No FPSO Cidade do Rio de Janeiro, o óleo recuperado no tratamento por hidrociclones e flotadores era encaminhado para tanques de slop e, daí, reinjetado na linha de produção. Em ambos os casos, a função técnica da segregação é evitar que frações mais oleosas, instáveis ou contaminadas retornem sem controle ao circuito de água tratada. Tanques de slop e drenagens segregadas atuam como pontos de retenção e concentração de correntes recuperadas, permitindo reintegração mais controlada ao processo principal. Essa segregação é relevante porque essas correntes podem diferir da água tratada em teor de óleo, gás, sólidos, tendência à emulsão e variabilidade operacional.

#### Importância da correspondência entre fluido real, função do tanque e documentação

Classificar documentalmente um tanque como armazenamento de óleo quando ele recebe água off-spec pode levar ao uso de premissas de projeto incompatíveis com o fluido real. Essa relação é tecnicamente importante porque a função real do tanque define quais fenômenos precisam ser considerados na operação e na integridade do sistema. Água produzida fora de especificação e óleo de carga podem impor demandas distintas de materiais, drenagem, ventilação, instrumentação, gestão de interfaces e tratamento de borras. Quando a documentação não representa o fluido real e a função operacional do equipamento, aumentam os riscos de inventário mal interpretado, seleção inadequada de salvaguardas e respostas incoerentes durante desvios. Em sistemas com múltiplas rotas de slop, off-spec e reprocessamento, a rastreabilidade correta de tanques e linhas faz parte do controle de processo.

#### Monitoramento on-line como suporte a decisões operacionais

Monitores on-line de óleo em água apoiam o acompanhamento contínuo do tratamento e precisam operar com procedimentos de amostragem, limpeza e verificação compatíveis com o serviço. As tecnologias citadas incluíram fluorescência ultravioleta, absorção ou dispersão no infravermelho e espalhamento a laser, selecionadas por adequação ao uso offshore, simplicidade, facilidade de condicionamento de amostra e baixa sensibilidade a variações decorrentes da mistura de óleos processados. Nesse contexto, o valor operacional do monitor não se limita à leitura instantânea: ele pode sustentar alarmes de tendência, confirmação de excursões e investigação de perda de desempenho, quando integrado à filosofia de controle da unidade. Isso não significa que um único instrumento seja universalmente suficiente para decidir descarte, reinjeção ou desvio. Deriva de calibração, mudança na composição do óleo, contaminação da célula de medição e amostragem pouco representativa podem comprometer a interpretação operacional.

### TOG, amostragem e desempenho

#### O que é controlado no descarte de água produzida

Água produzida é a corrente aquosa separada do petróleo e do gás durante o processamento primário. Mesmo após a separação do óleo, essa água ainda pode conter gás carbônico, sulfídrico, óleo remanescente, sólidos em suspensão, produtos de corrosão, incrustações, sais, metais e compostos orgânicos dissolvidos ou dispersos. Por isso, antes da destinação, ela normalmente requer tratamento e monitoramento.

No descarte contínuo em plataformas marítimas, o teor de óleos e graxas (TOG) aparece como parâmetro central de controle ambiental nas regras brasileiras citadas, acompanhado por controle por média e por valor máximo em base temporal definida pela norma. Outros atributos também podem ser relevantes para a caracterização e para a proteção ambiental, como temperatura, salinidade, metais, bactérias e constituintes orgânicos específicos. Assim, o TOG é central para o enquadramento do descarte, mas não resume sozinho toda a qualidade ambiental da água produzida.

#### Como o tratamento altera o TOG descarregado

Nos sistemas offshore citados, o tratamento da água oleosa busca remover óleo livre ou disperso e sólidos em suspensão antes do descarte. Um arranjo consagrado é a combinação em série de hidrociclones e flotadores. A suficiência de uma etapa isolada depende da separabilidade do óleo, da carga recebida e da qualidade exigida; precisa ser demonstrada na faixa operacional da unidade.

A redução do TOG depende de como o óleo está distribuído na água. Quando o óleo está em gotas mais facilmente separáveis, processos físicos tendem a ser mais eficazes. Quando está finamente disperso, emulsificado ou associado a sólidos, a remoção física tende a se tornar mais difícil. A aplicação de produtos químicos para quebra de emulsões pode modificar essa separabilidade.

Em FPSOs, correntes fora de especificação podem ser segregadas em tanque dedicado, em vez de seguirem diretamente para descarte. Esse manejo não é um requisito universal, mas é uma consequência operacional compatível com a necessidade de evitar lançamento de água com alto TOG enquanto a condição é corrigida.

#### Condições do fluido e da operação que mudam o resultado do tratamento e da medição

A quantidade de óleo presente na água produzida varia com pH, salinidade, temperatura, razão óleo-água e tipo e quantidade de produtos químicos adicionados durante a produção. Além disso, a composição da água produzida depende das características e da profundidade do campo produtor e pode variar entre ativos com perfis distintos de produção, inclusive entre plataformas produtoras de óleo e plataformas predominantemente de gás.

Essas variações mudam o comportamento do sistema porque afetam a forma de distribuição do óleo na água e a composição inorgânica associada ao efluente. Salinidade e teor de óleo são apontados como fatores determinantes na escolha de processos de tratamento e do local de descarte do efluente tratado.

Do ponto de vista de controle, isso significa que desempenho de tratamento, resposta de instrumentos e comparação entre campanhas podem mudar quando a matriz da água muda. Por isso, resultados e ajustes obtidos em um ativo ou período não devem ser transferidos automaticamente para outro sem validação local.

#### Instrumentos on-line de TOG: utilidade, limites e relação com o laboratório

O monitoramento em linha do TOG é valorizado por fornecer resposta em tempo real, aumentar a capacidade de controle do processamento, reduzir custo de análises rotineiras, gerar banco de dados e apoiar ajuste ou projeto de plantas. Entre as tecnologias citadas para determinação de TOG em contexto offshore estão fluorescência, espectrofotometria de infravermelho em linha e outras medições ópticas.

Em avaliação experimental resumida, diferentes monitores apresentaram correlação satisfatória com análise laboratorial. Esse resultado é relevante para uso operacional, mas não demonstra equivalência universal para qualquer instalação, qualquer tipo de água produzida ou qualquer exigência regulatória.

Na aplicação prática, o instrumento on-line tende a ser mais forte como ferramenta de tendência, alarme e ajuste operacional. Sua resposta pode depender da calibração, da composição do óleo, da presença de sólidos e bolhas e da correspondência entre o ponto medido e a corrente efetivamente descartada. Por isso, monitor on-line e laboratório exercem papéis complementares: um favorece resposta rápida; o outro sustenta referência analítica conforme o método utilizado.

#### Controle do descarte e consequências operacionais da não conformidade

Para descarte contínuo em plataformas marítimas, as regras brasileiras citadas tratam o controle do TOG por média temporal e por valor máximo diário, com comunicação imediata ao órgão ambiental quando houver descarte acima do máximo diário e relatório de não conformidade quando a média mensal ficar acima do limite aplicável. Também é mencionado envio semestral de laudo de caracterização com diversos parâmetros, incluindo compostos inorgânicos, radioisótopos, compostos orgânicos, toxicidade crônica e parâmetros complementares.

Isso mostra que a conformidade do descarte depende de uma cadeia integrada: tratamento, medição, registro, decisão operacional e gestão de correntes fora de especificação. A análise diária de óleo e graxas aparece como prática de acompanhamento da qualidade da água produzida.

Erros de caracterização do fluido também podem produzir consequência operacional relevante. Em um caso de FPSO, um tanque que recebia água produzida fora de especificação foi classificado como tanque de óleo, e essa incompatibilidade levou ao uso de referência de projeto diferente do fluido realmente armazenado. O mecanismo importante é que classificar incorretamente corrente ou inventário pode comprometer projeto, operação e resposta a desvios.
