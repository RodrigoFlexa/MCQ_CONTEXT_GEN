# Volumes, propriedades e incerteza na medição fiscal de óleo, na medição de gás e na transferência de custódia em offloading

## 1. Contexto metrológico e limites desta síntese

Na medição fiscal e na transferência de custódia, o resultado relevante não é apenas a indicação bruta do medidor, mas o **mensurando efetivamente declarado**: tipicamente o volume em condições padronizadas, associado a propriedades do fluido e a uma incerteza conhecida. Em termos metrológicos, isso exige:

- definição clara do mensurando;
- instrumentos e sistemas calibrados;
- correções por propriedades do fluido e pelas condições de medição;
- rastreabilidade a padrões reconhecidos;
- tratamento das grandezas de influência e das fontes de incerteza.

Os trechos fornecidos também distinguem alguns conceitos úteis:

- **Medição fiscal**: medição do volume de produção fiscalizada no ponto aplicável de medição.
- **Medição operacional**: inclui medições para controle da produção e também volumes de petróleo e gás natural transportados, estocados, movimentados ou com **transferência de custódia**.
- **Fator de calibração do medidor**: quociente entre o volume bruto medido pelo sistema de calibração e o volume registrado pelo medidor durante o teste de calibração.
- **Rastreabilidade**: propriedade pela qual o resultado de uma medição se relaciona a referências estabelecidas, normalmente padrões nacionais ou internacionais, por uma cadeia contínua de comparações com incertezas estabelecidas.
- **Falha**: evento em que o desempenho do sistema de medição não atende aos requisitos exigidos.
- **Falha presumida**: variação dos volumes medidos sem correspondência com mudanças reais das condições operacionais.

Esses conceitos são diretamente relevantes para a aceitação de resultados em medição fiscal e para a reconciliação de resultados em offloading, ainda que os trechos fornecidos não detalhem um arranjo específico FPSO–navio aliviador.

**Fontes da seção:** `petroles-004c2afadba7ea17c7dd7908:pNone:3297902.0-3297969.0`

## 2. Determinação do volume de óleo em condições padrão

Um ponto central dos trechos é que, por exigência regulatória citada no material, a medição fiscal de óleo deve estar disponível em **condições padronizadas**. Para um sistema volumétrico, o volume corrigido de óleo é expresso por:

\[
Q_o = Q_{TP} \times (1-BS\&W) \times \frac{1}{B_o} \times CTL \times CPL
\]

onde:

- **\(Q_o\)** = vazão/volume de óleo corrigido para condições padrão;
- **\(Q_{TP}\)** = vazão total medida em condições operacionais pelo medidor operacional, incluindo óleo + água;
- **BS&W** = teor de água e sedimentos básicos no óleo, medido em condições operacionais;
- **\(1/B_o\)** = fator de encolhimento do óleo;
- **CTL** = fator de correção de volume devido à temperatura;
- **CPL** = fator de correção de volume devido à pressão.

### Interpretação física da equação

A estrutura da equação mostra uma sequência de depurações e correções:

1. **Parte-se do volume total medido em linha**.
2. **Remove-se a fração não óleo** por meio de \((1-BS\&W)\).
3. **Converte-se do comportamento em condição operacional para a condição padrão**, considerando liberação de gás/encolhimento por \(1/B_o\).
4. **Aplicam-se as correções térmica e de pressão** por CTL e CPL.

Em termos práticos, isso significa que um bom medidor volumétrico, isoladamente, não basta para boa medição fiscal: a qualidade do resultado final depende também da qualidade metrológica de **BS&W**, do modelo/PVT usado para **\(B_o\)** e das medições/correções ligadas a temperatura e pressão.

### Medição mássica

O trecho também apresenta uma forma equivalente para medidor mássico, baseada na razão entre vazão mássica e a propriedade que representa a massa específica nas condições operacionais. Pelo estado do OCR, o símbolo aparece degradado, mas a lógica física é:

\[
Q_o \propto \frac{M_{TP}}{\rho_{TP}} \times (1-BS\&W) \times \frac{1}{B_o} \times CTL \times CPL
\]

Ou seja, em medição mássica, a determinação do volume padrão continua dependente da **massa específica/densidade em condição de medição**, além das demais correções de qualidade e PVT.

### Consequências operacionais

A equação deixa claro que discrepâncias em transferência de custódia podem nascer de várias origens diferentes, por exemplo:

- volume bruto correto, mas **BS&W mal determinado**;
- densidade/PVT inadequados, afetando **\(B_o\)**;
- sensores de temperatura/pressão fora de tolerância, afetando **CTL/CPL**;
- uso de correlação de propriedades fora da faixa representativa do fluido.

Por isso, a discussão de volume não pode ser separada da discussão de propriedades e incerteza.

**Fontes da seção:** `regis-44b5e0f18c0eba454e5dfcf8:pNone:271.0-318.0`, `petroles-004c2afadba7ea17c7dd7908:pNone:2857688.0-2857761.0`

## 3. Propriedades do fluido que mais afetam o resultado metrológico

### 3.1 BS&W

O teor de água e sedimentos básicos entra multiplicativamente no resultado final. Logo:

- erro em BS&W propaga-se diretamente para o volume líquido de óleo;
- a sensibilidade aumenta em correntes com maior variabilidade de emulsão e água livre;
- em sistemas com óleo cru, presença de água emulsionada é citada como uma das fontes relevantes de variabilidade da medição.

### 3.2 Fator de encolhimento \(B_o\)

O material associa o fator de encolhimento à conversão do óleo das condições operacionais para a condição padrão, refletindo liberação de gás e mudança volumétrica. A qualidade desse fator é crítica porque:

- afeta diretamente o volume padrão declarado;
- depende da representatividade dos dados PVT/laboratoriais;
- sua incerteza integra o orçamento global de incerteza da medição fiscal.

Um trecho adicional mostra um uso prático importante: **a medição de densidade pode servir para estimar o fator de encolhimento**, comparando o valor estimado com o resultado experimental. Com isso, resultados com desvios excessivos podem ser reprovados antes de entrar em banco de dados, e a correlação pode ser recalculada à medida que novos dados válidos sejam incorporados. Isso é particularmente útil como rotina de **validação de dados** que alimentam a medição fiscal.

### 3.3 Densidade / massa específica

A densidade é destacada como grandeza de grande importância em transações comerciais porque relaciona massa e volume do produto. Nos contextos de medição fiscal e transferência de custódia, ela é relevante por pelo menos três caminhos:

- conversão entre medição mássica e volumétrica;
- suporte à determinação/validação de fatores de correção e encolhimento;
- caracterização de produto para fins de aceitação comercial e reconciliação metrológica.

### 3.4 Temperatura e pressão: CTL e CPL

CTL e CPL representam a dependência volumétrica do fluido com temperatura e pressão. Conceitualmente:

- **CTL** corrige contração/dilatação térmica;
- **CPL** corrige compressibilidade/efeito da pressão.

Isso significa que a qualidade da medição de temperatura e pressão não é apenas auxiliar: ela integra o próprio cálculo do volume padrão.

### 3.5 Grandezas de influência típicas

Os trechos listam diversas variabilidades relevantes à medição de vazão e, por consequência, à determinação de volume e propriedades:

- variação de propriedades do fluido;
- perfil assimétrico de velocidade;
- regime de escoamento;
- turbulência;
- influência externa da instalação;
- interferência eletromagnética;
- água emulsionada no óleo;
- gás dissolvido;
- gás livre;
- encolhimento do óleo.

Em operações de offloading, essas mesmas variabilidades tendem a se refletir na comparação entre o valor medido a bordo da unidade e o valor aceito para transferência, ainda que o material fornecido não trate das particularidades instrumentais desse arranjo.

**Fontes da seção:** `regis-44b5e0f18c0eba454e5dfcf8:pNone:271.0-318.0`, `regis-2957bf09b49f6e9e6c5ea146:pNone:507.0-758.0`, `petroles-004c2afadba7ea17c7dd7908:pNone:2857688.0-2857761.0`

## 4. Gestão da incerteza de medição

### 4.1 Conceito

Os trechos definem a incerteza de medição como um parâmetro associado ao resultado que caracteriza a dispersão dos valores que podem ser fundamentadamente atribuídos ao mensurando. Em termos práticos, ela expressa a parte da dúvida que permanece mesmo quando se controla o processo de medição.

### 4.2 Fontes de incerteza citadas no material

O material enumera fontes importantes, entre elas:

1. definição incompleta do mensurando;
2. amostragem não representativa;
3. conhecimento insuficiente do processo;
4. conhecimento inadequado das condições ambientais;
5. viés de operador em leitura analógica;
6. método inadequado;
7. padrões ou materiais de referência com valores inexatos/não calibrados;
8. princípio de medição impróprio.

Essa lista é particularmente útil para medição fiscal porque mostra que a incerteza não nasce apenas do elemento primário de vazão. Ela é sistêmica.

