# Controle subsea e diagnóstico de falhas

## 1. Visão funcional do sistema de controle subsea
O sistema de controle subsea associado a poços, árvores de natal molhadas, manifolds e válvulas submarinas é responsável por **comandar atuadores remotamente**, **monitorar variáveis do processo** e **executar paradas seguras**, inclusive em emergência. Nos trechos disponíveis, os requisitos funcionais destacados para sistemas de controle de produção incluem:

- prover operabilidade para todas as válvulas subsea controladas remotamente;
- prover dados e informações suficientes para operação segura;
- prover parada de produção de emergência com resposta correta e dentro do tempo especificado pela norma aplicável ou pela autoridade competente.

A arquitetura básica é dividida entre:

### 1.1 Parte topside
Na unidade de produção, aparecem como elementos principais:

- **HPU - Hydraulic Power Unit**: fornece energia hidráulica ao sistema;
- **unidade de energia elétrica**;
- **MCS - Master Control Station / estação mestra de controle**: envia comandos e recebe feedback do sistema submarino;
- **topside junction box**: integra os meios de transmissão de energia e informação entre a unidade e o sistema submarino.

### 1.2 Parte submarina
No leito marinho, os trechos citam principalmente:

- ponto de recepção do umbilical;
- **SCM - Subsea Control Module**;
- **SEM - Subsea Electronic Module**;
- sensores e atuadores associados a válvulas e equipamentos.

O fluxo de informação é **bidirecional**: comandos descem da plataforma para o sistema submarino, e medições/estados retornam para a plataforma.

### 1.3 Papel dos sensores e do feedback
Os parâmetros mencionados como relevantes para controle e diagnóstico incluem, entre outros:

- pressão e temperatura de produção;
- pressão na choke;
- pressão no anular;
- pressão e temperatura no manifold;
- detecção de vazamento de hidrocarbonetos;
- posição de válvulas da árvore, direta ou inferida;
- posição da choke;
- diferencial de pressão na choke.

Esses sinais são a base para a lógica de operação, alarme, shutdown e diagnóstico.

_Fontes da seção: regis-9d017883010dd907fdb51652:pNone:188.0-212.0; regis-9d017883010dd907fdb51652:pNone:199.0-224.0_

## 2. Meios de comunicação e atuação
O elo físico entre FPSO e sistema submarino é o **umbilical**, descrito como um conjunto de tubulações e cabos elétricos/hidráulicos destinado a transportar:

- potência hidráulica;
- sinais elétricos;
- energia elétrica;
- produtos químicos, quando aplicável.

Nos materiais, o umbilical aparece como o principal meio de interface entre topside e subsea para comando, realimentação e suprimento energético. Também é citado que decisões de projeto devem buscar reduzir quantidade de cabos, tubulações, conectores e manobras, porque a distribuição dos elementos de controle afeta diretamente custo, peso e eficiência do sistema.

A HPU topside é descrita como a fonte de pressão hidráulica, com linhas de alta e baixa pressão. No campo, sua capacidade de manter pressão também influencia a percepção operacional de falhas, pois pequenos vazamentos podem ser temporariamente compensados pelo suprimento contínuo de fluido.

_Fontes da seção: regis-9d017883010dd907fdb51652:pNone:188.0-212.0; regis-9d017883010dd907fdb51652:pNone:199.0-224.0; regis-4dbb08942c491bcd76dc7960:pNone:455.60-495.0; petroles-004c2afadba7ea17c7dd7908:pNone:2972565.0-2972611.0_

## 3. Arquiteturas de controle relevantes para operação e diagnóstico

### 3.1 Controle hidráulico direto
No controle hidráulico direto, a válvula ou outra função subsea é pressurizada e despressurizada **diretamente pela linha dedicada desde a plataforma**. Características principais extraídas dos trechos:

- é a arquitetura mais simples;
- normalmente requer **uma linha hidráulica por função**;
- tende a aumentar dimensões e peso do umbilical;
- tem dificuldade maior para adicionar redundâncias;
- em grandes distâncias e lâminas dágua elevadas, pode apresentar **tempo de resposta lento**, especialmente na despressurização e especialmente quando há mangueiras termoplásticas;
- sua simplicidade facilita entendimento do sistema e localização de falhas.

