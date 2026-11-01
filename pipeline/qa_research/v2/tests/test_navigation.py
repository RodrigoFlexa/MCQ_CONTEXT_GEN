"""RSS/Atom descobrem artigos individuais, inclusive ao retomar o cache."""
import io
import json
import tempfile
import unittest
from contextlib import redirect_stdout
from pathlib import Path
from unittest.mock import patch

from pipeline.domain_corpora.io_utils import file_hash,atomic_json
from pipeline.qa_research.v2.install_corpora import install,CATALOG,HTML,permitted
from pipeline.qa_research.v2.navigation import feed_links


class NavigationTests(unittest.TestCase):
    def test_related_article_cards_do_not_replace_technical_body(self):
        parser=HTML()
        parser.feed('<nav>Menu</nav><section class="article-rte"><h2>Demulsification</h2>'
            '<p>The chemical destabilizes the emulsion.</p></section>'
            '<article class="related-resource"><p>Marketing case titles</p></article>')
        self.assertIn('destabilizes',parser.text())
        self.assertNotIn('Marketing',parser.text())
        self.assertNotIn('Menu',parser.text())

    def test_targeted_sources_have_allowed_seeds_and_bounded_hosts(self):
        for name in ('dupont','bakerhughes','slb_chemicals'):
            spec=CATALOG[name]
            self.assertTrue(all(permitted(url,spec) for url in spec['seeds']))
            self.assertFalse(permitted('https://example.org/unrelated',spec))

    def test_rss_atom_and_entity_rejection(self):
        self.assertEqual(feed_links('<rss><channel><item><title>A</title><link>https://example.org/a</link></item></channel></rss>'),['https://example.org/a'])
        self.assertEqual(feed_links('<feed xmlns="http://www.w3.org/2005/Atom"><entry><link href="https://example.org/a"/><link rel="self" href="https://example.org/api"/></entry></feed>'),['https://example.org/a'])
        self.assertIsNone(feed_links('<html><title>Manual</title></html>'))
        with self.assertRaises(ValueError):feed_links('<!DOCTYPE rss [<!ENTITY x "expand">]><rss>&x;</rss>')

    def test_feed_discovers_documents_and_cached_catalog_still_discovers(self):
        with tempfile.TemporaryDirectory() as directory:
            root=Path(directory)
            feed='https://www.imca-int.com/resources/safety/safety-flashes/rss-feed/'
            article='https://www.imca-int.com/resources/safety/safety-flashes/chemical/'
            text='The operator checks chemical storage conditions before starting the transfer and confirms the compatibility of materials with the chemical product. '*4
            content={feed:f'<rss><channel><title>Safety</title><item><title>Individual title</title><link>{article}</link></item></channel></rss>',
                article:f'<html><title>Individual title</title><main><p>{text}</p></main></html>'}
            class HTTP:
                def __init__(self):self.visited=[]
                def download(self,url,path):
                    self.visited.append(url);path.parent.mkdir(parents=True,exist_ok=True)
                    path.write_text(content[url],encoding='utf-8')
                    return dict(final_url=url,sha256=file_hash(path))
            spec=dict(CATALOG['imca'],seeds=[feed])
            with patch.dict(CATALOG,imca=spec),redirect_stdout(io.StringIO()):
                first=install(root,['imca'],HTTP())
                http=HTTP();second=install(root,['imca'],http)
            self.assertTrue(first['ready']);self.assertTrue(second['ready'])
            rows=[json.loads(line) for line in (root/'imca/pages.jsonl').read_text(encoding='utf-8').splitlines()]
            self.assertEqual({r['url'] for r in rows},{article})
            self.assertEqual({r['title'] for r in rows},{'Individual title'})
            self.assertIn(article,http.visited)
            self.assertEqual(second['discovery']['imca']['normalized_reused'],2)

    def test_bad_previous_feed_is_not_restored_when_network_fails(self):
        with tempfile.TemporaryDirectory() as directory:
            root=Path(directory);path=root/'imca/pages.jsonl';path.parent.mkdir()
            bad=dict(collection='imca',document_id='bad',url='https://www.imca-int.com/resources/safety/safety-flashes/rss-feed/',title='t'*130277,text='Mixed incidents')
            good=dict(collection='imca',document_id='good',url='https://www.imca-int.com/resources/safety/safety-flashes/chemical/',title='Individual safety flash',text='Technical conditions')
            path.write_text('\n'.join(json.dumps(r) for r in (bad,good))+'\n',encoding='utf-8')
            atomic_json(root/'install_report.json',dict(collections=[dict(id='imca',format='pages_jsonl',path='imca/pages.jsonl',sha256=file_hash(path))],selected_sources=['imca']))
            class HTTP:
                def download(self,*args):raise TimeoutError('offline')
            with redirect_stdout(io.StringIO()):result=install(root,['imca'],HTTP())
            rows=[json.loads(line) for line in path.read_text(encoding='utf-8').splitlines()]
            self.assertEqual(rows,[good]);self.assertTrue(result['ready'])
            self.assertEqual(result['discovery']['imca']['navigation_excluded'],1)
            self.assertTrue((root/'imca/navigation_excluded.json').exists())
