"""Testes offline do QA v7 (sem rede e sem chaves)."""
import json
import random
import re
import sys
import tempfile
import unittest

import numpy as np
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT))

from pipeline.inventario.llm import CallFailed  # noqa: E402
from pipeline.qa_v7 import comparar_juizes as CJ, gerar_qa as G, novidade as NV, plano as PL  # noqa: E402


def note(nid, assunto, alvos=('facil', 'media', 'dificil')):
    ref = f'c:{nid}#f0'
    return {'nid': nid, 'status': 'aprovada', 'topico': 'Tópico X', 'subtopico': 'Sub Y', 'sub_key': 's1',
            'assuntos': [assunto], 'assunto_texto': assunto, 'titulo': f'Nota {nid}', 'resumo': 'Resumo.',
            'secoes': [{'tipo': 'principio_mecanismo', 'texto': 'A espuma reduz a área de gás.', 'fatos': [ref],
                        'conhecimento_geral': False}],
            'alvos': [{'nivel': n, 'descricao': f'alvo {n} de {nid}'} for n in alvos],
            'fontes': {ref: {'tipo': 'fato', 'afirmacao': 'A espuma reduz a área de gás.', 'condicoes': '',
                             'citacao': 'A espuma reduz a área', 'collection': 'anp', 'title': 'doc',
                             'jurisdiction': 'BR', 'page_ini': 1}}}


def inventory(root):
    d = root / 'inv' / 'subtopicos' / 's1'
    d.mkdir(parents=True)
    notes = [note('k1', 'a01'), note('k2', 'a02'), note('k3', 'a03')]
    (d / 'notas_aprovadas.jsonl').write_text('\n'.join(json.dumps(n) for n in notes), encoding='utf-8')
    (d / 'combinacoes.json').write_text(json.dumps({'combinacoes': [
        {'cid': 's1:m1', 'notas': ['k1', 'k3'], 'titulo': 'Espuma e nível', 'ligacao': 'L', 'raciocinio': 'R',
         'cenario': 'C'}]}), encoding='utf-8')
    seeds = root / 'seeds.jsonl'
    seeds.write_text('\n'.join(json.dumps({'review_id': i, 'topic_path': f'Outro {i} > S', 'question': f'Pergunta {i}?',
                                           'answer': 'Resposta.'}) for i in range(5)), encoding='utf-8')
    ext = root / 'ext.jsonl'
    ext.write_text('\n'.join(json.dumps({'id': f'{ds}:{i}', 'question': f'Q {ds} {i}?', 'answer': 'A'})
                             for ds in ('arc_easy', 'arc_challenge', 'pira_ptbr', 'hotpotqa') for i in range(3)),
                   encoding='utf-8')
    return root / 'inv', seeds, ext


def verdict(qid, ok=True, reparavel=False, falha='suporte'):
    checks = {k: {'ok': True, 'razao': 'ok'} for k in G.CHECKS}
    if not ok:
        checks[falha] = {'ok': False, 'razao': 'falhou'}
    return {'id': qid, 'verificacoes': checks, 'notas': {'correcao': 0.95 if ok else 0.5},
            'reparavel': reparavel, 'problemas': [] if ok else ['problema']}


class FakeLLM:
    """Gerador/juiz simulado; `reject` define ids reprovados pelo juiz na primeira avaliação."""

    def __init__(self, reject=(), repairable=(), fail_gen=False):
        self.reject, self.repairable, self.fail_gen = set(reject), set(repairable), fail_gen
        self.usage = {'calls': 0, 'prompt_tokens': 0, 'completion_tokens': 0}
        self.seen = set()

    def json(self, system, user, tag='', max_tokens=0, validate=None, item=None):
        self.usage['calls'] += 1
        if system == G.GEN_SYSTEM:
            if self.fail_gen:
                raise CallFailed('falha simulada', kind='validacao')
            alvos = re.findall(r'^(A\d+) \((\w+)\):', user, flags=re.M)
            data = {'items': [{'alvo': a, 'tipo': t, 'pergunta': f'Por que a espuma afeta o gás ({t})?',
                               'resposta': 'Porque reduz a área de escoamento.', 'fatos': ['F1'], 'conceito': 'espuma'}
                              for a, t in alvos]}
        elif system == G.JUDGE_SYSTEM:
            qs = json.loads(user.split('QUESTÕES:\n', 1)[1])
            out = []
            for q in qs:
                first = q['id'] not in self.seen
                self.seen.add(q['id'])
                bad = q['id'] in self.reject and first or '::erro' in q['id'] or '::sem_suporte' in q['id']
                out.append(verdict(q['id'], ok=not bad, reparavel=q['id'] in self.repairable))
            data = {'avaliacoes': out}
        elif system == G.REFINE_SYSTEM:
            data = {'pergunta': 'Por que a espuma reduz a área de gás no separador?', 'resposta': 'Ocupa volume.',
                    'fatos': ['F1'], 'mudancas': 'redação'}
        elif system == NV.SYSTEM:
            ids = [x['id'] for x in json.loads(user)['anteriores']]
            data = {'pares': [{'id': i, 'julgamento': 'redundante', 'razao': 'mesma coisa'} for i in ids]}
        elif system == CJ.DEFECT_SYSTEM:
            data = {k: {'pergunta': f'Pergunta com {k}?', 'resposta': f'Resposta com {k}.', 'defeito': k} for k in CJ.DEFEITOS}
        else:
            raise AssertionError('chamada inesperada')
        if validate:
            validate(data)
        return data


