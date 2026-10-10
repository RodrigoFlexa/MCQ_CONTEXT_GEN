"""Testes do contrato experimental e da recuperação, sem Azure ou downloads."""
import contextlib
import hashlib
import io
import json
import random
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

import numpy as np

from pipeline.fase_4.config import QAConfig, ROOT
from pipeline.fase_4.domain import DomainResources, TOPICOS, legacy
from pipeline.fase_4.engine import execute, build_clients
from pipeline.fase_4.examples import ExamplePool, build_seed_bank
from pipeline.qa_references.download_qa_examples import CATALOG, normalize
from pipeline.fase_4.scoring import parse_verdict
from pipeline.fase_4.storage import read_jsonl, RunStore, BudgetedClient

SOURCE = "A bomba transfere energia ao fluido e estabelece a pressão necessária ao processo."
QUESTION = "Qual é a função da bomba no FPSO?"
ANSWER = "Transferir energia ao fluido."
TOPIC = next(iter(TOPICOS))
OTHER = next(t for t in TOPICOS if t != TOPIC)
SUBTOPIC = next(iter(TOPICOS[TOPIC]))


class FakeEmbedder:
    dim = 16

    def __init__(self, cfg=None, verbose=True, identical=False):
        self.identical = identical

    def encode(self, texts, **kwargs):
        values = []
        for text in texts:
            if self.identical:
                vector = np.ones(self.dim, dtype=np.float32)
            else:
                rng = np.random.default_rng(int(hashlib.sha256(text.encode()).hexdigest()[:8], 16))
                vector = rng.normal(size=self.dim).astype(np.float32)
            values.append(vector / np.linalg.norm(vector))
        return np.stack(values) if values else np.zeros((0, self.dim), dtype=np.float32)

    def salvar_cache(self):
        pass


class FakeDomain:
    signature = "test-domain"

    def __init__(self):
        self.emb = FakeEmbedder(identical=True)

    def covered_subtopics(self, topic):
        return list(TOPICOS[topic])

    def materialize(self, topic, subtopic, cursor):
        return {"topic": topic, "subtopic": subtopic, "scope": "Operação de FPSO",
                "focus": "Função de bombas", "document": SOURCE,
                "chunks": [{"chunk_id": "corpus.txt:1-1", "arquivo": "corpus.txt",
                            "linha_ini": 1, "linha_fim": 1, "texto": SOURCE}],
                "doc_id": f"document-{cursor}", "facet_id": "facet-test",
                "facet_title": "Bombas", "corpus_signature": self.signature}

    def entropy(self, rows, topic, subtopic=None):
        values = [r for r in rows if r.get("topic") == topic and
                  (subtopic is None or r.get("subtopic") == subtopic)]
        return {"value": 0.0, "clusters_visited": int(bool(values)),
                "clusters_total": 2, "n_questions": len(values), "reliable": True}


class FakeBackend:
    def __init__(self, role, calls, *, bad_first=False, invalid_judge=False):
        self.role, self.calls = role, calls
        self.bad_first, self.invalid_judge = bad_first, invalid_judge
        self.invocations = 0
        self.judged_questions = []

    def complete_json(self, prompt, **kwargs):
        import re
        self.invocations += 1
        self.calls.append(self.role)
        valid = {"question": QUESTION, "answer": ANSWER, "concept": "função de bombas",
                 "evidence": [{"chunk_id": "corpus.txt:1-1", "quote": SOURCE}]}
        if self.role == "generator":
            count = int(re.search(r"Gere (\d+)", prompt).group(1))
            rows = [dict(valid) for _ in range(count)]
            if self.bad_first and self.invocations == 1:
                rows[0] = {**valid, "question": "Segundo o texto, qual é a função da bomba?",
                           "evidence": [{"chunk_id": "corpus.txt:1-1", "quote": "Uma frase que não existe no corpus."}]}
            return {"items": rows}
        if self.role == "refiner":
            return {**valid, "changes": "Remove referência ao texto e corrige a evidência"}
        if self.role == "judge":
            text = prompt.split("Questões finais:\n", 1)[1].split("\nRetorne apenas JSON", 1)[0]
            questions = json.loads(text)
            self.judged_questions.extend(questions)
            rows = [{"id": q["id"], "technical_ok": True, "supported_by_sources": True,
                     "scope_ok": True, "self_contained": True, "technical_correctness": .9,
                     "clarity": .9, "answer_completeness": .9, "domain_relevance": .9,
                     "difficulty": "facil", "comment": "Sustentada pela fonte"} for q in questions]
            if self.invalid_judge:
                for row in rows:
                    del row["supported_by_sources"]
            return {"evaluations": rows}
        return {"facetas": [{"titulo": "Bomba", "foco": "Função de bombas",
                "query": "bomba pressão", "termos_fortes": ["bomba"], "termos_apoio": ["fluido"]}]}

    def complete(self, prompt, **kwargs):
        self.calls.append(self.role)
        return SOURCE


