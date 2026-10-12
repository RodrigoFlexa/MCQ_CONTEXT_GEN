# Calibração e controle metrológico na medição fiscal de óleo e gás e na transferência de custódia em offloading

## 1. Contexto metrológico e alcance regulatório
A medição fiscal e a medição para transferência de custódia são aplicações de alta relevância econômica e regulatória. Nas fontes fornecidas, o Regulamento Técnico de Medição (RTM) é apresentado como aplicável ao projeto, instalação e operação dos sistemas destinados a medir, computar, armazenar e indicar volumes de petróleo e gás natural usados em medição fiscal, apropriação, controle operacional, transporte, estocagem, exportação, importação e transferência de custódia. A revisão do RTM também é descrita como um movimento para ampliar o controle metrológico legal, aumentar a exatidão das medições e ajustar exigências à realidade operacional, inclusive com maior ênfase em computadores de vazão e em requisitos de calibração dos instrumentos associados.

Para FPSOs/FSOs e operações de offloading, isso significa que o sistema de medição não deve ser visto apenas como o medidor principal. O sistema inclui elementos de processo, instrumentos associados, algoritmos de cálculo, rotinas operacionais, registros, selagem, rastreabilidade e evidências de manutenção metrológica. Em termos práticos, a confiabilidade do resultado depende tanto da tecnologia do medidor quanto da robustez do controle metrológico do conjunto.

As fontes também destacam que, após a maior regulação do setor, a demanda por metrologia passou a envolver não só conformidade formal, mas redução de incerteza, rastreabilidade ao SI, disponibilidade de laboratórios e auditoria da operação. Esse ponto é central: a calibração não é um evento isolado; ela integra uma cadeia de rastreabilidade e um sistema de gestão da medição.

**Fontes da seção:** `regis-01a1a980c36144019fe34865:pNone:1316.0-1526.0`, `petroles-004c2afadba7ea17c7dd7908:pNone:3298956.0-3299028.0`, `petroles-4ee4bce16acf674505c8912d:pNone:2009322.0-2009348.0`

## 2. Conceitos operacionais: calibração, verificação, comprovação metrológica e rastreabilidade
Nas fontes, a gestão metrológica é descrita como um processo estruturado. A sequência típica envolve:

1. **Calibração** do equipamento ou sistema, com padrão rastreável.
2. **Verificação metrológica**, confrontando o desempenho obtido com os requisitos aplicáveis.
3. **Ações decorrentes de falhas**, quando houver desvios, não conformidades ou necessidade de ajuste.
4. **Registros formais**, relatórios ou certificados, emitidos e controlados por pessoal autorizado.

A ISO 10012, conforme resumida nas fontes, trata esse encadeamento como parte do processo de comprovação metrológica. O processo de medição, por sua vez, deve ser planejado, validado, implementado, documentado e controlado. A especificação do processo precisa contemplar todos os fatores que afetam a confiabilidade do resultado: equipamento, procedimento, software, condições ambientais, variáveis de influência e competência do operador.

A rastreabilidade é apresentada como requisito fundamental: os resultados de medição devem ser rastreáveis às unidades do Sistema Internacional por meio de laboratórios confiáveis e dos institutos nacionais de metrologia. As fontes também lembram que a infraestrutura de laboratórios é parte do problema real do setor: a capacidade laboratorial e a disponibilidade de padrões nem sempre acompanham a demanda de medição de petróleo e gás.

Em termos práticos, para medição fiscal ou de custódia, o valor só é defensável em auditoria se houver evidência de que:

- o padrão usado na calibração é rastreável;
- o método de calibração é apropriado para a tecnologia e a faixa operacional;
- as condições de uso são representativas ou há correções justificadas;
- os registros demonstram quando, como e por quem a comprovação metrológica foi executada.

**Fontes da seção:** `regis-47457e188d6e8fcb6f7f6952:pNone:2302.0-2532.0`, `petroles-4ee4bce16acf674505c8912d:pNone:2009322.0-2009348.0`, `petroles-004c2afadba7ea17c7dd7908:pNone:3298956.0-3299028.0`

