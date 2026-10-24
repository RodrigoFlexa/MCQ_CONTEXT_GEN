# Geração completa (v18): uma passagem por janela e encadeamento, sem meta

Janela com o prompt v18 (sem decisão), compostas a partir dos encadeamentos, auditor v2 (com motivo) como filtro, refinador para defeitos recuperáveis e banco dinâmico de exemplos e contraexemplos.

**Total: 142 questões válidas em 2 tópicos.**

| Tópico | Tema | blocos | encadeamentos | passagens de janela | rodadas | válidas | meta | janela aprov. | compostas aprov. | refinadas aprov. |
|---|---|---|---|---|---|---|---|---|---|---|
| 05_01 | Sistema de utilidades | 25 | 23 | 25 | 1 | **72** | - | 52/100 | 14/23 | 6/29 |
| 06_01 | Sistema de Combate a Incêndio | 24 | 21 | 24 | 1 | **70** | - | 47/96 | 14/21 | 9/34 |

| Tipo | janela (aprov./geradas) | compostas (aprov./geradas) |
|---|---|---|
| conceito | 22/49 | 0/0 |
| mecanismo | 37/51 | 0/1 |
| consequencia | 8/30 | 13/23 |
| diagnostico | 18/24 | 8/11 |
| decisao | 0/0 | 7/9 |
| procedimento | 14/42 | 0/0 |

Por rodada (0 = compostas): r0: 30/52 (dup. 1); r1: 112/251 (dup. 1).
Motivos do auditor: {'janela': {'trivial': 30, 'nenhum': 100, 'varias_respostas': 30, 'tecnicamente_errada': 3, 'resposta_vaga': 7, 'lista_generica': 7, 'caso_especifico': 1, 'prudencia_generica': 8, 'reformula_enunciado': 10}, 'composta': {'nenhum': 29, 'trivial': 4, 'caso_especifico': 1, 'tecnicamente_errada': 2, 'resposta_vaga': 2, 'reformula_enunciado': 4, 'varias_respostas': 1, 'prudencia_generica': 1}, 'refinada': {'caso_especifico': 3, 'varias_respostas': 22, 'nenhum': 15, 'sim_nao_disfarcado': 1, 'reformula_enunciado': 5, 'tecnicamente_errada': 3, 'lista_generica': 2, 'trivial': 9, 'prudencia_generica': 2, 'resposta_vaga': 1}}.
Refinador: {'tentadas': 63, 'reescritas': 63, 'descartadas': 0, 'aprovadas_apos_refino': 15, 'por_motivo': {'reformula_enunciado': 14, 'resposta_vaga': 9, 'lista_generica': 7, 'varias_respostas': 31, 'caso_especifico': 2}}.
Banco dinâmico: {'aprovadas': 1180, 'reprovadas': 1549, 'herdadas': {'aprovadas': 1038, 'reprovadas': 1390}}. Falhas pendentes: 0.

## Amostra de aprovadas por tópico

### 05_01

**[diagnostico · composta]** Num FPSO, o sistema de água doce segue o arranjo tanque, bombas e vaso hidrofórico antes da distribuição. O nível do tanque permanece estável, as bombas estão disponíveis e pequenas variações de consumo passaram a gerar caça de pressão na rede e partidas frequentes. A instabilidade aparece a jusante do bombeamento. Que causa técnica explica melhor esse comportamento?

- Resposta: Perda da função de amortecimento do vaso hidrofórico, porque pequenas variações de demanda voltam a oscilar a rede e aumentar a frequência de partidas das bombas.

**[diagnostico · simples]** Num sistema fechado com header comum de ida e retorno, a bomba principal e a temperatura de suprimento permanecem estáveis. Ao alinhar um consumidor adicional, a temperatura em alguns consumidores sobe, enquanto outros quase não se alteram. Qual causa específica explica melhor esse comportamento?

- Resposta: Redistribuição de vazão entre ramais por mudança da resistência hidráulica do circuito comum.

**[consequencia · composta]** Em um FPSO, um circuito de água do mar de serviços recebe água com alta carga de fosfato, nitrogênio e sulfato. O residual de hipoclorito fica repetidamente abaixo do alvo, e a operação vem tratando o desvio apenas como risco de lodo e obstrução. Nesse quadro, que modo de dano também deve ser esperado no circuito?

- Resposta: Biocorrosão associada à atividade microbiana, porque a subdosagem recorrente em água rica em nutrientes sustenta atividade biológica além do simples biofouling.

**[diagnostico · simples]** Em um FPSO, pressão e qualidade do ar atendem em regime normal, mas, em toda manutenção planejada do compressor em operação, o suprimento cai durante toda a intervenção para consumidores essenciais e a operação é afetada. Qual causa específica do arranjo explica a recorrência?

- Resposta: Ausência de unidade em reserva para um serviço em que a perda de ar traz impacto operacional relevante.

### 06_01

**[mecanismo · simples]** Como funções de emergência podem aumentar a chance de estabilizar um incêndio combatido com água ou espuma?

- Resposta: Ao reduzir o inventário liberado e desligar equipamentos, diminuem a alimentação e a severidade do fogo, facilitando seu controle.

**[mecanismo · simples]** Por que a falha de uma linha de fluido perigoso e a degradação da rede de combate agravam o mesmo incêndio?

- Resposta: Porque a primeira aumenta a alimentação do fogo, enquanto a segunda reduz a capacidade hidráulica de combatê-lo.

**[consequencia · composta]** Em um FPSO, o padrão de desempenho de uma bomba de firewater na manutenção está descrito apenas como “operar adequadamente”. No teste executado, a bomba partiu e o relatório foi encerrado como “satisfatório”, sem indicar no relatório ou na ordem de serviço qualquer referência pré-estabelecida para julgar o resultado. Que conclusão técnica esse teste sustenta quanto ao atendimento do requisito?

- Resposta: Inconclusivo para demonstrar atendimento do requisito, porque “satisfatório” sem referência pré-estabelecida não comprova aceitação.

**[mecanismo · simples]** Por que falhas em componentes auxiliares podem impedir o combate mesmo quando bombas e linhas principais parecem disponíveis?

- Resposta: Porque elas interrompem a sequência de atuação do sistema; sem alimentação, válvulas, instrumentação, comutação ou distribuição funcionando, a água não chega ao ponto protegido.
