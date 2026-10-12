# Gestão de mudanças e indisponibilidades em instrumentação, controle e automação

## 1. Contexto técnico da faceta
Em FPSOs, alterações de configuração e indisponibilidades temporárias em sistemas de instrumentação, controle e automação podem degradar camadas de proteção, modificar a resposta operacional e introduzir riscos não previstos no projeto original. Isso é especialmente sensível quando a intervenção atinge funções de controle, alarmes, intertravamentos, SIS, ESD, F&G, redes e elementos de campo que participam direta ou indiretamente da segurança do processo.

O ponto central não é apenas "mudar algo", mas controlar tecnicamente **o que foi mudado, por quê, por quanto tempo, com qual impacto sobre risco, quem autorizou, quais barreiras compensatórias foram adotadas e como a instalação será revalidada e documentada após a mudança**.

**Fontes da seção:** `petroles-004c2afadba7ea17c7dd7908:pNone:3235530.0-3235602.0`, `petroles-004c2afadba7ea17c7dd7908:pNone:3235577.0-3235648.0`, `anp-21b016bb482410ebc1a9261e:p7-8:159.0-109.0`

## 2. O que deve ser tratado como modificação em I&C/A
Na prática de gestão de mudanças, não devem ser tratados como simples manutenção apenas os grandes projetos. O material indica que também podem exigir gestão formal mudanças de pequeno porte quando alteram pressupostos de projeto, funcionamento, proteção, operação ou manutenção.

### 2.1 Alterações tipicamente enquadráveis como modificação
Entre as mudanças relevantes para instrumentação, controle e automação, destacam-se:

- alterações em **setpoints** de instrumentos, alarmes e intertravamentos;
- mudanças em **malhas de controle**, lógica, permissivos e intertravamentos;
- introdução de **bypasses** em equipamentos e seus intertravamentos;
- **jumpeamento** de circuitos e malhas de intertravamento;
- alterações em variáveis de processo que escapem às condições originais de projeto, como pressão, temperatura, vazão e nível;
- mudanças em equipamentos, inclusão de novos equipamentos ou modificação dos existentes com impacto em controle/proteção;
- revisões de procedimentos de operação, partida, parada e parada de emergência;
- uso de **equipamentos elétricos temporários** e conexões provisórias;
- tubulações, conexões, mangueiras e utilidades temporárias que modifiquem a configuração funcional da planta;
- mudanças na força de trabalho e na competência disponível para operar ou manter os sistemas.

O ponto relevante é que **uma alteração pequena em aparência pode ser grande em consequência**, por exemplo: alteração de setpoint de alarme, supressão temporária de um detector, forcing de uma saída, bypass de um iniciador de ESD, inversão de lógica ou instalação de arranjo temporário que mude fluxo, causa e efeito ou condição de disparo.

### 2.2 Manutenção normal x modificação
Um critério técnico útil é distinguir:

- **manutenção normal**: reposição equivalente, sem alterar função, arquitetura, filosofia, parâmetros aprovados, desempenho esperado ou interfaces;
- **modificação temporária**: mudança com duração definida para contingência, teste, reparo ou condição operacional excepcional;
- **modificação permanente**: alteração incorporada ao arranjo ou à configuração normal da instalação.

A literatura compilada alerta que empresas costumam tratar adequadamente grandes projetos, mas podem deixar mudanças menores acontecerem "a título de manutenção". Isso é particularmente perigoso quando a alteração recai sobre lógica, alarmes, intertravamentos, setpoints, conexões temporárias ou recursos provisórios.

**Fontes da seção:** `petroles-004c2afadba7ea17c7dd7908:pNone:3235530.0-3235602.0`, `petroles-004c2afadba7ea17c7dd7908:pNone:3235577.0-3235648.0`

## 3. Termos operacionais importantes: bypass, override, inibição e reconhecimento
Para gestão segura de indisponibilidades, convém separar conceitos que frequentemente são confundidos na operação.

### 3.1 Bypass
No material, bypass aparece como a retirada controlada de um ponto de entrada ou de uma função do caminho normal de atuação, inclusive em inicializadores de ESD, devendo ser usado apenas em situações excepcionais, sob procedimento específico e análise de riscos. Em termos práticos, o bypass reduz ou remove a participação de um sinal, equipamento ou função de proteção na lógica normal de decisão.

