# Experimento de refino: refinador fraco x forte

Origem: `pipeline/qa_research/relatorios/teste_v19_20261024T053346Z/geracao` (92 aprovadas). Candidatas: 153 originais reprovadas pelo auditor, por motivo: {'reformula_enunciado': 16, 'varias_respostas': 58, 'trivial': 41, 'tecnicamente_errada': 2, 'resposta_vaga': 10, 'lista_generica': 5, 'caso_especifico': 9, 'prudencia_generica': 12}.
Prompt `refinador_v3.md` (todos os motivos, histórico das versões reprovadas, exemplos aprovados do mesmo tipo); nova auditoria com o auditor v3 e o texto-fonte; ganho líquido depois da deduplicação por sentido contra as aprovadas da origem: conta só a recuperada com conhecimento que as aprovadas não cobrem (uma por grupo de recuperadas equivalentes). Braços `_cob` recebem as aprovadas sobre os mesmos blocos.

| Braço | modelo | recuperadas | ganho líquido | por rodada (aprov./reescritas/tentadas, descartadas) |
|---|---|---|---|---|
| mini | gpt-5-mini-petrobras:medium | 85/153 | **40** (92 → 132) | r1: 50/153/153, desc. 0; r2: 35/103/103, desc. 0 |
| forte | gpt-5-4-petrobras:high | 122/153 | **24** (92 → 116) | r1: 86/153/153, desc. 0; r2: 36/67/67, desc. 0 |
| forte_cob | gpt-5-4-petrobras:high | 96/153 | **54** (92 → 146) | r1: 68/153/153, desc. 0; r2: 28/85/85, desc. 0 |

Referência: na rodada de origem, o refinador antigo (gpt-5-mini, prompt v19, só motivos recuperáveis) teve 25 aprovadas de 98 reescritas, já descontadas a deduplicação e a revisão manual.

## mini

- Recuperadas por motivo original: {'reformula_enunciado': '8/16', 'varias_respostas': '36/58', 'trivial': '20/41', 'tecnicamente_errada': '2/2', 'resposta_vaga': '4/10', 'lista_generica': '1/5', 'caso_especifico': '8/9', 'prudencia_generica': '6/12'}
- Por origem: {'composta': 16, 'janela': 69}; tipo mudou em 22
- Ganho líquido por tópico: {'03_03': 20, '07_03': 20}
- Conhecimento novo por rodada: {2: 17, 1: 23}; repetem conhecimento já aprovado: {2: 18, 1: 27}
- Rodada 1, motivos do auditor nas reescritas: {'trivial': 21, 'nenhum': 50, 'varias_respostas': 31, 'reformula_enunciado': 13, 'lista_generica': 9, 'fora_da_fonte': 17, 'caso_especifico': 2, 'tecnicamente_errada': 4, 'prudencia_generica': 5, 'sim_nao_disfarcado': 1}
- Rodada 2, motivos do auditor nas reescritas: {'nenhum': 35, 'fora_da_fonte': 18, 'reformula_enunciado': 10, 'varias_respostas': 25, 'lista_generica': 3, 'caso_especifico': 1, 'trivial': 5, 'tecnicamente_errada': 4, 'prudencia_generica': 2}

### Amostra de recuperadas

**[03_03 · varias_respostas · consequencia → consequencia · r1]**
- Antes: Durante um offloading, um tanque de carga inertizado permaneceu em descarga. Nesse intervalo, o suprimento de gás inerte se perdeu por alinhamento incorreto, e a tendência de pressão do tanque passou a cair. Considerando esse quadro, que consequência específica pode ocorrer no interior do tanque? → Entrada de ar no tanque, porque a queda de pressão durante a descarga sem gás inerte mantido pode permitir o ingresso de ar.
- Depois: Durante offloading, um tanque de carga inertizado permaneceu em descarga e perdeu o suprimento de gás inerte por alinhamento incorreto; a pressão do tanque passou a cair. Qual consequência específica e imediata para a atmosfera interna do tanque decorre diretamente dessa perda de inertização e queda de pressão? → Entrada de ar no espaço de vapor do tanque, por insuficiência de pressão de gás inerte que permite o ingresso de ar.

**[07_03 · trivial · consequencia → consequencia · r1]**
- Antes: Em um FPSO, o CMMS segue emitindo ordens sistemáticas, mas vários equipamentos têm TAG incompleta, materiais genéricos e fechamentos de ordens com evidência de execução desigual no histórico. Sem saneamento prévio do cadastro, a equipe quer usar esse histórico para calcular MTBF e comparar períodos de operação. Nessa situação, que condição técnica deve ser atribuída a esses indicadores? → Tecnicamente frágeis, porque esse histórico não sustenta MTBF confiável nem comparação consistente entre períodos.
- Depois: Em um FPSO, o CMMS continua gerando ordens sistemáticas, mas muitos equipamentos têm TAG incompleta, materiais genéricos e fechamentos de ordens com evidência de execução desigual. Sem saneamento do cadastro, a equipe pretende usar esse histórico para calcular MTBF e comparar períodos. Nessa situação, que condição técnica deve ser atribuída a esses indicadores para fins de MTBF e comparação entre períodos? → Inadequados para cálculo de MTBF e comparações quantitativas; dados não padronizados e não distinguem eventos de falha/recuperação, exigindo saneamento prévio.

