# Capacidade e continuidade das utilidades

## 1. Escopo técnico e premissas de aplicação

A continuidade das utilidades em um FPSO não depende apenas da capacidade nominal do equipamento principal. Na prática, a disponibilidade do serviço resulta da combinação entre:

- capacidade instalada e capacidade efetivamente utilizável em regime normal, transiente e contingência;
- integridade das redes e dos elementos críticos associados;
- confiabilidade dos sistemas de medição, controle, proteção e interface com o SDCD/automação;
- tempo de diagnóstico e reparo em ambiente offshore;
- filosofia de redundância, sobressalentes e manutenção.

Os trechos disponíveis sustentam principalmente princípios de confiabilidade/disponibilidade aplicáveis a equipamentos críticos offshore, com maior detalhamento para compressores centrífugos e para sistemas acionados por VFD. Esses princípios são úteis para utilidades críticas como compressores de ar/nitrogênio, sistemas com vasos, válvulas de reciclo, redes de gás inerte e tubulações auxiliares, desde que aplicados com análise específica de cada pacote e instalação. [Fontes: `anp-b2cfa8a9492ef598716e9685:p52-54:15.0-0.0`, `regis-f8686f0be4025804d5448444:pNone:50.60-89.0`, `regis-cf9083b7fb6d77ade93a9431:pNone:0.0-40.0`, `regis-cf9083b7fb6d77ade93a9431:pNone:741.60-771.0`]

## 2. Capacidade útil, criticidade e filosofia de continuidade

### 2.1 Continuidade deve ser tratada como requisito de projeto, não apenas de operação

Em instalações offshore remotas, paradas não programadas de equipamentos críticos geram perda direta de produção e podem demandar mobilização de especialista, elevando fortemente o MTTR. Por isso, a filosofia de continuidade deve ser definida ainda na fase de projeto e especificação técnica, considerando:

- criticidade do serviço para produção e segurança;
- lucro cessante associado à indisponibilidade;
- dificuldade de acesso a bordo e mobilização de mão de obra especializada;
- espaço físico disponível para redundância ou equipamentos reserva;
- número de consumidores/equipamentos equivalentes na unidade;
- possibilidade de manutenção por oportunidade em paradas programadas.

Nos casos estudados de equipamentos offshore críticos, a viabilidade e o ganho de redundância dependeram fortemente do contexto da unidade. O material enfatiza que soluções para aumento de disponibilidade precisam ser avaliadas caso a caso, durante o projeto, e não transplantadas como regra geral entre instalações. [Fontes: `regis-cf9083b7fb6d77ade93a9431:pNone:0.0-40.0`, `regis-cf9083b7fb6d77ade93a9431:pNone:741.60-771.0`]

### 2.2 Capacidade nominal não garante continuidade

A análise de disponibilidade de um sistema crítico não deve se limitar ao equipamento principal. O histórico de falhas usado no estudo de VFD mostrou que a indisponibilidade real pode ser dominada por subsistemas de controle, medição e interface com automação, mesmo quando a etapa principal do equipamento é robusta. Em termos de utilidades, isso significa que a capacidade de um compressor, secador, sistema de nitrogênio ou rede auxiliar só é efetiva se também estiver assegurada a disponibilidade de:

- alimentação auxiliar confiável dos sistemas de controle;
- instrumentos e transmissores essenciais;
- lógica de proteção e interface com SDCD/PLC;
- atuadores e válvulas críticas;
- ventilação/exaustão, quando requerida pelo pacote;
- peças sobressalentes preservadas a bordo.

Essa visão amplia o conceito de “capacidade” para capacidade sustentada com controle e proteção operantes. [Fontes: `regis-cf9083b7fb6d77ade93a9431:pNone:539.0-572.0`, `regis-cf9083b7fb6d77ade93a9431:pNone:741.60-771.0`]

## 3. Redundância: onde ela agrega mais disponibilidade

### 3.1 Redundância do equipamento principal versus redundância dos auxiliares e do controle

Os dados empíricos do estudo de VFD mostraram que nem sempre o maior ganho de disponibilidade vem da duplicação do “bloco principal” do equipamento. Falhas de potência modular tiveram MTTR menor e, em certos casos, puderam ser contornadas por bypass e modularidade. Em contraste, falhas de sistema de controle e de interface com automação geraram tempos de parada mais altos. Os MTTRs observados foram:

- células de potência: **25,82 h**;
- sistema de controle: **34,18 h**;
- interface com automação: **64,70 h**.

