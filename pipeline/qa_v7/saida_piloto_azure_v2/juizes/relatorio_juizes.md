# Comparação de juízes

160 questões originais e 128 versões com defeito plantado. Cada juiz avaliou cada item isoladamente, com o mesmo material. Tempo 29.4 min.

Um bom juiz aprova a maior parte das originais (nem todas estão corretas) e reprova as versões com defeito. "Motivo certo" é a fração das detecções em que reprovou pela verificação esperada.

| Juiz | aprova originais | detecta erro técnico sutil | detecta sem suporte sutil | detecta pergunta depende de fonte | detecta caso específico na resposta | detecção média | erros | tokens entrada | tokens saída |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| gpt-5-4-petrobras:medium | 82% | 91% (100%) | 100% (100%) | 97% (100%) | 53% (100%) | 85% | 0 | 1,220,920 | 548,461 |
| gpt-5-2-petrobras:medium | 68% | 94% (97%) | 100% (100%) | 94% (97%) | 81% (100%) | 92% | 0 | 1,220,920 | 366,983 |
| gpt-5-4-petrobras:low | 81% | 91% (100%) | 100% (100%) | 97% (100%) | 66% (95%) | 88% | 0 | 1,220,920 | 259,526 |

| Par de juízes | concordância nas originais | kappa |
|---|---:|---:|
| gpt-5-4-petrobras:medium x gpt-5-2-petrobras:medium | 74% | 0.32 |
| gpt-5-4-petrobras:medium x gpt-5-4-petrobras:low | 82% | 0.411 |
| gpt-5-2-petrobras:medium x gpt-5-4-petrobras:low | 76% | 0.392 |

## Originais com divergência entre juízes

_Para o especialista decidir: quem está certo em cada caso._

### 01c1c3db6e-b0-A1 · facil · Operação de Offloading

**P:** Na operação de offloading, a que efeitos operacionais se associam a perda de propulsão do aliviador, a parada do sistema diesel-gerador e um evento de drive-off em embarcação com posicionamento dinâmico?

**R:** Perda de propulsão e parada do sistema diesel-gerador se associam a atraso operacional e à possibilidade de colisão se a operação prosseguir ou o problema persistir. Em evento de drive-off com posicionamento dinâmico, o cenário relevante também é colisão; nessa condição, a pequena distância entre as embarcações limita a velocidade de impacto a até 2 nós.

- **gpt-5-4-petrobras:medium:** reprova (autonomia, sem_generalizacao) · A resposta introduz o valor de 2 nós e seu mecanismo causal como se valessem genericamente para 'embarcação com posicionamento dinâmico', mas F14 restringe isso ao caso de FPSO e DP shuttle tanker durante offloading.; Para ficar autônoma e sem generalização, a questão pode pedir apenas os efeitos operacionais (atraso operacional e possibilidade de colisão) ou qualificar explicitamente o caso de F14.
- **gpt-5-2-petrobras:medium:** aprova
- **gpt-5-4-petrobras:low:** aprova

### 01c1c3db6e-b0-A2 · media · Operação de Offloading

**P:** Durante o offloading, a equipe enfrenta quatro ocorrências distintas: falha de equipamento genérica; falha no cilindro com sistema de posicionamento dinâmico disponível; problema de thruster; e problema de satélite GPS. Qual deve ser a resposta operacional em cada caso?

**R:** Na falha de equipamento, deve-se desconectar, desamarrar e afastar o aliviador da unidade de produção, com ativação da parada de emergência da transferência; isso aborta a operação. Na falha no cilindro, a desconexão, a desamarração e o afastamento devem ser executados usando o sistema de posicionamento dinâmico. Em problema de thruster, a operação deve ser abortada. Em problema de satélite GPS, a ação indicada é verificar os avisos aos navegantes sobre informações de satélites.

- **gpt-5-4-petrobras:medium:** aprova
- **gpt-5-2-petrobras:medium:** reprova (autonomia) · Falha de autonomia: a pergunta demanda conhecimento específico do material (especialmente a ação para problema de satélite GPS), não sendo garantidamente respondível por um profissional sem acesso à nota.
- **gpt-5-4-petrobras:low:** aprova

### 567fdce5c3-b0-A2 · media · Operação de tanques de carga, lastro, sistema gás inerte, ventilação e estabilidade

**P:** Durante uma manobra de lastro, a unidade recupera calado, trim e banda desejados. Esse resultado, por si só, basta para considerar a condição aceitável?

**R:** Não. A condição só é aceitável se, além de corrigir calado, trim e banda para uma condição segura e nivelada, a redistribuição de lastro também mantiver shear forces, bending moments e tensões torsionais dentro dos limites permissíveis.

- **gpt-5-4-petrobras:medium:** aprova
- **gpt-5-2-petrobras:medium:** reprova (suporte) · Falta de suporte explícito para 'calado' e 'banda' na resposta com base apenas em F1 (F1 fala em estabilidade e 'safe and level trim' e limites de carregamento estrutural, mas não menciona diretamente draft/calado ou list/banda). Para reparar com o mesmo material: (i) citar também F2 para calado e (ii) ajustar redação para não afirmar 'banda' como elemento suportado por F1, ou incluir fato adicional que mencione list/banda no contexto de controle de estabilidade (não fornecido como critério, apenas como ocorrência em F4).
- **gpt-5-4-petrobras:low:** aprova

### 567fdce5c3-b2-A1 · dificil_B · Operação de tanques de carga, lastro, sistema gás inerte, ventilação e estabilidade

**P:** Com um tanque slop indisponível, a equipe reconfigurou temporariamente drenos e uma transferência com bomba de stripping por linha segregada. Depois da manobra, os níveis remotos e o programa de estabilidade indicam condição aceitável, mas o trim observado e a resposta de alguns tanques não batem com a sequência prevista. Antes de autorizar nova transferência e ajuste de lastro, qual interpretação deve prevalecer e qual decisão técnica é a mais correta?

**R:** Deve prevalecer a hipótese de que a condição representada no programa pode estar errada, não a confiança automática no line-up presumido ou na telemedição. Em contingência de slop, o destino real das correntes pode mudar com a reconfiguração dos drenos e transferências, inclusive para outro tanque de carga, e o caminho hidráulico aberto pode diferir do esperado operacionalmente. Como o programa usa dados de tanques atualizados automaticamente, ele só é confiável quando o conteúdo dos tanques é confirmado por verificação manual regular. Se a condição observada a bordo diverge do que o programa mostra, a próxima transferência ou manobra de lastro não deve prosseguir até reconciliar o inventário real dos tanques com a condição carregada no software e, se necessário, reavaliar e simular a sequência antes da execução.

- **gpt-5-4-petrobras:medium:** aprova
- **gpt-5-2-petrobras:medium:** reprova (suporte, sem_generalizacao) · Suporte insuficiente para enunciados absolutos (“só é confiável quando...”) e para a prescrição categórica (“não deve prosseguir...”) com base apenas em F11/F17; ajustar para linguagem não absoluta (ex.: ‘a confiança deve ser condicionada a’ / ‘é recomendável não prosseguir até...’) mantém a ideia sem extrapolar os fatos.; Sem_generalizacao: a resposta universaliza uma prática descrita como recomendação/rotina em um caso/fonte; basta remover a generalização e ancorar como critério prudencial derivado das fontes.
- **gpt-5-4-petrobras:low:** aprova

### 62e43c1988-b0-A1 · facil · Sistema de ancoragem, manutenção e monitoramento da posição

**P:** Em uma unidade ancorada, ocorre a falha de uma linha de ancoragem. Qual deve ser a resposta operacional imediata, e de que fatores depende eventual retomada das operações?

**R:** As operações devem cessar imediatamente. A retomada depende de qual linha falhou, das condições meteorológicas presentes e futuras e da verificação de conformidade com os parâmetros de projeto.

- **gpt-5-4-petrobras:medium:** aprova
- **gpt-5-2-petrobras:medium:** aprova
- **gpt-5-4-petrobras:low:** reprova (autonomia, sem_generalizacao) · A pergunta carece de delimitação contextual e faz parecer universal um critério que, nos fatos, é apresentado como resposta operacional declarada nos materiais.; Para ficar autônoma sem exigir leitura do material, seria preciso reformular como critério do procedimento/material, por exemplo: 'Segundo o procedimento descrito...' ou 'Nos materiais apresentados...'

### ee74ce2b7b-b2-A1 · dificil_B · Sistema e operação de pull in de risers

**P:** Durante o pull-in de um riser, um FPSO monocaio com turret e thrusters para manter heading sofre perdas de heading que são recuperadas em seguida, enquanto o tempo piora. O arranjo geométrico entre amarrações e risers foi considerado com boa folga, e parte da equipe quer continuar por entender que o controle ainda se recupera. Qual decisão técnica é mais adequada nesse momento e por quê?

**R:** A decisão mais adequada é suspender preventivamente a operação, sem tratar a recuperação momentânea do heading como evidência suficiente de segurança. Perdas recorrentes de heading sob piora ambiental indicam redução de margem operacional. Nesse contexto, o desvio pode evoluir de excursão recuperável para twist do turret; se houver degradação adicional do controle dos thrusters e o turret não girar como necessário, a torção das amarrações pode reduzir as folgas até contato com os risers. A boa geometria entre linhas ajuda em condição normal, mas não elimina o risco em cenário extremo de twist. Se houver rotação anormal do turret, suspeita de contato ou evento severo, o retorno não deve se basear só em sinais de bordo; em arranjos com bóia latched e amarrações sem medição normal de tensão em água, a condição das linhas precisa ser confirmada por inspeção em água antes de retomar.

- **gpt-5-4-petrobras:medium:** aprova
- **gpt-5-2-petrobras:medium:** reprova (suporte) · Falta de suporte factual para o critério decisório central (‘suspender preventivamente’ por perdas recuperadas/recorrentes de heading e piora do tempo) — isso é o núcleo da pergunta e não está coberto pelos fatos citados.; Afirmações sobre ‘redução de margem operacional’ e uso de perdas recuperadas como gatilho de suspensão aparecem como interpretação operacional, mas não são sustentadas diretamente por F4/F6/F7/F14/F15.; F15 é citado, mas a resposta não trata de ‘weather side working’ nem deriva um critério operacional a partir desse fato; fica como citação deslocada.
- **gpt-5-4-petrobras:low:** reprova (suporte) · Falta suporte explícito em F# para a decisão normativa específica de 'suspender preventivamente'.; Falta suporte explícito em F# para a expressão 'redução de margem operacional'.; Seria necessário citar fatos adicionais que sustentem a decisão por suspensão com base em limites operacionais/continuidade da operação; sem isso, a resposta introduz critério operacional novo.

### 62d82a5ef2-b0-A2 · media · Medição Fiscal de óleo, medição fiscal de gás e transferência de custódia em operações de offloading

**P:** Em uma instalação offshore, foi identificada possível inconsistência na medição fiscal e a equipe precisa saber quais eventos podem abrir processo de recálculo da produção. Quais são os principais gatilhos e qual deles tende a ser o mais frequente?

**R:** Os principais gatilhos são notificação de falha do sistema de medição, inspeções, declarações das concessionárias, denúncias e validação da produção. Entre eles, a notificação de falha do sistema de medição tende a ser o canal mais frequente de abertura desses processos. Isso ocorre porque, quando a falha ou a não conformidade coloca em dúvida a veracidade dos dados informados, a fiscalização da medição pode instaurar recálculo da produção.

- **gpt-5-4-petrobras:medium:** aprova
- **gpt-5-2-petrobras:medium:** aprova
- **gpt-5-4-petrobras:low:** reprova (autonomia) · Falha de autonomia: a comparação sobre qual gatilho é o mais frequente depende de observação específica da fonte, não de regra técnica geral.

### 62d82a5ef2-b1-A1 · dificil_A · Medição Fiscal de óleo, medição fiscal de gás e transferência de custódia em operações de offloading

**P:** Durante o planejamento da medição de custódia no offloading, a equipe avalia duas alternativas: implantar monitoração online contínua de vazão, pressão estática e temperatura, ou limitar a instrumentação à medição direta de pressão estática na parede do duto e temperatura do escoamento. O orçamento é restrito, mas a operação quer manter o cálculo do volume compensado. Qual decisão técnica é mais consistente e qual o impacto dessa escolha sobre a estratégia de medição?

**R:** A decisão técnica depende de compatibilizar rigor metrológico com viabilidade de investimento. Se a monitoração online contínua de vazão, pressão estática e temperatura não se justificar economicamente, é consistente limitar a instrumentação à medição direta de pressão estática na parede do duto e temperatura do escoamento, porque essas duas variáveis devem compor o conjunto mínimo para viabilizar o cálculo do volume compensado. Nessa escolha, a estratégia de medição deixa de depender de uma base online completa em tempo real e passa a concentrar a representatividade do resultado no algoritmo de cálculo aplicado ao volume. Se houver recursos e interesse em maior representatividade operacional do escoamento, a monitoração online completa pode ser adotada, mas ela exige transmissores e sistemas automáticos adicionais. Em qualquer caso, a medição de custódia não se resume ao medidor de vazão; ela envolve o conjunto integrado da estação de medição e seus dispositivos de aquisição e cálculo.

- **gpt-5-4-petrobras:medium:** reprova (suporte) · Há afirmação sem suporte explícito nos fatos citados sobre a representatividade do resultado ficar concentrada no algoritmo de cálculo.; A resposta não explicita a condição de estabilidade operacional para que monitoração online seja tratada como representativa ao longo do intervalo, o que reduz a completude.
- **gpt-5-2-petrobras:medium:** aprova
- **gpt-5-4-petrobras:low:** reprova (suporte) · Falta de suporte explícito, nos fatos citados, para a afirmação sobre 'representatividade do resultado' concentrada no algoritmo.; Falta de suporte explícito, nos fatos citados, para a expressão 'maior representatividade operacional do escoamento'.; A resposta fica incompleta ao não mencionar a condição de estabilidade operacional apresentada na nota para uso representativo da medição online por intervalo mais extenso.

