"""Local, auditable corpus retrieval without a model or external service.

A verified domain-corpora manifest takes precedence. Without one, only original
excerpts in ``selecao.json`` are indexed and coverage is explicitly partial.
Generated reports, extracted claims, notes and questions are never discovered.
"""
from __future__ import annotations

import hashlib
import json
import re
import sqlite3
import tempfile
import time
from collections import Counter
from contextlib import closing
from pathlib import Path


_VERSION = "qa-research-corpus-v1"
_ENGINE = "SQLite FTS5 BM25"
_CHUNK_WORDS, _STRIDE = 350, 250
_STOP = frozenset("a ao aos as com da das de do dos e em entre essa esse esta este foi is na nas no nos o os ou para pela pelo por que se sem sobre um uma the a an and are as at be by for from how in into is it of on or that this to was were what which with".split())
_GENERATED_KINDS = {"generated", "synthetic", "generated_document", "technical_dossier", "research_note", "claim", "fact", "note", "qa"}


def _json(value):
    return json.dumps(value, ensure_ascii=False, sort_keys=True)


def _digest(value):
    return hashlib.sha256(value.encode("utf-8")).hexdigest()


def _file_hash(path):
    digest = hashlib.sha256()
    with Path(path).open("rb") as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def _body_hash(text):
    # Preserve letter case: scientific symbols can change meaning with case.
    return _digest(re.sub(r"\s+", " ", text).strip())


def _known_boundaries(row):
    boundary = str(row.get("source_boundary", "")).lower()
    if "unknown" in boundary or "concatenated" in boundary or row.get("document_boundaries_known") is False:
        return False
    if not row.get("document_id"):
        return False
    return (row.get("document_boundaries_known") is True
            or boundary in {"known_document", "document", "document_and_page"}
            or isinstance(row.get("page_ini", row.get("page")), int))


def _selection_files(origins):
    paths = set()
    for origin in origins:
        origin = Path(origin).resolve()
        if not origin.exists():
            raise FileNotFoundError(f"Origem do corpus ausente: {origin}")
        if origin.is_file():
            if origin.name != "selecao.json":
                raise ValueError("O fallback aceita somente arquivos selecao.json com trechos originais")
            paths.add(origin)
        else:
            paths.update(origin.rglob("selecao.json"))
    return sorted(paths)


def _saved_chunks(files):
    for path in files:
        data = json.loads(path.read_text(encoding="utf-8-sig"))
        subjects = data.get("assuntos")
        if not isinstance(subjects, dict):
            raise ValueError(f"Seleção sem o objeto assuntos: {path}")
        for subject in subjects.values():
            if not isinstance(subject, dict) or not isinstance(subject.get("trechos", []), list):
                raise ValueError(f"Formato de seleção inválido: {path}")
            for chunk in subject.get("trechos", []):
                if not isinstance(chunk, dict):
                    raise ValueError(f"Trecho inválido na seleção: {path}")
                if (chunk.get("source_kind") in _GENERATED_KINDS
                        or chunk.get("generated") is True or chunk.get("synthetic") is True):
                    continue
                yield {**chunk, "source_kind": "saved_selection", "source_file": str(path)}


def _manifest_chunks(collections):
    """Streaming word windows, preserving document/page/line provenance.

    This is independent of the old retrieval/generation implementation. Unknown
    boundaries in concatenated TXT remain unknown, including for neighbours.
    A page gap ends a window instead of inventing missing intervening content.
    """
    from pipeline.domain_corpora.manifest import iter_units

    for collection in collections:
        key, metadata, previous_page = None, None, None
        buffer, position, fresh = [], 0, 0
        source_file = (str(collection["resolved_path"]) if collection["format"] == "pages_jsonl"
                       else None)

        def emit():
            pages = [part[1] for part in buffer if part[1] is not None]
            lines = [part[2] for part in buffer if part[2] is not None]
            result = {k: v for k, v in metadata.items() if k not in {"text", "texto", "page", "line"}}
            result.update(page_ini=pages[0] if pages else None,
                          page_fim=pages[-1] if pages else None,
                          linha_ini=lines[0] if lines else None,
                          linha_fim=lines[-1] if lines else None,
                          word_offset=position, texto=" ".join(part[0] for part in buffer),
                          source_kind="verified_manifest", source_file=source_file,
                          whitespace_normalized=True)
            if collection["format"] == "petroles_txt":
                result["source_file"] = next((str(item["resolved_path"]) for item in collection["files"]
                    if item["sha256"] == metadata.get("source_sha256")), None)
            if collection["format"] == "pages_jsonl":
                result.setdefault("source_boundary", "known_document")
            result["chunk_id"] = f"{result['collection']}:{result['document_id']}:p{result['page_ini']}:w{position}"
            return result

        for unit in iter_units([collection]):
            unit_key = (unit["collection"], unit["document_id"])
            page = unit.get("page")
            gap = (unit_key == key and isinstance(page, int) and isinstance(previous_page, int)
                   and page not in (previous_page, previous_page + 1))
            if unit_key != key or gap:
                if buffer and fresh:
                    yield emit()
                position = position + len(buffer) if unit_key == key else 0
                buffer, fresh = [], 0
                key, metadata = unit_key, unit
            previous_page = page
            for word in unit["text"].split():
                buffer.append((word, page, unit.get("line")))
                fresh += 1
                if len(buffer) == _CHUNK_WORDS:
                    yield emit()
                    buffer = buffer[_STRIDE:]
                    position += _STRIDE
                    fresh = 0
        if buffer and fresh:
            yield emit()


