# Flaring, venting e perdas na operação de FPSOs

## 1. Enquadramento da faceta
Nesta faceta, o foco é o **controle operacional de emissões e perdas associadas ao sistema de alívio** em FPSOs, incluindo liberações para flare, venting direto e perdas de hidrocarbonetos ligadas a despressurizações, partidas, paradas, armazenamento e vazamentos. O material disponível é predominantemente bibliográfico e de inventário de emissões; portanto, a discussão abaixo deve ser lida como **base técnica de apoio**, e não como procedimento normativo ou certificação de conformidade.

*Fontes: `regis-6a1c29eb52a777ec29879fba:pNone:3413.0-3605.0`, `regis-6a1c29eb52a777ec29879fba:pNone:3607.0-3778.0`, `regis-ef7d62eda3748119ba3e9e9e:pNone:7709.0-7954.0`*

## 2. Classes de emissão relevantes para o sistema de alívio
Segundo a classificação citada pelo API (2004) na fonte, as emissões na indústria de óleo e gás podem ser organizadas em três classes gerais:

### 2.1 Fontes de combustão
São emissões oriundas da queima de combustíveis em equipamentos como motores, queimadores, fornos, caldeiras e **tochas**. A combustão gera principalmente **CO2** pela oxidação do carbono, além de pequenas quantidades de **N2O** e, em caso de combustão incompleta, traços de **CH4** nos gases de exaustão.

Para a operação de FPSO, isso significa que o próprio **flare** entra na categoria de fonte de combustão quando há queima do gás aliviado.

### 2.2 Fontes de processo
São liberações resultantes de operações normais ou inerentes ao processamento. A fonte consultada inclui nessa classe:

- estocagem e transporte de petróleo e derivados;
- equipamentos pneumáticos que liberam gás como parte da operação;
- bombas de injeção de químicos;
- etapas de processamento de gás;
- despressurizações para manutenção ou atividades intermitentes;
- emissões de partida de equipamentos;
- purgas antes da pressurização;
- liberações não-rotineiras de emergência;
- descargas de emergência, válvulas e tanques de alívio de pressão.

Ou seja, parte importante das emissões associadas ao sistema de alívio não é necessariamente "fugitiva": muitas são **emissões de processo**, porque decorrem da forma como a unidade é operada em eventos planejados ou contingenciais.

### 2.3 Fontes fugitivas
São liberações **não intencionais** por vazamentos de equipamentos e superfícies seladas. Exemplos citados:

- válvulas;
- flanges;
- selos de bombas;
- selos de compressores;
- conexões de amostragem;
- outras superfícies seladas sujeitas a desgaste ao longo do tempo.

Também podem incluir fontes evaporativas não pontuais, como tratamento de efluentes líquidos, manuseio de sólidos e lodos e torres de resfriamento.

Para a operação de FPSO, essa distinção é importante porque o controle de perdas depende de **separar o que é evento operacional esperado** do que é **vazamento evitável por integridade e manutenção**.

*Fontes: `regis-6a1c29eb52a777ec29879fba:pNone:3413.0-3605.0`*

## 3. Flaring e venting: diferença técnica e implicações operacionais
Quando o óleo bruto é produzido, o **gás associado** normalmente vem junto. Se houver limitação de infraestrutura para o gás, distância de mercado consumidor ou baixa viabilidade econômica para aproveitamento, parte desse gás pode ser:

- liberada **sem queima**: **venting**;
- liberada **com queima**: **flaring**.

A diferença ambiental central destacada nas fontes é a seguinte:

- o gás natural é constituído majoritariamente por **metano (CH4)**;
- no **venting**, esse CH4 é lançado diretamente à atmosfera;
- no **flaring**, o metano é convertido predominantemente em **CO2** por combustão.

A referência citada informa que, para horizonte de 100 anos, o potencial de aquecimento global do CH4 foi tomado como **21 vezes** o do CO2. Assim, **venting tende a ser climaticamente mais danoso que flaring**, embora o flare continue sendo uma fonte relevante de emissão de CO2 e represente perda do conteúdo energético do gás produzido.

Do ponto de vista operacional, isso leva a uma lógica de controle:

1. **evitar venting sempre que a configuração e a segurança permitirem**;
2. **evitar flaring desnecessário**, porque ele continua sendo emissão atmosférica e perda energética;
3. **maximizar o aproveitamento do gás** quando houver rota operacional para uso, tratamento ou geração de energia.

