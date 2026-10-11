"""Testes offline de download/extração/recuperação/integração, sem Azure."""
import hashlib
import io
import json
import tempfile
import unittest
import zipfile
from pathlib import Path
from types import SimpleNamespace
from unittest.mock import patch

import numpy as np

from pipeline.domain_corpora.extract import regis_pages, pdf_pages, accepted_pages, ExtractionRejected
from pipeline.domain_corpora.install_corpora import html_links, regis_members, include_petroles, canonical_document_url, discover
from pipeline.domain_corpora.io_utils import HTTP, RemoteZIP, atomic_json, file_hash
from pipeline.domain_corpora.manifest import load_manifest
from pipeline.fase_4.config import QAConfig, ROOT
from pipeline.fase_4.domain import DomainResources, TOPICOS, legacy
from pipeline.fase_4.multi_corpus import bilingual_facets, scan, plan_documents
from pipeline.fase_4.prompts_qa import source_text
from pipeline.fase_4.run_qa import parser, config_from_args
from pipeline.fase_4.scheduling import CoverageScheduler


def digest(data):return hashlib.sha256(data).hexdigest()


def setUpModule():
    # Mantém todos os temporários em uma pasta de teste conhecida do workspace.
    global previous_tempdir
    previous_tempdir=tempfile.tempdir
    base=ROOT/'dataset/test_tmp';base.mkdir(parents=True,exist_ok=True)
    tempfile.tempdir=str(base.resolve())


def tearDownModule():tempfile.tempdir=previous_tempdir


class Response(io.BytesIO):
    def __init__(self,data,status=200,headers=None):
        super().__init__(data);self.status=status;self.headers=headers or {};self.url='https://official.test/file'


class FakeHTTP(HTTP):
    def __init__(self,data,ignore_range=False):
        self.data=data;self.calls=[];self.ignore_range=ignore_range
    def open(self,url,headers=None):
        headers=headers or {};self.calls.append(headers)
        requested=headers.get('Range')
        if requested and not self.ignore_range:
            start,end=requested.removeprefix('bytes=').split('-');start=int(start);end=int(end) if end else len(self.data)-1
            data=self.data[start:end+1]
            return Response(data,206,{'Content-Range':f'bytes {start}-{end}/{len(self.data)}','Content-Length':str(len(data))})
        return Response(self.data,200,{'Content-Length':str(len(self.data))})


class Downloads(unittest.TestCase):
    def test_resume_and_integrity_and_cached_no_network(self):
        with tempfile.TemporaryDirectory() as directory:
            path=Path(directory)/'file.bin';data=b'original public file';http=FakeHTTP(data)
            path.with_suffix('.bin.part').write_bytes(data[:5])
            http.download('https://official.test/file',path,'sha256:'+digest(data),len(data))
            self.assertEqual(path.read_bytes(),data);self.assertEqual(http.calls[0]['Range'],'bytes=5-')
            http.download('https://official.test/file',path,'sha256:'+digest(data),len(data))
            self.assertEqual(len(http.calls),1)
            path.write_bytes(b'corrupt')
            http.download('https://official.test/file',path,'sha256:'+digest(data),len(data))
            self.assertEqual(path.read_bytes(),data);self.assertEqual(len(http.calls),2)

    def test_range_ignored_restarts(self):
        with tempfile.TemporaryDirectory() as directory:
            path=Path(directory)/'file.bin';path.with_suffix('.bin.part').write_bytes(b'old')
            FakeHTTP(b'new',True).download('https://official.test/file',path)
            self.assertEqual(path.read_bytes(),b'new')

    def test_bad_checksum_not_published(self):
        with tempfile.TemporaryDirectory() as directory:
            path=Path(directory)/'file.bin'
            with self.assertRaisesRegex(ValueError,'Checksum'):
                FakeHTTP(b'bad').download('https://official.test/file',path,'sha256:'+digest(b'good'))
            self.assertFalse(path.exists());self.assertFalse(path.with_suffix('.bin.part').exists())

    def test_complete_partial_after_interruption_does_not_request_416(self):
        with tempfile.TemporaryDirectory() as directory:
            path=Path(directory)/'file.bin';data=b'finished before crash';http=FakeHTTP(data)
            path.with_suffix('.bin.part').write_bytes(data)
            http.download('https://official.test/file',path,'sha256:'+digest(data),len(data))
            self.assertEqual(path.read_bytes(),data);self.assertFalse(http.calls)

    def test_remote_zip_crc_and_metadata_excluded(self):
        data=io.BytesIO()
        with zipfile.ZipFile(data,'w',zipfile.ZIP_DEFLATED) as z:
            z.writestr('repo/documents/example.xml','<doc><text>body</text></doc>')
            z.writestr('repo/queries.xml','queries');z.writestr('repo/qrels.txt','qrels')
        raw=data.getvalue();http=FakeHTTP(raw);remote=RemoteZIP(http,'https://official.test/file',len(raw))
        with zipfile.ZipFile(remote) as z:
            members=regis_members(z);self.assertEqual(len(members),1)
            self.assertIn(b'body',z.read(members[0]))

    def test_remote_zip_requires_real_ranges(self):
        with self.assertRaisesRegex(ValueError,'HTTP Range'):
            RemoteZIP(FakeHTTP(b'abcdef',True),'https://official.test/file',6).read(2)


