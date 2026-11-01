"""Gap pareado e evidências de sustentação; só clientes simulados."""
import copy
import csv
import io
import json
import tempfile
import unittest
from contextlib import redirect_stdout
from pathlib import Path
from unittest.mock import patch

from pipeline.qa_research import benchmark_gap as G
from pipeline.qa_research.tests.test_especialista_finalizacao import Respondente,Juiz


class Answer(Respondente):
    def __init__(self,**kw):super().__init__(**kw);self.payloads=[]
    def json(self,system,user,**kw):
        self.payloads.append(json.loads(user))
        return super().json(system,user,**kw)


class Faith:
    def __init__(self,blocked=False,transient=False):self.calls=0;self.blocked=blocked;self.transient=transient
    def json(self,system,user,validate=None,**kw):
        self.calls+=1
        if self.blocked:
            from pipeline.inventario.llm import ContentFiltered
            raise ContentFiltered('bloqueio simulado')
        if self.transient:raise RuntimeError('falha temporária')
        data=json.loads(user);b=data['blocos'][0]
        d=dict(cobertura_completa=True,afirmacoes=[dict(afirmacao=data['gabarito'],veredito='sustentada',
            evidencias=[dict(bloco=b['id'],trecho=b['texto'])],justificativa='Evidência do bloco.')],observacoes='')
        if validate:validate(d)
        return d


