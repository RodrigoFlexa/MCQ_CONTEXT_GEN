# Laboratório de instrumentação e calibração

## 1. Finalidade do laboratório no apoio à manutenção de um FPSO

No contexto de manutenção e integridade de ativos em um FPSO, o laboratório de instrumentação e calibração é a estrutura técnica responsável por gerar evidência objetiva de que instrumentos e componentes de medição podem ser **medidos, ajustados, verificados e liberados** com qualidade metrológica adequada ao uso pretendido. Isso inclui, por exemplo, transmissores, sensores, pressostatos, switches, manômetros, termômetros, válvulas de controle com posicionadores e outros dispositivos de malhas de controle.

A capacidade real desse laboratório não depende apenas da existência de bancadas e calibradores. Ela depende de um conjunto coerente de fatores:

- padrões e instrumentos de referência adequados;
- procedimentos documentados;
- rastreabilidade metrológica demonstrável;
- controle das incertezas de medição;
- competência técnica reconhecida dos executantes;
- controle ambiental compatível com a sensibilidade dos ensaios;
- registros que permitam liberação técnica e auditoria posterior.

Em termos práticos, o laboratório deve ser capaz de responder, para cada instrumento liberado: **qual referência foi usada, em quais condições, com qual incerteza, por qual procedimento, por quem e com qual conclusão de aceitação**.

**Fontes:** `petroles-004c2afadba7ea17c7dd7908:pNone:2152060.0-2152092.0`, `petroles-004c2afadba7ea17c7dd7908:pNone:2152094.0-2152129.0`, `petroles-4ee4bce16acf674505c8912d:pNone:636458.0-636503.0`

## 2. Conceitos metrológicos essenciais para calibração e liberação

### 2.1 Calibração não é ajuste

Calibração é a operação que, sob condições especificadas, estabelece a relação entre:

- os valores e incertezas fornecidos por padrões; e
- as indicações correspondentes do instrumento, também com suas incertezas associadas.

O resultado pode ser expresso por:

- declaração;
- função de calibração;
- curva de calibração;
- diagrama ou tabela de calibração;
- correção aditiva ou multiplicativa acompanhada da incerteza associada.

O material destaca que **não se deve confundir calibração com ajuste**. Ajuste modifica o sistema de medição; calibração determina a relação entre indicação e referência. Também não se deve confundir calibração com **verificação**, que é o provimento de evidência objetiva de atendimento a requisitos especificados.

Para a liberação de instrumentos em manutenção, isso significa que o laboratório precisa distinguir pelo menos três atos técnicos:

1. **calibrar**: medir o desvio em relação ao padrão;
2. **ajustar**, se aplicável: intervir no instrumento para reduzir o desvio;
3. **verificar/liberar**: demonstrar que o item atende aos requisitos definidos para o uso pretendido.

### 2.2 Verificação e validação

Verificação é a confirmação, por evidência objetiva, de que o item atende a requisitos especificados. O próprio material ressalta que a verificação **não deve ser confundida com calibração**. Já validação é uma verificação em que se demonstra que os requisitos especificados são adequados ao uso pretendido.

Para um laboratório de FPSO, isso tem implicação direta: um instrumento pode estar calibrado e ainda assim **não ser adequado** para a aplicação, se a incerteza obtida, a faixa útil, a estabilidade ou o critério de aceitação não forem compatíveis com a malha de processo.

### 2.3 Hierarquia de calibração e rastreabilidade metrológica

A rastreabilidade metrológica é a propriedade pela qual um resultado de medição pode ser relacionado a uma referência por meio de uma **cadeia ininterrupta e documentada de calibrações**, cada uma contribuindo para a incerteza de medição. Isso exige uma **hierarquia de calibração** estabelecida.

Os elementos apontados para confirmar essa rastreabilidade incluem:

- cadeia ininterrupta até padrão internacional ou nacional;
- incerteza de medição documentada;
- procedimento de medição documentado;
- competência técnica reconhecida;
- rastreabilidade ao SI;
- intervalos entre calibrações definidos.

Também é importante notar dois pontos críticos do material:

- a incerteza tende a aumentar ao longo da hierarquia de calibração;
- a rastreabilidade metrológica, por si só, **não garante** que a incerteza seja adequada ao objetivo nem elimina erros humanos.

