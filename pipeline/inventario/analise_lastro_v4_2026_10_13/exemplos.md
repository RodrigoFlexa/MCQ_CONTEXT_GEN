# Exemplos reais do Lastro v4

Notas produzidas no servidor antes dos ajustes de autonomia dos prompts. Textos preservados, sem reescrita nesta análise.

## Classes de DP/SPD, redundância e capacidade residual para desconexão segura em operações de alívio

ID: `62e43c1988:a25:k3`; subtópico: Sistema de ancoragem, manutenção e monitoramento da posição; coleções: hse, petroles

As classes de DP/SPD são definidas pelo efeito de uma falha simples sobre a manutenção de posição e, por isso, determinam o nível de redundância exigido na arquitetura de controle, potência e propulsão. Em operações de alívio próximas a FPSOs ou terminais oceânicos, o objetivo operacional da redundância não é apenas evitar a perda de posição, mas preservar margem de manobra suficiente para desconectar com segurança, afastar o aliviador e reduzir risco de colisão e derramamento.

### O que é e para que serve

As classes de DP/SPD graduam a confiabilidade de manutenção de posição de acordo com a consequência esperada da perda de posição. Nas diretrizes IMO citadas, a classe é definida pelo efeito de uma falha simples e pela natureza das falhas que precisam ser consideradas na análise. Em DP 1, ou SPD Classe I no texto aplicado a navios aliviadores, admite-se que uma falha singela possa levar à perda de posição. Em DP 2 e em SPD Classe II, essa perda não deve ocorrer por falha simples em componente ou sistema ativo. Em DP 3, o mesmo critério é estendido também a componentes ou sistemas estáticos, elevando a exigência da arquitetura.

Fatos/trechos: petroles:petroles-004c2afadba7ea17c7dd7908:pNone:w56704500#f0, petroles:petroles-004c2afadba7ea17c7dd7908:pNone:w56704500#f3, hse:hse-04d3623c0070fad00a0b82db:p42:w20000#f1, hse:hse-04d3623c0070fad00a0b82db:p41:w19750#f3, hse:hse-04d3623c0070fad00a0b82db:p41:w19750#f4

### Princípio de funcionamento e mecanismo

A arquitetura de redundância busca impedir que uma única falha derrube simultaneamente as funções necessárias ao posicionamento, especialmente controle, geração e distribuição elétrica e acionamentos dos propulsores. Nos navios aliviadores, redundâncias nesses subsistemas são aplicadas para reduzir o risco de blecaute e de perdas abruptas de posição e, se a falha ainda ocorrer, preservar margem de manobra ou capacidade residual de posicionamento. Para atender ao critério de falha simples da classe 2, normalmente é preciso redundar todos os componentes ativos; na classe 3, a prática indicada é redundar todos os componentes e ainda separá-los fisicamente. Assim, a classe não depende só da existência de equipamentos duplicados, mas de uma arquitetura em que uma falha simples não elimine toda a capacidade de manter estação. O desempenho requerido após a falha é manter posição por tempo suficiente para encerrar com segurança a atividade em curso.

Fatos/trechos: petroles:petroles-004c2afadba7ea17c7dd7908:pNone:w56704500#f1, hse:hse-04d3623c0070fad00a0b82db:p41:w19750#f5, hse:hse-04d3623c0070fad00a0b82db:p40:w19500#f0, hse:hse-04d3623c0070fad00a0b82db:p42:w20000#f2

### Problemas típicos, sintomas e causas

A perda de posição após uma falha simples tem significados operacionais diferentes conforme a classe declarada da embarcação. Em uma unidade Classe I, esse resultado é compatível com o critério da classe; já em Classe II ou DP 2, a mesma ocorrência associada a componente ou sistema ativo indica que a redundância esperada não estava disponível ou não estava efetiva frente ao cenário de falha simples. Se a unidade for DP 3, a análise deve abranger também componentes estáticos, porque essa classe pressupõe que uma falha simples neles igualmente não provoque perda de posição. Em operações muito próximas de unidades ancoradas, a falha na geração de energia dos propulsores é um cenário particularmente crítico porque remove a capacidade de reação dinâmica, razão pela qual podem ser necessárias âncoras de segurança como salvaguarda adicional.

