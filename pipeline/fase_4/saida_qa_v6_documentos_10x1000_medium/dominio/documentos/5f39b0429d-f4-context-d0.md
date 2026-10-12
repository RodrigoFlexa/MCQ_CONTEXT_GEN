# Requisitos NR-13 para integridade de equipamentos abrangidos

## 1. Enquadramento e foco de aplicação na integridade
Os trechos fornecidos tratam principalmente de **vasos de pressão** e, de forma complementar, de **caldeiras**. Para vasos de pressão, a NR-13 é apresentada como aplicável a equipamentos instalados em unidades industriais e outros estabelecimentos, sendo também aplicável a **navios e plataformas de exploração e produção de petróleo**, **desde que não exista legislação em contrário**. Em contexto de FPSO/FSO, isso significa que a aplicação prática da NR-13 deve ser verificada juntamente com o arranjo regulatório vigente da instalação, sem presumir exclusividade normativa da NR-13.

Do ponto de vista de integridade, os conceitos centrais destacados nos trechos são:
- **PMTA (Pressão Máxima de Trabalho Admissível)** como referência básica para ajuste de dispositivos de segurança, identificação do equipamento e avaliação documental.
- Necessidade de **documentação técnica atualizada e disponível** no local de operação.
- Execução de inspeções e decisões de reparo/alteração sob responsabilidade de **Profissional Habilitado (PH)** ou estrutura formal equivalente.
- Tratamento de condições de **risco grave e iminente** quando faltam salvaguardas essenciais ou quando o equipamento opera fora das condições de projeto.

Para vasos de pressão, os trechos lembram ainda que o dimensionamento deve considerar a **pressão diferencial resultante**, podendo haver predominância de pressão interna ou externa conforme o caso. Isso é relevante para integridade porque a avaliação de espessura remanescente, de deformações e de alterações operacionais não pode ser feita apenas com base na pressão interna nominal, mas sim nas condições efetivamente consideradas no projeto.  
**Fontes:** `petroles-004c2afadba7ea17c7dd7908:pNone:1730460.0-1730527.0`, `petroles-004c2afadba7ea17c7dd7908:pNone:1730557.0-1730602.0`

## 2. Dispositivos de segurança e situações de risco grave e iminente

### 2.1. O que a NR-13 reconhece como dispositivo de segurança
Para vasos de pressão, os trechos indicam que o dispositivo de segurança deve **aliviar automaticamente a pressão**, sem depender da atuação do operador, sempre que ocorrer sobrepressão. São citados como exemplos de “outro dispositivo de segurança”:
- disco de ruptura;
- válvula quebra-vácuo;
- plugue fusível;
- e, sob condição específica, válvula de segurança operada por piloto, desde que mantenha capacidade funcional em qualquer condição de anormalidade operacional.

Os textos também deixam claro que **pressostatos, reguladores de pressão, malhas de controle e instrumentação de controle** não devem ser confundidos com dispositivo de segurança. Em termos de integridade, isso é importante porque uma malha de controle pode reduzir frequência de sobrepressão, mas **não substitui** a proteção independente exigida para preservar a integridade estrutural do equipamento.

### 2.2. Ajuste e posicionamento dos dispositivos
As válvulas de segurança devem abrir na pressão estabelecida pelo código de projeto; no caso citado do **ASME VIII**, esse valor deve ser **igual ou inferior à PMTA**. Após a abertura, o código pode admitir sobrepressão limitada durante a atuação plena da válvula, mas essa margem não deve ser excedida.

Os trechos classificam como **risco grave e iminente** a falta de qualquer dos seguintes itens em vaso de pressão:
- válvula ou outro dispositivo de segurança com pressão de abertura ajustada em valor **igual ou inferior à PMTA**, instalada diretamente no vaso ou no sistema que o inclui;
- dispositivo de segurança contra **bloqueio inadvertido** da válvula, quando a válvula não estiver instalada diretamente no vaso.

### 2.3. Bloqueio inadvertido
O controle contra bloqueio inadvertido é especialmente relevante quando há:
- vasos com **dois ou mais dispositivos de segurança**;
- conjunto de vasos interligados protegidos por **única válvula de segurança**;
- arranjos com múltiplas válvulas de segurança e bloqueios independentes para facilitar manutenção.

