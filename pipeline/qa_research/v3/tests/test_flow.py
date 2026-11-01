"""Testes offline do fluxo inteiro e do transporte, sem credenciais ou chamadas reais."""
import asyncio
import copy
import io
import importlib.util
import json
import tempfile
import unittest
from contextlib import redirect_stdout
from pathlib import Path
from types import SimpleNamespace as NS
from unittest.mock import patch

from pipeline.domain_corpora.io_utils import file_hash
from pipeline.inventario.textutil import atomic_json, read_json
from pipeline.inventario.llm import BudgetExceeded
from pipeline.qa_research.v3 import contracts as C
from pipeline.qa_research.v3 import prompts as P
from pipeline.qa_research.v3.__main__ import configuration,execute,collect,main
from pipeline.qa_research.v3.runtime import Calls,CallFailure,topic
from pipeline.qa_research.v3.context import fit_write,input_size


def response(value, finish='stop', raw=None):
    return NS(choices=[NS(finish_reason=finish,message=NS(content=raw if raw is not None else json.dumps(value,ensure_ascii=False)))],
        usage=NS(prompt_tokens=100,completion_tokens=50))


class ServerError(Exception): status_code=500


class Model:
    def __init__(self):
        self.inputs=[];self.fail=set();self.refine=False;self.bad_section=None;self.writer_failed=None
        self.long_sections=False;self.regional=False;self.relevance='direta';self.gaps=[];self.essential=False;self.correction_failed=False
    async def __call__(self,role,messages,tokens):
        p=json.loads(messages[1]['content'])
        selecting='candidatas' in p and 'secao' in p
        self.inputs.append(('select' if selecting else role,p,tokens))
        if role in self.fail:raise ServerError('erro simulado')
        if p.get('tarefa'):return response({'ok':True})
        if selecting:
            return response(dict(selecionadas=[dict(id=s['id'],pertinencia=self.relevance,pontos=p['secao']['pontos'],
                aplicabilidade='Tratamento químico no processo simulado') for s in p['candidatas'][:p['limite']]],lacunas=[]))
        if role=='plan':
            d=dict(pontos=[dict(id='P1',ancora='espuma',descricao='Controle da espuma',prioritario=True),
                dict(id='P2',ancora='dosagem',descricao='Ajuste da dosagem',prioritario=True)],
                secoes=[dict(id=f'S{i}',titulo=f'Tratamento {i}',pontos=[f'P{i}'],
                    consultas=[dict(pt='tratamento químico espuma dosagem',en='chemical treatment foam dosing')]) for i in (1,2)])
        elif role=='write':
            sid=p['secao']['id']
            if sid==self.writer_failed:raise ServerError('seção temporariamente indisponível')
            if 'anterior' in p and self.correction_failed:raise ServerError('correção temporariamente indisponível')
            d=dict(titulo=p['secao']['titulo'],texto='O tratamento químico reduz a formação de espuma. A dosagem acompanha as condições do processo.',
                fontes=[p['fontes'][0]['id']] if p['fontes'] else [],complementos=[],lacunas=self.gaps)
            if self.long_sections:d['texto']+=' A equipe acompanha a aplicação durante a operação normal do processo.'*40
            if self.regional:d['texto']='A equipa verifica o caudal de água durante a operação.'
            if 'anterior' in p and any('EVIDENCIA_NOVA' in s['texto'] for s in p['fontes']):
                d['texto']+=' O residual confirmado orienta o ajuste da dosagem.'
                d['fontes']=[s['id'] for s in p['fontes']]
        elif role=='review':
            sections=p['secoes_enviadas'];mapping={s['id']:s['pontos'] for s in p['sumario']}
            coverage=[]
            for point in p['checklist']:
                used=[s['id'] for s in sections if point['id'] in mapping[s['id']]]
                missing=self.essential and point['id']=='P2' and not any('residual confirmado' in s['texto'] for s in sections)
                coverage.append(dict(id=point['id'],estado='parcial' if missing and used else 'atendido' if used else 'ausente',secoes=used,motivo='Parecer simulado'))
            d=dict(secoes=[dict(id=s['id'],decisao='corrigir' if s['id']==self.bad_section else 'liberar',
                motivo='Parecer técnico simulado',correcao='Corrigir o conteúdo técnico' if s['id']==self.bad_section else '',
                consultas=[dict(pt='criterioespecifico bombeamento residual',en='specificcriterion pump residual')] if self.essential and s['id']=='S2' and 'residual confirmado' not in s['texto'] else [],
                lacunas_essenciais=[dict(ponto='P2',descricao='Critério de ajuste aplicado')] if self.essential and s['id']=='S2' and 'residual confirmado' not in s['texto'] else [],
                limites=s.get('lacunas',[])) for s in sections],
                cobertura=coverage,omissoes_escopo=[])
        elif role=='author':
            qs=[]
            for i,s in enumerate(p['contexto'],1):
                point='P1' if s['id']=='S1' else 'P2'
                qs.append(dict(id=f'Q{i}',tipo='mecanismo',composicao='simples',cenario=False,
                    pergunta='Como o tratamento químico controla a espuma?' if point=='P1' else 'Como as condições do processo orientam a dosagem?',
                    resposta='Pela ação sobre a formação de espuma.' if point=='P1' else 'Pelo ajuste do tratamento às condições observadas.',
                    conhecimento='Relação '+point,ponte='',pontos=[point],fundamentos=[dict(secao=s['id'],trecho=s['texto'])]))
            d=dict(questoes=qs[:p['limite']],impedimentos=[])
        elif role=='solve':
            d=dict(resolucoes=[dict(id=q['id'],resposta='Resposta simulada com fundamento no contexto.',ambiguidades=[]) for q in p['questoes']])
        elif role=='judge':
            d=dict(avaliacoes=[dict(id=q['id'],decisao='corrigir' if self.refine and not p['originais'] else 'admitir',
                motivo='Melhorar a pergunta' if self.refine and not p['originais'] else 'Verificação simulada',duplicada_de=None,
                criterios={k:True for k in C.CRITERIA}) for q in p['candidatas']])
        elif role=='refine':
            d=dict(itens=[dict(id=r['id'],decisao='corrigida',motivo='Redação corrigida',
                questao=dict(r['questao'],pergunta=r['questao']['pergunta'].replace('Como','De que maneira'))) for r in p['corrigir']])
        return response(d)


