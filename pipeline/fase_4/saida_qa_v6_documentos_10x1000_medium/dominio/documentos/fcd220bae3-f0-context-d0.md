# Dimensionamento da ancoragem de FPSOs

## 1. Finalidade do sistema de ancoragem e critério básico de desempenho
O sistema de ancoragem de uma unidade flutuante tem a função de restringir os deslocamentos produzidos por vento, ondas e correntes, mantendo a unidade dentro de uma região na qual as operações possam ocorrer com segurança. Para FPSOs, isso significa manter a embarcação dentro de um círculo ou envelope de tolerância compatível com os equipamentos conectados, a operação e a lâmina d’água.

Um conceito central de dimensionamento é o **passeio** ou **excursão** da unidade. As fontes o definem como a distância horizontal entre a posição de equilíbrio neutro e a posição de equilíbrio sob carregamento ambiental, usualmente expressa como percentual da lâmina d’água. Em termos de projeto, a eficiência do sistema pode ser entendida pela capacidade de limitar esse passeio sem introduzir trações excessivas nas linhas ou reduzir a vida em fadiga do conjunto.

Há um compromisso estrutural importante:
- **maior rigidez do sistema** tende a reduzir o passeio;
- porém, **maior rigidez também tende a elevar as trações nas linhas** e, portanto, as tensões internas e a severidade de fadiga.

Assim, o dimensionamento não é apenas uma busca por menor offset, mas por um equilíbrio entre:
1. atendimento ao envelope de posicionamento;
2. cargas admissíveis nas linhas e fundações;
3. integridade estrutural e vida em fadiga ao longo da operação.

**Fontes:** `regis-f1d1b05bf91e1c627336a9fa:pNone:1658.0-1854.0`

## 2. Configurações de amarração aplicáveis a FPSOs: spread mooring versus ponto único/turret
Para FPSOs, as fontes indicam três arranjos principais de amarração:
- **single point mooring**;
- **spread mooring**;
- **turret**, tratado pelas fontes como uma forma de amarração em ponto único.

A distinção funcional mais relevante para seleção preliminar é o efeito sobre o **aproamento** e sobre a interação com os carregamentos ambientais:
- na **amarração em ponto único**, a principal vantagem indicada é permitir o alinhamento da embarcação com corrente, vento e onda, reduzindo os esforços ambientais no casco;
- no **spread mooring**, as linhas ficam distribuídas em torno da embarcação, restringindo não apenas movimentos horizontais no plano, mas também a variação de aproamento. Isso implica menor liberdade para weathervaning e maior dependência da direção de incidência ambiental no dimensionamento do sistema.

Para o FPSO, essa distinção afeta diretamente o dimensionamento porque muda:
- a distribuição de cargas entre linhas;
- o comportamento direcional do casco;
- a sensibilidade do sistema a combinações de vento, onda e corrente;
- os requisitos de raio de ancoragem e ocupação do leito marinho.

As fontes disponíveis, entretanto, trazem **mais detalhe para linhas e fundações do que para o dimensionamento interno de turrets**. Portanto, nesta faceta, o conteúdo mais robusto é o de seleção entre amarração distribuída e arranjos de ponto único sob o ponto de vista de comportamento global.

**Fontes:** `regis-c236bcf592c1c0696dbf71c2:pNone:335.60-403.0`, `regis-c236bcf592c1c0696dbf71c2:pNone:453.0-488.0`

## 3. Critérios principais de seleção da configuração geométrica das linhas
As fontes convergem em que a escolha da configuração de ancoragem depende principalmente de:
- tipo de embarcação;
- tipo de operação;
- quantidade de risers;
- profundidade d’água;
- intensidade dos carregamentos ambientais;
- custo dos materiais e da instalação.

As geometrias mais citadas são:
1. **catenária convencional**;
2. **taut-leg** ou linha retesada/perna esticada;
3. **tendões verticais** (mais associados a TLPs, boias e monobóias do que a FPSOs convencionais).

