"""Prompts do refino. Todos pedem JSON; os contratos ficam em contracts.py."""
from pipeline.qa_research.v2.language import POLICY

ESTILO = '''Padrão do documento final (critérios do especialista que revisou a versão anterior):
- Texto técnico autônomo, didático e organizado, para quem trabalha embarcado em FPSO no Brasil.
  Introduz o assunto, apresenta os componentes e suas funções, explica como se relacionam e segue
  uma sequência lógica (o que é → de que é feito → como funciona → como se opera e controla →
  problemas operacionais típicos → segurança, integridade e regulação → interfaces com outros sistemas).
- Contexto real de FPSO/UEP ancorada (turret ou spread mooring) e das correntes de fluido de um FPSO.
  Não trate de refinaria, coqueamento, perfuração, plantas onshore ou unidades de outro tipo,
  salvo como contraste curto e explícito.
- Sem casuística: nada de nomes de unidades, TAGs, válvulas identificadas, datas, relatórios de
  investigação ou "no incidente analisado". Uma lição aprendida vira princípio geral.
- Sem relato de leitura: não escreva "a fonte afirma", "o trecho", "o documento analisado",
  "segundo o estudo". O texto explica o assunto diretamente.
- Cada conceito é definido e explicado uma única vez. Não repita a mesma ideia em seções diferentes.
- Terminologia de bordo usada no Brasil (o critério é o termo falado a bordo, que às vezes é o
  anglicismo consagrado): header, turret, torre do flare, disco de ruptura, ventilação de tanques,
  falha segura, distúrbio, teste de poço, golpe de aríete, intertravamento, amarra (linha de
  ancoragem), eslinga, olhal, guindasteiro, homem de área, sinaleiro, supervisor/sinalizador,
  biocida, planicidade, água doce, capacidade de pouso, boca de sino.
- Siglas expandidas na primeira ocorrência, com o nome em português quando houver.
- Regulação brasileira (ANP, NRs do MTE, Marinha/NORMAM, IBAMA/CONAMA) é citada quando pertinente.
  Não afirme vigência, versão ou número de item de norma sem evidência.
- Números, limites, dosagens, tempos e valores de norma só com evidência ou quando já constam do
  texto revisado pelo especialista. Sem isso, descreva qualitativamente.
''' + POLICY

MAPA = '''Responda apenas JSON. Você organiza uma coleção de 40 documentos técnicos sobre FPSO, um por
tópico. O especialista observou que os mesmos conceitos se repetem na maioria dos textos.
Identifique os conceitos compartilhados que mais tendem a reaparecer entre documentos (por exemplo,
hidratos, barreiras de segurança, permissão de trabalho, gestão de mudanças, garantia de escoamento,
ESD/shutdown, gás inerte, detecção de gás) e atribua a cada um o documento DONO, aquele cujo tópico
é o lugar natural do desenvolvimento completo. Para os outros documentos que precisam tocar no
conceito, diga o enfoque específico daquele tópico (uma frase), para que o texto mencione o
conceito sob esse ângulo sem redefini-lo.
Use somente IDs de documento recebidos. Entre 30 e 120 conceitos, nomes curtos e distintos.
JSON {"conceitos":[{"conceito":"...","dono":"02_11","motivo":"...","mencoes":[{"doc":"02_02","enfoque":"..."}]}]}
'''

PLANO = '''Responda apenas JSON. Você vai planejar a NOVA versão de um documento técnico de contexto.
A versão anterior foi revisada por um especialista de FPSO; o texto revisado (sem os trechos que ele
mandou remover), o comentário literal dele, as lacunas que ele listou e, quando houver, a análise de
lacunas por LLM que ele mesmo curou estão na entrada. O documento será reescrito com roteiro novo.
Monte o roteiro:
- Primeira seção do tipo "introducao": situa o tópico no FPSO, define o objeto e apresenta a
  organização do documento. As demais seguem a sequência lógica do padrão abaixo, adaptada ao tópico.
- Cada seção tem objetivo e conhecimentos (o que o leitor precisa saber ao final), cada um com as
  lacunas do especialista que atende (IDs G.. e L..) e se é essencial.
- Toda lacuna recebida aparece em pelo menos um conhecimento ou em lacunas_fora_de_escopo, com
  justificativa (use isso só quando a lacuna pertence claramente a outro documento da coleção).
- Todo bloco da base vai para uma seção (blocos_base, para reaproveitar o conteúdo) ou para
  blocos_descartados com motivo: casuistico, fora_fpso, fora_escopo ou redundante.
- Conceitos de que este documento é dono são desenvolvidos aqui; conceitos de outros donos só
  aparecem sob o enfoque indicado, sem redefinição.
- Consultas de pesquisa por seção: pares PT/EN técnicos e específicos, de 3 a 16 palavras.
- O documento não deve ficar raso: cubra o tópico com a abrangência que o especialista cobrou.
''' + ESTILO + '''
JSON {"secoes":[{"id":"S01","tipo":"introducao|desenvolvimento","titulo":"...","objetivo":"...",
"conhecimentos":[{"id":"S01K01","descricao":"...","lacunas":["G01"],"essencial":true}],
"blocos_base":["B001"],"consultas":[{"pt":"...","en":"..."}]}],
"blocos_descartados":[{"id":"B009","motivo":"casuistico","justificativa":"..."}],
"lacunas_fora_de_escopo":[{"id":"G07","justificativa":"..."}]}
'''

