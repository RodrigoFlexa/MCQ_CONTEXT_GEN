# Adoçamento e contaminantes ácidos

## 1. Finalidade do tratamento de H2S e CO2 no gás produzido
O adoçamento do gás é a etapa de tratamento voltada à redução de gases ácidos, principalmente **H2S** e **CO2**, para que a corrente atenda ao uso pretendido e não comprometa segurança, integridade e operação. Em termos gerais, o tratamento do gás natural busca: **(i)** separar líquidos livres e sólidos arrastados; e **(ii)** remover impurezas para cumprir especificações de venda, uso interno ou reinjeção, observadas as restrições ambientais e operacionais do sistema. A seleção, o projeto e a operação dos processos dependem das propriedades da corrente produzida e do destino do gás tratado.

No contexto de uma unidade offshore como FPSO, isso se traduz em compatibilizar o gás tratado com rotas como **gás combustível**, **compressão/reinjeção** e **exportação**, sem assumir que uma mesma solução seja ótima para todos os cenários.

**Fontes da seção:** `regis-b481bf065addf6ea2a64713f:pNone:337.60-359.0`, `petroles-4ee4bce16acf674505c8912d:pNone:424185.0-424231.0`

## 2. Por que a remoção pode ser necessária

### 2.1 Segurança de processo e saúde ocupacional
O **H2S** é destacado nas fontes como um gás de elevada toxicidade. Em concentrações suficientemente altas, a exposição pode levar rapidamente a coma e morte; em exposições menos intensas, pode causar sintomas neurológicos, respiratórios e irritativos. Por isso, a necessidade de remover H2S não é apenas comercial: ela também decorre de exigências de **manipulação segura** do gás e de redução do risco ocupacional.

### 2.2 Corrosão e integridade
As fontes associam teores elevados de **H2S e CO2** à deterioração da integridade dos equipamentos por **corrosão**, especialmente em sistemas de tratamento com aminas e em correntes contendo água. Assim, mesmo quando o gás não é destinado à venda, o adoçamento pode ser necessário para proteger colunas, trocadores, vasos, linhas, compressores e materiais de vedação.

### 2.3 Atendimento às especificações do gás tratado
A necessidade de remoção depende da **qualidade requerida do produto final**. As fontes ressaltam que as especificações variam com a finalidade do gás, e que operar a unidade para atender especificações restritivas de H2S e CO2 exige controle contínuo e delicado. Para um mesmo campo, a exigência pode mudar conforme o destino seja:
- consumo interno como gás combustível;
- exportação/venda;
- alimentação de unidade de recuperação de enxofre;
- reinjeção.

### 2.4 Pressão parcial e composição da alimentação
Um dos critérios mais citados para seleção do processo é a **pressão parcial do gás ácido** a ser removido. As fontes a descrevem como a contribuição do componente ácido para a pressão total do sistema. Em termos práticos, a decisão tecnológica e a severidade do tratamento variam com:
- teor de H2S;
- teor de CO2;
- razão H2S/CO2;
- pressão total e temperatura da alimentação;
- vazão de gás;
- presença de hidrocarbonetos pesados e outras impurezas.

**Fontes da seção:** `petroles-4ee4bce16acf674505c8912d:pNone:424185.0-424231.0`, `petroles-4ee4bce16acf674505c8912d:pNone:1409787.0-1409852.0`, `regis-b481bf065addf6ea2a64713f:pNone:337.60-359.0`

## 3. Critérios de decisão para selecionar a rota de adoçamento
As fontes convergem em que **não existe um processo universalmente ótimo**. A seleção depende de múltiplos fatores de processo, operação e economia. Entre os fatores explicitamente citados estão:
- tipo de impureza a remover;
- concentração das impurezas e grau de remoção desejado;
- pressão, temperatura e vazão da alimentação;
- presença de etano e hidrocarbonetos mais pesados;
- facilidade e necessidade de recuperar enxofre;
- custos de energia;
- disponibilidade do solvente;
- regulamentações ambientais;
- presença de N2;
- pressão requerida para o gás tratado;
- localização onshore/offshore;
- familiaridade com a tecnologia;
- investimento versus custo operacional.

