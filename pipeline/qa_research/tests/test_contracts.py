"""Fixtures artificiais locais para testar contratos, nunca usadas nos prompts."""
from copy import deepcopy
import unittest
import unicodedata

from pipeline.qa_research import contracts as c


def evidence():
    return [
        {"id": "E1", "texto": "No ensaio, o produto Q reduziu a taxa em aço. A dosagem foi 5 mg/L.", "idioma": "pt"},
        {"id": "E2", "texto": "A formulação R não foi avaliada em aço.", "idioma": "pt"},
    ]


def support(identity="E1", quote="o produto Q reduziu a taxa em aço."):
    return [{"evidencia_id": identity, "citacao": quote}]


def topic():
    return {"titulo": "Produtos", "escopo": "Produtos químicos; água de injeção; compatibilidade e monitoramento."}


def facet():
    return {"titulo": "Compatibilidade em água", "servico": "água de injeção",
            "fenomeno_produto": "produtos químicos", "decisao": "compatibilidade",
            "ancoras_escopo": ["água de injeção", "compatibilidade"],
            "consultas": ["compatibilidade água injeção", "chemical compatibility injection water"],
            "justificativa": "Investigar as combinações relatadas."}


def planning():
    return {"eixos": {"servicos": ["água de injeção"],
                     "fenomenos_produtos": ["produtos químicos"], "decisoes": ["compatibilidade"]},
            "recortes": [facet()], "lacunas_planejamento": []}


def researching():
    return {"acao": "redigir", "orientacao": "Preservar as condições do ensaio.",
            "consultas": [], "lacunas": [], "descobertas": [],
            "avaliacoes_fontes": [
                {"evidencia_id": "E1", "pertinente": True, "tipo": "resultado_experimental",
                 "contexto": "Ensaio em aço.", "limites": ["Resultado local."]},
                {"evidencia_id": "E2", "pertinente": False, "tipo": "explicacao_tecnica",
                 "contexto": "Outra formulação.", "limites": []}]}


def document():
    return {"titulo": "Ensaio", "blocos": [
        {"texto": "No ensaio em aço, Q reduziu a taxa.", "fontes": ["E1"]},
        {"texto": "R não foi avaliado em aço.", "fontes": ["E2"]}], "lacunas": []}


def blocks():
    return [{"id": "B1", **document()["blocos"][0]}, {"id": "B2", **document()["blocos"][1]}]


def document_audit():
    return {"avaliacoes": [
        {"id": "B1", **dict.fromkeys(c.DOCUMENT_FLAGS, True),
         "parecer": "Corresponde ao ensaio.", "suporte": support()},
        {"id": "B2", **dict.fromkeys(c.DOCUMENT_FLAGS, True),
         "parecer": "Preserva a negação.",
         "suporte": support("E2", "R não foi avaliada em aço.")}],
        "lacunas": [], "consultas": []}


def unit():
    return {"proposicao": "No ensaio, o produto Q reduziu a taxa em aço.",
            "tipo": "resultado_experimental", "contexto": "Ensaio em aço.",
            "condicoes": ["Ensaio descrito."], "limites": ["Sem extrapolação."],
            "blocos": ["B1"], "jurisdicao": "", "edicao": "", "suporte": support(),
            "alvo": {"tipo": "entidade", "resposta": "produto Q", "variantes": ["Q"],
                     "qualificador": "No ensaio em aço."}}


def units():
    return [{"id": "U1", **unit()}]


def extracted():
    return {"unidades": [unit()], "motivo": ""}


def atoms_audit():
    return {"avaliacoes": [{"id": "U1", **dict.fromkeys(c.ATOM_FLAGS, True),
                            "parecer": "O alvo corresponde ao resultado delimitado."}]}


def question():
    return {"status": "ok", "pergunta": "No ensaio descrito em aço, qual produto reduziu a taxa?",
            "resposta": "produto Q", "variantes": ["Q"], "motivo": ""}


def blind():
    return {"status": "respondida", "resposta": "Q", "outras_respostas": [],
            "condicoes_ausentes": [], "parecer": "Resultado expresso no original.", "suporte": support()}


def qa_audit():
    return {**dict.fromkeys(c.QA_FLAGS, True), "outras_respostas": [],
            "parecer": "A pergunta delimita o ensaio e tem alvo sustentado."}


