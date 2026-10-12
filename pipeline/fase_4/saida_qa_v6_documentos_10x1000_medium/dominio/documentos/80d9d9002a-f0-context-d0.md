# Projeto e instalação da medição fiscal de óleo e gás e da medição de transferência de custódia em offloading

## 1. Enquadramento regulatório e metrológico
Os sistemas de medição de petróleo e gás natural empregados em produção, apropriação, controle operacional e transferência de custódia estão sujeitos ao Regulamento Técnico de Medição (RTM), no âmbito regulatório ANP/Inmetro, para aspectos de projeto, instalação e operação. O campo de aplicação resumido nos trechos fornecidos inclui sistemas destinados a medir, computar, armazenar, indicar e registrar volumes de petróleo e gás natural produzidos, injetados, processados, movimentados, acondicionados ou estocados, inclusive para medição fiscal, apropriação, controle operacional e transferência de custódia. Também há previsão de medições para importação/exportação e de água para controle operacional.

Para fins de conformidade de projeto e instalação, o ponto central é que **cada categoria de medição tem rigor metrológico próprio**, com diferenças de classe de exatidão, frequência de calibração e requisitos de controle. Os trechos indicam que os sistemas de medição fiscal, de transferência de custódia e de apropriação devem ser concebidos para atender às respectivas classes de exatidão do RTM, embora os valores numéricos não estejam legíveis no material fornecido.

Além da regulação técnica, o Decreto nº 2.705/1998, conforme o resumo reproduzido, vincula a medição ao cálculo de participações governamentais e exige que o concessionário determine periodicamente e regularmente o volume e a qualidade do petróleo e do gás produzidos, mantenha boletins de medição completos e acurados e envie boletins mensais de produção à ANP, sujeitos a correções posteriores.

**Implicação de projeto:** a conformidade não se limita ao medidor. O sistema deve ser desenhado para medir, corrigir, armazenar, reprocessar e auditar os resultados de forma rastreável.

**Fontes da seção:** `petroles-4ee4bce16acf674505c8912d:pNone:1742924.0-1742958.0`, `regis-01a1a980c36144019fe34865:pNone:1204.0-1421.0`, `petroles-004c2afadba7ea17c7dd7908:pNone:3297902.0-3297969.0`

## 2. Tipos de medição e arranjos relevantes para FPSO
Nos trechos fornecidos aparecem as seguintes categorias:

- **Medição fiscal:** medição do volume de produção fiscalizada no ponto de medição da produção, associada à transferência de propriedade da União para o concessionário.
- **Medição fiscal compartilhada:** usada quando a produção de dois ou mais campos se mistura antes do ponto fiscal.
- **Medição para apropriação:** usada para determinar quanto da produção total cabe a cada campo, concessão ou poço.
- **Medição operacional:** usada para controle de processo, movimentação, estocagem, consumo, injeção, gás ventilado/queimado etc.
- **Medição para transferência de custódia:** realizada na transferência de propriedade do óleo/gás do vendedor para o comprador, devendo seguir os mesmos requisitos técnicos da medição fiscal.

Para FPSOs, o material cita como arranjos observados na Bacia de Campos:

- **Medição fiscal em linha**, a montante do tanque de estocagem, como configuração comum em FPSOs;
- **Medição fiscal compartilhada**, a jusante de ponto de mistura de óleos de mais de um campo;
- **Medição fiscal durante o alívio (offloading)**, adotada em alguns ativos, embora não descrita como solução universal.

Em caso de medição fiscal compartilhada, a apropriação não deve ser tratada de forma simplista por diferença entre um medidor fiscal compartilhado e apenas um medidor adicional a jusante, porque perdas entre concessões (por exemplo, vazamentos em linha de transferência) podem distorcer o volume efetivamente retirado de cada reservatório. O trecho indica que a ANP exige medição de apropriação em cada concessão relevante nesses casos.

**Implicação de projeto:** ao definir a arquitetura de medição em um FPSO, é preciso distinguir claramente se o ponto servirá a:
1. produção fiscal do campo;
2. apropriação entre campos/poços;
3. transferência de custódia durante o offloading.

Essas finalidades não são intercambiáveis, ainda que usem tecnologias de medição semelhantes.

