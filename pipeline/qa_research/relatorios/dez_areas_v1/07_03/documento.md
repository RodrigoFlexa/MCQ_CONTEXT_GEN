# 7.3. Manutenção e Plano de Manutenção

## Manutenção e Plano de Manutenção

### Criticidade e estratégia de manutenção

#### Criticidade e finalidade da estratégia de manutenção

A estratégia de manutenção é o conjunto de decisões que define como cada sistema ou equipamento será tratado para reduzir falhas com consequências relevantes e sustentar a disponibilidade da unidade. Em instalações de óleo e gás, especialmente offshore, essas consequências não se limitam ao reparo do item: podem incluir perda de produção, acidente grave, dano ambiental, indisponibilidade de funções de processo e aumento de custo operacional. Por isso, a otimização da manutenção é tratada como problema de múltiplos objetivos, envolvendo simultaneamente segurança, saúde, meio ambiente, custo de manutenção e perdas de produção. Em unidades marítimas afastadas da costa, a estratégia também precisa considerar restrições logísticas e de suporte técnico, porque a dificuldade de acesso, a limitação de pessoal embarcado e a dependência de recursos em terra alteram o modo como se distribuem tarefas corretivas, preventivas e baseadas em condição.

#### Por que a criticidade muda a escolha entre corretiva, preventiva e baseada em condição

A criticidade funciona como filtro de decisão porque combina a importância funcional do item com as consequências de sua falha. Quando um equipamento é de baixa criticidade, a perda temporária de sua função pode ser tolerável ou recuperável sem impacto desproporcional; nesse contexto, pode ser tecnicamente aceitável adotar manutenção corretiva planejada, desde que exista capacidade de recompor a função após a falha. Em contraste, equipamentos de maior criticidade exigem análise de modos de falha e dados de confiabilidade para definir técnica de manutenção e periodicidade de ações preventivas. A manutenção preventiva é coerente quando há histórico ou comportamento de falha que permite programar intervenção antes da falha em serviço. A manutenção baseada em condição ou preditiva tende a ser preferível quando o modo de falha apresenta sinais detectáveis de degradação antes da perda funcional, permitindo intervir no momento em que o risco aumenta, sem antecipação excessiva.

#### Condições que alteram o comportamento da decisão

A mesma técnica não se comporta da mesma forma em todos os ativos. A escolha da estratégia varia com a severidade das consequências, a probabilidade de ocorrência, a detectabilidade do modo de falha, a disponibilidade de dados históricos, a arquitetura funcional do sistema e as restrições operacionais da unidade. Em plataformas marítimas, a quantidade reduzida de mantenedores a bordo favorece a transferência de parte do monitoramento e do suporte técnico para ambiente onshore, quando a filosofia operacional admite esse arranjo. A estruturação hierárquica de equipamentos e instalações também altera a decisão prática, porque permite agrupar intervenções por função e evitar retirada individual de itens manuteníveis de um mesmo conjunto, o que poderia aumentar indisponibilidade sem ganho proporcional de risco. Em sistemas modelados por Diagrama de Blocos de Confiabilidade (RBD, do inglês Reliability Block Diagram), a aplicação direta é mais adequada a sistemas sem reparação e sem dependência relevante da ordem das falhas; quando essas premissas não valem, outras técnicas ou associações de técnicas podem ser necessárias.

#### Como FMEA, FMECA e MCC/RCM se relacionam na escolha da política

A Análise dos Modos de Falha e seus Efeitos (FMEA) identifica como os subitens podem falhar e quais efeitos cada modo de falha produz no sistema. A Análise dos Modos de Falha, seus Efeitos e Criticidade (FMECA) amplia essa análise ao acrescentar avaliação de probabilidade de ocorrência e criticidade, o que ajuda a priorizar falhas mais relevantes. A Manutenção Centrada em Confiabilidade (MCC ou RCM, do inglês Reliability-Centered Maintenance) usa esse entendimento para planejar a manutenção e selecionar políticas para itens críticos. Em termos técnicos, o encadeamento útil é: identificar modos de falha e efeitos, distinguir quais falhas merecem prioridade pela criticidade e então escolher a política de manutenção segundo a natureza do modo de falha e a consequência para o sistema. Essa lógica é importante porque a decisão não depende apenas do nome do equipamento, mas do que sua falha causa, de como ela se desenvolve e de quão relevante ela é para produção, segurança ou meio ambiente.

