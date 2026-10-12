# Tratamento e estabilização do óleo em FPSOs

## 1. Finalidade do condicionamento do óleo

Em FPSOs, o processamento primário tem como objetivo separar gás, óleo e água e, em plantas mais completas, **condicionar e estabilizar o óleo** para que ele possa ser **armazenado, transferido e exportado** dentro de especificações técnicas aceitáveis. No contexto dos trechos fornecidos, isso significa sobretudo:

- reduzir **água e sedimentos** no óleo;
- reduzir **sais dissolvidos** arrastados com a água produzida;
- remover parte dos **hidrocarbonetos leves/gás associado** para tornar o óleo mais adequado ao armazenamento em tanques e ao offloading;
- mitigar problemas de corrosão, formação de depósitos, perda de capacidade de tancagem e dificuldades no refino.

Os materiais indicam valores **típicos** de especificação para o óleo após tratamento:

- **BS&W**: até **1,0% vol** para refino/consumo interno e até **0,5% vol** para exportação;
- **teor de sais**: até **570 mg/L** (como NaCl) para refino/consumo interno e até **285 mg/L** para exportação.

BS&W é a propriedade usada para verificar a presença de **água e sedimentos** no óleo; os sais são relevantes porque estão majoritariamente dissolvidos na fase aquosa co-produzida. Logo, controlar água e sais é, na prática, parte do mesmo problema de tratamento.

_Fuentes: regis-ef7d62eda3748119ba3e9e9e:pNone:874.0-1072.0, regis-2b32d20fca156fd1142e4bec:pNone:3225.0-3420.0, petroles-4ee4bce16acf674505c8912d:pNone:1447310.60-1447355.0, regis-f96d8b534287b9dfd7921821:pNone:4242.0-4444.0_

## 2. Posição do tratamento do óleo dentro da planta de processo

Os fluidos produzidos chegam ao FPSO a partir dos poços via **risers** e, conforme a arquitetura submarina do campo, podem ser centralizados por **manifolds** antes do envio à unidade. A planta pode ser mais simples ou mais complexa, dependendo das propriedades dos fluidos e da estratégia de projeto para entregar ou não hidrocarbonetos já enquadrados offshore.

Nos exemplos fornecidos, aparecem duas arquiteturas típicas:

1. **arranjo simplificado de óleo**:
   - separador trifásico de alta pressão;
   - separador bifásico de baixa pressão;
   - tratador eletrostático;
   - medição e envio aos tanques de carga;

2. **arranjo mais elaborado**:
   - separador de água livre/separador trifásico;
   - aquecimento em trocadores;
   - primeiro degaseificador;
   - primeiro tratador eletrostático;
   - segundo degaseificador;
   - segundo tratador eletrostático;
   - tanques de carga.

Esses arranjos mostram um ponto central: **o condicionamento do óleo não ocorre em um único equipamento**, mas em uma sequência de operações que combinam separação gravitacional, aquecimento, redução de pressão, desemulsificação e decantação.

_Fuentes: petroles-4ee4bce16acf674505c8912d:pNone:1447310.60-1447355.0, regis-95ab3f5dbd0879a0e75967a9:pNone:74.0-104.0, regis-2b32d20fca156fd1142e4bec:pNone:3225.0-3420.0_

## 3. Sequência típica de tratamento e estabilização do óleo

### 3.1 Separação primária: remoção inicial de gás e água livre

O primeiro vaso da planta costuma ser um **separador trifásico/gravitacional** ou separador de água livre. Nele, o fluido permanece por tempo de residência suficiente para promover a segregação por diferença de densidade:

- o **gás** sai pelo topo;
- a **água** sai pela parte inferior e segue para tratamento de água produzida;
- o **óleo** sai por uma tomada intermediária para estágios posteriores.

Essa etapa é necessária, mas **não é suficiente** para enquadrar o óleo. Os próprios trechos destacam que, após a separação inicial, ainda existe:

