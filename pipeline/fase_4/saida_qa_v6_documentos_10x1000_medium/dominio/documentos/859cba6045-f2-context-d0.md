# Flotação e skimming da água produzida para descarte no mar em FPSOs

## 1. Papel da flotação no trem de tratamento da água produzida
A flotação é uma etapa de remoção de óleo residual aplicada quando a separação gravitacional primária não é suficiente para enquadrar a água produzida para descarte. Em instalações offshore, o tratamento normalmente combina mais de um processo, porque a água produzida contém óleo livre, disperso, emulsificado, sólidos suspensos e compostos dissolvidos. Na prática, hidrociclones, vasos gravitacionais e flotadores são usados de forma conjugada para aumentar a eficiência global; para descarte offshore, a combinação hidrociclones + flotação por gás induzido é recorrente nas referências fornecidas. Em FPSOs, a seleção tecnológica também é influenciada por restrições de espaço e peso, o que favorece equipamentos compactos.  
**Fontes:** `petroles-004c2afadba7ea17c7dd7908:pNone:174466.0-174510.0`, `petroles-004c2afadba7ea17c7dd7908:pNone:1753803.0-1753840.0`, `petroles-4ee4bce16acf674505c8912d:pNone:421771.0-421805.0`

Do ponto de vista de desempenho do trem de tratamento, as referências indicam faixas típicas de concentração de óleos e graxas ao longo de etapas sucessivas: água oleosa bruta, separadores API/CPI e depois flotação. Nos dados citados, a flotação aparece como etapa capaz de reduzir a concentração para uma faixa inferior à dos separadores gravitacionais, tipicamente após a remoção das gotas maiores. Isso reforça que a flotação é, em geral, uma etapa de polimento de óleo disperso/emulsificado, e não substitui integralmente a separação primária.  
**Fontes:** `regis-5cbc251ea81156e88d920048:pNone:2961.0-3163.0`

## 2. Fundamentos do mecanismo de flotação
A flotação remove partículas suspensas e gotículas de óleo por adesão a bolhas de gás, formando agregados menos densos que a fase aquosa, os quais ascendem à superfície. O mecanismo essencial envolve: geração de bolhas, colisão bolha-gota, adesão bolha-gota e transporte do agregado até a superfície, onde se forma uma camada oleosa/espuma a ser removida por skimming.  
**Fontes:** `regis-5f8888d1c91c7261ea300be9:pNone:5389.0-5596.0`, `regis-5cbc251ea81156e88d920048:pNone:2961.0-3163.0`, `petroles-4ee4bce16acf674505c8912d:pNone:403116.0-403203.0`

Uma formulação útil para interpretar a eficiência do processo é a probabilidade global de flotação:

\[
P = P_c \cdot P_a \cdot P_s
\]

onde:
- \(P_c\): probabilidade de colisão bolha-gota;
- \(P_a\): probabilidade de adesão após a colisão;
- \(P_s\): probabilidade de formação de agregado bolha-gota estável.

Essa decomposição é relevante para diagnóstico operacional: uma unidade pode ter baixa eficiência por falha na geração/dispersão de bolhas, por baixa afinidade interfacial entre bolha e gota, ou por instabilidade do agregado formado.  
**Fontes:** `regis-5cbc251ea81156e88d920048:pNone:2961.0-3163.0`

A ascensão do agregado bolha-gota pode ser interpretada com base em uma forma da Lei de Stokes, em um “campo de força reverso” em relação à sedimentação:

\[
V_t = \frac{D^2 g (\rho_a - \rho_o)}{18\mu}
\]

onde:
- \(V_t\): velocidade terminal de ascensão do agregado bolha-gota (m/s);
- \(g\): aceleração da gravidade (9,80 m/s²);
- \(D\): diâmetro efetivo do agregado bolha-gota (m);
- \(\rho_a\): densidade da fase contínua (kg/m³);
- \(\rho_o\): densidade do agregado bolha-gota (kg/m³);
- \(\mu\): viscosidade da fase contínua (kg/(m·s)).

Operacionalmente, essa relação ajuda a entender por que agregados maiores e com maior diferença efetiva de densidade tendem a subir mais rapidamente, melhorando a remoção superficial.  
**Fontes:** `regis-5cbc251ea81156e88d920048:pNone:2961.0-3163.0`

## 3. Tipos de flotação e implicações para FPSOs
As referências distinguem principalmente:

### 3.1 Flotação por gás dissolvido (FGD/FAD)
Na flotação por gás dissolvido, o gás é dissolvido na corrente a pressões elevadas em um saturador; quando a pressão é reduzida, o excesso se desprende como microbolhas. Também há descrição de geração por vácuo ou por queda rápida de pressão. Em comparação com a flotação por gás induzido, a FGD produz bolhas menores, o que tende a favorecer colisão/adesão com gotas finas; em contrapartida, as referências destacam maior exigência de espaço, manutenção e operação.  
**Fontes:** `regis-5f8888d1c91c7261ea300be9:pNone:5389.0-5596.0`, `regis-5cbc251ea81156e88d920048:pNone:2961.0-3163.0`, `petroles-004c2afadba7ea17c7dd7908:pNone:1753803.0-1753840.0`

### 3.2 Flotação por gás induzido (FGI/FAI)
Na flotação por gás induzido, as bolhas são geradas mecanicamente ou hidraulicamente, por impeller, edutor, aspersão ou combinação bomba centrífuga + edutor. As referências descrevem para a FGI convencional bolhas com diâmetro entre 400 e 2000 µm, regime hidrodinâmico mais turbulento e tempo de retenção curto, da ordem de 4 a 10 min. Sistemas multiestágio (tipicamente 3 a 4 células) são descritos como mais versáteis e eficientes, porque cada estágio melhora a qualidade da água proveniente do anterior e oferece maior flexibilidade para lidar com flutuações de vazão e concentração.  
**Fontes:** `regis-5cbc251ea81156e88d920048:pNone:3824.0-4082.0`

### 3.3 Critérios práticos de seleção offshore
Com base nos trechos fornecidos, alguns critérios práticos são:
- **restrição de espaço/peso:** favorece tecnologias compactas; por isso FGI e hidrociclones aparecem fortemente associados ao offshore;  
- **necessidade de bolhas menores e maior controle do ar liberado:** favorece FGD/FAD, com penalidade potencial em footprint e complexidade;  
- **necessidade de flexibilidade operacional frente a grandes oscilações de carga:** favorece multiestágio em FGI;  
- **busca por menor manutenção mecânica:** em FGI, arranjos tipo edutor/nozzle podem ser vantajosos pela ausência de partes móveis na zona de geração de bolhas.  
**Fontes:** `petroles-004c2afadba7ea17c7dd7908:pNone:1753803.0-1753840.0`, `petroles-4ee4bce16acf674505c8912d:pNone:421771.0-421805.0`, `regis-5cbc251ea81156e88d920048:pNone:3824.0-4082.0`, `regis-5f8888d1c91c7261ea300be9:pNone:5389.0-5596.0`

## 4. Variáveis de processo que governam a remoção de óleo residual
As referências destacam que a eficiência da flotação depende de múltiplos fatores físicos e químicos:
- vazão de gás ou relação gás/líquido (**hold up**);
- tamanho e dispersão das bolhas;
- tamanho, concentração e características superficiais das gotas de óleo;
- concentração de agentes desestabilizantes;
- temperatura;
- pH.  
**Fontes:** `regis-5cbc251ea81156e88d920048:pNone:2961.0-3163.0`

### 4.1 Tamanho de gota e limite físico da separação
A distribuição de tamanho de gota é uma variável crítica. Os trechos citam queda acentuada da eficiência para gotas menores que 10 µm e ausência prática de eficiência para gotas com diâmetro médio de 2 µm em determinadas condições estudadas. Isso significa que, quando a água produzida sofre forte cisalhamento em bombas, válvulas, constrições hidráulicas e outros equipamentos, o óleo tende a se dispersar mais finamente e a formar emulsões mais estáveis, tornando a remoção por flotação significativamente mais difícil.  
**Fontes:** `regis-5cbc251ea81156e88d920048:pNone:2961.0-3163.0`, `petroles-4ee4bce16acf674505c8912d:pNone:63739.0-63780.0`

### 4.2 Tamanho de bolha e hold up
Os dados citados indicam que colisão e adesão são favorecidas por bolhas menores, gotas maiores e maior concentração de gás. Na FGI, aumento de hold up e redução do tamanho de bolha aumentaram a recuperação de óleo em estudos de bancada. Em coluna air-lift relatada nas referências, maior vazão de diluição elevou a remoção por aumentar a quantidade de microbolhas disponíveis para aderência às gotículas oleosas; o aumento da vazão de ar amplia a área superficial total das bolhas.  
**Fontes:** `regis-5cbc251ea81156e88d920048:pNone:2961.0-3163.0`, `regis-5cbc251ea81156e88d920048:pNone:3824.0-4082.0`, `petroles-004c2afadba7ea17c7dd7908:pNone:392301.0-392372.0`

