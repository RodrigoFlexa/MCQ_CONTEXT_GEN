# Tratamento e validação dos dados na medição fiscal de óleo e gás e na transferência de custódia em offloading de FPSOs

## 1. Finalidade da camada de tratamento e validação

Na medição fiscal e na transferência de custódia, a etapa de tratamento e validação de dados existe para transformar dados brutos de campo em informação tecnicamente utilizável para contabilização volumétrica, balanços, faturamento, alocação e análises corporativas, sem perder a rastreabilidade do dado original.

Os trechos utilizados descrevem uma arquitetura de gestão de medições focada em **aquisição automática de dados de EFM/flow computers, tanques e laboratórios**, com mecanismos para:

- reduzir atividades manuais;
- preservar integridade do dado desde a origem;
- identificar automaticamente dados suspeitos;
- permitir correções controladas sem apagar o registro original;
- liberar ao nível corporativo apenas dados considerados representativos das condições operacionais.

Em termos práticos, isso significa que o sistema de validação não substitui a medição de campo, mas cria uma **camada formal de QA/QC, consistência, auditoria e governança de dados** entre a origem do dado e seu uso fiscal/comercial.  

**Fontes:** `petroles-004c2afadba7ea17c7dd7908:pNone:534469.0-534503.0`

## 2. Fontes de dados e princípio de integridade na origem

Uma arquitetura robusta de tratamento de dados de medição deve, sempre que possível, receber automaticamente os dados diretamente da fonte primária de medição, incluindo:

- **flow computers / EFM**;
- **tanques**;
- **laboratórios**.

Nos trechos, um objetivo central do sistema especializado de gestão de medições é a **coleta automática direta da fonte**, evitando manipulação manual desnecessária. Quando a automação não é possível, a fonte menciona a necessidade de **mecanismos alternativos para entrada manual com controles de segurança**.

Um elemento importante é a preservação do dado bruto em formato difícil de adulterar. O caso citado descreve captura de arquivos EFM em formato binário, com a intenção de que o conteúdo permaneça auditável e não seja alterado por usuários. O valor técnico desse arranjo, para fins fiscais e de custódia, está em:

1. manter o **registro primário**;
2. separar o **dado recebido** do **dado tratado/corrigido**;
3. tornar verificável qualquer alteração posterior.

Essa separação é especialmente relevante em medições com impacto financeiro, como medição fiscal de petróleo, medição fiscal de gás natural e transferência de custódia no offloading, porque reduz o risco de manipulação não controlada e facilita auditorias.

Além disso, os trechos diferenciam a função do sistema de gestão de medições da função do SCADA: o **SCADA** permanece voltado ao monitoramento e controle de processo em tempo real, enquanto a camada dedicada à medição concentra-se nos dados de EFM e na análise volumétrica. Essa separação tende a favorecer independência funcional da rotina metrológica e do tratamento de dados.

**Fontes:** `petroles-004c2afadba7ea17c7dd7908:pNone:534469.0-534503.0`

## 3. Pré-tratamento e validação primária dos dados

A validação primária é a primeira barreira contra uso indevido de dados em cálculo fiscal ou de custódia. Os trechos apontam verificações típicas que devem ser feitas logo após a aquisição:

- **falhas de comunicação** com o sistema de aquisição;
- **congelamento de dados**;
- **falhas de instrumentos**;
- **violação de limites máximos e mínimos válidos**;
- **picos irreais** nos sinais de processo.

Com base nessa triagem, a informação pode ser classificada em categorias de qualidade como:

- **boa**;
- **questionável**;
- **falha**.

Um ponto importante da fonte é que **dados falhos não devem ser reconciliados**; para fins analíticos, devem ser tratados como não medidos no conjunto de dados usado para detecção de erros grosseiros e reconciliação. Essa distinção é importante porque evita que o algoritmo “force” coerência física a partir de um dado sabidamente inválido.

