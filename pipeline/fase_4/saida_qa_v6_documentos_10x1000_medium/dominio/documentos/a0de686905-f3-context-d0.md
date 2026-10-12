# Integridade e manutenção de meios de salvatagem em FPSOs

## 1. Objetivo técnico e limites deste texto
Este documento organiza princípios de **integridade, manutenção, degradação e prontidão operacional** aplicáveis aos meios de salvatagem de FPSOs sob o recorte de exposição ao **ambiente marinho** e a **períodos de inatividade**. O material disponível nesta rodada não traz requisitos estatutários específicos de LSA/SOLAS nem intervalos normativos completos de teste para baleeiras, balsas, rescue boats, turcos, ganchos ou dispositivos de liberação. Assim, a abordagem abaixo é construída a partir de fontes sobre **gestão de integridade de ativos marítimos, envelhecimento, corrosão, reparos, documentação e manutenção de sistemas críticos**, usando somente inferências técnicas plausíveis e explicitando as limitações.

**Fontes da seção:** `hse-8ae5be797e5471d76a0aa410:p6-9:3.0-0.0`, `anp-b2cfa8a9492ef598716e9685:p37-39:20.0-28.0`

## 2. Como o ambiente marinho e a inatividade degradam meios de salvatagem

### 2.1 Degradação de barreiras externas e exposição do metal ao meio salino
Um mecanismo recorrente em ativos offshore é a perda da integridade da **camada externa de proteção**. Nas linhas flexíveis, a ruptura da camada plástica externa expõe o anular e as armaduras metálicas ao ambiente marinho, iniciando ou acelerando corrosão e perda de resistência. Embora a fonte trate de dutos/risers, o mecanismo é tecnicamente relevante por analogia para meios de salvatagem com partes metálicas protegidas por pintura, revestimento, galvanização, encapsulamento ou carenagem: quando a barreira externa falha, a degradação tende a migrar de um problema superficial para um problema estrutural ou funcional.

Além disso, inspeções em linhas flexíveis mostram que danos iniciais muitas vezes surgem na instalação ou no contato com acessórios, e que o envelhecimento dos componentes externos favorece mecanismos de falha progressivos. Em equipamentos de salvatagem, isso reforça a necessidade de observar pontos de atrito, impacto, contato metal-metal, retenção de água salgada, frestas e interfaces entre materiais diferentes.

**Implicação prática:** em meios de abandono, a perda de revestimento, dano em proteção superficial ou abertura de caminho para água salgada não deve ser tratada como mera estética; ela pode ser o precursor de perda de capacidade de lançamento, recuperação ou sobrevivência.

**Fontes da seção:** `petroles-004c2afadba7ea17c7dd7908:pNone:4085582.0-4085625.0`, `regis-a43fe36ddcfe616b39546c2e:pNone:0.0-526.0`

### 2.2 Corrosão localizada e dificuldade de reparo em condição úmida
O estudo sobre reparo em dutos flexíveis indica dois pontos úteis para a manutenção de equipamentos expostos:

1. **A aderência de resina epóxi sobre aço úmido é fortemente afetada pela presença de fase líquida na superfície.**
2. Em misturas contendo água do mar, podem ocorrer formas de **corrosão localizada**.

Para meios de salvatagem, isso sugere cautela em reparos expedientes feitos com a estrutura úmida, salgada ou insuficientemente preparada. Uma pintura, selagem ou encapsulamento aplicado sobre superfície mal preparada pode criar falsa sensação de integridade e ainda encobrir a progressão do dano.

**Implicação prática:** o reparo anticorrosivo em ambiente marinho depende criticamente de preparação de superfície, compatibilidade do sistema de reparo e controle das condições de aplicação.

**Fontes da seção:** `regis-a43fe36ddcfe616b39546c2e:pNone:0.0-526.0`, `anp-ca80abc6bcc3d90b2aeb7b87:p10-13:22.0-4.0`

### 2.3 Envelhecimento, fadiga e ameaças de fim de vida
A gestão de integridade de FPSOs/FSUs destacada pela HSE enfatiza que, em fase tardia da vida, o sistema deve considerar **ameaças de envelhecimento**, inclusive **fadiga estrutural**, e que o escopo, a metodologia e a frequência de inspeção devem ser compatíveis com a **idade e a condição** do ativo. Também se recomenda revisão holística de anomalias abertas para identificar ameaças globais e risco de colapso progressivo.