**Fontes da seção:** `petroles-004c2afadba7ea17c7dd7908:pNone:1854969.0-1855014.0`, `petroles-004c2afadba7ea17c7dd7908:pNone:1185091.0-1185125.60`, `petroles-4ee4bce16acf674505c8912d:pNone:1742924.0-1742958.0`, `regis-864b525b79e3c20e7da3415d:pNone:293.60-341.0`

## 3. Localização dos pontos de medição e documentação para aprovação
Os trechos trazem critérios objetivos de localização para os pontos fiscais da produção:

### 3.1 Petróleo
O ponto de medição fiscal da produção de petróleo deve localizar-se **imediatamente após**:
- as instalações de separação;
- tratamento; e
- tancagem da produção,

e **antes** de quaisquer instalações de:
- transferência;
- processamento;
- estocagem em estações de armazenamento;
- transporte; ou
- terminais marítimos.

### 3.2 Gás natural
O ponto de medição fiscal da produção de gás natural deve localizar-se **imediatamente após**:
- as instalações de separação; e
- condicionamento,

e **antes** de quaisquer instalações de:
- transferência;
- processamento; ou
- transporte.

### 3.3 Aprovação e fiscalização pré-operacional
Para aprovação junto à ANP, os trechos indicam a necessidade de apresentar, entre outros:
- diagrama esquemático das instalações com principais correntes de óleo, gás e água e localização dos pontos de medição;
- fluxograma de engenharia dos sistemas de medição com tubulações, medidores e acessórios;
- especificações e folhas de dados dos instrumentos, amostradores e acessórios;
- memorial descritivo dos sistemas de medição e dos sistemas de calibração;
- memorial descritivo da operação, incluindo procedimentos de medição, amostragem, análise, determinação de propriedades e cálculo dos volumes.

Além disso, os sistemas de medição fiscal da produção devem ser **inspecionados pela ANP antes do início da produção** do campo ou de um teste de longa duração, para verificação da correta instalação e do funcionamento.

**Implicação de projeto:** a conformidade de instalação depende tanto do posicionamento físico correto do ponto de medição quanto da completude documental que demonstre a coerência entre processo, instrumentação, amostragem, cálculo e calibração.

**Fontes da seção:** `petroles-004c2afadba7ea17c7dd7908:pNone:1185382.0-1185418.0`, `petroles-004c2afadba7ea17c7dd7908:pNone:1185091.0-1185125.60`, `regis-01a1a980c36144019fe34865:pNone:1204.0-1421.0`

## 4. Requisitos de projeto do sistema de medição de petróleo em linha
Os trechos convergem para um conjunto mínimo de componentes para medição dinâmica de petróleo em linha.

### 4.1 Equipamentos mínimos
O sistema deve incluir, pelo menos:
- **medidor de fluidos** do tipo deslocamento positivo, turbina ou mássico tipo Coriolis com indicação de volume;
- **sistema de amostragem proporcional à vazão**, controlado por sinal de saída do medidor;
- **instrumento ou sistema de medição/compensação de temperatura**;
- **instrumento ou sistema de medição/compensação de pressão**;
- **sistema de calibração fixo ou móvel**, apropriado para calibração do medidor e aprovado/autorizado pela ANP.

Um dos trechos também destaca que os medidores devem possuir **totalizador protegido contra acessos não autorizados**, requisito importante para inviolabilidade e segurança metrológica.

### 4.2 Correções que o projeto deve contemplar
As medições de petróleo em linha devem ser corrigidas por fatores associados a:
- **dilatação térmica** entre a temperatura de medição e a temperatura de referência;
- **compressibilidade do líquido** entre a pressão de medição e a pressão de referência;
- **conteúdo de água e sedimentos (BSW)** no petróleo.

Portanto, o projeto não pode tratar o medidor como elemento isolado: a cadeia de medição deve permitir medição de propriedades, amostragem representativa e processamento dos fatores de correção.

### 4.3 Condição do fluido medido
O material informa que, **exceto nas medições para apropriação**, o petróleo medido nos pontos de medição deve ser **estabilizado** e não exceder o limite regulamentar de água e sedimentos. Embora o valor numérico do limite não esteja legível nos trechos, a implicação para projeto é clara: a medição fiscal e a de transferência de custódia requerem integração adequada com as etapas de separação/tratamento para que o fluido chegue ao ponto de medição em condição aceitável.

