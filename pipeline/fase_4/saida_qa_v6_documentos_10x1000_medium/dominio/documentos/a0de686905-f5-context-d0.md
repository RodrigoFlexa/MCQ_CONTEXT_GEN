# Prontidão e evacuação

## 1. Enquadramento da faceta e recorte técnico
A integração dos sistemas e equipamentos de salvatagem com muster, abandono e resgate em FPSOs depende menos de um item isolado de equipamento e mais da coerência entre análise de riscos, plano de emergência, comando da resposta, comunicações, treinamento, simulados e disponibilidade real dos recursos. Nesta faceta, o foco está na prontidão operacional para que os meios de salvatagem possam ser efetivamente usados quando o cenário evolui de alarme e reunião para evacuação, abandono e posterior resgate. (Fontes: `anp-eec7f988e9eeea4ece5e1b8d:p24-27:17.0-10.0`, `anp-dabfb60617e4f0ede433578e:p237-242:20.0-15.0`, `anp-dabfb60617e4f0ede433578e:p269-272:16.0-16.0`)

O material disponível nesta rodada é mais forte em requisitos de gestão e em lições aprendidas de resposta a emergência do que em critérios prescritivos de arquitetura naval ou de arranjo detalhado de embarcações de sobrevivência. Assim, este documento enfatiza integração operacional, coordenação, treinamento, simulados e fatores humanos. (Fontes: `anp-eec7f988e9eeea4ece5e1b8d:p24-27:17.0-10.0`)

## 2. Base SGSO para integrar salvatagem, muster, abandono e resgate
Pelo SGSO, o operador deve:

- identificar as grandes emergências e descrever os cenários acidentais associados;
- avaliar a capacidade de resposta a cada cenário;
- apresentar ações efetivas de resposta;
- preparar, documentar e estabelecer o Plano de Emergência da instalação;
- identificar todos os recursos de resposta, inclusive sistemas e equipamentos de emergência e empresas contratadas de apoio, certificando-se de sua adequação e disponibilidade;
- estabelecer sistemas confiáveis e eficazes de comunicação e alarme;
- manter programa de treinamento para a equipe de resposta e, no mínimo, treinamento de alarme e evacuação para todas as demais pessoas expostas aos cenários acidentais;
- realizar exercícios simulados periódicos abrangendo todos os cenários previstos no Plano de Emergência. (Fontes: `anp-eec7f988e9eeea4ece5e1b8d:p24-27:17.0-10.0`)

Para a integração com salvatagem, isso significa que os meios de abandono não podem ser tratados apenas como capacidade instalada. Eles precisam estar inseridos numa cadeia de resposta em que o plano defina, de modo rastreável:

1. quem decide e em que estrutura de comando;
2. como o alarme é disseminado;
3. para onde as pessoas se deslocam inicialmente;
4. como se confirma se o ponto de encontro ou refúgio temporário permanece seguro;
5. quais recursos complementares são acionados se houver degradação ou indisponibilidade;
6. como se faz a transição coordenada de reunião para evacuação, abandono e resgate. (Fontes: `anp-eec7f988e9eeea4ece5e1b8d:p24-27:17.0-10.0`, `petroles-004c2afadba7ea17c7dd7908:pNone:3234448.0-3234479.0`)

O mesmo regulamento também exige que os riscos sejam sistematicamente avaliados nas fases de projeto, construção, comissionamento e operação, com implementação documentada das ações corretivas. Na prática, mudanças de estratégia de muster, rotas de fuga, pontos de encontro, pontos alternativos e recursos complementares de resgate devem derivar dessa base analítica, e não apenas de hábito operacional. (Fontes: `anp-eec7f988e9eeea4ece5e1b8d:p24-27:17.0-10.0`)

## 3. Encadeamento funcional entre ponto de encontro, refúgio temporário e abandono
A investigação do acidente do FPSO Cidade de São Mateus mostra que a integração entre muster e abandono falha quando o ponto de encontro é tratado como local estático, sem reavaliação da exposição ao perigo e sem alternativas claramente estabelecidas. No caso analisado, houve desmobilização de pontos de encontro durante uma emergência ainda em curso, o que expôs pessoas a riscos adicionais e levou a condutas incompatíveis com uma situação emergencial, como deslocamentos desnecessários e uso de elevador. (Fontes: `anp-dabfb60617e4f0ede433578e:p237-242:20.0-15.0`)

