"""Regressões de recuperação e embeddings Azure, sem rede ou chamadas pagas."""
import json
import tempfile
import unittest
from pathlib import Path
from types import SimpleNamespace
from unittest.mock import patch

import numpy as np

from pipeline.fase_4.config import QAConfig
from pipeline.fase_4.domain import legacy
from pipeline.fase_4.azure_embeddings import AzureFullTextEmbedder, AzureEmbeddingBackend
from pipeline.fase_4.context_recovery import recover_context, validate_plan
from pipeline.fase_4.source_audit import audit_source,validate_audit
from pipeline.fase_4.multi_corpus import source_scores
from pipeline.fase_4.storage import RunStore,CallLimitReached
from pipeline.fase_4.facet_scope import ScopedFacetClient
from test_corpora import setUpModule,tearDownModule,Embedder


class Tokenizer:
    def encode(self,text,**kwargs):return [int(x) for x in text.split()]


class Backend:
    def __init__(self,dim=3072):self.calls=[];self.dim=dim;self.settings=None
    def create(self,inputs):
        self.calls.append([list(ids) for ids in inputs])
        data=[]
        for i,ids in enumerate(inputs):
            vector=np.zeros(self.dim);vector[0]=sum(ids)+1;vector[1]=len(ids)+1
            data.append(SimpleNamespace(index=i,embedding=vector.tolist()))
        return SimpleNamespace(data=list(reversed(data)))


def context():
    return {'doc_id':'f-context-d0','facet_id':'f','facet_title':'manutenção offshore','focus':'planejamento de manutenção',
        'scope':'produção FPSO','topic':'topic','subtopic':'sub','collections':['petroles'],
        'chunks':[{'chunk_id':'bad','collection':'petroles','texto':'A programação de refinaria não sustenta o alvo offshore.'}]}


def blocked():
    return {'approved':False,'reason':'Trecho de refinaria fora do escopo','issues':['refinaria'],
        'validation_errors':['source_not_approved'],'chunk_reviews':[
            {'chunk_id':'bad','compatible':False,'useful':False,'reason':'fora do escopo'}]}


class Planner:
    def __init__(self,ids,unrepairable=False):self.ids=ids;self.calls=0;self.unrepairable=unrepairable
    def complete_json(self,prompt,**kwargs):
        self.calls+=1
        return {'selected_chunk_ids':self.ids,'reason':'Evidências compatíveis selecionadas','unrepairable':self.unrepairable}


def raw_audit(approved=False):
    return {'approved':approved,'facet_correct':True,'scope_compatible':approved,'technically_consistent':approved,
        'regulatory_uncertainty':False,'confidence':.97,'original_context':'refinaria' if not approved else 'produção offshore',
        'transferability':'fora do escopo' if not approved else 'princípio aplicável',
        'allowed_chunk_ids':['a'] if approved else [],'claims':[
            {'claim':'Afirmação sustentada','evidence':[{'chunk_id':'a','quote':'A manutenção planejada monitora a condição'}]}] if approved else [],
        'targets':['Interpretar manutenção'] if approved else [],'limitations':[],'issues':[],
        'reason':'Aprovado' if approved else 'Bloqueado por escopo'}


class AuditValidation(unittest.TestCase):
    def test_valid_rejection_empty_allowed_list_uses_one_call(self):
        with tempfile.TemporaryDirectory() as directory:
            client=SimpleNamespace(complete_json=lambda *a,**k:raw_audit(False))
            with patch.object(client,'complete_json',wraps=client.complete_json) as call:
                result=audit_source(client,context(),Path(directory),'signature')
            self.assertFalse(result['approved']);self.assertEqual(call.call_count,1)
            self.assertIn('no_allowed_chunks',result['validation_errors'])
            self.assertNotIn('invalid_allowed_chunks',result['validation_errors'])

    def test_unknown_ids_always_invalid(self):
        raw=raw_audit(True);raw['allowed_chunk_ids']=['invented']
        self.assertIn('invalid_allowed_chunks',validate_audit(raw,context())['validation_errors'])

    def test_bad_review_type_returns_validation_error(self):
        raw=raw_audit(False);raw['chunk_reviews']=[{'chunk_id':['bad'],'compatible':False,'useful':False,'reason':'bad'}]
        self.assertIn('invalid_chunk_reviews',validate_audit(raw,context())['validation_errors'])

    def test_supported_claim_requires_literal_evidence(self):
        ctx={**context(),'chunks':[{'chunk_id':'a','texto':'A manutenção planejada monitora a condição dos ativos.'}]}
        self.assertTrue(validate_audit(raw_audit(True),ctx)['approved'])
        raw=raw_audit(True);raw['claims'][0]['evidence'][0]['quote']='Uma citação que não existe'
        self.assertFalse(validate_audit(raw,ctx)['approved'])


