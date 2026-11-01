"""Regressões do segundo piloto, sem API externa nem alteração dos datasets."""
import asyncio
import copy
import json
from pathlib import Path
from types import SimpleNamespace as NS
from unittest.mock import patch

import pytest

from pipeline.inventario.textutil import atomic_json, read_json
from pipeline.qa_research.polimento import contracts as C, prompts as P
from pipeline.qa_research.polimento.__main__ import configuration
from pipeline.qa_research.polimento.documents import apply_changes, build_review_payload, catalog
from pipeline.qa_research.polimento.finishing import cluster_problems, finish
from pipeline.qa_research.polimento.flow import polish, stabilize_coverage
from pipeline.qa_research.polimento.operations import edit_operations
from pipeline.qa_research.polimento.research import investigate
from pipeline.qa_research.v3.runtime import Calls, CallFailure


def response(value, finish='stop', raw=None):
    return NS(choices=[NS(finish_reason=finish, message=NS(content=raw if raw is not None else json.dumps(value)))],
              usage=NS(prompt_tokens=1, completion_tokens=1))


def document():
    return dict(titulo='Instrumentação e controle', capitulos=[dict(id=f'C{c:02d}', titulo=f'Capítulo {c}',
        grupo='Operação', blocos=[dict(id=f'B{c:02d}_{b:02d}', subtitulo=f'Mecanismo {b}',
            texto=f'A condição {c}.{b} depende da vazão e da pressão do processo.') for b in range(1, 4)])
        for c in range(1, 6)])


def base_data():
    return dict(item='07_01', entrada=dict(frase_especialista='Instrumentação e controle de sistemas em FPSO'),
        documento=document(), protecoes=[], pontos=[dict(id='F01', titulo='Controle')],
        resumo_anterior={}, fingerprints={'documento': 'teste'}, origem='base/documento.json', evidencias='ausente.jsonl')


def intervention(iid='I01', kind='editorial', targets=None):
    return dict(id=iid, tipo=kind, prioridade='alta', alvos=targets or ['B01_01', 'B01_02', 'B01_03'],
        pontos=['F01'], objetivo='Explicar o mecanismo com condições preservadas', motivo='Clareza técnica',
        sub_objetivos=[] if kind == 'editorial' else [dict(id='S1', descricao='Mecanismo de atuação')],
        consultas=[] if kind == 'editorial' else [dict(pt='controle vazão bomba', en='pump flow control')])


def change(oid, target, operation='substituir', **kwargs):
    return dict(op_id=oid, operacao=operation, alvo=target, subtitulo='Mecanismo e condições',
        texto='A equipe verifica a vazão e a pressão antes do ajuste do processo.', motivo='Clareza',
        preservacao='Mantém o mecanismo e as condições anteriores', achados=[], complementos=[], **kwargs)


def judgment(oid, iid, decision='aprovar'):
    flags = dict.fromkeys(C.FLAGS, True)
    if decision != 'aprovar':
        flags['autonomia'] = False
    return dict(op_id=oid, intervencao_id=iid, decisao=decision, motivo='Conferência localizada',
        correcao='Converter a frase em explicação direta' if decision == 'corrigir' else '', criterios=flags)


def test_review_payload_does_not_flag_new_insertion_as_duplicate():
    base = base_data()
    plan = intervention('I02', 'lacuna_essencial', ['C05'])
    proposal = dict(id='I02', alteracoes=[change('I02_OP01', 'C05', 'inserir')], pendencias=[])
    original = copy.deepcopy(base)
    payload = build_review_payload(base, [plan], [proposal], {}, [])
    operation = payload['intervencoes_e_operacoes_propostas'][0]['operacoes'][0]
    assert operation['status_existencia_alvo'] == 'CRIACAO_DE_BLOCO_OU_CAPITULO_NOVO_NESTA_PROPOSTA'
    assert operation['estado_anterior_do_bloco'] is None
    existing = {b['bloco_id'] for c in payload['mapa_estrutural_documento_vigente_ANTES_deste_lote'] for b in c['blocos_existentes']}
    assert 'N_I02_1' not in existing
    assert 'N_I02_1' in catalog(apply_changes(base['documento'], [proposal]))[1]
    assert base == original