### 4e96c8ab4a-b0-A2 · media · Operação de Separadores Trifásicos

**P:** Em um separador trifásico com pressão controlada pela saída de gás no topo, como a abertura das válvulas de saída de óleo e de água deve regular as vazões de descarga para manter o inventário líquido e a separação estáveis?

**R:** As válvulas das saídas líquidas devem ajustar as vazões de descarga conforme as variáveis de nível medidas no vaso. A saída de óleo responde ao controle de nível do líquido para manter o inventário na faixa desejada. A saída de água, pela linha inferior, responde ao nível de interface água-óleo para regular especificamente a retirada da água livre. Dessa forma, o inventário líquido é controlado sem usar a saída de gás para corrigir níveis, e a posição da interface é mantida pela própria descarga de água, o que favorece a estabilidade da separação.

- **gpt-5-4-petrobras:medium:** aprova
- **gpt-5-2-petrobras:medium:** reprova (suporte) · Falta de suporte: a afirmação sobre não usar a saída de gás para corrigir níveis não está respaldada por F1/F2 (nem é inferência direta inevitável a partir deles).
- **gpt-5-4-petrobras:low:** aprova

### 4e96c8ab4a-b1-A1 · dificil_A · Operação de Separadores Trifásicos

**P:** Em um FPSO, um separador trifásico passou a operar por período prolongado com condições reais de processo diferentes das premissas de projeto. O vaso continua com inspeções periódicas programadas, porém parte do histórico de manutenção e inspeção está incompleta no cadastro, e a equipe argumenta que a conformidade com requisitos de classe é suficiente para manter o regime atual. Nesse cenário, essa mudança já justifica revisar o regime de inspeção e reforçar a abordagem baseada em risco?

**R:** Sim. Operar fora do envelope de projeto já é uma condição que eleva o perigo potencial de perda de contenção, portanto aumenta a necessidade de reavaliar se frequência, escopo e prioridade das inspeções continuam adequados. Como o sistema de integridade pode ser estruturado por inspeção prescritiva e/ou baseada em risco, a resposta técnica não é manter o regime por inércia, mas revisar o plano quando a condição real de processo mudou e a incerteza aumentou. A situação fica ainda mais forte porque o histórico incompleto no cadastro reduz a visibilidade sobre inspeções, manutenção e reparos, o que prejudica a avaliação da condição do ativo. Além disso, conformidade com requisitos de classe, isoladamente, não basta quando pode haver lacunas de cobertura no sistema de integridade. Nessa condição, o adequado é reforçar o controle do ativo e revisar o regime com base no risco.

- **gpt-5-4-petrobras:medium:** aprova
- **gpt-5-2-petrobras:medium:** reprova (escopo) · Escopo/subtópico desalinhado: a questão está centrada em gestão de integridade/inspeção (RBI, cadastro, lacunas de classe) e não em operação de separadores trifásicos. Para reparar com o mesmo material, seria necessário reclassificar o subtópico (ou o enquadramento) para integridade/inspeção de vasos, ou então alterar o alvo/subtópico para refletir o conteúdo efetivamente avaliado.
- **gpt-5-4-petrobras:low:** reprova (escopo) · Desalinhamento de escopo com o subtópico 'Operação de Separadores Trifásicos': a questão está mais centrada em gestão de integridade/inspeção de vasos do que em operação do separador.

### 6ab1aa24b5-b0-A2 · media · Operação de Tratadores Eletrostáticos

**P:** Em uma campanha, a qualidade da água produzida piora progressivamente, mas o óleo exportado ainda atende à especificação de água. Sem evidência de vazamento, o que esse quadro sugere sobre a separação no separador trifásico ou no tratador eletrostático?

**R:** Sugere desvio de separação com perda de óleo para a corrente aquosa. O atendimento da especificação do óleo não garante que a separação global esteja adequada, porque parte do óleo pode estar sendo deslocada para a água produzida. Isso aumenta a carga de entrada do sistema de tratamento de água justamente na corrente que ele precisa enquadrar para descarte, reinjeção ou utilidades. Como esse sistema foi projetado para operar com água contendo óleo disperso na faixa de projeto na saída do separador trifásico, e não com carga de óleo bruto pouco diluída, a piora da água produzida é compatível com sobrecarga por perda de separação a montante.

- **gpt-5-4-petrobras:medium:** aprova
- **gpt-5-2-petrobras:medium:** reprova (suporte) · Falta de suporte explícito em F1/F2 para o nexo diagnóstico ‘piora da qualidade da água sem vazamento’ ⇒ ‘desvio de separação/arraste de óleo’ (o material factual fornecido só cobre função do tratamento e janela de projeto).; A resposta presume que a ‘piora da qualidade’ se deve a aumento de óleo na corrente aquosa e que isso decorre de falha de separação; para ficar suportado apenas com F1/F2, o enunciado deveria explicitar aumento de óleo na água (p.ex., acima da faixa de projeto ~1000 ppm) ou a resposta deveria ser mais condicional.
- **gpt-5-4-petrobras:low:** aprova

### 96c4f33979-b0-A2 · media · Produção, processo e processamento do óleo

**P:** Durante a preparação para partida, a inspeção encontra resíduos sólidos e depósitos no feixe de um trocador, além de depósitos no casco e na linha de entrada de utilidade. Como isso pode degradar o desempenho do trocador antes mesmo da operação contínua?

**R:** Esses achados indicam que o trocador já entra em serviço com condição interna diferente da prevista. Resíduos e depósitos no feixe reduzem a efetividade da troca térmica. Depósitos no casco e na linha de entrada de utilidade podem alterar a distribuição do escoamento e restringir passagens internas. Assim, mesmo antes de operação contínua, o equipamento pode partir com menor capacidade de transferência de calor e pior desempenho global, razão pela qual esses pontos devem ser verificados na inspeção de prontidão.

- **gpt-5-4-petrobras:medium:** aprova
- **gpt-5-2-petrobras:medium:** aprova
- **gpt-5-4-petrobras:low:** reprova (suporte) · Falta de suporte explícito para mecanismos e consequências centrais da resposta com base no fato citado (F4).; A resposta introduz conteúdo técnico adicional sem amarração suficiente em F# na forma exigida.

### 96c4f33979-b2-A1 · dificil_B · Produção, processo e processamento do óleo

**P:** Uma unidade quer intensificar a redução de sal no óleo aumentando a integração térmica com água separada quente dos tratadores eletrostáticos e mantendo injeção de água de lavagem. Ao mesmo tempo, há preocupação com incrustação carbonática em linhas e equipamentos do topside após aquecimento e despressurização. Qual decisão técnica é mais adequada para conciliar tratamento do óleo e integridade do sistema?

**R:** A decisão mais adequada é manter a dessalgação integrada à desidratação, sem tratar a recirculação quente como benefício automático nem como agravante automático, e reavaliar a mitigação de incrustação pela pior mistura de águas do sistema. A redução de sal depende de água de lavagem aquecida, contato dessa água com o óleo e remoção efetiva da fase aquosa no vaso por coalescência e decantação sob campo elétrico. Porém, no topside, a tendência à incrustação carbonática cresce com temperatura, pH e despressurização com liberação de CO2. Nessa avaliação, a água recirculada quente merece análise, mas seu efeito direto sobre a criticidade tende a ser baixo; a água de diluição usada para reduzir a salinidade do óleo é a variável com maior impacto sobre o potencial de incrustação. Portanto, a priorização correta é revisar a mistura de águas e a dosagem de inibidor com base no cenário mais crítico, não simplesmente maximizar a recirculação.

- **gpt-5-4-petrobras:medium:** reprova (correcao_tecnica, suporte, autonomia, sem_generalizacao) · Extrapola os achados condicionais de F7/F9 para uma unidade genérica.; A resposta presume o resultado da avaliação de incrustação, quando o material só autoriza afirmar que isso valeu para os cenários estudados.; A autonomia fica comprometida porque a decisão correta depende de conclusões específicas da fonte, não de regra geral do subtópico.
- **gpt-5-2-petrobras:medium:** reprova (suporte, sem_generalizacao) · Generalização não suportada: a resposta sugere como tendência geral que a recirculação tem baixo efeito, mas os fatos limitam isso aos cenários analisados (ajustar redação para 'no cenário analisado/avaliado' resolveria).; Suporte: a frase 'tende a ser baixo' precisa ser condicionada explicitamente ao estudo/cenário avaliado para ficar totalmente coberta por F7 e alinhada ao alerta de não generalização nas notas.
- **gpt-5-4-petrobras:low:** aprova

### e8459723b0-b2-A1 · dificil_B · Sistema de Alívio e Flare

**P:** Uma PSV de um vaso foi mantida após revisão porque, na verificação do cenário de sobrepressão do equipamento, o transiente mostrou pressão aceitável. Meses depois, em um upset com blowdown e alívio simultâneos para o mesmo flare, a pressão a montante de algumas PSVs permanece alta por mais tempo e há suspeita de abertura fora do esperado. Qual é o diagnóstico técnico mais consistente e qual decisão de projeto/operação deve ser priorizada?

**R:** O desvio mais consistente é a interação entre a PSV e o header comum sob evento combinado, não uma falha isolada do dispositivo. Uma PSV pode parecer adequada quando verificada para o equipamento protegido, mas perder desempenho se a descarga simultânea elevar a contrapressão no coletor além do admitido. Nessa condição, a contrapressão pode alterar a abertura de válvulas conectadas ao header e comprometer a proteção. A prioridade é reavaliar o sistema integrado: combinações críveis de alívio e blowdown, capacidade hidráulica do flare/header e adequação do tipo de PSV à contrapressão prevista. Se houver contrapressão relevante no coletor, a seleção de PSV balanceada é tecnicamente mais consistente do que a convencional. Se a capacidade simultânea do sistema receptor for insuficiente, a demanda deve ser compatibilizada com a capacidade disponível, por exemplo com despressurização faseada ou escalonada, em vez de presumir blowdown total simultâneo.

- **gpt-5-4-petrobras:medium:** aprova
- **gpt-5-2-petrobras:medium:** reprova (suporte) · Falta de suporte: recomendação específica de 'despressurização faseada/escalonada' não tem fato F# correspondente no material fornecido.; Suporte incompleto: a justificativa sobre escolha do tipo de PSV em função do arranjo/contrapressão depende de F2, que não está amarrado explicitamente no texto da resposta (embora exista no material). Para ficar rigoroso, deve-se citar/ancorar essa parte em F2 (e F1).
- **gpt-5-4-petrobras:low:** aprova

### 69f5898918-b2-A1 · dificil_B · Sistema de captação e tratamento de água do mar para injeção no reservatório

**P:** Uma unidade passou a ter ciclos de filtração mais curtos, mais retrolavagens e maior oscilação de vazão na sucção das bombas de injeção, com dificuldade para sustentar as cotas dos poços. Sem indício inicial de dano nas bombas, qual diagnóstico deve ser priorizado: limitação da filtração, limitação hidráulica de alimentação ou problema na fonte de captação? Justifique pela relação causal entre esses elementos.

**R:** A prioridade é verificar a fonte de captação como causa primária e tratar a filtração e a hidráulica como efeitos encadeados. Se a água captada chega com mais sólidos, turbidez ou maior variabilidade, aumenta a carga sobre o pré-tratamento. Nos filtros, isso encurta o ciclo de serviço, porque o leito retém partículas, se obstrui progressivamente e perde eficiência, exigindo retrolavagens mais frequentes. Essas transições tornam menos estável a disponibilidade de água tratada a montante do bombeio. A oscilação nas bombas passa então a ser manifestação hidráulica de uma perturbação originada antes, não necessariamente falha do bombeamento. Na etapa seguinte, deve-se confirmar se a reservação e o arranjo de estabilização estão conseguindo desacoplar essa variabilidade; se não estiverem, o sintoma hidráulico aparece com mais força, mas a origem continua sendo a piora da água na captação.

- **gpt-5-4-petrobras:medium:** aprova
- **gpt-5-2-petrobras:medium:** reprova (correcao_tecnica, suporte) · Elo causal ‘retrolavagens mais frequentes → menor estabilidade de disponibilidade de água tratada → oscilação na sucção’ não está explicitamente suportado pelos fatos fornecidos (F8 não descreve impacto hidráulico/indisponibilidade; F6 aborda outro mecanismo: queda de água produzida).; Uso de F6/F9 para justificar desacoplamento hidráulico no contexto de instabilidade originada em filtração não está ancorado no material (mecanismo de F6 é específico para variação de água produzida/entrada de água salgada).; A resposta introduz ‘mais sólidos/turbidez/variabilidade na captação’ como causa do aumento de ciclos sem evidência factual no enunciado nem fato que conecte diretamente captação piorada ao evento observado; fica como hipótese não sustentada.
- **gpt-5-4-petrobras:low:** aprova

### 1332c32a59-b1-A1 · dificil_A · Sistema de drenagem aberta e fechada

**P:** Durante um descomissionamento parcial, um trecho de drenagem aberta e uma linha overboard foram retirados da operação normal, mas a segregação definitiva ainda não foi concluída. A equipe propõe removê-los do plano de inspeção e tratar o isolamento existente como suficiente até a próxima parada. Tecnicamente, por que essa decisão é inadequada?

**R:** Porque, sem segregação definitiva, esses trechos ainda podem permanecer hidraulicamente conectados a tanques, convés ou mar e continuar relevantes para o risco. Nessa condição, a integridade mecânica das linhas internas a tanques e das interligações associadas deve seguir sendo considerada na gestão de mudanças e nas análises de risco, pois uma falha pode criar retorno de gás ao convés, transferência de carga entre tanques ou vazamento de óleo para o mar. Por isso, linhas inoperantes não devem ser tratadas como neutras apenas por estarem fora da operação normal. Elas precisam permanecer sob rotina de inspeções e manutenções, e o descomissionamento deve manter isolamento e bloqueios adequados até a segregação definitiva eliminar essas comunicações indesejadas.

