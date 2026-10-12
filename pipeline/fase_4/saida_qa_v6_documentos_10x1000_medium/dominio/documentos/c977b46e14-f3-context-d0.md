# Membranas e corrente rica em CO₂

## 1. Visão de processo e papel das membranas na redução de CO₂ em gás produzido
**Fontes:** `petroles-004c2afadba7ea17c7dd7908:pNone:817733.0-817782.0`, `petroles-004c2afadba7ea17c7dd7908:pNone:817840.0-817893.0`, `petroles-4ee4bce16acf674505c8912d:pNone:2634058.0-2634108.0`

A separação por membranas é um processo de transferência de massa no qual uma barreira semipermeável permite que alguns componentes atravessem a membrana mais rapidamente do que outros. No contexto de tratamento de gás produzido, isso permite reduzir o teor de CO₂ em uma corrente destinada, por exemplo, a especificação de gás combustível, exportação ou a outras etapas de processamento.

Os trechos fornecidos descrevem a tecnologia como já estabelecida industrialmente para separações gasosas, incluindo separação de CO₂ de gás natural, e apontam vantagens operacionais relevantes para unidades offshore: arranjo modular, partida rápida, baixo peso, pequeno volume instalado e custos de manutenção relativamente baixos quando comparados com soluções convencionais de maior porte.

Do ponto de vista funcional:

- a **corrente de alimentação** entra no módulo de membrana sob determinada pressão total;
- o componente mais permeável atravessa preferencialmente a membrana para o lado de **permeado**;
- a corrente remanescente no lado de alimentação deixa o módulo como **retentado**.

Em aplicações de redução de CO₂, o projeto busca explorar a maior taxa de permeação do CO₂ em relação aos hidrocarbonetos leves da corrente, produzindo:

- uma corrente com menor teor de CO₂, normalmente associada ao produto de interesse do sistema; e
- uma **corrente rica em CO₂**, que passa a exigir avaliação própria de pressão, composição e condicionamento subsequente.

O material recebido não traz um fluxograma completo de FPSO para reinjeção, mas permite afirmar que a integração da unidade de membranas com compressão e especificação do gás depende fortemente de como se gera a força motriz de separação: por **compressão a montante** e/ou por **redução de pressão no lado do permeado (vácuo)**.

## 2. Fundamentos de transferência de massa: permeabilidade, permeância e seletividade
**Fontes:** `petroles-004c2afadba7ea17c7dd7908:pNone:817840.0-817893.0`, `petroles-004c2afadba7ea17c7dd7908:pNone:817895.0-817934.0`, `petroles-4ee4bce16acf674505c8912d:pNone:2634058.0-2634108.0`

Os trechos tratam principalmente de membranas poliméricas densas/não porosas, nas quais o mecanismo dominante é o de **sorção–difusão–dessorção**. Nesse modelo:

1. o gás se dissolve na superfície da membrana;
2. difunde-se através do polímero;
3. dessorve no lado oposto.

A relação básica indicada nas fontes é que o fluxo do componente *i* é proporcional:

- à **permeabilidade** do componente na membrana, \(P_i\);
- à **área de membrana** disponível, \(A\);
- à **diferença de pressão parcial** do componente entre alimentação e permeado;
- e inversamente proporcional à **espessura** da camada seletiva, \(\ell\).

De forma simplificada, o projeto usa uma relação do tipo:

\[
J_i \propto \frac{P_i}{\ell}\,(x_i P_f - y_i P_p)
\]

onde:

- \(J_i\) = fluxo do componente *i*;
- \(x_i\) = fração molar de *i* na alimentação;
- \(y_i\) = fração molar de *i* no permeado;
- \(P_f\) = pressão do lado de alimentação;
- \(P_p\) = pressão do lado do permeado.

### 2.1 Permeabilidade e permeância
A **permeabilidade** expressa a facilidade intrínseca com que um gás atravessa o material da membrana. As fontes também lembram que, para membranas comerciais, é frequente trabalhar com **permeância**, que é a permeabilidade dividida pela espessura efetiva da camada seletiva. Em termos práticos:

- maior permeabilidade/permeância tende a reduzir a área necessária para uma dada vazão;
- porém alta permeabilidade sem seletividade suficiente pode gerar produto fora de especificação.

As fontes também associam a permeabilidade ao produto entre **difusividade** e **solubilidade** do gás no polímero. Isso é relevante para CO₂ porque, sendo um gás com alta interação com diversos polímeros, sua permeabilidade pode ser elevada, mas também mais sensível às condições de operação.

