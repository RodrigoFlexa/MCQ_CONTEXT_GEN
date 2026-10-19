"""Triagem opcional por tópico; exclusão é seleção operacional, não juízo factual."""
import heapq
import json
import os
import sqlite3
import tempfile
from collections import Counter
from contextlib import closing
from pathlib import Path

import numpy as np

from pipeline.inventario.locking import output_lock
from pipeline.inventario.textutil import atomic_json, read_json, sha
from .corpus import CorpusIndex

LOCAL_MODEL = "intfloat/multilingual-e5-small"
LOCAL_REVISION = "614241f622f53c4eeff9890bdc4f31cfecc418b3"


def validate_profile(profile, topic):
    if not isinstance(profile, dict):
        raise ValueError("Perfil de triagem deve ser um objeto JSON")
    if profile.get("topic") != topic:
        raise ValueError("Perfil de triagem pertence a outro tópico/escopo")
    queries = profile.get("queries")
    if (not isinstance(queries, list) or not queries or
            any(not isinstance(q, str) or not q.strip() for q in queries) or
            len(set(queries)) != len(queries)):
        raise ValueError("Perfil deve conter consultas distintas e não vazias")
    for key in ("lexical_per_query", "semantic_per_query"):
        if type(profile.get(key)) is not int or profile[key] < 1:
            raise ValueError(f"{key} deve ser inteiro positivo")
    if profile.get("context") != "whole_known_document":
        raise ValueError("Preserve whole_known_document; fronteiras desconhecidas não serão inventadas")


class LocalE5:
    """Somente triagem. Janelas de 400 tokens evitam descartar caudas dos trechos.

    Cache por conteúdo/modelo, separado do Azure; pontuação usa a melhor janela
    para cada consulta, sem misturar os dois espaços vetoriais.
    """
    def __init__(self, directory, offline=True, threads=4, device="cpu"):
        import torch
        from sentence_transformers import SentenceTransformer
        torch.set_num_threads(threads)
        self.model = SentenceTransformer(LOCAL_MODEL, revision=LOCAL_REVISION,
            local_files_only=offline, device=device, trust_remote_code=False)
        self.model.max_seq_length = 512
        self.protocol = {"model": LOCAL_MODEL, "revision": LOCAL_REVISION,
                         "window_tokens": 400, "stride_tokens": 320,
                         "pooling": "max_query_window_similarity", "normalized": True,
                         "query_prefix": "query: ", "passage_prefix": "passage: ",
                         "sentence_transformers": __import__("sentence_transformers").__version__}
        root = Path(directory) / "local-selection" / sha(json.dumps(self.protocol, sort_keys=True), 40)
        root.mkdir(parents=True, exist_ok=True)
        self.db = sqlite3.connect(root / "windows.sqlite3", timeout=60)
        self.db.execute("PRAGMA journal_mode=WAL")
        self.db.execute("CREATE TABLE IF NOT EXISTS windows(digest TEXT PRIMARY KEY, n INTEGER, matrix BLOB)")
        self.db.commit()

    def _encode(self, texts):
        vectors = np.asarray(self.model.encode(texts, batch_size=16, normalize_embeddings=True,
                             convert_to_numpy=True, show_progress_bar=False), dtype=np.float32)
        if vectors.ndim != 2 or vectors.shape[1] != 384 or not np.isfinite(vectors).all():
            raise ValueError("Resposta local E5 inválida")
        return vectors

    def queries(self, queries):
        texts = ["query: " + q for q in queries]
        if any(len(self.model.tokenizer.encode(t)) > 512 for t in texts):
            raise ValueError("Consulta de triagem excede 512 tokens; divida-a")
        return self._encode(texts)

    def _windows(self, text):
        tokenizer = self.model.tokenizer
        tokens = tokenizer.encode(text, add_special_tokens=False, truncation=False, verbose=False)
        windows = []
        for start in range(0, len(tokens), 320):
            passage = "passage: " + tokenizer.decode(tokens[start:start + 400], skip_special_tokens=True)
            if len(tokenizer.encode(passage)) > 512:
                raise ValueError("Janela local excedeu limite; não será truncada silenciosamente")
            windows.append(passage)
            if start + 400 >= len(tokens):
                break
        if not windows:
            raise ValueError("Trecho sem tokens")
        return windows

    def passages_many(self, texts):
        results, pending, windows = [], [], []
        for text in texts:
            digest = sha(text, 64)
            row = self.db.execute("SELECT n,matrix FROM windows WHERE digest=?", (digest,)).fetchone()
            if row:
                vectors = np.frombuffer(row[1], dtype=np.float32).reshape(row[0], 384)
                if row[0] < 1 or not np.isfinite(vectors).all():
                    raise ValueError("Cache local de triagem inválido")
                results.append(vectors)
            else:
                items = self._windows(text)
                pending.append((len(results), digest, len(windows), len(items)))
                windows.extend(items)
                results.append(None)
        if windows:
            encoded = self._encode(windows)
            for position, digest, start, size in pending:
                matrix = encoded[start:start + size]
                self.db.execute("INSERT OR IGNORE INTO windows VALUES(?,?,?)", (digest, size, matrix.tobytes()))
                results[position] = matrix
        return results

    def passages(self, text):
        return self.passages_many([text])[0]

    def flush(self):
        self.db.commit()

    def close(self):
        self.flush()
        self.db.close()


