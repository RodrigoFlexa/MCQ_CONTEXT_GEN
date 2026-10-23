# Piloto: inventário (estilo qa_v7) x configuração EC

Respondente sem contexto: `gpt-4-1-nano-petrobras`. Juiz: `gpt-5-4-petrobras:high`. Acurácia: correta = 1, parcial = 0,5. Quanto mais difícil a questão, menor deve ser a acurácia.

| Nível | Inventário | EC |
|---|---|---|
| facil | 0.56 (n=26; ✓11 ~7 ✗8; ref. inválida 3) | 0.69 (n=26; ✓16 ~4 ✗6; ref. inválida 1) |
| media | 0.66 (n=50; ✓24 ~18 ✗8; ref. inválida 2) | 0.74 (n=50; ✓30 ~14 ✗6; ref. inválida 2) |
| dificil | 0.60 (n=24; ✓10 ~9 ✗5; ref. inválida 0) | 0.67 (n=24; ✓12 ~8 ✗4; ref. inválida 0) |
| **total** | 0.62 (n=100; ✓45 ~34 ✗21; ref. inválida 5) | 0.71 (n=100; ✓58 ~26 ✗16; ref. inválida 3) |

Inventário por tipo de difícil: dificil_A: 0.50 (n=12; ✓4 ~4 ✗4; ref. inválida 0); dificil_B: 0.71 (n=12; ✓6 ~5 ✗1; ref. inválida 0).

Acurácia só nas referências válidas (sem as marcadas pelo juiz como ambíguas ou erradas): inventario facil: 0.609; inventario media: 0.677; inventario dificil: 0.604; ec facil: 0.72; ec media: 0.771; ec dificil: 0.667.

Inventário: relações {'01_01': 155, '02_02': 340}, combinações {'01_01': 15, '02_02': 15}, geração {'alvos': 100, 'ok': 100, 'insuficiente': 0, 'faltas_de_cota': {}}.
Falhas pendentes: 0.

## Questões avaliadas

**ec · dificil · parcial** Em um FPSO, um KPI de tratamento se afasta da faixa usual logo após perturbação de alimentação e mudança de estratégia de controle feitas para manter o produto em especificação. Minutos depois, as variáveis principais estabilizam e o produto permanece conforme. Qual decisão diagnóstica é correta?

- Referência: Não classificar ainda como perda estrutural; o desvio deve ser interpretado com o contexto do processo e o histórico recente, pois pode ser transitório.
- Respondente: Ajustar temporariamente a estratégia de controle ou otimizar os parâmetros para acomodar a perturbação, após o que o KPI deve retornar à faixa normal, indicando que a mudança foi adequada.
- Juiz: Reconhece um comportamento transitório ligado ao ajuste de controle, mas não explicita a decisão diagnóstica de não tratar o desvio como perda estrutural nem o uso do contexto e histórico.

**ec · dificil · correta** Em um FPSO, o painel em tempo real mostra melhora de um KPI agregado da instalação após redistribuição de carga. A coordenação quer usar esse mesmo indicador para decidir uma ação de melhoria no sistema de compressão, visando recuperar capacidade sem grande investimento. Qual definição de KPI deve prevalecer para sustentar essa decisão?

- Referência: Deve prevalecer um KPI específico do sistema de compressão ou da etapa afetada, coerente com a decisão local; o agregado da instalação não é o mais adequado para essa escolha.
- Respondente: O KPI deve refletir a capacidade operacional do sistema de compressão, como a eficiência ou taxa de compressão, para garantir que melhorias estejam diretamente relacionadas ao desempenho esperado na recuperação de capacidade.
- Juiz: Defende corretamente um KPI específico do sistema de compressão, mais aderente à decisão local do que um indicador agregado da instalação.

**ec · dificil · correta** Em dois meses consecutivos de um FPSO, os acidentes com afastamento caíram de 6 para 4. No mesmo intervalo, as horas-homem de exposição ao risco caíram de 200 mil para 80 mil. O critério de enquadramento permaneceu igual. Concluir melhora do desempenho de segurança só pela contagem bruta está correto?

- Referência: Não. A taxa de frequência por horas-homem aumentou, então a queda no número absoluto de casos não indica melhora real.
- Respondente: Não, a melhoria deve ser avaliada pela taxa de acidentes por hora-homem, não apenas pela contagem bruta, pois leva em consideração a exposição ao risco.
- Juiz: A resposta acerta que a avaliação deve ser pela taxa por horas-homem de exposição, e não pela simples contagem absoluta de acidentes.

**ec · dificil · correta** Dois compressores de um FPSO tiveram o mesmo número de falhas no mês. Em ambos, o reparo ativo levou 2 horas, mas no A houve espera logística e, após o retorno, ele operou temporariamente com restrições; no B, o retorno foi imediato e em condição aceitável. Para explicar por que o A perdeu mais produção, o que deve ser priorizado na análise?

- Referência: Deve-se priorizar o tempo e as condições de retorno à operação aceitável; no A, a indisponibilidade logística e o retorno restrito pesam mais que a frequência de falhas.
- Respondente: Priorize a análise do impacto da espera logística e das restrições operacionais temporárias no compressor A, pois essas condições reduziram a produção apesar do tempo de reparo ser igual ao do B.
- Juiz: Prioriza corretamente a espera logística e as restrições no retorno à operação como os fatores que explicam a maior perda de produção no compressor A.

**ec · dificil · incorreta** Num FPSO, três falhas simultâneas disputam a única equipe especializada. Duas exigem a mesma liberação de área, disponível por apenas 1 hora: uma recoloca a produção em 40 minutos; outra recupera uma função secundária em 3 horas. A terceira não compartilha essa restrição, mas não remove a limitação principal. Qual prioridade técnica deve vir primeiro?

- Referência: A intervenção funcionalmente crítica que cabe na janela de liberação comum, porque combina maior criticidade, menor recuperação e a restrição compartilhada.
- Respondente: A prioridade deve ser a recuperação da função secundária em 3 horas, pois não compartilha a restrição de tempo limitada e garante funcionalidade adicional ao FPSO.
- Juiz: Prioriza a intervenção menos crítica e ignora a janela comum de liberação, contrariando a prioridade da função crítica que restabelece a produção em 40 minutos.

**ec · dificil · correta** Após aumento do corte de água, um separador passou a operar abaixo da eficiência esperada. A qualidade da fase aquosa piorou, a reinjeção disponível está saturada e o tratamento para descarte no mar já opera no limite aceitável; compressão de gás e exportação de óleo permanecem normais. Qual mecanismo explica a necessidade de reduzir a vazão total do campo?

- Referência: A perda de eficiência do separador agravou o gargalo da malha de água produzida; sem capacidade de tratar, reinjetar ou descartar a fase aquosa com qualidade aceitável, a vazão total precisa cair.
- Respondente: Reduzir a vazão diminui a carga na fase aquosa, melhorando sua separação e evitando sobrecarregar o tratamento, garantindo conformidade com limites ambientais e mantendo a eficiência do separador.
- Juiz: Aponta corretamente que a redução de vazão serve para aliviar a carga da fase aquosa e evitar o gargalo do tratamento/descarga de água produzida.

**ec · dificil · correta** Um FPSO ampliou a capacidade de um equipamento para aliviar uma restrição, mas a vazão total não aumentou; a limitação só mudou de lugar na planta. Não houve alteração de fluido nem falha nova. Que diagnóstico esse padrão sustenta?

- Referência: Que o debottlenecking não localizou a variável ou o equipamento realmente limitante; a ação apenas deslocou o gargalo para outro ponto.
- Respondente: Indica que a restrição era na unidade de alívio original e foi realocada, não resolvendo o gargalo. A capacidade global não aumentou, apenas o ponto de alívio foi deslocado.
- Juiz: Conclui corretamente que a ação apenas deslocou o gargalo sem aumentar a capacidade global da planta.

**ec · dificil · parcial** Em um FPSO, um relatório de perdas encerra o caso como queda de vazão do poço após alteração de pressão. Nenhuma ação específica no sistema foi definida porque o registro ficou no efeito observado. Para que a atribuição da perda seja útil à operação, o que ainda precisa ser determinado?

- Referência: O mecanismo que limita a capacidade, o ativo afetado e as condições em que esse mecanismo se tornou dominante; a queda de vazão é só o efeito observado.
- Respondente: A causa exata da queda de vazão, identificando se é devido à formação, bloqueio ou equipamento, para orientar ações corretivas específicas.
- Juiz: A resposta pede identificar a causa, mas não explicita o mecanismo limitante, o ativo afetado e as condições em que ele passou a dominar.

**ec · dificil · parcial** Durante um transitório de processo, a equipe identifica um ajuste temporário que pode estabilizar a operação sem parar a planta. As barreiras técnicas estão disponíveis, mas a bordo faltam as premissas de projeto atualizadas, o suporte remoto não responde no tempo requerido e ninguém tem responsabilidade técnica claramente definida para autorizar a mudança. O que deve ser priorizado para viabilizar um controle efetivo?

- Referência: Priorizar responsabilidade técnica clara a bordo, com acesso à documentação atualizada para revisar premissas e validar a mudança.
- Respondente: Priorizar a autorização formal de um responsável técnico, garantindo a conformidade e segurança antes de qualquer ajuste temporário.
- Juiz: Acerta a necessidade de um responsável técnico claro para autorizar, mas omite o acesso à documentação atualizada para revisar premissas e validar a mudança.

**ec · dificil · correta** A unidade mantém monitoramento sistemático de risco e emite relatórios ao fim de cada parada. Mesmo assim, duas intervenções semelhantes repetem atraso na linha crítica, aumento de escopo e falta de suporte; as lições foram copiadas entre relatórios, sem verificar se ainda valiam. Qual falha de gestão explica melhor a repetição?

- Referência: Preenchimento formal sem análise crítica real do histórico, impedindo que o aprendizado retroalimente o planejamento.
- Respondente: Falha na análise de lições aprendidas e na implementação de melhorias contínuas, levando à repetição de erros similares.
- Juiz: Corresponde à falha de fazer lições aprendidas de forma apenas formal, sem análise crítica e sem retroalimentar o planejamento com melhorias reais.

**ec · dificil · correta** No histórico da frota, medição concentrou mais eventos que separação. No FPSO em análise, porém, a função de separação opera com barreira degradada e manutenção atrasada, enquanto a medição mantém desempenho previsto. Na atualização dos controles de risco, qual função deve receber prioridade na seleção de sistemas críticos?

- Referência: A separação, porque a seleção deve refletir a vulnerabilidade real da unidade; o histórico apenas informa a análise.
- Respondente: A função de separação deve receber prioridade na seleção de sistemas críticos devido à sua deficiência operativa e impacto no risco geral do FPSO.
- Juiz: Prioriza corretamente a separação com base na vulnerabilidade atual da unidade, e não no histórico agregado da frota.

**ec · dificil · incorreta** Um equipamento crítico de FPSO opera degradado, mas sua probabilidade histórica de falha é baixa. Não há sobressalente a bordo, a mobilização depende de janela logística e o especialista só chega dias depois. Na decisão entre intervir agora ou adiar, qual aspecto deve orientar a escolha?

- Referência: O tempo e os meios para restaurar a função, porque a disponibilidade fica limitada pelo suporte de manutenção e pelos recursos externos.
- Respondente: A criticidade do equipamento e o risco de falha inesperada devem orientar a decisão, priorizando intervenção imediata se o impacto operacional ou ambiental for elevado.
- Juiz: Foca criticidade e risco de falha, mas a referência pede como fator decisivo o tempo e os meios para restaurar a função diante das restrições logísticas e de suporte.

**ec · dificil · parcial** Uma equipe avaliou um produto para uma emulsão óleo-em-água. No bottle test, escolheu o candidato que mais aumentou a liberação de água do petróleo e ignorou o comportamento da fase aquosa. Qual foi o erro técnico na seleção?

- Referência: Usou o critério de água-em-óleo; em emulsão óleo-em-água, o indicador relevante é a clarificação da fase aquosa.
- Respondente: O erro foi focar na liberação de água sem avaliar a estabilidade da emulsão. Isso pode levar à seleção de um produto que não mantém a emulsificação adequada, comprometendo o desempenho em condições reais.
- Juiz: Identificou o erro de focar na liberação de água, mas não explicitou que, em emulsão óleo-em-água, o critério correto é a clarificação da fase aquosa.

**ec · dificil · parcial** Após mudar o blend de produção, a emulsão passou a separar mal. As análises mostram mais asfaltenos e sólidos, e uma tentativa de aumentar a salinidade não trouxe melhora. Sem outras anomalias de processo, qual decisão técnica deve ter prioridade antes de novos ajustes de pH ou salinidade?

- Referência: Reavaliar e comparar os produtos nas condições representativas do novo sistema, porque filmes de asfaltenos e sólidos podem exigir outra formulação e maior salinidade não garante melhor separação.
- Respondente: Realizar uma análise detalhada do conteúdo de asfaltenos e sólidos para identificar possíveis mudanças na composição, e considerar a utilização de aditivos dispersantes ou modificadores de fluxo antes de ajustes de pH ou salinidade.
- Juiz: Reconhece a mudança de composição, mas não prioriza a reavaliação e comparação dos produtos de separação nas novas condições e ainda sugere aditivos de outra natureza.

**ec · dificil · correta** Num FPSO, um antiespumante reduziu o arraste de líquido no gás no início da produção. Meses depois, a espuma reaparece e o arraste volta, embora vazão de injeção, equipamento e arranjo de aplicação permaneçam inalterados. No mesmo período aumentaram corte de água, sólidos produzidos e salinidade. Entre manter o programa químico como está e revê-lo, qual decisão é correta?

- Referência: Rever o programa químico e reavaliar o antiespumante, porque a mudança do fluido deslocou o equilíbrio entre formação e quebra de espuma.
- Respondente: Rever o programa químico é recomendável para ajustar ao aumento de sólidos, água e salinidade, garantindo a eficácia do antiespumante e controle de espuma.
- Juiz: Conclui corretamente que o programa químico deve ser revisto diante da mudança do fluido que afetou a eficácia do antiespumante.

**ec · dificil · correta** Em uma unidade com flotação por ar dissolvido, a geração de microbolhas está normal. A dosagem de coagulante já reduziu a repulsão elétrica, mas os agregados observados seguem pequenos e se rompem na circulação, mantendo baixa remoção de óleo. Qual função química está faltando no condicionamento?

- Referência: Falta a ação de ponte de um floculante polimérico, para gerar flocos maiores e mais resistentes, mais capturáveis por microbolhas.
- Respondente: Falta o uso de um floculante ou adjuvante coagular para promover a formação de flocos maiores e estáveis, facilitando a agregação e remoção efetiva do óleo.
- Juiz: Indica corretamente a necessidade de um floculante para formar flocos maiores e mais estáveis, equivalente à função de ponte da referência.

**ec · dificil · incorreta** Uma FPSO opera com URS. A saída mais carregada da unidade passou a ter risco local de depósito, enquanto a equipe tenta proteger os poços produtores aumentando a dosagem apenas na água de injeção. Qual aplicação do anti-incrustante deve ser priorizada?

- Referência: A proteção dos pontos da URS onde as espécies incrustantes se concentram; dosar só a água de injeção não assegura proteção aos produtores, porque o produto pode adsorver na rocha junto ao injetor.
- Respondente: Priorizar a aplicação de anti-incrustantes na água de injeção para prevenir depósitos na linha de saída mais carregada, garantindo fluxo e proteção do equipamento.
- Juiz: Contraria a referência ao priorizar dosagem apenas na água de injeção, em vez de proteger os pontos da URS onde a incrustação se concentra.

**ec · dificil · incorreta** Em uma unidade de água de injeção, o teor de oxigênio na água de entrada e a vazão da bomba dosadora permaneceram estáveis. Mesmo assim, a remoção piorou logo após começar o uso de uma solução preparada dias antes e mantida em tanque parcialmente cheio e ventilado. Qual diagnóstico melhor explica o desvio?

- Referência: A solução perdeu concentração ativa no armazenamento com contato com ar, e a mesma vazão volumétrica deixou de atender à demanda estequiométrica.
- Respondente: Possível proliferação bacteriana devido à estagnação da água e exposição ao ar, levando à formação de biofilmes e corrosão. A solução armazenada pode ter favorecido microrganismos que aumentam a resistência à remoção.
- Juiz: O desvio é melhor explicado pela perda de concentração ativa da solução armazenada em contato com o ar, não por proliferação bacteriana na linha de remoção de oxigênio.

**ec · dificil · parcial** Após iniciar desaeração a vácuo em água do mar, aumenta a tendência de depósito carbonático e o bissulfito passa a render menos na remoção de oxigênio dissolvido. Análises mostram cloro residual elevado na alimentação. Qual combinação de mecanismos explica esses dois efeitos?

- Referência: O cloro residual compete com o oxigênio e consome parte do bissulfito; ao mesmo tempo, a remoção de CO2 no vácuo pode favorecer a precipitação de carbonato de cálcio.
- Respondente: Cloro residual elevada promove formação de carbonatos ao reagir com íons cálcio, formando depósitos, e oxida BSS, reduzindo sua eficiência na remoção de oxigênio, dificultando a desaeração em água do mar.
- Juiz: Acerta que o cloro residual consome/oxida o bissulfito, mas erra o mecanismo do depósito carbonático, que decorre da remoção de CO2 no vácuo e não de reação do cloro com cálcio.

