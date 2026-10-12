# Ciclo de vida dos estudos de segurança em FPSOs

## 1. Função dos estudos de segurança ao longo da vida da unidade

A gestão de riscos em um FPSO depende de um processo contínuo de **identificação de perigos, análise de riscos e gerenciamento das medidas de controle ao longo de toda a vida útil da instalação**. No material fornecido, o **Safety Case** aparece como o documento integrador dessa lógica: ele é produzido pelo operador para demonstrar que os perigos relevantes foram identificados, os riscos foram avaliados, as medidas de controle foram adotadas e o risco foi reduzido a nível **ALARP** (*as low as reasonably practicable*, isto é, tão baixo quanto razoavelmente praticável, considerando a desproporção entre custo adicional de redução e benefício obtido). Além disso, o Safety Case deve descrever o sistema de gestão que assegura a aplicação consistente desses controles.

Isso é importante porque os estudos de segurança não devem ser tratados como entregáveis isolados de projeto. Eles formam um **conjunto articulado de análises** que sustenta decisões de engenharia, operação, manutenção, resposta a emergências e gestão de mudanças. No material analisado, o manual de implementação do Safety Case afirma que o escopo se aplica a **novos projetos, conversões, modificações e aprimoramentos em unidades e embarcações existentes**, e que o Safety Case é baseado em estudos formais como HAZID, HAZOP, HEMP, FEA, ETRERA, ESSA e QRA, entre outros.

**Rastreabilidade da seção:** `anp-dabfb60617e4f0ede433578e:p68-70:16.0-32.0`, `anp-dabfb60617e4f0ede433578e:p69-72:23.0-19.0`

## 2. Planejamento do pacote de estudos na fase de projeto e conversão

O material da ANP sobre o FPSO Cidade de São Mateus mostra, como exemplo concreto, um pacote de estudos elaborado ainda na fase de projeto/conversão. Entre os estudos listados constavam:

- **Layout Review Report**
- **HAZID Study**
- **Ship/Marine Systems HAZOP**
- **Topside/Process HAZOP**
- **QRA**
- **Exhaust Dispersion Study**
- **Non-Hydrocarbon Hazard Analysis (NHHA)**
- **CFD Gas Dispersion Modeling for Gas Detector Location**
- **Thermal Radiation and Gas Dispersion Study for Flare and Vent**
- **Fire and Explosion Assessment (FEA)**
- **Escape, Temporary Refuge, Evacuation and Rescue Analysis (ETRERA)**
- **Fire Propagation and Structural Protection Analysis**
- **Emergency Systems Survivability Analysis (ESSA)**

Esse conjunto ilustra um ponto essencial para o planejamento dos estudos: **cada técnica responde a uma parte do problema de segurança**, e o valor do pacote está na cobertura combinada das interfaces entre processo, casco/sistemas marinhos, dispersão, fogo/explosão, sobrevivência dos sistemas de emergência, refúgio e evacuação.

Do ponto de vista profissional, o planejamento do ciclo de vida desses estudos deve considerar pelo menos:

1. **Definição de escopo por fase do empreendimento**: projeto conceitual, detalhamento, conversão/construção, comissionamento, início de operação, operação madura, modificações, envelhecimento e desativação.
2. **Definição das bases de análise**: descrição da unidade, filosofia operacional, P&IDs, arranjo geral, condições de processo, sistemas marinhos, hipóteses de armazenamento/transferência, inventários e interfaces com utilidades e emergência.
3. **Sequenciamento lógico**: estudos qualitativos e de identificação de perigos tendem a preceder estudos quantitativos e de detalhamento, porque fornecem cenários, hipóteses e casos base.
4. **Definição de participantes**: o caso analisado mostra participação de áreas como Produção, Manutenção, Marinha, Utilidades e HSE; isso reforça o caráter multidisciplinar necessário à revisão e à validação.
5. **Critérios de interface**: resultados de um estudo devem alimentar os demais. Por exemplo, premissas de inventário, ventilação, detecção, ocupação, armazenamento e rotas de fuga não podem divergir entre análises correlatas.

Em termos práticos, o erro de planejamento mais crítico não é apenas “não fazer um estudo”, mas **não planejar a integração entre estudos que compartilham premissas**.

**Rastreabilidade da seção:** `anp-dabfb60617e4f0ede433578e:p69-72:23.0-19.0`, `anp-dabfb60617e4f0ede433578e:p167-170:12.0-23.0`

