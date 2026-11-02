import asyncio
import copy
import io
import json
import tempfile
import unittest
from contextlib import redirect_stdout
from pathlib import Path
from types import SimpleNamespace as NS

from pipeline.inventario.textutil import read_json, atomic_json
from pipeline.qa_research.piloto_qa import contracts as C
from pipeline.qa_research.piloto_qa.__main__ import config, collect, main, run, samples
from pipeline.qa_research.piloto_qa.documents import prepare, flatten, close_pilot, LATEST
from pipeline.qa_research.piloto_qa.generate import generate
from pipeline.qa_research.piloto_qa.evaluation import historical, paired_summary, evaluate
from pipeline.qa_research.piloto_qa.metrics import measure, matched, semantic, self_bleu, calculate


def response(data):
    return NS(choices=[NS(finish_reason='stop',message=NS(content=json.dumps(data)))],usage=NS(prompt_tokens=20,completion_tokens=20))


class Model:
    def __init__(self): self.inputs=[]; self.repair=False; self.fail_repair=False; self.duplicate=False
    async def __call__(self,role,messages,tokens):
        p=json.loads(messages[1]['content']);self.inputs.append((role,p))
        if role=='plan':
            b=p['documento'][0]
            data=dict(alvos=[dict(id=f'T{i}',tipo='mecanismo',composicao='simples',conhecimento=f'Relação técnica número {i}',ponte='',
                afirmacoes=[dict(afirmacao='Relação com condição',evidencias=[dict(bloco=b['id'],trecho=b['texto'])])]) for i in range(1,5)],impedimentos=[])
        elif role in ('author','refine'):
            data=dict(questoes=[],impedimentos=[])
            for target in p['alvos']:
                bid=p['contextos_por_alvo'][target['id']][0]
                data['questoes'].append(dict(id='UNKNOWN' if role=='refine' and self.fail_repair else target['id'],
                    pergunta='Como a restrição interfere na vazão '+('comum' if self.duplicate else target['id'])+'?',
                    resposta='A restrição altera a vazão conforme as condições.',cenario=False,
                    criterios=[dict(id='K1',criterio='Explicar a relação',evidencias=[dict(bloco=bid['id'],trecho=bid['texto'])],inferencia='')],
                    equivalentes=['A resposta pode usar sinônimos'],erros_materiais=['Inverter a relação']))
        elif role=='solve':
            self_payload=json.dumps(p)
            assert 'criterios' not in self_payload and 'erros_materiais' not in self_payload
            data=dict(resolucoes=[dict(id=q['id'],resposta='A restrição altera a vazão.',ambiguidades=[]) for q in p['questoes']])
        else:
            data=dict(avaliacoes=[])
            for q in p['candidatas']:
                bad=self.repair and q['id']=='T2'
                flags={k:True for k in C.FLAGS}
                if bad:flags['determinada']=False
                data['avaliacoes'].append(dict(id=q['id'],decisao='corrigir' if bad else 'admitir',motivo='Verificado',
                    correcao='Delimitar condição' if bad else '',duplicada_de=None,criterios=flags,
                    checagem_essenciais=[dict(id=c['id'],sustentado=True,evidencias=c['evidencias'],justificativa='Relação no contexto') for c in q['criterios']]))
        return response(data)


