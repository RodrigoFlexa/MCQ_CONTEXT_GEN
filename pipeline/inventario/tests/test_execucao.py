"""CLI inteira sobre cinco coleções pequenas e serviços simulados: continuidade, retomada e disjuntor."""
import contextlib
import io
import json
import tempfile
import unittest
from pathlib import Path
from unittest.mock import Mock, patch

import numpy as np

from apoio import FakeLLM, corpus_fixture
from pipeline.inventario.locking import output_lock
from pipeline.inventario.run_inventario import SystemicFailure, main, select_subtopics, Pipeline
from pipeline.fase_3.topicos import TOPICOS

TOPIC = 'Gestão do Desempenho Empresarial (KPI)'


def read_jsonl(path):
    return [json.loads(l) for l in Path(path).read_text(encoding='utf-8').splitlines() if l.strip()]


class Execucao(unittest.TestCase):
    def test_redator_isola_fatos_com_mesmo_id_por_subtopico(self):
        from types import SimpleNamespace
        from time import time
        subs = [{'key':'s1','subtopico':'Primeiro'}, {'key':'s2','subtopico':'Segundo'}]
        assunto = {'id':'a01','generico':False}
        facts = {s['key']:[{'fid':'mesmo-trecho#f0','sub_key':s['key']}] for s in subs}
        plans = {s['key']:{'a01':{'conceitos':[{'kid':s['key']+':a01:k1'}]}} for s in subs}
        pipeline = Pipeline(SimpleNamespace(), self.out, Mock(), None, None,
                            SimpleNamespace(rows=[]), subs, None, None, time())
        pipeline.run_jobs = lambda stage,jobs,fn,*a,**kw: {key:fn(payload) for key,payload in jobs}

        def write(llm, sub, subject, concept, lookup, chunks):
            self.assertEqual(lookup['mesmo-trecho#f0']['sub_key'], sub['key'])
            return {'insuficiente':'simulado'}

        def record(sub, subject, concept, draft, review, lookup, chunks):
            self.assertEqual(lookup['mesmo-trecho#f0']['sub_key'], sub['key'])
            return {'nid':concept['kid'],'status':'insuficiente'}

        with patch('pipeline.inventario.run_inventario.N.write_note', side_effect=write), \
             patch('pipeline.inventario.run_inventario.note_record', side_effect=record):
            result=pipeline.stage_notas({s['key']:[assunto] for s in subs},facts,{},plans,None,None)
        self.assertEqual(set(result),{'s1','s2'})

    def test_recorte_dos_quatro_topicos_preserva_lastro(self):
        names = ['Produção e Processo (Medição Fiscal e Sistema de Alívio)',
                 'Operações submarinas, poços, risers e equipamentos submarinos',
                 'Utilidades, geração de energia e sistemas auxiliares',
                 'Segurança Operacional, SGSO, Sistemas de Segurança e Gestão de Riscos']
        selected = select_subtopics(TOPICOS, names, [])
        self.assertEqual(len(selected), 23)
        self.assertEqual({s['topico'] for s in selected}, set(names))
        self.assertFalse(any('Lastro' in s['topico'] for s in selected))
        self.assertFalse(any('KPI' in s['topico'] for s in selected))

    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.root = Path(self.tmp.name)
        self.manifest = corpus_fixture(self.root)
        self.out = self.root / 'output'
        FakeLLM.fail = {}
        self.addCleanup(lambda: setattr(FakeLLM, 'fail', {}))

    def run_cli(self, *extra):
        args = ['--corpus-manifest', str(self.manifest), '--allow-sample-corpus', '--topicos', TOPIC,
                '--output', str(self.out), '--embedder', 'hash', '--workers', '2', *extra]
        with patch('pipeline.inventario.run_inventario.LLMClient', FakeLLM), contextlib.redirect_stdout(io.StringIO()):
            return main(args)

    def test_fluxo_completo_e_retomada(self):
        result = self.run_cli()
        self.assertEqual(result['status'], 'concluido')
        self.assertEqual(result['assuntos'], {'com_contexto': 1})
        notes = read_jsonl(self.out / 'notas_aprovadas.jsonl')
        self.assertEqual(len(notes), 1)
        self.assertTrue(notes[0]['fontes'])
        doc = json.loads((self.out / 'documentos_topicos.json').read_text(encoding='utf-8'))[0]
        text = (self.out / doc['arquivo']).read_text(encoding='utf-8')
        self.assertIn('Espuma em separadores de produção', text)
        self.assertIn('Conhecimentos avaliáveis', text)
        sub = next((self.out / 'subtopicos').iterdir())
        sel = json.loads((sub / 'selecao.json').read_text(encoding='utf-8'))['assuntos']['a01']
        self.assertGreaterEqual(len(sel['info']['colecoes']), 4)       # cota por coleção
        self.assertTrue(read_jsonl(sub / 'fatos_descartados.jsonl'))   # citação inventada descartada
        combos = json.loads((sub / 'combinacoes.json').read_text(encoding='utf-8'))
        self.assertEqual(combos['modo'], 'poucas_notas')               # 1 nota: sem combinação, sem chamada
        self.assertTrue((self.out / 'combinacoes.jsonl').exists())
        self.assertEqual(self.run_cli()['status'], 'concluido')        # retomada idempotente
        with self.assertRaisesRegex(ValueError, 'Configuração mudou'):
            self.run_cli('--chunk-words', '400')

    def test_filtro_de_conteudo_nao_interrompe(self):
        FakeLLM.fail = {'fatos': 'filtro', 'notas': 'filtro'}
        result = self.run_cli()
        self.assertEqual(result['status'], 'concluido_com_ocorrencias')
        occ = read_jsonl(self.out / 'ocorrencias.jsonl')
        self.assertEqual({o['etapa'] for o in occ}, {'fatos', 'notas'})
        self.assertTrue(all(o['tipo'] == 'filtro_conteudo' for o in occ))
        statuses = [n['status'] for n in read_jsonl(next((self.out / 'subtopicos').iterdir()) / 'notas.jsonl')]
        self.assertIn('filtrada', statuses)
        self.assertTrue((self.out / 'cobertura.md').exists())

    def test_falha_isolada_marca_incompleto_e_segue(self):
        FakeLLM.fail = {'notas': 'falha'}
        result = self.run_cli()
        self.assertEqual(result['ocorrencias'], {'validacao': 1})
        idx = read_jsonl(self.out / 'assuntos_para_geracao.jsonl')
        self.assertIn(idx[0]['modo_geracao'], ('reprocessar', 'com_contexto'))
        FakeLLM.fail = {}
        self.assertEqual(self.run_cli()['status'], 'concluido')     # repetir reprocessa o que faltou

    def test_falhas_em_serie_acionam_disjuntor(self):
        FakeLLM.fail = {'fatos': 'todos_falha'}
        with self.assertRaises(SystemicFailure):
            self.run_cli('--max-falhas-consecutivas', '2')
        self.assertEqual(json.loads((self.out / 'resumo.json').read_text(encoding='utf-8'))['status'], 'interrompido')

    def test_limite_de_assuntos_e_reaproveitamento(self):
        self.run_cli('--limite-assuntos', '1')
        first = self.out
        self.out = self.root / 'output2'
        result = self.run_cli('--limite-assuntos', '1', '--reaproveitar-de', str(first), '--parar-apos', 'varredura')
        self.assertEqual(result['status'], 'concluido')
        log = (self.out / 'execucao.log').read_text(encoding='utf-8')
        self.assertIn('[reaproveitamento]', log)
        self.assertIn('[varredura] reaproveitada', log)

    def test_corpus_corrompido_falha_antes_llm(self):
        (self.root / 'anp.jsonl').write_text('modificado', encoding='utf-8')
        with patch('pipeline.inventario.run_inventario.LLMClient') as llm, contextlib.redirect_stdout(io.StringIO()):
            with self.assertRaisesRegex(ValueError, 'corrompido'):
                main(['--corpus-manifest', str(self.manifest), '--allow-sample-corpus', '--topicos', TOPIC,
                      '--output', str(self.out), '--embedder', 'hash'])
            llm.assert_not_called()

    def test_corpus_novo_exige_nova_saida(self):
        self.run_cli('--parar-apos', 'varredura')
        data = json.loads(self.manifest.read_text(encoding='utf-8'))
        data['updated_at'] = 'nova versão'
        self.manifest.write_text(json.dumps(data), encoding='utf-8')
        with self.assertRaisesRegex(ValueError, 'corpora mudaram'):
            self.run_cli('--parar-apos', 'varredura')

    def test_plano_nao_chama_servicos(self):
        with patch('pipeline.inventario.run_inventario.LLMClient') as llm, contextlib.redirect_stdout(io.StringIO()):
            result = main(['--corpus-manifest', str(self.manifest), '--allow-sample-corpus', '--topicos', TOPIC,
                           '--output', str(self.out), '--plan'])
            self.assertEqual(result, {'subtopicos': 1, 'calls': 0})
            llm.assert_not_called()

    def test_impede_execucao_concorrente_mesma_saida(self):
        with output_lock(self.root):
            with self.assertRaisesRegex(RuntimeError, 'Outra execução'):
                with output_lock(self.root):
                    pass

    def test_check_api_forca_pedidos_novos(self):
        with patch('pipeline.inventario.run_inventario.LLMClient') as llm_cls, \
             patch('pipeline.inventario.modelos.load_models') as loader, contextlib.redirect_stdout(io.StringIO()):
            llm = llm_cls.return_value
            llm.json.return_value = {'ok': True}
            emb = Mock()
            emb.impl.encode.return_value = np.ones((2, 3072), dtype=np.float32)
            loader.return_value = (emb, None)
            args = ['--output', str(self.out), '--topicos', TOPIC, '--check-api']
            main(args)
            main(args)
            self.assertEqual(emb.impl.encode.call_count, 2)
            users = [c.args[1] for c in llm.json.call_args_list]
            self.assertNotEqual(users[0], users[1])


if __name__ == '__main__':
    unittest.main()
