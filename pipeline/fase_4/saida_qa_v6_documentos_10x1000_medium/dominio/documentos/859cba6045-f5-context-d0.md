# Fora de especificação e conformidade ambiental no tratamento de água produzida para descarte

## 1. Escopo técnico da faceta

Em FPSOs, a decisão operacional mais crítica na água produzida para descarte não é apenas **remover óleo**, mas **evitar qualquer descarga ao mar quando a corrente estiver fora de especificação** ou quando houver dúvida razoável sobre sua conformidade. Na prática, isso exige integrar:

- desempenho do trem de tratamento;
- confiabilidade de instrumentos e amostragem;
- destinação segura das correntes fora de especificação;
- atendimento ao licenciamento ambiental e aos requisitos regulatórios aplicáveis.

O material fornecido permite tratar principalmente de **decisões operacionais para correntes offspec**, seus riscos e a relação com a conformidade ambiental brasileira.  
**Fontes:** `anp-704e73838f089ea0537959f4:p18-21:23.0-14.0`, `anp-6fe724365261e407a57c90d5:p1-3:0.0-33.0`, `petroles-4ee4bce16acf674505c8912d:pNone:2075744.0-2075782.0`, `petroles-4ee4bce16acf674505c8912d:pNone:274493.0-274529.0`

## 2. O que significa “fora de especificação” na água produzida

Para esta faceta, uma corrente de água produzida está **fora de especificação** quando não pode ser descarregada ao mar com segurança e conformidade, seja por:

1. **TOG acima do limite aplicável** ao descarte contínuo;
2. **presença de óleo livre ou de slug de óleo bruto/emulsão**, ainda que transitório;
3. **incerteza metrológica relevante**, por falha de analisador, amostragem, medidor de interface ou inconsistência entre sinais de processo;
4. **condição anormal de processo** que invalide a confiança no tratamento, mesmo antes da confirmação laboratorial.

Esse ponto é essencial: a não conformidade pode ser **real** ou **suspeita**, e ambas exigem ação conservadora. O caso investigado pela ANP na P-53 mostra descarga oleosa intermitente sem perda de contenção clássica, associada a desvio/descontrole operacional no separador trifásico ou no tratador eletrostático, com arraste de óleo bruto pela corrente de água produzida.  
**Fontes:** `anp-704e73838f089ea0537959f4:p18-21:23.0-14.0`

## 3. Mecanismos típicos que levam a corrente offspec

### 3.1. Sobrecarga de óleo a montante do tratamento de água

O relatório da P-53 destaca um mecanismo crítico: o sistema de tratamento de água produzida estava projetado para receber, na saída do separador trifásico, água com cerca de **1000 ppm de óleo disperso**, e **não** para receber carga de **óleo bruto com baixa diluição em água**. Em outras palavras, há diferença entre:

- água com óleo disperso dentro da janela de projeto; e
- perda de óleo/emulsão para a linha de água, que muda completamente o regime hidráulico e a separabilidade.

Quando ocorre esse segundo caso, equipamentos posteriores podem deixar de atuar como polidores e passar a receber uma carga para a qual não foram dimensionados. O resultado provável é aumento abrupto do TOG e risco de descarga ao mar.  
**Fonte:** `anp-704e73838f089ea0537959f4:p18-21:23.0-14.0`

### 3.2. Falha ou má leitura de instrumentos de interface

No mesmo caso, o valor exibido de interface no separador não indicava perda de emulsão pela saída de água, mas a investigação posterior concluiu que o **medidor de interface apresentou problemas operacionais** e não refletia o valor real. Isso mostra que, para decisão operacional, **sinal “normal” no painel não é prova suficiente de conformidade**.

Consequência prática: sempre que houver indício externo de descarga oleosa, tendência incoerente de processo ou deterioração súbita da qualidade da água, o operador deve considerar a hipótese de **instrumento enganoso**, e não apenas de processo estável.  
**Fonte:** `anp-704e73838f089ea0537959f4:p18-21:23.0-14.0`

### 3.3. Desempenho insuficiente dos tratadores a montante

O parecer citado no relatório da ANP menciona obrigações de melhoria na planta da P-53, incluindo **problemas em tratadores eletrostáticos** e em **medidores de interface dos separadores**. Isso evidencia uma relação estrutural: a conformidade do descarte não depende só do skid final de água produzida; depende também de como o óleo é separado antes que a água chegue ao trem de polimento.

