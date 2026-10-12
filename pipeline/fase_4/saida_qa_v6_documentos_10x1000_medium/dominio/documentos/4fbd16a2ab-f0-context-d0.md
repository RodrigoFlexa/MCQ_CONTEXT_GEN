# Ar comprimido de utilidades

## 1. Função do sistema e contexto em FPSOs
O sistema de ar comprimido integra o conjunto de utilidades que fornece insumos necessários à operação dos sistemas da unidade. No contexto de plataformas e FPSOs, ele aparece como um sistema auxiliar essencial ao funcionamento de consumidores de processo e de utilidades. Em um caso de unidade marítima descrito nas fontes, o sistema possui **três unidades de ar comprimido**, sendo **uma em reserva**, e o ar seco é armazenado em **vaso de ar de serviço** e **vaso de ar de instrumentos**, a partir dos quais é distribuído aos consumidores. Esse arranjo ilustra uma filosofia de redundância e segregação funcional entre os dois serviços, sem que isso deva ser tomado como regra universal para toda instalação.  
**Fontes:** `petroles-4ee4bce16acf674505c8912d:pNone:2060968.0-2060998.0`, `petroles-004c2afadba7ea17c7dd7908:pNone:2160467.0-2160521.0`

### 1.1 Ar de instrumento versus ar de serviço
Os trechos fornecidos não trazem uma definição normativa formal de cada rede, mas o arranjo com vasos separados sugere uma distinção funcional importante:

- **Ar de instrumento**: rede cuja confiabilidade e qualidade tendem a ser mais críticas, pois alimenta atuadores e instrumentos pneumáticos.
- **Ar de serviço**: rede destinada a usos gerais e consumidores menos sensíveis, embora ainda sujeitos a requisitos mínimos de pressão e limpeza.

Do ponto de vista de projeto e operação, a separação de vasos e distribuição ajuda a:

- isolar perturbações de consumo;
- reduzir propagação de condensado e contaminantes entre usos distintos;
- preservar disponibilidade para consumidores mais críticos.

## 2. Qualidade do ar comprimido
A qualidade do ar comprimido é um dos pontos centrais do sistema. As fontes destacam três grupos principais de contaminantes:

- **água condensada**;
- **partículas sólidas**;
- **óleo**.

Esses contaminantes interagem entre si. Partículas sólidas em contato com água ou óleo podem formar aglomerados maiores e depositar-se ou condensar-se na tubulação, aumentando risco de obstrução, mau funcionamento de instrumentos e degradação da qualidade do ar entregue aos consumidores.  
**Fontes:** `regis-ae30be2f70cb5a1ec4c68390:pNone:3502.0-3900.0`, `regis-ae30be2f70cb5a1ec4c68390:pNone:3699.0-4053.0`

### 2.1 Classificação por contaminantes e ponto de orvalho
As fontes referem a **ISO 8573** como base de classificação da qualidade do ar por partículas, água e óleo. O trecho reproduz classes associadas a:

- dimensão/concentração de partículas;
- ponto de orvalho máximo;
- teor total de óleo.

Mesmo sem assumir a tabela reproduzida como referência normativa atual para uso contratual, ela é útil para raciocínio de engenharia: a especificação do sistema deve explicitar, para cada rede ou consumidor crítico, pelo menos:

- limite de umidade, frequentemente expresso como **ponto de orvalho**;
- limite de partículas;
- limite de óleo líquido, aerossol e/ou vapores.

### 2.2 Relevância do ponto de orvalho
O secador deve ser selecionado conforme o **ponto de orvalho esperado/requerido**. As fontes destacam que o controle do ponto de orvalho evita que condensados entrem na rede e protege os componentes a jusante. Em termos operacionais, isso significa que a qualidade do ar não deve ser avaliada apenas na descarga do compressor, mas no regime real da rede, incluindo pressão e trechos onde o ar pode resfriar.  
**Fontes:** `petroles-4ee4bce16acf674505c8912d:pNone:887738.0-887777.0`, `regis-ae30be2f70cb5a1ec4c68390:pNone:3699.0-4053.0`