Para FPSOs, o processo de seleção normalmente parte das consequências destas variáveis:
- **águas mais rasas** favorecem soluções mais pesadas e simples, inclusive linhas com maior fração de corrente;
- **águas profundas e ultraprofundas** tendem a exigir linhas combinadas para reduzir peso suspenso e preservar capacidade restauradora;
- **maior congestionamento submarino** penaliza arranjos com grande raio de ancoragem;
- **maior exigência de controle de offset** favorece configurações mais rígidas, desde que compatíveis com fadiga, carga em fundações e dinâmica da unidade.

As fontes também deixam claro que cada geometria de linha demanda um tipo apropriado de fundação. Portanto, a seleção da configuração das linhas e a seleção do elemento de ancoragem no solo devem ser tratadas de forma integrada.

**Fontes:** `regis-f1d1b05bf91e1c627336a9fa:pNone:1658.0-1854.0`, `petroles-4ee4bce16acf674505c8912d:pNone:62969.0-63000.0`, `regis-c236bcf592c1c0696dbf71c2:pNone:453.0-488.0`

## 4. Configuração em catenária: implicações de dimensionamento
Na ancoragem em catenária, a linha assume a forma de uma curva governada pelo seu peso próprio e pela flexibilidade do material. Uma característica essencial desse arranjo é a existência de **trecho apoiado no leito marinho**, o que traz duas consequências centrais:

### 4.1 Mecanismo resistente
- parte da força restauradora decorre do próprio comportamento geométrico da linha;
- o trecho em contato com o fundo contribui por **atrito no leito marinho**;
- em configuração convencional, a fundação tende a receber predominantemente **esforços horizontais**, permitindo o uso de âncoras/fundações menos exigidas em carga vertical.

### 4.2 Consequências para seleção e layout
- a catenária convencional permite **maiores deslocamentos** da unidade;
- para atender critérios de passeio, exige **raio de ancoragem elevado**;
- as fontes indicam ordem de grandeza de **aproximadamente 2 a 3 vezes a lâmina d’água**, e em outro trecho “cerca de 3 vezes” a lâmina d’água;
- esse grande raio aumenta o comprimento de linha, o custo e o potencial de **interferência com linhas de unidades vizinhas, dutos e equipamentos submarinos**.

### 4.3 Aplicabilidade
As fontes citam a catenária como solução aplicável a **plataformas semissubmersíveis e navios FPSO**. Em termos de projeto, ela tende a ser atrativa quando o campo tolera maior ocupação no fundo e quando a redução de carga vertical nas fundações é prioritária.

**Síntese de dimensionamento:** a catenária favorece fundações solicitadas principalmente em carga horizontal e se beneficia do contato com o solo, mas penaliza o layout submarino e o controle de passeio.

**Fontes:** `regis-f1d1b05bf91e1c627336a9fa:pNone:1658.0-1854.0`, `petroles-4ee4bce16acf674505c8912d:pNone:62969.0-63000.0`, `regis-c236bcf592c1c0696dbf71c2:pNone:453.0-488.0`

## 5. Configuração taut-leg: implicações de dimensionamento
Na configuração **taut-leg**, as linhas trabalham inclinadas e tracionadas, sem o mesmo trecho apoiado no leito típico da catenária convencional.

### 5.1 Efeito estrutural e operacional
As fontes associam a taut-leg a:
- **maior rigidez do sistema**;
- **menor comprimento total de linha**;
- **menor raio de ancoragem**;
- **melhor controle do passeio/offset**.

Uma das fontes informa que a projeção horizontal pode ser da mesma ordem da lâmina d’água, enquanto outra afirma explicitamente que o raio de abrangência pode ser aproximadamente igual à profundidade d’água. Em ambos os casos, a mensagem técnica é consistente: **o arranjo ocupa menos área no fundo do que a catenária**.

### 5.2 Consequência para fundações
Como a linha transmite componentes **horizontais e verticais**, as fundações devem resistir a cargas de arrancamento e a combinações mais severas de esforço axial. Por isso, as fontes relacionam a taut-leg a elementos como:
- **estacas de sucção**;
- **VLA (Vertical Load Anchor)**;
- **estacas torpedo**.

### 5.3 Materiais típicos
As fontes indicam que, assim como na convencional, a linha taut-leg costuma ter:
- **amarras ou cabos de aço nas extremidades**;
- **cabo de poliéster no trecho intermediário**.

