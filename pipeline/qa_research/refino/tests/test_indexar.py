"""O índice paralelo tem de ser idêntico ao do CorpusIndex sequencial.

    python -m unittest pipeline.qa_research.refino.tests.test_indexar -v
"""
import contextlib
import hashlib
import json
import random
import sqlite3
import tempfile
import unittest
from pathlib import Path

from pipeline.qa_research.corpus import CorpusIndex
from pipeline.qa_research.refino import indexar

WORDS = ('header flare amarra turret separador vaso pressão nível interface válvula bomba compressor gás óleo água '
         'produzida tratamento injeção alívio tocha piloto purga hidrato parafina corrosão inspeção integridade '
         'riser umbilical manifold árvore natal poço segurança barreira permissão trabalho guindaste eslinga').split()


def text(rng, n):
    return ' '.join(rng.choice(WORDS) for _ in range(n))


def corpus(root):
    rng = random.Random(7)
    root = Path(root)
    (root / 'paginas').mkdir(parents=True)
    rows, repeated = [], text(rng, 400)
    for d in range(9):
        pages = [1, 2, 3, 5, 6] if d % 3 == 0 else [1, 2, 3]  # lacuna de página em alguns documentos
        for p in pages:
            body = repeated if (d, p) in ((2, 1), (7, 1)) else text(rng, rng.randint(50, 500))
            rows.append(dict(collection='paginas', document_id=f'doc{d}', title=f'Documento {d}', page=p,
                             language='pt', jurisdiction='BR', source_boundary='known_document', text=body))
    # O mesmo documento reaparece depois de outro (vira nova chave no algoritmo original).
    rows.append(dict(collection='paginas', document_id='doc0', title='Documento 0', page=9, language='pt', text=text(rng, 380)))
    pages = root / 'paginas' / 'pages.jsonl'
    pages.write_text(''.join(json.dumps(r, ensure_ascii=False) + '\n' for r in rows), encoding='utf-8')
    txts = []
    for i in range(2):
        path = root / f'petroles_{i}.txt'
        path.write_text('\n'.join(text(rng, rng.randint(0, 40)) for _ in range(120)), encoding='utf-8')
        txts.append(path)
    sha = lambda p: hashlib.sha256(Path(p).read_bytes()).hexdigest()
    manifest = dict(schema='petroquest-professional-corpora-v1', ready=True, partial=True, sample=False, collections=[
        dict(id='petroles', format='petroles_txt', documents=2,
             files=[dict(path=p.name, sha256=sha(p)) for p in txts]),
        dict(id='paginas', format='pages_jsonl', path='paginas/pages.jsonl', sha256=sha(pages), documents=9)])
    (root / 'manifest.json').write_text(json.dumps(manifest), encoding='utf-8')
    return root / 'manifest.json'


def dump(path):
    with contextlib.closing(sqlite3.connect(path)) as db:
        return {table: db.execute(f'SELECT * FROM {table} ORDER BY 1, 2').fetchall()
                for table in ('metadata', 'chunks', 'sources')}


class IndexarTest(unittest.TestCase):
    def test_parallel_index_matches_sequential(self):
        with tempfile.TemporaryDirectory() as tmp:
            tmp = Path(tmp)
            manifest = corpus(tmp / 'corpus')
            sequential = CorpusIndex(tmp / 'seq', manifest=manifest)
            info_seq = sequential.build()
            info_par, path = indexar.build(manifest, tmp / 'par', workers=2, cache_mb=64, target_mb=0.004,
                                           progress=lambda *a, **k: None)
            self.assertGreater(info_par['construcao']['tarefas'], 3)
            self.assertEqual(info_seq['fingerprint'], info_par['fingerprint'])
            for key in ('chunks', 'source_records', 'invalid_chunks_skipped', 'collections', 'sources', 'complete_corpus'):
                self.assertEqual(info_seq[key], info_par[key], key)
            self.assertEqual(dump(sequential.path), dump(path))
            parallel = indexar.attach(manifest, tmp / 'par', info_par, path)
            for query in ('header flare piloto', 'amarra turret riser', 'hidrato parafina corrosão', 'eslinga guindaste'):
                a = sequential.search(query, limit=10, neighbors=True)
                b = parallel.search(query, limit=10, neighbors=True)
                self.assertEqual(json.dumps(a, sort_keys=True), json.dumps(b, sort_keys=True), query)
            # O CorpusIndex reconhece o índice paralelo e não reconstrói.
            reused = CorpusIndex(tmp / 'par', manifest=manifest)
            self.assertIn('construcao', reused.build())
            again, _ = indexar.build(manifest, tmp / 'par', workers=2, progress=lambda *a, **k: None)
            self.assertEqual(again['fingerprint'], info_par['fingerprint'])
            self.assertFalse(list((tmp / 'par').rglob('prep-*')))


if __name__ == '__main__':
    unittest.main()
