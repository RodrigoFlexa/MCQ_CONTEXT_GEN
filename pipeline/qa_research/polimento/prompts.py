"""Uma edição fundamentada do documento existente, sem resumo substituto."""
from pipeline.qa_research.v3.prompts import BASE

DIAGNOSE = BASE + '''Você prepara o POLIMENTO de um documento técnico existente.
A base já recebeu revisão editorial e correções do especialista. Preserve sua
profundidade, mecanismos, condições, exceções e distinções úteis. Leia a frase
integral do especialista e os recortes curados. Não replaneje os temas nem troque
o documento por uma síntese nova. Conteúdo adequado fica intocado.
Proponha no máximo limite intervenções, priorizando erro técnico e lacuna essencial.
Tipos: correcao_tecnica (erro, generalização, condição ou exceção importante ausente),
lacuna_essencial (parte do pedido não ensinada), aprofundamento (ganho pertinente),
editorial (clareza, organização, redundância; sem acrescentar fatos).
Limites opcionais não são lacunas essenciais. Não exija dosagens universais,
parâmetros de fabricante, normas ou matrizes completas se não forem indispensáveis.
As protecoes registram correções do especialista que precisam permanecer válidas.
Use IDs dos blocos para reparos; IDs de capítulo para acrescentar blocos; DOCUMENTO
somente para capítulo realmente ausente. Uma intervenção pode agrupar reparos
relacionados. Não atribua o mesmo bloco a intervenções distintas.
Consultas PT/EN são expressões técnicas específicas, até 16 palavras por idioma,
no máximo três pares. Para edição puramente editorial podem ser vazias.
Para qualquer intervenção técnica, ao menos um par é obrigatório. Busque a função
e o equipamento específico; consultas genéricas sobre o setor não fecham lacunas.
Leia também redundâncias entre capítulos e relatos de leitura herdados. Priorize
reparos que tornem o texto autônomo sem apagar condições de aplicação.
Em cobertura, avalie TODOS os pontos curados sem criar IDs novos. Omissões da frase
que o mapa não representa ficam em omissoes_escopo, sem esconder o problema.
Não use quantidade de palavras como medida de qualidade. Não crie defeitos para
preencher a lista. Retorne um plano compacto, não o documento reescrito.
JSON {"intervencoes":[{"id":"I01","tipo":"correcao_tecnica|lacuna_essencial|aprofundamento|editorial",
"prioridade":"alta|media|baixa","alvos":["B01_01"],"pontos":["F01"],
"objetivo":"o que melhorar","motivo":"por que é necessário",
"consultas":[{"pt":"...","en":"..."}]}],
"cobertura":[{"id":"F01","estado":"atendido|parcial|ausente","motivo":"..."}],
"omissoes_escopo":[]}.
'''

RESEARCH = BASE + '''Investigue SOMENTE a necessidade técnica da intervenção.
Você recebe passagens originais herdadas da pesquisa anterior e/ou de coleções
novas. Origem herdada não significa revisão factual nova. Avalie pertinência,
estatuto, equipamento, materiais, condições, exceções e limites. Não transforme
resultado de fabricante em desempenho universal ou recomendação estrangeira em
obrigação brasileira. Uma referência normativa sem edição/vigência verificada não
autoriza afirmar que a regra é atual. Relate essa pendência.
Extraia até oito relações úteis com suas condições e limites.
Classifique pertinencia=direta somente quando a proposição
responde concretamente ao objetivo da intervenção. Conteúdo genérico sobre o setor,
ou que declara não explicar o equipamento procurado, é contextual e não fundamenta
a inclusão. Se não houver achado direto, suficiente=false e reformule a consulta
pelo equipamento, sua função e termos técnicos equivalentes PT/EN. Não acumule
relações laterais para aparentar evidência.
Cite os IDs de parágrafos fornecidos; não copie citações literais nem invente posições no texto.
O código recupera a passagem original a partir do ID. suficiente indica
se os achados permitem melhorar o ponto, não se o tema inteiro ficou exaustivo.
Se faltar informação central, proponha até três consultas PT/EN curtas (máximo 16
palavras por idioma). Não repita consultas anteriores nem apenas sinônimos sem
perspectiva de evidência nova. Não acrescente QA nem exemplos de perguntas.
Nesta leitura, extraia somente achados das fontes atuais; anteriores serve para
evitar repetição, não para citar novamente um parágrafo que não foi enviado agora.
JSON {"suficiente":true,"achados":[{"proposicao":"relação técnica útil",
"citacoes":["N...P01"],"tipo":"explicacao_tecnica|resultado_experimental|recomendacao|opiniao|norma|indeterminado",
"pertinencia":"direta|contextual","condicoes":["..."],"limites":["..."]}],"consultas_adicionais":[],"pendencias":[]}.
'''

