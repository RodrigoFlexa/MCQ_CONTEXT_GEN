# Comparação de juízes

160 questões originais e 96 versões com defeito plantado. Cada juiz avaliou cada item isoladamente, com o mesmo material. Tempo 45.4 min.

Um bom juiz aprova a maior parte das originais (nem todas estão corretas) e reprova as versões com defeito. "Motivo certo" é a fração das detecções em que reprovou pela verificação esperada.

| Juiz | aprova originais | detecta erro técnico | detecta sem suporte | detecta dependência de fonte | detecção média | erros | tokens entrada | tokens saída |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| gpt-5-2-petrobras:medium | 34% | 100% (100%) | 100% (100%) | 100% (97%) | 100% | 0 | 1,087,194 | 340,036 |
| o3-petrobras:medium | 92% | 97% (100%) | 100% (100%) | 34% (64%) | 77% | 0 | 1,093,875 | 339,346 |
| gpt-5-4-petrobras:medium | 66% | 100% (100%) | 100% (100%) | 100% (100%) | 100% | 0 | 1,087,194 | 557,566 |
| gpt-5-petrobras:medium | 88% | 100% (100%) | 100% (100%) | 53% (88%) | 84% | 0 | 1,087,194 | 770,710 |

| Par de juízes | concordância nas originais | kappa |
|---|---:|---:|
| gpt-5-2-petrobras:medium x o3-petrobras:medium | 40% | 0.06 |
| gpt-5-2-petrobras:medium x gpt-5-4-petrobras:medium | 57% | 0.217 |
| gpt-5-2-petrobras:medium x gpt-5-petrobras:medium | 43% | 0.088 |
| o3-petrobras:medium x gpt-5-4-petrobras:medium | 66% | 0.064 |
| o3-petrobras:medium x gpt-5-petrobras:medium | 87% | 0.254 |
| gpt-5-4-petrobras:medium x gpt-5-petrobras:medium | 72% | 0.278 |

## Originais com divergência entre juízes

_Para o especialista decidir: quem está certo em cada caso._

### 01c1c3db6e-b0-A1 · facil · Operação de Offloading

**P:** Na operação de offloading, que quadro de consequências operacionais caracteriza a degradação de propulsão, geração elétrica ou controle automático do navio aliviador?

**R:** Essas degradações são tratadas como precursoras de perda de manobrabilidade e aumento do risco operacional. A perda de propulsão do aliviador tende a causar atraso operacional e pode evoluir para colisão se o problema persistir. A parada do sistema diesel-gerador também foi associada a atraso operacional e à possibilidade de colisão caso a operação prossiga. Já falhas de controle automático, como erro de programação, podem produzir manobras arriscadas durante o offloading, mesmo sem uma quebra mecânica completa.

- **gpt-5-2-petrobras:medium:** reprova (suporte) · Falta de suporte literal/estrito para 'perda de manobrabilidade' e 'aumento do risco operacional' como síntese geral; os fatos citados falam em atraso operacional, possibilidade de colisão e manobras arriscadas, mas não explicitam essa formulação.; A resposta poderia ficar totalmente suportada se restringisse a caracterização às consequências explicitadas: atraso operacional médio e possibilidade de colisão (F3, F4) e manobras arriscadas por erro de programação/julgamento (F1).
- **o3-petrobras:medium:** aprova
- **gpt-5-4-petrobras:medium:** reprova (correcao_tecnica, suporte, escopo, sem_generalizacao) · Omissão da falha do DP/perda de posição prevista no alvo A1.; Abertura excessiva do escopo para 'controle automático' sem tratar explicitamente o DP.; Afirmação-síntese inicial sem suporte direto nos fatos citados.
- **gpt-5-petrobras:medium:** aprova

### 01c1c3db6e-b1-A1 · dificil_A · Operação de Offloading

**P:** Durante um offloading, o aliviador sai do envelope seguro em três ocorrências distintas. Na primeira, a excursão vem junto com perda de alimentação para vários sistemas, inclusive bombas de óleo lubrificante do motor principal, seguida de parada do motor principal, navegação e manobra. Na segunda, os sistemas de navegação e controle permanecem energizados, mas há perda de propulsão e o navio passa a responder com atraso. Na terceira, energia e propulsão seguem disponíveis, porém após ajuste no automático ou avaliação inadequada da manobrabilidade o navio corrige na direção errada ou de forma incompatível com a condição. Qual é o diagnóstico mais compatível para cada ocorrência?

**R:** Primeira ocorrência: o diagnóstico mais compatível é blackout em cascata iniciado por falha do motor de combustão auxiliar, porque a assinatura observável é a perda elétrica ampla, atingindo bombas de óleo lubrificante, motor principal, navegação e manobra. Segunda ocorrência: o quadro é mais compatível com perda isolada de propulsão; ela tende a aparecer primeiro como atraso operacional, elevando o risco de colisão se persistir. Terceira ocorrência: o diagnóstico mais provável é erro de programação do sistema automático ou erro de julgamento das condições de manobrabilidade, pois o navio continua energizado e com capacidade propulsiva, mas responde de forma inadequada. Em offloading, distinguir essas assinaturas importa porque o mesmo desvio de posição pode evoluir para cenários de colisão por mecanismos diferentes, mesmo quando o sintoma inicial é apenas a saída do envelope seguro.

- **gpt-5-2-petrobras:medium:** reprova (suporte) · Falta de suporte: a conclusão final menciona 'saída do envelope seguro' e a relevância operacional dessa distinção sem citar fatos que suportem explicitamente o conceito de posição/envelope seguro no offloading (ex.: F2/F7/F1).; Ajuste simples: remover a frase sobre 'envelope seguro' ou adicionar suporte factual pertinente (F2/F7/F1) mantendo o restante inalterado.
- **o3-petrobras:medium:** aprova
- **gpt-5-4-petrobras:medium:** aprova
- **gpt-5-petrobras:medium:** aprova

### 567fdce5c3-b0-A1 · facil · Operação de tanques de carga, lastro, sistema gás inerte, ventilação e estabilidade

**P:** Em um FPSO monohull, para que o sistema de lastro é usado durante o carregamento e a descarga de óleo cru em relação ao calado?

**R:** Ele é usado para compensar a variação de calado à medida que o óleo cru é carregado ou descarregado, mantendo a condição operacional da unidade sob controle.

- **gpt-5-2-petrobras:medium:** reprova (suporte) · Falta de suporte: a frase 'mantendo a condição operacional da unidade sob controle' não está sustentada por F2. Remover ou reescrever para ficar estritamente em 'compensar o aumento/redução do calado' com base em F2.
- **o3-petrobras:medium:** aprova
- **gpt-5-4-petrobras:medium:** reprova (suporte) · Resposta contém acréscimo sem suporte factual: 'mantendo a condição operacional da unidade sob controle'.
- **gpt-5-petrobras:medium:** reprova (suporte) · Suporte insuficiente: a frase "mantendo a condição operacional da unidade sob controle" não tem respaldo explícito nos fatos fornecidos.

### 567fdce5c3-b1-A1 · dificil_A · Operação de tanques de carga, lastro, sistema gás inerte, ventilação e estabilidade

**P:** Durante uma operação de descarga para navio aliviador, a equipe identifica uma anormalidade no sistema de offloading com potencial de vazamento, enquanto a transferência ainda está em andamento. Parte do time propõe primeiro diagnosticar a origem antes de atuar; outra parte defende uma ação imediata para preservar a contenção. Qual deve ser a resposta operacional inicial e como ela se conecta à filosofia de barreiras e shut-offs aplicável ao offloading?

**R:** A resposta inicial deve ser interromper imediatamente a transferência, antes de qualquer outra providência, porque a prioridade é evitar a continuidade de uma condição com risco de avaria, poluição ou perda de contenção. Essa decisão preserva a barreira de contenção ao reduzir ou cessar o inventário que ainda pode alimentar um vazamento. No offloading, a filosofia de barreiras não depende só da integridade física da linha: ela também inclui funções de isolamento e parada para cenários como ruptura de mangueira, ruptura de tubulação ou desconexão por saída de posição do navio aliviador. Nesses cenários, os shut-offs podem envolver isolamento manual, válvulas de fechamento remoto, parada das bombas de carga e breakaway couplings. A lógica é não manter o sistema transferindo hidrocarbonetos enquanto existe anormalidade com potencial de perda de contenção; primeiro interrompe-se a transferência, depois se diagnostica a causa e se confirma a condição das barreiras.

- **gpt-5-2-petrobras:medium:** reprova (suporte) · Falta de suporte explícito para a justificativa mecanística 'reduzir inventário que alimenta vazamento' (não está nos fatos citados).; A menção explícita a 'perda de contenção' como critério em F11 não aparece literalmente; F11 fala em riscos/perigos/avarias/poluição. A resposta pode ser reescrita para ligar a interrupção imediata diretamente a esses termos e ao objetivo de 'minimizar perda de hidrocarbonetos' (F4) sem acrescentar mecanismo não citado.
- **o3-petrobras:medium:** aprova
- **gpt-5-4-petrobras:medium:** reprova (suporte) · Falta de suporte explícito para a afirmação final sobre diagnosticar a causa e confirmar a condição das barreiras após a interrupção.; A resposta poderia ficar integralmente suportada se parasse na interrupção imediata e na conexão com os shut-offs/barreiras de contenção previstos para offloading.
- **gpt-5-petrobras:medium:** aprova

### 567fdce5c3-b2-A1 · dificil_B · Operação de tanques de carga, lastro, sistema gás inerte, ventilação e estabilidade

**P:** Com o slop de bombordo indisponível, a equipe reconfigurou temporariamente drenos e transferências. Após a manobra, os níveis remotos dos tanques indicam condição aceitável no programa de estabilidade, mas o trim observado e a resposta de alguns tanques não coincidem com o previsto. Antes de iniciar nova transferência de carga e um ajuste de lastro, qual deve ser a decisão técnica prioritária e por quê?

**R:** A prioridade é interromper a aprovação da próxima manobra com base apenas no software e confirmar independentemente o inventário real dos tanques antes de qualquer nova transferência ou ajuste de lastro. Em line-up contingente, o caminho hidráulico aberto pode não ser o presumido: com slop indisponível, drenos podem ser redirecionados para outro slop ou para o 4C, e certos headers podem até drenar carga para o slop de bombordo se usados inadequadamente. Como o programa recebe dados automáticos dos tanques, mas sua confiabilidade depende de verificação manual regular e de entradas operacionais corretas, uma condição aparentemente aceitável pode estar mascarando migração real de conteúdo. Só depois de reconciliar medições e atualizar a condição no programa é que a nova sequência deve ser simulada e liberada, porque desviar do plano sem reavaliação pode gerar esforços estruturais excessivos.

- **gpt-5-2-petrobras:medium:** reprova (suporte) · Falta suporte explícito, com os F# citados, para a afirmação de que a condição do software pode estar 'mascarando migração real de conteúdo' (é uma inferência forte).; A alegação geral de que o 'caminho hidráulico aberto pode não ser o presumido' não está amarrada a um fato operacional específico dentre os F# citados; para sustentar, precisaria citar fatos do desvio de drenos via mangote/COW (ex.: F6/F4) ou reescrever de forma mais aderente aos F1/F2/F5.; A resposta menciona risco de inventário errado por line-up contingente, mas não evidencia (com fatos citados) um mecanismo concreto de transferência indesejada além do caso do header (F5) e redirecionamento de drenos (F1/F2).
- **o3-petrobras:medium:** aprova
- **gpt-5-4-petrobras:medium:** aprova
- **gpt-5-petrobras:medium:** aprova

### 62e43c1988-b0-A1 · facil · Sistema de ancoragem, manutenção e monitoramento da posição

**P:** Em uma unidade ancorada, o que a perda de uma única linha de ancoragem exige em termos de continuidade operacional, e de quais fatores depende uma eventual retomada?

**R:** A perda de uma linha de ancoragem deve ser tratada como condição para cessação imediata das operações. A retomada não é automática nem pode ser justificada apenas pela existência de outras linhas remanescentes. Ela deve ser reavaliada conforme a linha que falhou, as condições meteorológicas presentes e previstas e a verificação de conformidade com os parâmetros de projeto da unidade e do sistema de ancoragem.

- **gpt-5-2-petrobras:medium:** reprova (sem_generalizacao) · Generalização: a pergunta enuncia como regra geral ('exige') um critério que, nas notas, é apresentado como procedimento/declaração em casos específicos. Sugestão de reparo sem novo conteúdo: ajustar o enunciado para contextualizar como 'em procedimentos de contingência descritos nos casos/na nota' ou 'como critério operacional adotado', evitando universalizar.
- **o3-petrobras:medium:** aprova
- **gpt-5-4-petrobras:medium:** aprova
- **gpt-5-petrobras:medium:** aprova

### 62e43c1988-b0-A2 · media · Sistema de ancoragem, manutenção e monitoramento da posição

**P:** Durante a aproximação de uma tempestade, a unidade dispõe de recurso para ajustar as tensões de amarração, mas esse ajuste não é utilizado. Ao mesmo tempo, os limites máximos operacionais dos guinchos não estão prontamente disponíveis na sala de controle. Como essa combinação pode contribuir para exceder tensões operacionais?

**R:** Ela aumenta o risco por dois mecanismos complementares. Primeiro, deixar de ajustar preventivamente as tensões impede adaptar o sistema à condição ambiental severa, embora esse ajuste exista exatamente para esse tipo de situação. Segundo, sem os limites máximos operacionais prontamente disponíveis na sala de controle, a referência necessária para decidir e controlar o retensionamento fica retardada. Com a tempestade elevando rapidamente as solicitações nas linhas, a combinação de não preparar a distribuição de cargas e não dispor do limite operacional de forma imediata favorece decisões tardias ou mal controladas, tornando mais provável que tensões operacionais sejam excedidas.

- **gpt-5-2-petrobras:medium:** reprova (suporte) · Suporte insuficiente: a resposta inclui mecanismos não explicitados nos F1/F3/F5 (distribuição de cargas, dinâmica da tempestade, controle de retensionamento), indo além do que foi fornecido como fatos citados.; Para ficar 100% suportada, a resposta deveria se limitar ao que F3/F5 estabelecem (ajuste por procedimento em mau tempo; caso sem ajuste + suspeita de excedência; limites não disponíveis no CCR retardando referência), conectando-os sem detalhamento mecanístico não citado.
- **o3-petrobras:medium:** reprova (suporte) · Citação inadequada do F1: o fato referenciado diz exatamente o oposto do que a resposta afirma sobre a disponibilidade dos limites na CCR. Remover o F1 da lista de fatos (ou ajustar a frase para refletir seu conteúdo) resolveria.
- **gpt-5-4-petrobras:medium:** aprova
- **gpt-5-petrobras:medium:** aprova

### 62e43c1988-b2-A1 · dificil_B · Sistema de ancoragem, manutenção e monitoramento da posição

**P:** Um FPSO ancorado permanece dentro do limite operacional de offset. Ainda assim, nas últimas horas, aumentaram a assimetria das excursões, a variação de aproamento, os movimentos do topo e os sinais de inclinação/deformação em trechos de topo de alguns risers, sob estado de mar com swell e vento. A equipe discute manter a operação porque o critério geométrico principal não foi violado. Qual decisão técnica é mais consistente e por quê?

**R:** A condição não deve ser tratada como automaticamente aceitável só porque o offset global permanece dentro do limite. O monitoramento deve sair da lógica de limite único de posição e integrar tendências de station keeping com resposta estrutural dos risers e ambiente em tempo real. Isso porque a permanência dentro do offset seguro não garante menores esforços nos pontos críticos do riser, e valores fora de faixas-limite de inclinação, deformação ou esforços inferidos podem indicar ameaça à integridade mesmo sem excedência de offset. Além disso, movimentos do topo contribuem para fadiga e podem introduzir compressão dinâmica localizada, com risco de flambagem e aumento de curvatura/flexão. A decisão correta é elevar a condição para avaliação integrada, verificar alarmes e tendências, reavaliar carregamentos/ciclos esperados para o estado de mar vigente e adotar mitigação operacional proativa, em vez de usar o offset isolado como critério de continuidade.

- **gpt-5-2-petrobras:medium:** reprova (suporte) · Suporte insuficiente para a formulação específica ‘movimentos do topo ... podem introduzir compressão dinâmica localizada’: F14 suporta ‘esforços dinâmicos oscilatórios’ causando compressão momentânea, mas não atribui explicitamente essa compressão ao movimento de topo. Reescrever para ‘esforços dinâmicos oscilatórios associados ao ambiente/movimento’ ou citar/ancorar melhor a cadeia causal com o material disponível (mantendo-se estritamente nos fatos).
- **o3-petrobras:medium:** reprova (suporte) · Suporte incompleto: a menção à flambagem carece de citação ao fato correspondente (F11/F13). Falta de suporte reprova a questão.
- **gpt-5-4-petrobras:medium:** aprova
- **gpt-5-petrobras:medium:** aprova

### e9ca515f84-b1-A1 · dificil_A · Operações submarinas, poços, manifolds, PLEM e PLET

**P:** Uma linha submarina apresentou dúvida sobre sua condição externa após alteração operacional. A equipe consegue acessar apenas a parte aparente do trecho e a visibilidade da água está variável por maré e particulados. Em paralelo, existe a possibilidade de a atividade evoluir para atuação física na linha, incluindo modificação, correção ou reparo. Como classificar tecnicamente o escopo para definir se o recurso compatível é mergulho ou VOR/ROV?

**R:** Se a atividade terminar na verificação do estado externo do equipamento, limitada à parte aparente e acessível, o escopo é de inspeção ou vistoria e pode ser compatível com mergulho. Nessa condição, porém, o alcance real da inspeção depende da visibilidade da água, que pode reduzir a qualidade, a viabilidade e a cobertura da avaliação; mesmo com baixa visibilidade, a inspeção por tato continua restrita ao que está acessível. Se a demanda incluir atuar sobre a linha — como intervenção, expansão, modificação ou reparo — o escopo deixa de ser apenas inspeção e passa a se enquadrar nas operações associadas a VOR/ROV. Portanto, a distinção técnica deve partir do objetivo final da tarefa: observar a condição visível da parte acessível caracteriza vistoria; executar ação física sobre a linha caracteriza intervenção e direciona para VOR/ROV.

- **gpt-5-2-petrobras:medium:** reprova (suporte) · Falta de suporte para a afirmação de inspeção por tato em baixa visibilidade (não consta em F1–F2).; Falta de suporte para incluir “modificação/correção” como parte do conjunto explicitamente caracterizado em F1 (F1 cita intervenção, expansão e reparos, mas não ‘modificação/correção’).; Efeito descrito como ‘reduzir qualidade, viabilidade e cobertura’ extrapola a literalidade de F2; seria melhor limitar a ‘condicionada às condições visuais’ e ‘restrita à porção aparente’ conforme F2.
- **o3-petrobras:medium:** aprova
- **gpt-5-4-petrobras:medium:** aprova
- **gpt-5-petrobras:medium:** aprova

### e9ca515f84-b2-A1 · dificil_B · Operações submarinas, poços, manifolds, PLEM e PLET

**P:** Anos após o comissionamento, a linha entre um manifold e o FPSO passa a exigir maior diferencial de pressão para a mesma vazão aparente, enquanto o sistema se aproxima da vida útil de projeto. Houve mudança recente de razão gás-líquido e water-cut, e parte do histórico de instalação está incompleto. Sem evidência direta de vazamento, qual deve ser a linha de decisão para distinguir possível dano de instalação, degradação em operação ou incerteza de avaliação, e definir a resposta de integridade?

**R:** Não é tecnicamente defensável concluir de imediato por envelhecimento nem por dano de instalação. Primeiro, o indício hidráulico deve ser compatibilizado com a condição atual do fluido, porque a queda de pressão varia de forma não linear com vazão líquida, razão gás-líquido e water-cut; sem isso, pode-se confundir mudança de composição com anomalia mecânica. Em paralelo, a anomalia deve ser tratada formalmente, com registro e investigação do desvio operacional. A confirmação exige inspeção dirigida da linha e do entorno, incluindo enterramento, vãos livres, revestimento, proteção catódica, corrosão externa e interferências. Para separar origem de instalação, é preciso recuperar o máximo de evidência documental: as built, rastreabilidade de materiais e qualificação de executantes, além de registros de lançamento, como tensão monitorada e controle de dano ao revestimento. Se a evidência continuar insuficiente, a resposta correta é priorizar a anomalia e reduzir a incerteza com inspeções adicionais, reavaliação dos meios de detecção e, na proximidade/extensão de vida, modelagem avançada e dados conservadores antes de sustentar continuidade operacional.

- **gpt-5-2-petrobras:medium:** reprova (suporte, jurisdicao) · Suporte/formulação: ‘registro e investigação do desvio operacional’ precisa ser ancorado explicitamente em desvio dos limites do Envelope de Segurança (F1), senão extrapola o fato.; Suporte: item ‘interferências’ na lista de inspeção não está inequivocamente coberto pela citação de F9 apresentada; convém limitar-se aos itens explicitamente cobertos ou ajustar a referência.; Jurisdição: F13 (HSE/UK) deve ser explicitado como boa prática/referência de gestão, não como obrigação ANP/BR, para não induzir obrigação regulatória estrangeira.
- **o3-petrobras:medium:** aprova
- **gpt-5-4-petrobras:medium:** reprova (suporte) · Suporte parcial: 'registro e investigação do desvio operacional' extrapola F1, que trata especificamente de desvios do Envelope de Segurança.; Suporte parcial: 'na proximidade/extensão de vida' amplia F15 além da condição explícita de falta de dados/documentos na avaliação de extensão de vida.; Suporte parcial/contextual: 'reavaliação dos meios de detecção' em F12 é específica para vazamentos; a resposta a usa como passo geral de integridade para a anomalia descrita.
- **gpt-5-petrobras:medium:** aprova

### ee74ce2b7b-b0-A2 · media · Sistema e operação de pull in de risers

**P:** Em um procedimento de instalação com transferência do topo do riser do PLSV para um FPSO, quais pontos devem ser destacados para essa etapa e como eles delimitam o início da operação?

**R:** Os pontos destacados são o posicionamento do PLET e a máxima aproximação do PLSV ao FPSO. Essa máxima aproximação é definida como a aproximação máxima do topo do riser antes de começar a transferência para o FPSO. Portanto, o início do pull-in fica delimitado por essas condições do procedimento: o posicionamento do PLET deve estar conforme previsto e a transferência só deve começar quando a condição de máxima aproximação tiver sido atingida.

- **gpt-5-2-petrobras:medium:** reprova (correcao_tecnica, suporte) · Falta suporte/precisão ao tratar o posicionamento do PLET como condição que delimita diretamente o início da transferência; F2 só o aponta como questão importante do procedimento, enquanto o critério temporal de início está explicitado para a máxima aproximação.; A resposta adiciona normatividade (‘deve estar conforme previsto’) e causalidade (‘delimitado por essas condições’) sem amparo literal em F2 para o caso do PLET.
- **o3-petrobras:medium:** aprova
- **gpt-5-4-petrobras:medium:** aprova
- **gpt-5-petrobras:medium:** reprova (suporte) · Falta de suporte explícito para tratar o posicionamento do PLET como condição que delimita o início da transferência.; Uso de linguagem normativa ('deve') sem amparo direto no fato F2 para o ponto do PLET.

### ee74ce2b7b-b1-A1 · dificil_A · Sistema e operação de pull in de risers

**P:** Durante o planejamento do pull in de risers, a equipe compara duas arquiteturas de FPSO com turret. Na primeira, a unidade gira naturalmente em torno de um turret à vante. Na segunda, o turret fica mais ao meio do casco e a manutenção de aproamento e posição depende de thrusters comandados por Dynamic Positioning (DP). Qual é a diferença funcional mais relevante entre essas arquiteturas na forma de controlar a interface com os risers durante a operação?

**R:** Na arquitetura com turret à vante, a unidade se orienta passivamente por weathervaning ao redor do ponto de conexão. Assim, a rotação do casco em relação ao campo decorre predominantemente do alinhamento natural da embarcação, enquanto o turret mantém a conexão com risers e umbilicais mesmo com o giro do FPSO. Já na arquitetura com turret mais ao meio, heading e posição deixam de resultar principalmente desse alinhamento passivo e passam a ser mantidos ativamente. Nessa condição, o sistema DP usa informações de sensores e comanda direção e potência dos thrusters para corrigir posição e aproamento da unidade. Portanto, a diferença funcional central é que, em um caso, a interface com os risers convive com rotação passiva da unidade em torno do turret; no outro, essa interface é mantida com correções ativas e contínuas de heading e posição pelo conjunto DP-thrusters.

- **gpt-5-2-petrobras:medium:** aprova
- **o3-petrobras:medium:** aprova
- **gpt-5-4-petrobras:medium:** reprova (tipo_ok) · A forma não atende plenamente ao tipo difícil_A, pois falta exigir diagnóstico ou decisão no cenário; com o mesmo material, pode ser reformulada para pedir escolha ou diagnóstico operacional entre as arquiteturas.
- **gpt-5-petrobras:medium:** aprova

### ee74ce2b7b-b2-A1 · dificil_B · Sistema e operação de pull in de risers

**P:** Durante o pull-in de um riser em FPSO monocaio com turret e heading assistido por thrusters, ocorrem perdas de heading curtas, sempre recuperadas, enquanto vento e mar aumentam. O espaçamento geométrico entre amarrações e risers é bom em condição normal, mas já houve rotação anormal do conjunto. A operação deve ser tratada como oscilação aceitável ou como início de cenário crítico, e qual decisão operacional é mais adequada?

**R:** Deve ser tratada como degradação de margem, com potencial de evoluir para cenário crítico, não como oscilação automaticamente aceitável. Em FPSO com turret e thrusters, a perda de heading sob carregamento ambiental pode iniciar torção do turret e das amarrações; se o giro relativo esperado não ocorrer, a torção acumulada pode reduzir folgas até contato mooring–riser, mesmo quando o espaçamento geométrico é adequado em condição normal. Perdas de heading recuperadas indicam que a condição extrema ainda foi evitada, mas já sinalizam redução da capacidade de manter heading/posição com segurança. Assim, a decisão correta é suspender preventivamente o pull-in enquanto a unidade ainda estiver dentro dos limites, porque o mau tempo e a recorrência dos desvios reduzem a barreira de integridade e podem ainda aumentar a exposição em weather side working. Se houver saída dos limites operacionais, falha de amarração ou suspeita de contato/dano, a decisão passa a abortar e verificar a integridade antes de retomar.

- **gpt-5-2-petrobras:medium:** aprova
- **o3-petrobras:medium:** aprova
- **gpt-5-4-petrobras:medium:** reprova (suporte) · A resposta introduz critérios decisórios ('perdas recuperadas = margem reduzida' e 'suspender preventivamente por recorrência') sem suporte direto nos fatos citados.; A verificação de integridade antes do retorno é formulada de modo genérico, mas F14 só sustenta inspeção em água para sistemas específicos com bóia cônica latched/wire rope e sem medição normal de tensão.; Há suporte apenas parcial para algumas conclusões operacionais; pelo critério do julgamento, isso reprova em suporte.
- **gpt-5-petrobras:medium:** reprova (suporte) · Parte das afirmações decisórias (suspensão preventiva e abortamento) não está explicitamente apoiada em F#; a ligação com F13 (limites operacionais) não foi citada na resposta original.; A afirmação sobre perdas de heading recuperadas como indicador de redução de capacidade não tem F# de suporte.; O uso implícito de F14 (inspeção em água) só se aplica a sistemas desconectáveis com bóia cônica e wire rope, condição não especificada no cenário.

### 3b9ff23e32-b0-A1 · facil · Compressão de Gás

**P:** Qual é a função do compressor sobre o gás produzido e por que esse aumento de pressão e/ou densidade é necessário para encaminhá-lo às diferentes rotas de processo de uma planta offshore?

**R:** A função do compressor é transferir ao gás a energia recebida do acionador, como motor ou turbina, elevando seu estado de energia por aumento de pressão e/ou de densidade. Isso torna viável o escoamento do gás e o processamento subsequente. Em uma planta offshore, essa elevação de energia permite que o gás saia de uma condição de sucção e siga para as rotas de utilização e tratamento previstas no processo. Como a aplicação da máquina define a variável principal de controle, o serviço do compressor é ajustado para sustentar a necessidade operacional daquela rota; em compressores de gás úmido, isso é feito com foco na pressão de sucção.

