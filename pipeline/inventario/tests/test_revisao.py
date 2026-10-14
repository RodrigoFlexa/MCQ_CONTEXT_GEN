"""Revisor de notas, deduplicação e documentos."""
import json
import tempfile
import unittest
from pathlib import Path

import numpy as np

from apoio import FakeLLM, SOURCE, fact, note_json
from pipeline.inventario import fichas as F, notas as N, revisao as R
from pipeline.inventario.run_inventario import note_record

SUB = {'key': 's1', 'topico': 'Produção', 'subtopico': 'Separadores', 'frase': 'frase do especialista',
       'dir': 'prod__sep-s1'}
ASSUNTO = {'id': 'a01', 'texto': 'formação de espuma', 'generico': False}
CONCEITO = {'kid': 's1:a01:k1', 'nome': 'Espuma', 'foco': 'mecanismo', 'relevancia': 'alta', 'fatos': ['f1', 'f2']}
FACTS = {'f1': fact('f1'), 'f2': fact('f2', chunk='c2', coll='hse')}
CHUNKS = {'c1': {'chunk_id': 'c1', 'collection': 'anp', 'title': 'c1', 'texto': SOURCE},
          'c2': {'chunk_id': 'c2', 'collection': 'hse', 'title': 'c2', 'texto': SOURCE}}


class LLM:
    def __init__(self, data):
        self.data = data

    def json(self, system, user, **kw):
        kw['validate'](self.data)
        return self.data


def draft():
    return N.write_note(FakeLLM(), SUB, ASSUNTO, CONCEITO, FACTS, CHUNKS)


def verdict(decisao='aprovar', nota=None, **scores):
    av = {k: 5 for k in R.CRITERIOS}
    av.update(scores)
    return {'decisao': decisao, 'avaliacao': av, 'problemas': [], 'motivo': 'm', 'nota_final': nota}


class Revisor(unittest.TestCase):
    def test_aprovar(self):
        r = R.review_note(LLM(verdict()), draft(), 'k')
        self.assertEqual(r['status'], 'aprovada')
        self.assertEqual(r['revisao']['decisao'], 'aprovar')

    def test_corrigir_usa_nota_final_e_remove_secao_sem_fato(self):
        final = note_json(('F1',))
        final['secoes'].append({'tipo': 'seguranca_riscos', 'texto': 'Texto sem fonte nenhuma ' * 5, 'fatos': [],
                                'conhecimento_geral': False})
        r = R.review_note(LLM(verdict('corrigir', final)), draft(), 'k')
        self.assertEqual(r['status'], 'aprovada')
        self.assertEqual(len(r['nota']['secoes']), 3)
        self.assertTrue(any(a.startswith('secao_removida_sem_fato') for a in r['alertas_finais']))

    def test_rejeitar_e_notas_baixas_reprovam(self):
        self.assertEqual(R.review_note(LLM(verdict('rejeitar')), draft(), 'k')['status'], 'reprovada')
        r = R.review_note(LLM(verdict(riqueza=2)), draft(), 'k')
        self.assertEqual(r['status'], 'reprovada')
        self.assertIn('riqueza=2 < 3', r['motivos_reprovacao'])

    def test_validador(self):
        v = R.make_validator(draft())
        with self.assertRaisesRegex(ValueError, 'nota completa'):
            v(verdict('corrigir', None))
        with self.assertRaises(ValueError):
            v({**verdict(), 'avaliacao': {'correcao_tecnica': 9}})
        with self.assertRaisesRegex(ValueError, 'NUMBER'):
            v(verdict('corrigir', note_json(texto='valor <NUMBER> bar ' * 10)))


class Deduplicacao(unittest.TestCase):
    def test_mantem_melhor_e_herda_assuntos(self):
        notes = [{'nid': 'n1', 'assuntos': ['a01'], 'avaliacao': {'riqueza': 3}, 'metricas': {'palavras': 300}},
                 {'nid': 'n2', 'assuntos': ['a02'], 'avaliacao': {'riqueza': 5}, 'metricas': {'palavras': 300}},
                 {'nid': 'n3', 'assuntos': ['a03'], 'avaliacao': {'riqueza': 5}, 'metricas': {'palavras': 300}}]
        vecs = np.array([[1, 0], [0.99, 0.141], [0, 1]], dtype=np.float32)
        kept, removed = N.dedupe(notes, vecs, 0.92)
        self.assertEqual([n['nid'] for n in kept], ['n2', 'n3'])
        self.assertEqual(kept[0]['assuntos'], ['a01', 'a02'])
        self.assertEqual(removed[0]['duplicada_de'], 'n2')


class Documentos(unittest.TestCase):
    def test_nota_aprovada_nao_oculta_processamento_parcial(self):
        d = draft()
        rec = note_record(SUB, ASSUNTO, CONCEITO, d, R.review_note(LLM(verdict()), d, 'k'), FACTS, CHUNKS)
        with tempfile.TemporaryDirectory() as tmp:
            rows = F.write_subtopic(tmp, SUB, [ASSUNTO], {}, list(FACTS.values()), {}, [rec], {'a01'})
            self.assertEqual(rows[0]['status'], 'com_contexto')
            self.assertFalse(rows[0]['processamento_completo'])
            self.assertIn('itens pulados', (Path(tmp)/'documento.md').read_text(encoding='utf-8'))

    def test_documento_com_fontes_e_cobertura(self):
        d = draft()
        rec = note_record(SUB, ASSUNTO, CONCEITO, d, R.review_note(LLM(verdict()), d, 'k'), FACTS, CHUNKS)
        failed = note_record(SUB, {'id': 'a02', 'texto': 'b', 'generico': False}, {**CONCEITO, 'kid': 'k2'}, d,
                             R.review_note(LLM(verdict('rejeitar')), d, 'k'), FACTS, CHUNKS)
        assuntos = [ASSUNTO, {'id': 'a02', 'texto': 'drenagem', 'generico': False},
                    {'id': 'a03', 'texto': 'sem material', 'generico': False},
                    {'id': 'a04', 'texto': 'genérico', 'generico': True}]
        with tempfile.TemporaryDirectory() as tmp:
            out = Path(tmp)
            sd = out / 'subtopicos' / SUB['dir']
            rows = F.write_subtopic(sd, SUB, assuntos, {}, list(FACTS.values()), {}, [rec, failed], {'a02'})
            st = {r['assunto_id']: r['status'] for r in rows}
            self.assertEqual(st, {'a01': 'com_contexto', 'a02': 'incompleto', 'a03': 'sem_contexto', 'a04': 'generico'})
            doc = (sd / 'documento.md').read_text(encoding='utf-8')
            self.assertIn('Espuma em separadores de produção', doc)
            self.assertIn('**Fontes**', doc)
            self.assertIn('anp: c1.pdf', doc)
            self.assertIn('Repita o comando', doc)
            F.write_coverage(out, rows)
            F.write_generation_index(out, rows)
            F.write_topic_documents(out, [SUB])
            idx = [json.loads(l) for l in (out / 'assuntos_para_geracao.jsonl').read_text(encoding='utf-8').splitlines()]
            self.assertEqual({r['assunto_id']: r['modo_geracao'] for r in idx},
                             {'a01': 'com_contexto', 'a02': 'reprocessar', 'a03': 'sem_contexto'})
            self.assertEqual(idx[0]['notas'], ['s1:a01:k1'])
            topic = json.loads((out / 'documentos_topicos.json').read_text(encoding='utf-8'))[0]
            self.assertIn('### a01', (out / topic['arquivo']).read_text(encoding='utf-8'))


if __name__ == '__main__':
    unittest.main()
