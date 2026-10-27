"""Seleção humana conservadora, gabarito explícito e avaliação separada por fonte."""
import csv
import threading
import unittest
from collections import Counter
from zipfile import ZipFile
from xml.sax.saxutils import escape

from pipeline.qa_research.especialista_qa import core as M
from pipeline.qa_research.especialista_qa.revisadas import (
    CONJUNTO_AUTORAL, CONJUNTO_REVISADAS, classificar_parecer, extrair_revisadas, ler_entradas)
from pipeline.qa_research.tests.test_especialista_qa import Fixture, Fake, original
from pipeline.qa_research.tests import test_especialista_qa as fixtures


def revisada():
    row = original()
    row.update(uid='especialista_revisada:0001', conjunto_especialista=CONJUNTO_REVISADAS,
               subtopico_original='Subtópico preservado', selecionada_para_conversao=True,
               revisao_humana={'parecer_original': 'aprovada', 'status': 'aprovada_sem_observacoes',
                              'aprovacao_simples': True})
    return row


class CuradoriaTests(Fixture):
    def docx(self, comments, *, bold_letters=('B',), bold_only_label=False):
        paras = ['<w:p><w:pPr><w:pStyle w:val="Ttulo1"/></w:pPr><w:r><w:t>Área original</w:t></w:r></w:p>',
                 '<w:p><w:pPr><w:pStyle w:val="Ttulo2"/></w:pPr><w:r><w:t>Sub original</w:t></w:r></w:p>']
        for i, comment in enumerate(comments, 1):
            paras.append(f'<w:p><w:r><w:t>{i}. O que avalia o OEE?</w:t></w:r></w:p>')
            for letter, text in zip('ABCD', ('Alpha', 'Beta', 'Gamma', 'Delta')):
                bold = '<w:rPr><w:b/></w:rPr>' if letter in bold_letters else ''
                if bold_only_label:
                    runs = f'<w:r>{bold}<w:t>{letter}) </w:t></w:r><w:r><w:t>{text}</w:t></w:r>'
                else:
                    runs = f'<w:r>{bold}<w:t>{letter}) {text}</w:t></w:r>'
                paras.append('<w:p>'+runs+'</w:p>')
            paras.append('<w:p><w:r><w:t>'+escape(comment)+'</w:t></w:r></w:p>')
        source = self.root/'revisadas.docx'
        with ZipFile(source, 'w') as z:
            z.writestr('word/document.xml', '<w:document xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main"><w:body>'+''.join(paras)+'</w:body></w:document>')
            z.writestr('word/styles.xml', '<w:styles xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main"><w:style w:styleId="Ttulo1"><w:name w:val="heading 1"/></w:style><w:style w:styleId="Ttulo2"><w:name w:val="heading 2"/></w:style></w:styles>')
        return source

    def test_so_aprovacao_simples_incluindo_rotulos_com_erros_conhecidos(self):
        source = self.docx(['Comentário: aprovada', 'Comentário: aprovada com ressalvas',
                           'Comentário: descartar', 'Comentário: aprovada, mas cenário repetido',
                           'Comenário: aprovada.', 'Comentário : aprovar', 'Comentário: aprovda',
                           'Comentário: não aprovada', 'Comentário: aprovada. Distratores fracos'])
        summary = extrair_revisadas(source, self.root/'extraidas')
        selected = M.ler_linhas(self.root/'extraidas/aprovadas_mcq.jsonl')
        self.assertEqual(summary['total_mcq'], 9)
        self.assertEqual([r['numero_original'] for r in selected], [1, 5, 6])
        self.assertTrue(all(r['gabarito'] == 'B' and r['resposta_original'] == 'Beta' for r in selected))
        self.assertEqual(selected[0]['agrupamento_original'], 'Área original')
        self.assertEqual(selected[0]['subtopico_original'], 'Sub original')
        self.assertEqual(len(M.ler_linhas(self.root/'extraidas/curadoria_todas.jsonl')), 9)

    def test_nao_adivinha_gabarito_por_negrito_parcial_ou_multiplas_alternativas(self):
        for bold, partial in [((), False), (('A', 'B'), False), (('B',), True)]:
            with self.subTest(bold=bold, partial=partial):
                source = self.docx(['Comentário: aprovada'], bold_letters=bold, bold_only_label=partial)
                summary = extrair_revisadas(source, self.root/'extraidas')
                self.assertEqual(summary['selecionadas'], 0)

    def test_entrada_publicada_tem_1000_mcqs_e_apenas_446_aprovadas(self):
        folder = M.ENTRADA.parent/'revisadas'
        allrows = M.ler_linhas(folder/'curadoria_todas.jsonl')
        selected = ler_entradas(folder/'aprovadas_mcq.jsonl')
        summary = M.read_json(folder/'extracao.json')
        self.assertEqual(len(allrows), 1000)
        self.assertEqual({r['numero_original'] for r in allrows}, set(range(1, 1001)))
        self.assertEqual(len(selected), 446)
        self.assertEqual(summary['selecionadas']+summary['excluidas'], 1000)
        self.assertEqual([d['total'] for d in summary['por_agrupamento']], [100]*10)
        self.assertTrue(all(r['status_extracao'] == 'ok' and r['revisao_humana']['aprovacao_simples'] for r in selected))
        self.assertTrue(all(len(r['evidencias_gabarito']) == 1 for r in selected))
        self.assertTrue(all(classificar_parecer(r['revisao_humana']['parecer_original']) == 'aprovada_sem_observacoes' for r in selected))
        # Rótulos digitados incorretamente não devem fazer perder pareceres explícitos.
        self.assertTrue({513, 607, 822, 858}.issubset(r['numero_original'] for r in selected))
        self.assertFalse(any(r['numero_original'] == 510 for r in selected))
        self.assertEqual(len({r['fonte']['docx_sha256'] for r in allrows}), 1)

    def test_manifesto_combina_2992_ids_distintos_sem_alterar_autorais(self):
        before = M.ENTRADA_AUTORAL.read_bytes()
        rows = ler_entradas(M.ENTRADA)
        self.assertEqual(Counter(r['conjunto_especialista'] for r in rows),
                         {CONJUNTO_AUTORAL: 2546, CONJUNTO_REVISADAS: 446})
        self.assertEqual(len({r['uid'] for r in rows}), 2992)
        self.assertEqual(M.ENTRADA_AUTORAL.read_bytes(), before)

    def test_bloqueia_ressalva_mesmo_com_booleano_de_aprovacao_true(self):
        row = revisada()
        row['revisao_humana']['parecer_original'] = 'aprovada, mas cenário fora da realidade'
        M.jsonl(self.input, [row])
        fake = Fake()
        with self.assertRaisesRegex(ValueError, 'aprovação humana'):
            self.runner(fake)
        self.assertEqual(fake.calls, [])

    def test_bloqueia_revisada_disfarcada_de_autoral(self):
        row = revisada()
        row['conjunto_especialista'] = CONJUNTO_AUTORAL
        M.jsonl(self.input, [row])
        with self.assertRaisesRegex(ValueError, 'fonte incorreta'):
            self.runner()