### 4.4 Critérios práticos de seleção do medidor
Os trechos acadêmicos resumem características típicas dos medidores aceitos:
- **Deslocamento positivo:** pode ser aplicado a líquidos e gases; não depende de alimentação externa; pode ser vantajoso para fluidos mais viscosos; e, segundo o trecho, não exige trecho reto montante/jusante como requisito dominante do princípio de medição.
- **Turbina:** medidor volumétrico para líquidos e gases sem impurezas relevantes; reconhecido por alta linearidade e repetitividade; requer atenção à qualidade do fluido e às condições de escoamento.
- **Coriolis com indicação de volume:** mede vazão mássica a partir da força associada ao escoamento em tubo vibratório, podendo disponibilizar indicação volumétrica para atendimento ao sistema.

**Implicação de projeto:** a escolha do medidor deve ser coerente com viscosidade, limpeza do fluido, necessidade de prova/calibração, integração com amostragem e estratégia de correção de volume.

**Fontes da seção:** `regis-864b525b79e3c20e7da3415d:pNone:293.60-341.0`, `petroles-004c2afadba7ea17c7dd7908:pNone:1854969.0-1855014.0`, `petroles-004c2afadba7ea17c7dd7908:pNone:1185091.0-1185125.60`, `petroles-004c2afadba7ea17c7dd7908:pNone:1185382.0-1185418.0`

## 5. Requisitos de projeto do sistema de medição de gás natural
### 5.1 Local de medição e configuração básica
Os trechos indicam que a medição de gás deve ser realizada **em linha**, após a saída do gás do separador, e o ponto fiscal da produção de gás deve estar localizado após separação/condicionamento e antes de transferência, processamento ou transporte.

### 5.2 Tecnologias de medição
Nos trechos com redação atribuída ao RTM/Portaria, as medições de gás natural nos pontos de medição da produção devem usar:
- **placa de orifício**;
- **turbina**; ou
- **medidor ultrassônico**.

Há um trecho secundário que também cita Coriolis para gás, mas a redação normativa reproduzida nos demais trechos é mais restritiva. Para avaliação conservadora de conformidade de projeto e instalação, convém tomar como base o conjunto explicitamente associado à medição da produção nos trechos normativos reproduzidos.

### 5.3 Compensações automáticas e cálculo
O sistema de medição de gás deve incluir dispositivos para compensação automática de:
- **pressão estática**;
- **temperatura**; e
- **variações do coeficiente de compressibilidade do gás** decorrentes dessas grandezas.

Um computador de vazão deve ser programado para calcular os volumes produzidos a partir dessas variáveis. Um dos trechos ressalta explicitamente, no caso do gás natural, a importância da pressão estática **absoluta** no cálculo.

**Implicação de projeto:** a conformidade de um sistema de gás não depende apenas do elemento primário/medidor, mas da qualidade da instrumentação auxiliar, do modelo de compensação e do processamento de dados implementado no computador de vazão.

**Fontes da seção:** `petroles-004c2afadba7ea17c7dd7908:pNone:1185382.0-1185418.0`, `regis-864b525b79e3c20e7da3415d:pNone:293.60-341.0`, `petroles-4ee4bce16acf674505c8912d:pNone:1742924.0-1742958.0`

## 6. Estação de medição, instrumentação auxiliar e integração de instalação
Um dos trechos descreve a **Estação de Medição de Petróleo e Gás Natural (EMED)** como o conjunto que delimita fisicamente o sistema de medição no campo. Nessa descrição, a EMED pode compreender:
- medidor;
- provador;
- computador de vazão;
- transmissores de pressão e temperatura;
- filtro;
- desaerador;
- densímetros de linha; e
- acessórios diversos.

Essa visão é útil para avaliar projeto e instalação em FPSOs: a medição fiscal ou de transferência de custódia deve ser tratada como **um sistema integrado**, e não como um único instrumento.

O computador de vazão, além de calcular volumes corrigidos, deve estar integrado aos instrumentos de campo por rede adequada ao ambiente industrial. O trecho cita a rede HART como exemplo de comunicação, o que reforça a necessidade de projeto compatível com ambiente offshore hostil, manutenção e diagnóstico.

