"""Fluxo/contratos de QA com respostas simuladas; nenhum teste chama a Azure."""
import copy
import contextlib
import io
import json
import tempfile
import unittest
from pathlib import Path
from types import SimpleNamespace
from unittest.mock import patch

from pipeline.inventario.llm import BudgetExceeded, LLMClient
from pipeline.inventario.textutil import atomic_json, read_json
from pipeline.qa_research.document.common import file_hash
from pipeline.qa_research.qa_batch import contracts as C, inputs, prompts
from pipeline.qa_research.qa_batch.__main__ import main
from pipeline.qa_research.qa_batch.config import Config, ROLES
from pipeline.qa_research.qa_batch.export import collect
from pipeline.qa_research.qa_batch.runner import Runner

PASSAGE = "Relação técnica simulada para testar o contrato, sem validade científica."


def plan():
    return {"status": "ok", "motivo": "", "itens": [
        {"id": i, "dificuldade": "facil" if i <= 3 else "media" if i <= 6 else "dificil",
         "alvo": f"Alvo de teste {i}", "resposta_esperada": f"Resposta de teste {i}",
         "condicoes_necessarias": [], "exigencia_cognitiva": "Exigência simulada",
         "fundamentos": [PASSAGE]} for i in C.IDS]}


def batch(ids=C.IDS, corrected=False):
    return {"status": "ok", "motivo": "", "questoes": [
        {"id": i, "dificuldade": "facil" if i <= 3 else "media" if i <= 6 else "dificil",
         "pergunta": f"Pergunta simulada {i}{' corrigida' if corrected else ''}?",
         "resposta": f"Resposta de teste {i}"} for i in ids]}


def resolution():
    return {"resolucoes": [{"id": i, "status": "respondida", "resposta": f"Resposta de teste {i}",
             "outras_respostas": [], "condicoes_faltantes": []} for i in C.IDS]}


def review():
    return {"itens": [{"id": i, "criterios": dict.fromkeys(C.CRITERIA, True), "motivo": "",
             "correcao_sugerida": "", "fundamentos": [PASSAGE],
             "teste_de_unicidade": {"outra_resposta_plausivel": "", "condicao_que_a_exclui": ""},
             "dificuldade_observada": C.expected_difficulty(i)} for i in C.IDS],
            "diversidade": {"ok": True, "ids_conflitantes": [], "motivo": ""}}


class FakeLLM:
    def __init__(self, *, fail=None, reject=False, always_reject=False, ambiguous=False, insufficient=None,
                 competing=False, wrong_level=False):
        self.calls = []
        self.fail, self.reject, self.always_reject = fail, reject, always_reject
        self.ambiguous, self.insufficient = ambiguous, insufficient
        self.competing, self.wrong_level = competing, wrong_level

    def response(self, stage, payload):
        if self.fail == stage:
            raise RuntimeError("Interrupção simulada em " + stage)
        if self.insufficient == stage:
            return {"status": "insuficiente", "motivo": "Falta fundamento para o ID 9",
                    "itens" if stage == "planejamento" else "questoes": []}
        if stage == "planejamento":
            return plan()
        if stage == "geracao":
            return batch()
        if stage == "refinamento":
            return batch(payload["ids_para_corrigir"], corrected=True)
        if stage == "resolucao_cega":
            result = resolution()
            if self.ambiguous:
                result["resolucoes"][6].update(status="ambigua", outras_respostas=["Outra causa"])
            return result
        if stage == "verificacao":
            result = review()
            if self.competing:
                result["itens"][6]["teste_de_unicidade"]["outra_resposta_plausivel"] = "Outra causa não excluída"
            if self.wrong_level:
                result["itens"][6]["dificuldade_observada"] = "media"
            repaired = "corrigida" in payload["lote"]["questoes"][6]["pergunta"]
            if self.always_reject or (self.reject and not repaired):
                result["itens"][6]["criterios"]["resposta_determinada"] = False
                result["itens"][6].update(motivo="Sinais insuficientes", correcao_sugerida="Delimitar condição")
            return result
        raise AssertionError(stage)

    def json(self, system, user, tag, validate, **kwargs):
        stage = tag.removeprefix("qa9_")
        payload = json.loads(user)
        self.calls.append((stage, payload))
        result = self.response(stage, payload)
        validate(result)
        return copy.deepcopy(result)


class BatchTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.config = Config.load(document=self.root / "documento.json", output=self.root / "saida")
        atomic_json(self.config.document, {"titulo": inputs.topic(self.config)["titulo_documento"],
            "capitulos": [{"titulo": "Relações", "grupo": "Teste", "blocos": [
                {"subtitulo": "Contrato", "texto": PASSAGE}]}]})

    def run_fake(self, fake=None):
        fake = fake or FakeLLM()
        result = Runner(self.config, clients=dict.fromkeys(ROLES, fake), progress=lambda *a, **k: None).run()
        return result, fake

    def test_defaults_and_scope(self):
        self.assertEqual(self.config.models, {"planejamento": "gpt-5-4-petrobras:high",
            "geracao": "gpt-5-4-petrobras:high", "verificacao": "gpt-5-4-petrobras:low",
            "refinamento": "gpt-5-4-petrobras:low"})
        scope = inputs.topic(self.config)["escopo_orientador"]
        self.assertTrue(scope.startswith("As questões podem abordar"))
        self.assertNotIn("{{", prompts.system("planejamento"))
        self.assertIn("português brasileiro", prompts.system("geracao"))

    def test_happy_flow_blind_payload_and_resume(self):
        summary, fake = self.run_fake()
        self.assertEqual(summary["status"], "aprovado_modelo")
        self.assertEqual(summary["questoes_publicadas"], 9)
        self.assertEqual(summary["validacao_humana"], "pendente")
        self.assertEqual([c[0] for c in fake.calls], ["planejamento", "geracao", "resolucao_cega", "verificacao"])
        blind_payload = fake.calls[2][1]
        self.assertNotIn("plano", blind_payload)
        self.assertEqual(set(blind_payload["questoes"][0]), {"id", "pergunta"})
        final = read_json(self.config.output / "qa.json")
        self.assertEqual(set(final["questoes"][0]), {"id", "dificuldade", "pergunta", "resposta"})
        self.assertTrue((self.config.output / "qa.csv").is_file())
        self.assertNotIn("fundamentos", (self.config.output / "qa.md").read_text(encoding="utf-8"))
        summary, cached = self.run_fake(FakeLLM(fail="planejamento"))
        self.assertEqual(summary["status"], "aprovado_modelo")
        self.assertEqual(cached.calls, [])

    def test_refine_subset_then_verify_every_question_again(self):
        summary, fake = self.run_fake(FakeLLM(reject=True))
        self.assertEqual(summary["status"], "aprovado_modelo")
        self.assertEqual(summary["refinamentos"], 1)
        self.assertEqual(len(fake.calls), 7)
        repair = next(p for s, p in fake.calls if s == "refinamento")
        self.assertEqual(repair["ids_para_corrigir"], [7])
        self.assertEqual(len(fake.calls[-2][1]["questoes"]), 9)
        self.assertEqual(len(fake.calls[-1][1]["lote"]["questoes"]), 9)
        final = read_json(self.config.output / "qa.json")["questoes"]
        self.assertEqual(final[0], batch()["questoes"][0])
        self.assertIn("corrigida", final[6]["pergunta"])

    def test_rejection_and_ambiguous_blind_result_block_publication(self):
        self.config.data["max_refinements"] = 0
        summary, _ = self.run_fake(FakeLLM(ambiguous=True))
        self.assertEqual(summary["status"], "pendente_revisao")
        self.assertEqual(summary["ids_pendentes"], [7])
        self.assertFalse((self.config.output / "qa.json").exists())

    def test_audit_findings_block_publication_even_with_all_booleans_true(self):
        self.config.data["max_refinements"] = 0
        for field in ("competing", "wrong_level"):
            with self.subTest(field=field):
                self.config.output = self.root / field
                summary, fake = self.run_fake(FakeLLM(**{field: True}))
                self.assertEqual(summary["status"], "pendente_revisao")
                self.assertEqual(summary["ids_pendentes"], [7])
                self.assertEqual(len(fake.calls), 4)
                self.assertFalse((self.config.output / "qa.json").exists())
                audit = read_json(self.config.output / "revisoes" / "rodada_00.json")["auditoria"]
                self.assertTrue(all(audit["itens"][6]["criterios"].values()))

    def test_still_bad_after_refinement(self):
        summary, fake = self.run_fake(FakeLLM(always_reject=True))
        self.assertEqual(summary["status"], "pendente_revisao")
        self.assertEqual(len(fake.calls), 7)
        self.assertFalse((self.config.output / "qa.md").exists())

    def test_insufficient_stops_without_partial_lot(self):
        for stage in ("planejamento", "geracao", "refinamento"):
            with self.subTest(stage=stage):
                self.config.output = self.root / stage
                summary, fake = self.run_fake(FakeLLM(reject=True, insufficient=stage))
                self.assertNotEqual(summary["status"], "aprovado_modelo")
                self.assertFalse((self.config.output / "qa.json").exists())
                self.assertEqual(fake.calls[-1][0], stage)

    def test_interrupted_run_resumes_after_planning(self):
        with self.assertRaisesRegex(RuntimeError, "geracao"):
            self.run_fake(FakeLLM(fail="geracao"))
        self.assertEqual(read_json(self.config.output / "resumo.json")["status"], "interrompido")
        summary, fake = self.run_fake()
        self.assertEqual(summary["status"], "aprovado_modelo")
        self.assertEqual(fake.calls[0][0], "geracao")

    def test_changed_context_or_models_cannot_reuse_output(self):
        self.run_fake()
        self.config.models["geracao"] = "gpt-5-4-petrobras:low"
        with self.assertRaisesRegex(ValueError, "mudaram"):
            self.run_fake()
        self.config.models["geracao"] = "gpt-5-4-petrobras:high"
        value = read_json(self.config.document)
        value["capitulos"][0]["blocos"][0]["texto"] += " Alteração."
        atomic_json(self.config.document, value)
        with self.assertRaisesRegex(ValueError, "mudaram"):
            self.run_fake()

    def test_checkpoint_tampering_detected(self):
        self.run_fake()
        path = next((self.config.output / "chamadas").glob("*.json"))
        value = read_json(path)
        value["response"] = {"adulterado": True}
        atomic_json(path, value)
        with self.assertRaisesRegex(ValueError, "Checkpoint alterado"):
            self.run_fake()

    def test_document_not_complete_wrong_topic_or_snapshot_tampered(self):
        atomic_json(self.config.document.parent / "resumo.json", {"status": "parcial_com_pendencias"})
        with self.assertRaisesRegex(ValueError, "conclusão"):
            inputs.document(self.config, inputs.topic(self.config))
        atomic_json(self.config.document.parent / "resumo.json", {"status": "concluido"})
        atomic_json(self.config.document.parent / "manifest_resultados.json", {
            "schema": "document-results-v2", "files": {"documento.json": "hash_alterado"}})
        with self.assertRaisesRegex(ValueError, "manifesto"):
            inputs.document(self.config, inputs.topic(self.config))

    def test_raw_dataset_or_provenance_is_not_accepted_as_knowledge(self):
        atomic_json(self.config.document, {"questoes": [], "referencias": []})
        with self.assertRaises(ValueError):
            inputs.document(self.config, inputs.topic(self.config))

    def test_partial_document_allowed_only_after_consolidation(self):
        summary = {"status": "parcial_com_pendencias", "consolidacao_completa": True,
                   "etapas_pendentes": [], "interrupcao": None, "recortes_pendentes": ["compatibilidade"]}
        atomic_json(self.config.document.parent / "resumo.json", summary)
        source = inputs.document(self.config, inputs.topic(self.config))
        self.assertEqual(source["recortes_documentais_pendentes"], ["compatibilidade"])
        self.assertNotIn("recortes_documentais_pendentes", inputs.payload(inputs.topic(self.config), source))
        summary["interrupcao"] = "timeout"
        atomic_json(self.config.document.parent / "resumo.json", summary)
        with self.assertRaisesRegex(ValueError, "conclusão"):
            inputs.document(self.config, inputs.topic(self.config))

    def test_wrong_topic_cannot_supply_context(self):
        value = read_json(self.config.document)
        value["titulo"] = "Outro tema"
        atomic_json(self.config.document, value)
        with self.assertRaisesRegex(ValueError, "tópico"):
            inputs.document(self.config, inputs.topic(self.config))

    def test_collect_whitelist_hashes_and_immutable_destination(self):
        self.run_fake()
        (self.config.output / ".env").write_text("TOKEN=segredo", encoding="utf-8")
        (self.config.output / ".local").mkdir()
        (self.config.output / ".local" / "cache.sqlite3").write_bytes(b"local")
        target = collect(self.config.output, self.root / "snapshot")
        manifest = read_json(target / "manifest_resultados.json")
        self.assertEqual(manifest["schema"], "qa-batch-results-v1")
        self.assertFalse((target / ".env").exists())
        self.assertFalse((target / ".local").exists())
        for name, digest in manifest["files"].items():
            self.assertEqual(file_hash(target / name), digest)
        with self.assertRaises(ValueError):
            collect(self.config.output, target)

    def test_collect_cannot_claim_approval_for_changed_qa(self):
        self.run_fake()
        changed = read_json(self.config.output / "qa.json")
        changed["questoes"][0]["resposta"] = "Resposta alterada após a auditoria"
        atomic_json(self.config.output / "qa.json", changed)
        with self.assertRaisesRegex(ValueError, "inconsistente"):
            collect(self.config.output, self.root / "alterado")
        self.assertFalse((self.root / "alterado").exists())

    def test_cli_offline_plan_and_check_no_model_client(self):
        with patch("pipeline.qa_research.qa_batch.runner.LLMClient", side_effect=AssertionError("Não chamar API")):
            with contextlib.redirect_stdout(io.StringIO()) as output:
                code = main(["plan", "--document", str(self.root / "futuro.json")])
            self.assertEqual(code, 0)
            self.assertFalse(json.loads(output.getvalue())["documento_disponivel"])
            with contextlib.redirect_stdout(io.StringIO()) as output:
                code = main(["check", "--document", str(self.config.document)])
            self.assertEqual(code, 0)
            self.assertEqual(json.loads(output.getvalue())["entrada"]["blocos"], 1)

    def test_cli_completion_notice_and_git_commands(self):
        summary = {"status": "aprovado_modelo"}
        with patch("pipeline.qa_research.qa_batch.runner.run", return_value=summary):
            with contextlib.redirect_stdout(io.StringIO()) as output:
                code = main(["run"])
        self.assertEqual(code, 0)
        notice = output.getvalue()
        for required in ("O código acabou de rodar no terminal 🙂", " collect --output", "git add --", "git commit", "git push"):
            self.assertIn(required, notice)

    def test_clients_closed_if_later_client_creation_fails(self):
        first = FakeLLM()
        first.identity = {"provider": "azure"}
        closed = []
        first.close = lambda: closed.append(True)
        with patch("pipeline.qa_research.qa_batch.runner.LLMClient", side_effect=[first, RuntimeError("Configuração")]):
            with self.assertRaisesRegex(RuntimeError, "Configuração"):
                Runner(self.config, progress=lambda *a, **k: None).run()
        self.assertEqual(closed, [True])

    def test_actual_sdk_arguments_and_cumulative_budget(self):
        calls = []
        fake = FakeLLM(reject=True)

        def factory(model, effort, cache_path, log_path, **kwargs):
            role = cache_path.stem

            def create(**request):
                calls.append((role, request))
                payload = json.loads(request["messages"][1]["content"])
                stage = "resolucao_cega" if role == "verificacao" and "questoes" in payload else role
                result = fake.response(stage, payload)
                return SimpleNamespace(choices=[SimpleNamespace(finish_reason="stop",
                       message=SimpleNamespace(content=json.dumps(result)))],
                       usage=SimpleNamespace(prompt_tokens=100, completion_tokens=100))

            sdk = SimpleNamespace(chat=SimpleNamespace(completions=SimpleNamespace(create=create)))
            return LLMClient(model, effort, cache_path, log_path, client=sdk, **kwargs)

        with patch("pipeline.qa_research.qa_batch.runner.LLMClient", side_effect=factory):
            result = Runner(self.config, progress=lambda *a, **k: None).run()
        self.assertEqual(result["status"], "aprovado_modelo")
        self.assertEqual(result["tentativas_reservadas"], 7)
        for role, request in calls:
            self.assertEqual(request["model"], "gpt-5-4-petrobras")
            self.assertEqual(request["reasoning_effort"], "high" if role in {"planejamento", "geracao"} else "low")
        with patch("pipeline.qa_research.qa_batch.runner.LLMClient", side_effect=AssertionError("Não repetir")):
            result = Runner(self.config, progress=lambda *a, **k: None).run()
        self.assertEqual(result["tentativas_reservadas"], 7)

    def test_budget_does_not_reset_on_resume(self):
        self.config.output.mkdir()
        atomic_json(self.config.output / "orcamento.json", {"tentativas_reservadas": 40, "limite": 40})

        def factory(model, effort, cache_path, log_path, **kwargs):
            sdk = SimpleNamespace(chat=SimpleNamespace(completions=SimpleNamespace(
                create=lambda **k: self.fail("Orçamento deveria impedir a API"))))
            return LLMClient(model, effort, cache_path, log_path, client=sdk, **kwargs)

        with patch("pipeline.qa_research.qa_batch.runner.LLMClient", side_effect=factory):
            with self.assertRaises(BudgetExceeded):
                Runner(self.config, progress=lambda *a, **k: None).run()
        self.assertEqual(read_json(self.config.output / "orcamento.json")["tentativas_reservadas"], 40)


