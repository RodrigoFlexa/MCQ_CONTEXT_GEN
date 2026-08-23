"""
prompts_fase3.py — todos os prompts LLM do pipeline da fase 3.

Um lugar só para o texto dos prompts, para que o notebook fique com o fluxo e
não com parágrafos. Cada função devolve `(system, user)` pronto para
`AzureOpenAIBackend.complete(...)`.

Papéis e modelos (definidos em `utils_fase3.Config`):

    extrator     gpt-4o-mini   quebra a instrução longa do subtópico em facetas
    consolidador gpt-4o-mini   resume N trechos do Petrolês num documento enxuto
    gerador      gpt-5         escreve o lote de questões
    judge        gpt-5         julga corretude, qualidade [0,1] e dificuldade
    refinador    gpt-5         corrige questões que o scorer de vícios reprovou

Divisão de trabalho — o gerador escreve enunciado, alternativas e gabarito, e
mais uma coisa: uma autoavaliação de dificuldade (`dificuldade_gerador`), com
a MESMA rubrica do judge. Isso não duplica o trabalho do judge — a nota e o
`difficulty` oficiais continuam vindo só dele — é um segundo sinal, barato de
pedir (o gerador já está olhando pra questão inteira), que permite comparar as
duas avaliações e mirar uma distribuição de dificuldade no lote. O gerador não
redige justificativa da correta. A posição do gabarito também não é problema
dele: é embaralhada deterministicamente no pós-processamento
(`utils_fase3.embaralhar_posicao`), porque pedir distribuição de POSIÇÃO a um
modelo é gastar atenção dele com algo que uma linha de código resolve melhor.

Os critérios do judge são deliberadamente próximos do formulário aplicado aos
especialistas na fase 2 ("Clareza do enunciado", "Qualidade das alternativas de
resposta", "Correção técnica", "Relevância para a operação de FPSOs"), para que
a nota automática seja comparável ao julgamento humano que a originou.
"""

from __future__ import annotations

import json
from typing import Any, Sequence

# ===========================================================================
# 1. EXTRATOR DE FACETAS  (gpt-4o-mini)
# ===========================================================================
# As instruções dos subtópicos em `topicos.py` têm de 350 a 6.400 caracteres e
# enumeram muitos assuntos independentes numa frase só. Usar esse parágrafo
# inteiro como query dilui a busca (o embedding vira uma média de dez assuntos)
# e, na geração, dá sempre o mesmo alvo — as rodadas se repetem.
#
# O extrator quebra a instrução em facetas. Cada faceta é, ao mesmo tempo:
#   - uma query de busca (semântica) + um léxico (busca lexical);
#   - o alvo declarado de uma rodada de geração.
# É o que dá diversidade entre rodadas sem inventar assunto fora da instrução.

SYS_EXTRATOR = """
Você é um analista técnico da indústria de óleo e gás offshore (FPSO).
Sua tarefa é decompor a instrução de um especialista sobre um subtópico em
FACETAS independentes, para orientar busca documental e geração de questões.

Regras:
- Cada faceta cobre UM recorte técnico coerente da instrução. Não invente
  assunto que não esteja na instrução; não repita a mesma ideia em duas facetas.
- `foco` reescreve, em 1-2 frases, o que uma questão sobre essa faceta deve
  cobrir — na mesma voz da instrução do especialista ("As questões devem...").
- `query` é uma frase densa em termos técnicos, para busca semântica em um
  corpus em português de óleo e gás. Não use pronomes nem referências vagas.
- `termos_fortes` são expressões que praticamente só aparecem em texto sobre
  essa faceta (2 a 4 palavras, específicas). `termos_apoio` são termos do
  domínio, mais genéricos, que reforçam a evidência.
- Termos em minúsculas, SEM acentos, no singular quando fizer sentido. Prefira
  a forma por extenso E a sigla como termos separados ("fogo e gas", "f&g").
- Sem redundância entre termos_fortes e termos_apoio.
""".strip()


def prompt_extrator(topico: str, subtopico: str, instrucao: str,
                    n_facetas: int) -> tuple[str, str]:
    user = f"""
Tópico: {topico}
Subtópico: {subtopico}

Instrução do especialista:
\"\"\"
{instrucao.strip()}
\"\"\"

Decomponha em no máximo {n_facetas} facetas (menos, se a instrução for curta).

Retorne apenas JSON:
{{
  "facetas": [
    {{
      "titulo": "nome curto da faceta",
      "foco": "As questões devem abordar ...",
      "query": "frase densa em termos técnicos para busca semântica",
      "termos_fortes": ["medicao fiscal", "transferencia de custodia"],
      "termos_apoio": ["vazao", "calibracao"]
    }}
  ]
}}
""".strip()
    return SYS_EXTRATOR, user