## 3. Revisão no encerramento do projeto e no início da operação

O material indica um requisito particularmente relevante para a transição entre projeto e operação: o **HAZOP preparado durante o detalhamento deve ser revisto no início da fase operacional, considerando os “as built” dos P&IDs, com participação do pessoal de operação**. Além disso, o HAZOP deve continuar sendo revisto para incorporar mudanças de projeto feitas durante a operação.

Essa exigência tem implicações técnicas importantes:

- o estudo de projeto não é automaticamente válido para a operação real;
- mudanças ocorridas na construção, conversão, comissionamento e partida podem invalidar premissas originais;
- a participação da operação é necessária para confrontar a engenharia prevista com a prática operacional efetiva;
- a validação contra documentação “as built” é uma condição mínima para que o estudo continue servindo de base a decisões.

O caso investigado pela ANP mostra que **não foi possível evidenciar a revisão do Safety Case ao final da fase de projeto**, embora essa revisão pudesse ter identificado mudanças significativas de premissas operacionais definidas ainda durante a conversão. A lição técnica é clara: a passagem de fase não deve ser tratada como mera formalidade documental; ela é um ponto de **revalidação das bases de risco**.

**Rastreabilidade da seção:** `anp-dabfb60617e4f0ede433578e:p169-172:5.0-10.0`, `anp-dabfb60617e4f0ede433578e:p167-170:12.0-23.0`

## 4. Gatilhos de revisão, atualização e revalidação durante a operação

O material mostra dois mecanismos complementares de revisão:

### 4.1 Revisão periódica

No procedimento citado para o caso da BW, a revisão do Safety Case deveria ocorrer **no máximo cinco anos após o primeiro óleo**. Esse exemplo evidencia a utilidade de um ciclo periódico formal para evitar obsolescência dos estudos.

### 4.2 Revisão motivada por mudança ou perda de validade das premissas

Mais importante que a periodicidade isolada é o princípio de validade da análise. O material cita entendimento técnico segundo o qual uma análise de riscos só é válida como base para decisão quando permanecem válidas as suas bases: **método, modelos, dados de entrada, premissas e limitações**. Qualquer desvio dessa base deve disparar uma avaliação de impacto sobre o risco e/ou sobre a validade dos resultados.

Também é citado que a identificação de perigos e a avaliação de riscos podem precisar ser revistas e atualizadas quando surgem **novas situações significativas** ou quando são feitas **mudanças significativas na instalação**.

No procedimento da BW, aparecem como exemplos de temas que podem requerer revisão do Safety Case:

- mudanças de projeto;
- mudanças em parâmetros operacionais;
- alterações em elementos críticos de segurança;
- histórico de incidentes e eventos anormais;
- novos conhecimentos e compreensões;
- mudanças em padrões de segurança;
- mudanças na gestão de segurança e em fatores humanos que afetem a instalação;
- questões de **vida útil ligadas à fadiga e corrosão do topside e do casco**.

Além disso, para decidir se uma revisão do Safety Case é requerida, o procedimento previa a realização de **HAZID e HAZOP focalizados nas áreas alteradas**, com documentação da decisão de revisar ou não revisar.

Em síntese, o ciclo de vida dos estudos deve combinar:

- **revisão periódica programada**;
- **revisão orientada por MOC**;
- **revisão por mudança de fase**;
- **revisão por envelhecimento/degradação**;
- **revisão após incidentes, quase-acidentes ou novos conhecimentos**.

**Rastreabilidade da seção:** `anp-dabfb60617e4f0ede433578e:p167-170:12.0-23.0`, `anp-dabfb60617e4f0ede433578e:p169-172:5.0-10.0`

## 5. Adequação do escopo de revisão: o problema central não é revisar “algo”, mas revisar “o conjunto certo”

O caso CDSM é especialmente útil para mostrar um erro recorrente em FPSOs: executar uma revisão parcial sem capturar todas as análises impactadas pela mudança de premissas.

Segundo a investigação da ANP:

- a revisão dos estudos foi iniciada em 2014;
- o HAZOP foi o primeiro estudo a ser revisado;
- o Safety Case revisado ainda não havia sido emitido até a data do acidente;
- a revisão em curso **não contemplava todos os estudos afetados por mudanças de premissa**.

