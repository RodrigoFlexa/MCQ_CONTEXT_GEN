"""Retoma a run publicada sem regenerar QAs; bloqueios têm decisão terminal e cobertura explícita."""
import json
import shutil
import unittest

from pipeline.inventario.llm import ContentFiltered
from pipeline.qa_research.especialista_qa import core as M
from pipeline.qa_research.especialista_qa.avaliacao import avaliar
from pipeline.qa_research.tests.test_especialista_qa import Fixture, Fake, original


class NuncaChamar:
    def json(self, *a, **k):
        raise AssertionError('Não deve refazer chamadas concluídas ou bloqueadas')


class RetomadaTests(Fixture):
    def test_filtro_novo_na_conversao_e_validacao_exclui_sem_aprovar_ou_repetir(self):
        for role in ('converter', 'validar'):
            with self.subTest(role=role):
                self.out = self.root/role
                fake = Fake(fail='especialista_'+role, error=ContentFiltered('bloqueio simulado'))
                self.assertEqual(self.runner(fake).run(), 0)
                decisions = M.ler_linhas(self.out/'decisoes.jsonl')
                self.assertEqual(decisions[0]['status'], 'excluida_filtro_conteudo')
                self.assertEqual(decisions[0]['etapa'], role)
                self.assertEqual(M.ler_linhas(self.out/'aprovadas.jsonl'), [])
                self.assertTrue((self.out/'conversao_concluida.json').exists())
                self.assertEqual(len(list((self.out/'bloqueadas').glob('*.json'))), 1)
                count = len(fake.calls)
                self.assertEqual(self.runner(fake).run(), 0)
                self.assertEqual(len(fake.calls), count)

    def test_filtro_ja_salvo_e_finalizado_sem_api(self):
        path = self.out/'falhas'/M.ConverterEspecialista.nome(original()['uid'])
        M.atomic_json(path, {'uid': original()['uid'], 'erro': 'ContentFiltered', 'mensagem': 'bloqueio anterior'})
        self.assertEqual(self.runner(NuncaChamar()).run(), 0)
        self.assertFalse(path.exists())
        self.assertEqual(M.read_json(self.out/'resultado.json')['status'], {'excluida_filtro_conteudo': 1})

    def test_compatibilidade_exige_codigo_conhecido_e_protocolo_identico(self):
        self.runner().run()
        config = self.out/'config.json'
        old = M.read_json(config)
        old['codigo_sha256'] = next(iter(M.CORE_COMPATIVEL))
        M.atomic_json(config, old)
        before = config.read_bytes()
        self.assertEqual(self.runner(NuncaChamar()).run(), 0)
        self.assertEqual(config.read_bytes(), before)
        self.assertEqual(M.read_json(self.out/'compatibilidade_retomada.json')['config_original_sha256'], M.sha(old))
        runner = self.runner(NuncaChamar())
        runner.prompts['converter'] += '\nMudança de protocolo'
        with self.assertRaisesRegex(ValueError, 'mudaram'):
            runner.run()
        old['codigo_sha256'] = 'codigo-desconhecido'
        M.atomic_json(config, old)
        with self.assertRaisesRegex(ValueError, 'mudaram'):
            self.runner(NuncaChamar()).run()

    def test_run_publicada_preserva_as_798_aprovadas_e_todas_as_decisoes(self):
        source = M.ROOT/'pipeline/qa_research/relatorios/especialista_qa_v2'
        if not (source/'config.json').exists():
            self.skipTest('Snapshot da execução não disponível')
        shutil.copytree(source/'processadas', self.out/'processadas')
        shutil.copytree(source/'falhas', self.out/'falhas')
        shutil.copyfile(source/'config.json', self.out/'config.json')
        name = 'especialista_g07_0148.json'
        (self.out/'conversoes').mkdir()
        shutil.copyfile(source/'conversoes'/name, self.out/'conversoes'/name)
        before = {p.name: p.read_bytes() for p in (self.out/'processadas').glob('*.json')}
        approved_before = M.ler_linhas(source/'aprovadas.jsonl')
        c = M.ConverterEspecialista(self.out, clientes={'converter': NuncaChamar(), 'validar': NuncaChamar()},
                                   progress=lambda *a, **k: None)
        self.assertEqual(c.run(), 0)
        self.assertEqual(M.ler_linhas(self.out/'aprovadas.jsonl'), approved_before)
        self.assertEqual(len(approved_before), 798)
        self.assertTrue(all((self.out/'processadas'/name).read_bytes() == data for name, data in before.items()))
        self.assertEqual(M.read_json(self.out/'resultado.json')['status'],
                         {'aprovada': 798, 'reprovada': 2180, 'descartada_conversao': 13, 'excluida_filtro_conteudo': 1})
        self.assertEqual(M.read_json(self.out/'conversao_concluida.json')['bancos']['com_contexto_com_especialista'], 3616)
        self.assertEqual(M.read_json(self.out/'bloqueadas'/name)['etapa'], 'validar')