@pytest.mark.parametrize('editorial', [False, True])
def test_operation_level_commit_and_partial_repair(tmp_path, editorial):
    base = base_data()
    iid = 'E01' if editorial else 'I01'
    item = intervention(iid)
    original = dict(itens=[dict(id=iid, alteracoes=[change(f'{iid}_OP{b:02d}', f'B01_{b:02d}') for b in range(1, 4)], pendencias=[])])
    committed, decisions, errors, inputs = [], {}, [], []
    saved = tmp_path / 'documento.json'

    def checkpoint():
        atomic_json(saved, apply_changes(base['documento'], committed))

    class Model:
        config = configuration()
        async def call(self, role, tag, payload, validate, **kwargs):
            inputs.append((tag, copy.deepcopy(payload)))
            if role == 'write':
                if tag.endswith('_correcao'):
                    assert payload['op_ids_para_reparar'] == [iid + '_OP03']
                    assert [op['op_id'] for p in payload['anteriores'] for op in p['alteracoes']] == [iid + '_OP03']
                    # Os dois commits já estão no disco ANTES da chamada de reparo.
                    before = catalog(read_json(saved))[1]
                    assert before['B01_01']['texto'] == original['itens'][0]['alteracoes'][0]['texto']
                    assert before['B01_02']['texto'] == original['itens'][0]['alteracoes'][1]['texto']
                    assert catalog(payload['documento'])[1]['B01_02']['texto'] == before['B01_02']['texto']
                    result = dict(itens=[dict(id=iid, alteracoes=[original['itens'][0]['alteracoes'][2]], pendencias=[])])
                else:
                    result = copy.deepcopy(original)
            else:
                operations = [op for i in payload['intervencoes_e_operacoes_propostas'] for op in i['operacoes']]
                result = dict(avaliacoes_operacoes=[judgment(op['op_id'], iid,
                    'corrigir' if op['op_id'].endswith('03') else 'aprovar') for op in operations])
            validate(result)
            return result

    final = asyncio.run(edit_operations(base, base['documento'], [item], {}, Model(), tmp_path,
        'acabamento' if editorial else 'edicao', committed, decisions, errors, checkpoint,
        system=P.EDITORIAL if editorial else P.EDIT))
    assert {op['op_id'] for p in committed for op in p['alteracoes']} == {iid + '_OP01', iid + '_OP02'}
    assert catalog(final)[1]['B01_03'] == catalog(base['documento'])[1]['B01_03']
    assert read_json(saved) == final
    assert decisions[iid + '_OP03']['decisao'] == 'rejeitar'
    assert len([tag for tag, _ in inputs if tag.endswith('_correcao')]) == 1


def test_finishing_micro_batches_max_3_blocks():
    problems = [dict(blocos=['B04_05', 'B05_05'], tipo_defeito='repeticao_entre_capitulos', descricao='Mecanismo repetido')]
    problems += [dict(blocos=[f'B01_{i:02d}'], tipo_defeito='relato_de_leitura', descricao=f'Relato {i}') for i in range(1, 18)]
    batches = cluster_problems(problems)
    assert len(batches) > 1
    assert [b['id'] for b in batches] == [f'E{i:02d}' for i in range(1, len(batches) + 1)]
    assert all(len(set(b['alvos'])) <= 3 for b in batches)
    assert any({'B04_05', 'B05_05'}.issubset(b['alvos']) for b in batches)
    assert sum(len(b['problemas']) for b in batches) == 18


