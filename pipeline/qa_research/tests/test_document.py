"""Fluxo distribuído: modelos simulados, falhas reais de contrato e publicação."""
import copy
import json
import subprocess
import sys
import tempfile
import threading
import time
import unittest
from pathlib import Path
from unittest.mock import patch

from pipeline.inventario.llm import BudgetExceeded
from pipeline.inventario.textutil import atomic_json, read_json, write_jsonl
from pipeline.qa_research.document import contracts as C
from pipeline.qa_research.document.common import Packet, ROOT, citations_for, file_hash, source_record
from pipeline.qa_research.document.export import collect
from pipeline.qa_research.document.runner import Runner, run


class SimulatedLLM:
    """Contratos, não conteúdo científico de produção; nunca enviado à API."""
    def __init__(self, fail=None, reject=False, stop=False):
        self.calls, self.lock = [], threading.Lock()
        self.fail, self.reject, self.stop = fail, reject, stop

    def json(self, system, user, tag, item, validate, **kwargs):
        p = json.loads(user)
        stage = tag.removeprefix("document_")
        with self.lock:
            self.calls.append((stage, item))
        if stage == self.fail:
            raise RuntimeError("Falha simulada de " + stage)
        if self.stop and stage == "write":
            raise BudgetExceeded("Limite simulado")
        if stage == "research":
            data = {"avaliacoes": [{"id": s["id"], "pertinente": True, "tipo": "explicacao_tecnica",
                "achados": [{"proposicao": "Relação técnica limitada ao ensaio.", "trechos": [s["trechos"][0]["id"]], "condicoes": ["ensaio"], "limites": []}]}
                for s in p["fontes"]], "concluir": False, "proximas_fontes": [],
                "pedidos_busca": ["evidências adicionais para o ensaio"], "lacunas": ["Falta suporte para dosagem numérica."]}
        elif stage == "write":
            cid = p["fontes"][0]["trechos"][0]["id"]
            data = {"titulo": "Síntese delimitada", "blocos": [{"texto": "No ensaio descrito, o produto reduziu a espuma.", "trechos": [cid]},
                {"texto": "No ensaio descrito, o tratamento dependeu da temperatura.", "trechos": [cid]}], "lacunas": []}
        elif stage == "audit":
            cid = p["fontes"][0]["trechos"][0]["id"]
            reject = self.reject and p["bloco"]["id"].endswith("V01-B002")
            data = {"bloco": p["bloco"]["id"], **{f: not reject for f in C.FLAGS},
                "parecer": "Revisar relação." if reject else "Suportado no contexto do ensaio.",
                "suporte": [] if reject else [cid], "contraevidencia": [], "lacunas": []}
        elif stage == "gaps":
            data = {"resolucoes": [{"id": g["id"], "estado": "aberta", "parecer": "Não há valor quantitativo disponível.",
                "blocos": [], "trechos": []} for g in p["lacunas"]]}
        elif stage == "discover":
            data = {"propostas": []}
        elif stage == "dedup":
            data = {"comparacoes": [{"a": r["a"]["id"], "b": r["b"]["id"], "equivalentes": False,
                "mesmas_condicoes": False, "parecer": "Condições distintas."} for r in p["pares"]]}
        else:
            raise AssertionError(stage)
        validate(data)
        return data


class DocumentTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.root = Path(self.temp.name)
        self.path = self.root / "packet"
        self.path.mkdir()
        profile = read_json(ROOT / "pipeline/qa_research/configs/documento_produtos_quimicos.json")
        profile["facets"] = profile["facets"][:2]
        profile["runtime"].update(research_rounds=2, batch_sources=1, max_blocks=4, workers=2)
        self.sources = [source_record({"chunk_id": "original-" + str(i), "source_kind": "saved_selection",
            "collection": "estudo", "source_boundary": "known_document", "document_id": str(i),
            "texto": "No ensaio descrito, o produto reduziu a espuma; o tratamento dependeu da temperatura. "
                     "A dosagem foi <NUMBER> ppm. Não foi demonstrada validade universal. " + str(i)}) for i in range(3)]
        atomic_json(self.path / "profile.json", profile)
        atomic_json(self.path / "facets.json", [{**f, "fontes": [s["id"] for s in self.sources]} for f in profile["facets"]])
        atomic_json(self.path / "preparation.json", {"limitations": ["Subconjunto de teste."], "input_mode": "fixture"})
        write_jsonl(self.path / "sources.jsonl", self.sources)
        write_jsonl(self.path / "citations.jsonl", [c for s in self.sources for c in citations_for(s)])
        self.rehash()
        self.packet = Packet(self.path)
        self.output = self.root / "output"

    def tearDown(self):
        self.temp.cleanup()

    def rehash(self):
        atomic_json(self.path / "manifest.json", {"schema": "document-packet-v2", "files": {
            name: file_hash(self.path / name) for name in ("profile.json", "facets.json", "preparation.json", "sources.jsonl", "citations.jsonl")}})

    def execute(self, client=None):
        return run(self.path, self.output, client=client or SimulatedLLM(), progress=lambda _: None)

    def test_modified_packet_fails_hash_check(self):
        with (self.path / "sources.jsonl").open("a", encoding="utf-8") as stream:
            stream.write("{}\n")
        with self.assertRaisesRegex(ValueError, "alterado"):
            Packet(self.path)

    def test_forged_source_hash_fails_even_after_manifest_rehash(self):
        self.sources[0]["texto"] += " Alteração."
        write_jsonl(self.path / "sources.jsonl", self.sources)
        self.rehash()
        with self.assertRaisesRegex(ValueError, "Identidade"):
            Packet(self.path)

    def test_missing_citation_range_fails(self):
        rows = [c for s in self.sources for c in citations_for(s)]
        rows.pop()
        write_jsonl(self.path / "citations.jsonl", rows)
        self.rehash()
        with self.assertRaisesRegex(ValueError, "sem catálogo"):
            Packet(self.path)

    def test_citation_partition_preserves_exact_original(self):
        s = source_record({"chunk_id": "unicode", "source_kind": "verified_manifest", "texto": "Água: 8,2 mg/L.\n" * 110})
        ranges = citations_for(s)
        self.assertEqual("".join(s["texto"][c["inicio"]:c["fim"]] for c in ranges), s["texto"])

    def test_generated_documents_never_become_sources(self):
        for kind in ("generated", "technical_dossier", "qa", None):
            with self.assertRaises(ValueError):
                source_record({"chunk_id": "fake", "source_kind": kind, "texto": "Não é original."})

    def test_malformed_optional_findings_do_not_invalidate_core(self):
        sid = self.sources[0]["id"]
        data = {"avaliacoes": [{"id": sid, "pertinente": True, "tipo": "explicacao_tecnica", "achados": [{"errado": "item"}]}],
                "concluir": False, "proximas_fontes": {}, "pedidos_busca": {}, "lacunas": None}
        C.research_core(data, [sid])
        good, bad = C.findings(data, self.packet, [sid])
        self.assertFalse(good)
        self.assertEqual(len(bad), 1)

    def test_finding_cannot_cite_different_source(self):
        a, b = [s["id"] for s in self.sources[:2]]
        data = {"avaliacoes": [{"id": a, "pertinente": True, "achados": [{"proposicao": "Relação.", "trechos": self.packet.by_source[b], "condicoes": [], "limites": []}]}]}
        good, bad = C.findings(data, self.packet, [a])
        self.assertFalse(good)
        self.assertEqual(len(bad), 1)

    def test_placeholder_forbidden_in_published_text(self):
        with self.assertRaisesRegex(ValueError, "apagados"):
            C.draft({"titulo": "Teste", "blocos": [{"texto": "Use <NUMBER> ppm.", "trechos": []}], "lacunas": []}, [], 4, 200)

    def review(self, text):
        block = {"id": "B1", "texto": text, "trechos": self.packet.by_source[self.sources[0]["id"]]}
        review = {"bloco": "B1", **{f: True for f in C.FLAGS}, "parecer": "Suporte.", "suporte": block["trechos"], "contraevidencia": [], "lacunas": []}
        return block, review

    def test_masked_numbers_cannot_be_reconstructed(self):
        for value in ("Use 50 ppm.", "Reduziu 10%"):
            block, review = self.review(value)
            with self.assertRaisesRegex(ValueError, "Valor/unidade"):
                C.audit(review, block, self.packet, block["trechos"])

    def test_real_number_and_unit_are_preserved(self):
        self.assertEqual(C.numeric_tokens("Água a 8,2 mg/L."), C.numeric_tokens("água a 8.2mg/l"))
        self.assertEqual(C.numeric_tokens("10%"), {"10%"})

    def test_auditor_may_correct_reference_using_visible_original(self):
        block, review = self.review("O produto reduziu a espuma no ensaio.")
        review["suporte"] = self.packet.by_source[self.sources[1]["id"]]
        C.audit(review, block, self.packet, self.packet.citations)
        review["contraevidencia"] = self.packet.by_source[self.sources[2]["id"]]
        C.audit(review, block, self.packet, self.packet.citations)

    def test_unknown_audit_reference_is_rejected(self):
        block, review = self.review("Relação qualitativa.")
        review["suporte"] = ["inventado"]
        with self.assertRaises(ValueError):
            C.audit(review, block, self.packet, self.packet.citations)

    def test_seal_prevents_mutated_block_publication(self):
        block, review = self.review("O produto reduziu a espuma no ensaio.")
        sealed = {**review, "seal": C.seal(block, review, self.packet), "allowed_citations": block["trechos"]}
        state = {"active_blocks": [block], "reviews": {block["id"]: sealed}}
        self.assertEqual(len(C.approved(state, self.packet)), 1)
        block["texto"] = "Funciona em todo FPSO."
        self.assertEqual(C.approved(state, self.packet), [])

    def test_false_flag_prevents_publication(self):
        block, review = self.review("O produto reduziu a espuma no ensaio.")
        review["escopo_preservado"] = False
        state = {"active_blocks": [block], "reviews": {block["id"]: {**review, "allowed_citations": block["trechos"], "seal": C.seal(block, review, self.packet)}}}
        self.assertEqual(C.approved(state, self.packet), [])

    def test_resolved_gap_requires_current_block_and_span(self):
        data = {"resolucoes": [{"id": "G", "estado": "resolvida", "parecer": "Resolvido.", "blocos": [], "trechos": []}]}
        with self.assertRaises(ValueError):
            C.gaps(data, {"G"}, {"B1"}, self.packet.citations)
        data["resolucoes"][0].update(blocos=["OLD-V01-B001"], trechos=list(self.packet.citations)[:1])
        with self.assertRaises(ValueError):
            C.gaps(data, {"G"}, {"B1"}, self.packet.citations)

    def test_full_document_flow_and_breadth_first_rounds(self):
        client = SimulatedLLM()
        summary = self.execute(client)
        self.assertEqual(summary["status"], "concluido")
        self.assertEqual(summary["blocos_publicados"], 4)
        calls = [item for stage, item in client.calls if stage == "research"]
        self.assertEqual(set(calls[:2]), {f["id"] for f in self.packet.facets})
        self.assertEqual(len(calls), 4)
        self.assertTrue((self.output / "documento_auditado.md").is_file())
        self.assertFalse((self.output / "qa.csv").exists())
        self.assertNotIn("<NUMBER>", (self.output / "documento_auditado.md").read_text(encoding="utf-8"))

    def test_resume_reuses_completed_stages_without_calls(self):
        self.execute()
        client = SimulatedLLM(fail="research")
        summary = self.execute(client)
        self.assertEqual(summary["status"], "concluido")
        self.assertFalse(client.calls)

    def test_optional_discovery_failure_preserves_chapters(self):
        summary = self.execute(SimulatedLLM(fail="discover"))
        self.assertEqual(summary["status"], "concluido")
        self.assertEqual(summary["blocos_publicados"], 4)

    def test_failed_consolidation_is_explicit_and_can_resume(self):
        summary = self.execute(SimulatedLLM(fail="dedup"))
        self.assertEqual(summary["status"], "parcial_com_pendencias")
        self.assertEqual(summary["etapas_pendentes"], ["consolidacao"])
        self.assertEqual(summary["blocos_publicados"], 4)
        self.assertEqual(self.execute()["status"], "concluido")

    def test_writer_failure_is_pending_and_can_resume(self):
        summary = self.execute(SimulatedLLM(fail="write"))
        self.assertEqual(summary["status"], "parcial_com_pendencias")
        self.assertEqual(summary["blocos_publicados"], 0)
        summary = self.execute()
        self.assertEqual(summary["status"], "concluido")
        self.assertEqual(summary["blocos_publicados"], 4)

    def test_budget_stop_exports_partial_and_preserves_checkpoint(self):
        summary = self.execute(SimulatedLLM(stop=True))
        self.assertEqual(summary["status"], "interrompido")
        self.assertTrue((self.output / "resumo.json").exists())
        self.assertEqual(self.execute()["status"], "concluido")

    def test_rewrite_uses_new_block_ids_and_keeps_approved_blocks(self):
        summary = self.execute(SimulatedLLM(reject=True))
        self.assertEqual(summary["status"], "concluido")
        state = read_json(self.output / "recortes" / (self.packet.facets[0]["id"] + ".json"))
        self.assertEqual(len(state["versions"]), 2)
        ids = [b["id"] for b in state["active_blocks"]]
        self.assertTrue(any("V01-B001" in bid for bid in ids))
        self.assertTrue(any("V02" in bid for bid in ids))
        self.assertFalse(any("V01-B002" in bid for bid in ids))

    def test_single_failed_audit_does_not_hide_other_approved_blocks(self):
        class OneFailure(SimulatedLLM):
            def json(inner, *args, **kwargs):
                if kwargs["tag"] == "document_audit" and kwargs["item"].endswith("B002"):
                    raise RuntimeError("Falha só no segundo bloco")
                return super(OneFailure, inner).json(*args, **kwargs)
        summary = self.execute(OneFailure())
        self.assertEqual(summary["status"], "parcial_com_pendencias")
        self.assertEqual(summary["blocos_publicados"], 2)

    def test_parallel_facets_and_audits_share_global_concurrency_limit(self):
        class Busy(SimulatedLLM):
            active = maximum = 0
            guard = threading.Lock()
            def json(inner, *args, **kwargs):
                with inner.guard:
                    inner.active += 1
                    inner.maximum = max(inner.maximum, inner.active)
                try:
                    time.sleep(.02)
                    return super(Busy, inner).json(*args, **kwargs)
                finally:
                    with inner.guard:
                        inner.active -= 1
        client = Busy()
        self.execute(client)
        self.assertEqual(client.maximum, 2)  # workers=2 no perfil de teste

    def test_resolved_historical_gaps_do_not_appear_as_current(self):
        class Resolved(SimulatedLLM):
            def json(inner, system, user, **kwargs):
                if kwargs["tag"] == "document_gaps":
                    p = json.loads(user)
                    result = {"resolucoes": [{"id": g["id"], "estado": "resolvida", "parecer": "Delimitação explicitada no bloco.",
                        "blocos": [p["blocos"][0]["id"]], "trechos": [p["provas"][0]["trecho_id"]]} for g in p["lacunas"]]}
                    kwargs["validate"](result)
                    return result
                return super(Resolved, inner).json(system, user, **kwargs)
        self.execute(Resolved())
        doc = (self.output / "documento_auditado.md").read_text(encoding="utf-8")
        self.assertNotIn("Lacunas atuais:", doc)
        self.assertTrue(all(g["estado"] == "resolvida" for g in read_json(self.output / "lacunas.json")))

    def test_consolidation_removes_only_equivalence_with_same_conditions(self):
        class Duplicate(SimulatedLLM):
            def json(inner, system, user, **kwargs):
                if kwargs["tag"] == "document_dedup":
                    p = json.loads(user)
                    result = {"comparacoes": [{"a": r["a"]["id"], "b": r["b"]["id"], "equivalentes": True,
                        "mesmas_condicoes": r["a"]["texto"] == r["b"]["texto"], "parecer": "Mesmo ensaio e relação."} for r in p["pares"]]}
                    kwargs["validate"](result)
                    return result
                return super(Duplicate, inner).json(system, user, **kwargs)
        summary = self.execute(Duplicate())
        self.assertEqual(summary["blocos_publicados"], 2)
        coverage = read_json(self.output / "cobertura.json")
        self.assertTrue(coverage[1]["consolidado_em"])
        self.assertEqual(summary["recortes_com_conteudo"], 2)

    def test_result_snapshot_excludes_secrets_and_caches(self):
        self.execute()
        (self.output / ".env").write_text("DUMMY_SECRET=must-not-copy", encoding="utf-8")
        (self.output / ".local").mkdir(exist_ok=True)
        (self.output / ".local" / "cache.sqlite3").write_text("cache", encoding="utf-8")
        target = self.root / "returned"
        collect(self.output, target, self.path)
        manifest = read_json(target / "manifest_resultados.json")
        self.assertTrue(manifest["files"])
        self.assertFalse((target / ".env").exists())
        self.assertFalse((target / ".local").exists())
        for name, digest in manifest["files"].items():
            self.assertEqual(file_hash(target / name), digest)

    def test_changed_settings_cannot_silently_resume_previous_output(self):
        self.execute()
        with self.assertRaisesRegex(ValueError, "mudaram"):
            run(self.path, self.output, overrides={"model": "outro:low"}, client=SimulatedLLM())

    def test_missing_credentials_produce_collectable_diagnostic(self):
        with patch("pipeline.qa_research.document.runner.LLMClient", side_effect=RuntimeError("Credencial ausente")):
            result = run(self.path, self.output, progress=lambda _: None)
        self.assertEqual(result["status"], "interrompido")
        self.assertIn("Credencial ausente", result["interrupcao"])
        collect(self.output, self.root / "diagnostic", self.path)

    def test_server_imports_no_ml_libraries(self):
        code = "from pipeline.qa_research.document import runner, export; import sys; assert not ({'numpy','torch','sentence_transformers','faiss'} & set(sys.modules))"
        result = subprocess.run([sys.executable, "-S", "-c", code], cwd=ROOT, capture_output=True, text=True)
        self.assertEqual(result.returncode, 0, result.stderr)

    def test_non_string_reference_is_validation_error(self):
        with self.assertRaises(ValueError):
            C.refs([{"id": "wrong"}], self.packet.citations)

    def prep_profile(self):
        profile = copy.deepcopy(self.packet.profile)
        profile["cache_dir"] = str(self.root / "preparation_cache")
        profile["inputs"] = {"raw_texts": [], "origins": []}
        profile["facets"][0]["termos"] = ["desemulsificante"]
        profile["facets"][1]["termos"] = ["biocida"]
        for facet in profile["facets"]:
            facet.pop("context_groups", None)
            facet.pop("exclude_context", None)
        profile["selection"].update(frontier_per_facet=2, sources_per_facet=2)
        path = self.root / "local_profile.json"
        atomic_json(path, profile)
        originals = [{**s, "texto": word + ": texto original de ensaio.", "chunk_id": "prep-" + str(i)}
                     for i, (s, word) in enumerate(zip(self.sources, ("desemulsificante", "biocida")))]
        return path, originals

    def test_local_preparation_reuses_frontier_without_reading_again(self):
        from pipeline.qa_research.document.prepare import prepare
        profile, originals = self.prep_profile()
        seen = []
        def records():
            for row in originals:
                seen.append(row["chunk_id"])
                yield row
        def local_inputs(*args):
            return records(), [{"sha256": "fixture-originals"}], "fixture", []
        with patch("pipeline.qa_research.document.prepare.inputs", side_effect=local_inputs):
            first = prepare(profile, self.root / "prep1", semantic=False, progress=lambda _: None)
            second = prepare(profile, self.root / "prep2", semantic=False, progress=lambda _: None)
        self.assertEqual(len(seen), 2)
        self.assertEqual(first["selected_sources"], second["selected_sources"])
        self.assertEqual(len(Packet(self.root / "prep2").sources), 2)

    def test_semantic_channel_promotes_candidate_from_another_lexical_facet(self):
        import numpy as np
        from pipeline.qa_research.document.prepare import prepare
        profile, originals = self.prep_profile()
        class E5:
            protocol = {"model": "test-only-not-real"}
            def __init__(self, *args, **kwargs):
                pass
            def queries(self, qs):
                return np.asarray([[0., 1.] for q in qs])
            def passages_many(self, texts):
                return [np.asarray([[0., 1.] if "biocida" in t else [1., 0.]]) for t in texts]
            def flush(self):
                pass
            def close(self):
                pass
        with patch("pipeline.qa_research.document.prepare.inputs", return_value=(iter(originals), [], "fixture", [])), \
                patch("pipeline.qa_research.selection.LocalE5", E5):
            prepare(profile, self.root / "semantic", progress=lambda _: None)
        packet = Packet(self.root / "semantic")
        sid = next(sid for sid, s in packet.sources.items() if "biocida" in s["texto"])
        self.assertIn(sid, packet.facets[0]["fontes"])
        self.assertEqual(set(packet.facets[0]["ranking"][sid]["channels"]), {"semantic"})

    def test_unsupported_pressure_and_small_numeric_value_are_rejected(self):
        for value in ("No ensaio, a pressão foi 200 bar.", "O pH medido foi 5."):
            block, review = self.review(value)
            with self.assertRaisesRegex(ValueError, "Número"):
                C.audit(review, block, self.packet, block["trechos"])

    def test_context_filter_rejects_unrelated_storage_and_compatibility(self):
        from pipeline.qa_research.document.prepare import contextual, fold
        profile = read_json(ROOT / "pipeline/qa_research/configs/documento_produtos_quimicos.json")
        storage = next(f for f in profile["facets"] if f["id"] == "ARMAZENAMENTO")
        compatibility = next(f for f in profile["facets"] if f["id"] == "COMPATIBILIDADE")
        self.assertFalse(contextual(fold("Chemical preservation and storage of photographic films."), storage))
        self.assertFalse(contextual(fold("Compatibilidade química de misturas asfálticas para pavimentação."), compatibility))
        self.assertTrue(contextual(fold("Offshore chemical storage and handling of methanol."), storage))
        self.assertTrue(contextual(fold("Compatibilidade entre inibidor de corrosão e biocida na água de injeção."), compatibility))

    def test_short_context_anchor_is_not_substring_of_unrelated_word(self):
        from pipeline.qa_research.document.prepare import contextual
        self.assertFalse(contextual("curso de literatura", {"context_groups": [["URS"]]}))
        self.assertTrue(contextual("sistema urs para injecao", {"context_groups": [["URS"]]}))

    def test_reference_filter_does_not_discard_technical_paragraph_with_citations(self):
        from pipeline.qa_research.document.prepare import reference_list
        self.assertTrue(reference_list("numero do registro a numero do registro b"))
        self.assertTrue(reference_list("references astm conference thesis pp vol"))
        self.assertFalse(reference_list("no ensaio de corrosao as referencias tecnicas sustentam o metodo astm"))

    def test_acronym_list_filter_preserves_attached_abstract(self):
        from pipeline.qa_research.document.prepare import acronym_list
        text = "HSE - Health and Safety Executive " * 10
        self.assertTrue(acronym_list(text))
        self.assertFalse(acronym_list(text + "Resumo O ensaio mediu a corrosão em água do mar."))

    def test_tighter_post_filter_reuses_broad_frontier(self):
        from pipeline.qa_research.document.prepare import prepare
        profile, originals = self.prep_profile()
        seen = []
        def records():
            for row in originals:
                seen.append(row["chunk_id"])
                yield row
        with patch("pipeline.qa_research.document.prepare.inputs", side_effect=lambda *a: (records(), [], "fixture", [])):
            prepare(profile, self.root / "broad", semantic=False, progress=lambda _: None)
            data = read_json(profile)
            data["facets"][0]["post_context_groups"] = [["biocida"]]
            atomic_json(profile, data)
            prepare(profile, self.root / "narrow", semantic=False, progress=lambda _: None)
        self.assertEqual(len(seen), 2)
        self.assertEqual(Packet(self.root / "narrow").facets[0]["fontes"], [])

    def test_bibliographic_catalog_is_not_scientific_evidence(self):
        from pipeline.qa_research.document.prepare import bibliographic_catalog
        self.assertTrue(bibliographic_catalog("São emitidos por ano muitos resumos de patentes."))
        self.assertFalse(bibliographic_catalog("A revisão científica compara os resultados de ensaios de biocidas."))


if __name__ == "__main__":
    unittest.main()
