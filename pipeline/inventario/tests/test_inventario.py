"""Varredura, seleção bilíngue, fatos e plano de conceitos (sem rede e sem GPU)."""
import tempfile
import unittest
from pathlib import Path

import numpy as np

from apoio import FakeLLM, QUOTE, SOURCE, fact
from pipeline.inventario import consolidacao as C, extracao as X, selecao as S, varredura as V
from pipeline.inventario.modelos import EmbeddingCache, HashEmbedder

SUB = {'key': 's1', 'topico': 'Produção', 'subtopico': 'Separadores'}
ASSUNTOS = [{'id': 'a01', 'texto': 'formação de espuma', 'generico': False, 'consulta_pt': 'espuma em separadores',
             'consulta_en': 'foam in separators', 'termos_pt': ['espuma'], 'termos_en': ['foam']},
            {'id': 'a02', 'texto': 'aspectos gerais', 'generico': True, 'consulta_pt': 'x', 'consulta_en': 'x',
             'termos_pt': [], 'termos_en': []}]


def cand(cid, coll, text, doc=None):
    return {'chunk_id': cid, 'collection': coll, 'document_id': doc or cid, 'texto': text, 'lex_score': 3.0}


class Varredura(unittest.TestCase):
    def test_janelas_nao_atravessam_documentos(self):
        rows = [{'collection': 'anp', 'document_id': 'a', 'page': 1, 'text': ' '.join(f'w{i}' for i in range(900))},
                {'collection': 'hse', 'document_id': 'h', 'page': 1, 'text': ' '.join(f'x{i}' for i in range(120))}]
        wins = list(V.windows(rows, chunk_words=350, stride=250, min_words=80))
        self.assertTrue(all(len({w[0] for w in t.split()}) == 1 for _, t, _ in wins))
        self.assertIn('w899', ' '.join(t for _, t, p in wins if p['collection'] == 'anp'))

    def test_scan_encontra_termos_pt_e_en(self):
        assuntos = [{**ASSUNTOS[0], 'key': 's1::a01'}]
        rows = [{'collection': 'anp', 'document_id': 'a', 'page': 1, 'text': SOURCE * 4},
                {'collection': 'hse', 'document_id': 'h', 'page': 1,
                 'text': 'Foam in separators increases liquid carryover into the gas outlet. ' * 20}]
        found, stats = V.scan(rows, assuntos, quota=5, chunk_words=100, stride=80, min_words=40)
        self.assertEqual({c['collection'] for c in found['s1::a01']}, {'anp', 'hse'})


