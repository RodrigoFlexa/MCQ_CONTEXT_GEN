# Reauditoria das aprovadas da v16 com o auditor v2

Aprovadas antes: 1038; continuam aprovadas: **622**.
Motivos: {'nenhum': 622, 'resposta_vaga': 29, 'lista_generica': 52, 'trivial': 117, 'varias_respostas': 130, 'reformula_enunciado': 41, 'prudencia_generica': 23, 'caso_especifico': 13, 'sim_nao_disfarcado': 6, 'tecnicamente_errada': 5}.
Por tópico (aprovadas agora / antes): {'01_01': '52/103', '02_03': '60/98', '03_01': '60/99', '04_02': '63/102', '05_02': '68/100', '06_05': '73/107', '07_04': '79/120', '08_03': '61/101', '09_02': '62/113', '10_01': '44/95'}.
Removidas na revisão manual: 13; o auditor v2 reprova **10** ({'sim_nao_disfarcado': 1, 'trivial': 2, 'nenhum': 3, 'reformula_enunciado': 2, 'resposta_vaga': 1, 'varias_respostas': 2, 'prudencia_generica': 1, 'caso_especifico': 1}).

## Amostra de reprovadas agora

**[01_01 · diagnostico · varias_respostas]** Em um FPSO, o compressor ativo desarma e o equipamento reserva recebe comando automático. O reserva parte, atinge rotação e suas utilidades estão normais, mas a compressão não retorna. No histórico, a válvula comum de descarga não abriu em duas tentativas e a mesma permissiva do header permaneceu não atendida; em teste local posterior, válvula e atuador responderam normalmente. Qual causa específica explica melhor a perda da função?

- Resposta: Lógica de intertravamento comum na descarga, impedindo a comutação.
- Auditor: Os sinais indicam uma falha comum na cadeia de permissiva/descarga, mas não isolam unicamente lógica de intertravamento em vez de instrumento, sinal ou outra condição comum do header.

**[07_04 · diagnostico · varias_respostas]** Em um FPSO, um tanque concebido para óleo passou a armazenar água offspec por longos períodos. Nas últimas inspeções, há falhas do revestimento interno, sinais corrosivos também acima do fundo e ânodos envelhecidos. Parte da equipe ainda trata o risco como concentrado apenas na região de decantação. Qual é a causa técnica mais provável desse padrão de dano?

- Resposta: Insuficiência da proteção catódica originalmente concebida para o serviço efetivo, porque o novo armazenamento aquoso com revestimento degradado e ânodos envelhecidos supera a capacidade remanescente.
- Auditor: O padrão pode decorrer da mudança para serviço aquoso com molhamento ampliado, da falha do revestimento, do envelhecimento dos ânodos ou de combinação desses fatores, sem demonstrar que a causa dominante seja insuficiência da proteção catódica.

**[10_01 · procedimento · lista_generica]** Na comparação de destinações para materiais e equipamentos de um FPSO em descomissionamento, como a análise deve tratar os aspectos além do custo imediato?

- Resposta: Pelos critérios da comparação, incluindo segurança da remoção e do transporte, risco ambiental residual, viabilidade de recuperação ou reciclagem, logística e impacto econômico global.
- Auditor: A referência se limita a listar critérios amplos de comparação, sem indicar um método técnico preciso ou um elemento decisivo.

**[01_01 · mecanismo · lista_generica]** Por que a lista nominal de técnicas não basta, por si só, para selecionar a rota de mitigação de incrustação em um FPSO?

- Resposta: Porque a eficácia e a aplicabilidade dependem do mecanismo dominante, da origem dos íons, da arquitetura de injeção e produção, da acessibilidade e das penalidades de parada.
- Auditor: A referência responde com um rol de fatores de contexto, sem formular de modo decisivo o princípio técnico que governa a escolha da mitigação.

**[01_01 · diagnostico · reformula_enunciado]** Na análise de modos e efeitos de falha de um sistema do FPSO, os critérios de avaliação estão definidos e os dados são rastreáveis. Mesmo assim, para o mesmo item, especialistas registram funções diferentes e, a partir disso, surgem modos e efeitos incompatíveis entre si. Qual causa específica explica melhor esse desalinhamento?

- Resposta: Ausência de entendimento comum das funções analisadas.
- Auditor: A referência apenas reexprime o próprio sintoma dado no enunciado — funções divergentes para o mesmo item — sem avançar para uma causa técnica mais profunda.

**[03_01 · diagnostico · reformula_enunciado]** Em um FPSO de aproamento fixo com aliviador por posicionamento dinâmico, a perda de posição aparece repetidamente apenas em uma mesma faixa angular e sob um mesmo modo de controle adotado. Sensores e thrusters respondem normalmente, e elevar a potência instalada não mudou o comportamento. Qual causa específica explica melhor a limitação?

