import copy
import io
import json
import tempfile
import unittest
from contextlib import redirect_stdout
from pathlib import Path
from unittest.mock import patch

from pipeline.domain_corpora.io_utils import atomic_json,file_hash
from pipeline.domain_corpora.extract import pdf_pages,accepted_pages
from pipeline.qa_research.corpus import CorpusIndex
from pipeline.qa_research.v2.install_corpora import install,collect,CATALOG,error_record,main as install_main
from pipeline.qa_research.v2.language import (bilingual_search,validate_pairs,lint_ptbr,detect_language,audit_blocks)
from pipeline.qa_research.v2.questions import validate_qa_audit,QA_CRITERIA
from pipeline.qa_research.v2.tests.test_protocol import fixture_manifest


class RobustnessTests(unittest.TestCase):
    def setUp(self):
        self.temp=tempfile.TemporaryDirectory();self.root=Path(self.temp.name)
    def tearDown(self):self.temp.cleanup()

    def test_bilingual_retrieves_english_when_portuguese_has_no_matches(self):
        m=fixture_manifest(self.root/'corpus')
        data=json.loads(m.read_text(encoding='utf-8'));path=m.parent/'pages.jsonl'
        row=json.loads(path.read_text(encoding='utf-8'))
        row['text']='Chemical dosing flowrate is adjusted through the metering pump. The operator observes the flow and checks pump operation during the treatment process. '*4
        row['language']='en'
        path.write_text(json.dumps(row)+'\n',encoding='utf-8')
        data['collections'][0]['sha256']=file_hash(path);atomic_json(m,data)
        index=CorpusIndex(self.root/'index',manifest=m);index.build()
        pair=dict(pt='dosagem vazão coagulante',en='chemical dosing flowrate')
        validate_pairs({'pares':[pair]},3)
        self.assertFalse(index.search(pair['pt']))
        rows,traces=bilingual_search(index,[pair],10)
        self.assertTrue(rows);self.assertEqual([t['query_language'] for t in traces],['pt','en'])
        self.assertEqual(rows[0]['language'],'en')
        self.assertTrue(any(q['language']=='en' for q in rows[0]['bilingual_retrieval']['queries']))

    def test_query_pairs_cannot_drop_english_or_repeat_same_query(self):
        for pairs in ([{'pt':'consulta técnica brasileira'}],[{'pt':'chemical dosing system','en':'chemical dosing system'}]):
            with self.assertRaises(ValueError):validate_pairs({'pares':pairs},3)

    def test_ptbr_allows_industry_terms_but_flags_regional_words(self):
        self.assertFalse(lint_ptbr('A equipe acompanha a vazão durante o offloading no FPSO.'))
        self.assertTrue(lint_ptbr('A equipa verifica o caudal e o controlo.'))

    def test_statistical_language_is_recorded_without_discarding_source(self):
        english='The operator checks the equipment before starting the production system and monitors the water flow during normal operation. '*5
        pt='A equipe verifica os equipamentos antes da partida do sistema de produção e acompanha a vazão de água durante a operação normal. '*5
        self.assertEqual(detect_language(english)['language'],'en')
        self.assertEqual(detect_language(pt)['language'],'pt')
        self.assertTrue(lint_ptbr(english));self.assertFalse(lint_ptbr(pt))

    def test_audit_cannot_publish_foreign_language_despite_other_criteria(self):
        row=dict(aprovada=True,**{c:True for c in QA_CRITERIA},motivo='Teste',encaminhamento='aprovar')
        row['pt_br']=False
        with self.assertRaises(ValueError):validate_qa_audit(row)

    def test_document_locale_failures_become_rewrite_instructions(self):
        class FakeCalls:
            def call(self,role,system,payload,validate):
                d=dict(avaliacoes=[dict(id='B1',pt_br=False,terminologia_br=False,motivo='Rever português brasileiro.')])
                validate(d);return d
        report=audit_blocks([dict(id='B1',subtitulo='Operação',texto='A equipa verifica o caudal.')],FakeCalls())
        self.assertEqual(report['correcoes'][0]['blocos'],['B1'])

    def test_document_failure_does_not_block_healthy_source_but_strict_does(self):
        records=[dict(collection='kimray',document_id='d1',text='Texto técnico íntegro.')]
        failures=[dict(source='kimray',url='https://kimray.com/training/broken',error='PDF exige senha',category='password_protected')]
        with patch('pipeline.qa_research.v2.install_corpora.collect',return_value=(records,failures,{})):
            normal=install(self.root/'normal',['kimray'],None)
            strict=install(self.root/'strict',['kimray'],None,strict=True)
        self.assertTrue(normal['ready']);self.assertEqual(normal['status'],'ready_with_warnings')
        self.assertTrue(normal['errors']);self.assertFalse(strict['ready'])

    def test_retry_only_failed_url_and_preserve_other_collections(self):
        root=self.root/'installer';records=[dict(collection='kimray',document_id='good',text='Texto técnico íntegro.')]
        bad='https://kimray.com/training/failed'
        with patch('pipeline.qa_research.v2.install_corpora.collect',return_value=(records,[dict(source='kimray',url=bad,error='AES')],{})):
            install(root,['kimray'],None)
        previous=(root/'kimray/pages.jsonl').read_bytes()
        with patch('pipeline.qa_research.v2.install_corpora.collect',return_value=(records,[],{})) as mocked:
            fixed=install(root,['kimray'],None,retry_failed=True)
        self.assertEqual(mocked.call_args.kwargs['retry_urls'],[bad])
        self.assertTrue(fixed['ready']);self.assertEqual(fixed['errors'],[])
        self.assertEqual((root/'kimray/pages.jsonl').read_bytes(),previous)

    def test_recollection_preserves_previous_documents_when_network_fails(self):
        root=self.root/'installer';records=[dict(collection='kimray',document_id='good',text='Texto técnico íntegro.')]
        with patch('pipeline.qa_research.v2.install_corpora.collect',return_value=(records,[],{})):
            install(root,['kimray'],None)
        class BadHTTP:
            def download(self,*a):raise TimeoutError('network timeout')
        with redirect_stdout(io.StringIO()):
            preserved,errors,trace=collect('kimray',root,BadHTTP(),retry_urls=['https://kimray.com/training/failed'])
        self.assertEqual(preserved,records);self.assertEqual(errors[0]['category'],'timeout')

    def test_retry_preserves_combined_petroles_and_nonselected_collections(self):
        root=self.root/'combined';root.mkdir()
        path=root/'petroles.txt';path.write_text('Original do corpus existente.',encoding='utf-8')
        corpus=dict(id='petroles',format='petroles_txt',documents=1,files=[dict(path=path.name,sha256=file_hash(path))])
        atomic_json(root/'install_report.json',dict(collections=[corpus],selected_sources=['kimray'],errors=[],discovery={}))
        report=install(root,['kimray'],None,retry_failed=True)
        self.assertFalse(report['ready']);self.assertEqual(report['collections'][0]['id'],'petroles')

    def test_preflight_missing_crypto_preserves_existing_manifest(self):
        root=self.root/'preflight';root.mkdir()
        manifest=root/'manifest.json';manifest.write_text('{"ready":true}')
        with patch('pipeline.qa_research.v2.install_corpora.importlib.util.find_spec',return_value=None):
            with redirect_stdout(io.StringIO()):
                code=install_main(['--output',str(root),'--sources','offshorenorge','--retry-failed'])
        self.assertEqual(code,2);self.assertEqual(manifest.read_text(),'{"ready":true}')

    def test_missing_crypto_diagnostic_and_encrypted_pdf(self):
        self.assertEqual(error_record('offshorenorge','https://example.org',ImportError('cryptography>=3.1 is required for AES algorithm'))['category'],'missing_dependency')
        from pypdf import PdfWriter
        from pypdf.generic import DictionaryObject,NameObject,DecodedStreamObject
        writer=PdfWriter();page=writer.add_blank_page(width=600,height=800)
        font=DictionaryObject({NameObject('/Type'):NameObject('/Font'),NameObject('/Subtype'):NameObject('/Type1'),NameObject('/BaseFont'):NameObject('/Helvetica')})
        page[NameObject('/Resources')]=DictionaryObject({NameObject('/Font'):DictionaryObject({NameObject('/F1'):writer._add_object(font)})})
        stream=DecodedStreamObject()
        stream.set_data(b'BT /F1 10 Tf 20 750 Td (Public operational training document with enough text to validate extraction of an encrypted AES PDF file that opens without a reader password.) Tj ET')
        page[NameObject('/Contents')]=writer._add_object(stream)
        writer.encrypt('',owner_password='fixture-owner',algorithm='AES-256-R5')
        path=self.root/'aes.pdf';writer.write(path)
        pages,_=accepted_pages(list(pdf_pages(path)))
        self.assertIn('Public operational training',pages[0]['text'])


if __name__=='__main__':unittest.main()
