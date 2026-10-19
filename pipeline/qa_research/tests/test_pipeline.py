"""Testes funcionais com modelo simulado; não medem qualidade científica de LLM."""
import copy
import json
import tempfile
import unittest
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

from pipeline.inventario.llm import BudgetExceeded, CallFailed
from pipeline.inventario.textutil import read_json
from pipeline.qa_research import prompts as P
from pipeline.qa_research.config import Config, ROLES
from pipeline.qa_research.contracts import DOCUMENT_FLAGS, ATOM_FLAGS, QA_FLAGS
from pipeline.qa_research.engine import ResearchPipeline
from pipeline.qa_research.run import execute, inspect
from pipeline.qa_research.runtime import PersistentBudget


TEXT = ("A desaeração física pode não alcançar a especificação requerida. "
        "O tratamento químico complementar remove o oxigênio residual.")
QUOTE = "A desaeração física pode não alcançar a especificação requerida."


class FixtureIndex:
    def __init__(self):
        self.queries = []

    def build(self):
        return {"signature": "test-only-fixture", "corpus_bruto_completo": False,
                "cobertura": "fixture de teste"}

    def search(self, query, limit=8, exclude=(), neighbors=False):
        self.queries.append(query)
        return [{"chunk_id": "fixture:document:p1:w0", "texto": TEXT,
                 "collection": "fixture", "document_id": "document", "title": "Fixture sintética de teste",
                 "source_kind": "saved_selection", "page_ini": 1, "page_fim": 1}]


class FixtureModel:
    def __init__(self):
        self.requests = []
        self.reject_document = False
        self.reject_atom = False
        self.ambiguous = False
        self.fail_stage = None
        self.budget_stage = None
        self.opinion = False
        self.redundant = False

    def json(self, system, user, tag="", item=None, max_tokens=None, validate=None):
        stage = next(name for name in ("PLAN", "RESEARCH", "WRITE", "AUDIT_DOCUMENT", "EXTRACT",
                     "AUDIT_ATOMS", "GENERATE_QA", "ANSWER_BLIND", "AUDIT_QA", "NOVELTY")
                     if getattr(P, name) == system)
        payload = json.loads(user)
        self.requests.append((stage, copy.deepcopy(payload)))
        if self.fail_stage == stage:
            raise CallFailed("Falha simulada do teste")
        if self.budget_stage == stage:
            raise BudgetExceeded("Orçamento simulado do teste")
        method = getattr(self, stage.lower())
        data = method(payload)
        if validate:
            validate(data)
        return data

    @staticmethod
    def support(payload):
        return [{"evidencia_id": payload["evidencias"][0]["id"], "citacao": QUOTE}]

    @staticmethod
    def plan(payload):
        return {"eixos": {"servicos": ["Água de injeção"], "fenomenos_produtos": ["Oxigênio"],
                           "decisoes": ["Aplicação"]},
            "recortes": [{"titulo": "Complementação da desaeração", "servico": "Água de injeção",
                "fenomeno_produto": "Oxigênio", "decisao": "Aplicação",
                "ancoras_escopo": ["desaeração"], "consultas": ["desaeração oxigênio tratamento químico"],
                "justificativa": "Investigar função da complementação"}], "lacunas_planejamento": []}

    @staticmethod
    def research(payload):
        return {"acao": "redigir", "orientacao": "Preservar água de injeção como contexto", "consultas": [],
            "avaliacoes_fontes": [{"evidencia_id": e["id"], "pertinente": True,
                "tipo": "explicacao_tecnica", "contexto": "Água do mar para injeção", "limites": []}
                for e in payload["evidencias"]], "lacunas": [], "descobertas": []}

    @staticmethod
    def write(payload):
        return {"titulo": "Remoção de oxigênio", "blocos": [{"texto": TEXT,
                "fontes": [payload["evidencias"][0]["id"]]}], "lacunas": []}

    def audit_document(self, payload):
        return {"avaliacoes": [{"id": block["id"], **{k: not self.reject_document for k in DOCUMENT_FLAGS},
                "parecer": "Parecer simulado de teste", "suporte": self.support(payload)}
                for block in payload["capitulo"]["blocos"]], "lacunas": [], "consultas": []}

    def extract(self, payload):
        return {"unidades": [{"proposicao": "O tratamento químico complementa a desaeração física.",
            "tipo": "opiniao" if self.opinion else "mecanismo", "contexto": "Água do mar para injeção",
            "condicoes": ["Água do mar para injeção"], "limites": [],
            "blocos": [payload["capitulo_auditado"]["blocos"][0]["id"]], "jurisdicao": "", "edicao": "",
            "suporte": self.support(payload), "alvo": {"tipo": "procedimento",
                "resposta": "Tratamento químico complementar.", "variantes": [],
                "qualificador": "Após a desaeração física da água do mar para injeção"}}], "motivo": ""}

    def audit_atoms(self, payload):
        return {"avaliacoes": [{"id": unit["id"], **{k: not self.reject_atom for k in ATOM_FLAGS},
                                "parecer": "Parecer simulado de teste"} for unit in payload["unidades"]]}

    @staticmethod
    def generate_qa(payload):
        return {"status": "ok", "pergunta": "Que tratamento complementa a desaeração física da água do mar para injeção?",
                "resposta": payload["unidade"]["alvo"]["resposta"], "variantes": [], "motivo": ""}

    def answer_blind(self, payload):
        return {"status": "ambigua" if self.ambiguous else "respondida",
                "resposta": "Tratamento químico complementar", "outras_respostas": [],
                "condicoes_ausentes": ["Condição simulada ausente"] if self.ambiguous else [],
                "parecer": "Resolução simulada de teste", "suporte": self.support(payload)}

    def audit_qa(self, payload):
        return {**{k: not self.ambiguous for k in QA_FLAGS}, "outras_respostas": [],
                "parecer": "Auditoria simulada de teste"}

    def novelty(self, payload):
        return {"comparacoes": [{"id": u["id"], "classe": "redundante" if self.redundant else "distinta",
                "parecer": "Comparação simulada de teste"} for u in payload["anteriores"]]}


class PipelineTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(dir=Path(__file__).parent)
        self.root = Path(self.temp.name)
        self.config = Config(topic={"titulo": "Produtos químicos", "escopo": "Tratamento químico e desaeração da água do mar para injeção."},
            output=str(self.root / "output"), origins=[str(self.root / "input")], index_dir=str(self.root / "index"),
            initial_facets=1, max_facets=1, workers=1, max_repairs=0,
            target_qa=1, max_candidates=2, max_atoms_per_facet=2)
        self.index, self.model = FixtureIndex(), FixtureModel()
        self.clients = {role: self.model for role in ROLES}

    def tearDown(self):
        self.temp.cleanup()

    def run_pipeline(self, stage="completo"):
        return execute(self.config, stage=stage, clients=self.clients, index=self.index, progress=lambda _: None)

    def test_end_to_end_exports_only_short_qa_and_provenance(self):
        result = self.run_pipeline()
        self.assertEqual(result["qa_aprovadas_modelo"], 1)
        self.assertFalse(result["corpus_bruto_completo"])
        rows = [json.loads(line) for line in (Path(self.config.output) / "qa_aprovadas.jsonl").read_text(encoding="utf-8").splitlines()]
        self.assertEqual(len(rows), 1)
        self.assertIn("suporte", rows[0]["unidade"])
        self.assertEqual(rows[0]["validacao_humana"], "pendente")
        self.assertEqual((Path(self.config.output) / "qa.csv").read_text(encoding="utf-8-sig").splitlines()[0], "pergunta,resposta")

    def test_blind_payload_never_receives_reference_or_target(self):
        self.run_pipeline()
        blind = next(p for stage, p in self.model.requests if stage == "ANSWER_BLIND")
        self.assertEqual(set(blind), {"pergunta", "evidencias", "limite_palavras"})
        for stage, payload in self.model.requests:
            self.assertNotIn("exemplos", payload)
            self.assertNotIn("dataset", payload)

    def test_document_failure_prevents_extraction_and_qa(self):
        self.model.reject_document = True
        result = self.run_pipeline()
        self.assertEqual(result["capitulos_publicados"], 0)
        self.assertEqual(result["qa_aprovadas_modelo"], 0)
        self.assertNotIn("EXTRACT", [stage for stage, _ in self.model.requests])

    def test_atom_failure_does_not_reach_question_generator(self):
        self.model.reject_atom = True
        result = self.run_pipeline()
        self.assertEqual(result["unidades_elegiveis"], 0)
        self.assertNotIn("GENERATE_QA", [stage for stage, _ in self.model.requests])

    def test_opinion_is_not_exported_as_factual_qa(self):
        self.model.opinion = True
        result = self.run_pipeline()
        self.assertEqual(result["unidades"], 1)
        self.assertEqual(result["unidades_elegiveis"], 0)

    def test_ambiguity_rejects_item_despite_short_reference(self):
        self.model.ambiguous = True
        result = self.run_pipeline()
        self.assertEqual(result["qa_aprovadas_modelo"], 0)
        self.assertEqual(result["qa_por_status"], {"rejeitada": 1})

    def test_failed_blind_call_remains_pending_then_resumes(self):
        self.model.fail_stage = "ANSWER_BLIND"
        first = self.run_pipeline()
        self.assertTrue(first["pendencias_execucao"])
        self.assertEqual(first["qa_aprovadas_modelo"], 0)
        self.model.fail_stage = None
        second = self.run_pipeline()
        self.assertEqual(second["qa_aprovadas_modelo"], 1)
        self.assertEqual(sum(stage == "PLAN" for stage, _ in self.model.requests), 1)
        self.assertEqual(sum(stage == "GENERATE_QA" for stage, _ in self.model.requests), 1)

    def test_budget_interrupt_preserves_document_without_exporting_unverified_qa(self):
        self.model.budget_stage = "AUDIT_ATOMS"
        result = self.run_pipeline()
        self.assertIsNotNone(result["interrupcao"])
        self.assertEqual(result["capitulos_publicados"], 1)
        self.assertEqual(result["qa_aprovadas_modelo"], 0)

    def test_separate_research_and_qa_stages(self):
        research = self.run_pipeline("pesquisa")
        self.assertEqual(research["capitulos_publicados"], 1)
        self.assertNotIn("EXTRACT", [stage for stage, _ in self.model.requests])
        qa = self.run_pipeline("qa")
        self.assertEqual(qa["qa_aprovadas_modelo"], 1)

    def test_modified_configuration_refuses_incompatible_resume(self):
        self.run_pipeline("pesquisa")
        self.config.answer_words = 8
        with self.assertRaisesRegex(ValueError, "mudaram"):
            self.run_pipeline("qa")

    def test_resume_performs_no_duplicate_calls_and_budget_can_increase(self):
        self.run_pipeline()
        count = len(self.model.requests)
        self.config.max_calls += 20
        self.run_pipeline()
        self.assertEqual(len(self.model.requests), count)

    def test_qa_only_requires_prior_research(self):
        with self.assertRaisesRegex(ValueError, "pesquisa"):
            self.run_pipeline("qa")

    def test_output_cannot_overlap_inputs(self):
        self.config.output = self.config.origins[0]
        with self.assertRaisesRegex(ValueError, "separado"):
            self.config.validate()

    def test_config_rejects_removed_example_bank_parameters(self):
        with self.assertRaises(TypeError):
            Config(topic={}, output="x", external_examples="dataset.jsonl")

    def test_auditor_can_request_new_corpus_search_before_revision(self):
        self.config.max_repairs = 1
        self.config.research_rounds = 2
        original_audit = self.model.audit_document
        calls = []
        def audit(payload):
            calls.append(payload)
            result = original_audit(payload)
            if len(calls) == 1:
                for row in result["avaliacoes"]:
                    row["suportado"] = False
                result["consultas"] = ["consulta adicional"]
            return result
        original_search = self.index.search
        def search(query, **kwargs):
            rows = original_search(query, **kwargs)
            if query == "consulta adicional":
                rows[0] = {**rows[0], "chunk_id": "fixture:second:p2:w0", "document_id": "second",
                           "texto": TEXT + " Trecho complementar de teste."}
            return rows
        self.model.audit_document, self.index.search = audit, search
        result = self.run_pipeline()
        self.assertEqual(result["qa_aprovadas_modelo"], 1)
        self.assertIn("consulta adicional", self.index.queries)
        self.assertEqual(len(calls), 2)
        self.assertTrue(any(stage == "RESEARCH" and "pedido_auditor" in payload
                            for stage, payload in self.model.requests))

    def test_corpus_discovery_expands_research_and_duplicate_target_is_not_repeated(self):
        self.config.max_facets = 2
        self.config.target_qa = 2
        original_research = self.model.research
        def research(payload):
            result = original_research(payload)
            if payload["recorte"]["origem"] == "planejamento":
                result["descobertas"] = [{"titulo": "Monitoramento da desaeração", "servico": "Água de injeção",
                    "fenomeno_produto": "Oxigênio residual", "decisao": "Monitoramento",
                    "ancoras_escopo": ["desaeração"], "consultas": ["oxigênio residual monitoramento"],
                    "justificativa": "Investigar o contexto adicional identificado na fixture",
                    "suporte": self.model.support(payload)}]
            return result
        self.model.research = research
        result = self.run_pipeline()
        plan = read_json(Path(self.config.output) / "plano.json")
        self.assertEqual(len(plan["recortes"]), 2)
        self.assertEqual(plan["recortes"][1]["origem"], "descoberta_no_corpus")
        self.assertEqual(result["capitulos_publicados"], 2)
        self.assertEqual(result["qa_aprovadas_modelo"], 1)
        self.assertEqual(result["qa_por_status"].get("redundante"), 1)


class BudgetTests(unittest.TestCase):
    def test_corrupted_persisted_budget_is_rejected(self):
        with tempfile.TemporaryDirectory(dir=Path(__file__).parent) as temp:
            path = Path(temp) / "budget.json"
            for invalid in (-1, True, "2"):
                path.write_text(json.dumps({"tentativas_reservadas": invalid}), encoding="utf-8")
                with self.assertRaises(ValueError):
                    PersistentBudget(path, 10)

    def test_budget_is_cumulative_and_atomic_across_threads(self):
        with tempfile.TemporaryDirectory(dir=Path(__file__).parent) as temp:
            path = Path(temp) / "budget.json"
            budget = PersistentBudget(path, 9)
            def reserve(_):
                try:
                    budget.reserve()
                    return True
                except BudgetExceeded:
                    return False
            with ThreadPoolExecutor(max_workers=4) as pool:
                accepted = list(pool.map(reserve, range(20)))
            self.assertEqual(sum(accepted), 9)
            resumed = PersistentBudget(path, 10)
            resumed.reserve()
            with self.assertRaises(BudgetExceeded):
                resumed.reserve()
            self.assertEqual(read_json(path)["tentativas_reservadas"], 10)


if __name__ == "__main__":
    unittest.main()