**Implicação de instalação:** disposição física, acessibilidade, interligações, isolamento para prova/calibração, qualidade dos sinais de pressão/temperatura e integridade da cadeia de aquisição são parte da conformidade técnica do sistema.

**Fontes da seção:** `regis-864b525b79e3c20e7da3415d:pNone:293.60-341.0`

## 7. Calibração, rastreabilidade e controle metrológico
### 7.1 Conceitos metrológicos relevantes
Os trechos trazem definições úteis para avaliar conformidade:
- **calibração:** conjunto de operações que estabelece a relação entre valores indicados por um instrumento/sistema e os valores correspondentes estabelecidos por padrões;
- **classe de exatidão:** classe de instrumentos que satisfazem exigências metrológicas específicas;
- **erro de medição, desvio, fator de correção e incerteza de medição:** bases para julgar desempenho metrológico;
- **rastreabilidade:** propriedade de o resultado estar relacionado a padrões nacionais ou internacionais por cadeia contínua de comparações, todas com incertezas estabelecidas;
- **falha** e **falha presumida:** situações em que o desempenho não atende aos requisitos ou a variação medida não corresponde às condições operacionais.

### 7.2 Controle metrológico
Os instrumentos de medição, medidas materializadas e sistemas de medição utilizados devem ser submetidos ao controle metrológico do Inmetro, quando aplicável, ou comprovar rastreabilidade aos padrões do Inmetro. As calibrações e inspeções requeridas devem ser executadas por conta e risco do concessionário/autorizatário e por pessoas ou entidades qualificadas.

### 7.3 Fator de calibração do medidor
O material define o **fator de calibração do medidor** como o quociente entre:
- o volume bruto medido por um sistema de calibração; e
- o volume registrado pelo medidor durante um teste de calibração.

Em forma compacta:

**Fator de calibração = Volume bruto medido no sistema de calibração / Volume registrado pelo medidor no teste**

Esse conceito é central para projeto, porque a instalação deve prever meios físicos e lógicos para executar a calibração e incorporar corretamente o fator ao cálculo.

### 7.4 Sistemas de calibração para líquidos em linha
Para instalações e operação de sistemas de calibração de medidores de petróleo em linha, os trechos citam como alternativas:
- **provadores**;
- **tanques de prova**;
- **medidores padrão**; ou
- outros sistemas previamente autorizados pela ANP.

O trecho sobre transferência de custódia destaca o uso frequente do **provador bidirecional de esfera (bi-directional ball prover)** para grandes volumes líquidos.

**Implicação de projeto:** a estação deve nascer com filosofia de prova/metrologia claramente definida: tipo de provador, condições de operação, integração com computador de vazão, rastreabilidade dos padrões e acessibilidade para inspeção.

**Fontes da seção:** `petroles-004c2afadba7ea17c7dd7908:pNone:3297902.0-3297969.0`, `petroles-004c2afadba7ea17c7dd7908:pNone:1185382.0-1185418.0`, `petroles-4ee4bce16acf674505c8912d:pNone:1658044.0-1658072.60`, `petroles-4ee4bce16acf674505c8912d:pNone:1742924.0-1742958.0`

## 8. Transferência de custódia em operações de offloading
Na transferência de custódia, o foco metrológico é particularmente crítico porque há transferência de propriedade entre partes contratuais distintas e impacto econômico/fiscal relevante. O material afirma que esses pontos devem seguir **os mesmos requisitos técnicos da medição fiscal**.

Para operações de offloading em FPSO, os trechos permitem sustentar as seguintes conclusões de projeto e instalação:

1. **O arranjo de medição pode ser distinto do arranjo fiscal em linha a montante dos tanques.** O material cita a existência, em alguns FPSOs, de medição fiscal durante o alívio/offloading.
2. **O sistema deve ser em linha e metrologicamente demonstrável.** Para líquidos, isso inclui medidor aceito, compensações, amostragem proporcional à vazão e sistema de calibração/prova.
3. **A calibração é parte intrínseca do arranjo.** Em transferência de custódia, a verificação de desempenho do medidor é tratada como requisito fundamental.
4. **Provadores são especialmente relevantes.** O uso de ball prover é citado como comum em grandes volumes de líquidos em transferência de custódia.
5. **A documentação do ponto contratual e do sistema é indispensável.** O arranjo físico do ponto de medição, os instrumentos auxiliares, a forma de amostragem, o cálculo do volume e a sistemática de prova devem estar descritos e aprovados no contexto aplicável.

