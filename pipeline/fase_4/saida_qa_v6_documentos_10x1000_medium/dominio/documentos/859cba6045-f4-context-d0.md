# TOG e monitoramento analítico no descarte de água produzida

## 1. Finalidade do monitoramento de TOG no descarte offshore
O **TOG (teor de óleos e graxas)** é um dos parâmetros centrais para controle da qualidade da água produzida destinada ao descarte no mar. Nas fontes fornecidas, a água produzida é descrita como mistura de água de formação e água de injeção, podendo conter óleo, sais, compostos químicos, sólidos e metais. Em operação, sua qualidade é normalmente acompanhada pela concentração de óleo e graxas em **ppm**, equivalente a **mg/L** no contexto apresentado.

Do ponto de vista operacional, o monitoramento de TOG atende a dois objetivos complementares:

1. **Comprovar e sustentar o controle do descarte** por métodos laboratoriais reconhecidos.
2. **Dar resposta rápida ao processo** por meio de monitores em linha, permitindo correção operacional antes que a qualidade do efluente se deteriore de forma persistente.

As fontes destacam como principais motivações para adoção de monitoramento em linha:
- resposta em tempo real;
- redução do custo de análises laboratoriais rotineiras;
- formação de banco de dados para controle, modificação e projeto de plantas;
- monitoração mais efetiva da água descartada.

Na prática, isso significa que a medição analítica de TOG não é apenas uma atividade de laboratório: ela integra a malha de decisão operacional do tratamento de água produzida.

**Fontes:** `regis-b461ca66d401c4840d2c46cc:pNone:10.0-37.0`

## 2. Papel relativo de métodos laboratoriais e analisadores em linha
As fontes diferenciam claramente os **métodos laboratoriais de referência** dos **analisadores em linha**.

### 2.1 Métodos laboratoriais citados
São citados como aceitos pelos órgãos ambientais, no material fornecido:
- **método gravimétrico** (USEPA 1664);
- **espectrofotometria de infravermelho** (ASTM 3921 e Standard Methods 5520C ou 5520F, conforme texto-fonte).

O método gravimétrico, segundo o trecho, envolve:
1. extração com **hexano**;
2. evaporação do solvente;
3. pesagem do resíduo oleoso.

A medição por IR citada no texto-base envolve:
1. extração dos óleos e graxas da amostra com solvente organoalogenado;
2. leitura por espectrofotometria de infravermelho.

### 2.2 Monitores em linha
Os monitores em linha aparecem nas fontes como instrumentos voltados a **controle contínuo** e **tempo real**, com tecnologias distintas e incertezas dependentes da qualidade da água, da presença de gás e sólidos e da natureza do óleo processado. Eles são especialmente úteis para acompanhar a variação operacional do sistema de tratamento, mas exigem:
- seleção adequada da tecnologia;
- condicionamento de amostra;
- calibração com correlação a método laboratorial;
- manutenção e limpeza.

Assim, um entendimento técnico consistente é:
- **o laboratório ancora a referência analítica e a rastreabilidade**;
- **o analisador em linha apoia o controle operacional contínuo**.

**Fontes:** `regis-b461ca66d401c4840d2c46cc:pNone:10.0-37.0`

## 3. Critérios de seleção de tecnologia de medição de TOG
Antes de definir a tecnologia de monitoramento em linha, as fontes recomendam caracterizar o óleo e a água oleosa da unidade. Os critérios explicitamente citados incluem:

- **faixa de concentração (range)** a ser medida, em ppm;
- **compatibilidade da técnica** com o tipo de óleo;
- **procedimento de pré-condicionamento da amostra**;
- **periodicidade de limpeza** do sistema de medição;
- **simplicidade e robustez** para operação em ambiente severo, inclusive com corrosividade e risco de explosividade.