## 3. Cadeia de tratamento do ar comprimido
Os trechos permitem compor uma cadeia típica de tratamento do ar comprimido, com o objetivo de entregar ar seco, com baixo teor de partículas e baixo teor de óleo.

### 3.1 Resfriamento pós-compressão e remoção inicial de condensado
O primeiro passo após a compressão é reduzir a temperatura do ar na saída do compressor. As fontes indicam que essa temperatura pode chegar a cerca de **150 °C**, sendo o resfriamento feito por **aftercoolers** a ar ou a água. Além de reduzir temperatura, o resfriamento remove parte importante da água contida no ar, com formação de condensado conduzido a purgadores.  
**Fontes:** `regis-ae30be2f70cb5a1ec4c68390:pNone:3502.0-3900.0`

Consequências práticas:

- diminuição da carga térmica sobre o secador;
- remoção de parcela significativa da umidade antes das etapas finas de tratamento;
- redução do risco de condensação na rede e nos vasos.

### 3.2 Secadores de ar
As fontes distinguem secagem para **pontos de orvalho positivos** e para **pontos de orvalho negativos**.

#### a) Secadores de refrigeração
São indicados quando se deseja ponto de orvalho positivo, com limite citado de aproximadamente **+3 °C** no trecho. A seleção depende de cinco itens explicitados na fonte:

- débito efetivo de ar comprimido a ser tratado;
- pressão normal de trabalho;
- temperatura ambiente;
- temperatura do ar comprimido na entrada do secador;
- ponto de orvalho ou classe de ar pretendida.

Isso é diretamente aplicável a FPSO porque a carga térmica, a pressão da rede e a condição ambiente influenciam capacidade real do secador.  
**Fonte:** `regis-ae30be2f70cb5a1ec4c68390:pNone:3699.0-4053.0`

#### b) Secadores de adsorção
Quando se exige ponto de orvalho negativo, as fontes indicam o uso de secadores com dessecantes. São citados materiais e faixas típicas de desempenho:

- **silicagel**: cerca de **-20 °C**;
- **alumina ativada**: cerca de **-40 °C**;
- **peneira molecular**: cerca de **-70 °C**.

A regeneração do dessecante é descrita como sendo feita com pequena fração do próprio ar comprimido seco, da ordem de **10%**.  
**Fonte:** `regis-ae30be2f70cb5a1ec4c68390:pNone:4057.0-4375.0`

#### c) Critério prático de decisão
Com base nas fontes, a escolha do secador depende principalmente de:

- ponto de orvalho requerido pelo consumidor;
- risco de condensação ou congelamento a jusante;
- vazão efetiva e pressão de trabalho;
- condição térmica de entrada do ar no secador.

Em termos de fornecimento e qualidade, o secador não deve ser avaliado isoladamente: sua capacidade precisa ser compatível com a vazão do compressor em operação e com cenários de pico ou contingência.

### 3.3 Filtração
As fontes descrevem diversas camadas possíveis de filtração.

#### a) Separadores de condensado
São elementos mecânicos, normalmente instalados entre compressores e depósitos, que removem gotas de água pela mudança brusca de direção do escoamento, frequentemente com entrada tangencial para induzir rotação helicoidal do fluxo.  
**Fonte:** `regis-ae30be2f70cb5a1ec4c68390:pNone:4057.0-4375.0`

#### b) Filtros de superfície
Retêm partículas maiores que os poros do elemento. As fontes indicam aplicação típica para partículas até **1 µm**, com boa eficácia até **5 µm**, dependendo da configuração. Em linhas pressurizadas, é citado o arranjo de dentro para fora do elemento.  
**Fonte:** `regis-ae30be2f70cb5a1ec4c68390:pNone:4057.0-4375.0`

#### c) Filtros de profundidade / microfiltração
São destinados a partículas menores, chegando a retenções muito finas. A fonte cita retenção de partículas até **0,01 µm** em elementos de profundidade, com elevada eficiência.  
**Fonte:** `regis-ae30be2f70cb5a1ec4c68390:pNone:4057.0-4375.0`

