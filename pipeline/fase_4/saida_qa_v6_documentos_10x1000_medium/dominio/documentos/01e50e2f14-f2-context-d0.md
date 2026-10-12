# Disponibilidade e perdas de produção em FPSOs/FSOs: medição da disponibilidade, eficiência e apuração de perdas

## 1. Contexto gerencial da faceta
Em unidades de produção contínua, como FPSOs e sistemas associados, a gestão do desempenho é fortemente orientada pela continuidade operacional. A lógica gerencial central não é apenas “produzir quando possível”, mas manter a capacidade de produzir, sustentar a produção na faixa operacional adequada e minimizar interrupções, derates e perdas. Nesse contexto, indicadores de disponibilidade e de perdas de produção são KPIs estruturantes porque conectam confiabilidade dos ativos, prontidão operacional, custo, risco e resultado econômico.

Os trechos disponíveis também mostram que, em ambientes produtivos contínuos, o planejamento/engenharia de produção costuma exercer papel semelhante ao PCP, consolidando volume de produção, prazos, paradas programadas e controle/avaliação de resultados. Para KPI de disponibilidade e perdas, isso é relevante porque o indicador não é apenas um retrato técnico do equipamento: ele depende de como a organização programa paradas, registra anormalidades, integra operação e manutenção e consolida resultados.

**Fontes:** `regis-4d3e6334d0d2f5df318c7403:pNone:581.0-608.0`, `regis-4d3e6334d0d2f5df318c7403:pNone:593.0-620.0`

## 2. Conceitos de disponibilidade aplicáveis à gestão de FPSO

### 2.1 Fator de disponibilidade
O fator de disponibilidade é a relação entre **horas disponíveis** e **horas do período**. Horas disponíveis são aquelas em que o equipamento ou a unidade está em condições de produzir, mesmo que não esteja produzindo de fato. Esse indicador mede a aptidão para produzir, e não a produção efetivamente realizada.

Forma geral:

- **Fator de disponibilidade = horas disponíveis / horas do período**

Interpretação para FPSO:
- é útil quando a pergunta gerencial é: **“a unidade estava apta a operar?”**;
- separa prontidão da unidade de restrições comerciais, de escoamento, de priorização operacional ou de despacho;
- não mede sozinho se a unidade produziu à plena carga.

### 2.2 Disponibilidade equivalente
A disponibilidade equivalente é a relação entre **horas equivalentes disponíveis** e **horas do período**. As horas equivalentes disponíveis decorrem das horas disponíveis, descontadas as paradas forçadas e programadas, parciais e totais. O foco aqui é a capacidade de produzir **à plena carga**.

Forma geral:

- **Disponibilidade equivalente = horas equivalentes disponíveis / horas do período**

Interpretação para FPSO:
- é mais aderente quando há **restrições parciais** de capacidade, por exemplo limitação em compressão de gás, tratamento de água, utilidades, exportação ou subsistemas de processo;
- captura melhor o efeito de derates do que o simples fator de disponibilidade;
- continua sem explicar, por si só, se a indisponibilidade foi provocada por causa forçada ou programada.

### 2.3 Taxa de paradas forçadas
A taxa de paradas forçadas mede a exposição da unidade a interrupções não planejadas.

Forma geral:

- **Taxa de paradas forçadas = horas de paradas forçadas / (horas de operação + horas de paradas forçadas)**

Interpretação para FPSO:
- é um KPI útil para confiabilidade operacional;
- destaca interrupções que efetivamente quebram a continuidade da produção;
- é particularmente útil para análise de tendência de falhas de sistemas críticos, como geração elétrica, compressão, bombeamento, utilidades, automação, medição e exportação.

### 2.4 Fator de capacidade
O fator de capacidade relaciona a produção bruta efetiva à produção potencial máxima no período.

Forma geral:

- **Fator de capacidade = produção total bruta / (horas do período × capacidade máxima)**

Interpretação para FPSO:
- responde à pergunta: **“quanto da capacidade instalada foi efetivamente utilizada?”**;
- é sensível não apenas à indisponibilidade, mas também a limitações de reservatório, restrições operacionais, campanhas de manutenção, escoamento e condições de operação fora do ponto ótimo;
- é um KPI mais próximo da eficiência de utilização do ativo do que da mera prontidão.

