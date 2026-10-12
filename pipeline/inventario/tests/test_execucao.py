"""Executa a CLI inteira sobre cinco coleções pequenas e serviços simulados."""
import contextlib
import hashlib
import io
import json
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch
from unittest.mock import Mock
from types import SimpleNamespace
import numpy as np

from pipeline.inventario import assuntos as A, extracao as X, consolidacao as C, revisao as R
from pipeline.inventario.locking import output_lock
from pipeline.inventario.run_inventario import main

TOPIC = 'Gestão do Desempenho Empresarial (KPI)'
SOURCE = ('O backlog de manutenção corresponde ao conjunto de ordens de serviço pendentes. '
          'A priorização depende da criticidade dos ativos e do risco operacional. ')


class FakeLLM:
    fail_extraction = False
    def __init__(self, *args, **kwargs):
        self.usage = {'calls':0, 'cached':0, 'prompt_tokens':0, 'completion_tokens':0, 'errors':0}
    def close(self):
        pass
    def json(self, system, user, **kwargs):
        self.usage['calls'] += 1
        if system == A.SYSTEM:
            phrase = user.split('"""')[1]
            data = {'assuntos': [{'texto':phrase, 'generico':False, 'consulta_pt':'backlog de manutenção',
                     'consulta_en':'maintenance backlog', 'termos_pt':['backlog'], 'termos_en':['maintenance backlog']}]}
        elif system == X.SYSTEM:
            if self.fail_extraction:
                raise RuntimeError('indisponibilidade simulada')
            data = {'unidades': [{'tipo':'definicao', 'afirmacao':'Backlog reúne ordens de serviço pendentes.',
                'condicoes':'', 'entidades':['backlog'], 'assuntos':['a01'], 'aplicabilidade':'transferivel',
                'valor_para_pergunta':'alto',
                'carater_avaliativo':'conhecimento_profissional','alvo_qa':'Definir backlog de manutenção.',
                'citacao':'O backlog de manutenção corresponde ao conjunto de ordens de serviço pendentes.'}]}
        elif system == C.SYSTEM:
            data = {'grupos':[{'grupo':g['grupo'], 'status':'complementares'} for g in json.loads(user)]}
        elif system == R.SYSTEM:
            batch=json.loads(user)['unidades']
            data={'pareceres':[{'uid':u['uid'],'decisao':'aprovar','motivo':'Pertinente e consistente.',
                               'carater_avaliativo':u['carater_avaliativo'],'alvo_qa':u['alvo_qa'],
                               'base':'fonte_original','referencias':[],'suporte_citacao':True,
                               'unidade':{k:u[k] for k in R.FIELDS}} for u in batch]}
        else:
            raise AssertionError('Chamada inesperada')
        if system == X.SYSTEM:
            for u in data['unidades']:
                u['redacao']={'ajuste':'nenhum','afirmacao_original':u['afirmacao'],
                              'condicoes_originais':u['condicoes'],'base':'fonte_original',
                              'motivo':'','referencias':[],'suporte_citacao':True}
        kwargs['validate'](data)
        return data


def fixture(root):
    collections = []
    for c in ('petroles', 'anp', 'hse', 'bsee', 'regis'):
        path = root / f'{c}.jsonl'
        row = {'collection':c, 'document_id':c+'-1', 'title':c+'-1.pdf', 'language':'pt',
               'jurisdiction':'BR', 'page':1, 'text':SOURCE*10}
        path.write_text(json.dumps(row, ensure_ascii=False)+'\n', encoding='utf-8')
        collections.append({'id':c, 'documents':1, 'format':'pages_jsonl', 'path':path.name,
                            'sha256':hashlib.sha256(path.read_bytes()).hexdigest()})
    path = root / 'manifest.json'
    path.write_text(json.dumps({'schema':'petroquest-domain-corpora-v1', 'ready':True,
                               'sample':True, 'collections':collections}), encoding='utf-8')
    return path


