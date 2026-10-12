# Preditiva e condição: uso do monitoramento de condição para antecipar falhas e definir intervenções

## 1. Enquadramento da manutenção preditiva na gestão da manutenção

A manutenção preditiva, também chamada de **manutenção baseada na condição**, **baseada no estado** ou **manutenção condicional**, é descrita nas fontes como a prática de acompanhar periodicamente ou continuamente parâmetros significativos do equipamento para intervir **somente quando houver necessidade**, com foco na detecção precoce de sintomas que precedem uma avaria.

Nesse enquadramento:

- **Manutenção corretiva** atua após a falha, reparando o dano já ocorrido.
- **Manutenção preventiva sistemática** atua por tempo/intervalo predefinido.
- **Manutenção preditiva** usa medições, tendências e diagnóstico de condição para decidir o momento da intervenção.

O benefício central é evitar tanto a **quebra inesperada** quanto a **troca prematura** de componentes ainda com vida remanescente relevante. As fontes também destacam uma ideia operacional importante: intervir desnecessariamente pode introduzir defeitos; portanto, a manutenção baseada em condição busca “mexer na máquina o mínimo possível”, desde que a condição monitorada permaneça aceitável.

Na prática de gestão da manutenção, isso desloca a decisão de intervenção de um calendário fixo para uma lógica de **evidência de degradação**, desde que exista:

- parâmetro mensurável;
- método confiável de coleta e análise;
- histórico ou referência para comparação;
- pessoal qualificado;
- plano estruturado para transformar dados em decisão.

As fontes também apontam que a manutenção preditiva requer inspeções com instrumentos específicos e equipe capacitada, o que constitui uma de suas principais limitações de implementação.

**Fontes:** `regis-d80d8a09be0cb98c30c8ad85:pNone:788.0-990.0`, `petroles-4ee4bce16acf674505c8912d:pNone:992700.0-992733.0`

## 2. Relação com confiabilidade, disponibilidade, criticidade e seleção da política de manutenção

O material relaciona explicitamente a manutenção com os conceitos de **confiabilidade** e **disponibilidade**:

- **Confiabilidade**: possibilidade de um componente, equipamento ou sistema executar sua função, por um período especificado, sem falhar.
- **Disponibilidade**: depende da confiabilidade dos equipamentos e das políticas de manutenção adotadas; também tem implicação econômica direta, porque maior disponibilidade tende a significar maior capacidade de produção.

As fontes indicam que a escolha entre corretiva, preventiva e preditiva não deve ser genérica, mas orientada por criticidade e consequências. A sequência conceitual apresentada é:

1. Aplicar uma avaliação de confiabilidade, como **FMEA** (Análise de Modos e Efeitos de Falha), para identificar os modos de falha mais severos.
2. Avaliar as consequências desses modos de falha, inclusive **perda de produção**.
3. Selecionar a política de manutenção mais adequada para os componentes críticos, caracterizando a lógica de **RCM** (Manutenção Centrada em Confiabilidade).
4. Quando o modo de falha apresentar degradação detectável antes da perda funcional, a manutenção preditiva/monitoramento de condição torna-se candidata preferencial.

Portanto, para ativos de FPSO/FSO e produção subsea, o monitoramento de condição é mais justificável quando coexistem os seguintes fatores:

- alta consequência de falha para produção, segurança ou custo;
- janela detectável de degradação antes da falha funcional;
- parâmetro monitorável com repetibilidade;
- ação de manutenção viável após o diagnóstico.

Esse raciocínio é compatível com a priorização típica de equipamentos rotativos e sistemas auxiliares críticos, mas os valores de criticidade e os critérios de seleção da política dependem do ativo, do arranjo e do histórico local.

**Fontes:** `regis-d80d8a09be0cb98c30c8ad85:pNone:661.0-875.0`, `regis-d80d8a09be0cb98c30c8ad85:pNone:788.0-990.0`

## 3. Técnicas de monitoramento de condição destacadas nas fontes

As fontes listam, entre as técnicas de manutenção preditiva:

- análise de vibrações de equipamentos rotativos e alternativos;
- análise de corrente e fluxo magnético de motores elétricos;
- análise de óleo lubrificante;
- termografia de sistemas elétricos e mecânicos;
- ultrassom para vazamentos e defeitos de válvulas e purgadores.

Para esta faceta, o material oferecido aprofunda principalmente **análise de vibração** e **análise de óleo lubrificante**.

**Fontes:** `petroles-4ee4bce16acf674505c8912d:pNone:992700.0-992733.0`, `regis-d80d8a09be0cb98c30c8ad85:pNone:788.0-990.0`

## 4. Análise de vibração como ferramenta para antecipação de falhas

