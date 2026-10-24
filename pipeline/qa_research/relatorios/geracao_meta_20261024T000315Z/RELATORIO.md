# Geração por meta (v16): 100 questões válidas por tópico

Janela com o prompt v16 (sem decisão), compostas a partir dos encadeamentos, auditoria como filtro e banco dinâmico de exemplos e contraexemplos.

| Tópico | Tema | blocos | encadeamentos | passagens de janela | rodadas | válidas | meta | janela aprov. | compostas aprov. |
|---|---|---|---|---|---|---|---|---|---|
| 01_01 | Gestão do Desempenho Empresarial (KPI) | 24 | 32 | 60 | 3 | **104** | ✓ | 92/239 | 12/32 |
| 02_03 | Tratamento de água produzida para descarte | 27 | 13 | 53 | 3 | **102** | ✓ | 96/204 | 6/13 |
| 03_01 | Operação de Offloading | 30 | 27 | 50 | 4 | **101** | ✓ | 94/198 | 7/26 |
| 04_02 | Operações submarinas, poços, manifolds, PLEM  | 33 | 32 | 50 | 2 | **102** | ✓ | 95/200 | 7/32 |
| 05_02 | Geração e distribuição de energia elétrica | 21 | 30 | 42 | 2 | **100** | ✓ | 85/167 | 15/30 |
| 06_05 | Sistema de Fogo e Gás (F&G) | 20 | 30 | 52 | 3 | **107** | ✓ | 101/205 | 6/30 |
| 07_04 | Inspeção e Integridade | 31 | 27 | 69 | 3 | **120** | ✓ | 106/275 | 14/27 |
| 08_03 | Meio Ambiente, Gestão Ambiental e Sustentabil | 28 | 36 | 46 | 2 | **103** | ✓ | 85/180 | 18/36 |
| 09_02 | Movimentação de Cargas | 27 | 31 | 63 | 3 | **115** | ✓ | 101/244 | 14/31 |
| 10_01 | Geral | 23 | 0 | 67 | 4 | **97** | ✗ | 97/262 | 0/0 |

| Tipo | janela (aprov./geradas) | compostas (aprov./geradas) |
|---|---|---|
| conceito | 185/550 | 0/0 |
| mecanismo | 331/475 | 7/7 |
| consequencia | 96/340 | 20/61 |
| diagnostico | 192/388 | 28/75 |
| decisao | 0/0 | 44/114 |
| procedimento | 148/421 | 0/0 |

Por rodada (0 = compostas): r0: 99/257 (dup. 0); r1: 493/1056 (dup. 0); r2: 336/852 (dup. 2); r3: 120/252 (dup. 1); r4: 3/14 (dup. 0).
Banco dinâmico: {'aprovadas': 1051, 'reprovadas': 1377}. Falhas pendentes: 2.

## Amostra de aprovadas por tópico

### 01_01

**[consequencia · composta]** Num FPSO de alta produção, foi adiada para evitar gasto imediato a correção de uma barreira crítica com teste funcional vencido e falha ainda não eliminada. A função protegida por ela é necessária para operar dentro das premissas aprovadas, e não há contingência equivalente disponível. Qual é a principal consequência econômica potencial dessa decisão?

- Resposta: Perda potencial elevada de receita diária, porque numa unidade de alta produção a indisponibilidade ligada à barreira crítica compromete maior valor de produção.

**[diagnostico · simples]** Em duas bombas de serviço equivalentes de um FPSO, o número de falhas no trimestre é igual e a intervenção física em cada falha dura praticamente o mesmo. Mesmo assim, uma delas acumula muito mais horas fora de serviço; nos registros, os maiores intervalos ocorrem antes do início do reparo e antes do retorno seguro à operação. Qual causa específica explica esse pior resultado?

- Resposta: Tempos logísticos e administrativos mais longos por falha, não maior reparo ativo.

**[diagnostico · simples]** Em um FPSO, após aumentar o número de mantenedores, a indisponibilidade quase não cai. Nos eventos recentes, havia equipe pronta, mas o retorno só ocorreu após janela de acesso, chegada de sobressalente e liberação de trabalho; o reparo executado foi curto. Qual causa específica explica melhor esse ganho limitado?

- Resposta: Esperas por acesso, sobressalente, liberação ou logística dominam o retorno operacional, não a capacidade das equipes.

**[diagnostico · simples]** Após mudar a extração automática dos eventos de manutenção de uma bomba do FPSO, a duração média por ocorrência aumentou. A intervenção mecânica em campo permaneceu com a mesma duração, e os registros agora começam no diagnóstico e terminam apenas após liberação e retorno seguro. Qual causa específica explica o aumento?

- Resposta: O cálculo passou a usar a indisponibilidade total da falha, e não apenas o reparo ativo.

### 02_03

**[conceito · simples]** Nas famílias ATO, MTO e BTO, qual dimensão do hidrociclone é relevante tanto no projeto quanto no ajuste operacional?

- Resposta: O diâmetro do orifício de overflow.

