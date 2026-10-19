"""Contratos fechados de saída; integridade textual não prova suporte semântico.

Os validadores retornam o próprio objeto recebido e nunca o modificam. IDs de
blocos/unidades pertencem ao orquestrador, não às saídas de redator e extrator.
"""
import re
import unicodedata


DOCUMENT_FLAGS = ("suportado", "condicoes_preservadas", "escopo_preservado",
                  "estatuto_preservado", "fundamentacao_completa")
ATOM_FLAGS = ("fidelidade", "atomica", "contexto_suficiente",
              "resposta_determinada", "objetividade", "resposta_suportada")
QA_FLAGS = ("factual", "fechada", "univoca_no_contexto", "curta",
            "autossuficiente", "escopo_preservado", "alinhada_ao_alvo",
            "resolucao_equivalente", "variantes_equivalentes")

_FACET_KEYS = {"titulo", "servico", "fenomeno_produto", "decisao",
               "ancoras_escopo", "consultas", "justificativa"}
_SOURCE_TYPES = {"resultado_experimental", "explicacao_tecnica", "recomendacao",
                 "opiniao", "norma", "indeterminado"}
_UNIT_TYPES = {"principio", "mecanismo", "resultado_experimental", "procedimento",
               "requisito_normativo", "recomendacao", "opiniao", "hipotese"}
_TARGET_TYPES = {"entidade", "propriedade", "valor", "relacao", "condicao",
                 "procedimento"}
_PLACEHOLDER = re.compile(
    r"(?i)(?:<\s*(?:number|numero|número|num|value|valor)\s*>|"
    r"\[\s*(?:number|numero|número|value|valor|redacted|ileg[ií]vel)\s*\]|"
    r"\{\s*(?:number|numero|número|value|valor)\s*\})")
_NUMERIC_PLACEHOLDER = re.compile(r"(?i)(?:\b(?:x{3,}|tbd|redacted)\b|_{2,}|\?{2,})")


def _norm(text):
    return re.sub(r"\s+", " ", unicodedata.normalize("NFC", text)).strip()


def _equivalent_text(text):
    return _norm(text).casefold()


def _keys(value, keys, where):
    if type(value) is not dict or set(value) != set(keys):
        actual = sorted(map(str, value)) if type(value) is dict else type(value).__name__
        raise ValueError(f"{where}: chaves esperadas {sorted(keys)}; recebido {actual}")


def _text(value, where, empty=False):
    if type(value) is not str or (not empty and not value.strip()):
        raise ValueError(f"{where}: texto {'(pode ser vazio)' if empty else 'não vazio'} esperado")
    return value


def _list(value, where, minimum=0, maximum=None):
    if type(value) is not list or len(value) < minimum or (maximum is not None and len(value) > maximum):
        raise ValueError(f"{where}: lista com tamanho entre {minimum} e {maximum} esperada")
    return value


def _strings(value, where, minimum=0, maximum=None, unique=False):
    _list(value, where, minimum, maximum)
    for index, item in enumerate(value):
        _text(item, f"{where}[{index}]")
    if unique and len(set(value)) != len(value):
        raise ValueError(f"{where}: itens duplicados")
    return value


def _limit(value, where):
    if type(value) is not int or value < 1:
        raise ValueError(f"{where}: inteiro positivo esperado")


def _choice(value, choices, where):
    if type(value) is not str or value not in choices:
        raise ValueError(f"{where}: deve ser um de {sorted(choices)}")


def _flags(row, flags, where):
    for flag in flags:
        if type(row[flag]) is not bool:
            raise ValueError(f"{where}.{flag}: tipo bool esperado, sem coerção")


def _by_id(rows, where):
    _list(rows, where)
    result = {}
    for row in rows:
        if type(row) is not dict:
            raise ValueError(f"{where}: objeto esperado")
        identity = _text(row.get("id"), f"{where}.id")
        if identity in result:
            raise ValueError(f"{where}: ID repetido {identity!r}")
        result[identity] = row
    return result


def _evidence_map(evidences):
    result = _by_id(evidences, "evidencias")
    for identity, row in result.items():
        _text(row.get("texto"), f"evidencias[{identity}].texto")
    return result


def _references(ids, available, where, minimum=1):
    _strings(ids, where, minimum=minimum, unique=True)
    if not set(ids) <= set(available):
        raise ValueError(f"{where}: IDs desconhecidos {sorted(set(ids) - set(available))}")