- **gpt-5-2-petrobras:medium:** reprova (suporte) · Falta de suporte explícito para afirmações sobre 'viabilizar escoamento/processamento' e sobre 'ajuste do serviço para sustentar a rota' com os fatos citados.; Resposta não explicita os 'diferentes destinos/rotas' do gás na planta offshore (ex.: gás combustível, gas lift, exportação, reinjeção), que fazem parte do alvo A1 segundo a nota.
- **o3-petrobras:medium:** aprova
- **gpt-5-4-petrobras:medium:** reprova (suporte) · Falta suporte explícito, pelos F# citados, para a relação entre aumento de energia e 'rotas de utilização e tratamento'.; Falta suporte explícito, pelos F# citados, para a afirmação de que o serviço do compressor é ajustado para sustentar a necessidade operacional de cada rota.; A resposta não explicita os diferentes destinos do gás comprimido na planta offshore, como o alvo A1 solicita.
- **gpt-5-petrobras:medium:** aprova

### 3b9ff23e32-b0-A2 · media · Compressão de Gás

**P:** Em um trem de compressão offshore, a pressão de sucção precisa permanecer estável, mas a vazão recebida por cada estágio se afasta do valor compatível com a condição da máquina. Qual é a diferença funcional entre variar a rotação, estrangular a sucção e usar reciclo por estágio nesse controle?

**R:** Variação de rotação é a estratégia principal para sustentar a pressão de sucção sem grande oscilação, ajustando a capacidade global da máquina. O estrangulamento na sucção também pode ser usado para manter essa pressão, impondo uma restrição na entrada por meio de uma válvula posicionada a jusante do separador de entrada de baixa pressão. Já o reciclo por estágio não tem a função principal de estabilizar a pressão de sucção do trem; ele corrige a vazão efetiva vista por cada estágio. Para isso, a malha de vazão usa um setpoint que depende da rotação da máquina e manipula válvulas de reciclo para manter a vazão próxima desse valor. Assim, rotação e throttle atuam na pressão/capacidade, enquanto o reciclo corrige o desajuste de vazão em cada estágio.

- **gpt-5-2-petrobras:medium:** reprova (suporte) · Falta de suporte explícito para 'ajustando a capacidade global da máquina' (não consta em F3–F5).; Falta de suporte explícito para a hierarquização 'não tem a função principal de estabilizar a pressão de sucção' (F5 descreve função de controle de vazão, mas não compara 'função principal' vs. outras).; A última síntese mistura 'capacidade' com pressão; como 'capacidade' não está nos fatos citados, precisa ser reescrita apenas em termos suportados (pressão de sucção e vazão/setpoint/reciclo).
- **o3-petrobras:medium:** aprova
- **gpt-5-4-petrobras:medium:** aprova
- **gpt-5-petrobras:medium:** aprova

### 3b9ff23e32-b1-A1 · dificil_A · Compressão de Gás

**P:** Após uma alteração na lógica de controle do trem de compressão, a unidade passou a apresentar instabilidade. A pressão de sucção permanece no patamar habitual, mas a pressão de descarga alterna episódios de valor alto e baixo. Sem indício novo de mudança de regime do processo, qual deve ser a ação prioritária: focar a condição do sistema, a estratégia de controle ou a adequação do tipo de compressor à aplicação? Justifique pela variável afetada.

**R:** A prioridade deve ser a estratégia de controle, centrando o diagnóstico na pressão de descarga. Nesse trem, pressões alta e baixa na admissão e na descarga são tratadas como entradas formais de identificação, diagnóstico e procedimentos corretivos; portanto, a primeira decisão correta é usar a variável anormal e o lado afetado como critério primário de intervenção. Como a sucção permanece estável e a anomalia está localizada na descarga, o quadro deve ser lido primeiro como desvio associado à resposta do controle nessa variável, e não como perda genérica de desempenho. Também não é a melhor prioridade concluir, de imediato, por inadequação do tipo de compressor à aplicação, porque o padrão observado ainda está organizado pela variável de descarga dentro do sistema de controle.

- **gpt-5-2-petrobras:medium:** reprova (correcao_tecnica, suporte, sem_generalizacao) · Falta de suporte: o material (F1) não fornece critério para escolher entre condição do sistema, estratégia de controle ou adequação do tipo de compressor; a resposta escolhe 'estratégia de controle' por inferência não ancorada.; Generalização indevida: transforma 'pressões são entradas de diagnóstico' em 'priorize controle quando a descarga oscila'.; O alvo A1 exige uma decisão de priorização que não está fundamentável apenas com F1; seria necessário fato adicional explicitando o critério de priorização ou a relação entre alteração de lógica e instabilidade/pressão de descarga.
- **o3-petrobras:medium:** reprova (correcao_tecnica, suporte) · Falta de suporte factual para relacionar exclusivamente a anomalia de pressão de descarga com falha na lógica de controle; decisão poderia envolver condição de sistema. Resposta extrapola o material.
- **gpt-5-4-petrobras:medium:** reprova (correcao_tecnica, suporte) · A conclusão principal ('priorizar a estratégia de controle') não é sustentada por F1.; F1 permite localizar o desvio por variável/lado, mas não escolher entre condição do sistema, malha de controle ou adequação da máquina nesse cenário específico.; A resposta descarta, sem base factual suficiente, a hipótese de inadequação do tipo de compressor como prioridade inicial.
- **gpt-5-petrobras:medium:** aprova

### 62d82a5ef2-b0-A1 · facil · Medição Fiscal de óleo, medição fiscal de gás e transferência de custódia em operações de offloading

**P:** Qual é a função da notificação de falha do sistema de medição na passagem de uma anomalia técnica para a avaliação da confiabilidade dos dados de produção?

**R:** Ela formaliza a ocorrência de falha como evento tratável no sistema de gestão e de fiscalização da medição, ligando a detecção técnica à análise da confiabilidade dos dados informados. Isso é relevante porque a veracidade desses dados é objeto de fiscalização, e, quando a falha ou a não conformidade pode ter afetado os resultados, podem ser instaurados procedimentos de recálculo da produção. A notificação, portanto, não serve apenas para registrar um problema de instrumento; ela funciona como gatilho regulatório para verificar se os volumes declarados permanecem confiáveis.

- **gpt-5-2-petrobras:medium:** reprova (suporte) · Falta de suporte completo com os fatos citados: a resposta menciona ‘detecção técnica’/encadeamento detecção→análise, que exige pelo menos F3 (autodiagnóstico/anúncio de falhas) e, se mencionar controle/tratamento metrológico de não conformidade, também F4. Ajustar a lista de fatos citados (e/ou reescrever para ficar estritamente dentro de F1–F2) resolve com o mesmo material.
- **o3-petrobras:medium:** aprova
- **gpt-5-4-petrobras:medium:** aprova
- **gpt-5-petrobras:medium:** aprova

### 62d82a5ef2-b0-A2 · media · Medição Fiscal de óleo, medição fiscal de gás e transferência de custódia em operações de offloading

**P:** Após identificar possível inconsistência em volumes já informados, a equipe precisa reconhecer quais eventos podem abrir processo de recálculo da produção e qual deles tende a aparecer com mais frequência. Quais são esses gatilhos?

**R:** Os processos de recálculo podem ser abertos por notificação de falha do sistema de medição, inspeções, declarações das concessionárias, denúncias e validação da produção. Entre esses gatilhos, as notificações de falha do sistema de medição tendem a representar a maior parte dos casos. Na prática, isso torna a comunicação formal de falhas um canal recorrente de entrada para revisão da confiabilidade dos volumes já informados.

- **gpt-5-2-petrobras:medium:** aprova
- **o3-petrobras:medium:** aprova
- **gpt-5-4-petrobras:medium:** reprova (autonomia) · A pergunta perde autonomia ao cobrar uma frequência relativa ('qual deles tende a aparecer com mais frequência') que depende da observação reportada no material.; Pode ser corrigida com o mesmo material removendo a comparação de frequência ou enquadrando-a explicitamente como 'segundo o material' / 'nos casos observados'.
- **gpt-5-petrobras:medium:** aprova

### 62d82a5ef2-b1-A1 · dificil_A · Medição Fiscal de óleo, medição fiscal de gás e transferência de custódia em operações de offloading

**P:** Um FPSO vai revisar a medição de transferência de custódia no offloading. A equipe propõe duas alternativas: implantar monitoração online contínua de vazão, pressão estática e temperatura, ou manter instrumentação direta apenas de pressão estática na parede do duto e temperatura do escoamento, por restrição de CAPEX. Qual decisão técnica é mais consistente e como essa escolha afeta a estratégia de medição do volume compensado?

**R:** A decisão deve partir do equilíbrio entre rigor metrológico e viabilidade econômica. Se o investimento em transmissores e sistemas automáticos em tempo real se justificar, a monitoração online completa de vazão, pressão estática e temperatura amplia a capacidade de acompanhar o escoamento e pode sustentar o uso da medição online como valor representativo da transferência. Se esse investimento não se sustenta, limitar a instrumentação à pressão estática na parede do duto e à temperatura do escoamento continua tecnicamente consistente para o cálculo do volume compensado, porque essas duas variáveis compõem o conjunto mínimo exigido na estação de medição. Nessa condição, a estratégia de medição deixa de depender de uma representação online completa e passa a exigir maior atenção ao cálculo de compensação adotado. Em ambos os casos, a medição de custódia não se resume ao medidor de vazão, mas ao sistema integrado de medição.

- **gpt-5-2-petrobras:medium:** reprova (suporte) · Falta de suporte: a resposta afirma que monitoração online completa pode sustentar uso da medição online como valor representativo, mas isso não está em F1–F3 (dependeria de material sobre estabilidade operacional que não está nos fatos).; Falta de suporte: afirma que, com P/T apenas, a estratégia exige maior atenção ao algoritmo de compensação; essa criticidade do algoritmo não está explicitada em F1–F3.; Para ficar aderente aos fatos, a resposta deve restringir-se a: (i) custo/investimento da monitoração online completa (F3), (ii) mínimo obrigatório P estática na parede do duto e T do escoamento (F2), e (iii) entendimento de sistema integrado de medição (F1).
- **o3-petrobras:medium:** aprova
- **gpt-5-4-petrobras:medium:** reprova (correcao_tecnica, suporte) · Omissão do critério de estabilidade operacional demonstrada para admitir a medição online como valor representativo da transferência.; Suporte incompleto para a relação entre monitoração online completa e representatividade da medição ao longo do offloading.
- **gpt-5-petrobras:medium:** aprova

### 62d82a5ef2-b2-A1 · dificil_B · Medição Fiscal de óleo, medição fiscal de gás e transferência de custódia em operações de offloading

**P:** Em uma operação de offloading, a linha de medição fiscal de óleo passou a apresentar desvio recorrente de volume, sem alarme no medidor principal. Houve troca de trecho de tubulação próximo ao medidor, e a equipe dispõe de calibração anterior feita fora das condições usuais de campo. Qual diagnóstico deve ser priorizado para diferenciar causa de instalação de causa de calibração insuficientemente representativa, e por quê?

**R:** Deve-se verificar os dois eixos em sequência técnica, sem aceitar a calibração anterior como prova suficiente. Primeiro, confirmar se a instalação preserva as condições hidráulicas consideradas no dimensionamento e na calibração: trechos retos, diâmetro, espessura e rugosidade influenciam o perfil de escoamento e podem introduzir erro sistemático mesmo sem falha aparente do medidor principal. Depois, avaliar se a calibração representa as condições reais de operação, porque a confiabilidade metrológica exige ensaio em condições muito similares às de campo, com incerteza formalmente estimada e rastreabilidade. Se a calibração foi obtida fora de vazão, pressão, temperatura, viscosidade ou densidade representativas, o fator de calibração pode não sustentar o desempenho em serviço. O ponto central é que o resultado fiscal vem do sistema completo, incluindo instalação, instrumentos auxiliares, cálculo e base metrológica, não do medidor isolado.

- **gpt-5-2-petrobras:medium:** reprova (suporte) · Suporte parcial: a resposta afirma uma prioridade/ordem ('Primeiro... Depois...') como procedimento técnico sem haver fato que estabeleça essa sequência como critério.; Suporte parcial: a resposta trata 'rastreabilidade' como exigência normativa no contexto, mas cita apenas a definição (F22); para sustentar a exigência como requisito seria necessário apoiar em fatos como F24/ISO 10012, que não foram citados na resposta.; Completude: não explicita quais evidências/sintomas observar para distinguir hidráulica vs calibração (apesar de mencionar os eixos), o que reduz a força diagnóstica no nível difícil_B.
- **o3-petrobras:medium:** aprova
- **gpt-5-4-petrobras:medium:** reprova (suporte) · A ordem/priorização proposta na resposta ('primeiro instalação, depois calibração') não está sustentada pelos fatos fornecidos.; Falta de suporte torna a questão reprovável, embora o núcleo técnico da resposta esteja correto.
- **gpt-5-petrobras:medium:** aprova

### 4e96c8ab4a-b0-A1 · facil · Operação de Separadores Trifásicos

**P:** Qual é a função da válvula da linha inferior de água livre em um separador trifásico e como ela se relaciona com o controle da interface água-óleo?

**R:** A válvula da linha inferior regula a vazão de saída da água livre pelo fundo do separador. Sua abertura não deve responder ao nível total de líquido, mas ao nível da interface água-óleo, porque a variável crítica nessa descarga é a posição da camada de água no fundo do vaso. Assim, quando o controlador de interface atua sobre essa válvula, ele ajusta a retirada de água para manter a interface na faixa desejada e preservar a separação entre as fases líquidas.

- **gpt-5-2-petrobras:medium:** reprova (suporte) · Falta de suporte: a resposta inclui prescrição/critério ('não deve responder ao nível total') e justificativas de processo ('variável crítica', 'manter faixa desejada', 'preservar separação') não explicitadas em F1–F3.; Para ficar totalmente suportada, a resposta deve se limitar ao que os fatos dizem: válvula no fundo regula vazão de água livre e é acionada por controle/medição de interface.
- **o3-petrobras:medium:** aprova
- **gpt-5-4-petrobras:medium:** aprova
- **gpt-5-petrobras:medium:** reprova (suporte) · Parte da resposta não tem suporte explícito em F1–F3: 'manter a interface na faixa desejada' e 'preservar a separação entre as fases líquidas'.; Uso de F3 (caso P-53) como ilustração de atuação do controlador pode sugerir generalização se tomado isoladamente, embora F2 já suporte o princípio geral.

### 4e96c8ab4a-b0-A2 · media · Operação de Separadores Trifásicos

**P:** Em um separador trifásico horizontal, a pressão do vaso permanece controlada pela saída de gás no topo, mas os níveis internos começam a se desviar após variação na formação de óleo e água. Como a abertura das válvulas de saída de óleo e de água deve regular as vazões de descarga para manter o inventário líquido e a separação estáveis?

**R:** As correções devem ser feitas pelas válvulas das correntes líquidas, porque são elas que regulam o inventário no vaso. A válvula de saída de óleo deve responder ao controle de nível do líquido para ajustar a vazão dessa fase, enquanto a válvula da linha inferior de água deve responder ao nível de interface água-óleo para ajustar especificamente a vazão de água livre. Esse arranjo mantém os níveis internos compatíveis com a separação e evita deslocamento indevido da interface. A pressão, por sua vez, continua sendo tratada separadamente pela modulação da saída de gás no topo, sem usar as saídas líquidas para compensar desvio de pressão.

- **gpt-5-2-petrobras:medium:** reprova (suporte) · Falta de suporte: ‘evita deslocamento indevido da interface’ não está explicitamente em F1/F2.; Falta de suporte: ‘sem usar as saídas líquidas para compensar desvio de pressão’ não está explicitamente em F1/F2.; Completude parcialmente prejudicada porque a justificativa de estabilidade de separação/interface depende de trechos não citados; pode ser resolvido removendo/ajustando essas frases ou citando fatos adicionais se disponíveis.
- **o3-petrobras:medium:** aprova
- **gpt-5-4-petrobras:medium:** aprova
- **gpt-5-petrobras:medium:** aprova

### 4e96c8ab4a-b1-A1 · dificil_A · Operação de Separadores Trifásicos

**P:** Um separador trifásico de um FPSO passou a operar de forma recorrente com condições de processo diferentes das previstas no envelope de projeto. Ao mesmo tempo, há atraso de inspeções, histórico incompleto no cadastro do ativo e indicação de deterioração das barreiras anticorrosivas internas. A equipe discute manter o plano prescritivo original porque o vaso continua disponível e sem vazamento. Nesse cenário, o que justifica revisar o regime de inspeção e reforçar a abordagem baseada em risco no sistema de integridade?

**R:** A revisão se justifica porque a combinação de desvio das condições reais de processo, atraso de inspeções, perda de rastreabilidade e deterioração das barreiras anticorrosivas aumenta a incerteza sobre a condição remanescente do vaso e eleva o risco de perda de contenção. Mudanças do processo em relação ao envelope de projeto são um dos principais perigos potenciais para Loss of Containment em FPSO, podendo evoluir para acidente maior se não houver prevenção, detecção e mitigação. Se o sistema admite inspeção prescritiva e/ou baseada em risco, manter o plano original sem reavaliar frequência, escopo e prioridade deixa de ser tecnicamente robusto quando o serviço mudou e o histórico perdeu confiabilidade. Além disso, a continuidade da proteção anticorrosiva precisa ser mantida ao longo da vida operacional, e o descumprimento do planejamento de inspeções já foi associado a insuficiência dessa proteção sem justificativa técnica formal. O caminho prudente é reforçar o controle do ativo e revisar o plano com base no risco.

- **gpt-5-2-petrobras:medium:** reprova (suporte) · Falta de suporte explícito nos F# para algumas afirmações prescritivas/conclusivas (incerteza remanescente; necessidade de reavaliar frequência/escopo/prioridade; 'caminho prudente' de revisar com base no risco).; Para ficar estritamente suportado, a resposta deve amarrar a justificativa apenas ao que os F# afirmam (perigo de LoC por desvio do envelope, fragilidade do registro/histórico, falha de inspeções afetando barreiras anticorrosivas e possibilidade de RBI), evitando recomendações não enunciadas nos fatos.
- **o3-petrobras:medium:** aprova
- **gpt-5-4-petrobras:medium:** reprova (suporte, escopo) · Suporte parcial: há conclusões e critérios formulados além do que os F# citados sustentam diretamente.; Desalinhamento de escopo com o subtópico 'Operação de Separadores Trifásicos'; a questão avalia integridade/inspeção de vasos.; A resposta usa linguagem conclusiva de governança ('reavaliar frequência, escopo e prioridade', 'tecnicamente robusto') sem fato específico correspondente.
- **gpt-5-petrobras:medium:** aprova

### 4e96c8ab4a-b2-A1 · dificil_B · Operação de Separadores Trifásicos

**P:** Após mudança no fluido produzido, um separador trifásico passa a apresentar nível instável, alarmes recorrentes de alto nível e indícios de líquido na linha de gás. Em alguns eventos, o alarme sensibiliza a lógica de trip antes de a equipe confirmar aumento real de inventário líquido. Qual encadeamento técnico explica melhor esse comportamento e qual causa deve ser tratada como primária no diagnóstico para evitar carryover e shutdowns indevidos?

**R:** O encadeamento mais provável é formação de espuma no interior do vaso, favorecida por impurezas no líquido e/ou pela natureza do óleo. A espuma ocupa volume útil, reduz a área livre de escoamento do gás, piora a representatividade da medição de nível e aumenta o arraste de líquido para a saída de gás. Assim, um alarme de nível alto pode refletir a presença de espuma tanto quanto um aumento de líquido claro; se o nível total também estiver alto, o carryover para o gás se agrava. Isso explica por que um problema inicialmente de separação pode evoluir para alarme, intertravamento e trip, além de expor compressores a líquido. No diagnóstico, a causa primária a tratar é a espuma, não assumir automaticamente que todo alarme indica apenas inventário excessivo. A mitigação prioritária é evitar operação em nível muito alto e assegurar quebra de espuma no vaso, complementada por remoção de névoa na descarga de gás.

- **gpt-5-2-petrobras:medium:** reprova (suporte) · Falta de suporte/citação para a afirmação sobre influência do tipo/natureza do óleo na formação de espuma (exige F2).; Para sustentar a recomendação de remoção de névoa como barreira complementar, a base factual indicada nas notas também passa por F2 (junto com F1/F5), que não foi citado; ajustar citações e/ou redação para ficar estritamente suportado.
- **o3-petrobras:medium:** aprova
- **gpt-5-4-petrobras:medium:** aprova
- **gpt-5-petrobras:medium:** aprova

### 6ab1aa24b5-b0-A1 · facil · Operação de Tratadores Eletrostáticos

**P:** Por que o desempenho do tratador eletrostático influencia não só a qualidade do óleo exportado, mas também a carga enviada ao sistema de água produzida?

**R:** Porque a separação no processamento primário precisa atender dois destinos ao mesmo tempo: o óleo e a água. O tratamento de água produzida tem a função de enquadrar essa corrente para descarte, reinjeção ou utilidades, controlando contaminantes como óleo, sais e metais pesados conforme a destinação. Assim, quando a separação a montante não é adequada, o efeito não fica restrito ao teor de água no óleo exportado; ele também altera a quantidade de óleo que segue com a corrente aquosa. Como o sistema de tratamento de água foi projetado para receber, na saída do separador trifásico, água com cerca de 1000 ppm de óleo disperso, um aumento dessa carga pode tirar a operação da condição de projeto e dificultar o enquadramento final da água.

- **gpt-5-2-petrobras:medium:** reprova (correcao_tecnica, suporte) · Falta suporte nos fatos para o nexo específico entre desempenho do tratador eletrostático/separação e aumento de óleo na corrente aquosa (a resposta fala do tratador, mas F1/F2 não mencionam tratador nem esse mecanismo).; Com o material fornecido (apenas F1 e F2), não há como sustentar explicitamente o acoplamento operacional pedido no alvo A1; logo não é apenas ajuste de redação.
- **o3-petrobras:medium:** aprova
- **gpt-5-4-petrobras:medium:** aprova
- **gpt-5-petrobras:medium:** aprova

### 6ab1aa24b5-b0-A2 · media · Operação de Tratadores Eletrostáticos

**P:** Em uma unidade, a água produzida piora de qualidade e passa a exigir maior esforço do tratamento, mas o óleo de exportação ainda permanece dentro da especificação. Qual interpretação operacional é mais adequada para esse quadro?

**R:** A interpretação mais adequada é suspeitar de desvio de separação a montante, no separador trifásico e/ou no tratador eletrostático, com aumento da parcela de óleo que está seguindo pela corrente aquosa. O fato de o óleo de exportação ainda atender à especificação não elimina o problema, porque o tratamento de água produzida tem objetivo próprio: enquadrar a água para descarte, reinjeção ou utilidades, controlando contaminantes. Se mais óleo passar para a água, a carga de entrada no sistema de tratamento aumenta. Isso é crítico porque esse sistema foi projetado para operar com água contendo, na saída do separador trifásico, cerca de 1000 ppm de óleo disperso, e não para receber cargas de óleo bruto com baixa diluição na água. Portanto, a piora da água pode aparecer antes de um desvio evidente na exportação do óleo.

- **gpt-5-2-petrobras:medium:** reprova (suporte) · Falta de suporte explícito (via F1/F2) para o nexo diagnóstico 'piora da água sem perda do óleo exportado' => 'desvio de separação no separador/tratador'. É necessário incluir/citar um fato da nota que registre esse sintoma/diagnóstico (ou restringir a resposta apenas ao que F1/F2 suportam, o que prejudicaria o alvo A2).; A frase final ('pode aparecer antes') também não está diretamente suportada por F1/F2; precisa de fato específico da nota descrevendo essa precedência como indício observado/esperado.
- **o3-petrobras:medium:** reprova (suporte) · Falta de suporte factual explícito para a principal inferência sobre o desvio de separação (afirmação 1).
- **gpt-5-4-petrobras:medium:** aprova
- **gpt-5-petrobras:medium:** reprova (suporte) · Falta de suporte factual explícito (F1/F2) para o diagnóstico de desvio no separador/tratador como causa da piora da água.; A afirmação de que a piora da água pode preceder o desvio na exportação do óleo não está amparada em F1/F2.

### 6ab1aa24b5-b1-A1 · dificil_A · Operação de Tratadores Eletrostáticos

**P:** Em um FPSO, a separação primária está operando de forma estável e a equipe entende que isso já deveria bastar para liberar o óleo para exportação. Porém, a corrente exportada ainda precisa passar pelo tratador eletrostático e ser verificada quanto às condições finais da unidade. Por que uma boa separação primária, isoladamente, pode não ser suficiente para considerar o óleo pronto para exportação?

**R:** Porque a condição de exportação não é definida apenas pela separação grosseira das fases na etapa primária. Na unidade offshore, o objetivo do processamento é entregar um óleo tratado e estabilizado que atenda simultaneamente às condições de exportação, incluindo BSW, salinidade e temperatura. Nesse arranjo de processo, o óleo que sai do separador de produção ainda segue para o tratador eletrostático, cuja função é enquadrar o teor de BSW. Portanto, mesmo com boa separação primária, o óleo ainda pode não estar na condição final requerida. Além disso, o produto exportado corresponde ao petróleo tratado da unidade, isto é, ao blend dos fluidos produzidos pelos poços interligados, e essa qualidade final deve ser avaliada no conjunto tratado, não em uma etapa isolada do processo.

- **gpt-5-2-petrobras:medium:** reprova (suporte) · Falta de suporte: a resposta introduz a ideia de 'separação grosseira' na etapa primária sem que isso conste em F1/F2 ou como fato explícito na nota; pode ser corrigido removendo/neutralizando essa caracterização e mantendo apenas que a separação primária não garante, por si só, o atendimento simultâneo às condições de exportação.
- **o3-petrobras:medium:** aprova
- **gpt-5-4-petrobras:medium:** aprova
- **gpt-5-petrobras:medium:** aprova

### 9a7659b69d-b0-A1 · facil · Operação Geral FPSO

**P:** Qual é a finalidade da logística offshore para a continuidade operacional de uma unidade marítima?

**R:** Garantir o atendimento da unidade marítima com os insumos e equipamentos necessários à operação contínua. Para isso, a logística offshore organiza um fluxo integrado de materiais e informações entre fornecedores, armazéns, terminais portuários e a própria unidade, de modo que o suporte chegue de forma compatível com a necessidade operacional.

- **gpt-5-2-petrobras:medium:** reprova (suporte) · Falta de suporte factual para a ideia de 'chegar de forma compatível com a necessidade operacional' (prazo/compatibilidade não está em F1). Sugestão: remover ou reescrever mantendo apenas 'visando atender... com insumos e equipamentos necessários à continuidade operacional', conforme F1.
- **o3-petrobras:medium:** aprova
- **gpt-5-4-petrobras:medium:** aprova
- **gpt-5-petrobras:medium:** aprova

### 9a7659b69d-b0-A2 · media · Operação Geral FPSO

**P:** Em uma locação pioneira, foi adotado um FPSO com armazenamento a bordo e exportação do óleo por alívio. Como esse arranjo afeta a necessidade de linhas de exportação, oleodutos e manifolds submarinos?

**R:** Esse arranjo reduz a necessidade desses elementos de infraestrutura submarina e pode eliminá-los nas condições descritas. Como o FPSO armazena o óleo produzido e depois o transfere a um navio aliviador para transporte até terra, o escoamento não depende de linhas fixas de exportação, oleodutos e manifolds submarinos, o que aumenta a flexibilidade e torna a solução conveniente para locações pioneiras.

- **gpt-5-2-petrobras:medium:** reprova (correcao_tecnica, suporte) · Falta de suporte: a resposta afirma transferência para navio aliviador e transporte até terra sem base em F2 (único fato citado).; Para ficar suportada, a resposta deve restringir-se ao que F2 afirma (flexibilidade e eliminação/redução de infraestrutura submarina) ou citar fatos adicionais que descrevam o navio aliviador/transporte.
- **o3-petrobras:medium:** aprova
- **gpt-5-4-petrobras:medium:** reprova (suporte) · A resposta inclui detalhe não suportado pelos fatos fornecidos: transferência para navio aliviador e transporte até terra.; O conjunto de fatos citado para a questão (apenas F2) não sustenta integralmente todas as afirmações da resposta.
- **gpt-5-petrobras:medium:** reprova (suporte) · A afirmação sobre transferência para navio aliviador e transporte até terra não está suportada pelos fatos fornecidos (F1, F2).; A resposta inclui detalhe operacional além do necessário para o alvo, o que exige suporte documental que não foi apresentado.

### 9a7659b69d-b2-A1 · dificil_B · Operação Geral FPSO

**P:** Em um FPSO com controle manual, uma anomalia persiste por vários turnos. Não há medidores de vazão confiáveis, o TOG online é duvidoso, um tanque usado na prática para água offspec aparece cadastrado como óleo, e a troca de turno não assegurou registro claro de mudanças e isolamentos. No supervisório, parte das mensagens associadas ao desvio não exige ação imediata. Qual diagnóstico deve ser priorizado e que verificações vêm antes de concluir perda real de desempenho do processo?

