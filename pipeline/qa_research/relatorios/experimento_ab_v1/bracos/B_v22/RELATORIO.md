# Geração v22

Braço B_v22: 107 questões finais de 1020 propostas (18 recusadas pela régua, 130/1002 aprovadas pelo auditor, 23 redundantes).

Chamadas do gerador: 450, das quais 12 sem questões; questões por chamada: {0: 12, 1: 145, 2: 81, 3: 135, 4: 77}.
Falhas do auditor por verificação: {'depende_do_documento': 63, 'varias_respostas': 486, 'atalho': 715, 'nao_unico': 95, 'fora_da_fonte': 13}.
Segunda chance: 121 revisitas de foco após visita sem ganho (20 conhecimentos novos); 56 segundas tentativas de composta (8 finais).
Conhecimentos novos por rodada: {1: 45, 2: 25, 3: 13, 4: 4, 5: 0}; focos por número de visitas: {2: 73, 3: 40, 4: 7, 5: 6}.
Tipos finais: {'diagnostico': 34, 'consequencia': 21, 'mecanismo': 31, 'decisao': 9, 'procedimento': 11, 'conceito': 1}.
Falhas pendentes: 1.

## Amostra de questões finais

**[03_03 · diagnostico · janela]** Um mangote com desgaste interno conhecido opera sem vazamento em vazão estável, mas rompe repetidamente somente nas paradas bruscas da transferência. Sem marcas de impacto nem de dobra acentuada, qual mecanismo dominante deve orientar a resposta técnica?

- Resposta: Choque de momento nas paradas.
- Explicação: O padrão recorrente apenas nas paradas bruscas aponta para solicitação transitória como gatilho dominante; o dano prévio pode existir, mas o mecanismo que precipita a falha é o choque de momento.

**[02_02 · diagnostico · janela]** Após semanas de operação, o residual de oxigênio na água de injeção sobe sem mudança na vazão tratada, no oxigênio dissolvido de alimentação, no cloro residual a montante ou na vazão real da bomba dosadora confirmada em campo. A solução de bissulfito está estocada diluída em tanque com respiro e forte contato com ar. Qual causa explica melhor a perda de desempenho?

- Resposta: Queda da concentração ativa do bissulfito no armazenamento.
- Explicação: Com a mesma vazão real de dosagem e mesma carga oxidante, a piora do residual aponta para perda de atividade da solução. O bloco de apoio liga essa perda às condições de armazenamento e à exposição ao ar.

**[02_02 · mecanismo · janela]** Antes, a incrustação sulfática aparecia principalmente nos produtores. Após passar a reinjetar água produzida rica em bário com co-injeção de água do mar no mesmo poço, a perda de injetividade passa a ocorrer nos injetores. Qual mudança do sistema explica essa migração do problema?

- Resposta: O encontro entre sulfato e bário passou a ocorrer no injetor.
- Explicação: A deposição por BaSO4 ocorre onde a água do mar sulfatada encontra água rica em bário. Com a co-injeção da água produzida, esse ponto de mistura deixa de ser predominante no produtor e passa ao injetor.

**[07_01 · mecanismo · janela]** Numa malha de vazão, o controlador continua corrigindo o erro e a pressão no atuador sobe gradualmente, mas a vazão só reage quando a válvula dá um salto de posição. Que mecanismo explica esse atraso entre o comando e a mudança real da variável manipulada?

- Resposta: Acúmulo de esforço para vencer o atrito estático.
- Explicação: No stiction, o conjunto móvel permanece parado até que a força aplicada supere o atrito estático. O controlador segue corrigindo, mas esse esforço só se converte em movimento quando o limiar é vencido.

**[02_02 · decisao · janela]** Num trecho contaminado da água de injeção, o pigging não alcança a região afetada e uma parada de produção para limpeza interna não é viável. Dentro do programa microbiológico, qual abordagem tende a assumir o papel principal no controle de crescimento microbiano, souring e corrosão microbiológica?

- Resposta: Tratamento químico com biocida.
- Explicação: O bloco foco diz que, se a limpeza mecânica não alcança o trecho contaminado ou não é operacionalmente viável, o tratamento químico ganha importância e pode virar a principal alternativa prática.

**[02_02 · diagnostico · composta]** Na água de injeção de um FPSO, a única mudança recente foi reforçar a cloração na captação. O oxigênio dissolvido na saída da desaeração mecânica permaneceu usual, a dose de bissulfito foi mantida, mas surgiram oxidante residual e maior corrosividade a jusante. Qual é a causa técnica mais provável desse desvio?

- Resposta: Cloro residual consumindo o bissulfito, com subdosagem efetiva do sequestrante.
- Explicação: Com a desaeração mecânica estável, o desvio não vem dessa etapa. O reforço da cloração elevou o residual oxidante no ponto de aplicação; parte do bissulfito reagiu com ele, reduzindo a fração disponível para remover oxigênio.

