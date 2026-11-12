<tema>
Área: Gestão do Desempenho Empresarial (KPI)
Tema: Gestão do Desempenho Empresarial (KPI)
</tema>

<escopo_orientador>
As questões podem abordar aspectos de gestão e desempenho empresarial (KPI) de FPSOs, incluindo planejamento e controle operacional, gestão de indicadores e metas, eficiência e disponibilidade dos sistemas, confiabilidade dos ativos, gestão de riscos, custos, perdas de produção, desempenho das equipes e processos de melhoria contínua ao longo do ciclo de vida da unidade.
</escopo_orientador>

<defeitos_frequentes>
Nenhuma questão julgada ainda.
</defeitos_frequentes>

<boas_ja_avaliadas>
[consequencia] Pergunta: Num equipamento de processo, mantidos o modo de falha e a probabilidade estimada, foram adicionados alarmes, intertravamentos, contenção secundária e capacidade de isolamento. Que efeito isso produz na consequência considerada no plano de inspeção?
Resposta: Reduz a classe de consequência da falha.
Resposta padrão (errada aqui): Reduz a probabilidade de falha.
Por que não: Alarmes, contenção e isolamento não evitam a falha, limitam o impacto; na inspeção baseada em risco, mudam a consequência, não a probabilidade.

[diagnostico] Pergunta: Dois petróleos entram no mesmo tratador com teor semelhante de água emulsificada. O mais pesado exige mais aquecimento e ainda desidrata pior. Que combinação de propriedades físicas torna a separação óleo-água mais difícil nesse caso?
Resposta: Maior viscosidade do óleo e menor diferença de densidade entre óleo e água.
Resposta padrão (errada aqui): Maior teor de asfaltenos estabilizando a emulsão.
Por que não: Asfaltenos agem no filme interfacial; a pergunta pede propriedades físicas, e a velocidade de decantação cai com viscosidade alta e pouca diferença de densidade.

[procedimento] Pergunta: Durante o stripping de um tanque remanescente, será aplicado trim para recuperar a sucção. Como deve ser verificado o impacto dessa manobra no nível da unidade antes e durante a operação?
Resposta: No loading computer, conferindo estabilidade e esforços longitudinais do casco.
Resposta padrão (errada aqui): Acompanhando calados e inclinação durante a manobra.
Por que não: Calado e inclinação mostram o resultado depois; esforço cortante e momento fletor da nova distribuição de peso só o cálculo de carregamento mostra antes.

[decisao] Pergunta: Em um sistema dividido em dois semibarramentos com possibilidade de interligação por bus tie, qual filosofia normal de operação tende a limitar a propagação de faltas e o impacto de manutenção?
Resposta: Operação seccionada, com o bus tie aberto.
Resposta padrão (errada aqui): Semibarramentos interligados para dividir a carga.
Por que não: Com o bus tie fechado, uma falta num semibarramento atinge os dois; aberto, cada metade fica isolada e pode ser mantida sem desligar a outra.

[procedimento] Pergunta: Num FPSO com acesso ao I-tube apenas por janelas de inspeção, como se confirma visualmente um vazamento no anular?
Resposta: Por boroscopia com injeção de nitrogênio no anular, observando bolhas.
Resposta padrão (errada aqui): Por teste de pressão (estanqueidade) do anular.
Por que não: O teste de pressão indica que há vazamento, mas não o localiza; com acesso só por janelas, a confirmação visual exige boroscópio e gás para formar bolhas no ponto.

[consequencia] Pergunta: Num proof test fracionado por subsistemas, um cenário de shutdown com válvula pneumática on/off foi dado como coberto após o teste da matriz de causa e efeito do SIS. Qual efeito final da função ainda pode permanecer sem prova?
Resposta: O deslocamento real do obturador da válvula.
Resposta padrão (errada aqui): O tempo de resposta da lógica do SIS.
Por que não: O teste da matriz exercita entradas, lógica e saídas; a cadeia física solenoide-atuador-obturador só é provada vendo a válvula se mover.

[procedimento] Pergunta: Como a solução amínica rica é tipicamente regenerada em uma unidade de adoçamento?
Resposta: Redução de pressão seguida de stripping com vapor no regenerador.
Resposta padrão (errada aqui): Aquecimento da amina em trocador de calor.
Por que não: Só aquecer não remove os gases ácidos absorvidos; a regeneração usa flash por redução de pressão e esgotamento com vapor gerado no refervedor.

