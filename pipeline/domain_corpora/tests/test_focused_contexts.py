"""Regressões dos defeitos observados nos artefatos da execução QA v4."""
import json
import tempfile
import unittest
from pathlib import Path
from types import SimpleNamespace
from unittest.mock import patch

import numpy as np

from pipeline.fase_4.source_audit import audit_source, audit_prompt, SYSTEM_PROMPT
from pipeline.fase_4.multi_corpus import plan_documents, scan, source_scores, structural_noise
from pipeline.fase_4.context_recovery import recover_context
from pipeline.fase_4.domain import DomainResources, legacy, TOPICOS
from pipeline.fase_4.config import QAConfig
from pipeline.fase_4.storage import CallLimitReached
from azure_openai_backend import parse_json_loose
from test_corpora import setUpModule, tearDownModule, fixture, FakeTranslator, Embedder
from test_recovery_embeddings import context, raw_audit, blocked, Planner


class FocusedAudit(unittest.TestCase):
    def supported(self):
        return {**context(),'chunks':[{'chunk_id':'a','collection':'anp',
            'texto':'A manutenção planejada monitora a condição dos ativos.'}]}

    def test_one_supported_target_is_approved_with_partial_coverage(self):
        with tempfile.TemporaryDirectory() as directory:
            raw=raw_audit(True);raw.update(coverage='partial',supported_focus='Monitoramento da condição',
                limitations=['Não cobre custos, offloading ou todas as utilidades'])
            client=SimpleNamespace(complete_json=lambda *a,**k:raw)
            result=audit_source(client,self.supported(),Path(directory),'sig')
            self.assertTrue(result['approved']);self.assertEqual(result['coverage'],'partial')
            self.assertIn('UM alvo',SYSTEM_PROMPT)
            self.assertIn('NÃO precisam ser inteiramente cobertos',audit_prompt(self.supported()))

    def test_rejection_is_never_automatically_promoted(self):
        with tempfile.TemporaryDirectory() as directory:
            raw=raw_audit(True);raw.update(approved=False,scope_compatible=False,coverage='partial')
            result=audit_source(SimpleNamespace(complete_json=lambda *a,**k:raw),self.supported(),directory,'sig')
            self.assertFalse(result['approved']);self.assertEqual(result['audit_status'],'rejected_content')

    def test_invalid_answers_are_saved_and_quarantined_with_feedback(self):
        with tempfile.TemporaryDirectory() as directory:
            captured=[]
            def complete(prompt,**kwargs):captured.append(prompt);return {'approved':'wrong'}
            result=audit_source(SimpleNamespace(complete_json=complete),context(),directory,'sig')
            self.assertEqual(result['audit_status'],'invalid_response');self.assertFalse(result['approved'])
            self.assertIn('wrong',captured[1])
            root=Path(directory)
            self.assertTrue((root/'contextos_candidatos/f-context-d0.json').is_file())
            attempts=(root/'auditorias_respostas/f-context-d0.jsonl').read_text().splitlines()
            self.assertEqual(len(attempts),2)
            self.assertEqual(json.loads(json.loads(attempts[0])['response']),{'approved':'wrong'})
            client=SimpleNamespace(complete_json=lambda *a,**k: (_ for _ in ()).throw(AssertionError('cached')))
            self.assertEqual(audit_source(client,context(),directory,'sig')['audit_status'],'invalid_response')

    def test_bad_quote_is_repaired_even_in_rejected_response(self):
        with tempfile.TemporaryDirectory() as directory:
            raw=raw_audit(True);raw['approved']=False
            raw['claims'][0]['evidence'][0]['quote']='Citação que não está na fonte'
            responses=iter([raw,raw_audit(False)])
            client=SimpleNamespace(complete_json=lambda *a,**k:next(responses))
            result=audit_source(client,self.supported(),directory,'sig')
            self.assertEqual(result['audit_status'],'rejected_content')
            self.assertNotIn('nonliteral_claim_evidence',result['validation_errors'])

    def test_json_parse_failure_keeps_raw_response(self):
        with tempfile.TemporaryDirectory() as directory:
            def call(*a,**k):return parse_json_loose('Resposta sem JSON: texto completo')
            result=audit_source(SimpleNamespace(complete_json=call),context(),directory,'sig')
            self.assertEqual(result['audit_status'],'invalid_response')
            self.assertIn('texto completo',(Path(directory)/result['responses_path']).read_text())

    def test_nonfinite_confidence_is_quarantined_without_serialization_crash(self):
        with tempfile.TemporaryDirectory() as directory:
            raw=raw_audit(True);raw['confidence']=float('nan')
            result=audit_source(SimpleNamespace(complete_json=lambda *a,**k:raw),self.supported(),directory,'sig')
            self.assertEqual(result['audit_status'],'invalid_response')

    def test_budget_and_api_errors_are_not_treated_as_bad_content(self):
        for error in (CallLimitReached('budget'),RuntimeError('Azure unavailable')):
            with tempfile.TemporaryDirectory() as directory:
                def call(*args,**kwargs):raise error
                with self.assertRaises(type(error)):
                    audit_source(SimpleNamespace(complete_json=call),context(),directory,'sig')


