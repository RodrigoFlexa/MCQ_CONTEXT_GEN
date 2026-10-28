"""Seleção fixa e avaliação retomável, sem geração ou API real."""
import copy
import io
import tempfile
import unittest
from contextlib import redirect_stdout
from pathlib import Path
from unittest.mock import patch

from pipeline.qa_research.sem_conteudo import amostra as A
from pipeline.qa_research.sem_conteudo import core as C
from pipeline.qa_research.tests.test_sem_conteudo import question
from pipeline.qa_research.tests.test_especialista_finalizacao import Respondente, Juiz


class AmostraTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.root = Path(self.tmp.name)
        self.source = self.root/'fonte/questoes.jsonl'
        self.rows = [{**question(),'uid':f'01_01:sc:0001:{i}','item':'01_01','rodada':1,
                      'origem':'sem_conteudo','avaliacao_qualidade':'nao_realizada'} for i in range(1,6)]
        C.GeracaoSemConteudo.jsonl(self.source,self.rows)
        self.selected = [self.rows[i] for i in (3,0,4)]
        self.manifest = self.root/'amostra.json'
        C.atomic_json(self.manifest,dict(schema='amostra-sem-conteudo-v1',n=3,fonte_n=5,
            fonte_sha256=C.sha(self.rows),amostra_sha256=C.sha(self.selected),
            semente=20261028,repeticao=1,uids=[q['uid'] for q in self.selected]))
        self.out = self.root/'saida'

    def clients(self,nano=None,gpt=None,judge=None):
        return {'resp_gpt-5-4-nano':nano or Respondente(),'resp_gpt-5-4':gpt or Respondente(),'juiz':judge or Juiz()}

    def evaluate(self,clients=None,**kw):
        return A.avaliar(self.out,manifesto=self.manifest,fonte=self.source,
            clientes=clients or self.clients(),progress=lambda *a,**k:None,**kw)

    def test_manifesto_real_fixa_1000_do_primeiro_sorteio(self):
        data,rows=A.carregar()
        self.assertEqual((data['n'],data['fonte_n'],data['semente'],data['repeticao']),(1000,2818,20261028,1))
        self.assertEqual(len(rows),1000)
        self.assertEqual(len({q['uid'] for q in rows}),1000)
        self.assertEqual(C.sha(dict(ablacao='Sem contexto',repeticao=1,uids=data['uids'])),data['origem_ids_sha256'])
        # Conferência adicional local com os IDs efetivamente usados nos gráficos.
        path=C.ROOT/'docs/ablacoes_amostras_1000_20261028/amostras.jsonl'
        if path.exists():
            import json
            first=json.loads(path.read_text(encoding='utf-8').splitlines()[0])
            self.assertEqual(first['uids'],data['uids'])

    def test_plano_nao_cria_saida_nem_chama_api(self):
        with patch.object(A,'avaliar',side_effect=AssertionError('Sem API')),redirect_stdout(io.StringIO()):
            self.assertEqual(A.main(['--manifesto',str(self.manifest),'--fonte',str(self.source),'--saida',str(self.out),'--plano']),0)
        self.assertFalse(self.out.exists())

    def test_avalia_so_selecionadas_sem_geracao_e_sem_filtrar(self):
        before=self.source.read_bytes()
        n,g,j=Respondente(),Respondente(),Juiz()
        with patch.object(C.GeracaoSemConteudo,'cliente',side_effect=AssertionError('Não gerar questões')):
            self.assertEqual(self.evaluate(self.clients(n,g,j)),0)
        self.assertEqual((n.calls,g.calls),(3,3))
        self.assertEqual(A.linhas(self.out/'questoes.jsonl'),self.selected)
        self.assertEqual(self.source.read_bytes(),before)
        self.assertFalse((self.out/'aprovadas.jsonl').exists())
        self.assertFalse((self.out/'geracao_concluida.json').exists())
        rows=A.linhas(self.out/'avaliacao/avaliacoes.jsonl')
        self.assertEqual({q['uid'] for q in rows},{q['uid'] for q in self.selected})
        self.assertTrue(all('conjunto_especialista' not in q for q in rows))

    def test_retomada_nao_repete_respostas_ou_juiz(self):
        n,g,j=Respondente(),Respondente(),Juiz()
        cl=self.clients(n,g,j)
        self.assertEqual(self.evaluate(cl),0)
        calls=(n.calls,g.calls,j.calls)
        self.assertEqual(self.evaluate(cl,workers=3),0)
        self.assertEqual((n.calls,g.calls,j.calls),calls)

    def test_fonte_alterada_duplicada_ou_selecao_invalida_bloqueia_antes_de_api(self):
        altered=copy.deepcopy(self.rows);altered[0]['pergunta']='alterada'
        C.GeracaoSemConteudo.jsonl(self.source,altered)
        with self.assertRaisesRegex(ValueError,'Fonte mudou'):self.evaluate()
        self.assertFalse(self.out.exists())
        C.GeracaoSemConteudo.jsonl(self.source,self.rows)
        data=C.read_json(self.manifest);data['uids'][1]=data['uids'][0]
        C.atomic_json(self.manifest,data)
        with self.assertRaisesRegex(ValueError,'IDs'):self.evaluate()

    def test_bloqueia_alteracao_da_selecao_salva_ou_protocolo(self):
        self.evaluate()
        with self.assertRaisesRegex(ValueError,'protocolo'):self.evaluate(lote_juiz=2)
        selected=copy.deepcopy(self.selected);selected[0]['resposta']='alterada'
        C.GeracaoSemConteudo.jsonl(self.out/'questoes.jsonl',selected)
        with self.assertRaisesRegex(ValueError,'salvas foram alteradas'):self.evaluate()

    def test_nao_sobrescreve_fonte_nem_adota_avaliacao_desconhecida(self):
        with self.assertRaisesRegex(ValueError,'fora da run'):
            A.avaliar(self.source.parent,manifesto=self.manifest,fonte=self.source,clientes=self.clients())
        (self.out/'avaliacao').mkdir(parents=True)
        with self.assertRaisesRegex(ValueError,'sem protocolo'):self.evaluate()

    def test_filtro_respondente_terminal_sem_nota_e_sem_reenvio(self):
        n,g,j=Respondente(blocked=True),Respondente(),Juiz()
        cl=self.clients(n,g,j)
        self.assertEqual(self.evaluate(cl),0)
        d=C.read_json(self.out/'avaliacao/acuracia.json')['geral']['gpt-5-4-nano']
        self.assertEqual((d['total'],d['n'],d['nao_avaliadas']),(3,0,3))
        self.assertIsNone(d['acuracia'])
        self.assertEqual(self.evaluate(cl),0)
        self.assertEqual(n.calls,3)

    def test_juiz_bloqueado_nao_divide_lotes(self):
        j=Juiz(blocked=True);cl=self.clients(judge=j)
        self.assertEqual(self.evaluate(cl),0)
        self.assertEqual(j.calls,2)
        self.assertEqual(self.evaluate(cl),0)
        self.assertEqual(j.calls,2)
        self.assertEqual(C.read_json(self.out/'avaliacao/avaliacao_concluida.json')['status'],'concluida_com_bloqueios')

    def test_falha_api_retoma_somente_pendentes(self):
        g,j=Respondente(),Juiz()
        self.assertEqual(self.evaluate(self.clients(nano=Respondente(error=True),gpt=g,judge=j)),2)
        self.assertFalse((self.out/'avaliacao/avaliacao_concluida.json').exists())
        n=Respondente()
        self.assertEqual(self.evaluate(self.clients(n,g,j)),0)
        self.assertEqual((n.calls,g.calls),(3,3))

    def test_modelo_obrigatorio_indisponivel_nao_e_removido_silenciosamente(self):
        class Indisponivel:
            def json(self,*a,**kw):raise RuntimeError('indisponível')
        self.assertEqual(self.evaluate(self.clients(nano=Indisponivel())),2)
        self.assertFalse((self.out/'avaliacao/avaliacao_concluida.json').exists())
        self.assertEqual(self.evaluate(),0)


if __name__=='__main__':unittest.main()
