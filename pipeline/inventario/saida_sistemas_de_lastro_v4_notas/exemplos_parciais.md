# Exemplos parciais — Sistemas de Lastro (v4 notas)

Gerado do estado atual da execução (fatos e conceitos completos; notas parciais, lidas do cache).

## 1. Fatos

### operacao-de-offloading-01c1 (825 fatos)

**classificação da severidade** — `criterio_limite` · pertinência `fpso_direta` · coleção `regis`

- **Afirmação:** A severidade das consequências foi classificada pelo efeito mais grave apresentado pelo cenário acidental. Assim, se uma colisão implicasse lesões leves em pessoas e derramamento catastrófico de óleo, a severidade do cenário era classificada como catastrófica.
- **Condições:** Análise de risco seguindo a matriz de risco da norma PETROBRAS N-2782.
- **Citação literal:** > The consequences’ severity were classified following the most serious effect that an accident scenario presents, e.g., if a collision implied light injuries to people (category II following the risk matrix) and catastrophic oil spill (category V), the scenario severity was classified in category V – catastrophic.
- **Fonte:** 9388_AnaLuisadeBarrosOrsoliniCorr17.pdf (linhas None–None) https://zenodo.org/api/records/4726013/files/Petroles/regis-collection-1.0.zip/content
- **Assuntos:** a20, a24, a25 · fid `regis:regis-e8017584b2db5d2b9e42246a:pNone:w16500#f2` · score 0.6539

**correção de trim e banda** — `procedimento` · pertinência `transferivel` · coleção `regis`

- **Afirmação:** A diferença de calado entre popa e proa, chamada de trim, é corrigida por tanques de lastro localizados avante e a ré. A diferença entre bombordo e boreste, chamada de banda, é corrigida por tanques de lastro laterais.
- **Condições:** embarcações com tanques de lastro distribuídos no casco
- **Citação literal:** > A diferença de calado (parte submersa do casco) entre popa e proa, chamada de trim, é corrigida pelos tanques de lastro localizados avante e a ré da embarcação. A diferença entre bombordo e boreste, chamada de banda, é corrigida por tanques de lastro laterais
- **Fonte:** 22770_CT_COECI_2016_2_18.pdf (linhas None–None) https://zenodo.org/api/records/4726013/files/Petroles/regis-collection-1.0.zip/content
- **Assuntos:** a14 · fid `regis:regis-fc5c7ea3896ba60666702e05:pNone:w3000#f1` · score 0.5681

**avaliação carregado/lastro do NADP** — `procedimento` · pertinência `fpso_direta` · coleção `petroles`

- **Afirmação:** A sequência de avaliar carregado e depois lastro é usada para garantir que o downtime calculado para cada combinação de NADP, setor operacional e condição ambiental represente toda a duração da operação de offloading.
- **Condições:** avaliação de downtime de operações de offloading com NADP
- **Citação literal:** > Esta é uma forma de garantir que os resultados de downtime para uma determinada combinação de NADP setor operacional e condição ambiental consideraram toda a duração da operação de offloading
- **Fonte:** corpusPublico(sem IBICT)-SemProcessamento.txt (linhas 3026635–3026646) 
- **Assuntos:** a06, a14, a17 · fid `petroles:petroles-004c2afadba7ea17c7dd7908:pNone:w56745000#f4` · score 0.5786

**entradas do controle de REA** — `mecanismo` · pertinência `transferivel` · coleção `petroles`

- **Afirmação:** Em um sistema estudado para posicionamento dinâmico orientado à otimização de REA, a lógica é baseada em redes neurais. As entradas consideradas incluem tração no riser, densidade do fluido do riser, ângulos no topo e no fundo, LDA e corrente na superfície.
- **Condições:** Sistema estudado de DP para otimização dos ângulos das extremidades do riser.
- **Citação literal:** > A lógica do sistema é baseada em redes neurais e incorpora tração no riser densidade do fluido do riser ângulos no topo e no fundo LDA e corrente na superfície como dados de entrada
- **Fonte:** corpusPublico(sem IBICT)-SemProcessamento.txt (linhas 3313115–3313130) 
- **Assuntos:** a08 · fid `petroles:petroles-004c2afadba7ea17c7dd7908:pNone:w61784250#f4` · score 0.7295

### operacao-de-tanques-de-carga-lastro-sist-567f (666 fatos)

**redundância de referências de posição** — `requisito_normativo` · pertinência `transferivel` · coleção `petroles`

- **Afirmação:** Operações offshore com sondas DP requerem, como condição operacional ideal, sistemas de referência de posição operando continuamente com princípios físicos diferentes e modos de falha distintos, para configurar redundância. Esse requisito é estabelecido por normas e recomendações internacionais do IMO e do IMCA.
- **Condições:** operações offshore com sondas DP; referências internacionais IMO e IMCA
- **Citação literal:** > As operações offshore com sondas DP requerem como condições operacionais ideais um mínimo de <NUMBER> sistemas de referência de posição trabalhando continuamente baseados em <NUMBER> princípios físicos diferentes modos de falha distintos para configurar redundância
- **Fonte:** corpusPublico(sem IBICT)-SemProcessamento.txt (linhas 1917435–1917446) 
- **Assuntos:** a20 · fid `petroles:petroles-004c2afadba7ea17c7dd7908:pNone:w36984000#f4` · score 0.6088

**centro de gravidade por condição de carga** — `procedimento` · pertinência `fpso_direta` · coleção `regis`

