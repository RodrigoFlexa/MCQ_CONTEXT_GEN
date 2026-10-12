# Segmentação IT/OT em FPSOs: segregação segura entre redes corporativas e redes de automação

## 1. Objetivo técnico da segmentação IT/OT

Em FPSOs, a segmentação entre ambientes de Tecnologia da Informação (IT) e Tecnologia Operacional (OT) tem como finalidade principal limitar a propagação de falhas, reduzir exposição indevida dos sistemas de controle e preservar a disponibilidade operacional. Nas fontes disponíveis, a motivação prática aparece em dois eixos complementares:

1. **o ambiente OT é composto por camadas com requisitos de controle, supervisão e, em certos casos, intertravamento e segurança que não podem falhar ou sofrer degradação arbitrária**; e
2. **a integração com camadas corporativas, sistemas de gestão e serviços de análise aumenta a utilidade do dado, mas também amplia superfícies de interconexão**.

A segregação, portanto, não deve ser entendida como isolamento absoluto de toda troca de dados, mas como **controle rigoroso dos pontos de interligação** entre redes de processo, supervisão, bancos de dados/historiadores e redes corporativas. Nas fontes, isso é materializado por barreiras entre camadas, uso de firewalls, gateways, DMZ e limitação explícita dos protocolos autorizados a atravessar as fronteiras de rede.

Do ponto de vista operacional, a segmentação adequada também atua como medida de confiabilidade: o caso reportado em instalação offshore mostra redução de shutdowns não planejados e aumento de confiabilidade após adoção de arquitetura em profundidade com isolamento entre automação e negócio.

**Fontes da seção:** `petroles-004c2afadba7ea17c7dd7908:pNone:533075.0-533112.0`, `petroles-4ee4bce16acf674505c8912d:pNone:2443605.0-2443665.0`, `regis-ef515ebe1d05111fa1433c40:pNone:818.0-972.0`

## 2. Arquitetura funcional: onde termina IT e onde começa OT

As fontes descrevem a automação industrial como uma arquitetura em níveis/camadas. Embora os textos venham de contextos industriais gerais, eles são úteis para estruturar a segregação em FPSO.

### 2.1 Pirâmide de automação

Um modelo apresentado organiza a automação em cinco níveis:

- **Nível 1 – dispositivos de campo:** sensores e atuadores;
- **Nível 2 – controle:** CLP, RTU, SDCD e equipamentos equivalentes;
- **Nível 3 – supervisão:** SCADA, IHM, estações de trabalho e concentração de dados do processo;
- **Nível 4 – gerenciamento de planta:** planejamento e programação da operação;
- **Nível 5 – gerenciamento corporativo:** administração e sistemas de negócio.

Esse modelo ajuda a delimitar a fronteira IT/OT: em termos práticos, os níveis 1 a 3 pertencem ao núcleo operacional do processo, enquanto os níveis 4 e 5 representam a camada de gestão/negócio. A segmentação não precisa ser binária; ela pode exigir múltiplas fronteiras entre níveis com criticidades diferentes.

### 2.2 Camadas técnicas relevantes para segmentação

Outro texto detalha a automação em camadas mais próximas da infraestrutura real:

- **instrumentação e atuadores**;
- **remotas de I/O**;
- **rede de automação de campo**;
- **CLPs**;
- **rede de controle e supervisão de processo (CSP)**;
- **supervisório/SCADA**;
- **software**;
- **banco de dados do SCADA**;
- **historiador**;
- **rede de automação industrial corporativa (RAI)**;
- **estações de trabalho/IHM**.

Para fins de segmentação IT/OT, esse detalhamento é especialmente útil porque mostra que **nem toda rede “industrial” possui a mesma criticidade**. Exemplos:

- a **rede de campo** conecta instrumentos, sensores, remotas e CLPs e pode incluir intertravamentos; o texto afirma que essas redes “não podem falhar” e, por vezes, são determinísticas;
- a **rede CSP** interliga PLCs e supervisórios SCADA e é normalmente redundante, mesmo quando baseada em Ethernet;
- o **banco de dados do SCADA que faz interface direta com o processo não deve ser acessado diretamente por razões de segurança**;
- um **historiador** pode servir como camada intermediária para disponibilizar variáveis à engenharia e à gestão;
- a **RAI** é uma rede corporativa industrial de uso restrito da engenharia e operação, distinta da rede comum de informática da empresa e normalmente separada desta por várias camadas de proteção.

A consequência prática é que a segmentação IT/OT em FPSO não deve ser projetada apenas entre “escritório” e “planta”, mas também entre:

- campo e controle;
- controle e supervisão;
- supervisão e bancos de dados/historiadores;
- rede industrial corporativa e rede corporativa comum.