**ec · dificil · parcial** Em um sistema de água de injeção sob tratamento prolongado, a amostragem do fluido mostra baixa contagem de bactérias livres. Na inspeção de um trecho rugoso aparecem depósitos aderidos, biofilme recoberto por incrustação mineral e ataque localizado. Qual interpretação técnica do caso é mais consistente?

- Referência: Há regiões inacessíveis sob depósitos, onde o biocida não penetra adequadamente; o ataque não deve ser atribuído diretamente às bactérias sem avaliar também depósitos, química da água e suscetibilidade do material.
- Respondente: O sistema apresenta biofilme estabilizado com incrustações minerais, resultando em ataque localizado devido à corrosão sob biofilme, mesmo com baixa contagem de bactérias livres no fluido de injeção prolongada.
- Juiz: Reconhece biofilme/incrustação e ataque localizado, mas atribui a corrosão diretamente ao biofilme e omite a limitação de penetração do biocida e a necessidade de avaliar depósitos, química da água e material.

**ec · dificil · correta** Em um FPSO, o mesmo sistema de tratamento de gás inclui um trecho frio com risco de hidrato, um vaso com tendência à espuma e outro trecho onde a fase aquosa acelera o ataque ao aço. A equipe propõe usar um único químico em uma única corrente e no mesmo ponto de injeção para simplificar a operação. Qual decisão técnica é correta?

- Referência: Rejeitar a simplificação: os químicos devem ser selecionados pela ameaça dominante em cada trecho e não necessariamente na mesma corrente, concentração ou ponto de injeção.
- Respondente: Não, usar um único químico no mesmo ponto não é recomendado devido às diferentes naturezas e necessidades de cada trecho, prejudicando a eficácia do tratamento.
- Juiz: Rejeita corretamente a simplificação e reconhece que cada trecho requer seleção de químico conforme a ameaça dominante.

**ec · dificil · correta** Em um FPSO, escolheu-se combinar um inibidor de corrosão com um sequestrante de H2S porque cada um atendia sua própria função. A mistura foi aprovada em laboratório apenas em solução com NaCl, mas falha no serviço com água produzida multissalina e materiais específicos. Qual falha de avaliação explica esse falso sinal de compatibilidade?

- Referência: O ensaio foi não representativo do serviço: inferiu compatibilidade pela função e usou só NaCl, que não reproduz a água produzida multissalina.
- Respondente: A avaliação não considerou a interação entre os inibidores e materiais específicos na água multissalina, levando a uma compatibilidade aparente que falhou em condições reais devido às diferenças químicas e de salinidade.
- Juiz: Aponta corretamente que a avaliação foi não representativa das condições reais, por não reproduzir a água produzida multissalina e as interações relevantes do serviço.

**ec · dificil · correta** Em um campo com risco de incrustação por sulfato, uma tecnologia de transporte e retenção de inibidor no reservatório projeta custo menor que a URS. Porém, ainda não comprovou distribuição do inibidor, sua liberação nem compatibilidade. Na priorização da decisão, o menor custo basta para colocá-la no mesmo nível da remoção de sulfato, ou é necessária outra condição antes disso?

- Referência: Não; antes, é necessária a validação de distribuição, liberação e compatibilidade.
- Respondente: Outra condição é essencial. Sem comprovação da distribuição, liberação e compatibilidade do inibidor, seu uso não pode ser priorizado igual à remoção do sulfato, que oferece garantia de eficiência.
- Juiz: Afirma corretamente que o menor custo não basta sem validar distribuição, liberação e compatibilidade do inibidor.

**ec · dificil · parcial** Em um FPSO com oscilações usuais de vazão, pressão e composição, surge instabilidade a jusante: espuma inesperada e queda da eficiência de separação. A dosagem comandada e o consumo medido de um químico permanecem coerentes, não houve mistura com outros produtos, e o conteúdo do tanque de serviço mudou de cor após estocagem. Qual diagnóstico deve ser priorizado?

- Referência: Degradação do produto armazenado, pois a alteração de cor e a perda de resposta com dosagem coerente apontam para isso.
- Respondente: Priorizaria a inspeção do conteúdo do tanque de serviço, pois a mudança de cor sugere contaminação ou alteração química, podendo impactar na eficiência da separação e causar a espuma e instabilidades observadas.
- Juiz: Percebe que houve alteração do produto no tanque, mas não prioriza claramente a degradação do produto armazenado, que é o diagnóstico indicado pela referência.

**ec · facil · correta** Qual é a relação correta entre um KPI operacional e a variável de processo que ele acompanha?

- Referência: O KPI não substitui a variável de processo; ele resume seu efeito sobre o desempenho.
- Respondente: O KPI operacional deve refletir a performance da variável de processo, sendo uma métrica quantificável e específica que indica eficiência, produtividade ou qualidade do processo monitorado.
- Juiz: A resposta descreve o KPI como uma métrica de desempenho derivada da variável de processo, consistente com a ideia de que ele resume seu efeito.

**ec · facil · correta** Qual é a função básica de um KPI em processos industriais?

- Referência: Avaliar a eficiência e o desempenho dos processos.
- Respondente: Monitorar e medir o desempenho dos processos para identificar melhorias e garantir eficiência operacional.
- Juiz: A resposta traz a função de medir e monitorar o desempenho para avaliar a eficiência e orientar melhorias, equivalente à referência.

**ec · facil · incorreta** Que atributo expressa a chance de restaurar um sistema defeituoso em tempo especificado?

- Referência: Mantenabilidade.
- Respondente: O atributo é a taxa de confiabilidade, que indica a probabilidade de um sistema operar sem falhas em um tempo determinado.
- Juiz: Confundiu mantenabilidade com confiabilidade, que trata da probabilidade de operar sem falhas e não da restauração em tempo especificado.

**ec · facil · correta** Em estado estacionário, qual razão pode representar a disponibilidade?

- Referência: Uptime dividido pelo tempo total observado.
- Respondente: A disponibilidade pode ser representada pela razão entre o tempo de operação útil e o tempo total, incluindo falhas e manutenções.
- Juiz: A razão entre tempo de operação útil e tempo total observado corresponde à definição de disponibilidade em estado estacionário.

**ec · facil · correta** Em compressão, geração e tratamento em FPSO, o que caracteriza uma redundância útil?

- Referência: Preservar a função de processo relevante, não apenas duplicar equipamento.
- Respondente: Redundância útil em FPSO caracteriza-se por sistemas duplicados essenciais para continuidade operacional, garantindo segurança e funcionalidade, como unidades de armazenamento, sistemas de processamento ou energia, que podem assumir funções em caso de falha de um componente.
- Juiz: A resposta descreve redundância que mantém a função operacional relevante em caso de falha, que é a essência da referência.

**ec · facil · correta** Além de confiabilidade, disponibilidade e manutenibilidade, que dimensão o RAMS acrescenta à análise?

- Referência: Segurança.
- Respondente: O RAMS acrescenta a dimensão de segurança à análise, enfocando a confiabilidade, disponibilidade e manutenibilidade, mas também considerando aspectos de segurança operacional e minimização de riscos.
- Juiz: Ele identifica corretamente a segurança como a dimensão adicional do RAMS.

**ec · facil · correta** Qual indicador de reparo é calculado com o início da falha e o retorno à operação?

- Referência: MTTR.
- Respondente: O indicador é o Tempo Médio de Reparo (MTTR), que calcula o tempo desde o início da falha até o retorno à operação.
- Juiz: Identifica corretamente o MTTR como o tempo entre o início da falha e o retorno à operação.

**ec · facil · correta** Que finalidade operacional justifica a parada por função de proteção?

- Referência: Evitar estados perigosos, danos ambientais e consequências maiores.
- Respondente: A parada por função de proteção justifica-se para prevenir danos ao equipamento, evitar acidentes ou condições de operação inseguras, garantindo integridade estrutural e operacional do sistema.
- Juiz: Expressa a finalidade essencial de evitar condições inseguras e consequências maiores por meio da parada de proteção.

**ec · facil · parcial** Qual é a função do processamento primário nas facilidades de produção marítimas?

- Referência: Separar e tratar óleo, gás e água sob condições controladas.
- Respondente: O processamento primário remove água, gás dissolvido e impurezas do óleo bruto, estabilizando o petróleo para transporte e posterior refino.
- Juiz: Descreve a estabilização do óleo removendo água e gás, mas omite a função mais ampla de separar e tratar também as correntes de gás e água sob controle.

**ec · facil · incorreta** Quando a restrição está em um ponto comum do sistema do FPSO, qual decisão gerencial se torna inevitável?

- Referência: Priorizar entregas e alocar a capacidade disponível.
- Respondente: A decisão de reduzir a produção temporariamente para evitar riscos ou danos ao sistema, priorizando segurança e integridade do FPSO.
- Juiz: A referência trata da necessidade de priorizar entregas e alocar a capacidade disponível no gargalo comum, enquanto o candidato responde com redução temporária de produção por segurança.

**ec · facil · correta** Para que serve identificar componentes e sistemas críticos em um FPSO?

- Referência: Para orientar a implantação e a atualização dos controles de risco, priorizando as funções que merecem tratamento.
- Respondente: Para garantir a segurança, eficiência operacional e manutenção prioritária, prevenindo falhas catastróficas e assegurando a integridade do FPSO.
- Juiz: A resposta preserva a finalidade essencial de priorizar itens críticos para ações de segurança, integridade e tratamento de risco.

**ec · facil · correta** O que a confiabilidade de um item mede ao longo do tempo?

- Referência: A capacidade de cumprir a função requerida, sob condições especificadas, durante um intervalo de tempo.
- Respondente: A confiabilidade mede a probabilidade de um item operar sem falhas por um período específico, ao longo do tempo.
- Juiz: Define confiabilidade como a probabilidade de operar sem falhas por um período, equivalente à capacidade de cumprir a função requerida ao longo de um intervalo.

**ec · facil · parcial** Na análise de falhas, qual é a função técnica da FMEA?

- Referência: Estruturar a avaliação dos modos de falha e de seus efeitos, causas e controles.
- Respondente: Identificar, priorizar e minimizar riscos de falhas potencializando a confiabilidade dos equipamentos e processos.
- Juiz: Traz a ideia geral de identificar e priorizar falhas, mas omite a função específica da FMEA de estruturar modos de falha, efeitos, causas e controles.

**ec · facil · incorreta** Qual amostra serve de referência para avaliar a separação natural no bottle test?

- Referência: A amostra sem aditivo.
- Respondente: A amostra de óleo obtida após a primeira fase de decantação é usada como referência para avaliar a separação natural no bottle test.
- Juiz: A referência do bottle test é a amostra sem aditivo, não uma amostra após decantação.

**ec · facil · correta** Para romper a espuma, que região da bolha o antiespumante precisa alcançar?

- Referência: O filme que estabiliza a bolha, para favorecer sua ruptura ou drenagem.
- Respondente: O antiespumante deve alcançar a interface entre a bolha e a fase contínua para quebrar a espuma eficientemente.
- Juiz: Atinge a ideia central de que o antiespumante deve chegar à região interfacial/filme da bolha para promover sua ruptura.

**ec · facil · correta** Qual efeito a melhora da quebra de espuma tende a ter na saída de gás de um separador?

- Referência: Redução do arraste de líquido na saída de gás.
- Respondente: A melhora na quebra de espuma reduz a entrada de líquidos na saída de gás, aumentando a pureza do gás extraído e prevenindo problemas de corrosão e eficiência no processamento.
- Juiz: A melhora da quebra de espuma reduz o arraste de líquido na saída de gás, que é exatamente o efeito descrito na referência.

**ec · facil · parcial** Antes de considerar equivalentes um coagulante natural e um sintético, o que deve ser comprovado?

- Referência: A equivalência de desempenho na água produzida de interesse.
- Respondente: A eficácia na remoção de contaminantes, compatibilidade com o sistema, estabilidade durante o uso e impacto ambiental dos dois coagulantes.
- Juiz: Cita eficácia e outros critérios relevantes, mas não explicita a comprovação da equivalência de desempenho na água produzida específica.

**ec · facil · incorreta** Qual rota de desoxigenação é alternativa quando o gás de arraste está indisponível ou inadequado?

- Referência: A desaeração a vácuo.
- Respondente: A rota de desoxigenação alternativa inclui uso de agentes redutores químicos, como hidrazina, ou a desoxigenação por injeção de osmose ou lavagem com água com redução de oxigênio.
- Juiz: A referência pede a desaeração a vácuo como rota alternativa ao gás de arraste, e o candidato respondeu com agentes químicos e opções que não correspondem a essa rota.

**ec · facil · correta** Qual é a função do controle microbiológico na água de injeção?

- Referência: Limitar a contaminação, o crescimento e a atividade de microrganismos que favorecem biofilme, souring e corrosão microbiologicamente influenciada.
- Respondente: Garantir a ausência de microrganismos que possam causar corrosão ou obstruções, assegurando a qualidade e integridade do sistema de produção de óleo e gás.
- Juiz: Expressa o objetivo de controlar microrganismos para evitar danos como corrosão e obstruções, equivalente à função do controle microbiológico.

**ec · facil · incorreta · ref. inválida** Além da concentração, qual parâmetro do tratamento também afeta o desempenho químico contra microrganismos?

- Referência: O tempo de contato.
- Respondente: O pH do tratamento também impacta o desempenho químico contra microrganismos.
- Juiz: A referência aponta tempo de contato e o candidato cita pH, e a pergunta isoladamente admite mais de um parâmetro plausível, tornando a referência não única.

**ec · facil · parcial** Que tipo de inibidor é o MEG na prevenção de hidratos?

- Referência: Um inibidor termodinâmico.
- Respondente: O MEG (monoetilenoglicol) é um inibidor termofísico de formação de hidratos, atuando por dissolver água e reduzir a temperatura de formação dos hidratos.
- Juiz: Descreve o mecanismo geral corretamente, porém classifica o MEG como 'termofísico' em vez de inibidor termodinâmico.

**ec · facil · correta** Qual parâmetro de composição o monitoramento do programa de MEG acompanha na fase aquosa?

- Referência: A concentração de glicol na fase aquosa.
- Respondente: O monitoramento acompanha a concentração de etileno glicol na fase aquosa, garantindo a eficiência da remoção de umectantes e proteção do sistema de gás. Também verifica condições de corrosividade e a presença de contaminantes.
- Juiz: Identifica corretamente o parâmetro monitorado como a concentração de etileno glicol na fase aquosa, e os detalhes adicionais não contradizem a referência.

**ec · facil · correta** Que função tem o sequestrante de H2S no tratamento do gás?

- Referência: Consumir ou imobilizar a espécie sulfídrica.
- Respondente: O sequestrante de H2S remove o gás sulfidrico, protegendo equipamentos, evitando corrosão e garantindo a qualidade do gás para uso ou processamento.
- Juiz: Descreve a remoção ou neutralização do H2S, que corresponde à função de consumir ou imobilizar a espécie sulfídrica.

**ec · facil · incorreta** Como a URS faz a remoção seletiva de sulfato?

- Referência: Por membranas adequadas ao serviço.
- Respondente: A URS utiliza processos de troca iônica ou precipitação química para remover seletivamente o sulfato, promovendo sua troca por cloreto ou precipitação como sulfato de bário, dependendo da aplicação.
- Juiz: A referência indica remoção seletiva por membranas, e o candidato respondeu com troca iônica/precipitação química, que não corresponde ao mecanismo esperado da URS.

**ec · facil · correta** Qual é a função da segregação entre produtos químicos em uma instalação offshore?

- Referência: Impedir contato não intencional entre incompatíveis e evitar perda de desempenho por reação paralela.
- Respondente: A segregação evita reações químicas inadvertidas, garante a compatibilidade de produtos e previne contaminações, assegurando a segurança operacional e a integridade do sistema.
- Juiz: A resposta cobre a função essencial da segregação ao evitar contato indevido, reações inadvertidas e contaminação entre produtos incompatíveis.

**ec · facil · correta** Além do nível do tanque, que condições o monitoramento do armazenamento e manuseio deve verificar?

- Referência: Condições que antecedem falhas de segurança, corrosão ou perda de desempenho.
- Respondente: Temperatura, pressão, vazamentos, corrosão, integridade estrutural, compatibilidade do material, e condições de segurança operacionais.
- Juiz: Lista condições de monitoramento coerentes com a ideia de detectar antecipadamente riscos de segurança, corrosão e perda de desempenho.

**ec · media · correta** O óleo ainda atende à especificação, mas o KPI mostra deterioração contínua que sugere desvio futuro. Que objetivo do monitoramento está sendo usado ao investigar isso agora?

- Referência: Antecipar anormalidades.
- Respondente: O objetivo é prever a degradação do óleo, identificar tendências de deterioração e evitar falhas futuras, garantindo a manutenção pró-ativa.
- Juiz: Descreve corretamente o uso do monitoramento para antecipar anormalidades antes de o óleo sair de especificação.