#### d) Filtros coalescentes
Outro trecho descreve filtros coalescentes como equipamentos de alta eficiência para gases, capazes de separar óleo e água por coalescência de aerossóis em gotas, com baixa perda de carga e retenção de partículas finas. Em uma configuração de tratamento de ar comprimido, são citados:

- **pré-filtro**;
- **coalescente fino**;
- **coalescente superfino**;
- **secador**.

Essa lógica é particularmente relevante quando o compressor pode arrastar contaminantes do ar ambiente e traços de óleo.  
**Fontes:** `petroles-4ee4bce16acf674505c8912d:pNone:887720.0-887757.0`, `petroles-4ee4bce16acf674505c8912d:pNone:887738.0-887777.0`

#### e) Filtros de carvão ativado
São citados como elementos de absorção com camada de carvão ativado para retenção de vapores de óleo e odores, com finalidade de obtenção de ar tecnicamente isento de óleo e inodoro.  
**Fonte:** `petroles-4ee4bce16acf674505c8912d:pNone:887738.0-887777.0`

### 3.4 Encadeamento do tratamento
A partir das fontes, um encadeamento tecnicamente coerente para avaliação de suprimento e qualidade é:

1. compressão;
2. resfriamento pós-compressão;
3. remoção de condensado;
4. filtração preliminar/coalescente;
5. secagem;
6. filtração fina e, se necessário, polimento com carvão ativado;
7. armazenamento em vaso;
8. distribuição à rede.

O objetivo não é apenas atender à vazão, mas impedir que água, óleo e partículas se propaguem para vasos, tubulação e instrumentos.

## 4. Armazenamento e distribuição
Em um caso de FPSO citado, o ar seco é armazenado em **vaso de ar de serviço** e **vaso de ar de instrumentos**, antes da distribuição. O vaso cumpre papel de amortecimento de demanda, estabilização de pressão e desacoplamento parcial entre compressores/tratamento e consumidores.  
**Fonte:** `petroles-004c2afadba7ea17c7dd7908:pNone:2160467.0-2160521.0`

### 4.1 Arranjos de rede
As fontes sobre redes de ar comprimido citam duas possibilidades:

- **anel aberto**;
- **anel fechado**.

O anel fechado é apresentado como vantajoso por fornecer ar a qualquer ponto a partir de ambos os sentidos do anel, favorecendo equilíbrio de fornecimento. Para FPSOs, essa observação é útil para discutir robustez de distribuição e sensibilidade a perdas localizadas, ainda que o arranjo final dependa do layout da planta e dos consumidores.  
**Fonte:** `regis-ae30be2f70cb5a1ec4c68390:pNone:4057.0-4375.0`

### 4.2 Parâmetros de dimensionamento de tubulação
O trecho informa que o dimensionamento requer, no mínimo:

- caudal/vazão;
- pressão de funcionamento;
- distância até o ponto mais desfavorável.

O próprio excerto indica que havia ainda outro parâmetro necessário, mas ele não aparece integralmente no material fornecido. Logo, o documento preserva apenas o que está visível na fonte.  
**Fonte:** `regis-ae30be2f70cb5a1ec4c68390:pNone:4057.0-4375.0`

## 5. Controle operacional, proteção e filosofia de disponibilidade
### 5.1 Redundância
No caso de unidade marítima descrito, há **três unidades de ar comprimido**, com **uma em reserva**. Isso exemplifica uma filosofia de disponibilidade na qual a perda de uma máquina não elimina automaticamente o suprimento, desde que capacidade remanescente e sistema de tratamento sejam compatíveis.  
**Fonte:** `petroles-004c2afadba7ea17c7dd7908:pNone:2160467.0-2160521.0`

### 5.2 Modos de carga do compressor
Um trecho sobre compressor rotativo de parafuso descreve três estados de operação:

- **carga plena**;
- **carga parcial**;
- **alívio**.

A transição entre esses estados é comandada por **pressostatos**, de modo a evitar subpressão e sobrepressão. No exemplo:

- ao atingir um ajuste de pressão, a válvula de admissão fecha e o compressor migra para carga parcial;
- se o consumo superar a produção nessa condição, a pressão cai e o compressor retorna à carga plena;
- se o consumo permanecer abaixo da produção parcial, a pressão volta a subir e o compressor entra em alívio, sem produção útil para a rede.