Do ponto de vista de diagnóstico, a separação física por função ajuda a isolar defeitos: se uma única função falha em um sistema direto, a suspeita inicial tende a recair na linha dedicada, no atuador ou na válvula correspondente.

### 3.2 Controle hidráulico pilotado
Nos trechos disponíveis, o sistema pilotado usa:

- módulo de controle submarino;
- arranjo de válvulas pilotadas;
- acumuladores hidráulicos subsea alimentados pela HPU topside;
- comandos da estação mestra para manipular as válvulas pilotadas via mudanças de pressão.

Em comparação com o direto, o pilotado permite:

- umbilicais mais leves;
- maior flexibilidade para redundância;
- aumento de confiabilidade do controle.

Operacionalmente, isso desloca parte da lógica e da distribuição hidráulica para o ambiente submarino, mudando o diagnóstico: uma falha pode estar no suprimento comum, no módulo subsea ou no circuito local pilotado, não apenas numa linha dedicada individual.

### 3.3 Controle multiplexado / eletro-hidráulico
Os materiais descrevem uma arquitetura em que **sinais elétricos** são enviados da plataforma ao **SCM/SEM**, que decodifica o comando e aciona válvulas solenóides ou a válvula de controle direcional para aplicar energia hidráulica ao atuador subsea. Características destacadas:

- um pequeno conjunto de cabos de sinal, combinado com suprimento hidráulico, pode atuar muitas funções;
- a conversão do comando elétrico em ação hidráulica ocorre no ambiente submarino;
- o uso de acumuladores e distribuição local reduz a necessidade de grandes quantidades de linhas dedicadas;
- o fechamento pode ser mais rápido que no sistema direto porque a descarga/despressurização ocorre localmente, sem depender do retorno integral do fluido até a superfície;
- a arquitetura é mais complexa, com maior exigência de energia elétrica, adaptadores/conectores e maior sofisticação eletrônica;
- requer **maior limpeza do fluido hidráulico**, devido às pequenas passagens nas válvulas solenóides do SCM.

Nos trechos, o termo eletro-hidráulico aparece também como uma categoria mais ampla de sistemas com comando elétrico e atuação hidráulica. Para fins operacionais em FPSO-subsea, a interpretação mais robusta com base no material é a de **controle multiplexado com comando elétrico e potência hidráulica distribuída localmente**.

### 3.4 Controle elétrico
Também é citada a possibilidade de sistemas essencialmente elétricos, com substituição de unidades hidráulicas e tubulações por cabos elétricos para energia e sinais. Os trechos os caracterizam como:

- mais complexos;
- mais caros para instalar e manter;
- adequados a elevado grau de automação;
- dependentes de grande disponibilidade de energia elétrica.

Como o foco desta faceta é hidráulico e eletro-hidráulico, esse tipo é relevante principalmente como referência comparativa.

### 3.5 Comparação operacional resumida
| Arquitetura | Comunicação dominante | Atuação final | Vantagens | Limitações operacionais e de diagnóstico |
|---|---|---|---|---|
| Hidráulico direto | Hidráulica por linha dedicada | Hidráulica no atuador | Simplicidade, fácil entendimento, fácil correlação função-linha | Umbilical pesado, pouca redundância, resposta lenta em longas distâncias |
| Hidráulico pilotado | Comando via módulo e pressão pilotada | Hidráulica local/pilotada | Menor peso de umbilical, maior flexibilidade de redundância | Diagnóstico mais distribuído entre topside, módulo e circuito local |
| Multiplexado eletro-hidráulico | Elétrica para comando + hidráulica de suprimento | Hidráulica comandada localmente por SCM/SEM | Muitas funções com poucos sinais, resposta mais rápida, maior automação | Maior complexidade, dependência de eletrônica/solenóides e limpeza do fluido |

