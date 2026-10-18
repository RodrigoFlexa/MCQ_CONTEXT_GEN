"""QA com juiz, refino, resolução independente, resposta cega e novidade; sem afirmações atômicas."""
import copy

from pipeline.inventario.textutil import atomic_json, read_json
from . import contracts as C, qa_prompts as P


QUESTION_KEYS = ('status', 'pergunta', 'resposta', 'explicacao', 'competencia', 'rubrica', 'fontes', 'motivo')


def brief_question(record):
    return {k: record.get(k) for k in ('id', 'pergunta', 'resposta', 'competencia', 'rubrica')}


def generate(engine, document, qid, previous, examples):
    path = engine.out / 'questoes' / (qid + '.json')
    state = read_json(path) or {
        'id': qid, 'documento_id': document['id'], 'status': 'em_andamento', 'etapa': 'geracao',
        'pauta': document['pauta'], 'versoes': [], 'revisoes': [], 'refinamentos': 0,
        'busca_complementar_usada': False, 'evidencias': copy.deepcopy(document['evidencias']),
        'consultas_realizadas': [], 'validacao_humana': 'pendente',
    }
    if state['status'] in ('aprovada', 'reprovada', 'redundante', 'evidencia_insuficiente', 'pendente_validacao'):
        return state
    engine.begin_scope(qid, engine.args.max_chamadas_questao)
    state.update(status='em_andamento')
    state.pop('erro', None)
    accepted = [r for r in previous if r['status'] == 'aprovada']
    styles = examples.choose({'descricao': document['documento']['titulo'], 'habilidade': 'aplicacao'},
                             document['pauta']['topico'])
    state['exemplos'] = {key: [e['id'] for e in values] for key, values in styles.items()}

    def save():
        atomic_json(path, state)

    def finish(status, reason):
        state.update(status=status, motivo=reason, etapa='concluida')
        if state.get('questao', {}).get('status') == 'ok':
            for key in QUESTION_KEYS:
                if key not in ('status', 'motivo') and key in state['questao']:
                    state[key] = state['questao'][key]
        save()
        return state

    def material():
        return {'pauta': document['pauta'], 'capitulo_revisado': document['documento'],
                'fontes_originais': state['evidencias']}

    save()
    while True:
        stage = state['etapa']
        if stage == 'geracao':
            question = engine.call('pesquisador', P.GENERATE,
                                   {'material': material(), 'exemplos': styles,
                                    'itens_anteriores': [brief_question(r) for r in accepted],
                                    'tentativas_anteriores': [
                                        {'pergunta': r.get('pergunta', r.get('questao', {}).get('pergunta')),
                                         'motivo': r.get('motivo')} for r in previous[-10:]]},
                                   'qa_geracao', qid + ':geracao',
                                   lambda d: C.question(d, state['evidencias']), 9000)
            state['questao'] = {k: question[k] for k in QUESTION_KEYS if k in question}
            if question['status'] != 'ok':
                return finish('evidencia_insuficiente', question['motivo'])
            state['versoes'].append(copy.deepcopy(state['questao']))
            state['etapa'] = 'nucleo'
            save()
        elif stage == 'nucleo':
            state['nucleo'] = engine.call('revisor', P.NUCLEUS,
                                         {'material': material(), 'pergunta': state['questao']['pergunta']},
                                         'qa_nucleo', qid + ':nucleo', C.answer, 6000)
            state['etapa'] = 'juiz'
            save()
        elif stage == 'juiz':
            judgment = engine.call('revisor', P.JUDGE,
                                   {'material': material(), 'questao': state['questao'],
                                    'resolucao_sem_gabarito': state['nucleo'],
                                    'calibracao_defeitos': examples.anchors()},
                                   'qa_juiz', qid + ':juiz',
                                   lambda d: C.review(d, ('aprovar', 'refinar', 'pesquisar', 'rejeitar')), 10000)
            state['revisoes'].append({**judgment, 'versao': len(state['versoes']) - 1,
                                      'fontes_disponiveis': [e['id'] for e in state['evidencias']]})
            if judgment['decisao'] == 'aprovar':
                state['etapa'] = 'cego'
            elif judgment['decisao'] == 'rejeitar':
                return finish('reprovada', judgment['parecer'])
            elif judgment['decisao'] == 'pesquisar':
                if state['busca_complementar_usada']:
                    return finish('evidencia_insuficiente', judgment['parecer'])
                state['busca_complementar_usada'] = True
                added = engine.retrieve(state, judgment['consultas'])
                if not added:
                    return finish('evidencia_insuficiente', 'Busca complementar sem nova evidência: ' + judgment['parecer'])
                state['etapa'] = 'nucleo'
            else:
                state['feedback'] = judgment
                state['etapa'] = 'refino'
            save()
        elif stage == 'refino':
            if state['refinamentos'] >= engine.args.max_refinamentos_qa:
                return finish('reprovada', 'Limite de refinamentos; consulte os pareceres')
            revised = engine.call('refinador', P.REFINE,
                                  {'material': material(), 'questao': state['questao'],
                                   'parecer': state['feedback']},
                                  'qa_refino', qid + ':refino',
                                  lambda d: C.question_refinement(d, state['evidencias']), 9000)
            if revised['status'] == 'pesquisar':
                state.setdefault('pedidos_refinador', []).append(revised)
                if state['busca_complementar_usada']:
                    return finish('evidencia_insuficiente', revised['motivo'])
                state['busca_complementar_usada'] = True
                if not engine.retrieve(state, revised['consultas']):
                    return finish('evidencia_insuficiente', revised['motivo'])
                state['feedback'] = {'parecer_original': state['feedback'], 'pedido_refinador': revised}
                save()
                continue
            if revised['status'] != 'ok':
                return finish('evidencia_insuficiente', revised['motivo'])
            state['questao'] = {k: revised[k] for k in QUESTION_KEYS if k in revised}
            state['versoes'].append(copy.deepcopy(state['questao']))
            state['refinamentos'] += 1
            state['etapa'] = 'nucleo'
            save()
        elif stage == 'cego':
            # O respondente nunca recebe capítulo, fontes, rubrica ou gabarito.
            state['cego'] = engine.call('respondente', P.BLIND,
                                       {'pergunta': state['questao']['pergunta']},
                                       'qa_cego', qid + ':cego', C.answer, 6000)
            state['etapa'] = 'adjudicacao'
            save()
        elif stage == 'adjudicacao':
            comparison = engine.call('revisor', P.ADJUDICATE,
                                     {'material': material(), 'questao': state['questao'],
                                      'resposta_cega': state['cego']},
                                     'qa_adjudicacao', qid + ':adjudicacao', C.adjudication, 7000)
            state.setdefault('adjudicacoes', []).append({**comparison, 'cego': state['cego'],
                                                         'versao': len(state['versoes']) - 1})
            if comparison['veredito'] == 'indeterminado':
                return finish('pendente_validacao', comparison['parecer'])
            if comparison['veredito'] in ('ambiguidade_item', 'erro_referencia'):
                state['feedback'] = comparison
                state['etapa'] = 'refino'
            else:
                state['etapa'] = 'novidade'
            save()
        elif stage == 'novidade':
            if accepted:
                current = {'id': qid, **state['questao']}
                novelty = engine.call('novidade', P.NOVELTY,
                                      {'nova': brief_question(current),
                                       'anteriores': [brief_question(r) for r in accepted]},
                                      'qa_novidade', qid + ':novidade',
                                      lambda d: C.novelty(d, [r['id'] for r in accepted]), 7000)
            else:
                novelty = {'comparacoes': []}
            state['novidade'] = novelty
            if any(r['classe'] == 'redundante' for r in novelty['comparacoes']):
                return finish('redundante', 'Competência já coberta; consulte comparações')
            return finish('aprovada', 'Juiz, adjudicação e novidade concluídos; revisão humana pendente')
        else:
            raise ValueError(f'Etapa de QA desconhecida: {stage}')