class GenerationTests(unittest.TestCase):
    def setUp(self):
        self.tmp=tempfile.TemporaryDirectory();self.addCleanup(self.tmp.cleanup);self.out=Path(self.tmp.name)/'qa'
        self.doc=dict(titulo='Teste',capitulos=[dict(titulo='Processo',grupo='Processo',blocos=[dict(subtitulo='Restrição',texto='A restrição altera a vazão conforme as condições.')])])
        self.c=config();self.c.update(questions_per_item=2,batch_size=2,max_calls=40);self.model=Model()
    def run_gen(self):
        with redirect_stdout(io.StringIO()):return asyncio.run(generate(self.doc,'02_02','novo_refinado',self.c,self.out,transport=self.model))
    def test_target_first_generation_and_cache_resume(self):
        report=self.run_gen();self.assertEqual(report['admitidas'],2)
        before=copy.deepcopy(self.model.inputs);self.assertEqual(self.run_gen()['admitidas'],2);self.assertEqual(before,self.model.inputs)
        q=json.loads((self.out/'aprovadas.jsonl').read_text().splitlines()[0]);self.assertTrue(q['criterios']);self.assertTrue(q['blocos_contexto'])
    def test_duplicates_do_not_fill_quota(self):
        self.model.duplicate=True;r=self.run_gen();self.assertEqual(r['admitidas'],1);self.assertEqual(r['status'],'parcial')
    def test_repair_failure_keeps_already_admitted_question_and_retries_on_resume(self):
        self.model.repair=True;self.model.fail_repair=True;r=self.run_gen()
        self.assertEqual(r['admitidas'],1);self.assertEqual(r['motivo_parada'],'falha_retomavel')
        self.model.repair=False;self.model.fail_repair=False;r=self.run_gen();self.assertEqual(r['admitidas'],2)
    def test_changed_document_cannot_reuse_old_result(self):
        self.run_gen();self.doc['titulo']='Outra edição'
        with self.assertRaisesRegex(ValueError,'mudou'):self.run_gen()
    def test_budget_stop_is_resumable(self):
        self.c['max_calls']=1;self.assertEqual(self.run_gen()['admitidas'],0)
        self.c['max_calls']=40;self.assertEqual(self.run_gen()['admitidas'],2)
    def test_budget_during_repair_keeps_admitted_and_resumes(self):
        self.model.repair=True;self.c['max_calls']=4
        self.assertEqual(self.run_gen()['admitidas'],1)
        self.c['max_calls']=40;self.model.repair=False
        self.assertEqual(self.run_gen()['admitidas'],2)
    def test_full_orchestration_keeps_three_groups_and_reuses_calls(self):
        with redirect_stdout(io.StringIO()):
            result=asyncio.run(run(self.out,self.c,transport=self.model))
            before=len(self.model.inputs);asyncio.run(run(self.out,self.c,transport=self.model))
        self.assertEqual(len(self.model.inputs),before)
        self.assertEqual(sum(r['admitidas'] for g in result.values() for r in g.values()),12)
        groups=samples(self.out);self.assertEqual({g:len(qs) for g,qs in groups.items()},
            dict(historico=6,novo_antigo=6,novo_refinado=6))
        for _,payload in self.model.inputs:
            for example in payload.get('exemplos_de_forma',[]):
                self.assertNotIn(example['id'],{q['uid_historico'] for q in groups['historico']})


class DataTests(unittest.TestCase):
    def test_real_document_fixes_preserve_protections_and_snapshots(self):
        paths=list(LATEST.glob('*/documento_para_revisao.json'));before={p:p.read_bytes() for p in paths}
        for item in ['02_02','03_03','07_01']:
            doc,report=close_pilot(item);self.assertTrue(report['protecoes_preservadas']);self.assertTrue(report['alteracoes'])
            if item=='02_02':
                text='\n'.join(b['texto'] for b in flatten(doc))
                self.assertNotIn('Os mecanismos descritos',text);self.assertNotIn('indicadores citados',text)
                self.assertIn('não devem ser tratados como sinônimos automáticos',text)
            if item=='03_03':self.assertTrue(any(b['subtitulo'].startswith('P/V valves') for b in flatten(doc)))
        self.assertTrue(all(p.read_bytes()==v for p,v in before.items()))
    def test_prepare_is_reproducible(self):
        with tempfile.TemporaryDirectory() as t:
            a=prepare(Path(t),['02_02']);self.assertEqual(a,prepare(Path(t),['02_02']))
    def test_historical_sample_is_deterministic_and_balanced(self):
        a=historical(['02_02','03_03','07_01'],20,7)
        self.assertEqual(a,historical(['02_02','03_03','07_01'],20,7));self.assertEqual(len(a),60)
        self.assertTrue(all(q['blocos_contexto'] for q in a))
    def test_plan_is_read_only_and_has_correct_case_count(self):
        with tempfile.TemporaryDirectory() as t,redirect_stdout(io.StringIO()) as f:
            p=Path(t)/'absent';self.assertEqual(main(['--plan','--output',str(p)]),0)
            self.assertFalse(p.exists());self.assertIn('1080',f.getvalue())
    def test_collection_excludes_private_cache(self):
        with tempfile.TemporaryDirectory() as t:
            source=Path(t)/'run';atomic_json(source/'resumo.json',dict(status='ok'));atomic_json(source/'.local/raw.json',dict(secret='private'))
            destination=Path(t)/'snapshot';collect(source,destination)
            self.assertTrue((destination/'resumo.json').exists());self.assertFalse((destination/'.local').exists())


