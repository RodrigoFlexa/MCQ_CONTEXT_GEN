"""Diagnosticar, pesquisar intervenções, editar patches e revisar uma nova edição."""
import asyncio
import json
from pathlib import Path

from pipeline.inventario.llm import BudgetExceeded
from pipeline.inventario.textutil import atomic_json
from pipeline.qa_research.v3.runtime import Calls, CallFailure, Fatal, digest, stamp
from . import VERSION, contracts as C, prompts as P
from .documents import catalog, clean, markdown, validate_changes, apply_changes, diff
from .research import CombinedIndex, inherited_index, investigate, evidence_payload, public_research
from .editorial import audit, pending_work
from .finishing import finish


class EditionCalls(Calls):
    async def call(self, role, tag, payload, validate, **kwargs):
        return await super().call(role, tag, dict(payload, edicao=self.edition), validate, **kwargs)


def implementation():
    return digest({p.name: p.read_text(encoding='utf-8') for p in sorted(Path(__file__).parent.glob('*.py'))})


def snapshot(base, proposals, research):
    candidate = apply_changes(base['documento'], proposals)
    used = {aid for proposal in proposals for row in proposal['alteracoes'] for aid in row['achados']}
    cited = {key: dict(r, achados=[f for f in r['achados'] if f['id'] in used]) for key, r in research.items()}
    return dict(entrada=base['entrada'], documento=candidate, protecoes=base['protecoes'],
        alteracoes=diff(base['documento'], proposals),
        achados=[f for r in cited.values() for f in r['achados']], fontes=evidence_payload(cited))


