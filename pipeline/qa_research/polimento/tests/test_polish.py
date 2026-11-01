"""Testes offline de edição, fundamentação, preservação, retomada e lote de três."""
import asyncio
import copy
import io
import json
import subprocess
import tempfile
import unittest
from contextlib import redirect_stdout
from pathlib import Path
from types import SimpleNamespace as NS

from pipeline.domain_corpora.io_utils import file_hash
from pipeline.inventario.textutil import atomic_json, read_json
from pipeline.qa_research.polimento import contracts as C
from pipeline.qa_research.polimento.__main__ import configuration, execute, collect, main, DEFAULT_BASE, DEFAULT_LEGACY, DEFAULT_EXPERT, all_items
from pipeline.qa_research.polimento.documents import load_base, catalog, apply_changes, validate_changes, clean
from pipeline.qa_research.polimento.research import inherited_index, source, investigate
from pipeline.qa_research.polimento.editorial import audit, block_issues
from pipeline.qa_research.v3.runtime import CallFailure


def response(value):
    return NS(choices=[NS(finish_reason='stop', message=NS(content=json.dumps(value, ensure_ascii=False)))],
              usage=NS(prompt_tokens=100, completion_tokens=50))


class Model:
    def __init__(self):
        self.inputs = []
        self.bad_target = False
        self.reject = False
        self.critical = False
        self.protected = True
        self.partial = False
        self.research_bad = False
        self.cancel = False
        self.contextual = False
        self.reject_editorial = False
        self.missing_queries_once = False
        self.semantic_repeat = False

    async def __call__(self, role, messages, tokens):
        p = json.loads(messages[1]['content'])
        self.inputs.append((role, p))
        if role == 'plan':
            if self.cancel:
                raise asyncio.CancelledError()
            d = dict(intervencoes=[dict(id='I01', tipo='lacuna_essencial', prioridade='alta', alvos=['B01_01'],
                pontos=['F1'], objetivo='Explicar a resposta ao ajuste', motivo='Há relação pouco desenvolvida',
                sub_objetivos=[dict(id='S1', descricao='Explicar a resposta ao ajuste')], consultas=[dict(pt='bomba vazão controle', en='pump flow control')]),
                dict(id='I02', tipo='editorial', prioridade='media', alvos=['B01_02'], pontos=['F1'],
                     objetivo='Clarear a instrução', motivo='Redação pode melhorar', sub_objetivos=[], consultas=[])],
                cobertura=[dict(id='F1', estado='parcial', motivo='Falta aprofundar')], omissoes_escopo=[])
            if self.missing_queries_once:
                d['intervencoes'][0]['consultas'] = []
                self.missing_queries_once = False
        elif role == 'write' and 'intervencao' in p:
            pid = p['fontes'][0]['paragrafos'][0]['id']
            d = dict(suficiente=True, achados=[dict(proposicao='A vazão precisa ser observada após ajustar a bomba.',
                citacoes=['INVENTADA' if self.research_bad else pid], tipo='explicacao_tecnica', condicoes=['Bomba em operação'],
                limites=['Princípio qualitativo'], pertinencia='contextual' if self.contextual else 'direta',
                sub_objetivos_atendidos=[] if self.contextual else ['S1'])], consultas_adicionais=[], pendencias=[])
        elif role == 'write':
            blocks = catalog(p['documento'])[1]
            items = []
            for intervention in p['intervencoes']:
                iid, target = intervention['id'], intervention['alvos'][0]
                before = blocks[target]
                body = before['texto'] + (' A equipe observa a resposta da vazão ao ajuste.' if iid == 'I01' else ' A conferência precede a mudança.')
                if iid == 'E01':
                    body = before['texto'].replace('No caso relatado, ', '').replace('Explicação repetida sem informação exclusiva.', '')
                if self.bad_target and iid == 'I02' and 'pareceres' not in p:
                    target = 'B02_01'
                items.append(dict(id=iid, alteracoes=[dict(operacao='substituir', alvo=target,
                    subtitulo=before['subtitulo'], texto=body, motivo=intervention['objetivo'],
                    preservacao='Mantém as condições e o mecanismo anteriores.',
                    achados=[a['id'] for a in p['achados'][iid]], complementos=[])], pendencias=[]))
            d = dict(itens=items)
        elif 'intervencoes_e_operacoes_propostas' in p:
            d = dict(avaliacoes_operacoes=[])
            for intervention in p['intervencoes_e_operacoes_propostas']:
                iid = intervention['intervencao_id']
                bad = (self.reject and iid == 'I01') or (self.reject_editorial and iid.startswith('E'))
                flags = {k: True for k in C.FLAGS}
                if bad:
                    flags['sem_perda'] = False
                for op in intervention['operacoes']:
                    d['avaliacoes_operacoes'].append(dict(op_id=op['op_id'], intervencao_id=iid,
                        decisao='rejeitar' if bad else 'aprovar', motivo='Perda de condição' if bad else 'Alteração verificada',
                        correcao='', criterios=flags))
        elif 'sinais_editoriais' in p and 'pontos' not in p:
            text = ' '.join(b['texto'] for b in catalog(p['documento'])[1].values())
            d = dict(problemas=[dict(blocos=['B02_01'], descricao='Repetição semântica com o capítulo anterior', tipo_defeito='repeticao_entre_capitulos')]
                     if self.semantic_repeat and 'Explicação repetida sem informação exclusiva.' in text else [])
        else:
            d = dict(protecoes_preservadas=self.protected, problemas=[dict(blocos=['B01_01'], descricao='Condição não preservada', critico=True, tipo='tecnico')] if self.critical else [],
                cobertura=[dict(id='F1', estado='parcial' if self.partial else 'atendido', motivo='Avaliação consolidada', evidencia_regressao='')], omissoes_escopo=[])
        return response(d)


class FlowTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.root = Path(self.tmp.name)
        self.base, self.legacy = self.root / 'base', self.root / 'legacy'
        self.expert = self.root / 'expert.json'
        atomic_json(self.expert, dict(documentos={}))
        for item in ('02_02', '03_03', '07_01'):
            doc = dict(titulo='Contexto simulado', capitulos=[dict(titulo='Condições operacionais', grupo='Operação', blocos=[
                dict(subtitulo='Mecanismo', texto='O mecanismo depende das condições do processo. Confirmar o estado antes da aplicação.'),
                dict(subtitulo='Conferência', texto='A equipe verifica a vazão antes da mudança.')]),
                dict(titulo='Preservação', grupo='Integridade', blocos=[dict(subtitulo='Condição importante', texto='Este conteúdo permanece integralmente inalterado.')])])
            atomic_json(self.base / item / 'documento.json', doc)
            atomic_json(self.base / item / 'resumo.json', dict(recortes_pendentes=['F1']))
            atomic_json(self.legacy / item / 'pacote/facets.json', [dict(id='F1', titulo='Mecanismo', foco='Mecanismo e condições')])
            path = self.legacy / item / 'evidencias_citadas.jsonl'
            path.write_text(json.dumps(dict(id='E_OLD', collection='manual_antigo', document_id='old1', title='Manual anterior',
                texto=('A bomba acompanha a vazão no controle do processo. ' * 30) + ' FONTE_PRIVADA_NAO_EXPORTAR', language='pt',
                source_boundary='known_document', source_sha256='original', page_ini=3, chunk_id='oldchunk')) + '\n', encoding='utf-8')
        corpus = self.root / 'corpus'
        corpus.mkdir()
        pages = corpus / 'pages.jsonl'
        pages.write_text(json.dumps(dict(collection='manual', document_id='new1', title='Manual profissional',
            text=('The pump flow control depends on operating conditions. ' * 30) + ' FONTE_PRIVADA_NAO_EXPORTAR',
            page=1, source_boundary='known_document', language='en')) + '\n', encoding='utf-8')
        self.manifest = corpus / 'manifest.json'
        atomic_json(self.manifest, dict(schema='petroquest-professional-corpora-v1', ready=True, partial=True,
            collections=[dict(id='manual', format='pages_jsonl', path=pages.name, sha256=file_hash(pages), documents=1)]))
        self.config = configuration()
        self.output = self.root / 'run'
        self.model = Model()

    def run_flow(self, items=('02_02',)):
        with redirect_stdout(io.StringIO()):
            return asyncio.run(execute(self.base, self.legacy, self.expert, self.manifest,
                self.output, list(items), self.config, transport=self.model))

    def test_three_document_pilot_resume_and_unchanged_content(self):
        before = {p: p.read_bytes() for p in self.base.rglob('*') if p.is_file()}
        result = self.run_flow(('02_02', '03_03', '07_01'))
        self.assertEqual(result['status'], 'concluido', result)
        self.assertEqual(len(result['documentos']), 3)
        for item, row in result['documentos'].items():
            self.assertEqual(row['intervencoes_aprovadas'], 2)
            doc = read_json(self.output / item / 'documento.json')
            self.assertEqual(doc['capitulos'][1]['blocos'][0]['texto'], 'Este conteúdo permanece integralmente inalterado.')
            self.assertNotIn('id', doc['capitulos'][0]['blocos'][0])
        self.assertTrue(all(p.read_bytes() == data for p, data in before.items()))
        inputs = copy.deepcopy(self.model.inputs)
        self.config.update(workers=1, max_calls=80)
        resumed = self.run_flow(('02_02', '03_03', '07_01'))
        self.assertEqual(resumed['status'], 'concluido', resumed)
        self.assertEqual(self.model.inputs, inputs, 'Retomada não repete chamadas concluídas')

    def test_invalid_patch_is_repaired_without_losing_independent_approval(self):
        self.model.bad_target = True
        result = self.run_flow()
        self.assertEqual(result['status'], 'concluido', result)
        edits = [p for role, p in self.model.inputs if role == 'write' and 'intervencoes' in p]
        self.assertEqual(len(edits), 2)
        self.assertEqual([i['id'] for i in edits[-1]['intervencoes']], ['I02'])
        self.assertEqual(result['documentos']['02_02']['intervencoes_aprovadas'], 2)

    def test_rejected_depth_loss_is_not_applied_and_essential_gap_blocks_qa(self):
        self.model.reject = True
        result = self.run_flow()
        row = result['documentos']['02_02']
        self.assertFalse(row['qa_elegivel'])
        self.assertTrue(row['documento_publicado'])
        original = read_json(self.base / '02_02/documento.json')
        edited = read_json(self.output / '02_02/documento.json')
        self.assertEqual(original['capitulos'][0]['blocos'][0], edited['capitulos'][0]['blocos'][0])

    def test_critical_final_problem_quarantines_candidate(self):
        self.model.critical = True
        row = self.run_flow()['documentos']['02_02']
        self.assertEqual(row['status'], 'revisao_requerida')
        self.assertFalse((self.output / '02_02/documento.json').exists())
        self.assertTrue((self.output / '02_02/documento_para_revisao.json').exists())

    def test_specialist_reversal_cannot_publish_even_without_other_flags(self):
        self.model.protected = False
        row = self.run_flow()['documentos']['02_02']
        self.assertFalse(row['documento_publicado'])
        self.assertFalse(row['qa_elegivel'])

    def test_partial_coverage_does_not_discard_sound_edits(self):
        self.model.partial = True
        row = self.run_flow()['documentos']['02_02']
        self.assertEqual(row['status'], 'parcial')
        self.assertEqual(row['intervencoes_aprovadas'], 2)
        self.assertTrue(row['documento_publicado'])
        self.assertFalse(row['qa_elegivel'])
        self.assertTrue(any(p['origem'] == 'cobertura' and p['pontos'] == ['F1'] for p in row['pendencias']))

    def test_technical_gap_requires_queries_and_retry_performs_research(self):
        self.model.missing_queries_once = True
        row = self.run_flow()['documentos']['02_02']
        self.assertTrue(row['qa_elegivel'], row)
        self.assertEqual(sum(role == 'plan' for role, _ in self.model.inputs), 2)
        self.assertTrue(any('intervencao' in p for role, p in self.model.inputs if role == 'write'))

    def test_contextual_findings_cannot_authorize_technical_inclusion(self):
        self.model.contextual = True
        row = self.run_flow()['documentos']['02_02']
        self.assertFalse(row['qa_elegivel'])
        self.assertEqual(row['intervencoes_aprovadas'], 1)
        research = read_json(next((self.output / '02_02/versoes').glob('*/pesquisas.json')))
        self.assertEqual(research['I01']['status'], 'sem_evidencia_pertinente')
        self.assertEqual(research['I01']['achados'], [])

    def add_inherited_editorial_problem(self, text):
        path = self.base / '02_02/documento.json'
        document = read_json(path)
        document['capitulos'][1]['blocos'][0]['texto'] = text
        atomic_json(path, document)

    def test_local_check_finds_reading_report_even_when_model_misses_it(self):
        self.add_inherited_editorial_problem('No caso relatado, a equipe verifica a vazão.')
        row = self.run_flow()['documentos']['02_02']
        self.assertTrue(row['qa_elegivel'], row)
        self.assertEqual(row['acabamento_alteracoes'], 1)
        doc = read_json(self.output / '02_02/documento.json')
        self.assertNotIn('No caso relatado', json.dumps(doc))
        self.assertTrue(any(i['modo_validacao_suporte'] == 'MODO_PRESERVACAO_EDITORIAL_SEM_FATOS_NOVOS'
            for role, p in self.model.inputs if role == 'review'
            for i in p.get('intervencoes_e_operacoes_propostas', []) if i['intervencao_id'].startswith('E')))
        inputs = copy.deepcopy(self.model.inputs)
        self.assertTrue(self.run_flow()['documentos']['02_02']['qa_elegivel'])
        self.assertEqual(inputs, self.model.inputs, 'Retomada também reutiliza acabamento e conferência')

    def test_later_edit_batch_receives_previous_approved_inclusion(self):
        self.config['batch_size'] = 1
        row = self.run_flow()['documentos']['02_02']
        self.assertTrue(row['qa_elegivel'])
        edits = [p for role, p in self.model.inputs if role == 'write' and 'intervencoes' in p]
        self.assertIn('A equipe observa a resposta da vazão ao ajuste.', catalog(edits[1]['documento'])[1]['B01_01']['texto'])

    def test_rejected_editorial_repair_is_not_published_despite_positive_final(self):
        self.add_inherited_editorial_problem('No caso relatado, a equipe verifica a vazão.')
        self.model.reject_editorial = True
        row = self.run_flow()['documentos']['02_02']
        self.assertFalse(row['qa_elegivel'])
        self.assertFalse(row['documento_publicado'])
        self.assertTrue(row['problemas_editoriais'])
        self.assertEqual(row['acabamento_alteracoes'], 0)

    def test_interrupted_editorial_conference_preserves_patch_and_resumes(self):
        self.add_inherited_editorial_problem('No caso relatado, a equipe verifica a vazão.')
        self.config['max_calls'] = 7
        row = self.run_flow()['documentos']['02_02']
        self.assertEqual(row['status'], 'interrompido', row)
        self.assertEqual(row['acabamento_alteracoes'], 1)
        self.assertFalse(row['documento_publicado'])
        self.config['max_calls'] = 60
        row = self.run_flow()['documentos']['02_02']
        self.assertTrue(row['qa_elegivel'], row)
        self.assertEqual(sum(role == 'write' and p.get('intervencoes', [{}])[0].get('id') == 'E01'
                             for role, p in self.model.inputs), 1)

    def test_focused_reading_repairs_semantic_repetition_without_local_match(self):
        self.add_inherited_editorial_problem('Explicação repetida sem informação exclusiva. O conteúdo exclusivo permanece.')
        self.model.semantic_repeat = True
        row = self.run_flow()['documentos']['02_02']
        self.assertTrue(row['qa_elegivel'], row)
        doc = read_json(self.output / '02_02/documento.json')
        self.assertIn('O conteúdo exclusivo permanece.', json.dumps(doc, ensure_ascii=False))
        self.assertEqual(row['acabamento_alteracoes'], 1)

    def test_invented_evidence_id_is_rejected(self):
        self.model.research_bad = True
        row = self.run_flow()['documentos']['02_02']
        self.assertFalse(row['qa_elegivel'])
        self.assertEqual(row['intervencoes_aprovadas'], 1)
        self.assertTrue(row['erros'])

    def test_budget_exhaustion_is_collectible_and_resumable(self):
        self.config['max_calls'] = 2
        row = self.run_flow()['documentos']['02_02']
        self.assertEqual(row['status'], 'interrompido')
        self.assertFalse(row['documento_publicado'])
        self.config['max_calls'] = 60
        row = self.run_flow()['documentos']['02_02']
        self.assertEqual(row['status'], 'concluido', row)

    def test_collection_has_comparison_and_no_raw_external_passages(self):
        self.run_flow()
        atomic_json(self.output / '02_02/nao_coletar.json', dict(texto='FONTE_PRIVADA_NAO_EXPORTAR'))
        destination = self.root / 'snapshot'
        collect(self.output, destination)
        self.assertFalse((destination / '.local').exists())
        self.assertTrue(list(destination.glob('02_02/versoes/*/comparacao.json')))
        for path in destination.rglob('*'):
            if path.is_file():
                self.assertNotIn('FONTE_PRIVADA_NAO_EXPORTAR', path.read_text(encoding='utf-8'))
        hashes = read_json(destination / 'manifest_resultados.json')['files']
        self.assertTrue(all(file_hash(destination / name) == value for name, value in hashes.items()))

    def test_source_corruption_is_detected_before_models(self):
        self.manifest.with_name('pages.jsonl').write_text('corrompido', encoding='utf-8')
        with self.assertRaisesRegex(ValueError, 'corrompido'):
            self.run_flow()
        self.assertFalse(self.model.inputs)

    def test_input_missing_specialist_correction_is_blocked(self):
        atomic_json(self.expert, dict(documentos={'02_02': [dict(capitulo=0, bloco=0, depois='Correção ausente', motivo='Segurança')]}))
        with self.assertRaisesRegex(ValueError, 'especialista'):
            self.run_flow()
        self.assertFalse(self.model.inputs)

    def test_inherited_selections_from_same_document_are_not_concatenated(self):
        path = self.legacy / '02_02/evidencias_citadas.jsonl'
        rows = [dict(id='E_FIRST', document_id='same_pdf', collection='old', title='Manual',
            texto=('pump MARCADOR_PRIMEIRO flow operation ' * 35), page_ini=3, page_fim=4,
            source_boundary='known_document', language='en'),
            dict(id='E_SECOND', document_id='same_pdf', collection='old', title='Manual',
            texto=('pump MARCADOR_SEGUNDO pressure operation ' * 35), page_ini=3, page_fim=4,
            source_boundary='known_document', language='en')]
        path.write_text(''.join(json.dumps(row)+'\n' for row in rows), encoding='utf-8')
        base = load_base(self.base, '02_02', self.legacy, self.expert)
        index = inherited_index(base, self.output)
        hits = index.search('pump')
        self.assertEqual(len(hits), 2)
        for hit in hits:
            self.assertFalse('MARCADOR_PRIMEIRO' in hit['texto'] and 'MARCADOR_SEGUNDO' in hit['texto'])
            evidence = source(dict(hit, evidence_origin='herdada'))
            self.assertEqual(evidence['document_id'], 'same_pdf')
            self.assertEqual(evidence['page_fim'], 4)
            self.assertIn(evidence['original_evidence_id'], ('E_FIRST', 'E_SECOND'))

    def test_cancellation_stops_pilot_before_other_documents(self):
        self.model.cancel = True
        result = self.run_flow(('02_02', '03_03'))
        self.assertEqual(result['status'], 'interrompido')
        self.assertFalse((self.output / '03_03/resumo.json').exists())


