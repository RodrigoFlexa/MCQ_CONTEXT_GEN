"""Texto, redundância e verificações locais, sem modelo nem dependências externas.

A similaridade aqui é pista para o consolidador e medida para o relatório; não
autoriza apagar nada sozinha.
"""
import math
import re
import unicodedata
from collections import Counter

STOP = frozenset('''a à ao aos as às até com como da das de dela dele deles do dos e é ela elas ele eles em entre
era essa essas esse esses esta está estas este estes eu foi for há isso isto já la lhe mais mas me mesmo
muito na nas não nem no nos nós o os ou para pela pelas pelo pelos pode podem por qual quando que quem se
sem ser seu seus sua suas são também tem têm um uma umas uns ainda sobre após antes cada onde assim porque
deve devem quanto sendo sido seja forma caso modo todo toda todos todas outro outra outros outras
the of and to in for on with by is are be as at or an that this from it its into than then'''.split())

# Termos que o especialista substituiu e que não têm outro sentido plausível nestes
# documentos. Termos dependentes de contexto (operador, corrente, respiração) ficam
# como orientação nos prompts e na revisão, não como bloqueio.
DESACONSELHADOS = [
    (r'\bcabe[çc]alhos?\b', 'header'),
    (r'\brompedor(es)? de press[ãa]o\b', 'disco de ruptura'),
    (r'\bfail-safe\b', 'falha segura'),
    (r'\bupsets?\b', 'distúrbio'),
    (r'\bturretad[oa]s?\b', 'turret'),
    (r'\bchoque de momento\b', 'golpe de aríete'),
    (r'\bintertravage(m|ns)\b', 'intertravamento'),
    (r'\bwell test\b', 'teste de poço'),
    (r'\bengrenamentos?\b', 'engrenagem'),
    (r'\bplaneza\b', 'planicidade'),
    (r'\btrumpet\b', 'boca de sino'),
    (r'\bmicrobicidas?\b', 'biocida'),
    (r'\bpousabilidade\b', 'capacidade de pouso'),
    (r'\blingas?\b', 'eslinga'),
    (r'\blingueiros?\b', 'jogo de eslingas'),
    (r'\bpadeyes?\b', 'olhal'),
    (r'\bbanksman\b', 'supervisor/sinalizador'),
    (r'\bslingers?\b', 'homem de área'),
    (r'\beslingador(es)?\b', 'homem de área'),
    (r'\bchamin[ée] (do|de) flare\b', 'torre do flare'),
    (r'\bágua fresca\b', 'água doce'),
]
RELATO_FONTE = [
    r'\b(a|as|esta|essa|uma) fontes? (afirma|afirmam|indica|indicam|relata|relatam|descreve|descrevem|mostra|mostram|cita)\b',
    r'\bo trecho\b', r'\bos trechos\b', r'\bsegundo (o|a|os|as) (documento|fonte|relat[óo]rio|estudo|autor)',
    r'\bnos ensaios relatados\b', r'\bo documento (analisado|consultado|examinado)\b',
    r'\bo relat[óo]rio (analisado|examinado|de investiga[çc][ãa]o)\b', r'\bconforme (a|as) passage',
    r'\bpassagens? (recuperad|consultad|selecionad)', r'\bno caso (analisado|examinado|investigado)\b',
]
VALOR = re.compile(r'\d+(?:[.,]\d+)?\s*(?:%|ppm|ppb|mg/?\s?l|g/?l|bar[ag]?\b|psi[ag]?\b|kpa|mpa|°\s?c|ºc|k\b|m³|m3|nm³|'
                   r'kg|t\b|mm\b|cm\b|m\b|km\b|kv\b|v\b|kw\b|mw\b|hz\b|rpm\b|h\b|min\b|s\b|dias?\b|anos?\b|meses\b|n[óo]s\b|'
                   r'bpd|bbl|ppg|cp\b|db\b|db\(a\)|lux)', re.I)


def norm(text):
    return re.sub(r'\s+', ' ', unicodedata.normalize('NFC', (text or '').replace(' ', ' '))).strip()


def fold(text):
    return ''.join(c for c in unicodedata.normalize('NFD', text.casefold()) if unicodedata.category(c) != 'Mn')


def words(text):
    return re.findall(r"[\wÀ-ÿ]+(?:[-'][\wÀ-ÿ]+)*", text or '')


def sentences(text):
    parts = re.split(r'(?<=[.!?;])\s+(?=[A-ZÁÉÍÓÚÂÊÔÃÕÇ0-9“"(])', norm(text))
    return [p for p in parts if len(words(p)) >= 6]


def terms(text):
    return [w for w in (fold(x) for x in words(text)) if len(w) >= 3 and w not in STOP and not w.isdigit()]


def lint(text, desaconselhados=True):
    """Problemas locais: relato de fonte e termos que o especialista substituiu."""
    issues = []
    low = text.casefold()
    for pattern in RELATO_FONTE:
        for m in re.finditer(pattern, low):
            issues.append(dict(tipo='relato_fonte', trecho=text[max(0, m.start() - 30):m.end() + 30]))
    if desaconselhados:
        for pattern, suggestion in DESACONSELHADOS:
            for m in re.finditer(pattern, low):
                # "eslinga" contém "linga"; o \b do padrão já impede esse caso.
                issues.append(dict(tipo='terminologia', trecho=text[m.start():m.end()], sugestao=suggestion))
    return issues


def has_value(text):
    return bool(VALOR.search(text or ''))