**Implicação de conformidade:** um sistema de offloading não é tecnicamente aceitável apenas porque mede vazão. Ele precisa demonstrar aderência ao mesmo patamar técnico-metrológico exigido para medição fiscal, com ênfase em prova, correções volumétricas, rastreabilidade e inviolabilidade dos dados.

**Fontes da seção:** `petroles-004c2afadba7ea17c7dd7908:pNone:1854969.0-1855014.0`, `petroles-004c2afadba7ea17c7dd7908:pNone:1185091.0-1185125.60`, `petroles-4ee4bce16acf674505c8912d:pNone:1658044.0-1658072.60`, `regis-864b525b79e3c20e7da3415d:pNone:293.60-341.0`

## 9. Registros, tratamento de dados e auditabilidade como requisitos de projeto
Embora muitas vezes vistos como tema operacional, os trechos mostram que registros e tratamento de dados também são requisitos de projeto:

- o concessionário deve manter boletins de medição com vazões praticadas e produção acumulada;
- deve enviar boletins mensais à ANP;
- os registros estão sujeitos a correções para determinar a quantidade exata efetivamente recebida;
- a documentação para sistemas alternativos deve incluir procedimentos para **armazenamento de registros, rastreabilidade e inviolabilidade dos dados**.

Disso decorre que a arquitetura do sistema deve prever, desde a fase de projeto:
- registro confiável de variáveis primárias e auxiliares;
- retenção e recuperação de histórico;
- trilha de auditoria para reprocessamento de volumes;
- proteção contra acesso não autorizado e adulteração;
- coerência entre totalização local, computador de vazão e sistemas supervisórios/relatórios.

**Fontes da seção:** `regis-01a1a980c36144019fe34865:pNone:1204.0-1421.0`, `petroles-004c2afadba7ea17c7dd7908:pNone:1185382.0-1185418.0`, `petroles-004c2afadba7ea17c7dd7908:pNone:3297902.0-3297969.0`

## 10. Tecnologias alternativas e limite da conformidade por analogia
Os trechos informam que, para sistemas que não cumpram integralmente o RTM ou regulamentos metrológicos pertinentes, o concessionário pode requerer autorização à ANP e/ou ao Inmetro para uso de **tecnologias alternativas e inovadoras**, desde que apresente justificativa técnica e descrição detalhada do sistema.

No caso citado de medição multifásica, o texto acadêmico conclui que a Portaria não a previa explicitamente para apropriação, mas também não a vedava de forma absoluta, ficando sua utilização dependente de autorização específica e documentação técnica adicional.

**Implicação para a faceta de projeto/instalação:** soluções fora do arranjo convencional aceito não devem ser tratadas como conformes por equivalência presumida. A conformidade depende de autorização formal e de dossiê técnico robusto.

**Fontes da seção:** `petroles-004c2afadba7ea17c7dd7908:pNone:1185382.0-1185418.0`

## 11. Síntese objetiva para avaliação de conformidade técnica
Em uma análise profissional de projeto e instalação de medição fiscal e de transferência de custódia em FPSOs, os principais verificadores derivados dos trechos são:

1. **Finalidade metrológica corretamente definida**: fiscal, apropriação, operacional ou transferência de custódia.
2. **Ponto de medição corretamente localizado** em relação a separação, tratamento, tancagem, condicionamento e etapas posteriores.
3. **Tecnologia de medição compatível** com o fluido e com o tipo de medição aceito pelo arcabouço regulatório reproduzido.
4. **Instrumentação auxiliar completa**: pressão, temperatura, amostragem e compensações necessárias.
5. **Estratégia de calibração e prova prevista no projeto**, com sistema aprovado/autorizado e rastreável.
6. **Fluido em condição compatível com medição fiscal/custódia**, inclusive quanto à estabilização do petróleo e ao tratamento de BSW.
7. **Computação e armazenamento de dados auditáveis**, com proteção, rastreabilidade e possibilidade de correção.
8. **Documentação de engenharia suficiente para aprovação e inspeção** pela ANP.
9. **Tratamento conservador de exceções e tecnologias alternativas**, sempre sujeito a autorização formal.

**Fontes da seção:** consolidação de todas as fontes listadas acima.