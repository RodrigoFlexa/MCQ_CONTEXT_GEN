"""Contratos/metodologia, instalador e piloto completo com clientes simulados."""
import copy
import io
import json
import tempfile
import unittest
from contextlib import redirect_stdout
from pathlib import Path
from unittest.mock import patch

from pipeline.domain_corpora.io_utils import atomic_json,file_hash
from pipeline.domain_corpora.manifest import load_manifest
from pipeline.qa_research.corpus import CorpusIndex
from pipeline.qa_research.runtime import PersistentBudget
from pipeline.inventario.llm import BudgetExceeded
from pipeline.qa_research.tests.test_document import SimulatedLLM
from pipeline.qa_research.v2.common import topic, unique, TYPES, load_examples, Calls
from pipeline.qa_research.v2.__main__ import load_config, DEFAULT_CONFIG, execute, collect, main
from pipeline.qa_research.v2.context import validate_plan, generate as generate_context
from pipeline.qa_research.v2.questions import (validate_units,validate_qa_audit,validate_candidate,
    validate_targets,generate_one,statistics,QA_CRITERIA,UNIT_CRITERIA)
from pipeline.qa_research.v2.install_corpora import HTML,permitted,CATALOG,install,force


def fixture_manifest(root):
    root.mkdir(parents=True,exist_ok=True)
    path=root/'pages.jsonl'
    path.write_text(json.dumps(dict(collection='manual',document_id='doc',title='Manual de teste',
        document_type='manual_industrial',page=1,source_boundary='known_document',language='pt',
        text='O tratamento químico reduz a formação de espuma. A temperatura altera o desempenho do tratamento. '*35,
        url='https://example.org/manual',license='fixture'),ensure_ascii=False)+'\n',encoding='utf-8')
    manifest=root/'manifest.json'
    atomic_json(manifest,dict(schema='petroquest-professional-corpora-v1',ready=True,partial=True,
        collections=[dict(id='manual',format='pages_jsonl',documents=1,path=path.name,sha256=file_hash(path))]))
    return manifest


class Client:
    def __init__(self):self.count=0;self.inputs=[];self.old=SimulatedLLM()
    def json(self,system,user,tag,validate,**kwargs):
        self.count+=1;role=tag.removeprefix('v2_');p=json.loads(user);self.inputs.append((role,p))
        if role=='plan':
            d={'recortes':[dict(id='R01',titulo='Controle da espuma',foco='controle da espuma',ancora='espuma',
                essencial=True,consultas=['tratamento químico espuma'],termos=['espuma'])]}
        elif role in ('doc_research','doc_write','doc_audit') or (role=='coverage' and 'lacunas' in p) or (role=='dedup' and 'pares' in p):
            stage={'doc_write':'write','doc_audit':'audit','coverage':'gaps','dedup':'dedup'}.get(role,
                'research' if 'fontes' in p else 'discover')
            return self.old.json(system,user,'document_'+stage,'fixture',validate,**kwargs)
        elif role=='coverage':
            d=dict(cobertura=[dict(id='R01',coberto=True,blocos=[p['blocos'][0]['id']],justificativa='Cobertura de teste.',
                lacunas=[],proximas_consultas=[])],correcoes=[],repeticoes=[],novas_relacoes=[dict(conhecimento='Controle da espuma.',blocos=[p['blocos'][0]['id']])])
        elif role=='units':
            b=p['blocos'][0]
            d=dict(unidades=[dict(id='U01',conhecimento='Controle químico da espuma',condicoes=[],
                evidencias=[dict(bloco=b['id'],trecho=b['texto'])],alvos=[dict(tipo='conceito',alvo='Identificar a função do tratamento')])])
        elif role=='unit_audit':
            d=dict(avaliacoes=[dict(id=u['id'],aprovada=True,**{c:True for c in UNIT_CRITERIA},duplicada_de=None,motivo='Fundamentada.') for u in p['unidades']])
        elif role=='qa_plan':
            d=dict(alvos=[dict(id='A01',tipo='conceito',composicao='simples',unidades=[p['unidades'][0]['id']],
                alvo='Identificar a função do tratamento',resposta_esperada='Reduzir a formação de espuma.',ponte='')],impedimentos=[])
        elif role in ('qa_author','qa_refine'):
            d=dict(status='ok',motivo='',tipo='conceito',composicao='simples',cenario=False,
                   pergunta='Qual é a função do tratamento químico antiespumante?',resposta='Reduzir a formação de espuma.')
        elif role=='qa_solver':d=dict(resposta='Reduzir a formação de espuma.',ambiguidades=[],concorrentes=[])
        elif role=='qa_audit':d=dict(aprovada=True,**{c:True for c in QA_CRITERIA},motivo='Adequada.',encaminhamento='aprovar')
        elif role=='dedup':d=dict(duplicada_de=None,motivo='Conhecimento distinto.')
        else:raise AssertionError(role)
        validate(d);return d