_Fontes da seção: regis-9d017883010dd907fdb51652:pNone:199.0-224.0; regis-4dbb08942c491bcd76dc7960:pNone:455.60-495.0; petroles-004c2afadba7ea17c7dd7908:pNone:2972565.0-2972611.0_

## 4. Atuação de válvulas subsea e comportamento fail-safe
Nos trechos sobre árvore de natal molhada, as principais válvulas controladas da plataforma incluem master de produção, wing de produção, cross-over, master de anular e wing de anular. O material descreve essas válvulas como **do tipo gaveta com característica fail safe close**: para permanecerem abertas, o atuador deve estar pressurizado com fluido hidráulico; na perda de pressão, a mola promove o fechamento.

Essa lógica de falha segura é essencial para entender sintomas operacionais:

- **perda de pressão hidráulica** tende a resultar em fechamento automático;
- um vazamento na linha de controle pode causar **fechamento espúrio**;
- se o vazamento for pequeno, a HPU pode compensar a perda e mascarar temporariamente a falha, mantendo a válvula aberta até que a capacidade de reposição seja excedida ou a perda se agrave.

O mesmo raciocínio é coerente com outros dispositivos de segurança citados, como o DSSS/DHSV, também descrito no material como predominantemente controlado pela plataforma e com característica de falha segura.

Do ponto de vista de diagnóstico, isso significa que um fechamento inesperado nem sempre indica defeito da válvula em si; pode refletir perda de integridade hidráulica a montante do atuador, falha no SCM/solenóide, comando indevido ou perda de suprimento.

_Fontes da seção: petroles-004c2afadba7ea17c7dd7908:pNone:2972538.0-2972588.0; petroles-004c2afadba7ea17c7dd7908:pNone:2972565.0-2972611.0_

## 5. Monitoramento para operação normal e para diagnóstico
O material indica que o sistema de controle não apenas atua válvulas, mas também fornece à superfície informação de processo e de integridade operacional. Para diagnóstico de falhas, alguns grupos de sinais são particularmente relevantes:

### 5.1 Sinais de processo
- pressão e temperatura de produção;
- pressão do anular;
- pressão e temperatura em manifolds;
- diferencial de pressão em choke.

Esses dados ajudam a distinguir falhas de processo de falhas de controle. Exemplo: uma queda de vazão com válvula confirmadamente aberta pode indicar restrição de escoamento; já uma mudança de posição não comandada com alteração simultânea de pressão de atuação aponta mais para falha do sistema de controle.

### 5.2 Sinais de estado de atuadores e válvulas
- posição de válvula, direta ou inferida;
- posição da choke;
- confirmação de execução do comando.

Uma divergência entre comando enviado e posição retornada é indício clássico de anomalia de comunicação, atuação, instrumentação ou travamento mecânico.

### 5.3 Alarmes de integridade
- detecção de vazamento de hidrocarbonetos;
- comportamento anormal de consumo de fluido hidráulico;
- degradação de tempo de resposta.

Quando combinados, esses sinais ajudam a decidir se a resposta deve ser de shutdown, isolamento, investigação por ROV ou manutenção corretiva programada.

_Fontes da seção: regis-9d017883010dd907fdb51652:pNone:188.0-212.0; regis-4dbb08942c491bcd76dc7960:pNone:455.60-495.0; petroles-004c2afadba7ea17c7dd7908:pNone:2972565.0-2972611.0_

## 6. Diagnóstico de falhas operacionais por mecanismo provável

## 6.1 Falhas hidráulicas
### a) Vazamento em linha de controle ou no umbilical
Sintomas coerentes com os trechos:

- aumento de consumo da HPU;
- dificuldade de manter válvula aberta;
- fechamento espúrio de válvula fail-safe close;
- piora progressiva do desempenho em vez de perda instantânea total, quando a HPU ainda compensa pequenas perdas.

Em sistemas diretos, a correlação entre função e linha dedicada facilita localizar a função afetada. Em sistemas multiplexados, o diagnóstico deve separar se a perda está no suprimento hidráulico comum, no SCM ou no ramo final até a válvula.