**R:** Deve-se priorizar o diagnóstico de perda de observabilidade da planta, não assumir de imediato perda real de desempenho. Em controle manual, a falta de vazão confiável e a baixa confiabilidade do TOG já reduzem a capacidade de acompanhar o processo com base objetiva. Se o tanque está documentalmente classificado como óleo, mas recebe água offspec, a interpretação de inventário, risco e comportamento do fluido fica enviesada. A equipe ainda pode estar analisando o desvio com contexto incompleto se a passagem de serviço não transferiu mudanças, isolamentos e condições operacionais. No supervisório, é preciso separar alarme de evento, porque evento não define ação imediata do operador. Antes de concluir por degradação real do processo, devem ser verificados: aderência entre cadastro e recebimento real do tanque, suficiência das medições para controle manual, conhecimento dos limites operacionais seguros pela sala de controle e qualidade do handover.

- **gpt-5-2-petrobras:medium:** reprova (suporte) · Suporte insuficiente para a priorização/conclusão: o material sustenta que há perda de confiabilidade/aderência da informação e risco de mascaramento, mas não estabelece como regra que o diagnóstico a 'priorizar' deve ser necessariamente 'perda de observabilidade' nem que 'não se deve assumir' perda real de desempenho; isso precisa ser reescrito como hipótese/linha de investigação compatível com os fatos.; A expressão 'perda de observabilidade' não aparece nos fatos; é um rótulo interpretativo aceitável, mas na forma atual vira conclusão não demonstrada. Pode ser corrigido vinculando explicitamente à 'redução da capacidade de acompanhar o desempenho por falta de medições confiáveis' (F1) e ao mascaramento por classificação/handover (F4/F6).
- **o3-petrobras:medium:** aprova
- **gpt-5-4-petrobras:medium:** aprova
- **gpt-5-petrobras:medium:** aprova

### 96c4f33979-b0-A1 · facil · Produção, processo e processamento do óleo

**P:** Por que a inspeção interna, antes da partida ou do carregamento do leito, deve verificar ao mesmo tempo a integridade dos componentes internos e a presença de contaminantes em vasos, trocadores, filtros e tubulações?

**R:** Porque a liberação para a etapa seguinte depende de confirmar duas condições ao mesmo tempo: que o equipamento esteja internamente montado e preservado como previsto para sua função e que não haja contaminação incompatível com essa condição. Em vasos para leito de zeólitas, isso inclui refratário sem fissuras, furos ou rachaduras e ausência de umidade excessiva ou água acumulada. Em filtros coalescedores e de particulado, inclui montagem correta dos internos e integridade dos elementos. Em trocadores e tubulações, inclui ausência de resíduos sólidos, depósitos e resíduos de corrosão. Se qualquer desses desvios existir, o equipamento não está em condição interna compatível com entrada em serviço ou com o carregamento do leito.

- **gpt-5-2-petrobras:medium:** reprova (correcao_tecnica, suporte, sem_generalizacao) · Falta suporte para o ‘porquê’ (relação causal/critério) pedido na pergunta; os fatos listam o que inspecionar, mas não justificam a necessidade de verificar simultaneamente integridade e contaminantes como princípio geral.; Generalização/critério decisório final (‘qualquer desvio’ implica incompatibilidade com entrada em serviço/carregamento) sem base nos F#.; A justificativa central da resposta (liberação depende de duas condições simultâneas) não está explicitada nos fatos fornecidos para todos os equipamentos.
- **o3-petrobras:medium:** aprova
- **gpt-5-4-petrobras:medium:** aprova
- **gpt-5-petrobras:medium:** aprova

### 96c4f33979-b0-A2 · media · Produção, processo e processamento do óleo

**P:** Na preparação de um sistema de desidratação para operação com gás natural, a inspeção encontra resíduos sólidos e depósitos no feixe do trocador, no casco e nas linhas de entrada de utilidades. Como isso pode degradar o desempenho do trocador antes mesmo da operação contínua?

**R:** Esses achados mostram que o trocador já entra em serviço com condição interna diferente da prevista. Resíduos e depósitos no feixe, no casco e nas linhas de utilidades podem reduzir a área livre de passagem, alterar a distribuição do escoamento e prejudicar a troca térmica. Assim, mesmo antes de uma campanha operacional longa, o equipamento pode apresentar menor eficiência porque o fluido de processo e a utilidade deixam de circular nas condições esperadas de projeto. Por isso, a presença desses materiais é um desvio de prontidão operacional e deve ser tratada antes da partida.

- **gpt-5-2-petrobras:medium:** aprova
- **o3-petrobras:medium:** reprova (suporte) · Suporte insuficiente: mecanismos de degradação não estão cobertos pelo único fato F4 citado. É necessário citar também os trechos da nota que tratam desses mecanismos ou ajustar a resposta para caber no escopo do F4.
- **gpt-5-4-petrobras:medium:** aprova
- **gpt-5-petrobras:medium:** aprova

### 1c3beb869e-b1-A1 · dificil_A · Produtos químicos

**P:** Um campo com injeção de água do mar passa a produzir água com fração crescente de água injetada. A partir desse avanço, surgem perda de desempenho no poço, aumento de restrições na coluna de produção e deposição também em linhas e equipamentos de superfície. Sem mudança informada na estratégia de produção, a hipótese de incompatibilidade entre água injetada e água de formação com precipitação de sulfatos insolúveis é consistente com esse quadro? Justifique tecnicamente pelo momento e pelos locais afetados.

**R:** Sim, a hipótese é tecnicamente consistente. O aumento progressivo da fração de água injetada na água produzida indica aproximação ou ocorrência de breakthrough, isto é, a chegada da água de injeção ao produtor. A partir desse momento, os problemas de incrustação tendem a se tornar mais sérios e o poço deve ser monitorado continuamente. Isso faz sentido porque o contato entre água de injeção e água de formação, sob condições termodinâmicas adequadas, pode gerar depósitos insolúveis como sulfato de bário, sulfato de estrôncio e sulfato de cálcio. O fato de os sintomas aparecerem tanto no poço quanto em linhas e equipamentos de superfície reforça a suspeita, porque a precipitação pode ocorrer desde o meio poroso e vizinhança do poço até a coluna de produção e as instalações de superfície. Portanto, o momento de aparecimento e a distribuição dos efeitos são compatíveis com incrustação por mistura de águas.

- **gpt-5-2-petrobras:medium:** reprova (suporte) · Falta de suporte explícito para usar ‘fração crescente de água injetada na água produzida’ como indicador de aproximação/ocorrência de breakthrough com base apenas em F1/F4/F7.; Para ficar 100% aderente aos fatos, a resposta pode condicionar o raciocínio a ‘se houve breakthrough/chegada da água injetada ao produtor’ (F7) e então conectar aos mecanismos/deposição (F4, F1), sem afirmar o indicador não citado.
- **o3-petrobras:medium:** aprova
- **gpt-5-4-petrobras:medium:** aprova
- **gpt-5-petrobras:medium:** aprova

### 1c3beb869e-b2-A1 · dificil_B · Produtos químicos

**P:** Uma linha de aço-carbono reduziu o problema de H2S após injeção de glioxal, sem formação de sais, mas a corrosão aumentou. A equipe propõe apenas adicionar ou elevar o inibidor e seguir operando. Qual decisão técnica é mais adequada para validar esse pacote químico antes de consolidá-lo na rotina do FPSO?

**R:** A decisão mais adequada é manter a análise focada no meio real e validar o pacote combinado, não aprovar o ajuste por analogia. O glioxal pode remover H2S sem incrustação, mas em baixo pH torna o meio corrosivo para aço-carbono; portanto, a piora não deve ser atribuída só ao H2S residual nem descartada pela ausência de depósitos. O inibidor pode viabilizar o uso do glioxal porque atua por adsorção e estabilização do filme de óxido, com barreira difusional adicional, mas sua eficácia depende de conseguir manter essa proteção no meio tratado. Como combinações químicas podem piorar ou melhorar a proteção, é necessário ensaio representativo com o material e a matriz do sistema, seguido de monitoramento das taxas de corrosão e verificação dos pontos mais críticos em operação antes de consolidar dosagem e continuidade do pacote.

