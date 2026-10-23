# Geração híbrida por tipo de questão (v15)

Janela: prompt v15 (até 4: 1 conceito, 1 mecanismo ou consequência, 1 diagnóstico, decisão ou procedimento, 1 livre sem conceito), com exemplos e contraexemplos curados por tipo e sem datasets externos. Compostas: uma por encadeamento do inventário. Auditoria como filtro: `gpt-5-4-petrobras:high`.

**Aprovadas pelo filtro: 164** (referência válida e sem atalho) · por origem e documento: {'janela:01_01': '37/96', 'janela:02_02': '87/144', 'composta:01_01': '14/32', 'composta:02_02': '26/32'} · por tipo final: {'conceito': 26, 'procedimento': 16, 'diagnostico': 33, 'mecanismo': 49, 'consequencia': 20, 'decisao': 20}.

Janelas: 60 ({'ok': 60}); fundamentos literais 239; questões que usam bloco de apoio 13. Compostas: {'total': 64, 'ok': 64, 'insuficiente': 0}.

| Origem | Tipo | n | com cenário | palavras (perg./resp.) | tipo confere | ref. inválida | atalho | aprovadas |
|---|---|---|---|---|---|---|---|---|
| janela | conceito | 60 | 0 | 18.8/3.5 | 55/60 | 17 | 28 | 25 |
| janela | mecanismo | 57 | 1 | 19.1/18.5 | 57/57 | 6 | 11 | 43 |
| janela | consequencia | 30 | 10 | 27.6/11.4 | 30/30 | 4 | 16 | 14 |
| janela | diagnostico | 32 | 32 | 50.5/11.1 | 32/32 | 5 | 12 | 19 |
| janela | decisao | 20 | 20 | 37.0/11.2 | 19/20 | 8 | 12 | 5 |
| janela | procedimento | 41 | 13 | 22.4/15.0 | 38/41 | 12 | 19 | 18 |
| janela | **total** | 240 | 76 | 26.3/11.7 | 231/240 | 52 | 98 | 124 |
| composta | mecanismo | 5 | 5 | 62.4/21.8 | 5/5 | 0 | 1 | 4 |
| composta | consequencia | 12 | 12 | 54.9/20.1 | 11/12 | 2 | 5 | 6 |
| composta | diagnostico | 25 | 25 | 60.8/22.7 | 21/25 | 3 | 5 | 18 |
| composta | decisao | 22 | 22 | 60.6/21.4 | 19/22 | 1 | 9 | 12 |
| composta | **total** | 64 | 64 | 59.8/21.7 | 56/64 | 6 | 20 | 40 |

Tipos por documento: {'01_01': {'conceito': 24, 'mecanismo': 22, 'diagnostico': 22, 'consequencia': 21, 'procedimento': 16, 'decisao': 23}, '02_02': {'conceito': 36, 'mecanismo': 40, 'procedimento': 25, 'decisao': 19, 'consequencia': 21, 'diagnostico': 35}}.

Combinações de tipos mais comuns por janela: {'conceito+diagnostico+mecanismo+procedimento': 14, 'conceito+consequencia+diagnostico+mecanismo': 11, 'conceito+decisao+mecanismo+procedimento': 10, 'conceito+consequencia+mecanismo+procedimento': 10, 'conceito+consequencia+decisao+mecanismo': 3, 'conceito+decisao+diagnostico+mecanismo': 3, 'conceito+consequencia+decisao+procedimento': 2, 'conceito+consequencia+diagnostico+procedimento': 2, 'conceito+consequencia+procedimento+procedimento': 1, 'conceito+decisao+mecanismo+mecanismo': 1}.

Tipo declarado → sugerido pelo auditor (divergências): {'procedimento->decisao': 3, 'conceito->decisao': 3, 'decisao->procedimento': 3, 'diagnostico->conceito': 2, 'diagnostico->mecanismo': 2, 'decisao->conceito': 1, 'conceito->procedimento': 1, 'conceito->consequencia': 1, 'consequencia->conceito': 1}.

Pares quase duplicados (Jaccard ≥ 0,6): 0. Falhas pendentes: 0.

## Exemplos por tipo

### composta · consequencia (12)