Transposto para meios de salvatagem, esse princípio significa que equipamentos antigos, com histórico de exposição severa ou longos períodos sem uso real, não devem permanecer em regime de manutenção “padrão” apenas por tradição. A idade, a condição observada e o histórico de falhas precisam influenciar a estratégia de inspeção e substituição.

**Fontes da seção:** `hse-8ae5be797e5471d76a0aa410:p6-9:3.0-0.0`, `anp-226946a12711e04f54ee4bfb:p70-75:9.0-18.0`

### 2.4 Efeitos típicos da inatividade sobre subsistemas auxiliares
Mesmo quando não há uso frequente, a inatividade não preserva automaticamente o equipamento. As fontes apontam mecanismos clássicos:

- **baterias** perdem capacidade e precisam de testes periódicos para comprovar operacionalidade;
- **descargas profundas** reduzem a vida útil das baterias;
- **sistemas hidráulicos** exigem limpeza e lubrificação adequadas, inspeções periódicas, eliminação de desalinhamentos e folgas;
- após reparo de componente hidráulico principal, recomenda-se **troca de óleo e filtros**;
- o **nível de óleo** deve ser conferido com frequência;
- para válvulas e itens correlatos, a manutenção preventiva deve evitar **sujeira, superaquecimento e vazamentos**.

Esses mecanismos são diretamente úteis para subsistemas de salvatagem que dependem de partida elétrica, acumuladores, iluminação, painéis, circuitos de comando, freios, atuadores ou guinchos/hidráulicos.

**Fontes da seção:** `petroles-4ee4bce16acf674505c8912d:pNone:2025595.0-2025635.0`

## 3. Princípios para um programa de integridade dos meios de salvatagem

### 3.1 Sistema de gestão de integridade e lacunas de cobertura
A HSE destaca que o operador deve manter um **sistema apropriado de gestão da integridade**, apoiado por especialistas competentes, podendo combinar inspeção **prescritiva periódica** e/ou **inspeção baseada em risco**. Um ponto importante é que os requisitos de sociedade classificadora **não necessariamente cobrem todos os elementos estruturais e equipamentos**; portanto, o operador deve identificar lacunas e garantir que seu sistema trate essas omissões.

Aplicado aos meios de salvatagem, isso significa que a conformidade formal com inspeções mínimas não elimina a necessidade de verificar:

- itens que perderam visibilidade no sistema de manutenção;
- interfaces entre equipamento, suporte estrutural e utilidades;
- degradação progressiva por corrosão marinha, intempérie e baixa frequência de uso;
- reparos temporários ou de vida definida ainda em serviço.

**Fontes da seção:** `hse-8ae5be797e5471d76a0aa410:p6-9:3.0-0.0`

### 3.2 Cadastro de ativos e rastreabilidade
Boa prática destacada pela HSE é manter um **Marine Asset Register** preciso, com transparência sobre:

- componentes de cada sistema;
- localização;
- histórico de inspeções;
- histórico de manutenção;
- histórico de reparos.

A mesma fonte alerta que equipamentos podem **perder visibilidade** no sistema de manutenção ao longo do tempo, levando à falta de manutenção, reparos pendentes ou ausência de documentação-chave de serviço. Auditorias periódicas desse cadastro ajudam a identificar lacunas e corrigir desvios em tempo hábil.

Para meios de salvatagem, esse cadastro deve permitir saber, sem ambiguidade, o estado de prontidão de cada item e de suas partes críticas associadas.

**Fontes da seção:** `hse-8ae5be797e5471d76a0aa410:p6-9:3.0-0.0`

### 3.3 Síntese anual de integridade e visibilidade gerencial
A HSE recomenda um documento anual de síntese de integridade contendo, pelo menos, revisão de:

- histórico de inspeções;
- manutenção e reparos;
- anomalias pendentes;
- backlog de inspeções;
- modificações;
- análises executadas;
- incidentes relevantes do último ano;
- principais ameaças de integridade;
- atividades prioritárias para o ano seguinte.

A ANP, ao tratar de indicadores de segurança operacional e ECSE, reforça que os indicadores devem ser utilizados pela **alta liderança** para avaliar o cenário da instalação e considerar riscos operacionais na tomada de decisão. Há também exemplo de uso de manutenção preditiva em que degradações piores que o esperado levaram à **antecipação da manutenção programada**, com base unificada de informação e acompanhamento por indicadores.

Para meios de salvatagem, isso favorece governança sobre disponibilidade real, atrasos de manutenção, degradação observada e priorização de recursos.

