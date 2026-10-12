# Oficina elétrica e testes em FPSO

## 1. Papel da oficina elétrica no apoio à manutenção offshore
A oficina elétrica de um FPSO dá suporte ao diagnóstico, ensaio, reparo, ajuste e liberação técnica de equipamentos e circuitos cuja indisponibilidade pode afetar produção, segurança de processo, habitabilidade e resposta a emergências. Na prática, isso inclui pelo menos motores, painéis, CCMs, sistemas de corrente contínua, UPS, lógica de comando e parte da instrumentação/elétrica associada aos equipamentos de processo.

Em um exemplo de arquitetura de unidade investigada pela ANP, a instalação possuía geração principal e de emergência em **480 Vca**, sistemas de **24 Vcc** para painéis de controle e CLP, além de **UPS em 120 Vca** para cargas vitais de operação e supervisão. O mesmo caso mostra que podia existir condição de **realimentação (back feeding)** sob requisitos específicos. Para a oficina elétrica, isso é relevante porque o diagnóstico e a liberação de circuitos não podem considerar apenas a alimentação principal: é necessário verificar interligações, fontes auxiliares, UPS, comandos remotos, CLP e arranjos de transferência antes de bloquear, testar ausência de tensão e reenergizar.

**Implicação prática:** uma oficina elétrica eficiente em FPSO não é apenas um local de reparo; ela funciona como centro técnico de ensaios e de controle de risco elétrico, articulado com operação, sala de controle e planejamento da manutenção.

**Fontes da seção:** `anp-80a4074406f1461613df01eb:p6-8:34.0-52.0`, `regis-74dd376119cbb653fe9922bc:pNone:7096.0-7587.0`

## 2. Infraestrutura, recursos e controles de segurança elétrica
Para diagnóstico e reparo com segurança, a oficina elétrica e os locais de intervenção devem dispor de infraestrutura compatível com o nível de tensão, o risco de arco elétrico e a condição ambiental da unidade offshore.

### 2.1 EPIs, ferramentas e instrumentos
Os trabalhos em eletricidade requerem atenção especial à condição física e ao estado de alerta do executante, inclusive por efeito de turno e fadiga. Além das boas condições para o trabalho, a fonte destaca o uso de EPIs adequados, incluindo, conforme o risco:
- capuz;
- proteção facial;
- bota de segurança para eletricista;
- vestimentas de proteção contra arco elétrico;
- luvas isolantes compatíveis com o nível de energia incidente.

Ferramentas e dispositivos com isolamento elétrico devem:
- ser compatíveis com as tensões envolvidas;
- ser inspecionados e testados conforme regulamentação aplicável ou recomendação do fabricante;
- ter registros rastreáveis quando aplicável.

Para alta tensão, dispositivos como luvas isolantes, varas de manobra e detectores de tensão devem ser inspecionados/testados conforme instrução do fabricante; na falta desta, a fonte menciona periodicidade anual, com registros rastreáveis. Em baixa tensão, ferramentas manuais devem ser do tipo isolado e sofrer inspeção visual regular e antes do uso.

Instrumentos portáteis de medição devem possuir certificado de aferição. As pontas de prova devem ser compatíveis com a categoria do instrumento. A fonte recomenda multímetros no mínimo **categoria III**, e **categoria IV** quando o trabalho ocorrer em painéis conectados diretamente a redes aéreas.

### 2.2 Recursos fixos e portáteis de proteção
A fonte menciona, para subestações e salas de painéis, disponibilidade e identificação de:
- bastão isolante de resgate;
- manta antichama;
- tapetes isolantes na frente e, se acessível, atrás de painéis BT e AT;
- conjunto de aterramento temporário;
- detector de tensão e bastão de manobra compatíveis com o nível de tensão.

Painéis portáteis de distribuição, inclusive os usados para equipamentos temporários, devem possuir **proteção por DR**. Luminárias portáteis para compartimentos metálicos ou molhados devem ser ligadas por transformador isolador, por tomada com DR ou por extra-baixa tensão. Cabos de alimentação devem estar secos, íntegros, com isolação compatível, e as extensões devem permitir fácil visualização e inspeção.

