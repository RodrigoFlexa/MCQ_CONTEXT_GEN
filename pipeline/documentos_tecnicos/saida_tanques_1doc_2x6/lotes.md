# Lotes de questões

Candidatas e decisões automáticas; validação humana pendente.

## L01 — 6/6 candidatas

Documento: D01-0f6c385752b0. Estados: {'aprovada': 5, 'reprovada': 1}



### Q001 — aprovada

Durante uma transferência interna em um FPSO, a equipe informa que o inventário total de bordo não mudará, porque o volume será apenas deslocado de um tanque central para um tanque lateral de mesma capacidade. Explique por que essa justificativa é insuficiente para autorizar a operação e indique quais efeitos devem ser avaliados antes e durante a transferência para considerar a manobra tecnicamente segura.

**Resposta:** A justificativa é insuficiente porque manter o inventário total constante não significa manter a embarcação na mesma condição estrutural e de estabilidade. A transferência interna altera a distribuição longitudinal e/ou transversal de massa, podendo modificar banda, trim, estabilidade, bending moment (BM) e shear force (SF), inclusive nas condições transitórias da manobra. Além disso, durante a transferência podem existir níveis parciais de enchimento que exigem atenção às condições de carregamento do tanque. Para considerar a operação tecnicamente segura, devem ser verificados no plano aprovado e no loading/stability computer, no mínimo, os estados inicial, intermediário e final, acompanhando estabilidade, banda, trim, BM e SF ao longo da transferência.

**Parecer:** Juiz, adjudicação e novidade concluídos; revisão humana pendente

### Q002 — aprovada

Em uma descarga para offloading, a pressão de um tanque de carga começa a cair de forma persistente enquanto a vazão de exportação permanece alta. Sem assumir falha específica de equipamento, descreva a decisão operacional imediata mais adequada e justifique tecnicamente com base na relação entre bombeio, gás inerte e segurança do tanque.

**Resposta:** A decisão imediata mais adequada é reduzir a taxa de descarga ou interromper temporariamente o bombeio desse tanque, priorizando o restabelecimento de pressão positiva segura antes de prosseguir. A justificativa é que, no esvaziamento, o volume retirado do tanque precisa ser reposto por IG ou sistema de blanketing aplicável em vazão e qualidade suficientes. Se isso não ocorre, há risco de subpressão, entrada de ar, perda da inertização adequada e formação de atmosfera insegura no espaço de vapor. A continuidade da descarga com pressão em queda também pode exceder a capacidade atmosférica do sistema em relação à capacidade hidráulica das bombas. Em paralelo, deve-se verificar alinhamento do header, disponibilidade e resposta do sistema de IG, pressão no main/header e qualidade do gás antes de retomar a taxa planejada.

**Parecer:** Juiz, adjudicação e novidade concluídos; revisão humana pendente

### Q003 — aprovada

No planejamento de enchimento de um tanque de carga em FPSO, por que iniciar diretamente na vazão máxima da bomba pode ser tecnicamente inadequado mesmo quando o tanque tem espaço disponível? Responda relacionando a taxa de enchimento com venting, evolução de gás e proteção estrutural do tanque.

**Resposta:** Iniciar diretamente na vazão máxima pode ser inadequado porque a limitação da operação não é apenas volumétrica ou hidráulica; ela também é atmosférica. No enchimento, a atmosfera do espaço de vapor precisa ser deslocada e ventada na mesma ordem de grandeza do volume que entra, sem gerar sobrepressão. Em FPSO, esse requisito é mais sensível porque o óleo pode chegar com maior tendência de evolução de gás, inclusive por aquecimento e estabilização parcial, aumentando a carga sobre o sistema de venting. Se a taxa de enchimento exceder a capacidade efetiva de venting e de alívio, pode ocorrer aumento anormal de pressão, atuação indevida ou insuficiente de P/V valves, maior emissão de vapores inflamáveis e, em caso extremo, risco à integridade estrutural do tanque. Por isso, a sequência correta é partir em taxa moderada, observar pressão e comportamento do sistema e só então aumentar de forma controlada.