### 2.2 Seletividade
A **seletividade** é a capacidade de a membrana favorecer a passagem de um gás em relação a outro. Para um filme homogêneo, as fontes definem a seletividade ideal como a razão entre permeabilidades:

\[
\alpha_{ij} = \frac{P_i}{P_j}
\]

Para membranas comerciais, costuma-se usar a razão entre permeâncias observadas.

Na prática de projeto, a seletividade governa o compromisso entre:

- teor final de CO₂ no produto pobre em CO₂;
- pureza da corrente rica em CO₂;
- recuperação de hidrocarbonetos no retentado;
- número de estágios e reciclos necessários.

### 2.3 Dependência com pressão, temperatura e composição
As fontes destacam limitações importantes do tratamento simplificado:

- para gases permanentes, o modelo com permeabilidade constante é mais aplicável;
- para gases e vapores mais condensáveis, como o CO₂, a permeabilidade pode depender também da **pressão**;
- efeitos de não idealidade e de interação entre componentes podem invalidar o uso direto de dados de gases puros.

Isso tem consequência direta no tratamento de gás produzido: o desempenho real de uma membrana para CO₂/CH₄ ou CO₂/gás combustível não deve ser inferido apenas de catálogos de componente puro quando as pressões, temperaturas e composições reais diferem significativamente das condições de ensaio.

## 3. Variáveis críticas de projeto para redução de CO₂
**Fontes:** `petroles-004c2afadba7ea17c7dd7908:pNone:817733.0-817782.0`, `petroles-004c2afadba7ea17c7dd7908:pNone:817895.0-817934.0`, `petroles-4ee4bce16acf674505c8912d:pNone:2634058.0-2634108.0`

As fontes permitem organizar as principais variáveis de projeto da seguinte forma.

### 3.1 Força motriz: diferença de pressão parcial
A separação é impulsionada pela diferença de pressão parcial de cada componente entre os dois lados da membrana. Essa força motriz pode ser criada de duas maneiras:

- **compressão da alimentação**; ou
- **redução da pressão do permeado**, inclusive por vácuo.

Um trecho informa que, em certos estudos, a alternativa com vácuo em um único estágio foi energeticamente mais vantajosa do que a rota baseada em compressão, apesar de exigir maior área de membrana. Isso não deve ser generalizado sem estudo de caso, mas evidencia a troca clássica entre:

- **energia de compressão/vácuo**;
- **área instalada**;
- **pressão disponível na corrente rica em CO₂**.

### 3.2 Área de membrana e energia
Segundo as fontes, a área requerida e a energia de compressão dependem de:

- permeabilidade do material;
- seletividade para o par de componentes-chave;
- pressão parcial a montante e a jusante;
- queda de pressão no módulo;
- vazão de alimentação;
- vida útil e estabilidade do desempenho.

Em termos de decisão de engenharia, isso significa que um material muito seletivo, mas de baixa permeabilidade, pode exigir área excessiva; já um material muito permeável, mas pouco seletivo, pode falhar em entregar especificação.

### 3.3 Efeito da espessura e da estrutura da membrana
As fontes reforçam que a razão \(P_i/\ell\) é determinante. Membranas com camada seletiva mais fina tendem a fornecer maior fluxo, desde que a integridade mecânica e a ausência de defeitos sejam mantidas.

Por isso, membranas **assimétricas** e **compostas** são destacadas como relevantes industrialmente: combinam uma camada seletiva muito fina com um suporte poroso de resistência mecânica. Em gases, isso é especialmente importante porque pequenas imperfeições podem prejudicar fortemente a seletividade.

## 4. Módulos e arranjos de escoamento
**Fontes:** `petroles-004c2afadba7ea17c7dd7908:pNone:817733.0-817782.0`, `petroles-004c2afadba7ea17c7dd7908:pNone:817895.0-817934.0`, `petroles-4ee4bce16acf674505c8912d:pNone:2634058.0-2634108.0`, `petroles-4ee4bce16acf674505c8912d:pNone:2634085.0-2634138.0`

### 4.1 Tipos de módulo
Os trechos citam quatro configurações usuais de módulos:

- tubular;
- quadro e placas;
- espiral;
- fibras ocas.

Para aplicação em captura/separação de CO₂, os módulos **espiral** e **fibras ocas** são apontados como vantajosos por:

- menor custo de fabricação;
- menor área requerida para instalação;
- maior compactação da área de transferência.

Entretanto, as fontes também alertam que essas configurações são **mais suscetíveis à incrustação/fouling**. Em ambiente de FPSO, esse ponto é particularmente relevante porque arraste de líquidos, hidrocarbonetos pesados, partículas e contaminantes podem acelerar perda de desempenho.

