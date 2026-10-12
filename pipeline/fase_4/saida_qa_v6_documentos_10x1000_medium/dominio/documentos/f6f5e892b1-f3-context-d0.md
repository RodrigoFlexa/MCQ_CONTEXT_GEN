# Desaeração e oxigênio dissolvido em sistemas de água do mar para injeção

## 1. Finalidade da desaeração no sistema de injeção
**Fontes:** `regis-2abff12c300b2f0d5a6ea665:pNone:0.0-39.0`, `regis-b478d29fcb19d1d6be3194bc:pNone:176.60-224.0`

Em sistemas de captação, tratamento e injeção de água do mar, a desaeração tem como objetivo principal reduzir a corrosividade da água antes de sua passagem por bombas, tubulações, vasos e linhas de injeção, especialmente quando a metalurgia predominante é aço-carbono. O racional técnico apresentado nas fontes é que o controle de corrosão por remoção de oxigênio dissolvido tende a ser mais econômico do que depender apenas de inibidores de corrosão ou de materiais mais nobres.

Além da integridade dos equipamentos, a desaeração também protege a injetividade do reservatório. Produtos de corrosão gerados a jusante do tratamento podem ser arrastados para a formação e contribuir para tamponamento/plugueamento, com impacto em perda de injetividade, necessidade de limpeza e redução da continuidade operacional.

As fontes destacam ainda que, para água do mar, é comum combinar:
- **remoção física do oxigênio dissolvido**; e
- **tratamento químico complementar**, para atingir especificações mais severas.

Em formulação histórica citada nas fontes, uma água aceitável para injeção deveria apresentar **oxigênio dissolvido inferior a 0,05 ppm** (50 ppb), além de não ser corrosiva, não incrustar nas condições de operação e ser compatível com a água da jazida.

## 2. Mecanismo de corrosão associado ao oxigênio dissolvido
**Fontes:** `regis-2abff12c300b2f0d5a6ea665:pNone:0.0-39.0`

A corrosão do aço em água do mar é descrita nas fontes como controlada pela redução catódica do oxigênio dissolvido, acoplada à dissolução anódica do ferro:

- reação catódica: **2H2O + O2 + 4e- -> 4OH-**
- reação anódica: **2Fe0 -> 2Fe2+ + 4e-**

Como o oxigênio está dissolvido na fase aquosa, a taxa de corrosão depende da velocidade com que esse oxigênio chega à superfície metálica. Em sistemas dinâmicos de injeção, a velocidade da água aumenta a transferência de massa de oxigênio para o aço e, portanto, eleva a corrosão.

As fontes fornecem relações empíricas para a razão de corrosão em função da velocidade da água `V`:

- **mpy = 0,057 V^(7/8) + 0,4**
- para superfícies abrasadas por finos, como areia e silte: **mpy = 11,4 V^(7/8) + 63**

Essas equações são usadas nas fontes para justificar a necessidade de reduzir o oxigênio dissolvido para valores inferiores a **50 ppb**. Também é ressaltado que tais relações **não consideram o fator de piteamento**, que pode multiplicar a severidade da corrosão de forma importante.

Consequência prática para projeto e operação offshore:
- água do mar aerada é inadequada para manuseio em aço-carbono comum sem proteção adicional;
- a eficiência da desaeração afeta diretamente a seleção de materiais ao longo do trem de tratamento;
- falhas de desaeração elevam simultaneamente risco de corrosão generalizada, piteamento e geração de partículas de ferro.

## 3. Interação entre oxigênio dissolvido e cloro residual
**Fontes:** `regis-2abff12c300b2f0d5a6ea665:pNone:0.0-39.0`, `regis-2abff12c300b2f0d5a6ea665:pNone:40.0-81.0`

O sistema de tratamento de água do mar normalmente também emprega cloração ou hipoclorito para controle biológico. As fontes alertam que cloro/hipoclorito agem, do ponto de vista corrosivo, de forma análoga ao oxigênio, como oxidantes e despolarizadores.

É apresentada a equivalência:

- **0,23 x Cl2 dissolvido = O2 equivalente em ação corrosiva**

Com base nessa equivalência, as fontes recomendam:
- manter **cloro residual em torno de 0,5 ppm** na parte ainda aerada do sistema, para controle biológico;
- **após a desaeração**, a soma do oxigênio dissolvido com o cloro residual equivalente deve ser **inferior a 50 ppb**, considerando a equivalência acima.

Implicações operacionais:
- excesso de cloro residual na entrada da torre de desaeração pode piorar o potencial corrosivo remanescente;
- cloro residual excessivo também pode interferir no consumo de desoxigenantes químicos, competindo com o oxigênio na reação com bissulfito/sulfito;
- cloro residual insuficiente, por outro lado, favorece proliferação biológica no sistema de captação e pré-tratamento.