- **Afirmação:** Para cada condição de carregamento, estimam-se a posição do centro de gravidade e os momentos de inércia. Esses valores são utilizados no cálculo do comportamento em ondas.
- **Condições:** Etapa de plano de capacidades, pesos e centros do projeto.
- **Citação literal:** > Por fim são estimados, para cada condição de carregamento, a posição do centro de gravidade e os momentos de inércia que serão utilizados no cálculo do comportamento em ondas.
- **Fonte:** 10660_EduardoMarcalVilameaCorr17.pdf (linhas None–None) https://zenodo.org/api/records/4726013/files/Petroles/regis-collection-1.0.zip/content
- **Assuntos:** a16 · fid `regis:regis-8c94a1769b7cc2dc1938325e:pNone:w16000#f1` · score 0.5855

**alarme independente de alto nível** — `criterio_limite` · pertinência `transferivel` · coleção `regis`

- **Afirmação:** Os tanques de carga dispõem de sistema de alarme de nível independente ajustado em 98%.
- **Condições:** Na listagem de equipamentos de carga, lastro e limpeza de tanques.
- **Citação literal:** > B.5.4 Sistema de medição de nível, pressão e temperatura dos tanques de carga B.5.5 Sistema de medição de nível dos tanques de lastro B.5.6 Sistema de alarme de nível independente (98%) dos tanques de carga
- **Fonte:** 13071_arquivo9603_1.pdf (linhas None–None) https://zenodo.org/api/records/4726013/files/Petroles/regis-collection-1.0.zip/content
- **Assuntos:** a07 · fid `regis:regis-a9d6385a9d52317e10a5aceb:pNone:w23250#f0` · score 0.5913

**monitoramento remoto de tanques** — `causa_efeito` · pertinência `transferivel` · coleção `regis`

- **Afirmação:** A leitura remota do nível e da temperatura dos tanques torna menos complexas as operações com tanques e aumenta a segurança operacional, porque permite ao operador na sala de controle conhecer a qualquer instante essas variáveis.
- **Condições:** Tanques de armazenamento em unidades como terminais e refinarias; operador na sala de controle.
- **Citação literal:** > Este sistema, além de tornar menos complexa, aumenta, sobremaneira, a segurança das operações que envolvem tanques em unidades, tais como Terminais e Refinarias, uma vez que permitem ao operador que se encontra na sala de controle dessas unidades conhecer a qualquer instante o nível e a temperatura dos tanques.
- **Fonte:** BTP_1983_26_4_11_Sistema_eletronico.pdf (linhas None–None) https://zenodo.org/api/records/4726013/files/Petroles/regis-collection-1.0.zip/content
- **Assuntos:** a04, a19, a20 · fid `regis:regis-d363c7bb3065c11a893baea7:pNone:w0#f0` · score 0.6072

### sistema-de-ancoragem-manutencao-e-monito-62e4 (997 fatos)

**sobrecarga de alarmes** — `causa_efeito` · pertinência `transferivel` · coleção `petroles`

- **Afirmação:** O cenário de excesso de alarmes eleva o risco à segurança das pessoas e das instalações, agrava a deterioração ambiental e causa perda de produção.
- **Condições:** operação de processos industriais
- **Citação literal:** > The main consequences of this scenario are the increased risk to personal safety facilities environment deterioration and loss of production
- **Fonte:** corpusPublico(sem IBICT)-SemProcessamento.txt (linhas 2452546–2452577) 
- **Assuntos:** a18 · fid `petroles:petroles-004c2afadba7ea17c7dd7908:pNone:w45895000#f3` · score 0.5606

**dinâmica própria de linhas e risers** — `procedimento` · pertinência `fpso_direta` · coleção `regis`

- **Afirmação:** No modelo de simulação do sistema como um todo, a dinâmica própria das linhas é desconsiderada. Já no cálculo do aproamento ótimo que minimiza, entre outros aspectos, o carregamento dinâmico sobre os risers, esses efeitos devem ser considerados.
- **Condições:** Modelo de simulação global do sistema; cálculo de aproamento ótimo que minimiza, entre outros aspectos, o carregamento dinâmico sobre os risers.
- **Citação literal:** > Assim, no modelo de simulação do sistema como um todo desconsidera-se a dinâmica própria das linhas. Cabe observar no entanto que para o cálculo do aproamento ótimo, apresentado na seção 4.2, no qual um funcional que considera (entre outros aspectos) o carregamento dinâmico sobre os risers é minimizado, tais efeitos devem ser levados em consideração.
- **Fonte:** 11104_Tese_final.pdf (linhas None–None) https://zenodo.org/api/records/4726013/files/Petroles/regis-collection-1.0.zip/content
- **Assuntos:** a07, a08, a14 · fid `regis:regis-1db2e6ddc65e363f3291307f:pNone:w24000#f1` · score 0.5874

**composição da linha taut-leg** — `definicao` · pertinência `transferivel` · coleção `petroles`

- **Afirmação:** As linhas da ancoragem taut-leg são constituídas por cabos de aço ou amarras nas extremidades e por cabo de poliéster no trecho intermediário.
- **Condições:** linhas de ancoragem taut-leg
- **Citação literal:** > As linhas da ancoragem Taut-Leg são constituídas nas suas extremidades por cabos de aço ou amarras e no seu trecho intermediário por cabo de poliéster
- **Fonte:** corpusPublico(sem IBICT)-SemProcessamento.txt (linhas 3567096–3567113) 
- **Assuntos:** a09 · fid `petroles:petroles-004c2afadba7ea17c7dd7908:pNone:w66349750#f3` · score 0.7617

**permissão de trabalho** — `requisito_normativo` · pertinência `transferivel` · coleção `anp`

