# ECSO e integridade mecânica no SGSO de FPSOs

Este documento consolida, para fins de estudo e avaliação profissional, os principais requisitos e critérios técnicos relacionados à **avaliação do desempenho e da disponibilidade dos Elementos Críticos de Segurança Operacional (ECSO)** e à **integridade mecânica**, com ênfase no **tratamento de degradação, falha e indisponibilidade** em unidades do tipo FPSO. O texto combina requisitos do **SGSO da ANP para instalações marítimas** com conceitos e critérios técnicos complementares extraídos de notas técnicas e, de forma explicitamente limitada, de regulamento de integridade estrutural aplicável a instalações terrestres, usado aqui apenas como apoio conceitual e checklist técnico.

## 1. Conceitos fundamentais para avaliação de ECSO e integridade mecânica

No SGSO, os **Elementos Críticos de Segurança Operacional** são aqueles **essenciais para a prevenção ou mitigação** de acidentes operacionais, ou que, **em caso de falha**, possam provocar um acidente. Eles são classificados em três categorias:

- **Equipamentos Críticos de Segurança Operacional**;
- **Sistemas Críticos de Segurança Operacional**; e
- **Procedimentos Críticos de Segurança Operacional**.

Assim, a avaliação de um ECSO não se limita ao estado físico do hardware. Ela também deve considerar:

- a **função de segurança esperada**;
- as **características essenciais** definidas pelo operador;
- o **desempenho requerido em projeto**;
- a **confiabilidade presumida nas análises de risco**; e
- a **capacidade real de responder quando demandado**.

Como apoio conceitual, o RTSGI define **Adequação ao Uso** como a condição em que uma instalação ou equipamento é projetado, mantido, inspecionado, testado e operado de forma apropriada para o uso requerido, incluindo **desempenho, disponibilidade e efetividade**. Também define **Avaliação de Integridade** como um processo sistemático baseado em inspeção, avaliação de indicações, exame físico por técnicas apropriadas, caracterização de defeitos e verificação da integridade por análise estrutural. Embora esse texto regulatório seja voltado a instalações terrestres, os conceitos são tecnicamente úteis para interpretar a integridade mecânica de equipamentos e sistemas em FPSOs.

Outro conceito importante é o de **barreira**: mecanismo físico ou procedimento administrativo projetado para impedir ou mitigar acidentes. Quando uma barreira atende aos critérios do operador para ser considerada crítica, ela se relaciona diretamente com os ECSO. Nessa ótica, **disponibilidade** significa mais do que “estar instalado”: o elemento deve estar fisicamente presente, alinhado às normas pertinentes, com desempenho e confiabilidade compatíveis com o projeto e com as premissas das análises de risco.

**Fontes:** `anp-eec7f988e9eeea4ece5e1b8d:p22-25:52.0-40.0`, `anp-3971dc6c88f4e2d408134aab:p2-3:6.0-47.0`, `anp-912dd4dd5be0ece1d8e4973b:p6-9:0.0-10.0`

## 2. Disponibilidade, desempenho e estados de degradação dos ECSO

A Nota Técnica ANP sobre diagnóstico de barreiras distingue estados que são muito úteis para avaliação prática de ECSO:

### 2.1 Barreira/ECSO disponível
É o elemento:

- projetado ou elaborado conforme normas pertinentes;
- disponível fisicamente;
- com desempenho previsto em projeto; e
- capaz de desempenhar sua função de segurança quando solicitado.

A nota ressalta que o desempenho previsto inclui também a **confiabilidade**. Para mecanismos físicos, essa confiabilidade depende de **inspeção, testes e manutenção preventiva (ITMP)**. Para procedimentos, depende do gerenciamento dos fatores que influenciam o desempenho humano, como treinamento, fadiga, efetivo mínimo e sobrecarga da força de trabalho.

### 2.2 Barreira/ECSO degradado
O elemento está **com função de segurança comprometida**, mas não necessariamente totalmente perdida. Exemplos de causas citadas pela ANP:

- falha mecânica parcial;
- falha parcial em teste de performance;
- ausência de testes de performance;
- desvio de desempenho em relação ao projeto.

