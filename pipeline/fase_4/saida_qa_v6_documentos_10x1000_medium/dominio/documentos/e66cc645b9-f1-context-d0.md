# Identificação de perigos em estudos de segurança de FPSOs

## 1. Finalidade da identificação de perigos

A identificação de perigos é a etapa em que se pesquisam, de forma estruturada, os eventos que podem iniciar acidentes e os cenários acidentais que podem afetar pessoas, meio ambiente, patrimônio e integridade da instalação. Em termos práticos, ela busca:

- identificar **eventos iniciadores** e ameaças relevantes;
- levantar **causas**, incluindo falhas de equipamentos, falhas de instrumentação, desvios operacionais e **erros humanos**;
- descrever **consequências possíveis** e sua severidade qualitativa;
- consolidar **cenários acidentais** para estudo posterior;
- hierarquizar qualitativamente ou semiquantitativamente os riscos;
- propor **medidas preventivas e mitigadoras** e apontar onde análises mais detalhadas serão necessárias.

Essa etapa não se limita ao projeto conceitual. Os trechos consultados indicam aplicação desde fases iniciais de desenvolvimento até revisões de unidades em operação, além de uso em novos projetos, conversões e modificações. Em FPSOs, isso é particularmente relevante porque o conjunto de perigos inclui não apenas processo de produção, mas também sistemas navais/marítimos, utilidades, flare/vent, offloading e interfaces operacionais.

**Fontes da seção:** `regis-6ce306d1aa9065c0dae3e980:pNone:1742.0-2037.0`, `regis-a895130239a6e9ec62837349:pNone:6385.0-6572.0`, `regis-962e222ee3c37dec82110fd6:pNone:1187.0-1445.0`, `anp-dabfb60617e4f0ede433578e:p69-72:23.0-19.0`

## 2. Conceitos centrais para formulação dos cenários

Para a elaboração consistente de estudos de segurança, convém distinguir:

- **Perigo (hazard):** característica de uma atividade, condição de processo ou substância com potencial de causar dano.
- **Incidente:** evento não planejado que gerou ou poderia gerar acidente.
- **Acidente:** evento não planejado, ou sequência de eventos, com consequências indesejáveis.
- **Risco:** combinação entre a chance de ocorrência e a magnitude das perdas/danos.
- **Salvaguarda / barreira:** medida, função, equipamento, ação humana ou arranjo organizacional destinada a prevenir, controlar ou mitigar um evento indesejado.
- **Cenário acidental:** encadeamento coerente entre um evento iniciador, suas causas, falhas/sucessos de barreiras e consequências finais.

Na prática de FPSO, o perigo não é apenas a presença do hidrocarboneto, mas também a combinação entre inventário, pressão, temperatura, confinamento, ignição, arranjo físico, segregação de áreas e condições operacionais. Por isso, a qualidade da identificação depende de boa definição de limites do sistema e de compreensão das interfaces entre módulos e atividades.

**Fontes da seção:** `regis-19e018d6d806ef2ee68d7882:pNone:2169.0-2397.0`, `regis-a895130239a6e9ec62837349:pNone:6385.0-6572.0`, `regis-962e222ee3c37dec82110fd6:pNone:3831.0-4085.0`

## 3. Processo estruturado de identificação de perigos e cenários acidentais

Os materiais apontam um fluxo técnico recorrente para essa etapa:

1. **Caracterizar o sistema**
   - descrever subsistemas principais, suas funções e o desempenho esperado;
   - entender interações entre subsistemas;
   - registrar procedimentos normais e de emergência;
   - identificar alarmes, intertravamentos e sistemas de segurança;
   - definir fronteiras do sistema e módulos de análise.

2. **Levantar a base documental**
   - fluxogramas de processo;
   - diagramas de tubulação e instrumentação;
   - descrição de sistemas de proteção e segurança;
   - informações sobre fluidos, condições operacionais e inventários perigosos.

3. **Identificar perigos e eventos iniciadores**
   - vazamentos e perda de contenção;
   - incêndio, explosão, colisão, alagamento e outros eventos relevantes ao sistema analisado;
   - desvios de parâmetros de processo;
   - falhas funcionais de equipamentos e subsistemas;
   - falhas humanas e inconsistências procedimentais.

