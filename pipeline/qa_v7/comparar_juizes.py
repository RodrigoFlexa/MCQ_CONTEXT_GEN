"""Compara juízes sobre as mesmas questões e sobre versões com defeitos plantados.

1. Lê as questões geradas por gerar_qa.py e usa a versão ORIGINAL do gerador (antes de correções),
   para que todos os juízes recebam exatamente o mesmo item.
2. Para uma amostra, um modelo cria três versões defeituosas de cada questão:
   erro_tecnico (relação ou conclusão errada), sem_suporte (afirmação plausível que o material não
   sustenta) e dependencia_fonte (pergunta que só se responde conhecendo um caso ou documento).
3. Cada juiz avalia cada item isoladamente, com o mesmo material (notas + fatos com citação).

Métricas por juiz: aprovação das originais, detecção de cada tipo de defeito, se a verificação que
reprovou é a esperada, concordância entre juízes e uso de tokens. As originais em que os juízes
discordam ficam listadas para o especialista decidir.

    python -u pipeline/qa_v7/comparar_juizes.py --inventarios ... --questoes SAIDA/questoes.jsonl \\
        --saida SAIDA/juizes --juizes gpt-5-2-petrobras:medium o3-petrobras:medium gpt-5-4-petrobras:medium
"""
import argparse
import json
import random
import sys
import time
from collections import Counter, defaultdict
from concurrent.futures import ThreadPoolExecutor, as_completed
from itertools import combinations
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from pipeline.inventario.llm import CallFailed, ContentFiltered, load_dotenv  # noqa: E402
from pipeline.inventario.textutil import atomic_json, write_jsonl  # noqa: E402
from pipeline.qa_v7.gerar_qa import (TIPOS, failed_checks, judge_items, load_inventory, make_client, material,  # noqa: E402
                                     parse_role, read_jsonl, verdict_ok)

VERSION = 'comparar-juizes-v1'
DEFEITOS = ('erro_tecnico', 'sem_suporte', 'dependencia_fonte')
ESPERADO = {'erro_tecnico': {'correcao_tecnica', 'suporte'}, 'sem_suporte': {'suporte'},
            'dependencia_fonte': {'autonomia'}}

DEFECT_SYSTEM = """Você prepara um teste de juízes de questões técnicas de FPSO/FSO. Recebe o material (notas e fatos F#) e uma questão correta. Produza três versões DEFEITUOSAS da questão, cada uma com exatamente UM defeito, mantendo estilo, tamanho e tom; o defeito deve ser plausível para um leitor apressado, não grosseiro.
- erro_tecnico: altere a RESPOSTA para conter um erro técnico (inverta uma relação de causa e efeito, troque um critério ou chegue à conclusão errada). A pergunta não muda.
- sem_suporte: mantenha a resposta correta e ACRESCENTE uma afirmação específica e plausível (valor, norma, prazo ou procedimento) que o material NÃO sustenta. A pergunta não muda.
- dependencia_fonte: reescreva a PERGUNTA para que só possa ser respondida por quem conhece um estudo, caso, relatório ou documento específico (ex.: "no caso de ... relatado", "conforme a análise de risco de 2019"), sem usar as palavras "texto", "trecho" ou "segundo o material". A resposta pode ser ajustada de forma coerente.
Os campos "fatos" permanecem os da questão original. Descreva em "defeito" exatamente o que foi alterado.

Retorne JSON: {"erro_tecnico":{"pergunta":"...","resposta":"...","defeito":"..."},"sem_suporte":{...},"dependencia_fonte":{...}}"""


def kappa(a, b):
    n = len(a)
    if not n:
        return None
    po = sum(x == y for x, y in zip(a, b)) / n
    pa, pb = sum(a) / n, sum(b) / n
    pe = pa * pb + (1 - pa) * (1 - pb)
    return round((po - pe) / (1 - pe), 3) if pe < 1 else 1.0