class Respondente:
    def __init__(self, *, blocked=False, error=False):
        self.blocked, self.error, self.calls = blocked, error, 0

    def json(self, system, user, tag='', validate=None, **kw):
        if tag.startswith('resposta_'):
            self.calls += 1
            if self.blocked:
                raise ContentFiltered('resposta bloqueada')
            if self.error:
                raise RuntimeError('serviço temporariamente indisponível')
        d = {'resposta': 'Eficiência, disponibilidade e qualidade.'}
        if validate:
            validate(d)
        return d


class Juiz:
    def __init__(self, blocked=False, transient=False):
        self.blocked, self.transient, self.calls, self.payloads = blocked, transient, 0, []

    def json(self, system, user, validate=None, **kw):
        self.calls += 1
        self.payloads.append(json.loads(user))
        if self.blocked:
            raise ContentFiltered('lote bloqueado')
        if self.transient:
            self.transient = False
            raise RuntimeError('falha transitória do juiz')
        d = {'avaliacoes': [{'id': q['id'], 'veredito': 'correta', 'justificativa': 'Resposta confere.'} for q in json.loads(user)]}
        if validate:
            validate(d)
        return d


class AvaliacaoFinalTests(Fixture):
    def clients(self, a=None, b=None, judge=None):
        return {'resp_gpt-5-4-nano': a or Respondente(), 'resp_gpt-5-4': b or Respondente(), 'juiz': judge or Juiz()}

    def avaliar(self, clients, **kw):
        return avaliar(self.out, clientes=clients, progress=lambda *a, **k: None, **kw)

    def test_resposta_bloqueada_sem_juiz_e_sem_nota_tecnica(self):
        self.runner().run()
        a, judge = Respondente(blocked=True), Juiz()
        cl = self.clients(a=a, judge=judge)
        self.assertEqual(self.avaliar(cl), 0)
        d = M.read_json(self.out/'avaliacao/acuracia.json')['geral']['gpt-5-4-nano']
        self.assertEqual((d['processadas'], d['n'], d['nao_avaliadas'], d['bloqueios_respondente']), (1, 0, 1, 1))
        self.assertIsNone(d['acuracia'])
        self.assertEqual(judge.calls, 1)  # Só a resposta do outro modelo.
        self.assertEqual(self.avaliar(cl), 0)
        self.assertEqual((a.calls, judge.calls), (1, 1))
        row = M.ler_linhas(self.out/'avaliacao/avaliacoes.jsonl')[0]
        self.assertEqual(row['status_avaliacao_gpt-5-4-nano'], 'bloqueio_respondente')
        self.assertIsNone(row['veredito_gpt-5-4-nano'])
        self.assertEqual(M.read_json(self.out/'avaliacao/avaliacao_concluida.json')['status'], 'concluida_com_bloqueios')

    def test_juiz_bloqueado_registra_lote_sem_dividir_ou_reenviar(self):
        M.jsonl(self.input, [original(1), original(2)])
        self.runner().run()
        judge = Juiz(blocked=True)
        cl = self.clients(judge=judge)
        self.assertEqual(self.avaliar(cl, lote_juiz=2), 0)
        self.assertEqual(judge.calls, 2)
        self.assertEqual([len(p) for p in judge.payloads], [2, 2])
        for d in M.read_json(self.out/'avaliacao/acuracia.json')['geral'].values():
            self.assertEqual((d['processadas'], d['n'], d['bloqueios_juiz']), (2, 0, 2))
        self.assertEqual(self.avaliar(cl, lote_juiz=2), 0)
        self.assertEqual(judge.calls, 2)
        self.assertTrue((self.out/'avaliacao/avaliacao_concluida.json').exists())

    def test_falha_transitoria_resolvida_na_passagem_final_nao_impede_conclusao(self):
        self.runner().run()
        judge = Juiz(transient=True)
        self.assertEqual(self.avaliar(self.clients(judge=judge), lote_juiz=1), 0)
        for d in M.read_json(self.out/'avaliacao/acuracia.json')['geral'].values():
            self.assertEqual(d['n'], 1)
        self.assertEqual(M.read_json(self.out/'avaliacao/avaliacao_concluida.json')['status'], 'concluida')

    def test_outro_erro_nao_vira_bloqueio_ou_sucesso(self):
        self.runner().run()
        self.assertEqual(self.avaliar(self.clients(a=Respondente(error=True))), 2)
        self.assertFalse((self.out/'avaliacao/avaliacao_concluida.json').exists())
        d = M.read_json(self.out/'avaliacao/acuracia.json')['geral']['gpt-5-4-nano']
        self.assertEqual((d['processadas'], d['nao_avaliadas']), (0, 0))


if __name__ == '__main__':
    unittest.main()
