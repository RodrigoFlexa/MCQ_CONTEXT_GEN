# Nova edição do contexto — polimento

**Estado:** revisao_requerida

Etapa: consolidacao

Base: /home/gbs2/MCQ_CONTEXT_GEN/pipeline/qa_research/relatorios/polimento_3_contextos_20261101T194650/02_02/documento.json

Intervenções aprovadas: 4 de 4.
Alterações aprovadas: 6.
Alterações de acabamento: 11.
Tentativas externas cumulativas: 30.
Documento publicado: não; leia documento_para_revisao.md.
Elegível para QA: não.

A preservação de texto herdado não significa nova verificação de todas as afirmações.

| Ponto estável | Cobertura | Motivo |
|---|---|---|
| OLEO_EMULSOES | atendido | C01 cobre seleção, aplicação, dosagem em ensaios, limites de extrapolação, influência do fluido e monitoramento de desempenho de desemulsificantes e clarificantes. |
| OLEO_ESPUMA | atendido | C02 aborda mecanismo de formação e quebra de espuma, seleção entre formulações, ajuste de dosagem, ponto de aplicação, efeitos colaterais e monitoramento operacional do antiespumante. |
| AGUA_PRODUZIDA | atendido | C03 trata coagulação, floculação, desemulsificação reversa, integração com flotação, aplicação, janela de dosagem, compatibilidade e monitoramento de desempenho, incluindo o papel do TOG em B03_04. |
| AGUA_SRU | atendido | C04 cobre função da URS/SRU, incompatibilidade iônica, anti-incrustantes, limites de aplicação, contribuição para mitigação de souring em B04_01 e compatibilidade entre cloração/oxidantes residuais, membranas e etapas a jusante. |
| AGUA_OXIGENIO | atendido | C05 explica desaeração por membranas, uso de bissulfito, função da remoção de oxigênio, influência do arranjo do sistema, ponto de aplicação, mistura, tempo de residência, residual de cloro, CO2 e utilidades na seleção da rota. |
| AGUA_MICROBIOLOGIA | atendido | C06 cobre função do controle microbiológico, biofilme, cloração e biocidas não oxidantes, regimes de aplicação, limitações por depósitos, compatibilidade com o processo e critérios práticos de seleção do programa. |
| GAS_MEG_HIDRATOS | atendido | C07 trata o mecanismo termodinâmico do MEG, condições de aplicação em topside e subsea, dependência da concentração efetiva na fase aquosa, regeneração, sais, precipitação e limites de modelos e de extrapolação. |
| GAS_CORROSAO | atendido | C08 cobre função dos químicos no tratamento do gás, mecanismo de adsorção e filme, influência do meio água-MEG, compatibilidade com outros produtos, aplicação por serviço, ajuste qualitativo de dosagem e monitoramento em campo do inibidor de corrosão. |
| DEPOSITOS | atendido | C09 aborda prevenção química de incrustações e depósitos em topside e subsea, incluindo inibidores de incrustação, squeeze, URS como alternativa, parafinas, asfaltenos, solventes e limites entre mecanismos distintos. |
| COMPATIBILIDADE | atendido | C12 consolida o eixo transversal de compatibilidade entre produtos químicos e materiais, cobrindo interação entre programas, precipitação, perda de desempenho, validação em fluido/material/condição representativos e interfaces de armazenamento, transferência e dosagem. |
| ARMAZENAMENTO | atendido | C10 cobre segregação, compatibilidade entre produtos, contenção, materiais, transporte interno, transferência, resposta a derramamento, monitoramento do armazenamento e consequências operacionais de falhas de manuseio. |
| MONITORAMENTO | atendido | C11 oferece base para monitoramento do desempenho e ajuste de dosagem com indicadores microbiológicos, corrosão, confiabilidade de medição, automação, leitura temporal e interpretação integrada; os capítulos temáticos complementam com sinais específicos de processo e residual químico. |

