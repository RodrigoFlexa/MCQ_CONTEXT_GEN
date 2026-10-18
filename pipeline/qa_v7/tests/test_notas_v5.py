"""Regressões das falhas reais de QA e integração com notas transferíveis."""
import copy
import json
import random
import unittest

import numpy as np

from pipeline.inventario.llm import CallFailed
from pipeline.qa_v7 import gerar_qa as G, plano as P, novidade as NV
from pipeline.qa_v7.tests.test_qa_v7 import FakeLLM, note, verdict


def question():
    return {'id': 'probe', 'alvo': 'A1', 'tipo': 'facil', 'alvo_descricao': 'área',
            'pergunta': 'Qual efeito da espuma sobre a área de gás?', 'resposta': 'Reduz a área.',
            'pontos_essenciais': ['área reduzida'], 'explicacao': 'A espuma ocupa espaço.',
            'fatos': ['F1'], 'codigo': [], 'juiz': [], 'correcoes': []}


def structured_note():
    n = note('n1', 'a1', ('facil',))
    n.update(schema_conhecimento='nota-v5', lacunas=['não há sinais de diagnóstico único'],
             relacoes=[{'id': 'R1', 'avaliavel': True, 'origem': 'fonte', 'fatos': ['c:n1#f0'],
                        'afirmacao': 'espuma reduz área', 'premissas': [], 'condicoes': ['espuma'], 'limites': []},
                       {'id': 'R2', 'avaliavel': False, 'origem': 'parametrico', 'fatos': ['extra'],
                        'afirmacao': 'hipótese auxiliar', 'premissas': [], 'condicoes': [], 'limites': []}])
    n['fontes']['extra'] = {**n['fontes']['c:n1#f0'], 'afirmacao': 'hipótese auxiliar'}
    n['alvos'][0].update(resposta='Reduz área.', relacoes=['R1'], fatos=['c:n1#f0'],
                          habilidade='compreensao', criterios_correcao=['redução da área'],
                          condicoes_enunciado=['há espuma'], limites=[])
    return n


class NotasV5(unittest.TestCase):
    def test_erro_cego_nunca_aprova(self):
        class Down:
            def json(self, *args, **kwargs):
                raise CallFailed('serviço indisponível', kind='transitorio')
        q = question()
        G.Runner(None, None, [], {}, 1, cego=Down()).avaliar(q, verdict('probe'), '', '', {'F1': {}})
        self.assertEqual(q['status'], 'pendente_validacao')
        self.assertIn('cego_indisponivel', q['motivos'])

    def test_gabarito_invalido_no_comparador_reprova(self):
        class Invalid(FakeLLM):
            def json(self, system, user, **kwargs):
                if system == G.COMPARA_SYSTEM:
                    return {'veredito': 'referencia_invalida', 'razao': 'sem suporte'}
                return super().json(system, user, **kwargs)
        q = question()
        G.Runner(None, Invalid(), [], {}, 1, cego=FakeLLM()).avaliar(q, verdict('probe'), '', '', {'F1': {}})
        self.assertEqual(q['status'], 'reprovada')
        self.assertIn('referencia_invalida', q['motivos'])

    def test_refino_nao_troca_gabarito_e_limita_tentativas(self):
        class Switch:
            def json(self, *args, **kwargs):
                return {**question(), 'resposta': 'Aumenta a área.'}
        q = question()
        runner = G.Runner(Switch(), None, [], {}, 1)
        self.assertFalse(runner.refine('', {'F1': {}}, q, {}))
        self.assertEqual(q['resposta'], 'Reduz a área.')
        self.assertFalse(runner.refine('', {'F1': {}}, q, {}))
        self.assertEqual(len(q['correcoes']), 1)

    def test_juiz_precisa_mapear_afirmacoes_em_fontes_existentes(self):
        for claims in ([], [{'afirmacao': 'algo', 'fatos': ['F9']}]):
            q, v = question(), verdict('probe')
            v['afirmacoes'] = claims
            G.Runner(None, None, [], {}, 1).avaliar(q, v, '', '', {'F1': {}})
            self.assertEqual(q['status'], 'reprovada')
            self.assertIn('suporte', q['motivos'])

    def test_analise_independente_nao_recebe_gabarito(self):
        class Blind(FakeLLM):
            def json(self, system, user, **kwargs):
                if system == G.CEGO_SYSTEM:
                    self.received = user
                return super().json(system, user, **kwargs)
        blind, q = Blind(), question()
        q['resposta'] = 'SEGREDO_DO_GABARITO'
        G.Runner(None, FakeLLM(), [], {}, 1, cego=blind).checar_cego(q, 'material secreto')
        self.assertEqual(blind.received, 'PERGUNTA: ' + q['pergunta'])

    def test_relacao_parametrica_nao_vira_fato_e_contrato_chega_ao_prompt(self):
        n = structured_note()
        sub = {'key': 's1', 'topico': 'T', 'subtopico': 'S', 'notas': [n], 'combinacoes': []}
        batch = P.build_queue(sub, 7)[0]
        table, mat = G.material(sub, [n], batch['alvos'], True)
        self.assertEqual(len(table), 1)
        self.assertIn('CONTRATO A1', mat)
        self.assertIn('não há sinais de diagnóstico único', mat)
        self.assertEqual(batch['alvos'][0]['contrato']['criterios_correcao'], ['redução da área'])
        runner = G.Runner(None, None, [], {}, 1)
        kept, dropped = runner.triar(sub, batch)
        self.assertEqual(kept[0]['resposta_esperada'], 'Reduz área.')
        self.assertFalse(dropped)
        self.assertEqual(len(G.plan_subtopic(sub, random.Random(7))), 1)

    def test_trecho_completo_e_evidencia_disponivel(self):
        n = structured_note()
        n['relacoes'][0]['fatos'] = ['trecho:x']
        n['fontes']['trecho:x'] = {'tipo': 'trecho', 'texto': 'Fonte completa com condições.', 'chunk_id': 'x'}
        table, _ = G.fact_table([n])
        self.assertEqual(table['F1']['citacao'], 'Fonte completa com condições.')

    def test_insuficiencia_nao_chama_juiz(self):
        class Insufficient:
            def json(self, system, user, **kwargs):
                data = {'items': [{'alvo': 'A1', 'status': 'insuficiente', 'motivo': 'faltam sinais'}]}
                kwargs['validate'](data)
                return data
        n = structured_note()
        sub = {'key': 's1', 'topico': 'T', 'subtopico': 'S', 'notas': [n], 'combinacoes': [], 'inventario': 'v5'}
        batch = P.build_queue(sub, 7)[0]
        result = G.Runner(Insufficient(), None, [], {}, 7).run_job(sub, batch)
        self.assertEqual(result[0]['status'], 'evidencia_insuficiente')

    def test_novidade_compara_entre_subtopicos_mesmo_com_cosseno_baixo(self):
        qs = [{**question(), 'id': str(i), 'sub_key': str(i), 'topico': 'T', 'subtopico': str(i),
               'status': 'aprovada', 'ordem': 0} for i in range(2)]
        NV.measure(qs, lambda texts: np.eye(len(texts)), FakeLLM(), scope='topico')
        self.assertTrue(qs[1]['novidade']['checado'])
        self.assertTrue(qs[1]['novidade']['redundante'])
