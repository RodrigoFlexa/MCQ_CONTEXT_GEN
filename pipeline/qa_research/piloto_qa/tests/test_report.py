import csv
import io
import tempfile
import unittest
from contextlib import redirect_stdout
from pathlib import Path
from pipeline.inventario.textutil import atomic_json
from pipeline.qa_research.piloto_qa.documents import prepare
from pipeline.qa_research.piloto_qa.metrics import calculate
from pipeline.qa_research.piloto_qa.evaluation import evaluate
from pipeline.qa_research.piloto_qa.report import write
from pipeline.qa_research.piloto_qa.__main__ import collect
from pipeline.qa_research.piloto_qa.tests.test_pilot import EvalClient


class ReportTests(unittest.TestCase):
    def test_all_three_groups_quality_tables_and_html_collection(self):
        with tempfile.TemporaryDirectory() as tmp,redirect_stdout(io.StringIO()):
            output=Path(tmp)/'run';prepare(output/'contextos',['02_02'])
            atomic_json(output/'protocolo.json',dict(items=['02_02']))
            groups={g:[dict(uid=g+':a',grupo=g,item='02_02',tipo='mecanismo',composicao='simples',cenario=False,origem=g,
                pergunta='Como a restrição altera a vazão?',resposta='A restrição altera a vazão.',
                contexto_tecnico='A restrição altera a vazão.',blocos_contexto=[dict(id='B1',texto='A restrição altera a vazão.')])]
                for g in ('historico','novo_antigo','novo_refinado')}
            calculate(groups,output/'metricas')
            clients={k:EvalClient() for k in ['resp_gpt-4-1-nano','resp_gpt-4-1-mini','resp_gpt-4-1','juiz','faithfulness']}
            evaluate([q for qs in groups.values() for q in qs],output/'avaliacao_comparavel',clients=clients)
            write(output,groups)
            md=(output/'TABELAS.md').read_text(encoding='utf-8')
            web=(output/'TABELAS.html').read_text(encoding='utf-8')
            self.assertIn('Novo + contexto refinado',md);self.assertIn('IC 95% gap',md)
            self.assertIn('Sustentação dos gabaritos',md);self.assertIn('100.00',md)
            self.assertEqual(web.count('<table>'),web.count('</table>'));self.assertGreaterEqual(web.count('<table>'),10)
            for file in (output/'tabelas').glob('*.csv'):
                with file.open(encoding='utf-8-sig',newline='') as stream:rows=list(csv.reader(stream))
                self.assertTrue(all(len(row)==len(rows[0]) for row in rows))
            collect(output,Path(tmp)/'collected');self.assertTrue((Path(tmp)/'collected/TABELAS.html').exists())
            # Não apresentar avaliação antiga quando o banco tiver crescido.
            groups['novo_refinado'].append(dict(groups['novo_refinado'][0],uid='novo_refinado:b'))
            write(output,groups)
            self.assertNotIn('100.00',(output/'TABELAS.md').read_text(encoding='utf-8'))


if __name__=='__main__':unittest.main()
