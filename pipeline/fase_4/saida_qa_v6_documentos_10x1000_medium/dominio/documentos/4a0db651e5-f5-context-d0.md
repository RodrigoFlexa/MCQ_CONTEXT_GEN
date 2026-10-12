# Bypasses, falhas e revisão por mudanças em sistemas F&G

## 1. Enquadramento técnico da faceta

Em FPSOs, o sistema de fogo e gás (F&G) é tipicamente tratado como **elemento crítico de segurança operacional**, porque sua perda de disponibilidade, degradação de desempenho ou supressão de alarmes reduz a capacidade de detectar precocemente liberações inflamáveis, gases tóxicos e condições precursoras de incêndio. Na ótica de gestão apresentada pela ANP, falha, degradação ou indisponibilidade de elementos críticos — inclusive por **bypass, override, inibições** ou falha na execução de testes/verificações — deve estar coberta por **contingência prévia, robusta e adequada**, capaz de manter o risco em nível aceitável. Se isso não for possível, a contingência pode precisar incluir **parada de equipamentos, de sistemas ou até da planta**.

Para a faceta "bypasses, falhas e revisão por mudanças", o ponto central não é apenas o defeito do detector em si, mas o **processo de decisão** que mantém ou não a eficácia da função de detecção quando a instalação está fora da sua condição nominal: detector indisponível, área com inibição temporária, falhas recorrentes, alteração de processo, uso de linhas temporárias, abertura frequente de vents, aquecimento excepcional de tanques, mudanças de alinhamento, ou documentação desatualizada em situação de emergência.

_Fontes da seção_: ["anp-21b016bb482410ebc1a9261e:p7-8:159.0-109.0", "anp-dabfb60617e4f0ede433578e:p164-167:14.0-11.0", "anp-dabfb60617e4f0ede433578e:p163-165:7.0-22.0"]

## 2. Terminologia operacional relevante para indisponibilidades do F&G

Os trechos fornecidos distinguem conceitos úteis para operação e troubleshooting:

- **Bypass**: desvio aplicado a pontos de entrada, citado no material como aplicável a inicializadores de ESD. É operação **excepcional**, documentada e sujeita a análise de riscos e autorização hierárquica apropriada.
- **Override**: forçamento de pontos de saída para manter um atuador ativo ou inativo, também sob os mesmos critérios restritivos de segurança operacional.
- **Inibição**: forma **controlada e temporária** de desabilitar a anunciação do alarme por ação manual.
- **Desabilitação do alarme**: impedir a anunciação mesmo existindo condição para ativação.
- **Alarme de sistema**: alarme originado de falhas em hardware, software, instrumentos de campo ou comunicações.
- **Log de alarme / registro de eventos / histórico de variáveis**: base essencial para identificar repetição de falhas, alarmes incômodos, perda de comunicação, e degradação progressiva do desempenho.

Aplicado ao F&G, isso significa que nem toda perda de proteção é igual. Há diferença entre:

1. **detector saudável, mas temporariamente inibido**;
2. **detector em falha** ou com problema de comunicação/alimentação;
3. **lógica de alarme/trip desviada por bypass**;
4. **atuação associada forçada por override**;
5. **alarme anunciado, porém tratado como incômodo de forma repetitiva**.

Essa distinção é crítica porque cada caso demanda tratamento diferente em termos de contingência, rastreabilidade, prazo de restauração e impacto na operação.

_Fontes da seção_: ["petroles-004c2afadba7ea17c7dd7908:pNone:2452720.0-2452749.0", "anp-21b016bb482410ebc1a9261e:p7-8:159.0-109.0"]

## 3. Gestão de indisponibilidades: o que caracteriza uma resposta aceitável

