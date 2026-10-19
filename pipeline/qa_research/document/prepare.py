"""Leitura/triagem pesada local; o pacote final contém somente fontes selecionadas."""
import heapq
import itertools
import json
import os
import re
import shutil
import tempfile
import time
import unicodedata
from pathlib import Path

from pipeline.inventario.locking import output_lock
from pipeline.inventario.textutil import atomic_json, read_json, sha
from ..corpus import _saved_chunks, _selection_files, _manifest_chunks
from ..portable import _publish
from .common import Packet, absolute, canonical, citations_for, file_hash, load_profile, source_record


def fold(text):
    return "".join(c for c in unicodedata.normalize("NFKD", text.casefold()) if not unicodedata.combining(c))


def context_filter(facet):
    """Compile uma vez por recorte, em vez de normalizar cada termo por janela."""
    def pattern(terms):
        folded = list(dict.fromkeys(fold(t) for t in terms))
        return re.compile("|".join((r"\b" + re.escape(t) + r"\b") if len(t) <= 3 else re.escape(t) for t in folded)) if folded else None
    excluded = pattern(facet.get("exclude_context", []))
    groups = [pattern(g) for g in facet.get("context_groups", [])]
    return lambda text: (not excluded or not excluded.search(text)) and all(g and g.search(text) for g in groups)


def contextual(text, facet):
    """Entrada simples para validar os filtros fora da leitura em streaming."""
    return bool(context_filter(facet)(text))


def reference_list(text):
    if text.count("numero do registro") >= 2 or text.count("outros autores") >= 2:
        return True
    heading = re.search(r"\b(?:referencias(?: bibliograficas)?|references|bibliography)\b", text)
    if not heading or heading.start() > len(text) * .35:
        return False
    # Uma frase com 'referências' não basta para rejeitar a passagem.
    return len(re.findall(r"\b(?:astm|isbn|issn|doi|thesis|dissertacao|tese|congresso|conference|proceedings|vol|pp)\b", text[heading.end():])) >= 4


def acronym_list(text):
    # Listas de siglas podem conter todos os termos da consulta sem fornecer
    # conhecimento sobre aplicação. Preserve abstracts anexados ao mesmo chunk.
    if re.search(r"\b(?:resumo|abstract)\b", text, re.I):
        return False
    return len(re.findall(r"\b[A-Z][A-Z0-9]{1,8}\s*[-–—]\s*[A-ZÀ-Ö]", text)) >= 8


def bibliographic_catalog(text):
    text = fold(text)
    return "resumos separados por assuntos" in text or ("sao emitidos por ano" in text and "resumos" in text)


def digest_cached(path, cache):
    path = Path(path).resolve()
    stat = path.stat()
    stamp = [stat.st_size, stat.st_mtime_ns, stat.st_ctime_ns]
    old = cache.get(str(path), {})
    digest = old.get("sha256") if old.get("stat") == stamp else file_hash(path)
    cache[str(path)] = {"stat": stamp, "sha256": digest}
    return digest


def inputs(profile, cache, progress):
    spec = profile["inputs"]
    fingerprints, generators, missing = [], [], []
    if spec.get("manifest") and absolute(spec["manifest"]).is_file():
        from pipeline.domain_corpora.manifest import load_manifest
        _, collections = load_manifest(absolute(spec["manifest"]), verify=True)
        generators.append(_manifest_chunks(collections))
        fingerprints.append({"kind": "manifest", "sha256": file_hash(absolute(spec["manifest"]))})
        mode = "manifesto_completo"
    else:
        mode = "petroles_bruto_e_selecoes_parciais"
        if spec.get("manifest"):
            missing.append(spec["manifest"])
        for item in spec.get("raw_texts", []):
            path = absolute(item)
            if not path.is_file():
                missing.append(item)
                continue
            progress("Verificando texto original: " + path.name)
            digest = digest_cached(path, cache)
            fingerprints.append({"kind": "raw_text", "name": path.name, "sha256": digest})
            generators.append(_manifest_chunks([{"id": "petroles", "format": "petroles_txt",
                "files": [{"resolved_path": path, "sha256": digest}]}]))
        present_origins = [absolute(p) for p in spec.get("origins", []) if absolute(p).exists()]
        if present_origins:
            files = _selection_files(present_origins)
            fingerprints.extend({"kind": "selection", "name": str(p.relative_to(absolute('.'))),
                                 "sha256": digest_cached(p, cache)} for p in files)
            generators.append(_saved_chunks(files))
    for item in spec.get("evidence_exports", []):
        path = absolute(item)
        if not path.is_file():
            missing.append(item)
            continue
        fingerprints.append({"kind": "previous_evidence", "name": path.name, "sha256": digest_cached(path, cache)})
        def exported(filename=path):
            with filename.open(encoding="utf-8") as stream:
                for line in stream:
                    row = json.loads(line)
                    if row.get("source_kind") in ("saved_selection", "verified_manifest"):
                        yield row
        generators.append(exported())
    if not generators:
        raise ValueError("Nenhum corpus original/seleção verificável disponível localmente")
    return itertools.chain.from_iterable(generators), fingerprints, mode, missing


