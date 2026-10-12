# Sistema de gás inerte

## 1. Finalidade e princípio de segurança
**Fontes:** `hse-04d3623c0070fad00a0b82db:p52-54:45.0-30.0`, `hse-84ee4101a6ca194620d4089b:p106-109:38.0-5.0`

Em FPSOs, os tanques de carga e slop tanks permanecem com frequência parcialmente cheios durante produção, armazenamento e offloading. Nessa condição, o espaço livre acima do líquido precisa ser mantido em condição não inflamável. O papel do sistema de gás inerte (IG) é impedir a formação de mistura inflamável no espaço de vapor, principalmente por dois mecanismos combinados:

- **redução do teor de oxigênio** da atmosfera do tanque;
- **manutenção de pressão positiva** no tanque para evitar ingresso de ar.

Nos trechos utilizados, são citados os seguintes referenciais operacionais:

- o gás inerte entregue aos tanques é **geralmente tratado para teor de O₂ de 5% v/v ou menos**;
- a atmosfera no espaço de vapor do tanque deve ser mantida com **no máximo 8% v/v de O₂**;
- embora **11% de O₂** seja citado como valor “comumente reconhecido” abaixo do qual a combustão não se sustenta, a referência operacional mencionada é **8% v/v**.

Em termos práticos, o sistema deve manter os tanques com **pressão positiva em praticamente todo o tempo**, exceto quando o tanque estiver sendo **gas freed para entrada**. Isso é particularmente importante em FPSO porque as operações de carga interna, armazenamento e descarga ocorrem com alta frequência, e a taxa de transferência de óleo altera continuamente a necessidade de reposição de gás e de ventilação.

## 2. Arranjo típico e elementos funcionais
**Fontes:** `hse-04d3623c0070fad00a0b82db:p52-54:45.0-30.0`, `hse-84ee4101a6ca194620d4089b:p106-109:38.0-5.0`, `hse-84ee4101a6ca194620d4089b:p108-110:10.0-19.0`

Os trechos descrevem um sistema de IG relativamente extenso e com forte interface com o sistema de ventilação dos tanques. Elementos citados:

- **gerador de gás inerte**, comumente queimando diesel em FPSO;
- **scrubber**/tratamento do gás antes do envio aos tanques;
- **blowers** de IG;
- **rede de tubulações** de distribuição até os tanques;
- **deck seal**/selo d’água como barreira contra retorno de vapores;
- **dispositivos de não-retorno**, sendo requerido pelo menos dois sistemas;
- **válvulas de isolamento e/ou blanks**;
- **válvula reguladora de gás** entre scrubber e tanques;
- **válvulas de pressão/vácuo (P/V)** no sistema de ventilação;
- **emergency pressure/vacuum breaker** para cenário de falha da P/V principal;
- **vent headers** e dispositivos de ventilação de alta velocidade ou livre escoamento.

### 2.1 Requisitos de capacidade e redundância citados
O guia HSE que referencia requisitos SOLAS informa que o sistema deve ser capaz de:

- fornecer vazão de IG de pelo menos **125% v/v da capacidade nominal máxima das bombas de carga**;
- fazer isso com **pelo menos dois blowers**;
- manter pressão positiva no tanque, sendo citada **pressão normal de descarga de 0,12 barg**.

### 2.2 Barreiras contra retorno de vapores
São mencionados **pelo menos dois dispositivos/sistemas de não-retorno** para evitar retrofluxo de vapores de hidrocarbonetos para espaços de máquinas ou equipamentos de convés, incluindo:

1. **water seal/deck seal** localizado no convés principal;
2. outro dispositivo a jusante do selo d’água, que pode ser **mecânico** ou **válvula de isolamento manual**.

Essas barreiras são fundamentais porque o sistema de IG fica conectado a atmosferas contendo hidrocarbonetos e qualquer falha de segregação pode levar vapores inflamáveis de volta ao sistema.

### 2.3 Integração com o sistema de ventilação
É comum que o sistema de ventilação dos tanques de carga esteja **integrado em maior ou menor grau** com o sistema de IG. Isso reduz tubulação, mas pode **restringir operabilidade**, principalmente em situações de:

- isolamento individual de tanque;
- mudança entre modos de operação;
- preparo para entrada em tanque;
- resposta a falha de P/V, deck seal ou IG generator.

Por isso, os tanques individuais precisam poder ser **claramente isolados**.

## 3. Modos operacionais do sistema
**Fontes:** `hse-04d3623c0070fad00a0b82db:p52-54:45.0-30.0`, `hse-04d3623c0070fad00a0b82db:p54-56:31.0-24.0`