**ec · media · correta** No mesmo processo de um FPSO, a sala de controle acompanha a operação em tempo real e a gerência faz revisão mensal de desempenho. O indicador precisa ser o mesmo nas duas análises?

- Referência: Não. O mesmo processo pode usar indicadores diferentes, porque a forma de expressão depende da finalidade da avaliação e do usuário.
- Respondente: Não, o indicador na sala de controle é em tempo real, enquanto na revisão mensal pode incluir análises mais abrangentes, com dados agregados e tendências.
- Juiz: Responde que não e justifica corretamente que a análise operacional e a gerencial podem usar indicadores distintos conforme a finalidade e a agregação dos dados.

**ec · media · correta** Em um FPSO, duas taxas mensais de frequência de acidentes usam a mesma base de horas-homem, mas no segundo mês o critério de enquadramento dos casos foi ampliado. A comparação direta continua consistente?

- Referência: Não. A comparação fica comprometida porque mudou a definição dos casos que entram no numerador.
- Respondente: Não, a comparação direta não é consistente devido à ampliação do critério de enquadramento, que pode aumentar a contagem de acidentes e afetar a taxa calculada.
- Juiz: A resposta coincide com a referência ao apontar que a mudança no critério do numerador compromete a comparação direta entre as taxas.

**ec · media · correta** Em um FPSO, a lógica de proteção retira um equipamento de serviço ao detectar condição perigosa e evita dano maior. Qual efeito isso pode ter sobre a continuidade operacional?

- Referência: Pode reduzi-la, porque o sistema sai de serviço para preservar segurança e integridade.
- Respondente: Pode interromper temporariamente a operação do equipamento, impactando a continuidade, mas previne danos maiores, garantindo segurança e integridade do FPSO a longo prazo.
- Juiz: Expressa corretamente que a lógica de proteção pode tirar o equipamento de serviço e reduzir a continuidade operacional para preservar segurança e integridade.

**ec · media · correta** Dois relatórios usam critérios diferentes para contar indisponibilidades do mesmo sistema. Sem mudança real no equipamento, o que passa a explicar parte da diferença entre os valores de disponibilidade?

- Referência: O escopo do indicador, porque cada relatório inclui downtimes diferentes.
- Respondente: Diferenças nos critérios de classificação de indisponibilidade, como tempos mínimos ou causas consideradas, explicam variações na disponibilidade, mesmo sem mudanças no equipamento.
- Juiz: O candidato atribui a diferença aos critérios e ao escopo usados para contabilizar indisponibilidades, que é a mesma ideia central da referência.

**ec · media · parcial** Dois compressores falham com a mesma frequência e exigem o mesmo tempo de reparo ativo. Mesmo assim, um deles tem menor disponibilidade operacional. Que diferença explica esse resultado?

- Referência: Tempos logísticos e administrativos maiores em cada falha.
- Respondente: O compressor com menor disponibilidade provavelmente apresenta maior tempo de inatividade total, incluindo paradas programadas ou paradas não relacionadas ao reparo, além do tempo de reparo em si.
- Juiz: Percebe que a diferença está no tempo total de indisponibilidade, mas não identifica o ponto decisivo da referência, que são os atrasos logísticos e administrativos em cada falha.

**ec · media · correta** Num arranjo com reserva fria em um FPSO, o equipamento reserva não trabalha sob a mesma carga do ativo. Se ele permanece íntegro em espera, mas a função não retorna quando é solicitado, qual falha explica a perda do serviço?

- Referência: Falha de partida ou de comutação do equipamento reserva.
- Respondente: A falha pode ser uma falha na automação ou no sistema de transferência que impede a retomada da função, mesmo com o equipamento reserva intacto, levando à perda do serviço.
- Juiz: Descreve uma falha de automação ou transferência que impede a entrada do reserva, equivalente à falha de partida/comutação da referência.

**ec · media · correta** Em um FPSO, dois geradores redundantes podem ser bloqueados pela mesma lógica automática de proteção. Se esse bloqueio atuar, qual efeito a redundância terá sobre a indisponibilidade desse evento?

- Referência: Nenhum; uma lógica de intertravamento comum continua tornando os dois indisponíveis.
- Respondente: A redundância não reduz a indisponibilidade, pois o bloqueio simultâneo dos geradores elimina a possibilidade de backup ativo, aumentando o risco de falha total no sistema elétrico.
- Juiz: Expressa corretamente que a redundância não reduz a indisponibilidade quando uma lógica comum pode bloquear simultaneamente os dois geradores.

**ec · media · correta** Na fase preliminar de projeto de um FPSO, a equipe quer validar arranjo, quantidade de equipamentos e alternativas de redundância. Que nível de modelagem RAM é adequado nessa etapa?

- Referência: Modelos mais simples, suficientes para essa validação preliminar.
- Respondente: Modelo de Arquitetura de Recursos (RAM) de alto nível, que avalia arranjos, quantidade de equipamentos e redundâncias preliminares para validar soluções.
- Juiz: Modelo de alto nível ou simples para validar arranjo, quantidade de equipamentos e redundância na fase preliminar corresponde ao nível pedido.

**ec · media · correta** Após o detalhamento do sistema, a equipe manteve um modelo RAM preliminar e quer priorizar melhorias comparando modos operacionais. Que limitação esse modelo tende a ter?

- Referência: Tende a não identificar adequadamente os maiores contribuintes de falha nem a refinar as previsões de disponibilidade e confiabilidade.
- Respondente: O modelo RAM preliminar tende a simplificar, não capturando todas as variabilidades reais e interações complexas, limitando a precisão na priorização de melhorias entre modos operacionais.
- Juiz: A resposta expressa a mesma limitação essencial de um modelo RAM preliminar: simplificação excessiva que prejudica a priorização de melhorias e a qualidade das previsões.

**ec · media · correta** Em um FPSO, as ordens de manutenção registram várias paradas sob uma categoria genérica, sem distinguir mecanismos de falha. Qual consequência isso traz para priorizar ações corretivas?

- Referência: As causas deixam de ser distinguíveis, reduzindo a utilidade dos dados para priorizar ações corretivas.
- Respondente: Dificulta identificar causas específicas, comprometendo a priorização eficiente de ações corretivas e podendo gerar manutenção reativa, aumento de custos e downtime não otimizado.
- Juiz: A resposta coincide com a referência ao afirmar que a categorização genérica impede distinguir causas e prejudica a priorização das ações corretivas.

**ec · media · parcial** Um FPSO ampliou a equipe de manutenção, mas o retorno ao serviço continua atrasado porque os reparos aguardam sobressalente, liberação e logística. Qual efeito essa ampliação tende a ter na disponibilidade?

- Referência: Tende a gerar ganho limitado, porque o gargalo do retorno operacional não está na capacidade das equipes.
- Respondente: A ampliação da equipe, sem suprimentos e logística adequados, pode temporariamente reduzir a disponibilidade operacional devido a gargalos na manutenção e reparos.
- Juiz: Percebe que o gargalo está em sobressalentes, liberações e logística, mas erra ao dizer que a disponibilidade tende a cair, quando a referência aponta ganho apenas limitado.

**ec · media · incorreta** Os fluidos chegam misturados e com impurezas. Mesmo com a separação estável, a movimentação dos fluxos virou o limitante. O que explica a perda de capacidade da unidade?

- Referência: Porque a capacidade produtiva depende da capacidade combinada de separação, tratamento e movimentação; se a movimentação limita, a unidade perde capacidade.
- Respondente: A perda de capacidade ocorre devido ao acúmulo de impurezas e sedimentos, que obstruem componentes, além do aumento da viscosidade dos fluidos, dificultando o fluxo e sobrecarregando os equipamentos.
- Juiz: A referência trata de limitação de capacidade por gargalo na movimentação dos fluxos, enquanto a resposta atribui a perda a obstrução, sedimentos e viscosidade.

**ec · media · incorreta · ref. inválida** Um tratador passou a operar abaixo da eficiência esperada e a qualidade das correntes separadas caiu. Para manter especificações e estabilidade operacional, que ajuste pode ser necessário?

- Referência: Reduzir a produção.
- Respondente: Ajustar os parâmetros de controle do tratador, como vazão, temperatura ou pressão, e realizar limpeza ou manutenção nos filtros para melhorar a eficiência e a qualidade das correntes separadas.
- Juiz: A resposta não traz a redução de produção da referência e a própria pergunta é ambígua, pois admite outras ações operacionais igualmente plausíveis sem fixar restrições.

**ec · media · parcial** Dois FPSOs têm a mesma demanda de produção. Um deles foi concebido considerando localização, meio ambiente, ancoragem, casco, convés e arranjo de produção e armazenagem para reduzir impactos operacionais. O que se espera dessa unidade entre operações de offloading?

- Referência: Maior capacidade de minimizar paradas e problemas entre offloadings.
- Respondente: Espera-se maior eficiência operacional, menor tempo de offloading, redução de custos e menor impacto ambiental devido ao design otimizado e melhor integração dos sistemas.
- Juiz: Traz ganhos operacionais genéricos, mas não responde de forma direta ao ponto central da referência, que é minimizar paradas e problemas entre offloadings.

**ec · media · correta** Duas interdições decorrem da mesma falha operacional. Uma unidade produz mais e fica indisponível por mais tempo que a outra. Em qual delas a perda econômica tende a ser maior?

- Referência: Na unidade com maior volume produzido e maior duração da indisponibilidade.
- Respondente: Na unidade que produz mais e fica indisponível por mais tempo, a perda econômica tende a ser maior devido ao valor ou volume maior de produção afetada.
- Juiz: Reproduz a resposta essencial de que a maior perda econômica ocorre na unidade com maior produção e maior tempo de indisponibilidade.

**ec · media · parcial** Uma obstrução por incrustação já formada na coluna passou a limitar a capacidade. Para recuperar produção, que intervenção pode se tornar necessária?

- Referência: Remoção do depósito e avaliação da integridade do equipamento.
- Respondente: Realizar limpeza por fraturamento, utilização de fluidos quimiotratantes ou intervenções mecânicas para remover incrustações e restabelecer a capacidade da coluna.
- Juiz: Acerta a necessidade de remover a incrustação para recuperar capacidade, mas omite a avaliação de integridade do equipamento após a intervenção.

**ec · media · correta** Durante operação estável, a separação óleo-água perde eficiência. Qual é a consequência esperada para a detecção e correção de desvios?

- Referência: A observabilidade do processo e a margem para detectar e corrigir desvios diminuem, elevando o risco.
- Respondente: A perda de eficiência na separação dificulta a detecção de desvios devido ao aumento da presença de água no óleo, dificultando a identificação de anomalias e atrasando a correção, podendo levar a problemas de qualidade e operacionais.
- Juiz: Equivale à perda de observabilidade e de capacidade de correção ao afirmar que os desvios ficam mais difíceis de perceber e corrigir.

**ec · media · correta** Duas unidades têm a mesma designação. Na X, instrumentação, capacidade de segregação, inventário intermediário e flexibilidade operacional são maiores que na Y. Mantida a mesma perturbação, qual tende a postergar mais a redução de carga ou a parada?

- Referência: A X, porque esses recursos determinam quanto a unidade absorve a perturbação antes de reduzir carga ou parar.
- Respondente: A unidade X tende a postergar mais a redução de carga ou parada devido à maior capacidade de segregação, inventário intermediário, instrumentação e flexibilidade operacional.
- Juiz: Identifica corretamente a unidade X como a mais capaz de absorver a perturbação antes de reduzir carga ou parar, pelos recursos operacionais superiores.

**ec · media · correta** Durante um desvio operacional, a equipe depende de suporte remoto, não acessa a documentação atualizada e não sabe quem detém a responsabilidade técnica. Que efeito isso tende a produzir sobre a resposta e a validação de mudanças?

- Referência: Aumenta o tempo de resposta, atrasa decisões e dificulta validar mudanças diante do desvio.
- Respondente: Pode gerar atrasos, erros na implementação e dificuldades na validação, devido à falta de informações atualizadas e da clareza sobre responsabilidades técnicas, comprometendo a segurança e a eficiência da resposta ao desvio operacional.
- Juiz: A resposta reproduz o efeito essencial da referência ao apontar atrasos na resposta, dificuldade de decisão e problemas para validar mudanças.

**ec · media · parcial** Em várias paradas do mesmo sistema, o histórico mostra acréscimo recorrente de escopo no mesmo pacote e recursos de suporte maiores que o previsto. Além de explicar custos passados, que decisão sobre esse pacote esse histórico pode embasar?

- Referência: A revisão da estratégia de manutenção desse pacote.
- Respondente: Esse histórico pode embasar decisão de revisar o escopo, otimizar recursos ou renegociar contratos, ajustando planejamento e custos para futuras operações, refletindo lições aprendidas e evitando custos adicionais similares.
- Juiz: Propõe ajustes de escopo, recursos e contratos, mas não chega ao ponto central da referência, que é revisar a estratégia de manutenção do pacote.

**ec · media · parcial** Na revisão de risco, eventos anteriores mostram repetidamente desvios em separação de fluidos e medição. Como isso deve influenciar a seleção de sistemas críticos?

- Referência: Essas funções devem ser tratadas como sensíveis, servindo para formular hipóteses de falha e revisar cenários na priorização dos controles.
- Respondente: A repetição de desvios indica a necessidade de sistemas de separação e medição mais robustos, com redundância e monitoramento aprimorado, garantindo maior confiabilidade e controle adequado, mitigando riscos de falhas operacionais.
- Juiz: Percebe que separação e medição merecem maior atenção, mas não responde no sentido da referência de tratá-las como funções sensíveis para formular hipóteses de falha e revisar cenários na priorização.

**ec · media · correta** Um gestor compara a intervenção preventiva apenas com o custo imediato do reparo após a falha. Esse recorte é economicamente suficiente para decidir o controle de risco?

- Referência: Não. A análise deve incluir o efeito acumulado da indisponibilidade, das correções emergenciais e das restrições operacionais.
- Respondente: Não, o recorte considera apenas custos imediatos, ignorando custos futuros, perdas de produção e riscos ambientais, tornando-se insuficiente para uma decisão econômica completa.
- Juiz: Concorda com a referência ao dizer que o custo imediato do reparo é insuficiente e que a decisão deve considerar impactos econômicos mais amplos como perdas operacionais.

**ec · media · parcial** Em um trocador do FPSO, ataque químico progressivo reduz a espessura até surgir vazamento. Na análise de falhas, como se classificam o ataque químico e o vazamento?

- Referência: O ataque químico é o mecanismo de falha; o vazamento é o modo de falha.
- Respondente: O ataque químico é classificado como falha por corrosão ou ataque químico, e o vazamento como falha por ruptura ou fratura devido à perda de integridade estrutural.
- Juiz: Ela acerta o ataque químico como causa degradante, porém não classifica corretamente o vazamento como modo de falha.

**ec · media · incorreta** Em um FPSO, a FMEA de um sistema foi elaborada só pela manutenção, embora incluísse efeitos, causas e controles operacionais. Que requisito do método ficou sem atendimento?

- Referência: A condução por equipe multidisciplinar.
- Respondente: Incluiu-se a análise de falhas potencialmente não detectadas pela manutenção, como modo de falha e efeitos, o que é requisito do método FMEA.
- Juiz: A referência cobra o requisito de equipe multidisciplinar na FMEA, e a resposta do candidato não aborda esse ponto.

**ec · media · correta** Dois frascos receberam o mesmo desemulsificante e a mesma dosagem, mas um foi submetido a mistura mais intensa. A diferença observada pode ser usada como comparação válida do tratamento?

- Referência: Não. O bottle test exige condições controladas; mistura, temperatura, concentração do produto e tempo de observação precisam ser comparáveis.
- Respondente: Não, a diferença na mistura pode afetar a eficácia do desemulsificante, dificultando a comparação direta entre os frascos.
- Juiz: Reconhece corretamente que a comparação não é válida porque a intensidade de mistura alterou uma condição que deveria estar controlada no bottle test.

**ec · media · correta** Um produto foi o melhor na bancada, porém o ensaio não representou bem o fluido nem as condições relevantes do processo. Antes de adotá-lo no FPSO, o que deve ser feito?

- Referência: Validação operacional, porque cisalhamento, residência e composição real podem alterar o desempenho visto em bancada.
- Respondente: Realizar testes piloto sob condições reais do processo para validar o desempenho do produto antes da implementação no FPSO.
- Juiz: A resposta coincide com a referência ao pedir validação em condições reais do processo antes da adoção no FPSO.

**ec · media · correta** Uma emulsão segue estável por causa de um filme interfacial resistente. Se o aditivo desorganiza esse filme, qual mecanismo de separação passa a ser favorecido quando as gotas se tocam?

- Referência: A drenagem do filme líquido entre as gotas, favorecendo a coalescência.
- Respondente: O mecanismo de separação favorecido é a coalescência, onde as gotas se fundem devido à desorganização do filme interfacial.
- Juiz: Identifica corretamente que a desorganização do filme interfacial favorece a coalescência quando as gotas entram em contato.

**ec · media · correta** No mesmo separador, elevar a concentração do antiespumante melhora a quebra da espuma até certa faixa; acima disso, o desempenho deixa de crescer. O que isso indica sobre a relação dose-resposta?

