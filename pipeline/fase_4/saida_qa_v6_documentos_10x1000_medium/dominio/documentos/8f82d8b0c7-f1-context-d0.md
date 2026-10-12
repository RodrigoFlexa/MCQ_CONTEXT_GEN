# Acesso e identidades em sistemas digitais de FPSOs/FSOs

## 1. Contexto técnico da faceta
O material fornecido não apresenta um regulamento prescritivo completo sobre autenticação, perfis, privilégios, acesso remoto, MFA, bastion hosts, PAM, DMZ ou segmentação OT/IT. Ainda assim, ele permite construir uma base técnica consistente para a faceta **acesso e identidades** sob a ótica da **segurança operacional** e da **integridade dos sistemas automatizados**.

Os trechos indicam quatro eixos aplicáveis ao tema:

1. **Digitalização e cibersegurança em sistemas automatizados**: o IRF trata a digitalização como um desafio de redução de riscos em sistemas com alto nível de automação, inclusive quando há uso de IA/machine learning, com discussão explícita sobre **boas práticas de coleta de dados**, **segurança cibernética** e **projeto centrado no ser humano**. [Fontes: `anp-b2cfa8a9492ef598716e9685:p30-32:0.0-13.0`, `anp-260456cfa598f9103676bffc:p21-23:10.0-36.0`]
2. **Gestão de mudanças, documentação, treinamento e procedimentos**: alertas de segurança da ANP mostram que falhas nesses elementos removem salvaguardas, criam responsabilidades indefinidas e degradam o controle operacional. [Fonte: `anp-13a33bb67429b09d3272c53e:p1-4:0.0-0.0`]
3. **Controle de contratadas e monitoramento de operação**: o regulamento técnico de sistemas submarinos enfatiza critérios formais para seleção e avaliação de contratadas, revisão documental, classificação de procedimentos críticos, gestão de mudanças e monitoramento por alarmes/tendências, inclusive com medidas compensatórias quando não há supervisório. [Fonte: `anp-2e1d17d32fb37a1c34f1eeef:p3-5:41.0-14.0`]
4. **Investigação e aprendizado com incidentes**: o material destaca investigações mais rigorosas, causas-raiz, fatores contribuintes, fatores humanos, priorização de quase-acidentes e aplicação sistemática das lições aprendidas. Isso é diretamente útil para eventos ligados a credenciais, acessos indevidos, mudanças não autorizadas e sessões remotas mal controladas. [Fonte: `anp-260456cfa598f9103676bffc:p21-23:10.0-36.0`]

Em termos práticos, a faceta de acesso e identidades pode ser tratada como um problema de **controle de risco operacional em sistemas digitais críticos**, e não apenas como administração de usuários.

---

## 2. Por que acesso e identidades são tema de integridade operacional
Nos ambientes digitais de FPSOs/FSOs, o acesso de pessoas internas, fornecedores e contratadas pode afetar diretamente:

- parâmetros operacionais;
- lógicas de controle e de proteção;
- procedimentos executados por sistemas automatizados;
- monitoramento de variáveis e alarmes;
- disponibilidade de funções essenciais.

Os alertas da ANP mostram um ponto central: **quando há mudança sem avaliação adequada, documentação inconsistente, treinamento insuficiente, procedimentos incompletos e responsabilidades indefinidas, as salvaguardas podem ser enfraquecidas ou removidas**. Embora os casos citados não sejam incidentes cibernéticos, a mesma lógica vale para:

- habilitação de acessos remotos;
- alteração de privilégios de engenharia/operação/manutenção;
- uso de contas compartilhadas;
- conexões temporárias de terceiros;
- mudanças em estações de engenharia, servidores supervisórios ou sistemas automatizados.