### 3.2 Override
O material também descreve override como o **forçamento de uma saída** para que um atuador permaneça ativado ou desativado independentemente da lógica normal. Isso é mais invasivo que apenas reconhecer um alarme, porque atua diretamente sobre o estado comandado ao elemento final ou à função de controle/proteção.

### 3.3 Inibição
A inibição é apresentada como forma controlada e temporária de **desabilitar a anunciação do alarme** por ação manual. Em sistemas reais, a nomenclatura pode variar e, em alguns casos, a inibição pode afetar não só a anunciação, mas também a forma de tratamento do sinal pelo sistema; por isso, deve-se verificar a definição local do fabricante e da filosofia de automação/alarmes.

### 3.4 Reconhecimento de alarme
Reconhecer alarme significa informar que o operador tomou ciência da condição, silenciar a anunciação sonora e prosseguir com a resposta operacional. **Reconhecimento não equivale a inibição, bypass ou override**. O alarme continua válido e a causa continua existindo até normalização.

### 3.5 Consequência prática
Essas distinções importam porque os controles administrativos, as aprovações e o impacto sobre o risco não são equivalentes:

- reconhecer um alarme é rotina operacional;
- inibir um alarme já exige controle específico;
- fazer bypass de entrada/função de segurança é mais crítico;
- fazer override de saída/atuador pode alterar diretamente a resposta de segurança ou controle.

**Fontes da seção:** `petroles-004c2afadba7ea17c7dd7908:pNone:2452720.0-2452749.0`

## 4. Conteúdo mínimo de um processo de Gestão de Mudanças (MOC)
Um processo robusto de MOC para automação e instrumentação precisa ser formal, compreensível pelos usuários e aplicável tanto a mudanças grandes quanto pequenas. A estrutura abaixo consolida os elementos recorrentes do material.

### 4.1 Identificação e classificação da mudança
O processo deve exigir, antes da implementação:

- descrição da modificação e sua justificativa;
- classificação da mudança quanto a tecnologia, instalação/campo e força de trabalho;
- distinção explícita entre manutenção normal e modificação;
- identificação de se a mudança é temporária ou permanente;
- definição da duração permitida, quando temporária.

### 4.2 Documentação técnica de base
A análise deve considerar, conforme aplicável:

- bases de projeto de processo e mecânico;
- fluxogramas, P&IDs, descrição de processo e causa e efeito;
- limites máximos e mínimos de operação;
- balanços de material e energia, quando a mudança afetar o processo;
- manuais, desenhos e padrões operacionais;
- documentação de controle, alarmes, intertravamentos e SIS/ESD.

### 4.3 Avaliação de riscos
A mudança deve ser examinada quanto a segurança, saúde ocupacional e meio ambiente, inclusive efeitos a montante e a jusante. O material menciona uso de ferramentas como APR, HAZOP e FMEA. Para mudanças que afetem SIS, o guia HSE acrescenta a necessidade de **análise de impacto na segurança funcional**, verificando se a mudança compromete a integridade alcançada da SIF.

### 4.4 Aprovações e responsabilidades
O padrão deve definir:

- quem solicita;
- quem analisa tecnicamente;
- quem aprova por nível hierárquico;
- quem implementa;
- quem valida e encerra.

Isso é coerente com a indicação de que funções críticas, como bypass e override, só devem ocorrer com autorização de níveis superiores e após análise dos riscos envolvidos.

### 4.5 Comunicação e treinamento
As mudanças e seus impactos precisam ser divulgados ao pessoal envolvido. Quando a mudança altera operação, manutenção, lotação, competência ou resposta a alarmes/intertravamentos, o processo deve prever treinamento e atualização da força de trabalho.

### 4.6 Implementação controlada
A execução deve obedecer ao projeto aprovado e aos critérios de QA/QC. Quando houver montagem, ligação, parametrização ou programação, a alteração precisa ser executada de forma rastreável, sem improvisos de campo fora da documentação aprovada.