#### Como selecionar e aplicar a estratégia em novas unidades offshore

Em novas unidades offshore, a definição da estratégia de manutenção pode ser implantada antes do início da operação, ainda em fases de projeto avançado, construção, montagem, comissionamento, condicionamento, start-up e pré-operação, quando os principais fornecedores já estão definidos e o detalhamento do ativo é suficiente para análise. Nessa abordagem, a engenharia e o planejamento de manutenção passam a ser incorporados ao projeto da unidade. Uma sequência técnica possível é: estruturar hierarquicamente os ativos, classificar a criticidade dos equipamentos, identificar modos de falha e partes afetadas, incorporar dados de falha e confiabilidade quando disponíveis e então selecionar a técnica de manutenção mais adequada para bloquear determinado modo de falha ou priorizar intervenções baseadas em condição. Em metodologias específicas, o ranqueamento quantitativo de fatores de criticidade pode usar ferramentas como o critério de Mudge e apoio de normas NORSOK, mas isso permanece como recurso metodológico dessas aplicações, não como regra universal nem requisito brasileiro implícito.

### Planos, tarefas e CMMS

#### O que é um plano de manutenção e quais elementos o compõem

O plano de manutenção organiza as intervenções previstas para preservar a função dos ativos e registrar como a organização reage a desvios e falhas. Sua estrutura pode combinar ações programadas, executadas em períodos estipulados, com ações não programadas originadas por consequências das ações executadas, relatos de anomalias e análise de dados operacionais e de manutenção. Em ativos de FPSO, isso significa que o plano não é apenas um calendário: ele também é um mecanismo de conversão de informações de campo em novas tarefas, revisões de escopo, mudanças de periodicidade e inclusão de controles adicionais quando o comportamento real do equipamento diverge do esperado. A utilidade técnica do plano depende de ele representar o contexto funcional do equipamento, isto é, a função requerida, o modo de operação, a criticidade e as consequências da perda de desempenho. Por isso, o plano tende a incorporar tarefas preventivas, inspeções, calibrações, testes e verificações documentais, além de gatilhos para revisão quando surgem falhas recorrentes, desvios de processo, recomendações de análises de risco ou achados de auditoria.

#### Como o CMMS e o ERP estruturam cadastro, tarefas, ordens e histórico

O Sistema Computadorizado de Gestão da Manutenção, ou CMMS, apoia no mínimo a gestão de ordens de serviço, planejamento, programação, histórico de equipamentos, custos, recursos de trabalho, estoque e relatórios com indicadores. Sua eficácia depende de dados completos e precisos de equipamentos, peças, materiais, planos e procedimentos. No fluxo organizacional descrito, a base começa pelo cadastro do equipamento com campos obrigatórios, identificação por TAG, validação de inconsistências e posterior cadastro da lista de tarefas e do plano preventivo no ERP, como SAP. A lista de tarefas orienta a execução das ordens sistemáticas ao descrever a sequência de atividades do centro técnico responsável. Tecnicamente, o CMMS funciona como elo entre definição do plano e execução rastreável: transforma cadastro em ordens, ordens em registros e registros em histórico para revisão do plano. Se o cadastro estiver incompleto, o sistema ainda gera ordens, mas com baixa qualidade técnica, o que compromete programação, materiais, evidência de execução e capacidade de aprender com falhas e desvios.

#### Planejamento, plano mestre e programação de curto prazo

Após o cadastro dos planos, o planejamento pode ser feito para um período predeterminado a partir dos planos registrados no ERP para equipamentos mantidos por filosofia preventiva. A extração desses dados para um Plano Mestre de Manutenção Preventiva permite classificar e filtrar informações como responsável, equipamento, número do plano, semana e data planejadas, solicitação, status, periodicidade e local de instalação. Já a programação é apresentada como atividade de curto prazo, semanal, voltada para a semana seguinte, cujo principal produto é um plano de trabalho para a equipe executante. As origens dessa programação incluem demandas não sistemáticas dos usuários e relatórios do ERP referentes aos planos sistemáticos. Em FPSO, o plano mestre fornece horizonte e visibilidade; a programação converte esse horizonte em intervenção executável sob restrições reais de operação, acesso, janela climática, materiais, recursos e liberação operacional. Quando o plano mestre não se integra ao planejamento de produção, tende a prevalecer a urgência do curto prazo, reduzindo a capacidade de antecipar materiais, coordenar paradas e proteger a integridade dos ativos.

