# Águas utilitárias e potáveis

Este documento consolida conceitos de projeto, operação e integridade aplicáveis à geração, tratamento, armazenamento e distribuição de águas utilitárias em instalações de óleo e gás, com ênfase em água doce, potável, de serviço e técnica. As fontes disponíveis são majoritariamente de refinarias e de dessalinização em terra; portanto, o texto deve ser lido como **base técnica de engenharia por analogia**, não como descrição universal de todos os FPSOs/FSOs. *(Fontes gerais: `petroles-004c2afadba7ea17c7dd7908:pNone:398803.60-398833.0`, `petroles-004c2afadba7ea17c7dd7908:pNone:3247173.60-3247210.0`, `petroles-4ee4bce16acf674505c8912d:pNone:1727055.0-1727091.0`, `petroles-4ee4bce16acf674505c8912d:pNone:1727161.0-1727190.0`, `regis-195418cbcd17f97ab5f87ea2:pNone:4763.0-5120.0`, `regis-3d703c296545505228102293:pNone:2759.0-2961.0`)*

## 1. Classes de água e funções utilitárias

Os trechos consultados distinguem, ao menos, as seguintes classes funcionais de água:

- **Água bruta**: água captada da fonte primária, antes do tratamento.
- **Água clarificada**: água após remoção de sólidos suspensos em clarificação/coagulação.
- **Água filtrada / industrial**: água após filtração, destinada a parte relevante dos usos utilitários e de processo.
- **Água desmineralizada**: água com forte remoção de sais dissolvidos, usualmente para serviços mais exigentes, como geração de vapor.
- **Água potável**: água destinada ao consumo humano, obtida a partir de água tratada e submetida a desinfecção adicional.
- **Água de serviço / técnica**: água para usos auxiliares diversos, como lavagens, diluições, deslocamentos de líquidos e, conforme a instalação, reposição de perdas em alguns sistemas. 

Nos documentos de referência, os maiores consumidores industriais de água são os sistemas de **resfriamento** e de **geração de vapor**, seguidos de usos de processo, combate a incêndio, potável e serviço. Em um arranjo de utilidades, isso é importante porque a vazão de água doce/potável não deve ser analisada isoladamente: o balanço total depende da segmentação por qualidade e do perfil dos consumidores. *(Fontes: `petroles-004c2afadba7ea17c7dd7908:pNone:398803.60-398833.0`, `regis-195418cbcd17f97ab5f87ea2:pNone:4763.0-5120.0`)*

### Implicação para FPSO/FSO
Em contexto offshore, a engenharia de utilidades deve mapear consumidores por **classe de qualidade**, evitando especificar água de qualidade superior onde água de serviço seria suficiente. Isso reduz carga de tratamento, consumo químico, descarte de rejeitos e custo global do sistema. Essa conclusão decorre diretamente do fato, explicitado nas fontes, de que os **requisitos de qualidade variam conforme o uso**. *(Fonte: `petroles-004c2afadba7ea17c7dd7908:pNone:3247173.60-3247210.0`)*

## 2. Qualidade da água de alimentação e seleção do tratamento

A qualidade da água de entrada condiciona o trem de tratamento. As fontes listam contaminantes típicos por origem:

- **Rios**: areia, material coloidal, sólidos em suspensão, compostos orgânicos, sais dissolvidos, bactérias e vírus.
- **Lagos**: sais dissolvidos, material coloidal, compostos orgânicos, algas, bactérias, vírus e gases dissolvidos.
- **Águas subterrâneas**: amônia, gás sulfídrico, metais dissolvidos, compostos orgânicos e sais dissolvidos.
- **Águas pluviais**: sólidos em suspensão, compostos orgânicos, sólidos dissolvidos, microrganismos, cor e turbidez.

A consequência prática é que o tratamento deve ser dimensionado para os **mecanismos dominantes de contaminação**: remoção de sólidos suspensos, controle microbiológico, redução de sais dissolvidos e, quando necessário, polimento final para potabilidade ou para usos técnicos sensíveis. *(Fonte: `petroles-004c2afadba7ea17c7dd7908:pNone:3247173.60-3247210.0`)*

Para instalações marítimas, um caso frequente é a utilização de **água do mar** como matéria-prima para dessalinização. Os textos citam explicitamente o uso de osmose reversa em **navios, submarinos e plataformas de petróleo** para produção de água potável a partir de água do mar. *(Fonte: `petroles-4ee4bce16acf674505c8912d:pNone:1727161.0-1727190.0`)*

## 3. Rotas de geração de água doce e potável