**[03_03 · reformula_enunciado · conceito → conceito · r1]**
- Antes: Que fenômeno térmico deve ser considerado como cenário de sobrepressão quando um líquido fica confinado em volume fechado? → Expansão térmica do líquido confinado.
- Depois: Que componente do sistema de tanques é projetado para liberar gás e evitar sobrepressurização por expansão térmica de líquido confinado? → Dispositivo de vent e alívio automático do tanque.

**[03_03 · varias_respostas · conceito → mecanismo · r2]**
- Antes: Em sistemas associados aos tanques de carga, que modo de falha de válvula pode causar perda de contenção? → Passagem indesejada.
- Depois: Por que a falha de válvula que permite fluxo quando deveria interrompê‑lo é considerada um mecanismo de perda de contenção em FPSO? → Porque permite liberação de hidrocarbonetos e perda de estanqueidade, criando risco de vazamento, ingresso de atmosfera perigosa e escalada de falhas.

**[07_03 · trivial · conceito → conceito · r2]**
- Antes: Qual abordagem permite avaliar a manutenção simultaneamente por segurança, saúde, meio ambiente, custo de manutenção e perda de produção? → Abordagem multicritério.
- Depois: Que técnica analítica inclui avaliação da criticidade dos modos de falha para priorizar estratégias e periodicidade de manutenção? → FMECA — Análise dos Modos de Falha, seus Efeitos e Criticidade; classifica criticidade das falhas para priorizar estratégias e periodicidades de manutenção.

**[03_03 · resposta_vaga · consequencia → consequencia · r1]**
- Antes: Se a ventilação dos tanques for integrada ao sistema de gás inerte na mesma rede, qual efeito operacional tende a aparecer nas mudanças de modo? → Restrição de operabilidade, com menor flexibilidade porque a rede precisa atender funções diferentes em modos distintos.
- Depois: Se a ventilação dos tanques for integrada ao sistema de gás inerte na mesma rede, que efeito operacional tende a aparecer durante as transições entre modos operacionais? → Redução da flexibilidade operacional: exigência de segregação e múltiplos alinhamentos ao mudar de modo, alongando transições e aumentando risco de alinhamentos indevidos ou contaminação cruzada.

**[03_03 · trivial · consequencia → consequencia · r1]**
- Antes: Mantidas as demais condições do projeto, o que acontece com a capacidade da malha de acompanhar variações de pressão do tanque se a válvula é comissionada apenas como totalmente aberta ou fechada? → A malha perde a modulação prevista e passa a atuar apenas nos extremos.
- Depois: Durante carregamento ou descarga, com variações graduais de vazão, se a válvula de vent prevista para controle de posição for comissionada apenas como totalmente aberta ou fechada, qual consequência operacional imediata sobre a pressão interna do tanque tende a ocorrer e que risco isso acarreta? → Perda da regulação fina da pressão, gerando oscilações que podem acionar dispositivos de alívio, aumentar emissões e elevar o risco de sobrepressão/vácuo com potencial dano à integridade.

**[03_03 · caso_especifico · consequencia → mecanismo · r2]**
- Antes: Se a unidade entrar no arranjo previsto para operação sem produção de óleo, para onde o condensado deve seguir após a desidratação? → Para exportação por gasoduto.
- Depois: Quando a unidade adota o arranjo de operação sem produção de óleo, que princípio operacional explica por que a destinação do condensado após desidratação pode mudar? → A seleção de rotas conforme o modo operacional e a disponibilidade dos sistemas associados: se o processamento/exportação de óleo estiver inativo, o condensado segue a rota compatível disponível (ex.: gasoduto).

**[07_03 · trivial · mecanismo → diagnostico · r1]**
- Antes: Por que o tempo total indisponível de um item pode ser maior que o MTTR de reparo na mesma falha? → Porque soma esperas logísticas e administrativas fora dos intervalos de reparo contados no MTTR.
- Depois: Por que o tempo total indisponível de um item pode exceder o MTTR apurado para a mesma falha, e que registro permite identificar essas contribuições extras? → Esperas logísticas e administrativas não incluídas no MTTR; registrar consistentemente início da falha, início/fim das esperas e retorno à função.