Duas implicações técnicas são centrais:

### 3.1 O ponto de encontro não deve ser mantido nem desmobilizado automaticamente
A permanência em muster deve ser subordinada à segurança do local e à evolução do cenário. Porém, a simples liberação das pessoas durante uma emergência não controlada pode aumentar drasticamente a exposição. Logo, o plano de emergência deve prever critérios de gestão do ponto de encontro e da permanência no refúgio temporário com base em cenários acidentais estudados. (Fontes: `anp-dabfb60617e4f0ede433578e:p237-242:20.0-15.0`, `anp-eec7f988e9eeea4ece5e1b8d:p24-27:17.0-10.0`)

### 3.2 Devem existir alternativas para perda de segurança do ponto primário
A investigação apontou ausência de evidências de estudos que avaliassem a segurança dos pontos de encontro destinados a pessoas com função de resposta e que indicassem pontos alternativos quando os definidos no plano se tornassem inseguros. Para salvatagem, esse aprendizado é diretamente aplicável: a estratégia de evacuação precisa considerar perda de acesso, sobrepressão, fumaça, atmosfera perigosa e outras condições que inviabilizem o ponto primário ou o trajeto previsto. (Fontes: `anp-dabfb60617e4f0ede433578e:p237-242:20.0-15.0`)

Em termos operacionais, a interface entre refúgio temporário e abandono deve minimizar exposição humana durante a resposta, inclusive para brigada e equipes que precisem atuar fora do refúgio. Não basta prever locais de reunião; é necessário demonstrar que esses locais e seus alternativos foram considerados frente aos cenários acidentais relevantes. (Fontes: `anp-dabfb60617e4f0ede433578e:p237-242:20.0-15.0`, `anp-eec7f988e9eeea4ece5e1b8d:p24-27:17.0-10.0`)

## 4. Comando, coordenação e comunicação na prontidão para abandono e resgate
O SGSO exige estrutura organizacional de resposta, sistemas de alerta, comunicação do acidente, procedimentos de resposta e procedimento para acionamento de recursos e estruturas complementares. Isso inclui tanto coordenação interna quanto interface com recursos externos ou compartilhados. (Fonte: `anp-eec7f988e9eeea4ece5e1b8d:p24-27:17.0-10.0`)

A investigação do FPSO Cidade de São Mateus mostra a importância de um sistema de comando estruturado. A resposta inicialmente não se organizou conforme o Incident Command System, embora isso estivesse previsto proceduralmente; a estrutura foi ajustada depois, quando as consequências do evento e as dificuldades de controle ficaram evidentes. A lição técnica é que um modelo de comando só agrega valor se estiver efetivamente implantado, conhecido e exercitado, e não apenas escrito. (Fonte: `anp-dabfb60617e4f0ede433578e:p269-272:16.0-16.0`)

Para integrar salvatagem ao abandono e resgate, a cadeia de comando deve garantir, no mínimo:

- decisão clara sobre manutenção em refúgio temporário, evacuação ou abandono;
- disciplina de comunicações entre comando offshore, centro de crise onshore quando aplicável, equipes de resposta, embarcações de apoio e recursos externos;
- registro e passagem de turno/handover entre comandantes e funções-chave;
- ativação tempestiva de recursos complementares compartilhados ou de terceiros. (Fontes: `anp-eec7f988e9eeea4ece5e1b8d:p24-27:17.0-10.0`, `anp-dabfb60617e4f0ede433578e:p269-272:16.0-16.0`, `petroles-004c2afadba7ea17c7dd7908:pNone:3234448.0-3234479.0`)

Como boa prática de gestão, centros de controle de emergência devem dispor de planos, contatos, sistemas de comunicação e alarme, mapeamento de vulnerabilidades e planos de simulados. Embora essa referência venha de literatura técnica associada a API/OSHA, ela é útil como prática de engenharia e gestão para apoiar a coordenação de emergência em instalações complexas. (Fonte: `petroles-004c2afadba7ea17c7dd7908:pNone:3234448.0-3234479.0`)

