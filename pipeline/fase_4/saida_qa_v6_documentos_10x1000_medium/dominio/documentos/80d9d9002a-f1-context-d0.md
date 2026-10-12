# Operação de custódia no offloading

## 1. Escopo técnico efetivamente coberto e limitações do material
O material fornecido permite compor, com boa base, um documento sobre **a operação de transferência de óleo do FPSO para o navio aliviador** sob a ótica de sequência operacional, salvaguardas, monitoramento, decisão de continuidade/parada e fatores que afetam a integridade da transferência. 

Por outro lado, **não há base suficiente nos trechos recebidos** para detalhar requisitos metrológicos específicos de **medição fiscal de óleo**, **medição fiscal de gás natural**, **incerteza de medição**, **proving/calibração**, **fatores de medidor**, **tratamento/validação de dados fiscais**, **equações de correção PVT** ou requisitos regulatórios específicos de medição da ANP. Assim, o texto abaixo se concentra naquilo que os trechos efetivamente sustentam: o **procedimento operacional de custódia durante o offloading**, especialmente no que toca a preparação, teste, transferência, interrupção segura e condições de confiabilidade operacional.  
**Fontes:** [`anp-13a33bb67429b09d3272c53e:p1-4:0.0-0.0`, `anp-13a33bb67429b09d3272c53e:p2-4:39.0-5.0`, `petroles-004c2afadba7ea17c7dd7908:pNone:3026005.0-3026061.0`, `petroles-4ee4bce16acf674505c8912d:pNone:2060884.0-2060913.0`, `regis-a895130239a6e9ec62837349:pNone:374.0-577.0`]

## 2. Conceito operacional de custódia no offloading
Na prática operacional do FPSO, o **offloading** é a operação em que o óleo armazenado nos tanques de carga é transferido para um navio aliviador, por meio das bombas de carga e do sistema de mangotes/conexões. Em termos de custódia, este é o momento em que a carga deixa o sistema de armazenamento da unidade e passa para a embarcação que seguirá a cadeia logística.

Os trechos mostram que essa operação não é apenas uma atividade de bombeio: ela é uma **sequência integrada de manobra naval, conexão mecânica, teste de estanqueidade, monitoração contínua e tomada de decisão operacional**. Portanto, a confiabilidade da custódia durante o offloading depende da integridade conjunta de:

- posicionamento relativo FPSO–navio aliviador;
- sistemas de conexão e desconexão;
- linha de transferência e mangotes;
- vigilância operacional durante todo o bombeio;
- resposta automática e humana a desvios;
- controle da condição do produto transferido.

Esse enquadramento é importante porque, mesmo quando o foco é a medição de transferência de custódia, a **validade operacional da transferência** depende da inexistência de vazamento, da confirmação de condição normal do sistema e da distinção entre óleo transferido e fluidos auxiliares usados na operação, como água de teste/deslocamento.  
**Fontes:** [`petroles-004c2afadba7ea17c7dd7908:pNone:409827.0-409878.0`, `petroles-004c2afadba7ea17c7dd7908:pNone:3026005.0-3026061.0`, `anp-13a33bb67429b09d3272c53e:p1-4:0.0-0.0`]

## 3. Sequência operacional da transferência e seus pontos críticos para a custódia
### 3.1 Fases da operação
Os trechos descrevem cinco fases principais da operação de offloading entre FPSO e navio aliviador:

1. **aproximação**;
2. **conexão**;
3. **transferência de carga**;
4. **desconexão**;
5. **afastamento**.

Na aproximação, o navio aliviador se posiciona com velocidade controlada, em modo *weather vane*, respeitando distância mínima do terminal/offloading station. Na conexão, ocorre a transferência progressiva dos cabos mensageiros, do sistema de amarração (*hawser*) e do mangote, até a conexão no *Bow Loading System* (BLS) do navio aliviador.  
**Fontes:** [`petroles-004c2afadba7ea17c7dd7908:pNone:3026005.0-3026061.0`, `petroles-004c2afadba7ea17c7dd7908:pNone:3025145.0-3025174.0`]

### 3.2 Teste de estanqueidade antes da transferência
Antes do início do bombeio de óleo, os trechos indicam a execução de **teste de estanqueidade da conexão com água** e a verificação da ocorrência de vazamentos. Esse passo é central para a custódia, porque a transferência só deve prosseguir quando a conexão mecânica e hidráulica estiver comprovadamente íntegra.

Do ponto de vista operacional, isso significa que a autorização para o início do bombeio não é apenas uma decisão de produção; ela é também uma decisão de **aceitação da integridade da rota de transferência**. Se houver indício de vazamento nessa etapa, a operação não está em condição confiável para caracterizar uma transferência válida e segura.  
**Fontes:** [`petroles-004c2afadba7ea17c7dd7908:pNone:3026005.0-3026061.0`]