Embora esse trecho seja de um equipamento específico, ele é útil para raciocinar sobre controle de capacidade e estabilidade de pressão em redes de ar comprimido.  
**Fonte:** `petroles-4ee4bce16acf674505c8912d:pNone:334707.0-334749.0`

### 5.3 Proteções e intertravamentos
No mesmo exemplo, são citados:

- monitoramento de **pressão da rede** por manômetro;
- monitoramento de **temperatura de descarga**;
- **desligamento por termostato** em alta temperatura;
- **botão de emergência** para parada imediata;
- proteção elétrica por **relé de falta e sequência de fase**.

Esses elementos ilustram uma camada básica de proteção do compressor e podem ser associados a estratégias de monitoramento e intertravamento no sistema de utilidades.  
**Fonte:** `petroles-4ee4bce16acf674505c8912d:pNone:334707.0-334749.0`

### 5.4 Interface com outros sistemas de utilidades
Em um caso descrito, o sistema de água de resfriamento em circuito fechado atende, entre outros consumidores, o **compressor de ar de instrumento** e o **compressor de ar de partida**. Isso evidencia um ponto importante de confiabilidade: perda ou degradação de utilidade de resfriamento pode comprometer disponibilidade do ar comprimido.  
**Fonte:** `petroles-004c2afadba7ea17c7dd7908:pNone:2160467.0-2160521.0`

## 6. Monitoramento de desempenho e qualidade
### 6.1 Monitoramento de partículas
As fontes destacam a utilidade de **contador de partículas em tempo real** para gases sob pressão. O instrumento permite detectar, quantificar e alarmar a presença de partículas, inclusive em situações de:

- sobrecarga de filtros;
- erro operacional;
- acidentes;
- falha de manutenção;
- geração de partículas a jusante dos filtros.

Isso é particularmente útil para troubleshooting, porque o problema nem sempre está na sucção ou no compressor; pode estar em desprendimento interno de material, saturação de filtro, drenagem deficiente ou contaminação introduzida após manutenção.  
**Fontes:** `petroles-4ee4bce16acf674505c8912d:pNone:887720.0-887757.0`, `petroles-4ee4bce16acf674505c8912d:pNone:887738.0-887777.0`

### 6.2 Medição a montante e a jusante
No arranjo experimental descrito, o contador de partículas é ligado na entrada e na saída do filtro para cálculo de eficiência do meio filtrante, e há também uso de **manômetro diferencial** no filtro de linha. Como princípio de monitoramento, isso permite avaliar:

- eficiência instantânea do elemento filtrante;
- degradação ou colmatação do filtro;
- ocorrência de by-pass interno ou passagem preferencial;
- necessidade de manutenção antes de falha funcional evidente.  
**Fonte:** `petroles-4ee4bce16acf674505c8912d:pNone:887758.0-887796.0`

### 6.3 Variáveis críticas para acompanhamento
Com base nos trechos, as variáveis mais diretamente associadas ao suprimento e à qualidade do ar são:

- pressão da rede;
- temperatura de descarga do compressor;
- ponto de orvalho do ar seco;
- diferencial de pressão em filtros;
- presença de partículas;
- evidência de água/óleo na linha ou nos vasos.

## 7. Comissionamento e aceitação funcional
O material não traz um procedimento completo de comissionamento de FPSO, mas sustenta alguns pontos de verificação funcional indispensáveis:

1. **confirmar o ponto de orvalho entregue pelo secador** na condição de operação relevante;
2. **verificar a remoção de condensado** após compressão e resfriamento;
3. **testar eficiência de filtração** por diferencial de pressão e, quando aplicável, por amostragem/contagem de partículas;
4. **confirmar segregação e pressurização dos vasos** de ar de serviço e ar de instrumentos;
5. **testar transições automáticas do compressor** entre carga plena, parcial e alívio, quando essa filosofia existir;
6. **confirmar atuação de proteções** por alta temperatura, emergência e falhas elétricas;
7. **avaliar a resposta da rede** em cenários de mudança de consumo e indisponibilidade de uma unidade compressora.

