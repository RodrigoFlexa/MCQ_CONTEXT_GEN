"""Testes offline de extração, fidelidade, retomada, junção e respostas paralelas."""
import copy
import io
import json
import tempfile
import threading
import unittest
import importlib.util
from contextlib import redirect_stdout
from pathlib import Path
from unittest.mock import patch
from zipfile import ZipFile
from xml.sax.saxutils import escape

from pipeline.qa_research.especialista_qa import core as M
from pipeline.qa_research.especialista_qa.extracao import extrair, jsonl
from pipeline.qa_research.especialista_qa.__main__ import main


def original(i=1):
    options = {k: {'texto': t, 'metodo_rotulo': 'rotulo_explicito'} for k, t in zip('ABCD', (
        'Qualidade dos processos', 'Eficiência, disponibilidade e qualidade', 'Rendimento térmico', 'Custos operacionais'))}
    return {'uid': f'especialista:g01:{i:04d}', 'agrupamento_id': 'g01', 'agrupamento_original': 'Gestão do Desempenho',
            'numero_original': i, 'enunciado': 'O indicador OEE avalia:', 'alternativas': options,
            'gabarito': 'B', 'resposta_original': options['B']['texto'], 'justificativa_original': '',
            'evidencias_gabarito': [{'alternativa': 'B', 'metodo': 'marca_na_alternativa'}],
            'status_extracao': 'ok', 'problemas_extracao': [], 'fonte': {'paragrafo_inicio': i}}


def qa():
    return {'pergunta': 'O que avalia o indicador OEE?', 'resposta': 'Eficiência, disponibilidade e qualidade.',
            'item': '01_01', 'tipo': 'conceito', 'cenario': False, 'composicao': 'simples'}


class Fake:
    def __init__(self, *, discard=False, reject=False, leak=False, fail=None, reclassify=False, error=None):
        self.discard, self.reject, self.leak, self.fail = discard, reject, leak, fail
        self.reclassify = reclassify
        self.error = error
        self.calls = []

    def json(self, system, user, tag='', validate=None, **kw):
        payload = json.loads(user)
        self.calls.append((tag, payload, system))
        if tag == self.fail:
            self.fail = None
            raise self.error or RuntimeError('falha simulada')
        if tag == 'especialista_converter':
            q = qa()
            if self.leak:
                q['pergunta'] = 'O OEE avalia eficiência, disponibilidade e qualidade?'
            if self.reclassify:
                q['tipo'] = 'mecanismo'
            d = {'status': 'descartar' if self.discard else 'ok',
                 'motivo': 'Não há conversão inequívoca.' if self.discard else '',
                 'qa': None if self.discard else q}
        else:
            criteria = dict.fromkeys(M.CRITERIOS, True)
            criteria['univoca'] = not self.reject
            d = {'valida': not self.reject, 'item': '07_03' if self.reclassify else '01_01',
                 'tipo': 'conceito', 'cenario': False, 'composicao': 'simples',
                 'criterios': criteria, 'motivos': ['varias_respostas'] if self.reject else [],
                 'justificativa': 'Verificação simulada da fidelidade e da resposta.'}
        if validate:
            validate(d)
        return d