[consequencia] Pergunta: Em um tanque fechado de água produzida, o tempo de residência da água passa a ser muito maior que o habitual. Que alteração tende a se tornar mais provável no espaço de vapor?
Resposta: Aparecimento de H2S por atividade de bactérias redutoras de sulfato.
Resposta padrão (errada aqui): Acúmulo de vapor d'água e de voláteis.
Por que não: A volatilização se equilibra rapidamente; o que cresce com a residência em ambiente fechado é a atividade das BRS, que convertem sulfato em H2S.

[diagnostico] Pergunta: No stripping final de um tanque, a bomba opera estável e há vazão na descarga, mas o nível do tanque de origem quase não baixa. Qual causa hidráulica explica melhor esse esvaziamento ineficaz?
Resposta: Retorno ao tanque por válvula passando ou comunicação indevida.
Resposta padrão (errada aqui): Entrada de ar ou vórtice na sucção.
Por que não: Ar e vórtice derrubam e instabilizam a vazão; com a bomba estável entregando vazão, o líquido está voltando por outro caminho.

[procedimento] Pergunta: Uma válvula prevista para modular aparece normal na IHM, com comando e status coerentes. Antes da partida, como comprovar em campo que a função de controle está realmente disponível, e não apenas a interface?
Resposta: Teste de curso em campo comparando o comando com a posição atingida.
Resposta padrão (errada aqui): Conferir o sinal de posição (feedback) na IHM.
Por que não: O feedback na tela faz parte do que precisa ser provado; só a observação da haste em campo, para vários comandos, mostra que a válvula responde.
</boas_ja_avaliadas>

<ruins_ja_avaliadas>
[decisao] Pergunta: Em um FPSO, a água produzida sai com mais óleo e o óleo tratado com mais água justamente nos períodos de maior balanço da unidade, sem descontrole persistente de nível. Para reduzir essa perda de qualidade, com qual tecnologia de separação a modificação deve ser feita?
Resposta: Tecnologia ciclônica (hidrociclones).
Defeito: Várias respostas: internos que amortecem o movimento ou outros separadores compactos também resolvem, e o enunciado não os exclui.

[procedimento] Pergunta: Como deve ser validada uma redução de reciclo obtida por novo ajuste da linha de controle da segunda seção?
Resposta: Revalidando a proteção dinâmica em todo o envelope operacional.
Defeito: Procedimento vago: não nomeia método, ponto de medição nem critério; qualquer 'revalidar' seria aceito.

[mecanismo] Pergunta: No modelo fenomenológico de reinjeção, por que a concentração de partículas suspensas sozinha não determina quanto material ficará retido no meio poroso?
Resposta: Cinética de retenção dependente da concentração já retida e do coeficiente de filtração.
Defeito: Depende do documento: pergunta sobre um modelo próprio do texto, que um profissional não conhece por esse nome.

[conceito] Pergunta: De que depende a conversão da densidade observada de um petróleo para a densidade de referência?
Resposta: Temperatura observada, densidade do produto e fator de correção tabelado aplicável.
Defeito: Gabarito em lista: cobra itens enumerados pelo texto, e o acerto vira parcial conforme quantos itens o respondente lembra.

[decisao] Pergunta: Em um FPSO, após falhas repetidas de aparelho respiratório em serviço, os envolvidos não apresentam quadro clínico definido, mas a ocorrência expôs a equipe a risco de acidente maior. Na gestão de saúde ocupacional, que encaminhamento investigativo inicial é indicado?
Resposta: Triagem investigativa, com consulta a especialistas de saúde ocupacional.
Defeito: Decisão genérica: 'investigar, consultar especialistas' serve para qualquer problema e admite várias respostas.
</ruins_ja_avaliadas>

<exemplos_de_forma>
Pergunta: O que a PETROBRAS fez para transportar o gás de forma mais ecológica?
Resposta: A PETROBRAS pesquisou a tecnologia de gás em líquido (GTL), que converte o gás natural em óleo cru sintético que pode ser misturado ao óleo produzido para armazenamento e escoamento.

Pergunta: What is the primary source of energy that causes evaporation of water from the surface of bodies of water?
Resposta: solar radiation

Pergunta: No cenário em que um único núcleo onshore concentra requisições, compras e programações do FPSO, gerando fila decisória, resposta lenta às necessidades locais e uso inconsistente das informações, quais três elementos devem estar juntos no redesenho alinhado a suprimentos integrados?
Resposta: Autonomia operacional de áreas-chave, processos padronizados e sistema integrado entre produção, compras e almoxarifado.