- **Afirmação:** O Operador do Sistema Submarino deve estabelecer, implementar e documentar procedimento para emissão de permissão de trabalho, além de outros meios de controle, para gerenciar atividades que possam constituir riscos para a segurança operacional.
- **Condições:** Brasil; SGSS da ANP; Operador do Sistema Submarino; atividades com potencial de risco à segurança operacional.
- **Citação literal:** > O Operador do Sistema Submarino deverá estabelecer, implementa r e documentar procedimento para emissão de permissão de trabalho e outros meios de controle para gerenciar atividades que possam constituir riscos para a segurança operacional.
- **Fonte:** Regime de Segurança Operacional de Sistemas Submarinos e o Regulamento Técnico do Sistema de Gerenciamento de Segurança Operacional de Sistemas Submarinos – SGSS (p. 46–48) https://www.gov.br/anp/pt-br/assuntos/exploracao-e-producao-de-oleo-e-gas/seguranca-operacional/arq/regulamento_tecnico-sgss.pdf
- **Assuntos:** a26 · fid `anp:anp-226946a12711e04f54ee4bfb:p46:w9000#f0` · score 0.5915

## 2. Conceitos

### operacao-de-offloading-01c1

**Assunto a02** — None

- **Weathervaning e aproamento em ancoragem por turret/ponto único** (`01c1c3db6e:a02:k1`, relevância alta, 12 fatos)
  - *Foco:* Explicar como a ancoragem em ponto único, especialmente por turret, permite que o FPSO gire em torno do ponto de pivotamento e se alinhe à resultante de vento, ondas e corrente. A nota deve relacionar esse comportamento à redução de esforços no casco e à continuidade da produção e do carregamento durante o offloading.
- **Spread mooring: aproamento fixo e implicações operacionais para offloading** (`01c1c3db6e:a02:k2`, relevância alta, 12 fatos)
  - *Foco:* Explicar por que o Spread Mooring System mantém o aproamento praticamente fixo, como as linhas distribuídas no perímetro resistem aos carregamentos ambientais e por que isso altera tensões, número de linhas e ambiente de aplicação. A nota deve destacar também a disposição dos risers e do bordo livre para transferência de carga, incluindo impactos sobre a capacidade de conexão e a logística do offloading.

**Assunto a03** — None

- **Spread mooring, aproamento fixo e restrições ao offloading** (`01c1c3db6e:a03:k1`, relevância alta, 16 fatos)
  - *Foco:* Explicar como a distribuição das linhas no perímetro do FPSO praticamente fixa o aproamento, condiciona a resposta às condições ambientais e afeta diretamente a janela operacional de alívio. A nota deve ligar essa configuração a maiores tensões de amarração, escolha de aproamento pela ancoragem/arranjo submarino e dificuldades de posicionamento do navio aliviador.
- **Ancoragem por ponto único e turret: liberdade de alinhamento e implicações operacionais** (`01c1c3db6e:a03:k2`, relevância alta, 12 fatos)
  - *Foco:* Explicar como sistemas de ponto único concentram linhas e risers em um turret ou arranjo equivalente, permitindo weather-vaning e reduzindo esforços ambientais no casco. A nota deve diferenciar turret interno/externo e relacionar essa liberdade de alinhamento com limitações práticas como a disponibilidade de estação de offloading e o uso de thrusters em alguns arranjos.

**Assunto a04** — None

- **Alinhamento do navio aliviador com a resultante ambiental** (`01c1c3db6e:a04:k1`, relevância alta, 11 fatos)
  - *Foco:* Explicar como a combinação de vento, ondas e corrente define o melhor aproamento e a demanda de potência do aliviador nas fases de aproximação, conexão e manutenção de posição. A nota deve mostrar por que desalinhamentos e variações da resultante ambiental aumentam esforço de propulsão, deslocamentos relativos e risco de colisão.
- **Tipo de ancoragem e aproamento do FPSO sob vento, ondas e corrente** (`01c1c3db6e:a04:k2`, relevância alta, 14 fatos)
  - *Foco:* Explicar como o arranjo de ancoragem do FPSO/FSO altera sua capacidade de se alinhar aos agentes ambientais e como isso repercute no offloading. A nota deve contrastar SPM/weather-vaning, DICAS e amarração distribuída ou aproamento fixo, relacionando liberdade de giro, rigidez e carregamentos ambientais.

### operacao-de-tanques-de-carga-lastro-sist-567f

**Assunto a02** — None

- **Controle da atmosfera dos tanques durante enchimento, offloading e crude oil washing** (`567fdce5c3:a02:k1`, relevância alta, 11 fatos)
  - *Foco:* Explicar como o espaço livre dos tanques parcialmente cheios deve permanecer inertizado e com pressão controlada ao longo das fases de enchimento e esvaziamento. A nota deve cobrir ventilação, suprimento de gás inerte, recuperação de vapores/VOC, uso do header de IG e intertravamentos de pressão.
- **Sequência operacional e salvaguardas do offloading em tandem** (`567fdce5c3:a02:k2`, relevância alta, 19 fatos)
  - *Foco:* Explicar a sequência prática do offloading, desde aproximação, posicionamento seguro, amarração e conexão do mangote até pressurização da linha, controle de vazão, monitoramento, término, desconexão e afastamento. A nota deve também destacar permissivos, detecção de vazamentos e como falhas de equipamento ou mudanças sem análise degradam as barreiras de segurança.

**Assunto a03** — None