def select_topic(index, profile, topic, semantic=None, progress=print):
    validate_profile(profile, topic)
    queries = profile["queries"]
    reasons, queries_report = {}, []
    with closing(sqlite3.connect(index.path.as_uri() + "?mode=ro", uri=True)) as db:
        for qi, query in enumerate(queries):
            rows = index.search(query, limit=profile["lexical_per_query"])
            queries_report.append({"query": query, "lexical": len(rows), "semantic": 0})
            for rank, row in enumerate(rows, 1):
                identifier = db.execute("SELECT id FROM chunks WHERE digest=?", (row["content_hash"],)).fetchone()[0]
                reasons.setdefault(identifier, []).append({"query": qi, "channel": "lexical", "rank": rank})
    if semantic:
        vectors = semantic.queries(queries)
        heaps = [[] for _ in queries]
        k, count = profile["semantic_per_query"], 0
        for rows in index.iter_records(batch_size=32):
            matrices = (semantic.passages_many([text for _, text in rows])
                        if hasattr(semantic, "passages_many") else [semantic.passages(text) for _, text in rows])
            for (identifier, _), matrix in zip(rows, matrices):
                scores = (vectors @ matrix.T).max(axis=1)
                for qi, score in enumerate(scores):
                    entry = (float(score), -identifier)
                    if len(heaps[qi]) < k:
                        heapq.heappush(heaps[qi], entry)
                    elif entry > heaps[qi][0]:
                        heapq.heapreplace(heaps[qi], entry)
            count += len(rows)
            if hasattr(semantic, "flush"):
                semantic.flush()
            progress(f"Triagem semântica local: {count}/{index.info['chunks']} trechos (cache incremental)")
        for qi, heap in enumerate(heaps):
            queries_report[qi]["semantic"] = len(heap)
            for rank, (score, negative_id) in enumerate(sorted(heap, reverse=True), 1):
                reasons.setdefault(-negative_id, []).append(
                    {"query": qi, "channel": "local_semantic", "rank": rank, "score": score})
    if not reasons:
        raise ValueError("Nenhum trecho selecionado; amplie/revise o perfil de triagem")
    signature = sha(json.dumps({"version": "topic-selection-v1", "corpus": index.info["signature"],
        "profile": profile, "semantic": semantic.protocol if semantic else None,
        "selected_seeds": sorted(reasons)}, ensure_ascii=False, sort_keys=True), 64)
    return reasons, {"signature": signature, "source_signature": index.info["signature"],
        "profile": profile, "queries": queries_report, "semantic": semantic.protocol if semantic else None,
        "recall_validated": False, "warning": "Triagem pode omitir evidências pertinentes. Não demonstra exaustividade nem irrelevância dos excluídos."}