## 3. Calibração de medidores em linha de óleo: princípio, métodos e cuidados
Uma das referências fornecidas descreve o uso de **provador ou calibrador em linha de deslocamento mecânico**. Nesse arranjo, um tubo de volume calibrado é instalado em série com o medidor. Uma esfera ou êmbolo é deslocado pelo próprio fluido; detectores de proximidade definem o trecho útil do provador; entre esses dois pontos, o volume deslocado é conhecido com incerteza rastreada. Quando o medidor fornece pulsos, a razão entre o número total de pulsos e o volume de referência determina o **fator K** do medidor.

Esse princípio é particularmente relevante para sistemas dinâmicos de transferência de custódia em offloading quando a medição principal é feita em linha. A calibração em linha busca comparar a resposta do medidor sob escoamento real com um volume de referência conhecido. Nas fontes, também são citados como métodos aceitos para calibração de medidores fiscais em linha: calibradores de deslocamento mecânico, tanques de calibração, medidores mestres ou outro sistema previamente aprovado pela ANP.

### 3.1 Fator K e desempenho do medidor
Para medidores pulsados, o fator K vincula a indicação do instrumento ao volume de referência. Mudanças no fator K ao longo do tempo podem sinalizar:

- desgaste mecânico;
- variação de condição operacional fora da faixa validada;
- intervenção de manutenção com impacto no desempenho;
- alteração não autorizada de ajuste;
- efeito de propriedades do fluido diferentes daquelas consideradas na calibração.

As fontes acadêmicas chamam atenção para um problema importante: **desvios de calibração induzidos pelo uso de fluido de calibração diferente do fluido real**. Esse alerta é relevante em óleo, porque a equivalência metrológica entre calibrar com água e operar com petróleo não deve ser presumida sem base técnica. Quando se utiliza fluido de conveniência, é necessário demonstrar compatibilidade metrológica com as condições reais de uso.

### 3.2 Intervalo entre calibrações
Uma fonte secundária informa que medidores fiscais da produção de petróleo em linha devem ser calibrados com intervalo máximo de 60 dias entre calibrações sucessivas, admitindo intervalo maior mediante aprovação da ANP com base no histórico das calibrações. Outra fonte acadêmica, porém, registra que esse prazo de 60 dias já foi considerado tecnicamente inviável ou desnecessário em certos contextos. Portanto, o ponto técnico sólido que permanece é: **o intervalo de recalibração deve ser tecnicamente justificado, historicamente suportado e compatível com o requisito regulatório efetivamente vigente**.

### 3.3 Após ajuste, deve haver reconfirmação
As fontes sobre verificação metrológica deixam claro que, após correção ou ajuste, deve ser executado novo ensaio para confirmar o resultado. Isso evita que um ajuste seja aceito sem evidência objetiva de que o erro retornou à faixa admissível.

**Fontes da seção:** `regis-44b5e0f18c0eba454e5dfcf8:pNone:329.0-370.0`, `petroles-004c2afadba7ea17c7dd7908:pNone:3298956.0-3299028.0`, `petroles-004c2afadba7ea17c7dd7908:pNone:3301898.0-3301973.0`

## 4. Verificação metrológica de sistemas de medição de gás natural
As fontes fornecidas trazem mais detalhamento para sistemas de medição de combustíveis gasosos, útil por analogia operacional e diretamente aplicável à medição fiscal e de custódia de gás natural.

### 4.1 Verificação inicial em um ou dois estágios
É descrito que a verificação inicial pode ser realizada em um ou dois estágios. A abordagem em dois estágios é admissível quando ensaios em bancada representarem adequadamente a situação real e quando o desempenho do sistema não for afetado por desligamento, transporte e religamento. Nessa hipótese, o segundo estágio pode ser reduzido a exame complementar, e não necessariamente repetir todos os ensaios. Porém, para tecnologias não cobertas explicitamente pela norma de controle metrológico, a fonte registra que a verificação inicial deve sempre incluir avaliação metrológica na situação real de uso.

Esse critério é muito relevante para FPSOs e instalações offshore, onde vibração, ambiente marinho, variação de carga e condições de utilidades podem afetar o comportamento do sistema. A simples calibração em bancada não substitui, por si só, a comprovação de desempenho no local quando houver sensibilidade à instalação.

