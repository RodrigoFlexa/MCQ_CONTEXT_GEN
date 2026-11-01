"""Transações por operação, compartilhadas pela edição técnica e pelo acabamento."""
import copy
import json
import re

from pipeline.inventario.llm import BudgetExceeded
from pipeline.inventario.textutil import atomic_json
from pipeline.qa_research.v3.runtime import CallFailure, Fatal
from . import contracts as C, prompts as P
from .documents import apply_changes, build_review_payload, validate_changes
from .research import evidence_payload, objective_support


def operation_map(proposals):
    return {op['op_id']: dict(op, intervencao_id=p['id'])
            for p in proposals for op in p['alteracoes']}


def select_operations(proposals, ids):
    return [dict(p, alteracoes=[op for op in p['alteracoes'] if op['op_id'] in ids])
            for p in proposals if any(op['op_id'] in ids for op in p['alteracoes'])]


def dependent_operations(operations):
    """Fusões declaradas e conflitos de alvo não são commits independentes."""
    deps = {oid: set(op.get('dependencias', [])) for oid, op in operations.items()}
    for oid, op in operations.items():
        preserved_in = set(re.findall(r'\b(?:B[0-9]+_[0-9]+|N_[A-Za-z0-9_]+)\b', op.get('preservacao', '')))
        for other, peer in operations.items():
            if other == oid:
                continue
            destructive = {'substituir', 'remover', 'mover', 'renomear_capitulo'}
            same_target = (op.get('alvo') is not None and op.get('alvo') == peer.get('alvo')
                and (op.get('operacao') in destructive and peer.get('operacao') in destructive
                     or 'remover' in (op.get('operacao'), peer.get('operacao'))))
            fusion = peer.get('alvo') in preserved_in and ('remover' in (op.get('operacao'), peer.get('operacao')))
            if same_target or fusion:
                deps[oid].add(other)
                deps[other].add(oid)
    return deps


