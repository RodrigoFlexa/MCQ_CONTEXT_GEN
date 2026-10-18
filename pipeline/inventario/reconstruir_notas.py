"""Refaz notas/revisão/combinações a partir dos artefatos existentes, sem reextrair fatos.

Uma saída nova preserva os experimentos anteriores. --plan não usa APIs.
"""
import argparse
import json
import sys
import time
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from pipeline.inventario import notas as N, revisao as R, combinacoes as M
from pipeline.inventario.llm import LLMClient, load_dotenv
from pipeline.inventario.locking import output_lock
from pipeline.inventario.run_inventario import Pipeline, Log, Ocorrencias, parse as base_args, finish
from pipeline.inventario.textutil import read_json, read_jsonl, atomic_json, sha, norm


def parse(argv=None):
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('--origens', nargs='+', required=True)
    p.add_argument('--saida', required=True)
    p.add_argument('--subtopicos', nargs='*', default=[])
    p.add_argument('--limite-conceitos-por-subtopico', type=int)
    p.add_argument('--workers', type=int, default=8)
    p.add_argument('--modelo', default='gpt-5-4-petrobras')
    p.add_argument('--effort', choices=('low', 'medium', 'high'), default='low')
    p.add_argument('--provider', choices=('azure', 'openai'), default='azure')
    p.add_argument('--max-chamadas', type=int, default=30000)
    p.add_argument('--embedder', choices=('embedding-3-large-global', 'hash'), default='embedding-3-large-global')
    p.add_argument('--sem-complemento-notas', action='store_true')
    p.add_argument('--plan', action='store_true')
    a = p.parse_args(argv)
    if a.workers < 1 or a.max_chamadas < 1 or (
            a.limite_conceitos_por_subtopico is not None and a.limite_conceitos_por_subtopico < 1):
        p.error('workers, orçamento e limite devem ser positivos')
    return a


def load_sources(args):
    subs, by_sub, facts, chunks, plans, selections, candidates, fingerprints = [], {}, {}, {}, {}, {}, {}, []
    for origin in args.origens:
        root = Path(origin).resolve()
        if not root.is_dir():
            raise ValueError(f'inventário ausente: {root}')
        for folder in sorted((root / 'subtopicos').iterdir()):
            if not folder.is_dir():
                continue
            ass = read_json(folder / 'assuntos.json')
            if not ass:
                continue
            sub = ass['subtopico']
            if args.subtopicos and not any(norm(t) in norm(sub['subtopico']) for t in args.subtopicos):
                continue
            if any(s['key'] == sub['key'] for s in subs):
                raise ValueError(f'subtópico duplicado nas origens: {sub["subtopico"]}')
            for name in ('assuntos.json', 'selecao.json', 'fatos.jsonl', 'conceitos.json'):
                path = folder / name
                if not path.exists():
                    raise ValueError(f'artefato necessário ausente: {path}')
                fingerprints.append([str(path), sha(path.read_text(encoding='utf-8'), 40)])
            sub = {**sub, 'dir': folder.name}
            original_plans = read_json(folder / 'conceitos.json')
            # Round-robin entre assuntos: piloto não concentra todas as notas no primeiro.
            chosen = {aid: [] for aid in original_plans}
            queues = {aid: list(p['conceitos']) for aid, p in original_plans.items()}
            remaining = args.limite_conceitos_por_subtopico
            while any(queues.values()) and (remaining is None or remaining > 0):
                for aid in queues:
                    if queues[aid] and (remaining is None or remaining > 0):
                        chosen[aid].append(queues[aid].pop(0))
                        if remaining is not None:
                            remaining -= 1
            selected_plans = {aid: {**original_plans[aid], 'conceitos': ks} for aid, ks in chosen.items() if ks}
            if not selected_plans:
                continue
            subs.append(sub)
            sk = sub['key']
            by_sub[sk] = [a for a in ass['assuntos'] if a['id'] in selected_plans]
            plans[sk] = selected_plans
            facts[sk] = read_jsonl(folder / 'fatos.jsonl')
            all_selections = read_json(folder / 'selecao.json')['assuntos']
            selections[sk] = {aid: data for aid, data in all_selections.items() if aid in selected_plans}
            for aid, data in all_selections.items():
                candidates[f'{sk}::{aid}'] = list(data['trechos'])
                for chunk in data['trechos']:
                    chunks[chunk['chunk_id']] = chunk
        # Se disponíveis, candidatos não selecionados ampliam o complemento sem nova varredura.
        index = root / 'indices'
        if (index / 'trechos.jsonl').exists() and (index / 'candidatos.jsonl').exists():
            pool = {c['chunk_id']: c for c in read_jsonl(index / 'trechos.jsonl')}
            selected_keys = {s['key'] for s in subs}
            for row in read_jsonl(index / 'candidatos.jsonl'):
                if row['akey'].split('::', 1)[0] in selected_keys and row['chunk_id'] in pool:
                    candidates.setdefault(row['akey'], []).append(pool[row['chunk_id']])
            for name in ('trechos.jsonl', 'candidatos.jsonl'):
                fingerprints.append([str(index / name), sha((index / name).read_text(encoding='utf-8'), 40)])
    if not subs:
        raise ValueError('nenhum subtópico com conceitos corresponde aos filtros')
    return subs, by_sub, facts, chunks, plans, selections, candidates, fingerprints


