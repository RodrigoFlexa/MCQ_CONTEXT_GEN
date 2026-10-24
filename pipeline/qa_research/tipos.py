"""Tipos de questão (substituem os rótulos de dificuldade) e checagens aplicadas em código.

Decisão de 23/10/2026 (ver TIPOS_QUESTAO.md): os pilotos mostraram que fácil, média e difícil mediam
habilidades diferentes, não degraus de uma escala, e não previam o acerto dos modelos. Cada questão
passa a ter um de seis tipos, definidos pelo que a pergunta pede e pela forma da resposta, mais duas
marcas: `cenario` (situação operacional ou pergunta direta) e `composicao` (simples ou composta).
"""
from __future__ import annotations

import re

from pipeline.qa_research.dificuldade import _sem_acento, pergunta_final, problemas_forma

TIPOS = ("conceito", "mecanismo", "consequencia", "diagnostico", "decisao", "procedimento")
# Composição por janela: 1 de cada grupo + 1 livre (no máximo 2 do mesmo grupo).
GRUPOS = {"conceito": ("conceito",), "causal": ("mecanismo", "consequencia"),
          "aplicado": ("diagnostico", "decisao", "procedimento")}
GRUPO_DO_TIPO = {t: g for g, ts in GRUPOS.items() for t in ts}
# v16: decisão sai da janela (só nas compostas, onde a aprovação era o dobro).
GRUPOS_V16 = {"conceito": ("conceito",), "causal": ("mecanismo", "consequencia"),
              "aplicado": ("diagnostico", "procedimento")}
TETO_PERGUNTA = 90
TETO_CONCEITO = 35
_LISTA_ABERTA = re.compile(r"\b(que|quais) (aspectos|fatores|elementos|cuidados|itens|pontos|informacoes|"
                           r"condicoes|requisitos|caracteristicas|variaveis)\b|\balem d[aeo]s?\b")
# Perguntas sobre o que o texto disse ("é citado", "foi mencionado") dependem do documento.
_CITADO = re.compile(r"\b(e|foi|sao|foram|esta|estao|aparece|aparecem) (citad|mencionad|apontad|listad)"
                     r"|\b(citad|mencionad|apontad|listad)[oa]s? como\b")
# Caso específico: unidade, campo ou bacia com nome próprio (ex.: "FPSO Frade", "P-50", "Bacia de Campos").
_CASO = re.compile(r"\b(FPSO|FSO|[Pp]lataforma|[Nn]avio|[Uu]nidade|[Cc]ampo|[Bb]acia)\s+(?:de\s+|do\s+|da\s+)?"
                   r"[A-ZÁÉÍÓÚÂÊÔÃÕ][a-zà-ú]+|\bP-\d{2,3}\b|\bem (19|20)\d{2}\b")
# Resposta que não se compromete.
_VAGA = re.compile(r"\btendem? a (se )?(alterar|variar|mudar|modificar)\b|\bpotencialmente\b|\bpodem? (ou nao )?variar\b"
                   r"|\bdependem? d[aeo]s?\b")
# Referência à fonte: quem responde não leu os blocos nem o documento.
_FONTE = re.compile(r"\b(n[oa]s? (blocos?|texto|documento)( (acima|fornecid[oa]s?|apresentad[oa]s?))?"
                    r"|segundo [oa] (texto|documento|blocos?|fonte)|unic[oa] sob (essas|estas) condicoes)\b")
_SIGLA = re.compile(r"\b(sigla|acronimo|abreviatura|abreviacao)\b")
_QUE_TIPO = re.compile(r"\b(que|qual) (tipo|tipos|classe|categoria) de\b")
# Decisão por comparação de dois itens com atributos ("um ... ; o outro ...") tende a entregar a resposta.
_COMPARACAO = re.compile(r"\b(o outro|a outra|um deles|uma delas|o segundo|a segunda)\b")
_PRIORIDADE = re.compile(r"\b(qual|quais|que)\b[^?]{0,60}\b(prioridade|priorizad|primeiro|antes)\b")
# Letras latinas, dígitos, pontuação comum e símbolos técnicos; o resto (ex.: armênio) indica falha de geração.
_FORA_DO_SCRIPT = re.compile(r"[^\x00-\x7FÀ-ɏ‐-‧°-¿Α-ω⁰-₟"
                             r"←-⇿∀-⋿×÷′″]")


def caracteres_estranhos(texto: str) -> list[str]:
    return sorted(set(_FORA_DO_SCRIPT.findall(texto)))


