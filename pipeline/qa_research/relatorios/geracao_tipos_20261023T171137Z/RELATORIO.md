# Geração híbrida por tipo de questão

Janela: prompt v14 (1 conceito, 1 mecanismo ou consequência, 1 diagnóstico, decisão ou procedimento, 1 livre). Compostas: uma por encadeamento do inventário. Auditoria: `gpt-5-4-petrobras:high`.

Janelas: 60 ({'ok': 60}); fundamentos literais 240; questões que usam bloco de apoio 1. Compostas: {'total': 64, 'ok': 64, 'insuficiente': 0}.

| Origem | Tipo | n | com cenário | palavras (perg./resp.) | tipo confere | ref. inválida | atalho |
|---|---|---|---|---|---|---|---|
| janela | conceito | 79 | 0 | 16.4/5.0 | 67/79 | 22 | 34 |
| janela | mecanismo | 45 | 0 | 17.8/16.9 | 44/45 | 6 | 11 |
| janela | consequencia | 37 | 3 | 22.2/9.6 | 37/37 | 12 | 22 |
| janela | diagnostico | 13 | 13 | 44.2/12.1 | 13/13 | 2 | 5 |
| janela | decisao | 38 | 38 | 37.8/12.2 | 35/38 | 4 | 28 |
| janela | procedimento | 28 | 12 | 23.2/12.0 | 25/28 | 8 | 13 |
| janela | **total** | 240 | 66 | 23.3/10.3 | 221/240 | 54 | 113 |
| composta | mecanismo | 3 | 3 | 56.0/23.3 | 2/3 | 1 | 0 |
| composta | consequencia | 13 | 13 | 54.9/19.2 | 12/13 | 3 | 5 |
| composta | diagnostico | 26 | 26 | 56.6/20.6 | 22/26 | 3 | 4 |
| composta | decisao | 22 | 22 | 55.7/20.8 | 21/22 | 0 | 12 |
| composta | **total** | 64 | 64 | 55.9/20.5 | 57/64 | 7 | 21 |

Tipos por documento: {'01_01': {'conceito': 32, 'mecanismo': 20, 'decisao': 30, 'procedimento': 14, 'consequencia': 22, 'diagnostico': 10}, '02_02': {'conceito': 47, 'consequencia': 28, 'procedimento': 14, 'decisao': 30, 'mecanismo': 28, 'diagnostico': 29}}.

Combinações de tipos mais comuns por janela: {'conceito+consequencia+decisao+mecanismo': 10, 'conceito+consequencia+mecanismo+procedimento': 8, 'conceito+decisao+mecanismo+procedimento': 8, 'conceito+conceito+decisao+mecanismo': 5, 'conceito+conceito+consequencia+decisao': 5, 'conceito+conceito+mecanismo+procedimento': 4, 'conceito+consequencia+decisao+procedimento': 3, 'conceito+conceito+diagnostico+mecanismo': 3, 'conceito+consequencia+diagnostico+procedimento': 2, 'conceito+conceito+consequencia+procedimento': 2}.

Tipo declarado → sugerido pelo auditor (divergências): {'conceito->decisao': 9, 'decisao->procedimento': 3, 'procedimento->decisao': 3, 'mecanismo->diagnostico': 2, 'conceito->procedimento': 2, 'diagnostico->conceito': 2, 'diagnostico->mecanismo': 2, 'conceito->mecanismo': 1, 'decisao->diagnostico': 1, 'consequencia->conceito': 1}.

Pares quase duplicados (Jaccard ≥ 0,6): 0. Falhas pendentes: 0.

## Reclassificação do piloto v2

Acurácia dos respondentes sem contexto (R1 gpt-4-1-nano, R2 gpt-5-4-nano low) por tipo atribuído:

| Tipo | n | R1 | R2 | ref. inválida |
|---|---|---|---|---|
| conceito | 35 | 0.63 | 0.84 | 5 |
| mecanismo | 34 | 0.59 | 0.96 | 1 |
| consequencia | 26 | 0.73 | 0.87 | 6 |
| diagnostico | 60 | 0.63 | 0.88 | 9 |
| decisao | 36 | 0.71 | 0.79 | 4 |
| procedimento | 8 | 0.44 | 0.81 | 0 |