Fatos/trechos: petroles:petroles-004c2afadba7ea17c7dd7908:pNone:w56704500#f0, petroles:petroles-004c2afadba7ea17c7dd7908:pNone:w66350500#f3, hse:hse-04d3623c0070fad00a0b82db:p42:w20000#f0, hse:hse-04d3623c0070fad00a0b82db:p42:w20000#f1, hse:hse-04d3623c0070fad00a0b82db:p42:w20000#f2

### Decisões, ações e critérios

A seleção da classe e do nível de redundância deve ser compatível com a consequência da perda de posição e com a necessidade de manter a estação pelo tempo necessário para terminar a operação com segurança. Nas operações de alívio, o aumento de desconexões de emergência em terminais de aproamento fixo e FPSOs com ancoragem espalhada impulsionou a elevação dos requisitos de segurança, redundância e potência instalada dos navios aliviadores. O critério prático não é apenas evitar a falha inicial, mas assegurar que reste capacidade de manobra suficiente para desconectar com segurança o cabo de amarração e o mangote de transferência. Com essa capacidade residual, ganha-se tempo para afastar o navio aliviador do terminal oceânico, realizar reparos e reduzir a probabilidade de derramamento de óleo ou colisão entre as unidades. Quando a operação ocorre muito próxima de unidade ancorada, o emprego de âncoras de segurança passa a ser uma decisão de salvaguarda adicional diante da possibilidade de perda de geração dos propulsores.

Fatos/trechos: petroles:petroles-004c2afadba7ea17c7dd7908:pNone:w56721000#f2, petroles:petroles-004c2afadba7ea17c7dd7908:pNone:w56704500#f2, petroles:petroles-004c2afadba7ea17c7dd7908:pNone:w66350500#f3, hse:hse-04d3623c0070fad00a0b82db:p40:w19500#f0, hse:hse-04d3623c0070fad00a0b82db:p41:w19750#f3

### Segurança e riscos

Os riscos centrais tratados por essa arquitetura são blecaute, perda abrupta de posição, desconexão de emergência, colisão entre unidades e derramamento de óleo. A redundância em sistemas vitais existe para diminuir a probabilidade de que uma falha simples evolua diretamente para esses eventos. Quando a falha supera a barreira de prevenção, a barreira seguinte é manter margem de manobra ou capacidade residual de posicionamento suficiente para uma desconexão controlada e o afastamento do aliviador. Em operações de proximidade, âncoras de segurança podem funcionar como salvaguarda complementar contra a perda de empuxo decorrente de falha de geração.

Fatos/trechos: petroles:petroles-004c2afadba7ea17c7dd7908:pNone:w56704500#f1, petroles:petroles-004c2afadba7ea17c7dd7908:pNone:w56704500#f2, petroles:petroles-004c2afadba7ea17c7dd7908:pNone:w66350500#f3

### Divergências e limites das fontes

Há diferença de escopo entre as fontes. O texto sobre navios aliviadores usa a nomenclatura SPD Classe I e II para discutir requisitos e evolução operacional em operações de alívio, enquanto as fontes HSE/IMO descrevem DP Classes 1, 2 e 3 como classes de equipamento definidas por diretrizes e regras de classificação. As duas linhas convergem no critério de que a classe intermediária não deve perder posição por falha simples em componente ou sistema ativo. As fontes HSE/IMO explicitam ainda uma classe superior que inclui também componentes estáticos e a necessidade usual de separação física, ponto que não aparece no trecho sobre SPD Classe II. Portanto, a comparação entre SPD e DP aqui é técnica e de critério de falha, respeitando o contexto próprio de cada fonte.

Fatos/trechos: petroles:petroles-004c2afadba7ea17c7dd7908:pNone:w56704500#f3, hse:hse-04d3623c0070fad00a0b82db:p42:w20000#f1, hse:hse-04d3623c0070fad00a0b82db:p41:w19750#f3, hse:hse-04d3623c0070fad00a0b82db:p42:w20000#f2