### 4.2 Padrão de escoamento
Os trechos comparam arranjos de mistura completa, concorrente, contra-corrente e cross-flow. A indicação fornecida é que o **escoamento em contra-corrente** tende a ser o mais eficiente, por exigir menor área de membrana e proporcionar maior grau de separação.

Isso é importante para a etapa de concepção, porque a escolha do arranjo não afeta apenas a hidráulica do módulo, mas a própria economia global da unidade.

## 5. Pré-tratamento do gás de alimentação
**Fontes:** `petroles-4ee4bce16acf674505c8912d:pNone:2634058.0-2634108.0`, `petroles-4ee4bce16acf674505c8912d:pNone:2634085.0-2634138.0`, `petroles-004c2afadba7ea17c7dd7908:pNone:817895.0-817934.0`

O pré-tratamento é um ponto crítico para confiabilidade e desempenho. As fontes são explícitas em afirmar que a necessidade de pré-tratamento depende:

- das características do gás;
- do material da membrana.

### 5.1 Remoção de água
Um ponto particularmente importante é a **desidratação**. O material informa que membranas comerciais de **acetato de celulose**, por exemplo, exigem redução do teor de água do gás porque esse material não tolera água em excesso e é hidrofílico.

Como implicação prática:

- o teor de água na alimentação deve ser compatível com o limite de tolerância da membrana;
- a desidratação a montante não é apenas um requisito de qualidade do gás, mas também de **proteção do elemento separador**;
- em aplicações para corrente rica em CO₂ destinada a compressão posterior, a água residual também se torna um fator de risco para corrosão e condensação.

Os trechos citam como alternativas de desidratação, em outros contextos de processo, absorção com glicóis e peneira molecular; entre os glicóis mencionados, o **TEG** é apontado como opção indicada em separações desse tipo.

### 5.2 Remoção de enxofre/compostos sulfurados
As fontes observam que, dependendo do material da membrana, pode ser necessário **remover enxofre** antes dos módulos. Para a engenharia de tratamento de gás, isso significa que a avaliação da compatibilidade química da membrana com H₂S e outros contaminantes não pode ser separada da definição do esquema de processo.

### 5.3 Consequências de pré-tratamento insuficiente
Se o gás chegar aos módulos com água e contaminantes acima do tolerável, pode ocorrer:

- degradação ou perda de seletividade da membrana;
- maior tendência a incrustação/fouling;
- instabilidade de desempenho ao longo do tempo;
- aumento da complexidade de operação do sistema de compressão associado à corrente rica em CO₂.

## 6. Limitações do uso de dados de componente puro e necessidade de ensaios com mistura real
**Fontes:** `petroles-004c2afadba7ea17c7dd7908:pNone:817840.0-817893.0`, `petroles-004c2afadba7ea17c7dd7908:pNone:817895.0-817934.0`

Os trechos trazem uma advertência central para projeto confiável: **não se deve presumir automaticamente que a permeabilidade de cada componente em mistura seja igual à do componente puro**.

As razões citadas incluem:

- não idealidade;
- acoplamento/interferência entre fluxos dos componentes;
- desvio da lei de Henry quando a solubilidade é elevada;
- efeito da pressão absoluta sobre permeabilidade;
- alteração do material por inchamento/plasticização.

Por isso, as fontes recomendam expressamente a obtenção de **dados experimentais com a mistura gasosa real**, nas condições de pressão e temperatura do processo.

### 6.1 Método pseudo-binário
Um trecho informa que, para misturas multicomponente, é comum tratar o problema como um sistema pseudo-binário e calcular pseudo-permeabilidades médias. Contudo, a própria fonte alerta que a área de membrana obtida por esse método é **menor** do que a resultante da solução exata, logo o método **não é conservativo**.

Aplicação prática:

- o pseudo-binário pode servir para triagem inicial;
- não deve ser a única base para dimensionamento final de área, módulos e utilidades;
- em gás produzido com CO₂, CH₄, hidrocarbonetos mais pesados, água e traços ácidos, a validação experimental torna-se ainda mais importante.

## 7. Fenômenos que degradam a separação de CO₂
**Fontes:** `petroles-004c2afadba7ea17c7dd7908:pNone:817895.0-817934.0`, `petroles-4ee4bce16acf674505c8912d:pNone:690105.0-690141.0`

### 7.1 Inchamento e plasticização por CO₂
As fontes registram que o CO₂ pode **inchar determinadas membranas**. Em outro trecho, embora em contexto de CO₂ supercrítico, é descrito o fenômeno de **plasticização**, no qual a estrutura polimérica se expande e passa a permitir a passagem menos seletiva de outros componentes.

