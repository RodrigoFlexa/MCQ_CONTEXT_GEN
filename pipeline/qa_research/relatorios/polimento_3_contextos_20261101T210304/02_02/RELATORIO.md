# Nova edição do contexto — polimento

**Estado:** revisao_requerida

Base: /home/gbs2/MCQ_CONTEXT_GEN/pipeline/qa_research/relatorios/polimento_3_contextos_20261101T194650/02_02/documento.json

Intervenções aprovadas: 1 de 3.
Alterações aprovadas: 1.
Alterações de acabamento: 0.
Palavras: 9780 → 9840.
Tentativas externas cumulativas: 13.
Documento publicado: não; leia documento_para_revisao.md.
Elegível para QA: não.

A preservação de texto herdado não significa que todas as afirmações anteriores foram verificadas novamente.

| Ponto estável | Cobertura | Motivo |
|---|---|---|
| OLEO_EMULSOES | atendido | O capítulo cobre seleção, bottle test, dosagem, condições de aplicação, limites de extrapolação e monitoramento. A correção aprovada em B01_03 foi preservada: clarificante, floculante e quebrador de emulsão reversa não aparecem como sinônimos automáticos. |
| OLEO_ESPUMA | atendido | Há explicação de mecanismo, seleção entre formulações, ajuste de dosagem, ponto de aplicação, efeitos colaterais e monitoramento operacional do antiespumante. |
| AGUA_PRODUZIDA | atendido | O texto cobre coagulação, floculação, desemulsificação reversa, integração com flotação, janela de dosagem e consequências no efluente. A proteção do especialista em B03_04 foi preservada, incluindo a ligação explícita com o TOG da água produzida tratada. |
| AGUA_SRU | atendido | O documento cobre função da URS/SRU, incrustação por sulfatos, decisão frente a alternativas, pontos de uso de anti-incrustantes e cautelas com cloro/oxidantes e membranas. A proteção do especialista em B04_01 foi preservada, incluindo a contribuição da remoção de sulfato para mitigar souring. |
| AGUA_OXIGENIO | parcial | O capítulo cobre mecanismos de desaeração, papel do bissulfito, ponto de aplicação, interação com oxidantes e limitações operacionais. Porém, continua faltando um ensino mais direto e concentrado sobre monitoramento de desempenho no circuito real da desoxigenação/sequestrante, como já apontado no histórico de I02. |
| AGUA_MICROBIOLOGIA | atendido | Há função do controle microbiológico, biofilme, cloração e biocidas, regimes de aplicação, compatibilidade operacional e limites impostos por depósitos e limpeza mecânica. |
| GAS_MEG_HIDRATOS | atendido | O texto cobre mecanismo do MEG, condições de aplicação em topside e subsea, importância da concentração efetiva na fase aquosa, regeneração, sais e limites de modelos termodinâmicos. |
| GAS_CORROSAO | atendido | Há função dos químicos no tratamento do gás, mecanismo dos inibidores de corrosão, interação com MEG e outros produtos, aplicação por serviço e monitoramento em campo. |
| DEPOSITOS | atendido | O capítulo aborda inibidores de incrustação, squeeze, alternativas como URS, parafinas e asfaltenos, com mecanismos, critérios de seleção e limites de extrapolação. |
| COMPATIBILIDADE | atendido | O texto trata compatibilidade entre programas químicos e materiais no processo, na armazenagem, na transferência e no monitoramento, preservando mecanismos, condições e exceções. |
| ARMAZENAMENTO | atendido | Há segregação, contenção, transporte interno, transferência, ambiente corrosivo e monitoramento de armazenamento/manuseio com consequências operacionais. |
| MONITORAMENTO | parcial | O capítulo geral de monitoramento é consistente para microbiologia, corrosão, automação e confiabilidade da medição, mas não fecha de modo explícito o caso de monitoramento de desempenho da desaeração e do sequestrante de oxigênio, que permanece disperso no documento. |

Trabalho ainda pendente (intervenções, cobertura, escopo e revisão):