### 3.3 Condição normal da linha e autorização de bombeio
Na fase de transferência, a sequência descrita é explícita: o navio aliviador deve **confirmar condição normal da green line** e, a partir disso, **autorizar o início de bombeio**, quando então o FPSO inicia a transferência de óleo.

Essa lógica operacional é relevante para custódia porque estabelece um **ponto formal de liberação da transferência**. Em termos práticos, o bombeio não deveria começar apenas porque a conexão física foi concluída; ele depende também de uma confirmação funcional de que a linha está em condição normal.  
**Fontes:** [`petroles-004c2afadba7ea17c7dd7908:pNone:3026005.0-3026061.0`]

### 3.4 Água no mangote, deslocamento e segregação operacional
Os trechos mostram que a água é usada em momentos específicos da operação:

- no **teste de estanqueidade da conexão**;
- no **envio da água no mangote para o navio aliviador**;
- ao final da transferência, quando o aliviador **bombeia a água de volta ao FPSO**, deslocando o óleo na linha de mangotes;
- essa água é então **recebida no tanque de slop** do FPSO.

Para a custódia, isso é tecnicamente importante porque evidencia que a operação envolve mais de um fluido na linha. Portanto, há necessidade operacional de distinguir:

- o volume efetivamente associado à carga de óleo;
- o conteúdo hidráulico do sistema de mangotes;
- a água de teste/deslocamento que deve retornar e ser destinada ao sistema adequado (slop).

Mesmo sem detalhamento metrológico nos trechos, a implicação operacional é clara: **não se deve confundir água de teste/deslocamento com óleo de carga transferido**.  
**Fontes:** [`petroles-004c2afadba7ea17c7dd7908:pNone:3026005.0-3026061.0`]

## 4. Salvaguardas que sustentam a confiabilidade da custódia durante o bombeio
### 4.1 Telemetria e parada automática das bombas
Os trechos de Petrolês informam que o sistema de telemetria de offloading do FPSO dispõe de automação para **parada automática das bombas de carga** quando a *green line* com o navio aliviador é quebrada. Nesse caso, o bombeio é interrompido e a transferência cessa após breve intervalo, com o objetivo de evitar derramamento contínuo de óleo para o mar.

Para a custódia, essa automação é uma barreira essencial. Ela não mede o óleo, mas protege a **integridade material da transferência**. Uma operação em que a linha se rompe sem interrupção rápida do bombeio compromete simultaneamente:

- a segurança operacional;
- a proteção ambiental;
- a confiabilidade do saldo transferido;
- a reconciliação de volumes entre origem e destino.

Em outras palavras, a continuidade da medição ou da contabilização só faz sentido se o sistema de transferência permanecer íntegro.  
**Fontes:** [`petroles-004c2afadba7ea17c7dd7908:pNone:3026005.0-3026061.0`]

### 4.2 Intertravamentos e bloqueio automático por alta/baixa pressão
O alerta da ANP recomenda verificar a existência de **intertravamento e bloqueio automático** no sistema de offloading, além de avaliar salvaguardas automáticas para situações de **alta e baixa pressão** e assegurar seu funcionamento. O mesmo alerta registra, como causa do evento investigado, a remoção de uma salvaguarda de bloqueio por baixa pressão sem adequada gestão de mudança e sem atualização correspondente do HAZOP.

Na ótica da custódia operacional, isso significa que a transferência não depende apenas da condição aparente do sistema, mas da manutenção das **camadas de proteção projetadas** para conter desvios de processo e de integridade mecânica. A perda dessas salvaguardas aumenta a probabilidade de transferência interrompida, vazamento e necessidade de invalidação ou revisão dos resultados operacionais da carga.  
**Fontes:** [`anp-13a33bb67429b09d3272c53e:p1-4:0.0-0.0`, `anp-13a33bb67429b09d3272c53e:p2-4:39.0-5.0`]

### 4.3 Dispositivos de desconexão rápida e seu papel ambivalente
Os trechos descrevem o uso de sistemas como **QRF (Quick Release Flange)**, IHTP e, no navio aliviador, o **BLS**, incluindo a possibilidade de **desconexão de emergência**. Esses dispositivos existem para reduzir consequências em cenários críticos; porém, o alerta da ANP mostra que eles próprios podem se tornar fonte de falha quando há modificação inadequada, documentação insuficiente, manutenção indefinida ou treinamento deficiente.

Logo, sob o ponto de vista da custódia, a desconexão rápida tem papel ambivalente:

- é uma **salvaguarda necessária** para limitar consequências em emergência;
- mas sua confiabilidade depende de projeto, posicionamento correto, inspeção, manutenção e entendimento operacional consistentes.

