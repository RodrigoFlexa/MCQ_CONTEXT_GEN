# Qualidade de energia e transitórios em sistemas elétricos de FPSO

## 1. Enquadramento técnico da faceta

Em FPSOs, a avaliação da rede elétrica sob **cargas perturbadoras** e **eventos transitórios** exige separar fenômenos de naturezas distintas, mas acopladas:

- **regime permanente**: tensões, correntes e fluxos de potência ativa e reativa em condição estabilizada;
- **regime dinâmico**: evolução temporal da resposta elétrica e eletromecânica após perturbações, como partida de grandes motores, rejeição de carga, perda de geração e faltas;
- **transitórios eletromagnéticos rápidos**: chaveamentos, sobretensões e tensão de restabelecimento de disjuntores (TRV);
- **qualidade de energia**: distorção harmônica, desequilíbrio, afundamentos de tensão, tremulações e interferências provocadas por cargas não lineares e eletrônica de potência.

Para redes industriais com geração própria, como as encontradas em unidades offshore, não basta “fotografar” a condição da rede. É necessário avaliar o comportamento ao longo do tempo, com modelos adequados de geradores, motores, reguladores e cargas, pois a resposta dinâmica pode determinar se a instalação permanece operável ou entra em condição de instabilidade, subtensão, disparo indevido ou perda de seletividade.

**Fontes:** `petroles-004c2afadba7ea17c7dd7908:pNone:2134835.0-2134902.0`, `petroles-004c2afadba7ea17c7dd7908:pNone:2134903.0-2134951.0`

## 2. Estudos elétricos aplicáveis ao comportamento dinâmico da rede

Os trechos indicam que, em sistemas elétricos industriais, os estudos relevantes para esta faceta incluem:

### 2.1 Fluxo de potência
Determina tensões, correntes e fluxos de potência ativa e reativa em condição sem defeito. É a base para:

- verificar perfis de tensão antes de perturbações;
- identificar sobrecargas e barras com tensão baixa;
- testar contingências como perda de uma carga ou de um circuito;
- avaliar a condição inicial a partir da qual um evento dinâmico ocorrerá.

### 2.2 Curto-circuito
Determina correntes de falta para especificação de disjuntores, painéis e ajustes de proteção. Embora seja um estudo clássico de defeito, ele também é aproveitado em metodologias simplificadas para estimar queda de tensão em eventos severos, como partida de motor, quando certas cargas são aproximadas por impedâncias constantes.

### 2.3 Estabilidade
Aplica-se a sistemas com duas ou mais máquinas síncronas e avalia a capacidade de o sistema continuar operando após uma mudança. Para FPSOs com geração própria, isso é diretamente relevante em contingências como:

- rejeição de carga;
- partida de grandes motores;
- perda de geração própria;
- perda de suprimento externo, quando houver;
- curtos-circuitos.

Esses estudos demandam modelagem mais detalhada de geradores e motores, incluindo reguladores de tensão e de velocidade, e eventualmente saturação.

### 2.4 Partida de motores
É um estudo dinâmico típico de instalação industrial. A saída esperada não é apenas um valor final, mas curvas de:

- tensão na barra do motor;
- corrente do motor;
- velocidade;
- escorregamento;
- conjugado.

### 2.5 Harmônicos
Devem prever os níveis de distorção de tensão e corrente quando novas cargas não lineares forem adicionadas, bem como a necessidade de filtros.

### 2.6 Transitórios eletromagnéticos
São necessários para analisar:

- operação de disjuntores;
- chaveamento de bancos de capacitores;
- TRV de disjuntores.

Os trechos citam explicitamente o uso de ferramentas do tipo **EMTP** para esse tipo de fenômeno.

### 2.7 Coordenação de proteção
Embora não seja um estudo de qualidade de energia em si, torna-se inseparável da análise de transitórios e perturbações, porque a função do sistema de proteção é isolar a menor parte possível da rede, no menor tempo possível, minimizando danos a pessoas e equipamentos.

**Síntese prática:** em um FPSO, a avaliação de cargas perturbadoras não deve ser feita por um único estudo. O conjunto mínimo tende a combinar fluxo de potência, curto-circuito, partida de motores, estabilidade, harmônicos e, quando houver chaveamentos críticos, transitórios eletromagnéticos.

