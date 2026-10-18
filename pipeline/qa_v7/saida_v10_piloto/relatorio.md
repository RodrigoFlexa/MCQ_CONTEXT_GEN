# QA v7 (cota): perguntas a partir do inventário

Gerador gpt-5-4-petrobras:low, juiz gpt-5-4-petrobras:low. 30 questões geradas, 11 aprovadas (37%). Tempo 2.8 min. Chamadas 126, tokens de entrada 809,565, de saída 87,364.

O nível é o tipo pedido ao gerador (sem avaliador de dificuldade no loop).

| Tipo | geradas | aprovadas | corrigidas |
|---|---:|---:|---:|
| facil | 12 | 3 | 4 |
| media | 11 | 5 | 2 |
| dificil_A | 2 | 0 | 1 |
| dificil_B | 5 | 3 | 1 |

Motivos de reprovação: suporte (7), codigo:pergunta_longa (6), sem_pista (3), codigo:depende_do_material (2), codigo:resposta_longa (1), codigo:explicacao_longa (1), correcao_tecnica (1), sem_generalizacao (1), escopo (1)
Lotes com falha ou filtro de conteúdo: 0
Pendentes de validação cega: 0
Alvos descartados na triagem (genéricos): 0; recortados: 0

Respondente às cegas nas aprovadas (desempenho do modelo; não mede dificuldade humana):

| Tipo | equivalente | parcial | incorreta |
|---|---:|---:|---:|
| facil | 1 | 2 | 0 |
| media | 5 | 0 | 0 |
| dificil_A | 0 | 0 | 0 |
| dificil_B | 2 | 1 | 0 |

## Por subtópico