Para a operação de uma unidade de membranas para remoção de CO₂, o efeito prático é claro:

- a seletividade pode cair em determinadas faixas de pressão/composição;
- o desempenho obtido em ensaio simplificado pode não se repetir no campo;
- o ganho aparente de fluxo pode vir acompanhado de pior qualidade de separação.

### 7.2 Fouling, colmatação e polarização
As fontes também mencionam fenômenos de deposição/acúmulo sobre a membrana, como fouling, colmatação e polarização de concentração, que podem reduzir o fluxo com o tempo de operação.

Embora parte dos exemplos venha de outros serviços com membranas, o ensinamento para FPSO é pertinente: qualquer arraste de líquido, sólidos finos, condensáveis ou material pesado aumenta o risco de perda gradual de capacidade e piora do desempenho seletivo.

### 7.3 Queda de desempenho: sintomas observáveis
A partir das fontes, uma degradação de desempenho pode se manifestar como:

- aumento da área efetiva requerida para manter produção;
- queda do fluxo permeado;
- piora da especificação do produto pobre em CO₂;
- maior perda de hidrocarbonetos para a corrente rica em CO₂;
- maior sensibilidade a flutuações de pressão e composição.

## 8. Estagiamento, pureza, recuperação e reciclo
**Fontes:** `petroles-4ee4bce16acf674505c8912d:pNone:2634058.0-2634108.0`

Os trechos indicam que uma única etapa de membrana pode ser insuficiente para combinar simultaneamente:

- alta captura/remoção de CO₂; e
- alta pureza da corrente de CO₂.

No material fornecido, isso aparece em estudos de captura de CO₂ em que um único estágio com membrana de acetato de celulose não alcança simultaneamente metas elevadas de recuperação e pureza quando a alimentação tem baixa concentração de CO₂. O texto acrescenta que purezas mais altas podem exigir:

- **segundo estágio**;
- ou configurações com **reciclo**.

Mesmo sendo um contexto de captura diferente do gás produzido em FPSO, o princípio é diretamente útil: quando se busca especificação rigorosa do gás tratado e ao mesmo tempo geração de uma corrente rica em CO₂ com qualidade adequada para uso posterior, o engenheiro deve avaliar se um único estágio atende ou se há necessidade de múltiplos estágios.

## 9. Corrente rica em CO₂: implicações para condicionamento
**Fontes:** `petroles-4ee4bce16acf674505c8912d:pNone:2634058.0-2634108.0`, `petroles-4ee4bce16acf674505c8912d:pNone:2634085.0-2634138.0`, `petroles-004c2afadba7ea17c7dd7908:pNone:817733.0-817782.0`, `petroles-004c2afadba7ea17c7dd7908:pNone:817895.0-817934.0`

O material disponível não fornece critérios completos de reinjeção, mas permite estabelecer implicações de engenharia para a corrente rica em CO₂ gerada na unidade de membranas.

### 9.1 Nível de pressão da corrente rica em CO₂
Como a força motriz da membrana é baseada em diferença de pressão parcial, a pressão da corrente rica em CO₂ dependerá do arranjo adotado:

- se o sistema usar **compressão da alimentação**, a corrente do lado de permeado tenderá a estar a pressão menor que a alimentação;
- se o sistema usar **vácuo no permeado**, a corrente rica em CO₂ poderá sair em pressão ainda mais baixa.

Consequência operacional: a escolha que minimiza energia da etapa de separação não necessariamente minimiza a energia do **condicionamento subsequente** da corrente rica em CO₂. Se essa corrente precisar seguir para compressão adicional, o balanço global de energia do sistema deve considerar:

- energia da separação;
- pressão de saída da corrente rica em CO₂;
- necessidade de recompressão posterior.

### 9.2 Qualidade química da corrente rica em CO₂
Como o pré-tratamento depende do material da membrana e das características do gás, a qualidade da corrente rica em CO₂ será afetada por aquilo que entra no módulo. Em especial:

- se a desidratação for insuficiente, a corrente rica em CO₂ poderá carregar água em nível indesejado para etapas subsequentes;
- se não houver remoção adequada de enxofre quando requerida, contaminantes sulfurados podem permanecer associados à corrente rica em CO₂.

Para qualquer rota posterior de compressão e manuseio dessa corrente, isso afeta diretamente a robustez operacional do arranjo.

