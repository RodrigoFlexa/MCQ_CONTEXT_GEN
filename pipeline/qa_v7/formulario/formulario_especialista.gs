/**
 * PetroQuest: formulários de avaliação de questões por especialista (Google Apps Script).
 *
 * Como usar:
 *   1. Acesse https://script.google.com, crie um projeto novo e cole este arquivo inteiro no Código.gs.
 *   2. Selecione a função criarFormulario e clique em Executar. Autorize o acesso ao Google Forms/Sheets.
 *   3. Se o registro de execução disser que pausou por tempo, execute criarFormulario de novo:
 *      ele continua de onde parou, sem duplicar.
 *   4. No final, o registro mostra os links (listarLinks mostra de novo).
 *      Para começar do zero, execute recomecar, apague os formulários antigos no Drive e rode criarFormulario.
 *
 * Por padrão é criado um formulário por tópico (5 questões cada): o Google Forms limita o número de itens
 * por formulário e 100 questões numa página só ficariam longas demais para uma sessão. Se mesmo assim um
 * formulário atingir o limite, o script cria automaticamente uma "parte 2" e continua dali.
 *
 * Cada questão ocupa uma página: enunciado, resposta, critério de correção, justificativa, grade de notas de 1 a 5, o contexto usado na geração
 * com parecer e motivo, o parecer final da questão com motivo e a concordância com a nossa classificação de
 * dificuldade. Quem discorda vai para uma página curta: a classificação que daria e os motivos (com "Outro"). Os títulos levam o código (Q001...) para
 * cruzar as respostas com o arquivo mapa_questoes_formulario.csv.
 */

const CONFIG = {
  titulo: 'PetroQuest: avaliação de questões por especialista',
  // true: um formulário por tópico (recomendado). false: tenta um formulário único (divide em partes se lotar).
  umFormularioPorTopico: true,
  criarPlanilhaDeRespostas: true,
  permitirEditarResposta: false,  // o especialista só avalia; não edita a resposta depois de enviar
};

const CRITERIOS = [
  'Clareza do enunciado',
  'Corretude técnica',
  'Relevância para a operação de FPSOs',
  'Qualidade da resposta correta',
];
const NOTAS = ['1 (muito ruim)', '2', '3', '4', '5 (excelente)'];
const PARECERES = ['Aprovado', 'Aprovado com ressalvas', 'Rejeitado'];
const NIVEIS = ['Fácil', 'Média', 'Difícil'];
const CONCORDO = 'Concordo';
const DISCORDO = 'Discordo';
const MOTIVOS_DIFICULDADE = [
  'Exige apenas recordar um conceito ou definição',
  'A resposta é direta ou está sugerida no próprio enunciado',
  'É conhecimento básico para quem atua em FPSO',
  'O cenário não acrescenta raciocínio; a decisão é direta',
  'Exige integrar vários conceitos, sistemas ou disciplinas',
  'Exige várias etapas de raciocínio ou análise de prós e contras',
  'Exige conhecimento especializado ou pouco difundido',
  'Exige experiência prática de operação',
  'Envolve cálculo ou interpretação de valores e dados',
];
const LIMITE_MS = 5 * 60 * 1000;  // o Apps Script encerra execuções com 6 minutos