As fontes também observam que as operações offshore são semelhantes às onshore quanto aos processos, embora emissões de CH4 de processo e fugitivas possam ser, em termos gerais, menores em plataformas devido às restrições de espaço e de arranjo operacional.

*Fontes: `regis-6a1c29eb52a777ec29879fba:pNone:3512.0-3689.0`, `regis-6a1c29eb52a777ec29879fba:pNone:3607.0-3778.0`*

## 4. Onde surgem as emissões e perdas associadas ao sistema de alívio em um FPSO
O material permite identificar vários mecanismos relevantes para o controle operacional.

### 4.1 Despressurizações e blowdowns para manutenção ou atividades intermitentes
A despressurização de equipamentos para manutenção é explicitamente citada como fonte frequente de emissão de processo. O mesmo vale para atividades intermitentes que exigem remoção de inventário gasoso.

Implicação prática: esses eventos devem ser tratados como **perdas operacionais contabilizáveis**, e não como ruído inevitável do processo.

### 4.2 Partidas, paradas e purgas
Partidas de equipamentos e purgas antes da pressurização também podem gerar emissões. Em FPSOs, isso é particularmente relevante em:

- retomadas após manutenção;
- reconfiguração de trens de processo;
- preparação de linhas e vasos para retorno à operação.

Em termos de inventário e controle, partidas e purgas precisam aparecer separadamente porque podem elevar emissões mesmo quando não há falha de integridade.

### 4.3 Eventos de emergência e atuação de equipamentos de alívio
A fonte inclui como emissões de processo:

- paradas de emergência;
- descargas de emergência;
- válvulas de alívio de pressão;
- tanques de alívio de pressão.

Esses eventos estão diretamente ligados ao sistema de alívio. Portanto, para fins operacionais, a análise de emissões não deve olhar apenas para o flare contínuo ou para venting rotineiro: deve também registrar **eventos episódicos de alta vazão** associados a proteção da planta.

### 4.4 Tratamento de gás e dispositivos pneumáticos
Operações de separação óleo/gás e tratamento de gás podem resultar em perdas de CH4 em:

- tanques;
- desidratadores;
- unidades de amina;
- dispositivos pneumáticos.

Isso é importante porque parte das emissões atribuídas genericamente ao "sistema de alívio" pode, na realidade, ter origem em **venting de processo** ou em usos operacionais do gás em instrumentos e sistemas auxiliares.

### 4.5 Coleta, armazenamento e perdas em tanques
A coleta e o armazenamento do óleo produzido envolvem tubulações fechadas interligadas a tanques. As fontes citam três mecanismos relevantes:

- **perdas por trabalho** (*working losses*): durante enchimento e esvaziamento;
- **perdas em estagnação** (*standing* ou *breathing losses*): durante estocagem, por variações de temperatura;
- **perdas por expansão** (*flashing losses*): quando óleo cru pressurizado entra em tanque normalmente próximo à pressão atmosférica.

No contexto de produção, as **perdas por expansão** são apontadas como geralmente mais significativas para emissões de CH4 do que as perdas normais por trabalho e estagnação.

### 4.6 Emissões fugitivas na malha de coleta e compressão
As fontes citam como potenciais emissores:

- vazamentos de equipamentos;
- válvulas;
- flanges;
- selos de bombas e compressores;
- dispositivos pneumáticos acionados por gás.

Essas perdas não passam necessariamente pelo flare ou pelo sistema formal de alívio, mas concorrem para o mesmo problema operacional: **liberação de hidrocarbonetos à atmosfera** e perda de inventário energético.

*Fontes: `regis-6a1c29eb52a777ec29879fba:pNone:3413.0-3605.0`, `regis-6a1c29eb52a777ec29879fba:pNone:3607.0-3778.0`*

## 5. Critérios de controle operacional das emissões e perdas
Com base nas categorias e mecanismos acima, o controle operacional em FPSO pode ser estruturado em linhas de decisão.

### 5.1 Separar o que é combustão, processo e fuga
Misturar todas as emissões sob o rótulo "flare" distorce a análise. Para tomada de decisão, convém distinguir:

- **CO2 de combustão**: motores, turbinas, caldeiras e tocha;
- **CH4 de venting/processo**: purgas, despressurizações, tratamento de gás, pneumáticos;
- **CH4/COV de perdas fugitivas e de armazenamento**: válvulas, flanges, selos, tanques.

Essa separação é necessária porque ações corretivas diferentes atacam causas diferentes.

### 5.2 Tratar venting como ponto crítico climático
Como o CH4 possui potencial de aquecimento global muito superior ao do CO2 na referência usada, o venting deve ser visto como ponto crítico de controle, especialmente quando repetitivo ou operacionalmente recorrente.

