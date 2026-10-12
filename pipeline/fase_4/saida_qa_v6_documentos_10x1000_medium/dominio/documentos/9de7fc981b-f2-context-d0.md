# Operação do sistema de alívio em FPSO

## 1. Finalidade e posição do sistema de alívio na operação do FPSO
O sistema de alívio existe para impedir que equipamentos e linhas operem acima dos limites seguros de pressão quando as demais camadas de proteção não conseguem conter o desvio. Na literatura fornecida, as válvulas de segurança e/ou alívio são tratadas como a última camada de prevenção de acidentes por sobrepressão, atuando quando controle, alarmes, intervenção operacional e intertravamentos não foram suficientes. Em termos práticos de operação, isso significa que a atuação de uma PSV/PSRV não deve ser vista como condição normal desejada do processo, mas como resposta de proteção a uma condição anormal ou de emergência.  

Se a sobrepressão não for aliviada adequadamente, pode ocorrer ruptura de vasos, tubulações e conexões, com liberação de inventário inflamável ou tóxico. As consequências potenciais incluem incêndios, explosões de nuvem de vapor e, em cenários específicos de líquidos acima do ponto de ebulição à pressão atmosférica, BLEVE. Portanto, operar o sistema de alívio não é apenas “abrir uma válvula de proteção”, mas garantir que toda a rota de descarte posterior consiga receber, separar, conduzir e queimar ou dispersar o efluente de forma segura.  

**Fontes:** `petroles-004c2afadba7ea17c7dd7908:pNone:4273951.0-4274006.0`, `petroles-004c2afadba7ea17c7dd7908:pNone:4274127.0-4274164.0`, `regis-19e018d6d806ef2ee68d7882:pNone:1799.0-2049.0`

## 2. Terminologia essencial para a operação
Para interpretar corretamente eventos de alívio, os termos mais importantes são:

- **Pressão de ajuste (set pressure):** pressão manométrica na qual a PSV é ajustada para abrir em condição anormal.
- **Sobrepressão (overpressure):** incremento de pressão acima da pressão de ajuste durante a descarga.
- **Pressão de alívio:** soma da pressão de ajuste com a sobrepressão; representa a pressão máxima a que o equipamento pode ficar submetido durante o alívio.
- **Blowdown:** diferença entre a pressão de ajuste e a pressão de fechamento da válvula, usualmente expressa como percentual da pressão de ajuste.
- **Contrapressão superimposta:** pressão estática existente na saída da PSV imediatamente antes da abertura, originada no sistema de descarga.
- **Contrapressão desenvolvida:** aumento de pressão na saída da PSV causado pelo próprio escoamento de alívio após a abertura.
- **Contrapressão total (backpressure):** soma da contrapressão superimposta com a contrapressão desenvolvida.

Do ponto de vista operacional, a contrapressão é crítica porque influencia diretamente o comportamento da válvula e a capacidade efetiva de descarte. Um aumento indevido de pressão no header de flare, em vasos de separação do sistema de flare ou nas linhas de descarga pode alterar o desempenho da PSV e, dependendo do tipo construtivo, modificar a pressão efetiva de abertura ou a estabilidade do alívio.  

**Relações explícitas presentes nas fontes:**

- **Pressão de alívio = pressão de ajuste + sobrepressão**
- **Contrapressão total = contrapressão superimposta + contrapressão desenvolvida**

**Fontes:** `petroles-004c2afadba7ea17c7dd7908:pNone:4274165.0-4274196.0`, `regis-350bcc2de3ebad0b293b5ed6:pNone:21.0-86.0`

## 3. Tipos de válvulas e implicações operacionais
As fontes distinguem três comportamentos funcionais principais:

- **Válvula de alívio:** associada principalmente a serviço com líquidos; a abertura é proporcional ao aumento de pressão acima do ajuste.
- **Válvula de segurança:** associada a fluidos compressíveis, como gases e vapores; a abertura é rápida/instantânea.
- **Válvula de segurança e alívio:** pode atender serviço com líquidos e com gases, conforme a construção.

Quanto ao efeito da contrapressão, aparecem três classes relevantes:

1. **Convencional:** seu desempenho é diretamente afetado pela contrapressão. Em operação, isso exige maior atenção à pressão do sistema de descarga.
2. **Balanceada:** incorpora meios para reduzir o efeito da contrapressão, como fole ou pistão. Nas fontes, também aparece como opção útil quando a contrapressão é variável.
3. **Piloto-operada:** utiliza uma válvula piloto e uma válvula principal; ao atingir a pressão de ajuste, o piloto altera o balanço de pressões no pistão e promove a abertura da válvula principal.

Para a operação do FPSO, a consequência prática é que o comportamento esperado durante um evento de alívio depende não apenas da pressão a montante, mas também da configuração da válvula e das condições reais na descarga. Em headers com contrapressão variável, a escolha do tipo de PSV interfere na confiabilidade da resposta.  