**[07_03 · varias_respostas · conceito → conceito · r1]**
- Antes: Que sistema de informação, junto com dados de disponibilidade e confiabilidade, sustenta análises para identificar componentes com falhas e definir intervalos de manutenção? → Sistema de codificação de falhas.
- Depois: Que sistema de informação uniformiza o registro de falhas para permitir análises por modo e causa e, com dados de disponibilidade e confiabilidade, sustenta a definição de intervalos de manutenção? → Sistema de codificação de falhas.

**[03_03 · varias_respostas · decisao → decisao · r2]**
- Antes: Em um FPSO, no stripping final de um tanque de carga, a bomba segue operando, mas a retirada deixa de avançar com pequeno volume remanescente. O problema não apareceu com o tanque mais cheio, e não há assinatura dominante de descarga estrangulada, como elevação persistente de pressão de descarga, nem trip da bomba. Que ação operacional específica deve ser tentada para recuperar o esgotamento? → Alterar o trim, para favorecer o escoamento do remanescente até a sucção.
- Depois: Em um FPSO, durante o stripping final de um tanque de carga a bomba opera sem trip e sem assinatura de descarga estrangulada. Inspeção indica pequeno bolsão de líquido localizado no extremo longitudinal do tanque, diretamente oposto à tubulação de sucção (remanescente na área de popa enquanto a sucção está a vante). Que ação operacional específica deve ser tentada para recuperar o esgotamento? → Alterar o trim bombeando lastro fore/aft para aproximar o bolsão remanescente da sucção, monitorando estabilidade e limites estruturais.

**[07_03 · caso_especifico · procedimento → mecanismo · r1]**
- Antes: Em FPSOs e FSUs, como o backlog de inspeção estrutural e marítima deve aparecer nos relatórios do backlog geral? → Com visibilidade própria dentro do backlog geral, separada das demais ordens para acompanhamento.
- Depois: Por que o backlog de inspeção estrutural e marítima em FPSOs e FSUs deve ter visibilidade própria dentro do backlog geral? → Para evitar diluição e adiamentos repetidos que aumentam risco à estanqueidade, estabilidade e contenção, permitindo priorização e aplicação de medidas compensatórias rastreáveis.

**[07_03 · varias_respostas · procedimento → procedimento · r2]**
- Antes: Durante o planejamento de uma intervenção, a ação proposta contraria a documentação técnica existente e não há padrão de engenharia que a cubra. Como a liberação técnica deve ser conduzida? → Com análise de engenharia e aprovação de profissional habilitado antes da execução.
- Depois: Durante o planejamento de uma intervenção cuja ação contraria a documentação técnica e não há padrão de engenharia que a cubra, que elemento decisivo a liberação técnica deve exigir antes da execução? → Análise de engenharia documentada e aprovação por profissional habilitado antes da execução.

**[07_03 · prudencia_generica · procedimento → conceito · r2]**
- Antes: Depois de priorizar pela criticidade quais falhas merecem atenção, como a MCC/RCM deve escolher a política de manutenção? → Segundo a natureza do modo de falha e a consequência para o sistema.
- Depois: Num item crítico cuja falha tem consequência inaceitável, mas cujo início produz sinais previsíveis e mensuráveis antes da perda funcional, qual elemento técnico decisivo a MCC/RCM deve usar para optar por manutenção por condição em vez de programada ou reativa? → Detectabilidade/preditibilidade do modo de falha — se o início for previsível e mensurável por monitoramento confiável, favorece manutenção por condição.

**[07_03 · varias_respostas · decisao → conceito · r2]**
- Antes: Em um FPSO, uma intervenção para recolocar um equipamento crítico em serviço não tem cobertura clara na documentação técnica nem nos procedimentos vigentes. Ela será executada a bordo por equipe embarcada e contratada, em condição não usual, e parte da equipe propõe repetir uma prática informal já usada em campo. Que documento deve estar disponível no local antes da execução? → Plano específico disponível na locação, porque a execução local em condição não usual e sem cobertura documental não deve seguir prática informal.
- Depois: Em um FPSO, uma intervenção para recolocar um equipamento crítico em serviço não está coberta pelo manual operacional nem por procedimentos vigentes e será executada a bordo em condição não usual. Que decisão-documento deve existir e estar aprovado antes de autorizar a execução? → Análise de engenharia aprovada por profissional habilitado.

## forte

