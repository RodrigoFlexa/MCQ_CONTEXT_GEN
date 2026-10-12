# Envelopes e critérios metocean para offloading em FPSOs

## 1. Conceito e finalidade do envelope operacional

Nesta faceta, o envelope operacional é a combinação admissível de:
- distância entre FPSO e navio aliviador;
- setor angular de operação em torno da estação de alívio;
- aproamento do aliviador em relação ao FPSO e à resultante ambiental;
- capacidade de manutenção de posição do navio aliviador;
- limites ambientais e margens de segurança para vento, ondas e corrente;
- critérios de continuidade, suspensão e desconexão quando as condições deixam de ser seguras.

Nos trechos disponíveis, o envelope não aparece como um único número ou uma única curva. Ele é tratado como um conjunto de restrições geométricas, operacionais e de desempenho dinâmico. Em operações tandem, o alvo perseguido pelo navio aliviador tende a ser uma caixa de reação associada à estação de alívio do F(P)SO, e a operação deve respeitar simultaneamente a distância estabelecida e os ângulos dos setores operacionais.

Em termos práticos, o envelope metocean serve para responder quatro decisões operacionais:
1. se a operação pode iniciar;
2. se pode continuar;
3. quando deve ser colocada em condição de atenção ou suspensão;
4. quando a desconexão ou abortamento passa a ser a resposta segura.

**Fontes:** `regis-e8017584b2db5d2b9e42246a:pNone:1900.0-2091.0`, `regis-e8017584b2db5d2b9e42246a:pNone:2002.0-2170.0`

## 2. Influência da configuração de ancoragem no envelope metocean

### 2.1 FPSO com spread mooring

No sistema Spread Mooring System, várias linhas de ancoragem são conectadas ao perímetro do casco, mantendo o aproamento do FPSO praticamente fixo. Isso altera profundamente a lógica do offloading:
- o FPSO deixa de girar livremente para acompanhar a resultante ambiental;
- o navio aliviador passa a conviver com um obstáculo de aproamento fixo;
- a direção combinada de vento, onda e corrente pode empurrar o aliviador para fora do setor operacional admissível;
- a incidência ambiental pode ocorrer com maior desfavorabilidade relativa, inclusive em situações oblíquas ou de través para a unidade fixa.

Os trechos indicam que, no Brasil, a maior parte dos FPSOs considerados é spread moored. Para esse contexto, foi citado um afastamento operacional típico de 150 m para o navio aliviador com DP, em modo de operação descrito como Normal Mode, no qual o sistema de posicionamento mantém automaticamente um ponto fixo de referência, enquanto o navio aliviador pode alinhar seu aproamento com a resultante ambiental sem mudar a coordenada GPS do ponto de referência do seu través médio.

Também foi relatado que ocorreram desconexões de emergência na Bacia de Santos porque o navio-tanque foi empurrado para fora do setor verde por resultantes ambientais apontando para oeste. Isso mostra que, em FPSOs de aproamento fixo, a decisão de continuar ou abortar offloading depende fortemente não apenas da intensidade dos agentes ambientais, mas também da sua direção resultante em relação ao setor aprovado.

### 2.2 FPSO com turret ou outros sistemas de ponto único

Nos sistemas de ponto único, incluindo turret mooring, a unidade pode variar seu aproamento para se alinhar mais favoravelmente à resultante ambiental. Esse comportamento de weathervaning tende a reduzir as cargas ambientais globais sobre o casco e o sistema de ancoragem, o que muda o envelope operacional do offloading.

Os trechos de literatura resumidos na dissertação apontam que, no Mar do Norte, muitos FPSOs são single point moored, operam alinhados às condições ambientais e realizam offloading com o navio aliviador em distâncias típicas de 80 a 100 m. Nesses casos, a operação citada usa frequentemente modo Taut Hawser, com a distância ao FPSO sendo garantida manualmente pelo comandante e a tensão do hawser mantida até 20 t.

### 2.3 Consequência operacional

A comparação entre FPSOs spread moored e unidades com turret/SPM leva a uma conclusão importante: **limites ambientais, setores e distâncias descritos na literatura internacional não podem ser transferidos diretamente para o caso brasileiro de FPSOs com aproamento fixo**. O próprio material ressalta a necessidade de cautela ao interpretar recomendações produzidas para instalações e filosofias operacionais diferentes.

**Fontes:** `petroles-4ee4bce16acf674505c8912d:pNone:1806537.0-1806582.0`, `regis-e8017584b2db5d2b9e42246a:pNone:1900.0-2091.0`, `petroles-004c2afadba7ea17c7dd7908:pNone:3025145.0-3025174.0`, `petroles-004c2afadba7ea17c7dd7908:pNone:4402469.0-4402501.0`