No alerta de offloading, a ANP relaciona o evento a falhas de **gestão de mudança**, **atualização de HAZOP**, **divulgação de orientação corporativa**, **indefinição de responsabilidade**, **falhas de documentos do fornecedor**, **lacunas de procedimento** e **treinamento insuficiente**. Transposto para a faceta de acesso e identidades, isso significa que permissões e conexões não devem ser tratadas como simples ajustes administrativos; elas podem alterar a exposição ao risco da instalação. [Fonte: `anp-13a33bb67429b09d3272c53e:p1-4:0.0-0.0`]

---

## 3. Princípios de projeto e implantação aplicáveis a acesso e identidades

### 3.1 Acesso deve ser concebido como parte do projeto seguro do sistema automatizado
O material do IRF associa digitalização à **redução de riscos de sistemas automatizados** com uma abordagem de **design centrado no ser humano**. Para a faceta de acesso e identidades, isso leva a um princípio importante: o modelo de autenticação e autorização deve ser desenhado de forma compatível com a operação real, as limitações humanas e as condições de uso offshore. [Fontes: `anp-b2cfa8a9492ef598716e9685:p30-32:0.0-13.0`, `anp-260456cfa598f9103676bffc:p21-23:10.0-36.0`]

Implicações técnicas coerentes com os trechos:

- perfis de acesso devem refletir tarefas reais e responsabilidades definidas;
- privilégios que permitam modificar lógica, parâmetros ou configuração crítica exigem governança mais rígida do que acessos apenas de consulta;
- o desenho do acesso não deve depender de memória informal, prática local ou interpretação individual do fornecedor;
- a interface homem-sistema deve reduzir erro operacional, ambiguidade e uso indevido.

### 3.2 Responsabilidades precisam ser explícitas
No caso de offloading, a ANP identificou **indefinição de responsabilidade** na manutenção de um componente crítico. Em sistemas digitais, o mesmo tipo de falha ocorre quando não está claro:

- quem aprova criação de contas;
- quem concede ou revoga privilégios elevados;
- quem valida acesso de fornecedor;
- quem mantém a documentação mestre da configuração de acesso;
- quem responde por credenciais de estações de engenharia e operação.

Sem essa definição, surgem lacunas de controle, contas órfãs, permissões não revisadas e impossibilidade de responsabilização técnica. [Fonte: `anp-13a33bb67429b09d3272c53e:p1-4:0.0-0.0`]

### 3.3 Documentação é parte da barreira de segurança
Os trechos da ANP enfatizam fluxo de emissão/aprovação de documentos, revisão crítica, identificação de alterações e atualização de documentos afetados por mudanças. Para acesso e identidades, isso é particularmente relevante para:

- matriz de perfis e privilégios;
- lista de contas nominativas e contas técnicas;
- registros de autorização de acesso remoto;
- procedimentos de contingência e de revogação emergencial;
- documentação de fornecedores referente a operação, manutenção e limitações de sistemas digitais.

Documentação não revisada ou contraditória foi fator contribuinte em eventos reais. Em ambiente digital crítico, isso pode se traduzir em acessos mantidos por hábito, conexões não rastreadas e uso de procedimentos obsoletos. [Fontes: `anp-13a33bb67429b09d3272c53e:p1-4:0.0-0.0`, `anp-2e1d17d32fb37a1c34f1eeef:p3-5:41.0-14.0`]

---

## 4. Perfis, privilégios e segregação de funções

### 4.1 Perfis devem seguir criticidade operacional
Os trechos normativos não detalham um modelo formal de RBAC, mas sustentam um raciocínio operacional: atividades com maior potencial de afetar a segurança e a integridade exigem **controle mais rigoroso de qualificação, procedimento, documentação e mudança**.

Aplicado à faceta, isso recomenda distinguir pelo menos entre funções como:

- operação/consulta;
- manutenção;
- engenharia/configuração;
- suporte de fornecedor/contratada;
- administração técnica do sistema.

