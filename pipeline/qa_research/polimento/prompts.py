from pipeline.qa_research.v3.prompts import BASE

DIAGNOSE = (
    BASE
    + """
Você prepara o POLIMENTO INCREMENTAL de um documento técnico existente.
A base já recebeu revisão editorial e correções do especialista. Preserve sua
profundidade, mecanismos, condições, exceções e distinções úteis. Leia a frase
integral do especialista e os recortes curados. Não replaneje os temas nem troque
o documento por uma síntese nova. Conteúdo adequado fica intocado.

Proponha no máximo o limite configurado de intervenções, priorizando erro técnico e lacuna essencial.
Tipos permitidos:
- correcao_tecnica: erro, generalização indevida, condição de processo/FPSO ou exceção importante ausente.
- lacuna_essencial: parte obrigatória do escopo/frase do especialista ainda não ensinada.
- aprofundamento: ganho técnico e operacional pertinente ao escopo.
- editorial: clareza, autonomia textual (remoção de relato de leitura), organização ou eliminação de redundância entre capítulos, sem acrescentar fatos novos.

Regras estritas de decomposição e alvos:
1. Para toda intervenção técnica (correcao_tecnica, lacuna_essencial, aprofundamento), decomponha o objetivo em 1 a 3 `sub_objetivos` atômicos, concretos e verificáveis (ex.: S1 = mecanismo de atuação, S2 = condição de compatibilidade/limite operacional). Para `editorial`, `sub_objetivos` deve ser `[]`.
2. Limites opcionais não são lacunas essenciais. Não exija dosagens universais, parâmetros de fabricante, normas ou matrizes completas se não forem indispensáveis.
3. As `protecoes` registram correções do especialista que precisam permanecer válidas.
4. Use IDs dos blocos (`B01_01`) para reparos; IDs de capítulo (`C01`) para acrescentar blocos; `DOCUMENTO` somente para capítulo realmente ausente. Não atribua o mesmo bloco a intervenções distintas.
5. Consultas PT/EN são expressões técnicas específicas (até 16 palavras por idioma, máximo 3 pares), focadas no equipamento, fluido, mecanismo e função operacional. Para `editorial`, `consultas` pode ser `[]`; para intervenções técnicas, ao menos 1 par PT/EN é obrigatório.
6. Em `cobertura`, avalie TODOS os pontos curados sem criar IDs novos. Respeite o histórico de pontos já atendidos na base: não rebaixe um ponto já atendido para parcial sem apontar exatamente qual parte obrigatória da frase do especialista falta. Omissões da frase que o mapa não representa ficam em `omissoes_escopo`.

Retorne exclusivamente o JSON:
{"intervencoes":[{"id":"I01","tipo":"correcao_tecnica|lacuna_essencial|aprofundamento|editorial",
"prioridade":"alta|media|baixa","alvos":["B01_01"],"pontos":["F01"],
"objetivo":"o que melhorar","motivo":"por que é necessário",
"sub_objetivos":[{"id":"S1","descricao":"subproblema concreto 1"}],
"consultas":[{"pt":"...","en":"..."}]}],
"cobertura":[{"id":"F01","estado":"atendido|parcial|ausente","motivo":"..."}],
"omissoes_escopo":[]}
"""
)

RESEARCH = (
    BASE
    + """
Investigue SOMENTE a necessidade técnica da intervenção e seus `sub_objetivos`.
Você recebe passagens originais herdadas da pesquisa anterior e/ou de coleções
profissionais novas. Avalie pertinência, estatuto, equipamento, materiais, condições,
exceções e limites. Não transforme resultado de fabricante em desempenho universal
ou recomendação estrangeira em obrigação brasileira. Uma referência normativa sem
edição/vigência verificada não autoriza afirmar que a regra é atual; relate essa pendência.

Regras estritas de vinculação a `sub_objetivos`:
1. Extraia até oito relações úteis com suas condições e limites.
2. Classifique `pertinencia="direta"` SOMENTE quando a proposição responde concretamente a pelo menos um dos `sub_objetivos` listados na intervenção. Informe em `sub_objetivos_atendidos` os IDs exatos (ex.: `["S1"]`) que esse achado sustenta.
3. Conteúdo tangencial, genérico ou que aborda apenas outro aspecto do sistema (ex.: gestão de mudança quando o sub-objetivo pede restauração de backup) deve receber `pertinencia="contextual"` e `sub_objetivos_atendidos=[]`.
4. Defina `suficiente=true` somente se TODOS os `sub_objetivos` da intervenção tiverem pelo menos um achado com `pertinencia="direta"`. Se algum sub-objetivo continuar sem cobertura direta, defina `suficiente=false`, indique o que falta em `pendencias` e proponha até três consultas PT/EN curtas (máximo 16 palavras) focadas especificamente nos sub-objetivos descobertos.
5. Cite apenas os IDs de parágrafos fornecidos nesta leitura; não copie citações literais nem cite parágrafos de rodadas anteriores que não estejam no pacote atual.

Retorne exclusivamente o JSON:
{"suficiente":true,"achados":[{"proposicao":"relação técnica útil",
"citacoes":["N...P01"],"tipo":"explicacao_tecnica|resultado_experimental|recomendacao|opiniao|norma|indeterminado",
"pertinencia":"direta|contextual","sub_objetivos_atendidos":["S1"],
"condicoes":["..."],"limites":["..."]}],"consultas_adicionais":[],"pendencias":[]}
"""
)

