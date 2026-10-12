"""Contratos do revisor: corrigir conhecimento relevante e preservar a origem."""
import copy
import json
import tempfile
import unittest
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor
from unittest.mock import patch
import contextlib
import io

from pipeline.inventario import revisao as R, consolidacao as C, fichas as F
from pipeline.inventario.run_inventario import main, select_subtopics
from pipeline.fase_3.topicos import TOPICOS
from test_execucao import FakeLLM, fixture, TOPIC

QUOTE = 'A taxa de falha representa a probabilidade de um item falhar durante um determinado espaço de tempo.'
SUB = {'key':'s1','topico':'KPI','subtopico':'Confiabilidade'}
SUBJECTS = [{'id':'a01','texto':'confiabilidade dos ativos','generico':False,'literal':True,
             'consulta_pt':'confiabilidade','consulta_en':'reliability'},
            {'id':'a02','texto':'riscos','generico':False,'literal':True,'consulta_pt':'riscos','consulta_en':'risks'}]


def original(uid='d#u1'):
    return {'uid':uid,'tipo':'definicao','afirmacao':'Taxa de falha é a probabilidade de falhar num intervalo.',
            'condicoes':'','assuntos':['a01'],'aplicabilidade':'transferivel','valor':'alto','entidades':[],
            'citacao':QUOTE,'citacao_verificada':True,
            'fonte':{'chunk_id':'d','collection':'regis','document_id':'d','title':'Fonte de confiabilidade'}}


def verdict(u, decision='refinar'):
    refined = {k:copy.deepcopy(u[k]) for k in R.FIELDS}
    if decision=='refinar':
        refined['afirmacao']='A taxa de falha é uma taxa instantânea condicional por unidade de tempo.'
    return {'uid':u['uid'],'decisao':decision,'motivo':'Corrigir a distinção entre taxa e probabilidade.',
            'carater_avaliativo':'conhecimento_profissional','alvo_qa':'Distinguir taxa e probabilidade de falha.',
            'base':'referencia_tecnica' if decision=='refinar' else 'fonte_original',
            'referencias':['nist_taxa_falha'] if decision=='refinar' else [],
            'suporte_citacao':decision!='refinar',
            'unidade':refined if decision in ('aprovar','refinar') else None}


class Reviewer:
    model='gpt-5-4-petrobras'
    effort='medium'
    def __init__(self, decision='refinar'):
        self.decision=decision
        self.calls=0
    def json(self,system,user,**kwargs):
        self.calls+=1
        data={'pareceres':[verdict(u,self.decision) for u in json.loads(user)['unidades']]}
        kwargs['validate'](data)
        return data


