# Calibração e desempenho metrológico

## 1. Finalidade da calibração e da verificação metrológica em sistemas de instrumentação de processo

Em FPSOs/FSOs, a calibração e a verificação metrológica sustentam duas funções simultâneas: **controle operacional confiável** e **evidência de desempenho do sistema de medição**. Na prática, isso significa demonstrar, com rastreabilidade e critérios definidos, que a indicação do instrumento continua adequada ao uso pretendido e que a incerteza total permanece compatível com a decisão operacional, de controle, de proteção ou de contabilização associada.

Sob uma ótica metrológica, não basta “o instrumento funcionar”; é necessário conhecer **quanto ele erra, como esse erro varia no tempo e sob quais condições de medição isso ocorre**. Em sistemas de processo, a qualidade da medição depende não apenas do sensor principal, mas também da cadeia associada: elementos primários, condicionamento de sinal, compensações, aquisição, transmissão de dados, algoritmos de cálculo e condições de instalação.

Em aplicações de óleo e gás, especialmente vazão e composição, a medição é tratada como função crítica do negócio e da operação. Os trechos fornecidos também destacam que a insuficiência de capacitação em metrologia pode levar equipes a identificar anomalias sem conseguir determinar a causa, a extensão do problema ou o impacto global no sistema de medição.

**Fontes:** `regis-4a09ac0d89aabbb7901d8059:pNone:173.0-216.60`, `petroles-004c2afadba7ea17c7dd7908:pNone:3298484.0-3298549.0`

## 2. Conceitos metrológicos essenciais para avaliar desempenho

### 2.1 Incerteza de medição

A **incerteza de medição** é um parâmetro não negativo que caracteriza a dispersão dos valores atribuídos ao mensurando com base nas informações utilizadas. Para manutenção e integridade de instrumentos, isso é central porque dois instrumentos podem indicar valores próximos, mas com níveis de confiança distintos.

A avaliação pode incluir:

- **Tipo A**: baseada em análise estatística de resultados medidos sob condições definidas.
- **Tipo B**: baseada em outras informações, como certificado de calibração, classe de exatidão, experiência prévia, deriva e valores publicados.

Na prática de FPSO, a incerteza usada em uma decisão operacional ou de integridade costuma ser composta por várias parcelas: instrumento, padrão, resolução da aquisição, compensações, repetibilidade, influência ambiental e modelo de cálculo.

### 2.2 Condições de medição relevantes

Os trechos distinguem três condições úteis para análise de desempenho:

- **Repetibilidade**: mesmo procedimento, mesmo operador, mesmo sistema, mesmas condições e curto intervalo de tempo.
- **Precisão intermediária**: mesmo procedimento e local, mas com medições distribuídas ao longo de período mais extenso e admitindo algumas mudanças controladas.
- **Reprodutibilidade**: diferentes locais, operadores e sistemas.

Isso é importante para definir se um desvio observado em campo é um problema de ajuste pontual, de estabilidade ao longo do tempo ou de variabilidade entre instalações/equipes.

### 2.3 Termos úteis para diagnóstico de degradação

Os conceitos a seguir ajudam a interpretar resultados de calibração, verificações e históricos:

- **Estabilidade**: propriedade segundo a qual o instrumento mantém suas propriedades metrológicas constantes ao longo do tempo.
- **Tendência instrumental (bias)**: diferença entre a média de indicações repetidas e um valor de referência.
- **Deriva instrumental**: variação da indicação ao longo do tempo, contínua ou incremental, causada por variação das propriedades metrológicas do instrumento e não por mudança do mensurando.
- **Tempo de resposta a um degrau**: tempo para a indicação entrar e permanecer dentro de limites especificados em torno do valor final após uma mudança brusca na entrada.
- **Incerteza instrumental**: parcela da incerteza proveniente do próprio instrumento ou sistema de medição, usualmente obtida por calibração.
- **Classe de exatidão**: classe de instrumentos que atende a requisitos metrológicos sob condições especificadas.
- **Erro máximo admissível**: valor extremo de erro admitido por especificação ou regulamento.
- **Erro no zero**: erro no ponto de controle quando o valor medido especificado é zero.
- **Diagrama de calibração**: representação gráfica da relação entre indicação e resultado de medição correspondente.

