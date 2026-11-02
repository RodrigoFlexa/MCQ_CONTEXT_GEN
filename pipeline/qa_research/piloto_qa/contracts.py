import re
from pipeline.qa_research.v3.contracts import require, text, rows, exact, strings, TYPES
from pipeline.qa_research.v2.language import lint_ptbr

FLAGS = ('suporte', 'correta', 'autonoma', 'determinada', 'sem_pistas', 'distinta', 'composicao')


def evidence(value, blocks):
    require(isinstance(value, list) and value, 'Evidências não vazias obrigatórias')
    for e in value:
        require(isinstance(e, dict) and e.get('bloco') in blocks and text(e.get('trecho')),
                'Evidência deve indicar bloco e trecho')
        require(e['trecho'] in blocks[e['bloco']]['texto'], 'Trecho precisa ser literal no bloco indicado')


def planned(data, blocks, limit):
    targets = rows(data.get('alvos'), 'alvos')
    require(len(targets) <= limit, 'Alvos excedem limite')
    for t in targets:
        require(t.get('tipo') in TYPES and t.get('composicao') in ('simples', 'composta'), 'Classe/composição inválida')
        require(text(t.get('conhecimento')) and isinstance(t.get('ponte'), str), 'Declare conhecimento e ponte')
        require(t['composicao'] != 'composta' or text(t['ponte']), 'Composta exige ponte')
        require(t['tipo'] != 'conceito' or t['composicao'] == 'simples', 'Conceito deve ser simples')
        require(isinstance(t.get('afirmacoes'), list) and t['afirmacoes'], 'Selecione afirmações antes de escrever')
        require(t['composicao'] != 'composta' or len(t['afirmacoes']) >= 2, 'Composta exige duas relações')
        for a in t['afirmacoes']:
            require(isinstance(a, dict) and text(a.get('afirmacao')), 'Afirmação obrigatória')
            evidence(a.get('evidencias'), blocks)
    strings(data.get('impedimentos'), 'impedimentos')


def authored(data, targets, blocks, limit):
    questions = rows(data.get('questoes'), 'questoes')
    require(len(questions) <= limit and {q['id'] for q in questions} <= set(targets), 'Alvo desconhecido ou lote excedido')
    for q in questions:
        require(text(q.get('pergunta')) and text(q.get('resposta')), 'Pergunta/resposta obrigatórias')
        require(type(q.get('cenario')) is bool, 'Declare cenário')
        require(targets[q['id']]['tipo'] not in ('diagnostico', 'decisao') or q['cenario'], 'Cenário obrigatório')
        require(len(q['pergunta'].split()) <= 90 and len(q['resposta'].split()) <= 60, 'Limites: pergunta 90, resposta 60 palavras')
        require(not re.search(r'\b(segundo o texto|no documento|o trecho consultado|nos blocos)\b', q['pergunta'], re.I), 'Pergunta deve ser autônoma')
        require(not lint_ptbr(q['pergunta'] + ' ' + q['resposta']), 'Redija em PT-BR')
        criteria = rows(q.get('criterios'), 'criterios')
        require(criteria, 'Rubrica mínima obrigatória')
        for c in criteria:
            require(text(c.get('criterio')) and isinstance(c.get('inferencia'), str), 'Critério e inferência explícitos')
            evidence(c.get('evidencias'), blocks)
        strings(q.get('equivalentes'), 'equivalentes'); strings(q.get('erros_materiais'), 'erros_materiais')
    strings(data.get('impedimentos'), 'impedimentos')


def judged(data, questions, blocks, admitted):
    exact(data.get('avaliacoes'), questions, 'avaliacoes')
    previous = set(admitted)
    for row in data['avaliacoes']:
        require(row.get('decisao') in ('admitir', 'corrigir', 'descartar', 'lacuna_documental') and text(row.get('motivo')), 'Parecer inválido')
        flags = row.get('criterios', {})
        require(all(type(flags.get(k)) is bool for k in FLAGS), 'Sete critérios booleanos')
        require(isinstance(row.get('correcao'), str), 'Correção deve ser texto')
        require(row['decisao'] != 'corrigir' or text(row['correcao']), 'Indique reparo concreto')
        checks = row.get('checagem_essenciais')
        expected = {c['id'] for c in questions[row['id']]['criterios']}
        exact(checks, expected, 'checagem_essenciais')
        for c in checks:
            require(type(c.get('sustentado')) is bool and text(c.get('justificativa')), 'Suporte explícito por essencial')
            if c['sustentado']: evidence(c.get('evidencias'), blocks)
        dup = row.get('duplicada_de')
        require(dup is None or (dup in previous and row['decisao'] == 'descartar'), 'Duplicata deve apontar a admitida anterior')
        require(row['decisao'] != 'admitir' or (all(flags.values()) and all(c['sustentado'] for c in checks) and dup is None), 'Admissão contradiz critérios')
        if row['decisao'] == 'admitir': previous.add(row['id'])