## 4. Processos físicos de desaeração
**Fontes:** `regis-2abff12c300b2f0d5a6ea665:pNone:0.0-39.0`, `regis-2abff12c300b2f0d5a6ea665:pNone:40.0-81.0`, `regis-2abff12c300b2f0d5a6ea665:pNone:58.60-100.0`, `regis-b478d29fcb19d1d6be3194bc:pNone:176.60-224.0`

As fontes citam três abordagens de desaeração física:
- **stripping a gás em contracorrente**;
- **desaeração a vácuo**;
- **gas-lift** (mencionado como não utilizado comercialmente, à época da fonte).

As mesmas fontes também registram que a desaeração para água do mar de injeção é, em geral, feita por via **mecânica e química**, para alcançar o teor de oxigênio desejado.

### 4.1 Stripping a gás em contracorrente
A remoção do oxigênio dissolvido é descrita como regida pela **Lei de Henry**. Em uma torre, a água é distribuída na parte superior e escoa em cascata, enquanto o gás sobe pela parte inferior, maximizando a área de contato e promovendo dessorção do oxigênio.

Características citadas:
- gás de stripping pode ser **nitrogênio** ou **gás natural isento de gases ácidos**, como H2S e CO2;
- torres podem ser de **bandejas** ou com **enchimento** (anéis/selas);
- valores usuais de oxigênio dissolvido após o processo: **inferiores a 0,5 ppm**, tipicamente **0,05 a 0,2 ppm**.

Vantagens apontadas para uso offshore:
- operação relativamente simples;
- pouca manutenção;
- boa eficiência para o objetivo primário de desaeração;
- menor ocupação de espaço e peso mais favorável que sistemas a vácuo.

Limitação principal:
- necessidade de disponibilidade de gás adequado e isento de componentes ácidos.

### 4.2 Desaeração a vácuo
É indicada nas fontes para cenários em que:
- não há disponibilidade de gás;
- o uso de nitrogênio não é economicamente atraente;
- o gás disponível contém componentes ácidos, como H2S e/ou CO2.

Características citadas:
- torres de bandejas ou recheio em múltiplos estágios;
- necessidade de bombas de vácuo capazes de manusear vapor d'água juntamente com oxigênio e outros gases removidos.

Limitações operacionais importantes:
- tendência a **falsas entradas de ar**, que degradam a eficiência de desaeração;
- necessidade de **controle de espumas**;
- necessidade de acompanhar o equilíbrio **CO2-carbonato-bicarbonato**;
- maior peso e maior ocupação de espaço, o que reduz sua atratividade em FPSOs e outras instalações offshore.

As fontes ainda observam que, em certas condições, a remoção de CO2 pode desequilibrar esse sistema e **teoricamente precipitar cerca de 10 mg/L de carbonato de cálcio** em água do mar.

### 4.3 Sistema misto
Quando existe alguma disponibilidade de gás, as fontes consideram atrativa uma solução combinando vácuo e stripping. O arranjo descrito utiliza:
- um primeiro estágio com vácuo parcial;
- um segundo estágio com vácuo maior, auxiliado por stripping a gás.

Resultado informado nas fontes:
- oxigênio dissolvido de até **15 ppb**, reduzindo a carga sobre o desoxigenante químico e aproximando o teor de zero dentro da precisão analítica disponível.

Exemplo citado na fonte:
- primeira etapa: **100 mmHg**;
- segunda etapa: **46 mmHg**;
- com injeção de gás natural isento de gases ácidos.

## 5. Critérios de seleção do processo em FPSO/instalação offshore
**Fontes:** `regis-2abff12c300b2f0d5a6ea665:pNone:40.0-81.0`, `regis-2abff12c300b2f0d5a6ea665:pNone:58.60-100.0`

As fontes organizam a escolha do processo de desaeração em cinco grupos de fatores.

### 5.1 Condições existentes
Devem ser levantados, no mínimo:
- tipo de água;
- temperatura da água e do ambiente;
- teor de oxigênio dissolvido na alimentação;
- disponibilidade de gás natural e sua qualidade;
- possibilidade de obtenção/geração de nitrogênio e custo associado;
- localização da planta, em terra ou no mar.

### 5.2 Especificação requerida da água tratada
A escolha do processo não depende apenas de atingir um número de oxigênio dissolvido. Ela deve considerar também quanto da corrosão residual ainda contribuirá para geração de sólidos e para risco de tamponamento da formação.

Exemplo apresentado nas fontes:
- para testemunhos com **10 mD** de permeabilidade à água, admite-se **1 mg/L** de sólidos como nível de início de tamponamento;
- se o oxigênio dissolvido for mantido em **50 ppb**, a corrosão teoricamente contribuiria com **0,3 mg/L** de sólidos na água;
- por isso, a água deve ser filtrada para reduzir **STS** a valores **inferiores a 0,7 mg/L**, ainda sem coeficiente de segurança.

