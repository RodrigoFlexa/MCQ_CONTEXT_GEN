import asyncio
import io
import json
import tempfile
import copy
import unittest
from collections import Counter
from contextlib import redirect_stdout
from pathlib import Path
from unittest.mock import patch
import numpy as np
from pipeline.inventario.textutil import read_json
from pipeline.qa_research.piloto_qa import contracts as C
from pipeline.qa_research.piloto_qa.adaptive import generate
from pipeline.qa_research.piloto_qa.contextos import packages
from pipeline.qa_research.piloto_qa.fluxo import config,main,run
from pipeline.qa_research.piloto_qa.similarity import Similarity
from pipeline.qa_research.piloto_qa.generate import jsonl
from pipeline.qa_research.piloto_qa.tests.test_pilot import Model,response


class Encoder:
    protocol={'model':'fixture'}
    def queries(self,texts):
        return np.asarray([[1+len(t),1+sum(c.isdigit() for c in t),1+sum(c in 'aeiou' for c in t)] for t in texts])
    def close(self):pass


class FlowModel(Model):
    def __init__(self,novel=1):
        super().__init__();self.novel=novel;self.counts=Counter();self.broken=False;self.reject=False
    async def __call__(self,role,messages,tokens):
        p=json.loads(messages[1]['content'])
        if role=='author':
            self.inputs.append((role,p))
            if self.broken:raise TimeoutError('fixture')
            ctx=p['contexto'];self.counts[ctx['id']]+=1
            n=self.counts[ctx['id']];n=n if n<=self.novel else 1
            bid=ctx['blocos'][0];qid=p['prefixo']+'Q01';kind=p['prioridades_tipos'][0]
            return response(dict(alvos=[dict(id=qid,tipo=kind,composicao='simples',conhecimento='Relação técnica',ponte='',
                afirmacoes=[dict(afirmacao='Relação técnica',evidencias=[dict(bloco=bid['id'],trecho=bid['texto'])])])],
                questoes=[dict(id=qid,pergunta=f'Como a restrição interfere na vazão no cenário {ctx["id"]} número {n}?',
                    resposta='A restrição altera a vazão conforme as condições.',cenario=True,
                    criterios=[dict(id='K1',criterio='Explicar a relação',inferencia='',evidencias=[dict(bloco=bid['id'],trecho=bid['texto'])])],
                    equivalentes=[],erros_materiais=[])],impedimentos=[]))
        result=await super().__call__(role,messages,tokens)
        if role=='refine':
            data=json.loads(result.choices[0].message.content)
            for q in data['questoes']:
                q.update(pergunta='Como a restrição interfere na vazão nas condições apresentadas?',cenario=True)
            return response(data)
        if role=='judge':
            data=json.loads(result.choices[0].message.content)
            for row,q in zip(data['avaliacoes'],p['candidatas']):
                if self.repair and 'cenário' in q['pergunta']:
                    row.update(decisao='corrigir',correcao='Delimitar condição');row['criterios']['determinada']=False
                if self.reject and p['inventario_admitido']:
                    row.update(decisao='descartar',duplicada_de=p['inventario_admitido'][0]['id'])
                    row['criterios']['distinta']=False
            result=response(data)
        return result


class MixedModel(FlowModel):
    async def __call__(self,role,messages,tokens):
        result=await super().__call__(role,messages,tokens)
        if role=='author':
            data=json.loads(result.choices[0].message.content)
            target=copy.deepcopy(data['alvos'][0]);q=copy.deepcopy(data['questoes'][0])
            target['id']=target['id'][:-1]+'2';q['id']=target['id']
            q['pergunta']='Como a restrição interfere na vazão sob condições constantes?'
            data['alvos'].append(target);data['questoes'].append(q)
            return response(data)
        return result