**c:01_01:C18 · aprovada** Num FPSO, a produção foi mantida em condição desviada após uma alteração temporária no processo. A revisão técnica não saiu porque parâmetros de projeto estavam em arquivo inacessível, o especialista dependia de suporte remoto e não havia definição clara de quem autorizaria a atualização. A salvaguarda crítica permanece citada na análise de risco vigente. Que efeito final isso traz para o risco usado para decidir operar?

- Resposta: O risco real divergiu do risco assumido para operar, porque a barreira seguiu considerada sem validação técnica da mudança.

**c:02_02:C1 · aprovada** Em um FPSO, a água produzida chega à flotação por ar dissolvido com óleo fino disperso; a separação gravitacional a montante quase não reduz o TOG, e aumentar a geração de bolhas, sozinho, não tem enquadrado o descarte. Se a equipe passa a atuar com a química adequada ao mecanismo dominante dessa água, que efeito final específico deve aparecer na flotação?

- Resposta: Captura mais fácil dos agregados por microbolhas, acelerando a subida da fase oleosa na flotação.

**c:02_02:C16 · aprovada** Em um FPSO, após substituir o biocida por um produto com surfactantes, as contagens microbiológicas caíram. No mesmo período, não houve alteração relevante de internos, vazão ou controle do separador, mas a qualidade do gás de saída piorou. Que efeito específico na corrente de gás é mais esperado?

- Resposta: Aumento do arraste de líquido na saída de gás, porque o biocida com surfactantes pode sustentar espuma no vaso e reduzir a eficiência de separação.

**c:02_02:C23 · aprovada** Em um FPSO com recuperação de MEG, a equipe elevou a concentração do glicol para ganhar margem contra hidratos. A água produzida traz sais, e a unidade remove água para reconcentrar o MEG circulante. Nessa condição, que combinação de consequências operacionais tende a aparecer no circuito de recuperação?

- Resposta: Restrição hidráulica e perda de área efetiva de troca térmica, por precipitação de sais durante a reconcentração do MEG.

### composta · decisao (22)

**c:01_01:C13 · aprovada** Num FPSO com aumento de corte de água, as bombas de reinjeção passaram a operar próximas do limite. A linha de tratamento e descarte no mar está operacional e, nessa condição, atende às exigências aplicáveis. Separação primária, óleo e gás não mostram restrição equivalente no momento. Para sustentar a carga da unidade sem violar requisitos, qual ajuste operacional específico deve ser feito com a água produzida?

- Resposta: Desviar maior parcela da água produzida para tratamento e descarte no mar, pois a reinjeção é o gargalo e a outra rota segue admissível.

**c:01_01:C17 · aprovada** Em um FPSO em fase madura, a água produzida cresceu de forma relevante. As maiores médias históricas de downtime continuam em um subsistema de hidrocarbonetos, mas os cortes de carga recentes só aparecem quando o water cut fica alto, enquanto os equipamentos principais de óleo e gás operam dentro do esperado nesses eventos. Para iniciar um debottlenecking que recupere capacidade, onde ele deve começar?

- Resposta: Na malha de água produzida, localizando ali a variável ou equipamento limitante, porque os cortes de carga surgem com water cut alto.

**c:01_01:C20 · aprovada** Em um FPSO, propõe-se reduzir intervenções preventivas para ganhar mais horas operando. A defesa mostra apenas homem-hora, materiais e parada programada evitados, sem avaliação de risco e integridade concluída. Para fechar a conta dessa decisão, que parcela de custo ainda precisa entrar na comparação?

- Resposta: Indisponibilidade, correções emergenciais e restrições operacionais acumuladas, porque custo direto evitado e horas liberadas não capturam o efeito econômico total.

**c:01_01:C24 · aprovada** Num FPSO, dois trens de compressão em paralelo atendem a produção, mas ao elevar a carga de qualquer trem a pressão no coletor comum de descarga sobe até o mesmo limite e o intertravamento recua ambos. Utilidades e acesso de manutenção não são a restrição observada. Mesmo assim, foi proposta a instalação de um terceiro compressor idêntico em paralelo. Que mudança de debottlenecking deve ser priorizada?

- Resposta: Aliviar o sistema comum de descarga/controle, porque outro compressor em paralelo continuaria limitado pelo mesmo ponto compartilhado.

### composta · diagnostico (25)

