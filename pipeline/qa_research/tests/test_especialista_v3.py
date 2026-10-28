"""Curadoria ampliada, correção com parecer, ciclos limitados e reuso de avaliação."""
import copy
import json
import unittest

from pipeline.inventario.llm import ContentFiltered
from pipeline.qa_research.especialista_qa import core as C
from pipeline.qa_research.especialista_qa.preparacao_v3 import ENTRADA, ANTERIOR, ler_nao_reprovadas, reprovacao_explicita
from pipeline.qa_research.especialista_qa.refinamento_v3 import RefinarRevisadas, apoio_numeros, semear_avaliacao
from pipeline.qa_research.especialista_qa.avaliacao import avaliar
from pipeline.qa_research.tests.test_especialista_qa import Fixture, qa


class Model:
    def __init__(self, reject=0, fail_validation=False, filtered=False):
        self.reject, self.fail_validation, self.filtered = reject, fail_validation, filtered
        self.calls, self.validations = [], 0

    def json(self, system, user, tag='', validate=None, **kw):
        payload = json.loads(user)
        self.calls.append((tag, payload, system))
        if self.filtered:
            raise ContentFiltered('bloqueio simulado')
        if tag == 'especialista_converter':
            d = {'status': 'ok', 'motivo': '', 'qa': qa(), 'alteracoes': ['Delimitado o alvo da pergunta.'],
                 'uso_parecer': 'Parecer considerado na adaptação.', 'fonte_resposta': 'gabarito_original'}
        else:
            if self.fail_validation:
                self.fail_validation = False
                raise RuntimeError('falha temporária simulada')
            self.validations += 1
            approved = self.validations > self.reject
            criteria = dict.fromkeys(C.CRITERIOS, True)
            criteria['univoca'] = approved
            d = {'valida': approved, 'item': '01_01', 'tipo': 'conceito', 'cenario': False, 'composicao': 'simples',
                 'criterios': criteria, 'motivos': [] if approved else ['Delimite o alvo para evitar respostas distintas.'],
                 'justificativa': 'Auditoria simulada para testar o fluxo.'}
        if validate:
            validate(d)
        return d