### 2.5 Disponibilidade mecânica versus disponibilidade operacional
Outro ponto relevante é distinguir dois níveis de disponibilidade:

- **Disponibilidade mecânica**: relacionada à confiabilidade mecânica do ativo. Seu valor gerencial está em reduzir risco de interrupções involuntárias, perdas de produção e perdas de receita.
- **Disponibilidade operacional**: considera que a unidade esteja disponível e pronta para produzir, sem restrições de insumos/condições necessárias ao processo. A disponibilidade mecânica integra e afeta esse cálculo, mas não o esgota.

Para um FPSO, essa distinção evita erros comuns de leitura do KPI. Uma unidade pode ter boa disponibilidade mecânica e, ainda assim, baixa disponibilidade operacional por restrições de alimentação, utilidades, exportação, requisitos de segurança, condicionantes ambientais ou limitações sistêmicas externas à integridade mecânica imediata.

**Fontes:** `regis-4d3e6334d0d2f5df318c7403:pNone:593.0-620.0`, `regis-db7f3abd931d75c5b821bf6a:pNone:12132.0-12300.0`

## 3. Critérios de escolha do KPI de disponibilidade
A escolha do indicador deve seguir a decisão gerencial que se deseja apoiar.

### 3.1 Quando usar cada indicador
- **Fator de disponibilidade**: quando se quer medir **aptidão para produzir**.
- **Disponibilidade equivalente**: quando se quer medir **aptidão para produzir à plena carga**, inclusive capturando restrições parciais.
- **Taxa de paradas forçadas**: quando se quer medir **desempenho real frente a falhas não planejadas**.
- **Fator de capacidade**: quando se quer comparar **produção efetiva com potencial nominal**.
- **Disponibilidade mecânica**: quando o foco é **confiabilidade do ativo**.
- **Disponibilidade operacional**: quando o foco é **prontidão sistêmica para produzir**.

### 3.2 Risco de interpretação inadequada
Usar apenas um único indicador pode mascarar problemas:
- alta disponibilidade com baixo fator de capacidade pode indicar unidade apta, mas subutilizada;
- alta disponibilidade mecânica com baixa disponibilidade operacional pode revelar restrições fora da manutenção corretiva tradicional;
- boa produção em determinado período pode coexistir com elevada taxa de paradas forçadas compensada por operação intensiva em outro período, o que não significa robustez estrutural.

### 3.3 Comparação com padrão de referência
Os trechos utilizados indicam que sistemas de medição de desempenho se baseiam na comparação do realizado com um padrão: capacidade teórica, plena carga, produção programada ou outro referencial definido. Para FPSOs, a governança do KPI deve deixar explícito qual é o denominador gerencial adotado: capacidade de projeto, capacidade segura, capacidade licenciada, capacidade disponível do gargalo ou meta programada.

**Fontes:** `regis-4d3e6334d0d2f5df318c7403:pNone:593.0-620.0`, `regis-db7f3abd931d75c5b821bf6a:pNone:12132.0-12300.0`

## 4. Apuração das perdas de produção

### 4.1 Conceito operacional
As perdas de produção estão presentes em processos industriais em geral e, no setor de petróleo, surgem com frequência quando poços, equipamentos ou sistemas deixam de produzir, produzem menos do que o potencial ou operam sob restrição. O impacto é duplo: redução de produção/receita e aumento de custos.

No material fornecido, um estudo da OP-MG é usado para diagnosticar perdas de produção de óleo, identificar principais motivos de parada de poços e acompanhar essas perdas com ferramentas de gestão por processos. Embora o caso seja onshore, a lógica gerencial é transferível: registrar anormalidades, classificar motivos, priorizar recorrências e tratar causas-raiz.

### 4.2 Base de dados e rastreabilidade das perdas
O SIP é descrito como banco de dados oficial que registra, entre outros elementos:
- produção diária de óleo, gás, água e LGN;
- potencial-base dos poços;
- variáveis de referência dos poços, como BSW, RGO e RGLI;
- testes de produção;
- anormalidades causadoras das perdas, discriminadas por motivo, providência e responsáveis;
- injeção de fluidos.

Para a apuração das perdas, isso é crucial porque a reconciliação diária depende de três blocos de informação explicitados no trecho:
1. **potencial-base**;
2. **perda-base**;
3. **dados dos medidores**.