**c:01_01:C15 · aprovada · auditor: conceito** Num FPSO, um equipamento iniciou a campanha operando e, nas checagens de prontidão e no painel, quase sempre aparece em serviço quando requerido. Mesmo assim, o histórico da campanha registra várias paradas não planejadas, com retorno posterior após intervenção. Entre os atributos de desempenho acompanhados, qual está pior representado por esse comportamento?

- Resposta: Confiabilidade, porque as várias paradas não planejadas mostram incapacidade de manter a função durante a campanha, embora o item costume estar apto nas verificações instantâneas.

**c:01_01:C16 · aprovada · auditor: conceito** Num FPSO, após falha de um compressor, o retorno ao serviço foi muito mais rápido que o usual porque houve reforço extraordinário da equipe, jornada estendida e mobilização imediata de recursos de terra. Não mudaram o projeto do item, seu acesso físico, os sobressalentes embarcados nem os meios permanentes de manutenção. Em termos de KPI, o que esse caso de fato evidenciou?

- Resposta: Desempenho da ação de manutenção, não aumento de mantenabilidade, porque o retorno rápido veio de esforço excepcional sem mudança estrutural no item nem nos meios permanentes.

**c:01_01:C2 · aprovada** Num FPSO, dois trens de compressão operam em paralelo, e o KPI de indisponibilidade mostra mais falhas mecânicas registradas em um compressor. Ainda assim, nas paradas com maior perda de produção, o trem reserva estava disponível e sem falha própria, porém a compressão da planta inteira caiu no mesmo evento e só voltou após restabelecimento fora dos compressores. Que causa técnica mais provavelmente está mascarando o ganho esperado da redundância?

- Resposta: Gargalo compartilhado de utilidades, controle ou descarga entre os trens, porque sua indisponibilidade bloqueia a compressão mesmo com o reserva saudável.

**c:01_01:C28 · aprovada** Em dois meses de operação de um FPSO, a indisponibilidade total foi maior em um deles, embora a contagem de falhas corretivas tenha sido parecida. Nesse mês, várias falhas ocorreram no mesmo período; a duração típica de cada reparo ficou próxima do histórico; acesso, sobressalentes, liberações e logística não tiveram atraso relevante; e havia menos frentes de manutenção do que equipamentos indisponíveis simultaneamente. Que fator explica o pior desempenho global desse mês?

- Resposta: Capacidade das equipes de manutenção virou o gargalo do retorno operacional, não piora da confiabilidade, porque o número de falhas foi semelhante e elas coincidiram no tempo.

### composta · mecanismo (5)

**c:02_02:C12 · aprovada** No sistema de água de injeção de um FPSO, a desaeração mecânica permaneceu sem mudança relevante e a dosagem nominal de bissulfito de sódio foi mantida. Ainda assim, começou a surgir oxigênio residual a jusante, coincidindo com cloro residual na água acima do habitual. Sem apontar falha da etapa mecânica, que mecanismo explica esse residual de oxigênio?

- Resposta: Cloro residual consumindo o bissulfito antes da remoção do oxigênio, o que reduz a dosagem efetiva do sequestrante.

**c:02_02:C15 · aprovada** Em um FPSO, o sensor on-line de residual de biocida, na linha principal logo após a injeção, indica valor compatível com a dosagem prevista. Mesmo assim, um trecho distal específico do circuito continua formando depósitos e volta a apresentar alta contagem microbiológica, enquanto os demais pontos permanecem controlados. Que mecanismo explica a leitura aparentemente boa sem controle efetivo nesse trecho?

- Resposta: Zonas mortas ou má distribuição deixando o trecho contaminado sem concentração ativa suficiente, apesar do residual adequado medido na linha principal.

**c:02_02:C24 · aprovada** Em um FPSO, a regeneração de MEG atinge a meta de remoção de água para reúso, mas seguem surgindo sólidos e incrustação no circuito de recuperação. A água produzida é salina, e as restrições hidráulicas e a perda de troca térmica aumentam nas campanhas de maior severidade da regeneração. Que mecanismo explica por que cumprir a meta de regeneração não encerra esse problema?

- Resposta: Precipitação de sais ao concentrar o MEG, porque a regeneração remove água para reúso, mas a remoção de sais precisa ser tratada separadamente.

**c:02_02:C30 · aprovada** Um desemulsificante escolhido por bottle test foi aplicado em um FPSO. Em bancada, a separação era boa; na operação, a resposta caiu após mudanças observadas no pH e na salinidade da água produzida, com mistura em válvulas e bombas e tempo de residência diferentes do ensaio. A repetição da triagem não indicou erro grosseiro. Por que o desempenho piorou no processo real?

