# Hang-off, conexão e verificação final de risers em FPSOs

## 1. Papel técnico do hang-off e da conexão final

Na etapa final do **pull-in** de um riser até o FPSO, a operação deixa de ser dominada pela tração temporária do sistema de instalação e passa a ser dominada pela **transferência segura de cargas para a estrutura permanente** da unidade. Em termos práticos, isso significa que:

- o riser precisa chegar à posição final sem exceder o **raio mínimo de curvatura (MBR)** e sem danos à capa externa/revestimentos;
- o **conector de topo / end fitting** deve estar corretamente alinhado e apto a transmitir as cargas axiais, flexurais e, conforme o arranjo, torcionais para a estrutura do FPSO;
- a transição entre a flexibilidade do riser e a rigidez do casco, turret, I-tube, bell mouth ou outro ponto de conexão deve ocorrer com controle de curvatura e de concentração de tensões;
- a geometria final instalada deve permanecer dentro do **envelope de segurança** previsto em projeto.

Os requisitos de projeto citados no material da ANP reforçam que, para risers, devem ser considerados no mínimo: **criticidade para a unidade e para as conexões mecânicas**, mitigação de risco diante da capacidade reduzida de inspeção em operação, movimentos da unidade marítima por rotação e translação e interferências com outros dutos, linhas de ancoragem, estrutura, solo marinho e demais obstruções. Para a avaliação da conexão final, isso implica que o hang-off não pode ser tratado isoladamente: ele depende da resposta global do sistema unidade-riser-arranjo submarino.

Também é relevante que o projeto contenha documentação como folha de dados, diagrama do arranjo submarino, envelope de segurança, relatório meteoceanográfico e referências das análises de tensões e cargas. Esses documentos formam a base objetiva para aceitar ou rejeitar a condição final após o pull-in.

**Fontes:** `anp-226946a12711e04f54ee4bfb:p52-57:28.0-25.0`, `anp-226946a12711e04f54ee4bfb:p55-60:22.0-3.0`

## 2. Componentes críticos na conexão final

### 2.1 Conector / end fitting

O **conector** é um dos elementos mais críticos da linha flexível. Pelos trechos disponíveis, suas funções principais são:

1. **terminar e ancorar as camadas estruturais** da linha flexível, de forma que as trações e esforços de flexão sejam transmitidos à estrutura do conector;
2. **promover a transição** entre o corpo do riser e a conexão com a unidade flutuante;
3. **selar** as diferentes regiões do duto por meio das barreiras poliméricas;
4. **transmitir com segurança os carregamentos** e a transição de pressão entre o duto e o flange/elemento adjacente.

Os textos também indicam que, em conectores tradicionais de linhas flexíveis, a transferência de carga das armaduras de tração para a estrutura metálica do conector é obtida por geometria de ancoragem e preenchimento com **resina epóxi**. Como consequência, a integridade do conector depende não apenas das cargas em operação, mas também do histórico de fabricação e montagem da terminação.

Para o topo em FPSOs, o conector de topo tende a suportar os maiores carregamentos e, por isso, costuma ser uma região de **menor margem de fadiga** relativa quando comparada a outras interfaces da linha.

### 2.2 Flanges, spool e interface estrutural

A conexão final de topo normalmente faz a interligação do conector ao sistema da unidade, por exemplo a um **spool rígido** ou flange montado no FPSO. Os trechos citam flanges tradicionais e compactos; estes últimos podem ser atrativos quando há **restrição de espaço**, como em I-tubes pequenos. Na avaliação da conexão final, a compatibilidade geométrica e de carga entre conector, flange, spool e suporte estrutural é determinante para evitar desalinhamento e tensões parasitas.

### 2.3 Acessórios de controle de curvatura

Na região de topo, devido à forte diferença de rigidez entre o riser flexível e a estrutura do FPSO, são usados acessórios para controlar a curvatura:

- **bend stiffener**: promove uma transição suave de rigidez entre a linha e a unidade; é o acessório mais associado à proteção da conexão de topo em aplicações dinâmicas;
- **bend restrictor**: impede mecanicamente que a linha ultrapasse determinado raio mínimo de curvatura; os trechos consultados o associam principalmente a aplicações mais estáticas e a conexões submarinas, não tipicamente ao topo dinâmico do FPSO;
- **bell mouth**: limitador de curvatura ligado à estrutura da unidade, não à linha; pode induzir concentrações de tensão/compressão localizada e, segundo um dos trechos, não é o arranjo usual para FPSOs em águas profundas no Brasil.

Em termos de hang-off, isso significa que a aceitação da conexão final não depende apenas do travamento mecânico do conector, mas do **conjunto conector + acessório de curvatura + estrutura adjacente**.

**Fontes:** `petroles-004c2afadba7ea17c7dd7908:pNone:4085401.0-4085449.0`, `regis-bb4d33ecf4e2c91061213e85:pNone:552.60-573.0`, `petroles-004c2afadba7ea17c7dd7908:pNone:2661172.0-2661197.0`

## 3. Critérios de engenharia para aceitar a transferência de carga no hang-off

A transferência de carga do sistema temporário de pull-in para o arranjo permanente de hang-off deve ser avaliada por critérios combinados de **geometria, carga, integridade local e interferência**.

### 3.1 Continuidade do caminho de carga

A carga deve migrar de forma controlada:

- do sistema temporário de tração/pull-in;
- para a retenção provisória no ponto de chegada;
- e então para o **suporte definitivo** do conector/hang-off.

A condição aceitável é aquela em que o caminho de carga permanente fica claramente estabelecido, sem depender residual ou inadvertidamente do sistema temporário, sem apoio indevido do riser em bordas, guias ou na parede do I-tube.

### 3.2 Limites de curvatura, tensão e rotação

Os trechos não fornecem valores universais numéricos, mas são consistentes ao indicar que:

- as **tensões máximas e mínimas** ao longo da linha e as tensões/rotações no conector devem permanecer abaixo dos limites de projeto;
- o **raio mínimo de curvatura** não pode ser ultrapassado;
- a região próxima ao **bend stiffener** é particularmente sensível, inclusive com relatos de ultrapassagem de curvatura admissível nessa área.

Portanto, a avaliação de hang-off deve verificar se a geometria instalada não impõe:

- overbending na saída do conector ou na entrada do bend stiffener;
- contato indevido com I-tube, bell mouth, estrutura do turret ou casco;
- compressão localizada associada a arranjos inadequados de limitação de curvatura;
- torção ou desalinhamento capaz de reduzir a vida em fadiga.

### 3.3 Efeito dos movimentos do FPSO

Os movimentos da unidade afetam diretamente a integridade da conexão de topo. Os materiais consultados destacam que a conexão de topo é um dos pontos mais suscetíveis à **falha por fadiga** em risers flexíveis conectados a FPSOs com turret, justamente pela diferença de rigidez e pela excitação causada por ondas, correntes, offset e aproamento.

Além disso, uma configuração muito vertical pode reduzir a capacidade da linha de absorver deslocamentos da unidade, elevando os carregamentos de flexão no enrijecedor de topo. Na prática, a verificação final do hang-off não é apenas geométrica em condição estática; ela deve considerar se a posição final instalada é compatível com a resposta dinâmica prevista para a unidade.

### 3.4 Interferências e acessibilidade futura

A ANP exige que o projeto e a operação considerem interferências com outras linhas, estrutura da unidade, solo marinho e obstruções. Na aceitação do hang-off, isso se traduz em checar:

- folgas e clearances com estruturas adjacentes;
- possibilidade de inspeção futura;
- ausência de contato permanente não previsto;
- coerência entre a posição instalada e os documentos as-built.

