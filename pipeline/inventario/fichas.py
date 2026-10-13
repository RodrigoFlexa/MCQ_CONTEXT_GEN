"""Etapa final: documentos (Markdown), índices para a geração de QA e relatório de cobertura."""
import csv
from collections import Counter
from pathlib import Path

from .textutil import atomic_json, slug, sha, write_jsonl

# Modo de geração que a fase de QA deve usar para cada assunto.
MODO = {'com_contexto': 'com_contexto', 'sem_contexto': 'sem_contexto', 'incompleto': 'reprocessar',
        'generico': 'nao_gerar'}
NIVEL = {'facil': 'fácil', 'media': 'média', 'dificil': 'difícil'}


def _src_label(f):
    page = f" p.{f['page_ini']}" if f.get('page_ini') is not None else ''
    jur = f" ({f['jurisdiction']})" if f.get('jurisdiction') not in (None, '', 'not_specified') else ''
    return f"{f.get('collection')}: {f.get('title') or f.get('document_id')}{page}{jur}"


def render_note(n, level=3):
    h = '#' * level
    refs, order = {}, []

    def ref(fid):
        if fid not in refs:
            refs[fid] = len(refs) + 1
            order.append(fid)
        return refs[fid]
    lines = [f"{h} {n['titulo']}", '', f"_{n['resumo']}_", '']
    for s in n['secoes']:
        if s['conhecimento_geral']:
            lines += [f"**{s['titulo']}** _(conhecimento técnico geral, não extraído das fontes)_: {s['texto']}", '']
        else:
            marks = ''.join(f"[{ref(f)}]" for f in s['fatos'])
            lines += [f"**{s['titulo']}.** {s['texto']} {marks}".rstrip(), '']
    if n['alvos']:
        lines += ['**Conhecimentos avaliáveis**', '']
        lines += [f"- ({NIVEL[a['nivel']]}) {a['descricao']}" for a in n['alvos']]
        lines.append('')
    if n.get('correcoes'):
        lines += ['**Correções de terminologia/conceito em relação às fontes**', '']
        lines += [f"- {c.get('original', '')} → {c.get('corrigido', '')}: {c.get('motivo', '')}" for c in n['correcoes']]
        lines.append('')
    if order:
        lines += ['**Fontes**', '']
        for fid in order:
            f = n['fontes'].get(fid, {})
            if f.get('tipo') == 'trecho':
                lines.append(f"{refs[fid]}. {_src_label(f)} (trecho completo)")
            else:
                lines.append(f"{refs[fid]}. {_src_label(f)}: \"{f.get('citacao', '')}\"")
        lines.append('')
    av = (n.get('revisao') or {}).get('avaliacao') or {}
    lines += [f"<sub>Nota {n['nid']} · revisão: {(n.get('revisao') or {}).get('decisao', 'sem revisão')} · "
              + ', '.join(f"{k}={v}" for k, v in av.items()) + f" · {n['metricas']['palavras']} palavras</sub>", '']
    return '\n'.join(lines)


def assunto_status(a, approved, incomplete):
    if a['generico']:
        return 'generico'
    if approved:
        return 'com_contexto'
    if incomplete:
        return 'incompleto'
    return 'sem_contexto'


def write_subtopic(d, sub, assuntos, selections, facts, plans, notes, failed_assuntos, combos=()):
    """Documento do subtópico e linhas de cobertura por assunto."""
    d = Path(d)
    approved = [n for n in notes if n['status'] == 'aprovada']
    write_jsonl(d / 'notas_aprovadas.jsonl', approved)
    write_jsonl(d / 'notas.jsonl', notes)
    rows = []
    doc = [f"# {sub['subtopico']}", '', f"Tópico: {sub['topico']}", '',
           f"> Frase do especialista: {sub['frase']}", '']
    for a in assuntos:
        mine = [n for n in approved if a['id'] in n['assuntos']]
        others = [n for n in notes if a['id'] in n['assuntos'] and n['status'] != 'aprovada']
        sel = (selections.get(a['id']) or {}).get('info', {})
        plan = plans.get(a['id']) or {}
        st = assunto_status(a, mine, a['id'] in failed_assuntos)
        n_facts = sum(a['id'] in f['assuntos'] for f in facts)
        rows.append({'topico': sub['topico'], 'subtopico': sub['subtopico'], 'assunto_id': a['id'], 'assunto': a['texto'],
                     'status': st, 'modo_geracao': MODO[st], 'trechos': sel.get('selecionados', 0),
                     'colecoes_trechos': '|'.join(f"{k}:{v}" for k, v in sorted((sel.get('colecoes') or {}).items())),
                     'fatos': n_facts, 'conceitos': len(plan.get('conceitos', [])),
                     'notas_aprovadas': len(mine), 'notas_reprovadas': sum(n['status'] == 'reprovada' for n in others),
                     'notas_insuficientes': sum(n['status'] == 'insuficiente' for n in others),
                     'notas_falhas': sum(n['status'] in ('falhou', 'filtrada') for n in others),
                     'palavras': sum(n['metricas']['palavras'] for n in mine),
                     'alvos_dificeis': sum(n['metricas']['alvos']['dificil'] for n in mine),
                     'notas': [n['nid'] for n in mine], 'sub_dir': d.name})
        if a['generico']:
            continue
        doc += [f"## {a['id']} · {a['texto']}", '']
        if not mine:
            doc += [{'sem_contexto': '_Sem material nos corpora que sustente uma nota técnica. Assunto marcado para '
                                     'geração **sem contexto**._',
                     'incompleto': '_Processamento incompleto (falha registrada em ocorrencias.jsonl). '
                                   'Repita o comando para reprocessar._'}[st], '']
        for n in mine:
            doc.append(render_note(n, 3))
    if combos:
        titles = {n['nid']: n['titulo'] for n in approved}
        doc += ['## Combinações para questões difíceis (tipo B)', '',
                '_Conceitos que interagem numa situação real; a pergunta exige integrá-los._', '']
        for c in combos:
            doc += [f"### {c['titulo']}", '', f"**Notas:** {'; '.join(titles.get(n, n) for n in c['notas'])}  ",
                    f"**Ligação:** {c['ligacao']}  ", f"**Raciocínio exigido:** {c['raciocinio']}  ",
                    f"**Cenário:** {c['cenario']}", '']
    (d / 'documento.md').write_text('\n'.join(doc), encoding='utf-8')
    readme = [f"# {sub['subtopico']}", '', '| Assunto | Status | Trechos | Fatos | Conceitos | Notas | Palavras | Coleções |',
              '|---|---|---:|---:|---:|---:|---:|---|']
    for r in rows:
        readme.append(f"| {r['assunto_id']}: {r['assunto'][:80]} | {r['status']} | {r['trechos']} | {r['fatos']} | "
                      f"{r['conceitos']} | {r['notas_aprovadas']} | {r['palavras']} | {r['colecoes_trechos']} |")
    (d / 'README.md').write_text('\n'.join(readme) + '\n', encoding='utf-8')
    return rows


