"""Regressões da pesquisa: pertinência, diversidade, lacunas e parada delimitada."""
import asyncio
import unittest
import json
from pathlib import Path

from pipeline.qa_research.v3.__main__ import configuration
from pipeline.qa_research.v3.review import clean_headings,editor_issues,apply_editorial
from pipeline.qa_research.v3.retrieval import research,candidates
from pipeline.qa_research.v3 import contracts as C


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
        result=dict(selecionadas=[dict(id=s['id'],pertinencia='direta',pontos=['P1'],
            aplicabilidade='Condições do processo, sem obrigação legal brasileira')
            for s in payload['candidatas'] if not s['texto'].endswith('2')],lacunas=['P1'])
        validate(result);return result


class ResearchTests(unittest.TestCase):
    def test_initial_selection_does_not_expand_its_own_queries(self):
        index=Index();calls=Calls()
        section=dict(id='S1',titulo='Dosagem',pontos=['P1'],
            consultas=[dict(pt='dosagem química',en='chemical dosing')])
        selected,detail=asyncio.run(research(index,section,{},[dict(id='P1')],configuration(),calls))
        self.assertEqual(len(calls.inputs),1)
        self.assertEqual(len(index.queries),2)
        self.assertEqual({s['texto'] for s in selected},{source(1)['texto']})
        self.assertEqual(len(detail['consultas']),2)
        self.assertTrue(all(s['jurisdiction']=='NO' for s in selected))

    def test_followup_evaluates_only_unseen_passages(self):
        index=Index();calls=Calls();config=configuration()
        section=dict(id='S1',titulo='Dosagem',pontos=['P1'],
            consultas=[dict(pt='dosagem química',en='chemical dosing')])
        _,initial=asyncio.run(research(index,section,{},[],config,calls))
        selected,_=asyncio.run(research(index,section,{},[],config,calls,
            pairs=[dict(pt='nova dosagem',en='nova dosing')],
            exclude=[s['id'] for s in initial['candidatas']],suffix='complementar'))
        self.assertEqual(len(calls.inputs),2)
        self.assertEqual([s['texto'] for s in calls.inputs[-1]['candidatas']],[source(3)['texto']])
        self.assertEqual([s['texto'] for s in selected],[source(3)['texto']])
        _,detail=asyncio.run(research(index,section,{},[],config,calls,
            exclude=[s['id'] for s in initial['candidatas']],suffix='sem_novidade'))
        self.assertEqual(len(calls.inputs),2)
        self.assertIn('Nenhuma passagem nova',detail['motivo'])

    def test_multiple_collections_and_legacy_feed_exclusion(self):
        class Many(Index):
            def search(self,query,**kwargs):
                return [source('feed',url='https://www.imca-int.com/resources/safety/safety-flashes/rss-feed/')]+[
                    source(i,'norge') for i in range(30)]+[source(100,'abb')]
        selected,_,excluded=candidates(Many(),[dict(pt='processo',en='process')],configuration())
        self.assertEqual(len(selected),12)
        self.assertIn('abb',{s['collection'] for s in selected})
        self.assertTrue(excluded)
        self.assertNotIn('feed',{s['document_id'] for s in selected})

    def test_editorial_cleanliness_and_heading_hierarchy(self):
        for text in ('As referências disponíveis indicam um critério.','Conforme a referência consultada, há uma regra.',
                     'As fontes apontam outra condição.'):
            self.assertTrue(editor_issues(dict(texto=text)))
        self.assertFalse(editor_issues(dict(texto='A equipe acompanha o trecho realmente protegido da tubulação.')))
        self.assertEqual(clean_headings('## Dosagem\n\n## Critérios\nTexto\n### Condições\nCorpo','Dosagem','Produtos'),
                         '### Critérios\nTexto\n#### Condições\nCorpo')

    def test_previous_real_pilot_keeps_sound_sections_despite_optional_limits(self):
        folder=Path(__file__).resolve().parents[2]/'relatorios/piloto_fluxo_v3_02_02_20261101T041303/contexto/versoes/e82f27955f44f7cd8333/secoes'
        current={sid:json.loads((folder/(sid+'_corrigida.json')).read_text(encoding='utf-8')) for sid in ('S01','S02','S04')}
        report=dict(secoes=[dict(id=sid,decisao='liberar',motivo='Conteúdo adequado',correcao='',
            consultas=[],lacunas_essenciais=[],limites=section['lacunas']) for sid,section in current.items()])
        checked=apply_editorial(report,current)
        self.assertTrue(all(r['decisao']=='liberar' for r in checked['secoes']))
        self.assertTrue(all(section['lacunas'] for section in current.values()))

    def test_metalinguage_missed_in_previous_pilot_is_now_detected(self):
        for text in ('Para esta seção, a base disponível sustenta uma relação.',
                     'O conjunto disponível sustenta com mais segurança a atenção a volumes estagnados.'):
            self.assertTrue(editor_issues(dict(texto=text)))

    def test_essential_gap_cannot_coexist_with_fully_covered_point(self):
        report=dict(secoes=[dict(id='S1',decisao='liberar',motivo='Conteúdo adequado',correcao='',consultas=[],
            lacunas_essenciais=[dict(ponto='P1',descricao='Falta explicar seleção')],limites=[])],
            cobertura=[dict(id='P1',estado='atendido',secoes=['S1'],motivo='Coberto')],omissoes_escopo=[])
        with self.assertRaisesRegex(ValueError,'contradiz'):C.review(report,{'S1'},{'P1'})

    def test_queries_must_be_focused_expressions(self):
        with self.assertRaisesRegex(ValueError,'curtas'):
            C.pairs([dict(pt='palavra '*17,en='word '*17)],'consultas')