Esses parâmetros são especialmente úteis para distinguir falhas como: deslocamento de zero, perda de linearidade, aumento de histerese, lentidão de resposta, degradação progressiva e influência de variáveis externas.

**Fontes:** `regis-4a09ac0d89aabbb7901d8059:pNone:173.0-216.60`, `petroles-004c2afadba7ea17c7dd7908:pNone:2146021.0-2146057.0`

## 3. Estrutura de um programa de calibração e verificação metrológica

Um sistema de calibração sob controle, conforme os trechos fornecidos, requer pelo menos:

- **padrões de trabalho adequados**;
- **rastreabilidade dos padrões**;
- **determinação da contribuição de incerteza de cada variável** para a incerteza global;
- **procedimentos de controle e acompanhamento** das calibrações em linha;
- **critérios de aceitação** para a incerteza de cada variável envolvida.

Em termos práticos, para um instrumento de processo em FPSO, isso se traduz em:

1. definir a função do instrumento e a criticidade da medição;
2. identificar a variável medida e as grandezas de influência relevantes;
3. selecionar padrão, faixa e pontos de verificação coerentes com o uso real;
4. definir critério de aceitação: erro, repetibilidade, deriva, histerese, estabilidade, tempo de resposta ou combinação destes;
5. registrar resultados e comparar com histórico para detecção de degradação;
6. decidir entre ajuste, manutenção, substituição ou mera continuidade em serviço.

### 3.1 Calibração em laboratório versus em campo

Os materiais indicam que, para algumas aplicações, a calibração **não precisa reproduzir exatamente as mesmas condições operacionais**, desde que reproduza o **mesmo regime de operação sistemática** relevante ao comportamento do instrumento. Em estudo citado para medidores ultrassônicos de vazão, a faixa de **número de Reynolds** foi tratada como parâmetro hidrodinâmico chave; assim, combinações adequadas de vazão e viscosidade podem reproduzir o regime de escoamento mesmo com fluido diferente.

Esse princípio pode simplificar a logística e a remoção de medidores. Contudo, ele deve ser lido com cautela:

- o trecho o relaciona explicitamente a **medidores ultrassônicos de vazão**;
- não autoriza generalização automática para qualquer sensor de processo;
- a representatividade depende de quais variáveis de influência dominam o erro do instrumento.

### 3.2 Limitações práticas de calibração

Os trechos também mostram limitações reais do setor de óleo e gás:

- escassez de laboratórios aptos para certas faixas de vazão/viscosidade;
- tempos de espera longos para calibração;
- necessidade operacional de manter medidores sobressalentes para cumprir periodicidades regulatórias em contextos específicos.

Para gestão de integridade, isso reforça a necessidade de:

- planejamento antecipado de janelas de calibração;
- estratégia de sobressalentes críticos;
- priorização por criticidade e histórico de deriva;
- uso disciplinado de dados históricos para alongar ou encurtar intervalos somente quando o regime regulatório permitir.

**Fontes:** `regis-4bab1768b190ba8999f3c016:pNone:482.0-666.0`, `petroles-004c2afadba7ea17c7dd7908:pNone:3298484.0-3298549.0`

## 4. O que deve ser avaliado na calibração: além do erro em um ponto

Uma boa avaliação metrológica não se limita a comparar indicação e padrão em um único ponto. Os trechos permitem destacar os seguintes atributos de desempenho.

### 4.1 Linearidade

A linearidade expressa quão bem a saída acompanha a variação do mensurando ao longo da faixa. Em instrumentos analógicos, transmissores eletrônicos e cadeias com condicionamento, não linearidade pode ser parcela relevante da incerteza. Um instrumento pode apresentar bom ajuste no zero e no span e, ainda assim, erro relevante em pontos intermediários.

### 4.2 Histerese

A histerese aparece quando a indicação para um mesmo valor depende do sentido de aproximação do ponto (crescente ou decrescente). Em instrumentos de processo, isso pode ser causado por atrito, folgas mecânicas, deformações, efeitos térmicos ou comportamento do elemento sensor. O material fornecido cita explicitamente a histerese como parcela de incerteza em uma cadeia de medição.