- Recuperadas por motivo original: {'reformula_enunciado': '13/16', 'varias_respostas': '46/58', 'trivial': '35/41', 'tecnicamente_errada': '1/2', 'resposta_vaga': '9/10', 'lista_generica': '3/5', 'caso_especifico': '7/9', 'prudencia_generica': '8/12'}
- Por origem: {'composta': 18, 'janela': 104}; tipo mudou em 70
- Ganho líquido por tópico: {'03_03': 11, '07_03': 13}
- Conhecimento novo por rodada: {1: 16, 2: 8}; repetem conhecimento já aprovado: {1: 70, 2: 28}
- Rodada 1, motivos do auditor nas reescritas: {'nenhum': 86, 'varias_respostas': 26, 'prudencia_generica': 3, 'trivial': 17, 'reformula_enunciado': 19, 'caso_especifico': 2}
- Rodada 2, motivos do auditor nas reescritas: {'reformula_enunciado': 8, 'trivial': 11, 'nenhum': 36, 'varias_respostas': 7, 'prudencia_generica': 4, 'lista_generica': 1}

### Amostra de recuperadas

**[03_03 · varias_respostas · diagnostico → mecanismo · r1]**
- Antes: Num FPSO monohull, durante carregamento e descarga, o teor de O2 de um tanque inertizado sobe nos períodos de maior movimento da embarcação e volta a estabilizar quando a solicitação diminui. A pressão e a qualidade do gás inerte no header permanecem normais; a linha conectada ao tanque foi testada estanque e não houve manobra de ventilação. Que causa específica explica melhor esse comportamento? → Abertura de trinca estrutural existente por tensões cíclicas, permitindo ingresso de oxigênio.
- Depois: Num FPSO monohull, o teor de O2 de um tanque inertizado sobe nos períodos de maior movimento durante carregamento/descarga e volta a cair quando a solicitação diminui. O gás inerte no header está normal e não houve ventilação. Que mecanismo de integridade explica melhor essa correlação? → Perda de estanqueidade em defeito pré-existente; as tensões cíclicas do casco podem abrir ou propagar o dano e permitir ingresso de ar no tanque.

**[03_03 · resposta_vaga · procedimento → mecanismo · r2]**
- Antes: Durante uma contingência, uma corrente será redirecionada para um tanque de função diferente da usual. Qual verificação técnica deve preceder o alinhamento para preservar a segregação funcional? → A verificação de compatibilidade entre a corrente, o tanque e o circuito associado.
- Depois: Por que a estanqueidade das válvulas é indispensável para que a bomba de stripping retire efetivamente o líquido do tanque de origem? → Vedação deficiente cria retorno interno ou comunicação indevida entre tanques, e parte da vazão deixa de ser retirada efetiva do tanque de origem.

**[07_03 · varias_respostas · procedimento → decisao · r1]**
- Antes: Durante o planejamento de uma intervenção, a ação proposta contraria a documentação técnica existente e não há padrão de engenharia que a cubra. Como a liberação técnica deve ser conduzida? → Com análise de engenharia e aprovação de profissional habilitado antes da execução.
- Depois: Durante o planejamento de uma intervenção, a solução proposta diverge da documentação técnica existente e não está coberta por procedimento ou padrão de engenharia. Que condição técnica mínima deve ser atendida antes da execução? → Análise de engenharia com aprovação de profissional habilitado antes da execução.

**[03_03 · varias_respostas · procedimento → procedimento · r1]**
- Antes: Como devem ser configurados o suprimento de gás inerte e a ventilação dos tanques das duas embarcações durante o offloading? → Segundo a arquitetura aprovada de cada embarcação, sem presumir compartilhamento de gás inerte nem ausência total de emissões.
- Depois: Durante o offloading entre FPSO e aliviador, qual critério deve orientar o alinhamento do suprimento de gás inerte e da ventilação dos tanques? → A arquitetura aprovada de cada embarcação; o arranjo deve seguir o sistema real, sem presumir compartilhamento de gás inerte nem ausência total de emissões.

**[07_03 · lista_generica · procedimento → diagnostico · r2]**
- Antes: Em FPSOs em vida tardia, como o sistema de integridade deve redefinir o programa de inspeção diante de ameaças de envelhecimento e fim de vida? → Ajustando escopo, metodologia e frequência de inspeção à idade e à condição do vaso.
- Depois: Num FPSO em envelhecimento, as inspeções de campo seguem ocorrendo, mas o volume de dados cresce, a avaliação das anomalias atrasa e o backlog de inspeção não reduz. Que falha técnica explica esse padrão? → Gestão e análise descontínuas dos dados de inspeção, que sobrecarregam a capacidade de resposta e dificultam reduzir o backlog.

**[07_03 · trivial · mecanismo → mecanismo · r1]**
- Antes: Por que o tempo total indisponível de um item pode ser maior que o MTTR de reparo na mesma falha? → Porque soma esperas logísticas e administrativas fora dos intervalos de reparo contados no MTTR.
- Depois: Por que comparar MTBF ou MTTR entre equipamentos só faz sentido quando as populações analisadas são tecnicamente compatíveis? → Porque misturar funções, regimes ou modos de falha diferentes reúne comportamentos distintos num único valor e distorce a comparação de confiabilidade.