- Referência: Que ela não é universal; acima de uma faixa útil, mais concentração não garante melhor desempenho.
- Respondente: Indica uma relação de dose-resposta com ponto de saturação, onde aumento na dose não resulta em melhoria adicional, sugerindo níveis ótimos de antiespumante.
- Juiz: Descreve corretamente a saturação da dose-resposta, equivalente à ideia de que acima de certa faixa mais antiespumante não melhora o desempenho.

**ec · media · correta** Duas formulações antiespumantes são aplicadas no mesmo fluido e na mesma dose, mas uma controla melhor a espuma. Mantidas as demais condições, o que explica essa diferença?

- Referência: Diferenças de formulação alteram o espalhamento, a penetração e a dispersão do produto na interface gás-líquido.
- Respondente: Diferenças na composição química, concentração ou a eficiência de dispersão das formulações podem explicar a melhor performance de uma antiespumante em controlar a espuma.
- Juiz: Atribui corretamente a diferença de desempenho a diferenças de formulação/composição e de dispersão na interface, compatíveis com a referência.

**ec · media · parcial** Um antiespumante controla a espuma no primeiro vaso, mas sua formulação inclui fase oleosa e emulsificantes. Mantidas as demais condições do trem de processo, que efeito colateral precisa ser avaliado nos equipamentos seguintes?

- Referência: Possível alteração do comportamento das interfaces em outros equipamentos.
- Respondente: O risco de acúmulo de emulsões e resíduos oleosos nos equipamentos subsequentes, podendo causar entupimentos, manutenção increased e dificuldades no controle de processos.
- Juiz: Reconhece um efeito colateral a jusante com emulsões, mas não destaca o ponto central da referência, que é a alteração do comportamento das interfaces nos equipamentos seguintes.

**ec · media · correta** Uma água produzida mantém gotas finas dispersas principalmente por repulsão elétrica. Que ação do coagulante tende a aumentar a aproximação entre gotas e sólidos?

- Referência: Neutralização de cargas e/ou compressão da dupla camada elétrica, aproximando gotas e sólidos.
- Respondente: O coagulante que neutraliza cargas elétricas, como o alum ou ferro, reduz a repulsão entre gotas, promovendo a agregação e aproximação dos sólidos.
- Juiz: A neutralização de cargas reduz a repulsão eletrostática e favorece a aproximação entre gotas e sólidos, em linha com a referência.

**ec · media · incorreta** Após o condicionamento químico, a corrente segue para flotação por ar dissolvido. Se os agregados ficam maiores e as interfaces menos estáveis, que efeito se espera na remoção do óleo?

- Referência: A captura por microbolhas tende a ficar mais fácil, acelerando a subida da fase oleosa.
- Respondente: A remoção do óleo pode diminuir devido ao aumento do tamanho dos aglomerados e à diminuição da estabilidade das interfaces, dificultando a separação eficaz na flotação por ar dissolvido.
- Juiz: Afirma o efeito oposto ao esperado, pois agregados maiores e interfaces menos estáveis tendem a favorecer a flotação e a remoção do óleo.

**ec · media · parcial** Em um FPSO, o corte de água aumentou e parte da produção passou a vir de outros poços, sem mudança no equipamento. O que isso implica para a dosagem ótima do tratamento da água produzida?

- Referência: Ela pode mudar; o desempenho do tratamento deve ser reavaliado e a dosagem redeterminada.
- Respondente: Aumento na proporção de água produzida pode demandar ajuste na dosagem de produtos químicos de tratamento, aumentando a quantidade para evitar problemas de corrosão e incrustação devido ao maior volume de água tratada.
- Juiz: A resposta reconhece que a dosagem pode precisar mudar, mas reduz isso a um possível aumento por maior volume e não enfatiza a reavaliação do desempenho e a redeterminação da dosagem ótima.

**ec · media · correta** Após ajustar coagulante e floculante, a remoção de óleo continuou adequada, mas subiram os sólidos suspensos do efluente e o lodo passou a desaguar pior. Que conclusão isso impõe sobre a avaliação do programa químico?

- Referência: Ela não pode se limitar ao óleo removido; o programa também está afetando o perfil do efluente e o desaguamento do lodo.
- Respondente: Indica que os químicos podem estar otimizando a remoção de óleo, mas prejudicando a eficiência na floculação e a separação de sólidos, sugerindo necessidade de ajuste na dosagem ou formulação dos aditivos químicos.
- Juiz: Reconhece que o programa químico pode manter a remoção de óleo e ao mesmo tempo piorar sólidos e lodo, exigindo avaliação além do óleo removido.

**ec · media · correta** Uma FPSO usa URS para reduzir sulfato na água de injeção, mas persiste tendência de depósito por carbonato de cálcio na planta de processo. Nesse quadro, qual papel cabe ao anti-incrustante?

- Referência: Compensar uma incrustação que a remoção de sulfato não resolve, protegendo a planta de processo.
- Respondente: O anti-incrustante inibe a formação de depósitos de carbonato de cálcio, evitando incrustações e melhorando a eficiência do sistema de água de injeção na FPSO.
- Juiz: Expressa a função essencial do anti-incrustante, que é inibir a incrustação por carbonato de cálcio não resolvida pela URS.

**ec · media · incorreta** Se o teor de oxigênio dissolvido da água aumenta e a dosagem de bissulfito permanece inalterada, qual tendência operacional deve ser esperada?

- Referência: A demanda química cresce; a dosagem pode ficar insuficiente e deixar oxigênio residual no sistema.
- Respondente: Aumentar a remoção de oxigênio dissolvido, pois o bissulfito neutraliza o oxigênio, podendo reduzir sua concentração na água.
- Juiz: A tendência esperada é insuficiência da dosagem e oxigênio residual com maior demanda química, enquanto a resposta afirmou aumento da remoção.

**ec · media · parcial** Após substituir o produto por uma solução mais diluída de bissulfito, um circuito passa a exigir verificação extra de materiais, sem mudança de serviço. Qual aspecto justifica essa checagem?

- Referência: O baixo pH da solução diluída pode torná-la corrosiva para muitos materiais.
- Respondente: A redução na concentração de bissulfito pode alterar a compatibilidade dos materiais, aumentando riscos de corrosão ou reação adversa, exigindo verificação adicional para garantir a integridade do circuito.
- Juiz: Reconhece a preocupação com compatibilidade e corrosão, mas não explicita o aspecto decisivo da referência, que é o baixo pH da solução diluída.

**ec · media · parcial** Na seleção da desoxigenação por stripping a gás em um FPSO, há gás disponível, mas sua composição é variável e a corrente gasosa de saída não tem destino seguro definido. Qual decisão técnica decorre disso?

- Referência: A rota por stripping a gás não deve ser escolhida sem confirmar disponibilidade, composição adequada e destino seguro da corrente gasosa.
- Respondente: Deve-se implementar monitoramento contínuo da composição do gás, estabelecer destinação segura para a corrente de saída, e ajustar o processo de stripping conforme necessário para garantir a conformidade e segurança operacional.
- Juiz: Menciona a necessidade de controlar composição e definir destino seguro, mas não explicita a decisão da referência de não escolher a rota por stripping sem essas confirmações.

**ec · media · correta** No circuito de água de injeção, por que avaliar só microrganismos na fase aquosa pode subestimar o problema operacional?

- Referência: Porque o problema também inclui microrganismos aderidos às superfícies internas de linhas, tanques, filtros, tubulações e poços.
- Respondente: Pois microrganismos podem aderir às superfícies, formando biofilmes, que não são detectados na fase aquosa, subestimando o problema operacional de corrosão e entupimento.
- Juiz: O candidato identifica corretamente os microrganismos aderidos às superfícies e biofilmes como parte do problema não capturada pela fase aquosa.

**ec · media · correta** Em um sistema de água de injeção, um biocida teve bom resultado contra células planctônicas em teste, mas a colonização no equipamento ocorre como biofilme aderido. Sem mudar o produto, que comportamento é mais esperado no campo?

- Referência: Desempenho insuficiente contra o biofilme, porque ele dificulta o contato e a penetração do produto.
- Respondente: Espera-se que a eficácia do biocida diminua ao longo do tempo, exigindo monitoramento contínuo e possivelmente reforço na frequência de aplicação para controlar o biofilme aderido.
- Juiz: A resposta indica desempenho reduzido do biocida frente ao biofilme aderido, que é a essência da referência.

**ec · media · correta** Dois trechos de uma linha de água de injeção têm a mesma água, o mesmo material e a mesma vazão. O trecho B possui superfície interna mais rugosa. Em qual trecho a formação de biofilme tende a ser maior?

- Referência: No trecho B, porque a rugosidade da superfície favorece a formação de biofilme em escoamento.
- Respondente: No trecho B, a maior rugosidade promove maior aderência e formação de biofilme.
- Juiz: Respondeu que o trecho B, por ser mais rugoso, favorece a aderência e a formação de biofilme, em linha com a referência.

**ec · media · parcial** Mantidas a pressão e a composição do gás, a concentração de MEG foi elevada ao valor adequado. O que acontece com a temperatura em que o sistema passa a atingir a condição de hidrato?

- Referência: Ela diminui; o sistema pode operar a temperaturas mais baixas antes de alcançar o equilíbrio de hidrato.
- Respondente: A temperatura de formação de hidratos diminui, facilitando a formação em condições de operação.
- Juiz: Acerta que a temperatura de formação de hidratos diminui com maior concentração de MEG, mas erra ao afirmar que isso facilita a formação em operação.

**ec · media · parcial** Em uma unidade de regeneração de MEG, a carga de processamento aumenta e as condições de temperatura e pressão mudam. Que dois aspectos devem ser reavaliados porque essa mudança os afeta diretamente?

- Referência: A separação e o consumo de energia.
- Respondente: Vazão do líquido regenerado e eficiência da troca de calor, pois são influenciados por alterações na carga, temperatura e pressão.
- Juiz: Cita a eficiência de troca térmica, tangenciando o consumo de energia, mas não identifica a separação e substitui um dos dois aspectos centrais da referência.

**ec · media · correta** O gás precisa reduzir CO2 em um subsistema de adoçamento, e o risco dominante não é hidrato, espuma nem corrosão por fase aquosa. Que classe de produto atende esse objetivo?

- Referência: Solvente de absorção, como alcanolamina.
- Respondente: Utilização de processos de captura de carbono, como aminas ou tecnologias de servidão de gases, para reduzir CO2 no subsistema de adoçamento.
- Juiz: Cita aminas, que são solventes de absorção usados no adoçamento para remoção de CO2, apesar da formulação genérica adicional.

**ec · media · correta** Duas estratégias mantêm a mesma meta de controlar incrustação ao longo da vida do campo: instalar URS ou seguir com inibição. Com diferenças de investimento inicial, operação, manutenção e impacto de paradas, em que comparação a escolha deve se basear?

- Referência: Em estudo de viabilidade técnico-econômica, comparando investimento inicial e custos de operação e manutenção com custos recorrentes de inibição e perdas por parada de produção.
- Respondente: A escolha deve se basear na análise custo-benefício, considerando investimento, operação, manutenção e impacto na produção ao longo do ciclo de vida do campo.
- Juiz: A resposta preserva a essência da referência ao basear a decisão em análise técnico-econômica ao longo da vida do campo, considerando CAPEX, OPEX, manutenção e impacto produtivo.

**ec · media · parcial** Um produto passará a usar a mesma linha de injeção de outro, sem troca de mangueira ou dreno entre campanhas. O que deve ser verificado antes de autorizar a sequência?

- Referência: A compatibilidade entre os químicos, inclusive com a mistura residual na linha, na mangueira ou no recipiente.
- Respondente: Verificar compatibilidade química, pressão, vazão e compatibilidade de temperatura entre os produtos para evitar contaminação ou falhas no sistema.
- Juiz: Acerta a necessidade de verificar a compatibilidade química, mas omite o ponto decisivo da compatibilidade com o residual já existente na linha, mangueira ou recipiente.

**ec · media · incorreta · ref. inválida** Em um sistema de injeção sujeito à corrosão e com regime dinâmico, que técnicas foram consideradas adequadas para acompanhar variações de corrosividade?

- Referência: Par galvânico e resistência à polarização.
- Respondente: Monitoramento contínuo de resíduos de corrosão, análise de fluidos por técnicas como espectroscopia e sensores de corrosividade em tempo real foram consideradas adequadas.
- Juiz: A resposta não cita par galvânico nem resistência à polarização, e a pergunta isolada é ambígua porque outras técnicas de monitoramento de corrosão também poderiam ser consideradas adequadas.

**ec · media · correta** Mantidos o mesmo indicador e o mesmo processo, em qual caso a lógica de controle deve ser mais conservadora contra falso negativo: ativo pouco crítico ou ativo crítico?

- Referência: No ativo crítico, porque a consequência do falso negativo pesa mais na seleção do indicador e da lógica de controle.
- Respondente: Ativo crítico, pois a falha impacta significativamente a operação, exigindo uma lógica mais conservadora para evitar falsos negativos que possam levar a falhas graves.
- Juiz: O candidato identifica corretamente que, para ativo crítico, a lógica de controle deve ser mais conservadora contra falso negativo.

**ec · media · correta** Em um meio aquoso do FPSO suscetível à corrosão ácida, o pH cai durante a operação. Que tendência de mudança na perda metálica é esperada?

- Referência: Tendência de aumento da taxa de perda metálica.
- Respondente: A perda metálica tende a aumentar à medida que o pH cai, devido à maior agressividade do meio corrosivo ácido.
- Juiz: Expressa a mesma ideia essencial de que a queda do pH em meio ácido aumenta a taxa de perda metálica.

**inventario · dificil_A · correta** Durante aumento de carga em um FPSO, um KPI de tratamento de óleo se deteriora logo após perturbação na alimentação. As medições de pressão, temperatura e nível continuam disponíveis e mostram regime transitório, sem evidência imediata de falha de instrumento. Mesmo assim, a equipe quer usar apenas o KPI para concluir que a variável controlada saiu da faixa e ajustar a malha. Qual é a conclusão técnica correta sobre essa decisão?

- Referência: É uma decisão inadequada: o KPI só indica impacto no desempenho e não representa diretamente a variável de processo; a causa deve ser confirmada pelas próprias medições e pelo contexto operacional recente.
- Respondente: Confiar unicamente no KPI durante regime transitório é arriscado; é necessário verificar medições diretas de pressão, temperatura e nível para determinar mudanças reais na variável controlada.
- Juiz: A resposta acerta ao rejeitar o uso isolado do KPI em regime transitório e exigir confirmação por medições diretas e contexto operacional.

**inventario · dificil_A · correta** Em um FPSO, o 1º trimestre teve 3 acidentes enquadrados por um mesmo critério com 120 mil horas de exposição da força de trabalho; o 2º teve 4, no mesmo intervalo trimestral e sob o mesmo critério, mas com 180 mil horas por causa de uma campanha de manutenção. Qual comparação sustenta melhor o julgamento do desempenho de segurança entre os trimestres?

- Referência: A taxa de frequência por horas-homem, não a contagem bruta; com período, critério e base de exposição compatíveis, ela dá comparação temporal mais consistente.
- Respondente: A taxa de acidentes por milhão de horas, que é (3/120.000)*1.000.000=25 e (4/180.000)*1.000.000≈22,22, indica melhor desempenho no 2º trimestre.
- Juiz: Usa corretamente uma taxa de frequência normalizada por horas-homem, em vez da contagem bruta, e conclui de forma consistente.

**inventario · dificil_A · parcial** No FPSO, um compressor A opera e o B fica em reserva fria. Em testes periódicos, o B apareceu com bateria descarregada e, numa troca real, a sequência automática não concluiu, apesar das poucas horas acumuladas no reserva. Que conclusão técnica deve orientar a leitura do KPI de disponibilidade desse arranjo?

- Referência: A reserva fria não elimina as principais fontes de indisponibilidade; ela reduz apenas certos desgastes. O KPI deve considerar também falhas latentes em espera e falhas na partida ou na comutação para o equipamento reserva.
- Respondente: A bateria do compressor B provavelmente comprometeu sua disponibilidade, destacando a necessidade de monitoramento contínuo e manutenção preventiva na reserva fria para garantir prontidão operacional.
- Juiz: Identifica falha latente na reserva fria, mas não traz a conclusão completa de que o KPI deve incluir também falhas em espera, partida e comutação, além de reconhecer que a reserva fria não elimina as principais indisponibilidades.

**inventario · dificil_A · correta** Após uma parada parcial em um FPSO, a gerência mobilizou pessoal extra para acelerar o retorno. Mesmo assim, o KPI de retorno quase não melhorou: os registros mostram horas dominantes aguardando liberação de área, chegada de sobressalente e janela logística; quando o acesso é liberado, as intervenções terminam sem fila relevante de serviços para as equipes disponíveis. O que explica tecnicamente esse resultado?