### 4.3 Repetibilidade e estabilidade temporal

Repetibilidade insuficiente indica dispersão excessiva sob condições supostamente idênticas; estabilidade insuficiente indica que o instrumento não preserva suas propriedades metrológicas ao longo do tempo. Ambas podem surgir por envelhecimento, contaminação, umidade, variações de alimentação, degradação eletrônica ou problemas de instalação.

### 4.4 Deriva e tendência

A deriva é particularmente importante em manutenção baseada em condição. Se o erro cresce de forma lenta, mas consistente, há forte indicação para revisão do intervalo de calibração, investigação de causa física ou substituição programada antes da falha funcional.

### 4.5 Erro no zero e tempo de resposta

Instrumentos de pressão, temperatura, nível ou vazão usados em controle e proteção precisam ser avaliados também quanto a:

- **deslocamento de zero**;
- **resposta dinâmica**;
- **ruído** e estabilidade de leitura;
- **comportamento após perturbações rápidas**.

Em malhas de controle e intertravamentos, um instrumento estático “dentro da tolerância” ainda pode ser inadequado se responder lentamente ou apresentar ruído excessivo.

**Fontes:** `petroles-004c2afadba7ea17c7dd7908:pNone:2146021.0-2146057.0`, `petroles-4ee4bce16acf674505c8912d:pNone:751919.0-751965.0`

## 5. Contribuição da cadeia de medição para a incerteza total

Os trechos deixam claro que a incerteza do sistema não pertence apenas ao medidor principal. Em uma cadeia típica de instrumentação, contribuem para a incerteza:

- sensor primário;
- transmissor;
- condicionamento de sinal;
- compensações térmicas;
- resolução da aquisição digital;
- algoritmos de cálculo;
- posição dos pontos de medição de pressão e temperatura;
- repetibilidade de leitura;
- estabilidade do conjunto.

### 5.1 Exemplos práticos extraídos dos materiais

Os exemplos fornecidos mostram que a incerteza pode incluir, entre outros:

- **não linearidade do sinal**;
- **histerese**;
- **referência de pressão atmosférica** em transdutores manométricos;
- **classe e ligação dos sensores** (por exemplo, PT100 classe A a 4 fios);
- **acurácia e repetibilidade do medidor** (exemplo citado: Coriolis);
- **erro de instrumento auxiliar**, como wattímetro;
- **resolução da placa de aquisição**;
- **incerteza e repetibilidade da compensação de junta fria** em termopares.

Para manutenção e diagnóstico, isso significa que uma aparente “falha do sensor” pode, na verdade, estar na cadeia de aquisição, no condicionador, na compensação de temperatura, na alimentação elétrica ou na parametrização do sistema.

### 5.2 Implicação para calibração e verificação

Sempre que o uso do instrumento depender da cadeia completa, é tecnicamente mais robusto avaliar:

- o elemento isolado, quando necessário para manutenção de bancada; e
- a **cadeia fim a fim**, quando a função operacional depende do conjunto.

Em termos de diagnóstico, a divergência entre uma boa calibração de bancada e mau desempenho em serviço costuma indicar influência de instalação, ruído, aterramento, resolução, dinâmica de processo ou erro de compensação.

**Fontes:** `regis-4bab1768b190ba8999f3c016:pNone:482.0-666.0`, `petroles-4ee4bce16acf674505c8912d:pNone:751919.0-751965.0`

## 6. Instrumentos de vazão: particularidades metrológicas relevantes

Embora a faceta envolva instrumentos de processo em geral, os trechos recebidos concentram conteúdo mais robusto em **medição de vazão**. Alguns princípios são amplamente úteis para FPSOs.

### 6.1 Proving e calibração periódica

Os provadores são apresentados como instrumentos de alta importância porque determinam o desempenho do medidor volumétrico. O material descreve dois tipos principais:

- **provador convencional bidirecional de esfera**;
- **microprovador**, que usa pistão pressurizado/deslocador guiado e técnica de dupla cronometria para interpolar pulsos.