**Fontes da seção:** `hse-8ae5be797e5471d76a0aa410:p6-9:3.0-0.0`, `anp-b2cfa8a9492ef598716e9685:p37-39:20.0-28.0`, `petroles-004c2afadba7ea17c7dd7908:pNone:525884.0-525932.0`

## 4. Conteúdo técnico mínimo da manutenção e inspeção

### 4.1 Preservação anticorrosiva
A investigação da ANP sobre casco/tanques mostra uma lógica importante de projeto e manutenção para serviço marítimo prolongado:

- uso de **revestimentos epóxi ou hard coatings** como barreira principal;
- necessidade de compatibilidade entre **revestimento** e **proteção catódica** quando aplicável;
- para vidas longas, não é prudente presumir que a proteção catódica por si só substitui a pintura/barreira.

Embora a fonte trate de casco e tanques, o princípio é útil para estruturas metálicas de meios de salvatagem: o desempenho anticorrosivo é sistêmico, não dependendo apenas de um único recurso. A inspeção deve buscar falhas de revestimento, empolamento, destacamento, corrosão em frestas, corrosão sob depósitos, pites, perda de espessura, deterioração em áreas de contato e aprisionamento de sal.

**Fontes da seção:** `anp-ca80abc6bcc3d90b2aeb7b87:p10-13:22.0-4.0`

### 4.2 Partes hidráulicas, de acionamento e componentes sujeitos a travamento
Para qualquer subsistema hidráulico ou equivalente, as fontes suportam as seguintes ações de manutenção:

- assegurar **limpeza e lubrificação adequadas**;
- realizar **inspeções e ajustes periódicos**;
- eliminar **desalinhamentos e folgas**;
- manter vigilância sobre **nível de óleo**;
- trocar **óleo hidráulico e filtros** após reparo de componente principal;
- evitar contaminação, superaquecimento e vazamentos em válvulas e linhas.

Esse conjunto é particularmente relevante para mecanismos que permanecem longos períodos parados e são exigidos em condição de emergência, quando travamentos, vazamentos internos, resposta lenta e falha de comando tendem a se manifestar no pior momento.

**Fontes da seção:** `petroles-4ee4bce16acf674505c8912d:pNone:2025595.0-2025635.0`

### 4.3 Baterias, alimentação e circuitos de controle
As fontes também indicam que:

- baterias internas de UPS e sistemas equivalentes devem ser **testadas periodicamente** para comprovar operacionalidade;
- **descargas profundas** encurtam a vida útil;
- a operabilidade de **controladores automáticos**, alarmes e sistemas instrumentados deve ser verificada antes de operações críticas;
- em áreas com influência de gás, a troca de baterias de equipamentos portáteis pode introduzir risco de ignição.

Para meios de salvatagem, o princípio aplicável é que componentes dependentes de energia elétrica ou eletrônica — inclusive iluminação, localização, sinalização, partida, comando ou comunicação — exigem verificação funcional e gestão do envelhecimento das baterias, especialmente após longos períodos sem uso real.

**Fontes da seção:** `petroles-4ee4bce16acf674505c8912d:pNone:2025595.0-2025635.0`

## 5. Reparos, modificações e retorno seguro ao serviço
A norma da ANP para sistemas submarinos, embora não específica para meios de salvatagem, fornece um modelo robusto de controle que é tecnicamente útil:

- o reparo ou intervenção não deve levar o sistema a condição inferior ao nível de segurança estabelecido;
- reparos executados devem passar por **inspeções, ensaios e/ou testes**;
- o controle de qualidade deve observar **requisitos de projeto, fabricante, normas, regulamentações e melhores práticas**;
- materiais e insumos devem ser **certificados** e **rastreáveis**;
- procedimentos, força de trabalho e aprovações devem ser **qualificados**;
- todo reparo deve ser registrado com descrição, datas, testes executados, precauções, condições operacionais, prazo de validade quando houver, responsáveis e conclusões.

A HSE complementa que o sistema de integridade deve manter arranjos para **registrar, inspecionar, revisar e substituir reparos de vida definida**, quando necessário.

Para meios de salvatagem, isso implica que reparos temporários, reforços locais, substituições parciais, remendos de revestimento, recuperação de suportes, restauração de componentes mecânicos ou intervenções em circuitos de comando não podem “sumir” na rotina operacional.

**Fontes da seção:** `anp-226946a12711e04f54ee4bfb:p70-75:9.0-18.0`, `hse-8ae5be797e5471d76a0aa410:p6-9:3.0-0.0`