class Extraction(unittest.TestCase):
    def test_real_solr_regis_format(self):
        xml=b'<add><doc><field name="docid">BR-42</field><field name="filename">paper.pdf</field><field name="text">pressure\nflow control</field></doc></add>'
        title,docid,pages=regis_pages(xml)
        self.assertEqual((title,docid),('paper.pdf','BR-42'))
        self.assertEqual(pages,[{'page':None,'text':'pressure\nflow control'}])

    def test_xml_entities_rejected(self):
        with self.assertRaisesRegex(ValueError,'DTD'):
            regis_pages(b'<!DOCTYPE doc [<!ENTITY bomb "danger">]><doc><text>&bomb;</text></doc>')

    def test_missing_body_not_metadata_as_corpus(self):
        with self.assertRaisesRegex(ValueError,'corpo'):
            regis_pages(b'<doc><title>A scientific paper</title></doc>')

    def test_empty_pdf_quarantined(self):
        from pypdf import PdfWriter
        with tempfile.TemporaryDirectory() as directory:
            path=Path(directory)/'blank.pdf';writer=PdfWriter();writer.add_blank_page(300,300);writer.write(path)
            with self.assertRaises(ExtractionRejected):accepted_pages(list(pdf_pages(path)))

    def test_page_quality_preserves_original_number(self):
        kept,issues=accepted_pages([{'page':1,'text':'cover'},{'page':2,'text':'pump pressure and flow control '*20}])
        self.assertEqual(kept[0]['page'],2);self.assertEqual(issues[0]['page'],1)

    def test_html_content_scope(self):
        links=list(html_links(b'<nav><a href="/menu.pdf">menu</a></nav><main><a href="/report.pdf">Report</a></main>',
                              'https://official.test/catalog'))
        self.assertEqual(links,[('https://official.test/report.pdf','Report')])

    def test_anp_confirmed_path_migration(self):
        url='https://www.gov.br/anp/pt-br/seguranca-operacional-e-meio-ambiente/report.pdf'
        self.assertEqual(canonical_document_url('anp',url),url.replace('seguranca-operacional-e-meio-ambiente','seguranca-operacional'))
        self.assertEqual(canonical_document_url('hse',url),url)

    def test_bsee_pagination_and_detail_links(self):
        from pipeline.domain_corpora.catalog import BSEE_INDEX
        pages={BSEE_INDEX:b'<main><table><tbody><tr><td><a href="/safety-alerts/one">One</a></td></tr></tbody></table><ul class="usa-pagination__list js-pager__items"><li><a href="?page=1">Next</a></li></ul></main>',
            BSEE_INDEX+'?page=1':b'<main><table><tbody><tr><td><a href="/safety-alerts/two">Two</a></td></tr></tbody></table></main>',
            'https://www.bsee.gov/safety-alerts/one':b'<main><a href="/sites/bsee.gov/files/one.pdf">One</a></main>',
            'https://www.bsee.gov/safety-alerts/two':b'<main><a href="/sites/bsee.gov/files/two.pdf">Two</a></main>'}
        http=SimpleNamespace(bytes=lambda url:pages[url]);warnings=[]
        with tempfile.TemporaryDirectory() as directory:
            found=discover('bsee',http,Path(directory),0,warnings)
        self.assertFalse(warnings)
        self.assertTrue(any(url.endswith('one.pdf') for url,_ in found))
        self.assertTrue(any(url.endswith('two.pdf') for url,_ in found))


