"""Fail-closed publication checks for the complete local evidence chain.

These checks establish checkpoint integrity and repeat the structural contracts;
semantic judgments remain explicit model judgments, not proof of scientific truth.
No check mutates its input or calls a model.
"""
import copy
import json

from pipeline.inventario.textutil import sha
from . import contracts as C


_INVALID = (ValueError, KeyError, TypeError, AttributeError, IndexError)
_ATOM_FIELDS = {"proposicao", "tipo", "contexto", "condicoes", "limites", "blocos",
                "jurisdicao", "edicao", "suporte", "alvo"}


def _canonical(value):
    # JSON comparison distinguishes true/1, which Python equality does not.
    return json.dumps(value, ensure_ascii=False, sort_keys=True)


def _sources(rows):
    if type(rows) is not list:
        raise ValueError("Lista de fontes esperada")
    result = {}
    for row in rows:
        if type(row) is not dict:
            raise ValueError("Fonte inválida")
        text, chunk_id = row["texto"], row["chunk_id"]
        if type(text) is not str or not text.strip() or type(chunk_id) is not str or not chunk_id:
            raise ValueError("Fonte sem texto ou identificador")
        identity = "E" + sha(chunk_id + "\n" + text, 16)
        if row.get("id") != identity or row.get("texto_sha256") != sha(text, 64):
            raise ValueError("Identidade/hash da fonte não corresponde ao texto original")
        if identity in result:
            raise ValueError("Identificador de evidência repetido")
        if row.get("source_kind") not in (None, "saved_selection", "verified_manifest"):
            raise ValueError("Fonte não é passagem original autorizada")
        result[identity] = row
    return result


def _document_without_ids(document):
    if type(document) is not dict or set(document) != {"titulo", "blocos", "lacunas"}:
        raise ValueError("Capítulo fora do schema")
    if type(document["blocos"]) is not list:
        raise ValueError("Lista de blocos esperada")
    for block in document["blocos"]:
        if type(block) is not dict or set(block) != {"id", "texto", "fontes"}:
            raise ValueError("Bloco fora do schema")
    return {"titulo": document["titulo"], "lacunas": document["lacunas"],
            "blocos": [{"texto": block["texto"], "fontes": block["fontes"]}
                       for block in document["blocos"]]}


def _checked_chapter(state):
    if state["status"] not in ("auditado_modelo", "parcial"):
        return None
    identity = state["id"]
    if state["recorte"]["id"] != identity:
        return None
    sources = list(_sources(state["evidencias"]).values())
    versions, audits = state["versoes"], state["auditorias"]
    if type(versions) is not list or not versions or type(audits) is not list or not audits:
        return None
    version, audit = versions[-1], audits[-1]
    if type(audit["versao"]) is not int or audit["versao"] != len(versions):
        return None
    C.document(_document_without_ids(version), sources)
    expected_ids = [f"{identity}-B{i:03d}" for i in range(1, len(version["blocos"]) + 1)]
    if [block["id"] for block in version["blocos"]] != expected_ids:
        return None
    C.audit_document({k: v for k, v in audit.items() if k != "versao"}, version["blocos"], sources)
    approved = {row["id"] for row in audit["avaliacoes"]
                if all(row[flag] is True for flag in C.DOCUMENT_FLAGS)}
    published = state["capitulo"]
    C.document(_document_without_ids(published), sources)
    expected = [block for block in version["blocos"] if block["id"] in approved]
    if not expected or published["titulo"] != version["titulo"]:
        return None
    if _canonical(published["blocos"]) != _canonical(expected):
        return None
    if state["status"] == "auditado_modelo" and len(approved) != len(version["blocos"]):
        return None
    return copy.deepcopy(published)


def checked_chapter(state):
    """Return the chapter only when its actual latest version was audited."""
    try:
        return _checked_chapter(state)
    except _INVALID:
        return None


def _unit_eligible(unit):
    if unit.get("elegivel_qa") is not True:
        return False
    if not all(unit["auditoria"].get(flag) is True for flag in C.ATOM_FLAGS):
        return False
    if unit["tipo"] in ("opiniao", "hipotese"):
        return False
    if unit["tipo"] == "requisito_normativo" and not (unit["jurisdicao"].strip() and unit["edicao"].strip()):
        return False
    return True


def checked_units(pack, state, config):
    """Filter eligible atomic units against the published chapter and sources."""
    try:
        chapter = _checked_chapter(state)
        if not chapter or pack["recorte_id"] != state["id"]:
            return []
        rows = pack["unidades"]
        if type(rows) is not list or len(rows) > config.max_atoms_per_facet:
            return []
        sources = list(_sources(state["evidencias"]).values())
    except _INVALID:
        return []
    valid, seen = [], set()
    for unit in rows:
        try:
            if set(unit) != _ATOM_FIELDS | {"id", "recorte_id", "auditoria", "elegivel_qa"}:
                continue
            if unit["recorte_id"] != state["id"] or not _unit_eligible(unit):
                continue
            raw = {key: unit[key] for key in _ATOM_FIELDS}
            expected = state["id"] + "-U" + sha(json.dumps(raw, sort_keys=True, ensure_ascii=False), 14)
            if unit["id"] != expected or unit["id"] in seen:
                continue
            C.atoms({"unidades": [raw], "motivo": pack["motivo"]}, chapter["blocos"], sources,
                    config.max_atoms_per_facet, config.answer_words)
            C.audit_atoms({"avaliacoes": [unit["auditoria"]]}, [unit])
            valid.append(copy.deepcopy(unit))
            seen.add(unit["id"])
        except _INVALID:
            continue
    return valid


def checked_question(row, unit, state, config):
    """Accept only an intact QA linked to its valid unit and original evidence."""
    try:
        if row["status"] != "aprovada_modelo" or row["id"] != unit["id"]:
            return False
        if row["recorte_id"] != state["id"] or unit["recorte_id"] != state["id"]:
            return False
        if _canonical(row["unidade"]) != _canonical(unit):
            return False
        if not checked_units({"recorte_id": state["id"], "unidades": [unit], "motivo": ""}, state, config):
            return False
        C.question(row["candidata"], unit, config.answer_words)
        if row["candidata"]["status"] != "ok":
            return False
        for field in ("pergunta", "resposta", "variantes"):
            if _canonical(row[field]) != _canonical(row["candidata"][field]):
                return False
        originals = _sources(state["evidencias"])
        verification = _sources(row["evidencias_verificacao"])
        author_ids = {support["evidencia_id"] for support in unit["suporte"]}
        if not author_ids <= set(verification):
            return False
        if any(_canonical(verification[eid]) != _canonical(originals[eid]) for eid in author_ids):
            return False
        blind = row["resolucao_independente"]
        C.blind_answer(blind, list(verification.values()), config.answer_words)
        C.audit_qa(row["auditoria"])
        if not all(row["auditoria"][key] is True for key in C.QA_FLAGS):
            return False
        if (row["auditoria"]["outras_respostas"] or blind["status"] != "respondida"
                or blind["outras_respostas"] or blind["condicoes_ausentes"]):
            return False
        if "novidade" in row:
            novelty = row["novidade"]
            C.novelty(novelty, [item["id"] for item in novelty["comparacoes"]])
            if any(item["classe"] == "redundante" for item in novelty["comparacoes"]):
                return False
        return True
    except _INVALID:
        return False