### 3.1 Durante offloading/descarga do FPSO
Quando o óleo cru é transferido para navio aliviador, o volume líquido no tanque diminui e o espaço de vapor aumenta. Nessa fase, o sistema de IG deve suprir gás com:

- **vazão suficiente** para acompanhar a retirada de líquido;
- **qualidade adequada** para manter o O₂ do espaço de vapor abaixo de 8% v/v;
- **pressão suficiente** para impedir que ar seja aspirado para dentro do tanque.

Em termos operacionais, essa condição liga diretamente o desempenho do IG à taxa de offloading.

### 3.2 Durante enchimento/carregamento do tanque
Quando o tanque recebe óleo, a atmosfera inertizada acima do líquido é deslocada. Logo, é necessário **ventilar o excesso de atmosfera inertizada** para evitar acúmulo de pressão no tanque.

Ou seja:

- **descarga/offloading** aumenta a demanda de IG para reposição do volume;
- **enchimento** aumenta a demanda sobre o **sistema de ventilação**.

### 3.3 Durante períodos sem carga nem descarga
Quando o cru não está sendo carregado nem descarregado, o sistema de IG é usado para **“top up”** da atmosfera do tanque, isto é, repor perdas e manter a atmosfera em condição segura.

### 3.4 Exceção: gas freeing para entrada
A única exceção explícita à exigência de pressão positiva contínua é quando o tanque está sendo **gas freed para entrada**. Nessa condição, a filosofia deixa de ser “manter inertizado” e passa a ser “remover vapores com sequência controlada para não atravessar a faixa inflamável de forma perigosa”.

## 4. Ventilação, controle de pressão/vácuo e proteção estrutural
**Fontes:** `hse-04d3623c0070fad00a0b82db:p52-54:45.0-30.0`, `hse-04d3623c0070fad00a0b82db:p54-56:31.0-24.0`, `hse-84ee4101a6ca194620d4089b:p106-109:38.0-5.0`, `hse-84ee4101a6ca194620d4089b:p108-110:10.0-19.0`

O sistema de ventilação dos tanques não serve apenas para emissões: ele é descrito como mecanismo de **proteção da integridade estrutural** contra:

- **sobrepressão** durante enchimento, geração de gás ou falha de controle;
- **subpressão/vácuo** durante descarga ou falha de suprimento de IG.

### 4.1 Por que a ventilação é particularmente crítica em FPSO
Os trechos destacam fatores que podem elevar a carga sobre o sistema de ventilação em FPSO:

- o óleo pode sair do processamento com **baixo grau de estabilização**;
- é relativamente comum o cru ser **aquecido** para expulsar frações leves durante estabilização;
- ao chegar aos tanques, o cru aquecido pode **evoluir gás**;
- isso aumenta tanto a **vazão de vapores** quanto a probabilidade de formação de atmosferas inflamáveis ao redor dos pontos de descarga do vent.

Além disso, como o FPSO é essencialmente **fixo em posição**, em tempo calmo há menos movimento relativo do casco para ajudar na dispersão dos vapores, ao contrário de um navio tanque convencional em trânsito.

### 4.2 Localização e tipo de vents
A posição dos pontos de ventilação é muito importante, porque a atmosfera deslocada contém mistura de IG e hidrocarbonetos. As referências utilizadas citam que os vents devem ter a maior separação praticável de fontes de ignição, tanto em distância horizontal quanto em altura.

Também são citados critérios geométricos e funcionais:

- **free-flowing vents**: pelo menos **6 m acima do convés principal** e **10 m horizontalmente de tomadas de ar abertas**; devem possuir **flame arrestors** para evitar flashback ao tanque;
- **high velocity vents**: pelo menos **2 m acima do convés dos tanques de carga** e **10 m de tomadas de ar**; não requerem flame arrestor se a velocidade de saída for **≥30 m/s**, citada como cerca de duas vezes a velocidade da frente de chama.

Os vents também são citados com **detecção de fogo** e sistemas de **snuffing** associados.

### 4.3 Válvulas P/V e emergency breaker
São mencionados conjuntos automáticos de **válvulas pressão/vácuo** conectados ao vent header principal dos tanques, permitindo que os tanques “respirem”, com valores típicos citados de atuação em torno de:

- **0,2 kg/cm² acima da pressão atmosférica**;
- **0,07 kg/cm² abaixo da pressão atmosférica**.