class Selecao(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.cache = EmbeddingCache(Path(self.tmp.name) / 'e.npz', 'hash')
        self.emb = HashEmbedder()

    def test_cota_por_colecao_garante_ingles(self):
        pool = [cand(f'pt{i}', 'petroles', SOURCE + f' variação {i} ' * 3, doc='petroles-1') for i in range(10)]
        pool += [cand('en1', 'hse', 'Foam in separators reduces gas flow area and increases liquid carryover.', 'hse-1'),
                 cand('en2', 'bsee', 'Separator foam causes carryover of liquid into the gas outlet.', 'bsee-1')]
        chosen, info = S.select_for_assunto(ASSUNTOS[0], pool, self.cache, self.emb, k=4, min_por_colecao=1)
        self.assertLessEqual(len(chosen), 4)
        self.assertTrue({'hse', 'bsee'} & {c['collection'] for c in chosen}, info)
        self.assertEqual(info['modo'], 'hash')

    def test_teto_por_documento_e_duplicata(self):
        pool = [cand(f'd{i}', 'anp', SOURCE + ' ' + 'palavra ' * i, doc='mesmo-doc') for i in range(8)]
        chosen, _ = S.select_for_assunto(ASSUNTOS[0], pool, self.cache, self.emb, k=8, max_por_documento=3)
        self.assertLessEqual(len(chosen), 3)

    def test_corte_relativo_em_cosseno(self):
        class Emb(HashEmbedder):
            name = 'embedding-3-large-global'

            def encode(self, texts, batch_size=32, desc=None):
                v = np.zeros((len(texts), 2), dtype=np.float32)
                for i, t in enumerate(texts):
                    v[i] = [1, 0] if ('espuma' in t or 'foam' in t) else [0.3, 0.954]
                return v
        pool = [cand('bom', 'anp', 'espuma no separador'), cand('ruim', 'anp', 'tubulação de esgoto municipal')]
        cache = EmbeddingCache(Path(self.tmp.name) / 'e2.npz', 'emb')
        chosen, info = S.select_for_assunto(ASSUNTOS[0], pool, cache, Emb(), k=5)
        self.assertEqual([c['chunk_id'] for c in chosen], ['bom'])
        self.assertEqual(info['modo'], 'cosine')

    def test_sem_candidatos(self):
        chosen, info = S.select_for_assunto(ASSUNTOS[0], [], self.cache, self.emb)
        self.assertEqual((chosen, info['selecionados']), ([], 0))


class Fatos(unittest.TestCase):
    chunk = {'chunk_id': 'c1', 'collection': 'anp', 'document_id': 'c1', 'title': 'c1.pdf', 'texto': SOURCE * 2}

    def test_salva_fatos_bons_e_descarta_citacao_inventada(self):
        kept, dropped = X.extract_chunk(FakeLLM(), SUB, self.chunk, ASSUNTOS, {'a01'})
        self.assertEqual(len(kept), 2)
        self.assertEqual(dropped[0]['descartado_por'], ['citacao_nao_literal'])
        self.assertTrue(all(f['fonte']['chunk_id'] == 'c1' for f in kept))

    def test_fato_sem_assunto_herda_assunto_da_busca(self):
        raw = {'conceito': 'espuma', 'tipo': 'mecanismo', 'afirmacao': 'A espuma reduz a área de escoamento do gás.',
               'condicoes': '', 'assuntos': ['zz'], 'pertinencia': 'transferivel', 'citacao': QUOTE}
        f, reasons = X.review_fact(raw, self.chunk, {'a01'}, {'a01'})
        self.assertEqual((f['assuntos'], reasons, f['assunto_inferido']), (['a01'], [], True))

    def test_number_placeholder_e_fora(self):
        raw = {'conceito': 'x', 'tipo': 'criterio_limite', 'afirmacao': 'O limite é de <NUMBER> bar no separador.',
               'condicoes': '', 'assuntos': ['a01'], 'pertinencia': 'fora', 'citacao': QUOTE}
        _, reasons = X.review_fact(raw, self.chunk, {'a01'})
        self.assertIn('valor_ausente_na_fonte', reasons)
        self.assertIn('fora_de_fpso', reasons)

    def test_numero_sem_fonte_vira_alerta_nao_descarte(self):
        raw = {'conceito': 'x', 'tipo': 'criterio_limite', 'afirmacao': 'O tempo de retenção de 3 minutos a 70 bar deixa '
               'de ser efetivo com espuma.', 'condicoes': '', 'assuntos': ['a01'], 'pertinencia': 'fpso_direta',
               'citacao': QUOTE}
        f, reasons = X.review_fact(raw, self.chunk, {'a01'})
        self.assertEqual((reasons, f['numeros_nao_verificados']), ([], ['70']))

    def test_estrutura_invalida_pede_reparo(self):
        with self.assertRaises(ValueError):
            X.validate_structure({'unidades': []})


class Conceitos(unittest.TestCase):
    def test_vazio_e_direto_sem_chamada(self):
        llm = FakeLLM()
        self.assertEqual(C.plan_assunto(llm, SUB, ASSUNTOS[0], [])['modo'], 'vazio')
        plan = C.plan_assunto(llm, SUB, ASSUNTOS[0], [fact('f1'), fact('f2')])
        self.assertEqual((plan['modo'], len(plan['conceitos'][0]['fatos'])), ('direto', 2))
        self.assertEqual(llm.usage['calls'], 0)

    def test_modelo_agrupa_e_descarta(self):
        facts = [fact(f'f{i}', score=1 - i / 10) for i in range(6)]
        plan = C.plan_assunto(FakeLLM(), SUB, ASSUNTOS[0], facts)
        self.assertEqual(plan['modo'], 'modelo')
        self.assertEqual(len(plan['conceitos'][0]['fatos']) + len(plan['descartados']), 6)
        self.assertTrue(plan['conceitos'][0]['kid'].startswith('s1:a01:k'))

    def test_validador_exige_classificar_fatos(self):
        validate = C.make_validator({'F1', 'F2', 'F3', 'F4', 'F5'})
        with self.assertRaisesRegex(ValueError, 'faltaram'):
            validate({'conceitos': [{'nome': 'x', 'fatos': ['F1']}], 'descartados': []})
        self.assertTrue(validate({'conceitos': [], 'descartados': [{'fato': f'F{i}'} for i in range(1, 6)]}))

    def test_excesso_de_fatos_prioriza_pertinencia(self):
        facts = [fact(f'f{i:03d}') for i in range(C.MAX_FATOS_PLANO + 5)]
        facts[-1]['pertinencia'] = 'fpso_direta'
        for f in facts[:-1]:
            f['pertinencia'] = 'transferivel'
        plan = C.plan_assunto(FakeLLM(), SUB, ASSUNTOS[0], facts)
        self.assertEqual(len(plan['excedentes']), 5)
        self.assertNotIn(facts[-1]['fid'], plan['excedentes'])


if __name__ == '__main__':
    unittest.main()
