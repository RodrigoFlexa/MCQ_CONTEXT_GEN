"""Redator de notas técnicas: contexto, validação, alertas e critérios de suficiência."""
import unittest

from apoio import FakeLLM, SOURCE, fact, note_json
from pipeline.inventario import notas as N

SUB = {'key': 's1', 'topico': 'Produção', 'subtopico': 'Separadores'}
ASSUNTO = {'id': 'a01', 'texto': 'formação de espuma', 'generico': False}
CONCEITO = {'kid': 's1:a01:k1', 'nome': 'Espuma', 'foco': 'mecanismo', 'relevancia': 'alta', 'fatos': ['f1', 'f2']}
FACTS = {'f1': fact('f1'), 'f2': fact('f2', tipo='mecanismo', chunk='c2')}
CHUNKS = {'c1': {'chunk_id': 'c1', 'collection': 'anp', 'title': 'c1', 'texto': SOURCE},
          'c2': {'chunk_id': 'c2', 'collection': 'hse', 'title': 'c2', 'texto': SOURCE}}


class Contexto(unittest.TestCase):
    def test_ids_curtos_para_fatos_e_trechos(self):
        text, idmap, sources = N.build_context(SUB, ASSUNTO, CONCEITO, FACTS, CHUNKS)
        self.assertEqual(idmap['F1'], 'f1')
        self.assertEqual(idmap['T1'], 'trecho:c1')
        self.assertIn('Assunto (redação do especialista): formação de espuma', text)
        self.assertIn(SOURCE.strip()[:40], text)
        self.assertEqual(len(sources), 4)


class Validacao(unittest.TestCase):
    def setUp(self):
        _, self.idmap, self.sources = N.build_context(SUB, ASSUNTO, CONCEITO, FACTS, CHUNKS)

    def test_nota_valida_e_metricas(self):
        nota, alertas, m = N.normalize_note(note_json(('F1', 'T2')), self.idmap, self.sources)
        self.assertEqual(alertas, [])
        self.assertEqual(nota['secoes'][0]['fatos'], ['f1', 'trecho:c2'])
        self.assertEqual(m['secoes_fundamentadas'], 3)
        self.assertEqual(m['fatos_citados'], 1)
        self.assertIsNone(N.insufficient_reason(nota, m))

    def test_number_placeholder_pede_reparo(self):
        with self.assertRaisesRegex(ValueError, 'NUMBER'):
            N.normalize_note(note_json(texto='Opera a <NUMBER> bar ' * 20), self.idmap, self.sources)

    def test_campos_obrigatorios(self):
        bad = note_json()
        bad['titulo'] = ''
        with self.assertRaises(ValueError):
            N.normalize_note(bad, self.idmap, self.sources)
        with self.assertRaises(ValueError):
            N.normalize_note({**note_json(), 'secoes': []}, self.idmap, self.sources)

    def test_alertas_ref_invalida_numero_sem_fonte_e_secao_sem_fato(self):
        raw = note_json(('F9',), texto='O separador opera a 85 bar com espuma reduzindo a área de gás e o tempo de '
                        'retenção de 3 minutos deixa de ser efetivo, segundo os fatos citados.')
        nota, alertas, m = N.normalize_note(raw, self.idmap, self.sources)
        self.assertTrue(any('refs_invalidas:F9' in a for a in alertas))
        self.assertTrue(any('numeros_sem_fonte:85' in a for a in alertas))
        self.assertTrue(any(a.endswith('_sem_fato') for a in alertas))
        self.assertEqual(m['secoes_fundamentadas'], 0)
        self.assertIn('fundamentada', N.insufficient_reason(nota, m))

    def test_conhecimento_geral_com_fatos_vira_fundamentado(self):
        nota, alertas, _ = N.normalize_note(note_json(geral=True), self.idmap, self.sources)
        self.assertFalse(nota['secoes'][0]['conhecimento_geral'])
        self.assertTrue(any('geral_com_fatos' in a for a in alertas))

    def test_conhecimento_geral_dominante_e_insuficiente(self):
        raw = note_json()
        for s in raw['secoes'][:2]:
            s['conhecimento_geral'], s['fatos'] = True, []
        raw['secoes'][2]['texto'] = 'Avaliar a entrada.'
        nota, _, m = N.normalize_note(raw, self.idmap, self.sources)
        self.assertIsNotNone(N.insufficient_reason(nota, m))

    def test_status_insuficiente_do_redator(self):
        nota, _, m = N.normalize_note({**note_json(), 'status': 'insuficiente', 'lacunas': ['só definições']},
                                      self.idmap, self.sources)
        self.assertIn('só definições', N.insufficient_reason(nota, m))


class Redator(unittest.TestCase):
    def test_write_note_com_llm_simulado(self):
        draft = N.write_note(FakeLLM(), SUB, ASSUNTO, CONCEITO, FACTS, CHUNKS)
        self.assertIsNone(draft['insuficiente'])
        self.assertGreater(draft['metricas']['palavras'], N.MIN_PALAVRAS)
        payload = N.note_payload(draft['nota'], draft['idmap'])
        self.assertEqual(payload['secoes'][0]['fatos'], ['F1', 'F2'])


if __name__ == '__main__':
    unittest.main()