EDIT = BASE + '''Edite SOMENTE os alvos das intervenções recebidas. O documento
existente é a base e precisa conservar suas explicações úteis e as protecoes do
especialista. Não devolva uma reescrita integral, resuma capítulos ou transfira
conhecimento para notas. Pode corrigir, aprofundar, inserir e remover redundâncias
com justificativa e preservação da informação. Não há meta de aumentar ou reduzir
palavras. Cada alteração deve melhorar a necessidade indicada, respeitando o escopo.
Use os achados, condições e limites fornecidos. Não cite uma fonte que não sustente
o mecanismo ou o equipamento. Conceitos consolidados podem complementar a explicação:
declare-os em complementos e não atribua esse conteúdo ao corpus. Dados empíricos,
números operacionais, dosagens e requisitos normativos exigem suporte disponível.
Sem suporte útil, deixe alteracoes vazio e explique em pendencias. Não invente
conteúdo para aparentar que a lacuna foi resolvida. Edição editorial não cria fatos.
No corpo: texto didático autônomo em PT-BR, sem IDs, citações, referências, relato
de leitura, pareceres ou lacunas. Explique termos quando necessário. Distinga
conceitos, mecanismo, condições, critérios, interações e consequências.
Compare a inclusão com TODO o documento recebido: não repita a mesma explicação
em capítulos diferentes. Mantenha o mecanismo no capítulo próprio e acrescente
apenas a interação específica no outro. Preserve condições e exceções exclusivas.
Não use 'fabricante consultado', 'no contexto consultado', 'no caso relatado' ou
'a fonte afirma'. Converta em explicação autônoma com material, equipamento e
limites explícitos; um caso que não pode ser generalizado fica no auxiliar.
Explique no primeiro uso termos como peso leve (lightweight), esforços cortantes
(shear forces), momentos fletores (bending moments) e casa de bombas (pump room).
Operações: substituir/remover têm alvo B; inserir tem alvo B (depois dele) ou C
(fim do capítulo); novo_capitulo usa DOCUMENTO e informa capitulo/grupo técnicos.
Para reorganizar sem reescrever, mover usa alvo B e destino C, ambos autorizados;
renomear_capitulo usa alvo C e novo título em capitulo (grupo é opcional).
Preservacao explica concretamente onde ficaram mecanismos e condições do original
ou por que a informação foi descartada. Achados usa somente IDs recebidos. Para
remover, texto/subtitulo podem ser vazios. Não invente novos IDs de blocos.
JSON {"itens":[{"id":"I01","alteracoes":[{"operacao":"substituir|inserir|remover|novo_capitulo|mover|renomear_capitulo",
"alvo":"B01_01","subtitulo":"...","texto":"...","motivo":"...",
"preservacao":"o conhecimento conservado ou a razão de descartar",
"achados":["I01_A01"],"complementos":[]}],"pendencias":[]}]}.
Em correção, considere os pareceres e retorne o mesmo formato completo somente
para os itens indicados, preservando seus objetivos e alvos.
Mover, renomear e remover não precisam de subtitulo/texto novos.
'''

REVIEW = BASE + '''Revise as intervenções propostas contra a frase do especialista,
o documento consolidado, os blocos anteriores, as protecoes e as evidências.
Não confunda mais palavras ou mais fontes com melhoria. Verifique cada critério:
correta, suportada, condicoes_preservadas, sem_perda, escopo, autonomia, pt_br.
Autonomia=false se houver relato de leitura ou referência a fonte consultada,
inclusive em texto herdado que está sendo reeditado. Verifique repetição com os
outros capítulos: nova redação não significa informação nova. Exija consolidação
localizada quando o mesmo mecanismo/condição é repetido sem função didática.
Uma condensação não pode perder conhecimento útil, condição ou exceção. Confira
especialmente os alertas de redução e as remoções. Complementos conceituais são
permitidos, mas valores, dados e normas precisam de fonte. As protecoes são
obrigações semânticas, não exigência de repetição literal.
Rejeite generalização indevida de casos, equipamento, material ou contexto. Uma
coincidência de palavras na evidência não basta. Condição de aplicação ausente
pode invalidar a afirmação, mesmo se a frase isolada parecer correta.
Não aprovar quando algum critério for falso. corrigir só para defeito recuperável;
rejeitar se falta suporte ou o objetivo foi perdido. Limites opcionais não vetam
explicações corretas. Não peça refazer partes que não foram afetadas.
JSON {"avaliacoes":[{"id":"I01","decisao":"aprovar|corrigir|rejeitar",
"motivo":"...","correcao":"reparo concreto ou vazio","criterios":{
"correta":true,"suportada":true,"condicoes_preservadas":true,"sem_perda":true,
"escopo":true,"autonomia":true,"pt_br":true}}]}.
'''