#### Condições que mudam o comportamento do plano: criticidade, contexto funcional e adequação da estratégia

O comportamento do plano muda quando muda o contexto funcional do ativo e a criticidade do equipamento ou sistema. A Manutenção Centrada na Confiabilidade, RCM, é descrita como processo para determinar requisitos de manutenção dos ativos físicos no contexto funcional atual, buscando alinhar otimização e eficácia. Nessa lógica, a mesma peça pode exigir tratamento diferente conforme a função requerida, a consequência da falha e o regime operacional. A definição da estratégia de manutenção também pode considerar o tipo de manutenção a que o equipamento será submetido e a otimização do uso de recursos humanos e custos. Em sistemas relevantes para segurança operacional, desvios como ausência de programa preventivo implementado em item de proteção, descumprimento de plano de manutenção, teste e inspeção de equipamento crítico, ou falta de implementação de salvaguardas alteram o risco operacional do sistema. Em instrumentação de monitoramento de processo, a utilidade do plano também depende da adequação da tecnologia de medição e da faixa de calibração ao objetivo de detectar distúrbios do processo. Se a medição não revela o desvio com sensibilidade suficiente, a tarefa pode existir formalmente sem entregar o efeito de controle esperado.

#### Interações com materiais, documentação e disponibilidade operacional

A execução do plano depende de interação prática entre programação, materiais, ordens e documentação de apoio. O sistema de gestão e o armazém de manutenção sustentam essa interação ao reunir dados de peças, materiais, planos e procedimentos, além de apoiar compras, estoque e histórico. Na gestão de materiais de manutenção, podem ser usados padronização quando possível, posicionamento mais próximo do ponto de uso e planejamento de compras e estoque para estabilizar o processo. Isso influencia o tempo total de restabelecimento em manutenção corretiva, porque a duração não envolve apenas o reparo físico: inclui identificação da falha, definição do que deve ser feito, especificação do que é necessário, suprimento do material, logística e mobilização da equipe. Quando a estratégia e os materiais requeridos são especificados de forma proativa, o tempo de planejamento do trabalho pode ser reduzido; quando o material especificado está disponível em estoque, o tempo da cadeia de suprimento também pode ser reduzido. Em instalações offshore, a falta de sobressalentes para sistemas e equipamentos críticos foi associada, em auditorias e investigações, a problemas de disponibilidade de funções críticas e à fragilização da segurança operacional.

### Programação, backlog e diferimentos

#### O que são programação, backlog e diferimento

Programação de manutenção é a transformação das necessidades de inspeção, teste, calibração, reparo e intervenção em uma sequência executável no tempo, compatível com operação, logística, recursos e indisponibilidades permitidas. Backlog é o conjunto de atividades não concluídas após a data prevista segundo a definição adotada pela organização. Diferimento é a decisão formal de adiar uma atividade programada, com rastreio da nova data e tratamento do risco criado pelo adiamento.

Esses três elementos se conectam. A programação tenta transformar demanda técnica em trabalho realizável; o backlog mostra o descompasso entre demanda e capacidade de execução; e o diferimento é um mecanismo de controle para casos em que a atividade não será realizada no prazo planejado.

Quando a definição de backlog é complexa ou entendida de forma diferente entre equipes onshore e offshore, a gestão perde clareza. Isso dificulta priorização, previsão de recursos e decisão sobre o que está vencido, diferido ou ainda dentro de janela aceita pelo sistema de gestão.

#### Planejamento de recursos e visibilidade do backlog de integridade

A presença continuada de engenheiros de inspeção ou função equivalente pode contribuir para gestão mais eficaz de corrosão e integridade quando mantém conhecimento do ativo, atualiza diagramas e garante que os dados produzidos sejam convertidos em ações executadas. O efeito depende de continuidade, organização e capacidade real de resposta.