Resposta é dado específico (nome, local, parâmetro, prática) x geral: {'True': {'n': 129, 'R1': 0.59, 'R2': 0.84, 'ref_invalida': 16}, 'False': {'n': 70, 'R1': 0.74, 'R2': 0.91, 'ref_invalida': 9}}.
Classificações ambíguas: 18. Nível antigo x tipo: {'facil': {'conceito': 26, 'diagnostico': 3, 'procedimento': 2, 'decisao': 4, 'mecanismo': 3, 'consequencia': 2}, 'media': {'decisao': 14, 'consequencia': 15, 'diagnostico': 3, 'conceito': 4, 'procedimento': 2, 'mecanismo': 2}, 'dificil': {'diagnostico': 54, 'decisao': 18, 'consequencia': 9, 'procedimento': 4, 'conceito': 5, 'mecanismo': 29}}.

## Exemplos por tipo

### composta · consequencia (13)

**c:01_01:C11 · atalho** Nos topsides de um FPSO, a equipe usa ferramenta online para acompanhar um processo com margens estreitas de especificação e alta exigência de segurança. Durante a campanha, o analisador que fornece a medição-chave para esse acompanhamento ficou indisponível e, depois, passou a indicar valores pouco confiáveis; os demais sistemas continuam em serviço. Qual efeito final essa condição traz ao processo?

- Resposta: Aumento do risco de processo, porque a falta ou baixa confiabilidade de uma medição essencial reduz a capacidade de detectar e corrigir desvios.

**c:01_01:C18 · atalho** Em um FPSO, um desvio operacional foi mantido por vários turnos. A validação técnica da mudança não saiu porque a documentação aplicável estava inacessível e não havia definição clara de quem autorizaria a revisão. A barreira crítica do cenário continua citada na análise vigente, embora a configuração real de operação tenha mudado desde então. Que efeito final isso traz na relação entre o risco real e o risco assumido para operar?

- Resposta: O risco real divergiu do risco assumido para operar, porque a barreira permaneceu considerada sem revisão da condição efetiva.

**c:01_01:C19 · atalho** Em um FPSO de alta produção, a correção de uma barreira crítica foi adiada para evitar gasto imediato, embora seu desempenho real esteja degradado e ela sustente uma função considerada nas análises de risco. Em termos econômicos, que consequência potencial tende a ser a principal dessa decisão?

- Resposta: Perda potencial elevada de receita diária, porque numa unidade de alta produção a indisponibilidade compromete mais receita do que o custo direto do reparo.

**c:01_01:C21 · atalho** Na avaliação RAM de um FPSO novo, ainda sem histórico confiável da própria unidade, a equipe alimenta o modelo com um banco setorial para prever o desempenho desse FPSO nas suas condições locais de operação e manutenção. Qual é a principal limitação desse resultado?

- Resposta: Resultado RAM impreciso para a unidade, porque parâmetros do banco setorial podem não representar suas condições locais.

### composta · decisao (22)

**c:01_01:C10** Em um dashboard da sala de controle de um FPSO, o mesmo processo aparece com três métricas ambientais: taxa de auditorias concluídas, intensidade de emissão/flare e uma medida da qualidade ambiental externa. Durante o turno, uma intervenção precisa ser definida para corrigir o processo. Que classe de indicador ambiental deve orientar esse ajuste?

- Resposta: OPI, porque é a classe de indicador ambiental voltada ao desempenho operacional do processo.

**c:01_01:C12 · atalho** Em um poço ligado a um FPSO, foi constatada incrustação na coluna de produção. A vazão bruta caiu e a pressão observada no poço mudou em relação ao padrão anterior. Diante desse quadro, que natureza de ação deve ser priorizada?

- Resposta: Ação corretiva de remoção/desobstrução da restrição, pois a prevenção química não elimina o depósito já refletido na vazão e na pressão.