### 4.3 Regime hidrodinâmico e turbulência
A turbulência exerce efeito ambíguo: é necessária para dispersão do gás e promoção de contato bolha-gota, mas pode prejudicar a zona de flotação se excessiva. As referências relatam que o aumento da velocidade do impeller melhora a remoção em determinadas profundidades de submersão, porém piora em pequenas profundidades, provavelmente por excesso de turbulência na zona de separação. Em otimização operacional, isso implica buscar um ponto em que haja mistura suficiente para contato, sem romper agregados ou arrastar óleo novamente para o líquido tratado.  
**Fontes:** `regis-5cbc251ea81156e88d920048:pNone:3824.0-4082.0`

### 4.4 Efeito de surfactantes, sólidos finos e estabilidade de emulsão
As emulsões óleo-em-água são estabilizadas por sólidos finamente divididos, surfactantes naturais do petróleo e reagentes do processo. Nessa condição, a simples separação gravitacional tende a falhar e a flotação passa a exigir maior cuidado com química e hidrodinâmica. Quando a estabilidade interfacial é alta, a formação de agregados bolha-gota permanentes se torna menos provável, reduzindo \(P_a\) e \(P_s\).  
**Fontes:** `petroles-4ee4bce16acf674505c8912d:pNone:63739.0-63780.0`, `regis-5cbc251ea81156e88d920048:pNone:2961.0-3163.0`

## 5. Dosagem química e desestabilização para melhorar a flotação
As referências indicam que é comum adicionar coagulantes e floculantes em FGD para elevar a eficiência de separação. O racional é aumentar a agregação, elevar a probabilidade de colisão bolha-gota, acelerar a cinética de flotação e melhorar o aproveitamento do gás. Em um estudo citado, o uso de polímero floculante não iônico em FAI elevou a remoção de óleo a valores muito altos e reduziu a concentração residual para 10 mg/L naquele caso específico.  
**Fontes:** `regis-5cbc251ea81156e88d920048:pNone:3824.0-4082.0`

Para decisão operacional, a adição química tende a ser mais justificável quando:
- a emulsão está muito estável;
- a distribuição de gotas migrou para faixa fina por cisalhamento;
- a unidade opera perto do limite de descarte;
- a elevação de gás/energia sozinha não entrega a redução de TOG necessária.

Por outro lado, os resultados disponíveis também mostram que geometrias favoráveis e melhor contato bolha-gota podem produzir alta remoção sem aditivos em ensaios específicos. Logo, a otimização deve comparar benefício de química versus ajustes hidrodinâmicos, sempre reconhecendo que resultados de bancada/piloto não são automaticamente transferíveis para um FPSO em operação.  
**Fontes:** `petroles-004c2afadba7ea17c7dd7908:pNone:392301.0-392372.0`, `regis-5cbc251ea81156e88d920048:pNone:3824.0-4082.0`

## 6. Parâmetros operacionais úteis para controle e otimização
### 6.1 Razão ar/óleo em FGD com reciclo pressurizado
Para sistemas com compressão do reciclo, uma relação citada para análise da razão mássica ar/óleo é:

\[
R_{ar/óleo} = \frac{Q_r \cdot K \cdot f \cdot P}{Q_a \cdot C}
\]

onde:
- \(Q_r\): vazão de reciclo (m³/h);
- \(Q_a\): vazão de alimentação (m³/h);
- \(K\): solubilidade do ar a 1 kgf/cm² na temperatura de operação (mg/L);
- \(f\): eficiência de saturação, tipicamente cerca de 0,5;
- \(P\): pressão manométrica de operação (kgf/cm²);
- \(C\): concentração de óleo na alimentação (mg/L).

Essa expressão é útil para balancear três alavancas clássicas da FGD: reciclo, pressão e carga de óleo. As referências ainda relatam melhor eficiência, em duas refinarias avaliadas, para razões ar/óleo entre 0,058 e 0,077, mas esse intervalo deve ser tratado como dado de caso e não como valor universal de projeto.  
**Fontes:** `regis-5cbc251ea81156e88d920048:pNone:3824.0-4082.0`