### 4.7 Fechamento, atualização documental e aprendizado
Após a implementação, devem ser atualizados desenhos, procedimentos, padrões e registros da mudança. Mudanças temporárias precisam de mecanismo formal de vencimento, revisão e remoção; se permanecerem além do previsto, devem ser reavaliadas.

**Fontes da seção:** `petroles-004c2afadba7ea17c7dd7908:pNone:3235530.0-3235602.0`, `petroles-004c2afadba7ea17c7dd7908:pNone:3235577.0-3235648.0`, `petroles-004c2afadba7ea17c7dd7908:pNone:2452720.0-2452749.0`, `hse-5a060e67d97d7bb15290d26c:p30-34:20.0-1.0`

## 5. Gestão segura de bypasses, overrides e inibições temporárias
Essa é a parte mais crítica da faceta, pois a indisponibilidade temporária frequentemente incide sobre elementos críticos e camadas de proteção.

### 5.1 Quando são admissíveis
Os trechos convergem para que bypasses, overrides e inibições sejam tratados como **medidas excepcionais**, não como rotina operacional. Seu uso demanda:

- procedimento definido;
- circunstâncias permitidas claramente delimitadas;
- aprovação por papéis designados;
- registro formal;
- prazo ou duração permitida;
- monitoramento ativo;
- auditoria do processo.

### 5.2 O que deve ser registrado
Um registro mínimo deve conter, ao menos:

- identificação exata do ponto, função, laço, alarme ou atuador afetado;
- tipo de indisponibilidade: bypass, override, inibição, falha, teste não executado etc.;
- motivo e condição operacional associada;
- avaliação de risco adotada;
- barreiras compensatórias requeridas;
- data/hora de aplicação;
- responsável pela autorização e responsável pela remoção;
- prazo máximo autorizado;
- confirmação de retorno à condição normal.

### 5.3 Risco cumulativo
O guia HSE chama atenção para o **risco cumulativo** quando mais de um componente do SIS está em override. Em FPSOs, esse raciocínio também é útil para combinações de indisponibilidades em ESD, F&G e malhas críticas: a soma de pequenas dispensas pode retirar a efetividade global da barreira.

### 5.4 Duração e escalonamento
Overrides e inibições de curta duração, vinculados a atividade específica e sob monitoramento dedicado, não devem ser tratados do mesmo modo que degradações prolongadas. Quando a indisponibilidade se estende, o material aponta necessidade de avaliação adicional, potencialmente mais robusta do que uma APR isolada.

### 5.5 Medidas compensatórias
Segundo a Nota Técnica da ANP, o operador deve possuir procedimento de contingenciamento robusto para falha, degradação ou indisponibilidade de elemento crítico, inclusive em situações de bypass, override, inibição ou falha de teste/verificação. As contingências devem ser suficientes para manter os riscos em níveis aceitáveis e podem exigir:

- reforço de monitoração operacional;
- restrições de processo e redução de envelope operacional;
- patrulhamento local ou monitoração suplementar;
- adoção de barreiras procedimentais formalizadas;
- parada de equipamentos, sistemas ou da planta, se necessário.

### 5.6 Barreira procedimental não pode ser informal
Quando a compensação depender de ação humana, o material da ANP ressalta que isso só é aceitável com rigor compatível com a criticidade, incluindo:

- formalização em procedimento crítico específico;
- evidência de treinamento prático;
- verificação de mão de obra mínima necessária;
- análise temporal para confirmar que a resposta humana cabe no tempo disponível;
- avaliação das interfaces homem-máquina e das condições reais de execução.

### 5.7 Controle de acesso
O sistema supervisório e de controle deve trabalhar com categorias de usuários e níveis de acesso distintos. Funções de bypass e override não devem ficar liberadas indistintamente ao operador de rotina. O material destaca autorização hierárquica superior para comandos mais críticos.

**Fontes da seção:** `petroles-004c2afadba7ea17c7dd7908:pNone:2452720.0-2452749.0`, `anp-21b016bb482410ebc1a9261e:p7-8:159.0-109.0`, `hse-5a060e67d97d7bb15290d26c:p30-34:20.0-1.0`