Pergunta: Em suportes metálicos de convés externo expostos à névoa salina, mesmo quando chuvas frequentes removem parte dos sais e resíduos, quais dois fatores condicionam o risco final de corrosão?
Resposta: Tempo de permanência do filme úmido e contaminação remanescente na superfície.

Pergunta: Qual é o princípio orientador da gestão científica?
Resposta: Uma melhor maneira de fazer um trabalho

Pergunta: No que reservatórios com uma permeabilidade muito elevada podem resultar?
Resposta: Taxas extraordinárias de produção de petróleo

Pergunta: What must a chemical reaction overcome before starting?
Resposta: energy barrier

Pergunta: O que é um plano de sucessão?
Resposta: Um processo formal de planejamento para preencher um cargo que ser tornará vago
</exemplos_de_forma>

<janela>
[A1] Indicadores e metas / Indicadores de monitoramento operacional: detecção de desvios e diagnóstico
Em unidades de processo, indicadores de desempenho podem ser parte de uma metodologia de monitoramento mais ampla, voltada a detectar desvios, identificar variáveis perturbadas e apoiar o diagnóstico de causas prováveis. Essa lógica é útil para topsides de FPSO porque a operação depende da interação entre separação, tratamento de óleo, água, gás, utilidades e sistemas de controle. O indicador não substitui a variável de processo, mas resume seu efeito sobre desempenho. Ferramentas online tornam-se valiosas quando o processo opera sob especificações mais restritas e exigência maior de segurança, pois permitem avaliar condições operacionais em tempo próximo do real. Seus objetivos podem incluir manter produtos dentro de especificação, detectar períodos de operação anormal, antecipar anormalidades e fornecer referência para otimização. O comportamento do indicador muda com regime transiente, mudanças de carga, perturbações de alimentação, degradação de equipamento e alterações de estratégia de controle. Por isso, o uso operacional correto combina KPI com contexto do processo, histórico recente e conhecimento acumulado da operação. Sem essa integração, há risco de tratar sintoma como causa ou interpretar uma variação transitória como perda estrutural de desempenho.

[F] Indicadores e metas / O que são KPIs e como a finalidade muda sua definição
Indicadores-chave de desempenho, ou KPIs (Key Performance Indicators), são métricas usadas para avaliar a eficiência e o desempenho de processos industriais. Eles podem comparar resultados reais com referências teóricas e também expressar conformidade de cronograma, tempo de ciclo, consumo de energia e matérias-primas, além de aspectos de controle, operação e manutenção. A forma de expressão depende do interesse da avaliação e do usuário do indicador. Por isso, o mesmo processo pode ser acompanhado por indicadores diferentes quando a finalidade muda entre operação em tempo real, acompanhamento gerencial ou análise de melhoria. Em plantas de produção, os KPIs podem ser aplicados a equipamentos, a etapas específicas do processo ou à instalação como um todo. Seu uso busca identificar deficiências de desempenho e apoiar ações que reduzam custos ou elevem capacidade sem grandes investimentos, sem garantir esses ganhos em qualquer condição operacional. Em aplicações mais atuais, os indicadores podem ser exibidos em painéis de controle em tempo real, o que favorece acompanhamento rápido, desde que a definição da métrica permaneça coerente com a decisão que ela deve sustentar.

[A2] Indicadores e metas / Denominador, base de exposição e comparabilidade
O denominador define o que o indicador realmente compara. Em segurança ocupacional, isso aparece de forma explícita nas taxas de frequência de acidentes sem afastamento e com afastamento, calculadas em relação às horas-homem de exposição ao risco. Nessa estrutura, o numerador representa a quantidade de casos enquadrados pela definição adotada, enquanto o denominador representa a base de exposição no período. Esse arranjo permite comparação temporal mais consistente do que uma contagem bruta de acidentes, desde que o período, o critério de enquadramento e a base de horas-homem sejam mantidos de forma compatível. O mesmo princípio de normalização também aparece em indicadores intensivos de energia, materiais e impacto ambiental por unidade produzida. Sem uma base de referência adequada, uma variação no valor absoluto pode refletir apenas mudança de carga, de volume processado ou de população exposta, e não alteração real do desempenho intrínseco. Por isso, a escolha do denominador deve acompanhar o mecanismo que se deseja observar: exposição ao risco, produção entregue, consumo por unidade ou outra base tecnicamente coerente com a pergunta de gestão.
</janela>

Pedido: 01_01:001:v1