# ===========================================================================
# 2. CONSOLIDADOR  (gpt-4o-mini)
# ===========================================================================
# O corpus Petrolês é texto cru, uma sentença por linha, sem fronteira de
# documento e com números mascarados como <NUMBER>. Jogar 6 trechos brutos no
# prompt do gerador gasta contexto com ruído. O consolidador transforma os
# trechos num documento técnico enxuto — sem acrescentar conhecimento.

SYS_CONSOLIDADOR = """
Você é um redator técnico da indústria de óleo e gás offshore (FPSO).
Recebe trechos brutos de um corpus em português (texto sem formatação, números
mascarados como <NUMBER>, frases possivelmente truncadas) e os consolida em um
documento técnico único, limpo e denso.

Regras inegociáveis:
- NÃO acrescente conhecimento que não esteja nos trechos. Nada de completar
  lacunas com o que você sabe do domínio.
- Preserve o conhecimento técnico específico: mecanismos, causas, critérios,
  procedimentos, relações de causa e efeito, condições de contorno, trade-offs.
- Descarte ruído: cabeçalhos, referências bibliográficas, sobras de sumário,
  frases truncadas sem conteúdo, repetição entre trechos.
- Marque como `<NUMBER>` os números que vierem mascarados; não invente valores.
- Se os trechos forem pobres ou fora do assunto, diga isso explicitamente na
  primeira linha com o prefixo `AVISO:` e consolide só o que houver de útil.
- Português brasileiro, prosa técnica corrida com subtítulos curtos. Sem
  introdução, sem conclusão, sem meta-comentário sobre a tarefa.
""".strip()


def prompt_consolidacao(subtopico: str, faceta_foco: str,
                        trechos: Sequence[str], max_palavras: int) -> tuple[str, str]:
    blocos = "\n\n".join(
        f"[trecho {i + 1}]\n{t.strip()}" for i, t in enumerate(trechos)
    )
    user = f"""
Subtópico: {subtopico}
Recorte de interesse: {faceta_foco}

Consolide os trechos abaixo em um documento técnico de no máximo
{max_palavras} palavras, priorizando o que for relevante ao recorte de
interesse e descartando o resto.

{blocos}
""".strip()
    return SYS_CONSOLIDADOR, user


# ===========================================================================
# 3. GERADOR  (gpt-5)
# ===========================================================================
# Herdeiro do PORTUGUESE_V15 da fase 2 (`pipeline/prompts/prompt_mcq_generation.py`),
# com três acréscimos: a instrução do especialista para a faceta, few-shot
# amostrado do banco de questões de alto score, e o documento consolidado como
# única fonte factual.
#
# O escopo é estreito de propósito: enunciado, alternativas, gabarito e uma
# autoavaliação de dificuldade. Justificativa e posição da correta continuam
# saindo daqui, para o modelo gastar atenção no que só ele faz.