A ANP explicita a expectativa de que o operador tenha, **antes da ocorrência**, procedimento que dê diretrizes para contingenciar degradações e indisponibilidades de elementos críticos. Isso é diretamente aplicável ao F&G: um detector isolado, uma zona com sensores indisponíveis, uma votação reduzida, uma perda de comunicação, ou a inibição deliberada de alarmes não podem ser tratados apenas como ocorrência de manutenção; devem ser tratados como **alteração do perfil de risco da instalação**.

Pontos técnicos relevantes para a decisão:

### 3.1 Contingência deve ser proporcional ao impacto real na função de segurança

A contingência precisa ser suficiente para deixar o risco em nível aceitável. Logo, para F&G, a decisão não deveria se limitar a "pode operar / não pode operar"; deve considerar pelo menos:

- área afetada e ocupação humana;
- cenários de liberação plausíveis durante a indisponibilidade;
- existência de cobertura remanescente por outros detectores ou camadas independentes;
- perda de ações automáticas associadas (por exemplo, alarmes gerais, ESD, isolamento, HVAC, deluge, shutdowns), quando aplicável;
- duração prevista da indisponibilidade e capacidade real de resposta operacional.

Quando a contingência não for suficiente, a própria ANP admite que pode ser necessária **redução operacional ou parada**.

### 3.2 Medida compensatória procedimental só é válida se tiver robustez demonstrável

O material da ANP alerta que barreiras procedimentais, como uso de pessoas para executar ações compensatórias, só são aceitáveis se formalizadas com o mesmo rigor de uma barreira relevante para risco. Isso implica, para F&G degradado:

- procedimento crítico específico;
- treinamento prático dos envolvidos;
- verificação do efetivo mínimo necessário;
- análise temporal para confirmar se a ação humana ocorre dentro do tempo útil do cenário;
- avaliação das interfaces homem-máquina necessárias para executar a ação.

Exemplo: substituir temporariamente uma função automática de detecção/atuação por vigia humana, ronda com explosímetro portátil ou abertura manual de equipamentos de combate a incêndio só pode ser considerado compensação válida se houver demonstração formal de que a resposta é tempestiva e executável.

### 3.3 APR ou HAZID isolados podem ser insuficientes

A nota técnica da ANP chama atenção para o uso desordenado de análises preliminares para contingenciar degradações. Em indisponibilidades relevantes do F&G, uma avaliação simplificada pode não capturar adequadamente:

- acúmulo de restrições simultâneas;
- perda de independência entre barreiras;
- efeito de atrasos humanos;
- exposição de pessoal em áreas ocupadas;
- interações com outras mudanças temporárias em curso.

_Fontes da seção_: ["anp-21b016bb482410ebc1a9261e:p7-8:159.0-109.0"]

## 4. Falhas recorrentes e inibições repetidas como indicador de desvio de projeto

Um dos pontos mais fortes do material fornecido é que a repetição de permissões, bypasses e inibições pode indicar que a instalação **não está mais operando dentro das premissas originais de projeto**.

No caso investigado pela ANP, a equipe de bordo utilizava quase diariamente os vents do sistema de gás inerte para despressurizar tanques, e essa atividade exigia a **inibição dos detectores de gás do topside próximos aos vents**. A prática recorrente aparecia nos registros de bypass, mas não foi tratada como evidência de mudança dos parâmetros de projeto. Em outro momento, durante o aquecimento do tanque 6C para evaporar condensado, os vapores eram ventilados diariamente pelo vent riser durante o turno diurno, também com **inibição de detectores de gás no upper deck próximo à saída dos vapores**.

Do ponto de vista de F&G, uma inibição frequente ou quase rotineira deve ser tratada como **sinal de alerta de mais alto nível**, porque pode significar pelo menos uma das seguintes situações:

1. a operação real passou a gerar liberações previstas e recorrentes em local onde o F&G atua corretamente, mas a filosofia operacional não foi revista;
2. o detector está exposto de forma repetitiva a emissões decorrentes de rotina que não existiam ou não eram relevantes no projeto original;
3. a área passou a exigir outra filosofia de detecção, de segregação, de ventilação ou de operação;
4. o processo está sendo mantido com uma restrição crônica de barreira, normalizando a exceção.

