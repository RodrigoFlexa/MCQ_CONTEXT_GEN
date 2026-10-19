"""Functional retrieval tests with temporary source documents; no network/model."""
import hashlib
import json
import sqlite3
import tempfile
import unittest
from contextlib import closing
from pathlib import Path

from pipeline.qa_research.corpus import CorpusIndex


class CorpusTests(unittest.TestCase):
    def setUp(self):
        # Keep fixtures inside the authorized workspace on Windows sandboxes.
        self.temporary = tempfile.TemporaryDirectory(dir=Path(__file__).parent)
        self.root = Path(self.temporary.name)
        self.origin = self.root / "sources"
        self.origin.mkdir()
        self.directory = self.root / "index"

    def tearDown(self):
        self.temporary.cleanup()

    @staticmethod
    def chunk(text, cid="regis:study:p1:w0", **metadata):
        return {"chunk_id": cid, "texto": text, "collection": "regis",
                "document_id": "study", "title": "Estudo científico", "page_ini": 1,
                "page_fim": 1, "language": "pt", **metadata}

    def selection(self, chunks, name="subtopicos/chemistry/selecao.json"):
        path = self.origin / name
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(json.dumps({"assuntos": {"a01": {"trechos": chunks}}}, ensure_ascii=False), encoding="utf-8")
        return path

    def index(self):
        return CorpusIndex(self.directory, origins=[self.origin])

    def test_original_metadata_and_query_trace_survive_retrieval(self):
        text = "A concentração de oxigênio foi medida no ensaio de desaeração."
        self.selection([self.chunk(text, url="https://example.test/paper", jurisdiction="BR")])
        index = self.index()
        info = index.build()
        result = index.search("desaeracao oxygen")[0]
        self.assertEqual(result["texto"], text)
        self.assertEqual(result["chunk_id"], "regis:study:p1:w0")
        self.assertEqual(result["url"], "https://example.test/paper")
        self.assertEqual(result["source_kind"], "saved_selection")
        self.assertFalse(info["corpus_bruto_completo"])
        self.assertEqual(info["cobertura"], "saved_selections_partial")
        self.assertIn("parcial", info["warnings"][0])
        self.assertEqual(index.last_query_trace["chunk_ids"], [result["chunk_id"]])
        self.assertEqual(index.last_query_trace["engine"], "SQLite FTS5 BM25")

    def test_content_dedup_preserves_source_aliases_and_case(self):
        self.selection([self.chunk("MEG retarda hidratos.")])
        self.selection([self.chunk("MEG   retarda hidratos.\n", "anp:other:p2:w0", collection="anp", document_id="other")],
                       "subtopicos/other/selecao.json")
        index = self.index()
        self.assertEqual(index.build()["chunks"], 1)
        result = index.search("hidratos")[0]
        self.assertEqual(len(result["chunk_id_aliases"]), 2)
        self.assertEqual(len(result["provenance"]), 2)
        self.assertEqual(index.search("hidratos", exclude=["regis:study:p1:w0"]), [])
        self.assertEqual(index.search("hidratos", exclude=[result["content_hash"]]), [])

    def test_chemical_case_differences_are_not_deduplicated(self):
        self.selection([self.chunk("NO é um composto.", "regis:study:p1:w0"),
                        self.chunk("No é um composto.", "regis:study:p1:w250")])
        self.assertEqual(self.index().build()["chunks"], 2)

    def test_generated_outputs_are_never_discovered(self):
        self.selection([self.chunk("Desaeração física remove oxigênio.")])
        for name in ("documento.md", "notas.jsonl", "fatos.jsonl", "trechos.jsonl"):
            (self.origin / name).write_text("SegredoInventadoExisteAqui", encoding="utf-8")
        index = self.index()
        self.assertEqual(index.build()["chunks"], 1)
        self.assertEqual(index.search("SegredoInventadoExisteAqui"), [])

    def test_explicit_generated_rows_are_rejected_even_inside_selection(self):
        self.selection([self.chunk("Evidência fonte.", "regis:study:p1:w0"),
                        self.chunk("TextoFabricado", "regis:study:p1:w250", source_kind="generated")])
        index = self.index()
        self.assertEqual(index.build()["chunks"], 1)
        self.assertEqual(index.search("TextoFabricado"), [])

    def test_fingerprint_invalidates_cache_when_source_content_changes(self):
        path = self.selection([self.chunk("Biocida composto alfa.")])
        index = self.index()
        old = index.build()
        self.assertEqual(index.build()["fingerprint"], old["fingerprint"])
        self.selection([self.chunk("Biocida composto beta.")])
        updated = index.build()
        self.assertNotEqual(old["fingerprint"], updated["fingerprint"])
        self.assertEqual(index.search("alfa"), [])
        self.assertEqual(index.search("beta")[0]["source_file"], str(path.resolve()))

    def test_saved_selection_path_itself_is_an_allowed_origin(self):
        path = self.selection([self.chunk("Monitoramento de corrosão.")])
        index = CorpusIndex(self.directory, origins=[path])
        self.assertEqual(index.build()["chunks"], 1)
        (self.origin / "fake.json").write_text("{}", encoding="utf-8")
        with self.assertRaisesRegex(ValueError, "somente"):
            CorpusIndex(self.directory, origins=[self.origin / "fake.json"]).build()

    def test_no_fallback_sources_is_an_explicit_error(self):
        with self.assertRaisesRegex(ValueError, "Nenhum selecao"):
            self.index().build()

    def test_malformed_selection_is_an_explicit_error(self):
        path = self.selection([])
        path.write_text('{"notas": []}', encoding="utf-8")
        with self.assertRaisesRegex(ValueError, "assuntos"):
            self.index().build()

    def test_neighbor_context_stays_in_known_document_and_within_limit(self):
        self.selection([self.chunk("Oxigênio dissolvido.", "regis:study:p1:w0"),
                        self.chunk("Desaeração física.", "regis:study:p1:w250"),
                        self.chunk("Nunca anexar documento vizinho.", "regis:other:p1:w250", document_id="other")])
        index = self.index()
        results = index.search("oxigênio", limit=1, neighbors=True)
        self.assertEqual(len(results), 1)
        self.assertEqual(len(results[0]["neighbor_chunks"]), 1)
        self.assertEqual(results[0]["neighbor_chunks"][0]["texto"], "Desaeração física.")
        self.assertEqual(results[0]["neighbor_chunks"][0]["retrieval"]["kind"], "neighbor_context")

    def test_unknown_concatenated_boundaries_never_get_neighbors(self):
        metadata = {"source_boundary": "original_concatenated_txt; document boundaries unknown"}
        self.selection([self.chunk("Oxigênio dissolvido.", "regis:study:p1:w0", **metadata),
                        self.chunk("Este texto pode ser outra tese.", "regis:study:p1:w250", **metadata)])
        results = self.index().search("oxigênio", limit=1, neighbors=True)
        self.assertEqual(results[0]["neighbor_chunks"], [])

    def test_neighbor_does_not_jump_missing_pages(self):
        self.selection([self.chunk("Oxigênio dissolvido.", "regis:study:p1:w0"),
                        self.chunk("Página perdida entre os trechos.", "regis:study:p10:w250", page_ini=10, page_fim=10)])
        results = self.index().search("oxigênio", limit=1, neighbors=True)
        self.assertEqual(results[0]["neighbor_chunks"], [])

    def test_exclusion_applies_to_neighbor_context(self):
        self.selection([self.chunk("Oxigênio dissolvido.", "regis:study:p1:w0"),
                        self.chunk("Desaeração física.", "regis:study:p1:w250")])
        results = self.index().search("oxigênio", limit=1, neighbors=True, exclude=["regis:study:p1:w250"])
        self.assertEqual(results[0]["neighbor_chunks"], [])

    def test_empty_and_unsafe_query_syntax_are_harmless(self):
        self.selection([self.chunk("Inibidor de incrustação.")])
        index = self.index()
        self.assertEqual(index.search(""), [])
        self.assertEqual(index.search("e de para the"), [])
        self.assertEqual(index.search('" OR * NOT : - ; DROP TABLE chunks;'), [])
        self.assertEqual(len(index.search("incrustação")), 1)
        self.assertEqual(index.search("incrustação", limit=0), [])
        with self.assertRaises(ValueError):
            index.search("incrustação", limit=-1)

    def test_cache_database_signature_is_verified(self):
        self.selection([self.chunk("Corrosão monitorada.")])
        index = self.index()
        fingerprint = index.build()["fingerprint"]
        with closing(sqlite3.connect(index.path)) as db:
            db.execute("UPDATE metadata SET value='wrong'")
            db.commit()
        rebuilt = self.index()
        self.assertEqual(rebuilt.build()["fingerprint"], fingerprint)
        with closing(sqlite3.connect(index.path)) as db:
            self.assertEqual(db.execute("SELECT value FROM metadata").fetchone()[0], fingerprint)

    def test_shared_cache_root_cannot_replace_another_corpus_snapshot(self):
        first_path = self.selection([self.chunk("Evidência exclusiva Alfa")], "first/selecao.json")
        second_path = self.selection([self.chunk("Evidência exclusiva Beta")], "second/selecao.json")
        first = CorpusIndex(self.directory, origins=[first_path])
        second = CorpusIndex(self.directory, origins=[second_path])
        first.build()
        snapshot = first.path
        second.build()
        self.assertNotEqual(first.path, second.path)
        self.assertEqual(first.path, snapshot)
        self.assertTrue(snapshot.is_file())
        self.assertEqual(len(first.search("Alfa")), 1)
        self.assertEqual(first.search("Beta"), [])
        self.assertEqual(len(second.search("Beta")), 1)

    def make_manifest(self):
        root = self.root / "full_corpus"
        root.mkdir()
        collections = []
        for collection in ("petroles", "anp", "hse", "bsee", "regis"):
            path = root / (collection + (".txt" if collection == "petroles" else ".jsonl"))
            if collection == "petroles":
                path.write_text("Sequestrante remove oxigênio em água.\n", encoding="utf-8")
                item = {"id": collection, "format": "petroles_txt", "documents": 1,
                        "files": [{"path": path.name, "sha256": hashlib.sha256(path.read_bytes()).hexdigest()}]}
            else:
                row = {"collection": collection, "document_id": collection + "-study", "page": 1,
                       "title": "Thesis retained " + collection, "text": "Evidência científica " + collection,
                       "language": "en"}
                path.write_text(json.dumps(row) + "\n", encoding="utf-8")
                item = {"id": collection, "format": "pages_jsonl", "documents": 1,
                        "path": path.name, "sha256": hashlib.sha256(path.read_bytes()).hexdigest()}
            collections.append(item)
        manifest = root / "manifest.json"
        manifest.write_text(json.dumps({"schema": "petroquest-domain-corpora-v1", "ready": True,
                                        "sample": False, "collections": collections}), encoding="utf-8")
        return manifest

    def test_verified_manifest_takes_priority_and_keeps_theses(self):
        manifest = self.make_manifest()
        self.selection([self.chunk("OldSelectionOnly")])
        index = CorpusIndex(self.directory, origins=[self.origin], manifest=manifest)
        info = index.build()
        self.assertTrue(info["corpus_bruto_completo"])
        self.assertEqual(info["coverage"], "verified_manifest")
        self.assertEqual(info["chunks"], 5)
        self.assertEqual(index.search("OldSelectionOnly"), [])
        result = index.search("regis")[0]
        self.assertEqual(result["collection"], "regis")
        self.assertEqual(result["source_kind"], "verified_manifest")
        self.assertEqual(result["title"], "Thesis retained regis")
        self.assertEqual(result["chunk_id"], "regis:regis-study:p1:w0")
        self.assertEqual(result["source_boundary"], "known_document")
        petroles = index.search("sequestrante")[0]
        self.assertIn("unknown", petroles["source_boundary"])
        self.assertTrue(Path(petroles["source_file"]).is_file())

    def test_manifest_hash_is_reverified_before_using_existing_index(self):
        manifest = self.make_manifest()
        index = CorpusIndex(self.directory, manifest=manifest)
        index.build()
        (manifest.parent / "regis.jsonl").write_text("Corrupted raw corpus", encoding="utf-8")
        with self.assertRaisesRegex(ValueError, "modificado ou corrompido"):
            index.build()

    def test_manifest_windows_preserve_overlap_pages_and_document_boundaries(self):
        manifest = self.make_manifest()
        path = manifest.parent / "regis.jsonl"
        rows = [
            {"collection": "regis", "document_id": "long", "title": "Long thesis", "page": 1,
             "text": " ".join("word" + str(i) for i in range(350))},
            {"collection": "regis", "document_id": "long", "title": "Long thesis", "page": 2,
             "text": " ".join("word" + str(i) for i in range(350, 650))},
            {"collection": "regis", "document_id": "short", "title": "Short paper", "page": 1,
             "text": "Separately retained evidence."},
        ]
        path.write_text("\n".join(json.dumps(row) for row in rows) + "\n", encoding="utf-8")
        data = json.loads(manifest.read_text(encoding="utf-8"))
        item = next(item for item in data["collections"] if item["id"] == "regis")
        item["documents"] = 2
        item["sha256"] = hashlib.sha256(path.read_bytes()).hexdigest()
        manifest.write_text(json.dumps(data), encoding="utf-8")
        index = CorpusIndex(self.directory, manifest=manifest)
        self.assertEqual(index.build()["chunks"], 8)
        with closing(sqlite3.connect(index.path)) as db:
            chunks = [json.loads(row[0]) for row in db.execute("SELECT payload FROM chunks")]
        long = sorted((row for row in chunks if row["document_id"] == "long"), key=lambda row: row["word_offset"])
        self.assertEqual([row["word_offset"] for row in long], [0, 250, 500])
        self.assertEqual([len(row["texto"].split()) for row in long], [350, 350, 150])
        self.assertEqual((long[1]["page_ini"], long[1]["page_fim"]), (1, 2))
        self.assertTrue(long[2]["texto"].endswith("word649"))
        short = next(row for row in chunks if row["document_id"] == "short")
        self.assertEqual(short["texto"], "Separately retained evidence.")
        self.assertEqual(short["word_offset"], 0)

    def test_sample_manifest_is_not_silently_treated_as_complete(self):
        manifest = self.make_manifest()
        data = json.loads(manifest.read_text(encoding="utf-8"))
        data["sample"] = True
        manifest.write_text(json.dumps(data), encoding="utf-8")
        with self.assertRaisesRegex(ValueError, "amostra"):
            CorpusIndex(self.directory, manifest=manifest).build()


if __name__ == "__main__":
    unittest.main()