EDIT = (
    BASE
    + """
Edite SOMENTE os alvos das intervenções recebidas. O documento existente é a base
e precisa conservar suas explicações úteis e as `protecoes` do especialista.
Não devolva uma reescrita integral, não resuma capítulos nem transfira conhecimento
para notas. Não há meta de aumentar ou reduzir palavras.

Regras de suporte e escopo por sub-objetivo:
1. Resolva apenas os `sub_objetivos_com_suporte` usando os achados, condições e limites fornecidos. Se houver `sub_objetivos_sem_suporte`, registre-os em `pendencias` e NÃO invente nem extrapole fatos laterais para aparentar que foram resolvidos.
2. Conceitos consolidados de engenharia podem complementar a explicação didática: declare-os em `complementos` e nunca atribua esse conteúdo ao corpus. Dados empíricos, números operacionais, dosagens e requisitos normativos exigem suporte em `achados`. Edição do tipo `editorial` não cria fatos novos (`achados=[]`, `complementos=[]`).
3. No corpo do texto: escreva texto técnico didático e autônomo em PT-BR, sem IDs, sem citações, sem referências e sem relato de leitura. Proibido usar expressões como 'fabricante consultado', 'no contexto consultado', 'no caso relatado', 'a fonte afirma', 'é descrito como' ou 'são citados'. Converta em explicação direta explicitando a condição de validade, o fluido, o material e o equipamento (ex.: em FPSO).
4. Compare cada alteração com o restante do documento recebido: não repita a mesma explicação de mecanismo em capítulos diferentes. Mantenha o mecanismo completo no capítulo próprio e mencione apenas a interação operacional específica no outro.
5. Explique no primeiro uso termos estrangeiros não triviais, mantendo termos consagrados de petróleo (offloading, topside, subsea, pig, squeeze, bottle test) com clareza contextual.
6. Identifique cada operação com um `op_id` sequencial único (`I01_OP01`, `I01_OP02`, ...).
   - `substituir` / `remover`: exigem `alvo` de bloco existente (`B...`).
   - `inserir`: exige `alvo` de bloco (`B...`, insere logo após) ou capítulo (`C...`, insere ao final).
   - `novo_capitulo`: usa `alvo="DOCUMENTO"` e preenche `capitulo` e `grupo`.
   - `mover`: usa `alvo` (`B...`) e `destino` (`C...`).
   - `renomear_capitulo`: usa `alvo` (`C...`) e novo título em `capitulo`.
7. Em `preservacao`, explique concretamente onde permaneceram todos os mecanismos, condições e exceções do bloco original (ou em qual bloco do documento o conceito já está preservado, no caso de remoção de redundância).

Retorne exclusivamente o JSON:
{"itens":[{"id":"I01","alteracoes":[{"op_id":"I01_OP01",
"operacao":"substituir|inserir|remover|novo_capitulo|mover|renomear_capitulo",
"alvo":"B01_01","subtitulo":"...","texto":"...","motivo":"...",
"preservacao":"onde cada mecanismo e condição original foi mantido",
"achados":["I01_A01"],"complementos":[]}],"pendencias":[]}]}
"""
)

