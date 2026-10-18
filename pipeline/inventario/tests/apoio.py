"""Dados e LLM simulado compartilhados pelos testes do inventário."""
import hashlib
import json
import re

from pipeline.inventario import assuntos as A, combinacoes as M, consolidacao as C, extracao as X, notas as N, revisao as R
from pipeline.inventario.llm import CallFailed, ContentFiltered

SOURCE = ('A espuma no separador reduz a área disponível ao escoamento do gás e aumenta o arraste de líquido para a '
          'linha de gás. Impurezas e queda de pressão na entrada favorecem a formação de espuma. O controle de nível '
          'fica instável quando há espuma e o tempo de retenção de 3 minutos deixa de ser efetivo. ')
QUOTE = 'A espuma no separador reduz a área disponível ao escoamento do gás e aumenta o arraste de líquido'
QUOTE2 = 'Impurezas e queda de pressão na entrada favorecem a formação de espuma'


def fact(fid, conceito='espuma em separadores', assuntos=('a01',), coll='anp', tipo='causa_efeito', score=0.6,
         afirmacao='A espuma reduz a área de escoamento do gás e aumenta o arraste de líquido.', chunk='c1'):
    return {'fid': fid, 'conceito': conceito, 'tipo': tipo, 'afirmacao': afirmacao, 'condicoes': 'separadores de produção',
            'assuntos': list(assuntos), 'pertinencia': 'fpso_direta', 'citacao': QUOTE, 'numeros_nao_verificados': [],
            'score': score, 'sub_key': 's1',
            'fonte': {'chunk_id': chunk, 'collection': coll, 'document_id': chunk, 'title': chunk + '.pdf',
                      'jurisdiction': 'BR', 'page_ini': 1}}


def note_json(refs=('F1', 'F2'), status='ok', texto=None, geral=False):
    texto = texto or ('A espuma reduz a área disponível ao escoamento do gás no separador. Com menos área, a velocidade '
                      'do gás aumenta e gotas de líquido são arrastadas para a linha de gás. Impurezas e queda de pressão '
                      'na entrada favorecem a espuma, o que torna o controle de nível instável.')
    return {'status': status, 'titulo': 'Espuma em separadores de produção',
            'resumo': 'A espuma reduz a área de escoamento do gás e favorece o arraste de líquido.',
            'secoes': [{'tipo': 'principio_mecanismo', 'texto': texto, 'fatos': list(refs), 'conhecimento_geral': geral},
                       {'tipo': 'problemas_diagnostico', 'texto': texto, 'fatos': list(refs), 'conhecimento_geral': False},
                       {'tipo': 'decisoes_criterios', 'texto': 'Quando houver espuma, o operador deve avaliar a queda de '
                        'pressão na entrada e a presença de impurezas antes de alterar o nível, porque ambas favorecem a '
                        'formação de espuma e o arraste.', 'fatos': list(refs)[:1], 'conhecimento_geral': False}],
            'alvos': [{'nivel': 'facil', 'descricao': 'Efeito da espuma na área de gás.'},
                      {'nivel': 'dificil', 'descricao': 'Diagnosticar arraste de líquido com nível instável.'}],
            'correcoes': [], 'lacunas': []}


def note_v5_json(refs=('F1', 'F2'), **kwargs):
    raw = note_json(refs, **kwargs)
    raw.update(schema_conhecimento='nota-v5', relacoes=[{
        'id': 'R1', 'afirmacao': 'A espuma reduz a área de escoamento e favorece arraste de líquido.',
        'origem': 'fonte', 'natureza': 'principio', 'aplicabilidade': 'fpso',
        'condicoes': ['separador com espuma'], 'limites': ['não define a única causa de arraste'],
        'fatos': list(refs), 'premissas': []}], buscas_complementares=[])
    for target in raw['alvos']:
        target.update(relacoes=['R1'], habilidade='compreensao' if target['nivel'] == 'facil' else 'aplicacao',
                      resposta='Redução da área e aumento do arraste.', criterios_correcao=['área de gás reduzida'],
                      condicoes_enunciado=['há espuma no separador'])
    return raw