Além disso, quando havia sobressalente adequado a bordo, o tempo de retorno após falha em célula podia cair para **4,59 h**; sem sobressalente, um único evento elevou o TTR para **68,3 h**. A lição transferível para utilidades é direta: redundância e estratégia de reserva devem contemplar também controle, instrumentação, cartões de interface, fontes auxiliares e sobressalentes críticos, e não apenas compressores, bombas ou geradores de gás. [Fontes: `regis-cf9083b7fb6d77ade93a9431:pNone:592.0-621.0`, `regis-cf9083b7fb6d77ade93a9431:pNone:741.60-771.0`]

### 3.2 Critérios práticos de decisão

O material disponível sustenta os seguintes critérios de decisão para utilidades críticas:

1. **Alta consequência + alto MTTR + local remoto** → justificar maior nível de redundância e melhor gestão de sobressalentes.
2. **Falha catastrófica com reparo muito longo** → redundância total pode ser a única forma de retorno rápido.
3. **Equipamentos modulares com bypass/reconfiguração** → podem reduzir necessidade de duplicação integral, desde que os modos degradados sejam aceitáveis.
4. **Grande participação de falhas de controle/automação no downtime** → redundância de controle e de interface pode ser mais eficaz que apenas duplicar o equipamento principal.
5. **Espaço e arranjo a bordo limitados** → exigem avaliação técnico-econômica específica; a melhor solução pode variar com o número de consumidores atendidos e com a vazão/capacidade requerida.

O estudo citado simulou, para uma aplicação específica de VFD, que um conversor reserva para cada cinco operacionais poderia ser uma boa técnica em unidades com grande número de poços. Esse resultado é útil como exemplo metodológico, mas não deve ser convertido diretamente em regra para compressores, secadores ou bombas de utilidades sem estudo próprio. [Fontes: `regis-cf9083b7fb6d77ade93a9431:pNone:741.60-771.0`, `regis-cf9083b7fb6d77ade93a9431:pNone:592.0-621.0`]

## 4. Controle anti-surge e requisitos de resposta para compressores críticos

Para compressores centrífugos aplicados a serviços de utilidades, o controle anti-surge é um elemento central da continuidade operacional. O material fornece requisitos de projeto e comissionamento importantes:

### 4.1 Implementação do controle

- O controle anti-surge deve ser implementado por estágio quando a máquina tiver mais de um estágio.
- O projeto deve se basear nas curvas de desempenho da máquina, em unidades de engenharia.
- O algoritmo deve operar em equipamento digital com capacidade de execução em intervalos **menores que 100 ms**.
- O sistema pode operar em manual, com a válvula de reciclo comandada pelo SDCD por sinal físico **4–20 mA**.
- Se houver ameaça de surge e a válvula não estiver em manutenção, a lógica deve assumir automaticamente a posição da válvula de reciclo por estratégia de override.

### 4.2 Requisitos dinâmicos e de instrumentação

- Recomenda-se **tempo máximo de resposta dos transmissores de 100 ms**.
- Recomenda-se **linhas de impulso inferiores a 2 m**.
- A constante de tempo de abertura da válvula de reciclo deve ser **menor que 2 s**.
- A válvula de reciclo deve ser preferencialmente do tipo **globo** com característica inerente linear, posicionador, booster e indicação de posição da haste; válvula de **esfera segmentada** com característica inerente linear também é aceita.
- Quando houver possibilidade de condensado, a válvula deve ser instalada de forma a evitar acúmulo de líquido na linha de reciclo, pois isso prejudica a dinâmica do controle.

### 4.3 Filosofia em falha de instrumentos

- Em falha de transmissor de pressão participante dos cálculos, o controle anti-surge deve operar com o **valor de projeto** do sinal afetado.
- Em falha do sinal de vazão, a válvula de reciclo deve ir automaticamente para uma **posição predeterminada**, o controle deve ir para **manual** e um **alarme** deve ser gerado.
- Todos os parâmetros do controle devem estar indicados em **unidades de engenharia**.

### 4.4 Medição de vazão

- Deve ser medida a vazão de cada estágio e a vazão de reciclo.
- O diferencial de pressão dos medidores da linha de reciclo deve ser o mais baixo possível para não prejudicar o desempenho do controle.
- Quando a curva do compressor for dada em função da vazão de sucção, uma vazão medida na descarga de um estágio deve ser convertida para as condições de sucção.
- Devem ser evitadas tecnologias de medição sensíveis à vibração, como **Coriolis** e medição por **vórtices**.
- Preferencialmente usar tecnologias por **diferencial de pressão**, como **placa de orifício** ou **tubo de Venturi**; o texto também desaconselha medição por **annubar**.

Esses requisitos afetam diretamente a capacidade real da máquina de permanecer operando sem trips indevidos nem aproximação ao surge durante partidas, mudanças de carga e perturbações de processo. [Fonte: `regis-f8686f0be4025804d5448444:pNone:50.60-89.0`]

## 5. Intertravamentos, proteção e continuidade segura