**c:01_01:C13 · atalho** Em um FPSO, a reinjeção de água produzida opera próxima do limite. A linha de tratamento e descarte no mar está operacional, atende às exigências aplicáveis nessa condição, e não há outra restrição equivalente em óleo, gás ou separação primária no momento. Para sustentar a carga total da unidade, qual ajuste operacional deve ser priorizado?

- Resposta: Desviar mais água produzida para tratamento/descarte, porque a limitação está na reinjeção e a outra rota permanece disponível e admissível.

**c:01_01:C14 · atalho** Na revisão da FMEA de um FPSO, dois modos de falha receberam o mesmo NPR. Um interrompe a função principal de exportação por mais tempo e sua recuperação depende de recursos e janelas mais restritos; o outro afeta apenas um serviço auxiliar e pode ser contornado rapidamente sem parar a função principal. Qual modo deve receber prioridade operacional?

- Resposta: O modo que interrompe a função principal e tem recuperação mais longa e restrita, porque NPR igual não torna equivalentes impactos funcionais distintos.

### composta · diagnostico (26)

**c:01_01:C1** Em um pacote reparável de um FPSO, as ordens separam horas de intervenção técnica do tempo até o retorno. Em falhas repetidas, a intervenção ativa permaneceu quase igual, mas a parada total variou de horas para dias; colocar mais técnicos não encurtou o retorno operacional. Na disponibilidade operacional observada, o que está dominando a indisponibilidade?

- Resposta: Downtime logístico/administrativo dominante na disponibilidade operacional, porque a intervenção ativa ficou estável e o reforço de equipe não reduziu o tempo total parado.

**c:01_01:C15 · auditor: conceito** No início da campanha, uma bomba de injeção de água do FPSO entrou em operação normal. Nas verificações instantâneas de turno, ela quase sempre aparecia em serviço. Mesmo assim, o histórico do período registrou várias paradas não planejadas, com retorno posterior sob as mesmas condições. Qual atributo de desempenho está pior representado por esse comportamento?

- Resposta: confiabilidade, porque as paradas repetidas no período mostram incapacidade de manter a função requerida sob as mesmas condições.

**c:01_01:C16 · auditor: conceito** Após uma falha em um sistema do FPSO, o retorno à operação foi muito rápido com mobilização fora do padrão, jornada estendida e foco total da equipe. Entre antes e depois do evento, não houve mudança no projeto do item, na acessibilidade nem no arranjo de suporte à manutenção. Que aspecto foi efetivamente demonstrado por esse evento?

- Resposta: Desempenho da ação de manutenção, não aumento de mantenabilidade, porque o retorno rápido ocorreu por esforço excepcional sem mudança no sistema ou no suporte.

**c:01_01:C2** Em um FPSO, dois trens de compressão operam em paralelo. Nos eventos que mais reduzem a disponibilidade observada, o trem reserva estava disponível, mas a função se perde nos dois trens no mesmo instante; a comutação não restabelece a compressão e não há padrão de falha mecânica exclusivo de um compressor. No KPI de disponibilidade, que elemento deve ser tratado como limitante mais crítico?

- Resposta: O gargalo compartilhado de utilidades, controle ou descarga entre os trens, porque sua indisponibilidade derruba ambos e bloqueia a função relevante.

### composta · mecanismo (3)

**c:01_01:C32** Em uma FPSO, o KPI de disponibilidade de um trem de geração considera um gerador em reserva fria. Como ele fica meses parado, a equipe assume que a baixa exposição ao desgaste basta para tratá-lo como disponível. Considerando disponibilidade como a aptidão para executar a função quando requerida, com recursos externos assegurados, que mecanismo invalida essa premissa?

- Resposta: Falha de partida ou de comutação do reserva, porque baixa exposição ao desgaste não garante aptidão para cumprir a função quando for requerido.

**c:02_02:C15 · auditor: diagnostico · ref. inválida** Em um FPSO, o residual de biocida medido on-line na linha principal, logo após a injeção, acompanha a dosagem prevista. Mesmo assim, um trecho distal do circuito de água de injeção continua formando depósitos e voltando a apresentar alta contagem microbiológica. Que mecanismo explica essa leitura satisfatória sem controle efetivo naquele trecho?

