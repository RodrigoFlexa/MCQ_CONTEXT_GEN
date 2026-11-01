"""Contratos de polimento, sem permitir reconstrução silenciosa do documento."""
from pipeline.qa_research.v3.contracts import require, text, strings, rows, exact, refs, pairs

KINDS = ('correcao_tecnica', 'lacuna_essencial', 'aprofundamento', 'editorial')
FLAGS = ('correta', 'suportada', 'condicoes_preservadas', 'sem_perda', 'escopo', 'autonomia', 'pt_br')
TYPES = ('explicacao_tecnica', 'resultado_experimental', 'recomendacao', 'opiniao', 'norma', 'indeterminado')


def coverage(value, points):
    exact(value, points, 'cobertura')
    for row in value:
        require(row.get('estado') in ('atendido', 'parcial', 'ausente') and text(row.get('motivo')),
                row['id'] + ': cobertura inválida')


def diagnosis(data, blocks, chapters, points, limit):
    interventions = rows(data.get('intervencoes'), 'intervencoes')
    require(len(interventions) <= limit, 'Plano excedeu o limite de intervenções')
    occupied = set()
    for row in interventions:
        require(row.get('tipo') in KINDS, row['id'] + ': tipo de intervenção inválido')
        require(row.get('prioridade') in ('alta', 'media', 'baixa'), row['id'] + ': prioridade inválida')
        require(text(row.get('objetivo')) and text(row.get('motivo')), row['id'] + ': objetivo e motivo obrigatórios')
        refs(row.get('alvos'), set(blocks) | set(chapters) | {'DOCUMENTO'}, row['id'] + '.alvos')
        refs(row.get('pontos'), points, row['id'] + '.pontos')
        # Não há duas propostas independentes editando o mesmo texto original.
        touched = set(row['alvos']) & set(blocks)
        require(not touched & occupied, row['id'] + ': alvo já atribuído a outra intervenção; agrupe os reparos')
        occupied.update(touched)
        pairs(row.get('consultas'), row['id'] + '.consultas', empty=row['tipo'] == 'editorial')
    coverage(data.get('cobertura'), points)
    strings(data.get('omissoes_escopo'), 'omissoes_escopo')


def research(data, paragraphs):
    require(type(data.get('suficiente')) is bool, 'suficiente deve ser booleano')
    require(isinstance(data.get('achados'), list) and len(data['achados']) <= 8, 'Até oito achados por leitura')
    for row in data['achados']:
        require(isinstance(row, dict) and text(row.get('proposicao')), 'Achado precisa de proposição')
        refs(row.get('citacoes'), paragraphs, 'achado.citacoes')
        require(row.get('tipo') in TYPES, 'Estatuto da afirmação inválido')
        require(row.get('pertinencia') in ('direta', 'contextual'), 'Declare pertinencia direta ou contextual ao objetivo')
        strings(row.get('condicoes'), 'achado.condicoes')
        strings(row.get('limites'), 'achado.limites')
    pairs(data.get('consultas_adicionais'), 'consultas_adicionais', empty=True)
    strings(data.get('pendencias'), 'pendencias')


def editing(data, interventions):
    exact(data.get('itens'), interventions, 'itens')
    for row in data['itens']:
        require(isinstance(row.get('alteracoes'), list), row['id'] + ': alteracoes deve ser array')
        strings(row.get('pendencias'), row['id'] + '.pendencias')


def judgment(data, interventions):
    exact(data.get('avaliacoes'), interventions, 'avaliacoes')
    for row in data['avaliacoes']:
        require(row.get('decisao') in ('aprovar', 'corrigir', 'rejeitar') and text(row.get('motivo')), 'Parecer inválido')
        flags = row.get('criterios')
        require(isinstance(flags, dict) and all(type(flags.get(k)) is bool for k in FLAGS), 'Critérios booleanos obrigatórios')
        require(isinstance(row.get('correcao'), str), 'correcao deve ser texto')
        require(row['decisao'] != 'aprovar' or all(flags[k] for k in FLAGS), 'Aprovação contradiz critérios')
        require(row['decisao'] != 'corrigir' or text(row['correcao']), 'Indique reparo concreto')


def final_review(data, blocks, points):
    require(type(data.get('protecoes_preservadas')) is bool, 'Declare protecoes_preservadas explicitamente')
    coverage(data.get('cobertura'), points)
    require(isinstance(data.get('problemas'), list), 'problemas deve ser array')
    for row in data['problemas']:
        require(isinstance(row, dict) and text(row.get('descricao')) and type(row.get('critico')) is bool, 'Problema inválido')
        refs(row.get('blocos'), blocks, 'problema.blocos', empty=True)
        require(row.get('tipo') in ('editorial', 'tecnico'), 'Problema precisa de tipo editorial ou tecnico')
    strings(data.get('omissoes_escopo'), 'omissoes_escopo')


def editorial_review(data, blocks):
    require(isinstance(data.get('problemas'), list), 'problemas editoriais deve ser array')
    for row in data['problemas']:
        require(isinstance(row, dict) and text(row.get('descricao')), 'Descreva o defeito editorial concreto')
        refs(row.get('blocos'), blocks, 'problema editorial.blocos')