class PipelineTests(unittest.TestCase):
    def setUp(self):
        # Mantém os artefatos temporários dentro do workspace autorizado.
        base = ROOT / "pipeline/fase_4/saida_qa_tests"
        base.mkdir(exist_ok=True)
        self.tmp = tempfile.TemporaryDirectory(dir=base)
        self.assertTrue(Path(self.tmp.name).resolve().is_relative_to(base.resolve()))
        self.addCleanup(self.tmp.cleanup)
        self.cfg = QAConfig(output=Path(self.tmp.name), topics=[TOPIC], limit_per_topic=12,
                            batch_size=2, max_attempts_per_topic=30,
                            entropy_warmup=4, entropy_patience=2)
        self.calls = []
        self.seeds = [{"id": "expert-test", "question": "Qual sistema fornece energia elétrica?",
                       "answer": "Geração elétrica.", "origin": "expert_approved", "topic": OTHER,
                       "selection_weight": 3.0, "human_approved": True}]
        self.external = [{"id": "arc_easy:test", "question": "What is evaporation?", "answer": "A phase change."}]

    def run_pipeline(self, *, bad_first=False, invalid_judge=False):
        backends = {role: FakeBackend(role, self.calls, bad_first=bad_first, invalid_judge=invalid_judge)
                    for role in ("preparation", "generator", "refiner", "judge")}
        with contextlib.redirect_stdout(io.StringIO()):
            store = execute(self.cfg, backends=backends, domain=FakeDomain(),
                            seeds=self.seeds, external=self.external)
        return store, backends

    def test_observation_continues_with_identical_questions_and_saturation(self):
        store, _ = self.run_pipeline()
        self.assertEqual(len(store.accepted), 12)
        self.assertTrue(any(r["saturation_diagnostics"]["configured_saturation_would_stop"] for r in store.rounds))
        self.assertTrue(all(r["counterfactual_decisions"]["cosine_050_reject"] for r in store.accepted))
        self.assertTrue(any(r["counterfactual_decisions"]["exact_reject"] for r in store.accepted))
        self.assertTrue(all(not r["cosine_filter_enabled"] for r in store.accepted))
        self.assertTrue(all(r["judge"]["checks"]["supported_by_sources"] for r in store.accepted))
        self.assertEqual(store.meta["status"], "completed")

    def test_refiner_repairs_before_judge_sees_final_question(self):
        self.cfg.limit_per_topic = 2
        store, backends = self.run_pipeline(bad_first=True)
        self.assertEqual(self.calls[:3], ["generator", "refiner", "judge"])
        self.assertEqual(backends["judge"].judged_questions[0]["question"], QUESTION)
        row = store.accepted[0]
        self.assertNotEqual(row["original"]["question"], row["question"])
        self.assertFalse(row["scorer"]["needs_refinement"])
        self.assertTrue(row["refinements"])
        self.assertEqual(row["source_chunks"][0]["arquivo"], "corpus.txt")

    def test_missing_judge_evidence_verdict_never_passes(self):
        self.cfg.max_attempts_per_topic = 4
        store, _ = self.run_pipeline(invalid_judge=True)
        self.assertEqual(len(store.accepted), 0)
        self.assertTrue(all(r["rejection_reason"] == "invalid_judge_booleans" for r in store.records))
        self.assertEqual(store.meta["status"], "finished_with_limits")
        calls_before = store.state["api_calls"]
        self.cfg.resume = True
        resumed, _ = self.run_pipeline(invalid_judge=True)
        self.assertEqual(resumed.state["api_calls"], calls_before)

    def test_opt_in_cosine_filter_rejects_while_default_does_not(self):
        self.cfg.enable_cosine_filter = True
        self.cfg.max_attempts_per_topic = 4
        store, _ = self.run_pipeline()
        self.assertEqual(len(store.accepted), 0)
        self.assertTrue(all(r["quality_approved"] for r in store.records))
        self.assertTrue(all(r["rejection_reason"] == "cosine_filter_explicitly_enabled" for r in store.records))

    def test_opt_in_saturation_stops_only_when_enabled(self):
        self.cfg.enable_saturation_stop = True
        store, _ = self.run_pipeline()
        self.assertEqual(len(store.accepted), 4)
        summary = json.loads((self.cfg.output / "resumo_topicos.json").read_text(encoding="utf-8"))
        self.assertEqual(summary[0]["stop_reason"], "topic_saturated")

    def test_resume_rebuilds_export_and_preserves_ids_and_calls(self):
        self.cfg.limit_per_topic = 4
        initial, _ = self.run_pipeline()
        old_ids = {r["id"] for r in initial.accepted}
        old_calls = initial.state["api_calls"]
        (self.cfg.output / "questoes_qa.jsonl").unlink()
        self.cfg.resume = True
        resumed, _ = self.run_pipeline()
        self.assertEqual(resumed.state["api_calls"], old_calls)
        self.assertEqual({r["id"] for r in read_jsonl(self.cfg.output / "questoes_qa.jsonl")}, old_ids)
        self.cfg.limit_per_topic = 6
        expanded, _ = self.run_pipeline()
        self.assertEqual(len(expanded.accepted), 6)
        self.assertTrue(old_ids < {r["id"] for r in expanded.accepted})

    def test_global_call_budget_includes_generator_and_judge(self):
        self.cfg.max_calls = 4
        store, _ = self.run_pipeline()
        self.assertEqual(store.state["api_calls"], 4)
        self.assertEqual(store.state["calls_by_role"], {"generator": 2, "judge": 2})
        self.assertEqual(len(store.accepted), 4)

    def test_old_ungrounded_output_is_not_resumed(self):
        (self.cfg.output / "run_config.json").write_text('{"deployment":"old"}')
        self.cfg.resume = True
        with self.assertRaisesRegex(ValueError, "incompatível"):
            self.run_pipeline()

    def test_source_changes_require_a_new_run(self):
        self.cfg.limit_per_topic = 2
        self.run_pipeline()
        self.cfg.resume = True
        self.external[0]["answer"] = "Changed"
        with self.assertRaisesRegex(ValueError, "bancos de exemplos mudaram"):
            self.run_pipeline()

    def test_judge_false_source_gate_rejects_even_perfect_scores(self):
        verdict = {"technical_ok": True, "supported_by_sources": False, "scope_ok": True,
                   "self_contained": True, "technical_correctness": 1, "clarity": 1,
                   "answer_completeness": 1, "domain_relevance": 1, "difficulty": "facil"}
        self.assertFalse(parse_verdict(verdict, self.cfg)["approved"])

    def test_resume_cannot_change_experimental_policy(self):
        self.cfg.limit_per_topic = 2
        self.run_pipeline()
        self.cfg.resume = True
        self.cfg.format_examples += 1
        with self.assertRaisesRegex(ValueError, "format_examples mudou"):
            self.run_pipeline()

    def test_domain_retrieval_uses_real_fixture_and_preserves_line_provenance(self):
        corpus = self.cfg.output / "corpus"
        corpus.mkdir()
        text = "bomba fluido pressão processo energia operação vazão manutenção segurança controle sistema produção offshore equipamento válvula fluxo água óleo gás FPSO"
        (corpus / "domain.txt").write_text("\n".join(f"{text} registro{i}" for i in range(70)), encoding="utf-8")
        self.cfg.corpus_dir = corpus
        tiny_topics = {"Topic A": {"Sub A": "bomba fluido pressão"}}
        prep = FakeBackend("preparation", self.calls)
        with patch("pipeline.fase_4.domain.TOPICOS", tiny_topics), patch.object(legacy, "Embedder", FakeEmbedder), contextlib.redirect_stdout(io.StringIO()):
            resources = DomainResources(self.cfg, prep).prepare(["Topic A"])
            context = resources.materialize("Topic A", "Sub A", 0)
        self.assertTrue(context["chunks"])
        self.assertTrue(all(x["arquivo"] == "domain.txt" and x["linha_fim"] >= x["linha_ini"] for x in context["chunks"]))
        self.assertIn("bomba", context["chunks"][0]["texto"])
        self.assertTrue((self.cfg.output / "dominio/indices/candidatos.jsonl").exists())

    def test_missing_corpus_fails_before_preparation_calls(self):
        self.cfg.corpus_dir = self.cfg.output / "missing"
        with self.assertRaises(FileNotFoundError):
            DomainResources(self.cfg, FakeBackend("preparation", self.calls)).prepare([TOPIC])
        self.assertFalse(self.calls)

    def test_target_is_total_per_topic_across_subtopics(self):
        topic = next(t for t, subs in TOPICOS.items() if len(subs) > 1)
        self.cfg.topics, self.cfg.limit_per_topic = [topic], 7
        self.seeds[0]["topic"] = TOPIC
        store, _ = self.run_pipeline()
        self.assertEqual(len(store.accepted), 7)
        self.assertGreater(len({r["subtopic"] for r in store.accepted}), 1)
        self.assertEqual({r["requested_difficulty"] for r in store.accepted}, {"facil", "media", "dificil"})

    def test_quality_pool_excludes_low_scores_and_current_topic(self):
        accepted = [{"id": "good", "nota": .9, "topic": OTHER},
                    {"id": "bad", "nota": .2, "topic": OTHER},
                    {"id": "same-topic", "nota": 1, "topic": TOPIC}]
        pool = ExamplePool(self.cfg, self.seeds, accepted)
        selected = pool.sample_quality(TOPIC, 1)
        self.assertEqual({r["id"] for r in selected}, {"expert-test", "good"})

    def test_real_human_seed_sources_keep_evaluation_provenance(self):
        seeds = build_seed_bank(self.cfg)
        self.assertTrue(any(r["origin"] == "human_preference_phase2" and r.get("votes") for r in seeds))
        self.assertTrue(any(r["origin"] == "expert_approved" and r.get("review_id") for r in seeds))
        self.assertTrue(all("alternatives" not in r and r["question"] and r["answer"] for r in seeds))

    def test_backend_effort_is_not_silently_dropped(self):
        backend = FakeBackend("refiner", self.calls)
        backend._unsupported = {"reasoning_effort"}
        client = BudgetedClient(backend, "refiner", RunStore(self.cfg))
        with self.assertRaisesRegex(RuntimeError, "esforço removido"):
            client.complete_json("test")

    def test_all_roles_use_requested_azure_deployment_and_high_effort(self):
        with patch("azure_openai_backend.AzureOpenAIBackend") as factory:
            clients = build_clients(self.cfg, RunStore(self.cfg))
        self.assertEqual(set(clients), {"preparation", "generator", "refiner", "judge"})
        self.assertEqual(factory.call_count, 4)
        for call in factory.call_args_list:
            self.assertEqual(call.kwargs["deployment"], "gpt-5-4-petrobras")
            self.assertEqual(call.kwargs["reasoning_effort"], "high")
            self.assertEqual(call.kwargs["reasoning_min_tokens"], 12000)

    def test_arc_examples_are_qa_and_option_dependent_stems_are_removed(self):
        arc = next(x for x in CATALOG if x["id"] == "arc_easy")
        row = {"id": "fixture", "question": "What causes water evaporation?", "answerKey": "B",
               "choices": {"label": ["A", "B"], "text": ["Clouds", "Heat"]}}
        exported = normalize(arc, {"row": row})
        self.assertEqual(exported["answer"], "Heat")
        self.assertNotIn("choices", exported)
        for question in ("Which of these describes evaporation?", "Qual das seguintes causas evaporação?"):
            self.assertIsNone(normalize(arc, {"row": {**row, "question": question}}))


if __name__ == "__main__":
    unittest.main()