def _exact_rows(rows, available, where):
    actual = _by_id(rows, where)
    if set(actual) != set(available):
        raise ValueError(f"{where}: deve avaliar exatamente uma vez cada ID disponível")


def validate_support(rows, evidences, required=True):
    """Valida IDs e citações contíguas; preserva pontuação e caixa do original."""
    if type(required) is not bool:
        raise ValueError("required: booleano esperado")
    available = _evidence_map(evidences)
    _list(rows, "suporte", minimum=1 if required else 0)
    seen = set()
    for row in rows:
        _keys(row, {"evidencia_id", "citacao"}, "suporte[]")
        identity = _text(row["evidencia_id"], "suporte.evidencia_id")
        quote = _text(row["citacao"], "suporte.citacao")
        if identity not in available:
            raise ValueError(f"suporte: ID desconhecido {identity!r}")
        normalized = _norm(quote)
        if normalized not in _norm(available[identity]["texto"]):
            raise ValueError(f"suporte: citação não é trecho contíguo original de {identity!r}")
        key = (identity, normalized)
        if key in seen:
            raise ValueError("suporte: mesma citação repetida na mesma evidência")
        seen.add(key)
    return rows


def _facet(row, topic, discovered=False, evidences=None):
    _keys(row, _FACET_KEYS | ({"suporte"} if discovered else set()), "recorte")
    for key in ("titulo", "servico", "fenomeno_produto", "decisao", "justificativa"):
        _text(row[key], f"recorte.{key}")
    scope = _text(topic.get("escopo") if type(topic) is dict else None, "topic.escopo")
    _strings(row["ancoras_escopo"], "recorte.ancoras_escopo", minimum=1, unique=True)
    for anchor in row["ancoras_escopo"]:
        if _norm(anchor) not in _norm(scope):
            raise ValueError("recorte.ancoras_escopo: excerto não é contíguo no escopo")
    _strings(row["consultas"], "recorte.consultas", minimum=1, unique=True)
    if discovered:
        validate_support(row["suporte"], evidences)


def plan(data, topic, max_facets):
    _limit(max_facets, "max_facets")
    _keys(data, {"eixos", "recortes", "lacunas_planejamento"}, "plan")
    _keys(data["eixos"], {"servicos", "fenomenos_produtos", "decisoes"}, "eixos")
    for key, values in data["eixos"].items():
        _strings(values, f"eixos.{key}", minimum=1, unique=True)
    _list(data["recortes"], "recortes", minimum=1, maximum=max_facets)
    titles = set()
    for row in data["recortes"]:
        _facet(row, topic)
        title = _equivalent_text(row["titulo"])
        if title in titles:
            raise ValueError("recortes: títulos duplicados")
        titles.add(title)
    _strings(data["lacunas_planejamento"], "lacunas_planejamento")
    return data


def research(data, evidences, topic, max_queries):
    _limit(max_queries, "max_queries")
    _keys(data, {"acao", "orientacao", "consultas", "avaliacoes_fontes", "lacunas", "descobertas"}, "research")
    _choice(data["acao"], {"buscar", "redigir", "insuficiente"}, "acao")
    _text(data["orientacao"], "orientacao")
    _strings(data["consultas"], "consultas", minimum=int(data["acao"] == "buscar"), maximum=max_queries, unique=True)
    available = _evidence_map(evidences)
    _list(data["avaliacoes_fontes"], "avaliacoes_fontes")
    seen = set()
    for row in data["avaliacoes_fontes"]:
        _keys(row, {"evidencia_id", "pertinente", "tipo", "contexto", "limites"}, "avaliacoes_fontes[]")
        identity = _text(row["evidencia_id"], "avaliacoes_fontes.evidencia_id")
        if identity not in available or identity in seen:
            raise ValueError("avaliacoes_fontes: ID desconhecido ou repetido")
        seen.add(identity)
        _flags(row, ("pertinente",), "avaliacoes_fontes")
        _choice(row["tipo"], _SOURCE_TYPES, "avaliacoes_fontes.tipo")
        _text(row["contexto"], "avaliacoes_fontes.contexto")
        _strings(row["limites"], "avaliacoes_fontes.limites")
    if seen != set(available):
        raise ValueError("avaliacoes_fontes: deve avaliar exatamente uma vez cada evidência")
    if data["acao"] == "redigir" and not any(row["pertinente"] for row in data["avaliacoes_fontes"]):
        raise ValueError("redigir exige ao menos uma evidência pertinente")
    _strings(data["lacunas"], "lacunas")
    _list(data["descobertas"], "descobertas", maximum=3)
    for row in data["descobertas"]:
        _facet(row, topic, discovered=True, evidences=evidences)
    return data