**Fontes da seção:** `regis-ef515ebe1d05111fa1433c40:pNone:818.0-972.0`, `petroles-4ee4bce16acf674505c8912d:pNone:2443605.0-2443665.0`

## 3. Mecanismos de segregação descritos nas fontes

### 3.1 Defesa em profundidade

O caso de integração de sistemas em plataforma offshore descreve explicitamente a adoção de uma arquitetura de **Defense in Depth (defesa em profundidade)**. No material, isso significa isolar as camadas de negócio e de processo por meio de barreiras como **firewalls** e **gateways**, de forma a minimizar o tráfego de dados entre elas.

Tecnicamente, a defesa em profundidade apresentada nas fontes não depende de um único equipamento, mas de uma composição de controles de rede em diferentes fronteiras. Isso é consistente com ambientes em que coexistem:

- equipamentos próprios do operador;
- equipamentos de terceiros;
- SCADA;
- CLPs;
- sensores e equipamentos inteligentes;
- sistemas submarinos e medidores virtuais.

Quanto maior a heterogeneidade, maior a necessidade de múltiplas barreiras e de definição explícita dos caminhos de tráfego permitidos.

### 3.2 Firewalls perimetrais

O texto relata o uso de **um perímetro de firewalls** para proteção dos sistemas de operação. O conceito importante é que a rede operacional não deve ficar exposta diretamente à internet nem à rede de negócios. O firewall perimetral atua como fronteira de contenção entre domínios com perfis de risco distintos.

### 3.3 DMZ entre negócio e controle

A fonte cita o uso de **DMZ** para proteger o sistema de controle de processos da internet e da rede de negócios. Em termos funcionais, a DMZ representa uma zona intermediária para concentrar trocas necessárias sem permitir conexão direta irrestrita entre a camada corporativa e a camada de controle.

Pelo conjunto das fontes, a DMZ é coerente especialmente para hospedar ou intermediar serviços de consulta e integração que não devem tocar diretamente o banco do SCADA ou os CLPs.

### 3.4 Chaves gerenciáveis e lógica de segregação

A separação entre camadas de automação e negócio também foi feita com **chaves gerenciáveis** e **lógicas de segregação de rede**. Isso indica que a segmentação não depende só do firewall de borda; ela também precisa ser implementada no interior da topologia de switching, com separação lógica apropriada entre domínios de comunicação.

### 3.5 Restrição de protocolos e estratégia de troca de dados

No caso relatado, **apenas os protocolos necessários eram autorizados a atravessar as fronteiras**, com base em uma estratégia de troca de dados. Esse é o elemento mais diretamente associado ao princípio de privilégio mínimo aplicado à rede: não se libera “acesso entre redes” de forma genérica; liberam-se apenas **fluxos, sentidos e protocolos estritamente necessários** para a função operacional definida.

Para FPSOs, isso é particularmente relevante quando o SCADA interconecta CLPs, equipamentos inteligentes, sistemas submarinos e ferramentas como OPC. Quanto mais protocolos e serviços coexistem, maior a necessidade de controle explícito do que atravessa as fronteiras IT/OT.

### 3.6 Proteção próxima aos ativos de processo

A fonte menciona ainda a proteção de CLPs e diversos equipamentos de processo com sistema Tofino acoplado ao supervisório SCADA em módulo específico de firewall. Independentemente da solução comercial citada, o conceito técnico útil é o de **proteção segmentada próxima aos ativos ou às células de processo**, e não apenas na borda externa da rede.

**Fontes da seção:** `petroles-004c2afadba7ea17c7dd7908:pNone:533075.0-533112.0`

## 4. Controle de tráfego como requisito de integridade e disponibilidade

As fontes não tratam segmentação apenas como controle de acesso; elas a relacionam diretamente com **controle de tráfego** e **estabilidade operacional**.

No caso descrito, havia **elevado volume de tráfego** na rede devido ao uso de comunicação **UDP broadcast/multicast**, e esse tráfego precisava ser limitado. Esse ponto é tecnicamente importante em OT por três razões:

1. **broadcasts e multicasts excessivos podem consumir capacidade da rede e degradar a previsibilidade do tráfego útil**;
2. **em redes onde coexistem supervisão, controle e integração de terceiros, a propagação ampla de tráfego pode afetar componentes que não precisam receber aquela informação**;
3. **a segmentação ajuda a conter domínio de falha e domínio de inundação de tráfego**, evitando que fenômenos locais se espalhem para camadas adjacentes.

