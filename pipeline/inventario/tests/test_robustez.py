"""Cliente LLM, argumentos, corpora e embeddings: sem rede, sem chaves e sem GPU."""
import json
import tempfile
import unittest
from pathlib import Path
from types import SimpleNamespace as NS
from unittest.mock import Mock, patch

import numpy as np

from pipeline.inventario import assuntos as A, varredura as V
from pipeline.inventario.llm import BudgetExceeded, CallFailed, ContentFiltered, LLMClient
from pipeline.inventario.modelos import AzureEmbedder, EmbeddingCache, HashEmbedder, _device
from pipeline.inventario.run_inventario import parse, validate_args
from pipeline.inventario.textutil import quote_supported, unsupported_numbers


def response(data, finish='stop', raw=None):
    content = raw if raw is not None else json.dumps(data)
    return NS(choices=[NS(message=NS(content=content), finish_reason=finish)],
              usage=NS(prompt_tokens=10, completion_tokens=20))


def client_with(side_effect):
    return NS(chat=NS(completions=NS(create=Mock(side_effect=side_effect))))


class LLMBase(unittest.TestCase):
    def make(self, side_effect, **kw):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.client = client_with(side_effect)
        self.sleep = Mock()
        llm = LLMClient('gpt-5-4-petrobras', 'medium', Path(self.tmp.name) / 'c.db', Path(self.tmp.name) / 'l.jsonl',
                        client=self.client, sleep=self.sleep, **kw)
        self.addCleanup(llm.close)
        return llm

    def log(self):
        return [json.loads(l) for l in (Path(self.tmp.name) / 'l.jsonl').read_text(encoding='utf-8').splitlines()]


