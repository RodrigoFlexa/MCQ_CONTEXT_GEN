"""Transferência real de SQLite/FAISS; sem Azure nem download de modelo."""
import json
import os
import shutil
import sqlite3
import unittest
from dataclasses import replace
from pathlib import Path
from unittest.mock import patch

import numpy as np

from pipeline.qa_research.corpus import CorpusIndex, _file_hash
from pipeline.qa_research.hybrid import HybridCorpusIndex
from pipeline.qa_research.portable import PreparedCorpusIndex, verify_pack, write_pack, _publish
from pipeline.qa_research.prepare import prepare
from pipeline.qa_research.run import execute
from pipeline.qa_research.selection import LocalE5, materialize_selection, select_topic
import test_hybrid as fixtures


class SemanticFixture:
    protocol = {"model": "fixture-not-a-real-model"}

    def queries(self, queries):
        return np.asarray([[1., 0.] for _ in queries])

    def passages(self, text):
        return np.asarray([[1., 0.] if "Oxigênio" in text else [0., 1.]])


class PortableTests(unittest.TestCase):
    setUp = fixtures.HybridTests.setUp
    tearDown = fixtures.HybridTests.tearDown

    def pack(self, hybrid=True, name="pack"):
        if hybrid:
            self.hybrid.build()
        target = self.root / name
        write_pack(self.lexical, target, self.hybrid.vector if hybrid else None)
        return target

    def test_transfer_runs_without_originals_or_document_embedding_cache(self):
        target = self.pack()
        moved = self.root / "server" / "topic"
        moved.parent.mkdir()
        shutil.move(str(target), moved)
        self.origin.rename(self.root / "originals-offline")
        self.lexical.path.rename(self.lexical.path.with_suffix(".offline"))
        with patch.object(CorpusIndex, "build", side_effect=AssertionError("must not rebuild")), \
                patch.object(CorpusIndex, "iter_records", side_effect=AssertionError("must not embed corpus")):
            index = PreparedCorpusIndex(moved, self.root / "server-cache")
            hybrid = HybridCorpusIndex(self.config, index, self.embedder, fixtures.Reranker())
            before = len(self.api.calls)
            hybrid.build()
            self.assertEqual(len(self.api.calls), before)
            answer = hybrid.search("oxygen scavenger", limit=1)[0]
            self.assertIn("Oxigênio", answer["texto"])
            self.assertIn("provenance", answer)
            self.assertEqual(len(self.api.calls), before + 1)  # somente a consulta

    def test_run_pack_stage_index_never_embeds_documents(self):
        target = self.pack()
        config = replace(self.config, prepared_pack=str(target))
        before = len(self.api.calls)
        with patch("pipeline.qa_research.embeddings.AzureEmbedder", return_value=self.embedder), \
                patch("pipeline.qa_research.run.make_clients", side_effect=AssertionError("no chat for index")), \
                patch.object(CorpusIndex, "build", side_effect=AssertionError("must not rebuild")):
            result = execute(config, stage="indice", progress=lambda _: None)
        self.assertIsNone(result["interrupcao"])
        self.assertEqual(before, len(self.api.calls))
        # execute é proprietário do embedder; tearDown pode fechá-lo novamente.
        self.embedder.close = lambda: None

    def test_verified_pack_uses_stat_receipt_and_transfer_revalidates(self):
        target = self.pack()
        cache = self.root / "receipts"
        verify_pack(target, cache)
        with patch("pipeline.qa_research.portable._file_hash", side_effect=AssertionError("warm hash")):
            verify_pack(target, cache)
        moved = self.root / "other-host"
        shutil.copytree(target, moved)
        with patch("pipeline.qa_research.portable._file_hash", wraps=_file_hash) as hashes:
            verify_pack(moved, cache)
        self.assertEqual(hashes.call_count, 2)

    def test_changed_file_invalidates_receipt_and_fails_closed(self):
        target = self.pack()
        cache = self.root / "receipts"
        verify_pack(target, cache)
        path = target / "index.faiss"
        stat = path.stat()
        with path.open("r+b") as stream:
            stream.seek(-1, 2)
            stream.write(b"X")
        os.utime(path, ns=(stat.st_atime_ns, stat.st_mtime_ns + 1000000000))
        with self.assertRaisesRegex(ValueError, "Hash inválido"):
            verify_pack(target, cache)

    def test_same_count_wrong_vector_ids_are_rejected(self):
        import faiss
        target = self.pack()
        vector = faiss.IndexIDMap2(faiss.IndexFlatIP(3072))
        values = np.zeros((3, 3072), dtype=np.float32)
        values[:, 0] = 1
        vector.add_with_ids(values, np.asarray([10, 20, 30], dtype=np.int64))
        path = target / "index.faiss"
        faiss.write_index(vector, str(path))
        data = json.loads((target / "pack.json").read_text(encoding="utf-8"))
        data["files"]["index.faiss"] = {"bytes": path.stat().st_size, "sha256": _file_hash(path)}
        data["vector"]["sha256"] = _file_hash(path)
        (target / "pack.json").write_text(json.dumps(data), encoding="utf-8")
        with self.assertRaisesRegex(ValueError, "IDs FAISS"):
            verify_pack(target, self.root / "cache")

    def test_cloud_protocol_must_match_prepared_vectors(self):
        target = self.pack()
        index = PreparedCorpusIndex(target, self.root / "cache")
        self.embedder.protocol = {**self.embedder.protocol, "declared_model_version": "changed"}
        hybrid = HybridCorpusIndex(self.config, index, self.embedder, fixtures.Reranker())
        with self.assertRaisesRegex(ValueError, "Protocolo de consulta"):
            hybrid.build()

    def test_lexical_pack_cannot_silently_build_azure_on_server(self):
        target = self.pack(hybrid=False)
        index = PreparedCorpusIndex(target, self.root / "cache")
        hybrid = HybridCorpusIndex(self.config, index, self.embedder, fixtures.Reranker())
        with self.assertRaisesRegex(ValueError, "Finalize-o"):
            hybrid.build()
        self.assertEqual(self.api.calls, [])

    def test_explicit_preparation_finalizes_lexical_pack_without_raw_sources(self):
        source = self.pack(hybrid=False)
        self.origin.rename(self.root / "offline")
        destination = self.root / "final-pack"
        prepare(self.config, destination, source_pack=source,
                embedder_factory=lambda config, budget: self.embedder, progress=lambda _: None)
        self.embedder.close = lambda: None
        index = PreparedCorpusIndex(destination, self.root / "cache")
        self.assertIsNotNone(index.prepared_vector)
        self.assertEqual(index.info["chunks"], 3)

    def test_published_pack_is_immutable(self):
        target = self.pack(hybrid=False)
        with self.assertRaisesRegex(ValueError, "já existe"):
            write_pack(self.lexical, target)

    def test_windows_transient_publication_lock_retries_without_recopying(self):
        source, destination = self.root / "staging", self.root / "published"
        source.mkdir()
        error = PermissionError("transient Windows sharing lock")
        error.winerror = 32
        rename = os.rename
        attempts = []
        def transient(left, right):
            attempts.append(1)
            if len(attempts) < 3:
                raise error
            rename(left, right)
        with patch("pipeline.qa_research.portable.os.rename", side_effect=transient), \
                patch("pipeline.qa_research.portable.time.sleep"):
            _publish(source, destination)
        self.assertEqual(len(attempts), 3)
        self.assertTrue(destination.is_dir())
        with self.assertRaises(FileExistsError):
            _publish(source, destination)

    def test_identity_ignores_machine_specific_paths_only_in_pack_mode(self):
        left = replace(self.config, prepared_pack="C:/local/pack", origins=["C:/original"])
        right = replace(self.config, prepared_pack="/srv/pack", origins=["/absent"], index_dir="/srv/cache")
        self.assertEqual(left.identity(), right.identity())
        self.assertNotEqual(self.config.identity(), replace(self.config, index_dir="elsewhere").identity())

    def test_selection_preserves_known_document_and_original_provenance(self):
        path = self.origin / "selecao.json"
        data = json.loads(path.read_text(encoding="utf-8"))
        data["assuntos"]["a"]["trechos"].append({
            "chunk_id": "fixture:D0:p2:w250", "collection": "fixture", "document_id": "D0",
            "texto": "Condições e limitações do experimento original.", "page_ini": 2,
            "page_fim": 2, "word_offset": 250})
        path.write_text(json.dumps(data), encoding="utf-8")
        self.lexical = CorpusIndex(self.root / "lexical", [self.origin])
        self.lexical.build()
        profile = {"topic": self.config.topic, "queries": ["unmatched lexeme"],
                   "lexical_per_query": 1, "semantic_per_query": 1, "context": "whole_known_document"}
        reasons, report = select_topic(self.lexical, profile, self.config.topic, SemanticFixture())
        self.assertEqual(len(reasons), 1)
        subset, files = materialize_selection(self.lexical, reasons, report, self.root / "cache")
        self.assertEqual(subset.info["chunks"], 2)
        self.assertFalse(subset.info["complete_corpus"])
        self.assertFalse(subset.info["topic_selection"]["recall_validated"])
        rows = list(subset.iter_records())[0]
        self.assertEqual(len(subset.fetch_ids([i for i, _ in rows])), 2)
        selection = [json.loads(s) for s in files[1].read_text(encoding="utf-8").splitlines()]
        self.assertEqual(sum(s["selected"] for s in selection), 2)
        self.assertIn("whole_known_document", json.dumps(selection))
        pack = self.root / "selected-pack"
        write_pack(subset, pack, selection_files=files)
        self.assertEqual(PreparedCorpusIndex(pack, self.root / "receipt").info["chunks"], 2)

    def test_profile_cannot_be_reused_for_different_topic(self):
        profile = {"topic": {"titulo": "other"}, "queries": ["x"]}
        with self.assertRaisesRegex(ValueError, "outro tópico"):
            select_topic(self.lexical, profile, self.config.topic)

    def test_pack_manifest_rejects_path_escape(self):
        target = self.pack(hybrid=False)
        path = target / "pack.json"
        data = json.loads(path.read_text(encoding="utf-8"))
        data["files"]["../outside"] = {"bytes": 1, "sha256": "a" * 64}
        path.write_text(json.dumps(data), encoding="utf-8")
        with self.assertRaisesRegex(ValueError, "Lista de arquivos"):
            verify_pack(target, self.root / "cache")

    def test_ivfpq_pack_validates_ids_and_loads_after_transfer(self):
        import faiss
        from types import SimpleNamespace
        # A serialização de listas invertidas é diferente de IndexIDMap2.
        values = np.random.default_rng(42).normal(size=(300, 96)).astype(np.float32)
        vector = faiss.IndexIVFPQ(faiss.IndexFlatIP(96), 96, 1, 4, 4, faiss.METRIC_INNER_PRODUCT)
        vector.pq.cp.min_points_per_centroid = 1
        vector.train(values)
        vector.add_with_ids(values[:3], np.asarray([1, 2, 3], dtype=np.int64))
        directory = Path(self.config.index_dir) / "dense" / "fixture-compressed"
        directory.mkdir(parents=True)
        path = directory / "index.faiss"
        faiss.write_index(vector, str(path))
        info = {"signature": "fixture-compressed", "sha256": _file_hash(path), "chunks": 3,
                "dimensions": 96, "protocol": {"corpus": self.lexical.info["signature"]},
                "kind": "ivfpq_ip_approximate"}
        target = self.root / "compressed-pack"
        write_pack(self.lexical, target, SimpleNamespace(config=self.config, info=info))
        data, _ = verify_pack(target, self.root / "cache")
        self.assertEqual(data["vector"]["chunks"], 3)

    def test_existing_snapshot_can_be_exported_without_revisiting_raw_inputs(self):
        self.origin.rename(self.root / "offline")
        with patch.object(CorpusIndex, "build", side_effect=AssertionError("must not scan raw corpus")):
            result = prepare(self.config, self.root / "export", snapshot=self.lexical.path.parent,
                             lexical_only=True, progress=lambda _: None)
        self.assertEqual(result["chunks"], 3)

    def test_document_and_qa_run_from_prepared_pack_with_originals_offline(self):
        from pipeline.qa_research.tests.test_pipeline import FixtureModel, TEXT
        from pipeline.qa_research.hybrid import RERANK_PROMPT
        from pipeline.qa_research.config import ROLES
        from pipeline.qa_research.embeddings import AzureEmbedder
        from pipeline.qa_research.runtime import PersistentBudget
        row = {"chunk_id": "fixture:whole:p1:w0", "texto": TEXT,
               "collection": "fixture", "document_id": "whole", "page_ini": 1, "page_fim": 1}
        (self.origin / "selecao.json").write_text(
            json.dumps({"assuntos": {"a": {"trechos": [row]}}}), encoding="utf-8")
        self.lexical.build()
        self.hybrid.build()
        target = self.root / "research-pack"
        write_pack(self.lexical, target, self.hybrid.vector)
        self.origin.rename(self.root / "offline")
        class Model(FixtureModel):
            def close(self):
                pass

            def json(self, system, user, **kwargs):
                if system == RERANK_PROMPT:
                    result = {"avaliacoes": [{"id": c["id"], "score": 3, "motivo": "Teste"}
                              for c in json.loads(user)["candidatos"]]}
                    kwargs["validate"](result)
                    return result
                return super().json(system, user, **kwargs)
        model = Model()
        config = replace(self.config, prepared_pack=str(target), initial_facets=1, max_facets=1,
                         target_qa=1, max_repairs=0, index_dir=str(self.root / "fresh-server-cache"))
        # Cache Azure vazio no servidor: só novas consultas podem ser enviadas.
        api = fixtures.EmbeddingAPI()
        embedder = AzureEmbedder(config, PersistentBudget(self.root / "server-budget.json", 100),
                                 client=api, tokenizer=fixtures.Tokenizer())
        with patch("pipeline.qa_research.embeddings.AzureEmbedder", return_value=embedder), \
                patch("pipeline.qa_research.run.make_clients", return_value={r: model for r in ROLES}), \
                patch.object(CorpusIndex, "build", side_effect=AssertionError("must not rebuild")), \
                patch.object(CorpusIndex, "iter_records", side_effect=AssertionError("must not embed corpus")):
            result = execute(config, progress=lambda _: None)
        self.assertEqual(result["qa_aprovadas_modelo"], 1)
        self.assertTrue(result["indice_hibrido_pronto"])
        self.assertTrue(api.calls)
        sent = ["".join(chr(c) for c in text) for call in api.calls for text in call["input"]]
        self.assertNotIn(TEXT, sent)

    def test_local_windows_cover_tail_and_batches_are_cached(self):
        from types import SimpleNamespace
        class Tokenizer:
            def encode(self, text, **kwargs):
                return text.split()
            def decode(self, tokens, **kwargs):
                return " ".join(tokens)
        encoder = LocalE5.__new__(LocalE5)
        encoder.model = SimpleNamespace(tokenizer=Tokenizer())
        encoder.db = sqlite3.connect(":memory:")
        encoder.db.execute("CREATE TABLE windows(digest TEXT PRIMARY KEY,n INTEGER,matrix BLOB)")
        calls = []
        def encode(texts):
            calls.append(texts)
            values = np.zeros((len(texts), 384), dtype=np.float32)
            values[:, 0] = 1
            return values
        encoder._encode = encode
        text = " ".join(str(i) for i in range(1000))
        arrays = encoder.passages_many([text, "curto"])
        self.assertEqual([len(a) for a in arrays], [3, 1])
        self.assertEqual(len(calls), 1)
        covered = {t for w in calls[0] if w.startswith("passage: ") for t in w.split()[1:]}
        self.assertTrue(set(map(str, range(1000))).issubset(covered))
        self.assertTrue(all(len(w.split()) <= 512 for w in calls[0]))
        encoder.passages_many([text, "curto"])
        self.assertEqual(len(calls), 1)
        encoder.queries(["oxigênio residual"])
        self.assertEqual(calls[-1], ["query: oxigênio residual"])
        with self.assertRaisesRegex(ValueError, "excede 512"):
            encoder.queries(["termo " * 600])
        encoder.close()


if __name__ == "__main__":
    unittest.main()