**[03_03 · trivial · mecanismo → mecanismo · r1]**
- Antes: Por que manter pressão positiva controlada durante a inertização limita a entrada de ar no tanque? → Porque a pressão interna acima da externa faz o fluxo tender para fora, reduzindo a infiltração de ar por aberturas e vazamentos.
- Depois: No crude oil washing, o que faz a atmosfera do tanque ficar mais dependente da inertização contínua do que no offloading sem lavagem? → A aspersão de óleo cru intensifica a renovação da superfície líquido-vapor, tornando a atmosfera do tanque mais dependente do suprimento contínuo de gás inerte.

**[07_03 · trivial · conceito → conceito · r1]**
- Antes: Na manutenção de um FPSO, qual é o principal produto da programação semanal de curto prazo? → O plano de trabalho para a equipe executante.
- Depois: Que função o plano mestre cumpre na manutenção preventiva antes da programação semanal no FPSO? → Fornecer horizonte e visibilidade da manutenção preventiva para posterior programação executável.

**[03_03 · reformula_enunciado · procedimento → procedimento · r1]**
- Antes: Ao preparar uma rota alternativa que usará uma linha de outro serviço, como a contenção dessa rota deve ser confirmada antes da operação? → Por verificação de estanqueidade da rota alternativa.
- Depois: Ao preparar uma rota alternativa com linha originalmente de outro serviço, a estanqueidade já foi comprovada. Que análise técnica ainda deve ser feita antes da operação? → Mapear os novos caminhos de líquido e vapor e seus efeitos sobre inventário, pressões e comunicação entre sistemas.

**[07_03 · trivial · consequencia → mecanismo · r1]**
- Antes: Em um FPSO, passam a existir sobressalentes críticos a bordo, melhor acessibilidade ao equipamento e apoio mais organizado, sem mudar projeto, aplicação ou ambiente do componente. O que acontece com a disponibilidade? → Ela aumenta, pela redução do tempo de recuperação e da indisponibilidade total.
- Depois: Em um FPSO, passam a existir sobressalentes críticos a bordo, melhor acessibilidade ao equipamento e apoio mais organizado, sem mudar projeto, aplicação ou ambiente do componente. Por que essas mudanças podem elevar a disponibilidade sem alterar o comportamento de falha observado? → Redução do MTTR e das esperas de retorno: a função é restabelecida mais rápido após a falha, sem mudar os mecanismos físicos que determinam o MTBF.

**[03_03 · reformula_enunciado · mecanismo → mecanismo · r1]**
- Antes: Por que uma liberação para armazenar condensado estabilizado em tanque de carga não pode ser estendida automaticamente a outra composição, temperatura ou duração de estocagem? → Porque a avaliação foi feita sob condição termodinâmica específica e período limitado; alterando essas premissas, ela deixa de valer.
- Depois: Por que variar a composição, a temperatura ou o tempo de estocagem pode invalidar uma avaliação que liberou armazenagem temporária de condensado estabilizado em tanque de carga? → Porque essas variáveis mudam a condição termodinâmica e a compatibilidade do armazenamento com tanque, linhas, válvulas, ventilação e monitoramento considerados na avaliação.

**[03_03 · trivial · conceito → mecanismo · r2]**
- Antes: Qual elemento da compartimentação do FPSO deve confinar fluidos em caso de dano ou inundação para limitar a escalada do evento? → Compartimentos estanques.
- Depois: Por que uma trinca estrutural em um tanque de carga sob gás inerte pode criar condição insegura mesmo sem vazamento visível de líquido? → Cria caminho para ingresso de oxigênio no tanque, degradando a atmosfera segura mantida pelo sistema de gás inerte.

**[07_03 · varias_respostas · conceito → mecanismo · r1]**
- Antes: Como se chama a limitação operacional que impede concluir a manutenção planejada por falta de especialidade, sobressalente ou liberação de parada? → Ponto de estrangulamento.
- Depois: Por que campanhas de manutenção ajudam a reduzir backlog quando várias pendências compartilham acesso, recurso especializado ou a mesma indisponibilidade operacional? → Porque o agrupamento reduz remobilizações e melhora o aproveitamento da janela de execução.

**[03_03 · varias_respostas · consequencia → mecanismo · r1]**
- Antes: Durante um offloading, um tanque de carga inertizado permaneceu em descarga. Nesse intervalo, o suprimento de gás inerte se perdeu por alinhamento incorreto, e a tendência de pressão do tanque passou a cair. Considerando esse quadro, que consequência específica pode ocorrer no interior do tanque? → Entrada de ar no tanque, porque a queda de pressão durante a descarga sem gás inerte mantido pode permitir o ingresso de ar.
- Depois: Durante o crude oil washing em um tanque de carga, por que é essencial manter suprimento positivo de gás inerte ao vaso durante toda a operação? → A renovação intensa da interface líquido-vapor; ela aumenta a dependência da atmosfera do tanque da inertização contínua.