| Tópico | Subtópico | cota | geradas | aprovadas | redundantes (novidade) |
|---|---|---:|---:|---:|---:|
| Produção e Processo (Medição Fiscal e Si | Operação de Separadores Trifásicos | 10 | 12 | 4 | 4 |
| Segurança Operacional, SGSO, Sistemas de | SGSO | 10 | 14 | 5 | 2 |
| Sistemas de Lastro, Estabilidade, Ancora | Operação de tanques de carga, lastro, sistema gás  | 10 | 4 | 2 | 0 |

## Curva de novidade (aprovadas na ordem da fila, janelas de 20)

### Produção e Processo (Medição Fiscal e Sistema de Alívio)

| aprovadas | redundantes | fração |
|---|---:|---:|
| 1 a 4 | 0 | 0% |

### Segurança Operacional, SGSO, Sistemas de Segurança e Gestão de Riscos

| aprovadas | redundantes | fração |
|---|---:|---:|
| 1 a 5 | 0 | 0% |

### Sistemas de Lastro, Estabilidade, Ancoragem e Posicionamento, Offloading e Tanques de Carga

| aprovadas | redundantes | fração |
|---|---:|---:|
| 1 a 2 | 0 | 0% |

## Questões

### Produção e Processo (Medição Fiscal e Sistema de Alívio)

#### Operação de Separadores Trifásicos

**facil · REPROVADA: suporte**  
_Nota(s): Princípios físicos e mecanismos internos de separação em separadores trifásicos_

**P:** Em um separador trifásico típico de produção, descreva como a separação de gás, óleo e água ocorre ao longo do vaso, relacionando cada seção funcional ao mecanismo físico predominante e à posição no equipamento.

**R:** Na entrada, defletor ou difusor provoca desaceleração e mudança de direção, promovendo separação inercial gás-líquido. Na seção de acumulação, com menor turbulência e retenção, gravidade e diferença de densidade estratificam: gás no topo, água no fundo e óleo acima da água. No topo, a separação secundária decanta gotas ainda arrastadas pelo gás. Perto da saída de gás, meio poroso/extrator de névoa aglutina ou coalesce gotículas finas para recuperá-las.

_Explicação:_ A sequência correta combina mecanismos complementares. Primeiro, a entrada promove separação inercial entre gás e líquido. Depois, a zona líquida mais calma permite a ação gravitacional e a estratificação entre água e óleo. Na parte superior, gotas maiores ainda presentes no gás podem decantar. Por fim, gotículas finas remanescentes são removidas por aglutinação/coalescência em meios porosos ou extratores, antes da saída do gás.

**media · APROVADA**  
_Nota(s): Segregação óleo-água e limites funcionais da interface em separador trifásico_

**P:** Em um separador trifásico com defletor ou ciclone na entrada, região superior de gás e placas paralelas na câmara líquida, compare o papel desses internos na separação. Distinga o que cada grupo faz na entrada, no topo e na região líquida, sem confundir redução de arraste no gás com separação óleo-água.

**R:** Na entrada, defletor/difusor/ciclone promovem a separação primária gás-líquido ao desacelerar e desviar o escoamento. No topo, a separação secundária reduz o líquido carreado pelo gás por decantação. Na câmara líquida, placas paralelas auxiliam a separação óleo-água. Esses internos melhoram o condicionamento do escoamento, mas a segregação líquido-líquido continua dependente de gravidade e tempo de retenção.

_Explicação:_ Os fatos distinguem três funções no vaso: na entrada, internos como defletor ou ciclone retiram a maior parte do gás da fase líquida e preparam o escoamento; no topo, a separação secundária diminui o líquido carreado pela corrente gasosa; na região líquida, placas paralelas favorecem a separação entre fase predominantemente oleosa e aquosa. Portanto, reduzir arraste no gás não é o mesmo que controlar a interface ou separar óleo-água.

_Às cegas (equivalente):_ Entrada (defletor/ciclone): promove separação primária por mudança brusca de direção/centrifugação, retirando parte do líquido e reduzindo energia/turbulência antes da zona de calma. Topo (região de gás): volume para desengotamento; internos tipo demister/coalescedor (se existirem) retêm gotículas e reduzem arraste de líquido no gás—não separam óleo/água. Região líquida (placas paralelas): aumentam área e encurtam caminho de subida/decantação, favorecendo coalescência e separação óleo-água/clarificação.

**dificil_A · REPROVADA: codigo:depende_do_material · corrigida**  
_Nota(s): Segregação óleo-água e limites funcionais da interface em separador trifásico_

**P:** Em um separador trifásico de produção, com seção de acumulação inferior, controle de interface óleo-água e saída de água pelo fundo, discute-se operar a interface no extremo alto ou no extremo baixo para ganhar folga em outras variáveis. Sem adotar setpoint numérico e admitindo a possibilidade de emulsão na interface, justifique por que essa interface não deve ser operada arbitrariamente em nenhum desses extremos.

**R:** A interface deve permanecer na faixa funcional da seção de acumulação. Se subir demais, reduz o volume útil da camada oleosa e a folga para manter separação líquido-líquido estável. Se baixar demais, reduz a camada aquosa inferior necessária para retirar água livre pelo fundo com seletividade. Emulsões na interface ainda dificultam o controle e consomem volume útil. Não há valor numérico universal nas fontes.

_Explicação:_ No separador trifásico, a água livre se acumula no fundo e sua retirada ocorre pela saída inferior controlada pela interface. Por isso, a interface não deve descer a ponto de reduzir a camada aquosa necessária à retirada seletiva de água. Também não deve subir em excesso, porque reduz a região útil da fase oleosa e a folga para manter a separação líquido-líquido estável. Se houver emulsão na interface, o controle fica mais difícil e parte do volume útil é consumida. As fontes não fornecem limite geométrico nem valor numérico universal para essa posição.

**media · APROVADA**  
_Nota(s): Influência da vazão e da estabilidade de alimentação na eficiência do separador trifásico_

**P:** Em um FPSO, um separador trifásico recebe a soma das correntes de vários poços controlados por choke a montante. Durante a operação, ocorre um aumento súbito de produção de óleo, com oscilação rápida da alimentação. Quais consequências operacionais devem ser esperadas no separador quanto aos níveis, à qualidade da separação e ao risco operacional, e que prioridade de controle se torna mais adequada nesse contexto?

**R:** A mudança brusca de carga tende a desestabilizar níveis e demais variáveis internas, piorando a separação. Pode ocorrer arraste de óleo na corrente de gás e aumento do risco de nível muito alto, com possibilidade de parada de emergência. Por isso, o controle deve priorizar reduzir as oscilações da alimentação ao longo da planta, não apenas corrigir localmente o nível do separador.

_Explicação:_ A documentação indica que variações bruscas de produção degradam a separação e podem causar arraste de óleo na corrente de gás, além de elevar o nível do separador até condição de risco operacional. Como a alimentação depende do conjunto de poços e dos chokes a montante, o controle eficaz não se limita ao vaso; deve buscar atenuar oscilações que afetam pressão, interfaces, temperatura e qualidade de separação.

_Às cegas (equivalente):_ Oscilação rápida e aumento de óleo tendem a causar hunting dos níveis (óleo/água) e variações de pressão/espuma, com risco de carry-over de líquido ao gás e/ou carry-under de gás ao líquido, piorando BS&W/óleo na água e estabilidade. A sobrecarga reduz tempo de residência, aumentando arraste e acionamento de PSV/trips por HH/LL level. Prioridade de controle mais adequada: manter inventário/nível (override de alta) e pressão do vaso, com desacoplamento/filtragem do nível; choke a montante deve suavizar a vazão.

**facil · DESCARTADA (repete outra aprovada) · REDUNDANTE**  
_Nota(s): Seção de entrada do separador trifásico: como defletores, difusores e ciclones iniciam a separação por impacto, inércia e gravidade_

**P:** Em um separador trifásico de produção em FPSO/FSO, a corrente mista gás-líquido entra no vaso por uma seção com interno de entrada, como placa defletora ou difusor. Como essa seção inicia a separação gás-líquido dentro do vaso?

**R:** Na entrada, o interno provoca choque, desaceleração e mudança brusca de direção do escoamento, iniciando a separação inercial. Com isso, o líquido é lançado para o fundo do vaso, onde a gravidade sustenta sua acumulação inicial, enquanto o gás tende a seguir para a região superior.

_Explicação:_ A nota documenta que a separação primária ocorre na entrada do separador. Nessa região, defletores ou difusores alteram bruscamente velocidade e direção da corrente, ou impõem movimento que favorece a separação inicial. O mecanismo central combina efeito inercial com gravidade: o líquido é deslocado para baixo e o gás permanece preferencialmente na parte superior, reduzindo a carga para as etapas posteriores.

_Às cegas (equivalente):_ A seção de entrada reduz a velocidade e dissipa o momento da corrente, promovendo mudança brusca de direção/impacto (placa) ou distribuição uniforme (difusor). Isso causa desimpingement/inércia: gotas líquidas coalescem e caem por gravidade, enquanto o gás, mais leve, desacopla e segue para a região de gás. Também reduz turbulência e evita re-entrainment, criando um escoamento mais calmo para a separação subsequente.

**dificil_B · APROVADA**  
_Nota(s): Influência da vazão e da estabilidade de alimentação na eficiência do separador trifásico; Seção de entrada do separador trifásico: como defletores, difusores e ciclones iniciam a separação por impacto, inércia e gravidade; Princípios físicos e mecanismos internos de separação em separadores trifásicos_

**P:** Em um FPSO, vários poços alimentam o mesmo separador trifásico e a contribuição a montante muda bruscamente após ajuste de choke, sem evidência informada de falha mecânica dos internos. O separador possui seção de entrada com interno de separação primária e, no topo, região de separação secundária e remoção de névoa. Explique como essa perturbação pode levar a piora da qualidade do gás de saída por carreamento de líquido.

**R:** A mudança brusca de carga quebra a alimentação regular, reduzindo a estabilidade de nível e da circulação de gás e, com isso, a eficiência global. Na entrada, a separação primária por choque, mudança de direção/velocidade, inércia e gravidade remove menos líquido. Esse excedente sobrecarrega acumulação, separação secundária e extrator de névoa, aumentando a probabilidade de líquido arrastado na corrente de gás.

_Explicação:_ A vazão de entrada depende do somatório dos poços e dos chokes a montante. Fluxo regular favorece nível de óleo e circulação de gás estáveis; oscilações desestabilizam variáveis de qualidade. Na entrada, defletores/difusores/ciclones fazem a pré-separação rápida do líquido. Se essa etapa perde efetividade durante o surto, sobra mais líquido para as seções seguintes. A região de topo passa a receber mais gotas arrastadas, elevando a chance de líquido sair com o gás.

_Às cegas (equivalente):_ A mudança brusca de contribuição dos poços pode gerar slug/onda de líquido e aumento repentino de vazão/velocidade de gás na entrada. Isso reduz tempo de residência e eficiência da separação primária, eleva turbulência e re-entrainment, carrega gotículas para a zona superior e pode sobrecarregar/inundar o demister (maior ΔP), reduzindo sua captura. Também pode causar espuma e variação de nível, permitindo arraste direto para a saída de gás.

**media · APROVADA**  
_Nota(s): Princípios físicos e mecanismos internos de separação em separadores trifásicos_

**P:** Em vasos de separação de produção que recebem mistura com gás, óleo e água, compare conceitualmente o separador bifásico com o trifásico quanto ao princípio de funcionamento. Destaque o que o trifásico precisa acrescentar, em termos de região líquida e internos, para separar óleo e água dentro do mesmo vaso.

**R:** O bifásico separa gás do líquido total pelos mesmos mecanismos básicos de inércia na entrada e gravidade/diferença de densidade no vaso. O trifásico acrescenta uma seção líquida mais desenvolvida, com retenção para estratificação, mantendo água no fundo e óleo acima, além de poder usar internos voltados à separação líquido-líquido, como placas paralelas.

_Explicação:_ Os mecanismos centrais de separação gás-líquido permanecem os mesmos nos dois vasos: mudança de velocidade/direção na entrada e ação da gravidade com diferença de densidade. A diferença funcional do trifásico é criar condições úteis para separar também os dois líquidos, com região de acumulação mais favorável à formação de interface água-óleo e, quando aplicável, internos específicos que apoiem essa etapa.

_Às cegas (equivalente):_ Bifásico: separa gás do líquido; usa zona de gás (desengajamento), extrator de névoa e zona líquida com tempo de residência/placas para reduzir arraste.
Trifásico: além disso, precisa promover decantação óleo–água no mesmo vaso: região líquida “dupla” com zona de separação gravitacional, controle de interface (nível óleo e nível água), vertedouro/weir e/ou bucket, bota (boot) ou compartimento para água, e internos de coalescência/placas para acelerar a separação.

**dificil_B · REPROVADA: suporte, codigo:pergunta_longa, codigo:resposta_longa, codigo:explicacao_longa · corrigida**  
_Nota(s): Influência da vazão e da estabilidade de alimentação na eficiência do separador trifásico; Segregação óleo-água e limites funcionais da interface em separador trifásico_

**P:** Em um FPSO, um separador trifásico em operação monitora pressão interna, nível óleo-gás, nível/interface óleo-água e temperatura de entrada. Após redistribuição de contribuição entre poços alinhados ao mesmo header, passam a ocorrer oscilações de carga, maior variabilidade dos níveis internos, dificuldade de manter a interface óleo-água estável e episódios de indício de óleo na corrente de gás. Sem assumir falha de instrumentação e considerando, para a leitura integrada, apenas os sinais e sintomas deste cenário — carga de entrada, pressão interna, nível líquido, interface óleo-água, nível óleo-gás, temperatura de entrada e qualidade das correntes —, explique o encadeamento técnico mais provável.

**R:** A perturbação de carga a montante quebra a regularidade da alimentação, desestabilizando nível interno, circulação de gás e tempo de retenção. No trifásico, isso prejudica a segregação gravitacional óleo-água na seção de acumulação e desloca a interface da faixa funcional. Se houver emulsão na interface, o controle fica mais difícil e a retenção útil cai ainda mais. A leitura integrada deve considerar vazão/carga de entrada, pressão, nível líquido, interface óleo-água, nível óleo-gás, temperatura e qualidade das correntes, inclusive indício de óleo no gás.

_Explicação:_ A correção estreita a segunda parte do enunciado para evitar múltiplas listas igualmente válidas de variáveis. Em vez de pedir genericamente quais variáveis devem ser lidas de forma integrada, a pergunta passa a limitar essa leitura aos sinais e sintomas já delimitados no próprio cenário. Assim, a resposta continua exigindo a integração entre causa a montante e mecanismo interno do trifásico: a redistribuição de carga entre poços pode quebrar a regularidade da alimentação ao separador; isso desestabiliza variáveis internas relevantes à eficiência, como nível, circulação de gás e tempo de retenção. Como a separação óleo-água no trifásico depende de retenção gravitacional na seção de acumulação, a perda dessa estabilidade prejudica a estratificação. Se houver emulsão na interface, o controle fica mais difícil e a retenção útil diminui, o que ajuda a explicar a piora simultânea da interface, da qualidade das fases e o indício de óleo na corrente gasosa.

**facil · DESCARTADA (repete outra aprovada) · REDUNDANTE**  
_Nota(s): Segregação óleo-água e limites funcionais da interface em separador trifásico_

**P:** Em um separador trifásico de produção, o líquido permanece por algum tempo na seção de acumulação no fundo do vaso após a separação inicial do gás. Como se forma a camada de água no fundo e a camada oleosa acima nessa condição?

**R:** A estratificação ocorre por diferença de densidade sob ação da gravidade durante o tempo de retenção na seção de acumulação. Nesse período, a água decanta e fica na parte inferior, enquanto a fase oleosa permanece acima; o mesmo tempo também ajuda a liberar gás remanescente do líquido.

_Explicação:_ O mecanismo documentado para a separação óleo-água no trifásico é gravitacional, não dependente apenas de válvula ou pressão. Com líquido retido na seção de acumulação, a diferença de densidade permite a decantação da água para o fundo e a permanência da fase oleosa acima. Esse tempo de residência também contribui para desprender o gás remanescente ainda contido no líquido.

_Às cegas (equivalente):_ Após a separação inicial do gás, o líquido (óleo+água) fica em repouso relativo na seção de acumulação. Pela diferença de densidade e imiscibilidade, ocorre decantação gravitacional: gotas de água coalescem e sedimentam, formando uma camada aquosa no fundo; o óleo, menos denso, sobe e forma a camada oleosa acima. O tempo de residência favorece coalescência e a quebra parcial de emulsões, definindo uma interface.

**media · REPROVADA: suporte**  
_Nota(s): Seção de entrada do separador trifásico: como defletores, difusores e ciclones iniciam a separação por impacto, inércia e gravidade_

**P:** Na separação primária, na entrada de um separador trifásico, compare o papel de placa defletora, difusor e ciclone como internos de entrada. Indique como cada um atua sobre o escoamento e qual objetivo comum eles atendem, sem discutir qual é o melhor nem desempenho numérico.

**R:** A placa defletora atua pelo choque da corrente, com forte desaceleração e mudança brusca de direção. O difusor também altera o escoamento e pode impor movimento giratório. O ciclone, quando usado nessa etapa, trabalha com escoamento rotacional. Nos três casos, o objetivo comum é promover a separação inicial gás-líquido na entrada, deslocando rapidamente líquido para o fundo do vaso.

_Explicação:_ O material sustenta que a separação primária ocorre na entrada do vaso. A placa defletora promove choque, desaceleração e mudança de direção; o difusor pode impor rotação; e ciclones também podem compor essa etapa. Apesar das diferenças de atuação sobre o escoamento, todos servem para retirar rapidamente parte do líquido da corrente gasosa e enviá-lo ao fundo do vaso. Não há base aqui para comparar desempenho quantitativo ou escolher um interno como universalmente superior.

**facil · DESCARTADA (repete outra aprovada) · REDUNDANTE**  
_Nota(s): Influência da vazão e da estabilidade de alimentação na eficiência do separador trifásico_

**P:** Em um FPSO, um separador trifásico de produção pode operar recebendo alimentação mais regular ou com oscilações de vazão e mudanças bruscas de carga. Como essa regularidade da alimentação influencia a eficiência de separação?

**R:** A alimentação regular favorece a eficiência porque ajuda a manter estáveis variáveis que influenciam a separação, como tempo de residência, pressão e temperatura, além do nível de óleo e da circulação de gás. Já oscilações de vazão ou mudanças bruscas de carga desestabilizam essas condições internas e tendem a piorar a separação.

_Explicação:_ O material afirma que a qualidade da separação depende de variáveis como tempo de residência, temperatura e pressão, e que oscilações de vazão as desestabilizam. Também afirma que, com fluxo regular, o separador mantém estáveis o nível de óleo e a circulação de gás, condição associada à máxima eficiência. Logo, quando a alimentação perde regularidade, a eficiência tende a cair.

_Às cegas (equivalente):_ Alimentação mais regular tende a aumentar a eficiência do separador: mantém níveis e pressão estáveis, melhora o tempo de residência, reduz arraste de líquido no gás e de gás no líquido, e diminui turbulência/reentrainment, facilitando controle e demulsificação. Oscilações bruscas podem causar espuma, perturbar interfaces, saturar internals e válvulas, levando a off-spec (maior carryover/carryunder) e instabilidade operacional.

**media · DESCARTADA (repete outra aprovada) · REDUNDANTE**  
_Nota(s): Seção de entrada do separador trifásico: como defletores, difusores e ciclones iniciam a separação por impacto, inércia e gravidade_

**P:** Em um separador trifásico em operação normal, a corrente mista entra pela seção primária com internos de entrada, depois segue para a zona de acumulação, para a separação secundária e para a remoção de névoa. Se a separação primária passar a retirar menos líquido da corrente de entrada, qual é a consequência operacional esperada sobre as seções seguintes, sem assumir uma causa específica para essa perda de eficiência?

**R:** As seções seguintes passam a receber uma mistura menos pré-separada: mais líquido segue com o gás e mais gás remanescente pode permanecer no líquido acumulado. Isso aumenta a carga sobre a acumulação, a separação secundária e a remoção de névoa.

_Explicação:_ A separação primária existe para pré-separar gás e líquido antes das etapas posteriores. Se ela remove menos líquido na entrada, mais líquido é transferido adiante com a corrente gasosa e o líquido acumulado tende a chegar menos desgaseificado. Com isso, acumulação, separação secundária e extrator de névoa passam a trabalhar com maior demanda, sem que isso, por si só, indique a causa da perda de eficiência.

_Às cegas (equivalente):_ Menos remoção na primária aumenta o “carryover” de líquido para a zona de acumulação e a separação secundária, elevando carga hidráulica, turbulência e arraste. Espera-se tendência a nível mais alto/instável, menor eficiência de separação secundária e maior carga no removedor de névoa, com risco de inundação e maior líquido no gás (e/ou água/óleo fora de especificação nas saídas).

### Segurança Operacional, SGSO, Sistemas de Segurança e Gestão de Riscos

#### SGSO

**facil · REPROVADA: suporte**  
_Nota(s): Seleção e qualificação de contratadas no SGSO com base em risco, competência e capacidade técnica_

**P:** Em uma atividade terceirizada na instalação, por que a seleção da contratada no SGSO não deve se limitar a preço ou histórico comercial, especialmente quando o escopo pode afetar a segurança operacional e inclui pessoal e, às vezes, equipamentos próprios da contratada?

**R:** Porque, no SGSO, a seleção deve ser proporcional ao risco da atividade e considerar segurança operacional. Isso exige avaliar a competência e o treinamento do pessoal terceirizado e, quando a contratada usar meios próprios no escopo, também sua aptidão técnica e a integridade desses recursos.

_Explicação:_ O SGSO trata a contratação como controle prévio de segurança, não só como decisão comercial. Por isso, a robustez da qualificação deve acompanhar o risco da atividade. A avaliação inclui a capacidade do pessoal de executar o trabalho com segurança e, se o serviço depender de equipamentos ou recursos da contratada, também a condição desses meios, pois eles podem afetar diretamente a segurança operacional da instalação.

**media · APROVADA**  
_Nota(s): Definição de objetivos, metas e indicadores do SGSO_

**P:** No acompanhamento do desempenho de segurança operacional de uma instalação offshore pelo SGSO, qual é a diferença funcional entre indicadores pró-ativos e reativos, e por que os dois devem compor o conjunto de indicadores para avaliar a eficácia do sistema?

**R:** Os pró-ativos acompanham condições ou degradações que podem iniciar ou contribuir para acidentes; os reativos acompanham resultados ou eventos já ocorridos. No SGSO, ambos são necessários e complementares: só indicadores reativos mostram consequências já materializadas, enquanto os pró-ativos ajudam a identificar precursores e apoiar a prevenção.

_Explicação:_ O material do SGSO exige indicadores pró-ativos e reativos. Os pró-ativos servem para avaliar condições que possam dar início ou contribuir para acidentes operacionais; os reativos, por oposição técnica compatível com o texto, acompanham resultados ou eventos já ocorridos. A avaliação da eficácia do SGSO fica mais consistente quando combina sinais de degradação/precursores com evidências de consequências já materializadas.

_Às cegas (equivalente):_ Indicadores pró‑ativos (leading) medem condições/atividades que previnem eventos (ex.: conformidade de barreiras, inspeções, auditorias, ações corretivas no prazo); permitem intervenção antes do acidente. Indicadores reativos (lagging) medem resultados após falhas/eventos (ex.: incidentes, vazamentos, LTIs, perdas de contenção); confirmam consequências e tendências históricas. Ambos são necessários porque pró‑ativos avaliam robustez/controle do SGSO e reativos validam se isso se traduz em desempenho real, evitando cegueira por subnotificação ou por “conformidade” sem eficácia.

**dificil_A · REPROVADA: suporte, sem_pista, codigo:pergunta_longa**  
_Nota(s): Definição de objetivos, metas e indicadores do SGSO_

**P:** Em um FPSO, dois conjuntos de indicadores foram propostos para o SGSO. Conjunto X: combina indicadores pró-ativos e reativos com metas associadas, foi definido a partir dos principais riscos de acidente maior e dos controles/barreiras mais críticos, e cada indicador descreve o que mede, como o dado é coletado e tratado, quem é responsável e revisão periódica de relevância. Conjunto Y: também tem metas e mistura indicadores pró-ativos e reativos, mas foi montado pela repetição de indicadores históricos gerais, sem explicitar foco nos riscos principais, método de coleta/tratamento, responsáveis ou revisão regular. Qual conjunto está tecnicamente melhor estruturado para o SGSO, e por quê?

**R:** O conjunto X está melhor estruturado. Ele atende à base do SGSO com objetivos, metas e indicadores pró-ativos e reativos, e ainda usa seleção sistemática baseada em risco, focada nos controles/barreiras críticos. Além disso, define claramente medida, coleta, tratamento dos dados, responsabilidade e revisão periódica, o que sustenta utilidade e relevância do monitoramento.

_Explicação:_ Pelos requisitos do SGSO, o conjunto precisa servir à avaliação da eficácia do sistema e à melhoria contínua, com indicadores e metas monitoráveis. Como critério técnico complementar, o conjunto mais forte não é o que apenas repete histórico, mas o que deriva dos principais riscos e elementos críticos de controle. Sem definição clara de medida, coleta, tratamento, responsáveis e revisão regular, a utilidade técnica do conjunto fica mais fraca.

**media · REPROVADA: suporte · corrigida**  
_Nota(s): Programa de auditorias do SGSO: mecanismo formal de verificação da eficácia, conformidade e integração do sistema ao longo do ciclo operacional_

**P:** Em um FPSO com SGSO implementado e em operação, por que o programa de auditorias deve ser entendido como parte da estrutura de gestão do sistema, e não como atividade isolada, quando comparado funcionalmente a auditorias de programas correlatos de gerenciamento de risco?

**R:** O programa de auditorias integra a arquitetura do SGSO ao funcionar junto de monitoramento e melhoria contínua, gestão da informação/documentação e investigação de incidentes como mecanismo de verificação e retroalimentação do sistema. Em programas correlatos de risco, a auditoria também verifica conformidade e efetividade, o que mostra interface metodológica. Isso não torna esses programas normativamente idênticos nem altera a finalidade própria da auditoria no SGSO.

_Explicação:_ A correção retira a pista excessiva do enunciado: em vez de antecipar quais práticas do SGSO estão associadas à auditoria e qual é a função da auditoria em programas correlatos, a pergunta passa a exigir que o candidato mobilize esses elementos a partir do material. O núcleo técnico permanece o mesmo: no SGSO, auditoria é uma prática de gestão inserida na estrutura do sistema, ao lado de outras práticas de gestão, e sua comparação com programas correlatos de risco só se sustenta no plano funcional da verificação de conformidade e efetividade, sem equivalência normativa automática.

**facil · APROVADA · corrigida**  
_Nota(s): Integração de fatores humanos no ciclo de vida do projeto no SGSO_

**P:** No SGSO aplicado a FPSO/FSO, por que a integração de fatores humanos não pode ser tratada só como checagem documental ao fim do projeto? Responda com base no ciclo de vida da instalação e nas atividades centrais de engenharia de fatores humanos indicadas pela ANP.

**R:** Porque o SGSO exige considerar esses aspectos nas fases de projeto, construção, instalação e desativação, e a ANP indica o IOGP 454 como melhor prática desde a fase conceitual até a operação. Como a engenharia de fatores humanos atua sobre tarefas, sala de controle, HMI, alarmes e layout, ela muda decisões de engenharia e a interação operador-instalação, não só a documentação.

_Explicação:_ A resposta correta deve ligar dois pontos. Primeiro, no SGSO, códigos e padrões de ambiente de trabalho e fatores humanos precisam ser considerados nas fases de projeto, construção, instalação e desativação; além disso, a ANP aponta o IOGP 454 como melhor prática ao longo do projeto, da fase conceitual até a operação. Segundo, as atividades centrais de engenharia de fatores humanos incidem sobre tarefas, sala de controle, HMI, alarmes e layout. Por isso, o tema interfere em decisões de engenharia e na interação operador-instalação, em vez de se limitar a um registro documental ao final.

_Às cegas (parcial):_ Porque fatores humanos afetam decisões de concepção, construção/comissionamento, operação, manutenção e desativação. Se virar só “check” documental no fim, não corrige: layout, acessos, HMI/controle, alarmes, tarefas críticas, carga de trabalho, interfaces organização–tecnologia e requisitos de treinamento/procedimentos; nessa fase, mudanças são caras/impraticáveis e o risco permanece. As atividades centrais de EFH da ANP (análise de tarefas/erros, requisitos, verificação/validação e acompanhamento) exigem aplicação iterativa ao longo do ciclo de vida.

**dificil_B · REPROVADA: correcao_tecnica, suporte, sem_generalizacao**  
_Nota(s): Integração de fatores humanos no ciclo de vida do projeto no SGSO; Seleção e qualificação de contratadas no SGSO com base em risco, competência e capacidade técnica_

**P:** Em um FPSO, uma contratada foi mobilizada para um escopo que altera HMI, lógica de alarmes e arranjos de acesso usados por Operação e Manutenção. A seleção priorizou prazo e custo, sem explicitar na interface contratual responsabilidades de segurança do escopo. Após a entrada em serviço, surgem dificuldades de entendimento de alarmes e de execução de tarefas. No SGSO, por que esse problema não deve ser tratado apenas como falha de treinamento do operador embarcado, e o que a qualificação da contratada precisava contemplar?

**R:** Porque o escopo contratado interferiu em fatores humanos de projeto e operação, afetando HMI, alarmes, layout e tarefas, não só a atuação do operador final. Nesse caso, a seleção da contratada deve ser proporcional ao risco e incluir competência do pessoal para o escopo, capacitação em práticas seguras, instrução sobre perigos do trabalho, preparo para emergência e responsabilidades de segurança claramente definidas na interface contratual.

_Explicação:_ Pelo SGSO, fatores humanos devem ser considerados desde o projeto e continuam na operação, não se limitando a documentação. As atividades de engenharia de fatores humanos alcançam HMI, alarmes, sala de controle, layout e análise de tarefas. Se a contratada atua nesses elementos, sua qualificação passa a ser barreira de risco: deve ser avaliada conforme o risco do escopo, com pessoal capacitado, instrução sobre perigos e responsabilidades de segurança explícitas para evitar lacunas entre modificar e operar.

**media · APROVADA**  
_Nota(s): Cultura de segurança e compromisso gerencial no SGSO: como a liderança transforma segurança em decisão e recurso no FPSO/FSO_

**P:** Em duas organizações offshore sob SGSO, ambas enfrentando trade-offs entre produção, custo e risco, a primeira trata a segurança como valor integrado às demais prioridades e mantém interação contínua entre liderança e força de trabalho; a segunda deixa a segurança perder espaço quando aumentam as pressões técnico-econômicas. Compare como essa diferença tende a aparecer no processo decisório e em um traço de cultura de segurança.

**R:** Na primeira, a segurança permanece na decisão com peso estável, em igualdade com as avaliações técnico-econômicas, por ser tratada como valor ligado às demais prioridades. Isso é compatível com comunicação baseada em confiança mútua e percepção compartilhada da importância da segurança. Na segunda, a segurança vira prioridade móvel e pode ser rebaixada por pressão econômica ou operacional, contrariando a lógica decisória do SGSO.

_Explicação:_ O contraste pedido combina o requisito do SGSO de considerar a segurança com importância idêntica às avaliações técnico-econômicas com a noção conceitual de segurança como valor estável. Quando a segurança é deslocada por pressões do momento, ela deixa de influenciar escolhas de forma consistente. Já uma cultura positiva tende a aparecer em comunicação confiável e entendimento comum sobre a relevância da segurança.

_Às cegas (equivalente):_ No processo decisório, a 1ª tende a explicitar risco (critérios, barreiras, MOC), recusar/mitigar desvios e replanejar produção/custo com participação operacional; na 2ª, decisões tendem a privilegiar curto prazo, normalizar exceções e aceitar degradação de barreiras sob pressão. Traço cultural: 1ª mostra “mindfulness/just culture” e comunicação ascendente ativa; 2ª mostra cultura de produção/culpa, silêncio operacional e normalização do desvio.

**dificil_B · APROVADA**  
_Nota(s): SGSO em FPSOs: governança gerencial, cultura de segurança e provisão de recursos; Definição de objetivos, metas e indicadores do SGSO; Programa de auditorias do SGSO: mecanismo formal de verificação da eficácia, conformidade e integração do sistema ao longo do ciclo operacional_

**P:** Em um FPSO em operação, uma auditoria do SGSO volta a apontar desvios em elementos críticos já registrados em ciclo anterior. A gerência informa que abriu ações corretivas, mas os registros de acompanhamento são fragmentados e não demonstram tendência de melhora, estabilização ou recaída; também não há evidência clara de indicadores pró-ativos e reativos, nem de revisão de metas e desempenho. Há pressão para tratar o achado como falha local de execução, sem reavaliar recursos. À luz do SGSO, como esse quadro deve ser interpretado e o que precisa ser demonstrado para sustentar que o problema está controlado?

**R:** Deve ser tratado como indício combinado de fragilidade sistêmica: a recorrência em elemento crítico já diagnosticado indica possível insuficiência de recursos para implementar/funcionar o SGSO, e a auditoria expõe que o monitoramento não fornece base verificável de eficácia. Não basta fechar ações; é preciso demonstrar, com objetivos, indicadores pró-ativos e reativos, coleta, registros, metas e revisão periódica, melhora sustentada do desempenho e resposta gerencial com recursos compatíveis ao risco.

_Explicação:_ A integração exigida é tripla: auditoria revela formalmente a persistência do problema; recorrência em elemento crítico já diagnosticado aponta possível falta de recursos para sustentar o SGSO; e a ausência de monitoramento documentado impede demonstrar se houve controle real entre auditorias. Portanto, o caso não deve ser reduzido a não conformidade pontual. A conclusão correta é indicativa, com necessidade de análise adicional, mas exige reavaliação gerencial de recursos e monitoramento.

_Às cegas (equivalente):_ Interpreta-se como falha sistêmica do SGSO (ineficácia de ações corretivas e de monitoramento), não apenas execução local, pois há reincidência em elementos críticos sem evidência de controle. Para sustentar “controlado”, deve-se demonstrar: análise de causa raiz e barreiras; plano integrado com responsáveis/prazos/recursos; rastreabilidade e verificação de eficácia; indicadores pró-ativos e reativos com baseline e tendência; revisão de metas/performance; avaliação de riscos residual e adequação de recursos/competências, com evidência objetiva.

**facil · REPROVADA: sem_pista, codigo:pergunta_longa · corrigida**  
_Nota(s): Cultura de segurança e compromisso gerencial no SGSO: como a liderança transforma segurança em decisão e recurso no FPSO/FSO_

**P:** Em um FPSO/FSO sob o SGSO, a empresa declara que valoriza a segurança, mas mantém as decisões da instalação baseadas apenas em critérios técnico-econômicos e não planeja nem provê claramente os recursos para implementar e fazer funcionar o SGSO. Por que isso, por si só, não caracteriza uma cultura de segurança consistente?

**R:** Porque, no SGSO, cultura de segurança se materializa quando a segurança entra na tomada de decisão com o mesmo peso das avaliações técnico-econômicas e quando o operador planeja e provê recursos para implementar e fazer funcionar o sistema. Sem isso, a segurança fica só no discurso, ainda que existam declarações corporativas. Ela também se relaciona ao compromisso gerencial com o gerenciamento de riscos.

_Explicação:_ A situação descrita contraria os dois eixos centrais do material: no SGSO, a segurança deve entrar no processo decisório com o mesmo peso das avaliações técnico-econômicas, e o operador deve planejar e prover os recursos necessários para implementar e fazer funcionar o sistema. Por isso, declaração institucional isolada não basta para caracterizar cultura de segurança consistente. Como complemento interpretativo, o tema também se relaciona a compromisso gerencial e gerenciamento de riscos.

**media · REPROVADA: sem_pista, codigo:pergunta_longa · corrigida**  
_Nota(s): Seleção e qualificação de contratadas no SGSO com base em risco, competência e capacidade técnica_

**P:** Na mobilização de uma contratada para um serviço na instalação, o escopo usa ferramentas e equipamentos próprios do terceiro e envolve interface operacional com a equipe do operador. Compare uma qualificação baseada só no treinamento do pessoal com outra que também verifica os recursos da contratada usados no serviço e define claramente as responsabilidades de segurança na interface contratual. Qual delas é mais consistente com a execução segura do escopo? Justifique tecnicamente.

**R:** A qualificação mais consistente é a que vai além do treinamento individual. Olhar só pessoas é insuficiente quando a segurança também depende da condição dos equipamentos e recursos do terceiro e da clareza de responsabilidades na interface operador-contratada. Verificar esses meios e explicitar responsabilidades reduz falhas de coordenação e conflitos de interface, favorecendo a execução segura do serviço.

_Explicação:_ A resposta correta deve contrastar as duas abordagens e concluir que, nesse cenário, não basta qualificar apenas o pessoal. Como o escopo usa recursos próprios da contratada e há interface operacional com o operador, a consistência técnica aumenta quando a qualificação também considera os meios empregados no serviço e a definição clara de responsabilidades de segurança entre as partes. Isso se alinha ao SGSO por combinar competência das pessoas, atenção aos recursos do terceiro quando aplicáveis e redução de falhas de coordenação na interface contratual.

**facil · APROVADA**  
_Nota(s): SGSO em FPSOs: governança gerencial, cultura de segurança e provisão de recursos_

**P:** Em um FPSO sob o SGSO da ANP, por que a existência de procedimentos escritos, por si só, não é suficiente para sustentar a segurança operacional?

**R:** Porque o SGSO só funciona de forma real quando há estrutura organizacional definida, responsabilidades claras e participação efetiva da gerência, além de recursos planejados e providos para implementá-lo e mantê-lo. Também é necessário que a segurança operacional entre nas decisões da empresa com o mesmo peso das avaliações técnico-econômicas, para que prioridades, pessoal e investimentos sustentem o sistema na prática.

_Explicação:_ Os fatos do SGSO exigem mais que documentação formal. O Operador deve organizar a gestão da segurança, definir papéis e garantir participação gerencial, além de prover recursos para implementação e funcionamento do sistema. Como a segurança deve ter importância idêntica à técnico-econômica nas decisões, o SGSO depende de integração à gestão para virar prática operacional, e não apenas conjunto de procedimentos.

_Às cegas (parcial):_ Porque, no SGSO, segurança depende de procedimentos efetivamente implementados: pessoas competentes e treinadas, recursos, supervisão, cultura de reporte, gestão de mudanças, controle de risco, comunicação e disciplina operacional. Procedimentos “no papel” podem estar desatualizados, ser impraticáveis ou não seguidos; sem verificação/auditoria, indicadores e aprendizado com incidentes, não há evidência de conformidade nem de eficácia na prevenção de acidentes.

**media · DESCARTADA (repete outra aprovada) · REDUNDANTE**  
_Nota(s): Definição de objetivos, metas e indicadores do SGSO_

**P:** Em um FPSO, o operador quer acompanhar metas e objetivos de segurança operacional do SGSO para operações e atividades com potencial de causar incidentes. Por que esse acompanhamento exige métodos de coleta definidos, procedimentos documentados de monitoramento e medição e registros das informações, em vez de avaliações informais?

**R:** Porque o acompanhamento das metas do SGSO precisa ser regular, documentado e evidenciado. Métodos de coleta e procedimentos documentados tornam a medição reproduzível; os registros sustentam o acompanhamento do desempenho, os controles operacionais e a verificação de conformidade com metas e objetivos. Sem isso, falta base verificável para avaliar a eficácia do SGSO e revisar desempenho ou metas de modo consistente.

_Explicação:_ O SGSO exige monitorar e medir regularmente operações e atividades que possam causar incidentes por meio de procedimentos documentados. Esses procedimentos devem incluir registros, método de acompanhamento do desempenho, controles operacionais pertinentes e verificação da conformidade com metas e objetivos. Logo, a documentação e os registros não são burocracia isolada: eles viabilizam evidência rastreável para comparar desempenho, demonstrar conformidade e sustentar revisão e melhoria contínua.

_Às cegas (equivalente):_ Porque metas do SGSO só são demonstráveis e gerenciáveis com dados confiáveis: métodos definidos e procedimentos documentados garantem padronização, repetibilidade, comparabilidade e redução de vieses. Registros criam rastreabilidade e evidência para auditorias, verificação de conformidade regulatória/contratual, análise de tendências, tomada de decisão, gestão de ações corretivas e aprendizado. Avaliações informais são subjetivas, difíceis de reproduzir e não sustentam accountability nem melhoria contínua.

**facil · REPROVADA: codigo:pergunta_longa · corrigida**  
_Nota(s): Programa de auditorias do SGSO: mecanismo formal de verificação da eficácia, conformidade e integração do sistema ao longo do ciclo operacional_

**P:** Em um FPSO com SGSO implementado e em funcionamento, a auditoria é tratada pela gerência como checagem documental pontual. Considerando que, no programa de auditorias, elas podem ser internas ou de terceira parte e que, ao final do ciclo, todos os requisitos do SGSO devem ter sido considerados, por que essa abordagem é inadequada no SGSO?

**R:** Porque, no SGSO, auditoria é prática de gestão do próprio sistema para avaliar a eficácia da implementação e do funcionamento e buscar conformidade com o Regulamento Técnico. Pode ser interna ou de terceira parte, desde que o ciclo cubra todos os requisitos. Como integra o conjunto de práticas do SGSO, junto com monitoramento, gestão da informação/documentação e investigação de incidentes, não é atividade isolada.

_Explicação:_ A auditoria, no SGSO, não é atividade acessória. O material a trata como prática de gestão com finalidade própria: avaliar a eficácia da implementação e do funcionamento do sistema e buscar conformidade com o Regulamento Técnico. Também admite auditorias internas ou de terceira parte, desde que o ciclo de auditoria considere todos os requisitos do SGSO. Como essa prática integra a estrutura do sistema ao lado de monitoramento e melhoria contínua do desempenho, gestão da informação e da documentação e investigação de incidentes, ela tem função estruturante, e não de checagem isolada.

**facil · DESCARTADA (repete outra aprovada) · REDUNDANTE**  
_Nota(s): Definição de objetivos, metas e indicadores do SGSO_

**P:** No monitoramento e na melhoria contínua do SGSO de uma instalação offshore, como a política e o planejamento de segurança operacional são convertidos em acompanhamento mensurável do desempenho?

**R:** O SGSO desdobra a política em objetivos de segurança operacional, indicadores de desempenho e metas. Depois exige monitoramento e medição regular das operações e atividades com potencial de causar incidentes, por procedimentos documentados e com registros, para acompanhar o desempenho e verificar conformidade com metas e objetivos. Assim, o operador avalia a eficácia do SGSO e sustenta a melhoria contínua.

_Explicação:_ A lógica documental do SGSO é transformar diretrizes gerais em elementos verificáveis. Objetivos, indicadores e metas criam a base de medição; procedimentos documentados e registros tornam o acompanhamento rastreável; e o monitoramento regular das atividades com potencial de causar incidentes permite comparar desempenho com metas e objetivos. Sem esse encadeamento, a política permanece apenas declaratória e não permite avaliar a eficácia do sistema de forma consistente.

_Às cegas (parcial):_ Convertendo a política/planejamento em objetivos, metas e indicadores (KPIs) do SGSO, definidos com linha de base, critérios de aceitabilidade, responsáveis, periodicidade e método de medição. Isso se materializa em planos de monitoramento/auditoria, inspeções e coleta de dados (leading/lagging), análise de tendências, investigação de desvios, reporte à gestão e ações corretivas/preventivas com verificação de eficácia via revisões gerenciais.

### Sistemas de Lastro, Estabilidade, Ancoragem e Posicionamento, Offloading e Tanques de Carga

#### Operação de tanques de carga, lastro, sistema gás inerte, ventilação e estabilidade

**facil · REPROVADA: codigo:depende_do_material, codigo:pergunta_longa · corrigida**  
_Nota(s): Alinhamento real de headers, slops e rotas temporárias: por que o fluido nem sempre segue o caminho pretendido_

**P:** Com a bomba de stripping em operação, um tanque ligado à mesma rede não esvazia como esperado. Há histórico de comunicação entre tanques e suspeita de passagem em válvulas ou vazamento interno nas linhas. Explique por que isso pode ocorrer sem concluir automaticamente que a bomba está com defeito.

**R:** Porque a bomba não determina sozinha a rota real do fluido. Se houver comunicação entre tanques ou perda de estanqueidade em válvulas/linhas, parte do conteúdo pode migrar, recircular ou retornar pela rede, reduzindo a vazão útil de esgotamento. Assim, a baixa efetividade pode resultar de perda de segregação hidráulica, e não necessariamente de falha da bomba.

_Explicação:_ F1 mostra que o esvaziamento com bomba de stripping pode falhar quando há comunicação entre tanques. F2 e F3 sustentam que passagem em válvulas, vazamento interno nas linhas e perda de estanqueidade alteram o caminho real do fluido. Nessas condições, parte do conteúdo pode migrar pela rede e reduzir o esgotamento sem que isso prove defeito da bomba.

**media · REPROVADA: escopo**  
_Nota(s): Medição e controle da interface óleo-água em vasos e separadores: criticidade, limitações de medição e efeito da manutenção na confiabilidade_

**P:** Em um separador operando com escoamento multifásico e turbulência, contendo água, óleo, gás, sólidos, espuma e emulsão, por que a medição da interface óleo-água tende a ser mais difícil do que em um tanque de líquido estável? Considere também o caso de um método por diferencial de pressão baseado em densidade, quando a temperatura do fluido varia continuamente.

**R:** Porque, no serviço real, a interface deixa de ser uma linha nítida e vira uma zona perturbada por espuma, emulsão e turbulência, o que torna a indicação ambígua. Além disso, no diferencial de pressão a medição depende da densidade; se a temperatura varia e altera essa densidade, a leitura perde confiabilidade sem compensação contínua.

_Explicação:_ Nos fatos, a medição em separadores é dificultada pela presença simultânea de fases, espuma, emulsão, sólidos, gás e turbulência, condições nas quais a interface pode não estar claramente definida. Já o método por diferencial de pressão só é confiável quando a densidade é conhecida e permanece estável. Se a temperatura varia continuamente, a densidade também varia, prejudicando a conversão do sinal em nível/interface confiável.

**dificil_B · APROVADA**  
_Nota(s): Medição e controle da interface óleo-água em vasos e separadores: criticidade, limitações de medição e efeito da manutenção na confiabilidade; Alinhamento real de headers, slops e rotas temporárias: por que o fluido nem sempre segue o caminho pretendido_

**P:** Em um FPSO, um separador envia correntes segregadas de água e óleo. Durante a operação, aparece água acima do esperado em uma corrente/tanque de óleo. Ao mesmo tempo, o stripping de um tanque ligado à rede de headers/slops não reduz o conteúdo como previsto. O processo vinha operando com espuma/emulsão e turbulência; além disso, há histórico de suspeita de passagem em válvulas ou vazamento interno entre tanques/linhas. Qual diagnóstico técnico inicial é o mais consistente e como ele deve ser estruturado?

**R:** Tratar como duas hipóteses acopladas: origem no separador e redistribuição na malha de tanques. A interface pode estar mal controlada, pois sua medição perde confiabilidade com espuma, emulsão e turbulência; se for por DP, densidade variável por temperatura também compromete. Em paralelo, stripping ineficaz sugere caminho hidráulico não segregado, com passagem em válvulas/linhas e migração entre tanques. Logo, não concluir só por falha da bomba nem só pelo instrumento de interface.

_Explicação:_ A água observada pode nascer no separador, porque o controle de interface existe para evitar contaminação cruzada e sua medição fica ambígua quando a interface perde nitidez. Mas a persistência ou aparecimento em tanques fora da rota esperada, somada ao stripping ineficaz, também é compatível com comunicação indevida entre tanques por válvulas/linhas sem estanqueidade. O raciocínio correto separa geração na origem de redistribuição a jusante e evita confundir problema hidráulico com mera falha de bomba.

_Às cegas (parcial):_ Diagnóstico inicial mais consistente: comunicação indesejada (válvula passando/line-up incorreto/vazamento interno) entre rede slops/headers e sistema de óleo, permitindo entrada/retorno de água/emulsão; a espuma/turbulência agrava arraste e mascara interfaces, e explica stripping inefetivo (refluxo/curto‑circuito). Estruturar: (1) confirmar por amostras/teor de água e tendência de níveis/pressões; (2) checar alinhamento e sentido de fluxo nos headers; (3) isolar trechos e testar estanqueidade (valvulas/NRV), rastrear queda/ganho de inventário; (4) só então ajustar química/anti-espuma e regime.

**facil · APROVADA**  
_Nota(s): Medição e controle da interface óleo-água em vasos e separadores: criticidade, limitações de medição e efeito da manutenção na confiabilidade_

**P:** Em um separador em operação com saídas segregadas de óleo e água, por que a interface água-óleo precisa ser controlada?

**R:** Para manter a segregação correta das correntes líquidas, evitando contaminação cruzada: óleo na linha de água e água na linha de óleo.

_Explicação:_ A interface não é controlada apenas para indicar um nível no vaso. Nesse tipo de separador, ela precisa permanecer em posição adequada para que cada saída receba a fase esperada. Se o controle falha, ocorre contaminação cruzada entre as correntes, com envio de óleo para a linha de água ou de água para a linha de óleo.

_Às cegas (equivalente):_ Porque o nível da interface garante a separação eficiente e a qualidade/estabilidade das duas correntes: evita arraste de água no óleo (BS&W alto, corrosão, problemas em bombas/tratamento) e arraste de óleo na água (OIW alto, não conformidade ambiental, sobrecarga do tratamento). Também mantém volume de retenção e tempo de residência adequados, prevenindo instabilidade de controle, cavitação/entrada de gás em linhas e transbordo entre fases.