### 9.3 Perdas de hidrocarbonetos
Os trechos não trazem números de recuperação para CO₂/CH₄ em FPSO, mas deixam claro que pureza e recuperação são parâmetros centrais do processo. Logo, a avaliação da corrente rica em CO₂ não pode focar apenas no teor de CO₂: deve também considerar a **quantidade de hidrocarbonetos que permeiam junto** com o CO₂, pois isso impacta eficiência econômica e integração com as demais correntes de gás da unidade.

## 10. Diretrizes práticas de projeto, operação e solução de problemas
**Fontes:** `petroles-004c2afadba7ea17c7dd7908:pNone:817733.0-817782.0`, `petroles-004c2afadba7ea17c7dd7908:pNone:817840.0-817893.0`, `petroles-004c2afadba7ea17c7dd7908:pNone:817895.0-817934.0`, `petroles-4ee4bce16acf674505c8912d:pNone:2634058.0-2634108.0`, `petroles-4ee4bce16acf674505c8912d:pNone:2634085.0-2634138.0`, `petroles-4ee4bce16acf674505c8912d:pNone:690105.0-690141.0`

### 10.1 Na fase de projeto
É tecnicamente consistente verificar, no mínimo:

- seletividade do material para CO₂ frente aos componentes que se deseja reter;
- permeância efetiva e área total requerida;
- faixa real de pressão, temperatura e composição da alimentação;
- sensibilidade da membrana à água, enxofre e CO₂;
- tipo de módulo mais adequado ao espaço disponível e ao risco de incrustação;
- necessidade de estágio único, múltiplos estágios e/ou reciclo;
- balanço energético entre compressão da alimentação e vácuo do permeado;
- perda de hidrocarbonetos para a corrente rica em CO₂.

### 10.2 No comissionamento
Com base nas limitações apontadas pelas fontes, o comissionamento deve confirmar em campo:

- compatibilidade do pré-tratamento com a membrana instalada;
- desempenho com gás real, e não apenas com dados de catálogo;
- efeito da composição e da pressão sobre fluxo e especificação;
- integridade do arranjo hidráulico para evitar queda de desempenho por má distribuição ou contaminação inicial.

### 10.3 Na operação
Indicadores úteis de acompanhamento incluem:

- teor de CO₂ no produto pobre em CO₂;
- composição da corrente rica em CO₂;
- pressão da alimentação e do permeado;
- queda de pressão no módulo;
- tendência de fluxo/permeância ao longo do tempo;
- sinais indiretos de incrustação, plasticização ou degradação do material.

### 10.4 Na solução de problemas
Algumas relações causa–efeito suportadas pelo material são:

- **queda de seletividade**: pode estar associada a inchamento/plasticização por CO₂, contaminação da membrana ou uso de dados de projeto não representativos da mistura real;
- **queda de fluxo**: pode indicar fouling, colmatação, polarização de concentração ou aumento de resistência efetiva na camada seletiva;
- **produto fora de especificação**: pode decorrer de força motriz insuficiente, arranjo de estágio inadequado, perda de integridade da membrana ou mudança de composição da alimentação;
- **corrente rica em CO₂ inadequada para a etapa seguinte**: pode resultar de pressão de saída muito baixa, água residual excessiva, ou separação insuficiente em único estágio.

## 11. Síntese executiva
**Fontes:** `petroles-004c2afadba7ea17c7dd7908:pNone:817733.0-817782.0`, `petroles-004c2afadba7ea17c7dd7908:pNone:817840.0-817893.0`, `petroles-004c2afadba7ea17c7dd7908:pNone:817895.0-817934.0`, `petroles-4ee4bce16acf674505c8912d:pNone:2634058.0-2634108.0`, `petroles-4ee4bce16acf674505c8912d:pNone:2634085.0-2634138.0`, `petroles-4ee4bce16acf674505c8912d:pNone:690105.0-690141.0`

Com base exclusivamente nos trechos fornecidos, a avaliação de membranas para redução de CO₂ em gás produzido deve se apoiar em cinco princípios:

1. **A separação depende da diferença de pressão parcial**, da permeância da membrana e da seletividade para os componentes-chave.
2. **Dados de gases puros e aproximações pseudo-binárias não bastam** para projeto final confiável; a mistura real e as condições reais precisam ser testadas.
3. **Pré-tratamento é parte inseparável da solução**, principalmente quanto à remoção de água e, conforme o material, de compostos sulfurados.
4. **Módulos compactos, como fibras ocas e espirais, favorecem aplicação offshore**, mas exigem atenção maior a incrustação e perda de desempenho.
5. **A corrente rica em CO₂ não é um subproduto trivial**: sua pressão, pureza e contaminantes residuais são diretamente afetados pela escolha do arranjo de separação e condicionam as etapas subsequentes de compressão e uso.