class AdaptiveTests(unittest.TestCase):
    def setUp(self):
        self.tmp=tempfile.TemporaryDirectory();self.addCleanup(self.tmp.cleanup);self.root=Path(self.tmp.name)
        self.sim=Similarity(self.root,Encoder());self.addCleanup(self.sim.close)
        self.doc=dict(titulo='Teste',capitulos=[dict(titulo='Processo',grupo='Sistema',blocos=[
            dict(subtitulo='Restrição',texto='A restrição altera a vazão conforme as condições.')])])
        self.c=config();self.c.update(max_calls=300,memory_limit=2,patience=2)
        self.model=FlowModel();self.bank=[]
    def gen(self):
        with redirect_stdout(io.StringIO()):return asyncio.run(generate(self.doc,'02_02','novo_refinado',self.c,
            self.root/'run',self.bank,self.sim,transport=self.model))
    def test_no_question_ceiling_and_only_commands_in_bounded_memory(self):
        self.model.novel=23;r=self.gen()
        self.assertEqual(r['admitidas'],23);self.assertEqual(r['status'],'concluido')
        payloads=[p for role,p in self.model.inputs if role=='author']
        self.assertTrue(all(len(p['memoria'])<=2 and all(isinstance(q,str) for q in p['memoria']) for p in payloads))
        self.assertNotEqual(payloads[0]['prioridades_tipos'],payloads[1]['prioridades_tipos'])
        self.assertEqual(r['contextos'][0]['rodadas_sem_ganho'],2)
    def test_repeat_run_makes_no_model_calls(self):
        self.gen();n=len(self.model.inputs);self.gen();self.assertEqual(len(self.model.inputs),n)
    def test_budget_is_suspension_and_resumes_same_round(self):
        self.c['max_calls']=1;r=self.gen();self.assertEqual(r['motivo_parada'],'suspenso_orcamento')
        self.assertEqual(r['contextos'][0]['rodadas_sem_ganho'],0)
        self.c['max_calls']=300;self.assertEqual(self.gen()['admitidas'],1)
    def test_failure_is_not_low_productivity(self):
        self.model.broken=True
        # Sem aguardar o backoff de transporte no fixture.
        async def fast(*args,**kwargs):raise ValueError('erro de formato simulado')
        with patch('pipeline.qa_research.v3.runtime.Calls.call',fast):r=self.gen()
        self.assertEqual(r['motivo_parada'],'falha_retomavel');self.assertEqual(r['contextos'][0]['rodadas_sem_ganho'],0)
        self.model.broken=False;self.assertEqual(self.gen()['status'],'concluido')
    def test_refinement_rechecks_and_is_cached(self):
        self.model.repair=True;r=self.gen();self.assertEqual(r['admitidas'],1)
        self.assertTrue(any(role=='refine' for role,_ in self.model.inputs))
        before=len(self.model.inputs);self.gen();self.assertEqual(len(self.model.inputs),before)
    def test_repair_budget_preserves_valid_round_without_claiming_saturation(self):
        self.model.repair=True;self.c['max_calls']=3
        r=self.gen();self.assertEqual(r['motivo_parada'],'suspenso_orcamento');self.assertEqual(r['admitidas'],0)
        self.c['max_calls']=300;self.assertEqual(self.gen()['admitidas'],1)
    def test_budget_in_repair_preserves_other_admitted_question(self):
        self.model=MixedModel();self.model.repair=True;self.c['max_calls']=3
        r=self.gen();self.assertEqual(r['motivo_parada'],'suspenso_orcamento');self.assertEqual(r['admitidas'],1)
        self.c['max_calls']=300;r=self.gen();self.assertEqual(r['admitidas'],2);self.assertEqual(r['status'],'concluido')
    def test_semantic_neighbors_do_not_automatically_reject(self):
        self.bank=[dict(id='H1',uid='old',item='02_02',tipo='conceito',composicao='simples',conhecimento='Outra demanda',
            pergunta='Como a restrição interfere em outro mecanismo?',resposta='Outro efeito.')]
        self.assertEqual(self.gen()['admitidas'],1)
        initial=read_json(self.root/'run/rodadas/000001_inicial.json')
        self.assertEqual(initial['records'][0]['vizinhos'][0]['id'],'H1')
    def test_auditor_can_reject_semantic_duplicate(self):
        self.bank=[dict(id='H1',uid='old',item='02_02',tipo='conceito',composicao='simples',conhecimento='Mesma demanda',
            pergunta='Outra redação da mesma pergunta?',resposta='Mesmo conhecimento.')]
        self.model.reject=True;self.assertEqual(self.gen()['admitidas'],0)
    def test_contexts_are_revisited_and_interfaces_generated(self):
        self.doc['capitulos'].append(dict(titulo='Interface',grupo='Sistema',blocos=[dict(subtitulo='Controle',texto='O controle altera a restrição.')]))
        r=self.gen();self.assertEqual(len(r['contextos']),3);self.assertEqual(r['admitidas'],3)
        self.assertTrue(all(p['rodadas_sem_ganho']==2 for p in r['contextos']))
        self.assertEqual([p['tipo'] for p in packages(self.doc)],['capitulo','capitulo','interface'])
    def test_large_chapter_splits_only_at_block_boundaries(self):
        b=self.doc['capitulos'][0]['blocos'][0];b['texto']='Texto técnico. '*20
        self.doc['capitulos'][0]['blocos'].append(dict(subtitulo='Outro',texto='Outro texto técnico. '*15))
        ps=packages(self.doc,450);self.assertEqual(len(ps),2)
        self.assertEqual(ps[0]['blocos'][0]['texto'],b['texto'])
    def test_plan_is_read_only_without_count_target(self):
        out=self.root/'absent'
        with redirect_stdout(io.StringIO()) as stream:main(['--plan','--output',str(out),'--items','02_02'])
        self.assertFalse(out.exists());self.assertIsNone(json.loads(stream.getvalue())['teto_questoes'])
    def test_model_inputs_fit_even_full_context_not_repeated_in_candidates(self):
        self.gen()
        for role,p in self.model.inputs:
            if role=='judge':self.assertTrue(all('blocos_contexto' not in q and 'contexto_tecnico' not in q for q in p['candidatas']))
    def test_both_arms_start_with_same_bank_and_do_not_share_generated_questions(self):
        baseline=[dict(id='H'+str(i),uid='h'+str(i),item='04_01',tipo=t,composicao='simples',conhecimento='Relação',
            pergunta='Qual a relação técnica '+str(i)+'?',resposta='Resposta.') for i,t in enumerate(C.TYPES)]
        observed=[]
        async def fake(document,item,group,c,output,bank,similarity,*args,**kwargs):
            observed.append((group,len(bank),{q.get('grupo') for q in bank if q.get('nova')}))
            jsonl(Path(output)/'aprovadas.jsonl',[dict(id=item,uid=group+item,item=item,grupo=group,nova=True,tipo='conceito',pergunta='Pergunta '+item+'?')])
            return dict(status='concluido',admitidas=1)
        with patch('pipeline.qa_research.piloto_qa.fluxo.base_bank',return_value=baseline),patch('pipeline.qa_research.piloto_qa.fluxo.historical',return_value=[]),patch('pipeline.qa_research.piloto_qa.fluxo.generate',fake):
            asyncio.run(run(self.root/'cli',self.c,['novo_antigo','novo_refinado'],similarity=self.sim))
        self.assertEqual([n for _,n,_ in observed],[6,7,8,6,7,8])
        self.assertTrue(all(not seen or seen=={group} for group,_,seen in observed))
    def test_partial_document_prevents_advancing_to_another_bank(self):
        baseline=[dict(id='H'+str(i),uid='h'+str(i),item='04_01',tipo=t,pergunta='Pergunta '+str(i)+'?',resposta='Resposta') for i,t in enumerate(C.TYPES)]
        seen=[]
        async def partial(*args,**kwargs):seen.append(args[1]);return dict(status='parcial')
        with patch('pipeline.qa_research.piloto_qa.fluxo.base_bank',return_value=baseline),patch('pipeline.qa_research.piloto_qa.fluxo.historical',return_value=[]),patch('pipeline.qa_research.piloto_qa.fluxo.generate',partial):
            asyncio.run(run(self.root/'cli',self.c,['novo_antigo','novo_refinado'],similarity=self.sim))
        self.assertEqual(seen,['02_02'])
    def test_all_stage_evaluates_only_after_complete_generation(self):
        async def complete(*args,**kwargs):return {'novo_refinado':{i:dict(status='concluido') for i in self.c['items']}}
        with patch('pipeline.qa_research.piloto_qa.fluxo.run',complete),patch('pipeline.qa_research.piloto_qa.fluxo.tables',side_effect=[None,dict(status='concluido')]) as report,redirect_stdout(io.StringIO()):
            code=main(['--stage','all','--arms','refinado','--output',str(self.root/'cli')])
        self.assertEqual(code,0);self.assertEqual(report.call_count,2);self.assertTrue(report.call_args.kwargs['assessment'])
    def test_all_stage_partial_produces_tables_without_paid_evaluation(self):
        async def partial(*args,**kwargs):return {'novo_refinado':{'02_02':dict(status='parcial')}}
        with patch('pipeline.qa_research.piloto_qa.fluxo.run',partial),patch('pipeline.qa_research.piloto_qa.fluxo.tables') as report,redirect_stdout(io.StringIO()):
            code=main(['--stage','all','--arms','refinado','--output',str(self.root/'cli')])
        self.assertEqual(code,2);self.assertEqual(report.call_count,1);self.assertFalse(report.call_args.kwargs.get('assessment',False))


if __name__=='__main__':unittest.main()