- Referência: Adicionar mantenedores traz pouco ganho: a indisponibilidade é governada por dependências externas à execução do reparo, não por insuficiência de capacidade das equipes.
- Respondente: A lentidão no retorno pode ser devido à coordenação ineficiente, atrasos na liberação de áreas, dependência de sobressalentes específicos ou problemas logísticos, que não são resolvidos apenas com mais pessoal, refletindo gargalos operacionais e de planejamento.
- Juiz: Explica adequadamente que o gargalo está em liberações, sobressalentes e logística, não na quantidade de mantenedores disponíveis.

**inventario · dificil_A · parcial** Em um FPSO, ocorre um desvio no tratamento de água produzida. A equipe de bordo reconhece rapidamente o mecanismo, já visto antes, e não há necessidade de cálculo novo nem dúvida de processo; mesmo assim, a ação demora porque os P&IDs revisados não estão disponíveis a bordo, a decisão depende de especialistas em terra e ninguém assume a validação da mudança temporária. O que explica mais provavelmente o atraso de resposta e decisão?

- Referência: Uma fragilidade de governança técnica e de gestão documental/decisória; os entraves organizacionais, e não só a complexidade do desvio, estão ampliando o tempo de resposta.
- Respondente: A ausência dos P&IDs atualizados a bordo impede acesso rápido às informações essenciais, atrasando a validação da mudança temporária na água produzida.
- Juiz: Identifica um problema documental relevante, porém não captura plenamente que o atraso decorre principalmente de fragilidade de governança técnica e de decisão.

**inventario · dificil_A · parcial** Num FPSO, um compressor de serviço essencial mostra degradação, mas ainda sustenta a carga mínima. A probabilidade estimada de falha é semelhante à de outro caso antes adiado; desta vez, porém, o sobressalente está em terra, o especialista só embarca na próxima janela e a mobilização depende de tempo bom. Na decisão entre intervir agora, postergar ou aceitar operação degradada, que aspecto técnico impede basear a escolha só na chance de falha?

- Referência: Deve pesar a capacidade de recompor a função: prazo de recuperação e recursos/logística disponíveis para executar o reparo, não apenas a probabilidade de falha.
- Respondente: A capacidade de manutenção preventiva ou corretiva, que pode alterar a probabilidade de falha a longo prazo, impede decidir apenas pela chance de falha atual, pois outros fatores como impacto operacional e segurança também influenciam.
- Juiz: O candidato toca em capacidade de manutenção e outros fatores, mas não explicita o ponto decisivo da referência: a capacidade de recomposição da função via prazo de recuperação e logística/recursos de reparo.

**inventario · dificil_B · correta** Num FPSO, após restrição temporária na exportação de gás, a carga da planta é reduzida por algumas horas. O painel gerencial destaca queda no volume diário tratado, e esse mesmo número passa a ser usado na sala de controle para alegar perda de eficiência. Sem normalização explícita e com histórico recente indicando regime transiente, essa leitura justifica abrir ação corretiva imediata por degradação intrínseca do processo?

- Referência: Não. Para uso operacional, o indicador deve ser adequado à decisão em tempo real, normalizado por base coerente e lido com contexto e histórico recente; a queda absoluta pode refletir apenas a redução temporária de carga, não perda intrínseca de desempenho.
- Respondente: Não, a redução é temporária devido à restrição, não indica degradação intrínseca. A normalização e análise do regime transiente são essenciais antes de ações corretivas.
- Juiz: Reproduz corretamente que a queda absoluta em regime transiente não justifica ação corretiva imediata sem normalização e análise contextual.

**inventario · dificil_B · correta** Na FMEA de um FPSO, dois modos de falha receberam o mesmo NPR. Um compromete uma barreira associada a função já classificada como crítica naquela unidade e sua recuperação exigiria parada longa; o outro afeta função menos sensível, com retorno rápido. Ao definir a atualização dos controles, o empate no NPR basta para tratá-los como equivalentes?

- Referência: Não. NPR igual não significa prioridade igual; a decisão deve considerar a função crítica envolvida, o tempo de recuperação e o contexto da unidade, usando o índice apenas como triagem inicial.
- Respondente: Não, o empate no NPR não basta; deve-se considerar o impacto na criticidade e na recuperação, tratando os modos de falha de maneira diferenciada para priorizar ações específicas de controle.
- Juiz: Concorda com a referência ao afirmar que NPR igual não implica mesma prioridade e que criticidade e recuperação devem orientar a decisão.

**inventario · dificil_B · correta** Numa parada programada da FPSO, o efetivo embarcado aumentou fortemente e as horas-homem expostas ficaram muito acima do padrão. No período, houve mais acidentes sem afastamento em número absoluto que nos meses anteriores, com os casos enquadrados pelo mesmo critério corporativo. A gerência quer concluir piora do desempenho apenas por essa contagem. Como a comparação entre períodos deve ser feita tecnicamente?

- Referência: Não pela contagem bruta; deve-se comparar a taxa de frequência, com os casos definidos no numerador e as horas-homem no denominador, interpretando o resultado no contexto da maior exposição e do histórico do período.
- Respondente: A comparação deve considerar a taxa de acidentes por horas-homem expostas, não apenas o número absoluto, para avaliar o desempenho real, ajustando pelo incremento de efetivo e horas trabalhadas.
- Juiz: A resposta corresponde à referência ao exigir comparação por taxa de frequência ajustada por horas-homem, e não por contagem bruta.

**inventario · dificil_B · incorreta** Num FPSO em fim de platô, o corte de água sobe e a vazão total sustentada passa a depender da capacidade de separar, tratar e reinjetar ou descartar a água produzida. Mesmo assim, o KPI principal de capacidade continua expresso só em barris de óleo. Para definir a meta e diagnosticar a perda dominante, qual lógica de normalização é a mais adequada?

- Referência: Usar um denominador coerente com a função de manejo da fase aquosa, não apenas com o óleo, para que o KPI reflita o gargalo que pode estar restringindo a vazão total da unidade.
- Respondente: Normalizar o KPI principal em relação à vazão de óleo produzida, considerando a taxa de água separada e tratada, para identificar perdas específicas e avaliar a eficiência de separação e tratamento em relação à produção de óleo.
- Juiz: A referência exige normalizar o KPI por uma base coerente com o manejo da água, e o candidato manteve a lógica centrada na vazão de óleo.

**inventario · dificil_B · correta** No painel em tempo real do FPSO, um ranking por horas em serviço põe em último um trem de compressão que mais desarma por intertravamento. Esses desligamentos automáticos evitam escalada de anomalias. A gerência quer reduzir testes das proteções e mexer nos ajustes apenas para subir o ranking. Esse KPI, visto sozinho, é tecnicamente adequado para sustentar essa decisão?

- Referência: Não. O desarme pode ser atuação correta de proteção, inclusive em arquitetura que prioriza estado seguro à continuidade; a métrica só sustenta a decisão se for coerente com esse objetivo e a disponibilidade for lida com a segurança.
- Respondente: Não, pois o ranking por horas em serviço não reflete a eficácia das proteções nem prioriza a segurança; ajustes para melhorar o ranking podem comprometer a integridade operacional.
- Juiz: Rejeita corretamente o uso isolado do KPI e aponta que mexer em proteções apenas para subir ranking pode comprometer a segurança.

**inventario · dificil_B · correta** Em um FPSO operando com especificações apertadas, a medição de nível de interface de um separador primário ficou indisponível. O painel em tempo real continua mostrando estáveis os KPIs agregados de produção e qualidade global, que não medem diretamente essa variável, e a equipe quer seguir sem reavaliação. Essa conclusão é tecnicamente válida?

- Referência: Não. KPI agregado estável resume desempenho, mas não substitui a medição essencial; sem ela, cai a capacidade de detectar e corrigir desvios e o risco do processo aumenta. O painel em tempo real só ajuda se a métrica sustentar a decisão sem encobrir essa ausência.
- Respondente: Não, não é tecnicamente válido confiar em KPIs globais para monitorar a interface do separador sem uma medição direta, especialmente em condições operacionais críticas.
- Juiz: A resposta coincide com a referência ao afirmar que KPIs agregados não substituem a medição essencial da interface e não sustentam sozinhos a decisão operacional.

**inventario · dificil_A · correta** Após a troca do pacote químico de produção e o aumento de finos no fluido, um separador passou a manter espuma por longos períodos, com maior arraste de líquido na saída de gás. Vazão, pressão, internos do vaso e regime operacional permaneceram essencialmente inalterados. Qual mecanismo explica melhor essa persistência?

- Referência: A persistência decorre principalmente da estabilização do filme líquido por espécies de superfície ativas e impurezas, que retardam a drenagem e a ruptura da espuma.
- Respondente: A formação de espuma devido ao aumento de agentes espumantes ou estabilizadores no fluido, levando à persistência da espuma, ao mesmo tempo em que o maior arraste de líquido resulta da alta estabilidade dessa espuma, mesmo com constantes operacionais.
- Juiz: Capta o mecanismo essencial de persistência da espuma por aumento de espécies estabilizantes/superficialmente ativas, mesmo sem detalhar a drenagem do filme líquido.

**inventario · dificil_A · incorreta** Em um FPSO com injeção de água do mar, um poço produtor começa a perder produtividade após o breakthrough da água injetada. As análises mostram sulfato na água que retorna pelo poço, e esse reservatório tem água de formação rica em bário; a URS e suas membranas não apresentam sinais anormais. Qual depósito se torna o diagnóstico mais provável nesse poço?

- Referência: Incrustação por BaSO4 (barita), formada pela mistura da água do mar com sulfato e da água de formação com bário.
- Respondente: O depósito mais provável é de bicarbonato de bário (bariobicarbonato), formado devido à troca iônica entre o bário da água de formação e o bicarbonato na água de injeção, levando ao precipitado que reduz a produtividade do poço.
- Juiz: A referência aponta incrustação de BaSO4 por mistura de sulfato com bário, enquanto a resposta do candidato identifica um depósito diferente e incompatível com o caso.

**inventario · dificil_A · parcial** Após substituir o produto do programa microbiológico da água de injeção por outro que controlou o biofilme nas linhas, o FPSO passou a apresentar mais espuma no trem de separação, piora no tratamento da água produzida e ensaio ecotoxicológico mais crítico no descarte. Vazões, composição do fluido, pressões e ajustes dos equipamentos permaneceram estáveis, sem perturbações mecânicas relevantes. Que característica do novo tratamento químico é a causa técnica mais provável?

- Referência: A formulação do novo biocida, especialmente se ele contiver surfactantes; alguns produtos eficazes contra biofilme podem piorar a separação óleo-água, gerar espuma e aumentar a toxicidade aquática.
- Respondente: A introdução de um biocida com maior potencial de formação de espuma ou impacto na compatibilidade do sistema pode ser a causa, devido à alteração na composição química que afeta a estabilidade da espuma e o tratamento da água.
- Juiz: Aponta a composição química do novo biocida como provável causa, mas não traz com precisão o ponto central da formulação com surfactantes e seu vínculo também com a piora ecotoxicológica.

**inventario · dificil_A · incorreta** Em uma FPSO, a linha de água de injeção mantém contagens microbiológicas altas a jusante, apesar da dosagem correta de biocida. A concentração ativa e a compatibilidade com o processo já foram confirmadas, sem problemas de espuma ou separação, e há evidência de depósitos aderidos em um trecho que permite passagem de raspador. Qual intervenção tende a aumentar a efetividade do tratamento químico?

- Referência: Remover mecanicamente os depósitos nesse trecho, pois isso tende a reduzir a barreira física à ação do biocida.
- Respondente: Adição de um biocida de amplo espectro ou aumento da frequência de dosagem para reforçar o controle microbiológico, considerando os depósitos aderidos que podem proteger os micro-organismos.
- Juiz: A referência pede remoção mecânica dos depósitos para expor os microrganismos ao biocida, enquanto o candidato propõe apenas intensificar o tratamento químico.

**inventario · dificil_A · incorreta** Num FPSO, um tanque de água produzida ficou isolado, fechado e com baixa renovação por semanas. Ao ser aberto para inspeção, a atmosfera interna está tóxica e há ataque corrosivo, embora esse desvio não aparecesse quando a mesma corrente era apenas transferida sem retenção. Qual mecanismo mais provável explica o surgimento desse quadro no tanque?

- Referência: Proliferação de bactérias redutoras de sulfato no volume estagnado, com geração de H2S.
- Respondente: Acúmulo de gases dissolvidos na água produzida, que ao serem liberados ao abrir a estação, causam atmosfera tóxica e corrosão devido à liberação de compostos corrosivos como H2S ou CO2.
- Juiz: Atribui o quadro à liberação de gases dissolvidos, enquanto a referência aponta geração de H2S por proliferação de bactérias redutoras de sulfato em volume estagnado.

**inventario · dificil_A · incorreta** Em um FPSO, após reforçar o tratamento oxidante na água do mar tratada, o residual medido continuou na faixa esperada e a contagem bacteriana caiu, porém cupons indicaram mais corrosão e houve maior tendência a depósitos. As vazões e o preparo do inibidor de corrosão e do dispersante foram verificados sem desvio. Qual mecanismo explica melhor essa perda de proteção?

- Referência: Excesso de oxidante degradando o inibidor de corrosão e o dispersante; por isso o residual oxidante isolado parece aceitável, mas a proteção global diminui.
- Respondente: Possível mecanismo: formação de resíduos solúveis ou precipitados devido a alterações químicas na água, que reduzem a eficácia do inibidor e dispersante, levando ao aumento da corrosão e deposição apesar da concentração adequada dos tratamentos.
- Juiz: A resposta não identifica o mecanismo central da referência, que é a degradação do inibidor e do dispersante por excesso de oxidante.

**inventario · dificil_B · parcial** Após uma parada curta, um trecho com água livre a jusante do manifold do FPSO apresentou sinais compatíveis com hidrato no retorno à produção. A bomba de MEG permaneceu na vazão nominal prevista, mas o único analisador fica antes do ponto em que a mistura se completa e há indício de escoamento segregado. Qual conclusão técnica deve ser tirada sobre a proteção nesse trecho?

- Referência: Vazão nominal não comprova proteção: ela depende da concentração efetiva de MEG na água livre; má mistura, diluição ou distribuição desigual podem deixar regiões sem proteção, e a checagem deve usar medição representativa a jusante da mistura.
- Respondente: A proteção deve estar inibida ou inoperante, pois o analisador pré-mistura pode não detectar hidratos na fase segregada. Recomenda-se verificar sensores downstream e ajustar o sistema de proteção para detectar hidratos após a mistura.
- Juiz: Acerta ao questionar a representatividade da medição antes da mistura e pedir verificação a jusante, mas erra ao concluir que a proteção já está inoperante e não destaca que o critério é a concentração efetiva de MEG na água livre.

**inventario · dificil_B · parcial** Após previsão de maior risco de hidrato na linha, a operação eleva a concentração de MEG na fase aquosa. A água produzida contém sais dissolvidos e o circuito de recuperação/regeneração, sem mudança relevante de carga ou falha mecânica, passa dias depois a perder troca térmica, aumentar a perda de carga e exigir limpezas frequentes. O que o programa químico deixou de equilibrar?

- Referência: Deixou de equilibrar a proteção contra hidratos com o controle de sais na recuperação; em certas composições, mais MEG aumenta a margem anti-hidrato, mas favorece precipitados que causam incrustação, restrição hidráulica e instabilidade.
- Respondente: O programa químico não conseguiu manter o controle da concentração de MEG e dos sais dissolvidos, levando à formação de hidratos e acúmulo de sais, o que compromete a troca térmica e aumenta perdas de carga na recuperação/regeneração.
- Juiz: A resposta menciona MEG e sais, mas erra ao atribuir o problema à formação de hidratos em vez de ao desequilíbrio entre proteção anti-hidrato e controle de sais na recuperação.

**inventario · dificil_B · correta** Na linha de água de injeção de um FPSO, sulfeto e contagens microbiológicas seguem elevados após sucessivos ajustes do biocida; concentração ativa e tempo de contato na fase aquosa foram validados. Inspeções indicam depósitos aderidos e biofilme, e o trecho permite circulação de ferramentas internas na próxima parada. Qual decisão técnica deve ser tomada para recuperar a efetividade do controle microbiológico?

- Referência: Apenas rever o biocida não basta; deve-se integrar pigging para remover biofilme e depósitos, porque a adesão protege a massa microbiana e a limpeza tende a reduzir a barreira física ao tratamento químico.
- Respondente: Realizar limpeza mecânica ou químicas aprofundadas para remover biofilme antes de ajustar novamente a dosagem de biocida, garantindo melhor penetração e ação.
- Juiz: A resposta reconhece que só ajustar biocida não basta e que é necessário remover biofilme e depósitos por limpeza mecânica, em linha com a lógica técnica do pigging citado na referência.

**inventario · dificil_B · parcial** Em uma linha de água de injeção de um FPSO, NMP/PCR para microrganismos vieram positivos no mesmo período em que surgiram pites internos. Há sulfeto na água, depósitos aderidos com indício de biofilme, residual de biocida oscilante e o material da linha é suscetível ao mecanismo observado. Parte da equipe quer concluir a causa só pelo resultado microbiológico; outra quer tratá-lo como irrelevante porque o método não mede atividade. Qual conclusão técnica deve prevalecer?

