"""Regressões de proveniência, transferência, lacunas e reconstrução offline."""
import copy
import json
import tempfile
import unittest
from pathlib import Path

from apoio import FakeLLM, fact, note_v5_json, SOURCE
from pipeline.inventario import conhecimento as K, notas as N, complemento as CP
from pipeline.inventario import reconstruir_notas as RN, revisao as R
from pipeline.inventario import combinacoes as M
from pipeline.inventario.modelos import HashEmbedder


class Conhecimento(unittest.TestCase):
    def raw(self):
        return note_v5_json(('F1',))

    def normalize(self, raw):
        return K.normalize(raw, {'F1': 'c1#f0', 'T1': 'trecho:c1'})[0]

    def test_parametrico_citado_nao_vira_evidencia(self):
        raw = self.raw()
        raw['relacoes'][0]['origem'] = 'parametrico'
        note = self.normalize(raw)
        self.assertFalse(note['relacoes'][0]['avaliavel'])
        self.assertEqual(note['alvos'], [])
        self.assertEqual(len(note['alvos_bloqueados']), 2)

    def test_deducao_exige_todas_as_premissas(self):
        raw = self.raw()
        raw['relacoes'].append({**raw['relacoes'][0], 'id': 'R2', 'origem': 'deducao',
                                'fatos': [], 'premissas': ['R1']})
        raw['alvos'][0]['relacoes'] = ['R2']
        note = self.normalize(raw)
        self.assertTrue(note['relacoes'][1]['avaliavel'])
        self.assertEqual(note['relacoes'][1]['fatos'], ['c1#f0'])
        raw['relacoes'][0]['origem'] = 'parametrico'
        self.assertFalse(self.normalize(raw)['relacoes'][1]['avaliavel'])

    def test_deducao_herda_condicoes_e_limites_ate_o_alvo(self):
        raw = self.raw()
        raw['relacoes'].append({**raw['relacoes'][0], 'id': 'R2', 'origem': 'deducao',
                                'fatos': [], 'premissas': ['R1'], 'condicoes': [], 'limites': []})
        raw['alvos'][0].update(relacoes=['R2'], condicoes_enunciado=[])
        note = self.normalize(raw)
        self.assertIn('separador com espuma', note['alvos'][0]['condicoes_enunciado'])
        self.assertIn('não define a única causa de arraste', note['alvos'][0]['limites'])

    def test_combinacao_exige_relacao_avaliavel_de_cada_nota(self):
        normalized = self.normalize(self.raw())
        notes = {'N1': {**normalized, 'nid': 'n1', 'titulo': 'Um', 'assuntos': ['a']},
                 'N2': {**normalized, 'nid': 'n2', 'titulo': 'Dois', 'assuntos': ['b']}}
        combo = {'notas': ['N1', 'N2'], 'titulo': 'Integração', 'ligacao': 'L', 'raciocinio': 'R',
                 'cenario': 'C', 'resposta': 'Resposta', 'criterios_correcao': ['Critério'],
                 'conhecimentos': [{'nota': sid, 'conhecimento': 'k', 'relacoes': ['R1']} for sid in notes]}
        kept, _ = M.normalize({'combinacoes': [combo]}, notes)
        self.assertEqual(len(kept), 1)
        combo['conhecimentos'][1]['relacoes'] = ['R9']
        kept, dropped = M.normalize({'combinacoes': [combo]}, notes)
        self.assertFalse(kept)
        self.assertEqual(dropped[0]['motivo'], 'integracao_sem_contrato_sustentado')

    def test_caso_checklist_e_procedimento_nao_viram_regra(self):
        for nature in ('incidente', 'estudo', 'checklist', 'procedimento_local'):
            with self.subTest(nature=nature):
                raw = self.raw()
                raw['relacoes'][0]['natureza'] = nature
                self.assertFalse(self.normalize(raw)['alvos'])

    def test_transferencia_requer_justificativa(self):
        raw = self.raw()
        raw['relacoes'][0]['aplicabilidade'] = 'transferivel'
        self.assertFalse(self.normalize(raw)['alvos'])
        raw['relacoes'][0]['justificativa_transferencia'] = 'Mesmo mecanismo físico e regime no separador FPSO.'
        self.assertTrue(self.normalize(raw)['alvos'])

    def test_premissa_circular_ou_inexistente_e_referencia_invalida(self):
        for field, value in (('premissas', ['R1']), ('premissas', ['R9']), ('fatos', ['F9'])):
            raw = self.raw()
            raw['relacoes'][0][field] = value
            with self.assertRaises(ValueError):
                self.normalize(raw)

    def test_alvo_sem_rubrica_ou_relacao_e_bloqueado(self):
        for field, value in (('criterios_correcao', []), ('resposta', ''), ('relacoes', ['R9'])):
            raw = self.raw()
            raw['alvos'][0][field] = value
            self.assertEqual(len(self.normalize(raw)['alvos']), 1)

    def test_trocar_nivel_e_redacao_nao_cria_novo_alvo(self):
        raw = self.raw()
        raw['alvos'][1].update(habilidade=raw['alvos'][0]['habilidade'], descricao='Outro cenário e redação')
        self.assertEqual(len(self.normalize(raw)['alvos']), 1)

    def test_nota_curta_com_um_alvo_nao_precisa_forcar_niveis(self):
        raw = self.raw()
        raw['secoes'] = [raw['secoes'][0]]
        raw['secoes'][0]['texto'] = 'A espuma reduz a área disponível ao gás.'
        raw['alvos'] = raw['alvos'][:1]
        note, _, metrics = N.normalize_note(raw, {'F1': 'f1'}, [SOURCE])
        self.assertIsNone(N.insufficient_reason(note, metrics))

    def test_secao_parametrica_com_citacao_permanece_identificada(self):
        raw = self.raw()
        raw['secoes'][0].update(origem='parametrico', conhecimento_geral=True)
        note, _, _ = N.normalize_note(raw, {'F1': 'f1'}, [SOURCE])
        self.assertTrue(note['secoes'][0]['conhecimento_geral'])
        payload = N.note_payload(note, {'F1': 'f1'})
        self.assertEqual(payload['relacoes'][0]['fatos'], ['F1'])
        self.assertEqual(payload['alvos'][0]['criterios_correcao'], ['área de gás reduzida'])

    def test_revisor_nao_pode_apagar_proveniencia(self):
        note, _, metrics = N.normalize_note(self.raw(), {'F1': 'f1'}, [SOURCE])
        draft = {'nota': note, 'idmap': {'F1': 'f1'}, 'fontes_texto': [SOURCE]}
        final = self.raw()
        final.pop('schema_conhecimento')
        with self.assertRaisesRegex(ValueError, 'preservar'):
            R.make_validator(draft)({'decisao': 'corrigir', 'avaliacao': {k: 5 for k in R.CRITERIOS},
                                    'problemas': [], 'nota_final': final})