def write_coverage(out_dir, rows):
    out_dir = Path(out_dir)
    if not rows:
        return
    fields = [k for k in rows[0] if k != 'notas']
    with (out_dir / 'cobertura.csv').open('w', encoding='utf-8-sig', newline='') as f:
        w = csv.DictWriter(f, fieldnames=fields, extrasaction='ignore')
        w.writeheader()
        w.writerows(rows)
    subs = {}
    for r in rows:
        subs.setdefault((r['topico'], r['subtopico']), []).append(r)
    lines = ['# Cobertura do inventário', '',
             '| Subtópico | Assuntos | com contexto | sem contexto | incompleto | Notas | Palavras | Alvos difíceis |',
             '|---|---:|---:|---:|---:|---:|---:|---:|']
    for (t, s), rs in subs.items():
        c = Counter(r['status'] for r in rs)
        lines.append(f"| {s} | {len(rs) - c['generico']} | {c['com_contexto']} | {c['sem_contexto']} | {c['incompleto']} | "
                     f"{sum(r['notas_aprovadas'] for r in rs)} | {sum(r['palavras'] for r in rs)} | "
                     f"{sum(r['alvos_dificeis'] for r in rs)} |")
    for label, st in (('Assuntos que serão gerados sem contexto', 'sem_contexto'),
                      ('Assuntos incompletos (repita o comando)', 'incompleto')):
        sel = [r for r in rows if r['status'] == st]
        if sel:
            lines += ['', f'## {label}', ''] + [f"- {r['subtopico']} / {r['assunto_id']}: {r['assunto']}" for r in sel]
    (out_dir / 'cobertura.md').write_text('\n'.join(lines) + '\n', encoding='utf-8')


def write_generation_index(out_dir, rows):
    keep = ('topico', 'subtopico', 'assunto_id', 'assunto', 'modo_geracao', 'notas', 'sub_dir')
    write_jsonl(Path(out_dir) / 'assuntos_para_geracao.jsonl',
                [{k: r[k] for k in keep} for r in rows if r['modo_geracao'] != 'nao_gerar'])


def write_topic_documents(out_dir, subs):
    """Um documento por tópico: concatenação dos documentos dos subtópicos, na ordem do especialista."""
    out_dir = Path(out_dir)
    by_topic = {}
    for s in subs:
        by_topic.setdefault(s['topico'], []).append(s)
    index = []
    for topic, ss in by_topic.items():
        doc_dir = out_dir / 'topicos' / (slug(topic) + '-' + sha(topic, 8))
        doc_dir.mkdir(parents=True, exist_ok=True)
        parts = [f'# Documento técnico: {topic}', '',
                 'Notas técnicas por conceito, escritas a partir de fatos com citação literal e revisadas por modelo. '
                 'Trechos marcados como conhecimento técnico geral não foram extraídos das fontes. '
                 'Revisão por modelo não equivale a certificação por especialista.', '']
        for s in ss:
            path = out_dir / 'subtopicos' / s['dir'] / 'documento.md'
            if path.exists():
                body = path.read_text(encoding='utf-8').split('\n')
                parts += ['#' + line if line.startswith('#') else line for line in body]
                parts.append('')
        target = doc_dir / 'documento_tecnico.md'
        tmp = target.with_suffix('.md.tmp')
        tmp.write_text('\n'.join(parts), encoding='utf-8')
        tmp.replace(target)
        index.append({'topico': topic, 'subtopicos': len(ss), 'arquivo': target.relative_to(out_dir).as_posix()})
    atomic_json(out_dir / 'documentos_topicos.json', index)