4. **Relacionar causas e consequências**
   - causas imediatas e possíveis causas-raiz;
   - efeitos físicos esperados, por exemplo incêndio em poça, queimaduras, explosão, BLEVE, intoxicação ou danos à integridade da instalação;
   - barreiras de detecção, prevenção e mitigação já existentes.

5. **Consolidar e priorizar cenários**
   - agrupar eventos em cenários significativos;
   - descartar apenas os cenários claramente menos relevantes para o problema estudado;
   - selecionar hipóteses acidentais que seguirão para análises posteriores mais detalhadas.

6. **Produzir recomendações rastreáveis**
   - medidas para reduzir frequência e/ou severidade;
   - necessidades de revisão de projeto, instrumentação, procedimentos, treinamento, manutenção ou barreiras adicionais.

Um ponto importante é o uso de **análise histórica de acidentes e incidentes**. Mesmo quando não tratada como obrigação formal no trecho consultado, ela é útil para orientar a seleção de cenários relevantes e evitar que o estudo se restrinja apenas a hipóteses idealizadas.

**Fontes da seção:** `regis-a895130239a6e9ec62837349:pNone:6385.0-6572.0`, `regis-6ce306d1aa9065c0dae3e980:pNone:1742.0-2037.0`, `regis-ecacf0f324e4abda266a20de:pNone:3132.0-3364.0`

## 4. Critérios para selecionar a técnica de identificação de perigos

A escolha da técnica não é fixa; depende principalmente de:

- **fase do projeto ou da vida útil da instalação**;
- **nível de detalhamento desejado**;
- **tempo e recursos disponíveis**;
- **tipo de problema predominante**: processo, operabilidade, falha funcional, manutenção, revisão geral, interface operacional ou análise de barreiras.

De forma resumida:

- **HAZID / APR / APP / PHA**: úteis para visão ampla e identificação inicial de cenários.
- **HAZOP**: mais apropriado quando há maior detalhamento do processo e interesse nos desvios de parâmetros e operabilidade.
- **What-if / checklist**: úteis para triagem, revisão estruturada e complementação de outras técnicas.
- **FMEA**: mais forte quando a análise quer entender modos de falha de equipamentos, componentes ou subsistemas e seus efeitos.
- **Bow-Tie**: muito útil para consolidar, comunicar e gerir cenários já identificados, deixando explícitas ameaças, evento topo, consequências e barreiras.

Os trechos também sugerem que a decisão entre **PHA/APP** e **FMEA** pode depender do objeto principal: processo e cenários de perigo, no primeiro caso; vulnerabilidades funcionais, manutenção e sintomas de falha, no segundo.

**Fontes da seção:** `regis-2bc1d7ed973c40eb10c4dfe8:pNone:56.0-106.0`, `regis-a895130239a6e9ec62837349:pNone:6385.0-6572.0`, `regis-19e018d6d806ef2ee68d7882:pNone:2169.0-2397.0`

## 5. Técnicas qualitativas e semiquantitativas relevantes

### 5.1 HAZID / APR / APP / PHA

Nos trechos fornecidos, HAZID aparece como técnica qualitativa voltada à identificação de perigos, suas consequências, classificação de riscos e indicação de medidas de controle. Já APR/APP/PHA é descrita como técnica qualitativa amplamente usada para identificar acidentes potenciais, inclusive em fases iniciais de projeto ou como revisão de instalações em operação.

Características práticas da APR/APP:

- subdivisão da instalação em módulos ou subsistemas;
- definição de fronteiras do sistema;
- levantamento dos produtos perigosos e condições de processo/estocagem;
- preenchimento de planilhas em reuniões de equipe multidisciplinar;
- identificação de perigos, causas, efeitos, detecção/salvaguardas e recomendações.

Um modelo de planilha apresentado nos trechos inclui, tipicamente:

- unidade / sistema / trecho / referências / data / revisão;
- perigos identificados;
- causas prováveis;
- efeitos possíveis;
- modos de detecção e salvaguardas;
- categoria de frequência;
- categoria de severidade;
- categoria de risco;
- recomendações / observações;
- identificação do cenário.