## 3.1 Processos térmicos e por membranas

As fontes separam a dessalinização em dois grupos principais:

- **Processos térmicos**, baseados em mudança de fase da água, como destilação convencional e outras variantes de evaporação/destilação.
- **Processos por membranas**, com destaque para **osmose reversa** e eletrodiálise.

Os processos térmicos são descritos como **energo-intensivos**. Já os processos por membranas são apresentados como tecnologicamente competitivos e amplamente aplicáveis, inclusive em instalações marítimas. *(Fonte: `petroles-4ee4bce16acf674505c8912d:pNone:1727055.0-1727091.0`)*

### Osmose reversa: princípio de operação
A osmose natural ocorre quando duas soluções de concentrações diferentes são separadas por membrana semipermeável, com fluxo de água do meio menos concentrado para o mais concentrado. Na **osmose reversa**, esse fluxo é invertido pela aplicação de pressão no lado mais concentrado, de modo que a água atravesse a membrana e os sais permaneçam majoritariamente no lado do concentrado. Em termos conceituais, a reversão requer pressão aplicada superior à pressão osmótica da solução. *(Fonte: `petroles-4ee4bce16acf674505c8912d:pNone:1727055.0-1727091.0`)*

### Recuperação e rejeição de sais
O material consultado referencia equações de desempenho da dessalinização com as seguintes variáveis:

- **Vp** = vazão de água potável produzida, m³/h
- **Va** = vazão de alimentação, m³/h
- **Cp** = concentração de sais na água dessalinizada, mg/L
- **Ca** = concentração de sais na água de alimentação, mg/L
- **E** = eficiência da membrana na eliminação de sais, %

Essas variáveis sustentam dois indicadores fundamentais:

1. **Recuperação de água potável**: fração do volume de alimentação convertida em produto.
2. **Eliminação de sais**: capacidade da membrana de reduzir a salinidade entre alimentação e permeado.

Na prática operacional, esses dois indicadores devem ser acompanhados em conjunto: alta recuperação pode elevar risco de incrustação e concentração no rejeito; alta rejeição de sais não elimina a necessidade de monitorar a estabilidade operacional e a qualidade do permeado. *(Fonte: `regis-3d703c296545505228102293:pNone:2759.0-2961.0`)*

### Arranjo das membranas
As fontes indicam que a eficiência global pode ser alterada pela organização das membranas **em paralelo e/ou em série**. Em termos de engenharia, isso permite ajustar capacidade, turndown operacional e desempenho de dessalinização, mas sempre com geração simultânea de duas correntes:

- **permeado** (água dessalinizada);
- **rejeito/concentrado/salmoura**.

Ou seja, um sistema de osmose reversa nunca produz apenas água útil; ele também produz uma corrente concentrada que precisa de destinação adequada. *(Fonte: `regis-3d703c296545505228102293:pNone:2759.0-2961.0`)*

## 3.2 Trem convencional de tratamento para água utilitária

Os trechos de refinaria mostram um encadeamento clássico de tratamento aplicável como referência conceitual para sistemas utilitários:

1. **Captação e armazenamento de água bruta**.
2. **Dosagem de cloro e coagulante** na água bruta.
3. **Clarificação**, com formação e decantação de flocos.
4. **Filtração em areia** para retenção dos sólidos remanescentes.
5. **Distribuição por qualidade**:
   - parte da água para sistemas de resfriamento e serviços;
   - parte para produção de água potável, com desinfecção adicional;
   - parte para unidades de ultrafiltração/osmose reversa ou troca iônica, quando se exige água desmineralizada.

No tratamento convencional, os coagulantes citados incluem **sulfato de alumínio** e **cloreto férrico**; para ajuste de alcalinidade, são mencionados **barrilha (Na2CO3)**, **hidróxido de cálcio** e **hidróxido de sódio**. Na desinfecção, aparecem **cloro gás, hipoclorito de sódio e ozônio**. *(Fontes: `petroles-004c2afadba7ea17c7dd7908:pNone:3247173.60-3247210.0`, `regis-195418cbcd17f97ab5f87ea2:pNone:4763.0-5120.0`)*

### Ultrafiltração/microfiltração como substituição parcial do trem convencional
As fontes indicam que clarificação e filtração vêm sendo substituídas, em alguns casos, por **membranas de ultra ou microfiltração**, com as seguintes vantagens:

- menor uso de produtos químicos;
- menor área ocupada;
- menor geração de sólidos/lodo;
- água com melhor qualidade em sólidos suspensos.

Desvantagens citadas:

- maior custo de implantação;
- vida útil de membranas tipicamente entre **3 e 5 anos** no caso relatado.

Para FPSO, esse trade-off é particularmente relevante: menor área e menor inventário químico podem ser vantajosos offshore, mas o custo e a estratégia de manutenção/troca de membranas tornam-se críticos. *(Fonte: `petroles-004c2afadba7ea17c7dd7908:pNone:3247173.60-3247210.0`)*

## 3.3 Produção de água desmineralizada e polimento

A segunda etapa do tratamento, quando se requer água com baixo teor de sais dissolvidos, pode empregar **troca iônica**, **osmose reversa** ou a combinação de ambas. *(Fonte: `petroles-004c2afadba7ea17c7dd7908:pNone:3247173.60-3247210.0`)*

### Troca iônica
A sequência descrita nas fontes é:

1. **descloração**;
2. **resina catiônica**: retém cátions e libera H+;
3. **resina aniônica**: retém ânions e libera OH-;
4. **leito misto**: polimento final, produzindo água "polida".

Quando a capacidade de troca das resinas se esgota, os vasos saem de operação para **regeneração**:

- resina catiônica: regeneração com **ácido sulfúrico (H2SO4)**;
- resina aniônica: regeneração com **soda cáustica (NaOH)**.

Em instalações que usam osmose reversa antes da troca iônica, a troca iônica pode atuar como polimento; em outras, pode coexistir com membranas em rotas paralelas ou alternativas. *(Fontes: `petroles-004c2afadba7ea17c7dd7908:pNone:3247173.60-3247210.0`, `regis-195418cbcd17f97ab5f87ea2:pNone:4763.0-5120.0`)*

### Proteção de resinas e membranas contra cloro
Os documentos afirmam que, para proteger resinas de troca iônica e membranas de osmose inversa, é necessária a **remoção do cloro remanescente**, usando:

- **filtros de carvão ativado**, ou
- **bissulfito de sódio (NaHSO3)**.

Além disso, embora a cloração no pré-tratamento possa ajudar a reduzir formação de biofilme, a fonte alerta que o **cloro pode degradar quimicamente e danificar membranas**, exigindo controle cuidadoso da dosagem e da descloração a jusante. *(Fontes: `petroles-004c2afadba7ea17c7dd7908:pNone:3247173.60-3247210.0`, `petroles-4ee4bce16acf674505c8912d:pNone:1727161.0-1727190.0`)*

## 4. Água potável, água de serviço e água técnica

Os documentos distinguem claramente o fato de que a água potável tem requisitos mais restritivos que a água de serviço. Um ponto relevante é que **parte da água filtrada sofre desinfecção adicional para uso como água potável**, enquanto outra parcela segue para usos industriais/utilitários. *(Fonte: `petroles-004c2afadba7ea17c7dd7908:pNone:3247173.60-3247210.0`)*

Do ponto de vista de projeto de utilidades, isso implica:

- produzir a qualidade mínima necessária para cada rede;
- reservar tratamento final específico para a linha potável;
- evitar que consumidores de serviço ou processo imponham exigências desnecessárias ao sistema potável.

Os textos também citam usos típicos de **água de serviço** em lavagens, deslocamentos, testes hidrostáticos e outras demandas auxiliares. Em refinaria, até a água originalmente destinada a incêndio pode acabar sendo consumida em usos não emergenciais, o que evidencia a importância de controlar a segregação de redes e de contabilizar esses usos no balanço hídrico. *(Fontes: `petroles-004c2afadba7ea17c7dd7908:pNone:398803.60-398833.0`, `petroles-004c2afadba7ea17c7dd7908:pNone:3247173.60-3247210.0`, `regis-195418cbcd17f97ab5f87ea2:pNone:4763.0-5120.0`)*

## 5. Armazenamento, autonomia e distribuição

Os exemplos de refinaria mostram o papel essencial dos **tanques de armazenamento** para:

- garantir suprimento em caso de falha de adução/captação;
- desacoplar a fonte bruta dos consumidores finais;
- manter reserva para combate a incêndio;
- estabilizar a operação dos clarificadores, filtros e unidades de dessalinização/polimento.

No caso citado, a água bruta é estocada em três tanques interligados, dos quais parte segue para clarificação e parte pode alimentar diretamente outros usos, inclusive incêndio. Após o tratamento, tanques intermediários segregam água clarificada e água filtrada para abastecer ultrafiltração/osmose reversa, troca iônica, processos, água potável e complemento de resfriamento. *(Fonte: `regis-195418cbcd17f97ab5f87ea2:pNone:4763.0-5120.0`)*