- Resposta: Restrição dos modos e setores operacionais adotados.
- Auditor: A referência apenas renomeia o padrão já dado no enunciado — mesma faixa angular e mesmo modo de controle — sem apontar uma causa técnica mais discriminante.

**[04_02 · decisao · varias_respostas]** Como se deve posicionar a separação e destinar a água oleosa separada para reduzir o volume tratado e descartado offshore?

- Resposta: Com separação no leito marinho e reinjeção da água oleosa separada no reservatório.
- Auditor: Sem condições sobre reservatório, malha de injeção e arquitetura submarina, há mais de uma solução tecnicamente válida para reduzir tratamento e descarte offshore.

**[10_01 · diagnostico · tecnicamente_errada]** Em um projeto brasileiro de desmontagem offshore, as campanhas de plataforma, abandono de poços e sistema submarino disputam embarcações especializadas, as janelas operacionais úteis não coincidem e um atraso em uma frente reprograma as outras. Considerando que cada frente teria recursos suficientes se operasse isoladamente, qual causa de planejamento explica melhor esse comportamento?

- Resposta: Falta de separar plataforma, abandono de poços e sistema submarino em frentes com cronologias próprias.
- Auditor: O quadro descrito indica mais falha de integração de interfaces e de gestão de recursos compartilhados do que mera ausência de frentes com cronologias próprias, tornando a referência tecnicamente imprecisa.

**[03_01 · mecanismo · varias_respostas]** Por que diferenças observadas entre operações com SPM e SMS não definem, por si só, uma regra universal para selecionar aliviador, apoio externo e aproximação?

- Resposta: Porque o tipo de amarração influencia o problema de posicionamento, mas não determina sozinho a combinação de aliviador, apoio externo e aproximação.
- Auditor: A pergunta é ampla e admite várias justificativas igualmente corretas além do tipo de amarração, como metocean, capacidades do aliviador e filosofia operacional.

**[10_01 · mecanismo · varias_respostas]** Por que a separação entre plataforma, abandono de poços e sistema submarino não deve ser adotada como regra universal para qualquer ativo?

- Resposta: Porque a independência só vale com interfaces reais controladas; dependências técnicas ativas entre as frentes invalidam o desacoplamento geral.
- Auditor: Sem especificar quais dependências e interfaces estão em jogo, há várias explicações técnicas igualmente corretas para não adotar o desacoplamento como regra universal.

**[01_01 · consequencia · trivial]** Se uma falha de causa comum atinge ao mesmo tempo o equipamento ativo e o reserva de um FPSO, o que ocorre com o benefício esperado da redundância?

- Resposta: Reduz-se fortemente ou desaparece, porque ambos perdem a função no mesmo evento.
- Auditor: O desaparecimento do benefício da redundância quando uma causa comum derruba ativo e reserva é praticamente a própria definição do fenômeno.

**[06_05 · diagnostico · reformula_enunciado]** Em um teste funcional numa zona de processo do FPSO, um detector fixo entra em alarme e o evento é registrado, mas a atuação automática prevista para a zona não ocorre. Depois do teste, as saídas comandadas atuam normalmente quando forçadas pelo sistema, e a configuração da zona exige confirmação por dois canais. Em campo, apenas um detector dessa zona está operacional. Qual causa específica explica a ausência de atuação automática?

- Resposta: Número insuficiente de detectores operacionais na zona para satisfazer a lógica configurada.
- Auditor: O enunciado já entrega a causa ao informar que a zona exige dois canais e só um detector está operacional, e a resposta apenas reempacota esse dado.

**[09_02 · conceito · trivial]** Qual referência de capacidade do próprio guindaste continua necessária, mesmo após as verificações pré-uso?

- Resposta: Load chart.
- Auditor: Pede apenas o nome da referência padrão de capacidade do guindaste, algo muito direto e pouco discriminante.

**[01_01 · conceito · trivial]** Na dependabilidade de um sistema de FPSO, qual atributo expressa a capacidade de continuar prestando o serviço correto ao longo de um intervalo, sob condições definidas?

- Resposta: Confiabilidade.
- Auditor: A questão pede a definição clássica de confiabilidade, recuperável de forma imediata por qualquer profissional da área.

**[08_03 · mecanismo · varias_respostas]** Por que nomenclaturas históricas de licenças de perfuração ou pesquisa não servem como regra única para enquadrar a produção offshore?

- Resposta: Porque a modalidade de licença depende da atividade autorizada e do enquadramento do órgão competente; nomes históricos não abrangem, por si, a produção offshore.
- Auditor: A pergunta busca a causa de um enquadramento regulatório inadequado e admite razões igualmente válidas além da referência, como evolução normativa e distinção entre fases da atividade.

**[09_02 · conceito · trivial]** Em que sistema tendem a ser geridos os requisitos de manutenção dos equipamentos de içamento?