def materialize_selection(index, reasons, report, directory):
    root = Path(directory) / "topic-subsets" / report["signature"]
    with output_lock(root):
        info = read_json(root / "indice.json")
        if info and (root / "corpus.sqlite3").is_file():
            subset = CorpusIndex(root)
            subset.path, subset.info = root / "corpus.sqlite3", info
            return subset, [root / "selection.json", root / "selection.jsonl"]
        with tempfile.NamedTemporaryFile(dir=root, suffix=".sqlite3", delete=False) as stream:
            temporary = Path(stream.name)
        try:
            with closing(sqlite3.connect(temporary.as_uri(), uri=True)) as db:
                db.execute("ATTACH DATABASE ? AS original", (index.path.as_uri() + "?mode=ro",))
                db.execute("CREATE TEMP TABLE keep(id INTEGER PRIMARY KEY)")
                db.executemany("INSERT INTO keep VALUES(?)", [(i,) for i in sorted(reasons)])
                # Conserva documentos conhecidos inteiros (também fontes de
                # contraevidência), sem confundir um TXT concatenado com um livro.
                db.execute("""INSERT OR IGNORE INTO keep SELECT s.chunk FROM original.sources s
                    WHERE s.known=1 AND s.doc IN (SELECT t.doc FROM original.sources t
                    JOIN keep k ON k.id=t.chunk WHERE t.known=1)""")
                for table in ("metadata", "chunks", "sources"):
                    sql = db.execute("SELECT sql FROM original.sqlite_master WHERE name=?", (table,)).fetchone()[0]
                    db.execute(sql)
                db.execute("INSERT INTO chunks SELECT c.* FROM original.chunks c JOIN keep k ON k.id=c.id")
                db.execute("INSERT INTO sources SELECT s.* FROM original.sources s JOIN keep k ON k.id=s.chunk")
                db.executescript("""CREATE INDEX original_ids ON sources(original_id);
                    CREATE INDEX positions ON sources(doc,pos); CREATE INDEX source_chunks ON sources(chunk);
                    CREATE VIRTUAL TABLE search USING fts5(body,content='chunks',content_rowid='id',
                        tokenize='unicode61 remove_diacritics 2');
                    INSERT INTO search(rowid,body) SELECT id,body FROM chunks;
                    INSERT INTO search(search) VALUES('optimize');""")
                db.execute("INSERT INTO metadata VALUES('fingerprint',?)", (report["signature"],))
                count = db.execute("SELECT count(*) FROM chunks").fetchone()[0]
                collections = Counter(str(json.loads(row[0]).get("collection")) for row in db.execute("SELECT payload FROM chunks"))
                report = {**report, "total_chunks": index.info["chunks"], "seed_chunks": len(reasons),
                          "selected_chunks": count, "excluded_chunks": index.info["chunks"] - count,
                          "retained_fraction": count / index.info["chunks"], "collections": dict(collections)}
                info = {**index.info, "fingerprint": report["signature"], "signature": report["signature"],
                        "chunks": count, "source_records": db.execute("SELECT count(*) FROM sources").fetchone()[0],
                        "collections": dict(collections), "coverage": "topic_subset_partial",
                        "cobertura": "topic_subset_partial", "complete_corpus": False, "corpus_bruto_completo": False,
                        "index_path": str(root / "corpus.sqlite3"), "topic_selection": report,
                        "warnings": [*index.info.get("warnings", []), report["warning"]]}
                with (root / "selection.jsonl").open("w", encoding="utf-8") as stream:
                    for identifier, digest, payload, kept in db.execute("""SELECT c.id,c.digest,c.payload,k.id
                            FROM original.chunks c LEFT JOIN keep k ON k.id=c.id ORDER BY c.id"""):
                        chunk = json.loads(payload)
                        stream.write(json.dumps({"id": identifier, "content_hash": digest,
                            "chunk_id": chunk["chunk_id"], "collection": chunk.get("collection"),
                            "document_id": chunk.get("document_id"), "selected": kept is not None,
                            "reasons": reasons.get(identifier, [{"channel": "whole_known_document"}]
                                if kept else [{"channel": "not_selected_by_profile"}])}, ensure_ascii=False) + "\n")
                db.commit()
            os.replace(temporary, root / "corpus.sqlite3")
            atomic_json(root / "selection.json", report)
            atomic_json(root / "indice.json", info)
        finally:
            temporary.unlink(missing_ok=True)
    subset = CorpusIndex(root)
    subset.path, subset.info = root / "corpus.sqlite3", info
    return subset, [root / "selection.json", root / "selection.jsonl"]