Nesses casos, as válvulas remanescentes devem ter capacidade suficiente, em conjunto ou isoladamente, para aliviar a pressão do vaso. Também é enfatizado que o bloqueio inadvertido pode existir **a montante ou a jusante** da válvula de segurança. São citados como meios de prevenção válvulas de duas ou mais vias, válvulas-gaveta sem volante ou com volante travado por cadeado. Quando o vaso possui **apenas uma válvula de segurança**, o texto afirma que **não é recomendável** a existência de bloqueio entre a válvula e o vaso.

### 2.4. Instrumentação associada
Instrumentos de indicação de pressão, como manômetros, podem ter mostrador **analógico ou digital** e podem ser instalados no próprio equipamento ou em sala de controle. Isso não elimina a necessidade dos dispositivos de alívio, mas integra o conjunto mínimo de monitoramento operacional e de verificação das condições de integridade.  
**Fontes:** `petroles-004c2afadba7ea17c7dd7908:pNone:1730460.0-1730527.0`, `petroles-004c2afadba7ea17c7dd7908:pNone:1730529.0-1730578.0`

## 3. Identificação do equipamento e rastreabilidade física
A identificação física do equipamento é tratada como requisito operacional e também de resposta a emergências.

### 3.1. Placa de identificação de vasos de pressão
Todo vaso de pressão deve ter, em local visível e de fácil acesso, **placa de identificação indelével** com pelo menos:
- fabricante;
- número de identificação;
- ano de fabricação;
- PMTA;
- pressão de teste hidrostático;
- código de projeto e ano de edição.

O texto explica que o número de identificação pode corresponder ao **tag** ou outro identificador alfanumérico atribuído pelo projetista ou estabelecimento.

Se o ano de edição do código não for conhecido, o PH deve verificar se o equipamento atende aos requisitos da última edição publicada que preceda o ano de fabricação. Se o código original ou o ano de fabricação não forem conhecidos, o equipamento deve ser verificado com base em código internacionalmente aceito, como **ASME, DIN ou JIS**, sem presumir equivalência automática com o projeto original.

### 3.2. Categoria e marcação visível
Além da placa, devem constar em local visível:
- a **categoria do vaso**;
- seu número ou código de identificação.

Os trechos indicam que essas informações devem ser pintadas de forma que permitam **rápida identificação** em situação de emergência, podendo alternativamente constar de placa com visualização equivalente. A justificativa é prática: em cenários com vazamento, incêndio, fumaça, vapores ou névoa, a identificação visível auxilia operadores e equipes externas.

### 3.3. Paralelo com caldeiras
Para caldeiras, os trechos trazem lógica análoga, mas com dados adicionais na placa, como **capacidade de produção de vapor** e **área de superfície de aquecimento**. O material da placa deve resistir às intempéries e não deve ser fixado em partes removíveis, como bocas de visita ou chapas de isolamento.  
**Fontes:** `petroles-004c2afadba7ea17c7dd7908:pNone:1730529.0-1730578.0`, `petroles-004c2afadba7ea17c7dd7908:pNone:1730557.0-1730602.0`, `petroles-004c2afadba7ea17c7dd7908:pNone:1730043.0-1730101.0`

## 4. Documentação obrigatória e sua função na gestão da integridade
A documentação exigida pela NR-13 não é apenas comprovação regulatória; ela forma a base da gestão da integridade mecânica.

### 4.1. Conjunto documental mínimo para vasos de pressão
Todo vaso de pressão deve possuir, no estabelecimento onde estiver instalado, documentação atualizada contendo:
- **Prontuário do Vaso de Pressão**;
- **Registro de Segurança**;
- **Projeto de Instalação**;
- **Projetos de Alteração ou Reparo**;
- **Relatórios de Inspeção**.

O **Prontuário do Vaso** deve conter, no mínimo:
- código de projeto e ano de edição;
- especificação dos materiais;
- procedimentos usados na fabricação, montagem e inspeção final;
- determinação da PMTA;
- conjunto de desenhos e demais dados necessários ao monitoramento da vida útil;
- características funcionais;
- dados dos dispositivos de segurança;
- ano de fabricação;
- categoria do vaso.