- I02 (lacuna_essencial): Acrescentar um bloco curto sobre monitoramento de desempenho da desaeração e do sequestrante de oxigênio no ponto representativo do sistema.
- I03 (editorial): Ajustar a redação para deixar explícito, no corpo do texto e no auxiliar, quando a condição é específica do fabricante consultado e quando é uma cautela dependente do material da membrana e do arranjo adotado.
- cobertura_AGUA_OXIGENIO (lacuna_essencial): O capítulo cobre mecanismos de desaeração, papel do bissulfito, ponto de aplicação, interação com oxidantes e limitações operacionais. Porém, continua faltando um ensino mais direto e concentrado sobre monitoramento de desempenho no circuito real da desoxigenação/sequestrante, como já apontado no histórico de I02.
- cobertura_MONITORAMENTO (lacuna_essencial): O capítulo geral de monitoramento é consistente para microbiologia, corrosão, automação e confiabilidade da medição, mas não fecha de modo explícito o caso de monitoramento de desempenho da desaeração e do sequestrante de oxigênio, que permanece disperso no documento.
- escopo_1 (lacuna_essencial): A frase do especialista inclui prevenção de crescimento microbiológico em sistemas topside e subsea de forma ampla, mas o documento detalha microbiologia principalmente no contexto da água de injeção e não expande esse tratamento para outros sistemas topside/subsea fora desse circuito.
- revisao_1 (editorial): Permanece uma pendência editorial bloqueante nos dois blocos sobre cloro/oxidantes e membranas. O texto já condiciona a cautela ao "fabricante consultado" e ao material/arranjo, mas a origem e o escopo dessa ressalva não ficaram consolidados de forma única, e há sobreposição relevante entre os dois blocos. Como essa leitura já estava sinalizada como bloqueante, a edição não deve seguir para QA sem resolver a rastreabilidade editorial e a duplicação parcial.
- revisao_2 (editorial): Duplicação substancial: os dois blocos repetem a mesma explicação sobre membranas RO/NF de poliamida, com o mesmo mecanismo/condição — necessidade de descloração antes da membrana, dependência da agressividade do oxidante da química da água e limite de cloração contínua seguida de descloração para controlar bioincrustação a jusante. Reparo: consolidar a explicação em um único ponto e, no outro bloco, manter apenas a consequência específica do capítulo.
- revisao_3 (editorial): Duplicação dentro do capítulo: repete-se a mesma ideia de que contatores de membrana com fibras ocas oferecem grande área interfacial por volume, favorecem arranjos compactos/modulares em offshore e podem reduzir uso de sequestrante, com a mesma ressalva de dependência de projeto e operação. Reparo: fundir os trechos ou deixar um bloco para mecanismo e outro apenas para critérios de seleção que ainda não tenham sido ditos.
- revisao_4 (editorial): Há repetição do mesmo mecanismo central do MEG — inibição termodinâmica por atuação na fase aquosa e redução da atividade da água — e o bloco definicional aparece tarde, depois de o texto já usar a sigla e discutir aplicação. Reparo: trazer definição e expansão da sigla para o primeiro ponto de uso e eliminar a repetição do mecanismo no bloco posterior, preservando só o que for exclusivo.
- revisao_5 (editorial): B06_07 recompõe, além de uma síntese breve, duas explicações já desenvolvidas antes: (i) limite do pigging e uso do tratamento químico quando a limpeza mecânica não é viável; (ii) risco de surfactantes, resíduos e restrições de descarte/compatibilidade no programa de biocidas. Reparo: enxugar B06_07 para funcionar como fechamento curto, mantendo apenas critérios novos de seleção.
- revisao_6 (editorial): Duplicação interna: os dois blocos repetem a mesma cadeia causal para armazenamento de água produzida/segregada em ambiente fechado — favorecimento de BRS, geração de H2S, exigência de material compatível/monitoramento/tratamento químico — e também repetem que superdosagem de oxidantes pode agravar corrosão. Reparo: concentrar a explicação causal em um só bloco e deixar o outro apenas com consequências organizacionais ou critérios de arranjo ainda não mencionados.
- revisao_7 (editorial): Duplicação entre capítulos: B09_03 reexplica o mesmo mecanismo e o mesmo critério de decisão já tratados em C04 — a URS reduz sulfato para prevenir precipitação de BaSO4/SrSO4 e sua seleção frente à inibição química depende de viabilidade técnico-econômica. Reparo: em B09_03, manter só uma remissão curta da URS como alternativa ao squeeze, sem repetir o desenvolvimento já feito em C04.
- revisao_8 (editorial): Relato de leitura explícito: aparecem fórmulas como "descritas pelo fabricante consultado" e "no contexto consultado", o que faz a explicação depender da leitura da fonte. Reparo: enunciar diretamente o conceito e suas condições técnicas no corpo do texto (material da membrana, presença de oxidante, efeito a jusante) e deixar a origem da informação apenas no auxiliar.
- revisao_9 (editorial): Relato de leitura explícito em "foram consideradas adequadas, no contexto estudado". A redação informa o que um estudo concluiu, mas não ensina diretamente em que condições par galvânico e resistência à polarização são aplicáveis. Reparo: converter para explicação técnica direta e condicional, reservando a referência ao estudo para o auxiliar.
- revisao_10 (editorial): Relato de caso em "Em uma operação acompanhada..." seguido de inferência do tipo "essa sequência sugere". Isso desloca o texto para narrativa de caso, em vez de explicar o encadeamento causal de forma geral e condicionada. Reparo: transformar o trecho em explicação conceitual com condições explícitas e, se o caso for mantido, tratá-lo como exemplo auxiliar identificado como tal.
- revisao_11 (editorial): Relato de leitura por voz mediada em "foram sugeridos controles de...". A frase reporta sugestões de leitura em vez de explicar diretamente quais variáveis justificam cada malha de automação e sob quais condições o dado é representativo. Reparo: substituir a forma mediada por formulação direta e condicional, deixando a origem bibliográfica no auxiliar.
- revisao_12 (editorial): Há termos e siglas em inglês sem explicação em português brasileiro no primeiro uso: FPSO (B01_02), offshore (B02_01), RO/NF (B04_05), pigging (B06_01), topside/subsea (B07_02), gravel (B09_01), flushing (B10_01) e PCR/FISH (B11_01). Reparo: expandir ou explicar cada termo na primeira ocorrência, mantendo o original apenas como apoio terminológico quando necessário.
- revisao_13 (editorial): Relato de leitura: explique o conceito e suas condições; registre a origem no auxiliar
- revisao_14 (editorial): Relato de leitura: explique o conceito e suas condições; registre a origem no auxiliar

Pareceres, fontes, comparação antes/depois e decisões estão na pasta da versão: `versoes/9ca9c8e8cd825df56e3d5d0e/`.