class SupportTests(unittest.TestCase):
    def test_unicode_and_whitespace_only_normalization(self):
        original = "A ação\n  não aumentou a taxa; foi 5 mg/L."
        ev = [{"id": "E1", "texto": original}]
        quote = unicodedata.normalize("NFD", "ação não aumentou a taxa;")
        rows = support(quote=quote)
        before = deepcopy((rows, ev))
        self.assertIs(c.validate_support(rows, ev), rows)
        self.assertEqual((rows, ev), before)

    def test_rejects_reordering_ellipsis_translation_case_and_punctuation_changes(self):
        for quote in ["Q o produto reduziu a taxa", "o produto Q ... em aço.",
                      "product Q reduced the rate", "O PRODUTO Q", "o produto Q reduziu a taxa em aço!",
                      "o produto Q reduziu a taxa em aco.", "o produto Q reduziu a taxa em aço A dosagem"]:
            with self.subTest(quote=quote), self.assertRaises(ValueError):
                c.validate_support(support(quote=quote), evidence())

    def test_exact_ids_and_quote_origin(self):
        for identity in ["e1", " E1", "E1 ", "E3"]:
            with self.subTest(identity=identity), self.assertRaises(ValueError):
                c.validate_support(support(identity=identity), evidence())
        with self.assertRaises(ValueError):
            c.validate_support(support(identity="E2"), evidence())

    def test_rejects_duplicate_but_accepts_distinct_spans_same_source(self):
        with self.assertRaises(ValueError):
            c.validate_support(support() * 2, evidence())
        rows = support() + support(quote="A dosagem foi 5 mg/L.")
        c.validate_support(rows, evidence())

    def test_empty_support_is_explicitly_optional(self):
        with self.assertRaises(ValueError):
            c.validate_support([], evidence())
        self.assertEqual(c.validate_support([], evidence(), required=False), [])

    def test_bad_types_and_source_ids_raise_valueerror(self):
        cases = [None, {}, [True], [{"evidencia_id": "E1", "citacao": ""}],
                 [{"evidencia_id": "E1", "citacao": 1}],
                 [{"evidencia_id": "E1", "citacao": "aço", "extra": True}]]
        for rows in cases:
            with self.subTest(rows=rows), self.assertRaises(ValueError):
                c.validate_support(rows, evidence())
        with self.assertRaises(ValueError):
            c.validate_support(support(), evidence() + [evidence()[0]])


