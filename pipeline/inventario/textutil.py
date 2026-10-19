"""Normalização de texto, tokens e utilidades de arquivo."""
import hashlib
import json
import os
import re
import time
import unicodedata
from pathlib import Path

_TOKEN = re.compile(r"[a-z0-9]+(?:[./-][a-z0-9]+)*")

STOPWORDS = set("""
a o os as um uma uns umas de do da dos das em no na nos nas por para pelo pela pelos pelas com sem sob sobre entre
e ou que se ao aos à às como mais menos muito muita seu sua seus suas ser estar ter haver é são foi foram
quando onde qual quais quanto também já não sim isso esse essa este esta esses essas estes estas aquele aquela
the of and or to in on for by with from at as is are be been was were this that these those an a it its into
over under between than then which what when where who how not no can may must should shall will would
""".split())

# Termos que, sozinhos, não estabelecem pertinência técnica (iguais ao fase_4).
GENERIC_TERMS = {
    'kpi', 'gestao', 'indicador', 'indicadores', 'metas', 'meta', 'desempenho', 'programacao', 'projeto',
    'performance', 'management', 'indicator', 'indicators', 'project', 'planning', 'planejamento',
    'key performance indicator', 'key performance indicators', 'performance indicator', 'performance indicators',
    'fpso', 'fsos', 'fso', 'fpsos', 'offshore', 'subsea', 'producao', 'production', 'oil', 'gas', 'petroleo',
    'operacao', 'operation', 'operations', 'sistema', 'sistemas', 'system', 'systems', 'equipamento',
    'equipamentos', 'equipment', 'seguranca', 'safety', 'manutencao', 'maintenance', 'unidade', 'unit',
}


def strip_accents(text):
    return ''.join(c for c in unicodedata.normalize('NFKD', text) if not unicodedata.combining(c))


def norm(text):
    return strip_accents(text.casefold())


def tokens(text):
    return _TOKEN.findall(norm(text))


def squash(text):
    """Forma canônica para comparar citações: minúsculas, sem acento, só tokens."""
    return ' '.join(tokens(text))


def content_words(text):
    return [t for t in tokens(text) if len(t) >= 4 and t not in STOPWORDS and t not in GENERIC_TERMS]


def sha(text, n=16):
    return hashlib.sha256(text.encode('utf-8')).hexdigest()[:n]


def slug(text, n=48):
    s = re.sub(r'[^a-z0-9]+', '-', norm(text)).strip('-')
    return s[:n].strip('-') or 'x'


def _replace_file(tmp, path):
    # OneDrive/antivírus podem bloquear a troca por milissegundos no Windows.
    # Só repetimos bloqueios transitórios conhecidos; outros erros permanecem.
    for attempt in range(6):
        try:
            os.replace(tmp, path)
            return
        except PermissionError as exc:
            if getattr(exc, 'winerror', None) not in {5, 32} or attempt == 5:
                raise
            time.sleep(.05 * 2 ** attempt)


def atomic_json(path, data):
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    tmp = path.with_suffix(path.suffix + '.tmp')
    tmp.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding='utf-8')
    _replace_file(tmp, path)


def read_json(path, default=None):
    path = Path(path)
    if not path.exists():
        return default
    return json.loads(path.read_text(encoding='utf-8'))


def write_jsonl(path, rows):
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    tmp = path.with_suffix(path.suffix + '.tmp')
    with tmp.open('w', encoding='utf-8') as f:
        for r in rows:
            f.write(json.dumps(r, ensure_ascii=False) + '\n')
    _replace_file(tmp, path)


def read_jsonl(path):
    path = Path(path)
    if not path.exists():
        return []
    with path.open(encoding='utf-8') as f:
        return [json.loads(line) for line in f if line.strip()]


_NUM_SOURCE = re.compile(r'\d{1,3}(?: \d{3})+(?:[.,]\d+)?|\d+(?:[.,]\d+)*')
_NUM_CLAIM = re.compile(r'\d+(?:[.,]\d+)*')


def _num_keys(s):
    """Chaves equivalentes de um número: dígitos sem separadores e valor decimal provável."""
    digits = re.sub(r'\D', '', s).lstrip('0') or '0'
    keys = {digits}
    compact = s.replace(' ', '')
    if re.fullmatch(r'\d{1,3}(\.\d{3})+(,\d+)?', compact):
        compact = compact.replace('.', '').replace(',', '.')
    elif re.fullmatch(r'\d{1,3}(,\d{3})+(\.\d+)?', compact):
        compact = compact.replace(',', '')
    else:
        compact = compact.replace(',', '.')
    try:
        keys.add(repr(round(float(compact), 6)))
    except ValueError:
        pass
    return keys


def unsupported_numbers(claim, sources, min_value=10):
    """Números do texto que não aparecem nas fontes (tolera '1 050' = '1.050' e '8,33' = '8.33').

    Inteiros pequenos (< min_value) são ignorados: aparecem em contagens e fórmulas químicas.
    """
    known = set()
    for src in sources:
        for m in _NUM_SOURCE.finditer(src or ''):
            known |= _num_keys(m.group(0))
            for run in re.findall(r'\d+', m.group(0)):
                known.add(run.lstrip('0') or '0')
    missing = []
    for m in _NUM_CLAIM.finditer(claim or ''):
        s = m.group(0)
        if re.fullmatch(r'\d+', s) and int(s) < min_value:
            continue
        if not (_num_keys(s) & known):
            missing.append(s)
    return sorted(set(missing))


def quote_supported(quote, source, min_ratio=None):
    """Correspondência contígua; tolera caixa, acentos e espaços, nunca altera números/sinais."""
    def parts(text):
        return re.findall(r'[a-z0-9]+(?:[.,][0-9]+)*|[^\w\s]', norm(text))
    q, s = parts(quote), parts(source)
    if len(tokens(quote)) < 4 or not q:
        return False
    return any(s[i:i + len(q)] == q for i in range(len(s) - len(q) + 1))