SYS_GERADOR = """
Você cria questões de múltipla escolha de alta qualidade em português brasileiro
com gabarito, no domínio de unidades offshore de produção de petróleo (em
especial FPSOs).

CRITÉRIOS DE QUALIDADE (toda questão deve atender):
1. Testa RACIOCÍNIO sobre o conteúdo, não localização de fatos. Se a resposta
   pode ser obtida com Ctrl+F no documento, REFAZER.
2. O enunciado apresenta um CONTEXTO (cenário operacional, caso, afirmação a
   avaliar, comparação a fazer).
3. Cada distrator é uma POSIÇÃO ALTERNATIVA PLAUSÍVEL — outro mecanismo, outro
   componente, outra prioridade ou outra interpretação técnica que um
   profissional da indústria poderia defender à primeira vista — e captura um
   erro de raciocínio específico. O distrator NUNCA é uma versão exagerada,
   extremada ou caricata da alternativa correta: ele erra pelo CONTEÚDO, não
   pela forma da redação.
4. PARIDADE DE LINGUAGEM entre todas as alternativas: tom, nível de nuance e
   quantificadores indistinguíveis entre a correta e os distratores. Termos
   absolutistas ("apenas", "somente", "exclusivamente", "nunca", "sempre",
   "todos", "eliminando a necessidade", "dispensando", "sem considerar",
   "independentemente") não podem se concentrar nos distratores. Um leitor
   atento NÃO pode eliminar alternativas apenas pelo estilo da escrita.
5. Apenas conteúdo técnico e boas práticas de engenharia de óleo e gás offshore
   — projeto, operação, manutenção, gestão, conformidade, logística e
   descomissionamento. Nada sobre professor, instituição, empresa, fabricante,
   autor ou formato do documento.
6. A questão deve ser respondível por um profissional do domínio SEM ter o
    documento em mãos: não escreva "segundo o texto", "conforme o documento",
    "no trecho apresentado". O documento é a fonte do conhecimento, não o
    objeto da pergunta. Não mencione o documento COMO FONTE no enunciado nem nas alternativas.
7. Nenhum distrator se justifica minimizando o próprio ponto fraco DENTRO do
   texto da alternativa — frases como "assumindo que...", "pressupondo
   que...", "considerando que... tende a ser secundário/pequeno/irrelevante".
   Esse padrão entrega a resposta a qualquer leitor treinado em prova de
   múltipla escolha, mesmo sem nenhum conhecimento do domínio: o distrator
   precisa errar pelo CONTEÚDO técnico, afirmado com a mesma confiança da
   alternativa correta — nunca por uma ressalva que ele mesmo admite.

DIFICULDADE (sua própria avaliação, para o campo `dificuldade_gerador`) —
mesma régua usada depois por um avaliador independente (o judge), pensada
para um profissional experiente do domínio:
- "facil": exige compreensão do conceito, sem encadeamento;
- "media": exige aplicar o conceito a um cenário, ou conectar dois conceitos;
- "dificil": exige análise crítica, avaliação de trade-off ou síntese.
Isso NÃO é a questão sendo julgada duas vezes por você: é uma segunda opinião,
independente da nota e da avaliação final, que serve para comparar as duas
avaliações depois.

DISTRIBUIÇÃO ALVO no questionário:
- ~30% questões mais fáceis (compreensão profunda, NÃO memorização)
- ~40% questões médias (aplicação, conexão entre conceitos)
- ~30% questões difíceis (análise crítica, avaliação, síntese)

Confie no seu julgamento sobre como atingir esses critérios não há um processo
rígido a seguir.

Essa distribuição vale para o LOTE de questões que você está gerando agora
(não para a faceta inteira nem para o banco todo — outras rodadas cobrem
outros lotes). Com poucas questões por lote, nem sempre dá pra bater as
proporções exatas: priorize a régua de dificuldade acima sobre a
porcentagem exata.
""".strip()


def _formatar_exemplo(q: dict, i: int) -> str:
    # Só enunciado, alternativas e gabarito: o exemplo mostra exatamente o que
    # se espera de volta. Justificativa aqui reintroduziria, pela porta dos
    # fundos, um campo que o gerador não deve mais produzir.
    alts = "\n".join(
        f"  {chr(65 + j)}) {a}" for j, a in enumerate(q["alternatives"])
    )
    gab = chr(65 + int(q["correct_answer_index"]))
    return f"[exemplo {i}]\n{q['stem']}\n{alts}\n  Gabarito: {gab}"


def prompt_geracao(subtopico: str, topico: str, faceta_foco: str,
                   documento: str, exemplos: Sequence[dict],
                   n_questoes: int, n_alternativas: int,
                   marcador_rodada: str,
                   exemplo_externo: dict | None = None) -> tuple[str, str]:
    bloco_ex = ""
    if exemplos:
        corpo = "\n\n".join(_formatar_exemplo(q, i + 1) for i, q in enumerate(exemplos))
        bloco_ex = f"""
QUESTÕES DE REFERÊNCIA (avaliadas como boas por especialistas do domínio).
Use-as como calibração de estilo, profundidade e construção de distratores —
NÃO como fonte de conteúdo e NÃO para copiar o assunto:

{corpo}
"""

    bloco_externo = ""
    if exemplo_externo:
        bloco_externo = f"""
EXEMPLO DE OUTRO DOMÍNIO (ciências gerais, não é óleo e gás — IGNORE o
assunto). Sirva-se dele só pela LÓGICA de construção dos distratores: cada
alternativa errada é uma posição plausível que erra por um motivo específico
e identificável — nunca uma opção qualquer, e nunca uma opção tecnicamente
verdadeira que simplesmente não responde à pergunta feita:

{_formatar_exemplo(exemplo_externo, "externo")}
"""

    user = f"""
{marcador_rodada}

Tópico: {topico}
Subtópico: {subtopico}

Instrução do especialista para este recorte:
{faceta_foco}

DOCUMENTO DE REFERÊNCIA (única fonte factual permitida):
```
{documento.strip()}
```
{bloco_ex}{bloco_externo}
Gere {n_questoes} questões de múltipla escolha com {n_alternativas} alternativas
cada, ancoradas no documento de referência e atendendo à instrução do
especialista e aos critérios de qualidade.

Retorne apenas o JSON:
```json
{{
  "questoes": [
    {{
      "stem": "O texto da pergunta",
      "alternatives": ["Opção A", "Opção B", "Opção C", "Opção D"],
      "correct_answer_index": 2,
      "dificuldade_gerador": "media"
    }}
  ]
}}
```
""".strip()
    return SYS_GERADOR, user