- Resposta: Alteração da carga elétrica e da adsorção de espécies na interface da emulsão, porque pH/salinidade e o escoamento real mudam a resposta ao desemulsificante.

### janela · conceito (60)

**j:01_01-000-1 · aprovada** No monitoramento operacional de unidades de processo, qual é a função do KPI em relação à variável de processo?

- Resposta: Resumir o efeito da variável sobre o desempenho.

**j:01_01-004-1 · aprovada** Qual propriedade reúne disponibilidade, confiabilidade e mantenabilidade para sustentar a confiança no serviço de um sistema?

- Resposta: Dependabilidade.

**j:01_01-005-1 · aprovada** Na indisponibilidade de uma falha em um equipamento de FPSO, como se chama apenas a intervenção propriamente dita, sem esperas, acessos e liberações?

- Resposta: Tempo de reparo ativo.

**j:01_01-009-1 · aprovada** Qual propriedade expressa a chance de restaurar um sistema parado às condições especificadas dentro do tempo desejado, com meios de manutenção prescritos?

- Resposta: Mantenabilidade.

### janela · consequencia (30)

**j:01_01-006-4 · aprovada** Em um arranjo redundante de FPSO acompanhado por horizonte de missão cada vez mais longo, o que pode ocorrer com o ganho de confiabilidade e disponibilidade observado no início?

- Resposta: Ganho limitado no tempo: ele pode deixar de compensar a degradação dos equipamentos ativos.

**j:01_01-009-4 · aprovada** Sob taxa de reparo constante, se o tempo disponível para restaurar um sistema parado aumenta, o que acontece com a probabilidade acumulada de restabelecimento?

- Resposta: Ela aumenta e tende a 1.

**j:01_01-010-2 · aprovada** Num FPSO, o retorno após falhas está sendo atrasado principalmente por espera de acesso, sobressalente, liberação e logística, e não pela execução do reparo. Se forem adicionadas mais equipes de manutenção, que efeito tende a ocorrer na indisponibilidade?

- Resposta: Redução limitada da indisponibilidade, com pouco ganho de disponibilidade.

**j:01_01-014-2 · aprovada** Se a capacidade das rotas de reinjeção e de tratamento/descarte da água produzida fica abaixo da demanda gerada, o que acontece com a vazão total sustentável do FPSO?

- Resposta: Ela cai, porque a capacidade de manejar a fase aquosa passa a limitar a unidade.

### janela · decisao (20)

**j:01_01-021-3 · aprovada** Em um FPSO, um equipamento crítico pode seguir operando degradado até a próxima campanha, mas qualquer reparo exigirá sobressalente fora de estoque, especialista externo e mobilização de vários dias. A probabilidade de falha no curto prazo não é alta. Que ação técnica deve ser adotada?

- Resposta: Antecipar a intervenção de manutenção para restabelecer a função, sem adiar para a próxima campanha.

**j:02_02-013-3 · aprovada** Em um FPSO, duas correntes de água produzida passam pelo mesmo equipamento de flotação, com a mesma geração de bolhas, mistura e vazão. A primeira atinge a remoção requerida sem aditivo; a segunda não. Que ação técnica deve ser adotada para a segunda corrente?

- Resposta: Aplicar condicionamento químico com coagulante ou floculante antes da flotação.

**j:02_02-016-3 · aprovada** Na concepção de um FPSO, a água de injeção será do mar, haverá mistura no reservatório com água rica em bário e estrôncio, e o custo total de inibidores e paradas por deposição compromete a viabilidade do campo. Que solução deve ser adotada no condicionamento da água de injeção?

- Resposta: Instalar uma URS/SRU para dessulfatar a água do mar antes da injeção.

**j:02_02-019-3 · aprovada** Em um FPSO, a URS entrega água de injeção conforme especificação, mas a corrente concentrada acumula sulfato e cálcio e já houve precipitação interna. Que ação química deve ser aplicada?

- Resposta: Dosar anti-incrustante nos pontos internos e na corrente concentrada da URS, não na água de injeção.

### janela · diagnostico (32)