## 3. Setores operacionais: geometria, distância e função de segurança

### 3.1 Estrutura dos setores

Os trechos disponíveis mencionam a lógica de setores verde, amarelo e vermelho, associada à posição relativa do aliviador em relação ao FPSO e à estação de alívio. Embora os excertos não tragam uma tabela formal de ações por cor, eles mostram que:
- o respeito ao setor verde é condição central de continuidade da operação;
- sair do setor verde esteve associado, na prática, a desconexões de emergência;
- a geometria do setor deve ser analisada junto com a distância ao FPSO, a filosofia de aproximação e o risco de colisão.

Durante a fase de aproximação, foi explicitado que o navio aliviador deve manter distância mínima de 50 m em relação ao F(P)SO por razões de segurança.

### 3.2 Exemplos de envelopes setoriais citados

Os trechos fornecem exemplos de referência, que são úteis como comparação de filosofia, mas não devem ser tomados como universais:
- diretriz UKOOA para tandem loading: permite o shuttle mais próximo do FPSO do que alguns critérios brasileiros, citando distância de até 60 m durante a operação, porém com limitação mais restritiva para a posição da proa do shuttle, em ±25°;
- qualificação de um novo navio DP para operação com FPSO spread moored: setor do tipo banana, de -60° a bombordo e +75° a boreste, a 300 m do FPSO, validado por simulações em tempo real;
- estudo numérico para terminal LNG spread moored: por leitura gráfica, o setor verde parece ser aproximadamente ±45° e o amarelo ±60°, mas o próprio trecho informa que esses parâmetros não foram explicitamente publicados;
- caso Sevan Marine em FPSO cilíndrico spread moored no Mar do Norte: distância aproximada de 250 m, grande faixa de aproamentos possíveis do navio DP e estratégia de apontar para um ponto de pivô que não coincide com a estação de alívio, reduzindo o risco de colisão em caso de perda de posicionamento.

### 3.3 Leitura técnica desses exemplos

Os exemplos acima sugerem uma regra de engenharia importante: **a abertura angular admissível do setor depende do afastamento, da estratégia de referência usada pelo DP, do arranjo de offloading e da filosofia de segurança contra colisão**. Em geral, maior distância pode permitir setor angular mais amplo, mas isso precisa ser demonstrado por análise de risco e simulação, e não presumido.

**Fontes:** `regis-e8017584b2db5d2b9e42246a:pNone:1900.0-2091.0`, `regis-e8017584b2db5d2b9e42246a:pNone:2002.0-2170.0`

## 4. Variáveis metocean que controlam o envelope

### 4.1 Ação combinada de vento, ondas e corrente

Os trechos deixam claro que o desempenho da operação depende da ação simultânea de vento, ondas e corrente, com magnitudes e direções distintas. O problema não é apenas o valor máximo de cada agente isoladamente, mas a resultante combinada aplicada ao FPSO, ao navio aliviador e ao sistema de conexão.

Nas análises e simulações citadas, são observados:
- movimentos de ambas as embarcações;
- movimentos relativos entre elas;
- cargas no hawser e em outras linhas;
- forças de vento, onda e corrente;
- forças aplicadas por rebocadores e pelo sistema de ancoragem.

Isso mostra que o envelope operacional é um envelope de sistema, e não apenas do navio aliviador isolado.

### 4.2 Direção e rapidez de mudança das condições

O material destaca atenção especial para:
- rip currents;
- squalls;
- mudanças rápidas de velocidade e/ou direção do vento e da corrente.

Esses eventos reduzem a previsibilidade do stationkeeping e podem causar excursão rápida do aliviador para fora do setor seguro. Em operações com FPSO spread moored, isso é particularmente crítico, porque a unidade de produção não gira livremente para aliviar a incidência ambiental desfavorável.

### 4.3 Variação de calado durante a transferência

Os textos também salientam que, durante o offloading, as embarcações experimentam grandes variações de calado. Isso altera os carregamentos ambientais predominantes e, por consequência, modifica a dinâmica do sistema. Portanto, o envelope ambiental de início da operação não deve ser tratado como permanente: a margem disponível pode mudar ao longo da transferência.

### 4.4 Incidência oblíqua e de través em FPSOs de aproamento fixo

Há indicação de que FPSOs SMS são mais suscetíveis a receber ondas extremas oblíquas, de bochecha ou de través do que unidades com turret. Embora o trecho citado discuta principalmente embarque de água, o ponto é relevante para offloading: a orientação fixa da unidade pode produzir combinações de direção de onda e corrente mais penalizantes para a permanência do aliviador no setor operacional.