- **gpt-5-4-petrobras:medium:** aprova
- **gpt-5-2-petrobras:medium:** reprova (suporte) · Falta de suporte nos fatos citados para: (i) conexão hidráulica residual de trechos inoperantes/overboard; (ii) exigência de isolamento e bloqueios até segregação definitiva; (iii) afirmação normativa de que trechos inoperantes não são neutros. Para reparar, é preciso remover/ajustar essas partes ou incluir suporte explícito do material fornecido (sem adicionar conteúdo novo).
- **gpt-5-4-petrobras:low:** reprova (suporte) · Falta suporte explícito, nos fatos citados, para a parte da resposta sobre 'isolamento e bloqueios adequados até a segregação definitiva'.; A resposta introduz formulações amplas ('hidraulicamente conectados a tanques, convés ou mar', 'não devem ser tratadas como neutras') que não estão textual e diretamente ancoradas nos fatos citados da questão.

### 1332c32a59-b2-A1 · dificil_B · Sistema de drenagem aberta e fechada

**P:** Nos primeiros dias após o start-up de um sistema de drenagem aberta e fechada, surgem escoamento irregular, intervenções locais para desobstrução e suspeita de perda de segregação em dispositivos com selo líquido. O sistema havia sido liberado após flushing com água e ficou alguns dias vazio; além disso, há divergência entre equipes sobre a versão do procedimento usada na liberação. Tecnicamente, qual origem deve ser priorizada no diagnóstico: falha de manutenção rotineira ou desvio de comissionamento/preparação, e por quê?

**R:** Deve-se priorizar desvio de comissionamento/preparação. O problema apareceu nos primeiros dias de operação, fase em que ainda se confirmam processo e transição para o serviço; nesse contexto, falhas de cobertura dos testes ou de transição são causa provável. A divergência entre equipes sobre a versão do procedimento reforça deficiência de controle documental, compatível com liberação inadequada. Como houve flushing com água e o sistema ficou vazio por alguns dias, o diagnóstico deve verificar se a água foi drenada pelos pontos baixos, se houve remoção de residual com ar seco e se foi feita preservação com ar seco ou nitrogênio. Em paralelo, é necessário inspecionar integridade dos selos líquidos e presença de detritos em drenos, valas e headers. Esses achados podem parecer falha rotineira, mas também podem ter sido introduzidos pela preparação física incompleta antes da entrada em serviço.

- **gpt-5-4-petrobras:medium:** reprova (suporte) · A resposta inclui 'presença de detritos em headers' sem fato explícito correspondente.; A ligação entre achados de selos e sua introdução pela preparação física pré-serviço ficou mais ampla do que o suporte factual disponível.; A lista de fatos citados na questão/resposta omite F1, que é o suporte mais direto para 'falhas de cobertura dos testes'.
- **gpt-5-2-petrobras:medium:** aprova
- **gpt-5-4-petrobras:low:** aprova

### 9feff6fc72-b1-A1 · dificil_A · Tratamento do Gás produzido

**P:** Em uma plataforma com remoção de CO₂ por membranas, a equipe enfrenta três condições ao longo da campanha: indisponibilidade total das membranas, operação plena e operação parcial. Para cada condição, como deve ficar o balanço entre exportação e injeção de gás? Na condição de indisponibilidade total, qual é a conclusão explicitamente sustentada sobre o gás enviado às turbinas?

**R:** Com indisponibilidade total das membranas, a unidade opera em modo A: a exportação fica impedida e todo o gás deve ser direcionado para injeção. Com operação plena, opera em modo B: a remoção de CO₂ permite exportação máxima de gás. Com operação parcial, opera em modo C: a plataforma combina exportação parcial com injeção parcial. No modo A, como não existe parcela de gás tratada pelas membranas, o gás encaminhado às turbinas apresenta teor de CO₂ igual ao do fluido produzido nos poços.

- **gpt-5-4-petrobras:medium:** reprova (suporte) · A resposta não reproduz com fidelidade a conclusão explicitamente sustentada em F3: substitui 'petróleo oriundo dos poços' por 'fluido produzido nos poços'.; O enunciado pede o balanço entre exportação e injeção em cada condição; no modo B a resposta informa corretamente 'exportação máxima', mas não explicita o lado da injeção, o que reduz um pouco a completude.
- **gpt-5-2-petrobras:medium:** reprova (autonomia) · Falha de autonomia: a pergunta exige conhecimento de uma nomenclatura/filosofia operacional específica (modos A/B/C) e de uma regra operacional não universal; para ser autônoma, precisaria incorporar no enunciado a definição dos modos/da filosofia (ou evitar a nomenclatura) sem depender do material.
- **gpt-5-4-petrobras:low:** aprova

### d87b10b437-b1-A1 · dificil_A · Estudos de Segurança

**P:** Em um FPSO em operação, o gerenciamento de mudanças registrou uma alteração com impacto na planta de processo. Em paralelo, inspeções e dados de integridade indicam redução da vida remanescente por fadiga e corrosão em casco e topside. Antes de decidir se a Safety Case Review será aberta, que verificações e estudos adicionais devem ser feitos, e como essa decisão deve ser registrada no sistema de gestão?

**R:** A decisão deve ser subsidiada por duas frentes. Primeiro, verificar se as bases técnicas do safety case e dos demais estudos de risco ainda representam a configuração real, os equipamentos, os processos e as condições operacionais da unidade, incluindo se as premissas permanecem válidas e se o programa de integridade de ativos continua alinhado ao safety case. Segundo, avaliar o efeito da mudança e do envelhecimento sobre os perigos maiores, especialmente quando fadiga e corrosão alteram a vida remanescente de casco e topside. Se houver impacto, o sistema de gestão deve identificar, registrar e comunicar a mudança, acionar formalmente a Safety Case Review e, quando necessário, estudos adicionais como HAZID e HAZOP. A documentação deve evidenciar o critério usado para decidir, as premissas verificadas, os impactos identificados, os estudos complementares requeridos e o vínculo com a implementação das ações resultantes.

- **gpt-5-4-petrobras:medium:** reprova (suporte) · A resposta inclui HAZID sem suporte factual explícito no material fornecido.; Há leve imprecisão ao dizer 'se houver impacto', quando o cenário já informa mudança com impacto, condição que em F8 aciona a Safety Case Review.; Não explicita a checagem do escopo de estudos associados potencialmente relevantes na revisão, como estudos complementares cujas premissas sustentam cenários críticos.
- **gpt-5-2-petrobras:medium:** reprova (correcao_tecnica, suporte) · Inconsistência técnica: com “alteração com impacto” (enunciado), o F8 indica que a Safety Case Review deve ser gerada; a resposta mantém condicionalidade (“se houver impacto”) como se ainda fosse opcional.; Falta de suporte: inclusão de HAZID como estudo adicional não está suportada por nenhum fato fornecido.; Falta de suporte/precisão: lista detalhada do que “a documentação deve evidenciar” extrapola o que os fatos determinam explicitamente (F8 fala em identificar/reportar/comunicar e gerar a revisão/estudos; F15 fala em garantir validade de premissas; F14 caracteriza falha quando há reavaliação de prazos sem justificativa, mas não prescreve o pacote documental proposto).
- **gpt-5-4-petrobras:low:** aprova

### fadd3bccc0-b0-A2 · media · Operações simultâneas – SIMOPS

**P:** Em um projeto com SIMOPS, a contratada troca parte da crew no fim do turno enquanto a operação principal continua sem mudança relevante. Como essas trocas podem degradar a coordenação, e por que a comunicação entre a supervisão do operador e da contratada deve ser mantida durante todo o projeto?

**R:** Mudanças de turno e de crew são pontos em que a informação sobre interações entre frentes pode se perder, ser transmitida de forma incompleta ou chegar distorcida. Isso degrada a continuidade do entendimento sobre quais atividades coexistem, com quais operações a contratada pode interagir e quem deve acionar ou ajustar o trabalho quando o contexto muda. Por isso, a comunicação entre a supervisão do operador e a da contratada deve permanecer clara e contínua durante todo o projeto, não só no início, para preservar esse entendimento ao longo das passagens de turno e reduzir a chance de que interações críticas deixem de ser percebidas a tempo.

- **gpt-5-4-petrobras:medium:** aprova
- **gpt-5-2-petrobras:medium:** reprova (suporte) · Falta de suporte: a resposta adiciona a ideia de definição de quem aciona/ajusta o trabalho com mudança de contexto, sem fato correspondente (não suportado por F3/F4 e não decorre diretamente deles).; Cobertura parcial de suporte: para sustentar plenamente a parte de 'entendimento sobre quais atividades coexistem/interagem', seria recomendável ancorar explicitamente em F1 (awareness de interações), que não foi citado na questão.
- **gpt-5-4-petrobras:low:** reprova (suporte) · Há falta de suporte para a afirmação sobre 'quem deve acionar ou ajustar o trabalho quando o contexto muda'.; A resposta poderia ficar integralmente suportada se se limitasse à perda de comunicação, à distorção nas passagens de turno e à necessidade de manter linhas claras entre supervisões durante todo o projeto.

### fadd3bccc0-b1-A1 · dificil_A · Operações simultâneas – SIMOPS

**P:** Em uma SIMOPS com unidade conectada a infraestrutura submarina, duas condições anormais dinâmicas são discutidas no plano de resposta: no primeiro caso, forças ambientais em rápida piora elevam a carga dos propulsores, surgem deriva e desvio de rumo; no segundo, ocorre falha de energia principal. Em cada caso, qual função essencial deve ser preservada primeiro para levar a unidade a estado seguro, e qual ação operacional decorre dessa prioridade?

**R:** Se os sinais mostram aumento de carga nos propulsores, deriva e desvio de rumo, a função crítica em perda é a manutenção de posição. Nessa condição, a prioridade passa a ser evitar dano à infraestrutura submarina e à unidade, o que pode exigir iniciar a desconexão de emergência quando o posicionamento já não é mantido.

Se ocorre falha de energia principal, a função essencial a preservar primeiro é a estabilidade da unidade por meio da operabilidade do lastro. Para levar a unidade a estado seguro, devem permanecer disponíveis, a partir do quadro de emergência alimentado pelo gerador de emergência, uma ou mais bombas de lastro e o sistema completo de lastro, de modo a recuperar trim seguro e nivelado.

- **gpt-5-4-petrobras:medium:** reprova (tipo_ok) · Tipo/forma: a estrutura pede integração indispensável entre perda de posicionamento e perda de geração, ficando mais aderente a difícil_B do que a difícil_A.
- **gpt-5-2-petrobras:medium:** reprova (correcao_tecnica, suporte, jurisdicao, sem_generalizacao) · Falta de suporte: a resposta adiciona ‘evitar dano ... à unidade’, que não está nos fatos citados (F1 fala apenas de dano potencial à infraestrutura submarina).; Jurisdição/modal: usa ‘devem’ (obrigação) para orientação HSE UK (‘should’) sem qualificar como recomendação/arranjo da fonte, o que pode ser interpretado como exigência geral aplicável.; Generalização: transforma exemplo e guidance em regra universal sem qualificação (‘no caso descrito’/‘segundo a orientação citada’).
- **gpt-5-4-petrobras:low:** aprova

### fadd3bccc0-b2-A1 · dificil_B · Operações simultâneas – SIMOPS

**P:** Duas frentes em SIMOPS foram liberadas como compatíveis pela matriz vigente. Durante a execução, ocorre alarme de gás na área, com atuação automática que altera a ventilação e começa a afetar painéis elétricos; ao mesmo tempo, descobre-se que um maintenance bypass aplicado para viabilizar startup atuava sobre um transmissor que executa PSH e PSL, desabilitando ambas as funções. A coordenação deve manter, restringir ou interromper as frentes? Justifique pelo efeito combinado sobre a compatibilidade.

**R:** Deve interromper ou, no mínimo, suspender as frentes até reavaliar a compatibilidade com a arquitetura real de barreiras. A matriz só sustenta a compatibilidade se estiver convergente com o estado efetivo das barreiras e atualizada para mudanças operacionais. Aqui, a premissa deixou de valer por dois motivos combinados: o bypass não retirou apenas a função de partida, mas também a proteção primária de pressão do mesmo transmissor, reduzindo disponibilidade e independência das proteções; e o alarme não foi só indicação, pois a lógica automática alterou a ventilação e passou a impactar painéis elétricos e sistemas dependentes. Assim, o evento ocorreu com menos camadas de defesa do que a matriz nominal presumiu. Antes de retomar SIMOPS, é preciso restabelecer ou controlar formalmente as barreiras degradadas e atualizar a base de compatibilidade para refletir o novo arranjo.

- **gpt-5-4-petrobras:medium:** aprova
- **gpt-5-2-petrobras:medium:** reprova (suporte, sem_generalizacao) · Falta de suporte factual para a obrigação de ‘interromper’ (normativo), quando os fatos fornecidos suportam claramente ‘reavaliar/atualizar’ mas não impõem a decisão de parada em qualquer caso.; Uso de conceitos (‘disponibilidade’, ‘independência’, ‘menos camadas de defesa’) sem amarração explícita a F# na resposta; com o conjunto de fatos fornecido, isso vira conteúdo técnico novo não citado.; ‘Controlar formalmente’ o bypass aplicado ao transmissor é extrapolação: o fato de controle formal/corretivo citado (F18) refere-se especificamente a ESD em bypass, não a PSH/PSL nesse cenário.
- **gpt-5-4-petrobras:low:** reprova (suporte) · Falta de suporte explícito para 'reduzindo disponibilidade e independência das proteções'.; Falta de suporte explícito para 'controlar formalmente as barreiras degradadas'.; A resposta deveria ancorar a decisão de suspensão/interrupção com fatos mais diretamente ligados à reavaliação após impacto em utilidades/barreiras, ou reformular para evitar conteúdo novo não citado.

### 202d9e591b-b2-A1 · dificil_B · Segurança e Controle de Riscos