- Referência: O positivo microbiológico, sozinho, não prova nem invalida a causa; o diagnóstico deve integrar esse dado com sulfeto, depósitos/biofilme, química da água, corrosão localizada, residual de biocida e suscetibilidade do material.
- Respondente: A presença de biofilme, sulfeto e depósitos indica atividade microbiológica significativa, portanto, a culpa não deve ser atribuída apenas ao método de detecção; o foco deve ser na mitigação e controle microbiológico.
- Juiz: Reconhece indícios como biofilme, sulfeto e depósitos, porém não explicita que o resultado microbiológico isolado nem prova nem descarta a causa e que o diagnóstico deve integrar todos os evidentes fatores citados.

**inventario · dificil_B · parcial** Em um FPSO, após entrada de novo agrupamento de poços e revisão do programa químico de produção, o TOG da água tratada subiu de forma sustentada. Vazão, pressão e configuração da flotação seguem na faixa usual, e a injeção de coagulante/floculante está sem falhas de bomba ou calibração. Qual diagnóstico técnico deve orientar a reavaliação do tratamento, usando o TOG como principal referência?

- Referência: A dosagem ótima do tratamento pode ter se deslocado pela nova mistura de águas e por resíduos de químicos de produção, que passam a consumir coagulante e/ou alterar a interação gota-bolha; a confirmação deve vir da resposta do TOG da água tratada.
- Respondente: Possível aumento de sólidos em suspensão ou formação de sludge na água tratada, indicando necessidade de revisar dosagem de química, fluxo de alimentação ou condições de flotação para otimizar a remoção de sólidos e reduzir o TOG.
- Juiz: O candidato acerta ao sugerir reavaliar a química, mas não traz o diagnóstico central da referência sobre deslocamento da dosagem ótima pela nova mistura de águas e resíduos de químicos de produção afetando a interação gota-bolha.

**inventario · dificil_B · parcial** Num FPSO com área e peso muito limitados e pouca disponibilidade de utilidades, a água de injeção deve sair com 20 ppb de O2 dissolvido. Propõe-se usar membranas para cortar consumo químico com base em um piloto e em dados de outro campo, porém com água do mar, vazão e arranjo offshore diferentes. Qual deve ser o critério técnico para escolher a rota de desoxigenação?

- Referência: A escolha deve partir da meta de oxigênio residual e das restrições do FPSO; membranas podem reduzir o sequestrante, mas só se seu desempenho for comprovado nas condições reais de água, vazão, utilidades e configuração do sistema.
- Respondente: O critério deve ser a eficiência na remoção de O2 até 20 ppb, considerando compatibilidade com água do mar, redução de consumo químico, peso, espaço disponível, bem como confiabilidade e capacidade de operar com as condições específicas do campo, priorizando tecnologias de membranas de alto desempenho.
- Juiz: A resposta considera meta de O2 e restrições do FPSO, mas perde o ponto decisivo de que membranas só devem ser escolhidas se comprovadas nas condições reais, além de já as priorizar.

**inventario · facil · correta** Na operação de um FPSO, que tipo de métrica serve para avaliar a eficiência e o desempenho dos processos industriais?

- Referência: KPIs, ou indicadores-chave de desempenho.
- Respondente: Indicadores de desempenho como o Overall Equipment Effectiveness (OEE) são utilizados para avaliar a eficiência e desempenho dos processos industriais em FPSOs.
- Juiz: Indicadores de desempenho, como o OEE citado, são exemplos de KPIs usados para avaliar eficiência e desempenho.

**inventario · facil · correta** Qual é a função básica de um indicador ambiental na gestão da organização?

- Referência: Fornecer uma expressão específica que informe o desempenho ambiental da organização.
- Respondente: Monitorar e avaliar o impacto ambiental das atividades, garantindo conformidade legal e promovendo melhorias sustentáveis na gestão ambiental da organização.
- Juiz: Embora mais ampla, a resposta mantém a função básica de um indicador ambiental de informar e avaliar o desempenho ambiental da organização.

**inventario · facil · incorreta** Em um sistema do FPSO, disponibilidade, confiabilidade e mantenabilidade são atributos centrais de qual propriedade de desempenho?

- Referência: Dependabilidade.
- Respondente: Desempenho operacional
- Juiz: Disponibilidade, confiabilidade e mantenabilidade são atributos clássicos de dependabilidade, não de um conceito genérico de desempenho operacional.

**inventario · facil · incorreta** Na dependabilidade, qual atributo indica a chance de um sistema estar em operação quando observado?

- Referência: Disponibilidade.
- Respondente: Confiabilidade
- Juiz: Confiabilidade não é a chance de o sistema estar operando no instante observado; esse atributo é disponibilidade.

**inventario · facil · correta** Qual KPI de ativos tende a aumentar com maior MTBF e a diminuir com maior MTTR?

- Referência: Disponibilidade.
- Respondente: O KPI é a disponibilidade operacional (Availability), que aumenta com maior MTBF e diminui com maior MTTR.
- Juiz: Identifica corretamente a disponibilidade como o KPI que aumenta com maior MTBF e diminui com maior MTTR.

**inventario · facil · correta** Que dinâmica básica determina a disponibilidade em sistemas reparáveis?

- Referência: A alternância entre períodos operacionais e períodos indisponíveis por falha ou reparo.
- Respondente: A dinâmica básica que determina a disponibilidade em sistemas reparáveis é dada pela equação de disponibilidade, que combina as taxas de falha e reparo, geralmente expressa como uma função de taxa de falha (λ) e taxa de reparo (μ).
- Juiz: Embora use a formulação por taxas de falha e reparo, relaciona corretamente a disponibilidade à dinâmica de falha e reparo do sistema.

**inventario · facil · correta** Que objetivo técnico têm caminhos, equipamentos ou funções adicionais em um sistema quando parte do arranjo falha?

- Referência: Manter o serviço apesar da falha em parte do arranjo.
- Respondente: Garantir continuidade operacional, isolamento de falhas, manutenção e segurança do sistema, minimizando impactos e restabelecendo funções críticas rapidamente.
- Juiz: A resposta expressa a mesma ideia central da referência: manter a continuidade do serviço/operação apesar da falha em parte do arranjo.

**inventario · facil · parcial** Na gestão de uma unidade offshore, para que servem análises RAM ou RAMS?

- Referência: Para apoiar decisões de operação, fabricação, projeto e manutenção.
- Respondente: Análises RAM ou RAMS avaliam confiabilidade, disponibilidade e manutenção de sistemas para garantir segurança, desempenho e minimização de riscos na operação offshore.
- Juiz: Descreve o escopo da análise RAM/RAMS, mas não traz o ponto central da referência de apoiar decisões de operação, fabricação, projeto e manutenção.

**inventario · facil · incorreta** Que propriedade indica a chance de recolocar um sistema parado em operação nas condições e no tempo previstos, com recursos e procedimento prescritos?

- Referência: Mantenabilidade.
- Respondente: A propriedade é a confiabilidade do sistema.
- Juiz: Confunde mantenabilidade com confiabilidade, sendo mantenabilidade a propriedade de recolocar o sistema em operação no tempo e condições previstos.

**inventario · facil · correta** Qual é a função de uma barreira na gestão de risco operacional de um FPSO?

- Referência: Impedir ou mitigar acidentes, seja por meio de mecanismo físico, seja por procedimento administrativo.
- Respondente: A barreira identifica e mitiga riscos operacionais, prevenindo acidentes e falhas, garantindo segurança, integridade do equipamento e proteção ambiental no FPSO.
- Juiz: Atribui à barreira a função essencial de prevenir ou mitigar acidentes e reduzir riscos operacionais no FPSO.

**inventario · facil · correta** Qual conceito avalia se um item mantém a função requerida por um período nas condições previstas, em vez de apenas estar pronto quando solicitado?

- Referência: Confiabilidade.
- Respondente: Conceito de Confiabilidade
- Juiz: A resposta do candidato corresponde diretamente ao conceito de confiabilidade indicado na referência.

**inventario · facil · incorreta** Na análise de falhas, se o modo descreve a manifestação da perda de função, qual conceito descreve o processo que a produz?

- Referência: Mecanismo de falha.
- Respondente: O modo de falha descreve a manifestação, enquanto o efeito de falha ou causa de falha descreve o processo que a produz.
- Juiz: Substitui o conceito correto de mecanismo de falha por efeito ou causa de falha, que não são equivalentes.

**inventario · facil · parcial** Em análise de falhas, qual aspecto o modo de falha descreve?

- Referência: Descreve como a perda de função se apresenta no equipamento, sistema ou processo.
- Respondente: O modo de falha descreve a maneira específica como uma falha ocorre, indicando o processo ou evento que causa a falha.
- Juiz: Acerta ao falar da forma específica como a falha se apresenta, mas erra ao associar modo de falha ao processo ou evento causador, que remete mais à causa ou mecanismo.

**inventario · facil · incorreta · ref. inválida** Que aspectos do sistema influenciam a estabilidade de uma emulsão na produção?

- Referência: A composição do petróleo, da salmoura e do filme interfacial.
- Respondente: Viscosidade, razão de fases, pH, agitação, aditivos e temperatura influenciam a estabilidade da emulsão na produção de óleo e gás.
- Juiz: O candidato traz fatores reais de estabilidade de emulsões, mas não a composição do petróleo, da salmoura e do filme interfacial da referência, e a pergunta é ampla demais para ter resposta única.

**inventario · facil · parcial** Na avaliação de um desemulsificante, que aspectos além do volume separado precisam entrar no julgamento do desempenho?

- Referência: A cinética da separação e a qualidade das fases obtidas.
- Respondente: Além do volume separado, avalia-se a velocidade de emulsão, estabilidade do efeito, compatibilidade com fluidos e impacto na viscosidade do sistema.
- Juiz: Menciona um aspecto próximo da cinética de separação, mas não traz claramente a qualidade das fases obtidas, que é parte essencial da referência.

**inventario · facil · parcial** Na escolha de um produto para controlar espuma no processamento de óleo e gás, que elementos da composição do produto devem ser avaliados?

- Referência: Princípio ativo, concentração, veículo e coadjuvantes da formulação.
- Respondente: Devem ser avaliados seus agentes antiespumantes, capacidade de redução de tensão superficial, compatibilidade com o sistema, estabilidade térmica e resistência à decomposição química.
- Juiz: Cita o agente antiespumante, mas substitui os elementos de composição da formulação por critérios gerais de desempenho e compatibilidade.

**inventario · facil · parcial** Na água produzida, quando as gotas de óleo dispersas se mantêm estáveis no meio aquoso, qual etapa passa a ter menor eficiência?

- Referência: A separação gravitacional.
- Respondente: A separação do óleo da água se reduz de eficiência, dificultando a remoção do óleo disperso na água produzida.
- Juiz: Indica corretamente perda de eficiência na separação óleo-água, mas não identifica de forma específica a separação gravitacional citada na referência.

**inventario · facil · incorreta** Qual é a finalidade principal da URS/SRU no tratamento da água do mar antes da injeção no reservatório?

- Referência: Reduzir seletivamente a concentração de sulfato na água de injeção.
- Respondente: Remover sólidos, sedimentos, cloretos e matéria orgânica para evitar corrosão, prevenir incrustações e proteger a integridade dos equipamentos e o reservatório.
- Juiz: Descreve remoção geral de contaminantes, mas a finalidade principal da URS/SRU é a redução seletiva da concentração de sulfato na água de injeção.

**inventario · facil · parcial** Na escolha entre instalar uma URS e usar inibição química em uma plataforma, qual critério deve orientar a decisão?

- Referência: A viabilidade técnico-econômica, comparando CAPEX, operação e manutenção da URS com o custo da inibição ao longo da vida do campo, inclusive perdas por paradas de produção.
- Respondente: A decisão deve considerar a condição do sistema, custos, impacto ambiental, facilidade de manutenção e requisitos regulatórios, balanceando segurança e eficiência operacional.
- Juiz: Cita custos e manutenção, mas não apresenta como critério central a comparação de viabilidade técnico-econômica ao longo da vida do campo entre URS e inibição química.

**inventario · facil · correta** Qual mecanismo remove o oxigênio dissolvido na desaeração por membranas, com água no exterior das fibras ocas e gás de arraste ou vácuo no interior?

- Referência: A diferença de potencial de transferência de massa entre a água e o lado gasoso através da membrana.
- Respondente: O vácuo no interior das fibras ocasiona a remoção do oxigênio dissolvido, ao criar uma pressão que favorece a difusão do oxigênio da água para o gás de arraste através da membrana.
- Juiz: A resposta descreve a difusão do oxigênio através da membrana por um gradiente de pressão/transferência de massa entre a água e o lado gasoso, que é a essência da referência.

**inventario · facil · correta** Qual é a função do bissulfito de sódio no condicionamento de água quando há oxigênio dissolvido?

- Referência: Remover o oxigênio dissolvido por reação química, atuando como sequestrante de oxigênio.
- Respondente: O bissulfito de sódio atua como redutor, neutralizando o oxigênio dissolvido na água, prevenindo corrosão e formação de incrustações nas instalações de petróleo e gás.
- Juiz: Descreve corretamente o bissulfito de sódio como sequestrante químico de oxigênio dissolvido.

**inventario · facil · correta** Na água do mar destinada à injeção, qual efeito do oxigênio dissolvido sobre materiais metálicos e sobre a formação de partículas?

- Referência: Favorece a corrosão dos materiais metálicos e pode intensificar efeitos oxidativos associados à formação de partículas.
- Respondente: O oxigênio dissolvido promove corrosão em metais e favorece a formação de partículas como óxidos, aumentando a risco de incrustações e redução da vida útil dos equipamentos.
- Juiz: Reproduz o essencial de que o oxigênio dissolvido acelera a corrosão metálica e favorece a formação de partículas oxidativas.

**inventario · facil · correta** Na gestão microbiológica de sistemas de água de injeção e outros circuitos de óleo e gás, qual é a função dos biocidas?

- Referência: Matar microrganismos ou inibir seu crescimento.
- Respondente: Os biocidas controlam o crescimento microbiano, prevenindo corrosão, entupimentos e contaminações em sistemas de água de injeção e circuitos de óleo e gás.
- Juiz: Controlar o crescimento microbiano equivale essencialmente a matar ou inibir microrganismos, como diz a referência.

**inventario · facil · incorreta · ref. inválida** Que produto químico é usado na produção de gás natural para inibir a formação de hidratos, inclusive por injeção na cabeça do poço?

- Referência: Monoetilenoglicol (MEG).
- Respondente: O inibidor comum é o aguardente de polietilenoglicol (PEG) ou compostos de amina, como o metilglicol ou dietilenoglicol, injetados na cabeça do poço para prevenir a formação de hidratos de metano.
- Juiz: A referência aponta MEG, mas a pergunta admite outros inibidores igualmente corretos, como metanol; ainda assim o candidato não deu a resposta de referência.

**inventario · facil · parcial · ref. inválida** Na definição do arranjo de armazenamento e manuseio de químicos offshore, que fatores devem orientar a escolha além da operação nominal?

- Referência: A função do químico, o fluido com que ele interage e as consequências plausíveis de falha.
- Respondente: Fatores ambientais, compatibilidade química, segurança, acessibilidade, tratamento de eventual vazamento, resistência às condições offshore, e requisitos regulatórios.
- Juiz: A resposta só coincide parcialmente com a referência por trazer critérios gerais de segurança e compatibilidade sem citar explicitamente função do químico, fluido interagente e consequências de falha; além disso, a pergunta é aberta e admite outras respostas igualmente corretas.

**inventario · facil · incorreta** Para acompanhar a condição efetivamente aplicada ao equipamento após a adição de um químico, em que região a medição tende a ser mais representativa?

- Referência: A jusante do misturador ou do ponto de injeção, desde que o ponto seja representativo do escoamento.
- Respondente: Na região de fluxo turbulento próxima ao equipamento, onde as medições de condição são mais rápidas e precisas.
- Juiz: Foca em turbulência e proximidade do equipamento, mas não identifica o ponto essencial a jusante da injeção ou mistura e representativo do escoamento.

**inventario · media · parcial** Em uma unidade de processo do topside de um FPSO, a equipe acompanha KPIs junto com variáveis de processo, histórico recente e contexto operacional. Se um indicador se desvia após uma mudança de carga, que papel técnico essa metodologia cumpre nesse evento?

- Referência: Ela permite detectar o desvio, indicar quais variáveis podem ter sido perturbadas e apoiar o diagnóstico das causas prováveis, sem fechar sozinha a causa.
- Respondente: A metodologia auxilia na detecção precoce e na análise de desvios, permitindo ajustes oportunos para manter a operação segura, eficiente e dentro das especificações, facilitando tomada de decisão baseada em dados.
- Juiz: Acerta que a metodologia detecta e ajuda a analisar o desvio, mas fica genérica e não explicita o vínculo com variáveis perturbadas e diagnóstico provável sem fechar a causa sozinha.

**inventario · media · parcial · ref. inválida** Nos topsides de um FPSO, o desempenho global muda com interações entre separação, tratamento de óleo, água, gás, utilidades e malhas de controle. Que abordagem de acompanhamento operacional tende a ser mais útil para detectar desvios e apoiar o diagnóstico?