const QUESTOES = [
 {
  "codigo": "Q001",
  "id": "62e43c1988-s0000-A1",
  "topico": "Sistemas de Lastro, Estabilidade, Ancoragem e Posicionamento, Offloading e Tanques de Carga",
  "subtopico": "Sistema de ancoragem, manutenção e monitoramento da posição",
  "nivel": "Fácil",
  "dificuldade": "Fácil",
  "pergunta": "O que é o offset, ou passeio, de uma unidade flutuante ancorada?",
  "resposta": "É o deslocamento horizontal entre a posição inicial de equilíbrio neutro e a posição final de equilíbrio sob a ação de vento, correnteza e ondas.",
  "pontos_essenciais": [
   "deslocamento horizontal da unidade",
   "entre a posição inicial de equilíbrio neutro e a posição final sob cargas ambientais"
  ],
  "explicacao": "Offset, ou passeio, é definido pela mudança horizontal de posição da unidade quando as cargas ambientais a afastam da locação, até um novo equilíbrio. A definição depende da comparação entre a posição neutra inicial e a posição final sob vento, correnteza e ondas.",
  "contexto": "Nota técnica: Offset da unidade em sistemas de ancoragem: origem, cálculo, limites e evidências de conformidade\nResumo: O offset da unidade é o deslocamento horizontal imposto por vento, corrente e ondas e contido pela força de restauração do sistema de ancoragem. Em projeto, esse deslocamento é estimado a partir do equilíbrio entre ações ambientais e resposta das linhas, considerando condição intacta, avariada e efeitos dinâmicos e de baixa frequência. Em operação, a conformidade não se demonstra por suposição, mas por comparação com critérios aplicáveis e por registros confiáveis de offsets, movimentos e parâm…\nConhecimento que a questão deveria avaliar: Definir offset ou passeio como a distância horizontal entre a posição inicial de equilíbrio neutro e a posição final de equilíbrio sob cargas ambientais.\n\nFatos das fontes usados na resposta (afirmação e trecho original):\n• Sob carregamento ambiental de vento, correnteza e ondas, a unidade flutuante sofre passeio ou deslocamento. Esse deslocamento corresponde à distância horizontal percorrida desde a posição inicial de equilíbrio neutro até a posição final de equilíbrio sob a ação das cargas.\n  Trecho: \"A unidade flutuante se encontra sob a ação de um carregamento ambiental (vento, correnteza e ondas) e isto faz que com que a mesma, sofra um passeio ou deslocamento, correspondente a distância horizontal que a unidade percorre desde a sua posição inicial de equilíbrio neutro, até a posição final de equilíbrio sob a aç…\" [REGIS · 14873_000917140.pdf]\n• A componente horizontal da resultante das forças ambientais atua no deslocamento da unidade flutuante sobre a superfície do mar, afastando-a da locação.\n  Trecho: \"A componente horizontal da resultante destas forças atua no sentido de deslocar a unidade flutuante, sobre a superfície do plano do mar, afastando-a da locação\" [REGIS · 14873_000917140.pdf]"
 },
 {
  "codigo": "Q002",
  "id": "567fdce5c3-s0001-A1",
  "topico": "Sistemas de Lastro, Estabilidade, Ancoragem e Posicionamento, Offloading e Tanques de Carga",
  "subtopico": "Operação de tanques de carga, lastro, sistema gás inerte, ventilação e estabilidade",
  "nivel": "Média",
  "dificuldade": "Média",
  "pergunta": "Em uma troca de água de lastro por fluxo contínuo, qual volume bombeado em cada tanque demonstra, operacionalmente, o atendimento ao padrão equivalente de renovação de 95%?",
  "resposta": "Bombear, em cada tanque, volume igual a três vezes a sua capacidade.",
  "pontos_essenciais": [
   "três vezes a capacidade de cada tanque"
  ],
  "explicacao": "No processo de fluxo contínuo, o atendimento ao padrão de troca não é demonstrado apenas pela declaração de que houve renovação, mas pelo volume efetivamente bombeado por tanque. A equivalência operacional adotada para o padrão de 95% é três volumes do tanque.",
  "contexto": "Nota técnica: Risco biológico da água de lastro e motivação histórica do gerenciamento global\nResumo: A água de lastro cria uma rota operacional de transporte de organismos e sedimentos entre regiões, o que pode introduzir espécies fora de seus habitats naturais e gerar impactos ambientais, econômicos e à saúde humana. Como as fontes indicam que, à época, não havia tecnologia de tratamento prontamente aplicável a bordo para descarte seguro, a resposta internacional foi padronizar o gerenciamento e estabelecer critérios verificáveis de troca e qualidade da água.\nConhecimento que a questão deveria avaliar: Interpretar o critério de troca de 95% e sua equivalência operacional de três volumes de tanque no processo de fluxo contínuo.\n\nFatos das fontes usados na resposta (afirmação e trecho original):\n• Na inexistência de tecnologia viável a bordo para tratar a água de lastro com descarte seguro, foi estabelecida uma padronização global do gerenciamento e indicadores de qualidade da água. A padronização do gerenciamento decorreu da limitação de tratamento seguro a bordo.\n  Trecho: \"Com a inexistência de tecnologia viável para tratamento de água de lastro a bordo, suficiente para descarte seguro, foi estabelecida uma padronização global desse gerenciamento e indicadores de qualidade de água\" [REGIS · 9848_arquivo821_1.pdf]"
 },
 {
  "codigo": "Q003",
  "id": "01c1c3db6e-s0001-A1",
  "topico": "Sistemas de Lastro, Estabilidade, Ancoragem e Posicionamento, Offloading e Tanques de Carga",
  "subtopico": "Operação de Offloading",
  "nivel": "Média",
  "dificuldade": "Média",
  "pergunta": "Em uma PRA de offloading nas estações de proa e popa, qual evento de posicionamento relativo tende a concentrar os riscos classificados como “Not Tolerable”, por estar associado a vazamento de óleo em grande escala a partir do tanque de carga do FPSO?",
  "resposta": "O drive-off, por ser o principal gatilho dos riscos não toleráveis nessas estações e estar associado a vazamento de óleo em grande escala do tanque de carga do FPSO.",
  "pontos_essenciais": [
   "drive-off",
   "associação aos riscos “Not Tolerable” com vazamento em grande escala do tanque de carga do FPSO"
  ],
  "explicacao": "Nas estações de offloading pela proa e pela popa, a PRA identificou que os riscos “Not Tolerable” estão principalmente ligados à ocorrência de drive-off. Nesses cenários, a consequência crítica considerada é o vazamento de óleo em grande escala a partir do tanque de carga do FPSO.",
  "contexto": "Nota técnica: Drive-off, perda de posição e colisão no offloading: cenários críticos de poluição\nResumo: Na operação de offloading, a análise de risco prioriza drive-off, perda de posição e colisão porque esses eventos podem evoluir para derramamento de óleo em grande escala, inclusive a partir de tanque de carga do FPSO. O arranjo operacional adotado — setor de operação, tipo de conexão e possibilidade de desconexão rápida — altera diretamente o caminho causal entre desvio de posicionamento e perda de contenção.\nConhecimento que a questão deveria avaliar: Relacionar drive-off nas estações de proa e popa aos riscos “Not Tolerable” e ao vazamento de óleo em grande escala a partir de tanque de carga do FPSO.\n\nFatos das fontes usados na resposta (afirmação e trecho original):\n• Nas estações de offloading pela proa e pela popa, os riscos classificados como “Not Tolerable” estão principalmente relacionados à ocorrência de drive-off. Esses riscos não toleráveis envolvem vazamento de óleo em grande escala a partir de tanque de carga do FPSO.\n  Trecho: \"The “Not Tolerable” risks, both at the bow and stern stations, are mainly related to the occurrence of drive-off; • These not tolerable risks involve large-scale oil leak from and FPSO cargo tank when offloading by either bow or stern;\" [REGIS · 9388_AnaLuisadeBarrosOrsoliniCorr17.pdf]"
 },
 {
  "codigo": "Q004",
  "id": "567fdce5c3-s0002-A1",
  "topico": "Sistemas de Lastro, Estabilidade, Ancoragem e Posicionamento, Offloading e Tanques de Carga",
  "subtopico": "Operação de tanques de carga, lastro, sistema gás inerte, ventilação e estabilidade",
  "nivel": "Difícil (cenário em um conceito)",
  "dificuldade": "Difícil",
  "pergunta": "Em duas emergências, uma unidade inclinada por alagamento recebeu contralastro em tanques dedicados no bordo oposto, enquanto outra precisou encher tanques de carga com água oleosa para permanecer estável. Qual diferença operacional explica a segunda escolha, apesar do objetivo comum das duas manobras?",
  "resposta": "A segunda escolha ocorreu por insuficiência da capacidade de lastro dedicada; em ambas, o objetivo era recuperar uma condição segura de estabilidade, trim e nivelamento.",
  "pontos_essenciais": [
   "insuficiência/limitação da capacidade dos tanques ou do sistema de lastro dedicado",
   "objetivo comum de manter ou recuperar estabilidade em condição segura e nivelada"
  ],
  "explicacao": "Nas duas respostas, busca-se restabelecer condição segura de flutuação, com estabilidade, trim e nivelamento adequados. A diferença é que, quando o sistema de lastro dedicado não oferece capacidade suficiente, pode ser necessário usar tanques de carga de forma excepcional para manter a estabilidade.",
  "contexto": "Nota técnica: Lastro em emergência e compensação de avarias\nResumo: Em situação de emergência, o sistema de lastro é um recurso de resposta à avaria para levar a unidade a uma condição segura de trim e nivelamento e para compensar perda de flutuabilidade causada por dano. Os casos citados mostram que o contralastro, embora seja uma resposta à inclinação por alagamento, pode ao mesmo tempo aumentar o calado, e que limitações de capacidade do sistema podem levar, excepcionalmente, ao uso de tanques de carga para manter a estabilidade.\nConhecimento que a questão deveria avaliar: Comparar duas respostas de emergência — contralastro em tanques dedicados e preenchimento de tanques de carga — distinguindo o objetivo comum de estabilidade dos limites operacionais que levaram a cada escolha.\n\nFatos das fontes usados na resposta (afirmação e trecho original):\n• Em situação de emergência, o sistema de lastro deve ser usado para levar a embarcação o mais rápido possível a um trim seguro e nivelado. O sistema de lastro também é usado para compensar a perda de flutuabilidade causada por dano à instalação.\n  Trecho: \"In an emergency situation the ballast system will be used to bring the vessel to a safe and level trim as soon as possible. The ballast system is also used to compensate for the loss of buoyancy brought about by damage to the installation.\" [HSE (Reino Unido) · ed-loss-of-stability-and-positioning.pdf, p. 8]\n• Para corrigir a inclinação causada pela entrada de água na coluna avariada, foi determinado o carregamento com água do mar dos tanques de lastro na coluna diametralmente oposta, em proa bombordo. Essa ação acelerou o aumento indesejável do calado da plataforma.\n  Trecho: \"os tanques de lastro situados na coluna diametralmente oposta (proa bombordo) fossem carregados com água do mar a fim de restabelecer as condições operacionais da plataforma. É importante registrar que a ação tomada para corrigir a inclinação da plataforma acelerou o aumento indesejável de seu calado.\" [ANP · Relatório do acidente com a P-36 (versão em Português), p. 12]\n• Na unidade, os tanques de carga foram preenchidos com aproximadamente 86.000 m³ de água oleosa para manter a estabilidade da embarcação. Essa medida foi adotada porque a FPSO possuía apenas dois tanques de lastro.\n  Trecho: \"na unidade, os tanques de carga foram preenchidos com aproximadamente 86.000 m³ de água oleosa com vistas a manter a estabilidade da embarcação porque a FPSO possuía apenas dois tanques de lastro\" [ANP · Relatório de investigação do acidente de descarga de óleo ocorrido no FPSO Cida…, p. 19]"
 },
 {
  "codigo": "Q005",
  "id": "01c1c3db6e-s0005-A1",
  "topico": "Sistemas de Lastro, Estabilidade, Ancoragem e Posicionamento, Offloading e Tanques de Carga",
  "subtopico": "Operação de Offloading",
  "nivel": "Difícil (integra dois ou mais conceitos)",
  "dificuldade": "Difícil",
  "pergunta": "Ao fim de um offloading, o FPSO exportou o volume planejado, mas reteve óleo a bordo por requisito operacional e a planta continuou enviando óleo aos tanques nas horas seguintes. Para verificar a estabilidade e ajustar o lastro, qual condição deve ser tomada como referência?",
  "resposta": "A condição real final de carregamento do FPSO: inventário efetivamente a bordo e sua distribuição, incluindo óleo remanescente, óleo adicional pós-offloading e lastro vigente, confrontados com os limitantes do manual.",
  "pontos_essenciais": [
   "condição real final de carregamento/inventário e distribuição a bordo",
   "incluir óleo remanescente, acréscimo pós-offloading e lastro vigente, não só o volume exportado"
  ],
  "explicacao": "Durante o offloading, o lastro deve compensar a massa que sai sem violar trim, banda e esforços do casco, então a referência correta é a condição real de massa e sua distribuição, não o balanço bruto de descarga. Como pode permanecer óleo a bordo e a planta pode continuar elevando o inventário depois da transferência, a verificação de estabilidade precisa usar essa condição final efetiva e compará-la aos limitantes formais de estabilidade e carregamento do manual.",
  "contexto": "Nota técnica: Gestão do lastro em paralelo ao offloading para controle de calado, trim, banda e esforços do casco\nResumo: Na operação de offloading, o sistema de lastro compensa a variação de carga causada pela transferência de petróleo para manter a unidade em condição segura de calado, trim, banda, estabilidade e carregamento estrutural. A lógica operacional é contínua e simultânea à transferência: quem perde carga tende a receber lastro, e quem ganha carga tende a descarregar lastro, sempre com distribuição de água compatível com as restrições do casco e do Manual de Operação.\nNota técnica: Controle de estabilidade do FPSO: critérios limitantes, atualização de pesos e capacidade de cálculo\nResumo: A gestão segura da estabilidade em uma unidade flutuante depende de três pilares interligados: critério limitante formalizado, base de pesos e centro de gravidade continuamente atualizada, e capacidade de cálculo em qualquer condição, inclusive blackout. A nota também separa claramente o que serve para estabilidade intacta do que não pode ser extrapolado para estabilidade avariada, evitando decisões operacionais baseadas em critérios inadequados.\nNota técnica: Gestão do inventário de óleo e da condição final do FPSO ao término do offloading\nResumo: A condição de estabilidade de um FPSO ao fim do offloading não é definida apenas pelo volume transferido ao navio aliviador, mas pelo inventário que permanece a bordo e por qualquer óleo adicional que continue entrando nos tanques se a planta seguir operando. No caso analisado da P-34, essa diferença foi material: parte do óleo foi mantida intencionalmente para atender ao Manual de Carregamento, Trim e Estabilidade, e a continuidade da planta elevou depois o inventário total nos tanques de carg…\nConhecimento que a questão deveria avaliar: Condição final do FPSO após offloading: lastro, inventário remanescente e estabilidade real. Ligação: Durante o offloading, a compensação por lastro não pode ser guiada apenas pelo volume descarregado, porque a condição final da unidade depende do inventário que permanece a bordo e até do óleo que continua entrando se a planta seguir operando. Isso afeta diretamente a validade do cálculo de estabilidade e a conformidade com os limitantes formais da unidade. Raciocínio exigido: A resposta correta exige integrar a lógica dinâmica do lastro com o controle formal de estabilidade e com a diferença…\n\nFatos das fontes usados na resposta (afirmação e trecho original):\n• O sistema de lastro é safety critical e controla a estabilidade, intacta ou avariada, pela movimentação de água do mar entre diferentes regiões da estrutura. Essa movimentação busca colocar a unidade em trim seguro e nivelado e manter os carregamentos estruturais, como esforço cortante, momento fletor e tensões torsionais, dentro dos limites permissíveis.\n  Trecho: \"The Ballast system is safety critical and is used to control the stability, whether intact or damaged, by moving sea water to or from various locations in the structure in order to bring the vessel to a safe and level trim\" [HSE (Reino Unido) · ed-loss-of-stability-and-positioning.pdf, p. 7]\n• Durante o descarregamento, a água de lastro é bombeada para tanques projetados e distribuídos por todo o casco da embarcação. Durante o carregamento, os tanques de lastro são inteiramente ou parcialmente descarregados.\n  Trecho: \"A água de lastro é bombeada para tanques projetados e especialmente distribuídos por todo o casco da embarcação durante o descarregamento. Durante o carregamento da embarcação os tanques de lastro são inteiramente ou parcialmente descarregados\" [REGIS · 22770_CT_COECI_2016_2_18.pdf]\n• Os limites de carga no convés e as restrições de carregamento dos tanques devem ser definidos no Operations Manual, tipicamente para evita…"
 },
 {
  "codigo": "Q006",
  "id": "ee74ce2b7b-s0000-A1",
  "topico": "Operações submarinas, poços, risers e equipamentos submarinos",
  "subtopico": "Sistema e operação de pull in de risers",
  "nivel": "Fácil",
  "dificuldade": "Fácil",
  "pergunta": "Em uma configuração de instalação com SLWR, como uma distância pré-fixada entre PLET e FPSO atua sobre a projeção horizontal da linha?",
  "resposta": "Ela funciona como um condicionante geométrico que limita a projeção horizontal da linha.",
  "pontos_essenciais": [
   "limita a projeção horizontal",
   "atua como condicionante geométrico da configuração SLWR"
  ],
  "explicacao": "Na configuração considerada, a distância definida entre PLET e FPSO não é apenas um afastamento de arranjo; ela impõe um limite geométrico ao vão horizontal da linha. Esse limite faz parte das restrições necessárias para viabilizar a configuração de SLWR.",
  "contexto": "Nota técnica: Restrições geométricas e pontos de conexão no pull-in de risers integrados ao posicionamento do FPSO\nResumo: No pull-in, a geometria admissível da linha não depende apenas do equipamento submarino, mas também da posição relativa entre a unidade flutuante e a infraestrutura submarina, além do local efetivo onde a linha é conectada. Os fatos disponíveis mostram dois condicionantes centrais em configurações analisadas: a necessidade de um ponto de conexão variável para acomodar variação de calado e a adoção de distância pré-fixada entre PLET e FPSO para limitar a projeção horizontal e viabilizar uma conf…\nConhecimento que a questão deveria avaliar: Identificar como uma distância pré-fixada entre PLET e FPSO pode atuar na limitação da projeção horizontal da linha em uma configuração de instalação de SLWR.\n\nFatos das fontes usados na resposta (afirmação e trecho original):\n• O projeto/planejamento da instalação impôs distância pré-fixada entre o PLET e o FPSO, limitando a projeção horizontal. Essa limitação está conectada às restrições geométricas necessárias para viabilizar a configuração do SLWR.\n  Trecho: \"distância pré-fixada entre o PLET e o FPSO li-mitando a projeção horizontal\" [Petrolês · corpusPublico(sem IBICT)-SemProcessamento.txt]"
 },
 {
  "codigo": "Q007",
  "id": "e9ca515f84-s0003-A1",
  "topico": "Operações submarinas, poços, risers e equipamentos submarinos",
  "subtopico": "Operações submarinas, poços, manifolds, PLEM e PLET",
  "nivel": "Média",
  "dificuldade": "Média",
  "pergunta": "Em um sistema submarino, a avaliação do fluido indica risco simultâneo de hidratos, incrustação e alta viscosidade do óleo. Qual razão técnica torna inadequado adotar uma única medida de garantia de escoamento para todo o sistema?",
  "resposta": "Porque mecanismos distintos de restrição ao escoamento exigem medidas diferentes, e a solução tecnicamente e economicamente adequada tende a combinar alternativas.",
  "pontos_essenciais": [
   "mecanismos distintos exigem medidas diferentes",
   "a solução adequada tende a combinar alternativas"
  ],
  "explicacao": "A garantia de escoamento cobre fenômenos diferentes, como hidratos, incrustações e problemas associados à baixa fluidez, que não são resolvidos por uma medida universal. Por isso, a seleção deve se basear no comportamento real do fluido e pode exigir combinação de alternativas para atender ao critério técnico e econômico.",
  "contexto": "Nota técnica: Estratégias de garantia de escoamento ao longo do ciclo de vida em sistemas submarinos\nResumo: Garantia de escoamento, em sistemas submarinos, não é uma ação pontual de operação, mas um conjunto de atividades que começa no projeto e continua durante toda a fase produtiva. O tratamento adequado exige prever os fenômenos que podem restringir o escoamento, selecionar barreiras preventivas e definir medidas de mitigação e remoção compatíveis com o fluido, a arquitetura submarina e o risco operacional.\nConhecimento que a questão deveria avaliar: Justificar tecnicamente por que a solução de garantia de escoamento para um sistema em projeto ou em operação pode exigir combinação de alternativas, em vez de uma única medida.\n\nFatos das fontes usados na resposta (afirmação e trecho original):\n• As atividades de garantia de escoamento incluem previsão, prevenção, mitigação e remoção de depósitos orgânicos como hidratos e parafinas e inorgânicos como incrustações. O conjunto de atividades também abrange a atuação sobre outros fenômenos como corrosão, emulsões, escoamento de óleos muito viscosos e golfadas severas.\n  Trecho: \"As atividades que abrangem a garantia de escoamento são a previsão, prevenção, mitigação e remoção de depósitos orgânicos, como hidratos e parafinas, inorgânicos, como as incrustações, além de outros fenômenos, como corrosão, emulsões, escoamento de óleos muito viscosos e golfadas severas (ANDREOLLI, 2016).\" [REGIS · 9539_BRUNO%20V%20M%20e%20J%c3%89SSICA%20C%20L%20LUSTOSA.pdf]\n• Mesmo com semelhanças entre óleos quanto ao ºAPI e composição, deve ser feita análise laboratorial a partir de amostras representativas para avaliar os principais problemas de garantia de escoamento e propor soluções técnica e economicamente viáveis.\n  Trecho: \"Sendo assim, ainda que entre óleos com ºAPI similares, são esperados comportamentos diferentes de garantia de escoamento. É necessária uma análise laboratorial dos fenômenos a partir de amostras representativas para que se possa avaliar os principais problemas que podem ocorrer para propor soluções técnica e economica…\" [REGIS · 9539_BRUNO%20V%20M%20e%20J%c3%89SSICA%20C%20L%20LUSTOSA.pdf]\n• Para um determinado projeto ou sistema em operação, normalmente não existe uma única solução. A solução mais adequada do ponto de vista econômico e técnico pode envolver uma combinação de várias alternativas.\n  Trecho: \"Normalmente não existe uma única solução para um determinado projeto ou sistema em operação Muitas vezes a solução mais adequada do ponto de vista econômico e técnico é uma combinação de várias alternativas\" [Petrolês · corpusPublico(sem IBICT)-SemProcessamento.txt]"
 },
 {
  "codigo": "Q008",
  "id": "ee74ce2b7b-s0001-A1",
  "topico": "Operações submarinas, poços, risers e equipamentos submarinos",
  "subtopico": "Sistema e operação de pull in de risers",
  "nivel": "Média",
  "dificuldade": "Média",
  "pergunta": "Na seleção de configurações de pull-in em um arranjo com múltiplos risers, por que o menor deslocamento transversal é um critério adequado para reduzir interferência entre linhas?",
  "resposta": "Porque menor deslocamento transversal indica menor afastamento lateral da configuração e, portanto, menor potencial de aproximação e interferência com os demais risers.",
  "pontos_essenciais": [
   "menor deslocamento transversal = menor afastamento lateral",
   "isso reduz o potencial de interferência entre risers"
  ],
  "explicacao": "O deslocamento transversal foi adotado como medida de interferência entre configurações. Ao selecionar configurações com menor valor desse deslocamento, reduz-se a ocupação lateral da linha no arranjo e, com isso, a chance de interação indesejada com outros risers.",
  "contexto": "Nota técnica: Definição geométrica e envelope de instalação do SLWR no pull-in\nResumo: O envelope admissível do SLWR durante o pull-in é definido pela combinação entre geometria disponível, limites construtivos já impostos ao topo do riser, projeção horizontal até o PLET e restrições da embarcação de instalação. A configuração viável não resulta de uma única variável isolada, mas da otimização simultânea de ângulo, posição de conexão, calado, interferência, carregamentos e critérios de integridade estrutural e operacional.\nConhecimento que a questão deveria avaliar: Explicar por que o deslocamento transversal pode ser usado como critério de seleção de configurações quando se deseja minimizar interferência entre risers.\n\nFatos das fontes usados na resposta (afirmação e trecho original):\n• Para o critério de interferência, foi feita medição do deslocamento transversal de cada configuração para possibilitar a escolha de configurações com menor deslocamento. O objetivo declarado é minimizar a interferência entre risers.\n  Trecho: \"para o critério de interferência foi feita uma medição do deslocamento transversal de cada configuração a fim de possibilitar a escolha de configurações com menor deslocamento de modo a minimizar a interferência entre risers\" [Petrolês · corpusPublico(sem IBICT)-SemProcessamento.txt]"
 },
 {
  "codigo": "Q009",
  "id": "ee74ce2b7b-s0007-A1",
  "topico": "Operações submarinas, poços, risers e equipamentos submarinos",
  "subtopico": "Sistema e operação de pull in de risers",
  "nivel": "Difícil (cenário em um conceito)",
  "dificuldade": "Difícil",
  "pergunta": "Durante o hang-off de um SLWR, a equipe verifica que o fator de utilização das tensões permanece abaixo do limite admissível, mas a transferência de carga faz o esforço axial no topo cruzar de tração para compressão por um curto intervalo antes da suportação definitiva assumir o peso. Qual é a causa técnica mais provável para essa condição ainda ser rejeitada?",
  "resposta": "Porque a compressão na junta de topo viola o critério de integridade da conexão superior, que deve permanecer em tração para preservar o flexjoint.",
  "pontos_essenciais": [
   "compressão na junta de topo é inadmissível",
   "a exigência existe para preservar o flexjoint"
  ],
  "explicacao": "A aceitabilidade não depende só da resistência global ou do fator de utilização. Na transferência de carga, o topo do riser deve permanecer trativo; se entrar em compressão, a condição viola um requisito explícito de preservação do flexjoint.",
  "contexto": "Nota técnica: Critérios de controle de carga axial no topo do riser durante hang-off e transferência para a suportação definitiva\nResumo: Na transferência de carga no topo do riser, o critério estrutural destacado é duplo: o fator de utilização das tensões, segundo a DNV, deve permanecer inferior a 1 e o esforço axial no topo deve permanecer em tração. A proibição de compressão na junta de topo está ligada à preservação do flexjoint, de modo que o controle operacional da transferência precisa manter a conexão superior carregada trativamente durante todo o hang-off e a passagem para a suportação definitiva.\nConhecimento que a questão deveria avaliar: Analisar um cenário de transferência em que a estrutura global ainda atende à resistência geral, mas o topo tende a perder tração, e decidir por que essa condição continua sendo rejeitável pela exigência de preservação do flexjoint.\n\nFatos das fontes usados na resposta (afirmação e trecho original):\n• A otimização impõe que o fator de utilização das tensões segundo a DNV seja inferior a 1. O esforço axial no topo deve ser restrito a forças de tração, não sendo admitidas forças compressivas na junta de topo para preservar o elemento de conexão (flexjoint).\n  Trecho: \"que o fator de utilização das tensões segundo a DNV (Det Norske Veritas, 2010) seja inferior a 1; que o esforço axial no topo seja restrito a forças de tração, não sendo admitidas forças compressivas na junta de topo, a fim de preservar o elemento de conexão (flexjoint)\" [REGIS · BPP_2011_6_1_2_11_Desafios_enfrentados_no_projeto_das_configuracoes.pdf]"
 },
 {
  "codigo": "Q010",
  "id": "e9ca515f84-s0002-A1",
  "topico": "Operações submarinas, poços, risers e equipamentos submarinos",
  "subtopico": "Operações submarinas, poços, manifolds, PLEM e PLET",
  "nivel": "Difícil (cenário em um conceito)",
  "dificuldade": "Difícil",
  "pergunta": "Durante o teste de um poço conectado a um manifold submarino, o trem de teste na unidade está disponível, mas o fluxo do poço não chega isolado ao circuito de teste. Qual é a causa operacional mais provável no alinhamento subsea?",
  "resposta": "O poço não foi comutado para a rota segregada de teste e permaneceu alinhado à rota de produção.",
  "pontos_essenciais": [
   "não houve comutação para a linha/rota de teste",
   "o poço permaneceu na rota de produção"
  ],
  "explicacao": "No manifold, cada template de produção dispõe de válvulas distintas para produção e para teste, de modo que o encaminhamento ao circuito de teste exige segregação da rota normal de produção. Se essa comutação não ocorre, o fluxo não segue isolado para o ramal de teste, que pode incluir choke específico até o equipamento de teste.",
  "contexto": "Nota técnica: Funções do manifold submarino e arranjo de válvulas para produção, teste e injeção\nResumo: O manifold submarino atua como nó de coleta e distribuição do sistema subsea: reúne a produção de poços ou templates, distribui fluidos de injeção e oferece caminhos distintos para produção normal e teste de poço. Seu arranjo de válvulas, tipicamente hidráulicas ON-OFF e organizado em paralelo por template, permite selecionar a rota de cada conexão, isolar linhas específicas e bloquear ou liberar escoamento por meio de válvulas de bloqueio e ESDV.\nConhecimento que a questão deveria avaliar: Explicar, com base no arranjo de válvulas do manifold, por que o encaminhamento de um poço para teste exige segregação da rota de produção e uso do caminho específico de teste.\n\nFatos das fontes usados na resposta (afirmação e trecho original):\n• As válvulas do manifold são arranjadas em paralelo em relação a cada template de produção e/ou injeção conectado. Atualmente, a maioria das válvulas do manifold é do tipo ON-OFF acionada hidraulicamente por piloto; para cada template de produção ligado ao manifold há pelo menos duas válvulas (uma para a linha de produção e outra para a linha de teste de poço).\n  Trecho: \"The valves are arranged in parallel in respect to each production/injection template. Currently, most manifold valves are hydraulically piloted, ON-OFF valves [4]. For every production template linked to the manifold, there are at least two valves: one for production line and other for well test line.\" [REGIS · 11051_PFC_2016-1%20Amadeu_Placido_Neto.pdf]\n• Um manifold de produção conjunto de válvulas e linhas é usado para direcionar cada um dos poços para um dos ramais existentes, tipicamente partindo de uma “planta de processo” com pelo menos um trem de produção e um trem de teste. Esse arranjo suporta o direcionamento do fluxo de produção para os equipamentos disponíveis.\n  Trecho: \"CNT MANIFOLD de produo conjunto de v8lrulas e linhas para dlrecionar cada um dos popas a um dos tens existentes Nmalmcmte uma planta de procas90 m u i peki menos um tram de produçgo e um trem de teste\" [Petrolês · corpusPublico(sem IBICT)-SemProcessamento.txt]\n• Para cada template de produção ligado ao manifold, há pelo menos duas válvulas (produção e teste de poço), enquanto árvores de injeção exigem uma válvula para cada caso. Além disso, cada linha de fluido diferente no manifold possui sua própria válvula de bloqueio (shut valve).\n  Trecho: \"Meanwhile, injection trees requires one valve each. Each different fluid line in the manifold also has its own shut valve.\" [REGIS · 11051_PFC_2016-1%20Amadeu_Placido_Neto.pdf]\n• Um manifold de teste com válvulas e linhas é usado para permitir o fluxo de um poço para o queimador/separador, passando por um choke específico. O objetivo é viabilizar a condução do fluxo do poço para o equipamento de teste/controlado.\n  Trecho: \"MANIFW de taste mnjuntc de v&lvulas e linhas para owihlar fluxo de um p o o para o quelmador separador passando por um chob tispeclfico\" [Petrolês · corpusPublico(sem IBICT)-SemProcessamento.txt]"
 },
 {
  "codigo": "Q011",
  "id": "96c4f33979-s0000-A1",
  "topico": "Produção e Processo (Medição Fiscal e Sistema de Alívio)",
  "subtopico": "Produção, processo e processamento do óleo",
  "nivel": "Fácil",
  "dificuldade": "Fácil",
  "pergunta": "Por que a corrente de gás passa por vários estágios de compressão ao longo do processo e, às vezes, também após o processamento?",
  "resposta": "Porque o gás perde pressão ao longo do processo e precisa ser recomprimido para atingir a pressão exigida no uso final.",
  "pontos_essenciais": [
   "perda de pressão ao longo do processo",
   "adequação à pressão requerida no destino final"
  ],
  "explicacao": "A compressão recompõe a pressão degradada durante o escoamento e o processamento. Além disso, a pressão de descarga necessária depende da finalidade da corrente, como gás combustível, gas lift, reinjeção ou envio para terra.",
  "contexto": "Nota técnica: Restrições de escoamento e compressão como fontes de perda de produção e consumo energético\nResumo: Restrições na linha de produção podem se manifestar por aumento de pressões a montante, queda de pressão na cabeça e redução de produção, servindo como indicação de perda de capacidade e necessidade de limpeza nas condições do procedimento citado. Em paralelo, a corrente de gás passa por vários estágios de compressão ao longo do processo e após o processamento para recompor perdas de pressão e atender à pressão exigida pelo uso final. A interpretação conjunta desses efeitos pode ser feita com b…\nConhecimento que a questão deveria avaliar: Identificar por que a corrente de gás passa por vários estágios de compressão ao longo do processo e após o processamento.\n\nFatos das fontes usados na resposta (afirmação e trecho original):\n• A corrente de gás passa por vários estágios de compressão ao longo do processo devido à perda de pressão e também após o processamento, dependendo do uso final. As pressões atingidas serão de acordo com a finalidade, incluindo gás combustível para geração de energia, gás para gas lift, reinjeção ou envio para tratamento em terra, além de consumo direto.\n  Trecho: \"A corrente de gás passa por vários estágios de compressão ao longo do processo devido à perda de pressão e também após o processamento a depender do seu uso final As pressões atingidas serão de acordo com a finalidade\" [Petrolês · corpusPublicoIBICT-SemProcessamento.txt]"
 },
 {
  "codigo": "Q012",
  "id": "9a7659b69d-s0001-A1",
  "topico": "Produção e Processo (Medição Fiscal e Sistema de Alívio)",
  "subtopico": "Operação Geral FPSO",
  "nivel": "Média",
  "dificuldade": "Média",
  "pergunta": "Após manutenção ou período ocioso, qual é a razão técnica para tratar a reintrodução de fluidos em um sistema de processo como gestão de mudança, em vez de simples retomada da operação normal?",
  "resposta": "Porque a condição do sistema pode ter mudado durante a intervenção ou o período ocioso, tornando necessário reavaliar perigos e controles antes de reintroduzir fluidos.",
  "pontos_essenciais": [
   "mudança de condição do sistema após manutenção/ociosidade",
   "necessidade de reavaliar perigos e controles antes da introdução de fluidos"
  ],
  "explicacao": "O sistema que retorna ao serviço não deve ser presumido igual ao que saiu de operação. Alterações ocorridas durante a manutenção, mudanças desde a emissão de permissões ou modificações ainda não implementadas podem invalidar os controles previstos, exigindo revisão formal antes do start-up.",
  "contexto": "Nota técnica: Controle operacional de partidas, paradas e retomada após intervenção em FPSOs\nResumo: Partidas, paradas e retorno ao serviço em sistemas de processo não são apenas mudanças de estado operacional: elas alteram barreiras, restabelecem inventário de hidrocarbonetos e expõem a instalação a riscos de liberação se isolamentos, juntas e condições de processo não forem confirmados. O material mostra que procedimentos claros, revisão de permissões, gestão de mudanças e verificação formal da condição do sistema antes da reintrodução de fluidos são controles centrais para evitar operação f…\nConhecimento que a questão deveria avaliar: Explicar por que o retorno de fluidos a um sistema após manutenção ou fase ociosa deve ser tratado como gestão de mudança, e não apenas como recomeço da operação normal.\n\nFatos das fontes usados na resposta (afirmação e trecho original):\n• Deve ser avaliado se algo mudou desde que o Permit foi emitido. A existência de mudança desde a emissão, junto com a necessidade de revisão, afeta a adequação dos perigos e controles previstos no PTW em andamento.\n  Trecho: \"f. Has anything changed since the Permit was issued?\" [HSE (Reino Unido) · ed-control-of-work.pdf, p. 8]\n• Quando houver gestão de mudança de projeto não implementada, deve-se avaliar os perigos e o impacto global da sua não implementação à segurança da unidade, por meio de abertura de Gestão de Mudança Temporária. Também deve-se estabelecer um prazo para implementação.\n  Trecho: \"• Implementar todas as gestões de mudança de projeto. Para eventuais Gestões de Mudança não implementadas, deve-se avaliar os perig os e o impacto global da sua não implementação à segurança da unidade, por meio de a bertura de Gestão de Mudança Temporária, bem como estabelecer um prazo para implementação (SGSO 16.2).\" [ANP · 2024, p. 71]\n• A introdução de fluidos em um sistema de processo que passou recentemente por manutenção ou ficou em fase ociosa apresenta perigos associados e pode ser tratada como uma forma específica de gestão de mudança. Controle ineficaz do processo foi fundamental para o desastre Piper Alpha.\n  Trecho: \"Introduction of fluids into a process system that has recently undergone maintenance activity, or has been in an idle phase, has a number of associated hazards, and can be addressed as a particular form of management of change. Ineffective control of this process was clearly fundamental to the Piper Alpha disaster.\" [HSE (Reino Unido) · inspection-of-loss-of-containment.pdf, p. 53]"
 },
 {
  "codigo": "Q013",
  "id": "9feff6fc72-s0000-A1",
  "topico": "Produção e Processo (Medição Fiscal e Sistema de Alívio)",
  "subtopico": "Tratamento do Gás produzido",
  "nivel": "Fácil",
  "dificuldade": "Fácil",
  "pergunta": "Em um diagrama de fases de gás em equilíbrio com água líquida, que condição é representada por um ponto situado sobre a curva de hidrato?",
  "resposta": "A formação incipiente de hidrato, isto é, a condição de equilíbrio em que a fase hidrato começa a se formar.",
  "pontos_essenciais": [
   "formação incipiente de hidrato"
  ],
  "explicacao": "Sobre a curva de hidrato está o limite termodinâmico de mudança de fase. Acima da curva o hidrato já é estável e abaixo dela o hidrato não se forma.",
  "contexto": "Nota técnica: Equilíbrio de fases e formação incipiente de hidratos no gás produzido\nResumo: A formação de hidratos no gás produzido pode ser tratada como um problema de equilíbrio de fases entre gás, água líquida e fase hidrato. Para uma temperatura e uma composição gasosa dadas, calcula-se uma pressão de equilíbrio; comparando essa pressão com a pressão atuante do sistema, decide-se se a condição está na região de formação de hidratos ou fora dela, o que também pode ser interpretado em diagramas de fases.\nConhecimento que a questão deveria avaliar: Interpretar a curva de hidrato em um diagrama de fases, distinguindo condição sobre a curva, acima da curva e abaixo da curva.\n\nFatos das fontes usados na resposta (afirmação e trecho original):\n• Para sistemas gasosos em equilíbrio com água líquida, a região de interesse é aquela à direita da curva vertical do ponto de congelamento da água, mais especificamente a curva de hidrato. Observa-se que a formação de hidratos inicia sobre a curva; acima dela o hidrato já se formou; abaixo da curva o hidrato não se forma, sendo o foco obter valores de equilíbrio referentes à formação incipiente de…\n  Trecho: \"Em síntese, sempre se está interessado em obter os valores de equilíbrio, referentes à formação incipiente de hidratos para um determinado sistema em análise. Figura 5.1: Diagrama de fases para Sistemas de\" [REGIS · 5043_Rossi_LucianoFernandodosSantos_M.pdf]"
 },
 {
  "codigo": "Q014",
  "id": "e8459723b0-s0002-A1",
  "topico": "Produção e Processo (Medição Fiscal e Sistema de Alívio)",
  "subtopico": "Sistema de Alívio e Flare",
  "nivel": "Difícil (cenário em um conceito)",
  "dificuldade": "Difícil",
  "pergunta": "Na revisão de uma PSV de um separador, foram calculadas áreas requeridas de 3,8 cm² para bloqueio de saída, 5,1 cm² para fogo externo e 4,4 cm² para falha de controle. A operação percebe o bloqueio de saída como o evento mais severo. Qual cenário deve governar a seleção do orifício da PSV?",
  "resposta": "Fogo externo, porque é o caso com a maior área de alívio requerida e, portanto, o caso dimensionante do orifício.",
  "pontos_essenciais": [
   "identificar fogo externo como caso dimensionante",
   "relacionar a escolha ao maior valor de área requerida"
  ],
  "explicacao": "Na seleção da PSV, o caso dimensionante é o cenário que exige a maior área de alívio calculada, não o que parece mais severo operacionalmente. Depois disso, o orifício deve ser escolhido com área selecionada compatível com essa área requerida.",
  "contexto": "Nota técnica: Bases de seleção e dimensionamento de PSV a partir do sistema protegido\nResumo: A base de projeto de uma PSV começa pela definição do sistema de processo efetivamente protegido, isto é, o inventário que permanece na mesma condição de pressão e temperatura sem bloqueios internos. A partir desse inventário, o ajuste da válvula deve respeitar o limite do elemento mais suscetível a danos, e o dimensionamento deve comparar todos os cenários de sobrepressão, calculando a área requerida em cada um para então selecionar o orifício correspondente ao pior caso aplicável.\nConhecimento que a questão deveria avaliar: Dado um sistema protegido com múltiplos cenários de sobrepressão e diferentes áreas requeridas calculadas, justificar qual cenário é dimensionante e como isso governa a seleção do orifício da PSV, mesmo quando outro cenário pareça mais severo por percepção operacional.\n\nFatos das fontes usados na resposta (afirmação e trecho original):\n• O caso que apresentar maior área de alívio corresponde ao caso dimensionante da válvula. O dimensionamento da PSV é definido pelo tipo de orifício, em que cada orifício corresponde a uma área selecionada.\n  Trecho: \"O cenário que apresentar maior área corresponde ao caso dimensionante da válvula O dimensionamento da PSV é definido pelo tipo de orifício onde cada orifício corresponde á uma área selecionada\" [Petrolês · corpusPublico(sem IBICT)-SemProcessamento.txt]\n• O dimensionamento estático convencional de uma PSV requer o cálculo da vazão e das propriedades da corrente de alívio para cada cenário de sobrepressão ao qual o equipamento protegido está sujeito.\n  Trecho: \"O dimensionamento estático convencional de uma PSV requer o cálculo da vazão e das propriedades da corrente de alívio para cada cenário de sobrepressão que o equipamento a ser protegido está sujeito\" [Petrolês · corpusPublico(sem IBICT)-SemProcessamento.txt]\n• O orifício da PSV deve ser escolhido de forma que sua área selecionada seja compatível com a área requerida para o caso dimensionante. A correlação entre orifício e área selecionada é fornecida em tabela, e os valores tabelados seguem as equações de dimensionamento descritas no API.\n  Trecho: \"A Tabela <NUMBER> fornece a correlação entre orifício e área selecionada de PSV Vale ressaltar que os valores tabelados de área selecionada seguem as equações de dimensionamento descritas no API <NUMBER> parte <NUMBER> Tais equações são fornecidas neste item\" [Petrolês · corpusPublico(sem IBICT)-SemProcessamento.txt]"
 },
 {
  "codigo": "Q015",
  "id": "69f5898918-s0000-A1",
  "topico": "Produção e Processo (Medição Fiscal e Sistema de Alívio)",
  "subtopico": "Sistema de captação e tratamento de água do mar para injeção no reservatório",
  "nivel": "Fácil",
  "dificuldade": "Fácil",
  "pergunta": "Como a dureza e a baixa solubilidade das incrustações influenciam a estratégia operacional de tratamento na injeção de água?",
  "resposta": "Elas impõem estratégia predominantemente preventiva, com uso de anti-incrustante antes da deposição, em vez de depender de remoção corretiva periódica.",
  "pontos_essenciais": [
   "estratégia preventiva",
   "evitar dependência de remoção corretiva periódica"
  ],
  "explicacao": "Como a incrustação formada é dura e pouco solúvel, há poucos processos eficazes de remoção. Por isso, a operação deve priorizar prevenção química antes da deposição, reduzindo intervenções corretivas demoradas e custosas.",
  "contexto": "Nota técnica: Prevenção de incrustação na injeção de água e uso de métodos preditivos para selecionar anti-incrustantes\nResumo: Na injeção de água para reservatórios, o controle de incrustação deve ser predominantemente preventivo porque, uma vez formada, a incrustação tende a ser dura, pouco solúvel e de remoção difícil, com consumo elevado de tempo e recursos em intervenções periódicas. Métodos preditivos ajudam a antecipar a tendência de precipitação e, com isso, apoiam a escolha do tipo e da quantidade de inibidor mais adequados, reduzindo a dependência de ações corretivas e permitindo aplicação química mais criteri…\nConhecimento que a questão deveria avaliar: Descrever como a dureza e a baixa solubilidade das incrustações influenciam a estratégia operacional de tratamento.\n\nFatos das fontes usados na resposta (afirmação e trecho original):\n• Como essas incrustações são duras e de relativamente baixa solubilidade, existem poucos processos para remoção e são citadas medidas preventivas como uso de tratamentos químicos com antiincrustantes. Também é indicado que há muito gasto de tempo e de recursos com intervenções periódicas, além de existirem restrições ambientais para esse tipo de tratamento químico.\n  Trecho: \"Como estas incrustações são duras e relativamente de baixa solubilidade existem apenas alguns processos para a sua remoção e medidas preventivas tais como o uso de tratamentos químicos com antiincrustantes Entretanto há muito gasto de tempo e de recursos com intervenções periódicas e além disso hoje existem restrições…\" [Petrolês · corpusPublico(sem IBICT)-SemProcessamento.txt]"
 },
 {
  "codigo": "Q016",
  "id": "202d9e591b-s0000-A1",
  "topico": "Segurança Operacional, SGSO, Sistemas de Segurança e Gestão de Riscos",
  "subtopico": "Segurança e Controle de Riscos",
  "nivel": "Fácil",
  "dificuldade": "Fácil",
  "pergunta": "Que papel o DDS/toolbox deve cumprir quando a tarefa é regida por um procedimento operacional crítico derivado da análise de risco?",
  "resposta": "Apoiar a execução segura em campo, reforçando perigos, mitigadores e aderência ao procedimento, sem substituir a salvaguarda procedural.",
  "pontos_essenciais": [
   "apoia a execução segura em campo",
   "reforça aderência ao procedimento crítico, sem substituí-lo"
  ],
  "explicacao": "O procedimento operacional crítico funciona como salvaguarda ligada à análise de risco. O DDS/toolbox agrega valor ao comunicar perigos e mitigadores da tarefa e ao reforçar, sob supervisão, o cumprimento das instruções, permissões e procedimentos aplicáveis.",
  "contexto": "Nota técnica: DDS/toolbox e ferramentas de avaliação operacional: comunicação, capacitação, aderência procedimental e efetivo como base da execução segura\nResumo: Ferramentas como DDS/toolbox, APR e AST só controlam risco na prática quando a informação sobre o trabalho chega às pessoas certas, com perigos e mitigadores explicitados, e quando a equipe tem capacitação verificada para executar o previsto. A execução segura também depende de supervisão cotidiana que confira aderência a instruções, permissões e procedimentos, além de efetivo dimensionado para realizar tarefas críticas e responder a emergências sem atrasos indevidos por falta de pessoal.\nConhecimento que a questão deveria avaliar: Explicar a relação entre procedimento operacional crítico, análise de risco e ferramentas pré-tarefa, indicando como DDS/toolbox pode apoiar a execução segura em campo sem substituir o procedimento.\n\nFatos das fontes usados na resposta (afirmação e trecho original):\n• Procedimentos operacionais críticos são, em suma, salvaguardas de análises de risco para cenários de alta severidade, ou aqueles cuja execução já tenha sido fonte de incidentes. Também são relacionados às ações humanas descritas em planos de contingência.\n  Trecho: \"Procedimentos operacionais críDcos são, em suma, aqueles que são salvaguardas de análises de risco para cenários de alta severidade, ou cuja execução já tenha sido fonte de incidentes. Ações humanas descritas em planos de conDngência (derivadas, por exemplo, de uma gestão de mudança de projeto)\" [ANP · Nota Técnica nº 06/2023, p. 4]\n• Tool box meetings podem ser usados para apoiar a execução segura das tarefas. A eficácia depende de garantir que as pessoas no trabalho adiram às instruções/procedimentos do worksite ou aos work permits durante as rotinas diárias de supervisão.\n  Trecho: \"This can be achieved through tool box meetings, and ensure the people at work adhere to the given worksite instructions / procedures or work permits during their daily routine supervisory tours of the work place\" [HSE (Reino Unido) · Supervision audit report, p. 65]\n• BSEE recomenda que operadores e contratadas de OCS assegurem que os componentes do SEMS sejam abrangentes, compreendidos, seguidos por todo o pessoal e aplicados em todas as atividades de trabalho em OCS. Ao comunicar instruções de trabalho, deve-se considerar destacar os perigos potenciais e as etapas de mitigação incorporadas nos planos e procedimentos de trabalho.\n  Trecho: \"BSEE recommends that all OCS Operators and Contractors ensure that the components of your Safety and Environmental Management System (SEMS) are comprehensive, understood, followed by all personnel and enforced during all OCS work activities. • When communicating work instructions, consider highlighting the potential h…\" [BSEE (EUA) · Safety Alert 317 - Catastrophic Incident Avoided - June 12, 2015, p. 2]"
 },
 {
  "codigo": "Q017",
  "id": "202d9e591b-s0001-A1",
  "topico": "Segurança Operacional, SGSO, Sistemas de Segurança e Gestão de Riscos",
  "subtopico": "Segurança e Controle de Riscos",
  "nivel": "Média",
  "dificuldade": "Média",
  "pergunta": "Em uma PTW para serviço em área classificada, foi marcado que as ferramentas não geram centelha, faísca ou eletricidade estática, mas a atividade real inclui corte com maçarico, solda ou uso de lixadeira elétrica. Esse desvio caracteriza principalmente qual falha?",
  "resposta": "Falha de identificação formal do perigo na emissão da PTW, não mera falha documental.",
  "pontos_essenciais": [
   "identificação formal do perigo",
   "não é apenas erro documental"
  ],
  "explicacao": "Há incompatibilidade objetiva entre o perigo inerente à atividade e o que foi registrado na permissão. Como essas ferramentas podem gerar ignição em área classificada, a marcação incorreta indica que o perigo não foi reconhecido adequadamente na emissão da PTW.",
  "contexto": "Nota técnica: PTW em áreas classificadas e sistemas de hidrocarbonetos: reconhecimento de ignição, cenários de evento maior e gestão de salvaguardas afetadas\nResumo: A Permissão para Trabalho não deve apenas autorizar a tarefa: ela precisa explicitar o perigo principal, as fontes de ignição envolvidas, o pior cenário plausível e os controles que mantêm a atividade dentro de uma condição aceitável. Em trabalhos a quente e intervenções intrusivas em sistemas de hidrocarbonetos, falhas de identificação do perigo, comunicação deficiente e bypasses mal geridos podem degradar salvaguardas justamente quando o potencial de incêndio ou explosão é maior.\nConhecimento que a questão deveria avaliar: Distinguir uma falha meramente documental de uma falha de identificação de perigo em uma PTW, a partir de inconsistências entre a resposta marcada e os perigos inerentes às ferramentas e à atividade executada em área classificada.\n\nFatos das fontes usados na resposta (afirmação e trecho original):\n• Em resposta a “Os equipamentos para execução deste trabalho oferecem risco de gerar centelha, faíscas ou eletricidade estática quando forem usados em área classificada”, a marcação foi “NÃO”. A Análise Preliminar de Nível 2, com campos padronizados por atividade, reconhece liberação de faíscas e fagulhas em atividades de corte com maçarico, solda e preparação de superfície com lixadeira elétrica.\n  Trecho: \"introduzido pela utilização de algumas ferramentas. Para a questão: “Os equipamentos para execução deste trabalho oferecem risco de gerar centelha, faíscas ou eletricidade estática quando forem usados em área classificada ”, a resposta assinalada foi “NÃO”, sendo que a Análise Preliminar de Nível 2, com seus campos pr…\" [ANP · Relatório de Investigação do acidente de incêndio ocorrido na plataforma P-48 e…, p. 32]\n• Exemplos de atividades de alto risco em que pode ser necessário usar um procedimento escrito de PTW incluem trabalhos a quente como soldagem, entrada em vasos, corte em tubulações que carregam substâncias perigosas e trabalhos que exigem isolamento elétrico ou mecânico.\n  Trecho: \"Examples of high-risk jobs where a written permit to work procedure may need to be used include hot work such as welding, vessel entry, cutting into pipe-work carrying hazardous substances, and work that requires electr ical or mechanical isolation.\" [HSE (Reino Unido) · ed-control-of-work.pdf, p. 3]"
 },
 {
  "codigo": "Q018",
  "id": "fadd3bccc0-s0003-A1",
  "topico": "Segurança Operacional, SGSO, Sistemas de Segurança e Gestão de Riscos",
  "subtopico": "Operações simultâneas – SIMOPS",
  "nivel": "Média",
  "dificuldade": "Média",
  "pergunta": "Em SIMOPS, uma modificação planejada já foi comunicada à equipe impactada e refletida na documentação. Durante a execução, surge um perigo não previsto na instalação. Qual comunicação é exigida nesse momento, em contraste com a comunicação prévia da mudança planejada?",
  "resposta": "Comunicar o perigo ao Operador da Instalação; a comunicação prévia da mudança serve para preparar os impactados e refletir a nova condição na documentação.",
  "pontos_essenciais": [
   "comunicação do perigo ao Operador da Instalação",
   "contraste: a comunicação prévia da mudança prepara os impactados e atualiza a documentação da nova condição"
  ],
  "explicacao": "Se um perigo é identificado durante a atividade, ele deve ser comunicado ao Operador da Instalação. Isso é diferente da comunicação prévia de uma mudança planejada, que ocorre para alinhar a força de trabalho impactada e os documentos à condição modificada da instalação.",
  "contexto": "Nota técnica: Comunicação de mudanças, perigos e impacto em barreiras em SIMOPS\nResumo: Em operações simultâneas, a comunicação de mudanças operacionais ou de engenharia não é apenas informativa: ela precisa transferir para a força de trabalho uma compreensão atualizada da configuração real da instalação, dos perigos introduzidos e das barreiras afetadas. Para preservar a segurança operacional, essa comunicação deve estar refletida em documentos, desenhos, procedimentos e na coordenação contínua entre gerência e equipes, além de sustentar o reporte de perigos e a reênfase do stop…\nConhecimento que a questão deveria avaliar: Explicar o papel do reporte de perigo ao Operador da Instalação e sua diferença em relação à comunicação prévia de mudança planejada.\n\nFatos das fontes usados na resposta (afirmação e trecho original):\n• A comunicação ao Operador da Instalação deve ocorrer sempre que qualquer perigo identificado na Instalação for encontrado. Essa comunicação visa garantir que o Operador tome conhecimento do perigo identificado.\n  Trecho: \"e d) comuniquem ao Operador da Instalação qualquer perigo identificado na Instalação.\" [ANP · Regulamento Técnico do SGSO, p. 17]\n• Quando aplicável, deve ser realizado treinamento e comunicação para toda a Força de Trabalho impactada pela mudança. Essa ação ocorre no contexto da descrição e preparação da mudança.\n  Trecho: \"17.2.2.10 Treinamento, quando aplicável, e comunicação para toda a Força de Trabalho impactada pela mudança.\" [ANP · Regime de Segurança Operacional de Sistemas Submarinos e o Regulamento Técnico…, p. 42]\n• Devem ser identificados, divulgados e coordenados os impactos potenciais da instalação do TE nos sistemas de segurança e nas barreiras existentes. Deve-se atualizar desenhos de classificação de áreas, rotas de fuga, e garantir que as mudanças sejam refletidas em documentos de engenharia e que pessoal apropriado seja informado.\n  Trecho: \"Ensuring the potential impacts of the TE’s installation on existing safety systems and barriers are identified, publicized, and coordinated, and area classification drawings, egress routes, etc. are updated. • Updating existing engineering drawings and documents to reflect all operational changes and informing all app…\" [BSEE (EUA) · bsee-safety-alert-449-temporary-equipment-as-a-potential-source-of-ignition-on-…, p. 2]"
 },
 {
  "codigo": "Q019",
  "id": "d99fb5d8d3-s0002-A1",
  "topico": "Segurança Operacional, SGSO, Sistemas de Segurança e Gestão de Riscos",
  "subtopico": "SGSO",
  "nivel": "Difícil (cenário em um conceito)",
  "dificuldade": "Difícil",
  "pergunta": "Em uma FPSO, uma modificação já entrou em operação, mas o procedimento associado circula em rede interna fora do controle documental, sem revisão válida. Não há registros de treinamento nem de avaliação de aplicabilidade pela equipe, e o close out não traz evidência de atualização documental ou confirmação com operação e manutenção. Qual conclusão de conformidade é tecnicamente mais adequada?",
  "resposta": "A mudança não pode ser considerada adequadamente encerrada nem com risco comprovadamente sob controle.",
  "pontos_essenciais": [
   "a mudança não está adequadamente encerrada",
   "não há demonstração de controle do risco"
  ],
  "explicacao": "A existência física da modificação ou de um procedimento disponível não basta. Sem controle documental válido, registros de treinamento/aplicabilidade e evidência de close out com atualização documental e confirmação junto às equipes afetadas, falta a trilha objetiva que demonstra implementação efetiva e manutenção do controle do risco.",
  "contexto": "Nota técnica: Evidências documentais, registros e rastreabilidade para demonstrar conformidade do SGSO\nResumo: A demonstração de conformidade do SGSO não depende apenas de procedimentos escritos, mas da existência de registros controlados que provem que mudanças, treinamentos, atualizações documentais e ações corretivas foram efetivamente avaliados, autorizados, implementados e encerrados. Quando esses registros são íntegros, recuperáveis e rastreáveis, é possível verificar a conformidade e a gestão real do risco; quando faltam controle documental, revisão e evidência de capacitação, o sistema perde cap…\nConhecimento que a questão deveria avaliar: Analisar como falhas combinadas de controle documental, ausência de treinamento em procedimentos operacionais e falta de evidência de close out enfraquecem a demonstração de que o risco de uma mudança permanece gerenciado.\n\nFatos das fontes usados na resposta (afirmação e trecho original):\n• Para uma mudança concluída, deve-se revisar a documentação atualizada para confirmar que foi devidamente concluída e, se aplicável, revisar registros de treinamento. Também deve-se revisar treinamento e requisitos de close out ao selecionar mudanças de diferentes tipos.\n  Trecho: \"For a completed change, review the documentation which has been updated to confirm it has been suitably completed. Review training records if applicable.\" [HSE (Reino Unido) · inspection-of-loss-of-containment.pdf, p. 63]\n• Procedimentos antigos foram disponibilizados em rede interna sem atualização e fora do procedimento estabelecido de controle de documentos da empresa. Essa falta de controle de informação por meios diferentes desencorajou o uso do procedimento, tornando-o ineficiente para controle de risco operacional.\n  Trecho: \"BW Offshore (MS), it was decided to make available the old procedures of the unit, which had not been updated in the internal network to the FPSO Cidade de São Mateus , outside the established document control procedure in the company\" [ANP · ANP Final Report FPSO (english version), p. 191]\n• A BW Offshore não tinha um processo de treinamento que incluísse treinamento em procedimentos operacionais, de modo que não havia evidência de que a equipe do “navy team” da FPSO Cidade de São Mateus tivesse domínio dos requisitos do procedimento. Também foi constatado que a aplicabilidade do procedimento não havia sido avaliada pela equipe.\n  Trecho: \"However, since the BW had no training process that includes training in operational procedures, there is no evidence that the FPSO CDSM navy team had domain of the requirements of this procedure. It was found that the applicability of the procedure\" [ANP · ANP Final Report FPSO (english version), p. 191]\n• A inspeção deve revisar mudanças com pessoal offshore para garantir que pessoas de operação e manutenção estejam cientes das mudanças e de suas implicações. Materiais concernentes incluem cenários de falta de treinamento e treinamento não atualizado para planta e equipamentos novos ou modificados.\n  Trecho: \"Review changes with offshore personnel. Ensure that operations and maintenance personnel are aware of changes and the implications of them.\" [HSE (Reino Unido) · inspection-of-loss-of-containment.pdf, p. 63]"
 },
 {
  "codigo": "Q020",
  "id": "bfc6625c3d-s0000-A1",
  "topico": "Segurança Operacional, SGSO, Sistemas de Segurança e Gestão de Riscos",
  "subtopico": "Sistemas e equipamentos de salvatagem",
  "nivel": "Fácil",
  "dificuldade": "Fácil",
  "pergunta": "Quais meios de descida ao nível do mar não são considerados controlados no abandono por life raft por dependerem de força e destreza do usuário?",
  "resposta": "Cordas com nós e redes de escalada.",
  "pontos_essenciais": [
   "mencionar cordas com nós",
   "mencionar redes de escalada"
  ],
  "explicacao": "Esses meios exigem força e destreza sob emergência, por isso não recebem crédito como descida controlada. Meios controlados são aqueles que permitem chegar ao nível do mar com maior estabilidade e previsibilidade.",
  "contexto": "Nota técnica: Condições de acesso, descida ao mar e lançamento seguro de life rafts\nResumo: A executabilidade do abandono por life raft depende de uma cadeia contínua: chegar por rota disponível, descer por meio controlado, alcançar a embarcação sem cair na água e lançar/embarcar com proteção e iluminação adequadas. Os fatos fornecidos sustentam critérios de acesso, descida e lançamento que reduzem a exposição a radiação térmica, fumaça e à entrada física no mar, tratada como último recurso.\nConhecimento que a questão deveria avaliar: Distinguir meios controlados de descida ao nível do mar de meios que dependem de força e destreza do usuário.\n\nFatos das fontes usados na resposta (afirmação e trecho original):\n• Entrada física no mar como parte da fuga deve ser considerada como último recurso. Donuts, escape chutes e escadas fixas são meios controlados de descida ao nível do mar; cordas com nós e redes de escalada que exigem força e destreza não são meios controlados de descida.\n  Trecho: \"Physically entering the sea as part of escape should be regarded as a last resort. Systems such as Donuts, escape chutes and fixed ladders are acceptable controlled means of descent to sea level. Knotted ropes and scramble nets which require strength and dexterity to use are not considered as a controlled means of des…\" [HSE (Reino Unido) · ed-evacuation-escape-rescue.pdf, p. 40]"
 },
 {
  "codigo": "Q021",
  "id": "470390a408-s0008-A1",
  "topico": "Utilidades, geração de energia e sistemas auxiliares",
  "subtopico": "Geração e distribuição de energia elétrica",
  "nivel": "Fácil",
  "dificuldade": "Fácil",
  "pergunta": "Qual é a função dos sistemas de controle da geração e da distribuição elétrica em unidades offshore com demanda variável?",
  "resposta": "Manter a qualidade da energia, controlando tensão e frequência dentro de limites aceitáveis.",
  "pontos_essenciais": [
   "manter a qualidade da energia",
   "tensão e frequência dentro de limites aceitáveis"
  ],
  "explicacao": "Em unidades offshore, a demanda pode variar fortemente entre modos operacionais, e parte das cargas não tolera grandes desvios elétricos. Por isso, os sistemas de controle devem manter tensão e frequência dentro dos limites aplicáveis de qualidade de energia.",
  "contexto": "Nota técnica: Quedas e oscilações de tensão e frequência em sistemas elétricos offshore com geração local e carga variável\nResumo: Em unidades marítimas com geração local, desvios de tensão e frequência surgem quando a geração, a excitação e o compartilhamento de carga não acompanham perturbações rápidas de demanda ou de configuração do sistema. A combinação de grandes partidas, perda súbita de carga, falha de regulação e sincronização inadequada pode iniciar oscilações, perda de geração e blackout, especialmente em arranjos sujeitos a degraus de potência de alta magnitude.\nConhecimento que a questão deveria avaliar: Relacionar a função dos sistemas de controle da geração com a manutenção da qualidade de energia dentro de limites aceitáveis.\n\nFatos das fontes usados na resposta (afirmação e trecho original):\n• A alta variabilidade da demanda de potência em navios torna a qualidade da eletricidade muito importante, pois alguns equipamentos não suportam grandes faixas de variação de frequência ou tensão. A potência pode apresentar variações em etapas que chegam a alguns megawatts.\n  Trecho: \"As there is a high variability of the power demand in ships and sometimes the power step can reach some megawatts the quality of the electricity became very important as some equipments does not support a large range of variation in frequency or voltage\" [REGIS · 13301_GiovaniGiulioTristaoThibesVieiraOrig18.pdf]\n• Requisitos para sistemas de energia de navios devem manter a qualidade de potência em níveis aceitáveis, e sistemas de controle são importantes para manter o sistema operando dentro dos limites de padrões. O texto também vincula a existência de múltiplas condições operacionais (DP, manobras, standby sea voyage, porto/harbour) a mudanças significativas na demanda.\n  Trecho: \"This section discuss the requirements that ship power systems must attend to maintain in acceptable levels its power quality, it also discuss the importance of control systems to keep the system running under the limits of the standards\" [REGIS · 13301_GiovaniGiulioTristaoThibesVieiraOrig18.pdf]\n• Foram criadas normas internacionais para estabelecer limites de variação de frequência e tensão. Esses limites são associados à manutenção da qualidade de potência em níveis aceitáveis sob operação com demanda variável.\n  Trecho: \"International standards were created aiming at stablish limits of variation in frequency and voltage\" [REGIS · 13301_GiovaniGiulioTristaoThibesVieiraOrig18.pdf]"
 },
 {
  "codigo": "Q022",
  "id": "028022ae6b-s0001-A1",
  "topico": "Utilidades, geração de energia e sistemas auxiliares",
  "subtopico": "Sistema de utilidades",
  "nivel": "Média",
  "dificuldade": "Média",
  "pergunta": "Em um sistema de ar comprimido avaliado em regime permanente, por que a estimativa de potência e de consumo de combustível do compressor depende de perfis de pressão e temperatura, vazões, volumes e propriedades do gás?",
  "resposta": "Porque essas variáveis definem o estado hidráulico e termodinâmico do gás e, portanto, a carga de compressão que determina a potência requerida e o consumo de combustível.",
  "pontos_essenciais": [
   "definem o estado hidráulico/termodinâmico do gás",
   "determinam a carga de compressão, logo potência e combustível"
  ],
  "explicacao": "A potência do compressor não depende só da vazão isoladamente, mas da combinação entre pressão, temperatura, volumes, velocidades e propriedades do gás que caracteriza a compressão exigida no sistema. Em regime permanente, é esse conjunto de variáveis do modelo que sustenta o cálculo da potência estimada e do combustível necessário.",
  "contexto": "Nota técnica: Requisitos de pressão e capacidade na geração e distribuição de ar comprimido\nResumo: O dimensionamento de um sistema de ar comprimido depende de compatibilizar a pressão requerida no ponto de uso com a vazão demandada e com as perdas de carga ao longo da rede. Em regime permanente, essas variáveis também sustentam a estimativa da potência e do consumo de combustível dos compressores, além de orientar o dimensionamento das tubulações e a avaliação dos componentes inseridos na malha.\nConhecimento que a questão deveria avaliar: Explicar por que a estimativa de potência e de consumo de combustível do compressor depende de perfis de pressão e temperatura, vazões, volumes e propriedades do gás.\n\nFatos das fontes usados na resposta (afirmação e trecho original):\n• A ferramenta permite análise para gás natural ou fluidos compressíveis, mas modela apenas regime permanente, não permitindo análise de resposta no tempo. Como informações do sistema, pode-se incluir propriedades do gás em um ponto específico, além de perfis de temperatura e pressão ao longo da tubulação.\n  Trecho: \"inclui reguladores compressores válvulas reservatórios e elementos de ajuste Permite a analise para gás natural ou fluidos compressíveis no entanto modela somente regime permanente não permitindo a analise de resposta no tempo Como informações fornecidas pelo sistema pode-se incluir propriedades do gás em um ponto esp…\" [Petrolês · corpusPublicoIBICT-SemProcessamento.txt]\n• A partir das informações do modelo, o sistema pode calcular potência estimada e requisitos de combustível para compressores. Esse cálculo é suportado pelos dados incluídos como vazões, velocidades, volumes, perfis de temperatura e pressão e propriedades do gás em pontos especificados.\n  Trecho: \"Além disso pode indicar coeficientes de vazão para reguladores e calcular potência estimada e requisitos de combustível para compressores\" [Petrolês · corpusPublicoIBICT-SemProcessamento.txt]"
 },
 {
  "codigo": "Q023",
  "id": "470390a408-s0006-A1",
  "topico": "Utilidades, geração de energia e sistemas auxiliares",
  "subtopico": "Geração e distribuição de energia elétrica",
  "nivel": "Média",
  "dificuldade": "Média",
  "pergunta": "Na introdução de equipamento temporário que interfere em barreiras existentes, qual condição de integração deve ser confirmada antes da partida para que a resposta de segurança da instalação permaneça coerente com o arranjo real?",
  "resposta": "A mudança deve estar integralmente refletida nos detectores de gás, diagramas de alarme, lógica de ESD, desenhos de classificação de áreas, rotas de fuga e demais documentos de engenharia, com comunicação e treinamento correspondentes.",
  "pontos_essenciais": [
   "atualização coerente das interfaces de segurança e da documentação de engenharia",
   "abrange detectores/alarmes/lógica de ESD e desenhos como classificação de áreas e rotas de fuga"
  ],
  "explicacao": "A introdução de equipamento temporário pode alterar barreiras e criar perigos não previstos se o estado real da planta deixar de coincidir com a detecção, a alarmística, a lógica de desligamento e a documentação operacional. Por isso, antes da partida, é necessário confirmar que a modificação foi incorporada de forma consistente aos sistemas de segurança, aos desenhos e à preparação do pessoal afetado.",
  "contexto": "Nota técnica: Gestão de bypass do ESD e preservação das interfaces elétricas durante manutenção e introdução de equipamento temporário\nResumo: Quando o ESD é colocado em bypass, a instalação passa a operar com uma barreira crítica degradada, elevando a exposição a incêndio, explosão, inalação e outros perigos operacionais. Em intervenções no sistema elétrico ou na introdução de equipamento temporário, a redução desse risco depende de MOC/LOTO aprovados, PSSR antes da partida, avaliação de impactos nas barreiras existentes e atualização coerente de lógica, alarmes, detectores, desenhos e treinamento.\nConhecimento que a questão deveria avaliar: Relacionar a introdução de equipamento temporário com a necessidade de atualizar detectores de gás, diagramas de alarme, lógica de ESD, desenhos de classificação de áreas, rotas de fuga e demais documentos de engenharia.\n\nFatos das fontes usados na resposta (afirmação e trecho original):\n• A implementação de equipamento temporário (TE) deve ocorrer em conformidade com 30 CFR 250.1917, conduzindo uma Pre-Startup Safety Review (PSSR) 3 antes do TE ser implementado para prevenir perigos imprevistos que possam causar um incidente de segurança significativo.\n  Trecho: \"In accordance with 30 CFR 250.1917, conducting a Pre-Startup Safety Review 3 before TE is implemented to prevent unforeseen hazards from causing a significant safety incident.\" [BSEE (EUA) · bsee-safety-alert-449-temporary-equipment-as-a-potential-source-of-ignition-on-…, p. 2]\n• Antes e durante a introdução de TE, deve ser garantido que os impactos da instalação do TE nos sistemas de segurança existentes e barreiras sejam identificados, divulgados e coordenados, com atualização de desenhos de classificação de áreas e rotas de fuga; também devem ser atualizados desenhos e documentos de engenharia para refletir mudanças operacionais. O procedimento inclui estabelecer diret…\n  Trecho: \"Establishing safety guidelines, procedures, and training addressing the TE (e.g., new gas detectors, updated alarm and ESD logic diagrams, additional means of firefighting, etc.) • Ensuring the potential impacts of the TE’s installation on existing safety systems and barriers are identified, publicized, and coordinate…\" [BSEE (EUA) · bsee-safety-alert-449-temporary-equipment-as-a-potential-source-of-ignition-on-…, p. 2]"
 },
 {
  "codigo": "Q024",
  "id": "470390a408-s0002-A1",
  "topico": "Utilidades, geração de energia e sistemas auxiliares",
  "subtopico": "Geração e distribuição de energia elétrica",
  "nivel": "Difícil (cenário em um conceito)",
  "dificuldade": "Difícil",
  "pergunta": "Em um skid com ASD em área classificada, uma falha de isolamento energiza a carcaça do equipamento. As partes metálicas do conjunto e da estrutura estão bonded e aterradas, de modo que permanecem praticamente no mesmo potencial, mas a condição anormal continua alimentada. Qual função ainda deve atuar para completar a barreira de segurança?",
  "resposta": "Detecção da falta à terra com alarme e seccionamento automático da alimentação.",
  "pontos_essenciais": [
   "detecção de falta à terra",
   "seccionamento automático da alimentação"
  ],
  "explicacao": "O bonding com aterramento reduz diferenças de potencial de toque entre partes metálicas e ajuda a manter potenciais mais seguros, mas não elimina sozinho a permanência da falta. Em área classificada, a barreira se completa com proteção que reconheça a anormalidade e retire automaticamente a energia.",
  "contexto": "Nota técnica: Aterramento e bonding como barreiras de segurança elétrica na instalação offshore\nResumo: O aterramento de segurança e a equipotencialização por bonding reduzem o risco elétrico ao limitar diferenças de potencial entre partes metálicas e ao fornecer caminho controlado para correntes de falta à terra. No material fornecido, essas medidas aparecem como parte dos princípios fundamentais de segurança elétrica em instalações offshore e como requisito especialmente relevante em áreas classificadas e em sistemas com ASDs, onde falhas de isolamento, aquecimentos e outras condições anormais…\nConhecimento que a questão deveria avaliar: Analisar um cenário com massa metálica energizada por falha de isolamento e decidir por que aterramento, equipotencialização, detecção da falta e seccionamento automático devem atuar de forma coordenada, especialmente em área classificada ou em equipamento com ASD.\n\nFatos das fontes usados na resposta (afirmação e trecho original):\n• Todas as partes metálicas do ASD, tanto internas quanto do chassi, devem ser interligadas (bonded) e aterradas de modo a confirmar que potenciais de toque seguros existem em condições de falta à terra (groundfault conditions).\n  Trecho: \"Ensure all ASD metallic parts, both internal and chassis, are bonded together and grounded to earth to confirm safe touch voltage potentials exist in groundfault conditions;\" [BSEE (EUA) · BSEE Safety Alert 396 - Risk of Fires from Adjustable Speed Drives ASDs, p. 2]\n• Práticas de instalação devem ser documentadas e atender princípios fundamentais de segurança elétrica, incluindo proteção contra corrente de sobrecorrente e corrente de falta à terra conforme API RP 14F1 e API RP 14FZ2. A proteção deve ser considerada parte do que é exigido na instalação elétrica em instalações offshore.\n  Trecho: \"Ensure installation practices are documented and meet fundamental electrical safety principles, including protection against overcurrent and earth fault current in accordance with API RP14F1 & 14FZ2;\" [BSEE (EUA) · BSEE Safety Alert 396 - Risk of Fires from Adjustable Speed Drives ASDs, p. 2]\n• Em áreas classificadas, devem ser adotados dispositivos de proteção como alarme e seccionamento automático para prevenir sobretensões, sobrecorrentes, falhas de isolamento, aquecimentos ou outras condições anormais de operação.\n  Trecho: \"de acidentes Nas instalações elétricas de áreas classificadas devem ser adotados dispositivos de proteção como alarme e seccionamento automático para prevenir sobretensões sobrecorrentes falhas de isolamento aquecimentos ou outras condições anormais de operação\" [Petrolês · corpusPublico(sem IBICT)-SemProcessamento.txt]"
 },
 {
  "codigo": "Q025",
  "id": "470390a408-s0005-A1",
  "topico": "Utilidades, geração de energia e sistemas auxiliares",
  "subtopico": "Geração e distribuição de energia elétrica",
  "nivel": "Difícil (integra dois ou mais conceitos)",
  "dificuldade": "Difícil",
  "pergunta": "Em um barramento seccionado com duas zonas diferenciais, operando com bus tie e sem retaguarda local aplicável, ocorre falta em uma linha. Dois disjuntores associados à linha abrem e eliminam a falta; alguns ciclos depois, uma proteção temporizada desliga outro trecho sadio. Qual é o diagnóstico correto desse evento?",
  "resposta": "Perda de seletividade; a abertura inicial de dois disjuntores era prevista pela topologia, mas a atuação temporizada adicional foi indevida.",
  "pontos_essenciais": [
   "a abertura inicial de dois disjuntores pode ser comportamento esperado da configuração",
   "a atuação posterior da retaguarda em trecho sadio, após eliminação da falta, caracteriza perda de seletividade"
  ],
  "explicacao": "Em arranjos com duas zonas diferenciais de barramento, faltas na linha podem provocar a abertura de dois disjuntores como comportamento esperado da filosofia de proteção. Porém, se a falta já foi eliminada pela atuação inicial e depois ocorre desligamento temporizado adicional de trecho sadio, isso indica atuação indevida da retaguarda, portanto perda de seletividade.",
  "contexto": "Nota técnica: Arquiteturas de barramento, bus ties e transferência de circuitos\nResumo: A arquitetura do barramento define quanto da instalação permanece energizado após falhas, quanto esforço de manobra e proteção é necessário para transferir circuitos e quão ampla pode ser a recomposição do sistema. Em arranjos simples, seccionados ou mais flexíveis, o bus tie e o barramento de transferência ampliam as opções operacionais, mas também impõem requisitos de proteção e criam consequências severas quando o disjuntor de interligação falha.\nNota técnica: Proteção de barramentos seccionados, zonas diferenciais e falha de disjuntores\nResumo: A filosofia de proteção de barramentos não pode ser definida isoladamente do arranjo elétrico, porque a mesma falta pode exigir a abertura de um ou de vários disjuntores conforme a seção de barramento participe da linha, existam duas zonas diferenciais e o sistema opere em anel aberto. Quando não há retaguarda local aplicável e um disjuntor falha em abrir, a eliminação segura da falta depende de ações adicionais, incluindo a abertura do terminal remoto por relé no próprio terminal ou por transf…\nNota técnica: Seletividade e coordenação entre proteção primária e retaguarda em esquemas de sobrecorrente/falta à terra e arranjos de barramento\nResumo: Seletividade é ajustar as proteções para atuarem o mais rapidamente possível na sua zona primária e, fora dela, apenas como retaguarda temporizada. Em arranjos com bus tie, barramento de transferência, bypass, zonas diferenciais múltiplas, transformadores e falha de disjuntor, a coordenação deixa de ser apenas um problema de curva tempo-corrente e passa a depender também da topologia instantânea do sistema e da correta adaptação das zonas de atuação.\nConhecimento que a questão deveria avaliar: Desarme múltiplo em barramento seccionado: atuação prevista da proteção ou falha de coordenação?. Ligação: Em barramentos seccionados com bus tie e zonas de proteção dependentes da topologia, uma mesma falta pode exigir a abertura de vários disjuntores sem que isso signifique defeito. Porém, a coordenação entre proteção primária e retaguarda também pode produzir desarmes excessivos se não acompanhar a configuração instantânea do arranjo. Raciocínio exigido: A resposta exige diferenciar consequência normal da filosofia de proteção de uma atuação indevida por má coordenação. O candidato precisa…\n\nFatos das fontes usados na resposta (afirmação e trecho original):\n• Em arranjos com duas zonas de diferencial de barramento (“Two bus differential zones”), há repetição do comportamento de proteção: faltas na linha podem desarmar dois disjuntores. O texto também indica “Local backup not applicable” para essa configuração.\n  Trecho: \"Two bus differential zones <NUMBER> Local backup not applicable <NUMBER> Line faults trip two breakers\" [Petrolês · corpusPublico(sem IBICT)-SemProcessamento.txt]\n• A operação da proteção de backup é incorreta e indesejada se ocorrer enquanto a proteção primária daquela área não falhou ao eliminar a falta. A coordenação deve ser importante para assegurar continuidade máxima do serviço com o mínimo de desconexão do sistema.\n  Trecho: \"Operation of the backup protection is incorrect and undesirable unless the primary protection of that area fails to clear the fault Consequently selectivity or relay coordination is important to assure maximum service continuity with minimum system dis-connection\" [Petrolês · corpusPublico(sem IBICT)-SemProcessamento.txt]\n• Seletividade (também conhecida como coordenação de relés) é o processo de aplicar e ajustar relés de modo que eles operem o mais rápido possível dentro da zona primária, mas com operação atrasada na zona de backup/sobrealcance. Isso é necessário para permitir que os relés primários designados para a…"
 },
 {
  "codigo": "Q026",
  "id": "6fffbf5758-s0010-A1",
  "topico": "Descomissionamento e Gestão do Ciclo de Vida da Unidade",
  "subtopico": "Geral",
  "nivel": "Fácil",
  "dificuldade": "Fácil",
  "pergunta": "Que condição deve caracterizar a planta e os tanques de carga antes do transporte ou reboque da unidade após a parada da produção?",
  "resposta": "Devem estar drenados, ventilados/purgados e lavados, com remoção de hidrocarbonetos, outras substâncias e TENORM, além de isolamento para evitar recontaminação.",
  "pontos_essenciais": [
   "remoção dos inventários residuais por drenagem, ventilação/purga e lavagem",
   "isolamento dos sistemas para impedir contaminação ou recontaminação"
  ],
  "explicacao": "A condição requerida antes da etapa marítima é a de limpeza e isolamento da planta, tanques, vasos, equipamentos e linhas. Ela remove inventários remanescentes, inclusive TENORM, e mantém os trechos já tratados segregados, preparando a unidade para enquadramento de navegação ou reboque.",
  "contexto": "Nota técnica: Condição de limpeza, drenagem e isolamento da planta para transporte ou reboque\nResumo: Após a parada da produção, a unidade passa por uma condição de limpeza e isolamento destinada a remover hidrocarbonetos e outras substâncias da planta de processo, tanques de carga, linhas e sistemas associados, de modo a enquadrá-la na condição requerida pela classificadora para navegação ou reboque. Essa condição combina drenagem, ventilação, purga, lavagem, remoção de TENORM e isolamento contra recontaminação. Com tanques e planta limpos, realizam-se os reforços e ajustes estruturais necessá…\nConhecimento que a questão deveria avaliar: Explicar o que caracteriza a condição de limpeza da planta e dos tanques antes do transporte ou reboque, incluindo drenagem, ventilação, purga, lavagem e isolamento.\n\nFatos das fontes usados na resposta (afirmação e trecho original):\n• Após a parada são executadas limpezas da planta de processo com drenagem, ventilação, purga e lavagem de vasos, equipamentos e linhas dos tanques de carga, para enquadramento na condição determinada pela classificadora e para remoção de hidrocarbonetos e outras substâncias. A limpeza inclui remoção de TENORM e isola os sistemas para impedir contaminação, e com tanques e planta limpos são realizad…\n  Trecho: \"Após a parada são executadas as limpezas da planta de processo drenagem ventilação purga e lavagem de vasos equipamentos e linhas dos tanques de carga para enquadramento na condição determinada pela classificadora e dos sistemas de marinharia removendo hidrocarbonetos e outras substâncias inclusive o Rio Oil & Gas Exp…\" [Petrolês · corpusPublico(sem IBICT)-SemProcessamento.txt]"
 },
 {
  "codigo": "Q027",
  "id": "6fffbf5758-s0011-A1",
  "topico": "Descomissionamento e Gestão do Ciclo de Vida da Unidade",
  "subtopico": "Geral",
  "nivel": "Média",
  "dificuldade": "Média",
  "pergunta": "Antes do corte de uma linha no descomissionamento, foi medido TOG abaixo de 15 mg/L no fluido remanescente. Qual é a interpretação operacional mais adequada desse resultado para a decisão de corte?",
  "resposta": "Indica menor teor de óleo naquele fluido antes do corte, como critério complementar contextual, não como limite geral de liberação para qualquer intervenção.",
  "pontos_essenciais": [
   "menor teor de óleo no fluido remanescente antes do corte",
   "não generalizar como limite universal de liberação"
  ],
  "explicacao": "Esse resultado caracteriza a condição do fluido naquela operação específica de corte, ajudando a qualificar o potencial de descarga. A autorização continua dependendo da condição física do sistema, como esvaziamento, limpeza e ausência de resíduo perigoso, sem extrapolar esse valor para outros casos.",
  "contexto": "Nota técnica: Limpeza, isolamento e controle de perda de contenção antes de corte, desmontagem e intervenção\nResumo: Antes de cortar, desmontar ou abrir equipamentos e linhas no descomissionamento, a instalação precisa reduzir o inventário remanescente, remover contaminantes, impedir contaminação por sistemas conectados e verificar se a condição do fluido e da atmosfera é compatível com a atividade. Drenagem, despressurização, purga, ventilação, lavagem, isolamento mecânico e controle de integridade atuam em conjunto para prevenir vazamentos, retorno de gás, atmosferas perigosas e descargas para o mar durante…\nConhecimento que a questão deveria avaliar: Interpretar o significado operacional de um fluido remanescente com TOG abaixo de 15 mg/L antes de um corte, sem generalizar esse valor para qualquer situação.\n\nFatos das fontes usados na resposta (afirmação e trecho original):\n• Antes do corte dos risers e do corte das linhas de ancoragem na resposta à emergência, o fluido contido nas linhas já se encontrava com TOG enquadrado abaixo de 15 mg/L. Essa condição foi registrada como característica do fluido antes da operação de corte.\n  Trecho: \"Tais operações foram executadas no contexto da resposta à emergência, contudo, é importante destacar que, de acordo com a Petrobras, antes do corte , o fluido contido nas linhas já se encontrava com TOG enquadrado abaixo de 15 mg/L.\" [ANP · Relatório de investigação do acidente de descarga de óleo ocorrido no FPSO Cida…, p. 19]\n• A manutenção corretiva só pode intervir no equipamento quando a Produção oferecer condições para isso, incluindo esvaziar os fluidos do sistema e garantir ausência de resíduo nos equipamentos. Se os equipamentos contiverem material tóxico, explosivo, inflamável, corrosivo etc., essa condição deve ser garantida antes da intervenção.\n  Trecho: \"Além disso, a manutenção só poderá intervir no equipamento após a Produção oferecer as condições para isso, como esvaziar os fluidos do sistema e garantir que não haverá qualquer resíduo nos equipamentos, se eles contiverem material tóxico, explosivo, inflamável, corrosivo etc.\" [REGIS · 14405_Marcelo14_mai_2008_Versao_para_deposito_final.pdf]"
 },
 {
  "codigo": "Q028",
  "id": "6fffbf5758-s0001-A1",
  "topico": "Descomissionamento e Gestão do Ciclo de Vida da Unidade",
  "subtopico": "Geral",
  "nivel": "Média",
  "dificuldade": "Média",
  "pergunta": "Em um FPSO de casco simples que armazena ou armazenou água produzida, a campanha de tanques avaliou apenas a estrutura. Qual complemento mínimo ainda é necessário para que essa avaliação de integridade seja tecnicamente suficiente?",
  "resposta": "Avaliar também a funcionalidade da proteção catódica e a condição do revestimento, com inspeção e relatório de tanques em nível de exigência mais alto.",
  "pontos_essenciais": [
   "incluir proteção catódica e revestimento",
   "exigir maior rigor na inspeção e no relatório"
  ],
  "explicacao": "Em tanques de casco simples que armazenaram água produzida, a avaliação não deve se limitar à estrutura: ela deve incluir a funcionalidade da proteção catódica e a condição do revestimento. Além disso, a confiabilidade do diagnóstico depende de elevar a exigência técnica das inspeções e dos respectivos relatórios, inclusive quando executados por terceiros.",
  "contexto": "Nota técnica: Baseline survey e inspeções especiais como base técnica para extensão de vida de FPSO/FSU\nResumo: A extensão de vida depende de conhecer a condição real da unidade, e esse conhecimento não pode ser inferido apenas por histórico de classe ou por inspeções rotineiras isoladas. O baseline survey deve ter escopo abrangente, pelo menos equivalente ao da próxima Special Survey, e precisa ser integrado a inspeções por zonas, inspeções pós-evento, avaliações de casco, tanques, amarração, splash zone e envelope externo para sustentar decisões de life extension e, quando aplicável, o acompanhamento a…\nConhecimento que a questão deveria avaliar: Descrever como a avaliação de tanques pode precisar incluir, além da estrutura, a funcionalidade da proteção catódica, a condição do revestimento e a qualidade do relatório de inspeção.\n\nFatos das fontes usados na resposta (afirmação e trecho original):\n• Devem ser desenvolvidas ou adotadas ferramentas de gestão para aumentar efetivamente o grau de exigência das inspeções em tanques e nos respectivos relatórios. Isso vale para inspeções realizadas por pessoal próprio ou contratado.\n  Trecho: \"FPRJ_R03) Desenvolver ou adotar ferramentas de gestã o que aumentem efetivamente o grau de exigência da qualidade de inspeções em tanques e respectivos relatórios, sejam por pessoal próprio ou contratado.\" [ANP · Sumário Executivo do Relatório de investigação do acidente de descarga de óleo…, p. 5]\n• Foi indicada a necessidade de avaliar todos os tanques de FPSO de casco simples que tenham ou tiveram água produzida armazenada. A avaliação deve incluir análise de integridade, funcionalidade do sistema de proteção catódica e do revestimento.\n  Trecho: \"▪ Avaliar todos os tanques de FPSO de casco simples que tenham ou tiveram água produzida armazenada e realizar análise de sua integridade, da funcionalidade de seu sistema d e proteção catódica e de seu revestimento.\" [ANP · Versão em Português, p. 2]"
 },
 {
  "codigo": "Q029",
  "id": "6fffbf5758-s0007-A1",
  "topico": "Descomissionamento e Gestão do Ciclo de Vida da Unidade",
  "subtopico": "Geral",
  "nivel": "Difícil (cenário em um conceito)",
  "dificuldade": "Difícil",
  "pergunta": "Na preparação para o descomissionamento de um FPSO, houve redução de efetivo, acúmulo de funções e entrada de novos integrantes. Parte da equipe assumiu turno sem tutoria prévia, a passagem de serviço não registrava isolamentos e mudanças, e a supervisão ficou insuficiente. Após isso, surgiram falhas de inspeção e divergências sobre a condição operacional dos sistemas. Qual processo organizacional deveria ter sido formalmente acionado para controlar essa transição?",
  "resposta": "O gerenciamento de mudanças de pessoas, com tutoria antes da efetivação e suporte de supervisão e passagem de serviço formal.",
  "pontos_essenciais": [
   "gerenciamento de mudanças de pessoas",
   "tutoria prévia à efetivação da mudança"
  ],
  "explicacao": "Redução, aumento, acúmulo de funções e entrada ou saída de pessoas devem ser tratados como mudança organizacional formal. Sem esse processo, a organização redistribui responsabilidades sem garantir competência, supervisão e transferência confiável de informação, o que degrada o controle operacional e favorece falhas de inspeção, isolamento e execução.",
  "contexto": "Nota técnica: Governança, competências, recursos e coordenação organizacional no ciclo de vida e no descomissionamento de FPSOs\nResumo: A efetividade do ciclo de vida e do descomissionamento de uma FPSO depende de uma estrutura organizacional capaz de transformar requisitos de segurança, manutenção e mudança em execução supervisionada, com pessoas qualificadas e recursos disponíveis. Quando planejamento, supervisão, passagem de serviço, gestão de mudanças de pessoas, avaliação de contratadas e auditorias internas falham, surgem desvios previsíveis: inspeções deficientes, manutenção não cumprida, baixa percepção de risco e perda…\nConhecimento que a questão deveria avaliar: Analisar por que mudanças de efetivo, acúmulo de funções ou entrada e saída de pessoas devem ser tratadas como gerenciamento de mudanças, e como a omissão desse processo pode degradar a execução segura e controlada.\n\nFatos das fontes usados na resposta (afirmação e trecho original):\n• Deve existir procedimento escrito de passagem de serviço que garanta, no mínimo, formato do registro escrito e acesso e conhecimento de mudanças, isolamentos e condições operacionais dos sistemas afetos a cada função antes de assumir o trabalho a bordo. O procedimento deve definir funções sem desembarque simultâneo e para quais funções deve existir diálogo entre substituto e substituído.\n  Trecho: \"R08: Estabelecer procedimento escrito de passagem d e serviço que garanta, no mínimo, formato do registro escrito, bem como o acesso e conhecimen to de mudanças, isolamentos e condições operacionais dos sistemas afetos a cada função, ant es de assumir o trabalho a bordo. Este procedimento deve definir as funções para…\" [ANP · Resumo técnico executivo do Relatório de Investigação do incidente de explosão…, p. 31]\n• O concessionário e o operador da instalação devem garantir os recursos humanos necessários para a implementação da estrutura do gerenciamento mencionado no trecho.\n  Trecho: \"R13: O Concessionário e o Operador da Instalação de vem garantir os recursos humanos para a implementação da estrutura\" [ANP · Resumo técnico executivo do Relatório de Investigação do incidente de explosão…, p. 31]\n• Deve ser aplicado o processo de gerenciamento de mudanças de pessoas, incluindo casos de redução, aumento e acúmulo de funções, além de entrada e saída de pessoas. A ausência do gerenciamento de mudança de pessoas é associada a falhas relacionadas ao processo.\n  Trecho: \"CR07: Ausência dos superintendentes de marinha / [16.2] Ausênci a do gerenciamento de mudança de pessoas 16.3 R11: Garantir a aplicação do processo de gerenciamento de mudanças de pessoas, incluindo os casos de redução, aumento e acúmulo de funções, entrada e saída de pessoas.\" [ANP · Relatório final da investigação do FPSO Cidade de São Mateus, p. 276]\n• A ausência de tutoria/acompanhamento está associada a dimensionamento inadequado do programa de treinamento. Deve ser implementado processo de tutoria e acompanhamento de novas pessoas antes da efetivação da mudança, como parte do gerenciamento de pessoas.\n  Trecho: \"CR08: Ausência de tutoria/acompanhamento / [3.3.2] Dimensionamento inadequado do programa de treinamento 3.3.2 R12: Implementar processo de tutoria e acompanhamento de novas pessoas como parte do processo de gerenciamento de pessoas, antes da efetivação da mudança.\" [ANP · Relatório final da investigação do FPSO Cidade de São Mateus, p. 276]\n• A implementação da estrutura organizacional necessária para o cumprimento do SGSO requer recursos humanos de supervisão disponíveis; a ausência desses recursos impede o cumprimento. Também há requisito para que concessionário e operador garantam recursos humanos de supervisão para implementar a estrutura organizacional necessária.\n  Trecho: \"CR09: Ausência da função 1.5 R13…"
 },
 {
  "codigo": "Q030",
  "id": "6fffbf5758-s0005-A1",
  "topico": "Descomissionamento e Gestão do Ciclo de Vida da Unidade",
  "subtopico": "Geral",
  "nivel": "Difícil (integra dois ou mais conceitos)",
  "dificuldade": "Difícil",
  "pergunta": "Após a parada, a FPSO já teve tanques de carga drenados e lavados para preparação ao reboque, enquanto módulos e cargas de convés começaram a ser removidos para ajustes estruturais. O programa de estabilidade passou a mostrar condição aceitável, mas o calado/trim observados não batem com o modelo e a unidade perdeu margem após o esvaziamento. Qual ação deve vir primeiro antes de autorizar o avanço da preparação para tow-out?",
  "resposta": "Reconstituir a condição real de pesos e conteúdos e atualizar o programa de estabilidade antes de qualquer nova remoção ou liberação para reboque.",
  "pontos_essenciais": [
   "reconstituir/atualizar o inventário real de tanques e cargas",
   "usar essa condição real para reavaliar estabilidade e esforços antes de prosseguir"
  ],
  "explicacao": "A limpeza dos tanques e a remoção progressiva de módulos alteram distribuição de massa, centro de gravidade e esforços longitudinais, de modo que a condição de reboque não pode ser tratada como fixa. Como os tanques do casco entram automaticamente, mas cargas de convés dependem de lançamento manual, divergência entre bordo e programa exige recompor o inventário real antes de concluir aptidão ao trânsito ou decidir necessidade de compensação com líquidos em tanques de carga quando o lastro é limitado.",
  "contexto": "Nota técnica: Estabilidade, lastro e monitoramento da condição da FPSO na preparação para reboque\nResumo: Na preparação de uma FPSO para tow-out, a condição de estabilidade depende da distribuição de pesos entre tanques do casco, cargas de convés e compartimentos estanques, e não apenas da quantidade total de líquido a bordo. O controle operacional combina plano de estabilidade, uso do programa de estabilidade, decisões de lastro e verificação da integridade de flutuação, para manter simultaneamente a estabilidade da unidade e os esforços longitudinais dentro da condição monitorada pela equipe mari…\nNota técnica: Avaliação contínua de estabilidade, distribuição de pesos e centro de gravidade com remoção progressiva de cargas\nResumo: Em unidades flutuantes, a retirada progressiva de óleo, módulos, equipamentos e estruturas altera a distribuição de pesos, a posição do centro de gravidade e a margem de estabilidade, o que torna inadequado tratar a condição final como se fosse fixa durante todo o descomissionamento. Quando a capacidade de lastro é limitada, a manutenção de condição segura pode exigir o uso operacional de volumes em tanques de carga, desde que o controle de pesos e posicionamento seja continuamente atualizado.\nNota técnica: Limpeza, isolamento e reconfiguração estrutural da unidade após parada e antes de navegação/reboque\nResumo: Após a parada da produção, a unidade entra em uma fase de transição em que a planta de processo, os tanques de carga e sistemas associados são drenados, ventilados, purgados, lavados e isolados para remover hidrocarbonetos, TENORM e outras substâncias contaminantes. Essa preparação reduz perigos remanescentes do inventário de processo, permite enquadrar a unidade na condição exigida para a próxima fase e cria as condições para executar reforços e ajustes estruturais necessários à navegação ou a…\nConhecimento que a questão deveria avaliar: Estabilidade para reboque afetada pela limpeza dos tanques e pela remoção progressiva de pesos. Ligação: A preparação para tow-out exige controle de estabilidade, distribuição de pesos, integridade de flutuação e esforços longitudinais com base na condição real de tanques e cargas (N64). Essa condição não é estática no descomissionamento, porque a retirada progressiva de óleo, módulos e equipamentos desloca centro de gravidade e margem de estabilidade, podendo exigir uso operacional de volumes em tanques de carga quando o lastro é limitado (N73). Ao mesmo tempo, a limpeza e isolamento prévios…\n\nFatos das fontes usados na resposta (afirmação e trecho original):\n• O programa de estabilidade exibe a estabilidade atual, os bending moments e as shear forces da embarcação. O controle da estabilidade é associado a um apêndice específico que detalha o tema.\n  Trecho: \"The stability programme will display the current Stability, Bending moments and Shear forces on the vessel. Further details on the control of stability are found in Appendix 1 – Stability and Ballast Systems\" [HSE (Reino Unido) · ed-loss-of-stability-and-positioning.pdf, p. 52]\n• A estabilidade da instalação é controlada pelo Marine Supervisor ou pelo Ballast Control Operator. O computador de carga/estabilidade registra automaticamente conteúdos dos tanques do casco (lastro, crude oil, fuel oil e fresh water) e os envia automaticamente ao programa de estabilidade, enquanto mudanças de cargas de convés devem ser inseridas manualmente pela equipe marinha.\n  Trecho: \"The stability of the installation is under the control of the Marine Supervisor, or Ballast Control Operator. The load or stability computer will register the hull tank contents, such as ballast, crude oil, fuel oil and fresh water and these will be automatically uploaded to the stability programme. Marine personnel w…\" [HSE (Reino Unido) · e…"
 },
 {
  "codigo": "Q031",
  "id": "332e35e913-s0008-A1",
  "topico": "Gestão do Desempenho Empresarial (KPI)",
  "subtopico": "Gestão do Desempenho Empresarial (KPI)",
  "nivel": "Fácil",
  "dificuldade": "Fácil",
  "pergunta": "Que resultado da análise de falhas permite reduzir reincidências e deslocar manutenção e inspeção do modo reativo para o preventivo?",
  "resposta": "A compreensão dos mecanismos e das causas da falha.",
  "pontos_essenciais": [
   "compreensão dos mecanismos da falha",
   "identificação das causas da falha"
  ],
  "explicacao": "Quando os mecanismos e as causas são compreendidos, manutenção e inspeção podem ser redirecionadas para evitar repetição da falha, em vez de apenas reagir após a ocorrência. Isso reduz reincidências e melhora eficiência, confiabilidade e segurança.",
  "contexto": "Nota técnica: Retroalimentação por falhas, risco e integridade para melhoria sustentada ao longo da vida útil da unidade\nResumo: A melhoria contínua ao longo do ciclo de vida da unidade depende de transformar falhas, degradação de barreiras, dados de disponibilidade e informação de integridade em decisões de manutenção, inspeção, operação e governança. Quando essas entradas são auditáveis, completas e tratadas por pessoas competentes, inclusive na interface com contratadas, o desempenho tende a sair do reativo e se tornar mais previsível, com melhor controle do risco de processo e da integridade de longo prazo.\nConhecimento que a questão deveria avaliar: Explicar como a análise de falhas reduz reincidências e desloca a manutenção e a inspeção do eixo reativo para o preventivo.\n\nFatos das fontes usados na resposta (afirmação e trecho original):\n• Ao permitir a compreensão dos mecanismos e das causas associadas à ocorrência de uma falha, a Análise de Falhas inibe reincidências. Essa compreensão é determinante no deslocamento das atividades de manutenção e inspeção do eixo reativo para o preventivo, com ganhos diretos em eficiência, confiabilidade e segurança.\n  Trecho: \"Ao permitir a compreensão dos mecanismos e das causas associadas a ocorrência de uma falha a Análise de Falhas se institui com uma importante ferramenta para inibição de reincidências sendo determinante no processo de deslocamento das atividades de manutenção e inspeção do eixo reativo para o preventivo com ganhos dir…\" [Petrolês · corpusPublicoIBICT-SemProcessamento.txt]"
 },
 {
  "codigo": "Q032",
  "id": "332e35e913-s0009-A1",
  "topico": "Gestão do Desempenho Empresarial (KPI)",
  "subtopico": "Gestão do Desempenho Empresarial (KPI)",
  "nivel": "Média",
  "dificuldade": "Média",
  "pergunta": "Em um FPSO, os KPIs são acompanhados mensalmente, mas a gestão quer evitar que virem apenas números de reporte. No ciclo PDCA, que tratamento deve converter esses dados em ação de melhoria contínua?",
  "resposta": "Usá-los na etapa de verificação, junto com achados de auditoria e análise crítica da administração, para definir ações corretivas ou de aperfeiçoamento.",
  "pontos_essenciais": [
   "verificação com auditorias e análise crítica gerencial",
   "definição de ação corretiva ou melhoria"
  ],
  "explicacao": "No PDCA, a medição de desempenho não se encerra no acompanhamento do indicador. Os dados devem alimentar a checagem formal do sistema, combinados com auditorias e revisão gerencial, para que a etapa seguinte produza correção de desvios ou aperfeiçoamento do processo.",
  "contexto": "Nota técnica: KPI como elemento do ciclo de monitoramento, verificação e melhoria contínua na governança de FPSOs\nResumo: Em FPSOs, KPI não deve ser tratado apenas como número de reporte, mas como evidência usada para verificar desempenho frente a objetivos e metas, acionar auditorias, análises críticas e ações corretivas dentro do sistema de gestão. Quando integrado à governança operacional, o KPI fecha o ciclo entre planejamento, monitoramento, verificação pela gestão e melhoria contínua, em vez de servir apenas para prestação passiva de contas.\nConhecimento que a questão deveria avaliar: Descrever como o ciclo PDCA e a melhoria contínua usam dados de desempenho, auditorias e análise crítica da administração para transformar medição em ação.\n\nFatos das fontes usados na resposta (afirmação e trecho original):\n• Melhoria contínua é um processo contínuo de estabelecimento de objetivos e identificação de oportunidades de melhorias, usando constatações e conclusões de auditorias, análise de dados e análise crítica pela administração ou outras fontes. Esse processo busca oportunidades de aperfeiçoamento dos processos nas operações da empresa.\n  Trecho: \"processo contínuo de estabelecimento de objetivos e de identificação de oportunidades de melhorias, através do uso de constatações e conclusões de auditorias, análise de dados, análise crítica pela administração ou outras fontes. Quase sempre existe possibilidade de aperfeiçoamento dos processos nas operações em uma e…\" [REGIS · 3980_Eduardo%20Rocha%20Bastos.pdf]\n• Implementar o framework de DRM combina uma parte estática do modelo de probabilidade de blowout com uma parte dinâmica baseada no ciclo PDCA (Plan-Do-Check-Act). O PDCA é descrito como um método de alto nível para alcançar melhoria contínua, usado como prática no gerenciamento de riscos.\n  Trecho: \"for implementing the DRM framework combines the design of the blowout probability model static part with a dynamic part which is based on the Plan-Do-Check-Act P-D-C-A cycle PDCA is a high level method for achieving continuous improvement that has been a basic element of the total quality management movement\" [Petrolês · corpusPublico(sem IBICT)-SemProcessamento.txt]\n• O processo de gestão inclui verificação e ação corretiva como parte do conjunto de elementos de gestão. A verificação e a ação corretiva fazem parte do ciclo do sistema de gestão de SMS para tratar não conformidades ou desvios.\n  Trecho: \"Monitoramento e Mensuração de Desempenho Documentação do Processo de Gestão Verificação e Ação Corretiva Controle Operacional\" [Petrolês · corpusPublico(sem IBICT)-SemProcessamento.txt]\n• Achados de auditoria, dados de KPI e outras informações sobre desempenho de segurança devem ser reportados a nível sênior e ter ações decorrentes. O programa de auditorias do SMS deve ser executado conforme parte do sistema de gestão.\n  Trecho: \" Audit findings, KPI data and other information regarding safety performance reported to a senior level and acted upon 3. Implementation and maintenance of pipeline integrity management process\" [HSE (Reino Unido) · pipelines-integrity-management-inspection.pdf, p. 11]"
 },
 {
  "codigo": "Q033",
  "id": "332e35e913-s0003-A1",
  "topico": "Gestão do Desempenho Empresarial (KPI)",
  "subtopico": "Gestão do Desempenho Empresarial (KPI)",
  "nivel": "Média",
  "dificuldade": "Média",
  "pergunta": "Uma empresa ampliou a capacidade da planta e passou a produzir novos itens. Se o conjunto de KPIs foi definido antes dessas mudanças, qual efeito isso tem sobre o sistema de indicadores, especialmente nas perspectivas de processos internos e clientes?",
  "resposta": "O mix anterior de KPIs pode ficar insuficiente e deve ser revisado, porque as mudanças alteram os direcionadores e as relações de desempenho, com maior impacto em processos internos e clientes.",
  "pontos_essenciais": [
   "o mix anterior de KPIs/BSC torna-se insuficiente e requer revisão",
   "as mudanças afetam mais fortemente processos internos e clientes"
  ],
  "explicacao": "A ampliação de capacidade e a introdução de novos produtos mudam as relações entre variáveis que sustentam os resultados, afetando indicadores em todas as perspectivas. Por isso, a leitura do desempenho precisa ser atualizada para manter aderência à estratégia e ao processo de criação de valor.",
  "contexto": "Nota técnica: Alinhamento dos indicadores à estratégia e à criação de valor\nResumo: O sistema de indicadores deve traduzir a estratégia em medidas que permitam acompanhar sua implementação e explicitar como objetivos, processos e resultados se encadeiam na criação de valor. Em ambientes de mudança, o mix de KPIs não pode ser estático: alterações de capacidade, portfólio e modelo de gestão exigem revisão das métricas e dos critérios de avaliação, inclusive sob a ótica econômica das decisões dos gestores.\nConhecimento que a questão deveria avaliar: Explicar como mudanças no negócio, como aumento de capacidade e introdução de novos produtos, podem exigir revisão do mix de KPIs, especialmente nas perspectivas de processos internos e clientes.\n\nFatos das fontes usados na resposta (afirmação e trecho original):\n• O aumento de capacidade da planta industrial e a introdução de novos produtos no mix de produção impactam os indicadores de todas as perspectivas do sistema de medidas de desempenho, especialmente nas perspectivas de processos internos e clientes.\n  Trecho: \"aumento de capacidade da planta industrial e introdução de novos produtos no mix de produção, criando adicionalmente a capacitação de produção para o mercado externo, com impactos sobre os indicadores de todas as perspectivas, mas em especial nas perspectivas processos internos e clientes\" [REGIS · 6007_000658117.pdf]\n• O estudo propôs revisar o Balanced Scorecard (BSC) para incrementar sua contribuição ao processo de gestão estratégica da organização. A revisão é apresentada como meio para melhorar a gestão estratégica via melhor entendimento do desempenho.\n  Trecho: \"Revisar o Balanced Scorecard (BSC) da Refap, de modo a incrementar a sua contribuição ao processo de gestão estratégica da organização.\" [REGIS · 6007_000658117.pdf]\n• O conjunto de indicadores de desempenho deve permitir acompanhar a implementação da estratégia. Também deve permitir desenvolver o entendimento das causalidades sistêmicas entre objetivos e indicadores definidos no plano estratégico da empresa.\n  Trecho: \"Identificar um conjunto de indicadores de desempenho que permitam acompanhar a implementação da estratégia, e desenvolver o entendimento das causalidades sistêmicas entre os objetivos e indicadores definidos no plano estratégico da empresa\" [REGIS · 6007_000658117.pdf]"
 },
 {
  "codigo": "Q034",
  "id": "332e35e913-s0012-A1",
  "topico": "Gestão do Desempenho Empresarial (KPI)",
  "subtopico": "Gestão do Desempenho Empresarial (KPI)",
  "nivel": "Difícil (cenário em um conceito)",
  "dificuldade": "Difícil",
  "pergunta": "Um KPI de confiabilidade de uma bomba mostra tendência estável de vibração ao longo de 18 meses. Em campo, porém, houve troca do conjunto motobomba há 4 meses, mantendo-se o mesmo tag no sistema, e desde então surgiram sinais precoces de degradação no equipamento novo. Qual é a causa mais provável da inconsistência do KPI?",
  "resposta": "Perda de rastreabilidade do item físico monitorado por reaproveitamento do mesmo tag após a substituição do equipamento.",
  "pontos_essenciais": [
   "perda de rastreabilidade/identidade do item",
   "mesmo tag fundiu históricos do equipamento antigo e do novo"
  ],
  "explicacao": "A tendência aparentemente contínua fica artificial quando o histórico do equipamento substituído é misturado ao do novo sob o mesmo identificador. Nesse caso, o KPI deixa de representar um único item físico ao longo do tempo e perde valor preditivo.",
  "contexto": "Nota técnica: Qualidade dos dados e trending como base de KPIs preditivos de confiabilidade dos ativos\nResumo: KPIs de confiabilidade só têm valor preditivo quando se apoiam em dados corretos, completos, rastreáveis e analisados ao longo do tempo. Quando há erro de registro, perda de identidade do equipamento, informações espalhadas em ferramentas desconectadas e ausência de avaliação baseada em risco, a organização perde capacidade de prever falhas, estimar vida residual e agir antes de entrar no modo de manutenção por falha.\nConhecimento que a questão deveria avaliar: Distinguir, diante de um KPI inconsistente com a condição observada, se a causa mais provável está em erro de dado, perda de rastreabilidade do item, fragmentação entre ferramentas ou mudança real do regime de processo não tratada por avaliação baseada em risco.\n\nFatos das fontes usados na resposta (afirmação e trecho original):\n• Em sistemas computacionais, a identificação de equipamentos tende a ocorrer por localização funcional em vez dos itens específicos que compõem o sistema; assim, quando um componente é substituído, o novo equipamento pode receber o mesmo tag ID, perdendo rastreabilidade e podendo confundir históricos de desempenho.\n  Trecho: \"A particular ALE challenge found during KP4 related to equipment identification. Computer systems usually identify equipment systems based on a functional location rather than the specific equipment items that make up that system. So, for example, if the equipment system comprises a motor+gearbox+pump, all are covered…\" [HSE (Reino Unido) · KP4 Report, p. 31]\n• A gestão de dados e o trending são considerados importantes para prever ameaças futuras e permitir medidas mitigatórias em tempo oportuno. O programa KP4 apontou necessidade de melhor coleta e trending para melhorar previsões de vida residual de equipamentos e para facilitar manutenção proativa, evitando o risco de “fix on failure”.\n  Trecho: \"Accurate data management and its trending are important to forecast future threats to enable mitigating measures to be put in place in a timely manner. The KP4 programme found a need for better data collection and trending to improve predictions of equipment residual life to support ALE decision-making, and to facilit…\" [HSE (Reino Unido) · KP4 Report, p. 31]"
 },
 {
  "codigo": "Q035",
  "id": "332e35e913-s0005-A1",
  "topico": "Gestão do Desempenho Empresarial (KPI)",
  "subtopico": "Gestão do Desempenho Empresarial (KPI)",
  "nivel": "Difícil (integra dois ou mais conceitos)",
  "dificuldade": "Difícil",
  "pergunta": "Para melhorar o OPEX do semestre em uma unidade offshore, a diretoria propõe adiar intervenções preventivas. Ao mesmo tempo, a disponibilidade está caindo, o MTBF permanece quase estável, o MTTR subiu, o backlog de manutenção cresceu e o trending indica redução de vida residual de equipamentos críticos. Qual decisão é tecnicamente e economicamente mais consistente?",
  "resposta": "Não postergar as preventivas; revisar prioridades e migrar para manutenção proativa/baseada em condição.",
  "pontos_essenciais": [
   "não adiar intervenções preventivas",
   "migrar ou reforçar manutenção proativa/baseada em condição"
  ],
  "explicacao": "O conjunto de indicadores aponta aumento de indisponibilidade por recuperação mais lenta e maior vulnerabilidade do sistema, não simples aleatoriedade de falhas. Backlog alto e trending de ameaça futura indicam risco de cair em manutenção reativa; manter ou reforçar a estratégia proativa tende a reduzir reparos não programados, perdas de produção e custo total, mesmo que o OPEX imediato não caia.",
  "contexto": "Nota técnica: KPIs de integridade, manutenção e confiabilidade como tradutores de indisponibilidade, perdas de produção e custo\nResumo: Disponibilidade, confiabilidade, MTBF, MTTR, backlog e trending permitem converter o estado de integridade e a eficácia da manutenção em efeitos mensuráveis sobre continuidade operacional, perdas de produção e custo total. Quando esses indicadores são ligados à manutenção baseada na condição e à gestão de ativos, a manutenção deixa de ser apenas centro de gasto e passa a ser instrumento de redução de indisponibilidade e de aumento de rentabilidade.\nNota técnica: Trade-offs econômicos entre CAPEX, OPEX, risco operacional e perdas futuras de produção\nResumo: A gestão do desempenho empresarial, quando aplicada a decisões de desenvolvimento e operação, precisa comparar custos imediatos, risco técnico e impacto futuro sobre a receita do campo. Em cenários de preço deprimido e investimento restrito, a decisão economicamente superior não é apenas a de menor gasto inicial, mas a que melhor combina redução de CAPEX/OPEX, proteção da produção futura e avaliação de desempenho baseada nas consequências econômicas reais das ações gerenciais.\nNota técnica: Estratégias de manutenção para elevar confiabilidade e disponibilidade dos ativos\nResumo: A confiabilidade dos ativos não depende apenas de projeto, fabricação, montagem e operação corretos, porque o desgaste natural ao longo da vida útil pode levar à falha em serviço. A transição da manutenção reativa para estratégias preventivas e baseadas em condição melhora disponibilidade e rentabilidade ao reduzir reincidências, antecipar falhas e evitar reparos não programados.\nConhecimento que a questão deveria avaliar: Cortar gasto de manutenção ou migrar estratégia: o trade-off entre OPEX imediato e perdas futuras. Ligação: Disponibilidade, MTBF, MTTR, backlog e trending mostram como a manutenção influencia perdas e custo total; ao mesmo tempo, a decisão econômica correta não é a de menor OPEX imediato, mas a que melhor protege produção futura e risco operacional. A escolha da estratégia de manutenção, portanto, é um trade-off econômico-técnico e não apenas uma meta de redução de despesa. Raciocínio exigido: A resposta precisa integrar indicadores técnicos de integridade e confiabilidade com raciocínio eco…\n\nFatos das fontes usados na resposta (afirmação e trecho original):\n• A confiabilidade/fiabilidade representa a capacidade de um sistema realizar e manter seu funcionamento tanto em circunstâncias de rotina quanto em circunstâncias hostis e inesperadas. Quanto menor for o tempo de retorno ao estado operacional após falha, menor será o tempo de inatividade do sistema e mais rapidamente se restabelece a condição operacional.\n  Trecho: \"para as engenharias e especialistas que farão este tratamento menor será o tempo de retorno ao estado operacional Em geral confiabilidade ou fiabilidade é a capacidade de um sistema de realizar e manter seu funcionamento em circunstâncias de rotina bem como em circunstâncias hostis e inesperadas\" [Petrolês · corpusPublicoIBICT-SemProcessamento.txt]\n• A tolerância à falhas pode ser mensurada por dois parâmetros: Mean Time Between Failures (MTBF) e Mean Time To Repair (MTTR). O MTTR é o tempo médio entre a ocorrência da falha e a total recuperação do sistema ao seu estado operacional.\n  Trecho: \"Independentemente da solução adotada existem sempre dois parâmetros que possibilitam mensurar o grau de tolerância à falhas que são: o tempo médio entre as falhas ou Mean Time Between Failures MTBF e o tempo médio de recuperação ou Mean Time To Repair MTTR Este último refere-se ao tempo médio que decorre entre a ocorr…\" [Petrolês · corpusPublicoIBICT-SemProcessamento.txt]\n• O objetivo da gestão da manutenção é atingir um equilíbrio entre efeit…"
 },
 {
  "codigo": "Q036",
  "id": "26d45ade58-s0004-A1",
  "topico": "Logística, Suprimentos e Movimentação de Cargas",
  "subtopico": "Movimentação de Cargas",
  "nivel": "Fácil",
  "dificuldade": "Fácil",
  "pergunta": "Qual condição de risco faz com que pipe-racks e cabeças de poço sejam tratadas como áreas críticas em plataformas com facilidades de perfuração?",
  "resposta": "A exposição à queda acidental de objetos, um acidente frequente offshore e com potencial de causar danos.",
  "pontos_essenciais": [
   "exposição à queda acidental de objetos",
   "frequência/potencial de dano desse evento offshore"
  ],
  "explicacao": "Essas áreas devem ser projetadas contra queda acidental de objetos porque esse tipo de acidente é frequente em estruturas offshore e pode provocar danos. Por isso, pipe-racks e cabeças de poço são tratadas como áreas críticas quando estão expostas a esse cenário.",
  "contexto": "Nota técnica: Prevenção de queda de objetos e proteção de estruturas/áreas críticas em movimentação de cargas offshore\nResumo: Em operações offshore de içamento e movimentação de cargas, a queda acidental de objetos é um acidente frequente e precisa ser considerada no arranjo e na proteção de áreas vulneráveis. A justificativa técnica não é apenas evitar dano local: um impacto sobre pipe-racks, cabeças de poço, jaquetas ou risers pode evoluir para perda de integridade estrutural e, no caso de jaquetas e risers, para derrame com poluição ambiental.\nConhecimento que a questão deveria avaliar: Identificar por que pipe-racks e cabeças de poço devem ser considerados áreas críticas em plataformas com facilidades de perfuração.\n\nFatos das fontes usados na resposta (afirmação e trecho original):\n• A queda de objetos é um tipo de acidente bastante frequente em estruturas offshore e pode provocar danos. A área de pipe-rack e das cabeças-de-poco em plataformas com facilidades de perfuração deve ser projetada contra queda acidental de objetos.\n  Trecho: \"A queda de objetos é um tipo de acidente bastante frequente em estruturas offshore e sua capacidade de provocar danos j f o i demonstrada em diversas ocasiões A ãrea de pipe-rack e das cabesas-de-poco em plataformas com facilidades de perfuracão devem ser projetadas contra a queda Eac identa l de objetos\" [Petrolês · corpusPublico(sem IBICT)-SemProcessamento.txt]"
 },
 {
  "codigo": "Q037",
  "id": "b56db319e4-s0001-A1",
  "topico": "Logística, Suprimentos e Movimentação de Cargas",
  "subtopico": "Logística e Suprimento Offshore",
  "nivel": "Média",
  "dificuldade": "Média",
  "pergunta": "Em uma transferência offshore a granel, a equipe pretende aumentar a vazão sem trocar o mangote. Qual parâmetro do mangote precisa permanecer compatível com a vazão de projeto para não comprometer a integridade do sistema?",
  "resposta": "O diâmetro interno do mangote, porque ele deve manter a velocidade do fluido dentro do limite especificado pelo fabricante.",
  "pontos_essenciais": [
   "diâmetro interno do mangote compatível com a vazão",
   "velocidade do fluido dentro do limite do fabricante"
  ],
  "explicacao": "A integridade do sistema depende do casamento entre diâmetro e taxa de offloading de projeto. Se a vazão pretendida eleva a velocidade acima do limite do fabricante, o mangote passa a operar fora da condição admissível de integridade.",
  "contexto": "Nota técnica: Configuração e integridade do sistema de transferência por mangotes em operações offshore\nResumo: A transferência offshore a granel por mangotes e linhas flexíveis só permanece segura quando a configuração operacional, o posicionamento relativo entre as embarcações e a integridade mecânica dos componentes permanecem coerentes entre si. As fontes mostram que perda de contenção não decorre apenas de ruptura do mangote: ela também pode surgir por desalinhamento da embarcação receptora, por envelhecimento acumulado, por dimensionamento inadequado, por mudanças mal geridas na interface de descon…\nConhecimento que a questão deveria avaliar: Explicar por que o diâmetro do mangote deve ser compatível com a vazão de projeto e como limites de velocidade do fabricante influenciam a integridade do sistema.\n\nFatos das fontes usados na resposta (afirmação e trecho original):\n• O diâmetro da linha/mangote deve estar alinhado com a taxa de offloading de projeto, de forma a não exceder os limites de velocidade de fluido do fabricante. Após o offloading, deve haver capacidade adequada de nitrogênio ou gás inerte para deslocar o mangote de offloading, auxiliando sua recuperação.\n  Trecho: \"The diameter of the hose string should be in line with the design offloading rate as to not exceed manufacturers fluid velocity limits. After offloading, adequate capacity of nitrogen or inert gas should be available to displace the offloading hose to assist in its recovery.\" [HSE (Reino Unido) · inspection-of-loss-of-containment.pdf, p. 112]"
 },
 {
  "codigo": "Q038",
  "id": "26d45ade58-s0003-A1",
  "topico": "Logística, Suprimentos e Movimentação de Cargas",
  "subtopico": "Movimentação de Cargas",
  "nivel": "Média",
  "dificuldade": "Média",
  "pergunta": "Em um lift crítico, o supervisor se afasta durante a manobra e leva a única cópia do lift plan, enquanto a equipe continua o içamento em área com interferências próximas. Que falha de controle operacional isso caracteriza?",
  "resposta": "Caracteriza ruptura da cadeia de comunicação e supervisão, com perda de uma barreira essencial de execução no campo.",
  "pontos_essenciais": [
   "ruptura da cadeia de comunicação e supervisão",
   "perda do lift plan no campo como barreira operacional essencial"
  ],
  "explicacao": "Em lifts críticos, o controle não depende só da existência formal do plano, mas de sua disponibilidade na frente de trabalho e da supervisão que mantém a equipe alinhada às premissas, riscos e limites da manobra. Quando o trabalho continua sem o supervisor e sem o lift plan presente, a equipe perde uma barreira operacional essencial e aumenta a chance de desvio silencioso.",
  "contexto": "Nota técnica: Comunicação, supervisão e disciplina de execução em lifts complexos e críticos\nResumo: Em içamentos complexos e críticos, a segurança do lift plan depende menos da existência formal do documento e mais de sua tradução para a frente de trabalho, com riscos, premissas, comunicações e limites entendidos pela equipe executante. Os alertas analisados mostram que falhas de pre-job meeting, toolbox talk, disponibilidade do plano no local e supervisão efetiva permitem desvios silenciosos, especialmente em blind lifts e em áreas com interferências, linhas pressurizadas e pontos de contato.\nConhecimento que a questão deveria avaliar: Descrever como a falta de disponibilidade física do lift plan na frente de trabalho enfraquece o controle operacional durante um lift crítico.\n\nFatos das fontes usados na resposta (afirmação e trecho original):\n• Durante o içamento, o gerente responsável por supervisionar o içamento crítico foi chamado embora e não deixou uma cópia física do Lift Plan com a equipe. Como consequência, o trabalho prosseguiu sem ele e sem o plano de içamento presente, contribuindo para o dano a equipamentos e a quase catástrofe.\n  Trecho: \"The Offshore Construction Manager (OCM) who was responsible for overseeing the critical lift was called away during the lift. He did not leave a hard copy of the Lift Plan with the work crew. The job proceeded without him or the work plan present.\" [BSEE (EUA) · Safety Alert 317 - Catastrophic Incident Avoided - June 12, 2015, p. 1]\n• Embora a Hazard Analysis pré-job tenha identificado o risco de ruptura acidental de linhas pressurizadas próximas à área do içamento e tenha recomendado uma estratégia de içamento para reduzir o potencial de dano às linhas identificadas, essas informações não foram transferidas para a força de trabalho. Como consequência, houve contribuição para o dano a equipamentos e para a near catastrophe.\n  Trecho: \"Although the pre-job Hazard Analysis identified the risk of an accidental rupture of pressurized gas lines in proximity to the area where the lift was occurring, and it recommended a lift strategy that reduced the potential to damage the identified gas lines, this information appears not to have been transferred to th…\" [BSEE (EUA) · Safety Alert 317 - Catastrophic Incident Avoided - June 12, 2015, p. 1]\n• O Lift Plan descreveu um procedimento de içamento, mas não forneceu o contexto das premissas e dos riscos potenciais que deveriam ser mitigados por aquelas instruções. Também não forneceu orientação sobre riscos potenciais, o que foi apontado como fator contribuinte para o incidente.\n  Trecho: \"The Lift Plan outlined a lifting procedure but did not provide background on the assumptions and potential risks that were to be mitigated by those instructions, neither did it provide guidance on potential risks\" [BSEE (EUA) · Safety Alert 317 - Catastrophic Incident Avoided - June 12, 2015, p. 1]"
 },
 {
  "codigo": "Q039",
  "id": "b56db319e4-s0002-A1",
  "topico": "Logística, Suprimentos e Movimentação de Cargas",
  "subtopico": "Logística e Suprimento Offshore",
  "nivel": "Difícil (cenário em um conceito)",
  "dificuldade": "Difícil",
  "pergunta": "Um RSV será mobilizado para uma intervenção com ROV a 3200 m de profundidade. A embarcação dispõe de alimentação em alta tensão AC, telemetria por fibra e lançamento/recuperação por A-frame hidráulico. Qual classe de ROV é a mais compatível com essa campanha?",
  "resposta": "WCROV.",
  "pontos_essenciais": [
   "Indicar WCROV"
  ],
  "explicacao": "A profundidade requerida está acima de 3000 m e o arranjo disponível no RSV coincide com os requisitos associados ao WCROV: alta tensão em AC, transmissão por fibra e A-frame hidráulico. O MSROV é associado a profundidades acima de 1000 m, mas com outro conjunto típico de alimentação, transmissão e lançamento.",
  "contexto": "Nota técnica: Critérios de seleção da classe de ROV e do sistema de lançamento/recuperação em operações profundas\nResumo: A escolha entre classes de ROV em campanhas offshore profundas depende do conjunto profundidade operacional, arquitetura elétrica, meio de telemetria e arranjo de lançamento/recuperação disponível no RSV. Na referência fornecida, o aumento da profundidade está associado a classes com diferentes requisitos de alimentação elétrica, transmissão e manuseio, o que afeta a preparação logística da embarcação de apoio.\nConhecimento que a questão deveria avaliar: Dado um cenário com profundidade requerida acima de 1000 m ou acima de 3000 m, justificar qual classe entre MSROV e WCROV é a mais compatível, integrando profundidade, alimentação elétrica, meio de transmissão e arranjo de lançamento/recuperação indicado na referência.\n\nFatos das fontes usados na resposta (afirmação e trecho original):\n• O veículo MSROV (440/480) opera em profundidades maiores que 1000 m e utiliza fonte de tensão de média (AC ou DC), com materiais condutores de cobre ou fibra. No quadro apresentado, o lançamento é indicado como TMS.\n  Trecho: \"MSROV 440/480 Média AC ou DC Cobre ou Fibra >1000m Guindaste opcional elétrico/hidráulico\" [REGIS · 4439_TCC%20THIAGO%20VAZ.pdf]\n• O veículo WCROV (440/480) é associado a profundidades maiores que 3000 m, com fonte de tensão de alta (AC) e transmissão por fibra. No quadro, a categoria indica A-frame sim hidráulico/hidráulico.\n  Trecho: \"WCROV 440/480 Alta AC Fibra >3000m A-frame sim hidráulico/hidráulico\" [REGIS · 4439_TCC%20THIAGO%20VAZ.pdf]"
 },
 {
  "codigo": "Q040",
  "id": "26d45ade58-s0005-A1",
  "topico": "Logística, Suprimentos e Movimentação de Cargas",
  "subtopico": "Movimentação de Cargas",
  "nivel": "Difícil (integra dois ou mais conceitos)",
  "dificuldade": "Difícil",
  "pergunta": "Um FIBC será içado com peso total dentro do limite nominal. Na inspeção prévia, uma das alças apresenta degradação visível, e o arranjo proposto não assegura distribuição igual de esforços entre as alças. Qual ação deve vir primeiro antes da manobra?",
  "resposta": "Retirar o FIBC de serviço e não liberar o içamento.",
  "pontos_essenciais": [
   "retirar o FIBC de serviço antes do içamento",
   "a degradação visível da alça impede a liberação, mesmo com peso dentro do limite nominal"
  ],
  "explicacao": "Pelo critério operacional, qualquer degradação observada nas alças exige retirada de serviço antes do içamento. Além disso, sem distribuição uniforme de esforços, cresce o risco de sobrecarga localizada; portanto, o peso nominal isoladamente não autoriza a manobra.",
  "contexto": "Nota técnica: Integridade e limitações de FIBCs no içamento offshore\nResumo: FIBCs podem ser usados para movimentar materiais, mas sua integridade no içamento offshore depende fortemente do estado das alças, das condições ambientais e de como a carga é distribuída entre os pontos de içamento. O material mostra que intempéries, saturação por água, presença de detritos e frio com carga pesada ou desigual aumentam a probabilidade de fragilização e ruptura, o que desloca a decisão operacional para inspeção rigorosa, retirada de serviço ou uso de método alternativo de içamen…\nNota técnica: Distribuição de esforços entre alças e técnica de içamento em múltiplos pontos para FIBC\nResumo: Na movimentação de FIBC, a integridade da carga depende de como o peso é compartilhado entre as alças durante o içamento. O material fornecido sustenta duas orientações operacionais centrais: distribuir igualmente a força entre as alças e preferir a técnica de içamento em quatro pontos, em vez de ponto único, para preservar a condição de carregamento para a qual o conjunto foi concebido.\nNota técnica: Inspeção das alças do FIBC e retirada de serviço antes do içamento\nResumo: A segurança do içamento com FIBC não depende apenas da distribuição teórica de esforços entre as alças, mas também da capacidade real de cada ponto de sustentação no momento da manobra. Quando há degradação visível em qualquer alça, o critério recomendado é retirar o FIBC de serviço antes do içamento, porque a deterioração compromete a integridade da sustentação e eleva o risco de falha e de sobrecarga localizada.\nConhecimento que a questão deveria avaliar: FIBC aparentemente intacto, mas inseguro por combinação de degradação e má distribuição de esforços. Ligação: No FIBC, a integridade do içamento depende simultaneamente da condição real das alças e da forma como o peso é distribuído entre elas. A degradação visível de uma alça e a distribuição desigual de esforços são mecanismos diferentes que se reforçam: uma alça já enfraquecida pode se tornar o elo limitante justamente quando o método de içamento concentra carga localmente. Raciocínio exigido: A boa resposta precisa unir mecânica de compartilhamento de carga e critério de retirada de servi…\n\nFatos das fontes usados na resposta (afirmação e trecho original):\n• Durante reuniões de segurança antes do trabalho, deve-se enfatizar que a força aplicada a cada alça do FIBC seja igualmente distribuída para prevenir sobrecarga.\n  Trecho: \"Emphasize during safety meetings before the job that the force applied to each FIBC strap is equally distributed to prevent overloading.\" [BSEE (EUA) · BSEE Safety Alert 428 - Flexible Intermediate Bulk Container - FIBC - Parted St…, p. 2]\n• Deve-se aplicar uma técnica de içamento de quatro pontos nas alças do FIBC para manter a integridade da carga como projetada no local, ao invés de utilizar içamento em um único ponto.\n  Trecho: \"Ensure a 4-point lifting technique is applied to the FIBC straps to maintain the integrity of the load as designed in place of utilizing a single-point lift.\" [BSEE (EUA) · BSEE Safety Alert 428 - Flexible Intermediate Bulk Container - FIBC - Parted St…, p. 2]\n• Deve-se gerar um protocolo de inspeção e retirar o FIBC de serviço antes do içamento caso seja observada qualquer degradação nas alças pré-fabricadas. Também é recomendado distribuir igualmente a força aplicada a cada alça durante as reuniões de segurança antes da atividade para evitar sobrecarga.\n  Trecho: \"· Generate an inspection protocol and remove the FIBC from service before lifting if any degradation is observed in the pre-manufactured straps.. · Emphasize during safety meetings before the job that the force applied to each FIBC strap is equally distributed to prevent overloading.\" [BSEE (EUA) · BSEE Safety Al…"
 },
 {
  "codigo": "Q041",
  "id": "d21b4ace38-s0000-A1",
  "topico": "Manutenção, Inspeção e Integridade de Ativos",
  "subtopico": "Manutenção e Plano de Manutenção",
  "nivel": "Fácil",
  "dificuldade": "Fácil",
  "pergunta": "Qual critério deve ser usado para priorizar a manutenção quando há poucos mantenedores a bordo em uma unidade offshore?",
  "resposta": "A criticidade dos equipamentos, priorizando os de maior impacto potencial sobre produção, segurança da plataforma e meio ambiente.",
  "pontos_essenciais": [
   "uso da criticidade como critério de priorização",
   "foco nos equipamentos de maior impacto em produção, segurança e meio ambiente"
  ],
  "explicacao": "Com equipe de manutenção limitada a bordo, não é viável aplicar o mesmo esforço a todo o parque de equipamentos. Por isso, a filosofia de manutenção concentra recursos nos ativos mais críticos, definidos pelo impacto potencial de sua falha.",
  "contexto": "Nota técnica: Premissas da filosofia de manutenção: alinhamento ao negócio, criticidade e revisão ao longo do ciclo de vida\nResumo: A filosofia de manutenção é um conjunto de premissas que orienta como a empresa escolhe e prioriza suas abordagens de manutenção de acordo com a estratégia de negócio e com as restrições operacionais e financeiras do contexto offshore. Em unidades com recursos humanos limitados a bordo, essa filosofia precisa transformar criticidade e risco em critérios de priorização e não pode permanecer fixa: envelhecimento, intensidade de uso, experiência operacional e mudanças na aceitação de risco exigem…\nConhecimento que a questão deveria avaliar: Descrever como a limitação de mantenedores a bordo justifica a priorização de equipamentos por criticidade.\n\nFatos das fontes usados na resposta (afirmação e trecho original):\n• A limitação de recursos humanos a bordo justifica otimizar as estratégias de manutenção, priorizando equipamentos de maior criticidade. O método proposto classifica os equipamentos em quatro níveis de criticidade (altíssima, alta, média e baixa) em função do impacto na produção, segurança da plataforma e meio ambiente, entre outros fatores.\n  Trecho: \"Considerando o grande parque de equipamentos instalados e a limitação de mão-de-obra a bordo, é essencial que a estratégia de manutenção priorize os equipamentos de maior criticidade. Por essa razão, o método de priorização proposto classifica os equipamentos em 4 níveis de criticidade: altíssima, alta, média e baixa,…\" [REGIS · 5283_AlanRomuloSilvaQueirozOrigSemCorr16.pdf]\n• As políticas e diretrizes de manutenção são premissas adotadas com foco na estratégia de negócio, com base nas restrições operacionais e financeiras. Em ambientes offshore, uma restrição operacional significativa é a quantidade reduzida de mantenedores a bordo das unidades marítimas.\n  Trecho: \"As políticas e diretrizes de manutenção são premissas adotadas por cada empresa com foco em sua estratégia de negócio e com base nas suas restrições operacionais e financeiras. Na área de Exploração e Produção em ambientes offshore, uma restrição operacional significativa é a quantidade reduzida de mantenedores a bordo\" [REGIS · 5283_AlanRomuloSilvaQueirozOrigSemCorr16.pdf]\n• As políticas e diretrizes de manutenção são premissas adotadas por cada empresa com foco na estratégia de negócio e com base em restrições operacionais e financeiras. Em ambientes offshore, a quantidade reduzida de mantenedores a bordo é apresentada como restrição operacional significativa usada para orientar as diretrizes.\n  Trecho: \"As políticas e diretrizes de manutenção são premissas adotadas por cada empresa com foco em sua estratégia de negócio e com base nas suas restrições operacionais e financeiras. Na área de Exploração e Produção em ambientes offshore, uma restrição operacional significativa é a quantidade reduzida de mantenedores a bord…\" [REGIS · 5283_AlanRomuloSilvaQueirozOrigSemCorr16.pdf]"
 },
 {
  "codigo": "Q042",
  "id": "460979b6f3-s0001-A1",
  "topico": "Manutenção, Inspeção e Integridade de Ativos",
  "subtopico": "Inspeção e Integridade",
  "nivel": "Média",
  "dificuldade": "Média",
  "pergunta": "Em um programa de RBI, um equipamento passou a operar em condição diferente da original e inspeções recentes melhoraram o entendimento do dano ativo. Como essas informações devem entrar na atualização do risco e no plano de inspeção desse item?",
  "resposta": "Devem recalibrar a estimativa de risco com base nos mecanismos de dano e no histórico operacional, redefinindo a prioridade e ajustando frequência, método e escopo da inspeção.",
  "pontos_essenciais": [
   "atualizar o risco considerando mecanismos de dano e histórico operacional",
   "ajustar prioridade e plano de inspeção, como frequência, método ou escopo"
  ],
  "explicacao": "Na RBI, o risco não é estático: mudanças de operação e novos achados alteram a percepção de risco do equipamento. Como o plano deve ser coerente com os mecanismos de dano atuantes, a atualização do risco reordena prioridades e pode mudar frequência, métodos, testes e extensão da inspeção.",
  "contexto": "Nota técnica: RBI/IBR como base para priorização e otimização dinâmica dos planos de inspeção\nResumo: A RBI/IBR usa o risco como critério para decidir onde inspecionar primeiro, combinando probabilidade de falha e consequência de falha para classificar equipamentos e direcionar recursos. O plano resultante não é estático: novas inspeções, mudanças no histórico operacional e melhor entendimento dos mecanismos de dano alteram a percepção de risco e reordenam prioridades, frequência, escopo e métodos de inspeção.\nConhecimento que a questão deveria avaliar: Descrever como mecanismos de dano atuantes e histórico operacional entram na atualização do risco e influenciam a definição do plano de inspeção.\n\nFatos das fontes usados na resposta (afirmação e trecho original):\n• O estabelecimento de planos de inspeção coerentes com os mecanismos de danos atuantes em cada equipamento, aliado ao uso do histórico operacional para atualizar o risco, integra qualitativo e quantitativo para combinar probabilidade e consequência de falhas. Essa combinação serve para determinar quais equipamentos devem receber inspeção e manutenção prioritariamente.\n  Trecho: \"gerenciando o risco pelo estabelecimento de planos de inspeção coerentes com os mecanismos de danos atuantes em cada equipamento e permitindo a utilização do histórico operacional do equipamento para atualização do risco É considerada integrada porque envolve processos qualitativos e quantitativos para combinação tant…\" [REGIS · 14573_000737025.pdf]\n• A IBR considera o risco como guia nas decisões de inspeção e manutenção e permite gerenciar o risco por meio de planos coerentes com os mecanismos de danos de cada equipamento. A metodologia utiliza o histórico operacional do equipamento para atualização do risco.\n  Trecho: \"a inspeção Baseada em Risco (IBR), apresentada nos documentos API RP 580 e API STD 581, é uma metodologia integrada que considera e evidencia o risco como guia nas decisões de inspeção e manutenção de equipamentos, gerenciando o risco pelo estabelecimento de planos de inspeção coerentes com os mecanismos de danos atua…\" [REGIS · 14573_000737025.pdf]\n• A ordem de prioridades muda à medida que inspeções são realizadas, tornando a inspeção um processo dinâmico. A percepção de risco é sempre alterada conforme novas inspeções e alterações no plano de inspeção são realizadas.\n  Trecho: \"A medida que são realizadas inspeções, a ordem de prioridades é alterada, fazendo da inspeção um processo dinâmico, onde a percepção de risco é sempre alterada à medida que novas inspeções e alterações no plano de inspeção são realizadas\" [REGIS · 14573_000737025.pdf]\n• Com base nos resultados da análise RBI, podem ser alterados a frequência de inspeção, os métodos, ferramentas e testes utilizados, bem como o escopo, a qualidade e a extensão da inspeção. A análise também pode sugerir técnicas globais de inspeção como termografia e emissão acústica para acompanhamento do dano em serviço.\n  Trecho: \"LAFRAIA (2001) afirma que fundamentados nos resultados da análise, podem ser alterados a freqüência de inspeção, os métodos, ferramentas e testes utilizados, bem como o escopo, a qualidade e a extensão da inspeção. A análise pode ainda, sugerir a utilização de técnicas globais de inspeção como a termografia e a emissã…\" [REGIS · 14573_000737025.pdf]"
 },
 {
  "codigo": "Q043",
  "id": "a807dbd01e-s0001-A1",
  "topico": "Manutenção, Inspeção e Integridade de Ativos",
  "subtopico": "Apoio Técnico e Manutenção em um FPSO (Laboratório, Oficinas, Pipe Shop)",
  "nivel": "Média",
  "dificuldade": "Média",
  "pergunta": "Na gestão de sobressalentes de um FPSO, uma política só reavalia o estoque em intervalos fixos e, em cada revisão, calcula o pedido pela diferença entre o nível máximo e o saldo observado. Qual é essa política de reposição?",
  "resposta": "Reposição periódica.",
  "pontos_essenciais": [
   "identificar a política como reposição periódica"
  ],
  "explicacao": "Essa política se distingue porque o controle ocorre por revisões em datas fixas, e a quantidade a repor é calculada como MAX menos o estoque observado na revisão. Isso a diferencia do ponto de ressuprimento, que dispara pedido quando o saldo cai abaixo do gatilho, e da reposição contínua, baseada em ressuprimento automático.",
  "contexto": "Nota técnica: Políticas de ressuprimento e parametrização de níveis de estoque para sobressalentes\nResumo: A parametrização de estoque para sobressalentes depende da política de ressuprimento adotada, porque ponto de reposição, níveis mínimo e máximo, lote e frequência de revisão respondem de modo diferente à incerteza de demanda, ao lead time e à meta de nível de serviço. Os fatos fornecidos sustentam que o dimensionamento deve cobrir demanda e prazo de entrega sem elevar excessivamente o custo de inventário, e que a escolha entre reposição contínua, periódica, puxada e JIT muda a forma de controla…\nConhecimento que a questão deveria avaliar: Comparar reposição contínua, ponto de ressuprimento e reposição periódica quanto ao gatilho de pedido, ao cálculo da quantidade a repor e à forma de controle do estoque.\n\nFatos das fontes usados na resposta (afirmação e trecho original):\n• Na reposição periódica, existe um período fixo para revisões das quantidades em estoque. O pedido de ressuprimento é calculado como a diferença entre um nível máximo (MAX) e o valor em estoque no momento da revisão.\n  Trecho: \"Quantidade variável conhecido também como reposição periódica tem um período fixo para efetuar revisões periódicas das quantidades em estoque Um pedido de ressuprimento é calculado como a diferença entre um nível máximo MAX e o valor em estoque no momento da revisão MAX é definido a partir da demanda durante o tempo d…\" [Petrolês · corpusPublicoIBICT-SemProcessamento.txt]\n• No método do estoque mínimo (ponto de ressuprimento), busca-se controlar o valor ótimo em estoque. Quando o estoque cai abaixo do ponto de ressuprimento, solicita-se um pedido de lote de ressuprimento à produção, e a quantidade é definida como o lote econômico de reposição que equilibra custos de manutenção do estoque e de produção.\n  Trecho: \"Ponto de ressuprimento conhecido como método do estoque mínimo busca controlar o valor ótimo em estoque de maneira que quando o estoque cai abaixo de um valor conhecido denominado ponto de ressuprimento um pedido de um lote de ressuprimento é solicitado à produção\" [Petrolês · corpusPublicoIBICT-SemProcessamento.txt]\n• RC (Reposição contínua) é um processo de ressuprimento automático de estoques. O mecanismo descrito é a reposição automática via processo de ressuprimento contínuo.\n  Trecho: \"RC Reposição contínua Ressuprimento automático Processo de reposição automatica de estoques\" [REGIS · 13256_225305.pdf]"
 },
 {
  "codigo": "Q044",
  "id": "e1b6ad83e3-s0002-A1",
  "topico": "Manutenção, Inspeção e Integridade de Ativos",
  "subtopico": "Cibersegurança e Integridade de Sistemas Digitais",
  "nivel": "Difícil (cenário em um conceito)",
  "dificuldade": "Difícil",
  "pergunta": "Um FPSO já permite monitoramento remoto a partir de terra e tem canal digital em banda larga capaz de reproduzir à distância as mesmas operações disponíveis a bordo. A arquitetura é modular e a expansão da rede não compromete a continuidade operacional. Antes de liberar uma função remota de intervenção, qual critério deve decidir se ela pode ser habilitada?",
  "resposta": "A compatibilidade da função com o nível de privilégio autorizado e com o risco adicional de exposição da rede, não apenas a existência de conectividade remota.",
  "pontos_essenciais": [
   "privilégios de usuário autorizados",
   "risco/exposição da rede para a função remota"
  ],
  "explicacao": "A conectividade integrada e o canal de longa distância viabilizam monitoramento e operação remotos, mas isso não basta para liberar qualquer intervenção. O projeto deve condicionar a função remota ao privilégio do usuário e ao risco introduzido pela ampliação do acesso, preservando a continuidade operacional.",
  "contexto": "Nota técnica: Arquitetura integrada de redes e acesso remoto em sistemas digitais de FPSO\nResumo: A integração entre redes operacionais e corporativas, quando implementada em arquitetura distribuída, modular e escalável, amplia a visibilidade sobre dispositivos e processos, acelera o diagnóstico de causas-raiz e favorece atuação pró-ativa para reduzir paradas. Ao mesmo tempo, a ampliação da conectividade e do acesso remoto aumenta a exposição dos sistemas, exigindo desenho de permissões, barreiras de rede e mecanismos de mudança remota compatíveis com a operação segura dos sistemas de autom…\nConhecimento que a questão deveria avaliar: Avaliar o critério de projeto para decidir quando uma função remota deve permanecer restrita e quando pode ser liberada, integrando risco de conectividade ampliada, continuidade operacional e necessidade de suporte remoto.\n\nFatos das fontes usados na resposta (afirmação e trecho original):\n• Com a existência de Rede Ethernet na Plataforma Petrolífera Offshore, pessoas embarcadas podem acessar a Rede Corporativa e Intranet para desenvolver atividades (correio e troca de informações) e acessar a Rede Internet para lazer, aperfeiçoamento e consultas. Também é possível que qualquer pessoa de qualquer lugar da Rede Corporativa da PETROBRAS, usando softwares e privilégios de usuário, monit…\n  Trecho: \"Com a existência da Rede Ethernet na Plataforma Petrolífera Offshore as pessoas que porventura estiverem embarcadas podem acessar a Rede Corporativa e Intranet para desenvolver suas atividades correio troca de informações etc como também acessar a Rede Internet para momento de lazer aperfeiçoamento e consultas\" [Petrolês · corpusPublicoIBICT-SemProcessamento.txt]\n• Com a utilização do Canal de Dados Digitais de Longa Distância em Banda Larga interligando a Plataforma Petrolífera Offshore à Estação Onshore, podem ser realizadas as mesmas atividades de acesso e operação que são viabilizadas pela rede.\n  Trecho: \"Com a utilização do Canal de Dados Digitais de Longa Distância em Banda Larga interligando a Plataforma Petrolífera Offshore à Estação Onshore podem ser realizadas as mesmas atividades\" [Petrolês · corpusPublicoIBICT-SemProcessamento.txt]\n• Em redes integradas, o acréscimo de mais elementos não impacta a continuidade operacional. Isso é associado à construção de plantas em arranjo modular, com implementação escalável de novos sistemas à rede.\n  Trecho: \"Isto é feito de forma escalável uma vez que que numa rede integrada o acréscimo de mais elementos não impacta sua continuidade operacional O cerne das otimizações permitidas nestes sistemas está na aplicação de algoritmos de Business Analytics\" [Petrolês · corpusPublico(sem IBICT)-SemProcessamento.txt]\n• A integração das redes permite determinar causas-raiz de problemas que podem levar a planta a um shutdown. Com essa integração, a atuação pode ser pró-ativa, mantendo os sistemas estabilizados e menos sujeitos a paradas.\n  Trecho: \"A integração das redes permite mais agilidade e precisão na determinação de causas raízes para os problemas que podem levar a planta a um shutdown e permitindo atuação de forma pró-ativa mantendo assim os sistemas estabilizados e menos sujeito a paradas\" [Petrolês · corpusPublico(sem IBICT)-SemProcessamento.txt]"
 },
 {
  "codigo": "Q045",
  "id": "d21b4ace38-s0002-A1",
  "topico": "Manutenção, Inspeção e Integridade de Ativos",
  "subtopico": "Manutenção e Plano de Manutenção",
  "nivel": "Difícil (cenário em um conceito)",
  "dificuldade": "Difícil",
  "pergunta": "Em um FPSO, o CMMS está completo quanto a cadastro, planos, ordens e histórico, mas os equipamentos classificados como críticos em estudos de segurança não foram identificados no sistema. Qual é o efeito mais direto dessa lacuna sobre a gestão da integridade?",
  "resposta": "A gestão informatizada perde aderência à criticidade de integridade, porque o sistema deixa de tratar esses equipamentos e sistemas como críticos.",
  "pontos_essenciais": [
   "perda de aderência da gestão informatizada à criticidade/integridade",
   "ausência de identificação dos Equipamentos e Sistemas Críticos no sistema"
  ],
  "explicacao": "As informações de Equipamentos e Sistemas Críticos devem constar no sistema informatizado. Sem isso, mesmo com cadastro e planos completos, o CMMS não representa integralmente a criticidade definida nos estudos de segurança, limitando a gestão da integridade.",
  "contexto": "Nota técnica: Estruturação do cadastro de ativos e dos planos de manutenção no CMMS/SAP PM\nResumo: A eficácia do CMMS/SAP PM depende de uma cadeia lógica: cadastro consistente do equipamento, identificação física por TAG, lista de tarefas, plano preventivo, definição do início de ciclo e geração de ordens de serviço. Quando essa base cadastral é incompleta ou inconsistente, o sistema perde eficácia para gerir ordens, acumular histórico confiável e sustentar programas preventivos aderentes aos ativos e, quando aplicável, aos equipamentos e sistemas críticos definidos em estudos de segurança.\nConhecimento que a questão deveria avaliar: Justificar por que informações de Equipamentos e Sistemas Críticos oriundas de estudos de segurança devem ser incorporadas ao sistema informatizado e como isso influencia a gestão da integridade.\n\nFatos das fontes usados na resposta (afirmação e trecho original):\n• As informações de Equipamentos e Sistemas Críticos oriundas de estudos de segurança devem ser incluídas nos sistemas informatizados de gerenciamento.\n  Trecho: \"R29: Incluir as informações de Equipamentos e Siste mas Críticos oriundas de estudos de segurança nos sistemas informatizados de gerenciame nto de\" [ANP · Resumo técnico executivo do Relatório de Investigação do incidente de explosão…, p. 34]\n• O sistema de gestão de manutenção informatizado (CMMS) deve comportar, no mínimo, gestão de ordens de serviço, planejamento e programação, histórico de equipamentos, orçamento/custo, recursos de trabalho, gestão de stock e relatórios com indicadores-chave de desempenho (KPIs). Para ser totalmente eficaz, o CMMS deve ser implementado com base em dados de equipamentos completos e precisos, dados de…\n  Trecho: \"Para ser totalmente eficaz, o CMMS deve ser implementado com base nos dados de equipamentos completos e precisos, dados de peças e materiais, planos\" [REGIS · 4421_APLICA%c3%87%c3%83O%20DE%20UMA%20METODOLOGIA%20DE%20MANUTEN%c3%87%c3%83O%2…]"
 },
 {
  "codigo": "Q046",
  "id": "3204097d51-s0000-A1",
  "topico": "Segurança Ocupacional, Saúde e Meio Ambiente",
  "subtopico": "Condições Ambientais e Impactos Operacionais",
  "nivel": "Fácil",
  "dificuldade": "Fácil",
  "pergunta": "Por que a extensão de vida útil de uma FPSO/FSO não pode ser tratada apenas como prorrogação de prazo para continuar operando?",
  "resposta": "Porque a continuidade operacional só se sustenta se as avaliações de integridade atenderem às condicionantes e aos limites definidos no estudo de EVU.",
  "pontos_essenciais": [
   "continuidade operacional depende de avaliações de integridade",
   "atendimento às condicionantes e limites do estudo de EVU"
  ],
  "explicacao": "A extensão de vida útil não é uma mera decisão de calendário. A operação só pode continuar quando a base técnica de integridade ainda sustenta a unidade dentro das condicionantes impostas pelo estudo e dos limites estabelecidos para a continuidade operacional.",
  "contexto": "Nota técnica: Alterações meteoceanográficas na extensão de vida útil: revalidação da base de segurança e integridade\nResumo: Ao longo da vida de uma FPSO/FSO, a continuidade operacional em extensão de vida útil não se resume à prorrogação de prazo. Ela depende do atendimento de avaliações de integridade e das condicionantes impostas pelos estudos de EVU. Em paralelo, o safety case deve permanecer um documento ativo ao longo da vida da instalação e sua revisão completa deve considerar a integridade associada ao envelhecimento na fase tardia, para confirmar que ele continua fundamentalmente sólido. Em engenharia, mudan…\nConhecimento que a questão deveria avaliar: Explicar por que a extensão de vida útil de uma unidade flutuante não pode ser tratada apenas como prorrogação de prazo, mas depende de avaliações de integridade e do atendimento de condicionantes para continuidade operacional.\n\nFatos das fontes usados na resposta (afirmação e trecho original):\n• As notificações tiveram o objetivo de garantir atendimento às condicionantes impostas pelos estudos de extensão de vida útil (EVU) para a continuidade operacional. Também buscaram assegurar respeito aos limites definidos pelos estudos quanto à data final para paralisação.\n  Trecho: \"extensão de vida útil condici onada ao ate ndimento de uma série de avaliações de integridade. Assim, as notificações tiveram como objetivo garantir que todas as condicionantes impostas pelos estudos de EVU fossem atendidas para sua continuidade operacional e que fossem respeitados os l imites impostos pelos estudos e…\" [ANP · 2019, p. 33]"
 },
 {
  "codigo": "Q047",
  "id": "7408dc2a56-s0003-A1",
  "topico": "Segurança Ocupacional, Saúde e Meio Ambiente",
  "subtopico": "Gestão de Pessoas e Treinamento",
  "nivel": "Média",
  "dificuldade": "Média",
  "pergunta": "Na definição da reciclagem de um procedimento operacional offshore, a tarefa é crítica, complexa, associada a cenários severos, executada com baixa frequência e o procedimento foi recentemente revisado. O que isso implica para a periodicidade do treinamento?",
  "resposta": "A reciclagem deve ser mais frequente e revista imediatamente, com atualização específica antes da execução na condição modificada.",
  "pontos_essenciais": [
   "periodicidade mais frequente/encurtada",
   "revisão imediata por mudança de procedimento"
  ],
  "explicacao": "A periodicidade não deve ser fixa: ela precisa acompanhar criticidade, complexidade, severidade dos cenários, frequência de execução e atualizações dos procedimentos. Tarefas pouco frequentes e de maior consequência exigem reforço mais próximo da execução, e mudanças de procedimento exigem atualização específica sem esperar o ciclo periódico regular.",
  "contexto": "Nota técnica: Planejamento do treinamento por tarefas críticas, competência e reciclagem\nResumo: O programa de treinamento em instalações offshore deve ser estruturado a partir da análise das tarefas e atividades críticas para segurança e meio ambiente, relacionando as consequências de uma execução incorreta com os conhecimentos, habilidades técnicas e comportamentais exigidos para atuar em condições normais, anormais e de emergência. A definição de treinamento inicial, periódico e após modificações, bem como a frequência de reciclagem, deve considerar criticidade, complexidade, severidade…\nConhecimento que a questão deveria avaliar: Relacionar criticidade, complexidade, severidade dos cenários, frequência de execução da tarefa e atualização de procedimentos com a definição da periodicidade de reciclagem.\n\nFatos das fontes usados na resposta (afirmação e trecho original):\n• A periodicidade do treinamento deve ser avaliada quanto à compatibilidade com a complexidade, severidade dos cenários, frequência de realização das tarefas e atualizações dos procedimentos.\n  Trecho: \"1.2. R-ADB-03-02: Avaliar a compaƟbilidade da periodicidade de treinamento com a complexidade, severidade dos cenários, frequência de realização das tarefas e atualizações dos procedimentos.\" [ANP · Nota Técnica nº 4/2022/SSM-CSO/SSM/ANP-RJ de 15/3/2022:, p. 4]\n• O Programa de Gerenciamento de Risco deve prever um programa de treinamento para todas as pessoas responsáveis pelas operações realizadas na empresa, de acordo com suas funções e atribuições. Os treinamentos devem contemplar procedimentos operacionais, incluindo modificações em instalações e na tecnologia de processo, e devem ser do tipo treinamento inicial, treinamento periódico e treinamento ap…\n  Trecho: \"f) A capacitação de recursos humanos – o Programa de Gerenciamento de Risco deve prever um programa de treinamento para todas as pessoas responsáveis pelas operações realizadas na empresa, de acordo com suas diferentes funções e atribuições. Os treinamentos devem contemplar os procedimentos operacionais, incluindo eve…\" [REGIS · 7264_DISSERTA%c3%87%c3%83O_BomUsoPrinc%c3%adpio.pdf]\n• Deve existir programa de treinamento contínuo em procedimentos operacionais, com frequência de reciclagem diferenciada para procedimentos críticos.\n  Trecho: \"R17: Estabelecer programa de treinamento contínuo em procedimentos operacionais, sendo a frequência de reciclagem em procedimentos críticos diferenciada.\" [ANP · Relatório final da investigação do FPSO Cidade de São Mateus, p. 277]"
 },
 {
  "codigo": "Q048",
  "id": "b8c888d001-s0001-A1",
  "topico": "Segurança Ocupacional, Saúde e Meio Ambiente",
  "subtopico": "Saúde Ocupacional",
  "nivel": "Média",
  "dificuldade": "Média",
  "pergunta": "Em uma unidade offshore, o protocolo de restrições laborais para doença infecciosa pressupõe identificar previamente trabalhadores com maior risco de agravamento. Sob regras de privacidade médica que impedem triagem clínica por terceiros, qual limitação passa a afetar essa identificação?",
  "resposta": "A identificação fica dependente de autodeclaração do próprio trabalhador, tornando incompleto o reconhecimento prévio dos grupos de maior risco clínico.",
  "pontos_essenciais": [
   "dependência de autodeclaração",
   "identificação prévia de alto risco fica limitada/incompleta"
  ],
  "explicacao": "Quando regras de privacidade médica restringem o acesso do empregador às condições de saúde, o processo deixa de se apoiar em triagem por terceiros e passa a depender de autodeclaração. Isso reduz a robustez do acompanhamento de restrições, porque a organização não consegue presumir que já conhece todos os trabalhadores de maior risco clínico.",
  "contexto": "Nota técnica: Gestão de casos de doença, restrições e retorno seguro ao trabalho offshore\nResumo: A gestão de casos de doença infecciosa offshore precisa conectar monitoramento de saúde, isolamento, bloqueio de circulação de suspeitos ou doentes, comunicação operacional, sanitização e um processo formal de retorno ao trabalho. O material também mostra uma limitação prática relevante: sob regras de privacidade médica na jurisdição analisada, a identificação de trabalhadores com maior risco de agravamento dependia sobretudo de autodeclaração, o que afeta a robustez do acompanhamento de restri…\nConhecimento que a questão deveria avaliar: Explicar como regras de privacidade médica podem limitar a identificação de trabalhadores com maior risco clínico quando o processo depende de autodeclaração.\n\nFatos das fontes usados na resposta (afirmação e trecho original):\n• Devido a regras de privacidade médica, a maioria dos operadores dependia de que os empregados se autodeclarassem como grupo de alto risco para doença grave por COVID-19. O mecanismo de identificação de alto risco, portanto, era baseado em autodeclaração em vez de triagem por terceiros.\n  Trecho: \"Due to medical privacy rules, most operators relied on employees to self-identify as high risk for severe illness from COVID-19.\" [BSEE (EUA) · BSEE Safety Alert 403 - Findings from Pandemic Management Risk Based Inspections, p. 1]\n• Os planos devem incluir protocolos de monitoramento de saúde. Devem avaliar estratégias para lidar com pessoal que possa ter contraído doença infecciosa, incluindo planejamento de isolamento, protocolo para impedir que pessoas doentes ou potencialmente infectadas circulem pela instalação, comunicação clara, procedimentos de sanitização, processos de manejo de casos e protocolo de retorno ao traba…\n  Trecho: \"Assess existing strategies for managing personnel who may have contracted an infectious disease, including isolation planning, protocol to prevent ill or potentially infected personnel from walking throughout a facility, clear communication to offshore personnel, sanitization procedures, case management processes, and…\" [BSEE (EUA) · BSEE Safety Alert 403 - Findings from Pandemic Management Risk Based Inspections, p. 2]"
 },
 {
  "codigo": "Q049",
  "id": "c3419532e4-s0002-A1",
  "topico": "Segurança Ocupacional, Saúde e Meio Ambiente",
  "subtopico": "Segurança Ocupacional",
  "nivel": "Difícil (cenário em um conceito)",
  "dificuldade": "Difícil",
  "pergunta": "Uma linha que já transportou hidrocarbonetos foi drenada por gravidade, aberta à atmosfera e isolada a montante apenas por uma válvula esfera fechada. A equipe solicita liberação para corte com maçarico. Qual decisão deve ser tomada antes do início do serviço?",
  "resposta": "Não liberar o hot work; exigir PTW escrito com verificação positiva de ausência de condição perigosa e, se persistir potencial de inflamáveis, aplicar controles de engenharia adequados.",
  "pontos_essenciais": [
   "não liberar o serviço a quente nessa condição",
   "exigir verificação positiva via PTW e controles de engenharia se houver potencial de inflamáveis"
  ],
  "explicacao": "Drenagem, despressurização e abertura à atmosfera não comprovam remoção completa de líquidos ou vapores inflamáveis, e uma única válvula fechada não demonstra isolamento seguro do trecho. Em trabalho de alto risco, a liberação deve ficar vinculada no PTW à comprovação positiva de condição segura; sem isso, a linha deve ser tratada como potencialmente contendo inflamáveis e o risco de flash fire precisa ser reduzido com controles de engenharia compatíveis.",
  "contexto": "Nota técnica: Intervenções críticas com inflamáveis: por que drenagem e isolamento simples não bastam, e como PTW, verificação positiva e barreiras efetivas reduzem o risco de flash fire\nResumo: Em intervenções com corte, abertura ou quebra de contenção em linhas e vasos que já tiveram inflamáveis, a condição segura não pode ser presumida a partir de drenagem por gravidade, despressurização ou fechamento de uma única válvula. O controle robusto depende de PTW para trabalhos de alto risco, verificação positiva de ausência de condição perigosa, controles de engenharia contra ignição/propagação e isolamento físico eficaz da área para impedir a exposição de pessoas.\nConhecimento que a questão deveria avaliar: Dado um cenário com linha previamente em serviço com hidrocarbonetos, drenada, aberta à atmosfera e isolada por uma única válvula, decidir se o serviço a quente pode ser liberado e justificar a decisão integrando PTW, verificação positiva e controles adicionais.\n\nFatos das fontes usados na resposta (afirmação e trecho original):\n• Exemplos de trabalhos de alto risco para os quais pode ser necessário usar procedimento de PTW escrito incluem hot work como soldagem, entrada em vasos, corte em tubulação que carrega substâncias perigosas, e trabalhos que requerem isolamento elétrico ou mecânico.\n  Trecho: \"Examples of high-risk jobs where a written permit to work procedure may need to be used include hot work such as welding, vessel entry, cutting into pipe-work carrying hazardous substances, and work that requires electr ical or mechanical isolation.\" [HSE (Reino Unido) · ed-control-of-work.pdf, p. 3]\n• Todas as linhas e vasos que anteriormente continham líquidos ou vapores inflamáveis devem ser tratados como ainda contendo gases/vapores inflamáveis até verificação positiva de ausência de condição perigosa. Linhas/vasos isolados apenas por uma única barreira (por exemplo, válvula esfera fechada) também devem ser assumidos como contendo hidrocarbonetos inflamáveis.\n  Trecho: \"Always assume that all piping and vessels that previously contained flammable liquids or vapors may still contain these flammable gasses until it has been positively verified that there is no longer hazardous.\" [BSEE (EUA) · bsee-safety-alert-453-fires-during-decommissioning-cause-injuries[1].pdf, p. 2]\n• Gravidade drenando um vaso ou tubulação e abrindo-os à atmosfera pode não ser suficiente para remover todos os líquidos e vapores inflamáveis. Isso implica que ações baseadas apenas em drenagem e despressurização à atmosfera não substituem a verificação positiva e o controle do risco.\n  Trecho: \"Understand that gravity draining a vessel or pipe and opening them to the atmosphere may not be sufficient to remove all flammable liquids and vapors.\" [BSEE (EUA) · bsee-safety-alert-453-fires-during-decommissioning-cause-injuries[1].pdf, p. 2]\n• Devem ser implementados controles de engenharia para minimizar o risco de flash fires, como instalação de flame arrestors ou sistemas de purga com gás inerte em áreas onde há trabalho a quente em equipamentos potencialmente inflamáveis. Esses controles visam reduzir a condição que permite propagação/ignição associada ao evento.\n  Trecho: \"Implement engineering controls to minimize the risk of flash fires, such as installing flame arrestors or inert gas purging systems in areas where hot work is conducted on potentially flammable equipment.\" [BSEE (EUA) · BSEE Safety Alert 488 - Flash Fires During Welding Operations.pdf, p. 3]"
 },
 {
  "codigo": "Q050",
  "id": "b8c888d001-s0002-A1",
  "topico": "Segurança Ocupacional, Saúde e Meio Ambiente",
  "subtopico": "Saúde Ocupacional",
  "nivel": "Difícil (cenário em um conceito)",
  "dificuldade": "Difícil",
  "pergunta": "Em uma unidade offshore, a AET existente gerou várias recomendações sobre mobiliário administrativo, mas a operação mantém abertura manual frequente de válvulas com grande esforço, alcances inadequados em painéis da planta e, na sala de controle, operadores usam sequências de compensação para contornar interfaces pouco aderentes ao uso real. Com recursos limitados para intervir neste ciclo, qual critério deve orientar a prioridade das ações ergonômicas?",
  "resposta": "Priorizar as tarefas rotineiras da planta e da sala de controle em que a atividade real evidencia compensações e exigências acima das capacidades dos usuários.",
  "pontos_essenciais": [
   "priorizar tarefas rotineiras reais da planta industrial e da sala de controle",
   "usar como critério as compensações/esforços observados frente às capacidades dos usuários"
  ],
  "explicacao": "A priorização ergonômica deve se basear na atividade real, não na prescrição formal nem em achados restritos a escritório. Quando o trabalho exige estratégias de compensação, esforço excessivo ou contornos operacionais para viabilizar a tarefa, isso indica inadequação do posto, equipamento ou interface ao uso e às capacidades dos operadores e deve vir antes de ajustes administrativos.",
  "contexto": "Nota técnica: Análise Ergonômica do Trabalho como adaptação do trabalho ao homem e base para adequação ergonômica de postos, equipamentos e sistemas\nResumo: Ergonomia, neste contexto, é a adaptação do trabalho ao homem, com foco no trabalhador em situação real de trabalho e nas suas capacidades e limitações. A Análise Ergonômica do Trabalho deve, por isso, examinar a atividade efetivamente executada, a distância entre tarefa prescrita e trabalho real, a variabilidade e a carga de trabalho, para orientar a adequação de postos, mobiliário, ferramentas, equipamentos, sistemas e ambientes como a sala de controle e a planta industrial. Em instalações of…\nConhecimento que a questão deveria avaliar: Defender critérios para priorizar intervenções ergonômicas em planta industrial e sala de controle com base na atividade real, nas capacidades dos usuários e nas evidências de compensações exigidas pelo trabalho.\n\nFatos das fontes usados na resposta (afirmação e trecho original):\n• Todas as instalações devem possuir Análise Ergonômica do Trabalho, com avaliação da adequação da ergonomia de equipamentos e sistemas da planta industrial ao uso e às capacidades dos usuários, comparando com boas práticas de engenharia. A expectativa da auditoria era que também houvesse evidências de implementação das recomendações dessa análise.\n  Trecho: \"Análise Ergonômica dos trabalhos a serem realizados na instalação, assim como evidências de implementação de suas recomendações. Que todas as instalações possuíssem uma Análise Ergonômica do Trabalho, com avaliação se a ergonomia dos equipamentos e sistemas da planta industrial estava adequada ao uso e às capacidades…\" [ANP · 2022, p. 67]\n• A análise ergonômica da atividade é a análise das estratégias usadas pelo operador para administrar a distância entre o trabalho prescrito e o trabalho real. Essa abordagem considera o sistema homem-tarefa na interpretação das situações de trabalho.\n  Trecho: \"Dessa forma Guérin et al <NUMBER> argumenta que a análise ergonômica da atividade é a análise das estratégias usadas pelo operador para administrar a distância entre o prescrito e o real do trabalho ou seja a análise do sistema homem-tarefa conforme ilustra a Figura <NUMBER>\" [Petrolês · corpusPublicoIBICT-SemProcessamento.txt]\n• A tarefa representa o que é prescrito pela empresa ao operador e não corresponde ao trabalho. A atividade de trabalho é uma estratégia de adaptação do operador à situação real de trabalho em relação à prescrição.\n  Trecho: \"O primeiro fundamento remete à distinção entre tarefa e atividade A tarefa representa o que é prescrito pela empresa ao operador e não é o trabalho enquanto que a atividade de trabalho é uma estratégia de adaptação do operador à situação real de trabalho objeto da prescrição\" [Petrolês · corpusPublicoIBICT-SemProcessamento.txt]\n• Embora a Análise Ergonômica do Trabalho já fosse um recurso considerado obrigatório em todas as instalações, foram observadas falhas de gerenciamento e implementação das recomendações provenientes dos relatórios. Também foi registrada baixa qualidade da maior parte dos relatórios, com foco em ergonomia “mesa-cadeira-computador” em vez de avaliação de tarefas rotineiras na planta industrial ou sal…\n  Trecho: \"Como a Análise Ergonômica do Trabalho já é um recurso obrigatório em todas as instalações, por força da norma NR-1716, foi observado que todas as instalações a possuíam. Todavia, poucas instalações de fato gerenciaram ou implementaram as recomendações provenientes dos relatórios. Além disso, a qualidade da maior parte…\" [ANP · 2022, p. 67]"
 }
];

