"""Contratos das respostas. Um erro aqui volta ao modelo como pedido de correção."""
import re

from . import textos as T

ID = re.compile(r'^[A-Za-z0-9_-]{1,64}$')
TIPOS_AFIRMACAO = ('conceito', 'componente', 'funcao', 'mecanismo', 'procedimento', 'controle', 'problema',
                   'seguranca', 'regulacao', 'interface')
MOTIVOS_BLOCO = ('casuistico', 'fora_fpso', 'fora_escopo', 'redundante')
MOTIVOS_DESCARTE = ('duplicada', 'contradita', 'casuistica', 'fora_fpso', 'fora_escopo', 'valor_sem_fonte', 'irrelevante')
ESTADOS = ('atendido', 'parcial', 'ausente')
PROBLEMAS = ('vago', 'erro_tecnico', 'fora_fpso', 'casuistico', 'relato_fonte', 'terminologia', 'valor_sem_fonte',
             'redundancia', 'superficial', 'estrutura', 'pt_br')


def require(ok, message):
    if not ok:
        raise ValueError(message)


def text(value, min_words=1):
    return isinstance(value, str) and len(T.words(value)) >= min_words


def rows(value, where, min_len=0):
    require(isinstance(value, list), where + ': esperado array')
    require(len(value) >= min_len, where + f': no mínimo {min_len} itens')
    require(all(isinstance(r, dict) for r in value), where + ': esperado array de objetos')
    return value


def ids(value, where, allowed=None, empty=True):
    require(isinstance(value, list) and all(isinstance(v, str) for v in value), where + ': esperado array de IDs')
    require(empty or value, where + ': informe ao menos um ID')
    require(len(set(value)) == len(value), where + ': IDs repetidos')
    if allowed is not None:
        unknown = sorted(set(value) - set(allowed))
        require(not unknown, where + ': IDs desconhecidos ' + ', '.join(unknown[:8]))


def pairs(value, where, low=1, high=4):
    require(isinstance(value, list) and low <= len(value) <= high, where + f': entre {low} e {high} pares PT/EN')
    seen = set()
    for p in value:
        require(isinstance(p, dict) and text(p.get('pt'), 3) and text(p.get('en'), 3), where + ': pares pt/en de 3+ palavras')
        require(len(p['pt'].split()) <= 16 and len(p['en'].split()) <= 16, where + ': consultas de até 16 palavras')
        key = (p['pt'].casefold().strip(), p['en'].casefold().strip())
        require(key[0] != key[1] and key not in seen, where + ': par repetido ou sem tradução')
        seen.add(key)


def lint_or_fail(value, where):
    issues = T.lint(value)
    if issues:
        detail = '; '.join((i['trecho'] + (' → ' + i['sugestao'] if i.get('sugestao') else '')) for i in issues[:6])
        raise ValueError(where + ': reescreva sem relato de fonte e com a terminologia de bordo: ' + detail)


def mapa(data, documents):
    concepts = rows(data.get('conceitos'), 'conceitos', 10)
    names = set()
    for c in concepts:
        require(text(c.get('conceito')) and len(c['conceito']) <= 80, 'conceito: nome curto obrigatório')
        key = T.fold(c['conceito'])
        require(key not in names, 'conceito repetido: ' + c['conceito'])
        names.add(key)
        require(c.get('dono') in documents, c['conceito'] + ': dono desconhecido')
        for m in rows(c.get('mencoes', []), c['conceito'] + '.mencoes'):
            require(m.get('doc') in documents and m['doc'] != c['dono'], c['conceito'] + ': menção inválida')
            require(text(m.get('enfoque'), 2), c['conceito'] + ': enfoque obrigatório na menção')