### 4.3 Propagação da incerteza para o volume padrão de óleo

O trecho apresenta a forma de incerteza combinada por propagação de derivadas parciais. Para medição volumétrica, a estrutura geral é:

\[
u(Q_o)=\sqrt{\sum \left(\frac{\partial Q_o}{\partial x_i}u(x_i)\right)^2}
\]

com contribuições principais de:

- **\(u(Q_{TP})\)**: incerteza padrão do medidor operacional;
- **\(u(BS\&W)\)**: incerteza do sistema/medição de BS&W;
- **\(u(B_o)\)**: incerteza associada ao fator de encolhimento;
- incerteza associada às **curvas de ajuste PVT e às correções de condições padrão**.

Para medição mássica, a estrutura análoga inclui também:

- **\(u(M_{TP})\)**: incerteza da vazão mássica;
- **\(u(\rho_{TP})\)** ou grandeza equivalente em condição operacional, conforme a formulação OCRada do trecho.

### 4.4 Leitura técnica do orçamento de incerteza

A maior contribuição para a incerteza combinada nem sempre é a do medidor principal. Em petróleo, por exemplo, podem dominar:

- erro na determinação de BS&W em correntes instáveis;
- erro na densidade/PVT que alimenta \(B_o\);
- correções CTL/CPL baseadas em temperatura/pressão pouco estáveis;
- falta de representatividade da amostra laboratorial.

Assim, a gestão de incerteza deve ser feita no nível de **sistema de medição**, não apenas no nível do medidor de vazão.

### 4.5 Repetitividade, erro máximo admissível e regra metrológica prática

Um dos trechos sobre densímetros menciona a prática de exigir que o padrão usado para calibrar tenha erro máximo admissível significativamente menor que o do instrumento sob calibração, citando como exemplo uma relação de 1/10 e mencionando que relações 1/5 ou 1/3 podem ser consideradas em outros contextos. Embora o trecho seja específico e não deva ser tomado como regra universal, ele reforça um princípio importante: o padrão de referência precisa ter qualidade metrológica compatível com a meta de incerteza do sistema final.

**Fontes da seção:** `regis-44b5e0f18c0eba454e5dfcf8:pNone:271.0-318.0`, `petroles-004c2afadba7ea17c7dd7908:pNone:3297902.0-3297969.0`, `regis-2957bf09b49f6e9e6c5ea146:pNone:7176.0-7457.0`

## 5. Instrumentação e controle metrológico dos sistemas de medição

### 5.1 Medidores do tipo turbina

O material informa que a faixa operacional de medidores turbina aumenta com o diâmetro nominal. Como características típicas citadas:

- menores tamanhos: razão de faixa da ordem de **5 ou 6:1**;
- maiores tamanhos: até **10 ou 15:1**;
- linearidade típica dentro da faixa: cerca de **±0,25%** ou **±0,5%**.

Em aplicações de petróleo, é comum a utilização de **estações de medição com várias turbinas em paralelo** para cobrir a faixa total de operação. O trecho também menciona a possibilidade de:

- um medidor extra para procedimentos de calibração;
- um medidor reserva.

### 5.2 Fator K e calibração por provadores

Para turbinas, o parâmetro-chave é o **fator K**, expresso em ciclos por unidade de volume:

\[
K = \frac{F}{V}
\]

onde:

- **F** = número de pulsos totalizados;
- **V** = volume que passou pelo medidor na condição da calibração.

Quando o interesse é medição fiscal ou transferência de custódia, o trecho destaca a necessidade de **calibração periódica por provadores**. Isso é essencial porque desgaste de mancais, deposição de parafina nas pás e outras degradações podem alterar severamente a resposta do medidor, às vezes sem percepção imediata se não houver recalibração periódica.

### 5.3 Condicionamento da instalação

Duas recomendações de instalação aparecem de forma direta no material:

- uso de **filtros a montante** para evitar partículas sólidas que possam travar ou afetar o rotor;
- uso frequente de **separador de gás antes da turbina** para evitar erros causados por bolhas de gás arrastadas pelo fluido líquido.

Essas medidas são importantes porque parte da incerteza total decorre da interação entre o princípio de medição e o estado real do escoamento.

### 5.4 Aprendizados qualitativos com Ball Prover

O trecho sobre Ball Prover está degradado por OCR, mas preserva conclusões úteis:

