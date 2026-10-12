# Limpeza, gas freeing e entrada em tanques

## 1. Contexto operacional e objetivo de segurança
A preparação de tanques para inspeção, manutenção e entrada de pessoas em FPSOs/FSUs envolve uma transição controlada entre diferentes estados atmosféricos do tanque: condição com vapores de hidrocarbonetos, condição inertizada, condição em purga e, por fim, condição ventilada com ar para entrada segura. Em FPSOs, essa etapa é particularmente crítica porque o sistema de ventilação/venting é um sistema de segurança e de continuidade operacional: o óleo aquecido descarregado para tanques pode evoluir gás, aumentando a carga no sistema de vent e a quantidade de hidrocarbonetos potencialmente liberados. Como o FPSO tende a permanecer praticamente fixo, em tempo calmo há menor ajuda da movimentação do navio para dispersão dos vapores nos pontos de descarga do vent. Por isso, o preparo do tanque não pode ser tratado como atividade isolada do sistema de ventilação/blanketing/inertização.  

Além da segurança de pessoas, a operação de limpeza e abertura do tanque tem impacto direto na integridade: entrada indevida de oxigênio, permanência de resíduos aquosos, depósitos, sedimentos, biofilmes e falhas de venting podem acelerar processos corrosivos, criar atmosferas perigosas ou comprometer o retorno seguro ao serviço.  

**Fontes:** `hse-04d3623c0070fad00a0b82db:p54-56:31.0-24.0`, `anp-28ecd3b4b0e4434d9511c613:p2-4:17.0-44.0`

## 2. Sequência técnica de preparação do tanque

### 2.1 Avaliação prévia
Antes de qualquer entrada em tanque, deve ser realizada avaliação de riscos. Os testes de gás prévios devem refletir os contaminantes razoavelmente esperados no espaço, considerando pelo menos:
- conteúdo anterior do tanque;
- forma de ventilação do espaço;
- geometria/estrutura interna do tanque;
- revestimentos existentes;
- outros fatores relevantes do serviço anterior.  

Essa lógica também vale para espaços que normalmente não conteriam vapores de carga, como tanques de lastro e void spaces adjacentes a tanques de carga ou bunker: é prudente testar vapores de carga, deficiência de oxigênio e gases tóxicos quando houver adjacência ou possibilidade de migração.  

**Fontes:** `hse-04d3623c0070fad00a0b82db:p54-56:31.0-24.0`

### 2.2 Tank washing para remoção de depósitos
Se o tanque transportou óleo cru, normalmente será necessário passar por tank washing para remover depósitos antes da abertura. O ponto crítico é que a lavagem não deve degradar a condição atmosférica a um estado perigoso. O material da HSE informa um critério operacional específico: se, em qualquer momento durante a lavagem, o teor de O2 exceder 8%, a lavagem deve ser interrompida até que as condições se estabilizem em 8% O2 ou menos.  

O sentido técnico desse controle é evitar que a lavagem e a movimentação interna de vapores/desprendimentos levem a atmosfera do tanque para uma faixa inflamável. Em outras palavras, a lavagem não é apenas remoção de sujeira; ela é uma etapa ainda subordinada ao controle da atmosfera.  

**Fontes:** `hse-04d3623c0070fad00a0b82db:p54-56:31.0-24.0`

### 2.3 Purga com gás inerte
Após a lavagem, deve-se purgar a atmosfera com gás inerte até que ela possa ser testada e demonstrada com 2% ou menos de hidrocarbonetos. Segundo o material fornecido, esse patamar é usado para assegurar que, na etapa subsequente de gas freeing com ar, nenhuma parte da atmosfera do tanque atravesse a faixa inflamável.  

Esse ponto é central: a simples injeção direta de ar em um tanque ainda rico em hidrocarbonetos pode fazer a atmosfera passar pela região de inflamabilidade. A purga com gás inerte atua como etapa intermediária de redução segura da concentração de vapores combustíveis.  

**Fontes:** `hse-04d3623c0070fad00a0b82db:p54-56:31.0-24.0`