**Parecer:** Juiz, adjudicação e novidade concluídos; revisão humana pendente

### Q004 — aprovada

Um operador observa, durante uma transferência interna planejada, que o nível do tanque fonte está caindo conforme esperado, mas o tanque destino sobe muito menos do que o previsto. Considerando apenas as informações operacionais gerais de um FPSO, explique como essa discrepância deve ser interpretada e quais hipóteses técnicas prioritárias precisam ser consideradas antes de continuar a operação.

**Resposta:** A discrepância deve ser tratada como um desvio operacional potencialmente sério, não como simples atraso de leitura sem verificação. Se o tanque fonte perde volume e o destino não ganha volume correspondente, é necessário assumir que o caminho real do escoamento pode não ser o pretendido até que o balanço seja reconciliado em condição segura. As hipóteses técnicas prioritárias incluem: line-up incorreto; comunicação não intencional com outro tanque, slop ou header comum; válvula passing; modificação temporária ou isolamento inadequado, como spool, spade ou bypass esquecido; vazamento interno para rota não prevista; e erro relevante de medição, instrumentação ou calibração/strapping do tanque. A operação não deve prosseguir normalmente até confirmar o line-up real, verificar válvulas e isolamentos críticos, checar outros tanques ou sistemas que possam estar recebendo fluido e comparar as leituras com o sistema de carga/estabilidade.

**Parecer:** Juiz, adjudicação e novidade concluídos; revisão humana pendente

### Q005 — reprovada

Compare duas estratégias genéricas para uma operação de enchimento ou esvaziamento em FPSO/FSO: (A) manter vários tanques simultaneamente em níveis intermediários por longo período para ganhar flexibilidade hidráulica; (B) concentrar a transição em poucos tanques por vez, desde que BM, SF, trim e banda permaneçam dentro dos limites aprovados. Qual estratégia tende a ser mais robusta do ponto de vista de estabilidade e controle operacional, e por quê?

**Resposta:** Em geral, a estratégia B tende a ser mais robusta, porque reduz a quantidade de tanques parcialmente cheios ao mesmo tempo e, assim, tende a diminuir o efeito acumulado de superfície livre e a permanência em condições intermediárias mais sensíveis a sloshing. Já a estratégia A pode tornar os estados transitórios mais complexos de controlar e verificar. Essa preferência não é absoluta: a sequência só é adequada se permanecer dentro do envelope aprovado de estabilidade e dos limites de BM, SF, trim e banda.

**Parecer:** Limite de refinamentos; consulte os pareceres

### Q006 — aprovada

Antes de iniciar um offloading, a equipe confia no stability computer porque os conteúdos dos tanques do casco são recebidos automaticamente. Explique por que essa confiança, sozinha, pode ser insuficiente para validar a condição inicial da operação e indique que tipo de informação ainda precisa ser inserida ou reconciliada manualmente para que a simulação tenha valor operacional.

**Resposta:** Essa confiança, sozinha, é insuficiente porque o stability computer recebe automaticamente os conteúdos dos tanques do casco, mas não representa a condição real da unidade se outras variáveis relevantes não forem atualizadas manualmente. Ainda é necessário inserir ou reconciliar manualmente mudanças em cargas de convés, como contêineres, e outras variáveis não capturadas automaticamente. Se a condição inicial estiver incorreta, a simulação pode levar a uma avaliação errada da estabilidade, dos bending moments e das shear forces durante o offloading.

**Parecer:** Juiz, adjudicação e novidade concluídos; revisão humana pendente

## L02 — 6/6 candidatas

Documento: D01-0f6c385752b0. Estados: {'aprovada': 6}



### Q007 — aprovada

