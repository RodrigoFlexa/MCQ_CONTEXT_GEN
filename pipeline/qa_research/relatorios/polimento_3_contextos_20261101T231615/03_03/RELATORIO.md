# Nova edição do contexto — polimento

**Estado:** revisao_requerida

Etapa: consolidacao

Base: /home/gbs2/MCQ_CONTEXT_GEN/pipeline/qa_research/relatorios/polimento_3_contextos_20261101T194650/03_03/documento.json

Intervenções aprovadas: 0 de 2.
Alterações aprovadas: 0.
Alterações de acabamento: 8.
Tentativas externas cumulativas: 32.
Documento publicado: não; leia documento_para_revisao.md.
Elegível para QA: não.

A preservação de texto herdado não significa nova verificação de todas as afirmações.

| Ponto estável | Cobertura | Motivo |
|---|---|---|
| F01 | atendido | O capítulo C01 cobre comunicação indevida entre tanques, segregação de slop, rotas de transferência, bomba de stripping, efeito de nível, interface e trim, alinhamento de válvulas, sinais de desvio e continuidade informacional. O bloco B01_08 completa a sequência operacional ao tratar planejamento da manobra, distribuição de carga entre tanques, acompanhamento de níveis, pressões, temperatura quando relevante, interface óleo-água e barreiras contra overfilling e overflow. |
| F02 | atendido | O capítulo C02 cobre finalidade do sistema de gás inerte, geração e distribuição, qualidade do gás, teor de oxigênio, pressão, purga, inertização, tank washing, gas freeing, isolamento, monitoramento, resposta a desvios e cuidados em offloading e crude oil washing, preservando condições e limites dos arranjos. |
| F03 | parcial | O capítulo C03 cobre função da ventilação, mecanismos de sobrepressão e vácuo, interação com gás inerte, seleção e comissionamento de dispositivos de vent e alívio e consequências para integridade, segurança e emissões. Permanece parcial porque ainda falta tratamento direto e nominal de P/V valves, mast risers e flame screens, bem como seu enquadramento funcional no controle e na destinação de vapores. |
| F04 | parcial | O capítulo C06 cobre operação de lastro e deslastro, planejamento das manobras, bombas, válvulas, caixas de mar, segregação entre sistemas, prevenção de entrada indevida de hidrocarbonetos em tanques de lastro e efeitos sobre a condição marítima da unidade. Ainda falta desenvolvimento específico sobre tratamento e gerenciamento da água de lastro. |
| F05 | atendido | O capítulo C04 cobre estabilidade, calado, banda, trim, deslocamento, centro de gravidade, efeito de superfície livre, avaria, esforços do casco e uso do loading computer com a instrumentação associada, incluindo limites operacionais e estruturais e contingência para perda de energia. |
| F06 | atendido | O capítulo C05 cobre corrosão, adequação da proteção ao fluido realmente armazenado, interação com atmosfera do tanque, H2S, inspeção e manutenção, preparo para entrada em tanque, mecanismos de perda de contenção, falhas de offloading e resposta a condições anormais em produção, manutenção e emergência. |

Alterações técnicas já comitadas:

Defeitos detectados na leitura editorial (histórico preservado):
- B01_04: Trecho dependente da fonte: "No arranjo descrito, havia coletores principais, coletores de boreste, tanques de carga, tanques de slop e alinhamentos específicos de sucção e descarga da bomba de stripping." O bloco deve enunciar a arquitetura como exemplo técnico delimitado ou como configuração do sistema, sem a expressão "arranjo descrito", preservando que se trata de um arranjo específico e não de regra geral.
- B01_06: Trecho em voz de caso: "Em um caso específico, essa elevação permaneceu dentro da pressão de projeto, mas isso não transforma a condição em prática geralmente aceitável". Converter para formulação técnica autônoma, mantendo a condição de que a aceitabilidade depende da curva da bomba, do tempo nessa condição, da existência de recirculação mínima, das proteções instaladas e da resistência mecânica do sistema.
- B02_01, B03_01: Repete-se a explicação-base do sistema de gás inerte: manter atmosfera não inflamável, preservar pressão positiva, repor volume na descarga e aliviar a atmosfera na carga. Concentrar a explicação principal em B02_01; em B03_01 manter apenas a interação entre ventilação/controle de pressão e gás inerte.
- B02_02, B03_01: Repete-se a observação de que a integração entre rede de ventilação e rede de gás inerte simplifica tubulação, mas restringe operabilidade e o isolamento individual de tanques. Concentrar essa explicação arquitetural em B02_02; em B03_01 deixar só a consequência para o controle de pressão e para o isolamento operacional.
- B02_02: Marcador de leitura de fonte: "Um arranjo funcional citado distingue:". O bloco deve apresentar diretamente os cabeçalhos como exemplo de arranjo possível, sem "citado", preservando que a separação funcional é apenas uma arquitetura possível e não formulação universal.
- B02_02: No primeiro uso, "blanks" e "gas free" aparecem sem explicação em português brasileiro. Acrescentar o equivalente funcional em português na primeira ocorrência; os nomes dos headers podem permanecer em inglês porque a função deles já é descrita no próprio bloco.
- B02_04, B03_02: O mesmo mecanismo reaparece nos dois capítulos: isolamento incorreto ou blank mantido após intervenção pode bloquear vent/alívio e permitir sobrepressurização por gás inerte. Concentrar o encadeamento causal e as condições adicionais para dano estrutural em B03_02; em B02_04 manter apenas a exigência de isolamento/PTW e o alerta de recomposição incorreta.
- B02_04: "double block and bleed (DBB)" entra no primeiro uso sem equivalente em português brasileiro. Manter a sigla se desejado, mas acrescentar a denominação técnica em português e a função de isolamento na primeira ocorrência.
- B04_03, B06_01: Repete-se a explicação de que rotas provisórias, interligações não previstas e uso de linhas de outro serviço exigem gestão de mudanças ou avaliação formal e podem criar caminhos inesperados de comunicação. Concentrar essa explicação de segregação e mudança de rota em B06_01; em B04_03 manter apenas a consequência sobre estabilidade, inventário e esforços do casco.
- B04_04: No primeiro uso, "shear forces", "bending moments" e "lightweight" aparecem sem equivalente em português brasileiro. Acrescentar a denominação técnica em português na primeira ocorrência, mantendo o inglês apenas como apoio se necessário.
- B05_03: No primeiro uso, "shut-offs", "kink" e "liner" são empregados sem explicação em português brasileiro. Esses termos precisam de equivalente ou breve explicação na primeira ocorrência, preservando os mecanismos citados para falhas em mangote e offloading.