- Resposta: Má distribuição ou zonas mortas, deixando o trecho contaminado sem concentração ativa suficiente apesar do residual adequado medido na linha principal.

**c:02_02:C24** Num FPSO, a regeneração de MEG atinge a meta de remoção de água para reúso. Mesmo assim, seguem aparecendo incrustação e sólidos no circuito de recuperação, e o problema aumenta nos trechos que recebem glicol de retorno mais concentrado. A água produzida traz sais para o sistema. Que mecanismo explica por que a regeneração, sozinha, não encerra o problema?

- Resposta: Precipitação de sais ao concentrar o MEG, porque a regeneração remove água para reúso, mas não garante a remoção separada dos sais trazidos pela água produzida.

### janela · conceito (79)

**j:01_01-000-1** Em monitoramento operacional de topsides de FPSO, qual é a função do indicador de desempenho em relação à variável de processo?

- Resposta: Resumir o efeito da variável de processo sobre o desempenho, sem substituí-la.

**j:01_01-000-4 · auditor: mecanismo · ref. inválida** Em topsides de FPSO, o que torna útil uma metodologia ampla de monitoramento por indicadores?

- Resposta: A interação entre separação, tratamento de óleo, água, gás, utilidades e sistemas de controle.

**j:01_01-001-1 · ref. inválida** Com que tipo de referência um KPI pode comparar resultados reais?

- Resposta: Referências teóricas.

**j:01_01-001-4 · ref. inválida · atalho** Em plantas de produção, qual escopo de aplicação de KPI abrange toda a unidade?

- Resposta: A instalação como um todo.

### janela · consequencia (37)

**j:01_01-003-2 · atalho** Se a organização evolui de foco exclusivo em cumprimento legal para uma atuação com iniciativas voluntárias, que mudança tende a ocorrer na seleção dos indicadores ambientais?

- Resposta: Maior ênfase em indicadores associados a programas voluntários, além do cumprimento legal.

**j:01_01-005-2 · atalho** Se o MTTR aumenta e o MTBF permanece constante em um sistema reparável, qual efeito isso produz na disponibilidade?

- Resposta: A disponibilidade diminui.

**j:01_01-006-4** Ao longo de tempos de missão mais longos, qual tende a ser o comportamento do ganho trazido pela redundância?

- Resposta: O benefício deixa de ser ilimitado, porque a degradação dos ativos pode deixar de ser compensada pelo reserva.

**j:01_01-007-2** Em uma unidade nova ou com protótipos, qual efeito da ausência de histórico confiável na análise RAM?

- Resposta: Resultados imprecisos, por introdução de parâmetros inadequados.

### janela · decisao (38)

**j:01_01-000-3 · auditor: procedimento · atalho** Em um FPSO, um KPI do tratamento se afasta da referência durante um aumento de carga e volta a estabilizar poucos minutos depois, sem persistência fora de especificação no produto. Qual verificação deve ter prioridade antes de concluir que houve perda estrutural de desempenho?

- Resposta: Integrar o KPI ao contexto do processo, ao histórico recente e ao conhecimento acumulado da operação.

**j:01_01-001-3 · atalho** Num FPSO, um indicador criado para relatório mensal passará a orientar ajustes imediatos de operação no turno, sem mudança no processo físico monitorado. Qual critério deve guiar a redefinição desse indicador?

- Resposta: Coerência da definição com a decisão operacional que ele deve sustentar.

**j:01_01-003-3** Em um FPSO, o painel ambiental precisa distinguir resultados das práticas de gestão, resultados da operação e o estado do meio ao redor da unidade. Que estrutura de indicadores deve ser adotada?

- Resposta: MPI para gestão, OPI para operação e ECI para condições ambientais.

**j:01_01-007-3 · atalho** Na etapa preliminar do projeto de um FPSO, a equipe precisa validar arranjo, quantidade de equipamentos e alternativas de redundância antes do detalhamento do sistema. Que modelagem RAM deve priorizar?

