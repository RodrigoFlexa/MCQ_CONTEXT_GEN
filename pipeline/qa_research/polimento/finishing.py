"""Acabamento em micro-intervenções, com commits e reparos por operação."""
from pipeline.inventario.llm import BudgetExceeded
from pipeline.inventario.textutil import atomic_json
from pipeline.qa_research.v3.runtime import CallFailure, Fatal
from . import contracts as C, prompts as P
from .documents import catalog, diff
from .editorial import audit
from .operations import edit_operations


def cluster_problems(problems):
    """Nunca separa os blocos de um defeito; cada micro-lote tem até três IDs."""
    batches = []
    for problem in sorted(problems, key=lambda p: -len(set(p['blocos']))):
        targets = set(problem['blocos'])
        C.require(0 < len(targets) <= 3, 'Um defeito editorial deve acoplar de um a três blocos')
        batch = next((b for b in batches if len(set(b['alvos']) | targets) <= 3), None)
        if batch is None:
            batch = dict(id=f'E{len(batches) + 1:02d}', tipo='editorial', alvos=[], sub_objetivos=[],
                objetivo='Resolver somente os defeitos editoriais identificados', motivo='Leitura editorial focada',
                consultas=[], problemas=[])
            batches.append(batch)
        batch['alvos'] = sorted(set(batch['alvos']) | targets)
        batch['problemas'].append(problem)
    return batches


async def finish(base, candidate, accepted, decisions, plan, calls, work, editorial,
                 *, state=None, checkpoint=None, errors=None):
    state = state if state is not None else {}
    checkpoint = checkpoint or (lambda: None)
    errors = errors if errors is not None else []

    async def read(document, tag):
        signals = audit(document)
        result = await calls.call('review', tag,
            dict(documento=document, sinais_editoriais=signals),
            lambda d: C.editorial_review(d, catalog(document)[1]), system=P.EDITORIAL_AUDIT)
        problems = [dict(p, tipo='editorial', critico=False) for p in result['problemas']]
        problems += [p for p in signals if p['bloqueante'] and p not in problems]
        atomic_json(work / (tag + '.json'), dict(problemas=problems, sinais=signals))
        return problems

    problems = await read(candidate, 'leitura_editorial')
    state.update(etapa='leitura_editorial', leitura_editorial=problems,
        problemas_editoriais_detectados=problems, problemas_editoriais_pendentes=problems)
    checkpoint()
    batches = cluster_problems(problems)
    atomic_json(work / 'micro_intervencoes_editoriais.json', batches)
    for intervention in batches:
        existing = catalog(candidate)[1]
        intervention = dict(intervention, alvos=[bid for bid in intervention['alvos'] if bid in existing])
        if not intervention['alvos']:
            continue
        tag = 'acabamento_' + intervention['id']
        try:
            candidate = await edit_operations(base, candidate, [intervention], {}, calls, work, tag,
                editorial, decisions, errors, checkpoint, system=P.EDITORIAL, problems=intervention['problemas'])
        except (Fatal, BudgetExceeded):
            raise
        except (CallFailure, ValueError) as exc:
            errors.append(dict(etapa=tag, erro=str(exc)))
            checkpoint()
    state['etapa'] = 'acabamento'
    checkpoint()
    if editorial:
        problems = await read(candidate, 'leitura_editorial_conferencia')
        state['problemas_editoriais_pendentes'] = problems
        checkpoint()

    result = await calls.call('review', 'coerencia_final',
        dict(entrada=base['entrada'], documento=candidate, pontos=base['pontos'], protecoes=base['protecoes'],
             alteracoes=diff(base['documento'], accepted), acabamento=editorial,
             decisoes=list(decisions.values()), diagnostico=plan, sinais_editoriais=audit(candidate),
             cobertura_inicial_diagnostico=plan['cobertura'],
             cobertura_base_anterior=base['resumo_anterior'].get('cobertura', []),
             cobertura_anterior=state.get('cobertura_inicial', plan['cobertura'])),
        lambda d: C.final_review(d, catalog(candidate)[1], {p['id'] for p in base['pontos']}), system=P.CONSOLIDATE)
    for problem in problems:
        if problem not in result['problemas']:
            result['problemas'].append(problem)
    atomic_json(work / 'coerencia_final.json', result)
    state['etapa'] = 'consolidacao'
    checkpoint()
    return result