def fixture(root):
    """Cinco coleções pequenas, com idioma/jurisdição e SHA reais."""
    rows=[]
    petro=root/'petroles.txt';petro.write_text(('bomba fluido pressao '*100)+'\n',encoding='utf-8')
    rows.append({'id':'petroles','format':'petroles_txt','documents':1,
                 'files':[{'path':'petroles.txt','sha256':file_hash(petro),'bytes':petro.stat().st_size}]})
    for name,lang,jur in [('anp','pt','BR'),('hse','en','UK'),('bsee','en','US'),('regis','pt','not_specified')]:
        pages=root/(name+'.jsonl')
        words='pump pressure fluid ' if lang=='en' else 'bomba pressao fluido '
        with pages.open('w',encoding='utf-8') as stream:
            for page in (1,2):
                stream.write(json.dumps({'collection':name,'document_id':name+'-doc','language':lang,
                    'jurisdiction':jur,'title':name+' title','page':page,'url':'https://official.test/'+name,
                    'text':words*100})+'\n')
        rows.append({'id':name,'format':'pages_jsonl','documents':1,'path':pages.name,'sha256':file_hash(pages)})
    path=root/'manifest.json';atomic_json(path,{'schema':'petroquest-domain-corpora-v1','ready':True,'sample':False,'collections':rows})
    return path


class FakeTranslator:
    def __init__(self):self.calls=0
    def complete_json(self,prompt,**kwargs):
        self.calls+=1
        return {'translations':[{'id':r['id'],'query_en':'pump fluid pressure','strong_en':['pump'],
                                'support_en':['fluid','pressure']} for r in json.loads(prompt)]}


class Embedder:
    def __init__(self,*args,**kwargs):pass
    def encode(self,texts):
        vectors=[]
        for text in texts:
            rng=np.random.default_rng(int(digest(text.encode())[:8],16));v=rng.normal(size=8)
            vectors.append(v/np.linalg.norm(v))
        return np.array(vectors,dtype=np.float32)
    def diagnostics(self,text):return {'test':True}
    def salvar_cache(self):pass


