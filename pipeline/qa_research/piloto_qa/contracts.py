import re
from pipeline.qa_research.v3.contracts import require, text, rows, exact, strings, TYPES
from pipeline.qa_research.v2.language import lint_ptbr

FLAGS = ('suporte', 'correta', 'autonoma', 'determinada', 'sem_pistas', 'distinta', 'composicao')


def evidence(value, blocks, location='evidencias'):
    require(isinstance(value, list) and value, location + ': evidências não vazias obrigatórias')
    for index, e in enumerate(value):
        where = f'{location}[{index}]'
        require(isinstance(e, dict) and e.get('bloco') in blocks and text(e.get('trecho')),
                where + ': evidência deve indicar bloco conhecido e trecho')
        require(e['trecho'] in blocks[e['bloco']]['texto'],
                where + ': Trecho precisa ser literal no bloco indicado ' + e['bloco'] + ': ' + repr(e['trecho'][:160]))


def planned(data, blocks, limit):
    targets = rows(data.get('alvos'), 'alvos')
    require(len(targets) <= limit, 'Alvos excedem limite')
    for t in targets:
        target(t, blocks)
    strings(data.get('impedimentos'), 'impedimentos')


def target(t, blocks):
    where = 'alvos[' + str(t.get('id')) + ']'
    try:
        require(t.get('tipo') in TYPES and t.get('composicao') in ('simples', 'composta'), 'Classe/composição inválida')
        require(text(t.get('conhecimento')) and isinstance(t.get('ponte'), str), 'Declare conhecimento e ponte')
        require(t['composicao'] != 'composta' or text(t['ponte']), 'Composta exige ponte')
        require(t['tipo'] != 'conceito' or t['composicao'] == 'simples', 'Conceito deve ser simples')
        require(isinstance(t.get('afirmacoes'), list) and t['afirmacoes'], 'Selecione afirmações antes de escrever')
        require(t['composicao'] != 'composta' or len(t['afirmacoes']) >= 2, 'Composta exige duas relações')
        for index, a in enumerate(t['afirmacoes']):
            require(isinstance(a, dict) and text(a.get('afirmacao')), 'Afirmação obrigatória')
            evidence(a.get('evidencias'), blocks, f'afirmacoes[{index}].evidencias')
        if t['composicao'] == 'composta':
            distinct = {' '.join(a['afirmacao'].casefold().split()) for a in t['afirmacoes']}
            require(len(distinct) >= 2, 'Composta exige relações distintas, não a mesma afirmação duplicada')
    except ValueError as exc:
        raise ValueError(where + ': ' + str(exc)) from exc


def authored(data, targets, blocks, limit):
    questions = rows(data.get('questoes'), 'questoes')
    require(len(questions) <= limit and {q['id'] for q in questions} <= set(targets), 'Alvo desconhecido ou lote excedido')
    for q in questions:
        question(q, targets[q['id']], blocks)
    strings(data.get('impedimentos'), 'impedimentos')


def question(q, target, blocks):
    where = 'questoes[' + str(q.get('id')) + ']'
    try:
        require(text(q.get('pergunta')) and text(q.get('resposta')), 'Pergunta/resposta obrigatórias')
        require(type(q.get('cenario')) is bool, 'Declare cenário')
        require(target['tipo'] not in ('diagnostico', 'decisao') or q['cenario'], 'Cenário obrigatório')
        require(len(q['pergunta'].split()) <= 90 and len(q['resposta'].split()) <= 60, 'Limites: pergunta 90, resposta 60 palavras')
        require(not re.search(r'\b(segundo o texto|no documento|o trecho consultado|nos blocos)\b', q['pergunta'], re.I), 'Pergunta deve ser autônoma')
        require(not lint_ptbr(q['pergunta'] + ' ' + q['resposta']), 'Redija em PT-BR')
        criteria = rows(q.get('criterios'), 'criterios')
        require(criteria, 'Rubrica mínima obrigatória')
        for c in criteria:
            require(text(c.get('criterio')) and isinstance(c.get('inferencia'), str), 'Critério e inferência explícitos')
            evidence(c.get('evidencias'), blocks, 'criterios[' + c['id'] + '].evidencias')
        strings(q.get('equivalentes'), 'equivalentes'); strings(q.get('erros_materiais'), 'erros_materiais')
    except ValueError as exc:
        raise ValueError(where + ': ' + str(exc)) from exc


def judged(data, questions, blocks, admitted):
    exact(data.get('avaliacoes'), questions, 'avaliacoes')
    previous = set(admitted)
    for row in data['avaliacoes']:
        judgment(row, questions[row['id']], blocks, previous)
        if row['decisao'] == 'admitir': previous.add(row['id'])


def judgment(row, question, blocks, admitted):
    where = 'avaliacoes[' + str(row.get('id')) + ']'
    try:
        require(row.get('decisao') in ('admitir', 'corrigir', 'descartar', 'lacuna_documental') and text(row.get('motivo')), 'Parecer inválido')
        flags = row.get('criterios', {})
        require(isinstance(flags, dict), 'criterios: esperado objeto com sete booleanos')
        require(all(type(flags.get(k)) is bool for k in FLAGS), 'Sete critérios booleanos')
        require(isinstance(row.get('correcao'), str), 'Correção deve ser texto')
        require(row['decisao'] != 'corrigir' or text(row['correcao']), 'Indique reparo concreto')
        checks = row.get('checagem_essenciais')
        expected = {c['id'] for c in question['criterios']}
        exact(checks, expected, 'checagem_essenciais')
        for c in checks:
            require(type(c.get('sustentado')) is bool and text(c.get('justificativa')), 'Suporte explícito por essencial')
            if c['sustentado']: evidence(c.get('evidencias'), blocks, 'checagem_essenciais[' + c['id'] + '].evidencias')
        dup = row.get('duplicada_de')
        require(dup is None or (dup in admitted and row['decisao'] == 'descartar'), 'Duplicata deve apontar a admitida anterior')
        require(row['decisao'] != 'admitir' or (all(flags[k] for k in FLAGS) and all(c['sustentado'] for c in checks) and dup is None), 'Admissão contradiz critérios')
    except ValueError as exc:
        raise ValueError(where + ': ' + str(exc)) from exc


def envelope(data):
    """Somente erro de JSON/envelope pode solicitar regeneração de transporte.

    Campos e linhas são julgados individualmente depois de salvar a resposta.
    """
    require(isinstance(data, dict), 'Envelope JSON deve ser objeto')