### 2.3 Áreas classificadas e arranjo físico
Equipamentos elétricos destinados a áreas classificadas devem ter características construtivas adequadas à classificação da área e possuir certificação de conformidade. Isso impacta tanto o material usado em campo quanto, em certos casos, equipamentos portáteis empregados pela manutenção.

Salas de equipamentos elétricos, compartimentos e invólucros **não devem ser usados como área de armazenamento** ou posto de trabalho genérico. Também devem possuir sinalização de segurança com restrição de acesso a trabalhadores não autorizados.

### 2.4 Arco elétrico, comunicação e prontidão para emergência
Painéis elétricos devem ser sinalizados com o valor de energia incidente de arco elétrico, conforme citado na fonte. Em manobras e serviços em painéis de distribuição ou CCM, o trabalhador deve dispor de meio de comunicação com a equipe ou com a sala de controle durante a atividade.

O plano de emergência deve contemplar cenários de acidente com eletricidade, incluindo **choque** e **arco elétrico**. A fonte também reforça o direito de recusa diante de risco grave e iminente.

**Fontes da seção:** `petroles-004c2afadba7ea17c7dd7908:pNone:1994310.0-1994344.0`, `petroles-004c2afadba7ea17c7dd7908:pNone:1879939.0-1880029.0`

## 3. Planejamento, permissão de trabalho e critérios para intervenção
A oficina elétrica não deve separar ensaio técnico de controle formal de risco. Em FPSO, a intervenção elétrica depende de autorização, análise de risco, bloqueio efetivo e disciplina operacional.

### 3.1 Princípio básico: priorizar desenergização
A fonte é explícita ao priorizar medidas de proteção coletiva, em especial a **desenergização do circuito**. Na impossibilidade, deve-se empregar outras medidas, como isolamento de partes vivas, barreiras físicas, tapetes e mantas isolantes, varas de manobra, sinalização, seccionamento automático e bloqueio do religamento automático ou de outras fontes.

Um ponto operacional importante para a oficina: serviço em instalação apenas "desligada", mas **sem bloqueio** e ainda com possibilidade de energização por qualquer motivo, deve ser tratado com as exigências de serviço em instalação energizada.

### 3.2 Permissão, análise de risco e condições ambientais
Trabalhos de alto potencial de risco devem envolver o trabalhador autorizado no processo de emissão da PT. Não é permitido intervir em equipamentos energizados sob chuva e descargas atmosféricas. Em chuvisco ou condição atmosférica amena, a possibilidade de execução depende de análise preliminar de risco por profissional habilitado/autorizado.

Também não é permitido usar escadas ou andaimes metálicos para intervenção em circuitos ou equipamentos energizados.

### 3.3 Trabalho em dupla e zonas de trabalho
Serviços energizados em alta tensão devem ser executados por no mínimo dois trabalhadores autorizados, com comunicação entre si e com a equipe. Em baixa tensão, o risco do trabalho individual deve ser avaliado; se o serviço for de alto potencial de risco, como inserção/extração de gavetas, o trabalho deve ser preferencialmente em dupla.

A fonte diferencia **zona livre**, **zona controlada** e **zona de risco**. Em inserção ou retirada de gavetas energizadas, apenas os autorizados envolvidos na atividade devem permanecer na zona controlada/risco; os demais devem ficar na zona livre.

### 3.4 Área classificada e ingresso em zona controlada
O trabalho em área classificada deve ser realizado com circuito desenergizado. Se isso for inviável, é necessário procedimento específico baseado em análise de risco. Devem existir procedimentos específicos também para atividades que exijam ingresso na zona controlada.

### 3.5 Verificação de ausência de tensão: testar antes de tocar
A verificação de presença/ausência de tensão deve ser feita **sempre**, independentemente de ações anteriores. A rotina indicada é "testar antes de tocar". Os detectores de tensão devem ser conferidos em fonte energizada conhecida **antes e depois** da verificação do circuito.

Esse ponto é crítico em FPSOs por causa de fontes múltiplas: alimentação principal, emergência, UPS, 24 Vcc, comandos remotos, partida automática, supervisório e CLP.