## 6. Mudanças de configuração em SIS, ESD, PLC e DCS
Mudanças lógicas e paramétricas em sistemas de automação são especialmente sensíveis porque podem alterar a função sem alteração física visível de campo.

### 6.1 Exemplos típicos de mudanças de configuração sensíveis
- alteração de setpoint de alarme ou trip;
- mudança de ganhos ou parâmetros de controlador;
- modificação de permissivos e intertravamentos;
- mudança de votação em SIF ou lógica de disparo;
- redefinição de prioridades/grupos de alarme;
- parametrização que afete modo de operação seguro de instrumento ou cartão;
- forcing, bypass ou desabilitação de pontos de entrada/saída;
- mudança em valores de referência usados em cálculos, correções ou totalizações.

### 6.2 Requisitos adicionais para SIS
Quando a mudança afeta SIS, o material do HSE indica que o MOC deve exigir, conforme aplicável:

- análise de impacto para verificar efeito sobre a integridade alcançada da SIF;
- revisão da fase de identificação de perigos e avaliação de riscos, caso a mudança introduza ou altere perigos;
- revisão de estudos de alocação SIL quando premissas originais forem afetadas;
- atualização do SRS, se necessário;
- revisão do cálculo de verificação SIL, quando a mudança afetar hipóteses de projeto;
- consideração de uma nova avaliação funcional de segurança antes da reintrodução dos perigos;
- plano de validação e estratégia de testes para revalidar a função após a modificação;
- validação, registro e retenção de backups eletrônicos das mudanças de configuração.

### 6.3 Competência técnica e risco de erro sistemático
O mesmo guia ressalta que fabricantes podem exigir configuração específica para que instrumentos ou lógicas operem no modo SIL. Configuração incorreta pode desabilitar diagnósticos, reduzir detecção de falhas e degradar a confiabilidade esperada. Portanto, mudanças em software, parametrização e firmware exigem pessoal treinado ou suporte especializado.

### 6.4 Testes pós-modificação
Não basta "carregar a lógica" ou "mudar o setpoint". A alteração precisa ser revalidada por meio de testes coerentes com a função alterada: teste funcional, verificação de malha, causa e efeito, proof test parcial/completo ou combinação aplicável ao caso. O objetivo é confirmar que a função continua atuando conforme a especificação vigente.

**Fontes da seção:** `petroles-004c2afadba7ea17c7dd7908:pNone:2452720.0-2452749.0`, `hse-5a060e67d97d7bb15290d26c:p30-34:20.0-1.0`, `petroles-004c2afadba7ea17c7dd7908:pNone:3235530.0-3235602.0`

## 7. Desenhos, registros e rastreabilidade da configuração real
Mudança segura depende de que a documentação reflita a condição física e lógica real da instalação. O relatório da ANP mostra que falhas de registro e de atualização documental prejudicam tanto a operação normal quanto a resposta a emergências.

### 7.1 Atualização de P&ID e registros de isolamento
Quando houver isolamento de linha de processo, instalação de raquete, alteração temporária de arranjo ou outra condição persistente, o P&ID e os registros de isolamento de longo prazo devem refletir fielmente a configuração vigente. O material menciona, inclusive, marcação do desenho e posterior correção as-built.

### 7.2 Consequência da documentação desatualizada
O caso investigado pela ANP mostrou que uma raquete permaneceu instalada por longo período sem refletir-se adequadamente no controle de isolamentos de longo prazo nem no P&ID usado durante a emergência. Isso gerou dúvida sobre o real ponto de vazamento e prejudicou o entendimento da situação.

### 7.3 Aplicação à automação
Por analogia técnica dentro do escopo de automação, a mesma disciplina deve valer para:

- listas de bypass/inibição ativas;
- matriz de causa e efeito;
- listas de I/O e mapeamentos de sinais;
- narrativas de controle;
- filosofia de alarmes;
- backups de controladores/servidores/estações;
- registros de versão e histórico de mudanças.

Sem isso, a instalação pode operar com uma configuração real diferente da configuração documental, o que aumenta o risco de erro humano, diagnóstico incorreto e decisão inadequada em contingência.