- **Estratégia operacional de recebimento, priorização e transferência entre tanques de carga** (`567fdce5c3:a03:k1`, relevância alta, 7 fatos)
  - *Foco:* Explicar como a distribuição de carga é condicionada pelo arranjo do sistema de armazenamento: quais tanques recebem a produção primeiro, quais são priorizados para óleo pronto para exportação e como a transferência entre tanques é executada operacionalmente. A nota deve destacar que a distribuição não é apenas uma decisão de volume, mas depende do roteamento disponível, da capacidade instalada e do momento operacional, como após offloading com a planta ainda produzindo.
- **Controle da condição de carregamento por computador de estabilidade e ferramentas de modelagem** (`567fdce5c3:a03:k2`, relevância alta, 4 fatos)
  - *Foco:* Explicar como a distribuição de carga entre tanques é registrada, atualizada e representada em sistemas de estabilidade, incluindo entradas automáticas dos conteúdos dos tanques e complementação manual de cargas não integradas. A nota deve mostrar como ferramentas de cálculo permitem definir condições de carregamento por massa, volume, percentual de enchimento e por subconjuntos de tanques, apoiando a conferência da distribuição planejada.

**Assunto a04** — None

- **Medição e controle da interface óleo-água em vasos e separadores** (`567fdce5c3:a04:k1`, relevância alta, 11 fatos)
  - *Foco:* Explicar por que o controle da interface é crítico para evitar contaminação cruzada entre correntes de óleo e água, e por que essa medição se torna difícil em presença de emulsão, espuma, turbulência e variações de densidade. A nota deve comparar princípios de medição aplicáveis, limitações operacionais e impactos de manutenção inadequada na confiabilidade do controle.
- **Estratégias de controle de nível e automação em vasos de processo** (`567fdce5c3:a04:k2`, relevância alta, 13 fatos)
  - *Foco:* Explicar como o nível pode ser controlado por integração do medidor à rede de controle, atuação em bombas, chokes e válvulas, e algoritmos por bandas. A nota deve conectar sensores, lógica de controle e efeitos operacionais, como estabilidade da vazão a jusante e prevenção de arraste de gás ou líquido.

### sistema-de-ancoragem-manutencao-e-monito-62e4

**Assunto a02** — None

- **Spread mooring: arranjo multiponto, heading fixo e implicações operacionais** (`62e43c1988:a02:k1`, relevância alta, 9 fatos)
  - *Foco:* Explicar como o FPSO é mantido por múltiplas linhas distribuídas no perímetro do casco, com aproamento praticamente fixo, e quais elementos de configuração compõem esse arranjo. A nota deve também cobrir quando esse sistema é preferido e as implicações para risers, offloading e quantidade de linhas.
- **Turret mooring / Single Point: pivotamento, weathervaning e transferência por bearings e swivels** (`62e43c1988:a02:k2`, relevância alta, 11 fatos)
  - *Foco:* Explicar o turret como arranjo de ponto único em que a unidade gira em torno da parte fixa ancorada ao fundo, permitindo weathervaning. A nota deve descrever o papel de bearings e swivels, a compatibilidade com risers e como vento, ondas e corrente definem heading e offset estático.

**Assunto a03** — None

- **Escolha da configuração de ancoragem e seus efeitos no comportamento global** (`62e43c1988:a03:k1`, relevância alta, 18 fatos)
  - *Foco:* Explicar como selecionar entre catenária convencional, taut-leg e linhas retesadas/tendões a partir do tipo de unidade, profundidade, operação, quantidade de risers, cargas ambientais, deriva admissível e arranjo submarino. Destacar os impactos da configuração no raio de ancoragem, interferências, restauração e custo do sistema.
- **Seleção de materiais e composição das linhas de ancoragem** (`62e43c1988:a03:k2`, relevância alta, 10 fatos)
  - *Foco:* Explicar como definir os materiais e a composição da linha ao longo do comprimento para equilibrar peso submerso, rigidez axial, resistência, durabilidade e capacidade de restauração. A nota deve mostrar por que águas profundas favorecem linhas mistas e o papel de amarras, cabos de aço e sintéticos nessa escolha.

**Assunto a04** — None

- **Profundidade d’água como critério de seleção da arquitetura de ancoragem** (`62e43c1988:a04:k1`, relevância alta, 8 fatos)
  - *Foco:* Explicar como a lâmina d’água entra na escolha entre configurações convencionais, taut-leg e outras arquiteturas, sempre em conjunto com tipo de unidade, operação, risers, cargas e custo. A nota deve mostrar por que águas profundas e ultraprofundas deslocam a seleção para soluções com menor raio e melhor desempenho geométrico.
- **Efeito da profundidade na geometria das linhas, raio de ancoragem e passeios da unidade** (`62e43c1988:a04:k2`, relevância alta, 14 fatos)
  - *Foco:* Explicar como o aumento da profundidade altera comprimento, projeção horizontal, raio de ancoragem, interação com o leito e offset admissível. A nota deve contrastar a catenária convencional com o taut-leg e relacionar essas diferenças ao posicionamento da unidade e ao congestionamento submarino.

## 3. Notas (cache, ainda sem gravação final)

### Arranjo e sequência operacional da exportação de óleo para navio aliviador em FPSO

**Resumo:** A exportação em FPSO é a etapa de escoamento do óleo já separado e armazenado nos tanques da unidade, acionada quando a capacidade de armazenagem precisa ser liberada para continuidade da produção. Quando o uso de dutos submarinos é economicamente ou tecnologicamente desfavorável, o escoamento passa a ser feito por navio aliviador, em uma operação que combina amarração, conexão de mangotes, teste de vazamento e bombeio sequenciado.

#### definicao_funcao  (fatos: F1, F4, F9; conhecimento geral: False)