### 2.4 Gas freeing com ar
Somente depois da purga/inertização adequada é que se realiza gas freeing extensivo com ar fresco, até que a atmosfera do tanque atinja condição segura para entrada, sem ter passado pela faixa inflamável durante a transição. O conjunto fonte não fornece valores numéricos completos de aceitação para entrada humana após gas freeing; portanto, a aceitação final deve seguir o procedimento da instalação, a avaliação de riscos e a autoridade competente aplicável.  

**Fontes:** `hse-04d3623c0070fad00a0b82db:p54-56:31.0-24.0`

### 2.5 Tanques com hydrocarbon blanketing
Mesmo quando o FPSO utiliza hydrocarbon blanketing como sistema fechado para reduzir emissões e impedir entrada de oxigênio, os tanques ainda precisarão ser inspecionados ao longo da vida útil. Para isso, continuarão necessitando de gas freeing. O material da HSE indica que, nessas situações, será necessário um gerador de gás inerte: o gás inerte desloca os vapores de hidrocarbonetos do tanque mantendo o oxigênio abaixo de condição que sustente inflamabilidade, antes da purga posterior com ar.  

**Fontes:** `hse-04d3623c0070fad00a0b82db:p54-56:31.0-24.0`

## 3. Monitoramento atmosférico e interpretação das medições

### 3.1 O que monitorar
Para a preparação e a entrada em tanques, o conjunto de fontes sustenta pelo menos o monitoramento de:
- oxigênio (O2);
- hidrocarbonetos na atmosfera;
- gases tóxicos esperados, com destaque para H2S quando plausível pelo histórico do fluido/resíduo;
- em análises complementares de líquidos e resíduos: CO2 dissolvido, sulfatos, sulfetos, cloretos, pH, ácidos orgânicos, BSW, ferro total, bactérias redutoras de sulfato (BRS) e bactérias anaeróbicas heterotróficas totais (BANHT).  

Para resíduos sólidos, o material também cita caracterização de matéria inorgânica, sulfetos e contagem de bactérias sésseis. Isso é útil quando, após abertura do tanque, deseja-se distinguir se a condição encontrada é apenas “sujeira operacional” ou evidência de mecanismo corrosivo ativo ou recente.  

**Fontes:** `regis-8ce2356779a6c764f3bd597f:pNone:1866.0-2110.0`

### 3.2 Cuidado com amostras despressurizadas
Em fluidos produzidos ou resíduos contendo gases dissolvidos, resultados laboratoriais obtidos após retirada da amostra em pressão atmosférica podem não reproduzir fielmente a química existente sob condição operacional. O material cita, por exemplo, que a liberação de CO2 na despressurização altera a acidificação da fase aquosa e pode levar a pH de laboratório diferente do pH efetivo em serviço.  

Para tanques, essa observação é importante em duas frentes:
1. interpretação de amostras de água residual/slop após abertura do sistema;  
2. comparação entre medições de campo e análises de laboratório na investigação de corrosão ou risco toxicológico.  

**Fontes:** `petroles-4ee4bce16acf674505c8912d:pNone:2584975.0-2585022.0`

### 3.3 Instrumentação útil para avaliação de corrosividade e oxigênio em sistemas associados
Os trechos fornecidos descrevem três famílias de monitoramento úteis para integridade de sistemas com fluidos/resíduos correlatos:
- **sondas de resistência elétrica (ER):** acompanham corrosão acumulada pela variação de resistência elétrica associada à perda de seção do elemento sensor;
- **sondas LPR (Linear Polarization Resistance):** medem corrosividade instantânea do meio, com taxa de corrosão inversamente proporcional à resistência de polarização;
- **sondas galvânicas:** são altamente sensíveis ao oxigênio dissolvido e servem mais ao controle de níveis de oxigênio ou à avaliação de sequestrantes de oxigênio do que à medição direta de taxa de corrosão.  