### 4.2. Disponibilidade no local de operação
Se houver várias unidades, os documentos devem estar disponíveis na unidade em que o equipamento estiver instalado. Se operadores e responsáveis não permanecerem no local de instalação, os documentos devem ficar **próximos ao operador responsável**. O texto afirma explicitamente que essa exigência também se aplica a **navios e plataformas de exploração e produção de petróleo**.

Além disso, a documentação deve permanecer disponível para consulta de:
- operadores;
- manutenção;
- inspeção;
- representações dos trabalhadores e do empregador na CIPA;
- representação sindical, quando formalmente solicitada.

### 4.3. Guarda, reconstituição e vida útil documental
A documentação deve ser mantida **durante toda a vida útil** do vaso de pressão. Se o prontuário estiver inexistente ou extraviado, ele deve ser **reconstituído pelo proprietário**, com responsabilidade técnica do fabricante ou de PH. Os trechos destacam como imprescindível a reconstituição de:
- características funcionais;
- dados dos dispositivos de segurança;
- procedimento de determinação da PMTA.

Também é mencionado que o procedimento de determinação da PMTA deve explicar o roteiro de cálculo passo a passo, podendo o estabelecimento adotar, se houver interesse, a **pressão de projeto como PMTA**. O texto adverte ainda que normas internacionais reconhecidas indicam que o cálculo da PMTA deve considerar não apenas pressão, mas também outros esforços atuantes sobre conexões, flanges, suportes, selas e demais partes.

### 4.4. Registro de Segurança
O Registro de Segurança pode assumir a forma de:
- livro de páginas numeradas;
- pastas;
- sistema informatizado com confiabilidade equivalente.

Nele devem ser registradas:
- ocorrências importantes capazes de influir nas condições de segurança do vaso;
- ocorrências de inspeção de segurança.

Exemplos citados de registros pertinentes:
- explosões;
- incêndios;
- vazamentos;
- ruptura de componentes;
- operação fora dos valores previstos;
- funcionamento irregular de válvulas de segurança;
- serviços de manutenção efetuados.

Em termos de integridade, isso significa que o Registro de Segurança deve servir como **histórico rastreável de degradação, anomalias, intervenções e desvios operacionais**, apoiando decisões de inspeção, revisão de periodicidades e gestão de risco.  
**Fontes:** `petroles-004c2afadba7ea17c7dd7908:pNone:1730557.0-1730602.0`, `petroles-004c2afadba7ea17c7dd7908:pNone:1730579.0-1730622.0`

## 5. Profissional Habilitado (PH) e Serviço Próprio de Inspeção de Equipamentos (SPIE)
Os trechos fornecidos tratam o **PH** como agente central para decisões técnicas que afetam integridade, inspeção, reparo, testes e aceitação de alternativas.

### 5.1. Papel do PH
O PH aparece como responsável ou aprovador em temas como:
- verificação de enquadramento do equipamento a códigos de projeto quando há lacunas documentais;
- realização de inspeções de segurança;
- definição de parâmetros de testes hidrostáticos;
- justificativa técnica para substituir testes por métodos alternativos;
- concepção ou aprovação de projetos de alteração e reparo;
- definição de critérios mais rigorosos quando o código original é desconhecido.

### 5.2. SPIE e ampliação de prazos especiais
Antes de aplicar períodos especiais entre inspeções, o **Serviço Próprio de Inspeção de Equipamentos** da empresa deve ser certificado pelo **Inmetro** ou organismo credenciado, segundo os trechos fornecidos. Os requisitos mínimos citados incluem:
- pessoal próprio com dedicação exclusiva a inspeção, avaliação de integridade e vida residual;
- qualificação, formação e treinamento compatíveis;
- mão de obra contratada para END certificada conforme regulamentação vigente;
- responsável formalmente designado pela gestão do serviço;
- existência de pelo menos um PH;
- arquivo técnico atualizado e mecanismos de distribuição de informações;
- procedimentos escritos para as principais atividades;
- aparelhagem compatível com as atividades propostas.

Para plataformas de produção/exploração de petróleo e navios, o texto informa que o SPIE **pode ser instalado em terra**. Em ambiente FPSO, esse ponto é relevante porque a estrutura de governança de inspeção pode ser parcialmente onshore, desde que a documentação e a capacidade de resposta operacional no local continuem asseguradas.  
**Fontes:** `petroles-004c2afadba7ea17c7dd7908:pNone:1730460.0-1730527.0`, `petroles-004c2afadba7ea17c7dd7908:pNone:1730375.0-1730417.0`