Assim, a perda de produção não deve ser tratada apenas como “volume que deixou de sair”, mas como resultado de uma comparação estruturada entre o potencial esperado, as perdas registradas e a produção efetivamente medida.

### 4.3 Perdas totais, parciais e por motivo
Mesmo sem a fórmula completa no trecho, a lógica de gestão é clara:
- eventos precisam ser classificados por **motivo**;
- a perda deve ser associada a um **responsável** e a uma **providência**;
- a análise deve permitir visão por **grupo de motivo**, por **sistema/método** e por **tempo de indisponibilidade**.

Em um FPSO, essa lógica pode ser aplicada a categorias como:
- poço/subsea;
- escoamento e elevação/interligação;
- processamento topside;
- utilidades e geração;
- medição;
- exportação/offloading;
- restrições de segurança/ambiente/operação.

O ponto técnico importante é que o KPI de perdas precisa distinguir:
- **perda por parada total** versus **perda por restrição parcial**;
- **perda por falha forçada** versus **perda programada**;
- **perda por limitação própria do ativo** versus **perda por condicionante externa**.

### 4.4 Ferramentas para análise das perdas
O material cita explicitamente o uso de:
- **PDCA**;
- **Diagrama de Pareto**;
- **Diagrama de Causa e Efeito / Ishikawa**;
- **Árvore de Falhas**;
- **Análise de Causa Raiz (ACR)**.

Na governança de KPI, essas ferramentas cumprem papéis diferentes:
- **Pareto**: prioriza os poucos motivos que concentram a maior parte das perdas;
- **Árvore de falhas**: estrutura encadeamentos lógicos entre falhas básicas e evento topo de perda/indisponibilidade;
- **ACR**: aprofunda mecanismos causais e evita correções superficiais;
- **PDCA**: fecha o ciclo entre medição, análise, ação corretiva/preventiva e padronização.

**Fontes:** `petroles-004c2afadba7ea17c7dd7908:pNone:2036799.0-2036870.0`, `petroles-004c2afadba7ea17c7dd7908:pNone:1855015.0-1855053.0`

## 5. Medição, calibração e qualidade dos dados de perda
A qualidade do KPI depende diretamente da qualidade da medição. O material indica que a ANP exige calibração periódica dos sistemas de medição e adota exigências distintas conforme a finalidade do medidor. Ainda que os números específicos estejam suprimidos no trecho, a implicação técnica é inequívoca: erro metrológico pode distorcer produção realizada, apropriação de volumes e, por consequência, a própria apuração das perdas.

O exemplo fornecido é particularmente importante para FPSOs com arranjos integrados de medição/apropriação/fiscalização: após intervenção em poço de uma plataforma, o aumento de potencial apareceu em outra plataforma, comportamento que se mostrou decorrente de medidores descalibrados. Após calibração, a tendência ficou coerente com a intervenção realizada.

Consequências práticas para KPI de disponibilidade e perdas:
- uma perda pode ser **aparente**, não real, se a medição estiver comprometida;
- a distribuição da produção entre ativos, poços ou plataformas pode ser indevidamente deslocada;
- indicadores de eficiência operacional global podem ser enviesados pela base metrológica;
- o fechamento diário de perdas deve incluir verificação mínima de coerência entre evento operacional, potencial-base e medição.

Em FPSOs, isso se torna crítico quando há separação entre medição para apropriação interna e medição fiscal ou quando a produção passa por mais de um ponto de quantificação antes da consolidação corporativa.

**Fontes:** `petroles-004c2afadba7ea17c7dd7908:pNone:1855015.0-1855053.0`

## 6. Relação entre confiabilidade, indisponibilidade e perdas de produção
Os trechos de confiabilidade indicam que a melhora da disponibilidade mecânica reduz riscos de interrupções involuntárias, perdas de produção e perdas de receita. Também indicam que aumento da confiabilidade pode reduzir o prazo de indisponibilidade, diminuir custos e até melhorar condições de intervenção.

Para gestão de FPSO, a relação causal básica é:

1. **maior confiabilidade** tende a reduzir falhas e paradas forçadas;
2. menos paradas forçadas tende a aumentar disponibilidade mecânica;
3. maior disponibilidade mecânica contribui para maior disponibilidade operacional;
4. maior disponibilidade operacional reduz perdas de produção e melhora utilização do ativo.

