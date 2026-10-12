# Rede de água e bombeamento

## 1. Função técnica da rede de água de incêndio e limite do material
A rede de água de combate a incêndio existe para entregar **vazão e pressão suficientes no ponto de uso**, durante o cenário acidental considerado, de modo a permitir ataque ao fogo, resfriamento de equipamentos expostos e redução do potencial de escalonamento. Nos trechos utilizados, a água aparece principalmente como agente de **resfriamento** e, em menor medida, de **abafamento** quando convertida em vapor; isso explica por que o dimensionamento hidráulico não pode ser tratado apenas como transporte de fluido, mas como requisito direto de desempenho do sistema de emergência.  
**Fontes:** `regis-0706fb4ed5d69f422f2d0ffb:pNone:879.0-1047.0`

Os materiais disponíveis para esta faceta trazem dois tipos de evidência:
- um **exemplo de cálculo de tubulação** para hidrantes e canhão monitor em refinaria;
- uma **investigação de incidente** em plataforma, mostrando como falhas de cenário dimensionante, alimentação elétrica e acionamento de dilúvio podem reduzir a disponibilidade real de água durante um incêndio.

Assim, a base técnica mais sólida aqui é: **dimensionar pela demanda do cenário** e **garantir disponibilidade sob falha e sob fogo**, e não apenas instalar bombas com capacidade nominal elevada.  
**Fontes:** `regis-0706fb4ed5d69f422f2d0ffb:pNone:879.0-1047.0`, `anp-668be0de2e3714c6db785a31:p38-43:26.0-10.0`

## 2. Base de dimensionamento hidráulico: partir do cenário e do ponto de consumo
O exemplo de refinaria mostra uma filosofia de cálculo útil: começar pelos **requisitos de vazão e pressão no consumidor final** e retroceder pela rede até a tubulação principal. O próprio texto descreve isso como “atacar o problema pela fonte”, isto é, usar uma espécie de engenharia reversa a partir da demanda no canhão/hidrante para dimensionar os trechos a montante.  
**Fontes:** `regis-0706fb4ed5d69f422f2d0ffb:pNone:879.0-1047.0`, `regis-0706fb4ed5d69f422f2d0ffb:pNone:958.0-1178.0`

No caso específico citado, o sistema deveria fornecer, **separadamente para o canhão e para os hidrantes**, uma vazão mínima de **2000 L/min (120 m³/h)** com pressão mínima de **7 kgf/cm² (700 kPa)**. Esse valor **não deve ser universalizado** para FPSOs/FSOs; ele serve como exemplo de como o projeto precisa explicitar:
- a vazão requerida por consumidor ou grupo de consumidores;
- a pressão residual mínima aceitável no ponto de uso;
- se as demandas são **alternativas** ou **simultâneas**;
- qual o caminho hidráulico mais desfavorável.  
**Fontes:** `regis-0706fb4ed5d69f422f2d0ffb:pNone:879.0-1047.0`, `regis-0706fb4ed5d69f422f2d0ffb:pNone:958.0-1178.0`

A investigação da P-20 reforça um ponto decisivo para FPSO/FSO: o sistema não pode ser avaliado só por equipamentos isolados. O **caso dimensionante** deve considerar a combinação plausível de consumidores atuando ao mesmo tempo. No estudo citado para aquela unidade, o caso dimensionante foi a abertura conjunta de **cinco válvulas de dilúvio (ADVs 50201, 50301, 50303, 50401 e 50501)** com a utilização de **dois hidrantes**, requerendo **968,64 m³/h**.  
**Fontes:** `anp-668be0de2e3714c6db785a31:p38-43:26.0-10.0`

Tecnicamente, isso significa que a disponibilidade da rede depende de três definições de projeto:
1. **quais zonas/dispositivos podem operar simultaneamente**;
2. **qual vazão total essa simultaneidade impõe**;
3. **qual pressão residual ainda precisa existir nos pontos críticos** durante essa condição.

Se o caso dimensionante for subestimado, a rede pode parecer adequada em regime nominal, mas falhar exatamente no evento real.  
**Fontes:** `anp-668be0de2e3714c6db785a31:p38-43:26.0-10.0`

## 3. Pré-dimensionamento de tubulações: relação entre vazão, velocidade e diâmetro
No exemplo de cálculo, o diâmetro do trecho secundário foi obtido a partir da relação básica entre vazão, velocidade e área:

