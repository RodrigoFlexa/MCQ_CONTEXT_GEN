"""Ablação pareada, reaproveitamento conferido e retomada, sem chamadas reais."""
import copy
import csv
import io
import threading
import unittest
from contextlib import redirect_stdout
from unittest.mock import patch

from pipeline.qa_research.qa_medium import exploratoria as X
from pipeline.qa_research.tests import test_qa_medium as F

Q=X.Q


class Resposta(F.Resposta):
    def json(self,system,user,**kw):
        self.ultimo_max_tokens=kw.get('max_tokens')
        return super().json(system,user,**kw)


class ExploratoriaTests(unittest.TestCase):
    def setUp(self):
        F.MediumTests.setUp(self)
        self.ref=self.root/'referencia100'

    def preparar(self,n=None,blocked=False):
        if n:
            for c in self.data['condicoes']:
                source=c['fontes'][0];p=F.Path(source['path']);q=Q.linhas(p)[0]
                rows=[{**q,'uid':f"{c['id']}:{i}",
                    'pergunta':f"Pergunta {c['id']} {i}"+(' última?' if i==n-1 else '?')} for i in range(n)]
                Q.C.GeracaoSemConteudo.jsonl(p,rows)
                source.update(n=n,sha256=Q.C.sha(rows))
                c.update(n=n,uids=[r['uid'] for r in rows],amostra_sha256=Q.C.sha(rows))
            Q.atomic_json(self.manifest,self.data)
        self.assertEqual(Q.avaliar(self.ref,manifesto=self.manifest,lote_juiz=8,
            clientes={'resp_gpt-5-4-nano':Resposta(blocked=blocked),
                'resp_gpt-5-4':Resposta(),'juiz':F.Julgamento()},progress=lambda *a,**k:None),0)

    def evaluate(self,n=None,g=None,j=None,**kw):
        return X.avaliar(self.out,manifesto=self.manifest,referencia=self.ref,
            workers=4,judge_workers=1,clientes={'resp_gpt-5-4-nano':n or Resposta(),
                'resp_gpt-5-4':g or Resposta(),'juiz':j or F.Julgamento()},
            progress=lambda s,**kw:self.logs.append(s),**kw)

    def csv(self,name):
        with (self.out/'avaliacao'/name).open(encoding='utf-8-sig',newline='') as f:
            return list(csv.DictReader(f))

    def test_prompts_controle_e_amostras_reais(self):
        self.assertEqual(X.prompt_resposta('p100'),Q.prompt('respondente'))
        self.assertEqual(X.prompt_resposta('p50'),Q.prompt('respondente').replace('100 palavras','50 palavras'))
        self.assertEqual(X.prompt_juiz(),Q.prompt('juiz'))
        self.assertIn('sem um limite numérico de palavras',X.prompt_resposta('concisa_livre'))
        data,original,rows=X.carregar()
        self.assertEqual((len(original),len(rows)),(2000,6000))
        self.assertEqual([c['n'] for c in data['condicoes']],[1000,1000])
        self.assertEqual(len({q['uid'] for q in rows}),6000)
        byid={q['uid']:q for q in original}
        for b in X.BRACOS:
            self.assertEqual([{k:q[k] for k in byid[q['uid_original']]}|{'uid':q['uid_original'],'condicao':q['conjunto']}
                for q in rows if q['braco']==b],original)

    def test_reaproveita_100_e_gera_so_dois_bracos_medium(self):
        self.preparar();n,g,j=Resposta(),Resposta(),F.Julgamento()
        before=Q.linhas(self.ref/'avaliacao/avaliacoes.jsonl')
        self.assertEqual(self.evaluate(n,g,j),0)
        self.assertEqual((n.calls,g.calls),(16,16))
        self.assertEqual(n.ultimo_max_tokens,8000)
        for req in n.requests+g.requests:
            if req['tag'].startswith('resposta_'):
                self.assertIn(req['system'],[X.prompt_resposta(b) for b in ('p50','concisa_livre')])
                self.assertTrue(req['user'].startswith('Pergunta '))
                self.assertNotIn('resposta_referencia',req['user'])
        self.assertTrue(all(s==X.prompt_juiz() for s in j.systems))
        for payload in j.payloads:
            self.assertTrue(all(set(q)=={'id','pergunta','resposta_referencia','resposta_candidato'} for q in payload))
        cfg=Q.read_json(self.out/'config.json')
        self.assertTrue(all(a.endswith(':medium') for a in cfg['respondentes'].values()))
        self.assertEqual(cfg['juiz'],Q.JUIZ)
        self.assertEqual(cfg['referencia_100']['respostas'],16)
        after=Q.linhas(self.out/'avaliacao/avaliacoes.jsonl')
        self.assertEqual(len(after),24)
        old={q['uid']:q for q in before}
        for q in after:
            if q['braco']=='p100':
                for m in Q.RESPONDENTES:
                    self.assertTrue(q['reaproveitada_'+m])
                    for key in ('resposta_','veredito_','status_avaliacao_'):
                        self.assertEqual(q[key+m],old[q['uid_original']][key+m])
                    self.assertEqual(q['justificativa_'+m],'Resposta confere.')
        for m in Q.RESPONDENTES:
            for p in (self.out/'avaliacao/juiz'/m).glob('*.json'):
                batch=Q.read_json(p)['avaliacoes']
                self.assertEqual(len({q['uid'].split(':')[0] for q in batch}),1)
        self.assertEqual(Q.linhas(self.ref/'avaliacao/avaliacoes.jsonl'),before)
        self.assertTrue(any('[AO VIVO | sem_contexto / p50' in s for s in self.logs))

    def test_retomada_nao_repete_respostas_nem_julgamentos(self):
        self.preparar();n,g,j=Resposta(),Resposta(),F.Julgamento()
        self.assertEqual(self.evaluate(n,g,j),0);calls=(n.calls,g.calls,j.calls)
        self.assertEqual(self.evaluate(n,g,j),0)
        self.assertEqual((n.calls,g.calls,j.calls),calls)

    def test_acuracia_e_juiz_trabalham_antes_das_ultimas_respostas(self):
        self.preparar(n=6)
        event=threading.Event();n,g,j=Resposta(event),Resposta(event),F.Julgamento(event)
        self.assertEqual(self.evaluate(n,g,j),0)
        self.assertTrue(event.is_set())
        self.assertTrue(any('[AO VIVO' in s and '/ p50' in s and 'acurácia 100.00%' in s for s in self.logs))

    def test_juiz_transitorio_retoma_so_notas_e_lotes_menores_que_oito(self):
        self.preparar(n=3);n,g=Resposta(),Resposta()
        class Falha:
            def json(self,*a,**kw):raise RuntimeError('falha temporária')
        self.assertEqual(self.evaluate(n,g,Falha()),2)
        self.assertFalse((self.out/'avaliacao/avaliacao_concluida.json').exists())
        j=F.Julgamento()
        self.assertEqual(self.evaluate(n,g,j),0)
        self.assertEqual((n.calls,g.calls,j.calls),(12,12,4))
        self.assertTrue(all(len(p)==6 for p in j.payloads))

    def test_bloqueios_reaproveitados_e_novos_sao_terminais_sem_nota(self):
        self.preparar(blocked=True);n,g,j=Resposta(blocked=True),Resposta(),F.Julgamento()
        self.assertEqual(self.evaluate(n,g,j),0)
        self.assertEqual(n.calls,16)
        summary=Q.read_json(self.out/'avaliacao/acuracia.json')
        for cond,models in summary['por_condicao'].items():
            self.assertEqual((models['gpt-5-4-nano']['n'],models['gpt-5-4-nano']['sem_nota']),(0,4))
        for r in self.csv('comparacao_mesmas_questoes.csv'):
            self.assertEqual(int(r['n_comum']),0 if r['modelo']=='gpt-5-4-nano' else 4)
        before=(n.calls,g.calls,j.calls)
        self.assertEqual(self.evaluate(n,g,j),0)
        self.assertEqual((n.calls,g.calls,j.calls),before)
        self.assertEqual(Q.read_json(self.out/'avaliacao/avaliacao_concluida.json')['status'],'concluida_com_bloqueios')

    def test_bloqueio_juiz_nao_divide_ou_reenvia_lotes(self):
        self.preparar();j=F.Julgamento(blocked=True)
        self.assertEqual(self.evaluate(j=j),0)
        self.assertEqual(j.calls,4)
        self.assertEqual(self.evaluate(j=j),0);self.assertEqual(j.calls,4)

    def test_comparacao_pareada_usa_intersecao_das_perguntas_com_nota(self):
        self.preparar()
        class UmBloqueio(Resposta):
            def json(self,system,user,tag='',**kw):
                if tag.startswith('resposta_') and user=='Pergunta sem_contexto 0?' and 'até 50 palavras' in system:
                    from pipeline.inventario.llm import ContentFiltered
                    self.calls+=1
                    raise ContentFiltered('bloqueio simulado de um caso')
                return super().json(system,user,tag=tag,**kw)
        self.assertEqual(self.evaluate(n=UmBloqueio()),0)
        for row in self.csv('comparacao_mesmas_questoes.csv'):
            expected=3 if row['conjunto']=='sem_contexto' and row['modelo']=='gpt-5-4-nano' else 4
            self.assertEqual(int(row['n_comum']),expected)
        primary=self.csv('resumo_exploratorio.csv')
        self.assertEqual([r['julgadas'] for r in primary if r['conjunto']=='sem_contexto'
            and r['modelo']=='gpt-5-4-nano'],['3','4','4'])

    def test_registra_extensao_real_sem_cortar_ou_regenerar(self):
        self.preparar();n=Resposta(long=True)
        self.assertEqual(self.evaluate(n=n),0);self.assertEqual(n.calls,16)
        rows=self.csv('resumo_exploratorio.csv');self.assertEqual(len(rows),12)
        for r in rows:
            if r['modelo']=='gpt-5-4-nano' and r['braco']!='p100':
                self.assertEqual(float(r['palavras_media']),110)
                self.assertEqual(r['acima_limite'],'4' if r['braco']=='p50' else '')
            if r['braco']=='p100':self.assertEqual(r['reaproveitadas'],'4')

    def test_divergencia_referencia_e_configuracao_impedem_mistura(self):
        self.preparar();self.assertEqual(self.evaluate(),0)
        with patch.object(X,'prompt_juiz',return_value='outro juiz'):
            with self.assertRaisesRegex(ValueError,'Prompts de referência mudaram'):self.evaluate()
        cfg=Q.read_json(self.out/'config.json');cfg['juiz']='outro'
        Q.atomic_json(self.out/'config.json',cfg)
        with self.assertRaisesRegex(ValueError,'Configuração mudou'):self.evaluate()
        source=next((self.ref/'avaliacao/respostas/gpt-5-4').glob('*.json'))
        r=Q.read_json(source);r['resposta']='alterada';Q.atomic_json(source,r)
        with self.assertRaisesRegex(ValueError,'Resposta da referência inconsistente'):self.evaluate()

    def test_referencia_incompleta_ou_config_diferente_recusada_antes_api(self):
        self.preparar();cfg=Q.read_json(self.ref/'config.json');altered=copy.deepcopy(cfg)
        altered['lote_juiz']=10;Q.atomic_json(self.ref/'config.json',altered)
        with self.assertRaisesRegex(ValueError,'Referência 100 incompatível'):self.evaluate()
        self.assertFalse(self.out.exists())
        Q.atomic_json(self.ref/'config.json',cfg)
        (self.ref/'avaliacao/avaliacao_concluida.json').unlink()
        with self.assertRaisesRegex(ValueError,'precisa estar concluída'):self.evaluate()
        self.assertFalse(self.out.exists())

    def test_plano_nao_cria_saida_ou_chama_avaliacao(self):
        self.preparar()
        with patch.object(X,'avaliar',side_effect=AssertionError('Sem API')),redirect_stdout(io.StringIO()):
            self.assertEqual(X.main(['--manifesto',str(self.manifest),'--referencia-100',str(self.ref),
                '--saida',str(self.out),'--plano']),0)
        self.assertFalse(self.out.exists())

    def test_nao_escreve_dentro_da_referencia_ou_fontes(self):
        self.preparar()
        for p in (self.ref,self.ref/'filha',self.root/'sem_contexto'/'nova'):
            with self.assertRaisesRegex(ValueError,'fora das fontes/referência'):
                X.avaliar(p,manifesto=self.manifest,referencia=self.ref)


if __name__=='__main__':unittest.main()
