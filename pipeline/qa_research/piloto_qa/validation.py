"""Particionamento de respostas e evidências exatas, sem reprovar irmãos válidos."""
import copy
import re
from collections import Counter

from . import contracts as C


def question_key(text):
    return ' '.join(re.findall(r'\w+', text.casefold()))


def target_identity(target):
    """Compara o contrato do alvo, independente da representação da referência."""
    return dict({k: target[k] for k in ('id', 'tipo', 'composicao', 'conhecimento', 'ponte')},
        afirmacoes=[dict(afirmacao=a['afirmacao'], evidencias=[dict(bloco=e['bloco'], trecho=e['trecho'])
            for e in a['evidencias']]) for a in target['afirmacoes']])


def source_with_passages(blocks):
    result = []
    for block in blocks:
        passages = []
        # Intervalos sempre se referem ao texto original, sem normalizar ou resumir.
        for match in re.finditer(r'\S.*?(?=\n\s*\n|\Z)', block['texto'], re.S):
            start = match.start()
            end = start + len(match.group().rstrip())
            passages.append(dict(id=f'{block["id"]}_P{len(passages)+1:03}',
                bloco=block['id'], inicio=start, fim=end, texto=block['texto'][start:end]))
        result.append(dict(block, passagens=passages))
    return result


def resolve_evidence(value, blocks):
    """Expande IDs fornecidos em passagens literais. Nunca faz busca aproximada."""
    passages = {p['id']: p for b in source_with_passages(list(blocks.values())) for p in b['passagens']}
    result = copy.deepcopy(value)

    def walk(node, path):
        if isinstance(node, list):
            for i, child in enumerate(node): walk(child, f'{path}[{i}]')
        elif isinstance(node, dict):
            for key, child in node.items():
                if key != 'evidencias':
                    walk(child, path + '.' + key)
                    continue
                if not isinstance(child, list):
                    continue  # O contrato individual identifica o campo inválido.
                for index, evidence in enumerate(child):
                    if not isinstance(evidence, dict) or 'passagem' not in evidence:
                        continue
                    where = f'{path}.evidencias[{index}]'
                    pid = evidence['passagem']
                    C.require(isinstance(pid, str) and pid in passages, where + ': passagem desconhecida ' + repr(pid))
                    passage = passages[pid]
                    C.require(evidence.get('bloco', passage['bloco']) == passage['bloco'], where + ': bloco contradiz passagem')
                    # Uma citação opcional também precisa ser literal NA passagem indicada.
                    snippet = evidence.get('trecho', passage['texto'])
                    C.require(C.text(snippet) and snippet in passage['texto'], where + ': trecho contradiz passagem literal')
                    evidence.update(bloco=passage['bloco'], trecho=snippet)
    walk(result, str(result.get('id', 'item')) if isinstance(result, dict) else 'item')
    return result


def indexed(data, field):
    """IDs duplicados são ambíguos; nenhuma versão é escolhida silenciosamente."""
    rows = data.get(field)
    if not isinstance(rows, list):
        return {}, [dict(campo=field, erro='Esperado array', recebido=rows)]
    counts = Counter(r['id'] for r in rows if isinstance(r, dict) and isinstance(r.get('id'), str))
    result, errors = {}, []
    for index, row in enumerate(rows):
        qid = row.get('id') if isinstance(row, dict) else None
        if not isinstance(qid, str) or not re.fullmatch(r'[A-Za-z0-9_-]{1,64}', qid):
            errors.append(dict(campo=f'{field}[{index}]', erro='ID ausente ou inválido', recebido=row))
        elif counts[qid] != 1:
            errors.append(dict(id=qid, campo=f'{field}[{index}]', erro='ID duplicado', recebido=row))
            result[qid] = None
        else:
            result[qid] = row
    return result, errors


def validate_pair(target, question, blocks):
    errors, normalized = [], {}
    # Avalia os dois componentes mesmo se o primeiro tiver defeito: o reparo
    # recebe, por exemplo, a ponte ausente E a evidência inválida de uma vez.
    for name, value in (('alvo', target), ('questao', question)):
        try:
            C.require(isinstance(value, dict), name + ' ausente, inválido ou duplicado')
            C.rows([value], name)
            normalized[name] = resolve_evidence(value, blocks)
        except (ValueError, KeyError, TypeError, AttributeError, IndexError) as exc:
            errors.append(str(exc))
    if 'alvo' in normalized:
        try: C.target(normalized['alvo'], blocks)
        except (ValueError, KeyError, TypeError, AttributeError, IndexError) as exc: errors.append(str(exc))
    if 'questao' in normalized:
        try:
            C.question(normalized['questao'], target if isinstance(target, dict) and 'tipo' in target else {'tipo': None}, blocks)
        except (ValueError, KeyError, TypeError, AttributeError, IndexError) as exc: errors.append(str(exc))
    if not errors:
        C.require(normalized['alvo']['id'] == normalized['questao']['id'], 'IDs de alvo e questão devem coincidir')
    C.require(not errors, '; '.join(errors))
    return normalized['alvo'], normalized['questao']


def partition(data, blocks, *, prefix='', expected=None, targets=None, limit=4):
    """Retorna cada candidata válida ou inválida; excedentes não invalidam as demais."""
    given_targets, errors = indexed(data, 'alvos') if targets is None else (targets, [])
    questions, other_errors = indexed(data, 'questoes')
    errors += other_errors
    ids = list(dict.fromkeys(list(given_targets) + list(questions))) if expected is None else list(expected)
    records = []
    for index, qid in enumerate(ids):
        target, question = given_targets.get(qid), questions.get(qid)
        record = dict(id=qid, alvo=target, questao=question, decisao='pendente_resolucao', erros_validacao=[])
        try:
            C.require(not prefix or qid.startswith(prefix), qid + ': prefixo de ID incorreto')
            C.require(index < limit, qid + ': excedente do limite de candidatas solicitado')
            target, question = validate_pair(target, question, blocks)
        except (ValueError, KeyError, TypeError, AttributeError, IndexError) as exc:
            record.update(decisao='corrigir_contrato' if index < limit and (not prefix or qid.startswith(prefix)) else 'invalida_contrato',
                          erros_validacao=[dict(etapa='autoria', erro=str(exc))])
        else:
            record.update(alvo=target, questao=question)
        records.append(record)
    for index, issue in enumerate(other_errors):
        if 'id' in issue or not issue['campo'].startswith('questoes['): continue
        # Identidade interna só para auditar a linha malformada, nunca para admitir.
        qid = f'{prefix}INVALID_{index+1:03}'
        while qid in ids: qid += '_'
        records.append(dict(id=qid, alvo=None, questao=issue.get('recebido'), decisao='invalida_contrato',
                            erros_validacao=[dict(etapa='autoria', erro=issue['campo'] + ': ' + issue['erro'])]))
    extras = set(questions) - set(ids)
    errors.extend(dict(id=qid, campo='questoes', erro='ID não solicitado no reparo') for qid in sorted(extras))
    pending = data.get('impedimentos', [])
    if not isinstance(pending, list) or not all(C.text(s) for s in pending):
        errors.append(dict(campo='impedimentos', erro='Esperado array de strings não vazias', recebido=pending))
        pending = []
    return records, errors, pending
