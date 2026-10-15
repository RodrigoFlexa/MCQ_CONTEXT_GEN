"""Testes offline do QA v7 (sem rede e sem chaves)."""
import json
import random
import re
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT))

from pipeline.inventario.llm import CallFailed  # noqa: E402
from pipeline.qa_v7 import comparar_juizes as CJ, gerar_qa as G  # noqa: E402


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
        self.assertEqual(resumo['variantes'], 12)
        self.assertEqual(t['aprovacao_originais'], 1.0)
        self.assertEqual(t['deteccao_erro_tecnico'], 1.0)                 # o fake reprova erro técnico e sem suporte
        self.assertEqual(t['deteccao_dependencia_fonte'], 0.0)
        self.assertEqual(t['motivo_certo_sem_suporte'], 1.0)
        self.assertEqual(resumo['concordancia']['j1:medium x j2:low']['concordancia'], 1.0)
        self.assertIn('Defeitos plantados que passaram', (out / 'relatorio_juizes.md').read_text(encoding='utf-8'))

    def test_modelo_invalido(self):
        with self.assertRaises(ValueError):
            G.parse_role('gpt:altissimo')
        self.assertEqual(G.parse_role('o3-petrobras:medium'), ('o3-petrobras', 'medium'))


if __name__ == '__main__':
    unittest.main()