class IntegracaoFontesTests(Fixture):
    def test_conversao_e_avaliacao_preservam_fontes_e_separam_denominadores(self):
        M.jsonl(self.input, [original(1), original(2), revisada()])
        before = self.base.read_bytes(), self.raw.read_bytes()
        fake = Fake()
        self.assertEqual(self.runner(fake).run(), 0)
        qs = M.ler_linhas(self.out/'aprovadas.jsonl')
        reviewed = next(q for q in qs if q['conjunto_especialista'] == CONJUNTO_REVISADAS)
        self.assertEqual(reviewed['revisao_humana'], revisada()['revisao_humana'])
        self.assertEqual(reviewed['subtopico_original'], 'Subtópico preservado')
        self.assertTrue(reviewed['aprovada'])
        summary = M.read_json(self.out/'resultado.json')
        self.assertEqual(summary['por_conjunto_especialista'][CONJUNTO_AUTORAL]['aprovadas_qa'], 2)
        self.assertEqual(summary['por_conjunto_especialista'][CONJUNTO_REVISADAS]['aprovadas_qa'], 1)
        manifest = M.read_json(self.out/'bancos/manifesto.json')
        self.assertEqual([d['questoes'] for d in manifest['bancos']], [2, 2, 5])
        self.assertEqual(manifest['especialista_por_conjunto'], {CONJUNTO_AUTORAL: 2, CONJUNTO_REVISADAS: 1})
        self.assertEqual((self.base.read_bytes(), self.raw.read_bytes()), before)
        self.assertEqual(len({q['pergunta'] for q in qs}), 1)  # Duplicatas válidas continuam presentes.
        self.assertFalse(any('revisao_humana' in payload['original'] for _, payload, _ in fake.calls))

        from pipeline.qa_research.especialista_qa.avaliacao import avaliar
        barrier = threading.Barrier(2)
        a, b = fixtures.EvaluationTests.Responder(barrier), fixtures.EvaluationTests.Responder(barrier)
        clients = {'resp_gpt-5-4-nano': a, 'resp_gpt-5-4': b, 'juiz': fixtures.EvaluationTests.Judge()}
        self.assertEqual(avaliar(self.out, clientes=clients, progress=lambda *a, **k: None), 0)
        acc = M.read_json(self.out/'avaliacao/acuracia.json')
        for model in ('gpt-5-4-nano', 'gpt-5-4'):
            self.assertEqual(acc['geral'][model]['n'], 3)
            self.assertEqual(acc['por_conjunto_especialista'][CONJUNTO_AUTORAL][model]['n'], 2)
            self.assertEqual(acc['por_conjunto_especialista'][CONJUNTO_REVISADAS][model]['n'], 1)
        judgments = M.ler_linhas(self.out/'avaliacao/avaliacoes.jsonl')
        self.assertEqual(Counter(q['conjunto_especialista'] for q in judgments), {CONJUNTO_AUTORAL: 2, CONJUNTO_REVISADAS: 1})
        self.assertTrue(all(user == qs[0]['pergunta'] for user in a.users+b.users))
        with (self.out/'avaliacao/acuracia_por_conjunto.csv').open(encoding='utf-8-sig') as f:
            self.assertEqual(len(list(csv.DictReader(f))), 4)
        self.assertEqual(avaliar(self.out, clientes=clients, progress=lambda *a, **k: None), 0)
        self.assertEqual(len(a.users), 3)


if __name__ == '__main__':
    unittest.main()