No ciclo operacional do FPSO, a exportação de óleo ocorre depois da separação primária dos fluidos produzidos, quando o petróleo já tratado fica armazenado nos tanques da própria unidade. Quando essa capacidade de armazenagem é atingida, o inventário precisa ser escoado para terminais, e isso pode ser feito por dutos submarinos ou por navios aliviadores. Na alternativa com aliviador, o navio-tanque ou shuttle tanker se desloca até a locação e recebe a carga por uma linha de mangueiras flexíveis. Por isso, a estação de alívio não é apenas um ponto de conexão de mangote: ela reúne tanto as facilidades de bombeio e transferência de óleo quanto as facilidades de amarração do navio aliviador.

#### principio_mecanismo  (fatos: F3, F5, F8, F9; conhecimento geral: False)

O arranjo do offloading em tandem combina dois subsistemas que operam de forma acoplada: a amarração do aliviador e a transferência hidráulica do óleo. O bombeio pode ser realizado por bombas de carga submersas instaladas em cada tanque ou por bombas localizadas na sala de bombas, na praça de máquinas, definindo o caminho interno até a estação de alívio. Para esse serviço, o projeto, a fabricação e a manutenção da estação devem atender plenamente às operações com mangote de transferência flutuante. Em arranjos mais antigos, a estação era basicamente uma tubulação rígida terminada em flange, à qual o mangote era conectado. Isso evidencia a evolução de um ponto de conexão simples para uma facilidade integrada de transferência e amarração adequada ao offloading em tandem.

#### variaveis_condicoes  (fatos: T8, F6, F7, T6; conhecimento geral: False)

Na operação com shuttle tanker dotado de posicionamento dinâmico, a sequência é condicionada pela posição relativa entre as embarcações e pelo estado da linha de mangueiras. A aproximação é iniciada com auxílio do sistema DP quando o aliviador está a cerca de 1.500 m do FPSO, e a passagem da messenger line ocorre quando ele chega a aproximadamente 80 m. Concluída a conexão, o navio permanece tipicamente entre 120 m e 155 m do FPSO para continuar a operação, e essa fase de conexão dura em torno de 6 h. Somente após a conexão é executado o teste de vazamento no hose string; em seguida, bombeia-se água do FPSO para o slop tank do aliviador e depois se inicia o bombeio de óleo para os tanques de carga. Ao fim do carregamento, cerca de 24 h depois, a água de slop é bombeada de volta ao FPSO. Nas etapas finais, o mangote é lavado e recolhido, os cabos de amarração são desconectados e o aliviador segue para o terminal de descarga.

#### problemas_diagnostico  (fatos: F6, F7, T5, T2, T6; conhecimento geral: False)

Dois grupos de anomalias são críticos no offloading: perda de integridade da linha de transferência e perda da posição segura entre FPSO e aliviador. Se o problema aparece já no teste de vazamento executado logo após a conexão, o indício primário recai sobre o hose string, e a transferência de óleo não deve ser iniciada. Se a conexão está estanque, mas surgem alertas associados à distância relativa entre as embarcações ou à tração no cabo hawser, o sintoma aponta para degradação do posicionamento, situação que pode levar à interrupção do bombeio e, em estados mais severos, à desconexão do mangote e do cabo. Essa distinção é operacionalmente relevante porque o primeiro caso é diagnosticado pela estanqueidade da linha, enquanto o segundo é diagnosticado pelo monitoramento da separação entre as embarcações e dos esforços de amarração. Durante toda a operação, o acompanhamento das estações serve justamente para detectar cedo qual desses mecanismos está em curso.

#### decisoes_criterios  (fatos: F1, F2, F3, F4; conhecimento geral: False)

A primeira decisão estrutural de exportação é entre duto submarino e navio aliviador. Quando a distância entre a produção offshore e a costa torna o uso de dutos economicamente ou tecnologicamente inviável, a solução passa a ser o escoamento por navios aliviadores que vão até a locação do FPSO. Uma vez adotado o offloading por aliviador, o arranjo de bombeio pode ser baseado em bombas submersas nos tanques ou em bombas instaladas na sala de bombas, e essa escolha organiza o caminho interno de transferência até as mangueiras flexíveis. Como a exportação só ocorre após o óleo ter sido armazenado a bordo, essa decisão de escoamento se integra diretamente à gestão da capacidade de armazenagem do FPSO.

#### valores_limites  (fatos: F11, T3, T6, T8; conhecimento geral: False)

Os valores reportados nas fontes são exemplos de arranjos específicos e mostram que dimensões e capacidades de offloading variam entre unidades. Em uma unidade investigada, o escoamento de condensado para navio aliviador usava mangotes flexíveis de 20 pol de diâmetro e 235 m de comprimento, com três bombas de carga, cada uma com capacidade de 5.000 m³/h. Na P-34, o material citado registra mangote flutuante conectado à popa com 385 m de comprimento, linhas de carga de 300 mm e linhas de descarga e transferência de óleo de 600 mm e 350 mm. Em uma descrição geral da operação aparecem ainda mangotes de 12 pol e 250 m, reforçando que o conjunto não é padronizado por um único valor. Para shuttle tanker com posicionamento dinâmico, a conexão total foi descrita com duração de cerca de 6 h, e a etapa de carregamento se estendeu até cerca de 24 h antes do bombeio de retorno da água de slop ao FPSO.

#### seguranca_riscos  (fatos: T2, F5, F6, T6; conhecimento geral: False)