class CorpusIndex:
    """Persistent BM25 baseline. Call ``build`` once before a research run.

    Returned ``chunk_id`` values are the original identifiers, never rewritten.
    Content duplicates retain all original identifiers in ``chunk_id_aliases``
    and source metadata in ``provenance``. ``exclude`` accepts either an original
    identifier or a ``content_hash``. Optional neighbours are attached separately
    in ``neighbor_chunks``; ``limit`` always limits primary results.
    """

    def __init__(self, directory, origins=(), manifest=None):
        self.directory = Path(directory).resolve()
        self.origins = tuple(Path(origin) for origin in origins)
        self.manifest = Path(manifest).resolve() if manifest else None
        self.path = self.directory / "corpus.sqlite3"
        self.info = None
        self.last_query_trace = None

    def build(self):
        collections = None
        if self.manifest:
            from pipeline.domain_corpora.manifest import load_manifest
            manifest_data, collections = load_manifest(self.manifest, verify=True)
            files = [{"path": str(self.manifest), "sha256": _file_hash(self.manifest)}]
            for collection in collections:
                if collection["format"] == "pages_jsonl":
                    files.append({"path": str(collection["resolved_path"]), "sha256": collection["sha256"]})
                else:
                    files.extend({"path": str(item["resolved_path"]), "sha256": item["sha256"]}
                                 for item in collection["files"])
            chunks = _manifest_chunks(collections)
            coverage, complete = "verified_manifest", not manifest_data.get("sample", False)
        else:
            selection_paths = _selection_files(self.origins)
            if not selection_paths:
                raise ValueError("Nenhum selecao.json original encontrado. Informe origens ou um manifesto completo verificável.")
            files = [{"path": str(path), "sha256": _file_hash(path)} for path in selection_paths]
            chunks = _saved_chunks(selection_paths)
            coverage, complete = "saved_selections_partial", False
        fingerprint = _digest(_json({"version": _VERSION, "files": files,
                                     "chunk_words": _CHUNK_WORDS, "stride": _STRIDE}))
        # Each corpus snapshot has its own immutable location. A different run
        # may share the cache root without silently changing this instance's DB.
        snapshot_directory = self.directory / fingerprint
        self.path = snapshot_directory / "corpus.sqlite3"
        info_path = snapshot_directory / "indice.json"
        try:
            previous = json.loads(info_path.read_text(encoding="utf-8"))
            if previous.get("fingerprint") == fingerprint and self.path.is_file():
                with closing(sqlite3.connect(self.path)) as db:
                    stored = db.execute("SELECT value FROM metadata WHERE key='fingerprint'").fetchone()
                if stored and stored[0] == fingerprint:
                    self.info = previous
                    return self.info
        except (FileNotFoundError, json.JSONDecodeError, sqlite3.DatabaseError):
            pass
        snapshot_directory.mkdir(parents=True, exist_ok=True)
        with tempfile.NamedTemporaryFile(prefix="corpus-", suffix=".build.sqlite3", dir=snapshot_directory, delete=False) as stream:
            temporary = Path(stream.name)
        db = sqlite3.connect(temporary)
        try:
            db.executescript("""
                CREATE TABLE metadata(key TEXT PRIMARY KEY, value TEXT);
                CREATE TABLE chunks(id INTEGER PRIMARY KEY, digest TEXT UNIQUE, body TEXT, payload TEXT);
                CREATE TABLE sources(chunk INTEGER, uid TEXT UNIQUE, original_id TEXT, doc TEXT,
                                     pos INTEGER, known INTEGER, payload TEXT);
                CREATE INDEX original_ids ON sources(original_id);
                CREATE INDEX positions ON sources(doc,pos);
                CREATE INDEX source_chunks ON sources(chunk);
                CREATE VIRTUAL TABLE search USING fts5(body,content='chunks',content_rowid='id',
                                                       tokenize='unicode61 remove_diacritics 2');
            """)
            count, invalid, source_count = 0, 0, 0
            by_collection = Counter()
            for chunk in chunks:
                body = chunk.get("texto", chunk.get("text", ""))
                original_id = chunk.get("chunk_id")
                if not isinstance(body, str) or not body.strip() or not isinstance(original_id, str) or not original_id:
                    invalid += 1
                    continue
                chunk = {**chunk, "texto": body, "chunk_id_original": original_id}
                for field in ("collection", "document_id", "title"):
                    chunk.setdefault(field, None)
                digest = _body_hash(body)
                cursor = db.execute("INSERT OR IGNORE INTO chunks(digest,body,payload) VALUES(?,?,?)",
                                    (digest, body, _json(chunk)))
                if cursor.rowcount:
                    rowid = cursor.lastrowid
                    db.execute("INSERT INTO search(rowid,body) VALUES(?,?)", (rowid, body))
                    count += 1
                    by_collection[str(chunk.get("collection"))] += 1
                else:
                    rowid = db.execute("SELECT id FROM chunks WHERE digest=?", (digest,)).fetchone()[0]
                source = {k: v for k, v in chunk.items() if k not in {"texto", "text"}}
                uid = _digest(_json([digest, original_id, chunk.get("collection"),
                                     chunk.get("document_id"), chunk.get("source_file")]))
                position = chunk.get("word_offset")
                if not isinstance(position, int):
                    match = re.search(r":w(\d+)(?::|$)", original_id)
                    position = int(match[1]) if match else -1
                doc = _json([chunk.get("collection"), chunk.get("document_id")])
                result = db.execute("INSERT OR IGNORE INTO sources VALUES(?,?,?,?,?,?,?)",
                                    (rowid, uid, original_id, doc, position,
                                     int(_known_boundaries(chunk)), _json(source)))
                source_count += result.rowcount
            if not count:
                raise ValueError("As fontes informadas não contêm trechos originais válidos")
            db.execute("INSERT INTO metadata VALUES('fingerprint',?)", (fingerprint,))
            db.execute("INSERT INTO search(search) VALUES('optimize')")
            db.commit()
            info = {"version": _VERSION, "fingerprint": fingerprint, "signature": fingerprint,
                    "engine": _ENGINE, "chunks": count, "source_records": source_count,
                    "invalid_chunks_skipped": invalid, "collections": dict(by_collection),
                    "coverage": coverage, "cobertura": coverage, "complete_corpus": complete,
                    "corpus_bruto_completo": complete, "sources": files,
                    "index_path": str(self.path),
                    "warnings": ([] if complete else [
                        "Cobertura parcial: somente trechos originais de seleções salvas; ausência de resultados não demonstra ausência no corpus completo."]),
                    "neighbors": "same_document_known_boundaries_only"}
        except BaseException:
            db.close()
            temporary.unlink(missing_ok=True)
            raise
        db.close()
        temporary.replace(self.path)
        with tempfile.NamedTemporaryFile(mode="w", encoding="utf-8", prefix="indice-", suffix=".json", dir=snapshot_directory, delete=False) as stream:
            stream.write(json.dumps(info, ensure_ascii=False, indent=2) + "\n")
            temporary_info = Path(stream.name)
        temporary_info.replace(info_path)
        self.info = info
        return self.info

    @staticmethod
    def _hydrate(db, row):
        result = json.loads(row[2])
        provenance = [json.loads(item[0]) for item in db.execute(
            "SELECT payload FROM sources WHERE chunk=? ORDER BY uid", (row[0],))]
        result.update(content_hash=row[1], provenance=provenance,
                      chunk_id_aliases=sorted({item["chunk_id"] for item in provenance}))
        return result

    def _neighbors(self, db, primary, exclude):
        found, seen = [], {primary["content_hash"]}
        for source in db.execute("SELECT doc,pos,payload FROM sources WHERE chunk=? AND known=1 AND pos>=0",
                                 (primary["_rowid"],)).fetchall():
            anchor = json.loads(source[2])
            for row in db.execute("""SELECT c.id,c.digest,c.payload,s.payload FROM sources s
                JOIN chunks c ON c.id=s.chunk WHERE s.doc=? AND s.known=1 AND s.pos>=0
                AND s.pos BETWEEN ? AND ? AND c.id!=? ORDER BY s.pos LIMIT 6""",
                                  (source[0], source[1] - _CHUNK_WORDS, source[1] + _CHUNK_WORDS,
                                   primary["_rowid"])):
                if row[1] in seen:
                    continue
                seen.add(row[1])
                adjacent = json.loads(row[3])
                a_start, a_end = anchor.get("page_ini"), anchor.get("page_fim", anchor.get("page_ini"))
                b_start, b_end = adjacent.get("page_ini"), adjacent.get("page_fim", adjacent.get("page_ini"))
                if all(isinstance(page, int) for page in (a_start, a_end, b_start, b_end)):
                    if a_start > b_end + 1 or b_start > a_end + 1:
                        continue
                result = self._hydrate(db, row)
                if exclude.intersection([result["content_hash"], *result["chunk_id_aliases"]]):
                    continue
                result["retrieval"] = {"engine": _ENGINE, "kind": "neighbor_context",
                                       "anchor_chunk_id": primary["chunk_id"]}
                found.append(result)
        return found[:2]

    def search(self, query, limit=8, exclude=(), neighbors=False):
        if not isinstance(query, str):
            raise TypeError("A consulta deve ser texto")
        if not isinstance(limit, int) or isinstance(limit, bool) or limit < 0:
            raise ValueError("limit deve ser um inteiro não negativo")
        if self.info is None:
            self.build()
        started = time.monotonic()
        terms = list(dict.fromkeys(word.casefold() for word in re.findall(r"[^\W_]+", query)
                                   if word.casefold() not in _STOP))[:40]
        expression = " OR ".join('"' + term.replace('"', '""') + '"' for term in terms)
        excluded = set(exclude)
        trace = {"query": query, "engine": _ENGINE, "match_expression": expression,
                 "limit": limit, "excluded": len(excluded), "coverage": self.info["coverage"],
                 "fingerprint": self.info["fingerprint"], "chunk_ids": []}
        results = []
        if expression and limit:
            with closing(sqlite3.connect(self.path.as_uri() + "?mode=ro", uri=True)) as db:
                cursor = db.execute("""SELECT c.id,c.digest,c.payload,bm25(search) AS score
                    FROM search JOIN chunks c ON c.id=search.rowid
                    WHERE search MATCH ? ORDER BY score,c.id""", (expression,))
                for row in cursor:
                    result = self._hydrate(db, row)
                    if excluded.intersection([result["content_hash"], *result["chunk_id_aliases"]]):
                        continue
                    result["retrieval"] = {"engine": _ENGINE, "kind": "bm25", "score": row[3], "query": query}
                    if neighbors:
                        result["_rowid"] = row[0]
                        result["neighbor_chunks"] = self._neighbors(db, result, excluded)
                        del result["_rowid"]
                    results.append(result)
                    if len(results) == limit:
                        break
        trace.update(chunk_ids=[row["chunk_id"] for row in results],
                     duration_seconds=round(time.monotonic() - started, 6))
        self.last_query_trace = trace
        return results

    def iter_records(self, batch_size=256):
        """Streaming de textos únicos; IDs internos ligam FAISS ao mesmo snapshot."""
        if self.info is None:
            raise ValueError("Construa o índice lexical antes de iterar")
        with closing(sqlite3.connect(self.path.as_uri() + "?mode=ro", uri=True)) as db:
            cursor = db.execute("SELECT id,body FROM chunks ORDER BY id")
            while rows := cursor.fetchmany(batch_size):
                yield rows

    def fetch_ids(self, identifiers, exclude=(), neighbors=False):
        """Hidrata resultados vetoriais com a mesma proveniência do BM25."""
        result, excluded = [], set(exclude)
        with closing(sqlite3.connect(self.path.as_uri() + "?mode=ro", uri=True)) as db:
            for identifier in identifiers:
                row = db.execute("SELECT id,digest,payload FROM chunks WHERE id=?", (int(identifier),)).fetchone()
                if row is None:
                    raise ValueError("ID vetorial não pertence ao snapshot lexical")
                chunk = self._hydrate(db, row)
                if excluded.intersection([chunk["content_hash"], *chunk["chunk_id_aliases"]]):
                    continue
                if neighbors:
                    chunk["_rowid"] = row[0]
                    chunk["neighbor_chunks"] = self._neighbors(db, chunk, excluded)
                    del chunk["_rowid"]
                result.append(chunk)
        return result