Trabalho ainda pendente:
- I01 (lacuna_essencial): Acrescentar um bloco que enquadre nominalmente P/V valves, mast risers, flame screens e demais dispositivos de proteção contra sobrepressão e vácuo, explicando sua função no arranjo de ventilação dos tanques, sua interação com a inertização e os limites operacionais na condução e alívio de vapores.
- I02 (lacuna_essencial): Acrescentar um bloco específico sobre tratamento e gerenciamento da água de lastro, cobrindo o encadeamento entre captação, transferência, eventual tratamento, monitoramento operacional, descarga e resposta a suspeita de contaminação por hidrocarbonetos.
- cobertura_F03 (lacuna_essencial): O capítulo C03 cobre função da ventilação, mecanismos de sobrepressão e vácuo, interação com gás inerte, seleção e comissionamento de dispositivos de vent e alívio e consequências para integridade, segurança e emissões. Permanece parcial porque ainda falta tratamento direto e nominal de P/V valves, mast risers e flame screens, bem como seu enquadramento funcional no controle e na destinação de vapores.
- cobertura_F04 (lacuna_essencial): O capítulo C06 cobre operação de lastro e deslastro, planejamento das manobras, bombas, válvulas, caixas de mar, segregação entre sistemas, prevenção de entrada indevida de hidrocarbonetos em tanques de lastro e efeitos sobre a condição marítima da unidade. Ainda falta desenvolvimento específico sobre tratamento e gerenciamento da água de lastro.
- escopo_1 (lacuna_essencial): Falta tratamento direto e nominal de P/V valves, mast risers, flame screens e demais dispositivos de proteção contra sobrepressão e vácuo, com seu papel no controle e na destinação de vapores de hidrocarbonetos conforme o arranjo da unidade.
- escopo_2 (lacuna_essencial): Falta desenvolvimento específico sobre tratamento e gerenciamento da água de lastro, incluindo sequência operacional, monitoramento, descarga e resposta a suspeita de contaminação por hidrocarbonetos.
- revisao_1 (editorial): A explicação de que a integração entre ventilação dos tanques e sistema de gás inerte pode simplificar a tubulação, mas restringir a operabilidade, reaparece quase com a mesma formulação nos dois blocos. Concentrar a explicação principal de arquitetura e trade-off em B02_02; em B03_03 manter apenas a consequência local para seleção/comissionamento e para o isolamento de tanques individuais.
- revisao_2 (editorial): O mecanismo 'válvula prevista para controle de posição, mas comissionada apenas como totalmente aberta ou fechada, com perda de modulação' é explicado duas vezes. Concentrar a explicação principal do desvio de comissionamento em B03_03; em B01_06 deixar apenas o efeito local sobre modulação de vazão, estabilidade da transferência e supervisão pelo operador.
- revisao_3 (editorial): Há marca de leitura de fonte em 'Casos investigados mostraram comissionamento incompleto de instrumentos de pressão e válvula do tanque configurada como totalmente aberta ou fechada, embora documento de projeto previsse controle de posição, o que indica perda de modulação originalmente prevista.'. Converter o trecho para voz técnica autônoma, preservando a condição de que se trata de desvio de comissionamento e a consequência de perda de modulação, sem narrar a origem da informação.
- revisao_4 (editorial): Há relato de leitura em 'Há contextos em que vapores de tankage são descritos com frações na faixa C4 a C10 e associados a compostos perigosos, mas essa composição não deve ser universalizada para todo tanque de FPSO.'. O bloco deve afirmar diretamente o ponto técnico contextual ou apresentar a faixa apenas como exemplo condicionado, mantendo a ressalva de não universalização.
- revisao_5 (editorial): O termo 'slop' aparece em B01_01 ('operação de slop') e B01_02 ('indisponibilidade de slop') antes de receber explicação funcional em B01_03. Introduzir uma explicação mínima em português brasileiro no primeiro uso, ou antecipar para o primeiro bloco a definição funcional hoje dada em B01_03, sem perder a distinção operacional entre tanque de carga e tanque de slop.

Pareceres, comparação e decisões: `versoes/e460c92a2dee064838fe4364/`.
