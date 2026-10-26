"""Testes offline: isolamento das entradas, metas finais, retomada e falhas."""
import copy
import io
import json
import tempfile
import unittest
from contextlib import redirect_stdout
from pathlib import Path
from unittest.mock import patch

from pipeline.qa_research.sem_conteudo import core as M
from pipeline.qa_research.sem_conteudo.__main__ import main

QA = [
    ('Como a corrosão reduz a resistência do casco?', 'Pela perda de espessura resistente do aço.'),
    ('Como o gás natural libera energia na turbina?', 'Pela combustão, que fornece energia térmica ao ciclo.'),
    ('Como a lubrificação reduz desgaste no rolamento?', 'Pelo filme que separa as superfícies em movimento relativo.'),
    ('Como a filtragem retém partículas sólidas suspensas?', 'Pela passagem do fluido pelo meio poroso, que retém partículas.'),
    ('Como o campo elétrico aproxima gotículas na emulsão?', 'Pela polarização das gotas, favorecendo sua atração e coalescência.'),
    ('Como a refrigeração remove calor do compressor?', 'Pela transferência de calor do fluido quente para o meio frio.'),
    ('Como a ventilação diminui a concentração de contaminantes?', 'Pela renovação do ar, que dilui e remove contaminantes.'),
    ('Como o isolamento térmico reduz a troca de calor?', 'Pela resistência adicional à transferência térmica entre os meios.'),
]


def question(i):
    p,r=QA[i%len(QA)]
    return dict(tipo='mecanismo',cenario=False,composicao='simples',pergunta=p,resposta=r)


class Fake:
    def __init__(self,batches=None,deny=None,dedup=False,fail=None):
        self.batches=copy.deepcopy(batches)
        self.deny=deny or (lambda uid:False)
        self.dedup=dedup
        self.fail=fail
        self.requests=[]
        self.cache={}
        self.network=0
        self.index=0
        self.dedup_count=0

    def json(self,system,user,tag='',validate=None,**kw):
        role=tag.removeprefix('sem_conteudo_')
        payload=json.loads(user)
        self.requests.append((role,system,payload))
        key=(system,user)
        if key in self.cache:
            result=copy.deepcopy(self.cache[key])
        else:
            if self.fail==role:
                self.fail=None
                raise RuntimeError('falha simulada')
            self.network+=1
            if role=='geracao':
                n=payload['quantidade']
                qs=self.batches.pop(0) if self.batches is not None else [question(self.index+i) for i in range(n)]
                self.index+=n
                result={'status':'ok' if len(qs)==n else 'parcial' if qs else 'sem_questoes',
                        'motivo':'' if len(qs)==n else 'Sem alvos adicionais confiáveis.','questoes':qs}
            elif role=='auditoria':
                result={'avaliacoes':[dict(id=q['id'],aprovada=not self.deny(q['id']),
                    tipo_sugerido=q['tipo'],motivo='resposta_vaga' if self.deny(q['id']) else 'nenhum',
                    justificativa='Revisão paramétrica simulada.') for q in payload['questoes']]}
            elif role=='refinador':
                result={'status':'ok','motivo':'Correção do alvo técnico.','questao':question(5 if payload['tentativa']==1 else 6)}
            else:
                self.dedup_count+=1
                qs=payload['questoes']
                result={'grupos':[{'manter':qs[0]['id'],'remover':[qs[-1]['id']],'motivo':'Mesmo alvo.'}]
                        if self.dedup and self.dedup_count==1 else []}
            self.cache[key]=copy.deepcopy(result)
        if validate:
            validate(result)
        return result