O risco central do offloading é perder a posição segura entre o navio aliviador e o FPSO durante a transferência, com potencial de colisão ou de interrupção da operação. Em águas profundas e ultraprofundas, as fontes destacam que incidentes podem evoluir facilmente para acidentes com ameaça à vida dos trabalhadores e à continuidade operacional. Por isso, o teste de vazamento antes do bombeio, o monitoramento contínuo das estações durante toda a operação e a adequação de projeto, fabricação e manutenção da estação de alívio são barreiras essenciais. Em termos práticos, a segurança do offloading depende tanto da integridade do caminho hidráulico quanto da capacidade de manter amarração e posicionamento dentro de condições seguras.

**Outros campos:** `{"alvos": [{"nivel": "facil", "descricao": "Identificar em que ponto do ciclo operacional do FPSO a exportação é realizada e quais são os dois meios de escoamento citados nas fontes."}, {"nivel": "facil", "descricao": "Reconhecer que a estação de alívio reúne facilidades de bombeio e transferência de óleo e facilidades de amarração do navio aliviador."}, {"nivel": "media", "descricao": "Explicar por que o navio aliviador é adotado quando o uso de dutos submarinos se torna economicamente ou tecnologicamente inviável em grandes distâncias até a costa."}, {"nivel": "media", "descricao": "Distinguir os dois arranjos principais de bombeio de carga usados no offloading: bombas submersas em cada tanque e bombas localizadas na sala de bombas."}, {"nivel": "media", "descricao": "Descrever a sequência típica após a conexão: teste de vazamento, envio inicial de água ao slop tank, bombeio de óleo, retorno da água de slop ao FPSO e encerramento com lavagem e recolhimento do mangote."}, {"nivel": "dificil", "descricao": "Diagnosticar se uma interrupção do offloading decorre de problema de estanqueidade do hose string ou de perda do posicionamento relativo, usando a fase em que o sintoma aparece e as variáveis monitoradas."}, {"nivel": "dificil", "descricao": "Comparar os valores de diâmetro, comprimento de mangotes e capacidade de bombas entre fontes e reconhecer que se tratam de arranjos específicos de unidades ou casos, não de um único padrão universal."}], "correcoes": [], "lacunas": ["`

### Diagnóstico de esforço horizontal aparente por desalinhamento geométrico da amarra

**Resumo:** Em medições de esforço na ancoragem, uma componente horizontal negativa não implica, por si só, reversão física do carregamento transmitido. No caso descrito em modelo reduzido, esse sinal decorreu da geometria inicial da amarra na posição de 0° e da convenção de coordenadas adotada, o que orienta a leitura crítica de dados de ensaio ou monitoramento durante operações com carga e descarga.

#### definicao_funcao  (fatos: F1, T1; conhecimento geral: False)

Na interpretação de esforços transmitidos ao ponto de ancoragem, as componentes medidas precisam ser lidas como projeções vetoriais no sistema de coordenadas adotado, e não como evidência isolada do sentido físico do carregamento. No caso descrito, a componente horizontal apareceu negativa em algumas medições sem que isso fosse atribuído a um efeito próprio do carregamento, mas à posição inicial da amarra no ensaio. O ponto central, portanto, é distinguir entre uma anomalia de leitura aparente, produzida por geometria e convenção de eixos, e uma alteração real no modo como a carga está sendo transmitida à fundação. Essa distinção é relevante quando se avaliam resultados de carga e descarga e se tenta relacionar o sinal medido ao comportamento da linha de ancoragem.

#### principio_mecanismo  (fatos: F1, T1; conhecimento geral: False)

O mecanismo descrito é geométrico: na primeira posição de ensaio, definida como 0°, a amarra não estava totalmente vertical dentro do solo, e sua inclinação situava-se na porção negativa do sistema de coordenadas adotado. Por isso, a projeção da força transmitida no eixo horizontal podia assumir valor negativo, mesmo sem indicar um efeito físico anômalo do carregamento aplicado. O mesmo conjunto de resultados mostra que, à medida que o processo de carga e descarga ocorre para ângulos cada vez maiores em relação à direção vertical, a amplitude da carga que efetivamente chega ao ponto de ancoragem diminui, o que foi interpretado como absorção parcial de carga ao longo da amarra. Também foi observado que a variação do ângulo de incidência no topo da célula de carga aumenta quando a resistência do solo diminui, evidenciada pela elevação da componente horizontal.

#### problemas_diagnostico  (fatos: F1, T1; conhecimento geral: False)

Para diagnosticar uma componente horizontal negativa, o primeiro filtro é verificar se ela aparece associada à geometria inicial da linha, especialmente na primeira posição de ensaio, em vez de surgir como resposta coerente com a evolução do carregamento. No mesmo estudo, houve outros efeitos de natureza distinta: a componente vertical não retornou a zero após o descarregamento por causa de tensão residual ligada à reação do solo, e as curvas de carga e descarga não se sobrepuseram, caracterizando histerese. Esses sinais não devem ser confundidos com o efeito de sinal negativo causado pelo desalinhamento geométrico e pela convenção de coordenadas. Assim, uma leitura anômala deve ser separada entre três famílias de causa: projeção geométrica no eixo, memória mecânica solo-amarra após descarregamento e atenuação da carga ao longo da linha.

#### decisoes_criterios  (fatos: —; conhecimento geral: True)