- Resposta: No sistema de manutenção do operador.
- Auditor: A questão praticamente se responde sozinha, pois requisitos de manutenção serem geridos no sistema de manutenção do operador não exige conhecimento técnico específico.

**[04_02 · procedimento · lista_generica]** Na seleção prática de uma solução de controle subsea, como a avaliação deve ser conduzida?

- Resposta: Pela análise conjunta da função comandada, fail-safe, infraestrutura do umbilical, profundidade, distância, número de válvulas, criticidade temporal e capacidade de intervenção por ROV.
- Auditor: A resposta só enumera critérios de seleção e não estabelece um procedimento técnico decisivo ou verificável.

**[01_01 · conceito · varias_respostas]** Na análise de perdas de produção, que termo designa o fenômeno físico ou processo que compromete a operacionalidade do sistema?

- Resposta: Mecanismo de falha.
- Auditor: Sem o documento, um profissional pode responder com termos diferentes e plausíveis, como mecanismo de falha, modo de falha ou mecanismo de degradação.

**[10_01 · conceito · prudencia_generica]** Que abordagem deve embasar a decisão de enviar a unidade ao estaleiro?

- Resposta: Avaliação comparativa multicritério.
- Auditor: 'Avaliação comparativa multicritério' é um princípio decisório genérico, aplicável a inúmeras escolhas além deste contexto.

**[08_03 · decisao · prudencia_generica]** Num FPSO, o plano para um derramamento foi revisto com base no óleo real e em cenários plausíveis de mar e vento. A técnica preferida da equipe tem alta capacidade nominal, mas sua janela operacional e a mobilização disponível limitam a efetividade; ao mesmo tempo, há barreiras, proteção de áreas sensíveis e recolhimento complementar mobilizáveis. Na resposta, que lógica de emprego dos recursos deve orientar o plano?

- Resposta: Combinar medidas de resposta, porque o plano deve usar os recursos mobilizáveis para reduzir o dano total, não maximizar uma técnica isolada.
- Auditor: A resposta enuncia um princípio amplo de planejamento de resposta a derramamento, aplicável a muitos casos, sem apontar uma ação técnica específica e verificável.

**[04_02 · procedimento · trivial]** Em completação molhada, como deve ser comandada a ANM durante a operação do poço?

- Resposta: Por meio do sistema de controle remoto da ANM, acionado da plataforma ou de terra.
- Auditor: Comandar a ANM por sistema remoto em completação molhada é conhecimento básico e praticamente inerente ao conceito de árvore submarina.

**[01_01 · consequencia · trivial]** Em dois FPSOs com configuração, regime operacional, manutenção, barreiras e contexto organizacional diferentes, a equipe aplica o mesmo ranking histórico para definir criticidade. Que efeito isso tende a causar na priorização?

- Resposta: Priorização inadequada dos sistemas críticos, com possível exclusão de funções sensíveis da unidade.
- Auditor: Dizer que usar o mesmo ranking em contextos diferentes gera priorização inadequada é consequência evidente do próprio enunciado.

**[08_03 · mecanismo · lista_generica]** Como o encadeamento dos componentes do estudo ambiental torna tecnicamente avaliável uma nova interligação a um FPSO?

- Resposta: Ao localizar a interação com o ambiente, estabelecer a referência e relacionar fontes, riscos, controles e acompanhamento, o estudo conecta a atividade aos efeitos e à gestão.
- Auditor: A referência enumera componentes genéricos do estudo ambiental, mas não fixa um mecanismo técnico decisivo que explique a avaliabilidade da nova interligação.

**[05_02 · decisao · varias_respostas]** Na partida direta de um grande motor em um FPSO, com geradores em paralelo operando em droop, a tensão do barramento afunda e a frequência começa a cair. Já foi confirmado que não há curto-circuito no alimentador do motor nem perda adicional de gerador, e é preciso estabilizar o sistema sem sacrificar funções essenciais. Que ação técnica imediata deve ser aplicada?

- Resposta: Load shedding das cargas menos prioritárias, porque reduz rapidamente a solicitação sobre os geradores remanescentes e aumenta a chance de manter as funções essenciais.
- Auditor: Sem dizer se a partida do motor pode ou deve ser abortada, tanto retirar o motor de partida quanto fazer load shedding de não essenciais podem ser ações imediatas corretas.

**[06_05 · mecanismo · trivial]** Em um arranjo de CO2 com confirmação local, confirmação no supervisório e temporização antes da descarga, como essa sequência reduz disparos indevidos?

- Resposta: Ao exigir validações independentes antes do comando final, ela bloqueia atuações não confirmadas e só libera a descarga após checagem adicional.
- Auditor: A ideia de que mais confirmações e atraso reduzem disparos indevidos é um nexo causal bastante óbvio e geral.