class Fixture(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.out = self.root/'run'
        self.input = self.root/'questoes_mcq.jsonl'
        self.base = self.root/'base.jsonl'
        self.raw = self.root/'sem_contexto.jsonl'
        jsonl(self.input, [original()])
        jsonl(self.base, [{**qa(), 'uid': 'base:1', 'aprovada': True},
                          {**qa(), 'uid': 'base:2', 'aprovada': True}])
        jsonl(self.raw, [{**qa(), 'uid': 'raw:1'}, {**qa(), 'uid': 'raw:2'}])

    def runner(self, fake=None, **kw):
        f = fake or Fake()
        return M.ConverterEspecialista(self.out, entrada=self.input, base=self.base, sem_contexto=self.raw,
             clientes={'converter': f, 'validar': f}, progress=lambda *a, **k: None, **kw)


class ConversionTests(Fixture):
    def test_converte_valida_e_junta_somente_aprovadas(self):
        f = Fake(reclassify=True)
        self.assertEqual(self.runner(f).run(), 0)
        approved = M.ler_linhas(self.out/'aprovadas.jsonl')
        self.assertEqual(len(approved), 1)
        self.assertEqual(approved[0]['agrupamento_original'], 'Gestão do Desempenho')
        self.assertEqual(approved[0]['item'], '07_03')
        self.assertEqual(approved[0]['tipo'], 'conceito')
        self.assertEqual(approved[0]['tipo_declarado'], 'mecanismo')
        self.assertEqual(approved[0]['pergunta'], qa()['pergunta'])
        self.assertEqual(approved[0]['resposta'], qa()['resposta'])
        manifest = M.read_json(self.out/'bancos/manifesto.json')
        self.assertEqual([b['questoes'] for b in manifest['bancos']], [2, 2, 3])
        self.assertEqual(len(f.calls[0][1]['catalogo']), 40)
        self.assertEqual(f.calls[0][1]['original']['gabarito'], 'B')
        self.assertEqual(M.ler_linhas(self.base)[0]['uid'], 'base:1')

    def test_reprovada_nao_entra_no_banco(self):
        self.assertEqual(self.runner(Fake(reject=True)).run(), 0)
        self.assertEqual(M.ler_linhas(self.out/'aprovadas.jsonl'), [])
        self.assertEqual(len(M.ler_linhas(self.out/'reprovadas.jsonl')), 1)
        self.assertEqual(len(M.ler_linhas(self.out/'bancos/com_contexto_com_especialista.jsonl')), 2)

    def test_codigo_barra_resposta_no_enunciado_mesmo_com_auditor_aprovando(self):
        self.assertEqual(self.runner(Fake(leak=True)).run(), 0)
        decision = M.ler_linhas(self.out/'decisoes.jsonl')[0]
        self.assertEqual(decision['status'], 'reprovada')
        self.assertIn('resposta_literal_no_enunciado', decision['problemas_codigo'])

    def test_descartada_nao_chama_validador(self):
        f = Fake(discard=True)
        self.runner(f).run()
        self.assertEqual([c[0] for c in f.calls], ['especialista_converter'])
        self.assertEqual(M.read_json(self.out/'resultado.json')['status'], {'descartada_conversao': 1})

    def test_pendencia_extracao_nao_e_adivinhada(self):
        row = original()
        row.update(status_extracao='pendente', gabarito=None, resposta_original=None,
                   problemas_extracao=['gabarito_ausente'])
        jsonl(self.input, [row])
        f = Fake()
        self.runner(f).run()
        self.assertEqual(f.calls, [])

    def test_retomada_nao_converte_novamente_apos_falha_na_validacao(self):
        f = Fake(fail='especialista_validar')
        self.assertEqual(self.runner(f).run(), 2)
        self.assertFalse((self.out/'conversao_concluida.json').exists())
        self.assertEqual(self.runner(f).run(), 0)
        self.assertEqual([c[0] for c in f.calls].count('especialista_converter'), 1)
        n = len(f.calls)
        self.assertEqual(self.runner(f).run(), 0)
        self.assertEqual(len(f.calls), n)

    def test_preserva_duplicatas_validas_e_fontes_intactas(self):
        jsonl(self.input, [original(1), original(2)])
        before = self.base.read_bytes(), self.raw.read_bytes(), self.input.read_bytes()
        self.runner(workers=2).run()
        approved = M.ler_linhas(self.out/'aprovadas.jsonl')
        self.assertEqual(len(approved), 2)
        self.assertEqual(approved[0]['pergunta'], approved[1]['pergunta'])
        self.assertEqual(len({q['uid'] for q in approved}), 2)
        self.assertEqual((self.base.read_bytes(), self.raw.read_bytes(), self.input.read_bytes()), before)

    def test_piloto_preserva_selecao_na_retomada(self):
        jsonl(self.input, [original(1), original(2)])
        self.runner(limite=1).run()
        resumed = self.runner()
        self.assertEqual(len(resumed.rows), 1)
        self.assertEqual(resumed.run(), 0)

    def test_mudanca_na_entrada_bloqueia_retomada(self):
        self.runner().run()
        row = original()
        row['enunciado'] = 'Outro alvo.'
        jsonl(self.input, [row])
        with self.assertRaisesRegex(ValueError, 'mudaram'):
            self.runner().run()

    def test_gabarito_inconsistente_bloqueia_antes_da_api(self):
        row = original()
        row['gabarito'] = 'C'
        jsonl(self.input, [row])
        with self.assertRaisesRegex(ValueError, 'gabarito'):
            self.runner()

    def test_numero_novo_e_referencia_a_alternativas(self):
        q = {**qa(), 'resposta': '99%.'}
        self.assertIn('numero_novo_sem_sustentacao', M.problemas_codigo(q, original()))
        q = {**qa(), 'pergunta': 'Qual alternativa está correta?'}
        self.assertIn('referencia_a_alternativas', M.problemas_codigo(q, original()))
        self.assertIn('referencia_a_alternativas', M.problemas_codigo({**qa(), 'resposta': 'B'}, original()))

    def test_banco_de_referencia_mudou_nao_monta_outra_versao(self):
        c = self.runner()
        c.run()
        rows = M.ler_linhas(self.base)
        rows[0]['pergunta'] = 'Qual é outro alvo?'
        jsonl(self.base, rows)
        with self.assertRaisesRegex(ValueError, 'referência mudou'):
            c.montar_bancos()

    def test_plano_nao_chama_modelos_nem_cria_saida(self):
        args = ['converter', '--entrada', str(self.input), '--base', str(self.base),
                '--sem-contexto', str(self.raw), '--saida', str(self.out), '--plano']
        with patch.object(M.ConverterEspecialista, 'cliente', side_effect=AssertionError('Não chamar')), redirect_stdout(io.StringIO()):
            self.assertEqual(main(args), 0)
        self.assertFalse(self.out.exists())

    def test_validacao_exige_todos_os_criterios_e_ids_do_catalogo(self):
        f = Fake()
        audit = f.json('', json.dumps({'qa': qa()}), tag='especialista_validar')
        audit['criterios']['fiel_gabarito'] = False
        with self.assertRaises(ValueError):
            M.validar_auditoria(audit, {'01_01'})
        bad = {'status': 'ok', 'motivo': '', 'qa': {**qa(), 'item': 'desconhecido'}}
        with self.assertRaises(ValueError):
            M.validar_conversao(bad, {'01_01'})

    def test_erro_fatal_interrompe_as_chamadas_restantes(self):
        class Fatal(RuntimeError):
            kind = 'fatal'
        jsonl(self.input, [original(1), original(2)])
        f = Fake(fail='especialista_converter', error=Fatal('401 simulado'))
        self.assertEqual(self.runner(f, workers=1).run(), 2)
        self.assertEqual(len(f.calls), 1)
        self.assertTrue((self.out/'interrupcao.json').exists())


class ExtractionTests(Fixture):
    def docx(self, paragraphs):
        path = self.root/'source.docx'
        body = ''
        for text, numbered in paragraphs:
            props = '<w:pPr><w:numPr><w:numId w:val="1"/></w:numPr></w:pPr>' if numbered else ''
            runs = '<w:r>'+''.join('<w:t>'+escape(t)+'</w:t><w:br/>' for t in text.split('\n'))+'</w:r>'
            body += '<w:p>'+props+runs+'</w:p>'
        with ZipFile(path, 'w') as z:
            z.writestr('word/document.xml', '<w:document xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main"><w:body>'+body+'</w:body></w:document>')
        return path

    def test_marca_na_alternativa_e_gabarito_separado(self):
        path = self.docx([('Gestão – 2 Questões', False),
                         ('1. OEE avalia:\nA) Alpha\nB) Beta ✅\nC) Gamma\nD) Delta', False),
                         ('2- Qual é o alvo?', False), ('A- Alpha', True), ('B- Beta', True),
                         ('C- Gamma', True), ('D- Delta', True), ('- Resposta correta: C', True)])
        d = extrair(path, self.root/'extracted')
        self.assertEqual(d['elegiveis'], 2)
        rows = M.ler_linhas(self.root/'extracted/questoes_mcq.jsonl')
        self.assertEqual([r['gabarito'] for r in rows], ['B', 'C'])
        self.assertEqual(rows[1]['numero_original'], 2)

    def test_lista_automatica_do_word(self):
        path = self.docx([('Gestão – 1 Questões', False), ('1 Qual é o alvo?', False),
                         ('Alpha', True), ('Beta', True), ('Gamma', True), ('Delta\n✅ Resposta correta: B', True)])
        d = extrair(path, self.root/'extracted')
        self.assertEqual(d['elegiveis'], 1)
        row = M.ler_linhas(self.root/'extracted/questoes_mcq.jsonl')[0]
        self.assertEqual(row['resposta_original'], 'Beta')
        self.assertEqual(row['alternativas']['B']['metodo_rotulo'], 'ordem_lista_word')

    def test_gabarito_conflitante_e_ausente_ficam_pendentes(self):
        path = self.docx([('Gestão – 2 Questões', False),
            ('1. Qual é o alvo?\nA) Alpha\nB) Beta ✅\nC) Gamma\nD) Delta\nGabarito: C', False),
            ('2. Qual é o alvo?\nA) Alpha\nB) Beta\nC) Gamma\nD) Delta', False)])
        d = extrair(path, self.root/'extracted')
        self.assertEqual(d['elegiveis'], 0)
        self.assertEqual(d['pendentes'], 2)
        self.assertEqual(d['motivos_pendencia']['gabaritos_conflitantes'], 1)
        self.assertEqual(d['motivos_pendencia']['gabarito_ausente'], 1)

    def test_entrada_real_confere_com_as_dez_contagens(self):
        data = M.read_json(M.ENTRADA.parent/'extracao.json')
        rows = M.ler_linhas(M.ENTRADA_AUTORAL)
        self.assertEqual(len(rows), 2546)
        self.assertEqual(len(data['agrupamentos']), 10)
        self.assertEqual(sum(r['quantidade_declarada'] for r in data['agrupamentos']), 2546)
        self.assertTrue(all(r['diferenca_contagem'] == 0 for r in data['agrupamentos']))
        self.assertTrue(all(r['status_extracao'] == 'ok' for r in rows))
        self.assertEqual(rows[0]['gabarito'], 'B')
        self.assertEqual(rows[1]['resposta_original'], 'Alta disponibilidade')


class EvaluationTests(Fixture):
    class Responder:
        def __init__(self, barrier, fail=False):
            self.barrier, self.fail, self.users = barrier, fail, []

        def json(self, system, user, tag='', validate=None, **kw):
            if self.fail:
                raise RuntimeError('DeploymentNotFound')
            if tag.startswith('resposta_'):
                self.users.append(user)
                self.barrier.wait(timeout=5)
            d = {'resposta': 'Eficiência, disponibilidade e qualidade.'}
            if validate:
                validate(d)
            return d

    class Judge:
        def json(self, system, user, validate=None, **kw):
            d = {'avaliacoes': [{'id': q['id'], 'veredito': 'correta', 'justificativa': 'Mesmo alvo.'} for q in json.loads(user)]}
            if validate:
                validate(d)
            return d

    def test_dois_modelos_paralelos_sem_gabarito_e_retomada(self):
        from pipeline.qa_research.especialista_qa.avaliacao import avaliar
        self.runner().run()
        before = (self.out/'aprovadas.jsonl').read_bytes()
        barrier = threading.Barrier(2)
        a, b = self.Responder(barrier), self.Responder(barrier)
        cl = {'resp_gpt-5-4-nano': a, 'resp_gpt-5-4': b, 'juiz': self.Judge()}
        status = avaliar(self.out, clientes=cl, progress=lambda *a, **k: None)
        errors = [M.read_json(p) for p in (self.out/'avaliacao/falhas').glob('*.json')]
        errors.append(M.read_json(self.out/'avaliacao/falha_execucao.json'))
        self.assertEqual(status, 0, errors)
        self.assertEqual(a.users, [qa()['pergunta']])
        self.assertEqual(b.users, [qa()['pergunta']])
        self.assertEqual((self.out/'aprovadas.jsonl').read_bytes(), before)
        self.assertEqual(avaliar(self.out, clientes=cl, progress=lambda *a, **k: None), 0)
        self.assertEqual(len(a.users), 1)
        summary = M.read_json(self.out/'avaliacao/acuracia.json')
        self.assertEqual(set(summary['geral']), {'gpt-5-4-nano', 'gpt-5-4'})
        self.assertTrue((self.out/'avaliacao/avaliacao_concluida.json').exists())

    def test_modelo_obrigatorio_indisponivel_nao_e_sucesso(self):
        from pipeline.qa_research.especialista_qa.avaliacao import avaliar
        self.runner().run()
        barrier = threading.Barrier(2)
        cl = {'resp_gpt-5-4-nano': self.Responder(barrier, fail=True),
              'resp_gpt-5-4': self.Responder(barrier), 'juiz': self.Judge()}
        self.assertEqual(avaliar(self.out, clientes=cl, progress=lambda *a, **k: None), 2)
        self.assertFalse((self.out/'avaliacao/avaliacao_concluida.json').exists())


@unittest.skipUnless(all(importlib.util.find_spec(x) for x in ('numpy', 'sklearn', 'matplotlib')), 'Bibliotecas locais de análise não disponíveis')
class AnalysisTests(Fixture):
    def test_tres_bancos_e_graficos_sem_api_ou_remocao(self):
        import numpy as np
        from pipeline.qa_research.especialista_qa.analise import analisar
        self.runner().run()
        analysis = self.root/'analysis'
        def vectors(texts):
            return np.tile(np.array([[1., 0., 0.]], dtype=np.float32), (len(texts), 1))
        result = analisar(self.out/'bancos/manifesto.json', analysis, encoder=vectors)
        self.assertEqual([d['questoes'] for d in result.values()], [2, 2, 3])
        self.assertEqual(result['com_contexto_com_especialista']['similaridade']['e5_perguntas']['pares'], 3)
        for image in ('vocabulario.png', 'similaridade_perguntas.png', 'similaridade_perguntas_respostas.png'):
            self.assertTrue((analysis/image).exists())
        self.assertEqual(len(M.ler_linhas(self.out/'aprovadas.jsonl')), 1)


if __name__ == '__main__':
    unittest.main()
