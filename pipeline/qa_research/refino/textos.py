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
    r'\b(?:o|os|este|esse|neste|nesse|no) trechos? (?:citad|recuperad|analisad|consultad|selecionad|afirma|indica|mostra|descreve|relata)',
    r'\bsegundo (o|a|os|as) (documento|fonte|relat[óo]rio|estudo|autor)',
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


# Trocas sem ambiguidade (o especialista já indicou o termo de bordo); aplicadas antes da checagem.
TROCAS = [
    (r'\bupsets\b', 'distúrbios'), (r'\bupset\b', 'distúrbio'), (r'\bfail-safe\b', 'falha segura'),
    (r'\bwell tests?\b', 'teste de poço'), (r'\bpadeyes\b', 'olhais'), (r'\bpadeye\b', 'olhal'),
    (r'\bplaneza\b', 'planicidade'), (r'\bpousabilidade\b', 'capacidade de pouso'),
    (r'\bmicrobicidas\b', 'biocidas'), (r'\bmicrobicida\b', 'biocida'), (r'\bintertravagem\b', 'intertravamento'),
    (r'\bintertravagens\b', 'intertravamentos'), (r'\b[áa]gua fresca\b', 'água doce'), (r'\btrumpet\b', 'boca de sino'),
    (r'\bcabe[çc]alhos\b', 'headers'), (r'\bcabe[çc]alho\b', 'header'),
]


def fix_terms(text):
    for pattern, replacement in TROCAS:
        text = re.sub(pattern, replacement, text, flags=re.I)
    return text


def has_value(text):
    return bool(VALOR.search(text or ''))


# ---------------------------------------------------------------- estilo (polimento)

META = [
    r'\b(?:est[ea]|ness[ea]|nest[ea]|dest[ea]|o present[e]|a present[e]) (?:se[çc][ãa]o|documento|cap[íi]tulo|texto|parte)\b',
    r'\bse[çc](?:[ãa]o|[õo]es) \d+\b', r'\bestrutura do documento\b',
    r'\bo documento (?:segue|apresenta|trata|aborda|organiza|descreve|parte)\b',
    r'\b(?:como|conforme) (?:visto|descrito|mencionado|discutido|detalhado) (?:acima|anteriormente|adiante|mais adiante)\b',
    r'\b(?:ser[áa]o?|s[ãa]o) (?:tratad|abordad|detalhad|discutid)[oa]s? (?:adiante|a seguir|mais adiante|na se[çc][ãa]o)',
]
TRAVESSAO = re.compile(r'\s[—–]\s|—')
SIGLA = re.compile(r'\b[A-Z][A-Z0-9]*[A-Z](?:-\d+)?s?\b')
ROMANOS = frozenset('II III IV VI VII VIII IX XI XII XIII XIV XV XX'.split())


def style_issues(text):
    """Texto que fala do próprio documento e travessões."""
    issues = []
    for pattern in META:
        for m in re.finditer(pattern, text, re.I):
            issues.append(dict(tipo='metatexto', trecho=text[max(0, m.start() - 30):m.end() + 30]))
    for m in TRAVESSAO.finditer(text):
        issues.append(dict(tipo='travessao', trecho=text[max(0, m.start() - 30):m.end() + 30]))
    return issues


def _base_sigla(token):
    return token[:-1] if token.endswith('s') and token[:-1].isupper() else token


def _defined_here(text, m):
    """SIGLA (expansão), expansão (SIGLA) ou sigla dentro de um parêntese já aberto ("(Multiphase Flow Meter, MPFM)",
    "(Código IMDG)"): nos três casos o leitor tem a expansão ali."""
    after, before = text[m.end():m.end() + 3], text[max(0, m.start() - 1):m.start()]
    if after.lstrip().startswith('(') or before == '(':
        return True
    head = text[max(0, m.start() - 200):m.start()]
    if head.count('(') > head.count(')'):
        return True
    # A sigla faz parte do nome expandido logo adiante: "ASTM International (ASTM)", "No FPSO, unidade ... (FPSO, ...)".
    sigla = _base_sigla(m.group(0))
    return bool(re.match(r'[^.;()]{0,100}\(' + re.escape(sigla) + r'\b', text[m.end():m.end() + 120]))