class QAv7(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.root = Path(self.tmp.name)
        self.inv, self.seeds, self.ext = inventory(self.root)

    def args(self, *extra):
        return ['--inventarios', str(self.inv), '--saida', str(self.root / 'out'), '--sementes', str(self.seeds),
                '--exemplos-externos', str(self.ext), '--env', str(self.root), '--workers', '2', *extra]

    def test_plano_por_subtopico(self):
        sub = G.load_inventory([self.inv])[0]
        batches = G.plan_subtopic(sub, random.Random(1))
        self.assertEqual([[a['tipo'] for a in b['alvos']] for b in batches], [['facil', 'media'], ['dificil_A'], ['dificil_B']])
        self.assertNotEqual(batches[0]['notas'][0]['nid'], batches[1]['notas'][0]['nid'])
        self.assertEqual(len(batches[2]['notas']), 2)

    def test_verificacao_em_codigo(self):
        table = {'F1': {}}
        q = {'pergunta': 'Na opção A, com menor impacto, qual escolher?', 'resposta': 'A opção A.', 'fatos': ['F1']}
        self.assertEqual(G.check_code(q, table), [])                      # "opção A" de cenário não é alternativa
        for ok in ('A equipe avalia duas alternativas de projeto: qual priorizar?', 'O cenário foi considerado no estudo do sistema receptor?'):
            self.assertEqual(G.check_code({'pergunta': ok, 'resposta': 'Sim.', 'fatos': ['F1']}, table), [])
        for bad in ('Assinale a alternativa correta.', 'Conforme o estudo citado, qual a causa?', 'O F3 indica o quê?'):
            self.assertTrue(G.check_code({'pergunta': bad, 'resposta': 'Sim.', 'fatos': ['F1']}, table))
        q2 = {'pergunta': 'Segundo a nota técnica, qual das seguintes?', 'resposta': 'Ver F2.', 'fatos': ['F9']}
        self.assertEqual(set(G.check_code(q2, table)), {'referencia_alternativas', 'depende_do_material', 'fato_inexistente'})

    def test_fluxo_aprova_corrige_e_reprova(self):
        gen = FakeLLM()
        judge = FakeLLM(reject={'s1-b0-A1', 's1-b1-A1'}, repairable={'s1-b0-A1'})
        resumo = G.main(self.args(), clients=(gen, judge))
        rows = [json.loads(l) for l in (self.root / 'out' / 'questoes.jsonl').read_text(encoding='utf-8').splitlines()]
        by = {r['id']: r for r in rows}
        self.assertEqual(len(rows), 4)
        self.assertEqual(by['s1-b0-A1']['status'], 'aprovada')            # reparável: corrigida e reaprovada
        self.assertTrue(by['s1-b0-A1']['correcoes'])
        self.assertEqual(by['s1-b1-A1']['status'], 'reprovada')           # não reparável
        self.assertEqual(by['s1-b1-A1']['motivos'], ['suporte'])
        self.assertEqual(by['s1-b2-A1']['nivel'], 'dificil')              # nível = tipo pedido
        self.assertEqual(resumo['status'], {'aprovada': 3, 'reprovada': 1})
        self.assertNotIn('nivel_medido', by['s1-b0-A1'])
        self.assertTrue((self.root / 'out' / 'relatorio.md').exists())

    def test_falha_de_lote_nao_derruba_execucao(self):
        resumo = G.main(self.args(), clients=(FakeLLM(fail_gen=True), FakeLLM()))
        self.assertEqual(resumo['status'], {'falhou': 3})

    def test_comparacao_de_juizes(self):
        G.main(self.args(), clients=(FakeLLM(), FakeLLM()))
        out = self.root / 'cmp'
        resumo = CJ.main(['--inventarios', str(self.inv), '--questoes', str(self.root / 'out' / 'questoes.jsonl'),
                          '--saida', str(out), '--juizes', 'j1:medium', 'j2:low', '--defeitos', '4', '--env', str(self.root)],
                         clients={'juizes': {'j1:medium': FakeLLM(), 'j2:low': FakeLLM()}, 'defeitos': FakeLLM()})
        t = resumo['juizes']['j1:medium']
        self.assertEqual(resumo['originais'], 4)
        self.assertEqual(resumo['variantes'], 16)
        self.assertEqual(t['aprovacao_originais'], 1.0)
        self.assertEqual(t['deteccao_erro_tecnico'], 1.0)                 # o fake reprova erro técnico e sem suporte
        self.assertEqual(t['deteccao_dependencia_fonte'], 0.0)
        self.assertEqual(t['motivo_certo_sem_suporte'], 1.0)
        self.assertEqual(resumo['concordancia']['j1:medium x j2:low']['concordancia'], 1.0)
        self.assertIn('Defeitos plantados que passaram', (out / 'relatorio_juizes.md').read_text(encoding='utf-8'))

    def test_juiz_indisponivel_nao_derruba_comparacao(self):
        class Down(FakeLLM):
            def json(self, system, user, **kw):
                if system == G.JUDGE_SYSTEM:
                    raise RuntimeError('NotFoundError: deployment inexistente')
                return super().json(system, user, **kw)
        G.main(self.args(), clients=(FakeLLM(), FakeLLM()))
        resumo = CJ.main(['--inventarios', str(self.inv), '--questoes', str(self.root / 'out' / 'questoes.jsonl'),
                          '--saida', str(self.root / 'cmp2'), '--juizes', 'ok:low', 'fora:low', '--defeitos', '4',
                          '--env', str(self.root)],
                         clients={'juizes': {'ok:low': FakeLLM(), 'fora:low': Down()}, 'defeitos': FakeLLM()})
        self.assertEqual(resumo['juizes']['fora:low']['erros'], 20)
        self.assertEqual(resumo['juizes']['ok:low']['avaliados'], 20)

    def test_fila_reveza_niveis_notas_e_esgota_alvos(self):
        sub = G.load_inventory([self.inv])[0]
        q = PL.build_queue(sub, 7)
        self.assertEqual(len(q), 3 * 3 + 1)                               # 9 alvos + 1 combinação
        self.assertEqual(len({b['alvo_ref'] for b in q}), len(q))         # cada alvo uma vez
        self.assertEqual([b['alvos'][0]['tipo'] for b in q[:6]],
                         ['facil', 'media', 'dificil_A', 'media', 'facil', 'dificil_B'])
        self.assertEqual(len({b['notas'][0]['nid'] for b in q[:3]}), 3)   # 3 notas antes de repetir
        self.assertEqual(q, PL.build_queue(sub, 7))                       # determinística
        self.assertEqual([b['ordem'] for b in q], list(range(len(q))))

    def test_cota_por_topico(self):
        subs = [{'key': k, 'topico': t, 'notas': [0] * n} for k, t, n in
                (('a', 'T1', 60), ('b', 'T1', 30), ('c', 'T1', 2), ('d', 'T2', 5))]
        q = PL.allocate(subs, 100, 3)
        self.assertEqual(q['a'] + q['b'] + q['c'], 100)
        self.assertEqual(q['d'], 100)
        self.assertGreaterEqual(q['c'], 3)
        self.assertGreater(q['a'], q['b'])

    def test_modo_cota_repoe_reprovadas(self):
        judge = FakeLLM(reject={'s1-s0001-A1'})
        resumo = G.main(self.args('--modo', 'cota', '--por-topico', '4', '--min-por-subtopico', '1'),
                        clients=(FakeLLM(), judge))
        self.assertEqual(resumo['aprovadas_por_topico'], {'Tópico X': 4})
        rows = [json.loads(l) for l in (self.root / 'out' / 'questoes.jsonl').read_text(encoding='utf-8').splitlines()]
        self.assertEqual([r['ordem'] for r in rows], [0, 1, 2, 3, 4])      # 5ª da fila repõe a reprovada

    def test_modo_profundo_e_novidade(self):
        def embed(texts):
            return np.stack([np.ones(4) / 2 for _ in texts])              # tudo igual: tudo vizinho
        resumo = G.main(self.args('--modo', 'profundo', '--subtopicos', 'Sub Y'),
                        clients=(FakeLLM(), FakeLLM(), FakeLLM()), embed=embed)
        self.assertEqual(sum(resumo['status'].values()), 10)
        self.assertEqual(resumo['redundantes'], 9)                        # a primeira é nova; as demais repetem
        nov = json.loads((self.root / 'out' / 'novidade.json').read_text(encoding='utf-8'))
        self.assertEqual(nov['janelas']['s1'][0]['redundantes'], 9)
        self.assertIn('Curva de novidade', (self.root / 'out' / 'relatorio.md').read_text(encoding='utf-8'))

    def test_profundo_exige_subtopicos(self):
        with self.assertRaises(SystemExit):
            G.parse(self.args('--modo', 'profundo'))

    def test_citacao_de_estudo_na_resposta(self):
        r = G.check_code({'pergunta': 'Por que calibrar por condição?', 'resposta': 'Como em Hines et al. (2008a).',
                          'fatos': ['F1']}, {'F1': {}})
        self.assertIn('depende_do_material', r)

    def test_modelo_invalido(self):
        with self.assertRaises(ValueError):
            G.parse_role('gpt:altissimo')
        self.assertEqual(G.parse_role('o3-petrobras:medium'), ('o3-petrobras', 'medium'))


if __name__ == '__main__':
    unittest.main()