**[07_03 · varias_respostas · diagnostico → mecanismo · r1]**
- Antes: Em um FPSO, vários itens manuteníveis do mesmo conjunto entram na mesma janela. O plano prevê retirar cada item separadamente, com reaberturas sucessivas do conjunto e maior indisponibilidade total, embora o risco avaliado do conjunto permaneça o mesmo. Qual causa técnica do planejamento explica melhor esse resultado? → Falta de estruturação hierárquica de equipamentos e instalações, impedindo agrupar as intervenções por função.
- Depois: Por que a estruturação hierárquica de equipamentos e instalações ajuda a reduzir a indisponibilidade quando vários itens manuteníveis de um mesmo conjunto precisam ser tratados na mesma janela? → Porque permite agrupar intervenções por função no mesmo conjunto, evitando retiradas individuais e reaberturas sucessivas que aumentam a indisponibilidade sem reduzir mais o risco.

## forte_cob

- Recuperadas por motivo original: {'reformula_enunciado': '7/16', 'varias_respostas': '39/58', 'trivial': '26/41', 'tecnicamente_errada': '1/2', 'resposta_vaga': '8/10', 'lista_generica': '2/5', 'caso_especifico': '7/9', 'prudencia_generica': '6/12'}
- Por origem: {'composta': 16, 'janela': 80}; tipo mudou em 68
- Ganho líquido por tópico: {'03_03': 22, '07_03': 32}
- Conhecimento novo por rodada: {2: 24, 1: 30}; repetem conhecimento já aprovado: {2: 4, 1: 38}
- Rodada 1, motivos do auditor nas reescritas: {'reformula_enunciado': 35, 'nenhum': 68, 'varias_respostas': 24, 'trivial': 14, 'lista_generica': 2, 'resposta_vaga': 3, 'prudencia_generica': 3, 'caso_especifico': 4}
- Rodada 2, motivos do auditor nas reescritas: {'nenhum': 28, 'lista_generica': 3, 'varias_respostas': 14, 'trivial': 14, 'reformula_enunciado': 17, 'caso_especifico': 4, 'prudencia_generica': 2, 'resposta_vaga': 2, 'fora_da_fonte': 1}

### Amostra de recuperadas

**[03_03 · trivial · mecanismo → mecanismo · r1]**
- Antes: Por que manter pressão positiva controlada durante a inertização limita a entrada de ar no tanque? → Porque a pressão interna acima da externa faz o fluxo tender para fora, reduzindo a infiltração de ar por aberturas e vazamentos.
- Depois: Durante inspeção, o analisador de oxigênio do gás inerte responde corretamente, mas o alarme de alto oxigênio permaneceu com o mesmo setpoint após mudança do modo operacional. Por que isso pode deixar o sistema inadequadamente protegido? → Porque o setpoint antigo pode alarmar tarde: o oxigênio já terá ultrapassado o critério do novo modo antes da resposta operacional prevista.

**[07_03 · trivial · consequencia → decisao · r1]**
- Antes: Em um FPSO, passam a existir sobressalentes críticos a bordo, melhor acessibilidade ao equipamento e apoio mais organizado, sem mudar projeto, aplicação ou ambiente do componente. O que acontece com a disponibilidade? → Ela aumenta, pela redução do tempo de recuperação e da indisponibilidade total.
- Depois: Num FPSO, a criticidade, o modo de falha dominante e as consequências da perda de função já foram definidos, e o histórico fornece MTBF, MTTR e disponibilidade. A equipe quer escolher a periodicidade preventiva só com esses indicadores. Que verificação técnica da própria ação proposta ainda falta? → A eficácia real da intervenção proposta sobre o modo de falha.

**[07_03 · trivial · conceito → mecanismo · r1]**
- Antes: Na manutenção de um FPSO, qual é o principal produto da programação semanal de curto prazo? → O plano de trabalho para a equipe executante.
- Depois: Em um FPSO, por que o plano mestre de manutenção não basta, por si só, para definir o trabalho da semana seguinte? → A programação semanal converte o horizonte do plano mestre em intervenções executáveis sob restrições reais de operação, acesso, materiais, recursos, janela climática e liberação operacional.

**[03_03 · varias_respostas · mecanismo → mecanismo · r1]**
- Antes: Por que o histórico do fluido armazenado precisa ser considerado antes de manutenção e inspeção em tanque? → Porque ele condiciona a atmosfera interna e a presença de água ou depósitos que podem sustentar dano corrosivo oculto.
- Depois: Em áreas de produção e armazenamento com água produzida e depósitos, falhas no controle de SRB vieram acompanhadas de aumento de H2S. Como isso agrava a integridade além do risco toxicológico? → Alteração dos mecanismos corrosivos; o H2S gerado pelas SRB intensifica a corrosão, sobretudo na presença de água produzida e depósitos.