O material também destaca que o percentual de utilização do ativo melhora quando se amplia o período de operação dentro das especificações e se reduzem paradas imprevistas. Em unidades offshore, isso pode equivaler a sustentar campanha com menor frequência de interrupções, retorno mais rápido após manutenção e menor recorrência de falhas de sistemas críticos.

**Fontes:** `regis-db7f3abd931d75c5b821bf6a:pNone:12132.0-12300.0`

## 7. Nem toda indisponibilidade vem de falha de equipamento
Um ponto importante para a correta apuração de perdas é que indisponibilidade operacional pode existir mesmo sem falha intrínseca do equipamento. O estudo sobre operações de alívio mostra situações em que o downtime decorre de condições ambientais excedendo limites operacionais/safe operating envelope ou de restrições de setores e modos operacionais, sem considerar falhas em propulsão ou geração.

Lição aplicável a FPSO/FSO:
- parte da indisponibilidade pode ser causada por **restrições operacionais externas**, como metocean, janela de offloading, limites de aproximação ou critérios de segurança;
- essas perdas não devem ser automaticamente classificadas como falha mecânica do processo principal;
- para governança de KPI, convém separar pelo menos três naturezas de perda: **falha de equipamento**, **restrição operacional/sistêmica** e **restrição ambiental/segurança**.

Essa separação melhora a tomada de decisão, pois o tratamento é diferente: manutenção e confiabilidade para a primeira, revisão de procedimentos/setores operacionais para a segunda e gestão de risco/planejamento logístico para a terceira.

**Fontes:** `petroles-004c2afadba7ea17c7dd7908:pNone:3025161.0-3025189.0`

## 8. Alarmes, tempo de resposta e perdas de produção
A gestão de alarmes aparece no material como tema diretamente ligado à eficiência operacional. Pseudo-alarmes e configuração inadequada aumentam a carga cognitiva da operação, dificultam a identificação dos problemas reais e elevam o tempo de resposta às anormalidades. As consequências apontadas incluem aumento de risco à segurança, às instalações, ao meio ambiente e agravamento das perdas de produção.

Para KPI de disponibilidade e perdas, isso significa que o sistema de supervisão e controle influencia o desempenho, mesmo quando o equipamento principal está fisicamente íntegro. Em termos gerenciais:
- excesso de alarmes inúteis pode elevar tempo de recuperação de eventos;
- pior detecção diagnóstica pode transformar desvios pequenos em perdas maiores;
- a confiabilidade da informação operacional é parte da confiabilidade do processo.

Assim, indicadores de disponibilidade e perdas devem ser lidos em conjunto com indicadores de qualidade do sistema de alarmes e de resposta operacional, especialmente em plantas altamente automatizadas como FPSOs.

**Fontes:** `petroles-004c2afadba7ea17c7dd7908:pNone:2452524.0-2452607.0`

## 9. Impacto econômico dos indicadores
Os trechos sobre estrutura de custos mostram predominância de custos fixos, prazos longos de amortização e uso de custeio integral/centros de custos em processos contínuos. Isso reforça por que disponibilidade e perdas são KPIs econômicos e não apenas técnicos: quando a estrutura de custos fixos é alta, a indisponibilidade corrói rapidamente a geração de valor, porque o custo permanece enquanto a produção e a receita caem.

Além disso, o material de confiabilidade destaca que os efeitos da interrupção da produção aparecem no curto prazo, tanto operacional quanto economicamente. Portanto:
- perda de produção afeta receita diretamente;
- indisponibilidade eleva custo unitário por barril equivalente produzido;
- melhoria de confiabilidade reduz custo e tempo de indisponibilidade;
- bons KPIs de perdas apoiam priorização de investimentos com maior retorno operacional.

**Fontes:** `regis-4d3e6334d0d2f5df318c7403:pNone:581.0-608.0`, `regis-db7f3abd931d75c5b821bf6a:pNone:12132.0-12300.0`

## 10. Diretrizes práticas para apuração e gestão das perdas em FPSO
Com base nos trechos disponíveis, uma rotina tecnicamente consistente de KPI para disponibilidade e perdas deve incluir:

1. **Definir claramente o denominador do KPI**
   - horas do período, capacidade máxima, plena carga, produção programada ou outra base formal.

2. **Separar prontidão de produção efetiva**
   - disponibilidade não é sinônimo de produção realizada;
   - fator de capacidade não é sinônimo de confiabilidade.

3. **Classificar a perda por natureza**
   - forçada ou programada;
   - total ou parcial;
   - mecânica, operacional, metrológica, ambiental ou logística.

4. **Garantir qualidade metrológica**
   - calibração e coerência entre medição, potencial-base e evento registrado.

5. **Registrar anormalidades com rastreabilidade**
   - motivo, providência e responsável;
   - manter base histórica para análise de recorrência.

6. **Priorizar tratamento com Pareto**
   - concentrar esforços nos motivos de maior contribuição para perda total.

7. **Investigar causas profundas**
   - usar ACR, Ishikawa e árvore de falhas nos eventos prioritários.

8. **Fechar o ciclo de melhoria**
   - aplicar PDCA, padronizar soluções e monitorar efeito sobre indisponibilidade e volume perdido.

9. **Integrar operação, manutenção e planejamento**
   - evitar leitura setorial isolada dos indicadores;
   - privilegiar resultado global do processo produtivo.

10. **Distinguir falha de restrição operacional**
   - especialmente em offloading, utilidades, janelas ambientais e limitações de operação segura.

**Fontes:** `petroles-004c2afadba7ea17c7dd7908:pNone:2036799.0-2036870.0`, `petroles-004c2afadba7ea17c7dd7908:pNone:1855015.0-1855053.0`, `regis-4d3e6334d0d2f5df318c7403:pNone:581.0-608.0`, `regis-4d3e6334d0d2f5df318c7403:pNone:593.0-620.0`, `regis-db7f3abd931d75c5b821bf6a:pNone:12132.0-12300.0`, `petroles-004c2afadba7ea17c7dd7908:pNone:3025161.0-3025189.0`, `petroles-004c2afadba7ea17c7dd7908:pNone:2452524.0-2452607.0`

## 11. Exemplo de leitura integrada de KPI
Uma leitura madura de desempenho em FPSO pode seguir a seguinte lógica:

- **Disponibilidade mecânica alta + disponibilidade operacional baixa**: investigar restrições de insumos, exportação, utilidades, segurança ou logística.
- **Disponibilidade alta + fator de capacidade baixo**: investigar operação abaixo da capacidade, gargalos, restrições parciais ou limitação de alimentação.
- **Taxa de paradas forçadas alta + perdas concentradas em poucos motivos**: tratar confiabilidade dos sistemas críticos com Pareto + ACR.
- **Oscilação de perda sem coerência com eventos operacionais**: verificar calibração, apropriação e fechamento diário dos dados.
- **Downtime sem falha física evidente**: avaliar condicionantes ambientais e limites operacionais.
- **Resposta lenta a desvios**: revisar gestão de alarmes e qualidade da informação ao operador.

Essa abordagem evita o erro comum de atribuir toda perda à manutenção corretiva e melhora a qualidade da decisão sobre onde agir: equipamento, procedimento, medição, planejamento, operação ou interface logística.

**Fontes:** `regis-4d3e6334d0d2f5df318c7403:pNone:593.0-620.0`, `regis-db7f3abd931d75c5b821bf6a:pNone:12132.0-12300.0`, `petroles-004c2afadba7ea17c7dd7908:pNone:1855015.0-1855053.0`, `petroles-004c2afadba7ea17c7dd7908:pNone:3025161.0-3025189.0`, `petroles-004c2afadba7ea17c7dd7908:pNone:2452524.0-2452607.0`

## 12. Limites de aplicação do material
Os trechos fornecidos sustentam bem os conceitos de medição de disponibilidade, distinção entre disponibilidade mecânica e operacional, importância da confiabilidade, qualidade de medição e sistemática de tratamento de perdas. Entretanto, alguns detalhes quantitativos e fórmulas específicas de sistemas Petrobras/FPSO não aparecem integralmente nos excertos, de modo que o uso profissional do conteúdo deve ser entendido como base conceitual e analítica, e não como procedimento corporativo certificado.

**Fontes:** conjunto dos trechos citados nesta nota técnica.