**Fontes:** `petroles-004c2afadba7ea17c7dd7908:pNone:4274165.0-4274196.0`, `regis-350bcc2de3ebad0b293b5ed6:pNone:21.0-86.0`

## 4. Rota de descarte seguro em um FPSO: flare, vent e manejo de líquido
No material fornecido há um arranjo típico de plataforma/FPSO com:

- **dois sistemas independentes de flare:** um de **alta pressão (HP)** e outro de **baixa pressão (LP)**;
- coleta de gases excedentes oriundos de **válvulas de segurança**, **válvulas de controle de pressão** e **válvulas de despressurização**;
- **vasos de separação** no sistema de flare para remover líquido arrastado;
- envio do **líquido separado** para o **vaso de slop**;
- flare LP do tipo **multiqueimadores de baixa radiação**, com **gás de assistência** e **dois estágios**;
- flare HP do tipo **sônico**, com **três estágios**;
- **controle de seleção de estágios** para adequar a queima às condições de pressão e vazão;
- **cilindros de propano** para alimentar os **pilotos do flare** durante partida e em emergência;
- **dois sistemas de vent** para gases próximos à pressão atmosférica, descarregando em local seguro, afastado da área de radiação intensa do flare, para evitar autoignição e dispersão dos gases sobre a plataforma.

Esse arranjo mostra que a segurança do alívio depende do conjunto completo, não só da PSV. O descarte seguro exige, em sequência:

1. detecção/ocorrência da sobrepressão;
2. abertura da PSV ou dispositivo equivalente;
3. encaminhamento ao sistema correto de flare/vent;
4. separação de líquido arrastado;
5. drenagem desse líquido ao sistema apropriado, como slop;
6. manutenção de piloto, assistência de gás e configuração de estágios capazes de sustentar a queima;
7. liberação de correntes de baixa pressão para vent apenas quando essa for a rota prevista.

Operacionalmente, falhas em qualquer etapa podem transformar um evento de proteção em evento de perda de contenção ou queima inadequada.  

**Fontes:** `petroles-004c2afadba7ea17c7dd7908:pNone:388705.0-388733.0`, `regis-19e018d6d806ef2ee68d7882:pNone:1799.0-2049.0`

## 5. Condições normais e anormais de operação
### 5.1 Condição normal
Em condição normal, a PSV permanece fechada e o processo é mantido pelas malhas de controle. Ainda assim, o sistema de flare pode receber correntes de controle de pressão e descargas associadas a manobras de despressurização, conforme o arranjo descrito para a plataforma. Isso significa que, mesmo sem atuação de PSV por emergência, o sistema de descarte precisa permanecer disponível, com rota livre, piloto confiável e remoção de líquidos funcional.  

### 5.2 Condições anormais e de emergência
As fontes citam ou permitem reconhecer cenários como:

- falhas de controle e de intervenção operacional que levem à sobrepressão;
- erros operacionais, inclusive abertura inadvertida de válvulas em estudos de caso de processo;
- eventos de fogo, que podem alterar a sobrepressão admissível de projeto conforme a filosofia adotada;
- despressurizações de emergência;
- aumento de contrapressão no sistema de descarga;
- presença de líquido na corrente de alívio.

A presença de líquido é especialmente importante. Um dos estudos citados observou por simulação dinâmica a existência de líquido na vazão de alívio, embora o cálculo convencional estivesse considerando apenas vapor. Isso foi descrito como conservativo para a área da PSV, mas não necessariamente conservativo para o equipamento a jusante do alívio, como vaso de blowdown ou sistema de flare, que pode receber carga líquida relevante. Para a operação do FPSO, isso reforça a necessidade de tratar separação de líquidos, níveis nos vasos do flare e destino ao slop como parte integrante da resposta ao evento.  

**Fontes:** `petroles-004c2afadba7ea17c7dd7908:pNone:4274856.0-4274980.0`, `petroles-004c2afadba7ea17c7dd7908:pNone:388705.0-388733.0`, `petroles-004c2afadba7ea17c7dd7908:pNone:4273951.0-4274006.0`

## 6. Capacidade de alívio, regime de escoamento e variáveis relevantes
O material informa que o dimensionamento da PSV depende da definição da pressão de ajuste e da determinação, para cada cenário de sobrepressão, da vazão de alívio e das propriedades do fluido nas condições de alívio. A área requerida é então comparada com áreas padronizadas de orifício.

Para **gás e vapor**, as equações se dividem conforme o escoamento seja **crítico** ou **subcrítico**. O conjunto de variáveis explicitamente listado nas fontes inclui, entre outras:

- vazão de alívio requerida (**W**);
- pressão de alívio e contrapressão (**P1**, **P2**);
- temperatura de alívio (**T**);
- fator de compressibilidade (**Z**);
- peso molecular (**M**);
- razão de calores específicos (**k = Cp/Cv**);
- coeficientes/correções de descarga e instalação (**Kd**, **Kc**);
- correções por contrapressão (**Kb** para gás/vapor, **Kw** para líquido);
- correção por viscosidade (**Kv**).