class ClienteLLM(LLMBase):
    def test_cache_valida_e_distingue_max_tokens(self):
        llm = self.make([response({'ok': True}), response({'ok': True})])
        llm.json('s', 'u', max_tokens=200)
        validator = Mock()
        llm.json('s', 'u', max_tokens=200, validate=validator)
        validator.assert_called_once_with({'ok': True})
        llm.json('s', 'u', max_tokens=300)
        self.assertEqual(self.client.chat.completions.create.call_count, 2)
        self.assertEqual(self.client.chat.completions.create.call_args.kwargs['reasoning_effort'], 'medium')

    def test_orcamento_para_antes_do_pedido(self):
        llm = self.make([], max_calls=0)
        with self.assertRaises(BudgetExceeded):
            llm.json('s', 'u')
        self.client.chat.completions.create.assert_not_called()

    def test_erro_permanente_nao_repete(self):
        class PermissionDeniedError(Exception):
            status_code = 403
        llm = self.make(PermissionDeniedError('negado'))
        with self.assertRaises(PermissionDeniedError):
            llm.json('s', 'u')
        self.assertEqual(self.client.chat.completions.create.call_count, 1)
        self.sleep.assert_not_called()

    def test_429_espera_e_repete(self):
        class RateLimitError(Exception):
            status_code = 429
        llm = self.make([RateLimitError('lento'), response({'ok': True})])
        self.assertEqual(llm.json('s', 'u'), {'ok': True})
        self.assertEqual(self.client.chat.completions.create.call_count, 2)
        self.sleep.assert_called_once()

    def test_filtro_de_conteudo_no_prompt_nao_repete(self):
        class BadRequestError(Exception):
            status_code = 400
            body = {'error': {'code': 'content_filter', 'message': 'The response was filtered'}}
        llm = self.make(BadRequestError('Error code: 400'))
        with self.assertRaises(ContentFiltered):
            llm.json('s', 'u', item='trecho-1')
        self.assertEqual(self.client.chat.completions.create.call_count, 1)
        self.assertEqual(self.log()[-1]['kind'], 'filtro_conteudo')
        self.assertEqual(llm.usage['filtro_conteudo'], 1)

    def test_filtro_de_conteudo_na_resposta(self):
        llm = self.make([response(None, finish='content_filter', raw='')])
        with self.assertRaises(ContentFiltered):
            llm.json('s', 'u')
        self.assertEqual(self.client.chat.completions.create.call_count, 1)

    def test_validacao_devolve_erro_ao_modelo(self):
        llm = self.make([response({'ok': False}), response({'ok': True})])

        def validate(data):
            if data.get('ok') is not True:
                raise ValueError('ok deve ser true')
        self.assertEqual(llm.json('s', 'u', validate=validate), {'ok': True})
        second = self.client.chat.completions.create.call_args_list[1].kwargs['messages']
        self.assertEqual(second[2]['role'], 'assistant')
        self.assertIn('ok deve ser true', second[3]['content'])
        self.assertEqual(llm.usage['reparos'], 1)
        # A resposta reparada fica no cache da chave original.
        self.assertEqual(llm.json('s', 'u', validate=validate), {'ok': True})
        self.assertEqual(self.client.chat.completions.create.call_count, 2)

    def test_json_quebrado_tambem_e_reparado(self):
        llm = self.make([response(None, raw='{"ok": tru'), response({'ok': True})])
        self.assertEqual(llm.json('s', 'u'), {'ok': True})

    def test_truncada_aumenta_tokens_e_falha_com_motivo(self):
        llm = self.make([response({'ok': True}, 'length')] * 6, max_tokens_cap=1000)
        with self.assertRaises(CallFailed) as ctx:
            llm.json('s', 'u', max_tokens=500)
        self.assertEqual(ctx.exception.kind, 'truncada')
        tokens = [c.kwargs['max_completion_tokens'] for c in self.client.chat.completions.create.call_args_list]
        self.assertEqual(tokens, [500, 800, 1000])
        self.assertEqual(llm.db.execute('SELECT count(*) FROM cache').fetchone()[0], 0)

    def test_falha_registra_mensagem(self):
        class BadRequestError(Exception):
            status_code = 400
        llm = self.make(BadRequestError('context_length_exceeded: muito longo'))
        with self.assertRaises(CallFailed) as ctx:
            llm.json('s', 'u', tag='fatos', item='x')
        self.assertIn('context_length_exceeded', str(ctx.exception))
        self.assertIn('context_length_exceeded', self.log()[0]['message'])
        self.assertEqual(self.client.chat.completions.create.call_count, 2)  # 400 comum: não insiste

    def test_cache_invalido_e_refeito(self):
        llm = self.make([response({'ok': False}), response({'ok': True})])
        llm.json('s', 'u')

        def validate(data):
            if data.get('ok') is not True:
                raise ValueError('inválido')
        self.assertEqual(llm.json('s', 'u', validate=validate), {'ok': True})

    def test_azure_ausente_nao_migra_para_openai(self):
        from azure_openai_backend import AzureSettings
        with tempfile.TemporaryDirectory() as tmp, patch('openai.OpenAI') as public:
            with self.assertRaises(RuntimeError):
                LLMClient('gpt-5-4-petrobras', 'medium', Path(tmp) / 'c.db', Path(tmp) / 'l.jsonl', settings=AzureSettings())
            public.assert_not_called()

    def test_azure_cliente_usa_gateway_e_certificado(self):
        from azure_openai_backend import AzureSettings
        settings = AzureSettings(azure_endpoint='https://gateway.example/openai/v1', azure_api_key='test-key',
                                 azure_api_version='2024-10-21', use_base_url=True, ca_bundle='test-ca.pem')
        with tempfile.TemporaryDirectory() as tmp, patch('openai.AzureOpenAI') as cls, \
             patch('azure_openai_backend.AzureOpenAIBackend._build_http_client', return_value='http-tls'):
            llm = LLMClient('gpt-5-4-petrobras', 'medium', Path(tmp) / 'c.db', Path(tmp) / 'l.jsonl', settings=settings)
            try:
                self.assertEqual(cls.call_args.kwargs['base_url'], settings.azure_endpoint)
                self.assertEqual(cls.call_args.kwargs['http_client'], 'http-tls')
                self.assertNotIn('test-key', json.dumps(llm.identity))
            finally:
                llm.close()


class Argumentos(unittest.TestCase):
    def test_defaults_azure(self):
        args = parse([])
        self.assertEqual((args.llm_provider, args.embedder, args.reranker, args.workers),
                         ('azure', 'embedding-3-large-global', 'none', 8))

    def test_parametros_invalidos(self):
        for options in (['--workers', '0'], ['--chunk-stride', '900'], ['--min-score', 'nan'], ['--rel-score', '2'],
                        ['--limite-unidades', '-1'], ['--limite-assuntos', '0'], ['--plan', '--check-api'],
                        ['--max-falhas-consecutivas', '0']):
            with self.subTest(options=options), self.assertRaises(ValueError):
                validate_args(parse(options))

    def test_local_nao_aceita_cpu(self):
        with self.assertRaises(ValueError):
            _device('cpu')