Uma desconexão espúria ou falha mecânica no conjunto de conexão transforma imediatamente a operação em evento de perda de integridade, interrompendo a validade operacional da transferência.  
**Fontes:** [`anp-13a33bb67429b09d3272c53e:p1-4:0.0-0.0`, `petroles-004c2afadba7ea17c7dd7908:pNone:3025145.0-3025174.0`]

## 5. Vigilância operacional contínua durante a custódia
O alerta da ANP aponta que o procedimento da instalação não previa vigilância na estação de offloading pelo lado do FPSO, diferentemente do padrão corporativo, e que também houve falha de monitoramento por câmera na estação de controle. Entre as lições aprendidas, a ANP recomenda rever treinamento, aplicar verificação de conformidade com procedimento (VCP) e assegurar sistemática de controle de treinamento.

Para a custódia, a consequência técnica é direta: a operação não pode ser tratada como mero bombeio remoto. A transferência requer **vigilância contínua local e remota**, porque o desvio crítico pode surgir no ponto físico de conexão, no mangote, no carretel, na pressão do sistema ou na relação geométrica entre as embarcações.

Assim, uma operação de custódia robusta no offloading deve ser entendida como atividade que exige, ao menos conceitualmente:

- confirmação de aderência ao procedimento vigente;
- observação contínua da estação de offloading;
- resposta pronta a indícios de vazamento, perda de pressão ou condição anormal da linha;
- clareza sobre responsabilidades entre operador e contratadas.

Esses elementos não substituem requisitos metrológicos, mas são pré-condições para que a transferência ocorra em base confiável.  
**Fontes:** [`anp-13a33bb67429b09d3272c53e:p1-4:0.0-0.0`, `anp-13a33bb67429b09d3272c53e:p2-4:39.0-5.0`]

## 6. Condição do produto transferido: implicações operacionais de BS&W e armazenamento
Os trechos de processo indicam que o óleo enviado aos tanques de carga do FPSO deve atender a um limite de **BS&W** (água e sedimentos). Em situação normal, espera-se que o óleo encaminhado aos tanques já esteja abaixo do limite de especificação definido; contudo, o texto também registra que podem ocorrer situações em que o óleo entra nos tanques com BS&W um pouco acima da especificação, sem que isso necessariamente inviabilize o envio posterior, porque o tanque de carga atua como grande separador gravitacional óleo-água ao longo do tempo de residência. No momento do offloading, é comum observar BS&W menor do que o medido quando o óleo entrou no tanque.

Para a operação de custódia, esse ponto tem três implicações relevantes:

1. **a condição do óleo transferido depende do histórico de armazenamento**, não apenas da condição instantânea na saída do tratamento;
2. **o tanque de carga participa indiretamente da qualidade da carga transferida**, pela decantação adicional de água;
3. em termos operacionais, a avaliação da carga para offloading deve considerar que o produto no tanque pode estar em condição diferente da observada no momento de sua entrada.

Esse raciocínio é útil para entendimento da carga, mas não deve ser exagerado: o trecho descreve um comportamento operacional observado em FPSOs, e não uma regra universal de aceitação de qualidade ou de medição.  
**Fontes:** [`petroles-4ee4bce16acf674505c8912d:pNone:2060884.0-2060913.0`]

## 7. Variáveis ambientais e de posicionamento que condicionam a continuidade da custódia
Os trechos descrevem que FPSOs podem dispor de sensores de:

- vento;
- ondas por radar;
- corrente por ADCP;
- referência vertical da embarcação.

Segundo o texto, esses dados são usados para avaliar operações de offloading. Também se registra que, na análise de risco, **as condições ambientais e a forma de amarração influenciam significativamente o perfil de risco** da operação, cuja duração típica pode se estender por cerca de 24 horas. Como as condições ambientais podem mudar durante esse período, o risco não é estático; por isso, a decisão de manter a operação ou proceder a desconexão de emergência deve ser continuamente reavaliada.

Na ótica da custódia operacional, isso significa que a transferência tem um **envelope de continuidade** condicionado por fatores externos. Portanto:

- a autorização inicial de bombeio não elimina a necessidade de reavaliação durante a operação;
- mudanças de vento, onda e corrente podem degradar a condição relativa entre FPSO e aliviador;
- a forma de amarração e a capacidade de posicionamento do aliviador alteram a exposição a falha, colisão ou perda de conexão;
- uma operação de custódia segura inclui critério claro de interrupção quando o perfil de risco se deteriora.

Esses aspectos são especialmente relevantes em operações com navios aliviadores dotados de **posicionamento dinâmico (DP)** e **BLS**, nas quais a possibilidade de desconexão de emergência é parte intrínseca do conceito operacional.  
**Fontes:** [`petroles-004c2afadba7ea17c7dd7908:pNone:3026005.0-3026061.0`, `petroles-004c2afadba7ea17c7dd7908:pNone:3025145.0-3025174.0`, `regis-a895130239a6e9ec62837349:pNone:374.0-577.0`]