- Referência: Uma lógica de monitoramento por indicadores de desempenho (KPIs), integrada ao contexto do processo e às interações entre os subsistemas.
- Respondente: Monitoramento em tempo real com sistemas integrados de prognóstico e análise de dados, incluindo algoritmos de inteligência artificial, permite detectar desvios e apoiar o diagnóstico eficiente nos topsides de FPSO.
- Juiz: Propõe monitoramento integrado útil para detectar desvios, mas não traz a lógica centrada em KPIs com contexto e interações, e a pergunta admite outras abordagens igualmente corretas além da referência.

**inventario · media · correta** Num FPSO, dois meses tiveram a mesma quantidade de acidentes registráveis, mas o segundo teve muito mais horas de trabalho embarcado. Para evitar que a taxa reflita só a variação de atividade, o que o denominador desse indicador deve representar?

- Referência: A base de referência ou exposição do período, coerente com o fenômeno observado; é ela que define o que a taxa realmente compara.
- Respondente: O denominador deve representar as horas-homem ou horas de exposição embarecada, para refletir a intensidade do risco na atividade.
- Juiz: Horas-homem ou horas de exposição representam adequadamente a base de referência do período, conforme a lógica da taxa citada na referência.

**inventario · media · incorreta** Num FPSO, a equipe de sustentabilidade acompanha volume de efluentes lançados, reuso de água e geração de resíduos; paralelamente, monitora a qualidade da água no entorno da unidade. Como se classifica cada conjunto de indicadores?

- Referência: O primeiro conjunto é de desempenho ambiental; o segundo é de condições ambientais.
- Respondente: Efluentes, resíduos e reuso de água são indicadores de gestão ambiental; a qualidade da água ao entorno é um indicador de impacto ambiental.
- Juiz: Troca as classes da referência, pois o primeiro conjunto é de desempenho ambiental e o segundo de condições ambientais, não de gestão e impacto ambiental.

**inventario · media · parcial** Em um FPSO, um trem de compressão reserva fica em standby frio, só entra por partida automática e compartilha utilidades e intertravamentos com o ativo. Se o KPI de disponibilidade for calculado como se os dois trens fossem independentes, como tende a ficar a estimativa do ganho dessa duplicação?

- Referência: Tende a ficar superestimada, porque o efeito da duplicação depende da lógica funcional, da forma de acionamento do reserva e das dependências entre subsistemas.
- Respondente: A estimativa do ganho tende a ser otimista, pois a disponibilidade conjunta seria maior do que a prevista considerando trens independentes, devido ao compartilhamento de utilidades e intertravamentos que podem afetar a confiabilidade.
- Juiz: A resposta acerta ao dizer que o ganho fica otimista/superestimado, mas se contradiz ao afirmar que a disponibilidade conjunta seria maior do que a prevista para trens independentes.

**inventario · media · parcial** Em um FPSO, as paradas são registradas sem horário confiável de falha e sem confirmação consistente do retorno à operação. Ao calcular disponibilidade observada e confiabilidade dos equipamentos, qual efeito se espera na avaliação?

- Referência: A avaliação perde precisão e confiança analítica, porque registros incompletos de falha e de retorno à operação distorcem os indicadores.
- Respondente: A disponibilidade observada e confiabilidade serão subestimadas devido à falta de horários precisos e confirmação do retorno, levando a uma avaliação mais conservadora dos equipamentos.
- Juiz: Reconhece impacto negativo nos indicadores, porém a referência aponta perda de precisão e confiabilidade analítica sem afirmar necessariamente subestimação.

**inventario · media · correta** Em um FPSO, as paradas de equipamentos são registradas por operação, manutenção e inspeção em planilhas separadas, sem vínculo claro entre evento, mecanismo e intervenção. A equipe quer identificar causas recorrentes e definir onde agir primeiro. Que mudança no processo de dados é necessária?

- Referência: É necessário planejar uma coleta padronizada e integrada, com registros de falha, mecanismo e manutenção compartilhados entre áreas, para separar causas e priorizar ações corretivas.
- Respondente: Implementar um sistema integrado de registro de eventos com link entre causa, evento e intervenção, usando banco de dados centralizado para análise de causas recorrentes e priorização de ações.
- Juiz: Propõe integração e padronização dos registros conectando evento, causa e intervenção, que é a mudança essencial pedida pela referência.

**inventario · media · incorreta** Em um FPSO, um equipamento recebeu melhor acesso, modularização e sobressalentes dedicados, reduzindo o tempo esperado para voltar a operar após falha. Como nenhuma intervenção corretiva foi executada ainda, o que foi efetivamente melhorado?

- Referência: Foi melhorada a mantenabilidade do sistema e de seu suporte; o retorno ao serviço só se concretiza quando a manutenção é executada.
- Respondente: A disponibilidade do equipamento, levando a uma menor indisponibilidade e maior prontidão operacional.
- Juiz: Melhor acesso, modularização e sobressalentes melhoram a mantenabilidade e o suporte, não a disponibilidade efetiva antes de uma intervenção corretiva ocorrer.

**inventario · media · parcial** Em um FPSO, intertravamentos e funções automáticas de proteção estão atuando e, em alguns eventos, interrompem a produção para evitar dano ambiental e perdas maiores. Na avaliação do desempenho operacional, como a disponibilidade deve ser tratada?

- Referência: Deve ser avaliada em conjunto com a segurança, não isoladamente, porque essas atuações podem parar a produção para evitar consequências mais graves.
- Respondente: A disponibilidade deve ser considerada como a capacidade do sistema de operar dentro dos limites funcionais, levando em conta as interrupções por intertravamentos e proteções automáticas, refletindo a eficiência operacional e a confiabilidade do FPSO.
- Juiz: Considera as interrupções por intertravamentos, mas não explicita o ponto essencial de que a disponibilidade deve ser analisada em conjunto com a segurança.

**inventario · media · correta** Para elevar a disponibilidade do FPSO, a gestão propõe espaçar intervenções preventivas em equipamentos de processo, sem análise formal adicional. Essa decisão se sustenta tecnicamente apenas pela meta de produção?

- Referência: Não. A busca por maior disponibilidade não justifica reduzir intervenções preventivas sem avaliação de risco e integridade.
- Respondente: Não, a decisão deve considerar também a confiabilidade dos equipamentos, risco de falhas e impacto na operação, além da meta de produção.
- Juiz: O candidato responde corretamente que a meta de produção, sozinha, não sustenta espaçar preventivas sem considerar risco e confiabilidade.

**inventario · media · parcial** Em uma FPSO, os fluidos dos poços chegam misturados e podem trazer sólidos e outras impurezas. Se os sistemas de separação, tratamento e movimentação desses fluxos ficam restritivos, qual parâmetro global da unidade passa a ser o principal limitante da operação?

- Referência: A capacidade produtiva da unidade, pois ela depende da capacidade combinada de separar, tratar e movimentar óleo, gás e água.
- Respondente: A capacidade de processamento do sistema de separação e tratamento, especialmente o limite de fluxo máximo, passa a ser o parâmetro principal limitante.
- Juiz: Aponta a limitação de processamento, mas restringe a resposta ao sistema de separação/tratamento e não explicita a capacidade produtiva global da unidade, incluindo a movimentação dos fluxos.

**inventario · media · correta** Em um FPSO, uma bomba do processamento primário passa a operar com eficiência abaixo do esperado. Se a unidade precisa manter as especificações dos fluidos, a estabilidade operacional e o descarte de água dentro do aceitável, como a taxa de produção pode ser afetada?

- Referência: Pode precisar ser reduzida, porque a piora no desempenho do equipamento pode degradar a qualidade da separação e do tratamento dos fluidos.
- Respondente: A taxa de produção pode ser reduzida para compensar a eficiência da bomba, garantindo estabilidade, qualidade do fluido e descarte adequado.
- Juiz: O candidato afirma corretamente que a taxa de produção pode precisar ser reduzida para manter estabilidade operacional, qualidade dos fluidos e descarte adequado.

**inventario · media · parcial** No FPSO, o KPI de produção caiu porque o trem de processo virou a restrição e a equipe quer recuperar vazão ainda nesta campanha operacional. Qual classe de ação deve ser priorizada e por qual critério técnico ela deve ser escolhida?

- Referência: Deve-se priorizar uma medida corretiva, escolhida a partir da identificação do equipamento ou variável que limita a capacidade e do horizonte imediato de atuação.
- Respondente: Priorize ações de otimização do trem de processo, baseando-se na análise de gargalos, capacidade de ajuste, impacto na vazão e riscos operacionais para recuperar a produção.
- Juiz: Acerta ao usar análise de gargalo como critério, mas substitui a medida corretiva imediata da referência por uma formulação genérica de otimização.

**inventario · media · correta** Em um FPSO, a equipe passa a aplicar inibidor de incrustação em poços que ainda não perderam capacidade, priorizando evitar futuras paradas em vez de restaurar produção já afetada. Essa ação atua em que momento do problema e qual efeito se espera sobre a sua formação?

- Referência: Atua antes da perda e busca reduzir a probabilidade de formação do problema.
- Respondente: Ação preventiva que impede a formação de incrustações, mantendo a produção eficiente e evitando futuras interrupções por incrustações existentes.
- Juiz: Ela identifica corretamente uma ação preventiva antes da perda, voltada a reduzir a formação futura do problema.

**inventario · media · parcial** Em um FPSO, um equipamento compartilhado por várias correntes passa a limitar a vazão total processável da planta. Qual consequência de gestão se torna inevitável para a operação nesse caso?

- Referência: Torna-se inevitável priorizar entregas e alocar a capacidade disponível entre as correntes ou poços afetados pelo ponto comum limitado.
- Respondente: Adotar uma gestão de restrição de vazão ou gestor de fluxos para otimizar a produção e evitar sobrecarga do equipamento compartilhado.
- Juiz: Reconhece a necessidade de gerenciar a restrição, mas não explicita a priorização e alocação da capacidade entre correntes ou poços afetados.

**inventario · media · parcial** Em um FPSO, surgiu um gargalo em um equipamento compartilhado por várias correntes, sem falha individual de poço. Para operar dentro da capacidade disponível, que ajuste na contribuição dos produtores pode ser necessário?

- Referência: Redistribuir as vazões entre poços.
- Respondente: Reduzir a vazão de alguns poços ou produtores compartilhados para aliviar a carga no equipamento compartilhado e operar dentro da capacidade disponível.
- Juiz: Indica corte de vazão em alguns poços, mas a referência pede explicitamente a redistribuição das vazões entre produtores, e não apenas a redução de alguns.

**inventario · media · correta** Em um FPSO, um conjunto de poços entrou em fase madura, sem mudança relevante no arranjo de produção. Que corrente tende a crescer e passar a pressionar mais separação, tratamento, reinjeção e descarte?

- Referência: A corrente de água produzida tende a aumentar.
- Respondente: A corrente de água produzida tende a crescer, aumentando a pressão no sistema de separação, tratamento, reinjeção e descarte.
- Juiz: Coincide com a referência ao indicar o aumento da corrente de água produzida e seu impacto sobre separação, tratamento, reinjeção e descarte.

**inventario · media · correta** Uma análise de KPI em um FPSO mostra queda de vazão bruta em um poço e alteração de pressão; a evidência aponta formação de depósito na coluna de produção. Para atribuir corretamente essa perda, qual associação técnica deve ser feita?

- Referência: Deve-se vincular o depósito como fenômeno causador, a coluna de produção como ativo afetado e a alteração de pressão com queda de vazão como efeito operacional percebido.
- Respondente: A redução da vazão e a alteração de pressão indicam obstrução por depósitos na coluna de produção, afetando o fluxo e permitindo identificar a formação de depósitos como causa da perda de desempenho.
- Juiz: Relaciona o depósito como causa, a coluna de produção como ativo afetado e a alteração de pressão com queda de vazão como efeito operacional observado.

**inventario · media · correta** No processamento primário de um FPSO, medições críticas de pressão e nível ficam indisponíveis ou passam a oscilar sem confiabilidade, embora a capacidade física da planta não tenha mudado. O que isso tende a provocar na exposição da operação a desvios?

- Referência: Tende a elevar o risco de processo, porque a observabilidade cai e diminui a margem para detectar e corrigir desvios.
- Respondente: Aumenta a dificuldade de detectar desvios operacionais e limita a confiabilidade na tomada de decisão, podendo levar a ações corretivas tardias ou inadequadas.
- Juiz: Descreve corretamente a perda de observabilidade e a maior chance de ações tardias ou inadequadas, equivalente ao aumento do risco de processo.

**inventario · media · parcial** Em um FPSO, desvios operacionais exigem resposta rápida, mas a equipe depende de suporte remoto, a documentação está desatualizada e a responsabilidade técnica é difusa. Além das técnicas de análise, o que está faltando para sustentar a gestão de riscos ao longo da vida útil?

- Referência: Falta uma estrutura organizacional capaz de manter responsabilidades claras, documentação atualizada e acessível, gestão de mudanças e esclarecimento rápido dos parâmetros de projeto e operação.
- Respondente: Implementação de um sistema atualizado de gestão de conhecimento e formação contínua da equipe para melhorar a responsabilidade técnica e a resposta rápida.
- Juiz: Toca em atualização, conhecimento e responsabilidade, mas omite a necessidade central de estrutura organizacional com responsabilidades claras, gestão de mudanças e rápido esclarecimento de parâmetros de projeto e operação.

**inventario · media · parcial** Em uma parada de manutenção no FPSO, a equipe quer monitorar continuamente o risco e revisar decisões antes da próxima intervenção. Se o encerramento ficar restrito a custos finais e pendências, que registro ainda é necessário consolidar para viabilizar essas duas ações?

- Referência: É necessário registrar o que foi planejado, o que ocorreu, os desvios identificados e as lições que permanecem válidas para intervenções futuras.
- Respondente: Registro de atividades de manutenção, incluindo ações tomadas, condições da instalação e avaliações de risco atualizadas.
- Juiz: Ele cita registro de atividades e risco, mas não explicita o comparativo planejado versus ocorrido, os desvios e as lições aprendidas, que são o núcleo da referência.

**inventario · media · correta** Na gestão de planejamento, custos e riscos de um FPSO, a equipe conclui a seleção dos sistemas críticos após revisar funções e vulnerabilidades da unidade. Que consequência isso deve produzir na implantação e na atualização dos controles de risco?

- Referência: Os controles devem ser direcionados prioritariamente às funções identificadas como mais críticas na unidade.
- Respondente: A seleção dos sistemas críticos aprimora a eficiência na implantação e atualização dos controles de risco, priorizando recursos nas áreas mais vulneráveis e aumentando a segurança operacional do FPSO.
- Juiz: Indica corretamente que a criticidade definida deve direcionar prioritariamente a implantação e atualização dos controles de risco.

**inventario · media · correta** Em um FPSO, uma salvaguarda crítica segue cadastrada como disponível, mas está com testes atrasados, manutenção incompleta e hipóteses de demanda diferentes das usadas no estudo de risco. Para decidir se ela ainda sustenta a operação, o que deve prevalecer sobre sua mera existência documental?

- Referência: Deve prevalecer seu desempenho funcional real: capacidade de cumprir a função de projeto com a confiabilidade requerida e sob premissas ainda válidas nas análises de risco.
- Respondente: A condição operacional real e os testes atualizados, garantindo sua capacidade de suportar emergências, prevalecem sobre sua mera existência documental.
- Juiz: A resposta privilegia a condição e o desempenho operacional reais, verificados por testes, acima do cadastro documental, que é a essência da referência.

**inventario · media · parcial** Em um sistema crítico do FPSO, a taxa de falhas não muda, mas o tempo de reparo cai e sobressalentes e equipe já estão garantidos. Quando esse sistema for demandado, que métrica de desempenho tende a melhorar?

- Referência: A disponibilidade, porque ela depende da confiabilidade combinada à mantenabilidade e ao suporte de manutenção com recursos externos assegurados.
- Respondente: O tempo médio de reparo (MTTR) tende a melhorar, reduzindo o tempo total de indisponibilidade.
- Juiz: O candidato identifica a melhora do MTTR, que é a causa, mas não a métrica de desempenho pedida pela referência, que é a disponibilidade.

**inventario · media · incorreta · ref. inválida** Em um FPSO, uma auditoria identifica autodiagnóstico falho, ações contingenciais insuficientes e correções incompatíveis com o risco. Qual consequência operacional e econômica passa a ser plausível?

- Referência: A instalação pode ser interditada, com perdas relevantes de receita.
- Respondente: Aumento do risco de incidentes, potencial falha de equipamentos críticos, aumento de custos operacionais, multas e perda de produtividade devido a incidentes ou paradas não planejadas.
- Juiz: A resposta não traz a interdição da instalação com perda relevante de receita indicada na referência, e a própria pergunta admite outras consequências plausíveis, tornando a referência não única.

**inventario · media · parcial** Num FPSO, após comparar em bancada a mesma emulsão com vários produtos e dosagens sob temperatura, mistura e tempo controlados, um químico apresentou melhor separação. Que conclusão é válida para a escolha desse produto?

