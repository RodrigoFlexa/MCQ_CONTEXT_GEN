"""Monta o Google Apps Script do formulário de avaliação por especialista.

Seleciona N questões aprovadas por tópico (padrão 5: 1 fácil, 2 média, 1 difícil A, 1 difícil B; com 10: 3/4/2/1),
espalhadas pelos subtópicos, preferindo as que não foram corrigidas nem marcadas como repetidas.
Gera formulario_especialista.gs (dados embutidos) e o mapa código -> questão para analisar as respostas.

    python pipeline/qa_v7/formulario/montar_formulario.py \\
        --questoes pipeline/qa_v7/saida_cota_100_por_topico/questoes.jsonl --saida pipeline/qa_v7/formulario
"""
import argparse
import csv
import json
import random
import sys
from collections import defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from pipeline.qa_v7.gerar_qa import load_inventory, read_jsonl  # noqa: E402

# Mistura de tipos por tamanho do lote por tópico; outros tamanhos completam com médias.
MISTURAS = {5: (('facil', 1), ('media', 2), ('dificil_A', 1), ('dificil_B', 1)),
            10: (('facil', 3), ('media', 4), ('dificil_A', 2), ('dificil_B', 1))}
NIVEL = {'facil': 'Fácil', 'media': 'Média', 'dificil_A': 'Difícil (cenário em um conceito)',
         'dificil_B': 'Difícil (integra dois ou mais conceitos)'}
COLECAO = {'petroles': 'Petrolês', 'anp': 'ANP', 'hse': 'HSE (Reino Unido)', 'bsee': 'BSEE (EUA)', 'regis': 'REGIS'}
MAX_FATOS, MAX_CITACAO, MAX_CONTEXTO = 6, 320, 3800


def preferred(q):
    return not q['correcoes'] and not (q.get('novidade') or {}).get('redundante')


def select(rows, por_topico, seed):
    rng = random.Random(seed)
    ap = [q for q in rows if q.get('status') == 'aprovada']
    by_topic = defaultdict(list)
    for q in ap:
        by_topic[q['topico']].append(q)
    chosen = []
    for topic, qs in by_topic.items():
        picked, ids = [], set()
        subs = sorted({q['subtopico'] for q in qs})
        rng.shuffle(subs)
        cursor = 0
        mix = MISTURAS.get(por_topico, MISTURAS[10])
        plan = [t for t, n in mix for _ in range(n)]
        plan += ['media'] * max(0, por_topico - len(plan))
        for tipo in plan[:por_topico]:
            for pref in (True, False):
                done = False
                for k in range(len(subs)):
                    sub = subs[(cursor + k) % len(subs)]
                    pool = [q for q in qs if q['subtopico'] == sub and q['tipo'] == tipo and q['id'] not in ids
                            and (preferred(q) or not pref)]
                    if pool:
                        q = rng.choice(pool)
                        picked.append(q)
                        ids.add(q['id'])
                        cursor = (cursor + k + 1) % len(subs)
                        done = True
                        break
                if done:
                    break
        chosen += picked
    return chosen


def clip(text, n):
    text = ' '.join((text or '').split())
    return text if len(text) <= n else text[:n - 1].rstrip() + '…'


def context(q, notes_by_nid):
    lines = []
    for nid, title in zip(q['notas'], q['titulos_notas']):
        n = notes_by_nid.get(nid, {})
        lines.append(f'Nota técnica: {title}')
        if n.get('resumo'):
            lines.append(f"Resumo: {clip(n['resumo'], 500)}")
    lines.append(f"Conhecimento que a questão deveria avaliar: {clip(q['alvo_descricao'], 600)}")
    lines.append('')
    lines.append('Fatos das fontes usados na resposta (afirmação e trecho original):')
    for f in q['fontes'][:MAX_FATOS]:
        src = COLECAO.get(f.get('collection'), f.get('collection') or '')
        doc = f.get('title') or ''
        page = f", p. {f['page_ini']}" if f.get('page_ini') not in (None, '') else ''
        lines.append(f"• {clip(f['afirmacao'], 400)}")
        lines.append(f"  Trecho: \"{clip(f.get('citacao', ''), MAX_CITACAO)}\" [{src} · {clip(doc, 80)}{page}]")
    if len(q['fontes']) > MAX_FATOS:
        lines.append(f'(+{len(q["fontes"]) - MAX_FATOS} fatos não exibidos)')
    text = '\n'.join(lines)
    return text if len(text) <= MAX_CONTEXTO else text[:MAX_CONTEXTO - 1] + '…'


def main(argv=None):
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument('--questoes', default='pipeline/qa_v7/saida_cota_100_por_topico/questoes.jsonl')
    p.add_argument('--inventarios', nargs='+', default=[
        'pipeline/inventario/saida_sistemas_de_lastro_v4_notas', 'pipeline/inventario/saida_mais_4_topicos_v4_nano_low',
        'pipeline/inventario/saida_ultimos_5_topicos_v4_nano_low'])
    p.add_argument('--saida', default='pipeline/qa_v7/formulario')
    p.add_argument('--por-topico', type=int, default=5)
    p.add_argument('--seed', type=int, default=2026)
    a = p.parse_args(argv)
    out = Path(a.saida)
    out.mkdir(parents=True, exist_ok=True)
    rows = read_jsonl(a.questoes)
    notes = {n['nid']: n for s in load_inventory(a.inventarios) for n in s['notas']}
    chosen = select(rows, a.por_topico, a.seed)
    data = []
    for i, q in enumerate(chosen, 1):
        data.append({'codigo': f'Q{i:03d}', 'id': q['id'], 'topico': q['topico'], 'subtopico': q['subtopico'],
                     'nivel': NIVEL[q['tipo']], 'pergunta': q['pergunta'], 'resposta': q['resposta'],
                     'contexto': context(q, notes)})
    template = (Path(__file__).with_name('formulario_template.gs')).read_text(encoding='utf-8')
    payload = json.dumps(data, ensure_ascii=False, indent=1).replace('\u2028', '\\u2028').replace('\u2029', '\\u2029')
    (out / 'formulario_especialista.gs').write_text(template.replace('/*__QUESTOES__*/[]', payload), encoding='utf-8')
    with (out / 'mapa_questoes_formulario.csv').open('w', encoding='utf-8-sig', newline='') as f:
        w = csv.writer(f)
        w.writerow(['codigo', 'id', 'topico', 'subtopico', 'nivel', 'pergunta', 'resposta'])
        for d in data:
            w.writerow([d['codigo'], d['id'], d['topico'], d['subtopico'], d['nivel'], d['pergunta'], d['resposta']])
    counts = defaultdict(int)
    for d in data:
        counts[d['topico']] += 1
    print(f'{len(data)} questões -> {out / "formulario_especialista.gs"}')
    for t, n in counts.items():
        print(f'  {n:3d}  {t}')


if __name__ == '__main__':
    main()