### b) Resposta lenta de abertura/fechamento
Causas apontadas ou sugeridas pelos trechos:

- grande comprimento de umbilical;
- uso de mangueiras termoplásticas, com efeito mais sensível sobre a resposta;
- retorno do fluido até a superfície no sistema direto;
- aumento de atrito no conjunto atuador-válvula.

A degradação do tempo de resposta deve ser comparada com a arquitetura existente. Tempos maiores são mais esperados em controle direto que em multiplexado; portanto, a interpretação de anomalia depende da configuração instalada.

### c) Contaminação do fluido hidráulico
Nos sistemas multiplexados, a limpeza do fluido é especialmente crítica devido às pequenas passagens nas válvulas solenóides do SCM. Assim, falhas intermitentes, atuação incompleta ou comportamento errático de uma função comandada via SCM são compatíveis com hipótese de contaminação ou obstrução fina.

## 6.2 Falhas elétricas, eletrônicas e de comunicação
A arquitetura descrita implica uma cadeia de comunicação que passa por MCS, cabos/fibras no umbilical, SCM e SEM. Embora os trechos não forneçam uma taxonomia formal de falhas elétricas, a lógica operacional permite distinguir alguns padrões:

- **falha de múltiplas funções ao mesmo tempo**: suspeita maior em alimentação comum, comunicação topside-subsea, SCM ou SEM;
- **falha de uma única função em sistema multiplexado**: suspeita em canal específico, solenóide correspondente, circuito local ou atuador da válvula;
- **feedback ausente com comando emitido**: suspeita em sensor, instrumentação de posição ou caminho de retorno da informação;
- **feedback inconsistente**: suspeita em sensor/SEM ou em mecanismo que se move parcialmente sem completar curso.

## 6.3 Falhas mecânicas do conjunto válvula-atuador
Se o comando chega e a pressão de atuação cresce, mas a posição não muda como esperado, uma hipótese compatível com os trechos sobre assinatura de pressão é o aumento de atrito, desgaste ou outro tipo de degradação mecânica no conjunto atuador-válvula.

## 6.4 Efeito da localização do SCM sobre o diagnóstico
O SCM pode estar instalado junto à ANM ou em um manifold. Quando a árvore é controlada via manifold, o material descreve uma lógica híbrida: **multiplexado da plataforma até o manifold** e comportamento análogo a **hidráulico direto do manifold até a ANM**. Isso altera o raciocínio de falha:

- se várias funções de várias árvores falham simultaneamente, a suspeita pode se concentrar no trecho comum até o manifold;
- se a falha é localizada em uma árvore ou função específica, a suspeita desloca-se para o ramo downstream do manifold, para a linha final ou para o equipamento local.

_Fontes da seção: petroles-004c2afadba7ea17c7dd7908:pNone:2972565.0-2972611.0; regis-9d017883010dd907fdb51652:pNone:188.0-212.0; regis-4dbb08942c491bcd76dc7960:pNone:455.60-495.0_

## 7. Assinatura de pressão como ferramenta de condition monitoring
Os trechos sobre válvulas submarinas de isolamento e ESDV oferecem um conceito útil para diagnóstico subsea: a **assinatura de pressão**, definida como o gráfico temporal das pressões necessárias para abertura e fechamento da válvula/atuador.

### 7.1 O que a assinatura observa
A assinatura de pressão relaciona:

- pressão de atuação ao longo do tempo;
- pressões a montante e jusante da válvula;
- eventualmente outras pressões internas relevantes ao projeto da válvula.

### 7.2 O que os pontos-chave indicam
Segundo o material, há pontos notáveis na curva que permitem avaliar se o desgaste ou a degradação do sistema estão gerando **atrito elevado** e, portanto, pressões significativamente diferentes das esperadas em condição normal.

Em termos práticos, a assinatura pode apoiar o diagnóstico de:

- aumento de atrito no atuador;
- degradação de vedação ou partes móveis;
- alteração de comportamento dinâmico do acionamento;
- perda de desempenho antes da falha funcional completa.