As fontes também apontam tendências importantes:
- medidores que utilizam **extração** antes da remoção de sólidos tendem a apresentar **menores incertezas**;
- medidores por **espalhamento de luz** têm uso relevante em certas aplicações, mas a resposta depende fortemente das características físicas da dispersão;
- sistemas em que a amostra **não entra em contato com a célula óptica** tendem a ser menos suscetíveis a falhas por incrustação e sujeira.

Em FPSO/FSO, esses critérios têm impacto direto sobre a confiabilidade do controle do descarte, porque a medição de TOG é sensível às mesmas perturbações que afetam o próprio tratamento: gás livre, sólidos finos, variação de blend de óleo, formação de incrustação e alteração do tamanho de gota.

**Fontes:** `regis-b461ca66d401c4840d2c46cc:pNone:10.0-37.0`

## 4. Tecnologias analíticas relevantes para monitoramento de TOG

### 4.1 Espalhamento IR e IR/laser/visível
Nessa família de medidores, um feixe de luz é direcionado para a amostra em uma célula óptica. O espalhamento e a atenuação do feixe são correlacionados à concentração de substâncias suspensas. Nos analisadores descritos, sensores em torno da célula medem radiação espalhada, refletida e transmitida.

Pontos técnicos relevantes das fontes:
- a **intensidade de luz espalhada** é usada como indicativo da concentração de óleo;
- a fração **refletida** pode representar contribuição de **sólidos**;
- a amostra costuma passar por um **condicionador**, no qual o óleo é disperso em pequenas gotas por agitação ou passagem por orifício e placa defletora;
- a resposta depende da população de gotículas e, portanto, do **tamanho de gota** e da estabilidade da dispersão.

Implicação operacional: esses medidores podem responder bem, mas dependem fortemente da qualidade do condicionamento da amostra e sofrem interferência quando a composição sólida ou a hidrodinâmica da amostra mudam.

**Fontes:** `regis-b461ca66d401c4840d2c46cc:pNone:10.0-37.0`, `regis-b461ca66d401c4840d2c46cc:pNone:46.60-76.0`

### 4.2 Espectrofotometria de infravermelho (IR)
As fontes descrevem dois raciocínios de IR:

1. **Medição por absorção em comprimentos de onda característicos**, baseada na diferença entre os coeficientes de absorção da água e do óleo em torno de **3,4 µm**, com compensação em **3,6 µm** para perturbações por sólidos ou ar.
2. **Pré-extração com solvente**, seguida de leitura do extrato por IR, medindo absorvância associada às vibrações dos grupos **CH3, CH2 e CH**.

Aspectos operacionais importantes:
- a célula óptica pode exigir **caminho óptico estreito**, o que a torna suscetível a incrustação;
- pode ser necessário **sistema de lavagem automática**;
- a amostra pode precisar de bomba/condicionador para uniformizar sólidos e distribuição de gota;
- em um teste citado, o analisador por IR com pré-extração exigia **temperatura da amostra inferior a 30 °C**;
- a técnica com extração é apresentada como tendo vantagem importante: **menor dependência da origem da amostra**, sendo mais adequada quando o **blend de óleo varia com frequência**.

Em compensação, as fontes registram maior complexidade operacional, maior custo e consumo de solvente halogenado no equipamento testado.

**Fontes:** `regis-b461ca66d401c4840d2c46cc:pNone:10.0-37.0`, `regis-b461ca66d401c4840d2c46cc:pNone:38.60-54.0`, `regis-b461ca66d401c4840d2c46cc:pNone:79.60-103.0`

### 4.3 Fluorescência no ultravioleta (UVF)
Na fluorescência UV, a radiação ultravioleta incide sobre a amostra e os **hidrocarbonetos aromáticos** emitem fluorescência na faixa visível. A intensidade dessa fluorescência é usada como variável de leitura.

Condição crítica desta tecnologia: a leitura só pode ser correlacionada com o óleo total de forma confiável quando a relação entre aromáticos e alifáticos se mantém suficientemente estável. As próprias fontes enfatizam que o método é **específico para determinado tipo de óleo** e pode não ser sensível a óleos com baixo teor de aromáticos.

