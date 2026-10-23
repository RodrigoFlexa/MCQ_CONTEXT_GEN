"""Tipos de questão (substituem os rótulos de dificuldade) e checagens aplicadas em código.

Decisão de 23/10/2026 (ver TIPOS_QUESTAO.md): os pilotos mostraram que fácil, média e difícil mediam
habilidades diferentes, não degraus de uma escala, e não previam o acerto dos modelos. Cada questão
passa a ter um de seis tipos, definidos pelo que a pergunta pede e pela forma da resposta, mais duas
marcas: `cenario` (situação operacional ou pergunta direta) e `composicao` (simples ou composta).
"""
from __future__ import annotations

import re

from pipeline.qa_research.dificuldade import _sem_acento, problemas_forma

TIPOS = ("conceito", "mecanismo", "consequencia", "diagnostico", "decisao", "procedimento")
# Composição por janela: 1 de cada grupo + 1 livre (no máximo 2 do mesmo grupo).
GRUPOS = {"conceito": ("conceito",), "causal": ("mecanismo", "consequencia"),
          "aplicado": ("diagnostico", "decisao", "procedimento")}
GRUPO_DO_TIPO = {t: g for g, ts in GRUPOS.items() for t in ts}
TETO_PERGUNTA = 90
TETO_CONCEITO = 35
_LISTA_ABERTA = re.compile(r"\b(que|quais) (aspectos|fatores|elementos|cuidados|itens|pontos|informacoes|"
                           r"condicoes|requisitos|caracteristicas|variaveis)\b|\balem d[aeo]s?\b")
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
    if tipo == "conceito":
        if cenario or n > TETO_CONCEITO:
            out.append(f"conceito é pergunta direta, sem cenário, de até {TETO_CONCEITO} palavras")
        if _LISTA_ABERTA.search(final):
            out.append("conceito não pode pedir 'que aspectos/quais fatores' nem 'além de X': admite várias "
                       "respostas; pergunte por um termo, função, componente, parâmetro ou local único")
    if tipo in ("diagnostico", "decisao") and not cenario:
        out.append(f"{tipo} exige cenário: descreva a situação (sinais ou condições) e pergunte pela "
                   f"{'causa' if tipo == 'diagnostico' else 'ação ou critério'}")
    return out


def problemas_composicao(status: str, tipos: list[str], motivo: str, total: int = 4) -> list[str]:
    """Janela: `total` questões com ao menos uma de cada grupo e no máximo duas do mesmo grupo."""
    por_grupo = {g: sum(GRUPO_DO_TIPO.get(t) == g for t in tipos) for g in GRUPOS}
    out = []
    if len(tipos) > total:
        out.append(f"entregue no máximo {total} questões")
    excesso = [g for g, n in por_grupo.items() if n > 2]
    if excesso:
        out.append("no máximo duas questões do mesmo grupo (" + ", ".join(
            f"{g}: {'/'.join(GRUPOS[g])}" for g in excesso) + ")")
    completa = len(tipos) == total and all(por_grupo.values())
    if status == "ok" and not completa:
        out.append(f"status ok exige {total} questões com ao menos um conceito, um mecanismo ou consequência "
                   "e um diagnóstico, decisão ou procedimento; caso contrário, use parcial")
    if status == "parcial" and (not tipos or completa):
        out.append("status parcial exige de 1 a 3 questões ou um grupo faltando")
    if status == "sem_questoes" and tipos:
        out.append("status sem_questoes exige lista vazia")
    if status != "ok" and not motivo.strip():
        out.append("explique em motivo o que o bloco foco não sustenta")
    return out