Os trechos também indicam que, na seleção de variáveis de interesse para análise histórica ou condicionamento de dados, convém levantar estatísticas básicas, como:

- mínimo;
- máximo;
- média;
- variância.

Na fonte, variáveis com variância muito baixa podem ter baixa utilidade para certas análises estatísticas de retificação. Isso não significa que uma variável estável seja irrelevante para a medição fiscal; significa apenas que, em uma etapa de análise/condicionamento, ela pode carregar pouca informação estatística adicional.

### 3.1. Tipos de erro relevantes

Os trechos distinguem pelo menos três classes de erro:

- **Erros aleatórios**: decorrem de causas diversas e não coerentes; não são completamente elimináveis, mas seu efeito médio tende a zero com aumento do número de observações.
- **Erros grosseiros (outliers)**: observações claramente discrepantes, muitas vezes ligadas a falhas humanas, de registro ou a problemas evidentes de medição; devem ser detectados e removidos do conjunto analítico quando não representam o comportamento do processo.
- **Erros sistemáticos (bias)**: deslocamentos persistentes que afetam a concordância entre o valor médio medido e o valor de referência; têm implicação direta na exatidão metrológica e na reconciliação.

Para a medição fiscal e de custódia, essa classificação ajuda a decidir se o tratamento adequado é:

- apenas sinalizar e revisar;
- excluir da reconciliação;
- investigar instrumento/comunicação;
- tratar como desvio sistemático a ser corrigido por manutenção/calibração, e não apenas por ajuste de dado.

**Fontes:** `petroles-004c2afadba7ea17c7dd7908:pNone:2878195.0-2878236.0`, `regis-3e6f96fe13173e87e4b82393:pNone:11408.0-11697.0`

## 4. Validação de consistência técnica e metrológica

Após a triagem primária, a validação precisa verificar se os dados são **coerentes com o processo de medição e com a configuração do sistema**. O caso descrito na fonte menciona avaliação de múltiplas variáveis de processo, tais como:

- **pressão**;
- **temperatura**;
- **composição**;
- coerência das **configurações do flow computer**;
- consistência entre **tipo de processo de medição**, **tipo de produto** e **tabelas/métodos de cálculo aplicados**.

A lógica técnica é a seguinte: um valor pode estar dentro de um limite numérico aceitável e, ainda assim, ser inconsistente com:

- a natureza do fluido medido;
- o método de cálculo configurado no computador de vazão;
- a faixa operacional do sistema;
- o conjunto de propriedades laboratoriais usado para correções volumétricas/energéticas.

Em medição fiscal de óleo e gás e em offloading, essa camada é crucial porque o resultado final depende não só do sinal bruto de vazão, mas também da combinação correta entre:

- variáveis de processo;
- propriedades do fluido;
- configurações do medidor/computador de vazão;
- algoritmos/tabelas de cálculo volumétrico aplicáveis.

A fonte associa esse tipo de checagem às diretrizes de API/AGA/ASTM e à verificação de que o cálculo volumétrico foi executado corretamente segundo esses referenciais. Mesmo assim, para uso no contexto brasileiro, isso deve ser entendido como **referência técnica de boas práticas**, não como substituto direto de exigências regulatórias da ANP.

**Fontes:** `petroles-004c2afadba7ea17c7dd7908:pNone:534469.0-534503.0`

## 5. Tratamento de dados suspeitos e correções controladas

Um aspecto central do tratamento e validação é a diferença entre:

- **dado original recebido de campo**;
- **dado sinalizado como suspeito/errôneo**;
- **dado corrigido/justificado**.

A fonte descreve um fluxo em que os valores suspeitos são **marcados automaticamente**, e o especialista em medição passa a focar sua análise apenas nesses casos. Quando uma correção é necessária, o sistema deve manter:

- **controle estrito de mudanças**;
- registro de **quem** alterou;
- registro de **quando** alterou;
- registro de **por que** alterou;
- preservação do **dado original**.

Esse princípio é particularmente importante para medições fiscais e de custódia, nas quais uma correção sem trilha de auditoria pode comprometer:

- a rastreabilidade metrológica do processo informacional;
- a confiança da contraparte comercial;
- auditorias internas e externas;
- apuração de divergências entre balanços, volumes medidos e volumes contabilizados.

Em outras palavras, a correção pode ser tecnicamente necessária, mas ela só é aceitável em ambiente profissional quando permanece **integralmente auditável**.

**Fontes:** `petroles-004c2afadba7ea17c7dd7908:pNone:534469.0-534503.0`

## 6. Reconciliação de dados e balanços como ferramenta de consistência

### 6.1. Papel da reconciliação

Os trechos citam ferramentas automáticas para executar **balanços volumétricos, mássicos e energéticos** e também procedimentos de **reconciliação de dados**, inclusive em regime dinâmico. No contexto desta faceta, a reconciliação deve ser entendida como uma **camada de consistência** para avaliar se o conjunto de dados medidos representa adequadamente o estado operacional.

Isso é útil para distinguir, por exemplo:

- desvio explicável por problema de medição;
- inconsistência ligada a erro grosseiro;
- diferença associada a inventário/transiente;
- indício de volume não contabilizado ou perda.

A fonte do sistema SMADA destaca exatamente esse ganho: com os dados validados, torna-se mais fácil identificar se um desvio de balanço decorre de um problema específico de medição ou de volume não contabilizado/perdido.

### 6.2. Etapas típicas da reconciliação

Com base nos trechos, uma sequência coerente é:

1. adquirir dados da planta;
2. validar comunicação e qualidade dos sinais;
3. classificar dados em bons, questionáveis ou falhos;
4. retirar da reconciliação os dados falhos;
5. aplicar balanços/restrições do processo;
6. ajustar os dados dentro de critérios estatísticos e físicos;
7. reavaliar a coerência do conjunto reconciliado;
8. disponibilizar somente os resultados validados para sistemas corporativos.

### 6.3. Formulação estatística citada nas fontes

Uma das fontes descreve reconciliação dinâmica e não linear usando função objetivo de **máxima verossimilhança**. Outra apresenta uma função objetivo de modo DataRec, com estrutura ponderada por desvios das medições e por parâmetros de sintonia. Devido ao estado do texto extraído, a expressão aparece com lacunas, mas a forma geral pode ser representada como:

\[
\text{ObjFct}_{dr} \approx \sum_m \left(w_m \cdot \frac{Offset_m}{StdDev_m}\right) + \sum_{tp} \left(w_{tp} \cdot \frac{Offset_{tp}}{Scaling_{tp}}\right)
\]

onde, conceitualmente:

- \(Offset_m\): desvio entre valor do modelo e valor medido filtrado/selecionado;
- \(StdDev_m\): desvio-padrão associado à medição;
- \(w_m\): peso da medição na função objetivo;
- \(Offset_{tp}\): variação aplicada ao parâmetro de sintonia;
- \(Scaling_{tp}\): fator de escala/penalização do parâmetro de sintonia;
- \(w_{tp}\): peso do parâmetro de sintonia.

A interpretação prática é que medições com menor desvio-padrão tendem a ter maior influência relativa no ajuste, e grandes movimentos em parâmetros de sintonia podem ser penalizados. Em aplicações fiscais/custódia, essa lógica é útil para priorizar dados mais confiáveis na avaliação de consistência, sem apagar a distinção entre medição observada e valor ajustado pelo modelo.

### 6.4. Uso de janelas móveis e tempo real

Uma dissertação aplicada a tratamento de gás combustível em unidade offshore cita a implementação de **janelas móveis** para tornar viável a reconciliação em tempo real. O ponto transferível para esta faceta é que, em ambientes com grande volume de dados e necessidade de resposta operacional rápida, o tratamento de dados pode ser organizado por blocos temporais sucessivos, desde que:

- a qualidade dos dados seja previamente triada;
- as restrições físicas do sistema sejam preservadas;
- se entenda que a reconciliação é uma ferramenta de suporte à consistência, não um substituto da medição primária.

### 6.5. Limitações práticas

As fontes também apontam limitações importantes:

- o tempo de reconciliação cresce com o número de variáveis;
- o modo de acesso ao modelo influencia fortemente o desempenho;
- processos reais possuem **malhas de controle** cuja dinâmica pode afetar a estabilidade do procedimento de reconciliação;
- perturbações excessivas no modelo podem instabilizar a solução.

Portanto, ao aplicar reconciliação para conferir consistência de dados fiscais ou de custódia, é preciso evitar usar um modelo dinâmico complexo como se fosse uma “caixa-preta infalível”. A modelagem e a escolha das variáveis reconciliadas precisam ser compatíveis com a finalidade da análise.

**Fontes:** `petroles-004c2afadba7ea17c7dd7908:pNone:534469.0-534503.0`, `petroles-004c2afadba7ea17c7dd7908:pNone:2878195.0-2878236.0`, `petroles-004c2afadba7ea17c7dd7908:pNone:4134221.60-4134341.0`, `petroles-004c2afadba7ea17c7dd7908:pNone:4135317.0-4135377.0`, `petroles-004c2afadba7ea17c7dd7908:pNone:535393.0-535447.0`, `regis-3e6f96fe13173e87e4b82393:pNone:11408.0-11697.0`

## 7. Inventários, transientes e consistência em transferência de custódia/offloading

Os trechos sobre reconciliação de inventários mostram que, em sistemas com entradas, saídas e condições variáveis no tempo, a análise de consistência pode precisar considerar:

- **eventos transientes**;
- variações de **vazão, pressão e temperatura**;
- fechamento de **balanço material** ao longo de segmentos da rede.

Embora o texto-fonte trate explicitamente de redes de dutos, o conceito é tecnicamente relevante para transferências de custódia por offloading quando a operação envolve linhas/segmentos com inventário variável e comportamento transiente. Nesses casos, a consistência entre volume transferido, volume em linha, medições de processo e balanço global pode ser melhor avaliada se a rotina de validação incorporar raciocínio de inventário e não apenas leitura instantânea de vazão.

O uso profissional desse conceito, no contexto de offloading, não significa impor um método único; significa reconhecer que divergências de transferência podem decorrer de:

- dado inválido de medição;
- erro de propriedade/correção;
- falha de sincronismo dos dados;
- transiente operacional;
- variação de inventário do sistema.

Em ambiente corporativo, isso é útil para diferenciar **erro de medição** de **efeito operacional legítimo**.

**Fontes:** `petroles-004c2afadba7ea17c7dd7908:pNone:4160062.0-4160102.0`

## 8. Integração com aplicações corporativas e governança do dado validado

Depois de tratado e validado, o dado deve ser transferido a aplicações corporativas como:

- faturamento;
- alocação;
- balanços físicos e energéticos;
- monitoramento operacional;
- ERP e sistemas correlatos.

Os trechos destacam que uma plataforma confiável deve ser:

- **robusta**;
- **segura**;
- **auditável**;
- **padronizada**.

Também é indicada a utilização de interfaces de integração, inclusive por web services, para compartilhar os dados já validados com sistemas terceiros. Em medição fiscal e custódia, a implicação relevante é que o dado corporativo não deveria ser uma cópia não controlada do campo, mas o **resultado de um fluxo formal de aquisição, validação, correção rastreável e liberação**.

Outro ponto mencionado é a gestão de **KPIs** associados aos sistemas volumétricos de transferência de custódia. Para esta faceta, isso se relaciona diretamente ao acompanhamento de desempenho do processo de medição, por exemplo:

- quantidade de dados suspeitos por período;
- reincidência de falhas por instrumento/sistema;
- tempos de tratamento e liberação;
- frequência de correções manuais;
- impacto de desvios sobre balanços e contabilização.