Alterações técnicas já comitadas:
- I01_OP02 (I01): substituir em B05_05
- I02_OP01 (I02): substituir em B06_01
- I02_OP02 (I02): substituir em B06_07
- I01_OP01 (I01): substituir em B04_05
- I03_OP01 (I03): substituir em B09_01
- I04_OP01 (I04): substituir em B09_03

Defeitos detectados na leitura editorial (histórico preservado):
- B04_05, B05_05: A explicação sobre cloração/descloração, incompatibilidade de oxidantes residuais com membranas RO/NF de poliamida e persistência do risco de bioincrustação a jusante após a descloração aparece nos dois blocos com detalhe muito semelhante. Concentrar a explicação principal em B04_05, que é o bloco da SRU; em B05_05, manter apenas a consequência local para a desaeração e para o sequestrante de oxigênio: impacto do residual oxidante na demanda química, na escolha do arranjo e, quando houver membranas a jusante, uma remissão curta à exigência de compatibilidade.
- B04_02, B09_03: A comparação entre URS e inibição química ao longo da vida do campo, com menção a reinjeção de água produzida, uso de água de aquífero e avaliação técnico-econômica, foi repetida em dois capítulos. B04_02 deve concentrar a explicação comparativa completa; B09_03 deve manter só a interação local com as alternativas ao squeeze, registrando que a URS atua na causa química da incrustação sem reabrir a discussão completa de viabilidade e de arranjos de campo/planta.
- B07_05, B08_03: A definição do MEG como inibidor de hidratos e a enumeração de propriedades básicas do produto e de sua atuação preferencial na fase aquosa foram repetidas. B07_05 deve concentrar o mecanismo e as propriedades gerais do MEG; B08_03 deve manter apenas a consequência local para corrosão e para o meio água-MEG, sem repetir a apresentação básica do produto.
- B04_02: Há marcas de relato de fonte no trecho: "Há indicação de que a dessulfatação é mais justificável quando o risco de BaSO4 e SrSO4 é severo..." e "Alternativas citadas para reduzir incrustação incluem reinjeção de água produzida, uso de água de aquífero e diferentes estratégias com inibidores." O bloco deve assumir voz técnica autônoma, preservando as condições de severidade do risco, volume de água, impacto econômico e limitações de espaço e peso, sem remeter a "indicação" ou a "alternativas citadas".
- B09_04: O bloco denuncia leitura de fonte no trecho: "Os aditivos citados atuam por mecanismos diferentes" e em "são descritos como requerendo volumes elevados para maior eficiência". A redação deve ser convertida para voz técnica autônoma, mantendo a distinção entre mecanismos e o limite de que desempenho e necessidade de aplicação dependem do produto e da condição de referência, sem fórmulas do tipo "citados" ou "são descritos".
- B10_04: O trecho "técnicas eletroquímicas como par galvânico e resistência à polarização foram consideradas adequadas, no contexto estudado, para acompanhar variações de corrosividade em regime dinâmico" é relato de leitura, não redação técnica autônoma. O texto deve apresentar a utilidade dessas técnicas como condição de aplicação e limitação metodológica do próprio documento, sem a muleta "no contexto estudado".
- B09_01, B09_02, B09_03: Termos de nicho em inglês entram sem explicação em português no primeiro uso: "squeeze" (B09_01/B09_02), "gravel" (B09_01) e "frac-pack" (B09_03). Na primeira ocorrência, o documento deve glosar cada termo em português técnico do Brasil e só depois reutilizar a forma em inglês, para não depender de conhecimento prévio implícito do leitor.
- B12_01: O termo "fouling" aparece sem explicação em português no trecho final do bloco. No primeiro uso, convém indicar o fenômeno em português técnico pertinente ao contexto de membranas, como incrustação/colmatação/deposição na superfície, e então manter o anglicismo se ele continuar útil no capítulo.
- B07_05: B07_05 é um bloco definicional de abertura ("O que é o MEG e como ele atua na prevenção de hidratos"), mas foi colocado depois de blocos que já tratam de mecanismo, condições de aplicação, modelagem de sais e regeneração. A organização fica regressiva. Esse bloco deveria abrir o capítulo, ou ao menos anteceder B07_01 e B07_02, deixando os demais para aprofundamento operacional.