### Alvos avaliáveis

- facil: Diferenciar DP 1/SPD Classe I, DP 2/SPD Classe II e DP 3 pelo efeito permitido de uma falha simples sobre a manutenção de posição.
- facil: Explicar por que DP 2 normalmente requer redundância de todos os componentes ativos.
- media: Relacionar redundância em geração, distribuição de energia e controle dos propulsores com a redução do risco de blecaute e de perda abrupta de posição.
- media: Justificar o uso de âncoras de segurança quando uma unidade DP opera muito próxima de outra unidade ancorada.
- dificil: Avaliar se a perda de posição após falha simples em componente ou sistema ativo é compatível com a classe declarada da embarcação e o que isso indica sobre perda de redundância.
- dificil: Integrar classe de DP/SPD, potência instalada, capacidade residual de posicionamento e meios de salvaguarda para decidir se há margem suficiente para desconexão segura e afastamento do aliviador.

## Integridade de hawsers, chafe chains e acessórios de amarração no offloading em tandem

ID: `01c1c3db6e:a11:k5`; subtópico: Operação de Offloading; coleções: bsee, hse, petroles, regis

Na estação de alívio de um FPSO, a confiabilidade do hawser e dos acessórios associados depende tanto do projeto e da qualidade de fabricação quanto da disciplina de estiva, manuseio, inspeção e descarte. O material mostra que falhas de integridade podem nascer de degradação acelerada por manuseio inadequado ou de defeitos metalúrgicos e de especificação capazes de provocar ruptura catastrófica abaixo da carga esperada.

### O que é e para que serve

Na operação de offloading em tandem, a estação de alívio do FPSO reúne facilidades de bombeio e transferência de óleo e facilidades de amarração do navio aliviador. Seu projeto de engenharia, fabricação e manutenção devem ser conduzidos para atender plenamente esse modo operacional com mangote de transferência flutuante. No sistema de amarração, o hawser trabalha com acessórios nas extremidades, incluindo trechos de chafe chain para travamento nos mordentes das embarcações. Como a integridade do sistema de offloading abrange os tanker mooring hawsers e a durabilidade do cabo depende também de estiva e manuseio adequados, a gestão de integridade precisa alcançar o cabo, os acessórios associados e as facilidades usadas para sua estiva e manuseio.

Fatos/trechos: petroles:petroles-004c2afadba7ea17c7dd7908:pNone:w56723250#f1, hse:hse-8ae5be797e5471d76a0aa410:p8:w2500#f2, trecho:petroles:petroles-004c2afadba7ea17c7dd7908:pNone:w56723500

### Princípio de funcionamento e mecanismo

Em um arranjo de amarração, todos os componentes do caminho de carga trabalham em série; assim, a confiabilidade do conjunto tende a ser limitada pelo elo mais fraco ou mais degradado. Estiva inadequada, enrolamento sem controle, arraste, esmagamento e impactos tendem a introduzir abrasão, dobramento localizado e dano superficial, mecanismos que aceleram perda de vida útil em cabos e podem iniciar trincas ou entalhes em acessórios metálicos. Já na metalurgia de sockets, shackles e correntes, tenacidade insuficiente reduz a capacidade do material de absorver energia antes de fraturar, aumentando a probabilidade de ruptura brusca sob carregamento dinâmico. Por isso, integridade mecânica depende ao mesmo tempo de projeto do arranjo, qualidade de fabricação, disciplina de manuseio e critérios claros de inspeção e descarte.

Base: conhecimento geral marcado.

### Variáveis e condições operacionais