Em FPSOs, essa abordagem é útil para construir a visão inicial dos cenários envolvendo topsides, sistemas marítimos, utilidades, flare/vent, tanques, offloading e interfaces operacionais. Também é útil para decidir quais cenários exigirão aprofundamento em HAZOP, QRA, FEA/FERA, dispersão de gás, EERA/ETRERA ou ESSA.

**Fontes da seção:** `regis-962e222ee3c37dec82110fd6:pNone:1187.0-1445.0`, `regis-6ce306d1aa9065c0dae3e980:pNone:1742.0-2037.0`, `regis-6ce306d1aa9065c0dae3e980:pNone:1846.0-2191.0`, `regis-19e018d6d806ef2ee68d7882:pNone:2169.0-2397.0`

### 5.2 HAZOP

O HAZOP busca identificar **perigos e problemas de operabilidade** por meio da análise de **desvios** dos parâmetros de processo. O princípio é comparar a intenção de projeto/operação com desvios plausíveis e examinar:

- parâmetro;
- palavra-guia;
- desvio;
- causas;
- consequências;
- detecção;
- recomendações.

Os trechos indicam que o HAZOP é especialmente valioso quando os documentos de engenharia já estão disponíveis, pois permite examinar os nós de processo com maior rigor e ainda propor mudanças antes de impactos maiores de implantação. Ao mesmo tempo, ele também pode ser empregado em revisões de segurança durante a operação.

Aplicações úteis para FPSO:

- sistemas de processo dos topsides;
- utilidades críticas;
- sistemas marítimos/ship systems;
- operações com forte dependência de parâmetros como pressão, vazão, temperatura e nível;
- avaliação de inconsistências em procedimentos operacionais e potenciais fontes de erro humano.

Um dos trechos mostra um **HAZOP adaptado** para construção de poços, no qual os nós são fases operacionais e foi acrescentada coluna de criticidade. Embora esse exemplo não seja de FPSO, ele ilustra um princípio válido: em operações dinâmicas e sequenciais, pode ser necessário adaptar o recorte dos nós e o modo de priorização.

**Fontes da seção:** `regis-6ce306d1aa9065c0dae3e980:pNone:1846.0-2191.0`, `regis-2bc1d7ed973c40eb10c4dfe8:pNone:56.0-106.0`, `anp-dabfb60617e4f0ede433578e:p69-72:23.0-19.0`

### 5.3 What-if, checklist e brainstorming

Essas técnicas são mais simples, porém úteis quando bem aplicadas:

- **What-if**: explora perguntas do tipo “e se...?”, ajudando a revelar desvios operacionais, falhas de interface e cenários não imediatamente visíveis.
- **Checklist**: usa listas estruturadas de perguntas para revisar fontes de risco e áreas críticas; funciona bem como apoio à concepção, pré-operação e auditorias/revisões.
- **Brainstorming**: favorece a geração multidisciplinar de hipóteses e costuma ser um mecanismo de apoio à identificação inicial de perigos.

Checklist e What-if tendem a ser mais eficazes quando usados como **complemento** a análises mais robustas, e não como substitutos automáticos de HAZOP ou FMEA em sistemas complexos.

**Fontes da seção:** `regis-2bc1d7ed973c40eb10c4dfe8:pNone:56.0-106.0`, `regis-19e018d6d806ef2ee68d7882:pNone:2169.0-2397.0`, `regis-ecacf0f324e4abda266a20de:pNone:3132.0-3364.0`, `regis-962e222ee3c37dec82110fd6:pNone:3831.0-4085.0`

### 5.4 FMEA

A FMEA é uma técnica indutiva voltada a identificar:

- modos de falha;
- efeitos de cada falha;
- sintomas ou manifestações da falha;
- ações de melhoria para elevar a confiabilidade do sistema.

Ela é particularmente útil quando o foco da análise está em:

- equipamentos e componentes;
- subsistemas de segurança e suporte;
- manutenção e vulnerabilidades funcionais;
- identificação de falhas simples ou relativamente bem definidas.

Os trechos indicam que a FMEA pode ser usada de forma qualitativa e, em alguns casos, quantitativa, especialmente para estimar confiabilidade ou probabilidade de falha. Quando a lógica causal se torna muito complexa, a FMEA tende a precisar de complemento por técnicas dedutivas como árvore de falhas.