class ContractTests(unittest.TestCase):
    def test_reading_patterns_do_not_confuse_power_supply_with_source_report(self):
        for text in ['O fabricante consultado recomenda a configuração.', 'No contexto consultado, o resultado é adequado.',
                     'No caso relatado, o teste funcionou.']:
            self.assertTrue(block_issues(dict(texto=text)))
        self.assertFalse(block_issues(dict(texto='A fonte de alimentação fornece energia ao transmissor.')))

    def test_long_duplicate_paragraph_is_blocking_but_shared_terminology_is_not(self):
        paragraph = ' '.join('palavra' + str(n) for n in range(60))
        document = dict(capitulos=[dict(blocos=[dict(id='B1', texto=paragraph), dict(id='B2', texto=paragraph)])])
        self.assertTrue(any(i['bloqueante'] and set(i['blocos']) == {'B1', 'B2'} for i in audit(document)))
        document['capitulos'][0]['blocos'][1]['texto'] = ' '.join('termo' + str(n) for n in range(60))
        self.assertFalse(audit(document))

    def test_missing_queries_are_reported_as_not_executed_not_corpus_failure(self):
        result = asyncio.run(investigate(dict(id='I1', tipo='lacuna_essencial', consultas=[]), {}, None, {}, None))
        self.assertEqual(result['status'], 'nao_executada')
        self.assertEqual(result['leituras'], 0)
        self.assertTrue(result['pendencias'])

    def test_failed_followup_keeps_validated_findings_from_first_reading(self):
        class Index:
            def __init__(self): self.turn = 0
            def query(self, pairs, limit):
                self.turn += 1
                return [dict(chunk_id=str(self.turn), content_hash=str(self.turn), document_id=str(self.turn),
                    texto='Relação técnica com condições de aplicação.', title='Manual', evidence_origin='nova')], []
        class Calls:
            def __init__(self): self.turn = 0
            async def call(self, role, tag, payload, validate, **kwargs):
                self.turn += 1
                if self.turn == 2: raise CallFailure('Falha simulada da segunda leitura')
                data = dict(suficiente=False, achados=[dict(proposicao='Relação validada',
                    citacoes=[payload['fontes'][0]['paragrafos'][0]['id']], tipo='explicacao_tecnica',
                    condicoes=['Condição explícita'], limites=[], pertinencia='direta', sub_objetivos_atendidos=['S1'])],
                    consultas_adicionais=[dict(pt='outra condição operacional', en='another operating condition')], pendencias=[])
                validate(data)
                return data
        result = asyncio.run(investigate(dict(id='I1', sub_objetivos=[dict(id='S1', descricao='Mecanismo'), dict(id='S2', descricao='Limite')],
            consultas=[dict(pt='condição técnica', en='technical condition')]),
            dict(entrada={}), Index(), configuration(), Calls()))
        self.assertEqual(len(result['achados']), 1)
        self.assertEqual(result['leituras'], 1)
        self.assertEqual(len(result['erros']), 1)

    def test_reorganization_moves_original_block_without_rewriting_it(self):
        base = dict(titulo='Teste', capitulos=[dict(id='C1', titulo='A', grupo='Área', blocos=[
            dict(id='B1', subtitulo='Condição', texto='Mecanismo e condição essenciais.')]),
            dict(id='C2', titulo='B', grupo='Área', blocos=[dict(id='B2', subtitulo='Outro', texto='Conhecimento preservado.')])])
        intervention = dict(id='I1', tipo='editorial', alvos=['B1', 'C2'])
        proposal = dict(id='I1', alteracoes=[dict(operacao='mover', alvo='B1', destino='C2', motivo='Melhor sequência',
            preservacao='O bloco é movido integralmente', achados=[], complementos=[]),
            dict(operacao='renomear_capitulo', alvo='C2', capitulo='Mecanismos e condições', motivo='Título claro',
            preservacao='Mantém todos os blocos', achados=[], complementos=[])], pendencias=[])
        before = copy.deepcopy(base)
        validate_changes(proposal, intervention, base, set())
        result = apply_changes(base, [proposal])
        self.assertEqual(base, before)
        self.assertEqual(result['capitulos'][0]['titulo'], 'Mecanismos e condições')
        self.assertEqual(catalog(result)[1]['B1'], catalog(base)[1]['B1'])
        self.assertEqual(set(catalog(result)[1]), {'B1', 'B2'})

    def test_real_inventory_preserves_all_forty_and_expert_corrections(self):
        items = all_items()
        self.assertEqual(len(items), 40)
        # Usar recortes versionados: o workspace compartilhado pode conter edições
        # do usuário ainda não concluídas; não alterá-las para executar os testes.
        with tempfile.TemporaryDirectory() as temp:
            for item in items:
                raw = subprocess.check_output(['git', 'show', 'HEAD:pipeline/qa_research/relatorios/dez_areas_v1/' + item + '/pacote/facets.json'])
                path = Path(temp) / item / 'pacote/facets.json'
                path.parent.mkdir(parents=True)
                path.write_bytes(raw)
                base = load_base(DEFAULT_BASE, item, temp, DEFAULT_EXPERT)
                self.assertTrue(base['pontos'])
                self.assertTrue(catalog(base['documento'])[1])

    def test_plan_is_read_only(self):
        with tempfile.TemporaryDirectory() as temp, redirect_stdout(io.StringIO()):
            output = Path(temp) / 'absent'
            self.assertEqual(main(['--plan', '--output', str(output)]), 0)
            self.assertFalse(output.exists())

    def test_overlapping_block_interventions_cannot_be_planned(self):
        row = dict(id='I1', tipo='editorial', prioridade='alta', alvos=['B1'], pontos=['F1'], objetivo='Clareza', motivo='Redação', sub_objetivos=[], consultas=[])
        with self.assertRaisesRegex(ValueError, 'outra intervenção'):
            C.diagnosis(dict(intervencoes=[row, dict(row, id='I2')], cobertura=[dict(id='F1', estado='atendido', motivo='Completo')], omissoes_escopo=[]), {'B1'}, {'C1'}, {'F1'}, 6)

    def test_false_preservation_criterion_cannot_approve(self):
        flags = {k: True for k in C.FLAGS}
        flags['sem_perda'] = False
        with self.assertRaisesRegex(ValueError, 'contradiz'):
            C.judgment(dict(avaliacoes_operacoes=[dict(op_id='I1_OP01', intervencao_id='I1',
                decisao='aprovar', motivo='Teste', correcao='', criterios=flags)]), {'I1_OP01': {'intervencao_id': 'I1'}})