def plano(data, gaps, blocks, min_sections, max_sections):
    sections = rows(data.get('secoes'), 'secoes', min_sections)
    require(len(sections) <= max_sections, f'secoes: no máximo {max_sections}')
    seen_ids, used_gaps, used_blocks, knowledge = set(), set(), [], set()
    for i, s in enumerate(sections, 1):
        sid = f'S{i:02d}'
        require(s.get('id') == sid, f'secoes: use IDs sequenciais S01, S02...; esperado {sid}')
        require(s.get('tipo') == ('introducao' if i == 1 else 'desenvolvimento'), sid + ': a primeira seção é a introdução; as demais, desenvolvimento')
        require(text(s.get('titulo')) and text(s.get('objetivo'), 3), sid + ': título e objetivo obrigatórios')
        ks = rows(s.get('conhecimentos'), sid + '.conhecimentos', 1)
        for j, k in enumerate(ks, 1):
            require(k.get('id') == f'{sid}K{j:02d}', sid + f': conhecimentos com IDs {sid}K01, {sid}K02...')
            require(text(k.get('descricao'), 3) and type(k.get('essencial')) is bool, k['id'] + ': descrição e essencial')
            ids(k.get('lacunas', []), k['id'] + '.lacunas', gaps)
            used_gaps.update(k.get('lacunas', []))
            knowledge.add(k['id'])
        ids(s.get('blocos_base', []), sid + '.blocos_base', blocks)
        used_blocks += s.get('blocos_base', [])
        pairs(s.get('consultas'), sid + '.consultas')
        seen_ids.add(sid)
    dropped = rows(data.get('blocos_descartados', []), 'blocos_descartados')
    for d in dropped:
        require(d.get('id') in blocks and d.get('motivo') in MOTIVOS_BLOCO and text(d.get('justificativa'), 2),
                'blocos_descartados: id da base, motivo válido e justificativa')
    all_blocks = used_blocks + [d['id'] for d in dropped]
    repeated = sorted({b for b in all_blocks if all_blocks.count(b) > 1})
    require(not repeated, 'Cada bloco da base vai para uma única seção ou para descartados: ' + ', '.join(repeated[:8]))
    missing = sorted(set(blocks) - set(all_blocks))
    require(not missing, 'Blocos da base sem destino: ' + ', '.join(missing[:12]))
    out = rows(data.get('lacunas_fora_de_escopo', []), 'lacunas_fora_de_escopo')
    for o in out:
        require(o.get('id') in gaps and text(o.get('justificativa'), 3), 'lacunas_fora_de_escopo: id e justificativa')
    missing_gaps = sorted(set(gaps) - used_gaps - {o['id'] for o in out})
    require(not missing_gaps, 'Lacunas sem conhecimento nem justificativa: ' + ', '.join(missing_gaps[:12]))


def rascunho(data, knowledge, min_claims=4, max_claims=40):
    claims = rows(data.get('afirmacoes'), 'afirmacoes', min_claims)
    require(len(claims) <= max_claims, f'afirmacoes: no máximo {max_claims}')
    for i, a in enumerate(claims, 1):
        require(a.get('id') == f'A{i:02d}', 'afirmacoes: IDs sequenciais A01, A02...')
        require(text(a.get('texto'), 6), a['id'] + ': afirmação completa (6+ palavras)')
        require(a.get('tipo') in TIPOS_AFIRMACAO, a['id'] + ': tipo inválido')
        require(type(a.get('especifico')) is bool, a['id'] + ': especifico booleano')
        ids(a.get('conhecimentos'), a['id'] + '.conhecimentos', knowledge, empty=False)


def leitura(data, passages, knowledge, claims):
    findings = rows(data.get('achados'), 'achados')
    for i, f in enumerate(findings, 1):
        require(text(f.get('id')) and ID.match(f['id']), 'achados: id seguro')
        require(text(f.get('texto'), 6), f['id'] + ': síntese técnica (6+ palavras)')
        ids(f.get('fontes'), f['id'] + '.fontes', passages, empty=False)
        ids(f.get('conhecimentos'), f['id'] + '.conhecimentos', knowledge, empty=False)
    require(len({f['id'] for f in findings}) == len(findings), 'achados: IDs repetidos')
    for v in rows(data.get('verificacoes', []), 'verificacoes'):
        require(v.get('afirmacao') in claims and v.get('estado') in ('apoia', 'contradiz'), 'verificacoes: afirmação conhecida e estado apoia|contradiz')
        ids(v.get('fontes'), 'verificacoes.fontes', passages, empty=False)
    ids(data.get('lacunas', []), 'lacunas', knowledge)
    queries = data.get('novas_consultas', [])
    if queries:
        pairs(queries, 'novas_consultas')


