"""Rodada com checkpoints e validação independente de autoria, resolução e parecer."""
import copy
import json
from pathlib import Path

from pipeline.inventario.textutil import atomic_json, read_json
from . import contracts as C, prompts as P, prompts_fluxo as F
from .validation import indexed, partition, resolve_evidence, source_with_passages, target_identity, question_key as key


class CandidateRound:
    def __init__(self, calls, path, source, inventory, similarity, config, enrich, *, on_save=None, contexts=None):
        self.calls, self.path = calls, Path(path)
        self.source, self.inventory, self.similarity = source, inventory, similarity
        self.config, self.enrich, self.on_save = config, enrich, on_save or (lambda data: None)
        self.contexts = contexts
        self.blocks = {b['id']: b for b in source}
        self.data = read_json(self.path) or dict(records=[], alvos={}, impedimentos=[], erros_entrada=[], gerado=False)

    def save(self):
        atomic_json(self.path, self.data)
        self.on_save(self.data)

    def error(self, record, stage, error):
        record.setdefault('erros_validacao', []).append(dict(etapa=stage, erro=str(error)))
        self.calls.progress(f'[candidata:{record["id"]}] {stage}: {str(error)[:300]}', flush=True)

    def fits(self, payload, system):
        return len(json.dumps(payload, ensure_ascii=False)) + len(system) <= self.config['max_input_chars']

    def compact(self, question):
        # Alvos e contexto já seguem separadamente; não duplicar as mesmas passagens.
        return {k: v for k, v in question.items() if k not in ('blocos_contexto', 'contexto_tecnico', 'afirmacoes_alvo')}

    def context(self, record):
        return self.contexts(record['alvo']) if self.contexts else self.source

    def enrich_record(self, record):
        try:
            allowed = {b['id']: b for b in self.context(record)}
            for criterion in record['questao']['criterios']:
                C.evidence(criterion['evidencias'], allowed, f'questoes[{record["id"]}].criterios[{criterion["id"]}].evidencias')
            record['questao'] = self.enrich(record['questao'], {record['id']: record['alvo']})
        except (ValueError, KeyError, TypeError, AttributeError) as exc:
            record['decisao'] = 'corrigir_contrato'
            self.error(record, 'autoria', exc)

    def deduplicate(self):
        seen = {key(q['pergunta']) for q in self.inventory}
        seen.update(key(r['questao']['pergunta']) for r in self.data['records'] if r['decisao'] == 'admitir')
        for record in self.data['records']:
            if record['decisao'] != 'pendente_resolucao': continue
            value = key(record['questao']['pergunta'])
            if value in seen:
                record.update(decisao='descartar', motivo='Duplicata exata normalizada')
            else: seen.add(value)
        self.save()

    async def request(self, role, tag, payload, system):
        # Erros de uma linha nunca chegam ao retry global de transporte.
        return await self.calls.call(role, tag, payload, C.envelope, system=system)

    async def stage(self, records, field, role, tag, build, validate, accept, system, after_valid=None):
        """Duas leituras no máximo: a segunda contém apenas IDs ainda inválidos."""
        waiting = list(records)
        for attempt in range(2):
            if not waiting: break
            # Contadores persistidos impedem reabrir a etapa de irmãos concluídos.
            exhausted = [r for r in waiting if r.setdefault('tentativas_validacao', {}).get(field, 0) >= 2]
            for record in exhausted:
                record.update(decisao='invalida_contrato', motivo='Contrato individual não reparado em ' + field)
            waiting = [r for r in waiting if r not in exhausted]
            if not waiting: break
            payload = build(waiting)
            if attempt or any(r['tentativas_validacao'].get(field, 0) for r in waiting):
                payload.update(reparar_ids=[r['id'] for r in waiting],
                    erros_por_candidata={r['id']: r.get('erros_validacao', [])[-3:] for r in waiting},
                    instrucao='Retorne somente os IDs solicitados. Preserve as outras candidatas já processadas.')
            if len(waiting) > 1 and not self.fits(payload, system):
                middle = len(waiting) // 2
                await self.stage(waiting[:middle], field, role, tag + '_a', build, validate, accept, system, after_valid)
                await self.stage(waiting[middle:], field, role, tag + '_b', build, validate, accept, system, after_valid)
                return
            result = await self.request(role, tag + ('_contrato' if 'reparar_ids' in payload else ''), payload, system)
            mapping, errors = indexed(result, field)
            self.data['erros_entrada'].extend(dict(etapa=field, **e) for e in errors)
            allowed = {r['id'] for r in waiting}
            for unknown in set(mapping) - allowed:
                self.data['erros_entrada'].append(dict(etapa=field, id=unknown, erro='ID não solicitado'))
            failed = []
            for record in waiting:
                record['tentativas_validacao'][field] = record['tentativas_validacao'].get(field, 0) + 1
                value = mapping.get(record['id'])
                try:
                    C.require(isinstance(value, dict), field + '[' + record['id'] + ']: resposta ausente ou ID duplicado')
                    value = resolve_evidence(value, self.blocks)
                    validate(value, record)
                except (ValueError, KeyError, TypeError, AttributeError, IndexError) as exc:
                    self.error(record, field, exc)
                    record.setdefault('respostas_invalidas', {})[field] = value
                    failed.append(record)
                else:
                    accept(value, record)
                # Uma interrupção no próximo ID não apaga este resultado.
                self.save()
            if after_valid:
                await after_valid()
            waiting = failed
        for record in waiting:
            record.update(decisao='invalida_contrato', motivo='Contrato individual não reparado em ' + field)
        self.save()

    async def review(self, tag):
        pending = [r for r in self.data['records'] if r['decisao'] == 'pendente_resolucao']
        if pending:
            def solve_payload(records):
                return dict(questoes=[dict(id=r['id'], pergunta=r['questao']['pergunta']) for r in records],
                    contexto=source_with_passages(self.source),
                    contextos_por_alvo={r['id']: [b['id'] for b in self.context(r)] for r in records})
            def validate_solution(value, record):
                C.require(C.text(value.get('resposta')), 'resolucoes[' + record['id'] + '].resposta: resposta independente obrigatória')
                C.strings(value.get('ambiguidades'), 'resolucoes[' + record['id'] + '].ambiguidades')
            def solved(value, record):
                record.update(resolucao=value, decisao='pendente_revisao')
            # Primeiro avalia os irmãos já resolvidos; a recuperação dos demais vem depois.
            await self.stage(pending, 'resolucoes', 'solve', tag, solve_payload, validate_solution, solved, P.SOLVE,
                             after_valid=lambda: self.judge_ready(tag))
        await self.judge_ready(tag)

    async def judge_ready(self, tag):
        pending = [r for r in self.data['records'] if r['decisao'] == 'pendente_revisao']
        if not pending: return
        previous = list(self.inventory) + [r['questao'] for r in self.data['records'] if r['decisao'] == 'admitir']
        neighbors = {}
        for record in pending:
            if self.similarity is None:
                matches = [dict(q, similaridade=None) for q in previous]
            else:
                matches = self.similarity.nearest(record['questao']['pergunta'], previous, self.config.get('neighbors', 5))
            record['vizinhos'] = [dict(id=q['id'], similaridade=q.get('similaridade')) for q in matches]
            neighbors.update((q['id'], q) for q in matches)
        admitted = set(neighbors)
        def judge_payload(records):
            return dict(candidatas=[self.compact(r['questao']) for r in records],
                alvos=[r['alvo'] for r in records], contexto=source_with_passages(self.source),
                contextos_por_alvo={r['id']: [b['id'] for b in self.context(r)] for r in records},
                resolucoes=[r['resolucao'] for r in records],
                inventario_admitido=[{k: q[k] for k in ('id', 'pergunta', 'resposta', 'conhecimento', 'tipo', 'composicao') if k in q}
                                     for q in neighbors.values()])
        def validate_judgment(value, record):
            allowed = {b['id']: b for b in self.context(record)}
            C.judgment(value, record['questao'], allowed, admitted)
        def judged(value, record):
            record.update(parecer=value, decisao=value['decisao'])
            if value['decisao'] == 'admitir':
                admitted.add(record['id'])
                neighbors[record['id']] = record['questao']
            if value['decisao'] == 'corrigir' and record.get('refinado'):
                record['decisao'] = 'refino_esgotado'
        await self.stage(pending, 'avaliacoes', 'judge', tag, judge_payload, validate_judgment, judged, F.AUDIT)

    async def contract_repair(self, tag, prefix, records=None):
        broken = records if records is not None else [r for r in self.data['records'] if r['decisao'] == 'corrigir_contrato']
        exhausted = [r for r in broken if r.get('reparo_autoria')]
        for record in exhausted:
            record.update(decisao='invalida_contrato', motivo='Reparo individual de autoria esgotado')
        broken = [r for r in broken if not r.get('reparo_autoria')]
        if not broken: return
        ids = [r['id'] for r in broken]
        frozen_targets = {}
        for record in broken:
            try:
                C.require(isinstance(record['alvo'], dict), 'Alvo inválido')
                frozen = resolve_evidence(record['alvo'], self.blocks)
                C.target(frozen, self.blocks)
                frozen_targets[record['id']] = frozen
            except (ValueError, KeyError, TypeError, AttributeError):
                pass
        payload = dict(corrigir=[dict(id=r['id'], alvo=r['alvo'],
            questao=self.compact(r['questao']) if isinstance(r['questao'], dict) else r['questao'], erros=r['erros_validacao']) for r in broken],
            alvos=[r['alvo'] for r in broken if isinstance(r['alvo'], dict)],
            contextos_por_alvo={r['id']: self.context(r) for r in broken if isinstance(r['alvo'], dict)},
            contexto=source_with_passages(self.source), limite=len(broken), ids_para_reparar=ids,
            alvos_congelados=list(frozen_targets),
            instrucao='Retorne alvo e questão completos apenas para estes IDs. Não altere outras candidatas.')
        if len(broken) > 1 and not self.fits(payload, F.REPAIR):
            middle = len(broken) // 2
            await self.contract_repair(tag + '_a', prefix, broken[:middle])
            await self.contract_repair(tag + '_b', prefix, broken[middle:])
            return
        result = await self.request('refine', tag + '_contrato_autoria', payload, F.REPAIR)
        fixed, errors, pending = partition(result, self.blocks, prefix=prefix, expected=ids, limit=len(ids))
        self.data['erros_entrada'].extend(errors); self.data['impedimentos'].extend(pending)
        updates = {r['id']: r for r in fixed}
        for record in broken:
            replacement = updates[record['id']]
            record['reparo_autoria'] = True
            frozen = frozen_targets.get(record['id'])
            record.setdefault('historico', []).append(copy.deepcopy({k: v for k, v in record.items() if k != 'historico'}))
            changed = frozen is not None and (replacement['decisao'] != 'pendente_resolucao'
                or target_identity(replacement['alvo']) != target_identity(frozen))
            if replacement['decisao'] == 'pendente_resolucao' and not changed:
                record.update(alvo=replacement['alvo'], questao=replacement['questao'], decisao='pendente_resolucao')
                record['tentativas_validacao'] = {}
                self.enrich_record(record)
                self.data['alvos'][record['id']] = record['alvo']
                if record['decisao'] == 'corrigir_contrato':
                    record.update(decisao='invalida_contrato', motivo='Reparo individual ainda viola o contexto autorizado')
            else:
                record.update(decisao='invalida_contrato', motivo='Reparo individual de autoria insuficiente')
                record['erros_validacao'].extend(replacement['erros_validacao'])
                if changed and replacement['decisao'] == 'pendente_resolucao':
                    self.error(record, 'reparo_autoria', 'Alvo válido não pode ser alterado para contornar erro da questão')
            self.save()

    async def content_repair(self, tag, records=None):
        broken = records if records is not None else [r for r in self.data['records'] if r['decisao'] == 'corrigir' and not r.get('refinado')]
        if not broken: return
        targets = {r['id']: r['alvo'] for r in broken}
        payload = dict(alvos=list(targets.values()), contexto=source_with_passages(self.source),
            contextos_por_alvo={r['id']: self.context(r) for r in broken},
            corrigir=[dict(id=r['id'], questao=self.compact(r['questao']), parecer=r['parecer'], resolucao=r['resolucao'])
                      for r in broken], limite=len(broken))
        if len(broken) > 1 and not self.fits(payload, P.AUTHOR):
            middle = len(broken) // 2
            await self.content_repair(tag + '_a', broken[:middle])
            await self.content_repair(tag + '_b', broken[middle:])
            return
        result = await self.request('refine', tag + '_refino', payload, P.AUTHOR)
        fixed, errors, pending = partition(result, self.blocks, expected=list(targets), targets=targets, limit=len(targets))
        self.data['erros_entrada'].extend(errors); self.data['impedimentos'].extend(pending)
        for original, replacement in zip(broken, fixed):
            original.setdefault('historico', []).append(copy.deepcopy({k: v for k, v in original.items() if k != 'historico'}))
            original['refinado'] = True
            if replacement['decisao'] == 'pendente_resolucao':
                original.update(questao=replacement['questao'], decisao='pendente_resolucao', tentativas_validacao={})
                self.enrich_record(original)
            else:
                original.update(decisao='corrigir_contrato', motivo='Refino inválido')
                original['erros_validacao'].extend(replacement['erros_validacao'])
            self.save()

    async def process(self, payload, tag, *, prefix='', targets=None, system=None):
        if not self.data.get('gerado', bool(self.data['records'])):
            result = await self.request('author', tag, payload, system or F.GENERATE)
            records, errors, pending = partition(result, self.blocks, prefix=prefix, targets=targets,
                expected=list(targets) if targets is not None else None, limit=self.config['batch_size'])
            for record in records:
                if record['decisao'] == 'pendente_resolucao': self.enrich_record(record)
            self.data.update(records=records, alvos={r['id']: r['alvo'] for r in records if isinstance(r['alvo'], dict)},
                             erros_entrada=errors, impedimentos=pending, gerado=True)
            self.save()
        # Compatibilidade de leitura com checkpoints anteriores, nunca aprova sem parecer.
        for record in self.data['records']:
            record.setdefault('alvo', self.data['alvos'].get(record['id']))
        self.deduplicate()
        await self.review(tag)
        await self.contract_repair(tag, prefix)
        self.deduplicate()
        await self.review(tag + '_autoria_reparada')
        await self.content_repair(tag)
        await self.contract_repair(tag + '_refino', prefix)
        self.deduplicate()
        await self.review(tag + '_reparo')
        self.data['concluida'] = True
        self.save()
        return self.data