Em FPSOs, isso se conecta diretamente à necessidade de preservar a disponibilidade de redes de controle e supervisão. Não basta impedir acesso indevido; é igualmente necessário impedir que **padrões de comunicação mal distribuídos**, ainda que originados por sistemas legítimos, prejudiquem a operação.

As fontes também mostram que a rede de automação de campo pode suportar intertravamentos e pode ser determinística. Assim, decisões de segmentação devem considerar não apenas segurança lógica, mas também **comportamento temporal da rede**.

**Fontes da seção:** `petroles-004c2afadba7ea17c7dd7908:pNone:533075.0-533112.0`, `petroles-4ee4bce16acf674505c8912d:pNone:2443605.0-2443665.0`

## 5. Segmentação e requisitos de tempo real

Um dos riscos de uma segmentação mal concebida é tratar todas as comunicações como equivalentes, ignorando requisitos temporais distintos. As fontes sobre sistemas de tempo real ajudam a qualificar esse ponto.

O material afirma que a correção de um sistema em tempo real depende de dois critérios:

- **corretude lógica**: produzir a saída adequada em função das entradas;
- **corretude temporal**: produzir essa saída antes do prazo-limite.

Também são descritas classes de sistemas:

- **tempo real crítico (hard real-time)**: perda de prazo é falha crítica;
- **tempo real firme (firm real-time)**: atrasos esporádicos degradam o serviço, e resultados fora do prazo tendem a perder utilidade;
- **tempo real flexível/brando (soft real-time)**: atrasos esporádicos podem ser tolerados com menor impacto.

Aplicando isso à segmentação IT/OT em FPSO:

- **redes de campo, intertravamentos e funções de controle próximas ao processo não podem receber o mesmo tratamento de latência e inspeção que serviços administrativos ou de consulta histórica**;
- **mecanismos de filtragem e intermediação entre IT e OT precisam ser compatíveis com o comportamento temporal do serviço protegido**;
- **o aumento de barreiras é desejável do ponto de vista de contenção, mas não pode introduzir atrasos, perdas ou variações incompatíveis com funções críticas**.

Portanto, a boa segmentação é um equilíbrio entre **isolamento suficiente** e **preservação do desempenho temporal necessário**. Em redes industriais, segurança de rede que compromete a capacidade de cumprir prazos operacionais pode, ela própria, transformar-se em causa de indisponibilidade.

**Fontes da seção:** `petroles-004c2afadba7ea17c7dd7908:pNone:784628.0-784662.0`, `petroles-4ee4bce16acf674505c8912d:pNone:2443605.0-2443665.0`

## 6. Pontos de interconexão que exigem tratamento especial

### 6.1 SCADA como nó de convergência

As fontes caracterizam o SCADA como elemento que:

- faz interface com equipamentos de campo por meio dos PLCs;
- armazena variáveis e eventos em bancos de dados internos;
- envia comandos para a planta;
- gera alarmes, históricos, relatórios e informação gerencial.

Isso torna o SCADA um ponto de alta criticidade para segmentação: ele faz a ponte entre o mundo do processo e os consumidores de informação em níveis superiores. Em termos de arquitetura, isso significa que o SCADA não deve ser tratado como simples servidor corporativo, nem exposto a acessos amplos por conveniência operacional.

### 6.2 Banco de dados do SCADA e historiador

Um ponto objetivo das fontes é que **o banco de dados do SCADA que faz interface direta com o processo não deve ser acessado diretamente por razões de segurança**. Em contraste, há um **segundo nível de banco de dados, o historiador**, destinado a armazenar variáveis de campo e disponibilizá-las para camadas corporativas superiores.

Esse arranjo é tecnicamente importante para segmentação IT/OT porque cria uma separação entre:

- **dado operacional vivo e diretamente conectado ao processo**, e
- **dado disponibilizado para engenharia, análise e gestão**.

Na prática, o historiador funciona como fronteira informacional mais adequada para consumo externo do que o acesso direto ao núcleo de supervisão/controle.

### 6.3 Rede industrial corporativa distinta da rede corporativa comum

A RAI é descrita como rede corporativa de uso restrito da engenharia e operação, distinta da rede comum de informática da empresa e separada dela por várias camadas de proteção. Esse ponto é central para FPSOs porque evita dois extremos indesejáveis:

- conectar a automação diretamente à rede corporativa geral; ou
- impedir qualquer circulação de informação útil à operação e à gestão.

A solução intermediária indicada pelas fontes é uma **rede industrial corporativa própria**, ainda separada da TI comum por proteções adicionais.

**Fontes da seção:** `regis-ef515ebe1d05111fa1433c40:pNone:818.0-972.0`, `petroles-4ee4bce16acf674505c8912d:pNone:2443605.0-2443665.0`

## 7. Redundância, disponibilidade e efeito da camada mais fraca

