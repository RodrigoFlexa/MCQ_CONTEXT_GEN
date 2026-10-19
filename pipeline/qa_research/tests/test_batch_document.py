"""Contratos do lote: uma varredura, orçamento cumulativo e retorno íntegro."""
import contextlib
import copy
import io
import importlib.util
import json
import sys
import unittest
from pathlib import Path
from unittest.mock import patch

from pipeline.inventario.textutil import atomic_json, read_json
from pipeline.qa_research.document import batch
from pipeline.qa_research.document.common import ROOT, Packet, canonical, file_hash
from pipeline.qa_research.document.curation import facets_for, PLANS
from pipeline.qa_research.document.program import load_program
import test_document as document_fixture


class BatchDocumentTests(unittest.TestCase):
    def setUp(self):
        self.fixture = document_fixture.DocumentTests("test_local_preparation_reuses_frontier_without_reading_again")
        self.fixture.setUp()
        self.root = self.fixture.root
        # A suíte de preparação não lê nenhum dataset de questões.
        self.profile = self.fixture.packet.profile
        profile_path = self.root / "profile.json"
        atomic_json(profile_path, self.profile)
        self.rows = [{"id": key, "area_id": key[:2], "area": "Área " + key[:2],
            "subtopico": "Frase " + key, "profile": str(profile_path),
            "profile_sha256": file_hash(profile_path), "existing_packet": None}
            for key in ("01_01", "02_01")]
        self.program = self.root / "programa.json"
        atomic_json(self.program, {"schema": "document-program-v1", "items": self.rows})
        self.manifest = self.root / "lote.json"
        self.manifest_data = {"schema": "document-batch-v1", "program": str(self.program),
            "program_sha256": file_hash(self.program), "items": [{**r,
                "packet": str(self.fixture.path), "signature": self.fixture.packet.signature,
                "sources": 3, "facets": 2, "empty_facets": []} for r in self.rows]}
        atomic_json(self.manifest, self.manifest_data)
        self.output = self.root / "batch_output"

    def tearDown(self):
        self.fixture.tearDown()

    def executor(self, packet, output, **kwargs):
        from pipeline.qa_research.document.runner import run
        kwargs["client"] = document_fixture.SimulatedLLM()
        return run(packet, output, **kwargs)

    def test_every_specialist_phrase_has_manual_plan(self):
        from pipeline.fase_3.topicos import TOPICOS
        expected = {f"{ai:02}.{si:02}" for ai, (_, phrases) in enumerate(TOPICOS.items(), 1)
                    for si, _ in enumerate(phrases.items(), 1)} - {"02.02"}
        self.assertEqual(set(PLANS), expected)
        program = load_program()
        self.assertEqual(40, len(program["items"]))
        self.assertEqual(10, len({r["area_id"] for r in program["items"]}))
        for ai, (_, phrases) in enumerate(TOPICOS.items(), 1):
            for si, (_, scope) in enumerate(phrases.items(), 1):
                row = next(r for r in program["items"] if r["id"] == f"{ai:02}_{si:02}")
                self.assertEqual(scope, read_json(ROOT / row["profile"])["topic"]["escopo"])
        for key in PLANS:
            facets = facets_for(key, "Domínio técnico")
            self.assertGreaterEqual(len(facets), 4)
            self.assertTrue(all(len(f["consultas"]) == 2 and f["termos"] for f in facets))

    def test_unknown_selection_is_an_error(self):
        self.assertEqual(1, len(batch.choose(self.manifest_data["items"], ["02"])))
        self.assertEqual(1, len(batch.choose(self.manifest_data["items"], ["01_01"])))
        with self.assertRaises(ValueError):
            batch.choose(self.manifest_data["items"], ["unknown"])

    def test_reviewed_filters_reject_observed_context_confusions(self):
        from pipeline.qa_research.document.prepare import context_filter, fold
        examples = [
            ("02.01", 1, "Petróleo: densidade e compressibilidade em simulação de reservatório.",
             "Medição fiscal de petróleo: correção de volume pela densidade."),
            ("03.01", 0, "Operação offshore com duas sondas DP durante perfuração.",
             "FPSO: aproximação do navio aliviador para offloading."),
            ("06.04", 2, "Natural gas and fossil fuel production.",
             "Offshore SIS allocation of SIL and independent protection layers."),
        ]
        for key, index, bad, good in examples:
            f = facets_for(key, "Engenharia offshore")[index]
            rule = context_filter({**f, "context_groups": f["context_groups"] + f.get("post_context_groups", [])})
            self.assertFalse(rule(fold(bad)), key)
            self.assertTrue(rule(fold(good)), key)

    def test_translation_catalog_does_not_replace_technical_knowledge(self):
        from pipeline.qa_research.document.prepare import translation_list
        dictionary = "density densidade Port oil compressibility compressibilidade Port meter medidor Port valve válvula Port"
        self.assertTrue(translation_list(dictionary))
        self.assertFalse(translation_list("Bend stiffener: limita a curvatura do riser próximo à terminação."))
        self.assertFalse(translation_list(dictionary + ". O instrumento exige calibração. A medição é rastreável. A amostra deve ser representativa."))

    def test_corrupt_second_packet_prevents_any_call(self):
        self.manifest_data["items"][1]["signature"] = "alterado"
        atomic_json(self.manifest, self.manifest_data)
        calls = []
        with self.assertRaises(ValueError):
            batch.run_batch(self.manifest, self.output, execute=lambda *a, **k: calls.append(a))
        self.assertFalse(calls)

    def test_completed_batch_reuses_without_calls_and_collects_ten_area_shape(self):
        result = batch.run_batch(self.manifest, self.output, execute=self.executor, progress=lambda _: None)
        self.assertEqual("concluido", result["status"])
        with patch("pipeline.qa_research.document.runner.LLMClient", side_effect=AssertionError("não chamar")):
            again = batch.run_batch(self.manifest, self.output, progress=lambda _: None)
        self.assertEqual(2, again["concluidos"])
        destination = batch.collect_batch(self.manifest, self.output, self.root / "returned")
        batch.verify_results(destination)
        area = read_json(destination / "areas/01.json")
        self.assertEqual("Área 01", area["titulo"])
        self.assertEqual(1, len(area["secoes"]))
        self.assertNotIn("trechos", canonical(area))
        self.assertEqual(destination, batch.collect_batch(self.manifest, self.output, destination))
        (destination / "areas/01.md").write_text("alterado", encoding="utf-8")
        with self.assertRaises(ValueError):
            batch.verify_results(destination)

    def test_configuration_failure_stops_whole_batch(self):
        calls = []
        def fail(packet, folder, **kwargs):
            calls.append(str(folder))
            return {"status": "interrompido", "interrupcao": "configuração do backend", "blocos_publicados": 0}
        result = batch.run_batch(self.manifest, self.output, execute=fail, progress=lambda _: None)
        self.assertEqual(1, len(calls))
        self.assertEqual("interrompido", result["status"])

    def test_total_budget_counts_previous_reservations(self):
        atomic_json(self.output / "01_01/orcamento.json", {"tentativas_reservadas": 8})
        atomic_json(self.output / "02_01/orcamento.json", {"tentativas_reservadas": 2})
        calls = []
        result = batch.run_batch(self.manifest, self.output, total_max_calls=10,
            execute=lambda *a, **k: calls.append(k), progress=lambda _: None)
        self.assertFalse(calls)
        self.assertEqual("orçamento total do lote atingido", result["interrupcao"])

    def test_per_phrase_budget_does_not_stop_other_phrases(self):
        calls = []
        def exhausted(packet, folder, **kwargs):
            calls.append(str(folder))
            atomic_json(Path(folder) / "orcamento.json", {"tentativas_reservadas": 3})
            return {"status": "interrompido", "interrupcao": "orçamento ou erro fatal", "blocos_publicados": 0}
        result = batch.run_batch(self.manifest, self.output, max_calls=3,
            execute=exhausted, progress=lambda _: None)
        self.assertEqual(2, len(calls))
        self.assertIsNone(result["interrupcao"])

    def test_batch_notification_uses_actual_paths(self):
        with contextlib.redirect_stdout(io.StringIO()) as console:
            commands = batch.completion_batch(self.manifest, self.output, self.root / "returned", "parcial")
        self.assertIn("O código acabou de rodar no terminal", console.getvalue())
        self.assertIn("parcial", console.getvalue())
        self.assertIn("collect", commands[0])
        from pipeline.qa_research.document.terminal import command_path
        self.assertIn(command_path(self.manifest), commands[0])
        self.assertEqual("git", commands[-1][0])

    @unittest.skipUnless(importlib.util.find_spec("ahocorasick"), "Dependência apenas da preparação local")
    def test_joint_frontier_reads_one_stream_for_two_profiles(self):
        from pipeline.qa_research.document.batch_prepare import shared_frontiers
        profiles = []
        records_seen = []
        for item in self.rows:
            profile = copy.deepcopy(self.profile)
            profile["cache_dir"] = str(self.root / "cache")
            profile["selection"]["frontier_per_facet"] = 2
            for f in profile["facets"]:
                f["termos"] = ["espuma", "tratamento"]
                f["context_groups"] = []
            profiles.append((item, profile))
        def originals():
            for s in self.fixture.sources:
                records_seen.append(s["id"])
                yield s
        def metadata(*args):
            return originals(), [{"sha256": "fixture"}], "fixture", []
        with patch("pipeline.qa_research.document.batch_prepare.inputs", side_effect=metadata):
            first = shared_frontiers(profiles, lambda _: None)
            second = shared_frontiers(profiles, lambda _: None)
            for _, p in profiles:
                p["facets"][0]["post_context_groups"] = [["espuma"]]
            third = shared_frontiers(profiles, lambda _: None)
        self.assertEqual(3, len(records_seen))
        self.assertEqual(first, second)
        self.assertEqual(first, third)
        self.assertEqual(2, len(first))
        self.assertTrue(all(len(v) == 2 for f in first.values() for v in f["rows"].values()))

    def test_server_entry_does_not_import_ml(self):
        import subprocess
        result = subprocess.run([sys.executable, "-S", "-c",
            "import sys; from pipeline.qa_research.document.batch import main; "
            "assert not any(m in sys.modules for m in ['torch','numpy','ahocorasick','sentence_transformers']); "
            "print('stdlib-only')"], cwd=ROOT, capture_output=True, text=True)
        self.assertEqual(0, result.returncode, result.stderr)
        self.assertIn("stdlib-only", result.stdout)


if __name__ == "__main__":
    unittest.main()