function criarFormulario() {
  const inicio = Date.now();
  const props = PropertiesService.getScriptProperties();
  let estado = JSON.parse(props.getProperty('ESTADO') || 'null');
  if (!estado || estado.versao !== 4) {
    estado = { versao: 4, grupos: montarGrupos_(), atual: 0 };
  }
  const salvar = function () { props.setProperty('ESTADO', JSON.stringify(estado)); };
  while (estado.atual < estado.grupos.length) {
    const grupo = estado.grupos[estado.atual];
    if (!grupo.formIds.length) {
      novoFormulario_(grupo, salvar);
    }
    let form = FormApp.openById(grupo.formIds[grupo.formIds.length - 1]);
    let vazio = grupo.formIds.length > 1 && grupo.inicioParte === grupo.proxima;
    while (grupo.proxima < grupo.questoes.length) {
      if (Date.now() - inicio > LIMITE_MS) {
        salvar();
        Logger.log('Pausado por tempo: %s de %s questões criadas em "%s". Execute criarFormulario de novo.',
                   grupo.proxima, grupo.questoes.length, grupo.titulo);
        return;
      }
      const q = QUESTOES[grupo.questoes[grupo.proxima]];
      const criada = adicionarQuestao_(form, q, grupo.proxima + 1, grupo.questoes.length);
      if (criada) {
        if (grupo.anterior && grupo.anterior.formId === form.getId()) {
          ligarDificuldade_(form, grupo.anterior.itemId, form.getItemById(criada.pagina).asPageBreakItem());
        }
        grupo.anterior = { formId: form.getId(), itemId: criada.dificuldade };
        grupo.proxima += 1;
        vazio = false;
        salvar();
        continue;
      }
      if (vazio) {
        throw new Error('Um formulário novo não comportou nem uma questão: limite de itens inesperado.');
      }
      Logger.log('"%s" atingiu o limite de itens na questão %s. Criando uma nova parte.', grupo.titulo, q.codigo);
      grupo.inicioParte = grupo.proxima;
      grupo.anterior = null;
      form = novoFormulario_(grupo, salvar);
      vazio = true;
    }
    estado.atual += 1;
    salvar();
  }
  Logger.log('Concluído: %s questões.', QUESTOES.length);
  listarLinks();
}

