"""Composição 10x1000, proveniência e integração QA; sem rede ou Azure real."""
import json
import tempfile
import unittest
from pathlib import Path
from types import SimpleNamespace
from unittest.mock import patch
import numpy as np

from pipeline.fase_4.config import QAConfig
from pipeline.fase_4.context_composition import compose_document, validate_composition, material_report
from pipeline.fase_4.domain import DomainResources, TOPICOS, legacy
from pipeline.fase_4.multi_corpus import scan, plan_documents
from pipeline.fase_4.scheduling import target_list
from pipeline.fase_4.storage import CallLimitReached
from pipeline.fase_4.run_qa import parser,config_from_args
from pipeline.fase_4.engine import execute, ROLES
from pipeline.fase_4.scoring import BOOLEANS, WEIGHTS
from pipeline.fase_4.difficulty import DIMENSIONS
from test_corpora import setUpModule,tearDownModule,fixture,FakeTranslator,Embedder


def context():
    return {'doc_id':'f-context-d0','facet_id':'f','facet_title':'planejamento da manutenção',
        'topic':'topic','subtopic':'sub','focus':'planejamento','scope':'manutenção FPSO',
        'chunks':[{'chunk_id':f'c{i}','collection':('anp','petroles','regis','bsee','hse')[i%5],
                   'texto':f'Manutenção planejada exige recursos e acompanhamento. Fonte {i}. '+ 'conteúdo '*993}
                  for i in range(10)]}


def response(ctx):
    ids=[c['chunk_id'] for c in ctx['chunks']]
    return {'document':'# Manutenção\nA manutenção planejada exige recursos e acompanhamento. ['+ids[0]+']',
        'used_chunk_ids':ids,'targets':[{'description':'Avaliar planejamento de recursos','chunk_ids':[ids[0]]}],
        'warnings':['Conteúdo experimental, sem auditoria independente']}


class Composer:
    def __init__(self):self.calls=0
    def complete_json(self,prompt,**kwargs):
        self.calls+=1
        payload=json.JSONDecoder().raw_decode(prompt.split('\n',1)[1])[0]
        return response(payload)


class Composition(unittest.TestCase):
    def test_real_document_saved_with_ten_sources_and_cache(self):
        with tempfile.TemporaryDirectory() as directory:
            client=Composer();root=Path(directory);ctx=context()
            result=compose_document(client,ctx,root,'sig',32000)
            self.assertEqual(result['status'],'ready');self.assertEqual(result['retrieved_chunks'],10)
            self.assertGreaterEqual(result['retrieved_words'],9900);self.assertFalse(result['factually_audited'])
            self.assertTrue((root/'composicoes/f-context-d0.json').is_file())
            self.assertTrue((root/'contextos_candidatos/f-context-d0.json').is_file())
            self.assertEqual(compose_document(client,ctx,root,'sig',32000),result)
            self.assertEqual(client.calls,1)

    def test_wrong_source_and_malformed_targets_rejected(self):
        for change in ({'used_chunk_ids':['invented']},
                       {'targets':[{'description':'alvo','chunk_ids':['invented']}]},
                       {'targets':[{'description':'alvo','chunk_ids':[]}]},
                       {'document':12},{'warnings':'bad'}):
            with self.assertRaises(ValueError):validate_composition({**response(context()),**change},context()['chunks'])

    def test_content_warning_is_not_a_factual_gate(self):
        raw=response(context());raw['warnings']=['Há uma contradição a revisar posteriormente']
        result=validate_composition(raw,context()['chunks'])
        self.assertEqual(result['status'],'ready')
        report=material_report(result)
        self.assertFalse(report['factually_audited']);self.assertNotIn('approved',report)
        targets=target_list({'topic':'t','subtopic':'s','source_audit':report})
        self.assertEqual(targets[0]['chunk_ids'],['c0'])

    def test_no_useful_material_returns_diagnostic(self):
        raw={'document':'','used_chunk_ids':[],'targets':[],'warnings':['Nenhum conteúdo útil']}
        self.assertEqual(validate_composition(raw,context()['chunks'])['status'],'no_material')
        with self.assertRaises(ValueError):validate_composition({**raw,'document':'texto'},context()['chunks'])

    def test_invalid_response_corrected_with_previous_answer(self):
        with tempfile.TemporaryDirectory() as directory:
            calls=[]
            def call(prompt,**kwargs):
                calls.append(prompt)
                return {'document':'bad'} if len(calls)==1 else response(context())
            result=compose_document(SimpleNamespace(complete_json=call),context(),Path(directory),'sig',32000)
            self.assertEqual(result['status'],'ready');self.assertIn('bad',calls[1])
            self.assertEqual(len((Path(directory)/'composicoes/f-context-d0.respostas.jsonl').read_text().splitlines()),2)

    def test_twice_invalid_is_quarantined_not_approved(self):
        with tempfile.TemporaryDirectory() as directory:
            client=SimpleNamespace(complete_json=lambda *a,**k:{'document':'bad'})
            result=compose_document(client,context(),directory,'sig',32000)
            self.assertEqual(result['status'],'invalid_response');self.assertFalse(result['factually_audited'])

    def test_changed_evidence_does_not_reuse_old_document(self):
        with tempfile.TemporaryDirectory() as directory:
            compose_document(Composer(),context(),directory,'sig',32000)
            changed=context();changed['chunks'][0]['texto']+=' Texto mudou.'
            with self.assertRaisesRegex(ValueError,'cache incompatível'):
                compose_document(Composer(),changed,directory,'sig',32000)

    def test_api_budget_not_swallowed_as_content_failure(self):
        with tempfile.TemporaryDirectory() as directory:
            def call(*a,**k):raise CallLimitReached('budget')
            with self.assertRaises(CallLimitReached):
                compose_document(SimpleNamespace(complete_json=call),context(),directory,'sig',32000)


