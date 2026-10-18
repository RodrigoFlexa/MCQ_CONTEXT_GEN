"""Validação de transporte e referências; decisões técnicas pertencem à revisão com fontes."""
import re

CITATION = re.compile(r'\[E(\d+)\]')


def text(value, field):
    if not isinstance(value, str) or not value.strip():
        raise ValueError(f'{field}: esperado texto não vazio, recebido {type(value).__name__}')
    return value.strip()


def texts(value, field, maximum=None):
    if not isinstance(value, list) or any(not isinstance(v, str) or not v.strip() for v in value):
        raise ValueError(f'{field}: esperado lista de textos (use [] se vazio), recebido {type(value).__name__}')
    if maximum is not None and len(value) > maximum:
        raise ValueError(f'{field}: no máximo {maximum} textos')
    return value


def enum(data, field, values):
    value = data.get(field)
    if not isinstance(value, str) or value not in values:
        raise ValueError(f'{field}: permitido {list(values)}, recebido {value!r}')
    return value


def references(value, evidences, field, required=True):
    refs = texts(value, field)
    allowed = {e['id'] for e in evidences}
    invalid = [v for v in refs if v not in allowed]
    if invalid or (required and not refs):
        raise ValueError(f'{field}: IDs permitidos {sorted(allowed)}; inválidos {invalid}; '
                         f'lista não vazia obrigatória={required}')
    return refs


def research(data):
    action = enum(data, 'acao', ('buscar', 'redigir', 'insuficiente'))
    text(data.get('orientacao'), 'orientacao')
    queries = texts(data.get('consultas'), 'consultas', 3)
    if action == 'buscar' and not queries:
        raise ValueError('consultas: acao=buscar exige ao menos uma consulta não vazia')


def review(data, values=('aprovar', 'refinar', 'pesquisar', 'insuficiente')):
    decision = enum(data, 'decisao', values)
    text(data.get('parecer'), 'parecer')
    queries = texts(data.get('consultas'), 'consultas', 3)
    if decision == 'pesquisar' and not queries:
        raise ValueError('consultas: decisao=pesquisar exige ao menos uma consulta não vazia')


def document(data, evidences):
    text(data.get('titulo'), 'titulo')
    body = text(data.get('texto_markdown'), 'texto_markdown')
    listed = references(data.get('fontes'), evidences, 'fontes')
    cited = {'E' + n for n in CITATION.findall(body)}
    if set(listed) != cited:
        raise ValueError(f'fontes deve listar exatamente as citações [E#] do texto; '
                         f'citadas={sorted(cited)}, listadas={sorted(set(listed))}')


def refinement(data, evidences):
    if data.get('acao') == 'pesquisar':
        text(data.get('orientacao'), 'orientacao da pesquisa solicitada')
        if not texts(data.get('consultas'), 'consultas', 3):
            raise ValueError('consultas: refinador solicita pesquisa com ao menos uma consulta')
        return
    document(data, evidences)


def question(data, evidences):
    status = enum(data, 'status', ('ok', 'insuficiente'))
    if status == 'insuficiente':
        text(data.get('motivo'), 'motivo')
        return
    for key in ('pergunta', 'resposta', 'explicacao', 'competencia'):
        text(data.get(key), key)
    if not texts(data.get('rubrica'), 'rubrica'):
        raise ValueError('rubrica: lista não vazia obrigatória')
    references(data.get('fontes'), evidences, 'fontes')
    if CITATION.search(data['pergunta']) or CITATION.search(data['resposta']):
        raise ValueError('pergunta/resposta: retire referências [E#]; mantenha IDs somente em fontes')


def question_refinement(data, evidences):
    if data.get('status') == 'pesquisar':
        text(data.get('motivo'), 'motivo da pesquisa solicitada')
        if not texts(data.get('consultas'), 'consultas', 3):
            raise ValueError('consultas: refinador solicita pesquisa com ao menos uma consulta')
        return
    question(data, evidences)


def answer(data):
    text(data.get('resposta'), 'resposta')


def adjudication(data):
    enum(data, 'veredito', ('equivalentes', 'parcial_sem_contradicao', 'erro_respondente',
                           'ambiguidade_item', 'erro_referencia', 'indeterminado'))
    text(data.get('parecer'), 'parecer')


def novelty(data, ids):
    rows = data.get('comparacoes')
    if not isinstance(rows, list) or any(not isinstance(r, dict) for r in rows):
        raise ValueError('comparacoes: lista de objetos obrigatória')
    received = [r.get('id') for r in rows]
    if any(not isinstance(i, str) for i in received) or len(received) != len(ids) or set(received) != set(ids):
        raise ValueError(f'comparacoes: exatamente uma linha para cada ID {ids}; recebidos {received}')
    for row in rows:
        enum(row, 'classe', ('redundante', 'sobreposicao', 'distinta'))
        text(row.get('parecer'), 'parecer da comparação')
