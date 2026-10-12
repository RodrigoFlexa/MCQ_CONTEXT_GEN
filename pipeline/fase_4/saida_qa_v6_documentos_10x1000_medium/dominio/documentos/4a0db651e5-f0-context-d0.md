# Seleção da tecnologia de detecção em sistemas F&G

## 1. Finalidade da seleção tecnológica
A seleção da tecnologia de detecção em um sistema de Fogo e Gás (F&G) para FPSO/FSO não deve ser tratada como escolha genérica por catálogo. O sistema precisa ser específico para a instalação, para os perigos realmente presentes e para a forma como a planta opera, ventila, libera inventário e é mantida ao longo do ciclo de vida. Na prática, a escolha do detector decorre da combinação entre:

- tipo de perigo: gás inflamável, gás tóxico, chama, fumaça, calor, névoa/óleo, vazamento pressurizado;
- cenário de liberação: vazamento localizado, jato pressurizado, nuvem em área aberta, acúmulo em bolso, dispersão em módulo congestionado, passagem por dutos;
- características ambientais: ventilação natural ou mecânica, áreas abertas ou abrigadas, névoa, chuva, condensação, reflexos, umidade, ruído de fundo, acesso difícil e severidade offshore;
- desempenho necessário: cobertura, tempo de resposta, suscetibilidade a falso alarme, mantenabilidade, robustez e capacidade de autodiagnóstico.

Em ambiente offshore, a seleção também deve considerar restrições logísticas e de manutenção: acesso difícil, alto custo de reposição, maior agressividade ambiental e maior criticidade de indisponibilidade. Por isso, os trechos consultados sustentam que CAPEX isolado não é critério suficiente para definir tecnologia de detecção; qualidade, endurance, mantenabilidade e aplicabilidade tendem a ser mais relevantes para sistemas relacionados à segurança de vida.

**Fontes:** `petroles-004c2afadba7ea17c7dd7908:pNone:531993.0-532054.0`, `petroles-004c2afadba7ea17c7dd7908:pNone:532055.0-532109.0`

## 2. Premissas de engenharia que orientam a escolha
A seleção deve ser amarrada à análise de riscos e ao entendimento da instalação como um sistema integrado. Os materiais apontam, em especial, para as seguintes premissas:

1. **Partir da avaliação de vazamentos e do arranjo físico dos equipamentos.** A disposição dos equipamentos e as fontes prováveis de vazamento influenciam tanto a localização quanto a tecnologia.
2. **Levar em conta o regime de ventilação e dispersão.** A eficiência de detectores de gás por concentração local depende fortemente do movimento do ar; detectores por linha de visada/caminho aberto tendem a oferecer cobertura mais ampla.
3. **Não assumir que um detector "mede bem" em campo apenas porque responde bem na calibração.** O desempenho real depende da forma de chegada da nuvem ao sensor.
4. **Considerar mantenabilidade e autodiagnóstico como critério de seleção.** Para detectores de gás, leitura zero pode significar ausência de gás ou falha do sensor; por isso, a capacidade de discriminar falha do elemento sensor é importante.
5. **Incluir robustez elétrica e de instalação.** Os trechos de Petrolês chamam atenção para problemas de aterramento, eventos de energização/desenergização e necessidade de proteção elétrica adequada em campo.

Do ponto de vista de unidade medida, o material consultado mostra que diferentes tecnologias não entregam a mesma variável:

- detectores por concentração local para inflamáveis: tipicamente em **%LEL**;
- detectores tóxicos: usualmente em **ppm** e, em algumas aplicações, **ppb**;
- detectores open path/beam: medida integrada ao longo do caminho, como **%LEL·m**;
- detecção acústica: **dB** ou parâmetros derivados por algoritmo do fabricante.

Essa diferença é relevante porque a lógica de proteção deve ser compatível com a variável física medida.

