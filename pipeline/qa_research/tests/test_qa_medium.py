"""Duas amostras, prompts isolados e acurácia em fluxo contínuo, sem API real."""
import copy
import io
import json
import tempfile
import threading
import unittest
from pathlib import Path
from contextlib import redirect_stdout
from unittest.mock import patch

from pipeline.qa_research.qa_medium import core as Q
from pipeline.qa_research.tests.test_sem_conteudo import question
from pipeline.qa_research.tests.test_especialista_finalizacao import Respondente,Juiz


class Resposta(Respondente):
    def __init__(self,wait_for_judge=None,long=False,**kw):
        super().__init__(**kw);self.requests=[];self.event=wait_for_judge;self.long=long
    def json(self,system,user,tag='',validate=None,**kw):
        self.requests.append(dict(system=system,user=user,tag=tag))
        if tag.startswith('resposta_') and user.endswith('última?') and self.event is not None:
            if not self.event.wait(4):raise AssertionError('O juiz deveria trabalhar antes da última resposta')
        d=super().json(system,user,tag=tag,validate=validate,**kw)
        if self.long and tag.startswith('resposta_'):d={'resposta':' '.join(['palavra']*110)}
        return d


class Julgamento(Juiz):
    def __init__(self,event=None,**kw):
        super().__init__(**kw);self.event=event;self.systems=[]
    def json(self,system,user,**kw):
        self.systems.append(system)
        if self.event is not None:self.event.set()
        return super().json(system,user,**kw)