**Fontes:** `anp-226946a12711e04f54ee4bfb:p52-57:28.0-25.0`, `petroles-004c2afadba7ea17c7dd7908:pNone:2661172.0-2661197.0`, `petroles-004c2afadba7ea17c7dd7908:pNone:4085401.0-4085449.0`, `regis-bb4d33ecf4e2c91061213e85:pNone:552.60-573.0`, `petroles-004c2afadba7ea17c7dd7908:pNone:473945.0-473980.0`

## 4. Sequência técnica genérica da conexão final e da transferência de carga

Os trechos fornecidos não descrevem um passo a passo universal de hang-off, mas permitem estabelecer uma sequência técnica genérica e dependente do arranjo:

1. **Chegada do riser ao ponto de conexão** com controle de tração, alinhamento e curvatura.
2. **Retenção temporária** e confirmação de posição/azimute do conector.
3. **Engajamento do conector e da estrutura permanente de hang-off**, respeitando a geometria prevista de apoio e reação.
4. **Instalação ou confirmação do posicionamento do acessório de controle de curvatura** (tipicamente bend stiffener na conexão de topo dinâmica).
5. **Conexão mecânica/hidráulica ao sistema da unidade**, por flange, spool ou arranjo equivalente.
6. **Transferência progressiva de carga** do sistema temporário para o suporte definitivo, com monitoramento da tração aplicada.
7. **Verificação de condição final**, incluindo curvatura, centralização, folgas, estanqueidade e integridade externa.

Durante essa sequência, a ANP requer que as tensões aplicadas sejam **monitoradas e registradas** durante o lançamento/instalação, ainda que indiretamente, e que existam procedimentos documentados contemplando equipamentos, etapas, limites meteoceanográficos, tensões/cargas e contingências como abandono, recuperação e danos à capa externa ou revestimento.

Embora o texto da ANP trate de forma ampla de lançamento e comissionamento de sistemas submarinos, esses princípios são diretamente úteis para o estágio final do pull-in, porque o risco de dano local ao riser na fase de hang-off é alto e a reversão costuma ser complexa.

**Fontes:** `anp-226946a12711e04f54ee4bfb:p52-57:28.0-25.0`, `anp-226946a12711e04f54ee4bfb:p55-60:22.0-3.0`, `petroles-004c2afadba7ea17c7dd7908:pNone:4085401.0-4085449.0`

## 5. Verificações pós-instalação e comissionamento

Após a transferência de carga e a conexão final, a aceitação técnica do riser deve combinar **inspeção física**, **testes funcionais/estanqueidade** e **rastreabilidade documental**.

### 5.1 Inspeção pós-instalação

Segundo a ANP, deve haver **inspeção submarina com registro de imagens** após o lançamento, com relatório contendo no mínimo:

- coordenadas e perfil do duto/riser;
- cruzamentos e interferências com linhas rígidas, flexíveis, umbilicais, cabos e outros equipamentos;
- posição as-laid de componentes e complementos;
- vãos livres detectados e corrigidos, quando aplicável;
- condição do duto quanto a danos em anodos, revestimento ou capa externa.

Para o foco em hang-off, isso significa ampliar a verificação para a região de topo e suas interfaces, observando especialmente:

- condição da **capa externa** e da região do conector;
- posicionamento do **bend stiffener** e de acessórios auxiliares;
- indícios de **abrasão**, esmagamento, marcas de contato ou desalinhamento;
- interferência do riser com estrutura do FPSO ou com outros risers.

### 5.2 Comissionamento

A ANP determina que o procedimento de comissionamento contemple, conforme aplicável:

- limpeza;
- teste de estanqueidade e/ou teste hidrostático;
- calibração;
- teste de continuidade elétrica e isolamento do sistema de proteção catódica;
- teste de funcionamento de componentes e complementos;
- teste de funcionalidade de componentes de umbilicais;
- testes do sistema de vent;
- condicionamento.