A análise de vibração é apresentada como uma das ferramentas mais precisas para prever falhas mecânicas prematuras em equipamentos rotativos, sem interromper sua operação, especialmente em equipamentos críticos.

### 4.1 Mecanismos de degradação percebidos por vibração

Segundo o material, equipamentos adequadamente projetados tendem a produzir baixo nível de vibração, mas, em operação, ficam sujeitos a fenômenos como:

- desgaste;
- fadiga;
- deformação;
- corrosão.

Esses fenômenos podem levar ao aparecimento de:

- folgas;
- desalinhamentos;
- trincas;
- desbalanceamentos.

O aumento dos níveis de vibração e/ou a alteração do conteúdo espectral passam, então, a ser indicativos de anormalidade mecânica ou operacional.

### 4.2 Onde o monitoramento contínuo é mais justificável

As fontes exemplificam equipamentos considerados críticos, como:

- turbinas;
- compressores de grande porte;
- hidrogeradores;
- motobombas e conjuntos de BCS/subsea em estudos de aplicação.

Nesses casos, o monitoramento contínuo de parâmetros pode antecipar condições anormais de operação, projeto ou manutenção, reduzindo o risco de intervenções tardias e de custos elevados de parada.

### 4.3 Parâmetros e abordagens analíticas mencionadas

O material cita, como abordagens de diagnóstico vibratório:

- construção de espectros por **Transformada de Fourier**;
- acompanhamento de valores **RMS**;
- técnica do **envelope** para identificação de falhas em mancais de rolamento.

Também é citado o uso de sinais de vibração em compressores para antever condições operacionais destrutivas, como **surge**.

### 4.4 Implicações para decisão de intervenção

Com base nas fontes, o monitoramento vibratório permite:

- detectar anormalidades antes da falha funcional;
- diferenciar tipos prováveis de problema mecânico/operacional;
- definir o momento mais apropriado para intervenção planejada;
- elevar a confiabilidade de sistemas críticos.

Em termos de plano de manutenção, isso sustenta uma lógica de decisão por tendência:

- condição estável -> manter acompanhamento;
- tendência de degradação -> intensificar monitoramento e preparar intervenção;
- assinatura compatível com modo de falha relevante -> programar a intervenção antes da perda funcional.

As fontes não fornecem limites numéricos universais de alarme para vibração; portanto, a definição de gatilhos deve ser feita com referência a OEM, baseline do ativo e histórico operacional.

**Fontes:** `petroles-004c2afadba7ea17c7dd7908:pNone:3793022.60-3793051.0`

## 5. Análise de óleo lubrificante como ferramenta de monitoramento de condição

A análise de óleo é descrita como técnica importante de manutenção preditiva para detectar sintomas iniciais de desgaste e avaliar a condição do próprio lubrificante, sem necessidade de desmontagem ou inspeção visual interna do equipamento.

### 5.1 O que a análise de óleo procura revelar

As fontes indicam que a identificação da condição pode envolver o estudo de:

- quantidade de partículas;
- tamanho das partículas;
- forma das partículas;
- composição das partículas;
- viscosidade;
- **TBN** (Número Total de Basicidade);
- **TAN** (Número Total de Acidez);
- índice de partículas magnéticas.

Em termos de função diagnóstica, a análise de óleo atende a dois objetivos simultâneos:

1. **Avaliar desgaste interno do equipamento**.
2. **Avaliar degradação/contaminação do lubrificante**.

As fontes enfatizam que um lubrificante correto não dispensa o monitoramento, pois podem ocorrer contaminações e alterações físico-químicas com consequências para desgaste e desempenho.

### 5.2 Quando a contagem de partículas é especialmente útil

Um dos trechos informa que a **contagem de partículas** é amplamente usada em sistemas hidráulicos e é particularmente apropriada quando:

- os mecanismos de fadiga são precursores relevantes da falha; ou
- partículas contaminantes causam abrasão.

O mesmo trecho indica que existem níveis de limpeza recomendados publicados por diferentes indústrias, inclusive classificações ISO/NAS, mas os valores numéricos do excerto recebido estão incompletos por placeholders e, por isso, não devem ser reproduzidos como critério técnico fechado neste documento.

### 5.3 Importância da contaminação particulada

As fontes associam a contaminação por partículas metálicas no sistema de óleo a parcela significativa das falhas em turbinas a gás, reforçando que a gestão da limpeza do óleo e a análise de partículas podem ter impacto direto sobre confiabilidade e disponibilidade.

### 5.4 Decisão de manutenção baseada em análise de óleo

O material deixa claro que a análise do óleo faz parte de um processo decisório maior. Os resultados são comparados com referências e tendências para apoiar decisões como:

- manter o equipamento em serviço com continuidade do acompanhamento;
- definir a necessidade real de intervenção;
- substituir o óleo;
- avaliar uso de aditivos para recuperar condição do lubrificante, quando tecnicamente aplicável segundo referência do sistema/fabricante.

Além disso, a análise pode ajudar a identificar **problemas crônicos** e orientar correções que aumentem a disponibilidade e reduzam custos.

**Fontes:** `petroles-4ee4bce16acf674505c8912d:pNone:992700.0-992733.0`, `petroles-4ee4bce16acf674505c8912d:pNone:992661.0-992699.0`, `regis-d80d8a09be0cb98c30c8ad85:pNone:661.0-875.0`

## 6. Planejamento do programa de monitoramento de condição

As fontes ressaltam que a análise de condição não é apenas execução de teste; ela começa no **planejamento da manutenção preditiva**. Devem ser definidos, previamente:

- quais equipamentos serão monitorados;
- qual técnica será aplicada a cada equipamento;
- qual a periodicidade das análises;
- qual o procedimento de execução/coleta;
- como os resultados serão analisados e convertidos em decisão.

Isso é particularmente importante porque a qualidade da decisão depende da qualidade do dado. O material ainda observa que:

- vibração, termografia e boroscopia são frequentemente executadas por terceiros especializados;
- na análise de óleo, é comum a coleta ser feita por pessoal próprio e o ensaio laboratorial por laboratório externo;
- nessas situações, a coleta deve ser executada por pessoas capacitadas e com procedimento padronizado.

Também é enfatizado que programas de manutenção eficazes devem considerar recomendações do fabricante, tipos de inspeção e fatores que afetam a vida dos componentes, embora os detalhes específicos dependam do ativo analisado.

Para fins de plano de manutenção, isso implica que o monitoramento de condição precisa ser tratado como processo disciplinado, com:

- padronização de coleta/medição;
- consistência de laboratório/método quando se trabalha por tendência;
- critérios documentados de comparação com baseline e limites.

**Fontes:** `regis-d80d8a09be0cb98c30c8ad85:pNone:4499.0-4726.0`, `regis-d80d8a09be0cb98c30c8ad85:pNone:788.0-990.0`

## 7. Periodicidade, tendência e critérios de intervenção

As fontes não trazem uma fórmula universal para definir periodicidade. Em vez disso, indicam que a periodicidade deve ser escolhida no planejamento do programa, considerando a técnica adotada, o equipamento e o objetivo do monitoramento.

A lógica técnica implícita nos trechos é:

1. **Estabelecer referência inicial** do equipamento/fluido em condição saudável.
2. **Coletar séries históricas consistentes**.
3. **Analisar tendência**, não apenas resultado isolado.
4. **Comparar com limites aceitáveis** quando existirem.
5. **Definir intervenção** quando a condição real justificar.

Essa abordagem é coerente com a promessa da manutenção preditiva de determinar um “ponto ótimo” para a manutenção preventiva, reduzindo trocas prematuras e falhas em serviço.

### 7.1 Exemplo de limites citados para óleo de turbina a gás em serviço

Um trecho fornece um exemplo de limites aceitáveis para óleo lubrificante em serviço, comparados ao óleo novo, em aplicação de turbina a gás. Os limites citados incluem:

- **Água:** máximo de 2.000 ppm;
- **Viscosidade:** variação de **+20% ou -10%**;
- **TAN:** aumento de **0,4 mgKOH/g** para todos os tipos de óleo, ou limites máximos por classe de óleo indicados no texto de origem;
- **Formação de espuma:** sequência I e II 300/10;
- **Liberação de ar a 50°C:** máximo de 10 minutos;
- **RBOT:** 25% do valor original do óleo novo.

Esses valores devem ser entendidos como **exemplo contextualizado** da fonte, voltado a óleo de turbina e às normas/referências adotadas naquele estudo, e não como regra geral para todos os equipamentos de FPSO/FSO.

### 7.2 Tendência versus valor absoluto

O material valoriza o uso de tendência. Um dado isolado fora de tendência, ou obtido por método de coleta inconsistente, pode induzir decisão ruim. Por isso, além do limite, importa observar:

- velocidade de degradação;
- repetibilidade da medição;
- coerência com a condição operacional;
- correlação com outros sinais de condição, como vibração ou temperatura.

**Fontes:** `regis-d80d8a09be0cb98c30c8ad85:pNone:4499.0-4726.0`, `regis-d80d8a09be0cb98c30c8ad85:pNone:788.0-990.0`

## 8. Qualidade da amostragem e confiabilidade diagnóstica

Para que a análise de óleo realmente antecipe falhas, o procedimento de coleta é decisivo. As fontes destacam que a amostra deve ser representativa e que o planejamento da coleta deve ser criterioso.