## 6. Inspeção de segurança de vasos de pressão

### 6.1. Princípios gerais
Os trechos reforçam que a inspeção de segurança deve ser executada por **PH** e documentada em relatório. Embora os números exatos de periodicidade não estejam recuperados integralmente nos trechos, a estrutura regulatória mostrada distingue:
- inspeção inicial;
- inspeção periódica;
- inspeção extraordinária.

### 6.2. Inspeção extraordinária
A inspeção de segurança extraordinária deve ser feita nas seguintes oportunidades:
- quando o vaso for danificado por acidente ou outra ocorrência que comprometa sua segurança;
- quando o vaso sofrer reparo ou alteração importante capaz de alterar sua condição de segurança;
- antes de recolocação em funcionamento, quando permanecer inativo por período superior ao limite indicado na NR-13;
- quando houver alteração do local de instalação.

A inspeção extraordinária pode abranger todo o vaso ou apenas parte dele, conforme necessidade e critério do PH.

### 6.3. Exame interno, exame externo e alternativa para impossibilidade física
Quando o vaso não permitir exame interno ou externo por impossibilidade física, os trechos indicam a possibilidade de submetê-lo **alternativamente a teste hidrostático**, observadas as limitações normativas. São exemplos de impossibilidade de exame interno:
- ausência de bocas de visita ou aberturas que permitam a passagem de uma pessoa;
- diâmetro de casco que impeça acesso humano;
- trocadores de calor com espelho soldado ao casco.

Como exemplo de impossibilidade de acesso externo, o texto cita **equipamentos enterrados**.

### 6.4. Casos especiais com enchimento, catalisador ou revestimento
Vasos com **enchimento interno** ou **catalisador** podem ter a periodicidade do exame interno ou do teste hidrostático ampliada para coincidir com a época de substituição desses elementos, respeitado o limite percentual previsto na norma. Os trechos citam como exemplos de enchimento interno argila, aparas de aço e anéis de Raschig, e deixam claro que acessórios desmontáveis, como bandejas, não devem ser tratados como enchimento interno.

Para vasos com **revestimento interno higroscópico**, o teste hidrostático deve ser feito **antes da aplicação do revestimento**, sendo os testes subsequentes substituídos por técnicas alternativas. O exemplo dado é o revestimento refratário.

### 6.5. Substituição do teste hidrostático
Quando o teste hidrostático for tecnicamente inviável, e isso for registrado no Registro de Segurança pelo PH, ele pode ser substituído por outra técnica de ensaio não destrutivo ou inspeção que proporcione **segurança equivalente**. Os trechos citam como exemplos:
- ultrassom;
- líquido penetrante;
- partículas magnéticas;
- ensaio de estanqueidade;
- apreciação do histórico operacional ou de inspeções anteriores;
- técnicas do tipo **leakage before breaking**.

São citadas como razões técnicas típicas para inviabilizar o teste hidrostático:
- resistência estrutural da fundação ou sustentação incompatível com o peso da água de teste;
- efeito prejudicial do fluido de teste a elementos internos;
- impossibilidade técnica de purga e secagem;
- existência de revestimento interno;
- influência prejudicial do teste sobre defeitos subcríticos.

O texto explicita que **razões meramente econômicas não devem ser usadas** para afastar o teste hidrostático. A decisão de substituição deve constar do relatório de inspeção de segurança assinado pelo PH.

### 6.6. Teste pneumático e válvulas de segurança
O teste pneumático somente deve ser executado quando não houver alternativa, sob supervisão do PH e com cuidados especiais, por se tratar de atividade de alto risco.

As válvulas de segurança dos vasos de pressão devem ser desmontadas, inspecionadas e recalibradas por ocasião do exame interno periódico. Se a experiência operacional mostrar problemas em prazo menor, a frequência deve ser encurtada. Quando possível, a pressão de abertura pode ser verificada por dispositivo hidráulico com o vaso em operação.  
**Fontes:** `petroles-004c2afadba7ea17c7dd7908:pNone:1730765.0-1730821.0`, `petroles-004c2afadba7ea17c7dd7908:pNone:1730557.0-1730602.0`

