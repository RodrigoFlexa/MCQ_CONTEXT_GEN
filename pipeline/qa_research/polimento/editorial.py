"""Sinais editoriais verificáveis; reparo localizado e uma só reavaliação."""
import re
import unicodedata

from pipeline.qa_research.v3.review import editor_issues as inherited_issues

READING = re.compile(
    r'\b(?:fabricante consultado|no contexto consultado|no caso relatado|'
    r'(?:a|esta|essa) fonte (?:afirma|descreve|relata)|'
    r'(?:o|este|esse) (?:trecho|estudo|artigo|documento) (?:consultado|citado|fornecido)|'
    r'(?:nos|os) ensaios relatados|(?:na|a) literatura consultada)\b', re.I)


def block_issues(block):
    issues = inherited_issues(block)
    if READING.search(block['texto']):
        issues.append('Relato de leitura: explique o conceito e suas condições; registre a origem no auxiliar')
    return sorted(set(issues))


def words(text):
    text = unicodedata.normalize('NFKD', text.casefold())
    return re.findall(r'[a-z0-9]+', ''.join(c for c in text if not unicodedata.combining(c)))


def audit(document):
    """Similaridade é pista para o revisor, não autorização para apagar conceitos."""
    issues, paragraphs = [], []
    for chapter in document['capitulos']:
        for block in chapter['blocos']:
            for description in block_issues(block):
                issues.append(dict(tipo='editorial', blocos=[block['id']], descricao=description,
                                   critico=False, bloqueante=True))
            for text in re.split(r'\n\s*\n', block['texto']):
                tokens = words(text)
                if len(tokens) >= 40:
                    shingles = {tuple(tokens[i:i + 5]) for i in range(len(tokens) - 4)}
                    paragraphs.append((block['id'], tokens, shingles))
    seen = set()
    for i, (bid, tokens, shingles) in enumerate(paragraphs):
        for other, previous, other_shingles in paragraphs[:i]:
            score = len(shingles & other_shingles) / min(len(shingles), len(other_shingles))
            if score < .65:
                continue
            exact = tokens == previous
            key = (tuple(sorted({bid, other})), exact)
            if key in seen:
                continue
            seen.add(key)
            issues.append(dict(tipo='editorial', blocos=list(key[0]),
                descricao=('Parágrafo longo duplicado' if exact else 'Possível repetição entre parágrafos; conferir condições e informação exclusiva'),
                critico=False, bloqueante=exact, similaridade=round(score, 3)))
    return issues


def pending_work(interventions, coverage, omissions, problems):
    result = [dict(i, origem='intervencao') for i in interventions]
    result.extend(dict(id='cobertura_' + p['id'], tipo='lacuna_essencial', origem='cobertura',
        pontos=[p['id']], objetivo=p['motivo']) for p in coverage if p['estado'] != 'atendido')
    result.extend(dict(id=f'escopo_{i}', tipo='lacuna_essencial', origem='escopo', objetivo=text)
                  for i, text in enumerate(omissions, 1))
    result.extend(dict(id=f'revisao_{i}', tipo=p.get('tipo', 'tecnico'), origem='revisao',
        objetivo=p['descricao'], blocos=p['blocos']) for i, p in enumerate(problems, 1))
    return result