def problemas_tipo(tipo: str, cenario, pergunta: str, resposta: str) -> list[str]:
    """Mensagens para o modelo corrigir; lista vazia quando a questão respeita o tipo e a forma."""
    if tipo not in TIPOS:
        return [f"tipo deve ser um de: {', '.join(TIPOS)}"]
    if not isinstance(cenario, bool):
        return ["cenario deve ser true ou false"]
    out = list(problemas_forma(pergunta, resposta))
    estranhos = caracteres_estranhos(pergunta + " " + resposta)
    if estranhos:
        out.append(f"há caracteres fora do português ({''.join(estranhos)}); reescreva o trecho")
    n = len(pergunta.split())
    if n > TETO_PERGUNTA:
        out.append(f"o enunciado tem mais de {TETO_PERGUNTA} palavras")
    final = _sem_acento(pergunta)
    caso = _CASO.search(pergunta)
    if caso:
        out.append(f"caso específico ('{caso.group(0)}'): quem responde não leu o documento; pergunte pelo princípio "
                   "técnico, válido em qualquer unidade")
    if _VAGA.search(_sem_acento(resposta)):
        out.append("resposta vaga ('tende a se alterar', 'potencialmente', 'depende'): comprometa-se com uma direção, "
                   "um mecanismo ou um elemento concreto")
    if _FONTE.search(final + " " + _sem_acento(resposta)):
        out.append("não mencione blocos, texto, documento ou fonte, nem diga que a resposta é única: quem responde "
                   "não leu o material; escreva a pergunta como se fosse sobre a prática")
    if _CITADO.search(final):
        out.append("não pergunte o que é citado, mencionado ou listado: pergunte pelo conhecimento técnico")
    if tipo == "conceito":
        if cenario or n > TETO_CONCEITO:
            out.append(f"conceito é pergunta direta, sem cenário, de até {TETO_CONCEITO} palavras")
        if _LISTA_ABERTA.search(final):
            out.append("conceito não pode pedir 'que aspectos/quais fatores' nem 'além de X': admite várias "
                       "respostas; pergunte por um termo, função, componente, parâmetro ou local único")
        if _SIGLA.search(final):
            out.append("conceito não pode pedir uma sigla: costuma sair da expansão das palavras do enunciado")
        if _QUE_TIPO.search(final):
            out.append("conceito não pode pedir 'que tipo de': costuma ser um item de uma lista com outros igualmente "
                       "corretos; inclua o qualificador que torna a resposta única ou escolha outro conhecimento")
    if tipo == "decisao" and _COMPARACAO.search(final) and _PRIORIDADE.search(pergunta_final(pergunta)):
        out.append("decisão não pode comparar dois itens pelos atributos e perguntar qual priorizar: a resposta "
                   "só repete os atributos; peça a ação técnica específica")
    if tipo in ("diagnostico", "decisao") and not cenario:
        out.append(f"{tipo} exige cenário: descreva a situação (sinais ou condições) e pergunte pela "
                   f"{'causa' if tipo == 'diagnostico' else 'ação ou critério'}")
    return out


MAXIMO_V14 = {"conceito": 2, "causal": 2, "aplicado": 2}
MAXIMO_V15 = {"conceito": 1, "causal": 2, "aplicado": 2}   # a vaga livre não pode ser outro conceito


def problemas_composicao(status: str, tipos: list[str], motivo: str, total: int = 4,
                         maximo: dict = MAXIMO_V14, grupos: dict = GRUPOS) -> list[str]:
    """Janela: `total` questões com ao menos uma de cada grupo e no máximo `maximo[grupo]` de cada."""
    grupo_do_tipo = {t: g for g, ts in grupos.items() for t in ts}
    por_grupo = {g: sum(grupo_do_tipo.get(t) == g for t in tipos) for g in grupos}
    out = []
    fora = sorted({t for t in tipos if t not in grupo_do_tipo})
    if fora:
        out.append(f"tipo(s) não gerado(s) nesta etapa: {', '.join(fora)}")
    if len(tipos) > total:
        out.append(f"entregue no máximo {total} questões")
    excesso = [g for g, n in por_grupo.items() if n > maximo[g]]
    if excesso:
        out.append("excesso de questões no grupo (" + ", ".join(
            f"{g}: {'/'.join(grupos[g])}, máximo {maximo[g]}" for g in excesso) + ")")
    completa = len(tipos) == total and all(por_grupo.values())
    if status == "ok" and not completa:
        out.append(f"status ok exige {total} questões com ao menos uma de cada grupo (" + "; ".join(
            "/".join(ts) for ts in grupos.values()) + "); caso contrário, use parcial")
    if status == "parcial" and (not tipos or completa):
        out.append("status parcial exige de 1 a 3 questões ou um grupo faltando")
    if status == "sem_questoes" and tipos:
        out.append("status sem_questoes exige lista vazia")
    if status != "ok" and not motivo.strip():
        out.append("explique em motivo o que o bloco foco não sustenta")
    return out