class FocusedRetrieval(unittest.TestCase):
    def test_structural_pages_excluded_but_instructions_retained(self):
        self.assertTrue(structural_noise('Lista de figuras Figura 1 .... 15 Figura 2 .... 18'))
        self.assertTrue(structural_noise('References Smith 2020 DOI 10.1000 Jones 2022'))
        self.assertFalse(structural_noise('Lista de figuras. A pressão deve ser monitorada para evitar sobrepressão.'))
        self.assertFalse(structural_noise('A tabela apresenta causas de perda de produção.'))

    def test_distinctive_terms_have_reserved_candidate_capacity(self):
        with tempfile.TemporaryDirectory() as directory:
            cfg=legacy.Config(out_dir=Path(directory))
            facet=legacy.Faceta('f','t','s','disponibilidade','disponibilidade',
                'disponibilidade operacional',['disponibilidade operacional'],['producao','manutencao','utilidade','gestao'])
            units=[{'collection':'hse','document_id':str(i),'title':'Unit','page':1,
                'text':('producao manutencao utilidade gestao '*70 if i<6 else
                        'disponibilidade operacional '+ 'palavra '*280)} for i in range(7)]
            with patch('pipeline.fase_4.multi_corpus.iter_units',return_value=iter(units)):
                pool=scan([facet],[],cfg,legacy,2,'sig')['f']
            self.assertEqual(len(pool),2)
            self.assertTrue(any(c['termos_fortes'] for c in pool))

    def test_raw_cosines_do_not_inflate_a_uniformly_weak_pool(self):
        class E:
            def encode(self,values):return np.array([[1.,0.],[1.,0.]])
        values=[{'lex_score':1},{'lex_score':1}]
        score=source_scores(values,np.array([[.01,0.],[.02,0.]]),'q',E(),legacy)
        self.assertTrue(np.all(score<.13))

    def test_context_complements_anchor_before_unrelated_diversity(self):
        candidates=[{'chunk_id':cid,'collection':collection,'texto':cid,'lex_score':1}
                    for cid,collection in [('anchor','anp'),('near','hse'),('other','regis')]]
        class E:
            def encode(self,values):return np.array([[1.,0.],[.99,.1],[0.,1.]])
        facet=legacy.Faceta('f','t','s','title','focus','query',[],[])
        with patch('pipeline.fase_4.multi_corpus.source_scores',return_value=np.array([.9,.7,.75])):
            plans=plan_documents([facet],{'f':candidates},E(),legacy.Config(
                n_trechos_por_documento=2,n_documentos_por_faceta=2),legacy)
        self.assertEqual(plans[0]['chunk_ids'],['anchor','near'])
        self.assertEqual(plans[0]['collections'],['anp','hse'])
        self.assertEqual(plans[1]['chunk_ids'],['other'])