Durante a preparação para recolocar em serviço um tanque de carga que ficou isolado para inspeção interna, a equipe confirma no painel que as válvulas principais estão na posição prevista e propõe retomar a inertização e o uso operacional do tanque. Explique por que essa verificação é insuficiente como barreira única e descreva quais confirmações adicionais são tecnicamente necessárias antes do retorno ao serviço, considerando risco de sobrepressão e integridade do sistema atmosférico do tanque.

**Resposta:** A verificação apenas da posição indicada das válvulas é insuficiente porque o retorno ao serviço de um tanque previamente isolado depende também da remoção correta de blanks/spades, da restauração efetiva dos caminhos de IG, venting e alívio e do encerramento controlado das barreiras temporárias. Um tanque pode aparentar estar alinhado no painel e ainda assim permanecer parcialmente bloqueado ou mal reinstalado, o que pode levar a sobrepressurização quando o IG for restabelecido. Antes do retorno ao serviço, devem ser confirmados formalmente: retirada/instalação correta de blanks e spades; posição real das válvulas de isolamento; restabelecimento do caminho de venting e de proteção P/V; possibilidade de isolamento claro do tanque dentro do sistema de IG; coerência com PTW/P&ID e encerramento das permissões e isolações temporárias. A retomada da inertização e da operação só é aceitável após essa reconfirmação.

**Parecer:** Juiz, adjudicação e novidade concluídos; revisão humana pendente

### Q008 — aprovada

Em um offloading, a equipe decide usar os tanques de lastro apenas como correção posterior: primeiro descarrega a carga na maior taxa possível e só depois ajusta trim e banda caso apareçam desvios. Compare essa lógica com um planejamento da sequência em que carga e lastro são coordenados ao longo da operação, e justifique qual abordagem é tecnicamente mais adequada para manter a unidade dentro do envelope operacional.

**Resposta:** A abordagem tecnicamente mais adequada é a de planejar a sequência com coordenação entre descarga e lastro ao longo de toda a operação. No offloading, a retirada de carga modifica continuamente a distribuição de pesos e pode alterar trim, banda, estabilidade, bending moment (BM) e shear force (SF). Se o lastro for usado apenas de forma reativa, a unidade pode passar por condições transitórias inadequadas antes da correção. Por isso, a operação deve seguir plano de estabilidade/loading aprovado, com verificação das condições inicial, intermediárias e final no loading/stability computer. Fracionar a operação em etapas ou checkpoints é uma forma válida de implementar esse controle. A lógica de corrigir apenas depois do desvio aparecer só seria aceitável se análise prévia comprovasse que toda a curva de descarga permanece dentro dos limites sem compensação antecipada.

**Parecer:** Juiz, adjudicação e novidade concluídos; revisão humana pendente

### Q009 — aprovada

Em uma transferência interna entre um tanque de carga e um slop, a equipe argumenta que a manobra é hidraulicamente simples e que basta verificar se o nível final planejado foi atingido. Explique por que essa premissa é inadequada em um FPSO/FSO e indique, em termos gerais, que tipo de planejamento e controle operacional deve existir para tratar também as condições transitórias da operação.

**Resposta:** A premissa é inadequada porque, em FPSO/FSO, a condição mais crítica pode ocorrer durante a transferência e não apenas no estado final. Ao longo da manobra, a distribuição de pesos e conteúdos dos tanques muda continuamente, o que pode afetar trim, estabilidade e também os esforços globais do casco, como bending moment e shear force. Por isso, a transferência não deve ser conduzida apenas como um objetivo hidráulico de encher ou esvaziar um tanque, mas conforme um plano operacional aprovado, com a sequência da manobra e verificações intermediárias que permitam acompanhar os efeitos da condição transitória e corrigir ou interromper a operação se o comportamento real se afastar do previsto. Esse controle deve estar alinhado ao loading/stability manual, ao plano de estabilidade e ao loading or stability computer usado a bordo.

**Parecer:** Juiz, adjudicação e novidade concluídos; revisão humana pendente

### Q010 — aprovada