### Critérios práticos para o balanço de capacidade
Com base no material, o dimensionamento de capacidade deve considerar, no mínimo:

- demanda contínua de água potável;
- demanda de água de serviço/técnica;
- make-up de sistemas que perdem água;
- autonomia frente a indisponibilidade temporária da captação ou do tratamento;
- reserva para usos críticos e picos não rotineiros;
- reciclos internos de água recuperada.

O retorno de água recuperada do desaguamento de lodo ao início do tratamento é um exemplo de **recirculação interna** que reduz consumo bruto e pode melhorar a eficiência global, desde que a carga adicional de contaminantes seja compatível com a capacidade da etapa de clarificação. *(Fontes: `regis-195418cbcd17f97ab5f87ea2:pNone:4763.0-5120.0`, `petroles-004c2afadba7ea17c7dd7908:pNone:398803.60-398833.0`)*

## 6. Interface com sistemas de resfriamento e impacto na demanda de água doce

Mesmo quando o foco principal é água doce/potável, o balanço de utilidades deve incorporar os consumidores indiretos. A fonte de refinaria mostra que a água de resfriamento pode ser o **maior consumidor** de água da instalação, porque há perdas que exigem reposição contínua. Essas perdas são expressas por:

**R = E + D + A**

onde:

- **R** = água de reposição (make-up);
- **E** = evaporação;
- **D** = drenagem/blowdown para controle de concentração de sais;
- **A** = arraste de gotículas.

O trecho informa ainda, como valor aproximado de projeto/operação do caso citado, **A = 0,1% · Q**, sendo **Q** a vazão de circulação. *(Fonte: `regis-195418cbcd17f97ab5f87ea2:pNone:4763.0-5120.0`)*

### Relevância para águas utilitárias
Para um FPSO/FSO, isso significa que a planta de água doce não deve ser dimensionada apenas pelos consumidores “diretos” de potável e serviço. Se parte da água tratada for usada como make-up de resfriamento, as perdas por evaporação, arraste e blowdown podem dominar o consumo. Logo, problemas em torres/circuitos de resfriamento podem se manifestar como:

- aumento anormal do consumo de água doce;
- maior carga na unidade de dessalinização;
- maior geração de rejeito, lodo ou efluente de purga.

As fontes também lembram que, em circuitos fechados sem corrosão ou contaminação relevante, a água tende a retornar ao sistema, reduzindo perdas líquidas. *(Fontes: `regis-195418cbcd17f97ab5f87ea2:pNone:4763.0-5120.0`, `petroles-004c2afadba7ea17c7dd7908:pNone:398803.60-398833.0`)*

## 7. Controle operacional e monitoramento de desempenho

Com base nos mecanismos de tratamento descritos, o monitoramento mínimo deve cobrir:

### 7.1 Na água de alimentação
- turbidez e sólidos suspensos;
- salinidade / sólidos dissolvidos / condutividade;
- presença de microrganismos e matéria orgânica quando relevante;
- variações sazonais ou associadas à fonte de captação.

### 7.2 No pré-tratamento
- eficiência da coagulação/clarificação;
- qualidade do efluente de filtros ou de UF/MF;
- controle de dosagem de desinfetante e coagulante;
- cloro residual antes de membranas sensíveis ou troca iônica.

### 7.3 Na dessalinização/polimento
- vazões de alimentação, permeado e rejeito;
- recuperação de água produzida;
- qualidade do permeado em sais dissolvidos;
- desempenho de descloração;
- exaustão de resinas de troca iônica.

### 7.4 Na água potável/distribuição
- manutenção da qualidade da água após desinfecção final;
- integridade de tanques de armazenamento;
- estabilidade do suprimento frente a picos de consumo.

Os próprios documentos destacam que o desempenho do tratamento depende diretamente da **qualidade da água bruta**, que varia com a origem e pode comprometer processos a jusante se não for adequadamente controlada. *(Fontes: `petroles-004c2afadba7ea17c7dd7908:pNone:3247173.60-3247210.0`, `regis-3d703c296545505228102293:pNone:2759.0-2961.0`, `regis-195418cbcd17f97ab5f87ea2:pNone:4763.0-5120.0`)*

## 8. Integridade, manutenção e solução de problemas

### 8.1 Problemas típicos de pré-tratamento
- **Sobrecarga de sólidos suspensos, algas ou coloides**: reduz desempenho de clarificadores, filtros e membranas.
- **Dosagem inadequada de coagulante/alcalinizante**: piora formação de flocos e aumenta arraste de sólidos.
- **Geração elevada de lodo**: aumenta necessidade de desaguamento e disposição final.