**Fontes da seção:** `anp-dabfb60617e4f0ede433578e:p180-182:12.0-14.0`, `hse-5a060e67d97d7bb15290d26c:p30-34:20.0-1.0`

## 8. Quando uma mudança temporária deixa de ser "temporária"
Um ponto crítico dos casos investigados é a tendência de arranjos ou práticas excepcionais se normalizarem sem reabertura formal do MOC.

O relatório da ANP descreve situação em que uma condição entendida como temporária acabou se consolidando por longo período operacional, sem evidência adequada de reavaliação formal de riscos. Também foram observadas práticas frequentes de despressurização/venting com inibição de detectores de gás próximos aos vents, sem que a recorrência dessa condição tivesse sido tratada como indicação de alteração relevante nos parâmetros e premissas do projeto.

A lição técnica é direta: **recorrência, longa duração ou repetição de contingência indicam que a instalação pode já não estar mais em mero desvio temporário, mas em nova condição operacional que exige revisão formal das bases de projeto, dos riscos e das salvaguardas.**

**Fontes da seção:** `anp-dabfb60617e4f0ede433578e:p163-165:7.0-22.0`, `anp-21b016bb482410ebc1a9261e:p7-8:159.0-109.0`

## 9. Situações de atenção elevada para a equipe de automação
A equipe deve elevar o nível de exigência de MOC e de gestão de indisponibilidades quando ocorrer qualquer uma das condições abaixo:

- alteração em setpoint de alarme, trip, permissivo ou controlador fora do rito normal aprovado;
- bypass ou override em SIS, ESD, F&G ou malha crítica;
- inibição de detectores de gás/fogo para viabilizar atividade operacional ou de manutenção;
- falha de prova, inspeção ou verificação de elemento crítico sem contingência formal pronta;
- indisponibilidade simultânea de mais de um componente relevante da mesma barreira;
- uso de forcing, jumpeamento ou ligação provisória em campo ou em I/O;
- mudança temporária que ultrapassa o prazo inicial ou se repete com frequência;
- divergência entre estado real do sistema e desenhos/listas/causa e efeito/backups oficiais;
- necessidade de depender de ação humana como única compensação para perda de função automática.

**Fontes da seção:** `petroles-004c2afadba7ea17c7dd7908:pNone:3235530.0-3235602.0`, `petroles-004c2afadba7ea17c7dd7908:pNone:2452720.0-2452749.0`, `anp-21b016bb482410ebc1a9261e:p7-8:159.0-109.0`, `hse-5a060e67d97d7bb15290d26c:p30-34:20.0-1.0`

## 10. Critérios práticos de decisão
Antes de aprovar uma alteração de configuração ou manter um bypass/inibição ativo, perguntas técnicas úteis são:

1. A mudança altera a função de medir, controlar, alarmar, intertravar, desligar ou detectar?
2. Trata-se realmente de reposição equivalente ou há mudança de função, parâmetro, lógica, modo de falha ou desempenho?
3. Existe impacto a montante/jusante ou em outras barreiras da instalação?
4. A condição é temporária com prazo definido ou está se tornando recorrente/permanente?
5. Há avaliação de risco compatível com a criticidade e a duração da indisponibilidade?
6. As medidas compensatórias são reais, treinadas, executáveis no tempo disponível e auditáveis?
7. A continuidade operacional permanece justificável ou a situação exige redução de operação/parada?
8. Desenhos, listas, registros, backups e versões serão atualizados antes do encerramento?
9. Após a mudança, que testes/validações provarão que a função continua conforme especificação?

Se essas respostas não estiverem claramente demonstradas, a tendência correta é **não normalizar o desvio**, mas reavaliar a mudança e, se necessário, restringir ou interromper a operação.

**Fontes da seção:** `petroles-004c2afadba7ea17c7dd7908:pNone:3235577.0-3235648.0`, `anp-21b016bb482410ebc1a9261e:p7-8:159.0-109.0`, `hse-5a060e67d97d7bb15290d26c:p30-34:20.0-1.0`, `anp-dabfb60617e4f0ede433578e:p163-165:7.0-22.0`, `anp-dabfb60617e4f0ede433578e:p180-182:12.0-14.0`