class MediumTests(unittest.TestCase):
    def setUp(self):
        self.tmp=tempfile.TemporaryDirectory();self.addCleanup(self.tmp.cleanup)
        self.root=Path(self.tmp.name);self.out=self.root/'saida';self.manifest=self.root/'manifesto.json'
        self.data=dict(schema='qa-medium-amostras-v1',semente=20261028,repeticao=1,condicoes=[])
        for key in ('sem_contexto','default_ampliado'):
            rows=[{**question(),'uid':f'{key}:{i}','item':'01_01','origem':key,
                   'pergunta':f'Pergunta {key} {i}'+(' última?' if i==3 else '?')} for i in range(4)]
            p=self.root/key/'questoes.jsonl';Q.C.GeracaoSemConteudo.jsonl(p,rows)
            self.data['condicoes'].append(dict(id=key,rotulo=key,n=4,
                fontes=[dict(path=str(p),n=4,sha256=Q.C.sha(rows))],uids=[q['uid'] for q in rows],amostra_sha256=Q.C.sha(rows)))
        Q.atomic_json(self.manifest,self.data)
        self.logs=[]

    def evaluate(self,n=None,g=None,j=None,**kw):
        return Q.avaliar(self.out,manifesto=self.manifest,workers=2,judge_workers=1,
            lote_juiz=kw.pop('lote_juiz',2),clientes={'resp_gpt-5-4-nano':n or Resposta(),
                'resp_gpt-5-4':g or Resposta(),'juiz':j or Julgamento()},
            progress=lambda s,**kw:self.logs.append(s),**kw)

    def test_amostras_reais_exatamente_primeiro_sorteio_default_ampliado(self):
        data,rows=Q.carregar()
        self.assertEqual(len(rows),2000)
        self.assertEqual([c['n'] for c in data['condicoes']],[1000,1000])
        self.assertEqual({c['rotulo'] for c in data['condicoes']},{'Sem contexto','Default + Ampliado'})
        from pipeline.qa_research.sem_conteudo.amostra import carregar
        _,old=carregar()
        self.assertEqual([q['uid'] for q in rows if q['condicao']=='sem_contexto'],[q['uid'] for q in old])
        path=Q.C.ROOT/'docs/ablacoes_amostras_1000_20261028/amostras.jsonl'
        if path.exists():
            d=next(q for q in Q.linhas(path) if q['ablacao']=='Default + Ampliado' and q['repeticao']==1)
            self.assertEqual([q['uid'] for q in rows if q['condicao']=='default_ampliado'],d['uids'])

    def test_medium_e_novos_prompts_chegam_aos_papeis_corretos(self):
        n,g,j=Resposta(),Resposta(),Julgamento()
        self.assertEqual(self.evaluate(n,g,j),0)
        cfg=Q.read_json(self.out/'config.json')
        self.assertTrue(all(alias.endswith(':medium') for alias in cfg['respondentes'].values()))
        self.assertEqual(cfg['max_palavras'],100)
        self.assertEqual((n.calls,g.calls),(8,8))
        for r in n.requests+g.requests:
            self.assertEqual(r['system'],Q.prompt('respondente'))
            self.assertNotIn('resposta_referencia',r['user'])
        self.assertTrue(all(s==Q.prompt('juiz') for s in j.systems))
        for payload in j.payloads:
            self.assertTrue(all(set(q)=={'id','pergunta','resposta_referencia','resposta_candidato'} for q in payload))
        summary=Q.read_json(self.out/'avaliacao/acuracia.json')
        self.assertEqual(set(summary['por_condicao']),{'sem_contexto','default_ampliado'})
        self.assertEqual(summary['por_condicao']['sem_contexto']['gpt-5-4']['n'],4)

    def test_juiz_e_acuracia_antes_de_terminar_respostas(self):
        event=threading.Event();n,g,j=Resposta(event),Resposta(event),Julgamento(event)
        self.assertEqual(self.evaluate(n,g,j),0)
        self.assertTrue(event.is_set())
        self.assertTrue(any('[AO VIVO' in s and 'julgadas 2' in s for s in self.logs))
        self.assertTrue(any('[AO VIVO' in s and 'acurácia 100.00%' in s for s in self.logs))

    def test_retomada_nao_refaz_respostas_julgadas(self):
        n,g,j=Resposta(),Resposta(),Julgamento()
        self.assertEqual(self.evaluate(n,g,j),0)
        calls=(n.calls,g.calls,j.calls)
        self.assertEqual(self.evaluate(n,g,j),0)
        self.assertEqual((n.calls,g.calls,j.calls),calls)

    def test_retomada_de_lote_incompleto_com_todas_respostas_salvas(self):
        n,g=Resposta(),Resposta()
        self.assertEqual(self.evaluate(n,g,Julgamento(blocked=True),lote_juiz=10),0)
        self.assertEqual((n.calls,g.calls),(8,8))
        self.assertEqual(self.evaluate(n,g,Julgamento(),lote_juiz=10),0)
        # Bloqueios são terminais: não reenvia esses lotes.
        self.assertEqual(Q.read_json(self.out/'avaliacao/acuracia.json')['geral']['gpt-5-4']['n'],0)

    def test_falha_juiz_retoma_so_julgamento_incluindo_sobra(self):
        class Falha:
            def json(self,*a,**kw):raise RuntimeError('falha transitória')
        n,g,j=Resposta(),Resposta(),Julgamento()
        self.assertEqual(self.evaluate(n,g,Falha(),lote_juiz=10),2)
        self.assertFalse((self.out/'avaliacao/avaliacao_concluida.json').exists())
        self.assertEqual(self.evaluate(n,g,j,lote_juiz=10),0)
        self.assertEqual((n.calls,g.calls,j.calls),(8,8,2))

    def test_bloqueios_nao_recebem_nota_e_nao_sao_reenviados(self):
        n,g,j=Resposta(blocked=True),Resposta(),Julgamento()
        self.assertEqual(self.evaluate(n,g,j),0)
        s=Q.read_json(self.out/'avaliacao/acuracia.json')['por_condicao']['sem_contexto']['gpt-5-4-nano']
        self.assertEqual((s['n'],s['sem_nota']),(0,4));self.assertIsNone(s['acuracia'])
        before=n.calls
        self.assertEqual(self.evaluate(n,g,j),0);self.assertEqual(n.calls,before)

    def test_registra_excesso_de_palavras_sem_cortar_ou_regenerar(self):
        n=Resposta(long=True)
        self.assertEqual(self.evaluate(n=n),0)
        self.assertEqual(n.calls,8)
        rows=Q.linhas(self.out/'avaliacao/avaliacoes.jsonl')
        self.assertTrue(all(q['palavras_gpt-5-4-nano']==110 for q in rows))

    def test_rejeita_mudancas_protocolo_e_arquivos(self):
        self.evaluate()
        with self.assertRaisesRegex(ValueError,'Configuração mudou'):self.evaluate(lote_juiz=3)
        with patch.object(Q,'prompt',side_effect=lambda n:'prompt alterado'):
            with self.assertRaisesRegex(ValueError,'Configuração mudou'):self.evaluate()
        path=self.out/'questoes.jsonl';rows=Q.linhas(path);rows[0]['pergunta']='alterada'
        Q.C.GeracaoSemConteudo.jsonl(path,rows)
        with self.assertRaisesRegex(ValueError,'salvas alteradas'):self.evaluate()

    def test_plano_sem_saida_ou_chamadas(self):
        with patch.object(Q,'avaliar',side_effect=AssertionError('Sem API')),redirect_stdout(io.StringIO()):
            self.assertEqual(Q.main(['--manifesto',str(self.manifest),'--saida',str(self.out),'--plano']),0)
        self.assertFalse(self.out.exists())

    def test_modelo_indisponivel_impede_conclusao(self):
        class Falha:
            def json(self,*a,**kw):raise RuntimeError('deployment indisponível')
        self.assertEqual(self.evaluate(n=Falha()),2)
        self.assertFalse((self.out/'avaliacao/avaliacao_concluida.json').exists())
        self.assertEqual(self.evaluate(),0)

    def test_juiz_exige_justificativa_e_preserva_ids(self):
        good=dict(avaliacoes=[dict(id='Q1',veredito='parcial',justificativa='Falta o mecanismo solicitado.')])
        Q.validar_juiz(good,['Q1'])
        bad=copy.deepcopy(good);bad['avaliacoes'][0]['justificativa']=''
        with self.assertRaisesRegex(ValueError,'justificativa'):Q.validar_juiz(bad,['Q1'])
        with self.assertRaises(ValueError):Q.validar_juiz(good,['Q2'])


if __name__=='__main__':unittest.main()