class FlowTests(unittest.TestCase):
    def setUp(self):
        self.temp=tempfile.TemporaryDirectory();self.root=Path(self.temp.name)
        self.addCleanup(self.temp.cleanup)
        self.config=configuration(overrides=dict(sections=2,min_questions=2,max_batches=2,heartbeat=1))
        self.manifest=self.root/'corpus'/'manifest.json';self.manifest.parent.mkdir()
        pages=self.manifest.with_name('pages.jsonl')
        pages.write_text(json.dumps(dict(collection='manual',document_id='manual1',title='Manual simulado',
            text=('O tratamento químico reduz a formação de espuma e a dosagem acompanha as condições do processo. '*30)+' ORIGINAL_PRIVADO',
            page=1,source_boundary='known_document',language='pt',url='https://example.org/manual'))+'\n',encoding='utf-8')
        atomic_json(self.manifest,dict(schema='petroquest-professional-corpora-v1',ready=True,partial=True,
            collections=[dict(id='manual',format='pages_jsonl',path=pages.name,sha256=file_hash(pages),documents=1)]))
        self.output=self.root/'run';self.model=Model()

    def run_flow(self,stage='all',check=False):
        with redirect_stdout(io.StringIO()):
            return asyncio.run(execute(topic('02_02'),self.manifest,self.output,self.config,stage,transport=self.model,check=check))

    def test_complete_flow_resume_and_blind_solver(self):
        result=self.run_flow();self.assertEqual(result['status'],'concluido',result)
        self.assertEqual(result['questoes']['admitidas'],2)
        inputs=copy.deepcopy(self.model.inputs)
        roles=[r for r,_,_ in inputs]
        self.assertEqual(roles[0],'plan')
        self.assertCountEqual(roles[1:5],['select','select','write','write'])
        self.assertEqual(roles[5:],['review','author','solve','judge'])
        payload=next(p for r,p,_ in inputs if r=='solve')
        self.assertEqual(set(payload),{'questoes','contexto'})
        self.assertTrue(all(set(q)=={'id','pergunta'} for q in payload['questoes']))
        judge=next(p for r,p,_ in inputs if r=='judge')
        self.assertEqual(judge['entrada']['frase_especialista'],topic('02_02')['frase_especialista'])
        self.assertEqual({p['id'] for p in judge['pontos']},{'P1','P2'})
        self.config.update(workers=1,heartbeat=2,max_calls=140)
        resumed=self.run_flow();self.assertEqual(resumed['questoes']['admitidas'],2)
        self.assertEqual(self.model.inputs,inputs,'Retomada não deve repetir chamadas concluídas')
        doc=read_json(self.output/'contexto/documento.json')
        self.assertEqual(set(doc),{'titulo','secoes'})
        self.assertTrue(all(set(s)=={'titulo','texto'} for s in doc['secoes']))

    def test_selective_refinement_and_revalidation(self):
        self.model.refine=True;result=self.run_flow()
        self.assertEqual(result['questoes']['admitidas'],2,result)
        roles=[r for r,_,_ in self.model.inputs]
        self.assertEqual(roles.count('refine'),1);self.assertEqual(roles.count('solve'),2);self.assertEqual(roles.count('judge'),2)

    def test_known_technical_problem_excludes_section_and_blocks_qa(self):
        self.model.bad_section='S2';self.config['min_questions']=1
        result=self.run_flow();self.assertEqual(result['status'],'parcial',result)
        self.assertEqual(result['contexto']['secoes_liberadas'],1)
        self.assertIn('P2',result['contexto']['prioritarios_pendentes'])
        self.assertEqual(result['questoes']['admitidas'],0)
        self.assertEqual(result['questoes']['motivo_parada'],'contexto_pendente')
        self.assertFalse(any(r=='author' for r,_,_ in self.model.inputs))
        self.assertEqual(sum(r=='write' for r,_,_ in self.model.inputs),3,'Somente a seção problemática é reescrita')

    def test_operational_failure_of_section_preserves_other_section(self):
        self.model.writer_failed='S2';self.config['min_questions']=1
        result=self.run_flow();self.assertEqual(result['status'],'parcial',result)
        self.assertEqual(result['questoes']['admitidas'],0)
        self.assertEqual(result['contexto']['erros'][0]['secao'],'S2')

    def test_failure_in_qa_resumes_cached_document_and_author(self):
        self.model.fail={'solve'}
        result=self.run_flow();self.assertEqual(result['status'],'interrompido')
        before=len(self.model.inputs);self.model.fail.clear()
        resumed=self.run_flow();self.assertEqual(resumed['status'],'concluido',resumed)
        self.assertEqual([r for r,_,_ in self.model.inputs[before:]],['solve','judge'])

    def test_tampered_context_blocked_in_qa_only(self):
        self.run_flow(stage='context')
        path=self.output/'contexto/documento.json';doc=read_json(path);doc['secoes'][0]['texto']='Alteração externa'
        atomic_json(path,doc);before=len(self.model.inputs)
        result=self.run_flow(stage='qa');self.assertEqual(result['status'],'interrompido')
        self.assertIn('alterado',result['erro']);self.assertEqual(len(self.model.inputs),before)

    def test_collect_excludes_raw_sources_and_caches(self):
        self.run_flow();destination=self.root/'snapshot';collect(self.output,destination)
        self.assertFalse((destination/'.local').exists())
        self.assertTrue((destination/'questoes/qa.csv').exists())
        preparation=read_json(destination/'preparacao_corpus.json')
        self.assertEqual(preparation['manifest_sha256'],file_hash(self.manifest))
        self.assertEqual(preparation['collections'][0]['id'],'manual')
        for path in destination.rglob('*'):
            if path.is_file():self.assertNotIn('ORIGINAL_PRIVADO',path.read_text(encoding='utf-8-sig'))
        manifest=read_json(destination/'manifest_resultados.json')
        self.assertTrue(all(file_hash(destination/name)==sha for name,sha in manifest['files'].items()))

    def test_preflight_checks_three_model_specs(self):
        result=self.run_flow(check=True);self.assertEqual(result['status'],'verificado')
        self.assertEqual([r for r,_,_ in self.model.inputs],['write','review','solve'])
        self.assertFalse((self.output/'contexto').exists())

    def test_context_preflight_does_not_call_solver(self):
        result=self.run_flow(stage='context',check=True)
        self.assertEqual(result['status'],'verificado')
        self.assertEqual([r for r,_,_ in self.model.inputs],['write','review'])

    def test_context_collect_does_not_include_previous_questions(self):
        self.run_flow()
        self.run_flow(stage='context')
        target=self.root/'document_snapshot';collect(self.output,target)
        self.assertFalse((target/'questoes').exists())
        self.assertTrue(list((target/'contexto/versoes').glob('*/secoes/*.json')))

    def test_plan_is_read_only(self):
        with redirect_stdout(io.StringIO()):self.assertEqual(main(['--plan','--output',str(self.output)]),0)
        self.assertFalse(self.output.exists())

    def test_changed_qa_model_does_not_present_old_results_as_new(self):
        self.run_flow()
        self.config['models']['author']='outro-deployment:medium';self.model.fail={'author'}
        result=self.run_flow()
        self.assertEqual(result['status'],'interrompido')
        self.assertEqual(result['questoes']['admitidas'],0,'Resultados da versão anterior não podem parecer novos')
        self.assertTrue(list((self.output/'questoes/versoes').glob('*/lote_01.json')),'Histórico anterior deve continuar disponível')

    def test_source_hash_failure_happens_before_any_model_call(self):
        self.manifest.with_name('pages.jsonl').write_text('arquivo alterado',encoding='utf-8')
        with self.assertRaises(ValueError):self.run_flow()
        self.assertEqual(self.model.inputs,[])

    def test_only_generic_evidence_leaves_report_and_never_writes(self):
        self.model.relevance='apoio'
        result=self.run_flow()
        self.assertEqual(result['status'],'parcial',result)
        self.assertFalse(result['contexto']['qa_elegivel'])
        self.assertEqual(result['contexto']['secoes_liberadas'],0)
        self.assertFalse(any(r in ('write','review','author') for r,_,_ in self.model.inputs))
        self.assertTrue((self.output/'contexto/documento.md').exists())

    def test_optional_limits_do_not_veto_sound_document(self):
        self.model.gaps=['Não há faixas quantitativas universais por fabricante']
        result=self.run_flow()
        self.assertTrue(result['contexto']['qa_elegivel'],result)
        self.assertEqual(sum(r=='write' for r,_,_ in self.model.inputs),2)
        self.assertEqual(result['contexto']['secoes_liberadas'],2)

    def test_essential_gap_preserves_good_text_but_blocks_qa_without_new_evidence(self):
        self.model.essential=True
        result=self.run_flow()
        self.assertEqual(result['status'],'parcial',result)
        self.assertEqual(result['contexto']['secoes_liberadas'],2)
        self.assertEqual(result['contexto']['prioritarios_pendentes'],['P2'])
        self.assertEqual(sum(r=='write' for r,_,_ in self.model.inputs),2)
        self.assertEqual(sum(r=='select' for r,_,_ in self.model.inputs),2)
        self.assertEqual(sum(r=='review' for r,_,_ in self.model.inputs),1)
        self.assertFalse(any(r=='author' for r,_,_ in self.model.inputs))

    def add_specific_evidence(self):
        path=self.manifest.with_name('pages.jsonl')
        extra=dict(collection='manual',document_id='specific',title='Critério específico simulado',
            text=('EVIDENCIA_NOVA criterioespecifico residual bombeamento verificacao controle acompanhamento leitura. '*15),
            page=1,source_boundary='known_document',language='pt',url='https://example.org/specific')
        with path.open('a',encoding='utf-8') as stream:stream.write(json.dumps(extra)+'\n')
        manifest=read_json(self.manifest);manifest['collections'][0]['sha256']=file_hash(path);atomic_json(self.manifest,manifest)

    def test_only_section_with_new_direct_support_is_completed_and_reviewed(self):
        self.add_specific_evidence();self.model.essential=True
        result=self.run_flow()
        self.assertEqual(result['status'],'concluido',result)
        self.assertEqual(sum(r=='select' for r,_,_ in self.model.inputs),3)
        self.assertEqual(sum(r=='write' for r,_,_ in self.model.inputs),3)
        self.assertEqual(sum(r=='review' for r,_,_ in self.model.inputs),2)
        corrected=[p for r,p,_ in self.model.inputs if r=='write' and 'anterior' in p]
        self.assertEqual([p['secao']['id'] for p in corrected],['S2'])
        self.assertGreater(len(corrected[0]['fontes']),len(corrected[0]['anterior']['fontes']),
            'Complementação conserva evidência anterior e acrescenta suporte novo')

    def test_failed_coverage_improvement_preserves_previously_sound_section(self):
        self.add_specific_evidence();self.model.essential=True;self.model.correction_failed=True
        result=self.run_flow()
        self.assertEqual(result['status'],'parcial',result)
        self.assertEqual(result['contexto']['secoes_liberadas'],2)
        self.assertFalse(result['contexto']['qa_elegivel'])
        self.assertIn('P2',result['contexto']['prioritarios_pendentes'])
        self.assertEqual(sum(r=='review' for r,_,_ in self.model.inputs),1)

    def test_failed_technical_repair_excludes_bad_section_but_preserves_draft(self):
        self.model.bad_section='S2';self.model.correction_failed=True
        result=self.run_flow(stage='context')
        self.assertEqual(result['contexto']['secoes_liberadas'],1,result)
        self.assertEqual(result['contexto']['secoes_para_revisao'],2)
        released=(self.output/'contexto/documento.md').read_text(encoding='utf-8')
        draft=(self.output/'contexto/rascunho_para_revisao.md').read_text(encoding='utf-8')
        self.assertNotIn('Tratamento 2',released)
        self.assertIn('Tratamento 2',draft)

    def test_default_execution_stops_at_document_and_does_not_read_examples(self):
        with redirect_stdout(io.StringIO()),patch('pipeline.qa_research.v3.__main__.load_examples',side_effect=AssertionError('não ler QA')):
            result=asyncio.run(execute(topic('02_02'),self.manifest,self.output,self.config,transport=self.model))
        self.assertEqual(result['status'],'concluido',result)
        self.assertNotIn('questoes',result)
        self.assertFalse(any(r=='author' for r,_,_ in self.model.inputs))

    def test_previous_quality_policy_cannot_unlock_qa(self):
        self.run_flow(stage='context')
        path=self.output/'contexto/cobertura.json';report=read_json(path)
        report.pop('criterio_qualidade');report['qa_elegivel']=True;atomic_json(path,report)
        result=self.run_flow(stage='qa')
        self.assertEqual(result['questoes']['motivo_parada'],'contexto_pendente')
        self.assertFalse(any(r=='author' for r,_,_ in self.model.inputs))

    def test_large_review_splits_without_dropping_sources_and_checks_coherence(self):
        self.model.long_sections=True
        self.run_flow(stage='context')
        full=next(p for r,p,_ in self.model.inputs if r=='review')
        single=dict(full,secoes_enviadas=full['secoes_enviadas'][:1])
        sizes=[len(json.dumps(p,ensure_ascii=False))+len(P.PROMPTS[r]) for r,p,_ in self.model.inputs if r in ('plan','write')]
        lower=max(sizes+[len(json.dumps(single,ensure_ascii=False))+len(P.REVIEW)])
        upper=len(json.dumps(full,ensure_ascii=False))+len(P.REVIEW)
        self.assertLess(lower,upper)
        self.config['max_input_chars']=(lower+upper)//2
        self.model.inputs.clear();result=self.run_flow(stage='context')
        self.assertEqual(result['contexto']['secoes_liberadas'],2,result)
        reviews=[p for r,p,_ in self.model.inputs if r=='review']
        self.assertEqual(len(reviews),3)
        self.assertEqual(reviews[-1]['modo'],'coerencia_final')
        self.assertTrue(all(p['fontes'] for p in reviews[:-1]))

    def test_known_regionalisms_cannot_pass_despite_model_approval(self):
        self.model.regional=True
        result=self.run_flow()
        self.assertEqual(result['contexto']['secoes_liberadas'],0,result)
        self.assertFalse(any(r=='author' for r,_,_ in self.model.inputs))

    def test_large_source_metadata_is_packed_before_writing_and_review(self):
        path=self.manifest.with_name('pages.jsonl')
        row=json.loads(path.read_text(encoding='utf-8'));row['url']='https://example.org/'+('x'*220000)
        path.write_text(json.dumps(row)+'\n',encoding='utf-8')
        manifest=read_json(self.manifest);manifest['collections'][0]['sha256']=file_hash(path);atomic_json(self.manifest,manifest)
        result=self.run_flow();self.assertEqual(result['status'],'concluido',result)
        writers=[p for r,p,_ in self.model.inputs if r=='write']
        self.assertEqual(len(writers),2)
        self.assertTrue(all('url' not in s for p in writers for s in p['fontes']))
        version=result['contexto']['versao']
        size=read_json(self.output/'contexto/versoes'/version/'entradas/S1.json')
        self.assertGreater(size['caracteres_antes'],self.config['max_input_chars'])
        self.assertLess(size['caracteres_depois'],self.config['max_input_chars'])
        self.assertEqual(size['excluidas'],[],'Metadado extenso não deve eliminar a passagem técnica')