A redução de backlog exige selecionar o trabalho que deve entrar na frente e o tipo de recurso necessário para executá-lo. Em geral, a priorização considera criticidade do equipamento ou função, efeito sobre barreiras de segurança, impacto ambiental, perda de produção, dependência de parada, disponibilidade de redundância, complexidade logística e interação com outros serviços.

No contexto de integridade de FPSOs e FSUs, é importante que backlog de inspeção estrutural e marítima tenha visibilidade própria dentro do backlog geral. Quando fica diluído entre outras ordens, cresce o risco de adiamentos repetidos de inspeção de casco submerso, tanques, amarrações, válvulas de costado e sistemas marítimos com efeito potencial sobre estanqueidade, estabilidade e contenção.

#### Diferimento, medidas compensatórias e controle de risco

Diferir manutenção significa aceitar que a atividade não será realizada no prazo original e que pode existir degradação progressiva do elemento afetado. Por isso, o diferimento eficaz precisa ser formal, rastreável e tecnicamente justificado. Em tarefas críticas, o processo pode incluir aprovação por responsável designado, registro da mudança de data, identificação da mitigação e definição de nova data de conclusão. Também é relevante acompanhar a onda de trabalho criada pelos diferimentos, porque o adiamento de hoje pode concentrar muitas tarefas no mesmo período futuro.

A razão física para exigir compensação é que o elemento degradado pode ter função de barreira para eventos maiores. Se a barreira está enfraquecida, a operação contínua depende de medidas provisórias que reduzam a probabilidade de falha, limitem consequências ou acrescentem barreiras alternativas. Essas medidas podem envolver restrições operacionais, monitoramento reforçado, testes adicionais, vigilância aumentada ou outras ações compatíveis com o risco e com a função do sistema.

Avaliações isoladas por ordem de serviço podem ser insuficientes se a soma das degradações ultrapassar a tolerância de risco da instalação.

#### Como a programação funciona em múltiplos horizontes

A programação de manutenção pode ser estruturada em horizontes sucessivos de detalhamento. Em um horizonte mais longo, identificam-se grandes escopos e indisponibilidades relevantes. Em um horizonte intermediário, consolidam-se manutenção, inspeção e projetos. Em horizonte curto, o plano é ajustado às condições locais de execução, como efetivo disponível, atrasos e outras restrições operacionais.

Esse encadeamento ajuda a transformar demanda técnica em trabalho executável, porque o plano vai sendo refinado conforme surgem informações mais concretas sobre recursos, interferências e sequência de atividades.

Um sistema de gestão de manutenção pode apoiar esse processo ao detalhar, programar, executar e registrar atividades. No arranjo descrito, tarefas críticas para segurança são vinculadas a padrões de desempenho e recebem prioridade específica, e as datas programadas servem de base para planejamento, programação e gestão do backlog.

A interação entre planejamento onshore e offshore é relevante porque o plano detalhado precisa reagir a problemas locais sem perder alinhamento com escopos maiores e com as necessidades da instalação.

#### Por que definições simples e dados confiáveis melhoram a gestão do backlog

Na gestão de backlog de manutenção, uma definição simples e compartilhada entre equipes facilita classificar o que está vencido, em backlog ou diferido. Isso tende a tornar mais simples o agendamento, o planejamento global, o ranqueamento por criticidade e o entendimento gerencial das necessidades de recursos.

Quando a definição é complexa ou entendida de forma diferente entre onshore e offshore, a gestão do backlog e as decisões de diferimento se tornam mais difíceis.

A utilidade dos indicadores depende da qualidade dos dados. Quando os registros são confiáveis e livres de dados espúrios, os indicadores-chave de desempenho, ou KPIs, podem dar foco à redução do backlog. Nesse contexto, metas móveis de backlog e pontos de gatilho podem ser usados para acionar respostas gerenciais, como reforço de recursos, campanhas de manutenção ou revisão de cargas de projeto que estejam competindo com a manutenção planejada.

Esses mecanismos são mais aplicáveis quando a instalação já possui dados de boa qualidade e backlog baixo ou em redução, ou quando a organização está tentando conduzir essa redução de forma controlada.

#### Condições que fazem o backlog crescer e ficar difícil de reduzir

O backlog pode crescer quando a manutenção não é concluída conforme planejado por causa de pontos de estrangulamento específicos. Entre eles estão indisponibilidade de especialidades, falta de sobressalentes e necessidade de parada que não é liberada. Em ambientes offshore, conflitos com projetos, disputa por recursos e restrições de acomodação também podem dificultar a execução da manutenção planejada.