Em um contexto de tanque, essas técnicas são mais diretamente aplicáveis a sistemas associados, linhas, drenos, recirculações e circuitos onde haja histórico de água residual, produtos químicos ou zonas estagnadas. A escolha do método, instrumento, periodicidade e critério de aceitação deve integrar o programa documentado de monitoramento e controle de corrosão.  

**Fontes:** `regis-8ce2356779a6c764f3bd597f:pNone:1866.0-2110.0`, `anp-28ecd3b4b0e4434d9511c613:p2-4:17.0-44.0`

## 4. Limpeza e integridade: mecanismos relevantes durante parada, abertura e retorno

### 4.1 Papel do oxigênio
Os materiais mostram que o oxigênio tem papel duplo e potencialmente contraditório, que precisa ser entendido na operação de tanques:
- **na segurança de processo/entrada**, a presença de oxigênio é variável crítica para inflamabilidade durante lavagem, purga e gas freeing;
- **na integridade**, oxigênio dissolvido em água residual é agente corrosivo importante, acelerando corrosão por despolarização catódica em superfícies molhadas.  

Por outro lado, a remoção quase completa do oxigênio em volumes estagnados de água pode reduzir certa corrosão aeróbia uniforme, mas favorecer anaerobiose e o desenvolvimento de BRS/BANHT, associados à corrosão influenciada por microrganismos (MIC/CIM). Assim, nem a simples presença nem a simples ausência de oxigênio, isoladamente, resolvem o problema de integridade: é preciso controlar também água residual, nutrientes, depósitos e tempo de estagnação.  

**Fontes:** `petroles-4ee4bce16acf674505c8912d:pNone:764817.0-764847.0`, `hse-04d3623c0070fad00a0b82db:p54-56:31.0-24.0`

### 4.2 Biofilme, depósitos e limpeza
O material técnico sobre hibernação/teste hidrostático destaca que a formação de biofilme ocorre por adsorção de compostos orgânicos, fixação de bactérias sésseis, produção de exopolímeros e crescimento de comunidades microbianas. O biofilme dificulta difusão, protege microrganismos contra alguns biocidas e pode levar a corrosão sob depósito. Também é mencionado explicitamente que limpeza e sanitização impedem ou minimizam a formação de biofilme.  

Transferindo esse mecanismo de forma prudente para tanques e espaços com água residual, a limpeza não deve ser vista só como preparo para entrada, mas também como medida de controle de integridade, especialmente onde haja:
- fundos de água persistentes;
- slops e resíduos oleosos com sólidos;
- sedimentos e sais;
- regiões de baixa circulação ou estagnação.  

**Fontes:** `petroles-4ee4bce16acf674505c8912d:pNone:764817.0-764847.0`

### 4.3 O que verificar fisicamente após abertura
Com base nas fontes de integridade e monitoramento, a abertura de tanque é oportunidade para verificar, documentar e classificar pelo menos:
- presença de depósitos, sedimentos e resíduos aderidos;
- indícios de corrosão generalizada ou localizada;
- sinais de processos microbiológicos quando houver água residual, lodo, odor sulfídrico ou biofilme;
- eficácia aparente da limpeza e da drenagem;
- anormalidades nos sistemas de vent/linhas associadas, quando aplicável;
- necessidade de complementar o programa de monitoramento com análises de resíduos, bactérias, oxigênio dissolvido ou técnicas de corrosão.  

O material da ANP reforça que planos de manutenção, inspeção, testes e ensaios devem ser estabelecidos e documentados; que o programa de monitoramento e controle de corrosão precisa identificar métodos, instrumentos, periodicidade, critérios de aceitação e recursos; e que deve existir procedimento de inspeção do sistema de vent, quando aplicável.  

**Fontes:** `anp-28ecd3b4b0e4434d9511c613:p2-4:17.0-44.0`, `regis-8ce2356779a6c764f3bd597f:pNone:1866.0-2110.0`, `petroles-4ee4bce16acf674505c8912d:pNone:764817.0-764847.0`