Essa arquitetura decorre do fato de que o poliéster oferece baixo peso submerso e elevada elasticidade, propriedades úteis para absorção de movimentos dinâmicos da unidade e redução do peso suspenso em águas profundas.

### 5.4 Limitações implícitas
A maior rigidez e a presença de carga vertical nas fundações melhoram o controle de posição, mas tornam o sistema mais dependente de:
- fundações com capacidade compatível;
- controle adequado de pré-tração;
- avaliação de fadiga e de tensões máximas nas linhas.

**Síntese de dimensionamento:** a taut-leg é favorecida quando se busca reduzir excursão e raio de ancoragem, sobretudo em águas profundas, desde que o solo e as fundações suportem as componentes verticais e o projeto trate corretamente a fadiga e a pré-tração.

**Fontes:** `regis-f1d1b05bf91e1c627336a9fa:pNone:1658.0-1854.0`, `petroles-4ee4bce16acf674505c8912d:pNone:62969.0-63000.0`, `petroles-4ee4bce16acf674505c8912d:pNone:46686.0-46726.0`, `regis-c236bcf592c1c0696dbf71c2:pNone:453.0-488.0`

## 6. Materiais das linhas de ancoragem e critérios de composição
As fontes descrevem linhas **homogêneas** ou, mais tipicamente em águas profundas/ultraprofundas, **heterogêneas**, combinando materiais diferentes para equilibrar resistência, peso, abrasão e rigidez.

### 6.1 Amarras de aço
Características destacadas:
- elevada resistência à abrasão;
- boa vida útil em ambiente severo;
- robustez para manuseio e contato com o fundo e com equipamentos da unidade;
- maior peso linear.

Consequências de projeto:
- linhas compostas apenas por amarras tendem a se tornar inviáveis em águas profundas devido ao peso suspenso excessivo;
- por isso, as amarras são preferencialmente colocadas **junto ao fundo** e **junto à embarcação**, onde sua resistência ao desgaste é mais valiosa;
- essa escolha também ajuda a reduzir problemas de abrasão e, conforme uma das fontes, pode contribuir para evitar ou reduzir carga vertical indesejada na âncora, dependendo da geometria da linha.

As fontes citam ainda classificação por grau do aço, mencionando o grau **R4** como de alta resistência, mas sem fornecer aqui critérios normativos completos de seleção.

### 6.2 Cabos de aço
Características destacadas:
- menor peso que as amarras;
- elevada rigidez axial e boa flexibilidade global;
- maior elasticidade que amarras para mesma carga de ruptura, segundo uma das fontes;
- maior vulnerabilidade à corrosão e, portanto, potencial vida útil inferior à de amarras em certas aplicações.

Foram citados dois tipos principais:
- **six strand**, mais comum em unidades de perfuração por facilidade de manuseio;
- **spiral strand**, com maior durabilidade e melhor resistência à fadiga, porém com custo maior.

### 6.3 Cabos sintéticos, especialmente poliéster
O poliéster é apontado como material particularmente favorável em águas profundas e ultraprofundas por apresentar:
- **baixo peso submerso**;
- **alta elasticidade axial**;
- capacidade de reduzir peso suspenso e melhorar o comportamento de linhas taut-leg.

As fontes também observam que cabos de poliéster têm baixa ou nula rigidez à compressão axial, devendo trabalhar tracionados. Isso é coerente com seu uso em linhas pré-tensionadas.

### 6.4 Linhas combinadas
A solução típica descrita é:
- amarras nas extremidades;
- cabo de aço ou poliéster no trecho central.

O racional é maximizar desempenho:
- resistência ao desgaste nos pontos críticos de contato e manuseio;
- redução do peso submerso total;
- preservação da força restauradora;
- possibilidade de menor pré-tensão para mesma restauração, quando o trecho central reduz a carga vertical total da linha.

### 6.5 Conectores e descontinuidades
Os conectores unem os principais componentes da linha. Uma das fontes ressalta que elementos acessórios em pontos de descontinuidade podem ter a mesma carga de ruptura das amarras, mas serem **mais suscetíveis à fadiga**. Em dimensionamento e detalhamento, isso significa que conectores não devem ser tratados apenas por resistência estática; eles podem governar a integridade do sistema em serviço cíclico.

