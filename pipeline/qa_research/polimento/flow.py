"""Polimento incremental com revisão e persistência transacionais por operação."""
import asyncio
import json
from pathlib import Path

from pipeline.inventario.llm import BudgetExceeded
from pipeline.inventario.textutil import atomic_json
from pipeline.qa_research.v3.runtime import Calls, CallFailure, Fatal, digest, stamp
from . import VERSION, contracts as C, prompts as P
from .documents import catalog, clean, markdown, apply_changes, diff
from .research import CombinedIndex, inherited_index, investigate, public_research, objective_support
from .editorial import audit, pending_work
from .finishing import finish
from .operations import edit_operations


class EditionCalls(Calls):
    async def call(self, role, tag, payload, validate, **kwargs):
        return await super().call(role, tag, dict(payload, edicao=self.edition), validate, **kwargs)


def implementation():
    return digest({p.name: p.read_text(encoding='utf-8') for p in sorted(Path(__file__).parent.glob('*.py'))})


def save_incremental_summary(output_dir, state):
    """Resumo e relatório são legíveis inclusive antes do término ou após cancelamento."""
    output_dir = Path(output_dir)
    atomic_json(output_dir / 'resumo.json', state)
    lines = ['# Nova edição do contexto — polimento', '', '**Estado:** ' + state['status'],
        '', 'Etapa: ' + state.get('etapa', 'preparacao'), '', 'Base: ' + state['origem'], '',
        f"Intervenções aprovadas: {state.get('intervencoes_aprovadas', 0)} de {state.get('intervencoes_planejadas', 0)}.",
        f"Alterações aprovadas: {state.get('alteracoes_aprovadas', 0)}.",
        f"Alterações de acabamento: {state.get('acabamento_alteracoes', 0)}.",
        f"Tentativas externas cumulativas: {state.get('tentativas', 0)}.",
        'Documento publicado: ' + ('sim' if state.get('documento_publicado') else 'não; leia documento_para_revisao.md') + '.',
        'Elegível para QA: ' + ('sim, sujeito à validação especializada' if state.get('qa_elegivel') else 'não') + '.',
        '', 'A preservação de texto herdado não significa nova verificação de todas as afirmações.',
        '', '| Ponto estável | Cobertura | Motivo |', '|---|---|---|']
    lines += ['| ' + r['id'] + ' | ' + r['estado'] + ' | ' + r['motivo'].replace('|', '/') + ' |'
              for r in state.get('cobertura', [])]
    if state.get('erro'):
        lines += ['', 'Interrupção: ' + state['erro']]
    lines += ['', 'Alterações técnicas já comitadas:']
    lines += ['- ' + op['op_id'] + ' (' + p['id'] + '): ' + op['operacao'] + ' em ' + op['alvo']
              for p in state.get('intervencoes_tecnicas_aprovadas', []) for op in p['alteracoes']]
    if state.get('problemas_editoriais_detectados'):
        lines += ['', 'Defeitos detectados na leitura editorial (histórico preservado):']
        lines += ['- ' + ', '.join(p['blocos']) + ': ' + p['descricao'] for p in state['problemas_editoriais_detectados']]
    if state.get('pendencias'):
        lines += ['', 'Trabalho ainda pendente:']
        lines += ['- ' + r['id'] + ' (' + r['tipo'] + '): ' + r['objetivo'] for r in state['pendencias']]
    lines += ['', 'Pareceres, comparação e decisões: `versoes/' + state['versao'] + '/`.']
    report = '\n'.join(lines) + '\n'
    # Mantém o nome da CLI e também o nome solicitado para consumidores externos.
    for name in ('RELATORIO.md', 'relatorio.md'):
        path = output_dir / name
        temporary = path.with_suffix('.md.tmp')
        temporary.write_text(report, encoding='utf-8')
        temporary.replace(path)