class Vectors:
    """TF-IDF por sentença; IDF estimado no conjunto comparado."""
    def __init__(self, texts):
        bags = [Counter(terms(t)) for t in texts]
        df = Counter(t for b in bags for t in b)
        n = max(1, len(bags))
        self.idf = {t: math.log((1 + n) / (1 + c)) + 1 for t, c in df.items()}
        self.vectors = [self._weigh(b) for b in bags]

    def _weigh(self, bag):
        vector = {t: (1 + math.log(c)) * self.idf.get(t, 1.0) for t, c in bag.items()}
        size = math.sqrt(sum(v * v for v in vector.values())) or 1.0
        return {t: v / size for t, v in vector.items()}

    @staticmethod
    def cosine(a, b):
        if len(a) > len(b):
            a, b = b, a
        return sum(v * b.get(t, 0.0) for t, v in a.items())


def blocks_of(document):
    """documento.json → [(id, subtitulo, texto)]; aceita ids ausentes."""
    out = []
    for ci, chapter in enumerate(document.get('capitulos', []), 1):
        for bi, block in enumerate(chapter.get('blocos', []), 1):
            out.append((block.get('id') or f'C{ci:02d}B{bi:02d}', block.get('subtitulo', ''), block.get('texto', '')))
    return out


def redundancy(document, threshold=0.55, max_pairs=60):
    """Sentenças quase repetidas entre blocos diferentes do mesmo documento."""
    rows = [(bid, s) for bid, _, text in blocks_of(document) for s in sentences(text)]
    if len(rows) < 2:
        return dict(sentencas=len(rows), pares=[], taxa_redundancia=0.0, similaridade_maxima_media=0.0,
                    repeticao_6gramas=0.0)
    vec = Vectors([s for _, s in rows]).vectors
    pairs, best = [], [0.0] * len(rows)
    for i in range(len(rows)):
        for j in range(i + 1, len(rows)):
            if rows[i][0] == rows[j][0]:
                continue
            sim = Vectors.cosine(vec[i], vec[j])
            best[i], best[j] = max(best[i], sim), max(best[j], sim)
            if sim >= threshold:
                pairs.append(dict(a=rows[i][0], b=rows[j][0], similaridade=round(sim, 3),
                                  sentenca_a=rows[i][1], sentenca_b=rows[j][1]))
    pairs.sort(key=lambda p: -p['similaridade'])
    flagged = sum(1 for b in best if b >= threshold)
    return dict(sentencas=len(rows), pares=pairs[:max_pairs], n_pares=len(pairs),
                taxa_redundancia=round(flagged / len(rows), 4),
                similaridade_maxima_media=round(sum(best) / len(best), 4),
                repeticao_6gramas=ngram_repetition(' '.join(t for _, _, t in blocks_of(document))))


def ngram_repetition(text, n=6):
    tokens = terms(text)
    grams = [tuple(tokens[i:i + n]) for i in range(len(tokens) - n + 1)]
    if not grams:
        return 0.0
    counts = Counter(grams)
    return round(sum(c for c in counts.values() if c > 1) / len(grams), 4)


def cross_redundancy(documents, threshold=0.55):
    """Fração das sentenças de cada documento com quase-duplicata em outro documento."""
    rows = [(doc_id, s) for doc_id, doc in documents.items() for _, _, t in blocks_of(doc) for s in sentences(t)]
    if not rows:
        return {}
    vec = Vectors([s for _, s in rows]).vectors
    # Índice invertido por termo evita comparação quadrática completa.
    postings = {}
    for i, v in enumerate(vec):
        for t in sorted(v, key=lambda k: -v[k])[:8]:
            postings.setdefault(t, []).append(i)
    hit = [False] * len(rows)
    for i, v in enumerate(vec):
        if hit[i]:
            continue
        seen = set()
        for t in sorted(v, key=lambda k: -v[k])[:8]:
            for j in postings.get(t, []):
                if j in seen or rows[j][0] == rows[i][0]:
                    continue
                seen.add(j)
                if Vectors.cosine(v, vec[j]) >= threshold:
                    hit[i] = hit[j] = True
    result = {}
    for doc_id in documents:
        idx = [i for i, r in enumerate(rows) if r[0] == doc_id]
        result[doc_id] = round(sum(hit[i] for i in idx) / len(idx), 4) if idx else 0.0
    return result


def stats(document):
    blocks = blocks_of(document)
    text = ' '.join(t for _, _, t in blocks)
    return dict(palavras=len(words(text)), blocos=len(blocks), capitulos=len(document.get('capitulos', [])),
                sentencas=sum(len(sentences(t)) for _, _, t in blocks))


def markdown(document, grupo=None):
    """Mesmo formato Markdown da v2: # título, ## grupo, ### capítulo, #### bloco."""
    lines = ['# ' + document['titulo'], '']
    last_group = None
    for chapter in document['capitulos']:
        group = chapter.get('grupo') or grupo
        if group and group != last_group:
            lines += ['## ' + group, '']
            last_group = group
        lines += ['### ' + chapter['titulo'], '']
        for block in chapter['blocos']:
            lines += ['#### ' + block['subtitulo'], '']
            lines += [p.strip() + '\n' for p in block['texto'].split('\n\n') if p.strip()]
    return '\n'.join(lines).rstrip() + '\n'


def clean(document):
    """Formato consumido pela QA: sem ids, anotações ou proveniência."""
    return dict(titulo=document['titulo'], capitulos=[
        dict(titulo=c['titulo'], grupo=c.get('grupo'),
             blocos=[dict(subtitulo=b['subtitulo'], texto=b['texto']) for b in c['blocos']])
        for c in document['capitulos']])