Em FPSOs, a FMEA é especialmente útil para instrumentação, utilidades críticas, sistemas de emergência, funções de segurança e equipamentos cuja falha individual possa degradar barreiras ou disparar cenários de perda de contenção.

**Fontes da seção:** `regis-19e018d6d806ef2ee68d7882:pNone:2169.0-2397.0`, `regis-a895130239a6e9ec62837349:pNone:6385.0-6572.0`, `regis-2bc1d7ed973c40eb10c4dfe8:pNone:56.0-106.0`

### 5.5 Bow-Tie para consolidação de cenários e barreiras

O Bow-Tie é descrito como ferramenta gráfica baseada na relação causa-efeito, construída a partir da combinação conceitual de árvore de falhas com árvore de eventos. Seu valor para a identificação de perigos está em organizar um cenário em torno de:

- **ameaças** ou causas que podem levar ao evento principal/topo;
- **evento topo**;
- **barreiras preventivas**, posicionadas antes do evento topo;
- **barreiras mitigadoras**, posicionadas após o evento topo;
- **consequências** finais.

Os trechos consultados destacam que essa forma de representação ajuda a visualizar claramente:

- quais combinações de ameaças levam ao evento topo;
- onde cada barreira atua;
- como falhas ou degradação de barreiras podem permitir escalada do cenário;
- quais elementos devem ser monitorados como críticos para a segurança operacional.

Como instrumento profissional, o Bow-Tie é especialmente útil para transformar o inventário de cenários do HAZID/APR/HAZOP em um modelo gerenciável de barreiras preventivas e mitigadoras, além de apoiar comunicação com operação, manutenção, inspeção e resposta à emergência.

**Fontes da seção:** `petroles-004c2afadba7ea17c7dd7908:pNone:466560.0-466586.0`, `regis-962e222ee3c37dec82110fd6:pNone:3831.0-4085.0`

## 6. Priorização semiquantitativa dos cenários

Após identificar os cenários, é necessário priorizá-los. Os trechos fornecem três formas principais de priorização semiquantitativa.

### 6.1 Matriz frequência x severidade

Na APR/APP, os cenários podem ser classificados por categorias qualitativas de frequência e severidade. Um exemplo citado usa:

**Frequência:**
- A: extremamente remota;
- B: remota;
- C: pouco provável;
- D: provável;
- E: frequente.

**Severidade:**
- I: desprezível;
- II: marginal;
- III: crítica;
- IV: catastrófica.

O cruzamento gera uma categoria de risco, por exemplo:
- **Tolerável (T)**;
- **Moderado (M)**;
- **Não tolerável (NT)**.

Interpretação prática:
- risco tolerável: manter controles e monitoramento;
- risco moderado: avaliar controles adicionais e implementar os praticáveis;
- risco não tolerável: controles existentes são insuficientes e alternativas devem ser consideradas para reduzir frequência e/ou consequência.

### 6.2 Índice de criticidade no HAZOP/FMEA

Um dos trechos descreve a criação de **índices de criticidade** para selecionar quais desvios ou falhas merecem aprofundamento por diagramas de sequência de eventos e/ou árvores de falhas. Isso é útil quando o estudo gera muitos desvios e a equipe precisa concentrar esforço nos mais críticos.

### 6.3 Número de priorização de risco (RPN)

Na FMEA, aparece o **Risk Priority Number**:

**RPN = O × G × D**

onde:
- **O** = ocorrência;
- **G** = gravidade dos efeitos;
- **D** = detectabilidade.

O RPN ajuda a comparar modos de falha, mas não substitui julgamento técnico. Um cenário com RPN moderado pode ser inaceitável se tiver potencial catastrófico ou afetar barreiras críticas.

**Fontes da seção:** `regis-6ce306d1aa9065c0dae3e980:pNone:1846.0-2191.0`, `regis-2bc1d7ed973c40eb10c4dfe8:pNone:56.0-106.0`

## 7. Da identificação do perigo à modelagem da sequência acidental