Pontos técnicos explicitados no material:

- as amostras devem ser tomadas **com a turbina em operação**;
- o óleo deve estar em **temperatura de trabalho**;
- isso ajuda a assegurar **distribuição uniforme das partículas** no óleo;
- os procedimentos de coleta têm grande influência, especialmente para **contagem de partículas**;
- usar **método de amostragem consistente** e **laboratório confiável** é importante para estabelecer tendências válidas;
- manter o mesmo laboratório reduz variações de técnica de amostragem e medição que poderiam distorcer a interpretação.

Para a definição de intervenção, isso tem consequência direta: um bom plano de monitoramento não trata a medição como evento isolado, mas como parte de uma cadeia metrológica que precisa ser consistente para que a tendência seja confiável.

**Fontes:** `regis-d80d8a09be0cb98c30c8ad85:pNone:4499.0-4726.0`

## 9. Como converter monitoramento de condição em decisão de manutenção

Com base no conjunto das fontes, o uso profissional do monitoramento de condição para antecipar falhas e definir intervenções pode ser estruturado na sequência abaixo:

### 9.1 Selecionar o ativo e o modo de falha relevante

Usar criticidade, consequências e análise de modos de falha para selecionar componentes em que a degradação seja detectável e a falha tenha consequência significativa.

### 9.2 Escolher a técnica compatível com o mecanismo de falha

- **Vibração**: mais aderente a folga, desalinhamento, desbalanceamento, trinca, falhas em mancais e anormalidades dinâmicas/operacionais.
- **Óleo**: mais aderente a desgaste interno, contaminação, degradação do lubrificante e limpeza do sistema.
- As demais técnicas listadas no material podem complementar o diagnóstico quando aplicáveis.

### 9.3 Definir baseline, periodicidade e procedimento

Sem baseline e sem procedimento repetível, a tendência perde valor. Isso inclui padronização de coleta, condição operacional da medição e rastreabilidade da amostra.

### 9.4 Avaliar tendência e severidade

A decisão não deve se basear apenas na presença de anomalia, mas em:

- quão rápido a condição está piorando;
- quão crítico é o ativo;
- qual a consequência da falha;
- se há janela segura para planejar a intervenção.

### 9.5 Programar a intervenção no ponto mais vantajoso

O objetivo da manutenção baseada na condição é intervir **antes da falha funcional**, mas **sem antecipação excessiva**. As fontes associam isso a:

- aumento de disponibilidade;
- redução de custo de manutenção;
- aumento de vida útil dos componentes;
- menor troca prematura;
- menor risco de parada inesperada.

Esse raciocínio é diretamente aplicável a ativos críticos de produção offshore, sobretudo rotativos e sistemas lubrificados/hidráulicos, desde que os limites e procedimentos sejam específicos do equipamento e da instalação.

**Fontes:** `regis-d80d8a09be0cb98c30c8ad85:pNone:661.0-875.0`, `regis-d80d8a09be0cb98c30c8ad85:pNone:788.0-990.0`, `regis-d80d8a09be0cb98c30c8ad85:pNone:4499.0-4726.0`, `petroles-004c2afadba7ea17c7dd7908:pNone:3793022.60-3793051.0`, `petroles-4ee4bce16acf674505c8912d:pNone:992700.0-992733.0`

## 10. Síntese aplicada à faceta “Preditiva e condição”

O material recebido sustenta as seguintes conclusões técnicas para avaliação profissional do tema:

- monitoramento de condição é uma estratégia de manutenção para **antecipar falhas** por evidência de degradação;
- sua aplicação deve ser orientada por **criticidade, confiabilidade e consequências**;
- **FMEA** ajuda a identificar modos de falha relevantes e **RCM** ajuda a selecionar a política de manutenção adequada;
- **análise de vibração** e **análise de óleo** são ferramentas centrais para ativos rotativos/lubrificados;
- a qualidade do diagnóstico depende fortemente de **procedimento, repetibilidade, amostragem e tendência histórica**;
- a decisão de intervir deve buscar o equilíbrio entre **não falhar em serviço** e **não intervir cedo demais**.

**Fontes:** `regis-d80d8a09be0cb98c30c8ad85:pNone:661.0-875.0`, `regis-d80d8a09be0cb98c30c8ad85:pNone:788.0-990.0`, `regis-d80d8a09be0cb98c30c8ad85:pNone:4499.0-4726.0`, `petroles-004c2afadba7ea17c7dd7908:pNone:3793022.60-3793051.0`, `petroles-4ee4bce16acf674505c8912d:pNone:992700.0-992733.0`, `petroles-4ee4bce16acf674505c8912d:pNone:992661.0-992699.0`