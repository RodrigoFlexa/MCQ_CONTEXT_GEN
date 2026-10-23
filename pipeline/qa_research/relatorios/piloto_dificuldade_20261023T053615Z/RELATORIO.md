# Piloto de dificuldade v2: inventário x EC v13

Rubrica: `pipeline/qa_research/DIFICULDADE_V2.md`. Respondentes sem contexto: R1 gpt-4-1-nano-petrobras | R2 gpt-5-4-nano-petrobras:low. Juiz: `gpt-5-4-petrobras:high`.

Acurácia com correta = 1 e parcial = 0,5; entre parênteses, só as corretas. Se a dificuldade for real, a acurácia cai de fácil para difícil.

| Método | Nível | R1 | R2 | n | atalho genérico | ref. inválida | filtro simulado |
|---|---|---|---|---|---|---|---|
| inventário | facil | 0.65 (0.55) | 0.82 (0.75) | 20 | 8 | 4 | 0.00 (n=2) |
| inventário | media | 0.68 (0.45) | 0.85 (0.75) | 20 | 13 | 3 | 0.50 (n=1) |
| inventário | dificil | 0.60 (0.42) | 0.92 (0.85) | 60 | 20 | 4 | 0.00 (n=1) |
| inventário | ↳ dificil_A | 0.67 (0.47) | 0.93 (0.87) | 30 | 11 | 1 | – |
| inventário | ↳ dificil_B | 0.53 (0.37) | 0.90 (0.83) | 30 | 9 | 3 | 0.00 (n=1) |
| inventário | **total** | 0.62 (0.45) | 0.89 (0.81) | 100 | 41 | 11 | 0.12 (n=4) |
| EC v13 | facil | 0.62 (0.45) | 0.75 (0.70) | 20 | 10 | 8 | 0.38 (n=4) |
| EC v13 | media | 0.72 (0.60) | 0.72 (0.55) | 20 | 15 | 4 | 0.50 (n=2) |
| EC v13 | dificil | 0.65 (0.54) | 0.92 (0.85) | 59 | 31 | 2 | – |
| EC v13 | **total** | 0.66 (0.54) | 0.85 (0.76) | 99 | 56 | 14 | 0.42 (n=6) |

