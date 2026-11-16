"""Teste offline do refino com modelo simulado e corpus mínimo.

    python -m unittest pipeline.qa_research.refino.tests.test_refino -v
"""
import asyncio
import hashlib
import json
import re
import tempfile
import unittest
from pathlib import Path
from types import SimpleNamespace

from pipeline.qa_research.refino import contracts as C, textos as T
from pipeline.qa_research.refino import prompts as P, semantica as S
from pipeline.qa_research.refino.__main__ import configuration, execute, collect, HERE

TEXTO = ('O sistema de alívio do FPSO coleta descargas das válvulas de segurança no header e conduz o gás '
         'ao vaso knock out antes da torre do flare, onde os pilotos garantem a ignição imediata.')


def response(data):
    return SimpleNamespace(choices=[SimpleNamespace(message=SimpleNamespace(content=json.dumps(data, ensure_ascii=False)),
                                                    finish_reason='stop')],
                           usage=SimpleNamespace(prompt_tokens=10, completion_tokens=10))


class Fake:
    """Modelo simulado que respeita os contratos a partir da própria entrada."""
    def __init__(self):
        self.calls = 0

    async def __call__(self, role, messages, tokens):
        self.calls += 1
        system, payload = messages[0]['content'], json.loads(messages[1]['content'])
        if system == P.MAPA:
            ids = [d['id'] for d in payload['documentos']]
            return response(dict(conceitos=[dict(conceito=f'conceito {i}', dono=ids[i % len(ids)], motivo='teste',
                                                 mencoes=[dict(doc=ids[(i + 1) % len(ids)], enfoque='enfoque de teste')])
                                            for i in range(12)]))
        if system == P.PLANO:
            gaps = [g['id'] for g in payload['lacunas']]
            blocks = [b['id'] for b in payload['base']]
            sections = []
            for i in range(1, 5):
                sid = f'S{i:02d}'
                mine = gaps[i - 1::4] if i > 1 else []
                sections.append(dict(id=sid, tipo='introducao' if i == 1 else 'desenvolvimento', titulo=f'Seção {i} do sistema de alívio',
                                     objetivo='explicar componentes e funções do sistema',
                                     conhecimentos=[dict(id=f'{sid}K01', descricao='componentes do sistema de alívio e flare',
                                                         lacunas=mine, essencial=True)],
                                     blocos_base=blocks[i - 1::4],
                                     consultas=[dict(pt='sistema de alívio e flare em FPSO', en='FPSO relief and flare system')]))
            leftover = [g for g in gaps if g not in {x for s in sections for k in s['conhecimentos'] for x in k['lacunas']}]
            return response(dict(secoes=sections, blocos_descartados=[],
                                 lacunas_fora_de_escopo=[dict(id=g, justificativa='pertence a outro documento da coleção') for g in leftover]))
        if system.startswith(P.RASCUNHO):
            k = [x['id'] for x in payload['secao']['conhecimentos']]
            claims = [dict(id=f'A{i:02d}', texto=f'{TEXTO} Afirmação {i} da perspectiva {payload["redator"]}.',
                           conhecimentos=k, tipo='componente', especifico=False) for i in range(1, 5)]
            claims.append(dict(id='A05', texto='A pressão de ajuste típica da válvula é de 10 bar acima da operação normal.',
                               conhecimentos=k, tipo='controle', especifico=True))
            return response(dict(afirmacoes=claims))
        if system == P.LEITURA:
            pids = [p['id'] for p in payload['passagens']]
            k = [x['id'] for x in payload['secao']['conhecimentos']]
            first = not payload['achados_anteriores']
            return response(dict(achados=[dict(id=f'F{i:02d}', texto=TEXTO + f' Achado {i}.', fontes=[pid], conhecimentos=k,
                                               condicoes='FPSO', jurisdicao='BR') for i, pid in enumerate(pids[:2], 1)],
                                 verificacoes=[dict(afirmacao=payload['afirmacoes'][0]['id'], estado='apoia', fontes=pids[:1], nota='ok')],
                                 lacunas=k if first else [],
                                 novas_consultas=[dict(pt='vaso knock out do flare', en='flare knock out drum')] if first else []))
        if system == P.CONSOLIDACAO:
            claims = [a for a in payload['afirmacoes']]
            keep = [a for a in claims if not a['especifico']]
            findings = [f['id'] for f in payload['achados']]
            blocks = [b['id'] for b in payload['blocos']]
            k = [x['id'] for x in payload['secao']['conhecimentos']]
            units = []
            for i in range(0, len(keep), 3):
                group = keep[i:i + 3]
                units.append(dict(id=f'U{len(units) + 1:02d}', texto=TEXTO + f' Unidade {len(units) + 1}.', conhecimentos=k,
                                  origem=dict(afirmacoes=[a['id'] for a in group], achados=findings if not units else [],
                                              blocos=blocks if not units else [])))
            if not units:
                units.append(dict(id='U01', texto=TEXTO, conhecimentos=k, origem=dict(afirmacoes=[], achados=findings, blocos=blocks)))
            return response(dict(unidades=units, descartadas=[dict(ref=a['id'], motivo='valor_sem_fonte') for a in claims if a['especifico']],
                                 conflitos=[]))
        if system == P.REDACAO:
            sid, units = payload['secao']['id'], [u['id'] for u in payload['unidades']]
            half = max(1, len(units) // 2)
            parts = [units[:half], units[half:]] if len(units) > 1 else [units]
            return response(dict(blocos=[dict(id=f'{sid}B{i:02d}', subtitulo=f'Bloco {i} de {sid}',
                                              texto=(TEXTO + ' ') * 2 + f'Explicação didática {sid} {i}.', unidades=p)
                                         for i, p in enumerate(parts, 1) if p]))
        if system == P.CONSOLIDA_DOC:
            pairs = payload['pares_internos']
            ops = [dict(bloco=pairs[0]['b'], novo_texto='Texto consolidado sem repetição sobre os pilotos do flare e a purga do header, '
                        'com remissão à seção anterior para os componentes já descritos.', motivo='repetição literal',
                        informacao_preservada_em=[pairs[0]['a']])] if pairs else []
            return response(dict(operacoes=ops))
        if system == P.REVISAO:
            blocks = [b['id'] for b in payload['blocos']]
            return response(dict(cobertura=[dict(id=g['id'], estado='parcial', blocos=blocks[:1], nota='') for g in payload['lacunas']],
                                 problemas=[dict(bloco=blocks[1], tipo='superficial', descricao='falta detalhar o vaso',
                                                 correcao='explicar o knock out drum')], parecer='bom com ajustes'))
        if system == P.COBERTURA_BASE:
            blocks = [b['id'] for b in payload['blocos']]
            state = 'atendido' if blocks[0].startswith('S') else 'ausente'
            return response(dict(cobertura=[dict(id=g['id'], estado=state, blocos=[], nota='') for g in payload['lacunas']]))
        if system == P.REPARO:
            return response(dict(blocos=[dict(id=b['id'], subtitulo=b['subtitulo'],
                                              texto=b['texto'] + ' O vaso knock out separa líquidos arrastados antes da queima no flare.')
                                         for b in payload['blocos']]))
        raise AssertionError('Prompt inesperado para o papel ' + role)


def corpus(root):
    root = Path(root)
    (root / 'teste').mkdir(parents=True)
    pages = [dict(collection='teste', document_id=f'doc{i}', title=f'Manual {i}', url=f'https://exemplo.org/{i}',
                  page=1, language='pt', jurisdiction='BR', source_boundary='known_document',
                  text=(TEXTO + ' ') * 30 + f' Documento {i} sobre flare, header, knock out e pilotos.')
             for i in range(6)]
    path = root / 'teste' / 'pages.jsonl'
    path.write_text(''.join(json.dumps(p, ensure_ascii=False) + '\n' for p in pages), encoding='utf-8')
    manifest = dict(schema='petroquest-professional-corpora-v1', ready=True, partial=True, sample=False,
                    collections=[dict(id='teste', format='pages_jsonl', path='teste/pages.jsonl',
                                      sha256=hashlib.sha256(path.read_bytes()).hexdigest(), documents=6)])
    (root / 'manifest.json').write_text(json.dumps(manifest), encoding='utf-8')
    return root / 'manifest.json'


def entradas(folder):
    """Duas entradas reais, reduzidas para o teste."""
    out = {}
    for item in ('02_08', '09_01'):
        e = json.loads((HERE / 'entradas' / f'{item}.json').read_text(encoding='utf-8'))
        e['base']['capitulos'] = e['base']['capitulos'][:2]
        out[item] = e
    return out


class RefinoTest(unittest.TestCase):
    def test_contracts_and_text(self):
        self.assertTrue(T.lint('O cabeçalho de gás inerte e a linga'))
        self.assertFalse(T.lint('O header de gás inerte e a eslinga'))
        self.assertTrue(T.has_value('ajuste de 10 bar'))
        self.assertFalse(T.has_value('conforme a NR-13 e a API 754'))
        with self.assertRaises(ValueError):
            C.redacao(dict(blocos=[dict(id='S01B01', subtitulo='x', texto='a fonte afirma ' + 'palavra ' * 30, unidades=['U01'])]), ['U01'], 'S01')
        doc = dict(titulo='t', capitulos=[dict(titulo='c', blocos=[dict(id='a', subtitulo='s', texto=TEXTO),
                                                                    dict(id='b', subtitulo='s', texto=TEXTO)])])
        self.assertGreater(T.redundancy(doc)['taxa_redundancia'], 0.9)

    def test_semantic_redundancy_with_fake_embeddings(self):
        class Emb:
            async def create(self, model, input, dimensions):
                vec = lambda t: [1.0, 0.0] if 'flare' in t else [0.0, 1.0]
                return SimpleNamespace(data=[SimpleNamespace(embedding=vec(t)) for t in input])
        calls = SimpleNamespace(client=SimpleNamespace(embeddings=Emb()))
        doc = dict(titulo='t', capitulos=[dict(titulo='c', blocos=[
            dict(id='a', subtitulo='s', texto='A torre do flare queima o gás de alívio com segurança na unidade.'),
            dict(id='b', subtitulo='s', texto='O gás aliviado é queimado no flare de forma controlada e segura.'),
            dict(id='c', subtitulo='s', texto='A amarra de ancoragem é inspecionada por ROV em campanhas periódicas.')])])
        spec = dict(deployment='x', dimensions=2, threshold=0.9)
        with tempfile.TemporaryDirectory() as tmp:
            r = asyncio.run(S.redundancy(calls, doc, spec, Path(tmp) / 'e.json'))
        self.assertAlmostEqual(r['taxa_redundancia_semantica'], 2 / 3, places=3)

    def test_pipeline_offline_and_resume(self):
        with tempfile.TemporaryDirectory() as tmp:
            tmp = Path(tmp)
            manifest = corpus(tmp / 'corpus')
            config = configuration(HERE / 'config_piloto.json')
            config.update(max_calls=80, research_rounds=2, consolidation_rounds=1)
            fake = Fake()
            data = entradas(tmp)
            result = asyncio.run(execute(data, ['02_08', '09_01'], [manifest], tmp / 'saida', config, tmp / 'cache',
                                         tmp / 'sem_legado', transport=fake))
            self.assertEqual(result['status'], 'concluido', json.dumps(result, ensure_ascii=False)[:2000])
            for item in ('02_08', '09_01'):
                folder = tmp / 'saida' / item
                doc = json.loads((folder / 'documento.json').read_text(encoding='utf-8'))
                self.assertTrue(doc['capitulos'][0]['titulo'].startswith('Seção 1'))
                self.assertEqual(set(doc['capitulos'][0]['blocos'][0]), {'subtitulo', 'texto'})
                metrics = json.loads((folder / 'metricas.json').read_text(encoding='utf-8'))
                self.assertIn('evidencia', metrics['proveniencia']['por_estatuto'])
                self.assertEqual(metrics['rascunhos']['descartadas_por_motivo'].get('valor_sem_fonte'), 4 * 3)
                self.assertGreater(metrics['cobertura']['depois']['atendido'], metrics['cobertura']['antes']['atendido'])
                prov = json.loads((folder / 'proveniencia.json').read_text(encoding='utf-8'))
                self.assertTrue(all(not re.search(r'texto', json.dumps(v)) for v in prov['fontes'].values()))
                self.assertIn('Refino:', (folder / 'RELATORIO.md').read_text(encoding='utf-8'))
            used = fake.calls
            # Retomada: mesma saída, nenhuma chamada nova ao modelo.
            again = asyncio.run(execute(data, ['02_08', '09_01'], [manifest], tmp / 'saida', config, tmp / 'cache',
                                        tmp / 'sem_legado', transport=fake))
            self.assertEqual(again['status'], 'concluido')
            self.assertEqual(fake.calls, used)
            collect(tmp / 'saida', tmp / 'coleta')
            self.assertTrue((tmp / 'coleta' / '02_08' / 'documento.md').is_file())
            self.assertFalse(any('.local' in p.parts for p in (tmp / 'coleta').rglob('*')))


if __name__ == '__main__':
    unittest.main()