O exemplo mais forte foi a divergência entre a premissa documental e a operação real: o texto do HAZOP revisado do topside mencionava armazenamento de condensado junto com óleo cru em tanques de carga, enquanto a operação real era de **armazenamento de condensado puro** nos tanques. Apesar de essa mudança de premissa ter potencial impacto sobre o sistema de transferência de carga, **o HAZOP dos sistemas de transferência/carga não foi revisado**, permanecendo fora do escopo da revisão quinquenal. Outros estudos também ficaram fora do escopo previsto, como:

- **CFD Gas Dispersion Modeling for Gas Detector Location**
- **Fire Propagation and Structural Protection Analysis**

A implicação técnica é decisiva: quando muda uma premissa relevante, o gestor não deve perguntar apenas “qual estudo atualizar?”, mas sim:

1. **quais cenários foram alterados?**
2. **quais estudos usam essa premissa direta ou indiretamente?**
3. **quais recomendações anteriores deixam de ser plenamente válidas?**
4. **há impacto em detecção, combate, segregação, rotas de fuga, proteção passiva, ocupação, inventário, frequências, consequências ou resposta a emergências?**

Isso é gestão de interfaces entre análises. Uma revisão adequadamente planejada precisa evitar que o pacote final fique **internamente inconsistente**.

**Rastreabilidade da seção:** `anp-dabfb60617e4f0ede433578e:p167-170:12.0-23.0`, `anp-dabfb60617e4f0ede433578e:p169-172:5.0-10.0`

## 6. Aplicação dos resultados dos estudos no SGSO e na operação

Os estudos de segurança só cumprem sua função quando seus resultados são convertidos em ações de engenharia, operação, inspeção, manutenção e contingência. O alerta da ANP sobre proteção passiva contra incêndio (PPCI) mostra desvios típicos observados em unidades marítimas e ajuda a entender como as recomendações dos estudos devem ser tratadas na prática.

Entre os desvios citados no alerta estão:

- planos de inspeção e manutenção incompletos;
- adoção de solução alternativa sem fundamentação técnica equivalente ao grau de proteção originalmente previsto;
- implementação parcial de recomendação de estudo quantitativo sem devida demonstração técnica;
- instalação incompleta ou ausência de PPCI em pontos críticos;
- degradação avançada de proteções instaladas;
- ausência de controles alternativos equivalentes quando elemento crítico está degradado ou fora de operação;
- priorização de recomposição não compatível com o nível de risco.

À luz do SGSO citado no alerta, destacam-se consequências diretas para o ciclo de vida dos estudos:

### 6.1 Recomendações de análise de risco devem ser implementadas e rastreadas

O operador é responsável pela implementação das ações corretivas derivadas das análises de riscos e pela **documentação dessa implementação**. Se houver modificação na forma de implementação, ou rejeição de recomendação, a decisão deve ser **justificada**.

### 6.2 Medidas provisórias para elementos críticos degradados não dispensam base técnica

Quando equipamentos ou sistemas críticos de segurança operacional estiverem degradados ou fora de operação, devem existir **procedimentos de contingência** e controle formal. As medidas temporárias podem incluir, quando aplicável:

- controles alternativos equivalentes;
- redução ou limitação da produção;
- isolamento e parada de equipamentos, sistemas ou instalações.

### 6.3 Inspeção, teste e manutenção devem refletir os estudos de risco

Planos e procedimentos de inspeção, teste e manutenção devem buscar a integridade mecânica de sistemas, estruturas e elementos críticos e estar alinhados com recomendações de fabricantes, normas, padrões e boas práticas. Além disso, todos os equipamentos e sistemas críticos devem estar cobertos por esses planos.

Portanto, no ciclo de vida dos estudos, a etapa final não é a emissão do relatório: é a **absorção das conclusões no sistema de gestão**, com rastreabilidade até o encerramento técnico da recomendação.

**Rastreabilidade da seção:** `anp-35714b541d23cdf8fe609d5b:p2-4:16.0-12.0`

## 7. Governança, competência organizacional e suporte técnico para manter estudos válidos

O caso analisado pela ANP mostra que a manutenção da validade dos estudos depende de capacidade organizacional real, e não apenas de procedimentos escritos. A investigação apontou:

- forte dependência técnica da equipe local em relação a equipes no exterior;
- ausência de autonomia técnica local para temas ligados à segurança operacional;
- fragilidades em gerenciamento de mudanças, controle documental, atualização de desenhos, traduções e investigação de acidentes;
- ausência de estrutura local robusta de apoio de engenharia e segurança para suporte à operação.

