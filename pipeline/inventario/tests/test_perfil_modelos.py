"""Perfil misto: roteamento, orçamento concorrente, cache, logs e CLI sem rede."""
import contextlib
import io
import json
import tempfile
import unittest
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
from unittest.mock import Mock, patch

import numpy as np

from apoio import FakeLLM, corpus_fixture
from test_robustez import client_with, response
from pipeline.inventario.llm import BudgetExceeded, CallBudget, LLMClient
from pipeline.inventario.perfil_modelos import GPT, NANO, PROFILE, TAGS, StageLLM, resolve
from pipeline.inventario.run_inventario import main, parse


def mixed_routes():
    return resolve(parse(['--perfil-modelos', PROFILE]), GPT)


class PerfilModelos(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.root = Path(self.tmp.name)

    def router(self, max_calls=100, effects=None):
        self.sdks = {}

        def factory(model, effort, *args, **kwargs):
            sdk = client_with((effects or {}).get(model, lambda **kw: response({'ok': True})))
            self.sdks[model] = sdk
            return LLMClient(model, effort, *args, client=sdk, sleep=lambda _: None, **kwargs)

        router = StageLLM(mixed_routes(), self.root / 'cache.db', self.root / 'log.jsonl', max_calls,
                          client_factory=factory)
        self.addCleanup(router.close)
        return router

    def test_tabela_exata_e_retry_assuntos(self):
        routes = mixed_routes()
        self.assertEqual(set(routes), set(TAGS))
        for tag in TAGS:
            self.assertEqual(routes[tag], {'model': NANO if tag in ('assuntos', 'assuntos_retry', 'fatos') else GPT,
                                           'effort': 'low'})

    def test_incompativeis_falham_sem_fallback(self):
        for extra in (['--llm-provider', 'openai'], ['--llm-model', GPT], ['--effort', 'medium']):
            with self.subTest(extra=extra), self.assertRaises(ValueError):
                resolve(parse(['--perfil-modelos', PROFILE, *extra]), GPT)

    def test_modelo_unico_mantem_padrao_e_override(self):
        self.assertEqual(resolve(parse([]), GPT)['fatos'], {'model': GPT, 'effort': 'medium'})
        self.assertEqual(resolve(parse(['--effort', 'low']), NANO)['revisor'], {'model': NANO, 'effort': 'low'})

    def test_roteamento_log_e_uso_sem_contagem_dupla(self):
        llm = self.router()
        for tag in TAGS:
            llm.json('s', tag, tag=tag)
        self.assertEqual(self.sdks[NANO].chat.completions.create.call_count, 3)
        self.assertEqual(self.sdks[GPT].chat.completions.create.call_count, 4)
        self.assertEqual(llm.usage['calls'], 7)
        self.assertEqual(llm.usage['prompt_tokens'], 70)
        self.assertEqual(llm.budget.used, 7)
        rows = [json.loads(l) for l in (self.root / 'log.jsonl').read_text(encoding='utf-8').splitlines()]
        self.assertEqual(len(rows), 7)
        for row in rows:
            self.assertEqual(row['model'], llm.routes[row['tag']]['model'])
            self.assertEqual(row['effort'], 'low')
            self.assertEqual(row['provider'], 'azure')
            self.assertEqual(llm.usage_by_stage[row['tag']]['attempts'], 1)
            self.assertEqual(llm.usage_by_stage[row['tag']]['model'], row['model'])
        for sdk in self.sdks.values():
            self.assertTrue(all(c.kwargs['reasoning_effort'] == 'low'
                                for c in sdk.chat.completions.create.call_args_list))

    def test_etapa_desconhecida_falha_antes_da_api(self):
        llm = self.router()
        with self.assertRaisesRegex(ValueError, 'Etapa sem modelo'):
            llm.json('s', 'u', tag='extrator_com_typo')
        self.assertEqual(llm.budget.used, 0)

    def test_orcamento_global_inclui_reparo_e_cache_nao_consume(self):
        llm = self.router(max_calls=3, effects={NANO: [response({}, raw='JSON inválido'), response({'ok': True})]})
        llm.json('s', 'u', tag='fatos')
        llm.json('s', 'u', tag='fatos')  # cache Nano
        llm.json('s', 'u', tag='redator')  # mesmo prompt, outro modelo: outra entrada de cache
        llm.json('s', 'u', tag='redator')  # cache GPT
        with self.assertRaises(BudgetExceeded):
            llm.json('s', 'novo', tag='revisor')
        self.assertEqual(llm.budget.used, 3)
        self.assertEqual(llm.usage['cached'], 2)
        self.assertEqual(llm.usage_by_stage['fatos']['reparos'], 1)

    def test_orcamento_global_conta_erro_transitorio(self):
        class RateLimitError(Exception):
            status_code = 429
        llm = self.router(max_calls=1, effects={NANO: RateLimitError('aguarde')})
        with self.assertRaises(BudgetExceeded):
            llm.json('s', 'u', tag='fatos')
        with self.assertRaises(BudgetExceeded):
            llm.json('s', 'u', tag='redator')
        self.assertEqual(llm.usage['calls'], 0)
        self.assertEqual(llm.usage['errors'], 1)
        self.sdks[GPT].chat.completions.create.assert_not_called()

    def test_orcamento_e_log_com_workers(self):
        llm = self.router(max_calls=20)

        def job(i):
            try:
                llm.json('s', str(i), tag='fatos' if i % 2 else 'revisor')
                return True
            except BudgetExceeded:
                return False
        with ThreadPoolExecutor(max_workers=8) as pool:
            results = list(pool.map(job, range(60)))
        self.assertEqual(sum(results), 20)
        self.assertEqual(llm.budget.used, 20)
        self.assertEqual(llm.usage['calls'], 20)
        rows = [json.loads(l) for l in (self.root / 'log.jsonl').read_text(encoding='utf-8').splitlines()]
        self.assertEqual(len(rows), 20)
        self.assertEqual({r['model'] for r in rows}, {NANO, GPT})

    def test_budget_reservas_atomicas(self):
        budget = CallBudget(3)
        def reserve(_):
            try:
                budget.reserve()
                return 1
            except BudgetExceeded:
                return 0
        with ThreadPoolExecutor(max_workers=8) as pool:
            self.assertEqual(sum(pool.map(reserve, range(100))), 3)

    def test_close_dois_clientes_idempotente(self):
        clients = [Mock(), Mock()]
        llm = StageLLM(mixed_routes(), self.root/'c.db', self.root/'l.jsonl', 10,
                       client_factory=Mock(side_effect=clients))
        llm.close()
        llm.close()
        for c in clients:
            c.close.assert_called_once()

    def test_falha_construcao_fecha_primeiro(self):
        c = Mock()
        with self.assertRaisesRegex(RuntimeError, 'deployment'):
            StageLLM(mixed_routes(), self.root/'c.db', self.root/'l.jsonl', 10,
                     client_factory=Mock(side_effect=[c, RuntimeError('deployment ausente')]))
        c.close.assert_called_once()

    def test_close_tenta_todos_mesmo_com_erro(self):
        clients = [Mock(), Mock()]
        clients[0].close.side_effect = RuntimeError('close')
        llm = StageLLM(mixed_routes(), self.root/'c.db', self.root/'l.jsonl', 10,
                       client_factory=Mock(side_effect=clients))
        with self.assertRaises(RuntimeError):
            llm.close()
        clients[1].close.assert_called_once()

    def test_plan_misto_sem_cliente(self):
        manifest = corpus_fixture(self.root)
        with patch('pipeline.inventario.run_inventario.LLMClient') as cls, contextlib.redirect_stdout(io.StringIO()):
            result = main(['--perfil-modelos', PROFILE, '--plan', '--output', str(self.root/'out'),
                           '--topicos', 'Produção e Processo', 'Operações submarinas', 'Utilidades',
                           'Segurança Operacional', '--corpus-manifest', str(manifest), '--allow-sample-corpus'])
        self.assertEqual(result, {'subtopicos': 23, 'calls': 0})
        cls.assert_not_called()

    def test_check_api_misto_ambos_deployments_e_embedding_novo(self):
        clients = [Mock(), Mock()]
        for c in clients:
            c.json.return_value = {'ok': True}
        with patch('pipeline.inventario.run_inventario.LLMClient', side_effect=clients) as cls, \
             patch('pipeline.inventario.modelos.load_models') as loader, contextlib.redirect_stdout(io.StringIO()):
            emb = Mock()
            emb.impl.encode.return_value = np.ones((2, 3072), dtype=np.float32)
            loader.return_value = (emb, None)
            main(['--perfil-modelos', PROFILE, '--check-api', '--output', str(self.root/'out')])
        self.assertEqual([c.args[:2] for c in cls.call_args_list], [(NANO, 'low'), (GPT, 'low')])
        users = [c.json.call_args.args[1] for c in clients]
        self.assertNotEqual(users[0], users[1])
        emb.impl.encode.assert_called_once()
        self.assertFalse(emb.impl.encode.call_args.kwargs['usar_cache'])
        for c in clients:
            c.close.assert_called_once()
        emb.close.assert_called_once()

    def test_fluxo_completo_misto_e_configuracao_protegida(self):
        instances = []
        class TrackingFake(FakeLLM):
            def __init__(self, model, effort, *args, **kwargs):
                super().__init__()
                self.model, self.effort = model, effort
                self.tags = []
                instances.append(self)
            @property
            def usage_by_stage(self):
                return {tag: {'calls': self.tags.count(tag)} for tag in set(self.tags)}
            def json(self, *args, **kwargs):
                self.tags.append(kwargs['tag'])
                return super().json(*args, **kwargs)
        manifest = corpus_fixture(self.root)
        args = ['--perfil-modelos', PROFILE, '--corpus-manifest', str(manifest), '--allow-sample-corpus',
                '--topicos', 'Gestão do Desempenho Empresarial', '--output', str(self.root/'out'),
                '--embedder', 'hash', '--workers', '2']
        with patch('pipeline.inventario.run_inventario.LLMClient', TrackingFake), contextlib.redirect_stdout(io.StringIO()):
            result = main(args)
            with self.assertRaisesRegex(ValueError, 'Configuração mudou'):
                main([*args, '--perfil-modelos', 'unico', '--effort', 'low'])
        self.assertEqual(result['status'], 'concluido')
        self.assertEqual(len(instances), 2)
        self.assertTrue({'assuntos', 'fatos'} <= set(instances[0].tags))
        self.assertTrue({'conceitos', 'redator', 'revisor'} <= set(instances[1].tags))
        self.assertEqual(result['modelos_por_etapa'], mixed_routes())
        self.assertEqual(result['uso_llm']['calls'], sum(len(c.tags) for c in instances))
        self.assertEqual(result['uso_llm_por_etapa']['fatos']['model'], NANO)
        config = json.loads((self.root/'out/run_config.json').read_text(encoding='utf-8'))
        self.assertEqual(config['args']['effort'], 'low')
        self.assertEqual(config['modelos_por_etapa'], mixed_routes())

    def test_check_api_falha_segundo_deployment_fecha_recursos(self):
        clients = [Mock(), Mock()]
        clients[0].json.return_value = {'ok': True}
        clients[1].json.side_effect = RuntimeError('deployment GPT indisponível')
        with patch('pipeline.inventario.run_inventario.LLMClient', side_effect=clients), \
             patch('pipeline.inventario.modelos.load_models') as loader, contextlib.redirect_stdout(io.StringIO()):
            emb = Mock()
            loader.return_value = (emb, None)
            with self.assertRaisesRegex(RuntimeError, 'GPT indisponível'):
                main(['--perfil-modelos', PROFILE, '--check-api', '--output', str(self.root/'out')])
        for c in clients:
            c.close.assert_called_once()
        emb.close.assert_called_once()
        emb.impl.encode.assert_not_called()

    def test_retomada_assinatura_antiga_modelo_unico(self):
        from pipeline.inventario.textutil import sha
        manifest = corpus_fixture(self.root)
        args = ['--corpus-manifest', str(manifest), '--allow-sample-corpus', '--topicos',
                'Gestão do Desempenho Empresarial', '--output', str(self.root/'out'),
                '--embedder', 'hash', '--parar-apos', 'assuntos']
        with patch('pipeline.inventario.run_inventario.LLMClient', FakeLLM), contextlib.redirect_stdout(io.StringIO()):
            main(args)
            path = self.root/'out/run_config.json'
            config = json.loads(path.read_text(encoding='utf-8'))
            config['args'].pop('perfil_modelos')
            config.pop('modelos_por_etapa')
            identity = {k:v for k,v in config['args'].items() if k not in
                        ('workers','max_chamadas','parar_apos','plan','check_api','output',
                         'reaproveitar_de','max_falhas_consecutivas')}
            config['signature'] = sha(json.dumps([config['version'],config['model'],identity],sort_keys=True),40)
            path.write_text(json.dumps(config),encoding='utf-8')
            result = main(args)
        self.assertEqual(result['status'], 'concluido')


if __name__ == '__main__':
    unittest.main()
