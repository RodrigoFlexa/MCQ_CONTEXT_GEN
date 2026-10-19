"""Validação curta e estrita; citações são IDs resolvidos pelo programa."""
import re
from .common import PLACEHOLDER, canonical
from pipeline.inventario.textutil import sha

FLAGS = ("suportado", "condicoes_preservadas", "escopo_preservado", "estatuto_preservado", "fundamentacao_completa")
TYPES = {"resultado_experimental", "explicacao_tecnica", "recomendacao", "opiniao", "norma", "indeterminado"}
BASES = {"corpus", "conhecimento_tecnico", "mista"}
META_PROSE = re.compile(
    r"\b(?:o|os)\s+(?:pr[oó]prios?\s+)?(?:trechos?|excertos?|corpus)\b|"
    r"\b(?:a|as)\s+fontes?\s+(?:afirma|relata|descreve|apresenta|informa|indica|sustenta|menciona|fornece|cita)|"
    r"\b(?:o documento|o texto|o material)\s+(?:afirma|relata|descreve|apresenta|informa|indica|sustenta|menciona|fornece|cita)|"
    r"\bn(?:o|os)\s+ensaios?\s+(?:relatados?|descritos?)\b|\btamb[eé]m se afirma\b|"
    r"\bo que foi (?:mostrado|relatado)\b|\bneste recorte\b|\bn[aã]o h[aá] fonte\b|"
    r"\b(?:faltam|aus[eê]ncia de)\s+(?:dados|fontes|evid[eê]ncias)\b|"
    r"\b(?:bibliografia|refer[eê]ncias bibliogr[aá]ficas)\b|\bet\s+al\.", re.I)
REFERENCE = re.compile(r"https?://|\bdoi\s*:|\bE[0-9a-f]{16}(?::\d+:\d+)?\b|"
    r"\[\s*\d+(?:\s*[-,;]\s*\d+)*\s*\]|"
    r"\([A-ZÀ-ÖØ-Ý][A-Za-zÀ-ÿ'’ &-]{1,80}[,\s]+(?:19|20)\d{2}[a-z]?\)|<!--", re.I)
NUMBER_UNIT = re.compile(r"(?<![\w.,])[+-]?\d+(?:[.,]\d+)?\s*(?:ppbv?|ppmv?|mg\s*/\s*l|g\s*/\s*l|mm\s*/\s*ano|%|°\s*c|bar(?:g|a)?|psi(?:g|a)?|kpa|mpa|kgf\s*/\s*cm2)(?!\w)", re.I)
# Unidades coladas (50ppmv) também são valores. Dígitos internos de fórmulas
# como CO2/H2S continuam excluídos pelo limite à esquerda.
NUMBER = re.compile(r"(?<![\w.,])[+-]?\d+(?:[.,]\d+)*(?:[eE][+-]?\d+)?(?!\d|[.,]\d)")


def obj(value, keys):
    if type(value) is not dict or set(value) != set(keys):
        raise ValueError("Campos esperados: " + ", ".join(sorted(keys)))


def text(value, maximum=1800, empty=False):
    if type(value) is not str or (not empty and not value.strip()) or len(value) > maximum:
        raise ValueError("Texto ausente ou muito longo")


def strings(value, maximum=12):
    if type(value) is not list or len(value) > maximum or any(type(v) is not str for v in value) or len(set(value)) != len(value):
        raise ValueError("Lista de textos distintos esperada")
    for item in value:
        text(item)


def refs(value, available, minimum=1):
    strings(value, 40)
    if len(value) < minimum or not set(value) <= set(available):
        raise ValueError("Referência ausente, repetida ou desconhecida")


def research_core(data, sources):
    obj(data, {"avaliacoes", "concluir", "proximas_fontes", "pedidos_busca", "lacunas"})
    if type(data["concluir"]) is not bool or type(data["avaliacoes"]) is not list:
        raise ValueError("Decisão booleana e avaliações esperadas")
    seen = set()
    for row in data["avaliacoes"]:
        obj(row, {"id", "pertinente", "tipo", "achados"})
        if row["id"] not in sources or row["id"] in seen or type(row["pertinente"]) is not bool or row["tipo"] not in TYPES:
            raise ValueError("Avalie exatamente uma vez cada fonte disponível, com tipo permitido")
        seen.add(row["id"])
        # Achados/consultas são validados individualmente após salvar o núcleo.
    if seen != set(sources):
        raise ValueError("Falta avaliação de fonte")