Em FPSOs, uma planta de água produzida frequentemente falha por efeito de **causa a montante**, como:

- instabilidade de interface no separador;
- piora na desidratação/desemulsificação do óleo;
- arraste intermitente de emulsão;
- alteração de química de processo.

Nesses casos, “ajustar apenas o skid de água” pode não resolver.  
**Fonte:** `anp-704e73838f089ea0537959f4:p18-21:23.0-14.0`

### 3.4. Operação fora da janela hidráulica de hidrociclones

O estudo do sistema subsea SSAO registra testes com **recirculação parcial do underflow** dos hidrociclones quando a água produzida era bombeada para topside para monitoramento de qualidade, pois sem essa recirculação o volume de água que atravessaria os hidrociclones **não seria suficiente para assegurar o desempenho correto**.

A lição operacional é transferível como conceito: hidrociclones dependem de **janela hidráulica e razão de split**. Se a vazão efetiva cair abaixo da faixa necessária, a eficiência de separação pode se degradar, e a corrente passar a offspec mesmo sem falha mecânica.  
**Fonte:** `regis-0b8880698dff457e3e00d8b8:pNone:442.60-456.0`

## 4. Hierarquia de decisões para corrente fora de especificação

### 4.1. Princípio decisório

Diante de suspeita ou confirmação de água produzida offspec, a lógica operacional conservadora é:

1. **evitar descarte ao mar** da corrente duvidosa;
2. **conter e desviar** a corrente para rota segura temporária;
3. **estabilizar a causa de processo** a montante;
4. **confirmar a qualidade** por medição confiável antes de retomar o overboard.

Essa hierarquia decorre tanto do risco ambiental quanto do fato de que algumas anomalias são **intermitentes**: podem cessar sem intervenção visível, mascarando a causa. Foi exatamente esse padrão que a investigação da P-53 identificou.  
**Fonte:** `anp-704e73838f089ea0537959f4:p18-21:23.0-14.0`

### 4.2. Desvio e retenção temporária

Quando a água está fora de especificação, uma opção operacional usual é desviá-la para:

- vaso de rejeitos oleosos/slop;
- tanque dedicado de offspec water;
- recirculação para retratamento, quando o arranjo permitir;
- outra rota de contenção prevista em projeto e procedimento.

Entretanto, o alerta de segurança da ANP mostra que **armazenar água produzida em tanques inadequados** pode gerar falha estrutural grave. Houve eventos em que tanques de carga ou tanques secundários foram usados por períodos incompatíveis com sua proteção anticorrosiva, resultando em dano estrutural e, em um caso, descarga de mais de 25 m³ de óleo no mar.

Portanto, a decisão de “segurar offspec” só é aceitável se a rota de retenção:

- estiver **prevista em projeto** para água produzida;
- tiver **proteção contra corrosão** compatível com o fluido e o tempo de residência esperado;
- estiver coberta por **inspeção, manutenção e gestão de integridade** adequadas;
- for claramente distinguida nos documentos operacionais entre tanque primário, secundário e usos permitidos.

Não basta haver volume disponível; é preciso haver **aptidão de projeto e integridade**.  
**Fontes:** `anp-6fe724365261e407a57c90d5:p1-3:0.0-33.0`

### 4.3. Recirculação para retratamento

Recircular a água offspec para a frente do trem de tratamento ou para etapa anterior pode ser medida eficaz quando o problema é reversível e o circuito suporta a carga adicional. A evidência do estudo com hidrociclones mostra que a **recirculação parcial** também pode ser necessária para manter desempenho do próprio equipamento em certas condições de baixa vazão.

Operacionalmente, a recirculação tende a ser mais adequada quando:

- a causa é instabilidade transitória;
- o sistema tem capacidade hidráulica para retratamento;
- não há risco de realimentar o sistema com grande volume de óleo livre;
- a recirculação melhora a janela operacional do equipamento em vez de colapsá-la.

Ela tende a ser menos adequada quando:

- há slug de óleo bruto/emulsão severa a montante;
- o gargalo está justamente no equipamento de retratamento;
- o sistema já opera próximo do limite de vazão ou pressão.

**Fonte:** `regis-0b8880698dff457e3e00d8b8:pNone:442.60-456.0`, `anp-704e73838f089ea0537959f4:p18-21:23.0-14.0`

### 4.4. Redução de carga e estabilização a montante

Se a origem da não conformidade está em separador trifásico, tratador eletrostático ou química do óleo/água, a resposta operacional não deve ficar restrita ao sistema de água produzida. Medidas típicas de estabilização incluem:

- corrigir controle de interface;
- revisar condições dos tratadores eletrostáticos;
- reduzir temporariamente a carga de produção, se necessário;
- revisar dosagem química e sua efetividade;
- segregar correntes anormais até recuperar regime estacionário.

O ponto central é que **água offspec muitas vezes é sintoma, não causa primária**.  
**Fonte:** `anp-704e73838f089ea0537959f4:p18-21:23.0-14.0`

## 5. Monitoramento para decisão: dado operacional, amostragem e evidência de conformidade

### 5.1. TOG como variável de conformidade

Os trechos fornecidos apontam que, no Brasil, o descarte contínuo de água de processo ou produção em plataformas marítimas deve atender a limites de **teor de óleos e graxas (TOG)** definidos em resolução CONAMA específica, expressos como **média aritmética simples mensal** e **valor máximo diário**. Mesmo sem os números legíveis nos trechos, fica claro que:

- a conformidade não depende apenas de um valor instantâneo;
- há componente de controle contínuo e componente de pico diário;
- o monitoramento de TOG é base mínima para decisão de descarte.

**Fonte:** `petroles-4ee4bce16acf674505c8912d:pNone:2075744.0-2075782.0`

### 5.2. Medição on-line não substitui verificação crítica

O caso da P-53 mostra que indicadores de sala de controle podem sugerir normalidade enquanto ocorre descarga anômala. Assim, uma boa prática operacional é tratar a conformidade como resultado de **camadas de evidência**, por exemplo:

- analisador on-line de TOG, quando existente;
- amostragem representativa e análise laboratorial;
- tendência de interface e níveis dos vasos;
- comportamento de slop/rejeitos;
- observação operacional e evidências externas de anomalia.

Se essas camadas forem incoerentes entre si, a decisão segura é **restringir o descarte** até esclarecimento.  
**Fonte:** `anp-704e73838f089ea0537959f4:p18-21:23.0-14.0`

### 5.3. Avaliação de eficiência de remoção

O material experimental de flotação usa concentração inicial e final para avaliar remoção de óleo. Como forma geral de avaliação:

\[
\eta = \frac{C_0 - C_f}{C_0} \times 100
\]

onde:

- \(C_0\) = concentração inicial do efluente;
- \(C_f\) = concentração da água tratada;
- \(\eta\) = eficiência de remoção de óleo.

Em operação industrial, esse tipo de indicador é útil para:

- comparar desempenho entre equipamentos ou modos operacionais;
- verificar degradação progressiva;
- distinguir falha por sobrecarga de falha por baixa eficiência intrínseca.

Contudo, eficiência percentual alta não basta para autorizar descarte: a corrente final ainda precisa cumprir o **limite absoluto de TOG** e demais condicionantes aplicáveis.  
**Fonte:** `petroles-004c2afadba7ea17c7dd7908:pNone:391345.120-391388.60`

## 6. Papel dos equipamentos na decisão de conformidade

### 6.1. Separação primária e tratadores

O fluxograma de separação primária citado no material mostra que a água para o sistema de água produzida sai de um arranjo em que também há óleo e gás, com influência de aquecimento e tratadores eletrostáticos. Isso reforça que a qualidade da água enviada ao tratamento depende fortemente da **estabilidade da separação primária**.

Se a água já sai da etapa primária com carga anormal de óleo, o sistema posterior pode apenas limitar danos, não garantir conformidade.  
**Fonte:** `petroles-4ee4bce16acf674505c8912d:pNone:2061097.0-2061130.0`

### 6.2. Hidrociclones

O estudo complementar do SSAO é particularmente útil para decisões operacionais porque mostra que o hidrociclone pode exigir **recirculação parcial do underflow** para manter a condição de operação. Portanto, diante de água offspec, o operador deve investigar não só fouling ou desgaste, mas também:

- queda de vazão total;
- alteração do split de underflow/overflow;
- mudança de propriedades do óleo cru;
- alteração do regime de alimentação.

Logo, offspec não implica automaticamente falha mecânica do hidrociclone; pode indicar **saída da janela operacional**.  
**Fonte:** `regis-0b8880698dff457e3e00d8b8:pNone:442.60-456.0`

### 6.3. Flotação

