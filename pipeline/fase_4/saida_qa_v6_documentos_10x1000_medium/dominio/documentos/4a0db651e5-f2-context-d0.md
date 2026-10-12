# Alarmes, votação e ações automáticas em sistemas de Fogo & Gás (F&G)

## 1. Escopo técnico desta faceta
Este documento trata da **filosofia de alarme**, da **lógica de demanda para funções automáticas de segurança** e da **integração do F&G com ESD, isolamento e combate a incêndio**, com base apenas nos trechos fornecidos. O material disponível permite discutir:

- como os alarmes devem ser racionalizados e priorizados;
- como a detecção de gás/incêndio pode demandar ações automáticas;
- como estados degradados, bypasses e falhas de elementos finais precisam ser tratados;
- como testes e evidências de desempenho sustentam a confiabilidade da atuação.

Os trechos **não trazem parametrização completa de lógicas de votação** (por exemplo, critérios quantitativos de 1ooN, 2ooN, temporizações, setpoints ou matrizes causa-e-efeito completas). Portanto, este documento não prescreve arquiteturas de votação específicas, mas organiza os critérios e vínculos técnicos que devem sustentar tais decisões.  
**Fontes:** `petroles-004c2afadba7ea17c7dd7908:pNone:2452608.0-2452660.0`, `petroles-004c2afadba7ea17c7dd7908:pNone:2452918.0-2452957.180`, `petroles-4ee4bce16acf674505c8912d:pNone:2025382.60-2025432.0`, `anp-ac2e4f9942314aa203e5b9b3:p28-30:20.0-33.0`, `anp-ac72dc113a17b403b32f806c:p1-3:0.0-19.0`, `anp-9e6669a2f607f49346e5119c:p32-34:26.0-35.0`

## 2. Papel do alarme no contexto do F&G
Em unidades offshore altamente automatizadas, o sistema supervisório acompanha variáveis e estados de processo, utilidades e salvaguardas, gerando alarmes quando ocorre anomalia relevante. O material destaca que nem todo desvio deve virar alarme: uma configuração inadequada tende a produzir **falsos alarmes**, **alarmes intermitentes** e **sobrecarga de informação**, reduzindo a capacidade do operador de identificar rapidamente a anormalidade importante. O texto também relaciona explicitamente a má gestão de alarmes ao agravamento de incidentes e à perda de credibilidade do sistema de alarmes.  
**Fontes:** `petroles-004c2afadba7ea17c7dd7908:pNone:2452608.0-2452660.0`, `petroles-004c2afadba7ea17c7dd7908:pNone:2452918.0-2452957.180`

No contexto de F&G, isso é particularmente crítico porque o alarme não tem apenas função informativa: ele é parte da cadeia que pode levar a respostas como:

- atuação do ESD;
- fechamento de válvulas ligadas à emergência;
- parada de compressores e bombas;
- atuação de dilúvio por zona;
- comunicação da condição de emergência;
- anúncio de alarmes próprios da situação de emergência.

Ou seja, a filosofia de alarme do F&G precisa ser coerente com o papel do sistema como **barreira de detecção e de disparo de barreiras subsequentes**.  
**Fontes:** `petroles-4ee4bce16acf674505c8912d:pNone:2025382.60-2025432.0`, `petroles-004c2afadba7ea17c7dd7908:pNone:3060575.0-3060619.0`

## 3. Racionalização e priorização de alarmes
O material de gestão de alarmes descreve uma abordagem estruturada para configuração e revisão do sistema, com ênfase em:

1. **definir formalmente a filosofia de alarmes**;
2. **identificar bad actors**, isto é, alarmes que mais atuam ou se repetem;
3. **analisar o comportamento temporal** desses alarmes para distinguir ocorrências concentradas de alarmes crônicos/intermitentes;
4. **classificar a criticidade** com base em severidade e tempo de resposta;
5. decidir se o ponto deve permanecer como alarme ou ser tratado apenas como evento.

A fórmula explicitada no trecho é:

**Criticidade = severidade × tempo de resposta**

Essa formulação é útil para F&G porque ajuda a separar:

- condições que exigem **resposta operacional imediata**;
- condições que justificam **ação automática** por indisponibilidade do tempo humano de resposta;
- estados que devem ser registrados como **eventos**, e não anunciados como alarmes prioritários.

Para F&G, isso significa que a priorização não deve ser baseada apenas em frequência de ocorrência, mas principalmente nas consequências da não ação e no tempo disponível até agravamento do cenário.  
**Fontes:** `petroles-004c2afadba7ea17c7dd7908:pNone:2452918.0-2452957.180`, `petroles-004c2afadba7ea17c7dd7908:pNone:2452608.0-2452660.0`

## 4. Filosofia de alarme aplicada ao F&G
Com base nos trechos, uma filosofia de alarme aplicável ao F&G deve, no mínimo, diferenciar quatro grupos de informação:

### 4.1 Alarmes de processo/perigo detectado
São os alarmes ligados à identificação de condição perigosa, como detecção de gás ou vazamento. No exemplo fornecido, a detecção pode ocorrer por sistema de amostragem e por detectores fixos de gás. A presença de detecção de vazamento é citada explicitamente como condição de ativação do ESD.  
**Fonte:** `petroles-4ee4bce16acf674505c8912d:pNone:2025382.60-2025432.0`

### 4.2 Alarmes de estado degradado de barreira
O conjunto de exemplos de classificação de alarmes mostra que estados de bypass e indisponibilidade de funções ligadas a ESD e fechamento de válvulas devem ser tratados explicitamente no sistema de alarmes. Entre os exemplos listados aparecem mensagens como:

- bypass de emergência;
- bypass de botoeira ESD;
- bypass de botoeira de fechamento de SDV.

Isso é relevante para F&G porque um detector indisponível, uma botoeira bypassada ou uma lógica de fechamento inibida alteram a capacidade real de resposta da instalação. Em outras palavras, **a indisponibilidade da proteção também deve alarmar**.  
**Fonte:** `petroles-004c2afadba7ea17c7dd7908:pNone:2452918.0-2452957.180`

### 4.3 Alarmes de falha de atuação
Os achados de auditoria da ANP mostram a importância de alarmar falhas de elementos finais associados às funções automáticas, como:

- SDV degradada;
- ADV degradada;
- bomba de combate a incêndio degradada;
- falhas sem ordem de manutenção corretiva aberta;
- testes sem comprovação adequada de desempenho.

Esses alarmes não anunciam o perigo primário, mas a perda de capacidade de mitigação.  
**Fonte:** `anp-ac2e4f9942314aa203e5b9b3:p28-30:20.0-33.0`

### 4.4 Eventos e diagnósticos
Os trechos de gestão de alarmes reforçam que nem toda informação do supervisório deve ser alarme. Parte das informações deve permanecer como evento ou diagnóstico, para evitar sobrecarga operacional. Isso é particularmente importante em F&G para não mascarar alarmes de alta criticidade com excesso de mensagens de baixa relevância.  
**Fontes:** `petroles-004c2afadba7ea17c7dd7908:pNone:2452608.0-2452660.0`, `petroles-004c2afadba7ea17c7dd7908:pNone:2452918.0-2452957.180`

## 5. Integração do F&G com funções automáticas de segurança
O material descreve uma cadeia causa-efeito típica em que a detecção de perigo leva a ações automáticas. No exemplo do navio de GNL, o ESD é ativado, entre outras situações, por:

- acionamento manual por botoeiras de emergência;
- detecção de parâmetro fora das condições habituais de carga/descarga;
- detecção de vazamento pelo sistema de amostragem ou pelo sistema de detecção;
- falta de energia elétrica por blackout;
- comando externo do terminal.

Uma vez demandado, o ESD implica ações como:

- parada de compressores de alta e baixa vazão;
- parada de bombas criogênicas;
- fechamento das válvulas ligadas ao ESD;
- aviso ao terminal sobre a paralisação da operação;
- ativação dos alarmes da situação de emergência.

Embora esse exemplo não descreva uma planta de processo de FPSO em todos os detalhes, ele evidencia o princípio central: **a detecção deve estar amarrada a ações automáticas concretas de isolamento, parada e mitigação**.  
**Fonte:** `petroles-4ee4bce16acf674505c8912d:pNone:2025382.60-2025432.0`

