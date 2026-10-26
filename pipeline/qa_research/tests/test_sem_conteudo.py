"""Testes offline da geração bruta: repetições e questões fracas não impedem a meta."""
import copy
import io
import json
import tempfile
import unittest
from contextlib import redirect_stdout
from pathlib import Path
from unittest.mock import patch

from pipeline.qa_research.sem_conteudo import core as M
from pipeline.qa_research.sem_conteudo.__main__ import main


def question():
    # Deliberadamente fraca e incompatível com a rubrica de qualidade: deve ser preservada.
    return dict(tipo='diagnostico', cenario=False, composicao='simples',
                pergunta='É adequado manter o equipamento?', resposta='Sim, depende das condições.')


class Fake:
    def __init__(self, fail_at=None, same=True):
        self.requests = []
        self.cache = {}
        self.network = 0
        self.fail_at = fail_at
        self.same = same

    def json(self, system, user, tag='', validate=None, **kw):
        if tag != 'sem_conteudo_geracao':
            raise AssertionError('Auditoria, refinamento ou dedup não devem ser chamados')
        payload = json.loads(user)
        self.requests.append(payload)
        key = (system, user)
        if key in self.cache:
            result = copy.deepcopy(self.cache[key])
        else:
            if self.fail_at == len(self.requests):
                self.fail_at = None
                raise RuntimeError('falha de API simulada')
            self.network += 1
            qs = [question() for _ in range(payload['quantidade'])]
            if not self.same:
                for i, q in enumerate(qs):
                    q['pergunta'] = f"Qual é a função do componente {payload['lote']}-{i}?"
            result = {'questoes': qs}
            self.cache[key] = copy.deepcopy(result)
        if validate:
            validate(result)
        return result