## 8. Falhas típicas, efeitos e solução de problemas
### 8.1 Umidade excessiva na rede
Possíveis causas apoiadas nas fontes:

- falha ou subdimensionamento do secador;
- ar de entrada no secador mais quente que o previsto;
- drenagem/purgadores ineficazes após aftercooler ou separadores;
- condensação ao longo da rede por ponto de orvalho inadequado.

Efeitos prováveis:

- entrada de condensado na rede;
- contaminação de instrumentos e válvulas pneumáticas;
- deposição junto com partículas e óleo na tubulação.

### 8.2 Óleo no ar de instrumento/serviço
Possíveis causas:

- arraste do compressor;
- saturação ou ineficiência do coalescente;
- ausência de estágio de carvão ativado quando necessário ao serviço.

Efeitos prováveis:

- contaminação da rede e de equipamentos a jusante;
- odor e degradação da qualidade do ar;
- maior tendência a formação de depósitos com sólidos.

### 8.3 Partículas a jusante dos filtros
As fontes alertam que partículas podem surgir mesmo após filtragem, por sobrecarga, erro, acidentes, má manutenção ou geração a jusante do elemento. O diagnóstico favorece:

- medição on-line por contador de partículas;
- comparação entrada/saída do filtro;
- inspeção de manutenção recente e integridade do elemento filtrante.

### 8.4 Pressão instável ou capacidade insuficiente
O trecho sobre compressor mostra que a lógica de carga/plena/parcial/alívio afeta diretamente a pressão disponível. Assim, pressão instável pode estar associada a:

- ajuste inadequado dos pressostatos;
- desequilíbrio entre produção do compressor e consumo da rede;
- compressor preso em alívio ou em faixa inadequada de controle;
- indisponibilidade de uma unidade sem capacidade remanescente suficiente.

### 8.5 Alta temperatura de descarga
No exemplo apresentado, alta temperatura aciona proteção por termostato e desliga o compressor. Em termos de troubleshooting, isso exige verificação da condição térmica do compressor e de suas utilidades associadas, especialmente resfriamento.  
**Fontes:** `petroles-4ee4bce16acf674505c8912d:pNone:334707.0-334749.0`, `petroles-004c2afadba7ea17c7dd7908:pNone:2160467.0-2160521.0`

## 9. Manutenção, integridade e otimização
Com base nas fontes, boas práticas de manutenção e integridade para o sistema incluem:

- manutenção dos elementos de drenagem e remoção de condensado;
- troca/inspeção de filtros conforme diferencial de pressão e qualidade do ar entregue;
- verificação da regeneração e condição do dessecante em secadores de adsorção;
- inspeção de válvulas e dispositivos de proteção em linhas pressurizadas;
- acompanhamento de temperatura, pressão e contagem de partículas para manutenção preditiva;
- avaliação periódica da filosofia de redundância, especialmente quando uma unidade permanece em reserva.

Sob a ótica de otimização, a seleção correta do secador e da cadeia de filtração evita tratamento excessivo ou insuficiente. Também reduz consumo indireto de energia e manutenção corretiva, ao limitar arraste de água e óleo para a rede.

## 10. Síntese técnica para avaliação profissional
Os trechos permitem avaliar o sistema de ar comprimido de utilidades em FPSO a partir de um núcleo de decisões técnicas:

- se a **capacidade instalada e a redundância** são coerentes com a criticidade dos consumidores;
- se a **qualidade especificada** do ar considera água, partículas e óleo;
- se o **ponto de orvalho** exigido é compatível com a tecnologia de secagem escolhida;
- se a **sequência de tratamento** é compatível com os contaminantes esperados;
- se o **armazenamento e a distribuição** protegem o ar de instrumento contra perturbações do ar de serviço;
- se as **malhas de controle, alarmes e proteções** preservam a disponibilidade do sistema;
- se o **monitoramento** permite detectar degradação antes de perda funcional ou contaminação do processo.

Em resumo, suprimento e qualidade de ar de instrumento e ar de serviço não dependem apenas do compressor. Dependem do conjunto compressor-resfriamento-drenagem-secagem-filtração-armazenamento-distribuição, mais a filosofia de controle e manutenção associada.