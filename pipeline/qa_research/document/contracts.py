"""Validação curta e estrita; citações são IDs resolvidos pelo programa."""
import re
from .common import PLACEHOLDER, canonical
from pipeline.inventario.textutil import sha

FLAGS = ("suportado", "condicoes_preservadas", "escopo_preservado", "estatuto_preservado", "fundamentacao_completa")
TYPES = {"resultado_experimental", "explicacao_tecnica", "recomendacao", "opiniao", "norma", "indeterminado"}
NUMBER_UNIT = re.compile(r"(?<![\w])\d+(?:[.,]\d+)?\s*(?:ppb|ppm|mg\s*/\s*l|g\s*/\s*l|mm\s*/\s*ano|%|°\s*c|kgf\s*/\s*cm2)(?!\w)", re.I)
NUMBER = re.compile(r"(?<![\w.,])[+-]?\d+(?:[.,]\d+)*(?:[eE][+-]?\d+)?(?!\w|[.,]\d)")


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


def draft(data, citations, max_blocks, max_words):
    obj(data, {"titulo", "blocos", "lacunas"})
    text(data["titulo"], 300)
    if type(data["blocos"]) is not list or not 1 <= len(data["blocos"]) <= max_blocks:
        raise ValueError("Quantidade de blocos fora do limite")
    for block in data["blocos"]:
        obj(block, {"texto", "trechos"})
        text(block["texto"], 12000)
        if len(block["texto"].split()) > max_words:
            raise ValueError("Bloco excedeu limite de palavras; divida as relações")
        if PLACEHOLDER.search(block["texto"]):
            raise ValueError("O texto final não deve reproduzir valores apagados; explique a limitação em lacunas")
        refs(block["trechos"], citations)
    strings(data["lacunas"], 12)


def numeric_tokens(text):
    return {re.sub(r"\s+", "", m.group()).casefold().replace(",", ".") for m in NUMBER_UNIT.finditer(text)}


def audit(data, block, packet, allowed_citations):
    obj(data, {"bloco", *FLAGS, "parecer", "suporte", "contraevidencia", "lacunas"})
    if data["bloco"] != block["id"] or any(type(data[k]) is not bool for k in FLAGS):
        raise ValueError("Bloco ou flags de auditoria inválidos")
    text(data["parecer"], 2400)
    refs(data["suporte"], allowed_citations, minimum=int(all(data[k] for k in FLAGS)))
    refs(data["contraevidencia"], allowed_citations, minimum=0)
    strings(data["lacunas"], 8)
    if all(data[k] for k in FLAGS):
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
        minimum = int(row["estado"] == "resolvida")
        refs(row["blocos"], blocks, minimum=minimum)
        refs(row["trechos"], citations, minimum=minimum)
        if minimum and isinstance(blocks, dict):
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