### 4.2 Escopo mínimo da verificação inicial
Segundo as fontes, a verificação inicial do sistema de medição pode incluir:

- exame da conformidade do sistema e de todos os seus elementos;
- ensaio metrológico e exame do módulo de medição;
- ensaio metrológico e exame do conversor de volume e dos instrumentos associados, se aplicável;
- ensaio metrológico e exame do conversor de energia e do determinador de poder calorífico, se aplicável;
- exame da adequação das exigências documentadas.

Em sistemas de gás natural isso é crucial porque o valor faturado pode depender não apenas do volume bruto medido, mas também das correções de compressibilidade, densidade, composição e poder calorífico.

### 4.3 Gases de calibração e análise composicional
Para dispositivos de conversão de energia, a fonte informa que devem ser utilizados vários gases de calibração com poderes caloríficos espaçados ao longo da faixa esperada para o local de instalação. Também são citadas normas para cálculo de fator de compressibilidade, valor calorífico, densidade relativa e preparo/certificação de misturas gasosas, além de referências para amostragem de gás natural em transferência de custódia e para análise cromatográfica.

O ponto técnico principal é que o controle metrológico de gás envolve duas camadas:

- a do **medidor primário**;
- a dos **dispositivos de conversão e das análises de composição**, que corrigem o volume e, em alguns casos, convertem a medição para base energética.

Assim, calibrar apenas o elemento primário, sem controlar os instrumentos e algoritmos de correção, produz um sistema incompleto do ponto de vista metrológico.

**Fontes da seção:** `petroles-004c2afadba7ea17c7dd7908:pNone:3301898.0-3301973.0`, `petroles-004c2afadba7ea17c7dd7908:pNone:3301936.60-3302014.0`

## 5. Tanques, arqueação e sistemas de nível em transferência de custódia
As fontes incluem um conjunto de informações sobre **arqueação de tanques fixos** usados para medição, armazenamento e distribuição de granéis líquidos. Nelas, a arqueação é definida como o conjunto de operações para determinar a capacidade volumétrica do tanque em um ou vários níveis de enchimento. O resultado é materializado em tabela volumétrica e certificado emitido por órgão metrológico delegado ou autorizado pelo Inmetro.

Para atividades econômicas e transações comerciais, a fonte informa que o tanque precisa ter **Certificado de Arqueação em vigor**. Também informa que o serviço de arqueação compreende medição do tanque, cálculo do volume e determinação da tabela volumétrica, e que o certificado com validade legal permanece sob atribuição do Inmetro ou do órgão metrológico competente. Há ainda referência, nessa fonte, a frequência periódica de rearqueação de dez anos para determinado contexto regulatório de tanques fixos, com o tanque vazio, limpo e desgaseificado.

Para transferência de custódia em offloading, esse conteúdo é relevante quando a determinação do volume envolve tanques e sistemas de nível, especialmente em terminais e instalações fixas associadas à cadeia logística. O controle metrológico, nesse caso, não se limita ao instrumento de nível: depende da validade da tabela volumétrica, da integridade geométrica do tanque e da conformidade metrológica do arranjo como um todo.

Em termos de decisão profissional, quando houver participação de medição estática por tanques na cadeia de custódia, é necessário verificar pelo menos:

- existência de certificado válido;
- origem metrológica da tabela volumétrica;
- compatibilidade entre o uso do tanque e o certificado disponível;
- condição do sistema de nível e sua calibração/verificação;
- preservação das condições que sustentam a validade da arqueação.

**Fontes da seção:** `petroles-004c2afadba7ea17c7dd7908:pNone:508060.0-508108.0`, `regis-44b5e0f18c0eba454e5dfcf8:pNone:329.0-370.0`

## 6. Incerteza de medição e impacto da calibração
As fontes ressaltam que o controle metrológico deve perseguir não só conformidade, mas **redução dos níveis de incerteza**. Isso é decisivo em medição fiscal e custódia porque pequenas incertezas relativas podem representar valores econômicos relevantes.

### 6.1 Relação geral
A incerteza do resultado não depende somente do medidor principal. Ela incorpora, entre outros fatores:

- incerteza do padrão usado na calibração;
- repetibilidade e estabilidade do fator de calibração;
- resolução e qualidade do sistema de pulsos/sinal;
- condições reais de processo versus condições de calibração;
- instrumentos associados usados para correção de volume ou energia.

### 6.2 Exemplos de formulação
As fontes trazem expressões de propagação de incerteza para diferentes tecnologias.

#### a) Medidor tipo turbina
A vazão volumétrica é apresentada como:

`Q = F / K`

onde `F` é a frequência ou totalização de pulsos e `K` é o fator do medidor. A incerteza combinada é dada por propagação das incertezas de `F` e `K`:

`u(Q) = {[(∂Q/∂F)·u(F)]² + [(∂Q/∂K)·u(K)]²}^(1/2)`

com:

- `∂Q/∂F = 1/K`
- `∂Q/∂K = F/K²`

O ponto metrológico importante é que a qualidade da calibração do fator `K` afeta diretamente a incerteza final.

#### b) Medidor de deslocamento positivo
A fonte apresenta formulação análoga à da turbina:

`Q = F / K`

Logo, a incerteza combinada também depende da incerteza do gerador de pulsos e do fator `K`.

#### c) Medidor ultrassônico
Para um medidor monofeixe, a fonte registra:

`Q1 = A · K · V`

com velocidade derivada dos tempos de trânsito e da geometria do arranjo. A incerteza combinada passa a depender de `K`, da distância entre transdutores, dos tempos de trânsito e do termo geométrico associado ao ângulo do feixe. Em medidores multifeixe, entram ainda a função de ponderação e os pesos atribuídos a cada corda.

Na prática, isso mostra que o controle metrológico de medidores ultrassônicos não pode ser reduzido à calibração de um único parâmetro: geometria, eletrônica de tempo de trânsito e algoritmo de integração influenciam o resultado.

### 6.3 Consequência prática para calibração
Do ponto de vista de decisão profissional, a calibração é robusta quando:

- o padrão tem incerteza conhecida e compatível com a aplicação;
- a faixa calibrada cobre a faixa operacional relevante;
- o fluido e o regime de escoamento são representativos ou tecnicamente correlacionáveis;
- as correções posteriores são feitas por instrumentos também submetidos a controle metrológico.

**Fontes da seção:** `regis-44b5e0f18c0eba454e5dfcf8:pNone:329.0-370.0`, `petroles-004c2afadba7ea17c7dd7908:pNone:3298956.0-3299028.0`

## 7. Integridade do sistema: selagem, proteção contra ajustes e software
As fontes associadas à ISO 10012 e ao material metrológico de gás convergem em um ponto essencial: a comprovação metrológica só é durável se o sistema permanecer íntegro após a calibração.

### 7.1 Selagem e proteção contra alteração não autorizada
Os acessos a meios de ajuste e os dispositivos cuja posição afete o desempenho devem ser selados ou protegidos de modo que alterações não autorizadas sejam prevenidas e detectáveis. Isso vale tanto para hardware quanto para técnicas de escrita e programas de computador ligados ao processo de medição.

O material de gás reforça que todos os pontos previstos no plano de selagem devem permanecer lacrados. Também registra que qualquer dispositivo adicional projetado para ser instalado junto ao medidor deve ter aprovação específica quanto à possibilidade de interferir no funcionamento metrológico.

### 7.2 Exigências documentadas e sistema de garantia da qualidade
As fontes tratam as exigências documentadas como parte integrante do sistema de medição, e indicam que o sistema de garantia da qualidade pode ser essencial para preservar o uso correto e a integridade da instalação. Isso é particularmente sensível quando há calibração ou manutenção efetuada pelo usuário, ou quando há rotinas locais de ajuste.

O regulamento ou os procedimentos podem prever ensaios de rotina. Os resultados devem ser comparados com limites preestabelecidos e as diferenças devem gerar reações apropriadas. Em outras palavras, um bom sistema metrológico não espera a próxima calibração formal para perceber perda de desempenho; ele possui vigilância de rotina.