- \(Q = V \cdot A\)
- \(A = \pi D^2 / 4\)
- portanto, \(D = \sqrt{4Q/(\pi V)}\)

onde:
- \(Q\) = vazão, em m³/s;
- \(V\) = velocidade do escoamento, em m/s;
- \(A\) = área da seção transversal, em m²;
- \(D\) = diâmetro interno hidráulico aproximado do trecho.  
**Fontes:** `regis-0706fb4ed5d69f422f2d0ffb:pNone:879.0-1047.0`, `regis-0706fb4ed5d69f422f2d0ffb:pNone:958.0-1178.0`

O trecho utilizado adotou, para água doce em instalações industriais, uma faixa de **velocidade econômica de 2 a 3 m/s** e, para a vazão de **0,033 m³/s**, usando **2 m/s**, obteve diâmetro secundário próximo de **0,146 m**, equivalente a **6”**.  
**Fontes:** `regis-0706fb4ed5d69f422f2d0ffb:pNone:879.0-1047.0`, `regis-0706fb4ed5d69f422f2d0ffb:pNone:958.0-1178.0`

### Interpretação profissional dessa etapa
Esse cálculo é um **pré-dimensionamento**. Ele serve para transformar a demanda de incêndio em um diâmetro inicial coerente com a velocidade escolhida. Para análise profissional de uma rede de FPSO/FSO, isso ajuda a responder:
- se um ramal ou trecho do fire main tem ordem de grandeza compatível com a demanda;
- se a velocidade escolhida tende a gerar perdas elevadas ou diâmetros excessivos;
- se a arquitetura da rede cria trechos restritivos que podem derrubar a pressão residual no ponto remoto.

O valor de velocidade usado no exemplo é útil como referência de cálculo, mas **não substitui a validação hidráulica do sistema completo** sob o cenário dimensionante.  
**Fontes:** `regis-0706fb4ed5d69f422f2d0ffb:pNone:879.0-1047.0`, `anp-668be0de2e3714c6db785a31:p38-43:26.0-10.0`

## 4. Integridade mecânica da tubulação como condição de disponibilidade hidráulica
Embora o foco desta faceta seja hidráulico, a fonte de cálculo lembra que a rede de incêndio não é apenas uma linha de processo: ela precisa manter desempenho em emergência e, portanto, depende também de integridade mecânica.

O exemplo menciona, para projeto de tubulações, a necessidade de calcular ao menos:
- diâmetro dos trechos;
- espessura de parede;
- pesos e carregamentos;
- vãos máximos entre suportes;
- flexibilidade e esforços.  
**Fontes:** `regis-0706fb4ed5d69f422f2d0ffb:pNone:879.0-1047.0`, `regis-0706fb4ed5d69f422f2d0ffb:pNone:958.0-1178.0`

### 4.1 Espessura de parede
O texto atribui à ANSI/ASME B31 a formulação da espessura mínima para tubos sujeitos à pressão interna, considerando pressão de projeto, diâmetro, tensão admissível do material, eficiência de solda, coeficiente de redução e margem de corrosão/erosão/rosca/chanfro. No exemplo, o cálculo resultou em **4,05 mm**, mas a exigência mínima adotada para a tubulação de **6”** levou ao uso de **Schedule 40**, com espessura de **7,11 mm**.  
**Fontes:** `regis-0706fb4ed5d69f422f2d0ffb:pNone:958.0-1178.0`

Para o sistema de água de incêndio, a leitura prática é clara: **um diâmetro hidraulicamente suficiente pode não ser mecanicamente aceitável**. Se a parede, a classe ou os acessórios não suportarem as condições previstas, a rede perde confiabilidade justamente quando solicitada.

### 4.2 Peso e suportação
O exemplo calcula o carregamento distribuído da tubulação como soma do peso do tubo com o peso da água contida, usando:
- \(q = P_t + P_a\)
- \(P_a = V \cdot \rho\)

No caso citado, obteve-se **q = 455,57 N/m**.  
**Fontes:** `regis-0706fb4ed5d69f422f2d0ffb:pNone:958.0-1178.0`

Em seguida, o texto relaciona o vão máximo admissível aos parâmetros de flecha admissida, módulo de elasticidade, momento de inércia e carregamento, chegando a **9,6 m** para o caso calculado, antes de remeter à padronização interna de suportação.  
**Fontes:** `regis-0706fb4ed5d69f422f2d0ffb:pNone:958.0-1178.0`