### 5.1 Separar controle operacional de funções de segurança

O subsistema de intertravamento é responsável por ações automáticas quando a integridade física do equipamento está em risco, incluindo paradas de emergência. O material ressalta que:

- essas ações devem ser tratadas como **funções de segurança**;
- a classificação **SIL** se aplica às **malhas de segurança**, não isoladamente a sensores ou atuadores;
- sensores e atuadores devem ser especificados para atender ao nível de integridade exigido da malha.

No exemplo de compressor centrífugo, funções típicas incluíram nível alto em vasos de sucção, sobrevelocidade, alta temperatura de descarga, baixa pressão de óleo lubrificante, baixa pressão de gás de selagem, deslocamento axial alto e vibração alta. Para utilidades, a lista específica varia conforme o pacote, mas o princípio é o mesmo: a filosofia de continuidade deve preservar a operação sempre que possível, sem comprometer a função de segurança. [Fonte: `regis-f8686f0be4025804d5448444:pNone:50.60-89.0`]

### 5.2 Votação, redundância e falhas de causa comum

No exemplo apresentado para compressores, com exceção dos sensores de vibração **1oo1** e sobrevelocidade **2oo3**, os iniciadores de funções de segurança devem ter redundância **2oo2** com alarme de discrepância; se um sensor falhar, o esquema pode degradar para **1oo1**.

Entretanto, o material histórico sobre intertravamentos alerta que redundância “direta” com sensores da mesma natureza pode não ser a melhor resposta contra falhas de causa comum. Dois sensores iguais, instalados na mesma condição de processo, podem falhar em conjunto ou deixar de capturar um modo de falha fora da hipótese considerada. Assim, para utilidades críticas, a redundância deve ser analisada não apenas pela quantidade de sensores, mas por:

- diversidade de princípio de detecção, quando pertinente;
- independência física/funcional entre canais;
- cobertura de modos de falha reais;
- eliminação de pontos únicos de falha em alimentação e lógica;
- facilidade de manutenção sem perda indevida de proteção.

Outro ponto relevante é que o desenho do sistema de proteção não deve considerar apenas os “limites de bateria” do equipamento. Um trip correto para o pacote isolado pode ser inadequado para a instalação como um todo se provocar consequências piores a jusante ou montante. [Fontes: `regis-f8686f0be4025804d5448444:pNone:50.60-89.0`, `regis-4128d9e14c5ae32994a8678d:pNone:43.60-86.0`]

## 6. Principais causas de indisponibilidade: lições úteis para utilidades offshore

Os casos reais analisados em equipamentos offshore críticos mostram padrões muito úteis para utilidades:

### 6.1 Falhas de controle e alarmes pouco diagnósticos ampliam o downtime

Um caso de falha em placa microprocessadora de controle gerou alarme genérico (“internal trip”) e levou a **41,35 h** de parada, em grande parte pelo tempo gasto para identificar a causa. Outro caso, em cartão de saída digital do sistema de interface com a sala de controle, impediu a produção por **72 h**, pois o sinal de partida era perdido intermitentemente, produzindo desligamentos com indicação pouco conclusiva (“stop”).

Esses casos mostram que, para utilidades críticas, o projeto deve buscar:

- alarmes diagnósticos claros e específicos;
- segregação entre falhas de processo, falhas de proteção e falhas de interface;
- redução da dependência de único cartão/sinal para permissivos essenciais;
- possibilidade de comutação rápida para canal ou controle alternativo;
- documentação e treinamento adequados para a equipe de bordo.

### 6.2 Modularidade e bypass podem reduzir muito o MTTR

Em outro caso, uma falha de célula de potência por problema em conector de fibra ótica foi contornada com **bypass manual** e retorno à operação em **3,43 h**, deixando a substituição definitiva para uma parada programada. A lógica transferível é que recursos de reconfiguração, bypass seguro ou modo degradado podem preservar continuidade sem eliminar a necessidade de reparo definitivo.

### 6.3 Sobressalentes a bordo são parte da arquitetura de disponibilidade

A diferença entre reparar rapidamente e manter longa parada pode ser simplesmente a existência do sobressalente correto, preservado e disponível. Isso é aplicável a cartões eletrônicos, transmissores, atuadores, módulos de controle e componentes de pacote de utilidades. [Fontes: `regis-cf9083b7fb6d77ade93a9431:pNone:592.0-621.0`, `regis-cf9083b7fb6d77ade93a9431:pNone:539.0-572.0`, `regis-cf9083b7fb6d77ade93a9431:pNone:741.60-771.0`]

## 7. Integridade de redes e elementos críticos de utilidades

O relatório da ANP destaca que a dificuldade da indústria em garantir disponibilidade e integridade de elementos críticos permanece relevante. Em instalações offshore, foram apontados desvios como:

- sistemas críticos degradados;
- falhas de manutenção em UPS;
- obstrução e baixa vazão em sistemas de dilúvio e drenagem;
- falhas na integridade de tubulações de **gás inerte**, **gás combustível**, **gas lift** e drenagem;
- reparos temporários sem evidência de atendimento a parâmetros normativos de engenharia;
- inspeções vencidas e, em casos extremos, sistemas que jamais haviam sido inspecionados ao longo da vida produtiva da unidade;
- falhas de gestão de mudanças com modificações relevantes sem reavaliação adequada de risco.

Para utilidades, isso reforça que continuidade operacional não pode ser dissociada de integridade mecânica e disciplina de gestão. Redes de distribuição, vasos, tubulações e sistemas auxiliares precisam de:

- plano de inspeção com rastreabilidade e execução tempestiva;
- critérios formais para reparos temporários e limitação de prazo/condição de uso;
- contingências definidas para falha de elemento crítico;
- gestão de mudanças sempre que alterações físicas ou funcionais modificarem riscos, capacidade ou desempenho do sistema;
- auditorias e indicadores que efetivamente revelem degradação antes do vazamento ou da perda funcional.

Em síntese, capacidade sem integridade documentada é capacidade apenas nominal. [Fonte: `anp-b2cfa8a9492ef598716e9685:p52-54:15.0-0.0`]

## 8. Comissionamento e prontidão operacional

Com base nos trechos disponíveis, um comissionamento orientado à continuidade das utilidades deve verificar, no mínimo:

1. **Resposta dinâmica do controle crítico**: por exemplo, levantamento da curva real de surge na partida e validação dos tempos de resposta de transmissores, válvulas e algoritmo de controle.
2. **Lógica de falha de instrumentos**: comprovar posições seguras, uso de valores de projeto quando previsto, transição para manual e geração de alarmes.
3. **Intertravamentos e votação**: validar a lógica de trip, alarmes de discrepância e o comportamento degradado em falha de um canal.
4. **Diagnose e alarmística**: garantir que a indicação ao operador seja suficientemente específica para reduzir tempo de identificação de falha.
5. **Fontes auxiliares**: confirmar a confiabilidade da alimentação do controle e dos auxiliares essenciais do pacote.
6. **Sobressalentes e preservação**: verificar disponibilidade e condição de itens críticos para pronta intervenção.
7. **Modos de contingência**: comprovar se o pacote consegue operar em modo degradado ou com bypass previsto, e sob quais limitações.

Esses pontos são coerentes com a experiência de campo apresentada: falhas de interface e controle podem dominar a indisponibilidade, enquanto recursos de modularidade e reconfiguração podem reduzir fortemente o impacto operacional. [Fontes: `regis-f8686f0be4025804d5448444:pNone:50.60-89.0`, `regis-cf9083b7fb6d77ade93a9431:pNone:539.0-572.0`, `regis-cf9083b7fb6d77ade93a9431:pNone:592.0-621.0`, `regis-cf9083b7fb6d77ade93a9431:pNone:741.60-771.0`]

## 9. Síntese operacional para resposta a falhas

Quando ocorre perda parcial ou total de uma utilidade crítica, a resposta técnica tende a ser melhor quando o projeto já contemplou os seguintes princípios:

- **preservar a função segura** sem provocar trips desnecessários por baixa qualidade diagnóstica;
- **priorizar consumidores essenciais** e reconhecer os impactos de falhas comuns;
- **evitar pontos únicos de falha** em alimentação auxiliar, interface e proteção;
- **prever redundância onde o ganho de disponibilidade é real**, inclusive no controle;
- **empregar modularidade, bypass e manutenção por oportunidade** quando compatíveis com segurança e desempenho;
- **tratar inspeção, reparo temporário e gestão de mudanças como parte da continuidade**, não apenas da conformidade.

Em ambientes offshore, a principal mensagem dos trechos analisados é que disponibilidade sustentada depende menos de “superdimensionar” um pacote isolado e mais de projetar o sistema completo — máquina, controle, proteção, rede, integridade e suporte de manutenção — para falhar de forma controlada, ser diagnosticado rapidamente e retornar ao serviço com o menor MTTR possível. [Fontes: `anp-b2cfa8a9492ef598716e9685:p52-54:15.0-0.0`, `regis-f8686f0be4025804d5448444:pNone:50.60-89.0`, `regis-4128d9e14c5ae32994a8678d:pNone:43.60-86.0`, `regis-cf9083b7fb6d77ade93a9431:pNone:539.0-572.0`, `regis-cf9083b7fb6d77ade93a9431:pNone:592.0-621.0`, `regis-cf9083b7fb6d77ade93a9431:pNone:741.60-771.0`]