class TextoECorpora(unittest.TestCase):
    def test_citacao_numero_negacao_operador_contiguidade(self):
        text = 'A pressão máxima admissível de operação é de 15 bar durante o teste.'
        self.assertTrue(quote_supported('pressão máxima admissível de operação é de 15 bar', text))
        self.assertFalse(quote_supported(text.replace('15', '50'), text))
        neg = 'A válvula não deve ser aberta durante a manutenção do sistema.'
        self.assertFalse(quote_supported(neg.replace('não ', ''), neg))
        self.assertFalse(quote_supported('A pressão de operação deve ser >= 15 bar.', 'A pressão de operação deve ser <= 15 bar.'))

    def test_numeros_normalizados(self):
        src = 'volume útil de 1 050 litros, vazão de 8,33 m3/h; CO 2; 2.500 kPa; H<NUMBER>S'
        self.assertEqual(unsupported_numbers('1.050 L, 8.33 m³/h, 2500 kPa, CO2', [src]), [])
        self.assertEqual(unsupported_numbers('70 bar e 2,5 MPa', [src]), ['2,5', '70'])

    def test_limite_encerra_leitura_por_colecao(self):
        read = []

        def rows(collections):
            for i in range(100):
                read.append(i)
                yield {'collection': collections[0]['id'], 'page': i}
        with patch('pipeline.domain_corpora.manifest.iter_units', rows):
            result = list(V.iter_limited_units([{'id': 'anp'}, {'id': 'hse'}], 3))
        self.assertEqual((len(result), len(read)), (6, 6))

    def test_nao_junta_paginas_ausentes(self):
        rows = [{'collection': 'anp', 'document_id': 'd', 'text': ('palavra ' * 100), 'page': p} for p in (1, 9)]
        wins = list(V.windows(rows))
        self.assertEqual(len(wins), 2)

    def test_assinatura_manifesto_conteudo(self):
        with tempfile.TemporaryDirectory() as tmp:
            p = Path(tmp) / 'manifest.json'
            p.write_text('{"sha256":"a"}')
            a = V.signature([], p, {})
            p.write_text('{"sha256":"b"}')
            self.assertNotEqual(a, V.signature([], p, {}))

    def test_assunto_literal(self):
        with self.assertRaises(ValueError):
            A.validate_response('gestão de riscos')({'assuntos': [{'texto': 'economia de custos', 'consulta_pt': 'c',
                                                                   'consulta_en': 'c', 'termos_pt': [], 'termos_en': []}]})
        with self.assertRaises(ValueError):
            A.validate_response('despressurização de sistemas')({'assuntos': [{'texto': 'pressurização de sistemas',
                'consulta_pt': 'p', 'consulta_en': 'p', 'termos_pt': [], 'termos_en': []}]})


class Embeddings(unittest.TestCase):
    def test_cache_vetorial_preserva_normalizacao(self):
        with tempfile.TemporaryDirectory() as tmp:
            p = Path(tmp) / 'cache.npz'
            emb = HashEmbedder()
            original = EmbeddingCache(p, 'hash').encode(emb, ['disponibilidade MTBF manutenção'])
            cache = EmbeddingCache(p, 'hash')
            cache.encode(emb, ['disponibilidade MTBF manutenção'])
            cache.save()
            reloaded = EmbeddingCache(p, 'hash').encode(emb, ['disponibilidade MTBF manutenção'])
            np.testing.assert_allclose(reloaded, original, atol=1e-6)

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
                return NS(data=[NS(index=i, embedding=[1.0] + [0.0] * 3071) for i in range(len(inputs))])
        with tempfile.TemporaryDirectory() as tmp:
            b = Backend()
            emb = AzureEmbedder(tmp, backend=b, tokenizer=Tokenizer())
            try:
                texts = ['palavra ' * 10000, 'texto curto']
                self.assertEqual(emb.encode(texts).shape, (2, 3072))
                self.assertEqual(len(b.inputs), 3)
                emb.encode(texts)
                self.assertEqual(len(b.inputs), 3)
            finally:
                emb.close()


if __name__ == '__main__':
    unittest.main()
