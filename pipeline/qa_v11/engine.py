"""Preparação e avaliação v11, com limites de busca e histórico de cada decisão."""
import copy
import json
from pathlib import Path

from pipeline.inventario.textutil import atomic_json, read_json, sha
from . import contracts as C, prompts as P


def dumps(value):
    return json.dumps(value, ensure_ascii=False, sort_keys=True)


class Engine:
    def __init__(self, writer, judge, blind, novelty, index, examples, complement=True, input_mode='nota'):
        self.writer, self.judge, self.blind, self.novelty = writer, judge, blind, novelty
        self.index, self.examples = index, examples
        self.complement, self.input_mode = complement, input_mode

    def call(self, client, prompt, payload, tag, item, validate, tokens=9000):
        def schema_check(data):
            try:
                validate(data)
            except (TypeError, KeyError, AttributeError, IndexError) as exc:
                raise ValueError(f'estrutura JSON incompatível: {type(exc).__name__}; revise os campos pedidos') from exc
        return client.json(prompt, dumps(payload), tag=tag, item=item, validate=schema_check, max_tokens=tokens)

    def extract(self, evidences, context, offset, item):
        def validate(d):
            C.extract_claims(d, evidences, offset)
        data = self.call(self.writer, P.EXTRAIR, {'objetivo_explorado': context, 'evidencias': evidences},
                         'v11_extracao', item, validate)
        return C.extract_claims(data, evidences, offset)

    def verify(self, claims, evidences, context, item):
        def validate(d):
            result, _ = C.verify(d, claims, evidences)
            for before, after in zip(claims, result):
                if C.eligible(before) and not C.eligible(after):
                    conflict = after['verificacao']['adequacao_tecnica'] == 'conflitante' or (
                        after['verificacao']['fidelidade'] == 'contradita')
                    if not (conflict and after['suporte']):
                        raise ValueError('não perca afirmação já verificada sem evidência explícita de conflito')
        data = self.call(self.judge, P.VERIFICAR,
                         {'objetivo': context, 'afirmacoes': claims, 'evidencias': evidences},
                         'v11_verificacao', item, validate, tokens=14000)
        return C.verify(data, claims, evidences)

    def retrieve_gaps(self, gaps, evidences, context, item):
        known = {e['chunk_id'] for e in evidences} | {e['texto_sha256'] for e in evidences}
        candidate_map = {}
        for gap in gaps[:3]:
            query = gap.get('consulta_pt', '') + ' ' + gap.get('consulta_en', '')
            if not query.strip():
                continue
            for c in self.index.search(query, limit=4, exclude=known):
                candidate_map.setdefault(c['chunk_id'], c)
        last_eid = max((int(e['id'][1:]) for e in evidences), default=0)
        candidates = [C.evidence(c, f'E{last_eid + i}')
                      for i, c in enumerate(list(candidate_map.values())[:8], 1)]
        if not candidates:
            return [], {'lacunas': gaps, 'candidatos': [], 'motivo': 'busca sem material novo no acervo disponível'}
        def validate(d):
            rows = C.exact_rows(d.get('trechos'), [e['id'] for e in candidates])
            for r in rows.values():
                if r.get('classe') not in ('resolve', 'parcial', 'relacionado', 'conflita', 'irrelevante'):
                    raise ValueError('classe de complemento inválida')
                C.text(r.get('razao'), 'razao')
        data = self.call(self.judge, P.COMPLEMENTO,
                         {'objetivo': context, 'lacunas': gaps, 'candidatas': candidates},
                         'v11_complemento', item, validate)
        classes = {r['id']: r for r in data['trechos']}
        kept = [e for e in candidates if classes[e['id']]['classe'] in ('resolve', 'parcial', 'conflita')]
        return kept, {'lacunas': gaps, 'candidatos': candidates, 'avaliacao': data,
                      'incluidos': [e['id'] for e in kept]}

    def enrich(self, pack, gaps, item):
        """Acrescenta evidências; nunca substitui o texto original nem a proposição existente."""
        new, trace = self.retrieve_gaps(gaps, pack['evidencias'], pack['contexto'], item)
        updated = copy.deepcopy(pack)
        updated.setdefault('complementos', []).append(trace)
        if not new:
            return updated
        evidence = pack['evidencias'] + new
        # IDs não precisam ser contíguos; a sequência máxima evita colisão após quarentena.
        offset = max((int(a['id'][1:]) for a in pack['afirmacoes']), default=0)
        fresh = self.extract(new, pack['contexto'], offset, item + ':extrair')
        known = {sha(a['proposicao'], 40) for a in pack['afirmacoes']}
        fresh = [a for a in fresh if sha(a['proposicao'], 40) not in known]
        claims = pack['afirmacoes'] + fresh
        if claims:
            verified, remaining = self.verify(claims, evidence, pack['contexto'], item + ':verificar')
        else:
            verified, remaining = [], gaps
        updated['historico_afirmacoes'] = pack.get('historico_afirmacoes', []) + [copy.deepcopy(pack['afirmacoes'])]
        updated.update(evidencias=evidence, afirmacoes=verified, lacunas=remaining)
        return updated

    def draft_note(self, pack, item):
        def validate(d):
            C.validate_note(d, pack['afirmacoes'])
        note = self.call(self.writer, P.NOTA,
                         {'contexto': pack['contexto'], 'afirmacoes': pack['afirmacoes'], 'lacunas': pack['lacunas']},
                         'v11_nota', item, validate, tokens=11000)
        return note

    def review(self, pack, note, item):
        def validate(d):
            C.review_note(d, note, pack['afirmacoes'])
        data = self.call(self.judge, P.REVISAR_NOTA,
                         {'contexto': pack['contexto'], 'nota': note,
                          'afirmacoes': pack['afirmacoes'], 'evidencias': pack['evidencias']},
                         'v11_revisao_nota', item, validate, tokens=9000)
        return C.review_note(data, note, pack['afirmacoes'])

    def prepare(self, topic, unit, directory):
        path = Path(directory) / (sha(unit['id'], 24) + '.json')
        stored = read_json(path)
        if stored and stored.get('concluida'):
            return stored
        context = {'topico': topic['topico'], 'subtopico': topic['subtopico'],
                   'conceito': unit['conceito'], 'foco': unit['foco'], 'assunto': unit['assunto']}
        if stored:
            pack = stored
        else:
            a = unit['assunto']
            query = ' '.join([unit['conceito'], unit['foco'], a.get('consulta_pt', ''), a.get('consulta_en', '')])
            chunks = self.index.search(query, limit=8)
            evidences = [C.evidence(c, f'E{i}') for i, c in enumerate(chunks, 1)]
            pack = {'id': unit['id'], 'contexto': context, 'evidencias': evidences,
                    'afirmacoes': [], 'lacunas': [], 'etapa': 'fontes', 'concluida': False}
            atomic_json(path, pack)
        if pack['etapa'] == 'fontes':
            extracted = self.extract(pack['evidencias'], context, 0, unit['id']) if pack['evidencias'] else []
            pack.update(afirmacoes=extracted, etapa='extraidas')
            atomic_json(path, pack)
        if pack['etapa'] == 'extraidas':
            if pack['afirmacoes']:
                claims, gaps = self.verify(pack['afirmacoes'], pack['evidencias'], context, unit['id'])
                pack.update(afirmacoes=claims, lacunas=gaps)
            pack['etapa'] = 'verificadas'
            atomic_json(path, pack)
        if pack['etapa'] == 'verificadas':
            if self.complement and pack['lacunas']:
                pack = self.enrich(pack, pack['lacunas'], unit['id'] + ':lacunas')
            pack['etapa'] = 'complementadas'
            atomic_json(path, pack)
        if pack['etapa'] == 'complementadas':
            if any(C.eligible(a) for a in pack['afirmacoes']):
                note = self.draft_note(pack, unit['id'])
                pack['nota_rascunho'] = note
            else:
                pack['nota_rascunho'] = {'titulo': unit['conceito'], 'blocos': [], 'objetivos': [],
                                         'propostas_novas': [], 'lacunas': [], 'motivo': 'sem afirmações avaliáveis'}
            pack['etapa'] = 'redigida'
            atomic_json(path, pack)
        if pack['etapa'] == 'redigida':
            note = pack['nota_rascunho']
            proposals = note['propostas_novas'][:3]
            # Propostas paramétricas só são promovidas com a mesma verificação e prova original.
            if self.complement and proposals:
                offset = max((int(a['id'][1:]) for a in pack['afirmacoes']), default=0)
                additions = [{'id': f'A{offset + i}', 'proposicao': p['proposicao'], 'objeto': p['objeto'],
                              'estatuto_na_fonte': 'inferencia_proposta', 'origem': 'parametrica_proposta',
                              'condicoes': [], 'limites': [], 'suporte': [], 'premissas': p.get('premissas', [])}
                             for i, p in enumerate(proposals, 1)]
                original_ids = {a['id'] for a in pack['afirmacoes']}
                pack['afirmacoes'] += additions
                gaps = [{'afirmacoes': [a['id']], 'lacuna': a['proposicao'],
                         'consulta_pt': p['consulta_pt'], 'consulta_en': p['consulta_en'],
                         'criterio_resolucao': 'sustentar a nova explicação técnica e suas condições'}
                        for a, p in zip(additions, proposals)]
                pack = self.enrich(pack, gaps, unit['id'] + ':propostas')
                # A proposta pode estar sustentada nas evidências que já existiam, mesmo sem novo retorno.
                if any('verificacao' not in a for a in pack['afirmacoes']):
                    claims, gaps = self.verify(pack['afirmacoes'], pack['evidencias'], context, unit['id'] + ':propostas_existentes')
                    pack.update(afirmacoes=claims, lacunas=gaps)
                promoted = [a for a in pack['afirmacoes'] if a['id'] not in original_ids and C.eligible(a)]
                if promoted:
                    # A versão anterior permanece registrada; a nova será revisada inteira.
                    note = self.draft_note(pack, unit['id'] + ':elaborada')
            pack['nota_antes_revisao'] = note
            pack['etapa'] = 'elaborada'
            atomic_json(path, pack)
        if pack['etapa'] == 'elaborada':
            note = pack['nota_antes_revisao']
            pack['nota'] = self.review(pack, note, unit['id']) if note['objetivos'] or note['blocos'] else note
            for i, objective in enumerate(pack['nota']['objetivos'], 1):
                objective['id'] = f"{unit['id']}:O{i}"
            pack.update(etapa='concluida', concluida=True)
            atomic_json(path, pack)
        return pack

    def material(self, pack, objective):
        result = {'contexto': pack['contexto'], 'objetivo': objective,
                  'afirmacoes': pack['afirmacoes'], 'evidencias': pack['evidencias']}
        if self.input_mode == 'nota':
            result['nota_pedagogica'] = pack['nota']['blocos']
        return result

    def judge_item(self, pack, objective, question, item):
        def validate_nucleus(d):
            C.text(d.get('resposta_nucleo'), 'resposta_nucleo')
            C.texts(d.get('condicoes_faltantes'), 'condicoes_faltantes')
            if not isinstance(d.get('suporte'), list):
                raise ValueError('suporte deve ser lista')
            for row in d['suporte']:
                C.text(row.get('afirmacao'), 'afirmacao')
                C.references(row.get('afirmacoes'), {a['id'] for a in pack['afirmacoes'] if C.eligible(a)},
                             'suporte independente', required=False)
        nucleus = self.call(self.judge, P.NUCLEO,
                            {'material': self.material(pack, objective), 'pergunta': question['pergunta']},
                            'v11_nucleo_sem_gabarito', item, validate_nucleus, tokens=6000)
        data = self.call(self.judge, P.JUIZ,
                         {'material': self.material(pack, objective), 'item': question,
                          'resolucao_sem_gabarito': nucleus,
                          'calibracao_defeitos': self.examples.anchors()},
                         'v11_juiz', item, lambda d: C.validate_judgment(d, pack['afirmacoes']), tokens=11000)
        return {**data, 'resolucao_sem_gabarito': nucleus}

    def generate_item(self, pack, objective, previous, qid):
        chosen = self.examples.choose(objective, pack['contexto']['topico'])
        covered = [{'id': q['id'], 'objetivo': q['objetivo'], 'rubrica': q['rubrica']}
                   for q in previous if q['status'] == 'aprovada']
        question = self.call(self.writer, P.GERAR,
                             {'material': self.material(pack, objective), 'exemplos': chosen,
                              'competencias_ja_cobertas': covered},
                             'v11_geracao', qid,
                             lambda d: C.validate_question(d, pack['afirmacoes'], objective), tokens=9000)
        question = C.question_payload(question)
        record = {'id': qid, 'objetivo_id': objective['id'], 'objetivo': copy.deepcopy(objective),
                  'unidade': pack['id'], 'exemplos': {k: [e['id'] for e in v] for k, v in chosen.items()},
                  'versoes': [], 'validacao_humana': 'pendente'}
        def checkpoint(stage, final=False):
            directory = getattr(self, 'checkpoint_dir', None)
            if directory is not None:
                snapshot = {**record, **C.question_payload(question), 'etapa': stage,
                            'evidencias': active_pack['evidencias'], 'afirmacoes_verificadas': active_pack['afirmacoes']}
                snapshot['status'] = record.get('status') if final else 'pendente_validacao'
                atomic_json(Path(directory) / (sha(qid, 32) + '.json'), snapshot)
        active_pack = copy.deepcopy(pack)
        if question['status'] != 'ok':
            record.update(status='evidencia_insuficiente', motivo=question['motivo'])
            checkpoint('geracao_insuficiente', final=True)
            return record
        checkpoint('gerada')
        last_feedback = None
        retrieval_used = False
        # Até duas revisões: redação/gabarito ou ambiguidade. Cada versão é julgada novamente.
        for version in range(3):
            issues = C.presentation_issues(question)
            judgment = self.judge_item(active_pack, objective, question, qid + f':v{version}')
            trace = {'versao': version, 'questao': copy.deepcopy(question),
                     'apresentacao': issues, 'juiz': judgment}
            record['versoes'].append(trace)
            checkpoint('julgada')
            passed = C.approved(judgment) and not issues
            last_feedback = {'juiz': judgment, 'apresentacao': issues}
            if passed:
                def validate_blind(d):
                    C.text(d.get('resposta'), 'resposta cega')
                    C.texts(d.get('condicoes_faltantes'), 'condicoes_faltantes')
                    C.texts(d.get('interpretacoes'), 'interpretacoes')
                independent = self.call(self.blind, P.CEGO, {'pergunta': question['pergunta']},
                                        'v11_cego', qid + f':v{version}', validate_blind, tokens=4000)
                trace['cego'] = independent
                checkpoint('respondida_as_cegas')
                values = ('equivalentes', 'parcial_sem_contradicao', 'erro_respondente',
                          'ambiguidade_item', 'erro_referencia', 'indeterminado')
                def validate_compare(d):
                    if d.get('veredito') not in values:
                        raise ValueError('veredito de adjudicação inválido')
                    C.text(d.get('razao'), 'razao')
                    C.references(d.get('afirmacoes'), {a['id'] for a in active_pack['afirmacoes'] if C.eligible(a)},
                                 'afirmacoes da adjudicação', required=d['veredito'] != 'indeterminado')
                comparison = self.call(self.judge, P.ADJUDICAR,
                                       {'material': self.material(active_pack, objective),
                                        'item': question, 'resposta_independente': independent},
                                       'v11_adjudicacao', qid + f':v{version}', validate_compare, tokens=6000)
                trace.update(cego=independent, adjudicacao=comparison)
                checkpoint('adjudicada')
                if comparison['veredito'] in ('equivalentes', 'parcial_sem_contradicao', 'erro_respondente'):
                    record.update(question, status='aprovada')
                    break
                if comparison['veredito'] == 'indeterminado':
                    record.update(question, status='pendente_validacao', motivo=comparison['razao'])
                    break
                last_feedback['cego'] = comparison
            elif judgment['acao'] in ('rejeitar', 'recuperar_evidencia') and not issues:
                if judgment['acao'] == 'recuperar_evidencia' and self.complement and not retrieval_used:
                    gap = {'afirmacoes': [], 'lacuna': judgment['motivo'],
                           'consulta_pt': objective['descricao'] + ' ' + judgment['motivo'],
                           'consulta_en': question['pergunta'], 'criterio_resolucao': judgment['motivo']}
                    active_pack = self.enrich(active_pack, [gap], qid + ':evidencia')
                    retrieval_used = True
                    trace['busca_evidencia'] = active_pack['complementos'][-1]
                else:
                    record.update(question, status='evidencia_insuficiente' if judgment['acao'] == 'recuperar_evidencia'
                                  else 'reprovada', motivo=judgment['motivo'])
                    break
            if version == 2:
                record.update(question, status='reprovada', motivo='limite de revisões; consulte parecer por dimensão')
                break
            revised = self.call(self.writer, P.REFINAR,
                                {'material': self.material(active_pack, objective), 'item': question,
                                 'parecer': last_feedback}, 'v11_refino', qid + f':v{version}',
                                lambda d: C.validate_question(d, active_pack['afirmacoes'], objective), tokens=9000)
            if revised['status'] == 'necessita_evidencia' and self.complement and not retrieval_used:
                before_count = len(active_pack['evidencias'])
                gap = {'afirmacoes': [], 'lacuna': revised.get('lacuna') or revised['motivo'],
                       'consulta_pt': revised.get('consulta_pt') or objective['descricao'] + ' ' + revised['motivo'],
                       'consulta_en': revised.get('consulta_en') or question['pergunta'],
                       'criterio_resolucao': revised['motivo']}
                active_pack = self.enrich(active_pack, [gap], qid + ':evidencia_refino')
                retrieval_used = True
                trace['busca_solicitada_refinador'] = active_pack['complementos'][-1]
                if len(active_pack['evidencias']) > before_count:
                    revised = self.call(self.writer, P.REFINAR,
                                        {'material': self.material(active_pack, objective), 'item': question,
                                         'parecer': last_feedback, 'lacuna_investigada': gap},
                                        'v11_refino', qid + f':v{version}:com_evidencia',
                                        lambda d: C.validate_question(d, active_pack['afirmacoes'], objective), tokens=9000)
            if revised['status'] != 'ok':
                record.update(question, status='evidencia_insuficiente' if revised['status'] == 'necessita_evidencia'
                              else 'reprovada', motivo=revised['motivo'])
                break
            question = C.question_payload(revised)
            checkpoint('refinada')
        record['evidencias'] = active_pack['evidencias']
        record['afirmacoes_verificadas'] = active_pack['afirmacoes']
        if record['status'] == 'aprovada':
            accepted = [q for q in previous if q['status'] == 'aprovada']
            if accepted:
                ids = [q['id'] for q in accepted]
                def validate_novelty(d):
                    rows = C.exact_rows(d.get('pares'), ids)
                    for r in rows.values():
                        if r.get('classe') not in ('redundante', 'sobreposicao', 'distinta'):
                            raise ValueError('classe de novidade inválida')
                        C.text(r.get('razao'), 'razao')
                def brief(q):
                    return {k: q[k] for k in ('id', 'pergunta', 'resposta', 'rubrica', 'objetivo')}
                novelty = self.call(self.novelty, P.NOVIDADE,
                                    {'nova': brief(record), 'anteriores': [brief(q) for q in accepted]},
                                    'v11_novidade', qid, validate_novelty, tokens=6000)
                record['novidade'] = novelty
                if any(p['classe'] == 'redundante' for p in novelty['pares']):
                    record.update(status='redundante', motivo='mesma competência essencial de item anterior')
            else:
                record['novidade'] = {'pares': [], 'motivo': 'primeiro item do subtópico'}
        checkpoint('concluida', final=True)
        return record