Em termos de gestão, o uso repetido de inibições não deve ser encerrado apenas com registro no livro de bypass. Ele deve acionar, conforme o caso:

- análise de falha recorrente;
- revisão da causa do alarme;
- verificação de aderência ao projeto e aos parâmetros operacionais;
- reavaliação de riscos;
- abertura de gerenciamento de mudanças;
- atualização de procedimentos e documentação;
- revalidação das medidas compensatórias.

Os recursos do sistema supervisório citados no material — histórico de alarmes, registro de eventos, tendências e reconhecimento — são úteis justamente para separar: **alarme incômodo**, **alarme verdadeiro decorrente de mudança operacional**, **falha de instrumentação** e **uso inadequado de inibição para viabilizar rotina operacional**.

_Fontes da seção_: ["anp-dabfb60617e4f0ede433578e:p163-165:7.0-22.0", "anp-dabfb60617e4f0ede433578e:p181-183:14.0-15.0", "petroles-004c2afadba7ea17c7dd7908:pNone:2452720.0-2452749.0"]

## 5. Gerenciamento de mudanças (MOC) como mecanismo de preservação da eficácia do F&G

Os relatórios da ANP mostram repetidamente que alterações temporárias ou permanentes feitas sem MOC formal prejudicam a segurança operacional. Para a disciplina de F&G, isso é especialmente importante porque mudanças físicas e operacionais alteram diretamente:

- pontos prováveis de vazamento;
- direção e local de dispersão de vapores;
- frequência esperada de liberações;
- ocupação humana e rotas de fuga expostas;
- necessidade de alarmes, intertravamentos e zonas afetadas;
- premissas de cobertura de detectores e de resposta a emergências.

### 5.1 O que o processo de mudança deveria garantir

Segundo o material da ANP, quando os controles de risco do gerenciamento de mudanças fossem corretamente usados, seria esperado que:

1. a **justificativa** para a alteração fosse registrada;
2. a mudança só fosse implementada após **avaliação dos perigos e do impacto global nas atividades**;
3. procedimentos e documentação afetados fossem **atualizados**;
4. o pessoal impactado recebesse **treinamento e comunicação**;
5. a mudança tivesse **autorização por nível gerencial adequado**.

Esse encadeamento é diretamente aplicável a modificações que afetam F&G, como instalação de linhas temporárias, alteração de vents, mudanças de ventilação, rearranjo de equipamentos, uso de mangueiras, reversão de válvulas, novas rotas de escoamento, aquecimento de inventários voláteis ou qualquer condição que desloque o cenário de liberação em relação ao previsto no projeto.

### 5.2 Mudanças "temporárias" podem se consolidar e exigir revisão formal

No caso investigado, práticas inicialmente temporárias se consolidaram ao longo do tempo. Esse é um ponto crítico para F&G: o fato de uma modificação ser apresentada como provisória **não reduz** a necessidade de análise; ao contrário, mudanças temporárias frequentemente criam geometria de risco mais instável, com mangueiras, conexões não usuais, equipamentos portáteis e procedimentos operacionais excepcionais.

### 5.3 Exemplos operacionais que, em contexto de F&G, são gatilhos inequívocos para MOC

O material traz exemplos de alterações e arranjos operacionais que ocorreram sem avaliação prévia adequada dos perigos e do impacto global:

- uso temporário de linha de secagem de gás inerte para transferência de condensado;
- instalação de bombas submersíveis portáteis, válvulas manuais, raquetes e mangueiras flexíveis;
- inversão de válvula de retenção, alterando sentido de fluxo da linha temporária;
- alinhamentos não previstos originalmente, com novas conexões e isolamentos;
- aquecimento de tanque para volatilizar condensado, com vent aberto e detectores inibidos.