**Fontes:** `petroles-4ee4bce16acf674505c8912d:pNone:46686.0-46726.0`, `petroles-4ee4bce16acf674505c8912d:pNone:62986.0-63020.0`, `regis-c236bcf592c1c0696dbf71c2:pNone:453.0-488.0`

## 7. Fundações e elementos de ancoragem: compatibilização com a geometria da linha
O sistema de ancoragem transmite esforços ao solo marinho por meio de âncoras ou estacas. As fontes ressaltam que a fundação deve ser projetada para suportar **cargas estáticas, cíclicas e transitórias**, sem deformações excessivas nem resposta estrutural inadequada da unidade.

### 7.1 Compatibilidade linha-fundação
A escolha da fundação depende do tipo de carregamento que chega ao ponto de ancoragem:
- **catenária convencional:** predominância de carga horizontal na fundação;
- **taut-leg:** presença relevante de componentes horizontal e vertical;
- **tendões verticais:** carregamento predominantemente trativo vertical.

### 7.2 Tipos citados nas fontes
As fontes mencionam como soluções usuais:
- **estacas de sucção**: resistem a cargas horizontais e verticais;
- **VLA**: descritas como âncoras voltadas a carregamentos com componente vertical relevante;
- **SEPLA**: placa associada à estaca de sucção para efeito de cravação, conforme a redação da fonte;
- **estacas torpedo**: solução desenvolvida e usada no Brasil, especialmente em solos coesivos, citada como de baixo custo relativo, instalação simples e possibilidade de uso de meios navais de menor custo.

### 7.3 Implicações de dimensionamento
Do ponto de vista de seleção preliminar, o engenheiro deve verificar simultaneamente:
1. a geometria da linha e a direção das cargas no ponto de ancoragem;
2. a capacidade do solo;
3. a sensibilidade da fundação a cargas cíclicas e transitórias;
4. o método de instalação disponível e o custo logístico.

A compatibilidade entre o arranjo de linha e o tipo de fundação é uma condição de viabilidade do conceito, não apenas um detalhamento posterior.

**Fontes:** `petroles-4ee4bce16acf674505c8912d:pNone:62986.0-63020.0`, `petroles-4ee4bce16acf674505c8912d:pNone:62969.0-63000.0`, `regis-f1d1b05bf91e1c627336a9fa:pNone:1658.0-1854.0`

## 8. Pré-tração, instalação e comissionamento
A **pré-tração** é explicitamente apontada nas fontes como um dos principais parâmetros de projeto do sistema de ancoragem. Ela é definida como a **tensão total nas linhas quando o sistema está em equilíbrio na posição neutra, sem ação ambiental**.

### 8.1 Papel da pré-tração no dimensionamento
As fontes afirmam que o efeito das cargas dinâmicas nas linhas é fortemente afetado pela força de pré-tração. Em termos práticos, isso significa que a pré-tração influencia:
- a rigidez aparente do sistema;
- o offset médio e o passeio sob ações ambientais;
- a distribuição de cargas entre linhas;
- a resposta dinâmica e a fadiga.

### 8.2 Implicações de instalação/comissionamento
Uma das fontes informa que, após a penetração da âncora no solo, aplica-se uma carga de pré-tração com alinhamento do navio e com a inclinação desejada da linha. Uma vez atingida a tensão requerida, ela deve ser mantida por um período determinado por autoridades de certificação. Os valores específicos não puderam ser reproduzidos porque aparecem mascarados nas fontes, mas o princípio de comissionamento é claro:
- instalação da fundação;
- conexão/alinhamento da linha;
- aplicação da pré-tração de projeto;
- permanência da carga por tempo especificado para validação do assentamento/condição da ancoragem.

### 8.3 Cuidado de projeto
Como a pré-tração afeta o carregamento dinâmico, sua definição não deve ser tratada apenas como requisito de instalação. Ela precisa ser coerente com:
- a rigidez pretendida do sistema;
- a excursão admissível da unidade;
- a capacidade de linha e fundação;
- a vida em fadiga.

**Fontes:** `petroles-4ee4bce16acf674505c8912d:pNone:62986.0-63020.0`

## 9. Carregamentos ambientais considerados no dimensionamento
As fontes listam como ações ambientais principais:
- **ondas**;
- **vento**;
- **corrente**;
- e, em termos gerais, cargas transitórias e de impacto em algumas situações operacionais.

