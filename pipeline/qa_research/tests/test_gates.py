"""Adversarial checkpoint tests; fixtures contain no external QA dataset."""
import copy
import json
import unittest
from types import SimpleNamespace

from pipeline.inventario.textutil import sha
from pipeline.qa_research import contracts as C
from pipeline.qa_research.gates import checked_chapter, checked_question, checked_units


class GateTests(unittest.TestCase):
    def setUp(self):
        self.config = SimpleNamespace(max_atoms_per_facet=12, answer_words=24)
        source = {"chunk_id": "regis:paper:p3:w0", "texto": "MEG é a sigla de monoetilenoglicol.",
                  "source_kind": "saved_selection", "title": "Terminologia química", "page_ini": 3,
                  "collection": "regis", "document_id": "paper"}
        source["id"] = "E" + sha(source["chunk_id"] + "\n" + source["texto"], 16)
        source["texto_sha256"] = sha(source["texto"], 64)
        support = [{"evidencia_id": source["id"], "citacao": "MEG é a sigla de monoetilenoglicol."}]
        block = {"id": "Rfixture-B001", "texto": "MEG designa monoetilenoglicol.", "fontes": [source["id"]]}
        version = {"titulo": "Terminologia", "blocos": [block], "lacunas": []}
        audit = {"versao": 1, "avaliacoes": [{"id": block["id"], "parecer": "Relação sustentada.",
                 "suporte": support, **dict.fromkeys(C.DOCUMENT_FLAGS, True)}], "lacunas": [], "consultas": []}
        self.state = {"id": "Rfixture", "recorte": {"id": "Rfixture"}, "status": "auditado_modelo",
                      "evidencias": [source], "versoes": [version], "auditorias": [audit],
                      "capitulo": copy.deepcopy(version)}
        raw = {"proposicao": "MEG designa monoetilenoglicol.", "tipo": "principio",
               "contexto": "Terminologia de produtos químicos", "condicoes": [], "limites": [],
               "blocos": [block["id"]], "jurisdicao": "", "edicao": "", "suporte": copy.deepcopy(support),
               "alvo": {"tipo": "entidade", "resposta": "Monoetilenoglicol", "variantes": [], "qualificador": ""}}
        identity = "Rfixture-U" + sha(json.dumps(raw, sort_keys=True, ensure_ascii=False), 14)
        self.unit = {**raw, "id": identity, "recorte_id": "Rfixture", "elegivel_qa": True,
                     "auditoria": {"id": identity, "parecer": "Alvo sustentado.", **dict.fromkeys(C.ATOM_FLAGS, True)}}
        self.pack = {"recorte_id": "Rfixture", "unidades": [self.unit], "motivo": ""}
        question = {"status": "ok", "pergunta": "Qual composto é designado pela sigla MEG?",
                    "resposta": "Monoetilenoglicol", "variantes": [], "motivo": ""}
        self.row = {"id": identity, "recorte_id": "Rfixture", "unidade": copy.deepcopy(self.unit),
                    "status": "aprovada_modelo", "validacao_humana": "pendente", "candidata": question,
                    "evidencias_verificacao": copy.deepcopy([source]),
                    "resolucao_independente": {"status": "respondida", "resposta": "Monoetilenoglicol",
                     "outras_respostas": [], "condicoes_ausentes": [], "parecer": "Sigla resolvida.",
                     "suporte": copy.deepcopy(support)},
                    "auditoria": {**dict.fromkeys(C.QA_FLAGS, True), "outras_respostas": [], "parecer": "Aprovada."},
                    **{key: copy.deepcopy(question[key]) for key in ("pergunta", "resposta", "variantes")}}

    def test_intact_chain_passes_without_mutation(self):
        original = copy.deepcopy((self.state, self.pack, self.row))
        self.assertEqual(checked_chapter(self.state), self.state["capitulo"])
        self.assertEqual(checked_units(self.pack, self.state, self.config), [self.unit])
        self.assertTrue(checked_question(self.row, self.unit, self.state, self.config))
        self.assertEqual((self.state, self.pack, self.row), original)

    def test_latest_version_cannot_reuse_an_older_audit(self):
        self.state["versoes"].append(copy.deepcopy(self.state["versoes"][-1]))
        self.assertIsNone(checked_chapter(self.state))
        self.assertFalse(checked_question(self.row, self.unit, self.state, self.config))

    def test_published_block_cannot_change_after_audit(self):
        self.state["capitulo"]["blocos"][0]["texto"] = "Conclusão inventada após a auditoria."
        self.assertIsNone(checked_chapter(self.state))

    def test_unexpected_block_fields_are_not_hidden_by_validation(self):
        self.state["capitulo"]["blocos"][0]["resposta_nao_auditada"] = "Conteúdo externo"
        self.assertIsNone(checked_chapter(self.state))

    def test_status_alone_cannot_publish_rejected_blocks(self):
        self.state["auditorias"][-1]["avaliacoes"][0]["suportado"] = False
        self.assertIsNone(checked_chapter(self.state))

    def test_partial_chapter_must_match_approved_subset(self):
        block = {"id": "Rfixture-B002", "texto": "Outro bloco sem suporte.",
                 "fontes": [self.state["evidencias"][0]["id"]]}
        self.state["versoes"][-1]["blocos"].append(block)
        review = {"id": block["id"], "parecer": "Reprovado.", "suporte": [], **dict.fromkeys(C.DOCUMENT_FLAGS, False)}
        self.state["auditorias"][-1]["avaliacoes"].append(review)
        self.state["status"] = "parcial"
        self.assertIsNotNone(checked_chapter(self.state))
        self.state["capitulo"]["blocos"].append(block)
        self.assertIsNone(checked_chapter(self.state))

    def test_original_source_hash_and_id_are_rechecked(self):
        for field, replacement in (("texto", "Texto adulterado."), ("id", "Eunknown"), ("texto_sha256", "bad")):
            with self.subTest(field=field):
                state = copy.deepcopy(self.state)
                state["evidencias"][0][field] = replacement
                self.assertIsNone(checked_chapter(state))

    def test_document_audit_citation_must_still_exist(self):
        self.state["auditorias"][-1]["avaliacoes"][0]["suporte"][0]["citacao"] = "Frase nunca presente na fonte."
        self.assertIsNone(checked_chapter(self.state))

    def test_generated_source_cannot_be_laundered_through_status(self):
        self.state["evidencias"][0]["source_kind"] = "generated_document"
        self.assertIsNone(checked_chapter(self.state))

    def test_corrupt_unit_is_filtered_while_intact_unit_survives(self):
        corrupt = copy.deepcopy(self.unit)
        corrupt["id"] += "corrupt"
        self.pack["unidades"].append(corrupt)
        self.assertEqual(checked_units(self.pack, self.state, self.config), [self.unit])

    def test_unit_must_belong_to_the_current_facet(self):
        self.pack["recorte_id"] = "Rother"
        self.assertEqual(checked_units(self.pack, self.state, self.config), [])

    def test_atom_audit_flags_and_identity_are_rechecked(self):
        self.unit["auditoria"]["resposta_determinada"] = False
        self.assertEqual(checked_units(self.pack, self.state, self.config), [])

    def test_forged_eligibility_boolean_is_rejected(self):
        self.unit["elegivel_qa"] = 1
        self.assertEqual(checked_units(self.pack, self.state, self.config), [])

    def test_final_answer_cannot_diverge_from_validated_candidate(self):
        self.row["resposta"] = "Qualquer produto químico"
        self.assertFalse(checked_question(self.row, self.unit, self.state, self.config))

    def test_embedded_unit_must_match_current_registry(self):
        self.row["unidade"]["alvo"]["resposta"] = "Outra resposta"
        self.assertFalse(checked_question(self.row, self.unit, self.state, self.config))

    def test_missing_author_source_rejects_qa(self):
        self.row["evidencias_verificacao"] = []
        self.assertFalse(checked_question(self.row, self.unit, self.state, self.config))

    def test_source_metadata_cannot_change_between_author_and_verification(self):
        self.row["evidencias_verificacao"][0]["jurisdiction"] = "Invented jurisdiction"
        self.assertFalse(checked_question(self.row, self.unit, self.state, self.config))

    def test_blind_answer_requires_a_real_contiguous_support_quote(self):
        self.row["resolucao_independente"]["suporte"][0]["citacao"] = "Não está no corpus."
        self.assertFalse(checked_question(self.row, self.unit, self.state, self.config))

    def test_ambiguity_or_missing_conditions_prevent_publication(self):
        for field in ("outras_respostas", "condicoes_ausentes"):
            with self.subTest(field=field):
                row = copy.deepcopy(self.row)
                row["resolucao_independente"][field] = ["Outra possibilidade"]
                self.assertFalse(checked_question(row, self.unit, self.state, self.config))

    def test_auditor_flags_are_strict_boolean_and_complete(self):
        self.row["auditoria"]["factual"] = 1
        self.assertFalse(checked_question(self.row, self.unit, self.state, self.config))

    def test_redundancy_cannot_be_exported_as_approved(self):
        self.row["novidade"] = {"comparacoes": [{"id": "Uother", "classe": "redundante", "parecer": "Mesmo alvo."}]}
        self.assertFalse(checked_question(self.row, self.unit, self.state, self.config))

    def test_malformed_checkpoint_fails_closed(self):
        self.assertIsNone(checked_chapter({"status": "auditado_modelo"}))
        self.assertEqual(checked_units({}, self.state, self.config), [])
        self.assertFalse(checked_question({}, self.unit, self.state, self.config))


if __name__ == "__main__":
    unittest.main()