Pontos técnicos das fontes:
- boa sensibilidade para baixas concentrações;
- pode usar compensação para turbidez com luz visível;
- exige atenção ao **tamanho de gota**, pois a emissão detectável está associada à interface irradiada;
- pode incluir subsistemas de **lavagem automática** ou arranjos em que a amostra não toca diretamente o sistema óptico;
- requer **recalibração** quando houver mudança relevante do blend de óleo processado.

Para controle do descarte, a UVF é atrativa quando o campo, o tratamento e o tipo de óleo são relativamente estáveis e quando se busca simplicidade operacional.

**Fontes:** `regis-b461ca66d401c4840d2c46cc:pNone:38.60-54.0`, `regis-b461ca66d401c4840d2c46cc:pNone:46.60-76.0`, `regis-b461ca66d401c4840d2c46cc:pNone:79.60-103.0`

### 4.4 UV absorção e ultra-som
As fontes também descrevem, de forma comparativa:

- **UV absorção**: mede absorção de luz UV (na faixa citada de 254 nm) pelos aromáticos; depende da constância da fração aromática e usa arranjos ópticos para compensar incrustação/turbidez.
- **Ultra-som**: mede material disperso a partir de reflexos acústicos. Tem resposta rápida e pode usar sensor inserido diretamente na linha, reduzindo problemas de representatividade e perdas na linha de amostragem. Porém, tende a **superestimar** o óleo na presença de **gás** e **sólidos**, o que é particularmente crítico em água produzida offshore.

Essas duas tecnologias mostram uma lição geral importante: quanto mais a variável medida depende do comportamento físico da dispersão, maior a necessidade de **pré-tratamento da amostra** para remover gás livre, reduzir sólidos e estabilizar a distribuição de gotas.

**Fontes:** `regis-b461ca66d401c4840d2c46cc:pNone:38.60-54.0`, `regis-b461ca66d401c4840d2c46cc:pNone:46.60-76.0`

## 5. Amostragem e condicionamento da amostra
A confiabilidade do TOG medido depende fortemente da **representatividade** e do **condicionamento** da amostra.

### 5.1 Fatores que degradam a medição
As fontes apontam como principais interferentes:
- **gás livre**;
- **sólidos suspensos**;
- **turbidez**;
- **incrustação** e sujeira da célula de medição;
- variação da **distribuição de tamanho de gotas de óleo**;
- mudanças no **blend** de óleo processado.

Esses fatores podem alterar tanto a resposta analítica quanto a estabilidade operacional do instrumento.

### 5.2 Condicionamento da amostra em linha
O material fornecido descreve diferentes práticas de condicionamento, conforme a tecnologia:
- remoção de gás por **bubble trap** ou separador de bolhas a montante do analisador;
- uso de bombas, orifícios e placas defletoras para homogeneização e controle da dispersão;
- lavagem automática da célula para reduzir incrustação;
- compensações ópticas para sólidos/turbidez;
- pré-tratamento para remover gás livre e sólidos antes de análise ultrassônica.

Em termos de engenharia de medição, isso significa que o sistema analítico é composto por mais do que o sensor: **linha de amostragem, removedor de gás, condicionador, célula, sistema de limpeza e rotina de calibração** são partes do mesmo desempenho metrológico.

### 5.3 Conservação de amostras para análise laboratorial
Em um estudo acadêmico incluído no material, as amostras para análise de TOG foram conservadas segundo referência APHA, com:
- **acidificação com ácido sulfúrico** até **pH próximo de 2**;
- **refrigeração** até a análise.

Isso é tecnicamente coerente como prática de preservação quando a análise não é imediata, pois busca minimizar alterações da amostra durante transporte/armazenamento. Para o ambiente offshore, a utilidade prática dessa informação é lembrar que a qualidade do dado laboratorial depende não só do método analítico, mas também da forma de coleta, acondicionamento e tempo até a análise.