PERSPECTIVAS = {
    'operacao': '''Escreva como um supervisor de produção experiente em FPSO no Brasil: rotina de sala de
controle e de área, alinhamentos, partidas e paradas, controles, variáveis acompanhadas, problemas
operacionais típicos, como se reconhecem e como se responde a eles.''',
    'engenharia': '''Escreva como um engenheiro de processo e equipamentos de FPSO: componentes, princípios
de funcionamento, arquitetura do sistema, critérios de seleção e projeto, faixas de aplicação e
interfaces com os demais sistemas da planta.''',
    'sms_integridade': '''Escreva como um engenheiro de segurança, integridade e conformidade de FPSO: barreiras,
cenários de risco, inspeção e manutenção, modos de falha, requisitos regulatórios brasileiros
pertinentes (ANP, NRs do MTE, Marinha, IBAMA/CONAMA) e lições aprendidas generalizadas.''',
}

RASCUNHO = '''Responda apenas JSON. Você escreve, com o seu próprio conhecimento técnico (sem consulta),
o conteúdo de UMA seção de um documento técnico sobre FPSO, como afirmações atômicas: cada uma é
uma informação técnica completa e autossuficiente, em 1 a 3 frases, em português brasileiro.
Cubra os conhecimentos da seção com profundidade de quem conhece a prática a bordo. Não repita
assunto de outras seções do roteiro. Não invente números: quando um valor depende de projeto,
fabricante ou norma, explique de que depende. Marque especifico=true quando a afirmação contém
número, limite, dosagem, tempo, item ou versão de norma.
Tipos: conceito, componente, funcao, mecanismo, procedimento, controle, problema, seguranca,
regulacao, interface.
''' + ESTILO + '''
JSON {"afirmacoes":[{"id":"A01","texto":"...","conhecimentos":["S02K01"],"tipo":"componente","especifico":false}]}
'''

LEITURA = '''Responda apenas JSON. Você é um pesquisador. Leia as passagens recuperadas dos corpora e
extraia achados úteis para os conhecimentos da seção: mecanismo, componente, condição, critério,
procedimento, problema, controle, exceção, requisito. Cada achado é uma síntese técnica em português
brasileiro, em 1 a 3 frases, com as passagens que o sustentam (IDs E..). Indique condições e a
jurisdição quando a passagem for de outro país; não transforme regra estrangeira em requisito
brasileiro. Generalize relatos de incidente em princípios. Ignore passagens irrelevantes.
Verifique também as afirmações dos rascunhos listadas: "apoia" quando uma passagem sustenta a
afirmação, "contradiz" quando uma passagem a contraria (diga o quê). Não verifique o que as
passagens não tratam.
Informe os conhecimentos ainda sem suporte (lacunas) e, para eles, até quatro novas consultas
PT/EN diferentes das anteriores.
JSON {"achados":[{"id":"F01","texto":"...","fontes":["E..."],"conhecimentos":["S02K01"],"condicoes":"...","jurisdicao":"BR"}],
"verificacoes":[{"afirmacao":"W1A03","estado":"apoia","fontes":["E..."],"nota":"..."}],
"lacunas":["S02K03"],"novas_consultas":[{"pt":"...","en":"..."}]}
''' + POLICY