**Fontes:** `petroles-004c2afadba7ea17c7dd7908:pNone:2134835.0-2134902.0`, `petroles-004c2afadba7ea17c7dd7908:pNone:2134903.0-2134951.0`

## 3. Partida de grandes motores como carga perturbadora

A partida de um motor elétrico solicita da rede uma corrente várias vezes maior que a corrente nominal. As consequências indicadas nos trechos são:

- **queda de tensão** ao longo do sistema;
- impacto em **contatores**, **iluminação** e **outros motores**;
- risco de o motor em partida não desenvolver **conjugado suficiente** para acelerar a carga.

Há uma relação particularmente importante para avaliação dinâmica: o **conjugado de partida varia diretamente com o quadrado da tensão aplicada**. Isso significa que uma redução modesta de tensão pode degradar de forma muito mais severa a capacidade de aceleração do motor. Em termos práticos:

- queda de tensão excessiva prejudica a carga que já está operando;
- a mesma queda pode impedir o próprio motor de partir ou prolongar a aceleração;
- aceleração prolongada aumenta esforço térmico e pode aproximar a instalação de subtensão, subfrequência e atuação de proteções.

Em FPSOs, esse fenômeno é particularmente crítico quando o motor de grande porte disputa potência reativa e capacidade de curto prazo com poucos geradores em operação.

**Fontes:** `petroles-004c2afadba7ea17c7dd7908:pNone:2134835.0-2134902.0`

## 4. Modelagem da partida de motores: métodos e implicações

Os trechos comparam dois enfoques clássicos para o estudo da queda de tensão causada pela partida de motores.

### 4.1 Método baseado em fluxo de potência
Nesse método:

- a **carga inicial** é modelada como **potência constante**;
- o **motor em partida** é modelado como **impedância constante**;
- executa-se primeiro um fluxo de potência para obter a condição inicial;
- para a partida, adapta-se o modelo incluindo a representação da fonte com a tensão interna da máquina, associada à reatância transitória do gerador.

Esse tratamento é mais severo para o perfil de tensão, porque quando a tensão cai, a carga modelada como potência constante tende a demandar mais corrente para manter a potência, agravando a queda de tensão.

### 4.2 Método das impedâncias
Nesse método:

- tanto a **carga inicial** quanto o **motor em partida** são representados por **impedâncias constantes**;
- um programa de curto-circuito pode ser adaptado para a solução do problema.

Como a carga inicial passa a se comportar como impedância, a corrente tende a diminuir com a queda de tensão, o que reduz o agravamento adicional do afundamento. É um método mais simples e pode servir como primeira estimativa.

### 4.3 Diferenças práticas entre os métodos
A comparação dos textos destaca dois pontos decisivos:

1. **Modelagem da carga inicial**
   - potência constante: mais severa para tensão;
   - impedância constante: menos severa na representação da carga preexistente.

2. **Representação da tensão interna da geração**
   - no método mais detalhado, a tensão interna da máquina é obtida a partir da condição do gerador e da sua reatância transitória;
   - no método simplificado associado ao programa de curto-circuito, essa representação é mais aproximada.

Os trechos concluem que o método das impedâncias pode resultar em estimativas mais conservadoras de tensão em um caso comparado, além de ser mais simples para avaliações repetitivas, como estudos de reaceleração em múltiplos passos. Já o método com fluxo de potência é recomendado quando se dispõe de ferramenta computacional e se deseja melhor tratamento das condições iniciais e da fonte.

### 4.4 Aplicação ao contexto FPSO
Para redes de FPSO, essa comparação é valiosa porque a resposta durante a partida de compressores, bombas e outros grandes consumidores depende fortemente de:

- como as cargas remanescentes são modeladas;
- quantos geradores estão online;
- quanto suporte de tensão e potência reativa os geradores conseguem fornecer no transitório;
- qual é o tempo de aceleração da carga.

Portanto, resultados de afundamento de tensão, tempo de aceleração e margem operacional podem variar significativamente com a hipótese de modelagem, não sendo prudente extrapolar um método simplificado como representação universal do comportamento real.