Em um laboratório de bordo, portanto, não basta possuir certificados dos padrões. É preciso demonstrar que os certificados, os procedimentos, os prazos e a aplicação prática desses padrões realmente sustentam a qualidade do resultado emitido pelo laboratório.

**Fontes:** `petroles-004c2afadba7ea17c7dd7908:pNone:2152060.0-2152092.0`, `petroles-004c2afadba7ea17c7dd7908:pNone:2152094.0-2152129.0`, `petroles-004c2afadba7ea17c7dd7908:pNone:2145845.0-2145878.0`

## 3. Incerteza de medição como base da decisão técnica

### 3.1 Conceitos principais

O material apresenta os elementos clássicos de avaliação da incerteza:

- **incerteza padrão combinada**: obtida pela combinação das incertezas associadas às grandezas de entrada do modelo de medição;
- **incerteza expandida**: produto da incerteza padrão combinada por um fator maior que 1;
- **fator de abrangência** `k`: multiplicador usado para obter a incerteza expandida;
- **probabilidade de abrangência** e **intervalo de abrangência**: forma de expressar a probabilidade de o valor verdadeiro estar contido num intervalo especificado;
- **incerteza-alvo**: limite superior especificado em função do uso pretendido do resultado.

Em forma resumida:

`U = k x uc`

onde:

- `uc` = incerteza padrão combinada;
- `k` = fator de abrangência;
- `U` = incerteza expandida.

### 3.2 Balanço de incerteza

Um balanço de incerteza deve incluir, conforme o material:

- modelo de medição;
- estimativas das grandezas de entrada;
- incertezas associadas;
- covariâncias, quando houver correlação;
- tipos de distribuição de probabilidade;
- graus de liberdade;
- tipo de avaliação da incerteza;
- fator de abrangência utilizado.

### 3.3 Fontes típicas de incerteza relevantes ao laboratório

As fontes citadas incluem:

- características do instrumento;
- condições ambientais;
- natureza do mensurando;
- habilidade do operador.

O texto também menciona avaliações dos tipos **A** e **B**:

- tipo A: baseada em tratamento estatístico de medições repetidas;
- tipo B: baseada em certificado de calibração, material de referência, medições prévias, manual do fabricante ou experiência técnica.

### 3.4 Consequência para a liberação de instrumentos

Para fins de liberação, um laboratório tecnicamente robusto precisa demonstrar não apenas o erro encontrado, mas também se a **incerteza obtida é compatível com a decisão de aceitação**. Um resultado com rastreabilidade formal, porém com incerteza alta demais para a aplicação, pode ser insuficiente para liberar o instrumento com segurança operacional.

Além disso, em medições com múltiplas grandezas de entrada, cada uma deve ter sua própria rastreabilidade metrológica, em grau proporcional à contribuição para o resultado final.

**Fontes:** `petroles-004c2afadba7ea17c7dd7908:pNone:2152060.0-2152092.0`, `petroles-004c2afadba7ea17c7dd7908:pNone:2152094.0-2152129.0`, `petroles-4ee4bce16acf674505c8912d:pNone:636458.0-636503.0`

## 4. Infraestrutura e arranjo funcional do laboratório/oficina de instrumentação

Os trechos sobre recursos auxiliares de manutenção de instrumentos indicam uma visão organizacional ainda útil para avaliar a capacidade física do apoio técnico.

### 4.1 Localização e logística interna

É considerado conveniente que oficinas e locais de calibração fiquem próximos das áreas de maior concentração de instrumentos e serviços. A justificativa apresentada é o risco de:

- dano no transporte;
- descalibração por movimentação excessiva;
- aumento de tempo entre retirada, teste e retorno ao serviço.

O material chega a indicar que, pela importância da calibração, pode ser necessário dispor de recursos para execução **em campo** ou em locais preparados próximos à operação, como salas de controle, especialmente para intervenções frequentes.

Para um FPSO, esse raciocínio é particularmente relevante porque deslocamentos internos, vibração e limitações logísticas tendem a tornar desejável a combinação de:

- uma oficina/laboratório principal para serviços mais completos; e
- pontos locais de teste e calibração para intervenções mais recorrentes.

### 4.2 Setorização funcional mínima

O layout sugerido no material distingue ao menos quatro áreas:

1. **área para válvulas de controle e instrumentos mecânicos de maior porte**  
   Com bancadas especiais, suportes para válvulas/instrumentos, dispositivos de serviço e calibração, e recurso de movimentação de peças.

2. **área para manutenção geral de instrumentos**  
   Com bancadas, tomadas elétricas, ar comprimido, morsas e recursos para reparos gerais; pode receber máquinas operatrizes simples e dispositivos de calibração de manômetros e termômetros.

3. **sala de calibração de instrumentos**  
   Destinada aos dispositivos fixos de teste e calibração; convém possuir ar-condicionado, dada a sensibilidade de muitos serviços de calibração.

4. **sala para instrumentos eletrônicos e analisadores**  
   Também com ar-condicionado e com os equipamentos eletrônicos de teste e ferramentas específicas.

### 4.3 Recursos materiais e organização interna

O material menciona, como recursos auxiliares relevantes:

- equipamentos e dispositivos de teste e calibração;
- ferramentas;
- máquinas operatrizes;
- bancadas de serviço;
- locais apropriados para guarda de peças e sucata aproveitável, evitando acúmulo sobre bancadas.

Esse conjunto é importante porque a capacidade do laboratório não se resume à medição em si. Ela também envolve:

- recebimento físico do instrumento;
- desmontagem ou preparação para teste, quando aplicável;
- conexão segura aos dispositivos de calibração;
- eventual reparo ou ajuste;
- nova verificação e preservação até a reinstalação.

### 4.4 Controle ambiental

A recomendação explícita de ar-condicionado para salas de calibração e para serviços eletrônicos mostra que o ambiente deve ser controlado de modo compatível com a natureza da medição. Isso é coerente com o fato de que condições ambientais são fonte de incerteza.

Portanto, ao avaliar a capacidade do laboratório, é pertinente verificar se ele controla, conforme aplicável ao tipo de instrumento:

- temperatura;
- estabilidade do ambiente;
- condições de alimentação elétrica;
- qualidade do ar comprimido de teste;
- proteção dos instrumentos sensíveis durante transporte e manuseio.

**Fontes:** `regis-a448305960d327e79c9a0631:pNone:152.60-176.0`, `petroles-004c2afadba7ea17c7dd7908:pNone:981095.0-981149.0`, `petroles-4ee4bce16acf674505c8912d:pNone:636458.0-636503.0`

## 5. Elementos que demonstram capacidade de calibração com rastreabilidade metrológica

Uma avaliação profissional da capacidade do laboratório pode ser estruturada em perguntas técnicas objetivas.

### 5.1 Padrões e referências

O laboratório precisa demonstrar que seus padrões de medição:

- são usados como referência nos processos de calibração;
- possuem valor e incerteza associados bem determinados;
- são conservados de forma a preservar suas características metrológicas dentro de limites apropriados;
- possuem certificados e prazos válidos dentro da hierarquia de calibração aplicável.

### 5.2 Procedimentos documentados

A rastreabilidade metrológica exige procedimento de medição documentado. Logo, a capacidade do laboratório é enfraquecida quando a execução depende apenas de experiência tácita do técnico, sem procedimento que defina pelo menos:

- condições especificadas de calibração;
- referência utilizada;
- pontos de medição na faixa;
- forma de expressão do resultado;
- método de cálculo ou declaração da incerteza;
- critério de verificação/aceitação.

### 5.3 Competência técnica

O material associa a confirmação da rastreabilidade à competência técnica reconhecida. Em termos de avaliação de capacidade, isso significa que o laboratório deve ter pessoal apto a:

- selecionar o padrão correto;
- interpretar certificados;
- executar o procedimento sob as condições especificadas;
- identificar quando o resultado requer correção, ajuste, nova verificação ou rejeição do item.

### 5.4 Intervalos entre calibrações

Os intervalos entre calibrações fazem parte dos elementos necessários para confirmar a rastreabilidade. Portanto, não basta calibrar bem uma vez; é necessário demonstrar que padrões e instrumentos permanecem dentro de um regime de controle temporal coerente.

### 5.5 Registros para liberação

Após a execução do serviço, o laboratório deve ser capaz de emitir registros que permitam reconstruir a decisão de liberação. À luz dos conceitos do material, isso inclui ao menos:

- identificação do instrumento e do padrão utilizado;
- data e condições da calibração;
- resultado obtido e correções, quando aplicáveis;
- incerteza associada;
- referência metrológica utilizada;
- conclusão de verificação quanto ao requisito especificado;
- identificação do responsável técnico pela execução.

**Fontes:** `petroles-004c2afadba7ea17c7dd7908:pNone:2152060.0-2152092.0`, `petroles-004c2afadba7ea17c7dd7908:pNone:2152094.0-2152129.0`, `petroles-4ee4bce16acf674505c8912d:pNone:636458.0-636503.0`

## 6. Fluxo técnico de calibração, ajuste e liberação

Com base nos conceitos metrológicos fornecidos, um fluxo coerente de trabalho para o laboratório pode ser descrito assim:

1. **Recebimento e identificação do item**  
   Confirmar o instrumento, faixa, função e vínculo com o serviço.

2. **Seleção do procedimento e da referência metrológica**  
   Escolher padrão, método e condições de ensaio compatíveis.

3. **Execução da calibração sob condições especificadas**  
   Obter a relação entre padrão e indicação do instrumento.

4. **Expressão do resultado**  
   Emitir declaração, curva, tabela ou correção, com incerteza associada.

5. **Ajuste, quando necessário e permitido**  
   Caso o instrumento demande intervenção, o ajuste não substitui a calibração; ele deve ser tratado como ato distinto.

6. **Verificação para fins de aceitação/liberação**  
   Demonstrar, com evidência objetiva, que o item atende aos requisitos especificados para o uso pretendido.

7. **Registro e liberação**  
   Emitir evidência rastreável, preservando o histórico do serviço.

Esse fluxo é importante porque evita uma falha comum: tratar um simples ajuste de bancada como se fosse, por si só, comprovação metrológica suficiente para retorno ao serviço.

**Fontes:** `petroles-004c2afadba7ea17c7dd7908:pNone:2152060.0-2152092.0`, `petroles-004c2afadba7ea17c7dd7908:pNone:2152094.0-2152129.0`

## 7. Exemplos técnicos aplicáveis à avaliação da capacidade do laboratório

### 7.1 Sensores e transmissores de pressão com sinal 4-20 mA

Um exemplo descrito utiliza um calibrador portátil Druck DPI-615, com certificado de calibração do fabricante, para aferição de sensores de pressão. O equipamento fornecia pressão conhecida por bomba interna, dispunha de fonte de 24 V e realizava leitura da corrente transmitida pelo sensor, permitindo ensaiar instrumentos com faixa de 4-20 mA sem necessidade de fonte e multímetros externos.

Esse exemplo mostra alguns pontos relevantes para um laboratório de FPSO:

- um calibrador multifuncional aumenta a autonomia da bancada e do trabalho em campo;
- a capacidade de gerar a variável de processo e ler o sinal elétrico no mesmo equipamento simplifica o arranjo de teste;
- a avaliação da faixa do instrumento e da exatidão do padrão de referência é parte essencial da decisão de adequação do recurso de calibração.

Também foram citadas diferentes precisões do calibrador, dependendo da faixa de pressão. Isso é importante porque a capacidade do laboratório não deve ser avaliada genericamente; ela precisa ser verificada **para a faixa e o tipo de instrumento efetivamente tratados**.

### 7.2 Medidores de vazão: calibração, curvas e validação prática

Os exemplos de medidores de vazão mostram duas situações importantes:

- medidores calibrados pelo fabricante, com certificado de aferição e incerteza declarada;
- validações complementares usando tanque graduado e cronômetro para confrontar a leitura do sensor com um volume conhecido ao longo do tempo.

Além disso, no caso de medição de vazão de ar, o material indica uso de curvas e tabelas de calibração fornecidas pelo fabricante e correções associadas às condições de referência e de operação real. A implicação prática é clara: **nem todo instrumento pode ser tratado por simples comparação linear em bancada**. Alguns exigem aplicação correta de curva de calibração, condições padronizadas e variáveis de influência.

Isso reforça que a capacidade do laboratório envolve não só possuir padrões, mas também saber aplicar a forma correta de expressão do resultado metrológico: tabela, curva, correção ou função de calibração.

### 7.3 Válvulas de controle com posicionadores inteligentes