### 5.3 Registrar eventos episódicos, não apenas taxas médias
A própria fonte ressalta que emissões de despressurização, emergência e equipamentos de alívio são difíceis de determinar e devem ser avaliadas **caso a caso**, por combinação de fatores de emissão e cálculos de engenharia.

Logo, o controle não deve se limitar a médias mensais agregadas; ele precisa rastrear ao menos:

- partidas;
- paradas;
- purgas;
- despressurizações para manutenção;
- atuações de válvulas/sistemas de alívio;
- descargas de emergência.

### 5.4 Incluir perdas em tanques e armazenamento no balanço operacional
Em FPSOs, perdas associadas ao armazenamento de óleo não podem ser tratadas como secundárias por definição. A fonte destaca que perdas por expansão de óleo pressurizado para tanque atmosférico podem ser mais relevantes para CH4 que perdas normais de respiração do tanque.

### 5.5 Integrar operação e integridade
Parte importante das emissões é fugitiva. Assim, o desempenho ambiental e o controle de perdas dependem de:

- integridade de válvulas, flanges e selos;
- condição de selos de bombas e compressores;
- gestão de dispositivos pneumáticos acionados por gás;
- identificação de vazamentos em linhas e conexões de amostragem.

Em outras palavras, **controle operacional de emissões** e **confiabilidade mecânica** são temas inseparáveis.

*Fontes: `regis-6a1c29eb52a777ec29879fba:pNone:3413.0-3605.0`, `regis-6a1c29eb52a777ec29879fba:pNone:3607.0-3778.0`*

## 6. Exemplo útil para tomada de decisão: cenário com uso do gás na cogeração
Um estudo de caso de planta offshore genérica citado nas fontes avaliou processos internos como separação, tratamento de óleo, tratamento de água, tratamento de gás, geração de energia e flare. No cenário em que o **gás natural é utilizado na cogeração de energia**, a **queima em flare** aparece restrita a:

- situações de emergência; e
- queima de gás excedente.

Nesse cenário específico, a contribuição do flare para o total das emissões atmosféricas foi considerada **desprezível** frente aos demais sistemas.

Ao mesmo tempo, o mesmo estudo indica que os principais pesos ambientais podem estar em outros pontos da planta:

- **Geração de energia** dominando emissões de CO, N2O e NO2, além de parcela importante de material particulado, THC e CO2;
- **Tratamento de gás** concentrando a maior parte do CH4, atribuída principalmente ao **venting**;
- **Tratamento de óleo/armazenagem** concentrando emissões orgânicas voláteis.

A conclusão operacional útil é a seguinte: **reduzir flare não equivale, por si só, a controlar as principais perdas e emissões da unidade**. Em certos arranjos de FPSO, o foco mais efetivo pode estar em:

- reduzir venting no tratamento de gás;
- controlar emissões de tanques e armazenamento de óleo;
- reduzir vazamentos fugitivos;
- melhorar o aproveitamento energético do gás produzido.

*Fontes: `regis-ef7d62eda3748119ba3e9e9e:pNone:7709.0-7954.0`*

## 7. Síntese técnica para operação de FPSO
Para avaliação profissional da operação geral de FPSOs sob a ótica de **flaring, venting e perdas**, as ideias centrais são:

1. **Nem toda emissão associada ao sistema de alívio é flare**; muitas são emissões de processo e fugitivas.
2. **Venting de gás natural é particularmente crítico** por lançar CH4 diretamente à atmosfera.
3. **Flaring continua sendo perda energética e fonte de CO2**, embora possa ser menos danoso climaticamente que o venting do ponto de vista do CH4.
4. **Partidas, purgas, despressurizações, emergências e armazenamento** são eventos-chave para o inventário de emissões.
5. **Perdas em tanques**, especialmente por expansão de óleo pressurizado, podem ser relevantes.
6. **Integridade de equipamentos** é parte do controle ambiental, porque vazamentos fugitivos de válvulas, flanges, selos e pneumáticos afetam diretamente as perdas.
7. **A priorização operacional deve ser orientada por inventário e análise caso a caso**, porque as taxas de emissão de eventos de alívio e emergência são de difícil determinação por fator único.

*Fontes: `regis-6a1c29eb52a777ec29879fba:pNone:3413.0-3605.0`, `regis-6a1c29eb52a777ec29879fba:pNone:3607.0-3778.0`, `regis-ef7d62eda3748119ba3e9e9e:pNone:7709.0-7954.0`*