Se a P/V principal falhar, deve existir **emergency pressure/vacuum breaker**, tratado como **Safety Critical Element (SCE)**, sujeito a teste e manutenção rotineiros. Esse breaker deve ser dimensionado para o **maior cenário plausível de sobrepressão** dos tanques de carga.

### 4.4 Condições ambientais e drenagem
Os trechos usados também chamam atenção para situações ambientais severas:

- movimento do FPSO pode afetar a **drenagem dos sistemas de vent** e das linhas associadas;
- em topsides, **roll, pitch e trim** podem afetar drenagem para flare KO drum;
- o operador deve ter orientação sobre **quando venting pode ocorrer**; no material usado aparece como orientação geral que venting deveria ocorrer com **vento ≥2 m/s**.

## 5. Monitoramento, alarmes e lógica de proteção
**Fontes:** `hse-84ee4101a6ca194620d4089b:p106-109:38.0-5.0`, `hse-84ee4101a6ca194620d4089b:p108-110:10.0-19.0`, `hse-04d3623c0070fad00a0b82db:p58-60:22.0-4.0`

### 5.1 Variáveis críticas a monitorar
Com base nos trechos, o monitoramento do sistema de IG deve abranger pelo menos:

- **teor de O₂ no IG main**;
- **teor de O₂ em cada tanque inertizado**;
- **pressão do IG main/header**;
- **pressão nos tanques**;
- **temperatura do IG no main**;
- **pressão de água do scrubber**;
- **pressão de suprimento de água do deck seal**;
- **nível de água no deck seal**.

O material também descreve boa prática de possuir:

- **sensores fixos** no sistema de IG e em cada tanque;
- **sensores portáteis de O₂** para verificações complementares;
- **calibração regular** desses instrumentos, tratados como itens críticos de segurança.

### 5.2 Alarmes explicitamente citados
Os trechos informam alarmes para:

- **alto teor de oxigênio** no IG main, normalmente **>5% v/v**;
- **baixa pressão de gás** no IG main;
- **baixa pressão de alimentação do deck seal**;
- **baixo nível de água no deck seal**;
- **alta temperatura do IG** no main;
- **baixa pressão de água para o scrubber**.

### 5.3 Ação automática e intertravamentos
A **válvula reguladora de gás** entre o scrubber e os tanques normalmente controla o fluxo de IG e deve **fechar** quando ocorrer qualquer dos eventos de alarme citados acima, ou ainda em **falha dos blowers**.

Além disso, os trechos de HSE listam filosofias de proteção para cenários de sobre/subpressão:

- **fechamento da linha de carregamento de líquido** se for detectada **alta pressão no tanque**;
- **fechamento da válvula de suprimento de IG** se for detectada **alta pressão no header**;
- **parada das bombas de offloading** se for detectada **baixa pressão no tanque**;
- **parada do sistema de recuperação de VOC** se for detectada **baixa pressão no header**.

Essas proteções mostram que o sistema de IG não deve ser analisado isoladamente: ele interage com bombas de carga, sistema de VOC, venting e estratégia de alívio.

### 5.4 Registros e disciplina de manutenção
Os trechos trazem contraste entre boa e má prática:

- boa prática: monitoramento contínuo, sensores portáteis disponíveis, instrumentos calibrados, registros acessíveis;
- má prática: ausência de registros de calibração e manutenção deficiente, mesmo quando os sensores são classificados como críticos.

## 6. Isolamento de tanques e controle administrativo
**Fontes:** `hse-04d3623c0070fad00a0b82db:p52-54:45.0-30.0`, `hse-04d3623c0070fad00a0b82db:p54-56:31.0-24.0`

Quando um tanque precisa ser isolado para inspeção, limpeza ou entrada, o procedimento de isolamento deve estar coberto por **Permit to Work (PTW)**.

O material ressalta que o isolamento individual precisa ser inequívoco, porque erros de reinstalação já levaram a acidentes. É citado um caso em que, ao recolocar em serviço um tanque previamente isolado, foi usado procedimento incorreto e um **blank não removido** causou **sobrepressurização por IG**, levando a **distorção estrutural de antepara** e reparos significativos.

Isso evidencia alguns requisitos operacionais implícitos:

- identificação positiva de tanques isolados;
- conferência física de **valves/blinds/blanks** antes da reinstalação;
- validação da rota de vent/alívio antes de recolocar o tanque em inertização;
- coordenação entre operação, manutenção e autoridade do PTW.

## 7. Lavagem, purga, gas freeing e entrada em tanques
**Fontes:** `hse-04d3623c0070fad00a0b82db:p54-56:31.0-24.0`

Para preparar um tanque que carregou cru para entrada, os trechos descrevem uma sequência importante.