def prepare(profile_path, destination, semantic=True, feedback=None, progress=print):
    profile = load_profile(profile_path)
    destination = absolute(destination)
    if destination.exists():
        raise ValueError("Pacote publicado já existe; use outro destino para uma nova preparação")
    cache_dir = absolute(profile.get("cache_dir", "pipeline/qa_research/.local/document"))
    if cache_dir == destination or destination in cache_dir.parents or cache_dir in destination.parents:
        raise ValueError("Pacote deve ficar separado do cache local")
    for item in [*profile["inputs"].get("raw_texts", []), *profile["inputs"].get("origins", [])]:
        path = absolute(item)
        if destination == path or destination in path.parents or path in destination.parents:
            raise ValueError("Destino deve ficar separado dos originais")
    cache_dir.mkdir(parents=True, exist_ok=True)
    started = time.monotonic()
    with output_lock(cache_dir):
        hashes = read_json(cache_dir / "file_hashes.json") or {}
        stream, fingerprints, mode, missing = inputs(profile, hashes, progress)
        atomic_json(cache_dir / "file_hashes.json", hashes)
        facets = profile["facets"]
        context_rules = {f["id"]: context_filter(f) for f in facets}
        post_rules = {f["id"]: context_filter({**f, "context_groups":
                      f.get("context_groups", []) + f.get("post_context_groups", [])}) for f in facets}
        preferred = [fold(t) for t in profile["selection"].get("preferred_context", [])]
        auxiliary = {}
        if feedback:
            prior = read_json(absolute(feedback))
            if prior.get("topic") != profile["topic"]:
                raise ValueError("Pedidos de busca pertencem a outro tópico")
            auxiliary = {f["facet_id"]: f.get("queries", []) for f in prior.get("requests", [])}
        # Filtros adicionais só estreitam a fronteira já pronta. Alterá-los não
        # exige reler os originais; a fronteira ampla permanece igual.
        coarse_facets = [{k: v for k, v in f.items() if k != "post_context_groups"} for f in facets]
        selection_identity = {"version": "local-frontier-v2.2-context", "inputs": fingerprints,
                              "facets": coarse_facets, "selection": profile["selection"], "feedback": auxiliary}
        fingerprint = sha(canonical(selection_identity), 64)
        frontier_file = cache_dir / ("frontier-" + fingerprint + ".json")
        frontier = read_json(frontier_file)
        if frontier is None:
            progress("Triagem lexical em streaming: leitura local, sem embeddings de todo o corpus")
            patterns = []
            for f in facets:
                terms = [fold(t) for t in f["termos"]]
                # Pedidos adicionais ampliam o ranking; não são instruções executáveis.
                extra = re.findall(r"[a-z]{5,}", fold(" ".join(auxiliary.get(f["id"], []))))
                terms.extend(t for t in extra if t not in {"sobre", "entre", "which", "their", "where", "chemical", "quimico"})
                patterns.append(re.compile("|".join(re.escape(t) for t in dict.fromkeys(terms))))
            heaps, seen = [[] for _ in facets], [set() for _ in facets]
            serial, scanned, matched = 0, 0, 0
            limit = profile["selection"]["frontier_per_facet"]
            for row in stream:
                text = row.get("texto", row.get("text", ""))
                if not isinstance(text, str) or not text.strip() or not row.get("chunk_id"):
                    continue
                scanned += 1
                normalized = fold(text)
                if reference_list(normalized):
                    continue
                for fi, pattern in enumerate(patterns):
                    hits = list(pattern.finditer(normalized))
                    if not hits:
                        continue
                    if not context_rules[facets[fi]["id"]](normalized):
                        continue
                    unique = len({m.group() for m in hits})
                    # Cobertura vocabular pesa mais que repetição de uma palavra.
                    score = unique * 8 + min(len(hits), 16) * .15
                    score += min(4, sum(t in normalized for t in preferred)) * 3
                    score += .8 if row.get("collection") != "petroles" else 0
                    score += .6 if "<NUMBER>" not in text else 0
                    heap = heaps[fi]
                    if len(heap) >= limit and score < heap[0][0]:
                        continue
                    digest = sha(re.sub(r"\s+", " ", text).strip(), 64)
                    if digest in seen[fi]:
                        continue
                    source = source_record(row)
                    serial += 1
                    entry = (score, -serial, digest, source)
                    if len(heap) >= limit and entry <= heap[0]:
                        continue
                    if len(heap) < limit:
                        heapq.heappush(heap, entry)
                    else:
                        removed = heapq.heapreplace(heap, entry)
                        seen[fi].discard(removed[2])
                    seen[fi].add(digest)
                    matched += 1
                if scanned % 25000 == 0:
                    progress(f"Triagem local: {scanned:,} janelas examinadas")
            frontier = {"fingerprint": fingerprint, "scanned": scanned, "entries": matched,
                "rows": {f["id"]: [{"score": a[0], "source": a[3]} for a in sorted(h, reverse=True)]
                         for f, h in zip(facets, heaps)}}
            atomic_json(frontier_file, frontier)
        else:
            progress("Reutilizando triagem local pronta, sem reler o corpus")
        from collections import OrderedDict
        candidates = OrderedDict((r["source"]["id"], r["source"])
                                 for rows in frontier["rows"].values() for r in rows)
        excluded_lists = [sid for sid, row in candidates.items() if acronym_list(row["texto"]) or bibliographic_catalog(row["texto"])]
        candidates = OrderedDict((sid, row) for sid, row in candidates.items() if sid not in excluded_lists)
        if not candidates:
            raise ValueError("A fronteira só contém listas de siglas, sem conteúdo técnico substantivo")
        semantic_scores, semantic_protocol = {}, None
        if semantic:
            from ..selection import LocalE5
            import numpy as np
            progress(f"Triagem E5 local de {len(candidates)} candidatos, após o filtro amplo")
            model = LocalE5(cache_dir, offline=True, threads=profile["selection"].get("threads", 4))
            try:
                queries = [q for f in facets for q in [*f["consultas"], *auxiliary.get(f["id"], [])]]
                query_vectors = model.queries(queries)
                offsets, offset = {}, 0
                for f in facets:
                    size = len(f["consultas"]) + len(auxiliary.get(f["id"], []))
                    offsets[f["id"]] = (offset, offset + size)
                    offset += size
                candidate_rows = list(candidates.values())
                for start in range(0, len(candidate_rows), 24):
                    batch = candidate_rows[start:start + 24]
                    windows = model.passages_many([r["texto"] for r in batch])
                    for row, matrix in zip(batch, windows):
                        values = np.max(query_vectors @ matrix.T, axis=1)
                        semantic_scores[row["id"]] = {f["id"]: float(max(values[a:b]))
                            for f in facets for a, b in [offsets[f["id"]]]}
                    model.flush()
                    progress(f"E5 local: {min(start + len(batch), len(candidate_rows))}/{len(candidate_rows)}")
                semantic_protocol = model.protocol
            finally:
                model.close()
        selected_sources, selected_facets = {}, []
        for f in facets:
            lexical = [r for r in frontier["rows"][f["id"]] if r["source"]["id"] in candidates and post_rules[f["id"]](fold(r["source"]["texto"]))]
            # Canal semântico pode promover candidatos de OUTROS recortes da
            # fronteira temática, sem exigir correspondência lexical neste recorte.
            dense = sorted((sid for sid in candidates if post_rules[f["id"]](fold(candidates[sid]["texto"]))),
                           key=lambda sid: (-semantic_scores[sid][f["id"]], sid)) if semantic else []
            fusion = {}
            for channel, ids in (("lexical", [r["source"]["id"] for r in lexical]), ("semantic", dense)):
                for rank, sid in enumerate(ids, 1):
                    # Limita o canal semântico ao mesmo orçamento do lexical.
                    if rank > profile["selection"]["frontier_per_facet"]:
                        break
                    item = fusion.setdefault(sid, {"score": 0., "channels": {}})
                    item["score"] += 1 / (60 + rank)
                    item["channels"][channel] = rank
            chosen, tokens, doc_counts = [], set(), {}
            for sid, item in sorted(fusion.items(), key=lambda x: (-x[1]["score"], x[0])):
                source = candidates[sid]
                # Deduplica cópias quase iguais, sem usar equivalência numérica
                # para substituir uma fonte por outra ou recuperar valores.
                words = fold(source["texto"]).split()
                shingles = frozenset(" ".join(words[i:i + 5]) for i in range(0, len(words) - 4, 3))
                if shingles and any(len(shingles & old) / max(1, len(shingles | old)) > .88 for old in tokens):
                    continue
                doc = (source.get("collection"), source.get("document_id"))
                known = source["qualidade"]["documento_identificado"]
                if known and doc_counts.get(doc, 0) >= profile["selection"].get("max_per_document", 8):
                    continue
                chosen.append(sid)
                tokens.add(shingles)
                if known:
                    doc_counts[doc] = doc_counts.get(doc, 0) + 1
                selected_sources[sid] = source
                if len(chosen) >= profile["selection"]["sources_per_facet"]:
                    break
            selected_facets.append({**f, "fontes": chosen,
                "ranking": {sid: fusion[sid] for sid in chosen},
                "pedidos_locais_incluidos": auxiliary.get(f["id"], [])})
        if not selected_sources:
            raise ValueError("Triagem não encontrou fontes; reveja entradas e termos")
        destination.parent.mkdir(parents=True, exist_ok=True)
        staging = Path(tempfile.mkdtemp(prefix=".document-", dir=destination.parent))
        try:
            atomic_json(staging / "profile.json", profile)
            atomic_json(staging / "facets.json", selected_facets)
            with (staging / "sources.jsonl").open("w", encoding="utf-8", newline="\n") as sources_file, \
                    (staging / "citations.jsonl").open("w", encoding="utf-8", newline="\n") as citations_file:
                for sid in sorted(selected_sources):
                    source = selected_sources[sid]
                    sources_file.write(canonical(source) + "\n")
                    for c in citations_for(source):
                        citations_file.write(canonical(c) + "\n")
            info = {"inputs": fingerprints, "input_mode": mode, "missing_inputs": missing,
                "corpus_completo": False, "coverage": "subconjunto_tematico; recuperação integral não demonstrada",
                "scanned_windows": frontier["scanned"], "frontier_unique": len(candidates),
                "excluded_non_substantive": excluded_lists,
                "selected_sources": len(selected_sources), "semantic_protocol": semantic_protocol,
                "facets": [{"id": f["id"], "sources": len(f["fontes"])} for f in selected_facets],
                "seconds": round(time.monotonic() - started, 3),
                "limitations": ["A triagem temática pode omitir fontes pertinentes.",
                    "Números ausentes não foram reconstruídos.",
                    "O servidor explora este pacote e registra buscas adicionais para a próxima rodada local."]}
            atomic_json(staging / "preparation.json", info)
            files = {name: file_hash(staging / name) for name in
                     ("profile.json", "sources.jsonl", "citations.jsonl", "facets.json", "preparation.json")}
            if sum((staging / name).stat().st_size for name in files) > profile["selection"].get("max_packet_bytes", 20000000):
                raise ValueError("Pacote excede limite para Git; reduza fontes por recorte")
            atomic_json(staging / "manifest.json", {"schema": "document-packet-v2", "files": files})
            Packet(staging)
            _publish(staging, destination)
            return info
        finally:
            if staging.exists() and staging.resolve().parent == destination.parent and staging.name.startswith(".document-"):
                shutil.rmtree(staging)
