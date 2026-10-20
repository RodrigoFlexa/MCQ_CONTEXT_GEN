"""Regressões de retomada e citações com os arquivos reais do servidor, sem API."""
import copy
import io
import shutil
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from pipeline.inventario.llm import CallFailed, LLMError
from pipeline.inventario.textutil import atomic_json, read_json
from pipeline.qa_research.document.common import ROOT, file_hash
from pipeline.qa_research.qa_batch import contracts as C, references
from pipeline.qa_research.qa_batch.config import Config
from pipeline.qa_research.qa_batch.runner import Runner
from pipeline.qa_research.qa_all import collect_all, configurations, execute, finished
from pipeline.qa_research.tests.test_qa_batch import FakeLLM, batch, review, resolution


SNAPSHOTS = ROOT / "pipeline/qa_research/relatorios"
FAILED = SNAPSHOTS / "qa_lote_9_03_02_20261020T172806026463Z"
APPROVED = SNAPSHOTS / "qa_lote_9_02_02_20261020T162624575988Z"


class ReferenceTests(unittest.TestCase):
    def test_all_context_preserved_and_ids_resolve_to_original_text(self):
        context = "Primeira relação.\n\nSegunda relação.\nCondição necessária."
        questions = batch()["questoes"]
        catalog = references.catalog(context, questions)
        self.assertEqual(C.norm("\n\n".join(catalog["contexto"].values())), C.norm(context))
        raw = review()
        for row in raw["itens"]:
            row["fundamentos"] = ["C0002"]
            row["teste_de_unicidade"]["condicao_que_a_exclui"] = []
        raw["itens"][6]["teste_de_unicidade"] = {
            "outra_resposta_plausivel": "Outra causa", "condicao_que_a_exclui": ["Q7_S1"]}
        decoded = references.decode_review(raw, catalog)
        C.review(decoded, context, questions)
        self.assertEqual(decoded["itens"][0]["fundamentos"], ["Segunda relação.\nCondição necessária."])
        self.assertEqual(decoded["itens"][6]["teste_de_unicidade"]["condicao_que_a_exclui"], questions[6]["pergunta"])
        self.assertEqual(raw["itens"][0]["fundamentos"], ["C0002"])

    def test_unknown_ids_paraphrases_and_other_questions_are_rejected(self):
        catalog = references.catalog("Texto original.", batch()["questoes"])
        raw = review()
        for row in raw["itens"]:
            row["fundamentos"] = ["C0001"]
            row["teste_de_unicidade"]["condicao_que_a_exclui"] = []
        for bad in ("C9999", "Uma paráfrase do documento"):
            invalid = copy.deepcopy(raw)
            invalid["itens"][0]["fundamentos"] = [bad]
            with self.assertRaisesRegex(ValueError, "não é ID"):
                references.decode_review(invalid, catalog)
        for bad in ("Q2_S1", "Q1_S999", "texto inventado"):
            invalid = copy.deepcopy(raw)
            invalid["itens"][0]["teste_de_unicidade"].update(
                outra_resposta_plausivel="Outra causa", condicao_que_a_exclui=[bad])
            with self.assertRaisesRegex(ValueError, "próprio enunciado"):
                references.decode_review(invalid, catalog)

    def test_no_exclusion_still_blocks_an_ambiguous_item(self):
        raw = review()
        for row in raw["itens"]:
            row["fundamentos"] = ["C0001"]
            row["teste_de_unicidade"]["condicao_que_a_exclui"] = []
        raw["itens"][8]["teste_de_unicidade"]["outra_resposta_plausivel"] = "Outra causa"
        decoded = references.decode_review(raw, references.catalog("Texto original.", batch()["questoes"]))
        self.assertEqual(C.rejected(decoded, resolution()), [9])

    def test_two_conditions_can_be_cited_without_inventing_a_joined_quote(self):
        questions = batch()["questoes"]
        questions[6]["pergunta"] = "Primeira condição. Segunda condição. Qual mecanismo?"
        raw = review()
        for row in raw["itens"]:
            row["fundamentos"] = ["C0001"]
            row["teste_de_unicidade"]["condicao_que_a_exclui"] = []
        raw["itens"][6]["teste_de_unicidade"].update(
            outra_resposta_plausivel="Outra causa", condicao_que_a_exclui=["Q7_S1", "Q7_S2"])
        decoded = references.decode_review(raw, references.catalog("Texto original.", questions))
        C.review(decoded, "Texto original.", questions)
        self.assertEqual(decoded["itens"][6]["teste_de_unicidade"]["condicao_que_a_exclui"],
                         "Primeira condição. Segunda condição.")


class RecoveryTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)

    def config(self, item):
        return Config.load(item=item, output=self.root / "runs" / item)

    def test_real_03_02_resumes_only_audit_and_keeps_seven_reserved_calls(self):
        config = self.config("03_02")
        shutil.copytree(FAILED, config.output)
        original = {p.name: p.read_bytes() for p in (config.output / "chamadas").glob("*.json")}
        fake = FakeLLM()
        runner = Runner(config, clients={"verificacao": fake}, progress=lambda *a, **k: None)
        original_call = fake.json

        def counted(*args, **kwargs):
            runner.budget.reserve()
            return original_call(*args, **kwargs)

        fake.json = counted
        with patch("pipeline.qa_research.qa_batch.runner.LLMClient", side_effect=AssertionError("Não repetir etapas")):
            summary = runner.run()
        self.assertEqual([s for s, p in fake.calls], ["verificacao"])
        self.assertEqual(summary["tentativas_reservadas"], 8)
        self.assertEqual(summary["status"], "aprovado_modelo")  # Auditor simulado, não certificação técnica.
        self.assertTrue(list((config.output / "migracoes").glob("*.json")))
        for name, content in original.items():
            self.assertEqual((config.output / "chamadas" / name).read_bytes(), content)
        catalog = read_json(config.output / "referencias" / "rodada_00.json")
        audit = read_json(config.output / "revisoes" / "rodada_00.json")["auditoria"]
        self.assertIn(audit["itens"][0]["fundamentos"][0], catalog["contexto"].values())

    def test_real_approved_legacy_lot_is_preserved_without_api_or_rewrites(self):
        config = self.config("02_02")
        shutil.copytree(APPROVED, config.output)
        files = {p.relative_to(config.output): p.read_bytes() for p in config.output.rglob("*") if p.is_file()}
        with patch("pipeline.qa_research.qa_batch.runner.LLMClient", side_effect=AssertionError("Não chamar API")):
            summary = Runner(config, progress=lambda *a, **k: None).run()
        self.assertEqual(summary["status"], "aprovado_modelo")
        for name, content in files.items():
            self.assertEqual((config.output / name).read_bytes(), content)

    def test_unknown_implementation_and_modified_models_cannot_migrate(self):
        config = self.config("03_02")
        shutil.copytree(FAILED, config.output)
        identity = read_json(config.output / "identidade.json")
        identity["implementation"] = "unknown"
        atomic_json(config.output / "identidade.json", identity)
        with self.assertRaisesRegex(ValueError, "mudaram"):
            Runner(config, progress=lambda *a, **k: None).run()
        identity = read_json(FAILED / "identidade.json")
        atomic_json(config.output / "identidade.json", identity)
        config.models["planejamento"] = "gpt-5-4-petrobras:low"
        with self.assertRaisesRegex(ValueError, "mudaram"):
            Runner(config, progress=lambda *a, **k: None).run()

    def test_changed_approved_questions_are_not_skipped_as_valid(self):
        config = self.config("02_02")
        shutil.copytree(APPROVED, config.output)
        qa = read_json(config.output / "qa.json")
        qa["questoes"][0]["resposta"] = "Alterado"
        atomic_json(config.output / "qa.json", qa)
        with self.assertRaisesRegex(ValueError, "inconsistente"):
            Runner(config, progress=lambda *a, **k: None).run()

    def test_all_continues_after_validation_failure_and_reports_progress(self):
        configs = [self.config(i) for i in ("03_02", "03_03")]
        calls, messages = [], []

        def run_item(config, **kwargs):
            calls.append(config.item)
            if config.item == "03_02":
                raise CallFailed("Referência inválida", kind="validacao", tag="qa9_verificacao")
            return {"status": "aprovado_modelo", "questoes_publicadas": 9}

        with patch("pipeline.qa_research.qa_all.preflight"):
            code, report = execute(configs, self.root / "runs", run_item=run_item,
                progress=lambda text, **kwargs: messages.append(text))
        self.assertEqual(code, 2)
        self.assertEqual(calls, ["03_02", "03_03"])
        self.assertEqual(report["falhas"], 1)
        self.assertEqual(report["aprovados"], 1)
        self.assertTrue(any("2/2" in m and "ETA" in m for m in messages))
        self.assertEqual(read_json(self.root / "runs/resumo_todos.json")["status"], "finalizado")

    def test_all_stops_for_credentials_and_keyboard_interrupt(self):
        configs = [self.config(i) for i in ("03_02", "03_03")]
        for error, expected in ((LLMError("401", kind="fatal"), 1), (KeyboardInterrupt(), 130)):
            calls = []

            def run_item(config, **kwargs):
                calls.append(config.item)
                raise error

            with patch("pipeline.qa_research.qa_all.preflight"):
                code, report = execute(configs, self.root / "runs", run_item=run_item, progress=lambda *a, **k: None)
            self.assertEqual(code, expected)
            self.assertEqual(calls, ["03_02"])
            self.assertEqual(report["status"], "interrompido")

    def test_all_collects_completed_and_interrupted_lots_without_local_secrets(self):
        configs = [self.config(i) for i in ("02_02", "03_02")]
        shutil.copytree(APPROVED, configs[0].output)
        shutil.copytree(FAILED, configs[1].output)
        (configs[0].output / ".env").write_text("TOKEN=segredo", encoding="utf-8")
        (configs[0].output / ".local").mkdir()
        (configs[0].output / ".local/cache.sqlite3").write_bytes(b"cache")
        root = self.root / "runs"
        target = collect_all(configs, root, self.root / "snapshot")
        self.assertEqual(read_json(target / "indice.json")["coletados"], 2)
        self.assertTrue((target / "02_02/qa.md").is_file())
        self.assertFalse((target / "03_02/qa.md").exists())
        for name, digest in read_json(target / "manifest_resultados.json")["files"].items():
            self.assertEqual(file_hash(target / name), digest)
        self.assertFalse(any(p.name in {".env", ".local"} for p in target.rglob("*")))
        with self.assertRaises(ValueError):
            collect_all(configs, root, target)

    def test_from_item_validation_and_completion_collection_command(self):
        configs, root = configurations(output_root=self.root / "runs", from_item="03_02")
        self.assertEqual(configs[0].item, "03_02")
        self.assertEqual(len(configs), 26)
        with self.assertRaisesRegex(ValueError, "não pertence"):
            configurations(from_item="99_99")
        with patch("sys.stdout", new_callable=io.StringIO) as stream:
            finished(root, "config.json")
            notice = stream.getvalue()
        for text in ("O código acabou de rodar no terminal 🙂", "qa_all collect", "git add --", "git commit", "git push"):
            self.assertIn(text, notice)


if __name__ == "__main__":
    unittest.main()