class ContractTests(unittest.TestCase):
    def test_quotas_ids_levels_fields_and_answer_length(self):
        mutations = [lambda d: d["questoes"].pop(),
                     lambda d: d["questoes"][0].update(id=True),
                     lambda d: d["questoes"][8].update(id=1),
                     lambda d: d["questoes"][4].update(dificuldade="facil"),
                     lambda d: d["questoes"][0].update(resposta="palavra " * 51),
                     lambda d: d["questoes"][0].update(referencias=[]),
                     lambda d: d["questoes"][1].update(pergunta=d["questoes"][0]["pergunta"])]
        for mutate in mutations:
            data = batch()
            mutate(data)
            with self.assertRaises(ValueError):
                C.questions(data)
        data = batch()
        data["questoes"][0]["resposta"] = "palavra " * 50
        C.questions(data)

    def test_plan_quotes_must_be_literal(self):
        C.plan(plan(), PASSAGE)
        with self.assertRaisesRegex(ValueError, "literal"):
            C.plan(plan(), "Texto sem o fundamento citado")

    def test_discriminating_condition_must_be_in_question_not_only_context(self):
        data = review()
        check = data["itens"][6]["teste_de_unicidade"]
        check.update(outra_resposta_plausivel="Outra causa", condicao_que_a_exclui=PASSAGE)
        with self.assertRaisesRegex(ValueError, "literal da pergunta"):
            C.review(data, PASSAGE, batch()["questoes"])
        check["condicao_que_a_exclui"] = "simulada 7"
        C.review(data, PASSAGE, batch()["questoes"])
        self.assertEqual(C.rejected(data, resolution()), [])

    def test_competing_response_without_exclusion_is_rejected(self):
        data = review()
        data["itens"][8]["teste_de_unicidade"]["outra_resposta_plausivel"] = "Outra explicação"
        C.review(data, PASSAGE, batch()["questoes"])
        self.assertEqual(C.rejected(data, resolution()), [9])

    def test_observed_difficulty_does_not_inherit_requested_level(self):
        for observed in ("facil", "media", "indeterminada"):
            with self.subTest(observed=observed):
                data = review()
                data["itens"][7]["dificuldade_observada"] = observed
                C.review(data, PASSAGE, batch()["questoes"])
                self.assertEqual(C.rejected(data, resolution()), [8])

    def test_audit_requires_new_fields_and_valid_observed_level(self):
        for field in ("teste_de_unicidade", "dificuldade_observada"):
            data = review()
            del data["itens"][0][field]
            with self.assertRaises(ValueError):
                C.review(data, PASSAGE, batch()["questoes"])
        data = review()
        data["itens"][0]["dificuldade_observada"] = "alta"
        with self.assertRaisesRegex(ValueError, "Dificuldade observada"):
            C.review(data, PASSAGE, batch()["questoes"])
        data = review()
        data["itens"][0]["teste_de_unicidade"]["condicao_que_a_exclui"] = "simulada 1"
        with self.assertRaisesRegex(ValueError, "resposta concorrente"):
            C.review(data, PASSAGE, batch()["questoes"])

    def test_incomplete_audit_boolean_conflicts_and_blind_consistency(self):
        invalid = review()
        invalid["itens"].pop()
        with self.assertRaises(ValueError):
            C.review(invalid, PASSAGE, batch()["questoes"])
        invalid = review()
        invalid["itens"][0]["criterios"]["foco"] = "true"
        with self.assertRaises(ValueError):
            C.review(invalid, PASSAGE, batch()["questoes"])
        invalid = review()
        invalid["diversidade"] = {"ok": False, "ids_conflitantes": [1], "motivo": "Repetição"}
        with self.assertRaises(ValueError):
            C.review(invalid, PASSAGE, batch()["questoes"])
        invalid = resolution()
        invalid["resolucoes"][0]["outras_respostas"] = ["Outra conclusão"]
        with self.assertRaises(ValueError):
            C.blind(invalid)


if __name__ == "__main__":
    unittest.main()