def item_material(subs_by_key, q):
    sub = subs_by_key[q['sub_key']]
    by_nid = {n['nid']: n for n in sub['notas']}
    notes = [by_nid[n] for n in q['notas']]
    alvo = {'aid': q['alvo'], 'tipo': q['tipo'], 'descricao': q['alvo_descricao']}
    return material(sub, notes, [alvo], with_quotes=True)[1]


def base_item(q):
    orig = q.get('original') or {}
    return {'id': f"{q['id']}::original", 'qid': q['id'], 'variante': 'original', 'alvo': q['alvo'], 'tipo': q['tipo'],
            'pergunta': orig.get('pergunta', q['pergunta']), 'resposta': orig.get('resposta', q['resposta']),
            'fatos': orig.get('fatos', q['fatos']), 'topico': q['topico'], 'subtopico': q['subtopico'],
            'status_geracao': q['status']}


def make_defects(llm, mat, item):
    def check(data):
        for k in DEFEITOS:
            v = data.get(k)
            if not isinstance(v, dict) or not all(isinstance(v.get(f), str) and v[f].strip() for f in ('pergunta', 'resposta')):
                raise ValueError(f'"{k}" precisa de pergunta e resposta')
            if v['pergunta'].strip() == item['pergunta'] and v['resposta'].strip() == item['resposta']:
                raise ValueError(f'"{k}" idêntico à original')
    user = mat + '\n\nQUESTÃO CORRETA:\n' + json.dumps({k: item[k] for k in ('alvo', 'tipo', 'pergunta', 'resposta', 'fatos')},
                                                       ensure_ascii=False)
    data = llm.json(DEFECT_SYSTEM, user, tag='qa_defeitos', max_tokens=8000, validate=check, item=item['id'])
    return [{**item, 'id': f"{item['qid']}::{k}", 'variante': k, 'pergunta': data[k]['pergunta'].strip(),
             'resposta': data[k]['resposta'].strip(), 'defeito': data[k].get('defeito', '')} for k in DEFEITOS]


