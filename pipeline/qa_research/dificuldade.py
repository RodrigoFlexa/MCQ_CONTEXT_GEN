"""Rubrica de dificuldade v2: checagens de forma aplicadas em código (ver DIFICULDADE_V2.md).

O piloto inventário x EC (23/10/2026) mostrou que perguntas de sim ou não, escolhas entre duas opções
dadas no enunciado e respostas de prudência genérica são acertadas por um modelo pequeno sem
contexto, mesmo rotuladas como difíceis. Estas funções barram a forma; o conteúdo fica com o prompt
(campo `desenho`) e com o juiz (`atalho_generico`).
"""
from __future__ import annotations

import re
import unicodedata

TETO_RESPOSTA = 30
CAMPOS_DESENHO = ("passo_oculto", "resposta_atraente", "sinal_que_descarta")
_INTERROGATIVAS = re.compile(
    r"\b(qual|quais|como|onde|aonde|quando|quanto|quanta|quantos|quantas|quem|cujo|cuja|por que|porque)\b")
# "que" só é interrogativo no início da oração ou depois de preposição/artigo ("o que", "em que", "a que").
_QUE = re.compile(r"(^|[,;:]\s*|\b(o|em|de|do|da|para|com|a|por|sob|ate|ao|no|na)\s+)que\b")
_INICIO_SIM_NAO = re.compile(
    r"^\s*(sim|nao|e (uma )?(decisao|conclusao|leitura|proposta|acao) (in)?adequad|e (in)?adequad|"
    r"esta (in)?corret|(in)?correto|(in)?correta|procede|nao procede|basta|nao basta)\b")
_CONCLUSAO_SOBRE = re.compile(r"\b(conclusao|avaliacao|leitura) (tecnica )?(correta )?sobre (essa|esta|a) "
                              r"(decisao|proposta|conclusao|leitura|acao|interpretacao)\b")
_ESCOLHA = r"(qual|quais) (das|dos) (duas|dois|opcoes|alternativas)|(qual|que) (decisao|opcao|alternativa|escolha|caminho)"
_ESCOLHA_BINARIA = re.compile(r"\bentre\b[^?]{1,120}\b(e|ou)\b[^?]{0,120}\b(" + _ESCOLHA + r")\b"
                              r"|\b(" + _ESCOLHA + r")\b[^?]{0,60}\bentre\b[^?]{1,120}\b(e|ou)\b"
                              r"|\b(" + _ESCOLHA + r")\b[^?]{0,80}[:,][^?]{1,120}\bou\b")


def _sem_acento(texto: str) -> str:
    t = unicodedata.normalize("NFKD", texto.lower())
    return "".join(c for c in t if not unicodedata.combining(c))


def pergunta_final(pergunta: str) -> str:
    """A última oração interrogativa do enunciado (ou o enunciado inteiro, se não houver '?')."""
    t = _sem_acento(pergunta).strip()
    if "?" not in t:
        return t
    antes = t[: t.rindex("?")]
    partes = re.split(r"(?<=[.!?])\s+", antes)
    return partes[-1].strip() if partes else antes


def eh_aberta(pergunta: str) -> bool:
    final = pergunta_final(pergunta)
    return bool(_INTERROGATIVAS.search(final) or _QUE.search(final))


def problemas_forma(pergunta: str, resposta: str, teto_resposta: int = TETO_RESPOSTA) -> list[str]:
    """Mensagens para o modelo corrigir; lista vazia quando a forma está adequada."""
    out = []
    final = pergunta_final(pergunta)
    if not eh_aberta(pergunta):
        out.append("a pergunta é de sim ou não; reformule como pergunta aberta (qual, que, como, onde...) "
                   "cuja resposta seja um elemento técnico específico")
    elif _CONCLUSAO_SOBRE.search(final):
        out.append("perguntar a 'conclusão correta sobre a decisão' é sim ou não disfarçado; pergunte pelo "
                   "mecanismo, pela causa, pela variável ou pela ação específica")
    if _ESCOLHA_BINARIA.search(final):
        out.append("a pergunta oferece a escolha entre opções dadas no enunciado; peça a resposta sem listar "
                   "as alternativas")
    if _INICIO_SIM_NAO.search(_sem_acento(resposta)):
        out.append("a resposta começa por sim, não ou um juízo de adequação; comece pelo elemento decisivo")
    if len(resposta.split()) > teto_resposta:
        out.append(f"a resposta tem mais de {teto_resposta} palavras")
    return out


def problemas_desenho(desenho, dificuldade: str, resposta: str) -> list[str]:
    """`desenho` registra o que torna a difícil difícil; obrigatório só nas difíceis."""
    if not isinstance(desenho, dict) or set(desenho) != set(CAMPOS_DESENHO) \
            or not all(isinstance(desenho[c], str) for c in CAMPOS_DESENHO):
        return [f"desenho deve ser um objeto com os textos {', '.join(CAMPOS_DESENHO)}"]
    if not dificuldade.startswith("dificil"):
        return []
    out = [f"na difícil, preencha desenho.{c}" for c in CAMPOS_DESENHO if not desenho[c].strip()]
    if not out and _sem_acento(desenho["resposta_atraente"]).strip(" .") == _sem_acento(resposta).strip(" ."):
        out.append("a resposta atraente precisa ser diferente da resposta correta")
    return out