class TransportTests(unittest.TestCase):
    def setUp(self):
        self.temp=tempfile.TemporaryDirectory();self.root=Path(self.temp.name);self.addCleanup(self.temp.cleanup)
        self.config=configuration(overrides={'heartbeat':1})

    def run_call(self,transport,validator=lambda d:None):
        async def run():
            calls=Calls(self.root,self.config,transport=transport)
            try:return await calls.call('review','teste',{'contexto':'simulado'},validator)
            finally:await calls.close()
        with redirect_stdout(io.StringIO()):return asyncio.run(run())

    def test_truncation_gets_full_budget_on_last_attempt(self):
        tokens=[]
        async def transport(role,messages,limit):
            tokens.append(limit);return response({'ok':True},'length' if len(tokens)==1 else 'stop')
        self.assertEqual(self.run_call(transport),{'ok':True});self.assertEqual(tokens,[16000,32000])
        self.assertEqual(read_json(self.root/'orcamento.json')['tentativas_reservadas'],2)

    def test_two_truncations_never_enter_a_nested_retry_loop(self):
        count=[]
        async def transport(*args):count.append(1);return response({},'length')
        with self.assertRaisesRegex(CallFailure,'2 tentativas'):self.run_call(transport)
        self.assertEqual(len(count),2)

    def test_schema_repair_gets_actionable_error_and_then_caches(self):
        inputs=[]
        async def transport(role,messages,limit):
            inputs.append(messages);return response({'ok':len(inputs)>1})
        def validate(d):C.require(d.get('ok') is True,'campo ok precisa ser true')
        self.assertEqual(self.run_call(transport,validate),{'ok':True})
        self.assertIn('campo ok',inputs[1][-1]['content'])
        self.run_call(transport,validate);self.assertEqual(len(inputs),2)

    def test_timeout_cancels_requests_and_finishes(self):
        self.config['request_timeout']=.02;cancelled=[]
        async def transport(*args):
            try:await asyncio.sleep(30)
            finally:cancelled.append(True)
        with self.assertRaisesRegex(CallFailure,'TimeoutError'):self.run_call(transport)
        self.assertEqual(len(cancelled),2)

    def test_transient_server_error_retries_once(self):
        attempts=[]
        async def transport(*args):
            attempts.append(1)
            if len(attempts)==1:raise ServerError('erro com corpo que não deve ir ao log')
            return response({'ok':True})
        self.assertEqual(self.run_call(transport),{'ok':True});self.assertEqual(len(attempts),2)
        self.assertNotIn('corpo que',(self.root/'chamadas_llm.jsonl').read_text())

    def test_budget_is_cumulative_and_enforced_before_api(self):
        self.config['max_calls']=1;attempts=[]
        async def transport(*args):attempts.append(1);return response({},'length')
        with self.assertRaises(BudgetExceeded):self.run_call(transport)
        self.assertEqual(len(attempts),1)

    def test_contradictory_judgment_cannot_admit_question(self):
        row=dict(id='Q1',decisao='admitir',motivo='teste',duplicada_de=None,criterios={k:True for k in C.CRITERIA})
        row['criterios']['correta']=False
        with self.assertRaisesRegex(ValueError,'contradiz'):C.judged({'avaliacoes':[row]},{'Q1'},set())

    def test_duplicate_must_point_to_an_admitted_question(self):
        rows=[dict(id=k,decisao='descartar',motivo='teste',duplicada_de=v,criterios={k:False for k in C.CRITERIA}) for k,v in [('Q1','Q2'),('Q2','Q1')]]
        with self.assertRaisesRegex(ValueError,'admitida'):C.judged({'avaliacoes':rows},{'Q1','Q2'},set())

    def test_human_progress_explains_retry_without_showing_token_configuration(self):
        shown=[];attempts=[]
        async def transport(*args):
            attempts.append(1)
            if len(attempts)==1:raise ServerError('simulado')
            return response({'ok':True})
        async def run():
            calls=Calls(self.root,self.config,transport=transport,progress=lambda value,**kwargs:shown.append(value))
            await calls.call('review','teste',{},lambda d:None)
        asyncio.run(run())
        self.assertTrue(any('Falha temporária' in s for s in shown))
        self.assertFalse(any('tokens' in s or 'tentativa 0' in s for s in shown))
        logs=[json.loads(line) for line in (self.root/'chamadas_llm.jsonl').read_text().splitlines()]
        self.assertEqual([r['attempt'] for r in logs],[1,2])
        self.assertTrue(all(r['max_tokens']==16000 for r in logs))

    @unittest.skipUnless(importlib.util.find_spec('openai'),'SDK não instalado neste Python; executar também no ambiente do SDK')
    def test_real_async_sdk_adapter_with_mock_http(self):
        import httpx
        from azure_openai_backend import AzureSettings
        async def run():
            for base_url in (False,True):
                settings=AzureSettings(azure_endpoint='https://sdk-test.invalid/openai' if base_url else 'https://sdk-test.invalid',
                    azure_api_key='CHAVE_SINTETICA_TESTE',azure_api_version='2024-10-21',use_base_url=base_url)
                with patch('azure_openai_backend.AzureSettings.load',return_value=settings):
                    calls=Calls(self.root/str(base_url),self.config)
                calls.make_client();http=calls.client._client;old=http._transport;seen=[]
                async def handler(request):
                    seen.append(json.loads(request.content))
                    self.assertEqual(request.headers['api-key'],'CHAVE_SINTETICA_TESTE')
                    return httpx.Response(200,json={'id':'test','object':'chat.completion','created':0,
                        'model':'simulado','choices':[{'index':0,'finish_reason':'stop','message':{'role':'assistant','content':'{"ok":true}'}}],
                        'usage':{'prompt_tokens':10,'completion_tokens':20,'total_tokens':30}})
                http._transport=httpx.MockTransport(handler);http._mounts={}
                try:
                    result=await calls.call('review','adaptador',{'teste':True},lambda d:C.require(d.get('ok'),'ok obrigatório'))
                    self.assertEqual(result,{'ok':True})
                    self.assertEqual(seen[0]['max_completion_tokens'],16000)
                    self.assertEqual(seen[0]['reasoning_effort'],'high')
                    self.assertEqual(calls.client.max_retries,0)
                    self.assertNotIn('CHAVE_SINTETICA_TESTE',(calls.output/'chamadas_llm.jsonl').read_text())
                finally:
                    await calls.close();await old.aclose()
        with redirect_stdout(io.StringIO()):asyncio.run(run())