def document(data, evidences):
    _keys(data, {"titulo", "blocos", "lacunas"}, "document")
    _text(data["titulo"], "titulo")
    _list(data["blocos"], "blocos", maximum=12)
    available = _evidence_map(evidences)
    for row in data["blocos"]:
        _keys(row, {"texto", "fontes"}, "blocos[]")
        _text(row["texto"], "blocos.texto")
        _references(row["fontes"], available, "blocos.fontes")
    _strings(data["lacunas"], "lacunas")
    return data


def audit_document(data, blocks, evidences):
    _keys(data, {"avaliacoes", "lacunas", "consultas"}, "audit_document")
    available = _by_id(blocks, "blocos")
    sources = _evidence_map(evidences)
    for block in blocks:
        _references(block.get("fontes"), sources, "blocos.fontes")
    _exact_rows(data["avaliacoes"], available, "avaliacoes")
    for row in data["avaliacoes"]:
        _keys(row, {"id", "parecer", "suporte", *DOCUMENT_FLAGS}, "avaliacoes[]")
        _flags(row, DOCUMENT_FLAGS, "avaliacoes")
        _text(row["parecer"], "avaliacoes.parecer")
        validate_support(row["suporte"], evidences, required=all(row[key] for key in DOCUMENT_FLAGS))
        if any(s["evidencia_id"] not in available[row["id"]]["fontes"] for s in row["suporte"]):
            raise ValueError("avaliacoes.suporte: evidência não citada pelo bloco")
    _strings(data["lacunas"], "lacunas")
    _strings(data["consultas"], "consultas", unique=True)
    return data


def _short_answer(value, answer_words, where, empty=False, numeric=False):
    _text(value, where, empty=empty)
    if len(value.split()) > answer_words:
        raise ValueError(f"{where}: excede limite de {answer_words} palavras")
    if _PLACEHOLDER.search(value) or (numeric and _NUMERIC_PLACEHOLDER.search(value)):
        raise ValueError(f"{where}: alvo contém valor substituído ou ilegível")


def atoms(data, blocks, evidences, max_atoms, answer_words):
    _limit(max_atoms, "max_atoms")
    _limit(answer_words, "answer_words")
    _keys(data, {"unidades", "motivo"}, "atoms")
    _text(data["motivo"], "motivo", empty=True)
    _list(data["unidades"], "unidades", maximum=max_atoms)
    available = _by_id(blocks, "blocos")
    sources = _evidence_map(evidences)
    for block in blocks:
        _references(block.get("fontes"), sources, "blocos.fontes")
    for row in data["unidades"]:
        _keys(row, {"proposicao", "tipo", "contexto", "condicoes", "limites", "blocos",
                    "jurisdicao", "edicao", "suporte", "alvo"}, "unidades[]")
        _text(row["proposicao"], "unidades.proposicao")
        _choice(row["tipo"], _UNIT_TYPES, "unidades.tipo")
        _text(row["contexto"], "unidades.contexto")
        for key in ("jurisdicao", "edicao"):
            _text(row[key], f"unidades.{key}", empty=True)
        for key in ("condicoes", "limites"):
            _strings(row[key], f"unidades.{key}")
        _references(row["blocos"], available, "unidades.blocos")
        validate_support(row["suporte"], evidences)
        allowed_sources = {source for identity in row["blocos"] for source in available[identity]["fontes"]}
        if any(s["evidencia_id"] not in allowed_sources for s in row["suporte"]):
            raise ValueError("unidades.suporte: evidência não pertence aos blocos vinculados")
        target = row["alvo"]
        _keys(target, {"tipo", "resposta", "variantes", "qualificador"}, "alvo")
        _choice(target["tipo"], _TARGET_TYPES, "alvo.tipo")
        _short_answer(target["resposta"], answer_words, "alvo.resposta", numeric=target["tipo"] == "valor")
        _strings(target["variantes"], "alvo.variantes", unique=True)
        for variant in target["variantes"]:
            _short_answer(variant, answer_words, "alvo.variantes[]", numeric=target["tipo"] == "valor")
        _text(target["qualificador"], "alvo.qualificador", empty=True)
    return data