### 7.3 Relação com tempo de resposta
Como a assinatura é temporal, ela também ajuda a avaliar o **tempo real de acionamento**, que nos próprios trechos é tratado como variável importante de projeto e integridade operacional.

### 7.4 Limite de aplicação direta
Os exemplos disponíveis referem-se principalmente a ESDV e válvulas submarinas de isolamento, não a todas as válvulas de ANM/manifold. Ainda assim, o princípio de monitorar pressão de atuação ao longo do ciclo é tecnicamente útil como abordagem diagnóstica para outros conjuntos atuador-válvula subsea, desde que respeitadas as diferenças de projeto.

_Fontes da seção: regis-4dbb08942c491bcd76dc7960:pNone:455.60-495.0_

## 8. Critérios de decisão de engenharia e operação
Com base nos materiais, alguns critérios de decisão se destacam para projeto, operação e troubleshooting:

### 8.1 Quando priorizar simplicidade e facilidade de troubleshooting
O controle hidráulico direto tende a ser preferível quando a simplicidade, a facilidade de entendimento e a facilidade de localizar falhas são mais importantes que compactação de umbilical e rapidez de resposta.

### 8.2 Quando priorizar desempenho e escalabilidade
Arquiteturas pilotadas e multiplexadas são favorecidas quando se busca:

- redução de peso e complexidade física do umbilical;
- maior número de funções controladas;
- possibilidade de redundância;
- melhor resposta dinâmica;
- automação mais sofisticada.

### 8.3 Quando suspeitar de problema de integridade de linha e não de válvula
Em válvulas fail-safe close, uma perda de pressão no circuito de controle pode fechar a válvula mesmo que o elemento mecânico esteja íntegro. Portanto, um shutdown espúrio deve levar a verificar o circuito hidráulico, e não apenas o corpo/obturador da válvula.

### 8.4 Quando uma falha tende a ser local ou sistêmica
- **Falha isolada em sistema direto**: maior probabilidade de defeito local na linha ou função específica.
- **Falha múltipla em sistema multiplexado**: maior probabilidade de defeito comum em alimentação, comunicação ou SCM.
- **Falha em grupo de poços ligados ao mesmo manifold/SCM**: investigar primeiro a camada compartilhada.

### 8.5 Tempo de resposta como requisito de segurança
O material enfatiza que o sistema deve responder corretamente e no tempo especificado para shutdown. Logo, resposta lenta não é apenas questão de performance; pode ser também **questão de segurança funcional e de conformidade de projeto**.

_Fontes da seção: regis-9d017883010dd907fdb51652:pNone:188.0-212.0; regis-9d017883010dd907fdb51652:pNone:199.0-224.0; petroles-004c2afadba7ea17c7dd7908:pNone:2972565.0-2972611.0; regis-4dbb08942c491bcd76dc7960:pNone:455.60-495.0_

## 9. Aplicações operacionais diretamente sustentadas pelos trechos
Os materiais permitem sustentar, no mínimo, as seguintes leituras operacionais:

- entender a cadeia de comando e feedback entre FPSO e equipamentos subsea;
- comparar arquiteturas de controle segundo tempo de resposta, redundância, peso do umbilical e complexidade diagnóstica;
- reconhecer o impacto de vazamentos hidráulicos sobre válvulas fail-safe close;
- usar sintomas de campo para diferenciar falha de linha, falha de módulo submarino, falha de comunicação e aumento de atrito mecânico;
- interpretar a localização do SCM, especialmente quando associado a manifold, como fator decisivo para localizar falhas e planejar intervenção.

_Fontes da seção: regis-9d017883010dd907fdb51652:pNone:188.0-212.0; regis-9d017883010dd907fdb51652:pNone:199.0-224.0; petroles-004c2afadba7ea17c7dd7908:pNone:2972538.0-2972588.0; petroles-004c2afadba7ea17c7dd7908:pNone:2972565.0-2972611.0; regis-4dbb08942c491bcd76dc7960:pNone:455.60-495.0_