Complementarmente, há indicação de que **cada zona a ser protegida contra incêndio é provida de uma ADV independente com sistema de acionamento próprio**. Isso mostra um critério importante de integração do F&G com mitigação: a lógica de atuação deve respeitar a compartimentação por zona, evitando dependência excessiva de um único elemento de disparo para toda a instalação.  
**Fonte:** `petroles-004c2afadba7ea17c7dd7908:pNone:3060575.0-3060619.0`

## 6. Votação: o que os trechos permitem afirmar
Os trechos fornecidos **não explicitam** arquiteturas como 1ooN, 2ooN, 2oo3, cruzamento entre detectores de gás e chama, nem temporizações configuradas para evitar disparos espúrios. Assim, não é possível, com rastreabilidade suficiente, definir neste documento qual filosofia de votação é “correta” para cada cenário.

Ainda assim, o material permite estabelecer requisitos mínimos para avaliar uma filosofia de votação em F&G:

1. **A votação precisa ser compatível com a criticidade do cenário**, isto é, com severidade e tempo de resposta disponível. Se o cenário evolui mais rápido do que a resposta humana, a filosofia deve privilegiar atuação automática tempestiva.  
   **Base:** classificação por criticidade e necessidade de ação oportuna.  
   **Fontes:** `petroles-004c2afadba7ea17c7dd7908:pNone:2452918.0-2452957.180`, `petroles-004c2afadba7ea17c7dd7908:pNone:2452608.0-2452660.0`

2. **A votação deve ser coerente com a capacidade real dos elementos finais**. Não adianta lógica sofisticada se SDVs, ADVs, bombas de incêndio ou drenagem não entregam o desempenho de projeto quando demandados.  
   **Base:** auditorias ANP sobre tempos de fechamento, estanqueidade, vazão, pressão e funcionalidade.  
   **Fonte:** `anp-ac2e4f9942314aa203e5b9b3:p28-30:20.0-33.0`

3. **A filosofia deve considerar estados degradados e contingenciamentos**. Detectores indisponíveis, bypasses, SDV travada, ADV degradada ou bomba degradada alteram a cobertura real da lógica e exigem compensações e prazos compatíveis com o risco.  
   **Fontes:** `petroles-004c2afadba7ea17c7dd7908:pNone:2452918.0-2452957.180`, `anp-ac2e4f9942314aa203e5b9b3:p28-30:20.0-33.0`, `anp-9e6669a2f607f49346e5119c:p32-34:26.0-35.0`

4. **A decisão sobre votação deve estar ligada a estudos de risco e à aplicação verificável de ALARP ou critério equivalente**. O relatório da ANP enfatiza que decisões sobre planos de ação e barreiras devem ser fundamentadas em risco, confiabilidade, custo-benefício e boas práticas reconhecidas.  
   **Fonte:** `anp-9e6669a2f607f49346e5119c:p32-34:26.0-35.0`

Em síntese: mesmo sem os detalhes numéricos de 1ooN/2ooN, os trechos indicam que a votação não pode ser escolhida isoladamente; ela precisa ser demonstravelmente consistente com **risco, tempo de resposta, desempenho dos elementos finais e gestão de degradações**.

## 7. Desempenho dos elementos finais acionados pelo F&G
A integração entre F&G e funções automáticas só é efetiva se os elementos a jusante comprovarem desempenho. As auditorias da ANP destacam pontos objetivos que devem ser verificados:

### 7.1 SDVs
Foram avaliados:

- **tempo de atuação/fechamento** por full stroke test, que deve atender às premissas do estudo de propagação de incêndio;
- **estanqueidade** por leak test;
- adequação de procedimentos e registros.

Entre os desvios encontrados apareceram:

- ausência de contingência para SDV degradada;
- SDV travada mecanicamente sem análise de risco adequada;
- teste sem registro do travel time;
- aprovação de teste sem medição adequada de variação de pressão a jusante;
- velocidade de deslocamento usada em tarefa diferente da prevista em projeto.

