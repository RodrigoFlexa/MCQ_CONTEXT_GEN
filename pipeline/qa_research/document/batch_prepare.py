"""Uma leitura do corpus para todas as frases; um E5 e cache compartilhados."""
import heapq
import re
import time
from collections import Counter, defaultdict

from pipeline.inventario.locking import output_lock
from pipeline.inventario.textutil import atomic_json, read_json, sha
from .common import Packet, absolute, canonical, file_hash, load_profile, source_record
from .prepare import (prepare, inputs, fold, context_filter, reference_list,
                      acronym_list, bibliographic_catalog)
from .program import load_program, DEFAULT_PROGRAM, DEFAULT_PACKETS


def shared_frontiers(jobs, progress=print):
    """Aho-Corasick encontra todas as âncoras de todos os perfis na mesma passagem.

    Conta correspondências sobrepostas (declarado na identidade da triagem).
    Limites por recorte impedem que o corpus inteiro seja embeddado ou carregado.
    """
    import ahocorasick
    first = jobs[0][1]
    if any(p["inputs"] != first["inputs"] for _, p in jobs):
        raise ValueError("A varredura compartilhada exige o mesmo conjunto de entradas")
    cache = absolute(first["cache_dir"])
    cache.mkdir(parents=True, exist_ok=True)
    result, pending = {}, []
    with output_lock(cache):
        hashes = read_json(cache / "file_hashes.json") or {}
        stream, fingerprints, mode, missing = inputs(first, hashes, progress)
        atomic_json(cache / "file_hashes.json", hashes)
        for item, profile in jobs:
            # Pós-filtros só estreitam a fronteira salva; refiná-los não exige
            # outra varredura dos originais nem novos embeddings das passagens.
            coarse_facets = [{k: v for k, v in f.items() if k != "post_context_groups"} for f in profile["facets"]]
            identity = {"version": "joint-aho-frontier-v1", "inputs": fingerprints,
                        "facets": coarse_facets, "selection": profile["selection"]}
            fingerprint = sha(canonical(identity), 64)
            path = cache / ("joint-frontier-" + fingerprint + ".json")
            old = read_json(path)
            if old and old.get("fingerprint") == fingerprint:
                result[item["id"]] = old
            else:
                pending.append((item, profile, path, fingerprint))
        if not pending:
            progress("Todas as fronteiras locais já estão prontas; corpus não será relido")
            return result
        term_facets, specs = defaultdict(set), []
        for item, profile, _, _ in pending:
            for f in profile["facets"]:
                fi = len(specs)
                specs.append({"job": item["id"], "facet": f["id"], "rule": context_filter(f),
                    "limit": profile["selection"]["frontier_per_facet"], "heap": [], "seen": set(),
                    "preferred": [fold(t) for t in profile["selection"].get("preferred_context", [])]})
                for term in f["termos"]:
                    term_facets[fold(term)].add(fi)
        automaton = ahocorasick.Automaton()
        for term, indices in term_facets.items():
            automaton.add_word(term, (term, tuple(indices)))
        automaton.make_automaton()
        scanned = serial = 0
        progress(f"Uma varredura compartilhada: {len(pending)} frases, {len(specs)} recortes, {len(term_facets)} âncoras")
        for row in stream:
            text = row.get("texto", row.get("text", ""))
            if not isinstance(text, str) or not text.strip() or not row.get("chunk_id"):
                continue
            scanned += 1
            normalized = fold(text)
            matches = defaultdict(Counter)
            for _, (term, indices) in automaton.iter(normalized):
                for fi in indices:
                    matches[fi][term] += 1
            if matches and not reference_list(normalized) and not acronym_list(text) and not bibliographic_catalog(text):
                source = digest = None
                for fi, hits in matches.items():
                    s = specs[fi]
                    if not s["rule"](normalized):
                        continue
                    score = len(hits) * 8 + min(sum(hits.values()), 16) * .15
                    score += min(4, sum(t in normalized for t in s["preferred"])) * 3
                    score += .8 if row.get("collection") != "petroles" else 0
                    score += .6 if "<NUMBER>" not in text else 0
                    heap = s["heap"]
                    if len(heap) >= s["limit"] and score <= heap[0][0]:
                        continue
                    if digest is None:
                        digest = sha(re.sub(r"\s+", " ", text).strip(), 64)
                    if digest in s["seen"]:
                        continue
                    if source is None:
                        source = source_record(row)
                    serial += 1
                    entry = (score, -serial, digest, source)
                    if len(heap) < s["limit"]:
                        heapq.heappush(heap, entry)
                    else:
                        removed = heapq.heapreplace(heap, entry)
                        s["seen"].discard(removed[2])
                    s["seen"].add(digest)
            if scanned % 25000 == 0:
                progress(f"Varredura conjunta: {scanned:,} janelas")
        for item, profile, path, fingerprint in pending:
            frontier = {"fingerprint": fingerprint, "scanned": scanned, "inputs": fingerprints,
                "input_mode": mode, "missing_inputs": missing,
                "rows": {s["facet"]: [{"score": a[0], "source": a[3]} for a in sorted(s["heap"], reverse=True)]
                         for s in specs if s["job"] == item["id"]}}
            atomic_json(path, frontier)
            result[item["id"]] = frontier
    return result