- óleo arrastado na água;
- água e gás dissolvido/arrastado no óleo;
- água e hidrocarbonetos pesados no gás.

Ou seja, a separação primária é um **pré-condicionamento**, não o produto final.

_Fuentes: regis-2b32d20fca156fd1142e4bec:pNone:3225.0-3420.0, regis-f96d8b534287b9dfd7921821:pNone:4242.0-4444.0, regis-8bb1e427d3fe8d93d0c370d9:pNone:1165.0-1399.0_

### 3.2 Aquecimento do óleo

Após a separação primária, o óleo pode passar por **trocadores de calor** para elevar sua temperatura antes dos vasos subsequentes. Os trechos indicam duas funções principais desse aquecimento:

- **reduzir a viscosidade** do óleo e da emulsão óleo/água, facilitando a coalescência e a decantação da água;
- **evitar ou reduzir problemas de cera/parafina** nos equipamentos de separação.

Em um dos arranjos descritos, parte do aquecimento é obtida por **recuperação de calor** do próprio processo e por um sistema de água quente alimentado por **WRHU (Waste Heat Recovery Unit)** associado aos gases de exaustão de turbinas a gás.

Do ponto de vista operacional, maior temperatura tende a melhorar a separação até certo ponto porque reduz a viscosidade; porém o valor ótimo depende do óleo, da estabilidade da emulsão e do arranjo da planta. Os trechos trazem faixas operacionais exemplificativas para certos casos, mas não estabelecem um valor universal para todo FPSO.

_Fuentes: regis-2b32d20fca156fd1142e4bec:pNone:3225.0-3420.0, petroles-4ee4bce16acf674505c8912d:pNone:1447310.60-1447355.0, regis-f96d8b534287b9dfd7921821:pNone:4242.0-4444.0, regis-8bb1e427d3fe8d93d0c370d9:pNone:1165.0-1399.0_

### 3.3 Redução de pressão e degaseificação

A estabilização do óleo, no material disponível, inclui a **remoção progressiva de frações leves** por estágios de menor pressão. Em um dos exemplos, após o aquecimento o óleo segue para pares de:

- **degaseificador**;
- **tratador eletrostático**.

No primeiro degaseificador, operando a pressão menor que o separador primário, ocorre liberação adicional de hidrocarbonetos leves. O gás liberado segue para uma **Unidade de Recuperação de Vapor (URV)**. Um segundo par de vasos opera a pressão ainda mais baixa, ampliando a separação antes do envio aos tanques de carga.

Esse escalonamento de pressão atende a dois objetivos práticos:

- **reduzir gás retido no óleo**, tornando-o mais adequado ao armazenamento;
- **aprimorar a separação água/óleo** nas etapas seguintes.

Em outra fonte, a separação em estágios de alta, intermediária e baixa pressão é apresentada como estratégia típica para maximizar recuperação de óleo e acomodar correntes com diferentes pressões de escoamento.

_Fuentes: regis-2b32d20fca156fd1142e4bec:pNone:3225.0-3420.0, regis-ef7d62eda3748119ba3e9e9e:pNone:874.0-1072.0_

### 3.4 Tratamento eletrostático: ajuste fino do BSW e dos sais

O **tratador eletrostático** é o equipamento-chave de ajuste fino do óleo. Seu princípio, conforme os trechos, baseia-se em um **campo elétrico** aplicado entre placas internas polarizadas. Como as gotículas de água são polares e condutoras em relação ao meio oleoso, o campo provoca:

1. deformação/alongamento das gotículas;
2. aproximação e atração entre gotículas vizinhas;
3. enfraquecimento da película estabilizante da emulsão;
4. **coalescência** em gotas maiores;
5. **decantação** da água para o fundo do vaso.

O óleo tratado é retirado pela parte superior. Como os sais estão predominantemente dissolvidos na água produzida, a remoção da água emulsionada também promove o **enquadramento do teor de sal**.