Em dados de ensaio ou monitoramento, a interpretação deve começar pela reconstrução da geometria de referência da linha e pela conferência do sistema de eixos usado para registrar as componentes. Se o sinal horizontal estiver invertido apenas em uma condição inicial ou em uma faixa angular específica, a hipótese de desalinhamento geométrico e convenção de sinais deve ser testada antes de concluir que houve mudança física no sentido do esforço transmitido. A leitura também ganha robustez quando a componente horizontal é analisada junto com a vertical remanescente após descarregamento e com a presença de histerese, porque esses fenômenos apontam mecanismos diferentes. Em operações como offloading, esse critério evita atribuir ao movimento de carga um efeito que pode ser apenas artefato de referência geométrica ou de processamento do dado.

**Outros campos:** `{"alvos": [{"nivel": "facil", "descricao": "Reconhecer que uma componente horizontal negativa pode resultar da geometria inicial da amarra e da convenção de coordenadas, sem representar inversão física do carregamento."}, {"nivel": "facil", "descricao": "Identificar a condição específica do caso em que o efeito foi observado: primeira posição de ensaio a 0°, com a amarra não totalmente vertical dentro do solo."}, {"nivel": "media", "descricao": "Explicar por que o aumento do ângulo em relação à vertical reduz a amplitude da carga que chega ao ponto de ancoragem, com absorção parcial ao longo da amarra."}, {"nivel": "media", "descricao": "Distinguir componente horizontal negativa por projeção geométrica de componente vertical residual após descarregamento, associada à reação do solo."}, {"nivel": "dificil", "descricao": "Diagnosticar um conjunto de leituras contendo sinal horizontal negativo, vertical remanescente após descarga e histerese, separando o que decorre de geometria e sistema de eixos do que decorre da interação solo-amarra."}], "correcoes": [], "lacunas": ["O material disponível está baseado em estudo de modelo reduzido de linha de ancoragem e não fornece valores quantitativos, critérios de aceitação, algoritmo de transformação de coordenadas nem exemplo instrumental de operação real de offloading em FPSO/FSO; por isso, a nota sustenta o diagnóstico conceitual e a interpretação qualitativa, mas não define limites operacionais de campo."]}`

### Arquitetura interna de transferência de carga entre tanques e equipamentos associados

**Resumo:** No caso analisado do FPSO Cidade de São Mateus, a arquitetura interna de transferência de carga não permitia encaminhar livremente a produção para qualquer tanque: o recebimento inicial era restrito aos tanques 2C e 3C, e a redistribuição aos demais dependia dos headers de fundo. Suspeitas de passagem em válvulas e acoplamentos Dresser provocavam migração indesejada entre tanques, e a indisponibilidade de 2C e 3C para manutenção levou à proposição de uma rota alternativa para o tanque 6C, com apoio de bombas auxiliares e da bomba de stripping.

#### definicao_funcao  (fatos: F6, F7, F2; conhecimento geral: False)

No escopo analisado, o sistema interno de transferência de carga compreende a linha de chegada da produção aos tanques, os dois headers de fundo — central header e starboard header — e os tanques de armazenamento 2C, 3C, 4C, 5C e 6C. Esse escopo não inclui o sistema de lastro nem o sistema de gás. Pela arquitetura de projeto, os líquidos produzidos destinados ao armazenamento só podiam ser encaminhados inicialmente aos tanques 2C e 3C. O envio para os demais tanques ocorria depois, por meio dos headers no fundo dos tanques, o que mostra que a distribuição interna da carga dependia de rotas de redistribuição e não de acesso direto da produção a todos os tanques.

#### principio_mecanismo  (fatos: —; conhecimento geral: True)

Em arquiteturas desse tipo, a run down line funciona como ponto de alimentação do sistema, enquanto os headers de fundo operam como troncos de redistribuição entre tanques e para preparação da carga para etapas seguintes do manejo operacional. As válvulas determinam quais trechos permanecem isolados e quais passam a se comunicar, de modo que a flexibilidade real de roteamento depende do arranjo hidráulico e dos pontos de isolamento disponíveis. Quando a rota normal não atende à condição operacional, uma linha alternativa só é útil se estabelecer uma nova continuidade hidráulica entre origem e destino, com segregação controlada dos demais volumes armazenados. A bomba de stripping, em termos funcionais, costuma complementar as rotas principais ao remover volumes remanescentes ou de baixa sucção, em vez de substituir a função estrutural dos caminhos principais de transferência.

#### variaveis_condicoes  (fatos: F2, F4, F5; conhecimento geral: False)

A disponibilidade dos tanques 2C e 3C era uma condição decisiva, porque o projeto só permitia que a produção destinada ao armazenamento fosse encaminhada inicialmente a esses dois tanques. Quando se tornou necessário entrar em 2C e 3C para manutenção, a limitação de roteamento deixou de ser apenas uma característica de projeto e passou a exigir uma mudança temporária na arquitetura de transferência. A solução proposta foi destinar a produção ao tanque 6C usando uma linha de secagem de gás inerte que estava fora de uso no deck principal, além de outras adaptações. Isso evidencia que a continuidade da operação dependia não só do estado dos tanques, mas também da existência de uma rota alternativa fisicamente conectável a outro tanque de armazenamento.

#### problemas_diagnostico  (fatos: F1, F2; conhecimento geral: False)

No caso citado, os tanques 2C, 3C, 4C e 5C apresentavam suspeita de problemas de passagem em válvulas e em acoplamentos Dresser, e o efeito associado era a migração de conteúdo entre os tanques. O sintoma relevante, portanto, era a comunicação indesejada entre inventários que deveriam permanecer segregados. Como o projeto previa redistribuição de carga aos demais tanques por meio dos headers de fundo, essa migração interferia na distribuição esperada quando se pretendia remanejar conteúdo internamente. Para diagnóstico, o relatório indica que a investigação não deveria se limitar às válvulas, porque os acoplamentos Dresser do trecho também eram suspeitos e foram vinculados ao mesmo efeito observado.

