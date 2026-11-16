"""Converte a revisão do especialista (.docx) em entradas do refino.

Uso, na raiz do repositório:

    python -m pipeline.qa_research.refino.preparar_entradas \
        --docx "Comentários especialista/Documento de Contexto - revisão especialista 2026-11-16"

Cada entrada reúne, para um documento:
- a base: texto revisado pelo especialista, sem o comentário final, sem os trechos
  que ele mandou remover/descartar e sem os comentários escritos no corpo;
- as anotações de bloco (trecho fora do contexto FPSO, trecho realçado sem instrução);
- o feedback: comentário literal, comentários no corpo, análise por LLM anexada,
  lacunas enumeradas (codificação em dados/metricas_feedback_especialista.json),
  nível de encaminhamento e categorias de problema.

Não chama modelos nem rede. A saída é determinística e versionada no Git.
"""
import argparse
import hashlib
import json
import re
import unicodedata
import zipfile
from pathlib import Path
from xml.etree import ElementTree as ET

W = '{http://schemas.openxmlformats.org/wordprocessingml/2006/main}'
HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
SCHEMA = 'refino-entrada-v1'
COMMENT = re.compile(r'^Coment[aá]rios? Mazzuco:\s*')
INLINE_COMMENT = re.compile(r'^Coment[aá]rio:\s*')
REMOVE = re.compile(r'\(?\s*(?:remover|descartar) este trecho\s*\)?\.?', re.I)
OUT_OF_CONTEXT = '(fora do contexto FPSO)'
# Substituições automáticas do especialista que produziram erro evidente no 9.2.
# Mantidas fora do texto do especialista em correcoes_automaticas para auditoria.
FIXES = {
    '09_02': [
        ('homem de áreaes', 'homens de área', 'plural quebrado pela troca eslingadores → homem de área'),
        ('mais de um guindasteiro para conexão e desconexão', 'mais de um homem de área para conexão e desconexão',
         'troca eslingador → guindasteiro neste ponto contradiz a função (conexão e desconexão é feita pelo homem de área)'),
        ('“estilingadas"', '“estilingadas”', 'aspas desbalanceadas; termo de bordo mantido como o especialista escreveu'),
    ],
}


def norm(text):
    return re.sub(r'\s+', ' ', unicodedata.normalize('NFC', (text or '').replace(' ', ' '))).strip()


