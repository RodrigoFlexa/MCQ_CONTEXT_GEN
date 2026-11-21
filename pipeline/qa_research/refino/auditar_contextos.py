"""Auditoria dos 40 documentos refinados: problemas de forma e de conteúdo detectáveis por regra."""
import json, re, sys, collections
from pathlib import Path
from pipeline.qa_research.refino import textos as T

base = Path(sys.argv[1])
ING = re.compile(r'\b(?:heading|subsea|marine|topside|offloading|riser|risers|flare|blowdown|shutdown|slug|slugging|scrubber|manifold|header|knock-out|turret|swivel|hawser|weather vaning|trim|blanket|ring main|stress-joint|pull in|pull-in|hook up|hook-up)\b', re.I)
rows = []
total = collections.Counter()
for d in sorted(p for p in base.iterdir() if (p / 'documento.json').exists()):
    doc = json.loads((d / 'documento.json').read_text())
    gl = json.loads((d / 'glossario.json').read_text()) if (d / 'glossario.json').exists() else {}
    blocks = list(T.blocks_of(doc))
    text = '\n'.join(t for _, _, t in blocks)
    pend, defined = T.acronyms(doc)
    sty = T.style_report(doc)
    lint = sum(len(T.lint(s + ' ' + t)) for _, s, t in blocks)
    words = [len(T.words(t)) for _, _, t in blocks]
    longos = sum(w > 450 for w in words); curtos = sum(w < 60 for w in words)
    defs_fpso = len(re.findall(r'FPSO\)?,? (?:é|que é) uma', text))
    expans = collections.Counter(m.group(1) for m in re.finditer(r'\(([A-Z][A-Z0-9-]{1,})\)', text))
    reexp = {k: v for k, v in expans.items() if v > 1}
    sub_dup = len([s for s, c in collections.Counter(s for _, s, _ in blocks).items() if c > 1])
    meta = sum(1 for _, s, t in blocks for i in T.style_issues(s + ' ' + t) if i['tipo'] == 'metatexto')
    nums = len(re.findall(r'\b\d+(?:[.,]\d+)?\s?(?:%|bar|psi|°C|ºC|m|mm|km|h|kV|V|MW|kW|ppm|mg/L|kg|t)\b', text))
    vag = T.testability(doc)['vagas']
    caps = [c['titulo'] for c in doc['capitulos']]
    r = dict(id=d.name, palavras=len(T.words(text)), blocos=len(blocks), siglas_pend=sum(len(v) for v in pend.values()),
             pend=sorted({s for v in pend.values() for s in v})[:12], reexpandidas=reexp, meta=meta, travessao=sty['travessao'],
             lint=lint, longos=longos, curtos=curtos, defs_fpso=defs_fpso, sub_dup=sub_dup, valores=nums,
             vagas=vag, ingles=len(ING.findall(text)), glossario=len(gl), caps=len(caps))
    rows.append(r)
json.dump(rows, open(sys.argv[2], 'w'), ensure_ascii=False, indent=1)
for r in rows:
    print(r['id'], r['palavras'], r['blocos'], 'pend', r['siglas_pend'], r['pend'][:6], 'reexp', list(r['reexpandidas'].items())[:4],
          'meta', r['meta'], 'trav', r['travessao'], 'lint', r['lint'], 'long', r['longos'], 'curt', r['curtos'],
          'subdup', r['sub_dup'], 'val', r['valores'], 'ing', r['ingles'])