A identificação de perigos não encerra o estudo; ela alimenta a modelagem da progressão do acidente. Os trechos descrevem a etapa seguinte como a construção da **sequência acidental**, isto é, a cadeia que parte do evento iniciador e evolui por sucessos/falhas de sistemas e barreiras até estados finais.

Ferramentas citadas nesse encadeamento:

- **diagramas sequenciais de eventos**;
- **árvores de eventos**;
- **árvores de falhas**;
- **análise causa-consequência**;
- **Bow-Tie**.

A utilidade dessa interface é dupla:

1. entender quais eventos e falhas realmente controlam a progressão do acidente;
2. selecionar os cenários que seguirão para estudos mais aprofundados de frequência, consequências e critérios de aceitabilidade.

Para FPSOs, isso é particularmente importante porque um mesmo evento iniciador pode evoluir de formas distintas conforme haja ou não isolamento, detecção, ignição, confinamento, resposta de emergência e disponibilidade de sistemas críticos.

**Fontes da seção:** `regis-a895130239a6e9ec62837349:pNone:6385.0-6572.0`, `regis-ecacf0f324e4abda266a20de:pNone:3132.0-3364.0`, `petroles-004c2afadba7ea17c7dd7908:pNone:466560.0-466586.0`

## 8. Interface com Safety Case e demais estudos de segurança

O relatório da ANP sobre o FPSO Cidade de São Mateus mostra, como exemplo de uma instalação específica, um conjunto de estudos que alimentaram o Safety Case, incluindo:

- Layout Review;
- HAZID;
- HAZOP de sistemas marítimos;
- HAZOP de processo topside;
- QRA;
- estudos de dispersão;
- análises de incêndio e explosão;
- ETRERA/EERA;
- Fire Propagation and Structural Protection Analysis;
- ESSA.

O ponto técnico relevante para esta faceta é que a **identificação de perigos** funciona como base integradora: sem ela, a seleção de cenários para estudos de fogo, explosão, dispersão, refúgio temporário, evacuação, sobrevivência de sistemas de emergência e risco quantificado perde consistência.

Os trechos indicam ainda que o Safety Case, em sentido amplo, pretende demonstrar que:

- os perigos foram identificados;
- os riscos foram avaliados;
- medidas de controle foram adotadas;
- o risco foi reduzido para níveis do tipo **ALARP**, quando esse critério for adotado pela organização ou pelo marco regulatório aplicável.

**Fontes da seção:** `anp-dabfb60617e4f0ede433578e:p69-72:23.0-19.0`, `regis-2bc1d7ed973c40eb10c4dfe8:pNone:56.0-106.0`

## 9. Boas práticas para aplicação em FPSO

Com base no material disponível, algumas boas práticas para estudos de identificação de perigos em FPSOs são:

- estruturar a análise por **módulos, subsistemas e interfaces**;
- cobrir tanto **processo topside** quanto **sistemas marítimos/navais** e operações associadas;
- usar equipe multidisciplinar e documentação atualizada;
- registrar explicitamente **causas, consequências, detecção, salvaguardas e recomendações**;
- não limitar a análise a falhas técnicas: incluir **erros humanos** e inconsistências procedimentais;
- utilizar técnicas complementares, em vez de presumir que uma única técnica cobre todo o problema;
- priorizar cenários de maior severidade e aqueles que degradam barreiras críticas;
- manter rastreabilidade entre cenário identificado, recomendação gerada e estudo posterior que dele depende.

Exemplos de perguntas profissionais coerentes com essa prática incluem:
- qual técnica é mais adequada para triagem inicial de cenários de um novo módulo de processo;
- quando um desvio de HAZOP deve ser aprofundado por análise causal mais detalhada;
- como registrar frequência, severidade e risco em planilha APR;
- como diferenciar uma ameaça, um evento topo e uma barreira no Bow-Tie.

**Fontes da seção:** `regis-6ce306d1aa9065c0dae3e980:pNone:1742.0-2037.0`, `regis-6ce306d1aa9065c0dae3e980:pNone:1846.0-2191.0`, `regis-2bc1d7ed973c40eb10c4dfe8:pNone:56.0-106.0`, `anp-dabfb60617e4f0ede433578e:p69-72:23.0-19.0`