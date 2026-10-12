"""Normalização de texto, tokens e utilidades de arquivo."""
import hashlib
import json
import os
import re
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


def atomic_json(path, data):
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    tmp = path.with_suffix(path.suffix + '.tmp')
    tmp.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding='utf-8')
    os.replace(tmp, path)


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
    os.replace(tmp, path)


def read_jsonl(path):
    path = Path(path)
    if not path.exists():
        return []
    with path.open(encoding='utf-8') as f:
        return [json.loads(line) for line in f if line.strip()]


def quote_supported(quote, source, min_ratio=None):
    """Correspondência contígua; tolera caixa, acentos e espaços, nunca altera números/sinais."""
    def parts(text):
        return re.findall(r'[a-z0-9]+(?:[.,][0-9]+)*|[^\w\s]', norm(text))
    q, s = parts(quote), parts(source)
    if len(tokens(quote)) < 4 or not q:
        return False
    return any(s[i:i + len(q)] == q for i in range(len(s) - len(q) + 1))