def consolidacao(data, claims, findings, blocks, knowledge, contradicted, specific, allow_values=False):
    units = rows(data.get('unidades'), 'unidades', 1)
    accounted = []
    for i, u in enumerate(units, 1):
        require(u.get('id') == f'U{i:02d}', 'unidades: IDs sequenciais U01, U02...')
        require(text(u.get('texto'), 6), u['id'] + ': texto completo')
        ids(u.get('conhecimentos'), u['id'] + '.conhecimentos', knowledge, empty=False)
        origin = u.get('origem')
        require(isinstance(origin, dict), u['id'] + ': origem obrigatória')
        a, f, b = origin.get('afirmacoes', []), origin.get('achados', []), origin.get('blocos', [])
        ids(a, u['id'] + '.origem.afirmacoes', claims)
        ids(f, u['id'] + '.origem.achados', findings)
        ids(b, u['id'] + '.origem.blocos', blocks)
        require(a or f or b, u['id'] + ': informe ao menos uma origem')
        require(not (set(a) & contradicted) or f, u['id'] + ': afirmação contradita só entra corrigida por achado')
        if not allow_values and not f and not b:
            require(not T.has_value(u['texto']), u['id'] + ': valor numérico sem achado nem bloco revisado; descreva qualitativamente')
        lint_or_fail(u['texto'], u['id'])
        accounted += a + f + b
    discarded = []
    for d in rows(data.get('descartadas', []), 'descartadas'):
        require(d.get('ref') in set(claims) | set(findings) | set(blocks), 'descartadas: ref desconhecida')
        require(d.get('motivo') in MOTIVOS_DESCARTE, 'descartadas: motivo inválido')
        discarded.append(d['ref'])
    expected = set(claims) | set(findings) | set(blocks)
    missing = sorted(expected - set(accounted) - set(discarded))
    # Tolerância pequena: o relatório registra o que ficou sem destino explícito.
    require(len(missing) <= max(2, len(expected) // 10),
            'IDs sem destino (use em uma unidade ou descarte): ' + ', '.join(missing[:15]))
    both = sorted(set(accounted) & set(discarded))
    require(not both, 'IDs ao mesmo tempo usados e descartados: ' + ', '.join(both[:15]))
    # Uma afirmação de redator entra em uma única unidade: é o que impede repetição.
    # Achados e blocos podem sustentar mais de uma unidade.
    used_claims = [x for u in units for x in u['origem'].get('afirmacoes', [])]
    repeated = sorted({x for x in used_claims if used_claims.count(x) > 1})
    require(not repeated, 'Afirmações em mais de uma unidade (funda ou escolha uma): ' + ', '.join(repeated[:15]))
    rows(data.get('conflitos', []), 'conflitos')


def redacao(data, units, section_id):
    blocks = rows(data.get('blocos'), 'blocos', 1)
    require(len(blocks) <= 10, 'blocos: no máximo 10 por seção')
    used = []
    for i, b in enumerate(blocks, 1):
        require(b.get('id') == f'{section_id}B{i:02d}', f'blocos: IDs {section_id}B01, {section_id}B02...')
        require(text(b.get('subtitulo')) and text(b.get('texto'), 25), b['id'] + ': subtítulo e texto (25+ palavras)')
        ids(b.get('unidades'), b['id'] + '.unidades', units, empty=False)
        lint_or_fail(b['subtitulo'] + ' ' + b['texto'], b['id'])
        used += b['unidades']
    missing = sorted(set(units) - set(used))
    repeated = sorted({u for u in used if used.count(u) > 1})
    require(not missing, 'Unidades não usadas: ' + ', '.join(missing[:15]))
    require(not repeated, 'Unidades usadas mais de uma vez: ' + ', '.join(repeated[:15]))


def consolida_doc(data, blocks):
    ops = rows(data.get('operacoes', []), 'operacoes')
    seen = set()
    for o in ops:
        require(o.get('bloco') in blocks and o['bloco'] not in seen, 'operacoes: bloco conhecido, uma operação por bloco')
        seen.add(o['bloco'])
        require(text(o.get('novo_texto'), 15) and text(o.get('motivo'), 2), o['bloco'] + ': novo_texto e motivo')
        ids(o.get('informacao_preservada_em', []), o['bloco'] + '.informacao_preservada_em', blocks)
        lint_or_fail(o['novo_texto'], o['bloco'])


def cobertura(data, gaps, blocks):
    cov = rows(data.get('cobertura'), 'cobertura')
    require({c.get('id') for c in cov} == set(gaps) and len(cov) == len(gaps), 'cobertura: avalie cada lacuna exatamente uma vez')
    for c in cov:
        require(c.get('estado') in ESTADOS, c['id'] + ': estado atendido|parcial|ausente')
        ids(c.get('blocos', []), c['id'] + '.blocos', blocks)


def revisao(data, gaps, blocks):
    cobertura(data, gaps, blocks)
    for p in rows(data.get('problemas', []), 'problemas'):
        require(p.get('bloco') in blocks and p.get('tipo') in PROBLEMAS, 'problemas: bloco conhecido e tipo válido')
        require(text(p.get('descricao'), 3) and text(p.get('correcao'), 2), 'problemas: descrição e correção')
    require(text(data.get('parecer'), 3), 'parecer obrigatório')


def reparo(data, expected):
    blocks = rows(data.get('blocos'), 'blocos', 1)
    require({b.get('id') for b in blocks} == set(expected) and len(blocks) == len(expected), 'blocos: devolva exatamente os blocos pedidos')
    for b in blocks:
        require(text(b.get('subtitulo')) and text(b.get('texto'), 25), b['id'] + ': subtítulo e texto')
        lint_or_fail(b['subtitulo'] + ' ' + b['texto'], b['id'])


def polimento(data, originals):
    """Mesmos blocos, sem perder conteúdo: nenhum número novo e texto de tamanho comparável."""
    blocks = rows(data.get('blocos'), 'blocos', 1)
    expected = {b['id']: b for b in originals}
    require({b.get('id') for b in blocks} == set(expected) and len(blocks) == len(expected),
            'blocos: devolva exatamente os blocos recebidos, na mesma ordem')
    kept_old = kept_new = 0
    for b in blocks:
        old = expected[b['id']]
        if b.get('remover') is True:
            require(len(T.words(old['texto'])) <= 150, b['id'] + ': só remova bloco curto que descreve o documento')
            continue
        require(text(b.get('subtitulo')) and text(b.get('texto'), 15), b['id'] + ': subtítulo e texto')
        new_numbers = T.numbers(b['texto']) - T.numbers(old['subtitulo'] + ' ' + old['texto'])
        require(not new_numbers, b['id'] + ': números novos não permitidos: ' + ', '.join(sorted(new_numbers)[:5]))
        lint_or_fail(b['subtitulo'] + ' ' + b['texto'], b['id'])
        kept_old += len(T.words(old['texto']))
        kept_new += len(T.words(b['texto']))
    require(kept_new >= 0.8 * kept_old, 'texto encurtado demais: o polimento não resume nem corta conteúdo')
    siglas = rows(data.get('siglas_expandidas', []), 'siglas_expandidas')
    require(all(isinstance(s.get('sigla'), str) and text(s.get('expansao')) for s in siglas),
            'siglas_expandidas: sigla e expansao')
    final = ' '.join(b.get('texto', '') for b in blocks if b.get('remover') is not True)
    pending, _ = T.acronyms(dict(capitulos=[dict(blocos=[dict(id=b['id'], subtitulo=b.get('subtitulo', ''),
                                                              texto=b.get('texto', '')) for b in blocks
                                                         if b.get('remover') is not True])]))
    left = sorted({s for v in pending.values() for s in v})
    require(not left, 'siglas sem expansão na primeira ocorrência do capítulo: ' + ', '.join(left[:12]))
    unknown = [s['sigla'] for s in siglas if s['sigla'] not in final]
    require(not unknown, 'siglas_expandidas: siglas que não aparecem no capítulo: ' + ', '.join(unknown[:8]))
