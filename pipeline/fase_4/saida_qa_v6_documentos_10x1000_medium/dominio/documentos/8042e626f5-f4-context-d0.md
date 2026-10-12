# Ferramentas, instrumentos e içamento no apoio técnico à manutenção em FPSO

## 1. Objetivo da faceta
O controle de ferramentas, instrumentos de teste/calibração e recursos de içamento em um FPSO deve assegurar, ao mesmo tempo, **disponibilidade operacional**, **confiabilidade do resultado técnico** e **segurança da execução**. Na prática, isso significa garantir que o recurso certo esteja disponível no momento do serviço, em condição física adequada, com identificação rastreável e, quando aplicável, com inspeção, calibração ou certificação válidas.

Nesta faceta, o foco recai sobre os recursos que suportam manutenção, inspeção, diagnóstico, teste, ajuste e retorno ao serviço de componentes e sistemas. O material de origem disponível trata principalmente de oficinas de instrumentação, planejamento de paradas, cadastro/planejamento em sistemas e requisitos de inspeção e rastreabilidade. A aplicação específica a FPSO exige adaptação de contexto.  
**Fontes:** `petroles-004c2afadba7ea17c7dd7908:pNone:981095.0-981149.0`, `regis-d98eb152398d79661d91c35f:pNone:15.60-38.60`, `regis-7493a0b7af9688fbb59924e0:pNone:4062.0-4278.0`, `anp-912dd4dd5be0ece1d8e4973b:p27-32:23.0-9.0`, `anp-912dd4dd5be0ece1d8e4973b:p30-33:17.0-35.0`

## 2. Classes de recursos a controlar
Com base no material, os **recursos auxiliares para manutenção de instrumentos** abrangem:

- prédio ou locais de oficina;
- equipamentos e dispositivos de teste e calibração;
- ferramentas;
- máquinas operatrizes;
- bancadas de serviço;
- meios de movimentação interna, como **talha móvel** para deslocamento entre bancadas e dispositivos fixos.

Para fins de gestão em FPSO, esses recursos podem ser organizados em três grupos funcionais:

### 2.1 Ferramentas de execução
Incluem maletas, ferramentas manuais, acessórios de bancada e itens de uso recorrente nas oficinas e no campo.

### 2.2 Instrumentos e dispositivos de teste
Incluem malas de calibração, multímetros, dispositivos fixos de teste/calibração, fontes de pressão, dispositivos de calibração de manômetros e termômetros e outros equipamentos eletrônicos de apoio ao diagnóstico.

### 2.3 Recursos de içamento e movimentação interna
Incluem talhas móveis e dispositivos usados para movimentar válvulas de controle, instrumentos de maior porte e peças entre bancadas e pontos de serviço.

Essa classificação é útil porque o tipo de controle requerido não é idêntico: ferramentas demandam principalmente inspeção de condição e disponibilidade; instrumentos de teste demandam também controle metrológico; recursos de içamento demandam evidência de condição segura e aptidão ao uso.  
**Fontes:** `petroles-004c2afadba7ea17c7dd7908:pNone:981095.0-981149.0`, `regis-d98eb152398d79661d91c35f:pNone:15.60-38.60`

## 3. Infraestrutura e layout: impacto direto na disponibilidade e na confiabilidade
O material destaca que a oficina não é apenas um espaço físico; ela influencia diretamente a qualidade da manutenção e a estabilidade da calibração.

### 3.1 Localização da oficina e risco de descalibração
É conveniente que as oficinas ou pontos de apoio fiquem próximos às áreas com maior concentração de serviços. A justificativa principal é reduzir:

- dano no transporte;
- descalibração durante deslocamentos longos;
- tempo improdutivo de ida e volta do instrumento;
- necessidade de retirar o equipamento do processo por períodos maiores.

O texto aponta que o transporte em longos percursos é, estatisticamente, um agente relevante de problemas de calibração. Por isso, uma solução prática é combinar:

- **oficina central** para serviços gerais de manutenção e calibração; e
- **pontos locais estrategicamente preparados**, com recursos de teste/calibração de uso mais frequente, inclusive em campo ou em salas de controle quando viável.

Em um FPSO, essa lógica favorece a redução do tempo de indisponibilidade e do retrabalho pós-instalação por perda de ajuste durante o manuseio.  
**Fonte:** `petroles-004c2afadba7ea17c7dd7908:pNone:981095.0-981149.0`