### 7.1 Tank washing
Dependendo do conteúdo anterior, o tanque precisará passar por **tank washing** para remoção de depósitos. Durante essa etapa:

- se, em qualquer momento, o teor de **O₂ exceder 8%**, a lavagem deve ser **interrompida**;
- a operação só deve prosseguir quando a condição estiver estável em **8% O₂ ou menos**.

### 7.2 Purga com gás inerte
Após a lavagem, a atmosfera deve ser **purgada com IG** até que os testes demonstrem **2% ou menos de hidrocarbonetos**.

A finalidade é evitar que, no passo seguinte de gas freeing com ar, alguma parte da atmosfera do tanque passe pela **faixa inflamável**.

### 7.3 Gas freeing com ar e teste de atmosfera
Somente depois da purga adequada é que se faz o **gas freeing extensivo com ar fresco**, até a atmosfera atingir condição segura para entrada.

Os testes de gás antes da entrada devem refletir os contaminantes razoavelmente esperados, considerando:

- carga anterior;
- ventilação do espaço;
- geometria/estrutura do tanque;
- revestimentos/coatings;
- outros fatores relevantes.

Para **ballast tanks** ou **void spaces** adjacentes a tanques de carga ou bunker, é prudente testar também:

- vapores de carga;
- deficiência de oxigênio;
- gases tóxicos.

### 7.4 Risco de espaço confinado
Os trechos chamam atenção para o histórico de acidentes em espaços confinados por entrada sem supervisão ou sem aderência a procedimento. Também destacam o risco adicional de **resgate rápido** de pessoa colapsada em espaço fechado.

## 8. Sistema de blanketing com hidrocarboneto e interface com IG
**Fontes:** `hse-04d3623c0070fad00a0b82db:p54-56:31.0-24.0`, `hse-84ee4101a6ca194620d4089b:p106-109:38.0-5.0`, `hse-84ee4101a6ca194620d4089b:p108-110:10.0-19.0`

Os trechos apresentam o **hydrocarbon blanketing** como alternativa de sistema fechado, quando o campo produz gás suficiente.

### 8.1 Função
Nesse arranjo, o gás de blanket nos tanques de carga é **hidrocarboneto puro**, não IG. O objetivo é:

- impedir intrusão de oxigênio nos tanques;
- recuperar o gás deslocado/off-gas;
- reduzir ou eliminar emissões atmosféricas normais de hidrocarbonetos e VOC.

### 8.2 Modo de operação citado
- **Loading mode:** o gás excedente deslocado da carga é recuperado e reciclado ao processo por blower/ejetor/compressor.
- **Offloading mode:** devido aos grandes volumes requeridos, é provável que ainda seja necessário usar **sistema de IG** para manter a pressão nos tanques.
- Em offloading para navio aliviador, o sistema pode ser conectado ao shuttle tanker, protegendo os tanques de ambos sem perda de hidrocarbonetos/VOC.

### 8.3 Requisitos adicionais de segurança
Mesmo com blanketing de hidrocarboneto, os trechos reforçam que:

- deve existir **backup de IG**;
- o operador deve ter procedimento para **troca para IG** se o HC blanketing ficar indisponível;
- devem existir **medidas secundárias** se a troca falhar, como **shutdown da planta**;
- se o sistema puder fechar a rota para flare, precisa haver método **fail-safe** para restabelecer essa rota e evitar sobrepressão;
- se a flare não for continuamente acesa, deve haver procedimento para **acendê-la** em ocorrência de sobrepressão.

## 9. Inspeção, manutenção e integridade do sistema
**Fontes:** `hse-84ee4101a6ca194620d4089b:p108-110:10.0-19.0`, `hse-04d3623c0070fad00a0b82db:p58-60:22.0-4.0`, `hse-04d3623c0070fad00a0b82db:p52-54:45.0-30.0`

Pontos de inspeção e integridade explicitamente suportados pelos trechos:

- confirmar que há **procedimentos operacionais** para venting de tanques de carga;
- confirmar política ou procedimento para **venting em vento baixo**;
- confirmar a ação prevista para **condições ambientais extremas** que afetem drenagem dos vent headers e vasos associados;
- verificar que **P/V breakers** estão tratados como **SCE** com padrão de desempenho definido;
- verificar que o sistema de IG consegue a **capacidade mínima** requerida;
- verificar método de **monitoramento de oxigênio** e níveis de alarme;
- confirmar a **resposta operacional** esperada para alto teor de oxigênio no IG stream;
- manter **testes periódicos** de P/V valves e do emergency breaker;
- manter **calibração e registros** dos sensores fixos e portáteis.

