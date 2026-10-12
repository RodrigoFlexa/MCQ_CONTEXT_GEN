"""Etapa 6: fichas por assunto (Markdown + JSON) e relatório de cobertura."""
import csv
from pathlib import Path

from .textutil import atomic_json, write_jsonl, slug, sha

TIPO_LABEL = {'definicao': 'Definições', 'mecanismo': 'Mecanismos', 'causa_efeito': 'Causa e efeito',
              'procedimento': 'Procedimentos', 'criterio_limite': 'Critérios e limites',
              'formula_calculo': 'Fórmulas e cálculos', 'comparacao': 'Comparações',
              'requisito_normativo': 'Requisitos normativos', 'licao_incidente': 'Lições de incidentes', 'outro': 'Outros'}
APLIC_LABEL = {'fpso_direta': 'FPSO direta', 'transferivel': 'transferível', 'nao_aplicavel': 'não aplicável'}


# Modo de geração que a próxima fase deve usar para cada assunto.
MODO = {'ok': 'com_contexto', 'contexto_parcial': 'com_contexto_parcial', 'sem_contexto': 'sem_contexto',
        'generico': 'nao_gerar'}


def status_assunto(a, n_units, n_high):
    if a['generico']:
        return 'generico'
    if n_units == 0:
        return 'sem_contexto'   # limitação dos corpora: gerar só com conhecimento do modelo
    if n_units < 3 or n_high == 0:
        return 'contexto_parcial'
    return 'ok'


def _src(f):
    page = ''
    if f.get('page_ini') is not None:
        page = f" p.{f['page_ini']}" + (f"-{f['page_fim']}" if f.get('page_fim') not in (None, f['page_ini']) else '')
    title = f.get('title') or f.get('document_id')
    return f"{f['collection']}: {title}{page}"


def render_ficha(sub, a, units, sel_info):
    lines = [f"# {a['id']} · {sub['subtopico']}", '',
             f"**Assunto (redação do especialista):** {a['texto']}", '',
             f"Tópico: {sub['topico']}  ",
             f"Consulta: {a['consulta_pt']} / {a['consulta_en']}  ",
             f"Trechos: {sel_info.get('candidatos', 0)} candidatos, {sel_info.get('selecionados', 0)} selecionados "
             f"({', '.join(sel_info.get('colecoes', [])) or '—'})  ",
             f"Unidades consolidadas: {len(units)} ({sum(u['valor'] == 'alto' for u in units)} de alto valor, "
             f"{sum(u['status'] == 'corroborada' for u in units)} corroboradas, "
             f"{sum(u['status'] == 'conflito' for u in units)} conflitos)", '']
    conflicts = [u for u in units if u['status'] in ('conflito', 'condicoes_diferentes')]
    if conflicts:
        lines += ['## ⚠ Divergências entre fontes', '']
        for u in conflicts:
            lines.append(f"- **[{u['cid'].split(':')[-1]}] {u['status']}:** {u['nota'] or u['afirmacao']}")
            for f in u['fontes']:
                lines.append(f"  - {_src(f)}: {f.get('citacao', '')}")
            for original in u.get('unidades_originais', []):
                lines.append(f"  - Afirmação original: {original['afirmacao']} (condições: {original['condicoes']})")
        lines.append('')
    by_tipo = {}
    for u in units:
        if u['status'] == 'conflito':
            continue
        by_tipo.setdefault(u['tipo'], []).append(u)
    for tipo in TIPO_LABEL:
        group = by_tipo.get(tipo)
        if not group:
            continue
        lines += [f"## {TIPO_LABEL[tipo]}", '']
        for u in sorted(group, key=lambda u: (u['valor'] != 'alto', -u['n_documentos'], u['cid'])):
            tag = [u['valor'], APLIC_LABEL.get(u['aplicabilidade'], u['aplicabilidade'])]
            if u['n_documentos'] > 1:
                tag.append(f"{u['n_documentos']} documentos")
            lines.append(f"- **[{u['cid'].split(':')[-1]}]** {u['afirmacao']} _({' · '.join(tag)})_")
            if u['condicoes']:
                lines.append(f"  - Condições: {u['condicoes']}")
            for f in u['fontes'][:3]:
                lines.append(f"  - Fonte: {_src(f)} — \"{f.get('citacao', '')}\"")
        lines.append('')
    if not any(u['status'] != 'conflito' for u in units):
        lines += ['_Nenhuma unidade utilizável foi encontrada nos corpora para este assunto. '
                  'Ele fica indicado como **sem_contexto** para a futura geração de QA. '
                  'Este inventário não gera perguntas nem comprova as afirmações de um modelo sem fontes._', '']
    return '\n'.join(lines)