**Fontes da seção:** `petroles-004c2afadba7ea17c7dd7908:pNone:1994346.0-1994394.0`, `petroles-004c2afadba7ea17c7dd7908:pNone:1994310.0-1994344.0`, `anp-80a4074406f1461613df01eb:p6-8:34.0-52.0`

## 4. Bloqueio, etiquetagem, comandos remotos e reenergização
### 4.1 Bloqueio e etiquetagem
Para bloqueio de gavetas, disjuntores e chaves seccionadoras com intervenção no equipamento, a fonte descreve uma prática robusta em que:
- são usados pelo menos **dois cadeados**: um pelo responsável da manutenção e outro pelo operador;
- não se usa grupo de cadeados com chave mestra;
- cada cadeado é aberto apenas por sua própria chave;
- a etiqueta de advertência continua obrigatória, mesmo com o cadeado.

Em circuitos com comandos múltiplos, como botoeira remota, partida automática, supervisório ou CLP, deve existir meio de bloqueio efetivo para impedir energização acidental, inclusive com teste prévio do circuito bloqueado.

### 4.2 Suspensão do serviço
Serviços em instalações energizadas ou em suas proximidades devem ser imediatamente suspensos quando surgir iminência de ocorrência perigosa. Qualquer executante ou superior pode interromper o trabalho.

### 4.3 Reenergização e liberação final
Antes de reenergizar circuitos/equipamentos que sofreram intervenção, a fonte lista providências mínimas:
- recolher ferramentas, materiais e equipamentos;
- manter o local limpo;
- afastar da zona controlada quem não participa da reenergização;
- remover aterramentos temporários, equipotencialização e proteções adicionais;
- retirar etiquetas e sinalização de isolamento apenas quando a condição de normalidade estiver confirmada;
- remover bloqueios e travamentos.

Em termos de oficina elétrica, isso significa que a **liberação técnica** não é apenas o término do reparo: ela exige confirmação formal de integridade, recomposição do sistema e prontidão segura para retorno ao serviço.

**Fontes da seção:** `petroles-004c2afadba7ea17c7dd7908:pNone:1994366.0-1994420.0`, `petroles-004c2afadba7ea17c7dd7908:pNone:1994346.0-1994394.0`

## 5. Ensaios de diagnóstico e critérios de decisão em motores elétricos
Motores elétricos são itens típicos de oficina elétrica em FPSO, seja para inspeção pré-operação, retorno de sobressalente ao estoque, avaliação pós-reparo ou análise de falha.

### 5.1 Variáveis e verificações úteis
Uma rotina de acompanhamento citada na fonte inclui verificar:
- chaves seccionadoras;
- fusíveis de força e comando;
- conexões principais e fiação;
- sinalização e lâmpadas;
- relés;
- vibrações espúrias;
- elevação de temperatura;
- isolação;
- temperatura do motor e do ambiente;
- umidade relativa do ar;
- corrente, tensão e fator de potência;
- identificação do instrumento de medição;
- data e identificação do eletricista.

Essa lógica é adequada à oficina elétrica porque integra diagnóstico elétrico, condição ambiental, rastreabilidade metrológica e decisão de liberar ou não o equipamento.

### 5.2 Resistência de isolação e índice de polarização
A fonte descreve o uso de **Megger** com leitura em 60 s, usualmente em **1 000 Vcc** e, em certos casos, **500 Vcc**. Também registra o uso do **índice de polarização (PI)** como critério adicional.

Aspectos técnicos importantes extraídos da fonte:
- o Megger mostra a resistência instantânea à passagem de corrente pelo isolante sob tensão contínua aplicada;
- leitura próxima de zero indica que o motor não deve ser energizado;
- o ensaio de isolação, isoladamente, **não garante** que o motor não venha a falhar após energizado.

### 5.3 Curva de absorção de umidade
Para investigar umidade, a fonte propõe levantar a curva **isolação x tempo**, com leitura na hora zero e depois a cada duas horas, por até 24 h ou até a isolação se aproximar de zero. Recomenda-se medir, preferencialmente, as três fases separadamente.