REVIEW = (
    BASE
    + """
Você é o Auditor Técnico e Editorial Diferencial. Avalie CADA OPERAÇÃO (`op_id`)
individualmente comparando `estado_anterior_do_bloco` com `estado_proposto_pela_operacao`,
a frase do especialista, as `protecoes_especialista`, as `evidencias_fornecidas`
e o `mapa_estrutural_documento_vigente_ANTES_deste_lote`.

ATENÇÃO A TRÊS REGRAS CRÍTICAS DE JULGAMENTO:
1. DISTINÇÃO ENTRE BASE ANTERIOR E INSERÇÃO NOVA (`status_existencia_alvo`):
   - Quando `status_existencia_alvo == "CRIACAO_DE_BLOCO_OU_CAPITULO_NOVO_NESTA_PROPOSTA"`, o bloco proposto NÃO existia no documento antes desta operação. NÃO rejeite uma inserção alegando que ela já consta na proposta que você está avaliando. Só existe repetição se o mesmo mecanismo/conteúdo já constar em outro bloco preexistente listado em `mapa_estrutural_documento_vigente_ANTES_deste_lote` ou `contexto_blocos_vizinhos_no_capitulo`.
2. DUPLO REGIME DO CRITÉRIO `suportada` (`modo_validacao_suporte`):
   - Se `modo_validacao_suporte == "MODO_PRESERVACAO_EDITORIAL_SEM_FATOS_NOVOS"` (intervenções editoriais e acabamento): o objetivo é limpar relato de fonte, melhorar clareza ou condensar redundância entre blocos existentes. As afirmações técnicas já pertencem à base herdada! Portanto, marque `suportada=true` desde que a edição NÃO invente fatos, números, normas ou generalizações novas além do que já estava em `estado_anterior_do_bloco`. É PROIBIDO reprovar edição editorial por ausência de `achados` novos para fatos que já estavam no bloco original.
   - Se `modo_validacao_suporte == "EXIGE_EVIDENCIA_NOVA_PARA_FATOS_NOVOS"`: toda afirmação empírica, parâmetro, condição de equipamento ou mecanismo novo acrescentado ao bloco exige suporte nas `evidencias_fornecidas` (respeitando suas condições e limites) ou declaração legítima em `complementos` para conceitos básicos de engenharia.
3. JULGAMENTO INDEPENDENTE POR OPERAÇÃO (`op_id`):
   - Avalie cada `op_id` separadamente. Um defeito em `E01_OP02` NÃO deve reprovar `E01_OP01` se `E01_OP01` estiver correto e autônomo.
   - Verifique os 7 critérios booleanos para cada `op_id`:
     * `correta`: tecnicamente exata no domínio de óleo, gás e FPSO.
     * `suportada`: atende ao regime de suporte acima sem extrapolar evidências.
     * `condicoes_preservadas`: não converteu caso específico, condição de fluido/pH/pressão ou recomendação localizada em regra universal irrestrita.
     * `sem_perda`: nenhum mecanismo, exceção ou condição técnica útil do `estado_anterior_do_bloco` foi perdido (ou está explicitamente preservado no bloco irmão indicado em `preservacao`).
     * `escopo`: pertence estritamente ao subtópico e à frase do especialista.
     * `autonomia`: `false` se o texto contiver qualquer relato de leitura ('fabricante consultado', 'no contexto consultado', 'no caso relatado', 'a fonte afirma', 'é descrito como', 'são citados').
     * `pt_br`: português brasileiro técnico natural, com termos estrangeiros novos explicados no primeiro uso.
   - `decisao="aprovar"` exige todos os 7 critérios `true`. Use `"corrigir"` quando o defeito for recuperável por ajuste localizado no texto (forneça a instrução exata em `correcao`). Use `"rejeitar"` somente quando não houver suporte factual possível ou a operação for irremediavelmente fora de escopo.

Retorne exclusivamente o JSON:
{"avaliacoes_operacoes":[{"op_id":"I01_OP01","intervencao_id":"I01",
"decisao":"aprovar|corrigir|rejeitar","motivo":"...",
"correcao":"instrução concreta e localizada para o editor corrigir, ou vazio",
"criterios":{"correta":true,"suportada":true,"condicoes_preservadas":true,
"sem_perda":true,"escopo":true,"autonomia":true,"pt_br":true}}]}
"""
)