### 7.3 Equipamentos recondicionados
As fontes registram que sistemas recondicionados devem ser submetidos a nova verificação metrológica. Esse ponto é importante em operações offshore, onde intervenções de manutenção podem envolver desmontagem, substituição de componentes e reconfiguração.

**Fontes da seção:** `regis-47457e188d6e8fcb6f7f6952:pNone:2302.0-2532.0`, `petroles-004c2afadba7ea17c7dd7908:pNone:3301898.0-3301973.0`, `petroles-004c2afadba7ea17c7dd7908:pNone:3301936.60-3302014.0`

## 8. Registros, auditoria e evidência de conformidade
As fontes são claras ao exigir que os registros do processo de comprovação metrológica sejam datados e aprovados por pessoal autorizado. Esses registros devem incluir, quando aplicável:

- descrição e identificação única do equipamento;
- fabricante;
- data de conclusão da comprovação metrológica;
- resultado da comprovação;
- intervalo fixado para a próxima comprovação;
- documentos de verificação pertinentes;
- condições de operação relevantes.

Além disso, os processos de medição implementados devem manter registros suficientes para demonstrar conformidade com os requisitos especificados. Isso inclui a descrição completa do processo, os elementos usados, as condições operacionais e as ações decorrentes dos dados de controle.

No nível de sistema, a análise e melhoria são apoiadas por auditoria, monitoramento e controle de não conformidades. As fontes citam auditorias internas e ações fiscalizatórias ligadas à ANP/RTM. Para medição fiscal e custódia, a robustez dos registros é tão importante quanto a exatidão instantânea do medidor: sem trilha documental, a medição perde defensabilidade técnica e regulatória.

**Fontes da seção:** `regis-47457e188d6e8fcb6f7f6952:pNone:2302.0-2532.0`, `petroles-004c2afadba7ea17c7dd7908:pNone:3298956.0-3299028.0`

## 9. Síntese prática para FPSO/FSO e offloading
Com base nas fontes fornecidas, uma prática metrologicamente consistente para medição fiscal de óleo e gás e para custódia em offloading deve combinar os seguintes elementos:

1. **Definição clara do arranjo de medição principal e dos instrumentos associados**.
2. **Calibração por método aceito e rastreável**, como provador, tanque de calibração, medidor mestre ou sistema aprovado.
3. **Comprovação de representatividade** entre a calibração e as condições reais de uso, sobretudo quando houver bancada, fluido substituto ou tecnologias sensíveis à instalação.
4. **Controle dos dispositivos de correção**, especialmente em gás: conversores de volume, energia, composição e poder calorífico.
5. **Selagem e proteção** de pontos de ajuste, inclusive em software e parametrização.
6. **Ensaios de rotina e critérios de reação** a desvios.
7. **Registros completos, autorizados e auditáveis**.
8. **Revisão dos intervalos metrológicos com base em histórico, desempenho e requisito regulatório aplicável**.
9. **Nova verificação após recondicionamento, ajuste relevante ou intervenção que possa afetar o desempenho**.
10. **Quando houver tanques na cadeia de custódia**, uso de tabela volumétrica e certificado metrológico compatíveis com a aplicação.

Esse conjunto traduz a ideia central comum às fontes: na medição fiscal e na transferência de custódia, não basta ter um medidor nominalmente preciso. É necessário ter um **sistema de medição comprovado, rastreável, protegido contra alterações indevidas e sustentado por documentação técnica e metrológica verificável**.

**Fontes da seção:** `regis-01a1a980c36144019fe34865:pNone:1316.0-1526.0`, `regis-44b5e0f18c0eba454e5dfcf8:pNone:329.0-370.0`, `regis-47457e188d6e8fcb6f7f6952:pNone:2302.0-2532.0`, `petroles-004c2afadba7ea17c7dd7908:pNone:3301898.0-3301973.0`, `petroles-004c2afadba7ea17c7dd7908:pNone:3301936.60-3302014.0`, `petroles-004c2afadba7ea17c7dd7908:pNone:508060.0-508108.0`, `petroles-004c2afadba7ea17c7dd7908:pNone:3298956.0-3299028.0`, `petroles-4ee4bce16acf674505c8912d:pNone:2009322.0-2009348.0`