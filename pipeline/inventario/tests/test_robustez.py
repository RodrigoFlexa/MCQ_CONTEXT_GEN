"""Regressões de revisão: sem rede, sem chaves e sem GPU."""
import json
import tempfile
import unittest
from pathlib import Path
from types import SimpleNamespace as NS
from unittest.mock import Mock, patch

import numpy as np

from pipeline.inventario import assuntos as A, consolidacao as C, extracao as X, fichas as F, varredura as V
from pipeline.inventario.llm import LLMClient, BudgetExceeded
from pipeline.inventario.modelos import AzureEmbedder, EmbeddingCache, HashEmbedder, _device
from pipeline.inventario.run_inventario import main, parse, validate_args
from pipeline.inventario.textutil import quote_supported, sha


def response(data, finish='stop'):
    return NS(choices=[NS(message=NS(content=json.dumps(data)), finish_reason=finish)],
              usage=NS(prompt_tokens=10, completion_tokens=20))


def unit(uid='u1', assertion='Disponibilidade = MTBF/(MTBF+MTTR).'):
    return {'uid': uid, 'assuntos': ['a01'], 'tipo': 'formula_calculo', 'afirmacao': assertion,
            'condicoes': 'MTBF é o tempo médio de operação', 'aplicabilidade': 'transferivel', 'valor': 'alto',
            'citacao': 'O tempo médio de operação é usado no cálculo da disponibilidade.',
            'entidades': ['MTBF'], 'fonte': {'document_id': uid, 'collection': 'anp', 'title': uid}}