**P:** Após manutenção, um sistema retorna ao serviço em configuração temporária diferente da rotina. Durante a tarefa, a equipe identifica no campo um perigo relevante que não constava da análise usada para liberar o trabalho. A supervisão deve tratar isso principalmente como falha pontual de execução ou como evidência de falha mais ampla no processo de gestão de riscos, e qual providência técnica deve priorizar antes de continuar?

**R:** Deve tratar principalmente como evidência de falha mais ampla no processo de gestão de riscos. Quando um perigo relevante só é reconhecido durante a execução, isso indica que a identificação de perigos não representou a condição real da operação. Em retorno ao serviço e outras transições, a planta sai da base rotineira; essa condição pode alterar barreiras, ações humanas críticas e limites operacionais, exigindo gestão de mudanças e reavaliação das análises aplicáveis antes da continuidade. A prioridade é interromper a continuidade baseada na análise insuficiente e revisar formalmente a condição operacional: descrever e justificar a mudança, reavaliar os perigos da transição, verificar se a atividade é crítica a ponto de exigir HRA e restabelecer os controles de retorno ao serviço compatíveis com a condição real, como PTW e certificados de isolamento.

- **gpt-5-4-petrobras:medium:** aprova
- **gpt-5-2-petrobras:medium:** reprova (suporte) · Suporte insuficiente para afirmar que transições necessariamente alteram barreiras/ações humanas críticas e que isso, por si, exige reavaliação antes de continuar (não há F# que diga isso explicitamente; F4/F6/F7/F10 apontam requisitos/controles, mas não estabelecem a relação causal completa como redigida).; Recomendação de 'interromper a continuidade' e priorizar revisão antes de continuar é uma orientação operacional substantiva sem ancoragem direta em F# (pode ser boa prática, mas falta suporte literal/expresso no material fornecido).
- **gpt-5-4-petrobras:low:** aprova

### d99fb5d8d3-b1-A1 · dificil_A · SGSO

**P:** Em um FPSO, auditorias sucessivas de SGSO voltam a registrar desvios ligados a elementos críticos, mesmo após correções locais apontadas como concluídas pelas áreas operacionais. Parte dos desvios envolve salvaguardas que não estavam claramente tratadas como críticas no sistema de gestão. Por que esse quadro pode caracterizar falha sistêmica na identificação ou no tratamento dos ECSO, e não apenas falhas isoladas de execução local?

**R:** Porque a repetição de desvios após ações corretivas indica que o tratamento anterior não eliminou a causa de gestão, apenas corrigiu manifestações locais. Quando isso ocorre em elementos críticos, o problema deixa de ser pontual e passa a sugerir insuficiência de abrangência no tratamento dado pelo operador. Se, além disso, há salvaguardas relevantes sem identificação ou classificação consistente como ECSO, a organização tende a monitorar e gerir apenas parte das barreiras críticas. Isso compromete a visão sobre disponibilidade e integridade dessas salvaguardas e revela inconsistência estrutural na definição do que é barreira crítica no SGSO. Nessa condição, a recorrência não é explicada apenas por execução local deficiente, mas por falha sistêmica na identificação dos elementos críticos e/ou na eficácia do tratamento gerencial dos desvios.

- **gpt-5-4-petrobras:medium:** aprova
- **gpt-5-2-petrobras:medium:** reprova (suporte) · Falta de suporte: a resposta afirma comprometimento da visão/monitoramento de disponibilidade e integridade sem fato citado que sustente isso (nos fatos citados não há R22/monitoramento gerencial nem indicadores).; A resposta usa linguagem de monitoramento e integridade/disponibilidade que extrapola o suporte fornecido em F7 e F8; deveria restringir-se ao que está explicitamente suportado ou incluir fatos pertinentes (não citados).
- **gpt-5-4-petrobras:low:** aprova

### d99fb5d8d3-b2-A1 · dificil_B · SGSO

**P:** Após uma reorganização com entrada de pessoal, acúmulo temporário de funções e uso de contratadas em manutenção, os procedimentos da área seguem atuais e acessíveis no sistema. Em campo, ocupantes do mesmo cargo executam a rotina com diferenças em etapas críticas, e os registros mostram apenas treinamentos anteriores, sem evidência específica da transição. Qual é o diagnóstico técnico mais consistente e qual controle deve ser priorizado para restabelecer a efetividade da barreira procedimental?

**R:** O diagnóstico mais consistente é barreira procedimental formalmente disponível, porém degradada por falha de gestão de mudanças de pessoas e de capacitação por função. A mudança de pessoas e o acúmulo de funções alteram a competência disponível e exigem tratamento formal, inclusive para entradas de pessoal. Se a transição não foi acompanhada por capacitação teórica e prática, reciclagem, tutoria prévia para novos integrantes e verificação de entendimento das implicações operacionais, o procedimento pode permanecer vigente no sistema sem ser executado de forma uniforme. A prioridade é aplicar o gerenciamento de mudanças de pessoas à reorganização e reconverter a execução do procedimento em requisito controlado: requisitos mínimos por cargo com avaliação teórica e prática, treinamento nos procedimentos aplicáveis à nova condição, revisão com as equipes de operação e manutenção sobre as implicações da mudança e, para contratadas, evidência de treinamento adequado e acompanhamento por indicadores.

- **gpt-5-4-petrobras:medium:** aprova
- **gpt-5-2-petrobras:medium:** reprova (jurisdicao) · Jurisdicao: uso de F11 (HSE/UK) como se fosse controle obrigatório do SGSO/ANP, sem ressalva de que é expectativa inspetiva estrangeira e deve ser usada apenas como reforço técnico (conforme Nota 2).; Clareza: o enunciado pede 'qual controle deve ser priorizado', mas a resposta lista um pacote de controles; pode ser ajustada para destacar explicitamente a prioridade (aplicar MOC de pessoas + garantir capacitação/avaliação/reciclagem e tutoria na transição) e deixar os demais como complementares.
- **gpt-5-4-petrobras:low:** aprova

### 86765f00dc-b2-A1 · dificil_B · Sistema de Fogo e Gás (F&G)

**P:** Em uma área com potencial de acúmulo de gás inflamável, um detector de estado sólido passou a oscilar e a aparentar perda de sensibilidade em dias com alta umidade, variação térmica e presença intermitente de névoa. A equipe discute trocar o sensor, recalibrar imediatamente ou manter observação. Qual deve ser a prioridade diagnóstica e como distinguir interferência ambiental de deriva real do detector antes de decidir ajuste ou substituição?

**R:** A prioridade é investigar primeiro a correlação da instabilidade com o ambiente e confrontá-la com o histórico metrológico do detector, antes de ajustar ou substituir. Em sensores de estado sólido, umidade e temperatura alteram a adsorção na superfície sensível e podem mudar a resposta para a mesma concentração. Em presença de névoa, a sensibilidade pode variar e a calibração associada tem alta incerteza, reduzindo a confiança em interpretar a oscilação como defeito. Para separar isso de deriva real, a verificação deve comparar o desempenho com padrão usando o mesmo gás de referência no início e no fim do intervalo de ajuste e registrar a tendência ao longo do tempo. Se a variação acompanhar as condições ambientais, sem tendência consistente contra o padrão, não há base para concluir defeito eletrônico nem para recalibração imediata. Se houver desvio recorrente ou anormal frente ao padrão, aí cabe ajuste e, se o comportamento fugir do esperado, investigação de reparo.

- **gpt-5-4-petrobras:medium:** reprova (suporte, sem_generalizacao) · Generalização indevida de F6/F8: a resposta fala em 'névoa' genericamente, mas o fato disponível trata de liberações de óleo ou névoa/mist e da incerteza de calibração nesse cenário.; O suporte fica insuficiente nesse trecho específico, o que reprova a questão mesmo com núcleo diagnóstico bom.
- **gpt-5-2-petrobras:medium:** aprova
- **gpt-5-4-petrobras:low:** reprova (correcao_tecnica, suporte) · Conclusão sem suporte: 'não há base para concluir defeito eletrônico' não decorre dos fatos citados; os fatos só permitem dizer que a variação pode estar associada a interferência ambiental e que desvio anormal pode indicar defeito.; Suporte incompleto para 'névoa' no cenário: os fatos F6/F8 tratam de óleo ou névoa/mist, mas a resposta usa 'névoa' sem qualificar o tipo; isso enfraquece o nexo factual.; Decisão excessivamente assertiva sobre ajuste: F9 permite inferir necessidade de ajuste quando a comparação com padrão mostra desvio, mas a formulação 'aí cabe ajuste' simplifica demais, porque desvio anormal também pode apontar defeito que exija reparo.

### bfc6625c3d-b0-A1 · facil · Sistemas e equipamentos de salvatagem

**P:** O que significa estruturar a resposta a emergências com pontos de encontro distribuídos por função e localização na unidade?

**R:** Significa que a apresentação inicial do pessoal não é concentrada em um único local genérico. A resposta é organizada com pontos de encontro previamente definidos para funções diferentes, em locais distintos da unidade, como comando, atendimento, áreas técnicas, recursos de resposta e refúgio temporário. Assim, cada grupo se dirige ao ponto correspondente à sua função e posição prevista na estrutura de emergência.

- **gpt-5-4-petrobras:medium:** aprova
- **gpt-5-2-petrobras:medium:** reprova (suporte) · Falta de suporte para a expressão 'apresentação inicial do pessoal' (não consta em F1). Pode ser corrigido removendo/ajustando essa parte sem adicionar conteúdo novo.
- **gpt-5-4-petrobras:low:** aprova

### bfc6625c3d-b0-A2 · media · Sistemas e equipamentos de salvatagem

**P:** Em uma emergência, a unidade já possui locais de apresentação previamente definidos para cada função em diferentes áreas, em vez de reunir todos no mesmo ponto. Como essa definição tende a influenciar a organização inicial da resposta, a concentração de equipes e a contabilização de pessoal?

**R:** Ela tende a organizar a resposta desde o início, porque cada função já tem um local esperado de apresentação. Isso evita reunir todo o pessoal em um único ponto, distribuindo as equipes conforme sua função e sua posição na estrutura de emergência. Também favorece a contabilização por grupos e locais previamente definidos, porque a verificação passa a ser feita onde cada função deve se apresentar.

- **gpt-5-4-petrobras:medium:** aprova
- **gpt-5-2-petrobras:medium:** reprova (suporte) · Falta de suporte: os efeitos afirmados (organização inicial, redução de concentração e melhoria da contabilização) não estão contidos no fato F1 nem em qualquer outro F# fornecido; a resposta introduz mecanismo/benefício sem base factual citada.
- **gpt-5-4-petrobras:low:** aprova

### bfc6625c3d-b1-A1 · dificil_A · Sistemas e equipamentos de salvatagem

**P:** Em um abandono noturno, a rota até a estação de life raft permanece fisicamente desobstruída e a balsa throw-over está a bordo. Porém, o único meio de descer ao nível do mar é uma rede de escalada, o acesso à painter line só seria possível já dentro d’água, e o ponto de lançamento fica sujeito a radiação térmica e fumaça sem proteção dedicada. A estação tem iluminação de emergência, mas o trecho final da rota pode perder visibilidade se a iluminação normal falhar. Esse arranjo torna a cadeia acesso–descida–alcance da balsa–embarque realmente viável?

**R:** Não. A cadeia falha em mais de uma etapa crítica. A rede de escalada não caracteriza meio controlado de descida, porque depende de força e destreza sob emergência. Além disso, se a pessoa só consegue alcançar a painter line após entrar na água, o arranjo passa a depender da entrada física no mar como etapa prática do acesso à balsa, e isso deve ser tratado como último recurso, não como solução normal de abandono. O ponto de lançamento e embarque também não atende ao critério de viabilidade se permanece exposto à radiação térmica, e a rota final não pode ser considerada disponível se pode perder condições de uso por fumaça ou falha de iluminação sem proteção ou iluminação adequada. Ter rota física e balsa disponível não basta; o abandono só é executável quando acesso, descida, conexão com a balsa e lançamento/embarque permanecem utilizáveis nas condições do cenário.

- **gpt-5-4-petrobras:medium:** aprova
- **gpt-5-2-petrobras:medium:** reprova (correcao_tecnica, suporte) · Falta de suporte para exigir/avaliar iluminação de emergência ao longo da rota (os fatos só exigem iluminação de emergência na estação: F3).; Falta de suporte para tratar 'fumaça no ponto de lançamento/embarque' como critério (F3 trata proteção SFAIRP contra radiação térmica; F4 trata fumaça em rotas, não no ponto).; Para ficar suportada, a resposta deve restringir-se a: (i) descida não controlada (F1), (ii) necessidade de seguir/acessar painter line sem depender de entrar no mar (F1/F2), (iii) proteção SFAIRP contra radiação térmica no ponto de lançamento/embarque (F3), (iv) proteção contra fumaça etc. nas rotas quando necessário (F4), sem introduzir requisito novo de iluminação nas rotas.
- **gpt-5-4-petrobras:low:** reprova (suporte) · Falta de suporte específico para a afirmação sobre perda de uso da rota por falha de iluminação; os fatos citados só sustentam iluminação de emergência na estação, não na rota.; A resposta mistura corretamente fumaça/radiação térmica com um elemento de iluminação da rota que excede o suporte factual disponível.

### bfc6625c3d-b2-A1 · dificil_B · Sistemas e equipamentos de salvatagem

**P:** Após a indisponibilidade de um meio de evacuação, uma área da unidade passa a depender de rota alternativa até o escape-to-sea. Essa rota cruza zona com potencial de fumaça e radiação térmica, e o abandono pode atrasar, aumentando o tempo de permanência no Temporary Refuge (TR). Qual critério técnico deve orientar a decisão sobre a aceitabilidade dessa condição degradada?

**R:** A condição só é aceitável se a degradação não romper a cadeia completa de abandono. Isso exige verificar, primeiro, se ainda existe rota segura e efetivamente disponível até o escape-to-sea, sem dependência de um único percurso vulnerável; segundo, se a rota remanescente e os pontos de embarque permanecem utilizáveis pelo tempo requerido sob fumaça e radiação térmica; e, terceiro, se o TR suporta a maior permanência com habitabilidade preservada. Nessa verificação, o TR não pode ser tratado apenas como compartimento existente: sua proteção contra sobrepressão, suas condições atmosféricas internas admissíveis e a confiabilidade de detecção de fumaça, gás e funções de desligamento precisam sustentar permanência segura. Se a perda do meio de evacuação transfere a proteção para um TR degradado ou para rota que não sobreviva ao cenário, a condição não é aceitável.

- **gpt-5-4-petrobras:medium:** reprova (suporte) · A resposta introduz requisito sem suporte ao afirmar que pontos de embarque precisam permanecer utilizáveis 'pelo tempo requerido sob fumaça'; F9 não cobre isso.; Há leve ampliação de F1 ao formular 'sem dependência de um único percurso vulnerável' como critério geral, quando o fato explicita isso para áreas vulneráveis.
- **gpt-5-2-petrobras:medium:** reprova (suporte) · Suporte: a resposta usa 'confiabilidade' de sistemas (fumaça/gás/ESD) como requisito explícito; F2/F3 falam em KPIs/trending e evitar 'fix on fault', mas não estabelecem diretamente um critério de 'confiabilidade' (termo pode ser mantido apenas se ancorado como 'desempenho monitorado/trendado').; Suporte: aplica 'pelo tempo requerido' também aos 'pontos de embarque'; F6 cobre 'access routes' e F9 cobre proteção/iluminação em estações de baleeiras, mas não explicita endurance para pontos de embarque. Dá para corrigir restringindo endurance às rotas e mantendo para pontos de embarque apenas proteção térmica/iluminação conforme F9.; Redação: a resposta mistura critérios de projeto (sobrepressão na fase de projeto) e de operação (KPIs/trending) sem marcar claramente a natureza de cada verificação; pode ser ajustado sem conteúdo novo.
- **gpt-5-4-petrobras:low:** aprova

### 028022ae6b-b2-A1 · dificil_B · Sistema de utilidades

**P:** Durante o retorno de um sistema de heating medium em fase líquida, o queimador principal entra em serviço sem confirmação confiável de circulação. Em seguida, a temperatura a jusante da câmara de combustão sobe e a pressão do circuito aumenta rapidamente. Qual é o diagnóstico mais provável para a falha da proteção e quais barreiras deveriam ter atuado, em ordem funcional, antes que o evento evoluísse para perda de contenção e incêndio?

**R:** O diagnóstico mais provável é falha da permissiva/intertravamento que deveria bloquear a admissão de combustível ao queimador sem circulação comprovada. Com a fonte térmica ativa e sem escoamento, o calor deixa de ser removido da região aquecida, o fluido superaquece, expande e eleva rapidamente a pressão. Se a progressão continuar, o tanque de expansão pode romper, com extravasamento sobre superfícies quentes e ignição. A sequência correta de barreiras é: primeiro, bloqueio da válvula de combustível quando as bombas de circulação não estiverem operando; segundo, detecção contínua da anomalia por sensores de temperatura imediatamente a jusante da câmara de combustão; terceiro, limitação das consequências mecânicas por tanque de expansão com classificação de pressão adequada e válvula de alívio secundária de grande capacidade.

- **gpt-5-4-petrobras:medium:** reprova (tipo_ok) · Tipo difícil_B não atendido: a questão não torna indispensável integrar notas distintas; a Nota 1 já basta para responder.; A formulação 'sem confirmação confiável de circulação' é respondida com o critério factual de bombas em operação; isso é próximo, mas menos preciso do que explicitar a base do intertravamento em F6.
- **gpt-5-2-petrobras:medium:** reprova ()
- **gpt-5-4-petrobras:low:** aprova

### 332e35e913-b0-A2 · media · Gestão do Desempenho Empresarial (KPI)

**P:** Um elemento crítico de segurança (SCE) foi identificado como degradado e a unidade avalia continuar operando com mitigação temporária. Quais elementos de governança devem existir nessa avaliação de risco para sustentar a decisão?

**R:** Deve existir um procedimento formal de gestão que defina o processo de avaliação de risco, os níveis de autoridade para decidir, a expertise técnica que precisa participar e os requisitos de revisão. A avaliação deve considerar o papel do SCE como barreira contra acidentes maiores, para sustentar mitigação temporária e, se necessário, barreiras adicionais. As avaliações precisam ser registradas e auditadas regularmente. Também deve haver revisões gerais periódicas com nível apropriado de expertise, sem depender só da gestão offshore, porque o risco combinado pode ser excessivo mesmo quando avaliações individuais pareçam adequadas. Além disso, dados de KPI, auditorias e demais informações de desempenho devem ser reportados ao nível sênior com ações decorrentes.

- **gpt-5-4-petrobras:medium:** aprova
- **gpt-5-2-petrobras:medium:** aprova
- **gpt-5-4-petrobras:low:** reprova (jurisdicao, sem_generalizacao) · Apresenta requisitos de fatos de jurisdição UK como obrigação geral, sem ressalva de contexto jurisdicional.; Generaliza orientação de fonte específica como regra universal.

### 332e35e913-b2-A1 · dificil_B · Gestão do Desempenho Empresarial (KPI)

**P:** Em um FPSO sob preço de petróleo pressionado, a gestão reforça metas de reduzir OPEX e manter produção. Nas semanas seguintes, margem e volume melhoram, mas há adiamento de intervenções e desvios operacionais que afetam funções de segurança. Ao revisar o painel estratégico, qual mudança de desenho é prioritária para decidir se o ativo está realmente criando valor, e por quê?

**R:** A revisão prioritária é deixar de avaliar custo e produção como resultados isolados e passar a conectá-los, no mesmo encadeamento causal, às variáveis que mostram o efeito dos desvios de operação e manutenção sobre funções de segurança e sobre o resultado econômico. O painel deve traduzir a estratégia por variáveis-chave inter-relacionadas e selecionar indicadores capazes de monitorar o impacto desses eventos nos resultados. Isso é necessário porque, sob pressão de margem, reduzir gasto ou adiar intervenção pode aparentar ganho local, mas também degradar ou inibir funções de segurança, elevando a frequência ou a severidade de cenários de risco. Como acidentes de processo afetam fortemente a sustentabilidade do negócio, melhora de margem sem essa leitura integrada pode apenas deslocar perda futura para a frente. A revisão deve, portanto, impedir que produção e OPEX premiem decisões que destruam rentabilidade do ativo quando considerado o risco total.

- **gpt-5-4-petrobras:medium:** aprova
- **gpt-5-2-petrobras:medium:** reprova (suporte) · Falta de suporte para as afirmações de consequência econômica específica e prospectiva (‘deslocar perda futura’, ‘destruir rentabilidade’) e para o mecanismo de ‘premiar’ decisões como efeito do painel, que não aparecem de forma explícita nos F# citados.
- **gpt-5-4-petrobras:low:** aprova

### b56db319e4-b0-A1 · facil · Logística e Suprimento Offshore

**P:** Por que a eliminação do umbilical em operações com AUV reduz a exigência sobre o sistema de lançamento e sobre a embarcação de apoio, especialmente em maiores profundidades?

**R:** Porque, sem umbilical, a operação deixa de depender de recursos de lançamento mais robustos associados ao manejo contínuo do veículo pela superfície, como guincho e pórtico com compensação de heave. Isso simplifica o lançamento e reduz a carga operacional e estrutural imposta à embarcação de apoio. Esse efeito aumenta com a profundidade, pois a redução de exigências ligadas ao lançamento e à recuperação se torna mais relevante à medida que a operação ocorre em lâminas d’água maiores.

- **gpt-5-4-petrobras:medium:** reprova (suporte) · A resposta introduz a ideia de 'carga estrutural' sobre a embarcação de apoio, que não está sustentada pelos fatos citados.; O suporte factual ficou incompleto para uma parte substantiva da conclusão sobre a embarcação de apoio.
- **gpt-5-2-petrobras:medium:** aprova
- **gpt-5-4-petrobras:low:** aprova

### b56db319e4-b2-A1 · dificil_B · Logística e Suprimento Offshore

**P:** Um FPSO, com pouco espaço para armazenagem, pede na mesma viagem de PSV contêineres de materiais para uma manutenção programada, consumíveis necessários à operação corrente e alguns volumes longos que não podem ser girados. Pela lista de pesos, tudo caberia; no arranjo real, sem empilhamento, o convés não fecha. A manutenção pode ser reprogramada sem parada imediata, mas a falta dos consumíveis afeta a continuidade operacional. Como o embarque deve ser reordenado e qual é o limitante técnico que governa essa decisão?

**R:** O embarque deve ser reordenado pelo impacto da postergação, não pela tonelagem total. Como o PSV é limitado no convés por área útil e geometria de arrumação, sem empilhamento e sem rotação, o gargalo real é a carga de convés. Portanto, devem entrar primeiro os consumíveis cuja falta compromete a continuidade operacional da unidade, e devem ser postergados ou fracionados os materiais de manutenção reprogramável e os volumes de geometria desfavorável que consumam área crítica no convés. O fato de a lista de pesos parecer compatível não resolve a viagem se os itens não puderem ser acomodados na orientação permitida. Em unidade com pouca armazenagem, a prioridade prática é selecionar o conjunto de cargas que caiba fisicamente no convés e reduza o risco de interrupção do trabalho a bordo.

- **gpt-5-4-petrobras:medium:** reprova (suporte) · A resposta inclui 'fracionados' como medida para os itens não priorizados, mas essa ação não está sustentada por F7, F8 ou F11 nos termos exigidos.; Os fatos citados sustentam bem o diagnóstico do limitante e a priorização, porém não cobrem integralmente todas as medidas operacionais mencionadas na resposta.
- **gpt-5-2-petrobras:medium:** aprova
- **gpt-5-4-petrobras:low:** aprova

### 26d45ade58-b0-A1 · facil · Movimentação de Cargas

**P:** Qual é a função do lifting plan na operação de içamento e como ele se relaciona com a definição do equipamento a ser utilizado?

**R:** O lifting plan funciona como a instrução operacional da atividade: ele descreve a execução em passos e define o equipamento que deve ser usado no içamento. Por isso, ele vincula a equipe a um método previamente validado para aquela operação, em vez de deixar a escolha do modo de executar e dos recursos ao ajuste informal em campo.

- **gpt-5-4-petrobras:medium:** aprova
- **gpt-5-2-petrobras:medium:** reprova (suporte) · Falta de suporte para o contraste 'em vez de deixar ... ao ajuste informal em campo' (sem fato correspondente).; O trecho sobre 'vincular a equipe a um método previamente validado' depende de inferência; para ficar estritamente suportado, deveria mencionar apenas que o plano é produzido/autorizado por Pessoa Competente (F1), sem extrapolações.
- **gpt-5-4-petrobras:low:** aprova

### a807dbd01e-b2-A1 · dificil_B · Apoio Técnico e Manutenção em um FPSO (Laboratório, Oficinas, Pipe Shop)

**P:** Em uma auditoria interna de um FPSO, há recomendações antigas de inspeção para equipamentos críticos com status divergente entre sistemas. Parte dos reparos foi executada, mas os registros não ligam claramente achado, recomendação, prazo, testes/ensaios de aceitação e aprovação técnica para retorno ao serviço. A operação afirma que os itens foram tratados. Qual deve ser o diagnóstico prioritário e por que esse quadro pode sustentar risco de interdição mesmo com manutenção já realizada?

**R:** O diagnóstico prioritário é deficiência de gestão da integridade com perda de rastreabilidade do ciclo achado-recomendação-ação-verificação-fechamento, e não simples comprovação de atraso ou de reparo físico isolado. Em equipamentos críticos, a recomendação só reduz risco quando entra em sistemática formal com classificação, prazo compatível com o risco, controle de qualidade por inspeções, testes e ensaios e acompanhamento até fechamento. Se os registros não conectam a condição observada à intervenção executada, nem mostram a justificativa técnica para retorno ao serviço, não há evidência verificável de que o dano relevante foi tratado nem de que o item pode continuar operando com segurança. Essa lacuna mascara falsa sensação de controle, impede priorização por risco e fragiliza o autodiagnóstico e a demonstração de contingência e correção em tempo adequado, condição que pode evoluir para interdição.

- **gpt-5-4-petrobras:medium:** aprova
- **gpt-5-2-petrobras:medium:** reprova (suporte) · Falta de suporte: a exigência de 'justificativa/aprovação técnica documentada para retorno ao serviço' não está coberta por nenhum fato F# fornecido (F5 cobre QC para aprovar o serviço executado, mas não a decisão formal de retorno ao serviço).; A resposta poderia permanecer correta e suportada se substituísse essa parte por 'evidência de inspeções/testes/ensaios para aprovar o serviço executado' (F5), mas do jeito que está há conteúdo técnico novo sem base factual.
- **gpt-5-4-petrobras:low:** reprova (suporte) · Há falta de suporte explícito para a parte da resposta que exige 'justificativa técnica para retorno ao serviço'; os fatos citados/disponíveis não trazem essa exigência de forma direta.; A formulação 'fechamento' do ciclo está tecnicamente coerente, mas parte dela excede o texto factual disponível ao pressupor autorização documentada de retorno ao serviço.

### e1b6ad83e3-b2-A1 · dificil_B · Cibersegurança e Integridade de Sistemas Digitais

**P:** Após ampliar a integração entre OT e camadas superiores de um FPSO, a sala de controle passou a perceber IHMs mais lentas, eventos inconsistentes e dificuldade para entender desvios. Em uma perturbação, surgiu grande volume de mensagens e a equipe não conseguiu decidir se a limitação principal estava na arquitetura de conectividade/acesso remoto ou na configuração de alarmes e diagnósticos. Qual diagnóstico deve ser priorizado para separar essas causas?

**R:** A separação deve começar por três sinais. Se a perda de apoio aparece como degradação ampla de acesso, visualização e monitoramento entre camadas, o foco inicial é a arquitetura de conectividade, porque a rede integrada é a base que torna informações e suporte remoto disponíveis de forma coordenada. Se o sintoma dominante é excesso de alarmes já em estado normal, com piora do tempo de resposta, o problema principal é a gestão de alarmes; se, durante a atuação do SIS, ocorre avalanche de alarmes, isso caracteriza configuração deficiente. Se os alarmes existem, mas a equipe continua sem distinguir falha de processo, de PLC, de rede ou condição transitória de instrumento, a prioridade passa a ser a camada de diagnósticos e IHM: gerar diagnósticos nos controladores e carregá-los de forma coerente em banco de dados, supervisório e painel.

- **gpt-5-4-petrobras:medium:** aprova
- **gpt-5-2-petrobras:medium:** reprova (suporte) · Falta de suporte/citação para a enumeração específica de causas (processo vs PLC vs rede vs transitório de instrumento) com os fatos atualmente citados; ajustar citando F23/F24 e/ou reescrevendo para não introduzir categorias não suportadas.; A resposta usa 'degradação ampla de acesso/visualização/monitoramento' como sinal de problema de conectividade; isso é plausível, mas poderia ficar melhor amarrado aos fatos explicitando que a integração viabiliza monitoramento remoto e acesso (F3/F4) e que a integração melhora correlação/diagnóstico de causas-raiz (F1).
- **gpt-5-4-petrobras:low:** reprova (suporte) · A resposta introduz distinções específicas ('falha de processo, de PLC, de rede ou condição transitória de instrumento') sem suporte nos fatos citados da questão.; Para sustentar 'condição transitória de instrumento' seria necessário fato correspondente como F23; para diagnósticos de rede, F24 seria pertinente, mas não foi citado.; Como a exigência é de suporte por fatos citados ou da nota, a resposta fica sem lastro completo e deve ser reprovada por suporte insuficiente.

### 460979b6f3-b0-A1 · facil · Inspeção e Integridade

**P:** O que é Inspeção Baseada em Risco e como a combinação de probabilidade e consequência de falha é usada para priorizar inspeção e manutenção em equipamentos de processo?

**R:** Inspeção Baseada em Risco é uma metodologia em que o risco orienta as decisões de inspeção e manutenção, em vez de distribuir recursos de forma uniforme. Para isso, o plano deve ser coerente com os mecanismos de dano de cada equipamento e usar o histórico operacional para atualizar o risco. A priorização resulta da combinação, por meios qualitativos e quantitativos, da probabilidade de falha com a consequência de falha. Com essa combinação, os equipamentos de maior risco relativo são identificados para receber inspeção e manutenção antes dos demais.

- **gpt-5-4-petrobras:medium:** aprova
- **gpt-5-2-petrobras:medium:** reprova (suporte) · Falta de suporte explícito (nos fatos citados F1/F2) para a afirmação 'em vez de distribuir recursos de forma uniforme'. Remover ou reformular para algo diretamente coberto por F1/F2 (ex.: 'o risco orienta as decisões e define prioridades').
- **gpt-5-4-petrobras:low:** aprova

### 460979b6f3-b1-A1 · dificil_A · Inspeção e Integridade

**P:** Uma unidade pretende usar inspeção subaquática em substituição à docagem. Na revisão do programa, a equipe propõe concentrar o exame no costado externo e tratar separadamente os compartimentos internos, enquanto no espaço de máquinas há pontos sensíveis junto ao topo do tanque, brackets, anteparas e poços de bilge, além de conexões laterais do casco com válvulas e tubulações associadas. Que lógica de inspeção deve prevalecer para preservar o envelope do casco?

**R:** Deve prevalecer uma lógica única de integridade do envelope, não uma separação entre costado externo, compartimentos internos e conexões laterais. O plano formal precisa cobrir o envelope externo para suportar a UWILD e, ao mesmo tempo, incluir os compartimentos e arranjos estruturais cujo estado confirma se a resistência e a estanqueidade permanecem eficazes. No espaço de máquinas, as regiões da chapa do costado junto aos brackets, as anteparas na zona do topo do tanque e os poços de bilge merecem atenção específica, porque são interfaces críticas de dano estrutural. As conexões laterais do casco, com válvulas e tubulações associadas, entram na mesma lógica porque podem comprometer diretamente a estanqueidade. O exame visual deve ser complementado por medições de espessura e testes sempre que necessário para identificar corrosão substancial, deformações, fraturas, danos e outras deteriorações antes de decidir reparo ou renovação.

- **gpt-5-4-petrobras:medium:** reprova (suporte, jurisdicao) · A resposta universaliza como obrigação geral o uso de plano formal de inspeção para UWILD com base em referência HSE/UK (F2), sem qualificação jurisdicional.; A expressão 'antes de decidir reparo ou renovação' introduz conteúdo decisório não sustentado explicitamente por F1-F4.
- **gpt-5-2-petrobras:medium:** aprova
- **gpt-5-4-petrobras:low:** reprova (suporte) · Falta de suporte explícito em F1-F4 para a afirmação sobre decidir 'reparo ou renovação'.; A resposta introduz consequência de manutenção específica não coberta pelos fatos citados na questão.

### 1c3fa83845-b0-A1 · facil · Instrumentação, Controle e Automação

**P:** Por que a calibração periódica manual pode reduzir a disponibilidade do processo e nem sempre ser a melhor estratégia de manutenção de instrumentos?

**R:** Porque a calibração manual periódica frequentemente exige retirar o instrumento de operação e, em muitos casos, parar o processo. Isso reduz a disponibilidade. Além disso, intervir por calendário não garante necessidade técnica: uma parcela pequena das calibrações manuais tende a ser realmente necessária, e a própria intervenção manual pode afetar negativamente a confiabilidade do instrumento. Por isso, quando as leituras podem ser validadas em operação e o comportamento permanece estável, faz mais sentido condicionar a intervenção à evidência de degradação metrológica do que executar recalibrações físicas de rotina.

- **gpt-5-4-petrobras:medium:** aprova
- **gpt-5-2-petrobras:medium:** reprova (suporte) · Falta de suporte explícito (nos fatos citados) para os critérios ‘comportamento permanece estável’ e ‘condicionar à evidência de degradação metrológica’.; A resposta pode ser ajustada para ficar 100% ancorada em F1, removendo/encurtando o trecho prescritivo sobre validação em operação e degradação.
- **gpt-5-4-petrobras:low:** aprova

### 1c3fa83845-b1-A1 · dificil_A · Instrumentação, Controle e Automação

**P:** Em uma unidade offshore, um transmissor de pressão envia HART sobre 4–20 mA, enquanto a automação usa FOUNDATION Fieldbus e a supervisão remota usa servidor OPC-DA com cliente Web. A medição existe em campo, mas a equipe quer garantir que ela chegue até a visualização remota. Por que essa arquitetura precisa tratar a integração em duas camadas distintas, e o que cada camada deve cumprir para que a variável fique disponível de ponta a ponta?

**R:** Porque há dois problemas técnicos diferentes na cadeia. Primeiro, a variável precisa sair do domínio elétrico/comunicacional do instrumento e entrar no barramento digital da automação. Quando o instrumento fornece 4–20 mA, 0–20 mA ou HART sobre 4–20 mA e a rede é FOUNDATION Fieldbus, isso exige um conversor intermediário; sem essa interface, a variável não chega ao sistema fieldbus. Segundo, depois de recebida na automação, a variável ainda precisa ser organizada para consumo supervisório. Para isso, os dados são mapeados, recebem endereçamento padronizado e são armazenados no servidor OPC-DA; é essa base que o cliente Web usa para publicar a informação. Assim, a primeira camada condiciona a entrada da variável na rede de automação, e a segunda condiciona sua disponibilização na supervisão remota.

- **gpt-5-4-petrobras:medium:** aprova
- **gpt-5-2-petrobras:medium:** reprova ()
- **gpt-5-4-petrobras:low:** aprova

### 1c3fa83845-b2-A1 · dificil_B · Instrumentação, Controle e Automação

**P:** Em um separador trifásico, a malha que tenta manter a interface estável passa a oscilar quando a composição interna varia, e a mesma variável também é cogitada para gerar desarme por interface de água criticamente baixa. A unidade dispõe de radar de onda guiada e de medição nucleônica de densidade em pontos distintos do vaso. Qual escolha de medição e de atuação é mais coerente para controle contínuo e proteção, e por quê?

**R:** A escolha mais coerente é usar, para a malha de interface e para a proteção por interface criticamente baixa, a medição de densidade aplicada ao ponto do vaso onde essa interface é operacionalmente relevante, com elemento final de controle de posicionamento contínuo. A interface entre fases pode ser inferida por densidade e esse tipo de medição pode alimentar o controlador e também a lógica de desarme. Já o radar de onda guiada mede pela reflexão na descontinuidade dielétrica; quando a composição muda, a qualidade do eco depende do contraste de constante dielétrica entre os meios, o que pode tornar o sinal menos robusto para a finalidade de controle. Além disso, mesmo uma medição fisicamente correta degrada a malha se sua resposta dinâmica ou as condições de instalação atrasarem ou deformarem as variações relevantes, porque o controlador passa a atuar sobre um sinal inadequado. Para controle proporcional, a atuação não deve ser liga-desliga.

- **gpt-5-4-petrobras:medium:** aprova
- **gpt-5-2-petrobras:medium:** reprova (suporte) · Falta de suporte explícito (por fatos citados) para 'condições de instalação' como fonte de erro/degradação (necessitaria de F8).; Falta de suporte explícito (por fatos citados) para a característica 'posicionamento contínuo' (seria sustentado diretamente por F11; com os fatos atuais, só fica parcialmente inferido a partir de F12).
- **gpt-5-4-petrobras:low:** aprova

### d21b4ace38-b0-A2 · media · Manutenção e Plano de Manutenção

**P:** Após o encerramento técnico dos serviços, a engenharia de manutenção consolida indicadores e histórico no sistema e percebe recorrência de intervenções e lacunas de reposição. Como esse histórico pode gerar recomendações sobre planos de manutenção e sobressalentes?

**R:** O histórico e os indicadores extraídos do sistema permitem analisar o comportamento das falhas e das intervenções já executadas. A partir dessa análise, a engenharia pode encaminhar para a gestão recomendações de melhoria em planos existentes, criação de novos planos e inclusão de itens em estoque. Quando associados aos resultados de estudos de FMEA, esses dados ajudam a revisar o plano conforme a necessidade observada no histórico, em vez de manter tarefas e reposições sem base nos registros consolidados.

- **gpt-5-4-petrobras:medium:** aprova
- **gpt-5-2-petrobras:medium:** reprova (suporte) · Falta de suporte explícito para 'analisar o comportamento das falhas' (F5 não menciona falhas, apenas histórico de serviços/indicadores).; Falta de suporte explícito para o contraste normativo/valorativo 'em vez de manter tarefas e reposições sem base nos registros' (não está em F5).
- **gpt-5-4-petrobras:low:** aprova

### d21b4ace38-b1-A1 · dificil_A · Manutenção e Plano de Manutenção

**P:** Após manutenção em um sistema de armazenamento com tanques de carga e de armazenamento de água, o supervisório mostra barreiras e intertravamentos como disponíveis. Na inspeção de campo, a equipe encontra uma válvula crítica fora da posição normal, um vent sem recomposição correta e dúvida sobre a remoção de um isolamento temporário. A produção pode ser mantida com contingência provisória, mas sem evidência de que o arranjo real voltou à condição de projeto. O retorno ao serviço é tecnicamente defensável?

**R:** Não. A disponibilidade aparente no supervisório, sozinha, não confirma a barreira. Após manutenção, é necessário verificar em campo se o equipamento foi recomposto conforme o projeto, com remoção de isolamentos temporários, retorno de válvulas críticas à posição normal, posicionamento correto de vents e alinhamento dos dispositivos protetivos. Em sistema de armazenamento, também é preciso confirmar aderência entre a condição operacional observada e a condição de projeto. Como há incoerências de campo e não se comprovou o arranjo pretendido, a barreira está apenas nominalmente disponível. Nesse quadro, a continuidade só seria defensável se a contingência residual mantivesse o risco em nível aceitável; se isso não puder ser demonstrado, deve-se restringir a operação ou parar o equipamento, o sistema associado ou a planta, conforme necessário.

- **gpt-5-4-petrobras:medium:** aprova
- **gpt-5-2-petrobras:medium:** reprova (correcao_tecnica, suporte, jurisdicao) · Conclusão inicial absoluta ('Não') conflita com a possibilidade prevista em F4 (operação pode continuar se contingência suficiente mantiver risco aceitável); precisa ser condicionada ao não atendimento das verificações/contingências.; Uso de F3 (HSE/UK) como obrigação sem qualificar como boa prática/diretriz; falha de jurisdição e de suporte no sentido normativo (não pode parecer requisito brasileiro).; Pequena inconsistência de redação: o texto diz 'não é defensável', mas em seguida admite defensabilidade se contingência mantiver risco aceitável; precisa harmonizar a resposta.
- **gpt-5-4-petrobras:low:** reprova (suporte, jurisdicao) · A resposta apresenta itens de checagem de F3 como exigência geral sem qualificar que o suporte vem de fonte UK, criando problema de jurisdição.; Há leve insuficiência de suporte/jurisdição na formulação normativa baseada em F3; seria preciso reescrever para não tratar a referência estrangeira como obrigação brasileira.

### d21b4ace38-b2-A1 · dificil_B · Manutenção e Plano de Manutenção

**P:** Em um FPSO, a falha de um componente importante para continuidade operacional exigiu reparo físico simples, mas a parada durou muito mais que o previsto porque a peça não estava disponível, a compra só começou após a falha e houve recorrência de fretes emergenciais e ordens emitidas sem material assegurado. Qual diagnóstico estrutural melhor explica a indisponibilidade prolongada e qual priorização de gestão tende a reduzir esse padrão?

**R:** O quadro indica que a indisponibilidade foi ampliada mais pela prontidão logística do que pela complexidade técnica do reparo. A causa estrutural mais consistente é a combinação de gestão fraca de sobressalentes críticos com integração insuficiente entre plano de manutenção, materiais e compras. Itens relevantes devem ser priorizados pelo impacto da falha, risco associado, taxa de falha, quantidade instalada e lead time, e não só por consumo histórico ou custo da peça. Se a ordem é emitida sem verificação, reserva ou ressuprimento antecipado, a restauração passa a depender de compra reativa, aumentando atraso, erro de especificação e risco de desvio de qualidade. A prioridade é integrar o CMMS ao microplanejamento de materiais e ao ressuprimento, dimensionando sobressalentes críticos por risco e lead time para que a programação já nasça executável.

- **gpt-5-4-petrobras:medium:** aprova
- **gpt-5-2-petrobras:medium:** reprova (suporte) · Falta de suporte: menção a 'consumo histórico' como critério inadequado não é suportada por nenhum F# citado.; Falta de suporte: afirmação de que a priorização não deve ser guiada por 'custo da peça' não é suportada por nenhum F# citado (os fatos não trazem esse critério como inadequado).
- **gpt-5-4-petrobras:low:** reprova (suporte) · Afirmação sem suporte explícito nos fatos citados: 'e não só por consumo histórico'.; A resposta menciona 'a programação já nasça executável', ideia coerente com as notas, mas não explicitamente sustentada pelos fatos citados dessa questão.

### 3204097d51-b1-A1 · dificil_A · Condições Ambientais e Impactos Operacionais

**P:** Em uma área interna próxima à exaustão de gases e produtos de combustão, o monitor de gases foi especificado com base na temperatura externa média. Ao longo do dia, a carga do processo varia, o local aquece em alguns turnos e há períodos de pouca ventilação. Que avaliação técnica deve ser feita para decidir se o sistema de medição continua adequado nessa condição?

**R:** A decisão deve ser baseada na temperatura do ponto realmente monitorado, não na condição externa. É preciso verificar se as variações térmicas ao longo do dia, somadas ao regime operacional, deslocam a faixa de valores esperada a ponto de comprometer o fundo de escala e a adequação da medição. Também é necessário caracterizar a composição do fundo gasoso no local, porque gases presentes fora da espécie de interesse podem introduzir leituras equivocadas. Como há pouca ventilação em certos períodos, a análise deve incluir a possibilidade de condensação e seu efeito sobre a viabilidade da medição. Por fim, o regime de exposição do sensor ao ambiente real deve entrar no critério, porque a adequação depende das condições efetivas de operação e não apenas da condição nominal escolhida para operação normal.

- **gpt-5-4-petrobras:medium:** aprova
- **gpt-5-2-petrobras:medium:** reprova (correcao_tecnica, suporte) · Falta de suporte: resposta inclui composição de fundo gasoso/interferentes, ventilação/condensação e regime de exposição como critério sem haver fato correspondente em F1.; Como o alvo A1 exige integrar temperatura local + composição de fundo gasoso + ventilação + regime de exposição, mas o material fornecido como fato (F1) não sustenta esses itens, não é possível corrigir apenas por redação mantendo o mesmo material.
- **gpt-5-4-petrobras:low:** aprova

### 7408dc2a56-b0-A1 · facil · Gestão de Pessoas e Treinamento

**P:** Qual a diferença entre uma matriz de treinamentos mandatórios gerais e uma matriz de treinamentos em procedimentos operacionais por função, e o que cada uma comprova ou não comprova?

**R:** A matriz de treinamentos mandatórios gerais comprova a cobertura de cursos obrigatórios aplicáveis à força de trabalho, com evidência formal e documentada do que foi realizado. Ela não comprova, por si só, que a pessoa foi treinada nos procedimentos operacionais específicos que executa na função nem que diferenças de competência entre ocupantes do mesmo cargo foram controladas. Já a matriz de treinamentos em procedimentos operacionais por função vincula a necessidade de capacitação ao cargo e às atividades efetivamente executadas, permitindo demonstrar aderência do treinamento à função e evidência de competência para operar conforme os procedimentos aplicáveis.

- **gpt-5-4-petrobras:medium:** reprova (suporte) · Uma afirmação substantiva da resposta não está suportada pelos fatos citados: controle de diferenças de competência entre ocupantes do mesmo cargo.; A resposta poderia ficar integralmente suportada se limitasse o contraste ao que F1, F2, F8 e F9 efetivamente demonstram: cursos obrigatórios gerais versus treinamento em procedimentos operacionais por função.
- **gpt-5-2-petrobras:medium:** reprova (correcao_tecnica, suporte, sem_generalizacao) · Extrapolação sem suporte: ‘controlar diferenças de competência entre ocupantes do mesmo cargo’.; Extrapolação/erro conceitual potencial: tratar matriz/treinamento documentado como ‘evidência de competência’ (treinamento registrado não é, por si, comprovação de competência).; Formulação imprecisa: atribui à ‘matriz’ a ‘evidência formal e documentada do que foi realizado’; os fatos sustentam a exigência de treinamento formal/documentado e manutenção de evidências, mas não que a matriz, isoladamente, seja essa evidência.
- **gpt-5-4-petrobras:low:** aprova

### ba30ee0893-b0-A1 · facil · Meio Ambiente, Gestão Ambiental e Sustentabilidade

**P:** Qual é a função de sistemas rigorosos de gestão de saúde, segurança, social e ambiental na avaliação e minimização de riscos em operações offshore com potencial de impacto ao ambiente marinho?

**R:** Fornecer à operação capacidade estruturada para avaliar e minimizar riscos e para desenvolver processos que reduzam impactos negativos ao ambiente marinho. Na prática, esses sistemas organizam a prevenção, o controle e a resposta de modo que a proteção ambiental seja tratada como parte da gestão dos riscos operacionais.

- **gpt-5-4-petrobras:medium:** aprova
- **gpt-5-2-petrobras:medium:** aprova
- **gpt-5-4-petrobras:low:** reprova (suporte) · Há falta de suporte estrito para parte da resposta com base no fato citado (F1).; A resposta introduz conteúdo adicional sobre prevenção, controle, resposta e integração com gestão de riscos operacionais sem amarração explícita ao fato listado.

### ba30ee0893-b1-A1 · dificil_A · Meio Ambiente, Gestão Ambiental e Sustentabilidade

**P:** Em um projeto de FPSO, duas alternativas de utilidades têm desempenho econômico inicial semelhante. A alternativa 1 usa materiais e processos mais intensivos em recursos e energia, mas atende ao requisito funcional. A alternativa 2 reduz consumo de recursos, adota processos e fontes energéticas de menor impacto e apresenta menor exposição futura a emissões e a preços de carbono. Qual alternativa deve ser escolhida e por quê?

**R:** A alternativa 2. Com desempenho econômico inicial semelhante, a decisão deve usar abordagem de ciclo de vida, não apenas impacto imediato. Nessa lógica, a comparação inclui minimização de recursos consumidos e seleção de materiais, processos e fontes energéticas de menor impacto ao longo das fases do empreendimento. Além disso, a decisão deve considerar o risco de carbono, que abrange a exposição futura a emissões, preços de carbono e efeitos associados às mudanças climáticas e à transição energética. Portanto, a alternativa 2 é a mais consistente porque combina menor carga ambiental no ciclo de vida com menor exposição econômica e estratégica ao risco de carbono.

- **gpt-5-4-petrobras:medium:** aprova
- **gpt-5-2-petrobras:medium:** reprova (suporte, sem_generalizacao) · Suporte insuficiente para linguagem de obrigação (‘deve’) como regra geral; F6/F7 apresentam diretrizes/metodologia, não uma obrigatoriedade universal.; Termo ‘estratégica’ na conclusão não está explicitamente suportado por F6/F7 (F6 fala em conduzir de forma econômica e gerenciar risco do negócio, mas não caracteriza ‘exposição estratégica’).; A resposta poderia precisar que se trata de usar critérios de ciclo de vida (LCD) e risco de carbono como base de comparação, em vez de afirmar como obrigação geral.
- **gpt-5-4-petrobras:low:** aprova

### b8c888d001-b0-A1 · facil · Saúde Ocupacional

**P:** Qual é a função de um programa de vigilância médica ocupacional em uma instalação offshore além do acompanhamento clínico individual?

**R:** É transformar sinais de agravo à saúde em gestão ativa do risco: receber notificações, consolidar informações de saúde, investigar casos, definir medidas de controle e acompanhar sua eficácia. Em cenário infeccioso, isso inclui usar dados como POB, casos suspeitos e contactantes para orientar isolamento, restrição de circulação, manejo de casos e retorno ao trabalho. O programa também apoia decisões de continuidade operacional quando a doença pode afastar profissionais-chave necessários para operar e responder a emergências com segurança.

- **gpt-5-4-petrobras:medium:** reprova (suporte) · Há falta de suporte para a expressão 'responder a emergências com segurança'.
- **gpt-5-2-petrobras:medium:** aprova
- **gpt-5-4-petrobras:low:** aprova

### b8c888d001-b1-A1 · dificil_A · Saúde Ocupacional

**P:** Em uma unidade offshore, um trabalhador foi afastado após apresentar sintomas compatíveis com doença infecciosa durante o turno e ter circulado por áreas comuns antes da avaliação. Ao mesmo tempo, a supervisão informa que há outros afastamentos recentes ligados a trabalho em área com condição operacional insegura e ambiente fora do padrão. Qual deve ser a prioridade imediata de gestão para esse caso específico e por quê?

**R:** A prioridade imediata deve recair no controle do caso infeccioso. Como há suspeita de doença infecciosa com circulação prévia pela instalação, o manejo precisa acionar o encadeamento de monitoramento de saúde, isolamento, impedimento de circulação, comunicação clara ao pessoal, sanitização, manejo do caso e retorno ao trabalho. Os afastamentos por condição operacional insegura e por ambiente em desconformidade exigem correção do contexto operacional, mas isso responde a outra natureza de problema. Quando o afastamento decorre de suspeita infecciosa, tratar o caso como mera questão de condição operacional reduz a efetividade da resposta, porque deixa de atacar os mecanismos centrais de contenção do risco de transmissão a bordo.

- **gpt-5-4-petrobras:medium:** aprova
- **gpt-5-2-petrobras:medium:** reprova (sem_generalizacao) · Generalização/linguagem normativa sem ressalva do contexto de origem (BSEE/EUA) do encadeamento do F1; convém enquadrar como boa prática aplicável ao cenário de doença infecciosa, não como exigência universal.
- **gpt-5-4-petrobras:low:** aprova

### b8c888d001-b2-A1 · dificil_B · Saúde Ocupacional

**P:** Após uma refeição, vários trabalhadores de setores diferentes apresentam sintomas gastrointestinais em poucas horas. No mesmo período, houve abastecimento recente de água por bunkering e também ocorreu falha de refrigeração na área de alimentos. Qual trilha de investigação e contenção deve ser priorizada nas primeiras decisões, considerando a necessidade de manter operação segura?

**R:** A prioridade é tratar o evento como possível exposição coletiva por fonte comum e abrir, em paralelo, duas frentes: água potável e alimentos. Na água, verificar imediatamente se houve perda de potabilidade ou contaminação introduzida no abastecimento, incluindo condição sanitária das mangueiras e conexões e eventual desvio de identificação de pontos potáveis. Nos alimentos, verificar se a falha de refrigeração comprometeu a conservação e se houve falha de higiene na manipulação. Como a resposta muda conforme a fonte, devem ser acionados os planos específicos para suspeita de contaminação ou interrupção da água potável e para falha de refrigeração/surto alimentar. Ao mesmo tempo, conter novos expostos e avaliar se o número de afetados ou o impacto no efetivo já compromete a operação normal, para adaptar a operação e escalar a resposta sanitária.

- **gpt-5-4-petrobras:medium:** aprova
- **gpt-5-2-petrobras:medium:** reprova (suporte) · Falta de suporte: ‘adaptar a operação’/‘escalar a resposta sanitária’ não está sustentado pelos fatos citados; o gatilho de F13 cobre comunicação regulatória por normalidade/10%, mas não explicita a decisão de adaptação operacional (isso aparece nas notas via outros fatos, p.ex. ANP 816/2020 e lógica de POB/EOR, que não foram citados aqui).; Falta de suporte parcial: ‘conter novos expostos’ é genérico; F12 sustenta exemplos (isolamento/rastreamento/evacuação), mas a resposta não explicita essas ações, ficando com suporte indireto/fraco.
- **gpt-5-4-petrobras:low:** aprova

### c3419532e4-b0-A2 · media · Segurança Ocupacional

**P:** Em um trabalho a quente executado em altura com solda elétrica, há possibilidade de flash fire e exposição intensa ao arco. Como relacionar cada EPI citado ao mecanismo de dano que ele deve mitigar?

**R:** A roupa resistente ao fogo deve ser associada ao risco térmico e ao possível flash fire, reduzindo a severidade da exposição ao calor. O capacete de soldagem com tonalidade adequada deve ser associado à luminosidade excessiva da solda elétrica, atenuando a agressão ocular causada pelo arco. A proteção contra quedas deve ser associada ao risco adicional do trabalho em desnível, para mitigar as consequências de perda de equilíbrio ou queda durante a atividade.

- **gpt-5-4-petrobras:medium:** reprova (autonomia) · A pergunta não é plenamente autônoma porque se refere a 'cada EPI citado' sem listar os EPIs no próprio enunciado.
- **gpt-5-2-petrobras:medium:** aprova
- **gpt-5-4-petrobras:low:** aprova

## Defeitos plantados que passaram

- **gpt-5-4-petrobras:medium** aprovou `1c3beb869e-b0-A2::caso_na_resposta` (caso_na_resposta): A pergunta foi mantida, mas a resposta passou a se apoiar em um caso/arranjo específico — a sequência SAO → tanques com tratamento químico → flotação — como se esse exemplo particular valesse como regra geral.
- **gpt-5-4-petrobras:medium** aprovou `1c3beb869e-b0-A2::dependencia_fonte` (dependencia_fonte): A pergunta foi reescrita para depender discretamente do conhecimento de um arranjo específico de processo (SAO, tanques com tratamento químico e injeção de flotadores antes da flotação), de modo que só quem conhece essa descrição/fonte consegue respondê-la plenamente.
- **gpt-5-4-petrobras:medium** aprovou `1c3fa83845-b0-A1::caso_na_resposta` (caso_na_resposta): A resposta passou a se apoiar em um caso/estudo específico ('como ocorreu no estudo de Hines et al. (2008a)') como se esse exemplo particular bastasse para fundamentar a regra geral.
- **gpt-5-4-petrobras:medium** aprovou `202d9e591b-b0-A1::caso_na_resposta` (caso_na_resposta): A pergunta foi mantida, mas a resposta passou a se apoiar em um caso específico ('como no caso da mistura hidrogênio-ar') como se exemplificasse a regra geral, introduzindo dependência indevida de um caso particular.
- **gpt-5-4-petrobras:medium** aprovou `460979b6f3-b0-A1::caso_na_resposta` (caso_na_resposta): A resposta passou a apoiar a explicação geral em um caso/fonte específica ao citar 'a aplicação típica dos documentos API RP 580 e API STD 581' como se isso fundamentasse a regra geral.
- **gpt-5-4-petrobras:medium** aprovou `26d45ade58-b1-A1::caso_na_resposta` (caso_na_resposta): A resposta passou a se apoiar em um caso/contexto específico — campanhas de offloading no Golfo do México — como se essa referência particular servisse de regra geral para justificar a decisão.
- **gpt-5-4-petrobras:medium** aprovou `26d45ade58-b1-A1::erro_tecnico` (erro_tecnico): Na resposta, foi introduzida uma afirmação tecnicamente errada ao sugerir que permanecer abaixo do limite estático do equipamento ainda é um referencial aceitável na decisão; o correto é que a referência aplicável é o limite dinâmico, não o estático.
- **gpt-5-4-petrobras:medium** aprovou `4e96c8ab4a-b0-A1::caso_na_resposta` (caso_na_resposta): A pergunta foi mantida, mas a resposta passou a se apoiar em um caso específico da P-53 e em tags de instrumentos concretos, como se esse exemplo particular valesse como formulação geral da regra.
- **gpt-5-4-petrobras:medium** aprovou `4e96c8ab4a-b0-A2::caso_na_resposta` (caso_na_resposta): A resposta passou a apoiar a explicação geral em um caso específico da P-53, citando LIC-1223002/008 e LV-1223002A1/A2/B1/B2 como se essa implementação particular servisse de base geral para a resposta.
- **gpt-5-4-petrobras:medium** aprovou `567fdce5c3-b2-A1::caso_na_resposta` (caso_na_resposta): A resposta passou a apoiar a regra geral em um caso específico, usando o desvio dos drenos para o tanque 4C via linha de COW como se fosse formulação geral do princípio.
- **gpt-5-4-petrobras:medium** aprovou `62e43c1988-b1-A1::caso_na_resposta` (caso_na_resposta): A resposta passou a se apoiar em um caso/procedimento específico — o adotado para as estacas torpedo da CENPES PETROBRAS — como se isso fosse a formulação geral da regra.
- **gpt-5-4-petrobras:medium** aprovou `62e43c1988-b0-A2::caso_na_resposta` (caso_na_resposta): A resposta passou a apoiar a explicação em um caso específico — a tempestade de inverno reportada pela HSE — e usa esse exemplo como se tivesse validade geral.
- **gpt-5-4-petrobras:medium** aprovou `9a7659b69d-b0-A1::erro_tecnico` (erro_tecnico): Na resposta, foi alterado um elo do sistema logístico: 'terminais portuários' foi trocado por 'unidades marítimas' na enumeração do fluxo integrado, tornando a formulação tecnicamente incorreta em relação à definição dada.
- **gpt-5-4-petrobras:medium** aprovou `7408dc2a56-b0-A2::caso_na_resposta` (caso_na_resposta): Foi mantida a pergunta e a resposta passou a se apoiar indevidamente em um caso específico — 'como ocorreu no FPSO CDSM' — como se esse exemplo particular valesse como regra geral.
- **gpt-5-4-petrobras:medium** aprovou `b5d9016da7-b1-A1::caso_na_resposta` (caso_na_resposta): A resposta passou a apoiar a conclusão em um caso específico ('como ocorreu na P-53') como se esse exemplo particular servisse como regra geral para o diagnóstico.
- **gpt-5-4-petrobras:medium** aprovou `bfc6625c3d-b0-A1::caso_na_resposta` (caso_na_resposta): A resposta foi feita apoiar-se em um caso específico — o PRE214 e o uso do refeitório como refúgio temporário — como se esse exemplo particular servisse de regra geral.
- **gpt-5-4-petrobras:medium** aprovou `b8c888d001-b1-A1::caso_na_resposta` (caso_na_resposta): A resposta foi feita apoiar-se em um caso específico — as inspeções da BSEE durante a pandemia — como se esse exemplo particular funcionasse como regra geral para o julgamento do caso.
- **gpt-5-4-petrobras:medium** aprovou `d21b4ace38-b1-A1::erro_tecnico` (erro_tecnico): Na resposta, foi alterado o critério de aceitação da contingência: em vez de manter o risco em nível aceitável, passou a exigir que a contingência residual eliminasse o risco a nível aceitável.
- **gpt-5-4-petrobras:medium** aprovou `d720962e6f-b0-A1::caso_na_resposta` (caso_na_resposta): A resposta foi ancorada em um caso/referência específica — as recomendações das “Guidelines for Engineering Design for Process Safety” para separação entre salas de controle e áreas de grande perigo — como se isso servisse de base geral para a afirmação.
- **gpt-5-2-petrobras:medium** aprovou `1c3beb869e-b0-A2::caso_na_resposta` (caso_na_resposta): A pergunta foi mantida, mas a resposta passou a se apoiar em um caso/arranjo específico — a sequência SAO → tanques com tratamento químico → flotação — como se esse exemplo particular valesse como regra geral.
- **gpt-5-2-petrobras:medium** aprovou `1c3beb869e-b0-A2::dependencia_fonte` (dependencia_fonte): A pergunta foi reescrita para depender discretamente do conhecimento de um arranjo específico de processo (SAO, tanques com tratamento químico e injeção de flotadores antes da flotação), de modo que só quem conhece essa descrição/fonte consegue respondê-la plenamente.
- **gpt-5-2-petrobras:medium** aprovou `1c3fa83845-b0-A1::caso_na_resposta` (caso_na_resposta): A resposta passou a se apoiar em um caso/estudo específico ('como ocorreu no estudo de Hines et al. (2008a)') como se esse exemplo particular bastasse para fundamentar a regra geral.
- **gpt-5-2-petrobras:medium** aprovou `202d9e591b-b0-A1::caso_na_resposta` (caso_na_resposta): A pergunta foi mantida, mas a resposta passou a se apoiar em um caso específico ('como no caso da mistura hidrogênio-ar') como se exemplificasse a regra geral, introduzindo dependência indevida de um caso particular.
- **gpt-5-2-petrobras:medium** aprovou `460979b6f3-b0-A1::caso_na_resposta` (caso_na_resposta): A resposta passou a apoiar a explicação geral em um caso/fonte específica ao citar 'a aplicação típica dos documentos API RP 580 e API STD 581' como se isso fundamentasse a regra geral.
- **gpt-5-2-petrobras:medium** aprovou `26d45ade58-b1-A1::erro_tecnico` (erro_tecnico): Na resposta, foi introduzida uma afirmação tecnicamente errada ao sugerir que permanecer abaixo do limite estático do equipamento ainda é um referencial aceitável na decisão; o correto é que a referência aplicável é o limite dinâmico, não o estático.
- **gpt-5-2-petrobras:medium** aprovou `62e43c1988-b0-A2::caso_na_resposta` (caso_na_resposta): A resposta passou a apoiar a explicação em um caso específico — a tempestade de inverno reportada pela HSE — e usa esse exemplo como se tivesse validade geral.
- **gpt-5-2-petrobras:medium** aprovou `9a7659b69d-b0-A1::erro_tecnico` (erro_tecnico): Na resposta, foi alterado um elo do sistema logístico: 'terminais portuários' foi trocado por 'unidades marítimas' na enumeração do fluxo integrado, tornando a formulação tecnicamente incorreta em relação à definição dada.
- **gpt-5-2-petrobras:medium** aprovou `b8c888d001-b1-A1::caso_na_resposta` (caso_na_resposta): A resposta foi feita apoiar-se em um caso específico — as inspeções da BSEE durante a pandemia — como se esse exemplo particular funcionasse como regra geral para o julgamento do caso.
- **gpt-5-2-petrobras:medium** aprovou `d21b4ace38-b0-A1::dependencia_fonte` (dependencia_fonte): A pergunta foi reescrita para depender do conhecimento de uma fonte específica, ao exigir a sequência proposta por Moubray para o RCM.
- **gpt-5-4-petrobras:low** aprovou `1c3beb869e-b0-A2::caso_na_resposta` (caso_na_resposta): A pergunta foi mantida, mas a resposta passou a se apoiar em um caso/arranjo específico — a sequência SAO → tanques com tratamento químico → flotação — como se esse exemplo particular valesse como regra geral.
- **gpt-5-4-petrobras:low** aprovou `1c3fa83845-b0-A1::caso_na_resposta` (caso_na_resposta): A resposta passou a se apoiar em um caso/estudo específico ('como ocorreu no estudo de Hines et al. (2008a)') como se esse exemplo particular bastasse para fundamentar a regra geral.
- **gpt-5-4-petrobras:low** aprovou `202d9e591b-b0-A1::caso_na_resposta` (caso_na_resposta): A pergunta foi mantida, mas a resposta passou a se apoiar em um caso específico ('como no caso da mistura hidrogênio-ar') como se exemplificasse a regra geral, introduzindo dependência indevida de um caso particular.
- **gpt-5-4-petrobras:low** aprovou `460979b6f3-b0-A1::caso_na_resposta` (caso_na_resposta): A resposta passou a apoiar a explicação geral em um caso/fonte específica ao citar 'a aplicação típica dos documentos API RP 580 e API STD 581' como se isso fundamentasse a regra geral.
- **gpt-5-4-petrobras:low** aprovou `26d45ade58-b1-A1::erro_tecnico` (erro_tecnico): Na resposta, foi introduzida uma afirmação tecnicamente errada ao sugerir que permanecer abaixo do limite estático do equipamento ainda é um referencial aceitável na decisão; o correto é que a referência aplicável é o limite dinâmico, não o estático.
- **gpt-5-4-petrobras:low** aprovou `4e96c8ab4a-b0-A2::caso_na_resposta` (caso_na_resposta): A resposta passou a apoiar a explicação geral em um caso específico da P-53, citando LIC-1223002/008 e LV-1223002A1/A2/B1/B2 como se essa implementação particular servisse de base geral para a resposta.
- **gpt-5-4-petrobras:low** aprovou `567fdce5c3-b2-A1::caso_na_resposta` (caso_na_resposta): A resposta passou a apoiar a regra geral em um caso específico, usando o desvio dos drenos para o tanque 4C via linha de COW como se fosse formulação geral do princípio.
- **gpt-5-4-petrobras:low** aprovou `62e43c1988-b0-A2::caso_na_resposta` (caso_na_resposta): A resposta passou a apoiar a explicação em um caso específico — a tempestade de inverno reportada pela HSE — e usa esse exemplo como se tivesse validade geral.
- **gpt-5-4-petrobras:low** aprovou `62e43c1988-b1-A1::caso_na_resposta` (caso_na_resposta): A resposta passou a se apoiar em um caso/procedimento específico — o adotado para as estacas torpedo da CENPES PETROBRAS — como se isso fosse a formulação geral da regra.
- **gpt-5-4-petrobras:low** aprovou `9a7659b69d-b0-A1::erro_tecnico` (erro_tecnico): Na resposta, foi alterado um elo do sistema logístico: 'terminais portuários' foi trocado por 'unidades marítimas' na enumeração do fluxo integrado, tornando a formulação tecnicamente incorreta em relação à definição dada.
- **gpt-5-4-petrobras:low** aprovou `b8c888d001-b1-A1::caso_na_resposta` (caso_na_resposta): A resposta foi feita apoiar-se em um caso específico — as inspeções da BSEE durante a pandemia — como se esse exemplo particular funcionasse como regra geral para o julgamento do caso.
- **gpt-5-4-petrobras:low** aprovou `bfc6625c3d-b0-A1::caso_na_resposta` (caso_na_resposta): A resposta foi feita apoiar-se em um caso específico — o PRE214 e o uso do refeitório como refúgio temporário — como se esse exemplo particular servisse de regra geral.
- **gpt-5-4-petrobras:low** aprovou `d21b4ace38-b0-A1::dependencia_fonte` (dependencia_fonte): A pergunta foi reescrita para depender do conhecimento de uma fonte específica, ao exigir a sequência proposta por Moubray para o RCM.
- **gpt-5-4-petrobras:low** aprovou `d21b4ace38-b1-A1::erro_tecnico` (erro_tecnico): Na resposta, foi alterado o critério de aceitação da contingência: em vez de manter o risco em nível aceitável, passou a exigir que a contingência residual eliminasse o risco a nível aceitável.
- **gpt-5-4-petrobras:low** aprovou `d720962e6f-b0-A1::caso_na_resposta` (caso_na_resposta): A resposta foi ancorada em um caso/referência específica — as recomendações das “Guidelines for Engineering Design for Process Safety” para separação entre salas de controle e áreas de grande perigo — como se isso servisse de base geral para a afirmação.