Em instalações em envelhecimento, a dificuldade aumenta porque a degradação tende a crescer e os programas de inspeção podem ficar para trás. Ao mesmo tempo, o volume de dados de inspeção pode se tornar elevado. Se esses dados não forem geridos e analisados com continuidade, a capacidade de resposta pode ser sobrecarregada e a redução do backlog de inspeção se torna mais difícil.

Em FPSOs e Unidades Flutuantes de Armazenamento, ou FSUs, ameaças de envelhecimento e fim de vida exigem que o sistema de integridade ajuste escopo, metodologia e frequência de inspeção à idade e à condição do vaso. Em vida tardia, cumprir o programa planejado pode demandar recursos adicionais.

Assim, backlog persistente pode refletir combinação entre aumento de degradação, aumento de demanda de inspeção e capacidade insuficiente de análise, planejamento ou execução.

#### Campanhas, paradas e competição por recursos

Campanhas de manutenção podem ser úteis quando várias pendências compartilham acesso, recurso especializado ou a mesma indisponibilidade operacional. Nessa condição, o agrupamento de atividades pode reduzir remobilizações e melhorar o aproveitamento da janela de execução.

Paradas programadas se tornam relevantes quando a atividade depende de indisponibilidade coordenada de equipamento ou sistema. Nessas situações, a execução não depende apenas de prioridade administrativa, mas também de uma janela operacional compatível com a intervenção.

A carga de projetos também pode competir com a manutenção planejada. Em contexto offshore, projetos podem consumir leitos, recursos especializados e capacidade das equipes de manutenção, além de gerar carga adicional associada a reparos e recondicionamento. Quando isso ocorre, a manutenção planejada tende a perder espaço para demandas concorrentes, o que favorece a formação de novo backlog.

Por isso, a seleção de campanhas e paradas precisa considerar não só a criticidade técnica das pendências, mas também o compartilhamento de recursos e os conflitos previsíveis com outras frentes de trabalho.

#### Monitoramento por indicadores e consequências operacionais

Indicadores podem ser usados para acompanhar a gestão da manutenção por mais de um ângulo. Um grupo de indicadores mostra volume e carga de trabalho, como backlog preventivo e corretivo, com segregação entre itens críticos e não críticos, e horas de manutenção por tipo de atividade. Outro grupo pode monitorar o desempenho de elementos críticos de segurança operacional por meio de indicadores como número de falhas por número de testes em sistemas e componentes críticos.

Em instalações envelhecidas, indicadores semelhantes podem ajudar a avaliar impactos do envelhecimento, especialmente próximos ao fim da vida de projeto ou em transferências de instalações.

Quando existem dados de disponibilidade e confiabilidade e um sistema de codificação de falhas, análises de disponibilidade de elementos críticos de segurança, ou SCEs, podem apoiar a identificação de componentes com falhas e a definição de intervalos de manutenção. Backlog alto de manutenção nesses elementos pode indicar que a confiabilidade geral pode estar abaixo do necessário.

As consequências do descompasso entre backlog e recursos podem atingir a operação. Em um caso investigado no sistema de tratamento de água produzida de uma plataforma, backlog incompatível com a disponibilidade de pessoas a bordo foi associado à insuficiência de recursos, degradação e indisponibilidade de equipamentos, com efeitos como maior controle manual, menor informação de processo e redução da capacidade de separação.

### Condição, falhas e causa raiz

#### Ferrografia e análise de detritos: relação entre óleo, gás e desgaste

A ferrografia é uma técnica de monitoramento por óleo voltada à avaliação de detritos de desgaste, especialmente partículas ferromagnéticas. O princípio é simples: o fluido contendo partículas passa por uma lâmina sob campo magnético, e as partículas são depositadas para posterior leitura. Isso acelera a avaliação laboratorial e pode revelar mudanças na taxa e na natureza do desgaste.

A técnica funciona porque o material removido das superfícies em atrito carrega informação sobre o mecanismo de degradação. Forma, tamanho relativo, quantidade e aspecto das partículas podem indicar se o processo é compatível com desgaste progressivo, contato severo ou mudança abrupta de regime de lubrificação. Em máquinas com óleo lubrificante, isso ajuda a detectar anomalias antes de perda completa de função.