**Fontes:** `petroles-004c2afadba7ea17c7dd7908:pNone:532083.0-532142.0`, `petroles-004c2afadba7ea17c7dd7908:pNone:532912.0-532945.0`, `hse-48d901a1fbf08e9f46bb522f:p17-20:10.0-20.0`

## 3. Tecnologias para detecção de gases inflamáveis e tóxicos

### 3.1 Visão comparativa das tecnologias citadas
| Tecnologia | Princípio indicado no material | Uso típico indicado | Pontos fortes destacados | Limitações/condições destacadas |
|---|---|---|---|---|
| Eletroquímica | Reação à presença do gás | Gases tóxicos; detectores pontuais e portáteis | Aplicável a tóxicos | Vida limitada; envelhecimento do sensor |
| Catalítica | Reação à presença do gás | Combustíveis e H2; detectores pontuais e portáteis | Tecnologia tradicional | Requer presença de oxigênio; vida limitada |
| Infravermelho pontual | Absorção de gás | Combustíveis; detectores pontuais e portáteis | Maior durabilidade; em estudo citado teve melhor desempenho que catalítico | Continua dependente do encontro da nuvem com o ponto de medição |
| Laser frequência única | Absorção de gás em open path/portátil | Combustíveis | Aplicável em caminho aberto | Fonte consultada atribui baixa sensibilidade por necessidade de alto offset |
| Laser multifrequência | Absorção de gás em open path | Combustíveis e tóxicos | Potencial para melhor discriminação entre espécies e menor interferência | Trecho disponível tem caráter parcialmente promocional; requer validação caso a caso |
| PID | Fotoionização / mudança de condutividade no trecho | Compostos orgânicos voláteis | Útil para orgânicos voláteis | Não é tecnologia típica de proteção primária para todo cenário F&G offshore |
| "Eletrônico" para H2S | Reação à presença do gás | H2S; detector pontual | Aplicação para H2S citada | Sensibilidade à alta umidade; nomenclatura do tipo sensor é ambígua no trecho |

Além dessa comparação geral, a evidência da HSE aponta que, em testes de configuração de detectores em módulos naturalmente ventilados, **detectores IR pontuais apresentaram desempenho melhor que os catalíticos** em número de liberações detectadas e em tempo de detecção, e que **detectores IR beam/open path** tiveram bom desempenho quando comparados a fileiras de detectores pontuais IR.

**Fontes:** `petroles-004c2afadba7ea17c7dd7908:pNone:532055.0-532109.0`, `hse-48d901a1fbf08e9f46bb522f:p17-20:10.0-20.0`

### 3.2 Detectores pontuais: quando tendem a ser mais adequados
Os materiais sugerem que detectores pontuais são mais aderentes quando há possibilidade razoável de a nuvem atingir o sensor por concentração local, por exemplo:

- áreas com **bolsões de gás** ou tendência de acúmulo;
- módulos com **congestionamento** e algum grau de confinamento;
- regiões sujeitas a **slumping** de vapores densos e frios, onde a nuvem desce e permanece em níveis baixos;
- pontos específicos próximos a fontes de vazamento conhecidas, desde que o regime de ventilação permita interceptação.

A HSE destaca que o espaçamento e a cobertura dos detectores pontuais dependem de:

- tamanho e geometria da área;
- confinamento e congestionamento;
- ventilação;
- natureza da liberação.

Em módulos com tendência a slumping de vapores, os cabeçotes devem ser distribuídos em padrão tridimensional, incluindo níveis baixos. Em áreas congestionadas, a referência consultada menciona **malha típica mínima de cerca de 5 m**, com o cuidado de que esse valor não é universal.

Os trechos de Petrolês acrescentam uma observação de campo importante: em instalações externas e ventiladas, especialmente sob vento, o detector pontual pode responder mais lentamente do que o sugerido em ensaios de calibração, porque a nuvem pode não entrar adequadamente no volume de amostragem do sensor. Assim, para área aberta e muito ventilada, detector pontual isolado pode ser inadequado como principal meio de detecção de um vazamento dispersivo.