**Fontes:** `petroles-004c2afadba7ea17c7dd7908:pNone:3025145.0-3025174.0`, `regis-e8017584b2db5d2b9e42246a:pNone:2002.0-2170.0`, `petroles-004c2afadba7ea17c7dd7908:pNone:4402469.0-4402501.0`

## 5. Critérios metocean para iniciar a operação

Com base nos trechos, o início do offloading deve ser condicionado, no mínimo, aos seguintes elementos:

### 5.1 Previsão ambiental compatível com o envelope aprovado

Antes do início, deve-se verificar a previsão meteoceanográfica da operação pretendida em relação aos limites seguros do terminal e do navio aliviador. O material destaca explicitamente a necessidade de comparar a previsão com limites seguros de alívio em terminais offshore.

Como várias cifras do material aparecem mascaradas, o ponto tecnicamente seguro a reter é: **a decisão de início depende de limites ambientais específicos da instalação e do navio, e não apenas de julgamento qualitativo de bom ou mau tempo**.

### 5.2 Compatibilidade entre direção ambiental prevista e setor operacional

Em FPSOs spread moored, não basta que vento, onda e corrente estejam abaixo de certos máximos. É necessário que a direção resultante prevista seja compatível com o setor operacional aprovado. O histórico citado de desconexões por empurrar o navio para fora do setor verde demonstra que a direção da resultante ambiental pode ser o fator crítico mesmo sem um estado extremo absoluto.

### 5.3 Adequação do navio aliviador ao cenário esperado

Os trechos indicam que, em cenários críticos, embarcações menores e com melhor capacidade de manobra podem ser priorizadas. Também se menciona a importância de avaliar a classe, a redundância e a capacidade do sistema de posicionamento dinâmico para a operação pretendida.

### 5.4 Favorabilidade da estação de alívio

Quando o FPSO dispõe de estações de alívio em proa e popa, a disponibilidade operacional melhora com essa flexibilidade. O material afirma que o downtime aumenta consideravelmente quando a estação de proa está inoperante. Logo, a seleção da estação de alívio deve integrar a decisão de início, principalmente sob previsão ambiental marginal.

**Fontes:** `regis-e8017584b2db5d2b9e42246a:pNone:247.0-456.0`, `petroles-004c2afadba7ea17c7dd7908:pNone:3025900.60-3025925.0`, `petroles-004c2afadba7ea17c7dd7908:pNone:3026709.60-3026769.0`

## 6. Critérios metocean para manter, suspender ou abortar o offloading

### 6.1 Critérios de manutenção

A operação deve permanecer dentro do envelope aprovado durante toda a transferência. Pelos trechos disponíveis, isso implica monitorar continuamente:
- permanência no setor operacional seguro, especialmente no setor verde;
- distância ao FPSO;
- aproamento relativo do aliviador;
- movimentos relativos entre as embarcações;
- cargas no hawser e nas linhas associadas;
- demanda de potência do sistema DP e sua margem remanescente;
- evolução de vento, onda e corrente, inclusive mudanças súbitas.

### 6.2 Situações que justificam suspensão ou abortamento

Os excertos apontam como situações críticas para suspensão ou abortamento:
- deslocamento do navio aliviador para fora do setor verde por ação da resultante ambiental;
- incapacidade de manter posição com margem suficiente do sistema DP;
- ocorrência ou iminência de drift-off, entendido no material como perda de posição por insuficiência de potência instalada para resistir aos agentes ambientais;
- mudanças rápidas de vento e corrente, como squalls e rip currents, capazes de elevar rapidamente movimentos relativos e cargas no hawser;
- condição em que a posição, a distância mínima, a excursão do navio, a tração no hawser ou os demais critérios operacionais deixem de ser atendidos.

### 6.3 Critério em condição degradada

O envelope não deve ser verificado apenas para condição intacta. O material menciona explicitamente a necessidade de avaliar a capacidade de manutenção de posição em estados degradados, incluindo perda de propulsores e cenários de pior falha singela. Isso é decisivo para a decisão de continuidade: uma operação aceitável em condição intacta pode deixar de ser aceitável se a margem em condição degradada for insuficiente.

**Fontes:** `regis-e8017584b2db5d2b9e42246a:pNone:247.0-456.0`, `regis-e8017584b2db5d2b9e42246a:pNone:2002.0-2170.0`, `petroles-004c2afadba7ea17c7dd7908:pNone:3026513.0-3026536.0`, `petroles-004c2afadba7ea17c7dd7908:pNone:3026709.60-3026769.0`