Há também orientações gerais de seleção citadas nas fontes:
- **aminas** tendem a ser preferidas quando se precisa atingir **especificações restritivas**;
- **solventes físicos** tendem a ser mais atrativos quando a alimentação já está a **alta pressão** e/ou com **alta carga de gases ácidos**;
- **membranas** aparecem como alternativa especialmente para **altas concentrações de CO2** na carga;
- **processos não regenerativos** e **leitos sólidos** aparecem associados a certos casos de baixa a média carga de H2S ou mercaptanas.

Outro ponto importante é que as quantidades de **CO2 e H2S** influenciam fortemente a escolha do solvente, o número de estágios/pratos, a razão de refluxo do regenerador e até os **materiais de construção**.

**Fontes da seção:** `petroles-4ee4bce16acf674505c8912d:pNone:1409787.0-1409852.0`, `petroles-004c2afadba7ea17c7dd7908:pNone:400231.0-400272.0`, `petroles-4ee4bce16acf674505c8912d:pNone:424185.0-424231.0`, `regis-b481bf065addf6ea2a64713f:pNone:323.60-345.0`

## 4. Principais tecnologias e seu enquadramento técnico

### 4.1 Absorção química com aminas
É a rota mais detalhada nas fontes para remoção de H2S e CO2. O princípio é o contato do gás ácido com uma **solução aquosa de amina** em contracorrente numa coluna absorvedora. A absorção é descrita como **reação exotérmica**, favorecida por **baixas temperaturas** e, no arranjo descrito, com gás pressurizado. A solução rica em gases ácidos é depois regenerada por **stripping endotérmico** em condições opostas, com **baixa pressão** e **alta temperatura**, recuperando a amina pobre para recirculação.

#### Arranjo de processo descrito nas fontes
Fluxo típico:
1. gás ácido entra pelo fundo da absorvedora;
2. amina pobre entra pelo topo;
3. gás tratado sai no topo;
4. amina rica sai no fundo;
5. amina rica passa por **vaso flash** para remoção de hidrocarbonetos absorvidos;
6. passa por **trocador rico/pobre** para recuperação de calor;
7. entra na coluna regeneradora;
8. o topo do regenerador libera corrente ácida rica em H2S/CO2;
9. a amina pobre de fundo é bombeada, filtrada, resfriada e recirculada.

O regenerador é citado como coluna de pratos ou recheio com **condensador de topo**, **refervedor no fundo** e, normalmente, **refluxo no topo**.

#### Solventes amínicos citados
As fontes citam, entre outros:
- **MEA** (monoetanolamina);
- **DEA** (dietanolamina);
- **MDEA** (metildietanolamina);
- **DGA** (diglicolamina);
- **TEA** (trietanolamina, mencionada de forma histórica e com limitações de capacidade/reatividade).

Aspectos comparativos mencionados:
- **MEA e DEA**: alta reatividade para remoção de gases ácidos;
- **MDEA**: maior estabilidade e menores perdas relativas; importante para remoção **seletiva de H2S** na presença de CO2;
- **DGA**: indicada em operação a temperaturas mais baixas, por apresentar viscosidade e ponto de congelamento menores;
- **TEA**: foi superada por baixa capacidade e menor reatividade.

#### Variáveis de otimização
As fontes apontam como variáveis relevantes:
- temperatura do solvente;
- concentração da amina;
- taxa de circulação;
- número de estágios/pratos na absorção;
- razão de refluxo do regenerador;
- pequenas mudanças de temperatura da amina;
- uso de misturas de aminas;
- aditivos ativantes, reguladores de pH e antiespumantes.

Em casos de aumento da carga ácida, as fontes mencionam como alternativas de **baixo CAPEX**:
- elevar a concentração da amina;
- usar misturas de aminas;
- ajustar moderadamente a temperatura da amina.

#### Limitações operacionais importantes
- **espuma** reduz o contato gás-líquido e prejudica a absorção;
- aminas podem sofrer **oxidação** na presença de oxigênio, formando amônia e compostos corrosivos, exigindo reposição de solvente;
- há risco de **corrosão**, particularmente em sistemas com MEA/DEA e em contato com CO2;
- produtos de degradação devem ser controlados, inclusive com **filtragem**;
- hidrocarbonetos absorvidos devem ser removidos do circuito, motivo do vaso flash da amina rica.

**Fontes da seção:** `petroles-4ee4bce16acf674505c8912d:pNone:1409829.0-1409874.0`, `petroles-004c2afadba7ea17c7dd7908:pNone:400231.0-400272.0`, `regis-97bdec0bc57184708a525b4a:pNone:1231.0-1401.0`, `regis-b481bf065addf6ea2a64713f:pNone:323.60-345.0`, `regis-b481bf065addf6ea2a64713f:pNone:337.60-359.0`

