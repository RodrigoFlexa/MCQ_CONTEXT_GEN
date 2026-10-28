"""Preservação, retomada, isolamento do prompt e dificuldade, sem API."""
import copy
import io
import tempfile
import unittest
from contextlib import redirect_stdout
from pathlib import Path
from unittest.mock import patch

from pipeline.qa_research.sem_conteudo import full as F
from pipeline.qa_research.sem_conteudo import core as C
from pipeline.qa_research.sem_conteudo.avaliacao_full import avaliar
from pipeline.qa_research.tests.test_sem_conteudo import Fake, question
from pipeline.qa_research.tests.test_especialista_finalizacao import Respondente, Juiz


class FullTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.root = Path(self.tmp.name)
        self.seed = self.root/'antiga/questoes.jsonl'
        self.rows = [{**question(), 'uid': f'01_01:sc:0001:{i}', 'rodada': 1,
                      'item': '01_01', 'origem': 'sem_conteudo', 'avaliacao_qualidade': 'nao_realizada'} for i in (1,2)]
        C.GeracaoSemConteudo.jsonl(self.seed, self.rows)
        self.metas = self.root/'metas.json'
        C.atomic_json(self.metas,dict(schema='metas-sem-conteudo-v1',run_referencia='Full',total=5,
            full_sha256='contagens_sem_textos_full',semente_sha256=C.sha(self.rows),semente_total=2,semente_por_item={'01_01':2},
            itens=[dict(id='01_01',topico='Gestão',subtopico='Desempenho',frase_especialista='Avaliar desempenho.',meta=5)]))
        self.out = self.root/'nova'

    def runner(self,fake=None,**kw):
        return F.GeracaoFull(self.out,metas=self.metas,semente=self.seed,
            clientes={'geracao':fake or Fake()},progress=lambda *a,**k:None,**kw)

    def clients(self,nano=None,gpt=None,judge=None):
        return {'resp_gpt-5-4-nano':nano or Respondente(),'resp_gpt-5-4':gpt or Respondente(),'juiz':judge or Juiz()}

    def evaluate(self,clients,**kw):
        return avaliar(self.out,clientes=clients,progress=lambda *a,**k:None,**kw)

    def test_metas_reais_4111_e_1293_novas_por_topico(self):
        g = F.GeracaoFull(self.out)
        self.assertEqual(len(g.semente),2818)
        self.assertEqual(sum(i['meta'] for i in g.itens),4111)
        self.assertEqual(len(g.itens),40)
        self.assertEqual(sum(i['meta']-len(g.por_item[i['id']]) for i in g.itens),1293)
        self.assertTrue(all(i['meta']>=len(g.por_item[i['id']]) for i in g.itens))
        for i in g.itens:
            self.assertEqual(set(i),{'id','topico','subtopico','frase_especialista','meta'})
        from collections import Counter
        root=C.ROOT/'pipeline/qa_research/relatorios'
        full=F.linhas(root/'geracao_final_20261024T204734Z/aprovadas.jsonl')+F.linhas(root/'especialista_revisadas_v3/aprovadas.jsonl')
        full += [q for q in F.linhas(root/'especialista_qa_v2/aprovadas.jsonl') if q['conjunto_especialista']=='autoral_especialista']
        self.assertEqual(C.sha(full),g.manifesto['full_sha256'])
        self.assertEqual(dict(Counter(q['item'] for q in full)),{i['id']:i['meta'] for i in g.itens})

    def test_preserva_semente_e_duplicatas_com_novos_ids(self):
        before = self.seed.read_bytes()
        f = Fake()
        self.assertEqual(self.runner(f).run(),0)
        qs = F.linhas(self.out/'questoes.jsonl')
        self.assertEqual(qs[:2],self.rows)
        self.assertEqual(len(qs),5)
        self.assertEqual(len({q['uid'] for q in qs}),5)
        self.assertEqual(len({q['pergunta'] for q in qs}),1)
        self.assertTrue(all('aprovada' not in q for q in qs))
        self.assertEqual(self.seed.read_bytes(),before)
        self.assertFalse((self.out/'aprovadas.jsonl').exists())
        self.assertEqual(C.read_json(self.out/'resultado.json')['novas'],3)
        self.assertEqual(f.requests[0]['recentes'],[{k:q[k] for k in ('pergunta','resposta')} for q in self.rows])
        self.assertEqual(set(f.requests[0]),{'escopo','lote','quantidade','recentes'})
        self.assertEqual(self.runner(f).run(),0)
        self.assertEqual(f.network,1)

    def test_interrupcao_retoma_sem_regerar_semente(self):
        f = Fake(fail_at=2)
        self.assertEqual(self.runner(f,lote=1).run(),2)
        self.assertEqual(len(F.linhas(self.out/'questoes.jsonl')),3)
        self.assertFalse((self.out/'geracao_concluida.json').exists())
        self.assertEqual(self.runner(f,lote=1).run(),0)
        self.assertEqual(F.linhas(self.out/'questoes.jsonl')[:2],self.rows)
        self.assertEqual(f.network,3)

    def test_limite_e_incompletude_nao_disparam_avaliacao(self):
        self.assertEqual(self.runner(lote=1,max_lotes=1).run(),2)
        with self.assertRaisesRegex(ValueError,'Conclua'):
            self.evaluate(self.clients())
        self.assertFalse((self.out/'avaliacao').exists())
        self.assertEqual(self.runner(lote=1,max_lotes=5).run(),0)

    def test_mudanca_de_semente_meta_prompt_e_checkpoint_bloqueia(self):
        self.runner().run()
        with self.assertRaisesRegex(ValueError,'Configuração'):
            self.runner(memoria=1).run()
        g = self.runner()
        g.prompt+='\nMudança'
        with self.assertRaisesRegex(ValueError,'Configuração'):g.run()
        path=self.out/'topicos/01_01/estado.json'
        s=C.read_json(path);s['questoes'][0]['pergunta']='alterada';C.atomic_json(path,s)
        with self.assertRaisesRegex(ValueError,'Checkpoint'):self.runner().run()
        altered=copy.deepcopy(self.rows);altered[0]['resposta']='alterada'
        C.GeracaoSemConteudo.jsonl(self.seed,altered)
        with self.assertRaisesRegex(ValueError,'Semente mudou'):self.runner()

    def test_plano_sem_saida_e_sem_api(self):
        with patch.object(C.GeracaoSemConteudo,'cliente',side_effect=AssertionError('Sem API')),redirect_stdout(io.StringIO()):
            self.assertEqual(F.main(['--saida',str(self.out),'--metas',str(self.metas),'--semente',str(self.seed),'--plano']),0)
        self.assertFalse(self.out.exists())
        with self.assertRaisesRegex(ValueError,'saída nova'):
            F.GeracaoFull(self.seed.parent,metas=self.metas,semente=self.seed)

    def test_avalia_todas_sem_fingir_aprovacao_e_retoma(self):
        self.runner().run()
        n,g,j=Respondente(),Respondente(),Juiz()
        self.assertEqual(self.evaluate(self.clients(n,g,j)),0)
        self.assertEqual((n.calls,g.calls),(5,5))
        rows=F.linhas(self.out/'avaliacao/avaliacoes.jsonl')
        self.assertEqual(len(rows),5)
        self.assertEqual({r['uid'] for r in rows},{q['uid'] for q in F.linhas(self.out/'questoes.jsonl')})
        self.assertTrue(all('conjunto_especialista' not in r for r in rows))
        self.assertFalse((self.out/'aprovadas.jsonl').exists())
        before=j.calls
        self.assertEqual(self.evaluate(self.clients(n,g,j)),0)
        self.assertEqual((n.calls,g.calls,j.calls),(5,5,before))
        self.assertEqual(C.read_json(self.out/'avaliacao/avaliacao_concluida.json')['questoes'],5)

    def test_bloqueio_terminal_sem_nota_sem_tentar_novamente(self):
        self.runner().run()
        n,g,j=Respondente(blocked=True),Respondente(),Juiz()
        self.assertEqual(self.evaluate(self.clients(n,g,j)),0)
        d=C.read_json(self.out/'avaliacao/acuracia.json')['geral']
        self.assertEqual((d['gpt-5-4-nano']['n'],d['gpt-5-4-nano']['nao_avaliadas']),(0,5))
        self.assertIsNone(d['gpt-5-4-nano']['acuracia'])
        self.assertEqual(self.evaluate(self.clients(n,g,j)),0)
        self.assertEqual(n.calls,5)

    def test_juiz_bloqueado_nao_divide_ou_reenvia(self):
        self.runner().run()
        j=Juiz(blocked=True)
        self.assertEqual(self.evaluate(self.clients(judge=j)),0)
        self.assertEqual(j.calls,2)
        self.assertEqual(self.evaluate(self.clients(judge=j)),0)
        self.assertEqual(j.calls,2)
        self.assertEqual(C.read_json(self.out/'avaliacao/avaliacao_concluida.json')['status'],'concluida_com_bloqueios')

    def test_falha_transitoria_modelo_nao_vira_conclusao(self):
        self.runner().run()
        self.assertEqual(self.evaluate(self.clients(nano=Respondente(error=True))),2)
        self.assertFalse((self.out/'avaliacao/avaliacao_concluida.json').exists())
        self.assertEqual(self.evaluate(self.clients()),0)

    def test_avaliacao_recusa_alteracao_de_banco_ou_protocolo(self):
        self.runner().run()
        self.assertEqual(self.evaluate(self.clients()),0)
        with self.assertRaisesRegex(ValueError,'protocolo'):
            self.evaluate(self.clients(),lote_juiz=4)
        rows=F.linhas(self.out/'questoes.jsonl');rows[-1]['resposta']='alterada'
        C.GeracaoSemConteudo.jsonl(self.out/'questoes.jsonl',rows)
        with self.assertRaisesRegex(ValueError,'alterados'):
            self.evaluate(self.clients())

    def test_modelo_indisponivel_na_sondagem_nao_e_excluido(self):
        class Indisponivel:
            def json(self,*a,**kw):raise RuntimeError('deployment indisponível')
        self.runner().run()
        self.assertEqual(self.evaluate(self.clients(nano=Indisponivel())),2)
        self.assertFalse((self.out/'avaliacao/avaliacao_concluida.json').exists())
        self.assertEqual(self.evaluate(self.clients()),0)


if __name__=='__main__':unittest.main()