## 6. Critérios para extensão de vida e operação após longos períodos de inatividade
Quando houver intenção de operar além da vida de projeto, ou quando o histórico de inatividade longa gerar dúvida relevante sobre confiabilidade, a referência da ANP indica que a avaliação deve contemplar, no mínimo:

- **análise de riscos**;
- **avaliação de integridade**;
- histórico operacional, de manutenção, inspeção, testes, ensaios e intervenções;
- verificação das **premissas de projeto** e lacunas em relação a normas atuais;
- reavaliação com base em informações correntes e melhores práticas disponíveis;
- análise de **cargas, tensões, mecanismos e modos de falha**;
- avaliação de **fadiga** quando aplicável;
- análise do histórico de incidentes.

Se faltarem dados ou documentos, a mesma referência recomenda medidas mitigadoras como:

- **inspeções adicionais** para gerar a informação faltante;
- uso de **modelagem numérica avançada** quando pertinente;
- adoção de **premissas conservadoras**.

A HSE complementa que, em fase tardia, a frequência e a profundidade da inspeção podem demandar **recursos adicionais** e que a validade de limites de carregamento e critérios de integridade precisa ser revista à luz da deterioração observada.

**Fontes da seção:** `anp-226946a12711e04f54ee4bfb:p70-75:9.0-18.0`, `hse-8ae5be797e5471d76a0aa410:p6-9:3.0-0.0`

## 7. Indicadores úteis de prontidão e integridade
Com base nas fontes sobre indicadores, manutenção preditiva, backlog e síntese anual, um programa maduro de meios de salvatagem tende a acompanhar pelo menos categorias como:

- anomalias abertas;
- backlog de inspeções e reparos;
- falhas confirmadas em campo;
- intervenções antecipadas por degradação acima do esperado;
- pendências de documentação e rastreabilidade;
- reparos temporários ou de vida definida ainda vigentes.

O valor do indicador não está só no número: ele serve para orientar decisão gerencial, alocação de recursos e reconhecimento precoce de perda de prontidão.

**Fontes da seção:** `anp-b2cfa8a9492ef598716e9685:p37-39:20.0-28.0`, `petroles-004c2afadba7ea17c7dd7908:pNone:525884.0-525932.0`, `hse-8ae5be797e5471d76a0aa410:p6-9:3.0-0.0`

## 8. Consequências de falhas de manutenção
O material de REGIS sobre acidentes da navegação define **mau aparelhamento da embarcação** como falta ou impropriedade de aparelhos, equipamentos, sobressalentes, acessórios e materiais em desacordo com projeto aprovado, boa técnica marinheira e normas técnicas. A mesma fonte destaca que idade, construção, reparo e equipamento técnico influenciam a ocorrência de danos, e que **inspeções regulares** e melhoramentos técnicos são fatores mitigadores de risco.

No contexto de meios de salvatagem, a mensagem é direta: indisponibilidade, degradação escondida, reparo inadequado ou deficiência de equipagem/documentação podem transformar um sistema formalmente existente em um sistema **operacionalmente não confiável**.

**Fontes da seção:** `regis-fe87df28d91f7a2cc8dd24d2:pNone:6819.0-6968.0`

## 9. Síntese operacional
Sob exposição marinha e inatividade, a integridade dos meios de salvatagem depende menos de “cumprir uma rotina” e mais de combinar:

1. **visibilidade do ativo** no sistema de manutenção;
2. **inspeção proporcional à idade, condição e criticidade**;
3. preservação efetiva de **barreiras anticorrosivas**;
4. cuidado com **baterias, óleo, filtros, alinhamento, folgas e vazamentos**;
5. **testes/ensaios após reparos**;
6. **rastreabilidade e qualificação** do que foi modificado;
7. revisão crítica de **anomalias, backlog e reparos temporários**;
8. avaliação estruturada antes de **estender vida** ou recolocar em serviço equipamentos degradados ou muito tempo inativos.

Essa lógica aumenta a probabilidade de que o meio de salvatagem esteja disponível e funcional quando realmente necessário.

**Fontes da seção:** `hse-8ae5be797e5471d76a0aa410:p6-9:3.0-0.0`, `anp-226946a12711e04f54ee4bfb:p70-75:9.0-18.0`, `petroles-4ee4bce16acf674505c8912d:pNone:2025595.0-2025635.0`, `anp-b2cfa8a9492ef598716e9685:p37-39:20.0-28.0`