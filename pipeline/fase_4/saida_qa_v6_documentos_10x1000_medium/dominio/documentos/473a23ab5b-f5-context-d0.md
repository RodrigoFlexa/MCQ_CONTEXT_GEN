# Diagnóstico, integridade e proteção de separadores trifásicos

## 1. Escopo técnico e limite desta síntese
Este documento foca a operação de separadores trifásicos sob a ótica de **diagnóstico de baixo desempenho**, **integridade do vaso** e **atuação das salvaguardas de processo**. A cobertura é deliberadamente parcial: os trechos fornecidos sustentam melhor os temas de camadas de proteção, PSV, intertravamentos, inspeção/manutenção, revisão pré-operação, monitoramento e confiabilidade do que os detalhes de dimensionamento hidráulico do separador ou de eficiência de internos.

Em um FPSO, o separador trifásico é um vaso crítico porque combina:
- inventário relevante de hidrocarbonetos e água produzida;
- operação sujeita a transientes de vazão, pressão, composição e slugging;
- dependência forte de medição e controle de níveis, interface e pressão;
- interação direta com compressão de gás, tratamento de óleo, tratamento de água produzida e sistema de alívio.

Na prática, baixo desempenho de um separador trifásico costuma se manifestar como pelo menos um dos seguintes sintomas operacionais:
- carryover de líquido para a saída de gás;
- arraste de gás para as saídas líquidas;
- separação deficiente óleo/água;
- oscilação persistente de níveis ou da interface;
- perda de capacidade útil por espuma, sólidos, areia, incrustação ou dano de internos;
- acionamento frequente de alarmes, intertravamentos ou PSV.

**Fontes da seção:** `petroles-004c2afadba7ea17c7dd7908:pNone:4273983.0-4274025.0`, `petroles-004c2afadba7ea17c7dd7908:pNone:4274127.0-4274164.0`, `regis-74dd376119cbb653fe9922bc:pNone:34257.0-34687.0`

---

## 2. Camadas de proteção aplicáveis ao separador
Os trechos fornecidos descrevem uma hierarquia clássica de proteção de processo, plenamente aplicável a um separador trifásico:

1. **Projeto adequado** à capacidade, ao tipo de fluido e às condições operacionais esperadas.
2. **Malhas de controle** para manter o processo em região segura.
3. **Alarmes** para sinalizar desvios não corrigidos automaticamente.
4. **Intertravamentos** para executar ações automáticas de proteção, como fechamento de válvulas, parada de máquinas ou isolamento.
5. **PSV ou disco de ruptura** como última camada de prevenção/mitigação frente à sobrepressão.

Para separadores trifásicos, isso se traduz tipicamente em:
- controle de pressão do vaso na saída de gás;
- controle de nível total e, quando aplicável, da interface óleo-água;
- alarmes de pressão alta/baixa e nível alto/baixo;
- intertravamentos HH/LL capazes de isolar alimentação, reduzir carga ou iniciar shutdown;
- PSV protegendo o vaso quando as camadas anteriores forem insuficientes.

O ponto mais importante do material é que **PSV não substitui controle nem intertravamento**. Ela atua quando as camadas anteriores falham ou não conseguem devolver o processo à região segura. Em separadores sujeitos a slugging, espuma ou mal desempenho de controle, isso é crítico: o problema deve ser diagnosticado e tratado a montante da válvula de alívio, e não aceito como modo normal de operação.

**Fontes da seção:** `petroles-004c2afadba7ea17c7dd7908:pNone:4273983.0-4274025.0`, `petroles-004c2afadba7ea17c7dd7908:pNone:3236368.0-3236405.0`

---

## 3. Proteção contra sobrepressão: PSV, intertravamentos e limites práticos
Os trechos informam que a PSV é um dispositivo projetado para abrir quando a pressão do processo protegido excede a pressão de projeto em margem predeterminada. Também alertam para um aspecto relevante de operação e confiabilidade: **superdimensionamento não é automaticamente conservador**. Se a válvula for dimensionada para vazão muito superior àquela efetivamente descarregada em certos cenários, pode ocorrer **chatter**, isto é, abertura e fechamento rápidos, com dano à PSV e risco de ela deixar de cumprir sua função futura.

