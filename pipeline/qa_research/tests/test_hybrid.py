"""FAISS real e cliente Azure simulado: verifica mecanismos, não qualidade do modelo."""
import copy
import json
import tempfile
import unittest
from pathlib import Path
from types import SimpleNamespace
from unittest.mock import patch

import numpy as np

from pipeline.inventario.llm import BudgetExceeded
from pipeline.qa_research.config import Config
from pipeline.qa_research.corpus import CorpusIndex
from pipeline.qa_research.embeddings import AzureEmbedder
from pipeline.qa_research.hybrid import HybridCorpusIndex, LLMReranker, validate_ranking
from pipeline.qa_research.runtime import PersistentBudget


class Tokenizer:
    def encode(self, text, **kwargs):
        return [ord(c) for c in text]


class EmbeddingAPI:
    def __init__(self):
        self.calls, self.errors, self.closed = [], [], False
        self.embeddings = self
        self.invalid = None

    def create(self, **kwargs):
        self.calls.append(copy.deepcopy(kwargs))
        if self.errors:
            raise self.errors.pop(0)
        rows = []
        for i, tokens in enumerate(kwargs["input"]):
            text = "".join(chr(c) for c in tokens).lower()
            vector = np.zeros(kwargs["dimensions"], dtype=np.float32)
            slot = 0 if "oxygen" in text or "oxigênio" in text else 1 if "sulfato" in text else 2
            vector[slot] = 1
            if self.invalid == "dimensions":
                vector = vector[:2]
            if self.invalid == "nan":
                vector[0] = np.nan
            if self.invalid == "zero":
                vector[:] = 0
            rows.append(SimpleNamespace(index=i, embedding=vector.tolist()))
        if self.invalid == "incomplete":
            rows = rows[:-1]
        return SimpleNamespace(data=list(reversed(rows)), usage=SimpleNamespace(total_tokens=sum(map(len, kwargs["input"]))),
                               model="text-embedding-3-large")

    def close(self):
        self.closed = True


class Reranker:
    def __init__(self):
        self.calls, self.zero, self.prefer = [], False, "Oxigênio"

    def rank(self, query, candidates, context):
        self.calls.append((query, copy.deepcopy(candidates), context))
        return {"avaliacoes": [{"id": c["content_hash"],
                "score": 0 if self.zero else 3 if self.prefer in c["texto"] else 1,
                "motivo": "Pontuação simulada de teste"} for c in candidates]}