class ProtocolTests(unittest.TestCase):
    def setUp(self):
        self.temp=tempfile.TemporaryDirectory();self.root=Path(self.temp.name)
        self.config=load_config(DEFAULT_CONFIG);self.config.update(workers=1,min_questions=1,document_rounds=1)
    def tearDown(self):self.temp.cleanup()

    def test_real_input_preserved_and_anchor_required(self):
        selected=topic('02_02');self.assertEqual(selected['subtopico'],'Produtos químicos')
        row=dict(id='R1',titulo='Água',foco='Aplicação',ancora='água produzida',essencial=True,consultas=['água'],termos=['água'])
        validate_plan({'recortes':[row]},selected,12)
        with self.assertRaises(ValueError):validate_plan({'recortes':[{**row,'ancora':'subtópico inventado'}]},selected,12)
        with self.assertRaises(ValueError):unique([{'id':'../../escape'}])

    def test_units_must_quote_real_blocks(self):
        u=dict(id='U1',conhecimento='Relação',condicoes=[],evidencias=[dict(bloco='B1',trecho='inventado')],
               alvos=[dict(tipo='conceito',alvo='Identificar')])
        with self.assertRaises(ValueError):validate_units({'unidades':[u]},{'B1':{'texto':'original'}},10)

    def test_classes_composition_and_conflicting_audit(self):
        units={'U1':{'alvos':[{'tipo':t} for t in TYPES]},'U2':{'alvos':[]}}
        for t in TYPES:
            validate_targets(dict(alvos=[dict(id='A',tipo=t,composicao='simples',unidades=['U1'],alvo='Alvo',resposta_esperada='Resposta')],impedimentos=[]),units,1)
        with self.assertRaises(ValueError):validate_targets(dict(alvos=[dict(id='A',tipo='conceito',composicao='composta',unidades=['U1','U2'],alvo='A',resposta_esperada='R',ponte='ponte')],impedimentos=[]),units,1)
        with self.assertRaises(ValueError):validate_qa_audit({**dict(aprovada=True,**{c:True for c in QA_CRITERIA},motivo='x',encaminhamento='aprovar'),'sustentada':False})

    def test_complete_pilot_resume_and_blind_solver(self):
        manifest=fixture_manifest(self.root/'corpus');client=Client();clients={r:client for r in self.config['models']}
        output=self.root/'run'
        with redirect_stdout(io.StringIO()):
            result=execute(topic('02_02'),manifest,output,self.config,clients=clients)
        self.assertEqual(result['status'],'concluido',result)
        self.assertEqual(result['questoes']['aprovadas'],1)
        self.assertEqual(result['questoes']['cobertura_demandas'],1)
        solver=next(p for role,p in client.inputs if role=='qa_solver')
        self.assertEqual(set(solver),{'pergunta','blocos'})
        audit=next(p for role,p in client.inputs if role=='qa_audit')
        self.assertTrue(audit['blocos'])
        count=client.count
        with redirect_stdout(io.StringIO()):
            execute(topic('02_02'),manifest,output,self.config,clients=clients)
        self.assertEqual(client.count,count,'Retomada não deve repetir chamadas concluídas')
        changed=copy.deepcopy(self.config);changed['models']['qa_author']='outro:high'
        with self.assertRaisesRegex(ValueError,'mudaram'):execute(topic('02_02'),manifest,output,changed,clients=clients)
        (output/'contexto'/'rodada_01'/'pacote'/'secret.txt').write_text('original')
        collect(output,self.root/'snapshot')
        self.assertFalse(list((self.root/'snapshot').rglob('secret.txt')))
        self.assertTrue((self.root/'snapshot'/'questoes'/'qa.csv').is_file())

    def test_manifest_compatible_with_existing_search_and_tamper_detection(self):
        m=fixture_manifest(self.root)
        index=CorpusIndex(self.root/'index',manifest=m);index.build()
        self.assertFalse(index.info['complete_corpus'],'Manifesto parcial não pode anunciar corpus completo')
        self.assertTrue(index.search('espuma'))
        (self.root/'pages.jsonl').write_text('{}')
        with self.assertRaisesRegex(ValueError,'corrompido'):load_manifest(m)

    def test_plan_does_not_load_client_or_create_output(self):
        with patch('pipeline.qa_research.v2.__main__.Calls',side_effect=AssertionError('não criar cliente')):
            with redirect_stdout(io.StringIO()):
                self.assertEqual(main(['--plan','--output',str(self.root/'absent')]),0)
        self.assertFalse((self.root/'absent').exists())

    def test_examples_read_only_and_other_topic(self):
        p=self.root/'examples.jsonl'
        p.write_text(json.dumps(dict(item='02_02',pergunta='Não usar',resposta='X'))+'\n'+json.dumps(dict(item='01_01',pergunta='Pergunta',resposta='Resposta')))
        before=p.read_bytes();rows=load_examples([p],'02_02')
        self.assertEqual(len(rows),1);self.assertEqual(p.read_bytes(),before)

    def test_persistent_budget_does_not_reset(self):
        budget=PersistentBudget(self.root/'budget.json',1);budget.reserve()
        with self.assertRaises(BudgetExceeded):PersistentBudget(self.root/'budget.json',1).reserve()
        PersistentBudget(self.root/'budget.json',2).reserve()

    def test_refinement_is_reaudited_and_gap_is_routed(self):
        target=dict(id='A1',tipo='conceito',composicao='simples',unidades=['U1'],alvo='Função do produto')
        units={'U1':dict(id='U1',evidencias=[dict(bloco='B1',trecho='Espuma')])}
        blocks={'B1':dict(id='B1',texto='O produto reduz a espuma.')}
        class FakeCalls:
            def __init__(self,gap=False):self.seen=[];self.gap=gap;self.audits=0
            def call(self,role,system,payload,validate):
                self.seen.append((role,payload))
                if role in ('qa_author','qa_refine'):
                    q='Qual é a função do tratamento químico antiespumante?' if role=='qa_author' else 'Para que serve o tratamento químico antiespumante aplicado ao processo?'
                    d=dict(status='ok',motivo='',tipo='conceito',composicao='simples',cenario=False,pergunta=q,resposta='Reduzir a formação de espuma.')
                elif role=='qa_solver':d=dict(resposta='Reduzir a formação de espuma.',ambiguidades=[],concorrentes=[])
                elif role=='qa_audit':
                    self.audits+=1;ok=self.audits>1
                    d=dict(aprovada=ok,**{c:True for c in QA_CRITERIA},motivo='Rever o enunciado.',encaminhamento='aprovar' if ok else ('lacuna_documental' if self.gap else 'reescrever'))
                    if not ok:d['sem_pistas']=False
                validate(d);return d
        calls=FakeCalls()
        r=generate_one(target,units,blocks,[],[],self.config,calls)
        self.assertEqual(r['status'],'aprovada_modelo');self.assertEqual(calls.audits,2)
        self.assertTrue(all(set(p)=={'pergunta','blocos'} for role,p in calls.seen if role=='qa_solver'))
        calls=FakeCalls(gap=True)
        r=generate_one(target,units,blocks,[],[],self.config,calls)
        self.assertEqual(r['status'],'lacuna_documental');self.assertNotIn('qa_refine',[s for s,p in calls.seen])

    def test_unit_coverage_does_not_imply_class_coverage(self):
        units=[dict(id='U1',alvos=[dict(tipo=t) for t in TYPES])]
        rows=[dict(status='aprovada_modelo',tipo='conceito',composicao='simples',alvo=dict(unidades=['U1']))]
        stats=statistics(units,rows)
        self.assertEqual(stats['cobertura_unidades'],1)
        self.assertAlmostEqual(stats['cobertura_demandas'],1/6)

    def test_document_stops_on_knowledge_gain_and_keeps_gap(self):
        class NoGain(Client):
            def json(self,system,user,tag,validate,**kwargs):
                p=json.loads(user)
                if tag=='v2_coverage' and 'plano' in p:
                    d=dict(cobertura=[dict(id='R01',coberto=False,blocos=[],justificativa='Falta conhecimento essencial.',
                        lacunas=['Falta relação'],proximas_consultas=['espuma'])],correcoes=[],repeticoes=[],novas_relacoes=[])
                    validate(d);return d
                return super().json(system,user,tag,validate,**kwargs)
        client=NoGain();config={**self.config,'document_rounds':3}
        calls=Calls(self.root/'run',config,{r:client for r in config['models']})
        with redirect_stdout(io.StringIO()):
            doc,report=generate_context(topic('02_02'),fixture_manifest(self.root/'corpus'),self.root/'context',config,calls)
        self.assertEqual(report['motivo_parada'],'pesquisa_estabilizada_com_pendencias')
        self.assertEqual(report['status'],'parcial');self.assertEqual(len(report['historico']),2)
        self.assertEqual(report['historico'][0]['novas_relacoes_auditadas'],0)
        self.assertGreater(report['historico'][0]['novas_evidencias'],0)

    def test_force_imports_actual_schema_without_downloading_qa(self):
        content='Operação industrial com texto suficiente para descrever o trabalho profissional e suas condições de execução e controle no relatório diário de uma instalação offshore.'
        raw=('filename,page,content,content_scrubbed_light,content_scrubbed_light_could_be_natural_language\n'+
             f'relatorio.pdf,2,original,{content},True\n'+f'ruim.pdf,1,original,{content},False\n').encode()
        class FakeHTTP:
            def bytes(self,url):
                return json.dumps(dict(metadata=dict(license=dict(id='cc-by-4.0')),files=[dict(key='reports.csv',links=dict(self='https://zenodo.org/file.csv'),checksum='md5:fixture',size=len(raw))])).encode()
            def download(self,url,target,*args):target.parent.mkdir(parents=True,exist_ok=True);target.write_bytes(raw)
        meta=force(self.root,FakeHTTP())
        self.assertEqual(meta['documents'],1)
        row=json.loads((self.root/'force/pages.jsonl').read_text(encoding='utf-8'))
        self.assertEqual(row['page'],2);self.assertEqual(row['title'],'relatorio.pdf')
        self.assertEqual(row['text'],content)

    def test_installer_scope_html_and_partial_failure(self):
        h=HTML();h.feed('<nav>Excluir</nav><main><h1>Manual</h1><p>Conteúdo técnico.</p></main>')
        self.assertNotIn('Excluir',h.text());self.assertIn('Conteúdo',h.text())
        self.assertFalse(permitted('https://evil.test/training',CATALOG['kimray']))
        self.assertFalse(permitted('https://kimray.com/sales',CATALOG['kimray']))
        with patch('pipeline.qa_research.v2.install_corpora.collect',return_value=([],[{'error':'bloqueio'}],{})):
            r=install(self.root/'installer',['kimray'],None)
        self.assertFalse(r['ready'])
        with self.assertRaises(ValueError):load_manifest(self.root/'installer'/'manifest.json')


if __name__=='__main__':unittest.main()