#### decisoes_criterios  (fatos: F2, F4, F5, T1, F8, F3; conhecimento geral: False)

Na mudança temporária proposta, a decisão foi criar uma rota alternativa para o tanque 6C, porque os tanques 2C e 3C precisavam ser liberados para manutenção e não podiam continuar como único ponto inicial de recebimento da produção destinada ao armazenamento. O planejamento também previa usar a linha adaptada para transferir ao tanque 6C o conteúdo remanescente, após offloading, dos tanques 2C a 5C, com auxílio de bombas submersíveis portáteis e da bomba de stripping. Nesse arranjo, a bomba de stripping era um equipamento associado de apoio à transferência interna: tratava-se de uma bomba alternativa de duplo efeito, acionada a vapor, instalada no fundo da casa de bombas. Sua proteção incluía uma válvula de alívio fornecida pelo fabricante, interligada à câmara de ar e com descarga retornando à sucção da bomba, compondo a proteção do conjunto durante a operação.

**Outros campos:** `{"alvos": [{"nivel": "facil", "descricao": "Reconhecer o escopo do sistema de transferência de carga analisado e identificar seus principais componentes: run down line, central header, starboard header e tanques 2C a 6C."}, {"nivel": "media", "descricao": "Explicar a limitação de roteamento do projeto, na qual a produção destinada ao armazenamento só podia entrar inicialmente nos tanques 2C e 3C."}, {"nivel": "media", "descricao": "Relacionar o uso dos headers de fundo à redistribuição posterior de carga para os demais tanques de armazenamento."}, {"nivel": "media", "descricao": "Associar suspeita de passagem em válvulas e acoplamentos Dresser nos tanques 2C a 5C ao sintoma de migração indesejada de conteúdo entre tanques."}, {"nivel": "media", "descricao": "Descrever por que a necessidade de entrada para manutenção nos tanques 2C e 3C levou à proposição de uma linha alternativa para o tanque 6C."}, {"nivel": "dificil", "descricao": "Integrar restrição de recebimento inicial, indisponibilidade de 2C e 3C, migração entre tanques e uso de linha adaptada com bombas auxiliares para analisar como preparar a transferência interna e o remanejamento de remanescentes após offloading."}, {"nivel": "dificil", "descricao": "Identificar a função operacional da bomba de stripping no arranjo temporário e reconhecer que sua válvula de alívio recircula para a sucção como parte da proteção do conjunto."}], "correcoes": [{"original": "\"escape valve\"", "corrigido": "válvula de alívio de pressã`

### Exemplos de revisão automática

- decisão **corrigir**, avaliação {'correcao_tecnica': 5, 'suporte': 5, 'pertinencia': 5, 'riqueza': 4}, problemas: [{'secao': 0, 'tipo': 'sem_suporte', 'descricao': 'A redação factual introduz uma explicação específica sobre alteração do espaço de vapor do tanque durante carregamento e descarga, ponto que não aparece explicitamente nos fatos citados.'}, {'secao': 3, 'tipo': 'sem_suporte', 'descricao': 'A seção faz uma integração válida entre offloading e atmosfera do tanque, mas parte da formulação original extrapola o texto-fonte ao caracterizar essa exigência como barreira da exportação sem amarração textual direta.'}]
  - A nota é pertinente, tecnicamente correta e rica, mas havia pequenas extrapolações em seções marcadas como não baseadas em conhecimento geral. A correção preserva o conteúdo central integralmente sustentado pelos fatos e pelo trecho fornecido.
- decisão **corrigir**, avaliação {'correcao_tecnica': 5, 'suporte': 5, 'pertinencia': 5, 'riqueza': 5}, problemas: [{'secao': 0, 'tipo': 'incorreto', 'descricao': "A oposição entre turret e spread mooring foi formulada como se a ancoragem distribuída deixasse a unidade 'rigidamente orientada'. Isso não é sustentado pelas fontes citadas e simplifica em excesso o comportamento operacional de arranjos distribuídos."}, {'secao': 3, 'tipo': 'sem_suporte', 'descricao': 'A afirmação de que uma fonte apresenta o turret como alternativa dentro da família SPM, ao lado de yoke, CALM e SALM, não estava integralmente sustentada pelos fatos citados na seção. Era necessário ajustar o texto ou citar trecho de origem explícito.'}]
  - A nota é pertinente, tecnicamente boa e rica, mas exigia ajustes pontuais de suporte e formulação para evitar simplificação excessiva sobre spread mooring e para rastrear corretamente a relação entre SPM, turret e outros arranjos citados nas fontes.
- decisão **corrigir**, avaliação {'correcao_tecnica': 5, 'suporte': 5, 'pertinencia': 5, 'riqueza': 5}, problemas: [{'secao': 3, 'tipo': 'sem_suporte', 'descricao': 'A seção usa conteúdo do trecho T3 além do fato F3, incluindo a exigência de metodologia/programa de inspeção e a abrangência de propulsão/thrusters, mas não cita T3 no campo fatos.'}, {'secao': 4, 'tipo': 'sem_suporte', 'descricao': 'A seção atribui à HSE barreiras e requisitos que constam em T3, mas o campo fatos cita apenas F3 e F4. Além disso, a abertura da seção estava mais ampla que o suporte explícito das fontes.'}]
  - A nota é pertinente, tecnicamente correta e rica, mas havia uso de conteúdo de T3 sem rastreabilidade completa nos campos de fatos e uma formulação final que podia ser mais aderente ao suporte documental. Corrigida, a nota fica integralmente sustentada.