- em **vazões muito baixas**, a qualidade da calibração pode piorar devido à perda de movimento contínuo da esfera;
- em **vazão intermediária**, a turbina tende a apresentar leitura mais confiável pelo aumento do número de pulsos gerados;
- os resultados indicam a importância de avaliar a adequação da faixa de operação do provador e do medidor, em vez de assumir comportamento uniforme em toda a faixa.

Para controle metrológico, isso reforça a necessidade de verificar se a calibração cobre as condições representativas de operação e se o número de pulsos/ciclos é suficiente para a meta de incerteza.

**Fontes da seção:** `regis-44b5e0f18c0eba454e5dfcf8:pNone:271.0-318.0`, `petroles-4ee4bce16acf674505c8912d:pNone:1658501.0-1658554.0`

## 6. Determinação e calibração de densidade como propriedade crítica

### 6.1 Papel da densidade

A densidade é tratada no material como propriedade de grande importância no setor de petróleo e gás, especialmente por ligar massa e volume em transações comerciais. Em sistemas fiscais ou de custódia, erros de densidade afetam:

- conversões massa-volume;
- correções de propriedade e PVT;
- validação de dados laboratoriais;
- aceitação comercial do produto.

### 6.2 Calibração de densímetros de processo

O material sobre densímetros digitais de tubo oscilatório ressalta que, antes do uso, o instrumento deve ser calibrado **nas condições de temperatura, pressão e densidade em que será utilizado**, para:

- conhecer seu estado metrológico;
- estimar erro máximo/compatibilidade com a meta metrológica;
- garantir rastreabilidade.

Há também a recomendação de que uma recalibração seja realizada nas **mesmas condições da primeira calibração** para que os resultados sejam comparáveis. O trecho apresenta como exemplo experimental:

- fluidos: água, nitrogênio e propano com pureza certificada, preferencialmente MRC;
- pressões: 15,7; 20,6; 25,5; 30,4; 35,3; 40,2 bar;
- temperaturas: 25; 30; 35; 40 °C.

Esses valores devem ser entendidos como **exemplo de campanha de calibração**, não como exigência geral para qualquer sistema fiscal.

### 6.3 Compensação de pressão no densímetro

Um ponto técnico importante do material é que o densímetro citado calcula a densidade à temperatura de medição, mas **não considera internamente a variação da densidade com a pressão**. Por isso, recomenda-se:

- solicitar ao fabricante as constantes específicas de pressão do instrumento;
- ou desenvolver metodologia experimental para obter tais constantes e ajustar curva de variação da densidade com a pressão.

Esse ponto é crítico porque um densímetro aparentemente estável pode introduzir viés sistemático se a influência da pressão não for corretamente compensada.

### 6.4 Estabilidade das variáveis durante a calibração

O estudo piloto mencionado no material indica que o densímetro testado tinha potencial para atender requisitos metrológicos, mas apontou como condição crítica a **estabilidade das variáveis ao longo do experimento**. Isso tem implicação direta para uso em processo:

- flutuações de temperatura, pressão e composição durante calibração ou verificação degradam a comparabilidade;
- a incerteza de densidade não depende apenas do sensor, mas também da estabilidade do sistema onde ele é calibrado/verificado.

**Fontes da seção:** `regis-2957bf09b49f6e9e6c5ea146:pNone:507.0-758.0`, `regis-2957bf09b49f6e9e6c5ea146:pNone:7176.0-7457.0`

## 7. Aspectos aplicáveis à medição de gás natural

Os trechos fornecidos não trazem uma equação completa de volume padrão de gás natural, mas trazem um ponto decisivo para a gestão da incerteza: a **representatividade da amostra** e o controle das propriedades do gás.

### 7.1 Amostragem representativa

Em correntes próximas ao ponto de orvalho de hidrocarbonetos, pequenas mudanças de pressão e temperatura durante a coleta podem provocar **condensação parcial**, alterando a composição da amostra e comprometendo sua representatividade. O trecho alerta também para situações em que a corrente de gás:

- carrega gotículas de líquido condensado;
- ou apresenta escoamento multifásico com líquido e gás segregados no duto.

Isso é especialmente relevante porque composição e densidade do gás influenciam qualquer conversão para condições de referência e o cálculo de propriedades derivadas.

### 7.2 Boas práticas qualitativas indicadas no trecho

O material recomenda, qualitativamente, que o ponto de amostragem seja:

- montado preferencialmente na vertical, no topo de trecho reto de tubulação horizontal;
- com probe entrando até a região central da seção de escoamento;
- posicionado a jusante suficiente de elementos perturbadores;
- e que a eventual redução de pressão para coleta use aquecimento, evitando resfriamento por efeito Joule-Thomson e consequente condensação.