A aplicabilidade tem limites claros: a técnica descrita é voltada a detritos ferromagnéticos, portanto não captura da mesma forma materiais não magnéticos. Além disso, a representatividade depende da circulação do óleo e da chegada das partículas ao ponto de coleta. Em componentes não lavados por lubrificante, a análise pode ser estendida a partículas transportadas por gás e depositadas em superfícies acessíveis, desde que a coleta seja praticável.

#### Seleção e combinação de técnicas conforme equipamento, fluido e regime operacional

A seleção de técnicas de condição não deve ser genérica. Equipamentos rotativos rápidos, como turbogeradores, tendem a responder bem a vibração e análise de óleo porque concentram mecanismos de degradação em mancais, eixos, palhetas, engrenamentos e sistemas de lubrificação. Já equipamentos e sistemas em contato direto com fluidos de processo exigem acompanhamento de integridade física e estado geral em frequência compatível com sua importância para o processo, tipo e condição do fluido e consequências de falha para segurança, meio ambiente e produção.

No FPSO, a criticidade do sistema de geração elétrica aumenta o valor do monitoramento de condição, pois a unidade depende desse sistema para operar os demais subsistemas. Além disso, operações com alta demanda de potência, como offloading, podem alterar carga e esforço dos turbogeradores, o que muda a interpretação de sinais de condição e pode exigir comparação com referências obtidas em regime semelhante.

Na prática, a melhor aplicação costuma combinar histórico de falhas, sintomas observados, mecanismo físico plausível e evidências de mais de uma técnica. Vibração aponta comportamento dinâmico; detritos no óleo mostram desgaste material; investigação de causa raiz conecta ambos ao defeito eliminável e às ações corretivas permanentes.

#### Recorrência, causas sistêmicas e tratamento de eventos semelhantes

Quando diferentes distúrbios de produção apresentam causas raízes semelhantes, a reavaliação de eventos passados ajuda a verificar se recomendações anteriores foram adequadas e se foram realmente encerradas. Esse tratamento amplia a investigação além do evento isolado e favorece a identificação de mecanismos repetitivos.

A combinação de Lean Six Sigma com DMAIC, sigla para Define, Measure, Analyze, Improve e Control, foi apresentada como meio de investigar causas de eventos individuais e também causas sistêmicas. Nesse arranjo, LPO, sigla para Lost Production Opportunity, e MTBF, sigla para Mean Time Between Failures, aparecem como medidas associadas ao comportamento de recorrência e à confiabilidade no caso estudado. A ampliação da cobertura de investigação e a redução do tempo de ciclo foram reportadas para a unidade analisada, sem implicar regra universal.

Como complemento técnico, falhas crônicas e eventos repetitivos exigem leitura do histórico agregado, porque pequenas perturbações sucessivas podem acumular perda de produção e manter vulnerabilidades operacionais mesmo sem parada total da planta. A efetividade do processo depende do envolvimento das pessoas diretamente ligadas ao problema e da disciplina no fechamento das ações definidas.

### Indicadores e confiabilidade

#### Como os indicadores são obtidos a partir dos eventos operacionais

Para calcular indicadores de confiabilidade, o requisito básico é identificar com rastreabilidade quando cada elemento falhou e quando voltou a operar. O registro padronizado de mensagens de evento na falha e no retorno ao estado operacional fornece os instantes necessários para compor tempos entre falhas e tempos individuais de reparo. Com isso, o MTTR pode ser obtido pela soma dos tempos em falha dividida pelo número de falhas registradas. O MTBF é descrito como a razão entre o tempo de acompanhamento e o número de falhas observadas no período. A disponibilidade pode então ser construída a partir da combinação entre tempos entre falhas e tempos totais de reparo. Em sistemas de automação e monitoramento embarcados, a qualidade do indicador depende de o evento representar corretamente a perda e a recuperação da função requerida, e não apenas uma mudança de estado irrelevante. Se houver mensagens heterogêneas entre fabricantes e tecnologias, torna-se mais difícil consolidar bases comparáveis e calcular indicadores de forma uniforme entre diferentes elementos, camadas ou subsistemas.

#### Condições que mudam a interpretação dos dados