def write_subtopic(out_dir, sub, assuntos, consolidated, selections, extraction_stats):
    d = Path(out_dir)
    rows = []
    for a in assuntos:
        units = [u for u in consolidated if a['id'] in u['assuntos']]
        sel = selections.get(a['id'], {}).get('info', {})
        usable = [u for u in units if u['status'] != 'conflito']
        n_high = sum(u['valor'] == 'alto' for u in usable)
        st = status_assunto(a, len(usable), n_high)
        rows.append({'topico': sub['topico'], 'subtopico': sub['subtopico'], 'assunto_id': a['id'],
                     'assunto': a['texto'], 'generico': a['generico'], 'literal': a['literal'],
                     'candidatos': sel.get('candidatos', 0), 'trechos_selecionados': sel.get('selecionados', 0),
                     'rerank_max': sel.get('rerank_max'), 'colecoes': '|'.join(sel.get('colecoes', [])),
                     'unidades': len(usable), 'alto_valor': n_high,
                     'corroboradas': sum(u['status'] == 'corroborada' for u in units),
                     'conflitos': sum(u['status'] == 'conflito' for u in units),
                     'fpso_direta': sum(u['aplicabilidade'] == 'fpso_direta' for u in units), 'status': st,
                     'modo_geracao': MODO[st], 'sub_dir': d.name,
                     'ficha': f"subtopicos/{d.name}/fichas/{a['id']}.json" if not a['generico'] else None})
        if not a['generico']:
            (d / 'fichas').mkdir(parents=True, exist_ok=True)
            (d / 'fichas' / f"{a['id']}.md").write_text(render_ficha(sub, a, units, sel), encoding='utf-8')
            atomic_json(d / 'fichas' / f"{a['id']}.json", {'subtopico': {k: sub.get(k) for k in ('key', 'topico', 'subtopico', 'frase')},
                                                          'assunto': a, 'status': st, 'modo_geracao': MODO[st],
                                                          'selecao': sel, 'unidades': usable,
                                                          'divergencias': [u for u in units if u['status'] == 'conflito']})
    write_jsonl(d / 'unidades_consolidadas.jsonl', consolidated)
    resumo = ['# ' + sub['subtopico'], '', f"Tópico: {sub['topico']}", '',
              '| Assunto | Status | Trechos | Unidades | Alto valor | Corrob. | Conflitos | Coleções |',
              '|---|---|---:|---:|---:|---:|---:|---|']
    for r in rows:
        resumo.append(f"| {r['assunto_id']}: {r['assunto'][:90]} | {r['status']} | {r['trechos_selecionados']} | {r['unidades']} | "
                      f"{r['alto_valor']} | {r['corroboradas']} | {r['conflitos']} | {r['colecoes']} |")
    resumo += ['', f"Extração: {extraction_stats}"]
    (d / 'README.md').write_text('\n'.join(resumo), encoding='utf-8')
    return rows


def write_coverage(out_dir, rows):
    out_dir = Path(out_dir)
    if not rows:
        return
    with (out_dir / 'cobertura.csv').open('w', encoding='utf-8-sig', newline='') as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0]))
        w.writeheader()
        w.writerows(rows)
    subs = {}
    for r in rows:
        subs.setdefault((r['topico'], r['subtopico']), []).append(r)
    lines = ['# Cobertura do inventário', '',
             '| Tópico | Subtópico | Assuntos | com contexto | contexto parcial | sem contexto | genérico | Unidades | Alto valor | Conflitos |',
             '|---|---|---:|---:|---:|---:|---:|---:|---:|---:|']
    for (t, s), rs in subs.items():
        c = lambda st: sum(r['status'] == st for r in rs)
        lines.append(f"| {t} | {s} | {len(rs)} | {c('ok')} | {c('contexto_parcial')} | {c('sem_contexto')} | {c('generico')} | "
                     f"{sum(r['unidades'] for r in rs)} | {sum(r['alto_valor'] for r in rs)} | {sum(r['conflitos'] for r in rs)} |")
    lacunas = [r for r in rows if r['status'] == 'sem_contexto']
    if lacunas:
        lines += ['', '## Assuntos que serão gerados sem contexto (sem trechos nos corpora)', '']
        lines += [f"- {r['subtopico']} / {r['assunto_id']}: {r['assunto']}" for r in lacunas]
    (out_dir / 'cobertura.md').write_text('\n'.join(lines), encoding='utf-8')


def write_generation_index(out_dir, rows):
    """Índice consumido pela fase de geração: um registro por assunto gerável."""
    keep = ('topico', 'subtopico', 'assunto_id', 'assunto', 'modo_geracao', 'unidades', 'alto_valor', 'ficha')
    write_jsonl(Path(out_dir) / 'assuntos_para_geracao.jsonl',
                [{k: r[k] for k in keep} for r in rows if r['modo_geracao'] != 'nao_gerar'])


def write_topic_documents(out_dir, rows):
    """Reúne as fichas em um documento por tópico, sem síntese adicional do LLM."""
    out_dir = Path(out_dir)
    groups = {}
    for r in rows:
        if not r['generico']:
            groups.setdefault(r['topico'], []).append(r)
    index = []
    for topic, rs in groups.items():
        doc_dir = out_dir / 'topicos' / (slug(topic) + '-' + sha(topic, 8))
        doc_dir.mkdir(parents=True, exist_ok=True)
        parts = [f'# Documento técnico: {topic}', '',
                 'Inventário para curadoria antes da geração de QA. Citações verificadas literalmente; '
                 'a correspondência textual não comprova corretude técnica. Conflitos são separados '
                 'das unidades utilizáveis. Assuntos sem evidência permanecem identificados.', '']
        for r in rs:
            ficha_md = out_dir / Path(r['ficha']).with_suffix('.md')
            parts.extend([f"## {r['subtopico']} / {r['assunto_id']} — {r['status']}", '',
                          ficha_md.read_text(encoding='utf-8').replace('# ', '### ', 1), ''])
        path = doc_dir / 'documento_tecnico.md'
        tmp = path.with_suffix('.md.tmp')
        tmp.write_text('\n'.join(parts), encoding='utf-8')
        tmp.replace(path)
        index.append({'topico': topic, 'assuntos': len(rs), 'arquivo': path.relative_to(out_dir).as_posix()})
    atomic_json(out_dir / 'documentos_topicos.json', index)