O trabalho experimental sobre flotação destaca a técnica como uma das mais utilizadas no tratamento de água produzida, baseada na adesão de microbolhas de ar às partículas oleosas, reduzindo a densidade aparente do agregado e favorecendo a subida/flotação. O estudo também mostra que variáveis como concentração do efluente, vazão de alimentação e vazão de diluição influenciam a eficiência de remoção.

Para a operação, isso sugere que unidades de flotação podem degradar seu desempenho por:

- aumento de carga de óleo na alimentação;
- alteração de vazão fora da condição ótima;
- hidráulica inadequada de recirculação/diluição.

Assim, quando uma unidade de flotação entrega água offspec, a resposta deve considerar tanto o estado mecânico quanto a **janela de processo**.  
**Fonte:** `petroles-004c2afadba7ea17c7dd7908:pNone:391345.120-391388.60`

## 7. Correntes oleosas associadas e sua destinação

Quando a água produzida fica fora de especificação, surgem ou aumentam correntes secundárias com óleo, como:

- rejeitos oleosos;
- slop do tratamento;
- underflow enriquecido em óleo;
- drenagens para retratamento.

O relatório da P-53 menciona explicitamente o **vaso de rejeitos oleosos/slop** como equipamento relevante para análise do evento. Na lógica de operação, essas correntes não devem ser vistas como resíduo “periférico”, mas como parte do sistema de contenção ambiental: elas permitem retirar do overboard aquilo que não está apto ao descarte.

Porém, sua destinação segura depende de capacidade, projeto, integridade e procedimentos. O alerta da ANP demonstra que o armazenamento prolongado de água produzida offspec em tanques inadequados pode transformar uma medida de contenção em nova fonte de acidente.  
**Fontes:** `anp-704e73838f089ea0537959f4:p18-21:23.0-14.0`, `anp-6fe724365261e407a57c90d5:p1-3:0.0-33.0`

## 8. Conformidade ambiental brasileira: o que o operador precisa considerar

### 8.1. Licenciamento ambiental e controle federal offshore

Os trechos fornecidos indicam que, nas atividades petroleiras offshore, o **licenciamento e o controle ambiental são eminentemente federais**, executados pelo **IBAMA**, e que os contratos de concessão e operação estão condicionados ao prévio licenciamento ambiental. Também indicam a importância das resoluções CONAMA para padrões e condições de lançamento de efluentes.

Para a operação de água produzida, isso significa que a decisão de descarte deve obedecer simultaneamente a:

- padrões ambientais gerais aplicáveis;
- condições da licença ambiental da instalação;
- exigências e obrigações específicas eventualmente impostas em pareceres e fiscalizações.

Em termos práticos, a licença pode ser tão importante quanto a regra geral, porque pode impor obrigações adicionais de monitoramento, melhoria de planta e gestão da água produzida.  
**Fontes:** `petroles-4ee4bce16acf674505c8912d:pNone:274493.0-274529.0`, `anp-704e73838f089ea0537959f4:p18-21:23.0-14.0`

### 8.2. Resoluções CONAMA e padrão de lançamento

O material aponta duas camadas normativas citadas para o tema:

- resolução geral sobre classificação de corpos d’água e padrões de lançamento de efluentes;
- resolução complementar específica sobre descarte contínuo de água de processo ou produção em plataformas marítimas.

Os trechos deixam claro que, para plataformas, o controle explicitado inclui pelo menos o **TOG** com média mensal e máximo diário. Em operação, isso reforça a necessidade de:

- registrar histórico de desempenho, não apenas resultado pontual;
- controlar eventos transitórios de pico;
- rastrear desvios e paradas de overboard por offspec.

**Fonte:** `petroles-4ee4bce16acf674505c8912d:pNone:2075744.0-2075782.0`

### 8.3. Papel da ANP na segurança operacional e integridade

O alerta de segurança da ANP relaciona o tema não só ao meio ambiente, mas à **segurança operacional e integridade mecânica**, citando requisitos do regulamento técnico do SGSO para:

- planos e procedimentos de inspeção, teste e manutenção;
- garantia da qualidade na execução dos procedimentos;
- monitoramento e avaliação de resultados de inspeções e testes;
- definição de responsabilidades de contratadas;
- identificação de normas, padrões e boas práticas desde projeto até desativação.

Aplicado à água produzida offspec, isso significa que a conformidade ambiental depende também de:

- confiabilidade estrutural dos tanques e rotas de retenção;
- qualidade das inspeções e relatórios;
- clareza documental sobre o uso permitido de cada tanque/equipamento;
- pessoal e supervisão adequados.