class Retrieval(unittest.TestCase):
    def test_petroles_nilc_rejected(self):
        with tempfile.TemporaryDirectory() as directory:
            path=Path(directory)/'NILC.txt';path.write_text('unrelated')
            with self.assertRaisesRegex(ValueError,'NILC'):include_petroles(None,[path],Path(directory))

    def test_sample_and_corruption_block_before_api(self):
        with tempfile.TemporaryDirectory() as directory:
            root=Path(directory);path=fixture(root);m=json.loads(path.read_text())
            m['sample']=True;atomic_json(path,m)
            with self.assertRaisesRegex(ValueError,'amostra'):load_manifest(path)
            load_manifest(path,True)
            (root/'hse.jsonl').write_text('corrupt')
            with self.assertRaisesRegex(ValueError,'corrompido'):load_manifest(path,True)

    def test_manifest_cli_disables_automatic_petroles_discovery(self):
        cfg=config_from_args(parser().parse_args(['--corpus-manifest','dataset/manifest.json']))
        self.assertIsNone(cfg.corpus_dir);self.assertFalse(cfg.enable_cosine_filter);self.assertFalse(cfg.enable_saturation_stop)

    def test_bilingual_translation_cached(self):
        with tempfile.TemporaryDirectory() as directory:
            facet=legacy.Faceta('f','topic','sub','Bomba','fluxo','bomba pressao',['bomba'],['fluido'])
            client=FakeTranslator();path=Path(directory)/'translations.json'
            output=bilingual_facets([facet],client,path,legacy)
            self.assertIn('pump',output[0].termos_fortes)
            bilingual_facets([facet],client,path,legacy);self.assertEqual(client.calls,1)

    def test_collection_quotas_long_xml_and_page_boundaries(self):
        with tempfile.TemporaryDirectory() as directory:
            root=Path(directory);manifest,collections=load_manifest(fixture(root))
            cfg=legacy.Config(out_dir=root/'index');facet=legacy.Faceta('f','topic','sub','Bomba','fluxo','pump bomba',
                    ['bomba','pump'],['fluido','fluid','pressure','pressao'])
            results=scan([facet],collections,cfg,legacy,2,'signature')['f']
            counts=__import__('collections').Counter(c['collection'] for c in results)
            self.assertEqual(set(counts),{'petroles','anp','hse','bsee','regis'})
            self.assertTrue(all(0<n<=2 for n in counts.values()))
            self.assertTrue(all(c['page'] in (1,2) for c in results if c['collection']!='petroles'))
            self.assertTrue(all(len(c['texto'].split())<=cfg.max_palavras for c in results))
            plans=plan_documents([facet],{'f':results},Embedder(),cfg,legacy)
            self.assertEqual(len(plans),5)
            self.assertEqual(len({c['chunk_id'] for c in results}),len(results))
            again=scan([facet],collections,cfg,legacy,2,'signature')['f']
            self.assertEqual({c['chunk_id'] for c in results},{c['chunk_id'] for c in again})

    def test_short_final_window_not_lost(self):
        with tempfile.TemporaryDirectory() as directory:
            root=Path(directory);path=fixture(root);_,collections=load_manifest(path)
            for c in collections:
                if c['id']=='hse':
                    row={'collection':'hse','document_id':'short','title':'Short report','page':4,'text':'pump fluid pressure '*30}
                    c['resolved_path'].write_text(json.dumps(row)+'\n')
            facet=legacy.Faceta('f','topic','sub','Bomba','fluxo','pump',['pump'],['pressure'])
            result=scan([facet],collections,legacy.Config(out_dir=root/'index'),legacy,2,'short')['f']
            self.assertTrue(any(c['document_id']=='short' and c['page']==4 for c in result))

    def test_domain_audit_and_scheduler_five_collections(self):
        with tempfile.TemporaryDirectory() as directory:
            root=Path(directory);path=fixture(root);topic=next(iter(TOPICOS));sub=next(iter(TOPICOS[topic]))
            facet=legacy.Faceta('f',topic,sub,'Bomba','fluxo','bomba pressao',['bomba'],['fluido'])
            cfg=QAConfig(output=root/'run',corpus_manifest=path,corpus_dir=None)
            cfg.output.mkdir();client=FakeTranslator();audits=[]
            def audit(_,context,*args):
                audits.append(context)
                return {'approved':True,'allowed_chunk_ids':[c['chunk_id'] for c in context['chunks']],
                        'targets':['Função da bomba'],'claims':[],'limitations':[],'original_context':'produção','transferability':'técnica'}
            with patch.object(legacy,'extrair_facetas',return_value=[facet]),\
                 patch('pipeline.fase_4.embedding.FullTextEmbedder',Embedder),\
                 patch('pipeline.fase_4.domain.audit_source',side_effect=audit),\
                 patch('pipeline.fase_4.domain.audited_document',return_value='Afirmações verificadas'),\
                 patch.object(DomainResources,'make_codebook',return_value=SimpleNamespace(k=3)):
                domain=DomainResources(cfg,client).prepare([topic])
                signature=domain.signature
                (root/'hse.jsonl').touch();path.touch()
                domain=DomainResources(cfg,client).prepare([topic])
                self.assertEqual(domain.signature,signature)
                self.assertEqual(client.calls,1)
            documents=domain.documents(topic,sub);self.assertEqual(len(documents),5);self.assertEqual(len(audits),10)
            self.assertEqual({d['collections'][0] for d in documents},{'petroles','anp','hse','bsee','regis'})
            chunk=next(c for d in documents for c in d['chunks'] if c['collection']=='hse')
            self.assertEqual(chunk['jurisdiction'],'UK');self.assertIn('UK',source_text([chunk]));self.assertIn('page',source_text([chunk]))
            store=SimpleNamespace(state={},records=[],rounds=[],save_state=lambda:None)
            scheduler=CoverageScheduler(cfg,domain,store);selected=[]
            for _ in range(5):
                context,difficulty,selection,_=scheduler.choose(topic);selected+=context['collections']
                store.rounds.append({'topic':topic,'subtopic':sub,'doc_id':context['doc_id'],
                    'facet_id':context['facet_id'],'requested_difficulty':difficulty,'selection':selection})
            self.assertEqual(len(set(selected)),5)


if __name__=='__main__':unittest.main()
