# SIMOPS em FPSOs/FSOs: emergência, interrupção segura e retomada

## 1. Finalidade e recorte técnico

Em operações simultâneas (SIMOPS), a resposta a condições anormais não pode ser tratada como problema isolado de uma única tarefa. Uma perda de contenção, detecção de gás, falha de barreira, atuação de ESD, despressurização inesperada, indisponibilidade de proteção contra incêndio ou alteração emergencial de lógica de controle pode invalidar a base de risco de várias atividades que ocorrem ao mesmo tempo.

Sob a ótica de segurança de processo, os procedimentos operacionais devem definir limites de operação segura, sequências de parada normal e emergencial, consequências de operar fora desses limites e ações requeridas nessas condições. Além disso, mudanças e retomadas após anormalidades exigem análise de risco e revisão de segurança pré-partida, e não apenas a liberação informal do retorno ao trabalho. Em SIMOPS, isso significa reavaliar o conjunto das interfaces entre produção, manutenção, resposta a emergência, marine, offloading, intervenções, testes e atividades em áreas classificadas.

Este documento consolida lições técnicas extraídas de alertas de segurança, relatórios de auditoria/investigação e um anexo conceitual de gestão de segurança de processo. Não constitui procedimento certificado nem substitui requisitos internos da instalação.  
**Fontes:** `regis-161cd3328a094e3a98a6fa18:pNone:5493.0-5862.0`, `anp-ac72dc113a17b403b32f806c:p1-3:0.0-19.0`, `anp-13a33bb67429b09d3272c53e:p1-4:0.0-0.0`

## 2. Condições anormais que exigem reavaliação imediata das SIMOPS

Os materiais analisados mostram que certas anormalidades devem disparar reavaliação imediata da continuidade das atividades simultâneas, porque afetam diretamente as barreiras ou elevam o potencial de escalonamento:

- **Perda de contenção de hidrocarbonetos ou fluidos perigosos**, inclusive vazamentos em linha de gas-lift, em sistemas de offloading, flanges, risers e linhas críticas.
- **Detecção confirmada de gás ou atmosfera inflamável**, especialmente em ambiente confinado ou de ventilação limitada. O caso do FPSO Cidade de São Mateus mostra que a permanência de equipes e a mobilização de novas frentes de trabalho com indicação de gás muito alto/LIE elevado representam degradação crítica da condição operacional.
- **Atuação, não atuação ou indisponibilidade de sistemas de ESD, fogo e gás, dilúvio, bombas de incêndio e válvulas automáticas**. A falha de detecção e a demora para interromper vazamento agravaram evento com incêndio após ruptura de linha de gas-lift.
- **Aberturas/fechamentos de válvulas e despressurizações que alterem significativamente o regime de pressão**, sobretudo em partida/repartida. No caso de gas-lift, a combinação de blowdown inadequado, check valves sem estanqueidade e reabertura de SDV sem avaliação de pressão contribuiu para golpe de aríete e ruptura.
- **Barreiras críticas degradadas ou fora de operação**, como PPCI, SDVs, ADV de dilúvio, bombas de incêndio ou linhas críticas com reparos temporários inadequados.
- **Mudanças emergenciais na lógica de proteção ou derrotas de causa e efeito** para manter produção/ventilação/energia sem análise de risco formal.
- **Perda de monitoramento confiável** da operação, como offloading sem vigilância adequada no lado do FPSO ou falha de monitoramento por câmera.
- **Incerteza documental relevante**, por exemplo P&IDs que não representam o arranjo real, dificultando a identificação do ponto de vazamento, isolamentos existentes ou presença de raquetes/blindagens.

Em SIMOPS, a consequência prática é que a autorização vigente de um trabalho deixa de ser suficiente se a condição de contorno mudou. A continuidade só é defensável quando a nova condição anormal foi analisada, as barreiras remanescentes foram verificadas e a autoridade competente redefiniu os limites de operação.  
**Fontes:** `anp-dabfb60617e4f0ede433578e:p25-27:16.0-26.0`, `anp-ac72dc113a17b403b32f806c:p1-3:0.0-19.0`, `anp-13a33bb67429b09d3272c53e:p1-4:0.0-0.0`, `anp-ac2e4f9942314aa203e5b9b3:p29-31:25.0-37.0`

## 3. Critérios técnicos para interrupção segura

### 3.1 Princípio decisório

A interrupção segura em SIMOPS deve ser orientada pelo estado das barreiras, e não apenas pela intenção operacional de concluir uma tarefa ou retomar a produção. Os textos da ANP sobre elementos críticos e contingência deixam claro que, quando equipamento ou sistema crítico de segurança operacional estiver degradado ou fora de operação, o operador deve adotar medidas temporárias equivalentes, podendo incluir:

- implantação de controles alternativos equivalentes;
- redução e limitação da produção;
- isolamento e parada de equipamentos, sistemas ou instalações.

Há um ponto particularmente forte nos achados de auditoria: quando uma recomendação técnica de inspeção for crítica e a correção for imediata, a concessão de prazo só seria aceitável se o elemento fosse colocado fora de operação; mantê-lo operando configura risco grave e iminente. Esse raciocínio é diretamente aplicável a SIMOPS: não se deve manter atividades simultâneas apoiadas em barreiras degradadas sem contingência robusta e aprovada.  
**Fontes:** `anp-35714b541d23cdf8fe609d5b:p2-4:16.0-12.0`, `anp-ac2e4f9942314aa203e5b9b3:p29-31:25.0-37.0`

### 3.2 Gatilhos práticos de parada/suspensão

Com base nos casos analisados, são gatilhos fortes para suspender parcial ou totalmente SIMOPS na área/sistema afetado:

1. **Gás detectado em nível incompatível com permanência e execução de serviço**, sobretudo se houver ingresso em espaço/volume confinado, uso de ferramentas, equipamentos não Ex ou movimentação de pessoas.
2. **Perda de contenção sem ponto de vazamento claramente identificado e isolado**.
3. **Atuação de ESD ou necessidade de ESD não efetivada**, incluindo situações em que a resposta emergencial demora a interromper a liberação.
4. **Necessidade de derrotar lógica de segurança para manter produção ou utilidades**, sem gestão de mudança e análise de risco apropriadas.
5. **Barreiras de incêndio/explosão indisponíveis ou degradadas**, como detecção, dilúvio, bombas, PPCI ou SDVs fora do desempenho requerido.
6. **Operação de transferência/offloading sem salvaguardas automáticas e sem vigilância adequada**, diante de anomalia de pressão, falha do QRF/IHTP ou perda de monitoramento local.
7. **Teste, intervenção ou pressurização com energia acumulada significativa**, quando o isolamento e a segregação frente a outras atividades não forem mais garantidos.

Esses gatilhos não implicam que toda a unidade sempre deva parar; porém exigem, no mínimo, congelar a autorização anterior, recentralizar a decisão no comando operacional/emergencial e redefinir escopo, área, pessoas expostas e permissões.  
**Fontes:** `anp-dabfb60617e4f0ede433578e:p25-27:16.0-26.0`, `anp-13a33bb67429b09d3272c53e:p1-4:0.0-0.0`, `anp-28ecd3b4b0e4434d9511c613:p1-4:0.0-3.0`, `anp-ac72dc113a17b403b32f806c:p1-3:0.0-19.0`, `anp-35714b541d23cdf8fe609d5b:p2-4:16.0-12.0`

## 4. Resposta à emergência durante SIMOPS: lições operacionais

### 4.1 Não degradar ainda mais as barreiras

Uma lição central dos eventos analisados é que, em condição anormal, a resposta não pode enfraquecer as próprias salvaguardas do sistema. O caso do FPSO Cidade de São Mateus ilustra más decisões operacionais durante um vazamento com gás detectado:

- tentativa de identificar e reparar em campo sem restabelecer condição segura;
- envio de novas equipes ao local com detecção perigosa de gás;
- autorização de limpeza e preparação de reparo sem controle efetivo da atmosfera;
- reversão de ação automática da matriz de causa e efeito para manter funcionamento normal de ar condicionado/painéis, contrariando a lógica projetada;
- desmobilização parcial de pontos de reunião antes da eliminação do perigo;
- ingresso com materiais/ferramentas potencialmente inadequados à atmosfera existente.

Para SIMOPS, a implicação é direta: diante de emergência ou quase-emergência, a prioridade passa a ser controlar a fonte, proteger pessoas e preservar as funções críticas de detecção, isolamento, despressurização, ventilação de segurança, combate a incêndio e evacuação. Medidas voltadas primariamente à continuidade operacional devem ser subordinadas a essa lógica.  
**Fontes:** `anp-dabfb60617e4f0ede433578e:p25-27:16.0-26.0`, `anp-ac72dc113a17b403b32f806c:p2-3:19.0-25.0`, `anp-35714b541d23cdf8fe609d5b:p1-3:0.0-21.0`

### 4.2 Isolamento, despressurização e energia