class GapTests(unittest.TestCase):
    def setUp(self):
        tmp=tempfile.TemporaryDirectory();self.addCleanup(tmp.cleanup)
        self.root=Path(tmp.name);self.source=self.root/'fonte'/'aprovadas.jsonl';self.docs=self.root/'documentos';self.out=self.root/'saida'
        self.original=[]
        for item in ('01_01','02_02'):
            G.atomic_json(self.docs/item/'documento.json',dict(titulo='Documento '+item,capitulos=[dict(titulo='Capítulo',blocos=[
                dict(subtitulo='Parte '+str(i),texto=f'Texto técnico do bloco {i}, relativo a {item}.') for i in range(4)])]))
            for i in range(2):
                self.original.append(dict(uid=item+':qa:'+str(i),item=item,tipo='mecanismo',cenario=False,
                    origem='janela' if i==0 else 'refinada',original=None if i==0 else 'origem_mcq_nao_utilizada',
                    composicao='simples' if i==0 else 'composta',foco=1 if i==0 else None,
                    blocos=None if i==0 else [0,3],pergunta=f'Pergunta {item} {i}?',resposta='SEGREDO_GABARITO',aprovada=True))
        G.Q.C.GeracaoSemConteudo.jsonl(self.source,self.original)
        self.a,self.b,self.c,self.j,self.f=Answer(),Answer(),Answer(),Juiz(),Faith()
        self.logs=[]

    def run_gap(self):
        return G.executar(self.out,source=self.source,docs=self.docs,workers=3,judge_workers=1,
            clientes={'resp_gpt-4-1-nano':self.a,'resp_gpt-4-1-mini':self.b,'resp_gpt-4-1':self.c,
                'juiz':self.j,'faithfulness':self.f},progress=lambda s,**kw:self.logs.append(s))

    def test_pares_completos_contexto_sem_gabarito_e_tres_modelos(self):
        self.assertEqual(self.run_gap(),0)
        self.assertEqual((self.a.calls,self.b.calls,self.c.calls,self.f.calls),(8,8,8,4))
        for model in (self.a,self.b,self.c):
            payloads=model.payloads[1:] # exclui sondagem
            self.assertEqual(sum(p['contexto'] is None for p in payloads),4)
            self.assertEqual(sum(p['contexto'] is not None for p in payloads),4)
            self.assertTrue(all(set(p)=={'pergunta','contexto'} for p in payloads))
            self.assertTrue(all('SEGREDO_GABARITO' not in json.dumps(p) for p in payloads))
        with (self.out/'gap_pareado.csv').open(encoding='utf-8-sig') as f:results=list(csv.DictReader(f))
        self.assertEqual(len(results),3)
        self.assertTrue(all(r['pares_com_nota']=='4' and float(r['gap_pp'])==0 for r in results))
        summary=G.read_json(self.out/'faithfulness_resumo.json')
        self.assertEqual((summary['com_decisao'],summary['totalmente_sustentadas']),(4,4))
        self.assertTrue((self.out/'rodada_concluida.json').exists())
        self.assertTrue(any('[AO VIVO | open_book' in s for s in self.logs))

    def test_retomada_nao_repete_chamadas_de_casos_concluidos(self):
        self.assertEqual(self.run_gap(),0)
        before=(self.a.calls,self.b.calls,self.c.calls,self.j.calls,self.f.calls)
        self.assertEqual(self.run_gap(),0)
        self.assertEqual((self.a.calls,self.b.calls,self.c.calls,self.j.calls,self.f.calls),before)

    def test_gap_pareado_e_bloqueio_em_apenas_um_braco(self):
        target=self.original[0]['pergunta']
        class Contrast(Answer):
            def json(self,system,user,tag='',**kw):
                d=super().json(system,user,tag=tag,**kw);p=json.loads(user)
                if tag.startswith('resposta_'):
                    d={'resposta':'acerto' if p['contexto'] else 'erro'}
                return d
        class BlockOne(Contrast):
            def json(self,system,user,tag='',**kw):
                p=json.loads(user)
                if tag.startswith('resposta_') and p['contexto'] and p['pergunta']==target:
                    from pipeline.inventario.llm import ContentFiltered
                    self.calls+=1;raise ContentFiltered('bloqueio simulado')
                return super().json(system,user,tag=tag,**kw)
        class Judge(Juiz):
            def json(self,system,user,validate=None,**kw):
                self.calls+=1;p=json.loads(user);self.payloads.append(p)
                assert len({q['pergunta'] for q in p})==len(p)
                d={'avaliacoes':[dict(id=q['id'],veredito='correta' if q['resposta_candidato']=='acerto' else 'incorreta',
                    justificativa='Julgamento simulado.') for q in p]}
                if validate:validate(d)
                return d
        self.a,self.b,self.c,self.j=BlockOne(),Contrast(),Contrast(),Judge()
        self.assertEqual(self.run_gap(),0)
        with (self.out/'gap_pareado.csv').open(encoding='utf-8-sig') as f:results=list(csv.DictReader(f))
        for r in results:
            n=3 if r['modelo']=='gpt-4-1-nano' else 4
            self.assertEqual(int(r['pares_com_nota']),n)
            self.assertEqual((float(r['acuracia_closed']),float(r['acuracia_open']),float(r['gap_pp'])),(0,100,100))
            self.assertEqual((int(r['ganhos']),int(r['perdas'])),(n,0))

    def test_bloqueios_sem_nota_e_terminais(self):
        self.a=Answer(blocked=True);self.f=Faith(blocked=True)
        self.assertEqual(self.run_gap(),0)
        fs=G.read_json(self.out/'faithfulness_resumo.json')
        self.assertEqual((fs['bloqueadas'],fs['com_decisao']),(4,0))
        self.assertIsNone(fs['taxa_totalmente_sustentadas'])
        before=(self.a.calls,self.f.calls,self.j.calls)
        self.assertEqual(self.run_gap(),0)
        self.assertEqual((self.a.calls,self.f.calls,self.j.calls),before)

    def test_falha_transitoria_faithfulness_retoma_sem_refazer_qa(self):
        self.f=Faith(transient=True)
        self.assertEqual(self.run_gap(),2)
        self.assertFalse((self.out/'rodada_concluida.json').exists())
        before=(self.a.calls,self.j.calls);self.f=Faith()
        self.assertEqual(self.run_gap(),0)
        self.assertEqual((self.a.calls,self.j.calls),before)
        self.assertEqual(self.f.calls,4)

    def test_mini_indisponivel_nao_e_removido_nem_substituido(self):
        class Missing:
            def json(self,*a,**kw):raise RuntimeError('deployment não existe')
        self.b=Missing()
        self.assertEqual(self.run_gap(),2)
        self.assertEqual((self.a.calls,self.c.calls,self.f.calls),(0,0,0))
        self.assertFalse((self.out/'rodada_concluida.json').exists())
        self.b=Answer();self.assertEqual(self.run_gap(),0)
        self.assertFalse((self.out/'falha_execucao.json').exists())

    def test_dados_ou_protocolos_alterados_nao_sao_misturados(self):
        self.assertEqual(self.run_gap(),0)
        self.original[0]['pergunta']='Pergunta alterada?'
        G.Q.C.GeracaoSemConteudo.jsonl(self.source,self.original)
        with self.assertRaisesRegex(ValueError,'mudaram'):self.run_gap()

    def test_validacao_evidencia_literal_e_cobertura_nao_inventa_faithfulness(self):
        blocks={'B1':'Uma frase técnica.'}
        d=dict(cobertura_completa=True,afirmacoes=[dict(afirmacao='Uma afirmação.',veredito='sustentada',
            evidencias=[dict(bloco='B1',trecho='Uma frase técnica.')],justificativa='Explicação.')],observacoes='')
        G.validar_faithfulness(d,blocks)
        bad=copy.deepcopy(d);bad['afirmacoes'][0]['evidencias'][0]['trecho']='Trecho inventado.'
        with self.assertRaisesRegex(ValueError,'literal'):G.validar_faithfulness(bad,blocks)
        bad=copy.deepcopy(d);bad['afirmacoes'][0]['evidencias']=[]
        with self.assertRaisesRegex(ValueError,'evidência'):G.validar_faithfulness(bad,blocks)
        d['cobertura_completa']=False
        self.assertEqual(G.resumo_faithfulness(d)['status'],'inconclusivo')
        d['cobertura_completa']=True;d['afirmacoes'][0]['veredito']='insuficiente';d['afirmacoes'][0]['evidencias']=[]
        G.validar_faithfulness(d,blocks)
        self.assertEqual(G.resumo_faithfulness(d)['status'],'suporte_insuficiente')

    def test_contextos_reais_todos_2818_incluindo_refinadas(self):
        original,rows=G.carregar()
        self.assertEqual((len(original),len(rows)),(2818,5636))
        self.assertEqual(len({q['uid_original'] for q in rows}),2818)
        self.assertEqual(sum(q['origem']=='refinada' for q in original),1278)
        self.assertTrue(all(q['contexto_tecnico'] for q in original))
        with patch.object(G,'executar',side_effect=AssertionError('Sem API')),redirect_stdout(io.StringIO()):
            self.assertEqual(G.main(['--plano','--saida',str(self.out)]),0)
        self.assertFalse(self.out.exists())

    def test_csv_preserva_controles_aspas_e_compatibilidade_estrita(self):
        data=[dict(texto='Texto com \x00, "aspas"\n e \\barra\r fim')]
        path=self.root/'controles.csv';G.salvar_csv(path,data)
        with path.open(encoding='utf-8-sig',newline='') as f:
            self.assertEqual(list(csv.DictReader(f,escapechar='\\')),data)
        self.assertEqual(self.run_gap(),0)
        cfg=G.read_json(self.out/'config.json');cfg['codigo']=next(iter(G.CODIGOS_COMPATIVEIS))
        G.atomic_json(self.out/'config.json',cfg)
        before=(self.a.calls,self.b.calls,self.c.calls,self.j.calls,self.f.calls)
        self.assertEqual(self.run_gap(),0)
        self.assertEqual((self.a.calls,self.b.calls,self.c.calls,self.j.calls,self.f.calls),before)
        cfg['limite_palavras']=50;G.atomic_json(self.out/'config.json',cfg)
        with self.assertRaisesRegex(ValueError,'mudaram'):self.run_gap()


if __name__=='__main__':unittest.main()