def test_runtime_retry_escalates_tokens_after_format_error_on_large_output(tmp_path):
    limits = []
    async def transport(role, messages, tokens):
        limits.append(tokens)
        return response({'id': 'INVALIDO', 'texto': 'x' * 36000}) if len(limits) == 1 else response({}, 'length')
    def validate(value):
        C.require(value.get('id') == 'I01', 'ID inválido')
    async def run():
        calls = Calls(tmp_path, configuration(), transport=transport, progress=lambda *a, **k: None)
        try:
            return await calls.call('write', 'pacote_grande', {}, validate, system=P.EDIT)
        finally:
            await calls.close()
    with pytest.raises(CallFailure) as captured:
        asyncio.run(run())
    assert limits == [16000, 32000]
    history = captured.value.attempt_history
    assert [r['failure_type'] for r in history] == ['contract_error', 'truncation']
    assert history[0]['raw_char_len'] > 35000
    assert 'T1: contract_error (ID inválido) com 16000 tokens' in str(captured.value)
    assert 'T2: truncation com 32000 tokens' in str(captured.value)
    logs = [json.loads(line) for line in (tmp_path / 'chamadas_llm.jsonl').read_text(encoding='utf-8').splitlines()]
    assert logs[-1]['attempt_history'] == history


@pytest.mark.parametrize('kind,size,expected', [
    ('format_error', 35000, 16000), ('format_error', 35001, 32000),
    ('contract_error', 35000, 16000), ('contract_error', 35001, 32000),
    ('truncation', 10, 32000),
])
def test_retry_token_threshold_and_failure_classification(tmp_path, kind, size, expected):
    limits = []
    async def transport(role, messages, tokens):
        limits.append(tokens)
        if len(limits) == 2:
            return response(dict(ok=True))
        raw = 'x' * size if kind == 'truncation' else '{' + 'x' * (size - 1) if kind == 'format_error' else json.dumps({'pad': ''})
        raw += ' ' * (size - len(raw))
        return response({}, 'length' if kind == 'truncation' else 'stop', raw)
    async def run():
        calls = Calls(tmp_path, configuration(), transport=transport, progress=lambda *a, **k: None)
        try:
            return await calls.call('write', 'limiar', {}, lambda d: C.require(d.get('ok'), 'Falta ok'), system=P.EDIT)
        finally:
            await calls.close()
    assert asyncio.run(run()) == {'ok': True}
    assert limits == [16000, expected]
    logs = [json.loads(line) for line in (tmp_path / 'chamadas_llm.jsonl').read_text(encoding='utf-8').splitlines()]
    assert logs[-1]['attempt_history'][0]['failure_type'] == kind
    assert logs[-1]['attempt_history'][0]['raw_char_len'] == size