class V3Tests(Fixture):
    def setUp(self):
        super().setUp()
        self.rows = ler_nao_reprovadas(ENTRADA)
        self.previous = {r['uid']:r for r in C.ler_linhas(ANTERIOR/'decisoes.jsonl')}
        self.row = next(r for r in self.rows if self.previous.get(r['uid'], {}).get('status') == 'reprovada')
        self.input = self.root/'v3.jsonl'
        C.jsonl(self.input, [self.row])

    def runner(self, model=None, **kw):
        model = model or Model()
        return RefinarRevisadas(self.out, entrada=self.input, base=self.base, sem_contexto=self.raw,
            clientes={'converter': model, 'validar': model}, progress=lambda *a, **k: None, **kw)

    def test_selecao_real_720_e_descarte_prevalece_em_qualquer_posicao(self):
        self.assertEqual(len(self.rows), 720)
        self.assertTrue(all(r['status_extracao'] == 'ok' for r in self.rows))
        numbers = {r['numero_original'] for r in self.rows}
        self.assertFalse({25, 86, 165} & numbers)
        self.assertTrue({38, 111, 191, 384, 890}.issubset(numbers))
        for text in ('aprovada, mas correto é descartar', 'não aprovada', 'Reprovada.', 'Descartar'):
            self.assertTrue(reprovacao_explicita(text))
        self.assertFalse(reprovacao_explicita('Não descartar. Aprovada com ressalvas.'))
        self.assertFalse(reprovacao_explicita('não reprovada'))

    def test_explicacoes_de_siglas_preservadas_sem_adivinhar_gabarito(self):
        r = next(r for r in self.rows if r['numero_original'] == 384)
        self.assertIn('MAOP =', r['notas_documento'])
        self.assertEqual(len(r['problemas_extracao_originais']), 4)
        self.assertEqual(len(r['evidencias_gabarito']), 1)

    def test_parecer_e_critica_chegam_ao_refinador_e_ao_auditor(self):
        m = Model(reject=1)
        self.assertEqual(self.runner(m).run(), 0)
        self.assertEqual(len(m.calls), 4)
        self.assertEqual(m.calls[0][1]['original']['parecer_especialista'], self.row['revisao_humana']['parecer_original'])
        self.assertTrue(m.calls[0][1]['qa_anterior'])
        self.assertEqual(m.calls[2][1]['critica_anterior'], ['Delimite o alvo para evitar respostas distintas.'])
        self.assertIn('parecer_especialista', m.calls[3][1]['original'])
        result = C.read_json(self.out/'resultado.json')
        self.assertEqual((result['aprovadas'], result['novas_aprovadas_v3']), (1, 1))
        self.assertEqual(C.ler_linhas(self.out/'decisoes.jsonl')[0]['ciclos_v3'], 2)

    def test_maximo_tres_ciclos_sem_forcar_aprovacao(self):
        m = Model(reject=100)
        self.assertEqual(self.runner(m).run(), 0)
        self.assertEqual(len(m.calls), 6)
        self.assertEqual(C.ler_linhas(self.out/'aprovadas.jsonl'), [])
        self.assertEqual(C.ler_linhas(self.out/'decisoes.jsonl')[0]['status'], 'reprovada')
        self.runner(m).run()
        self.assertEqual(len(m.calls), 6)

    def test_retomada_de_falha_na_validacao_nao_refaz_conversao(self):
        m = Model(fail_validation=True)
        self.assertEqual(self.runner(m).run(), 2)
        self.assertEqual(self.runner(m).run(), 0)
        self.assertEqual(sum(tag == 'especialista_converter' for tag,_,_ in m.calls), 1)

    def test_filtro_nao_dispara_refatoracao(self):
        m = Model(filtered=True)
        self.assertEqual(self.runner(m).run(), 0)
        self.assertEqual(len(m.calls), 1)
        self.assertEqual(C.ler_linhas(self.out/'decisoes.jsonl')[0]['status'], 'excluida_filtro_conteudo')

    def test_reprovada_na_entrada_e_bloqueada_antes_da_api(self):
        row = copy.deepcopy(self.row)
        row['revisao_humana']['parecer_original'] = 'aprovada, mas descartar'
        C.jsonl(self.input, [row])
        with self.assertRaisesRegex(ValueError, 'reprovada'):
            self.runner()

    def test_numeros_de_correcao_explicita_sao_apoio_sem_liberar_numero_inventado(self):
        row = copy.deepcopy(self.row)
        row['revisao_humana']['parecer_original'] = 'Aprovada com ressalva: considerar pressão de 275 bar.'
        self.assertNotIn('numero_novo_sem_sustentacao', C.problemas_codigo({**qa(), 'resposta': '275 bar.'}, apoio_numeros(row)))
        self.assertIn('numero_novo_sem_sustentacao', C.problemas_codigo({**qa(), 'resposta': '99999 bar.'}, apoio_numeros(row)))

    def test_preserva_175_e_reutiliza_respostas_e_notas_sem_novas_chamadas(self):
        approved = [r for r in self.rows if self.previous.get(r['uid'], {}).get('status') == 'aprovada']
        self.assertEqual(len(approved), 175)
        C.jsonl(self.input, approved)
        m = Model()
        self.assertEqual(self.runner(m).run(), 0)
        self.assertEqual(m.calls, [])
        self.assertEqual(C.read_json(self.out/'resultado.json')['reaproveitadas_v2'], 175)
        self.assertEqual(semear_avaliacao(self.out), 175)

        class OnlyProbe:
            def __init__(self):
                self.tags = []
            def json(self, system, user, tag='', validate=None, **kw):
                self.tags.append(tag)
                if not tag.startswith('teste_'):
                    raise AssertionError('Não responder/julgar novamente as 175 QAs')
                d = {'resposta': 'Separar óleo, gás e água.'}
                if validate:
                    validate(d)
                return d
        a,b = OnlyProbe(),OnlyProbe()
        self.assertEqual(avaliar(self.out, clientes={'resp_gpt-5-4-nano': a, 'resp_gpt-5-4': b, 'juiz': OnlyProbe()},
            progress=lambda *a, **k: None), 0)
        for s in C.read_json(self.out/'avaliacao/acuracia.json')['geral'].values():
            self.assertEqual(s['n'], 175)
        self.assertEqual(semear_avaliacao(self.out), 175)
        questions = C.ler_linhas(self.out/'aprovadas.jsonl')
        questions[0]['pergunta'] = 'Qual é outro alvo?'
        C.jsonl(self.out/'aprovadas.jsonl', questions)
        with self.assertRaisesRegex(ValueError, 'mudou'):
            semear_avaliacao(self.out)


if __name__ == '__main__':
    unittest.main()
