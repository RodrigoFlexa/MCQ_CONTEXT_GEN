"""Regressões da pesquisa: pertinência, diversidade, lacunas e parada delimitada."""
import asyncio
import unittest

from pipeline.qa_research.v3.__main__ import configuration
from pipeline.qa_research.v3.context import clean_headings,editor_issues
from pipeline.qa_research.v3.retrieval import research,candidates


def source(n,collection='manual',url=None):
    return dict(chunk_id=str(n),content_hash=str(n),document_id=str(n),collection=collection,
        texto='Condições técnicas integrais '+str(n),title='Manual',language='en',
        jurisdiction='NO',document_type='guia_profissional',url=url or 'https://example.org/'+str(n))


class Index:
    def __init__(self):self.last_query_trace={};self.queries=[]
    def search(self,query,**kwargs):
        self.queries.append(query);self.last_query_trace=dict(query=query)
        return [source(3)] if 'nova' in query else [source(1),source(2)]


class Calls:
    def __init__(self):self.inputs=[]
    async def call(self,role,label,payload,validate,**kwargs):
        self.inputs.append(payload)
        result=dict(avaliacoes=[dict(id=s['id'],pertinencia='descartar' if s['texto'].endswith('2') else 'direta',
            motivo='Pertinência simulada',aplicabilidade='Condições do processo, sem obrigação legal brasileira') for s in payload['candidatas']],
            lacunas=['P1'],consultas=[dict(pt='nova busca dosagem',en='nova search dosing')])
        validate(result);return result


class ResearchTests(unittest.TestCase):
    def test_followup_is_bounded_and_excluded_passage_never_reaches_writer(self):
        index=Index();calls=Calls()
        selected,detail=asyncio.run(research(index,dict(id='S1',titulo='Dosagem',pontos=['P1'],
            consultas=[dict(pt='dosagem química',en='chemical dosing')]),{},[dict(id='P1')],configuration(),calls))
        self.assertEqual(len(calls.inputs),2)
        self.assertEqual(len(index.queries),4)
        self.assertEqual({s['texto'] for s in selected},{source(1)['texto'],source(3)['texto']})
        self.assertEqual(len(detail['consultas']),4)
        self.assertTrue(all(s['jurisdiction']=='NO' for s in selected))

    def test_no_new_passages_stops_without_second_selection(self):
        class Same(Index):
            def search(self,query,**kwargs):return super().search('original',**kwargs)
        calls=Calls()
        asyncio.run(research(Same(),dict(id='S1',titulo='Dosagem',pontos=['P1'],
            consultas=[dict(pt='dosagem química',en='chemical dosing')]),{},[],configuration(),calls))
        self.assertEqual(len(calls.inputs),1)

    def test_multiple_collections_and_legacy_feed_exclusion(self):
        class Many(Index):
            def search(self,query,**kwargs):
                return [source('feed',url='https://www.imca-int.com/resources/safety/safety-flashes/rss-feed/')]+[
                    source(i,'norge') for i in range(30)]+[source(100,'abb')]
        selected,_,excluded=candidates(Many(),[dict(pt='processo',en='process')],configuration())
        self.assertEqual(len(selected),24)
        self.assertIn('abb',{s['collection'] for s in selected})
        self.assertTrue(excluded)
        self.assertNotIn('feed',{s['document_id'] for s in selected})

    def test_editorial_cleanliness_and_heading_hierarchy(self):
        for text in ('As referências disponíveis indicam um critério.','Conforme a referência consultada, há uma regra.',
                     'As fontes apontam outra condição.'):
            self.assertTrue(editor_issues(dict(texto=text)))
        self.assertEqual(clean_headings('## Dosagem\n\n## Critérios\nTexto\n### Condições\nCorpo','Dosagem','Produtos'),
                         '### Critérios\nTexto\n#### Condições\nCorpo')