def sample_for_defects(items, n, rng):
    by_type = defaultdict(list)
    for it in items:
        if it['status_geracao'] == 'aprovada':
            by_type[it['tipo']].append(it)
    chosen = []
    per = max(1, n // max(1, len(by_type)))
    for t in TIPOS:
        pool = by_type.get(t, [])
        chosen += rng.sample(pool, min(per, len(pool)))
    return chosen[:n]


def summarize(results, judges, items):
    variants = {it['id']: it for it in items}
    table = {}
    for j in judges:
        rs = [r for r in results if r['juiz'] == j and r['valido']]
        orig = [r for r in rs if r['variante'] == 'original']
        row = {'avaliados': len(rs), 'erros': sum(1 for r in results if r['juiz'] == j and not r['valido']),
               'aprovacao_originais': round(sum(r['aprovado'] for r in orig) / max(1, len(orig)), 3), 'n_originais': len(orig)}
        det = []
        for d in DEFEITOS:
            dv = [r for r in rs if r['variante'] == d]
            caught = [r for r in dv if not r['aprovado']]
            row[f'deteccao_{d}'] = round(len(caught) / max(1, len(dv)), 3)
            row[f'motivo_certo_{d}'] = round(sum(bool(set(r['falhas']) & ESPERADO[d]) for r in caught) / max(1, len(caught)), 3)
            row[f'n_{d}'] = len(dv)
            det.append(row[f'deteccao_{d}'])
        row['deteccao_media'] = round(sum(det) / len(det), 3)
        table[j] = row
    agree = {}
    for a, b in combinations(judges, 2):
        va = {r['item']: r['aprovado'] for r in results if r['juiz'] == a and r['valido'] and r['variante'] == 'original'}
        vb = {r['item']: r['aprovado'] for r in results if r['juiz'] == b and r['valido'] and r['variante'] == 'original'}
        common = sorted(set(va) & set(vb))
        agree[f'{a} x {b}'] = {'n': len(common), 'concordancia': round(sum(va[i] == vb[i] for i in common) / max(1, len(common)), 3),
                               'kappa': kappa([va[i] for i in common], [vb[i] for i in common])}
    return table, agree


def report(out, table, agree, results, items, judges, usage, elapsed):
    by_item = defaultdict(dict)
    for r in results:
        if r['valido']:
            by_item[r['item']][r['juiz']] = r
    lines = ['# Comparação de juízes', '',
             f'{sum(1 for i in items if i["variante"] == "original")} questões originais e '
             f'{sum(1 for i in items if i["variante"] != "original")} versões com defeito plantado. '
             f'Cada juiz avaliou cada item isoladamente, com o mesmo material. Tempo {elapsed / 60:.1f} min.', '',
             'Um bom juiz aprova a maior parte das originais (nem todas estão corretas) e reprova as versões com defeito. '
             '"Motivo certo" é a fração das detecções em que reprovou pela verificação esperada.', '',
             '| Juiz | aprova originais | detecta erro técnico | detecta sem suporte | detecta dependência de fonte | detecção média | erros | tokens entrada | tokens saída |',
             '|---|---:|---:|---:|---:|---:|---:|---:|---:|']
    for j in judges:
        t, u = table[j], usage.get(j, {})
        lines.append(f"| {j} | {t['aprovacao_originais']:.0%} | {t['deteccao_erro_tecnico']:.0%} ({t['motivo_certo_erro_tecnico']:.0%}) | "
                     f"{t['deteccao_sem_suporte']:.0%} ({t['motivo_certo_sem_suporte']:.0%}) | "
                     f"{t['deteccao_dependencia_fonte']:.0%} ({t['motivo_certo_dependencia_fonte']:.0%}) | "
                     f"{t['deteccao_media']:.0%} | {t['erros']} | {u.get('prompt_tokens', 0):,} | {u.get('completion_tokens', 0):,} |")
    lines += ['', '| Par de juízes | concordância nas originais | kappa |', '|---|---:|---:|']
    lines += [f"| {k} | {v['concordancia']:.0%} | {v['kappa']} |" for k, v in agree.items()]
    lines += ['', '## Originais com divergência entre juízes', '',
              '_Para o especialista decidir: quem está certo em cada caso._', '']
    for it in items:
        if it['variante'] != 'original':
            continue
        votes = by_item.get(it['id'], {})
        if len({r['aprovado'] for r in votes.values()}) < 2:
            continue
        lines += [f"### {it['qid']} · {it['tipo']} · {it['subtopico']}", '', f"**P:** {it['pergunta']}", '',
                  f"**R:** {it['resposta']}", '']
        for j, r in votes.items():
            why = '; '.join(r['problemas'][:3]) or ', '.join(r['falhas'])
            lines.append(f"- **{j}:** {'aprova' if r['aprovado'] else 'reprova (' + ', '.join(r['falhas']) + ')'}"
                         + (f" · {why}" if not r['aprovado'] and why else ''))
        lines.append('')
    misses = [r for r in results if r['valido'] and r['variante'] != 'original' and r['aprovado']]
    lines += ['## Defeitos plantados que passaram', '']
    for r in misses[:60]:
        it = next(i for i in items if i['id'] == r['item'])
        lines.append(f"- **{r['juiz']}** aprovou `{r['item']}` ({it['variante']}): {it.get('defeito', '')}")
    (out / 'relatorio_juizes.md').write_text('\n'.join(lines) + '\n', encoding='utf-8')


def main(argv=None, clients=None):
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument('--inventarios', nargs='+', required=True)
    p.add_argument('--questoes', required=True, help='questoes.jsonl produzido por gerar_qa.py')
    p.add_argument('--saida', required=True)
    p.add_argument('--juizes', nargs='+', required=True, help='deployment:effort de cada juiz')
    p.add_argument('--gerador-defeitos', default='gpt-5-4-petrobras:low')
    p.add_argument('--defeitos', type=int, default=32, help='questões originais que recebem versões com defeito')
    p.add_argument('--limite-originais', type=int, default=0)
    p.add_argument('--llm-provider', choices=['azure', 'openai'], default='azure')
    p.add_argument('--workers', type=int, default=8)
    p.add_argument('--max-chamadas', type=int, default=4000)
    p.add_argument('--seed', type=int, default=11)
    p.add_argument('--env', default=None)
    a = p.parse_args(argv)
    for spec in [*a.juizes, a.gerador_defeitos]:
        parse_role(spec)
    if len(set(a.juizes)) != len(a.juizes):
        raise SystemExit('Juízes repetidos')
    load_dotenv(Path(a.env) if a.env else ROOT)
    out = Path(a.saida)
    out.mkdir(parents=True, exist_ok=True)
    subs = {s['key']: s for s in load_inventory(a.inventarios)}
    rows = [q for q in read_jsonl(a.questoes) if 'pergunta' in q and q.get('sub_key') in subs]
    if a.limite_originais:
        rows = rows[:a.limite_originais]
    if not rows:
        raise SystemExit('Nenhuma questão utilizável em --questoes')
    rng = random.Random(a.seed)
    originals = [base_item(q) for q in rows]
    mats = {q['id']: item_material(subs, q) for q in rows}
    judges = clients['juizes'] if clients else {j: make_client(j, a.llm_provider, out, a.max_chamadas, 'juiz') for j in a.juizes}
    maker = clients['defeitos'] if clients else make_client(a.gerador_defeitos, a.llm_provider, out, a.max_chamadas, 'defeitos')
    t0 = time.time()

    variants = []
    chosen = sample_for_defects(originals, a.defeitos, rng)
    with ThreadPoolExecutor(a.workers) as pool:
        futs = {pool.submit(make_defects, maker, mats[it['qid']], it): it for it in chosen}
        for f in as_completed(futs):
            try:
                variants += f.result()
            except (ContentFiltered, CallFailed) as e:
                print(f"[juizes] defeitos não gerados para {futs[f]['qid']}: {e}", flush=True)
    items = originals + sorted(variants, key=lambda x: x['id'])
    print(f'[juizes] {len(originals)} originais + {len(variants)} variantes com defeito | juízes: {", ".join(a.juizes)}', flush=True)

    def evaluate(judge, it):
        base = {'juiz': judge, 'item': it['id'], 'qid': it['qid'], 'variante': it['variante'], 'tipo': it['tipo']}
        try:
            v = judge_items(judges[judge], mats[it['qid']], [it], it['id'])[it['id']]
        except (ContentFiltered, CallFailed) as e:
            return {**base, 'valido': False, 'erro': str(e)[:300]}
        return {**base, 'valido': True, 'aprovado': verdict_ok(v), 'falhas': failed_checks(v),
                'problemas': [str(x) for x in v.get('problemas') or []], 'parecer': v}
    results = []
    with ThreadPoolExecutor(a.workers) as pool:
        futs = [pool.submit(evaluate, j, it) for j in a.juizes for it in items]
        for i, f in enumerate(as_completed(futs), 1):
            results.append(f.result())
            if i % 50 == 0:
                print(f'[juizes] {i}/{len(futs)} avaliações', flush=True)
    elapsed = time.time() - t0
    usage = {j: c.usage for j, c in judges.items()}
    table, agree = summarize(results, a.juizes, items)
    write_jsonl(out / 'itens.jsonl', items)
    write_jsonl(out / 'avaliacoes.jsonl', sorted(results, key=lambda r: (r['juiz'], r['item'])))
    report(out, table, agree, results, items, a.juizes, usage, elapsed)
    resumo = {'version': VERSION, 'juizes': table, 'concordancia': agree, 'uso': usage, 'uso_defeitos': maker.usage,
              'originais': len(originals), 'variantes': len(variants), 'tempo_s': round(elapsed, 1)}
    atomic_json(out / 'resumo_juizes.json', resumo)
    print('[juizes] fim ' + json.dumps(table, ensure_ascii=False), flush=True)
    return resumo


if __name__ == '__main__':
    main()
