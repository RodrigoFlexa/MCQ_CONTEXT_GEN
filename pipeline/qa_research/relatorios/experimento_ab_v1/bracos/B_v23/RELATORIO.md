# Geração v22

Braço B_v23: 301 questões finais de 1137 propostas (9 recusadas pela régua, 353/1128 aprovadas pelo auditor, 52 redundantes).

Chamadas do gerador: 524, das quais 14 sem questões; questões por chamada: {0: 14, 1: 160, 2: 144, 3: 135, 4: 71}.
Falhas do auditor por verificação: {'atalho': 661, 'varias_respostas': 154, 'nao_unico': 6, 'depende_do_documento': 15, 'fora_da_fonte': 32}.
Segunda chance: 112 revisitas de foco após visita sem ganho (41 conhecimentos novos); 37 segundas tentativas de composta (10 finais).
Conhecimentos novos por rodada: {1: 109, 2: 69, 3: 43, 4: 18, 5: 11}; focos por número de visitas: {2: 35, 3: 38, 4: 32, 5: 21}.
Tipos finais: {'procedimento': 41, 'decisao': 96, 'consequencia': 8, 'mecanismo': 49, 'diagnostico': 95, 'conceito': 12}.
Falhas pendentes: 0.

## Amostra de questões finais

**[02_02 · decisao · janela]** Na ampliação da água de injeção de um FPSO, a nova etapa de desoxigenação precisa caber em área muito restrita, com limite de peso, partida rápida após paradas e menor sensibilidade ao balanço da unidade. Qual rota de desaeração tende a ser mais adequada?

- Resposta: Desaeração por membranas com contatores de fibras ocas.
- Explicação: Com restrição de área e peso, necessidade de modularidade, partida rápida e menor efeito das ondas, a rota por membranas reúne as vantagens operacionais destacadas para FPSO.

**[02_02 · diagnostico · janela]** Duas campanhas lidam com a mesma água sulfatada e a mesma água rica em bário. Numa, a incrustação aparece em equipamentos de superfície; noutra, só no poço. Qual variável do arranjo do sistema explica essa mudança do ponto crítico de deposição?

- Resposta: O local de mistura entre as correntes.
- Explicação: Com as mesmas águas incompatíveis, o que desloca onde a supersaturação nasce é o ponto em que elas primeiro se encontram.

**[07_01 · diagnostico · janela]** Numa malha de controle, o sinal do controlador varia continuamente, a válvula fica um tempo parada, depois dá um salto de posição e a variável de processo repete esse padrão mesmo sem novo distúrbio externo. Que comportamento dinâmico tende a se estabelecer na malha?

- Resposta: Ciclo limite.
- Explicação: O stick-slip introduz movimento descontínuo e pode manter ciclos repetitivos mesmo sem novo estímulo. Isso é efeito típico de stiction, diferente do hunting sustentado por instabilidade.

**[02_02 · mecanismo · janela]** Num sistema de água produzida, a remoção de óleo cai depois que um pré-tratamento passa a reter finos minerais; ao mesmo tempo, o potencial zeta da água quase não se altera com o coagulante. Qual interação antes favorecida por esse químico deixou de contribuir para a separação?

- Resposta: Aproximação entre gotas de óleo e sólidos por espécies catiônicas.
- Explicação: Além de reduzir repulsão, o coagulante pode mediar contato entre gotas e sólidos. Ao retirar os finos, perde-se essa via de agregação e captura.

**[02_02 · mecanismo · janela]** Na recuperação convencional de MEG, o MEG pobre opera próximo da saturação de NaCl, surgem incrustações em superfícies quentes, o glicol regenerado escurece e a demanda de make-up cresce. Qual mecanismo específico de perda de glicol explica melhor esse quadro?

- Resposta: Degradação térmica do MEG.
- Explicação: No bloco foco, saturação de NaCl no MEG pobre está associada a incrustação e perda de MEG por degradação térmica. O escurecimento em zonas quentes incrustadas é compatível com essa via.

**[03_03 · mecanismo · janela]** Durante crude oil washing simultâneo ao offloading, qual mecanismo físico faz a atmosfera do tanque depender mais da inertização contínua do que numa descarga sem lavagem?

- Resposta: Renovação intensificada da interface líquido-vapor pelos jatos de aspersão.
- Explicação: No COW, óleo cru seco retorna por bicos de aspersão e renova mais a superfície exposta ao espaço de vapor, aumentando a troca e a dependência do suprimento contínuo de gás inerte.

**[03_03 · diagnostico · janela]** Durante transferência por rota alternativa que reaproveita linha de outra função, a vazão líquida se mantém estável, mas surgem oscilações de pressão em tanques não diretamente ligados à movimentação do líquido. Que caminho técnico novo deve ser verificado?