A política de integridade do sistema de offloading deve considerar recomendações do fabricante, guias da indústria e fatores específicos da instalação, como condições meteoceanográficas, tipo de carga e número de operações. O material de incidente mostra que especificações desatualizadas ou inadequadas e requisitos de teste insuficientes ou não seguidos enfraquecem a capacidade de demonstrar que o componente atende à demanda de uso. Além disso, o modo como o equipamento é transportado, instalado, estivado e manuseado também influencia o desempenho: a ausência de facilidades adequadas para estiva e manuseio do hawser reduz de forma importante sua durabilidade, e o próprio manuseio durante a instalação pode expor acessórios críticos a danos. Assim, a política de integridade não se limita ao componente fabricado, mas precisa incorporar também as condições reais de uso e de manuseio.

Fatos/trechos: petroles:petroles-004c2afadba7ea17c7dd7908:pNone:w56723500#f1, hse:hse-8ae5be797e5471d76a0aa410:p8:w2500#f2, trecho:bsee:bsee-2388ad71df5cf1eba3badeeb:p1:w250

### Problemas típicos, sintomas e causas

Dois padrões de falha merecem ser separados no diagnóstico. Quando a vida útil do hawser cai de forma acentuada, uma causa forte é deficiência de estiva e manuseio, porque o material disponível associa diretamente a falta dessas facilidades à redução da durabilidade. Já uma ruptura catastrófica de socket ou shackle com carga inferior à especificada aponta para outra família causal: procedimento de fabricação defeituoso, tratamento térmico inadequado e metal com tenacidade abaixo do necessário; em paralelo, especificações desatualizadas, testes inadequados ou não cumpridos e danos de manuseio na instalação precisam ser verificados. A distinção entre esses cenários depende de examinar as evidências de fabricação e testes, as condições de manuseio na instalação e as condições de estiva e manuseio adotadas na operação.

Fatos/trechos: petroles:petroles-004c2afadba7ea17c7dd7908:pNone:w56723500#f1, bsee:bsee-2388ad71df5cf1eba3badeeb:p1:w250#f0, trecho:bsee:bsee-2388ad71df5cf1eba3badeeb:p1:w250

### Decisões, ações e critérios

As decisões de engenharia e operação devem partir do princípio de que projeto, fabricação e manutenção da estação de alívio precisam atender plenamente ao offloading em tandem com mangote flutuante; portanto, facilidades de estiva e manuseio do hawser fazem parte da solução de confiabilidade do sistema. No texto citado do HSE para FPSO/FSU, a integridade do sistema de offloading é baseada em política de inspeção, manutenção, testes, recertificação e retirada de serviço dos componentes, ajustada às recomendações do fabricante, à orientação da indústria e às condições específicas da instalação. Para o carregamento, um critério explícito é distribuir os esforços uniformemente entre as amarras e manter o esforço em cada elemento dentro de 55% do esforço máximo de rotura recomendado pela OCIMF. Na aquisição e aceitação de componentes críticos, as lições de incidente apontam para revisar especificações, incluir requisitos suficientes de ensaio Charpy, definir requisitos adequados de ensaios destrutivos e não destrutivos e garantir que os corpos de prova sejam representativos do material produzido; além disso, requisitos de manuseio e inspeção devem evitar danos em transporte e instalação. Essas decisões conectam a base de projeto da estação a uma política de integridade voltada à redução da probabilidade de falha catastrófica no caminho de carga.

Fatos/trechos: petroles:petroles-004c2afadba7ea17c7dd7908:pNone:w56723250#f1, hse:hse-8ae5be797e5471d76a0aa410:p8:w2500#f2, regis:regis-ca0681d6e9dec6eaf72dc259:pNone:w58000#f3, trecho:bsee:bsee-2388ad71df5cf1eba3badeeb:p1:w250

### Valores, faixas e limites citados

O único valor explícito no material é a recomendação da OCIMF de que os esforços sejam distribuídos de forma uniforme pelas amarras e que o esforço em cada uma não exceda 55% do esforço máximo de rotura do elemento. Esse valor é adimensional, expresso como porcentagem da capacidade de ruptura, e vale como critério recomendatório para elementos de amarração no contexto citado. Operacionalmente, ele exige avaliar não só a carga total do sistema, mas também como essa carga se reparte entre os componentes, porque concentração de esforço em um único trecho pode violar o critério mesmo com demanda global aparentemente moderada.