A distribuição simplificada das ações é descrita assim:
- ondas e correntes atuam no casco e nas linhas de ancoragem;
- o vento atua nas áreas emersas da unidade.

Esses carregamentos produzem deslocamentos da plataforma e se convertem em solicitações no sistema de ancoragem. As fontes distinguem ainda:
- **cargas quase-estáticas**, associadas às componentes médias de vento, onda e corrente;
- **cargas dinâmicas totais**, que superpõem os efeitos variáveis ao longo do tempo.

Para dimensionamento preliminar, isso reforça que o sistema de ancoragem não deve ser avaliado apenas por tração estática máxima. É necessário considerar:
- resposta média de offset;
- variação dinâmica das trações;
- efeito cíclico nas linhas e fundações;
- integridade sob combinação de ações.

**Fontes:** `petroles-4ee4bce16acf674505c8912d:pNone:62986.0-63020.0`

## 10. Implicações específicas para FPSOs em projeto conceitual
Com base nas fontes, um roteiro coerente de seleção e dimensionamento conceitual para FPSOs pode ser resumido assim:

### 10.1 Escolha do arranjo global de amarração
- Se a prioridade é permitir alinhamento da embarcação com o ambiente e reduzir cargas no casco, as fontes associam essa vantagem aos sistemas de **ponto único**, incluindo o **turret**.
- Se a unidade aceitar restrição maior de aproamento e o objetivo for distribuir linhas ao redor do casco, aplica-se o **spread mooring**.

### 10.2 Escolha da geometria das linhas
- **Catenária** quando maior excursão e maior raio de ancoragem forem aceitáveis e quando se desejar reduzir exigência de carga vertical na fundação.
- **Taut-leg** quando houver necessidade de reduzir offset e ocupação no fundo, especialmente em lâminas d’água maiores, desde que as fundações suportem componentes verticais e o sistema trate adequadamente a fadiga.

### 10.3 Escolha dos materiais
- **Mais corrente em águas rasas** e em trechos sujeitos a abrasão/manuseio.
- **Linhas combinadas em águas profundas**, com corrente nas extremidades e aço ou poliéster no trecho central.
- **Poliéster** particularmente atrativo em águas profundas/ultraprofundas, pelo baixo peso submerso e maior elasticidade.

### 10.4 Escolha das fundações
- Compatibilizar direção e magnitude das cargas da linha com a fundação.
- Para **taut-leg**, priorizar elementos aptos a receber componente vertical relevante, como as soluções citadas nas fontes.
- Considerar capacidade do solo e efeitos de carregamento cíclico e transitório.

### 10.5 Definição da pré-tração
- Tratar a pré-tração como variável de projeto e de comissionamento.
- Verificar seu efeito no offset, na carga dinâmica e na fadiga.

**Fontes:** `regis-c236bcf592c1c0696dbf71c2:pNone:335.60-403.0`, `regis-c236bcf592c1c0696dbf71c2:pNone:453.0-488.0`, `regis-f1d1b05bf91e1c627336a9fa:pNone:1658.0-1854.0`, `petroles-4ee4bce16acf674505c8912d:pNone:62969.0-63000.0`, `petroles-4ee4bce16acf674505c8912d:pNone:62986.0-63020.0`, `petroles-4ee4bce16acf674505c8912d:pNone:46686.0-46726.0`

## 11. Limites do material para esta faceta
As fontes permitem estruturar bem os critérios de seleção entre catenária, taut-leg e arranjos globais spread versus ponto único/turret, bem como a seleção preliminar de materiais e fundações. Porém, o material fornecido não traz detalhamento suficiente para consolidar, nesta faceta, critérios quantitativos completos de:
- estados-limite último, acidental e de fadiga;
- análise acoplada casco-risers-ancoragem;
- distribuição de cargas por setor e por linha em intacto e avariado com valores confiáveis;
- componentes como fairleads, chain stoppers e conectores especiais além de observações gerais;
- critérios normativos formais de classe, certificação ou autoridade marítima.

Portanto, este documento é adequado como base conceitual e de decisão preliminar, mas não substitui especificações de projeto detalhado, regras de classe e documentos contratuais da instalação considerada.