### 4.2 Seletividade H2S/CO2 e avaliação da necessidade de remoção conjunta ou seletiva
A remoção simultânea de H2S e CO2 é o caso mais comum, mas as fontes ressaltam que o processo pode ser ajustado para priorizar **H2S**. Essa seletividade pode ser desejável por razões operacionais e econômicas, por exemplo:
- quando o gás doce será usado para **queima**, e a restrição de CO2 é menos severa;
- quando a corrente ácida alimenta **unidade de recuperação de enxofre**, já que o CO2 se comporta como inerte e reduz a eficiência desse sistema.

A **MDEA** é citada repetidamente como amina adequada para absorção seletiva de H2S em detrimento do CO2. As fontes também indicam que:
- misturas de aminas podem melhorar o desempenho em alguns casos de **baixa pressão**;
- em **altas pressões**, certas misturas mostraram pouca ou nenhuma vantagem nos casos estudados;
- o aumento da concentração de gás ácido pode levar a um gás doce que atende H2S, mas **não cumpre a especificação de CO2**.

Logo, avaliar a necessidade de remover os dois contaminantes juntos ou de forma seletiva exige observar o uso final da corrente, a razão H2S/CO2 e o risco de o CO2 residual tornar o gás fora de especificação.

**Fontes da seção:** `regis-b481bf065addf6ea2a64713f:pNone:323.60-345.0`, `regis-b481bf065addf6ea2a64713f:pNone:337.60-359.0`, `petroles-4ee4bce16acf674505c8912d:pNone:1409930.0-1409979.0`, `petroles-4ee4bce16acf674505c8912d:pNone:1409829.0-1409874.0`

### 4.3 Absorção física e solventes híbridos
Nos processos de **absorção física**, o gás ácido é dissolvido no solvente sem reação química predominante. As fontes destacam que a capacidade de absorção por volume aumenta com a **pressão operacional**, motivo pelo qual essa rota é preferível quando o gás já chega a **alta pressão** e/ou com **alta contaminação por gases ácidos**.

Vantagens apontadas:
- regeneração com **menor demanda térmica** que a absorção química;
- boa aplicação em correntes com alta carga de CO2/H2S;
- afinidade frequentemente maior por H2S do que por CO2 em muitos solventes orgânicos.

Aspectos de seleção desejáveis para o solvente:
- alta seletividade por gases ácidos;
- baixa solubilidade para outros componentes do gás;
- baixa viscosidade;
- baixa ou moderada higroscopicidade;
- não corrosividade;
- baixa pressão de vapor e custo aceitável.

Limitações destacadas:
- absorção de **hidrocarbonetos**, inclusive pesados;
- eventual necessidade de lavagem/controle de perdas de solvente, conforme o processo.

Exemplos citados:
- **Selexol**, **Purisol** e **Rectisol** como processos físicos industriais;
- **carbonato de propileno (CP)**, citado como atrativo para alto CO2, com regeneração por despressurização, mas menos indicado quando o H2S é elevado;
- **Sulfinol**, como solução combinando solvente físico e químico.

**Fontes da seção:** `regis-97bdec0bc57184708a525b4a:pNone:1231.0-1401.0`, `petroles-004c2afadba7ea17c7dd7908:pNone:400231.0-400272.0`, `petroles-4ee4bce16acf674505c8912d:pNone:424210.0-424256.0`, `petroles-4ee4bce16acf674505c8912d:pNone:424185.0-424231.0`

### 4.4 Leitos sólidos e processos secos
As fontes citam **leitos sólidos** para adoçamento com base em **adsorção** ou reação sobre um sólido. São normalmente associados a gases com **baixa a média concentração de H2S e mercaptanas**. Um exemplo recorrente é o uso de **óxido de ferro** suportado em meio sólido, incluindo referências ao **Iron Sponge** e ao **Sulfatreat**.

Pontos relevantes das fontes:
- são opções para casos específicos, principalmente quando a carga ácida não é alta;
- o processo **Iron Sponge** é descrito como cíclico e não regenerativo na referência citada;
- uma das fontes afirma que a corrente a tratar deveria estar **isenta de CO2** no caso do Iron Sponge, para evitar reações paralelas e perda de eficiência.