Fatos/trechos: regis:regis-ca0681d6e9dec6eaf72dc259:pNone:w58000#f3

### Divergências e limites das fontes

As fontes têm naturezas diferentes e isso muda o peso de cada uma na tomada de decisão. O texto do HSE descreve um requisito de gestão de integridade aplicável à jurisdição do Reino Unido, a recomendação da OCIMF fornece um critério técnico de indústria para carregamento, e os casos analisados por MMS e U.S.C.G. nos Estados Unidos são lições de incidente sobre fabricação, especificação, testes e manuseio. Elas não têm a mesma força normativa nem o mesmo escopo, mas convergem em um ponto operacional: a integridade de hawsers e acessórios não pode ser inferida apenas da carga nominal, porque depende do ciclo completo de projeto, fabricação, manuseio, inspeção e descarte.

Fatos/trechos: hse:hse-8ae5be797e5471d76a0aa410:p8:w2500#f2, regis:regis-ca0681d6e9dec6eaf72dc259:pNone:w58000#f3, bsee:bsee-2388ad71df5cf1eba3badeeb:p1:w250#f0

### Alvos avaliáveis

- facil: Explicar por que facilidades adequadas de estiva e manuseio aumentam a durabilidade do hawser na operação de offloading.
- facil: Identificar quais dimensões devem compor a política de integridade do sistema de offloading: inspeção, manutenção, testes, recertificação e retirada de serviço.
- media: Relacionar condições meteoceanográficas, tipo de carga e número de operações com a política de integridade dos componentes de amarração no referencial citado.
- media: Aplicar o critério de distribuição uniforme de esforços e o limite de 55% do esforço máximo de rotura por elemento na avaliação de carregamento das amarras.
- dificil: Distinguir um caso de vida útil reduzida por estiva e manuseio inadequados de um caso de falha catastrófica abaixo da carga especificada por defeito de fabricação, baixa tenacidade ou testes inadequados.
- dificil: Definir critérios de aquisição, aceitação e retirada de serviço que integrem base de projeto da estação de alívio, recomendações do fabricante, histórico operacional, requisitos de ensaio e prevenção de dano em transporte e instalação.

## Compatibilização da sequência de tanques e do lastro com estabilidade e esforços globais do casco

ID: `567fdce5c3:a02:k5`; subtópico: Operação de tanques de carga, lastro, sistema gás inerte, ventilação e estabilidade; coleções: hse, petroles

A operação de enchimento, esvaziamento, transferência interna e offloading não pode ser definida apenas pelo objetivo logístico de mover volume entre tanques. A ordem das etapas e o plano de lastro precisam ser verificados contra critérios de trim, estabilidade e integridade estrutural, inclusive nas condições intermediárias. Guias operacionais e ferramentas de cálculo servem justamente para transformar cada etapa proposta em uma condição verificável antes da execução.

### O que é e para que serve

A orientação operacional de trim e estabilidade existe para guiar o comandante e os demais responsáveis na carga, transferência e descarga de carga e lastro em terminais flutuantes. Essa orientação deve incluir exemplos de condições carregadas, transitórias e lastreadas ao longo de toda a faixa de calados operacionais, sempre acompanhadas dos critérios de estabilidade aplicáveis. Com esse conjunto de referência, o pessoal responsável consegue avaliar a estabilidade intacta e também a estabilidade em avaria de qualquer condição de carregamento que venha a ser proposta. O material indica ainda que essas informações podem ser emitidas em livreto separado de trim e estabilidade, inseridas no manual operacional ou incorporadas ao instrumento de carregamento.

Fatos/trechos: petroles:petroles-004c2afadba7ea17c7dd7908:pNone:w45247250#f0

### Princípio de funcionamento e mecanismo