Em FPSO, falhas nesses itens não são apenas problemas instrumentais: elas podem resultar em:

- perda da condição não inflamável do espaço de vapor;
- sobrepressão ou vácuo com risco estrutural ao tanque;
- emissão indevida de hidrocarbonetos;
- retorno de vapores para áreas indevidas do convés;
- indisponibilidade operacional para produção e offloading.

## 10. Resposta a desvios e condições anormais
**Fontes:** `hse-84ee4101a6ca194620d4089b:p106-109:38.0-5.0`, `hse-84ee4101a6ca194620d4089b:p108-110:10.0-19.0`, `hse-04d3623c0070fad00a0b82db:p52-54:45.0-30.0`, `hse-04d3623c0070fad00a0b82db:p54-56:31.0-24.0`

Com base nos trechos, a filosofia de resposta deve considerar pelo menos os desvios abaixo.

### 10.1 Alto teor de O₂ no IG
Condição crítica porque o sistema pode deixar de manter atmosfera não inflamável. A referência indica alarme acima de **5% O₂ no IG main**, e a válvula reguladora deve **fechar** para evitar envio de gás inadequado aos tanques. Operacionalmente, isso exige investigar:

- desempenho do gerador de IG;
- scrubber/condicionamento do gás;
- instrumentos de medição;
- continuidade segura das operações de carga/descarga.

### 10.2 Baixa pressão de IG ou baixa pressão no tanque
Baixa pressão eleva o risco de **ingresso de ar**. A filosofia citada inclui:

- alarme de baixa pressão no IG main;
- **parada de bombas de offloading** se houver baixa pressão no tanque;
- **parada do sistema de recuperação de VOC** se houver baixa pressão no header.

### 10.3 Alta pressão no tanque ou header
A alta pressão pode causar dano estrutural. As referências citam:

- fechamento da **linha de carregamento de líquido** se houver alta pressão no tanque;
- fechamento da **válvula de suprimento de IG** se houver alta pressão no header;
- dependência do correto funcionamento de vents, P/V valves e emergency P/V breaker.

O caso relatado de blank não removido ilustra que a sobrepressão pode resultar de **erro de alinhamento/isolamento**, não apenas de falha de instrumento.

### 10.4 Perda de água do scrubber ou do deck seal
Os alarmes de **baixa pressão de água do scrubber**, **baixa pressão de suprimento ao deck seal** e **baixo nível do deck seal** são importantes porque afetam:

- a qualidade do gás inerte;
- a integridade da barreira de não-retorno de vapores.

### 10.5 Alta temperatura do IG
A alta temperatura no IG main também é condição de alarme e gatilho para fechamento da válvula reguladora, indicando necessidade de interromper envio do gás e restabelecer a condição de tratamento.

### 10.6 Indisponibilidade do HC blanketing/VOC recovery
Se houver sistema de blanketing/recovery, a planta deve estar preparada para:

- trocar para **IG de backup**;
- aplicar **medidas secundárias** se a troca falhar;
- manter rota segura para **flare** e evitar sobrepressão.

## 11. Síntese operacional
**Fontes:** `hse-04d3623c0070fad00a0b82db:p52-54:45.0-30.0`, `hse-04d3623c0070fad00a0b82db:p54-56:31.0-24.0`, `hse-84ee4101a6ca194620d4089b:p106-109:38.0-5.0`, `hse-84ee4101a6ca194620d4089b:p108-110:10.0-19.0`, `hse-04d3623c0070fad00a0b82db:p58-60:22.0-4.0`

Para manter atmosferas não inflamáveis nos tanques de carga de um FPSO, o sistema de IG precisa ser entendido como um conjunto integrado de:

- **geração/tratamento de gás**;
- **suprimento com capacidade compatível com a taxa de transferência**;
- **pressurização positiva contínua** dos tanques, salvo gas freeing controlado;
- **monitoramento contínuo de O₂ e pressão**;
- **dispositivos de não-retorno** para impedir retrofluxo de vapores;
- **venting e P/V protection** para preservar integridade estrutural;
- **isolamento seguro** de tanques para inspeção e entrada;
- **procedimentos de resposta a falhas** de qualidade do IG, pressão, vedação, ventilação e recuperação de vapores.

Do ponto de vista de operação e integridade, a falha do sistema de IG não é apenas uma anomalia de utilidade: ela pode comprometer simultaneamente **segurança de processo, segurança marítima, integridade estrutural do tanque, disponibilidade de produção e controle ambiental**.