**Fontes da seção:** `petroles-4ee4bce16acf674505c8912d:pNone:424185.0-424231.0`, `petroles-4ee4bce16acf674505c8912d:pNone:424210.0-424256.0`

### 4.5 Membranas para redução de CO2
As membranas são apresentadas como tecnologia de separação baseada em **solução-difusão** através de uma barreira semipermeável, usualmente polimérica. A separação depende da **difusão** e da **solubilidade** dos componentes no material da membrana, não apenas do tamanho molecular.

Vantagens destacadas nas fontes, particularmente relevantes para offshore:
- **menor ocupação de espaço**;
- simplicidade operacional;
- menor custo de capital e operação em determinados contextos.

Limitações importantes:
- necessidade de **alta pressão de alimentação**;
- necessidade de **pré-tratamento do gás**;
- **baixa pureza** da corrente de CO2 produzida;
- **perda de hidrocarbonetos no permeado**.

Como orientação geral de seleção, as fontes associam membranas a casos de **alta concentração de CO2 na carga**, enquanto as aminas permanecem fortes candidatas quando a especificação final é muito restritiva.

**Fontes da seção:** `petroles-004c2afadba7ea17c7dd7908:pNone:400231.0-400272.0`

## 5. Como avaliar o desempenho da remoção de H2S e CO2
A avaliação de desempenho deve ir além de verificar se o sistema está “rodando”. Pelas fontes, os principais critérios técnicos são:

### 5.1 Conformidade do gás tratado
O primeiro teste é se o gás de saída cumpre o nível requerido de H2S e CO2 para o destino da corrente. Isso deve ser verificado separadamente, porque uma unidade pode operar de forma satisfatória para H2S e ainda assim falhar na especificação de CO2, especialmente em operações seletivas ou quando a carga ácida aumenta.

### 5.2 Adequação do processo ao regime de pressão parcial
O processo escolhido precisa ser coerente com a pressão parcial dos gases ácidos. Em linhas gerais, as fontes indicam:
- **solventes físicos**: melhor aderência a altas pressões parciais e altas contaminações;
- **aminas**: fortes candidatas para especificações mais severas e baixas concentrações residuais;
- **membranas**: aplicação favorecida em alta carga de CO2 e disponibilidade de pressão;
- **leitos sólidos**: mais compatíveis com baixas/médias cargas em aplicações específicas.

### 5.3 Qualidade do circuito de solvente
Em unidades com amina, desempenho insuficiente pode estar associado a:
- concentração inadequada de amina;
- taxa de circulação insuficiente;
- regeneração deficiente;
- espuma;
- degradação/oxidação do solvente;
- presença de hidrocarbonetos no circuito;
- retorno de produtos de degradação por filtração deficiente.

### 5.4 Seletividade efetiva
Quando a estratégia é remover **preferencialmente H2S**, o desempenho não pode ser avaliado apenas pela queda total de gases ácidos: é preciso verificar se o **CO2 residual** continua aceitável para o destino do gás. Se o objetivo incluir recuperação de enxofre, também importa minimizar a diluição por CO2 da corrente ácida.

### 5.5 Penalidades operacionais e de integridade
Um bom desempenho de remoção não é suficiente se vier acompanhado de:
- corrosão acelerada;
- elevado consumo/reposição de solvente;
- excesso de espuma;
- grande absorção ou perda de hidrocarbonetos;
- aumento de paradas de manutenção.

As fontes citam explicitamente o uso de inibidores de corrosão, antiespumantes e filtração como medidas de suporte ao desempenho sustentado.

### 5.6 No caso de membranas
O desempenho deve ser julgado, no mínimo, por:
- adequação da pressão de alimentação;
- qualidade do pré-tratamento do gás;
- redução efetiva de CO2;
- impacto da perda de hidrocarbonetos no permeado;
- compatibilidade entre a pureza obtida e a especificação requerida do gás tratado.

**Fontes da seção:** `regis-b481bf065addf6ea2a64713f:pNone:337.60-359.0`, `regis-b481bf065addf6ea2a64713f:pNone:323.60-345.0`, `regis-97bdec0bc57184708a525b4a:pNone:1231.0-1401.0`, `petroles-004c2afadba7ea17c7dd7908:pNone:400231.0-400272.0`, `petroles-4ee4bce16acf674505c8912d:pNone:1409829.0-1409874.0`

## 6. Situações típicas de decisão técnica