async def edit_operations(base, document, batch, research, calls, work, tag,
                          committed, decisions, errors, checkpoint, *, system=None, problems=None):
    """Salva aprovações antes do único reparo, que recebe só os op_id pendentes."""
    system = system or P.EDIT
    mapping = {i['id']: dict(i, **objective_support(i, research.get(i['id'], {}).get('achados', []))) for i in batch}

    def payload_for(current, selected):
        shown = current
        if system == P.EDITORIAL:
            targets = {bid for i in selected for bid in i['alvos']}
            C.require(len(targets) <= 3, 'Micro-acabamento permite no máximo três blocos')
            shown = dict(current, capitulos=[dict(c, blocos=[b for b in c['blocos'] if b['id'] in targets])
                for c in current['capitulos'] if any(b['id'] in targets for b in c['blocos'])])
        payload = dict(entrada=base['entrada'], documento=shown, protecoes=base['protecoes'],
            intervencoes=selected, achados={i['id']: research.get(i['id'], {}).get('achados', []) for i in selected},
            fontes=evidence_payload(research))
        if problems is not None:
            payload['problemas'] = problems
        return payload

    async def judge(proposals, current, suffix):
        if not proposals:
            return {}
        payload = build_review_payload(dict(base, documento=current), list(mapping.values()), proposals, research, base['protecoes'])
        if len(json.dumps(payload, ensure_ascii=False)) + len(P.REVIEW) > calls.config['max_input_chars']:
            ids = list(operation_map(proposals))
            if len(ids) > 1:
                middle = len(ids) // 2
                left = await judge(select_operations(proposals, set(ids[:middle])), current, suffix + 'a')
                right = await judge(select_operations(proposals, set(ids[middle:])), current, suffix + 'b')
                return dict(left, **right)
        result = await calls.call('review', tag + suffix, payload,
            lambda d: C.judgment(d, operation_map(proposals)), system=P.REVIEW)
        atomic_json(work / (tag + suffix + '.json'), result)
        return {r['op_id']: r for r in result['avaliacoes_operacoes']}

    def checked(items, current):
        valid, failed = [], {}
        for item in items:
            good = []
            intervention = mapping[item['id']]
            for sid in intervention['sub_objetivos_sem_suporte']:
                pending = 'Sem suporte direto para ' + sid
                if pending not in item['pendencias']:
                    item['pendencias'].append(pending)
            if not item['alteracoes']:
                decisions[item['id']] = dict(id=item['id'], intervencao_id=item['id'], decisao='sem_alteracao',
                    motivo='; '.join(item['pendencias']) or 'Nenhuma alteração proposta')
            for op in item['alteracoes']:
                single = dict(item, alteracoes=[op])
                try:
                    validate_changes(single, intervention, current,
                        {f['id'] for f in research.get(item['id'], {}).get('achados', [])})
                    if system == P.EDITORIAL:
                        C.require(op['operacao'] in ('substituir', 'remover'),
                                  'Acabamento somente substitui/remove texto')
                    good.append(op)
                except (ValueError, KeyError, TypeError) as exc:
                    failed[op['op_id']] = dict(op_id=op['op_id'], intervencao_id=item['id'],
                        decisao='corrigir', motivo='Contrato local', correcao=str(exc))
            if good:
                valid.append(dict(item, alteracoes=good))
        return valid, failed

    def commit(proposals, judgments, all_operations, current, *, repair_allowed=True):
        dependencies = dependent_operations(all_operations)
        eligible = {oid for oid, decision in judgments.items() if decision['decisao'] == 'aprovar'}
        while True:
            blocked = {oid for oid in eligible if dependencies[oid] - eligible}
            if not blocked:
                break
            eligible -= blocked
        for oid, decision in judgments.items():
            if decision['decisao'] == 'aprovar' and oid not in eligible:
                decision.update(decisao='corrigir' if repair_allowed else 'rejeitar', motivo='Fusão depende de operação ainda não aprovada',
                    correcao='Preserve o conhecimento independentemente das operações rejeitadas ou pendentes')
        # Cada componente acoplado é atômico; uma falha não desfaz outros commits.
        remaining = set(eligible)
        while remaining:
            seed = next(oid for oid in all_operations if oid in remaining)
            group, queue = {seed}, [seed]
            while queue:
                for dep in dependencies[queue.pop()] & remaining:
                    if dep not in group:
                        group.add(dep)
                        queue.append(dep)
            selected = select_operations(proposals, group)
            try:
                updated = apply_changes(current, selected)
            except (ValueError, KeyError, StopIteration) as exc:
                for oid in group:
                    judgments[oid].update(decisao='rejeitar', motivo='Conflito transacional: ' + str(exc))
            else:
                committed.extend(copy.deepcopy(selected))
                current = updated
            remaining -= group
        decisions.update(judgments)
        checkpoint()
        return current

    payload = payload_for(document, list(mapping.values()))
    original = await calls.call('write', tag, payload, lambda d: C.editing(d, mapping), system=system)
    atomic_json(work / (tag + '.json'), original)
    valid, local = checked(original['itens'], document)
    judgments = await judge(valid, document, '_parecer')
    judgments.update(local)
    operations = operation_map(original['itens'])
    document = commit(valid, judgments, operations, document)
    repair = {oid: r for oid, r in judgments.items() if r['decisao'] == 'corrigir'}
    if repair:
        previous = select_operations(original['itens'], set(repair))
        ids = {p['id'] for p in previous}
        correction = payload_for(document, [mapping[iid] for iid in mapping if iid in ids])
        correction.update(anteriores=previous, pareceres=list(repair.values()), op_ids_para_reparar=list(repair),
            instrucao_reparo='Retorne somente os op_id indicados, mantendo seus IDs, operação e alvo. '
                'O documento já contém os commits aprovados; não os reapresente.')
        expected = {oid: dict(operations[oid], alvos_autorizados=mapping[operations[oid]['intervencao_id']]['alvos']) for oid in repair}
        try:
            fixed = await calls.call('write', tag + '_correcao', correction,
                lambda d: C.editing(d, ids, expected), system=system)
            atomic_json(work / (tag + '_correcao.json'), fixed)
            valid, local = checked(fixed['itens'], document)
            reviewed = await judge(valid, document, '_reavaliacao')
            reviewed.update(local)
            for row in reviewed.values():
                if row['decisao'] == 'corrigir':
                    row.update(decisao='rejeitar', motivo='Reparo único insuficiente: ' + row['motivo'])
            document = commit(valid, reviewed, operation_map(fixed['itens']), document, repair_allowed=False)
        except (Fatal, BudgetExceeded):
            raise
        except (CallFailure, ValueError) as exc:
            errors.append(dict(etapa=tag + '_correcao', erro=str(exc)))
            for oid in repair:
                decisions[oid] = dict(repair[oid], decisao='rejeitar', motivo='Falha no reparo único: ' + str(exc))
            checkpoint()
    return document