**Fontes:** `regis-b461ca66d401c4840d2c46cc:pNone:10.0-37.0`, `regis-b461ca66d401c4840d2c46cc:pNone:38.60-54.0`, `regis-b461ca66d401c4840d2c46cc:pNone:46.60-76.0`, `petroles-4ee4bce16acf674505c8912d:pNone:371473.0-371537.0`

## 6. Calibração, correlação com laboratório e interpretação da leitura
Os monitores em linha descritos nas fontes não devem ser tratados como instrumentos universais e autossuficientes. Sua confiabilidade depende de correlação com análises laboratoriais aceitas.

### 6.1 Exemplo de correlação por UVF
Em teste de campo na P-08, após ajuste do condicionamento de amostra, a relação inicial entre a leitura do monitor de fluorescência UV e a concentração de óleo e graxa foi expressa por:

\[
Y = aX + b
\]

onde:
- **Y** = TOG em ppm;
- **X** = leitura em unidades de fluorescência fornecida pelo monitor;
- **a = 0,31236**;
- **b = -179,38**;
- **R² = 0,927**.

O próprio texto ressalta que os valores de **a** e **b** devem ser **recalculados a cada nova calibração** do equipamento.

### 6.2 Significado prático da calibração
Esse exemplo mostra pontos essenciais:
- a leitura bruta do analisador não equivale automaticamente ao TOG regulatório;
- é necessária **curva de correlação** com método laboratorial de referência;
- a calibração depende do **tipo de óleo**, do **condicionamento de amostra** e do **estado do sistema**;
- alteração do blend ou da hidrodinâmica da amostra pode invalidar a calibração anterior.

### 6.3 Laboratório como referência de verificação
No caso do teste UVF, os resultados foram comparados com **Standard Methods 5520C** e também houve menção a boa correlação com o método gravimétrico **USEPA 1664**. Isso reforça o papel do laboratório para:
- validar a curva inicial;
- conferir deriva do analisador;
- investigar discrepâncias entre indicação em linha e comportamento esperado do processo.

**Fontes:** `regis-b461ca66d401c4840d2c46cc:pNone:46.60-76.0`

## 7. Exemplos de falhas e diagnóstico operacional

### 7.1 Gás livre causando erro em UVF
No teste de campo citado para fluorescência UV, os resultados iniciais foram insatisfatórios devido à grande quantidade de gás na água. O mecanismo descrito foi:
1. presença de gás na amostra;
2. respingos nas janelas da célula de medição;
3. deposição de óleo, sal e óxido de ferro;
4. leituras errôneas.

As ações corretivas adotadas foram:
- substituição do removedor de bolhas por outro mais eficiente;
- instalação em ponto mais alto;
- verificação periódica da célula com padrão sólido de emissão conhecida.

Isso evidencia um princípio importante: **mau condicionamento de amostra frequentemente se manifesta como problema analítico, mas sua causa raiz é mecânica/hidráulica**.

### 7.2 Problemas de continuidade operacional em analisador por espalhamento IR
Outro caso relatado mostrou boa correlação analítica, porém com **paradas frequentes por problemas de fluxo da amostra** no sistema de medição. Ou seja: boa resposta metrológica em teste não garante disponibilidade operacional.

### 7.3 Interferência por FeS
As fontes relatam ainda interferência causada por **FeS** em analisador por espalhamento de IR. Em águas com sulfetos, o texto informa necessidade de **injeção contínua de ácido a montante** para converter sulfeto de ferro em **H2S** ou garantir que o sulfeto esteja sob forma ácida.

Essa informação é relevante para diagnóstico: quando a leitura do TOG é incompatível com o desempenho esperado do tratamento e a água contém sulfetos, deve-se investigar interferência química/matriz, e não apenas falha de sensor.

### 7.4 Efeito do blend de óleo
Os analisadores por UVF e espalhamento são descritos como dependentes da composição do óleo. Assim, mudanças frequentes no blend podem exigir:
- nova correlação com laboratório;
- revisão do condicionamento da amostra;
- em alguns casos, migração para técnica menos dependente da origem do óleo, como IR com pré-extração.