def initial_coverage(base, plan):
    previous = {p['id']: p for p in base['resumo_anterior'].get('cobertura', [])}
    return [dict(previous[p['id']] if previous.get(p['id'], {}).get('estado') == 'atendido' else p)
            for p in plan['cobertura']]


def stabilize_coverage(coverage, initial, interventions, proposals):
    """Cobertura curada não regride por preferência por aprofundamento opcional."""
    known = {p['id']: p for p in initial}
    mapping = {i['id']: i for i in interventions}
    removed_points = {pid for p in proposals for op in p['alteracoes'] if op['operacao'] == 'remover'
                      for pid in mapping.get(p['id'], {}).get('pontos', [])}
    stabilized, warnings = [], []
    for point in coverage:
        if (known.get(point['id'], {}).get('estado') == 'atendido' and point['estado'] != 'atendido'
                and point['id'] not in removed_points and not point.get('evidencia_regressao', '').strip()):
            warnings.append(dict(ponto=point['id'], estado_recusado=point['estado'],
                motivo='Cobertura atendida preservada: nenhuma remoção ou evidência concreta de regressão'))
            point = dict(point, estado='atendido', motivo=known[point['id']]['motivo'])
        stabilized.append(point)
    return stabilized, warnings


async def polish(base, global_index, manifest_identity, config, output, transport=None):
    output = Path(output)
    semantic = {k: v for k, v in config.items() if k not in ('workers', 'max_calls', 'request_timeout', 'heartbeat', 'verbose', 'items')}
    version = digest([VERSION, base['fingerprints'], base['entrada'], manifest_identity, semantic, implementation()])[:24]
    work = output / 'versoes' / version
    work.mkdir(parents=True, exist_ok=True)
    calls = EditionCalls(output, config, transport=transport)
    calls.edition = version
    chapters, blocks = catalog(base['documento'])
    state = dict(status='em_andamento', etapa='preparacao', item=base['item'], versao=version, inicio=stamp(),
        base=base['fingerprints'], origem=base['origem'], corpus=manifest_identity, qa_elegivel=False)
    plan, researches, accepted, decisions, errors = None, {}, [], {}, []
    final, editorial = None, []
    for filename in ('documento.json', 'documento.md'):
        (output / filename).unlink(missing_ok=True)

    def checkpoint():
        technical = apply_changes(base['documento'], accepted)
        candidate = apply_changes(technical, editorial)
        intervention_results = []
        for intervention in (plan or {}).get('intervencoes', []):
            iid = intervention['id']
            rows = [r for r in decisions.values() if r.get('intervencao_id') == iid]
            support = objective_support(intervention, researches.get(iid, {}).get('achados', []))
            pending = [msg for p in accepted if p['id'] == iid for msg in p['pendencias']]
            resolved = bool(rows) and all(r['decisao'] == 'aprovar' for r in rows) and not support['sub_objetivos_sem_suporte'] and not pending
            intervention_results.append(dict(intervention, decisao='aprovar' if resolved else 'pendente',
                operacoes=rows, pendencias=pending, **support))
        unresolved = [i for i in intervention_results if i['decisao'] != 'aprovar']
        coverage = (final or {}).get('cobertura', state.get('cobertura_inicial', (plan or {}).get('cobertura', [])))
        problems = list((final or {}).get('problemas', []))
        for problem in state.get('problemas_editoriais_pendentes', []) + [p for p in audit(candidate) if p['bloqueante']]:
            if problem not in problems:
                problems.append(problem)
        omissions = (final or plan or {}).get('omissoes_escopo', [])
        critical = [i['id'] for i in unresolved if i['tipo'] == 'correcao_tecnica']
        publishable = (state['status'] != 'interrompido' and final is not None and final['protecoes_preservadas']
            and not critical and not any(p['critico'] or p.get('tipo') == 'editorial' for p in problems))
        complete = bool(coverage) and all(p['estado'] == 'atendido' for p in coverage) and not omissions
        state.update(atualizado=stamp(), tentativas=calls.budget.used,
            intervencoes_planejadas=len((plan or {}).get('intervencoes', [])),
            intervencoes_aprovadas=len({p['id'] for p in accepted}), intervencoes_resultados=intervention_results,
            intervencoes_tecnicas_aprovadas=accepted, operacoes_decisoes=list(decisions.values()),
            alteracoes_aprovadas=sum(len(p['alteracoes']) for p in accepted),
            acabamento_alteracoes=sum(len(p['alteracoes']) for p in editorial),
            cobertura=coverage, pendencias=pending_work(unresolved, coverage, omissions, problems),
            problemas_editoriais=[p for p in problems if p.get('tipo') == 'editorial'],
            riscos_tecnicos_pendentes=critical, erros=errors, documento_publicado=bool(publishable),
            qa_elegivel=bool(publishable and complete and not any(i['tipo'] == 'lacuna_essencial' for i in unresolved) and not problems),
            documento_sha256=digest(clean(candidate)), baseline_sha256=digest(clean(base['documento'])),
            palavras_antes=sum(len(b['texto'].split()) for b in blocks.values()),
            palavras_depois=sum(len(b['texto'].split()) for b in catalog(candidate)[1].values()),
            criterio='Revisão automática de alterações; validação pelo especialista pendente')
        atomic_json(work / 'alteracoes_aprovadas.json', accepted)
        atomic_json(work / 'acabamento_aprovado.json', editorial)
        atomic_json(work / 'decisoes.json', list(decisions.values()))
        atomic_json(work / 'pesquisas.json', {k: public_research(r) for k, r in researches.items()})
        atomic_json(output / '.local' / 'pesquisas' / (version + '.json'), researches)
        atomic_json(output / 'documento_para_revisao.json', clean(candidate))
        (output / 'documento_para_revisao.md').write_text(markdown(candidate), encoding='utf-8')
        save_incremental_summary(output, state)
        return technical, candidate

    async def read(intervention, index):
        iid = intervention['id']
        try:
            result = await investigate(intervention, base, index, config, calls)
        except (Fatal, BudgetExceeded):
            raise
        except (CallFailure, ValueError) as exc:
            result = dict(id=iid, status='falha_leitura', achados=[], fontes=[], consultas=[], leituras=0,
                pendencias=[str(exc)], **objective_support(intervention, []))
            errors.append(dict(intervencao=iid, etapa='pesquisa', erro=str(exc)))
        researches[iid] = result
        errors.extend(result.get('erros', []))
        checkpoint()

    async def edit_batch(batch, tag):
        current = apply_changes(base['documento'], accepted)
        research = {i['id']: researches[i['id']] for i in batch}
        estimate = dict(entrada=base['entrada'], documento=current, intervencoes=batch, pesquisa=research)
        if len(json.dumps(estimate, ensure_ascii=False)) + len(P.EDIT) > config['max_input_chars'] and len(batch) > 1:
            middle = len(batch) // 2
            await edit_batch(batch[:middle], tag + 'a')
            await edit_batch(batch[middle:], tag + 'b')
            return
        await edit_operations(base, current, batch, research, calls, work, tag, accepted, decisions, errors, checkpoint)

    try:
        checkpoint()
        plan = await calls.call('plan', 'diagnostico', dict(entrada=base['entrada'], documento=base['documento'],
            pontos=base['pontos'], protecoes=base['protecoes'], limite=config['max_interventions'],
            sinais_editoriais=audit(base['documento']), cobertura_anterior=base['resumo_anterior'].get('cobertura', []),
            pendencias_anteriores=base['resumo_anterior'].get('recortes_pendentes', []),
            observacao_editorial=base['resumo_anterior'].get('observacao_editorial', '')),
            lambda d: C.diagnosis(d, blocks, chapters, {p['id'] for p in base['pontos']}, config['max_interventions']), system=P.DIAGNOSE)
        atomic_json(work / 'diagnostico.json', plan)
        state.update(etapa='diagnostico', cobertura_inicial=initial_coverage(base, plan))
        checkpoint()
        old_index = await asyncio.to_thread(inherited_index, base, output)
        indexes = [('nova', global_index)]
        if old_index is not None:
            indexes.insert(0, ('herdada', old_index))
        index = CombinedIndex(indexes)
        state['pesquisa_herdada_disponivel'] = old_index is not None
        ordered = sorted(plan['intervencoes'], key=lambda i: ('alta', 'media', 'baixa').index(i['prioridade']))
        tasks = [asyncio.create_task(read(i, index)) for i in ordered]
        try:
            results = await asyncio.gather(*tasks, return_exceptions=True)
            for result in results:
                if isinstance(result, BaseException):
                    raise result
        finally:
            for task in tasks:
                if not task.done():
                    task.cancel()
            await asyncio.gather(*tasks, return_exceptions=True)
        state['etapa'] = 'pesquisa'
        checkpoint()
        editable = []
        for intervention in ordered:
            iid = intervention['id']
            if intervention['tipo'] != 'editorial' and not researches[iid]['achados']:
                decisions[iid] = dict(id=iid, intervencao_id=iid, decisao='sem_alteracao',
                    motivo='Pesquisa: ' + researches[iid].get('status', 'sem_achados') + '. ' + '; '.join(researches[iid]['pendencias']))
            else:
                editable.append(intervention)
        for start in range(0, len(editable), config['batch_size']):
            batch = editable[start:start + config['batch_size']]
            tag = 'edicao_' + str(start // config['batch_size'] + 1).zfill(2)
            try:
                await edit_batch(batch, tag)
            except (Fatal, BudgetExceeded):
                raise
            except (CallFailure, ValueError) as exc:
                errors.append(dict(etapa=tag, erro=str(exc)))
        state['etapa'] = 'edicao_tecnica'
        checkpoint()
        candidate = apply_changes(base['documento'], accepted)
        final = await finish(base, candidate, accepted, decisions, plan, calls, work, editorial,
            state=state, checkpoint=checkpoint, errors=errors)
        final['cobertura'], warnings = stabilize_coverage(final['cobertura'], state['cobertura_inicial'],
            plan['intervencoes'], accepted + editorial)
        state['avisos_estabilizacao_cobertura'] = warnings
        for warning in warnings:
            calls.log(dict(kind='estabilizacao_cobertura', **warning))
        atomic_json(work / 'coerencia_final.json', final)
        state.update(status='avaliado', etapa='consolidacao')
        checkpoint()
    except (asyncio.CancelledError, KeyboardInterrupt) as exc:
        state.update(status='interrompido', erro=type(exc).__name__ + ': execução interrompida; checkpoints preservados')
        raise
    except Exception as exc:
        state.update(status='interrompido', erro=type(exc).__name__ + ': ' + str(exc)[:900])
    finally:
        try:
            technical, candidate = checkpoint()
            if state['status'] != 'interrompido':
                state['status'] = 'concluido' if state['qa_elegivel'] else 'parcial' if state['documento_publicado'] else 'revisao_requerida'
            state['fim'] = stamp()
            if state['documento_publicado']:
                atomic_json(output / 'documento.json', clean(candidate))
                (output / 'documento.md').write_text(markdown(candidate), encoding='utf-8')
            atomic_json(work / 'comparacao.json', dict(base=base['fingerprints'], alteracoes=diff(base['documento'], accepted),
                acabamento=diff(technical, editorial),
                blocos_inalterados=[bid for bid, block in blocks.items() if catalog(candidate)[1].get(bid) == block],
                procedencia='Texto herdado preservado não equivale a nova verificação de todas as suas afirmações'))
            save_incremental_summary(output, state)
        finally:
            await calls.close()
    return state