def findings(data, packet, allowed_sources):
    accepted, rejected = [], []
    for assessment in data["avaliacoes"]:
        candidates = assessment.get("achados")
        if not isinstance(candidates, list):
            rejected.append({"fonte": assessment["id"], "erro": "achados não é lista"})
            continue
        for row in candidates[:6]:
            try:
                obj(row, {"proposicao", "trechos", "condicoes", "limites"})
                text(row["proposicao"], 1000)
                strings(row["condicoes"], 6)
                strings(row["limites"], 6)
                refs(row["trechos"], packet.citations)
                if not assessment["pertinente"] or any(packet.citations[c]["fonte"] != assessment["id"] for c in row["trechos"]):
                    raise ValueError("Achado sem suporte na fonte que o avaliou")
                if assessment["id"] not in allowed_sources:
                    raise ValueError("Fonte fora do lote")
                accepted.append({**row, "fonte": assessment["id"], "tipo": assessment["tipo"]})
            except (ValueError, KeyError, TypeError) as exc:
                rejected.append({"fonte": assessment["id"], "erro": str(exc), "item": row})
    return accepted, rejected


def prose(block):
    """Barreira editorial complementar à revisão semântica; nunca remove frases."""
    text(block.get("subtitulo"), 160)
    if re.search(r"\b(?:lacunas|pend[eê]ncias|auditoria|refer[eê]ncias|bibliografia)\b", block["subtitulo"], re.I):
        raise ValueError("O subtítulo deve organizar conhecimento técnico; pendências e referências ficam nos auxiliares")
    body = block["subtitulo"] + "\n" + block["texto"]
    match = META_PROSE.search(body) or REFERENCE.search(body)
    if match:
        raise ValueError("Escreva conhecimento técnico autônomo, sem referência/metadiscurso: " + match.group())
    if re.search(r"\bAE[12]\b", body):
        raise ValueError("Código de produto anônimo não define conhecimento independente")


def draft(data, citations, max_blocks, max_words, synthesis=False):
    obj(data, {"titulo", "blocos", "lacunas"})
    text(data["titulo"], 300)
    if type(data["blocos"]) is not list or not 1 <= len(data["blocos"]) <= max_blocks:
        raise ValueError("Quantidade de blocos fora do limite")
    for block in data["blocos"]:
        obj(block, {"texto", "trechos", "subtitulo", "base", "complementos"} if synthesis else {"texto", "trechos"})
        text(block["texto"], 12000)
        if len(block["texto"].split()) > max_words:
            raise ValueError("Bloco excedeu limite de palavras; divida as relações")
        if PLACEHOLDER.search(block["texto"]):
            raise ValueError("O texto final não deve reproduzir valores apagados; explique a limitação em lacunas")
        if synthesis:
            prose(block)
            if block["base"] not in BASES:
                raise ValueError("Origem do conhecimento desconhecida")
            strings(block["complementos"], 6)
            if (block["base"] == "corpus") != (len(block["complementos"]) == 0):
                raise ValueError("Identifique as afirmações complementares; corpus puro não tem complementos")
            if block["base"] == "conhecimento_tecnico" and block["trechos"]:
                raise ValueError("Conhecimento complementar puro não deve alegar suporte do corpus")
        refs(block["trechos"], citations, minimum=int(not synthesis or block["base"] != "conhecimento_tecnico"))
    strings(data["lacunas"], 12)


def numeric_tokens(text):
    return {re.sub(r"\s+", "", m.group()).casefold().replace(",", ".") for m in NUMBER_UNIT.finditer(text)}