Para separadores trifásicos, isso tem implicações diretas:
- uma PSV mal selecionada pode proteger no papel, mas degradar em serviço real;
- cenários de alívio precisam considerar não só o inventário estático, mas também a dinâmica do vaso, dos controles e das correntes associadas;
- transientes com grande variação de vazão, flash, expansão de gás, espuma ou fechamento indevido de válvulas podem alterar fortemente a vazão efetiva de alívio.

O material também lista variáveis normalmente envolvidas no dimensionamento de PSV, sem trazer a equação completa: área requerida `A`, vazão requerida `W`, pressões de alívio e contrapressão `P1` e `P2`, fator de compressibilidade `Z`, relação de calores específicos `k`, peso molecular `M`, temperatura `T`, viscosidade e fatores de correção como `Kb`, `Kc`, `Kd`, `Kw` e `Kv`. Isso reforça que a proteção de sobrepressão depende de:
- natureza do fluido liberado;
- regime crítico ou não crítico do escoamento no alívio;
- contrapressão do sistema de flare/blowdown;
- viscosidade, compressibilidade e propriedade térmica na condição real de alívio.

Como apoio à engenharia de proteção, a simulação dinâmica é apresentada como ferramenta complementar ao HAZOP e útil para:
- estudo de partidas;
- sintonia de controladores;
- avaliação de cenários anormais e de acidente;
- comparação entre respostas dinâmicas e cálculos convencionais.

Em separadores trifásicos offshore, essa abordagem é especialmente útil quando o desempenho do vaso depende do acoplamento com manifold, compressor, tratador eletrostático, descarga de água produzida e lógica de shutdown.

**Fontes da seção:** `petroles-004c2afadba7ea17c7dd7908:pNone:4273983.0-4274025.0`, `petroles-004c2afadba7ea17c7dd7908:pNone:4273951.0-4274006.0`, `petroles-004c2afadba7ea17c7dd7908:pNone:4274127.0-4274164.0`

---

## 4. Diagnóstico de baixo desempenho do separador: abordagem estruturada

### 4.1 Princípio de diagnóstico
Para um separador trifásico, o diagnóstico eficaz precisa distinguir entre quatro classes de problema:

1. **Distúrbio de processo**: mudança de vazão, composição, slugging, formação de espuma, aumento de sólidos, variação de pressão a jusante.
2. **Perda de capacidade interna**: dano ou obstrução de internos, redução de volume útil, coalescência deficiente, acúmulo de areia/deposição.
3. **Falha de instrumentação/controle**: transmissores enviesados, linhas de impulso obstruídas, válvulas de controle travando, sintonia inadequada.
4. **Degradação mecânica ou de contenção**: corrosão, erosão, vibração, perda de espessura, vazamento, falha de conexões ou bicos.

O material utilizado ressalta a utilidade de **monitoramento, detecção e diagnóstico de falhas** e destaca benefícios como:
- simplificação do monitoramento por redução do número de variáveis/alarmes que exigem atenção do operador;
- detecção eficiente de desvios;
- diagnóstico com padrões distintos para diferentes falhas;
- necessidade de calibração periódica do modelo e dos parâmetros de controle conforme a condição real do processo.

Em um separador trifásico, essa lógica pode ser aplicada com base em tendências e correlação entre variáveis, por exemplo:
- pressão do vaso versus abertura da válvula de controle de gás;
- nível total e interface versus vazões de saída de óleo e água;
- aumento de DP em internos ou malhas associadas versus perda de capacidade;
- repetição de alarmes HH/LL sem coerência de processo versus possível defeito instrumental;
- oscilação simultânea de nível e pressão após mudanças de poço versus problema de transiente ou sintonia.

### 4.2 Sintomas práticos e pistas de causa