async def polish(base, global_index, manifest_identity, config, output, transport=None):
    output = Path(output)
    semantic = {k: v for k, v in config.items() if k not in ('workers', 'max_calls', 'request_timeout', 'heartbeat', 'verbose', 'items')}
    version = digest([VERSION, base['fingerprints'], base['entrada'], manifest_identity, semantic, implementation()])[:24]
    work = output / 'versoes' / version
    work.mkdir(parents=True, exist_ok=True)
    calls = EditionCalls(output, config, transport=transport)
    calls.edition = version
    chapters, blocks = catalog(base['documento'])
    state = dict(status='em_andamento', item=base['item'], versao=version, inicio=stamp(),
        base=base['fingerprints'], origem=base['origem'], corpus=manifest_identity, qa_elegivel=False)
    plan, researches, accepted, decisions, errors = None, {}, [], {}, []
    final = None
    editorial = []
    # Nunca apresentar uma publicação antiga como resultado da versão em andamento.
    for filename in ('documento.json', 'documento.md'):
        (output / filename).unlink(missing_ok=True)

    def checkpoint():
        atomic_json(work / 'alteracoes_aprovadas.json', accepted)
        atomic_json(work / 'acabamento_aprovado.json', editorial)
        atomic_json(work / 'decisoes.json', list(decisions.values()))
        atomic_json(work / 'pesquisas.json', {k: public_research(r) for k, r in researches.items()})
        atomic_json(output / '.local' / 'pesquisas' / (version + '.json'), researches)

    async def read(intervention, index):
        iid = intervention['id']
        try:
            result = await investigate(intervention, base, index, config, calls)
        except (Fatal, BudgetExceeded):
            raise
        except (CallFailure, ValueError) as exc:
            result = dict(id=iid, status='falha_leitura', achados=[], fontes=[], consultas=[], leituras=0, pendencias=[str(exc)])
            errors.append(dict(intervencao=iid, etapa='pesquisa', erro=str(exc)))
        researches[iid] = result
        errors.extend(result.get('erros', []))
        checkpoint()

    async def judge(proposals, research, tag):
        if not proposals:
            return {}
        payload = snapshot(base, accepted + proposals, research)
        payload['avaliar'] = [p['id'] for p in proposals]
        result = await calls.call('review', tag, payload,
            lambda d: C.judgment(d, payload['avaliar']), system=P.REVIEW)
        atomic_json(work / (tag + '.json'), result)
        return {r['id']: r for r in result['avaliacoes']}

    async def edit_batch(batch, tag):
        research = {i['id']: researches[i['id']] for i in batch}
        current = apply_changes(base['documento'], accepted)
        payload = dict(entrada=base['entrada'], documento=current, protecoes=base['protecoes'],
            intervencoes=batch, achados={k: r['achados'] for k, r in research.items()}, fontes=evidence_payload(research))
        if len(json.dumps(payload, ensure_ascii=False)) + len(P.EDIT) > config['max_input_chars'] and len(batch) > 1:
            middle = len(batch) // 2
            await edit_batch(batch[:middle], tag + 'a')
            await edit_batch(batch[middle:], tag + 'b')
            return
        mapping = {i['id']: i for i in batch}
        original = await calls.call('write', tag, payload, lambda d: C.editing(d, mapping), system=P.EDIT)
        atomic_json(work / (tag + '.json'), original)
        proposals, local = [], {}

        def checked(items):
            good, bad = [], {}
            for row in items:
                try:
                    validate_changes(row, mapping[row['id']], current,
                                     {f['id'] for f in research[row['id']]['achados']})
                    if row['alteracoes']:
                        good.append(row)
                    else:
                        bad[row['id']] = dict(id=row['id'], decisao='sem_alteracao',
                            motivo='; '.join(row['pendencias']) or 'Nenhuma alteração fundamentada proposta')
                except (ValueError, KeyError, TypeError) as exc:
                    bad[row['id']] = dict(id=row['id'], decisao='corrigir', motivo='Contrato local', correcao=str(exc))
            return good, bad

        proposals, local = checked(original['itens'])
        judgments = await judge(proposals, research, tag + '_parecer')
        judgments.update(local)
        repair = {k: r for k, r in judgments.items() if r['decisao'] == 'corrigir'}
        # Aprovações independentes são preservadas mesmo se o reparo de outro item falhar.
        accepted.extend(p for p in proposals if judgments[p['id']]['decisao'] == 'aprovar')
        decisions.update(judgments)
        checkpoint()
        if repair:
            correction = dict(payload, intervencoes=[mapping[k] for k in repair],
                anteriores=[r for r in original['itens'] if r['id'] in repair], pareceres=list(repair.values()))
            try:
                fixed = await calls.call('write', tag + '_correcao', correction,
                    lambda d: C.editing(d, repair), system=P.EDIT)
                atomic_json(work / (tag + '_correcao.json'), fixed)
                valid, failed = checked(fixed['itens'])
                reviewed = await judge(valid, research, tag + '_reavaliacao')
                reviewed.update(failed)
                accepted.extend(p for p in valid if reviewed[p['id']]['decisao'] == 'aprovar')
                decisions.update(reviewed)
            except (Fatal, BudgetExceeded):
                raise
            except (CallFailure, ValueError) as exc:
                errors.append(dict(etapa=tag + '_correcao', erro=str(exc)))
        checkpoint()

    try:
        plan = await calls.call('plan', 'diagnostico', dict(entrada=base['entrada'], documento=base['documento'],
            pontos=base['pontos'], protecoes=base['protecoes'], limite=config['max_interventions'],
            sinais_editoriais=audit(base['documento']),
            pendencias_anteriores=base['resumo_anterior'].get('recortes_pendentes', []),
            observacao_editorial=base['resumo_anterior'].get('observacao_editorial', '')),
            lambda d: C.diagnosis(d, blocks, chapters, {p['id'] for p in base['pontos']}, config['max_interventions']), system=P.DIAGNOSE)
        atomic_json(work / 'diagnostico.json', plan)
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
        editable = []
        for intervention in ordered:
            iid = intervention['id']
            if intervention['tipo'] != 'editorial' and not researches[iid]['achados']:
                result = researches[iid]
                decisions[iid] = dict(id=iid, decisao='sem_alteracao',
                    motivo='Pesquisa: ' + result.get('status', 'sem_achados') + '. ' + '; '.join(result['pendencias']))
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
                for row in batch:
                    decisions.setdefault(row['id'], dict(id=row['id'], decisao='pendente', motivo=str(exc)))
        candidate = apply_changes(base['documento'], accepted)
        final = await finish(base, candidate, accepted, decisions, plan, calls, work, editorial)
        state['status'] = 'avaliado'
    except asyncio.CancelledError:
        state.update(status='interrompido', erro='CancelledError: execução interrompida; checkpoints preservados')
        raise
    except Exception as exc:
        state.update(status='interrompido', erro=type(exc).__name__ + ': ' + str(exc)[:900])
    finally:
        checkpoint()
        technical_candidate = apply_changes(base['documento'], accepted)
        candidate = apply_changes(technical_candidate, editorial)
        unresolved = [i for i in (plan or {}).get('intervencoes', []) if decisions.get(i['id'], {}).get('decisao') != 'aprovar']
        critical = [i['id'] for i in unresolved if i['tipo'] == 'correcao_tecnica']
        coverage = final['cobertura'] if final else (plan or {}).get('cobertura', [])
        problems = list((final or {}).get('problemas', []))
        problems.extend(p for p in audit(candidate) if p['bloqueante'] and p not in problems)
        omissions = (final or plan or {}).get('omissoes_escopo', [])
        publishable = state['status'] != 'interrompido' and final is not None and final['protecoes_preservadas'] and not critical and not any(p['critico'] or p.get('tipo') == 'editorial' for p in problems)
        complete = bool(coverage) and all(p['estado'] == 'atendido' for p in coverage) and not omissions
        essential = [i['id'] for i in unresolved if i['tipo'] == 'lacuna_essencial']
        state.update(fim=stamp(), tentativas=calls.budget.used, intervencoes_planejadas=len((plan or {}).get('intervencoes', [])),
            intervencoes_aprovadas=len(accepted), alteracoes_aprovadas=len(diff(base['documento'], accepted)),
            cobertura=coverage, pendencias=pending_work(unresolved, coverage, omissions, problems),
            problemas_editoriais=[p for p in problems if p.get('tipo') == 'editorial'],
            acabamento_alteracoes=len(diff(technical_candidate, editorial)),
            riscos_tecnicos_pendentes=critical, erros=errors,
            documento_publicado=publishable, qa_elegivel=bool(publishable and complete and not essential and not problems),
            documento_sha256=digest(clean(candidate)), baseline_sha256=digest(clean(base['documento'])),
            palavras_antes=sum(len(b['texto'].split()) for b in blocks.values()),
            palavras_depois=sum(len(b['texto'].split()) for b in catalog(candidate)[1].values()),
            criterio='Revisão automática de alterações; validação pelo especialista pendente')
        if state['status'] != 'interrompido':
            state['status'] = 'concluido' if state['qa_elegivel'] else 'parcial' if publishable else 'revisao_requerida'
        atomic_json(output / 'documento_para_revisao.json', clean(candidate))
        (output / 'documento_para_revisao.md').write_text(markdown(candidate), encoding='utf-8')
        if publishable:
            atomic_json(output / 'documento.json', clean(candidate))
            (output / 'documento.md').write_text(markdown(candidate), encoding='utf-8')
        atomic_json(work / 'comparacao.json', dict(base=base['fingerprints'], alteracoes=diff(base['documento'], accepted),
            acabamento=diff(technical_candidate, editorial),
            blocos_inalterados=[bid for bid, block in blocks.items() if catalog(candidate)[1].get(bid) == block],
            procedencia='Texto herdado preservado não equivale a nova verificação de todas as suas afirmações'))
        atomic_json(output / 'resumo.json', state)
        await calls.close()
    return state