Um ponto importante da nota é que **um elemento ainda capaz de atuar pode continuar degradado** se não atender aos parâmetros previstos em projeto. Ou seja, “funcionar de algum modo” não basta para classificá-lo como disponível.

### 2.3 Barreira/ECSO indisponível
O elemento está **incapaz de exercer sua função de segurança**, por exemplo por:

- falha mecânica total;
- falha total em teste de performance; ou
- falha de projeto que inviabilize sua função.

### 2.4 Situações contingenciadas
Tanto barreiras degradadas quanto indisponíveis podem estar **contingenciadas**, desde que existam medidas temporárias formalmente estabelecidas e implementadas, capazes de reduzir os riscos a níveis aceitáveis.

Sem contingência adequada:

- **barreira degradada** permanece condição insegura; e
- **barreira indisponível**, quando crítica, **impede a continuidade operacional**.

### 2.5 Relação com PFD e intervalo de testes
A nota técnica explicita que, sob a ótica da engenharia de confiabilidade, o teste funcional identifica falhas ocultas e reduz a **PFD (probabilidade de falha na demanda)** para próximo da condição de projeto. Em contrapartida, quando o **intervalo de teste de funcionalidade é ultrapassado**, a PFD aumenta em relação ao valor assumido em projeto; por isso, o elemento não deve ser considerado disponível apenas por estar instalado.

O material fornecido não apresenta fórmula para cálculo da PFD; o ponto técnico relevante é a **relação qualitativa** entre atraso de testes, aumento da probabilidade de falha sob demanda e perda de disponibilidade.

**Fontes:** `anp-3971dc6c88f4e2d408134aab:p2-3:6.0-47.0`

## 3. Requisitos do SGSO para identificar, controlar e tratar ECSO degradados ou fora de operação

O SGSO exige que o operador:

1. **identifique os ECSO** da instalação;
2. **descreva suas características essenciais e funções**;
3. estabeleça **sistemas de gerenciamento e controle** desses elementos; e
4. mantenha procedimentos específicos para cenários de **degradação, falha ou indisponibilidade**.

Quando equipamentos ou sistemas críticos estiverem **em condições degradadas ou fora de operação**, o operador deve estabelecer:

- **procedimentos de contingência**;
- um **sistema de aprovação e controle** desses procedimentos; e
- **medidas temporárias** capazes de suprir a ausência ou degradação do ECSO, incluindo, quando aplicável:
  - implantação de **controles alternativos equivalentes**;
  - **redução e limitação da produção**; e
  - **isolamento e parada** de equipamentos, sistemas ou instalações.

Além disso, o SGSO determina que o operador **defina o prazo** durante o qual os procedimentos temporários poderão ser aceitos, até a implementação das medidas corretivas definitivas. Logo, a contingência não é uma solução aberta ou permanente; ela deve ter:

- justificativa técnica;
- aprovação formal;
- prazo de validade;
- monitoramento; e
- vínculo claro com a correção definitiva.

Na prática, essa lógica evita que degradações crônicas sejam “normalizadas” pela operação.

**Fontes:** `anp-eec7f988e9eeea4ece5e1b8d:p22-25:52.0-40.0`, `anp-3971dc6c88f4e2d408134aab:p2-3:6.0-47.0`

## 4. Integridade mecânica no SGSO: planejamento, controle e rastreabilidade

A prática de gestão de **Integridade Mecânica** do SGSO estabelece que a instalação, seus sistemas, estruturas e equipamentos devem passar por **inspeções, testes e manutenções necessários, de forma planejada e controlada**, buscando a integridade mecânica e a adequação ao uso.

### 4.1 Planejamento mínimo esperado
O operador deve estabelecer:

- **planos e procedimentos** para inspeção, teste e manutenção;
- alinhamento desses documentos com:
  - recomendações de fabricantes;
  - normas e padrões aplicáveis; e
  - boas práticas de engenharia;
- procedimentos com **instruções claras** para condução segura das atividades.

### 4.2 Controle da execução
O operador deve:

- **documentar todas as atividades** de integridade mecânica desenvolvidas a bordo;
- assegurar que procedimentos, manuais e demais documentos relevantes estejam **acessíveis ao pessoal de manutenção**, próprio ou contratado;
- estabelecer **requisitos de garantia da qualidade** na execução; e
- garantir que **todos os Equipamentos e Sistemas Críticos de Segurança Operacional** estejam cobertos pelos planos de inspeção, teste e manutenção.

### 4.3 Desvios de projeto e mudança
Qualquer **desvio das especificações de projeto** deve ser tratado pelo processo de **Gerenciamento de Mudanças (MOC)**. Isso é decisivo para integridade mecânica porque uma alteração não rastreada pode invalidar:

- pressupostos de projeto;
- critérios de inspeção e teste;
- premissas das análises de risco; e
- a própria classificação de disponibilidade do ECSO.

### 4.4 Monitoramento de resultados
O operador é responsável por **monitorar e avaliar os resultados** de inspeções e testes. Portanto, não basta executar atividades; é necessário verificar se os resultados confirmam, ou não, a permanência da integridade e do desempenho requerido.

**Fontes:** `anp-eec7f988e9eeea4ece5e1b8d:p22-25:52.0-40.0`

## 5. O que caracteriza uma avaliação robusta de integridade mecânica

Tomando como base as orientações técnicas disponibilizadas pela ANP, uma avaliação robusta de integridade mecânica deve contemplar pelo menos os seguintes pontos.

### 5.1 Cobertura integral do escopo
Todos os **sistemas de tubulações, equipamentos e ECSO relevantes** devem estar cobertos pelos planos de inspeção. A ausência de cobertura de parte do sistema compromete a visão de risco e pode mascarar perda de contenção primária ou falhas latentes.

### 5.2 Inspeções no prazo e gestão das recomendações
É esperado que:

- as inspeções sejam realizadas **em dia** com os planos estabelecidos;
- as recomendações resultantes sejam **classificadas com base em risco**;
- essas recomendações sejam implementadas **dentro do prazo inicialmente estabelecido**.

A revalidação de recomendações vencidas deve ser **excepcional** e, conforme a orientação técnica da ANP, deve ocorrer antes do vencimento original, mediante nova avaliação ou nova inspeção que sustente a prorrogação.

### 5.3 Critérios de aceitação de testes
Os testes de equipamentos e sistemas devem ter:

- **critérios de aceitação bem estabelecidos**;
- aderência a boas práticas de engenharia, manuais de fabricantes e normas reconhecidas;
- relatórios **conclusivos** sobre a condição do elemento testado.

Se o relatório não permite concluir se o elemento atendeu ou não aos requisitos, o teste é inadequado como evidência de disponibilidade.

### 5.4 Tratamento do desvio identificado em teste ou inspeção
Quando houver desvio ou não atendimento aos requisitos:

- deve ser emitida **ordem de manutenção corretiva**;
- a priorização deve considerar a **gravidade do desvio** e a **criticidade do elemento**;
- se o elemento for ECSO, deve ser implementada a **contingência**, nos termos da PG 11 do SGSO.

### 5.5 Rastreabilidade e responsabilidade técnica
A ANP destaca que testes, manutenções e inspeções devem ter **responsável técnico identificado**, além de assinaturas pertinentes, inclusive de revisão/aprovação conforme o sistema de gestão do operador. Isso reforça a necessidade de:

- rastreabilidade documental;
- responsabilização técnica; e
- capacidade de auditoria e reconstituição da decisão.

**Fontes:** `anp-21b016bb482410ebc1a9261e:p10:3.0-174.0`, `anp-eec7f988e9eeea4ece5e1b8d:p22-25:52.0-40.0`

## 6. Contenção primária e reparos temporários: ponto crítico da integridade mecânica

A ANP enfatiza a **garantia da contenção primária dos fluidos** como aspecto central da integridade mecânica. Se a contenção primária não é garantida, aumenta significativamente a probabilidade de:

- incêndios;
- explosões; e
- perda grave de segurança operacional.

Por isso, desvios de integridade em tubulações e equipamentos costumam ter alto potencial de risco e podem ser classificados como **graves ou críticos**.

### 6.1 Requisitos técnicos para reparos temporários
Reparos temporários em tubulações e equipamentos devem seguir as **melhores práticas de engenharia**, com:

- **memorial de cálculo**;
- execução conforme norma reconhecida, como **ASME PCC-2** e **ISO 24817**; e
- garantia de aderência às condições de serviço.

Sem essa base técnica, a ANP entende que **não é possível garantir a contenção primária**.

### 6.2 Equivalência da resistência sob fogo
Para haver equivalência entre o reparo e a condição original do item reparado, o operador deve assegurar que o reparo resista às **mesmas condições térmicas e de incêndio** a que o componente original resistiria, incluindo referência a **incêndio em poça** ou **incêndio em jato**, quando aplicável. A orientação técnica destaca a relevância dessa prática para:

- tubulações e equipamentos com **fluido perigoso**; e
- componentes da **rede de combate a incêndio**.

Esse critério é particularmente relevante em FPSOs, em que a perda de contenção pode se propagar rapidamente para cenários de incêndio/explosão.

### 6.3 Gestão de sobressalentes
A gestão de sobressalentes deve considerar, minimamente:

- obsolescência;
- taxa de falha;
- criticidade da falha;
- tempo de compra/reposição; e
- possibilidade de contingenciamento.

Uma gestão adequada de sobressalentes reduz a permanência de ECSO degradados ou contingenciados por períodos excessivos.

**Fontes:** `anp-21b016bb482410ebc1a9261e:p10:3.0-174.0`

## 7. Relação entre integridade mecânica, análise de riscos e gerenciamento de mudanças

O SGSO exige que a metodologia de identificação e análise de riscos:

- considere os **ECSO**;
- considere outras análises de risco e o **histórico de incidentes**;
- considere **layout, fatores humanos e causas externas**, quando aplicável;
- classifique os riscos identificados; e
- identifique ações para **mitigação e prevenção**.

Além disso:

- as análises devem ser conduzidas por **equipe multidisciplinar**;
- aprovadas pelo responsável da instalação ou designado; e
- documentadas em relatório com escopo, metodologia, riscos, classificação, recomendações e conclusões.

Quanto aos resultados:

- o operador é responsável por **implementar as ações corretivas** derivadas das análises de risco;
- deve **documentar** essa implementação;
- e, quando aplicável, deve indicar a necessidade de **revisão da lista de ECSO**.

Isso é decisivo para tratamento de degradação: quando uma falha recorrente, uma mudança de processo, uma alteração física ou uma nova vulnerabilidade passa a influenciar a prevenção/mitigação de acidentes, pode ser necessário:

1. rever a classificação do elemento como crítico;
2. revisar as premissas de desempenho e disponibilidade; e
3. adequar planos de inspeção, teste, manutenção e contingência.

Na mesma linha, qualquer desvio das especificações de projeto ou mudança física/operacional relevante deve ser tratado por **Gerenciamento de Mudanças**, justamente para evitar que a instalação opere com premissas de risco desatualizadas.

**Fontes:** `anp-eec7f988e9eeea4ece5e1b8d:p22-25:52.0-40.0`, `anp-b2cfa8a9492ef598716e9685:p52-54:15.0-0.0`

## 8. Conteúdo técnico útil para inspeções e avaliação de adequação ao uso

Como apoio conceitual adicional, o RTSGI terrestre explicita conteúdo mínimo de procedimentos de inspeção que pode ser aproveitado como referência técnica em programas de integridade mecânica. Para equipamentos estáticos e tubulações, a inspeção pode abranger:

- inspeções iniciais, periódicas e extraordinárias;
- análise do prontuário e da documentação;
- histórico de inspeção e de manutenção;
- registros operacionais e de segurança;
- exame visual;
- medição de espessura;
- outros ensaios, quando necessários;
- avaliação de vida remanescente;
- avaliação de corrosão e outros mecanismos de dano;
- mapeamento de pontos de medição e descontinuidades;
- determinação da **PMTA atual**, quando aplicável;
- verificação da instrumentação;
- acompanhamento de teste hidrostático, quando aplicável;
- assessoria técnica em alteração e reparo;
- cobertura fotográfica; e
- relatório específico de inspeção.

Para equipamentos dinâmicos, o texto destaca também:

- análise do histórico de operação;
- tempo médio entre falhas;
- ensaios e testes;
- avaliação de mecanismos de dano;
- verificação da instrumentação;
- registro fotográfico e relatório.

### 8.1 Inspeções extraordinárias
Ainda como referência conceitual, o RTSGI prevê inspeção extraordinária quando ocorrer, por exemplo:

- anormalidade que comprometa a segurança operacional;
- alteração de parâmetros operacionais, como pressão máxima de operação, temperatura de projeto ou fluido de trabalho;
- retirada prolongada de operação; ou
- retorno de equipamento fora de operação.

Esses gatilhos são tecnicamente coerentes com o SGSO e ajudam a estruturar a decisão sobre quando uma degradação exige avaliação adicional antes do retorno ao serviço.

**Fontes:** `anp-912dd4dd5be0ece1d8e4973b:p27-32:23.0-9.0`, `anp-912dd4dd5be0ece1d8e4973b:p6-9:0.0-10.0`

## 9. Critérios práticos de decisão para tratamento de degradação de ECSO

Com base nos trechos analisados, um fluxo decisório tecnicamente consistente pode ser resumido assim:

### 9.1 O ECSO atende ao desempenho de projeto e está testado/inspecionado dentro do prazo?
- **Sim:** pode ser tratado como **disponível**, desde que a documentação e a rastreabilidade sejam adequadas.
- **Não:** prosseguir para avaliação de degradação/indisponibilidade.

### 9.2 A falha é parcial ou total?
- **Parcial**, com função comprometida mas não totalmente perdida: tendência a classificar como **degradado**.
- **Total**, sem função de segurança: tendência a classificar como **indisponível**.

### 9.3 Existe contingência formal e implementada?
Se houver medidas temporárias aprovadas, rastreáveis e eficazes para reduzir o risco a níveis aceitáveis, o elemento pode ser tratado como:

- **degradado contingenciado**; ou
- **indisponível contingenciado**.

Se não houver contingência adequada:

- permanece como **degradado** ou **indisponível**; e
- sendo elemento crítico, essa condição pode **impedir a continuidade operacional** do sistema afetado.

### 9.4 A contingência inclui medidas proporcionais ao risco?
O SGSO e as orientações técnicas da ANP apontam, conforme aplicável, para:

- controles alternativos equivalentes;
- limitação ou redução da produção;
- isolamento do sistema;
- parada de equipamentos ou da instalação.

### 9.5 Há prazo definido para permanência da condição temporária?
A contingência só é aceitável se houver:

- prazo definido;
- responsável pela correção;
- acompanhamento da ação corretiva; e
- documentação das decisões.

### 9.6 O evento exige reanálise de risco, inspeção extraordinária ou MOC?
Isso tende a ser necessário quando houver:

- alteração física ou funcional do sistema;
- desvio de projeto;
- mudança de parâmetros operacionais;
- retorno de equipamento após longo período fora de operação; ou
- evidência de que a lista de ECSO precisa ser revista.

**Fontes:** `anp-eec7f988e9eeea4ece5e1b8d:p22-25:52.0-40.0`, `anp-3971dc6c88f4e2d408134aab:p2-3:6.0-47.0`, `anp-21b016bb482410ebc1a9261e:p10:3.0-174.0`, `anp-912dd4dd5be0ece1d8e4973b:p27-32:23.0-9.0`

## 10. Não conformidades e lições observadas pela ANP que ajudam a avaliar a eficácia do SGSO

Os materiais da ANP trazem exemplos práticos de desvios recorrentes que são particularmente úteis para avaliar o desempenho do SGSO na gestão de ECSO e da integridade mecânica.

### 10.1 Exemplos de problemas identificados em fiscalizações e auditorias
Foram citados, entre outros:

- sistemas críticos degradados, como:
  - **Public Address** sem inteligibilidade suficiente das mensagens;
  - sistemas de **dilúvio e drenagem** com bicos aspersores obstruídos e vazão abaixo da requerida;
  - sistema **UPS** com falhas de manutenção;
  - falhas na integridade de tubulações de **gas lift, drenagem, gás inerte e gás combustível**;