Para o ciclo de vida dos estudos, isso tem impacto direto porque a revisão e a revalidação dependem de:

1. **acesso rápido a parâmetros de projeto e operação**;
2. **controle de versão e coerência documental**;
3. **capacidade de avaliar MOCs sem atraso excessivo**;
4. **suporte técnico para interpretar desvios, degradação e mudanças de premissas**;
5. **integração entre bordo e terra**.

Sem essa base, o risco não é apenas “atrasar um estudo”; é **continuar operando com análises formalmente existentes, porém materialmente desatualizadas**.

**Rastreabilidade da seção:** `anp-dabfb60617e4f0ede433578e:p68-70:16.0-32.0`

## 8. Envelhecimento, vida útil, modificações e desativação

O material fornecido associa explicitamente a revisão do Safety Case a temas de **vida útil, fadiga e corrosão do topside e do casco**. Isso é tecnicamente coerente com a lógica de FPSOs, especialmente em unidades convertidas ou já envelhecidas: a degradação física altera a confiabilidade de barreiras, a robustez estrutural, as hipóteses de disponibilidade e, potencialmente, a severidade ou a probabilidade de cenários acidentais.

Além disso, o alerta da ANP remete à prática de gestão do SGSO referente a **Projeto, Construção, Instalação e Desativação**, reforçando que a disciplina de segurança não se encerra na partida operacional. A consequência prática é que estudos de segurança devem permanecer adequados até a fase de desativação, o que inclui reavaliações quando houver:

- envelhecimento significativo de estruturas e equipamentos;
- mudanças de modo operacional;
- mudanças de inventário e de fluidos processados/armazenados;
- alterações físicas relevantes por retrofit, modificação ou reparo estrutural;
- redefinição de barreiras ou de estratégias de emergência;
- preparação para descomissionamento/desativação.

No material fornecido não há metodologia quantitativa detalhada para extensão de vida ou desativação; contudo, o conteúdo permite afirmar que **envelhecimento e mudança de condição operacional são gatilhos legítimos de revalidação dos estudos**.

**Rastreabilidade da seção:** `anp-dabfb60617e4f0ede433578e:p167-170:12.0-23.0`, `anp-35714b541d23cdf8fe609d5b:p2-4:16.0-12.0`

## 9. Critérios profissionais de boa prática derivados do material

Com base nos trechos analisados, um processo tecnicamente consistente para o ciclo de vida dos estudos de segurança em FPSOs deve contemplar:

1. **Pacote inicial de estudos formalmente planejado** na fase de projeto/conversão, com interfaces explícitas entre análises.
2. **Revisão na transição para a operação**, considerando documentação “as built” e participação da operação.
3. **Revisões periódicas formais**, sem substituir revisões motivadas por mudança.
4. **Mecanismo robusto de MOC**, capaz de identificar quais estudos e recomendações são afetados por cada alteração.
5. **Teste permanente de validade das bases da análise**: método, modelos, dados, premissas e limitações.
6. **Revisão por eventos de degradação e envelhecimento**, inclusive fadiga, corrosão e obsolescência de elementos críticos.
7. **Escopo completo de revisão**, cobrindo todos os estudos impactados e não apenas o documento mais visível.
8. **Rastreabilidade das recomendações até implementação, justificativa de desvios e encerramento técnico**.
9. **Integração com inspeção, manutenção, contingência e gestão de elementos críticos**, inclusive quando barreiras estiverem degradadas.
10. **Suporte organizacional e técnico suficiente** para manter os estudos vivos, coerentes e aplicáveis à operação real.

Em termos de avaliação profissional, a maturidade do processo não é demonstrada apenas pela existência de HAZID, HAZOP, QRA, FEA/FERA, ETRERA/EERA ou ESSA, mas pela capacidade de **planejar, revisar, revalidar, aplicar e manter coerente o conjunto das análises ao longo de todo o ciclo de vida da unidade**.

**Rastreabilidade da seção:** `anp-dabfb60617e4f0ede433578e:p69-72:23.0-19.0`, `anp-dabfb60617e4f0ede433578e:p167-170:12.0-23.0`, `anp-dabfb60617e4f0ede433578e:p169-172:5.0-10.0`, `anp-35714b541d23cdf8fe609d5b:p2-4:16.0-12.0`