class TestSemConteudo(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.root = Path(self.tmp.name)
        self.metas = self.root / 'metas.json'
        self.out = self.root / 'run'
        self.set_metas(3)

    def set_metas(self, n, second=False):
        items = [dict(id='01_01', topico='Gestão', subtopico='Desempenho',
                      frase_especialista='Avaliar os sistemas de um FPSO.', meta=n)]
        if second:
            items.append({**items[0], 'id': '02_01', 'subtopico': 'Medição', 'meta': 2})
        M.atomic_json(self.metas, dict(schema='metas-sem-conteudo-v1', run_referencia='run_antiga',
                                     total=n + (2 if second else 0), itens=items))

    def runner(self, fake=None, **kw):
        return M.GeracaoSemConteudo(self.out, metas=self.metas, clientes={'geracao': fake or Fake()},
                                   progress=lambda *a, **k: None, **kw)

    def test_metas_oficiais_e_programa(self):
        from pipeline.fase_3.topicos import TOPICOS
        d = M.carregar_metas()
        self.assertEqual(d['total'], 2818)
        self.assertEqual(len(d['itens']), 40)
        self.assertEqual(d['itens'][0]['meta'], 62)
        for i in d['itens']:
            self.assertEqual(i['frase_especialista'], TOPICOS[i['topico']][i['subtopico']])
        raw = (M.ROOT / 'pipeline/qa_research/relatorios' / d['run_referencia'] / 'aprovadas.jsonl').read_bytes().replace(b'\r\n', b'\n')
        self.assertEqual(__import__('hashlib').sha256(raw).hexdigest(), d['aprovadas_referencia_sha256'])
        counts = __import__('collections').Counter(json.loads(x)['item'] for x in raw.decode().splitlines() if x.strip())
        self.assertEqual({i['id']: i['meta'] for i in d['itens']}, dict(counts))

    def test_preserva_todas_as_duplicatas_e_questoes_fracas(self):
        self.set_metas(62)
        f = Fake()
        with patch('pipeline.qa_research.tipos.problemas_tipo', side_effect=AssertionError('Não filtrar')):
            self.assertEqual(self.runner(f).run(), 0)
        s = M.read_json(self.out / 'topicos/01_01/estado.json')
        self.assertEqual(len(s['questoes']), 62)
        self.assertEqual(len({q['pergunta'] for q in s['questoes']}), 1)
        self.assertEqual(f.network, 13)  # somente ceil(62/5) chamadas de geração
        self.assertEqual([p['quantidade'] for p in f.requests], [5] * 12 + [2])
        for q in s['questoes']:
            self.assertEqual({k: q[k] for k in M.CAMPOS}, question())
            self.assertEqual(q['avaliacao_qualidade'], 'nao_realizada')
            self.assertNotIn('aprovada', q)
            self.assertNotIn('auditoria', q)

    def test_saida_e_avaliacao_incluem_repetidas_sem_rotular_aprovadas(self):
        self.assertEqual(self.runner(lote=2).run(), 0)
        result = M.read_json(self.out / 'resultado.json')
        self.assertEqual(result['geradas'], 3)
        self.assertNotIn('aprovadas', result)
        self.assertFalse((self.out / 'aprovadas.jsonl').exists())
        from pipeline.qa_research.geracao_tipos.avaliacao import AvaliacaoModelos
        self.assertEqual(len(AvaliacaoModelos(self.out).carregar_questoes()), 3)
        self.assertEqual(M.read_json(self.out / 'topicos/01_01/finalizado.json')['geradas'], 3)

    def test_avaliador_legado_continua_lendo_apenas_aprovadas(self):
        from pipeline.qa_research.geracao_tipos.avaliacao import AvaliacaoModelos
        self.out.mkdir()
        a = {**question(), 'uid': 'A', 'item': '01_01'}
        b = {**question(), 'uid': 'B', 'item': '01_01'}
        M.GeracaoSemConteudo.jsonl(self.out / 'aprovadas.jsonl', [a])
        M.GeracaoSemConteudo.jsonl(self.out / 'questoes.jsonl', [a, b])
        self.assertEqual(set(AvaliacaoModelos(self.out).carregar_questoes()), {'A'})

    def test_memoria_limitada_e_sem_leitura_de_conteudo_externo(self):
        f = Fake(same=False)
        original = Path.read_text
        def guarded(path, *args, **kw):
            if path.name in ('aprovadas.jsonl', 'exemplos.json', 'banco_dinamico.json') or (
                    path.suffix == '.md' and 'prompts' not in str(path)):
                raise AssertionError('Leitura externa proibida: ' + str(path))
            return original(path, *args, **kw)
        with patch.object(Path, 'read_text', guarded):
            self.assertEqual(self.runner(f, lote=1, memoria=1).run(), 0)
        self.assertEqual(f.requests[0]['recentes'], [])
        self.assertEqual(len(f.requests[1]['recentes']), 1)
        self.assertEqual(f.requests[2]['recentes'][0]['pergunta'], 'Qual é a função do componente 2-0?')
        for payload in f.requests:
            self.assertEqual(set(payload), {'escopo', 'quantidade', 'lote', 'recentes'})
            self.assertEqual(set(payload['escopo']), {'topico', 'subtopico', 'frase_especialista'})

    def test_limite_parcial_nao_e_sucesso_e_retoma(self):
        f = Fake()
        self.assertEqual(self.runner(f, lote=1, max_lotes=1).run(), 2)
        self.assertFalse((self.out / 'geracao_concluida.json').exists())
        self.assertFalse((self.out / 'topicos/01_01/finalizado.json').exists())
        self.assertEqual(self.runner(f, lote=1, max_lotes=5).run(), 0)
        before = f.network
        self.assertEqual(self.runner(f, lote=1, max_lotes=5).run(), 0)
        self.assertEqual(f.network, before)

    def test_falha_de_api_preserva_lote_anterior(self):
        f = Fake(fail_at=2)
        self.assertEqual(self.runner(f, lote=1).run(), 2)
        s = M.read_json(self.out / 'topicos/01_01/estado.json')
        self.assertEqual(s['lotes'], 1)
        self.assertEqual(len(s['questoes']), 1)
        self.assertEqual(self.runner(f, lote=1).run(), 0)
        qs = [json.loads(x) for x in (self.out / 'questoes.jsonl').read_text(encoding='utf-8').splitlines()]
        self.assertEqual(len(qs), 3)
        self.assertEqual(len({q['uid'] for q in qs}), 3)

    def test_replay_usa_cache_apos_interrupcao_antes_do_checkpoint(self):
        f = Fake()
        g = self.runner(f)
        original = M.atomic_json
        failed = False
        def interrupt(path, data):
            nonlocal failed
            if Path(path).name == 'estado.json' and not failed and data.get('lotes') == 1:
                failed = True
                raise KeyboardInterrupt()
            return original(path, data)
        with patch.object(M, 'atomic_json', interrupt):
            with self.assertRaises(KeyboardInterrupt):
                g.run()
        self.assertEqual(self.runner(f).run(), 0)
        self.assertEqual(f.network, 1)
        self.assertEqual(M.read_json(self.out / 'resultado.json')['geradas'], 3)

    def test_configuracao_incompativel_bloqueia_retomada(self):
        self.runner().run()
        with self.assertRaisesRegex(ValueError, 'Configuração mudou'):
            self.runner(memoria=1).run()

    def test_nao_mistura_resultados_do_modo_antigo_filtrado(self):
        self.out.mkdir()
        old = {'schema': 'geracao-sem-conteudo-v1', 'itens': ['01_01']}
        M.atomic_json(self.out / 'config.json', old)
        with self.assertRaisesRegex(ValueError, 'run filtrada'):
            self.runner().run()
        self.assertEqual(M.read_json(self.out / 'config.json'), old)

    def test_topicos_paralelos_e_retomada_da_selecao(self):
        self.set_metas(3, second=True)
        self.assertEqual(self.runner(lote=2, workers=2).run(), 0)
        self.assertEqual(M.read_json(self.out / 'resultado.json')['geradas'], 5)
        other = self.root / 'other'
        g = M.GeracaoSemConteudo(other, metas=self.metas, itens=['02_01'],
                                clientes={'geracao': Fake()}, progress=lambda *a, **k: None)
        self.assertEqual(g.run(), 0)
        resumed = M.GeracaoSemConteudo(other, metas=self.metas, clientes={'geracao': Fake()})
        self.assertEqual([i['id'] for i in resumed.itens], ['02_01'])

    def test_plano_nao_cria_saida_nem_cliente(self):
        with patch.object(M.GeracaoSemConteudo, 'cliente', side_effect=AssertionError('Não chamar API')), redirect_stdout(io.StringIO()):
            self.assertEqual(main(['--saida', str(self.out), '--metas', str(self.metas), '--plano']), 0)
        self.assertFalse(self.out.exists())

    def test_validacao_e_somente_estrutural(self):
        M.validar_geracao({'questoes': [question(), question()]}, 2)
        for payload in [{'questoes': []}, {'questoes': [question()], 'auditoria': 'não usar'},
                        {'questoes': [{**question(), 'resposta': ''}]}]:
            with self.assertRaises(ValueError):
                M.validar_geracao(payload, 1)
        self.assertEqual(set(M.MODELOS), {'geracao'})
        self.assertFalse(hasattr(M.GeracaoSemConteudo, 'deduplicar'))
        self.assertFalse(hasattr(M.GeracaoSemConteudo, 'auditar'))


if __name__ == '__main__':
    unittest.main()