**Fontes:** `petroles-004c2afadba7ea17c7dd7908:pNone:532055.0-532109.0`, `hse-48d901a1fbf08e9f46bb522f:p15-18:28.0-21.0`, `hse-48d901a1fbf08e9f46bb522f:p17-20:10.0-20.0`

### 3.3 Detectores open path / beam: quando tendem a ser mais adequados
Os materiais consultados convergem para a utilidade de detectores por caminho aberto ou feixe em cenários nos quais se deseja cobrir **maior volume ou largura efetiva de área**, principalmente quando a ventilação reduz a probabilidade de uma nuvem encontrar um sensor pontual.

Aplicações favorecidas pelos trechos:

- **áreas externas abertas**;
- regiões em que se pretende interceptar a passagem de nuvens ao longo de um corredor ou frente de dispersão;
- **dutos de HVAC**, onde a HSE informa que detectores ponto ou beam podem ser usados, mas beam tende a fornecer cobertura mais transversal do duto.

Entretanto, a seleção de open path precisa levar em conta limitações importantes:

- suscetibilidade a **luz solar de baixa geometria**, **neblina/condensação** e **reflexos**;
- possibilidade de interferência por **CO2**, **névoa**, **vapor** e outros constituintes atmosféricos, conforme relato de Petrolês para algumas tecnologias IR/open path;
- necessidade de compatibilizar a variável medida (**%LEL·m**) com a filosofia de alarme e com a interpretação do perigo real, relação que a HSE classifica como ainda não completamente compreendida;
- alinhamento mecânico e confiabilidade do arranjo emissor-receptor, quando aplicável.

Os trechos de Petrolês diferenciam ainda tecnologias open path de frequência única e multifrequência a laser, atribuindo à multifrequência melhor capacidade de distinguir gases de absorção espectral próxima e menor suscetibilidade a falso alarme. Como o material disponível tem forte caráter opinativo/comercial e contém OCR ruidoso, esse ponto deve ser interpretado como **direção de seleção** e não como comprovação definitiva de desempenho.

**Fontes:** `petroles-004c2afadba7ea17c7dd7908:pNone:532055.0-532109.0`, `petroles-004c2afadba7ea17c7dd7908:pNone:532083.0-532142.0`, `hse-48d901a1fbf08e9f46bb522f:p15-18:28.0-21.0`, `hse-48d901a1fbf08e9f46bb522f:p17-20:10.0-20.0`

### 3.4 Seleção específica para gases tóxicos, incluindo H2S
Para gases tóxicos, os trechos citam principalmente:

- **eletroquímicos** para detecção pontual de tóxicos;
- tecnologias open path a **laser multifrequência** como possibilidade para alguns tóxicos, inclusive H2S, amônia e HF, segundo o material de Petrolês;
- uma tecnologia denominada no texto como **"eletrônica"** aplicada a H2S, com limitação por alta umidade.

Da comparação disponível, algumas implicações práticas podem ser extraídas:

1. **Se o objetivo é detectar exposição/localização de vazamento em ponto específico ou área ocupada**, detectores pontuais de tóxicos permanecem coerentes, desde que a vida útil e a degradação do sensor sejam geridas.
2. **Se o cenário é área aberta com necessidade de interceptar pluma ao longo de um trajeto**, tecnologias open path específicas para tóxicos podem ser consideradas, desde que haja validação para o gás de interesse, para o ambiente e para a estratégia de manutenção.
3. **Alta umidade e condensação** são fatores de seleção relevantes, porque podem degradar ou interferir em certos princípios de medição.

**Fontes:** `petroles-004c2afadba7ea17c7dd7908:pNone:532055.0-532109.0`, `petroles-004c2afadba7ea17c7dd7908:pNone:532083.0-532142.0`

## 4. Tecnologias complementares ou de apoio diagnóstico
Os materiais incluem tecnologias úteis para identificação de vazamentos, mas que não devem ser automaticamente tratadas como substitutas de uma malha fixa clássica de F&G em FPSO/FSO.