## 5. Resposta a condições anormais
As fontes permitem estabelecer alguns gatilhos claros de parada, reavaliação ou não prosseguimento da atividade:

1. **O2 acima de 8% durante tank washing de tanque que carregou óleo cru:** interromper a lavagem até estabilização em 8% O2 ou menos.  
2. **Atmosfera com mais de 2% de hidrocarbonetos antes da introdução de ar para gas freeing:** manter/retomar a purga com gás inerte; não avançar para aeração direta.  
3. **Detecção inesperada de vapores de carga, deficiência de O2 ou gases tóxicos em tanque de lastro/void space adjacente:** tratar o espaço como potencialmente contaminado e reavaliar o plano de entrada.  
4. **Indícios de ingresso de oxigênio, corrosão anormal ou falha no venting/inertização:** tratar como modo de falha a ser incorporado à análise de risco e ao gerenciamento da integridade.  
5. **Anormalidades encontradas em comissionamento/recomissionamento:** documentar e fechar pendências impeditivas antes do retorno ao serviço.  

Além disso, o FPSO pode ter maior vulnerabilidade à formação de atmosferas inflamáveis ao redor das saídas de vent em condições de tempo calmo e com óleo aquecido/gaseificante, porque a dispersão natural dos vapores pode ser pior do que em um navio-tanque em movimento.  

**Fontes:** `hse-04d3623c0070fad00a0b82db:p54-56:31.0-24.0`, `anp-28ecd3b4b0e4434d9511c613:p2-4:17.0-44.0`

## 6. Retorno ao serviço do tanque
O conjunto de fontes não fornece um procedimento completo de retorno ao serviço passo a passo, mas sustenta alguns princípios técnicos que não devem ser omitidos:

- o retorno ao serviço deve ser tratado como **recomissionamento controlado**, não apenas como encerramento da inspeção;
- as **anormalidades encontradas** devem constar em relatório de comissionamento/recomissionamento;
- o **sistema de vent** e os elementos associados à inertização/blanketing devem ser verificados quanto à adequação e condição funcional, quando aplicável;
- a **atmosfera final do tanque** deve ser compatível com o modo operacional de retorno; isto é, tanque destinado a voltar ao serviço com hidrocarbonetos não deve ser simplesmente reintroduzido em operação a partir de uma condição de abertura sem transição atmosférica controlada;
- achados de corrosão, resíduos, bactérias ou ingresso de oxigênio devem retroalimentar a **análise de risco**, o programa de **monitoramento e controle de corrosão** e os procedimentos operacionais.  

Nos casos em que exista hydrocarbon blanketing, o material da HSE também informa que, em modo de offloading, é provável o uso de sistema de gás inerte para manter pressão nos tanques. Isso reforça que o retorno à condição operacional depende da filosofia atmosférica do tanque em cada modo de operação.  

**Fontes:** `anp-28ecd3b4b0e4434d9511c613:p2-4:17.0-44.0`, `hse-04d3623c0070fad00a0b82db:p54-56:31.0-24.0`

## 7. Síntese operacional
Para esta faceta, a lógica técnica central é:
1. avaliar riscos e contaminantes plausíveis;  
2. remover depósitos com tank washing sem perder o controle do O2;  
3. purgar com gás inerte até reduzir hidrocarbonetos a patamar que permita transição segura;  
4. executar gas freeing com ar até condição segura para entrada;  
5. monitorar atmosfera e resíduos com foco simultâneo em segurança e integridade;  
6. inspecionar corrosão, depósitos, biofilme, água residual e venting;  
7. só retornar ao serviço após recomissionamento documentado, fechamento de anormalidades e restauração da filosofia atmosférica adequada do tanque.  

**Fontes:** `hse-04d3623c0070fad00a0b82db:p54-56:31.0-24.0`, `anp-28ecd3b4b0e4434d9511c613:p2-4:17.0-44.0`, `regis-8ce2356779a6c764f3bd597f:pNone:1866.0-2110.0`, `petroles-4ee4bce16acf674505c8912d:pNone:764817.0-764847.0`