### 6.2 Carga afluente e ponto operacional
Os resultados experimentais fornecidos mostram que concentração de óleo no afluente e vazões do efluente/diluição podem ser fatores influentes na remoção. Em um caso de coluna air-lift, os maiores níveis experimentais dessas variáveis elevaram a resposta de remoção, interpretação associada a maior presença de gotículas para captura e maior quantidade de microbolhas para adesão. Em operação real, isso não significa que “quanto maior a carga, melhor” de forma irrestrita; significa que, dentro do espaço experimental estudado, a coluna não estava saturada e o aumento do fornecimento de bolhas melhorou a captura. Em escala industrial, a extrapolação deve considerar capacidade hidráulica, curto-circuito, sobrecarga da remoção superficial e limite de residência.  
**Fontes:** `petroles-004c2afadba7ea17c7dd7908:pNone:392301.0-392372.0`

### 6.3 Tempo de retenção e estágios
Na FGI convencional, tempos de retenção de 4 a 10 min e múltiplos estágios aparecem como características importantes. Operacionalmente, esse arranjo permite distribuir a remoção ao longo das células e acomodar flutuações de vazão ou concentração sem depender de uma única zona de flotação.  
**Fontes:** `regis-5cbc251ea81156e88d920048:pNone:3824.0-4082.0`

## 7. Skimming da fase oleosa flotada e correntes oleosas associadas
O resultado visível da flotação é a formação de uma camada superficial de espuma/óleo, gerada pela ascensão dos agregados bolha-gota. A retirada dessa camada por **skimming** é parte integrante do processo: se a fase flotada não for removida de forma estável, há risco de re-entrainment, piora do óleo residual na água e perda de capacidade útil do equipamento.  
**Fontes:** `regis-5f8888d1c91c7261ea300be9:pNone:5389.0-5596.0`, `regis-5cbc251ea81156e88d920048:pNone:2961.0-3163.0`

Os trechos fornecidos não detalham a geometria ou os controles específicos de **skimming vessels** dedicados. Ainda assim, eles permitem afirmar tecnicamente que:
- a flotação requer uma etapa de remoção superficial do óleo concentrado;
- vasos/tanques gravitacionais podem complementar a separação física no sistema global;
- a eficiência do trem depende não só da geração de bolhas e da captura, mas também da retirada da fase oleosa concentrada no topo.  
**Fontes:** `petroles-004c2afadba7ea17c7dd7908:pNone:174466.0-174510.0`, `regis-5f8888d1c91c7261ea300be9:pNone:5389.0-5596.0`

Como diretriz de operação, o skimming deve ser avaliado junto com:
- estabilidade da lâmina oleosa/espuma no topo;
- efeito de turbulência excessiva sobre o retorno do óleo à fase aquosa;
- capacidade de remoção das correntes oleosas geradas pelo tratamento.

## 8. Limites intrínsecos da flotação e interface com outras etapas
A flotação é eficaz para óleo disperso/emulsificado, mas não resolve integralmente o problema dos compostos dissolvidos. Uma referência informa que a capacidade da flotação para remoção de compostos orgânicos é limitada pelos compostos solúveis, que podem permanecer em concentrações da ordem de 60 mg/L. Outras referências reforçam que sais, metais e parte dos contaminantes dissolvidos exigem processos complementares como adsorção, troca iônica, membranas ou tratamento biológico, conforme o contaminante-alvo.  
**Fontes:** `regis-5cbc251ea81156e88d920048:pNone:2961.0-3163.0`, `petroles-004c2afadba7ea17c7dd7908:pNone:764663.0-764706.0`, `petroles-4ee4bce16acf674505c8912d:pNone:421771.0-421805.0`

Isso tem consequência direta para o diagnóstico de performance: uma água com baixo teor de óleo disperso, mas ainda fora de condicionante ambiental por compostos dissolvidos, não necessariamente indica falha da flotação. Pode indicar limitação do próprio mecanismo físico de separação adotado.  
**Fontes:** `regis-5cbc251ea81156e88d920048:pNone:2961.0-3163.0`

## 9. Diagnóstico de falhas operacionais na remoção por flotação
Situações típicas de perda de desempenho, coerentes com o material fornecido, incluem:

1. **Gotas excessivamente finas por cisalhamento**  
   Bombas, válvulas e constrições podem produzir emulsões mais estáveis e gotas menores, reduzindo a eficiência da captura por bolhas.  
   **Fontes:** `petroles-4ee4bce16acf674505c8912d:pNone:63739.0-63780.0`, `regis-5cbc251ea81156e88d920048:pNone:2961.0-3163.0`

2. **Bolhas grandes demais ou mal distribuídas**  
   Reduzem a área interfacial total disponível e podem piorar colisão/adesão com gotas pequenas.  
   **Fontes:** `regis-5cbc251ea81156e88d920048:pNone:2961.0-3163.0`, `regis-5cbc251ea81156e88d920048:pNone:3824.0-4082.0`

3. **Hold up insuficiente**  
   Menor quantidade de gás disponível reduz a chance de captura do óleo.  
   **Fontes:** `regis-5cbc251ea81156e88d920048:pNone:2961.0-3163.0`, `regis-5cbc251ea81156e88d920048:pNone:3824.0-4082.0`

4. **Turbulência excessiva na zona de flotação**  
   Pode romper agregados ou remisturar o óleo já separado.  
   **Fontes:** `regis-5cbc251ea81156e88d920048:pNone:3824.0-4082.0`

5. **Química desfavorável da água**  
   pH, temperatura, surfactantes e sólidos finos afetam adesão, estabilidade da emulsão e eficiência global.  
   **Fontes:** `regis-5cbc251ea81156e88d920048:pNone:2961.0-3163.0`, `petroles-4ee4bce16acf674505c8912d:pNone:63739.0-63780.0`

6. **Remoção superficial inadequada do óleo flotado**  
   Mesmo com boa captura, skimming deficiente compromete o resultado final.  
   **Fontes:** `regis-5f8888d1c91c7261ea300be9:pNone:5389.0-5596.0`

## 10. TOG, conformidade ambiental e implicações operacionais
O teor de óleos e graxas (TOG) aparece nos trechos como um dos principais parâmetros de controle para descarte da água produzida no mar. As referências também apontam que a legislação ambiental é um critério central de escolha tecnológica e de viabilidade operacional.  
**Fontes:** `petroles-4ee4bce16acf674505c8912d:pNone:403116.0-403203.0`, `petroles-4ee4bce16acf674505c8912d:pNone:421771.0-421805.0`

No entanto, nos trechos fornecidos os valores numéricos de resoluções brasileiras aparecem mascarados como `<NUMBER>`. Assim, o documento não reproduz limites legais específicos. Ainda assim, do ponto de vista técnico, a implicação é clara: a operação da flotação e do skimming deve ser conduzida para manter o TOG da água tratada dentro dos limites aplicáveis da licença e da regulamentação vigente, lembrando que a flotação trata sobretudo óleo disperso/emulsificado, não sendo solução completa para contaminantes dissolvidos.  
**Fontes:** `petroles-4ee4bce16acf674505c8912d:pNone:403116.0-403203.0`, `petroles-4ee4bce16acf674505c8912d:pNone:63739.0-63780.0`, `petroles-004c2afadba7ea17c7dd7908:pNone:1753803.0-1753840.0`

## 11. Síntese para operação e otimização em FPSOs
Para a faceta de flotação e skimming, os pontos mais úteis para avaliação profissional são:
- a flotação é etapa de remoção de óleo residual após a separação primária, especialmente importante para gotas finas e emulsificadas;  
- eficiência depende do tripé **gota-bolha-hidrodinâmica**: tamanho de gota, tamanho/quantidade de bolhas e regime de escoamento;  
- FGI tende a ser atraente offshore por compactação e flexibilidade; FGD oferece microbolhas e controle fino, mas pode custar mais em espaço e operação;  
- química de desestabilização pode ser decisiva quando a emulsão é estável;  
- skimming não é acessório: é parte funcional da separação, pois a remoção do óleo no topo fecha o balanço do processo;  
- TOG é o indicador operacional central do descarte, mas a leitura desse indicador deve considerar as limitações intrínsecas da flotação para compostos dissolvidos.  
**Fontes:** `regis-5cbc251ea81156e88d920048:pNone:2961.0-3163.0`, `regis-5cbc251ea81156e88d920048:pNone:3824.0-4082.0`, `regis-5f8888d1c91c7261ea300be9:pNone:5389.0-5596.0`, `petroles-4ee4bce16acf674505c8912d:pNone:403116.0-403203.0`, `petroles-004c2afadba7ea17c7dd7908:pNone:1753803.0-1753840.0`