class TestSemConteudo(unittest.TestCase):
    def setUp(self):
        self.tmp=tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.root=Path(self.tmp.name)
        self.metas=self.root/'metas.json'
        self.out=self.root/'run'
        self.set_metas(3)

    def set_metas(self,n,second=False):
        items=[dict(id='01_01',topico='Gestão',subtopico='Desempenho',
                    frase_especialista='Avaliar os sistemas de um FPSO.',meta=n)]
        if second:
            items.append({**items[0],'id':'02_01','subtopico':'Medição','meta':2})
        M.atomic_json(self.metas,dict(schema='metas-sem-conteudo-v1',run_referencia='run_antiga',
                                    total=n+(2 if second else 0),itens=items))

    def runner(self,fake=None,**kw):
        fake=fake or Fake()
        return M.GeracaoSemConteudo(self.out,metas=self.metas,clientes=dict.fromkeys(M.MODELOS,fake),
                                   progress=lambda *a,**k:None,**kw)

    def test_metas_oficiais_e_programa(self):
        from pipeline.fase_3.topicos import TOPICOS
        d=M.carregar_metas()
        self.assertEqual(d['total'],2818)
        self.assertEqual(len(d['itens']),40)
        self.assertEqual(d['itens'][0]['meta'],62)
        for i in d['itens']:
            self.assertEqual(i['frase_especialista'],TOPICOS[i['topico']][i['subtopico']])
        raw=(M.ROOT/'pipeline/qa_research/relatorios'/d['run_referencia']/'aprovadas.jsonl').read_bytes().replace(b'\r\n',b'\n')
        self.assertEqual(__import__('hashlib').sha256(raw).hexdigest(),d['aprovadas_referencia_sha256'])
        counts=__import__('collections').Counter(json.loads(x)['item'] for x in raw.decode().splitlines() if x.strip())
        self.assertEqual({i['id']:i['meta'] for i in d['itens']},dict(counts))

    def test_quantidade_exata_e_compatibilidade_avaliador(self):
        self.assertEqual(self.runner(lote=2,refinos=0).run(),0)
        result=M.read_json(self.out/'resultado.json')
        self.assertEqual(result['aprovadas'],3)
        self.assertEqual(result['tentativas_de_questao'],3)
        from pipeline.qa_research.geracao_tipos.avaliacao import AvaliacaoModelos
        e=AvaliacaoModelos(self.out,clientes={})
        self.assertEqual(len(e.carregar_questoes()),3)
        self.assertTrue((self.out/'topicos/01_01/finalizado.json').exists())

    def test_memoria_limitada_e_sem_leitura_da_run_antiga(self):
        f=Fake()
        original=Path.read_text
        def guarded(path,*args,**kw):
            if path.name in ('aprovadas.jsonl','exemplos.json','banco_dinamico.json') or path.suffix=='.md' and 'prompts' not in str(path):
                raise AssertionError('Leitura externa proibida: '+str(path))
            return original(path,*args,**kw)
        with patch.object(Path,'read_text',guarded):
            self.assertEqual(self.runner(f,lote=1,memoria=1,refinos=0).run(),0)
        generations=[p for r,s,p in f.requests if r=='geracao']
        self.assertEqual(generations[0]['recentes'],[])
        self.assertEqual(len(generations[1]['recentes']),1)
        self.assertEqual(generations[2]['recentes'][0]['pergunta'],QA[1][0])
        for role,system,payload in f.requests:
            self.assertEqual(set(payload['escopo']),{'topico','subtopico','frase_especialista'})
            self.assertNotIn('frase_especialista',' '.join(payload.keys()))
            self.assertNotIn('exemplos',payload)
            self.assertNotIn('documento',payload)

    def test_dedup_remove_e_completa_meta(self):
        f=Fake(dedup=True)
        self.assertEqual(self.runner(f,lote=3,refinos=0).run(),0)
        d=M.read_json(self.out/'resultado.json')
        self.assertEqual(d['aprovadas'],3)
        self.assertEqual(d['tentativas_de_questao'],4)
        s=M.read_json(self.out/'topicos/01_01/estado.json')
        self.assertEqual(sum(q.get('redundante',False) for q in s['questoes']),1)

    def test_duplicata_lexical_nao_conta(self):
        self.set_metas(2)
        f=Fake(batches=[[question(0),question(0)],[question(1)]])
        self.assertEqual(self.runner(f,lote=2,refinos=0).run(),0)
        d=M.read_json(self.out/'resultado.json')
        self.assertEqual(d['aprovadas'],2)
        self.assertEqual(d['tentativas_de_questao'],3)

    def test_refino_duas_tentativas_sem_fontes(self):
        self.set_metas(1)
        f=Fake(deny=lambda uid:not uid.endswith(':ref2'))
        self.assertEqual(self.runner(f,lote=1).run(),0)
        s=M.read_json(self.out/'topicos/01_01/estado.json')
        self.assertEqual(len(s['questoes']),3)
        self.assertTrue(s['aprovadas'][0]['uid'].endswith(':ref2'))
        self.assertEqual(s['aprovadas'][0]['origem'],'refinada')

    def test_limite_parcial_nao_e_sucesso_e_retoma(self):
        f=Fake()
        self.assertEqual(self.runner(f,lote=1,refinos=0,max_lotes=1).run(),2)
        self.assertFalse((self.out/'geracao_concluida.json').exists())
        self.assertFalse((self.out/'topicos/01_01/finalizado.json').exists())
        self.assertEqual(self.runner(f,lote=1,refinos=0,max_lotes=5).run(),0)
        before=f.network
        self.assertEqual(self.runner(f,lote=1,refinos=0,max_lotes=5).run(),0)
        self.assertEqual(f.network,before)

    def test_falha_auditoria_replay_sem_perda_ou_duplicacao(self):
        f=Fake(fail='auditoria')
        self.assertEqual(self.runner(f,lote=3,refinos=0).run(),2)
        s=M.read_json(self.out/'topicos/01_01/estado.json')
        self.assertEqual(s['lotes'],0)
        self.assertEqual(s['aprovadas'],[])
        self.assertEqual(self.runner(f,lote=3,refinos=0).run(),0)
        self.assertEqual(f.network,3)  # geração, auditoria bem sucedida e dedup; geração veio do cache
        self.assertEqual(M.read_json(self.out/'resultado.json')['aprovadas'],3)

    def test_falha_dedup_retoma_sem_gerar_novamente(self):
        f=Fake(fail='dedup')
        self.assertEqual(self.runner(f,lote=3,refinos=0).run(),2)
        self.assertEqual(self.runner(f,lote=3,refinos=0).run(),0)
        self.assertEqual(sum(role=='geracao' for role,_,_ in f.requests),1)

    def test_configuracao_incompativel_bloqueia_retomada(self):
        self.runner(refinos=0).run()
        with self.assertRaisesRegex(ValueError,'Configuração mudou'):
            self.runner(refinos=0,memoria=1).run()

    def test_topicos_paralelos_e_retomada_selecao(self):
        self.set_metas(3,second=True)
        self.assertEqual(self.runner(lote=2,refinos=0,workers=2).run(),0)
        self.assertEqual(M.read_json(self.out/'resultado.json')['aprovadas'],5)
        other=self.root/'other'
        g=M.GeracaoSemConteudo(other,metas=self.metas,itens=['02_01'],refinos=0,
                              clientes=dict.fromkeys(M.MODELOS,Fake()),progress=lambda *a,**k:None)
        self.assertEqual(g.run(),0)
        resumed=M.GeracaoSemConteudo(other,metas=self.metas,refinos=0,clientes=dict.fromkeys(M.MODELOS,Fake()))
        self.assertEqual([i['id'] for i in resumed.itens],['02_01'])

    def test_plano_nao_cria_saida_nem_cliente(self):
        with patch.object(M.GeracaoSemConteudo,'cliente',side_effect=AssertionError('Não chamar API')),redirect_stdout(io.StringIO()):
            self.assertEqual(main(['--saida',str(self.out),'--metas',str(self.metas),'--plano']),0)
        self.assertFalse(self.out.exists())

    def test_validadores_rejeitam_ids_e_aprovacoes_inconsistentes(self):
        for groups in [[dict(manter='A',remover=['A'],motivo='erro')],
                       [dict(manter='A',remover=['X'],motivo='erro')],
                       [dict(manter='A',remover=['B'],motivo='erro'),dict(manter='B',remover=['C'],motivo='erro')]]:
            with self.assertRaises(ValueError):
                M.validar_dedup({'grupos':groups},['A','B','C'])
        with self.assertRaises(ValueError):
            M.validar_auditoria({'avaliacoes':[dict(id='A',aprovada=True,tipo_sugerido='conceito',
                motivo='trivial',justificativa='Inválida.')]},['A'])
        with self.assertRaises(ValueError):
            M.validar_geracao(dict(status='ok',motivo='',questoes=[question(0)]),2)


if __name__=='__main__':
    unittest.main()