**Fonte:** `anp-6fe724365261e407a57c90d5:p1-3:0.0-33.0`

## 9. Critérios práticos para decisão operacional

Com base nos materiais, uma matriz prática de decisão pode ser sintetizada assim:

### 9.1. Quando suspender ou desviar o descarte

Deve-se tratar a corrente como offspec e restringir o overboard quando houver um ou mais dos seguintes sinais:

- evidência visual, remota ou operacional de descarga oleosa;
- aumento súbito de óleo na água tratada;
- comportamento incoerente entre processo e instrumentos;
- suspeita de falha em medidor de interface ou tratador;
- saída do equipamento de sua janela de vazão/recirculação.

### 9.2. Quando privilegiar correção a montante

É preferível atuar a montante quando os indícios apontarem para:

- perda de emulsão pelo separador;
- instabilidade de interface;
- degradação do tratador eletrostático;
- mudança de características do fluido ou da química.

### 9.3. Quando a retenção temporária é aceitável

A retenção temporária é medida defensiva válida se:

- a rota foi projetada para água produzida/offspec;
- a integridade e a proteção anticorrosiva são compatíveis;
- há inspeção e limite de tempo/uso claramente definidos.

### 9.4. Quando a retenção temporária se torna novo risco

Ela se torna inadequada quando:

- usa tanque não projetado ou não protegido para água produzida;
- o tanque secundário passa a ser usado continuamente fora do previsto;
- não há diferenciação operacional clara entre tanques e usos;
- inspeção, limpeza e verificação de integridade são deficientes.

**Fontes:** `anp-704e73838f089ea0537959f4:p18-21:23.0-14.0`, `anp-6fe724365261e407a57c90d5:p1-3:0.0-33.0`, `regis-0b8880698dff457e3e00d8b8:pNone:442.60-456.0`

## 10. Boas práticas de prevenção e otimização compatíveis com os trechos fornecidos

1. **Não confiar em um único indicador** para liberar descarte.
2. **Tratar descargas intermitentes como evento crítico**, mesmo que cessem espontaneamente.
3. **Manter instrumentos de interface e tratadores sob gestão de desempenho**, pois defeitos nesses itens afetam diretamente o overboard.
4. **Operar hidrociclones e flotação dentro da janela hidráulica**, considerando vazão, recirculação e características do fluido.
5. **Usar apenas tanques e vasos adequados ao serviço de offspec water**, com proteção anticorrosiva compatível.
6. **Vincular decisão operacional à integridade mecânica**, e não só ao balanço de volume disponível.
7. **Documentar claramente as rotas de contingência**, incluindo diferenciação entre tanque offspec primário e secundário e seus limites de uso.
8. **Rastrear tendências de TOG, desvios, recirculações e retratamentos** para atuação antes da violação ambiental.

**Fontes:** `anp-704e73838f089ea0537959f4:p18-21:23.0-14.0`, `anp-6fe724365261e407a57c90d5:p1-3:0.0-33.0`, `regis-0b8880698dff457e3e00d8b8:pNone:442.60-456.0`, `petroles-004c2afadba7ea17c7dd7908:pNone:391345.120-391388.60`

## 11. Síntese final

Na ótica desta faceta, conformidade ambiental no descarte de água produzida em FPSOs depende menos de um “limite numérico isolado” e mais da capacidade de **tomar a decisão correta quando a corrente sai do regime normal**. Os materiais mostram três mensagens centrais:

- água offspec costuma ser consequência de **desvio de processo a montante**, não apenas de falha do último equipamento;
- a resposta correta é **reter, desviar, recircular ou estabilizar**, e não insistir no overboard com base em indicação duvidosa;
- a contenção de offspec precisa ser feita em **equipamentos aptos e íntegros**, caso contrário a solução temporária vira novo risco ambiental e de segurança operacional.

Em termos profissionais, o operador deve ser capaz de reconhecer sinais precoces de não conformidade, escolher a rota de contingência tecnicamente segura e alinhar a decisão aos requisitos do licenciamento, das resoluções ambientais aplicáveis e da gestão de integridade da instalação.  
**Fontes:** `anp-704e73838f089ea0537959f4:p18-21:23.0-14.0`, `anp-6fe724365261e407a57c90d5:p1-3:0.0-33.0`, `petroles-4ee4bce16acf674505c8912d:pNone:2075744.0-2075782.0`, `petroles-4ee4bce16acf674505c8912d:pNone:274493.0-274529.0`