# ===========================================================================
# 4. JUDGE  (gpt-5, esforço baixo, em lote)
# ===========================================================================
# Os quatro critérios abaixo são os mesmos que os especialistas usaram para
# justificar a escolha no formulário comparativo da fase 2. A nota final [0,1]
# é uma média ponderada declarada no prompt, para que o judge não invente a
# própria escala.

CRITERIOS_JUDGE = """
1. CORREÇÃO TÉCNICA (peso 0,40)
   A alternativa marcada como correta está tecnicamente certa e é a ÚNICA
   defensável? Os fatos, mecanismos e relações de causa e efeito do enunciado
   estão corretos segundo a boa prática de engenharia de óleo e gás offshore?
   Há mais de uma alternativa defensável, ou nenhuma? Esta é a porta de entrada:
   se a questão falha aqui de forma insanável, ela é descartada.

2. CLAREZA DO ENUNCIADO (peso 0,20)
   O enunciado é inequívoco, autocontido e formula uma pergunta única? O leitor
   sabe exatamente o que está sendo pedido antes de ler as alternativas? Há
   ambiguidade, dupla negação, cenário confuso ou informação faltante?

3. QUALIDADE DAS ALTERNATIVAS DE RESPOSTA (peso 0,25)
   Os distratores são posições tecnicamente plausíveis, cada um capturando um
   erro de raciocínio específico? Ou são obviamente errados, redundantes entre
   si, absolutistas, ou desconectados do enunciado? A correta se destaca pela
   forma (tamanho, tom, repetição de termos do enunciado) em vez do conteúdo?

4. RELEVÂNCIA PARA A OPERAÇÃO DE FPSOs (peso 0,15)
   O cenário representa uma situação real e significativa de projeto, operação,
   manutenção, gestão, conformidade, logística ou descomissionamento de uma
   unidade offshore? Ou é genérico, artificial, ou de outro domínio?
""".strip()

SYS_JUDGE = f"""
Você é um especialista sênior em operação de unidades offshore de produção de
petróleo (FPSO) avaliando questões de múltipla escolha para um banco de
avaliação profissional. Você é rigoroso: uma questão medíocre aprovada
contamina o banco inteiro.

CRITÉRIOS (cada um pontuado de 0,0 a 1,0):
{CRITERIOS_JUDGE}

NOTA DE QUALIDADE = 0,40·correcao + 0,20·clareza + 0,25·alternativas + 0,15·relevancia
Calcule-a você mesmo com esses pesos e devolva arredondada em 2 casas.

DESCARTE (`correta_ok: false`) quando, e somente quando:
- a alternativa marcada como correta estiver tecnicamente errada; ou
- houver outra alternativa igualmente defensável como correta; ou
- o enunciado contiver erro técnico que invalide a questão.
Redação ruim, distrator fraco ou cenário pouco relevante NÃO são motivo de
descarte — são nota baixa.

DIFICULDADE para um profissional experiente do domínio:
- "facil": exige compreensão do conceito, sem encadeamento;
- "media": exige aplicar o conceito a um cenário, ou conectar dois conceitos;
- "dificil": exige análise crítica, avaliação de trade-off ou síntese.

Seja econômico no raciocínio: julgue direto, sem deliberação extensa.
""".strip()


def prompt_judge(questoes: Sequence[dict], subtopico: str) -> tuple[str, str]:
    itens = []
    for q in questoes:
        alts = "\n".join(
            f"  {chr(65 + j)}) {a}" for j, a in enumerate(q["alternatives"])
        )
        gab = chr(65 + int(q["correct_answer_index"]))
        itens.append(
            f"[id {q['id']}]\n{q['stem']}\n{alts}\n"
            f"  Gabarito declarado: {gab}"
        )
    corpo = "\n\n".join(itens)
    user = f"""
Subtópico: {subtopico}

Avalie as {len(questoes)} questões abaixo.

{corpo}

Retorne apenas o JSON, um objeto por questão, na mesma ordem:
```json
{{
  "avaliacoes": [
    {{
      "id": "id da questão",
      "correta_ok": true,
      "correcao": 0.9,
      "clareza": 0.8,
      "alternativas": 0.7,
      "relevancia": 0.9,
      "nota": 0.83,
      "dificuldade": "media",
      "comentario": "uma frase apontando o principal problema, ou o principal acerto"
    }}
  ]
}}
```
""".strip()
    return SYS_JUDGE, user


