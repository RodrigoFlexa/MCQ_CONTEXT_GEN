"""Regressões dos defeitos reais e das falhas parciais nas quatro etapas."""
import asyncio
import copy
import io
import json
import tempfile
import unittest
from contextlib import redirect_stdout
from pathlib import Path

from pipeline.inventario.textutil import read_json
from pipeline.qa_research.piloto_qa import contracts as C, prompts_fluxo as F
from pipeline.qa_research.piloto_qa.adaptive import generate
from pipeline.qa_research.piloto_qa.documents import flatten
from pipeline.qa_research.piloto_qa.fluxo import config
from pipeline.qa_research.piloto_qa.tests.test_pilot import response
from pipeline.qa_research.piloto_qa.validation import partition, resolve_evidence, source_with_passages


class Similarity:
    protocol = {'model': 'offline'}
    def nearest(self, text, bank, limit):
        return [dict(q, similaridade=0.5) for q in bank[:limit]]


class Model:
    def __init__(self, output):
        self.output = output
        self.inputs = []
        self.mode = 'valid'
        self.repair_ok = True
        self.cancel = False
        self.original = None
        self.after_commits = []

    def pair(self, qid, number):
        evidence = [dict(passagem='B001_P001')]
        target = dict(id=qid, tipo='mecanismo', composicao='simples', conhecimento=f'Relação operacional {number}',
            ponte='', afirmacoes=[dict(afirmacao='A restrição altera a vazão conforme as condições.', evidencias=evidence)])
        question = dict(id=qid, pergunta=f'Como a restrição altera a vazão na condição operacional {number}?',
            resposta='A restrição altera a vazão conforme as condições.', cenario=False,
            criterios=[dict(id='K1', criterio='Relacionar restrição e vazão', inferencia='', evidencias=evidence)],
            equivalentes=[], erros_materiais=[])
        return target, question

    def known_commits(self):
        path = self.output / 'aprovadas.jsonl'
        return [json.loads(s) for s in path.read_text(encoding='utf-8').splitlines()] if path.exists() else []

    async def __call__(self, role, messages, tokens):
        payload = json.loads(messages[1]['content'])
        self.inputs.append((role, copy.deepcopy(payload)))
        if role == 'author':
            if payload['rodada'] != 1:
                return response(dict(alvos=[], questoes=[], impedimentos=['Sem outra demanda suportada']))
            pairs = [self.pair(payload['prefixo'] + f'Q{i:02}', i) for i in range(1, 5)]
            data = dict(alvos=[t for t, q in pairs], questoes=[q for t, q in pairs], impedimentos=[])
            if self.mode in ('mixed', 'cancel', 'budget'):
                data['alvos'][1].update(composicao='composta', ponte='', afirmacoes=data['alvos'][1]['afirmacoes'] * 2)
                data['questoes'][2]['criterios'][0]['evidencias'] = [dict(bloco='B001', trecho='Citação inventada')]
            elif self.mode == 'duplicate':
                data['questoes'][1]['id'] = data['questoes'][0]['id']
            self.original = copy.deepcopy(data)
            return response(data)
        if role == 'refine' and 'ids_para_reparar' in payload:
            self.after_commits.append([q['id'] for q in self.known_commits()])
            if self.cancel: raise asyncio.CancelledError()
            pairs = [self.pair(qid, int(qid[-2:])) for qid in payload['ids_para_reparar']]
            data = dict(alvos=[t for t, q in pairs], questoes=[q for t, q in pairs], impedimentos=[])
            if not self.repair_ok:
                for q in data['questoes']:
                    q['criterios'][0]['evidencias'] = [dict(passagem='INVENTADA')]
            return response(data)
        if role == 'refine':
            self.after_commits.append([q['id'] for q in self.known_commits()])
            return response(dict(questoes=[self.pair(t['id'], int(t['id'][-2:]))[1] for t in payload['alvos']], impedimentos=[]))
        if role == 'solve':
            values = [dict(id=q['id'], resposta='A restrição altera a vazão.', ambiguidades=[]) for q in payload['questoes']]
            if self.mode == 'solver' and 'reparar_ids' not in payload:
                values[-1]['resposta'] = ''
            if 'reparar_ids' in payload:
                self.after_commits.append([q['id'] for q in self.known_commits()])
                if self.cancel: raise asyncio.CancelledError()
            return response(dict(resolucoes=values))
        values = []
        for question in payload['candidatas']:
            semantic_repair = self.mode == 'semantic' and question['id'].endswith('Q01') and not any(
                r == 'refine' and 'ids_para_reparar' not in p for r, p in self.inputs)
            flags = dict.fromkeys(C.FLAGS, True)
            if semantic_repair: flags['determinada'] = False
            row = dict(id=question['id'], decisao='corrigir' if semantic_repair else 'admitir', motivo='Conferido',
                correcao='Delimitar condição' if semantic_repair else '', duplicada_de=None, criterios=flags,
                checagem_essenciais=[dict(id=c['id'], sustentado=True, evidencias=[dict(passagem='B001_P001')],
                                          justificativa='Relação literal no contexto') for c in question['criterios']])
            if self.mode == 'judge' and question['id'].endswith('Q04') and 'reparar_ids' not in payload:
                row['criterios']['suporte'] = 'true'
            values.append(row)
        if 'reparar_ids' in payload:
            self.after_commits.append([q['id'] for q in self.known_commits()])
            if self.cancel: raise asyncio.CancelledError()
        return response(dict(avaliacoes=values))


class IsolationTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory(); self.addCleanup(self.tmp.cleanup)
        self.output = Path(self.tmp.name) / 'run'
        self.document = dict(titulo='Controle', capitulos=[dict(titulo='Processo', grupo='Processo', blocos=[
            dict(subtitulo='Restrição', texto='A restrição altera a vazão conforme as condições.\n\nA pressão também depende do processo.')])])
        self.config = config(); self.config.update(max_calls=60, patience=1)
        self.model = Model(self.output)

    def run_flow(self):
        with redirect_stdout(io.StringIO()):
            return asyncio.run(generate(self.document, '02_02', 'novo_refinado', self.config,
                self.output, [], Similarity(), transport=self.model))

    def test_mixed_real_contract_failures_preserve_valid_siblings_and_repair_only_bad_ids(self):
        self.model.mode = 'mixed'
        result = self.run_flow()
        self.assertEqual(result['admitidas'], 4, result)
        repair = next(p for r, p in self.model.inputs if r == 'refine')
        self.assertEqual(repair['ids_para_reparar'], ['02_02_000001_Q02', '02_02_000001_Q03'])
        self.assertEqual(repair['alvos_congelados'], ['02_02_000001_Q03'])
        self.assertEqual(len(self.model.after_commits[0]), 2)
        author = [p for r, p in self.model.inputs if r == 'author' and p['rodada'] == 1]
        self.assertEqual(len(author), 1, 'Contrato ruim não provoca regeneração do lote')
        initial = read_json(self.output / 'rodadas/000001_inicial.json')
        bad = [r for r in initial['records'] if r.get('reparo_autoria')]
        self.assertTrue(any('Composta exige ponte' in e['erro'] for r in bad for e in r['erros_validacao']))
        self.assertTrue(any('criterios[K1].evidencias[0]' in e['erro'] for r in bad for e in r['erros_validacao']))

    def test_failed_individual_repair_never_discards_good_siblings_or_blocks_next_round(self):
        self.model.mode = 'mixed'; self.model.repair_ok = False
        result = self.run_flow()
        self.assertEqual(result['admitidas'], 2, result)
        self.assertEqual(result['invalidas_contrato'], 2)
        self.assertEqual(result['status'], 'concluido')
        self.assertTrue(any(r == 'author' and p['rodada'] == 2 for r, p in self.model.inputs))

    def test_solver_invalid_sibling_is_repaired_after_other_questions_are_committed(self):
        self.model.mode = 'solver'
        result = self.run_flow()
        self.assertEqual(result['admitidas'], 4, result)
        repair = [p for r, p in self.model.inputs if r == 'solve' and 'reparar_ids' in p]
        self.assertEqual([q['id'] for q in repair[0]['questoes']], ['02_02_000001_Q04'])
        self.assertEqual(len(self.model.after_commits[0]), 3)

    def test_judge_invalid_boolean_only_reasks_the_affected_verdict(self):
        self.model.mode = 'judge'
        result = self.run_flow()
        self.assertEqual(result['admitidas'], 4, result)
        repair = [p for r, p in self.model.inputs if r == 'judge' and 'reparar_ids' in p]
        self.assertEqual([q['id'] for q in repair[0]['candidatas']], ['02_02_000001_Q04'])
        self.assertEqual(len(self.model.after_commits[0]), 3)

    def test_semantic_refinement_is_individual_and_other_approvals_precede_it(self):
        self.model.mode = 'semantic'
        result = self.run_flow()
        self.assertEqual(result['admitidas'], 4, result)
        repair = [p for r, p in self.model.inputs if r == 'refine']
        self.assertEqual([t['id'] for t in repair[0]['alvos']], ['02_02_000001_Q01'])
        self.assertEqual(len(self.model.after_commits[0]), 3)

    def test_budget_in_bad_candidate_repair_preserves_commits_and_resumes_without_regenerating_them(self):
        self.model.mode = 'budget'; self.config['max_calls'] = 3
        result = self.run_flow()
        self.assertEqual(result['admitidas'], 2)
        self.assertEqual(result['motivo_parada'], 'suspenso_orcamento')
        self.config['max_calls'] = 60
        result = self.run_flow()
        self.assertEqual(result['admitidas'], 4, result)
        self.assertEqual(sum(r == 'author' and p['rodada'] == 1 for r, p in self.model.inputs), 1)
        self.assertEqual(sum(r == 'solve' and len(p['questoes']) == 2 for r, p in self.model.inputs), 2)

    def test_cancellation_in_contract_repair_keeps_public_and_round_checkpoints(self):
        self.model.mode = 'cancel'; self.model.cancel = True
        with self.assertRaises(asyncio.CancelledError): self.run_flow()
        summary = read_json(self.output / 'resumo.json')
        self.assertEqual(summary['admitidas'], 2)
        self.assertEqual(summary['motivo_parada'], 'interrompido')
        self.assertEqual(len(self.model.known_commits()), 2)
        self.model.cancel = False
        self.assertEqual(self.run_flow()['admitidas'], 4)

    def test_duplicate_question_id_does_not_invalidate_unambiguous_siblings(self):
        self.model.mode = 'duplicate'
        result = self.run_flow()
        self.assertEqual(result['admitidas'], 4, result)
        self.assertEqual(len(self.model.after_commits[0]), 2)

    def test_unknown_passage_is_rejected_without_fuzzy_matching_or_fact_invention(self):
        blocks = {b['id']: b for b in flatten(self.document)}
        with self.assertRaisesRegex(ValueError, 'passagem desconhecida'):
            resolve_evidence(dict(id='Q1', evidencias=[dict(passagem='INVENTADA')]), blocks)
        with self.assertRaisesRegex(ValueError, 'contradiz passagem'):
            resolve_evidence(dict(id='Q1', evidencias=[dict(passagem='B001_P001', trecho='Outra afirmação')]), blocks)

    def test_passage_ids_expand_to_exact_original_slices(self):
        blocks = flatten(self.document)
        passages = source_with_passages(blocks)[0]['passagens']
        self.assertEqual(len(passages), 2)
        for p in passages:
            self.assertEqual(p['texto'], blocks[0]['texto'][p['inicio']:p['fim']])
            expanded = resolve_evidence(dict(id='Q1', evidencias=[dict(passagem=p['id'])]), {'B001': blocks[0]})
            C.evidence(expanded['evidencias'], {'B001': blocks[0]})

    def test_passage_offsets_preserve_crlf_and_trailing_whitespace(self):
        text = '  Primeira condição.  \r\n\r\n  Segunda condição.   \r\n'
        block = dict(id='B1', texto=text)
        passages = source_with_passages([block])[0]['passagens']
        self.assertEqual([p['texto'] for p in passages], ['Primeira condição.', 'Segunda condição.'])
        self.assertTrue(all(text[p['inicio']:p['fim']] == p['texto'] for p in passages))

    def test_nonobject_and_missing_id_rows_are_logged_individually(self):
        blocks = {b['id']: b for b in flatten(self.document)}
        t, q = self.model.pair('Q1', 1)
        records, errors, _ = partition(dict(alvos=[t], questoes=[q, None, {'pergunta': 'Sem ID'}], impedimentos={}), blocks)
        self.assertEqual(records[0]['decisao'], 'pendente_resolucao')
        self.assertEqual(sum(r['decisao'] == 'invalida_contrato' for r in records), 2)
        self.assertTrue(any(e['campo'] == 'impedimentos' for e in errors))

    def test_full_retry_history_and_individual_errors_are_both_available(self):
        self.model.mode = 'mixed'; self.model.repair_ok = False
        self.run_flow()
        logs = [json.loads(s) for s in (self.output / 'chamadas_llm.jsonl').read_text(encoding='utf-8').splitlines()]
        self.assertTrue(all(row['ok'] for row in logs), 'Transporte recebeu JSON válido, apesar dos contratos individuais inválidos')
        decisions = read_json(self.output / 'decisoes.json')
        self.assertEqual(sum(r['decisao'] == 'invalida_contrato' for r in decisions), 2)
        self.assertTrue(all(r.get('erros_validacao') for r in decisions if r['decisao'] == 'invalida_contrato'))

    def test_continuous_prompt_contains_complete_composition_rules(self):
        self.assertIn('ponte NUNCA fica vazia', F.GENERATE)
        self.assertIn('DUAS', F.GENERATE)
        self.assertNotIn('alvo recebido', F.GENERATE)

    def test_permanent_judge_contract_error_rejects_only_one_question(self):
        class BrokenJudge(Model):
            async def __call__(self, role, messages, tokens):
                p = json.loads(messages[1]['content'])
                if role == 'judge' and 'reparar_ids' in p:
                    self.inputs.append((role, p))
                    return response(dict(avaliacoes=[]))
                return await super().__call__(role, messages, tokens)
        self.model = BrokenJudge(self.output); self.model.mode = 'judge'
        result = self.run_flow()
        self.assertEqual(result['admitidas'], 3, result)
        self.assertEqual(result['invalidas_contrato'], 1)
        self.assertEqual(len([p for r, p in self.model.inputs if r == 'judge' and 'reparar_ids' in p]), 1)

    def test_invalid_refinement_cannot_reject_other_approved_questions(self):
        class BrokenRefinement(Model):
            async def __call__(self, role, messages, tokens):
                result = await super().__call__(role, messages, tokens)
                if role == 'refine' and 'ids_para_reparar' not in json.loads(messages[1]['content']):
                    data = json.loads(result.choices[0].message.content)
                    for question in data['questoes']: question['criterios'] = []
                    return response(data)
                return result
        self.model = BrokenRefinement(self.output); self.model.mode = 'semantic'; self.model.repair_ok = False
        result = self.run_flow()
        self.assertEqual(result['admitidas'], 3, result)
        self.assertEqual(result['invalidas_contrato'], 1)

    def test_cancellation_in_solver_repair_keeps_other_judgments_and_resumes_locally(self):
        self.model.mode = 'solver'; self.model.cancel = True
        with self.assertRaises(asyncio.CancelledError): self.run_flow()
        self.assertEqual(len(self.model.known_commits()), 3)
        self.model.cancel = False
        result = self.run_flow()
        self.assertEqual(result['admitidas'], 4, result)
        full_solves = [p for r, p in self.model.inputs if r == 'solve' and len(p['questoes']) == 4]
        self.assertEqual(len(full_solves), 1)

    def test_contract_repair_cannot_change_an_already_valid_target(self):
        class ChangedTarget(Model):
            async def __call__(self, role, messages, tokens):
                result = await super().__call__(role, messages, tokens)
                if role == 'refine':
                    data = json.loads(result.choices[0].message.content)
                    for target in data.get('alvos', []):
                        if target['id'].endswith('Q03'): target['conhecimento'] = 'Outro objetivo'
                    return response(data)
                return result
        self.model = ChangedTarget(self.output); self.model.mode = 'mixed'
        result = self.run_flow()
        self.assertEqual(result['admitidas'], 3, result)
        self.assertEqual(result['invalidas_contrato'], 1)
        self.assertTrue(any('Alvo válido não pode ser alterado' in e['erro'] for r in read_json(self.output/'decisoes.json')
                            for e in r.get('erros_validacao', [])))

    def test_all_invalid_rounds_have_a_finite_limit_without_claiming_saturation(self):
        class AllInvalid(Model):
            async def __call__(self, role, messages, tokens):
                p = json.loads(messages[1]['content']); self.inputs.append((role, p))
                if role == 'author':
                    t, q = self.pair(p['prefixo']+'Q01', 1)
                    t.update(composicao='composta', ponte='')
                    return response(dict(alvos=[t], questoes=[q], impedimentos=[]))
                return response(dict(alvos=[], questoes=[], impedimentos=['Sem reparo suportado']))
        self.model = AllInvalid(self.output)
        result = self.run_flow()
        self.assertEqual(result['motivo_parada'], 'contextos_com_falhas', result)
        self.assertEqual(result['status'], 'parcial')
        self.assertEqual(result['contextos'][0]['rodadas_sem_ganho'], 0)
        self.assertEqual(result['contextos'][0]['falhas_contrato'], 3)
        self.assertEqual(len([p for r, p in self.model.inputs if r == 'author']), 3)

    def test_a_failed_context_does_not_block_healthy_contexts(self):
        class MixedContexts(Model):
            healthy_seen = False
            async def __call__(self, role, messages, tokens):
                p = json.loads(messages[1]['content'])
                if role == 'author':
                    self.inputs.append((role, p))
                    bad = p['contexto']['nome'] == 'Processo'
                    if not bad and self.healthy_seen:
                        return response(dict(alvos=[], questoes=[], impedimentos=['Sem outra demanda']))
                    t, q = self.pair(p['prefixo']+'Q01', 1)
                    if bad: t.update(composicao='composta', ponte='')
                    else: self.healthy_seen = True
                    for element in t['afirmacoes'] + q['criterios']:
                        element['evidencias'] = [dict(passagem=p['contexto']['blocos'][0]['passagens'][0]['id'])]
                    return response(dict(alvos=[t], questoes=[q], impedimentos=[]))
                if role == 'refine':
                    self.inputs.append((role, p))
                    return response(dict(alvos=[], questoes=[], impedimentos=['Não reparado']))
                result = await super().__call__(role, messages, tokens)
                if role == 'judge':
                    data = json.loads(result.choices[0].message.content)
                    for row in data['avaliacoes']:
                        row['checagem_essenciais'][0]['evidencias'] = [dict(passagem='B002_P001')]
                    return response(data)
                return result
        self.document['capitulos'].append(dict(titulo='Outro sistema', grupo='Outro', blocos=[
            dict(subtitulo='Controle', texto='A restrição altera a vazão conforme as condições.')]))
        self.model = MixedContexts(self.output)
        result = self.run_flow()
        self.assertEqual(result['admitidas'], 1, result)
        self.assertEqual(result['motivo_parada'], 'contextos_com_falhas')
        self.assertEqual(result['contextos'][1]['rodadas_sem_ganho'], 1)

    def test_large_verdict_payload_splits_without_discarding_candidates(self):
        self.document['capitulos'][0]['blocos'][0]['texto'] = 'A restrição altera a vazão conforme as condições. ' * 80
        self.config['max_input_chars'] = 28000
        result = self.run_flow()
        self.assertEqual(result['admitidas'], 4, result)
        self.assertGreater(len([p for r, p in self.model.inputs if r == 'judge']), 1)

    def test_wrong_prefix_only_discards_its_own_candidate(self):
        blocks = {b['id']: b for b in flatten(self.document)}
        good = self.model.pair('P_Q01', 1); bad = self.model.pair('OTHER_Q02', 2)
        records, _, _ = partition(dict(alvos=[good[0], bad[0]], questoes=[good[1], bad[1]], impedimentos=[]), blocks, prefix='P_')
        self.assertEqual([r['decisao'] for r in records], ['pendente_resolucao', 'invalida_contrato'])

    def test_excess_candidates_do_not_invalidate_requested_candidates(self):
        blocks = {b['id']: b for b in flatten(self.document)}
        pairs = [self.model.pair(f'Q{i}', i) for i in range(5)]
        records, _, _ = partition(dict(alvos=[t for t,q in pairs], questoes=[q for t,q in pairs], impedimentos=[]), blocks, limit=4)
        self.assertEqual(sum(r['decisao']=='pendente_resolucao' for r in records), 4)
        self.assertEqual(records[-1]['decisao'], 'invalida_contrato')

    def test_one_candidate_reports_both_bad_bridge_and_bad_literal_before_repair(self):
        blocks = {b['id']: b for b in flatten(self.document)}
        t, q = self.model.pair('Q1', 1)
        t.update(composicao='composta', ponte='', afirmacoes=t['afirmacoes'] * 2)
        q['criterios'][0]['evidencias'] = [dict(bloco='B001', trecho='Inexistente')]
        records, _, _ = partition(dict(alvos=[t], questoes=[q], impedimentos=[]), blocks)
        error = records[0]['erros_validacao'][0]['erro']
        self.assertIn('Composta exige ponte', error)
        self.assertIn('Trecho precisa ser literal', error)

    def test_same_target_with_legacy_evidence_is_preserved_during_repair(self):
        class LegacyEvidence(Model):
            async def __call__(self, role, messages, tokens):
                result = await super().__call__(role, messages, tokens)
                if role == 'refine':
                    data = json.loads(result.choices[0].message.content)
                    for target in data.get('alvos', []):
                        for a in target['afirmacoes']:
                            a['evidencias'] = [dict(bloco='B001', trecho='A restrição altera a vazão conforme as condições.')]
                    return response(data)
                return result
        self.model = LegacyEvidence(self.output); self.model.mode = 'mixed'
        result = self.run_flow()
        self.assertEqual(result['admitidas'], 4, result)

    def test_repeating_one_assertion_does_not_create_a_composed_question(self):
        blocks = {b['id']: b for b in flatten(self.document)}
        t, q = self.model.pair('Q1', 1)
        t.update(composicao='composta', ponte='A segunda relação combina com a primeira.', afirmacoes=t['afirmacoes'] * 2)
        records, _, _ = partition(dict(alvos=[t], questoes=[q], impedimentos=[]), blocks)
        self.assertEqual(records[0]['decisao'], 'corrigir_contrato')
        self.assertIn('relações distintas', records[0]['erros_validacao'][0]['erro'])