function listarLinks() {
  const estado = JSON.parse(PropertiesService.getScriptProperties().getProperty('ESTADO') || 'null');
  if (!estado || estado.versao !== 4) {
    Logger.log('Nenhum formulário criado ainda. Execute criarFormulario.');
    return;
  }
  estado.grupos.forEach(function (g) {
    g.formIds.forEach(function (id, i) {
      const form = FormApp.openById(id);
      Logger.log('%s%s\n  Para o especialista: %s\n  Para editar: %s',
                 g.titulo, g.formIds.length > 1 ? ' (parte ' + (i + 1) + ')' : '',
                 form.getPublishedUrl(), form.getEditUrl());
    });
    Logger.log('  Questões criadas: %s de %s', g.proxima, g.questoes.length);
  });
}

function recomecar() {
  PropertiesService.getScriptProperties().deleteProperty('ESTADO');
  Logger.log('Estado apagado. Os formulários já criados continuam no seu Google Drive; apague-os se não forem usar.');
}

function montarGrupos_() {
  const novo = function (titulo) {
    return { titulo: titulo, questoes: [], proxima: 0, formIds: [], inicioParte: 0, anterior: null };
  };
  if (!CONFIG.umFormularioPorTopico) {
    const g = novo(CONFIG.titulo);
    QUESTOES.forEach(function (_, i) { g.questoes.push(i); });
    return [g];
  }
  const grupos = [];
  const porTopico = {};
  QUESTOES.forEach(function (q, i) {
    if (!(q.topico in porTopico)) {
      porTopico[q.topico] = grupos.length;
      grupos.push(novo(CONFIG.titulo + ': ' + q.topico));
    }
    grupos[porTopico[q.topico]].questoes.push(i);
  });
  return grupos;
}