CONSOLIDACAO = '''Responda apenas JSON. Você consolida o material de UMA seção em unidades de conteúdo
sem redundância. Entradas: afirmações escritas por vários redatores (IDs W..A..), com o resultado da
verificação nos corpora; achados da pesquisa (IDs F..) e blocos do texto revisado pelo especialista
(IDs B..).
Regras:
- Afirmações equivalentes ou sobrepostas viram UMA unidade, que reúne o que cada uma tem de útil.
- Prefira a formulação sustentada por achado; quando a evidência for pobre ou ausente, complemente
  com as afirmações dos redatores (conhecimento do modelo é aceito como complemento).
- Afirmação contradita por achado: corrija com o achado ou descarte.
- Descarte o que for casuístico, fora do contexto FPSO, fora do escopo da seção, duplicado ou valor
  numérico sem evidência (quando o valor não vem de achado nem de bloco revisado).
- Conceitos de outros donos aparecem só sob o enfoque indicado, sem redefinição.
- Cada ID recebido aparece exatamente uma vez: na origem de uma unidade ou em descartadas.
- Ordene as unidades na sequência lógica em que serão escritas.
''' + ESTILO + '''
JSON {"unidades":[{"id":"U01","texto":"...","conhecimentos":["S02K01"],"origem":{"afirmacoes":["W1A01"],"achados":["F02"],"blocos":["B004"]}}],
"descartadas":[{"ref":"W3A07","motivo":"duplicada|contradita|casuistica|fora_fpso|fora_escopo|valor_sem_fonte|irrelevante"}],
"conflitos":[{"descricao":"...","resolucao":"..."}]}
'''

REDACAO = '''Responda apenas JSON. Redija UMA seção do documento a partir das unidades de conteúdo, em
blocos com subtítulo. Use todas as unidades, cada uma exatamente uma vez, na ordem que favorecer a
explicação. Pode acrescentar ligações, transições e explicações didáticas, mas não fatos novos.
Parágrafos densos e claros; nada de listas soltas sem explicação. Para a introdução, situe o tópico
no FPSO e apresente o que as seções seguintes tratam, sem antecipar o desenvolvimento delas.
''' + ESTILO + '''
JSON {"blocos":[{"id":"S02B01","subtitulo":"...","texto":"parágrafo 1\\n\\nparágrafo 2","unidades":["U01","U02"]}]}
'''

CONSOLIDA_DOC = '''Responda apenas JSON. Você é o consolidador final do documento. Recebe o documento
completo (blocos com IDs), pares de sentenças quase repetidas detectados automaticamente e os
conceitos de que outros documentos são donos. Elimine a redundância: cada ideia fica no bloco mais
adequado; nos demais, remova ou troque por uma remissão curta à seção correspondente. Não perca
informação: toda informação distinta permanece em algum bloco. Similaridade automática é pista,
não ordem: repetição necessária para a compreensão local pode ficar, em forma curta.
Corrija também ligações quebradas entre seções. Altere só os blocos necessários.
''' + ESTILO + '''
JSON {"operacoes":[{"bloco":"S04B02","novo_texto":"...","motivo":"...","informacao_preservada_em":["S02B01"]}]}
'''

REVISAO = '''Responda apenas JSON. Revise o documento como o especialista de FPSO revisaria.
1) Cobertura: para cada lacuna recebida (IDs G.. e L..), estado atendido, parcial ou ausente, e os
   blocos que a atendem.
2) Problemas por bloco: erro_tecnico, fora_fpso, casuistico, relato_fonte, terminologia,
   valor_sem_fonte, redundancia, superficial, estrutura, pt_br. Descreva e diga a correção.
   Alertas locais recebidos são pistas: confirme ou descarte.
3) Parecer geral curto.
Não aponte problema sem localização. Não peça para alongar o que já está completo.
''' + ESTILO + '''
JSON {"cobertura":[{"id":"G01","estado":"atendido","blocos":["S02B01"],"nota":"..."}],
"problemas":[{"bloco":"S03B02","tipo":"fora_fpso","descricao":"...","correcao":"..."}],
"parecer":"..."}
'''

COBERTURA_BASE = '''Responda apenas JSON. Avalie se o texto recebido atende cada lacuna listada pelo
especialista (IDs G.. e L..): atendido, parcial ou ausente, com os blocos que a atendem. Seja
rigoroso e use o mesmo critério para qualquer versão do documento.
JSON {"cobertura":[{"id":"G01","estado":"parcial","blocos":["B003"],"nota":"..."}]}
'''

REPARO = '''Responda apenas JSON. Corrija os blocos indicados conforme os problemas apontados na revisão.
Reescreva só esses blocos, preservando toda informação correta deles. Para acrescentar conteúdo
cobrado, use as unidades e achados fornecidos e, quando eles não bastarem, o seu conhecimento técnico
como complemento (sem números sem evidência).
''' + ESTILO + '''
JSON {"blocos":[{"id":"S03B02","subtitulo":"...","texto":"..."}]}
'''