Em casos de óleo com teor salino elevado, uma referência indica que pode ser necessária a **adição de água fresca** ao óleo para diluir/dessorver sais e facilitar a dessalgação subsequente. O conceito importante é que **dessalgar o óleo implica primeiro lidar corretamente com a água associada**.

_Fuentes: regis-2b32d20fca156fd1142e4bec:pNone:3225.0-3420.0, petroles-4ee4bce16acf674505c8912d:pNone:1447310.60-1447355.0, regis-ef7d62eda3748119ba3e9e9e:pNone:874.0-1072.0_

## 4. Água no petróleo: formas, efeitos e implicações para o FPSO

A água associada ao petróleo pode aparecer como:

- **água livre**: mais fácil de remover por gravidade;
- **água emulsionada**: requer tratamento específico;
- **água solúvel/dissolvida**: em geral presente em baixos teores.

Para o condicionamento do óleo em FPSO, o principal desafio é a **água emulsionada**, pois ela carrega sais e sedimentos e resiste à separação simples por gravidade.

As consequências de não remover adequadamente essa água incluem:

- **corrosão** em tanques, dutos e equipamentos;
- aumento do volume não comercial de líquido enviado para bombeamento, tancagem e transporte;
- piora do dimensionamento e da eficiência do sistema de bombeio/transferência;
- formação de **depósitos salinos** e incrustações em trocadores e unidades de refino;
- possibilidade de formação de **HCl** a partir de cloretos em processos térmicos de refino, com efeitos corrosivos;
- penalização da qualidade do produto entregue ao cliente ou à refinaria.

Portanto, do ponto de vista de processo, retirar água e sais não é apenas atender uma especificação comercial: é também proteger a integridade do FPSO, reduzir perdas operacionais e evitar problemas a jusante.

_Fuentes: petroles-4ee4bce16acf674505c8912d:pNone:1463376.0-1463412.0, regis-ef7d62eda3748119ba3e9e9e:pNone:874.0-1072.0_

## 5. Formação e estabilidade de emulsões óleo/água

Uma emulsão se forma quando dois líquidos imiscíveis, como óleo e água, são submetidos a agitação e cisalhamento suficientes para dispersar uma fase na outra em forma de gotículas. No petróleo, a emulsão mais comum é **água em óleo**.

Os trechos relacionam a estabilidade dessa emulsão aos seguintes fatores:

- **agentes emulsificantes naturais do petróleo**, como asfaltenos, resinas, parafinas e compostos oxigenados;
- **sólidos finos** e sedimentos, como argilas;
- **intensidade de cisalhamento** a que o fluido foi submetido;
- **viscosidade da emulsão**;
- **temperatura**;
- **grau API do petróleo**;
- quantidade de **água livre** e sua **salinidade**;
- escolha de métodos de elevação e arranjos de produção que imponham maior ou menor cisalhamento ao fluido.

Quanto mais viscosa e estável a emulsão, mais difícil é sua quebra. Por isso, o tratamento do óleo combina:

- calor;
- tempo de residência;
- campo elétrico;
- uso de **desemulsificantes** para reduzir a tensão interfacial e enfraquecer o filme interfacial.

Em termos de decisão operacional, isso significa que um aumento de BSW na saída do tratamento pode não ser um problema apenas do tratador eletrostático: a causa pode estar também em **cisalhamento excessivo a montante**, mudança de composição do fluido, aumento de sólidos, queda de temperatura ou espuma.

_Fuentes: petroles-4ee4bce16acf674505c8912d:pNone:1463376.0-1463412.0, petroles-4ee4bce16acf674505c8912d:pNone:1447310.60-1447355.0, regis-ef7d62eda3748119ba3e9e9e:pNone:874.0-1072.0_

## 6. Aspectos construtivos e funcionais dos separadores relevantes para a qualidade do óleo

Os separadores de produção possuem seções internas com funções distintas. Nos trechos, aparecem quatro regiões típicas:

- **seção de separação primária**: impacto em defletores/difusores e queda inicial de velocidade;
- **seção de separação secundária**: decantação de gotículas ainda arrastadas;
- **seção de acumulação de líquido**: retenção suficiente para liberação de gás e, em vasos trifásicos, segregação adicional de água;
- **seção de aglutinação/coalescência** na saída de gás: remoção de líquido remanescente por grande área de contato.

Esses detalhes são importantes porque a qualidade do óleo depende não apenas da química e da temperatura, mas também de:

- tempo de residência efetivo;
- estabilidade de nível e interface;
- distribuição de fluxo dentro do vaso;
- capacidade do equipamento frente à vazão de entrada.

Separadores horizontais tendem a favorecer a separação gás/líquido pela maior área superficial, podendo ser úteis em correntes com espuma e alta razão gás/óleo. Em contrapartida, podem ter maior dificuldade de lidar com remoção de sólidos e com grandes variações de vazão. Já os verticais facilitam a deposição localizada de sólidos no fundo.

_Fuentes: regis-f96d8b534287b9dfd7921821:pNone:4242.0-4444.0, regis-8bb1e427d3fe8d93d0c370d9:pNone:1165.0-1399.0_

## 7. Problemas operacionais que degradam o enquadramento do óleo

### 7.1 Espuma

A presença de espuma dificulta o controle de nível nos vasos, reduz a área efetiva de escoamento do gás e aumenta o risco de arraste de líquido para a saída de gás ou de descontrole operacional. Os trechos associam espuma a impurezas do líquido e indicam que aquecimento e, quando aplicável, antiespumante podem reduzir o problema.

### 7.2 Areia e sólidos

Areia e outros sólidos podem causar:

- corrosão de válvulas;
- obstrução de saídas e drenos;
- piora do controle de nível/interface;
- maior estabilidade de emulsão ao atuar como particulados interfaciais.

A remoção contínua por drenos é citada como prática de mitigação.

### 7.3 Parafinas/cera

Se a temperatura cair abaixo da condição de aparecimento de parafina, podem ocorrer cristalização e deposição, com obstrução de linhas e saídas dos separadores. Isso reforça o papel do aquecimento não apenas na quebra de emulsão, mas também na **manutenção da escoabilidade**.

### 7.4 Arraste de óleo pelo gás ou de gás pelo óleo

O arraste pode ocorrer por:

- nível excessivo de líquido;
- espuma;
- obstrução da saída de líquido por areia ou parafina;
- subdimensionamento do separador em relação à vazão de alimentação.

Na prática, esses fenômenos afetam diretamente o óleo tratado, porque aumentam a instabilidade do processo e reduzem a eficiência global de separação.

_Fuentes: petroles-4ee4bce16acf674505c8912d:pNone:1447310.60-1447355.0, regis-f96d8b534287b9dfd7921821:pNone:4242.0-4444.0, regis-8bb1e427d3fe8d93d0c370d9:pNone:1165.0-1399.0_

## 8. Critérios práticos para diagnosticar óleo fora de especificação

Com base nos mecanismos descritos nas fontes, uma análise profissional do óleo fora de especificação pode seguir a lógica abaixo.

### 8.1 BSW alto na saída do tratamento

Verificar, em primeiro nível:

- **temperatura** insuficiente do óleo/alimentação;
- aumento de **viscosidade** ou mudança de composição do cru;
- dosagem inadequada de **desemulsificante**;
- instabilidade operacional no separador/tratador (nível, interface, tempo de residência);
- presença de **espuma**, sólidos ou parafinas;
- maior **cisalhamento a montante**, formando emulsão mais estável;
- baixa eficiência do campo elétrico/coalescência no tratador.

### 8.2 Teor de sal alto com BSW aparentemente controlado

Isso sugere que ainda permanece água salina associada ao óleo ou que a dessalgação está ineficiente. Os trechos indicam que:

- o sal está majoritariamente na fase aquosa;
- remover água emulsionada ajuda a reduzir sal;
- em algumas situações pode ser necessária adição de água para lavagem/diluição dos sais antes da separação.

### 8.3 Óleo com excesso de gás/light ends para armazenamento

Nessa situação, devem ser avaliados:

- a eficiência dos estágios de redução de pressão/degaseificação;
- a pressão de operação dos vasos;
- o encaminhamento do gás liberado para recuperação/compressão.

Isso é especialmente importante em FPSOs porque o óleo segue para **tanques de carga**, e a presença de frações leves afeta a estabilidade operacional do armazenamento e da transferência.

_Fuentes: regis-2b32d20fca156fd1142e4bec:pNone:3225.0-3420.0, regis-ef7d62eda3748119ba3e9e9e:pNone:874.0-1072.0, petroles-4ee4bce16acf674505c8912d:pNone:1447310.60-1447355.0, petroles-4ee4bce16acf674505c8912d:pNone:1463376.0-1463412.0, regis-f96d8b534287b9dfd7921821:pNone:4242.0-4444.0_

## 9. Armazenamento em tanques de carga e impacto no offloading

Após o enquadramento, o óleo passa pelo sistema de medição e segue aos **tanques de carga** até o offloading para navio aliviador. Um ponto operacional relevante trazido nas fontes é que o tanque pode funcionar, por tempo de residência mais longo, como um **grande separador bifásico óleo-água**, permitindo decantação adicional e eventual redução do BS&W antes da transferência.

Esse efeito pode aliviar pequenas oscilações de qualidade entre a saída do tratamento e o momento do offloading, mas **não substitui** o tratamento adequado na planta. Confiar apenas na decantação em tanque aumenta risco de:

- ocupação de volume útil com água;
- corrosão em tancagem;
- incerteza de qualidade no momento da exportação;
- necessidade posterior de manejo da água separada.

Assim, o papel dos tanques é melhor entendido como **amortecimento operacional e decantação complementar**, não como etapa principal de enquadramento.

_Fuentes: petroles-4ee4bce16acf674505c8912d:pNone:1447310.60-1447355.0, petroles-4ee4bce16acf674505c8912d:pNone:2060884.0-2060913.0_

## 10. Síntese técnica

O condicionamento do óleo em FPSOs, nos materiais fornecidos, pode ser resumido como a combinação de:

- **separação gravitacional inicial** para retirar gás e água livre;
- **aquecimento** para reduzir viscosidade, melhorar decantação e reduzir problemas com parafinas;
- **redução escalonada de pressão** para degaseificação e estabilização do óleo antes da tancagem;
- **tratamento eletrostático** para quebrar emulsões, reduzir BSW e remover a água que carrega sais;
- **controle operacional** de temperatura, níveis, espuma, sólidos e química do processo;
- **verificação de qualidade** antes do armazenamento e do offloading.

O óleo tratado deve atender aos limites de água/sedimentos e sais compatíveis com sua destinação. Quando isso não ocorre, as causas mais prováveis envolvem emulsão mais estável, temperatura inadequada, baixa eficiência de coalescência, problemas de separação/nível nos vasos ou aumento de sólidos/espuma. Em termos profissionais, estabilizar e tratar o óleo em um FPSO é equilibrar **qualidade de produto, segurança operacional, capacidade de processamento e confiabilidade da exportação**.

_Fuentes: regis-ef7d62eda3748119ba3e9e9e:pNone:874.0-1072.0, regis-2b32d20fca156fd1142e4bec:pNone:3225.0-3420.0, petroles-4ee4bce16acf674505c8912d:pNone:1447310.60-1447355.0, petroles-4ee4bce16acf674505c8912d:pNone:1463376.0-1463412.0, regis-f96d8b534287b9dfd7921821:pNone:4242.0-4444.0, petroles-4ee4bce16acf674505c8912d:pNone:2060884.0-2060913.0_