def main(argv=None, llm=None, embedder=None):
    args = parse(argv)
    out = Path(args.saida).resolve()
    for src in args.origens:
        source = Path(src).resolve()
        if out == source or source in out.parents:
            raise ValueError('use uma saída nova fora dos inventários de origem')
    subs, by_sub, facts, chunks, plans, selections, candidates, fingerprint = load_sources(args)
    counts = {s['subtopico']: sum(len(p['conceitos']) for p in plans[s['key']].values()) for s in subs}
    if args.plan:
        print(json.dumps({'schema': N.K.SCHEMA, 'conceitos': counts, 'chamadas': 0}, ensure_ascii=False, indent=2))
        return counts
    identity = {k: v for k, v in vars(args).items() if k not in ('workers', 'max_chamadas', 'plan', 'saida')}
    signature = sha(json.dumps([identity, fingerprint, N.VERSION, R.VERSION, M.VERSION], sort_keys=True), 40)
    with output_lock(out):
        previous = read_json(out / 'run_config.json')
        if previous and previous.get('signature') != signature:
            raise ValueError('configuração ou fontes mudaram; escolha outra saída')
        if not previous and any(out.glob('subtopicos/*/notas*.jsonl')):
            raise ValueError('saída já contém notas sem configuração compatível; escolha outra pasta')
        atomic_json(out / 'run_config.json', {'signature': signature, 'args': vars(args), 'fontes': fingerprint,
                                             'notas_version': N.VERSION, 'revisao_version': R.VERSION})
        log, t0 = Log(out / 'execucao.log'), time.time()
        log('[reconstrução] conceitos:', json.dumps(counts, ensure_ascii=False))
        load_dotenv(ROOT)
        owned_llm, owned_emb = llm is None, embedder is None
        if owned_llm:
            llm = LLMClient(args.modelo, args.effort, out / 'cache/llm_cache.sqlite3',
                            out / 'chamadas_llm.jsonl', max_calls=args.max_chamadas, provider=args.provider)
        try:
            from pipeline.inventario.modelos import EmbeddingCache, load_models
            if owned_emb:
                embedder, _ = load_models(args.embedder, 'none', 'cpu', output=out)
            cache = EmbeddingCache(out / 'indices/emb_cache.npz', args.embedder)
            options = base_args([])
            options.sem_complemento_notas = args.sem_complemento_notas
            with ThreadPoolExecutor(max_workers=args.workers) as pool:
                pipe = Pipeline(options, out, log, llm, pool, Ocorrencias(out / 'ocorrencias.jsonl'),
                                subs, None, [], t0)
                pipe.candidates = candidates
                notes = pipe.stage_notas(by_sub, facts, chunks, plans, embedder, cache)
                cache.save()
                combos = pipe.stage_combinacoes(by_sub, notes)
                rows = pipe.stage_documentos(by_sub, selections, facts, plans, notes, combos)
                return finish(out, log, llm, pipe.occ, pipe.timings, t0, rows=rows, notes=notes)
        finally:
            if owned_llm:
                llm.close()
            if owned_emb and embedder is not None and hasattr(embedder, 'close'):
                embedder.close()


if __name__ == '__main__':
    main()
