<tema>
Área: Gestão do Desempenho Empresarial (KPI)
Tema: Gestão do Desempenho Empresarial (KPI)
</tema>

<escopo_orientador>
As questões podem abordar aspectos de gestão e desempenho empresarial (KPI) de FPSOs, incluindo planejamento e controle operacional, gestão de indicadores e metas, eficiência e disponibilidade dos sistemas, confiabilidade dos ativos, gestão de riscos, custos, perdas de produção, desempenho das equipes e processos de melhoria contínua ao longo do ciclo de vida da unidade.
</escopo_orientador>

<conhecimentos_cobertos>
- Aproximação da disponibilidade em sistemas reparáveis quando não há série direta de uptime e downtime. (resposta: MTBF dividido por MTBF mais MTTR)
- Diferença entre MTTR e mantenabilidade ao avaliar cumprimento de prazo de restabelecimento. (resposta: Mantenabilidade)
- Seleção do nível de modelagem RAM conforme a maturidade do projeto e o objetivo da análise. (resposta: Diagrama de blocos de confiabilidade simplificado.)
- Falha de autodiagnóstico sem contingência tempestiva pode evoluir de indisponibilidade técnica para interdição formal da operação. (resposta: Interdição da instalação.)
- Em perturbações curtas, o inventário intermediário é o recurso que sustenta a operação por mais tempo antes de cortar carga. (resposta: Inventário intermediário)
- Usar o histórico para extrair mecanismo de processo da falha na revisão de cenários, em vez de transferir a criticidade observada. (resposta: Mecanismo de processo da falha.)
- Na aceitação de operação degradada, recursos externos de restauração tornam o suporte de manutenção decisivo para disponibilidade e custo. (resposta: Suporte de manutenção.)
</conhecimentos_cobertos>

<questoes_deste_foco>
- [reprovada (atalho: A resposta decorre de um princípio geral de normalização de KPI: para comparar eficiência entre meses com cargas diferentes, usa-se consumo de energia por unidade de gás comprimido, exatamente a lógica afirmada nos blocos.)] A potência elétrica do sistema de compressão aumentou junto com a vazão processada, e a comparação entre meses precisa refletir eficiência, não apenas carga. Qual KPI deve ser adotado? → Consumo específico de energia por unidade de gás comprimido.
- [reprovada (atalho: O ponto decisivo é a finalidade do KPI: para diagnosticar perda real de desempenho, ele deve ser referenciado ao desempenho esperado/teórico do processo, não a metas de campanha ou cronograma.)] Mantida a carga de um trocador, a equipe quer saber se houve perda real de desempenho térmico por incrustação, e não apenas se a campanha cumpriu o plano mensal. Com que referência o KPI deve comparar o resultado real? → Referência teórica do processo.
- [reprovada (atalho: A resposta é conhecimento corrente de processo e está diretamente sustentada no bloco A1, mas o enunciado praticamente já descreve um transiente e sua reversão ao estabilizar, tornando a solução um reempacotamento dos próprios termos da pergunta.)] O KPI de separação cai nas partidas, nas mudanças de carga e após perturbações de alimentação, mas retorna ao patamar anterior quando o processo estabiliza. Qual condição primária explica esse comportamento? → Regime transiente.
- [reprovada (atalho: A escolha do nível do KPI é conhecimento geral de monitoramento e, aqui, o próprio enunciado já indica que o agregado da etapa mascara a perda do compressor, enquanto os blocos sustentam que o KPI deve ser definido conforme a finalidade da decisão e pode ser aplicado ao equipamento.)] Falhas de partida e aumento de potência ocorrem só em um compressor crítico, enquanto a etapa mantém a produção por compensação dos paralelos. Para acompanhar a perda real sem mascaramento, em que escopo o KPI deve ser aplicado? → No equipamento.
</questoes_deste_foco>

<boas_ja_avaliadas>
[consequencia] Pergunta: Depois de uma modificação, a mistura passou a sofrer mais agitação entre vasos e a emulsão primária ficou mais persistente, sem perda de volume útil nem mudança na composição da entrada. Que característica da água dispersa mudou no sentido de dificultar a separação?
Resposta: Menor diâmetro médio das gotas de água
Resposta padrão (errada aqui): Menor tempo de residência do separador.
Por que não: Sem perda de volume útil, a piora descrita vem da quebra de gotas por cisalhamento, não de menor retenção.