**[03_03 · reformula_enunciado · decisao → conceito · r2]**
- Antes: Em um FPSO, um tanque de carga que continha óleo cru foi lavado e depois purgado com gás inerte para inspeção interna. A equipe quer liberar a entrada porque o tanque já está fora de serviço. Nos registros, porém, não aparece conclusão do gas freeing com ar fresco nem medições atmosféricas de liberação. Que preparação atmosférica ainda falta antes da entrada? → Gas freeing/ventilação com ar fresco, seguido de verificação atmosférica de liberação; a purga com gás inerte não torna o tanque apto à entrada.
- Depois: Durante a preparação de um tanque inertizado para retorno ao serviço, análises confirmam baixo teor de oxigênio no gás fornecido e na atmosfera interna. Na revisão de prontidão, que salvaguarda ainda precisa estar disponível antes da liberação? → Proteção contra sobrepressão e vácuo do tanque; baixo teor de oxigênio controla a composição, mas não protege contra desvios de pressão.

**[03_03 · trivial · consequencia → mecanismo · r1]**
- Antes: Num FPSO, um tanque de carga já estava em nível muito alto quando a transferência para reduzi-lo passou a apresentar vazão oscilante e pouca resposta na indicação de nível do tanque de origem, apesar de a bomba de stripping seguir em operação. Diante disso, a equipe passou a cogitar manobra para outro tanque. Nesse quadro, como fica a margem disponível contra perda de contenção? → A margem disponível contra perda de contenção está reduzida, porque o tanque segue muito alto enquanto a retirada efetiva ficou menor que a necessária.
- Depois: Numa transferência interna por stripping, a bomba segue em operação e há escoamento na descarga, mas o nível do tanque de origem responde pouco. Como a vedação deficiente de válvulas pode produzir esse efeito? → Retorno interno ou comunicação indevida entre tanques, desviando parte da vazão e reduzindo a retirada efetiva do tanque de origem.

**[07_03 · reformula_enunciado · mecanismo → diagnostico · r2]**
- Antes: Por que a manutenção corretiva planejada pode ser tecnicamente aceitável em equipamento de baixa criticidade, quando a função pode ser recomposta após a falha? → Porque a perda temporária da função é tolerável ou recuperável sem impacto desproporcional, e a recomposição após a falha limita a consequência.
- Depois: Na revisão do plano de um item crítico do FPSO, os modos de falha já foram identificados, mas a equipe não consegue sustentar se a intervenção preventiva deve ocorrer em semanas ou meses. Que base técnica está faltando para definir essa periodicidade? → Dados de confiabilidade do item, especialmente seu histórico de falha, para sustentar o intervalo preventivo.

**[03_03 · trivial · mecanismo → mecanismo · r1]**
- Antes: Por que o monitoramento do gás inerte precisa confirmar a capacidade de resposta dos alarmes, e não só o teor de oxigênio? → Porque só um alarme responsivo detecta a subida de oxigênio acima do aceitável a tempo de acionar a resposta operacional prevista.
- Depois: Por que, numa inspeção do sistema de gás inerte, não basta comprovar que o alarme de alto O2 soa quando estimulado; é preciso confirmar também o ponto de atuação e a resposta operacional prevista? → Da salvaguarda completa: sem ponto de atuação adequado ao modo e resposta operacional definida, o alarme só anuncia o desvio e pode não impedir gás fora de especificação.

**[07_03 · resposta_vaga · conceito → mecanismo · r2]**
- Antes: Qual condição das populações analisadas é necessária para comparar indicadores de confiabilidade? → Compatibilidade técnica entre as populações analisadas.
- Depois: Um item reparável passou vários dias indisponível por espera logística entre falhas. Por que usar o tempo corrido do período, em vez do tempo efetivamente operado, distorce o MTBF observado? → Porque o MTBF usual usa o tempo de operação acumulado; incluir paradas no numerador eleva artificialmente o indicador.

**[03_03 · tecnicamente_errada · diagnostico → diagnostico · r1]**
- Antes: Após manutenção em um tanque de carga inertizado, surgiram deformações localizadas em chapas. Na inspeção, havia evidência de isolamento incorreto ou reinstalação inadequada na rota de vent/alívio. O tanque possuía vent automático e monitoramento com alarme de pressão. Nesse quadro, que falha adicional explica tecnicamente o dano estrutural? → Falha do alarme de pressão ou ausência de resposta ao alarme, pois o vent automático torna insuficiente atribuir a deformação apenas ao bloqueio do vent.
- Depois: Em um FPSO, um tanque de carga inertizado está em descarga contínua. O nível cai como previsto, a rota de vent/alívio está disponível e, ainda assim, a pressão do tanque cai progressivamente até vácuo. Que falha técnica explica melhor esse comportamento? → Reposição insuficiente de gás inerte: a vazão ou a pressão de IG não acompanham o volume retirado na descarga.

