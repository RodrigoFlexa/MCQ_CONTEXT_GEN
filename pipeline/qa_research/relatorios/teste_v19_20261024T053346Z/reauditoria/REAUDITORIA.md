# Reauditoria das aprovadas com o auditor atual

Aprovadas antes: 132; continuam aprovadas: **99**.
Motivos: {'trivial': 13, 'nenhum': 99, 'varias_respostas': 11, 'reformula_enunciado': 7, 'caso_especifico': 1, 'tecnicamente_errada': 1}.
Por tópico (aprovadas agora / antes): {'05_01': '58/71', '06_01': '41/61'}.
Removidas na revisão manual: 10; o auditor v2 reprova **8** ({'reformula_enunciado': 3, 'trivial': 2, 'prudencia_generica': 1, 'varias_respostas': 2, 'nenhum': 2}).

## Amostra de reprovadas agora

**[06_01 · consequencia · reformula_enunciado]** Se um reparo temporário na rede de incêndio for aceito só pela estanqueidade em condição normal, sem memorial de cálculo nem comprovação para calor e fogo do serviço, o que pode ocorrer numa emergência?

- Resposta: O reparo pode perder contenção sob exposição térmica ou incêndio e indisponibilizar a rede.
- Auditor: A consequência só espelha o que o enunciado já sugeriu: sem comprovação para calor/fogo, o reparo falha sob calor/fogo.

**[05_01 · diagnostico · reformula_enunciado]** Em um sistema de água do mar de serviços, a perda de carga subiu, trocadores alimentados pela mesma água perderam desempenho térmico e surgiram obstruções em linhas e equipamentos. O quadro apareceu após um período de dosagem biocida abaixo do necessário, em água rica em nutrientes. Qual mecanismo de degradação explica melhor esses sinais?

- Resposta: Biofouling, decorrente de controle microbiológico insuficiente.
- Auditor: O enunciado já combina subdosagem de biocida, água rica em nutrientes e sintomas típicos; a referência apenas rotula isso como biofouling.

**[05_01 · mecanismo · reformula_enunciado]** Em um PSA de dois leitos, por que o produto permanece enriquecido no gás menos adsorvido enquanto a extremidade de saída do leito ainda tem capacidade de adsorção?

- Resposta: Porque o componente preferencialmente retido continua sendo removido pelo adsorvente antes de atingir a saída, mantendo a corrente de produto enriquecida no menos adsorvido.
- Auditor: A resposta apenas reescreve que ainda há capacidade na saída, o que já implica que o componente mais adsorvido não atingiu o produto.

**[05_01 · consequencia · varias_respostas]** Se o hipoclorito for aplicado em superdosagem no mesmo material e circuito, qual efeito se espera sobre a corrosão?

- Resposta: Aceleração da corrosão, porque a água se torna mais agressiva.
- Auditor: Sem especificar o material, a química detalhada e o regime do circuito, a consequência da superdosagem não é universal e há respostas distintas defensáveis.

**[06_01 · procedimento · varias_respostas]** Em um compartimento ocupado de FPSO protegido por agente gasoso, como a ocupação deve ser tratada quando o sistema for acionado?

- Resposta: Com evacuação prévia e restrição de entrada durante ou imediatamente no acionamento.
- Auditor: Para compartimentos ocupados com agentes gasosos, as medidas dependem do agente e do arranjo de segurança, de modo que evacuação e restrição de entrada não esgotam uma resposta única.

**[05_01 · consequencia · trivial]** Em um skid PSA de separação do ar, o licenciante especifica uma zeólita na qual a interação do N2 com os cátions da estrutura é favorecida. Considerando a etapa de adsorção em alta pressão, que corrente sai do leito como produto útil?

- Resposta: Corrente enriquecida em oxigênio na saída do leito, porque o N2 é o componente mais adsorvido nessa condição.
- Auditor: O enunciado já informa que o N2 é o componente mais adsorvido; concluir que o produto útil é a corrente enriquecida no outro componente sai por lógica direta.

**[06_01 · conceito · trivial]** Qual condição do ambiente térmico no ponto de ataque limita a utilidade operacional dos meios dirigidos de combate?

- Resposta: Carga térmica suportável pela equipe.
- Auditor: A limitação por carga térmica suportável pela equipe é praticamente a própria definição de tenabilidade no ponto de ataque.