| Sintoma observado | Mecanismos prováveis | Verificações prioritárias |
|---|---|---|
| Líquido na linha de gás | nível alto real, espuma, demister danificado/cego, slug severo, controle de pressão agressivo | tendência de nível, DP ou inspeção do eliminador de névoa, histórico de slugging, abertura da PCV |
| Gás nas saídas líquidas | baixa pressão, vórtice em bocais, nível baixo, flashing, turbulência excessiva | pressão do vaso, estabilidade do nível, condição das tomadas de saída, regime de vazão |
| Óleo na água ou água no óleo acima do esperado | interface instável, emulsão, coalescência deficiente, internos degradados, residence time insuficiente por sobrecarga | leitura da interface, atuação da LCV, inspeção de internos, variação recente de composição/temperatura |
| Oscilação persistente de níveis | instrumento com erro, válvula de controle travando, sintonia ruim, slugs | calibração do transmissor, teste de curso da válvula, revisão de tuning, correlação com manifold/poços |
| Alarmes frequentes sem perda clara de especificação | alarme mal racionalizado, ruído de medição, desvio transitório tolerável, falha intermitente de instrumento | histórico de alarmes, histerese, filtragem, validação por variável redundante |
| Queda gradual de desempenho | incrustação, areia, corrosão sob depósito, espuma recorrente, dano lento de internos | inspeção, abertura programada, amostras de sólidos, análise de corrosão, revisão de química |

### 4.3 Uso de simulação dinâmica e monitoramento
A simulação dinâmica pode apoiar três decisões importantes no separador:
- diferenciar evento transitório aceitável de problema estrutural de controle;
- testar estratégias de partida, retomada e mudança de produção sem expor o vaso a upset real;
- estimar a consequência de falhas de válvulas, perda de utilidades ou mudanças abruptas de pressão a jusante.

A mensagem central dos trechos é que o diagnóstico não deve se apoiar apenas em observação pontual. Ele deve combinar:
- dados históricos;
- comportamento dinâmico das variáveis;
- validação de instrumentos;
- coerência entre causa provável, resposta do controle e atuação das salvaguardas.

**Fontes da seção:** `petroles-004c2afadba7ea17c7dd7908:pNone:4274127.0-4274164.0`, `petroles-004c2afadba7ea17c7dd7908:pNone:4014952.0-4014990.0`

---

## 5. Inspeção e integridade do vaso e de seus internos

### 5.1 Requisitos de gestão de integridade
Os trechos citando NR-30 e prática de gestão SGSO indicam que instalações e equipamentos de plataforma devem possuir **plano documentado de inspeção e manutenção**, contemplando no mínimo:
- equipamentos, máquinas e instalações sujeitos a inspeção/manutenção;
- tipos de intervenção;
- procedimentos de inspeção e manutenção;
- cronograma;
- identificação de responsáveis;
- quantidade, especialidade e capacitação dos trabalhadores;
- procedimentos de segurança;
- sistemas e equipamentos de proteção coletiva e individual.

A periodicidade de inspeções e intervenções deve considerar, no mínimo:
- recomendações normativas e técnicas aplicáveis;
- recomendações do fabricante, sobretudo nos itens críticos à segurança;
- relatórios de inspeção, investigação de acidentes e incidentes;
- análises de risco;
- condições ambientais agressivas;
- boas práticas de engenharia;
- notificações de autoridades competentes.

Também é destacado que as recomendações decorrentes das inspeções e manutenções devem ser **registradas e implementadas com prazo e responsável definido**.

### 5.2 Aplicação prática ao separador trifásico
Para um separador trifásico, o plano de integridade deve cobrir não só o casco do vaso, mas também itens que frequentemente explicam baixo desempenho sem perda de contenção imediata, como:
- bocais e regiões de impacto de entrada;
- interno de entrada e defletores;
- placas/coalescedores, chicanas, vertedores e dispositivos de calmaria;
- eliminador de névoa e seus suportes;
- drenos, linhas de areia, tomadas de amostragem e bocais de instrumentação;
- válvulas de controle, SDV/BDV associadas e linhas de alívio;
- linhas de impulso e instrumentos de nível, interface e pressão;
- suportes, soldas, nozzles e pontos suscetíveis a vibração.