## 7. Operação fora do projeto, reparos, alterações e manutenção

### 7.1. Operar fora do projeto é condição crítica
Os trechos caracterizam como **condição de risco grave e iminente** a operação de vaso de pressão em condições diferentes das previstas no projeto original sem que:
- o equipamento seja reprojetado considerando todas as variáveis da nova condição operacional;
- sejam adotados os procedimentos de segurança decorrentes da nova classificação, no que se refere a instalação, operação, manutenção e inspeção.

São exemplos de mudanças citadas:
- pressões superiores às de operação original;
- temperaturas superiores às consideradas no projeto;
- fluidos diferentes dos originalmente previstos;
- alterações de geometria, espessura ou material.

Em gestão de integridade, isso implica que mudanças de processo, de envelope operacional ou de fluido não podem ser tratadas apenas como ajuste operacional: elas podem exigir **revalidação de projeto, atualização documental e revisão do plano de inspeção**.

### 7.2. Reparo x alteração
Os textos distinguem:
- **reparo**: intervenção para corrigir não conformidade em relação ao projeto original, como recomposição por solda, remoção de defeitos em juntas soldadas ou substituição de conexões corroídas;
- **alteração**: intervenção que modifica o projeto original, inclusive parâmetros operacionais, como mudança de materiais, internos, conexões ou geometria.

### 7.3. Regras para reparos e alterações
Todos os reparos ou alterações devem respeitar o código de projeto de construção e as prescrições do fabricante quanto a:
- materiais;
- procedimentos de execução;
- procedimentos de controle da qualidade;
- qualificação e certificação de pessoal.

Para tubulação, o trecho fornecido limita essa abrangência ao trecho compreendido entre o corpo do vaso e a solda ou flange mais próximo, inclusive.

Se o código original for desconhecido, deve-se respeitar a concepção original do vaso e adotar os procedimentos de controle **mais rigorosos** prescritos por códigos pertinentes. Se a documentação tiver sido extraviada e o fabricante não puder ser localizado, o PH deve propor testes, ensaios e critérios de aceitação compatíveis com esse maior rigor.

### 7.4. Projeto de Alteração ou Reparo
Deve existir **Projeto de Alteração ou Reparo concebido previamente** sempre que:
- as condições de projeto forem modificadas;
- forem realizados reparos que possam comprometer a segurança.

Esse projeto deve:
- ser concebido ou aprovado por PH;
- determinar materiais, procedimentos de execução, controle da qualidade e qualificação de pessoal;
- ser divulgado aos trabalhadores envolvidos com o equipamento.

### 7.5. Teste após intervenções em partes sob pressão
Intervenções com soldagem em partes que operem sob pressão devem ser seguidas de **teste hidrostático** com características definidas pelo PH, incluindo medidas de segurança, fluido de teste, taxa de pressurização, pressão final e tempo de permanência pressurizado. Pequenas intervenções superficiais podem ter o teste dispensado a critério do PH, considerando tipo de reparo, END executados, qualificação da equipe e risco de falha.

### 7.6. Sistemas de controle e segurança
Os sistemas de controle e segurança dos vasos devem ser submetidos a **manutenção preventiva ou preditiva**. A definição de quais instrumentos e sistemas entram no plano, bem como sua periodicidade, deve ser feita por profissional legalmente competente.  
**Fontes:** `petroles-004c2afadba7ea17c7dd7908:pNone:1730696.0-1730749.0`

## 8. Requisitos de instalação que impactam inspeção e segurança
A forma de instalação afeta diretamente a capacidade de inspecionar, operar e responder a emergências.

Os trechos indicam que todo vaso de pressão deve ser instalado de modo que **drenos, respiros, bocas de visita e indicadores de nível, pressão e temperatura** sejam facilmente acessíveis. Os acessórios que exijam presença do trabalhador para operação, manutenção ou inspeção devem permitir acesso fácil e seguro por escadas, plataformas e meios compatíveis com as NRs.

Quando instalados em **ambientes confinados**, os vasos devem dispor de:
- pelo menos duas saídas amplas, permanentemente desobstruídas e em direções distintas;
- fácil acesso seguro para manutenção, operação e inspeção;
- ventilação permanente com entradas de ar não bloqueáveis;
- iluminação conforme normas oficiais;
- iluminação de emergência.