## 8. Falhas organizacionais que comprometem a custódia durante o offloading
O alerta da ANP é particularmente útil para mostrar que falhas de custódia operacional não decorrem apenas de equipamento. As causas identificadas incluem:

- **gestão de mudança deficiente**;
- **HAZOP não atualizado** após modificação relevante;
- falhas de documentação do fornecedor;
- ausência de definição clara de responsabilidade de manutenção;
- falhas de treinamento especializado;
- ausência ou insuficiência de VCP;
- lacunas procedimentais de monitoramento;
- ausência de previsão de cenário de emergência específico.

Esses fatores têm efeito cumulativo. Em uma operação de transferência de custódia, eles podem produzir desvios como:

- liberação de bombeio em condição inadequada;
- incapacidade de identificar sinais precoces de perda de integridade;
- resposta tardia a vazamento ou baixa pressão;
- divergência sobre o estado funcional dos equipamentos de conexão;
- perda de rastreabilidade operacional do evento.

Portanto, o controle da custódia durante o offloading exige não só disciplina operacional em campo, mas também **governança técnica do sistema**: projeto revisado, salvaguardas mantidas, documentação coerente, manutenção atribuída e treinamento específico.  
**Fontes:** [`anp-13a33bb67429b09d3272c53e:p1-4:0.0-0.0`, `anp-13a33bb67429b09d3272c53e:p2-4:39.0-5.0`]

## 9. Referenciais de gestão e segurança citados no alerta ANP
O alerta menciona a **Resolução ANP nº 43/2007 (SGSO)** e associa o evento a práticas de gestão ligadas a:

- qualificação e treinamento necessários às atividades dos procedimentos operacionais;
- capacitação de contratadas nas práticas de trabalho seguro da instalação;
- atendimento a critérios de projeto e boas práticas de engenharia;
- identificação de normas, padrões e boas práticas relacionadas à segurança operacional;
- consideração dos riscos no projeto e em revisões subsequentes;
- identificação e análise de riscos;
- elaboração, documentação e controle de procedimentos operacionais com instruções claras e específicas;
- gestão de mudanças que possam afetar a segurança operacional, com avaliação prévia de perigos e impactos.

Embora esses itens não sejam, pelos trechos recebidos, requisitos específicos de metrologia fiscal, eles são diretamente aplicáveis à **robustez operacional da transferência de custódia**, pois definem a base de competência, mudança controlada, análise de risco e aderência procedimental sem as quais o offloading fica vulnerável a falhas críticas.  
**Fontes:** [`anp-13a33bb67429b09d3272c53e:p1-4:0.0-0.0`, `anp-13a33bb67429b09d3272c53e:p2-4:39.0-5.0`]

## 10. Síntese prática para avaliação profissional da operação de custódia no offloading
Com base apenas no material fornecido, uma avaliação profissional da operação de custódia durante o offloading em FPSO pode verificar se o operador compreende que:

- a transferência ocorre em fases e só deve avançar quando a fase anterior estiver íntegra;
- **teste de estanqueidade**, **verificação de vazamentos** e **confirmação de condição normal da green line** precedem o bombeio de óleo;
- a operação envolve também **água de teste/deslocamento**, que deve ser operacionalmente distinguida da carga de óleo;
- a **telemetria de offloading** e a **parada automática das bombas** quando a green line é perdida são barreiras centrais para preservar integridade da transferência;
- mudanças ambientais e limitações de posicionamento/amarras podem alterar o perfil de risco durante a operação e justificar interrupção ou desconexão de emergência;
- dispositivos de desconexão rápida são necessários, mas dependem de gestão de mudança, documentação, manutenção, treinamento e monitoramento adequados;
- a condição da carga no momento do offloading pode refletir o tempo de residência nos tanques e a evolução do BS&W;
- falhas organizacionais podem comprometer tanto a segurança quanto a confiabilidade operacional da custódia.

Em suma, o material recebido sustenta a visão de que a custódia no offloading não deve ser avaliada apenas como um problema de medição, mas como uma **operação integrada de transferência**, cuja validade depende de integridade mecânica, vigilância, salvaguardas automáticas, disciplina procedimental e decisão contínua frente ao risco.  
**Fontes:** [`anp-13a33bb67429b09d3272c53e:p1-4:0.0-0.0`, `anp-13a33bb67429b09d3272c53e:p2-4:39.0-5.0`, `petroles-004c2afadba7ea17c7dd7908:pNone:3026005.0-3026061.0`, `petroles-004c2afadba7ea17c7dd7908:pNone:3025145.0-3025174.0`, `petroles-4ee4bce16acf674505c8912d:pNone:2060884.0-2060913.0`, `regis-a895130239a6e9ec62837349:pNone:374.0-577.0`]