class ContractTests(unittest.TestCase):
    def validators(self):
        return [
            (planning(), lambda d: c.plan(d, topic(), 3)),
            (researching(), lambda d: c.research(d, evidence(), topic(), 3)),
            (document(), lambda d: c.document(d, evidence())),
            (document_audit(), lambda d: c.audit_document(d, blocks(), evidence())),
            (extracted(), lambda d: c.atoms(d, blocks(), evidence(), 3, 8)),
            (atoms_audit(), lambda d: c.audit_atoms(d, units())),
            (question(), lambda d: c.question(d, unit(), 8)),
            (blind(), lambda d: c.blind_answer(d, evidence(), 8)),
            (qa_audit(), c.audit_qa),
            ({"comparacoes": [{"id": "U0", "classe": "distinta", "parecer": "Outro alvo."}]},
             lambda d: c.novelty(d, ["U0"]))]

    def test_every_role_accepts_valid_payload_without_mutation(self):
        for data, validate in self.validators():
            original = deepcopy(data)
            with self.subTest(role=validate):
                self.assertIs(validate(data), data)
                self.assertEqual(data, original)

    def test_all_root_schemas_are_closed_and_required(self):
        for data, validate in self.validators():
            with self.subTest(role=validate, error="extra"), self.assertRaises(ValueError):
                validate({**data, "aprovado": True})
            missing = deepcopy(data)
            del missing[next(iter(missing))]
            with self.subTest(role=validate, error="missing"), self.assertRaises(ValueError):
                validate(missing)

    def test_boolean_fields_do_not_coerce_strings_numbers_or_null(self):
        for value in ["true", "false", 1, 0, None, [], {}]:
            for factory, flags, runner in [
                (document_audit, c.DOCUMENT_FLAGS, lambda d: c.audit_document(d, blocks(), evidence())),
                (atoms_audit, c.ATOM_FLAGS, lambda d: c.audit_atoms(d, units())),
                (qa_audit, c.QA_FLAGS, c.audit_qa)]:
                for flag in flags:
                    data = factory()
                    row = data["avaliacoes"][0] if "avaliacoes" in data else data
                    row[flag] = value
                    with self.subTest(value=value, flag=flag), self.assertRaises(ValueError):
                        runner(data)
            data = researching()
            data["avaliacoes_fontes"][0]["pertinente"] = value
            with self.subTest(value=value), self.assertRaises(ValueError):
                c.research(data, evidence(), topic(), 3)

    def test_false_audit_flags_remain_valid_rejections(self):
        doc = document_audit()
        doc["avaliacoes"][0]["suportado"] = False
        doc["avaliacoes"][0]["suporte"] = []
        c.audit_document(doc, blocks(), evidence())
        item = qa_audit()
        item["univoca_no_contexto"] = False
        item["outras_respostas"] = ["produto R"]
        c.audit_qa(item)

    def test_audits_require_every_id_once_even_when_counts_match(self):
        for row_change in ["duplicate", "unknown", "missing"]:
            doc = document_audit()
            if row_change == "duplicate":
                doc["avaliacoes"][1] = deepcopy(doc["avaliacoes"][0])
            elif row_change == "unknown":
                doc["avaliacoes"][1]["id"] = "B999"
            else:
                doc["avaliacoes"].pop()
            with self.subTest(row_change=row_change), self.assertRaises(ValueError):
                c.audit_document(doc, blocks(), evidence())
        for ids in [[], ["U0", "U0"], ["U0", "U9"]]:
            data = {"comparacoes": [{"id": i, "classe": "distinta", "parecer": "Outro alvo."} for i in ids]}
            with self.subTest(ids=ids), self.assertRaises(ValueError):
                c.novelty(data, ["U0", "U1"])
        data = atoms_audit()
        data["avaliacoes"][0]["id"] = "u1"
        with self.assertRaises(ValueError):
            c.audit_atoms(data, units())

    def test_plan_scope_anchors_are_literal_not_semantic_paraphrases(self):
        data = planning()
        data["recortes"][0]["ancoras_escopo"] = ["água para injetar"]
        with self.assertRaises(ValueError):
            c.plan(data, topic(), 3)
        with self.assertRaises(ValueError):
            c.plan(planning(), topic(), True)
        data = planning()
        data["recortes"] *= 2
        with self.assertRaises(ValueError):
            c.plan(data, topic(), 3)

    def test_research_discovery_has_same_facet_and_literal_support_contract(self):
        data = researching()
        data["descobertas"] = [{**facet(), "suporte": support()}]
        c.research(data, evidence(), topic(), 3)
        data["descobertas"][0]["suporte"] = support(quote="Q sempre funciona")
        with self.assertRaises(ValueError):
            c.research(data, evidence(), topic(), 3)

    def test_research_decisions_and_limits(self):
        data = researching()
        data["acao"] = "buscar"
        with self.assertRaises(ValueError):
            c.research(data, evidence(), topic(), 3)
        data["consultas"] = ["contexto do ensaio"]
        c.research(data, evidence(), topic(), 3)
        data["consultas"] = ["a", "b", "c", "d"]
        with self.assertRaises(ValueError):
            c.research(data, evidence(), topic(), 3)
        data = researching()
        for row in data["avaliacoes_fontes"]:
            row["pertinente"] = False
        with self.assertRaises(ValueError):
            c.research(data, evidence(), topic(), 3)
        data["acao"] = "insuficiente"
        c.research(data, evidence(), topic(), 3)

    def test_research_cannot_skip_or_duplicate_source_assessment(self):
        for rows in [researching()["avaliacoes_fontes"][:1],
                     [researching()["avaliacoes_fontes"][0]] * 2]:
            data = researching()
            data["avaliacoes_fontes"] = rows
            with self.subTest(rows=rows), self.assertRaises(ValueError):
                c.research(data, evidence(), topic(), 3)

    def test_block_sources_and_audits_cannot_substitute_unlinked_evidence(self):
        data = document()
        data["blocos"][0]["fontes"] = ["E3"]
        with self.assertRaises(ValueError):
            c.document(data, evidence())
        data = document_audit()
        data["avaliacoes"][0]["suporte"] = support("E2", "R não foi avaliada em aço.")
        with self.assertRaises(ValueError):
            c.audit_document(data, blocks(), evidence())
        data = document_audit()
        data["avaliacoes"][0]["suporte"] = []
        with self.assertRaises(ValueError):
            c.audit_document(data, blocks(), evidence())

    def test_atoms_cannot_cite_evidence_outside_their_block_sources(self):
        data = extracted()
        data["unidades"][0]["suporte"] = support("E2", "R não foi avaliada em aço.")
        with self.assertRaises(ValueError):
            c.atoms(data, blocks(), evidence(), 3, 8)
        data["unidades"][0]["blocos"] = ["B1", "B2"]
        c.atoms(data, blocks(), evidence(), 3, 8)

    def test_atoms_require_existing_block_ids_and_allow_empty_lots(self):
        data = extracted()
        data["unidades"][0]["blocos"] = ["B99"]
        with self.assertRaises(ValueError):
            c.atoms(data, blocks(), evidence(), 3, 8)
        c.atoms({"unidades": [], "motivo": "Sem alvo curto."}, blocks(), evidence(), 3, 8)

    def test_norm_without_metadata_can_be_extracted_for_context(self):
        data = extracted()
        data["unidades"][0]["tipo"] = "requisito_normativo"
        c.atoms(data, blocks(), evidence(), 3, 8)

    def test_numeric_corruption_is_not_reconstructed(self):
        for value in ["<NUMBER> mg/L", "< number > mg/L", "[VALOR] mg/L", "{value} mg/L",
                      "XXX mg/L", "__ mg/L", "TBD mg/L", "?? mg/L"]:
            data = extracted()
            data["unidades"][0]["alvo"].update(tipo="valor", resposta=value)
            with self.subTest(value=value), self.assertRaises(ValueError):
                c.atoms(data, blocks(), evidence(), 3, 8)
        data = extracted()
        data["unidades"][0]["alvo"].update(tipo="valor", resposta="5 mg/L", variantes=["5 miligramas por litro"])
        c.atoms(data, blocks(), evidence(), 3, 8)

    def test_model_cannot_assign_block_or_unit_ids(self):
        data = document()
        data["blocos"][0]["id"] = "INVENTADO"
        with self.assertRaises(ValueError):
            c.document(data, evidence())
        data = extracted()
        data["unidades"][0]["id"] = "INVENTADO"
        with self.assertRaises(ValueError):
            c.atoms(data, blocks(), evidence(), 3, 8)

    def test_answer_alignment_uses_only_nfc_whitespace_and_casefold(self):
        for response in [" PRODUTO   q ", "Q"]:
            data = question()
            data["resposta"] = response
            c.question(data, unit(), 8)
        for response in ["produto R", "produto-Q", "Q porque reduz a taxa"]:
            data = question()
            data["resposta"] = response
            with self.subTest(response=response), self.assertRaises(ValueError):
                c.question(data, unit(), 8)

    def test_additional_aliases_are_checked_later_semantically(self):
        data = question()
        data["variantes"] = ["Designação equivalente a conferir pelo auditor"]
        c.question(data, unit(), 8)

    def test_question_form_and_shortness(self):
        for text in ["Qual produto", "Qual produto? Qual taxa?", "Qual produto? justifique",
                     "Discuta o comportamento observado?", "Explique detalhadamente o estudo?",
                     "Qual produto\nA) Q\nB) R?"]:
            data = question()
            data["pergunta"] = text
            with self.subTest(text=text), self.assertRaises(ValueError):
                c.question(data, unit(), 8)
        data = extracted()
        data["unidades"][0]["alvo"]["resposta"] = "uma resposta que excede o limite de palavras"
        with self.assertRaises(ValueError):
            c.atoms(data, blocks(), evidence(), 3, 3)

    def test_insufficient_generation_does_not_leave_an_exportable_question(self):
        data = {"status": "insuficiente", "pergunta": "", "resposta": "",
                "variantes": [], "motivo": "Condições insuficientes."}
        c.question(data, unit(), 8)
        data["resposta"] = "Q"
        with self.assertRaises(ValueError):
            c.question(data, unit(), 8)

    def test_blind_answer_cannot_claim_answer_without_support(self):
        data = blind()
        data["suporte"] = []
        with self.assertRaises(ValueError):
            c.blind_answer(data, evidence(), 8)
        data.update(status="sem_suporte", resposta="")
        c.blind_answer(data, evidence(), 8)
        data["resposta"] = "Q"
        with self.assertRaises(ValueError):
            c.blind_answer(data, evidence(), 8)

    def test_qa_audit_cannot_approve_and_report_distinct_valid_answers(self):
        data = qa_audit()
        data["outras_respostas"] = ["produto R"]
        with self.assertRaises(ValueError):
            c.audit_qa(data)

    def test_empty_novelty_comparison_for_first_qa(self):
        c.novelty({"comparacoes": []}, [])
        with self.assertRaises(ValueError):
            c.novelty({"comparacoes": []}, ["U0"])


if __name__ == "__main__":
    unittest.main()
