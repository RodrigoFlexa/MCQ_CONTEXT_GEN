"""Progresso real, ETA ponderada e acompanhamento durante chamadas bloqueantes."""
import contextlib
import io
import os
import subprocess
import sys
import tempfile
import threading
import unittest
from pathlib import Path
from unittest.mock import patch

from pipeline.inventario.textutil import atomic_json
from pipeline.qa_research import document_progress as P
from pipeline.qa_research.document.common import ROOT


class DocumentProgressTests(unittest.TestCase):
    epoch = 1_700_000_000.

    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.output = Path(self.temp.name) / "run"
        self.items = [dict(id="01_01", area_id="01", subtopico="Indicadores", facets=4),
                      dict(id="02_02", area_id="02", subtopico="Produtos químicos", facets=12),
                      dict(id="03_01", area_id="03", subtopico="Offloading", facets=4)]

    def tearDown(self):
        self.temp.cleanup()

    def write(self, name, data, stamp):
        path = self.output / name
        atomic_json(path, data)
        stamp = stamp + self.epoch if stamp < self.epoch else stamp
        os.utime(path, (stamp, stamp))

    def scan(self, items=None, now=160., session_start=None):
        return P.snapshot(items or self.items, self.output, now=self.epoch + now,
                          session_start=self.epoch + session_start if session_start is not None else None)

    def root(self, rows, stamp=130., status="em_andamento", began=100.):
        self.write("identidade_lote.json", {"schema": "document-batch-run-v1"}, began)
        self.write("resumo_lote.json", {"items": rows, "status": status}, stamp)

    def summary(self, identifier, status="concluido", seconds=40., stamp=130., interruption=None):
        data = dict(status=status, session_seconds=seconds, interrupcao=interruption)
        self.write(identifier + "/resumo.json", data, stamp)
        return data

    def test_before_first_result_eta_is_unknown_and_no_directory_is_created(self):
        state = self.scan(now=120., session_start=100.)
        self.assertEqual(0, state["processed"])
        self.assertIsNone(state["eta_seconds"])
        self.assertIn("calculando", P.render(state))
        self.assertFalse(self.output.exists())

    def test_eta_uses_facets_and_subtracts_current_document_elapsed(self):
        done = self.summary("01_01", seconds=40.)
        self.root({"01_01": done})
        self.write("02_02/identidade.json", {}, 140.)
        self.write("02_02/progresso.json", {"etapa": "audit"}, 155.)
        state = self.scan()
        self.assertEqual(1, state["processed"])
        # 40s / 4 recortes * (12 + 4) - 20s do atual = 140s.
        self.assertEqual(140., state["eta_seconds"])
        self.assertEqual("auditoria", state["active"]["stage"])
        self.assertEqual(60., state["elapsed_seconds"])
        self.assertIn("Término estimado", P.render(state))

    def test_partial_export_during_audit_is_not_a_processed_document(self):
        done = self.summary("01_01")
        self.root({"01_01": done})
        self.write("02_02/identidade.json", {}, 140.)
        self.summary("02_02", status="parcial_com_pendencias", seconds=0., stamp=150.)
        state = self.scan()
        self.assertEqual(1, state["processed"])
        self.assertEqual(0, state["with_pending"])
        self.assertEqual("02_02", state["active"]["id"])

    def test_finished_partial_attempt_is_counted_separately(self):
        done = self.summary("01_01")
        partial = self.summary("02_02", status="parcial_com_pendencias", seconds=120.)
        self.root({"01_01": done, "02_02": partial})
        state = self.scan()
        self.assertEqual((2, 1, 1), (state["processed"], state["completed"], state["with_pending"]))
        self.assertEqual(40., state["eta_seconds"])

    def test_resume_keeps_complete_but_retries_old_partial(self):
        done = self.summary("01_01", stamp=50.)
        partial = self.summary("02_02", "parcial_com_pendencias", stamp=60.)
        self.root({"01_01": done, "02_02": partial}, stamp=70., status="parcial_com_pendencias", began=100.)
        self.write("02_02/identidade.json", {}, 110.)
        state = self.scan(now=120.)
        self.assertFalse(state["finished"])
        self.assertEqual(1, state["processed"])
        self.assertEqual("02_02", state["active"]["id"])

    def test_interruption_does_not_publish_an_eta_for_unstarted_documents(self):
        failed = self.summary("01_01", "interrompido", interruption="configuração do backend")
        self.root({"01_01": failed}, status="interrompido")
        state = self.scan()
        self.assertTrue(state["finished"])
        self.assertIsNone(state["eta_seconds"])
        self.assertEqual(0, state["sample_documents"])
        self.assertIn("execução encerrada", P.render(state))

    def test_overdue_last_document_does_not_show_false_zero_eta(self):
        done = self.summary("01_01")
        self.root({"01_01": done})
        self.write("02_02/identidade.json", {}, 140.)
        state = self.scan(self.items[:2], now=300.)
        self.assertEqual(1, state["remaining"])
        self.assertIsNone(state["eta_seconds"])
        self.assertIn("ultrapassou a média", state["eta_note"])

    def test_selected_scope_has_its_own_denominator_and_final_pending_notice(self):
        partial = self.summary("02_02", "parcial_com_pendencias")
        self.root({"02_02": partial}, status="parcial_com_pendencias")
        state = self.scan(self.items[1:2])
        self.assertEqual((1, 1, 0.), (state["processed"], state["total"], state["eta_seconds"]))
        self.assertIn("1/1", P.render(state))
        self.assertIn("tentativa encerrada", P.render(state))

    def test_corrupt_checkpoint_does_not_interrupt_snapshot(self):
        self.output.mkdir()
        (self.output / "resumo_lote.json").write_text("{incomplete", encoding="utf-8")
        state = self.scan()
        self.assertEqual(0, state["processed"])

    def test_timer_reports_while_main_thread_is_waiting_and_stops_on_exit(self):
        reports, tick = [], threading.Event()
        def emit(text):
            reports.append(text)
            if len(reports) >= 2:
                tick.set()
        monitor = P.Monitor(self.items, self.output, interval=.01, emit=emit)
        with monitor:
            self.assertTrue(tick.wait(1.), "O painel deveria atualizar mesmo sem retorno de chamada")
        self.assertFalse(monitor.thread.is_alive())
        self.assertGreaterEqual(len(reports), 3)  # início, periódico e término.

    def test_monitor_failure_cannot_prevent_work_or_mask_its_error(self):
        def unavailable(text):
            raise OSError("Saída do painel temporariamente indisponível")
        monitor = P.Monitor(self.items, self.output, interval=.01, emit=unavailable)
        with self.assertRaisesRegex(RuntimeError, "Erro original"):
            with monitor:
                raise RuntimeError("Erro original")
        self.assertFalse(monitor.thread.is_alive())

    def test_cli_watch_is_read_only_and_never_calls_backend(self):
        done = self.summary("01_01")
        self.root({"01_01": done}, status="concluido")
        with patch.object(P, "load_items", return_value=self.items[:1]), \
                patch.object(P.batch, "run_batch", side_effect=AssertionError("não chamar")), \
                contextlib.redirect_stdout(io.StringIO()) as console:
            self.assertEqual(0, P.main(["watch", "--output", str(self.output)]))
        self.assertIn("1/1", console.getvalue())

    def test_cli_run_retains_completion_message_and_return_commands(self):
        def run(*args, **kwargs):
            done = self.summary("01_01", stamp=2_000_000_000.)
            self.root({"01_01": done}, stamp=2_000_000_001., status="concluido")
            return {"status": "concluido", "items": {"01_01": done}}
        with patch.object(P, "load_items", return_value=self.items[:1]), \
                patch.object(P.batch, "run_batch", side_effect=run), \
                contextlib.redirect_stdout(io.StringIO()) as console:
            self.assertEqual(0, P.main(["run", "--output", str(self.output)]))
        self.assertIn("O código acabou de rodar no terminal", console.getvalue())
        self.assertIn("git push origin codex/qa-evidencias-verificadas", console.getvalue())
        self.assertIn("Documentos processados: 1/1", console.getvalue())

    def test_cli_rejects_invalid_interval_before_starting(self):
        for value in ("0", "-1", "nan", "inf"):
            with contextlib.redirect_stderr(io.StringIO()), self.assertRaises(SystemExit):
                P.main(["run", "--progress-interval", value])

    def test_watcher_loads_without_ml_or_backend_dependencies(self):
        result = subprocess.run([sys.executable, "-S", "-c",
            "import sys; from pipeline.qa_research.document_progress import load_items; "
            "assert len(load_items('pipeline/qa_research/pacotes/dez_areas_v1/lote.json')) == 40; "
            "assert not any(x in sys.modules for x in ['torch','numpy','sentence_transformers','openai']); "
            "print('stdlib-only')"], cwd=ROOT, capture_output=True, text=True)
        self.assertEqual(0, result.returncode, result.stderr)


if __name__ == "__main__":
    unittest.main()