### 8.2 Problemas típicos de membranas
- **Biofilme/fouling**: pode ser mitigado por controle microbiológico no pré-tratamento, mas com cuidado para não expor a membrana a cloro residual incompatível.
- **Ataque químico por cloro**: risco explicitamente citado nas fontes.
- **Queda de qualidade do permeado**: sugere perda de integridade, condições inadequadas de operação ou limitação do pré-tratamento.
- **Aumento do volume de rejeito ou queda de recuperação**: afeta balanço hídrico e capacidade líquida de produção de água doce.

### 8.3 Problemas típicos de troca iônica
- **Exaustão de resinas**: aumento de sais no produto e necessidade de regeneração.
- **Falha de descloração**: degradação da capacidade do sistema a jusante.

### 8.4 Problemas de armazenamento e distribuição
- **Consumos não previstos ou uso indevido de redes**: distorcem balanço de água e podem comprometer autonomia.
- **Contaminação em tanques/rede**: afeta especialmente a linha potável.
- **Perdas em consumidores auxiliares**: aumentam a taxa de reposição e mascaram problemas operacionais em outras utilidades.

*(Fontes: `petroles-004c2afadba7ea17c7dd7908:pNone:3247173.60-3247210.0`, `petroles-4ee4bce16acf674505c8912d:pNone:1727161.0-1727190.0`, `regis-195418cbcd17f97ab5f87ea2:pNone:4763.0-5120.0`)*

## 9. Destinação de rejeitos e resíduos do tratamento

As fontes destacam dois resíduos principais:

1. **Lodo** da clarificação/filtração, que pode ser espessado, desaguado e enviado para disposição final, com eventual retorno da fase líquida ao início do tratamento.
2. **Rejeito/concentrado** da osmose reversa, de alta salinidade, cuja destinação deve ser definida desde o projeto.

O concentrado da dessalinização tem relevância operacional porque pode ser gerado em volumes comparáveis à água dessalinizada, dependendo do arranjo e da recuperação adotada. A literatura citada comenta alternativas como descarte ao mar, descarte em corpos d’água, injeção profunda e usos integrados em sistemas produtivos; entretanto, a adequação depende fortemente do contexto local. Para instalações marítimas, a simples existência do mar não elimina a necessidade de avaliar compatibilidade ambiental e operacional da descarga. *(Fontes: `regis-3d703c296545505228102293:pNone:2759.0-2961.0`, `petroles-4ee4bce16acf674505c8912d:pNone:1727161.0-1727190.0`, `regis-195418cbcd17f97ab5f87ea2:pNone:4763.0-5120.0`)*

## 10. Síntese de critérios de decisão para projeto e operação

Com base nas fontes, a engenharia de águas utilitárias e potáveis deve verificar, pelo menos, os seguintes pontos:

1. **Qual a fonte de água e quais contaminantes dominam?**
   - define necessidade de clarificação, filtração, desinfecção e dessalinização.

2. **Quais consumidores exigem cada classe de qualidade?**
   - evita supertratamento e melhora eficiência global.

3. **O pré-tratamento protege adequadamente membranas e resinas?**
   - atenção a sólidos suspensos, microrganismos e cloro residual.

4. **A capacidade foi calculada sobre demanda líquida ou sobre demanda total incluindo perdas?**
   - considerar make-up, rejeitos, lodo, picos e autonomia.

5. **A filosofia de armazenamento desacopla falhas da fonte/tratamento dos consumidores críticos?**
   - tanques intermediários e segregação por qualidade ajudam a manter continuidade.

6. **A destinação de rejeitos está incorporada ao projeto?**
   - sem isso, a água produzida pode existir apenas no papel, mas não em operação sustentável.

7. **O sistema dispõe de indicadores claros de desempenho?**
   - vazões, recuperação, qualidade do permeado/produto, cloro residual e estabilidade de consumo.

*(Fontes: `petroles-004c2afadba7ea17c7dd7908:pNone:3247173.60-3247210.0`, `petroles-004c2afadba7ea17c7dd7908:pNone:398803.60-398833.0`, `petroles-4ee4bce16acf674505c8912d:pNone:1727055.0-1727091.0`, `petroles-4ee4bce16acf674505c8912d:pNone:1727161.0-1727190.0`, `regis-195418cbcd17f97ab5f87ea2:pNone:4763.0-5120.0`, `regis-3d703c296545505228102293:pNone:2759.0-2961.0`)*