class Robustez(unittest.TestCase):
    def test_defaults_azure(self):
        args = parse([])
        self.assertEqual((args.llm_provider, args.embedder, args.reranker),
                         ('azure', 'embedding-3-large-global', 'none'))

    def test_limite_encerra_leitura_por_colecao(self):
        read = []
        def rows(collections):
            for i in range(100):
                read.append(i)
                yield {'collection':collections[0]['id'], 'page':i}
        with patch('pipeline.domain_corpora.manifest.iter_units', rows):
            result = list(V.iter_limited_units([{'id':'anp'}, {'id':'hse'}], 3))
        self.assertEqual(len(result), 6)
        self.assertEqual(len(read), 6)

    def test_parametros_invalidos(self):
        for options in (['--workers', '0'], ['--chunk-stride', '900'], ['--min-rerank', 'nan'],
                        ['--limite-unidades', '-1'], ['--plan', '--check-api']):
            with self.subTest(options=options), self.assertRaises(ValueError):
                validate_args(parse(options))

    def test_local_nao_aceita_cpu(self):
        with self.assertRaises(ValueError):
            _device('cpu')

    def test_citacao_numero_alterado(self):
        text = 'A pressão máxima admissível de operação é de 15 bar durante o teste.'
        self.assertFalse(quote_supported(text.replace('15', '50'), text))

    def test_citacao_negacao_alterada(self):
        text = 'A válvula não deve ser aberta durante a manutenção do sistema.'
        self.assertFalse(quote_supported(text.replace('não ', ''), text))

    def test_citacao_operador_alterado(self):
        self.assertFalse(quote_supported('A pressão de operação deve ser >= 15 bar.',
                                         'A pressão de operação deve ser <= 15 bar.'))

    def test_citacao_contigua(self):
        self.assertFalse(quote_supported('A válvula pode ser aberta com pressão elevada no sistema',
                                         'A válvula pode ser aberta após despressurizar. É proibida pressão elevada no sistema'))

    def test_assunto_inventado_rejeitado(self):
        with self.assertRaises(ValueError):
            A.validate_response('gestão de riscos')({'assuntos': [{'texto': 'economia de custos',
                'consulta_pt': 'custos', 'consulta_en': 'costs', 'termos_pt': [], 'termos_en': []}]})

    def test_assunto_nao_pode_ser_fragmento_de_palavra(self):
        with self.assertRaises(ValueError):
            A.validate_response('despressurização de sistemas')({'assuntos':[{'texto':'pressurização de sistemas',
                'consulta_pt':'pressurização', 'consulta_en':'pressurization', 'termos_pt':[], 'termos_en':[]}]})

    def test_azure_ausente_nao_migra_para_openai(self):
        from azure_openai_backend import AzureSettings
        with tempfile.TemporaryDirectory() as tmp, patch('openai.OpenAI') as public:
            with self.assertRaises(RuntimeError):
                LLMClient('gpt-5-4-petrobras', 'medium', Path(tmp)/'c.db', Path(tmp)/'l.jsonl',
                          settings=AzureSettings())
            public.assert_not_called()

    def test_generico_string_rejeitado(self):
        with self.assertRaises(ValueError):
            A.validate_response('gestão de riscos')({'assuntos': [{'texto': 'gestão de riscos', 'generico': 'false',
                'consulta_pt': 'riscos', 'consulta_en': 'risks', 'termos_pt': [], 'termos_en': []}]})

    def test_extracao_classificacao_invalida(self):
        with self.assertRaises(ValueError):
            X._validate({'unidades': [{'afirmacao': 'Uma afirmação', 'tipo': 'inventado'}]})

    def test_nao_junta_paginas_ausentes(self):
        rows = [{'collection': 'anp', 'document_id': 'd', 'text': ('palavra ' * 100), 'page': p} for p in (1, 9)]
        wins = list(V.windows(rows))
        self.assertEqual(len(wins), 2)
        self.assertTrue(all(r['page_ini'] == r['page_fim'] for _, _, r in wins))

    def test_assinatura_manifesto_conteudo(self):
        with tempfile.TemporaryDirectory() as tmp:
            p = Path(tmp) / 'manifest.json'
            p.write_text('{"sha256":"a"}')
            a = V.signature([], p, {})
            p.write_text('{"sha256":"b"}')
            self.assertNotEqual(a, V.signature([], p, {}))

    def test_cache_vetorial_preserva_normalizacao(self):
        with tempfile.TemporaryDirectory() as tmp:
            p = Path(tmp) / 'cache.npz'
            emb = HashEmbedder()
            cache = EmbeddingCache(p, 'hash')
            original = cache.encode(emb, ['disponibilidade MTBF manutenção'])
            cache.save()
            reloaded = EmbeddingCache(p, 'hash').encode(emb, ['disponibilidade MTBF manutenção'])
            np.testing.assert_allclose(reloaded, original, atol=1e-6)
            np.testing.assert_allclose(np.linalg.norm(reloaded, axis=1), 1, atol=1e-6)

    def test_cache_llm_valida_e_distingue_orcamento(self):
        with tempfile.TemporaryDirectory() as tmp:
            client = NS(chat=NS(completions=NS(create=Mock(return_value=response({'ok': True})))))
            llm = LLMClient('gpt-5-4-petrobras', 'medium', Path(tmp)/'c.db', Path(tmp)/'l.jsonl', client=client)
            try:
                llm.json('s', 'u', max_tokens=200)
                validator = Mock()
                llm.json('s', 'u', max_tokens=200, validate=validator)
                validator.assert_called_once_with({'ok': True})
                llm.json('s', 'u', max_tokens=300)
                self.assertEqual(client.chat.completions.create.call_count, 2)
                self.assertEqual(client.chat.completions.create.call_args.kwargs['reasoning_effort'], 'medium')
            finally:
                llm.close()

    def test_orcamento_para_antes_do_pedido(self):
        with tempfile.TemporaryDirectory() as tmp:
            client = NS(chat=NS(completions=NS(create=Mock())))
            llm = LLMClient('gpt-5-4-petrobras', 'medium', Path(tmp)/'c.db', Path(tmp)/'l.jsonl',
                            max_calls=0, client=client)
            try:
                with self.assertRaises(BudgetExceeded):
                    llm.json('s', 'u')
                client.chat.completions.create.assert_not_called()
            finally:
                llm.close()

    def test_erro_permanente_nao_repete(self):
        class PermissionDeniedError(Exception):
            status_code = 403
        with tempfile.TemporaryDirectory() as tmp, patch('pipeline.inventario.llm.time.sleep') as sleep:
            client = NS(chat=NS(completions=NS(create=Mock(side_effect=PermissionDeniedError('negado')))))
            llm = LLMClient('gpt-5-4-petrobras', 'medium', Path(tmp)/'c.db', Path(tmp)/'l.jsonl', client=client)
            try:
                with self.assertRaises(PermissionDeniedError):
                    llm.json('s', 'u')
                self.assertEqual(client.chat.completions.create.call_count, 1)
                sleep.assert_not_called()
            finally:
                llm.close()

    def test_429_repete_sem_remover_effort(self):
        class RateLimitError(Exception):
            status_code = 429
        with tempfile.TemporaryDirectory() as tmp, patch('pipeline.inventario.llm.time.sleep') as sleep:
            client = NS(chat=NS(completions=NS(create=Mock(side_effect=[RateLimitError(), response({'ok':True})]))))
            llm = LLMClient('gpt-5-4-petrobras', 'medium', Path(tmp)/'c.db', Path(tmp)/'l.jsonl', client=client)
            try:
                self.assertEqual(llm.json('s', 'u'), {'ok':True})
                self.assertEqual(client.chat.completions.create.call_count, 2)
                self.assertTrue(all(c.kwargs['reasoning_effort']=='medium'
                                    for c in client.chat.completions.create.call_args_list))
                sleep.assert_called_once()
            finally:
                llm.close()

    def test_cache_invalido_e_refeito(self):
        with tempfile.TemporaryDirectory() as tmp:
            client = NS(chat=NS(completions=NS(create=Mock(side_effect=[response({'ok':False}), response({'ok':True})]))))
            llm = LLMClient('gpt-5-4-petrobras', 'medium', Path(tmp)/'c.db', Path(tmp)/'l.jsonl', client=client)
            try:
                llm.json('s', 'u')
                def validate(data):
                    if data.get('ok') is not True:
                        raise ValueError('inválido')
                self.assertEqual(llm.json('s', 'u', validate=validate), {'ok':True})
                self.assertEqual(client.chat.completions.create.call_count, 2)
            finally:
                llm.close()

    def test_resposta_truncada_nao_cacheada(self):
        with tempfile.TemporaryDirectory() as tmp, patch('pipeline.inventario.llm.time.sleep'):
            client = NS(chat=NS(completions=NS(create=Mock(return_value=response({'ok': True}, 'length')))))
            llm = LLMClient('gpt-5-4-petrobras', 'medium', Path(tmp)/'c.db', Path(tmp)/'l.jsonl', client=client)
            try:
                with self.assertRaises(RuntimeError):
                    llm.json('s', 'u')
                self.assertEqual(llm.db.execute('SELECT count(*) FROM cache').fetchone()[0], 0)
                self.assertEqual(llm.usage['prompt_tokens'], 60)
            finally:
                llm.close()

    def test_azure_cliente_usa_gateway_e_certificado(self):
        from azure_openai_backend import AzureSettings
        settings = AzureSettings(azure_endpoint='https://gateway.example/openai/v1', azure_api_key='test-key',
                                 azure_api_version='2024-10-21', use_base_url=True, ca_bundle='test-ca.pem')
        with tempfile.TemporaryDirectory() as tmp, patch('openai.AzureOpenAI') as cls, \
             patch('azure_openai_backend.AzureOpenAIBackend._build_http_client', return_value='http-tls'):
            llm = LLMClient('gpt-5-4-petrobras', 'medium', Path(tmp)/'c.db', Path(tmp)/'l.jsonl', settings=settings)
            try:
                self.assertEqual(cls.call_args.kwargs['base_url'], settings.azure_endpoint)
                self.assertEqual(cls.call_args.kwargs['http_client'], 'http-tls')
                self.assertNotIn('test-key', json.dumps(llm.identity))
            finally:
                llm.close()

    def test_azure_embedding_integral_e_cache(self):
        class Tokenizer:
            def encode(self, text, **kwargs):
                return list(range(len(text.split())))
        class Backend:
            settings = None
            def __init__(self):
                self.inputs = []
            def create(self, inputs):
                self.inputs.extend(inputs)
                return NS(data=[NS(index=i, embedding=[1.0] + [0.0]*3071) for i in range(len(inputs))])
        with tempfile.TemporaryDirectory() as tmp:
            b = Backend()
            emb = AzureEmbedder(tmp, backend=b, tokenizer=Tokenizer())
            try:
                texts = ['palavra ' * 10000, 'texto curto']
                vectors = emb.encode(texts)
                self.assertEqual(vectors.shape, (2, 3072))
                self.assertEqual(len(b.inputs), 3)
                self.assertTrue(all(len(x) <= 8192 for x in b.inputs))
                self.assertEqual(b.inputs[1][0], 8176)
                emb.encode(texts)
                self.assertEqual(len(b.inputs), 3)
            finally:
                emb.close()

    def test_conflito_preserva_as_duas_afirmacoes(self):
        class LLM:
            def json(self, system, user, **kwargs):
                data = {'grupos': [{'grupo': 'g1', 'status': 'conflito', 'nota': 'Convenções incompatíveis'}]}
                kwargs['validate'](data)
                return data
        units = [unit(), unit('u2', 'Disponibilidade = MTTF/MTBF.')]
        result, _ = C.consolidate(LLM(), 's1', units, np.array([[1., 0.], [1., 0.]]))
        self.assertEqual(len(result[0]['unidades_originais']), 2)
        self.assertFalse(result[0]['utilizavel_para_qa'])

    def test_fusao_sem_membros_rejeitada(self):
        class LLM:
            def json(self, system, user, **kwargs):
                data = {'grupos': [{'grupo': 'g1', 'status': 'equivalentes', 'membros': [], 'afirmacao': 'nova'}]}
                kwargs['validate'](data)
                return data
        with self.assertRaises(ValueError):
            C.consolidate(LLM(), 's1', [unit(), unit('u2')], np.array([[1., 0.], [1., 0.]]))

    def test_conflito_nao_conta_como_cobertura(self):
        with tempfile.TemporaryDirectory() as tmp:
            cons = C._from_members([unit(), unit('u2')], 's1', 1, 'conflito', nota='definições diferentes')
            rows = F.write_subtopic(Path(tmp)/'sub', {'key':'s1', 'topico':'KPI', 'subtopico':'KPI'},
                [{'id':'a01', 'texto':'disponibilidade', 'generico':False, 'literal':True,
                  'consulta_pt':'disponibilidade', 'consulta_en':'availability'}], [cons], {}, {})
            self.assertEqual(rows[0]['unidades'], 0)
            self.assertEqual(rows[0]['conflitos'], 1)
            ficha = json.loads((Path(tmp)/'sub/fichas/a01.json').read_text(encoding='utf-8'))
            self.assertEqual(ficha['unidades'], [])
            self.assertEqual(len(ficha['divergencias']), 1)


if __name__ == '__main__':
    unittest.main()
