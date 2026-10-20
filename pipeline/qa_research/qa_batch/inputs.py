"""Lê somente o documento de conhecimento e o escopo; nunca datasets de QA."""
import re

from pipeline.inventario.textutil import read_json, sha
from ..document.common import absolute, canonical, file_hash, load_profile
from ..document.program import load_program
from . import contracts as C


def topic(config):
    program = load_program(config.data["program"])
    row = next((r for r in program["items"] if r["id"] == config.item), None)
    if row is None:
        raise ValueError("Item não pertence ao programa: " + config.item)
    profile = load_profile(absolute(row["profile"]))
    scope = re.sub(r"\bAs questões devem abordar\b", "As questões podem abordar",
                   profile["topic"]["escopo"], count=1, flags=re.I)
    return {"id": config.item, "area": row["area"], "tema": row["subtopico"],
            "titulo_documento": profile["topic"]["titulo"], "escopo_orientador": scope}


def document(config, selected):
    path = config.document
    if not path.is_file() or path.is_symlink():
        raise ValueError("Documento técnico ainda não disponível: " + str(path))
    data = read_json(path)
    C.obj(data, ("titulo", "capitulos"))
    C.text(data["titulo"])
    if data["titulo"] != selected["titulo_documento"]:
        raise ValueError("Documento não corresponde ao tópico selecionado")
    if not isinstance(data["capitulos"], list) or not data["capitulos"]:
        raise ValueError("Documento sem capítulos técnicos")
    lines, blocks = ["# " + data["titulo"], ""], 0
    for chapter in data["capitulos"]:
        C.obj(chapter, ("titulo", "grupo", "blocos"))
        C.text(chapter["titulo"])
        C.text(chapter["grupo"])
        if not isinstance(chapter["blocos"], list) or not chapter["blocos"]:
            raise ValueError("Capítulo sem blocos técnicos")
        lines.extend(["## " + chapter["grupo"], "", "### " + chapter["titulo"], ""])
        for block in chapter["blocos"]:
            C.obj(block, ("subtitulo", "texto"))
            C.text(block["subtitulo"])
            C.text(block["texto"])
            lines.extend(["#### " + block["subtitulo"], "", block["texto"], ""])
            blocks += 1
    # Snapshots coletados verificam os bytes; saídas diretas precisam estar finalizadas.
    manifest = read_json(path.parent / "manifest_resultados.json")
    if manifest:
        if manifest.get("schema") != "document-results-v2" or manifest.get("files", {}).get(path.name) != file_hash(path):
            raise ValueError("Documento diverge do manifesto de resultados")
        summary_hash = manifest["files"].get("resumo.json")
        if summary_hash and file_hash(path.parent / "resumo.json") != summary_hash:
            raise ValueError("Resumo documental diverge do manifesto")
    summary = read_json(path.parent / "resumo.json")
    if summary:
        # Cobertura parcial não invalida os blocos já auditados/publicados. Exige
        # consolidação finalizada e ausência de interrupção/etapa em andamento.
        finalized_partial = (summary.get("status") == "parcial_com_pendencias"
                             and summary.get("consolidacao_completa") is True
                             and summary.get("etapas_pendentes") == []
                             and summary.get("interrupcao") is None)
        if summary.get("status") != "concluido" and not finalized_partial:
            raise ValueError("Aguarde a conclusão do documento antes de gerar o lote QA")
    context = "\n".join(lines).replace("\r\n", "\n")
    return {"contexto_tecnico": context, "contexto_sha256": sha(context, 64),
            "blocos": blocks, "caracteres": len(context), "arquivo_sha256": file_hash(path),
            "manifesto_verificado": bool(manifest), "conclusao_verificada": bool(summary),
            "status_documento": summary.get("status") if summary else "nao_informado",
            "recortes_documentais_pendentes": summary.get("recortes_pendentes", []) if summary else [],
            "documento": str(path)}


def payload(selected, source):
    return {"tema": {"area": selected["area"], "tema": selected["tema"]},
            "contexto_tecnico": source["contexto_tecnico"]}


def digest(value):
    return sha(canonical(value), 64)