## 5. Disponibilidade real de recursos de resgate e apoio externo
A adequação do plano depende de os recursos previstos estarem realmente disponíveis quando acionados. No caso investigado pela ANP, observou-se falta de clareza sobre como atuar em períodos de indisponibilidade de helicópteros aeromédicos, pois não havia obrigação clara de disponibilização de aeronave substituta equivalente. Também se registrou que o PRE e documentos correlatos não descreviam os recursos necessários para cada cenário acidental e, por isso, não podiam garantir sua disponibilidade. (Fonte: `anp-dabfb60617e4f0ede433578e:p269-272:16.0-16.0`)

Transpondo a lição para salvatagem em FPSO, a integração com abandono e resgate exige que recursos complementares — por exemplo, apoio aeromédico, meios externos de resgate e recursos compartilhados com outras bases ou contratadas — tenham:

- critérios de acionamento definidos;
- disponibilidade conhecida em condição normal e degradada;
- tratamento explícito para manutenção, substituição e indisponibilidade;
- correspondência entre cenário previsto e recurso efetivamente mobilizável. (Fontes: `anp-dabfb60617e4f0ede433578e:p269-272:16.0-16.0`, `anp-eec7f988e9eeea4ece5e1b8d:p24-27:17.0-10.0`)

Sem isso, a instalação pode possuir um arranjo formal de abandono e resgate, mas não uma capacidade assegurada de resposta.

## 6. Treinamento, familiarização e simulados
O SGSO estabelece dois níveis mínimos de capacitação:

- membros da equipe de resposta à emergência: treinamento compatível com suas funções;
- demais pessoas expostas: ao menos treinamento relativo a procedimentos de alarme e evacuação. (Fonte: `anp-eec7f988e9eeea4ece5e1b8d:p24-27:17.0-10.0`)

No caso investigado, embora houvesse previsão de cursos relevantes para brigadistas, inclusive embarcações de sobrevivência e salvamento e embarcações rápidas de resgate, a capacitação para lidar com grandes emergências mostrava concentração excessiva no OIM, e a formação dos ocupantes de funções de destaque no sistema de comando era limitada. Apenas parte do grupo amostral havia participado de curso sobre o tema, e poucos tinham experiência em simulados. Isso evidencia que treinamento nominal ou concentrado em poucas lideranças não assegura prontidão coletiva. (Fonte: `anp-dabfb60617e4f0ede433578e:p269-272:16.0-16.0`)

O material complementar de Petrolês reforça boas práticas úteis para essa faceta:

- programação anual de simulados aprovada em coordenação gerencial;
- planejamento do simulado com definição do cenário e dos impactos esperados;
- treinamentos práticos de campo para aprimoramento de técnicas de resposta, resgate e primeiros socorros;
- reconhecimento de trajetos, tempos de percurso e dificuldades operacionais;
- treinamento de todos os cenários relevantes, inclusive com estruturas de auxílio mútuo e contingência quando aplicável. (Fontes: `petroles-004c2afadba7ea17c7dd7908:pNone:2449364.0-2449410.0`, `petroles-004c2afadba7ea17c7dd7908:pNone:3234448.0-3234479.0`)

Além da execução do exercício, é tecnicamente importante avaliar:

- comunicação via rádio e in loco;
- deslocamento até o local e até os pontos previstos;
- tempo de resposta;
- adequação da tática empregada ao plano;
- suficiência de recursos humanos e materiais;
- oportunidades de melhoria, com realimentação do plano e disseminação entre grupos de turno. (Fonte: `petroles-004c2afadba7ea17c7dd7908:pNone:508283.0-508329.0`)

Essa lógica é particularmente relevante para abandono e resgate, porque a execução sob estresse tende a divergir do procedimento escrito. O simulado deve, portanto, testar não só o conhecimento declaratório, mas a coordenação real entre pessoas, comando e recursos.

## 7. Fatores humanos críticos na evacuação e no abandono
As fontes apontam vários fatores humanos com impacto direto sobre a salvatagem:

### 7.1 Baixa frequência e alta consequência
Emergências industriais e offshore são eventos de baixa frequência. Mesmo com treinamento, podem conter elementos desconhecidos para os envolvidos. Em cenários súbitos, a hesitação dos trabalhadores em reagir pode atrasar decisões críticas. (Fonte: `petroles-004c2afadba7ea17c7dd7908:pNone:508283.0-508329.0`)