**Fontes:** `regis-9593862d806a3d6956cf5a9e:pNone:28.0-107.0`

## 5. Estabilidade eletromecânica e resposta temporal da geração

Os estudos de estabilidade, conforme descritos nos trechos, tratam da capacidade de um sistema com máquinas síncronas de continuar operando após uma mudança. Para a faceta de qualidade de energia e transitórios, isso significa que a análise não deve se limitar à magnitude do afundamento de tensão; também deve considerar:

- comportamento do rotor das máquinas;
- equilíbrio entre potência ativa e frequência;
- resposta dos reguladores de tensão;
- resposta dos reguladores de velocidade;
- possibilidade de não linearidades, inclusive saturação.

Em perturbações relevantes para FPSOs, como a entrada de um grande motor, rejeição de carga ou perda de um gerador, o fenômeno observado na rede é resultado combinado de:

- dinâmica eletromagnética imediata da rede;
- dinâmica eletromecânica dos eixos girantes;
- ação dos controles automáticos.

Assim, uma rede pode apresentar tensão aparentemente aceitável em um “instantâneo” e, ainda assim, evoluir mal no tempo por deficiência de controle, excesso de solicitação reativa ou perda de sincronismo/estabilidade.

**Fontes:** `petroles-004c2afadba7ea17c7dd7908:pNone:2134835.0-2134902.0`

## 6. Harmônicos e cargas não lineares

Os trechos identificam a eletrônica de potência como fonte crescente de problemas de qualidade de energia em sistemas industriais. Na indústria do petróleo, destacam-se como cargas não lineares típicas os **conversores de frequência**.

As consequências citadas para a presença de harmônicos de tensão e corrente incluem:

- interferências em sistemas de controle;
- aquecimento de máquinas rotativas;
- falhas de capacitores;
- interferência em telecomunicações.

Em termos de engenharia, o efeito de rede é duplo:

1. a carga não linear injeta **correntes não senoidais**;
2. a passagem dessas correntes pela impedância do sistema produz **distorção de tensão** nas barras.

Por isso, a avaliação de harmônicos em FPSOs não deve focar apenas no equipamento emissor; deve considerar a impedância da rede local, a topologia de barramentos, a presença de bancos capacitivos e a sensibilidade das cargas vizinhas.

Os trechos também indicam que os estudos devem prever os níveis de distorção quando novas cargas não lineares forem adicionadas, bem como a instalação de **filtros** quando necessário.

**Fontes:** `petroles-004c2afadba7ea17c7dd7908:pNone:2134835.0-2134902.0`, `petroles-004c2afadba7ea17c7dd7908:pNone:2134903.0-2134951.0`

## 7. Distúrbios de alta frequência gerados por inversores

Os trechos sobre inversores de frequência acrescentam uma camada importante à análise de qualidade de energia: além dos harmônicos clássicos de baixa ordem, conversores com retificador, elo CC e estágio inversor com IGBTs podem gerar **ruído impulsivo de alta frequência** e amplo espectro.

### 7.1 Mecanismos de geração
Os textos associam os distúrbios principalmente a duas partes do conversor:

- **etapa retificadora**: gera correntes harmônicas enquanto o capacitor do elo CC é carregado pela ponte retificadora;
- **etapa inversora**: o chaveamento dos IGBTs, com altas frequências e altos gradientes de tensão, gera ruído impulsivo assíncrono em relação à frequência fundamental.

### 7.2 Consequências técnicas
Os efeitos apontados incluem:

- distorção harmônica de corrente e, por interação com a impedância da linha, também de tensão;
- propagação de ruído de alta frequência pela rede;
- redução da taxa de transferência de dados e aumento de erros quando há sistemas de comunicação que compartilham o mesmo meio elétrico;
- aquecimento adicional e solicitação dielétrica em motores alimentados por formas de onda não senoidais.

### 7.3 Relevância para FPSO e subsea
Embora os exemplos dos trechos sejam ligados a BCS/BCSS, o mecanismo físico é aplicável a acionamentos por velocidade variável em geral: drives de média tensão, cargas submarinas alimentadas eletricamente, sistemas auxiliares com conversores e UPS/inversores podem impor à rede distorções e ruídos que excedem a simples análise em 50/60 Hz.