class Recovery(unittest.TestCase):
    def run_recovery(self,root,planner,audit_fn,max_attempts=2):
        cfg=QAConfig(output=root,max_context_refinements=max_attempts)
        candidates=[{'chunk_id':name,'collection':name,'texto':'manutenção de produção offshore '+name,'lex_score':5}
                    for name in ('hse','anp')]
        events=[]
        return recover_context(context(),blocked(),candidates,Embedder(),legacy.Config(),cfg,planner,None,
            root/'dominio','sig',legacy,audit_fn,lambda c,a:events.append((c,a)))

    def test_repaired_context_mixes_sources_and_reaudits(self):
        with tempfile.TemporaryDirectory() as directory:
            root=Path(directory);planner=Planner(['anp','hse']);calls=[]
            def audit(_,ctx,*args):calls.append(ctx);return {'approved':True,'reason':'Material adequado'}
            ctx,result=self.run_recovery(root,planner,audit)
            self.assertTrue(result['approved']);self.assertEqual(ctx['collections'],['anp','hse'])
            self.assertEqual(ctx['doc_id'],'f-context-d0-r1');self.assertEqual(len(calls),1)
            self.assertTrue(ctx['context_recovery']['recovered'])

    def test_planner_cannot_invent_ids_or_repeat_failed_set(self):
        pool=[{'chunk_id':'known'}]
        for raw in ({'selected_chunk_ids':['unknown'],'reason':'reason','unrepairable':False},
                    {'selected_chunk_ids':['known'],'reason':'reason','unrepairable':False}):
            with self.assertRaises(ValueError):validate_plan(raw,pool,[frozenset(['known'])],6)

    def test_unrefinable_stays_blocked_no_audit_call(self):
        with tempfile.TemporaryDirectory() as directory:
            audit=SimpleNamespace(calls=0)
            def fail(*args):audit.calls+=1;raise AssertionError('Não deveria auditar')
            ctx,result=self.run_recovery(Path(directory),Planner([],True),fail)
            self.assertFalse(result['approved']);self.assertEqual(audit.calls,0)
            self.assertEqual(ctx['context_recovery']['attempts'][0]['status'],'unrepairable')

    def test_cached_plan_not_requested_again(self):
        with tempfile.TemporaryDirectory() as directory:
            planner=Planner(['anp','hse'])
            def audit(*args):return {'approved':True,'reason':'OK'}
            self.run_recovery(Path(directory),planner,audit)
            self.run_recovery(Path(directory),planner,audit)
            self.assertEqual(planner.calls,1)
            rows=(Path(directory)/'recuperacoes_contexto.jsonl').read_text().splitlines()
            self.assertEqual(len(rows),1)

    def test_zero_attempts_disabled(self):
        with tempfile.TemporaryDirectory() as directory:
            planner=Planner(['anp']);ctx,result=self.run_recovery(Path(directory),planner,lambda *a:None,0)
            self.assertFalse(result['approved']);self.assertEqual(planner.calls,0)

    def test_recovery_stops_after_two_rejected_recompositions(self):
        with tempfile.TemporaryDirectory() as directory:
            class Alternating(Planner):
                def complete_json(self,*args,**kwargs):
                    self.calls+=1
                    return {'selected_chunk_ids':['anp' if self.calls==1 else 'hse'],'reason':'substituição',
                            'unrepairable':False}
            planner=Alternating([]);audits=[]
            def audit(_,ctx,*args):
                audits.append(ctx);return {'approved':False,'reason':'Suporte ainda insuficiente','issues':[],
                                          'validation_errors':['source_not_approved']}
            ctx,result=self.run_recovery(Path(directory),planner,audit)
            self.assertFalse(result['approved']);self.assertEqual(planner.calls,2);self.assertEqual(len(audits),2)
            self.assertEqual(len(ctx['context_recovery']['attempts']),2)


