"""Testes sem rede e sem GPU (LLM simulado, embedding por hash).

    python -m unittest discover -s pipeline/inventario/tests -v
"""
import json
import sys
import tempfile
import unittest
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT))

from pipeline.inventario import assuntos as A  # noqa: E402
from pipeline.inventario import consolidacao as C  # noqa: E402
from pipeline.inventario import extracao as X  # noqa: E402
from pipeline.inventario import fichas as F  # noqa: E402
from pipeline.inventario import selecao as S  # noqa: E402
from pipeline.inventario import varredura as V  # noqa: E402
from pipeline.inventario.modelos import EmbeddingCache, HashEmbedder, HashReranker  # noqa: E402
from pipeline.inventario.textutil import quote_supported, squash  # noqa: E402

FRASE = ("As questões devem abordar os aspectos relacionados à gestão da manutenção, incluindo gestão de backlog, "
         "priorização de serviços e cumprimento da programação, análise de manutenção vencida, diferida ou postergada "
         "e avaliação dos riscos associados, avaliação de MTBF, MTTR, disponibilidade e confiabilidade, além da "
         "aplicação de boas práticas de engenharia.")

BACKLOG = ("O backlog de manutenção corresponde ao conjunto de ordens de serviço pendentes. A gestão de backlog "
           "exige priorização por criticidade e acompanhamento do envelhecimento das pendências. O cumprimento da "
           "programação mede a fração dos serviços programados efetivamente concluídos no período.")
MTBF = ("A disponibilidade de um equipamento reparável pode ser estimada por MTBF dividido pela soma de MTBF e MTTR. "
        "O MTTR representa o tempo médio para reparo e inclui diagnóstico, espera de sobressalentes e execução. "
        "Reduzir o MTTR aumenta a disponibilidade sem alterar a taxa de falhas.")
LIXO = "Referências Bibliográficas SILVA, J. 2001. SOUZA, M. 2003. " * 10


class FakeLLM:
    def __init__(self):
        self.usage = {'calls': 0, 'cached': 0, 'prompt_tokens': 0, 'completion_tokens': 0, 'errors': 0}

    def json(self, system, user, tag='', max_tokens=0, validate=None):
        self.usage['calls'] += 1
        if system is A.SYSTEM:
            data = {'assuntos': [
                {'id': 'a01', 'texto': 'gestão de backlog, priorização de serviços e cumprimento da programação',
                 'consulta_pt': 'gestão de backlog de manutenção', 'consulta_en': 'maintenance backlog management',
                 'termos_pt': ['backlog', 'cumprimento da programação', 'FPSO'], 'termos_en': ['backlog']},
                {'id': 'a02', 'texto': 'avaliação de MTBF, MTTR, disponibilidade e confiabilidade',
                 'consulta_pt': 'MTBF MTTR disponibilidade', 'consulta_en': 'MTBF MTTR availability',
                 'termos_pt': ['MTBF', 'MTTR'], 'termos_en': ['mean time to repair']},
                {'id': 'a03', 'texto': 'aplicação de boas práticas de engenharia', 'generico': True,
                 'consulta_pt': 'boas práticas', 'consulta_en': 'good practice', 'termos_pt': [], 'termos_en': []}]}
        elif system is X.SYSTEM:
            if 'MTBF' in user:
                data = {'unidades': [
                    {'tipo': 'formula_calculo', 'afirmacao': 'Disponibilidade = MTBF/(MTBF+MTTR).', 'condicoes': 'equipamento reparável',
                     'entidades': ['MTBF'], 'assuntos': ['a02'], 'aplicabilidade': 'transferivel', 'valor_para_pergunta': 'alto',
                     'citacao': 'pode ser estimada por MTBF dividido pela soma de MTBF e MTTR'},
                    {'tipo': 'causa_efeito', 'afirmacao': 'Reduzir o MTTR aumenta a disponibilidade.', 'condicoes': '',
                     'entidades': ['MTTR'], 'assuntos': ['a02', 'zz'], 'aplicabilidade': 'transferivel', 'valor_para_pergunta': 'alto',
                     'citacao': 'Reduzir o MTTR aumenta a disponibilidade sem alterar a taxa de falhas'},
                    {'tipo': 'definicao', 'afirmacao': 'Inventado.', 'condicoes': '', 'entidades': [], 'assuntos': ['a02'],
                     'aplicabilidade': 'transferivel', 'valor_para_pergunta': 'alto', 'citacao': 'frase que não existe no trecho original'}]}
            else:
                data = {'unidades': [
                    {'tipo': 'definicao', 'afirmacao': 'Backlog é o conjunto de ordens pendentes.', 'condicoes': '',
                     'entidades': ['backlog'], 'assuntos': ['a01'], 'aplicabilidade': 'transferivel', 'valor_para_pergunta': 'medio',
                     'citacao': 'O backlog de manutenção corresponde ao conjunto de ordens de serviço pendentes'}]}
        elif system is C.SYSTEM:
            groups = json.loads(user)
            data = {'grupos': [{'grupo': g['grupo'], 'status': 'equivalentes', 'afirmacao': 'Canônica.',
                                'membros': [u['uid'] for u in g['unidades']]} for g in groups]}
        else:
            raise AssertionError('prompt inesperado')
        if validate:
            validate(data)
        return data