[decisao] Pergunta: Há muitos risers, e um bordo precisa permanecer livre para transferência de carga. Qual configuração de ancoragem acomoda melhor esse arranjo?
Resposta: Spread mooring.
Resposta padrão (errada aqui): Turret mooring.
Por que não: No turret, linhas e risers convergem ao mesmo ponto; isso não cria um bordo dedicado e livre para a transferência.

[mecanismo] Pergunta: O tratamento microbiológico funciona antes da injeção, porém perde efeito quando se busca atuar no interior da formação. Qual limitação do meio explica essa perda de desempenho?
Resposta: Inativação rápida do biocida no reservatório.
Resposta padrão (errada aqui): Diluição no volume poroso da formação.
Por que não: A limitação destacada não é só dispersão espacial; é perda química de atividade no meio do reservatório.

[decisao] Pergunta: O gás chega ao demister com grande carga líquida e perfil desuniforme, e o carryover persiste mesmo com o elemento limpo. Qual parte do separador deve ser corrigida antes de redimensionar o próprio demister?
Resposta: O sistema de distribuição de entrada.
Resposta padrão (errada aqui): Aumentar a área do demister.
Por que não: Sem boa distribuição de entrada, a sobrecarga hidrodinâmica continua e o dispositivo pode inundar ou re-entrainar líquido.

[decisao] Pergunta: Bloqueio a jusante elevou a pressão do separador. A alimentação foi isolada pela ESDV, mas o vaso permaneceu pressurizado com inventário interno. Que dispositivo deve limitar a pressão nessa condição?
Resposta: PSV do separador.
Resposta padrão (errada aqui): A ESDV de entrada.
Por que não: Isolamento corta a comunicação com a fonte, mas não reduz por si só a pressão do volume retido.

[mecanismo] Pergunta: Elevou-se a pressão do primeiro estágio; a vazão de gás do vaso caiu e a carga líquida a jusante subiu, sem mudança na alimentação. Que mecanismo específico explica esse desvio?
Resposta: Menor liberação de gás por flash.
Resposta padrão (errada aqui): Maior arraste mecânico de óleo para o gás.
Por que não: O sinal dominante é queda de gás produzido com aumento da carga líquida, típico de mudança de equilíbrio, não de carryover para o gás.

[procedimento] Pergunta: Com rotação mantida, a temperatura de sucção e a composição do gás mudam após perturbação a montante. Que referência da máquina deve ser reavaliada para julgar a proximidade dos limites aerodinâmicos?
Resposta: Ponto de operação do compressor.
Resposta padrão (errada aqui): Curva característica do compressor.
Por que não: A curva é característica da máquina; quem se desloca com a condição de processo é o ponto de operação sobre ela.

[decisao] Pergunta: Com alimentação estável e limitação severa de porte, deseja-se antecipar a coalescência no tratador convencional. Em relação aos eletrodos, onde a alimentação deve entrar?
Resposta: Diretamente na região entre os eletrodos.
Resposta padrão (errada aqui): Abaixo da região de eletrodos, próxima à interface.
Por que não: Essa disposição caracteriza o arranjo de baixa velocidade, mais robusto a variações, não o de menor porte.

[decisao] Pergunta: Com campo elétrico, química e temperatura estáveis, o aumento de vazão fez a água voltar a sair mais dispersa na seção ativa do tratador. Qual variável local deve ser reduzida para recuperar a coalescência?
Resposta: Cisalhamento local do escoamento.
Resposta padrão (errada aqui): Tempo de residência global do vaso.
Por que não: Se o contato ocorre sob cisalhamento excessivo, mais residência não corrige a causa que está frustrando a união entre gotas.

[procedimento] Pergunta: Na partida, o header e a chaminé ficaram expostos à atmosfera durante manutenção e os pilotos ainda estão apagados. Que etapa deve ser concluída antes do acendimento para que o conteúdo gasoso até a ponta não permaneça na faixa inflamável?
Resposta: Purga completa do header, riser e chaminé.
Resposta padrão (errada aqui): Acender os pilotos primeiro para estabilizar a ponta e depois purgar.
Por que não: Piloto aceso na presença de ar remanescente pode inflamar mistura dentro do sistema; primeiro é preciso remover o ar.
</boas_ja_avaliadas>

<ruins_ja_avaliadas>
[procedimento] Pergunta: Tanques de óleo recebem produção estabilizada e, em certas condições, também condensado do processamento de gás. Antes de fechar a custódia de um offloading, que delimitação material precisa estar definida no balanço?
Resposta: As correntes do estoque transferível e sua condição operacional de entrada.
Defeito: atalho: A exigência é conhecimento geral de custódia em FPSO e está afirmada explicitamente em A2, embora o próprio enunciado já conduza quase diretamente à ideia de delimitar quais correntes compõem o estoque transferível.