Em uma instalação com F&G, mudanças dessa natureza tendem a afetar o estudo de perigos de fogo e gás, a base de posicionamento dos detectores e as condições de uso de inibições. Portanto, não devem ser tratadas como mero expediente operacional.

_Fontes da seção_: ["anp-dabfb60617e4f0ede433578e:p164-167:14.0-11.0", "anp-dabfb60617e4f0ede433578e:p172-176:13.0-13.0", "anp-dabfb60617e4f0ede433578e:p120-122:8.0-27.0", "anp-dabfb60617e4f0ede433578e:p181-183:14.0-15.0"]

## 6. Revisão de estudos de segurança e revalidação do F&G após mudanças ou degradação

O relatório da ANP registra que, no caso analisado, os estudos de segurança elaborados no projeto não refletiram a condição operacional efetiva posteriormente adotada, e que o procedimento do operador previa atualização dos estudos entre projeto e operação, além de revisão periódica e em caso de mudança significativa. O mesmo procedimento citado pela ANP indicava que mudanças com impacto deveriam gerar revisão do Safety Case e de estudos complementares.

Também foram apresentados exemplos de alterações que deveriam disparar revisão, incluindo:

- mudanças de projeto e de parâmetros operacionais de estrutura e processo;
- manutenção, inspeção e experiência proveniente de testes de elementos críticos de segurança (SCEs);
- modificações na instalação, inclusive nos próprios SCEs.

Aplicado ao F&G, isso significa que **não basta restaurar o detector** após uma falha recorrente ou encerrar a PT após uma inibição. Dependendo do padrão observado, é necessário revisar a base técnica do sistema, por exemplo:

- se o alarme recorrente decorre de condição operacional que passou a ser frequente;
- se a indisponibilidade de detectores se tornou parte da rotina para viabilizar a operação;
- se houve alteração física ou funcional da instalação que muda a geometria de dispersão, a ventilação, a ocupação ou as rotas de propagação de fogo/gás;
- se testes, inspeções ou manutenção revelaram desempenho inadequado de elemento crítico relacionado.

Em termos práticos, a revisão por mudança deve responder não apenas "o detector voltou a funcionar?", mas também "a filosofia de detecção continua válida para a instalação real?".

_Fontes da seção_: ["anp-dabfb60617e4f0ede433578e:p164-167:14.0-11.0", "anp-dabfb60617e4f0ede433578e:p163-165:7.0-22.0"]

## 7. Documentação controlada e rastreabilidade: requisito para resposta segura à emergência

O material da ANP mostra um caso em que uma raquete permaneceu instalada por longo período sem ser corretamente transcrita para o controle de isolamento de longo prazo e sem atualização do P&ID para refletir a configuração física real. Durante a emergência, foi usado um desenho sem as marcações correspondentes, o que prejudicou o entendimento do ponto real de vazamento.

A lição técnica para F&G é direta: qualquer alteração que mude a configuração física relevante para segurança deve aparecer de forma controlada na documentação utilizada para operação e resposta a emergências. No contexto de F&G, isso abrange, conforme aplicável:

- listas de bypass e inibições vigentes;
- registros de indisponibilidade de detectores e funções associadas;
- documentação de causa e efeito;
- mapas de detectores e zonas afetadas por mudanças físicas;
- procedimentos temporários válidos durante a degradação;
- registros de restauração e encerramento da condição anormal.

Sem essa rastreabilidade, a instalação corre dois riscos simultâneos:

1. operar com perda de barreira sem plena consciência da extensão da degradação;
2. responder a uma emergência com informação incompatível com a configuração real.

O procedimento citado pela ANP também destacava a necessidade de manter registros atualizados, com cópia eletrônica e impressa sob controle, e realizar verificações periódicas de isolamentos de longo prazo. Para F&G, o princípio equivalente é que a informação de indisponibilidade não pode ficar dispersa em anotações informais ou apenas em memória operacional.

_Fontes da seção_: ["anp-dabfb60617e4f0ede433578e:p180-182:12.0-14.0"]