function novoFormulario_(grupo, salvar) {
  const parte = grupo.formIds.length + 1;
  const titulo = grupo.titulo + (parte > 1 ? ' (parte ' + parte + ')' : '');
  const form = FormApp.create(titulo);
  grupo.formIds.push(form.getId());
  salvar();  // guarda o id antes de qualquer outra chamada
  form.setDescription(
    'Obrigado por colaborar. Cada página traz uma questão gerada automaticamente sobre operação de FPSOs, ' +
    'com a resposta considerada correta. Dê notas de 1 (muito ruim) a 5 (excelente) aos quatro critérios, ' +
    'avalie o contexto usado para gerar a questão, dê o parecer sobre a questão e diga se concorda ' +
    'com a nossa classificação de dificuldade.\n\n' +
    'Sua tarefa é apenas avaliar: não é preciso reescrever nem corrigir as questões. ' +
    'Quando marcar "Rejeitado" ou "Aprovado com ressalvas", escreva o motivo no campo logo abaixo.' +
    (CONFIG.permitirEditarResposta ? '\n\nDepois de enviar, você poderá editar suas respostas pelo link de edição.' : ''));
  form.setProgressBar(true);
  form.setCollectEmail(false);
  form.setAllowResponseEdits(CONFIG.permitirEditarResposta);
  form.setShuffleQuestions(false);
  form.addTextItem().setTitle('Nome completo').setRequired(true);
  const email = form.addTextItem().setTitle('E-mail').setRequired(true);
  email.setValidation(FormApp.createTextValidation().requireTextIsEmail()
    .setHelpText('Informe um e-mail válido.').build());
  if (CONFIG.criarPlanilhaDeRespostas) {
    const planilha = SpreadsheetApp.create(titulo + ' (respostas)');
    form.setDestination(FormApp.DestinationType.SPREADSHEET, planilha.getId());
  }
  return form;
}