Durante o planejamento de aumento de vazão em uma operação com tanque inertizado, a bomba e a linha de processo têm capacidade disponível, mas há dúvida sobre o desempenho do sistema de venting e da proteção P/V. Tomando apenas essas informações gerais, decida se o aumento de taxa deve ser autorizado e justifique com base na relação entre capacidade hidráulica, capacidade atmosférica e função do emergency P/V breaker.

**Resposta:** O aumento de taxa não deve ser autorizado apenas com base na capacidade hidráulica da bomba e da linha. Em operações de enchimento ou esvaziamento, a taxa segura também é limitada pela capacidade atmosférica do tanque: venting, IG, válvulas P/V e dispositivos de alívio precisam acompanhar a variação de volume sem gerar sobrepressão ou vácuo excessivo. Se houver dúvida sobre o desempenho do venting ou da proteção P/V, a decisão tecnicamente correta é manter taxa conservadora ou interromper o aumento até verificar a disponibilidade e a integridade desses sistemas. O emergency P/V breaker não justifica operar no limite por conveniência; ele é uma barreira de segurança para falha do conjunto principal, deve ser dimensionado para cenário severo plausível e mantido/testado como elemento crítico, não usado como substituto de capacidade operacional confirmada. Se houver indício de contrapressão por drenagem deficiente de vent header/KO drum ou falha de P/V, a restrição é ainda mais forte.

**Parecer:** Juiz, adjudicação e novidade concluídos; revisão humana pendente

### Q011 — aprovada

Em uma condição de baixo vento, a equipe pretende realizar venting operacional de tanques porque o restante do sistema está disponível e a taxa de operação é considerada moderada. Explique por que a avaliação meteorológica entra como parte da decisão operacional e quais riscos adicionais de dispersão devem ser considerados em FPSO em comparação com um navio-tanque em trânsito.

**Resposta:** A avaliação meteorológica entra na decisão porque o venting não é apenas uma função de alívio do tanque; ele também depende da capacidade de dispersar com segurança os vapores liberados. Em FPSO, esse ponto é mais crítico do que em um navio-tanque em trânsito porque a unidade permanece praticamente fixa e, em calmaria, há menos movimento relativo para ajudar na dispersão das misturas de IG e hidrocarbonetos ao redor das saídas de vent. Assim, mesmo com sistema disponível e taxa moderada, baixo vento pode aumentar a chance de formação de atmosfera inflamável nas proximidades dos outlets e de áreas adjacentes ou tomadas de ar. Por isso, o procedimento deve considerar critérios meteorológicos para permitir venting e, se as condições forem desfavoráveis, restringir, adiar ou reconfigurar a operação conforme a prática aprovada da unidade.

**Parecer:** Juiz, adjudicação e novidade concluídos; revisão humana pendente

### Q012 — aprovada

Durante o planejamento de offloading tandem, a equipe discute apenas a sequência de retirada de óleo dos tanques e a meta de vazão de exportação. Justifique por que esse planejamento é incompleto e indique que outros elementos da sequência devem ser incluídos para que a operação contemple parada segura e recuperação da linha de exportação.

**Resposta:** Esse planejamento é incompleto porque, no offloading tandem, não basta definir de quais tanques sairão os volumes e em que vazão. A sequência também precisa contemplar as barreiras de transferência entre FPSO e shuttle tanker, especialmente os permissivos de bombeio, os meios de shut-off para minimizar perda de hidrocarbonetos em caso de ruptura, desconexão ou perda de posição relativa, e a condição de recuperação segura da linha após o término. Devem ser previstos, no mínimo, a lógica de permit to pump/alinhamento entre as unidades, os dispositivos e ações de isolamento ou parada remota da exportação, e a disponibilidade de nitrogênio ou gás inerte para deslocar o conteúdo da mangueira/linha após a operação. Esses itens fazem parte da segurança da sequência porque reduzem inventário remanescente na linha, limitam vazamentos e garantem encerramento controlado do offloading.

**Parecer:** Juiz, adjudicação e novidade concluídos; revisão humana pendente