class Complemento(unittest.TestCase):
    def test_busca_exclui_usados_e_nao_aceita_so_um_termo(self):
        gaps = [{'lacuna': 'faltam critérios', 'consulta_pt': 'coalescencia gotas interface', 'consulta_en': ''}]
        chunks = [{'chunk_id': 'c1', 'texto': 'coalescencia de gotas na interface'},
                  {'chunk_id': 'c2', 'texto': 'coalescencia de gotas'},
                  {'chunk_id': 'c3', 'texto': 'interface isolada'}]
        self.assertEqual([c['chunk_id'] for c in CP.retrieve(gaps, chunks, ['c1'])], ['c2'])

    def test_complemento_preserva_novos_trechos_e_trilha(self):
        raw = note_v5_json(('F1',))
        note, alerts, measures = N.normalize_note(raw, {'F1': 'f1'}, [SOURCE])
        draft = {'nota': note, 'idmap': {'F1': 'f1'}, 'fontes_texto': [SOURCE], 'contexto': 'F1 fato'}
        extra = [{'chunk_id': 'extra', 'texto': SOURCE, 'lacuna': 'mecanismo'}]
        result = N.enrich_note(FakeLLM(), draft, extra, 'k1')
        self.assertEqual(result['idmap']['T1'], 'trecho:extra')
        self.assertEqual(result['complemento'][0]['chunk_id'], 'extra')
        self.assertEqual(result['antes_complemento'], note)


class Reconstrucao(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.root = Path(self.tmp.name)
        self.origin = self.root / 'original'
        folder = self.origin / 'subtopicos/prod-sep'
        folder.mkdir(parents=True)
        sub = {'key': 's1', 'dir': 'prod-sep', 'topico': 'Produção', 'subtopico': 'Separadores', 'frase': 'espuma'}
        assunto = {'id': 'a01', 'texto': 'espuma', 'generico': False}
        data = {'assuntos.json': {'subtopico': sub, 'assuntos': [assunto]},
                'conceitos.json': {'a01': {'conceitos': [{'kid': 's1:a01:k1', 'nome': 'espuma', 'fatos': ['f1']}],
                                           'descartados': []}},
                'selecao.json': {'assuntos': {'a01': {'info': {'colecoes': {'anp': 1}, 'selecionados': 1},
                      'trechos': [{'chunk_id': 'c1', 'texto': SOURCE, 'collection': 'anp', 'title': 'doc'}]}}}}
        for name, obj in data.items():
            (folder / name).write_text(json.dumps(obj), encoding='utf-8')
        (folder / 'fatos.jsonl').write_text(json.dumps(fact('f1')) + '\n', encoding='utf-8')

    def args(self):
        return ['--origens', str(self.origin), '--saida', str(self.root / 'nova'), '--embedder', 'hash']

    def test_plan_sem_apis_e_sem_criar_saida(self):
        self.assertEqual(RN.main(self.args() + ['--plan']), {'Separadores': 1})
        self.assertFalse((self.root / 'nova').exists())

    def test_refaz_so_notas_preserva_original_e_retoma(self):
        old = (self.origin / 'subtopicos/prod-sep/fatos.jsonl').read_bytes()
        RN.main(self.args(), llm=FakeLLM(), embedder=HashEmbedder())
        path = self.root / 'nova/subtopicos/prod-sep/notas_aprovadas.jsonl'
        note = json.loads(path.read_text(encoding='utf-8').splitlines()[0])
        self.assertEqual(note['schema_conhecimento'], K.SCHEMA)
        self.assertTrue(note['relacoes'][0]['avaliavel'])
        self.assertEqual(old, (self.origin / 'subtopicos/prod-sep/fatos.jsonl').read_bytes())
        RN.main(self.args(), llm=FakeLLM(), embedder=HashEmbedder())
        with self.assertRaisesRegex(ValueError, 'mudaram'):
            RN.main(self.args() + ['--effort', 'medium'], llm=FakeLLM(), embedder=HashEmbedder())

    def test_saida_na_origem_e_proibida(self):
        args = self.args()
        args[args.index('--saida') + 1] = str(self.origin / 'nova')
        with self.assertRaisesRegex(ValueError, 'saída nova'):
            RN.main(args)