### 6.1 Quando o H2S domina o problema de segurança/integridade
Se o H2S for o principal limitante por toxicidade, corrosão e especificação, as fontes apontam forte espaço para processos amínicos e, em certos casos, para rotas seletivas de H2S. O destino da corrente ácida também pesa: se houver recuperação de enxofre, a seletividade a H2S ganha valor adicional.

### 6.2 Quando o CO2 é o principal limitante de especificação
Para correntes com muito CO2, as fontes associam maior atratividade a **membranas** e **solventes físicos**, sobretudo se a alimentação já está pressurizada. Ainda assim, se a especificação final do gás for muito severa, as **aminas** permanecem referência.

### 6.3 Quando H2S e CO2 coexistem em proporções relevantes
Nessa condição, a decisão depende fortemente da **razão H2S/CO2**. As fontes destacam que essa razão pode determinar desde a escolha do solvente até o nível de seletividade desejado e a configuração do regenerador.

### 6.4 Quando se busca ajuste operacional sem grande investimento
Para unidades amínicas existentes, as fontes citam como alavancas típicas:
- aumentar a concentração de amina;
- empregar misturas de aminas;
- realizar pequenos ajustes de temperatura;
- controlar espuma e corrosão;
- manter boa filtração e regeneração.

**Fontes da seção:** `petroles-4ee4bce16acf674505c8912d:pNone:1409787.0-1409852.0`, `regis-b481bf065addf6ea2a64713f:pNone:337.60-359.0`, `petroles-004c2afadba7ea17c7dd7908:pNone:400231.0-400272.0`, `petroles-4ee4bce16acf674505c8912d:pNone:1409930.0-1409979.0`

## 7. Implicações para operação e troubleshooting
Sinais de desempenho degradado ou decisão inadequada de processo, à luz das fontes, incluem:
- gás tratado fora da especificação de H2S e/ou CO2;
- corrosão recorrente na unidade de amina;
- espumação e perda de contato gás-líquido;
- necessidade frequente de reposição de solvente por degradação/oxidação;
- aumento de perdas de hidrocarbonetos, inclusive por absorção em solventes físicos ou no permeado de membranas;
- incapacidade de manter a seletividade desejada entre H2S e CO2.

As ações de resposta mais diretamente suportadas nas fontes são:
- revisar se a tecnologia continua coerente com a pressão parcial e a composição atual do gás;
- ajustar concentração, circulação e temperatura do solvente;
- avaliar misturas de aminas quando a condição de pressão/composição justificar;
- controlar espuma, corrosão e degradação do solvente com aditivos e filtração adequados;
- reavaliar o papel de membranas ou solventes físicos em correntes de alto CO2, especialmente quando houver limitação de espaço offshore.

**Fontes da seção:** `regis-b481bf065addf6ea2a64713f:pNone:323.60-345.0`, `regis-b481bf065addf6ea2a64713f:pNone:337.60-359.0`, `regis-97bdec0bc57184708a525b4a:pNone:1231.0-1401.0`, `petroles-004c2afadba7ea17c7dd7908:pNone:400231.0-400272.0`

## 8. Síntese prática
Para avaliar a necessidade e o desempenho da remoção de H2S e CO2 do gás produzido, o profissional deve partir de cinco perguntas centrais:
1. **Quais contaminantes ácidos estão presentes e em que severidade relativa?**
2. **Qual especificação final o gás precisa atender no seu destino real?**
3. **A pressão parcial e a composição favorecem aminas, solventes físicos, membranas ou leito sólido?**
4. **A unidade está entregando o resultado com estabilidade operacional, sem espuma, corrosão excessiva ou perdas de solvente/hidrocarbonetos?**
5. **Há ganho técnico ou econômico em remover H2S seletivamente, deixando parte do CO2, ou isso colocará o gás fora de especificação?**

Essa lógica é consistente com as fontes, mas a resposta final permanece **caso dependente**, especialmente em instalações offshore com restrição de espaço, energia e flexibilidade operacional.

**Fontes da seção:** `petroles-4ee4bce16acf674505c8912d:pNone:1409787.0-1409852.0`, `petroles-4ee4bce16acf674505c8912d:pNone:1409829.0-1409874.0`, `petroles-004c2afadba7ea17c7dd7908:pNone:400231.0-400272.0`, `petroles-4ee4bce16acf674505c8912d:pNone:424185.0-424231.0`