### 3.2 Layout funcional mínimo da oficina de instrumentação
O material descreve como conveniente a separação em áreas distintas:

1. **Área para válvulas de controle e instrumentos de maior porte**  
   - bancadas especiais, preferencialmente metálicas;
   - suportes especiais para válvulas e instrumentos;
   - dispositivos de serviço e calibração;
   - **talha móvel** para deslocamento de equipamentos e peças;
   - possível localização de esmeris e politrizes.

2. **Área geral de manutenção de instrumentos**  
   - bancadas com utilidades diretamente disponíveis;
   - tomadas elétricas, ar comprimido, morsas etc.;
   - localização de máquinas operatrizes, como furadeira de mesa;
   - dispositivos de calibração de manômetros e termômetros;
   - possibilidade de bancadas específicas para rotinas contínuas, como preventiva.

3. **Sala de calibração**  
   - localização dos dispositivos fixos de teste e calibração;
   - conveniência de ar-condicionado pela natureza do serviço;
   - possibilidade de bancadas especiais para instrumentos mais sensíveis;
   - uso compartilhado de recursos comuns, como fontes de pressão, para instrumentos eletrônicos e pneumáticos.

4. **Sala de serviços em instrumentos eletrônicos e analisadores**  
   - ar-condicionado;
   - equipamentos eletrônicos de teste;
   - ferramentas e recursos para circuitos eletrônicos;
   - dispositivos especiais de testes em analisadores.

Também é importante prever locais adequados para **guarda de peças, sucata aproveitável, armários e prateleiras**, evitando acúmulo sobre bancadas. Isso afeta diretamente organização, preservação e disponibilidade dos recursos.  
**Fonte:** `petroles-004c2afadba7ea17c7dd7908:pNone:981095.0-981149.0`

## 4. Controle administrativo e físico de ferramentas e instrumentos
A disponibilidade de um recurso depende de ele estar **cadastrado, identificado, localizado e vinculado a um responsável**.

### 4.1 Cadastro e identificação
O material de gestão de manutenção mostra um fluxo de cadastro em ERP/SAP com campos obrigatórios como:

- centro de custo;
- centro técnico responsável;
- local de instalação;
- identificação/tag do equipamento.

Após o cadastro, o equipamento é identificado por etiqueta, e há inspeções periódicas de tagueamento para verificação de inconsistências. Embora o texto trate de equipamentos fabris, a lógica é diretamente aplicável ao controle de recursos de manutenção, especialmente os críticos ou compartilhados.

Para ferramentas e instrumentos de teste em FPSO, uma sistemática coerente tende a incluir, no mínimo:

- código único do item;
- descrição padronizada;
- responsável técnico ou área custodiante;
- localização física usual;
- status de uso (disponível, reservado, em calibração, em reparo, segregado);
- vínculo a certificado aplicável, quando houver;
- histórico de movimentação e intervenções.

### 4.2 Listas de tarefas e vínculo com a programação
O material também destaca a importância de listas de tarefas associadas aos planos de manutenção e do uso do sistema para programar serviços. Para os recursos de apoio, isso significa que a necessidade de instrumentos de teste, ferramentas especiais e apoio de oficina deve aparecer na fase de planejamento, e não somente na execução.

Sem esse vínculo, a organização cai em programação de curto prazo e corre maior risco de:

- indisponibilidade na hora da intervenção;
- uso de recurso inadequado;
- aumento de espera a bordo;
- compras emergenciais e logística reativa.

### 4.3 Inspeções periódicas de identificação e consistência cadastral
A inspeção periódica de tagueamento citada no material é especialmente útil para evitar:

- item físico sem registro no sistema;
- item registrado, porém não localizável;
- recurso em uso com certificado vencido por falha de associação documental;
- duplicidade de cadastro e distorção da disponibilidade real.

**Fontes:** `regis-7493a0b7af9688fbb59924e0:pNone:4062.0-4278.0`

## 5. Inspeção, calibração, certificação e rastreabilidade

## 5.1 Princípio geral
Os textos regulatórios disponibilizados enfatizam que inspeções, ensaios e testes devem ser cobertos por planos e procedimentos, com instruções claras, registros atualizados, rastreabilidade e execução por pessoal qualificado; quando aplicável, por pessoal certificado.