Também devem existir **critérios de aceitação documentados** para testes e ensaios e relatório de comissionamento com descrição, referências, resultados, anormalidades e conclusões.

Na etapa final de conexão do riser ao FPSO, os itens mais diretamente ligados ao hang-off são:

- **estanqueidade** da conexão de topo e da interface com spool/flange;
- **funcionamento** de componentes associados ao conector e ao vent, quando existentes;
- **coerência entre a posição física instalada e a configuração prevista em projeto**;
- registro formal das **anormalidades encontradas**.

### 5.3 Verificações específicas recomendadas para risers flexíveis

A literatura compilada indica que inspeções visuais podem detectar, entre outros:

- danos, abrasão, ruptura, vazamento e deformações na capa externa;
- falhas na válvula de alívio da seção de topo;
- falhas na armadura de pressão;
- configuração inadequada de catenária;
- interferência entre risers ou entre riser e embarcação;
- instabilidade torcional;
- ruptura de arames da armadura de tração;
- danos na seção de topo do riser flexível;
- falhas, envelhecimento ou má fixação do bend stiffener;
- ingresso de água do mar no espaço anular.

Esses pontos são particularmente importantes porque a conexão final pode aparentar estar montada corretamente e ainda assim abrigar uma condição incipiente de dano por contato, desalinhamento ou comprometimento da capa externa.

**Fontes:** `anp-226946a12711e04f54ee4bfb:p52-57:28.0-25.0`, `anp-226946a12711e04f54ee4bfb:p55-60:22.0-3.0`, `petroles-004c2afadba7ea17c7dd7908:pNone:2990188.0-2990221.0`

## 6. Monitoramento após entrada em operação inicial

Depois da aceitação do hang-off e do comissionamento, a integridade da conexão final depende de operar o sistema **dentro do envelope de segurança** e monitorar variáveis e anormalidades.

Conforme a ANP, o operador deve:

- garantir operação dentro dos limites do envelope de segurança;
- registrar e investigar desvios;
- monitorar variáveis operacionais com limites de alarme e análise de tendência;
- adotar controles e monitoramento adicionais quando não houver acompanhamento por sistema supervisório;
- comunicar anormalidades e contingências às áreas/empresas envolvidas;
- avaliar periodicamente a capacidade dos meios de detecção e monitoramento de vazamentos.

Para o topo de risers flexíveis, a literatura também recomenda atenção a sistemas de **monitoramento do gás percolado no anular** quando houver conector emerso conduzindo hidrocarbonetos. Isso não substitui inspeção estrutural, mas pode antecipar evidências de degradação da capa externa, entrada de água, permeação e ambiente corrosivo nas armaduras metálicas.

**Fontes:** `anp-226946a12711e04f54ee4bfb:p55-60:22.0-3.0`, `petroles-004c2afadba7ea17c7dd7908:pNone:2990188.0-2990221.0`

## 7. Falhas típicas, sinais de alerta e resposta técnica

Na região de hang-off/conexão final, os sinais de alerta mais relevantes nos trechos fornecidos são:

- aumento anormal de curvatura na transição do conector para o bend stiffener;
- contato não previsto entre riser e I-tube/estrutura;
- dano, abrasão ou perda de vedação da capa externa;
- falhas na seção de topo e em acessórios;
- indícios de ingresso de água do mar no anular;
- vazamento detectado em teste de estanqueidade, sistema de vent ou monitoramento do anular;
- instabilidade torcional, ruptura de arames e degradação por fadiga/corrosão.

As respostas técnicas compatíveis com o material consultado incluem:

1. **interromper ou restringir a progressão operacional** se a condição exceder o envelope de segurança;
2. **registrar e investigar o desvio**;
3. executar **inspeção visual/ROV/boroscopia**, conforme acessibilidade;
4. repetir ou complementar **testes de estanqueidade/vent/anular** quando houver suspeita de dano na região de topo;
5. realizar **análise estrutural local** quando houver indício de contato, desalinhamento ou curvatura excessiva;
6. documentar conclusões e medidas corretivas.