Quando esses acionamentos coexistem com sistemas sensíveis de controle, instrumentação ou telecomunicações, a análise deve considerar não só THD, mas também compatibilidade eletromagnética, ruído conduzido e dv/dt nos terminais das máquinas.

**Fontes:** `petroles-4ee4bce16acf674505c8912d:pNone:574755.0-574796.0`, `petroles-004c2afadba7ea17c7dd7908:pNone:2450082.0-2450160.0`

## 8. Outras manifestações de qualidade de energia relevantes

Um dos trechos define impactos típicos de cargas não lineares e de elevada potência sobre a rede, úteis como referência conceitual para ambientes industriais:

### 8.1 Instabilidade de tensão
É a capacidade do sistema, a partir de uma condição inicial, de recuperar um estado de equilíbrio após um distúrbio. Cargas não lineares ou pulsantes, ao absorverem potência relevante em intervalo curto, podem degradar essa recuperação.

### 8.2 Distorção harmônica
É a deformação da onda de tensão ou corrente causada por harmônicos. Seus efeitos incluem envelhecimento precoce de equipamentos, aumento de perdas e, em certos casos, aparecimento de corrente no neutro.

### 8.3 Desequilíbrio de tensões
Ocorre quando amplitudes de fase diferem ou quando o defasamento entre fases se afasta de 120°. É agravado por distribuição desigual de carga entre fases.

### 8.4 Tremulações
O trecho descreve a tremulação como redução de tensão eficaz por intervalos curtos, associada a curto-circuitos, sobrecargas ou partida de motores de potência considerável. Embora a definição reproduzida seja simplificada, o ponto técnico útil é que cargas com variação abrupta de corrente podem produzir flutuações perceptíveis e críticas para outras cargas.

Para FPSOs, esses conceitos ajudam a interpretar sintomas como oscilações de tensão em barramentos, disparos por subtensão, mau funcionamento de eletrônica sensível e degradação térmica sem ocorrência de falta franca.

**Fontes:** `regis-9f1f312c16d0a04b5f83c7a1:pNone:1255.0-1491.0`

## 9. Transitórios de chaveamento e sobretensões

Os trechos indicam explicitamente que certos fenômenos exigem estudo de transitórios eletromagnéticos, especialmente:

- **operação de disjuntores**;
- **chaveamento de bancos de capacitores**;
- **tensão de restabelecimento de disjuntores (TRV)**.

Esses eventos podem gerar sobretensões, oscilações de alta frequência e solicitações dielétricas incompatíveis com a simples análise em regime permanente. Em aplicações offshore, isso é particularmente sensível quando a rede é compacta, com cabos relativamente curtos, transformadores próximos, cargas eletrônicas e equipamentos de comutação com alta frequência de manobra.

A indicação de uso de ferramentas do tipo **EMTP** é relevante porque tais programas permitem representar elementos distribuídos e fenômenos rápidos que não aparecem adequadamente em fluxo de potência ou em estudos puramente fasoriais.

**Fontes:** `petroles-004c2afadba7ea17c7dd7908:pNone:2134903.0-2134951.0`

## 10. Papel dos controles de conversores na mitigação local

Os trechos sobre conversores CC-CA mostram que a estratégia de controle influencia diretamente a qualidade da tensão entregue à carga.

Pontos técnicos úteis:

- pode-se controlar a tensão na entrada do inversor, dentro do inversor por modulação/defasagem, ou na saída;
- cargas não lineares exigiram estratégias além da simples regulação do valor eficaz, com foco em baixa distorção harmônica;
- controles com **malha externa de tensão** e **malha interna de corrente** melhoram a dinâmica e a estabilidade;
- controladores **PID**, **repetitivos**, **proporcional-ressonantes** e compensadores harmônicos podem reduzir erro estático e minimizar harmônicas indesejáveis.