class PreparationResilience(unittest.TestCase):
    def test_three_invalid_audits_stop_with_diagnostics_instead_of_false_rejections(self):
        with tempfile.TemporaryDirectory() as directory:
            root=Path(directory);manifest=fixture(root);topic=next(iter(TOPICOS));sub=next(iter(TOPICOS[topic]))
            facets=[legacy.Faceta(f'f{i}',topic,sub,'Bomba','fluxo','bomba',['bomba'],['fluido']) for i in range(2)]
            cfg=QAConfig(context_mode='audited',chunk_words=250,chunks_per_facet=3,output=root/'run',corpus_manifest=manifest,corpus_dir=None,max_context_refinements=0)
            cfg.output.mkdir()
            with patch.object(legacy,'extrair_facetas',return_value=facets),\
                 patch('pipeline.fase_4.azure_embeddings.AzureFullTextEmbedder',Embedder),\
                 patch('pipeline.fase_4.domain.audit_source',return_value={
                    'approved':False,'audit_status':'invalid_response','reason':'invalid structure'}):
                with self.assertRaisesRegex(RuntimeError,'Falhas consecutivas'):
                    DomainResources(cfg,FakeTranslator()).prepare([topic])
            status=json.loads((cfg.output/'preparacao_status.json').read_text())
            self.assertEqual(status['invalid_response'],3);self.assertEqual(status['rejected_content'],0)

    def test_invalid_audit_does_not_prevent_the_next_valid_context(self):
        with tempfile.TemporaryDirectory() as directory:
            root=Path(directory);manifest=fixture(root);topic=next(iter(TOPICOS));sub=next(iter(TOPICOS[topic]))
            facet=legacy.Faceta('f',topic,sub,'Bomba','fluxo','bomba',['bomba'],['fluido'])
            cfg=QAConfig(context_mode='audited',chunk_words=250,chunks_per_facet=3,output=root/'run',corpus_manifest=manifest,corpus_dir=None,max_context_refinements=0)
            cfg.output.mkdir()
            def audit(_,ctx,*args):
                if ctx['doc_id'].endswith('d0'):
                    return {'approved':False,'audit_status':'invalid_response','reason':'invalid JSON'}
                return {'approved':True,'audit_status':'approved','coverage':'partial','supported_focus':'Condição da bomba',
                    'allowed_chunk_ids':[c['chunk_id'] for c in ctx['chunks']],'targets':['Condição da bomba'],
                    'claims':[],'limitations':[],'original_context':'produção','transferability':'técnica'}
            with patch.object(legacy,'extrair_facetas',return_value=[facet]),\
                 patch('pipeline.fase_4.azure_embeddings.AzureFullTextEmbedder',Embedder),\
                 patch('pipeline.fase_4.domain.audit_source',side_effect=audit),\
                 patch('pipeline.fase_4.domain.audited_document',return_value='Claims'),\
                 patch.object(DomainResources,'make_codebook',return_value=SimpleNamespace(k=3)):
                domain=DomainResources(cfg,FakeTranslator()).prepare([topic])
            self.assertEqual(len(domain.documents(topic,sub)),1)
            self.assertEqual(domain.documents(topic,sub)[0]['focus'],'Condição da bomba')
            coverage=json.loads((cfg.output/'cobertura_dominio.json').read_text())[0]
            self.assertEqual(coverage['invalid_audits'],1);self.assertEqual(coverage['blocked_documents'],0)
            self.assertEqual(coverage['partially_supported_documents'],1)

    def test_bad_recovery_plan_is_saved_without_aborting_all_preparation(self):
        with tempfile.TemporaryDirectory() as directory:
            root=Path(directory);cfg=QAConfig(context_mode='audited',chunk_words=250,chunks_per_facet=3,output=root);planner=Planner(['invented'])
            candidates=[{'chunk_id':'real','collection':'hse','texto':'manutenção offshore','lex_score':5}]
            _,result=recover_context(context(),blocked(),candidates,Embedder(),legacy.Config(),cfg,planner,None,
                root/'dominio','sig',legacy,lambda *a: (_ for _ in ()).throw(AssertionError('no audit')),
                lambda *a:None)
            self.assertFalse(result['approved'])
            self.assertEqual(json.loads((root/'recuperacoes_contexto.jsonl').read_text())['status'],'invalid_response')
            self.assertEqual(planner.calls,2)


if __name__=='__main__':unittest.main()