A segmentação segura não é apenas uma questão de onde colocar barreiras; ela depende da robustez conjunta das camadas envolvidas. As fontes destacam que:

- a **rede CSP** costuma ser **redundante**, mesmo quando baseada em Ethernet;
- falhas em uma camada podem inutilizar todo o sistema, ainda que outra camada esteja íntegra;
- não adianta ter um PLC altamente disponível se a rede que transporta os comandos não tem a mesma robustez.

Essa visão é especialmente pertinente em FPSO, onde a continuidade operacional depende do funcionamento coordenado de instrumentação, redes de campo, CLPs, SCADA, estações de operação e enlaces entre redes. Assim, a segmentação deve ser avaliada não só por sua eficácia de isolamento, mas também por seu impacto sobre:

- continuidade do comando e da supervisão;
- tolerância a falhas de comunicação;
- manutenção do serviço em arquiteturas redundantes;
- capacidade de conter falhas sem indisponibilizar funções que precisam permanecer operacionais.

Em outras palavras, uma arquitetura segmentada é tecnicamente boa quando **reduz a superfície de propagação de falhas sem se tornar o elo que inviabiliza a operação**.

**Fontes da seção:** `petroles-4ee4bce16acf674505c8912d:pNone:2443605.0-2443665.0`

## 8. Lições práticas extraídas das fontes para FPSOs

Com base exclusivamente no material fornecido, as seguintes lições são tecnicamente sustentáveis para segmentação IT/OT:

1. **Segregue negócio e processo por camadas e não apenas por endereçamento lógico simples.** As fontes enfatizam barreiras explícitas entre automação e negócio.
2. **Use múltiplos mecanismos complementares.** Firewalls perimetrais, gateways, chaves gerenciáveis, lógica de segregação e DMZ aparecem de forma combinada.
3. **Autorize somente o tráfego necessário.** O caso reportado destaca liberação apenas dos protocolos necessários, segundo estratégia de troca de dados.
4. **Controle domínios de broadcast/multicast.** Tráfego excessivo pode comprometer estabilidade e disponibilidade.
5. **Evite acesso direto do ambiente corporativo ao núcleo de controle/supervisão.** O banco de dados do SCADA diretamente ligado ao processo não deve ser acessado diretamente; o historiador é a interface mais apropriada para disponibilização superior.
6. **Considere criticidade temporal ao segmentar.** Redes de campo, intertravamentos e controle exigem atenção a determinismo, latência e cumprimento de prazos.
7. **Projete a segmentação junto com a arquitetura de disponibilidade.** Redundância de rede de supervisão/controle e robustez ponta a ponta são partes da integridade do arranjo.
8. **Não trate integração com terceiros e sistemas submarinos como mera extensão da TI.** A convergência de equipamentos próprios, terceiros, SCADA, CLPs e comunicação OPC exige delimitação clara dos fluxos entre domínios.

No caso citado, a aplicação dessas medidas foi associada a menor número de shutdowns não planejados, maior confiabilidade e maior produtividade da instalação. Embora o texto não forneça todos os detalhes quantitativos, ele reforça o vínculo entre segmentação adequada e desempenho operacional.

**Fontes da seção:** `petroles-004c2afadba7ea17c7dd7908:pNone:533075.0-533112.0`, `petroles-4ee4bce16acf674505c8912d:pNone:2443605.0-2443665.0`, `regis-ef515ebe1d05111fa1433c40:pNone:818.0-972.0`, `petroles-004c2afadba7ea17c7dd7908:pNone:784628.0-784662.0`

## 9. Síntese

Segmentação IT/OT, nas fontes analisadas, é uma disciplina de arquitetura operacional voltada a **conter tráfego e acessos**, **proteger o processo das redes corporativas e externas**, **preservar requisitos temporais das funções industriais** e **manter a disponibilidade global da automação**. Em FPSOs, isso se traduz em separar adequadamente campo, controle, supervisão, historiadores, rede industrial corporativa e rede corporativa comum, com barreiras múltiplas e troca de dados estritamente necessária.

A principal consequência técnica de uma boa segmentação não é apenas “mais segurança” em sentido abstrato, mas sim **menor propagação de falhas, menor exposição indevida do controle, maior estabilidade da comunicação e melhor continuidade operacional**.

**Fontes da seção:** `petroles-004c2afadba7ea17c7dd7908:pNone:533075.0-533112.0`, `petroles-4ee4bce16acf674505c8912d:pNone:2443605.0-2443665.0`, `regis-ef515ebe1d05111fa1433c40:pNone:818.0-972.0`, `petroles-004c2afadba7ea17c7dd7908:pNone:784628.0-784662.0`