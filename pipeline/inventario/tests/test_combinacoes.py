"""Mapa de combinações de notas (base das questões difíceis do tipo B)."""
import unittest

from apoio import FakeLLM
from pipeline.inventario import combinacoes as M
from pipeline.inventario.llm import CallFailed

SUB = {'key': 's1', 'topico': 'Produção', 'subtopico': 'Separadores', 'frase': '...'}


def note(nid, assunto='a01', status='aprovada', palavras=300):
    return {'nid': nid, 'status': status, 'titulo': f'Nota {nid}', 'resumo': 'Resumo.', 'assunto_texto': 'assunto',
            'assuntos': [assunto], 'secoes': [{'titulo': 'Mecanismo', 'texto': 'Texto técnico da seção.'}],
            'metricas': {'palavras': palavras}, 'avaliacao': {'correcao_tecnica': 5, 'riqueza': 4}}


def combo(ids, **kw):
    return {'notas': ids, 'titulo': 'T', 'ligacao': 'L', 'raciocinio': 'R', 'cenario': 'C',
            'conhecimentos': [{'nota': i, 'conhecimento': 'k'} for i in ids], **kw}


class Combinacoes(unittest.TestCase):
    def setUp(self):
        self.short = {'N1': note('k1'), 'N2': note('k2', 'a02'), 'N3': note('k3'), 'N4': note('k4', 'a03')}

    def test_normaliza_e_descarta_com_motivo(self):
        data = {'combinacoes': [combo(['N1', 'N2']), combo(['N2', 'N1']), combo(['N1']), combo(['N1', 'N9']),
                                combo(['N1', 'N3'], cenario=' '), combo(['N1', 'N2', 'N3', 'N4']), 'x',
                                combo(['N1', 'N3', 'N4'])]}
        kept, dropped = M.normalize(data, self.short)
        self.assertEqual([c['notas'] for c in kept], [['k1', 'k2'], ['k1', 'k3', 'k4']])
        self.assertEqual([d['motivo'] for d in dropped], ['repetida', 'quantidade_de_notas', 'nota_inexistente',
                                                         'campos_vazios', 'quantidade_de_notas', 'formato_invalido'])
        self.assertTrue(kept[0]['multi_assunto'])
        self.assertEqual(kept[0]['assuntos'], ['a01', 'a02'])
        self.assertEqual([k['nid'] for k in kept[0]['conhecimentos']], ['k1', 'k2'])

    def test_quantidade_alvo(self):
        self.assertEqual([M.target_count(n) for n in (2, 9, 30, 100)], [2, 3, 10, 10])

    def test_poucas_notas_nao_chama_modelo(self):
        llm = FakeLLM()
        plan = M.plan_subtopic(llm, SUB, [note('k1'), note('k2', status='reprovada')])
        self.assertEqual((plan['modo'], plan['combinacoes'], llm.usage['calls']), ('poucas_notas', [], 0))

    def test_plano_usa_somente_aprovadas(self):
        llm = FakeLLM()
        plan = M.plan_subtopic(llm, SUB, [note('k2', 'a02'), note('k1'), note('k3', status='reprovada')])
        self.assertEqual(plan['modo'], 'modelo')
        c = plan['combinacoes'][0]
        self.assertEqual((c['cid'], c['notas'], c['sub_key']), ('s1:m1', ['k1', 'k2'], 's1'))

    def test_falha_propagada_para_o_orquestrador(self):
        FakeLLM.fail = {'combinacoes': 'falha'}
        self.addCleanup(lambda: setattr(FakeLLM, 'fail', {}))
        with self.assertRaises(CallFailed):
            M.plan_subtopic(FakeLLM(), SUB, [note('k1'), note('k2')])


if __name__ == '__main__':
    unittest.main()