### 4.1 Detecção acústica de vazamentos
A detecção acústica identifica o ruído gerado por vazamento de gás pressurizado em componente, decorrente do escoamento turbulento através de uma abertura. Segundo os trechos consultados:

- é particularmente aplicável a **componentes de tubulação** e **pontos de união** em instalações de gás de alta pressão;
- a localização deve partir da identificação das **fontes potenciais de vazamento**;
- pode ser útil em ambientes de maior ruído, mas exige conhecimento do **ruído de fundo**;
- reflexões acústicas podem gerar **falsos alarmes**;
- a variável medida é acústica, não concentração; a relação entre **dB** e perigo inflamável efetivo não é plenamente consolidada;
- tende a ser uma tecnologia **complementar**, especialmente valiosa quando a liberação pressurizada pode não formar imediatamente uma nuvem concentrada sobre um sensor por concentração.

Para seleção em F&G, ela faz mais sentido como reforço em sistemas de gás de alta pressão do que como substituta universal de detectores de concentração.

**Fontes:** `regis-67642b2b68bab45b898ee0a3:pNone:3563.0-3791.0`, `regis-67642b2b68bab45b898ee0a3:pNone:3673.0-3913.0`, `hse-48d901a1fbf08e9f46bb522f:p15-18:28.0-21.0`, `hse-48d901a1fbf08e9f46bb522f:p17-20:10.0-20.0`

### 4.2 OGI - Optical Gas Imaging
OGI usa câmera sensível na faixa infravermelha para visualizar plumas de determinados compostos. Pelas fontes:

- é útil para **grandes vazamentos de hidrocarbonetos** e áreas de **difícil acesso**;
- pode ser aplicada a fontes pontuais e áreas;
- permite visualização e gravação de imagens;
- **não quantifica nem especia** adequadamente os compostos em todas as situações;
- seus limites de detecção e sensibilidade não são totalmente conhecidos.

Logo, OGI é melhor entendida como ferramenta de **inspeção, confirmação ou apoio operacional**, e não como base única de disparo automático de funções instrumentadas de segurança.

**Fontes:** `regis-67642b2b68bab45b898ee0a3:pNone:3563.0-3791.0`, `regis-67642b2b68bab45b898ee0a3:pNone:3673.0-3913.0`

### 4.3 UV-DOAS, OP-FTIR/RPM, SOF/DIAL e tecnologias de pluma/perímetro
Os trechos de REGIS descrevem tecnologias ópticas de caminho aberto e de pluma voltadas principalmente para:

- monitoramento de **cerca/perímetro**;
- detecção de **grandes emissores em fontes área**;
- cálculo de fluxo de emissões com apoio de velocidade do vento.

As próprias fontes ressaltam que essas tecnologias **não são aplicáveis à detecção de emissões de componentes individuais de linhas de processo**. Portanto, seu papel é mais coerente em monitoramento ambiental, emissões fugitivas em larga escala ou campanhas específicas, e não como primeira linha de defesa para detecção pontual de vazamentos de processo em um F&G embarcado.

**Fontes:** `regis-67642b2b68bab45b898ee0a3:pNone:3563.0-3791.0`, `regis-67642b2b68bab45b898ee0a3:pNone:3673.0-3913.0`

## 5. Seleção de tecnologias para fogo, chama, fumaça e calor
O material fornecido é menos detalhado para chama/fumaça/calor do que para gás, mas ainda permite algumas conclusões úteis.

### 5.1 Detectores de chama
A HSE informa que o fogo pode ser detectado por radiação na faixa **UV, visível e IR**, e que sistemas atuais de detecção de fogo, em geral, são confiáveis e eficazes. Para detectores de chama por IR:

- o posicionamento deve garantir que o **cone de visão** cubra as áreas onde o fogo pode ocorrer;
- cerca de **15 m** é citado como alcance razoável para detectores de chama IR, em razão de obscurecimento por fumaça e redução de sensibilidade nas bordas do campo de visão;
- detectores são frequentemente posicionados nos **cantos** de uma área ou módulo;
- sistemas **triple-band IR** são menos propensos a falsos alarmes.

Assim, na seleção tecnológica, detectores de chama ganham atratividade quando se deseja independência do transporte convectivo de fumaça e quando há boa linha de visada para o cenário de incêndio esperado.

### 5.2 Detectores de calor
Os detectores pontuais de calor, segundo a HSE:

- em áreas abertas e naturalmente ventiladas, são citados com densidade aproximada de **1 por 25 m²**, espaçamento de **7 m** e distância máxima de **3,5 m** de anteparos;
- em módulos enclausurados com ventilação mecânica, cerca de **1 por 37 m²**, espaçamento de **9 m** e distância máxima de **4,5 m** de anteparos;
- **não são adequados para tetos altos**, acima de cerca de **8 m**, devido à perda de sensibilidade com a altura.

Portanto, sua seleção depende fortemente de geometria e altura do espaço, e não é apropriada para qualquer volume aberto alto.

### 5.3 Detectores de fumaça
Os detectores pontuais de fumaça dependem do transporte convectivo dos produtos de combustão até o sensor. A HSE registra que:

- os detectores atuais são posicionados com afastamento de cerca de **7,5 m**;
- não são apropriados para **tetos altos** acima de aproximadamente **10,5 m**;
- a resposta depende do transporte dos produtos da combustão, ao contrário de detectores de chama, que não dependem da ventilação da mesma forma.

Em seleção tecnológica, isso significa que fumaça pontual tende a ser mais adequada em áreas fechadas ou controladas, nas quais a convecção leve os produtos ao detector em tempo útil.

**Fontes:** `hse-48d901a1fbf08e9f46bb522f:p15-18:28.0-21.0`

## 6. Critérios práticos de escolha por cenário

### 6.1 Área externa aberta e ventilada, com risco de nuvem inflamável dispersiva
Tende a favorecer:

- **open path / beam** para cobertura mais ampla da trajetória provável da nuvem;
- eventual combinação com **acústico** se houver linhas de alta pressão e interesse em detectar ruído de vazamento antes de formação significativa de nuvem;
- uso de **pontuais** apenas onde existam bolsões, recantos, depressões ou trajetórias preferenciais de acúmulo.

### 6.2 Módulo congestionado ou parcialmente confinado
Tende a favorecer:

- **detectores pontuais**, preferencialmente com tecnologia robusta ao ambiente e ao regime de manutenção;
- distribuição em **3D**, inclusive em nível baixo quando houver possibilidade de vapores densos/slumping;
- eventual reforço com **beam** quando a geometria permitir cobertura integrada útil.

### 6.3 Sistema de gás de alta pressão, com possibilidade de jato pressurizado
Tende a favorecer combinação de:

- **concentração** (pontual e/ou beam), para detecção da nuvem;
- **acústico**, para capturar o fenômeno de vazamento pressurizado junto a conexões e componentes críticos.

### 6.4 Risco tóxico localizado, especialmente em área ocupada
Tende a favorecer:

- **detectores pontuais eletroquímicos** próximos às fontes prováveis e zonas de exposição;
- atenção reforçada à **vida útil do sensor**, degradação e umidade;
- open path específico para tóxicos apenas quando o cenário de dispersão e a tecnologia forem adequadamente validados.

### 6.5 HVAC e dutos
A HSE admite detectores ponto ou beam em dutos, com observação de que beam tende a oferecer melhor cobertura transversal do duto.

### 6.6 Inspeção complementar, áreas de difícil acesso e confirmação visual
Tendem a favorecer:

- **OGI** como ferramenta complementar;
- tecnologias de **pluma/perímetro** para monitoramento ambiental ou campanhas, não para substituir o F&G de proteção imediata.