EDITORIAL_AUDIT = (
    BASE
    + """
Faça uma leitura editorial crítica do documento inteiro.
Sua tarefa é SOMENTE encontrar defeitos concretos de escrita, autonomia e redundância,
sem avaliar cobertura de escopo, sem pedir pesquisa externa e sem reescrever o documento.

Procure especificamente quatro categorias de defeito (`tipo_defeito`):
1. `repeticao_entre_capitulos`: a mesma explicação de mecanismo ou condição foi repetida em dois capítulos/blocos diferentes sem função didática. Indique exatamente o par de blocos (`["B04_05", "B05_05"]`), qual bloco deve concentrar a explicação principal e qual deve manter apenas a consequência/interação local.
2. `relato_de_leitura`: expressões que denunciam colagem de fonte, como 'fabricante consultado', 'no contexto consultado', 'no caso relatado', 'a fonte afirma', 'é descrito como muito eficaz', 'são citados produtos', 'outras alternativas citadas são'. Indique o bloco (`["B01_01"]`) e o trecho exato a converter em voz técnica autônoma com condições preservadas.
3. `termo_ingles`: termo técnico em inglês não trivial usado sem explicação em português brasileiro no primeiro uso (siglas e termos consagrados de uso diário como FPSO, topside, subsea, offloading e pig não são defeito se o contexto estiver claro).
4. `organizacao`: bloco deslocado de capítulo ou subtítulo incoerente com o conteúdo do bloco.

Regras:
- Cada item em `problemas` deve listar no máximo 2 ou 3 blocos diretamente acoplados pelo mesmo defeito. Não agrupe o documento inteiro em um único item.
- Não crie defeitos artificiais para preencher lista. Se o documento estiver limpo, retorne `"problemas": []`.

Retorne exclusivamente o JSON:
{"problemas":[{"blocos":["B04_05","B05_05"],
"tipo_defeito":"repeticao_entre_capitulos|relato_de_leitura|termo_ingles|organizacao",
"descricao":"descrição exata do defeito e como reparar sem perder condições técnicas"}]}
"""
)

EDITORIAL = (
    EDIT
    + """
MODO DE MICRO-ACABAMENTO EDITORIAL LOCALIZADO:
Você está recebendo um micro-lote de acabamento editorial (máximo de 3 blocos acoplados).
A base recebida já contém as alterações técnicas aprovadas.
Regras estritas desta etapa:
1. Corrija APENAS os defeitos editoriais apontados nos blocos autorizados da micro-intervenção (`E01`, `E02`...), usando exclusivamente as operações `substituir` ou `remover`.
2. É PROIBIDO acrescentar fatos novos, números, dosagens, limites, normas ou recomendações externas. `achados` e `complementos` devem ser obrigatoriamente listas vazias `[]`.
3. Ao remover relato de leitura ('no contexto consultado', 'é descrito como', etc.), NÃO transforme uma condição específica do fluido/equipamento em verdade universal irrestrita; mantenha a condição técnica explícita na frase (ex.: 'Em sistemas de água do mar com presença de cloro residual...').
4. Ao eliminar redundância entre dois blocos, preserve 100% das condições exclusivas de cada bloco e declare detalhadamente em `preservacao` em qual bloco cada mecanismo permaneceu.
"""
)

CONSOLIDATE = (
    BASE
    + """
Avalie a edição consolidada final contra a frase de escopo do especialista, as
`protecoes` do especialista, a `cobertura_anterior` e os sinais editoriais locais.

Regras de julgamento final:
1. Verifique se todas as `protecoes` do especialista continuam semanticamente preservadas (`protecoes_preservadas=true`).
2. Liste em `problemas` apenas defeitos reais remanescentes no texto atual:
   - `tipo="editorial"` para relato de leitura residual, duplicação de parágrafos ou falha grave de PT-BR.
   - `tipo="tecnico"` para contradição interna entre blocos, perda de condição essencial ou erro factual.
   - Marque `critico=true` para erros técnicos, perda de proteção do especialista ou relato de fonte explícito que impeça publicar o texto para geração de questões.
3. ESTABILIDADE DA COBERTURA (`cobertura`):
   - Avalie todos os pontos curados com os mesmos IDs do diagnóstico.
   - Compare com `cobertura_anterior`: se um ponto já estava `atendido` e nenhuma informação dele foi apagada, mantenha `atendido`. Só rebaixe um ponto de `atendido` para `parcial` se você preencher `evidencia_regressao` explicando exatamente qual requisito obrigatório da frase do especialista está ausente no texto atual. Não exija aprofundamentos opcionais para marcar `atendido`.

Retorne exclusivamente o JSON:
{"protecoes_preservadas":true,
"problemas":[{"blocos":["B01_01"],"descricao":"...","tipo":"tecnico|editorial","critico":true}],
"cobertura":[{"id":"F01","estado":"atendido|parcial|ausente","motivo":"...","evidencia_regressao":""}],
"omissoes_escopo":[]}
"""
)
