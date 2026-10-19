"""Reaproveita apenas a investigação, nunca redação/auditoria de uma versão anterior."""
from copy import deepcopy
from pathlib import Path

from pipeline.inventario.textutil import atomic_json, read_json, sha
from . import contracts as C
from .common import canonical, file_hash


def reuse_research(packet, source, output, states, save):
    source, output = Path(source).resolve(), Path(output).resolve()
    if source == output or source in output.parents or output in source.parents:
        raise ValueError("Pesquisa anterior e nova saída devem ficar separadas")
    paths = ["identidade.json", *("recortes/" + f["id"] + ".json" for f in packet.facets)]
    manifest = read_json(source / "manifest_resultados.json")
    hashes = {}
    for name in paths:
        path = source / name
        if not path.is_file() or path.is_symlink():
            raise ValueError("Arquivo de pesquisa anterior ausente/inválido: " + name)
        hashes[name] = file_hash(path)
        if manifest and manifest.get("files", {}).get(name) != hashes[name]:
            raise ValueError("Snapshot anterior alterado: " + name)
    if read_json(source / "identidade.json").get("packet") != packet.signature:
        raise ValueError("A pesquisa anterior pertence a outro pacote")
    signature = sha(canonical({"packet": packet.signature, "files": hashes}), 64)
    receipt_path = output / "pesquisa_reutilizada.json"
    receipt = read_json(receipt_path)
    if receipt and receipt["signature"] != signature:
        raise ValueError("A origem da pesquisa reutilizada mudou; use outra saída")
    if receipt and receipt.get("complete"):
        return
    seeds = {}
    for facet in packet.facets:
        fid = facet["id"]
        current = states[fid]
        if current["seen"] and current.get("research_seed") != signature:
            raise ValueError("Informe --reuse-research na primeira execução de uma saída nova")
        if current["versions"]:
            raise ValueError("Não sobrescreva uma redação iniciada ao reutilizar pesquisa")
        old = read_json(source / "recortes" / (fid + ".json"))
        C.strings(old["seen"], len(facet["fontes"]))
        if old.get("id") != fid or not set(old["seen"]) <= set(facet["fontes"]):
            raise ValueError("Fontes lidas fora do catálogo do recorte")
        if type(old["read_done"]) is not bool or type(old["round"]) is not int or old["round"] < 0:
            raise ValueError("Estado de pesquisa anterior inválido")
        assessments = old["assessments"]
        C.research_core({"avaliacoes": [{**r, "achados": []} for r in assessments],
                         "concluir": old["read_done"], "proximas_fontes": [], "pedidos_busca": [], "lacunas": []}, old["seen"])
        assessed = {r["id"]: r for r in assessments}
        for finding in old["findings"]:
            C.obj(finding, {"proposicao", "trechos", "condicoes", "limites", "fonte", "tipo"})
            C.text(finding["proposicao"], 1000)
            C.strings(finding["condicoes"], 6)
            C.strings(finding["limites"], 6)
            if finding["fonte"] not in old["seen"] or finding["tipo"] not in C.TYPES:
                raise ValueError("Achado anterior fora da investigação validada")
            if not assessed[finding["fonte"]]["pertinente"] or assessed[finding["fonte"]]["tipo"] != finding["tipo"]:
                raise ValueError("Achado anterior contradiz a avaliação de sua fonte")
            C.refs(finding["trechos"], packet.by_source[finding["fonte"]])
        seed = deepcopy(current)
        for key in ("round", "read_done", "seen", "assessments", "findings"):
            seed[key] = deepcopy(old[key])
        seed["requests"] = [q for q in old.get("requests", []) if isinstance(q, str) and 0 < len(q) <= 1800][:30]
        seed["next"] = []
        seed["gap_history"] = [deepcopy(g) for g in old.get("gap_history", [])
                               if str(g.get("origem", "")).startswith("pesquisa_")]
        seed["status"] = "pesquisado" if seed["read_done"] else "pesquisando"
        seed["research_seed"] = signature
        seeds[fid] = seed
    # Recibo incompleto permite retomar uma interrupção entre gravações, sem API.
    receipt = {"signature": signature, "source": str(source), "files": hashes, "complete": False,
               "reused": ["leituras", "avaliacoes", "achados"], "new_generation": ["redacao", "auditoria", "consolidacao"]}
    atomic_json(receipt_path, receipt)
    for fid, seed in seeds.items():
        states[fid] = seed
        save(seed)
    atomic_json(receipt_path, {**receipt, "complete": True})