def test_finishing_executes_micro_batches_with_local_repair_and_preserves_other_commits(tmp_path):
    base = base_data()
    base['documento']['capitulos'][0]['blocos'] += [dict(id=f'B01_{i:02d}', subtitulo='Condição',
        texto='A verificação depende das condições do processo.') for i in range(4, 18)]
    problems = [dict(blocos=['B04_02', 'B05_02'], tipo_defeito='repeticao_entre_capitulos', descricao='Par acoplado')]
    problems += [dict(blocos=[f'B01_{i:02d}'], tipo_defeito='relato_de_leitura', descricao=f'Clareza {i}') for i in range(1, 18)]
    plan = dict(intervencoes=[], cobertura=[dict(id='F01', estado='atendido', motivo='Coberto')])
    editorial, decisions, errors, inputs, state = [], {}, [], [], {}
    saved = tmp_path / 'commits.json'
    def checkpoint():
        atomic_json(saved, apply_changes(base['documento'], editorial))
    class Model:
        config = configuration()
        async def call(self, role, tag, payload, validate, *, system):
            inputs.append((system, tag, copy.deepcopy(payload)))
            if system == P.EDITORIAL_AUDIT:
                result = dict(problemas=problems if tag == 'leitura_editorial' else [problems[0]])
            elif system == P.EDITORIAL:
                assert len(catalog(payload['documento'])[1]) <= 3
                assert len(payload['intervencoes']) == 1
                iid = payload['intervencoes'][0]['id']
                if tag.endswith('_correcao'):
                    changes = copy.deepcopy(payload['anteriores'][0]['alteracoes'])
                    assert [op['op_id'] for op in changes] == ['E01_OP02']
                    # OP01 já foi preservada em disco antes do reparo de OP02.
                    assert any(p['id'] == 'E01' and any(op['op_id'] == 'E01_OP01' for op in p['alteracoes']) for p in editorial)
                else:
                    changes = [change(f'{iid}_OP{i:02d}', bid) for i, bid in enumerate(payload['intervencoes'][0]['alvos'], 1)]
                result = dict(itens=[dict(id=iid, alteracoes=changes, pendencias=[])])
            elif system == P.REVIEW:
                result = dict(avaliacoes_operacoes=[])
                for item in payload['intervencoes_e_operacoes_propostas']:
                    assert item['modo_validacao_suporte'] == 'MODO_PRESERVACAO_EDITORIAL_SEM_FATOS_NOVOS'
                    assert item['evidencias_fornecidas'] == []
                    for op in item['operacoes']:
                        assert op['estado_anterior_do_bloco'] is not None
                        result['avaliacoes_operacoes'].append(judgment(op['op_id'], item['intervencao_id'],
                            'corrigir' if op['op_id'] == 'E01_OP02' else 'aprovar'))
            else:
                assert system == P.CONSOLIDATE
                assert payload['cobertura_inicial_diagnostico'] == plan['cobertura']
                result = dict(protecoes_preservadas=True, problemas=[], cobertura=[dict(plan['cobertura'][0], evidencia_regressao='')], omissoes_escopo=[])
            validate(result)
            return result
    final = asyncio.run(finish(base, base['documento'], [], decisions, plan, Model(), tmp_path, editorial,
        state=state, checkpoint=checkpoint, errors=errors))
    writes = [payload for system, tag, payload in inputs if system == P.EDITORIAL and not tag.endswith('_correcao')]
    assert len(writes) > 1
    assert any({'B04_02', 'B05_02'}.issubset(payload['intervencoes'][0]['alvos']) for payload in writes)
    assert len(state['problemas_editoriais_detectados']) == 18
    assert final['problemas'][0]['descricao'] == 'Par acoplado'
    assert decisions['E01_OP02']['decisao'] == 'rejeitar'
    assert sum(len(p['alteracoes']) for p in editorial) == 18
    assert read_json(saved) == apply_changes(base['documento'], editorial)


def test_interrupted_flow_preserves_editorial_audit_in_summary(tmp_path):
    base = base_data()
    plan = dict(intervencoes=[intervention('I01', 'lacuna_essencial', ['B01_01'])],
        cobertura=[dict(id='F01', estado='parcial', motivo='Falta explicar o mecanismo')], omissoes_escopo=[])
    defects = [dict(blocos=['B02_01'], tipo_defeito='relato_de_leitura', descricao='Relato editorial detectado'),
               dict(blocos=['B04_01', 'B05_01'], tipo_defeito='repeticao_entre_capitulos', descricao='Repetição entre capítulos detectada')]
    async def transport(role, messages, tokens):
        payload = json.loads(messages[1]['content'])
        system = messages[0]['content']
        if system == P.DIAGNOSE:
            return response(plan)
        if system == P.EDIT:
            op = change('I01_OP01', 'B01_01')
            op['achados'] = ['I01_A01']
            return response(dict(itens=[dict(id='I01', alteracoes=[op], pendencias=[])]))
        if system == P.REVIEW:
            return response(dict(avaliacoes_operacoes=[judgment(op['op_id'], i['intervencao_id'])
                for i in payload['intervencoes_e_operacoes_propostas'] for op in i['operacoes']]))
        if system == P.EDITORIAL_AUDIT:
            return response(dict(problemas=defects))
        if system == P.EDITORIAL:
            # O resumo da leitura já precisa existir ao entrar no acabamento.
            assert len(read_json(tmp_path / 'resumo.json')['problemas_editoriais']) == 2
            raise asyncio.CancelledError()
        raise AssertionError('Chamada inesperada')
    async def research(*args):
        return dict(id='I01', status='com_achados', achados=[dict(id='I01_A01', proposicao='Mecanismo',
            citacoes=[], pertinencia='direta', sub_objetivos_atendidos=['S1'])], fontes=[], pendencias=[], erros=[])
    with patch('pipeline.qa_research.polimento.flow.inherited_index', return_value=None), \
         patch('pipeline.qa_research.polimento.flow.investigate', side_effect=research):
        with pytest.raises(asyncio.CancelledError):
            asyncio.run(polish(base, None, 'corpus_teste', configuration(), tmp_path, transport))
    summary = read_json(tmp_path / 'resumo.json')
    report = (tmp_path / 'relatorio.md').read_text(encoding='utf-8')
    assert summary['status'] == 'interrompido'
    assert summary['alteracoes_aprovadas'] == 1
    assert summary['intervencoes_tecnicas_aprovadas'][0]['alteracoes'][0]['op_id'] == 'I01_OP01'
    assert len(summary['problemas_editoriais']) == len(defects)
    for defect in defects:
        assert defect['descricao'] in report
        assert any(p['descricao'] == defect['descricao'] for p in summary['problemas_editoriais'])
    assert 'I01_OP01' in report
    candidate = read_json(tmp_path / 'documento_para_revisao.json')
    assert candidate['capitulos'][0]['blocos'][0]['texto'] == change('I01_OP01', 'B01_01')['texto']
    assert not (tmp_path / 'documento.json').exists()