**Fontes:** `petroles-004c2afadba7ea17c7dd7908:pNone:534469.0-534503.0`

## 9. Critérios práticos de decisão para tratamento e validação

Com base nos trechos, um fluxo decisório coerente para dados de medição fiscal e de custódia pode ser resumido assim:

### 9.1. Dado com falha evidente

Exemplos: perda de comunicação, congelamento, violação impossível de limite, pico irreal, falha de instrumento.

**Tratamento indicado pela lógica das fontes:**

- classificar como falho;
- não usar esse valor em reconciliação como se fosse confiável;
- investigar causa instrumental, de comunicação ou de aquisição;
- manter registro da ocorrência.

### 9.2. Dado suspeito, mas fisicamente plausível

Exemplos: valor destoante de tendência, inconsistência com composição, temperatura ou configuração de cálculo.

**Tratamento indicado:**

- marcar como suspeito;
- direcionar à revisão do especialista;
- confrontar com redundâncias, balanços e coerência do flow computer;
- corrigir somente sob controle de mudança e mantendo o original.

### 9.3. Dado sem anomalia primária, mas inconsistente no conjunto

Exemplos: leitura individual plausível, porém incompatível com balanço volumétrico/mássico/energético.

**Tratamento indicado:**

- aplicar reconciliação/balanço para investigar consistência do conjunto;
- avaliar possibilidade de erro sistemático, propriedade incorreta ou inventário/transiente;
- evitar concluir imediatamente por perda ou volume não contabilizado sem análise adicional.

### 9.4. Dado validado e representativo

Quando a triagem, a coerência metrológica e a verificação de consistência forem satisfatórias, o dado pode ser liberado para uso corporativo em alocação, billing e contabilização.

**Fontes:** `petroles-004c2afadba7ea17c7dd7908:pNone:534469.0-534503.0`, `petroles-004c2afadba7ea17c7dd7908:pNone:2878195.0-2878236.0`, `regis-3e6f96fe13173e87e4b82393:pNone:11408.0-11697.0`, `petroles-004c2afadba7ea17c7dd7908:pNone:4160062.0-4160102.0`

## 10. Síntese aplicada à faceta

Para fins de avaliação profissional sobre **tratamento, validação e consistência dos dados** em medição fiscal de óleo, medição fiscal de gás e transferência de custódia em offloading de FPSOs, os pontos mais sólidos extraídos do material são:

1. a validação começa na **aquisição segura e rastreável da fonte primária**;
2. a triagem deve detectar **falha de comunicação, congelamento, falha instrumental, limites inválidos e picos irreais**;
3. os dados precisam ser classificados por qualidade e os **falhos não devem alimentar reconciliação como se fossem confiáveis**;
4. a consistência exige verificar não só valores, mas também **pressão, temperatura, composição, configuração do flow computer e método/tabela de cálculo**;
5. correções de dados só são aceitáveis com **trilha de auditoria completa** e preservação do dado original;
6. **balanços e reconciliação de dados** são ferramentas valiosas para análise de consistência e para distinguir problema de medição de volume não contabilizado/perdas;
7. em operações sujeitas a transientes, a análise de **inventário** pode ser necessária para interpretar diferenças de transferência;
8. somente após esse fluxo o dado deve ser liberado para **faturamento, alocação e demais aplicações corporativas**.

**Fontes:** `petroles-004c2afadba7ea17c7dd7908:pNone:534469.0-534503.0`, `petroles-004c2afadba7ea17c7dd7908:pNone:2878195.0-2878236.0`, `regis-3e6f96fe13173e87e4b82393:pNone:11408.0-11697.0`, `petroles-004c2afadba7ea17c7dd7908:pNone:4160062.0-4160102.0`, `petroles-004c2afadba7ea17c7dd7908:pNone:4134221.60-4134341.0`, `petroles-004c2afadba7ea17c7dd7908:pNone:4135317.0-4135377.0`, `petroles-004c2afadba7ea17c7dd7908:pNone:535393.0-535447.0`