**[consequencia · simples]** Se, após a colisão, a interface entre bolha e gota ficar pouco favorável à adesão, o que acontece com a remoção de óleo na flotação?

- Resposta: Ela cai, porque menos agregados bolha-gota se mantêm estáveis até a ascensão.

**[mecanismo · simples]** Por que bolhas menores podem ampliar a área interfacial e, ainda assim, não garantir melhor desempenho da flotação?

- Resposta: Porque bolhas menores também mudam a velocidade de ascensão e a interação bolha-gota/floco; o desempenho passa a depender da distribuição de tamanhos, estabilidade da dispersão, carga de óleo e hidrodinâmica.

**[mecanismo · simples]** Por que a simples injeção de gás não garante bom desempenho da flotação em água oleosa?

- Resposta: Porque a separação só ocorre com colisão, adesão e sobrevivência do agregado; sem essa cadeia, o óleo não ascende à região de coleta.

### 03_01

**[consequencia · simples]** Durante a aproximação a um FPSO spread moored de aproamento fixo, vento, corrente e ondas mudam de direção. Que efeito isso tende a ter sobre o posicionamento do navio aliviador?

- Resposta: A exigência de posicionamento aumenta no aliviador, com mais acomodação das mudanças ambientais pela sua estratégia de controle.

**[conceito · simples]** Na parada de emergência do offloading, qual é a finalidade física principal da desconexão?

- Resposta: Reduzir a energia transmitida entre os corpos flutuantes e limitar a escalada do evento.

**[mecanismo · simples]** Como as válvulas fazem a mesma energia fornecida pela bomba resultar em diferentes vazões e pressões na linha de offloading?

- Resposta: Redistribuindo as perdas de carga do circuito, o que altera como a energia da bomba se traduz em vazão e pressão.

**[diagnostico · simples]** Após bom desempenho de um conceito sem hawser em uma unidade, decidiu-se replicá-lo sem mudanças em outras. Na réplica, não se reavaliaram afastamento, lógica de posicionamento nem arranjo para mangote e carretel. Qual característica técnica do conceito original explica a inadequação dessa replicação direta?

- Resposta: Dependência de premissas de projeto; é arquitetura específica, não substituição universal das práticas com hawser.

### 04_02

**[mecanismo · simples]** Como um comando enviado pela estação mestra se converte em abertura ou fechamento de uma válvula gaveta subsea?

- Resposta: O módulo converte o comando em sinal elétrico para a unidade hidráulica, que pressuriza o cilindro e desloca o atuador da válvula.

**[mecanismo · composta]** Em inspeção com ROV numa linha rígida, a parede externa não mostra corrosão nem dano marcante, e a campanha mediu vão livre em um trecho antes apoiado no leito. Para justificar a avaliação estrutural do trecho mesmo sem perda visível de parede, por que esse achado importa?

- Resposta: Mudança das condições de contorno e da resposta dinâmica da linha, porque o vão livre altera tensões e estabilidade mesmo sem dano visível imediato.

**[mecanismo · simples]** Como uma perturbação de processo no topside pode levar à parada de produção sem indicar falha da barreira primária do poço?

- Resposta: Ela atua no processo de superfície e pode acionar a parada, enquanto o envelope de contenção do poço permanece íntegro.

**[procedimento · simples]** Na comparação de arquiteturas subsea com foco em perda de contenção, como a análise deve ir além de decidir onde produzir e separar?

- Resposta: Mapeando, em cada alternativa, volumes, energia de pressão, pontos de isolamento e meios de resposta a falhas.

### 05_02

**[mecanismo · simples]** Como ensaios operacionais sob carga aplicável revelam falhas que podem não aparecer em verificações sem carga na distribuição elétrica?

- Resposta: Ao submeter o sistema a esforço elétrico real, interação entre controles e aquecimento, fazendo aparecer falhas latentes.

**[conceito · simples]** Na distribuição elétrica offshore, qual configuração de barramento ajuda a conter falhas e simplificar intervenções?

- Resposta: Barramento seccionado.

**[mecanismo · simples]** Por que a realimentação parcial do painel principal por geração de emergência exige permissivos e isolamento adequado das fontes?

- Resposta: Para evitar paralelismo indevido, retroalimentação de partes não previstas e energização de cargas acima da capacidade e da finalidade da fonte emergencial.

**[mecanismo · simples]** Como alimentar duas estações master da ECOS pelo mesmo conjunto de UPS agrava a perda de supervisão quando esse conjunto falha?

- Resposta: Porque elimina a independência entre canais e converte a falha de um único UPS em perda simultânea dos dois caminhos de supervisão.

### 06_05

**[conceito · simples]** No F&G, como se denomina a condição obtida apenas com a retirada da inibição ou do bloqueio de um detector ou de uma zona?

- Resposta: Disponibilidade administrativa.

**[procedimento · simples]** Após instalar equipamentos temporários e barreiras corta-vento em um módulo do FPSO, como a malha de gás deve ser revista antes de operar nessa configuração?

- Resposta: Reanalisando a cobertura para a ventilação resultante e os novos caminhos preferenciais da dispersão, não só pela quantidade de detectores.