class FakeLLM:
    """Responde a cada etapa conforme o prompt de sistema; falhas configuráveis por etapa."""
    fail = {}          # etapa -> 'filtro' | 'falha' | 'todos_falha'

    def __init__(self, *args, **kwargs):
        self.usage = {'calls': 0, 'cached': 0, 'prompt_tokens': 0, 'completion_tokens': 0, 'errors': 0,
                      'filtro_conteudo': 0, 'reparos': 0}
        self.seen = {}

    def close(self):
        pass

    def _maybe_fail(self, stage, item):
        mode = self.fail.get(stage)
        first = self.seen.setdefault(stage, item) == item
        if mode == 'filtro' and first:
            raise ContentFiltered('Filtro de conteúdo simulado', tag=stage, item=item)
        if mode == 'falha' and first:
            raise CallFailed('validação simulada', kind='validacao', tag=stage, item=item)
        if mode == 'todos_falha':
            raise CallFailed('serviço simulado indisponível', kind='transitorio', tag=stage, item=item)

    def json(self, system, user, tag='', max_tokens=0, validate=None, item=None):
        self.usage['calls'] += 1
        if system == A.SYSTEM:
            phrase = user.split('"""')[1]
            data = {'assuntos': [{'texto': phrase, 'generico': False, 'consulta_pt': 'espuma em separadores',
                                  'consulta_en': 'foam in separators', 'termos_pt': ['espuma', 'arraste'],
                                  'termos_en': ['foam', 'carryover']}]}
        elif system == X.SYSTEM:
            self._maybe_fail('fatos', item)
            data = {'fatos': [
                {'conceito': 'espuma em separadores', 'tipo': 'causa_efeito', 'afirmacao': 'A espuma reduz a área de '
                 'escoamento do gás e aumenta o arraste de líquido para a linha de gás.', 'condicoes': 'separadores',
                 'assuntos': ['a01'], 'pertinencia': 'fpso_direta', 'citacao': QUOTE},
                {'conceito': 'espuma em separadores', 'tipo': 'mecanismo', 'afirmacao': 'Impurezas e queda de pressão '
                 'na entrada favorecem a formação de espuma no separador.', 'condicoes': '', 'assuntos': ['a01'],
                 'pertinencia': 'transferivel', 'citacao': QUOTE2},
                {'conceito': 'x', 'tipo': 'definicao', 'afirmacao': 'Afirmação com citação inventada no trecho.',
                 'condicoes': '', 'assuntos': ['a01'], 'pertinencia': 'transferivel',
                 'citacao': 'esta frase não existe no trecho de origem de forma alguma'}]}
        elif system == C.SYSTEM:
            ids = re.findall(r'^(F\d+) ', user, flags=re.M)
            data = {'conceitos': [{'nome': 'Espuma e arraste em separadores', 'foco': 'mecanismo e diagnóstico',
                                   'relevancia': 'alta', 'fatos': ids[:-1]}],
                    'descartados': [{'fato': ids[-1], 'motivo': 'redundante'}]}
        elif system == N.SYSTEM:
            self._maybe_fail('notas', item)
            refs = tuple(re.findall(r'^(F\d+) ', user, flags=re.M)[:2])
            data = note_v5_json(refs)
        elif system == R.SYSTEM:
            data = {'decisao': 'aprovar', 'avaliacao': {k: 5 for k in R.CRITERIOS}, 'problemas': [], 'motivo': 'ok',
                    'nota_final': None}
        elif system == M.SYSTEM:
            self._maybe_fail('combinacoes', item)
            ids = re.findall(r'^(N\d+): ', user, flags=re.M)
            data = {'combinacoes': [{'notas': ids[:2], 'titulo': 'Espuma e nível', 'ligacao': 'a espuma mascara o nível',
                                     'raciocinio': 'integrar espuma e controle de nível', 'cenario': 'Nível oscila.',
                                     'resposta': 'A espuma mascara o nível.', 'criterios_correcao': ['integrar as relações'],
                                     'condicoes_enunciado': ['há espuma'], 'limites': [],
                                     'conhecimentos': [{'nota': sid, 'conhecimento': 'espuma', 'relacoes': ['R1']}
                                                      for sid in ids[:2]]}],
                    'observacao': ''}
        else:
            raise AssertionError('Chamada inesperada: ' + system[:60])
        if validate:
            validate(data)
        return data


def corpus_fixture(root, collections=('petroles', 'anp', 'hse', 'bsee', 'regis')):
    entries = []
    for c in collections:
        path = root / f'{c}.jsonl'
        lang = 'en' if c in ('hse', 'bsee') else 'pt'
        rows = [{'collection': c, 'document_id': f'{c}-{d}', 'title': f'{c}-{d}.pdf', 'language': lang,
                 'jurisdiction': 'BR', 'page': 1, 'text': ' '.join(
                     SOURCE + ' '.join(f'{c}{d}termo{j} registro{k}{c}' for j in range(25)) for k in range(6))}
                for d in (1, 2)]
        path.write_text('\n'.join(json.dumps(r, ensure_ascii=False) for r in rows) + '\n', encoding='utf-8')
        entries.append({'id': c, 'documents': 2, 'format': 'pages_jsonl', 'path': path.name,
                        'sha256': hashlib.sha256(path.read_bytes()).hexdigest()})
    path = root / 'manifest.json'
    path.write_text(json.dumps({'schema': 'petroquest-domain-corpora-v1', 'ready': True, 'sample': True,
                                'collections': entries}), encoding='utf-8')
    return path