Aplicado aos recursos de manutenção, isso sustenta que o controle de ferramentas e instrumentos não deve se limitar a “existir no almoxarifado”. É necessário comprovar que o recurso:

- está apto para o serviço pretendido;
- foi verificado conforme procedimento;
- possui evidência documental do seu estado;
- está sob rastreabilidade compatível com a criticidade do uso.

### 5.2 O que deve ser controlado por tipo de recurso

#### a) Ferramentas gerais
O controle prioritário é de:
- condição física;
- integridade aparente;
- identificação;
- limpeza e guarda;
- disponibilidade para retirada e devolução;
- segregação quando danificadas ou inadequadas.

#### b) Instrumentos e dispositivos de teste/calibração
Além da condição física, o controle precisa abranger:
- validade de calibração, quando aplicável;
- registro do padrão ou dispositivo usado;
- procedimento de teste/calibração aplicável;
- histórico de resultados e intervenções;
- identificação inequívoca do instrumento;
- evidência de ajuste ou segregação quando fora de tolerância.

#### c) Recursos de içamento
Os textos fornecidos só mencionam explicitamente a necessidade de talha móvel para movimentação interna. Portanto, o ponto suportado pelas fontes é que esses recursos devem existir e estar disponíveis para manuseio de componentes maiores, especialmente válvulas de controle e instrumentos de maior porte. Em uma sistemática robusta, seu controle deve impedir uso de recurso sem evidência de aptidão, mas as fontes não detalham critérios numéricos ou periodicidades.

### 5.3 Rastreabilidade documental mínima
Por analogia aos requisitos de inspeção e relatórios do material regulatório, uma trilha documental consistente para recursos críticos de manutenção deve conter, conforme aplicável:

- identificação do recurso;
- tipo de verificação executada;
- data de início e término da atividade;
- resultado do teste/ensaio/calibração;
- recomendações ou restrições de uso;
- nome e assinatura legível dos executantes e responsáveis;
- relatórios, registros fotográficos ou documentos complementares quando pertinentes.

### 5.4 Inspeção inicial e após transporte/reparo
Os textos regulatórios indicam que inspeções iniciais devem verificar defeitos de transporte, defeitos de montagem, identificação, prontuário, testes realizados e calibração/ajustes de sistemas de controle e segurança. Em FPSO, esse princípio é particularmente útil para recursos enviados de terra ou retornados de oficina externa: o recebimento técnico não deve assumir automaticamente que o item está pronto para uso apenas porque chegou a bordo.

### 5.5 Qualificação do pessoal
Os textos também indicam a necessidade de **pessoal qualificado** para inspeções e, quando aplicável, **pessoal certificado** para ensaios. No contexto desta faceta, isso é decisivo porque a confiabilidade do resultado depende não só do instrumento, mas do operador e do procedimento. Um instrumento calibrado operado fora do método ainda produz decisão ruim.

**Fontes:** `anp-912dd4dd5be0ece1d8e4973b:p27-32:23.0-9.0`, `anp-912dd4dd5be0ece1d8e4973b:p30-33:17.0-35.0`

## 6. Disponibilidade operacional: planejamento, parada e rotina
A disponibilidade real de ferramentas e instrumentos é função de planejamento prévio. O material sobre paradas programadas é particularmente claro nesse ponto.

### 6.1 Levantamento prévio de necessidades
Na organização da parada, cada equipe deve levantar o material necessário à execução dos serviços. A partir disso, os itens são classificados em:

- **existentes em estoque**; e
- **não disponíveis**, que precisam ser comprados.

A compra do que não está disponível deve receber prioridade elevada, em coordenação com suprimentos. Para a faceta em questão, isso inclui não apenas peças e materiais, mas também:

- instrumentos de teste;
- malas de calibração;
- multímetros;
- maletas de ferramentas;
- meios de comunicação;
- apoio de andaimes, pintura, escavações ou outras interfaces necessárias ao acesso e à execução.

### 6.2 Documentação técnica como recurso de apoio
Os textos reforçam que desenhos e documentos atualizados da instalação são de capital importância, pois o serviço executado em parada tem objetivo semelhante ao de uma montagem: garantir o funcionamento dos instrumentos e malhas dentro das especificações. Assim, a indisponibilidade documental é também uma forma de indisponibilidade operacional do recurso de manutenção.