# ===========================================================================
# 5. REFINADOR  (gpt-5)
# ===========================================================================
# Recebe a questão com o diagnóstico quantitativo do scorer de vícios. O prompt
# nomeia o vício medido e o valor, para o modelo não sair reescrevendo o que
# estava bom.

SYS_REFINADOR = """
Você reescreve questões de múltipla escolha do domínio de óleo e gás offshore
(FPSO) para eliminar vícios de construção detectados automaticamente, SEM
alterar o conteúdo técnico avaliado.

Invariantes (quebrar qualquer um destes é falha grave):
- O conhecimento técnico cobrado permanece o mesmo. A questão continua sobre o
  mesmo ponto, com a mesma resposta tecnicamente correta.
- O número de alternativas permanece o mesmo.
- A alternativa correta continua sendo a única defensável.
- Não se preocupe com a POSIÇÃO da correta: mantenha a que veio, ou mude e
  atualize `correct_answer_index` — a posição final é sorteada depois.

Como corrigir cada vício:
- `similaridade`: a correta repete termos do enunciado que os distratores não
  repetem, entregando o gabarito. Redistribua o vocabulário: parafraseie a
  correta com sinônimos técnicos e traga termos do enunciado para dentro dos
  distratores, sem torná-los verdadeiros.
- `comprimento`: a correta destoa em tamanho. Traga-a para a faixa dos
  distratores cortando qualificação redundante e explicação que a pergunta não
  pediu. NÃO infle distratores com enchimento vazio; se um distrator precisa de
  mais texto, ele ganha conteúdo técnico plausível e errado, não palavras a mais.
- `distratores`: há distrator sem relação semântica com o enunciado (fora do
  assunto, descartável de imediato) ou carregado de linguagem absolutista
  ("apenas", "somente", "exclusivamente", "nunca", "sempre", "único"). Reescreva
  esses distratores como posições técnicas plausíveis e matizadas, erradas pelo
  conteúdo, com o mesmo tom e o mesmo nível de hedging da alternativa correta.
- `racionalizacao`: o distrator se justifica DENTRO do próprio texto,
  minimizando o seu ponto fraco ("assumindo que...", "pressupondo que...",
  "...tende a ser secundário/pequeno/irrelevante"). Isso entrega a resposta a
  qualquer leitor treinado em prova de múltipla escolha, mesmo sem
  conhecimento do domínio. Reescreva-o como uma afirmação direta e confiante
  — do mesmo jeito que a alternativa correta é redigida — errando pelo
  CONTEÚDO técnico, nunca por uma ressalva que ele mesmo admite.

Não comente a tarefa. Devolva apenas o JSON pedido.
""".strip()


def prompt_refinamento(questao: dict, diagnostico: dict,
                       documento: str | None = None) -> tuple[str, str]:
    alts = "\n".join(
        f"  {chr(65 + j)}) {a}" for j, a in enumerate(questao["alternatives"])
    )
    gab = chr(65 + int(questao["correct_answer_index"]))
    diag_txt = "\n".join(
        f"  - {k}: medido {v['valor']:.2f} (tolerância {v['limite']:.2f}) — {v['detalhe']}"
        for k, v in diagnostico.items() if v["excedeu"]
    )
    bloco_doc = ""
    if documento:
        bloco_doc = f"""
Documento de referência (para manter a fidelidade técnica):
```
{documento.strip()[:6000]}
```
"""
    user = f"""
Questão a refinar:

{questao['stem']}
{alts}
  Gabarito: {gab}

Vícios detectados pelo scorer automático:
{diag_txt}
{bloco_doc}
Reescreva a questão eliminando exatamente esses vícios e preservando o
conteúdo técnico avaliado.

Retorne apenas o JSON:
```json
{{
  "stem": "enunciado reescrito",
  "alternatives": ["...", "...", "...", "..."],
  "correct_answer_index": 0,
  "mudancas": "uma frase sobre o que foi alterado e por quê"
}}
```
""".strip()
    return SYS_REFINADOR, user


__all__ = [
    "prompt_extrator", "prompt_consolidacao", "prompt_geracao",
    "prompt_judge", "prompt_refinamento", "CRITERIOS_JUDGE",
    "SYS_EXTRATOR", "SYS_CONSOLIDADOR", "SYS_GERADOR", "SYS_JUDGE",
    "SYS_REFINADOR",
]