def audit_atoms(data, units):
    _keys(data, {"avaliacoes"}, "audit_atoms")
    available = _by_id(units, "unidades")
    _exact_rows(data["avaliacoes"], available, "avaliacoes")
    for row in data["avaliacoes"]:
        _keys(row, {"id", "parecer", *ATOM_FLAGS}, "avaliacoes[]")
        _flags(row, ATOM_FLAGS, "avaliacoes")
        _text(row["parecer"], "avaliacoes.parecer")
    return data


def question(data, unit, answer_words):
    _limit(answer_words, "answer_words")
    _keys(data, {"status", "pergunta", "resposta", "variantes", "motivo"}, "question")
    _choice(data["status"], {"ok", "insuficiente"}, "status")
    _text(data["motivo"], "motivo", empty=True)
    _text(data["pergunta"], "pergunta", empty=data["status"] == "insuficiente")
    _short_answer(data["resposta"], answer_words, "resposta", empty=data["status"] == "insuficiente")
    _strings(data["variantes"], "variantes", unique=True)
    for variant in data["variantes"]:
        _short_answer(variant, answer_words, "variantes[]")
    if data["status"] == "insuficiente":
        if data["pergunta"].strip() or data["resposta"].strip() or data["variantes"] or not data["motivo"].strip():
            raise ValueError("insuficiente: pergunta/resposta vazias, sem variantes e motivo obrigatório")
        return data
    text = data["pergunta"].strip()
    if text.count("?") != 1 or not text.endswith("?"):
        raise ValueError("pergunta: uma única interrogação final é necessária")
    options = re.findall(r"(?:^|\n)\s*[A-Ea-e][.)]\s+\S", text)
    if len(options) > 1:
        raise ValueError("pergunta: alternativas de múltipla escolha não são permitidas")
    if re.match(r"(?i)^\s*(?:discuta\b|disserte\b|explique\s+detalhadamente\b|elabore\s+(?:uma\s+)?reda[çc][ãa]o\b)", text):
        raise ValueError("pergunta: demanda aberta incompatível com QA curta")
    if type(unit) is not dict or type(unit.get("alvo")) is not dict:
        raise ValueError("unit.alvo: objeto esperado")
    target = unit["alvo"]
    _text(target.get("resposta"), "unit.alvo.resposta")
    _strings(target.get("variantes"), "unit.alvo.variantes")
    allowed = {_equivalent_text(v) for v in [target["resposta"], *target["variantes"]]}
    if _equivalent_text(data["resposta"]) not in allowed:
        raise ValueError("resposta: deve coincidir com alvo aprovado ou uma de suas variantes")
    return data


def blind_answer(data, evidences, answer_words):
    _limit(answer_words, "answer_words")
    _keys(data, {"status", "resposta", "outras_respostas", "condicoes_ausentes", "parecer", "suporte"}, "blind_answer")
    _choice(data["status"], {"respondida", "ambigua", "sem_suporte"}, "status")
    _short_answer(data["resposta"], answer_words, "resposta", empty=data["status"] != "respondida")
    for key in ("outras_respostas", "condicoes_ausentes"):
        _strings(data[key], key, unique=True)
    for other in data["outras_respostas"]:
        _short_answer(other, answer_words, "outras_respostas[]")
    _text(data["parecer"], "parecer")
    validate_support(data["suporte"], evidences, required=data["status"] == "respondida")
    if data["status"] == "sem_suporte" and data["resposta"].strip():
        raise ValueError("sem_suporte: não deve apresentar resposta afirmativa")
    return data


def audit_qa(data):
    _keys(data, {*QA_FLAGS, "outras_respostas", "parecer"}, "audit_qa")
    _flags(data, QA_FLAGS, "audit_qa")
    _strings(data["outras_respostas"], "outras_respostas", unique=True)
    _text(data["parecer"], "parecer")
    if all(data[key] for key in QA_FLAGS) and data["outras_respostas"]:
        raise ValueError("audit_qa: aprovação contraditória com outras respostas distintas")
    return data


def novelty(data, previous_ids):
    _keys(data, {"comparacoes"}, "novelty")
    _strings(previous_ids, "previous_ids", unique=True)
    _exact_rows(data["comparacoes"], previous_ids, "comparacoes")
    for row in data["comparacoes"]:
        _keys(row, {"id", "classe", "parecer"}, "comparacoes[]")
        _choice(row["classe"], {"redundante", "sobreposicao", "distinta"}, "comparacoes.classe")
        _text(row["parecer"], "comparacoes.parecer")
    return data