class Execucao(unittest.TestCase):
    def options(self, manifest, out):
        return ['--corpus-manifest', str(manifest), '--allow-sample-corpus', '--topicos', TOPIC,
                '--output', str(out), '--embedder', 'hash', '--min-rerank', '0', '--workers', '2']

    def test_topico_documentos_e_retomada(self):
        with tempfile.TemporaryDirectory() as tmp, patch('pipeline.inventario.run_inventario.LLMClient', FakeLLM), \
             contextlib.redirect_stdout(io.StringIO()):
            root = Path(tmp)
            manifest = fixture(root)
            out = root/'output'
            result = main(self.options(manifest, out))
            self.assertEqual(result['assuntos'], 1)
            docs = json.loads((out/'documentos_topicos.json').read_text(encoding='utf-8'))
            self.assertEqual([d['topico'] for d in docs], [TOPIC])
            self.assertIn('Backlog reúne', (out/docs[0]['arquivo']).read_text(encoding='utf-8'))
            self.assertFalse((out/'questoes_qa.jsonl').exists())
            drafts=json.loads((out/'resumo_redacao.json').read_text(encoding='utf-8'))
            self.assertTrue(all(x['nenhum']>0 and x['tecnico']==0 for x in drafts.values()))
            second = main(self.options(manifest, out))
            self.assertEqual(second['assuntos'], 1)
            self.assertEqual(len(list((out/'subtopicos').iterdir())), 1)
            with self.assertRaises(ValueError):
                main(self.options(manifest, out) + ['--chunk-words', '400'])

    def test_falha_extracao_nao_vira_sem_contexto(self):
        with tempfile.TemporaryDirectory() as tmp, patch('pipeline.inventario.run_inventario.LLMClient', FakeLLM), \
             patch.object(FakeLLM, 'fail_extraction', True), contextlib.redirect_stdout(io.StringIO()):
            root = Path(tmp)
            manifest = fixture(root)
            out = root/'output'
            with self.assertRaisesRegex(RuntimeError, 'extrações falharam'):
                main(self.options(manifest, out))
            self.assertTrue((out/'falhas_extracao.json').exists())
            self.assertFalse((out/'assuntos_para_geracao.jsonl').exists())
            self.assertFalse((out/'documentos_topicos.json').exists())

    def test_corpus_corrompido_falha_antes_llm(self):
        with tempfile.TemporaryDirectory() as tmp, patch('pipeline.inventario.run_inventario.LLMClient') as llm, \
             contextlib.redirect_stdout(io.StringIO()):
            root = Path(tmp)
            manifest = fixture(root)
            (root/'anp.jsonl').write_text('modificado', encoding='utf-8')
            with self.assertRaisesRegex(ValueError, 'corrompido'):
                main(self.options(manifest, root/'output'))
            llm.assert_not_called()

    def test_corpus_novo_exige_nova_saida(self):
        with tempfile.TemporaryDirectory() as tmp, patch('pipeline.inventario.run_inventario.LLMClient', FakeLLM), \
             contextlib.redirect_stdout(io.StringIO()):
            root = Path(tmp)
            manifest = fixture(root)
            out = root/'output'
            main(self.options(manifest, out))
            data = json.loads(manifest.read_text(encoding='utf-8'))
            data['updated_at'] = 'nova versão'
            manifest.write_text(json.dumps(data), encoding='utf-8')
            with self.assertRaisesRegex(ValueError, 'corpora mudaram'):
                main(self.options(manifest, out))

    def test_plano_nao_chama_servicos(self):
        with tempfile.TemporaryDirectory() as tmp, patch('pipeline.inventario.run_inventario.LLMClient') as llm, \
             contextlib.redirect_stdout(io.StringIO()):
            root = Path(tmp)
            result = main(self.options(fixture(root), root/'output') + ['--plan'])
            self.assertEqual(result, {'subtopicos':1, 'calls':0})
            llm.assert_not_called()

    def test_impede_execucao_concorrente_mesma_saida(self):
        with tempfile.TemporaryDirectory() as tmp:
            with output_lock(tmp):
                with self.assertRaisesRegex(RuntimeError, 'Outra execução'):
                    with output_lock(tmp):
                        pass
            with output_lock(tmp):
                pass

    def test_check_api_forca_pedidos_novos(self):
        with tempfile.TemporaryDirectory() as tmp, \
             patch('pipeline.inventario.run_inventario.LLMClient') as llm_cls, \
             patch('pipeline.inventario.modelos.load_models') as loader, \
             contextlib.redirect_stdout(io.StringIO()):
            llm = llm_cls.return_value
            llm.json.return_value = {'ok':True}
            emb = Mock()
            emb.impl.encode.return_value = np.ones((2, 3072), dtype=np.float32)
            loader.return_value = (emb, None)
            args = ['--output', tmp, '--topicos', TOPIC, '--check-api']
            main(args)
            main(args)
            self.assertEqual(emb.impl.encode.call_count, 2)
            self.assertTrue(all(c.kwargs['usar_cache'] is False for c in emb.impl.encode.call_args_list))
            users = [c.args[1] for c in llm.json.call_args_list]
            self.assertNotEqual(users[0], users[1])


if __name__ == '__main__':
    unittest.main()