**[06_01 · diagnostico · varias_respostas]** Num compartimento de FPSO protegido por agente gasoso, houve descarga do sistema, mas o fogo não foi controlado. Durante a resposta, constatou-se porta aberta e ventilação mantida. Qual causa do insucesso deve ser priorizada?

- Resposta: Perda da concentração extintora por falta de estanqueidade do compartimento.
- Auditor: Porta aberta e ventilação mantida são causas técnicas independentes e ambas podem explicar o insucesso, então a referência escolhe uma sem condição suficiente.

**[06_01 · conceito · varias_respostas]** Qual referência técnica deve ser mensurável para ligar o requisito do sistema de combate a incêndio à ordem de serviço?

- Resposta: Padrão de desempenho.
- Auditor: Sem contexto adicional, mais de um referencial técnico mensurável pode ligar requisito à ordem de serviço, como padrão de desempenho, critério de aceitação ou requisito funcional.

**[05_01 · consequencia · trivial]** Se a água captada passa a ter fosfato, nitrogênio e sulfato em grande quantidade, o que ocorre com a criticidade de uma subdosagem de hipoclorito?

- Resposta: Ela se torna mais crítica, com maior retomada do crescimento microbiológico.
- Auditor: Mais nutrientes tornando uma subdosagem de hipoclorito pior é consequência direta e previsível, sem exigir elaboração técnica relevante.

**[06_01 · mecanismo · reformula_enunciado]** Por que corrosão interna, crescimento marinho ou bloqueio de bicos comprometem a proteção de um sistema de dilúvio?

- Resposta: Porque restringem a distribuição do agente extintor justamente nos pontos que deveriam receber proteção.
- Auditor: A resposta só resume os próprios mecanismos já sugeridos no enunciado, convertendo corrosão, incrustação e bloqueio em 'restrição da distribuição do agente'.

**[06_01 · consequencia · trivial]** Durante teste da rede de incêndio em uma unidade offshore, as bombas partiram normalmente e o anel foi pressurizado. Inspeção encontrou incrustação e obstrução em trechos de tubulação, sem evidência de falha de partida. Que consequência operacional final essa condição ilustra?

- Resposta: Vazão/pressão insuficientes nos consumidores críticos, impedindo a entrega do agente extintor no local, no tempo e na condição necessários.
- Auditor: Obstrução e incrustação em rede de incêndio levarem a vazão e pressão insuficientes nos consumidores é efeito hidráulico básico.

**[06_01 · conceito · trivial]** Qual sistema complementar à rede ativa afeta sua sobrevivência por ter de comportar a água aplicada em emergência?

- Resposta: Drenagem.
- Auditor: A própria formulação 'comportar a água aplicada' conduz diretamente a drenagem, sem exigir conhecimento técnico distintivo.

**[06_01 · procedimento · varias_respostas]** Para um alvo específico no convés, como deve ser verificado o atendimento por um meio de aplicação dirigida de água ou espuma?

- Resposta: Pelo arranjo real e cenário do incêndio, confirmando alcance do alvo sem sombreamento excessivo, com acesso, visibilidade e comunicação.
- Auditor: A pergunta é ampla demais e admite métodos distintos de verificação, enquanto a referência vira uma checklist de aspectos sem procedimento único e exclusivo.

**[06_01 · conceito · varias_respostas]** Na estratégia de proteção de um FPSO, que papel a rede principal de incêndio exerce?

- Resposta: Barreira de mitigação da escalada do evento.
- Auditor: A pergunta admite vários papéis técnicos corretos para a rede principal de incêndio, e a referência fixa apenas um enquadramento abstrato.

**[06_01 · consequencia · trivial]** Em um FPSO, o padrão de desempenho de uma bomba de firewater na manutenção está descrito apenas como “operar adequadamente”. No teste executado, a bomba partiu e o relatório foi encerrado como “satisfatório”, sem indicar no relatório ou na ordem de serviço qualquer referência pré-estabelecida para julgar o resultado. Que conclusão técnica esse teste sustenta quanto ao atendimento do requisito?

- Resposta: Inconclusivo para demonstrar atendimento do requisito, porque “satisfatório” sem referência pré-estabelecida não comprova aceitação.
- Auditor: Concluir que o teste é inconclusivo na ausência de critério de aceitação pré-definido decorre de lógica geral de verificação, sem exigir conhecimento técnico específico do sistema.

**[06_01 · mecanismo · trivial]** Por que a falha de uma linha de fluido perigoso e a degradação da rede de combate agravam o mesmo incêndio?