**[07_03 · varias_respostas · decisao → mecanismo · r1]**
- Antes: Em um FPSO em vida tardia, a degradação cresce, o programa de inspeção ficou para trás e campanhas sucessivas geram grande volume de dados. O backlog de inspeção aumenta, diagramas e referências de integridade deixam de acompanhar os achados, e a proposta da equipe é ampliar ainda mais a coleta. Para restaurar a eficácia da gestão de corrosão e integridade, que presença técnica contínua deve ser estabelecida? → Presença continuada de engenheiro de inspeção ou função equivalente, para preservar conhecimento do ativo, atualizar diagramas e converter achados em ações executadas.
- Depois: Em um FPSO em vida tardia, a degradação cresce, o programa de inspeção atrasou e novas campanhas ampliam o volume de dados. Mesmo assim, diagramas e referências de integridade deixam de acompanhar os achados e o backlog aumenta. Por que ampliar ainda mais a coleta não tende a resolver esse quadro? → Sobrecarga da capacidade contínua de análise e resposta, porque sem gerir os dados com continuidade eles não viram atualização do conhecimento do ativo nem ações executadas.

**[03_03 · caso_especifico · conceito → mecanismo · r2]**
- Antes: Qual cabeçalho de gás inerte é usado na inertização inicial de um tanque previamente gas free antes da introdução de óleo? → Clean inert gas header.
- Depois: Em uma instalação em que a ventilação dos tanques compartilha a rede de gás inerte, por que a mudança de carregamento para descarga tende a restringir a operabilidade? → Porque no carregamento a rede alivia a atmosfera excedente, e na descarga repõe gás inerte para manter pressão positiva; uma única linha limita esses caminhos independentes.

**[07_03 · varias_respostas · consequencia → diagnostico · r1]**
- Antes: Em um FPSO, projetos offshore passam a consumir leitos, recursos especializados e capacidade das equipes de manutenção, além de gerar carga extra de reparos e recondicionamento. O que acontece com a manutenção planejada? → A manutenção planejada perde espaço para demandas concorrentes, favorecendo a formação de novo backlog.
- Depois: Numa unidade envelhecida, o programa de inspeção foi ampliado e o volume de relatórios cresceu. As inspeções de campo seguem ocorrendo, mas as respostas aos achados se acumulam e o backlog de inspeção não recua. Que mecanismo técnico explica esse quadro? → Sobrecarga da capacidade de gerir e analisar continuamente os dados de inspeção, limitando a resposta aos achados.

**[07_03 · reformula_enunciado · decisao → procedimento · r1]**
- Antes: Em um FPSO, o efetivo de manutenção embarcado é reduzido. Após intervenção, um sistema crítico que já possui monitoramento remoto voltou ao serviço, e a mesma equipe enxuta permanecerá na semana seguinte. A filosofia operacional da unidade já admite, para alguns ativos, distribuição das atividades técnicas além do efetivo embarcado. No período inicial de observação desse retorno, como deve ser estruturado o acompanhamento? → Acompanhamento onshore articulado com a equipe embarcada, aproveitando o monitoramento remoto no período inicial após a reentrada em serviço.
- Depois: Após intervenção em um equipamento crítico do FPSO, o ensaio local foi aprovado. Em operação, porém, sua função depende de permissivos, intertravamentos e suprimentos externos ao próprio equipamento. Que verificação deve complementar o retorno ao serviço? → Teste pós-manutenção das interfaces com processo, utilidades, automação e proteção, confirmando compatibilidade e estabilidade na operação inicial.

**[03_03 · varias_respostas · diagnostico → mecanismo · r1]**
- Antes: Num FPSO monohull, durante carregamento e descarga, o teor de O2 de um tanque inertizado sobe nos períodos de maior movimento da embarcação e volta a estabilizar quando a solicitação diminui. A pressão e a qualidade do gás inerte no header permanecem normais; a linha conectada ao tanque foi testada estanque e não houve manobra de ventilação. Que causa específica explica melhor esse comportamento? → Abertura de trinca estrutural existente por tensões cíclicas, permitindo ingresso de oxigênio.
- Depois: Por que falhas no controle de bactérias redutoras de sulfato em áreas de produção e armazenamento agravam também a integridade, além do risco toxicológico? → Porque elevam o H2S, que na presença de água produzida e depósitos altera e pode intensificar mecanismos corrosivos.