class MetricTests(unittest.TestCase):
    def test_ngrams_never_cross_context_blocks_and_short_answer_is_missing(self):
        q=dict(uid='a',grupo='g',item='02_02',tipo='conceito',pergunta='b c?',resposta='b c',blocos_contexto=[dict(texto='b'),dict(texto='c')])
        m=measure(q,set());self.assertEqual(m['novel_2gram_pct'],100);self.assertIsNone(m['novel_3gram_pct'])
    def test_equal_sample_size_by_item_and_type(self):
        row=lambda uid,t:dict(uid=uid,item='02_02',tipo=t)
        groups={'a':[row('a1','mecanismo'),row('a2','mecanismo'),row('a3','conceito')],
                'b':[row('b1','mecanismo'),row('b2','conceito')]}
        selected=matched(groups,1);self.assertEqual([len(v) for v in selected.values()],[2,2])
    def test_vendi_and_cosine_known_geometry(self):
        s=semantic([[1,0],[0,1]]);self.assertAlmostEqual(s['vendi_cosseno'],2);self.assertEqual(s['cosseno_medio'],0)
        self.assertIsNone(semantic([[1,0],[1,0]])['vendi_centrado_sensibilidade'])
    def test_self_bleu_needs_two_questions(self):self.assertIsNone(self_bleu(['pergunta única']))
    def test_metrics_report_balances_groups_and_marks_missing_semantics(self):
        q=dict(uid='a',grupo='g',item='02_02',tipo='conceito',pergunta='Como a restrição altera a vazão?',
            resposta='A restrição altera a vazão.',blocos_contexto=[dict(texto='A restrição altera a vazão.')])
        with tempfile.TemporaryDirectory() as t:
            result=calculate({'g':[q],'h':[dict(q,uid='b',grupo='h')]},Path(t))
            self.assertEqual(result['comparavel_mesmo_n_item_classe']['g']['n'],1)
            self.assertEqual(result['integral']['g']['semantica']['status'],'nao_calculada')
            self.assertTrue((Path(t)/'RESULTADOS.md').exists())
    def test_gap_uses_only_valid_paired_answers(self):
        pairs=[dict(uid='a',modelo='m',veredito_closed_book='parcial',veredito_open_book='correta'),
               dict(uid='b',modelo='m',veredito_closed_book='',veredito_open_book='correta')]
        r=paired_summary(pairs,{'a':dict(grupo='g'),'b':dict(grupo='g')},1,100)[0]
        self.assertEqual(r['gap_pp'],100);self.assertEqual(r['pares_validos'],1);self.assertEqual(r['sem_par'],1)
    def test_nonliteral_evidence_is_rejected(self):
        with self.assertRaisesRegex(ValueError,'literal'):C.evidence([dict(bloco='B1',trecho='inventado')],{'B1':dict(texto='real')})


class EvalClient:
    def json(self,system,user,**kw):
        p=json.loads(user)
        if 'afirmacoes' in system and isinstance(p,dict) and 'gabarito' in p:
            b=p['blocos'][0];d=dict(cobertura_completa=True,afirmacoes=[dict(afirmacao=p['gabarito'],veredito='sustentada',
                evidencias=[dict(bloco=b['id'],trecho=b['texto'])],justificativa='Suporte literal')],observacoes='')
        elif isinstance(p,list):d=dict(avaliacoes=[dict(id=q['id'],veredito='correta',justificativa='Núcleo correto') for q in p])
        else:d=dict(resposta='A restrição altera a vazão.')
        kw['validate'](d);return d


class EvaluationTests(unittest.TestCase):
    def test_existing_benchmark_adapter_runs_both_arms_and_independent_audit(self):
        qs=[dict(uid=g+':a',grupo=g,item='02_02',tipo='mecanismo',composicao='simples',cenario=False,origem=g,
            pergunta='Como a restrição altera a vazão?',resposta='Depende das condições.',contexto_tecnico='A restrição altera a vazão.',
            blocos_contexto=[dict(id='B1',texto='A restrição altera a vazão.')]) for g in ['historico','novo_antigo','novo_refinado']]
        clients={k:EvalClient() for k in ['resp_gpt-4-1-nano','resp_gpt-4-1-mini','resp_gpt-4-1','juiz','faithfulness']}
        with tempfile.TemporaryDirectory() as t,redirect_stdout(io.StringIO()):
            result=evaluate(qs,Path(t)/'eval',clients=clients)
            self.assertEqual(result['status'],'concluido');self.assertEqual(len(result['gap_por_grupo']),9)
            self.assertEqual(result['sustentacao_por_grupo']['novo_refinado']['taxa_sustentacao'],100)


if __name__=='__main__':unittest.main()