Mesmo quando o vaso não está em risco imediato de ruptura, a perda de integridade desses componentes pode degradar fortemente a separação. Em outras palavras, **integridade mecânica e eficiência de processo são inseparáveis**.

### 5.3 Mecanismos de degradação relevantes
Um dos trechos fornecidos, embora trate de trocadores de calor, lista mecanismos plenamente úteis como referência de degradação física em equipamentos pressurizados:
- vibração excessiva;
- material inadequado;
- erosão por alta velocidade;
- corrosão;
- perda de espessura de parede.

Esses mecanismos são diretamente pertinentes a separadores, especialmente em:
- regiões de entrada com alta energia de impacto;
- partes baixas com água salina, areia e corrosão sob depósito;
- bocais sujeitos a jato bifásico/trifásico;
- internos finos ou suportes suscetíveis a erosão ou fadiga vibratória.

### 5.4 Desvios organizacionais que pioram o risco
Outro trecho relata, em diagnóstico de uma planta, ausência de evidências de padrões formais para inspeção/manutenção de itens críticos como:
- sistemas de emergência e parada;
- intertravamentos e alarmes;
- malhas de controle críticas.

Também registra ausência de evidência de **revisão de segurança na pré-operação** para instalações modificadas. Para separadores trifásicos em FPSO, essa lacuna é especialmente grave após mudanças como:
- alteração de faixa de produção dos poços;
- revamp de internos;
- mudança de filosofia de controle de interface;
- conexão de novos poços, risers ou equipamentos a jusante;
- alteração do sistema de flare ou de compressão.

Nesses casos, a integridade funcional precisa ser revista junto com a integridade mecânica.

**Fontes da seção:** `regis-74dd376119cbb653fe9922bc:pNone:34257.0-34687.0`, `petroles-004c2afadba7ea17c7dd7908:pNone:3236368.0-3236405.0`, `petroles-004c2afadba7ea17c7dd7908:pNone:2485043.60-2485070.0`

---

## 6. Intertravamentos, confiabilidade e política de testes
Um estudo de confiabilidade citado no material compara proteção tradicional por PSV com sistema de intertravamento, isoladamente e em conjunto com discos de ruptura. O estudo conclui que, **naquele caso específico**, o intertravamento isolado mostrou confiabilidade comparável à proteção por PSV se seguida uma política de teste/manutenção; e que o uso conjunto com disco de ruptura permitiu maior espaçamento entre alguns testes.

A lição útil para separadores trifásicos não é copiar os intervalos do estudo, e sim reconhecer três princípios:
- a confiabilidade real da proteção depende da **política de teste, manutenção e reparo**;
- intertravamento sem prova periódica pode degradar silenciosamente;
- combinação de camadas independentes pode aumentar a robustez da proteção, desde que cada uma cubra cenário relevante.

Assim, para um separador, devem receber atenção de prova funcional periódica:
- transmissores e chaves de pressão que iniciam shutdown ou isolamento;
- medição de nível/interface usada em HH/LL;
- válvulas finais de elemento de segurança, como SDV, BDV e válvulas de bloqueio associadas;
- lógica de intertravamento e alimentação do sistema;
- dispositivos passivos, como disco de ruptura, quando existentes.

A experiência citada também reforça que resultados de confiabilidade só fazem sentido quando vinculados a premissas explícitas de:
- intervalo de testes;
- duração de teste;
- tempo médio de reparo;
- arquitetura do sistema.

**Fontes da seção:** `regis-faabb54ebe90c9b03a141f67:pNone:151.0-234.0`, `regis-74dd376119cbb653fe9922bc:pNone:34257.0-34687.0`

---

## 7. Partida, modificação e análise de cenários anormais
Os trechos fornecidos posicionam a simulação dinâmica como ferramenta complementar ao HAZOP e suporte a:
- partida;
- sintonia de controladores;
- estudo de cenários de operação;
- avaliação de respostas do processo a perturbações.