Trabalho ainda pendente:
- revisao_1 (editorial): Há duplicação residual da mesma ressalva sobre o fato de que cloração contínua seguida de descloração não elimina, por si só, o risco de bioincrustação a jusante, o que prejudica a fluidez da leitura.
- revisao_2 (editorial): O bloco definicional do MEG permanece depois de blocos mais avançados do capítulo, quebrando a progressão expositiva e deixando a leitura menos natural.
- revisao_3 (editorial): Repete a mesma explicação sobre residual de cloro/oxidantes, necessidade de descloração e compatibilidade de membranas poliméricas, inclusive com menção a SRU e RO/NF. Concentrar a explicação principal em B04_05, que já trata de cloração, oxidantes residuais e compatibilidade com a SRU e etapas a jusante. Em B05_05, manter apenas a consequência local para desaeração e sequestrante: residual oxidante altera a demanda química e, se houver membranas a jusante, deve obedecer ao critério de compatibilidade já definido no capítulo da SRU.
- revisao_4 (editorial): Repete quase a mesma cadeia explicativa 'fibras ocas -> grande área interfacial por volume -> sistemas compactos e modulares'. Concentrar a explicação principal em B05_01, que apresenta o mecanismo da desaeração por membranas. Em B05_04, manter só as consequências para FPSO/offshore, como atratividade por espaço, peso, modularidade e integração operacional, sem reabrir o mecanismo básico.
- revisao_5 (editorial): Repete o mesmo mecanismo sobre água produzida/água segregada em ambiente fechado, atividade de BRS, geração de H2S e agravamento de corrosão por superdosagem de oxidantes. Concentrar a explicação técnica em B10_02, cujo subtítulo já trata de contenção, materiais e ambiente corrosivo. Em B10_05, manter apenas a consequência para seleção do arranjo e para segregação de oxidantes e redutores, sem reexplicar o mecanismo microbiológico e corrosivo.
- revisao_6 (editorial): B07_05 está deslocado dentro do capítulo: traz a definição básica de MEG, hidratos e mecanismo termodinâmico depois de blocos que já discutem aplicação, sais e regeneração. Esse conteúdo introdutório deveria abrir o capítulo, antes de B07_01, ou ser absorvido por ele. Na posição atual, quebra a progressão lógica e ainda reforça redundância com a explicação mecanística já apresentada.
- revisao_7 (editorial): Há marcas de narrativa de fonte nos trechos 'foram sugeridos controles de pH, inibidor de corrosão, dispersante, hipoclorito e descargas com base em variáveis de processo' e 'Em uma operação acompanhada, períodos de alta demanda de cloro coincidiram...'. Esses trechos denunciam recomendação ou caso relatado, não redação técnica autônoma. Converter para voz técnica impessoal, preservando as condições: automação depende da qualidade metrológica e o acoplamento entre qualidade da água, demanda de cloro, deposição, microbiologia e corrosão é possível, mas condicionado ao sistema monitorado.
- revisao_8 (editorial): O trecho 'Entre os indicadores citados para esse acompanhamento estão sonda de corrosão, amostragem de ferro dissolvido e residual do inibidor' denuncia enumeração trazida de fonte. Converter para formulação técnica autônoma, preservando a condição de que o monitoramento ganha robustez quando combina indicadores de corrosão com indicadores de presença do químico no circuito.
- revisao_9 (editorial): O termo inglês 'stripping' aparece sem explicação em português brasileiro no primeiro uso em 'desaeração mecânica por stripping com gás em contracorrente' e reaparece em 'Stripping a gás exige avaliar...'. No primeiro uso, convém manter o termo apenas se vier acompanhado do equivalente/explicação em português; depois disso, o uso isolado fica aceitável.

Pareceres, comparação e decisões: `versoes/8ebc36b09235f03eda8febfc/`.