Em termos de integridade e segurança operacional, isso significa que a NR-13 não separa completamente o equipamento de seu contexto físico de instalação: um vaso com boa condição mecânica, mas sem acesso seguro ou rota de fuga adequada, permanece em situação inadequada do ponto de vista regulatório e operacional.  
**Fontes:** `petroles-004c2afadba7ea17c7dd7908:pNone:1730579.0-1730622.0`

## 9. Pontos específicos sobre caldeiras que podem coexistir em FPSO/FSO
Embora o foco operacional em unidades flutuantes recaia com frequência sobre vasos, separadores e trocadores, os trechos também trazem requisitos importantes para **caldeiras**, que podem existir como utilidades em certas instalações.

### 9.1. PMTA e atualização
O material destaca que a PMTA pode se alterar ao longo da vida da caldeira em função de:
- redução da resistência mecânica dos materiais;
- redução de espessuras;
- outras alterações relevantes.

Quando houver alteração da PMTA, devem ser ajustados, conforme aplicável:
- pressão de abertura das válvulas de segurança;
- placa de identificação;
- demais elementos de controle dependentes desse valor.

### 9.2. Itens mínimos de segurança e risco grave
Os trechos classificam como risco grave e iminente, em caldeiras, a falta de itens essenciais como:
- válvula de segurança ajustada em valor igual ou inferior à PMTA;
- instrumento de indicação de pressão do vapor acumulado;
- meios específicos de alimentação de água e controle de nível, conforme tipo de caldeira;
- outros itens particulares ao serviço.

### 9.3. Documentação e inspeções
Também para caldeiras existe exigência de:
- placa de identificação indelével;
- prontuário;
- registro de segurança;
- projeto de instalação;
- projetos de alteração ou reparo;
- relatórios de inspeção.

As inspeções de segurança podem ser iniciais, periódicas ou extraordinárias. Os trechos fornecidos informam ainda:
- necessidade de avaliação rigorosa de integridade e vida remanescente após determinado tempo de uso previsto na NR-13;
- inspeção periódica de válvulas de segurança, com acionamento manual em certas categorias e desmontagem/teste/recalibração em outras;
- execução de **teste de acumulação** em situações específicas, como inspeção inicial, modificações relevantes ou mudança de parâmetros operacionais.

Como os valores numéricos exatos não foram preservados nos trechos, esses requisitos devem ser aplicados com consulta à redação normativa vigente.  
**Fontes:** `petroles-004c2afadba7ea17c7dd7908:pNone:1730043.0-1730101.0`, `petroles-004c2afadba7ea17c7dd7908:pNone:1730375.0-1730417.0`

## 10. Síntese prática para aplicação em integridade
Com base nos trechos fornecidos, a aplicação da NR-13 à integridade de equipamentos abrangidos pode ser resumida em uma lógica decisória:

1. **Confirmar enquadramento do equipamento** e sua categoria.  
2. **Assegurar identificação física** visível e coerente com a documentação.  
3. **Manter prontuário, registro, projeto de instalação, projetos de reparo/alteração e relatórios de inspeção** atualizados e disponíveis no local de operação.  
4. **Verificar dispositivos de segurança** ajustados à PMTA e protegidos contra bloqueio inadvertido quando aplicável.  
5. **Executar inspeções sob responsabilidade de PH**, registrando resultados e ocorrências relevantes no Registro de Segurança.  
6. **Tratar mudanças operacionais, reparos e alterações como eventos de integridade**, não apenas de manutenção, com reprojeto e documentação quando necessários.  
7. **Justificar tecnicamente qualquer substituição de teste hidrostático** por END ou técnicas alternativas, formalizando a decisão.  
8. **Garantir acessibilidade e condições seguras de instalação**, pois elas afetam a inspeção, a manutenção e a resposta a emergências.

Essa leitura é adequada para avaliação profissional de conformidade e integridade mecânica em FPSO/FSO, mas depende de validação contra a redação vigente da NR-13 e contra os requisitos específicos aplicáveis à instalação.  
**Fontes:** todos os trechos listados em `used_chunk_ids`.