Do ponto de vista operacional, isso se traduz em um princípio simples: a capacidade real do sistema de alívio depende do fluido, da fase, da contrapressão e da hidráulica do sistema de descarga, não apenas do valor nominal da PSV.  

**Fontes:** `petroles-004c2afadba7ea17c7dd7908:pNone:4274165.0-4274196.0`, `petroles-004c2afadba7ea17c7dd7908:pNone:4273951.0-4274006.0`, `regis-350bcc2de3ebad0b293b5ed6:pNone:21.0-86.0`

## 7. Fenômenos operacionais relevantes: contrapressão, superdimensionamento e chatter
As fontes alertam que a ideia de que uma PSV superdimensionada é sempre inofensiva é inadequada. Uma válvula muito grande para a vazão efetivamente aliviada pode entrar em **chatter**, isto é, ciclos rápidos de abertura e fechamento. Esse comportamento é indesejável porque pode danificar a válvula e comprometer sua função protetiva.

Além disso, a contrapressão participa do balanço de forças na PSV. Portanto:

- contrapressão elevada pode degradar o desempenho de válvulas convencionais;
- cabeçalho de flare congestionado ou com hidráulica desfavorável pode alterar a resposta do sistema;
- presença de líquido a jusante ou na própria corrente de alívio pode afetar não só a válvula, mas a separação e o manejo no flare/slop.

Em termos operacionais, uma atuação de PSV não deve ser analisada somente pelo pico de pressão a montante. Também devem ser avaliados estabilidade da válvula, comportamento do header de flare, ocorrência de arraste de líquido e desempenho do sistema de descarte.  

**Fontes:** `petroles-004c2afadba7ea17c7dd7908:pNone:4273951.0-4274006.0`, `petroles-004c2afadba7ea17c7dd7908:pNone:4274856.0-4274980.0`, `petroles-004c2afadba7ea17c7dd7908:pNone:4274165.0-4274196.0`

## 8. Simulação dinâmica como apoio à operação e à análise de risco
As fontes apresentam a **simulação dinâmica** como ferramenta útil para:

- complemento de estudos de **HAZOP**;
- suporte a **partidas**;
- **sintonia de controladores**;
- avaliação de **cenários operacionais** e de **emergência**;
- avaliação de **PSVs existentes** e de **sistemas de flare**, especialmente em revamps ou aumento de capacidade.

O valor operacional dessa abordagem é permitir observar a evolução temporal do evento, incluindo variação de pressão, resposta das malhas de controle, surgimento de condições bifásicas e carga efetiva ao flare. Um resultado particularmente importante das fontes é que a simulação pode revelar aspectos não capturados por métodos convencionais simplificados, como a presença de líquido na descarga.

Ao mesmo tempo, o próprio material ressalta uma limitação: não foi identificado, naquele levantamento, uso consolidado da simulação dinâmica como ferramenta única para dimensionamento de PSV na etapa de projeto básico. Portanto, para operação de FPSO, a simulação deve ser entendida como **ferramenta complementar de análise e decisão**, e não como substituto automático de critérios normativos, dados de fabricante e verificações de engenharia do sistema de alívio.  

**Fontes:** `petroles-004c2afadba7ea17c7dd7908:pNone:4274127.0-4274164.0`, `petroles-004c2afadba7ea17c7dd7908:pNone:4274856.0-4274980.0`

## 9. Implicações práticas para a operação do FPSO
Com base no material fornecido, uma operação robusta do sistema de alívio envolve, no mínimo:

- manter disponibilidade da rota correta de **flare HP**, **flare LP** e **vent**;
- assegurar que a descarga de alívio chegue a local seguro e compatível com sua pressão e natureza;
- verificar condições de **piloto**, suprimento de ignição de contingência e assistência ao flare;
- acompanhar separação de líquido e remoção para **slop**;
- reconhecer que atuação frequente de PSV indica desvio operacional, problema de controle ou restrição a jusante;
- tratar aumento de contrapressão como risco funcional para o dispositivo de proteção;
- considerar que alívios com líquido ou bifásicos impõem exigências adicionais ao sistema a jusante;
- usar dados históricos, análise de eventos e, quando aplicável, simulação dinâmica para revisar gargalos do flare e condições de instabilidade da PSV.

Em síntese, a operação do sistema de alívio em FPSO deve ser vista como gestão integrada de **sobrepressão + rota de descarte + queima/vent segura + manejo de líquido + integridade do dispositivo**.  

**Fontes:** `petroles-004c2afadba7ea17c7dd7908:pNone:388705.0-388733.0`, `petroles-004c2afadba7ea17c7dd7908:pNone:4274165.0-4274196.0`, `petroles-004c2afadba7ea17c7dd7908:pNone:4274856.0-4274980.0`, `petroles-004c2afadba7ea17c7dd7908:pNone:4274127.0-4274164.0`, `regis-19e018d6d806ef2ee68d7882:pNone:1799.0-2049.0`