**[conceito · simples]** Qual instrumento transforma a decisão de engenharia do F&G em comandos verificáveis?

- Resposta: A matriz de causa e efeito.

**[mecanismo · simples]** Ao definir a proteção F&G para um cenário de gás, por que a análise não deve depender da identificação posterior de uma fonte específica de ignição?

- Resposta: Porque a resposta deve ser definida para a liberação e a dispersão em curso, considerando ignições possíveis sem depender de confirmar depois qual fonte iniciaria o evento.

### 07_04

**[conceito · simples]** Que fenômeno estrutural a revisão holística de anomalias busca revelar quando as pendências deixam de parecer independentes?

- Resposta: Potencial de colapso progressivo.

**[mecanismo · simples]** Como identificar o tipo de deterioração ajuda a definir simultaneamente onde examinar e qual técnica usar?

- Resposta: Porque o mecanismo de dano indica qual descontinuidade procurar e onde ela tende a ocorrer, orientando o método aplicável e o ponto de inspeção.

**[mecanismo · simples]** Como profundidade, abertura, orientação, acesso e contraste físico do defeito afetam a capacidade de detecção de uma técnica de inspeção?

- Resposta: Eles mudam a interação da técnica com o defeito e o material sadio, alterando o sinal obtido e a probabilidade de detecção.

**[mecanismo · simples]** Por que a entrada de hidrogênio atômico faz o metal perder tolerância a trincas?

- Resposta: Porque ele difunde-se e se concentra em defeitos e pontas de trinca, reduzindo ductilidade e tenacidade à fratura e facilitando a nucleação e o crescimento subcrítico.

### 08_03

**[conceito · simples]** Como se denomina a corrente aquosa separada da mistura óleo-água proveniente do poço após a segregação do hidrocarboneto?

- Resposta: Água produzida.

**[diagnostico · simples]** Uma atividade offshore entrou no processo autorizativo ambiental. O órgão pediu documentação da fase, mas não exigiu EIA/RIMA. Os dados disponíveis ainda se limitam a indícios de jazida, sem sistema completo de produção definido. Que distinção técnica explica essa combinação?

- Resposta: Licenciamento ambiental e exigência de EIA não são sinônimos.

**[mecanismo · simples]** Por que, nas fases iniciais de um projeto offshore, as interações ambientais tendem a ser menos definidas?

- Resposta: Porque a empresa ainda conhece menos a jazida, o reservatório e o arranjo definitivo de produção, limitando a definição de instalações, escoamento e interações ambientais.

**[mecanismo · simples]** Como a perda do vínculo entre uma remessa e seu resultado de caracterização eleva o risco de encaminhamento incompatível?

- Resposta: Porque a carga perde sua identidade, favorece mistura indevida e pode ser recebida ou tratada como corrente de classe errada.

### 09_02

**[conceito · simples]** No planejamento do içamento, que aspecto da seleção do equipamento é governado por peso, centro de gravidade, pontos de içamento, trajetória e raio?

- Resposta: A compatibilidade entre a carga e o equipamento.

**[mecanismo · simples]** Por que a análise de acidentes de içamento deve separar a queda da carga da falha estrutural catastrófica do equipamento?

- Resposta: Porque a queda da carga decorre de causas operacionais de trajetória ou conexão, enquanto a falha estrutural depende também da integridade, manutenção e condição do sistema.

**[conceito · simples]** Qual estrutura de gestão de equipamentos e acessórios portáteis usa armazenamento que reduza dano e deterioração, controle de uso e verificação pré-uso antes da liberação?

- Resposta: Rigging loft.

**[diagnostico · simples]** Num FPSO, a verificação do guindaste indicava folga para a carga, mas a análise da operação apontou limites menores ligados à embarcação de suprimento, à instalação e à configuração da carga na descida. Qual causa técnica explica essa divergência?

- Resposta: Capacidade utilizável do sistema real inferior à capacidade da máquina isolada.

### 10_01

**[procedimento · simples]** Na fase de definição da desmontagem offshore, como a execução aprovada deve ser preparada antes do campo?

- Resposta: Pela elaboração de orçamentos, cronogramas executivos e procedimentos.

**[mecanismo · simples]** Por que retirar o inventário material não elimina, por si só, o risco na abertura de equipamentos?

- Resposta: Porque energia elétrica, hidráulica, pneumática, mecânica e pressão residual ainda podem sustentar liberação ou movimento perigoso.

**[mecanismo · simples]** Como os levantamentos tornam confiável a base técnica das análises de transporte do FPSO?

- Resposta: Ao transformar a condição real levantada em premissas controladas de massa, distribuição de peso, centro de gravidade e lastro para o reboque.

**[diagnostico · simples]** A produção foi encerrada, mas dois risers seguem conectados, os umbilicais continuam energizados e o checklist de isolamento final dos poços ainda está aberto. Não há pendência ambiental, econômica ou de navegação sobre a destinação da ancoragem. Qual causa específica impede iniciar a retirada da ancoragem?

- Resposta: Dependências entre poços, risers, umbilicais e unidade ainda não encerradas com segurança.