class RevisaoTests(unittest.TestCase):
    def setUp(self):
        self.u=original()
        self.chunks={'d':{'chunk_id':'d','texto':QUOTE}}

    def check(self,row):
        return R.validator([self.u],self.chunks,SUBJECTS)({'pareceres':[row]})

    def test_corrige_taxa_sem_descartar_trecho(self):
        kept,discarded,pending,rows,stats=R.review_units(Reviewer(),SUB,[self.u],self.chunks,SUBJECTS)
        self.assertEqual(stats['refinar'],1)
        self.assertEqual(len(kept),1)
        self.assertEqual(discarded+pending,[])
        self.assertEqual(kept[0]['citacao'],QUOTE)
        self.assertNotEqual(kept[0]['afirmacao'],self.u['afirmacao'])
        self.assertEqual(kept[0]['revisao']['afirmacao_original'],self.u['afirmacao'])
        self.assertFalse(kept[0]['revisao']['suporte_citacao'])
        self.assertEqual(self.u,original())

    def test_refinamento_propagado_a_ficha(self):
        kept,*_=R.review_units(Reviewer(),SUB,[self.u],self.chunks,SUBJECTS)
        c=C._from_members(kept,'s1',1,'unica')
        self.assertTrue(c['revisada'])
        md=F.render_ficha(SUB,SUBJECTS[0],[c],{})
        self.assertIn('Antes da revisão',md)
        self.assertIn('nist.gov',md)
        self.assertIn('registra a origem',md)

    def test_recupera_unidade_descartada_na_extracao(self):
        u=original();u['descartada_por']=['valor_baixo']
        kept,*_=R.review_units(Reviewer(),SUB,[u],self.chunks,SUBJECTS)
        self.assertEqual(len(kept),1)
        self.assertNotIn('descartada_por',kept[0])

    def test_pendente_nao_e_fora_escopo(self):
        kept,rejected,pending,rows,stats=R.review_units(Reviewer('pendente'),SUB,[self.u],self.chunks,SUBJECTS)
        self.assertEqual(kept+rejected,[])
        self.assertEqual(len(pending),1)
        self.assertEqual(pending[0]['afirmacao'],self.u['afirmacao'])

    def test_fora_escopo_preserva_parecer(self):
        kept,rejected,pending,rows,stats=R.review_units(Reviewer('fora_escopo'),SUB,[self.u],self.chunks,SUBJECTS)
        self.assertEqual(kept+pending,[])
        self.assertEqual(rejected[0]['descartada_por'],['revisor_fora_escopo'])
        self.assertTrue(rows[0]['parecer']['motivo'])

    def test_rejeita_uid_trocado(self):
        r=verdict(self.u);r['uid']='outra-fonte'
        with self.assertRaises(ValueError):self.check(r)

    def test_rejeita_citacao_fabricada(self):
        r=verdict(self.u);r['unidade']['citacao']='A taxa é sempre de cinco falhas por hora em todos os equipamentos.'
        with self.assertRaises(ValueError):self.check(r)

    def test_rejeita_referencia_inventada(self):
        r=verdict(self.u);r['referencias']=['norma-xyz']
        with self.assertRaises(ValueError):self.check(r)

    def test_rejeita_numero_inventado(self):
        r=verdict(self.u);r['unidade']['afirmacao']='A taxa de falha é de 50 por hora.'
        with self.assertRaises(ValueError):self.check(r)

    def test_numero_ja_inventado_na_extracao_nao_vira_evidencia(self):
        self.u['afirmacao']='Taxa de falha é de 50 por hora.'
        r=verdict(self.u,'aprovar')
        with self.assertRaises(ValueError):self.check(r)

    def test_rejeita_valor_ausente(self):
        r=verdict(self.u);r['unidade']['condicoes']='Pressão limitada a <NUMBER> bar'
        with self.assertRaises(ValueError):self.check(r)

    def test_rejeita_obrigacao_sem_suporte(self):
        r=verdict(self.u);r['unidade']['tipo']='requisito_normativo';r['unidade']['condicoes']='Brasil'
        with self.assertRaises(ValueError):self.check(r)

    def test_mudanca_nao_pode_ser_oculta_como_aprovacao(self):
        r=verdict(self.u,'aprovar');r['unidade']['afirmacao']='Outra afirmação.'
        with self.assertRaises(ValueError):self.check(r)

    def test_memoria_do_caso_nao_pode_ser_aprovada(self):
        r=verdict(self.u,'aprovar');r['carater_avaliativo']='memoria_do_caso'
        r['alvo_qa']='Recordar quantas viagens o OIM realizou.'
        with self.assertRaises(ValueError):self.check(r)

    def test_aprovacao_precisa_de_alvo(self):
        r=verdict(self.u,'aprovar');r['alvo_qa']=''
        with self.assertRaises(ValueError):self.check(r)

    def test_alvo_preservado_na_consolidacao_e_documento(self):
        kept,*_=R.review_units(Reviewer(),SUB,[self.u],self.chunks,SUBJECTS)
        c=C._from_members(kept,'s1',1,'unica')
        self.assertEqual(c['alvos_qa'][0]['descricao'],'Distinguir taxa e probabilidade de falha.')
        self.assertIn('Conhecimento avaliável',F.render_ficha(SUB,SUBJECTS[0],[c],{}))

    def test_rejeita_pareceres_incompletos(self):
        with self.assertRaises(ValueError):R.validator([self.u],self.chunks,SUBJECTS)({'pareceres':[]})

    def test_lotes_e_ordem_deterministica(self):
        units=[original(f'd#u{i}') for i in range(11,-1,-1)]
        llm=Reviewer()
        with ThreadPoolExecutor(2) as pool:
            kept,*_=R.review_units(llm,SUB,units,self.chunks,SUBJECTS,batch_size=3,pool=pool)
        self.assertEqual(llm.calls,4)
        self.assertEqual([u['uid'] for u in kept],sorted(u['uid'] for u in units))

    def test_documento_nao_repete_unidade_em_varios_assuntos(self):
        with tempfile.TemporaryDirectory() as tmp:
            out=Path(tmp);d=out/'subtopicos'/'sub'
            u=original();u['assuntos']=['a01','a02']
            c=C._from_members([u],'s1',1,'unica')
            rows=F.write_subtopic(d,SUB,SUBJECTS,[c],{}, {})
            F.write_topic_documents(out,rows)
            p=next((out/'topicos').glob('*/documento_tecnico.md'))
            text=p.read_text(encoding='utf-8')
            self.assertEqual(text.count('#### c0001'),1)
            self.assertIn('a01, a02',text)

    def test_proximo_topico_tem_doze_subtopicos(self):
        selected=select_subtopics(TOPICOS,['Produção e Processo (Medição Fiscal e Sistema de Alívio)'],[])
        self.assertEqual(len(selected),12)
        self.assertTrue(all(s['topico'].startswith('Produção e Processo') for s in selected))

    def test_pipeline_completo_dos_doze_subtopicos_sem_qa(self):
        with tempfile.TemporaryDirectory() as tmp,patch('pipeline.inventario.run_inventario.LLMClient',FakeLLM), \
             contextlib.redirect_stdout(io.StringIO()):
            out=Path(tmp)/'out';manifest=fixture(Path(tmp))
            main(['--corpus-manifest',str(manifest),'--allow-sample-corpus','--topicos',
                  'Produção e Processo (Medição Fiscal e Sistema de Alívio)',
                  '--output',str(out),'--embedder','hash','--min-rerank','0'])
            self.assertEqual(len(list((out/'subtopicos').glob('*/resumo_revisao.json'))),12)
            self.assertEqual(len(list((out/'topicos').glob('*/documento_tecnico.md'))),1)
            self.assertFalse((out/'questoes_qa.jsonl').exists())

    def test_falha_revisor_impede_documento_final(self):
        class Failing(FakeLLM):
            def json(self,system,user,**kwargs):
                if system==R.SYSTEM:raise RuntimeError('falha simulada de revisão')
                return super().json(system,user,**kwargs)
        with tempfile.TemporaryDirectory() as tmp,patch('pipeline.inventario.run_inventario.LLMClient',Failing), \
             contextlib.redirect_stdout(io.StringIO()):
            out=Path(tmp)/'out';manifest=fixture(Path(tmp))
            with self.assertRaises(RuntimeError):
                main(['--corpus-manifest',str(manifest),'--allow-sample-corpus','--topicos',TOPIC,
                      '--output',str(out),'--embedder','hash','--min-rerank','0'])
            self.assertTrue((out/'falha_revisao.json').exists())
            self.assertFalse((out/'documentos_topicos.json').exists())


if __name__=='__main__':unittest.main()