No contexto de FPSO, isso é mais aplicável a equipamentos como UPS, fontes CA estáticas, inversores dedicados e certos acionamentos, do que à geração principal síncrona. Ainda assim, a mensagem de engenharia é relevante: a mitigação de problemas de qualidade de energia pode ocorrer tanto no nível do sistema elétrico quanto no nível do controle do conversor emissor.

**Fontes:** `regis-0dc50fc46ae97dc94d152862:pNone:2069.0-2212.0`

## 11. Diretrizes práticas para projeto, comissionamento, operação e troubleshooting

Com base nos trechos, uma abordagem tecnicamente consistente para redes de FPSO submetidas a cargas perturbadoras e eventos transitórios inclui:

### 11.1 No projeto
- estabelecer um caso-base por **fluxo de potência**;
- avaliar contingências de **perda de carga**, **perda de linha/alimentador** e **maior motor em partida**;
- realizar estudos de **estabilidade** quando houver múltiplos geradores síncronos e contingências severas;
- realizar estudos de **harmônicos** ao introduzir VFDs, UPS/inversores e outras cargas não lineares;
- realizar estudos de **transitórios eletromagnéticos** para chaveamentos críticos, bancos de capacitores e TRV;
- revisar a **coordenação da proteção** para garantir isolamento rápido e seletivo da parte defeituosa.

### 11.2 No comissionamento
- confirmar se os perfis reais de partida de motores correspondem aos estudos;
- verificar se a rede apresenta afundamentos de tensão compatíveis com a continuidade operacional das demais cargas;
- observar aquecimento anormal de máquinas rotativas e capacitores em presença de conversores;
- verificar interferências em controle, telecom e sistemas eletrônicos quando acionamentos de frequência variável entram em operação.

### 11.3 Na operação e solução de problemas
Sintomas que sugerem problemas de qualidade de energia ou transitórios mal controlados incluem:

- subtensão recorrente em partidas;
- dificuldade de aceleração de motores grandes;
- disparos sem falta franca aparente;
- aquecimento adicional em motores, transformadores ou capacitores;
- erros de comunicação e interferência em sistemas sensíveis;
- degradação prematura de isolamento em motores alimentados por inversores;
- comportamento instável após rejeição de carga ou perda de geração.

### 11.4 Na mitigação
As medidas explicitamente sustentadas pelos trechos incluem:

- **modelagem adequada** dos eventos e equipamentos, em vez de depender apenas de estimativas estáticas;
- **filtros** para correção de distorção harmônica, quando os estudos indicarem necessidade;
- **estratégias de controle de conversores** que melhorem dinâmica e THD;
- **ajuste/seleção apropriada da proteção** para isolar apenas a porção defeituosa da rede.

**Fontes:** `petroles-004c2afadba7ea17c7dd7908:pNone:2134835.0-2134902.0`, `petroles-004c2afadba7ea17c7dd7908:pNone:2134903.0-2134951.0`, `regis-9593862d806a3d6956cf5a9e:pNone:28.0-107.0`, `regis-0dc50fc46ae97dc94d152862:pNone:2069.0-2212.0`, `petroles-4ee4bce16acf674505c8912d:pNone:574755.0-574796.0`, `petroles-004c2afadba7ea17c7dd7908:pNone:2450082.0-2450160.0`, `regis-9f1f312c16d0a04b5f83c7a1:pNone:1255.0-1491.0`

## 12. Síntese final

Para avaliar o comportamento dinâmico da rede elétrica de um FPSO diante de cargas perturbadoras e eventos transitórios, o ponto central é combinar corretamente **modelagem**, **tipo de estudo** e **fenômeno físico dominante**. Partidas de motores e perda de geração exigem visão dinâmica eletromecânica; harmônicos e ruído de inversores exigem avaliação de qualidade de energia e compatibilidade; chaveamentos e TRV exigem estudo de transitórios eletromagnéticos. A confiabilidade do resultado depende mais da adequação dessas hipóteses do que do uso isolado de qualquer ferramenta de cálculo.

**Fontes:** `petroles-004c2afadba7ea17c7dd7908:pNone:2134835.0-2134902.0`, `petroles-004c2afadba7ea17c7dd7908:pNone:2134903.0-2134951.0`, `regis-9593862d806a3d6956cf5a9e:pNone:28.0-107.0`