No provador convencional, a passagem da esfera entre detectores inicia e encerra a contagem de pulsos do medidor. O volume inferido pelos pulsos é comparado com o volume calibrado do provador. No microprovador, o menor volume interno calibrado só se torna viável pela técnica de dupla cronometria, mantendo incerteza baixa no contexto descrito.

### 6.2 Variáveis auxiliares necessárias

A exatidão do sistema exige instrumentação auxiliar compatível:

- medição de **pressão** e **temperatura** junto ao medidor e ao provador;
- em vazão mássica, necessidade de **densímetro em linha**;
- para provadores convencionais, pressão e temperatura normalmente medidas na entrada e saída, usando-se a média nos cálculos.

Ou seja, um bom desempenho do medidor de vazão pode ser invalidado por desempenho metrológico inadequado de instrumentos auxiliares.

### 6.3 Requisitos físicos de integridade do provador

Os trechos apontam a necessidade de **estanqueidade absoluta** entre entrada e saída do provador, verificável pelo dreno de válvula de duplo bloqueio. Também mencionam revestimentos internos duros e lisos, além de isolamento externo para reduzir corrosão, aumentar vida útil e minimizar diferenças de temperatura entre medidor e provador. Mesmo quando tais diferenças térmicas possam ser compensadas nos cálculos, elas introduzem incertezas adicionais.

### 6.4 Instrumentos mais e menos difíceis de calibrar

Segundo o material, instrumentos de **pressão** e **temperatura** em geral não apresentam maiores dificuldades de calibração. Já **densímetros** podem apresentar maior dificuldade por ausência de padrão adequado e, frequentemente, precisam de calibração periódica fora de linha.

**Fontes:** `regis-4bab1768b190ba8999f3c016:pNone:482.0-666.0`

## 7. Verificação de desempenho, tempo de teste e interpretação de resultados

Os trechos mostram que o tempo de integração do teste pode alterar significativamente a incerteza estimada. Em estudo de medição multifásica citado, testes de curta duração tenderam a gerar incertezas mais elevadas do que testes de longa duração realizados em plataforma. Isso é coerente com sistemas sujeitos a variabilidade de processo, onde janelas curtas podem capturar flutuações transitórias de maneira mais severa.

### 7.1 Consequências práticas

Para avaliação de instrumentos em FPSO, isso sugere que o plano de verificação de desempenho deve definir explicitamente:

- duração do teste;
- regime operacional representado;
- estabilidade do processo durante a coleta;
- número de repetições;
- estatística usada para aceitação.

Sem essa definição, comparações entre resultados de oficina, bancada, teste de aceitação e desempenho em campo podem ser enganosas.

### 7.2 Interpretação cautelosa

Resultados de laboratório obtidos com integração curta podem ser mais conservadores, mas isso não significa automaticamente que representem melhor o comportamento operacional. A interpretação depende do objetivo do teste:

- qualificação metrológica do instrumento;
- comparação entre tecnologias;
- aceitação para uso em processo instável;
- investigação de degradação.

**Fontes:** `regis-4a09ac0d89aabbb7901d8059:pNone:173.0-216.60`, `petroles-004c2afadba7ea17c7dd7908:pNone:4039049.0-4039116.0`

## 8. Ambientes e aplicações em que a calibração é mais desafiadora

Os trechos sobre medição em sistemas de tocha ilustram um caso extremo, útil como referência para FPSOs: regime pulsante, grandes variações instantâneas de vazão e pressões absolutas abaixo da atmosférica local. Nessa condição, a calibração convencional pode se tornar tecnicamente difícil porque:

- o sistema fixo pode não conseguir garantir a repetibilidade requerida;
- retirar o medidor e calibrá-lo em laboratório externo pode não cobrir toda a faixa real de operação;
- a própria variabilidade operacional torna difícil reproduzir em campo uma condição estável de verificação.

Por isso, o material menciona que operadores vêm buscando aprovação de métodos de verificação como a chamada **calibração de zero** para comprovação metrológica desse tipo de medição. Para manutenção e integridade, a lição principal é que o método de verificação precisa ser compatível com o comportamento real do processo; nem toda aplicação crítica admite o mesmo modelo de calibração periódica tradicional.