@pytest.mark.parametrize('additional_queries', [True, False])
def test_sub_objectives_force_focused_second_round_and_partial_pending(additional_queries):
    item = intervention('I01', 'lacuna_essencial')
    item['sub_objetivos'].append(dict(id='S2', descricao='Limite de compatibilidade'))
    if not additional_queries:
        item['consultas'] = [dict(pt='bomba controle vazão pressão fluido material equipamento mecanismo atuação operação condições regime processo sistema ajuste resposta',
                                 en='pump flow pressure control')]
    payloads = []
    class Index:
        turn = 0
        def query(self, pairs, limit):
            self.turn += 1
            return [dict(chunk_id=str(self.turn), content_hash=str(self.turn), document_id=str(self.turn),
                texto='Mecanismo de atuação com condição explícita.', evidence_origin='nova')], []
    class Model:
        async def call(self, role, tag, payload, validate, **kwargs):
            payloads.append(payload)
            data = dict(suficiente=True, achados=[dict(proposicao='Mecanismo',
                citacoes=[payload['fontes'][0]['paragrafos'][0]['id']], tipo='explicacao_tecnica',
                pertinencia='direta', sub_objetivos_atendidos=['S1'], condicoes=[], limites=[])] if len(payloads) == 1 else [],
                consultas_adicionais=[dict(pt='limite compatibilidade material', en='material compatibility limit')] if additional_queries else [], pendencias=[])
            validate(data)
            return data
    result = asyncio.run(investigate(item, base_data(), Index(), configuration(), Model()))
    assert len(payloads) == 2
    assert [s['id'] for s in payloads[1]['intervencao']['sub_objetivos']] == ['S2']
    assert result['sub_objetivos_com_suporte'] == ['S1']
    assert result['sub_objetivos_sem_suporte'] == ['S2']
    assert not result['todos_sub_objetivos_cobertos']
    assert any('S2' in p for p in result['pendencias'])


def test_coverage_stability_preserves_attended_without_regression():
    initial = [dict(id='F01', estado='atendido', motivo='Mecanismo ensinado')]
    downgraded = [dict(id='F01', estado='parcial', motivo='Quero mais detalhe', evidencia_regressao='')]
    coverage, warnings = stabilize_coverage(downgraded, initial, [], [])
    assert coverage[0]['estado'] == 'atendido'
    assert warnings[0]['ponto'] == 'F01'
    real = [dict(downgraded[0], evidencia_regressao='Falta a condição de pressão exigida pelo escopo')]
    assert stabilize_coverage(real, initial, [], [])[0][0]['estado'] == 'parcial'