Para a faceta de alarmes e ações automáticas, a implicação é direta: a lógica de F&G pode demandar fechamento, mas a salvaguarda só é real se o tempo e a vedação corresponderem ao assumido nos estudos.  
**Fonte:** `anp-ac2e4f9942314aa203e5b9b3:p28-30:20.0-33.0`

### 7.2 Dilúvio e válvulas ADV
A ANP também apontou desvios como:

- ausência de contingência para bombas de combate a incêndio;
- teste de dilúvio molhado sem exigência de medição de pressão/vazão;
- aprovação de teste sem registro da vazão no bico mais desfavorável;
- ADV degradada sem contingenciamento adequado;
- teste funcional não realizado com continuidade operacional sem justificativa técnica adequada;
- duração do teste inferior ao estabelecido em procedimento.

Logo, quando o F&G é integrado ao dilúvio, o comissionamento, os testes periódicos e o registro da performance hidráulica são parte inseparável da própria filosofia de atuação automática.  
**Fonte:** `anp-ac2e4f9942314aa203e5b9b3:p28-30:20.0-33.0`

### 7.3 Independência por zona
O trecho que informa uma ADV independente por zona protegida reforça que o projeto deve evitar dependências desnecessárias entre zonas de incêndio. Em termos de lógica, a setorização influencia diretamente o escopo do disparo automático e a extensão das consequências de uma falha única.  
**Fonte:** `petroles-004c2afadba7ea17c7dd7908:pNone:3060575.0-3060619.0`

## 8. Gestão de degradação, bypasses e contingenciamento
Os relatórios da ANP e os exemplos de classificação de alarmes convergem em um ponto: a gestão de barreiras degradadas precisa ser formal, rastreável e proporcional ao risco.

Aspectos destacados nos trechos:

- contingenciamentos propostos podem ser inadequados ou ter prazos incompatíveis com o risco;
- componentes degradados não podem permanecer sem tratamento formal;
- é necessário abrir ordens/notas de manutenção para desvios identificados em teste;
- decisões e planos de ação devem ser baseados em risco e com aplicação verificável de ALARP ou critério equivalente;
- estados de bypass associados a ESD/fechamento precisam ser classificados e acompanhados.

Para F&G, isso significa que a indisponibilidade de detector, lógica, SDV, ADV, bomba ou comunicação associada não deve ser tratada apenas como pendência de manutenção: trata-se de **redução de capacidade da barreira de segurança**, com necessidade de alarme, contingência e prazo compatível com a exposição ao perigo.  
**Fontes:** `petroles-004c2afadba7ea17c7dd7908:pNone:2452918.0-2452957.180`, `anp-ac2e4f9942314aa203e5b9b3:p28-30:20.0-33.0`, `anp-9e6669a2f607f49346e5119c:p32-34:26.0-35.0`

## 9. Lições de falha: quando a integração F&G–ESD não funciona
O alerta de segurança da ANP sobre liberação de gás em alta pressão e incêndio após ruptura de linha de gas-lift é particularmente importante para esta faceta. Entre as causas identificadas pelo operador, aparecem simultaneamente:

- **demora na interrupção do vazamento**;
- **inexistência de treinamento para fechamento local de SDV**;
- **projeto do sistema supervisório que não permitia atuação eficiente e rápida da SDV**;
- **resposta inadequada à emergência, sem ativação manual e automática do ESD**;
- **não atuação do sistema de detecção de fogo e gás**, que apresentava não conformidades de manutenção;
- **alocação inadequada de detectores de fogo e gás**.

Esse conjunto de causas mostra que a filosofia de alarme e atuação automática pode falhar por múltiplos mecanismos encadeados:

1. detecção ineficaz;
2. arquitetura de supervisão pouco operável;
3. falha humana por falta de treinamento;
4. ausência de disparo automático ou manual do ESD;
5. demora no isolamento do inventário;
6. posterior ignição da nuvem.

As lições aprendidas indicadas no alerta incluem:

- estabelecer requisitos específicos de treinamento para tarefas críticas de fechamento de válvulas;
- projetar elementos críticos considerando as interações com o operador de sala de controle e fatores humanos;
- estabelecer planos e procedimentos de inspeção, teste e manutenção compatíveis com o risco;
- garantir rotina de inspeção da locação e posicionamento de detectores de fogo e gás;
- realizar revisão de segurança pré-partida.

