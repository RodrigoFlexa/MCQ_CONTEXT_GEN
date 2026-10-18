"""Contratos v11. IDs de evidência, hashes e versões pertencem ao código, não ao LLM."""
import copy
import re
import unicodedata

from pipeline.inventario.textutil import sha
from .prompts import DIMENSOES

ESTATUTOS = {'principio_apresentado', 'definicao', 'resultado_estudo', 'hipotese', 'opiniao',
             'evento_relatado', 'recomendacao', 'requisito', 'inferencia_proposta'}
QUESTION_FIELDS = {'status', 'pergunta', 'resposta', 'rubrica', 'respostas_aceitaveis', 'explicacao',
                   'premissas_cenario', 'suporte', 'dependencias', 'mudancas', 'motivo', 'lacuna',
                   'consulta_pt', 'consulta_en'}


def question_payload(data):
    """Metadados de execução não podem ser substituídos por campos inesperados do modelo."""
    return {k: copy.deepcopy(v) for k, v in data.items() if k in QUESTION_FIELDS}


def text(value, name):
    if not isinstance(value, str) or not value.strip():
        raise ValueError(f'{name}: texto não vazio obrigatório')
    return value.strip()


def texts(value, name):
    if not isinstance(value, list) or any(not isinstance(x, str) or not x.strip() for x in value):
        raise ValueError(f'{name}: lista de textos obrigatória')
    return list(dict.fromkeys(x.strip() for x in value))


def references(value, allowed, name, required=True):
    result = texts(value, name)
    if (required and not result) or any(r not in allowed for r in result):
        raise ValueError(f'{name}: use IDs existentes, sem omitir o suporte obrigatório')
    return result


def exact_rows(rows, expected, field='id'):
    if not isinstance(rows, list) or any(not isinstance(r, dict) for r in rows):
        raise ValueError('lista de avaliações obrigatória')
    ids = [r.get(field) for r in rows]
    if any(type(i) not in (str, int) for i in ids) or len(ids) != len(expected) or set(ids) != set(expected):
        raise ValueError(f'inclua exatamente uma avaliação por {field}; esperados: {list(expected)}')
    return {r[field]: r for r in rows}


def evidence(chunk, eid):
    body = chunk.get('texto', chunk.get('text', ''))
    text(body, 'texto original')
    issues = []
    if '<NUMBER>' in body:
        issues.append('numeros_mascarados')
    if 'unknown' in chunk.get('source_boundary', ''):
        issues.append('fronteira_documental_desconhecida')
    if chunk.get('page_ini') is None:
        issues.append('sem_paginacao_confiavel')
    if re.search(r'\b(?:figura|tabela|figure|table)\s+\d+', body, re.I):
        issues.append('referencia_visual_verificar_se_suporte_textual_basta')
    return {'id': eid, 'texto': body, 'texto_sha256': sha(body, 64),
            'chunk_id': chunk['chunk_id'], 'documento_id': chunk.get('document_id'),
            # Coleção agregadora não é família documental independente.
            'familia_documental': None if 'fronteira_documental_desconhecida' in issues else (
                chunk.get('original_document_id') or chunk.get('document_id')),
            'metadados': {k: chunk.get(k) for k in ('collection', 'title', 'url', 'language', 'jurisdiction',
                                                  'page_ini', 'page_fim', 'linha_ini', 'linha_fim', 'source_boundary')},
            'problemas_extracao': issues}


def support(rows, evidences, required=True):
    if not isinstance(rows, list) or (required and not rows):
        raise ValueError('suporte exige evidências com citação literal')
    known = {e['id']: e for e in evidences}
    out = []
    for row in rows:
        if not isinstance(row, dict) or row.get('evidencia_id') not in known:
            raise ValueError('evidência inexistente')
        quote = text(row.get('citacao'), 'citacao')
        def canonical(value):
            return re.sub(r'\s+', ' ', unicodedata.normalize('NFC', value).casefold()).strip()
        if canonical(quote) not in canonical(known[row['evidencia_id']]['texto']):
            raise ValueError('citação não contígua no original; preserve sinais, números e ressalvas')
        out.append({'evidencia_id': row['evidencia_id'], 'citacao': quote})
    return out


def extract_claims(data, evidences, offset=0):
    rows = data.get('afirmacoes')
    if not isinstance(rows, list) or len(rows) > 10:
        raise ValueError('afirmacoes: lista de até 10 objetos')
    if not rows:
        text(data.get('motivo'), 'motivo da ausência de afirmações')
    result = []
    for i, row in enumerate(rows, offset + 1):
        if row.get('estatuto_na_fonte') not in ESTATUTOS - {'inferencia_proposta'}:
            raise ValueError('estatuto_na_fonte inválido')
        result.append({'id': f'A{i}', 'proposicao': text(row.get('proposicao'), 'proposicao'),
                       'objeto': text(row.get('objeto'), 'objeto'), 'estatuto_na_fonte': row['estatuto_na_fonte'],
                       'condicoes': texts(row.get('condicoes'), 'condicoes'),
                       'limites': texts(row.get('limites'), 'limites'),
                       'suporte': support(row.get('suporte'), evidences), 'origem': 'extracao'})
    return result


