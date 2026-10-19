"""Programa das dez áreas; perfis explícitos, revisáveis e separados do corpus."""
import copy
from pathlib import Path

from pipeline.inventario.textutil import atomic_json, read_json
from .common import ROOT, absolute, file_hash, load_profile

DEFAULT_PROGRAM = "pipeline/qa_research/configs/dez_areas_v1/programa.json"
DEFAULT_PACKETS = "pipeline/qa_research/pacotes/dez_areas_v1"
DEFAULT_OUTPUT = "pipeline/qa_research/saida_documento_dez_areas_v1"
DEFAULT_RESULTS = "pipeline/qa_research/relatorios/dez_areas_v1"


def write_changed(path, value):
    if read_json(path) != value:
        atomic_json(path, value)


def build_program(destination=DEFAULT_PROGRAM):
    from pipeline.fase_3.topicos import TOPICOS
    from .curation import facets_for, PLANS
    destination = absolute(destination)
    base_path = ROOT / "pipeline/qa_research/configs/documento_produtos_quimicos.json"
    base = load_profile(base_path)
    rows, curated = [], set()
    for ai, (area, phrases) in enumerate(TOPICOS.items(), 1):
        for si, (title, scope) in enumerate(phrases.items(), 1):
            key, identifier = f"{ai:02}.{si:02}", f"{ai:02}_{si:02}"
            profile = copy.deepcopy(base)
            if key == "02.02":
                if profile["topic"]["escopo"] != scope:
                    raise ValueError("A frase de Produtos químicos mudou; revise o perfil existente")
                existing = "pipeline/qa_research/pacotes/produtos_quimicos_v2"
            else:
                profile["topic"] = {"titulo": f"{ai}.{si}. {title if title != 'Geral' else area}",
                    "escopo": scope, "area": area,
                    "restricoes": "Cenários de FPSO/FSO e sistemas associados. Não confundir operação submarina com perfuração ou intervenção direta com sonda. Não inventar requisitos legais ou limites."}
                profile["facets"] = facets_for(key, title if title != "Geral" else area)
                profile["runtime"]["max_calls"] = max(200, 45 * len(profile["facets"]))
                curated.add(key)
                existing = None
            path = destination.parent / (identifier + ".json")
            write_changed(path, profile)
            rows.append({"id": identifier, "area_id": f"{ai:02}", "area": area,
                "subtopico": title, "profile": path.relative_to(ROOT).as_posix(),
                "profile_sha256": file_hash(path), "existing_packet": existing})
    if curated != set(PLANS):
        raise ValueError("A curadoria e as frases do especialista divergiram")
    program = {"schema": "document-program-v1", "areas": len(TOPICOS),
        "source": "pipeline/fase_3/topicos.py", "source_sha256": file_hash(ROOT / "pipeline/fase_3/topicos.py"),
        "curation": "pipeline/qa_research/document/curation.py",
        "curation_sha256": file_hash(Path(__file__).with_name("curation.py")), "items": rows}
    write_changed(destination, program)
    return program


def load_program(path=DEFAULT_PROGRAM):
    program = read_json(absolute(path))
    if not program or program.get("schema") != "document-program-v1":
        raise ValueError("Programa documental ausente ou incompatível")
    ids = [r["id"] for r in program["items"]]
    if len(ids) != len(set(ids)) or not ids:
        raise ValueError("Identificadores de frases inválidos")
    for row in program["items"]:
        if file_hash(absolute(row["profile"])) != row["profile_sha256"]:
            raise ValueError("Perfil mudou; reconstrua o programa: " + row["id"])
        load_profile(absolute(row["profile"]))
    return program