Em termos de disponibilidade do sistema, isso importa porque uma rede de incêndio mal suportada ou mecanicamente subdimensionada pode:
- sofrer deformação excessiva;
- comprometer alinhamento e integridade de juntas e flanges;
- aumentar o risco de indisponibilidade após vibração, choque hidráulico ou ações térmicas locais.

## 5. Bombeamento: capacidade nominal não basta, é preciso sobrevivência do arranjo
A investigação da P-20 oferece uma lição central para rede de água de incêndio em unidade offshore: **capacidade instalada de bombas não é sinônimo de água disponível no incêndio real**.  
**Fontes:** `anp-668be0de2e3714c6db785a31:p38-43:26.0-10.0`

Na unidade analisada, o sistema fixo de combate a incêndio possuía:
- **2 bombas elétricas**, cada uma com capacidade nominal de **350 m³/h**;
- **2 bombas a diesel**, cada uma com capacidade nominal de **700 m³/h**.  
**Fontes:** `anp-668be0de2e3714c6db785a31:p38-43:26.0-10.0`

Mesmo com esse arranjo, houve **redução da disponibilidade de água** durante o combate. As causas relevantes para esta faceta foram:
1. perda de sinais e abertura de válvulas de dilúvio por condição de falha;
2. partida das bombas por **pressão baixa no anel de incêndio**;
3. falha das bombas elétricas por vulnerabilidade do suprimento elétrico ao incêndio;
4. indisponibilidade adicional das bombas a diesel, investigada no mesmo evento.  
**Fontes:** `anp-668be0de2e3714c6db785a31:p38-43:26.0-10.0`

### 5.1 Partida automática por baixa pressão
O relatório registra que o sinal de **pressão baixa nos pressostatos do anel de incêndio** comandou a partida das bombas. Isso mostra uma filosofia clássica de proteção: a rede detecta queda de pressão e responde automaticamente elevando o bombeamento.  
**Fontes:** `anp-668be0de2e3714c6db785a31:p38-43:26.0-10.0`

Do ponto de vista de avaliação profissional, esse arranjo exige verificar:
- se a instrumentação de baixa pressão está posicionada e ajustada de forma compatível com a filosofia do sistema;
- se a lógica de partida automática é robusta em cenário de incêndio;
- se a rede mantém pressão adequada após partidas e após abertura simultânea de consumidores.

### 5.2 Vulnerabilidade comum de alimentação elétrica
A investigação concluiu que os cabos elétricos do barramento **não possuíam encaminhamento por duas rotas distintas** e **não eram resistentes ao fogo**, embora a filosofia citada para a época previsse rotas distintas ou cabo resistente ao fogo para serviços essenciais e de emergência em áreas perigosas. Como os cabos não resistiram ao incêndio, houve falha do suprimento de energia das bombas elétricas de combate a incêndio e prejuízo ao monitoramento pelo sistema supervisório.  
**Fontes:** `anp-668be0de2e3714c6db785a31:p38-43:26.0-10.0`

A conclusão prática é que, ao avaliar disponibilidade de bombeamento, deve-se olhar além da curva da bomba e perguntar:
- a alimentação elétrica sobrevive ao incêndio dimensionante?
- há segregação física suficiente entre rotas ou proteção ao cabeamento?
- a perda de uma rota ou de um barramento elimina mais de uma função crítica ao mesmo tempo?

### 5.3 Diversificação de acionamento
O arranjo com bombas elétricas e a diesel mostra a lógica de **diversificação de acionamento**. Em tese, isso reduz a dependência de um único insumo energético. Porém, o evento evidencia que a mera existência de bombas com motores diferentes não resolve o problema se houver falhas de projeto, integração ou manutenção que impeçam a resposta efetiva.  
**Fontes:** `anp-668be0de2e3714c6db785a31:p38-43:26.0-10.0`

## 6. Efeito das válvulas de dilúvio e da filosofia fail-open sobre a demanda da rede
Um aspecto operacional importante do caso P-20 foi o comportamento das ADVs. O relatório informa que as válvulas do sistema de dilúvio eram do tipo **FA (falha aberta)** e que a investigação concluiu que elas foram abertas por esse motivo após a perda do barramento. Há também relato de abertura de ADVs pelo pessoal de bordo, na sala de controle e em campo, para resfriar outros equipamentos e reduzir os efeitos do incêndio.  
**Fontes:** `anp-668be0de2e3714c6db785a31:p38-43:26.0-10.0`