**Fontes:** `petroles-004c2afadba7ea17c7dd7908:pNone:4262464.0-4262498.0`

## 9. Diagnóstico de degradação de desempenho em serviço

Com base nos conceitos e exemplos dos trechos, a degradação metrológica de instrumentos de processo pode ser investigada por meio dos seguintes sinais:

- crescimento da **tendência** em relação ao padrão ou à referência de processo;
- aumento da **deriva** entre calibrações sucessivas;
- piora da **repetibilidade** em testes sob mesmas condições;
- aumento de **histerese** em ciclos de subida e descida;
- deslocamento de **zero**;
- piora do **tempo de resposta**;
- indícios de **ruído**, interferência elétrica ou perda de pulsos;
- discrepância entre desempenho do sensor isolado e da cadeia completa.

Em medidores com saída por pulsos, o material ressalta que confrontar a frequência de dois captadores pode reduzir erros causados por ruído, interferência elétrica ou perda de pulsos. Esse raciocínio é aplicável a diagnósticos de integridade de sinais em campo: quando a variável primária parece fisicamente coerente, mas a contagem transmitida ao sistema é instável, a causa pode estar na detecção, cabeamento, aterramento, eletrônica associada ou comunicação do sinal.

**Fontes:** `petroles-004c2afadba7ea17c7dd7908:pNone:2146021.0-2146057.0`, `regis-4bab1768b190ba8999f3c016:pNone:482.0-666.0`, `petroles-4ee4bce16acf674505c8912d:pNone:751919.0-751965.0`

## 10. Critérios práticos para decisão de manutenção, ajuste ou substituição

À luz dos materiais, uma decisão técnica sobre um instrumento deve considerar simultaneamente:

1. **erro atual** frente ao critério aplicável;
2. **histórico de deriva**;
3. **repetibilidade** e estabilidade do resultado;
4. **impacto da incerteza** na função do instrumento;
5. **representatividade do método de calibração** para o regime real de operação;
6. **disponibilidade de laboratório/padrão adequado**;
7. **criticidade operacional** e necessidade de continuidade de produção.

Como orientação geral:

- **Ajustar** é adequado quando há desvio corrigível sem evidência de instabilidade estrutural.
- **Reparar** é mais coerente quando há não linearidade, histerese, lentidão ou instabilidade incompatíveis com simples ajuste.
- **Substituir** tende a ser a melhor opção quando a deriva é recorrente, a estabilidade é baixa, o custo de restauração é elevado ou a aplicação crítica não tolera reincidência.
- **Manter em serviço com monitoramento** pode ser justificável apenas quando o desvio é conhecido, a incerteza remanescente continua aceitável e o regime de risco permite tal decisão.

Em todos os casos, a avaliação deve ser documentada com base em resultados rastreáveis e contexto de aplicação, e não apenas em julgamento subjetivo de funcionamento.

**Fontes:** `regis-4a09ac0d89aabbb7901d8059:pNone:173.0-216.60`, `regis-4bab1768b190ba8999f3c016:pNone:482.0-666.0`, `petroles-004c2afadba7ea17c7dd7908:pNone:2146021.0-2146057.0`, `petroles-004c2afadba7ea17c7dd7908:pNone:3298484.0-3298549.0`

## 11. Síntese operacional para FPSOs/FSOs

Para fins de manutenção e integridade, a calibração e o desempenho metrológico de instrumentos de processo devem ser tratados como disciplina contínua, não como evento isolado. Os trechos sustentam uma abordagem em que o profissional precisa:

- conhecer os conceitos formais de erro, incerteza, repetibilidade, deriva e estabilidade;
- avaliar o instrumento dentro da **cadeia completa de medição**;
- distinguir entre calibração em bancada, verificação em campo e verificação de desempenho em serviço;
- selecionar métodos coerentes com o regime do processo;
- usar histórico para detectar degradação antes da perda funcional;
- reconhecer limitações laboratoriais, operacionais e regulatórias da aplicação.

Em instrumentos de processo, especialmente vazão, o desempenho metrológico confiável depende tanto da qualidade do medidor quanto da qualidade do método de comprovação desse desempenho.