def audit(data, block, packet, allowed_citations):
    synthesis = "base" in block
    keys = {"bloco", *FLAGS, "parecer", "suporte", "contraevidencia", "lacunas"}
    obj(data, keys | ({"validacao_complementar"} if synthesis else set()))
    if data["bloco"] != block["id"] or any(type(data[k]) is not bool for k in FLAGS):
        raise ValueError("Bloco ou flags de auditoria inválidos")
    text(data["parecer"], 2400)
    accepted = all(data[k] for k in FLAGS)
    refs(data["suporte"], allowed_citations, minimum=int(accepted and block.get("base") != "conhecimento_tecnico"))
    refs(data["contraevidencia"], allowed_citations, minimum=0)
    strings(data["lacunas"], 8)
    if synthesis:
        if block["base"] not in BASES:
            raise ValueError("Origem do bloco desconhecida")
        if block["base"] == "conhecimento_tecnico" and data["suporte"]:
            raise ValueError("Complemento puro não pode ser atribuído ao corpus")
        validations = data["validacao_complementar"]
        if type(validations) is not list:
            raise ValueError("Lista de validações complementares esperada")
        checked = set()
        for row in validations:
            obj(row, {"indice", "justificativa"})
            index = row["indice"]
            if type(index) is not int or not 1 <= index <= len(block["complementos"]) or index in checked:
                raise ValueError("Índice complementar repetido ou desconhecido")
            text(row["justificativa"], 1800)
            if len(row["justificativa"].split()) < 4:
                raise ValueError("Justifique tecnicamente a validação complementar")
            checked.add(index)
        if accepted and checked != set(range(1, len(block["complementos"]) + 1)):
            raise ValueError("Valide cada afirmação complementar antes de aprovar")
    if accepted:
        if synthesis:
            prose(block)
        quoted = " ".join(packet.quote(cid) for cid in data["suporte"])
        if not numeric_tokens(block["texto"]) <= numeric_tokens(quoted):
            raise ValueError("Valor/unidade do bloco não aparece no suporte auditado")
        values = lambda s: {m.group().replace(",", ".") for m in NUMBER.finditer(s)}
        if not values(block["texto"]) <= values(quoted):
            raise ValueError("Número do bloco não aparece no suporte auditado; cálculos novos não são autorizados")


def seal(block, review, packet):
    return sha(canonical({"block": block, "review": review,
                         "sources": {packet.citations[c]["fonte"]: packet.sources[packet.citations[c]["fonte"]]["texto_sha256"]
                                     for c in review["suporte"]}}), 64)


def approved(state, packet):
    result = []
    for block in state.get("active_blocks", []):
        review = state.get("reviews", {}).get(block["id"])
        if not review or not all(review.get(k) is True for k in FLAGS):
            continue
        try:
            core = {k: v for k, v in review.items() if k not in {"seal", "allowed_citations"}}
            audit(core, block, packet, review["allowed_citations"])
            if review.get("seal") != seal(block, core, packet):
                continue
            result.append({**block, "trechos": core["suporte"], "auditoria": core})
        except (ValueError, KeyError, TypeError):
            continue
    return result


def gaps(data, entries, blocks, citations):
    obj(data, {"resolucoes"})
    if type(data["resolucoes"]) is not list:
        raise ValueError("Resoluções esperadas")
    seen = set()
    for row in data["resolucoes"]:
        obj(row, {"id", "estado", "parecer", "blocos", "trechos"})
        if row["id"] not in entries or row["id"] in seen or row["estado"] not in {"aberta", "parcial", "resolvida"}:
            raise ValueError("Lacuna repetida/desconhecida ou estado inválido")
        seen.add(row["id"])
        text(row["parecer"], 1400)
        resolved = row["estado"] == "resolvida"
        refs(row["blocos"], blocks, minimum=int(resolved))
        complementary = isinstance(blocks, dict) and any(blocks[b].get("base") in {"mista", "conhecimento_tecnico"} for b in row["blocos"])
        refs(row["trechos"], citations, minimum=int(resolved and not complementary))
        if resolved and isinstance(blocks, dict):
            related = {c for bid in row["blocos"] for c in blocks[bid]["trechos"]}
            if not set(row["trechos"]) <= related:
                raise ValueError("Trecho de resolução não pertence ao suporte dos blocos indicados")
    if seen != set(entries):
        raise ValueError("Reavalie exatamente uma vez cada lacuna histórica")


def duplicates(data, pairs):
    obj(data, {"comparacoes"})
    if type(data["comparacoes"]) is not list:
        raise ValueError("Comparações esperadas")
    expected = {tuple(p) for p in pairs}
    seen = set()
    for row in data["comparacoes"]:
        obj(row, {"a", "b", "equivalentes", "mesmas_condicoes", "parecer"})
        pair = (row["a"], row["b"])
        if pair not in expected or pair in seen or any(type(row[k]) is not bool for k in ("equivalentes", "mesmas_condicoes")):
            raise ValueError("Comparação inválida")
        seen.add(pair)
        text(row["parecer"])
    if seen != expected:
        raise ValueError("Compare todos os pares solicitados")