Mesmo sem os valores numéricos completos no trecho OCRado, a mensagem técnica é clara: **erro de amostragem é erro de propriedade**, e erro de propriedade se transforma em erro de volume/faturamento.

### 7.3 Densidade e composição do gás

O conjunto de trechos menciona normas e práticas ligadas à determinação de composição com incerteza definida, amostragem de gás natural e cálculo de fator de compressibilidade, mas sem desenvolver essas metodologias. Ainda assim, fica estabelecido o princípio de que a medição de gás confiável depende de um encadeamento entre:

- amostragem representativa;
- composição confiável;
- propriedades termofísicas coerentes;
- instrumentos calibrados e rastreáveis.

**Fontes da seção:** `petroles-004c2afadba7ea17c7dd7908:pNone:4262903.0-4262991.0`, `regis-2957bf09b49f6e9e6c5ea146:pNone:507.0-758.0`

## 8. Tratamento, validação de dados e critérios de decisão

### 8.1 Validação técnica de resultados de propriedades

O material apresenta um caso útil de validação do fator de encolhimento por meio de densidade. A lógica é:

1. estimar o fator de encolhimento a partir da densidade;
2. comparar o valor estimado com o resultado experimental;
3. aceitar ou rejeitar o resultado com base no desvio obtido;
4. atualizar o banco de dados e recalcular a correlação com novos dados válidos.

Esse tipo de rotina é relevante para medição fiscal porque evita alimentar o sistema de medição com propriedades inconsistentes ou não representativas.

### 8.2 Decisões típicas sustentadas por abordagem metrológica

Com base nos trechos, decisões técnicas robustas sobre volumes, propriedades e incerteza passam por perguntas como:

- o mensurando está claramente definido?
- a amostra ou dado de propriedade é representativo da corrente real?
- o instrumento foi calibrado na faixa e nas condições relevantes?
- o padrão usado tem qualidade metrológica compatível?
- as correções de temperatura, pressão e encolhimento estão sustentadas por dados válidos?
- o comportamento do medidor na faixa baixa/intermediária/alta foi verificado?
- existe evidência de falha ou falha presumida?

### 8.3 Registros e auditoria metrológica

Embora os trechos não detalhem um procedimento documental completo, os conceitos de rastreabilidade, fator de calibração, falha e incerteza implicam a necessidade de manter, no mínimo:

- histórico de calibrações/verificações;
- identificação dos padrões utilizados;
- resultados e incertezas associadas;
- condições de operação representativas usadas na avaliação;
- registros de desvios, falhas e ações corretivas;
- critérios documentados de aceitação/rejeição de dados de propriedades.

Em transferência de custódia por offloading, esse conjunto é essencial para sustentar tecnicamente reconciliações entre partes, mesmo quando o material fornecido não aborda diretamente a interface FPSO–navio.

**Fontes da seção:** `petroles-004c2afadba7ea17c7dd7908:pNone:3297902.0-3297969.0`, `petroles-004c2afadba7ea17c7dd7908:pNone:2857688.0-2857761.0`, `regis-44b5e0f18c0eba454e5dfcf8:pNone:271.0-318.0`

## 9. Síntese técnica

Os trechos convergem para uma ideia central: **medição fiscal e transferência de custódia confiáveis dependem da integração entre medidor, propriedades do fluido e gestão formal da incerteza**.

Para óleo, o resultado em condição padrão depende explicitamente de:

- volume bruto ou massa medida;
- BS&W;
- fator de encolhimento;
- correções por temperatura e pressão.

Para gás, o material recebido destaca sobretudo que a confiabilidade do resultado depende da qualidade da amostragem e da determinação das propriedades, especialmente quando há risco de condensação e perda de representatividade.

Em ambos os casos, o controle metrológico eficaz requer:

- calibração periódica e rastreável;
- verificação da adequação da instalação;
- avaliação sistemática de fontes de incerteza;
- validação dos dados de propriedades;
- identificação e tratamento de falhas e falhas presumidas.

**Fontes da seção:** `regis-44b5e0f18c0eba454e5dfcf8:pNone:271.0-318.0`, `regis-2957bf09b49f6e9e6c5ea146:pNone:507.0-758.0`, `petroles-004c2afadba7ea17c7dd7908:pNone:3297902.0-3297969.0`, `petroles-004c2afadba7ea17c7dd7908:pNone:4262903.0-4262991.0`