- reparos temporários de tubulações **sem evidência de atendimento aos parâmetros normativos**;
- inspeções e recomendações **vencidas** ou sistemas inteiros sem inspeção ao longo da vida operacional;
- alterações físicas relevantes sem **gerenciamento de mudanças**;
- relatórios de teste/performance sem os requisitos requeridos em normas;
- relatórios de inspeção/teste sem preenchimento adequado, sem ações requeridas ou com instruções imprecisas;
- equipamentos fora de operação, em falha ou degradados **sem ordem de manutenção**;
- baixo nível geral de manutenção.

### 10.2 Interpretação técnica dessas evidências
Esses exemplos mostram fragilidades típicas em cinco frentes:

1. **definição insuficiente dos padrões de desempenho** do ECSO;
2. **falha de execução ou de qualidade** em inspeção, teste e manutenção;
3. **falta de rastreabilidade** e de documentação conclusiva;
4. **cultura reativa**, em que o reparo acontece após vazamento ou falha evidente; e
5. **integração deficiente** entre integridade mecânica, análise de riscos e gerenciamento de mudanças.

Quando a ANP observa, por exemplo, que reparos ocorreram após vazamentos, isso é interpretado como indício de cultura organizacional deficiente no gerenciamento da integridade. Em outras palavras, o processo passou a reagir a perdas de contenção já materializadas, em vez de manter o risco controlado por inspeção, análise de mecanismos de dano e intervenção antecipada.

### 10.3 Consequências potenciais
Os documentos citam que falhas nesse campo podem levar a:

- classificação de desvios como **críticos** ou **graves**;
- interdição de tubulações, sistemas ou instalações inteiras; e
- perdas econômicas relevantes associadas à parada da unidade.

Do ponto de vista técnico, essas consequências decorrem do aumento da exposição a cenários de:

- perda de contenção primária;
- incêndio;
- explosão; e
- falha de sistemas de mitigação.

**Fontes:** `anp-b2cfa8a9492ef598716e9685:p52-54:15.0-0.0`, `anp-21b016bb482410ebc1a9261e:p10:3.0-174.0`, `anp-3971dc6c88f4e2d408134aab:p2-3:6.0-47.0`

## 11. Síntese técnica

Para fins de SGSO em FPSOs, a avaliação de ECSO e da integridade mecânica é robusta quando demonstra, por evidências documentais e técnicas, que:

- os **ECSO foram corretamente identificados** e têm função de segurança claramente definida;
- o operador conhece o **desempenho exigido** de cada elemento e os critérios de aceitação correspondentes;
- todos os ECSO relevantes estão cobertos por **planos de inspeção, teste e manutenção**;
- os resultados dessas atividades são **monitorados, avaliados e rastreáveis**;
- degradações e falhas são classificadas de modo coerente como **degradadas, indisponíveis, contingenciadas ou disponíveis**;
- contingências são **temporárias, formais, proporcionais ao risco e com prazo definido**;
- reparos temporários preservam a **contenção primária** e são sustentados por cálculo, norma e controle de qualidade;
- desvios de projeto, alterações operacionais e mudanças físicas passam por **Gerenciamento de Mudanças**;
- análises de risco são usadas para revisar planos, ações e até a própria **lista de ECSO**; e
- a organização evita cultura reativa, atacando **mecanismos de dano, vencimentos de inspeção, recorrência de desvios e não conformidades documentais** antes que evoluam para perda de contenção ou falha de barreira.

Em síntese, **disponibilidade** de ECSO não é mera existência física; é a combinação verificável de **função de segurança preservada, desempenho conforme projeto, confiabilidade mantida, testes válidos, integridade mecânica controlada e contingência adequada quando houver degradação**.

**Fontes:** `anp-eec7f988e9eeea4ece5e1b8d:p22-25:52.0-40.0`, `anp-3971dc6c88f4e2d408134aab:p2-3:6.0-47.0`, `anp-21b016bb482410ebc1a9261e:p10:3.0-174.0`, `anp-b2cfa8a9492ef598716e9685:p52-54:15.0-0.0`, `anp-912dd4dd5be0ece1d8e4973b:p27-32:23.0-9.0`, `anp-912dd4dd5be0ece1d8e4973b:p6-9:0.0-10.0`