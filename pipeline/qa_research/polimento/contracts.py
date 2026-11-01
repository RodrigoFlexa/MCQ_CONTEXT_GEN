"""Contratos de polimento, sem permitir reconstrução silenciosa do documento."""
import re

from pipeline.qa_research.v3.contracts import require, text, strings, rows, exact, refs, pairs

KINDS = ('correcao_tecnica', 'lacuna_essencial', 'aprofundamento', 'editorial')
FLAGS = ('correta', 'suportada', 'condicoes_preservadas', 'sem_perda', 'escopo', 'autonomia', 'pt_br')
TYPES = ('explicacao_tecnica', 'resultado_experimental', 'recomendacao', 'opiniao', 'norma', 'indeterminado')
DEFECTS = ('repeticao_entre_capitulos', 'relato_de_leitura', 'termo_ingles', 'organizacao')


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
        objectives = rows(row.get('sub_objetivos'), row['id'] + '.sub_objetivos')
        require((not objectives if row['tipo'] == 'editorial' else 1 <= len(objectives) <= 3),
                row['id'] + ': decomponha a intervenção técnica em 1 a 3 sub_objetivos; editorial usa []')
        for objective in objectives:
            require(re.fullmatch(r'S[1-3]', objective['id']) and text(objective.get('descricao')),
                    row['id'] + ': sub_objetivo precisa de ID S1..S3 e descrição verificável')
    coverage(data.get('cobertura'), points)
    strings(data.get('omissoes_escopo'), 'omissoes_escopo')


def research(data, paragraphs, sub_ids):
    require(type(data.get('suficiente')) is bool, 'suficiente deve ser booleano')
    require(isinstance(data.get('achados'), list) and len(data['achados']) <= 8, 'Até oito achados por leitura')
    for row in data['achados']:
        require(isinstance(row, dict) and text(row.get('proposicao')), 'Achado precisa de proposição')
        refs(row.get('citacoes'), paragraphs, 'achado.citacoes')
        require(row.get('tipo') in TYPES, 'Estatuto da afirmação inválido')
        require(row.get('pertinencia') in ('direta', 'contextual'), 'Declare pertinencia direta ou contextual ao objetivo')
        refs(row.get('sub_objetivos_atendidos'), sub_ids, 'achado.sub_objetivos_atendidos', empty=True)
        require(row['pertinencia'] != 'direta' or row['sub_objetivos_atendidos'],
                'Achado direto exige sub_objetivos_atendidos válidos')
        require(row['pertinencia'] != 'contextual' or not row['sub_objetivos_atendidos'],
                'Achado contextual não cobre sub_objetivos')
        strings(row.get('condicoes'), 'achado.condicoes')
        strings(row.get('limites'), 'achado.limites')
    pairs(data.get('consultas_adicionais'), 'consultas_adicionais', empty=True)
    strings(data.get('pendencias'), 'pendencias')


def normalize_operations(item, expected=None):
    """IDs faltantes/ilegais são atribuídos antes de validar ou persistir a resposta."""
    seen = set()
    changes = item['alteracoes']
    pattern = re.escape(item['id']) + r'_OP(?:0[1-9]|[1-9][0-9]+)'
    reserved = {r.get('op_id') for r in changes if isinstance(r, dict)
                and isinstance(r.get('op_id'), str)
                and re.fullmatch(pattern, r['op_id'])}
    for index, row in enumerate(changes, 1):
        require(isinstance(row, dict), 'Alteração deve ser objeto')
        oid = row.get('op_id')
        if not isinstance(oid, str) or not re.fullmatch(pattern, oid) or oid in seen:
            oid = expected[index - 1] if expected and index <= len(expected) else f'{item["id"]}_OP{index:02d}'
            suffix = index
            while oid in seen or (oid in reserved and not expected):
                suffix += 1
                oid = f'{item["id"]}_OP{suffix:02d}'
            row['op_id'] = oid
        seen.add(oid)


def editing(data, interventions, repair_operations=None):
    exact(data.get('itens'), interventions, 'itens')
    for row in data['itens']:
        require(isinstance(row.get('alteracoes'), list), row['id'] + ': alteracoes deve ser array')
        strings(row.get('pendencias'), row['id'] + '.pendencias')
        expected = [oid for oid, op in (repair_operations or {}).items() if op['intervencao_id'] == row['id']]
        normalize_operations(row, expected)
        if repair_operations is not None:
            require({op['op_id'] for op in row['alteracoes']} == set(expected),
                    'Reparo deve conter somente os op_id solicitados')
            for op in row['alteracoes']:
                original = repair_operations[op['op_id']]
                authorized = original.get('alvos_autorizados', [original.get('alvo')])
                require(all(op.get(k) == original.get(k) for k in ('operacao', 'destino'))
                        and (op.get('alvo') == original.get('alvo') if original.get('alvo') in authorized else op.get('alvo') in authorized),
                        'Reparo não pode mudar operação, alvo ou destino do op_id')


def judgment(data, operations):
    evaluations = data.get('avaliacoes_operacoes')
    require(isinstance(evaluations, list) and all(isinstance(r, dict) for r in evaluations),
            'avaliacoes_operacoes deve ser array de objetos')
    ids = [r.get('op_id') for r in evaluations]
    require(all(isinstance(oid, str) for oid in ids) and len(set(ids)) == len(ids)
            and set(ids) == set(operations), 'Parecer deve cobrir exatamente cada op_id proposto')
    for row in evaluations:
        require(row.get('intervencao_id') == operations[row['op_id']]['intervencao_id'],
                'Parecer associou op_id à intervenção incorreta')
        require(row.get('decisao') in ('aprovar', 'corrigir', 'rejeitar') and text(row.get('motivo')), 'Parecer inválido')
        flags = row.get('criterios')
        require(isinstance(flags, dict) and all(type(flags.get(k)) is bool for k in FLAGS), 'Critérios booleanos obrigatórios')
        require(isinstance(row.get('correcao'), str), 'correcao deve ser texto')
        require(row['decisao'] != 'aprovar' or all(flags[k] for k in FLAGS), 'Aprovação contradiz critérios')
        require(row['decisao'] != 'corrigir' or text(row['correcao']), 'Indique reparo concreto')


def final_review(data, blocks, points):
    require(type(data.get('protecoes_preservadas')) is bool, 'Declare protecoes_preservadas explicitamente')
    coverage(data.get('cobertura'), points)
    for row in data['cobertura']:
        require(isinstance(row.get('evidencia_regressao'), str), 'Declare evidencia_regressao (ou texto vazio)')
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
        require(len(row['blocos']) <= 3 and row.get('tipo_defeito') in DEFECTS,
                'Defeito editorial precisa de tipo_defeito válido e até três blocos acoplados')