Os indicadores só são comparáveis quando as populações analisadas são tecnicamente compatíveis. Bancos de dados de confiabilidade evoluíram justamente para tratar subpopulações não homogêneas, distinguir taxas de falha baseadas em tempo das baseadas em demanda e categorizar modos de falha. Isso evita combinar em um mesmo número equipamentos, regimes ou funções que falham por mecanismos diferentes. Em equipamentos offshore, referências setoriais como OREDA podem apoiar estimativas e comparações, mas seu uso como base de referência não transforma seus valores em requisito obrigatório nem substitui o histórico específico do ativo. Também é necessário reconhecer o limite do indicador médio: MTBF e MTTR resumem comportamento observado, mas podem esconder dispersão, mudanças de regime e diferenças entre fabricantes, configurações ou condições ambientais. Em sensores permanentes submarinos, por exemplo, a extração de tipos de falha, modelagem das falhas, tempo de sobrevivência e MTBF permitiu comparação de desempenho entre fabricantes dentro do conjunto estudado, sem que isso autorize generalização automática para toda a instalação offshore ou para qualquer FPSO.

#### Conceitos centrais e significado operacional

MTBF, do inglês Mean Time Between Failures, expressa o tempo médio entre falhas observadas durante um período de acompanhamento. MTTR, Mean Time To Repair, expressa o tempo médio entre a falha e o retorno do item à condição operacional. A disponibilidade pode ser construída a partir da relação entre tempos entre falhas e tempos de reparo ou retorno. Esses indicadores descrevem dimensões diferentes do desempenho: MTBF resume o comportamento de falha observado, enquanto MTTR resume a capacidade de restaurar a função após a falha. Por isso, não são intercambiáveis. Um sistema pode apresentar intervalos médios longos entre falhas e ainda assim perder muita produção se a recuperação for lenta; também pode falhar mais vezes, mas manter disponibilidade aceitável se o restabelecimento for rápido. Em plataformas offshore, essa distinção é relevante para ativos de produção, utilidades, automação e segurança.

#### O que altera MTBF e o que altera MTTR

O MTBF muda quando mudam os mecanismos que levam o item a falhar ao longo do serviço observado. Isso inclui diferenças de projeto, fabricação, aplicação, ambiente, regime operacional e envelhecimento, desde que esses fatores alterem a frequência ou o intervalo das falhas registradas. Já o MTTR muda quando mudam as condições de recuperação do item após a falha. O tempo de reparo é influenciado por projeto, gestão de recursos, treinamento, estoque de peças, procedimentos e agilidade de deslocamento até a unidade. Assim, o MTTR não representa apenas o reparo físico estrito: ele também reflete mantenabilidade e resposta organizacional até o retorno à operação. Em ambiente offshore, a distância da costa e a dependência de suporte em terra tendem a ampliar a sensibilidade do MTTR à logística, mobilização e acesso. Como consequência, melhorias em sobressalentes, acessibilidade, recursos de apoio e organização do atendimento podem elevar a disponibilidade sem necessariamente alterar o mecanismo físico de falha do componente.

#### Uso na seleção de estratégia e periodicidade

MTBF, MTTR e disponibilidade, isoladamente, não bastam para definir a melhor tarefa de manutenção nem a periodicidade mais adequada. A decisão depende de relacionar o indicador ao modo de falha, à consequência da perda de função e à eficácia real da intervenção proposta. Por isso, a seleção de estratégias costuma exigir análise de criticidade, modos de falha e consequências para segurança, meio ambiente, produção e custo. Técnicas como FMEA, Análise dos Modos de Falha e seus Efeitos, FMECA, Análise dos Modos de Falha, seus Efeitos e Criticidade, e MCC, Manutenção Centrada em Confiabilidade, ajudam a estruturar essa ligação entre comportamento observado e ação de manutenção. Em abordagens multicritério, a manutenção pode ser avaliada simultaneamente por segurança, saúde, meio ambiente, custo de manutenção e perda de produção. Em metodologia proposta para novas unidades offshore, equipamentos de maior criticidade são associados à análise de modos de falha e dados de confiabilidade para subsidiar técnica e periodicidade preventiva.

#### Agregação, padronização e limites de aplicação