## 7. Capability plots, setor comprovado e limitação de potência

Os trechos apresentam os capability plots e as rosetas de potência como ferramentas centrais para definir o envelope metocean. Em termos funcionais:
- a roseta de potência avalia a demanda de potência do navio aliviador para manter a posição;
- o capability plot representa, em forma polar, a condição limite de vento e ondas associadas para a qual o navio ainda consegue manter posição.

Foi mencionado que é prática recomendada por entidades de referência considerar como capacidade comprovada de manutenção dinâmica da posição apenas o setor de aproximadamente ±30° em relação à proa da embarcação. Porém, o próprio texto ressalta que essa recomendação foi originalmente associada a sondas DP e depois aplicada a navios aliviadores operando com FPSOs de aproamento variável. Portanto, sua aplicação direta a terminais de aproamento fixo deve ser feita com cautela.

Essa observação é tecnicamente relevante: em FPSOs spread moored, o obstáculo fixo e a direção do setor podem tornar insuficiente uma leitura simplificada baseada apenas em capacidade genérica do DP. O que importa é a capacidade de manter a posição dentro do setor aprovado e com risco aceitável de colisão, poluição e desconexão.

**Fontes:** `petroles-004c2afadba7ea17c7dd7908:pNone:3026513.0-3026536.0`

## 8. Metodologia para definir ou revisar envelopes ambientais

Os trechos descrevem uma metodologia estruturada para revisar setores e envelopes de offloading com navios DP em FPSOs spread moored. As etapas citadas são:
1. Análise Preliminar de Riscos;
2. avaliação do ganho de disponibilidade da operação;
3. avaliação da demanda de potência do sistema DP nos setores original e estendido;
4. simulações em tempo real com operadores experientes;
5. testes de campo para validação.

A lógica dessa metodologia é importante para o tema metocean porque mostra que o envelope operacional não deve ser definido apenas por tradição operacional. Ele deve ser demonstrado por combinação de:
- risco;
- disponibilidade ou downtime;
- capacidade do DP;
- comportamento dinâmico realista;
- validação operacional.

Os resultados resumidos na dissertação indicam ganho médio de disponibilidade de até 9% na Bacia de Campos e 13% na Bacia de Santos com a extensão do setor, desde que as medidas mitigadoras levantadas na APR fossem implementadas.

Os trechos também informam que um setor operacional proposto já incorporava limitações do hawser e condições mais abrangentes para operação segura. Mesmo assim, o próprio material recomenda, como continuidade técnica, análises dinâmicas adicionais para tração no hawser, distância mínima ao FPSO, excursão do navio, simulações em tempo real e ensaios/validações complementares.

**Fontes:** `regis-e8017584b2db5d2b9e42246a:pNone:247.0-456.0`, `petroles-004c2afadba7ea17c7dd7908:pNone:3026709.60-3026769.0`

## 9. Síntese prática para decisão operacional

### 9.1 Iniciar

Iniciar o offloading apenas quando:
- a previsão metoceanográfica estiver dentro do envelope aprovado para a instalação e o navio;
- a direção resultante prevista for compatível com o setor operacional aprovado;
- a estação de alívio selecionada for favorável e estiver operacional;
- a análise de capacidade de posicionamento, inclusive em condição degradada, suportar o cenário previsto;
- houver margem de segurança suficiente para toda a duração prevista da operação, e não apenas para o instante inicial.

### 9.2 Manter

Manter a operação enquanto:
- o navio permanecer no setor seguro e na distância requerida;
- os movimentos relativos e as cargas no hawser permanecerem aceitáveis;
- a demanda de potência do DP conservar margem operacional adequada;
- não houver tendência de excursão que empurre o aliviador para fora do envelope.

### 9.3 Suspender ou abortar

Suspender ou abortar quando:
- a resultante ambiental ou sua mudança rápida criar tendência de saída do setor seguro;
- a capacidade de stationkeeping, principalmente em condição degradada, deixar de ser suficiente;
- os critérios de distância mínima, excursão, tração no hawser ou integridade do arranjo deixarem de ser atendidos;
- houver risco de drift-off, colisão, desconexão de emergência ou poluição.

## 10. Limites de aplicação deste documento

Os exemplos de ângulos, distâncias e modos operacionais citados pertencem a instalações e estudos diferentes, incluindo FPSOs spread moored, unidades com turret/SPM, navios DP auxiliares e terminais em regiões distintas. Portanto, eles servem para explicar mecanismos e critérios de engenharia, mas não substituem envelope aprovado da instalação específica.

**Fontes:** conjunto das seções anteriores.