def prepare_program(program_path=DEFAULT_PROGRAM, destination=DEFAULT_PACKETS,
                    device="auto", batch_size=64, progress=print):
    program = load_program(program_path)
    destination = absolute(destination)
    destination.mkdir(parents=True, exist_ok=True)
    started = time.monotonic()
    entries, jobs = [], []
    with output_lock(destination):
        for item in program["items"]:
            profile = load_profile(absolute(item["profile"]))
            packet_path = absolute(item["existing_packet"]) if item.get("existing_packet") else destination / item["id"]
            if packet_path.exists():
                packet = Packet(packet_path)
                if packet.profile != profile:
                    raise ValueError("Pacote existente usa outro perfil; use novo destino: " + item["id"])
                progress("Pacote pronto e verificado: " + item["id"])
            else:
                jobs.append((item, profile))
        execution = None
        if jobs:
            from ..selection import LocalE5
            # Falhar antes da longa leitura se o Python/modelo/GPU estiver incorreto.
            model = LocalE5(absolute(jobs[0][1]["cache_dir"]), device=device, batch_size=batch_size)
            execution = model.execution
            progress("Embeddings locais: " + canonical(execution))
            try:
                frontiers = shared_frontiers(jobs, progress)
                for i, (item, profile) in enumerate(jobs, 1):
                    progress(f"Preparando frase {i}/{len(jobs)}: {item['id']} {item['subtopico']}")
                    if not any(frontiers[item["id"]]["rows"].values()):
                        raise ValueError("Nenhuma fonte para " + item["id"] + "; revise a curadoria antes de enviar ao servidor")
                    prepare(absolute(item["profile"]), destination / item["id"],
                            progress=progress, frontier_data=frontiers[item["id"]], shared_model=model)
            finally:
                model.close()
        for item in program["items"]:
            packet_path = absolute(item["existing_packet"]) if item.get("existing_packet") else destination / item["id"]
            packet = Packet(packet_path)
            entries.append({**{k: item[k] for k in ("id", "area_id", "area", "subtopico")},
                "packet": packet_path.relative_to(absolute('.')).as_posix(), "signature": packet.signature,
                "profile_sha256": item["profile_sha256"],
                "sources": len(packet.sources), "facets": len(packet.facets),
                "empty_facets": [f["id"] for f in packet.facets if not f["fontes"]]})
        # Só publica o catálogo quando TODOS os pacotes foram verificados.
        manifest = {"schema": "document-batch-v1", "program": str(absolute(program_path).relative_to(absolute('.')).as_posix()),
            "program_sha256": file_hash(absolute(program_path)), "items": entries}
        old = read_json(destination / "lote.json")
        if old and old != manifest:
            raise ValueError("Catálogo publicado divergente; use novo destino")
        if not old:
            atomic_json(destination / "lote.json", manifest)
        info = {"areas": len({r["area_id"] for r in entries}), "phrases": len(entries),
            "facets": sum(r["facets"] for r in entries), "source_assignments": sum(r["sources"] for r in entries),
            "execution": execution, "seconds": round(time.monotonic() - started, 2),
            "empty_facets": {r["id"]: r["empty_facets"] for r in entries if r["empty_facets"]}}
        progress(canonical(info))
        return info