Os casos mostram que a sequência de parada e retomada importa. No evento de gas-lift, a abertura de BDV sem necessidade, associada à falta de estanqueidade de check valves, favoreceu despressurização do coletor e criou condição para golpe de aríete na retomada. Assim, durante SIMOPS:

- isolar e despressurizar são ações essenciais, mas devem seguir a filosofia de projeto e os procedimentos;
- despressurização inadequada pode criar novos riscos para a retomada;
- válvulas de bloqueio, check valves, SDVs e BDVs precisam ter integridade e lógica coerentes com o cenário;
- fechamento local/manual deve ser viável e a equipe precisa ser treinada para isso.

No teste hidrostático de riser, a produção já estava parada e o riser isolado antes do ensaio; o próprio relato indica que, se a ruptura tivesse ocorrido com produção em curso, o inventário e o tempo de resposta de ESD poderiam agravar muito as consequências. Isso reforça que certas atividades energizadas/testes devem ser segregadas de outras operações incompatíveis.  
**Fontes:** `anp-ac72dc113a17b403b32f806c:p1-3:0.0-19.0`, `anp-ac72dc113a17b403b32f806c:p2-3:19.0-25.0`, `anp-28ecd3b4b0e4434d9511c613:p1-4:0.0-3.0`

### 4.3 Controle de ignição e áreas classificadas

Na ocorrência de gas-lift com incêndio, um contêiner refrigerado não ATEX em área classificada foi apontado como fonte de ignição mais provável. Em ambiente SIMOPS, isso significa que a resposta à anormalidade deve incluir checagem imediata de:

- equipamentos temporários ou móveis instalados na área;
- conformidade Ex/ATEX de equipamentos em atmosfera potencialmente explosiva;
- validade e execução da manutenção dos equipamentos Ex;
- permanência de ferramentas/equipamentos trazidos para inspeção, limpeza ou reparo emergencial.

A emergência não suspende o controle de ignição; ao contrário, ele se torna mais crítico.  
**Fontes:** `anp-ac72dc113a17b403b32f806c:p1-3:0.0-19.0`, `anp-ac72dc113a17b403b32f806c:p2-3:19.0-25.0`

## 5. Retomada das atividades após interrupção ou emergência

A retomada segura em SIMOPS não é simples “volta ao normal”. Ela deve comprovar que a base de segurança foi restaurada ou formalmente redefinida.

### 5.1 Condições mínimas para retomada

Dos materiais analisados, sobressaem os seguintes requisitos técnicos:

- **Revisão de segurança pré-partida/repartida** antes do retorno da operação, especialmente após parada de emergência, despressurização, mudança de configuração ou intervenção relevante.
- **Verificação do estado das pressões e do alinhamento do sistema** antes de reabrir SDVs ou restabelecer fluxo, para evitar transientes perigosos.
- **Confirmação de disponibilidade e desempenho das barreiras**: fogo e gás, ESD, dilúvio, bombas de incêndio, ADVs, SDVs, PPCI, ventilação e contenção primária.
- **Restauração da condição de projeto ou implantação formal de contingências equivalentes**, quando houver degradação de elemento crítico.
- **Atualização de análise de riscos/HAZOP/Gestão de Mudança**, quando a retomada ocorrer após alteração de arranjo, remoção de salvaguarda, mudança de procedimento ou urgência operacional.
- **Documentação técnica confiável e coerente com o arranjo real**, inclusive desenhos, TAGs, lista de pendências impeditivas e condições de isolamento.
- **Treinamento e competência específicos** para tarefas críticas de fechamento de válvulas, partida, offloading e resposta à emergência.
- **Monitoramento adequado da operação retomada**, incluindo vigilância local quando necessário, e não apenas confiança em monitoração remota falha.

No caso de offloading, a urgência na retomada contribuiu para ausência de atualização de HAZOP após remoção de salvaguarda de bloqueio por baixa pressão; além disso, faltou previsão do cenário de vazamento por falha espúria do QRF. Logo, retomadas “rápidas” que suprimem revisão de risco tendem a reintroduzir o evento.  
**Fontes:** `anp-ac72dc113a17b403b32f806c:p2-3:19.0-25.0`, `anp-13a33bb67429b09d3272c53e:p1-4:0.0-0.0`, `regis-161cd3328a094e3a98a6fa18:pNone:5493.0-5862.0`, `anp-ac2e4f9942314aa203e5b9b3:p29-31:25.0-37.0`

### 5.2 Barreira degradada: retomar ou manter parado?