Quanto maior a capacidade de alterar comportamento do sistema, maior deve ser o nível de controle associado à concessão, manutenção e revisão do privilégio. Esse entendimento é coerente com os trechos sobre procedimentos críticos, análise de riscos, gestão de mudanças e necessidade de operar dentro de limites definidos. [Fonte: `anp-2e1d17d32fb37a1c34f1eeef:p3-5:41.0-14.0`]

### 4.2 Procedimentos críticos e acessos críticos devem caminhar juntos
O SGSS citado pela ANP classifica **procedimentos críticos de segurança operacional** como elementos críticos. Em sistemas digitais, isso sustenta o entendimento de que acessos utilizados para executar procedimentos críticos não podem ser administrados de forma informal.

Exemplos de implicação prática:

- um procedimento crítico não deve depender de conta sem titularidade clara;
- mudança de privilégio associada a atividade crítica deve ser tratada como mudança controlada;
- acessos usados para testes, manutenção ou intervenção em sistemas de processo precisam estar vinculados a procedimento aplicável e pessoal capacitado.

### 4.3 Qualificação e treinamento condicionam o privilégio
Os trechos da ANP associam treinamento especializado, reciclagem periódica, capacitação de contratadas e verificação de conformidade com procedimento à execução segura das atividades. Para a faceta de identidades, isso permite concluir que **autorização técnica e autorização de acesso não devem ser dissociadas**.

Em outras palavras, conceder privilégio sem comprovação de treinamento, entendimento do procedimento e ciência das limitações do sistema equivale a criar uma vulnerabilidade organizacional. [Fonte: `anp-13a33bb67429b09d3272c53e:p1-4:0.0-0.0`]

---

## 5. Acesso remoto de equipes internas, fornecedores e contratadas

### 5.1 Acesso remoto é mudança de exposição ao risco
Os casos analisados pela ANP mostram que mudanças implementadas com urgência, sem revisão suficiente de salvaguardas e documentação, podem remover barreiras e introduzir falhas latentes. O mesmo raciocínio se aplica a:

- abertura de acesso remoto a ambiente OT;
- liberação temporária de fornecedor;
- ampliação de permissões de suporte;
- ativação emergencial de conexão para diagnóstico;
- mudança de método de autenticação ou de estação autorizada.

Se a mudança puder afetar segurança operacional, ela deve ser previamente avaliada quanto a perigos, impactos globais e documentos/procedimentos afetados. [Fontes: `anp-13a33bb67429b09d3272c53e:p1-4:0.0-0.0`, `anp-2e1d17d32fb37a1c34f1eeef:p3-5:41.0-14.0`]

### 5.2 Terceiros precisam de controle proporcional ao risco da atividade
O trecho do SGSS é claro ao exigir critérios para seleção, avaliação de desempenho e obtenção de informações sobre procedimentos, normas e manuais afetos à segurança operacional das contratadas. Para acesso remoto e identidades, isso suporta os seguintes critérios de governança:

- acesso de terceiro não deve ser liberado apenas por necessidade comercial ou conveniência;
- a contratada precisa ter desempenho e procedimentos compatíveis com o risco da atividade;
- deve haver registro das avaliações realizadas;
- mudanças nas práticas da contratada devem ser auditadas ou reavaliadas periodicamente.

Isso é especialmente relevante quando o terceiro acessa ativos com capacidade de alterar configuração, lógica, alarmes, tendências ou disponibilidade do sistema. [Fonte: `anp-2e1d17d32fb37a1c34f1eeef:p3-5:41.0-14.0`]

### 5.3 Acesso remoto sem observabilidade adequada exige medidas compensatórias
O SGSS citado determina que, para variáveis operacionais sem acompanhamento em sistema supervisório, o operador adote **procedimentos de segurança** e **mecanismos de controle e monitoramento** que permitam identificar anormalidades. Aplicado à faceta de acesso remoto, o princípio é:

> se a sessão remota, a ação executada ou o efeito sobre o sistema não puderem ser acompanhados de forma suficiente pelos meios normais, devem existir controles compensatórios que permitam detectar desvios e interromper a condição insegura.

