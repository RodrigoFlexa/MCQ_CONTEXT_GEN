# Geração v22

Braço tipo_decisao: 1945 questões finais de 10307 propostas (90 recusadas pela régua, 2353/10217 aprovadas pelo auditor, 408 redundantes).

Chamadas do gerador: 4167, das quais 125 sem questões; questões por chamada: {0: 125, 1: 555, 2: 1367, 3: 1462, 4: 658}.
Falhas do auditor por verificação: {'atalho': 7033, 'varias_respostas': 1542, 'fora_da_fonte': 279, 'nao_unico': 65, 'depende_do_documento': 296, 'bloqueio': 2}.
Segunda chance: 1891 revisitas de foco após visita sem ganho (519 conhecimentos novos); 0 segundas tentativas de composta (0 finais).
Conhecimentos novos por rodada: {1: 779, 2: 447, 3: 313, 4: 272}; focos por número de visitas: {1: 1, 2: 14, 3: 46, 4: 1000}.
Tipos finais: {'decisao': 1649, 'mecanismo': 6, 'procedimento': 167, 'conceito': 12, 'diagnostico': 111}.
Falhas pendentes: 0.

## Amostra de questões finais

**[06_04 · decisao · janela]** Inspeção periódica de corrosão do atuador de uma válvula de ESD foi lançada como barreira preventiva adicional contra perda de contenção. Como esse item deve ser tratado no Bow-Tie?

- Resposta: como controle de fator de degradação da válvula de ESD
- Explicação: A inspeção preserva a capacidade da válvula cumprir sua função; não interrompe diretamente a progressão da ameaça até o evento topo.

**[05_02 · decisao · janela]** Após interligar permanentemente os secundários de dois transformadores, o teste de falha do disjuntor de um alimentador mostra que a retaguarda de fase do primário deixou de atuar, embora a temporização siga seletiva. Que ajuste fazer?

- Resposta: Reduzir a corrente de partida da retaguarda de fase do primário.
- Explicação: A interligação cria caminhos adicionais de corrente de falta e pode reduzir a corrente vista por cada primário. Se o escalonamento temporal continua correto, o problema é de sensibilidade da retaguarda de fase.

**[02_04 · decisao · janela]** Misturas variáveis de duas águas serão co-injetadas, e a decisão agora é definir o sal mais crítico e o antincrustante preventivo. Qual abordagem de previsão deve servir de base técnica inicial?

- Resposta: Modelo de equilíbrio termodinâmico compatível com o sistema real.
- Explicação: Para identificar sais com maior tendência de precipitação e apoiar a escolha de inibidores, a base inicial é a previsão por equilíbrio termodinâmico, desde que represente a mistura real.

**[02_11 · decisao · janela]** Misturadas antes do adoçamento, uma corrente sai com CO2 muito abaixo da meta e a outra ainda oscila no limite de H2S; o regenerador precisa continuar único. Que arranjo você adota?

- Resposta: Absorvedores separados com regeneração comum.
- Explicação: As correntes pedem objetivos de remoção distintos. Separar a absorção permite ajustar cada dever de contato sem perder o benefício de um único trem regenerativo.

**[02_10 · decisao · janela]** Água produzida pressurizada sai sem óleo livre visível, mas com gotículas dispersas acima da capacidade do polimento; nesta etapa, não se quer usar gás. Que equipamento deve ser instalado logo a jusante do separador?

- Resposta: Hidrociclone.
- Explicação: Na água produzida com óleo disperso remanescente, o hidrociclone separa em linha pelo campo centrípeto; a flotação é mais adequada ao polimento de microgotículas com gás.

**[03_01 · decisao · janela]** O casco em ponto único de amarração está em weathervaning, e o operador quer referenciar o aliviador só pelo aproamento absoluto do produtor. Qual referência de posicionamento deve continuar comandando o controle?

- Resposta: Posição relativa à estação de alívio
- Explicação: O giro do casco para a resultante ambiental não elimina o controle do aliviador. A aproximação e a permanência continuam exigindo compatibilidade relativa com a estação de alívio.

**[09_02 · procedimento · janela]** Skid sairá do convés, cruzará a lâmina d’água e será assentado em berço submarino. O conjunto passa com folga na verificação pelo peso no ar com um único fator dinâmico. Que tratamento analítico deve substituir essa validação antes de autorizar a manobra?