Filtro simulado: acurácia de R1 nas questões que o último respondente errou (ideia de filtro adversarial, como em Humanity's Last Exam).

Histórico v1 (R1 = gpt-4-1-nano): inventario facil 0.56, media 0.66, dificil 0.60; ec facil 0.69, media 0.74, dificil 0.67.

Acurácia limpa de R1 (sem referências inválidas e sem atalho genérico): inv facil: 0.444; inv media: 0.333; inv dificil: 0.513; ec facil: 0.429; ec media: 0.667; ec dificil: 0.393.

Inventário: relações {'01_01': 155, '02_02': 340}, encadeamentos {'01_01': 32, '02_02': 32}, geração {'geradas': 100, 'ok': 100, 'insuficiente': 0, 'insuficiente_por_tipo': {'facil': 0, 'media': 0, 'dificil_A': 0, 'dificil_B': 0}, 'faltas_no_inventario': {}, 'faltas_finais': {}}.
EC: {'faltas_amostra': {'01_01:dificil': 1}, 'falhas_janelas': 0}.
Falhas pendentes: 0.

## Questões avaliadas

**ec · dificil · R1 correta · R2 correta · atalho** Em um FPSO, um KPI online de separação se afasta da meta sempre nos minutos seguintes a cada aumento de carga. Nesses mesmos intervalos, pressão e níveis oscilam; depois, com a carga estabilizada, essas variáveis e o KPI retornam ao patamar anterior. O padrão se repete em todos os degraus da semana, sem piora acumulada e sem mudança de alimentação ou de estratégia de controle. Que conclusão sobre o desempenho esse conjunto sustenta?

- Referência: Sem perda estrutural de desempenho; o desvio acompanha regime transiente após mudança de carga.
- R1: Indicativo de resposta transitória, possivelmente por efeito de dinâmica de processo ou controle adaptativo, não sinalizando degradação permanente, mas necessidade de ajuste na estratégia ou na modelagem do controle para melhorar estabilidade.
- R2: Sustenta que o desempenho global é estável: o KPI desvia apenas transitoriamente durante degraus de carga (com oscilações de pressão/níveis) e retorna ao baseline quando a carga estabiliza. Não há deterioração acumulada nem mudança de regime; logo a separação e o controle estão bem sintonizados, refletindo respostas dinâmicas normais a perturbações.
- Desenho: atraente = Degradação de equipamento. | descarta = O KPI e as variáveis retornam ao patamar anterior após cada degrau, sem piora acumulada ao longo da semana. | passo oculto = Inferir que o desvio segue os degraus de carga e desaparece após a estabilização, caracterizando comportamento transitório.
- Juiz: Como o KPI só se afasta durante os transientes de aumento de carga e retorna ao patamar anterior sem piora acumulada, ambos concluem corretamente que não há perda estrutural de desempenho, algo praticamente dado pelo padrão descrito.

**ec · dificil · R1 correta · R2 correta · atalho** No painel em tempo real do FPSO, a operação passou a usar o mesmo KPI criado para o relatório mensal da gerência. Mesmo com atualização rápida, ele continua útil só para tendência mensal e não ajuda a decidir ajustes durante mudanças de carga. Que mudança deve ser feita nesse KPI?

- Referência: Redefinir a métrica para a decisão operacional em tempo real, não manter a definição gerencial.
- R1: Incluir um componente de tempo real ou limite de variação para o KPI, permitindo ajustes durante mudanças de carga, além de análise instantânea de desvios para ações rápidas.
- R2: Ajustar o KPI para calcular com janela móvel de curto prazo (ex.: média/rolling dos últimos minutos/horas) em vez de agregação mensal fixa. Assim ele reflete variações rápidas de carga e suporta decisão operacional em tempo real.
- Desenho: atraente = Aumentar ainda mais a taxa de atualização do painel. | descarta = Mesmo com atualização rápida, o KPI segue útil só para tendência mensal e não ajuda nas decisões durante mudanças de carga. | passo oculto = O problema não é a velocidade de exibição, mas a incoerência entre a finalidade original do KPI e a decisão operacional que ele precisa sustentar.
- Juiz: Ambos acertam ao mudar o KPI da agregação/definição gerencial para uma métrica de horizonte curto voltada à decisão operacional em tempo real; a referência é válida e um atalho genérico como 'adaptar para tempo real' já bastaria.

**ec · dificil · R1 correta · R2 correta · atalho** Em um FPSO, a taxa anual de acidentes com afastamento ficou igual à do ano anterior. No entanto, neste ano passaram a entrar no numerador e nas horas-homem os contratados de campanha, antes excluídos. Que aspecto técnico dessa comparação fica comprometido?

- Referência: A comparabilidade temporal do indicador, porque mudou o critério de enquadramento e a base de exposição.
- R1: A comparabilidade da taxa de acidentes é comprometida, pois a inclusão de contratados de campanha no numerador e horas-homem influencia o cálculo, dificultando a avaliação real do desempenho de segurança ao longo do tempo.
- R2: Fica comprometida a comparabilidade temporal (consistência da definição do indicador). Ao alterar o escopo do numerador e do denominador (inclusão dos contratados de campanha), a taxa anual deixa de ser diretamente comparável ao ano anterior, pois não mede a mesma população de trabalhadores/horas-homem.
- Desenho: atraente = Desempenho estável. | descarta = Neste ano passaram a entrar no numerador e nas horas-homem os contratados de campanha, antes excluídos. | passo oculto = Ao incluir contratados, a taxa passou a medir uma população exposta diferente, mesmo com o mesmo valor numérico.
- Juiz: Ambos reconhecem que a taxa perdeu comparabilidade temporal porque mudou simultaneamente o critério de inclusão e a base de exposição, algo que sai quase diretamente do enunciado ao alterar numerador e horas-homem.

**ec · dificil · R1 correta · R2 correta** Dois equipamentos reparáveis de um FPSO tiveram a mesma frequência de falhas no mês e o mesmo tempo de intervenção ativa por falha. Mesmo assim, um permaneceu menos tempo apto a cumprir a função, porque após cada evento houve mais espera por sobressalentes, acesso e liberação para retorno seguro. Que indicador fica pior nesse equipamento?

- Referência: Disponibilidade operacional, porque o downtime total aumenta mesmo sem mudar a frequência de falhas nem o reparo ativo.
- R1: O indicador de disponibilidade operacional fica pior devido ao maior tempo de inatividade causado pela espera por sobressalentes e liberação
- R2: O indicador que piora é a **Disponibilidade Operacional (A)** do equipamento, pois aumenta o tempo total de indisponibilidade (maior espera por sobressalentes, acesso e liberação para retorno seguro), mesmo com mesma frequência de falhas e mesma intervenção ativa.
- Desenho: atraente = Confiabilidade. | descarta = A mesma frequência de falhas e o mesmo tempo de intervenção ativa mostram que a diferença vem das esperas para retorno, não da ocorrência das falhas. | passo oculto = As esperas logísticas e administrativas ampliam a indisponibilidade total e reduzem a fração de tempo em que o equipamento fica apto a cumprir a função.
- Juiz: O decisivo é que aumentou o downtime total por esperas logísticas e de liberação, piorando a disponibilidade operacional mesmo com mesma frequência de falhas e mesmo reparo ativo, o que ambos responderam, e distinguir esse indicador não é mero atalho genérico.

**ec · dificil · R1 incorreta · R2 correta** Em 1.000 h observadas no FPSO, o compressor A teve 2 falhas; cada uma consumiu 4 h de intervenção ativa e mais 36 h entre diagnóstico, mobilização, acesso, liberação e retorno seguro. O compressor B teve 5 falhas; cada uma consumiu 4 h de intervenção ativa e 4 h nesses mesmos tempos adicionais. Em qual compressor a disponibilidade operacional fica menor?

- Referência: Compressor A, por acumular 80 h de downtime total contra 40 h do B.
- R1: O compressor B apresenta menor disponibilidade operacional devido ao maior número de falhas e maior tempo total de intervenção e diagnósticos.
- R2: O compressor A. Downtime A = 2×(4+36)=80 h (disponibilidade 920/1000=92%). Downtime B = 5×(4+4)=40 h (disponibilidade 960/1000=96%). Logo, a disponibilidade operacional é menor no A.
- Desenho: atraente = Compressor B, por falhar mais vezes. | descarta = No A, cada falha soma 40 h de indisponibilidade, enquanto no B cada falha soma 8 h; o downtime total do A fica maior. | passo oculto = Somar a indisponibilidade por falha de cada compressor e converter o maior downtime total em menor disponibilidade operacional.
- Juiz: Só R2 somou corretamente o downtime operacional completo de cada falha e concluiu que o A tem menor disponibilidade, tornando a referência válida e sem atalho.

**ec · dificil · R1 parcial · R2 correta** Em um FPSO, um compressor em serviço falha. O reserva em standby recebe comando, parte e atinge rotação nominal, mas a exportação não retorna porque os dois trens ficam sem água de resfriamento após a parada de uma única bomba comum. Não houve falha mecânica adicional no reserva. Que dependência do arranjo explica o ganho de disponibilidade menor que o previsto?

- Referência: Um gargalo de utilidades compartilhado na água de resfriamento.
- R1: A dependência do arranjo de resfriamento que requer o funcionamento concomitante de ambos os trens para manutenção da água de resfriamento explica o ganho de disponibilidade menor que o previsto.
- R2: Dependência de “utilidades” compartilhadas (common-cause): os dois trens de compressão dependem de uma mesma bomba/linha comum de água de resfriamento. Assim, ao parar a bomba comum, ambos ficam sem resfriamento e o reserva também não consegue exportar, reduzindo a disponibilidade.
- Desenho: atraente = Falha de partida ou de comutação do compressor reserva. | descarta = O reserva recebeu comando, partiu, atingiu rotação nominal e não apresentou falha mecânica adicional. | passo oculto = A partida bem-sucedida do reserva descarta problema de comutação; a perda da água de resfriamento comum retira a condição necessária para ambos os trens manterem o serviço.
- Juiz: A referência é válida porque o ponto decisivo é a utilidade compartilhada de água de resfriamento como gargalo comum; R2 afirmou isso claramente, enquanto R1 mencionou apenas uma dependência do resfriamento sem explicitar o elemento comum que derruba ambos os trens.

**ec · dificil · R1 correta · R2 correta · atalho** Um FPSO novo usou um modelo RAM bastante detalhado, com lógica funcional já capaz de representar dependências e modos operacionais. Mesmo assim, a disponibilidade prevista ficou distante do desempenho inicial. Os parâmetros de falha e reparo vieram de outra unidade com arquitetura, acessibilidade e estratégia de manutenção diferentes, porque não havia histórico local robusto. Que fator técnico mais comprometeu essa previsão?

- Referência: Parâmetros de falha e reparo não representativos da unidade, por falta de histórico confiável próprio.
- R1: A falta de dados históricos locais precisos comprometeu a precisão da previsão de disponibilidade, pois os parâmetros de falha e reparo não refletiam a realidade operacional específica da unidade.
- R2: O principal foi a extrapolação de parâmetros de falha e reparo de outra unidade: diferenças de arquitetura, acessibilidade e estratégia de manutenção tornam as taxas de falha/MTTR não representativas. Sem histórico local para calibrar o RAM, a disponibilidade prevista fica sistematicamente distante do desempenho real.
- Desenho: atraente = Modelo simplificado demais. | descarta = A lógica funcional já era capaz de representar dependências e modos operacionais. | passo oculto = Se a lógica do modelo já representa dependências e modos operacionais, o desvio principal passa a vir da inadequação dos dados; esses parâmetros mudam com arquitetura, acessibilidade e manutenção.
- Juiz: O ponto técnico decisivo é a não representatividade dos parâmetros de falha e reparo importados de outra unidade por falta de histórico local confiável, e o próprio enunciado praticamente entrega esse fator.

**ec · dificil · R1 correta · R2 correta · atalho** Após seis anos de operação, um FPSO acumulou muitos registros de falha e retorno à operação. Ainda assim, as análises seguem pouco confiáveis: operação, manutenção e engenharia usam classificações diferentes, vários mecanismos distintos entram na mesma categoria e parte do histórico fica em planilhas separadas. Um analista atribui o problema à falta de histórico. O que realmente está limitando a avaliação de disponibilidade e confiabilidade?

- Referência: A ausência de padronização e gestão eletrônica que diferencie as causas de falha.
- R1: A ausência de um sistema padronizado, integrado e confiável de registro e classificação de dados limita a avaliação de disponibilidade e confiabilidade.
- R2: A limitação principal é a baixa qualidade e consistência do dado: taxonomia/definições diferentes entre Operação-Manutenção-Engenharia, classificação que mistura múltiplos mecanismos em uma categoria e histórico fragmentado (planilhas separadas), impedindo rastreio unívoco de falha→reparo→parada e, portanto, avaliação confiável de disponibilidade/confiabilidade.
- Desenho: atraente = Falta de histórico. | descarta = Seis anos de operação com muitos registros acumulados, mas em classificações diferentes e planilhas separadas. | passo oculto = Muitos anos de registros não aumentam a confiança se os dados não estiverem padronizados, eletronicamente geridos e capazes de separar causas.
- Juiz: O ponto decisivo é a falta de padronização, integração eletrônica e diferenciação adequada das causas de falha nos registros, que ambos reconheceram; a referência é válida e o enunciado praticamente entrega esse diagnóstico.

**ec · dificil · R1 correta · R2 correta · atalho** Em um FPSO remoto, os relatórios mostram que o tempo das atividades de reparo permaneceu praticamente estável após uma revisão de procedimentos. Mesmo assim, o MTTR do KPI subiu no período em que houve atrasos frequentes de embarque e de acesso à área, e a equipe passou a contar da falha até o retorno ao serviço. O que realmente está elevando o indicador?

- Referência: A inclusão de esperas logísticas e de acesso no MTTR, não uma piora da mantenabilidade.
- R1: O aumento do MTTR ocorre porque o período de medição inclui o tempo total desde a falha até o restabelecimento, incluindo atrasos de embarque e acesso, o que amplia o tempo de reparo efetivo.
- R2: O MTTR subiu porque o KPI passou a incluir tempos fora do reparo: atrasos de embarque e de acesso/retorno à área (esperas por pessoal, materiais, liberação operacional e condições seguras). O trabalho em si ficou estável; o indicador capturou o tempo total de indisponibilidade até o retorno ao serviço.
- Desenho: atraente = Piora da mantenabilidade do sistema. | descarta = O tempo das atividades de reparo permaneceu praticamente estável, enquanto houve atrasos de embarque e acesso e a contagem passou da falha ao retorno ao serviço. | passo oculto = Se o tempo das atividades de reparo ficou estável, a alta do KPI veio de tempos fora do reparo que passaram a entrar no intervalo medido.
- Juiz: A referência é válida e o aumento decorre de o MTTR ter passado a incluir esperas logísticas e de acesso até o retorno ao serviço, exatamente o que ambos apontam, e isso é quase uma releitura do enunciado.

**ec · dificil · R1 correta · R2 correta · atalho** Após aumentar o número de equipes de manutenção, a indisponibilidade quase não mudou. Nos registros dos eventos, o tempo de reparo executado pela equipe diminuiu, mas a maior parte do tempo parado permaneceu em espera por acesso à área, sobressalente, liberação e mobilização logística. Que gargalo efetivo ainda limita o retorno operacional?

- Referência: A espera por acesso, sobressalente, liberação e logística; a capacidade das equipes não é o gargalo.
- R1: O gargalo efetivo é o tempo de espera para acesso, liberação e logística, que limita o retorno operacional mesmo com equipes maiores e reparos mais rápidos.
- R2: O gargalo efetivo é o tempo de espera operacional: não há limitação principal de capacidade de reparo, mas de acessos e prontidão do sistema (liberação do acesso/segurança, disponibilidade de sobressalentes e logística/ mobilização para retomar o trabalho).
- Desenho: atraente = A capacidade das equipes de manutenção. | descarta = O tempo de reparo da equipe diminuiu, mas a maior parte do tempo parado continuou em espera por acesso, sobressalente, liberação e logística. | passo oculto = A parcela dominante da indisponibilidade está fora da execução do reparo; logo, o gargalo não é a capacidade das equipes.
- Juiz: R1 e R2 acertaram ao identificar que o gargalo segue nos tempos de espera por acesso, liberação, sobressalentes e logística, e não na capacidade das equipes; a referência é válida e há atalho genérico porque o enunciado já explicita esses tempos como a parcela dominante da parada.

**ec · dificil · R1 parcial · R2 correta · ref. inválida · atalho** O óleo e o gás seguem dentro das especificações, o separador trabalha na eficiência esperada e não há indício de limitação em compressor ou bomba de hidrocarbonetos. Ainda assim, quando aumenta a fração aquosa do fluido de entrada, a unidade precisa cortar a vazão total; a reinjeção está indisponível e o tratamento para descarte já opera no limite legal. Que sistema está efetivamente limitando a capacidade da unidade?

- Referência: A malha de água produzida; faltou capacidade para tratar e dar destino à fase aquosa.
- R1: Sistema de separação de água, que não consegue processar o aumento da fração aquosa, limitando a vazão total da unidade.
- R2: O sistema que limita a capacidade é o de tratamento/disposição do efluente (água produzida): quando aumenta a fração aquosa, cresce a carga de água a tratar e o skid já opera no limite legal; sem reinjeção disponível, a restrição efetiva passa a ser a vazão máx. de descarte/tratamento, não o separador/compressão/bombas.
- Desenho: atraente = O separador primário. | descarta = Óleo e gás permanecem especificados, o separador está eficiente e os destinos da fase aquosa estão indisponível ou no limite. | passo oculto = O aumento da fração aquosa eleva a demanda de tratamento e destino da água até esgotar essa capacidade.
- Juiz: O limitante real era a malha de tratamento e destino da água produzida, não o separador; por isso R2 acerta, R1 confunde com separação, e o enunciado praticamente entrega a restrição, tornando a referência inválida e o item um atalho.

**ec · dificil · R1 correta · R2 correta · atalho** Após ampliar a capacidade do compressor apontado como limitante, a FPSO manteve a mesma vazão total. O compressor passou a operar com folga, sem saturar potência nem vazão, mas agora o nível do separador a jusante atinge o limite antes dos demais parâmetros. Que fenômeno de gargalo esse resultado indica?

- Referência: Deslocamento do gargalo para o separador a jusante.
- R1: Indica um fenômeno de restrição de fluxo no separador, onde a capacidade de processamento do equipamento limita a vazão, mesmo com o compressor operando em condições favoráveis.
- R2: Indica um novo gargalo a jusante: capacidade limitada do sistema de separação/remoção de líquido no separador (por exemplo, drenagem/bombas), fazendo o nível do separador atingir o limite antes de saturar potência ou vazão do compressor.
- Desenho: atraente = O compressor ampliado não entregou a capacidade prometida. | descarta = O compressor passou a operar com folga, sem saturar potência nem vazão, enquanto o primeiro limite agora aparece no separador a jusante. | passo oculto = Se o compressor ganhou folga e a vazão total não aumentou, a limitação original foi aliviada; como outro limite apareceu a jusante, a restrição migrou no sistema.
- Juiz: O elemento decisivo é o deslocamento do gargalo do compressor para o separador a jusante, reconhecido por ambos, e há atalho porque o próprio enunciado já aponta o nível do separador como novo limitante.

**ec · dificil · R1 incorreta · R2 correta · atalho** Em um FPSO, a queda de produção levou a equipe a propor apenas reduzir a carga de processamento. Contudo, inspeção confirmou falha em elemento de ancoragem, e o reparo exige intervenção de integridade. O conceito da unidade permite afastamento controlado do ponto de operação e posterior retorno ao serviço. Depois da parada da produção, que sequência operacional específica deve ser prevista?

- Referência: Desconexão e posterior reconexão da unidade, para viabilizar a intervenção de integridade.
- R1: Realizar lockdown, conduzir inspeção detalhada, preparar reparo, executar intervenção de integridade, realizar testes de avaliação, retomar operações controladamente, e monitorar o sistema durante o retorno.
- R2: Sequência sugerida: (1) parar produção e despressurizar/segregar sistemas; (2) executar afastamento controlado do ponto de ancoragem (proa/arranjo com janela operacional); (3) imobilizar e bloquear integridade do posicionamento; (4) realizar intervenção e inspeção do elemento; (5) recuperar ancoragem/posicionamento e validar; (6) retomar com partida gradual e testes.
- Desenho: atraente = Reduzir a carga de processamento. | descarta = A inspeção confirmou falha em elemento de ancoragem, e o reparo exige intervenção de integridade. | passo oculto = Inferir que a falha de ancoragem exige intervenção de integridade com a produção interrompida e, pelo conceito da unidade, isso leva à manobra adicional.
- Juiz: R2 é correta por descrever a sequência de desconexão/afastamento controlado seguida de intervenção e reconexão/retorno, enquanto R1 omite justamente a desconexão e reconexão; a referência é válida e o enunciado praticamente entrega essa sequência.

**ec · dificil · R1 correta · R2 correta · atalho** Dois FPSOs recebem fluido do pré-sal na mesma pressão e com os mesmos teores de CO2 e H2S. Em um, a produção segue sem restrição relevante; no outro, a mesma composição passou a impor limite após anos de operação. Ensaios confirmam que a composição não mudou e não houve nova exigência legal externa. Que fator explica essa diferença entre as unidades?

- Referência: Projeto, condição dos ativos e estratégia operacional da unidade.
- R1: Diferenças na integridade ou condições do sistema de processamento, como corrosão, incrustações ou falhas na vedação, podem aumentar a sensibilidade ao CO2 e H2S, limitando a produção mesmo com composição similar.
- R2: A diferença decorre de condições secundárias que mudam com o tempo na unidade: variação de água produzida/química (pH, cloretos, salinidade), eficiência de inibidores e formação de incrustações/produtos de corrosão. Mesmo com mesma composição de CO2/H2S e pressão, a taxa de corrosão/entupimento aumenta e passa a limitar a operação após anos.
- Desenho: atraente = Maior teor de CO2 e H2S no fluido. | descarta = Os dois FPSOs recebem a mesma composição na mesma pressão, e os ensaios confirmam que isso não mudou. | passo oculto = Como composição e pressão são as mesmas e não houve mudança externa, o limitante decorre de fatores próprios da unidade, não do fluido em si.
- Juiz: A resposta correta é que o limite é dependente do projeto, condição dos ativos e estratégia operacional da unidade, não da composição do fluido em si, e ambos remetem a essa dependência ampla, que admite resposta genérica.

**ec · dificil · R1 correta · R2 correta · atalho** Após semanas de queda de vazão bruta e mudança de pressão observada no poço, a coluna de produção é aberta e encontra-se depósito mineral por precipitação reduzindo a seção de escoamento. A equipe propõe aumentar a dosagem de inibidor de incrustação para recuperar a capacidade imediatamente. Com esse quadro, o que é necessário para recuperar a capacidade?

- Referência: Remoção do depósito, com avaliação da integridade do equipamento.
- R1: É necessário realizar limpeza física, como window washing ou scraping, juntamente com o aumento controlado da dosagem de inibidores para prevenir futuras incrustações.
- R2: Aumentar apenas o inibidor geralmente não recupera a seção já incrustada. Para recuperar a capacidade é necessário intervenção para dissolver/remover a incrustação (acidização/“washing” compatível com o mineral) e depois reestabelecer proteção com tratamento inibidor (squeeze/batch) e monitorar pressões/vazão.
- Desenho: atraente = Aumentar a dosagem de inibidor de incrustação. | descarta = A coluna foi aberta e havia depósito mineral por precipitação reduzindo a seção de escoamento. | passo oculto = O depósito por precipitação na coluna caracteriza obstrução por incrustação já formada; como o inibidor só previne nova precipitação, ele não recupera a capacidade perdida.
- Juiz: A referência é válida e o elemento decisivo é que a capacidade só se recupera com remoção/dissolução da incrustação já formada, como ambos disseram, sendo um caso com atalho por associação direta ao depósito bloqueando a seção.

**ec · dificil · R1 correta · R2 correta · atalho** Dois FPSOs têm a mesma designação. No primeiro, medições essenciais estão intermitentes e a separação óleo-água perdeu eficiência; no segundo, a instrumentação é confiável e a separação permanece estável. Um generalista poderia tratá-los como equivalentes pela designação. Ao estimar a capacidade de resposta à mesma perturbação, qual referência técnica deve prevalecer?

- Referência: O arranjo real da unidade, porque a designação isolada não determina sua capacidade de resposta.
- R1: A referência técnica que deve prevalecer é a performance real do sistema, especialmente medições essenciais e eficiência da separação, pois refletem a capacidade de resposta à perturbação.
- R2: Deve prevalecer a referência técnica baseada em dados verificados de desempenho/funcionamento (instrumentação validada e eficiência real de separação), não a designação do FPSO. Use curvas/funções de resposta obtidas do sistema instrumentado e do “as-built/as-operated” (modelo dinâmico e parâmetros calibrados), considerando a perda de eficiência no 1º.
- Desenho: atraente = A designação da instalação. | descarta = No primeiro há medições intermitentes e perda de eficiência na separação; no segundo, esses pontos permanecem estáveis. | passo oculto = As condições do primeiro FPSO reduzem observabilidade e margem operacional, alterando sua capacidade efetiva de responder à perturbação.
- Juiz: O que deve prevalecer é a condição/arranjo real as-built ou as-operated da unidade, não a designação, ideia atendida por ambos ao priorizar desempenho e instrumentação reais; a referência é válida, embora o contraste do enunciado facilite uma resposta genérica.

**ec · dificil · R1 correta · R2 correta · atalho** Num FPSO maduro, estudos de risco sofisticados continuam sendo executados, e os perigos são identificados nas análises. Mesmo assim, após alterações operacionais, a atualização documental atrasa, dúvidas sobre parâmetros de projeto levam horas para ser esclarecidas e a validação formal das mudanças trava. Que deficiência mais específica explica esse padrão?

- Referência: Estrutura organizacional incapaz de sustentar gestão de mudanças, atualização documental e esclarecimento técnico rápido.
- R1: Falta de integração e celeridade na atualização documental, indicando deficiência na gestão de mudanças e controle de configuração.
- R2: A deficiência mais provável é fraca Governança de Mudanças (MOC): falta de rastreabilidade e atualização documental imediata pós-alteração, com lacunas no controle de versões/parâmetros e na validação formal (aprovações, critérios e comunicação), causando retrabalho e atrasos no esclarecimento.
- Desenho: atraente = Falta de técnicas de análise de risco. | descarta = Os estudos de risco continuam sendo executados, e os perigos são identificados nas análises. | passo oculto = Como as análises existem e os perigos são identificados, a falha está em sustentar operacionalmente atualização documental, gestão de mudanças e esclarecimento técnico.
- Juiz: Ambos identificam corretamente a deficiência de gestão de mudanças/controle de configuração sustentada pela organização, que explica atraso documental, dúvida sobre parâmetros e travamento da validação formal; a referência é válida e há atalho genérico porque os sintomas descritos apontam quase diretamente para MOC.

**ec · dificil · R1 correta · R2 parcial · atalho** Em paradas anteriores do FPSO, os arquivos ficaram completos e acessíveis, com objetivo, escopo, prazos, efetivo, custos, acidentes, desvios e lições; o monitoramento foi sistemático. Mesmo assim, na intervenção seguinte repetiram-se erros de alocação de suporte, e as lições do ciclo anterior foram apenas transcritas apesar de mudanças no escopo e nos desvios observados. O que faltou no processo?

- Referência: Análise crítica real do conteúdo consolidado.
- R1: Falta uma análise de aprendizado contínuo e atualização das lições, ajustando o plano conforme mudanças no escopo e desvios, para evitar repetição de erros.
- R2: Faltou transformar lições em controles operacionais: gestão de mudanças e revalidação do plano (escopo/desvios) com critérios de alocação de suporte, atualização de procedimentos/SOPs, verificação de aderência antes da intervenção e responsabilização/monitoramento de implementação — não apenas transcrição documental.
- Desenho: atraente = Disciplina documental. | descarta = Os arquivos estavam completos e acessíveis, e o monitoramento já era sistemático. | passo oculto = Inferir que a disciplina documental e o monitoramento já existiam; como as lições foram só transcritas e os erros se repetiram, faltou transformar registro em aprendizado por análise crítica.
- Juiz: R1 reproduz o elemento decisivo — faltou análise crítica real das lições e dados consolidados para replanejar — enquanto R2 desloca o foco para implementação de controles e gestão de mudanças; a referência é válida e há atalho genérico porque 'analisar criticamente as lições' sai quase diretamente do enunciado.

**ec · dificil · R1 correta · R2 correta · atalho** Uma equipe herdou de outras FPSOs um ranking em que medição recebe prioridade máxima e pretende adotá-lo sem ajuste. Na unidade atual, a configuração do processo, o regime operacional, a manutenção, as barreiras e o contexto organizacional diferem dos casos do histórico. Ao fechar a seleção dos sistemas críticos, que base deve prevalecer?

- Referência: O exame específico das funções e vulnerabilidades da própria unidade, usando o histórico apenas para informar a análise.
- R1: A base de referência deve ser o sistema atual da unidade, considerando suas configurações, operações e contexto, para garantir a relevância e eficácia na seleção dos sistemas críticos.
- R2: Deve prevalecer a base atual: uma reavaliação/local de criticidade e seleção de sistemas críticos com base na análise de risco do processo (funções de segurança, barreiras, modos de falha, criticidade e integridade), considerando configuração, regime operacional, manutenção e contexto organizacional atuais, não o ranking herdado sem ajuste.
- Desenho: atraente = O ranking histórico herdado, mantendo medição como prioridade máxima. | descarta = Na unidade atual, a configuração do processo, o regime operacional, a manutenção, as barreiras e o contexto organizacional diferem dos casos do histórico. | passo oculto = As diferenças de configuração, regime, manutenção, barreiras e contexto alteram frequência e gravidade, invalidando a transferência direta do ranking histórico.
- Juiz: Ambos dizem corretamente que deve prevalecer a análise específica das funções, vulnerabilidades e criticidade da própria unidade, usando o histórico herdado no máximo como insumo, e a referência é válida embora bastante genérica.

**ec · dificil · R1 correta · R2 correta** Em um FPSO, uma barreira crítica continua cadastrada como disponível e não houve retirada física do equipamento. Porém, os testes periódicos estão vencidos, a manutenção preventiva foi adiada e a análise de risco usada no plano ainda assume premissas que já não refletem a operação atual. A equipe quer manter o mesmo enquadramento de risco apenas porque a barreira segue no sistema. Que condição dessa barreira torna essa decisão inadequada?

- Referência: O estado real de desempenho da barreira, porque sua funcionalidade pode não sustentar o risco assumido.
- R1: A condição de que os testes periódicos estejam vencidos e a manutenção preventiva esteja adiada compromete a confiabilidade da barreira, tornando inadequada sua manutenção no mesmo enquadramento de risco, pois a ausência de testes atualizados pode ocultar falhas.
- R2: Inadequada porque a barreira perdeu evidência de eficácia: testes periódicos vencidos e manutenção preventiva adiada, além de premissas do estudo de risco não refletirem a operação atual. Assim, a barreira não pode ser considerada funcional/confiável no enquadramento de risco.
- Desenho: atraente = A existência documental da barreira como disponível. | descarta = Os testes periódicos estão vencidos, a manutenção preventiva foi adiada e as premissas da análise de risco já não refletem a operação atual. | passo oculto = Testes vencidos, manutenção adiada e premissas antigas indicam que a funcionalidade da barreira não está demonstrada.
- Juiz: Ambos reconheceram que o enquadramento depende do estado real e da evidência de desempenho/funcionalidade da barreira, não do cadastro no sistema, e isso exige conhecimento específico.

**ec · dificil · R1 incorreta · R2 correta** Dois itens críticos de mesma função em um FPSO têm criticidade equivalente. O item A tem probabilidade de falha um pouco maior, mas o reparo usa sobressalente embarcado e equipe de bordo em poucas horas. O item B tem probabilidade de falha um pouco menor, porém só volta com especialista externo, peça não embarcada e mobilização dependente do tempo. Se apenas uma intervenção preventiva puder ser antecipada, qual item deve ser priorizado?

- Referência: O item B, porque o suporte de manutenção piora a disponibilidade e amplia o impacto da indisponibilidade.
- R1: O item A deve ser priorizado, pois sua intervenção preventiva pode ser antecipada rapidamente com equipe de bordo e sobressalente, reduzindo o risco de falha.
- R2: Priorize o item B. Mesmo com menor probabilidade, sua indisponibilidade esperada é maior por depender de mobilização e peça/equipe externa, elevando o risco operacional (consequência + tempo de indisponibilidade) em relação ao item A, reparável em poucas horas com sobressalente embarcado.
- Desenho: atraente = O item A, por ter probabilidade de falha maior. | descarta = O item B só volta com especialista externo, peça não embarcada e mobilização dependente do tempo. | passo oculto = A dependência de especialista, peça externa e mobilização condicionada ao tempo reduz o suporte de manutenção, alonga a restauração e derruba a disponibilidade esperada.
- Juiz: Só R2 reconhece que, com criticidades equivalentes, a pior suportabilidade de manutenção do item B aumenta a indisponibilidade esperada e por isso ele deve ser priorizado, enquanto R1 privilegia apenas a maior probabilidade de falha do item A.

**ec · dificil · R1 incorreta · R2 parcial** Em uma FPSO de alta produção, uma falha não percebida evolui até parada compulsória. O reparo exige especialistas e materiais trazidos fora do plano e, após o retorno, a unidade segue algum tempo com capacidade limitada até a solução definitiva. A gerência quer comparar esse evento com um investimento preventivo usando só o custo do reparo e a receita perdida nos dias totalmente parados. Que parcela final do custo está ficando de fora?

- Referência: O efeito acumulado de indisponibilidade, correções emergenciais e restrições operacionais.
- R1: A manutenção preditiva ou preventiva, incluindo custos de inspeção e monitoramento, além de contratos de suporte tecno-operacional que podem reduzir a frequência e o impacto de falhas.
- R2: Fica de fora a perda de receita (ou ganho) durante o período em que a FPSO retorna operando com capacidade limitada, além de quaisquer custos de ramp-up/recuperação e restrições operacionais pós-parada.
- Desenho: atraente = O custo da mobilização extraordinária. | descarta = Após o retorno, a unidade segue algum tempo com capacidade limitada até a solução definitiva. | passo oculto = As observações indicam que o evento gerou custo além do reparo e da parada total, inclusive resposta emergencial e perda após a retomada.
- Juiz: O decisivo era notar que o custo do evento excede reparo mais dias totalmente parados, incluindo o efeito acumulado de indisponibilidade e restrições operacionais, por isso R2 fica parcial ao cobrir só a perda durante capacidade limitada e R1 erra ao responder com gasto preventivo; a referência é válida e não há atalho genérico.

**ec · dificil · R1 parcial · R2 correta** Modo A tem severidade 10, ocorrência 2 e detecção 4, com consequência tratada internamente como crítica. Modo B tem severidade 4, ocorrência 5 e detecção 4. A planilha mostrou o mesmo produto para ambos, e o gestor concluiu que o empate basta para encerrar a discussão. Qual limitação do índice torna essa conclusão errada?

- Referência: Combinações distintas podem gerar o mesmo índice, e consequências críticas ainda exigem análise individual.
- R1: O índice de risco não considera a crítica da consequência, podendo subestimar o impacto de Modo A ao empate, levando a uma conclusão inadequada.
- R2: A limitação é que o índice (tipo RPN) usa produto multiplicativo e trata severidade, ocorrência e detecção com “pesos” iguais e escala linear. Assim, valores diferentes podem empatar (mesmo RPN) apesar de severidade muito maior em um modo, mascarando risco real.
- Desenho: atraente = Nenhuma limitação; o empate permite encerrar a priorização só pelo número. | descarta = O modo A tem consequência tratada internamente como crítica. | passo oculto = Perceber que 10×2×4 e 4×5×4 geram o mesmo índice e que esse empate não elimina a necessidade de examinar separadamente a consequência crítica.
- Juiz: A limitação é que combinações diferentes de severidade/ocorrência/detecção podem dar o mesmo índice e mascarar um modo crítico que ainda requer análise individual; R1 capta isso só parcialmente ao focar na crítica da consequência e R2 identifica corretamente o empate por combinações distintas do produto.

**ec · dificil · R1 correta · R2 correta · atalho** Na seleção de químico para tratar água produzida de um FPSO, três frascos receberam a mesma temperatura, mistura, dose e tempo. A amostra representa uma emulsão óleo-em-água. O produto A formou rapidamente uma camada de óleo separada e interface nítida, mas a fase aquosa ficou turva; o B deixou a fase aquosa mais clara; o C pouco mudou frente ao branco. Qual produto deve seguir para validação operacional?

- Referência: O produto B, porque em óleo-em-água o critério é a clarificação da fase aquosa.
- R1: Produto B, pois proporcionou a maior claridade na fase aquosa, indicando melhor separação óleo-água.
- R2: O produto B. A formou separação de óleo, mas a água permaneceu turva (falha de clarificação). B reduziu a turbidez e melhorou a fase aquosa; C pouco diferiu do branco. Logo, B é o mais adequado para validação operacional.
- Desenho: atraente = Produto A, pela separação mais visível e pela interface nítida. | descarta = A amostra é óleo-em-água e, no A, a fase aquosa permaneceu turva. | passo oculto = Inferir que, por ser uma emulsão óleo-em-água, o desempenho relevante no bottle test é a clarificação da fase aquosa.
- Juiz: Em emulsão óleo-em-água o critério decisivo é a clarificação da fase aquosa, por isso B está correto em R1 e R2, e há atalho porque o enunciado já informa diretamente que B deixou a água mais clara.

**ec · dificil · R1 parcial · R2 correta** Em um FPSO, a água produzida tratada ficou fora da especificação para reinjeção, enquanto o óleo de exportação permaneceu dentro da meta de teor de água. Na corrente problemática, a microscopia mostra gotículas de óleo dispersas na fase contínua aquosa. Um operador sugere reforçar o tratamento típico de desidratação do petróleo. Que função química deve ser priorizada?

- Referência: Clarificante de água; promove a aglomeração das gotículas de óleo e facilita a separação de fases.
- R1: A priorização deve ser de um desmobilizante, que auxilia na coalescência das gotículas de óleo, promovendo sua separação da água na fase de desidratação.
- R2: Priorizar um desemulsificante/coagulante para quebrar emulsões óleo-em-água (gota de óleo dispersa na fase aquosa), promovendo coalescência e remoção em DAF/filtração—não apenas desidratação do óleo exportado.
- Desenho: atraente = Desemulsificante voltado à desidratação do petróleo, para remover água residual do óleo. | descarta = O óleo de exportação já atende a meta de teor de água, e a microscopia mostra gotículas de óleo na fase contínua aquosa. | passo oculto = Identificar que a corrente problemática é uma emulsão óleo-em-água no tratamento de água produzida e que o alvo é reduzir óleo na água para reinjeção.
- Juiz: A referência é válida e o decisivo é priorizar a química do lado aquoso para coalescer/remover gotas de óleo em emulsão óleo-em-água, de modo que R2 acerta e R1 fica parcial por remeter à desidratação do petróleo, exigindo distinguir a fase contínua e a função química adequada.

**ec · dificil · R1 correta · R2 correta · atalho** Um desemulsificante foi escolhido em ensaio com salmoura padrão. No FPSO, a salmoura mudou, o pH caiu, a salinidade subiu e a separação piorou; sem alterações mecânicas, um técnico quer manter o produto porque "pH baixo e sal alto sempre ajudam". Como a seleção do químico deve ser refeita?

- Referência: Comparando produtos nas condições representativas do sistema atual, porque pH e salinidade não garantem melhor separação.
- R1: Reavalie o desemulsificante com base em testes de laboratório considerando as novas condições de salinidade, pH e composição da salmoura para garantir eficácia na separação.
- R2: Refaça a seleção requalificando o desemulsificante nas novas condições do FPSO: mesma faixa de pH, salinidade e composição iônica (Ca/Mg/Na/SO4), temperatura e química da água. Faça ensaios de bancada (jar/BS&W, tempo/ODT) e ajuste dose. Selecione produto com maior taxa de quebra e menor concentração, considerando compatibilidade com processo.
- Desenho: atraente = Manter o produto atual, assumindo que pH mais baixo e salinidade maior já favorecem a separação. | descarta = A separação piorou justamente depois de o pH cair e a salinidade subir. | passo oculto = A mudança de salmoura alterou a interface e a resposta ao produto passou a depender da formulação e do fluido atuais.
- Juiz: Ambos acertam ao exigir requalificação da seleção com testes representativos das condições atuais do sistema, em vez de assumir que pH baixo e salinidade alta sempre ajudam, e a referência é válida embora permita um atalho prudencial.

**ec · dificil · R1 parcial · R2 correta · atalho** O arraste de líquido na saída de gás aumentou em um separador. A equipe suspeitou de excesso de vazão ou problema de internos, mas vazão, regime de escoamento, internos e controle operacional permaneceram inalterados. O fluido de entrada passou a conter mais espécies de superfície ativas e impurezas, e observou-se espuma persistente. Que causa específica no fluido explica a perda de desempenho?

- Referência: Estabilização do filme líquido da espuma por espécies de superfície ativas e impurezas presentes no fluido.
- R1: A presença de mais espécies de superfície ativas e impurezas aumenta a formação de espuma, reduz a eficiência de separação, elevando o arraste de líquido na saída de gás.
- R2: O aumento de espécies de superfície ativas (tensoativos/contaminantes espumantes) no gás/liquido de entrada elevou a formação e estabilidade de espuma persistente, aumentando arraste de líquido na saída e reduzindo o desempenho do separador por carryover de gotículas.
- Desenho: atraente = Excesso de vazão de gás ou problema nos internos do vaso. | descarta = Vazão, regime de escoamento, internos e controle operacional permaneceram inalterados. | passo oculto = As mudanças no fluido estabilizam o filme líquido, mantêm a espuma persistente e assim reduzem a área livre de escoamento do gás.
- Juiz: R1 foi parcial por falar genericamente em mais espuma, enquanto R2 acertou o mecanismo específico de estabilização da espuma por espécies de superfície ativas e impurezas; a referência é válida e há atalho por associação direta porque o enunciado já traz surfactantes, impurezas e espuma persistente.

**ec · dificil · R1 correta · R2 parcial · ref. inválida · atalho** Após mudança na composição do fluido, com maior teor de sais e sólidos, um separador passa a apresentar espuma persistente. O mesmo antiespumante comercial permanece em uso. A dose foi elevada em etapas: houve leve melhora no início, mas depois não apareceu ganho adicional. Sem mudança operacional relevante no vaso, que fator técnico explica melhor a perda de desempenho do controle químico?

- Referência: Incompatibilidade do antiespumante com a interface gás-líquido atual, reduzindo seu espalhamento, penetração ou dispersão até o filme estabilizante.
- R1: A maior concentração de sais e sólidos alterou as propriedades físicas do fluido, reduzindo a eficácia do antiespumante devido à mudança na interface entre fases, dificultando o controle da espuma.
- R2: Com o aumento de sais e sólidos, o antiespumante é progressivamente adsorvido/retido na fase particulada e pode ser desativado por interações com íons (salting-out, formação de filmes mais estáveis). Assim, sua concentração efetiva na interface espuma-líquido não cresce com a dose, levando à perda de desempenho.
- Desenho: atraente = Dose insuficiente de antiespumante. | descarta = A dose foi elevada em etapas e, após leve melhora inicial, não houve ganho adicional. | passo oculto = A mudança de sais e sólidos alterou a interface gás-líquido e reduziu o contato eficaz do produto com o filme; o platô mostra que não é apenas falta de dose.
- Juiz: Embora a referência privilegie a perda de compatibilidade do antiespumante com a interface alterada — que R1 capta e R2 só tangencia ao trocar para adsorção/desativação por sólidos e íons — o enunciado também admite outros mecanismos plausíveis com sais e sólidos, então a referência não é única e uma explicação genérica sobre mudança de interface já seria aceita.

**ec · dificil · R1 parcial · R2 correta** Dois antiespumantes da mesma classe, com o mesmo princípio ativo e a mesma concentração, tiveram desempenho igual em teste simples de colapso. No separador do FPSO, porém, sob maior cisalhamento e menor tempo de residência, o Produto A manteve baixa espuma residual e não afetou a separação óleo-água; o B perdeu efeito. A equipe atribuiu a diferença ao princípio ativo. Que parte da formulação explica tecnicamente a vantagem do Produto A?

- Referência: O veículo com seus coadjuvantes, por governarem dispersão, penetração no filme e persistência do efeito.
- R1: Diferenças na estabilidade da emulsão e na dispersão micelar, influenciadas por fatores como surfactantes adicionais, permitem ao Produto A manter sua eficácia sob condições de maior cisalhamento.
- R2: Como o princípio ativo e a concentração são iguais, a diferença em separador (maior cisalhamento/menor tempo) costuma vir dos excipientes: veículo/solvente e agentes dispersantes que controlam a taxa de migração/adsorção na interface e a quebra rápida do filme de espuma. Em geral, o “carrier” e dispersantes explicam a vantagem do A.
- Desenho: atraente = O princípio ativo. | descarta = Os dois produtos têm o mesmo princípio ativo e a mesma concentração. | passo oculto = Como princípio ativo e concentração são iguais, a diferença vem do restante da formulação; sob maior cisalhamento e menor tempo de residência, isso altera dispersão e persistência.
- Juiz: Como ativo e concentração são iguais, a vantagem vem da formulação inerte — veículo/carrier e coadjuvantes de dispersão, penetração e persistência —, o que R2 explicita e R1 só aborda parcialmente ao falar genericamente de surfactantes e dispersão.

**ec · dificil · R1 parcial · R2 parcial** Em um separador, a espuma passou a persistir e o arraste de líquido no gás aumentou logo após a injeção do antiespumante ser movida para a descarga de uma bomba de recirculação. Salinidade, corte de água, temperatura e teor de sólidos ficaram estáveis, e elevar a dose não mudou o quadro. Que fator operacional explica mais especificamente essa perda de desempenho?

- Referência: Cisalhamento excessivo no ponto de injeção, que dispersa o produto de modo desfavorável.
- R1: A introdução da bomba de recirculação provavelmente alterou o fluxo e a distribuição do antiespumante, causando uma resposta ineficaz na eliminação da espuma devido a mudanças na mistura ou na passagem do fluido.
- R2: O principal fator é a mudança do ponto de injeção: ao colocar o antiespumante na descarga da bomba de recirculação, perde-se dispersão e/ou tempo de contato adequado com a interface espuma no separador, então o produto não chega eficazmente à fase que gera a espuma, mesmo com dose maior.
- Desenho: atraente = Dose insuficiente do antiespumante. | descarta = A dose foi elevada sem melhora, e o problema começou após a mudança do ponto de injeção, com propriedades do fluido estáveis. | passo oculto = Mover a injeção para a descarga da bomba elevou o cisalhamento; isso dispersou o antiespumante de forma desfavorável e reduziu sua penetração no filme espumante.
- Juiz: A referência é válida porque o fator específico pedido é o cisalhamento excessivo no novo ponto de injeção, mas R1 e R2 ficaram apenas em efeitos genéricos da mudança de ponto/mistura sem cravar esse mecanismo, e não há atalho genérico.

**ec · dificil · R1 correta · R2 parcial** Em um trem de água produzida com flotação por ar dissolvido, a vazão de recirculação e a geração de microbolhas permaneceram normais. Após trocar por um químico de caráter surfactante que alcança o sistema óleo/água, o efluente passou a sair com mais óleo e a microscopia mostrou gotas mais finas permanecendo dispersas por mais tempo. Muitos suspeitam da flotação. Que mecanismo explica melhor a piora?

- Referência: Estabilização da emulsão óleo em água pelo surfactante na interface, dificultando a captura e a separação.
- R1: A introdução do surfactante aumenta a estabilidade das microgotas de óleo, dificultando sua coalescência e separação, levando a uma menor eficiência na flotação e aumento do óleo na saída.
- R2: O surfactante altera a hidrofobicidade e estabiliza a emulsão: reduz a tensão interfacial, adsorve na gota e impede coalescência/levantamento, mantendo microgotas dispersas. Assim, a probabilidade de captura na bolha e a floculação aumentam e a remoção por flotação piora, mesmo com recirculação e microbolhas normais.
- Desenho: atraente = Falha da flotação por ar dissolvido. | descarta = A vazão de recirculação e a geração de microbolhas permaneceram normais após a troca do químico. | passo oculto = Inferir que a troca do surfactante tornou a interface mais estável, mantendo gotas menores e mais persistentes; com a flotação normal, a perda está na condição da dispersão.
- Juiz: O mecanismo decisivo é a estabilização da emulsão óleo em água pelo surfactante na interface, dificultando coalescência e captura na flotação; R1 expressa isso, enquanto R2 mistura esse acerto com o erro relevante de dizer que a captura/floculação aumentam.

**ec · dificil · R1 correta · R2 correta · atalho** Um trem tratava certa água por flotação sem aditivo e atendia o descarte. Depois, a vazão aumentou, mas a carga de óleo de entrada e as condições de geração de bolhas permaneceram as mesmas; ainda assim a remoção piorou. A reação mais proposta foi iniciar coagulante. Pelo mecanismo do sistema, que fator passou a limitar a captura?

- Referência: Menor frequência de colisão, causada pela piora do regime hidráulico e do tempo de contato com a maior vazão.
- R1: O aumento da vazão diminuiu a eficiência de flotação, limitando a captura de óleo devido à redução do contato entre bolhas e partículas, causando menor adesão e coalescência.
- R2: Com o aumento da vazão mantendo a geração de bolhas e a carga de óleo, o que limita a captura passa a ser o tempo de contato (residência) e a probabilidade de colisão/adesão óleo–bolha, reduzidas pelo aumento da carga hidráulica/“overflow rate” do flotador.
- Desenho: atraente = Necessidade de iniciar coagulante. | descarta = A mesma água já atendia sem aditivo, e a carga de óleo e a geração de bolhas permaneceram as mesmas. | passo oculto = Inferir que o aumento de vazão alterou o regime hidráulico e reduziu o tempo de contato, diminuindo as colisões bolha-gota/floco.
- Juiz: O limitante passou a ser o menor contato/colisão óleo–bolha pela maior carga hidráulica e menor residência, exatamente o que ambos apontam, e isso é inferível quase diretamente do aumento de vazão mantendo o restante constante.

**ec · dificil · R1 correta · R2 correta · atalho** No mesmo fluido e equipamento, o ponto de injeção já garante boa mistura e tempo antes da flotação. Após elevar a dosagem, o TOG sobe, o residual orgânico também e os flocos observados quebram-se facilmente. Que condição de dosagem explica esse conjunto?

- Referência: Superdosagem, que pode reestabilizar dispersões, elevar o residual orgânico e gerar flocos frágeis pouco capturáveis.
- R1: A dose de injeção excessiva causa saturação, aumentando o TOG, residual orgânico, e quebrando os flocos devido à sobrecarrega de agentes químico-organizantes, prejudicando a formação e estabilidade dos flocos.
- R2: Superdosagem do polieletrólito/surfactante: com excesso, o residual orgânico cresce e ocorre “restabilização”/perda de ponte entre partículas (reversão de carga), gerando flocos mais fracos que se desfazem facilmente e maior TOG antes/depois da flotação.
- Desenho: atraente = Subdosagem. | descarta = Após elevar a dosagem, o residual orgânico também sobe e os flocos observados quebram-se facilmente. | passo oculto = Boa mistura e tempo descartam falha de aplicação; residual orgânico maior e flocos frágeis após aumento de dose indicam que a janela ótima foi ultrapassada.
- Juiz: A referência é válida e o decisivo é identificar superdosagem como causa de restabilização/residual alto e flocos frágeis, o que ambos fazem, embora a resposta possa sair quase diretamente do enunciado.

**ec · dificil · R1 incorreta · R2 correta** Após anos de injeção de água do mar sem dessulfatação, a URS entra em operação e análises confirmam forte queda do sulfato na água agora injetada. Mesmo assim, pouco depois, o H2S nos fluidos produzidos permanece elevado. Sem indício de desvio na qualidade da água tratada, que fator explica essa persistência?

- Referência: Sulfato já introduzido na formação, ainda disponível para as BRS gerarem H2S.
- R1: O H2S pode estar sendo gerado por processos biológicos ou degradação de componentes sulfurados no reservatório, não relacionado à sulfatação da água injetada.
- R2: Persistência do H2S ocorre porque a atividade de bactérias redutoras de sulfato (biomassa/biofilme) já foi “instalada” no reservatório e nas tubulações. Elas continuam reduzindo sulfato residual retido no meio poroso/depósitos e liberando H2S a partir de sulfetos já formados (ex.: FeS).
- Desenho: atraente = Falha da URS na remoção de sulfato. | descarta = análises confirmam forte queda do sulfato na água agora injetada | passo oculto = A queda do sulfato na água injetada mostra que a URS está reduzindo apenas a carga nova; o reservatório ainda pode conter sulfato previamente introduzido.
- Juiz: A referência é válida e o fator decisivo é o sulfato já introduzido na formação, ainda disponível para as BRS gerarem H2S; R2 contempla esse sulfato retido no meio poroso, enquanto R1 desvia para outras fontes não sustentadas pelo quadro.

**ec · dificil · R1 incorreta · R2 correta** Em um arranjo com URS, o anti-incrustante é dosado apenas na água de injeção. A concentração no cabeçote do poço injetor permanece na meta, mas, após o tempo de trânsito previsto, não há traços do produto no poço produtor nem o efeito esperado no processo de produção. O que explica essa falta de proteção no produtor?

- Referência: Adsorção do inibidor na rocha em torno do poço injetor, impedindo que ele alcance o poço produtor.
- R1: O anti-incrustante pode estar sendo inativado ou degradado durante o trânsito, ou a concentração na água de injeção não é suficiente para manter a proteção no poço produtor devido a diluição, ou atividade microbiológica que consome o produto antes de alcançar o produtor.
- R2: Provável “loss” do anti-incrustante durante o transporte no reservatório: adsorção/retensão no meio poroso (e/ou com superfície/escala) e possível degradação química. Assim, embora o cabeçote do injetor mantenha a concentração-alvo, o produto não chega ativo ao poço produtor e não há proteção esperada.
- Desenho: atraente = Dosagem insuficiente do anti-incrustante. | descarta = A concentração no cabeçote do poço injetor permanece na meta e o tempo de trânsito previsto já passou. | passo oculto = Se a concentração no injetor está correta e o produto não aparece no produtor após o trânsito esperado, ele foi retido antes de migrar até a produção.
- Juiz: A adsorção/retensão do anti-incrustante no meio poroso junto ao injetor é o elemento decisivo, ausente em R1 e presente em R2 apesar das hipóteses extras; a referência é válida e não há atalho genérico porque a explicação depende do mecanismo de transporte e retenção no reservatório.

**ec · dificil · R1 parcial · R2 correta** Em uma URS, a água tratada passa a sair em menor quantidade e com pior retenção iônica, embora a composição das correntes de entrada e o ponto de mistura externo permaneçam estáveis. Qual mecanismo interno explica simultaneamente a perda hidráulica e a perda de seletividade?

- Referência: Depósitos nas membranas da URS; eles reduzem o fluxo de água e elevam a passagem de íons.
- R1: O mecanismo é o acúmulo de fouling ou incrustação na mídia de troca iônica, reduzindo a permeabilidade hidráulica e a eficiência de troca, levando à perda de vazão e de seletividade.
- R2: O mecanismo mais provável é o fouling/incrustação interna na membrana (colmatação de poros/espessamento do fouling layer), que aumenta a resistência hidráulica (maior ΔP/menor vazão) e reduz a seletividade ao criar caminhos de menor barreira e alterar o transporte iônico (diminuição da rejeição).
- Desenho: atraente = Alteração da composição das águas ou do local de mistura entre correntes. | descarta = A composição das correntes de entrada e o ponto de mistura externo permanecem estáveis. | passo oculto = Pior retenção iônica implica maior passagem de íons; combinada com menor vazão, essa assinatura aponta para depósitos na membrana.
- Juiz: O acerto exigia apontar depósitos/fouling nas membranas da URS como causa simultânea de menor fluxo e maior passagem iônica, e R1 ficou próximo mas errou o elemento interno ao falar em mídia de troca iônica.

**ec · dificil · R1 incorreta · R2 parcial** Em um FPSO, o teor de oxigênio dissolvido na água antes do ponto de injeção do bissulfito segue no patamar usual, e a vazão da bomba dosadora não mudou. Ainda assim, o residual de oxigênio a jusante aumenta. A solução está sendo mantida por vários dias em tanque com respiro aberto, e o trecho de dosagem que conduz solução diluída começa a mostrar ataque corrosivo. Que causa específica explica melhor esse conjunto?

- Referência: Perda de concentração ativa do bissulfito por armazenamento exposto ao ar; na linha, a solução diluída ainda agrava corrosão pelo baixo pH.
- R1: Acúmulo de oxigênio residual na solução, combinado ao ataque corrosivo na tubulação, devido à presença de oxigênio dissOrdenado que não foi completamente consumido pelo bissulfito, levando à corrosão por oxidação e aumento do residual a jusante.
- R2: A causa mais provável é a reoxidação do bissulfito durante a estocagem em tanque com respiro aberto: o O2 do ar dissolve/oxida o agente redutor antes da dosagem, elevando o residual de oxigênio a jusante e deixando a linha com solução mais “pobre” em redutor, permitindo ataque corrosivo pelo oxigênio.
- Desenho: atraente = Aumento da carga de oxigênio a remover. | descarta = O teor de oxigênio dissolvido na água antes do ponto de injeção segue no patamar usual. | passo oculto = A exposição ao ar reduz a concentração ativa da solução; com a mesma vazão volumétrica, a dosagem efetiva cai e sobra oxigênio residual.
- Juiz: A referência exige a perda de bissulfito ativo por oxidação durante armazenamento em tanque aberto e a corrosão da linha pela acidez da solução diluída; R1 não traz essa causa e R2 acerta a depleção no tanque, mas erra ao atribuir o ataque da linha ao oxigênio em vez do baixo pH.

**ec · dificil · R1 parcial · R2 correta** Em um FPSO, o oxigênio residual após o tratamento químico passou a subir, embora a concentração ativa do bissulfito e as condições de armazenamento tenham sido verificadas como adequadas. Ao mesmo tempo, medições mostraram aumento do oxigênio na saída da desaeração mecânica, sem mudança na dosagem do químico. Que mecanismo explica a perda de desempenho?

- Referência: Subdosagem estequiométrica do bissulfito por aumento da carga de oxigênio sobre a etapa química.
- R1: Possível formação de compostos insolúveis de bissulfito que reduzem sua eficiência, ou entrada de oxigênio externo devido a vazamentos ou falhas na estanqueidade do sistema de desaeração, aumentando a concentração residual apesar da dosagem constante.
- R2: Perda de desempenho por aumento do “carga” de O₂ na corrente: a desaeração mecânica passou a remover menos, elevando o O₂ na saída (ex.: vazamento/entrada de ar, falha de vedação ou queda de eficiência/condição de operação do sistema). O bissulfito não compensa sem aumento de dosagem.
- Desenho: atraente = Degradação da solução de bissulfito por armazenamento inadequado. | descarta = A concentração ativa do bissulfito e as condições de armazenamento foram verificadas como adequadas. | passo oculto = O aumento do oxigênio na saída da etapa mecânica elevou a carga de O2 que chega ao bissulfito; com a mesma dosagem, o balanço estequiométrico tornou-se insuficiente.
- Juiz: O elemento decisivo era a subdosagem estequiométrica do bissulfito causada pelo aumento da carga de O₂ após piora da desaeração mecânica, e R1 só tangenciou isso ao citar possível ingresso extra de oxigênio misturado com hipótese errada.

**ec · dificil · R1 correta · R2 correta** Em água do mar, o conceito original por stripping a gás foi trocado por vácuo porque o gás disponível se tornou inadequado. Depois da mudança, a meta de oxigênio dissolvido segue atendida, a salinidade não mudou e surge tendência nova de incrustação mineral. Qual espécie de precipitado passa a ser teoricamente favorecida por essa troca de processo?

- Referência: Carbonato de cálcio, porque o vácuo pode remover CO2 dissolvido e desequilibrar o sistema carbonato/bicarbonato.
- R1: O precipitado teoricamente favorecido é o carbonato de cálcio (calcita), devido à redução da pressão de carbono e aumento do pH com o uso do vácuo.
- R2: A troca para desgaseificação a vácuo tende a aumentar o pH por redução de CO₂ dissolvido, deslocando o equilíbrio carbonato/bicarbonato. Com isso, fica teoricamente favorecida a precipitação de carbonato de cálcio, principalmente CaCO₃ (calcita/aragonita).
- Desenho: atraente = Sulfato de cálcio. | descarta = A salinidade não mudou; a mudança relevante foi a adoção do vácuo após o gás se tornar inadequado. | passo oculto = A troca para vácuo pode remover CO2 dissolvido e deslocar o equilíbrio CO2/carbonato/bicarbonato.
- Juiz: A referência é válida e ambos identificaram corretamente que o vácuo remove CO2, eleva o pH/desloca o equilíbrio carbonato-bicarbonato e passa a favorecer a precipitação de CaCO3.

**ec · dificil · R1 incorreta · R2 parcial · atalho** Após a troca do biocida em um FPSO, a contagem microbiana na água de injeção cai, mas surgem espuma no separador, piora no tratamento de água produzida e questionamentos de descarte pela jurisdição local. Nenhum outro químico foi alterado, e a equipe quer corrigir só a dosagem porque o novo produto é gerado no local e se decompõe rápido. Que causa única deve ser apontada para esses desvios?

- Referência: Incompatibilidade operacional e toxicológica do biocida e de seus resíduos com o processo e o descarte do FPSO.
- R1: A mudança na dose do biocida, levando a uma eficácia inadequada, pode causar crescimento microbiano residual, formando espuma e afetando o tratamento de água, além de gerar descarte questionável.
- R2: Incompatibilidade do novo biocida com o sistema de separação/tratamento: seus produtos de decomposição (gerados rápido no local) atuam como agentes tensoativos/estabilizantes de emulsão, reduzindo eficácia do antiespumante e causando espuma no separador e piora do tratamento de água produzida.
- Desenho: atraente = Ajuste de dosagem do biocida. | descarta = A contagem microbiana cai, nenhum outro químico mudou e os desvios aparecem ao mesmo tempo em separador, tratamento de água produzida e descarte. | passo oculto = Como a contagem microbiana caiu, o problema principal não é falta de ação biocida; os desvios simultâneos em processo e descarte apontam para efeito cruzado do produto.
- Juiz: R2 fica parcial por reconhecer a incompatibilidade do novo biocida/resíduos com o processo, mas sem abranger a incompatibilidade toxicológica/regulatória no descarte, enquanto R1 erra ao atribuir os desvios apenas à dosagem/eficácia; a referência é válida e há atalho porque 'biocida incompatível com processo e descarte' já atenderia.

**ec · dificil · R1 correta · R2 correta** Após várias bateladas de biocida, as amostras da fase aquosa mostram baixa contagem microbiana. Mesmo assim, sulfeto e corrosão localizada continuam surgindo em filtros, trechos de baixa circulação e partes com depósito interno; produto, concentração e ponto de injeção foram verificados. Que mecanismo explica melhor essa persistência?

- Referência: Biofilme aderido em nichos protegidos, menos acessível ao tratamento químico e à ação do biocida.
- R1: O mecanismo é a formação de biofilmes que protegem micro-organismos, permitindo sua persistência e produção de sulfeto e corrosão, mesmo com baixa contagem microbiana na fase aquosa.
- R2: Persistência por biofilme/consórcios recalcitrantes em depósitos e zonas de baixa circulação. Mesmo com baixa contagem em amostra aquosa, as bactérias/consórcios sésseis e/ou em matriz exopolimérica ficam protegidos do biocida, reativam atividade sulfatante/geradora de sulfeto e recolonizam gradualmente, mantendo corrosão localizada e sulfeto.
- Desenho: atraente = Biocida inadequado ou subdosagem geral do tratamento. | descarta = Baixa contagem nas amostras da fase aquosa, dosagem e ponto de injeção verificados, e problema restrito a regiões de baixa circulação com depósito. | passo oculto = Inferir que a persistência não está na fase aquosa, mas em superfícies internas com baixa varredura e depósito; daí concluir menor acessibilidade ao biocida.
- Juiz: A persistência de sulfeto e corrosão com baixa contagem na fase aquosa é explicada por biofilme sésil em nichos protegidos pouco alcançados pelo biocida, mecanismo identificado por ambos.

**ec · dificil · R1 correta · R2 correta · atalho** Num sistema de água de injeção, o mesmo biocida segue com concentração e tempo de contato validados. A atividade planctônica caiu, mas persistem colonização e pites apenas sob depósitos aderidos. Após remover esses depósitos, sem trocar o tratamento químico, a atividade local desaparece. Que mecanismo limitava a ação do biocida antes da limpeza?

- Referência: Blindagem por biofilme e depósitos aderidos, que impediam o contato do biocida com os microrganismos locais.
- R1: A presença de depósitos aderidos protegia as biomassas de contato, limitando a penetração do biocida. Após limpeza, o biocida atingiu as áreas, eliminando a atividade biológica residual.
- R2: O biocida era inibido por efeito físico/químico dos depósitos: difusão limitada e “shielding” por biofilme/partículas aderidas, além de adsorção/deativação do produto no lodo, reduzindo a concentração eficaz na camada planctônica/aderida até a remoção.
- Desenho: atraente = Resistência ao biocida. | descarta = A atividade planctônica caiu e o problema local desapareceu após a remoção dos depósitos, sem troca do tratamento químico. | passo oculto = A queda da atividade planctônica com concentração e tempo validados indica que o biocida funcionava na fase aquosa; a persistência local vinha de regiões inacessíveis sob materiais aderidos.
- Juiz: Ambos apontam corretamente a blindagem e a limitação de difusão pelo biofilme/depósitos aderidos como o fator que impedia o contato do biocida, a referência é válida, e o próprio enunciado praticamente entrega esse mecanismo.

**ec · dificil · R1 correta · R2 correta · atalho** Em um circuito de água de injeção contaminado, a dosagem contínua mantém a concentração especificada no ponto de aplicação. Mesmo assim, a contagem microbiana volta a subir após os tratamentos. A equipe passou a alternar biocidas, mas o monitoramento e os testes não mostraram perda de suscetibilidade nem incompatibilidade dos produtos. Inspeções encontraram depósitos aderidos no trecho afetado. Antes de nova revisão do programa, que ação deve ser tomada?

- Referência: Remoção de biofilmes e depósitos, se tecnicamente viável.
- R1: Realizar limpeza e remoção dos depósitos aderidos para melhorar o controle microbiológico e prevenir recidiva, antes de ajustar o programa de biocidas.
- R2: Realizar limpeza mecânica/hidráulica do trecho com depósitos (flush/descarga e remoção de incrustações/biofilme), removendo a fonte de aderência; só depois reaplicar e validar o programa de biocidas, pois a contaminação persiste por proteção em depósitos, não por falha de suscetibilidade.
- Desenho: atraente = Alternar novamente os biocidas. | descarta = O monitoramento e os testes não mostraram perda de suscetibilidade nem incompatibilidade, e as inspeções encontraram depósitos aderidos. | passo oculto = Os depósitos atuam como barreira, impedem exposição efetiva na região contaminada e permitem a recuperação da população apesar da troca de produtos.
- Juiz: A referência é válida e, como perda de suscetibilidade e incompatibilidade foram descartadas e há depósitos aderidos, o passo decisivo é remover biofilme/depósitos antes de revisar o programa; ambos dizem isso e o enunciado praticamente entrega esse caminho.

**ec · dificil · R1 incorreta · R2 correta** Após uma modificação na tubulação, a vazão nominal de MEG, a pressão, a composição do gás, o volume de água produzida e o perfil térmico permaneceram estáveis. Mesmo assim, apenas um trecho passou a formar hidrato, e a amostra total do escoamento a montante mostra MEG dentro da meta. Que mecanismo explica a perda de proteção nesse trecho?

- Referência: Falha de distribuição ou de mistura do MEG; a concentração efetiva na água livre ficou insuficiente nesse trecho.
- R1: Possível acúmulo ou alteração local na hidratação do MEG, formando uma barreira que reduz sua eficiência na proteção contra hidratos, mesmo sem mudanças na composição ou condições globais do sistema.
- R2: Apesar dos parâmetros médios estarem estáveis, a modificação pode ter causado má distribuição/mistura local do MEG (estratificação, segregação e/ou zona morta hidráulica), levando a uma queda momentânea da concentração efetiva de MEG no ponto crítico. Assim, ali ocorre supersaturação de hidrato mesmo com MEG total “dentro da meta” a montante.
- Desenho: atraente = Subdosagem global de MEG. | descarta = Somente um trecho foi afetado, enquanto vazão nominal, água produzida, pressão, composição do gás e perfil térmico permaneceram estáveis, com teor global de MEG a montante dentro da meta. | passo oculto = Teor global e vazão nominal adequados não asseguram a concentração efetiva do MEG na água livre em cada trecho; um problema isolado após a modificação indica perda local de mistura ou distribuição.
- Juiz: Como o MEG total está na meta e só um trecho falha após a modificação, o ponto decisivo é subconcentração local por má distribuição/mistura na água livre, o que torna R2 correta e R1 incorreta; a referência é válida e não se resolve por atalho genérico.

**ec · dificil · R1 correta · R2 correta** Um modelo termodinâmico calibrado apenas com solução de NaCl foi usado para definir a faixa segura do regenerador. Após a entrada de um novo blend de água produzida, a concentração de MEG e a temperatura continuam dentro da faixa estudada, mas surgem depósitos; as análises mostram agora vários íons dissolvidos e traços de contaminantes antes ausentes. Que limitação do modelo explica o desvio entre previsão e campo?

- Referência: Falta de validação para as espécies iônicas e a composição operada; calibração com sal isolado não representa água multissalina com contaminantes.
- R1: O modelo não considera os efeitos de contaminantes e íons dissolvidos na formação de depósitos, limitando sua precisão na previsão do comportamento com água produzida contaminada.
- R2: O modelo foi calibrado apenas para brina de NaCl (sistema monossal/estequiométrico), não representando a química multicomponente da água produzida (interações entre íons, coeficientes de atividade e espécies que induzem precipitação). Assim, prevê faixa térmica segura sem capturar o início de incrustação por novos sais/contaminantes.
- Desenho: atraente = Temperatura fora da faixa estudada. | descarta = a concentração de MEG e a temperatura continuam dentro da faixa estudada | passo oculto = A nova água alterou o equilíbrio de solubilidade por incluir múltiplos íons e contaminantes; assim, a calibração anterior deixou de representar o sistema real.
- Juiz: A referência é válida e ambos apontaram a limitação decisiva: um modelo calibrado só com NaCl não representa nem foi validado para a água produzida multicomponente com novos íons e contaminantes.

**ec · dificil · R1 parcial · R2 correta** Em bancada, uma alternativa de regeneração de MEG secou bem um fluido preparado sem contaminantes. No FPSO, ela passou a tratar corrente com sais, sólidos e hidrocarbonetos; temperatura, pressão e carga ficaram na faixa prevista, mas a regeneração ficou instável. Que erro de julgamento explica essa seleção?

- Referência: Transferir para o arranjo industrial o resultado de um ensaio simplificado, sem representar o circuito real.
- R1: A seleção não considerou a composição variável do fluido de pólo, principalmente os sais e sólidos, que causam obstrução e instabilidade na regeneração do MEG em operações de campo.
- R2: Extrapolação indevida dos resultados de bancada para o serviço real: o projeto/julgamento ignorou que sais, sólidos e hidrocarbonetos causam deposição/fouling, mudança de equilíbrio de fases e transferência de calor, levando a instabilidade na regeneração do MEG apesar de T, P e carga estarem na faixa.
- Desenho: atraente = Ajuste inadequado de temperatura, pressão e carga. | descarta = temperatura, pressão e carga ficaram na faixa prevista | passo oculto = Como a instabilidade surge com a corrente real e não com o fluido limpo de bancada, o ensaio não representava o circuito operacional.
- Juiz: A referência é válida ao tratar o erro como extrapolação indevida de ensaio simplificado para o circuito real; R2 traz exatamente isso e R1 ficou parcial por focar só nos contaminantes do campo, sem explicitar o erro de transferência bancada-industrial.

**ec · dificil · R1 incorreta · R2 parcial** Após alterar a regeneração para entregar MEG mais concentrado, o circuito passou a operar com mais aquecimento, maior evaporação de água e recirculação de correntes salinas. Surgiram aumento de perda de carga, queda de desempenho térmico e oscilação da unidade. A dosagem de MEG para controle de hidratos não mudou. Que mecanismo explica melhor esse conjunto de sinais?

- Referência: Precipitação de sais da água produzida, formando incrustações no circuito de recuperação.
- R1: A alteração na concentração de MEG aumentou a viscosidade do fluido, elevando a perda de carga, dificultando a transferência de calor, o que provoca aquecimento excessivo, evaporação de água, recirculação de salinas e instabilidades no sistema.
- R2: O principal mecanismo é aumento de arraste/assincronia de equilíbrio no regenerador: com MEG mais concentrado, cresce a evaporação de água e a volatilização/arraste de material hidratante e sais (carryover), retornando correntes salinas ao circuito. Isso eleva incrustação, perda de carga, piora térmica e induz instabilidade/oscilação.
- Desenho: atraente = Formação de hidratos por dosagem insuficiente de MEG. | descarta = Os sinais surgem na recuperação/regeneração com aquecimento e evaporação de água, e a dosagem de MEG não mudou. | passo oculto = Mais aquecimento, menos água disponível e recirculação salina elevam a supersaturação; isso leva à saída dos sais da solução antes dos efeitos hidráulicos e térmicos aparecerem.
- Juiz: R1 atribui os sintomas à viscosidade do MEG, enquanto R2 relaciona salmoura e incrustação mas coloca arraste/carryover como mecanismo principal em vez da precipitação de sais no circuito de recuperação; a referência é válida e não há atalho genérico porque o diagnóstico depende desse encadeamento técnico específico.

**ec · dificil · R1 correta · R2 correta · atalho** Após o resfriamento do gás, os drenos de um trecho passaram a recolher água livre e a taxa de perda metálica aumentou só ali. O gás ainda contém CO2, mas não há H2S, espuma nem condição de hidrato relevante. Que serviço químico deve ser priorizado nesse trecho?

- Referência: Inibidor de corrosão de gás, porque o problema dominante ali é o ataque ao metal associado à fase aquosa.
- R1: Priorizar tratamento anticorrosivo usando inibidores de corrosão e sistemas de escorva química para controlar a corrosão devido à água livre e CO2.
- R2: Priorize **tratamento químico de controle de corrosão por CO₂** no trecho com água livre: injeção de **inibidor film-forming (filming amine)** para proteger o metal contra a corrosão carbonática (ácido carbônico), acompanhando dosagem e eficiência.
- Desenho: atraente = Solvente de absorção, como alcanolamina. | descarta = A perda metálica aumentou só onde surgiu água livre, enquanto H2S, espuma e risco de hidrato foram descartados. | passo oculto = A presença de água livre com aumento localizado de perda metálica indica que a ameaça dominante no trecho é a corrosão por fase aquosa.
- Juiz: Com água livre após o resfriamento e aumento localizado de perda metálica em gás com CO2, o problema dominante é corrosão associada à fase aquosa e ambos priorizaram inibidor de corrosão, algo fortemente sugerido pelo próprio enunciado.

**ec · dificil · R1 correta · R2 correta · atalho** Em uma plataforma de gás, a taxa de corrosão subiu após aumento de água de formação. A concentração do inibidor no ponto de controle permaneceu na faixa, mas o MEG pobre passou a sair da regeneração com NaCl próximo da saturação e surgiram depósitos. Qual fator do meio explica melhor a perda de proteção?

- Referência: O acúmulo de sais no meio água-MEG, que altera solubilidade, transporte de massa e depósitos e compromete o filme protetor.
- R1: Aumento da salinidade no MEG devido à saída de NaCl saturado, reduzindo sua capacidade de inibição e causando depósitos que comprometem a proteção contra corrosão.
- R2: Aumento de salinidade (NaCl) até quase saturação no MEG/linha, levando à precipitação/surgimento de depósitos (escala). Esses depósitos blindam a superfície e dificultam a adsorção/distribuição do inibidor, causando perda efetiva de proteção, apesar da concentração no ponto de controle.
- Desenho: atraente = Subdosagem do inibidor de corrosão. | descarta = A concentração do inibidor no ponto de controle permaneceu na faixa. | passo oculto = NaCl próximo da saturação no MEG pobre indica mudança da composição água-MEG e favorece depósitos no meio onde o inibidor atua.
- Juiz: Ambos apontam o acúmulo de sais/salinidade no meio água-MEG com deposição comprometendo a proteção do inibidor, e o enunciado praticamente entrega esse caminho ao citar NaCl quase saturado e depósitos.

**ec · dificil · R1 incorreta · R2 correta** Após um reroteamento, duas correntes que formam mistura incompatível passam a se encontrar muito mais perto do trecho onde o depósito costuma surgir. O residual de fósforo na água produzida segue representativo e acima da MIC do squeeze, e a química das correntes não mudou. Que fator passou a limitar a proteção contra incrustação?

- Referência: A formação da mistura incompatível muito próxima do ponto crítico, reduzindo o tempo de residência antes da precipitação.
- R1: A distância reduzida entre as correntes aumenta a concentração local de fósforo, favorecendo incrustações, limitando a eficácia do squeeze na prevenção de incrustações devido à maior proximidade das áreas suscetíveis.
- R2: O fator passou a ser a cinética/tempo de contato e a eficiência de mistura: com o reroteamento, a incompatibilidade causa supersaturação e nucleação antes do inibidor (fosfato) se dispersar/atuar no volume onde o depósito se forma. A química e o residual foram mantidos, então o limite ficou na janela de mistura.
- Desenho: atraente = Residual insuficiente do inibidor, exigindo novo squeeze. | descarta = O residual de fósforo é representativo e permanece acima da MIC. | passo oculto = Inferir que o residual acima da MIC não aponta esgotamento do squeeze e que o novo ponto de encontro encurtou o tempo disponível para o inibidor afetar a cristalização.
- Juiz: R2 acerta ao apontar que o limitante passou a ser a janela de mistura/tempo de residência antes da precipitação, enquanto R1 erra ao atribuir o problema a aumento local de fósforo; a referência é válida e não admite atalho genérico.

**ec · dificil · R1 parcial · R2 correta** Após um squeeze, a curva residual seguia o histórico. Depois de uma intervenção no poço, a produção de água aumentou e a concentração passou a cair mais rápido, embora ainda não tenha alcançado o limite usado para programar novo tratamento. A coleta continua representativa e o método analítico segue compatível com o produto. Que fator explica melhor essa mudança da curva?

- Referência: Mudança de regime com maior produção de água, aumentando a diluição do inibidor liberado.
- R1: A intervenção provavelmente melhorou a vedação do poço ou alterou as condições de fluxo, acelerando a retirada de água residual, o que explica a rápida queda na concentração após o aumento na produção de água.
- R2: O aumento da produção de água (maior water cut) após a intervenção diluiu o componente alvo no fluido produzido, acelerando a queda da concentração na curva residual. A tendência permanece dentro do comportamento histórico, sem ainda atingir o limite de critério para novo tratamento.
- Desenho: atraente = Esgotamento do squeeze, com necessidade imediata de novo tratamento. | descarta = A queda acelerada começou após a intervenção com aumento da produção de água, enquanto a coleta segue representativa, o método é compatível e o limite operacional ainda não foi atingido. | passo oculto = A intervenção alterou o regime do poço; com mais água produzida, a mesma liberação do inibidor passa a aparecer em menor concentração por diluição.
- Juiz: A mudança da curva é explicada pela maior produção de água diluindo o inibidor liberado, ponto que R2 trouxe claramente, enquanto R1 relacionou a queda ao aumento de água mas sem explicitar a diluição e ainda acrescentou causas especulativas.

**ec · dificil · R1 incorreta · R2 correta** Num loop refrigerado, um aditivo reduziu a viscosidade do óleo e a pressão necessária para voltar a escoar após resfriamento estático. A temperatura de aparecimento de cristais não mudou, a taxa de deposição no trecho resfriado permaneceu igual e a aderência à parede também não mudou. Que classe de aditivo foi mais provavelmente aplicada?

- Referência: Redutor de ponto de fluidez (PPD); o efeito dominante foi reológico em baixa temperatura.
- R1: Aditivo dispersante ou molécula inibidora de cristalização. Isto mantém a viscosidade reduzida sem afetar a formação de cristais, aderência ou deposição, facilitando o fluxo no sistema.
- R2: Mais provável: aditivo “flow improver” do tipo depressor de ponto de fluidez/anti-wax (ex.: copolímero polimérico do tipo alkil-acrilato/polimetácrilato). Ele reduz viscosidade e tensão de escoamento aparente sem alterar temperatura de início de cristalização, deposição ou aderência.
- Desenho: atraente = Inibidor termodinâmico de cera (TWI). | descarta = A temperatura de aparecimento de cristais não mudou; além disso, taxa de deposição e aderência à parede permaneceram iguais. | passo oculto = As observações excluem atuação sobre início da cristalização, aderência e taxa de deposição; sobra melhora do comportamento reológico em baixa temperatura.
- Juiz: Como o aditivo melhorou só a reologia a frio sem alterar WAT, deposição ou aderência, o quadro é típico de PPD, corretamente identificado por R2 e não por R1.

**ec · dificil · R1 correta · R2 correta · atalho** Uma linha com depósito orgânico confirmado tem um pig disponível, mas o trecho inclui redução de diâmetro, histórico de perda de espessura e o procedimento aprovado não contempla passagem de pig. Ensaios mostram que um solvente disponível dissolve o material retirado da linha. O que deve ser escolhido como método de remoção?

- Referência: Aplicação química; a geometria, a integridade e o procedimento aprovado descartam o pigging.
- R1: Utilizar solvente para dissolver o depósito orgânico na linha, já que o procedimento aprovado não contempla passagem de pig e há risco de danos.
- R2: Escolher limpeza química por dissolução: injeção do solvente compatível para solubilizar o depósito orgânico, seguida de circulação/flush e remoção dos fluidos dissolvidos. Evitar pigging, já que o procedimento aprovado não contempla passagem de pig e o trecho tem restrição de diâmetro e perda de espessura.
- Desenho: atraente = Pigging. | descarta = O trecho inclui redução de diâmetro, histórico de perda de espessura e o procedimento aprovado não contempla passagem de pig. | passo oculto = As restrições de geometria, integridade e procedimento tornam o pigging não selecionável; como o solvente dissolve o depósito, o método viável passa a ser químico.
- Juiz: Ambos escolhem corretamente a limpeza química com solvente e descartam o pigging pelas restrições geométricas, de integridade e de procedimento aprovado; a referência é válida e há atalho genérico porque o enunciado praticamente elimina o pig e informa a solvência do depósito.

**ec · dificil · R1 parcial · R2 correta** Um tanque fechado de água produzida permaneceu por longo período com acúmulo e baixa renovação. O risco deixou de parecer apenas o de armazenagem e passou a incluir toxicidade e corrosão interna. Não houve superdosagem de hipoclorito nem derrame para áreas adjacentes. Qual mecanismo específico explica essa mudança do risco dominante?

- Referência: Geração de H2S por proliferação de BRS no acúmulo prolongado de água produzida.
- R1: A proliferação de microrganismos que formam biofilmes, causando corrosão microbiológica e liberação de substâncias tóxicas.
- R2: O mecanismo é a perda de controle biocida: com baixa renovação, o hipoclorito é consumido e se estabelece biofilme/atividade microbiana (p.ex., redução de sulfato), gerando H₂S e espécies corrosivas. Isso aumenta toxicidade (toxicidade por H₂S) e acelera corrosão interna.
- Desenho: atraente = Corrosão por superdosagem de hipoclorito. | descarta = O enunciado informa que não houve superdosagem de hipoclorito. | passo oculto = O acúmulo prolongado em tanque fechado favorece a proliferação de BRS antes da geração do gás.
- Juiz: O ponto decisivo é a geração de H2S por BRS em água produzida estagnada; R1 fica genérico em MIC/toxicidade microbiana e R2 explicita redução de sulfato com formação de H2S e corrosão associada.

**ec · dificil · R1 correta · R2 correta · atalho** Num FPSO, o tanque do químico mantém nível compatível com o plano, e as oscilações usuais de vazão, pressão e composição seguem dentro do histórico. Mesmo assim, surgem alteração de cor do produto, consumo anormal, espuma inesperada, perda de eficiência de separação e desvio persistente entre dosagem planejada e resposta do processo. Que foco do monitoramento de armazenamento/manuseio ficou insuficiente?

- Referência: Controle apenas do nível em tanque; faltou monitorar sinais indiretos e condições precursoras.
- R1: Monitoramento da condição do químico, incluindo análises de qualidade e composição, ficou insuficiente.
- R2: Monitoramento insuficiente de contaminação/estabilidade do produto no tanque (ingresso de água/impurezas, incompatibilidades, estratificação e condições de mistura/temperatura), levando a alteração de cor, formação de espuma, perda de eficiência de separação e resposta inconsistente à dosagem.
- Desenho: atraente = Instabilidade normal do processo offshore. | descarta = Alteração de cor, consumo anormal, espuma inesperada, perda de eficiência de separação e desvio entre dosagem planejada e resposta do processo. | passo oculto = Os sinais observados indicam problema de estocagem/manuseio do químico, apesar do nível normal e das oscilações usuais do processo.
- Juiz: O erro foi monitorar essencialmente o nível do tanque e não a condição/estabilidade do químico por sinais indiretos e precursores, o que ambos capturam, e um 'monitorar qualidade, não só nível' já bastaria.

**ec · dificil · R1 parcial · R2 parcial · atalho** Durante testes, um oxidante foi superdosado por engano. A corrosão aumentou muito no spool logo após o ponto de injeção, em aço carbono, mas pouco em outro trecho do mesmo circuito com material diferente. Não houve contato com correntes incompatíveis, e a operação nominal global do processo permaneceu a mesma. Que fator técnico final explica a diferença de severidade observada?

- Referência: O local de aplicação no circuito, combinado com o material e as condições locais.
- R1: A diferença ocorre devido à menor resistência à corrosão do aço carbono em contato com o oxidante superdosado, causando maior ataque localizado no spool. Materiais diferentes têm resistências variáveis à corrosão por oxidantes, explicando a variação de severidade.
- R2: A severidade muda por causa da reatividade eletroquímica local do aço carbono em meio oxidante: o oxidante eleva o potencial redox, desestabiliza/passiva mal os filmes e acelera dissolução anódica. No trecho de outro material, forma-se película/óxidos mais estáveis, reduzindo a taxa de corrosão.
- Desenho: atraente = A superdosagem global do oxidante. | descarta = A corrosão aumentou muito só no spool logo após a injeção, em aço carbono, enquanto no outro trecho do mesmo circuito o efeito foi pequeno e a operação nominal global ficou igual. | passo oculto = Inferir que a superdosagem agrava a corrosão, mas a diferença entre trechos decorre da exposição no ponto de aplicação e da suscetibilidade local do material.
- Juiz: A explicação correta combina o ponto de aplicação no circuito com material e condições locais; R1 e R2 acertam a influência do material/reatividade do aço carbono, mas não fecham o papel decisivo do local logo após a injeção, e o próprio enunciado quase entrega essa combinação.

**ec · dificil · R1 incorreta · R2 correta** Em uma linha de dosagem de dispersante, o indicador on-line mostra concentração baixa e a malha aumenta a injeção. Amostras de laboratório colhidas no mesmo bocal confirmam essa leitura, mas amostras coletadas mais adiante na linha mostram concentração estável na faixa alvo. Vazão de processo e bomba de dosagem estão estáveis. Que mudança no arranjo de medição corrige o problema mais diretamente?

- Referência: Reposicionar o sensor para jusante do ponto de injeção, após a mistura; ali a leitura representa a condição no equipamento.
- R1: Rever a calibragem ou substituir o sensor de concentração on-line para garantir medições precisas e confiáveis.
- R2: Ajustar o arranjo de medição para captar uma amostra representativa: mover o sensor/tomada de amostra para um ponto após mistura efetiva (ex.: instalar/usar um misturador estático ou aumentar distância de mistura) em vez de medir logo após a injeção, onde há estratificação/localmente baixa concentração.
- Desenho: atraente = Recalibrar ou limpar o sensor no ponto atual. | descarta = As amostras de laboratório colhidas no mesmo bocal confirmam a leitura do sensor. | passo oculto = Se laboratório e sensor concordam no mesmo bocal, o sensor não é o principal problema; a diferença para o ponto mais adiante indica mistura incompleta no ponto atual.
- Juiz: A referência é válida e exige reconhecer erro de representatividade por medição antes da mistura, corrigido ao mover a medição/amostragem para jusante do ponto de injeção, o que só R2 traz e não sai de um atalho genérico.

**ec · dificil · R1 incorreta · R2 correta** Num circuito tratado com hipoclorito, aumentaram ao mesmo tempo corrosão, contagem de bactérias aeróbias e indicação de deposição. Depois que os indicadores de qualidade da água melhoraram e a adição de hipoclorito aumentou, todos os indicadores voltaram ao normal. Que causa comum explica por que a ação eficaz foi aumentar o oxidante, e não reduzi-lo?

- Referência: Piora da qualidade da água, elevando a demanda de cloro e deixando o biocida efetivamente deficiente.
- R1: Aumentar o oxidante como o hipoclorito promove a oxidação de matéria orgânica e materiais corrosivos, controlando bactérias e deposições, pois seu efeito é regenerador ou de manutenção rápida do equilíbrio, diferente de um redutor que poderia agravar a corrosão e contaminantes.
- R2: A causa comum é a “demanda de cloro” (consumo do hipoclorito por matéria orgânica/biofilme e depósitos). Quando o oxidante foi aumentado, o ORP/oxidante efetivo finalmente subiu, rompendo biofilme e reduzindo corrosão e contagem/deposição; ao contrário, a redução não teria compensado a demanda.
- Desenho: atraente = Excesso de oxidante degradando inibidor de corrosão e dispersante. | descarta = A contagem de bactérias aeróbias aumentou e o quadro normalizou após aumentar o hipoclorito. | passo oculto = A piora da qualidade da água elevou a demanda de cloro; sem atender essa demanda, houve deficiência efetiva de biocida.
- Juiz: O ponto decisivo é a piora da qualidade da água aumentando a demanda de cloro e deixando o oxidante efetivo deficiente, citado por R2 e ausente em R1, e isso exige mecanismo técnico específico, sem atalho genérico.

**ec · dificil · R1 correta · R2 correta · atalho** Em uma linha aquosa, quedas de pH vieram acompanhadas de maior perda metálica na sonda RE. A equipe quer usar essa mesma correlação em outro circuito que também sofre acidificação, mas tem metalurgia diferente, presença de fase aquosa distinta, composição do fluido alterada, temperatura maior e outro regime de escoamento. Que tratamento técnico essa correlação deve receber no segundo circuito?

- Referência: Revalidação local; essa correlação não deve ser tratada como regra universal no segundo circuito.
- R1: A correlação deve ser recalibrada com dados específicos do novo circuito, considerando suas diferenças de metalurgia, fluido, temperatura e fluxo, através de testes de corrosividade e monitoramento para ajuste preciso da previsão de perda metálica.
- R2: A correlação deve ser revalidada/recalibrada: tratar como dependente de matriz e hidrodinâmica. Ajustar parâmetros por cinética corrosiva (diferença de composição, sais/O2/CO2, temperatura), diferentes mecanismos/metalurgia (sensibilidade a pH), e condições de escoamento (Nusselt/Sherwood; transferência de massa). Usar normalização por taxa de corrosão e fator de transferência.
- Desenho: atraente = Aplicar a mesma regra de ajuste baseada em pH usada no primeiro circuito. | descarta = O segundo circuito opera com metalurgia, fase aquosa, composição do fluido, temperatura e regime de escoamento diferentes. | passo oculto = As diferenças de metalurgia, fase aquosa, composição, temperatura e escoamento alteram a sensibilidade da resposta corrosiva à acidificação.
- Juiz: O ponto decisivo é revalidar/recalibrar localmente a correlação no novo circuito, sem tratá-la como universal, e ambos disseram isso, sendo um item que aceita até a resposta genérica de prudência de 'revalidar localmente'.

**ec · facil · R1 incorreta · R2 incorreta · ref. inválida** Qual é o papel do indicador em relação à variável de processo?

- Referência: Resumir seu efeito sobre o desempenho.
- R1: O indicador mede e exibe a variável de processo, permitindo monitoramento, controle e tomada de decisão para manter operações dentro de parâmetros desejados.
- R2: Em instrumentação, o indicador (I) fornece uma leitura visual da variável de processo (ex.: pressão, vazão, nível, temperatura). Ele não altera o processo; apenas exibe o valor para o operador e, conforme projeto, pode servir como referência para atuação do controlador.
- Juiz: A pergunta é ambígua entre indicador de desempenho e indicador de instrumentação, o que invalida a referência, e ambos responderam no sentido de exibir/medir a variável de processo, diferente do que a referência traz.

**ec · facil · R1 correta · R2 correta · ref. inválida · atalho** O que pode fazer um mesmo processo ser acompanhado por KPIs diferentes?

- Referência: A mudança da finalidade da avaliação e do usuário do indicador.
- R1: Porque indicadores variam conforme objetivos, níveis de gestão ou critérios de avaliação, refletindo diferentes aspectos do processo e suas metas específicas.
- R2: O mesmo processo pode ser acompanhado por KPIs diferentes por variação de objetivo (eficiência x qualidade x segurança), mudanças de escopo/limites do processo, diferentes prioridades contratuais/regulatórias, disponibilidade de dados, maturidade operacional e definições distintas de métricas (tempo, custo, risco).
- Juiz: A pergunta é ampla e admite várias respostas corretas além da dupla finalidade/usuário, tornando a referência não exclusiva e suscetível a atalho genérico, mas ambos acertam ao apontar mudança de objetivos/gestão como motivo para KPIs distintos.

**ec · facil · R1 parcial · R2 correta** Em FPSO, o que a redundância precisa manter para ser útil em compressão, geração ou tratamento?

- Referência: A função de processo relevante, não apenas a duplicação de equipamento.
- R1: Manter fontes de energia, sistemas de controle e componentes críticos redundantes para assegurar continuidade operacional na compressão, geração ou tratamento.
- R2: A redundância só é útil se mantiver o “serviço” dentro dos limites do processo: compressão precisa manter vazão/pressão requeridas; geração precisa manter disponibilidade/capacidade elétrica para acionar cargas críticas; tratamento precisa manter eficiência de separação/remoção (especificações de efluente e estabilidade do sistema).
- Juiz: R2 reproduz o ponto decisivo ao exigir manutenção da função/serviço de processo dentro dos requisitos, enquanto R1 fica na redundância de recursos/equipamentos, e a referência é válida sem atalho genérico.

**ec · facil · R1 correta · R2 correta · atalho** Além de confiabilidade, disponibilidade e manutenibilidade, que dimensão o RAMS incorpora?

- Referência: Segurança.
- R1: Segurança, incluindo aspectos de risco e proteção, também é incorporada na análise RAMS.
- R2: Além de confiabilidade, disponibilidade e manutenibilidade, o RAMS incorpora a dimensão de segurança (Safety).
- Juiz: A referência é válida e a resposta sai praticamente por associação direta ao S de RAMS, portanto há atalho, e ambos responderam segurança.

**ec · facil · R1 incorreta · R2 correta** Que instantes devem ser registrados para calcular MTTR e disponibilidade observada?

- Referência: O início da falha e o retorno ao estado operacional.
- R1: Devem ser registrados o tempo de inatividade, tempo de reparo e tempo total de operação para calcular MTTR e disponibilidade observada.
- R2: Para MTTR/Disponibilidade: registrar o instante de falha (início da perda de função/"failure start"), o instante de detecção/aceite do estado de indisponibilidade (se aplicável) e o instante de retorno à função ("restoration/return to service" ou conclusão do reparo, quando opera dentro de limites). Somar os tempos de reparo.
- Juiz: Para MTTR e disponibilidade observada importam os instantes de início da falha e de retorno ao estado operacional, por isso R2 é correta, R1 é incorreta por listar durações em vez de marcos temporais, a referência é válida e não há atalho genérico.

**ec · facil · R1 parcial · R2 incorreta · ref. inválida · atalho** Além de separar e tratar as correntes, que função do processamento primário também condiciona a capacidade produtiva da unidade?

- Referência: A movimentação dos fluxos.
- R1: O controle do fluxo de entrada e a volumetria do choke que regula a entrada do fluido na unidade.
- R2: A função é o condicionamento do fluido para transporte e processamento a jusante, principalmente por remoção de água e sais/impurezas (dessalinização e desidratação), reduzindo corrosão e incrustação e evitando limitações operacionais que restringem a capacidade produtiva.
- Juiz: A referência quer a função de movimentação dos fluxos; R1 apenas tangencia isso ao focar no controle de entrada/choke e R2 retorna ao tratamento das correntes, enquanto a formulação da pergunta é vaga e admite outras respostas equivalentes.

**ec · facil · R1 parcial · R2 correta** Quando a limitação de produção está em um ponto comum do sistema, que tipo de decisão se torna inevitável?

- Referência: Priorização de entregas e alocação de capacidade.
- R1: A decisão de restringir ou ajustar a produção para manter a estabilidade do sistema e evitar sobrecarga ou falhas operacionais.
- R2: Quando a limitação ocorre em um ponto comum (gargalo compartilhado), torna-se inevitável uma decisão de alocação/prioridade de produção entre as diversas linhas ou campos atendidos por esse recurso restritivo, definindo quem recebe a capacidade e quem sofre restrição (curtailment).
- Juiz: A referência é válida e o decisivo é que um gargalo comum obriga a priorizar e alocar capacidade entre correntes ou entregas, algo que R2 traz e R1 só aborda genericamente como restrição de produção, sem atalho fácil.

**ec · facil · R1 correta · R2 correta · ref. inválida · atalho** Que indefinição organizacional pode dificultar a validação de mudanças diante de desvios operacionais?

- Referência: Indefinição de responsabilidade técnica.
- R1: Falta de clareza na hierarquia e responsabilidades pode dificultar a aprovação rápida de mudanças operacionais devido à indefinição na autoridade decisória.
- R2: Indefinições de responsabilidades e aprovações (matriz RACI/fluxo de governança) — quem valida, em que etapa e com qual autoridade — dificultam a validação de mudanças quando surgem desvios operacionais.
- Juiz: Ambos apontam a indefinição de responsabilidades/autoridade para validar mudanças, alinhada ao núcleo de responsabilidade técnica, mas a pergunta é ampla e uma resposta genérica sobre falta de clareza de papéis já sairia correta.

**ec · facil · R1 parcial · R2 correta · atalho** Na gestão de risco de um FPSO, para que serve identificar componentes e sistemas críticos?

- Referência: Para orientar a implantação e a atualização dos controles de risco, priorizando as funções críticas.
- R1: Para priorizar manutenção e monitoramento, minimizando falhas, acidentes e perdas ambientais, garantindo a segurança e eficiência do FPSO.
- R2: Identificar componentes e sistemas críticos permite direcionar a análise de risco e as medidas de mitigação (barreiras, redundância, inspeções e testes), priorizando itens que mais afetam segurança, integridade do FPSO e continuidade operacional, reduzindo probabilidade e consequência de falhas.
- Juiz: A referência é válida e o decisivo era usar a identificação de criticidade para orientar a implantação e atualização dos controles de risco, o que R2 expressou claramente e R1 apenas parcialmente ao restringir isso a manutenção e monitoramento; além disso, a formulação aceita resposta bastante genérica de priorização.

**ec · facil · R1 correta · R2 correta · atalho** Na FMEA, que composição de equipe organiza a avaliação?

- Referência: Equipe multidisciplinar.
- R1: A equipe de avaliação da FMEA é composta por especialistas multidisciplinares, incluindo engenheiros de projeto, operação, manutenção e segurança, que contribuem com conhecimento técnico específico para identificar e avaliar falhas potenciais.
- R2: Na FMEA, a avaliação é organizada tipicamente por um time multidisciplinar liderado por Engenharia de Processo/Qualidade e com participação de Operações (produção), Manutenção, Projeto/Engenharia, Segurança e Meio Ambiente, e Controle/Instrumentação.
- Juiz: Bastava reconhecer que a FMEA é conduzida por equipe multidisciplinar; ambos acertam, a referência é válida e o item permite atalho genérico por definição direta.

**ec · facil · R1 correta · R2 correta** Após a desestabilização química da água produzida, como a flotação retira gotas de óleo e flocos?

- Referência: Por adesão a bolhas e ascensão.
- R1: A flotação utiliza bolhas de gás que aderem às gotas de óleo e flocos, elevando-os à superfície para remoção, separando-os da água produzida.
- R2: Na flotação por ar dissolvido/induzido, bolhas finas se aderem a gotas de óleo e partículas hidrofóbicas/flocos condicionados (via reagentes: coletor/coagulante e ajustes de pH). A energia interfacial favorece a captura; então a mistura flutua, formando escuma rica em óleo para remoção.
- Juiz: O mecanismo decisivo é a adesão de gotas/flocos às bolhas seguida de ascensão, exatamente descrito por R1 e R2, e não basta uma resposta genérica para acertar.

**ec · facil · R1 parcial · R2 correta** No tratamento da água produzida para descarte, qual variável é principal para avaliar o desempenho do sistema e o enquadramento do descarte?

- Referência: TOG da água produzida tratada.
- R1: A variável principal é a concentração de contaminantes específicos, como óleo ou sólidos em suspensão, que garante o cumprimento das normas ambientais e eficiência do tratamento.
- R2: A variável principal é o teor de óleo e graxas (geralmente medido como THC/TOG). Ela é o principal critério de desempenho dos processos de separação (ex.: flotação/dessorção/filtração) e o parâmetro mais usado para enquadramento do descarte de água produzida.
- Juiz: O ponto decisivo é o TOG/teor de óleo e graxas da água tratada como principal parâmetro de desempenho e enquadramento do descarte, que R2 nomeia, enquanto R1 fica genérico ao falar de contaminantes ou sólidos em suspensão.

**ec · facil · R1 incorreta · R2 incorreta · ref. inválida** Além da disponibilidade e da composição, que condição da corrente gasosa precisa ser avaliada para usar stripping a gás?

- Referência: O destino seguro da corrente gasosa.
- R1: A velocidade e o fator de contato entre gases e líquidos devem ser otimizados para garantir eficiência na transferência de componentes.
- R2: Além da disponibilidade e da composição, deve-se avaliar as condições de operação da corrente gasosa, principalmente pressão (e temperatura associada), pois elas determinam as pressões parciais e o equilíbrio de fases, garantindo força motriz e eficiência do stripping a gás.
- Juiz: A referência cobra avaliar a destinação segura da corrente gasosa de stripping, que nenhum candidato citou, mas o item é mal formulado porque fala em 'condição da corrente gasosa' e isso abre respostas plausíveis como pressão/temperatura.

**ec · facil · R1 correta · R2 correta · atalho** Em biocidas gerados no local e de rápida decomposição, o que a persistência curta não significa?

- Referência: Ausência de risco.
- R1: Não significa ausência de efeito tóxico ou de resistência biológica, apenas que o biocida se degrada rapidamente no ambiente.
- R2: Que a persistência curta não significa “ausência de toxicidade” ou “inocuidade”; apenas indica menor tempo de permanência no meio. Pode haver efeito agudo no curto prazo, dependendo da dose, biodisponibilidade e forma química do biocida.
- Juiz: A referência é válida porque o essencial é que persistência curta não equivale a ausência de risco/inocuidade, ideia presente em R1 e R2, e há atalho por ser praticamente a negação direta pedida no enunciado.

**ec · facil · R1 incorreta · R2 correta** Na prevenção de hidratos com MEG, que tipo de inibidor ele é?

- Referência: Inibidor termodinâmico.
- R1: O MEG atua como inibidor termofílico de hidratos, formando uma camada protetora que impede a formação de cristais de hidrato de metano.
- R2: O MEG (monoetilenoglicol) é um inibidor termodinâmico (deslocador de hidratos), ou seja, reduz a atividade da água e aumenta o equilíbrio de formação de hidratos, dificultando sua nucleação e crescimento.
- Juiz: A classificação correta é inibidor termodinâmico, dada apenas por R2, enquanto R1 descreve um mecanismo e um termo errados, com referência válida e específica.

**ec · facil · R1 parcial · R2 parcial** Além da presença de MEG, de que composição a severidade das incrustações no circuito depende?

- Referência: Da composição iônica real da água produzida.
- R1: A severidade das incrustações depende também da concentração de íons de cálcio e magnésio na água do circuito.
- R2: Além de MEG (monoetilenoglicol), a severidade depende principalmente de: concentração de sais (NaCl/CaCO3 etc.), relação saturação/temperatura, pH, presença de CO2/H2S (corrosão e incrustação), composição do óleo/água (orgânicos, surfactantes), razão água/óleo e taxa de deformação/temperatura do escoamento.
- Juiz: R1 foi parcial por citar só alguns íons e R2 por misturar vários fatores sem focar na composição iônica real da água produzida, que é o elemento decisivo; a referência é válida e não há atalho genérico porque é preciso identificar especificamente essa composição.

**ec · facil · R1 correta · R2 correta · atalho** No tratamento do gás offshore, qual é a função do sequestrante de H2S?

- Referência: Consumir ou imobilizar a espécie sulfídrica.
- R1: O sequestrante de H₂S removal o gás, neutralizando o gás ácido e evitando corrosão e problemas ambientais na operação offshore.
- R2: O sequestrante de H2S reage com o sulfeto de hidrogênio no gás, convertendo-o quimicamente em espécies menos tóxicas e mais estáveis (tipicamente sólidos/compostos sulfurosos), reduzindo a corrosão e protegendo equipamentos e dutos.
- Juiz: R1 e R2 acertaram ao indicar que o sequestrante reage com/neutraliza o H2S, removendo-o por consumo ou imobilização; a referência é válida e há atalho genérico porque 'sequestrante de H2S' praticamente permite responder por associação direta que sua função é retirar o H2S.

**ec · facil · R1 parcial · R2 parcial · ref. inválida** De que três bases deve partir a seleção do arranjo de armazenamento e manuseio de um químico offshore?

- Referência: Função do químico, fluido de interação e consequências plausíveis de falha.
- R1: Segurança, compatibilidade química e eficiência operacional.
- R2: Deve partir das três bases: (1) características físico‑químicas do produto (compatibilidade, inflamabilidade, toxicidade, estado e volatilidade); (2) requisitos operacionais de uso/transferência (vazão, frequência, temperatura, forma de dosagem); (3) critérios de segurança, conformidade e meio ambiente (prevenção de vazamentos, contenção, normas).
- Juiz: A referência cobra a tríade função do químico, fluido de interação e consequências plausíveis de falha, mas a pergunta é ampla e admite outras decomposições igualmente defensáveis; por isso a referência é fraca e R1/R2 ficam só parcialmente alinhados ao citarem compatibilidade/operação/segurança sem essa tríade específica.

**ec · facil · R1 correta · R2 incorreta · ref. inválida · atalho** No ajuste automático de dosagem, que tipo de variabilidade a automação tende a reduzir?

- Referência: A variabilidade humana.
- R1: A automação reduz a variabilidade devido a fatores humanos, proporcionando dose mais consistente e ajustada às condições operacionais em tempo real.
- R2: Em geral, o ajuste automático de dosagem reduz a variabilidade de operação controlada, principalmente variações de vazão/concentração do dosado causadas por distúrbios (ex.: variações de vazão do processo, temperatura, propriedades do influente). Também reduz variação do setpoint e desvios de mistura.
- Juiz: R1 coincide com a referência ao focar na variabilidade humana, mas R2 fala de distúrbios do processo; como a pergunta é ampla e pode admitir outras variabilidades também reduzidas por automação, a referência não é exclusiva e o atalho é genérico.

**ec · facil · R1 correta · R2 correta · ref. inválida · atalho** Qual é a principal vantagem da leitura temporal na avaliação da corrosão?

- Referência: Correlacionar a corrosão com variáveis operacionais que mudam durante a operação.
- R1: Permite monitorar a taxa de corrosão ao longo do tempo, identificando padrões e agindo preventivamente para reduzir falhas e manutenção, garantindo a integridade da estrutura.
- R2: A leitura temporal permite acompanhar a evolução da taxa de corrosão ao longo do tempo, distinguindo variações sazonais/operacionais e identificando tendência de degradação, em vez de uma estimativa pontual apenas num instante.
- Juiz: A pergunta é ampla e admite como vantagem principal tanto correlacionar a corrosão com variáveis operacionais quanto acompanhar tendência/evolução temporal, de modo que R1 e R2 são tecnicamente aceitáveis e há forte atalho por associação direta com 'temporal'.

**ec · media · R1 correta · R2 parcial · atalho** Em um FPSO, a equipe quer medir apenas o desempenho de um compressor de gás, sem incluir a etapa de tratamento nem o resultado global da planta. Em que escopo o KPI deve ser definido?

- Referência: No equipamento.
- R1: O KPI deve ser definido no escopo de performance do compressor de gás, especificamente concentrando-se na eficiência, capacidade e operação isolada do equipamento, independentemente do tratamento ou resultados globais da planta.
- R2: Defina o KPI no escopo da unidade/linha de processo do compressor (escopo do equipamento ou “battery limits” do compressor), medindo desempenho operacional sem incluir tratamento a jusante e sem KPI global da planta/FP SO.
- Juiz: R1 acerta o escopo no equipamento, R2 mistura isso com um nível mais amplo de unidade/linha, e a resposta praticamente sai por associação direta do enunciado para o nível do compressor.

**ec · media · R1 incorreta · R2 parcial · ref. inválida** Na partida da campanha de um FPSO, a redundância elevou a disponibilidade de um sistema. Sem mudar a arquitetura, como a vantagem tende a se comportar quando o horizonte de operação fica muito mais longo?

- Referência: Perde o caráter ilimitado; a degradação dos ativos pode superar o benefício do reserva.
- R1: A vantagem da redundância aumenta com o tempo, pois ela reduz a probabilidade de falha total do sistema ao longo de um horizonte prolongado.
- R2: Com horizonte muito longo, a partida transiente “assenta” e o desempenho converge para o regime permanente. A vantagem da redundância não cresce indefinidamente: tende a estabilizar na diferença de disponibilidade em regime, determinada por taxas de falha e tempos de reparo (assumindo falhas independentes).
- Juiz: R1 erra ao dizer que a vantagem cresce com o tempo e R2 acerta apenas que ela não cresce indefinidamente, mas a referência não é única porque o enunciado é ambíguo entre envelhecimento/degradação e convergência a regime permanente, sem atalho genérico.

**ec · media · R1 correta · R2 parcial · atalho** Em um estudo de confiabilidade de um FPSO, a equipe já levantou falhas e reparos próprios da unidade, mas decide usar somente OREDA para representar o comportamento local por considerá-lo mais robusto. Que base deveria sustentar as condições locais?

- Referência: Os dados da própria unidade; bancos setoriais só apoiam comparação e padronização.
- R1: A base deve incluir dados de inspeções, registros históricos específicos do FPSO e condições ambientais locais para complementar o OREDA, garantindo uma representação precisa do comportamento local.
- R2: Devem ser suportadas pelas condições de projeto e de operação do FPSO (arranjo/uso, ambiente, temperatura, pressão, vibração, qualidade do fluido, frequência de acionamento) comparadas às condições de referência do OREDA, aplicando fatores de ajuste para refletir o “local”.
- Juiz: R1 acerta ao priorizar os dados históricos da própria unidade para representar o comportamento local, enquanto R2 fica incompleto ao focar só em condições de projeto/operação e ajustes ao OREDA; a referência é válida e há atalho genérico porque o enunciado já contrapõe explicitamente os dados próprios ao uso exclusivo do banco setorial.

**ec · media · R1 correta · R2 correta · atalho** Na manutenção de um equipamento do FPSO, a intervenção segue sob as mesmas condições e com taxa de reparo assumida constante. Se o tempo disponível for ampliado, como muda a probabilidade acumulada de restabelecimento?

- Referência: Aumenta, aproximando-se de 1 à medida que o tempo cresce.
- R1: A probabilidade acumulada de restabelecimento aumenta, pois um tempo adicional oferece maior chance do equipamento se reparar, seguindo uma função de distribuição acumulada, como a exponencial.
- R2: Com taxa de reparo constante (modelo exponencial), a probabilidade acumulada de restabelecimento cresce com o tempo disponível: P(t)=1−e^(−μt). Ao ampliar t, P(t) aumenta continuamente, tendendo a 1 para tempos muito longos.
- Juiz: O ponto decisivo é que, com taxa de reparo constante, a probabilidade acumulada de restabelecimento cresce com o tempo e tende a 1, o que ambos afirmaram; a referência é válida e a resposta sai quase por associação direta ao enunciado.

**ec · media · R1 correta · R2 correta · atalho** Dois módulos de um sistema do FPSO têm falhas equivalentes, mesma equipe, mesmo diagnóstico e mesmos sobressalentes. Em um, o item é modular e facilmente acessível; no outro, exige desmontagem extensa em área restrita. Em qual deles o MTTR tende a ser menor?

- Referência: No módulo acessível e modular, porque acessibilidade e modularização reduzem o tempo médio de reparo.
- R1: No módulo com acesso fácil, o MTTR tende a ser menor devido à manutenção rápida e menos desmontagem.
- R2: Tende a ser menor no primeiro. Se o item é modular e facilmente acessível, o tempo de intervenção para diagnóstico/retirada e reinstalação reduz a desmontagem, sequência de trabalho em área restrita e filas de autorização, diminuindo o componente de tempo de reparo do MTTR.
- Juiz: A referência é válida e um atalho de bom senso basta porque maior acessibilidade e modularização reduzem desmontagem e tempo de reparo, exatamente o que ambos apontaram.

**ec · media · R1 incorreta · R2 incorreta · atalho** Um compressor opera abaixo da eficiência esperada. Para preservar especificações dos produtos e estabilidade operacional, que ajuste tende a ser necessário na produção?

- Referência: Redução da vazão de produção.
- R1: Ajuste na pressão de operação ou na taxa de compressão para reduzir a carga e melhorar a eficiência do compressor.
- R2: Quando a eficiência do compressor cai, para manter a pressão/condições exigidas a jusante tende a ser necessário aumentar a potência fornecida (maior rotação/abertura de válvulas de controle) para atingir o mesmo diferencial de pressão e vazão do processo.
- Juiz: O ajuste pedido era cortar a vazão de produção, e nenhum candidato mencionou isso; a referência é válida, mas o item aceita atalho genérico porque a resposta é a prudência operacional óbvia diante de compressor limitante.

**ec · media · R1 parcial · R2 correta · atalho** Com mecanismo dominante, origem dos íons e arquitetura equivalentes entre duas rotas de controle de incrustação, o campo tem intervenção difícil e paradas muito penalizadas. Que condicionante passa a pesar decisivamente na seleção?

- Referência: A dificuldade de intervenção associada à penalidade de parada.
- R1: O custo operacional e o impacto na produção passam a pesar decisivamente na seleção.
- R2: Com mecanismos e fontes de íons equivalentes, a seleção passa a depender principalmente da facilidade de aplicação e do impacto operacional: em campo com intervenção difícil e paradas caras, prioriza-se a rota que permite tratamento contínuo/in situ, minimizando shut-downs e ações manuais.
- Juiz: A referência é válida e há atalho porque o próprio enunciado destaca a intervenção difícil e a penalidade de parada; R1 citou só custo/impacto produtivo, enquanto R2 capturou o condicionante decisivo completo.

**ec · media · R1 correta · R2 correta · atalho** Dois registros de parada de um FPSO têm o mesmo custo final. Um traz apenas totais pagos; o outro também compara planejado e realizado, acréscimos de escopo e suporte usado. Qual deles apoia melhor o custo do ciclo de vida?

- Referência: O detalhado, porque mostra onde o plano subestimou complexidade e suporte.
- R1: O registro com comparação planejado e realizado, acréscimos de escopo e suporte, apoia melhor o custo do ciclo de vida, pois fornece um entendimento mais completo e preciso dos custos totais e variações ao longo do ciclo.
- R2: O segundo registro. Ao comparar planejado x realizado, detalhar acréscimos de escopo e explicitar suporte utilizado, ele permite rastrear variações e causas, corrigir premissas e refinar estimativas futuras—melhorando o controle e a otimização do custo do ciclo de vida do FPSO.
- Juiz: A referência é válida porque o registro detalhado é o único que mostra desvios entre planejado e realizado, acréscimos de escopo e suporte para refinar custo de ciclo de vida, e ambos disseram isso num item praticamente óbvio pela própria comparação descrita.

**ec · media · R1 correta · R2 parcial · ref. inválida · atalho** Em intervenções sucessivas de um FPSO, desvios recorrentes aparecem em tarefas antes pouco priorizadas e acabam deslocando o prazo global. Na preparação da próxima parada, que critério deve ser revisto com esse histórico?

- Referência: A priorização por risco das tarefas.
- R1: O critério de priorização das tarefas deve ser revisto, focando naquelas com maior impacto nos desvios recorrentes para prevenir atrasos na globalidade das intervenções.
- R2: Reveja o critério de priorização/seqüenciamento das atividades usado no planejamento, migrando de uma “prioridade por criticidade nominal” para uma priorização baseada no caminho crítico/restrições (critical path & bottlenecks), atualizada pelo histórico de desvios das intervenções anteriores.
- Juiz: A referência aponta para revisar a priorização por risco das tarefas, o que R1 atende ao focar nas de maior impacto histórico dos desvios, enquanto R2 fica parcial por substituir isso por critério de caminho crítico/restrições; a referência não é totalmente única porque outros critérios de planejamento também podem ser defendidos, e há atalho genérico porque 'rever a priorização' quase sai do próprio enunciado.

**ec · media · R1 correta · R2 correta · atalho** Dois FPSOs teriam a mesma duração de parada, o mesmo escopo corretivo e o mesmo contexto contratual. Um deles tem maior produção diária. Em qual a perda potencial tende a ser maior?

- Referência: No de maior produção, porque a receita diária comprometida é maior.
- R1: A perda potencial tende a ser maior no FPSO com maior produção diária, pois sua parada gera maior impacto financeiro devido ao volume de petróleo não produzido.
- R2: A perda potencial tende a ser maior no FPSO com maior produção diária, pois a parada tem mesma duração e escopo, então a quantidade de óleo/gás não produzido (e, portanto, a receita perdida) é proporcional à taxa de produção.
- Juiz: O ponto decisivo era que, com mesma duração, escopo e contexto, o FPSO de maior produção perde mais receita por dia, o que ambos responderam; a referência é válida e há atalho genérico por ser associação direta entre maior produção e maior perda.

**ec · media · R1 correta · R2 correta · atalho** Dois trens de tratamento lidam com emulsões diferentes em FPSOs. Em um, a emulsão é mais estável; no outro, as fases separadas precisam atender especificações mais rigorosas. Que fatores devem definir as condições de tratamento?

- Referência: A estabilidade da emulsão e as especificações das fases separadas.
- R1: A estabilidade da emulsão, composição do petróleo, teor de água, presença de detergentes e requisitos de qualidade final influenciam as condições de tratamento, ajustando fatores como temperatura, agentes de demulsificação e tempo de processamento.
- R2: Definam-se pelas propriedades da emulsão (tamanho de gota, viscosidade, tensão interfacial, densidade, teor de sal/água, SARA/asfaltenos, temperatura e composição do óleo), especificações do produto (BS&W, sal residual, água livre/total), limite de química/compatibilidade (desemulsificante, antiespumante, pH) e restrições operacionais (vazões, retenção, pressão, energia de aquecimento, capacidade de decantadores/eletrodes).
- Juiz: A referência é válida porque, no contraste dado, as condições devem ser definidas pela estabilidade da emulsão e pelas especificações das fases separadas, elementos presentes em R1 e R2, mas há atalho porque isso praticamente repete os próprios termos do enunciado.

**ec · media · R1 parcial · R2 correta · ref. inválida** Após mudar a salinidade da salmoura, o mesmo clarificante passou a responder de modo diferente, sem alteração de petróleo nem de dosagem. Que propriedades interfaciais podem ter mudado?

- Referência: Carga elétrica, solvatação e adsorção de espécies na interface.
- R1: A tensão superficial, a compatibilidade interfacial entre óleo, água e clarificante, e aadsorção de agentes dispersantes podem ter sido alteradas pela mudança na salinidade.
- R2: Mudanças de salinidade podem alterar: (1) tensão interfacial óleo–água (IFT), (2) atividade/adsorção do clarificante na interface, (3) forças de repulsão/estabilização e potencial zeta das partículas emulsificadas, (4) estabilidade da emulsão (tamanho de gota, coalescência) e (5) eletrólitos → efeito salting-out e CMC/condição micelar do surfactante ativo.
- Juiz: R2 cobre os eixos da referência ao tratar de carga/repulsão, adsorção e efeito salino na solvatação, enquanto R1 só tangencia a adsorção com termos mais vagos; porém a pergunta é aberta e admite outras propriedades interfaciais igualmente corretas, então a referência não é única.

**ec · media · R1 parcial · R2 parcial · atalho** Após mover a injeção do antiespumante para um trecho retilíneo, de escoamento suave e sem elementos de turbulência antes do separador, a espuma continua com dose e formulação inalteradas. Que variável de aplicação está limitando a resposta?

- Referência: A intensidade de mistura, insuficiente para contato efetivo com a interface crítica.
- R1: A variável limitante é a eficiência do ponto de injeção, que pode não estar otimizada para distribuir o antiespumante eficazmente na espuma, mesmo com o novo trecho retilíneo.
- R2: A variável limitante é o tempo de residência/condição de contato do antiespumante com a espuma antes do separador (relacionado à mistura/dispersion no trecho), reduzindo a oportunidade de ruptura e coalescência das bolhas.
- Juiz: A referência exige apontar a mistura insuficiente, sugerida pelo trecho retilíneo sem turbulência, e R1/R2 só tangenciam isso ao falar de distribuição do ponto ou de tempo de contato, enquanto o enunciado já dá a pista principal.

**ec · media · R1 correta · R2 correta · atalho** Com mesmo fluido, mesma dosagem e mesma flotação, um ponto injeta o reagente em trecho com mistura suficiente e tempo antes da flotação; o outro, já na entrada da flotação, com pouca mistura. Em qual condição a formação de flocos removíveis tende a ser mais adequada?

- Referência: No ponto com mistura suficiente e tempo antes da flotação, porque favorece dispersão do reagente, coagulação e formação de flocos.
- R1: A formação de flocos removíveis tende a ser mais adequada quando o reagente é adicionado com mistura suficiente e tempo antes da flotação, permitindo melhor nucleação e crescimento dos flocos.
- R2: Tende a ser mais adequada na primeira condição: com mistura suficiente e tempo antes da flotação, a cinética de agregação aumenta e formam-se flocos maiores e mais estáveis, com melhor aderência às bolhas e maior removibilidade.
- Juiz: R1 e R2 acertaram ao escolher a condição com mistura suficiente e tempo antes da flotação, que favorece dispersão do reagente, coagulação e formação de flocos; a referência é válida e há atalho genérico porque a comparação do enunciado praticamente entrega a melhor condição.

**ec · media · R1 parcial · R2 correta · ref. inválida · atalho** Suponha reinjeção de água produzida com co-injeção de água do mar. Em que tipo de poço a deposição por sulfato também pode ocorrer?

- Referência: Nos poços injetores.
- R1: Na produção de poços de petróleo, especialmente em ambientes com alta salinidade, a deposição por sulfato pode ocorrer durante a reinjeção de água produzida e água do mar, formando sulfatos que causam incrustações nos tubos e equipamentos.
- R2: Pode ocorrer em poços injetores onde a água produzida e a água do mar são misturadas/compartilham trechos do poço (ex.: no anular e/ou na coluna de injeção/tubing), favorecendo a formação de sulfatos (BaSO4, SrSO4) ao longo da tubulação.
- Juiz: A pergunta é ambígua porque deposição por sulfato também pode ocorrer em produtores sob mistura adequada, embora a referência tenha escolhido injetores; por isso R2 coincide com a referência, R1 fica parcial ao apontar produção de forma confusa, e há atalho por associação direta com reinjeção/injetor.

**ec · media · R1 parcial · R2 parcial · atalho** Duas rotas de desoxigenação atendem a mesma meta de oxigênio residual. Em um FPSO com limitações severas de peso, área ocupada e utilidades, que critério adicional deve direcionar a escolha?

- Referência: A compatibilidade da rota com as limitações de topsides e com o modo de operação do sistema.
- R1: A eficiência energética e consumo de energia, priorizando a rota que demandar menor energia operacional, devido às limitações severas de peso e utilidades.
- R2: Direcionar pela melhor confiabilidade e menor custo operacional total: em vez da oxigenação residual (mesma meta), escolher a rota com menor complexidade e menor consumo/necessidade de reposição de insumos (reagentes) e utilidades, reduzindo paradas e logística em operação no FPSO.
- Juiz: A referência é válida e o elemento decisivo era a compatibilidade da rota com as restrições de topsides e com o modo de operação do FPSO, enquanto ambos focaram apenas em partes do problema como energia, confiabilidade, insumos e custo; além disso, a pergunta é fortemente induzida pelas limitações já citadas.

**ec · media · R1 correta · R2 correta · atalho** Em um circuito de água de injeção com sulfato disponível, aparece sulfeto e cresce a preocupação com ataque em componentes de ferro e aço. Que grupo microbiano ganha prioridade nessa avaliação?

- Referência: Bactérias redutoras de sulfato, por converterem sulfato em sulfeto e se associarem à biocorrosão.
- R1: Bactérias sulfato-redutoras (BSRs), que convertem sulfato em sulfeto, aumentando o risco de corrosão em ferro e aço.
- R2: Bactérias redutoras de sulfato (grupo dos SRB, como Desulfovibrio/Desulfotomaculum), pois reduzem sulfato a sulfeto (H2S), elevando risco de corrosão microbiologicamente influenciada em aços e ferros.
- Juiz: Ambos indicam corretamente as bactérias redutoras de sulfato como prioritárias por converterem sulfato em sulfeto e se associarem à biocorrosão, e a referência admite atalho por associação quase direta entre os termos do enunciado.

**ec · media · R1 correta · R2 incorreta** A equipe monitora apenas amostras da fase aquosa do sistema de água de injeção. Que parcela do problema operacional pode ficar fora dessa avaliação?

- Referência: Os microrganismos aderidos às superfícies internas do sistema.
- R1: A avaliação pode deixar fora a corrosão interna de tubulações e equipamentos, além de possíveis biofilmes ou bactérias que afetam a integridade do sistema.
- R2: A avaliação pode ficar cega para problemas associados à fase não aquosa — como arraste de óleo/hidrocarbonetos (óleo livre ou emulsão) e/ou presença de gás livre — e efeitos relacionados a depósitos/contaminações formados a partir dessas fases, mesmo que a amostra aquosa pareça “limpa”.
- Juiz: R1 acerta ao incluir biofilmes ou microrganismos aderidos às superfícies internas como parcela que pode escapar da amostragem da fase aquosa, enquanto R2 desvia para arraste de óleo/gás e outras fases, que não são o ponto decisivo da referência.

**ec · media · R1 correta · R2 correta** Uma mudança operacional alterou simultaneamente a temperatura, a pressão e a carga da regeneração de MEG. Que aspectos do processo tendem a ser diretamente afetados?

- Referência: A separação e o consumo de energia.
- R1: A eficiência de remoção de água, a taxa de regeneração, o consumo de energia e a estabilidade do sistema de regeneração de MEG.
- R2: Afetam diretamente a destilação/stripping: ponto de ebulição e equilíbrio vapor-líquido (teor de água removida), taxas de vapor e refluxo, eficiência de separação nas colunas/ pratos, carga térmica do reboiler e condensador (consumo de energia) e, por consequência, a qualidade do MEG regenerado.
- Juiz: R1 e R2 acertaram por relacionar a mudança de temperatura, pressão e carga à eficiência de separação/regeneração e ao consumo de energia; a referência é válida e não há atalho genérico porque isso exige entendimento do efeito dessas variáveis na regeneração de MEG.

**ec · media · R1 incorreta · R2 parcial** Em uma linha de produção, o inibidor é dosado, mas no ponto em que encontra os íons formadores a água livre mostra residual insuficiente. Que requisito do mecanismo de proteção deixou de ser atendido?

- Referência: Disponibilidade do inibidor na fase aquosa, em concentração suficiente durante o contato com os íons incrustantes.
- R1: O requisito de formação de uma barreira protetora adequada pelos íons inibidores, que impede a corrosão mesmo com água residual insuficiente.
- R2: Deixou de ser atendido o requisito de manter uma quantidade mínima de água livre/microfase aquosa para dissolver, transportar e permitir a ação do inibidor (contato com os íons formadores e formação do filme/controle de reação).
- Juiz: R1 erra ao trocar o mecanismo por uma barreira anticorrosiva, e R2 só se aproxima ao falar em fase/microfase aquosa mas não no residual do inibidor em concentração suficiente na água durante o contato com os íons; a referência é válida e não há atalho genérico porque a pergunta exige esse mecanismo específico de disponibilidade na fase aquosa.

**inventario · dificil_A · R1 correta · R2 correta · atalho** Em dois trimestres consecutivos de um FPSO, os acidentes sem afastamento passaram de 4 para 7. No segundo, uma parada programada embarcou muito mais contratados e acumulou quase o dobro de horas de trabalho; o painel reporta só o total de casos em cada trimestre. Nessa leitura, por que esse aumento não permite atribuir, diretamente, piora real ao desempenho de segurança?

- Referência: Contagem bruta sem base de exposição; com mais pessoas e horas de trabalho a bordo, o aumento pode refletir só maior exposição, não piora intrínseca.
- R1: Porque o aumento pode estar relacionado a fatores como maior contratação, horas de trabalho ou mudança na coleta de dados, não refletindo necessariamente uma piora real na segurança, mas sim variações na exposição ou na documentação de incidentes.
- R2: Porque o painel só mostra contagem absoluta por trimestre; com mais contratados e mais horas (maior exposição) na parada, o número esperado pode aumentar mesmo sem piorar a taxa de acidente. Sem normalizar por horas/homem ou UMs/turnos e sem incidentes por atividade, não dá para inferir deterioração de desempenho.
- Desenho: atraente = Houve piora real do desempenho intrínseco de segurança no segundo trimestre. | descarta = A parada programada elevou fortemente o efetivo embarcado e as horas de trabalho, e o painel mostra apenas a contagem absoluta de casos. | passo oculto = Inferir que a contagem absoluta de ocorrências precisa ser relacionada à exposição ao risco; com muito mais pessoas e horas de trabalho, o aumento bruto pode resultar só dessa exposição maior.
- Juiz: O decisivo é que o painel mostra contagem bruta sem normalização pela exposição (pessoas/horas), fundamento presente em ambos; a referência é válida e permite atalho genérico de normalizar por horas.

**inventario · dificil_A · R1 parcial · R2 correta** Em um FPSO, o KPI supunha alta disponibilidade de um trem com um equipamento ativo e outro em reserva fria, porque o reserva acumulava poucas horas e apresentava pouco desgaste. Mesmo assim, em demandas reais o reserva ficou indisponível: uma vez por bateria do sistema de acionamento descarregada e outra por atuador da linha cruzada travado. Por que o KPI não pode tratar a baixa exposição ao desgaste como garantia suficiente?

- Referência: Falhas em espera, de partida e de comutação; operar menos reduz alguns desgastes, mas não elimina esses modos na reserva fria.
- R1: Porque o KPI não considerou eventos imprevisíveis ou falhas operacionais; baixa exposição ao desgaste não garante confiabilidade contra falhas inesperadas, que podem ocorrer independentemente do tempo de uso.
- R2: Porque baixa “exposição ao desgaste” não garante confiabilidade. O tempo entre falhas do reserva depende de modos dominantes não proporcionais ao uso (p.ex., falha por falta de carga de bateria e falha mecânica por travamento). Além disso, há falhas ocultas, degradação por armazenamento/ambiente e exigências de comutação que testam o sistema. KPI baseado só em horas e desgaste ignora esses mecanismos e o impacto em disponibilidade.
- Desenho: atraente = O reserva é essencialmente mais confiável porque opera menos e sofre menos desgaste que o equipamento ativo. | descarta = Apesar das poucas horas e do baixo desgaste, houve indisponibilidade por bateria do acionamento descarregada e por atuador da linha cruzada travado. | passo oculto = Inferir que a indisponibilidade do reserva vem de modos de falha latentes fora da operação sob carga, que só aparecem quando ele é demandado.
- Juiz: O ponto decisivo era citar modos de falha de espera, partida e comutação independentes do desgaste; por isso R2 acerta, R1 fica genérico demais, e o item é válido sem atalho genérico.

**inventario · dificil_A · R1 correta · R2 correta · atalho** No fechamento do KPI de disponibilidade de um FPSO, a previsão da análise RAM ficou distante do realizado. A lógica do modelo já representava dependências e redundâncias com detalhe, mas as frequências de falha e os tempos de reparo vieram de outra unidade; nesta, arquitetura, acessos, estratégia de manutenção e regime operacional são diferentes. Qual é a principal causa técnica da distorção?

- Referência: Parâmetros não aderentes à unidade; frequências de falha e tempos de reparo devem ser atualizados com dados do próprio FPSO.
- R1: Diferenças na arquitetura, acessos, estratégias de manutenção e regimes operacionais entre unidades resultam em dados de falha e reparo incompatíveis, causando distorções na análise RAM do FPSO.
- R2: A principal causa é a utilização de parâmetros de confiabilidade (frequências de falha e MTTR/tempos de reparo) provenientes de outro FPSO/unidade. Mesmo com lógica RAM correta, quando o regime operacional, arquitetura/arquitetura funcional e estratégia/condições de manutenção diferem, a taxa e os tempos previstos deixam de ser representativos.
- Desenho: atraente = O modelo é pouco sofisticado ou simplificado demais. | descarta = A lógica e as redundâncias já estavam detalhadas, e os parâmetros usados vieram de outra unidade com arquitetura, acessos, manutenção e regime operacional distintos. | passo oculto = Inferir que, com a lógica já bem representada, a divergência decorre dos parâmetros transferidos de outra unidade, que variam com características da instalação analisada.
- Juiz: O elemento decisivo é o uso de frequências de falha e tempos de reparo não aderentes à unidade analisada, que ambos identificaram corretamente; a referência é válida e a causa já está praticamente explicitada no enunciado.

**inventario · dificil_A · R1 parcial · R2 parcial** No KPI mensal de disponibilidade de um FPSO, três ordens corretivas de equipamentos independentes foram liberadas na mesma manhã. Sobressalentes estavam a bordo, áreas acessíveis e permissões emitidas; não houve espera por logística. Ainda assim, o segundo e o terceiro reparos só começaram após o término do anterior, e cada ativo ficou parado além do seu tempo individual de reparo. Por que a indisponibilidade total se prolongou?

- Referência: Porque a capacidade das equipes de manutenção era o limitante; as falhas simultâneas entraram em fila de atendimento e ampliaram a indisponibilidade.
- R1: A sequência dos reparos sem sobreposição, além do tempo agregado para concluir cada um, elevou a indisponibilidade total mesmo com recursos e logística disponíveis.
- R2: Mesmo com ordens independentes, a indisponibilidade total prolonga quando não há paralelismo real: requerem a mesma “janela” de parada, recursos comuns (equipe/mestres), interfaces de segurança/SIMOPS e liberações por teste de comissionamento e verificação final. O término do 1º é condição para emitir/validar os demais, tornando o trabalho sequencial.
- Desenho: atraente = Espera por acesso, sobressalente, liberação ou logística. | descarta = Sobressalentes estavam a bordo, áreas acessíveis, permissões emitidas e não houve espera por logística. | passo oculto = Inferir que, sem atraso por acesso, sobressalente, liberação ou logística, a espera entre reparos decorre da capacidade de atendimento, e falhas simultâneas passam a competir por esse recurso.
- Juiz: O ponto decisivo é a fila causada por capacidade limitada de manutenção; R1 só descreve a sequenciação sem explicitar o gargalo e R2 menciona recurso comum/equipe, mas mistura causas contrariadas pelo enunciado, de modo que a referência é válida e não se resolve por resposta genérica.

**inventario · dificil_A · R1 parcial · R2 correta** A vazão total do campo foi reduzida após aumento do teor de água dos poços. O compressor de gás, a exportação e o condicionamento de óleo seguem com folga. Ao mesmo tempo, a reinjeção atingiu a taxa máxima estável, o descarte opera no limite aceitável e o inventário líquido nos separadores continua subindo. Que limitação específica explica esse corte?

- Referência: Perda de capacidade na malha de água produzida, porque o volume aquoso coproduzido já não consegue ser reinjetado ou descartado na taxa gerada.
- R1: A limitação é devido ao aumento do teor de água que reduz a capacidade de separação, causando acúmulo líquido nos separadores e limitando a vazão total do campo.
- R2: A limitação é a capacidade de manejo/remoção de água produzida: reinjeção já atingiu o máximo estável e o descarte está no limite. Com isso, a água não consegue escoar dos separadores, elevando o inventário e obrigando o corte da vazão total.
- Desenho: atraente = Gargalo em equipamentos de óleo ou gás do processamento primário. | descarta = Compressor, exportação e condicionamento de óleo seguem com folga, enquanto reinjeção e descarte atingem limite e o inventário líquido nos separadores sobe. | passo oculto = Inferir que o gargalo está no manejo do volume aquoso coproduzido e que isso, mesmo sem limitação dominante em óleo ou gás, força reduzir a vazão total do campo.
- Juiz: O corte decorre especificamente do gargalo na malha de água produzida — reinjeção e descarte já no limite, elevando o inventário nos separadores — que R2 explicitou e R1 reduziu genericamente a uma perda de separação, e a resposta exige inferir esse mecanismo a partir de vários indícios, não um atalho genérico.

**inventario · dificil_A · R1 parcial · R2 parcial** Em uma FPSO, após semanas redistribuindo vazões entre poços por gargalo num ponto comum do processamento, a produção é interrompida. No mesmo período, ROV confirma curvatura fora do envelope em uma linha flexível ligada ao turret e o monitoramento mostra queda persistente de tração numa linha que mantém a unidade posicionada; a retomada fica condicionada a reparo e verificação subaquática. Que causa específica explica melhor essa parada?

- Referência: Comprometimento em riser e/ou ancoragem; a parada decorre da necessidade de intervenção de integridade, não só de redistribuição operacional.
- R1: A curvatura fora do envelope na linha flexível compromete sua integridade estrutural, levando à perda de tração, o que pode causar vazamentos ou falhas no fluxo, resultando na parada da FPSO para reparo.
- R2: A parada é melhor explicada por dano/degeneração em uma linha flexível conectada ao turret, com curvatura fora do envelope, causando perda persistente de tração (perda de integridade/contato adequado) na linha que mantém o posicionamento. Isso exige reparo e verificação subaquática antes da retomada.
- Desenho: atraente = Decisão operacional de redistribuição de vazões por restrição em ponto comum do processamento. | descarta = Curvatura fora do envelope, queda persistente de tração e retomada condicionada a reparo e verificação subaquática. | passo oculto = Inferir que anomalias subsea na linha flexível e na linha de posicionamento caracterizam problema de integridade em sistemas críticos da unidade, capaz de justificar a interrupção.
- Juiz: A referência é válida e exige reconhecer uma parada por integridade em riser e/ou ancoragem, não por mera redistribuição operacional, e ambos chegaram perto mas confundiram os sintomas do flexível com a perda de tração da linha de posicionamento.

**inventario · dificil_A · R1 parcial · R2 correta** Em um FPSO, os KPIs de produção e receita caíram fortemente após longa indisponibilidade. A capacidade nominal de processo e os limites usuais de exportação não mudaram, mas a auditoria registrou falhas de autodiagnóstico e ações contingenciais e corretivas concluídas depois do prazo compatível com o risco. Que mecanismo melhor explica essas perdas elevadas?

- Referência: Interdição da instalação, causada por falhas de autodiagnóstico e por resposta contingencial e corretiva fora de prazo compatível com o risco.
- R1: Falha no autodiagnóstico e ações corretivas atrasadas prejudicaram a operação, levando às perdas, apesar da capacidade nominal e limites não modificados.
- R2: O principal mecanismo é aumento de tempo morto e redução de desempenho durante rampa/retomada: falhas de autodiagnóstico geram bloqueios/trips, exigem contingências e corretivas tardias, prolongando indisponibilidade operacional e o período de estabilização, reduzindo volume exportado e, portanto, receita.
- Desenho: atraente = Baixa eficiência operacional ou restrição normal de capacidade produtiva. | descarta = A capacidade nominal e os limites usuais de exportação não mudaram, enquanto a auditoria apontou falhas de autodiagnóstico e ações contingenciais e corretivas fora do prazo compatível com o risco. | passo oculto = Inferir que a combinação de autodiagnóstico falho e resposta tardia ao risco desloca a causa das perdas de um problema de desempenho para um mecanismo de segurança e conformidade que tira a instalação de operação.
- Juiz: A referência é válida e o ponto decisivo é a perda por interdição/indisponibilidade prolongada causada por autodiagnóstico falho e resposta tardia, o que R2 explicita e R1 só sugere genericamente, sem caber atalho de prudência.

**inventario · dificil_A · R1 parcial · R2 correta · atalho** No painel de KPIs de um FPSO maduro, a vazão total parou de crescer. Compressão de gás, estabilização e exportação de óleo seguem com folga. Em paralelo, o corte de água aumenta, as interfaces nos separadores ficam mais difíceis de controlar, o sistema de tratamento se aproxima do limite de qualidade e as bombas de reinjeção já operam no máximo contínuo. Qual limitação passou a definir a capacidade prática da unidade?

- Referência: Restrição na rota aquosa; o limite passou a vir do volume de água coproduzida e de seu destino, não do manuseio de hidrocarbonetos.
- R1: A limitação é o aumento na corte de água e o controle das interfaces nos separadores, que afetam a produção sem afetar os demais KPIs.
- R2: A limitação passou a ser o sistema de tratamento e reinjeção de água produzida: maior corte de água dificultando separação/controle de interfaces, aproximação do limite de qualidade do efluente e bombas de reinjeção operando em regime máximo contínuo, limitando a vazão total exportável.
- Desenho: atraente = Capacidade de manuseio de hidrocarbonetos. | descarta = Compressão, estabilização e exportação de óleo têm folga, enquanto separadores, tratamento e bombas de reinjeção estão pressionados pelo aumento do corte de água. | passo oculto = Inferir que a folga nos sistemas de óleo e gás, somada à pressão crescente sobre separação, tratamento e reinjeção, indica migração do gargalo para a corrente aquosa.
- Juiz: O limite migrou para a rota aquosa — tratamento e destino/reinjeção da água produzida —, então R2 acerta ao apontar o gargalo completo e R1 fica apenas nos sintomas de maior corte de água e controle de interfaces, com forte pista direta no próprio enunciado.

**inventario · dificil_A · R1 parcial · R2 parcial · ref. inválida** Em um poço ligado a um FPSO, a vazão bruta caiu nas últimas semanas. Choke, linha e separação mantiveram a mesma condição operacional, mas as pressões medidas no poço saíram do padrão histórico. Sem indício de limitação nova em superfície, que mecanismo específico melhor explica essa perda?

- Referência: Incrustação na coluna de produção, elevando a resistência ao fluxo e associando a queda de vazão bruta à alteração de pressão observada no poço.
- R1: Possível acumulação de influxos de fluidos ou sólidos no poço, causando bloqueios ou alterações na resistência à produção, levando à queda de vazão e mudanças na pressão, mesmo com operações de choke e separação constantes.
- R2: Queda de vazão por redução da produtividade do reservatório próximo ao poço, mais compatível com incrustação/entupimento no intervalo (ex.: formação de escala/asfaltenos) ou dano na zona de influência. Isso altera o gradiente e as pressões downhole, sem necessidade de mudança operacional em superfície.
- Desenho: atraente = Outra limitação genérica do sistema, como restrição em superfície. | descarta = Choke, linha e separação ficaram inalterados, enquanto a mudança apareceu nas pressões medidas no poço. | passo oculto = Inferir que a combinação de queda de vazão bruta com desvio de pressão no poço, sem nova limitação em superfície, indica aumento de resistência ao fluxo dentro da coluna.
- Juiz: A referência escolhe incrustação na coluna de produção como aumento de resistência ao fluxo, de modo que R1 chega perto apenas como obstrução genérica e R2 mistura incrustação com queda de produtividade/dano próximo ao poço, mas o enunciado não discrimina bem esse mecanismo de outras causas subsuperficiais igualmente plausíveis.

**inventario · dificil_A · R1 parcial · R2 correta · atalho** Num FPSO, um desvio operacional raro ocorre no trem de compressão. A equipe de bordo identifica a causa provável e uma ação temporária, porém a resposta demora porque aguarda retorno do especialista em terra, a revisão do fluxograma aplicável não está acessível localmente e ninguém define quem aprova a alteração provisória. Que fator explica melhor o atraso de resposta, de decisão e de validação da mudança?

- Referência: Fragilidade organizacional: dependência de suporte remoto, documentação inacessível e responsabilidade técnica indefinida, não apenas a complexidade do desvio.
- R1: Falta de autoridade e procedimentos claros para aprovação rápida de alterações provisórias em situações de emergência.
- R2: A ausência de governança e processo formal de Mudança Temporária (MOC) — indefinição de autoridade/fluxo de aprovação, somada à falta de procedimentos (fluxograma) acessíveis — explica melhor o atraso na resposta, decisão e validação.
- Desenho: atraente = Complexidade técnica do desvio operacional raro no trem de compressão. | descarta = A demora aparece associada à espera por especialista em terra, à falta de acesso à revisão aplicável e à dúvida sobre quem autoriza a alteração provisória. | passo oculto = Inferir que o gargalo principal vem da estrutura organizacional e documental para responder ao desvio, e não da dificuldade técnica intrínseca do evento.
- Juiz: O atraso decorre de fragilidade organizacional/MOC com documentação inacessível e autoridade indefinida, não da complexidade técnica do desvio; R1 cobre só parte disso e R2 sintetiza o quadro completo, que já está praticamente explicitado no enunciado.

**inventario · dificil_A · R1 correta · R2 correta · atalho** Em um FPSO, duas paradas anteriores geraram relatórios finais completos, mas os mesmos desvios de interface, isolamento e autorização voltaram a ocorrer. Na terceira parada, o formato do relatório quase não mudou; a diferença foi que as lições passaram a ser discutidas nas análises de risco das frentes seguintes e acompanhadas por indicadores até tratamento. A recorrência caiu e a priorização das ações futuras melhorou. O que explica tecnicamente essa melhora?

- Referência: A incorporação do aprendizado à cultura de segurança com monitoramento sistemático das ações, não a mera emissão formal do relatório final.
- R1: A integração das lições nos riscos e indicadores promove maior conscientização, monitoramento contínuo e ações preventivas, reduzindo recorrências através de melhorias na gestão de riscos e comunicação.
- R2: A melhoria ocorre pela institucionalização das lições aprendidas no ciclo de gestão de risco e governança: desvios viram critérios de identificação/mitigação nas análises das frentes seguintes, com responsáveis e indicadores de acompanhamento até o tratamento (fechamento/eficácia). Isso quebra o “mesmo padrão” operacional e reduz recorrência.
- Desenho: atraente = A emissão ou maior detalhamento do relatório final. | descarta = As duas paradas anteriores já tinham relatórios completos, e na terceira o formato quase não mudou; o que mudou foi discutir lições nas análises de risco e acompanhá-las por indicadores. | passo oculto = Inferir que o fator decisivo não foi ter relatório, pois ele já existia antes; foi transformar as lições em prática recorrente de segurança e acompanhamento.
- Juiz: O decisivo é transformar o relatório em aprendizado incorporado às análises de risco com acompanhamento por indicadores até tratamento, o que ambos disseram, e isso é praticamente explicitado no enunciado.

**inventario · dificil_A · R1 correta · R2 correta · atalho** No dashboard do FPSO, o KPI de barreiras críticas aparece verde porque contabiliza apenas itens cadastrados. Mesmo assim, uma proteção de isolamento de emergência está com teste funcional vencido, falhas repetidas sem eliminação da causa e parâmetros mantidos de uma condição antiga do reservatório. Como fica a exposição efetiva da operação?

- Referência: Ela pode divergir da considerada para operar, porque a proteção existe formalmente, mas não sustenta a confiabilidade nem as premissas usadas na análise.
- R1: A exposição efetiva permanece elevada, pois a barreira crítica não reflete condições atuais, como testes vencidos e falhas recorrentes, comprometendo a segurança operacional mesmo com KPI verde.
- R2: A exposição efetiva aumenta: o KPI verde é apenas “coverage” por cadastro. Com teste funcional vencido, falhas repetidas sem eliminação de causa e parâmetros desalinhados do reservatório, a barreira não está confiável. Deve-se tratar como barreira degradada/indisponível, elevar risco operacional e ativar mitigação compensatória.
- Desenho: atraente = A exposição permanece a mesma da análise original, porque a proteção existe, está cadastrada e o KPI está verde. | descarta = O teste funcional está vencido, há falhas repetidas sem correção definitiva e os parâmetros seguem uma condição antiga do reservatório. | passo oculto = Inferir que KPI baseado em existência cadastral não comprova funcionalidade; com teste, manutenção ou premissas inadequados, a proteção deixa de sustentar a exposição assumida.
- Juiz: Ambas reconhecem que o KPI verde por cadastro não representa a exposição real porque a barreira está degradada e fora das premissas da análise, e há atalho genérico porque bastaria dizer que o risco efetivo é maior apesar do verde.

**inventario · dificil_B · R1 parcial · R2 correta · atalho** Em um FPSO, falhas repetidas de um mesmo pacote geraram ordens em que a intervenção técnica durou quase sempre 6 a 8 h, mas o retorno operacional variou de 1 a 5 dias. Os registros separam intervenção de outros intervalos; em várias ocorrências houve pendência de acesso, liberação e peça, e colocar mais técnicos não encurtou a parada total. Na disponibilidade operacional observada, o que mais explica a perda capturada por esse KPI?

- Referência: Downtime logístico/administrativo dominante na disponibilidade operacional, não limitação do reparo ativo.
- R1: A principal causa é o tempo de manutenção e o tempo para liberar acesso, peças e logística, que geram atrasos além do tempo de intervenção técnico, impactando significativamente a disponibilidade operacional.
- R2: A maior causa da perda no KPI foi o “tempo de recuperação” fora da intervenção: filas/pendências de acesso e liberação (permissões, bloqueios), espera de peça e logística, além de start-up/testes. Esses gargalos dominam o cronograma e não são reduzidos apenas aumentando técnicos.
- Desenho: atraente = MTTR alto por baixa mantenabilidade do equipamento | descarta = as horas de intervenção técnica ficaram semelhantes entre as falhas e mais técnicos não reduziram o tempo total até o retorno | passo oculto = inferir que o tempo que mais alonga a indisponibilidade está fora da intervenção técnica, em acessos, liberações, sobressalentes ou mobilização
- Juiz: R2 acerta ao identificar o downtime logístico/administrativo fora da intervenção como dominante, R1 fica parcial por misturá-lo com o tempo de manutenção ativa, e a referência é válida embora haja atalho porque o enunciado já expõe acesso/liberação/peça como gargalos.

**inventario · dificil_B · R1 correta · R2 correta · ref. inválida · atalho** Num FPSO, há duas bombas de exportação em paralelo. Nas paradas que mais afetam o KPI, a bomba em serviço desarma e a reserva estava liberada, sem falha mecânica registrada, mas também não assume; em todos os eventos, a pressão do ar de instrumentos fica abaixo do permissivo de ambas e a exportação cessa. O que o arranjo duplicado está mascarando como verdadeiro limitante do desempenho?

- Referência: Um gargalo compartilhado de utilidades entre as bombas: o ar de instrumentos comum às duas.
- R1: O arranjo duplicado mascara a limitação do controle de pressão do ar de instrumentos, que ao ficar abaixo do permissivo, impede a troca automática ou backup, causando a parada do sistema mesmo sem falha mecânica nas bombas.
- R2: O arranjo paralelo mascara o verdadeiro limitante: a pressão de ar de instrumentos está baixa. Isso leva a falha do comando/atuadores (valv. de controle/recuperação, permissivos e intertravamentos) e faz as bombas não reassumirem/causam trip, cessando a exportação apesar da reserva disponível.
- Desenho: atraente = Falta de redundância da bomba principal. | descarta = A bomba reserva estava liberada e sem falha mecânica, mas também perdeu a função no mesmo evento. | passo oculto = Inferir que a redundância das bombas não preserva a função porque ambas dependem do mesmo insumo para manter permissivo e operar.
- Juiz: O essencial era apontar o gargalo compartilhado de utilidades no ar de instrumentos comum às duas bombas; ambos acertam, mas o próprio enunciado praticamente entrega a resposta, tornando a referência inválida e o item um atalho por associação direta.

**inventario · dificil_B · R1 correta · R2 correta · atalho** Na análise RAM de um FPSO protótipo, sem histórico confiável próprio, a equipe usou apenas um banco setorial para estimar o desempenho desse mesmo ativo em sua futura operação. Qual é a principal limitação do resultado obtido?

- Referência: Resultados RAM imprecisos por uso de dados setoriais que não refletem a unidade específica.
- R1: A principal limitação é a falta de dados históricos específicos do FPSO, levando a estimativas menos precisas e potencialmente enviesadas ao usar apenas um banco setorial geral.
- R2: A principal limitação é a baixa representatividade do banco setorial para o FPSO específico: sem histórico próprio, a confiabilidade/desempenho estimados ficam sujeitos a vieses por diferenças de projeto, modo operacional, ambiente e estratégia de manutenção, reduzindo a validade do resultado para a futura operação.
- Desenho: atraente = O banco setorial já basta para representar fielmente a unidade. | descarta = Trata-se de um protótipo sem histórico confiável próprio, e a estimativa é para a operação desse mesmo ativo. | passo oculto = Inferir que, para prever o comportamento da própria unidade, dados setoriais não substituem dados do ativo e podem levar a parametrização inadequada.
- Juiz: O ponto central era a baixa representatividade de dados setoriais para a unidade específica, tornando o resultado RAM impreciso, e isso pode ser respondido por um atalho genérico sobre falta de dados próprios.

**inventario · dificil_B · R1 correta · R2 correta · atalho** Na revisão do planejamento operacional de um FPSO, ocorrências anteriores da própria unidade e de ativos semelhantes repetiram desvios na separação de fluidos. Na unidade atual, a barreira prevista para essa função aparece no procedimento e no cadastro de barreiras. Antes de considerá-la como controle efetivo no risco assumido para a operação, que aspecto dessa barreira ainda precisa ser verificado?

- Referência: O estado real de desempenho da barreira associada, não apenas sua presença em procedimento e cadastro.
- R1: A sua eficácia operacional, incluindo testes de funcionamento, manutenção e confiabilidade, deve ser verificada para garantir sua efetividade como controle de risco.
- R2: Verificar a eficácia/condição real da barreira: integridade mecânico-funcional e desempenho comprovado (evidência de teste/prova/inspeção dentro do intervalo, calibração e prontidão para a condição de projeto), não apenas o registro/procedimento.
- Desenho: atraente = A confirmação de que a barreira está listada na documentação. | descarta = O enunciado já informa que a barreira consta em procedimento e cadastro, mas isso ainda não autoriza tratá-la como controle efetivo. | passo oculto = Inferir que o histórico ajuda a priorizar a função no planejamento, mas não substitui verificar se a barreira realmente cumpre sua função na unidade atual.
- Juiz: R1 e R2 acertaram ao exigir verificação da condição/desempenho real da barreira, e não apenas sua existência em procedimento e cadastro; a referência é válida e há atalho genérico porque um 'ver se funciona de verdade' já atende ao núcleo técnico da resposta.

**inventario · dificil_B · R1 parcial · R2 correta** Em um FPSO, o painel de KPI registra cada evento só com a hora da falha e a hora do retorno à operação. Em vários eventos, entre esses marcos houve espera por acesso, liberação, sobressalente e mobilização antes da intervenção. Se o painel tirar a média direta desses intervalos para reportar MTTR, que indicador estará medindo de fato?

- Referência: Downtime total médio; MTTR só sai ao separar o tempo de reparo ativo das esperas.
- R1: O painel estará mensurando o MTTR médio desde o início da falha até o retorno à operação, incluindo tempos de espera e outras atividades não diretamente relacionadas à reparação técnica.
- R2: A média estará medindo o tempo de indisponibilidade “de ponta a ponta” até a liberação do sistema para voltar à operação (downtime/Time-to-Restore), incluindo esperas e mobilização/obtenção de recursos, não apenas o tempo efetivo de reparo (MTTR estrito).
- Desenho: atraente = MTTR médio, usando toda a duração da parada. | descarta = O enunciado informa esperas por acesso, liberação, sobressalente e mobilização dentro do mesmo evento. | passo oculto = Inferir que o intervalo entre falha e retorno mistura tempo de reparo com esperas, portanto não isola o reparo.
- Juiz: R2 distingue corretamente downtime total/tempo de restauração de MTTR estrito, enquanto R1 descreve o intervalo de ponta a ponta incluindo esperas, mas o chama de MTTR e por isso fica apenas parcial.

**inventario · dificil_B · R1 incorreta · R2 incorreta** Em um FPSO, dois trens de compressão em paralelo operam abaixo do limite mecânico individual. Quando ambos aumentam carga simultaneamente, a pressão no cabeçote único de descarga atinge o máximo permitido e a vazão total se estabiliza. Mesmo assim, propõem instalar um terceiro compressor idêntico em paralelo. Que frente de modificação tende a elevar a capacidade efetiva do sistema?

- Referência: Atuar no recurso compartilhado a jusante que satura o sistema; outro compressor em paralelo não eleva a capacidade efetiva.
- R1: Adicionar um compressor em paralelo aumenta a capacidade total de compressão, permitindo maior vazão ou pressão sem atingir limites mecânicos individuais, elevando assim a capacidade efetiva do sistema.
- R2: Instalar um terceiro compressor idêntico em paralelo, mantendo a limitação de pressão do cabeçote de descarga via controle (IGV/anti-surge) para que a pressão permaneça no teto permitido. Assim, cada máquina opera em menor vazão, reduzindo o estrangulamento individual e elevando a vazão total efetiva até o novo equilíbrio.
- Desenho: atraente = instalar um terceiro compressor idêntico em paralelo | descarta = quando os dois trens aumentam carga juntos, a pressão no cabeçote único de descarga atinge o máximo permitido e a vazão total deixa de crescer | passo oculto = Inferir que o limitante real está no elemento compartilhado pelos trens, então a mudança eficaz deve atuar nele, não no número de máquinas paralelas.
- Juiz: Como o gargalo é o cabeçote ou recurso compartilhado a jusante saturado na pressão máxima, nenhuma das respostas que aposta em mais um compressor atende ao ponto decisivo; a referência é válida e não há atalho genérico.

**inventario · dificil_B · R1 parcial · R2 correta · ref. inválida · atalho** Em um FPSO, um desvio evoluiu sem autodiagnóstico eficaz; as medidas de contingência só começaram quando a unidade já estava em interdição parcial. Além da produção perdida na parada forçada, que impactos econômicos indiretos tendem a aparecer nesse quadro?

- Referência: Mobilização extraordinária e replanejamento logístico, porque a resposta já saiu da rotina operacional.
- R1: Impactos indiretos incluem custos de reparo, perda de contratos futuros, aumento de seguros, impacto na reputação, multas por não conformidade e aumento de custos operacionais devido à interrupção e ao gerenciamento de crises.
- R2: Além da perda imediata de produção: custos de manutenção/reparo emergencial, honorários e horas-extras de mobilização (tripulação/terceiros), atrasos em contratos e multas SLA, aumento do CAPEX/OPEX por correções e testes adicionais, perdas por maior taxa de indisponibilidade futura/tempo fora de cronograma e potenciais custos regulatórios/seguradoras (causas investigatórias).
- Desenho: atraente = Apenas perda de eficiência operacional do processo. | descarta = As medidas só começaram quando a unidade já estava em interdição parcial e houve parada forçada. | passo oculto = Inferir que a falha de autodiagnóstico e a contingência iniciada tarde transformaram o caso em correção emergencial, que passa a gerar custos indiretos além da perda de produção.
- Juiz: A pergunta é aberta e aceita outros impactos indiretos além do citado na referência, inclusive respostas genéricas de custo, mas R2 foi o que melhor captou a mobilização extraordinária fora da rotina e R1 ficou amplo e especulativo.

**inventario · dificil_B · R1 parcial · R2 correta** Num FPSO, dois períodos tiveram contagem parecida de falhas. No segundo, várias ocorrências se sobrepuseram; não houve espera relevante por acesso, sobressalentes, liberações nem logística, mas o tempo até voltar à operação aceitável aumentou. O que explica o pior desempenho global desse segundo período?

- Referência: Capacidade da equipe de manutenção tornou-se o gargalo do retorno, prolongando a indisponibilidade quando as ocorrências se sobrepuseram.
- R1: A sobreposição de falhas e a complexidade de intervenções ampliaram o tempo de reparo e resolução, elevando o tempo total fora de operação mesmo sem espera por recursos, causando pior desempenho global.
- R2: O pior desempenho no 2º período é explicado por falhas simultâneas/empilhadas em sistemas dependentes: mesmo sem esperas “formais” de acesso/sobressalentes/logística, a equipe e o tempo de diagnóstico, paralelização e testes/finalização competem, elevando MTTR e causando maior downtime agregado (efeito cascata e sobreposição de intervenções).
- Desenho: atraente = a confiabilidade dos equipamentos piorou | descarta = A contagem de falhas foi semelhante; o que mudou foi a sobreposição das ocorrências e o aumento do tempo para restabelecer a operação aceitável. | passo oculto = Inferir que, sem espera relevante por acesso, sobressalentes, liberações ou logística, as falhas sobrepostas passaram a disputar a capacidade das equipes.
- Juiz: O elemento decisivo é que a capacidade da equipe de manutenção virou o gargalo quando as falhas se sobrepuseram, explicitado por R2, enquanto R1 descreve apenas o efeito de sobreposição/complexidade sem identificar esse limitante.

**inventario · dificil_B · R1 parcial · R2 correta** Em um FPSO de campo maduro, a água produzida cresce continuamente. Separação e tratamento de óleo e compressão de gás seguem sem perda relevante de desempenho, mas alarmes e aproximações de limite passam a ocorrer em tratamento, reinjeção e descarte de água. Que consequência operacional isso tende a impor ao campo?

- Referência: Necessidade de reduzir a vazão total do campo, porque a capacidade de manejar a fase aquosa passa a definir o patamar sustentável.
- R1: Aumenta o risco de restrições operacionais, possível redução na capacidade de reinjeção e descarte, além de maior complexidade na gestão do tratamento de água, podendo levar a limites de segurança ou ambientais mais rígidos.
- R2: Com a água produzida dominando, o sistema passa a operar continuamente próximo aos limites de tratamento/reinjeção/descarte, gerando restrições de escoamento, intermitências por alarme e necessidade de throttling/limitação da produção. Em casos extremos, pode haver paradas ou reinjeção insuficiente, elevando risco operacional.
- Desenho: atraente = gargalo principal no tratamento de óleo ou gás | descarta = os limites aparecem nas rotas de água produzida, enquanto óleo e gás seguem estáveis | passo oculto = Inferir que a restrição prática deixou de estar no manuseio de hidrocarbonetos e passou para a malha de água produzida.
- Juiz: R2 captou que o gargalo de manejo da água impõe throttling/redução da produção do campo, ao passo que R1 ficou só em restrições genéricas, e a referência é válida sem resposta de bom senso suficiente.

**inventario · dificil_B · R1 correta · R2 correta · atalho** Em uma RAM de compressão no FPSO, um arranjo com um compressor operando e outro de reserva foi tratado como dois blocos paralelos idênticos. Na prática, o reserva só entra após permissivos de partida e comutação, e os dois trens usam a mesma utilidade e o mesmo sistema de controle. O resultado ficou mais otimista que a operação esperada. Que aspecto da representação está faltando para corrigir essa superestimação?

- Referência: Modelar explicitamente o acionamento do reserva e as dependências por utilidades e controle compartilhados.
- R1: Incluir os critérios de ativação sequencial e uso compartilhado de utilidades e controle, que indicam que o treno de reserva só opera após permissivos, para refletir a operação real e evitar superestimações.
- R2: Falta modelar corretamente a redundância “standby com comutação” (1 trem em operação, reserva só após falha/permissivos), incluindo o tempo/condições de comutação e a dependência por utilidades e sistema de controle comum (falhas comuns). Tratar como dois blocos paralelos independentes superestima a disponibilidade.
- Desenho: atraente = Manter o paralelo simplificado e apenas recalibrar os dados numéricos de falha e reparo. | descarta = O reserva só entra após permissivos de partida e comutação, e os dois trens usam a mesma utilidade e o mesmo sistema de controle. | passo oculto = Deduzir que a redundância real não se comporta como paralelo simples, porque o reserva depende de entrada condicionada e de recursos comuns.
- Juiz: Os dois candidatos corrigem a superestimação ao incluir standby com partida/comutação do reserva e dependências por utilidades/controle comuns, elementos que o próprio enunciado já fornece quase literalmente.

**inventario · dificil_B · R1 parcial · R2 correta** Em um FPSO, um arranjo com reserva fria mantém um equipamento longos períodos parado, e por isso ele é tratado informalmente como “garantido”. Como disponibilidade aqui é estar apto quando requerido, e os recursos externos estão assegurados, o histórico mostra perda repetida da função justamente quando o ativo sai e o reserva precisa assumir. Que mecanismo torna essa disponibilidade apenas aparente?

- Referência: Falha de partida/comutação do reserva, deixando-o inapto no momento da demanda e comprometendo a disponibilidade.
- R1: A falta de manutenção preventiva e testes de reserva compromete a real disponibilidade, tornando-a aparente ao neglectar condições operacionais reais, especialmente ao longo de longos períodos de inatividade do equipamento.
- R2: Em reserva fria a “falha sob demanda” não é zero: o ativo entra apenas quando requerido, mas o tempo de comissionamento/partida (pressurização, aquecimento, energização, alinhamentos e verificação de controles) causa demora e chances de não sincronizar na transferência, tornando a disponibilidade aparente.
- Desenho: atraente = Como o reserva quase não desgasta, sua disponibilidade é praticamente garantida. | descarta = A perda de função ocorre repetidamente justamente quando o reserva é requerido para assumir a carga. | passo oculto = Deduzir que, em reserva fria, menor desgaste não garante aptidão sob demanda; se a perda de função aparece ao requerer o reserva, o problema relevante está na entrada em serviço.
- Juiz: O ponto decisivo é a falha sob demanda na partida/comutação do reserva frio, de modo que R2 a explicita, R1 fica apenas na causa contributiva de manutenção/testes, a referência é válida e não há atalho genérico.

**inventario · dificil_B · R1 correta · R2 correta · atalho** Em um FPSO, um trimestre teve campanha com muito mais contratados embarcados e duração total das atividades muito maior que o outro. O total de acidentes ocupacionais mudou entre os trimestres, e a gerência quer comparar o desempenho de segurança entre eles. Com que grandeza os casos devem ser relacionados nessa comparação?

- Referência: Horas-homem de exposição ao risco.
- R1: Devem ser relacionados às horas trabalhadas (taxa de acidentes por hora ou por milhão de horas), para normalizar a comparação.
- R2: Relacionar os acidentes a uma medida de exposição ocupacional, tipicamente frequência: taxa por horas-homem trabalhadas (ex.: acidentes por 1 milhão de horas ou por 200.000 horas), podendo complementar com severidade (dias perdidos por horas).
- Desenho: atraente = Número absoluto de acidentes no período. | descarta = Um dos trimestres teve muito mais contratados embarcados e duração total das atividades muito maior. | passo oculto = Inferir que, com efetivo e duração das atividades diferentes, os acidentes precisam ser comparados pela exposição ao risco e, nesse caso, essa exposição é medida em horas-homem.
- Juiz: A comparação correta é por horas-homem de exposição ao risco, exatamente o denominador usado por ambos, e a necessidade de normalizar por exposição está explícita no enunciado.

**inventario · dificil_A · R1 correta · R2 correta · atalho** Num FPSO, um desemulsificante foi selecionado em laboratório por boa resposta em certa salinidade. Em operação, a mesma dosagem e o mesmo lote passam a entregar pior separação depois de aumento de vazão: a temperatura real no processo mudou, o tempo de residência caiu, o cisalhamento em válvulas e bombas aumentou, o corte de água subiu e entrou outro químico no sistema. Que diagnóstico técnico explica melhor essa mudança?

- Referência: Mudança nas condições reais de processo no FPSO alterou o desempenho do desemulsificante; o resultado de laboratório não se aplica isoladamente.
- R1: A mudança na temperatura e no cisalhamento alteram a eficiência do desemulsificante, reduzindo sua capacidade de separar água; a entrada de outro químico pode interferir na formulação, agravando a deterioração da separação.
- R2: O diagnóstico mais provável é falha cinética: com o aumento de vazão, a temperatura mudou e principalmente o tempo de residência no sistema caiu, não permitindo que o demulsificante desestabilize a emulsão antes do estágio de separação. O maior cisalhamento pode ainda re-emulsionar e o “novo químico” pode antagonizar.
- Desenho: atraente = A família escolhida em laboratório para aquela salinidade perdeu desempenho por uma tendência intrínseca do produto indicada no ensaio. | descarta = A piora coincide com mudanças de temperatura real, tempo de residência, cisalhamento, corte de água e presença de outro químico, apesar de mesma dosagem e mesmo lote. | passo oculto = Inferir que a piora decorre das variáveis operacionais reais do FPSO, que alteram o desempenho do desemulsificante, mesmo com produto e dosagem mantidos.
- Juiz: Ambos atribuem a piora à mudança das condições reais de processo no FPSO, que altera o desempenho do desemulsificante e invalida a extrapolação direta do teste de laboratório, e a referência admite atalho por praticamente resumir os fatores já dados no enunciado.

**inventario · dificil_A · R1 correta · R2 correta · atalho** No separador de produção de um FPSO, a espuma passou a persistir e a elevar o arraste de líquido no gás. O vaso, os internos, as vazões e a queda de pressão de entrada permaneceram nos valores usuais. Em paralelo, a caracterização do fluido indicou aumento de compostos polares e de partículas finas na corrente. Que mecanismo explica essa persistência da espuma?

- Referência: Estabilização do filme líquido por espécies de superfície ativa e impurezas do fluido, tornando a espuma persistente.
- R1: O aumento de compostos polares e partículas finas favorece a formação e estabilidade da espuma, formando uma camada que retarda o desprendimento das bolhas e mantém a espuma persistente mesmo sem mudanças nas condições operacionais.
- R2: A persistência é típica de espuma estabilizada: aumento de componentes polares e finos aumenta a adsorção no filme líquido e reduz a coalescência/ruptura das bolhas (viscosidade superficial e efeito de partículas como “agentes espumantes”). Assim, a drenagem do filme fica lenta e a espuma mantém-se, elevando arraste.
- Desenho: atraente = Geometria do vaso ou regime de escoamento inadequado. | descarta = Vaso, internos, vazões e queda de pressão de entrada permaneceram nos valores usuais. | passo oculto = Inferir que o aumento de compostos polares e partículas finas corresponde à presença de agentes superfície-ativos e impurezas que estabilizam os filmes da espuma.
- Juiz: O ponto central é a estabilização do filme líquido da espuma por espécies de superfície ativa e partículas finas do fluido, reduzindo drenagem e ruptura das bolhas, o que ambos descrevem, e o enunciado já direciona fortemente para esse mecanismo.

**inventario · dificil_A · R1 correta · R2 correta** Num separador do FPSO, a espuma voltou a ocupar o vaso e a equipe associou a perda de desempenho do antiespumante à dose. Porém, a bomba e a concentração na linha foram confirmadas iguais às da campanha anterior. O que mudou foi a chegada de uma nova mistura de óleo, água produzida com condutividade mais alta e maior arraste de finos. Que fator explica melhor essa piora de desempenho?

- Referência: A composição do sistema; sais, finos e componentes de superfície podem estabilizar a espuma e dificultar o contato do antiespumante com o filme.
- R1: O aumento da condutividade e o maior arraste de finos podem gerar maior estabilidade da espuma, dificultando o desempenho do antiespumante mesmo com a mesma dose, devido à formação de filmes mais resistentes.
- R2: A maior carga de finos (sólidos/partículas) do novo óleo: eles adsorvem o antiespumante e estabilizam a película interfacial, consumindo mais agente e impedindo a quebra da espuma, mesmo com bomba e dose/concentração na linha corretas.
- Desenho: atraente = Dose insuficiente do antiespumante. | descarta = A bomba e a concentração na linha foram confirmadas iguais às da campanha anterior, enquanto mudaram a mistura de óleo, a condutividade da água produzida e o arraste de finos. | passo oculto = Inferir que, com dose efetivamente mantida, a mudança de desempenho decorre das propriedades interfaciais alteradas pela nova composição do fluido, não da dosagem em si.
- Juiz: A referência é válida e pede o mecanismo técnico de mudança de composição do sistema, com sais/finos estabilizando a espuma e dificultando a ação do antiespumante, o que ambos explicaram adequadamente.

**inventario · dificil_A · R1 incorreta · R2 correta** Em um FPSO, após semanas injetando água do mar por bypass da SRU durante manutenção, produtores da mesma região passaram a perder produtividade e surgiram depósitos duros em linhas e equipamentos. Não houve aumento de areia, corrosão nem mudança relevante de temperatura. As amostras do depósito e da água produzida mostram bário e estrôncio, e o setor recebe mistura com água de formação. Que mecanismo químico específico explica essa incrustação?

- Referência: Incompatibilidade iônica entre água do mar injetada sem SRU e água de formação rica em Ba/Sr, com precipitação de sulfatos pouco solúveis.
- R1: A precipitação de minerais de bário e estrôncio, formando depósitos duros, ocorre por saturação devido à introdução de água do mar enriquecida com esses íons, promovendo a formação de sais insolúveis ao eliminar compostos tamponantes durante manutenção.
- R2: Precipitação por mistura de águas (incrustação de sulfatos): em presença de sulfato dissolvido, ocorre reação de dupla troca e formação de barita e celestita—Ba2+ + SO4^2- → BaSO4(s) e Sr2+ + SO4^2- → SrSO4(s).
- Desenho: atraente = Deposição genérica de sólidos ou outro depósito não relacionado ao que a SRU remove. | descarta = O cenário combina injeção sem SRU com contato com água de formação e presença de bário e estrôncio nas amostras, sem sinais de areia, corrosão ou efeito térmico. | passo oculto = Inferir que o bypass da SRU manteve sulfato dissolvido na água injetada, que ao encontrar Ba/Sr da outra água precipita incrustação.
- Juiz: A incrustação decorre especificamente da incompatibilidade entre sulfato da água do mar sem SRU e Ba/Sr da água de formação, precipitando sulfatos pouco solúveis, e R1 erra ao atribuir os íons ao lado errado e acrescentar explicação espúria.

**inventario · dificil_A · R1 correta · R2 correta · atalho** Após avanço da água de injeção em um poço produtor do FPSO, surge depósito mineral com perda de produtividade. A água produzida passa a conter sulfato típico da água do mar, enquanto a água de formação desse poço é rica em bário. No mesmo período, a URS não mostra queda de fluxo nem aumento de passagem de íons nas membranas. Que depósito específico esse quadro favorece no poço?

- Referência: BaSO4 (barita), pela mistura de água do mar com sulfato e água de formação com bário no poço produtor.
- R1: Formação de depósitos de barita (sulfato de bário) precipitados pela interação da água injetada com bário na formação, formando incrustações que reduzem a produtividade.
- R2: O quadro favorece incrustação de **sulfato de bário (BaSO₄, barita)**: a água de injeção/carregada de sulfato reage com o bário presente na água de formação, formando precipitado insolúvel que reduz a permeabilidade e a produtividade. URS sem queda sugere não ser incrustação que afete fortemente a membrana.
- Desenho: atraente = Incrustação genérica por sais pouco solúveis ou depósito associado às membranas da URS. | descarta = A mistura entre água do mar com sulfato e água de formação rica em bário é observada no poço produtor, enquanto a URS não apresenta sintomas de incrustação nas membranas. | passo oculto = Inferir que a incrustação decorre da mistura, no poço produtor, entre sulfato da água do mar e bário da água de formação, formando barita.
- Juiz: O decisivo era identificar barita pela mistura de sulfato da água do mar com bário da água de formação, que R1 e R2 trouxeram corretamente; a referência é válida e há atalho genérico porque o enunciado praticamente aponta diretamente para BaSO4.

**inventario · dificil_A · R1 incorreta · R2 correta · atalho** Em um FPSO, a água tratada passou a apresentar oxigênio residual após alguns dias usando bissulfito de sódio de um tanque diário ventilado. A análise da solução na descarga da bomba mostrou a mesma concentração ativa da solução recém-preparada; no mesmo período, o oxigênio dissolvido na água de entrada aumentou e a vazão de injeção do químico ficou inalterada. Qual causa específica tende a explicar esse residual?

- Referência: Dosagem de bissulfito abaixo da necessidade imposta pela carga de oxigênio presente.
- R1: Diminuição da eficácia do bissulfito de sódio devido à presença de oxigênio causado por entrada de ar ou cavitação, reduzindo sua capacidade de remover oxigênio residual na água.
- R2: A causa mais provável é o aumento do O₂ dissolvido na água de entrada (carga oxidante maior que a estequiometria do bissulfito). Como a concentração ativa na descarga do ponto de dosagem está igual e a vazão de injeção não mudou, o bissulfito é consumido totalmente antes de toda a água tratada, restando O₂ residual.
- Desenho: atraente = Degradação da solução de bissulfito durante o armazenamento no tanque diário ventilado. | descarta = A solução medida na descarga da bomba manteve a mesma concentração ativa da recém-preparada; o que mudou foi o teor de oxigênio de entrada, sem ajuste da injeção. | passo oculto = Inferir que, com concentração ativa preservada, aumento do oxigênio na água de entrada e injeção inalterada, a razão de bissulfito disponível por oxigênio ficou abaixo da necessária.
- Juiz: A referência é válida e o decisivo é subdosagem de bissulfito frente ao aumento da carga de O₂, por isso R2 acerta e R1 erra ao atribuir perda de eficácia/entrada de ar, havendo atalho por associação direta entre O₂ maior e vazão de químico inalterada.

**inventario · dificil_A · R1 correta · R2 correta** Em um FPSO, após introduzir um novo produto para controle de biofilme na água de injeção, surgiram espuma persistente no separador, aumento de óleo na água produzida e piora do perfil ecotoxicológico do descarte. Vazão, nível de interface, agitação e características do fluido produzido não mudaram. Com que característica do produto esse quadro é mais compatível?

- Referência: Presença de surfactantes no biocida; eles podem gerar espuma, piorar a separação óleo-água e aumentar a toxicidade aquática.
- R1: O quadro é compatível com um produto que tenha surfactantes que aumentam a estabilidade da espuma, promovem o entrelaçamento de óleos e podem impactar negativamente a ecotoxicidade do descarte.
- R2: Mais compatível com um produto que funcione como tensoativo (surfactante), tipicamente de natureza catiônica (ex.: quaternários de amônio), capaz de estabilizar espuma no separador e aumentar arraste de óleo para a água produzida, piorando o impacto ecotoxicológico do descarte.
- Desenho: atraente = Perturbação mecânica no separador ou variação do fluido de processo. | descarta = Vazão, nível de interface, agitação e características do fluido permaneceram sem mudança relevante, e o perfil ecotoxicológico piorou após a introdução do produto. | passo oculto = Inferir que, sem mudança mecânica nem do fluido, a combinação de espuma, pior separação e pior ecotoxicidade aponta para surfactantes no produto de controle de biofilme.
- Juiz: O quadro é típico de biocida com caráter surfactante, que espuma, atrapalha a separação óleo-água e piora a ecotoxicidade, exatamente o que ambos identificaram.

**inventario · dificil_A · R1 parcial · R2 correta** Na água de injeção de um FPSO, as contagens microbiológicas caem após cada aplicação e voltam a subir antes do ciclo seguinte. Os isolados continuam suscetíveis ao produto e a compatibilidade química do programa foi confirmada. Em pontos remotos, o residual ativo desaparece cedo, e inspeções mostram incrustações aderidas em trechos do circuito. Que mecanismo explica essa persistência da população?

- Referência: Alcance efetivo insuficiente do biocida — falta permanência nas áreas críticas e as incrustações resguardam microrganismos, permitindo persistência ou recuperação.
- R1: A formação de biofilme nas incrustações protege microrganismos, permitindo que permaneçam resistentes às quatidades de biocida, mesmo após aplicações sucessivas.
- R2: Formação/recrescimento de biofilme e células sésseis aderidas (protegidas por EPS), que consomem/neutralizam rapidamente o biocida. Assim, o residual ativo some cedo em pontos remotos, enquanto a população persiste e volta a crescer antes do próximo ciclo.
- Desenho: atraente = Necessidade de trocar imediatamente o biocida por outro produto. | descarta = Os isolados seguem suscetíveis e a compatibilidade foi confirmada, enquanto o residual some cedo em pontos remotos e há incrustações aderidas no circuito. | passo oculto = Inferir que a recuperação microbiológica decorre de o tratamento não atingir nem permanecer adequadamente nas regiões contaminadas, com abrigo físico em incrustações, e não de troca imediata de produto.
- Juiz: A persistência decorre de alcance efetivo insuficiente do biocida nas áreas críticas, com residual ativo que some cedo e microrganismos protegidos em incrustações/biofilme, quadro que R2 descreveu por completo e R1 só abordou parcialmente ao citar proteção por biofilme e ainda sugerir 'resistência'.

**inventario · dificil_A · R1 parcial · R2 correta** Na malha de água de injeção, a contagem microbiana a jusante da dosagem segue alta. A concentração ativa do biocida na linha está conforme, seus produtos de decomposição e a compatibilidade com os demais químicos foram verificados, e não houve espuma nem piora da separação óleo-água. Em um trecho com lançador/recebedor disponível, a inspeção indicou material orgânico aderido e incrustação mineral. Que intervenção tende a aumentar a efetividade do biocida nesse trecho?

- Referência: Limpeza mecânica com pig; ao remover material aderido e incrustação, tende a reduzir a barreira física ao acesso do biocida.
- R1: Realizar limpeza física com jatos de água ou solventes específicos para remover matéria orgânica e incrustações, seguido de ajuste na dosagem de biocida para garantir contato eficaz.
- R2: Aumentar a efetividade tende a exigir remoção do filme/depósitos (scaling e matéria orgânica) no trecho: limpeza mecânica ou “pigging”/escovamento e, se compatível, choque químico (biocida oxidante ou pré-tratamento dispersante/quelante) antes da manutenção com o biocida.
- Desenho: atraente = Troca do biocida por incompatibilidade intrínseca com o processo. | descarta = A concentração ativa, os produtos de decomposição e a compatibilidade com outros químicos já foram verificados, sem espuma nem piora da separação, e há depósitos aderidos em trecho com lançador/recebedor disponível. | passo oculto = Inferir que, com biocida ativo e compatível, a limitação dominante passa a ser o bloqueio físico por depósitos em trecho acessível à limpeza interna.
- Juiz: R2 acerta ao apontar a remoção mecânica de depósitos, especialmente por pigging no trecho com lançador/recebedor, para reduzir a barreira física ao biocida, enquanto R1 fica em limpeza genérica e não chega ao elemento decisivo do pig.

**inventario · dificil_A · R1 correta · R2 correta · atalho** Num FPSO, o MEG regenerado volta com concentração na fase aquosa e balanço de água dentro da faixa, e a operação do regenerador segue estável. Ainda assim, no circuito real persistem aumento de condutividade e depósitos inorgânicos. Que necessidade técnica não pode ser considerada automaticamente atendida só porque a água foi removida?

- Referência: Remoção de sais: sua necessidade deve ser avaliada separadamente da regeneração, que apenas retira água para permitir o reúso do MEG.
- R1: A remoção de água não garante a eliminação completa de íons inorgânicos e sólidos dissolvidos responsáveis pela formação de depósitos e aumento de condutividade.
- R2: Não pode ser considerada atendida automaticamente a necessidade de controlar a composição iônica (sais/dureza, sílica, metais) e, portanto, a prevenção de incrustações e corrosão. Remover “água” não garante que os contaminantes dissolvidos responsáveis por condutividade e depósitos inorgânicos foram eliminados.
- Desenho: atraente = Nenhuma adicional; a própria regeneração já resolveu automaticamente o problema de sais. | descarta = Mesmo com regeneração estável, concentração e balanço de água adequados, persistem aumento de condutividade e depósitos inorgânicos no circuito real. | passo oculto = Inferir que recuperar concentração de MEG e balanço de água comprova desidratação para reúso, mas não tratamento dos inorgânicos dissolvidos.
- Juiz: O ponto central é que regeneração remove água, não necessariamente sais/íons, portanto ambos acertam a necessidade separada de remoção de sais/controle iônico; a referência é válida e a resposta sai quase por associação direta com condutividade e depósitos.

**inventario · dificil_A · R1 correta · R2 correta** Após iniciar injeção de MEG, um trecho com água livre deixou de apresentar tampões de hidrato. No ponto crítico, pressão e temperatura permaneceram na mesma faixa do período anterior, e as amostras mostraram o glicol concentrado na água separada. Que mecanismo explica a maior dificuldade de formar hidrato nesse trecho?

- Referência: Concentração do MEG na fase aquosa, reduzindo a atividade da água e dificultando termodinamicamente a formação de hidratos nas mesmas condições externas.
- R1: A injeção de MEG reduz a atividade do água, dificultando a formação do hidrato ao remover o potencial de hidratação, mesmo com condições próximas ao ponto crítico, devido ao efeito de mareante do glicol concentrado.
- R2: Inibição química por MEG: o glicol reduz a atividade da água (deprime o equilíbrio de hidrato), deslocando a condição necessária de formação. Assim, mesmo com P/T inalterados, a menor atividade de água na interface gás–água impede nucleação e crescimento dos hidratos no trecho.
- Desenho: atraente = Mudança das condições externas de pressão e temperatura. | descarta = As medições no ponto crítico permaneceram na mesma faixa de pressão e temperatura do período anterior, enquanto o glicol apareceu concentrado na água separada. | passo oculto = Inferir que, como pressão e temperatura não mudaram e o MEG se concentrou na água livre, a redução da tendência a hidrato vem da alteração da atividade da água.
- Juiz: Ambos trazem o mecanismo correto de inibição termodinâmica por concentração de MEG na fase aquosa, com redução da atividade da água e maior dificuldade de formar hidrato mesmo em P/T semelhantes.

**inventario · dificil_A · R1 incorreta · R2 correta** Num trecho de aço carbono do tratamento de gás de um FPSO, a taxa de corrosão dos cupons subiu mesmo com a vazão do inibidor orgânico e o ponto de injeção inalterados, sem falha da bomba. No mesmo período, a fase aquosa passou a receber mais glicol e apresentou salinidade maior. Que mecanismo explica melhor a perda de proteção?

- Referência: Alteração da eficiência do inibidor pela mudança do meio, comprometendo adsorção e continuidade do filme protetor.
- R1: Aumento da salinidade, levando à formação de camadas de sal na superfície, supera a ação do inibidor orgânico, reduzindo sua efetividade e aumentando a corrosão.
- R2: Aumento de salinidade e de fração aquosa tende a intensificar a desadsorção/diluição do inibidor na interface aço‑líquido: íons (Cl−, etc.) competem pelos sítios e elevam a condutividade, debilitando o filme protetor. Assim, mesmo com vazão/injeção nominal inalteradas, a proteção efetiva cai.
- Desenho: atraente = Dosagem inadequada do inibidor. | descarta = A vazão do inibidor e o ponto de injeção permaneceram inalterados, sem falha da bomba, enquanto a fase aquosa mudou de composição e salinidade. | passo oculto = Inferir que, com dosagem e injeção estáveis, a piora decorre da sensibilidade do inibidor às mudanças da fase aquosa, não de falta de produto.
- Juiz: O mecanismo decisivo é a perda de adsorção/continuidade do filme do inibidor por mudança do meio com mais glicol e salinidade, descrito por R2, enquanto R1 troca isso por formação de camada de sal, que é outro mecanismo.

**inventario · dificil_A · R1 parcial · R2 correta** Após um squeeze, o fósforo na água produzida aumenta nas primeiras coletas e, em seguida, cai de modo consistente. As amostras são representativas, as duplicatas concordam, o método analítico é o mesmo e não houve intervenção nem mudança de regime do poço. A que mecanismo esse comportamento aponta?

- Referência: Liberação do inibidor retido na formação, seguida de diluição na água produzida.
- R1: Indica liberação residual de fósforo de sedimentos ou rochas após o squeeze, que inicialmente mobiliza fósforo disponível, seguido de estabilização à medida que o fósforo é removido ou sedimenta, refletindo o equilíbrio entre liberação e remoção.
- R2: Indica “lixiviação/liberação inicial” de fósforo (fosfatos) associada ao fluido/contaminante do squeeze ou a depósitos na formação/biofilme, seguida por “lavagem/diluição e remoção” nas coletas posteriores, levando a queda consistente sem novo aporte ou mudança de regime do poço.
- Desenho: atraente = Falha analítica ou de amostragem. | descarta = Amostras representativas, duplicatas concordantes, método analítico inalterado e ausência de intervenção ou mudança de regime. | passo oculto = Inferir que, com amostragem representativa e resultados reprodutíveis, o pico inicial seguido de queda reflete o comportamento do inibidor na formação e não um artefato de medição.
- Juiz: O mecanismo esperado é a liberação do inibidor retido na formação seguida de diluição na água produzida; R1 só se aproxima ao citar liberação inicial, mas erra a origem e a queda, enquanto R2 descreve adequadamente liberação inicial do squeeze com lavagem/diluição, e o item não admite resposta genérica.

**inventario · dificil_A · R1 parcial · R2 correta** Dois tanques receberam a mesma água produzida. Após semanas, o tanque A permaneceu fechado e sem renovação; o B operou com renovação normal. Na verificação, só o A apresenta H2S no espaço de vapor e início de ataque interno. A explicação imediata seria a composição original do fluido. Que mecanismo fica mais compatível com esse quadro?

- Referência: Proliferação de bactérias redutoras de sulfato no tanque fechado com acúmulo prolongado da água produzida, gerando H2S.
- R1: A acumulação de H2S no tanque A devido à ausência de renovação favorece a produção microbiológica anaeróbica, onde microrganismos específicos convertem compostos orgânicos em H2S, levando ao ataque interno e à presença de gás sulfídrico.
- R2: Mais compatível: corrosão microbiana (SRB) em condição anaeróbia no tanque A, com geração de H2S no líquido e migração para o espaço de vapor. A ausência de renovação permite acúmulo/elevação de concentração e acelera o ataque interno; no B, a renovação remove/mitiga.
- Desenho: atraente = A composição original do fluido armazenado. | descarta = Somente o tanque que ficou fechado e sem renovação por semanas apresentou H2S, embora ambos tenham recebido a mesma água produzida. | passo oculto = Inferir que, como a mesma água só apresentou H2S no tanque fechado e estagnado por semanas, a origem mais compatível é geração durante o armazenamento por atividade microbiana.
- Juiz: O quadro é mais compatível com atividade de bactérias redutoras de sulfato em condição anaeróbia no tanque fechado; R2 explicita isso, R1 fica em produção microbiológica genérica, e o item é válido sem atalho.

**inventario · dificil_A · R1 correta · R2 correta** Num FPSO, um tanque fechado que manuseia água produzida e água segregada permaneceu vários dias com baixa renovação. Surgiu H2S no espaço de gás e na descarga do tanque, mas amostras repetidas da linha de entrada, coletadas antes do armazenamento, vieram sem H2S detectável. Com qual mecanismo esse quadro é mais compatível?

- Referência: Atividade de bactérias redutoras de sulfato no próprio tanque, favorecida pelo tempo de residência elevado em ambiente fechado.
- R1: Formação bacteriana anaeróbica no tanque indica sulfato-redução, produzindo H2S, especialmente em baixa renovação e atmosfera fechada.
- R2: Mais compatível com “souring” bacteriano: redução biológica de sulfatos por bactérias redutoras de sulfato durante o armazenamento com baixa renovação, gerando H2S no volume líquido e liberando para o espaço de gás e para a descarga.
- Desenho: atraente = H2S já vinha contaminando o fluido de processo a montante. | descarta = As amostras repetidas da linha de entrada antes do tanque vieram sem H2S detectável, enquanto o H2S apareceu após vários dias de baixa renovação. | passo oculto = Inferir que, se o H2S não está na alimentação e aparece após permanência prolongada em tanque fechado de água produzida/segregada, a fonte mais compatível é geração interna por BRS.
- Juiz: Os dois identificam corretamente souring por bactérias redutoras de sulfato gerando H2S dentro do próprio tanque, favorecido pelo alto tempo de residência em ambiente fechado, que é o mecanismo específico pedido.

**inventario · dificil_A · R1 incorreta · R2 correta** No circuito de água do mar de um FPSO, o residual oxidante no retorno segue na meta. Mesmo assim, aumentam taxa de corrosão e sinais de deposição. Vazão, calibração e concentração das soluções de inibidor de corrosão e dispersante foram confirmadas na entrada do sistema; a mudança recente foi elevar fortemente a injeção de hipoclorito para sustentar aquele residual diante de maior demanda da água. Que mecanismo explica a queda de proteção global?

- Referência: Degradação oxidativa do inibidor e do dispersante pela alta dosagem de hipoclorito, reduzindo a proteção global apesar do residual aparente adequado.
- R1: A elevação do hipoclorito aumenta a formação de óxidos de ferro e resíduos que podem comprometer a eficiência do inibidor, reduzindo a proteção contra corrosão e promovendo deposições.
- R2: Provável mecanismo: o aumento de hipoclorito elevou o agente oxidante (HOCl/OCl−), que degrada quimicamente e/ou impede a adsorção do inibidor na superfície metálica (remoção do filme passivante/protetor). Com menos cobertura e mais oxidação local, cresce a corrosão e surgem depósitos mais porosos (espécies oxidada/precipitados), reduzindo a proteção global.
- Desenho: atraente = Dosagem insuficiente de inibidor de corrosão ou de dispersante. | descarta = Vazão, calibração e concentração desses dois químicos foram confirmadas; a única mudança relevante foi o forte aumento de hipoclorito para manter o mesmo residual. | passo oculto = Inferir que, com inibidor e dispersante confirmados na entrada e piora após forte aumento de hipoclorito, o oxidante passou a consumir a eficácia desses químicos no sistema.
- Juiz: O ponto decisivo era a sobredosagem de hipoclorito oxidar/degradar o pacote químico de proteção, por isso R2 acerta ao apontar degradação do inibidor e R1 erra ao focar em formação de óxidos de ferro; a referência é válida e não há atalho genérico.

**inventario · dificil_A · R1 correta · R2 parcial** Em um circuito de água de um FPSO, a água passou a chegar com alta carga de nutrientes e, em seguida, aumentaram a corrosão e a indicação de deposição. No mesmo período, cresceu a contagem de bactérias aeróbias; depois que a qualidade da água foi recuperada e a adição de hipoclorito aumentou, esses indicadores voltaram ao normal. Que mecanismo específico explica melhor a piora observada?

- Referência: Deficiência de biocida, favorecendo crescimento microbiológico em água com alta carga de nutrientes e, daí, deposição e corrosão.
- R1: A proliferação de bactérias aeróbias, devido ao aumento de nutrientes, promove corrosão microbiológica (MIC) e deposição de biocálculos, agravada pela redução da biocida, resultando na piora do circuito.
- R2: O mecanismo mais provável é MIC por biofilme: o aumento de nutrientes favorece crescimento de bactérias aeróbias, que formam biofilme (fouling) e criam gradientes de O₂/diferencial de aeração, acelerando corrosão e promovendo deposição; ao elevar hipoclorito, ocorre controle microbiológico e recuperação dos indicadores.
- Desenho: atraente = Piora físico-química da água causando deposição e corrosão por mecanismo não microbiológico. | descarta = A contagem de bactérias aeróbias cresceu e voltou ao normal junto com corrosão e deposição após recuperar a qualidade da água e aumentar o hipoclorito. | passo oculto = Inferir que a combinação de alta carga de nutrientes, aumento de bactérias e normalização após mais hipoclorito aponta falha no controle microbiológico como origem comum de depósitos e corrosão.
- Juiz: A referência válida exige insuficiência de biocida em água com alta carga de nutrientes como causa da piora microbiológica; R1 inclui esse ponto, enquanto R2 descreve MIC por biofilme mas não explicita a deficiência de biocida como elemento decisivo.

**inventario · dificil_A · R1 correta · R2 correta** Num FPSO, a sonda ER de um spool da água produzida mostrou maior perda metálica nos períodos em que o pH caiu. Em outro spool, sob oscilações de pH parecidas, a resposta não se repetiu; os dois diferem em metalurgia, fração de água, composição do fluido, temperatura e regime de escoamento. Um técnico quer transformar a correlação do primeiro spool em regra fixa para todo o sistema. Que explicação técnica esse conjunto sustenta para o aumento observado no primeiro spool?

- Referência: Resposta corrosiva específica do circuito com fase aquosa; pH mais baixo pode elevar a perda metálica por alterar reações eletroquímicas e filmes, não como regra universal.
- R1: A queda de pH aumenta a corrosividade, acelerando a perda metálica, especialmente em materiais suscetíveis, como o primeiro spool, devido à maior agressividade do meio em condições específicas de metalurgia e regime.
- R2: O aumento de perda metálica no primeiro spool, quando o pH cai, é consistente com corrosão acelerada por CO2/H2S em meio mais ácido: maior atividade de H+ aumenta a dissolução do metal e desestabiliza filmes/passivação e produtos de corrosão (sob depósitos), elevando a taxa de corrosão. A não repetição no outro spool indica dependência de mecanismo, metalurgia, água/cloretos, temperatura e escoamento.
- Desenho: atraente = Uma regra universal de que toda queda de pH sempre aumenta a corrosão da mesma forma em qualquer sistema. | descarta = Outro spool, com metalurgia, fração de água, composição, temperatura e escoamento diferentes, não reproduziu a mesma resposta apesar de oscilações de pH semelhantes. | passo oculto = Inferir que a correlação entre queda de pH e perda metálica no primeiro spool é dependente das condições daquele sistema, não uma lei transferível para qualquer circuito.
- Juiz: A referência é válida e o conjunto sustenta uma resposta corrosiva dependente daquele circuito e da presença de fase aquosa, em que pH mais baixo pode elevar a perda metálica por afetar reações/filmes sem virar regra universal; ambos capturam essa especificidade e um atalho genérico do tipo 'ácido corrói mais' não bastaria.

**inventario · dificil_B · R1 incorreta · R2 parcial · ref. inválida** Em um FPSO, passou-se a dosar continuamente inibidor de incrustação na água de injeção. A taxa de dosagem permanece conforme o programa, mas a incrustação segue aparecendo no lado produtor e as amostras desse lado não confirmam presença do químico onde a mistura incompatível se forma. Que mecanismo explica a falha dessa estratégia em proteger a produção?

- Referência: Adsorção do inibidor na rocha ao redor do injetor, deixando-o indisponível na fase aquosa para proteger o produtor.
- R1: A inibição de incrustação pode ser ineficaz devido à formação de camadas impenetráveis ou incompatibilidade do químico na fase de produção, permitindo que incrustações se formem antes de a inibição atuar, mesmo com dosagem contínua na água de injeção.
- R2: Falha por não chegar ao ponto de nucleação: ocorre segregação/curto-circuito de fluxos ou má distribuição do inibidor na água injetada, gerando uma zona de mistura incompatível sem concentração efetiva (diluição, bypass e “dead volumes”), consumindo/evitando contato do químico antes da formação da incrustação.
- Desenho: atraente = Subdosagem geral do inibidor na água de injeção. | descarta = A taxa de dosagem foi mantida, mas as amostras do lado produtor não confirmam presença do químico no ponto crítico. | passo oculto = Inferir que o inibidor está sendo retido na formação próxima ao injetor e, por isso, não permanece disponível na fase aquosa até o ponto crítico no produtor.
- Juiz: A referência exige retenção do inibidor por adsorção na rocha próxima ao injetor, que R1 não aborda e R2 só tangencia ao dizer que o químico não chega ao ponto, porém por outro mecanismo; a referência fica estreita porque outras perdas de transporte também poderiam explicar o quadro, e não há atalho genérico.

**inventario · dificil_B · R1 incorreta · R2 parcial** Em um FPSO, a água produzida está sendo reinjetada com co-injeção de água do mar, sem unidade de dessulfatação. A restrição de injeção surge nos poços injetores durante essa operação, e não como um caso inicialmente percebido em produtores. Que local específico passa a ser o principal alvo da proteção com inibidor?

- Referência: Os pontos de mistura de águas incompatíveis nos poços injetores.
- R1: O local específico principal alvo da proteção com inibidor é a tubulação de fluxo, especialmente os poços injetores, para evitar corrosão devido à água produzida com sal e contaminantes.
- R2: Com a reinjeção por co-injeção sem dessulfatação, o H2S permanece e passa a corroer principalmente no poço injetor: a região da completaçao/injeção (tubing e liner, próximo à face do reservatório) e seus trechos internos onde ocorre mistura e reação dos fluidos.
- Desenho: atraente = apenas os poços produtores | descarta = a restrição de injeção está surgindo nos poços injetores durante a co-injeção, não primeiro nos produtores | passo oculto = Inferir que a co-injeção desloca o risco clássico de BaSO4 para o lado da injeção e concentra a proteção no ponto em que as duas correntes se encontram nos injetores.
- Juiz: A referência é válida e o ponto decisivo é proteger os pontos de mistura de águas incompatíveis dentro dos injetores; R1 desloca o problema para corrosão em linhas/poços de forma genérica, R2 só acerta parcialmente ao localizar a mistura no injetor mas com mecanismo errado, e 'poço injetor' sozinho não basta.

**inventario · dificil_B · R1 incorreta · R2 correta · atalho** Após retorno de mangueiras em uma área com dosagem de oxidante para desinfecção e de bissulfito para desoxigenação, o consumo de bissulfito aumentou e passou a aparecer oxigênio residual a jusante. A concentração da solução e a regulagem de dosagem do bissulfito foram verificadas sem mudança, e a carga de oxigênio da água de entrada permaneceu estável. Que mecanismo específico deve ser investigado como causa desse quadro?

- Referência: Contaminação cruzada com cloro residual consumindo o bissulfito antes da desoxigenação.
- R1: Aoxigenação devida à degradação do oxidante residual ou reação do bissulfito com compostos presentes, gerando oxigênio residual, deve ser investigada.
- R2: Investigar “carry-over”/contaminação de oxidante pelas mangueiras/linhas retornadas (resíduo de cloro/oxidante na tubulação), que reage com o bissulfito consumindo-o e gerando breakthrough: oxigênio residual a jusante por excesso de oxidante após a desoxigenação.
- Desenho: atraente = A água de entrada passou a trazer mais oxigênio dissolvido. | descarta = A carga de oxigênio da água de entrada permaneceu estável no período. | passo oculto = Inferir que o bissulfito está sendo consumido por uma reação paralela, gerando subdosagem efetiva mesmo sem aumento da carga de oxigênio de entrada.
- Juiz: O elemento decisivo era carry-over/contaminação cruzada de oxidante-cloro pelas mangueiras ou linhas retornadas consumindo o bissulfito antes da desoxigenação, então R2 acerta e R1 erra o mecanismo, e o enunciado praticamente conduz a essa associação.

**inventario · dificil_B · R1 correta · R2 correta** Em uma linha de água de injeção cuja geometria inviabiliza pigging, o controle microbiológico é químico. Após cada dosagem de biocida, a contagem microbiana cai, mas só volta a subir no mesmo trecho, onde há indícios de material aderido e depósitos. Que condição local explica essa recorrência?

- Referência: Regiões protegidas por depósitos e biofilme, onde o biocida não atinge concentração efetiva.
- R1: A formação de biofilmes aderidos a depósitos favorece a proteção microbiana contra biocidas, permitindo o ressurgimento da contagem após a sua aplicação.
- R2: Regrowth a partir de biofilme e células remanescentes protegidas em depósitos/material aderido (microambiente com baixa penetração do biocida), que se reativam após a dosagem e recolonizam o trecho.
- Desenho: atraente = O biocida é intrinsecamente ineficaz. | descarta = A contagem cai após cada dosagem e a recorrência fica concentrada no trecho inacessível com depósitos. | passo oculto = Inferir que o material aderido e os depósitos limitam o alcance e o tempo de contato do biocida no trecho, deixando nichos de sobrevivência microbiana.
- Juiz: A condição local relevante são nichos protegidos por depósitos e biofilme com baixa penetração do biocida, o que ambos os candidatos identificaram, e a questão pede esse mecanismo específico, não um conselho genérico.

**inventario · dificil_B · R1 correta · R2 correta** Em um sistema de água de injeção de FPSO, o residual de biocida é monitorado on-line na linha principal, logo após a injeção, e aparece compatível com a dosagem prevista. Mesmo assim, a extremidade de um ramal lateral onde os depósitos reaparecem volta a mostrar alta contagem microbiológica. Sem mudar produto nem dose, que mecanismo explica essa coexistência?

- Referência: Zonas mortas ou má distribuição, deixando a extremidade do ramal sem concentração ativa suficiente apesar do residual adequado na linha principal.
- R1: Possível formação de biofilmes ou áreas de baixa circulação no ramal, protegendo micro-organismos e dificultando o contato do biocida, mesmo com dosagem adequada na linha principal.
- R2: Coexistência ocorre por penetração incompleta do biocida no ramal (dead leg/baixa vazão e mistura). Microrganismos já estabelecidos em biofilme/entupimentos ficam protegidos por EPS e liberam células ao longo do tempo, enquanto a linha principal, bem misturada e com maior contato, mantém residual compatível.
- Desenho: atraente = Resistência microbiana como causa principal. | descarta = O residual é acompanhado na linha principal logo após a injeção, enquanto a alta contagem reaparece na extremidade de um ramal lateral. | passo oculto = Inferir que a leitura na linha principal logo após a injeção não garante a concentração ativa no ramal onde a contaminação persiste.
- Juiz: R1 e R2 acertam ao apontar baixa circulação/dead leg no ramal, com biofilme como agravante, deixando a extremidade sem concentração ativa suficiente apesar do residual adequado na linha principal; a referência é válida e não há atalho genérico porque é preciso distinguir residual global de distribuição local.

**inventario · dificil_B · R1 incorreta · R2 correta** Em uma malha aquosa do FPSO, o controle microbiológico usa oxidante e existe dosagem contínua de inibidor de corrosão. Para manter o residual oxidante na faixa esperada, a dosagem do oxidante foi elevada; depois disso, os sinais de corrosão subiram, sem mudança relevante do regime. Nesse quadro, que mecanismo final específico deixou de atuar sobre o metal?

- Referência: Perda da película adsorvida do inibidor de corrosão na superfície metálica.
- R1: O mecanismo de formação de filmes de passivação através do oxidação controlada foi comprometido, pois o excesso de oxidante pode destrui-los, reduzindo a proteção corrosiva do metal.
- R2: Provavelmente a camada protetora do inibidor (filme adsorvido/passivante na superfície do metal) deixou de se manter: o aumento do oxidante oxidou/degradou o inibidor ou removeu o filme, reduzindo a proteção e permitindo retomada da corrosão.
- Desenho: atraente = Proteção global adequada porque o residual oxidante ficou na faixa esperada. | descarta = Os sinais de corrosão aumentaram logo após elevar a dosagem do oxidante, embora o residual parecesse bom e o regime não tivesse mudado. | passo oculto = O aumento excessivo do oxidante comprometeu o inibidor de corrosão em uso.
- Juiz: O mecanismo específico é a perda do filme adsorvido do inibidor sobre o metal, explicitado por R2, enquanto R1 troca isso por passivação oxidativa; a referência é válida e requer esse mecanismo, sem caber resposta genérica.

**inventario · dificil_B · R1 parcial · R2 correta** Em uma flotação de água produzida, o TOG da água tratada aumentou logo após a equipe elevar apenas a dosagem de coagulante/floculante. Vazão, carga de óleo na entrada e condições de geração de bolhas permaneceram sem mudança relevante. A decisão anterior partia da premissa de que mais químico sempre melhoraria a remoção. Que mecanismo explica essa piora?

- Referência: reestabilização da dispersão por superdosagem
- R1: A superdosagem de coagulante/floculante pode destabilizar a formação de flocos, impedindo a formação adequada de bolhas de ar e reduzindo a eficiência da remoção de óleo na flotação, levando ao aumento do TOG na água tratada.
- R2: Provável “overdosing”: excesso de coagulante/floculante satura a superfície das gotículas e promove reversão de carga (restabilização da emulsão), gerando flocos menores/mais frágeis e coalescência pior. Com isso, menos óleo ascende na flotação e o TOG do efluente aumenta.
- Desenho: atraente = ainda falta aumentar mais a dose | descarta = o desempenho piorou justamente depois do aumento isolado da dosagem, com vazão, carga de óleo e geração de bolhas estáveis | passo oculto = Inferir que, se o TOG piorou depois de aumentar só a dosagem com as demais variáveis estáveis, a dose ultrapassou a janela ótima e entrou em regime de superdosagem.
- Juiz: O mecanismo decisivo era a reestabilização da dispersão por superdosagem; R2 traz isso, R1 apenas descreve piora genérica de flocos/bolhas, e o item é válido sem atalho.

**inventario · dificil_B · R1 incorreta · R2 correta** Em um circuito aquoso de um FPSO, houve queda transitória de pH e, nesse intervalo, a sonda RE passou a registrar maior perda de espessura. Depois o pH retornou ao patamar anterior, mas a leitura da sonda não recuou na mesma rapidez, sem outro indício claro de falha instrumental. Que leitura técnica explica esse descompasso?

- Referência: O dano metálico é cumulativo, então a curva de perda de espessura fica defasada da curva de pH e não volta junto com a recuperação rápida do pH.
- R1: A retardo na recuperação do valor de perda de espessura após o pH retornar ao normal pode ser devido à corrosão passiva que ocorreu durante a queda de pH, levando a uma alteração na camada de proteção e uma resposta lenta da sonda à mudança de condições.
- R2: A sonda RE (elemento resistivo) mede perda de metal **cumulativa**. Assim, a queda de pH acelera a corrosão durante o evento; ao pH voltar, a taxa diminui, mas a **espessura já removida não se “reverte”** e a leitura não recua na mesma rapidez (inerência/tempo de integração da sonda).
- Desenho: atraente = A sonda RE está com defeito. | descarta = A elevação da leitura coincidiu com o intervalo de pH baixo e não há outro indício claro de falha instrumental. | passo oculto = Inferir que a sonda RE continua refletindo a perda já produzida durante o episódio de pH baixo, em vez de espelhar apenas o valor instantâneo de pH.
- Juiz: O ponto decisivo era reconhecer que a sonda RE acumula perda metálica e, por isso, a espessura já perdida não acompanha de volta a recuperação do pH, o que R2 fez e R1 não.

**inventario · dificil_B · R1 parcial · R2 correta** Num FPSO, usa-se MEG contra hidratos. A vazão nominal de injeção permaneceu no valor habitual, mas o corte de água aumentou; os sinais de risco passaram a surgir nos pontos baixos e outros trechos com acúmulo de líquido, sem evidência de parada da bomba. Que condição do MEG na fase aquosa provavelmente passou a existir nesses pontos?

- Referência: Queda da concentração efetiva de MEG na água livre nesses trechos, apesar da vazão nominal mantida.
- R1: Probabilidade de contenção ou esgotamento do MEG na fase aquosa, reduzindo sua capacidade de inibir hidratos, levando ao aumento de risco de formação nesses pontos.
- R2: Provavelmente ocorreu “diluição/consumo de MEG” na fase aquosa (MEG starving): a maior produção de água elevou o teor de água e reduziu a concentração local de MEG abaixo do necessário para inibir hidratos, permitindo formação de hidratos nos pontos baixos e trechos acumuladores.
- Desenho: atraente = Falha simples da bomba de injeção de MEG. | descarta = A vazão nominal de injeção permaneceu no valor habitual e os sinais aparecem justamente nos trechos com acúmulo de líquido. | passo oculto = Com mais água produzida e retenção de líquido, a mesma vazão nominal de MEG passa a se repartir por mais fase aquosa e não protege igualmente todos os pontos.
- Juiz: O ponto decisivo é a queda da concentração efetiva de MEG na água livre nos pontos baixos apesar da vazão nominal, explicitada por R2, enquanto R1 só indica insuficiência/esgotamento de forma vaga, e a pergunta exige esse mecanismo específico.

**inventario · dificil_B · R1 correta · R2 correta** Em um FPSO, a regeneração de MEG está atendendo à meta de remoção de água para reúso. Mesmo assim, no circuito de recuperação continuam surgindo incrustação e sólidos, e o quadro piora quando o glicol retorna mais concentrado. Sabe-se que a água produzida traz sais para o sistema. Que mecanismo explica por que cumprir a meta da regeneração não encerra esse problema?

- Referência: Os sais precipitam quando o processo concentra o glicol e remove água, embora a regeneração tenha atingido a meta de desidratação.
- R1: A água residual carrega sais que promovem incrustações, e mesmo com a remoção de água, a concentração de sais fica elevada, causando depósitos e sólidos no circuito, que não são completamente eliminados pela regeneração de MEG.
- R2: Porque a regeneração remove principalmente água (volátil) do MEG, mas não remove sais não voláteis da água produzida. Esses sais permanecem no glicol e vão sendo concentrados no circuito; ao retornar mais concentrado, aumenta a supersaturação e ocorre precipitação/incrustação, gerando sólidos e piorando o fouling.
- Desenho: atraente = Cumprir a meta de regeneração já deveria eliminar também o problema de sais. | descarta = A remoção de água foi atingida, mas a incrustação persiste no circuito de recuperação e piora quando o glicol retorna mais concentrado. | passo oculto = Inferir que a regeneração cumpriu apenas a remoção de água para reúso e que os sais permaneceram no circuito até perderem solubilidade com o aumento da concentração de MEG.
- Juiz: A referência é válida e pede o mecanismo de sais não voláteis se concentrarem no MEG até precipitar, mesmo com a meta de desidratação atendida, o que ambos explicaram corretamente.

**inventario · dificil_B · R1 correta · R2 correta · atalho** Uma combinação de químicos foi liberada em compatibilidade usando apenas solução de NaCl. Em campo, na corrente real multissalina, o comportamento mudou, embora as concentrações dos produtos e os materiais metálicos tenham sido mantidos como no teste. Que leitura técnica deve ser feita desse contraste?

- Referência: O ensaio em NaCl não representou adequadamente a corrente real multissalina.
- R1: A mudança indica que os sais presentes na solução real influenciam a compatibilidade química, potencialmente promovendo reações ou precipitações não observadas na solução de NaCl pura, destacando a necessidade de testes em condições representativas do ambiente operacional.
- R2: O contraste indica que a compatibilidade observada em NaCl não representa a realidade multissalina: outros íons (ex.: Ca/Mg/SO4/HCO3/Cl−) alteram especiação, complexação, força iônica e podem promover precipitação/escalamento e corrosão. Conclusão: a avaliação deve ser recalibrada com a composição real da água de formação.
- Desenho: atraente = As concentrações dos químicos ou o material metálico em campo estavam diferentes do teste. | descarta = O enunciado informa que concentrações e materiais foram mantidos; o que mudou foi a corrente real multissalina. | passo oculto = Inferir que, mantidos dosagens e materiais, a diferença relevante passou a ser a composição do fluido; portanto, o resultado em NaCl não se generaliza à corrente real.
- Juiz: O contraste mostra que o ensaio em NaCl não representou a química da corrente multissalina real, de modo que ambos respondem corretamente, a referência é válida e há atalho por associação direta com o contraste descrito.

**inventario · dificil_B · R1 correta · R2 correta** Em bottle test para um FPSO, dois desemulsificantes entregam praticamente o mesmo volume final de água separada. No separador da unidade, o volume final exigido já é atingido, mas a camada intermediária permanece espessa e oscilante, com arraste recorrente entre óleo e água. Na escolha entre os dois produtos, que critério do teste deve decidir?

- Referência: Cinética de separação e qualidade da interface, porque o empate no volume final não representa o gargalo observado.
- R1: O critério deve ser a capacidade de desacumular a camada intermediária e reduzir a deterioração da fase de arraste, priorizando aquele que mantém a estabilidade e minimiza a oscilação, mesmo que o volume final de água separada seja similar.
- R2: Escolha o desemulsificante que, no bottle test, **quebra a emulsão mais rapidamente e reduz a interface (camada intermediária) / arraste**: verifique **tempo para atingimento do volume final** e **estabilidade da separação (menor “interface” e menor óleo residual no sobrenadante/água)**, não apenas o volume final.
- Desenho: atraente = Qualquer um, porque o volume final separado foi praticamente igual. | descarta = Na unidade, o volume final exigido já é atingido, mas persiste camada intermediária espessa e oscilante, com arraste entre óleo e água. | passo oculto = Inferir que, com volume final semelhante, a escolha deve ser feita pelo indicador que representa o gargalo operacional real, ligado à evolução da separação e à condição entre as fases.
- Juiz: A referência é válida e manda decidir pelo desempenho dinâmico da separação — sobretudo interface/camada intermediária e arraste, além da rapidez —, que R2 explicita e R1 capta de forma suficiente, sem atalho meramente genérico.

**inventario · dificil_B · R1 parcial · R2 correta** Um desemulsificante escolhido em bottle test foi aplicado no FPSO. Depois, a água produzida passou a operar com outro pH/salinidade e o escoamento real envolveu mistura mais intensa em válvulas e bombas e outro tempo de residência; a perda de resposta apareceu só nessa condição, sem indício de erro grosseiro na triagem. Que mecanismo na emulsão explica melhor essa mudança de desempenho?

- Referência: Alteração da carga elétrica e da adsorção de espécies na interface da emulsão, porque a química da água e o escoamento real mudam a resposta do produto.
- R1: Mudança no pH e salinidade altera a estabilidade da emulsão, promovendo desestabilização e dificultando a ação do desemulsificante devido à modificação na interfacialidade. A mistura mais intensa e o tempo de residência também podem afetar a formação e ruptura da emulsão.
- R2: Mudança de pH/salinidade altera a carga e a solubilidade dos estabilizantes (resinas/asfaltenos) na película interfacial, tornando-a mais resistente. Assim, o desemulsificante perde capacidade de adsorver/disocar o filme e atrasar a drenagem (cinética), elevando a estabilidade quando o cisalhamento e o tempo de residência mudam.
- Desenho: atraente = O bottle test foi inútil e deve ser descartado. | descarta = A perda de resposta surgiu somente após mudanças de química da água e de mistura/residência no processo real, sem indício de erro grosseiro no ensaio. | passo oculto = Inferir que a divergência entre bancada e FPSO vem de mudanças interfaciais provocadas por pH/salinidade e pelas condições reais de escoamento, não de falha intrínseca da triagem.
- Juiz: O decisivo é a mudança de carga elétrica e de adsorção na interface da emulsão com pH, salinidade e escoamento real, explicitada por R2, enquanto R1 ficou genérico sobre estabilidade/interfacialidade, e não há atalho genérico.

**inventario · dificil_B · R1 parcial · R2 parcial** Em um separador de FPSO, o controle de espuma vinha estável com certa faixa de antiespumante. Após aumento do teor de sólidos no fluido e indícios de espécies interfacialmente ativas, a espuma passou a persistir mais tempo nessa mesma faixa, sem outras mudanças operacionais relevantes. Que mecanismo explica melhor essa perda de resposta do produto?

- Referência: dificuldade de entrada do antiespumante no filme espumante estabilizado, e não simples insuficiência de dose.
- R1: Aumento de sólidos e espécies interfaciais ativa extensivamente a formação de foam, reduzindo a eficácia do antiespumante ao dificultar a degradação da espuma pelo reforço da interface.
- R2: A melhor explicação é que o aumento de sólidos e de espécies interfacialmente ativas adsorve/consome o antiespumante e estabiliza as lamelas (maior resistência ao afinamento/drenagem e menor ruptura), reduzindo a capacidade do produto de colapsar a espuma na mesma faixa de dosagem.
- Desenho: atraente = faltou apenas aumentar a dose | descarta = a piora coincidiu com aumento de sólidos e de espécies interfacialmente ativas, mantendo a mesma faixa de dose que antes respondia. | passo oculto = inferir que o aumento de sólidos e espécies interfaciais estabilizou a interface e reduziu a efetividade de ação do antiespumante antes de concluir sobre a dose.
- Juiz: A referência é válida e específica ao apontar a perda de resposta por dificuldade de entrada do antiespumante no filme estabilizado; R1 ficou parcial por falar só em reforço da interface/maior estabilidade da espuma e R2 também parcial por misturar isso com consumo/adsorção do produto, sem cravar o mecanismo decisivo.

**inventario · dificil_B · R1 incorreta · R2 parcial** Num FPSO, a flotação, os pontos de injeção e a configuração do tratamento permaneceram inalterados. Depois da entrada de poços de outra origem e do aumento do corte de água, a mesma dosagem de coagulante/floculante que antes mantinha o TOG do descarte sob controle deixou de estabilizar o desempenho. Que elemento do tratamento químico passou a ser outro?

- Referência: Deslocamento da janela ótima de dosagem do tratamento químico; a dose antes adequada deixou de ser a correta para o novo fluido alimentado.
- R1: O elemento que provavelmente mudou foi o polímero de floculação, devido ao aumento do corte de água, influenciando na eficiência da coagulação e flotação.
- R2: Passou a ser diferente a condição de pH/alcalinidade (e consequentemente a química de coagulação/floculação) do efluente: a nova água produzida de outra origem alterou composição/salinidade/ácidos, reduzindo a eficiência do mesmo coagulante/floculante para manter o TOG.
- Desenho: atraente = Degradação do equipamento de flotação por si só. | descarta = A flotação, os pontos de injeção e a configuração do tratamento permaneceram inalterados; a mudança observada foi no fluido alimentado. | passo oculto = Inferir que a mudança de origem dos poços e de corte de água alterou o fluido alimentado e, com isso, o ajuste químico anteriormente válido.
- Juiz: A resposta de referência é o deslocamento da janela ótima de dosagem para o novo fluido; R1 erra ao trocar o elemento químico e R2 só tangencia ao falar de mudança de química/pH sem identificar que o que mudou foi a dose ótima, com referência válida e sem atalho genérico.

**inventario · dificil_B · R1 correta · R2 correta** No separador de produção de um FPSO, a água produzida passou a chegar com maior salinidade e mais sólidos finos. A espuma ficou persistente, a resposta ao mesmo antiespumante passou a variar entre campanhas e novos ajustes de dosagem não sustentaram melhora. O ponto de injeção, o tempo até o vaso e a mistura permaneceram inalterados. Além da dose, que aspecto do tratamento químico deve ser revisto?

- Referência: A formulação do antiespumante, porque a mudança do fluido pode tornar inadequado o mesmo produto mesmo com ajuste de dose.
- R1: Rever a seleção do antiespumante, seu tipo, concentração e fase de adição, além das condições de mistura, para melhorar a eficácia e controle da espuma persistente.
- R2: Rever a **seleção/formulação do antiespumante** (tipo e química, e compatibilidade com a nova água produzida de maior salinidade e sólidos finos). A dosagem pode não “compensar” quando mudam os surfactantes/estabilidade; pode ser necessário antiespumante de outra tecnologia e/ou sinergia com demulsificante/coagulante.
- Desenho: atraente = Apenas aumentar a dose do mesmo produto. | descarta = A resposta ao mesmo antiespumante ficou inconsistente após aumento de salinidade e sólidos finos, sem melhora sustentada com novos ajustes de dose. | passo oculto = Inferir que a mudança nas características do fluido deslocou a adequação do produto, então o problema deixou de ser resolvível só por dosagem.
- Juiz: O decisivo era rever a seleção/formulação do antiespumante diante da mudança de salinidade e sólidos do fluido, e ambos apontam esse aspecto químico além de mera dosagem.

**inventario · dificil_B · R1 incorreta · R2 correta** Em um FPSO, duas formulações antiespumantes apresentaram queda de espuma praticamente igual no vaso onde são dosadas. Após aplicação contínua, uma delas passou a coincidir com mais água no óleo e mais óleo na água produzida na etapa seguinte. Na comparação entre essas formulações, qual critério de ensaio deveria ter sido tratado como decisivo?

- Referência: Compatibilidade com a separação óleo-água, porque a quebra de espuma foi semelhante e o desempate veio do efeito a jusante nas correntes líquidas.
- R1: O critério decisivo seria a estabilidade, ou seja, a resistência do antiespumante à quebra de espuma ao longo do tempo, para evitar mistura de água e óleo na produção.
- R2: O critério decisivo é o desempenho de desemulsificação/estabilidade da emulsão (capacidade de quebrar emulsões O/A sem aumentar oil-in-water e sem piorar o arraste de óleo para a água produzida), avaliado em ensaio de separação e BS&W (ex.: “bottle test”/settling).
- Desenho: atraente = velocidade de quebra da espuma | descarta = As duas formulações quebraram a espuma de forma praticamente igual no ponto de aplicação, mas diferiram nas correntes líquidas da etapa seguinte. | passo oculto = Inferir que, com quebra de espuma equivalente, o critério que decide é o impacto da formulação no desempenho líquido-líquido a jusante.
- Juiz: Como a quebra de espuma foi equivalente, o desempate técnico é a compatibilidade do antiespumante com a separação óleo-água a jusante, critério que R2 captou e R1 trocou indevidamente por estabilidade do antiespumante.

**inventario · dificil_B · R1 incorreta · R2 correta** Em uma FPSO, a URS entrou em operação e o permeado segue dentro do esperado para injeção. O risco de incrustação por sulfatos no sistema de injeção caiu, mas surgiu preocupação com precipitação de CaSO4 em parte da própria unidade. Se for considerado anti-incrustante por esse novo risco, em qual corrente ele tende a fazer mais sentido?

- Referência: Na corrente concentrada rica em sulfato da própria URS, não no permeado de injeção.
- R1: O anti-incrustante faz mais sentido na corrente de água de produção ou no sistema de lavagem da FPSO, para prevenir deposição de CaSO4 que pode ocorrer na própria unidade.
- R2: Para mitigar precipitação de CaSO4 “na própria unidade”, faz mais sentido dosar o anti-incrustante na corrente que alimenta os equipamentos de concentração (ex.: entrada do RO/recirculação do retentado ou lado de maior TDS), antes de onde Ca e SO4 ficam supersaturados.
- Desenho: atraente = no permeado destinado à injeção | descarta = o permeado segue dentro do esperado para injeção e foi justamente onde o risco por sulfato diminuiu | passo oculto = Inferir que o novo risco interno de CaSO4 aparece na corrente em que a URS concentra sulfato, e não na água permeada para injeção.
- Juiz: O ponto decisivo é o lado concentrado/retentado da URS, onde sulfato e TDS se elevam e surge a supersaturação, não o permeado de injeção, por isso R2 acerta e R1 aponta correntes erradas.

**inventario · facil · R1 correta · R2 correta · atalho** Para que são usados os KPIs em processos industriais?

- Referência: Para avaliar a eficiência e o desempenho dos processos industriais.
- R1: KPIs em processos industriais monitoram desempenho, identificam melhorias e garantem eficiência operacional, segurança, qualidade e custos, facilitando a tomada de decisões estratégicas.
- R2: KPIs em processos industriais são usados para medir desempenho e progresso operacional, como eficiência, produtividade, confiabilidade e qualidade. Ajudam no controle e otimização do processo, identificação de desvios, melhoria contínua, priorização de ações e suporte a decisões de operação e manutenção (ex.: disponibilidade, MTBF/MTTR, perdas/ rendimento).
- Juiz: R1 e R2 acertaram ao apontar que KPIs servem para medir/avaliar desempenho e eficiência dos processos; a referência é válida e há atalho genérico porque a própria ideia de KPI leva diretamente a essa resposta.

**inventario · facil · R1 correta · R2 correta · atalho** No acompanhamento ambiental da empresa, qual é a função básica de um indicador ambiental?

- Referência: Expressar o desempenho ambiental da organização, fornecendo informação específica sobre ele.
- R1: Monitorar, avaliar e comunicar o desempenho ambiental, facilitando a tomada de decisões para redução de impactos e conformidade com normas ambientais.
- R2: Um indicador ambiental serve para medir, de forma objetiva e comparável, o desempenho e as condições ambientais associadas às atividades da empresa, permitindo acompanhar tendências, avaliar conformidade e apoiar decisões de gestão e mitigação de impactos.
- Juiz: Bastava indicar que o indicador ambiental mede/expressa o desempenho ambiental da organização, e a referência é ampla o suficiente para aceitar respostas genéricas desse tipo.

**inventario · facil · R1 parcial · R2 correta** No acompanhamento de desempenho operacional de um sistema em FPSO, o que caracteriza sua dependabilidade?

- Referência: O conjunto de atributos que sustenta a confiança no serviço prestado por um sistema.
- R1: A dependabilidade do sistema é caracterizada pela sua capacidade de operar sem falhas e com alta disponibilidade ao longo do tempo, garantindo continuidade na produção e minimizando paradas não planejadas.
- R2: Dependabilidade, em acompanhamento operacional de FPSO, é a capacidade do sistema de cumprir a função continuamente com falhas mínimas: expressa por confiabilidade (MTBF/ taxa de falha), disponibilidade (uptime), manutenibilidade (MTTR/tempo de reparo) e, em níveis, segurança e integridade.
- Juiz: Dependabilidade é o conjunto de atributos que sustenta a confiança no serviço; R1 a reduz a operar sem falhas/alta disponibilidade, enquanto R2 explicita os atributos centrais de forma compatível com a definição.

**inventario · facil · R1 correta · R2 correta · atalho** Em um FPSO, o que a disponibilidade de um equipamento crítico expressa?

- Referência: A aptidão de o equipamento estar pronto para executar a função requerida quando for necessário.
- R1: A porcentagem de tempo em que o equipamento está operacional e disponível para uso, refletindo sua confiabilidade e manutenção efetiva.
- R2: A disponibilidade de um equipamento crítico expressa a fração do tempo em que ele fica em condição de operar quando necessário, considerando falhas, reparos e paradas. No FPSO, isso mede o quanto o sistema consegue manter a produção/serviços sem interrupções por indisponibilidade do equipamento.
- Juiz: A disponibilidade expressa estar em condição de cumprir a função quando requerido, ideia capturada por ambos; a referência é válida e o item aceita resposta genérica de definição.

**inventario · facil · R1 correta · R2 correta · atalho** Em um sistema de processo de FPSO, para que se adota redundância?

- Referência: Para manter o serviço usando caminhos, equipamentos ou funções adicionais quando parte do arranjo falha.
- R1: Redundância é adotada para assegurar continuidade operacional, minimizar paradas não planejadas e aumentar a confiabilidade do sistema de processo na FPSO.
- R2: Adota-se redundância para aumentar a confiabilidade e reduzir a probabilidade de falha, garantindo operação segura e contínua em FPSO. Em caso de falha de um componente (equipamento, controle ou energia), o sistema mantém a função crítica, minimiza paradas e protege pessoas, meio ambiente e produção.
- Juiz: Redundância serve para manter a função/serviço quando parte do sistema falha, ideia capturada por ambos, e a referência é genérica o bastante para aceitar respostas de continuidade e confiabilidade.

**inventario · facil · R1 incorreta · R2 parcial · ref. inválida** Na gestão de desempenho de um FPSO, em quais quatro frentes as análises RAM ou RAMS costumam orientar decisões?

- Referência: Operação, fabricação, projeto e manutenção.
- R1: Segurança, Confiabilidade, Disponibilidade e Manutenção, orientando melhorias na operação, redução de riscos, otimização de desempenho e estratégias de manutenção preventiva.
- R2: Geralmente, as análises RAM/RAMS orientam decisões em: (1) projeto e redundância (confiabilidade), (2) estratégia de manutenção e reparo (mantenabilidade), (3) filosofia/planejamento de operação para maximizar disponibilidade (performance), e (4) segurança e integridade (falhas críticas, consequências e mitigação de risco).
- Juiz: R2 fica parcial por cobrir projeto, operação e manutenção mas trocar fabricação por segurança, R1 é incorreta por listar atributos do acrônimo em vez das frentes decisórias, e a referência não é única porque em RAMS segurança também é uma frente plausível.

**inventario · facil · R1 parcial · R2 correta** Na gestão de ativos de um FPSO, o que expressa a mantenabilidade de um sistema após uma falha?

- Referência: A probabilidade de restaurar o sistema parado às condições definidas de funcionamento, desempenho e admissibilidade no tempo desejado, com manutenção feita nas condições e meios prescritos.
- R1: A mantenabilidade de um sistema após uma falha é expressa pelo tempo de reparo ou tempo médio entre falhas (MTTR), indicando a facilidade e rapidez para restaurar suas condições operacionais.
- R2: A mantenabilidade após uma falha é expressa pelo tempo requerido para restaurar o sistema, tipicamente via MTTR (Mean Time To Repair) ou pela distribuição/ probabilidade de reparo dentro de um tempo especificado (p.ex., TTR).
- Juiz: A referência válida exige a noção de restaurar o sistema em um tempo especificado, idealmente como probabilidade/distribuição de reparo, e R1 ficou incompleto e ainda confundiu a métrica ao citar MTBF.

**inventario · facil · R1 correta · R2 correta · atalho** Que finalidade tem uma barreira na gestão de risco operacional de um FPSO?

- Referência: Impedir ou mitigar acidentes, como mecanismo físico ou procedimento administrativo.
- R1: A barreira na gestão de risco operacional de um FPSO visa prevenir falhas e acidentes, controlando perigos e protegendo pessoas, meio ambiente e ativos, garantindo a segurança e a continuidade das operações.
- R2: Uma barreira no FPSO é um elemento de contenção/mitigação (técnico ou operacional) para reduzir a frequência e/ou consequências de eventos iniciadores, assegurando o controle de riscos: prevenir vazamentos/incêndios, controlar pressão/níveis, e permitir recuperação segura até procedimentos ou sistemas de emergência.
- Juiz: A referência é válida porque o elemento decisivo é que a barreira serve para impedir ou mitigar acidentes/riscos, o que ambos disseram, e há atalho genérico porque uma resposta ampla como 'reduzir riscos e proteger pessoas/ativos' já acertaria.

**inventario · facil · R1 correta · R2 correta** Em um FPSO, o que a confiabilidade de um equipamento expressa na gestão de desempenho?

- Referência: A capacidade de cumprir a função requerida, nas condições especificadas, ao longo de um intervalo de tempo.
- R1: A confiabilidade mede a capacidade do equipamento de desempenhar suas funções sem falhas por um período definido, influenciando a disponibilidade, manutenção preventiva e segurança operacional do FPSO.
- R2: Em um FPSO, confiabilidade expressa a capacidade do equipamento operar sem falhas por um período/condição definidos, afetando diretamente a disponibilidade. Na gestão de desempenho, traduz-se em taxas de falha, MTBF e impacto em paradas, permitindo monitorar e otimizar manutenção e planos de intervenção.
- Juiz: Ambos definem confiabilidade como a capacidade de o equipamento cumprir sua função sem falhar ao longo de um período definido, com R2 explicitando também as condições de operação, em linha com a referência técnica.

**inventario · facil · R1 correta · R2 correta · atalho** Na análise de falhas de um sistema do FPSO, o que caracteriza o mecanismo de falha?

- Referência: O processo físico, químico ou organizacional que provoca a perda de função.
- R1: O mecanismo de falha caracteriza o processo ou causa que leva à falha do sistema, incluindo fatores como fadiga, corrosão, desgaste ou falha de material.
- R2: O mecanismo de falha é o fenômeno físico/químico que leva à degradação do componente até a perda de função (ex.: fadiga, corrosão, erosão, desgaste, falha elétrica). Ele descreve a causa “de fundo” e como a falha se propaga, não apenas o sintoma final.
- Juiz: O decisivo é definir mecanismo de falha como o processo ou fenômeno que leva à perda de função, o que ambos captam, mas a definição é ampla o bastante para aceitar respostas genéricas de causa/processo; ainda assim a referência é válida e há atalho genérico.

**inventario · facil · R1 correta · R2 correta · ref. inválida** Em produção e processo, de que fatores depende a permanência de uma mistura água-óleo sem se separar?

- Referência: Da composição do petróleo, da salmoura e do filme interfacial.
- R1: A permanência depende do método de emulsificação, viscosidade, concentração de emulsificante, temperatura e agitação.
- R2: A permanência depende da estabilidade físico-química da emulsão: presença de tensoativos naturais/sólidos (asfaltenos, resinas, argilas) que formam filme interfacial; tamanho de gota e viscosidade; intensidade de agitação; salinidade e composição (pH, íons) que alteram repulsão; temperatura; além de baixa diferença de densidade e reduzida coalescência.
- Juiz: A pergunta é ampla demais para restringir a resposta apenas à composição do petróleo, da salmoura e do filme interfacial, pois estabilidade da emulsão também depende de fatores como viscosidade, temperatura, agitação e modo de emulsificação, tornando tecnicamente aceitáveis tanto R1 quanto R2.

**inventario · facil · R1 parcial · R2 parcial** Na escolha de um antiespumante para controle de espuma em processo de óleo e gás, quais aspectos da formulação precisam ser avaliados?

- Referência: Princípio ativo, concentração, veículo e coadjuvantes da formulação.
- R1: A composição química, a compatibilidade com o fluido, a eficácia na supressão de espuma, a estabilidade térmica e a compatibilidade ambiental devem ser avaliadas na formulação do antiespumante.
- R2: Avaliar: compatibilidade química com a fase (água/óleo), tipo de espuma e surfactantes presentes, salinidade/pH/temperatura, presença de sólidos, taxa de dosagem e estabilidade (emulsionante/solubilidade), eficiência em condições de processo (cisalhamento, tempo de contato), desempenho em presença de gás dissolvido, e efeito secundário (corrosão, quebra de emulsão, impacto em separação/filtração).
- Juiz: A referência pede os componentes da formulação — princípio ativo, concentração, veículo e coadjuvantes — e ambos falaram mais de compatibilidade/desempenho de uso do que dessa composição, apenas tangenciando o esperado.

**inventario · facil · R1 incorreta · R2 incorreta** Na preparação da água do mar para injeção em reservatório, qual é a função principal da URS/SRU?

- Referência: Reduzir seletivamente a concentração de sulfato na água injetada.
- R1: A URS/SRU remove sulfitos, uréia e outros contaminantes, garantindo água de alta pureza para evitar formação de corrosão, depósitos e problemas de escala no sistema de injeção.
- R2: A URS/SRU tem como função principal remover sólidos em suspensão e turbidez da água do mar, reduzindo biofouling e entupimento das etapas seguintes (ex.: filtração fina/desalinação), preparando a água para injeção no reservatório com menor risco de incrustações.
- Juiz: URS/SRU serve principalmente para remover seletivamente sulfato da água de injeção, e ambos os candidatos descreveram outras funções de tratamento, com referência válida e específica.

**inventario · facil · R1 correta · R2 correta · atalho** No controle microbiológico da água de injeção em FPSOs, que função cumprem os biocidas?

- Referência: Matar microrganismos ou inibir seu crescimento nos circuitos tratados.
- R1: Os biocidas eliminam ou controlam microrganismos na água de injeção, evitando corrosão, regolito e obstruções que comprometem a integridade e o desempenho do sistema de injeção em FPSOs.
- R2: Biocidas controlam microrganismos (bactérias, fungos, biofilmes) na água de injeção, reduzindo a biocarga e prevenindo corrosão microbiologicamente influenciada (MIC), entupimento por biofouling e degradação de equipamentos/linhas, mantendo a qualidade microbiológica para injeção no reservatório.
- Juiz: O elemento decisivo era a função de matar ou inibir o crescimento de microrganismos no circuito tratado, algo diretamente associado ao termo biocida e atendido por ambas as respostas.

**inventario · facil · R1 incorreta · R2 correta** Na produção de gás natural, para que o MEG é aplicado em linhas e equipamentos?

- Referência: Como inibidor da formação de hidratos.
- R1: O MEG (Monoetilenoglicol) é utilizado como agente dessidratante para remover a umidade do gás natural, prevenindo a formação de condensados e corrosão nos equipamentos.
- R2: MEG (monoetilenoglicol) é usado como inibidor de hidratos e controlador de ponto de orvalho/decondensação. Ao injetar e manter baixa atividade de água, evita formação de hidratos e reduz corrosão/entupimentos em linhas e equipamentos de produção, transporte e processamento de gás.
- Juiz: O elemento decisivo é o uso do MEG para inibir hidratos; R2 o trouxe explicitamente, R1 confundiu com desidratação do gás, e não há atalho genérico.

**inventario · facil · R1 incorreta · R2 parcial · ref. inválida** Na recuperação do MEG injetado, qual risco operacional ligado à água produzida não é removido só porque o MEG controla hidratos?

- Referência: Precipitação de sais da água produzida, com formação de incrustações no circuito de recuperação do MEG.
- R1: O risco de corrosão devido à presença de CO₂ e H₂S na água produzida não é totalmente eliminado pelo controle de hidratos pelo MEG.
- R2: Mesmo com MEG reduzindo formação de hidratos, a água produzida ainda pode causar corrosão (e.g., MIC e corrosão por CO₂/H₂S) e incrustações associadas, afetando integridade de dutos/equipamentos e aumentando paradas e vazamentos.
- Juiz: A referência aponta incrustação por precipitação de sais no circuito de recuperação do MEG, então R1 erra ao tratar só de corrosão e R2 só acerta parcialmente por citar incrustações junto com outro mecanismo, mas a pergunta é ampla e também admite corrosão como risco plausível.

**inventario · facil · R1 correta · R2 correta** Como um inibidor orgânico de corrosão reduz o ataque corrosivo ao metal?

- Referência: Por adsorção na superfície metálica e formação de uma película que dificulta o acesso de espécies agressivas.
- R1: O inibidor orgânico forma uma camada protetora adsorvida na superfície do metal, bloqueando fontes de corrosão e impedindo reações químicas que causam o dano.
- R2: Um inibidor orgânico de corrosão adsorve-se na superfície metálica (quimissorção/fisisorção), formando um filme protetor que bloqueia sítios anódicos/catódicos e reduz a transferência de carga. Isso aumenta a resistência de polarização, limita a difusão de espécies corrosivas e diminui a taxa de reação.
- Juiz: Ambos trazem o elemento decisivo da adsorção do inibidor na superfície metálica com formação de película protetora que dificulta o ataque corrosivo, em uma referência válida e técnica.

**inventario · facil · R1 incorreta · R2 incorreta** No monitoramento de um tratamento squeeze, como se acompanha sua evolução no poço?

- Referência: Pelo retorno do inibidor na água produzida.
- R1: Acompanhando variações na pressão do reservatório, fluxos de produção, níveis de produção e análise de datos de sensores de poço para detectar fechamento do fecho e eficiência do tratamento.
- R2: Acompanha-se o squeeze via dados de pressão/fluxo e, principalmente, estabilidade do injectivity/perda de carga: monitorar pressão de bombeio e taxas ao longo do tempo, variação do fundo (BHP), retorno/absorção, e tempo de sorvedouro. Normalmente confirma-se por queda da taxa para mesma pressão (formato do perfil) e posterior estabilização; idealmente com pressão antes/depois e logs/annulus se disponíveis.
- Juiz: A referência é válida e específica: a evolução de um squeeze se acompanha pelo retorno/concentração do inibidor na água produzida, elemento ausente em ambas as respostas, e um atalho genérico sobre pressão ou vazão não bastaria.

**inventario · facil · R1 parcial · R2 correta** Ao analisar risco de deposição de asfaltenos, que fatores governam sua estabilidade no petróleo?

- Referência: A composição do petróleo e as interações que mantêm essas espécies dispersas.
- R1: Temperatura, composição química, presença de porosidade, e taxa de resfriamento influenciam a estabilidade dos asfaltenos no petróleo.
- R2: Estabilidade dos asfaltenos depende do equilíbrio entre peptização (resinas/aromáticos) e forças de agregação (asfaltenos). Governam: composição (teor/ tipo de resinas e aromáticos), razão SARA, pressão/temperatura (degasificação), GOR e solubilidade do óleo, composição do gás dissolvido (C1–C5), salinidade/água, grau de envelhecimento/oxidação e presença de sólidos/catalisadores. Mudanças levam à perda de solubilidade e floculação.
- Juiz: A estabilidade de asfaltenos é governada principalmente pela composição/solvência e pelas interações dispersantes, que R2 descreve corretamente, enquanto R1 só cita composição de modo incompleto e acrescenta fator inadequado como porosidade.

**inventario · facil · R1 correta · R2 correta · ref. inválida · atalho** Por que a dosagem de produtos químicos não deve ser ajustada com base em apenas um indicador isolado?

- Referência: Porque pode melhorar esse indicador e, ao mesmo tempo, piorar outra variável do processo, deslocando o problema.
- R1: Porque um indicador isolado pode não refletir toda a condição do sistema, levando a ajustes inadequados; múltiplos parâmetros garantem uma avaliação mais precisa e segura.
- R2: Porque um único indicador isolado pode estar desviado por variações de processo, instrumentação ou interferências químicas. Ajustar a dosagem só com esse dado pode gerar subdosagem/overdose, piorar corrosão, incrustação ou eficiência de tratamento e causar instabilidade operacional.
- Juiz: A ideia central é que um único indicador não representa sozinho o estado do sistema e pode induzir ajuste que desloque o problema para outra variável, então R2 traz o efeito cruzado explicitamente e R1 também é aceitável pela amplitude da pergunta, que não tem referência única e permite resposta genérica.

**inventario · media · R1 correta · R2 correta · atalho** Em um FPSO, após mudança de carga na unidade de processo, um KPI sai da faixa esperada e a equipe o analisa junto com variáveis de processo e histórico recente, sem tratá-lo isoladamente. Como esse KPI deve ser usado tecnicamente nessa situação?

- Referência: Para detectar o desvio, identificar variáveis perturbadas e apoiar o diagnóstico de causas prováveis.
- R1: O KPI deve ser avaliado como um indicador de tendência, considerando variáveis relacionadas e contexto operacional, para identificar causas raízes possíveis antes de tomar ações corretivas.
- R2: Use o KPI como variável de diagnóstico integrada ao estado do processo: compare tendência (baseline vs. situação pós-mudança), correlacione com variáveis operacionais e eventos recentes, e empregue como gatilho para investigação/ajuste de controle. Não como limite isolado: interprete via análise de causa e efeitos, confirmando com estabilidade/recuperação.
- Juiz: Ambos usam o KPI corretamente como indicador contextual para detectar desvio, correlacionar variáveis perturbadas e apoiar o diagnóstico de causas prováveis, e a referência é válida mas ampla o bastante para aceitar resposta de bom senso.

**inventario · media · R1 correta · R2 correta · atalho** Em um FPSO, março e abril tiveram 4 acidentes sem afastamento cada, mas em abril houve parada com efetivo ampliado e muito mais horas trabalhadas. Ao montar a taxa para comparar os meses de forma consistente, que componente da fórmula deve refletir essa diferença operacional?

- Referência: O denominador, usando as horas-homem de exposição no período.
- R1: O componente que deve refletir essa diferença é as horas trabalhadas; utilizar as horas totais trabalhadas por mês na fórmula de taxa padroniza a comparação.
- R2: Na comparação consistente entre meses, a diferença operacional (efetivo ampliado e mais horas trabalhadas) deve refletir na **exposição**, ou seja, no **denominador do cálculo por taxa**, usando **horas-homem (ou homem-hora trabalhada)** do período.
- Juiz: A referência é válida e há atalho por associação direta, pois a diferença operacional deve entrar no denominador como horas-homem de exposição, exatamente como ambos responderam.

**inventario · media · R1 parcial · R2 correta · ref. inválida · atalho** Em um FPSO, parte das falhas tem hora de início registrada, mas muitas voltas à operação entram sem horário confiável e em formatos diferentes entre áreas. Na consolidação dos KPIs do mês, o que fica diretamente prejudicado?

- Referência: A qualidade da avaliação de disponibilidade e confiabilidade, porque os tempos de reparo e de indisponibilidade observada deixam de ser calculados com confiança.
- R1: A confiabilidade e a precisão dos KPIs, especialmente relacionados à manutenção e ao desempenho operacional, ficam prejudicadas devido à inconsistência e falta de horário confiável nas entradas de falhas.
- R2: Com início de falha sem horário confiável, ficam prejudicados os cálculos de duração dos eventos: downtime/indisponibilidade, MTTR e KPIs de disponibilidade/uptime (porque dependem do intervalo entre início e retorno). A contagem de falhas pode até existir, mas os tempos não.
- Juiz: A falta de horário confiável de retorno prejudica diretamente métricas baseadas em duração como downtime/MTTR e disponibilidade, o que R2 explicitou e R1 tratou de modo genérico, mas a pergunta admite respostas equivalentes além da referência e até um atalho amplo sobre 'KPIs prejudicados' quase responde.

**inventario · media · R1 parcial · R2 incorreta · atalho** Em um FPSO, a produção teve paradas por atuação de intertravamentos e funções de proteção durante desvios de processo, evitando condição perigosa e potencial dano ambiental. Na avaliação do desempenho operacional, que aspecto deve ser analisado junto com a disponibilidade?

- Referência: Segurança, porque essas atuações podem interromper a produção para evitar estados perigosos, danos ambientais e consequências maiores.
- R1: Deve-se analisar a confiabilidade do sistema de proteção e controle, garantindo que os mecanismos atuem corretamente para prevenir riscos ambientais e operacionais.
- R2: Além da disponibilidade, deve-se analisar a confiabilidade operacional (ex.: frequência e duração das falhas/intertravamentos que demandam proteção), associada a métricas como MTBF e taxa de eventos, para refletir estabilidade do sistema sob desvios de processo.
- Juiz: O elemento decisivo é analisar segurança além da disponibilidade, algo sugerido pelo próprio enunciado, então R1 fica parcial por falar da confiabilidade da proteção em função dos riscos, R2 erra ao trocar por confiabilidade operacional, a referência é válida e há atalho genérico.

**inventario · media · R1 parcial · R2 correta** Num FPSO, os poços enviam uma mistura de óleo, gás e água com possíveis sólidos, e alguns equipamentos já operam perto do limite. Ao avaliar o KPI de capacidade produtiva da unidade, que fator do processo deve ser tratado como determinante?

- Referência: A capacidade combinada de separar, tratar e movimentar as correntes de óleo, gás e água.
- R1: O fator determinante é a capacidade de separação e processamento do fluxo de entrada, especialmente a eficiência dos vasos de separação, pois afeta a quantidade de óleo, gás e água que podem ser produzidos e processados sem sobrecarregar os equipamentos.
- R2: O fator determinante é o gargalo do processo de separação e condicionamento da produção (capacidade dos separadores trifásicos/linha de gás e tratamento de água, incluindo remoção de sólidos). Isso controla o quanto de óleo/gás pode ser efetivamente estabilizado, comprimido e escoado sem ultrapassar os limites dos equipamentos.
- Juiz: O fator determinante é a capacidade combinada ou gargalo de separar, tratar e movimentar óleo, gás e água, e R1 reduziu isso sobretudo à separação enquanto R2 cobriu o conjunto do processo.

**inventario · media · R1 parcial · R2 parcial · ref. inválida** O KPI de produção de um FPSO caiu por perdas recorrentes, e a equipe avalia combinar ações antes das perdas com intervenções quando a capacidade já foi afetada. De que depende a escolha entre essas medidas?

- Referência: Da localização da restrição e do horizonte de atuação: prevenir antes da perda ou corrigir depois que a capacidade já foi comprometida.
- R1: A escolha depende do custo, impacto na produção, capacidade de monitoramento e rapidez de resposta às perdas, equilibrando prevenção e intervenção corretiva para otimizar a eficiência operacional.
- R2: Depende principalmente da causa e dinâmica da perda (reversibilidade/tempo de recuperação), criticidade e taxa de recorrência, disponibilidade de janelas de manutenção/recursos, custo vs. impacto na produção (valor do petróleo), e capacidade do FPSO para atuar preventivamente (integridade mecânica/elétrica/processos) vs. necessidade de intervenção corretiva.
- Juiz: A referência exige localização da restrição e horizonte preventivo/corretivo; R1 e R2 ficam em critérios gerenciais/causais gerais e só tangenciam prevenção versus correção, e a pergunta é ampla a ponto de admitir outras bases de decisão igualmente plausíveis.

**inventario · media · R1 parcial · R2 correta** Em um FPSO, a capacidade do único compressor que recebe o gás de vários poços caiu abaixo da vazão total produzida. Os demais sistemas seguem disponíveis, mas todas essas correntes dependem desse mesmo equipamento. Qual consequência operacional imediata isso impõe?

- Referência: Priorização das entregas e alocação da capacidade disponível entre as correntes atendidas por esse ponto comum.
- R1: O risco de acumulação de gás e potencial perda de produção, podendo levar ao desligamento de poços ou interrupções no processamento até resolver a limitação do compressor.
- R2: A operação passa a ser limitada pela menor capacidade do compressor: impõe aumento de contrapressão na coleta e consequente redução/curtailment da produção (principalmente dos poços) para casar a vazão de gás com a capacidade disponível; caso contrário ocorre transbordo/instabilidade do sistema de gás.
- Juiz: O decisivo era reconhecer o compressor como gargalo comum que força alocação/curtailment da capacidade entre correntes, então R2 acerta ao descrever a limitação com redução para casar vazões e R1 fica parcial por citar apenas riscos genéricos de perda ou parada; a referência é válida e não há atalho genérico.

**inventario · media · R1 incorreta · R2 correta** Num FPSO, um evento foi lançado só como “queda de vazão do poço”, após alteração de pressão observada e confirmação de depósito na coluna de produção. Ao revisar a atribuição da perda no KPI, que ligação precisa constar para a causa ficar corretamente atribuída?

- Referência: A da causa física ao ativo atingido e ao efeito operacional; no caso, depósito na coluna ligado à restrição de escoamento e à queda de vazão.
- R1: A ligação da choke ou válvula de controle de fluxo precisa constar, pois controla o fluxo e sua alteração indica a queda de vazão do poço.
- R2: A causa deve ficar ligada ao ativo/ocorrência de **restrição por depósito na coluna de produção** (ex.: *incrustação/entupimento na coluna/tubing*), não apenas como “queda de vazão do poço”. Ou seja, o evento no KPI deve ser atribuído à **coluna de produção (downhole/tubing)** como falha causadora.
- Juiz: A atribuição correta exige ligar o depósito na coluna de produção ao ativo afetado e à restrição de escoamento que derruba a vazão; R1 desloca a causa para choke/válvula e R2 faz essa vinculação corretamente, sem caber atalho genérico.

**inventario · media · R1 correta · R2 correta · atalho** No processamento primário de um FPSO, a operação segue com um instrumento crítico fora de serviço e outro fornecendo leituras instáveis, ambos usados para acompanhar variáveis essenciais. Que efeito isso tende a ter sobre o risco de processo?

- Referência: Aumenta o risco de processo, porque medições essenciais ausentes ou pouco confiáveis reduzem a capacidade de detectar e corrigir desvios a tempo.
- R1: Aumenta o risco de processo devido à perda de monitoramento preciso, podendo levar a operações inseguras ou decisões incorretas, pois as variáveis essenciais não são obtidas com confiabilidade.
- R2: Tende a aumentar o risco de processo: um instrumento crítico fora de serviço reduz a detecção/controle de desvios e o outro com leituras instáveis pode gerar alarmes/intertravamentos incorretos ou atrasar a resposta, elevando a probabilidade de condições fora de especificação e falhas de proteção.
- Juiz: O decisivo era que medições essenciais ausentes ou instáveis elevam o risco por reduzir a detecção e correção tempestiva de desvios, o que ambos afirmam; a referência é válida e há atalho genérico por ser conclusão de bom senso explicitamente sugerida no enunciado.

**inventario · media · R1 parcial · R2 parcial · ref. inválida · atalho** Após uma parada programada no FPSO, a equipe arquivou apenas o custo total e a duração final. Não documentou o previsto, o realizado, os desvios nem as lições aproveitáveis para a próxima campanha. O que tende a ficar comprometido nessa gestão?

- Referência: O monitoramento contínuo do risco e a revisão das decisões futuras, por faltar base documentada do planejado, do ocorrido, dos desvios e das lições válidas.
- R1: A gestão de lições aprendidas, controle de desvios e precisão na análise de desempenho, comprometendo melhorias futuras e a eficiência na próxima parada.
- R2: A gestão de turnaround fica comprometida em planejamento e controle: perde-se a comparabilidade previsto×real, a detecção de desvios (custos, prazos e escopo) e a rastreabilidade das causas. Consequentemente, reduz-se a melhoria contínua, aumentando reincidência de falhas e incerteza para campanhas futuras.
- Juiz: A pergunta admite várias respostas de gestão igualmente defensáveis, de modo que a referência não é única e um atalho genérico sobre desvios/lições pareceria suficiente; ainda assim, ambos ficaram aquém do foco específico da referência em monitoramento de risco e revisão de decisões futuras.

**inventario · media · R1 parcial · R2 parcial** Num FPSO, antes de testar em linha um novo pacote químico para uma emulsão água-em-óleo, a equipe precisa comparar, em bancada, diferentes produtos e dosagens com a mesma amostra, controlando temperatura, mistura e tempo e observando água separada e interface. Que ensaio deve usar?

- Referência: Bottle test, usado como triagem empírica para selecionar desemulsificantes e dosagens em condições controladas; depois ainda requer validação operacional.
- R1: O ensaio adequado é o teste de emulsificação em bancada, que avalia a estabilidade da emulsão água-em-óleo sob condições controladas de temperatura, mistura e tempo.
- R2: Use ensaio de jar/test (teste de bancada em proveta/jarretes) com variação de dosagem e tempo, à temperatura controlada e sob agitação padronizada, para avaliar separação de água e altura/estabilidade da interface água-óleo.
- Juiz: O elemento decisivo era nomear o bottle test como ensaio padrão de triagem de desemulsificante; ambos descrevem uma comparação de bancada sob controle, mas sem identificar corretamente esse ensaio específico, e a questão não se resolve por prudência genérica.

**inventario · media · R1 correta · R2 correta · atalho** Em um separador de produção, a espuma persiste, o gás perde área livre de escoamento no vaso e aumenta o arraste de líquido na saída de gás. Por que essa espuma passa a exigir mitigação no processo?

- Referência: Redução da separação gravitacional entre gás e líquido no separador.
- R1: A espuma persistente reduz a eficiência de separação, aumenta a carga de líquido no gás e pode causar plugging ou problemas operacionais, exigindo mitigação para manter o fluxo adequado e evitar danos ao sistema.
- R2: Porque a espuma reduz a eficiência do separador: bloqueia/encolhe a área de disengajamento do gás (vazão efetiva), intensifica o arraste de gotículas para a linha de gás e aumenta o risco de violar limites de qualidade/segurança e de sobrecarga de equipamentos a jusante, exigindo mitigação.
- Juiz: A referência é válida e o decisivo era que a espuma prejudica a separação gás-líquido no separador, ponto capturado por ambos ao descrever perda de eficiência/área de disengajamento e aumento de arraste, sendo uma resposta também muito sugerida pelo próprio enunciado.

**inventario · media · R1 correta · R2 correta · atalho** Em um separador de produção, após mudança na composição do fluido, os filmes líquidos entre as bolhas passam a escoar mais devagar e as bolhas rompem com menos facilidade, mantendo-se o mesmo regime de mistura. Como tende a se comportar a espuma?

- Referência: Mais persistente, porque a drenagem mais lenta e a maior resistência à ruptura prolongam a vida da espuma.
- R1: A espuma tende a se tornar mais estável, com bolhas maiores e mais resistentes, devido à redução do escoamento dos filmes líquidos, dificultando o rompimento das bolhas.
- R2: Tende a aumentar a estabilidade e a persistência da espuma: com escoamento dos filmes mais lento e ruptura menos fácil, a espuma fica mais duradoura e volumosa, elevando o hold-up de espuma no separador.
- Juiz: Menor drenagem dos filmes e menor ruptura das bolhas significam espuma mais estável e persistente, o que ambos dizem; a referência é válida, mas a resposta praticamente repete o enunciado.

**inventario · media · R1 parcial · R2 correta** Em um sistema de água de injeção de FPSO que usa bissulfito como sequestrante de oxigênio, a água passou a chegar com cloro residual em excesso. Como tende a ficar a remoção de oxigênio dissolvido?

- Referência: Menor, porque parte do bissulfito é consumida pelo cloro residual em vez de reagir com o oxigênio.
- R1: O excesso de cloro residual pode reduzir a eficiência da remoção de oxigênio dissolvido, pois o cloro reage com materiais oxidáveis, concorrendo com o oxigênio pela reação, possivelmente dificultando a diminuição do oxigênio na água.
- R2: Com cloro residual em excesso, a capacidade redutora do bissulfito está insuficiente/foi consumida, indicando “breakthrough” do oxidante. Assim, a remoção de oxigênio dissolvido tende a piorar, ficando DO mais alto (menor remoção) e mantendo condição oxidante com residual de cloro.
- Juiz: R2 reproduz o mecanismo decisivo — o cloro residual consome bissulfito e sobra menos sequestrante para remover O2 — enquanto R1 fica parcial por falar só em concorrência genérica; a referência é válida e não há atalho genérico porque é preciso apontar essa reação específica.

**inventario · media · R1 correta · R2 correta · atalho** Na água de injeção de um FPSO, a equipe precisa definir o regime de biocida para controle microbiológico e já possui validação de eficácia para o circuito em operação. Com que critério esse regime deve ser escolhido?

- Referência: Pelas condições do circuito e pela validação de eficácia; o programa pode usar dosagem contínua ou aplicações intermitentes.
- R1: O regime deve ser escolhido baseado na compatibilidade com o sistema, o perfil microbiológico, o tipo de microbiota presente e a frequência de aplicação, priorizando eficácia comprovada, segurança operacional e minimização de impacto ambiental.
- R2: O regime deve ser definido por um critério de desempenho microbiológico: manter, no ponto crítico do circuito (pior condição de contato/consumo), a concentração residual de biocida e a eficácia comprovada (redução/controle dos indicadores) nos cenários de operação (vazão, temperatura, demanda orgânica), conforme a validação.
- Juiz: O critério decisivo é escolher o regime pelas condições do circuito com eficácia já validada, o que ambos capturam de modo aceitável; a referência é válida, mas ampla o suficiente para admitir resposta bem genérica.

**inventario · media · R1 parcial · R2 parcial · atalho** Num FPSO, o MEG é injetado em topside e subsea e հետո regenerado para reúso. Após elevar a dosagem para ampliar a margem operacional em baixa temperatura, a concentração na fase aquosa permanece adequada, mas o teor de sais aumenta no circuito de recuperação. Que critério deve orientar o programa de MEG?

- Referência: Equilibrar simultaneamente a proteção contra hidratos e o controle de sais na recuperação do MEG.
- R1: O programa de MEG deve ser orientado pelo controle da concentração de sais e do teor de condensado, garantindo a eficiência do dessalhamento e evitando a corrosão, além de manter a integridade do sistema e a recuperação adequada do gás.
- R2: O programa de MEG deve ser orientado pelo limite de sais/carga iônica no circuito de recuperação (TDS/condutividade, principalmente Cl⁻/Na⁺), para evitar acumulação e incrustação/corrosão, em vez de apenas pela concentração na fase aquosa.
- Juiz: A resposta esperada era balancear simultaneamente a proteção contra hidratos com o controle de sais no circuito de recuperação do MEG, e R1 e R2 pegam sobretudo o lado dos sais sem explicitar o compromisso conjunto com a função anti-hidrato, enquanto o trade-off já está quase explícito no enunciado.

**inventario · media · R1 correta · R2 correta · atalho** Em um FPSO, o gás úmido recebe MEG na linha de produção, enquanto a etapa de adoçamento usa amina e outro trecho exige controle de corrosão e espuma. Ao revisar os pontos de injeção, que critério deve definir em que corrente cada produto será aplicado?

- Referência: A ameaça dominante em cada trecho, porque cada produto químico atua sobre um problema específico.
- R1: A escolha é baseada na fase do fluido, composição, potencial de corrosão, necessidade de remoção de umidade ou aminas, garantindo eficiência e proteção específica em cada etapa.
- R2: Defina por critério de “alvo químico e mecanismo”: aplicar cada produto apenas na corrente onde existam as espécies/condições que causam o problema (MEG onde há risco de formação de hidratos por água+gás; amina na corrente com CO2/H2S; inibidor de corrosão e antiespuma no trecho onde atuam, conforme água, salinidade, pH e tendência de corrosão/espuma sob T e P locais).
- Juiz: A referência é válida porque o critério é aplicar cada químico na corrente cuja ameaça ou alvo químico dominante ele trata, o que R2 explicita e R1 também expressa de forma mais ampla, e uma resposta genérica do tipo 'onde está o problema' já passaria.

**inventario · media · R1 incorreta · R2 correta** Em um poço com produção de gás e água, adota-se injeção contínua de MEG na cabeça do poço para prevenir o sólido que pode obstruir o escoamento. Como fica a condição térmica em que esse sólido passa a se formar?

- Referência: Ela diminui: o MEG reduz a temperatura de formação de hidratos.
- R1: O sólido se forma quando a temperatura do gás diminui abaixo do ponto de orvalho ou do ponto de congelamento do componente, formando hidratos de gás ou outros sólidos.
- R2: Com MEG contínuo, o sólido (gelo/hidrato) só passa a se formar quando a temperatura cair abaixo da curva de estabilidade do sistema água+MEG (ponto de congelamento reduzido e inibição de hidratos). Na prática, a formação é deslocada para temperaturas bem menores e ocorre apenas após consumo/depleção do MEG ou por perda de concentração.
- Juiz: O ponto decisivo é que o MEG desloca a formação de hidratos para temperaturas menores, então R2 é correta, R1 é incorreta por não tratar desse efeito e usar critérios inadequados, a referência é válida e não há atalho genérico.

**inventario · media · R1 correta · R2 correta · atalho** Em um poço ligado a um FPSO, a dosagem química mantém o produto ativo na fase aquosa e ele passa a interferir na nucleação, no crescimento e na aglomeração dos cristais antes da precipitação. Que efeito se espera na coluna, no gravel e nas demais superfícies molhadas?

- Referência: Redução da tendência de formação de depósitos aderentes nessas superfícies.
- R1: Espera-se redução da formação de depósitos, menor incrustação e melhor fluxo nas superfícies molhadas, devido à inibição da nucleação e crescimento de cristais.
- R2: Espera-se redução do fouling por incrustação: a dosagem inibe nucleação/crescimento e aglomeração, gerando cristais menores e dispersos ou mantendo-os em suspensão. Assim, a coluna, gravel e demais superfícies molhadas tendem a receber menor massa e menor aderência de precipitado, com menor obstrução da permeabilidade.
- Juiz: Como o decisivo era prever menor formação de incrustação aderente nas superfícies molhadas pela interferência na nucleação, crescimento e aglomeração, R1 e R2 acertam; a referência é válida e há atalho genérico porque o próprio mecanismo descrito no enunciado leva quase diretamente à resposta de redução de depósitos.

**inventario · media · R1 correta · R2 correta · atalho** Durante o manuseio de químicos em um FPSO, a área de transferência tem mureta, piso estanque e coleta local; em outra área similar, o líquido escoa livremente pelo convés. Se uma mangueira vazar, o que muda na primeira condição?

- Referência: Reduz a propagação do derrame, limitando a exposição de pessoas, equipamentos, áreas vizinhas e meio externo.
- R1: Na primeira condição, a mureta, piso estanque e coleta local limitam a dispersão do líquido, facilitando controle e contenção do vazamento, ao contrário da área sem esses recursos, onde o líquido se espalha livremente.
- R2: Na primeira condição, um vazamento da mangueira fica contido pela mureta e pelo piso estanque e é direcionado à coleta local, reduzindo a área afetada e evitando dispersão pelo convés. Na segunda, o líquido escoa livremente, espalhando e aumentando o volume potencialmente contaminante.
- Juiz: A referência é válida e o elemento decisivo é a contenção local reduzir a propagação do derrame e a exposição, exatamente o que ambos descrevem, em uma pergunta resolvível por associação direta.