Essa lógica mostra que o controle de oxigênio dissolvido e o desempenho da filtração não podem ser avaliados separadamente: a corrosão a jusante gera carga sólida adicional que consome a margem de qualidade da água de injeção.

### 5.3 Condições operacionais
Em FPSOs, destacam-se:
- espaço disponível;
- grau de automação;
- facilidade de controle da qualidade da água;
- robustez para manter a especificação ao longo do tempo.

As fontes enfatizam que torres a vácuo podem permitir com mais facilidade entradas parasitas de ar, o que penaliza a confiabilidade operacional.

### 5.4 Manutenção e continuidade de injeção
A injeção de água deve operar com alto percentual de disponibilidade. Portanto, a solução escolhida deve ser sustentável ao longo dos anos, com manutenção compatível com o regime operacional da unidade e com o objetivo de injeção contínua.

### 5.5 Materiais disponíveis
A seleção de materiais deve ser consistente com o perfil de oxigênio ao longo do sistema. As fontes associam diretamente a necessidade de materiais mais resistentes às regiões em que a água ainda permanece aerada ou parcialmente tratada.

### 5.6 Síntese decisória indicada nas fontes
De forma geral:
- **stripping a gás** é preferível quando existe gás sem componentes ácidos, facilidade de queima segura e restrição de espaço;
- **vácuo** tende a ser opção quando não há gás disponível e o espaço não é limitante;
- **sistema misto** torna-se atrativo quando há alguma disponibilidade de gás doce e se busca teor de O2 mais baixo com menor consumo de sequestrante químico.

As fontes recomendam ainda a construção/operação de **instalação piloto** para estudo de variáveis operacionais, otimização e treinamento, antes da consolidação do processo definitivo.

## 6. Complementação química da desaeração
**Fontes:** `regis-2abff12c300b2f0d5a6ea665:pNone:0.0-39.0`, `regis-2abff12c300b2f0d5a6ea665:pNone:40.0-81.0`, `regis-b478d29fcb19d1d6be3194bc:pNone:176.60-224.0`

As fontes afirmam que, em água do mar, a prática usual é combinar desaeração mecânica com **desoxigenação química complementar**. O motivo é econômico e operacional:
- o processo físico, isoladamente, pode não alcançar a especificação final exigida;
- o tratamento químico sozinho tende a ser menos econômico.

No texto, são citados **bissulfito** ou **sulfito** como desoxigenantes químicos. A função desses reagentes é consumir o oxigênio residual após a etapa física, reduzindo a corrosão remanescente a níveis aceitáveis.

Do ponto de vista operacional, o consumo do desoxigenante químico aumenta quando:
- a desaeração física perde desempenho;
- há entrada falsa de ar na torre ou nas linhas subsequentes;
- chega cloro residual excessivo à etapa de inibição química, pois esse oxidante compete com o oxigênio.

Assim, o controle eficiente da etapa física diminui custo químico, melhora estabilidade do processo e reduz variabilidade de qualidade da água injetada.

## 7. Monitoramento e controle da qualidade da água após a desaeração
**Fontes:** `regis-2abff12c300b2f0d5a6ea665:pNone:40.0-81.0`, `regis-2abff12c300b2f0d5a6ea665:pNone:58.60-100.0`

As fontes tratam a desaeração como um processo que deve ser acompanhado por um conjunto de indicadores, e não apenas por uma leitura isolada de oxigênio dissolvido.

### 7.1 Oxigênio dissolvido
- **controle contínuo**: monitor do tipo Oxymeter com célula de eletrodo de ouro;
- **verificação periódica por via úmida**: reação da Rodazina D, com mudança de cor do amarelo claro para violeta, observável por comparação visual, colorímetro ou espectrofotômetro de campo.

### 7.2 Turbidez
Medida continuamente pela passagem de fluxo de água por feixe luminoso controlado. É um indicador indireto de alteração de qualidade da água e pode sinalizar degradação do sistema de tratamento.

### 7.3 Sólidos totais em suspensão (STS)
Controle periódico por filtração em membrana **0,45 micrômetros**, especialmente quando houver suspeita de mudança da qualidade da água captada ou em tratamento.

### 7.4 Corrosão e piteamento
Alguns sistemas controlam:
- **teor de ferro total**;
- **razão de corrosão**;
- **pitting factor**;
com uso de monitores contínuos por eletrodos energizados.

### 7.5 Cloro residual e equilíbrio carbonático
Medições adicionais relevantes:
- **cloro residual** na entrada da torre, para verificar se o controle biológico está adequado sem penalizar a desoxigenação química;
- em sistemas a vácuo, avaliação do equilíbrio **CO2/CO3(2-)/HCO3(-)** para evitar efeitos colaterais como precipitação de carbonato.