**j:01_01-005-4 · aprovada** Em dois equipamentos idênticos do topside de um FPSO, a frequência de falhas é a mesma e a intervenção física em cada falha dura o mesmo. Ainda assim, um fecha o mês com menor fração de tempo apto ao serviço. Nos registros desse equipamento, a maior parte da indisponibilidade ocorre antes do início da intervenção e depois de seu término, até a liberação para retorno seguro. Qual causa específica explica a diferença?

- Resposta: Tempos logísticos e administrativos maiores na indisponibilidade de cada falha.

**j:01_01-009-3 · aprovada** Em um ativo offshore remoto, após falhas semelhantes, o intervalo entre a parada e o início da intervenção aumentou; a condição segura e a liberação já estavam prontas, o sobressalente estava a bordo e, após a equipe chegar, diagnóstico e reparo duraram o mesmo de antes. Qual causa específica explica melhor o aumento do MTTR?

- Resposta: Logística de acesso e mobilização da equipe.

**j:01_01-010-3 · aprovada** Em um FPSO, vários subsistemas falham quase ao mesmo tempo. Acesso, sobressalentes, liberações e logística estão disponíveis sem atraso, mas parte dos reparos só inicia depois que outras frentes terminam. Os tempos de execução de cada reparo não mudaram. Qual causa específica melhor explica o aumento da indisponibilidade?

- Resposta: Capacidade insuficiente das equipes de manutenção, gerando fila de atendimento.

**j:01_01-018-3 · aprovada** Após três paradas de um FPSO, os relatórios finais foram emitidos e arquivados com campos completos. Nas duas últimas, repetiram-se os mesmos acréscimos de escopo e atrasos por suporte não previsto. As lições registradas reaparecem praticamente sem alteração, e nas revisões seguintes não há confronto sistemático entre planejado e realizado. Qual causa específica explica melhor por que o histórico não está melhorando as decisões?

- Resposta: Preenchimento formal do relatório sem análise crítica real dos desvios e das lições aprendidas.

### janela · mecanismo (57)

**j:01_01-006-2 · aprovada** Quando o equipamento reserva permanece parado até ser demandado, como ele ainda pode falhar em manter o serviço após a perda do item ativo?

- Resposta: Falhas em espera e de partida/comutação podem impedir sua entrada em operação quando solicitada.

**j:01_01-007-2 · aprovada** Depois que o sistema está detalhado, como um modelo RAM mais completo melhora as previsões de disponibilidade e confiabilidade?

- Resposta: Ao evidenciar os maiores contribuintes de falha e comparar modos operacionais, tornando a previsão mais aderente ao sistema.

**j:01_01-008-2 · aprovada** Em um FPSO, por que um item com baixa taxa de falha pode exigir mais atenção que outro que falha mais?

- Resposta: Porque sua indisponibilidade pode bloquear produção, segurança de processo ou exportação, gerando impacto sistêmico maior mesmo com menor frequência de falha.

**j:01_01-009-2 · aprovada** Ao apurar o MTTR de um sistema de topsides, por que incluir no mesmo intervalo as esperas por acesso, sobressalente ou liberação distorce o indicador?

- Resposta: Porque mistura tempo efetivo de reparo com outros tempos de indisponibilidade, fazendo o indicador refletir atrasos de suporte e não só o reparo.

### janela · procedimento (41)

**j:01_01-002-4 · aprovada** Ao comparar taxas de frequência de acidentes de períodos diferentes em um FPSO, como a equipe deve verificar se a série histórica é comparável?

- Resposta: Mantendo compatíveis o período de apuração, o critério de enquadramento e a base de horas-homem.

**j:01_01-005-3 · aprovada** Em estado estacionário, como representar a disponibilidade observada de um equipamento do FPSO a partir do histórico de operação?

- Resposta: Pela razão entre uptime e tempo total observado.

**j:01_01-012-4 · aprovada · auditor: decisao** Na escolha de uma rota para prevenir incrustação em produção offshore, como a alternativa deve ser selecionada?

- Resposta: Pela análise do mecanismo dominante de incrustação, da origem dos íons, da arquitetura de injeção e produção, da acessibilidade para intervenção e das penalidades de parada.

**j:02_02-006-3 · aprovada** Ao avaliar a dosagem de um antiespumante no processamento de óleo e gás, como a resposta à dose deve ser verificada?

- Resposta: Mapeando a faixa útil de concentração, o ponto sem ganho adicional e eventuais efeitos nas demais etapas do processo.