[mecanismo] Pergunta: Sob vibração contínua e meio corrosivo, a taxa observada de crescimento de trincas em um suporte soldado supera a prevista por curvas de fadiga em ar. Que mecanismo deve governar a avaliação de vida remanescente?
Resposta: Corrosão-fadiga.
Defeito: atalho: A combinação de carregamento cíclico/vibração com meio agressivo e crescimento de trinca acima da fadiga em ar aponta para corrosão-fadiga, e o bloco [F] sustenta exatamente que o meio agressivo reduz a iniciação e o crescimento de trincas em componentes sob ciclos.

[diagnostico] Pergunta: Num simulado com incêndio, dois supervisores emitem ordens conflitantes, embora o plano traga funções genéricas e pontos de encontro. Que definição faltou no arranjo de resposta?
Resposta: Composição do Incident Command Team (ICT).
Defeito: atalho: O ponto decisivo está explicitado no bloco A2 e, embora um profissional experiente possa responder sem o documento, a inferência também sai quase diretamente do enunciado como necessidade de cadeia de comando/ICT definido.

[decisao] Pergunta: Ao usar um limite ocupacional estrangeiro em uma instalação brasileira, que elemento deve ser confirmado antes de tratá-lo como exigência legal de conformidade?
Resposta: Previsão em instrumento legal brasileiro aplicável
Defeito: atalho: O ponto decisivo é que um valor estrangeiro só vira exigência legal no Brasil se houver previsão em instrumento legal nacional aplicável, algo explicitado nos blocos e também inferível pelo próprio enunciado.

[decisao] Pergunta: Qual foco técnico deve puxar a prioridade das auditorias, se os incidentes leves seguem estáveis, mas há descomissionamento, equipe reduzida e controle irregular de inspeção e manutenção?
Resposta: Condições com potencial de falha de barreiras.
Defeito: atalho: A resposta é conhecimento de ofício em segurança de processo e está diretamente sustentada pelos blocos, mas o enunciado já conduz por um princípio genérico de priorização por risco real das barreiras, e não por contagem estável de incidentes leves.

[procedimento] Pergunta: Linha temporária montada, desenho revisado e várias válvulas manuais entram no alinhamento. Como confirmar antes da manobra que a configuração real ainda coincide com a referência emitida?
Resposta: Walkdown de campo dos alinhamentos e isolamentos.
Defeito: atalho: A resposta é prática operacional padrão para arranjos temporários e está sustentada pelos blocos que exigem documentação fidedigna e verificação dos isolamentos, embora também decorra quase diretamente do próprio enunciado por prudência operacional.

[procedimento] Pergunta: Mudanças de salinidade e pH entre campanhas fizeram um produto escolhido em água sintética perder desempenho no processo. Como os candidatos devem ser comparados na triagem para que o resultado seja transferível à operação?
Resposta: Em bottle tests com petróleo e salmoura representativos, no pH e salinidade reais.
Defeito: atalho: O ponto decisivo é a comparação dos produtos em condições representativas da operação real, uma prática geral da área e explicitamente afirmada no bloco F.

[decisao] Pergunta: Em um FPSO, após falhas repetidas de aparelho respiratório em serviço, os envolvidos não apresentam quadro clínico definido, mas a ocorrência expôs a equipe a risco de acidente maior. Na gestão de saúde ocupacional, que encaminhamento investigativo inicial é indicado?
Resposta: Triagem investigativa, com consulta a especialistas de saúde ocupacional.
Defeito: Decisão genérica: 'investigar, consultar especialistas' serve para qualquer problema e admite várias respostas.
</ruins_ja_avaliadas>

<exemplos_de_forma>
Pergunta: Na reunião semanal de PCM de um FPSO, qual variável do painel tático mostra que há acúmulo de ordens preventivas não absorvidas pela execução planejada?
Resposta: Carteira vencida.

Pergunta: O que acontece com a força da atração gravitacional entre dois objetos pequenos, se a massa de cada objeto for dobrada e a distância entre seus centros também for dobrada?
Resposta: Permanece a mesma.

Pergunta: Sam was listing the differences between a euglena and a paramecium. Which characteristic should not be on Sam's list?
Resposta: only the euglena have a definite shape

Pergunta: Após o comissionamento de uma URS por membranas, há aumento da tendência de incrustação no circuito da corrente de rejeito, associado à química do concentrado gerado pela dessulfatação. Ao aplicar inibidor de incrustação nesse caso, em qual variável a dosagem deve ser baseada?
Resposta: Potencial de precipitação no concentrado, com dosagem integrada ao controle operacional da URS.