- Resposta: Modelos mais simples.

### janela · diagnostico (13)

**j:01_01-005-3 · ref. inválida · atalho** Em dois compressores de um FPSO com a mesma frequência de falhas e o mesmo tempo de intervenção ativa, um acumula mais horas indisponível por evento fora da intervenção propriamente dita, até o retorno seguro à operação. Qual causa específica explica sua menor disponibilidade operacional?

- Resposta: Tempos logísticos e administrativos mais longos no downtime.

**j:01_01-010-3** Em um FPSO, dois subsistemas da planta falham quase ao mesmo tempo. O acesso já está liberado, sobressalentes e ferramentas estão a bordo e as permissões emitidas, mas o segundo reparo só começa após o término do primeiro, aumentando o tempo parado. Qual é a causa mais provável desse prolongamento?

- Resposta: Gargalo na capacidade das equipes de manutenção, gerando fila entre falhas simultâneas.

**j:01_01-011-3 · atalho** Em um FPSO hipotético, a separação de óleo e a compressão de gás seguem sem desvios relevantes, mas o volume aquoso gerado já não consegue ser todo reinjetado nem tratado para descarte dentro do aceitável; para manter conformidade, a vazão total do campo é reduzida. Qual restrição específica explica essa redução?

- Resposta: Perda de capacidade na malha de água produzida, sem capacidade suficiente para reinjetar ou descartar a fase aquosa gerada.

**j:02_02-013-4** Duas correntes de água produzida passam pela mesma unidade e pelo mesmo equipamento de flotação. Uma atende sem aditivo; a outra só melhora quando se injeta coagulante/floculante. Qual causa específica explica a necessidade de condicionamento na segunda corrente?

- Resposta: Maior estabilidade da dispersão nessa corrente, tornando a flotação simples insuficiente.

### janela · mecanismo (45)

**j:01_01-000-2 · atalho** Por que ferramentas online se tornam mais valiosas quando o processo opera com especificações mais restritas e maior exigência de segurança?

- Resposta: Porque permitem avaliar condições operacionais em tempo próximo do real, facilitando detectar operação anormal e antecipar anormalidades.

**j:01_01-001-2 · atalho** Por que o mesmo processo de topsides de um FPSO pode ser acompanhado por indicadores diferentes quando muda a finalidade da avaliação?

- Resposta: Porque a forma de expressão do indicador depende do interesse da avaliação e do usuário.

**j:01_01-002-2 · atalho** Por que um indicador de energia por unidade produzida é mais adequado que o consumo total para avaliar mudança real de eficiência em um FPSO?

- Resposta: Porque normaliza o consumo pela produção e separa o efeito de carga ou volume processado do desempenho intrínseco.

**j:01_01-004-2 · atalho** Como um projeto para falha segura pode reduzir a continuidade operacional de um sistema em FPSO?

- Resposta: Ao interromper o serviço quando a proteção atua, preservando segurança e integridade mesmo com menor continuidade operacional.

### janela · procedimento (28)

**j:01_01-002-3 · atalho** Em dois meses, o FPSO teve 3 acidentes sem afastamento em cada mês, mas no segundo houve muito mais horas de trabalho por campanha de manutenção. Como o indicador deve ser estruturado para comparar o desempenho de segurança?

- Resposta: Como taxa de frequência por horas-homem de exposição ao risco.

**j:01_01-003-4 · atalho** Como a minimização de resíduos deve ser conduzida em projetos de exploração e produção?

- Resposta: Por identificação de oportunidades de redução na fonte, com reutilização e reciclagem.

**j:01_01-004-3 · auditor: decisao · ref. inválida** Dois sistemas de FPSO tiveram a mesma quantidade de falhas no período. Como o desempenho global deve ser comparado?

- Resposta: Pela rapidez e pelas condições de retorno à operação aceitável de cada sistema.

**j:01_01-005-4** Sem registros diretos de uptime e downtime de um sistema reparável, como aproximar a disponibilidade de referência?

- Resposta: Usando os valores médios de MTBF e MTTR.