**[02_02 · diagnostico · janela]** Em um sistema de água de injeção recém-limpo, o residual de biocida no volume está dentro do esperado e a contagem planctônica cai após cada dosagem. Mesmo assim, reaparecem sulfeto e pites em fundos de equipamentos e ramais pouco circulados. Qual é a causa mais provável?

- Resposta: BRS aderidas em biofilme, em nichos pouco alcançados pelo biocida.
- Explicação: Com residual e resposta planctônica adequados, a falha não está no volume principal. F destaca que biomassa aderida pode persistir em nichos protegidos do escoamento, menos acessíveis ao químico; BRS geram sulfeto e sustentam MIC localizada.

**[02_02 · procedimento · janela]** Uma nova água produzida chega ao mesmo sistema, e o ensaio de bancada indica que o químico desestabiliza a dispersão. Antes de fixar dosagem contínua, como verificar se esse aditivo é realmente necessário para a flotação em operação?

- Resposta: Comparando o TOG do flotador com e sem aditivo.
- Explicação: Os blocos afirmam que algumas águas respondem sem aditivo e outras não, e que o benefício depende também do equipamento. O efeito operacional deve aparecer no TOG da água tratada.

**[02_02 · mecanismo · janela]** Em corrosão por fase aquosa em sistemas de gás, qual é o elemento protetor imediato gerado pelo inibidor orgânico sobre o metal?

- Resposta: Película adsorvida na superfície metálica.
- Explicação: O inibidor protege ao adsorver no metal e formar uma película que dificulta o acesso das espécies agressivas.

**[07_01 · consequencia · composta]** Num proof test fracionado por subsistemas, um cenário de shutdown com válvula pneumática on/off foi dado como coberto após o teste da matriz de causa e efeito do SIS. Considerando o alcance desse tipo de evidência, qual efeito final da função ainda pode permanecer sem prova?

- Resposta: O deslocamento real do obturador.
- Explicação: A matriz de causa e efeito demonstra apenas o que o ensaio efetivamente percorreu. Em válvula pneumática on/off, a aprovação no sistema não comprova que a cadeia até o obturador produziu movimento físico.

**[02_02 · consequencia · janela]** Em um sistema de MEG com água produzida já caracterizada como pouco propensa a precipitação salina e sem limitação de bombeamento, a operação decide elevar a concentração de glicol para ampliar a margem contra hidratos. Qual seção do circuito tende a receber a maior carga operacional adicional?

- Resposta: Recuperação e regeneração do glicol.
- Explicação: Excluídas limitações por salting e por bombeamento, o aumento da concentração desloca o gargalo prático para a etapa que reconcentra o MEG, apontada como meta concorrente da proteção contra hidratos.

**[03_03 · diagnostico · janela]** Durante COW no tanque A, logo após uma manobra simultânea nos cabeçalhos de ventilação/IG, o tanque A perde pressão positiva e o O2 sobe. O gerador e o cabeçalho principal permanecem estáveis, enquanto um tanque vizinho fora de operação apresenta aumento inesperado de pressão. Qual é a causa mais provável?

- Resposta: Tanque errado alinhado no caminho de fluxo.
- Explicação: Com gerador e cabeçalho estáveis, a perda no tanque em lavagem combinada com pressurização de outro tanque aponta desvio do fluxo para o vaso incorreto, não falha geral de suprimento.

**[02_02 · diagnostico · janela]** Depois de um squeeze, o residual do inibidor retorna como previsto e a água produzida não mostra sinal de nova incrustação, mas a produtividade do poço cai logo após o tratamento e permanece baixa. Qual causa ligada ao próprio squeeze deve ser investigada primeiro?

- Resposta: Dano à formação pelo tratamento de squeeze.
- Explicação: Com retorno residual adequado e sem sinais de nova incrustação, a queda persistente de produtividade logo após o squeeze aponta primeiro para incompatibilidade ou dano causado pelo próprio tratamento na formação.

**[03_03 · diagnostico · janela]** Durante o deslastro, a bomba é parada e a única rota que permaneceu alinhada é a descarga ao mar. Sem novo comando, a pressão da linha cai e o nível do tanque volta a subir lentamente. Qual é a causa mais provável?

- Resposta: Problema na válvula de retenção da descarga ao mar.
- Explicação: Em F, a retenção na descarga ao mar é barreira operacional. Com a bomba parada e só essa rota alinhada, a reversão de nível indica retorno de água do mar por retenção sem vedação ou mal orientada.

**[02_02 · mecanismo · janela]** Um mesmo biocida controlava a água de injeção e passa a falhar quando a mesma população-alvo é tratada em água com maior carga de espécies reativas e matéria orgânica. O tempo de contato, os materiais e os demais aditivos não mudaram. Qual mecanismo liga essa mudança à perda de controle no ponto contaminado?

- Resposta: Demanda química consumindo o ativo antes de ele chegar ao ponto contaminado.
- Explicação: Com maior demanda química na água, parte do biocida é consumida antes de alcançar a região afetada. Assim, cai a concentração ativa efetiva no ponto contaminado, mesmo com a mesma dosagem nominal.