def file_hash(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def item_id(name):
    a, b = re.match(r'(\d+)\.(\d+)\.', name).groups()
    return f'{int(a):02d}_{int(b):02d}'


def runs(paragraph):
    out = []
    for run in paragraph.iter(W + 'r'):
        text = ''.join(t.text or '' for t in run.iter(W + 't'))
        props = run.find(W + 'rPr')
        marked = False
        if props is not None:
            hl, color = props.find(W + 'highlight'), props.find(W + 'color')
            marked = ((hl is not None and hl.get(W + 'val') == 'yellow')
                      or (color is not None and color.get(W + 'val', '').lower() == 'ff0000'))
        out.append((text, marked))
    return out


def style(paragraph):
    node = paragraph.find(W + 'pPr/' + W + 'pStyle')
    return node.get(W + 'val') if node is not None else ''


def cell_text(cell):
    return norm(' '.join(''.join(t.text or '' for t in p.iter(W + 't')) for p in cell.iter(W + 'p')))


def table_rows(table):
    return [[cell_text(c) for c in row.findall(W + 'tc')] for row in table.findall(W + 'tr')]


def markdown_table(rows):
    if not rows:
        return ''
    width = max(len(r) for r in rows)
    rows = [r + [''] * (width - len(r)) for r in rows]
    esc = lambda s: s.replace('|', '\\|')
    lines = ['| ' + ' | '.join(map(esc, rows[0])) + ' |', '|' + '---|' * width]
    lines += ['| ' + ' | '.join(map(esc, r)) + ' |' for r in rows[1:]]
    return '\n'.join(lines)


def parse_docx(path, item):
    body = ET.fromstring(zipfile.ZipFile(path).read('word/document.xml')).find(W + 'body')
    items = [('p', e) if e.tag == W + 'p' else ('t', e) for e in body if e.tag in (W + 'p', W + 'tbl')]
    start = next((i for i, (k, e) in enumerate(items)
                  if k == 'p' and COMMENT.match(norm(''.join(t for t, _ in runs(e))))), len(items))
    title, group, chapters, removed, inline = None, None, [], [], []
    chapter = block = None
    counter = 0

    def new_block(subtitle):
        nonlocal block, counter
        counter += 1
        block = dict(id=f'B{counter:03d}', subtitulo=subtitle, paragrafos=[], anotacoes=[], descartar=False)
        chapter['blocos'].append(block)

    for kind, element in items[:start]:
        if kind != 'p':
            continue
        parts = runs(element)
        text = norm(''.join(t for t, _ in parts))
        if not text:
            continue
        kind_style = style(element).lower()
        marked = norm(' '.join(t for t, m in parts if m))
        whole = all(m or not t.strip() for t, m in parts)
        if kind_style == 'title':
            title = text
            continue
        if kind_style == 'heading1':
            group = text
            continue
        if kind_style == 'heading2':
            chapter = dict(titulo=text, grupo=group, blocos=[])
            chapters.append(chapter)
            block = None
            continue
        if chapter is None:
            chapter = dict(titulo=group or title, grupo=group, blocos=[])
            chapters.append(chapter)
        if kind_style == 'heading3':
            new_block(text)
            if whole and marked:
                block['anotacoes'].append(dict(tipo='destacado_sem_instrucao', trecho=text))
            continue
        if block is None:
            new_block(chapter['titulo'])
        if INLINE_COMMENT.match(text):
            inline.append(dict(bloco=block['id'], secao=block['subtitulo'], texto=INLINE_COMMENT.sub('', text)))
            continue
        if 'descartar este trecho' in text.lower():
            # O bloco inteiro sai da base; o registro é feito uma vez, no fechamento.
            block['descartar'] = True
            block['paragrafos'].append(norm(REMOVE.sub('', text)))
            continue
        if 'remover este trecho' in text.lower():
            kept = norm(''.join(t for t, m in parts if not m))
            removed.append(dict(tipo='remover', bloco=block['id'], secao=block['subtitulo'],
                                texto=norm(REMOVE.sub('', marked))))
            if kept:
                block['paragrafos'].append(kept)
            continue
        if OUT_OF_CONTEXT in text:
            block['anotacoes'].append(dict(tipo='fora_contexto_fpso',
                                           trecho=norm(marked.replace(OUT_OF_CONTEXT, ''))))
            text = norm(text.replace(OUT_OF_CONTEXT, ''))
        elif whole and marked and len(text) > 40:
            block['anotacoes'].append(dict(tipo='destacado_sem_instrucao', trecho=text))
        block['paragrafos'].append(text)
    for chapter_row in chapters:
        for row in chapter_row['blocos']:
            if row['descartar']:
                removed.append(dict(tipo='descartar', bloco=row['id'], secao=row['subtitulo'],
                                    texto=' '.join(row['paragrafos'])))
        chapter_row['blocos'] = [dict(id=b['id'], subtitulo=b['subtitulo'], texto='\n\n'.join(b['paragrafos']),
                                      anotacoes=b['anotacoes'])
                                 for b in chapter_row['blocos'] if not b['descartar'] and b['paragrafos']]
    chapters = [c for c in chapters if c['blocos']]
    applied = []
    for old, new, why in FIXES.get(item, []):
        for c in chapters:
            for b in c['blocos']:
                if old in b['texto']:
                    b['texto'] = b['texto'].replace(old, new)
                    applied.append(dict(bloco=b['id'], antes=old, depois=new, motivo=why))
    # Comentário final: prosa do especialista e material de LLM anexado por ele.
    prose, llm_md, tables = [], [], []
    in_llm = False
    for index, (kind, element) in enumerate(items[start:]):
        if kind == 't':
            in_llm = True
            rows = table_rows(element)
            tables.append(rows)
            llm_md.append(markdown_table(rows))
            continue
        text = norm(''.join(t for t, _ in runs(element)))
        if not text:
            continue
        if index == 0:
            text = COMMENT.sub('', text)
        heading = style(element).lower().startswith('heading')
        if item == '01_01' and index >= 2:
            in_llm = True
        if heading:
            in_llm = True
        (llm_md if in_llm else prose).append(('#### ' + text) if heading else text)
    return dict(titulo=title, capitulos=chapters), removed, inline, prose, '\n\n'.join(llm_md), tables, applied


def llm_gaps(item, tables, llm_markdown):
    """Linhas das tabelas de lacunas por LLM anexadas pelo especialista."""
    gaps = []
    for rows in tables:
        if not rows:
            continue
        header = rows[0]
        for row in rows[1:]:
            if row == header or row[0] in ('Nº', 'KPI', 'Tema'):
                continue
            if 'Situação' in header:
                get = lambda name: row[header.index(name)] if name in header and header.index(name) < len(row) else ''
                gaps.append(dict(topico=get('Tópico'), situacao=get('Situação'),
                                 aspectos=get('Aspectos que deveriam ser incluídos')))
            elif header[0] == 'Tema':
                gaps.append(dict(topico=row[0], situacao='Parcialmente abordado',
                                 aspectos=row[2] if len(row) > 2 else '', cobre=row[1] if len(row) > 1 else ''))
    if item == '01_01':
        for match in re.finditer(r'^(\d+)\. ([^:]+): (.+)$', llm_markdown, re.M):
            if match[1] in ('10', '14', '17'):
                gaps.insert(len([g for g in gaps if g['situacao'] == 'Não abordado']),
                            dict(topico=match[2], situacao='Não abordado', aspectos=match[3]))
    return [dict(id=f'L{i:02d}', **g) for i, g in enumerate(gaps, 1)]


def build(docx_dir, metrics_path, output):
    metrics = {d['id']: d for d in json.loads(Path(metrics_path).read_text(encoding='utf-8'))['por_documento']}
    from pipeline.fase_3.topicos import TOPICOS
    topics = {}
    for ai, (area, subjects) in enumerate(TOPICOS.items(), 1):
        for si, (subject, phrase) in enumerate(subjects.items(), 1):
            topics[f'{ai:02}_{si:02}'] = dict(topico=area, subtopico=subject, frase_especialista=phrase)
    files = sorted(Path(docx_dir).rglob('*.docx'), key=lambda p: [int(x) for x in item_id(p.name).split('_')])
    output = Path(output)
    output.mkdir(parents=True, exist_ok=True)
    index = []
    for path in files:
        item = item_id(path.name)
        base, removed, inline, prose, llm_markdown, tables, applied = parse_docx(path, item)
        m = metrics[item]
        v2 = ROOT / 'pipeline/qa_research/relatorios/dez_areas_final_v2' / item / 'documento.json'
        entry = dict(schema=SCHEMA, id=item, titulo=base['titulo'], area=int(item[:2]), **topics[item],
            origem=dict(docx=path.name, docx_sha256=file_hash(path),
                        base_v2=v2.relative_to(ROOT).as_posix() if v2.is_file() else None,
                        base_v2_sha256=file_hash(v2) if v2.is_file() else None,
                        revisao='Mazzuco, devolvida em 16/11/2026'),
            base=base, removidos=removed, correcoes_automaticas=applied,
            feedback=dict(comentario=prose, comentarios_no_corpo=inline, analise_llm=llm_markdown,
                lacunas=[dict(id=f'G{i:02d}', descricao=d) for i, d in enumerate(m['lacunas_listadas'], 1)],
                lacunas_llm=llm_gaps(item, tables, llm_markdown), nivel=m['nivel'], nivel_nome=m['nivel_nome'],
                problemas=m['codigos'], evidencia_inadequacao=m['evidencia_inadequacao']))
        target = output / f'{item}.json'
        target.write_text(json.dumps(entry, ensure_ascii=False, indent=1) + '\n', encoding='utf-8')
        blocks = sum(len(c['blocos']) for c in base['capitulos'])
        index.append(dict(id=item, titulo=base['titulo'], blocos=blocks, removidos=len(removed),
                          lacunas=len(entry['feedback']['lacunas']), lacunas_llm=len(entry['feedback']['lacunas_llm']),
                          nivel=m['nivel'], sha256=file_hash(target)))
    (output / 'indice.json').write_text(json.dumps(dict(schema=SCHEMA, documentos=index), ensure_ascii=False, indent=1) + '\n',
                                        encoding='utf-8')
    return index


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument('--docx', type=Path, required=True, help='Pasta com os 40 .docx revisados (busca recursiva)')
    parser.add_argument('--metricas', type=Path, default=HERE / 'dados/metricas_feedback_especialista.json')
    parser.add_argument('--output', type=Path, default=HERE / 'entradas')
    args = parser.parse_args(argv)
    index = build(args.docx, args.metricas, args.output)
    for row in index:
        print(row['id'], row['blocos'], 'blocos |', row['lacunas'], 'lacunas +', row['lacunas_llm'], 'LLM |',
              row['removidos'], 'removidos')
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