/**
 * Cria a página da questão e a página condicional de discordância da dificuldade.
 * Devolve {pagina, dificuldade} (ids) ou null, sem deixar itens soltos, se o formulário atingiu o limite.
 * "Concordo" leva à próxima questão (ligado quando ela é criada; na última, envia o formulário);
 * "Discordo" abre a página em que o especialista dá a classificação dele e marca os motivos.
 */
function adicionarQuestao_(form, q, n, total) {
  const criados = [];
  const add = function (item) { criados.push(item); return item; };
  const c = q.codigo;
  try {
    const pagina = add(form.addPageBreakItem())
      .setTitle(c + ' · Questão ' + n + ' de ' + total)
      .setHelpText('Tópico: ' + q.topico + '\nSubtópico: ' + q.subtopico);
    add(form.addSectionHeaderItem()).setTitle('Enunciado').setHelpText(q.pergunta);
    add(form.addSectionHeaderItem()).setTitle('Resposta correta').setHelpText(q.resposta);
    if (q.pontos_essenciais && q.pontos_essenciais.length) {
      add(form.addSectionHeaderItem()).setTitle('Critério de correção (o que uma resposta precisa conter)')
        .setHelpText(q.pontos_essenciais.map(function (p) { return '• ' + p; }).join('\n'));
    }
    if (q.explicacao) {
      add(form.addSectionHeaderItem()).setTitle('Justificativa da resposta').setHelpText(q.explicacao);
    }
    add(form.addGridItem())
      .setTitle(c + ' · Notas da questão')
      .setHelpText('De 1 (muito ruim) a 5 (excelente), uma nota por linha.')
      .setRows(CRITERIOS)
      .setColumns(NOTAS)
      .setRequired(true);
    add(form.addSectionHeaderItem())
      .setTitle('Contexto usado para gerar a questão')
      .setHelpText(q.contexto);
    add(form.addMultipleChoiceItem())
      .setTitle(c + ' · Parecer sobre o contexto')
      .setHelpText('O material é tecnicamente correto e adequado para sustentar esta questão?')
      .setChoiceValues(PARECERES)
      .setRequired(true);
    add(form.addParagraphTextItem())
      .setTitle(c + ' · Motivo (contexto)')
      .setHelpText('Obrigatório se marcou "Rejeitado" ou "Aprovado com ressalvas".');
    add(form.addMultipleChoiceItem())
      .setTitle(c + ' · Parecer final sobre a questão')
      .setChoiceValues(PARECERES)
      .setRequired(true);
    add(form.addParagraphTextItem())
      .setTitle(c + ' · Motivo (questão)')
      .setHelpText('Obrigatório se marcou "Rejeitado" ou "Aprovado com ressalvas".');
    const dif = add(form.addMultipleChoiceItem());
    dif.setTitle(c + ' · Nossa classificação de dificuldade: ' + q.dificuldade.toUpperCase() + '. Você concorda?')
      .setHelpText('Considere um profissional que atua em operação de FPSOs.')
      .setChoices([dif.createChoice(CONCORDO, FormApp.PageNavigationType.SUBMIT),
                   dif.createChoice(DISCORDO, FormApp.PageNavigationType.CONTINUE)])
      .setRequired(true);
    add(form.addPageBreakItem())
      .setTitle(c + ' · Sua classificação de dificuldade')
      .setHelpText('Você discordou da nossa classificação (' + q.dificuldade + ').');
    add(form.addMultipleChoiceItem())
      .setTitle(c + ' · Qual classificação você daria?')
      .setChoiceValues(NIVEIS.filter(function (x) { return x !== q.dificuldade; }))
      .setRequired(true);
    add(form.addCheckboxItem())
      .setTitle(c + ' · Por que essa classificação?')
      .setHelpText('Marque todas as opções que se aplicam. Use "Outro" se nenhuma descrever o motivo.')
      .setChoiceValues(MOTIVOS_DIFICULDADE)
      .showOtherOption(true)
      .setRequired(true);
    return { pagina: pagina.getId(), dificuldade: dif.getId() };
  } catch (e) {
    criados.reverse().forEach(function (item) {
      try { form.deleteItem(item); } catch (ignorado) { /* item já inexistente */ }
    });
    if (/m[áa]ximo de itens|maximum number of items|too many items/i.test(String(e && e.message || e))) {
      return null;
    }
    throw e;
  }
}

/** "Concordo" na questão anterior passa a levar à página da questão recém-criada. */
function ligarDificuldade_(form, itemId, proximaPagina) {
  const mc = form.getItemById(itemId).asMultipleChoiceItem();
  mc.setChoices([mc.createChoice(CONCORDO, proximaPagina),
                 mc.createChoice(DISCORDO, FormApp.PageNavigationType.CONTINUE)]);
}