def units_for(docs):
    for coll, doc, text in docs:
        for page, part in enumerate([text[i:i + 400] for i in range(0, len(text), 400)], 1):
            yield {'collection': coll, 'document_id': doc, 'title': doc + '.pdf', 'language': 'pt',
                   'jurisdiction': 'BR', 'page': page, 'text': part}


class Tests(unittest.TestCase):
    def setUp(self):
        self.llm = FakeLLM()
        items, diag = A.extract_assuntos(self.llm, 'Manutenção', 'Plano de Manutenção', FRASE)
        self.items = items
        self.sub = {'key': 'k1', 'topico': 'Manutenção', 'subtopico': 'Plano de Manutenção'}
        self.searchable = [{**a, 'key': f"k1::{a['id']}", 'sub_key': 'k1'} for a in items if not a['generico']]

    def test_assuntos_literais_e_genericos(self):
        self.assertTrue(all(a['literal'] for a in self.items))
        self.assertEqual([a['generico'] for a in self.items], [False, False, True])
        self.assertNotIn('FPSO', self.items[0]['termos_pt'])  # termo genérico removido

    def test_janelas_nao_atravessam_documentos(self):
        docs = [('anp', 'anp-1', ' '.join(f'w{i}' for i in range(900))), ('hse', 'hse-1', ' '.join(f'x{i}' for i in range(120)))]
        wins = list(V.windows(units_for(docs), chunk_words=350, stride=250, min_words=80))
        self.assertTrue(all(len(t.split()) <= 350 for _, t, _ in wins))
        for _, t, p in wins:
            self.assertEqual(len({w[0] for w in t.split()}), 1, 'janela mistura documentos')
        joined = ' '.join(t for _, t, p in wins if p['collection'] == 'anp')
        self.assertIn('w899', joined)

    def test_varredura_selecao_extracao_consolidacao(self):
        docs = [('anp', 'anp-1', (BACKLOG + ' ') * 4), ('hse', 'hse-1', (MTBF + ' ') * 4),
                ('regis', 'regis-1', LIXO), ('petroles', 'petroles-x', ('texto sem relação com o tema ' * 60))]
        cands, stats = V.scan(units_for(docs), self.searchable, quota=5, chunk_words=120, stride=80, min_words=40)
        self.assertIn('k1::a01', cands)
        self.assertIn('k1::a02', cands)
        self.assertTrue(all(c['collection'] == 'anp' for c in cands['k1::a01']))
        self.assertGreater(stats['ruido'], 0)
        emb = HashEmbedder()
        with tempfile.TemporaryDirectory() as tmp:
            cache = EmbeddingCache(Path(tmp) / 'e.npz', 'hash')
            sels = {}
            for a in self.searchable:
                chosen, info = S.select_for_assunto(a, cands[a['key']], cache, emb, HashReranker(emb), k=3, min_rerank=0.0)
                self.assertLessEqual(len(chosen), 3)
                sels[a['id']] = {'info': info, 'trechos': chosen}
            cache.save()
            self.assertTrue((Path(tmp) / 'e.npz').exists())
            cache2 = EmbeddingCache(Path(tmp) / 'e.npz', 'hash')
            self.assertEqual(len(cache2.vectors), len(cache.vectors))
            kept, dropped = [], []
            for aid, v in sels.items():
                for c in v['trechos']:
                    k, d = X.extract_chunk(self.llm, self.sub, c, self.items, {aid})
                    kept += k
                    dropped += d
            self.assertTrue(any('citacao_nao_encontrada' in d['descartada_por'] for d in dropped))
            self.assertTrue(all(u['citacao_verificada'] for u in kept))
            self.assertTrue(all('zz' not in u['assuntos'] for u in kept))
            self.assertGreaterEqual(len(kept), 2)
            # Simula a mesma afirmação vinda de outro documento (corroboração).
            twin = json.loads(json.dumps(kept[0]))
            twin['uid'] += '-twin'
            twin['fonte']['document_id'] = 'outro-doc'
            kept.append(twin)
            vecs = emb.encode([u['afirmacao'] + ' ' + u['condicoes'] for u in kept])
            with ThreadPoolExecutor(2) as pool:
                cons, st = C.consolidate(self.llm, 'k1', kept, vecs, threshold=0.9, pool=pool)
            self.assertLess(len(cons), len(kept))  # a cópia foi fundida
            self.assertGreater(st['equivalentes'], 0)
            self.assertTrue(any(c['status'] == 'corroborada' and c['n_documentos'] == 2 for c in cons))
            rows = F.write_subtopic(Path(tmp) / 'sub', self.sub, self.items, cons, sels, {'aceitas': len(kept)})
            F.write_coverage(Path(tmp), rows)
            md = (Path(tmp) / 'sub' / 'fichas' / 'a02.md').read_text(encoding='utf-8')
            self.assertIn('redação do especialista', md)
            self.assertEqual({r['status'] for r in rows if r['generico']}, {'generico'})
            self.assertTrue((Path(tmp) / 'cobertura.md').exists())
            F.write_generation_index(Path(tmp), rows)
            idx = [json.loads(l) for l in (Path(tmp) / 'assuntos_para_geracao.jsonl').read_text(encoding='utf-8').splitlines()]
            self.assertEqual(len(idx), 2)  # o genérico não entra
            self.assertTrue(all(r['modo_geracao'] in ('com_contexto', 'com_contexto_parcial', 'sem_contexto') for r in idx))

    def test_assunto_sem_trechos_vira_sem_contexto(self):
        with tempfile.TemporaryDirectory() as tmp:
            rows = F.write_subtopic(Path(tmp) / 'sub', self.sub, self.items, [], {}, {})
            st = {r['assunto_id']: (r['status'], r['modo_geracao']) for r in rows}
            self.assertEqual(st['a01'], ('sem_contexto', 'sem_contexto'))
            self.assertEqual(st['a03'], ('generico', 'nao_gerar'))
            self.assertIn('sem_contexto', (Path(tmp) / 'sub' / 'fichas' / 'a01.md').read_text(encoding='utf-8'))

    def test_sem_gpu_falha_cedo(self):
        from pipeline.inventario.modelos import _device
        try:
            import torch
            has_gpu = torch.cuda.is_available()
        except ImportError:
            has_gpu = False
        if has_gpu:
            self.skipTest('máquina com GPU')
        with self.assertRaises(RuntimeError):
            _device('cuda')

    def test_citacao(self):
        self.assertTrue(quote_supported('O MTTR representa o tempo médio para reparo', MTBF))
        self.assertTrue(quote_supported('o mttr  representa o tempo\nmedio para reparo', MTBF))
        self.assertFalse(quote_supported('O MTTR representa o tempo máximo de parada da planta inteira', MTBF))
        self.assertEqual(squash('Ação  Média'), 'acao media')


if __name__ == '__main__':
    unittest.main()