Pergunta: What happens to vomitus so that toxic materials are removed from the stomach before they are absorbed?
Resposta: expelled

Pergunta: Por que o complexo sistema da atmosfera e das correntes oceânicas é crucial para a distribuição da vida no oceano?
Resposta: Porque regula a temperatura, a salinidade, o teor de oxigênio, a absorção do dióxido de carbono e a penetração da luz e a distribuição dos nutrientes.

Pergunta: O que é um nop sled?
Resposta: É uma sequência de nops precedendo shellcode injetado, útil quando o endereço de retorno é desconhecido

Pergunta: Qual é a faixa de profundidade do campo de Albacora, localizado na bacia de Campos?
Resposta: Profundidades subaquáticas que variam de 230m a 1.900m.
</exemplos_de_forma>

<janela>
[A1] Indicadores e metas / Indicadores de monitoramento operacional: detecção de desvios e diagnóstico
Em unidades de processo, indicadores de desempenho podem ser parte de uma metodologia de monitoramento mais ampla, voltada a detectar desvios, identificar variáveis perturbadas e apoiar o diagnóstico de causas prováveis. Essa lógica é útil para topsides de FPSO porque a operação depende da interação entre separação, tratamento de óleo, água, gás, utilidades e sistemas de controle. O indicador não substitui a variável de processo, mas resume seu efeito sobre desempenho. Ferramentas online tornam-se valiosas quando o processo opera sob especificações mais restritas e exigência maior de segurança, pois permitem avaliar condições operacionais em tempo próximo do real. Seus objetivos podem incluir manter produtos dentro de especificação, detectar períodos de operação anormal, antecipar anormalidades e fornecer referência para otimização. O comportamento do indicador muda com regime transiente, mudanças de carga, perturbações de alimentação, degradação de equipamento e alterações de estratégia de controle. Por isso, o uso operacional correto combina KPI com contexto do processo, histórico recente e conhecimento acumulado da operação. Sem essa integração, há risco de tratar sintoma como causa ou interpretar uma variação transitória como perda estrutural de desempenho.

[F] Indicadores e metas / O que são KPIs e como a finalidade muda sua definição
Indicadores-chave de desempenho, ou KPIs (Key Performance Indicators), são métricas usadas para avaliar a eficiência e o desempenho de processos industriais. Eles podem comparar resultados reais com referências teóricas e também expressar conformidade de cronograma, tempo de ciclo, consumo de energia e matérias-primas, além de aspectos de controle, operação e manutenção. A forma de expressão depende do interesse da avaliação e do usuário do indicador. Por isso, o mesmo processo pode ser acompanhado por indicadores diferentes quando a finalidade muda entre operação em tempo real, acompanhamento gerencial ou análise de melhoria. Em plantas de produção, os KPIs podem ser aplicados a equipamentos, a etapas específicas do processo ou à instalação como um todo. Seu uso busca identificar deficiências de desempenho e apoiar ações que reduzam custos ou elevem capacidade sem grandes investimentos, sem garantir esses ganhos em qualquer condição operacional. Em aplicações mais atuais, os indicadores podem ser exibidos em painéis de controle em tempo real, o que favorece acompanhamento rápido, desde que a definição da métrica permaneça coerente com a decisão que ela deve sustentar.

[A2] Indicadores e metas / Denominador, base de exposição e comparabilidade
O denominador define o que o indicador realmente compara. Em segurança ocupacional, isso aparece de forma explícita nas taxas de frequência de acidentes sem afastamento e com afastamento, calculadas em relação às horas-homem de exposição ao risco. Nessa estrutura, o numerador representa a quantidade de casos enquadrados pela definição adotada, enquanto o denominador representa a base de exposição no período. Esse arranjo permite comparação temporal mais consistente do que uma contagem bruta de acidentes, desde que o período, o critério de enquadramento e a base de horas-homem sejam mantidos de forma compatível. O mesmo princípio de normalização também aparece em indicadores intensivos de energia, materiais e impacto ambiental por unidade produzida. Sem uma base de referência adequada, uma variação no valor absoluto pode refletir apenas mudança de carga, de volume processado ou de população exposta, e não alteração real do desempenho intrínseco. Por isso, a escolha do denominador deve acompanhar o mecanismo que se deseja observar: exposição ao risco, produção entregue, consumo por unidade ou outra base tecnicamente coerente com a pergunta de gestão.
</janela>

Pedido: 01_01:001:v2