def verify(data, claims, evidences):
    by_id = exact_rows(data.get('avaliacoes'), [a['id'] for a in claims])
    result = []
    for claim in claims:
        r = by_id[claim['id']]
        for name, values in {
            'fidelidade': ('sustentada', 'parcial', 'contradita', 'indeterminada'),
            'adequacao_tecnica': ('suficiente_no_escopo', 'conflitante', 'pendente'),
            'aplicabilidade': ('fpso', 'transferivel', 'restrita', 'fora'),
            'decisao_uso': ('avaliavel_no_escopo', 'apenas_contexto', 'investigar', 'excluir'),
        }.items():
            if r.get(name) not in values:
                raise ValueError(f'{name}: enum inválido')
        v = {k: r[k] for k in ('fidelidade', 'adequacao_tecnica', 'aplicabilidade', 'decisao_uso')}
        v['justificativa'] = text(r.get('justificativa'), 'justificativa')
        premises = references(r.get('premissas'), by_id, 'premissas', required=False)
        if claim['id'] in premises:
            raise ValueError('afirmação não pode sustentar a si própria')
        proofs = support(r.get('suporte'), evidences, required=False)
        derivation = r.get('derivacao', '')
        if not isinstance(derivation, str):
            raise ValueError('derivacao deve ser texto')
        if v['decisao_uso'] == 'avaliavel_no_escopo':
            if (v['fidelidade'] != 'sustentada' or v['adequacao_tecnica'] != 'suficiente_no_escopo'
                    or v['aplicabilidade'] not in ('fpso', 'transferivel')):
                raise ValueError('decisão avaliável incompatível com fidelidade/adequação/aplicabilidade')
            if not proofs and not (premises and derivation.strip()):
                raise ValueError('afirmação avaliável exige citação original ou dedução explícita')
        result.append({**copy.deepcopy(claim), 'condicoes': list(dict.fromkeys(
            claim['condicoes'] + texts(r.get('condicoes'), 'condicoes'))),
            'limites': list(dict.fromkeys(claim['limites'] + texts(r.get('limites'), 'limites'))),
            'suporte': proofs, 'premissas': premises, 'derivacao': derivation, 'verificacao': v})
    # Dependências são verificadas em grafo, independentemente da ordem do modelo.
    table = {a['id']: a for a in result}
    completed = set()
    def walk(aid, active):
        if aid in active:
            raise ValueError('ciclo nas premissas')
        if aid in completed:
            return
        a = table[aid]
        for pid in a['premissas']:
            walk(pid, active | {aid})
            if eligible(a) and not eligible(table[pid]):
                raise ValueError('dedução avaliável depende de premissa não avaliável')
            a['condicoes'] = list(dict.fromkeys(a['condicoes'] + table[pid]['condicoes']))
            a['limites'] = list(dict.fromkeys(a['limites'] + table[pid]['limites']))
        completed.add(aid)
    for aid in table:
        walk(aid, set())
    gaps = data.get('lacunas')
    if not isinstance(gaps, list) or len(gaps) > 3:
        raise ValueError('lacunas: lista de até três objetos')
    for gap in gaps:
        references(gap.get('afirmacoes'), table, 'afirmacoes da lacuna', required=False)
        for key in ('lacuna', 'consulta_pt', 'consulta_en', 'criterio_resolucao'):
            text(gap.get(key), key)
    return result, copy.deepcopy(gaps)


def eligible(claim):
    return claim.get('verificacao', {}).get('decisao_uso') == 'avaliavel_no_escopo'


def validate_note(data, claims):
    allowed = {a['id'] for a in claims if eligible(a)}
    text(data.get('titulo'), 'titulo')
    for key in ('blocos', 'objetivos', 'propostas_novas', 'lacunas'):
        if not isinstance(data.get(key), list):
            raise ValueError(f'{key}: lista obrigatória')
    if len(data['objetivos']) > 3:
        raise ValueError('até três objetivos por unidade, sem cota mínima')
    for b in data['blocos']:
        text(b.get('texto'), 'texto do bloco')
        references(b.get('afirmacoes'), allowed, 'afirmacoes do bloco')
    for o in data['objetivos']:
        text(o.get('descricao'), 'descricao do objetivo')
        if o.get('habilidade') not in ('compreensao', 'aplicacao', 'comparacao', 'diagnostico', 'decisao', 'integracao'):
            raise ValueError('habilidade inválida')
        refs = references(o.get('afirmacoes'), allowed, 'afirmacoes do objetivo')
        for key in ('condicoes_enunciado', 'criterios_correcao', 'respostas_aceitaveis'):
            texts(o.get(key), key)
        if not o['criterios_correcao']:
            raise ValueError('objetivo exige critérios semânticos')
        dependencies(o.get('dependencias'), refs, required=o['habilidade'] == 'integracao')
    for p in data['propostas_novas']:
        for key in ('proposicao', 'objeto', 'consulta_pt', 'consulta_en'):
            text(p.get(key), key)
        references(p.get('premissas'), allowed, 'premissas da proposta', required=False)