**Fontes:** `petroles-004c2afadba7ea17c7dd7908:pNone:532055.0-532109.0`, `petroles-004c2afadba7ea17c7dd7908:pNone:532083.0-532142.0`, `hse-48d901a1fbf08e9f46bb522f:p15-18:28.0-21.0`, `hse-48d901a1fbf08e9f46bb522f:p17-20:10.0-20.0`, `regis-67642b2b68bab45b898ee0a3:pNone:3563.0-3791.0`, `regis-67642b2b68bab45b898ee0a3:pNone:3673.0-3913.0`

## 7. Limitações e incertezas técnicas explicitadas nas fontes
As próprias fontes reconhecem pontos de incerteza relevantes para a seleção de tecnologia e interpretação de desempenho:

- a combinação ótima entre detectores **pontuais, beam e acústicos** ainda carece de guias detalhados e consolidados;
- a localização mais eficaz para diferentes tipos de liberação — por exemplo, **metano, propano e condensados** — não está totalmente definida;
- há pouca informação sobre eficácia de detecção para **liberações de baixa taxa** que se tornam relevantes ao longo do tempo;
- a resposta de instrumentos calibrados para **metano** quando expostos a hidrocarbonetos mais pesados não é bem definida;
- a relação entre **%LEL·m** ou **dB** e o perigo inflamável efetivo ainda não é completamente compreendida;
- dados históricos citados pela HSE indicaram taxa de detecção efetiva relativamente limitada em conjunto amplo de instalações, o que reforça que seleção e posicionamento inadequados reduzem o valor da barreira.

Essas limitações reforçam que a seleção tecnológica precisa ser acompanhada por análise de dispersão/ventilação, cenários de liberação e revisão crítica do arranjo de detectores, em vez de mera adoção de padrões genéricos.

**Fontes:** `hse-48d901a1fbf08e9f46bb522f:p15-18:28.0-21.0`, `hse-48d901a1fbf08e9f46bb522f:p17-20:10.0-20.0`

## 8. Síntese decisória
Em termos práticos, a seleção da tecnologia de detecção em F&G pode ser resumida assim:

- **Ponto**: melhor para concentração local, bolsões, congestionamento, módulos e fontes conhecidas; perde efetividade quando a ventilação impede o encontro da nuvem com o sensor.
- **Beam / open path**: melhor para área aberta, cobertura ampla, corredores de dispersão e dutos; requer maior cuidado com interferências ópticas e interpretação da grandeza integrada.
- **IR pontual**: nas evidências citadas, tende a superar catalítico em desempenho de detecção e durabilidade.
- **Catalítico**: continua sendo tecnologia clássica, mas exige oxigênio e tem vida limitada.
- **Eletroquímico**: referência principal para tóxicos, com atenção à vida útil e condições ambientais.
- **Acústico**: reforço útil para vazamentos pressurizados, especialmente em alta pressão; não substitui medição de concentração.
- **OGI e tecnologias de pluma/perímetro**: úteis como apoio diagnóstico, inspeção e monitoramento ambiental; em regra, não substituem a malha fixa de F&G para proteção de processo.
- **Chama/fogo**: detectores de chama por linha de visada e multi-IR ganham relevância quando se quer independência da convecção; calor e fumaça têm limitações geométricas e de altura mais pronunciadas.

**Fontes:** `petroles-004c2afadba7ea17c7dd7908:pNone:531993.0-532054.0`, `petroles-004c2afadba7ea17c7dd7908:pNone:532055.0-532109.0`, `petroles-004c2afadba7ea17c7dd7908:pNone:532083.0-532142.0`, `hse-48d901a1fbf08e9f46bb522f:p15-18:28.0-21.0`, `hse-48d901a1fbf08e9f46bb522f:p17-20:10.0-20.0`, `regis-67642b2b68bab45b898ee0a3:pNone:3563.0-3791.0`, `regis-67642b2b68bab45b898ee0a3:pNone:3673.0-3913.0`