### 6.3 Controle de duração e capacidade
Para dividir os serviços em lotes executáveis, recomenda-se usar estimativas ou **MTTR (mean time to repair)** dos instrumentos e acrescentar **folga de 20% para imprevistos**. Esse critério ajuda a dimensionar:

- quantas maletas e instrumentos de teste precisam estar disponíveis simultaneamente;
- quantas equipes podem trabalhar em paralelo;
- quando um recurso compartilhado se torna gargalo da parada.

### 6.4 Coordenação local e guarda dos recursos
O material recomenda espaço dedicado para coordenação e guarda de instrumentos de teste e maletas de ferramentas. Em um FPSO, isso ajuda a:

- evitar perdas e extravios;
- reduzir tempo de procura;
- controlar retirada/devolução;
- concentrar documentação e comunicação operacional.

### 6.5 Supervisão e controle diário
Durante a parada, os serviços devem ser supervisionados continuamente, e cada equipe deve listar diariamente os serviços efetuados e os itens executados do programa. Isso permite à coordenação decidir por:

- realocação de pessoal;
- contratação adicional;
- replanejamento;
- remanejamento de instrumentos e ferramentas entre frentes.

Esse mesmo princípio é válido para a rotina offshore: a disponibilidade precisa ser acompanhada em base suficientemente curta para impedir que um recurso crítico se transforme em atraso generalizado.  
**Fontes:** `regis-d98eb152398d79661d91c35f:pNone:15.60-38.60`

## 7. Lead time e impacto na disponibilidade dos recursos
O material define **lead time** como a soma de:

**lead time = tempo de processamento + tempo de inspeção + tempo de espera + tempo de movimentação**

Para ferramentas e instrumentos de apoio à manutenção em FPSO, essa decomposição é útil porque evidencia que a indisponibilidade não decorre apenas da falta do item. Ela pode decorrer de qualquer parcela do ciclo, por exemplo:

- processamento: cadastro, aprovação, preparação ou embalagem;
- inspeção: conferência de recebimento, verificação técnica, checagem documental;
- espera: fila para calibração, liberação administrativa, transporte, janela logística;
- movimentação: trânsito terra-base-unidade, deslocamento interno na unidade, retorno de oficina.

Como consequência, melhorar a disponibilidade não é só aumentar estoque. Pode ser mais efetivo:

- reduzir tempo de inspeção por padronização de recebimento;
- melhorar identificação e localização;
- antecipar reservas no sistema;
- descentralizar alguns recursos de calibração de uso frequente;
- integrar a programação da manutenção com a aquisição e a logística.

O mesmo material observa que, sem integração entre planejamento de manutenção e aquisição/produção, prevalece a programação de curto prazo. Em ambiente offshore, isso tende a aumentar urgências, fretes emergenciais e tempo perdido esperando recurso.  
**Fonte:** `regis-7493a0b7af9688fbb59924e0:pNone:4062.0-4278.0`

## 8. Criticidade, contingência e limites de decisão
Os textos regulatórios indicam que equipamentos e sistemas críticos precisam ser identificados, listados e cobertos por procedimentos; quando houver falta, falha, degradação ou indisponibilidade, devem existir medidas temporárias, como controles alternativos equivalentes, limitação de produção, isolamento e parada, conforme aplicável.

Para esta faceta, a aplicação prática é a seguinte: quando a manutenção ou a inspeção de um item crítico depende de um instrumento de teste ou recurso de apoio específico, a indisponibilidade desse recurso pode inviabilizar uma liberação confiável ao serviço. Nesses casos, a decisão não deve ser puramente administrativa; ela deve considerar o risco operacional e a criticidade do ativo.

Critérios técnicos úteis de decisão incluem:

- o recurso é indispensável para comprovar a condição do item antes do retorno ao serviço?
- existe método alternativo tecnicamente equivalente?
- o executante alternativo é qualificado/certificado para o método substituto?
- a ausência do recurso compromete a integridade, segurança ou conformidade do serviço?
- é necessário limitar operação, adiar retorno ao serviço ou isolar o equipamento até recomposição do recurso?

O material não fornece uma matriz específica para essa decisão em FPSO, mas sustenta o princípio de que ausência de recurso crítico requer medida temporária formalizada, e não improvisação.  
**Fontes:** `anp-912dd4dd5be0ece1d8e4973b:p27-32:23.0-9.0`, `anp-912dd4dd5be0ece1d8e4973b:p30-33:17.0-35.0`