def review_note(data, note, claims):
    allowed = {a['id'] for a in claims if eligible(a)}
    out = copy.deepcopy(note)
    out['revisao'] = copy.deepcopy(data)
    out['quarentena'] = {}
    for key in ('blocos', 'objetivos'):
        verdicts = exact_rows(data.get(key), range(len(note[key])), 'indice')
        kept, dropped = [], []
        for i, original in enumerate(note[key]):
            v = verdicts[i]
            if type(v.get('ok')) is not bool:
                raise ValueError('revisão exige ok booleano')
            text(v.get('razao'), 'razao')
            if v['ok']:
                references(v.get('afirmacoes_suporte'), allowed, 'suporte da revisão')
                references(original['afirmacoes'], allowed, 'suporte original do bloco/objetivo aprovado')
                kept.append(original)
            else:
                dropped.append({'original': original, 'parecer': v})
        out[key], out['quarentena'][key] = kept, dropped
    return out


def dependencies(rows, allowed, required=False):
    if not isinstance(rows, list) or (required and not rows):
        raise ValueError('dependencias: lista obrigatória; integração exige ligação explícita')
    for row in rows:
        if row.get('de') not in allowed or row.get('para') not in allowed or row['de'] == row['para']:
            raise ValueError('dependência exige duas afirmações distintas existentes')
        text(row.get('necessidade'), 'necessidade da ligação')


def validate_question(data, claims, objective):
    if data.get('status') in ('insuficiente', 'impossivel', 'necessita_evidencia'):
        text(data.get('motivo'), 'motivo')
        return
    if data.get('status') != 'ok':
        raise ValueError('status inválido')
    for key in ('pergunta', 'resposta', 'explicacao'):
        text(data.get(key), key)
    if not texts(data.get('rubrica'), 'rubrica'):
        raise ValueError('rubrica semântica obrigatória')
    texts(data.get('respostas_aceitaveis'), 'respostas_aceitaveis')
    texts(data.get('premissas_cenario'), 'premissas_cenario')
    allowed = {a['id'] for a in claims if eligible(a)}
    rows = data.get('suporte')
    if not isinstance(rows, list) or not rows:
        raise ValueError('mapeie as afirmações substantivas da resposta/explicação')
    for row in rows:
        text(row.get('afirmacao'), 'afirmacao')
        references(row.get('afirmacoes'), allowed, 'suporte do item')
    dependencies(data.get('dependencias'), allowed, required=objective['habilidade'] == 'integracao')


def presentation_issues(q):
    problems = []
    for key in ('pergunta', 'resposta', 'explicacao'):
        value = q[key]
        if re.search(r'\b(?:A\d+|E\d+)\b|<NUMBER>|texto acima|material fornecido', value, re.I):
            problems.append(f'{key}:referencia_interna')
    if re.search(r'\b(?:a correção|o refinamento|retirei|reescrevi|o juiz|o gabarito foi)\b', q['explicacao'], re.I):
        problems.append('explicacao:comentario_editorial')
    # Limites de apresentação amplos, nunca interpretados como ausência de evidência.
    for key, maximum in (('pergunta', 180), ('resposta', 180), ('explicacao', 300)):
        if len(q[key].split()) > maximum:
            problems.append(f'{key}:editar_extensao')
    return problems


def validate_judgment(data, claims):
    dims = data.get('dimensoes')
    if not isinstance(dims, dict) or set(dims) != set(DIMENSOES):
        raise ValueError('inclua todas as dimensões pedidas, sem nota global')
    for v in dims.values():
        if not isinstance(v, dict) or type(v.get('ok')) is not bool:
            raise ValueError('ok booleano obrigatório')
        text(v.get('razao'), 'razao da dimensão')
    text(data.get('analise_independente'), 'analise_independente')
    text(data.get('motivo'), 'motivo')
    if data.get('acao') not in ('aprovar', 'editar', 'revisar_gabarito', 'recuperar_evidencia', 'rejeitar'):
        raise ValueError('acao inválida')
    passed = all(v['ok'] for v in dims.values())
    if data['acao'] == 'aprovar' and not passed:
        raise ValueError('aprovação contradiz dimensões reprovadas')
    allowed = {a['id'] for a in claims if eligible(a)}
    if not isinstance(data.get('suporte'), list) or (data['acao'] == 'aprovar' and not data['suporte']):
        raise ValueError('liste o suporte que auditou')
    for s in data['suporte']:
        text(s.get('afirmacao'), 'afirmacao auditada')
        references(s.get('afirmacoes'), allowed, 'suporte auditado', required=data['acao'] == 'aprovar')


def approved(judgment):
    return judgment['acao'] == 'aprovar' and all(v['ok'] for v in judgment['dimensoes'].values())