## 8. Relação entre oxigênio dissolvido, corrosão e sólidos que chegam à formação
**Fontes:** `regis-2abff12c300b2f0d5a6ea665:pNone:40.0-81.0`, `regis-b478d29fcb19d1d6be3194bc:pNone:176.60-224.0`

O controle do oxigênio dissolvido deve ser entendido não apenas como proteção metalúrgica, mas como requisito de qualidade da água para preservar a injetividade.

Encadeamento causal resumido:
1. aumento de O2 dissolvido ->
2. aumento de corrosão em aço-carbono ->
3. geração de produtos de corrosão/ferro em suspensão ->
4. aumento de STS e risco de deposição ->
5. maior probabilidade de tamponamento da formação e queda de injetividade.

Por isso, a decisão sobre o limite de oxigênio não deve ser feita isoladamente. Ela precisa considerar:
- permeabilidade e sensibilidade do reservatório;
- especificação de sólidos da água injetada;
- capacidade real de filtração a jusante;
- possibilidade de corrosão localizada e geração intermitente de partículas, especialmente em transientes operacionais.

## 9. Efeito da desaeração sobre risco microbiológico e necessidade de controle complementar
**Fontes:** `regis-b478d29fcb19d1d6be3194bc:pNone:176.60-224.0`

As fontes alertam para um efeito colateral importante: ao eliminar o oxigênio dissolvido, cria-se ambiente favorável à proliferação de **bactérias anaeróbias**, incluindo sulfato-redutoras. Essas bactérias podem:
- agravar a corrosão;
- formar sulfetos de ferro em suspensão;
- contribuir para tamponamento da jazida.

Logo, a desaeração não elimina a necessidade de controle microbiológico. Pelo contrário, ela exige integração com estratégias de:
- esterilização química/biocidas;
- controle de matéria orgânica microscópica;
- monitoramento de qualidade da água ao longo do tempo.

## 10. Implicações práticas para operação e otimização em FPSO
**Fontes:** `regis-2abff12c300b2f0d5a6ea665:pNone:0.0-39.0`, `regis-2abff12c300b2f0d5a6ea665:pNone:40.0-81.0`, `regis-2abff12c300b2f0d5a6ea665:pNone:58.60-100.0`, `regis-b478d29fcb19d1d6be3194bc:pNone:176.60-224.0`

Para fins de projeto, operação e otimização, o material sugere os seguintes princípios técnicos:

1. **Definir a meta de O2 a partir do risco combinado de corrosão e dano à formação**, e não apenas por convenção operacional.
2. **Avaliar conjuntamente O2 dissolvido e cloro residual**, usando a equivalência corrosiva indicada nas fontes.
3. **Preferir stripping a gás em unidades offshore** quando houver gás doce disponível e espaço/peso forem restritivos.
4. **Tratar torres a vácuo como soluções mais sensíveis à integridade do sistema**, por risco de falsa entrada de ar e maior penalidade de espaço/peso.
5. **Usar tratamento químico como complemento**, não como substituto automático da boa performance da etapa física.
6. **Correlacionar desempenho de desaeração com STS, turbidez, ferro total e taxa de corrosão**, para distinguir baixa eficiência de remoção de O2 de outros problemas do sistema.
7. **Controlar microbiologia em paralelo**, pois água desoxigenada continua podendo causar dano por atividade anaeróbia.
8. **Preservar continuidade de injeção**, escolhendo um arranjo que seja tecnicamente eficaz e operacionalmente sustentável no regime de manutenção do FPSO.

## 11. Síntese técnica
**Fontes:** `regis-2abff12c300b2f0d5a6ea665:pNone:0.0-39.0`, `regis-2abff12c300b2f0d5a6ea665:pNone:40.0-81.0`, `regis-2abff12c300b2f0d5a6ea665:pNone:58.60-100.0`, `regis-b478d29fcb19d1d6be3194bc:pNone:176.60-224.0`

A desaeração é um elemento central do tratamento de água do mar para injeção, porque o oxigênio dissolvido controla a corrosividade da água em sistemas de aço-carbono e, indiretamente, a geração de sólidos que prejudicam a injetividade. Em termos de seleção de processo, as fontes favorecem o **stripping a gás** em cenários offshore com disponibilidade de gás doce e restrição de espaço, reservando **vácuo** para contextos sem gás disponível e admitindo **sistemas mistos** quando se buscam teores mais baixos de O2.

O controle eficaz não se limita ao valor de oxigênio dissolvido: deve incluir cloro residual, STS, turbidez, corrosão, ferro total e, quando aplicável, efeitos sobre equilíbrio carbonático e microbiologia. A condição operacional desejável é manter a água tratada com potencial corrosivo suficientemente baixo para proteger equipamentos e evitar geração de sólidos a jusante, preservando simultaneamente a qualidade requerida para a formação.