## 9. Impacto das falhas dos equipamentos de teste
Um dos trechos disponíveis registra que a análise de falhas em equipamentos usados em testes mostra impacto direto no **tempo de operação**, sendo útil para direcionar esforços de melhoria de confiabilidade e planejamento de sobressalentes.

Mesmo tratando de equipamentos de avaliação de formações e não de oficinas de FPSO, o princípio é aplicável: falhas em recursos de teste e diagnóstico podem ampliar o tempo total da intervenção por três caminhos principais:

1. **tempo perdido aguardando substituição**;
2. **retrabalho por resultado inválido ou inconclusivo**;
3. **adiamento da decisão técnica de retorno ao serviço**.

Assim, o controle de disponibilidade não deve se limitar ao item principal; deve incluir também:

- sobressalentes do próprio equipamento de teste;
- acessórios e cabos associados;
- baterias ou fontes de alimentação, quando aplicável;
- kits de conexão e adaptação;
- histórico de falhas para priorização de confiabilidade.

Esse raciocínio justifica tratar certos instrumentos de teste como ativos relevantes da própria manutenção, e não apenas como acessórios de oficina.  
**Fonte:** `petroles-004c2afadba7ea17c7dd7908:pNone:1404420.0-1404497.0`

## 10. Indicadores e controles gerenciais coerentes com a faceta
Os textos não apresentam um conjunto fechado de KPIs para ferramentas e instrumentos, mas permitem derivar controles diretamente consistentes com o material:

### 10.1 Disponibilidade e prontidão
- percentual de recursos disponíveis para uso imediato;
- quantidade de recursos indisponíveis por falta de calibração, reparo ou documentação;
- tempo médio de atendimento de uma reserva/solicitação.

### 10.2 Conformidade de controle
- percentual de instrumentos com identificação legível e vinculada ao cadastro;
- percentual com registro atualizado de inspeção/calibração aplicável;
- número de inconsistências entre item físico e sistema.

### 10.3 Eficiência de planejamento
- percentual de serviços iniciados com todos os recursos previstos disponíveis;
- atrasos de parada associados à indisponibilidade de ferramenta/instrumento;
- aderência entre recursos planejados e efetivamente consumidos.

### 10.4 Aprendizado e melhoria
- falhas recorrentes de equipamentos de teste;
- desvios encontrados em inspeção inicial após transporte;
- lições aprendidas de parada registradas em relatório final.

A utilidade prática desses controles é transformar a gestão de ferramentas e instrumentos em parte visível da confiabilidade da manutenção.  
**Fontes:** `regis-d98eb152398d79661d91c35f:pNone:15.60-38.60`, `regis-7493a0b7af9688fbb59924e0:pNone:4062.0-4278.0`, `petroles-004c2afadba7ea17c7dd7908:pNone:1404420.0-1404497.0`

## 11. Síntese técnica
Para apoio técnico eficiente à manutenção em FPSO, o controle de ferramentas, instrumentos e içamento deve combinar cinco dimensões:

1. **infraestrutura adequada**, com layout compatível com o tipo de serviço e proteção dos instrumentos sensíveis;
2. **cadastro, identificação e localização**, para evitar perda de disponibilidade por desorganização;
3. **inspeção, calibração/certificação e rastreabilidade**, com registros consistentes e pessoal qualificado;
4. **planejamento integrado**, principalmente para paradas, considerando estoque, compras, documentação, MTTR e contingência;
5. **gestão de criticidade**, reconhecendo que a falta de um recurso de teste ou içamento pode impedir liberação segura e ampliar significativamente o tempo de indisponibilidade.

Em termos operacionais, um sistema maduro é aquele em que o recurso de apoio não aparece como surpresa de última hora: ele já está previsto, localizado, conferido, documentado e pronto para uso quando a manutenção começa.  
**Fontes:** `petroles-004c2afadba7ea17c7dd7908:pNone:981095.0-981149.0`, `regis-d98eb152398d79661d91c35f:pNone:15.60-38.60`, `regis-7493a0b7af9688fbb59924e0:pNone:4062.0-4278.0`, `anp-912dd4dd5be0ece1d8e4973b:p27-32:23.0-9.0`, `anp-912dd4dd5be0ece1d8e4973b:p30-33:17.0-35.0`, `petroles-004c2afadba7ea17c7dd7908:pNone:1404420.0-1404497.0`