A ordem de enchimento, esvaziamento e transferência interna altera a distribuição longitudinal e transversal de massa da unidade a cada etapa da operação. Como o casco é sustentado pela flutuação ao longo do seu comprimento, qualquer desequilíbrio temporário entre pesos e empuxo modifica trim, banda e margens de estabilidade, além de gerar esforços internos sob a forma de esforço cortante e momento fletor. Por isso, uma sequência operacional segura não é definida apenas pela condição inicial e pela condição final dos tanques; as condições intermediárias também precisam permanecer aceitáveis. O lastro funciona como variável de compensação para manter a condição hidrostática e a distribuição de cargas dentro do envelope estrutural e de estabilidade durante a transição.

Base: conhecimento geral marcado.

### Variáveis e condições operacionais

As verificações requeridas abrangem condições carregadas, transitórias e lastreadas em toda a faixa de calados operacionais, o que mostra que o desempenho da sequência depende do estágio exato da operação e não apenas do inventário final de tanques. O material sobre ferramenta de cálculo informa que é possível criar condições de carregamento e executar, para cada uma delas, os cálculos de equilíbrio e de estabilidade intacta. Isso dá base para representar separadamente as etapas de carregamento, transferência interna, descarga ou ajuste de lastro que alterem de forma relevante o arranjo de pesos. Essa abordagem permite verificar uma condição proposta fora dos exemplos do guia, desde que ela seja comparada com os critérios de estabilidade previstos.

Fatos/trechos: petroles:petroles-004c2afadba7ea17c7dd7908:pNone:w45247250#f0, petroles:petroles-004c2afadba7ea17c7dd7908:pNone:w7650750#f2

### Problemas típicos, sintomas e causas

Durante a operação de lastro, uma divergência entre a condição esperada e a condição observada não deve ser tratada apenas como questão de cálculo de estabilidade. No caso relatado pela HSE, a possibilidade de operar os sistemas sem transferência formal de controle entre uma estação e outra já havia gerado confusão e, em uma ocorrência, resultou em adernamento perceptível. No mesmo contexto operacional, o seguimento dos planos de carregamento e descarga de lastro é apresentado como necessário para evitar esforços excessivos na estrutura, com confirmação no programa de estabilidade. Assim, quando a condição real se afasta da prevista, a verificação operacional precisa abranger tanto a transferência correta de controle entre estações quanto a aderência ao plano e à condição simulada.

Fatos/trechos: hse:hse-04d3623c0070fad00a0b82db:p13:w4750#f3, trecho:hse:hse-04d3623c0070fad00a0b82db:p13:w4750

### Decisões, ações e critérios

Operacionalmente, a tripulação define um plano de carregamento que estabelece a sequência de enchimento dos tanques, e o material afirma que essa sequência é importante para que os limites de tensão estrutural do navio não sejam atingidos. De forma análoga, planos de carregamento e descarga de lastro eram mantidos e sempre seguidos porque se entendia que desvios desses planos poderiam levar a momentos fletores e/ou esforços cortantes excessivos na estrutura da embarcação. No exemplo de boa prática descrito pela HSE, o programa de estabilidade era usado para confirmar que as manobras permaneciam dentro de parâmetros estritos; quando um desvio era necessário, como no caso de tanque aberto para inspeção, os requisitos eram modificados e simulados antes da execução. O mesmo exemplo relata a conferência manual regular do conteúdo dos tanques para validar os dados automaticamente atualizados no computador de estabilidade, o que mostra que a decisão correta combina plano formal, simulação prévia e verificação em campo.

Fatos/trechos: hse:hse-04d3623c0070fad00a0b82db:p13:w4750#f3, petroles:petroles-4ee4bce16acf674505c8912d:pNone:w15604500#f0, trecho:hse:hse-04d3623c0070fad00a0b82db:p13:w4750

### Alvos avaliáveis