### 7.2 Disciplina operacional sob incerteza
No caso do FPSO Cidade de São Mateus, a desmobilização de pontos de encontro durante emergência em andamento foi interpretada como evidência de baixa disciplina operacional e deficiência de conscientização das lideranças de bordo. Para abandono e evacuação, isso significa que a pressão para retomar rotinas, buscar conforto ou executar deslocamentos não essenciais pode aumentar a exposição justamente quando a situação ainda é instável. (Fonte: `anp-dabfb60617e4f0ede433578e:p237-242:20.0-15.0`)

### 7.3 Conscientização de toda a força de trabalho
A investigação concluiu que a força de trabalho envolvida na operação e manutenção não havia sido adequadamente conscientizada sobre situações e condições capazes de provocar incidentes ou escalonar a emergência. Em termos de salvatagem, isso reforça que familiarização não deve ficar restrita à brigada: toda a população a bordo precisa compreender alarme, reunião, permanência em refúgio, restrições de circulação e obediência à estrutura de comando. (Fontes: `anp-dabfb60617e4f0ede433578e:p237-242:20.0-15.0`, `anp-eec7f988e9eeea4ece5e1b8d:p24-27:17.0-10.0`)

### 7.4 Clareza de papéis
A organização da resposta deve deixar explícito quem permanece em funções de combate/mitigação, quem protege o refúgio temporário, quem prepara a evacuação e quem coordena o acionamento de recursos externos. Ambiguidade organizacional reduz velocidade e aumenta a chance de exposição indevida. (Fontes: `anp-eec7f988e9eeea4ece5e1b8d:p24-27:17.0-10.0`, `anp-dabfb60617e4f0ede433578e:p269-272:16.0-16.0`)

## 8. Ciclo de melhoria contínua aplicado à prontidão
A preparação para emergências deve ser tratada como processo contínuo, envolvendo prevenção, prontidão, resposta e recuperação. Para esta faceta, isso se traduz em um ciclo fechado:

1. análise de riscos e cenários;
2. definição dos recursos e da estratégia de resposta;
3. treinamento e familiarização;
4. simulado e verificação prática;
5. análise crítica das falhas e dificuldades;
6. revisão do plano, dos recursos e das interfaces organizacionais. (Fontes: `petroles-004c2afadba7ea17c7dd7908:pNone:3234448.0-3234479.0`, `petroles-004c2afadba7ea17c7dd7908:pNone:508283.0-508329.0`, `anp-eec7f988e9eeea4ece5e1b8d:p24-27:17.0-10.0`)

Esse ciclo é decisivo para salvatagem porque muitos desvios só aparecem quando se testa a resposta de forma integrada: comunicações, deslocamento, ocupação de pontos de encontro, interface com refúgio temporário, acionamento de meios complementares e disciplina de comando.

## 9. Síntese técnica
Para fins de prontidão e evacuação em FPSOs, a integração eficaz dos sistemas e equipamentos de salvatagem com muster, abandono e resgate requer, de forma combinada:

- cenários acidentais e capacidade de resposta formalmente avaliados;
- plano de emergência que conecte alarme, comunicação, estrutura organizacional, recursos e acionamento de apoio complementar;
- análise explícita da segurança dos pontos de encontro e de seus alternativos;
- minimização da exposição humana, inclusive da brigada e das equipes que atuam fora do refúgio temporário;
- comando estruturado e efetivamente treinado, não apenas previsto em procedimento;
- disponibilidade comprovável dos recursos próprios, compartilhados e terceirizados;
- treinamentos e simulados periódicos abrangendo todos os cenários relevantes;
- tratamento explícito dos fatores humanos: hesitação, disciplina operacional, clareza de papéis e familiarização de toda a população a bordo. (Fontes: `anp-eec7f988e9eeea4ece5e1b8d:p24-27:17.0-10.0`, `anp-dabfb60617e4f0ede433578e:p237-242:20.0-15.0`, `anp-dabfb60617e4f0ede433578e:p269-272:16.0-16.0`, `petroles-004c2afadba7ea17c7dd7908:pNone:2449364.0-2449410.0`, `petroles-004c2afadba7ea17c7dd7908:pNone:508283.0-508329.0`, `petroles-004c2afadba7ea17c7dd7908:pNone:3234448.0-3234479.0`)