Quando elementos têm relevâncias diferentes para automação, produção e segurança, a disponibilidade agregada precisa considerar essa diferença de importância. Em sistemas de automação embarcados, foi proposta ponderação apropriada para compor indicadores de camada porque tratar todos os elementos de forma uniforme pode mascarar a indisponibilidade de itens funcionalmente mais relevantes. O monitoramento também depende de dados diagnósticos comparáveis. Mensagens heterogêneas entre fabricantes, redes e tecnologias dificultam consolidar eventos de falha e retorno em uma base uniforme. Por isso, a padronização aberta e genérica das mensagens de diagnóstico favorece interpretação comum entre diferentes especialidades e aumenta a comparabilidade do acompanhamento. Guias e normas técnicas apoiam aquisição de dados, definição de termos, troca de informações e escolha de técnicas analíticas, mas a seleção do método continua dependente do sistema, do componente e das condições de uso. Análises econômicas simplificadas não bastam, por si sós, para definir benefícios universais ou periodicidades válidas para qualquer instalação.

### Execução, preservação e retorno

#### Função da manutenção e significado do retorno ao serviço

Manutenção é o conjunto de cuidados técnicos que conserva, adequa, restaura, substitui e previne degradações em máquinas, equipamentos, ferramentas e instalações. Seu objetivo operacional é manter o ativo nas condições para as quais foi projetado e fazê-lo retornar a essa condição quando houver desvio. Em um FPSO, esse retorno não é apenas reiniciar um equipamento: envolve restabelecer sua função requerida dentro de limites compatíveis com produção, segurança, meio ambiente e custo.

Esse princípio ganha peso especial em sistemas dos quais a unidade depende integralmente, como a geração de energia. Quando a função do sistema é indispensável para os demais subsistemas, a execução da manutenção e a liberação para operação precisam considerar não só o item intervindo, mas também os efeitos sobre toda a planta. Em unidades offshore distantes da costa, a dificuldade de apoio logístico e o potencial de acidentes graves, danos ambientais e perdas econômicas ampliam a necessidade de preparar bem a intervenção e controlar o retorno ao serviço.

#### Preparação da intervenção: dados úteis, documentação e decisão de engenharia

A preparação da manutenção depende de informação técnica utilizável. Os registros devem privilegiar dados com finalidade definida, evitando informação supérflua ou sem uso claro. Para confiabilidade e manutenção, são relevantes a identificação e taxonomia do equipamento, seus atributos, os dados e causas de falha, as consequências da falha, as ações de manutenção, os recursos utilizados, as consequências da manutenção e o tempo de parada.

Esse conjunto melhora a análise porque permite separar mecanismos de falha diferentes, distinguir eventos associados ao tempo daqueles associados à demanda e tratar populações de equipamentos que não se comportam de modo homogêneo. Documentação técnica, procedimentos e padrões de engenharia apoiam a preparação e a decisão. Quando a ação pretendida estiver em desacordo com essa documentação, ou não estiver coberta por ela, torna-se necessária análise de engenharia e aprovação de profissional habilitado. Em termos técnicos, esse cuidado tende a ganhar importância em itens críticos e em equipamentos expostos a fluidos de processo, porque a importância para o processo, o tipo de fluido e suas condições alteram a relevância das consequências de falha.

#### Testes pós-manutenção, observação inicial e contingência

Após a intervenção, o retorno seguro ao serviço requer verificar se a função pretendida foi restabelecida e se a manutenção não introduziu defeitos latentes. Em termos gerais, o teste pós-manutenção deve confirmar integridade, resposta funcional, ausência de interferências indevidas, compatibilidade com o sistema e estabilidade na operação inicial. Em equipamentos críticos, a verificação tende a incluir também as interfaces com processo, utilidades, automação e proteção, porque a função restaurada pode depender dessas interações para se manter estável.

Em sistemas críticos monitorados remotamente, o acompanhamento em terra pode apoiar a observação do período inicial após a reentrada em serviço, em articulação com a equipe embarcada. Além disso, planos de contingência definem responsabilidades, ações imediatas e recursos humanos, materiais e equipamentos para prevenção, controle e combate à emergência. Quando houver aplicações especiais, ou operações e equipamentos não cobertos pelo manual operacional, podem ser necessários planos específicos disponíveis na locação para operador e executantes.