Interpretação útil para a oficina:
- se as três curvas forem semelhantes, a baixa isolação tende a estar distribuída ao longo dos enrolamentos;
- se uma curva divergir muito das demais, pode haver baixa isolação localizada em uma fase específica.

Isso ajuda a distinguir entre problema difuso por umidade e defeito localizado do enrolamento.

### 5.4 Secagem controlada do motor
A mesma fonte descreve uma prática de secagem por corrente contínua no estator, com injeção crescente até **50% da corrente nominal** ou até **70 °C no cobre**, com taxa de elevação de temperatura inferior a **7 °C/h**. Para secagem mais eficiente, menciona resistências auxiliares, cobertura e exaustão do ar úmido.

Durante a secagem, as leituras de isolação devem ser registradas periodicamente para formar a curva de secagem. A curva pode apresentar uma "barriga": sobe, depois cai, e volta a subir; portanto, a evolução não é necessariamente monotônica.

### 5.5 Faixas de decisão para liberação: uso com cautela
A fonte relata uma convenção prática de decisão baseada em resistência de isolação:
- **acima de 100 MΩ**: liberar o motor;
- **entre 10 e 100 MΩ**: liberar somente sob condições adicionais, como PI maior que 1,5 e confirmação de contexto favorável;
- **abaixo de 10 MΩ**: não liberar; comunicar ao controle e tratar a baixa isolação.

Como apoio adicional, a mesma fonte menciona valores fase-terra superiores a **2 000 MΩ a 20 °C**, corrigidos para essa temperatura, e **PI > 1,5** como referência de recebimento. Em oficina de FPSO, esses números só devem ser usados se compatíveis com fabricante, classe do motor, tensão nominal, procedimento corporativo e norma adotada.

### 5.6 Outros ensaios úteis
A fonte também descreve:
- **medidor de baixa resistência ôhmica** para comparar resistências de fase e investigar curto entre espiras;
- **detector de espira aberta/curto-circuitada**;
- uso de multímetro/ohmímetro para verificar continuidade à massa quando a isolação permanece muito baixa.

**Fontes da seção:** `regis-786ec96c222231847ec16dbc:pNone:26.0-79.0`

## 6. Bancada de testes e organização técnica da oficina
Como referência de arquitetura de bancada de ensaio, uma fonte REGIS descreve um arranjo com:
- quadro de energia com sistema de proteção por relés térmicos, fusíveis, disjuntores e contatores;
- transdutores para potência ativa, potência reativa, força e corrente;
- sensores de temperatura do tipo RTD;
- inversor parametrizável;
- sistema de aquisição de dados e supervisório computacional;
- dispositivos de controle de carga e de posição.

Embora esse caso seja de laboratório e não de oficina de FPSO, ele ilustra um princípio útil: a bancada de testes deve separar claramente:
1. **alimentação e proteção**;
2. **acionamento controlado**;
3. **instrumentação de medição**;
4. **aquisição/registro de dados**;
5. **critérios de parada segura**.

Em oficina elétrica offshore, essa lógica é particularmente importante para testes pós-reparo de motores, painéis, conjuntos portáteis, acionamentos e módulos reparáveis.

**Fontes da seção:** `regis-3d3198096e7a51fa9b7aa6ee:pNone:404.0-450.0`

## 7. Liberação técnica, qualificação da equipe e prontidão para emergência
A fonte reforça que trabalhos em eletricidade devem ser executados por trabalhador **autorizado** e com a capacitação, qualificação ou habilitação requeridas. Para a oficina elétrica, isso implica que nem todo técnico de manutenção genérico está automaticamente apto a diagnosticar, testar e liberar circuitos elétricos críticos.

O trabalhador autorizado, segundo a fonte, deve:
- conhecer os locais e dispositivos de desligamento de emergência;
- saber executar resgate com bastão de resgate;
- saber prestar primeiros socorros;
- saber aplicar manta antichama;
- saber operar os equipamentos portáteis de combate a incêndio das instalações elétricas.

Além disso, trabalhadores que atuam em área classificada devem ter treinamento específico quando autorizados a intervir nessas áreas.