- Referência: Que ele é um candidato selecionado por triagem empírica de bancada para desemulsificação; a escolha final ainda exige validação operacional.
- Respondente: A escolha do químico deve ser baseada na melhor eficiência de separação, estabilidade e compatibilidade com condições operacionais, garantindo desempenho otimizado na produção do FPSO.
- Juiz: Reconhece a importância do desempenho e da compatibilidade operacional, mas não explicita que o resultado de bancada apenas seleciona um candidato e ainda requer validação em operação.

**inventario · media · parcial** Em uma corrente de produção, o escoamento passa a impor alto cisalhamento e as gotículas formadas não se reagrupam com rapidez. Nessa condição, que comportamento tende a surgir entre as fases líquidas?

- Referência: Óleo e água tendem a permanecer dispersos um no outro, caracterizando emulsão óleo/água.
- Respondente: O comportamento tende a ser de separação de fases, formando uma emulsão ou dispersão não reattiva, dificultando a coalescência e a formação de gotículas maiores.
- Juiz: Acerta ao mencionar emulsão/dispersão e dificuldade de coalescência, mas erra ao falar em separação de fases, que contraria a permanência das fases dispersas.

**inventario · media · correta** Num separador de produção, a espuma persiste e passa a dificultar a separação gravitacional entre gás e líquido. Qual efeito tende a surgir na linha de gás como sinal desse quadro?

- Referência: Tende a aumentar o arraste de líquido na saída de gás, com queda da eficiência global de separação.
- Respondente: Aumento de sólidos ou água no gás de top, indicando contaminação e entupimento potencial na linha de gás.
- Juiz: Ao citar aumento de água no gás de topo, a resposta captura o arraste de líquido na saída de gás indicado pela referência.

**inventario · media · parcial** Em testes de processo no FPSO, os filmes entre bolhas passam a drenar mais devagar e a romper com mais dificuldade. Qual tendência operacional se espera para a espuma no separador?

- Referência: Ela tende a durar mais no separador, ficando mais difícil de colapsar.
- Respondente: A tendência é que a espuma se torne mais persistente e difícil de romper, levando a uma maior retenção de bolhas e possível aumento da eficiência na separação de fases líquidas e gaseosas.
- Juiz: A resposta acerta a maior persistência da espuma, mas adiciona a ideia de possível aumento de eficiência de separação, o que contraria a implicação operacional usual do problema.

**inventario · media · correta** Num FPSO, duas correntes de água produzida para descarte têm salinidade semelhante, mas uma se comporta como coloide estável e a outra como emulsão fina persistente. Se a equipe escolher coagulante e floculante apenas pela família química usual, que premissa técnica essencial estará sendo desconsiderada?

- Referência: Que a seleção deve começar pelo mecanismo dominante da água a tratar, e não pela família do produto isoladamente.
- Respondente: A abiidade de formar sistemas estáveis depende de características específicas da água, como composição iônica, pH e partículas presentes, que não são determinadas apenas pela família química do coagulante ou floculante.
- Juiz: A resposta reconhece que a escolha deve considerar o comportamento dominante da água tratada, e não apenas a família química do produto.

**inventario · media · parcial** Num FPSO, a água do mar após cloração segue para tratamento com bissulfito. Em uma campanha, o cloro residual entra acima do habitual e a dosagem do sequestrante não muda. O que tende a ocorrer com o teor de oxigênio dissolvido na saída desse tratamento?

- Referência: Ele tende a aumentar, porque parte do bissulfito reage com o cloro residual e sobra menos reagente para remover o oxigênio.
- Respondente: O teor de oxigênio dissolvido tende a aumentar devido à redução do cloro residual, que reduz a oxidação de matéria orgânica e diminui o consumo de oxigênio na etapa seguinte.
- Juiz: Acerta a tendência de aumento do oxigênio dissolvido, mas erra o mecanismo, que na referência é o consumo do bissulfito pelo excesso de cloro residual.

**inventario · media · correta** Em um FPSO, dois biocidas reduzem igualmente a contagem microbiológica da água de injeção. Nos testes, um deles passa a gerar espuma e piora a separação óleo-água nas etapas associadas. Qual deve ser o fator decisivo na escolha?

- Referência: Deve prevalecer o produto que não compromete o processamento; eficácia microbiológica igual não compensa efeitos adversos como espuma e pior separação.
- Respondente: Deve-se priorizar o biocida que não comprometa a separação óleo-água, garantindo eficiência microbiológica sem afetar o processo de separação.
- Juiz: A resposta coincide com a referência ao priorizar o biocida que preserve o processamento e a separação óleo-água quando a eficácia microbiológica é equivalente.

**inventario · media · correta** Na água de injeção de um FPSO, o tratamento químico para controle microbiológico mantém a mesma dosagem e o mesmo tempo de aplicação, mas há incrustações minerais e camadas aderidas nas superfícies internas. Qual efeito isso tende a ter sobre o resultado do tratamento?

- Referência: Tende a reduzir a eficácia do biocida, porque essas camadas criam regiões protegidas e limitam o alcance do produto aos microrganismos.
- Respondente: Incrustações minerais podem reduzir a eficiência do tratamento microbiológico, dificultando a penetração dos produtos químicos e favorecendo a formação de biofilmes, o que compromete o controle microbiológico na água de injeção.
- Juiz: A resposta coincide com a referência ao apontar que incrustações e camadas aderidas protegem microrganismos e reduzem a penetração/eficácia do biocida.

**inventario · media · correta** Após analisar as condições do circuito de água de injeção e validar por monitoramento que o tratamento microbiológico é eficaz, a equipe vai definir a forma temporal de aplicação do biocida. Que regimes podem ser escolhidos?

- Referência: Pode-se adotar dosagem contínua ou aplicações intermitentes, conforme o circuito e a eficácia comprovada.
- Respondente: Regimes possíveis incluem doses contínuas, pulsadas ou sob demanda, dependendo da criticidade e ciclo de operação do sistema de injeção.
- Juiz: Inclui dosagem contínua e aplicações pulsadas ou intermitentes, que correspondem aos regimes previstos na referência.

**inventario · media · incorreta** Em uma linha de gás de um FPSO, mantendo pressão e composição do gás constantes e assumindo boa mistura na água livre, a concentração efetiva de MEG na fase aquosa aumenta. O que acontece com a temperatura limite para início de formação de hidratos?

- Referência: Ela diminui; com mais MEG na fase aquosa, o sistema pode operar a temperaturas mais baixas antes de atingir a condição de formação de hidratos.
- Respondente: A temperatura limite para formação de hidratos aumenta, pois maior concentração de MEG na água libera mais energia, permitindo maior estabilidade térmica antes da formação dos hidratos.
- Juiz: A referência indica que maior concentração de MEG diminui a temperatura limite de formação de hidratos, e o candidato afirmou o oposto.

**inventario · media · incorreta** Em um FPSO, MEG é injetado em trechos topside e subsea para evitar hidratos e depois segue para recuperação e reúso. Ao ajustar esse programa, além da proteção nas linhas, que aspecto do circuito precisa ser acompanhado em paralelo?

- Referência: O controle do teor de sais na etapa de recuperação do MEG.
- Respondente: O controle da temperatura e pressão do fluido injetado deve ser monitorado em paralelo para evitar a formação de hidratos no sistema.
- Juiz: A resposta trata de temperatura e pressão para prevenir hidratos, mas a referência pede acompanhar o teor de sais no circuito de recuperação do MEG.

**inventario · media · incorreta** Em um FPSO, a injeção de MEG mantém o controle de hidratos. Na unidade de recuperação, a corrente retorna com água produzida rica em íons e o processo passa a concentrar o glicol com remoção de água. Que risco operacional adicional ainda deve ser considerado nesse circuito?

- Referência: Pode ocorrer precipitação dos sais trazidos pela água produzida, formando incrustações no circuito de recuperação do MEG.
- Respondente: Risco de formação de hidratos devido à concentração do glicol e presença de íons, que pode obstruir o sistema e reduzir a eficiência do controle de hidratos.
- Juiz: O risco adicional esperado no circuito de recuperação de MEG com água rica em íons é precipitação de sais e incrustação, não formação de hidratos.

**inventario · media · correta** Em um FPSO, o gás úmido tem risco de hidrato em uma linha resfriada, traços de H2S em outro trecho e tendência à espuma no condicionamento. Ao definir onde aplicar os químicos, qual critério técnico deve orientar a distribuição entre correntes e subsistemas?

- Referência: Deve-se distribuir cada produto conforme a ameaça predominante em cada trecho, porque cada químico atua sobre um problema específico; por isso, eles podem coexistir no processo sem necessariamente ir para a mesma corrente ou ponto de injeção.
- Respondente: Priorizar a aplicação de químicos em áreas com risco de formação de hidratos, H2S ou espuma, considerando a severidade do risco, fluxo, temperatura e composição do gás e líquidos, para prevenção eficiente e econômica.
- Juiz: A resposta adota o critério correto de distribuir químicos conforme o risco/problema predominante em cada trecho ou subsistema.

**inventario · media · correta** Em uma linha de produção, um inibidor orgânico consegue se adsorver ao aço carbono e manter um filme contínuo sobre a parede interna, sem mudança relevante de pH, salinidade ou temperatura. Que efeito se espera sobre a taxa de corrosão?

- Referência: Tende a diminuir, porque o filme adsorvido dificulta o acesso das espécies agressivas à superfície metálica.
- Respondente: A taxa de corrosão diminui devido à formação de um filme protetor que impede o contato direto entre o aço e o ambiente corrosivo.
- Juiz: Indica corretamente que o filme adsorvido do inibidor reduz a taxa de corrosão ao dificultar o acesso das espécies agressivas ao metal.

**inventario · media · incorreta** Num poço com risco de obstrução por hidratos no escoamento, passa-se a injetar MEG na cabeça do poço como medida de prevenção. Mantida a pressão, para que lado se desloca a condição térmica em que esses sólidos começariam a se formar?

- Referência: Para temperaturas mais baixas; a injeção de MEG reduz a temperatura de formação de hidratos.
- Respondente: A condição térmica desloca-se para temperaturas mais altas, reduzindo a formação de hidratos ao aumentar a temperatura do fluido na cabeça do poço.
- Juiz: Afirma o deslocamento no sentido oposto ao correto, pois o MEG reduz a temperatura de formação de hidratos a uma dada pressão.

**inventario · media · correta** Se o tratamento mantém inibidor disponível na fase aquosa durante o contato com íons formadores e ele interfere na nucleação e no crescimento cristalino, qual efeito se espera em coluna, gravel e outras superfícies molhadas do sistema produtor?

- Referência: Redução da tendência de formação de incrustações aderentes nessas superfícies, sem implicar eliminação completa.
- Respondente: Espera-se redução na formação de incrustações, resultando em melhor fluxo e menor obstrução nas superfícies molhadas do sistema.
- Juiz: A resposta traz o efeito essencial esperado, que é a redução da formação de incrustações nas superfícies molhadas do sistema produtor.

**inventario · media · incorreta** Após um squeeze em um poço ligado ao FPSO, a equipe quer acompanhar a evolução do tratamento ao longo das semanas. Em qual corrente de produção deve monitorar a presença do produto químico?

- Referência: Na água produzida, acompanhando o retorno do inibidor.
- Respondente: Deve monitorar na corrente de produção que acompanha o tratamento químico, geralmente na linha de produção principal ou na saída do sistema de tratamento, para verificar a eficácia e presença do químico ao longo do tempo.
- Juiz: No acompanhamento de squeeze, a presença do químico deve ser monitorada na água produzida, e o candidato não indicou essa corrente.

**inventario · media · correta** Em um FPSO, um trecho da linha de produção opera mais frio que o restante, e o óleo sofre queda adicional de temperatura ao passar por ele. Que tipo de depósito tende a se intensificar nesse trecho?

- Referência: Tende a aumentar a deposição de parafinas, porque o resfriamento do óleo favorece a cristalização das frações parafínicas.
- Respondente: Depositos de parfinas e sólidos de管理
- Juiz: Menciona deposição de parafinas, que é o efeito esperado do resfriamento adicional do óleo, apesar do texto final estar truncado.

**inventario · media · correta** Em um FPSO, após a mistura de correntes de diferentes origens, surgem depósitos orgânicos em uma linha, embora pressão e temperatura tenham permanecido praticamente constantes. Na avaliação da tendência desse depósito, que aspecto do fluido deve ser priorizado para explicar a perda de estabilidade?

- Referência: A composição do petróleo e as interações que mantêm essas espécies dispersas.
- Respondente: Deve-se priorizar a composição química do fluido, especialmente a concentração de compostos orgânicos e sais, que influenciam a solubilidade e estabilidade do depósito.
- Juiz: Foca corretamente na composição do fluido como aspecto prioritário para explicar a perda de estabilidade após a mistura.

**inventario · media · correta** Num FPSO, mangueiras e recipientes são usados sequencialmente para dois químicos sem linha dedicada nem flushing adequado, e pode haver resíduo entre transferências. Qual consequência técnica essa condição tende a gerar?

- Referência: Favorece contato acidental entre produtos incompatíveis, com reação paralela que consome reagente e reduz o desempenho do tratamento ou da injeção.
- Respondente: Contaminação cruzada, que pode comprometer a qualidade do químico, provocar reações indesejadas e afetar a eficiência do processo de tratamento ou produção.
- Juiz: Identifica corretamente a contaminação cruzada entre produtos incompatíveis, com reações indesejadas e perda de desempenho.

**inventario · media · correta** Durante a transferência de um químico em um módulo offshore, uma ruptura de mangueira libera líquido dentro de uma área com mureta estanque e drenagem dedicada. Qual efeito isso tende a ter sobre o derrame e a segurança no entorno?

- Referência: O vazamento tende a ficar restrito ao local, reduzindo o espalhamento para áreas adjacentes e a exposição de pessoas, equipamentos e meio externo.
- Respondente: A drenagem dedicada deve ajudar a conter e direcionar o líquido, minimizando o risco de propagação e facilitando a limpeza, enquanto a mureta estanque impede que o líquido se espalhe para áreas adjacentes, aumentando a segurança.
- Juiz: Descreve corretamente o efeito de contenção local pela mureta e pela drenagem dedicada, reduzindo espalhamento e exposição no entorno.

**inventario · media · correta** Num FPSO, a rota de um químico passou a ter mais repasses internos entre recebimento, estocagem, tanque de serviço, linha de injeção e eventual recirculação. Sem mudar o produto, o que tende a acontecer com a chance de desvios de manuseio?

- Referência: Ela tende a aumentar, porque cada etapa adicional pode favorecer identificação incorreta, mistura indevida, entrada de ar, retenção de produto e maior exposição ocupacional.
- Respondente: Aumenta a chance de desvios de manuseio devido à maior complexidade operacional e maior número de etapas interligadas.
- Juiz: Mantém a ideia essencial de que mais etapas e interfaces aumentam a probabilidade de desvios de manuseio.

**inventario · media · parcial** Em uma rotina offshore de químicos, a equipe acompanha apenas o volume nos tanques. Se a intenção é evitar surpresas operacionais a jusante, que foco adicional o monitoramento precisa ter?

- Referência: Precisa acompanhar condições e sinais precoces do armazenamento e manuseio que antecedam falhas de segurança, aumento de corrosividade ou perda de desempenho do processo, não só o inventário.
- Respondente: Monitoramento da composição química, temperatura e pressão dos tanques para detectar variações que possam afetar a operação e a qualidade do produto.
- Juiz: Vai além do inventário ao citar condições dos tanques, mas omite o foco em sinais precoces ligados a segurança, corrosividade e perda de desempenho do processo.

**inventario · media · correta** Em um FPSO, a injeção de biocida é regulada por um método microbiológico cujo resultado sai dias após a coleta, embora a meta seja acompanhar a população-alvo durante a operação. Que efeito isso tende a ter sobre o ajuste de dosagem?

- Referência: Tende a tornar o ajuste menos adequado, porque a dosagem passa a reagir tarde à população-alvo, aumentando o risco de desperdício, custo excessivo e impacto ambiental desnecessário.
- Respondente: Atraso na análise dificulta ajustes precisos, podendo levar a sub ou superdosagem de biocida, afetando o controle microbiológico e a eficiência do tratamento na operação do FPSO.
- Juiz: Captura a essência de que o atraso analítico piora o ajuste da dosagem e pode causar sub ou superdosagem durante a operação.

**inventario · media · parcial** Em um FPSO, a dosagem de oxidante no sistema de água é aumentada até o residual ficar adequado, e esse passa a ser o único indicador usado para correção. Considerando interação entre químicos e variáveis de processo, que efeito operacional esse critério pode mascarar?

- Referência: Pode melhorar o residual oxidante e, ao mesmo tempo, piorar outra variável do processo, como corrosão ou deposição, por perda da proteção química global.
- Respondente: Pode mascarar a efetividade de outros produtos químicos, como biocombatentes ou dispersantes, além de não indicar possíveis desequilíbrios microbiológicos ou químico-biológicos no sistema.
- Juiz: Reconhece que usar só o residual pode mascarar efeitos sobre outros químicos, mas não explicita a piora operacional típica de corrosão ou deposição por perda da proteção química global.