Os alertas e auditorias indicam um critério robusto: se a barreira crítica está degradada, ausente, fora de especificação ou sem teste/desempenho demonstrado, a retomada só pode ocorrer com justificativa técnica, contingência aprovada e compatibilidade com o risco. Isso vale para PPCI, sistemas de dilúvio, ADVs, bombas de incêndio, SDVs e linhas críticas.

Exemplos práticos dos achados:

- PPCI ausente/degradada sem medida compensatória adequada não sustenta retorno à condição normal de risco.
- Testes de dilúvio aprovados sem registro de vazão/pressão, ou com desempenho abaixo do projeto, enfraquecem a evidência de prontidão da barreira.
- Recomendação de inspeção crítica não implementada não deve conviver com continuidade operacional do elemento afetado.

Portanto, em SIMOPS, a retomada parcial pode até ser possível em algumas áreas/sistemas, mas não deve se apoiar em presunções vagas de que “a barreira deve funcionar”; é preciso evidência, contingência ou indisponibilização do elemento/sistema.  
**Fontes:** `anp-35714b541d23cdf8fe609d5b:p1-3:0.0-21.0`, `anp-35714b541d23cdf8fe609d5b:p2-4:16.0-12.0`, `anp-ac2e4f9942314aa203e5b9b3:p29-31:25.0-37.0`

## 6. Registro das decisões, desvios e lições aprendidas

O registro técnico da interrupção e da retomada é parte do controle de risco, não mera formalidade administrativa. Os materiais apontam repetidamente falhas de rastreabilidade, de gestão de mudança, de implementação de recomendações e de documentação do arranjo real. Para SIMOPS, o registro mínimo deve capturar:

- evento deflagrador da suspensão/interrupção;
- horário, alarmes, leituras relevantes de gás, pressão, vazão e estado do processo;
- atividades simultâneas afetadas e decisão sobre suspensão total, parcial ou re-sequenciamento;
- autoridade que decidiu, base técnica utilizada e restrições impostas;
- estado das barreiras críticas e qualquer inibição, bypass, derrota de causa e efeito ou indisponibilidade temporária;
- isolamentos aplicados, PT/certificados envolvidos e relação com manutenção/intervenção/teste;
- contingências implementadas, prazo, responsável e critérios de expiração;
- verificações para retomada, inclusive revisão pré-partida e testes/inspeções executados;
- modificações em procedimentos, HAZOP, treinamento, inspeção e manutenção;
- lições aprendidas e disseminação para ativos/instalações similares.

A rastreabilidade é especialmente relevante em transições entre operadores, em pendências de inspeção (RTI), em documentação de fornecedor incompleta e em mudanças de configuração feitas sob pressão para retomar a operação.  
**Fontes:** `anp-ac72dc113a17b403b32f806c:p1-3:0.0-19.0`, `anp-13a33bb67429b09d3272c53e:p1-4:0.0-0.0`, `anp-35714b541d23cdf8fe609d5b:p2-4:16.0-12.0`, `anp-28ecd3b4b0e4434d9511c613:p1-4:0.0-3.0`

## 7. Síntese aplicada à decisão em SIMOPS

Em condição anormal durante SIMOPS, a boa decisão técnica tende a seguir esta lógica:

1. **Reconhecer que a base de risco mudou** e congelar a autorização anterior.
2. **Preservar vidas e barreiras**, em vez de priorizar continuidade operacional.
3. **Suspender atividades incompatíveis** com a nova condição de risco.
4. **Isolar, despressurizar e controlar fontes de ignição** conforme filosofia de projeto e procedimentos.
5. **Não derrotar salvaguardas** sem análise de risco formal, aprovação e registro.
6. **Verificar se barreiras críticas estão disponíveis e independentes**; se não estiverem, implantar controles equivalentes ou manter indisponível/parado.
7. **Só retomar após revisão técnica de partida/repartida**, validação das pressões/configurações, atualização documental e definição explícita de quem aprova a retomada.

Os casos analisados mostram que emergências em FPSOs não são agravadas apenas pela falha inicial, mas também por retomadas apressadas, monitoramento insuficiente, lógica de proteção enfraquecida, barreiras degradadas e decisões pouco rastreáveis.  
**Fontes:** `anp-dabfb60617e4f0ede433578e:p25-27:16.0-26.0`, `anp-ac72dc113a17b403b32f806c:p1-3:0.0-19.0`, `anp-ac72dc113a17b403b32f806c:p2-3:19.0-25.0`, `anp-13a33bb67429b09d3272c53e:p1-4:0.0-0.0`, `anp-35714b541d23cdf8fe609d5b:p2-4:16.0-12.0`, `anp-ac2e4f9942314aa203e5b9b3:p29-31:25.0-37.0`