Para fins de liberação técnica, uma boa prática coerente com as fontes é exigir que o reparo só seja encerrado quando houver evidência documentada de que:
- o defeito foi identificado ou o sintoma foi reproduzido/controlado;
- o ensaio aplicável foi executado com instrumento válido;
- o resultado foi comparado com critério definido;
- o circuito/equipamento foi recomposto, bloqueios retirados no momento correto e a reenergização foi controlada.

**Fontes da seção:** `petroles-004c2afadba7ea17c7dd7908:pNone:1994366.0-1994420.0`, `petroles-004c2afadba7ea17c7dd7908:pNone:1994310.0-1994344.0`

## 8. Rastreabilidade, cadastro técnico e integração com CMMS
A oficina elétrica depende de rastreabilidade para que o reparo seja auditável, repetível e útil à confiabilidade do FPSO.

Uma fonte REGIS, baseada em cadastro de confiabilidade/manutenabilidade, indica que motores elétricos podem requerer no CMMS dados como:
- máquina acionada;
- tipo de proteção **Ex**;
- grau de proteção **IP**;
- tipo de motor;
- velocidade de projeto;
- potência;
- tensão de alimentação;
- classe de isolamento do rotor e do estator;
- elevação de temperatura;
- existência de variador de velocidade;
- potência típica de operação.

A mesma fonte mostra a importância de definir **fronteiras hierárquicas** entre sistemas, por exemplo: geração principal, distribuição principal, distribuição normal, geração de emergência, corrente contínua e UPS, distribuição de emergência e cargas de processo. Para um painel, não basta cadastrar apenas o conjunto: disjuntores, relés e itens manuteníveis relevantes podem precisar de identificação individual por cubículo/subunidade.

Aplicado à oficina elétrica, isso significa que os registros de teste e reparo devem se conectar ao cadastro correto do ativo. Exemplos de rastros úteis:
- tag do equipamento e subunidade;
- número de série;
- condição Ex/IP quando aplicável;
- certificado de aferição do instrumento usado;
- número de identificação do Megger ou do equipamento de teste;
- valores medidos, condições ambientais e critério de aceitação;
- responsável técnico e data;
- decisão final: liberado, restrito, preservado ou enviado para serviço externo.

Sem essa estrutura, a oficina pode até consertar, mas não consegue demonstrar qualidade do reparo nem alimentar análise de falhas e confiabilidade.

**Fontes da seção:** `regis-74dd376119cbb653fe9922bc:pNone:7096.0-7587.0`, `regis-786ec96c222231847ec16dbc:pNone:26.0-79.0`

## 9. Fatores humanos relevantes para a oficina elétrica offshore
A fonte Petrolês destaca que o regime de embarque, a mudança de turno e a perda de sono podem reduzir o estado de alerta, especialmente nas primeiras noites de trabalho, além de afetar humor e atitude frente à segurança. Para trabalhos em eletricidade, isso é crítico porque a atividade depende de atenção sustentada, cumprimento estrito de sequência e resposta adequada a sinais de perigo.

Portanto, na gestão da oficina elétrica e dos testes em campo, a competência técnica deve ser acompanhada por controle de fadiga, comunicação efetiva e possibilidade real de interromper o serviço quando o risco se elevar.

**Fontes da seção:** `petroles-004c2afadba7ea17c7dd7908:pNone:1994310.0-1994344.0`

## 10. Síntese operacional
Em um FPSO, a oficina elétrica para diagnóstico, ensaios e reparos deve combinar quatro eixos:
1. **segurança elétrica rigorosa**, com prioridade à desenergização, bloqueio efetivo, teste de ausência de tensão e controle de arco elétrico;
2. **capacidade técnica de ensaio**, especialmente para motores, painéis, circuitos auxiliares, UPS e comandos;
3. **liberação técnica formal**, com critérios definidos e reenergização controlada;
4. **rastreabilidade no CMMS**, para que o reparo se converta em dado de confiabilidade, histórico e tomada de decisão.

Quando esses eixos falham, a oficina deixa de ser apoio à manutenção e passa a ser uma fonte adicional de risco operacional.