Para a rede de água e bombeamento, isso tem duas consequências diretas:
1. a **demanda instantânea** pode aumentar muito mais do que a prevista para um único consumidor;
2. a **disponibilidade de água nos hidrantes/monitores** pode cair se a simultaneidade real superar o caso dimensionante ou se parte do bombeamento falhar.

Em outras palavras, a filosofia de fail-open pode ser tecnicamente adequada para proteção de zonas, mas ela precisa ser compatibilizada com:
- a capacidade das bombas;
- a capacidade hidráulica do anel/fire main;
- o cenário de múltiplas aberturas automáticas e manuais em emergência.

## 7. Critérios práticos de avaliação profissional da rede de água e bombeamento
Com base apenas nos trechos aproveitados, uma avaliação técnica consistente desta faceta deve verificar, no mínimo, os seguintes pontos:

### 7.1 Cenário dimensionante
- O projeto define claramente **quais consumidores podem atuar simultaneamente**?
- O caso dimensionante foi construído com base em cenário de incêndio crível, e não em operação isolada de um único dispositivo?
- A demanda total de água no caso dimensionante está explicitada?  
**Fontes:** `anp-668be0de2e3714c6db785a31:p38-43:26.0-10.0`

### 7.2 Pressão e vazão no ponto de uso
- Há requisito explícito de **vazão mínima** e **pressão residual mínima** no ponto remoto ou consumidor crítico?
- O dimensionamento da tubulação foi feito a partir desses requisitos de saída?  
**Fontes:** `regis-0706fb4ed5d69f422f2d0ffb:pNone:879.0-1047.0`, `regis-0706fb4ed5d69f422f2d0ffb:pNone:958.0-1178.0`

### 7.3 Coerência do diâmetro com a vazão
- O diâmetro preliminar obtido por \(Q = V \cdot A\) é coerente com a faixa de velocidade escolhida?
- Existem trechos potencialmente restritivos que possam causar perda excessiva de pressão?  
**Fontes:** `regis-0706fb4ed5d69f422f2d0ffb:pNone:879.0-1047.0`, `regis-0706fb4ed5d69f422f2d0ffb:pNone:958.0-1178.0`

### 7.4 Sobrevivência do bombeamento
- A lógica de partida automática por baixa pressão funciona sob incêndio?
- As bombas elétricas dependem de uma única rota vulnerável ao fogo?
- Existe diversificação real de acionamento e não apenas capacidade nominal em catálogo?  
**Fontes:** `anp-668be0de2e3714c6db785a31:p38-43:26.0-10.0`

### 7.5 Efeito de falhas e aberturas não planejadas
- A abertura fail-open de válvulas de dilúvio foi considerada no balanço de demanda?
- O sistema continua atendendo hidrantes e monitores quando múltiplas zonas são abertas?  
**Fontes:** `anp-668be0de2e3714c6db785a31:p38-43:26.0-10.0`

### 7.6 Integridade mecânica como pré-requisito de disponibilidade
- Espessura, suportação e carregamentos da tubulação são compatíveis com o serviço de emergência?
- O material e a espessura adotados refletem não só o cálculo mínimo, mas também os mínimos construtivos aplicáveis?  
**Fontes:** `regis-0706fb4ed5d69f422f2d0ffb:pNone:958.0-1178.0`

## 8. Síntese técnica
Os trechos analisados sustentam uma conclusão objetiva: o desempenho da rede de água de incêndio em FPSO/FSO deve ser avaliado por dois eixos inseparáveis:

1. **dimensionamento hidráulico pelo cenário real de demanda**, partindo da vazão e pressão exigidas nos consumidores e considerando simultaneidade plausível de hidrantes, canhões e zonas de dilúvio;  
2. **disponibilidade do bombeamento e da rede sob dano de incêndio**, incluindo vulnerabilidade de alimentação elétrica, lógica de acionamento, diversificação de acionamento e efeitos de abertura automática/manual de válvulas.

Quando um desses eixos falha, o resultado provável é o mesmo observado no caso investigado: **redução da disponibilidade de água**, maior duração do combate e maior potencial de agravamento do evento.  
**Fontes:** `regis-0706fb4ed5d69f422f2d0ffb:pNone:879.0-1047.0`, `regis-0706fb4ed5d69f422f2d0ffb:pNone:958.0-1178.0`, `anp-668be0de2e3714c6db785a31:p38-43:26.0-10.0`