Outro exemplo relevante relata a instalação de posicionadores inteligentes em válvulas de controle, capazes de fornecer dados gráficos relacionados ao posicionamento da haste e à pressão de ar comprimido no atuador. As informações eram transmitidas para a sala de controle e analisadas por meio de ferramenta específica, permitindo monitoramento de assinaturas e diagnóstico de anomalias, inclusive em caráter preditivo.

Para um laboratório de instrumentação, esse caso é relevante porque mostra que a liberação técnica de um componente pode ir além da calibração clássica de sinal. Em válvulas de controle, a decisão sobre retorno ao serviço pode requerer também evidências funcionais, como:

- coerência entre comando e posicionamento;
- comportamento da assinatura do posicionador;
- detecção de sintomas de desgaste, má instalação, dano ou vazamento.

Assim, a capacidade do laboratório pode incluir dois níveis complementares:

- **capacidade metrológica**, para calibrar e verificar sinais e referências;
- **capacidade diagnóstica funcional**, para interpretar o comportamento do conjunto válvula-posicionador e apoiar a decisão entre liberar, reparar a bordo ou encaminhar para serviço especializado.

**Fontes:** `regis-476facaf06f6aba284b450bf:pNone:1099.0-1172.0`, `regis-13fcf16cf864daa63ae34ce3:pNone:767.0-1033.0`

## 8. Critérios práticos para avaliar a suficiência do laboratório

À luz do material disponível, um laboratório de instrumentação e calibração pode ser considerado tecnicamente mais robusto quando apresenta, de forma integrada:

- **rastreabilidade metrológica demonstrável** dos padrões e resultados;
- **incerteza documentada** e coerente com o uso pretendido;
- **separação conceitual e documental** entre calibração, ajuste e verificação;
- **infraestrutura setorizada**, com ambiente apropriado para calibração e eletrônica sensível;
- **proximidade operacional** ou recursos de campo para reduzir riscos de dano e descalibração por transporte;
- **instrumentação de teste adequada à faixa e ao princípio de medição** do item ensaiado;
- **capacidade de emitir registros rastreáveis** que sustentem a liberação;
- **capacidade de diagnóstico complementar**, especialmente para válvulas com posicionadores inteligentes e outros dispositivos com dados de condição.

Em contrapartida, a capacidade é questionável quando o laboratório:

- não demonstra cadeia de rastreabilidade dos padrões;
- não informa a incerteza associada aos resultados;
- usa “calibração” como sinônimo de ajuste;
- libera instrumentos com base apenas em intervenção de bancada sem evidência de verificação;
- não controla adequadamente o ambiente para instrumentos sensíveis;
- não dispõe de procedimento documentado para instrumentos cuja resposta depende de curva, tabela ou condições de influência.

**Fontes:** `petroles-004c2afadba7ea17c7dd7908:pNone:2152060.0-2152092.0`, `petroles-004c2afadba7ea17c7dd7908:pNone:2152094.0-2152129.0`, `regis-a448305960d327e79c9a0631:pNone:152.60-176.0`, `regis-476facaf06f6aba284b450bf:pNone:1099.0-1172.0`, `regis-13fcf16cf864daa63ae34ce3:pNone:767.0-1033.0`

## 9. Síntese

Para fins de apoio técnico à manutenção em FPSO, a avaliação da capacidade do laboratório para calibração, ajuste e liberação de instrumentos com rastreabilidade metrológica deve considerar simultaneamente:

- base conceitual metrológica correta;
- adequação de padrões, procedimentos e incerteza;
- infraestrutura física e ambiental compatível;
- competência para ensaios em sinais, variáveis de processo e funções de controle;
- emissão de registros que transformem a atividade de bancada em evidência técnica confiável para retorno ao serviço.

Em resumo, o laboratório competente não é apenas aquele que “mede” instrumentos. É aquele que consegue **medir, interpretar, documentar e justificar tecnicamente a liberação**, mantendo a ligação metrológica do resultado com uma referência reconhecida e com incerteza conhecida.

**Fontes:** `petroles-004c2afadba7ea17c7dd7908:pNone:2152060.0-2152092.0`, `petroles-004c2afadba7ea17c7dd7908:pNone:2152094.0-2152129.0`, `regis-a448305960d327e79c9a0631:pNone:152.60-176.0`, `petroles-4ee4bce16acf674505c8912d:pNone:636458.0-636503.0`