class HybridTests(unittest.TestCase):
    def setUp(self):
        self.temporary = tempfile.TemporaryDirectory(dir=Path(__file__).parent)
        self.root = Path(self.temporary.name)
        self.origin = self.root / "source"
        self.origin.mkdir()
        self.config = Config(topic={"titulo": "Produtos químicos", "escopo": "Produtos químicos e desaeração"},
            output=str(self.root / "output"), origins=[str(self.origin)], index_dir=str(self.root / "index"))
        texts = ["Oxigênio dissolvido é removido por sequestrante químico.",
                 "A unidade de remoção de sulfato opera com membranas.",
                 "O solvente MEG atua na prevenção de hidratos."]
        rows = [{"chunk_id": f"fixture:D{i}:p1:w0", "collection": "fixture", "document_id": f"D{i}",
                 "texto": t, "title": f"Documento {i}", "page_ini": 1, "page_fim": 1}
                for i, t in enumerate(texts)]
        (self.origin / "selecao.json").write_text(json.dumps({"assuntos": {"a": {"trechos": rows}}}), encoding="utf-8")
        self.lexical = CorpusIndex(self.root / "lexical", [self.origin])
        self.lexical.build()
        self.api = EmbeddingAPI()
        self.budget = PersistentBudget(self.root / "budget.json", 100)
        self.embedder = AzureEmbedder(self.config, self.budget, client=self.api, tokenizer=Tokenizer())
        self.reranker = Reranker()
        self.hybrid = HybridCorpusIndex(self.config, self.lexical, self.embedder, self.reranker)

    def tearDown(self):
        self.embedder.close()
        self.temporary.cleanup()

    def test_dense_channel_recovers_without_lexical_match_and_preserves_sources(self):
        self.hybrid.build()
        self.assertEqual(self.lexical.search("oxygen scavenger"), [])
        rows = self.hybrid.search("oxygen scavenger", limit=1)
        self.assertIn("Oxigênio", rows[0]["texto"])
        self.assertEqual(set(rows[0]["retrieval"]["channels"]), {"dense"})
        self.assertEqual(rows[0]["document_id"], "D0")
        self.assertIn("provenance", rows[0])
        self.assertTrue(list((Path(self.config.output) / "recuperacoes").glob("*.json")))

    def test_rrf_combines_rank_positions_without_mixing_score_scales(self):
        self.hybrid.build()
        rows = self.hybrid.search("Oxigênio", limit=1)
        retrieval = rows[0]["retrieval"]
        self.assertEqual(set(retrieval["channels"]), {"lexical", "dense"})
        self.assertAlmostEqual(retrieval["rrf"], 2 / (self.config.rrf_constant + 1))

    def test_reranker_can_promote_complementary_evidence(self):
        self.hybrid.build()
        self.reranker.prefer = "sulfato"
        rows = self.hybrid.search_contextual("oxygen scavenger", limit=1, context={"recorte": "compatibilidade"})
        self.assertIn("sulfato", rows[0]["texto"])
        self.assertEqual(self.reranker.calls[-1][2], {"recorte": "compatibilidade"})

    def test_all_irrelevant_candidates_are_not_forced_into_context(self):
        self.hybrid.build()
        self.reranker.zero = True
        self.assertEqual(self.hybrid.search("oxygen scavenger"), [])

    def test_missing_reranker_never_silently_degrades_to_bm25(self):
        self.hybrid.build()
        self.hybrid.reranker = None
        with self.assertRaises(RuntimeError):
            self.hybrid.search("oxygen")

    def test_failed_reranker_does_not_publish_a_fallback_selection(self):
        self.hybrid.build()
        with patch.object(self.reranker, "rank", side_effect=RuntimeError("indisponível")):
            with self.assertRaises(RuntimeError):
                self.hybrid.search("oxygen")

    def test_source_exclusion_applies_to_both_channels(self):
        self.hybrid.build()
        result = self.hybrid.search("Oxigênio", limit=1)[0]
        others = self.hybrid.search("Oxigênio", exclude=[result["chunk_id"], result["content_hash"]])
        self.assertNotIn(result["chunk_id"], [c["chunk_id"] for c in others])

    def test_warm_index_and_query_cache_make_no_extra_embedding_requests(self):
        self.hybrid.build()
        self.hybrid.search("oxygen")
        count = len(self.api.calls)
        second = HybridCorpusIndex(self.config, self.lexical, self.embedder, self.reranker)
        second.build()
        second.search("oxygen")
        self.assertEqual(len(self.api.calls), count)
        self.assertEqual(self.hybrid.vector.info["kind"], "flat_ip_exact")

    def test_corrupted_faiss_snapshot_is_not_reused(self):
        self.hybrid.build()
        file = next((Path(self.config.index_dir) / "dense").glob("*/index.faiss"))
        with file.open("ab") as stream:
            stream.write(b"corruption")
        with self.assertRaisesRegex(ValueError, "corrompido"):
            HybridCorpusIndex(self.config, self.lexical, self.embedder, self.reranker).build()

    def test_embedding_cache_invalidates_when_protocol_changes(self):
        self.embedder.encode(["oxygen"])
        self.config.embedding_deployment = "outro-deployment"
        other = AzureEmbedder(self.config, self.budget, client=self.api, tokenizer=Tokenizer())
        try:
            other.encode(["oxygen"])
            self.assertNotEqual(other.signature, self.embedder.signature)
            self.assertEqual(len(self.api.calls), 2)
        finally:
            other.close()

    def test_input_reaches_azure_with_requested_model_and_dimensions(self):
        vector = self.embedder.encode(["oxygen"])[0]
        request = self.api.calls[0]
        self.assertEqual(request["model"], "embedding-3-large-global")
        self.assertEqual(request["dimensions"], 3072)
        self.assertAlmostEqual(float(np.linalg.norm(vector)), 1.)

    def test_long_text_is_windowed_without_losing_tail(self):
        self.config.embedding_window_tokens = 128
        self.config.embedding_overlap_tokens = 16
        # Construir outro embedder para que o protocolo corresponda aos limites usados.
        other = AzureEmbedder(self.config, self.budget, client=self.api, tokenizer=Tokenizer())
        try:
            vector = other.encode(["x" * 300 + "Z"])[0]
            inputs = [entry for call in self.api.calls for entry in call["input"]]
            self.assertTrue(all(len(i) <= 128 for i in inputs))
            self.assertEqual(inputs[-1][-1], ord("Z"))
            self.assertAlmostEqual(float(np.linalg.norm(vector)), 1.)
        finally:
            other.close()

    def test_duplicate_texts_are_embedded_once_and_output_order_is_preserved(self):
        vectors = self.embedder.encode(["oxygen", "sulfato", "oxygen"])
        self.assertEqual(len(self.api.calls[0]["input"]), 2)
        np.testing.assert_array_equal(vectors[0], vectors[2])
        self.assertFalse(np.array_equal(vectors[0], vectors[1]))

    def test_embedding_response_is_validated(self):
        for invalid in ("dimensions", "nan", "zero", "incomplete"):
            self.api.invalid = invalid
            with self.subTest(invalid=invalid), self.assertRaises(ValueError):
                self.embedder.encode(["uncached " + invalid])

    def test_budget_exhaustion_prevents_embedding_http_call(self):
        self.budget.limit = 1
        self.embedder.encode(["oxygen"])
        with self.assertRaises(BudgetExceeded):
            self.embedder.encode(["sulfato"])
        self.assertEqual(len(self.api.calls), 1)

    def test_transient_retries_are_counted_and_logged(self):
        class RateLimitError(Exception):
            status_code = 429
        self.api.errors = [RateLimitError("simulado")]
        self.embedder.sleep = lambda _: None
        self.embedder.encode(["oxygen"])
        self.assertEqual(self.budget.used, 2)
        rows = self.embedder.log.read_text(encoding="utf-8").splitlines()
        self.assertEqual(len(rows), 2)

    def test_empty_input_is_not_embedded(self):
        with self.assertRaises(ValueError):
            self.embedder.encode([""])
        self.assertEqual(self.api.calls, [])

    def test_pipeline_research_and_qa_use_hybrid_sources_and_context(self):
        from pipeline.qa_research.tests.test_pipeline import FixtureModel, TEXT
        from pipeline.qa_research.config import ROLES
        from pipeline.qa_research.run import execute
        row = {"chunk_id": "fixture:whole:p1:w0", "collection": "fixture", "document_id": "whole",
               "texto": TEXT, "title": "Fonte de teste", "page_ini": 1, "page_fim": 1}
        (self.origin / "selecao.json").write_text(json.dumps({"assuntos": {"a": {"trechos": [row]}}}), encoding="utf-8")
        self.lexical.build()
        self.config.initial_facets = self.config.max_facets = self.config.target_qa = 1
        self.config.max_repairs = 0
        model = FixtureModel()
        result = execute(self.config, clients={role: model for role in ROLES}, index=self.hybrid, progress=lambda _: None)
        self.assertEqual(result["qa_aprovadas_modelo"], 1)
        self.assertTrue(result["indice_hibrido_pronto"])
        self.assertTrue(any("recorte" in context for _, _, context in self.reranker.calls))
        source = next(payload["evidencias"][0] for stage, payload in model.requests if stage == "RESEARCH")
        self.assertEqual(source["retrieval"]["kind"], "hybrid_reranked")

    def test_ivfpq_build_and_reload_with_real_faiss(self):
        # Dimensão reduzida SOMENTE na fixture para testar treino/serialização rapidamente.
        # Config.validate continua exigindo 3072 na execução real.
        self.config.embedding_dimensions = 96
        self.config.vector_flat_threshold = 10
        texts = [f"Fixture numérica {i}" for i in range(10000)]
        rows = [{"chunk_id": f"fixture:compressed:p1:w{i}", "texto": text,
                 "document_id": "compressed", "collection": "fixture", "title": "Fixture"}
                for i, text in enumerate(texts)]
        (self.origin / "selecao.json").write_text(json.dumps({"assuntos": {"a": {"trechos": rows}}}), encoding="utf-8")
        self.lexical.build()
        class RandomEmbedder:
            protocol = {"fixture": "random-unit-vectors-96", "dimensions": 96}
            def encode(self, values):
                from pipeline.inventario.textutil import sha
                array = np.stack([np.random.default_rng(int(sha(v, 8), 16)).normal(size=96).astype(np.float32) for v in values])
                return array / np.linalg.norm(array, axis=1)[:, None]
        from pipeline.qa_research.hybrid import VectorIndex
        vector = VectorIndex(self.config, self.lexical, RandomEmbedder())
        info = vector.build()
        self.assertEqual(info["kind"], "ivfpq_ip_approximate")
        self.assertEqual(vector.index.ntotal, 10000)
        second = VectorIndex(self.config, self.lexical, RandomEmbedder())
        self.assertEqual(second.build()["signature"], info["signature"])
        self.assertTrue(second.search(texts[123], 10, ()))

    def test_production_wiring_prepares_index_then_research_and_qa(self):
        from pipeline.qa_research.tests.test_pipeline import FixtureModel, TEXT
        from pipeline.qa_research.config import ROLES
        from pipeline.qa_research.run import execute
        from pipeline.qa_research.hybrid import RERANK_PROMPT
        source = {"chunk_id": "fixture:wiring:p1:w0", "collection": "fixture", "document_id": "wiring",
                  "texto": TEXT, "title": "Fonte de teste", "page_ini": 1, "page_fim": 1}
        (self.origin / "selecao.json").write_text(json.dumps({"assuntos": {"a": {"trechos": [source]}}}), encoding="utf-8")
        self.config.initial_facets = self.config.max_facets = self.config.target_qa = 1
        self.config.max_repairs = 0
        class Model(FixtureModel):
            def json(self, system, user, **kwargs):
                if system != RERANK_PROMPT:
                    return super().json(system, user, **kwargs)
                payload = json.loads(user)
                self.requests.append(("RERANK", payload))
                result = {"avaliacoes": [{"id": c["id"], "score": 3, "motivo": "Teste de integração"}
                          for c in payload["candidatos"]]}
                kwargs["validate"](result)
                return result
            def close(self):
                pass
        model = Model()
        real_embedder = AzureEmbedder
        def factory(config, budget):
            return real_embedder(config, budget, client=self.api, tokenizer=Tokenizer())
        with patch("pipeline.qa_research.embeddings.AzureEmbedder", side_effect=factory):
            with patch("pipeline.qa_research.run.make_clients", side_effect=AssertionError("Índice não deve criar LLM")):
                prepared = execute(self.config, stage="indice", progress=lambda _: None)
            self.assertTrue(prepared["indice_hibrido_pronto"])
            with patch("pipeline.qa_research.run.make_clients", return_value={role: model for role in ROLES}):
                research = execute(self.config, stage="pesquisa", progress=lambda _: None)
                qa = execute(self.config, stage="qa", progress=lambda _: None)
            self.assertEqual(research["capitulos_publicados"], 1)
            self.assertEqual(qa["qa_aprovadas_modelo"], 1)
            self.assertGreater(qa["tentativas_embeddings_cumulativas"], 0)
            self.assertTrue(any(stage == "RERANK" for stage, _ in model.requests))


class RankingTests(unittest.TestCase):
    def test_invalid_scores_and_incomplete_ranking_are_rejected(self):
        for data in ({"avaliacoes": []}, {"avaliacoes": [{"id": "x", "score": True, "motivo": "a"}]},
                     {"avaliacoes": [{"id": "other", "score": 3, "motivo": "a"}]}):
            with self.assertRaises(ValueError):
                validate_ranking(data, ["x"])

    def test_llm_reranker_receives_only_sources_and_research_context(self):
        class Client:
            def json(self, system, user, **kwargs):
                self.payload = json.loads(user)
                result = {"avaliacoes": [{"id": "x", "score": 2, "motivo": "Complementar"}]}
                kwargs["validate"](result)
                return result
        client = Client()
        LLMReranker(client).rank("oxygen", [{"content_hash": "x", "texto": "Original"}], {"recorte": "Água"})
        self.assertNotIn("resposta", client.payload)
        self.assertEqual(client.payload["contexto"], {"recorte": "Água"})


if __name__ == "__main__":
    unittest.main()