def test_operation_ids_are_unique_and_stable_after_partial_insertions():
    item = dict(id='I02', alteracoes=[change('', 'C05', 'inserir'), change('errado', 'C05', 'inserir')], pendencias=[])
    C.editing({'itens': [item]}, {'I02'})
    assert [op['op_id'] for op in item['alteracoes']] == ['I02_OP01', 'I02_OP02']
    partial = dict(item, alteracoes=item['alteracoes'][1:])
    assert 'N_I02_2' in catalog(apply_changes(document(), [partial]))[1]


def test_reviewer_must_return_each_operation_once():
    operations = {'I01_OP01': {'intervencao_id': 'I01'}}
    row = judgment('I01_OP01', 'I01')
    with pytest.raises(ValueError, match='exatamente'):
        C.judgment(dict(avaliacoes_operacoes=[row, row]), operations)
    with pytest.raises(ValueError, match='incorreta'):
        C.judgment(dict(avaliacoes_operacoes=[dict(row, intervencao_id='I02')]), operations)


def test_unsupported_sub_objective_is_automatically_pending_in_committed_edit(tmp_path):
    base = base_data()
    item = intervention('I01', 'aprofundamento', ['B01_01'])
    item['sub_objetivos'].append(dict(id='S2', descricao='Compatibilidade do material'))
    finding = dict(id='I01_A01', pertinencia='direta', sub_objetivos_atendidos=['S1'], citacoes=[])
    research = {'I01': dict(achados=[finding], fontes=[])}
    committed, decisions, errors = [], {}, []
    class Model:
        config = configuration()
        async def call(self, role, tag, payload, validate, **kwargs):
            if role == 'write':
                assert payload['intervencoes'][0]['sub_objetivos_com_suporte'] == ['S1']
                assert payload['intervencoes'][0]['sub_objetivos_sem_suporte'] == ['S2']
                op = change('I01_OP01', 'B01_01')
                op['achados'] = ['I01_A01']
                result = dict(itens=[dict(id='I01', alteracoes=[op], pendencias=[])])
            else:
                result = dict(avaliacoes_operacoes=[judgment('I01_OP01', 'I01')])
            validate(result)
            return result
    asyncio.run(edit_operations(base, base['documento'], [item], research, Model(), tmp_path, 'edicao',
        committed, decisions, errors, lambda: None))
    assert committed[0]['pendencias'] == ['Sem suporte direto para S2']


def test_rejected_fusion_does_not_commit_dependent_removal(tmp_path):
    base = base_data()
    item = intervention('E01', targets=['B01_01', 'B01_02', 'B01_03'])
    removal = change('E01_OP01', 'B01_01', 'remover')
    removal['preservacao'] = 'Todo o mecanismo será preservado em B01_02'
    proposal = dict(id='E01', alteracoes=[removal, change('E01_OP02', 'B01_02'), change('E01_OP03', 'B01_03')], pendencias=[])
    committed, decisions, errors = [], {}, []
    class Model:
        config = configuration()
        async def call(self, role, tag, payload, validate, **kwargs):
            if role == 'write':
                if tag.endswith('_correcao'):
                    assert payload['op_ids_para_reparar'] == ['E01_OP01']
                    assert {op['op_id'] for p in committed for op in p['alteracoes']} == {'E01_OP03'}
                    raise CallFailure('Reparo sem preservação disponível')
                result = dict(itens=[copy.deepcopy(proposal)])
            else:
                result = dict(avaliacoes_operacoes=[judgment(op['op_id'], 'E01',
                    'rejeitar' if op['op_id'] == 'E01_OP02' else 'aprovar') for op in proposal['alteracoes']])
            validate(result)
            return result
    final = asyncio.run(edit_operations(base, base['documento'], [item], {}, Model(), tmp_path, 'acabamento',
        committed, decisions, errors, lambda: None, system=P.EDITORIAL))
    assert catalog(final)[1]['B01_01'] == catalog(base['documento'])[1]['B01_01']
    assert {op['op_id'] for p in committed for op in p['alteracoes']} == {'E01_OP03'}
    assert decisions['E01_OP01']['decisao'] == 'rejeitar'