- facil: Identificar a função do guia de trim e estabilidade na avaliação de operações de carga, transferência, descarga e lastro.
- facil: Reconhecer que a sequência de enchimento dos tanques faz parte do plano de carregamento e existe para evitar atingir limites de tensão estrutural.
- media: Explicar por que as verificações devem cobrir condições carregadas, transitórias e lastreadas em toda a faixa de calados operacionais.
- media: Descrever o papel da ferramenta de cálculo na criação de condições de carregamento e na execução dos cálculos de equilíbrio e estabilidade intacta para cada etapa relevante.
- dificil: Diante da indisponibilidade de um tanque para inspeção, definir que a sequência e os requisitos de lastro/carga devem ser modificados e simulados no programa de estabilidade antes da execução.
- dificil: Diante de diferença entre a condição prevista e a observada durante o lastro, decidir verificar a transferência correta de controle entre estações, a aderência ao plano de lastro e a condição confirmada no programa de estabilidade.

## Perguntas reais do experimento

### q002 · pedido facil · medido facil

**Pergunta:** Por que facilidades adequadas de estiva e manuseio aumentam a durabilidade do hawser na operação de offloading?

**Resposta:** Facilidades adequadas de estiva e manuseio aumentam a durabilidade do hawser porque reduzem os danos mecânicos introduzidos no uso normal do cabo. Quando a estiva é deficiente ou o manuseio é feito com arraste, enrolamento sem controle, esmagamento ou impactos, surgem abrasão, dobramento localizado e danos superficiais que aceleram a perda de vida útil. Essas mesmas condições também podem danificar acessórios associados, especialmente durante transporte e instalação. Por isso, a durabilidade do hawser depende não só do seu projeto e fabricação, mas também das condições reais de estiva e manuseio oferecidas pela instalação.

### q003 · pedido facil · medido media

**Pergunta:** O que explica o insucesso no esvaziamento dos slops de boreste e do tanque 6C com a bomba de stripping?

**Resposta:** O esvaziamento não foi eficaz porque havia comunicação indesejada entre compartimentos. Existia comunicação entre os tanques de slop e também entre o slop de bombordo e o tanque 6C. Nessa condição, a bomba de stripping não conseguia promover a retirada efetiva do líquido como previsto, porque os tanques deixavam de se comportar como volumes isolados. Assim, a dificuldade estava na comunicação entre tanques, e não apenas no desempenho da bomba.

**Observação da análise:** depende do episódio do tanque 6C sem fornecer suas condições. O rótulo de dificuldade não detectou esse problema de autonomia. Não usar a QA como está.

### q021 · pedido dificil_B · medido dificil

**Pergunta:** Após um evento de ingresso de água em uma unidade flutuante, a equipe para bombas, executa o isolamento inicial das linhas e confirma o fechamento comandado das válvulas acessíveis. Mesmo assim, ao longo das horas o trim continua aumentando, e os níveis indicam que a água atingiu mais de um espaço, sem comportamento compatível com um único compartimento já estabilizado. Qual diagnóstico deve ser priorizado antes de decidir novo contralastro, e por que esse quadro pode indicar continuidade de comunicação com o mar e perda da compartimentação real, e não apenas falha de bombeamento?

**Resposta:** O diagnóstico prioritário é verificar se ainda existe caminho hidráulico passivo entre o mar e o interior da unidade e, em paralelo, se a estanqueidade real entre compartimentos foi degradada. Parar bombas e isolar redes não garante o fim do alagamento, porque a admissão de água do mar pode ocorrer por gravidade e continuar por sucções, caixas de mar, válvulas de costado ou tubulações comprometidas que permaneçam comunicando com o mar. Se o trim continua se alterando e a água alcança múltiplos espaços, o quadro é compatível com alagamento progressivo ativo ou com perda de confinamento por acessos, aberturas ou fronteiras estanques degradadas, fazendo a unidade responder como se a avaria abrangesse uma região maior que a prevista. Isso também pode contrariar a filosofia nominal fail-close, indicando que o isolamento efetivo não foi obtido ou que o ingresso ocorre por outra via, como respiros ou aberturas sem proteção eficaz. Antes de aplicar contralastro, é necessário confirmar a eliminação da comunicação com o mar e redefinir a compartimentação realmente preservada, porque a resposta de estabilidade depende do volume efetivamente ainda estanque e não apenas do arranjo assumido no estudo original.