class LargeWindows(unittest.TestCase):
    def scan_units(self,root,units):
        cfg=legacy.Config(out_dir=root,alvo_palavras_trecho=1000,min_palavras=80,max_palavras=1200,max_linhas_trecho=1000)
        cfg.join_document_pages=True
        facet=legacy.Faceta('f','t','s','bomba','pressão','bomba',['bomba'],['pressao'])
        with patch('pipeline.fase_4.multi_corpus.iter_units',return_value=iter(units)):
            return scan([facet],[],cfg,legacy,60,'sig')['f']

    def unit(self,doc,page):
        return {'collection':'anp','document_id':doc,'title':doc,'page':page,'text':('bomba pressao fluido '+doc+' ')*80}

    def test_adjacent_pages_create_1000_word_chunks_with_spans(self):
        with tempfile.TemporaryDirectory() as directory:
            results=self.scan_units(Path(directory),[self.unit('doc',i) for i in range(1,6)])
            large=[c for c in results if len(c['texto'].split())>=1000]
            self.assertTrue(large);self.assertTrue(all(len(c['texto'].split())<=1200 for c in results))
            for c in large:
                self.assertGreater(len(c['pages']),1);self.assertIsNone(c['page'])
                self.assertEqual([s['page'] for s in c['page_spans']],c['pages'])
            self.assertTrue(all('doc:p' in c['chunk_id'] for c in results))

    def test_never_join_different_documents_or_missing_pages(self):
        with tempfile.TemporaryDirectory() as directory:
            results=self.scan_units(Path(directory),[self.unit('docA',1),self.unit('docA',3),self.unit('docB',1)])
            self.assertTrue(all(len(c['pages'])==1 for c in results))
            self.assertFalse(any('docA' in c['texto'] and 'docB' in c['texto'] for c in results))

    def test_ten_chunks_one_document_per_facet(self):
        facet=legacy.Faceta('f','t','s','title','focus','query',[],[])
        candidates=[{**c,'lex_score':3} for c in context()['chunks']]
        plans=plan_documents([facet],{'f':candidates},Embedder(),legacy.Config(
            n_trechos_por_documento=10,n_documentos_por_faceta=1),legacy)
        self.assertEqual(len(plans),1);self.assertEqual(len(plans[0]['chunk_ids']),10)
        self.assertEqual(set(plans[0]['collections']),{'anp','hse','bsee','petroles','regis'})

    def test_defaults_and_cli(self):
        cfg=config_from_args(parser().parse_args(['--context-mode','composed','--chunk-words','1000','--chunks-per-facet','10','--observe-only']))
        cfg.validate();self.assertEqual(cfg.context_mode,'composed');self.assertEqual(cfg.chunk_words,1000)
        self.assertEqual(cfg.chunks_per_facet,10)
        self.assertFalse(cfg.enable_cosine_filter or cfg.enable_saturation_stop or cfg.filter_redundancy)

    def test_domain_composes_without_calling_source_audit(self):
        with tempfile.TemporaryDirectory() as directory:
            root=Path(directory);manifest=fixture(root);topic=next(iter(TOPICOS));sub=next(iter(TOPICOS[topic]))
            cfg=QAConfig(output=root/'run',corpus_manifest=manifest,corpus_dir=None);cfg.output.mkdir()
            facet=legacy.Faceta('f',topic,sub,'Bomba','fluxo','bomba',['bomba'],['fluido'])
            composer=Composer()
            with patch.object(legacy,'extrair_facetas',return_value=[facet]),\
                 patch('pipeline.fase_4.azure_embeddings.AzureFullTextEmbedder',Embedder),\
                 patch('pipeline.fase_4.domain.audit_source',side_effect=AssertionError('Auditor não deve ser chamado')):
                domain=DomainResources(cfg,FakeTranslator());domain.composition_client=composer
                domain.prepare([topic])
            docs=domain.documents(topic,sub);self.assertEqual(len(docs),1)
            self.assertIn('# Manutenção',docs[0]['document']);self.assertEqual(docs[0]['context_mode'],'composed')
            self.assertFalse(docs[0]['source_audit']['factually_audited']);self.assertEqual(composer.calls,1)
            self.assertTrue((cfg.output/'dominio/documentos/f-context-d0.md').is_file())
            coverage=json.loads((cfg.output/'cobertura_dominio.json').read_text())[0]
            self.assertEqual(coverage['composed_documents'],1);self.assertFalse(coverage['factually_audited'])
            self.assertEqual(coverage['documents_with_fewer_than_requested_chunks'],1)

    def test_document_reaches_generator_judge_and_difficulty_in_full_engine(self):
        with tempfile.TemporaryDirectory() as directory:
            root=Path(directory);manifest=fixture(root);topic=next(iter(TOPICOS));sub=next(iter(TOPICOS[topic]))
            cfg=QAConfig(output=root/'run',corpus_manifest=manifest,corpus_dir=None,topics=[topic],
                         limit_per_topic=1,batch_size=1,max_attempts_per_topic=1,max_refinements=0,max_calls=20)
            cfg.output.mkdir();facet=legacy.Faceta('f',topic,sub,'Bomba','fluxo','bomba',['bomba'],['fluido'])
            class E(Embedder):
                dim=8
                def encode(self,texts):return super().encode(texts) if texts else np.empty((0,8),dtype=np.float32)
            with patch.object(legacy,'extrair_facetas',return_value=[facet]),\
                 patch('pipeline.fase_4.azure_embeddings.AzureFullTextEmbedder',E):
                domain=DomainResources(cfg,FakeTranslator());domain.composition_client=Composer()
                domain.prepare([topic])
            doc=domain.documents(topic,sub)[0];chunk=doc['chunks'][0];captured={}
            class Backend:
                def __init__(self,role):self.role=role
                def complete_json(self,prompt,**kwargs):
                    captured[self.role]=prompt
                    if self.role=='generator':
                        targets=json.JSONDecoder().raw_decode(prompt.split('alvo no lote):\n',1)[1])[0]
                        return {'items':[{'question':'Por que é necessário acompanhar a condição de uma bomba?',
                            'answer':'Para identificar alterações de pressão e do fluido bombeado.',
                            'concept':'condição da bomba','target_id':targets[0]['target_id'],
                            'evidence':[{'chunk_id':chunk['chunk_id'],'quote':' '.join(chunk['texto'].split()[:8])}]}]}
                    if self.role=='judge':
                        items=json.JSONDecoder().raw_decode(prompt.split('Questões finais:\n',1)[1])[0]
                        return {'evaluations':[{'id':q['id'],**{k:True for k in BOOLEANS},
                            **{k:1. for k in WEIGHTS},'repairable':False,'reasons':{k:'Veredito simulado' for k in BOOLEANS},
                            'evidence_alignment':[{'claim':q['answer'],'chunk_ids':[chunk['chunk_id']]}],
                            'comment':'Fluxo validado com resposta simulada'} for q in items]}
                    if self.role=='difficulty':
                        items=json.JSONDecoder().raw_decode(prompt.split('independentemente:\n',1)[1])[0]
                        return {'evaluations':[{'id':q['id'],**{k:1 for k in DIMENSIONS},
                            'reasons':{k:'Avaliação simulada' for k in DIMENSIONS},'confidence':.99} for q in items]}
                    if self.role=='redundancy':
                        pairs=json.JSONDecoder().raw_decode(prompt.split('Compare TODOS os pares: ',1)[1])[0]
                        return {'pairs':[{'reference_id':p['reference_id'],'label':'distinct','confidence':1.,
                                          'reason':'Comparação simulada'} for p in pairs]}
                    raise AssertionError('Papel não esperado: '+self.role)
            seed={'id':'seed','question':'Como se mede a temperatura de um fluido?', 'answer':'Com um instrumento apropriado.',
                  'topic':'Outro tópico','subtopic':'Outro','selection_weight':1.,'origin':'human_seed'}
            external=[{'id':'arc_easy:test','question':'O que mede um termômetro?','answer':'Temperatura.'}]
            store=execute(cfg,backends={role:Backend(role) for role in ROLES},domain=domain,seeds=[seed],external=external)
            self.assertEqual(len(store.accepted),1);self.assertEqual(store.meta['status'],'completed')
            row=store.accepted[0];self.assertEqual(row['context_mode'],'composed')
            self.assertFalse(row['source_audit']['factually_audited'])
            for role in ('generator','judge'):self.assertIn(doc['document'],captured[role])
            self.assertNotIn('source_auditor',captured)
            self.assertIn('difficulty',captured)


if __name__=='__main__':unittest.main()