class Embeddings(unittest.TestCase):
    def test_azure_vectors_order_cache_and_dimensions(self):
        with tempfile.TemporaryDirectory() as directory:
            cfg=QAConfig(output=Path(directory));backend=Backend();embedder=AzureFullTextEmbedder(cfg,backend,Tokenizer())
            values=embedder.encode(['1 2 3','4 5','1 2 3'])
            self.assertEqual(values.shape,(3,3072));self.assertTrue(np.allclose(np.linalg.norm(values,axis=1),1))
            self.assertTrue(np.array_equal(values[0],values[2]))
            embedder.encode(['1 2 3','4 5']);self.assertEqual(len(backend.calls),1)
            embedder.cache.close()
            reloaded=AzureFullTextEmbedder(cfg,backend,Tokenizer());reloaded.encode(['4 5'])
            self.assertEqual(len(backend.calls),1);reloaded.cache.close()

    def test_full_text_beyond_8192_is_not_truncated(self):
        with tempfile.TemporaryDirectory() as directory:
            cfg=QAConfig(output=Path(directory));backend=Backend();embedder=AzureFullTextEmbedder(cfg,backend,Tokenizer())
            text=' '.join(str(i) for i in range(9000));embedder.encode([text])
            windows=[w for batch in backend.calls for w in batch]
            self.assertEqual(len(windows),2);self.assertTrue(all(len(w)<=8192 for w in windows))
            self.assertEqual(windows[-1][-1],8999)
            self.assertFalse(embedder.diagnostics(text)['silently_truncated']);embedder.cache.close()

    def test_batch_token_budget_and_bad_dimension(self):
        with tempfile.TemporaryDirectory() as directory:
            cfg=QAConfig(output=Path(directory),embedding_batch_tokens=5);backend=Backend()
            embedder=AzureFullTextEmbedder(cfg,backend,Tokenizer());embedder.encode(['1 2 3','4 5 6','7 8'])
            self.assertTrue(all(sum(map(len,b))<=5 for b in backend.calls));embedder.cache.close()
        with tempfile.TemporaryDirectory() as directory:
            embedder=AzureFullTextEmbedder(QAConfig(output=Path(directory)),Backend(1536),Tokenizer())
            with self.assertRaises(ValueError):embedder.encode(['1 2 3'])
            embedder.cache.close()

    def test_no_local_cache_or_model_fallback(self):
        with tempfile.TemporaryDirectory() as directory:
            root=Path(directory)/'dominio/embeddings';root.mkdir(parents=True);(root/'cache.npz').write_bytes(b'local')
            with self.assertRaises(ValueError):AzureFullTextEmbedder(QAConfig(output=Path(directory)),Backend(),Tokenizer())
        with self.assertRaises(ValueError):QAConfig(embedding_deployment='embedding-3-small-global').validate()

    def test_azure_backend_budget_and_request_payload(self):
        with tempfile.TemporaryDirectory() as directory:
            cfg=QAConfig(output=Path(directory),max_calls=1);store=RunStore(cfg);requests=[]
            def create(**kwargs):
                requests.append(kwargs);return SimpleNamespace(data=[],model='text-embedding-3-large',
                    usage=SimpleNamespace(prompt_tokens=3,total_tokens=3))
            backend=AzureEmbeddingBackend(cfg,store,SimpleNamespace(embeddings=SimpleNamespace(create=create)))
            backend.create([[1,2,3]])
            self.assertEqual(requests[0]['model'],'embedding-3-large-global')
            self.assertNotIn('reasoning_effort',requests[0]);self.assertNotIn('temperature',requests[0])
            with self.assertRaises(CallLimitReached):backend.create([[1]])
            self.assertEqual(store.state['calls_by_role']['embeddings'],1)

    def test_transient_azure_error_retries_and_records_attempts(self):
        with tempfile.TemporaryDirectory() as directory:
            requests=[]
            def create(**kwargs):
                requests.append(kwargs)
                if len(requests)==1:
                    error=RuntimeError('rate limit');error.status_code=429;raise error
                return SimpleNamespace(data=[],model='text-embedding-3-large',usage=None)
            backend=AzureEmbeddingBackend(QAConfig(output=Path(directory)),client=SimpleNamespace(
                embeddings=SimpleNamespace(create=create)))
            with patch('pipeline.fase_4.azure_embeddings.time.sleep'):backend.create([[1,2]])
            record=json.loads((Path(directory)/'chamadas_embeddings.jsonl').read_text())
            self.assertEqual(record['http_attempts'],2);self.assertIsNone(record['error_type'])

    def test_generic_terms_demoted_and_domain_scope_prompt(self):
        captured=[]
        def call(prompt,**kwargs):
            captured.append(kwargs['system']);return {'facetas':[{'termos_fortes':['KPI','manutencao em atraso'],'termos_apoio':[]}]}
        result=ScopedFacetClient(SimpleNamespace(complete_json=call)).complete_json('scope',system='base')
        self.assertEqual(result['facetas'][0]['termos_fortes'],['manutencao em atraso'])
        self.assertIn('KPI',result['facetas'][0]['termos_apoio']);self.assertIn('FPSO',captured[0])

    def test_bad_or_missing_vector_response_is_not_cached(self):
        with tempfile.TemporaryDirectory() as directory:
            backend=SimpleNamespace(settings=None,create=lambda inputs:SimpleNamespace(data=[]))
            embedder=AzureFullTextEmbedder(QAConfig(output=Path(directory)),backend,Tokenizer())
            try:
                with self.assertRaises(ValueError):embedder.encode(['1 2'])
                self.assertEqual(embedder.cache.execute('SELECT count(*) FROM vectors').fetchone()[0],0)
            finally:embedder.close()

    def test_protocol_change_rejects_existing_cache(self):
        with tempfile.TemporaryDirectory() as directory:
            cfg=QAConfig(output=Path(directory));embedder=AzureFullTextEmbedder(cfg,Backend(),Tokenizer());embedder.close()
            cfg.embedding_overlap_tokens=32
            with self.assertRaises(ValueError):AzureFullTextEmbedder(cfg,Backend(),Tokenizer())


if __name__=='__main__':unittest.main()