- Resposta: Análise dinâmica faseada da entrada na água ao pouso no fundo.
- Explicação: A manobra muda de regime entre peso no ar, efeitos hidrodinâmicos na descida e interação no pouso; uma única checagem no ar não representa os esforços das fases críticas.

**[01_01 · decisao · janela]** Comparando a mantenabilidade de dois equipamentos, o reparo físico dura 2 horas em ambos, mas um fica indisponível muito mais tempo por espera de acesso, sobressalente e liberação. Que tempo deve entrar no indicador de mantenabilidade?

- Resposta: tempo de reparo ativo
- Explicação: Para medir a capacidade de restauração do item, usa-se a intervenção propriamente dita; esperas logísticas e administrativas pertencem à indisponibilidade operacional.

**[07_03 · decisao · janela]** Planos preventivos já estão cadastrados no ERP, e colisões com produção e materiais só aparecem na véspera. Para enxergar as próximas semanas por responsável, local e data planejada antes da programação, que instrumento deve ser montado?

- Resposta: Plano Mestre de Manutenção Preventiva
- Explicação: Para preventivas já registradas, o plano mestre é a extração que classifica por semana, responsável e local, dando horizonte e visibilidade antes da programação curta.

**[04_02 · diagnostico · janela]** Válvulas e sensores ligados a módulos diferentes na mesma estrutura deixam juntos de responder ou atualizar; estruturas vizinhas seguem normais, sem relação com movimento da embarcação. Em que ponto técnico intervir primeiro?

- Resposta: Terminação e distribuição do umbilical nessa estrutura.
- Explicação: A perda simultânea em equipamentos de módulos distintos, limitada a uma única estrutura, aponta para o ponto comum onde o umbilical se conecta e distribui energia, sinais e serviços.

**[08_03 · decisao · janela]** Corrente aquosa separada do poço passou a ser enviada às drenagens oleosas porque o óleo livre é baixo e o volume, pequeno. Qual arranjo técnico deve ser mantido para essa corrente?

- Resposta: Segregação no sistema dedicado de água produzida
- Explicação: Mesmo com pouco óleo livre, a corrente pode conter sais, orgânicos dissolvidos e dispersos, sólidos, gases, metais e químicos; por isso exige controle e destinação próprios, não tratamento como efluente genérico.

**[02_05 · decisao · janela]** Camada livre de óleo reaparece no topo do tanque de drenagem aberta após lavagens de convés, e mandar todo o volume ao slop vem sobrecarregando transferências. Que arranjo interno deve ser adotado nesse tanque?

- Resposta: Compartimento superior para hidrocarboneto sobrenadante.
- Explicação: Nos sistemas abertos descritos, o tanque pode reter a fase de hidrocarboneto flutuante antes do envio ao slop, reduzindo carga desnecessária de transferência e preservando a contenção.

**[08_02 · decisao · janela]** Troca-se apenas o desengraxante; ferramenta, tarefa e tempo de manuseio continuam iguais. O estoque quer manter a mesma luva usada no produto anterior. Que referência técnica deve comandar a escolha do material da luva?

- Resposta: Compatibilidade do material da luva na FDS do novo produto.
- Explicação: A mesma tarefa pode expor a substâncias diferentes; a FDS orienta incompatibilidades e o material de luva adequado para aquele produto.

**[02_11 · decisao · janela]** Gás úmido com condensado passa por estrangulamento e segue para linha fria; o solvente desse trecho será recuperado após contato com água e hidrocarboneto líquido. Qual glicol selecionar?

- Resposta: MEG
- Explicação: A demanda principal é inibição de hidratos em pontos frios, com recuperação do solvente mesmo após contato com condensado. Nessa função, o MEG é o glicol mais adequado.

**[02_05 · diagnostico · janela]** Com o aumento de vazão, o dreno antes estável passa a puxar líquido e enviá-lo a jusante, sem bloqueio visível na linha. Que variável hidráulica deve ser corrigida no arranjo?

- Resposta: Perda de carga do arranjo de separação.
- Explicação: O sinal descrito é sucção induzida pelo diferencial de pressão do próprio arranjo. Corrigir a perda de carga remove a força que passou a arrastar líquido pelo dreno.