def acronyms(document, known=()):
    """Primeira ocorrência de cada sigla no documento, na ordem; sem expansão = pendente.

    Retorna ({bloco: [siglas pendentes]}, conjunto de siglas definidas)."""
    defined, seen, pending = set(known), set(known), {}
    for bid, subtitle, text in blocks_of(document):
        for m in SIGLA.finditer(text):
            token = _base_sigla(m.group(0))
            if token in ROMANOS or token in seen:
                continue
            seen.add(token)
            if _defined_here(text, m):
                defined.add(token)
            else:
                pending.setdefault(bid, []).append(token)
    return pending, defined


DEPENDENTE = re.compile(r'^\s*(?:ess[ea]s?|isso|isto|nesse contexto|nesse caso|por isso|al[ée]m disso|da mesma forma|'
                        r'o mesmo|a mesma|tal (?:sistema|equipamento|condi[çc][ãa]o)|esses? (?:sistemas?|equipamentos?|indicadores?))\b', re.I)


def dependent_opening(text):
    """Bloco que começa apoiado em algo dito em outro bloco (ruim quando o texto é recortado)."""
    m = DEPENDENTE.match(text or '')
    return [dict(tipo='abertura_dependente', trecho=(text or '')[:80])] if m else []


def style_report(document):
    """Contagem dos problemas de estilo, antes e depois do polimento."""
    pending, _ = acronyms(document)
    counts = Counter(i['tipo'] for _, s, t in blocks_of(document) for i in style_issues(s + ' ' + t))
    return dict(metatexto=counts.get('metatexto', 0), travessao=counts.get('travessao', 0),
                siglas_sem_expansao=sum(len(v) for v in pending.values()),
                aberturas_dependentes=sum(1 for _, _, t in blocks_of(document) if dependent_opening(t)))


# ---------------------------------------------------------------- uso como fonte de questões

TESTAVEL = {
    'definicao': r'\b(?:[ée] (?:o|a|um|uma) [\wÀ-ÿ-]+|consiste em|define-se|denomina-se|chama-se|corresponde a|refere-se a)\b',
    'funcao': r'\b(?:serve para|tem (?:a|como) fun[çc][ãa]o|destina-se a|permite|impede|evita|protege|garante que)\b',
    'causa': r'\b(?:porque|devido a|provoca|causa|resulta em|leva a|em consequ[êe]ncia|por causa de|reduz|aumenta|eleva)\b',
    'condicao': r'\b(?:quando|caso|somente|s[óo] (?:quando|se)|desde que|exceto|a menos que|se (?:o|a|os|as|houver))\b',
    'contraste': r'\b(?:diferentemente|ao contr[áa]rio|enquanto|difere|em vez de|por outro lado|j[áa] (?:o|a))\b',
    'sequencia': r'\b(?:primeiro|em seguida|depois de|antes de|ap[óo]s|por fim|na sequ[êe]ncia)\b',
}
VAGO = re.compile(r'\b(?:[ée] (?:fundamental|essencial|importante|crucial) (?:que|considerar|garantir|manter)|contribui para|'
                  r'de forma integrada|de maneira integrada|papel (?:relevante|central|fundamental)|vis[ãa]o hol[íi]stica|'
                  r'agrega valor|de modo sist[êe]mico)\b', re.I)


def testability(document):
    """Fração de sentenças com ao menos uma relação verificável (definição, função, causa, condição,
    contraste, sequência) e fração com marcadores de prosa vaga. Heurística, para comparar versões."""
    rows = [s for _, _, t in blocks_of(document) for s in sentences(t)]
    if not rows:
        return dict(sentencas=0, testaveis=0.0, vagas=0.0, por_tipo={})
    kinds = Counter()
    hits = 0
    for s in rows:
        found = [k for k, pattern in TESTAVEL.items() if re.search(pattern, s, re.I)]
        kinds.update(found)
        hits += bool(found)
    vague = sum(1 for s in rows if VAGO.search(s))
    return dict(sentencas=len(rows), testaveis=round(hits / len(rows), 4), vagas=round(vague / len(rows), 4),
                por_tipo={k: round(v / len(rows), 4) for k, v in sorted(kinds.items())})


def numbers(text):
    return set(re.findall(r'\d+(?:[.,]\d+)?', text or ''))


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