## 8. Critérios práticos de decisão para o tratamento de bypasses e falhas em F&G

Com base nos materiais fornecidos, podem ser extraídos critérios práticos de boa gestão para esta faceta:

### 8.1 Inibição pontual e planejada

Pode ser admissível apenas como condição excepcional, com:

- análise de risco específica;
- autorização por nível apropriado;
- prazo definido e controle de restauração;
- registro formal em sistema/livro apropriado;
- compensações proporcionais ao risco;
- verificação de que a operação permanece em condição aceitável.

### 8.2 Inibição recorrente ou quase rotineira

Não deve ser normalizada. Deve ser tratada como gatilho para:

- investigação de causa;
- revisão do processo/arranjo operacional;
- revisão de risco e de estudos de segurança, se aplicável;
- abertura de MOC;
- reavaliação da filosofia de detecção, alarmes e resposta.

### 8.3 Detector ou função de F&G degradados com compensação humana

Só é defensável quando a compensação procedimental for formal, treinada, temporalmente viável e dotada de recursos humanos suficientes. Se isso não puder ser demonstrado, a tendência correta é restringir ou interromper a operação afetada.

### 8.4 Falhas recorrentes, testes não executados ou verificação insuficiente

Devem ser entendidos como problema de disponibilidade e confiabilidade de elemento crítico, e não apenas pendência de manutenção. A gestão deve integrar manutenção, operação, engenharia, risco e documentação.

### 8.5 Modificação operacional ou física da instalação

Toda mudança que altere cenários de liberação, venting, isolamento, fluxo, inventário, ocupação ou arranjo físico deve ser avaliada pelo seu impacto no F&G antes da implementação e refletida na documentação controlada após a implementação.

_Fontes da seção_: ["anp-21b016bb482410ebc1a9261e:p7-8:159.0-109.0", "anp-dabfb60617e4f0ede433578e:p163-165:7.0-22.0", "anp-dabfb60617e4f0ede433578e:p164-167:14.0-11.0", "anp-dabfb60617e4f0ede433578e:p180-182:12.0-14.0", "petroles-004c2afadba7ea17c7dd7908:pNone:2452720.0-2452749.0"]

## 9. Síntese técnica

A eficácia do F&G não é preservada apenas por escolha correta de detectores ou por calibração periódica. Ela depende de um ciclo disciplinado de **disponibilidade, registro, análise de recorrência, contingência robusta e revisão por mudanças**. O material fornecido sugere a seguinte leitura profissional:

- **bypass, override e inibição** são exceções formais, não ferramentas de rotina;
- **repetição de inibições** é indício de desvio entre operação real e base de projeto;
- **mudanças temporárias** também exigem MOC e podem alterar substancialmente o risco de fogo e gás;
- **documentação desatualizada** degrada a resposta à emergência;
- **contingência frágil** para elemento crítico degradado não sustenta continuidade operacional segura.

Para fins de projeto, comissionamento, operação e troubleshooting de F&G em FPSOs, a questão-chave passa a ser: **a instalação continua com capacidade demonstrável de detectar e reagir a cenários perigosos, mesmo durante a anormalidade?** Se a resposta depender de premissas não registradas, inibições frequentes, documentos desatualizados ou ações humanas não validadas, a eficácia da detecção está comprometida e a condição precisa ser revista formalmente.

_Fontes da seção_: ["anp-21b016bb482410ebc1a9261e:p7-8:159.0-109.0", "anp-dabfb60617e4f0ede433578e:p163-165:7.0-22.0", "anp-dabfb60617e4f0ede433578e:p164-167:14.0-11.0", "anp-dabfb60617e4f0ede433578e:p180-182:12.0-14.0", "anp-dabfb60617e4f0ede433578e:p181-183:14.0-15.0", "petroles-004c2afadba7ea17c7dd7908:pNone:2452720.0-2452749.0"]