CONSOLIDATE = BASE + '''Avalie a edição consolidada, sua frase de escopo, as protecoes
do especialista e o histórico de intervenções aceitas/rejeitadas. Alterações aceitas
já passaram por revisão com fontes; esta etapa verifica coerência do documento,
preservação das correções anteriores, autonomia editorial e cobertura estável.
Não suponha que a ausência de novos apontamentos prove validação de toda a base
herdada. Registre contradições, condições omitidas e erros técnicos aparentes.
Use os sinais editoriais fornecidos para conferir o texto inteiro. Confirme ou
descarte possíveis repetições com leitura das condições e informações exclusivas;
não apague diferenças técnicas por similaridade de palavras. Procure também
repetição semântica mesmo sem sinal automático. Marque tipo=editorial para relato
de leitura, redundância dispensável, organização ou termo inglês sem explicação;
tipo=tecnico para defeito factual. A aprovação anterior não dispensa essa leitura.
Problemas editoriais impedem liberar QA até serem resolvidos. Lacunas pertencem
à cobertura/omissões; não invente defeito editorial por ausência de conteúdo.
Critico=true para erro técnico, perda de condição essencial ou reversão de correção
do especialista que impede usar a edição em QA; lacuna sem afirmação errada deve
ficar na cobertura, não como erro de todos os parágrafos.
Avalie exatamente todos os pontos curados, com os mesmos IDs do diagnóstico.
Omissões de escopo não representadas nesses pontos ficam no auxiliar. Não marque
atendido só pela presença de um termo. Não exija aprofundamentos opcionais.
Declare protecoes_preservadas=true somente se todas as correções do especialista
continuam válidas; sem proteções fornecidas, true. Não ignore uma reversão.
JSON {"protecoes_preservadas":true,"problemas":[{"blocos":["B01_01"],"descricao":"...","tipo":"tecnico|editorial","critico":true}],
"cobertura":[{"id":"F01","estado":"atendido|parcial|ausente","motivo":"..."}],
"omissoes_escopo":[]}.
'''

EDITORIAL = EDIT + '''Esta é a única rodada de acabamento global. A base recebida
já contém as alterações técnicas aprovadas. Corrija apenas os problemas editoriais
indicados, nos blocos autorizados; apenas substituir ou remover são permitidos.
Não acrescente fatos, doses, limites, normas, exemplos empíricos nem recomendações.
Não preencha lacunas técnicas nesta etapa. Não apague informação exclusiva para
reduzir redundância. Em remoção, declare em preservacao o bloco onde permanece
cada conceito/condição. Retorne todos os itens pedidos; se não houver reparo seguro,
deixe alteracoes vazio e explique. Achados e complementos devem ser arrays vazios.
'''

EDITORIAL_AUDIT = BASE + '''Faça uma leitura editorial crítica do documento inteiro.
Sua tarefa é somente encontrar defeitos concretos de escrita e organização, sem
avaliar cobertura, completar conteúdo ou emitir um parecer técnico geral.
1. Compare explicações entre TODOS os capítulos: a mesma ideia foi acrescentada
duas vezes? Indique os dois blocos e o mecanismo/condição repetido. Recapitulação
curta com função didática não é defeito; informações exclusivas devem permanecer.
2. Localize relato de leitura: 'fabricante consultado', 'no contexto consultado',
'no caso relatado', 'a fonte afirma' e equivalentes. O contexto deve ensinar o
conceito diretamente, com condições explícitas, sem depender da leitura da fonte.
3. Confira termos em inglês sem explicação em português brasileiro no primeiro uso.
Os sinais locais são pistas; procure também falhas que não estejam nesses sinais.
Ignore aprovações anteriores. Para cada defeito dê IDs de blocos e descreva o
problema específico e o reparo necessário, sem reescrever o documento. Não crie
falhas para preencher a resposta e não peça pesquisa por lacunas de conteúdo.
JSON {"problemas":[{"blocos":["B01_01","B02_01"],"descricao":"defeito e reparo localizado"}]}.
'''