Para separadores trifásicos, isso é valioso em situações como:
- retorno após parada com inventário residual desconhecido;
- reabertura de alimentação com gás aprisionado em saídas líquidas;
- mudança abrupta de contrapressão no gás por compressor indisponível;
- alteração de temperatura/composição que favoreça espuma ou emulsão;
- sequência de fechamento/abertura de válvulas que leve o vaso a sobrepressão ou inundação.

O material também sugere, por analogia metodológica, que sistemas de monitoramento de processo podem reduzir a sobrecarga de alarmes e orientar o operador para a causa provável do desvio, em vez de apenas indicar sintomas desconexos. Em separadores, isso é particularmente útil quando vários alarmes aparecem ao mesmo tempo durante slugging ou upset.

**Fontes da seção:** `petroles-004c2afadba7ea17c7dd7908:pNone:4274127.0-4274164.0`, `petroles-004c2afadba7ea17c7dd7908:pNone:4014952.0-4014990.0`, `petroles-004c2afadba7ea17c7dd7908:pNone:3236368.0-3236405.0`

---

## 8. Critérios práticos para diferenciar baixo desempenho de risco imediato
Uma decisão operacional central em um separador trifásico é distinguir quando o problema é de eficiência e quando já se tornou problema de segurança de processo.

### 8.1 Indícios de baixo desempenho ainda contido
- especificação degradada de óleo, água ou gás sem tendência rápida de piora;
- oscilações moderadas, mas controláveis, de nível/interface;
- aumento gradual de alarmes de operação, sem atuação de trip;
- evidência de incrustação, espuma ou dano parcial de interno, porém com contenção íntegra.

Nessa situação, a resposta tende a priorizar:
- redução de carga ou suavização de transientes;
- confirmação instrumental;
- inspeção programada de internos e válvulas;
- revisão de sintonia e estratégia de controle;
- reavaliação da química de processo e da interação com equipamentos a montante/jusante.

### 8.2 Indícios de risco imediato à integridade ou à proteção
- subida de pressão sem resposta adequada do controle;
- nível alto-alto com risco de carryover para gás ou inundação do vaso;
- atuação repetida de PSV ou chatter;
- incoerência entre variáveis críticas e indicação instrumental, sugerindo falha de proteção;
- evidência de vazamento, corrosão severa, vibração anormal ou perda de espessura;
- falha simultânea ou indisponibilidade de intertravamentos relevantes.

Nessa condição, a resposta deve migrar rapidamente de otimização para **proteção da instalação**, com prevalência da filosofia de shutdown, isolamento e alívio conforme o caso.

**Fontes da seção:** `petroles-004c2afadba7ea17c7dd7908:pNone:4273983.0-4274025.0`, `petroles-004c2afadba7ea17c7dd7908:pNone:4014952.0-4014990.0`, `petroles-004c2afadba7ea17c7dd7908:pNone:2485043.60-2485070.0`

---

## 9. Síntese operacional
Para o separador trifásico, o diagnóstico e a proteção devem ser tratados como um sistema único:
- **baixo desempenho recorrente** não é apenas problema de qualidade de produto; pode ser precursor de perda de integridade ou de ativação indevida de salvaguardas;
- **inspeção do vaso** não deve ficar restrita ao casco; internos, bocais, instrumentos e elementos finais de controle afetam diretamente a separação e a segurança;
- **PSV e intertravamentos** devem ser avaliados em cenário dinâmico realista, evitando tanto subproteção quanto superdimensionamento prejudicial;
- **planos de inspeção, teste e manutenção** precisam ser documentados, rastreáveis e conectados a risco, fabricante, histórico e condições agressivas do serviço;
- **modificações e revamps** exigem revisão pré-operação e gestão de mudanças para evitar que o separador opere fora das premissas de projeto e de proteção.

**Fontes da seção:** `petroles-004c2afadba7ea17c7dd7908:pNone:4273983.0-4274025.0`, `petroles-004c2afadba7ea17c7dd7908:pNone:4274127.0-4274164.0`, `regis-74dd376119cbb653fe9922bc:pNone:34257.0-34687.0`, `regis-faabb54ebe90c9b03a141f67:pNone:151.0-234.0`