O trecho não especifica a tecnologia, mas o conceito é importante: **não se deve aceitar perda de visibilidade operacional em nome da conveniência do acesso**. [Fonte: `anp-2e1d17d32fb37a1c34f1eeef:p3-5:41.0-14.0`]

---

## 6. Operação, monitoramento e preservação da integridade digital

### 6.1 Operar dentro de limites definidos
O SGSS exige operar dentro do **Envelope de Segurança**, registrar e investigar desvios, estabelecer limites de alarmes e analisar tendências. Embora o trecho trate de sistema submarino, a lógica é valiosa para a integridade digital de sistemas críticos:

- acessos e ações autorizadas devem permanecer dentro de limites operacionais e administrativos previamente definidos;
- desvios de privilégio, uso fora de horário/escopo e alterações fora de procedimento devem ser tratados como anormalidades a investigar;
- somente conceder acesso não basta; é necessário verificar se o uso do acesso se mantém dentro do contexto aprovado.

[Fonte: `anp-2e1d17d32fb37a1c34f1eeef:p3-5:41.0-14.0`]

### 6.2 Monitorar tendência é mais útil do que reagir apenas ao evento final
Os trechos da ANP valorizam monitoramento de variáveis, análise de tendências, investigação de desvios e identificação de fatores contribuintes. Para a faceta em estudo, isso sugere que a gestão de identidades não deve depender apenas da descoberta de um incidente consumado; ela deve observar sinais de deterioração de controle, como:

- recorrência de acessos temporários prorrogados;
- crescimento de exceções operacionais;
- revalidações atrasadas;
- mudanças frequentes em perfis sensíveis;
- fornecedores com necessidade recorrente de ampliação de acesso.

A utilidade técnica desse enfoque está em detectar deterioração organizacional antes que ela se traduza em perda de integridade do sistema. [Fontes: `anp-2e1d17d32fb37a1c34f1eeef:p3-5:41.0-14.0`, `anp-260456cfa598f9103676bffc:p21-23:10.0-36.0`]

### 6.3 Falta de vigilância local ou remota é fragilidade reconhecida
No alerta de offloading, a ANP registrou deficiência de monitoramento na estação e por câmera. A tradução para sistemas digitais é direta: quando a organização permite acessos, intervenções ou mudanças sem vigilância suficiente, a capacidade de detecção precoce se reduz. [Fonte: `anp-13a33bb67429b09d3272c53e:p1-4:0.0-0.0`]

---

## 7. Gestão de mudanças aplicada a identidades e acessos
A ANP relaciona eventos reais à ausência de gestão de mudança, à falta de atualização de análises e à documentação não revisada. Em ambiente digital crítico, devem ser tratados como mudanças potencialmente relevantes para a segurança operacional, por exemplo:

- criação de novo canal de acesso remoto;
- alteração de política de autenticação em sistema crítico;
- inclusão de fornecedor com acesso a sistema automatizado;
- mudança de estação autorizada para engenharia/operação;
- ativação de modo de manutenção que altere salvaguardas ou comportamento de monitoração;
- mudança em procedimento de suporte remoto.

A lógica técnica extraída dos trechos é que a gestão de mudança deve considerar, antes da implementação:

- perigos introduzidos pela mudança;
- impacto global nas atividades;
- atualização de procedimentos, manuais e demais documentos afetados;
- eventual revisão de análise de riscos principal;
- efeitos sobre integridade e sobre o programa de gerenciamento correspondente.

[Fontes: `anp-13a33bb67429b09d3272c53e:p1-4:0.0-0.0`, `anp-2e1d17d32fb37a1c34f1eeef:p3-5:41.0-14.0`]

---

## 8. Resposta a incidentes e aprendizado organizacional
O material da ANP e do IRF enfatiza que a indústria precisa fortalecer:

- investigações rigorosas para identificar causas-raiz e fatores contribuintes;
- priorização de incidentes e quase-acidentes que merecem investigação detalhada;
- inclusão estrutural de fatores humanos;
- compartilhamento mais amplo dos aprendizados;
- definição de ações prioritárias e monitoramento da implementação;
- substituição de cultura de culpabilização por cultura de aprendizado.

Na faceta de acesso e identidades, isso significa que incidentes como uso indevido de credenciais, alteração não autorizada, sessão remota sem rastreabilidade, liberação indevida de fornecedor ou erro humano em conta privilegiada não devem ser tratados só como falha individual. É preciso verificar:

- se o perfil concedido era excessivo para a tarefa;
- se havia procedimento claro e atualizado;
- se o treinamento era suficiente;
- se a contratada havia sido adequadamente avaliada;
- se a mudança havia sido formalmente apreciada;
- se a monitoração existente era apta a detectar o desvio em tempo hábil.

Esse enfoque é consistente com a linha defendida nos relatórios da ANP/IRF para investigação de incidentes e disseminação de lições aprendidas. [Fonte: `anp-260456cfa598f9103676bffc:p21-23:10.0-36.0`]

---

## 9. Critérios práticos de decisão para não expor sistemas operacionais críticos
Com base nos trechos, uma decisão de conceder, ampliar ou manter acesso a sistema digital crítico é tecnicamente mais robusta quando responde positivamente às perguntas abaixo:

1. **A responsabilidade pela autorização, uso e revogação está claramente definida?** [Fonte: `anp-13a33bb67429b09d3272c53e:p1-4:0.0-0.0`]
2. **A atividade do usuário/terceiro está coberta por procedimento claro, específico e controlado?** [Fontes: `anp-13a33bb67429b09d3272c53e:p1-4:0.0-0.0`, `anp-2e1d17d32fb37a1c34f1eeef:p3-5:41.0-14.0`]
3. **A pessoa ou contratada possui qualificação, treinamento e desempenho compatíveis com o risco da atividade?** [Fontes: `anp-13a33bb67429b09d3272c53e:p1-4:0.0-0.0`, `anp-2e1d17d32fb37a1c34f1eeef:p3-5:41.0-14.0`]
4. **A mudança de acesso foi analisada quanto a impacto na segurança operacional e nos documentos afetados?** [Fontes: `anp-13a33bb67429b09d3272c53e:p1-4:0.0-0.0`, `anp-2e1d17d32fb37a1c34f1eeef:p3-5:41.0-14.0`]
5. **Há monitoramento suficiente para identificar anormalidades, desvios e tendências?** [Fonte: `anp-2e1d17d32fb37a1c34f1eeef:p3-5:41.0-14.0`]
6. **Se a observabilidade normal não existir, foram previstas medidas compensatórias?** [Fonte: `anp-2e1d17d32fb37a1c34f1eeef:p3-5:41.0-14.0`]
7. **Existe plano para aprender com desvios, quase-acidentes e falhas de processo, sem restringir a análise à culpa individual?** [Fonte: `anp-260456cfa598f9103676bffc:p21-23:10.0-36.0`]

---

## 10. Síntese técnica
Para esta faceta, o material aponta uma conclusão central: em FPSOs/FSOs, **autenticação, perfis, privilégios e acesso remoto devem ser geridos como barreiras de segurança operacional de sistemas automatizados**, especialmente quando podem afetar comportamento do processo, disponibilidade de funções e resposta a anormalidades.

Mesmo sem detalhar tecnologias específicas de cibersegurança, os trechos sustentam uma base robusta para avaliação profissional de acesso e identidades, centrada em:

- projeto centrado no ser humano;
- controle de mudanças;
- documentação íntegra e revisada;
- treinamento e competência;
- controle de contratadas e terceiros;
- monitoramento de desvios e tendências;
- investigação rigorosa e aplicação de lições aprendidas.

Essa abordagem reduz o risco de expor sistemas operacionais críticos por meio de acessos mal definidos, permissões mal governadas ou conexões remotas insuficientemente controladas.