Para troubleshooting e melhoria contínua, esse alerta é evidência forte de que o desempenho do F&G não depende apenas do detector em si, mas da **cadeia completa detector–alarme–operador–lógica–elemento final**.  
**Fonte:** `anp-ac72dc113a17b403b32f806c:p1-3:0.0-19.0`

## 10. Consequências práticas para comissionamento, operação e monitoramento
A partir dos trechos, a verificação de uma filosofia de alarme e votação integrada ao F&G deve incluir, no mínimo, os seguintes pontos de checagem:

### 10.1 No projeto e na racionalização
- existência de filosofia formal de alarmes;
- definição clara do que é alarme versus evento;
- priorização baseada em severidade e tempo de resposta;
- amarração da lógica aos cenários de risco e às consequências da não ação;
- definição explícita de alarmes para estados degradados, bypasses e indisponibilidade de barreiras.  
**Fontes:** `petroles-004c2afadba7ea17c7dd7908:pNone:2452918.0-2452957.180`, `petroles-004c2afadba7ea17c7dd7908:pNone:2452608.0-2452660.0`

### 10.2 No comissionamento e teste
- comprovação do tempo de fechamento de SDVs;
- comprovação de estanqueidade;
- comprovação de vazão/pressão de dilúvio e desempenho de ADV;
- registros completos de teste, com pressões, horários e medições relevantes;
- verificação de que a atuação automática atende às premissas usadas nos estudos.  
**Fonte:** `anp-ac2e4f9942314aa203e5b9b3:p28-30:20.0-33.0`

### 10.3 Na operação
- monitoramento de bad actors e alarmes intermitentes;
- revisão periódica de alarmes crônicos que possam mascarar alarmes reais de F&G;
- vigilância sobre bypasses e inibições de ESD/fechamento;
- confirmação da capacidade operacional de resposta manual quando aplicável.  
**Fontes:** `petroles-004c2afadba7ea17c7dd7908:pNone:2452918.0-2452957.180`, `anp-ac72dc113a17b403b32f806c:p1-3:0.0-19.0`

### 10.4 Na gestão de mudanças e degradações
- contingenciamento imediato para elementos críticos degradados;
- decisão baseada em risco/ALARP para prazos e medidas compensatórias;
- rastreabilidade de ações de inspeção, teste e manutenção;
- revisão da filosofia quando mudanças de operador, layout, manutenção deficiente ou falhas recorrentes comprometerem a função de detecção/atuação.  
**Fontes:** `anp-9e6669a2f607f49346e5119c:p32-34:26.0-35.0`, `anp-ac72dc113a17b403b32f806c:p1-3:0.0-19.0`, `anp-ac2e4f9942314aa203e5b9b3:p28-30:20.0-33.0`

## 11. Síntese técnica
Os trechos fornecidos sustentam as seguintes conclusões para a faceta **Alarmes, votação e ações automáticas**:

- a qualidade da filosofia de alarme é determinante para que o F&G cumpra sua função de barreira;
- a priorização deve considerar **criticidade = severidade × tempo de resposta**;
- detecção de vazamento/gás pode e deve demandar ações automáticas como ESD, fechamento de válvulas, parada de equipamentos e acionamento de sistemas de mitigação;
- a setorização de incêndio e a independência de atuação por zona são relevantes para o escopo das respostas automáticas;
- a filosofia de votação não pode ser analisada isoladamente dos estudos de risco, do desempenho dos elementos finais e da gestão de estados degradados;
- testes de SDV, ADV, dilúvio e outros elementos finais são parte essencial da validação da lógica de F&G;
- falhas de manutenção, mau posicionamento de detectores, inadequações do supervisório e ausência de treinamento podem anular, na prática, a integração entre alarme e segurança.

Em consequência, a avaliação profissional de um sistema F&G nesta faceta deve observar simultaneamente **racionalização de alarmes, cadeia causa-efeito, desempenho comprovado dos atuadores, gestão de bypasses e contingências baseadas em risco**.  
**Fontes:** todos os chunk_ids listados em `used_chunk_ids`.