- Resposta: Porque a primeira aumenta a alimentação do fogo, enquanto a segunda reduz a capacidade hidráulica de combatê-lo.
- Auditor: A resposta apenas explicita o óbvio: uma falha em linha de fluido alimenta o fogo e a degradação da rede reduz o combate.

**[06_01 · conceito · trivial]** Na rede de incêndio, qual condição distingue redundância real de mera duplicação de equipamentos?

- Resposta: Manter a função requerida mesmo após a falha de um elemento relevante.
- Auditor: A resposta praticamente enuncia a própria definição funcional de redundância, sem exigir elaboração técnica relevante.

**[05_01 · mecanismo · trivial]** Como um vaso hidrofórico adequadamente ajustado reduz a frequência de partidas das bombas quando a demanda oscila?

- Resposta: Amortecendo variações de pressão e demanda; assim, pequenas oscilações na rede não exigem partida imediata das bombas.
- Auditor: A resposta praticamente enuncia a função básica do vaso hidrofórico, sem trazer o mecanismo decisivo de volume tampão pela compressibilidade do gás.

**[05_01 · consequencia · trivial]** Num FPSO, os consumidores do processo são resfriados por água doce recirculante em circuito fechado, que troca calor com um circuito aberto de água do mar nos trocadores. Durante uma campanha, o residual de hipoclorito no circuito aberto ficou acima do previsto. Em que parte do sistema a corrosão tende a se acelerar?

- Resposta: Nos equipamentos e trechos do circuito aberto de água do mar, porque o arranjo fechado mantém os consumidores do processo fora do contato direto com essa água.
- Auditor: A resposta decorre quase diretamente do fato de apenas o circuito aberto estar em contato com a água do mar com hipoclorito elevado.

**[05_01 · mecanismo · varias_respostas]** Como a separação entre os ramos de instrumentos e de serviço permite atender consumidores com criticidades diferentes?

- Resposta: Porque cada ramo pode receber tratamento e armazenamento próprios, ajustando a qualidade do ar à sensibilidade do uso final.
- Auditor: A separação pode atender criticidades diferentes por vários mecanismos igualmente corretos, como isolamento de perturbações, pressões distintas e prioridade de suprimento, não só por tratamento e armazenamento próprios.

**[06_01 · conceito · tecnicamente_errada]** Em uma área ocupada de unidade offshore, quando se espera que pessoas permaneçam no local durante o acionamento de um sistema fixo com agente gasoso, qual é o elemento decisivo que deve orientar a seleção do agente?

- Resposta: Restrição de permanência de pessoas
- Auditor: A referência não aponta o critério técnico decisivo de seleção do agente para área ocupada, como toxicidade/limites de exposição humana, e fica imprecisa a ponto de induzir erro.

**[06_01 · consequencia · varias_respostas]** Em um FPSO, o sistema de água de combate a incêndio mantém bombas, tubulações e válvulas instaladas, mas há corrosão relevante na rede, relatos de bicos bloqueados, testes recentes pouco conclusivos e não conformidades críticas abertas há longo tempo. A equipe sustenta que o sistema “está lá” e “vem sendo testado”. Na avaliação da barreira durante uma emergência, que condição de disponibilidade deve ser considerada?

- Resposta: Funcionalmente indisponível, porque presença física com testes fracos e degradação persistente não demonstra efetividade do sistema na emergência.
- Auditor: Sem um critério explícito para classificar a barreira, o cenário admite respostas como 'degradada', 'não comprovada' ou 'indisponível', então a referência não é única.

**[06_01 · procedimento · varias_respostas]** Antes de selecionar um sistema fixo por agente gasoso para um compartimento, como deve ser verificada a condição do volume protegido?

- Resposta: Verificando sua capacidade de reter o agente, pela estanqueidade e pelo controle de portas, aberturas e ventilação.
- Auditor: A pergunta não fixa um método de verificação e admite respostas igualmente válidas como ensaio de integridade do recinto, cálculo de hold time ou inspeção de vazamentos, enquanto a referência traz só um critério geral.

**[06_01 · consequencia · trivial]** Um trecho da rede principal de incêndio recebeu reparo temporário para conter perda de espessura. Em incêndio adjacente, o reparo não tem resistência térmica equivalente à condição original. Qual efeito direto deve ser esperado nesse trecho?

- Resposta: Indisponibilidade do trecho por falha do reparo sob carga térmica.
- Auditor: Dado que o reparo não resiste termicamente como o original em um incêndio adjacente, esperar sua falha no trecho é consequência direta e óbvia.