- Resposta: Interligação dos espaços de vapor entre tanques.
- Explicação: Ao reutilizar linhas de outra função, podem surgir novos caminhos de vapor; pressão anormal em tanques fora da rota líquida aponta para acoplamento gasoso entre espaços de tanque.

**[07_01 · decisao · janela]** Em uma substituição emergencial de um laço de temperatura, o cartão disponível aceita diretamente o sinal primário do elemento sensor em milivolts, sem transmissor de campo. Que tipo de sensor deve ser escolhido para compatibilizar o arranjo?

- Resposta: Termopar.
- Explicação: Quando o sistema recebe diretamente milivolts do elemento, o sensor compatível é o que gera tensão termoelétrica. RTD responde por variação de resistência e exige condicionamento apropriado.

**[02_02 · decisao · janela]** Após partidas e correções, um sistema com oxidante passa a apresentar ataque concentrado no carretel de injeção, embora em operação contínua a dose nominal seja baixa e o residual médio a jusante fique na meta. Ao revisar o arranjo de armazenamento e manuseio, qual condição de dosagem deve ser usada como base?

- Resposta: A máxima concentração local plausível no ponto de aplicação.
- Explicação: O dano aparece onde o oxidante atinge o metal antes da diluição completa. Em oxidantes, a severidade depende do local de aplicação e dos transitórios, não apenas do regime contínuo nominal.

**[02_02 · diagnostico · janela]** Depois de encher o tanque de serviço e colocar a bomba dosadora em operação, curso, frequência e pulsação de descarga permanecem normais; o tanque perde nível, porém o residual medido a jusante do ponto de injeção quase não aumenta. Que caminho hidráulico específico explica melhor essa perda de dosagem efetiva?

- Resposta: Linha de recirculação aberta retornando ao tanque de serviço.
- Explicação: Se a dosadora desloca produto e o tanque esvazia, mas o residual após a injeção não sobe, o químico está retornando por recirculação em vez de seguir ao processo.

**[02_02 · decisao · janela]** Um depósito orgânico confirmado como asfáltico foi tratado com a mesma mistura solvente antes eficaz para parafina; na campanha, só a fração mais macia se removeu e o núcleo aderido permaneceu. O que deve ser reespecificado no solvente antes de repetir a limpeza?

- Resposta: A composição do solvente.
- Explicação: A química do solvente determina a solvência sobre o depósito. Mistura adequada à parafina pode não dissolver asfaltenos, mesmo com mais volume ou contato.

**[02_02 · mecanismo · composta]** Na água de injeção com desaeração mecânica seguida de dosagem de bissulfito, a cloração da captação foi reforçada. Depois disso, com a mesma taxa de bissulfito, apareceram oxidante residual e maior corrosividade a jusante, embora o O2 dissolvido medido na saída da etapa mecânica continue na faixa habitual. Qual mecanismo específico explica esse desvio?

- Resposta: Subdosagem efetiva do bissulfito por consumo com cloro residual no ponto de aplicação.
- Explicação: Com a carga de O2 após a etapa mecânica inalterada, o novo consumo do bissulfito vem do cloro sobrevivente à cloração. Isso reduz a fração disponível para remover O2 e deixa oxidante residual a jusante.

**[02_02 · decisao · composta]** Um desemulsificante foi escolhido em bottle test por mostrar maior separação visível de fases. Na operação, a exportação de petróleo permaneceu dentro do controle, mas o óleo na água produzida tratada continuou sendo a limitação. Ao refazer a comparação de bancada para essa aplicação, qual indicador deve decidir a escolha do produto?

- Resposta: Clarificação da fase aquosa.
- Explicação: Se a limitação operacional está na água produzida, o indicador do ensaio deve representar esse ponto. Em emulsões óleo-em-água, o bottle test avalia desempenho pela clarificação da fase aquosa, não pela água liberada do petróleo.

**[02_02 · procedimento · janela]** Num poço com teor de água variável e emulsão na produção, o squeeze é acompanhado por fósforo. Para que a curva de liberação seja confiável, de qual corrente a amostra precisa ser representativa?

- Resposta: Da água produzida.
- Explicação: O retorno do inibidor é acompanhado na fase aquosa; amostra do fluido total pode distorcer o residual e a interpretação da liberação.

**[02_02 · procedimento · janela]** Após um choque com biocida de consumo rápido, o residual medido a jusante zera. Para distinguir consumo químico completo do ativo de uma subinjeção, que verificação independente da resposta microbiológica deve ser feita?

- Resposta: Balanço estequiométrico do ativo.
- Explicação: Quando a necessidade é confirmar dosagem, e não resposta biológica, o balanço relaciona a massa de ativo injetada com a demanda química capaz de consumir o produto.