**Fontes:** `regis-b461ca66d401c4840d2c46cc:pNone:46.60-76.0`, `regis-b461ca66d401c4840d2c46cc:pNone:79.60-103.0`

## 8. Uso do TOG para controle operacional do descarte
Do material fornecido, algumas conclusões operacionais são particularmente úteis para FPSO/FSO:

1. **TOG em linha é instrumento de controle de processo**, não apenas de registro ambiental.
2. A decisão sobre qual analisador usar deve considerar não só correlação analítica, mas também:
   - disponibilidade do sistema de amostragem;
   - facilidade de limpeza;
   - estabilidade frente a gás e sólidos;
   - sensibilidade a variação de blend.
3. **Boa correlação pontual não basta**: continuidade operacional e robustez são igualmente críticas.
4. Sempre que houver desvio relevante entre leitura em linha, tendência do processo e resultado laboratorial, a investigação deve começar por:
   - ponto e representatividade da amostragem;
   - presença de gás livre;
   - sólidos/turbidez;
   - incrustação e limpeza da célula;
   - validade da calibração;
   - temperatura da amostra, se aplicável;
   - interferentes químicos como sulfetos/FeS.

Pelas conclusões relatadas nas fontes:
- UVF foi o analisador de **maior simplicidade operacional** entre os testados;
- espalhamento IR/laser/visível, UVF e espalhamento IR exigem **condicionamento cuidadoso da amostra** e **nova calibração** quando varia o blend;
- espectrofotometria de IR pode ser preferível em sistemas com variação frequente do blend, embora com **maior custo e complexidade**.

**Fontes:** `regis-b461ca66d401c4840d2c46cc:pNone:79.60-103.0`

## 9. Referências ambientais citadas nas fontes e seu uso prudente
O material fornecido cita, em contexto histórico:
- limite de **20 mg/L** de óleo e graxas pelo método gravimétrico em referência ao **IBAMA/CONAMA 20/86**;
- exigência de métodos de coleta e análise conforme normas aprovadas pelo INMETRO ou, na ausência, **Standard Methods**;
- referência internacional da **IMO** com média mensal de **29 ppm** e picos diários de **42 ppm** em determinadas condições operacionais.

Para uso profissional adequado, essas referências devem ser lidas como **contexto trazido pelas fontes**, não como consolidação automática da obrigação vigente para uma unidade no Brasil. Em operações reais, o controle de descarte precisa ser conciliado com:
- legislação ambiental brasileira vigente;
- licenciamento e condicionantes específicos da instalação;
- critérios internos de operação e resposta a desvios;
- método analítico oficialmente aceito para o caso aplicável.

**Fontes:** `regis-b461ca66d401c4840d2c46cc:pNone:10.0-37.0`

## 10. Síntese técnica
Para controle do descarte de água produzida em FPSO/FSO, a medição de TOG deve ser entendida como um sistema integrado de:
- **método analítico**;
- **amostragem representativa**;
- **condicionamento de amostra**;
- **calibração com referência laboratorial**;
- **diagnóstico de interferências**;
- **robustez operacional do hardware**.

Os trechos fornecidos convergem para uma conclusão central: a maior causa de mau desempenho do monitoramento de TOG em campo não é apenas a tecnologia do sensor, mas a combinação entre **matriz da água produzida**, **gás/sólidos**, **estado do sistema de amostragem** e **adequação da calibração ao óleo efetivamente processado**.

**Fontes:** `regis-b461ca66d401c4840d2c46cc:pNone:10.0-37.0`, `regis-b461ca66d401c4840d2c46cc:pNone:38.60-54.0`, `regis-b461ca66d401c4840d2c46cc:pNone:46.60-76.0`, `regis-b461ca66d401c4840d2c46cc:pNone:79.60-103.0`, `petroles-4ee4bce16acf674505c8912d:pNone:371473.0-371537.0`