- **gpt-5-2-petrobras:medium:** reprova (suporte) · Falta suporte explícito (F#) para: (i) ‘ensaio representativo com a matriz do sistema’ como critério (seria melhor ancorar em fatos de mimetização/condições representativas, p.ex. F16/F19, que não foram citados) e (ii) ‘eficácia depende de manter proteção/barreira estável’ como conclusão operacional (não está literal em F2).; Trecho final sobre ‘consolidar dosagem e continuidade’ é plausível, mas não está suportado por fato citado; pode ser removido ou reescrito como ‘antes de manter/expandir a aplicação’ sem afirmar consolidação de dosagem.; Para robustez, faltou citar fatos que sustentem explicitamente a lógica de testar em condição que mimetiza operação e/ou de combinar ensaio com monitoramento (p.ex., F16/F19/F20), se a resposta for manter essa linha argumentativa.
- **o3-petrobras:medium:** aprova
- **gpt-5-4-petrobras:medium:** aprova
- **gpt-5-petrobras:medium:** aprova

### e8459723b0-b0-A1 · facil · Sistema de Alívio e Flare

**P:** Qual é a função do comissionamento na transição entre construção e operação, e por que o uso de checklists é importante para assegurar aderência ao projeto detalhado?

**R:** O comissionamento faz a ponte entre a montagem física e a prontidão operacional. Sua função é verificar, inspecionar e testar os componentes físicos do empreendimento e, depois, confirmar o funcionamento dos processos antes do início pleno da operação, eliminando erros que poderiam ser transferidos para a rotina operacional. Os checklists são importantes porque estruturam o conjunto de testes para garantir cobertura completa dos componentes do projeto e confirmar que os itens necessários à futura operação estejam disponíveis e operando exatamente como previsto no projeto detalhado. Assim, não basta o equipamento estar instalado; ele precisa demonstrar desempenho compatível com o que foi definido em engenharia para que a liberação para operação tenha base técnica.

- **gpt-5-2-petrobras:medium:** reprova (suporte) · Falta de suporte explícito (com os fatos citados) para expressões/conclusões como 'ponte', 'prontidão operacional' e 'liberação para operação ter base técnica'. Pode ser corrigido reescrevendo apenas com o conteúdo de F1 e F3 (verificar/testar componentes e processos; checklists para cobrir itens do projeto e assegurar disponibilidade/operação conforme o detalhamento).
- **o3-petrobras:medium:** aprova
- **gpt-5-4-petrobras:medium:** aprova
- **gpt-5-petrobras:medium:** aprova

### e8459723b0-b0-A2 · media · Sistema de Alívio e Flare

**P:** Em um vendor package de sistema de flare, a equipe pretende receber o pacote após os testes, mas sem participação ativa de operadores e técnicos no comissionamento com o fornecedor. Por que essa decisão tende a reduzir a capacidade futura de operação e manutenção do sistema?

**R:** Porque a participação ativa de operadores e técnicos no comissionamento com o fornecedor aumenta a familiaridade prática com o equipamento, o que melhora a capacidade futura de operar e manter o pacote. Sem esse envolvimento, cresce o risco de a equipe receber o sistema com conhecimento prático limitado de operação e manutenção. Além disso, a transição para a operação depende de arranjos adequados de treinamento, que devem existir quando o projeto estiver fixado e os procedimentos operacionais disponíveis. Se houver mudança no modo de operação, o retreinamento passa a ser necessário. Portanto, excluir a equipe do comissionamento enfraquece a absorção de conhecimento operacional e de manutenção justamente na fase em que esse aprendizado é mais eficaz.

- **gpt-5-2-petrobras:medium:** reprova (suporte) · Falta de suporte para a afirmação causal 'a transição para a operação depende de...' (F11 não estabelece essa dependência).; Falta de suporte para 'na fase em que esse aprendizado é mais eficaz' (não consta dos fatos).; Há conteúdo adicional sobre treinamento/retreinamento que é pertinente, mas precisa ser redigido sem extrapolar causalidades não afirmadas nos fatos.
- **o3-petrobras:medium:** aprova
- **gpt-5-4-petrobras:medium:** reprova (suporte) · Há falta de suporte para a afirmação final de que essa é 'a fase em que esse aprendizado é mais eficaz'.; A resposta traz conteúdo adicional sobre treinamento e retreinamento que é compatível com os fatos, mas vai além do necessário para responder ao alvo com objetividade.
- **gpt-5-petrobras:medium:** aprova

### e8459723b0-b1-A1 · dificil_A · Sistema de Alívio e Flare

**P:** Em um FPSO, após modificações no topo da planta, a equipe pretende recolocar em serviço o flare e manter um vent atmosférico existente. Na condição de vento prevista para a partida, há possibilidade de abertura de gás antes da chama estabilizar. Qual deve ser o uso técnico dos estudos de radiação térmica e dispersão para decidir se o arranjo continua aceitável e para definir restrições do procedimento de partida do flare?

**R:** Os estudos devem ser usados em duas frentes integradas. Primeiro, verificar o arranjo físico: a avaliação de radiação confirma se a chama do flare pode expor pessoas, equipamentos e áreas da instalação a níveis térmicos inadmissíveis, o que depende da geometria da chama e da posição dos pontos avaliados. A avaliação de dispersão verifica se uma liberação não ignitada pode alcançar áreas sensíveis, como o deck de processo, tanto pelo flare quanto pelo vent atmosférico. Se houver risco de toque de nuvem ou de exposição térmica excessiva, o arranjo não deve ser considerado aceitável sem correção. Segundo, a partida do flare deve incorporar os resultados de dispersão e as condições atmosféricas do momento, especialmente velocidade e direção do vento, para evitar venting não ignitado prolongado antes da ignição. Como há vent atmosférico, ele também deve ter proteção contra flash-back, como flame arrestor ou dispositivo equivalente.

- **gpt-5-2-petrobras:medium:** reprova (suporte) · Falta de suporte: a conclusão normativa sobre aceitabilidade do arranjo ('não deve ser considerado aceitável sem correção') não está explicitada nos fatos citados; para ficar suportado, a resposta deve limitar-se a dizer que os estudos servem para verificar/determinar o risco e subsidiar decisão de necessidade de mudanças, sem impor um critério decisório não fornecido.; (Menor) Pode-se explicitar melhor a separação 'dispersão pelo flare' (F2) versus 'dispersão pelo vent atmosférico' (F3) para evitar leitura de que um único fato suporta ambos indistintamente.
- **o3-petrobras:medium:** aprova
- **gpt-5-4-petrobras:medium:** aprova
- **gpt-5-petrobras:medium:** aprova

### 69f5898918-b0-A1 · facil · Sistema de captação e tratamento de água do mar para injeção no reservatório

**P:** Como sulfato, presença de H2S, Eh e pH podem ser usados para identificar atividade de bactérias redutoras de sulfato nas condições em que esses parâmetros são aplicados para esse diagnóstico?

**R:** Nessas condições, a identificação de atividade de bactérias redutoras de sulfato deve ser feita pela interpretação conjunta desses parâmetros, e não por um sinal isolado. A dosagem de sulfato, o teste qualitativo de H2S e as medidas de Eh e pH foram usados para confirmar a presença e a atividade desse grupo. O H2S funciona como indicador relevante do processo associado à geração de sulfeto, enquanto sulfato, Eh e pH ajudam a caracterizar um quadro compatível com esse metabolismo redutivo. Portanto, quando esse conjunto de variáveis aponta na mesma direção, a hipótese técnica consistente é atividade de bactérias redutoras de sulfato.

- **gpt-5-2-petrobras:medium:** reprova (suporte) · Falta de suporte para formulação normativa/obrigatória (“deve ser feita”) e para a exclusão explícita de uso de parâmetro isolado (“e não por um sinal isolado”). Isso pode ser corrigido com reescrita para linguagem descritiva (ex.: “pode ser feita/foi feita” e “a avaliação conjunta é usada/é mais robusta”).
- **o3-petrobras:medium:** aprova
- **gpt-5-4-petrobras:medium:** aprova
- **gpt-5-petrobras:medium:** aprova

### 69f5898918-b1-A1 · dificil_A · Sistema de captação e tratamento de água do mar para injeção no reservatório

**P:** Após o comissionamento da injeção de água do mar em um FPSO, a equipe passou a misturar correntes de água de origens diferentes para manter vazão. Em seguida, houve queda de injetividade, aumento de restrição em válvulas e inspeção com depósitos aderidos; a análise química da mistura indicou tendência à precipitação de sais pouco solúveis quando a água injetada entra em contato com a água de formação. Qual diagnóstico é mais consistente para a perda de desempenho do sistema?

**R:** O diagnóstico mais consistente é incompatibilidade química entre a água de injeção e a água de formação, com formação de incrustações. A mudança para mistura de correntes com características diferentes é um gatilho relevante, porque essa condição pode levar à precipitação de sais e gerar incrustação tanto nas tubulações quanto no reservatório. Esse mecanismo explica a queda de injetividade, a restrição em válvulas e os depósitos observados. Também é compatível com risco de redução da permeoporosidade da formação e favorecimento de corrosão localizada por pitting. Como a escolha da água depende das características do reservatório e da compatibilidade com a formação receptora, o caso aponta mais para scale por mistura incompatível do que para um problema definido primariamente como sólidos externos, atividade bacteriana ou corrosividade isolada. O monitoramento desde o início da injeção é justamente a barreira para detectar essa deterioração cedo e corrigir a operação antes de dano severo.

- **gpt-5-2-petrobras:medium:** reprova (suporte) · Suporte insuficiente para atribuir diretamente a 'queda de injetividade' ao mecanismo usando apenas os F# citados (embora seja plausível tecnicamente).; Falta de suporte, nos F# citados, para a exclusão comparativa de outras causas (sólidos, atividade bacteriana, corrosividade isolada); a nota teria que trazer (como fato citável) critérios diferenciais, ou a resposta deve ser reescrita sem essa comparação.; A resposta pode ser ajustada para ficar estritamente suportada: focar em obstrução/deposição/precipitação e compatibilidade com formação, e remover (ou qualificar) as partes não suportadas.
- **o3-petrobras:medium:** aprova
- **gpt-5-4-petrobras:medium:** reprova (suporte) · A exclusão explícita de sólidos externos, atividade bacteriana e corrosividade isolada como causas primárias não está sustentada por fato F# específico.; A associação direta com 'queda de injetividade' tem suporte apenas indireto nos fatos citados; os fatos falam em dano à formação, redução de permeoporosidade, obstrução e redução de produção.; Há falta de suporte integral para todas as afirmações substantivas da resposta, o que reprova em suporte.
- **gpt-5-petrobras:medium:** aprova

### 69f5898918-b2-A1 · dificil_B · Sistema de captação e tratamento de água do mar para injeção no reservatório

**P:** Em um FPSO, aumentaram os ciclos curtos de filtração e os eventos de retrolavagem no tratamento de água do mar. Ao mesmo tempo, cresceram as oscilações de vazão na sucção das bombas de injeção e o atendimento aos poços ficou irregular. Sem interromper a injeção, qual diagnóstico deve ser priorizado e qual elemento do sistema ajuda a diferenciar se a instabilidade vem da qualidade/carga de sólidos captada ou de limitação hidráulica de alimentação?

**R:** O diagnóstico prioritário é verificar se a água captada passou a impor maior carga ou variabilidade de sólidos ao pré-tratamento, porque isso encurta o ciclo dos filtros e aumenta a necessidade de retrolavagem. A retrolavagem é consequência esperada da obstrução do leito por partículas retidas e gera períodos em que a disponibilidade de água filtrada fica mais variável. Se essa variabilidade chega às bombas, a oscilação observada pode ser efeito secundário da captação e da filtração, não falha primária de bombeio. Para diferenciar isso de limitação hidráulica de alimentação, o ponto-chave é avaliar se o arranjo de desacoplamento está cumprindo sua função: entrada de água do mar tratada para repor suprimento e vaso de injeção mantendo pressão constante às bombas. Se esse amortecimento estiver eficaz, a causa mais provável está a montante, na captação/filtração; se não, a limitação hidráulica ganha prioridade.

- **gpt-5-2-petrobras:medium:** reprova (correcao_tecnica, suporte) · Falta de suporte para ‘disponibilidade variável de água filtrada’ como efeito direto da retrolavagem chegando às bombas (não está em F8).; Falta de suporte para a regra decisória ‘se vaso eficaz então causa a montante’/‘se não então hidráulica’ (não há fato que estabeleça essa inferência).; A menção à ‘entrada de água do mar tratada para repor suprimento’ deveria ser alinhada ao fato F6 (entrada de água salgada quando cai a água produzida) ou removida para não extrapolar.
- **o3-petrobras:medium:** aprova
- **gpt-5-4-petrobras:medium:** reprova (suporte) · Falta suporte factual para afirmar que a maior frequência de retrolavagem torna variável a disponibilidade de água filtrada às bombas.; Falta suporte factual direto para a regra diagnóstica final baseada no sucesso do amortecimento hidráulico.; A resposta fica incompleta ao não considerar explicitamente a reservação como parte da diferenciação da limitação hidráulica de alimentação.
- **gpt-5-petrobras:medium:** aprova

### 1332c32a59-b0-A2 · media · Sistema de drenagem aberta e fechada

**P:** Durante a operação, um override de proteção foi aplicado em painel remoto ou HMI sem conhecimento da sala de controle e sem autorização nem avaliação formal. Qual risco operacional essa prática introduz?

**R:** Ela introduz risco por degradação não controlada da função de proteção. Quando o override é aplicado sem conhecimento da sala de controle, sem autorização e sem avaliação apropriada, a instalação pode operar com a proteção instrumentada indisponível ou reduzida sem que essa condição seja gerida. Isso aumenta a exposição a perda de contenção, porque a barreira que deveria atuar automaticamente pode estar neutralizada justamente quando uma condição insegura ocorrer. Além disso, essa prática rompe o controle operacional sobre a indisponibilidade temporária da função de proteção.

- **gpt-5-2-petrobras:medium:** aprova
- **o3-petrobras:medium:** aprova
- **gpt-5-4-petrobras:medium:** reprova (escopo) · Falta amarração explícita ao subtópico 'sistema de drenagem aberta e fechada'; o cenário está formulado de modo genérico para proteção de processo.
- **gpt-5-petrobras:medium:** aprova

### 1332c32a59-b1-A1 · dificil_A · Sistema de drenagem aberta e fechada

**P:** Durante um descomissionamento parcial, um trecho de drenagem aberta com descarga overboard deixou de operar, mas ainda não recebeu segregação física definitiva. Como não há fluxo normal previsto, a equipe propõe retirar esse trecho do plano de inspeção e tratar o isolamento apenas na etapa final. Tecnicamente, por que essa decisão é frágil?

**R:** A decisão é frágil porque um trecho inoperante, mas ainda não segregado de forma definitiva, continua sendo um caminho potencial de comunicação entre convés, tanques e mar. Em linhas que passam no interior de tanques, a perda de integridade pode gerar retorno de gás ao convés, transferência de carga entre tanques e vazamento de óleo para o mar, riscos que precisam ser tratados na análise de risco e na gestão de mudanças. Por isso, esses trechos não devem ser considerados neutros só por estarem fora da operação normal. Eles precisam permanecer sob rotina de gestão da integridade, com inspeções e manutenções, até que o isolamento e a segregação sejam efetivamente concluídos. Se uma falha ou desvio for identificado, o tratamento deve seguir por manutenção corretiva formal, com planejamento compatível com o risco e a complexidade, e não como pendência adiada para o fim do projeto.

- **gpt-5-2-petrobras:medium:** reprova (correcao_tecnica, suporte) · Falta de suporte (pelos fatos citados) para: manutenção do trecho inoperante/overboard no plano de inspeção ‘até’ a segregação definitiva e para a afirmação de que ele é ‘caminho de comunicação’ convés–tanques–mar.; Conclusão operacional específica (não retirar do plano e não postergar isolamento) não está explicitamente estabelecida em F4/F5/F6/F13; exigiria fato adicional sobre trechos inoperantes/overboard durante descomissionamento e necessidade de isolamento/bloqueios até a conclusão.
- **o3-petrobras:medium:** aprova
- **gpt-5-4-petrobras:medium:** aprova
- **gpt-5-petrobras:medium:** aprova

### 1332c32a59-b2-A1 · dificil_B · Sistema de drenagem aberta e fechada

**P:** Nos primeiros dias após o start-up de um sistema de drenagem aberta e fechada em um FPSO, surgem escoamento irregular, intervenções locais por acúmulo em drenos e suspeita de perda de segregação em seal pots e loops. O sistema havia sido formalmente liberado, mas há dúvida se o evento é falha de operação/manutenção inicial ou desvio introduzido antes da entrada em serviço. Qual origem deve ser priorizada na análise técnica e por quê?

**R:** A origem a priorizar é desvio de comissionamento e preparação pré-serviço, antes de atribuir o evento à rotina operacional inicial. Nos primeiros dias, esse padrão é compatível com cobertura incompleta dos testes ou transição insuficiente para a operação, mesmo com liberação formal do sistema, especialmente se o comportamento real diverge do previsto logo após a partida. Na preparação física, flushing e limpeza removem detritos; se isso falhou, podem permanecer materiais que depois bloqueiam drenos e headers. Se houve uso de água, também era necessário drenar pontos baixos, remover residual com ar seco e preservar com ar seco ou nitrogênio quando o sistema ficaria vazio por alguns dias; falhas aí favorecem problemas já na partida. A inspeção rotineira de selos e bloqueios continua necessária, mas, nesse momento, ela pode estar apenas revelando anomalias semeadas antes da entrada em serviço, inclusive perda da função de segregação ou obstrução por detritos.

- **gpt-5-2-petrobras:medium:** reprova (correcao_tecnica, suporte, sem_generalizacao) · Conclusão técnica desequilibrada: para o sintoma de perda de segregação em seal pots/loops, os fatos apontam primariamente para integridade do selo e manutenção do selo líquido (F8/F9), não para flushing/drenagem (F4/F5).; Falta de suporte: afirma que perda de segregação pode ter sido “semeada” no comissionamento sem citar/ancorar mecanismo nos fatos fornecidos.; Generalização: trata “priorizar comissionamento” como regra para o conjunto de sintomas, sem condicionar por evidências diagnósticas (detritos/obstrução vs. selos vazios/não íntegros).
- **o3-petrobras:medium:** aprova
- **gpt-5-4-petrobras:medium:** aprova
- **gpt-5-petrobras:medium:** aprova

### b5d9016da7-b1-A1 · dificil_A · Tratamento de água produzida para descarte

**P:** Em um FPSO, a água produzida passou a sair pior da bateria de hidrociclones. Ao mesmo tempo, análises na alimentação desse estágio mostraram óleo disperso acima de 1000 mg/L, após instabilidade no separador e no tratador eletrostático. Sem evidência de perda de pressão de alimentação aos hidrociclones, qual causa é mais provável para a piora e por quê?

**R:** A causa mais provável é sobrecarga por arraste de óleo a montante. Nesse trem de processo, os hidrociclones recebem a corrente aquosa já separada nos estágios anteriores e atuam como etapa intermediária antes do flotador, não como substitutos de uma boa separação primária. Há uma condição de alimentação: a água que sai dos separadores deve chegar a esse estágio com até 1000 mg/L de óleo disperso. Se esse valor é ultrapassado junto com instabilidade no separador e no tratador eletrostático, a interpretação mais consistente é deficiência a montante carregando óleo excessivo para o tratamento subsequente. Perda de desempenho no próprio hidrociclone seria mais diretamente suspeita se houvesse indício de comprometimento do seu mecanismo de operação, que depende de alimentação tangencial sob pressão para gerar o campo centrífugo de separação.

- **gpt-5-2-petrobras:medium:** reprova (suporte, sem_generalizacao) · Falta de suporte explícito para a afirmação normativa/interpretativa de que hidrociclones “não substituem” boa separação primária (não está em F1/F2 como enunciado factual).; Generalização do limite de 1000 mg/L como condição universal para ‘um FPSO’, quando F1 o apresenta no contexto/configuração descrita (P-53). Recomenda-se qualificar: ‘na configuração descrita’/‘neste arranjo’ e limitar a inferência ao caso do enunciado.
- **o3-petrobras:medium:** aprova
- **gpt-5-4-petrobras:medium:** reprova (autonomia, sem_generalizacao) · A autonomia é insuficiente porque o enunciado não explicita que 1000 mg/L é o critério relevante desse arranjo.; Há generalização indevida do valor de 1000 mg/L, que na nota vale para a configuração descrita e não foi qualificado assim na resposta.; A redação pode ser corrigida com o mesmo material, explicitando no enunciado ou na resposta que se trata do arranjo descrito e que o critério de alimentação é dado do caso.
- **gpt-5-petrobras:medium:** aprova

### b5d9016da7-b2-A1 · dificil_B · Tratamento de água produzida para descarte

**P:** Uma unidade de tratamento de água produzida passa a exigir múltiplas passagens para enquadrar TOG e, em alguns períodos, a operação recorre a by-pass manual. Ao mesmo tempo, há suspeita de medição lenta ou descalibrada da interface óleo/água no separador e no tratador eletrostático. Como estruturar o diagnóstico para distinguir perda de controle na separação primária de limitação do mecanismo dos equipamentos de tratamento, e qual frente deve ser verificada primeiro?

**R:** Estruture por HAZOP em nós separados: separação primária e tratamento. Em cada nó, defina o comportamento esperado, escolha parâmetros e aplique palavras-guia para gerar desvios, causas, consequências, ação e meios de detecção/atuação. No nó da separação primária, investigue “interface mais/menos” e “medição lenta/incorreta”, porque o controle da interface evita envio de óleo para a corrente de água produzida; se o sensor de interface tem deriva, erro ou atraso, ele degrada simultaneamente o controle e o próprio diagnóstico. No nó do tratamento, investigue se a carga recebida contém gotas finas ou óleo emulsionado, situação compatível com necessidade de múltiplas passagens, ou se há perda de capacidade por bloqueio de poros com retrolavagem. A prioridade é verificar primeiro a confiabilidade da medição e o controle de interface a montante, porque arraste de óleo da separação primária pode sobrecarregar o tratamento e mascarar uma limitação tecnológica real.

- **gpt-5-2-petrobras:medium:** reprova (suporte, sem_generalizacao) · Falta de suporte para a regra de priorização ('verificar primeiro') como critério obrigatório/geral.; Falta de suporte explícito para os efeitos 'sobrecarregar o tratamento' e 'mascarar limitação tecnológica' (consequência e nexo causal não estão afirmados nos F#).; Sem_generalizacao: a recomendação de prioridade aparece como regra sem ancoragem factual suficiente.
- **o3-petrobras:medium:** aprova
- **gpt-5-4-petrobras:medium:** reprova (correcao_tecnica, suporte) · A priorização 'verificar primeiro' a frente de medição/interface não está estabelecida pelos fatos como critério de decisão.; A ideia de que o problema a montante 'mascara' limitação tecnológica real não tem suporte explícito no material.; A resposta mistura fatos suportados com uma conclusão prescritiva adicional, o que reprova em suporte integral.
- **gpt-5-petrobras:medium:** aprova

### 9feff6fc72-b0-A1 · facil · Tratamento do Gás produzido

**P:** Qual é a função da desidratação do gás produzido e por que a remoção de água protege linhas e equipamentos a jusante contra condensação e danos?

**R:** A desidratação remove a água da corrente de gás sob pressão para reduzir a formação de fase aquosa e de hidratos ao longo do escoamento e do tratamento. Ao retirar essa água, diminui-se a chance de condensação líquida nas linhas e equipamentos a jusante, o que ajuda a evitar sua deterioração. Em arranjos usuais, o gás que permanece na fase gasosa após compressão e resfriamento segue para a unidade de secagem antes de tratamentos posteriores e da exportação. Essa etapa trata especificamente o teor de água do gás; ela não substitui o ajuste do ponto de orvalho de hidrocarbonetos, que é uma etapa distinta para controlar a condensação de componentes pesados do próprio gás.

- **gpt-5-2-petrobras:medium:** aprova
- **o3-petrobras:medium:** aprova
- **gpt-5-4-petrobras:medium:** aprova
- **gpt-5-petrobras:medium:** reprova (suporte) · A menção de que a secagem antecede a exportação não está suportada por citações literais dos fatos fornecidos.

### 9feff6fc72-b0-A2 · media · Tratamento do Gás produzido

**P:** Em uma unidade offshore de tratamento de gás, a equipe avalia manter desidratação por absorção com glicol ou migrar para tecnologia mais severa de remoção de umidade. Compare essas alternativas e indique por que a absorção líquida é frequente offshore e em que condição a especificação pode levar a outra escolha.

**R:** A absorção com glicol é frequente offshore porque o uso de absorventes líquidos favorece a logística de manuseio nesse ambiente e constitui a solução mais comum para secagem do gás. Nessa configuração, o glicol remove água da corrente e depois é regenerado para reuso. Quando a exigência de umidade é mais severa, a escolha pode migrar para tecnologias capazes de entregar gás mais seco, como peneiras moleculares, pois o TEG normalmente deixa teor de umidade mais alto do que o obtido com essas unidades. A decisão depende das condições de pressão e temperatura que o gás enfrentará depois do tratamento: regimes mais críticos tendem a exigir especificações de umidade mais rigorosas, enquanto condições menos severas podem admitir especificação menos restritiva e outras soluções de desidratação.

- **gpt-5-2-petrobras:medium:** aprova
- **o3-petrobras:medium:** aprova
- **gpt-5-4-petrobras:medium:** reprova (suporte) · Suporte insuficiente para a frase 'regimes mais críticos tendem a exigir especificações de umidade mais rigorosas' com os fatos citados (F8, F7, F1, F10).; A resposta está tecnicamente boa, mas uma afirmação causal relevante ficou apenas inferida, não explicitamente ancorada nos fatos citados.
- **gpt-5-petrobras:medium:** aprova

### 9feff6fc72-b2-A1 · dificil_B · Tratamento do Gás produzido

**P:** Após aumento de carga no trem de compressão com resfriamento entre estágios, uma unidade de desidratação por peneiras moleculares passou a entregar gás mais úmido, e a regeneração seguinte não recuperou o desempenho. Houve indícios de líquido a montante do adsorvedor. Qual mecanismo deve ser priorizado no diagnóstico e que barreira de processo precisa ser verificada primeiro para evitar recorrência?

**R:** O diagnóstico deve priorizar entrada de líquido no leito, e não apenas saturação normal da peneira ou falha isolada de regeneração. No trem de compressão, o resfriamento entre estágios reduz a temperatura do gás e promove condensação de frações mais pesadas, exigindo remoção do líquido formado em scrubbers ou separadores antes que o gás siga adiante. Se essa retenção falha, gotículas ou condensado podem alcançar o adsorvedor. Em peneiras moleculares, água líquida no leito pode solubilizar o ligante, formar cakes durante a regeneração, reduzir a área superficial e piorar a distribuição do fluxo, com caminhos preferenciais; por isso a regeneração deixa de restaurar o desempenho como faria em um leito apenas carregado de água adsorvida. A primeira barreira a verificar é a separação mecânica de líquidos a montante do adsorvedor, especialmente nos pontos a jusante dos resfriadores, onde o condensado volta a se formar.

- **gpt-5-2-petrobras:medium:** reprova (suporte) · Suporte incompleto: há conclusões diagnósticas (priorização do mecanismo vs. saturação/regeneração) e efeitos (regeneração não recupera) não explicitados nos fatos citados.; Alguns termos específicos (‘frações mais pesadas’, ‘gotículas’) não estão cobertos pelos fatos citados; ou devem ser suportados por fatos adicionais do conjunto ou removidos/reescritos para ficar estritamente aderente aos fatos citados.
- **o3-petrobras:medium:** aprova
- **gpt-5-4-petrobras:medium:** aprova
- **gpt-5-petrobras:medium:** aprova

### d87b10b437-b0-A2 · media · Estudos de Segurança

**P:** Em um estudo de segurança, um cenário foi classificado pela pior consequência que pode ocorrer imediatamente após a liberação do perigo, e sua frequência foi calculada assumindo barreiras disponíveis e operando conforme esperado. Como essa classificação deve ser interpretada?

**R:** Ela deve ser entendida como o risco do cenário sob hipóteses explícitas de desempenho das barreiras. A severidade usada na classificação corresponde à pior consequência imediata após a liberação do perigo, não a escalonamentos posteriores. Já a frequência estimada pressupõe que as barreiras de segurança estão disponíveis e atuam no nível de performance esperado. Portanto, o resultado não representa automaticamente o risco real em qualquer condição operacional: ele vale dentro dessas premissas sobre disponibilidade, adequação e desempenho das barreiras creditadas.

- **gpt-5-2-petrobras:medium:** reprova (suporte) · Falta de suporte explícito para 'não escalonamentos posteriores' (a nota só diz que a consequência considerada é a imediata) e para a conclusão sobre 'não representar automaticamente o risco real em qualquer condição operacional'. Para ficar suportado, a resposta deveria limitar-se a reiterar que a classificação/frequência foi obtida sob as premissas de F3 e que a efetividade foi definida sob os pressupostos de F4, sem extrapolar para 'risco real' fora dessas premissas.
- **o3-petrobras:medium:** aprova
- **gpt-5-4-petrobras:medium:** aprova
- **gpt-5-petrobras:medium:** aprova

### d87b10b437-b1-A1 · dificil_A · Estudos de Segurança

**P:** Um FPSO se aproxima de late life e a equipe de integridade identificou indícios de fadiga e corrosão no casco e no topside, com possível efeito sobre a vida remanescente. Em paralelo, houve modificações na unidade registradas no gerenciamento de mudanças. Para decidir se a revisão do safety case deve ser acionada, quais verificações técnicas e estudos adicionais devem ser avaliados, e como essa decisão deve ser formalizada no sistema de gestão?

**R:** A decisão deve verificar se as bases técnicas do safety case ainda representam a unidade real. Isso inclui confirmar o efeito do envelhecimento e da integridade em late life sobre casco, topside, barreiras e risco residual, porque fadiga e corrosão podem alterar premissas antes aceitas e são exemplo de condição que exige revisão. Também é necessário checar se as modificações registradas pelo gerenciamento de mudanças têm impacto relevante e se as premissas dos estudos de risco continuam válidas. A revisão não deve ficar restrita ao documento principal: quando aplicável, deve acionar estudos adicionais, como HAZID e HAZOP, e incluir estudos complementares cujas premissas sustentam detectabilidade, severidade e proteção, evitando escopo incompleto. No sistema de gestão, a alteração deve ser identificada, registrada, comunicada e vinculada à Safety Case Review, com evidência da avaliação das premissas, da implementação das recomendações e do alinhamento com o programa de integridade de ativos para manter o risco em ALARP.

- **gpt-5-2-petrobras:medium:** reprova (correcao_tecnica, suporte) · Cita HAZID como estudo adicional a acionar, mas não há fato F# que sustente HAZID (apenas menção genérica a ‘further studies’ em F8 e HAZOP em F16).; Introduz ‘barreiras’ como item explícito de verificação sem suporte literal em F# (pode ser removido ou reescrito para ‘premissas/condições da instalação’).; A resposta mistura elementos bem suportados (late life, MoC, escopo de estudos complementares, formalização no SG) com itens não suportados; precisa ajuste para ficar 100% rastreável aos F# sem adicionar conteúdo novo.
- **o3-petrobras:medium:** aprova
- **gpt-5-4-petrobras:medium:** reprova (suporte) · A resposta cita HAZID como estudo adicional sem fato numerado correspondente.; A resposta acrescenta verificação explícita de barreiras sem F# de suporte entre os fatos citados.; Como há afirmações substantivas sem suporte completo, a questão deve ser reprovada mesmo sendo tecnicamente plausível no restante.
- **gpt-5-petrobras:medium:** aprova

### d87b10b437-b2-A1 · dificil_B · Estudos de Segurança

**P:** Na atualização dos estudos de uma unidade offshore, a equipe decide manter apenas HAZID e What-if antigos para afirmar que os cenários de incêndio e explosão já estão cobertos. A decisão pendente é selecionar medidas adicionais de redução de risco para possíveis liberações inflamáveis em área congestionada. Qual encaminhamento metodológico é o mais consistente para evitar distorção na seleção dos cenários, e por quê?

**R:** Não basta aceitar os estudos qualitativos anteriores como base única. O encaminhamento consistente é rejustificar a metodologia e consolidar os cenários de liberação inflamável em hipóteses acidentais estruturadas, com árvore de eventos, cobrindo liberação, dispersão, ignição e consequências, e então adotar aprofundamento semiquantitativo ou quantitativo se a decisão exigir comparar frequência, consequências e alternativas de redução de risco. HAZID e What-if são úteis para identificar perigos, mas a escolha da técnica deve ser explicada conforme o tipo de perigo e a profundidade necessária à decisão. Em liberações inflamáveis, o desfecho depende de variáveis como tipo de vazamento, tempo de ignição, confinamento e dispersão do gás; sem isso, a seleção dos cenários de incêndio e explosão pode ficar incompleta ou pouco plausível. Para decisões mais completas sobre comportamento do incêndio e redução de risco, a abordagem quantitativa tende a ser a mais adequada.

- **gpt-5-2-petrobras:medium:** reprova (suporte) · Falta suporte explícito para a parte "comparar alternativas" como critério para exigir aprofundamento semiquantitativo/quantitativo (os fatos citados sustentam frequência+consequência e explicitação metodológica, mas não a comparação de alternativas de mitigação de forma geral).; A resposta mistura critérios de seleção metodológica (explicar e aprofundar) com finalidade de comparação de alternativas sem ancorar essa finalidade em fato aplicável ao contexto (fora do caso específico de AQRPQ).
- **o3-petrobras:medium:** reprova ()
- **gpt-5-4-petrobras:medium:** aprova
- **gpt-5-petrobras:medium:** aprova

### fadd3bccc0-b0-A2 · media · Operações simultâneas – SIMOPS

**P:** Em um projeto offshore com trabalho de contratada executado simultaneamente à produção, a troca de turno ocorre junto com substituição parcial da crew. Como essas mudanças podem degradar a coordenação de SIMOPS e por que a comunicação entre a supervisão do operador e a da contratada deve ser mantida durante todo o projeto?

**R:** Mudanças de turno e de crew são pontos típicos de perda de continuidade da informação. Nelas, detalhes sobre quais atividades coexistem, onde há interação entre frentes e quem responde por cada interface podem se distorcer ou deixar de ser repassados, reduzindo a capacidade de perceber conflitos a tempo. Por isso, a comunicação entre a supervisão do operador e a da contratada deve permanecer clara e contínua ao longo de todo o projeto, e não só no início, para preservar o mesmo entendimento operacional apesar das trocas de pessoas. Em atividades cobertas por Permit, essa continuidade também deve aparecer em rotinas formais como discussão do trabalho, reunião de Permit e passagem de turno, nas quais os Permits e suas interações são revisitados para manter a coordenação entre as frentes.

- **gpt-5-2-petrobras:medium:** reprova (suporte) · Falta de suporte explícito para 'quem responde por cada interface' (responsabilidades/interfaces) a partir de F1/F4/F7.; Falta de suporte explícito para 'reduzindo a capacidade de perceber conflitos a tempo' (consequência formulada como conflito), que não está textual nos fatos citados.; Trecho sobre 'Permits e suas interações são revisitados' mistura F7 (discutir Permits) com F1 (awareness de interações) de forma inferida; pode ser reescrito para ficar estritamente aderente aos fatos.
- **o3-petrobras:medium:** aprova
- **gpt-5-4-petrobras:medium:** aprova
- **gpt-5-petrobras:medium:** aprova

### fadd3bccc0-b1-A1 · dificil_A · Operações simultâneas – SIMOPS

**P:** Durante SIMOPS, uma unidade entra em condição anormal dinâmica por dois caminhos possíveis. No primeiro, o posicionamento dinâmico passa a operar com carga crescente nos propulsores, desvio de rumo e deriva sob piora ambiental. No segundo, ocorre falha de energia principal. Comparando os dois casos, quais funções essenciais devem ser preservadas primeiro em cada um para conduzir a unidade a um estado seguro, e qual decisão operacional tende a prevalecer em cada cenário?

**R:** Se a condição predominante for perda de posicionamento, a função essencial a preservar primeiro é a capacidade de evitar interação danosa com a infraestrutura submarina. Carga crescente nos propulsores, desvio de rumo e deriva sob agravamento ambiental caracterizam degradação da capacidade de manter posição; quando o DP já não sustenta rumo e posição, a decisão que tende a prevalecer é a desconexão de emergência para evitar danos potenciais à infraestrutura submarina. Se a condição predominante for falha de energia principal, a função essencial a preservar primeiro é a estabilidade da unidade por meio da operabilidade do lastro. Nesse caso, a transição segura depende de conseguir levar o vaso a trim seguro e nivelado, mantendo uma ou mais bombas de lastro e o sistema completo de lastro operáveis a partir do quadro de emergência alimentado pelo gerador de emergência. Portanto, no primeiro caso prevalece desconectar; no segundo, preservar lastro e estabilidade.

- **gpt-5-2-petrobras:medium:** aprova
- **o3-petrobras:medium:** aprova
- **gpt-5-4-petrobras:medium:** reprova (autonomia, sem_generalizacao) · No ramo de perda de posicionamento, falta no enunciado a condição 'atividade com potencial de interação com infraestrutura submarina', necessária para sustentar especificamente a decisão por EDS.; A resposta extrapola um caso particular para formulação quase geral; deve condicionar a desconexão ao cenário em que manter posição já não é possível e há risco de interação danosa com a infraestrutura.; Pode ser corrigida com o mesmo material, ajustando pergunta e resposta para explicitar o contexto do primeiro cenário.
- **gpt-5-petrobras:medium:** aprova

### fadd3bccc0-b2-A1 · dificil_B · Operações simultâneas – SIMOPS

**P:** Duas frentes em SIMOPS foram liberadas como compatíveis pela matriz vigente. Durante a execução, ocorre detecção de gás na pumps room, com atuação automática que muda a ventilação e passa a aquecer painéis do e-house. Ao mesmo tempo, descobre-se que, para viabilizar outra frente, um maintenance bypass foi aplicado a um transmissor que concentra PSH e PSL. A coordenação deve manter, restringir ou interromper as frentes? Justifique pela compatibilidade real das barreiras.

**R:** Deve interromper ou, no mínimo, suspender imediatamente as frentes até reavaliar o arranjo real de barreiras. A premissa de compatibilidade deixou de valer porque ela depende do estado efetivo das barreiras, não da matriz nominal: uma operação pode afetar várias barreiras, e a lista só sustenta SIMOPS se estiver atualizada e convergente com o campo (F1, F2). O bypass no transmissor não retirou apenas a função pretendida; desabilitou simultaneamente PSH e PSL, reduzindo disponibilidade e independência das proteções por uma única ação (F4). Em paralelo, o alarme de gás não foi mera perturbação: sua lógica automática alterou a ventilação e levou ao aquecimento de painéis, com potencial perda de produção e geração, ampliando o impacto sobre atividades acopladas (F7). Portanto, é necessário atualizar o mapeamento operação-barreira, comunicar a condição e só retomar após confirmar quais barreiras permanecem válidas e operantes (F2, F3).

- **gpt-5-2-petrobras:medium:** reprova (correcao_tecnica, suporte, jurisdicao, sem_generalizacao) · Decisão prescritiva (interromper/suspender imediatamente) sem suporte explícito nos fatos; pode ser reescrita como necessidade de reavaliar compatibilidade/arranjo de barreiras antes de manter SIMOPS, usando F2+F4+F7.; Atribuição de perda de 'independência' não está suportada por F4 (nem por outro fato citado); remover ou apoiar com fato apropriado (não disponível aqui).; Uso de F3 (BSEE/US e condicionado a TE) como base para obrigação geral de comunicação/atualização; ajustar para não transpor requisito estrangeiro e/ou fundamentar só em F2 (atualização periódica) e no raciocínio de convergência com campo.
- **o3-petrobras:medium:** reprova ()
- **gpt-5-4-petrobras:medium:** reprova (suporte) · Falta de suporte integral para a prescrição 'interromper/suspender imediatamente'; os fatos sustentam reavaliação e aumento de risco, mas não essa obrigação de forma explícita.; A referência à perda de 'independência' está subfundamentada: F4 comprova perda simultânea de funções, porém não explicita independência como atributo afetado.; 'Só retomar após confirmar quais barreiras permanecem válidas e operantes' é recomendação plausível, mas excede o suporte factual literal apresentado.
- **gpt-5-petrobras:medium:** aprova

### 202d9e591b-b0-A2 · media · Segurança e Controle de Riscos

**P:** Em uma instalação elétrica localizada em área classificada, como dispositivos de alarme e seccionamento automático reduzem o risco de ignição quando surgem sobretensão, sobrecorrente, falha de isolamento ou aquecimento anormal?

**R:** Esses dispositivos reduzem o risco ao identificar condições elétricas anormais antes que elas evoluam para uma fonte de ignição e, então, sinalizar a anomalia e interromper automaticamente a energia do circuito afetado. Com isso, diminuem a probabilidade de formação de arcos, faíscas ou superfícies aquecidas capazes de inflamar gases ou vapores presentes na área classificada. Sua função é atuar como barreira complementar contra anormalidades como sobretensão, sobrecorrente, falha de isolamento e aquecimento excessivo, limitando a progressão da falha para um evento de incêndio ou explosão.

- **gpt-5-2-petrobras:medium:** reprova (suporte) · Falta suporte explícito para o elo 'sobretensão/sobrecorrente/falha de isolamento/aquecimento anormal' -> 'formação de arcos e faíscas' na forma como foi afirmado (os fatos suportam prevenção de condições anormais e reconhecem arcos/faíscas/superfícies aquecidas como fontes, mas não conectam diretamente as anomalias citadas à redução específica de arcos/faíscas).; Para ficar 100% suportada, a resposta deve restringir-se ao que F8 afirma (prevenir condições anormais por alarme e seccionamento) e ao que F2/F3 afirmam (fontes de ignição), evitando causalidade não citada sobre arcos/faíscas.
- **o3-petrobras:medium:** aprova
- **gpt-5-4-petrobras:medium:** aprova
- **gpt-5-petrobras:medium:** aprova

### 202d9e591b-b1-A1 · dificil_A · Segurança e Controle de Riscos

**P:** Em uma atividade de manutenção repetitiva em unidade offshore, ocorreu um quase acidente na recolocação em serviço após isolamento. A investigação mostrou um desvio na execução, mas também encontrou auditorias com não conformidades recorrentes no isolamento, ausência de sistema para revisar válvulas travadas abertas ou fechadas, supervisão fraca e avaliação de riscos/método de trabalho alterados apenas depois de questionamento. Quais ações corretivas e preventivas são mais coerentes com esse diagnóstico?

**R:** As ações devem atacar a cadeia causal completa, não apenas o erro de execução. É tecnicamente mais coerente restaurar a eficácia das barreiras de isolamento, implantando controle e revisão sistemática das válvulas travadas abertas ou fechadas e corrigindo as fragilidades práticas do arranjo de isolamento evidenciadas por auditorias e recorrência. Em paralelo, a organização deve revisar a avaliação de riscos e o método de trabalho, porque a mudança só após questionamento indica falha prévia nessas etapas. Também é necessário fortalecer como o trabalho é controlado e supervisionado, com monitoramento de conformidade mais eficaz, revisão dos controles procedimentais e das deficiências de gestão que permitiram a permanência do problema. Medidas apenas disciplinares, de requalificação isolada ou de produção documental são insuficientes, porque não removem as falhas de barreira, supervisão e gestão que sustentam a repetição do evento.

- **gpt-5-2-petrobras:medium:** reprova (suporte) · Falta de suporte: a resposta afirma que medidas disciplinares/produção documental (e ‘requalificação isolada’) são insuficientes, mas isso não está sustentado pelos fatos citados (F3, F7, F11, F12, F13).
- **o3-petrobras:medium:** aprova
- **gpt-5-4-petrobras:medium:** aprova
- **gpt-5-petrobras:medium:** aprova

### 202d9e591b-b2-A1 · dificil_B · Segurança e Controle de Riscos

**P:** Após manutenção, uma unidade entra em retorno ao serviço. Durante a tarefa liberada por PT, a equipe identifica no campo um perigo relevante de liberação de substância perigosa que não constava da análise usada para autorizar o trabalho. A supervisão deve tratar isso como falha pontual de execução ou como evidência de lacuna no processo de gestão de riscos? Qual decisão técnica é mais adequada?

**R:** Deve tratar como evidência de lacuna sistêmica de identificação e reavaliação de perigos, não apenas como falha local da equipe. Quando um perigo relevante só é reconhecido durante a execução, isso indica que a análise não representou a condição operacional real; esse sinal já foi observado em desconexão com H2S aprisionado não previsto no HAZID. Retorno ao serviço após manutenção é condição diferente da rotina, com perigos próprios, e pode exigir gestão de mudanças, procedimento específico de partida/retorno, atualização das informações de pré-operação e controles efetivos de PTW e isolamento. Como o processo estava em transiente, a análise deveria cobrir essa etapa e seus limites operacionais. Se a tarefa ou procedimento for crítico para a segurança, a revisão deve incluir HRA. Se a metodologia permitiu essa omissão, o procedimento de gestão de riscos deve ser revisto com ferramenta reconhecida e rastreabilidade documental.

- **gpt-5-2-petrobras:medium:** reprova (suporte, sem_generalizacao) · Suporte insuficiente para exigir revisão do procedimento de gestão de riscos com ferramentas reconhecidas e rastreabilidade documental no contexto de retorno ao serviço após manutenção: F3 é específico de planejamento e construção de poços.; Generalização indevida (sem_generalizacao): transforma uma determinação contextual (F3) em regra/decisão geral para qualquer atividade.; Trecho 'procedimento específico de partida/retorno' carece de amarração direta no material para 'retorno ao serviço após manutenção'; F5 fala em partida/desativação e atualização de pré-operação, mas a equivalência com retorno ao serviço pós-manutenção precisaria ser explicitada/qualificada na redação.
- **o3-petrobras:medium:** aprova
- **gpt-5-4-petrobras:medium:** reprova (suporte, sem_generalizacao) · Suporte parcial na prescrição de revisão metodológica: F3 é específico para planejamento e construção de poços.; Generalização indevida de requisito contextualizado em F3 para cenário amplo de retorno ao serviço após manutenção.
- **gpt-5-petrobras:medium:** aprova

### d99fb5d8d3-b0-A1 · facil · SGSO

**P:** Quais elementos mínimos o Plano de Emergência da instalação deve contemplar para estruturar a resposta a cenários acidentais?

**R:** Deve contemplar, no mínimo: identificação da instalação e do responsável legal; descrição dos acessos; cenários acidentais previstos; sistemas de alerta; comunicação do acidente; estrutura organizacional de resposta; procedimentos de resposta; equipamentos e materiais de resposta; e procedimento para acionamento de recursos e estruturas complementares, quando aplicável. Para cenários com materiais perigosos, o planejamento deve incluir ações específicas para isolamento e controle de vazamentos, porque essa definição é parte relevante da capacidade de resposta.

- **gpt-5-2-petrobras:medium:** reprova (suporte) · Suporte insuficiente para a justificativa ‘porque essa definição é parte relevante da capacidade de resposta’ (não está explicitamente ancorada em F8/F9 ou no texto da nota). Basta remover a justificativa ou reescrever ancorando no que o material diz (ex.: que é item frequentemente esquecido/deficiência recorrente).
- **o3-petrobras:medium:** aprova
- **gpt-5-4-petrobras:medium:** reprova (correcao_tecnica, suporte, jurisdicao) · A resposta adiciona conteúdo além da lista mínima pedida em F8.; O acréscimo sobre materiais perigosos é tratado com tom de obrigatoriedade sem suporte jurisdicional específico.; A justificativa 'parte relevante da capacidade de resposta' não está sustentada pelos fatos citados.
- **gpt-5-petrobras:medium:** reprova (suporte) · Afirmação não suportada: 'essa definição é parte relevante da capacidade de resposta' não está respaldada pelos Fatos citados.; A resposta inclui recomendação sobre materiais perigosos que não faz parte do rol mínimo de F8, o que pode extrapolar o escopo do 'mínimo' exigido.

### d99fb5d8d3-b1-A1 · dificil_A · SGSO

**P:** Em um FPSO, auditorias sucessivas voltam a registrar desvios ligados a salvaguardas classificadas como críticas. As correções locais foram encerradas a cada ciclo, mas os mesmos tipos de problema reaparecem em áreas diferentes e a gerência não consegue demonstrar, por indicadores, visão estável da disponibilidade e integridade dessas barreiras. Por que esse quadro sugere falha sistêmica na identificação ou no tratamento dos Elementos Críticos de Segurança Operacional, e não apenas falhas isoladas de execução?

**R:** Porque a recorrência, após ações corretivas anteriores, indica que o tratamento não foi suficientemente abrangente para eliminar a causa de gestão, apenas manifestações locais do desvio. Quando isso ocorre no universo de salvaguardas críticas, o problema deixa de ser pontual e passa a sugerir inconsistência estrutural em como o sistema identifica quais elementos realmente são barreiras críticas e como os gerencia. No SGSO, são críticos não só equipamentos, mas também sistemas e procedimentos cuja função é prevenir ou mitigar acidentes, ou cuja falha pode provocá-los; se a identificação for incompleta ou inconsistente, parte dessas barreiras fica fora do controle gerencial. Além disso, a disponibilidade e a integridade devem ser monitoradas continuamente em nível gerencial, com apoio de indicadores por unidade offshore. Se a gerência não consegue evidenciar essa visão e os desvios se repetem, há forte sinal de falha sistêmica; em recorrência no gerenciamento dos elementos críticos, pode ser requerida verificação de barreiras por terceira parte.

- **gpt-5-2-petrobras:medium:** reprova (suporte) · Suporte parcial: a resposta inclui pelo menos uma consequência/alegação relevante (“parte das barreiras fica fora do controle gerencial”) não explicitada nos fatos citados; o requisito exige suporte explícito para cada afirmação substantiva.
- **o3-petrobras:medium:** aprova
- **gpt-5-4-petrobras:medium:** aprova
- **gpt-5-petrobras:medium:** aprova

### d99fb5d8d3-b2-A1 · dificil_B · SGSO

**P:** Após reorganização de equipes com acúmulo temporário de funções e entrada de novos operadores, os procedimentos críticos permanecem atualizados e acessíveis no sistema documental. Em campo, porém, ocupantes do mesmo cargo executam a mesma rotina com interpretações diferentes e dúvidas sobre etapas críticas; há registros de treinamentos passados, mas não de tutoria prévia nem de revisão da mudança com operação e manutenção. Qual é o diagnóstico técnico prioritário e a ação de gestão mais consistente?

**R:** O problema prioritário é barreira humana degradada por mudança de pessoas não absorvida, e não falha principal de controle documental. Mesmo com procedimento vigente e acessível, sua efetividade depende de capacitação por função, treinamento contínuo e verificação da execução com qualidade; sem isso, o procedimento perde autoridade operacional na prática. Como houve acúmulo de funções e entrada de pessoal, a situação deveria ter passado pelo gerenciamento de mudanças de pessoas, com tratamento formal dessas alterações, capacitação teórica e prática, reciclagem e tutoria antes da efetivação. A heterogeneidade de execução indica que a equipe não converteu a mudança em entendimento uniforme do procedimento. A ação mais consistente é reabrir a mudança como mudança de pessoas, revisar suas implicações com operação e manutenção, aplicar tutoria e treinamento específico por função e restabelecer a verificação da qualidade da execução no campo.

- **gpt-5-2-petrobras:medium:** reprova (correcao_tecnica, suporte) · Falta de suporte: duas conclusões centrais (“perde autoridade operacional”, “heterogeneidade indica...”) não são sustentadas pelos F# citados; isso reprova pelo critério de suporte parcial.; A resposta poderia estar correta em espírito, mas excede o que os fatos fornecidos comprovam explicitamente, introduzindo relações efeito/conclusão sem base factual apresentada.
- **o3-petrobras:medium:** aprova
- **gpt-5-4-petrobras:medium:** aprova
- **gpt-5-petrobras:medium:** aprova

### d720962e6f-b1-A1 · dificil_A · Sistema de Combate a Incêndio

**P:** Em um FPSO, uma bomba principal de água de incêndio falhou no teste de desempenho e não atingiu os requisitos de vazão/pressão definidos. O equipamento é crítico para a resposta a incêndio e a unidade pretende mantê-lo nessa condição até a próxima parada, sem contingência formalmente aprovada. No SGSO, quais decisões de controle são indispensáveis nessa situação?

**R:** O primeiro controle é tratar o resultado do teste como desvio conclusivo de desempenho, não como pendência genérica: como houve não atendimento aos requisitos, deve ser emitida ordem de manutenção corretiva, priorizada pela gravidade do desvio e pela criticidade da bomba para a função de combate a incêndio. Além disso, o operador deve avaliar formalmente o resultado do teste para decidir sobre a aptidão do elemento e o risco associado à sua permanência degradada. Como se trata de elemento crítico degradado, a unidade não deve permanecer apenas com a falha aberta; é necessário acionar procedimento de contingência com aprovação e controle, incluindo medidas temporárias equivalentes quando aplicável. Se a bomba permanecer degradada sem contingência aprovada, o problema deixa de ser apenas técnico e passa a caracterizar falha no controle do risco residual, porque a capacidade de resposta a incêndio fica comprometida.

- **gpt-5-2-petrobras:medium:** reprova (suporte) · Falta de suporte: a resposta introduz 'priorização pela criticidade' (não explicitada em F9) e a expressão/conclusão 'falha no controle do risco residual' (não consta nos fatos citados), violando a exigência de que cada afirmação substantiva esteja sustentada.; Para ficar plenamente suportada, a resposta precisaria limitar-se ao que os fatos afirmam (priorização conforme desvio e elemento degradado; necessidade de contingência com aprovação/controle; comprometimento da resposta sem contingência), sem acrescentar critérios/qualificações não citados.
- **o3-petrobras:medium:** aprova
- **gpt-5-4-petrobras:medium:** aprova
- **gpt-5-petrobras:medium:** aprova

### 86765f00dc-b0-A2 · media · Sistema de Fogo e Gás (F&G)

**P:** Em uma SIF, o proof test parcial confirmou atuação do instrumento, mas há preocupação com alteração de campo e envelhecimento físico do arranjo instalado. Quais verificações de inspeção devem acompanhar esse teste para tratar esse risco?

**R:** Devem acompanhar o teste inspeções que confirmem que o equipamento instalado não foi modificado e não se deteriorou a ponto de deixar de atender ao SRS. Isso inclui identificar claramente os itens a inspecionar e verificar não só os instrumentos, mas também equipamentos associados, como tubing de instrumentação, caixas de junção e trace heating. A inspeção deve checar sinais de modificação não autorizada, por exemplo conferência de números de série, e evidências de deterioração física, como falta de parafusos, tampas ausentes, suportes com corrosão e danos em cabos. Essas verificações são normalmente incorporadas ao proof test ou partial proof test para evitar que uma função pareça disponível no teste, mas esteja fisicamente degradada ou alterada em campo.

- **gpt-5-2-petrobras:medium:** reprova (sem_generalizacao) · Generalização: a resposta deveria qualificar que se trata de requisito/expectativa do contexto BS EN 61511/HSE (UK) ou enquadrar explicitamente como boa prática técnica, evitando prescrição universal sem base jurisdicional local.
- **o3-petrobras:medium:** aprova
- **gpt-5-4-petrobras:medium:** aprova
- **gpt-5-petrobras:medium:** aprova

### bfc6625c3d-b0-A1 · facil · Sistemas e equipamentos de salvatagem

**P:** O que significa estruturar a resposta a emergências com pontos de encontro distribuídos por função e localização em uma unidade offshore?

**R:** Significa que a reunião inicial do pessoal não é tratada como um único ponto genérico para todos. A estrutura de emergência define previamente funções e respectivos pontos de encontro em diferentes locais da unidade, como CCR (Centro de Controle e Rádio), enfermaria, sala de controle da praça de máquinas, bote de resgate rápido, locais com equipamentos de brigada e o refúgio temporário. Na prática, isso organiza a apresentação das pessoas conforme seu papel e o local previsto para sua atuação ou suporte na resposta.

- **gpt-5-2-petrobras:medium:** reprova (correcao_tecnica, suporte) · Expansão incorreta/inconsistente de CCR (F1 traz ‘Central Control Room’).; Efeito prático (‘organiza a apresentação...’) não está suportado pelo fato citado (apenas por interpretação). Para passar no critério de suporte estrito, reescrever para ficar aderente ao que F1 afirma, ou citar explicitamente um trecho da nota que estabeleça esse efeito.
- **o3-petrobras:medium:** aprova
- **gpt-5-4-petrobras:medium:** reprova (correcao_tecnica, suporte) · Expansão técnica incorreta da sigla CCR: o fato cita 'Central Control Room', não 'Centro de Controle e Rádio'.; Há falta de suporte para a expansão dada à sigla CCR, o que reprova o critério de suporte.
- **gpt-5-petrobras:medium:** reprova (correcao_tecnica, suporte) · Expansão/definição incorreta de CCR ('Centro de Controle e Rádio') em desacordo com F1 ('Central Control Room').; Suporte insuficiente devido à presença de uma afirmação incorreta e não suportada.

### bfc6625c3d-b0-A2 · media · Sistemas e equipamentos de salvatagem

**P:** Em uma unidade offshore, os locais de apresentação do pessoal já estão definidos por função em diferentes pontos da instalação. Como essa definição prévia influencia a organização inicial da resposta, a concentração de equipes e a contabilização de pessoal?

**R:** Ela tende a tornar a resposta inicial mais organizada, porque cada função se apresenta no local previamente previsto para seu grupo, em vez de convergir para um único ponto genérico. Como os pontos de encontro são distribuídos por função e localização na unidade, a concentração de equipes em um só local é reduzida e a alocação inicial do pessoal fica mais estruturada. Além disso, quando existe um local esperado para cada função, a conferência de presença e a identificação de ausências ou desvios ficam mais objetivas na fase inicial da emergência.

- **gpt-5-2-petrobras:medium:** reprova (suporte) · Falta de suporte factual (F#) para os efeitos alegados (organização, evitar convergência e melhoria na contabilização); com os fatos disponíveis (F1 e F2), não é possível sustentar essas relações sem introduzir conteúdo novo.
- **o3-petrobras:medium:** aprova
- **gpt-5-4-petrobras:medium:** reprova (suporte) · Falta de suporte factual suficiente: F1 comprova apenas a existência de pontos de encontro por função em múltiplos locais.; As relações de causa e efeito sobre organização inicial, redução de concentração e contabilização de pessoal não estão sustentadas pelos fatos citados.
- **gpt-5-petrobras:medium:** reprova (suporte) · Afirmações de efeito (organização, redução de concentração, contabilização) sem suporte explícito nos Fatos fornecidos.; Suporte parcial aos argumentos: apenas a existência de pontos distribuídos por função está em F1; os benefícios inferidos não estão ancorados em F# específicos.

### bfc6625c3d-b1-A1 · dificil_A · Sistemas e equipamentos de salvatagem

**P:** Em um abandono, a tripulação consegue chegar a uma estação de life raft throw-over por uma rota física existente. Porém, no ponto de lançamento há exposição relevante a radiação térmica e fumaça, e o único modo prático de alcançar a balsa já implantada é descer por corda com nós e nadar alguns metros até a painter line. A balsa está disponível e pode ser lançada. Esse arranjo torna o abandono realmente viável?

**R:** Não. A cadeia acesso–descida–alcance da balsa–embarque não é executável com segurança apenas porque existe rota física e a balsa está a bordo. Neste cenário, o arranjo falha em dois pontos críticos. Primeiro, a entrada física no mar aparece como etapa necessária para conectar-se à balsa, quando deveria ser último recurso. Além disso, corda com nós não é meio controlado de descida, porque depende de força e destreza sob emergência. Segundo, o ponto de lançamento/embarque e, quando necessário, a rota de acesso precisam permanecer disponíveis sob os efeitos do cenário, com proteção suficiente contra radiação térmica e fumaça; se o ponto relevante está exposto, a disponibilidade operacional da estação fica comprometida. Portanto, a presença da balsa não basta: sem descida controlada, acesso funcional à painter line e proteção adequada da rota e do ponto de embarque, o abandono não é considerado viável.

- **gpt-5-2-petrobras:medium:** reprova (correcao_tecnica, suporte) · Falta de suporte (e potencial erro técnico, conforme os fatos) ao exigir proteção contra fumaça especificamente para o ponto de lançamento/embarque; os fatos exigem proteção do ponto contra radiação térmica (F3) e tratam fumaça apenas para rotas de acesso (F4).; A resposta pode ser corrigida restringindo a fumaça às rotas (F4) e mantendo o ponto com foco em radiação térmica (F3), sem mudar o restante do raciocínio.
- **o3-petrobras:medium:** aprova
- **gpt-5-4-petrobras:medium:** reprova (correcao_tecnica, suporte, sem_generalizacao) · Estende sem suporte a exigência de proteção contra fumaça das rotas de acesso aos pontos de lançamento/embarque.; Há falta de suporte em parte substantiva da justificativa; pelo critério definido, isso reprova a questão.
- **gpt-5-petrobras:medium:** aprova

### bfc6625c3d-b2-A1 · dificil_B · Sistemas e equipamentos de salvatagem

**P:** Em um FPSO, uma estação de abandono fica indisponível após falha mecânica. O plano passa a concentrar o pessoal no Temporary Refuge (TR) até usar rotas remanescentes para outro ponto de embarque com baleeira throw-over. Ao mesmo tempo, há tendência de piora no desempenho da detecção de gás ligada ao TR, e a rota alternativa pode ficar exposta a fumaça e radiação térmica. Qual decisão técnica deve ser priorizada para julgar a aceitabilidade de continuar operando nessa condição degradada?

**R:** A prioridade é verificar a cadeia remanescente completa de proteção e abandono, não apenas a existência nominal de outro meio final. A condição só é tecnicamente aceitável se ainda houver rotas seguras até o escape-to-sea, mantidas e disponíveis, e se essas rotas e o ponto de embarque permanecerem utilizáveis pelo tempo requerido, com proteção contra fumaça e radiação térmica e iluminação de emergência no ponto de baleeira throw-over. Como a perda de um meio de abandono aumenta a dependência do TR, também é preciso confirmar que ele continua apto a receber muster, avaliar a emergência e sustentar habitabilidade, com limites internos definidos para atmosfera e gestão preventiva dos sistemas associados. Se a tendência de desempenho da detecção de gás e do shutdown indica aproximação de não conformidade, não se deve aceitar controle por “corrigir quando falhar”. Em cenários com potencial de explosão, a proteção do TR contra sobrepressão também é condição crítica.

- **gpt-5-2-petrobras:medium:** reprova (correcao_tecnica, suporte, jurisdicao, sem_generalizacao) · Afirmação sem suporte nos F# citados: 'perda de um meio de abandono aumenta a dependência do TR' (não está em F1–F9; só aparece no texto narrativo das notas, sem F#).; Problema de jurisdição/obrigatoriedade: linguagem prescritiva e uso de SFAIRP/dutyholder/HSE como se fosse critério universal para FPSO, sem qualificar que são expectativas UK (F1, F2, F3, F5, F6, F9).; Generalização: conclui aceitabilidade operacional global ('só é tecnicamente aceitável se...') a partir de guidance específico; precisa enquadrar como boa prática/critério da fonte ou restringir a jurisdição/escopo.
- **o3-petrobras:medium:** aprova
- **gpt-5-4-petrobras:medium:** reprova (suporte) · Falta suporte direto em F# para a afirmação causal de que a perda de um meio de abandono aumenta a dependência do TR.; A abertura da resposta usa uma síntese plausível ('cadeia remanescente completa' versus 'existência nominal'), mas sem F# textual suficientemente direto para sustentar integralmente essa formulação.; Como suporte parcial reprova, a questão não deve ser aprovada na forma atual, apesar de estar tecnicamente bem orientada.
- **gpt-5-petrobras:medium:** reprova (suporte) · Inclui proteção contra fumaça no ponto de embarque sem apoio explícito em F# (F9 trata de radiação térmica e iluminação, não de fumaça no ponto de embarque).; Afirma que a perda de um meio aumenta a dependência do TR sem um F# que estabeleça explicitamente essa relação; embora coerente e indicado no cenário e nas notas descritivas, falta citação factual numerada.

### 470390a408-b0-A2 · media · Geração e distribuição de energia elétrica

**P:** Em uma unidade offshore com variação relevante de demanda, por que a aquisição contínua de tensões, correntes e fator de potência é importante para decidir a conexão de outro gerador ao barramento e a partilha de carga?

**R:** Porque essas variáveis mostram, em tempo real, a condição elétrica do barramento e a evolução da carga. Ao integrar esses dados com sinais de proteção, controle de motores e acionamentos, o sistema ganha visibilidade suficiente para reconhecer aumento de demanda, aproximação de sobrecarga ou comportamento anormal de grandes consumidores. Com base nisso, o PMS pode antecipar a partida e a conexão de outro gerador ao barramento sob supervisão de frequência e sincronismo e, depois, redistribuir a carga entre as máquinas em operação. Essa lógica ajuda a manter a estabilidade e reduzir a probabilidade de atuação das proteções por sobrecarga, especialmente quando diferentes modos operacionais provocam mudanças significativas de demanda.

- **gpt-5-2-petrobras:medium:** aprova
- **o3-petrobras:medium:** aprova
- **gpt-5-4-petrobras:medium:** reprova (suporte) · Falta de suporte para a afirmação de que a lógica descrita reduz a probabilidade de atuação das proteções por sobrecarga.; O restante da resposta está alinhado ao material, mas a exigência é suporte integral de cada afirmação substantiva.
- **gpt-5-petrobras:medium:** aprova

### 470390a408-b1-A1 · dificil_A · Geração e distribuição de energia elétrica

**P:** Uma FPSO possui vários geradores e a partida de um deles vinha sendo feita por bloco de partida axial. Esse arranjo apresenta falhas operacionais recorrentes, com impacto na disponibilidade da unidade, e a equipe avalia migrar para um Conversor Estático de Frequência (SFC) com sequência de partida automática integrada ao controle dos geradores. Tecnicamente, por que essa substituição é justificável?

**R:** A substituição é justificável porque o problema deixou de ser apenas “conseguir partir” a máquina e passou a ser garantir partida confiável. O bloco de partida axial atendia funcionalmente tanto à partida apenas do gerador, inclusive para operação como compensador síncrono, quanto à partida da unidade completa para geração de potência ativa. Porém, como esse arranjo apresentava problemas operacionais frequentes, ele comprometia a confiabilidade das unidades. Nessa condição, trocar o bloco por um SFC é coerente com o objetivo de reduzir a recorrência das falhas no processo de partida e tornar a colocação da unidade em serviço mais confiável. Além disso, o SFC tornou o processo de partida totalmente automatizado, e o sistema já dispõe de uma unidade de controle automática para comandar a partida de todos os geradores. Assim, a solução melhora simultaneamente a confiabilidade da partida e sua coordenação automática no conjunto gerador.

- **gpt-5-2-petrobras:medium:** reprova (suporte) · Falta de suporte explícito para benefícios afirmados como resultado (p.ex., 'reduzir recorrência das falhas', 'tornar mais confiável', 'melhorar coordenação automática do conjunto'). Os fatos apenas registram que falhas afetavam a confiabilidade e que a substituição por SFC tornou a partida automatizada e que existe unidade automática para controlar partidas; não afirmam os ganhos adicionais como efeito.; Trecho final sugere melhoria de coordenação do conjunto por causa do SFC, mas F3 só diz que há controle automático para partidas, não que o SFC melhore essa coordenação.
- **o3-petrobras:medium:** aprova
- **gpt-5-4-petrobras:medium:** aprova
- **gpt-5-petrobras:medium:** aprova

### 470390a408-b2-A1 · dificil_B · Geração e distribuição de energia elétrica

**P:** Após perda total da geração principal, a geração de emergência está disponível e as permissivas de back feeding foram atendidas, energizando parte do painel principal. Ao mesmo tempo, um dos conjuntos de 24 Vcc que alimenta CLP e painéis de controle falhou, e o TIE ainda não foi fechado. Há tensão em parte dos barramentos, mas algumas funções de controle seguem indisponíveis. Qual diagnóstico técnico explica esse quadro e qual reconfiguração deve ser priorizada para restabelecer as cargas prioritárias afetadas?

**R:** O quadro é compatível com duas camadas de alimentação diferentes: o back feeding recompõe apenas parte da distribuição em CA ligada ao painel principal, mas não substitui automaticamente a alimentação auxiliar e de controle em 24 Vcc. Assim, pode haver barramentos energizados e, ainda assim, CLP e painéis de controle permanecerem sem alimentação funcional se o ramo CC remanescente não estiver assumindo os consumidores do ramo falhado. A prioridade é reconfigurar o sistema de 24 Vcc pelo fechamento do TIE para transferir esses consumidores ao conjunto remanescente, porque cada conjunto tem capacidade para atender 100% da demanda do quadro. O back feeding continua necessário para as cargas ligadas ao painel principal, mas, isoladamente, não garante a disponibilidade das funções de controle prioritárias.

- **gpt-5-2-petrobras:medium:** reprova (autonomia) · Autonomia: o enunciado não explicita que cada conjunto 24 Vcc (A/B) tem capacidade para 100% da demanda nem que a transferência é via TIE; a resposta depende desse dado do material para justificar a prioridade.
- **o3-petrobras:medium:** aprova
- **gpt-5-4-petrobras:medium:** aprova
- **gpt-5-petrobras:medium:** aprova

### 028022ae6b-b0-A1 · facil · Sistema de utilidades

**P:** Por que a confiabilidade dos dados de medição em um sistema de utilidades depende de inspeção e calibração periódica, e como isso afeta a avaliação de desempenho energético?

**R:** Porque os dados só são confiáveis para gestão e avaliação de desempenho quando os equipamentos de medição mantêm sua condição metrológica assegurada por inspeções e calibrações periódicas. Sem essa confiabilidade, o uso dos dados fica condicionado e a caracterização rigorosa do desempenho energético perde sustentação. Na prática, isso compromete a medição e verificação do consumo, enfraquece o monitoramento contínuo e reduz a capacidade de gerir, monitorar e reportar o uso de energia de forma consistente. Como consequência, a unidade passa a ter menor base técnica para avaliar o desempenho real e para sustentar ações de eficiência energética ao longo da operação.

- **gpt-5-2-petrobras:medium:** aprova
- **o3-petrobras:medium:** aprova
- **gpt-5-4-petrobras:medium:** reprova (suporte) · Há extrapolação além do suporte explícito dos fatos ao afirmar comprometimento da M&V do consumo, enfraquecimento do monitoramento contínuo e menor base para sustentar ações de eficiência energética.; A resposta pode ser corrigida com o mesmo material, restringindo-se ao que F7 e F1 sustentam de modo direto: inspeção/calibração periódica asseguram confiabilidade, e sem ela o uso dos dados para gestão e avaliação do desempenho fica condicionado.
- **gpt-5-petrobras:medium:** aprova

### 028022ae6b-b0-A2 · media · Sistema de utilidades

**P:** Uma unidade offshore quer reduzir consumo de energia e água nas utilidades, mas ainda não mapeou claramente os principais pontos de consumo, as quantidades e qualidades requeridas em cada aplicação nem os pontos de geração de efluentes. Como essa lacuna afeta a identificação de oportunidades de otimização?

**R:** Essa lacuna dificulta a identificação de oportunidades de otimização porque o conhecimento das atividades industriais é a base para reconhecer onde estão os principais consumidores, quanto recurso cada aplicação exige, qual qualidade é necessária e onde os efluentes são gerados. Sem essa visão, fica prejudicada a identificação de oportunidades de adequação do uso de energia e água em cada unidade e a escolha de uma estratégia compatível com o perfil de operação dos equipamentos. Com esse conhecimento, a otimização deixa de ser genérica e passa a focar os pontos de maior impacto no consumo, no custo e nas descargas de águas residuais industriais.

- **gpt-5-2-petrobras:medium:** reprova (suporte) · Falta de suporte literal para afirmações de que a otimização 'deixa de ser genérica' e que se passa a focar 'pontos de maior impacto'.; Cadeia causal entre ausência do mapeamento descrito e 'escolha de estratégia compatível com o perfil de operação' não está explicitamente suportada pelos fatos; precisa ser reescrita para ficar estritamente dentro do que F5/F6 afirmam.
- **o3-petrobras:medium:** aprova
- **gpt-5-4-petrobras:medium:** reprova (suporte) · Há extrapolação sem suporte explícito em 'pontos de maior impacto'.; A resposta pode ser corrigida removendo a formulação não sustentada e mantendo apenas o que F5-F6 afirmam.
- **gpt-5-petrobras:medium:** aprova

### 6fffbf5758-b0-A1 · facil · Geral

**P:** Por que a gestão do ciclo de vida de uma unidade flutuante deve começar na fase de projeto, e não apenas durante a operação ou perto do descomissionamento?

**R:** Porque decisões tomadas no projeto já permitem reduzir, com menor custo, impactos ambientais, sociais e de saúde e segurança do descomissionamento, por meio de medidas preventivas como melhor arranjo de componentes, afastamento de áreas sensíveis e provisão de garantias financeiras. Além disso, o gerenciamento de riscos precisa nascer nessa fase, com antecipação de desvios, condições inseguras e falhas de camadas de proteção, e seguir até a desativação. Quando a gestão começa cedo, inspeção e manutenção passam a ser controladas ao longo de todo o ciclo de vida, formando a base histórica necessária para decisões futuras de extensão de vida ou descomissionamento. Se isso é deixado para o fim, a unidade tende a chegar à etapa final com integridade menos conhecida e decisões mais reativas.

- **gpt-5-2-petrobras:medium:** reprova (suporte) · Falta de suporte factual para: (1) 'base histórica necessária para decisões futuras de extensão de vida ou descomissionamento' e (2) 'chegar ao fim com integridade menos conhecida e decisões mais reativas'.; A afirmação sobre controle de inspeção/manutenção 'ao longo de todo o ciclo de vida' extrapola o enunciado literal de F7 (que só exige/adota ferramentas com controle adequado), sem um F# que explicite a abrangência temporal.
- **o3-petrobras:medium:** aprova
- **gpt-5-4-petrobras:medium:** aprova
- **gpt-5-petrobras:medium:** aprova

### 6fffbf5758-b0-A2 · media · Geral

**P:** Uma unidade flutuante se aproxima do fim da vida de projeto, mas o operador dispõe de registros de condição, inspeção e manutenção acumulados ao longo dos anos. Por que a extensão de vida deve ser tratada como processo contínuo de preparação, e o que precisa sustentá-la tecnicamente?

**R:** Ela deve ser contínua porque envelhecimento não se define pela idade cronológica, mas pelo conhecimento da condição real do ativo e dos fatores que influenciaram sua degradação ao longo da operação. Por isso, preparar a extensão de vida apenas no fim da vida de projeto é inadequado. Tecnicamente, a decisão precisa ser sustentada por uma metodologia de life extension com avaliação completa da unidade para verificar se a integridade estrutural e mecânica permanece suficiente para operar com segurança além da vida de projeto. Isso não deve se basear apenas em achados dispersos de auditoria ou correções pontuais, mas em avaliações técnicas formais e estruturadas voltadas a demonstrar a adequação das barreiras de segurança. O histórico controlado de inspeção e manutenção é parte essencial dessa base técnica.

- **gpt-5-2-petrobras:medium:** reprova (suporte) · Falta de suporte: a resposta eleva “histórico controlado de inspeção e manutenção” a ‘parte essencial’ da base técnica para extensão de vida sem fato que estabeleça essa relação de essencialidade/decisão (F7 só fala em desenvolver/adotar ferramentas com controle de inspeção/manutenção).
- **o3-petrobras:medium:** aprova
- **gpt-5-4-petrobras:medium:** aprova
- **gpt-5-petrobras:medium:** aprova

### 6fffbf5758-b1-A1 · dificil_A · Geral

**P:** Após 18 dias em lay-up, um circuito de processo de um FPSO será devolvido à operação depois de intervenção. A manutenção foi encerrada, mas ainda há isolamentos temporários sob controle documental e existe dúvida se o volume interno deve ser inertizado antes da partida. Qual sequência de decisão e execução é tecnicamente mais adequada para o retorno ao serviço, e por que essa etapa deve ser tratada como gestão de mudanças, e não como simples continuação da manutenção?

**R:** A sequência adequada é conduzir o retorno ao serviço por procedimento específico da instalação, sob PTW (permissão de trabalho) e certificados de isolamento, tratando a reintrodução de fluido como etapa própria; avaliar então a necessidade de inertização; somente depois retirar os isolamentos de forma controlada e confirmar a recomposição final necessária para operar, incluindo a reinstalação do tampão cap roscado nos drenos; por fim, introduzir os fluidos. Essa lógica é necessária porque o risco relevante surge justamente quando o sistema volta a receber inventário, pressão e temperatura: a introdução de fluidos em sistema recém-mantido ou que esteve ocioso tem perigos próprios e pode ser tratada como gestão de mudanças. Assim, a decisão não pode se limitar ao encerramento da manutenção, mas deve assegurar que a configuração liberada para trabalho foi realmente recomposta para operação segura antes da partida.

- **gpt-5-2-petrobras:medium:** reprova (correcao_tecnica, suporte) · Falta de suporte para a SEQUÊNCIA detalhada solicitada (ordem de inertização/retirada de isolamentos/recomposição/introdução de fluidos).; Afirmações adicionais de mecanismo de risco (inventário/pressão/temperatura) e critério de decisão (‘não pode se limitar ao encerramento da manutenção’) não estão suportadas por F1–F2.; Possível inconsistência com F1 ao colocar reinstalação do tampão cap como passo prévio à introdução de fluidos, quando o fato diz ‘Após o retorno’ (ambiguidade temporal).
- **o3-petrobras:medium:** aprova
- **gpt-5-4-petrobras:medium:** reprova (correcao_tecnica, suporte) · A resposta determina uma ordem única entre inertização, retirada de isolamentos, recomposição e introdução de fluidos sem base explícita em F1/F2.; A reinstalação do tampão cap dos drenos é colocada antes da introdução de fluidos, mas F1 apenas a situa 'após o retorno'.; Parte da justificativa usa conteúdo não sustentado diretamente pelos fatos citados, como 'inventário, pressão e temperatura' e 'configuração liberada para trabalho recomposta para operação segura'.
- **gpt-5-petrobras:medium:** aprova

### 6fffbf5758-b2-A1 · dificil_B · Geral

**P:** Uma FPSO em fim de vida teve avaliação inicial favorável de integridade, navegabilidade e de parte dos sistemas que ainda seriam usados na desativação. A equipe propõe rebocá-la a estaleiro para reduzir exposição offshore, mas a unidade ainda não passou pela limpeza e isolamento para condição de reboque, há espécies exóticas invasoras no casco e a retirada da locação exigiria manobra próxima a instalação adjacente com risers/poços. Qual estratégia é tecnicamente mais defensável e por quê?

**R:** A desmontagem offshore ganha força. A avaliação inicial favorável não basta para justificar o tow-out, porque a aceitabilidade do reboque depende também de a unidade ser colocada na condição requerida para navegação ou reboque, com limpeza da planta e tanques, drenagem, ventilação, purga, lavagem, remoção de TENORM e isolamento para evitar recontaminação; só depois disso vêm os reforços e ajustes estruturais para navegação. Além disso, a presença de espécies exóticas invasoras torna o método de reflutuação e reboque não recomendado, pois aumenta o risco de disseminação. Somado a isso, retirar a unidade próxima de instalação adjacente com risers ou operações de poço introduz risco de perda de posição com potencial de colisão ou liberação de hidrocarbonetos. Assim, o reboque deixa de ser uma vantagem logística simples e passa a concentrar restrições ambientais e perigo de acidente maior.

- **gpt-5-2-petrobras:medium:** reprova (suporte) · Falta de suporte: a resposta afirma que a manobra próxima 'introduz risco de perda de posição', mas F3 apenas descreve consequências caso haja perda de posição; para ficar suportado, deve-se condicionar: 'se ocorrer perda de posição, pode haver colisão/liberação...' ou remover a causalidade.
- **o3-petrobras:medium:** aprova
- **gpt-5-4-petrobras:medium:** aprova
- **gpt-5-petrobras:medium:** aprova

### 332e35e913-b0-A2 · media · Gestão do Desempenho Empresarial (KPI)

**P:** Um elemento crítico de segurança (SCE) foi identificado como degradado e a unidade pretende avaliar se pode continuar operando. Quais elementos de governança devem existir nessa avaliação de risco?

**R:** Devem existir, no mínimo, um procedimento formal e robusto que defina como a avaliação de risco será feita, quais são os níveis de autoridade para decidir, qual expertise técnica deve participar e quais revisões são exigidas. A avaliação deve considerar o papel do SCE como barreira contra major accident hazards, para sustentar medidas mitigatórias e, se necessário, barreiras adicionais. Também deve haver registro das avaliações e auditoria regular desses registros. Como o risco combinado pode ser elevado mesmo quando avaliações individuais parecem adequadas, o processo deve prever revisões gerais periódicas com expertise apropriada, sem depender apenas da gestão offshore. Além disso, dados de desempenho, KPIs e achados de auditoria devem ser reportados ao nível sênior, com ações decorrentes.

- **gpt-5-2-petrobras:medium:** reprova (suporte, sem_generalizacao) · Falta de suporte literal para a expressão de minimalidade ('no mínimo').; Generalização normativa: a redação impõe como regra universal requisitos derivados de referência em contexto UK; pode ser reparado qualificando como 'conforme a referência' ou 'como boa prática' sem adicionar conteúdo novo.
- **o3-petrobras:medium:** aprova
- **gpt-5-4-petrobras:medium:** aprova
- **gpt-5-petrobras:medium:** aprova

### 332e35e913-b1-A1 · dificil_A · Gestão do Desempenho Empresarial (KPI)

**P:** Um KPI preditivo de confiabilidade de um conjunto motobomba permaneceu com tendência suave e aparentemente estável, mas em campo surgiram sinais de degradação pouco depois da troca do motor. A equipe confirma que a análise veio de uma única base, sem planilhas paralelas, e que não houve mudança relevante de fluido ou de regime de processo no período. Qual é a causa mais provável da inconsistência do KPI e por quê?

**R:** A causa mais provável é a perda de rastreabilidade do item físico monitorado. Quando o sistema identifica o equipamento pela localização funcional e o componente substituído recebe o mesmo tag ID, o histórico do item antigo pode ser fundido ao do novo, criando uma falsa continuidade de desempenho. Isso explica um KPI com tendência suave ou estável mesmo após troca de componente e com comportamento em campo já diferente. Como o cenário exclui fragmentação entre ferramentas e mudanças relevantes de processo, essas hipóteses perdem força. Erro de dado continua possível em qualquer sistema, mas o indício dominante aqui é a manutenção do mesmo identificador após substituição, justamente a condição que pode confundir históricos e distorcer a leitura preditiva do KPI.

- **gpt-5-2-petrobras:medium:** reprova (suporte) · Falha de suporte: a resposta introduz possibilidade de 'erro de dado em qualquer sistema' sem fato citado que sustente; seria necessário citar F4 ou remover/reformular a frase para ficar integralmente apoiada nos fatos listados.
- **o3-petrobras:medium:** aprova
- **gpt-5-4-petrobras:medium:** reprova (suporte, sem_generalizacao) · Há extrapolação sem suporte em 'erro de dado continua possível em qualquer sistema'.; A resposta ficaria plenamente suportada se removesse a generalização e ficasse apenas na causa de rastreabilidade sustentada por F5.
- **gpt-5-petrobras:medium:** aprova

### 332e35e913-b2-A1 · dificil_B · Gestão do Desempenho Empresarial (KPI)

**P:** Em um FPSO sob preço de petróleo pressionado, a gestão reforçou metas de redução de OPEX e manutenção da produção. Nas semanas seguintes, margem e volume melhoraram, mas cresceram adiamentos de manutenção e desvios operacionais com potencial de reduzir a efetividade de funções de segurança. Ao revisar o painel estratégico, qual mudança de desenho é mais adequada para decidir se o ativo está realmente criando valor, e não apenas antecipando ganho econômico à custa de risco futuro?

**R:** A revisão deve substituir um painel centrado em volume e custo por um sistema de KPIs que explicite a cadeia causal entre estratégia, decisões operacionais, manutenção, resultado econômico e risco de processo. Em ambiente mutável, o sistema de indicadores deve apoiar a gestão estratégica e o entendimento da criação de valor, por meio de um mapa sistêmico com inter-relações entre variáveis-chave e associação de eventos relevantes às variáveis usadas para monitorar seus efeitos nos resultados. Sob pressão de margem, os KPIs precisam mostrar simultaneamente efeitos sobre CAPEX/OPEX e sobre a capacidade de sustentar receita, evitando premiar eficiência local sem consequência econômica real. Como desvios de produção e manutenção podem degradar funções de segurança e aumentar frequência e/ou severidade de cenários de risco, o painel deve incorporar indicadores que revelem esses desvios e seus impactos sobre continuidade operacional e sustentabilidade do negócio, não apenas ganho financeiro imediato.

- **gpt-5-2-petrobras:medium:** reprova (suporte) · Falta de suporte explícito para caracterizar o painel atual como 'centrado em volume e custo' e para a prescrição de 'substituição' nesses termos (não consta em F1–F12).; Falta de suporte para a expressão 'continuidade operacional' como consequência/variável a ser indicada; os fatos falam em sustentabilidade do negócio, não em continuidade operacional como item específico (F11–F12).; A resposta poderia ficar totalmente suportada se reescrevesse esses trechos usando apenas termos e relações presentes em F1–F4, F7–F9 e F11–F12 (ex.: focar em causalidade sistêmica, efeitos econômicos e aumento de frequência/severidade de cenários de risco).
- **o3-petrobras:medium:** aprova
- **gpt-5-4-petrobras:medium:** reprova (suporte) · Falta suporte explícito para 'continuidade operacional' na resposta.; Falta suporte explícito para a oposição 'não apenas ganho financeiro imediato'.; A formulação sobre mostrar simultaneamente CAPEX/OPEX e sustentação de receita está plausível, mas não está ancorada de modo direto e completo nos fatos citados.
- **gpt-5-petrobras:medium:** aprova

### b56db319e4-b0-A1 · facil · Logística e Suprimento Offshore

**P:** Por que a eliminação do umbilical em operações com AUV reduz a exigência sobre o sistema de lançamento e sobre a embarcação de apoio, e por que esse efeito tende a aumentar com a profundidade?

**R:** Porque, sem umbilical, a operação com AUV deixa de depender de recursos de lançamento mais robustos associados ao manejo contínuo desse vínculo com a superfície, como guincho e pórtico com compensação de heave. Isso simplifica o lançamento e reduz a demanda estrutural e operacional imposta à embarcação de apoio. O efeito cresce com a profundidade porque a redução desses requisitos tem impacto diretamente proporcional ao aumento da profundidade, tornando mais relevante a diferença logística entre um arranjo sem umbilical e outro que depende desse tipo de suporte.

- **gpt-5-2-petrobras:medium:** reprova (suporte) · Falta de suporte estrito para trechos que vão além do F6 ('manejo contínuo', 'simplifica o lançamento', 'demanda estrutural e operacional na embarcação'). Ajustar a redação para ficar estritamente dentro do que o F6 afirma (redução de exigência de guincho/pórtico com heave compensation e impacto proporcional à profundidade).
- **o3-petrobras:medium:** aprova
- **gpt-5-4-petrobras:medium:** aprova
- **gpt-5-petrobras:medium:** aprova

### b56db319e4-b0-A2 · media · Logística e Suprimento Offshore

**P:** Uma campanha submarina inicialmente prevista para inspeção de rotina passou a incluir abertura de válvulas e cortes localizados no fundo do mar. Como essa mudança afeta a escolha entre AUV e ROV?

**R:** A escolha passa a favorecer o ROV. Para inspeção, o AUV reduz requisitos de lançamento e de embarcação por não usar umbilical, o que simplifica a logística. Porém, quando o escopo inclui intervenção física, como abertura e fechamento de válvulas, cortes e hidrojateamento, o requisito principal deixa de ser apenas cobertura de inspeção e passa a ser capacidade operacional de atuar sobre os componentes submarinos. O ROV atende esse tipo de tarefa porque dispõe de manipuladores e sistemas de operação remota para executar intervenções, embora isso exija sala de controle dedicada, equipe mínima específica e operação de guincho na borda da unidade, aumentando as interfaces logísticas e operacionais.

- **gpt-5-2-petrobras:medium:** aprova
- **o3-petrobras:medium:** aprova
- **gpt-5-4-petrobras:medium:** reprova (suporte) · Suporte incompleto para 'reduz requisitos de embarcação' na parte do AUV.; Parte da conclusão sobre aumento de interfaces logísticas do ROV está inferida, não explicitamente sustentada pelos fatos citados.; Como há falta de suporte material em afirmações substantivas, a questão deve ser reprovada nos termos do critério de suporte.
- **gpt-5-petrobras:medium:** aprova

### b56db319e4-b1-A1 · dificil_A · Logística e Suprimento Offshore

**P:** Uma operadora offshore discute cortar o estoque de um componente cuja falha interrompe uma função crítica de segurança e também pode prolongar a perda de produção até a restauração da função. O mercado fornecedor desse item é complexo, e a área usuária exige alto nível de serviço. Entre reduzir estoque, manter o sobressalente a bordo/base ou priorizar apenas parceria com fornecedor, qual decisão é tecnicamente mais adequada e por quê?

**R:** A decisão mais adequada é manter o sobressalente disponível, porque a prioridade deve seguir a criticidade, o risco da falha e a necessidade de reduzir o tempo de restauração da função. Em item crítico, a indisponibilidade compromete a mitigação de consequências de segurança e pode ampliar o downtime de produção; por isso, tratá-lo apenas como corte de inventário é tecnicamente frágil. O custo relevante não é só o valor estocado, mas o custo total do suprimento combinado com o nível de serviço requerido. Como níveis mais altos de serviço se relacionam diretamente com custo e desempenho da cadeia, reduzir estoque para melhorar apenas indicador interno de custo pode piorar atendimento e continuidade operacional. A complexidade do mercado fornecedor reforça a necessidade de estratégia de sourcing e parceria, mas como complemento para reduzir custo total e sustentar serviço, não como substituto da disponibilidade imediata do item crítico.

- **gpt-5-2-petrobras:medium:** reprova (suporte) · Falta de suporte explícito para 'parceria com fornecedor/alianças' (seria necessário citar F11/F12 para sustentar parcerias como estratégia).; Falta de suporte/citação para a crítica a reduções internas de estoque sem enfoque logístico total (seria necessário citar F9).; Trecho 'parceria ... não como substituto da disponibilidade imediata' extrapola o que F13 afirma (SCM melhora atendimento/reduz custos), exigindo reescrita ou suporte adicional.
- **o3-petrobras:medium:** aprova
- **gpt-5-4-petrobras:medium:** reprova (suporte, sem_generalizacao) · Suporte parcial para a recomendação de parceria com fornecedor no cenário genérico.; Generalização de fatos contextuais sobre alianças/parcerias para além das condições explicitadas nas fontes.
- **gpt-5-petrobras:medium:** aprova

### b56db319e4-b2-A1 · dificil_B · Logística e Suprimento Offshore

**P:** Um FPSO, com baixa capacidade de armazenagem, pede na mesma viagem de PSV contêineres de materiais de manutenção, consumíveis operacionais e alguns volumes longos de geometria desfavorável. Pela lista de pesos, tudo caberia, mas no carregamento real o convés não fecha. Como a carga deve ser repriorizada para essa viagem, e qual é o erro técnico de tratar a decisão apenas pela tonelagem total disponível?

**R:** A repriorização deve partir do gargalo real: a área útil e a geometria de arrumação no convés do PSV, não a tonelagem total. No PSV, carga de convés não pode ser empilhada, deve permanecer no nível do convés e não pode ser rotacionada livremente; por isso, itens longos ou de geometria desfavorável podem consumir a capacidade prática mesmo quando a massa total parece aceitável. Nessa condição, entram primeiro os itens de maior criticidade para manter operação segura e continuidade operacional do FPSO, e ficam para viagem posterior os materiais menos críticos que bloqueiam área desproporcional. A lógica correta é selecionar o conjunto que melhor usa a área de convés escassa e evita interrupção de atividades, porque a unidade não consegue compensar falhas logísticas estocando tudo a bordo. O erro técnico é supor que peso total representa capacidade útil quando o limitante físico da viagem é o deck cargo.

- **gpt-5-2-petrobras:medium:** reprova (suporte) · Falta de suporte para a afirmação de 'operação segura' (não há fato citado que conecte este critério à decisão de carga no contexto apresentado).; Citações F12 e F20 não sustentam o conteúdo efetivamente usado; introduzem tema (POB/downtime) que não aparece no raciocínio e pode confundir o critério.; Para ficar totalmente aderente ao material, a resposta deveria formular o critério como continuidade do trabalho/evitar interrupção e perda econômica (F11) sob restrição física de convés (F7/F8), sem invocar segurança sem suporte.
- **o3-petrobras:medium:** aprova
- **gpt-5-4-petrobras:medium:** reprova (suporte) · A expressão 'manter operação segura' não tem suporte factual direto para priorização de cargas neste cenário.; O critério de seleção por 'maior criticidade' está apenas indiretamente inferido a partir de F11, sem suporte factual explícito suficiente como formulado na resposta.
- **gpt-5-petrobras:medium:** aprova

### 26d45ade58-b0-A1 · facil · Movimentação de Cargas

**P:** Qual é a função do lifting plan em uma operação de içamento e como ele se relaciona com a definição do equipamento a ser utilizado?

**R:** O lifting plan funciona como a instrução operacional da atividade: ele descreve o içamento em etapas passo a passo e especifica o equipamento que deve ser usado na execução. Assim, ele não é apenas um registro administrativo, mas a referência que traduz a tarefa em um método previamente definido para a equipe em campo. Para cumprir essa função de controle, o plano deve ser elaborado por uma Pessoa Competente ou, no mínimo, autorizado por ela.

- **gpt-5-2-petrobras:medium:** reprova (suporte) · Suporte insuficiente: a resposta inclui enquadramentos (‘não é apenas registro administrativo’, ‘função de controle’, ‘referência que traduz a tarefa em método para a equipe’) que não estão explicitamente suportados por F1 (único fato citado).; Completude/aderência ao alvo: para A1, a parte sobre Pessoa Competente é correta, mas não é necessária para responder ao alvo e aumenta o risco de incluir conteúdo não pedido.
- **o3-petrobras:medium:** aprova
- **gpt-5-4-petrobras:medium:** reprova (suporte) · A resposta contém afirmação sem suporte explícito: 'não é apenas um registro administrativo'.; A resposta extrapola levemente o alvo A1 ao incluir requisito de Pessoa Competente, ainda que isso não a torne tecnicamente incorreta.
- **gpt-5-petrobras:medium:** aprova

### 26d45ade58-b0-A2 · media · Movimentação de Cargas

**P:** Em um içamento, o plano foi emitido, mas o supervisor se afasta da área e a equipe continua o trabalho com pouco monitoramento em campo. Qual é o papel técnico do supervisor de içamento e da organização para manter a aderência entre o plano, a execução e o monitoramento do trabalho?

**R:** O supervisor deve manter acompanhamento em campo para que a execução permaneça aderente ao método autorizado, assegurando continuidade entre plano, trabalho real e monitoramento da atividade. A organização, por sua vez, deve ter procedimentos efetivos de supervisão e monitoramento, verificar se esses procedimentos funcionam na prática e identificar fatores que prejudiquem a supervisão efetiva, como falta de tempo ou treinamento insuficiente do supervisor. Isso é relevante porque supervisão inadequada aparece como causa subjacente importante de acidentes, e a continuidade do trabalho sem supervisão adequada favorece desvio entre o que foi planejado e o que é executado.

- **gpt-5-2-petrobras:medium:** reprova (suporte) · Suporte insuficiente: termos/ideias de ‘método autorizado’ e ‘aderência plano–execução’ não estão sustentados por F4–F6 (exigiriam F1/F2/F3 ou reformulação para ficar estritamente no que F6 evidencia).; Completude: não explicita, como ação organizacional/supervisão, a necessidade de garantir a disponibilidade do Lift Plan junto à equipe durante a execução, embora isso seja central em F6.; Suporte parcial: a primeira e a última afirmação extrapolam o texto literal de F6 ao falar em ‘método autorizado’ e ‘desvio’, sem ancoragem explícita nos fatos citados.
- **o3-petrobras:medium:** aprova
- **gpt-5-4-petrobras:medium:** aprova
- **gpt-5-petrobras:medium:** aprova

### 26d45ade58-b2-A1 · dificil_B · Movimentação de Cargas

**P:** Em um içamento próximo a estruturas, o operador confirma resposta ao comando de descida, mas o rigger não observa avanço coerente da carga no trajeto. O indicador de peso não sugere sobrecarga, a visibilidade do operador é limitada e parte da equipe interpreta a situação como simples resistência da carga no apoio. Como o supervisor deve diagnosticar a condição e qual decisão operacional deve priorizar?

**R:** O quadro deve ser tratado primeiro como possível interferência mecânica na trajetória ou na linha, e não como mera resistência da carga. A combinação de comando executado, ausência de movimento coerente da carga e indicação de peso aparentemente normal é compatível com snag, em que parte da sustentação migra para a estrutura e o indicador deixa de representar corretamente a carga no guincho. Com visibilidade limitada, o diagnóstico deve cruzar comportamento real da carga, trajetória da linha e pontos potenciais de contato previamente mapeados, com comunicação explícita de verificação incremental do movimento. A decisão prioritária é interromper a manobra, confirmar caminho livre da linha e da carga e investigar interferências antes de prosseguir, porque insistir pode acumular folga/energia e levar à liberação súbita do ponto preso.

- **gpt-5-2-petrobras:medium:** reprova (suporte) · Falta de suporte: a resposta prescreve 'interromper a manobra' como decisão prioritária, mas não há F# citado que estabeleça esse critério explicitamente.; Falta de suporte: a justificativa por 'acumular folga/energia' não está sustentada nos F# citados (é explicação da nota, mas não aparece como fato referenciado).; Se a intenção é usar a NOTA 3 (decisoes_criterios) como base para 'interromper e confirmar caminho livre', isso precisa ser trazido como suporte factual citável (ou o texto deve ser reescrito para ficar estritamente dentro de F4/F5/F12/F14/F15/F17).
- **o3-petrobras:medium:** aprova
- **gpt-5-4-petrobras:medium:** aprova
- **gpt-5-petrobras:medium:** aprova

### a807dbd01e-b0-A1 · facil · Apoio Técnico e Manutenção em um FPSO (Laboratório, Oficinas, Pipe Shop)

**P:** Qual é a finalidade da limpeza prévia do equipamento de amostragem e de ensaio antes de testes laboratoriais de corrosão?

**R:** A limpeza prévia serve para evitar contaminações introduzidas pelo próprio sistema de amostragem ou pelo aparato de ensaio. Resíduos remanescentes podem falsear o resultado do teste de corrosão, fazendo o laboratório medir um efeito do equipamento contaminado, e não a condição real que se pretende avaliar. Por isso, a limpeza conforme método estabelecido é uma barreira para preservar a validade do ensaio e sua utilidade em decisões técnicas.

- **gpt-5-2-petrobras:medium:** reprova (suporte) · Falta suporte explícito para trechos que extrapolam F2 ("condição real", "barreira", "validade" e "utilidade em decisões técnicas"). Pode ser corrigido restringindo a resposta ao que F2 afirma: limpeza prévia conforme método estabelecido para evitar contaminações que falseiem o resultado do ensaio.
- **o3-petrobras:medium:** aprova
- **gpt-5-4-petrobras:medium:** aprova
- **gpt-5-petrobras:medium:** aprova

### a807dbd01e-b2-A1 · dificil_B · Apoio Técnico e Manutenção em um FPSO (Laboratório, Oficinas, Pipe Shop)

**P:** Em um FPSO, recomendações antigas de inspeção em equipamentos críticos aparecem com status divergente entre sistemas. Há ordens de serviço encerradas, mas os registros não ligam claramente o achado à intervenção executada, nem mostram inspeções, testes ou ensaios de aceitação e a justificativa técnica para retorno ao serviço. A operação afirma que os itens já foram tratados. Qual deve ser o diagnóstico prioritário e a decisão gerencial imediata para reduzir o risco de interdição?

**R:** O diagnóstico prioritário é perda de controle da integridade por falha de rastreabilidade e de fechamento técnico das recomendações, não simples atraso administrativo. Em itens críticos, o plano deve identificar mecanismos de dano, periodicidades, recursos e a sistemática de registros; sem isso, não se demonstra o que foi inspecionado, qual achado existia e se a intervenção tratou o dano relevante. A recomendação só reduz risco quando entra em sistemática formal com classificação, prazo compatível com o risco, acompanhamento e verificação por inspeções, testes ou ensaios que aprovem o serviço executado. Se o registro não conecta condição observada, ação corretiva e autorização técnica de retorno ao serviço, a alegação de que o item foi “endereçado” não comprova restauração da segurança operacional. A decisão imediata é reconstituir e revisar essas pendências por criticidade, exigir evidência técnica de aceitação ou adotar contingências e restrições operacionais até o fechamento rastreável, porque falhas nesse ciclo podem sustentar interdição.

- **gpt-5-2-petrobras:medium:** reprova (suporte) · Falta de suporte para exigir ‘justificativa/autoridade técnica de retorno ao serviço’ com os fatos citados; isso exigiria incluir fato específico (não fornecido na lista) ou remover/reformular.; Falta de suporte para a formulação normativa/causal ‘a recomendação só reduz risco quando...’ do modo como está escrita; pode ser reescrita para ficar estritamente ancorada em F5 (exigência de controle de qualidade por inspeções/testes/ensaios) e F4 (interdição quando não há ação compatível com o risco).
- **o3-petrobras:medium:** aprova
- **gpt-5-4-petrobras:medium:** reprova (suporte) · Falta suporte explícito para 'autorização técnica de retorno ao serviço'.; 'Restrições operacionais' não aparece como medida explícita nos fatos fornecidos.; A frase sobre o registro conectar condição observada, ação corretiva e retorno ao serviço extrapola os F# disponíveis, embora seja tecnicamente plausível.
- **gpt-5-petrobras:medium:** aprova

### e1b6ad83e3-b0-A2 · media · Cibersegurança e Integridade de Sistemas Digitais

**P:** Em um sistema usado para funções essenciais, o cadastro aceita senhas fracas e depois ocorrem logins válidos associados a ações indevidas em contas de usuário. Como a exigência de qualidade de senha se relaciona com a confiabilidade da autenticação e com a prevenção desse tipo de uso indevido?

**R:** Se o sistema aceita senhas sem qualidade adequada, a autenticação perde confiabilidade porque um login válido deixa de representar, com segurança suficiente, que a conta está sendo usada pelo agente autorizado. Nesse caso, a entrada no sistema pode ocorrer por apropriação indevida da credencial, mesmo sem falha aparente no registro de login. Exigir qualidade de senha atua na origem do problema, fortalecendo a credencial antes do primeiro uso e reduzindo a chance de uso indevido da conta. Em sistemas que sustentam funções essenciais, isso é relevante porque o acesso deve ser autenticado de forma robusta e a proteção da credencial integra a defesa da integridade operacional.

- **gpt-5-2-petrobras:medium:** reprova (suporte, sem_generalizacao) · Falta de suporte: o nexo causal entre qualidade de senha, confiabilidade da autenticação e prevenção de uso indevido não está estabelecido em F1/F5, mas é o núcleo do alvo A2.; Generalização sem base factual: afirma mecanismos e consequências (apropriação indevida, perda de confiabilidade do login) não suportados pelos fatos citados.
- **o3-petrobras:medium:** aprova
- **gpt-5-4-petrobras:medium:** aprova
- **gpt-5-petrobras:medium:** aprova

### 460979b6f3-b0-A1 · facil · Inspeção e Integridade

**P:** O que é Inspeção Baseada em Risco (IBR/RBI) e como a combinação de probabilidade e consequência de falha é usada para priorizar inspeção e manutenção de equipamentos em uma unidade de processo?

**R:** IBR/RBI é uma metodologia em que o risco orienta as decisões de inspeção e manutenção. Em vez de distribuir recursos de forma uniforme, ela avalia cada equipamento pela combinação entre probabilidade de falha e consequência de falha para definir prioridades. Essa análise deve ser coerente com os mecanismos de dano atuantes e incorporar o histórico operacional do equipamento para atualizar o risco. Com isso, os equipamentos com maior risco relativo tendem a receber primeiro inspeção e manutenção, e o plano pode ajustar intensidade, método e escopo conforme a criticidade e a evolução das condições em serviço.

- **gpt-5-2-petrobras:medium:** reprova (suporte) · Falta de suporte para: (1) afirmação de que a IBR/RBI se opõe à distribuição uniforme de recursos; (2) afirmação de ajuste de intensidade/método/escopo conforme criticidade/evolução. Para reparar, remover ou reescrever essas partes para ficar estritamente dentro de F1/F2 (priorização por risco e atualização por histórico).
- **o3-petrobras:medium:** reprova (suporte) · Falta de suporte explícito para a última afirmação (não foi citado o fato F10).
- **gpt-5-4-petrobras:medium:** aprova
- **gpt-5-petrobras:medium:** aprova

### 460979b6f3-b0-A2 · media · Inspeção e Integridade

**P:** Após uma inspeção, um vaso em FPSO passa a apresentar indícios de mecanismo de dano diferente do previsto, e a unidade também mudou suas condições de operação desde a última análise. Por que o plano de inspeção deve ser revisto nesse caso?

**R:** O plano deve ser revisto porque, em IBR, o risco é atualizado com base nos mecanismos de dano efetivamente atuantes e no histórico operacional mais recente. Se a inspeção indica dano diferente do esperado, a base técnica do plano anterior pode ter perdido aderência. Além disso, mudanças nas condições de operação alteram o histórico do equipamento e podem modificar sua probabilidade de falha e sua priorização. Como a efetividade do plano depende da compatibilidade entre técnica de inspeção e mecanismo de dano, a revisão é necessária para reavaliar métodos, escopo e frequência e manter a inspeção capaz de detectar e dimensionar o dano de forma confiável.

- **gpt-5-2-petrobras:medium:** reprova (suporte) · Falta suporte, com os fatos citados, para 'compatibilidade entre técnica de inspeção e mecanismo de dano' e para a conclusão operacional de 'reavaliar métodos, escopo e frequência'.; Para sustentar essas partes, seria necessário citar fatos adicionais do material (por exemplo, F1 para coerência com mecanismos de dano e F10/F9 para ajuste de nível de inspeção) e/ou ajustar a redação para ficar estritamente dentro de F2/F4/F8.
- **o3-petrobras:medium:** aprova
- **gpt-5-4-petrobras:medium:** aprova
- **gpt-5-petrobras:medium:** aprova

### 460979b6f3-b1-A1 · dificil_A · Inspeção e Integridade

**P:** Um FPSO pretende executar UWILD no lugar da docagem. Na preparação, a equipe propõe concentrar o exame no costado externo e tratar separadamente os compartimentos internos, enquanto no espaço de máquinas há indícios de deterioração junto aos brackets na ligação com o topo do tanque, anteparas próximas aos poços de bilge e também nas conexões laterais do casco. Qual lógica de inspeção e decisão melhor preserva o envelope do casco nesse caso?

**R:** A lógica correta é tratar o envelope do casco como uma barreira única de integridade, não como inspeções isoladas. Para usar UWILD, o envelope externo deve estar coberto por um plano formal de inspeção de integridade já desenvolvido e implementado. Esse plano precisa integrar o exame do costado externo com os compartimentos estruturais internos incluídos no escopo de inspeção e com as conexões laterais do casco, porque a estanqueidade depende também de válvulas de casco e tubulações associadas. No espaço de máquinas, os pontos críticos junto aos brackets na região do topo do tanque, às anteparas próximas ao topo do tanque e aos poços de bilge exigem atenção especial. Além do exame visual, devem ser aplicadas medições de espessura e testes quando necessários para identificar corrosão substancial, deformações, fraturas e outros danos. Se a degradação puder comprometer resistência estrutural ou estanqueidade, a decisão deve ser reparar ou renovar para restabelecer a integridade.

- **gpt-5-2-petrobras:medium:** reprova (jurisdicao) · Jurisdição: F1 e F2 são explicitamente HSE/UK; a resposta usa linguagem mandatória ('deve') sem qualificar a origem/âmbito (diretriz do UK), podendo induzir obrigação fora do contexto.; Ajuste simples possível: trocar por 'conforme diretriz HSE/UK' ou por linguagem de boa prática ('deve/é recomendado conforme...') mantendo o mesmo material.
- **o3-petrobras:medium:** aprova
- **gpt-5-4-petrobras:medium:** aprova
- **gpt-5-petrobras:medium:** aprova

### 460979b6f3-b2-A1 · dificil_B · Inspeção e Integridade

**P:** Em um FPSO de casco simples, um tanque que armazenou água produzida apresenta perda de espessura em regiões com revestimento em condição ruim. Na mesma campanha, a eficácia da proteção catódica não pôde ser confirmada porque há indícios de queda de potencial e ânodos desgastados. Tecnicamente, isso pode ser tratado como anomalia localizada com simples acompanhamento, ou deve receber prioridade maior? Justifique a decisão pelo mecanismo de dano e pelo escopo mínimo de reavaliação.

**R:** Deve receber prioridade maior. A perda de espessura não deve ser lida isoladamente: ela precisa ser comparada com a espessura mínima estrutural acrescida da sobreespessura para corrosão, porque a redução de seção afeta a capacidade resistente da chapa. Ao mesmo tempo, o revestimento em condição ruim remove uma barreira anticorrosiva e está associado ao aumento da corrosão e à própria redução de espessura. Se a proteção catódica também está duvidosa, a combinação de queda de potencial e desgaste dos ânodos indica perda de desempenho por despolarização, situação que requer ação corretiva. Portanto, não é caso de simples acompanhamento local: a reavaliação deve integrar espessura remanescente, condição do revestimento e funcionalidade da proteção catódica, incluindo verificação por potencial, corrente e condição física dos ânodos, para decidir reparo, restauração das barreiras e prioridade de inspeção.

- **gpt-5-2-petrobras:medium:** reprova (suporte, autonomia) · Falta de suporte explícito para a afirmação ‘redução de seção afeta a capacidade resistente’ (remover ou reescrever ancorando estritamente em F17).; Falta de suporte para ‘decidir reparo/restauração das barreiras’ no contexto de tanques; os fatos citados sobre ação corretiva (F6/F8) são de PC em equipamentos/dutos, não decisão de reparo de tanque/revestimento.; Autonomia: ‘escopo mínimo’ sugere resposta que depende de F13 (avaliar todos os tanques com histórico de água produzida); a resposta não explicita isso e a pergunta não é plenamente respondível sem o material.
- **o3-petrobras:medium:** aprova
- **gpt-5-4-petrobras:medium:** aprova
- **gpt-5-petrobras:medium:** aprova

### 1c3fa83845-b0-A1 · facil · Instrumentação, Controle e Automação

**P:** Por que a calibração periódica manual pode reduzir a disponibilidade do processo e nem sempre ser a melhor estratégia de manutenção de instrumentos?

**R:** Porque a calibração periódica manual frequentemente exige retirada do instrumento de operação e, em muitos casos, parada do processo, o que impacta diretamente a disponibilidade. Além disso, essa estratégia pode levar a intervenções desnecessárias, já que foi observado que uma pequena parcela das calibrações manuais realizadas era realmente necessária. Há ainda o risco de a própria intervenção manual afetar negativamente a confiabilidade do instrumento. Por isso, quando o estado do instrumento pode ser validado por evidências do seu comportamento metrológico em operação, a intervenção deixa de ser apenas rotineira por calendário e passa a ser tecnicamente mais bem justificada.

- **gpt-5-2-petrobras:medium:** reprova (suporte) · Falta de suporte explícito em F1 para a parte que contrasta com manutenção/validação em operação e política baseada em evidência (a resposta introduz manutenção por condição sem fato correspondente citado). Para reparar com o mesmo material citado (F1), basta remover/restringir essa última justificativa e manter apenas disponibilidade, desnecessidade e impacto na confiabilidade.
- **o3-petrobras:medium:** aprova
- **gpt-5-4-petrobras:medium:** reprova (suporte) · Há extrapolação não sustentada pelo fato citado F1 na frase final sobre validação em operação e mudança de política de intervenção por calendário para intervenção baseada em evidência.
- **gpt-5-petrobras:medium:** aprova

### 1c3fa83845-b0-A2 · media · Instrumentação, Controle e Automação

**P:** Em um transmissor, as leituras sob a mesma condição de processo passam a apresentar maior dispersão em medições sucessivas, mas sem deslocamento persistente da média ao longo do tempo. Em outro caso, as leituras permanecem pouco dispersas, porém a indicação se desloca lentamente de forma contínua ao longo das semanas. Como distinguir tecnicamente esses dois comportamentos?

**R:** No primeiro caso, o padrão é mais compatível com perda de repetibilidade, porque o problema aparece como aumento da dispersão em medições sucessivas sob as mesmas condições, sem tendência lenta persistente. No segundo, o comportamento é compatível com deriva, porque a indicação mantém boa repetibilidade no curto prazo, mas sofre deslocamento gradual ao longo do tempo. Tecnicamente, a repetibilidade expressa a estabilidade em curto prazo, enquanto a deriva representa uma variação lenta das características metrológicas, associada à estabilidade de longo prazo. Portanto, a chave do diagnóstico é separar dispersão de curto prazo de deslocamento sistemático e progressivo.

- **gpt-5-2-petrobras:medium:** reprova (suporte) · Falta suporte factual explícito (apenas com F2) para associar diretamente ‘aumento de dispersão sem tendência’ a perda de repetibilidade e ‘boa repetibilidade com deslocamento gradual’ a deriva; isso aparece como regra diagnóstica na resposta, mas não está literal no fato citado.; Para ficar suportado apenas por F2, a resposta precisaria se limitar a mapear os comportamentos a ‘curto prazo/repetibilidade’ versus ‘longo prazo/deriva’ sem afirmar critérios diagnósticos adicionais não presentes no fato.
- **o3-petrobras:medium:** aprova
- **gpt-5-4-petrobras:medium:** aprova
- **gpt-5-petrobras:medium:** aprova

### 1c3fa83845-b1-A1 · dificil_A · Instrumentação, Controle e Automação

**P:** Em uma unidade offshore, um transmissor de nível com HART sobre 4–20 mA foi ligado à automação baseada em FOUNDATION Fieldbus, e uma variável de pressão já existente no sistema de automação deixou de aparecer na supervisão Web após alteração de configuração. Considerando a arquitetura descrita, por que a integração precisa ser tratada em duas camadas e qual verificação técnica cabe em cada uma para restabelecer a disponibilização fim a fim das variáveis?

**R:** A integração é separada em duas camadas porque elas resolvem problemas técnicos diferentes. A primeira é a compatibilização entre o sinal de campo e a rede de automação: um instrumento com saída 4–20 mA, 0–20 mA ou HART sobre 4–20 mA não entra diretamente na rede FOUNDATION Fieldbus no arranjo descrito, então deve passar por um conversor de corrente para fieldbus. Sem essa interface, a variável nem chega ao ambiente de automação. A segunda camada é a disponibilização supervisória: depois de recebidos, os dados precisam ser mapeados, receber endereçamento padronizado e ser armazenados no servidor OPC-DA, pois a aplicação cliente Web usa essa base para publicar as variáveis. Assim, para o transmissor de nível, a verificação principal é a conversão para FOUNDATION Fieldbus; para a pressão que já está na automação mas sumiu da Web, a verificação principal é o mapeamento/endereço no OPC-DA. Quando mapeadas e disponíveis, essas variáveis podem ser exibidas em navegador, inclusive em smartphone.

- **gpt-5-2-petrobras:medium:** reprova (suporte, sem_generalizacao) · Falta de suporte/qualificação: a frase sobre exibição em smartphone é sustentada apenas por F3, que é específico do monitoramento BCP; a questão/arquitetura na pergunta não restringe ao BCP. Para ficar suportado, precisa remover a menção a smartphone ou condicionar explicitamente ao caso do BCP conforme F3.; Generalização indevida (sem_generalizacao): extrapola característica específica (uso em smartphone no BCP) para o caso geral.
- **o3-petrobras:medium:** aprova
- **gpt-5-4-petrobras:medium:** reprova (autonomia) · A pergunta não é plenamente autônoma: remete à 'arquitetura descrita' e pressupõe conhecimento da etapa OPC-DA/Web que não está explicitada no enunciado.
- **gpt-5-petrobras:medium:** reprova (autonomia) · Autonomia: a questão depende do conhecimento da arquitetura específica descrita no material (conversor para FF e servidor OPC-DA), o que reduz a respondibilidade sem o texto-base.

### 1c3fa83845-b2-A1 · dificil_B · Instrumentação, Controle e Automação

**P:** Em um separador trifásico de FPSO, a malha que tenta estabilizar a condição interna perde qualidade quando a composição das fases varia. A equipe quer usar a mesma medição para controle contínuo e também para proteção por interface crítica. Qual decisão técnica é mais coerente quanto ao princípio de medição e à cadeia medição-atuação, e por quê?

**R:** A decisão mais coerente é controlar a interface com medição associada ao fenômeno de separação relevante no ponto crítico do vaso, usando sinal apto a controle e proteção, e manter atuação proporcional no elemento final. Para interface próxima à saída de água, a medição nucleônica por densidade é a mais alinhada, porque pode alimentar o controlador e também gerar desarme quando a interface de água fica extremamente baixa. Já o radar de onda guiada mede pela reflexão na descontinuidade dielétrica ao longo da sonda; se a composição variar, o contraste dielétrico entre fases muda e a qualidade do eco pode piorar, afetando a robustez da indicação. Mesmo com princípio físico adequado, a medição só serve à malha se tempo de resposta, resposta em frequência e sensibilidade a variáveis de instalação forem compatíveis com a dinâmica do processo. Na atuação, a saída deve ir para válvula de controle com posicionamento contínuo; liga-desliga não é ideal para controle proporcional.

- **gpt-5-2-petrobras:medium:** reprova (suporte) · Falta de suporte estrito para a afirmação ‘válvula de controle com posicionamento contínuo’ com os fatos citados (F10, F12). Correção possível: (i) citar F11 como suporte, ou (ii) reescrever para ‘elemento final modulante/proporcional (não liga-desliga)’ sem afirmar ‘posicionamento contínuo’ explicitamente.
- **o3-petrobras:medium:** aprova
- **gpt-5-4-petrobras:medium:** aprova
- **gpt-5-petrobras:medium:** aprova

### d21b4ace38-b0-A1 · facil · Manutenção e Plano de Manutenção

**P:** O que a FMEA/FMECA deve identificar em equipamentos críticos e por que a análise precisa avançar da função e da falha funcional até os modos, efeitos e consequências da falha?

**R:** Em equipamentos críticos, a FMEA/FMECA deve identificar os modos de falha e de deterioração. A análise precisa começar pela função e pelo padrão de desempenho esperado, passar pelas falhas funcionais, detalhar os modos de falha e suas causas, listar os efeitos e analisar as consequências, porque esse encadeamento mostra como a perda de função ocorre no ativo e qual impacto ela produz. Sem detalhar a causa de cada modo de falha, a manutenção tende a agir sobre sintomas, e não sobre o mecanismo real da falha. Ao avançar até efeitos e consequências, a análise cria base técnica para decisões de manutenção coerentes com a função do equipamento e com a criticidade da falha.

- **gpt-5-2-petrobras:medium:** reprova (suporte) · Falta de suporte: a afirmação sobre a análise 'criar base técnica para decisões de manutenção coerentes com a criticidade' não está sustentada pelos fatos citados (F1, F2). Seria necessário apoio explícito (p.ex., F3/F4/F5), mas eles não foram citados na questão.
- **o3-petrobras:medium:** aprova
- **gpt-5-4-petrobras:medium:** reprova (suporte) · A resposta acrescenta uma conclusão não integralmente suportada pelos fatos citados: 'criticidade da falha'.; A formulação final mistura consequência da falha com criticidade sem lastro explícito em F1-F2.
- **gpt-5-petrobras:medium:** reprova (suporte) · Menção a 'criticidade da falha' não está suportada por F1 e F2; substituir por 'consequências da falha' (suportado por F2) resolveria o problema de suporte.

### d21b4ace38-b1-A1 · dificil_A · Manutenção e Plano de Manutenção

**P:** Após manutenção em um sistema de armazenamento, o supervisório indica barreiras disponíveis e níveis coerentes com operação normal. Na inspeção de campo, a equipe encontra uma válvula crítica fora da posição normal, um ponto de sangria sem tampa e dúvida se o arranjo atual dos tanques corresponde à condição de projeto prevista para operação. A produção poderia ser mantida com monitoramento reforçado enquanto se corrige o restante, ou o retorno ao serviço deve ser bloqueado? Justifique tecnicamente.

**R:** O retorno ao serviço deve ser bloqueado até confirmar a recomposição física do sistema e a aderência do arranjo à condição de projeto. A disponibilidade aparente de barreiras não se confirma apenas pelo supervisório; ela precisa ser verificada fisicamente e/ou no sistema de supervisão, com coerência entre as evidências. Após manutenção, a checagem visual deve confirmar conclusão das atividades, equipamento conforme o projeto, remoção de isolamentos temporários, retorno de válvulas críticas, posicionamento correto de vents e drains, presença de tampas em pontos de sangria e alinhamento de dispositivos protetivos instrumentados. Além disso, no sistema de armazenamento, a comparação entre condição operacional e condição de projeto faz parte da verificação. Manter produção só seria defensável se houvesse contingências suficientes para manter o risco em nível aceitável; quando há degradação ou indisponibilidade de elementos críticos, essas contingências podem exigir parada do equipamento, do sistema ou da planta.

- **gpt-5-2-petrobras:medium:** reprova (jurisdicao) · Jurisdição/força normativa: uso de orientação HSE (UK) com linguagem de obrigação ('deve') sem qualificar como boa prática ou sem separar do que é requisito ANP (BR). Ajuste redacional resolveria sem alterar o conteúdo técnico.
- **o3-petrobras:medium:** aprova
- **gpt-5-4-petrobras:medium:** aprova
- **gpt-5-petrobras:medium:** aprova

### 3204097d51-b0-A1 · facil · Condições Ambientais e Impactos Operacionais

**P:** Por que a falha de um riser caracteriza uma perda de contenção com potencial de liberação de hidrocarbonetos ao ambiente marinho?

**R:** Porque o riser transporta hidrocarbonetos e, quando falha, perde a capacidade de manter esse inventário confinado, permitindo a descarga do produto no mar. Esse potencial de liberação é especialmente relevante quando o escoamento inclui, além do petróleo, gases residuais e compostos corrosivos associados ao fluido produzido, pois a falha passa a ter consequência direta de contaminação ambiental pela saída do conteúdo transportado para o ambiente marinho.

- **gpt-5-2-petrobras:medium:** reprova (suporte) · Suporte insuficiente com os fatos citados: 'transporta hidrocarbonetos' e 'contaminação ambiental' não estão sustentados por F1; exigiriam ajuste de redação para ficar estritamente em 'liberação ao ambiente' ou inclusão de fatos adicionais (ex.: F3).
- **o3-petrobras:medium:** aprova
- **gpt-5-4-petrobras:medium:** aprova
- **gpt-5-petrobras:medium:** aprova

### 3204097d51-b0-A2 · media · Condições Ambientais e Impactos Operacionais

**P:** Em uma ruptura total de riser flexível no trecho submerso, como o evento pode evoluir de dano localizado para um cenário de maior severidade operacional e ambiental?

**R:** A ruptura pode deixar de ser um dano restrito ao próprio riser quando o evento passa a ameaçar estruturas e risers adjacentes, provocando novos rompimentos e ampliando a liberação de óleo para o mar. Nessa condição, a severidade aumenta porque o acidente combina perda de contenção inicial, propagação do dano físico na instalação e maior volume potencial de hidrocarbonetos no ambiente. O impacto também deixa de ser apenas local quando a pluma pode se dispersar para áreas ambientalmente sensíveis, como praias e manguezais, exigindo avaliar ao mesmo tempo o escalonamento mecânico da falha e a dispersão do poluente.

- **gpt-5-2-petrobras:medium:** reprova (suporte) · Falta de suporte explícito para 'maior volume potencial de hidrocarbonetos' (não declarado em F2/F3).; Falta de suporte explícito (nos F# citados no item) para a conclusão prescritiva 'exigindo avaliar ao mesmo tempo...' — está alinhada ao texto da nota, mas não está ancorada em F2/F3 no item.; Correção possível: remover/atenuar as afirmações sem suporte ou incluir fatos que as sustentem (p.ex., conectar à avaliação de consequências/dispersão conforme material).
- **o3-petrobras:medium:** aprova
- **gpt-5-4-petrobras:medium:** aprova
- **gpt-5-petrobras:medium:** aprova

### 3204097d51-b1-A1 · dificil_A · Condições Ambientais e Impactos Operacionais

**P:** Em um compartimento interno de uma unidade offshore, um detector de gás será instalado próximo à exaustão. A carga do processo varia ao longo do dia, alterando o aquecimento local, e a equipe quer validar se um instrumento selecionado pela condição climática externa continua adequado. Como deve ser feita essa avaliação de adequação, considerando temperatura local, composição do fundo gasoso, ventilação e regime de exposição do sensor?

**R:** A adequação não deve ser julgada pela temperatura externa, mas pela condição real do ponto monitorado, por ser um ambiente interno e influenciado pela exaustão. A avaliação deve considerar o processo monitorado e o regime operacional efetivo, incluindo variações térmicas ao longo do dia e entre condições sazonais, porque essas mudanças podem deslocar a faixa de valores observada e afetar o fundo de escala requerido. Portanto, o critério correto é verificar se o sistema permanece compatível com as condições locais mais severas e fora do regime normal, no ponto onde o sensor ficará exposto. Como a atmosfera real do local é a referência de projeto, a composição do fundo gasoso e a ventilação do ponto não podem ser tratadas por aproximação climática geral; elas precisam ser caracterizadas no próprio ambiente de instalação antes de confirmar a adequação do sistema.

- **gpt-5-2-petrobras:medium:** reprova (correcao_tecnica, suporte, sem_generalizacao) · Falta de suporte: composição de fundo gasoso, ventilação e regime de exposição do sensor não são cobertos pelo fato F1 citado.; Critério 'condições mais severas/fora do normal' e exigência de 'caracterização' local dessas variáveis não estão demonstrados no material factual fornecido (F1).; Generalização indevida de requisitos não suportados (caracterização de fundo/ventilação como regra).
- **o3-petrobras:medium:** aprova
- **gpt-5-4-petrobras:medium:** aprova
- **gpt-5-petrobras:medium:** aprova

### 3204097d51-b2-A1 · dificil_B · Condições Ambientais e Impactos Operacionais

**P:** Em um módulo de processo de FPSO, alarmes intermitentes de gás surgem principalmente durante mudanças de regime e aumento de temperatura local. As rondas não confirmam atmosfera perigosa persistente, mas há obstáculos e zonas pouco ventiladas; a equipe começa a tratar os alarmes como espúrios. Qual diagnóstico técnico integrado deve orientar a decisão operacional sobre esses alarmes?

**R:** A interpretação mais robusta é que os alarmes não devem ser classificados de imediato nem como pseudoalarmes puros nem como vazamento confirmado uniforme. Eles podem resultar de acúmulo real e transitório da pluma em zonas de recirculação criadas por geometria e vento, onde concentração local depende de mistura turbulenta e transporte vertical, ou de inadequação do monitoramento sob a temperatura efetiva, umidade e composição gasosa reais do ponto medido, incluindo interferência por gases espúrios. Como essas causas produzem aparência semelhante de perda de prontidão, a decisão correta é manter a credibilidade da barreira e separar as hipóteses verificando conjuntamente dispersão local, temperatura/composição do ambiente monitorado e regime de exposição do sensor. Também é necessário revisar a configuração de alarmes e a resposta automática associada, porque pseudoalarmes e atrasos na atuação de ventilação/shutdown podem aumentar o tempo de resposta e favorecer propagação para áreas ocupadas.

- **gpt-5-2-petrobras:medium:** reprova (suporte) · Falta de suporte: a menção a 'umidade' (e, por implicação, efeitos associados) não está respaldada pelos fatos citados. Ajuste possível: remover 'umidade' ou substituir por elementos suportados (temperatura local, composição/interferentes, regime de exposição, pseudoalarmes, HVAC/ventilação).; Suporte: algumas expressões gerais ('manter a credibilidade da barreira') são aceitáveis como linguagem operacional, mas idealmente deveriam ser ancoradas explicitamente nos efeitos de pseudoalarmes/tempo de resposta (F19) para evitar parecer prescritivo sem base.
- **o3-petrobras:medium:** aprova
- **gpt-5-4-petrobras:medium:** reprova (suporte) · A resposta inclui 'umidade' sem F# de suporte explícito no material estruturado.; A formulação 'manter a credibilidade da barreira' é prescritiva e não está ancorada diretamente em um fato citado.; Como há falta de suporte em afirmações substantivas, a questão reprova em suporte mesmo sendo tecnicamente boa no conjunto.
- **gpt-5-petrobras:medium:** aprova

### 7408dc2a56-b0-A1 · facil · Gestão de Pessoas e Treinamento

**P:** Qual é a diferença entre uma matriz de treinamentos mandatórios gerais e uma matriz de treinamentos em procedimentos operacionais por função, e o que cada uma comprova ou não comprova?

**R:** A matriz de treinamentos mandatórios gerais comprova a cobertura de cursos obrigatórios formais e documentados aplicáveis à força de trabalho, com evidência rastreável do que foi realizado. Isso ajuda a demonstrar atendimento a exigências gerais de treinamento, mas não comprova, por si só, que cada trabalhador foi treinado nos procedimentos operacionais específicos da atividade que executa. Já a matriz de treinamentos em procedimentos operacionais por função relaciona as necessidades de capacitação ao cargo e à execução real das tarefas, permitindo demonstrar treinamento adequado ao exercício da função. Sem essa matriz específica e sem registros correspondentes, a organização não consegue provar competência operacional por função nem distinguir adequadamente lacunas entre ocupantes do mesmo cargo.

- **gpt-5-2-petrobras:medium:** reprova (correcao_tecnica, suporte) · Uso de 'comprova' e 'evidência rastreável do que foi realizado' para a matriz de mandatórios sem suporte explícito em F8/F9/F2.; Atribuição de 'formal e documentado' aos cursos/matriz de mandatórios sem ligação suportada: F1 traz um requisito geral de formalidade/documentação, mas não demonstra que a matriz mandatória (citada em F8) cumpre isso ou que a matriz por si comprova execução.; Parte da descrição da matriz por função pode ser mantida, mas deve ser ancorada mais diretamente em F2 (evidência de treinamento adequado à função) e em F8/F9 (ausência de matriz/registros de procedimentos operacionais).
- **o3-petrobras:medium:** aprova
- **gpt-5-4-petrobras:medium:** reprova (correcao_tecnica, suporte) · Confunde a função da matriz com a função dos registros de treinamento.; Atribui à matriz, isoladamente, a comprovação do treinamento realizado.; Suporte parcial para a ideia de que a matriz por função, sem explicitar a necessidade de registros, demonstra competência adequada.
- **gpt-5-petrobras:medium:** aprova

### 7408dc2a56-b0-A2 · media · Gestão de Pessoas e Treinamento

**P:** Em uma unidade offshore, a matriz de treinamento existe, mas não acompanha mudanças de pessoal, experiência e requisitos operacionais. Como isso afeta a verificação das competências, a escalação de pessoal e a demonstração de conformidade?

**R:** A matriz atualizada é o instrumento que deve refletir o status real das competências, permitindo verificar se os requisitos de cada função continuam atendidos. Quando ela não acompanha a situação real, perde a capacidade de mostrar quem está efetivamente apto, dificultando a alocação segura de pessoal para atividades e funções específicas. Isso também compromete a demonstração de que a força de trabalho recebeu treinamento adequado e de que o operador consegue verificar periodicamente esse atendimento. Em auditorias ou investigações, uma matriz desatualizada pode aparentar cobertura sem evidenciar competência vigente, criando falsa sensação de conformidade. Além disso, a revisão do programa deixa de capturar necessidades associadas a pessoal pouco experiente, treinamento prático específico da instalação e inclusão de novos temas ou tecnologias.

- **gpt-5-2-petrobras:medium:** reprova (suporte) · Falta suporte factual explícito para a afirmação sobre impacto na escalação/alocação segura de pessoal; os fatos fornecidos tratam de evidência/checagem de treinamento (F2), necessidade de matriz refletir status real (F4) e revisão do programa (F6), mas não mencionam escalação/alocação.; Para ficar plenamente suportada com o mesmo material, a resposta deve reformular a parte de 'escalação/alocação segura' para algo diretamente ancorado em F2/F4 (ex.: dificuldade de demonstrar/confirmar atendimento aos requisitos de competência por função), ou remover essa afirmação.
- **o3-petrobras:medium:** aprova
- **gpt-5-4-petrobras:medium:** reprova (correcao_tecnica, suporte) · A resposta introduz 'alocação segura de pessoal' sem fato explícito que sustente essa consequência.; A relação causal entre matriz desatualizada e falha necessária da revisão do programa está mais forte do que o material permite afirmar.; Parte da conclusão sobre 'falsa sensação de conformidade' é plausível, mas excede o suporte literal disponível.
- **gpt-5-petrobras:medium:** aprova

### 7408dc2a56-b1-A1 · dificil_A · Gestão de Pessoas e Treinamento

**P:** Em um FPSO, o mesmo cargo cobre operação de utilidades e apoio ao tratamento de gás, mas as descrições de função trazem requisitos genéricos. A empresa mantém registros de treinamento válidos, porém não possui critérios formais para designar supervisores de turno com responsabilidade de liderança, e parte da equipe executa procedimentos já desatualizados. Sem evidência de redução de efetivo, qual causa predominante deve ser diagnosticada: definição insuficiente do padrão da função, qualificação inadequada para o papel, suficiência de recursos ou avaliação de competência?

**R:** A causa predominante é definição insuficiente do padrão da função. Os sinais mais fortes estão a montante da qualificação: requisitos genéricos nas descrições de função, ausência de critérios formais para supervisão e acúmulo de funções no mesmo cargo sem matriz específica por função. Em instalações offshore, os requisitos de formação, experiência, habilidades e treinamento devem ser definidos para cada função, e, quando um cargo exerce funções distintas, o treinamento deve ser tratado por matriz específica. Para funções operacionais e posições-chave, o padrão deve vincular responsabilidades, tarefas, procedimentos e tarefas críticas de segurança; quando não houver requisito externo detalhado, o operador deve estabelecer seu próprio padrão. A execução com procedimentos desatualizados agrava o desvio, mas, com treinamentos formalmente válidos e sem evidência de insuficiência de efetivo, o problema principal é que o referencial da função está mal definido, o que contamina seleção, treinamento e atuação.

- **gpt-5-2-petrobras:medium:** reprova (correcao_tecnica, suporte, jurisdicao) · Ambiguidade diagnóstica: sintomas suportam mais de uma alternativa (padrão de função vs. qualificação/seleção de supervisores vs. gestão/atualização de procedimentos), mas a questão força uma única “causa predominante” sem critério adicional.; Falta de suporte: a resposta infere “sem matriz específica” e uma cadeia causal (“contamina seleção, treinamento e atuação”) que não está explicitada nos fatos citados nem no enunciado.; Jurisdição: uso de orientação HSE/UK (F7) como obrigação (“deve”) para FPSO, sem qualificar como boa prática/orientação e sem base normativa aplicável ao caso.
- **o3-petrobras:medium:** aprova
- **gpt-5-4-petrobras:medium:** reprova (suporte, jurisdicao) · A resposta infere 'sem matriz específica por função', mas a pergunta não informa isso.; O detalhamento de F7 (HSE/UK) foi usado como obrigação geral, sem ressalva de contexto regulatório.; Registros válidos de treinamento não eliminam, por si só, deficiência de avaliação de competência; a exclusão dessa causa ficou sem suporte suficiente.
- **gpt-5-petrobras:medium:** reprova (suporte) · Afirmação sem suporte direto em F#: 'A execução com procedimentos desatualizados agrava o desvio'.

### 7408dc2a56-b2-A1 · dificil_B · Gestão de Pessoas e Treinamento

**P:** Em um FPSO, a equipe própria e contratada está com certificados e reciclagens periódicas em dia, e a maioria foi aprovada em avaliações gerais. Mesmo assim, em exercícios de mesa e observações de campo aparecem erros repetidos em partes específicas de procedimentos críticos, sobretudo em tarefas pouco frequentes. Qual revisão do sistema de treinamento e avaliação melhor demonstra eficácia real do treinamento e reduz o risco de liberar pessoas apenas “documentalmente competentes”?

**R:** A revisão deve sair da comprovação documental e da nota global para um assurance por função, baseado em evidências múltiplas e proporcionais à criticidade. Certificados, curso concluído e aprovação geral não bastam para provar competência mantida. Para procedimentos críticos, a avaliação deve combinar teste de conhecimento, observação prática da execução e cenários/exercícios de mesa, com registro de evidências. As lacunas precisam ser identificadas por área ou seção da tarefa, para aplicar treinamento adicional dirigido e, depois, reavaliar somente o trecho deficiente. Em tarefas pouco frequentes, a reciclagem deve ser mais frequente ou pré-tarefa. Como há pessoal contratado, a verificação não pode ficar só na pré-mobilização: deve ocorrer no início do contrato e durante a operação. O sistema também deve monitorar desempenho e reavaliar áreas-chave continuamente antes de ampliar escopo ou manter liberação para a função.

- **gpt-5-2-petrobras:medium:** reprova (suporte) · Falta suporte explícito (com os fatos citados) para a afirmação sobre 'nota global/aprovação geral' como insuficientes; para sustentar isso, seria necessário citar material que trate de análise por tópico/seção (p.ex., F13/F15 ou equivalentes da Nota 2).; A expressão 'antes de ampliar escopo' introduz um critério decisório não presente nos fatos citados; pode ser removida ou substituída por formulação suportada (p.ex., manter liberação condicionada a reassessment/monitoramento — F24).
- **o3-petrobras:medium:** aprova
- **gpt-5-4-petrobras:medium:** aprova
- **gpt-5-petrobras:medium:** aprova

### ba30ee0893-b0-A1 · facil · Meio Ambiente, Gestão Ambiental e Sustentabilidade

**P:** Qual é a função de sistemas rigorosos de gestão de saúde, segurança, social e ambiental na operação offshore com potencial de impacto ao ambiente marinho?

**R:** Esses sistemas fornecem a base para avaliar e minimizar os riscos das operações e para estruturar processos que reduzam os impactos negativos ao ambiente marinho. Na prática, sua função é transformar a proteção ambiental em prevenção e controle operacionais, sustentando a identificação de riscos e a adoção de medidas para reduzir efeitos como poluição e outros impactos associados à atividade offshore.

- **gpt-5-2-petrobras:medium:** reprova (suporte) · Falta de suporte: parte final da resposta adiciona funções/mecanismos e exemplos (prevenção/controle operacionais; identificação de riscos; poluição) que não estão explicitados no F1 citado.; Para ficar suportada, a resposta deve limitar-se ao que o F1 afirma (capacidade de avaliar/minimizar riscos e desenvolver processos para reduzir impactos negativos ao meio marinho) ou citar fatos adicionais que suportem os detalhes.
- **o3-petrobras:medium:** aprova
- **gpt-5-4-petrobras:medium:** reprova (suporte) · A resposta contém extrapolações sem suporte explícito nos fatos, especialmente 'transformar a proteção ambiental em prevenção e controle operacionais'.; A menção específica a 'poluição' não está sustentada pelo fato citado F1.
- **gpt-5-petrobras:medium:** aprova

### ba30ee0893-b2-A1 · dificil_B · Meio Ambiente, Gestão Ambiental e Sustentabilidade

**P:** Em uma auditoria interna de um FPSO, a operação sustenta que o descarte de água produzida está sob controle porque o TOG medido em linha permanece estável e é usado para ajustar o tratamento. Porém, a revisão do licenciamento e dos relatórios enviados ao órgão ambiental indica possível desalinhamento entre a condicionante de descarte e o método analítico reportado. Qual é o diagnóstico técnico mais provável e qual deve ser a prioridade de ação?

**R:** O diagnóstico mais provável é de falsa conformidade. TOG em linha pode ser um bom indicador operacional para controlar o processo e acompanhar a água descartada, mas isso não prova, por si só, atendimento à condicionante se o parâmetro e o método exigidos no licenciamento forem outros. No Brasil, o descarte ao meio ambiente pode estar vinculado a óleo e graxas por método gravimétrico; já TOG e seus critérios aparecem em outras condições de aplicação. Portanto, antes de concluir que o problema é do tratamento, é preciso verificar a coerência entre licença, jurisdição, parâmetro, método analítico, amostragem e reporte. A prioridade é tratar o desvio como não conformidade de gestão e evidência regulatória: revisar os requisitos aplicáveis e os documentos de licenciamento, corrigir o plano de monitoramento e reporte, definir responsáveis e prazos proporcionais ao risco e manter o indicador em linha apenas como apoio operacional, não como evidência formal isolada.

- **gpt-5-2-petrobras:medium:** reprova (suporte) · Falta de suporte explícito para prescrições sobre 'plano de monitoramento e reporte' (reporte/comprovação formal) e para a afirmação normativa de que TOG em linha não deve ser usado como 'evidência formal isolada'.; Para ficar 100% suportada, a resposta deve ser reescrita para se limitar ao que os fatos afirmam: (i) necessidade de avaliar e cumprir restrições/exigências do licenciamento; (ii) diferença de parâmetro/método entre IBAMA/CONAMA (óleo e graxas gravimétrico) e IMO (TOG); (iii) tratamento formal de não conformidades com plano de ação proporcional ao risco.
- **o3-petrobras:medium:** aprova
- **gpt-5-4-petrobras:medium:** reprova (suporte) · Suporte parcial: 'amostragem' e 'reporte' são introduzidos sem fato específico correspondente.; Suporte insuficiente para a formulação categórica de que o indicador em linha não pode servir como 'evidência formal isolada'; o material sustenta a distinção entre uso operacional e critério regulatório, mas não com essa redação normativa exata.; A resposta poderia limitar-se ao que está explicitamente suportado: revisão de requisitos/licença, verificação de parâmetro e método aplicáveis e tratamento formal da não conformidade com responsáveis e prazos proporcionais ao risco.
- **gpt-5-petrobras:medium:** aprova

### b8c888d001-b0-A1 · facil · Saúde Ocupacional

**P:** Qual é a função de um programa de vigilância médica ocupacional em ambiente offshore além do acompanhamento clínico individual?

**R:** É transformar sinais de adoecimento em controle efetivo do risco para as pessoas e para a operação. Isso exige que preocupações com doença sejam reportadas e investigadas, com definição de ação corretiva para prevenir recorrência, em vez de apenas registrar casos. Em surtos ou pandemias, o programa também precisa sustentar decisões operacionais com base em informações como POB (pessoas a bordo), casos suspeitos, contactantes e óbitos, além de prever medidas para a ausência de profissionais-chave. Por isso, a vigilância médica offshore conecta monitoramento de saúde, gestão de casos, medidas de contenção e continuidade operacional segura, especialmente quando a indisponibilidade de lideranças, equipe médica ou técnicos de segurança pode degradar a capacidade de resposta da instalação.

- **gpt-5-2-petrobras:medium:** reprova (suporte, jurisdicao, sem_generalizacao) · Falta de suporte explícito para a afirmação de que os dados (POB/suspeitos/contactantes/óbitos) são usados como base para decisões operacionais; F3 apenas registra que houve troca desses dados, sem estabelecer o vínculo decisório.; Uso de linguagem normativa geral ('Isso exige...') apoiada em fonte HSE (UK) sem qualificação, gerando problema de jurisdição/generalização.; A resposta menciona 'gestão de casos' e 'medidas de contenção' sem que a questão tenha citado F6; mesmo existindo na nota, o conjunto de fatos referenciado na questão não sustenta essa parte da resposta.
- **o3-petrobras:medium:** aprova
- **gpt-5-4-petrobras:medium:** aprova
- **gpt-5-petrobras:medium:** aprova

### b8c888d001-b1-A1 · dificil_A · Saúde Ocupacional

**P:** Em uma unidade offshore, dois trabalhadores foram afastados no mesmo turno. Um apresentou febre e tosse após conviver com a equipe em área comum; o outro foi retirado da atividade porque a tarefa estava sendo executada em condição operacional insegura e em ambiente fora do padrão operacional. Se a equipe de gestão precisar definir a prioridade técnica de tratamento de cada afastamento, qual deve ser o foco principal em cada caso?

**R:** No caso com febre e tosse, a prioridade deve recair no controle do caso infeccioso. Isso exige tratar o evento como processo operacional controlado, com monitoramento de saúde, isolamento, impedimento de circulação do trabalhador suspeito ou potencialmente infectado, comunicação clara ao pessoal, sanitização, manejo do caso e retorno ao trabalho. Já no afastamento ligado à condição operacional insegura e ao ambiente em desconformidade, a prioridade é corrigir a condição operacional que sustenta o afastamento, porque esse tipo de ocorrência aparece como consequência de falhas do contexto operacional. Tratar ambos os afastamentos da mesma forma reduz a efetividade da resposta: no primeiro, o risco central é propagação e convivência a bordo; no segundo, o problema central é a condição de operação e de conformidade do ambiente de trabalho.

- **gpt-5-2-petrobras:medium:** reprova (suporte) · Falta de suporte: a resposta inclui afirmações não sustentadas por F1/F2 (p.ex., ‘risco central é propagação e convivência’ e ‘tratar ambos da mesma forma reduz a efetividade’).; Para ficar suportada, a resposta pode ser reescrita mantendo apenas o que F1 e F2 afirmam explicitamente (elementos do protocolo infeccioso e a ligação dos afastamentos a condições operacionais inseguras/ambiente fora de padrão), sem acrescentar conclusões não citadas.
- **o3-petrobras:medium:** aprova
- **gpt-5-4-petrobras:medium:** aprova
- **gpt-5-petrobras:medium:** aprova

### b8c888d001-b2-A1 · dificil_B · Saúde Ocupacional

**P:** Após bunkering recente de água, 12% do efetivo de um FPSO apresenta sintomas gastrointestinais em poucas horas. Os casos estão em setores diferentes; parte não consumiu a mesma refeição, mas todos usaram água das áreas de vivência. No mesmo período houve falha temporária de refrigeração na cozinha. Qual trilha de investigação e contenção deve ser priorizada para decidir a resposta inicial sem perder a segurança operacional?

**R:** Trate o evento como emergência sanitária coletiva por fonte comum potencial. Como os casos não se concentram em uma única refeição e todos compartilharam a água de vivência, a água potável deve entrar como hipótese prioritária, sem descartar alimento: verifique imediatamente a integridade do abastecimento recente, incluindo higiene sanitária de mangueiras e conexões de bunkering, além de acionar a contingência para suspeita de falta ou contaminação da água. Em paralelo, acione a contingência de falha de refrigeração e de surto transmitido por alimentos, porque a conservação inadequada também pode ter sido vetor. A resposta inicial deve combinar contenção clínica e epidemiológica com isolamento dos casos, rastreamento de contatos, tratamento sintomático e, se necessário, evacuação. Como 12% do efetivo foi atingido, reavalie a normalidade operacional e o efetivo mínimo para operar com segurança, além de comunicar o evento conforme o gatilho aplicável no Brasil.

- **gpt-5-2-petrobras:medium:** reprova (correcao_tecnica, suporte, jurisdicao, sem_generalizacao) · Afirmação de priorização da água potável por lógica ‘refeição vs água’ não está explicitamente sustentada pelos F# citados (é uma inferência plausível, mas a exigência aqui é suporte explícito).; Elementos de resposta clínica (isolamento, rastreamento, evacuação) aparecem em F12 como descrição de planos na jurisdição US (BSEE), mas foram redigidos como obrigação geral (‘deve’), gerando falha de jurisdição e generalização.; Introdução de ‘efetivo mínimo para operar com segurança’ não tem suporte em F1/F8/F10/F12/F13; precisaria ser removido ou fundamentado por fato fornecido.
- **o3-petrobras:medium:** aprova
- **gpt-5-4-petrobras:medium:** reprova (suporte, sem_generalizacao) · Suporte insuficiente para prescrever isolamento/rastreamento/evacuação como resposta inicial obrigatória; F12 é exemplo de planos na jurisdição dos EUA, não regra geral.; Generalização indevida de observação particular da BSEE para conduta universal.; A menção a 'efetivo mínimo para operar com segurança' não está explicitamente sustentada pelos fatos literais citados para a questão.
- **gpt-5-petrobras:medium:** reprova (suporte) · Afirmação sobre priorizar água como hipótese principal carece de suporte explícito em Fatos.; A menção a reavaliar 'efetivo mínimo' não está explicitamente suportada por F11 ou outro Fato.; Uso do termo 'emergência sanitária coletiva' é adequado em sentido geral, mas a priorização específica não é referenciada por F#.

### c3419532e4-b0-A1 · facil · Segurança Ocupacional

**P:** Quais são os principais perigos que devem ser considerados em solda, corte e outros trabalhos a quente em ambiente industrial ou offshore?

**R:** Os principais perigos incluem queimaduras por exposição térmica direta, ignição quando há vapores inflamáveis na área, inalação de gases, fumos e vapores, choque elétrico, luminosidade excessiva do arco de solda e projeção de fagulhas ou partículas/projéteis oriundos do corte. Em alguns contextos, também pode haver risco de explosão de cilindros de oxigênio. Esses mecanismos podem ocorrer simultaneamente, por isso a atividade não deve ser tratada como risco único.

- **gpt-5-2-petrobras:medium:** reprova (suporte) · Falta de suporte: as frases finais sobre simultaneidade e a conclusão 'não deve ser tratada como risco único' não estão sustentadas pelos F# citados (nem há F# no enunciado fornecendo essa relação).; Reparo possível removendo essas frases finais ou substituindo por formulação estritamente descritiva dos perigos listados, mantendo apenas o que está coberto por F1/F2/F3.
- **o3-petrobras:medium:** aprova
- **gpt-5-4-petrobras:medium:** reprova (suporte) · As duas frases finais da resposta não têm suporte explícito nos F# citados pela questão.; A questão cita F3, que é de jurisdição US; isso não invalida a resposta, mas exige cuidado para não derivar obrigação normativa a partir dele.
- **gpt-5-petrobras:medium:** aprova

### c3419532e4-b0-A2 · media · Segurança Ocupacional

**P:** Em um serviço de solda executado em plataforma, com possibilidade de flash fire, exposição ao arco elétrico e trabalho em desnível, como cada EPI deve ser relacionado ao mecanismo de dano que controla?

**R:** A roupa resistente ao fogo é indicada para reduzir a severidade do dano térmico e os efeitos de um possível flash fire. O capacete de soldagem com tonalidade adequada serve para atenuar a luminosidade excessiva associada à solda elétrica. A proteção contra quedas controla o risco adicional de trabalho em desnível, especialmente se um evento térmico súbito provocar reação intempestiva ou perda de equilíbrio. A escolha do EPI, portanto, deve cobrir simultaneamente risco térmico, ocular e de queda.

- **gpt-5-2-petrobras:medium:** reprova (suporte) · Falta de suporte para a relação causal 'evento térmico súbito -> reação/perda de equilíbrio' com os fatos citados (F2, F5). Remover ou reescrever sem essa justificativa específica resolve com o mesmo material.
- **o3-petrobras:medium:** aprova
- **gpt-5-4-petrobras:medium:** aprova
- **gpt-5-petrobras:medium:** aprova

## Defeitos plantados que passaram

- **o3-petrobras:medium** aprovou `1c3beb869e-b0-A1::dependencia_fonte` (dependencia_fonte): A pergunta foi reescrita para depender de conhecimento de um documento específico, ao mencionar 'o relatório operacional da unidade', o que a torna respondível apenas por quem conhece essa fonte.
- **o3-petrobras:medium** aprovou `26d45ade58-b0-A2::dependencia_fonte` (dependencia_fonte): A pergunta foi reescrita para depender de conhecimento de um caso específico — o içamento crítico com o Offshore Construction Manager chamado para fora da área e sem cópia física do Lift Plan — em vez de poder ser respondida apenas pelos princípios gerais.
- **o3-petrobras:medium** aprovou `3204097d51-b0-A1::dependencia_fonte` (dependencia_fonte): A pergunta foi reescrita para depender de uma fonte específica, ao restringi-la ao caso da análise de risco da P-52, o que exige conhecimento desse documento/caso para responder.
- **o3-petrobras:medium** aprovou `3b9ff23e32-b0-A2::dependencia_fonte` (dependencia_fonte): A pergunta foi reescrita para depender do conhecimento de um arranjo/documento específico ao mencionar explicitamente a unidade com LP inlet separator e os controladores FIC-2, FIC-3 e FIC-4, em vez de poder ser respondida apenas pelos conceitos gerais.
- **o3-petrobras:medium** aprovou `3204097d51-b2-A1::erro_tecnico` (erro_tecnico): Foi alterada a relação técnica final: a resposta passa a afirmar erroneamente que pseudoalarmes e atrasos na ventilação/shutdown reduzem o tempo de resposta e dificultam a propagação, quando o material sustenta o contrário.
- **o3-petrobras:medium** aprovou `3204097d51-b2-A1::dependencia_fonte` (dependencia_fonte): A pergunta foi reescrita para depender de uma fonte específica, ao ancorar a resposta em 'o caso analisado pela HSE', o que exige conhecimento desse caso/documento e não apenas dos fatos gerais.
- **o3-petrobras:medium** aprovou `470390a408-b0-A2::dependencia_fonte` (dependencia_fonte): A pergunta foi reescrita para depender de um estudo específico sobre qualidade de potência e modos operacionais de navios, exigindo conhecimento dessa fonte externa para ser respondida adequadamente.
- **o3-petrobras:medium** aprovou `470390a408-b2-A1::dependencia_fonte` (dependencia_fonte): A pergunta foi reescrita para depender do conhecimento de um documento específico, ao mencionar explicitamente 'o relatório da P-34' e o caso nele analisado, tornando a resposta dependente dessa fonte.
- **o3-petrobras:medium** aprovou `567fdce5c3-b1-A1::dependencia_fonte` (dependencia_fonte): A pergunta foi reescrita para depender de conhecimento de uma ocorrência e investigação específicas da ANP sobre o rompimento do QRF/IHTP, em vez de poder ser respondida apenas pelos fatos gerais apresentados.
- **o3-petrobras:medium** aprovou `4e96c8ab4a-b2-A1::dependencia_fonte` (dependencia_fonte): A pergunta foi reescrita para depender de conhecimento de um caso e de configurações específicas da unidade SSAO, criando dependência de fonte externa para contextualização da resposta.
- **o3-petrobras:medium** aprovou `567fdce5c3-b2-A1::dependencia_fonte` (dependencia_fonte): A pergunta foi reescrita para depender do conhecimento de casos e documentos específicos — a investigação do FPSO Cidade de São Mateus e um estudo do Reino Unido sobre stability computer — em vez de poder ser respondida apenas com conhecimento técnico geral e os fatos apresentados.
- **o3-petrobras:medium** aprovou `62e43c1988-b1-A1::dependencia_fonte` (dependencia_fonte): A pergunta foi reescrita para depender de um documento específico — um relatório de integridade de ancoragem de 2019 da campanha de aumento de cargas ambientais — de modo que só quem conhece essa fonte consegue responder diretamente.
- **o3-petrobras:medium** aprovou `86765f00dc-b0-A1::dependencia_fonte` (dependencia_fonte): A pergunta foi reescrita para depender de conhecimento de uma fonte específica — o guia de inspeção da HSE para proof testing em SIS — em vez de poder ser respondida apenas com base no enunciado geral do tema.
- **o3-petrobras:medium** aprovou `6fffbf5758-b2-A1::dependencia_fonte` (dependencia_fonte): A pergunta foi reescrita para depender de conhecimento de um caso/documento específico — o safety case da instalação analisada — em vez de poder ser respondida apenas com os fatos gerais fornecidos.
- **o3-petrobras:medium** aprovou `86765f00dc-b0-A2::dependencia_fonte` (dependencia_fonte): A pergunta foi reescrita para depender de conhecimento de uma referência específica — o guia de inspeção da HSE e a BS EN 61511-1:2017, cláusula 16.3.2 — em vez de poder ser respondida apenas pelos fatos gerais do enunciado.
- **o3-petrobras:medium** aprovou `b56db319e4-b0-A2::dependencia_fonte` (dependencia_fonte): A pergunta foi reescrita para depender do conhecimento de um caso/documento específico ao mencionar o arranjo operacional da SSDP PHI, tornando a resposta condicionada a essa fonte externa.
- **o3-petrobras:medium** aprovou `c3419532e4-b0-A2::dependencia_fonte` (dependencia_fonte): A pergunta foi reescrita para depender de um documento específico externo — um relatório de investigação da plataforma — em vez de poder ser respondida apenas com o conteúdo factual geral disponível.
- **o3-petrobras:medium** aprovou `d720962e6f-b0-A1::dependencia_fonte` (dependencia_fonte): A pergunta foi reescrita para depender de conhecimento de um relatório específico, o R-ADB-10-02, em vez de poder ser respondida apenas com o conhecimento técnico geral expresso nos fatos.
- **o3-petrobras:medium** aprovou `d720962e6f-b0-A2::dependencia_fonte` (dependencia_fonte): A pergunta foi reescrita para depender do conhecimento de uma fonte específica, ao vincular a resposta ao caso apresentado nas “Guidelines for Engineering Design for Process Safety”.
- **o3-petrobras:medium** aprovou `d720962e6f-b1-A1::dependencia_fonte` (dependencia_fonte): A pergunta foi reescrita para depender do conhecimento de um caso/documento específico (NC_040_SSM_2022-08), tornando a resposta dependente de fonte externa em vez de ser respondível apenas pelos fatos gerais apresentados.
- **o3-petrobras:medium** aprovou `e9ca515f84-b2-A1::dependencia_fonte` (dependencia_fonte): A pergunta foi reescrita para depender do conhecimento de uma análise/estudo específico ('a análise de integridade que modela a curva Δp̂ ... e combina essa leitura com a prática de anomaly management até close out'), em vez de poder ser respondida apenas com os fatos gerais.
- **o3-petrobras:medium** aprovou `fadd3bccc0-b1-A1::dependencia_fonte` (dependencia_fonte): A pergunta foi reescrita para depender de conhecimento de fontes específicas externas — o caso investigado pelo BSEE e o critério do HSE — em vez de ser respondível apenas pelo conteúdo factual geral apresentado.
- **gpt-5-petrobras:medium** aprovou `26d45ade58-b0-A2::dependencia_fonte` (dependencia_fonte): A pergunta foi reescrita para depender de conhecimento de um caso específico — o içamento crítico com o Offshore Construction Manager chamado para fora da área e sem cópia física do Lift Plan — em vez de poder ser respondida apenas pelos princípios gerais.
- **gpt-5-petrobras:medium** aprovou `3b9ff23e32-b0-A2::dependencia_fonte` (dependencia_fonte): A pergunta foi reescrita para depender do conhecimento de um arranjo/documento específico ao mencionar explicitamente a unidade com LP inlet separator e os controladores FIC-2, FIC-3 e FIC-4, em vez de poder ser respondida apenas pelos conceitos gerais.
- **gpt-5-petrobras:medium** aprovou `460979b6f3-b0-A1::dependencia_fonte` (dependencia_fonte): A pergunta foi reescrita para depender do conhecimento de documentos específicos, citando a API RP 580 e a API STD 581 como referência necessária para responder.
- **gpt-5-petrobras:medium** aprovou `470390a408-b0-A2::dependencia_fonte` (dependencia_fonte): A pergunta foi reescrita para depender de um estudo específico sobre qualidade de potência e modos operacionais de navios, exigindo conhecimento dessa fonte externa para ser respondida adequadamente.
- **gpt-5-petrobras:medium** aprovou `470390a408-b2-A1::dependencia_fonte` (dependencia_fonte): A pergunta foi reescrita para depender do conhecimento de um documento específico, ao mencionar explicitamente 'o relatório da P-34' e o caso nele analisado, tornando a resposta dependente dessa fonte.
- **gpt-5-petrobras:medium** aprovou `567fdce5c3-b1-A1::dependencia_fonte` (dependencia_fonte): A pergunta foi reescrita para depender de conhecimento de uma ocorrência e investigação específicas da ANP sobre o rompimento do QRF/IHTP, em vez de poder ser respondida apenas pelos fatos gerais apresentados.
- **gpt-5-petrobras:medium** aprovou `4e96c8ab4a-b2-A1::dependencia_fonte` (dependencia_fonte): A pergunta foi reescrita para depender de conhecimento de um caso e de configurações específicas da unidade SSAO, criando dependência de fonte externa para contextualização da resposta.
- **gpt-5-petrobras:medium** aprovou `62e43c1988-b1-A1::dependencia_fonte` (dependencia_fonte): A pergunta foi reescrita para depender de um documento específico — um relatório de integridade de ancoragem de 2019 da campanha de aumento de cargas ambientais — de modo que só quem conhece essa fonte consegue responder diretamente.
- **gpt-5-petrobras:medium** aprovou `567fdce5c3-b2-A1::dependencia_fonte` (dependencia_fonte): A pergunta foi reescrita para depender do conhecimento de casos e documentos específicos — a investigação do FPSO Cidade de São Mateus e um estudo do Reino Unido sobre stability computer — em vez de poder ser respondida apenas com conhecimento técnico geral e os fatos apresentados.
- **gpt-5-petrobras:medium** aprovou `6fffbf5758-b2-A1::dependencia_fonte` (dependencia_fonte): A pergunta foi reescrita para depender de conhecimento de um caso/documento específico — o safety case da instalação analisada — em vez de poder ser respondida apenas com os fatos gerais fornecidos.
- **gpt-5-petrobras:medium** aprovou `96c4f33979-b0-A2::dependencia_fonte` (dependencia_fonte): A pergunta foi reescrita para depender de uma fonte específica externa ao enunciado, ao mencionar 'o relatório de comissionamento da fase final de construção em estaleiro', de modo que só quem conhece esse documento consegue responder diretamente.
- **gpt-5-petrobras:medium** aprovou `b56db319e4-b0-A2::dependencia_fonte` (dependencia_fonte): A pergunta foi reescrita para depender do conhecimento de um caso/documento específico ao mencionar o arranjo operacional da SSDP PHI, tornando a resposta condicionada a essa fonte externa.
- **gpt-5-petrobras:medium** aprovou `d720962e6f-b0-A2::dependencia_fonte` (dependencia_fonte): A pergunta foi reescrita para depender do conhecimento de uma fonte específica, ao vincular a resposta ao caso apresentado nas “Guidelines for Engineering Design for Process Safety”.
- **gpt-5-petrobras:medium** aprovou `d720962e6f-b1-A1::dependencia_fonte` (dependencia_fonte): A pergunta foi reescrita para depender do conhecimento de um caso/documento específico (NC_040_SSM_2022-08), tornando a resposta dependente de fonte externa em vez de ser respondível apenas pelos fatos gerais apresentados.
- **gpt-5-petrobras:medium** aprovou `e9ca515f84-b2-A1::dependencia_fonte` (dependencia_fonte): A pergunta foi reescrita para depender do conhecimento de uma análise/estudo específico ('a análise de integridade que modela a curva Δp̂ ... e combina essa leitura com a prática de anomaly management até close out'), em vez de poder ser respondida apenas com os fatos gerais.
