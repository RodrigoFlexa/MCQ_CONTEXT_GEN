"""Leitura editorial focada, um reparo e conferência da edição resultante."""
from pipeline.inventario.textutil import atomic_json
from . import contracts as C, prompts as P
from .documents import catalog, apply_changes, validate_changes, diff
from .editorial import audit


async def finish(base, candidate, accepted, decisions, plan, calls, work, editorial):
    async def read(document, tag):
        signals = audit(document)
        result = await calls.call('review', tag,
            dict(documento=document, sinais_editoriais=signals),
            lambda d: C.editorial_review(d, catalog(document)[1]), system=P.EDITORIAL_AUDIT)
        problems = [dict(p, tipo='editorial', critico=False) for p in result['problemas']]
        problems += [p for p in signals if p['bloqueante']]
        result = dict(problemas=problems, sinais=signals)
        atomic_json(work / (tag + '.json'), result)
        return problems

    problems = await read(candidate, 'leitura_editorial')
    if problems:
        targets = sorted({bid for p in problems for bid in p['blocos']})
        intervention = dict(id='E01', tipo='editorial', alvos=targets,
            objetivo='Resolver somente os defeitos editoriais identificados', motivo='Leitura global focada', consultas=[])
        payload = dict(entrada=base['entrada'], documento=candidate, protecoes=base['protecoes'],
            intervencoes=[intervention], problemas=problems, achados={'E01': []}, fontes=[])

        def validate(data):
            C.editing(data, {'E01'})
            proposal = data['itens'][0]
            validate_changes(proposal, intervention, candidate, set())
            for change in proposal['alteracoes']:
                C.require(change['operacao'] in ('substituir', 'remover') and not change['achados'] and not change['complementos'],
                          'Acabamento apenas substitui/remove texto; não acrescenta fundamento factual')

        fixed = await calls.call('write', 'acabamento_editorial', payload, validate, system=P.EDITORIAL)
        atomic_json(work / 'acabamento_editorial.json', fixed)
        proposal = fixed['itens'][0]
        if proposal['alteracoes']:
            edited = apply_changes(candidate, [proposal])
            changes = diff(candidate, [proposal])
            judgment = await calls.call('review', 'acabamento_parecer',
                dict(entrada=base['entrada'], documento=edited, protecoes=base['protecoes'],
                     alteracoes=changes, avaliar=['E01'], achados=[], fontes=[], problemas_originais=problems,
                     restricao='Edição editorial: nenhum fato novo; preservar condições e informação exclusiva'),
                lambda d: C.judgment(d, {'E01'}), system=P.REVIEW)
            atomic_json(work / 'acabamento_parecer.json', judgment)
            if judgment['avaliacoes'][0]['decisao'] == 'aprovar':
                editorial.append(proposal)
                atomic_json(work / 'acabamento_aprovado.json', editorial)
                candidate = edited
                problems = await read(candidate, 'leitura_editorial_conferencia')
        # Nunca repetir o reparo até o modelo aprovar. Defeitos restantes ficam pendentes.

    result = await calls.call('review', 'coerencia_final',
        dict(entrada=base['entrada'], documento=candidate, pontos=base['pontos'], protecoes=base['protecoes'],
             alteracoes=diff(base['documento'], accepted), acabamento=editorial,
             decisoes=list(decisions.values()), diagnostico=plan, sinais_editoriais=audit(candidate)),
        lambda d: C.final_review(d, catalog(candidate)[1], {p['id'] for p in base['pontos']}), system=P.CONSOLIDATE)
    # Um parecer geral positivo não apaga falha observada pela leitura específica ou pelo código.
    result['problemas'].extend(problems)
    atomic_json(work / 'coerencia_final.json', result)
    return result