A ANP também exige procedimento de contingência documentado para situações como **abandono, recuperação e danos ao revestimento ou capa externa**, o que é diretamente pertinente se, durante a fase final do pull-in, a conexão não puder ser aceita com segurança.

**Fontes:** `anp-226946a12711e04f54ee4bfb:p52-57:28.0-25.0`, `anp-226946a12711e04f54ee4bfb:p55-60:22.0-3.0`, `petroles-004c2afadba7ea17c7dd7908:pNone:2990188.0-2990221.0`

## 8. Exemplo aplicado: vazamento no anular e contato com I-tube

Um caso relatado na literatura compilada é útil para entender a importância da verificação final, sem transformá-lo em regra universal.

Nesse caso, após análises de fadiga e inspeções, foi realizada campanha de **teste anular** com objetivos de:

- verificar agentes corrosivos no anular;
- estimar volume livre entre camadas metálicas;
- verificar integridade da camada externa na seção superior;
- medir a capacidade de ventilação das portas de vent.

Os resultados indicaram possível vazamento de anular em um riser de produção conectado a FPSO. Em seguida, uma **boroscopia no interior do I-tube**, feita a partir de janelas de inspeção abaixo do hang-off, revelou que:

- o riser estava em contato com a parede do I-tube;
- o riser não estava centralizado;
- bolhas apareciam no ponto de contato durante injeção de N2, confirmando o vazamento naquela região;
- não era possível descartar danos adicionais em áreas sem acesso visual.

A recomendação subsequente foi desenvolver **estudo numérico** para reproduzir a forma deformada do riser dentro do I-tube, considerando as condições de hang-off e bend stiffener, de modo a estimar cargas e outros possíveis pontos de contato.

A lição técnica para a faceta de hang-off é direta: uma conexão final aparentemente concluída pode ainda esconder **contato indevido, perda de centralização, abrasão e vazamento local**, exigindo inspeção dirigida e eventual reavaliação estrutural.

**Fontes:** `petroles-004c2afadba7ea17c7dd7908:pNone:473945.0-473980.0`

## 9. Síntese prática para aceitação da conexão final

Uma avaliação profissional da conexão final do riser após o pull-in, com base nos trechos disponíveis, deve confirmar pelo menos os seguintes pontos:

- o conector/end fitting está corretamente engajado e com **caminho de carga permanente** estabelecido;
- a transferência de carga foi feita com **monitoramento de tração** e sem evidência de sobrecarga local;
- a geometria final respeita **MBR, limites de tensão/rotação e folgas estruturais** definidos em projeto;
- o **bend stiffener** ou acessório equivalente está adequadamente posicionado e funcional na transição de rigidez;
- não há **interferência, contato não previsto, abrasão ou desalinhamento** na região de topo/I-tube/turret;
- a inspeção pós-instalação e o comissionamento confirmaram **estanqueidade, condição externa e funcionalidade** dos componentes aplicáveis;
- os registros **as-built, relatórios de inspeção, comissionamento e anormalidades** foram emitidos e arquivados com rastreabilidade.

Sem esses elementos, a conexão final não deve ser tratada como tecnicamente verificada apenas por ter sido mecanicamente concluída.

**Fontes:** `anp-226946a12711e04f54ee4bfb:p52-57:28.0-25.0`, `anp-226946a12711e04f54ee4bfb:p55-60:22.0-3.0`, `petroles-004c2afadba7ea17c7dd7908:pNone:4085401.0-4085449.0`, `petroles-004c2afadba7ea17c7dd7908:pNone:2990188.0-2990221.0`, `petroles-004c2afadba7ea17c7dd7908:pNone:473945.0-473980.0`, `regis-bb4d33ecf4e2c91061213e85:pNone:552.60-573.0`