class PackingTests(unittest.TestCase):
    def setUp(self):
        self.config=configuration()
        self.payload=dict(entrada=topic('02_02'),sumario=[dict(id='S1',titulo='Tratamento',pontos=['P1'],consultas=[dict(pt='tratamento químico espuma',en='chemical foam treatment')])],
            secao=dict(id='S1',titulo='Tratamento',pontos=['P1'],consultas=[]),palavras_alvo=700,
            fontes=[dict(id='E1',texto='Explicação técnica integral.',url='https://example.org/manual')])

    def test_small_packet_is_unchanged_to_reuse_previous_calls(self):
        packed,detail=fit_write(self.payload,self.config)
        self.assertIs(packed,self.payload)
        self.assertFalse(detail['ajustado'])

    def test_huge_metadata_is_removed_without_cutting_technical_text(self):
        self.payload['fontes'][0].update(url='https://example.org/'+('x'*250000),title='t'*200000)
        original=copy.deepcopy(self.payload)
        packed,detail=fit_write(self.payload,self.config)
        self.assertEqual(packed['fontes'][0]['texto'],original['fontes'][0]['texto'])
        self.assertEqual(self.payload,original,'Originais devem permanecer intactos')
        self.assertLessEqual(input_size(packed,P.WRITE),self.config['max_input_chars'])
        self.assertEqual(detail['excluidas'],[])

    def test_oversized_passage_is_skipped_whole_and_alternative_is_kept(self):
        self.payload['fontes']=[dict(id='E1',texto='x'*250000),dict(id='E2',texto='Passagem alternativa com condições completas.')]
        packed,detail=fit_write(self.payload,self.config)
        self.assertEqual(packed['fontes'],[self.payload['fontes'][1]])
        self.assertEqual(detail['excluidas'][0]['id'],'E1')
        self.assertEqual(packed['entrada'],self.payload['entrada'])

    def test_no_fitting_source_is_explicitly_diagnosed(self):
        self.payload['fontes']=[dict(id='E1',texto='x'*250000)]
        packed,detail=fit_write(self.payload,self.config)
        self.assertIn('Nenhuma passagem',detail['erro'])
        self.assertEqual(packed['fontes'],[])
